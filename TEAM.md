# Team

## Thông tin nhóm

- Tên nhóm: TrustAI
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY08-TrustAI-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: main / [ĐIỀN_COMMIT_HASH_7_KY_TU_O_DAY]

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Thanh Tùng | 2A202603807 | 26ai.tungnt7@vinuni.edu.vn | thanhtung578804 | CP2 |
|   2 | Nguyễn Trọng Truyền | 2A202603868 | 26ai.truyennt2@vinuni.edu.vn | truien | CP3 |
|   3 | Lã Thái Minh | 2A202603756 | 26ai.minhlt4@vinuni.edu.vn | minh17023 | CP4 |
|   4 | Vương Quang Thắng | 2A202603855 | 26ai.thangvq@vinuni.edu.vn | vuongquangthang | CP1 + CP5 + Bonus B3 |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Thanh Tùng | CP2 (shapes implementation) | `25d5335 feat: add shape implementations for orchestrator, single agent, workflow, and tests` | `src/tests/test_cp2_shapes.py::test_workflow_deterministic_flow` |
| Nguyễn Trọng Truyền | CP3 (handoff, ledger, crash) | `812ea03 feat(cp3): pass crash_at to issue_refund and re-raise InjectedCrash in all shapes` | `src/tests/test_refund_idempotency.py::test_issue_refund_twice_returns_same_row` |
| Lã Thái Minh | CP4 (safety, approval, secret) | `e8caa59 test: verify CP4 approval trace and crash safety` | `src/tests/test_cp4_safety.py::test_approval_bound_to_claim` |
| Vương Quang Thắng | CP1 + CP5 + Bonus B3 (evaluation, ADR, bonus verifier) | `feat(bonus): implement swarm_verified B3, adversarial suite and reports` | `src/tests/test_bonus_b3_verifier.py::test_swarm_verified_fixes_seed_55_t02_hallucination` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202603855_VuongQuangThang.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603855_VuongQuangThang

### Phần việc phụ trách

- System Analyst & Evaluation Lead (Phụ trách Checkpoint CP1, CP5 và Topic Bonus B3 — Đánh giá thực nghiệm, Kiến trúc phần mềm và Verifier chống khuếch đại lỗi).

### Đóng góp cụ thể

- Thực thi ma trận benchmark 4 kiến trúc x 5 seeds, đối soát tính toàn vẹn số liệu với `src/reports/benchmark.json`.
- Hoàn thiện Hồ sơ Quyết định Kiến trúc (`report/team/decision_adr.md`), chọn kiến trúc Workflow dựa trên chứng minh thực nghiệm (Pass rate 1.000, chi phí 27.86 VND).
- Hoàn thiện phiếu nghiên cứu đối chiếu lý thuyết MAST NeurIPS 2025 (`report/team/research_card.md`) và báo cáo nhóm (`report/team/group_report.md`).
- **Nhiệm vụ Điểm cộng (Bonus B3 - Google Research 2026)**:
  + Hiện thực hóa kiến trúc `swarm_verified` tại `src/bonus/swarm_verified.py`, tích hợp Code Verifier & Reconciler đối chiếu dữ kiện với SQLite DB, sửa triệt để lỗi ảo giác tại seed 55 (`status resolved != denied`).
  + Xây dựng bộ dữ liệu 8 khiếu nại đối kháng tại `src/bonus/cases.jsonl` và `src/bonus/world.json`.
  + Viết bộ test `src/tests/test_bonus_b3_verifier.py` (3 test pass 100%).
  + Chạy benchmark thực nghiệm `src/reports/bonus_benchmark.json` (Pass rate 1.000, Pass^5 1.000, variance 0.000000) và hoàn thành báo cáo `report/team/bonus_report.md`.

### Bằng chứng

- Commit: `feat(bonus): implement swarm_verified B3, adversarial suite and reports`
- Báo cáo cá nhân chi tiết: `report/team/2A202603855_VuongQuangThang.md`
- Báo cáo Bonus: `report/team/bonus_report.md`
- Dữ liệu benchmark: `src/reports/bonus_benchmark.json`
- Tests: `src/tests/test_bonus_b3_verifier.py::test_swarm_verified_fixes_seed_55_t02_hallucination`
