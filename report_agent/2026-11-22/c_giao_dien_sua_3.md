# Giao diện cho "thêm điểm không tự thế chỗ" — report của phiên C (viết 08:57 22/11/2026)

Việc: sổ việc khối A, gạch "ĐÃ Ở MAIN, CHƯA MỞ" — tính năng `sua_lich_them_khong_the` (thêm X vào buổi đã kín thì KHÔNG tự thế chỗ một điểm đang có,
mà nói rõ và gợi ý câu "thay Y bằng X") bị chặn bởi hai chỗ giao diện phiên đo thấy tối 21/11. Nhánh `p9-c-giao-dien-sua-3`:
`frontend/src/App.jsx`, `frontend/src/chat.jsx`, một dòng chú thích ở `backend/config/settings.yaml` (công tắc VẪN TẮT — phiên điều phối mở sau khi có
người nhìn). Người đọc / nhìn: phiên E.

## 1. Người dùng thấy gì khác

| Chỗ | Trước (lượt đo 21/11) | Sau (lượt nhìn 22/11, model đang chạy) |
|---|---|---|
| Thẻ lịch trên trang Lên kế hoạch, sau một lượt sửa KHÔNG áp được gì ("Thêm lăng Khải Định vào sáng ngày 1") | không có dòng nào về lệnh thêm; còn giữ dòng "Chưa làm: phần câu hỏi…" của lượt TRƯỚC | "Đã bỏ Chùa Thiên Mụ." (của bản lịch đang hiện) + "Chưa làm: thêm Lăng Khải Định … bạn nhắn đủ câu: thay Lăng Đồng Khánh bằng Lăng Khải Định (buổi sáng ngày 2)."; dòng "Chưa làm" cũ không còn |
| Trang trợ lý trên điện thoại (390), lượt sửa không áp được gì | vẽ lại cả tấm lịch dưới dòng báo, phải cuộn ngược | chỉ khối báo + nút "Xem cả lịch" (lượt cao 265 px thay cho hơn 4.000 px); bấm nút vẫn mở đủ lịch 2 ngày |
| Khung trợ lý nổi (1440), lượt sửa lịch bất kỳ | khung chỉ cuộn lúc gửi câu ⇒ khối báo về sau bị cắt đuôi dưới mép (câu gợi ý "thay … bằng …" phải cuộn mới thấy — ảnh `luot_1/1440_luot_2_o_chat.png`) | lượt sửa lịch vừa xong ⇒ khung cuộn lại tới đầu lượt: câu hỏi, cả khối báo và nút "Xem cả lịch" nằm trọn trong khung |
| Trang trợ lý trên điện thoại, lượt "vừa sửa vừa hỏi" (có thay đổi làm được ⇒ vẫn vẽ cả lịch) | dòng "Đã bỏ…" nằm sát mép dưới, dòng "Chưa làm: phần câu hỏi…" bị khuất | câu hỏi lên đầu màn hình, hai dòng báo nằm trọn trong màn hình đầu |

Điều chỉnh so với ghi chú của phiên đo: ở khung nổi, lượt cuối vốn ĐÃ gọn từ 16/11 (không vẽ lại lịch); ảnh tối 21/11 chụp cả trang nên trông như cả
tấm lịch đè lên — lỗi thật ở đó là vị trí cuộn (dòng trên bảng).

## 2. Code đổi gì (ba chỗ nhỏ)

- `App.jsx`: thẻ lịch của trang lấy thêm khối báo của lượt sửa XONG mới nhất khi lượt đó không áp được gì — ghép "các dòng Đã… của bản lịch đang hiện" +
  "dòng báo của lượt mới". Lịch hiển thị không đổi (vẫn là bản tốt gần nhất).
- `chat.jsx`: (a) lượt sửa không có dòng nào làm được ⇒ vẽ gọn ở cả trang trợ lý (dùng lại đúng kiểu gọn sẵn có của khung nổi); (b) lượt sửa lịch
  chuyển sang "xong" ⇒ cuộn lại tới đầu lượt. Chỉ áp cho lượt sửa lịch: câu trả lời thường có thể đang chạy chữ dần, cuộn lại sẽ giật khỏi chỗ đang đọc.
- `settings.yaml`: chú thích của `sua_lich_them_khong_the` hết ghi "chờ đo cả hai model và chủ dự án chọn" (trái quyết định 21:43 / 21:50 21/11).

## 3. Bằng chứng [máy kiểm — phiên C tự nhìn; chờ phiên E nhìn]

Server tạm cổng 8011 từ cây nhánh (giao diện dựng lại từ nhánh), công tắc `sua_lich_them_khong_the` ghi đè MỞ trong bộ nhớ, model đang chạy. Chuỗi như lượt
đo 21/11: xếp lịch 2 ngày ⇒ "Bỏ điểm đầu tiên của ngày 2 khỏi lịch, à mà vào Đại Nội thì nên mặc gì?" ⇒ "Thêm lăng Khải Định vào sáng ngày 1"; hai khổ
1440 và 390. Script + ảnh ĐÚNG KHUNG NHÌN + số (riêng tư): `data/test_cuoi/chay_2026-11-22_c_gd3/` (`nhin.py`; `luot_1/` = trước khi thêm bước cuộn lại,
`luot_2/` = bản cuối). Phép đo "thấy trọn" = điểm đầu và điểm cuối của từng dòng không bị thứ khác che (`elementFromPoint`).

| Khổ · lượt | Lượt cao | Câu hỏi | Mọi dòng báo | Nút "Xem cả lịch" |
|---|---|---|---|---|
| 1440 · sửa kèm hỏi | 264 px (gọn) | thấy trọn | 2 / 2 thấy trọn | thấy trọn |
| 1440 · thêm (không áp được) | 237 px (gọn) | thấy trọn | 1 / 1 thấy trọn | thấy trọn |
| 390 · sửa kèm hỏi | 4.311 px (vẽ cả lịch — có thay đổi làm được) | thấy trọn, ở đầu màn | 2 / 2 thấy trọn | (không có — lượt vẽ cả lịch) |
| 390 · thêm (không áp được) | 265 px (gọn) | thấy trọn | 1 / 1 thấy trọn | thấy trọn |

Cả hai khổ: thẻ lịch sau lượt cuối = "Đã bỏ Chùa Thiên Mụ." + dòng "Chưa làm: thêm Lăng Khải Định…", vẫn vẽ đủ 2 ngày; bấm "Xem cả lịch" ra 2 ngày;
tràn ngang 0; lỗi trang 0. Tiền: 12 lượt, 0,2075 USD (`scripts/dem_chat_metrics.py --sha 2671accf`).

## 4. Chưa làm · giới hạn

- CHƯA: phiên E nhìn; mở công tắc (phiên điều phối); dựng lại `frontend/dist` ở cây chính sau khi gộp (`cd frontend && npm run build`); mục `bai_hoc/`.
- Giới hạn còn lại: thẻ lịch vẫn giữ dòng "Chưa làm: phần câu hỏi…" của lượt sửa-kèm-hỏi cho tới khi có lượt sửa kế (hành vi cũ, không đổi) · bước cuộn
  lại không áp cho câu trả lời thường (cố ý) · frontend không có bộ test tự động — bằng chứng là lượt nhìn trình duyệt.

Phép này KHÔNG cho biết: trình duyệt khác Chromium, điện thoại thật · hướng rộng hơn: cho lượt cuối một chiều cao tối thiểu bằng khung để mọi câu hỏi
luôn lên đầu khung ngay lúc gửi (cách các khung trò chuyện lớn làm) — đổi cảm giác cuộn của mọi lượt nên không làm ở đây · đếm rẻ nhất: không.
