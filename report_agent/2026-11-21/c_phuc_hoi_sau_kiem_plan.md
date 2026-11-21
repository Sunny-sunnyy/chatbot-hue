# Kế hoạch một trang — phục hồi sau khi kiểm SỐ không qua (nhánh `p9-c-phuc-hoi-sau-kiem`)

Viết: 13:21 21/11/2026 (giờ `date`), phiên C, TRƯỚC khi sửa code. Giao: phiên điều phối. Áp cả hai model. Nền: main `3c3aadef`.

Từ dùng: *phép kiểm số* = sau khi model viết, code so mọi con số thời tiết / khoảng cách trong chữ model với tập số được phép (số hệ thống in + số trong đoạn kho được trích);
*rút lại* = kiểm trượt ⇒ người dùng thấy "Câu trả lời không đáp ứng yêu cầu trích dẫn" + nút Thử lại, chữ đã hiện bị xoá.

## 1. Vì sao (số của lượt người dùng mô phỏng 21/11)

7 lượt bị rút (luna 3 / 48, Sonnet 4 / 53). Phát lại qua lõi, 6 / 7 lượt ra đúng lỗi: 5 lượt `weather numbers without source` — con số trượt là số NGƯỜI DÙNG gõ ("2 mm", "25 mm";
hệ thống in 2,1 và 25,4), 4 lượt nằm ở chính câu hỏi của lượt đó, 1 lượt ở câu hỏi liền trước; 1 lượt `distance numbers without source` — giờ đồng hồ "13h" bị đếm là thời lượng trong
một câu trả lời tốt. Không lượt nào thiếu trích dẫn thật.

## 2. Đổi gì

1. **Tập số được phép** của hai phép kiểm thêm: mọi con số trong câu hỏi của lượt này và trong CÂU HỎI LIỀN TRƯỚC (không lấy câu hỏi xa hơn, không lấy câu trả lời cũ — phiên điều phối duyệt mức này). Cách so số giữ nguyên (2 ≠ 2,1).
2. **Kiểm vẫn trượt ⇒ gỡ câu, không ném lỗi:** tìm đúng chỗ con số trượt nằm; gỡ đơn vị nhỏ nhất chứa nó (một câu trong đoạn văn, hoặc cả dòng nếu là dòng gạch đầu dòng / tiêu đề).
   Phần còn lại còn ít nhất một trích dẫn [n] và qua bộ kiểm trích dẫn ⇒ đó là câu trả lời (nấc 1). Không còn gì dùng được ⇒ câu từ chối cố định (nấc 2). Khối dự báo / câu bản tin
   chính thức do code nối vẫn nối như cũ ở cả hai nấc. Không còn kết cục "rút lại" cho hai phép kiểm này.
3. **Không che bệnh:** mỗi lần trượt ghi vào vết và số đo của lượt: loại kiểm, các con số trượt, số câu đã gỡ, nấc — để thước đếm được.
4. **Đường stream:** chữ đã hiện trước khi kiểm ⇒ thêm MỘT sự kiện `thay_chu` mang chữ cuối, phát trước `sources` khi chữ cuối khác chữ đã phát; giao diện (`frontend/src/chat.jsx`)
   thay chữ đang hiện bằng chữ đó. Cần dựng lại `frontend/dist` khi gộp.

KHÔNG làm ở nhánh này: bước kiểm trích dẫn (`Grounded answer has no citation`…) — chờ nhánh ba-sửa của phiên B vào main rồi làm cùng khuôn; (sửa sau khi duyệt: phép kiểm khoảng cách bỏ qua GIỜ ĐỒNG HỒ theo luật hẹp "lúc / từ / vào / trước / sau + 5–23 h" trên chữ model — phiên điều phối duyệt.)

## 3. Xong khi (ghi trước)

1. Phát lại 7 lượt bị rút (script riêng tư `phat_lai_rut.py`, chạy trên nhánh): 0 lượt có lỗi; ≥ 5 lượt giữ được câu trả lời của model.
2. Hai chiều (0 USD, chữ model dựng tay): 8 ca model tự thêm số KHÔNG có ở khối hệ thống in, không ở đoạn kho, không ở câu hỏi (4 thời tiết, 4 khoảng cách) ⇒ 8 / 8 con số đó
   không còn trong chữ gửi người dùng. 4 ca đối chứng không có số lạ ⇒ chữ gửi đi giống hệt chữ model.
3. Đường không trượt: các file test hiện có chạm đường này đạt; 10 lời gọi model chụp lại cùng mã băm với main.
4. Stream: test dựng app — lượt có gỡ câu phát `thay_chu` trước `sources`; lượt thường không có sự kiện mới.
Đo (phiên đo): sáu mục `rut_lai_*` của bộ câu khó; rào: an toàn 10 + ngoài phạm vi 10 không đổi.

## 4. Rủi ro đã thấy

- Người dùng đưa một con số SAI ("mai mưa 90 % phải không") và model nhắc lại như xác nhận ⇒ nay lọt qua phép kiểm. Chấp nhận: khối dự báo thật của hệ thống luôn nằm ngay dưới;
  lượt bão / lũ vẫn đi đường không-số của công cụ. Ghi giới hạn.
- Gỡ một câu có thể làm đoạn còn lại cụt ý. Đọc tay 7 lượt phát lại trước khi báo xong.
