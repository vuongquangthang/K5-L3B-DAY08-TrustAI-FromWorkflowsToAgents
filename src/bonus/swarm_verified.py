"""Shape Bonus B3 — Swarm Verified (Code-based verifier & aggregator).

Inherits the peer communication and investigator workflow from reference Swarm,
but inserts a deterministic code-level Verifier before issuing refund decisions.
The verifier reconciles extracted/hallucinated claim facts against structured order
records in SQLite DB, intercepting errors (such as seed 55 T02 delay hallucination)
and preventing error amplification as described in Google Research (2026).
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.handoff import make_handoff
from lab8.mock_llm import complete, parse_delay_days
from lab8.runtime import run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import compute_compensation, tool_cost


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn: sqlite3.Connection, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    run_id = make_run_id("swarm_verified", claim_id, seed)
    trace = _Trace(run_id)
    budget.add_tool(tool_cost())

    claim_row = conn.execute(
        "SELECT claim_id, principal_id, order_id, ticket FROM claims WHERE claim_id = ?",
        (claim_id,),
    ).fetchone()
    if claim_row is None:
        trace.add("error", {"reason": "unknown_claim"})
        return finish(
            conn,
            shape="swarm_verified",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="unknown_claim",
        )

    ticket = claim_row["ticket"]
    # 1. Peer deliberation & ticket parsing (Swarm cognitive layer)
    complete(budget, seed=seed, purpose="peer", prompt=ticket)
    parsed_delay = parse_delay_days(ticket)
    complete(budget, seed=seed, purpose="parse", prompt=ticket)

    # 2. Missing order validation
    if not claim_row["order_id"]:
        complete(budget, seed=seed, purpose="draft", prompt="needs_info")
        trace.add("decision", {"status": "needs_info"})
        return finish(
            conn,
            shape="swarm_verified",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="missing_order_id",
        )

    # 3. Handoff to read-only investigators
    handoff = make_handoff(
        request_id=f"REQ-{claim_id}",
        claim_id=claim_id,
        task="check_applicable_policy",
        facts={},
        allowed_tools=["lookup_order", "lookup_policy", "compute_compensation"],
    )
    trace.add("handoff", safe_dump(handoff))
    investigated = run_readonly_investigators(
        conn, budget, handoff, principal_id=claim_row["principal_id"]
    )
    order_view = investigated["tools"].get("lookup_order", {})
    trace.add(
        "investigator",
        {
            "lookup_order": order_view,
            "policy_count": len((investigated["tools"].get("lookup_policy") or {}).get("policies") or []),
        },
    )

    if not order_view.get("visible"):
        complete(budget, seed=seed, purpose="draft", prompt="escalated")
        return finish(
            conn,
            shape="swarm_verified",
            claim_id=claim_id,
            seed=seed,
            status="escalated",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=order_view.get("reason"),
        )

    structured_order = order_view["order"]
    order = dict(structured_order)

    # Swarm reference heuristic/weakness: agent trusts ticket over DB facts on seed % 5 == 0
    if parsed_delay is not None and parsed_delay != int(order["delay_days"]) and seed % 5 == 0:
        order["delay_days"] = parsed_delay
        trace.add("model_override", {"delay_days": parsed_delay})

    # =========================================================================
    # CODE-LEVEL VERIFIER & RECONCILIATION LAYER (Topic B3)
    # Compares candidate order facts with ground truth DB records.
    # Reverts hallucinated / distorted fields and emits 'verifier_override'.
    # =========================================================================
    discrepancies: dict[str, dict[str, object]] = {}
    for fact_key in ("delay_days", "status", "damage_verified"):
        candidate_val = order.get(fact_key)
        db_val = structured_order.get(fact_key)
        if candidate_val != db_val:
            discrepancies[fact_key] = {
                "candidate": candidate_val,
                "verified_db": db_val,
            }

    if discrepancies:
        for fact_key in discrepancies:
            order[fact_key] = structured_order[fact_key]
        trace.add(
            "verifier_override",
            {
                "action": "reconcile_with_ground_truth_order",
                "discrepancies": discrepancies,
                "reason": "prevent_hallucination_amplification",
            },
        )

    # 4. Compensation calculation with verified facts
    budget.add_tool(tool_cost())
    quote_payload = compute_compensation(conn, order)
    proposal = int(quote_payload["amount_vnd"])
    trace.add("quote", quote_payload)
    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal}")

    if proposal <= 0:
        return finish(
            conn,
            shape="swarm_verified",
            claim_id=claim_id,
            seed=seed,
            status="denied",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=quote_payload.get("reason"),
        )

    # 5. Issue refund through durability host
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    if not outcome["ok"]:
        status = "failed" if outcome["conflict"] else "denied"
        return finish(
            conn,
            shape="swarm_verified",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=outcome["reason"],
        )

    return finish(
        conn,
        shape="swarm_verified",
        claim_id=claim_id,
        seed=seed,
        status="resolved",
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=None,
    )


class _Trace:
    """Trace contract v1 wrapper."""

    def __init__(self, run_id: str) -> None:
        from lab8.trace import Trace

        self._inner = Trace(run_id)

    def add(self, kind: str, payload: dict) -> None:
        self._inner.add(kind, payload)

    def write(self) -> str:
        return self._inner.write()

    @property
    def run_id(self) -> str:
        return self._inner.run_id
