# Ảnh khách sạn — đếm cơ sở hiện trong lịch + tìm ảnh (E · 11:20 15/11/2026, `date`)

A giao 15/11 (User duyệt): tìm thêm ảnh theo luật W78 (`WORKFLOW.md` §3 mục 6), ưu tiên cơ sở hay hiện trong lịch; không ra ⇒ danh sách cho User.

## Đếm trước (0 USD, `data/anh_khach_san_2026-11-15/tools/dem_hien.py` ⇒ `dem_hien.json`)
- 3.840 khung mô phỏng × 4 lựa chọn chỗ ở (không chọn / 4–5 / 2–3 / 1 sao), code + bảng v3 đang chạy trên main.
- **Chỉ 33 / 137 cơ sở từng hiện trong lịch.** 61.044 ô cơ sở hiện ra, **55.084 có ảnh (90,2 %)**; tính riêng "không chọn mức": 97,6 % (số cũ, B).
- **7 cơ sở hiện trong lịch mà chưa có ảnh** (số lần hiện / 15.360 lượt mô phỏng):

| Cơ sở | Hạng | Hiện khi | Lần hiện |
|---|---|---|---|
| Khách sạn Thành Nội (57 Đặng Dung) | 2 sao | chọn 2–3 sao | 2.220 |
| Khách sạn Thành Lợi (11 Đinh Tiên Hoàng) | 1 sao | chọn 1 sao | 2.220 |
| Khách sạn Mimosa Fiori (199 Điện Biên Phủ) | 1 sao | không chọn + chọn 1 sao | 728 |
| Khách sạn Hoàng Tuấn (B16-17 Phạm Văn Đồng) | 2 sao | chọn 2–3 sao | 252 |
| Khách sạn Như Hiền 2 (18 Phạm Văn Đồng) | đạt chuẩn | chọn 1 sao | 252 |
| Khách sạn Sang Trọng (57 Phạm Văn Đồng) | đạt chuẩn | chọn 1 sao | 252 |
| Khách sạn Phúc Khang (Mỹ Thượng, Phú Vang) | đạt chuẩn | chọn 1 sao, ven biển bắc | 36 |

## Tìm ảnh (Serper 15 câu ≈ 0,015 USD; bỏ 1.888 URL đã xem ở các lượt trước)
**Kết quả: 0 ảnh thêm.** Không ảnh nào đạt W78 (ảnh phải tự cho thấy đúng nơi; chỉ có nguồn chính thức thì không đủ):
- Thành Nội: ảnh hồ bơi trên trang Tripadvisor của khách sạn. Không có biển tên, không có gì cho thấy đúng nơi.
- Mimosa Fiori: ảnh phòng có gối thương hiệu OYO (tên cũ "OYO 807 Mimosa Fiori"). Phòng giống mọi khách sạn OYO, không nhận ra được nơi.
- Hoàng Tuấn: mặt tiền toà nhà trên trang Agoda Huế của khách sạn. Không thấy biển tên.
- Thành Lợi / Phúc Khang: kết quả là cơ sở **cùng tên ở tỉnh khác** (Thanh Hoá; TP HCM). Sang Trọng: trang chung chung. Như Hiền 2: 0 ảnh mới.
- Gợi ý cho User: ảnh mặt tiền có biển tên (tự chụp, hoặc ảnh Google Maps / Facebook của chính cơ sở — agent không mở các trang đó). Ưu tiên Thành Nội và Thành Lợi: mỗi cơ sở hiện ở 2.220 lượt mô phỏng, tức mọi lịch trung tâm khi khách chọn đúng mức đó.

## Ghi cho A
- **71 ảnh khách sạn đang chạy được chọn theo luật B 14/11** (căn cứ: tiêu đề trang nêu đúng tên + cảnh hợp), có trước W78. Theo W78 thì một phần có thể không đạt (ví dụ ảnh phòng / hồ bơi không có biển tên). E **chưa** rà lại. Rà hay giữ: A / User quyết.
- 104 cơ sở chưa từng hiện trong lịch (chỉ có trên trang Chỗ ở) không tìm ảnh ở lượt này: lợi thấp (trang chỉ mở từ ô Nơi ở).
