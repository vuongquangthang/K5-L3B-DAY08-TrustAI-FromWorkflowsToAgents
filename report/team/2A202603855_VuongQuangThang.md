# Báo cáo cá nhân — 2A202603855_VuongQuangThang

## 1. Thông tin thành viên

- Họ tên: Vương Quang Thắng
- MSSV: 2A202603855
- Email: 26ai.thangvq@vinuni.edu.vn
- GitHub: vuongquangthang

## 2. Phần việc phụ trách

- **Vai trò trong nhóm**: System Analyst, Evaluation Lead & Bonus Lead (Phụ trách Checkpoint CP1, CP5 và Topic Bonus B3 — Kiến trúc phần mềm, Đánh giá thực nghiệm và Verifier chống khuếch đại lỗi).
- **Phạm vi phụ trách chính**:
  - Khởi tạo môi trường, thẩm định contract và chia vai ở giai đoạn khởi động (CP1).
  - Chịu trách nhiệm thực thi và đối soát bộ thực nghiệm đa hình thái (benchmark 4 shapes x 5 seeds x 14 claims trên bộ public).
  - Phân tích đánh đổi kiến trúc (Architectural Trade-offs) và lập Hồ sơ Quyết định Kiến trúc (ADR) tại `report/team/decision_adr.md`.
  - Nghiên cứu thực nghiệm, phân loại lỗi Multi-Agent (R2 Failure Taxonomy & Ablation Study) tại `report/team/research_card.md`.
  - Viết và tổng hợp Báo cáo Kiến trúc Nhóm tại `report/team/group_report.md` cùng Bảng đóng góp tại `TEAM.md`.
  - **Chủ trì và hiện thực hóa trọn vẹn Topic Bonus B3 (+10 điểm)**: Xây dựng kiến trúc `swarm_verified` chống khuếch đại lỗi (Google Research 2026), bộ dữ liệu đối kháng và báo cáo `report/team/bonus_report.md`.
  - Rà soát kiểm tra toàn diện quy chuẩn nộp bài tự động (`python -m lab8.check_submission`) đảm bảo 0 FAIL.

## 3. Đóng góp cụ thể

- **Phân tích định lượng và ban hành Quyết định Kiến trúc (CP5 / ADR)**:
  - Phân tích chi tiết 280 trials thực nghiệm từ `src/reports/benchmark.json`, so sánh đa chiều giữa 4 kiến trúc: Workflow (ít tự chủ nhất), Single ReAct, Orchestrator (phân cấp), và Swarm (tự chủ tối đa).
  - Quyết định lựa chọn **Workflow** làm kiến trúc chốt nộp bài chấm cổng hidden dựa trên bằng chứng thực nghiệm: đạt Pass rate tuyệt đối (1.000), Pass^5 (1.000), phương sai bằng không (variance = 0.000000) và chi phí thấp nhất hệ thống (27.86 VND/success so với 56.65 VND của Orchestrator).
  - Làm rõ luận điểm kiến trúc: Trong bài toán xử lý bồi hoàn (claims flow) với các luật nghiệp vụ cứng (policy, SLA, trần hoàn tiền theo đơn), việc tăng mức độ tự chủ của LLM không làm tăng chất lượng mà chỉ làm tăng chi phí token và rủi ro ảo giác logic.
- **Nghiên cứu nguyên nhân thất bại của Multi-Agent (Research Card / Ablation)**:
  - Phân tích trường hợp thất bại của Swarm tại seed 55 (`status resolved != denied x1` trên claim T02): chứng minh hiện tượng LLM bị ảo giác (hallucination), tự ý tin vào số ngày trễ người dùng khai báo trong ticket (5 ngày) thay vì dữ liệu thẩm định trong database (2 ngày), từ đó phê duyệt sai quy định SLA.
  - Hoàn thiện phiếu nghiên cứu đối chiếu lý thuyết (dựa trên nghiên cứu MAST NeurIPS 2025) và kiểm chứng bằng thực nghiệm ablation có kiểm soát.
- **Hiện thực hóa Topic Bonus B3 — Verifier / Aggregator chống khuếch đại lỗi (+10 điểm)**:
  - Thiết kế và lập trình module `src/bonus/swarm_verified.py`: tích hợp một tầng Code Verifier & Reconciler đối soát dữ kiện (`delay_days`, `status`, `damage_verified`) với cơ sở dữ liệu có cấu trúc SQLite, sửa triệt để lỗi ảo giác của Swarm ở seed 55 và ghi event `verifier_override` vào Trace.
  - Xây dựng bộ dữ liệu 8 khiếu nại đối kháng (`src/bonus/cases.jsonl` và `src/bonus/world.json`) kiểm thử các kịch bản khách khai khống ngày trễ, nói dối hàng hỏng, hoặc đưa nhiều con số gây nhiễu.
  - Viết bộ unit test `src/tests/test_bonus_b3_verifier.py` (3 test pass 100%).
  - Chạy benchmark so sánh 3 shape (`src/reports/bonus_benchmark.json`), chứng minh đưa Pass rate của Swarm từ 0.986 lên 1.000 tuyệt đối, Pass^5 từ 0.929 lên 1.000, triệt tiêu phương sai hoàn toàn (variance = 0.000000).
  - Hoàn thành báo cáo khoa học 2 trang `report/team/bonus_report.md` theo khung quy định.
- **Đảm bảo chất lượng bài nộp và tuân thủ Hợp đồng**:
  - Đối soát độc lập ranh giới an toàn: xác nhận toàn bộ 70 trials của Workflow và 70 trials của Swarm Verified tuân thủ 100% Trace contract v1, không rò rỉ secret (`CANARY_SECRET_*`), không lộ PII, 0 approval bypass và đạt 20/20 kịch bản crash safety.

## 4. Bằng chứng

- **Hồ sơ tài liệu kiến trúc & Bonus đã hoàn thiện**:
  - `report/team/decision_adr.md`: Khẳng định shape chọn `workflow`, liên kết chuỗi run_id thực tế `R-workflow-C-001-s11`.
  - `report/team/research_card.md`: Điền đủ 7 tiêu chí nghiên cứu, phân tích sâu các câu hỏi R1–R4 và kết quả ablation.
  - `report/team/bonus_report.md`: Báo cáo điểm cộng Topic B3 hoàn chỉnh theo khung quy chuẩn.
  - `report/team/group_report.md`: Báo cáo kết quả benchmark và phần kết luận định hướng kiến trúc.
  - `TEAM.md`: Bảng phân công và đóng góp thành viên chuẩn format máy đọc.
- **Mã nguồn và dữ liệu thực nghiệm**:
  - `src/bonus/swarm_verified.py`: Code module Swarm Verified tích hợp Verifier.
  - `src/bonus/cases.jsonl` & `src/bonus/world.json`: Bộ 8 case đối kháng tự xây dựng.
  - `src/tests/test_bonus_b3_verifier.py`: 3 unit tests mới cho phần bonus.
  - `src/reports/bonus_benchmark.json`: Tập dữ liệu benchmark so sánh workflow, swarm và swarm_verified.
  - `src/reports/benchmark.json` & `src/reports/crash.json` (20/20 crash safety).
- **Kết quả kiểm tra tự động**:
  - `python -m pytest -q`: Đạt **93 passed** (toàn bộ test suite chính và bonus đều xanh).
  - `python -m lab8.check_submission`: Đạt chuẩn tuyệt đối **0 FAIL** (shapes [OK], reports [OK], docs [OK], bonus [OK]).

## 5. Công cụ AI đã dùng

- **Công cụ sử dụng**: Gemini
- **Mục đích sử dụng:**
- Dùng AI để giải thích nhanh các khái niệm hệ thống phức tạp như `idempotency` (tính lũy đẳng trong giao dịch), cơ chế `handoff` an toàn và ranh giới bảo mật trong `trace`.
- Nhờ AI hỗ trợ format (định dạng) các bảng biểu Markdown trong file `TEAM.md` và cấu trúc các ý phân tích số liệu `benchmark.json` để đưa vào `research_card.md` một cách mạch lạc.
- Nhờ AI rà soát logic khi phân tích lý do kiến trúc Swarm bị fail ở test case `status resolved != denied`.

**Cách tự kiểm tra kết quả (Validation):**
- **Không dùng AI tạo số liệu giả:** Toàn bộ số liệu điền trong `decision_adr.md` và `benchmark.json` đều được lấy từ kết quả chạy thật dưới local bằng lệnh `python -m lab8.benchmark`.
- **Kiểm chứng chéo với tài liệu:** Đọc đối chiếu các gợi ý giải thích của AI với file `docs/business_rules.md` và `docs/contracts.md` để đảm bảo không bị sai lệch luật nghiệp vụ.
- **Kiểm chứng bằng công cụ test:** Thay vì tin tưởng hoàn toàn mã nguồn do AI gợi ý, tôi luôn tự tay chạy lệnh `python -m lab8.crash_test --count 20` để xác nhận điểm tuyệt đối 20/20 và lệnh `python -m lab8.check_submission` để đảm bảo đầu ra báo `0 FAIL`.

## 6. Tự đánh giá

- **Mức độ hoàn thành công việc**: Hoàn thành 100% khối lượng công việc được giao thuộc Checkpoint CP1, CP5 và vượt chỉ tiêu khi hoàn thành xuất sắc Topic Bonus B3 mang về điểm thưởng tối đa (+10 điểm).
- **Kỹ năng đạt được**: Nắm vững phương pháp đánh giá thực nghiệm hệ thống AI, hiểu rõ sự đánh đổi giữa Workflow xác định và Agent tự chủ (MAS), làm chủ kỹ thuật xây dựng Verifier/Aggregator chống khuếch đại lỗi (error amplification mitigation) và các kỹ thuật bảo mật ranh giới giao dịch.
- **Điểm tự đánh giá**: 10/10 (+ điểm thưởng Bonus B3).
