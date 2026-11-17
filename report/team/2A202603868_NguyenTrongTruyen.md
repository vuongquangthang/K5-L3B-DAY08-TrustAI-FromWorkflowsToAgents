# Báo cáo cá nhân — 2A202603868_NguyenTrongTruyen

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trọng Truyền
- MSSV: 2A202603868
- Email: 26ai.truyennt2@vinuni.edu.vn
- GitHub: truien

## 2. Phần việc phụ trách

- **Vai trò trong nhóm**: Durability & Handoff Engineer (Phụ trách Checkpoint CP3 — Handoff, ledger, crash).
- **Phạm vi phụ trách chính**:
  - Ghi tiền an toàn khi gọi lại cùng claim (T11) và khi crash rồi resume (T12) trên cả ba shape `workflow`, `single`, `orchestrator`.
  - Đảm bảo handoff của orchestrator không mang secret qua ranh giới: tool chỉ đọc, trace chỉ ghi handoff đã sanitize, không ghi parent context.

## 3. Đóng góp cụ thể

- **Commit chính**: `812ea03 feat(cp3): pass crash_at to issue_refund and re-raise InjectedCrash in all shapes` (nhánh `truien`), làm trên nền code CP2 của Nguyễn Thanh Tùng (`25d5335`).
- **Thay đổi kỹ thuật** (`src/lab8/shapes/workflow.py`, `single.py`, `orchestrator.py`):
  - Truyền `crash_at` vào `durability.issue_refund(conn, claim_id, proposal, crash_at=crash_at)`. Vẫn truyền quote đầy đủ để host tự trừ phần các claim khác đã hoàn trên cùng đơn, tránh trừ hai lần (T13, T14).
  - Bắt `InjectedCrash` chỉ để ghi event `crash` vào trace và flush trace, sau đó `raise` lại. Shape không nuốt lỗi, nên crash suite thấy đúng crash, còn lần chạy lại trên cùng DB là no-op nhờ idempotency key `refund:{claim_id}`.
- **Quyết định kỹ thuật**:
  - Không tự trừ tiền đã hoàn và không tự dựng cơ chế chống trùng ở tầng shape. Ledger, audit `refund_committed` và checkpoint nằm trong `lab8/durability.py`, shape chỉ gọi đúng và không che lỗi.
  - Handoff của orchestrator đã dùng `make_handoff` với allowlist; mình rà lại và giữ nguyên, không thêm trường nào ngoài allowlist vào trace.
- **Hiểu rõ**: chạy `python -m lab8.demo.buggy_workflow` cho thấy checkpoint đơn lẻ làm ledger có 2 dòng refund. Vì vậy chống refund đôi phải dựa vào ledger và idempotency key, không dựa vào checkpoint. Tóm tắt bằng LLM cũng không tính là redaction.
- **Test**: không thêm test mới. Dùng test có sẵn của giảng viên (T11, T12 trong `src/tests/test_public_matrix.py`) để kiểm tra.

## 4. Bằng chứng

- Commit: `812ea03` (CP3) và `c8db8d9` (mục cá nhân trong `TEAM.md`), nhánh `truien`.
- Kết quả chạy:
  - `python -m pytest -q` → 63 passed.
  - `python -m pytest -q -m student -o addopts=` → 248 passed, 0 failed (gồm T11, T12 trên cả ba shape).
- Test liên quan: `src/tests/test_public_matrix.py::test_t12_crash_before_checkpoint_does_not_double_pay`.
- Demo phản ví dụ: `python -m lab8.demo.buggy_workflow` in `unsafe refund rows: 2 (the host ledger must stay at 1)`.

## 5. Công cụ AI đã dùng

- **Công cụ**: Claude Code.
- **Dùng vào việc**:
  - Đọc hiểu `CHECKPOINTS.md`, `durability.py`, `handoff.py`, `swarm_reference.py` để nắm yêu cầu CP3.
  - Hỗ trợ đoạn sửa ở ba shape theo mẫu có sẵn trong `swarm_reference.py`.
  - Soạn nháp mục cá nhân trong `TEAM.md` và báo cáo này.
- **Cách tự kiểm tra**:
  - Xem lại diff (3 file, +21/−12 dòng) và đối chiếu với `durability.py`.
  - Tự chạy hai lệnh pytest ở trên và đọc kết quả thật, không dựa vào lời AI.
  - Đối chiếu số liệu và tên test trong báo cáo với repo.

## 6. Tự đánh giá

- Hoàn thành phần CP3 được giao: T11 và T12 xanh trên cả ba shape, cổng host vẫn xanh.
- Hạn chế: chưa thêm test riêng cho CP3 và chưa tự chạy crash suite 20 điểm, phần đó thuộc CP4 của thành viên khác.
- Học được: vì sao ledger kèm idempotency key mới bảo đảm không hoàn tiền hai lần, còn checkpoint thì không; và vì sao trace là ranh giới bảo mật chứ không phải tiện ích debug.
