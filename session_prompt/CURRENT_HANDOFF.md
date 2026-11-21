# CURRENT_HANDOFF — nhật ký theo giờ của ngày

Cập nhật: 17:47 21/11/2026 (phiên điều phối; viết lại sau lượt cả nhóm soát xung đột 21/11). Sổ việc — việc đang mở, ai làm, bước kế, quyết định đang chờ — là `session_prompt/VIEC_DANG_MO.md`; trang này KHÔNG chép bước kế.

## PHIÊN SAU ĐỌC TRƯỚC
1. `session_prompt/HIEN_TRANG.md` (đủ) ⇒ `session_prompt/VIEC_DANG_MO.md` khối đầu + khối có tên mình ⇒ `session_prompt/sessions/STATUS_<X>.md` của mình.
2. Máy mở lại: `/tmp` MẤT (worktree ghi trong sổ từng phiên phải tạo lại), `docker compose up -d qdrant`, kiểm 9.436 điểm. Việc nặng (server, đo, cả bộ test): phiên làm báo phiên điều phối một dòng; phiên điều phối hỏi "ok?" phiên điều phối của hai dự án khác KHI họ đang mở phiên và chờ một dòng; xong nhắn "máy trả".
3. Dòng theo giờ các ngày trước: `report_agent/<ngày>/TONG_HOP.md`; bản tới tối 19/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-19.md`.

## Ghi trong ngày (phiên điều phối nối dòng mới ở đây; cuối ngày dời sang `TONG_HOP.md` của ngày)
- 18:22 21/11/2026 — mở phiên tối (A, B, C, E; chủ dự án vắng tới 21:30, đã duyệt tiền API). Đã làm: giao theo khối A của sổ việc; khởi động agent con soát tích hợp (bước 2) trên `187cf6e5`; gộp nhánh bỏ dòng ghi nguồn bản đồ ⇒ main `cf1a70c3`; C sửa bộ chạy 12 vai (đặt rõ nhà cung cấp cho cả hai nhánh, tắt bộ nhớ đệm câu trả lời). Chỗ lệch các phiên báo: khối prompt chủ dự án dán lúc mở là bản CŨ của `START_SESSION.md` (các phiên làm theo bản trong repo) — nói với chủ dự án khi về.
