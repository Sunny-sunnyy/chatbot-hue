# Review nhánh `p9-gd-anh-gt` `fc77b25` (C + màn thời kỳ của B) · E · 15:19 14/11/2026

Phạm vi: bỏ ghi công ảnh ở Khám phá / trang bài / Giới thiệu + chân trang; Giới thiệu sửa chữ "làm được gì / giới hạn", dải "Kho tư liệu", gắn màn
"Huế qua các thời kỳ" (B). Mức nhẹ, một review cả nhánh, 0 USD.

## Kết luận: `changes_requested` nhẹ — 1 major (một câu chữ hứa sai), sửa 1 dòng rồi A merge, không cần E kiểm lại cả nhánh

## Đã kiểm
- Diff 10 file, đúng phạm vi; không chạm file của E. Gộp với `p9-gd-anh-e` sạch (merge thử `a2cfafc`, build đạt, JS chính 124,44 KB gzip).
- **Không còn chữ ghi công trên giao diện** (Playwright bản build gộp, 1440 + 390, có / không giảm chuyển động): Giới thiệu, Khám phá, một lĩnh vực, một
  trang bài ⇒ 0 chuỗi "Ảnh: / CC BY / Phạm vi công cộng / Commons / đã thu nhỏ / Ảnh minh hoạ / Nguồn ảnh"; trang bài 0 `figcaption`;
  `ghi_cong.json` không còn trong `dist/`. Lỗi console 0; cuộn ngang 0.
- **Khối hiện dần không kẹt:** sau khi cuộn hết trang (hiệu ứng bật, 1440), khối duy nhất còn mờ là 5 mốc thời kỳ chưa đọc (độ đậm 0,55 — đúng
  thiết kế m-1); giảm chuyển động ⇒ 0 khối mờ.
- **Màn thời kỳ:** E dò 12 mốc số / tên trong kho bằng `grep_kb.sh` — 1306, Trần Anh Tông, châu Ô, 1636, 1687, núi Bân, 1805, 143 năm, gạch vồ,
  1920, 30/08/1945, 11/12/1993, 01/01/2025, Thái Hòa nghiệm thu 11/2024 ⇒ đều có trong kho. Ảnh dùng lại bộ ảnh lịch (không thêm ảnh).
- Dải "Kho tư liệu": số bài đếm từ `/api/kham_pha` (không gõ tay); lỗi tải ⇒ không hiện.
- Giới hạn: bỏ "nơi lưu trú" khỏi "chưa có" — đúng (kho có bài lưu trú từ 14/11).
- Test: `test_static_ui` + `test_cong_dot_1` 26 đạt (cây gộp).

## Finding
- **M-1 (major, chữ hứa sai):** thẻ "Thời tiết Huế" ghi "Dự báo 7 ngày tới ở trang chủ" — trang chủ chỉ hiện **hôm nay** (`TrangChu.jsx` đọc
  `tt.hom_nay`; `/api/thoi_tiet` chỉ trả `hom_nay`). Đóng khi: đổi thành ý đúng, vd "Thời tiết hôm nay ở trang chủ; hỏi trợ lý “mai trời thế nào”
  để có dự báo tới 7 ngày, kèm nguồn." (trợ lý: ngoài 7 ngày ⇒ câu cố định — B5b).
- **m-1 (ghi chú, phần của E):** bundle còn 2 chuỗi "Phạm vi công cộng" + tên tác giả trong `anh.js` (trường `tacGia / giayPhep`, `GP`, `MOI_ANH`)
  — không hiện ra giao diện. E dọn trên nhánh `p9-gd-anh-e` **sau khi** nhánh này vào main (main hiện vẫn dùng `MOI_ANH` ở Giới thiệu) ⇒ A
  merge C trước rồi E.
