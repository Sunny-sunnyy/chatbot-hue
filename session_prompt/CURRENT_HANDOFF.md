# CURRENT_HANDOFF — nhật ký theo giờ của ngày

Cập nhật: 08:24 22/11/2026 (phiên điều phối; mở phiên sáng 22/11, hai dòng tối 21/11 đã dời sang `report_agent/2026-11-21/TONG_HOP.md`). Sổ việc — việc đang mở, ai làm, bước kế, quyết định đang chờ — là `session_prompt/VIEC_DANG_MO.md`; trang này KHÔNG chép bước kế.

## PHIÊN SAU ĐỌC TRƯỚC
1. `session_prompt/HIEN_TRANG.md` (đủ) ⇒ `session_prompt/VIEC_DANG_MO.md` khối đầu + khối có tên mình ⇒ `session_prompt/sessions/STATUS_<X>.md` của mình.
2. Máy mở lại: `/tmp` MẤT (worktree ghi trong sổ từng phiên phải tạo lại), `docker compose up -d qdrant`, kiểm 9.436 điểm. Việc nặng (server, đo, cả bộ test): phiên làm báo phiên điều phối một dòng; phiên điều phối hỏi "ok?" phiên điều phối của hai dự án khác KHI họ đang mở phiên và chờ một dòng; xong nhắn "máy trả".
3. Dòng theo giờ các ngày trước: `report_agent/<ngày>/TONG_HOP.md`; bản tới tối 19/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-19.md`.

## Ghi trong ngày (phiên điều phối nối dòng mới ở đây; cuối ngày dời sang `TONG_HOP.md` của ngày)
- 08:24 22/11/2026 — mở phiên sáng 22/11 (phiên điều phối `hue-rag-7a`, B `hue-rag-b1`, C `hue-rag-4f`, phiên đo `hue-rag-67`; chủ dự án có mặt). Máy mở lại 08:13 ⇒ `/tmp` mất, sổ worktree cũ đã gỡ; Qdrant 9.436 điểm. Đã giao: phép thử khói sau bản gộp tối 21/11 (ĐẠT 10 / 10 bước, giữ bản "mục web chỉ mở khi cả câu bị từ chối") · hàng [7] chia hai nửa (C lệnh cập nhật riêng bài đã sửa, B lệnh đề xuất, phiên đo viết phép kiểm) · đọc nhánh công cụ "gần một điểm có gì". Đã gửi chủ dự án hướng dẫn cấp quyền chữ chạy dần và nhắc một lần việc đọc bài nháp "Huế → Hội An". Chi tiết: sổ việc khối A, gạch đầu.
