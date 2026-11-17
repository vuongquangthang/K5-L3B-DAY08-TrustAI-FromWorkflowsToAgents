# Báo cáo cá nhân — 2A202603756_LaThaiMinh

## 1. Thông tin thành viên

- Họ tên: Lã Thái Minh
- MSSV: 2A202603756
- Email: 26ai.minhlt4@vinuni.edu.vn
- GitHub: [minh17023](https://github.com/minh17023)

## 2. Phần việc phụ trách

Phụ trách M3/CP4: rà soát việc chặn các approval không hợp lệ, kiểm tra dữ liệu nhạy cảm trong trace và stdout, và xác nhận khả năng phục hồi sau crash trên ba shape `workflow`, `single`, `orchestrator`.

## 3. Đóng góp cụ thể

- Commit chính: [`e8caa59`](https://github.com/vuongquangthang/K5-L3B-DAY08-TrustAI-FromWorkflowsToAgents/commit/e8caa599b99e3658853ef9e14a33b9aa1ae82acd) — thêm `src/tests/test_cp4_safety.py` và báo cáo `src/reports/crash.json` do công cụ lab sinh ra.
- Thêm 27 trường hợp test CP4 trên ba shape: 5 loại approval sai (thiếu, thuộc claim khác, bị thu hồi, hết hạn, số tiền bằng 0), kiểm tra trace/stdout không lộ canary và thông tin cá nhân, cùng 3 điểm crash (`before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`).
- Kiểm tra quote dương bị host từ chối vẫn giữ `proposal_amount = 35000`, không tạo refund hoặc audit `refund_committed`, và có audit `policy_denied` với đúng lý do. Kiểm tra retry sau crash chỉ để lại một dòng ledger và một audit `refund_committed`.
- Không thay đổi thước đo, dữ liệu public, policy hay code host. Phần kiểm chứng giữ nguyên ranh giới: shape gọi host để duyệt và ghi tiền; trace chỉ chứa dữ liệu đã lọc.

## 4. Bằng chứng

- Ba test đã thêm: `test_cp4_bad_approval_never_pays`, `test_cp4_trace_and_stdout_omit_untrusted_and_private_data`, `test_cp4_each_shape_recovers_without_double_refund` trong [`src/tests/test_cp4_safety.py`](../../src/tests/test_cp4_safety.py).
- Chạy `python -m pytest -q tests/test_cp4_safety.py`: **27 passed**.
- Chạy `python -m pytest -q`: **90 passed, 248 deselected**. Ma trận student trước khi thêm test CP4: **248 passed, 63 deselected**.
- Chạy `python -m lab8.crash_test --count 20 --out reports/crash.json`: **`crash_safety = 20/20`** trong [`src/reports/crash.json`](../../src/reports/crash.json).
- Báo cáo crash gồm 20 kịch bản pass. Đây là crash suite của lab; test mới bổ sung kiểm chứng resume qua cả ba shape.

## 5. Công cụ AI đã dùng

- Codex (OpenAI): đọc contract và code M1/M2, hỗ trợ viết các test CP4, chạy test và kiểm tra kết quả trước khi commit.
- Tự kiểm chứng bằng output của pytest, báo cáo crash do lệnh của lab sinh ra, `git diff --check` và lịch sử commit. Không dùng AI để tạo số liệu kiểm thử hoặc sửa tay JSON báo cáo.

## 6. Tự đánh giá

Đã hoàn thành phần kiểm chứng M3/CP4 trên dữ liệu public: các nhánh approval được test, trace/stdout không chứa chuỗi nhạy cảm được kiểm tra, và crash suite đạt 20/20. Phạm vi chứng cứ hiện tại là bộ public và test tự bổ sung; kết quả hidden do grader của giảng viên quyết định.
