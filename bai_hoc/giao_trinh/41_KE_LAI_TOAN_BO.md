# Bài 41 — Kể lại toàn bộ trong một phút, trong năm phút, và kịch bản chạy thử

*Cập nhật 14:49, ngày 22/11/2026 · mọi con số chép từ bài gốc của nó, ghi "bài N" ngay cạnh, hoặc từ cấu hình và sổ việc lúc 14:48 22/11; kịch bản chạy thử lấy từ kịch bản 10 bước nhóm đã chạy lặp ngày 21–22/11 và từ lượt kiểm chốt trưa 22/11 (Claude Sonnet 5.5); đã sửa theo một lượt đối chiếu độc lập; người viết không chạy lại lượt nào.*

**Bài trước đã biết:** hệ thống làm được tới đâu, còn yếu ở đâu (bài 40).
**Bài này thêm:** bốn thứ để dùng ngay: một bản kể một phút, một bản kể năm phút, một kịch bản chạy thử từng bước, và mười câu hỏi hay gặp kèm câu trả lời ngắn.

## 1. Kể trong một phút

hue_rag là một ứng dụng web giúp du khách và người dân hỏi về văn hoá, du lịch Huế. Nó chỉ trả lời từ một kho 266 bài viết đã soạn sẵn, cắt thành 9.458 đoạn (bài 7). Khi có câu hỏi, chương trình lấy 30 đoạn gần nghĩa nhất, chấm lại theo từ khoá, giữ 10 đoạn (bài 13). Model đọc 10 đoạn đó rồi viết câu trả lời, mỗi ý ghi số nguồn; chương trình kiểm lại rằng mọi số nguồn đều có thật (bài 16). Kho không có thì hệ thống từ chối bằng một câu cố định, rồi tra web một lần, để ở mục riêng ghi "chưa kiểm" (bài 25). Ngày âm lịch, khoảng cách, xếp lịch thì chương trình tính; model chỉ diễn đạt (bài 3). Người dùng còn lên được một lịch nhiều ngày bằng vài nút bấm, rồi sửa lịch bằng lời (bài 27, 31). Thay đổi được đo theo điều kiện ghi trước, trên bộ 176 câu mẫu và các thước nhiều lượt (bài 17, 20, 32). Hệ thống chạy trên máy, model viết là Claude Sonnet 5.5, chưa đưa lên mạng.

## 2. Kể trong năm phút

**Bài toán.** Người dùng là du khách và người dân Huế, gõ tiếng Việt có dấu. Họ cần ba việc: hỏi đáp có nguồn, vài việc cần tính, và một lịch tham quan. Luật gốc là chỉ trả lời từ kho; kho không có thì nói không có. Thứ tự lỗi do chủ dự án đặt: nặng nhất là sai một cảnh báo an toàn, nhẹ nhất là từ chối nhầm (bài 4).

**Chuẩn bị kho, làm một lần.** Kho là 266 bài tiếng Việt về món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch (bài 7). Chương trình cắt bài theo cấu trúc: mỗi đoạn văn, mỗi mục danh sách, mỗi bảng ngắn là một đoạn, bảng dài thì tách từng dòng; được 9.458 đoạn (bài 8). Mỗi đoạn mang tên bài và tên mục của nó (bài 9), được đổi thành một dãy 384 con số bằng một model embedding nhỏ chạy ngay trên máy (bài 10), rồi cất vào Qdrant (bài 12).

**Một câu hỏi đi qua sáu bước.** Lấy câu "Giá vé tham quan Đại Nội Huế là bao nhiêu?". Một lần gọi model ngắn xếp câu vào một trong bốn tuyến; câu này là "về Huế" (bài 22). Cùng lúc, chương trình lấy 30 ứng viên gần nghĩa nhất, chấm lại 30 ứng viên đó theo từ khoá, trộn hai bảng xếp hạng và giữ 10 đoạn (bài 13). Model viết đọc lời dặn, câu hỏi và 10 đoạn đánh số, rồi viết câu trả lời có số nguồn (bài 15). Chữ hiện trước, kiểm sau: chương trình kiểm ba luật về số nguồn, hỏng thì rút câu trả lời lại (bài 16). Cả lượt mất 3,7 giây, trong đó model viết 3,6 giây; bước tìm chỉ khoảng 0,04 giây (bài 6).

**Khi kho không có.** Với câu "Chùa Thiên Mụ có chỗ đậu ô tô không?", model trả đúng câu từ chối cố định. Chương trình nhận ra, tra web một lần, viết một mục riêng "Từ web (chưa kiểm)" chỉ từ các đoạn trích tìm được, và kiểm con số trong đó (bài 25). Kho luôn thắng: câu đã trả lời được từ kho thì không tra web.

**Trợ lý.** Tìm một lần có khi chưa đủ. Model được xin tìm thêm, từ chiều 22/11 tối đa 3 lần (bài 21 kể theo trần cũ là 2); số vòng gọi model có trần, cả phần viết có hạn 45 giây (bài 21). Máy chủ nhớ 3 lượt gần nhất trong 30 phút, nên hiểu được "vé vào đó bao nhiêu" (bài 23). Câu có ngày, thời tiết, khoảng cách thì chương trình tính, dựng thành một nguồn có số riêng cho model trích (bài 24). Model chỉ xin; chương trình mới là thứ chạy (bài 3).

**Lên kế hoạch.** Người dùng chọn số ngày, người đi cùng, sở thích bằng nút. Chương trình xếp lịch từ một bảng 41 điểm tham quan, theo luật có thứ tự ưu tiên: an toàn, giờ mở cửa, gom điểm gần nhau, sở thích (bài 27, 28). Một bước kiểm viết riêng đối chiếu lịch với 23 luật (bài 29). Model chỉ viết câu mô tả mỗi điểm. Ở ví dụ 3 ngày, 2 người lớn, thích di tích, chương trình xếp 11 điểm; khung lịch hiện sau 0,2 giây, đủ câu mô tả sau 9,3 giây (bài 27). Muốn sửa thì nhắn "bỏ lăng Tự Đức": model chỉ trả một danh sách lệnh, chương trình áp và kiểm; bộ 10 chuỗi sửa lịch đạt 9 trên 10, đo trước khi đổi sang Claude (bài 31).

**Đo.** Đề chính là 176 câu hỏi mẫu kèm đáp án, chia 120 câu để thử và 56 câu để kiểm lại (bài 17). Bước tìm và câu trả lời được chấm riêng (bài 18, 19). Người chấm là một model, chấm mù, ba thang điểm; hai bản được so theo cặp kèm khoảng tin cậy, và phải thắng vượt mức nhiễu (bài 19). Mỗi thay đổi là một thí nghiệm có điều kiện ghi trước; hơn một nửa số lần thử kết thúc bằng "bỏ" (bài 20). Phần trợ lý nhiều lượt đo bằng 12 vai người dùng mô phỏng: 7 · 7 · 8 trên 12 phiên đạt với Claude ngày 21/11; đo lại ngày 22/11 ra 8 trên 12, vẫn trong khoảng nhiễu (bài 32, 40).

**Giới hạn.** Bước kiểm mới kiểm số nguồn có thật, chưa kiểm nghĩa (bài 16). Kho là trần: ở lượt mốc, phần lớn ý bị trượt là thứ kho chưa có (bài 40). Tin dài chờ khoảng 13 giây, tin ngắn lúc máy rảnh khoảng 7 giây; chữ tới một lần (bài 34). Chưa có người dùng thật, chưa đưa lên mạng (bài 36).

**Cách làm.** Chủ dự án quyết mục tiêu, kho, tiền, model; nhiều phiên coding agent viết, đo, kiểm chéo nhau; người viết không tự duyệt (bài 39).

## 3. Kịch bản chạy thử

Các bước 2–4, 6–8, 12–15 là kịch bản 10 bước nhóm đã chạy lặp qua đường gọi thật, cùng câu gõ: 0 trên 10 lần hỏng ở cả hai model ngày 21/11, và ba lần chạy lại sau các đợt đưa thay đổi vào bản chính không bước nào hỏng (bài 32). Các bước còn lại không nằm trong lượt chạy lặp đó: bước 5 là lượt thật ngày 20–21/11; bước 9 là loại bước đã đạt trên trình duyệt trưa 22/11 với một câu khác; bước 10 đã thấy thật ngày 20/11 với model cũ; phần ảnh ở bước 16 chưa chạy trên model đang chạy.

**Trước khi bắt đầu.**
- Docker Desktop đang chạy.
- Trình duyệt chỉ mở ứng dụng ở **một tab**.
- Không khởi động lại máy chủ giữa chừng.
- Không tải lại trang giữa chừng: mỗi lần tải trang là một cuộc trò chuyện mới, lịch đang có mất mà màn hình không báo. Sang trang khác thì bấm menu trong cùng tab.
- Bấm "Cuộc trò chuyện mới" trước bước 12, để phần lịch chạy trong một cuộc riêng như lượt đã chạy lặp.
- Nếu máy chủ đã chạy sẵn từ một lần thử trước, câu ở bước 2 có thể về ngay từ bộ nhớ câu trả lời, không có dòng "Đã tìm trong kho…".

| Bước | Làm gì | Sẽ thấy gì | Bước này cho thấy điều gì của hệ thống |
|---|---|---|---|
| 1 | Ở thư mục dự án, gõ `scripts/bat_he_thong.sh` (bài 36) | "SẴN SÀNG — mở http://127.0.0.1:8010 …"; từ lúc Qdrant tắt mất khoảng 34 giây (bài 36). Máy chủ đã chạy sẵn thì in "SẴN SÀNG (server đã chạy sẵn) — mở …" | lệnh kiểm từng điều kiện theo thứ tự rồi mới bật máy chủ; thiếu gì thì in đúng một dòng "CHƯA BẬT ĐƯỢC — …" |
| 2 | Mở địa chỉ đó. Vào Trợ lý Huế, gõ *"Lăng Tự Đức có gì đặc biệt?"* | dòng "Đã tìm trong kho, đang chuẩn bị câu trả lời…", rồi câu trả lời có số [n], dòng "Nguồn:" bấm xem được đoạn gốc | đường đi chính: tìm 10 đoạn, model viết, chương trình kiểm số nguồn (bài 13–16) |
| 3 | Gõ tiếp *"Vé vào đó bao nhiêu tiền?"* | giá vé lăng Tự Đức, kèm nguồn | máy chủ nhớ lượt trước; model tự viết câu tìm có tên lăng (bài 23) |
| 4 | *"Ở Hội An có quán cao lầu nào ngon?"* | "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế. Bạn muốn hỏi gì về Huế không?" | bước xếp loại câu; câu ngoài phạm vi không được trả lời bằng kho (bài 22) |
| 5 | *"Chùa Thiên Mụ có chỗ đậu ô tô không?"* | "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)." và mục "Từ web (chưa kiểm)". Dịch vụ tìm web lỗi thì thấy câu từ chối gốc "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." và dòng "Mình chưa tra được web lúc này." | kho không có thì từ chối, không đoán; tra web một lần, để riêng (bài 16, 25) |
| 6 | *"Cuối tuần này Huế có mưa không?"* | con số dự báo, kèm nguồn do chương trình dựng | việc cần dữ liệu hôm nay do chương trình lấy; model không tự nghĩ ra số (bài 24) |
| 7 | *"Từ Đại Nội đến lăng Khải Định bao xa, đi mất bao lâu?"* | một số ki-lô-mét và một số phút | khoảng cách tra từ bảng dựng sẵn, không gọi mạng lúc trả lời (bài 24) |
| 8 | *"Đặt giúp mình một phòng khách sạn gần Đại Nội tối mai"* | câu nói thật là không đặt được; có thể kèm vài thẻ khách sạn ghi "Theo danh mục, chưa kiểm giá / phòng trống." | hệ thống không làm thay; không bao giờ nói "đã đặt" (bài 4) |
| 9 | Một câu có chữ "bão", ví dụ *"Ngày mai Huế có bão không?"* | dưới câu trả lời: dòng "Dự báo dưới đây chỉ có nhiệt độ và mưa, không có thông tin bão hay áp thấp.", bảng mưa, rồi câu cố định "Với bão, lũ, ngập: hãy theo dõi bản tin chính thức … khi gặp nguy hiểm gọi 112." | câu bão, lũ: model không nhận con số nào, chương trình nối khối chỉ dẫn cố định (bài 24) — loại lỗi nặng nhất của bài 4 |
| 10 | (tuỳ chọn) Bấm "Cuộc trò chuyện mới", gõ lại **đúng từng chữ** câu ở bước 2, kể cả dấu "?" | câu trả lời về gần như ngay, không có dòng "Đã tìm trong kho…" | bộ nhớ câu trả lời 24 giờ: khoảng 0,1 giây, không gọi model (bài 34). Chỉ trúng khi câu ở bước 2 là câu đầu của cuộc lúc đó, lượt đó chỉ dùng công cụ tìm kho, và máy chủ chưa khởi động lại. Đọc từ chương trình; mới thấy thật ngày 20/11 với model cũ |
| 11 | Bấm "Cuộc trò chuyện mới" | khung trò chuyện trống | phần lịch chạy trong một cuộc riêng |
| 12 | Trang Lên kế hoạch, kéo xuống khung "Ví dụ", bấm "Xếp lịch như ví dụ" (2 ngày · 2 người lớn · cân bằng · thích di tích · chỗ ở 2–3 sao) | khung lịch hiện gần như ngay; câu mô tả từng điểm tới sau vài giây | chương trình xếp lịch, model chỉ viết câu mô tả; lịch phải qua bước kiểm 23 luật (bài 27–29) |
| 13 | Bấm nút **Trợ lý Huế**, gõ *"Bỏ <tên điểm tham quan đầu tiên của ngày 2> khỏi lịch"* | thẻ lịch đổi; dòng báo "Đã bỏ …" ở đầu thẻ, thường kèm "thêm … vào chỗ trống" | model hiểu ý thành lệnh; chương trình áp, kiểm, tự viết câu báo, và lấp chỗ trống bằng bộ xếp (bài 31) |
| 14 | *"Ngày 1 đi hết mấy tiếng, có kịp về trước 5 giờ chiều không?"* | số giờ của ngày 1, đúng số chương trình tính | đã có lịch thì câu hỏi được trả lời trên đúng lịch đó (bài 27) |
| 15 | Bấm "Tải PowerPoint" | file mở được, không còn điểm đã bỏ | file dựng ở máy chủ từ lịch đã lưu của cuộc trò chuyện (bài 30) |
| 16 | (tuỳ chọn) trang Bản đồ; gửi một ảnh ở khung Trợ lý | các điểm trên bản đồ; với ảnh, dòng "Mình đoán trong ảnh là … — có thể sai." hoặc thẻ chọn tên (phần ảnh chưa chạy trên model đang chạy) | bản đồ lấy toạ độ từ bảng; ảnh chỉ để đoán tên trong 42 tên, người trả lời không nhìn ảnh (bài 26, 30) |

**Điều đã thấy ở các lần chạy lặp.** Với model đang chạy, chữ đứng im khoảng 10 giây rồi hiện một lần (bài 33, 34). Ở bước 8, Claude thường tự viết lời từ chối riêng, nên chỉ 1 trên 10 lần có link sang trang Chỗ ở (bài 32).

**Lượt kiểm chốt trưa 22/11** (phiên điều phối báo trưa 22/11): 41 tin gõ qua trình duyệt, cả câu trung vị 6,9 giây, 95 % số lượt dưới 13,1 giây, 0 màn hình lỗi; lệnh bật chạy từ lúc Qdrant tắt, 34 giây ra "SẴN SÀNG" (bài 34, 36).

**Khi một bước hỏng.** Ba dòng có chữ **(đã thử)** là ba trong bốn ca hỏng đã thử thật trưa 22/11; ca thứ tư (bật máy chủ lúc Qdrant tắt) ở câu cuối dòng Qdrant (bài 6).

| Thấy gì | Vì sao | Làm gì |
|---|---|---|
| lệnh bật in "CHƯA BẬT ĐƯỢC — …" | thiếu một điều kiện (Docker, file khoá, chỉ mục); hệ thống kiểm đủ điều kiện trước khi nhận câu hỏi (bài 36) | làm đúng điều dòng đó nói, rồi chạy lại lệnh |
| mọi câu ra "Không thể tạo câu trả lời vào lúc này." **(đã thử: máy chủ bật lúc thiếu đường tới file khoá)** | model viết không gọi được. Máy chủ không tự gọi lại, không có model dự phòng (bài 6) | thiếu đường tới file khoá lúc bật: bấm "Thử lại" không hết; tắt máy chủ (Ctrl+C) rồi chạy lại lệnh bật, lệnh này chặn ca đó trước khi bật. Khoá hết hạn: thay file khoá rồi bấm "Thử lại" (đọc từ chương trình, chưa thử). Hãng lỗi: chờ rồi bấm "Thử lại" |
| "Hệ thống tra cứu tạm thời không khả dụng." **(đã thử)** | Qdrant ngừng; khối chính hỏng thì dừng và nói thật (bài 6) | bật lại Qdrant; hỏi được ngay (2,9 giây ở lượt thử). Nếu Qdrant tắt từ lúc bật máy chủ thì phải khởi động lại máy chủ (bài 6) |
| "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" | chữ hiện trước, kiểm sau; số nguồn sai thì cả câu bị rút (bài 16). Từng hay gặp ở tin dài 4–5 ý; chiều 22/11 có bốn thay đổi ở khâu tìm cho loại tin này (bài 40) | bấm "Thử lại" |
| thẻ lịch còn, nhưng lệnh sửa lịch bị trả lời như câu hỏi thường **(đã thử)** | máy chủ đã khởi động lại giữa cuộc; lịch chỉ nằm trong bộ nhớ của máy chủ, chưa có cách giữ qua lần khởi động (bài 6) | tải lại trang, lập lịch lại |
| cuộc trò chuyện và lịch ở tab thứ nhất biến mất, không báo (phiên điều phối báo trưa 22/11) | hai tab của cùng trình duyệt dùng chung một mã cuộc trò chuyện, nên cuộc mới của tab sau thay luôn cuộc của tab trước; cách sửa là mỗi tab một mã cuộc, chưa làm (bài 35) | đóng tab thừa, làm lại trong một tab |

## 4. Mười câu hỏi hay gặp

| # | Câu hỏi | Trả lời ngắn | Bài |
|---|---|---|---|
| 1 | Vì sao không cho model trả lời bằng hiểu biết của nó? | Đó là luật gốc chủ dự án đặt; câu trả lời từ kho thì có nguồn để người dùng tự xem lại. Cái giá là từ chối nhầm: 3 trên 158 câu kho có ở lượt đo 12/11 với gpt-6-luna. | 4 |
| 2 | Vì sao tìm bằng hai cách, và vì sao 10 đoạn? | Cách "tìm theo nghĩa rồi chấm lại theo từ khoá" là cách mốc chủ dự án chốt ngày 11/09; các lần so cuối tháng 10 không cách nào hơn nên giữ. Đưa 10 đoạn thay vì 5 là lần thắng duy nhất của đợt rà cuối tháng 10; 15 đoạn, cả mục, cả bài đều không khá hơn. | 11, 13 |
| 3 | Vì sao không có bước xếp lại bằng model? | Đã thử ba cách, không cách nào qua điều kiện ghi trước. Cách tốt nhất làm bước tìm tốt hơn hẳn nhưng 5 câu tệ đi, quá mức cho phép 4. | 14 |
| 4 | Làm sao biết câu trả lời không bịa nguồn? | Chương trình kiểm ba luật: có ít nhất một số nguồn, mọi số là số của một nguồn đã thật sự đưa cho model, câu từ chối không kèm số. Phạm luật thì rút cả câu. Nó chưa kiểm đoạn đó có nói đúng ý không. | 16 |
| 5 | Vì sao chương trình xếp lịch, model chỉ viết câu mô tả? | Giờ, thời lượng, thứ tự phải luôn đúng và lặp lại được; cùng tám giá trị luôn ra cùng một lịch. Xếp lịch từ câu gõ tự do để model làm nhiều hơn đã thử hai lần, chưa đạt. | 3, 28 |
| 6 | Làm sao biết một thay đổi làm hệ thống tốt hơn? | Ghi điều kiện trước, đổi một thứ, so theo cặp trên cùng câu hỏi với bản đang chạy; phải thắng vượt mức nhiễu. Vỡ một điều kiện như "0 câu ngoài kho được trả lời" thì mặc định bỏ; vài ngoại lệ đều ghi lý do và có người kiểm đồng ý. | 19, 20 |
| 7 | Đổi model viết thì sao? | Giữa hai model đã dùng, đổi là sửa một dòng cấu hình rồi khởi động lại; hiện chưa về được gpt-6-luna vì tài khoản OpenAI đang ngừng. Hãng mới thì phải viết thêm một lớp nối. Kiến thức nằm ở kho nên không mất; lời dặn và các ngưỡng phải đo lại. | 2, 33 |
| 8 | Vì sao trả lời chậm? | Gần như toàn bộ thời gian là model viết: lần viết cuối chiếm 72 % lượt đứng giữa. Hai cách lợi lớn (chữ chạy dần, câu ngắn hơn) đều là thứ chủ dự án đã quyết; hạ mức suy luận chỉ mua khoảng 0,3 giây. | 34 |
| 9 | Một khối hỏng thì sao? | Khối chính (model viết, Qdrant, chỉ mục) hỏng thì dừng và nói thật, có nút "Thử lại". Khối phụ (thời tiết, tìm web, xếp loại câu) hỏng thì bỏ phần đó, trả lời tiếp. | 6 |
| 10 | Dữ liệu người dùng đi đâu? | Chữ người dùng không ghi xuống đĩa; nó tới hãng model, và tới dịch vụ tìm web khi kho từ chối. Máy chủ giữ trong bộ nhớ tối đa 30 phút (cuộc trò chuyện) hoặc 24 giờ (câu trả lời đã nhớ); sổ số đo chỉ có số. | 37 |

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- **Mọi con số của phần 1, 2, 4** chép từ "Ý chính", "Quyết định và lý do" hoặc "Chi tiết để tra" của bài ghi cạnh số; bảng đối chiếu từng số ở báo cáo của người viết (`data/hoc_cung_D/viet/viet_39_41.md` [riêng tư]). Ví dụ chính (3,7 giây, model viết 3,6 giây, tìm 0,04 giây): bài 6. Ví dụ "kho không có": bài 16 và mục lục giáo trình. Ví dụ lập lịch 3 ngày, 11 điểm, 0,2 / 9,3 giây: bài 27 "Chi tiết để tra" và mục lục giáo trình. 9 / 10 chuỗi sửa lịch đo 14–19/11, trước khi đổi sang Claude: bài 31 mục "Đã so".
- Trần tìm thêm 3 lần từ 14:33 22/11 (trước là 2): `backend/config/settings.yaml` dòng `so_lan_tim_kho` (chú thích "2 ⇒ 3 lúc 14:33 22/11/2026") và `so_vong_cong_cu` (4 ⇒ 5) [code, đọc 14:48 22/11]. Bài 21 còn viết theo con số cũ.
- 12 vai đo lại 22/11: 8 / 12, trong khoảng nhiễu: `session_prompt/VIEC_DANG_MO.md` hàng X3 (14:13 22/11) [phiên đo, một lượt]. 13 giây (49 lượt chạy một mình, tin dài hơn) và 6,9 giây (41 tin phần lớn ngắn, máy rảnh): bài 34 dòng 29 và "Chi tiết để tra".
- **Kịch bản 10 bước** (câu gõ của bước 2, 3, 4, 6, 7, 8, 13, 14; nút ví dụ ở bước 12; tải PowerPoint ở bước 15): `data/thu_bedrock_2026-11-21/do/demo/chay_demo.py` danh sách `BUOC` [riêng tư; code đo đã chạy, người viết chỉ đọc]. Câu ở bước 14 chép đúng câu của kịch bản. Kịch bản chạy trong tiến trình qua đường gửi dần như trình duyệt, tắt bộ nhớ câu trả lời, mở cuộc mới khi chuyển sang phần lịch (dòng 140, 158–159) — vì vậy bước 11 là bắt buộc. 0 / 10 lần hỏng, ba lần chạy lại 0 bước hỏng, 1 / 10 link trang Chỗ ở: bài 32 dòng 14, 189.
- Ở các lượt chạy lặp, điểm đầu tiên của ngày 2 là lăng Tự Đức (`do/demo/KET_QUA_DEMO.md`) [riêng tư]; bài để dạng "<tên điểm…>" vì lịch có thể khác. Giá vé lăng Tự Đức trong kho: dò bằng `scripts/grep_kb.sh 'Tự Đức'` ngày 22/11 [đã chạy].
- Bước 9 (câu bão): câu ví dụ người viết đặt theo cơ chế của bài 24 (câu có từ nguy hiểm thời tiết ⇒ model không nhận số, chương trình nối khối cố định); lời nguyên văn: `backend/llm/thoi_tiet.py` (`CAU_BAO_LU`) và bài 24 mục "Câu bão, lũ có thêm một lớp" [code]. "Loại bước đã đạt trên trình duyệt trưa 22/11": danh sách tự thử của chủ dự án `data/test_cuoi/DANH_SACH.md` [riêng tư; phiên điều phối và biên bản kiểm báo, người viết không mở].
- Bước 10 (bộ nhớ câu trả lời): điều kiện trúng đọc ở `backend/api/cache_tra_loi.py`, `backend/api/routes/chat.py`, `frontend/src/chat.jsx` (nút "Cuộc trò chuyện mới" gọi cuộc mới) theo biên bản kiểm [suy từ code, chưa thử]; lần thấy thật 20/11 với gpt-6-luna (7,5 ⇒ 0,11 giây): phụ lục B dòng `cache_cau_tra_loi`.
- Nhãn nút và lời báo nguyên văn: "Xếp lịch như ví dụ" và chuỗi tóm tắt `frontend/src/LenKeHoach.jsx` dòng 109; "Tải PowerPoint" `frontend/src/LichV2.jsx` dòng 358; "Cuộc trò chuyện mới", "Thử lại" `frontend/src/chat.jsx` dòng 384, 421; "Đã tìm trong kho, đang chuẩn bị câu trả lời…" `chat.jsx` dòng 23; "Theo danh mục, chưa kiểm giá / phòng trống." `chat.jsx` dòng 631; câu ngoài phạm vi `backend/llm/full_corpus_prompt.py` dòng 63; câu từ chối gốc cùng file dòng 8; "Đã bỏ …" và "… vào chỗ trống." theo `backend/tests/test_sua_lich_v2.py` dòng 39–40; "SẴN SÀNG — mở …", "SẴN SÀNG (server đã chạy sẵn)", "CHƯA BẬT ĐƯỢC — " `scripts/bat_he_thong.sh` dòng 24, 56, 71; câu dẫn sang mục web: bài 16 dòng 64; "Mình chưa tra được web lúc này.": bài 6; "Mình đoán trong ảnh là … — có thể sai.": bài 26; ba lời báo lỗi: bài 6 [code].
- Lượt kiểm chốt trưa 22/11 (41 tin, 6,9 giây, 13,1 giây, 0 màn hình lỗi; 34 giây; tab thứ hai xoá cuộc và lịch; "mỗi tab một mã cuộc — chưa làm"): phiên điều phối báo trưa 22/11; chép ở `bai_hoc/VIEC_MOI_XONG.md` mục 40, 41 và `session_prompt/VIEC_DANG_MO.md` hàng X2 [máy kiểm, phiên đo, một lần]. Tải lại trang là cuộc mới, lịch mất không báo: `frontend/src/chat.jsx` dòng 212 và danh sách tự thử [riêng tư].
- Bốn ca hỏng đã thử (2,9 giây): bài 6. Cách xử ca thiếu khoá lúc bật (tắt máy chủ, bật lại bằng lệnh bật): `scripts/bat_he_thong.sh` dòng 33–37 và danh sách tự thử; khoá hết hạn đọc lại ở mỗi lần gọi: `backend/llm/bedrock_model.py` [đọc code, chưa thử].
- Bốn thay đổi khâu tìm chiều 22/11: bài 40 và `settings.yaml` (`tim_ve_bo_cut`, `tach_cau_tim_model`, `het_luot_viet_lai`, `so_lan_tim_kho`) [code].
- FAQ 2: cách mốc 11/09, các lần so cuối tháng 10: bài 11 quyết định 1; 10 đoạn: bài 13 quyết định 4. FAQ 6 ngoại lệ: bài 20 quyết định 4. FAQ 7: bài 33 "Ý chính" và "Giới hạn đã biết".
- Lệnh bật nằm trong thân bài vì đây là thứ người chạy thử phải gõ; các bài khác chỉ ghi nó ở khối Nguồn (bài 36).
- Bài đã qua một lượt đối chiếu độc lập (14:43 22/11/2026): `data/hoc_cung_D/kiem/bai_39_41.md` [riêng tư]; các dòng đã áp và không áp ghi ở báo cáo của người viết.

</details>
