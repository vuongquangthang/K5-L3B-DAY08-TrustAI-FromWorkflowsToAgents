---
noteId: "96cbe2b0e23e11f1af08fbca3e5532da"
tags: []

---

# Bonus report: B3

- Topic + nguồn (tên, năm, slide): Topic B3 · Verifier/aggregator chống khuếch đại lỗi (Google Research 2026, *Towards a Science of Scaling Agent Systems*, slide 17, 22, 42).
- CLAIM của nguồn (1 câu): Các tác nhân độc lập trong hệ thống Multi-Agent khuếch đại lỗi tới 17.2× so với lỗi ban đầu, trong khi cơ chế điều phối có kiểm chứng tập trung (verifier/evaluator) giúp giảm thiểu hiện tượng này xuống còn 4.4× và khôi phục độ chính xác của toàn hệ thống.
- BOUNDARY (model / dataset / setup): Môi trường giải quyết bồi thường giao hàng LogiX-VN với luật nghiệp vụ ràng buộc; MockLLM trên 14 claims public và 8 claims đối kháng tự sinh, 5 seeds cố định (11, 22, 33, 44, 55).
- HYPOTHESIS trên LogiX: Bổ sung một tầng Code-Level Verifier & Reconciler vào Swarm (tạo thành `swarm_verified`) sẽ triệt tiêu hoàn toàn lỗi ảo giác tại seed 55 (`status resolved != denied x1`), nâng Pass rate từ 0.986 lên 1.000, Pass^5 từ 0.929 lên 1.000, đưa phương sai variance về 0.000000; đổi lại chi phí (cost/success) sẽ tăng nhẹ (~15%) do phát sinh thao tác đối soát và tính toán lại bồi thường có kiểm chứng.
- Biến cố định / biến thay đổi: Cố định MockLLM, bộ công cụ (tools), 14 claims public, 5 seeds (11, 22, 33, 44, 55), biểu giá token và evaluator SQLite ledger. Biến duy nhất thay đổi: Tích hợp bước kiểm chứng dữ kiện bằng code (`verifier_override`) trước khi ra quyết định ghi nhận bồi hoàn.
- Lệnh tái lập (copy-paste được): `python -m lab8.benchmark --shapes workflow,swarm,swarm_verified --extra-shape swarm_verified=bonus.swarm_verified:run_claim --seeds 11,22,33,44,55 --out reports/bonus_benchmark.json`
- File report + run id: `src/reports/bonus_benchmark.json` (Run id dẫn chứng: `R-swarm_verified-C-002-s55`)

## Kết quả

Số liệu đo lường thực nghiệm từ `src/reports/bonus_benchmark.json` (70 trials/shape trên tập public):

| Shape | Pass rate | Pass^5 | Seed Variance | Min Seed | Max Seed | Cost/success (VND) | Mean Steps | Lỗi thường gặp |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **workflow** | 1.000 | 1.000 | 0.000000 | 1.000 | 1.000 | 27.86 | 1.86 | Không có lỗi (0 fail) |
| **swarm** | 0.986 | 0.929 | 0.000816 | 0.929 | 1.000 | 49.57 | 2.80 | `status resolved != denied x1` |
| **swarm_verified** | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | **57.29** | **2.81** | **Không có lỗi (0 fail)** |

- **Số lần Verifier can thiệp trên bộ public**: Can thiệp đúng 1 lần tại seed 55 trên claim C-002.
- **Kết quả trên bộ dữ liệu đối kháng (8 adversarial claims trong `src/bonus/cases.jsonl`)**: Swarm Verified vượt qua 8/8 ca thử thách (100% pass), bắt trọn vẹn các trường hợp khách hàng nói quá số ngày trễ, khai khống hàng hỏng, hoặc đưa nhiều con số đánh lạc hướng.
- **Trích đoạn Trace minh họa sự can thiệp của Verifier (`src/traces/R-swarm_verified-C-002-s55.json`)**:
  ```json
  {"kind": "model_override", "payload": {"delay_days": 5}}
  {"kind": "verifier_override", "payload": {
      "action": "reconcile_with_ground_truth_order",
      "discrepancies": {"delay_days": {"candidate": 5, "verified_db": 2}},
      "reason": "prevent_hallucination_amplification"
  }}
  {"kind": "quote", "payload": {"amount_vnd": 0, "reason": "no_entitlement"}}
  ```

## Kết luận

- **Kết luận**: **ỦNG HỘ** mạnh mẽ claim của Google Research (2026). Việc bổ sung một tầng Verifier bằng mã lệnh tất định đã ngăn chặn hiệu quả hiện tượng khuếch đại lỗi do ảo giác của LLM gây ra, đưa tỷ lệ tin cậy của Swarm từ 0.986 (với rủi ro phương sai 0.000816) đạt mốc hoàn hảo 1.000 (phương sai 0.000000).
- **Phân tích giá trị kiến trúc**: Mặc dù Verifier đã can thiệp khôi phục các thuộc tính bị biến dạng, kiến trúc Swarm vẫn giữ lại giá trị ở khả năng hiểu ngôn ngữ tự nhiên phi cấu trúc từ ticket của khách hàng, trích xuất ngữ cảnh ban đầu và điều phối giao việc cho Investigator. Tuy nhiên, chi phí của `swarm_verified` (57.29 VND) cao hơn gấp đôi so với `workflow` (27.86 VND).
- **Điều kiện đảo ngược kết luận**: Kết luận sẽ bị đảo ngược nếu nghiệp vụ khiếu nại hoàn toàn không có dữ liệu nguồn đối soát trong database (ví dụ: bồi thường theo thỏa thuận hòa giải mở hoặc tranh chấp định tính ngoài hợp đồng), khi đó Verifier không có ground-truth để đối chiếu và việc can thiệp bằng code cứng có thể làm triệt tiêu tính linh hoạt của LLM.

## Giới hạn

- Thử nghiệm dựa trên mô hình MockLLM trong môi trường cục bộ; độ trễ mạng thực tế và tỷ lệ lỗi suy luận trong môi trường LLM thương mại chưa được phản ánh (latency là `unavailable`).
- Biểu phí token là giá mô phỏng theo biểu phí giả định của lab.
- Tập dữ liệu gồm 14 public claims và 8 adversarial claims, cần mở rộng kiểm thử trên tập dữ liệu quy mô lớn hàng nghìn trường hợp trong môi trường production.
