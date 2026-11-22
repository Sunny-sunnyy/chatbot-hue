# CURRENT_HANDOFF — nhật ký theo giờ của ngày

Cập nhật: 08:24 22/11/2026 (phiên điều phối; mở phiên sáng 22/11, hai dòng tối 21/11 đã dời sang `report_agent/2026-11-21/TONG_HOP.md`). Sổ việc — việc đang mở, ai làm, bước kế, quyết định đang chờ — là `session_prompt/VIEC_DANG_MO.md`; trang này KHÔNG chép bước kế.

## PHIÊN SAU ĐỌC TRƯỚC
1. `session_prompt/HIEN_TRANG.md` (đủ) ⇒ `session_prompt/VIEC_DANG_MO.md` khối đầu + khối có tên mình ⇒ `session_prompt/sessions/STATUS_<X>.md` của mình.
2. Máy mở lại: `/tmp` MẤT (worktree ghi trong sổ từng phiên phải tạo lại), `docker compose up -d qdrant`, kiểm 9.458 điểm. Việc nặng (server, đo, cả bộ test): phiên làm báo phiên điều phối một dòng; phiên điều phối hỏi "ok?" phiên điều phối của hai dự án khác KHI họ đang mở phiên và chờ một dòng; xong nhắn "máy trả".
3. Dòng theo giờ các ngày trước: `report_agent/<ngày>/TONG_HOP.md`; bản tới tối 19/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-19.md`.

## Ghi trong ngày (phiên điều phối nối dòng mới ở đây; cuối ngày dời sang `TONG_HOP.md` của ngày)
- 08:24 22/11/2026 — mở phiên sáng 22/11 (phiên điều phối `hue-rag-7a`, B `hue-rag-b1`, C `hue-rag-4f`, phiên đo `hue-rag-67`; chủ dự án có mặt). Máy mở lại 08:13 ⇒ `/tmp` mất, sổ worktree cũ đã gỡ; Qdrant 9.436 điểm. Đã giao: phép thử khói sau bản gộp tối 21/11 (ĐẠT 10 / 10 bước, giữ bản "mục web chỉ mở khi cả câu bị từ chối") · hàng [7] chia hai nửa (C lệnh cập nhật riêng bài đã sửa, B lệnh đề xuất, phiên đo viết phép kiểm) · đọc nhánh công cụ "gần một điểm có gì". Đã gửi chủ dự án hướng dẫn cấp quyền chữ chạy dần và nhắc một lần việc đọc bài nháp "Huế → Hội An". Chi tiết: sổ việc khối A, gạch đầu.
- 11:20 22/11/2026 — KẾT PHIÊN SÁNG 22/11 (chủ dự án có mặt cả buổi, dặn "không vội, ổn và tự tin thì báo"). Sáng nay: sáu tính năng mở (36 ⇒ 42) · hai lệnh sửa kho vào main và chạy thật ba lần · kho 266 bài / 9.458 đoạn · bốn bản sửa lỗi người dùng thấy · cổng đóng đạt (75 file test / 1.961 ca, demo 10 / 10, server thật sạch) · README + trang bản đồ dự án viết lại · giáo trình của phiên D: 13 bài + bài mẫu kiểu mới chờ chủ dự án đọc. B, C, phiên đo đã ghi sổ kết phiên. Việc đầu phiên sau + thứ đang chờ chủ dự án: sổ việc khối A. Diễn biến: `report_agent/2026-11-22/TONG_HOP.md`.
