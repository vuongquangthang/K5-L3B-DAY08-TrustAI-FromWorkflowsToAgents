# Báo cáo nhóm — Lab 8 TrustAI

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: TrustAI
- Lớp: L3B
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): b9ab387

## 2. Mục tiêu và cách tiếp cận

Nhóm tiếp cận bài toán xử lý khiếu nại bồi thường giao hàng LogiX-VN theo hành trình tiến hóa kiến trúc phần mềm: từ quy trình tất định thuần túy (Workflow), qua tác nhân đơn lẻ (Single ReAct Agent), đến kiến trúc điều phối tập trung (Orchestrator - Workers) và mô hình bầy đàn cộng tác tự do (Swarm Reference). Mục tiêu trọng tâm là đánh giá thực nghiệm sự đánh đổi (trade-offs) giữa quyền tự chủ của LLM, độ chính xác nghiệp vụ (pass rate), độ tin cậy đa seed (pass^5, variance), chi phí suy luận (cost/success) và độ an toàn hệ thống (crash safety, secret leak, approval bypass).

## 3. Giải pháp

Hệ thống thiết lập ranh giới bảo mật và phân quyền nghiêm ngặt giữa tầng điều khiển (Code/Host) và tầng nhận thức (LLM):
- **Workflow**: Thực thi pipeline mã lệnh Python cố định; chỉ gọi tool nghiệp vụ đã kiểm chứng, LLM chỉ đóng vai trò định dạng văn bản; loại trừ hoàn toàn tính ngẫu nhiên.
- **Single ReAct**: Vòng lặp suy luận - hành động giới hạn tối đa 8 bước; Host kiểm soát và chặn trước các vi phạm an toàn.
- **Orchestrator**: Điều phối viên phân rã kế hoạch, chuyển giao handoff đã được sanitize nghiêm ngặt (theo chuẩn `handoff.v1`, loại bỏ `parent_secret`, token và PII) cho Investigator chỉ có quyền đọc.
- **Trace contract v1**: Ghi vết minh bạch mọi sự kiện thực thi hợp lệ, đảm bảo 0 rò rỉ secret và 0 vi phạm phê duyệt.

## 4. Kết quả

Bảng so sánh 4 shape trên bộ public claims (từ `src/reports/benchmark.json`, 14 claims x 5 seeds = 70 trials/shape):

| Shape | Pass rate | Pass^5 | Seed Variance | Min Seed | Max Seed | Cost/success (VND) | Mean Steps |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **workflow** | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | **27.86** | **1.86** |
| single | 1.000 | 1.000 | 0.000000 | 1.000 | 1.000 | 29.43 | 1.86 |
| orchestrator | 1.000 | 1.000 | 0.000000 | 1.000 | 1.000 | 56.65 | 2.79 |
| swarm | 0.986 | 0.929 | 0.000816 | 0.929 | 1.000 | 49.57 | 2.80 |

- **Crash safety**: Đạt 20/20 kịch bản an toàn (`src/reports/crash.json`), đảm bảo tính toàn vẹn idempotency và khôi phục giao dịch sau sự cố.
- **Bảo mật**: 0 secret leak, 0 approval bypass trên toàn bộ các trials.

Quyết định kiến trúc và lý do chi tiết: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

- Xử lý xung đột số ngày trễ giữa thông tin khách khai báo và dữ liệu bảng `orders`: Luôn ưu tiên dữ liệu đã thẩm định trong database, ngăn ngừa ảo giác do LLM tự suy diễn.
- Đảm bảo an toàn giao dịch khi xảy ra crash bất ngờ: Tận dụng cơ chế transaction SQLite và kiểm tra trạng thái ledger trước khi ghi nhận bồi hoàn.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency hiển thị là `unavailable`. Biểu phí token là giá trị mô phỏng. Khi mở rộng sang bài toán hỗ trợ đa phương thức không có cấu trúc cố định, hệ thống sẽ cần cân nhắc nâng cấp cơ chế routing linh hoạt giữa Workflow và Multi-Agent.

## 8. Tài liệu tham khảo

- Google Research (2026), *Towards a Science of Scaling Agent Systems*.
- MAST (NeurIPS 2025), *Why Do Multi-Agent LLM Systems Fail?*.
- AgentArch (AACL 2026).

## 9. Kết luận

Dựa trên kết quả thực nghiệm toàn diện từ bộ benchmark, nhóm khẳng định lựa chọn kiến trúc **Workflow** làm giải pháp kiến trúc tối ưu nhất cho bài toán giải quyết khiếu nại LogiX-VN. Kiến trúc Workflow đạt hiệu suất tối đa tuyệt đối (Pass rate 1.000, Pass^5 1.000, variance 0.000000) đồng thời tối ưu hóa chi phí vận hành ở mức thấp nhất (27.86 VND/success, tiết kiệm hơn 50% chi phí so với Orchestrator 56.65 VND). Trong bối cảnh nghiệp vụ có quy trình xử lý rõ ràng và luật chính sách cứng nhắc, kiến trúc kiểm soát tất định bằng mã lệnh không chỉ triệt tiêu rủi ro ảo giác logic của LLM mà còn bảo đảm tính toàn vẹn dữ liệu, an toàn bảo mật và độ ổn định cao nhất khi đưa vào vận hành thực tế.
