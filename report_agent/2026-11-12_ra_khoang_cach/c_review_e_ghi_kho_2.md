# Review nhẹ — gói ghi kho lần 2 của E (bài lưu trú vào chỉ mục) · C · 13:29 14/11/2026

A giao: tính lại 2–3 số chính của `e_ghi_kho_luu_tru_implementation.md` từ file kết quả. 0 USD; chỉ đọc file kết quả "trước" / "sau" của E.
Không chấm lại chất lượng câu trả lời, không xem lại nội dung bài.

**Kết luận: ready — 0 blocker · 0 major · 0 minor.** Mọi số C tính lại đều khớp report.

## Số tính lại

| Số trong report | C đếm lại từ file | Khớp |
|---|---|---|
| K1 Golden 176: từ chối 23 ⇒ 23 | 23 ⇒ 23. Mới từ chối 4 câu, hết từ chối 4 câu | khớp |
| K1: 8 câu đổi từ chối có ngữ cảnh lần tìm đầu giống hệt, các lần tìm thêm không có đoạn lưu trú ⇒ nhiễu | 8 / 8 câu có `top_chunk_ids` giống hệt hai bên; 0 / 8 câu có đoạn lưu trú (cả kết quả lần tìm thêm) | khớp |
| K1: 0 lỗi kỹ thuật, 0 lỗi trích dẫn | 0 · 0 (hai bên) | khớp |
| K1: 2 câu có đoạn lưu trú | 2 câu | khớp |
| K2 an toàn 32: 0 câu chạm đoạn mới, 0 câu đổi lớp | 0 câu có tiêu đề bài lưu trú trong ngữ cảnh; 0 câu đổi lớp; 0 lỗi | khớp |
| K4 lưu trú 12: được trả lời 4 ⇒ 11 / 12, 0 câu nêu giá | 4 ⇒ 11 / 12; 0 câu có số tiền (dò mẫu số + đồng / VNĐ / k / nghìn / triệu) | khớp |
| Tiền "trước": Golden 0,0749 | 0,0749 (cộng trường `usd`) | khớp |

## Ghi chú (không phải finding)

- Lần đếm đầu C ra "0 câu Golden có đoạn lưu trú". Lý do: C đọc nhầm trường `context_sources`, trường này chỉ là **số** nguồn chứ không phải tên.
  Tên đoạn nằm ở `top_chunk_ids`. Đếm lại theo trường đó thì đúng 2. Ghi lại để người tính lại sau không vấp cùng chỗ.
- K4 là câu E tự viết, không phải bộ Golden, nên số 11 / 12 chỉ là dấu hiệu bài mới được tìm thấy. Trong ngữ cảnh, 10 / 12 câu có đoạn
  lưu trú. Phần chấm mù "0 điều không có trong ngữ cảnh" C không chấm lại.
