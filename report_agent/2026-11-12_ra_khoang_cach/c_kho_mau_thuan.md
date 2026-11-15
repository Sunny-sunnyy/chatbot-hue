# Kho tự mâu thuẫn — đếm + tra nguồn (C, 11:08 15/11/2026)

Việc A giao 15/11, bước đầu của việc (5) "kho tự mâu thuẫn". **Chưa sửa kho**: web mâu thuẫn kho ⇒ không tự chọn phía, A trình User.
Tiền: Serper 2 lượt ≈ 0,002 USD; WebFetch 0. Grep chỉ qua `scripts/grep_kb.sh`. Script `data/kho_mau_thuan_2026-11-15/tools/` (`quet.py`, `unesco.py`, `tim.py`); kết quả tìm `tay_son_{1,2}.json`.

## Kết quả

| # | Loại | Trạng thái kho | Nguồn công khai | Đề xuất |
|---|---|---|---|---|
| 1 | Vị trí một bảo tàng | **Đã khớp.** Mọi bài nhắc tới đều ghi cùng một chỗ (trong Kinh thành, bờ Bắc, cùng số nhà). Lệch từng ghi ngày 06/11 đã hết, có lẽ sửa ở lần ghi kho 14/11. | — | Đóng, không làm gì |
| 2 | Năm một triều đại đóng đô (1786 ↔ 1788) | **Còn lệch.** Hai bài di tích lớn ghi hai năm bắt đầu khác nhau cho cùng giai đoạn kinh đô; năm kết thúc (1801) khớp. Các bài khác dùng 1786 cho sự kiện chiếm thành, 1788 cho lễ lên ngôi — đúng sự kiện. | Nguồn **không trái nhau, mà nói hai sự kiện**: 1786 là năm quân Tây Sơn chiếm Phú Xuân (khamphahue.com.vn, 29/07/2018: "giải phóng Thuận Hóa – Phú Xuân (1786)"; "Ngày 20/6/1786, quân Tây Sơn đánh thành Phú Xuân"); 1788 là năm Nguyễn Huệ lên ngôi tại Phú Xuân — "triều đại này chỉ thực sự bắt đầu từ năm 1788" (cùng trang); Tạp chí Đông Nam Á 29/11/2024 ghi Phú Xuân là kinh đô "dưới triều Tây Sơn (1788–1802)". Cổng hue.gov.vn đặt tên giai đoạn "Thời Tây Sơn (1786–1801)" (tiêu đề; trang tải bằng JavaScript, WebFetch không đọc được thân bài). | **Chờ User.** Gợi ý: thống nhất hai bài thành "Tây Sơn làm chủ Phú Xuân từ 1786; Phú Xuân là kinh đô từ khi Quang Trung lên ngôi (1788) tới 1801" — đúng cả hai mốc, không bỏ năm nào. Sửa 2 câu ở 2 bài, sao lưu `meta/`, dựng lại chỉ mục, đo câu đổi top 10. |

## Quét thêm (có giới hạn, ~25 phút, 0 USD)
- **Năm xây / dựng / ghi danh của một nơi ở bài khác ↔ bài riêng của nơi đó** (`quet.py`): 7 ứng viên, soát tay **0 lệch thật**. 6 khớp nhầm câu kế bên (vd năm của công trình khác đứng sau tên); 1 là năm hành chính.
- **Năm UNESCO ghi danh** của 7 di sản tư liệu / phi vật thể / thế giới (`unesco.py`): **0 lệch**. Các năm "lạ" là câu liệt kê nhiều di sản trong một câu, hoặc là hai mốc đúng của cùng một di sản (vd một di sản ghi danh cấp khu vực trước, cấp thế giới sau; được công nhận một năm, chuyển sang danh sách đại diện năm khác) — bài ghi cả hai mốc.
- **Giá vé + giờ một điểm chính giữa các bài:** giá khớp (số khác duy nhất là phí xe điện, không phải giá vé); giờ chưa so được bằng mẫu đơn giản (cách viết giờ khác nhau) — không quét thêm.
- **Không quét:** mọi năm × mọi thực thể (quá rộng, nhiều khớp nhầm). Loại chưa quét: số đo (chiều cao, diện tích), tên người xây.

## Kết luận
1 chỗ còn lệch (năm đóng đô), cần User chọn câu sửa; 1 chỗ đã tự hết (vị trí bảo tàng). Quét giới hạn không thấy chỗ lệch mới. Nếu User duyệt: việc sửa nhỏ, ≈ 0,02 USD (đo câu đổi top 10).
