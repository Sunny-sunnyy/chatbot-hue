# Implementation Report: B173 — 3 bản mẫu HTML tĩnh cho cổng đợt 1

Người làm: B (Claude Code, Opus 5.5)
Date: 22:40 06/11/2026 (`date`) — dừng khi User kết phiên; phần dựng + chụp + đo đã xong.
Canonical guide: tin A giao B173 (giữa 22:27 và 22:40 06/11/2026 — sau khi B báo xong B172, trước lệnh `date` lúc dừng); 15 mẫu ở `data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md` §3.

## 1. Phạm vi

Ba bản mẫu tĩnh để User chọn hướng nhìn cho cổng đợt 1. 0 USD, không sửa `frontend/`.

Mỗi bản có 4 cảnh:
- trang chủ: ô hỏi lớn + chip gợi ý + 5 ô khám phá + khối xếp lịch + ô thời tiết;
- danh sách Di tích;
- chi tiết Lăng Tự Đức: bài kho + hộp thông tin + nút "Hỏi trợ lý về điểm này" + câu trả lời mẫu có dòng "Nguồn: …";
- khung chat: laptop góc phải; điện thoại phủ màn + thanh dưới có nút giữa.

## 2. Thay đổi chính (`data/nghien_cuu_giao_dien_2026-11-06/`, private)

- `mau/1.html`, `2.html`, `3.html` sinh từ `tools/dung_mau.py`: cùng nội dung, 3 bộ màu / bo góc / điểm nhớ. Mở thẳng file, đổi cảnh bằng `#trang-chu` / `#danh-sach` / `#chi-tiet` / `#chi-tiet-chat`.
  - **1 Son thếp:** đỏ son `#8F1D1D` và vàng thếp trên nền giấy. Viền hồi văn vàng trên / dưới hero. Ô hỏi kiểu tấm hoành phi viền vàng. Góc vuông 4–6 px.
  - **2 Sông Hương:** xanh ngọc `#0E6B66`, nước sâu `#0A3D40`, sen `#9C2A4F` cho nút "Hỏi trợ lý". Hero căn giữa có sóng SVG. **5 chủ đề là 5 "bến" dọc một đường sông** (điện thoại: đường sông dọc). Bo tròn.
  - **3 Tím Huế trầm:** đúng bộ màu `frontend/src/index.css` hiện tại (`#3D1A5C` / `#5B2C83` / vàng `#E9B949` trang trí), nét sông vàng như dải đầu trang hiện nay, hero hai cột. Làm mốc so sánh.
- Chữ: chỉ **Be Vietnam Pro** (gói đã có; woff2 chép vào `mau/fonts/`). Không thêm font mới, các bản khác nhau bằng độ đậm / cỡ.
- Ảnh: chưa có ảnh được phép ⇒ khối hoa văn CSS / SVG có nhãn "Chỗ ảnh: <tên>".
- Chữ mẫu:
  - Tên bài thật trong kho (9 bài di tích, tiêu đề mục của bài Lăng Tự Đức).
  - Số bài mỗi chủ đề đếm thật (91 / 29 / 27 / 13 / 47 file).
  - Khu vực lấy từ cụm của `diem_v3.json`; giờ chung Quần thể 07h00 – 17h30. Tóm tắt và câu trả lời mẫu viết lại ngắn.
  - Đoạn gốc trích 1 dòng.
  - **Số thời tiết là số mẫu** (ghi trên trang).
  - Câu gợi ý tự viết, không dùng Golden / câu kín.
- `tools/chup_mau.py` (Playwright, file trên máy, không mạng), `tools/do_tuong_phan.py` (đo tương phản chữ thật trên trang), `tools/ghep.py`.

## 3. Cách đã chạy thật

Từ gốc repo:
- `uv run python data/nghien_cuu_giao_dien_2026-11-06/tools/dung_mau.py` — sinh 3 file.
- `timeout 300 uv run python …/tools/chup_mau.py` — 3 bản × 4 cảnh × 1440 / 390 = **24 ảnh** `mau/anh/`.
- `timeout 300 uv run python …/tools/do_tuong_phan.py`.
- Bản ghép so 3 bản cạnh nhau: `mau/anh_nho/so_<cảnh>_<cỡ>.jpg`.

## 4. Kết quả quan sát [Chạy]

- 24 / 24 cảnh: không tràn ngang, font nạp được, 0 lỗi console / 0 request hỏng.
- **Tương phản:** mọi chữ nhìn thấy ≥ 4,5:1 (chữ lớn ≥ 3:1), đo trên màu đã trộn nền. 6 chỗ dưới ngưỡng đều là nhãn ẩn chỉ cho trình đọc màn hình ("Câu hỏi", khung 1 px) — không phải chữ hiển thị.
- Đã sửa sau lần soát ảnh đầu:
  - nhãn khối xếp lịch lệch dòng ⇒ chuyển sang lưới 2 cột;
  - ô thời tiết header lặp với ô trong hero ở trang chủ ⇒ ẩn ở trang chủ;
  - bản 2 điện thoại: "91 bài" đè đường sông ⇒ thụt vào;
  - bỏ dấu "·" ở dòng phụ (chỉ dòng Nguồn dùng);
  - thẻ Nhã nhạc ghi sai "Bài tư liệu" ⇒ "Không có giờ mở cửa".

Tiền: 0 USD.

## 5. Lỗi và giới hạn

1. **Chưa có người khác soát** (A / User xem ảnh). B tự soát bằng ảnh + phép đo.
2. Ảnh cả trang (full page) vẽ nút "Hỏi trợ lý" nổi / thanh dưới điện thoại **chồng giữa trang** — do cách chụp phần tử cố định, không phải lỗi bố cục (xem ảnh `*-chat` màn đầu cho vị trí thật).
3. Danh sách và chi tiết dùng **chung bố cục** ở cả 3 bản (khác màu / bo / điểm nhớ ở trang chủ). Muốn so cả bố cục ⇒ làm thêm.
4. Một font cho cả 3 bản ⇒ khác biệt về chữ ít. Nếu User muốn tiêu đề có chân (hợp bản 1), cần **thêm 1 gói `@fontsource`** — chưa cài, A / User duyệt.
5. Chip, nút chỉ là hình (không chạy thật); "Trợ lý AI" ở menu mở khung chat ở trang chi tiết; "Bản đồ" ghi "sắp có" (đợt 2).
6. Chưa kiểm bàn phím / trình đọc màn hình kỹ (có `:focus-visible`, nhãn ẩn cho ô nhập, `aria-pressed` cho chip, `role=dialog` cho khung chat).

## 6. Bàn giao cho người kiểm

- Xem nhanh: `mau/anh_nho/so_trang-chu_1440.jpg`, `so_trang-chu_390.jpg`, `so_chi-tiet_1440.jpg`, `so_chat_390.jpg`. Ảnh đủ cỡ: `mau/anh/<bản>_<cảnh>_<cỡ>.png`.
- Mở trực tiếp `mau/1.html#chi-tiet-chat` … trong trình duyệt.
- Chạy lại: các lệnh mục 3 (0 USD).
