# Review: "Huế qua các thời kỳ" (B, nhánh `p9-hue-thoi-ky` `67d63a9`)

Cập nhật: 15:12 14/11/2026 (C). Kết luận: **ready_for_user_confirmation**. Gắn vào Giới thiệu trên nhánh `p9-gd-anh-gt` (`6b47ec1`).

## Đã kiểm
- **Chữ ↔ kho:** đọc từng dòng kho trong `data/hue_thoi_ky_2026-11-14/can_cu.json` (bài + số dòng), so với chữ của 6 mốc.
  - Mọi năm, ngày, tên người và sự việc đều có đúng ở dòng được dẫn.
  - 0 ý vượt kho, 0 số sai.
  - Chỗ hai bài kho lệch nhau về năm Tây Sơn đóng đô (1786 ↔ 1788) đã được B né đúng: màn chỉ nêu mốc 1788 lên ngôi, cả hai bài cùng khớp.
- **Ảnh:** 6 / 6 file có trong `public/anh/lich/`. Không có chữ ghi công.
- **Chạy thật:** chạy trên bản build của nhánh C (cổng 8873), khổ 1366 và 390.
  - 0 lỗi console.
  - Khổ hẹp: mọi khối có độ mờ 1,0 sau khi cuộn.
  - Khổ rộng: 5 / 6 mốc ở độ mờ 0,42. Đây là đúng thiết kế: chỉ mốc đang đọc rõ.
  - Máy giảm chuyển động: hiện đủ.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor | `hue_thoi_ky.css` `.tk-buoc:not(.tk-dang) { opacity: .42 }` | Ở khổ rộng, chữ của mốc chưa đọc tới bị nhạt khá mạnh, độ tương phản có thể dưới mức dễ đọc. Ai muốn đọc lướt trước thì khó. | nâng lên khoảng .55, hoặc giữ nguyên nếu User xem thấy ổn |
