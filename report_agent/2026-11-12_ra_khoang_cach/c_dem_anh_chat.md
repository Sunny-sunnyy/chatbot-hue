# Đếm trước khi xây — "ảnh trong chat" theo tên nơi / món / khách sạn (C, 11:26 15/11/2026)

Việc A giao 15/11 (User muốn: câu trả lời nhắc bún bò ⇒ ảnh bún bò; nhắc Kinh thành ⇒ ảnh Kinh thành; cả khách sạn). 0 USD, chỉ đọc câu trả lời đã lưu.
Script `data/anh_chat_2026-11-15/tools/dem.py` ⇒ `data/anh_chat_2026-11-15/dem.json` (gồm danh sách câu, private).

## Tập đếm
- Câu trả lời Golden đã lưu trên kho 6: lượt mới nhất của từng câu (lượt đủ 176 câu sau ghi kho 2, đè bằng lượt sau ghi kho 6 và lượt đo bù 65 câu).
- Còn **154** câu có trả lời; bỏ 22 câu từ chối / lỗi.
- **Không có câu nào về khách sạn**: 0 / 154 câu nhắc tên một trong 137 cơ sở. Phần khách sạn **chưa đo được** trên tập này; muốn đo phải tự đặt câu.

## Số đếm [đã chạy]

| Đo gì | Số | Ghi chú |
|---|---|---|
| Luật hiện hành hiện ảnh | **77 / 154** (50 %) | luật: mọi nguồn trích thuộc MỘT bài "một nơi / món", ảnh chắc |
| Câu nhắc tên ≥ 1 bài "một nơi / món" | 83 / 154 | khớp tên bài + "Tên gọi khác" trong chữ trả lời |
| … trong đó bài có ảnh chắc | **80 / 154** | 201 / 244 bài "một nơi / món" có ảnh chắc |
| … luật hiện hành đã hiện ảnh | 39 | |
| … luật hiện hành **không** hiện | **41** | 22 câu nhắc 1 nơi, 19 câu nhắc 2 nơi |
| Vì sao 41 câu đó không có ảnh | nguồn trích thuộc ≥ 2 bài 32 · bài được trích là loại khác (vé, tổng quan, lưu trú) 5 · không trích 3 · bài trích không có ảnh chắc 1 | |
| Luật cũ hiện mà chữ không nhắc tên bài | 38 | câu trả lời không gọi tên nơi (vd "quán mở lúc…"), hoặc gọi khác tên bài |
| Nếu **giữ luật cũ + thêm** ảnh theo tên khớp (≤ 3) | 77 + 41 = **118 / 154** (77 %) | |
| Số ảnh nếu hiện mọi tên khớp (≤ 3 / câu) | 107 trên 80 câu | 54 câu 1 ảnh · 25 câu 2 ảnh · 1 câu ≥ 3 |

**Độ đúng của khớp tên** (C soát tay 20 câu ngẫu nhiên, 24 lần khớp): 23 / 24 đúng nơi / món câu trả lời đang nói.
- 1 lần đáng ngờ: tên quán là một cụm thông dụng ("quán nhỏ"), có thể khớp nhầm với lời thường.
- 10 bài có tên ≤ 2 từ từng khớp (vd tên quán, suối, chợ, ga). Đây là nhóm dễ khớp nhầm nhất ⇒ nếu xây thì cần danh sách chặn tên thông dụng, hoặc đòi khớp cả nguồn trích.
- Khớp qua "Tên gọi khác" đúng ở 1 / 1 lần gặp.

**Xấp xỉ đã dùng:** "nguồn trích" = đoạn thứ n trong top 10 cho mỗi [n] của câu trả lời (lượt đo không lưu danh sách nguồn đã gói). Cách đếm luật cũ ở đây vì vậy có thể lệch vài câu so với giao diện thật.

## Gợi ý thiết kế để bàn (chưa làm)
- Giữ luật cũ, thêm: **code** khớp tên bài / tên khác trong chữ trả lời.
  - Chỉ tính bài thuộc loại "một nơi / món", ảnh chắc (không `kc`).
  - Nên đòi thêm: bài đó nằm trong **nguồn được trích** (chặn khớp nhầm tên thông dụng; ước mất ít vì 32 / 41 câu thiếu ảnh là do trích ≥ 2 bài — tức bài có trong nguồn).
  - Tối đa 3 ảnh, theo thứ tự tên xuất hiện. Model không chọn ảnh.
- Khách sạn: cùng cách với tên trong bảng 137 cơ sở (69 có ảnh). Cần ≥ 10 câu tự đặt để đo, vì tập Golden không có câu khách sạn.
- Lợi ước trên tập này: câu có ảnh **77 ⇒ ~118 / 154**. Đây là ước trước khi xây, không phải số đo.
