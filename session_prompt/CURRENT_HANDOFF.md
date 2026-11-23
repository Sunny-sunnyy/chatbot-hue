# CURRENT_HANDOFF — nhật ký theo giờ của ngày

Cập nhật: 09:09 23/11/2026 (phiên điều phối; mở phiên sáng 23/11). Sổ việc — việc đang mở, ai làm, bước kế, quyết định đang chờ — là `session_prompt/VIEC_DANG_MO.md`; trang này KHÔNG chép bước kế.

## PHIÊN SAU ĐỌC TRƯỚC
1. `session_prompt/HIEN_TRANG.md` (đủ) ⇒ `session_prompt/VIEC_DANG_MO.md` khối đầu + khối có tên mình ⇒ `session_prompt/sessions/STATUS_<X>.md` của mình.
2. Máy mở lại: `/tmp` MẤT (worktree ghi trong sổ từng phiên phải tạo lại), `docker compose up -d qdrant`, kiểm 9.479 điểm. Việc nặng (server, đo, cả bộ test): phiên làm báo phiên điều phối một dòng; phiên điều phối hỏi "ok?" phiên điều phối của hai dự án khác KHI họ đang mở phiên và chờ một dòng; xong nhắn "máy trả".
3. Dòng theo giờ các ngày trước: `report_agent/<ngày>/TONG_HOP.md`; bản tới tối 19/11: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-19.md`.

## Ghi trong ngày (phiên điều phối nối dòng mới ở đây; cuối ngày dời sang `TONG_HOP.md` của ngày)
- 09:09 23/11/2026 — MỞ PHIÊN SÁNG 23/11 (MÁY KHỞI ĐỘNG LẠI 08:59: `/tmp` mất, Docker 0 container ⇒ phiên điều phối bật lại Qdrant 09:05, 9.479 điểm; bốn bản chụp Qdrant của 22/11 mất theo container cũ, chỉ mục nguyên; phiên điều phối `hue-rag-1d`, B `hue-rag-1c`, C `hue-rag-3c`, D `hue-rag-cf`, phiên đo `hue-rag-eb`; chủ dự án có mặt, hôm nay tự test). Giao ngay trong tin mở phiên: phiên đo đọc nhánh an toàn rồi chạy nốt cổng gộp giao diện · C chữa lỗi cổng + làm mới gói Docker · B tra cứu + trang phương án hạ tầng cho việc chuẩn bị deploy, xen các phép đếm harness, nhận thêm hai điểm Carbon từ phiên đo · D chờ phiếu. Phiên điều phối tự mở ảnh màn đầu ở cỡ máy demo: NHẬN "bến chỉ còn tên". Ba dòng theo giờ còn lại của ngày 22/11 đã dời sang `report_agent/2026-11-23/TONG_HOP.md`.
