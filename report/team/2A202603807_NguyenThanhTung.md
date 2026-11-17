# Báo cáo cá nhân — 2A202603807_NguyenThanhTung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thanh Tùng
- MSSV: 2A202603807
- Email: 26ai.tungnt7@vinuni.edu.vn
- GitHub: thanhtung578804

## 2. Phần việc phụ trách

- **Vai trò trong nhóm**: Core Shapes Implementation Engineer (Phụ trách Checkpoint CP2 — Triển khai ba kiến trúc xử lý claim: `workflow`, `single`, `orchestrator` và bộ kiểm thử đơn vị CP2).
- **Phạm vi phụ trách chính**:
  - Hiện thực hóa đầy đủ luồng nghiệp vụ xử lý claim hoàn phí cho cả ba kiến trúc A (`workflow`), B (`single`), C (`orchestrator`) theo đúng chữ ký `run_claim(claim_id, *, seed, store_path, crash_at=None) -> RunResult`.
  - Thiết lập ranh giới rõ ràng giữa Code và Model (MockLLM): tính toán bồi hoàn bằng `compute_compensation`, kiểm tra quyền sở hữu đơn qua `lookup_order`, và chỉ gọi ghi sổ cái thông qua cổng host `durability.issue_refund`.
  - Đảm bảo mọi nhánh trả về (`resolved`, `denied`, `needs_info`, `escalated`, `failed`) đều đóng gói qua `lab8.shapes.common.finish()` và sinh file nhật ký tuân thủ **Trace contract v1** (không lộ `parent_secret` hay PII).
  - Xây dựng bộ unit test `src/tests/test_cp2_shapes.py` để kiểm chứng tính đúng đắn của ba shape ở CP2.

## 3. Đóng góp cụ thể

- **Commit chính**: `25d5335 feat: add shape implementations for orchestrator, single agent, workflow, and tests` (nhánh `thanhtung`, đã merge vào `main`).
- **Triển khai kỹ thuật trên 3 shape**:
  1. **Shape A (`src/lab8/shapes/workflow.py`)**:
     - Xây dựng luồng Python tuần tự, xác định (0 model call): đọc claim qua `get_claim_view` (tránh `SELECT *` để không chạm `parent_secret`), kiểm tra thiếu `order_id` (`needs_info`), kiểm tra quyền truy cập đơn qua `lookup_order` (`escalated` nếu không `visible`), tính quote bằng `compute_compensation` từ dữ liệu DB (bỏ qua số ngày trễ do người dùng tự khai trong ticket), và truyền **quote đầy đủ** vào `issue_refund`.
  2. **Shape B (`src/lab8/shapes/single.py`)**:
     - Xây dựng vòng lặp ReAct giới hạn `max_steps=8` thông qua `lab8.runtime.run_react`. Hàm `decide(seen)` chỉ được chọn các read tool (`lookup_order`, `compute_compensation`) và ghi nhận chi phí model qua `mock_llm.complete`. Sau khi vòng lặp kết thúc, phần code của shape mới kiểm tra `proposal > 0` và gọi `issue_refund`.
  3. **Shape C (`src/lab8/shapes/orchestrator.py`)**:
     - Phân tách quyền hạn giữa Orchestrator và Investigator: dựng gói `handoff` đã làm sạch bằng `lab8.handoff.make_handoff` (`facts={}`, chỉ cấp quyền các read-only tool `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`), ghi `safe_dump(handoff)` vào trace, chạy `run_readonly_investigators` với quyền worker, sau đó Orchestrator nhận quote và trực tiếp gọi `issue_refund`.
- **Thiết kế & viết Unit Test (`src/tests/test_cp2_shapes.py` — 9 test cases)**:
  - `test_cp2_shapes_ignore_ticket_delay_at_seed_55`: Chứng minh cả 3 shape không bị đánh lừa bởi số ngày trễ trong ticket ở `C-002` (`seed=55`), trả về `denied` với `proposal_amount == 0` (khắc phục điểm yếu `REFERENCE_WEAKNESS` của `swarm`).
  - `test_cp2_shapes_unknown_claim_returns_failed_with_valid_trace`: Kiểm chứng khi truyền `claim_id` không tồn tại (`C-999`), cả 3 shape không ném exception mà trả `status == "failed"`, `error_reason == "unknown_claim"` kèm trace hợp lệ.
  - `test_cp2_shapes_pass_full_quote_on_partially_refunded_order`: Kiểm chứng trên `C-014` (T14 — đơn `O-515` đã hoàn 30.000đ phí ship trước đó), cả 3 shape truyền **quote đầy đủ** (`150000`) vào `issue_refund` để host tự trừ phần đã hoàn và chỉ ghi dòng ledger mới `120000`.

## 4. Bằng chứng

- **Commit**: `25d5335` (`feat: add shape implementations for orchestrator, single agent, workflow, and tests`).
- **Files đã triển khai**:
  - `src/lab8/shapes/workflow.py`
  - `src/lab8/shapes/single.py`
  - `src/lab8/shapes/orchestrator.py`
  - `src/tests/test_cp2_shapes.py`
- **Kết quả kiểm thử**:
  - Cổng host sau khi thêm `test_cp2_shapes.py`: `python -m pytest -q` → tăng thêm 9 passed (từ 54 lên 63 passed ở mốc CP2, và 90 passed sau khi ghép CP4).
  - Ma trận student: `python -m pytest -q -m student -o addopts=` → pass toàn bộ các kịch bản nghiệp vụ T01–T10, T11, T13, T14 trên cả 3 shape, tạo nền tảng để CP3 gắn tiếp `crash_at` đạt 248/248 passed.

## 5. Công cụ AI đã dùng

- **Công cụ**: Gemini / Antigravity.
- **Mục đích sử dụng**:
  - Hỗ trợ phân tích yêu cầu đề bài, đối chiếu luật nghiệp vụ trong `docs/business_rules.md` và `docs/contracts.md` với mẫu `swarm_reference.py`.
  - Gợi ý cấu trúc hàm `decide(seen)` trong `single.py` và cách tổ chức bộ unit test `src/tests/test_cp2_shapes.py`.
  - Hỗ trợ xử lý lỗi môi trường Python 3.12 (`PyYAML` wheel trên Windows) và rà soát định dạng báo cáo cá nhân.
- **Cách tự kiểm tra kết quả**:
  - Tự chạy kiểm chứng trực tiếp bằng `python -m lab8.smoke`, `python -m pytest -q` và `python -m pytest -q -m student -o addopts=` trên máy local.
  - Kiểm tra từng nhánh trả về trong code để chắc chắn không có lệnh `SELECT *` trên bảng `claims`/`orders`, không lộ `parent_secret` hay PII vào trace, và truyền đúng quote đầy đủ vào `issue_refund`.

## 6. Tự đánh giá

- **Mức độ hoàn thành**: Hoàn thành 100% nhiệm vụ Checkpoint CP2 (cả 3 shape và bộ unit test riêng), bàn giao code sạch với các mốc `TODO CP3` rõ ràng để các thành viên phụ trách CP3, CP4, CP5 phát triển tiếp.
- **Bài học rút ra**: Hiểu rõ nguyên lý thiết kế hệ thống Agent an toàn — phân tách quyền đọc/ghi giữa model và host, tại sao không được để LLM tự quyết định số tiền hoàn hoặc tự trừ trần hoàn tiền theo đơn, và vai trò của Trace contract v1 như một ranh giới bảo mật.
