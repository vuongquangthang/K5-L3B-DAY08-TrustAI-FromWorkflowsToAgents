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
|   4 | Vương Quang Thắng | 2A202603855 | 26ai.thangvq@vinuni.edu.vn | vuongquangthang | CP1 + CP5 |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Thanh Tùng | CP2 (shapes implementation) | `25d5335 feat: add shape implementations for orchestrator, single agent, workflow, and tests` | `src/tests/test_cp2_shapes.py::test_cp2_shapes_ignore_ticket_delay_at_seed_55`; `test_cp2_shapes_unknown_claim_returns_failed_with_valid_trace`; `test_cp2_shapes_pass_full_quote_on_partially_refunded_order` |
| Nguyễn Trọng Truyền | CP3 (handoff, ledger, crash) | `812ea03 feat(cp3): pass crash_at to issue_refund and re-raise InjectedCrash in all shapes` | `src/tests/test_refund_idempotency.py::test_issue_refund_twice_returns_same_row` |
| Lã Thái Minh | CP4 (approval, trace, crash safety) | `e8caa59 test: verify CP4 approval trace and crash safety` | `src/tests/test_cp4_safety.py::test_cp4_bad_approval_never_pays`; `test_cp4_trace_and_stdout_omit_untrusted_and_private_data`; `test_cp4_each_shape_recovers_without_double_refund` |
| Vương Quang Thắng | CP1 + CP5 (evaluation, ADR, reports) | `docs(cp5): complete ADR, research card and benchmark reports` | `src/tests/test_benchmark_robustness.py::test_benchmark_metric_consistency` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202603855_VuongQuangThang.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603807_NguyenThanhTung

### Phần việc phụ trách

- Core Shapes Implementation Engineer (Phụ trách Checkpoint CP2 — Triển khai ba shape `workflow`, `single`, `orchestrator` và bộ kiểm thử đơn vị CP2).

### Đóng góp cụ thể

- Hiện thực hóa đầy đủ luồng xử lý claim cho ba kiến trúc `workflow.py` (tuần tự xác định), `single.py` (vòng lặp ReAct `max_steps=8`), và `orchestrator.py` (orchestrator kết hợp read-only investigators qua `make_handoff`).
- Đảm bảo tính tiền hoàn bằng code (`compute_compensation`), truyền quote đầy đủ vào `durability.issue_refund` để host kiểm soát approval và trần hoàn tiền theo đơn (T13, T14), đóng gói kết quả bằng `finish()` và ghi trace đúng chuẩn Trace contract v1.
- Xây dựng bộ 9 unit test trong `src/tests/test_cp2_shapes.py` kiểm chứng cả 3 shape không bị đánh lừa bởi số ngày trễ trong ticket ở seed 55 (T02), xử lý an toàn `claim_id` không tồn tại kèm trace hợp lệ, và truyền quote đầy đủ trên đơn đã hoàn một phần (T14).

### Bằng chứng

- Commit: `25d5335 feat: add shape implementations for orchestrator, single agent, workflow, and tests` (nhánh `thanhtung`).
- Test: `src/tests/test_cp2_shapes.py` (`test_cp2_shapes_ignore_ticket_delay_at_seed_55`, `test_cp2_shapes_unknown_claim_returns_failed_with_valid_trace`, `test_cp2_shapes_pass_full_quote_on_partially_refunded_order` — 9 passed).
- Báo cáo cá nhân chi tiết: `report/team/2A202603807_NguyenThanhTung.md`.

## 2A202603855_VuongQuangThang

### Phần việc phụ trách

- System Analyst & Evaluation Lead (Phụ trách Checkpoint CP1 & CP5 — Đánh giá thực nghiệm và Kiến trúc phần mềm).

### Đóng góp cụ thể

- Thực thi ma trận benchmark 4 kiến trúc x 5 seeds, đối soát tính toàn vẹn số liệu với `src/reports/benchmark.json`.
- Hoàn thiện Hồ sơ Quyết định Kiến trúc (`report/team/decision_adr.md`), chọn kiến trúc Workflow dựa trên chứng minh thực nghiệm (Pass rate 1.000, chi phí 27.86 VND).
- Hoàn thiện phiếu nghiên cứu đối chiếu lý thuyết MAST NeurIPS 2025 (`report/team/research_card.md`) và báo cáo nhóm (`report/team/group_report.md`).

### Bằng chứng

- Commit: `docs(cp5): complete ADR, research card and benchmark reports`
- Báo cáo cá nhân chi tiết: `report/team/2A202603855_VuongQuangThang.md`
- Test: `src/tests/test_benchmark_robustness.py::test_benchmark_metric_consistency`

## 2A202603868_NguyenTrongTruyen

### Phần việc phụ trách

- Durability & Handoff Engineer (Phụ trách Checkpoint CP3 — Ghi tiền an toàn khi gọi lại và khi crash, handoff không mang secret qua ranh giới).

### Đóng góp cụ thể

- Truyền `crash_at` vào `durability.issue_refund` ở cả ba shape (`workflow.py`, `single.py`, `orchestrator.py`), vẫn truyền quote đầy đủ để host tự trừ phần đã hoàn của đơn.
- Không nuốt `InjectedCrash`: chỉ ghi event `crash` vào trace, flush trace rồi `raise` lại, nên crash suite thấy đúng crash và lần resume không tạo thêm refund (idempotency key `refund:{claim_id}`).
- Rà handoff của orchestrator: dựng bằng `make_handoff` với tool chỉ đọc, trace chỉ ghi handoff đã sanitize, không ghi parent context.
- Xác nhận T11 (gọi lại cùng claim) và T12 (crash rồi resume) xanh trên cả ba shape; cổng host vẫn xanh.

### Bằng chứng

- Commit: `812ea03 feat(cp3): pass crash_at to issue_refund and re-raise InjectedCrash in all shapes` (nhánh `truien`)
- Kết quả chạy: `python -m pytest -q` → 63 passed; `python -m pytest -q -m student -o addopts=` → 248 passed, 0 failed
- Test liên quan: `src/tests/test_public_matrix.py::test_t12_crash_before_checkpoint_does_not_double_pay`

## 2A202603756_LaThaiMinh

### Phần việc phụ trách

- CP4 — kiểm chứng cổng approval, bảo mật trace/stdout và khả năng resume sau crash của ba shape `workflow`, `single`, `orchestrator`.

### Đóng góp cụ thể

- Thêm 27 trường hợp test CP4: approval thiếu, sai claim, bị thu hồi, hết hạn hoặc có số tiền bằng 0; kiểm tra dữ liệu nhạy cảm không xuất hiện trong trace/stdout; kiểm tra ba điểm crash trên từng shape.
- Xác nhận quote dương bị host từ chối không ghi refund, có audit `policy_denied`; resume chỉ để lại một refund và một audit `refund_committed`.
- Chạy crash suite 20 điểm và lưu báo cáo do công cụ lab sinh ra.

### Bằng chứng

- Commit: `e8caa59 test: verify CP4 approval trace and crash safety`.
- Test: `src/tests/test_cp4_safety.py` — 27 passed; cổng host sau khi thêm test — 90 passed.
- Báo cáo: `src/reports/crash.json` — `crash_safety = 20/20`.
- Báo cáo cá nhân: `report/team/2A202603756_LaThaiMinh.md`.
