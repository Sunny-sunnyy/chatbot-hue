# Đếm 2 hướng mở rộng ảnh chat (E dò hệ thống) — C, 12:30 15/11/2026

0 USD. Script `data/anh_chat_2026-11-15/tools/dem_bien_the.py` + `bien_the.mjs` (gọi chính `anhTraLoi.js` đang chạy trên main, thêm biến thể bên ngoài; không sửa giao diện) ⇒ `bien_the.json`. Cùng 154 câu đã lưu như T3; câu hỏi lấy từ Golden (private, không ghi ở đây).

| Biến thể | Câu có ảnh | Ảnh | Thêm |
|---|---|---|---|
| Hiện hành (main) | 103 / 154 | 116 | — |
| (a) nguồn trích có đúng 1 bài "một nơi" có ảnh chắc ⇒ dùng ảnh đó | 108 | 121 | +5 câu |
| (b) khớp tên bài trên cả **câu hỏi** (bài vẫn phải được trích) | 106 | 119 | +3 câu |
| (a) + (b) | 109 | 122 | +6 câu |

**Nhìn lại ảnh mới (C, đọc câu trả lời cạnh bài + xem ảnh):**
- **(a): 2 / 5 lạc đề.**
  - Một câu hỏi về trang phục vào một điện thờ ⇒ ảnh bài tổng quan quần thể di tích.
  - Một câu hỏi xe máy qua hầm đèo ⇒ ảnh vịnh biển ở đầu kia đèo.
  - Bài được trích chỉ là nguồn phụ, câu trả lời không nói về nơi trong ảnh.
  - 3 / 5 còn lại hợp.
- **(b): 3 / 3 đúng.** Tên nằm trong câu người dùng hỏi nên đó là nơi họ hỏi. Ảnh đúng nơi: lối vào một đàn tế, thuyền trên sông cho bài ca Huế, biệt thự trên núi (`xem_lai_b.jpg`).

**Đề xuất:** làm **(b)**, **không** làm (a). (a) thêm ảnh bằng cách đoán "nguồn duy nhất là nơi đó", và đoán sai 2 / 5. (b) giữ đúng ý "ảnh của thứ đang được nói tới".
Plan bản 2: mục cuối của `docs/superpowers/plans/2026-11-15-anh-trong-chat-plan.md`.
