# 00 — Cả hệ thống trong 3 phút

*Bài để hiểu, viết 11/11/2026. Đọc khoảng 3 phút.*

## Một người hướng dẫn viên cẩn thận

Hình dung bạn đi Huế với một người hướng dẫn viên. Người này không giỏi nhớ, nhưng rất cẩn thận và luôn mang theo một cuốn sổ tay du lịch do chính họ soạn.
Bạn hỏi: *"Chùa Thiên Mụ mở cửa mấy giờ?"*. Họ không trả lời theo trí nhớ. Họ lật sổ tay, tìm vài trang nói về chùa Thiên Mụ, đọc rồi mới trả lời bạn, kèm
câu "mình đọc ở trang này". Nếu sổ không có, họ nói thẳng: "Sổ của mình không có thông tin này". Họ không đoán.

Chatbot Huế làm đúng như người hướng dẫn viên đó. Nó có ba phần:

1. **Cuốn sổ tay** gồm 204 bài viết về món ăn, di tích, lễ hội, nghệ thuật biểu diễn và du lịch Huế. Đây là tất cả những gì chatbot "biết".
2. **Người tìm trang**: khi có câu hỏi, máy tìm trong sổ khoảng 10 mẩu nói đúng chuyện được hỏi.
3. **Người viết** là một mô hình ngôn ngữ của OpenAI, loại máy đọc hiểu và viết được tiếng Việt như người (tên chung là LLM). Nó đọc 10 mẩu đó rồi viết câu
   trả lời. Ý nào lấy từ đâu thì ghi nguồn bên dưới, để người dùng bấm vào đọc lại bài gốc.

## Vì sao không hỏi thẳng ChatGPT cho nhanh?

ChatGPT trả lời bằng trí nhớ. Trí nhớ đó rộng nhưng có thể đã cũ, và khi không biết, nó vẫn hay nói rất chắc. Với khách du lịch, nói chắc mà sai giờ mở
cửa hay giá vé còn tệ hơn là không nói. Cách "tra sổ rồi mới viết" đổi lại ba điều: câu nào cũng có nguồn để kiểm, sổ không có thì chatbot nói không có, và
muốn sửa thông tin sai thì chỉ cần sửa sổ, không phải dạy lại model. Kiểu làm này có tên là **RAG** (viết tắt tiếng Anh của "tạo câu trả lời có tra cứu").
Tên đề tài của bạn cũng nói đúng điều này.

## Hai việc người hướng dẫn làm thêm

- **Nghe xem khách hỏi chuyện gì trước khi lật sổ.** Câu chào hỏi thì đáp luôn. Câu không liên quan tới Huế, ví dụ giá vàng hôm nay, thì lịch sự từ chối. Chỉ
  câu về Huế mới đi tra sổ. Việc xếp loại này cũng do model làm, bằng một lần hỏi rất ngắn.
- **Việc dễ nhầm thì để máy tính làm.** Hôm nay là ngày mấy âm lịch, cuối tuần này là ngày nào, dự báo thời tiết bao nhiêu độ: những thứ này **code** tính
  hoặc lấy về, model chỉ chép lại cho thành câu. Lý do là model hay tính nhầm ngày và hay tự thêm con số, dù đã được dặn đừng làm vậy.

Khi chatbot vừa tra sổ vừa biết tự nhờ máy tính những việc như vậy, ta gọi nó là **trợ lý** chứ không chỉ là máy hỏi đáp. Đây là phần việc đang làm bây giờ.

## Tốt tới đâu

- **Ít nói sai.** Trong lần chấm đầy đủ gần nhất (01/11, trên khoảng 130 câu hỏi mẫu có đáp án), điểm "đúng" trung bình là 4,7 trên 5. Nói cách khác, gần như
  không câu nào nói ngược với đáp án.
- **Không bịa câu ngoài sổ.** Với những câu sổ không có, chưa lần đo nào chatbot tự trả lời từ sổ.
- **Đủ nhanh.** Chữ đầu tiên hiện trên màn hình sau khoảng 2 giây với câu thường gặp. Yêu cầu bạn đặt là dưới 3 giây.

## Khi nào hỏng

- **Sổ có mà tìm không ra trang.** Đây là lỗi hay gặp nhất. Mẩu có đáp án nằm trong sổ nhưng không lọt vào 10 mẩu được đưa cho người viết, nên chatbot nói
  "không đủ thông tin" dù sổ có. Lần đo gần nhất có khoảng 4–6 trên 158 câu bị như vậy.
- **Sổ cũ.** Giá vé, giờ mở cửa có thể đổi mà sổ chưa kịp sửa. Vì vậy câu trả lời về vé, điểm tham quan và lễ hội có kèm dòng "thông tin có thể đã thay đổi".
- **Có nguồn chưa có nghĩa là đã kiểm từng chữ.** Máy chỉ kiểm được rằng nguồn được ghi là có thật, chưa kiểm được câu viết ra có khớp đúng từng chữ với nguồn
  hay không.

## Các bài tiếp theo (đi theo đường đi của một câu hỏi)

01 Cuốn sổ tay: kho dữ liệu · 02 Cắt sổ thành mẩu nhỏ *(sắp viết)* · 03 Tìm mẩu nào hợp câu hỏi *(sắp viết)* · 04 Viết câu trả lời có nguồn *(sắp viết)* ·
05 Trợ lý: xếp loại câu và nhờ máy tính *(sắp viết)* · 06 Làm sao biết chatbot tốt tới đâu *(sắp viết)*

## Ba điều chính

1. Chatbot giống một người hướng dẫn viên cẩn thận: **tra sổ tay rồi mới trả lời**, ghi rõ đọc ở đâu, và sổ không có thì nói không có.
2. Cách này được chọn vì với khách du lịch, **nói chắc mà sai còn tệ hơn không nói**. Tra sổ thì câu nào cũng kiểm được, và sửa sổ là sửa được câu trả lời.
3. Chỗ yếu nhất hiện nay không nằm ở người viết, mà ở **bước tìm trang**: đôi khi sổ có đáp án mà máy tìm không ra.
