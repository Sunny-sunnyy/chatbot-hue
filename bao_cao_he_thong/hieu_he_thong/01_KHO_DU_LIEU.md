# 01 — Cuốn sổ tay: chatbot biết những gì

*Bài để hiểu, viết 11/11/2026. Đọc khoảng 3 phút. Bài trước: [00 — cả hệ thống](00_CA_HE_THONG_TRONG_3_PHUT.md).*

## Cuốn sổ tay gồm gì

Ở bài 00, chatbot giống một người hướng dẫn viên luôn tra sổ tay. Bài này nói về chính cuốn sổ đó. Sổ có **204 bài viết tiếng Việt**, chia làm năm phần:

- **Món ăn** (91 bài): đặc sản Huế, quán ăn, quán cà phê.
- **Di tích** (29 bài): Đại Nội, Kinh thành, các lăng, chùa, Nhã nhạc…
- **Lễ hội** (27 bài): lễ hội và lễ tế trong năm.
- **Nghệ thuật biểu diễn** (12 bài): ca Huế, các chương trình biểu diễn.
- **Du lịch** (45 bài): biển, đầm phá, chợ, đèo, lịch trình mẫu, chi phí, vé.

Mỗi bài viết về một thứ, như một bài báo ngắn. Bài món ăn có mô tả món, ăn ở đâu, giá bao nhiêu, mở mấy giờ. Cuối bài ghi thông tin lấy từ đâu, phần lớn là
trang của tỉnh, báo và trang du lịch. Ngoài 204 bài này, chatbot không biết gì khác. Ba ngoại lệ có ghi rõ: ngày tháng và thời tiết do máy tính, và mục
"Từ web" ở cuối bài này.

## Vì sao phải tự soạn sổ, không để chatbot đọc thẳng trên mạng

Trên mạng, cùng một quán có thể có ba giờ mở cửa khác nhau, kèm quảng cáo và bài viết đã cũ nhiều năm. Nếu chatbot đọc thẳng như vậy mỗi lần có câu hỏi, không
ai biết trước nó sẽ nói gì. Soạn sổ một lần thì kiểm được trước: bài nào nói gì, lấy từ đâu, chỗ nào mâu thuẫn. Từ đó có một luật đơn giản: **chatbot chỉ
nói điều sổ có**. Câu trả lời tốt tới đâu phụ thuộc trước hết vào cuốn sổ.

## Vì sao mỗi bài phải "đọc riêng vẫn hiểu"

Đây là điều dễ bỏ qua nhất. Khi trả lời, chatbot **không đọc cả cuốn sổ**. Nó chỉ đọc khoảng 10 mẩu nhỏ cắt ra từ nhiều bài khác nhau (bài 02 sẽ kể cách
cắt). Nếu một mẩu viết "Quán này mở từ 6 giờ sáng" mà không nói quán nào, người viết không biết "quán này" là quán nào. Vì vậy các bài được viết sao cho
từng câu, từng dòng mang đủ tên và bối cảnh của nó. Câu lưu ý chung ở đầu một bài vé cũng được gắn kèm vào từng mẩu giá của bài đó, để mẩu nào được tìm ra cũng mang theo lưu ý.

## Sổ được giữ đúng như thế nào

- **Rà và sửa có kiểm.** Ví dụ: từ tháng 7/2025, Huế sắp xếp lại phường xã, nên nhiều tên phường trong sổ thành sai. Sổ đã được rà và sửa theo tên mới, tên
  cũ để trong ngoặc. Với chỗ không chắc, cách làm là **viết nhẹ đi** (bỏ con số không chắc) chứ không đoán. Sau mỗi lần sửa, chatbot được chấm lại để chắc rằng
  sửa không làm hỏng câu trả lời nào.
- **Sửa sổ thì chatbot biết.** Chatbot không lật sổ gốc mỗi lần hỏi. Nó dùng một bản đã chuẩn bị sẵn để tìm cho nhanh (bài 03 sẽ kể). Nếu sửa sổ mà quên
  làm lại bản chuẩn bị, hai bản sẽ lệch nhau. Lúc khởi động, chatbot tự so hai bản; lệch thì nó **không chạy**, để không trả lời bằng thông tin cũ. Giống
  thủ thư không cho mượn sách khi mục lục chưa cập nhật.

## Tốt tới đâu, khi nào hỏng

Sổ đủ cho phần lớn câu khách hay hỏi về ăn gì, đi đâu, vé, lễ hội. Có ba chỗ hỏng cần biết:

- **Sổ thiếu thật.** Ví dụ khách sạn, nhà nghỉ, giờ và giá của chợ hay chùa ngoài khu di tích, lễ hội đúng một ngày cụ thể. Khi đó chatbot nói "không đủ thông
  tin", rồi tra web một lần và hiện riêng một mục **"Từ web (chưa kiểm)"** để người dùng biết phần này không lấy từ sổ.
- **Sổ cũ dần.** Giá và giờ thay đổi theo thời gian. Câu trả lời về vé, điểm tham quan và lễ hội luôn kèm dòng "thông tin có thể đã thay đổi".
- **Sổ có mà tìm không ra.** Đây không phải lỗi của sổ mà của bước tìm. Nó lại là lỗi hay gặp nhất, nên có bài riêng (bài 03).

## Ba điều chính

1. Chatbot chỉ biết **204 bài trong sổ tay** (cộng ngày, thời tiết và mục web ghi riêng). Sổ tốt thì câu trả lời mới tốt.
2. Sổ được **soạn và kiểm trước**, và mỗi câu trong sổ phải **đọc riêng vẫn hiểu**, vì chatbot chỉ đọc vài mẩu nhỏ chứ không đọc cả cuốn.
3. Sổ thiếu hoặc cũ thì chatbot **nói không đủ thông tin** hoặc ghi "có thể đã thay đổi", chứ không đoán.

---
*Muốn tra chi tiết (các đợt sửa, con số, cách sửa sổ): sổ ghi việc [02_BAO_CAO_KHO_DU_LIEU.md](../02_BAO_CAO_KHO_DU_LIEU.md).*
