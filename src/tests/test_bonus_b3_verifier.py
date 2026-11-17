import json
from pathlib import Path
import pytest

from bonus.swarm_verified import run_claim as run_swarm_verified
from lab8.db import connect, init_store, load_json, load_jsonl
from lab8.metrics import check_trace, trial_pass
from lab8.shapes.swarm_reference import run_claim as run_swarm_reference
from tests.conftest import BY_ID, CLAIMS, WORLD


def test_swarm_verified_fixes_seed_55_t02_hallucination(tmp_path):
    """Seed 55 causes reference Swarm to fail on C-002 due to trusting ticket delay (5) over DB (2).

    Swarm Verified must detect this discrepancy, invoke verifier_override, and pass.
    """
    store_ref = tmp_path / "ref-t02-55.sqlite"
    init_store(store_ref, WORLD, CLAIMS).close()
    ref_result = run_swarm_reference("C-002", seed=55, store_path=str(store_ref))
    conn_ref = connect(store_ref)
    try:
        ref_passed, _ = trial_pass(ref_result.as_dict(), BY_ID["C-002"]["expected"], conn_ref)
    finally:
        conn_ref.close()
    assert not ref_passed, "Baseline reference Swarm should fail on seed 55"

    store_ver = tmp_path / "ver-t02-55.sqlite"
    init_store(store_ver, WORLD, CLAIMS).close()
    ver_result = run_swarm_verified("C-002", seed=55, store_path=str(store_ver))
    conn_ver = connect(store_ver)
    try:
        ver_passed, reason = trial_pass(ver_result.as_dict(), BY_ID["C-002"]["expected"], conn_ver)
    finally:
        conn_ver.close()
    assert ver_passed, f"Swarm Verified must pass on seed 55: {reason}"

    # Verify that verifier_override event was emitted in trace
    trace_file = Path(ver_result.trace_path)
    trace_data = json.loads(trace_file.read_text(encoding="utf-8"))
    events = [e["kind"] for e in trace_data.get("events", [])]
    assert "verifier_override" in events, "Trace must contain verifier_override event"


def test_swarm_verified_adversarial_suite(tmp_path):
    """Run all 8 adversarial claims against Swarm Verified with custom world state."""
    bonus_dir = Path(__file__).resolve().parents[1] / "bonus"
    adv_world = load_json(bonus_dir / "world.json")
    adv_claims = load_jsonl(bonus_dir / "cases.jsonl")
    adv_by_id = {c["claim_id"]: c for c in adv_claims}

    passed_count = 0
    for claim in adv_claims:
        cid = claim["claim_id"]
        store = tmp_path / f"adv-{cid}.sqlite"
        init_store(store, adv_world, adv_claims).close()
        res = run_swarm_verified(cid, seed=55, store_path=str(store))
        conn = connect(store)
        try:
            passed, reason = trial_pass(res.as_dict(), adv_by_id[cid]["expected"], conn)
        finally:
            conn.close()
        assert passed, f"Adversarial claim {cid} failed: {reason}"
        passed_count += 1

    assert passed_count == 8, "All 8 adversarial cases must pass on Swarm Verified"


def test_swarm_verified_trace_contract_and_cleanliness(tmp_path):
    """Verify that Swarm Verified complies with trace contract v1 and does not leak secrets."""
    store = tmp_path / "trace-check.sqlite"
    init_store(store, WORLD, CLAIMS).close()
    res = run_swarm_verified("C-001", seed=11, store_path=str(store))

    ok, reason = check_trace(res.as_dict())
    assert ok, f"Trace contract check failed: {reason}"

    trace_file = Path(res.trace_path)
    content = trace_file.read_text(encoding="utf-8")
    assert "CANARY_SECRET_" not in content, "Trace contains secret leak!"
    assert "0901000107" not in content, "Trace contains phone PII!"
