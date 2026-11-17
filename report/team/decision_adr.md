# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: b9ab387
- Run id dẫn chứng: R-workflow-C-001-s11 (src/reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000-1.000 / 0.000000
- Cost per success (mô phỏng, VND): 27.86
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Trên cùng tập kiểm thử công khai (14 claims) và đối soát trên toàn bộ 5 seeds cố định (11, 22, 33, 44, 55, tổng cộng 70 trials độc lập), kiến trúc Workflow đạt độ chính xác tuyệt đối: Pass rate = 1.000, Pass^5 = 1.000, độ biến thiên giữa các seed bằng không tuyệt đối (variance = 0.000000, min 1.000, max 1.000). Về mặt kinh tế, Workflow có chi phí thấp nhất toàn diện với 27.86 VND/success (1.86 steps/claim), thấp hơn đáng kể so với Single ReAct (29.43 VND), Swarm (49.57 VND) và Orchestrator (56.65 VND). Bản chất quy trình bồi thường khiếu nại (claims resolution) của LogiX-VN là một chuỗi nghiệp vụ tất định (deterministic business rules) với các điều kiện ràng buộc chặt chẽ: xác thực quyền sở hữu đơn hàng, kiểm tra SLA trễ hạn theo policy có hiệu lực, tính toán bồi thường và khống chế trần theo đơn hàng, kiểm tra approval và ghi nhận vào ledger SQLite kèm audit log trong cùng một transaction. Việc mã hóa luồng bằng Python tĩnh giúp loại trừ hoàn toàn rủi ro sai lệch logic (hallucination) từ mô hình ngôn ngữ lớn, ngăn chặn triệt để tình trạng vi phạm ràng buộc bảo mật hoặc sai lệch số tiền đền bù.

## Có đáng đổi lấy multi-agent không

Hoàn toàn không đáng đổi lấy multi-agent (Orchestrator hoặc Swarm). Dữ liệu benchmark cho thấy việc chuyển sang multi-agent không đem lại bất kỳ cải thiện nào về tỷ lệ thành công (Orchestrator đạt pass rate 1.000 ngang với Workflow nhưng chi phí tăng hơn gấp đôi lên 56.65 VND do tiêu tốn token cho việc lập kế hoạch và phân rã tác vụ; Swarm thậm chí còn sụt giảm hiệu năng với pass rate 0.986, pass^5 giảm xuống 0.929 và variance tăng lên 0.000816, đồng thời phát sinh lỗi nghiêm trọng do ảo giác `status resolved != denied x1` ở seed 55 khi agent tự ý lấy số ngày trễ từ ticket thay vì bảng đối soát DB). Nhóm kiên quyết giữ kiến trúc Workflow. Quyết định chỉ có thể đảo ngược khi và chỉ khi hệ thống phải xử lý các nghiệp vụ khiếu nại phi cấu trúc mở (unstructured multi-modal disputes, thẩm định gian lận phức tạp xuyên biên giới, đàm phán hợp đồng thương lượng ngoại lệ) - nơi các quy tắc code tĩnh không thể bao quát và sự tự chủ linh hoạt của multi-agent chứng minh được năng lực giải quyết vượt trội đủ để bù đắp cho chi phí token và phương sai rủi ro.

## Trace và bằng chứng

Trace của hệ thống ghi lại nhật ký thực thi chuẩn theo Trace contract v1, bao gồm các sự kiện vòng đời: tiếp nhận yêu cầu (`claim_received`), tra cứu đơn hàng (`order_lookup`), tính toán mức bồi thường (`compensation_computed`), gửi lệnh hoàn tiền an toàn qua host (`refund_dispatched`), và hoàn tất phiên (`trial_finished`), kèm theo `run_id`, timestamp và số bước. Hệ thống áp dụng nguyên tắc đặc quyền tối thiểu (least privilege) và phân tách ranh giới an toàn: cố ý **KHÔNG** ghi lại các trường nhạy cảm như `parent_secret` (chuỗi canary token), token xác thực trong header, thông tin định danh cá nhân (PII: số điện thoại, địa chỉ nhận hàng của khách), ghi chú nội bộ của nhà xe, và tên chi tiết món hàng (chỉ truy cập qua allowlist projection views). Đội ngũ bảo mật chứng minh hệ thống không lộ lọt bí mật bằng cách kích hoạt scanner tự động quét toàn văn các tệp trace JSON (`trace_path` và các file `<run_id>*`) cùng thư mục, kết hợp với bộ test kiểm tra rò rỉ (`assert 0 secret leakage` và `assert 0 approval bypass`), xác nhận không có bất kỳ token bí mật hay dữ liệu PII nào xuất hiện trong trace hoặc output trên toàn bộ 70 trials.

## Giới hạn

Thử nghiệm được thực hiện trên môi trường MockLLM mô phỏng, chưa phản ánh đầy đủ độ trễ mạng thực tế, tỷ lệ timeout, hay hiện tượng suy thoái nhận thức (cognitive drift) của các mô hình LLM sản xuất (production APIs) khi xử lý ngữ cảnh dài; độ trễ được đánh dấu là `unavailable`. Chi phí tính toán là giá mô phỏng theo biểu phí giả định (20 VND/1k input, 80 VND/1k output, 10 VND/tool call). Không chỉnh sửa kết quả JSON nhân tạo để vượt ngưỡng đánh giá 0.75.
