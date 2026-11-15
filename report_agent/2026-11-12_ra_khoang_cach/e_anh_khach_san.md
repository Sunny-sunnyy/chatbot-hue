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

## Rà lại 69 ảnh đang chạy theo W78 (A giao, User duyệt "không đạt ⇒ gỡ") — 11:58 15/11/2026 (`date`)
- Agent con chấm 69 (`data/anh_khach_san_2026-11-15/ra_w78/cham_agent.json`), E nhìn lại cả 6 tấm ghép: **50 đạt** (biển / chữ tên đọc được), **19 không đạt** (ảnh resort từ trên cao, hồ bơi, mặt tiền không chữ, tên bị cắt). 0 ca trẻ em / mặt người / số điện thoại.
- Tìm ảnh thay cho 19 (Serper 38 câu ≈ 0,038 USD, câu "biển hiệu / entrance sign") ⇒ agent con chọn 10 ⇒ E nhìn lại cả 10, **nhận 8**: Lapochine (tảng đá khắc tên) · Azerai La Residence (cửa kính có tên) · Đường Sắt ("Railway Hotel") · Alba Spa · La Vela · Thiên Phú · TTC Imperial · Meliá Vinpearl. **Bác 2**: Silk Path (chữ quá nhỏ ở cỡ thẻ) · Villa Louise (chữ "Beach Boutique" khớp mục Villa Louise kia hơn — không chắc đúng mục).
- A review: ảnh La Vela dọc thu nhỏ không đọc được tên ⇒ E cắt lại phần biển + tầng đế (nhánh `p9-anh-lavela`).
- Kết quả: bảng v4 (md5 `c98ca8c19889`) — **58 / 137 có ảnh** (trước 69). Nhánh `p9-anh-ks-w78` (đã merge).

### 11 cơ sở bị gỡ ảnh — cho User tìm ảnh mặt tiền có biển tên
| Cơ sở | Hạng | Hiện trong lịch (lượt / 15.360 mô phỏng) |
|---|---|---|
| Khách sạn Indochine Palace | 5 sao | **5.708** — gợi ý ở mọi lịch trung tâm khi không chọn mức / chọn 4–5 sao |
| Khách sạn Bình Dương 4 (7/25 Hai Bà Trưng) | 1 sao | **3.488** |
| Khách sạn Silk Path Grand Huế (02 Lê Lợi) | 5 sao | 200 |
| Khách sạn nghỉ dưỡng Villa Louise (Hòa Duân, Phú Vang) | 2 sao | 72 |
| Khu nghỉ dưỡng Villa Louise Beach (49B Phú Thuận) | đạt chuẩn | 72 |
| Khách sạn nghỉ dưỡng SBH Gloria Hue | 4 sao | 72 |
| Khách sạn nghỉ dưỡng Làng Hành Hương | 5 sao | 0 (chỉ trang Chỗ ở) |
| Khách sạn Hạnh Đạt (15 Phạm Văn Đồng) | 2 sao | 0 |
| Khu nghỉ dưỡng ven sông Huế (588 Bùi Thị Xuân) | 2 sao | 0 |
| Khách sạn nghỉ dưỡng Vedana Lagoon (Phú Lộc) | 5 sao | 0 |
| Sankofa Village Hill (khu nghỉ dưỡng, Kim Long) | đạt chuẩn | 0 |

Ưu tiên: **Indochine Palace** và **Bình Dương 4** (hai cơ sở hiện nhiều nhất, nay là ô màu), rồi 7 cơ sở hiện trong lịch ở mục trên (Thành Nội, Thành Lợi…).

### Câu hỏi cho User (E không gộp — không đủ căn cứ)
- **Như Phú**: hai mục cùng tên, địa chỉ 16 và 14b Chu Văn An, cùng toạ độ Places, **mã danh mục khác nhau** (5326 — 1 sao; 17196 — đạt chuẩn). Có thể cùng một cơ sở đăng ký lại. Gộp hay giữ?
- **Villa Louise**: "Khách sạn nghỉ dưỡng Villa Louise" (Hòa Duân, 2 sao, mã 5187) và "Khu nghỉ dưỡng Villa Louise Beach" (49B Phú Thuận, đạt chuẩn, mã 17239). Hòa Duân thuộc vùng Phú Thuận ⇒ có thể là một khu. Gộp hay giữ?
