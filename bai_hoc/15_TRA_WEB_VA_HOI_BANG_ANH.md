# Bài 15 — Khi sổ không có: tra web, và hỏi bằng ảnh

*Cập nhật lần cuối: 21:34, ngày 15/11/2026 · phần hỏi bằng ảnh viết lại theo luồng mới tối 15/11 (ảnh đính kèm câu hỏi; nhận ra một tên thì trả lời luôn, phân vân thì hỏi chọn). Trước: 18:24, ngày 15/11/2026 · thêm chuyện thật thứ ba: câu hỏi nối tiếp ra web bằng câu cụt (bật 15/11). Trước: 20:37, ngày 13/11/2026 · sửa theo kiểm độc lập; thêm chuyện thật thứ hai: thử Exa cho tra web rồi giữ Serper; ghi ngày cho số tốc độ mục web (ghi ở Nguồn).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Tra web | **`tra_web`** (dịch vụ **Serper**, tìm Google) | Khi kho không có, code tìm web **một lần** rồi model viết một mục riêng (đã gặp ở bài 12). |
| Cổng web — **mới** | **`web_gate_open`** | Điều kiện để được tra web: câu về Huế, kho đã trả câu từ chối, không lỗi gì khác. |
| Mục web | **"Từ web (chưa kiểm)"** | Phần trả lời từ web, tách riêng khỏi phần trả lời từ kho. |
| Sổ link — **mới** | mã **`[w n]`** | Mỗi kết quả web có một số; model chỉ được trích các số có trong sổ. |
| Hỏi bằng ảnh | **`nhan_anh`** (cờ `anh.bat: true`) | Người dùng gửi ảnh kèm câu hỏi; model đoán tối đa 3 tên trong một danh sách 42 mục; ra đúng một tên thì trợ lý trả lời luôn từ kho, ra 2–3 tên thì hỏi người dùng chọn (đã gặp ở bài 12). |
| Rào chắn | **guardrail** | Chỗ code chặn trước khi chữ tới người dùng. |
| Câu hỏi nối tiếp — **mới** | cờ **`web_cau_noi_tiep`** (bật 15/11) | Câu hỏi sau không nhắc lại tên nơi / món của câu trước ("mở cửa lúc mấy giờ"). Ở lượt này câu tra web lấy từ câu tìm trong sổ mà model vừa viết. |
| Exa | dịch vụ tìm web **Exa** (`highlights`) | Một dịch vụ tìm web khác, trả **đoạn trích nguyên văn trong trang**, chọn theo câu hỏi. Đã thử 12/11, không dùng. |

---

*Bài 14 kể những việc dễ nhầm do code làm. Bài này kể hai đường mở rộng ra ngoài cuốn sổ: **tra web** khi kho không có, và **hỏi bằng ảnh** khi người dùng không
biết tên thứ mình đang nhìn. Cả hai đều chạm vào luật chính "chỉ nói điều kho có", nên phải có rào chắn rõ.*

## Quay lại người hướng dẫn viên

Khách hỏi một chuyện cuốn sổ không có: *"Khách sạn nào gần cầu Trường Tiền?"*. Người hướng dẫn viên cẩn thận trả lời theo hai bước:
1. **nói thật**: "sổ của mình không có thông tin này";
2. rồi **mở điện thoại tra giúp**, nhưng nói rõ: "đây là mình vừa tra trên mạng, **chưa kiểm**, anh xem kỹ lại nhé". Họ không đọc lại link lạ, không đọc giá
   tiền không thấy trên trang, và với chuyện bão lũ thì chỉ khách tới nguồn chính thức.

Khách đưa điện thoại có một tấm ảnh: *"Đây là chỗ nào vậy?"*. Họ nhìn ảnh. Nhận ra **một nơi** thì mở sổ kể luôn, nhưng mở đầu bằng câu "mình đoán đây
là chỗ này, có thể sai". Còn **phân vân giữa vài nơi** thì hỏi lại: "là chỗ này hay chỗ kia?", khách chọn rồi họ mới kể. Lúc nào họ cũng kể từ sổ, không kể theo
trí nhớ về tấm ảnh.

## Tra web: chỉ khi kho không có, và tách riêng

**Khi nào được tra.** Cổng web chỉ mở khi đủ mọi điều kiện:
- câu được xếp loại **về Huế**;
- phần trả lời từ kho đã ra **đúng câu từ chối cố định** (bài 8);
- không có lỗi ghi nguồn, lỗi công cụ, không có lịch trình, và chưa tra lần nào;
- cờ `tra_web` đang bật.

Kho trả lời được thì **không tra**. Câu ngoài chủ đề thì **không tra**. Phần chạy song song lúc xếp loại (bài 12) cũng không được tra.

**Code làm gì:**
- **Dựng câu tìm**: từ câu hỏi, bỏ số điện thoại và email nếu có, cắt còn tối đa 120 ký tự, thêm chữ "Huế". Chỉ câu tìm này được gửi ra Serper.
  Từ 15/11, ở **lượt hỏi tiếp** câu tìm được dựng từ câu tìm trong sổ mà model vừa viết thay cho câu người dùng gõ (chuyện thật thứ ba bên dưới).
- Gọi Serper **một lần**, hạn **5 giây**, không thử lại, lấy tối đa **5 kết quả**. Mỗi kết quả vào **sổ link** với một số `[w 1]`, `[w 2]`…
- Model viết một mục riêng **"Từ web (chưa kiểm)"** từ các đoạn trích đó, trích bằng `[w n]`.
- **Code kiểm trước khi hiện:**
  - mọi `[w n]` phải có trong sổ;
  - **chặn** link do model tự viết, mã trang web thô, dạng `href=`;
  - **số tiền** model viết phải có nguyên văn trong đoạn trích;
  - câu về **chỗ ở** thì không được nêu số tiền nào;
  - câu cần thông tin **"ngay lúc này"** (giá hôm nay, đang mở cửa không…) mà có con số thì thay bằng câu "chưa xác minh";
  - câu về **thiên tai** thì thay hẳn bằng câu cố định trỏ tới nguồn chính thức và 112. Model không được viết.
- Giao diện hiện mục web **tách khỏi** phần trả lời từ kho, dưới nhãn "Từ web (chưa kiểm)". Link trong mục web lấy từ sổ link, trang web **không bao giờ tạo
  link từ chữ của model**.

**Kết quả:**
- Bộ câu kín (05/11): **0 / 7** câu khẳng định thông tin chưa kiểm như thật; **7 / 7** câu có mục web hữu ích.
- Tốc độ (bộ kín, 05/11): mục web tới sau khoảng **13 giây** (trung vị), so với câu kho thường khoảng 3 giây. Chậm, nhưng chỉ xảy ra với câu kho không có.
- Tiền: khoảng **0,0018 USD** một câu có tra web, gồm Serper và model.

**Đường ra mới.** Tra web là lần đầu chatbot gửi chữ của người dùng (đã dựng thành câu tìm) ra một dịch vụ ngoài OpenAI. Anh đã chấp nhận điều này khi duyệt
thiết kế Phase 9. Từ 15/11, ở lượt hỏi tiếp thứ đi ra là **chữ model viết** (có tên nơi lấy từ câu trước), không còn là nguyên chữ người dùng gõ; anh đã nghe rõ
điều này và rủi ro kèm theo trước khi chọn bật.

## Hỏi bằng ảnh: một tên thì trả lời luôn, phân vân thì hỏi lại

**Cách chạy:**
1. Người dùng bấm **dấu cộng trong ô nhập** để chọn ảnh, hoặc **dán ảnh** thẳng vào ô. Ảnh nằm trong ô như một tệp đính kèm của câu hỏi; lúc này hệ thống **chưa
   gửi gì đi**. Gõ câu hỏi (hoặc để trống) rồi bấm **Hỏi** thì ảnh mới được gửi. Máy chủ kiểm trước khi đọc: chỉ nhận **JPEG, PNG, WEBP**, tối đa **10 MB**, không quá 40 triệu điểm ảnh, phải gửi từ đúng trang
   web của chatbot. Sai thì trả lỗi ngay.
2. Ảnh được **xoá thông tin kèm theo** (vị trí chụp, máy chụp), **thu nhỏ** còn cạnh dài 1.024 điểm ảnh, rồi gửi cho gpt-6-luna kèm **danh sách 42 điểm / món dễ
   nhận ra bằng ảnh**. Danh sách do code lập từ kho. Không kèm chữ của người dùng, không kèm lịch sử. Máy chủ **không lưu ảnh**.
3. Model chỉ được trả **tối đa 3 mã trong danh sách**, hoặc "không nhận ra". Code kiểm lại mã có trong danh sách thật.
4. Model trả **đúng một tên** ⇒ code ghép tên đó vào câu người dùng gõ và hỏi luôn như một câu thường, đi đường trả lời từ kho; đầu câu trả lời có dòng **"Mình
   đoán trong ảnh là … — có thể sai"** và một nút để gõ lại tên nếu đoán nhầm. Model trả **2–3 tên** ⇒ giao diện hiện các nút tên, người dùng **bấm đúng tên** rồi
   mới có câu trả lời. Model **không nhận ra** ⇒ lời báo, người dùng gõ tên. Ở cả ba trường hợp, model viết câu trả lời **không nhìn ảnh**: nó chỉ nhận cái tên
   và trả lời từ sổ, có nguồn như mọi câu khác.

**Vì sao phải chờ xác nhận.** Đo trên bộ ảnh (05/11): tên đúng nằm trong 3 gợi ý ở **22 / 25 ảnh**, đạt ngưỡng đặt trước (22). Nhưng với **ảnh không phải ở Huế**,
model vẫn gán một tên Huế cho **2 / 5 ảnh**, vượt ngưỡng cho phép (tối đa 1). Theo thước đặt trước thì kết quả **âm**. Anh quyết giữ tính năng nhưng ở dạng
**gợi ý có xác nhận**: model đoán nhầm thì người dùng không bấm, không có câu trả lời sai nào được viết ra. Bản đó chạy từ 08/11 tới 15/11.

**Vì sao tối 15/11 đổi sang "một tên thì trả lời luôn".** Khi thử, anh thấy bước bấm tên là thừa: hỏi "đây là đâu?" kèm ảnh thì phải có câu trả lời, như hỏi
ảnh ở các trợ lý quen dùng. Trước khi đổi, nhóm đếm lại kết quả đã lưu của bộ 33 ảnh, mỗi ảnh chạy 2 lượt (66 lượt): nếu **lượt nào cũng trả lời luôn theo tên
đầu tiên** thì **14 / 66 lượt** ra câu trả lời về **sai nơi**. Nhưng lỗi không rải đều: khi model chỉ đưa **một tên**, tên đó đúng ở **31 / 33 lượt** (xét các
ảnh có trong danh sách); khi model đưa 2–3 tên, tên đầu chỉ đúng 11 / 17. Tức là chính lúc model phân vân mới hay sai. Từ đó có cách **lai**: một tên thì
trả lời luôn, 2–3 tên thì hỏi chọn. Tính trên cùng 66 lượt, số lượt trả lời sai nơi còn **6 / 66**, đổi lại **19 / 66 lượt (29 %)** người dùng vẫn phải bấm
chọn. So với mốc cũ (luôn bấm tên, không lượt nào tự trả lời sai), cách lai **chấp nhận một ít câu sai nơi** để phần lớn lượt không phải bấm; vì vậy mới có
dòng "Mình đoán… có thể sai" ngay đầu câu trả lời. Mẫu nhỏ (33 ảnh, phần lớn là ảnh công khai chụp đẹp), nên các số này chỉ cho biết hướng, chưa phải tỉ lệ
với ảnh người dùng tự chụp.

**Tốc độ và tiền:** đoán mất khoảng **3 giây** ở trung vị, nhưng câu chậm 6–9 giây (chưa đạt mức 5 giây); khoảng 0,0004 USD một ảnh.

## Một chuyện thật: rào chắn bằng code bắt được điều lời dặn không bắt

**Tra web, vòng đầu.** Ở 2 câu, mục web **khẳng định như thật** lịch cúp điện và mức lũ lấy từ một trang chưa kiểm. Đây đúng loại lỗi nặng nhất (sai cảnh báo an
toàn). Cách sửa không phải dặn model "cẩn thận hơn", mà thêm **luật bằng code**: câu thiên tai thì thay bằng câu cố định; câu "ngay lúc này" có số thì thay bằng
"chưa xác minh". Review sau đó còn bắt thêm hai lỗ: link dạng mã trang web thô lọt qua bộ lọc, và bộ dò thiên tai thiếu chữ "lụt", "áp thấp". Cả hai được vá
bằng code.

**Hỏi bằng ảnh.** Thử cả cách không dùng model lớn: một model nhận ảnh chạy trên máy (SigLIP 2). Cách tốt nhất của nó được 20 / 25 ảnh đúng, nhưng gán tên Huế
cho **cả 5 / 5** ảnh không phải Huế, kể cả một ảnh con mèo. Bỏ. Còn thử ảnh có dán chữ kiểu "ra lệnh" cho model: 1 / 3 ảnh lừa được model ở mọi lượt. Đây là
thêm một lý do để **không trả lời khi người dùng chưa xác nhận**.

## Chuyện thật thứ hai: thử Exa, đo riêng thì đạt, qua máy chủ thật thì không

**Vì sao thử.** Mình đếm trên log máy chủ (từ 05/11): **73 lượt** có tra web. Có mục web ở **44 lượt (60 %)**; 13 lượt (18 %) ra "chưa xác minh" do luật "ngay lúc
này" (cố ý); 14 lượt (19 %) bị luật kiểm **bỏ cả mục** vì không tin cậy; Serper không lỗi lần nào, tra mất khoảng 2 giây. Giả thuyết: Serper chỉ đưa **tiêu đề và
một đoạn trích ngắn**, trung vị 147 ký tự mỗi kết quả, và 32 % kết quả là trang mạng xã hội. Câu hỏi giá, giờ cần con số nằm trong trang, không nằm trong 147 ký
tự đó, nên model hay viết số theo trí nhớ, rồi luật kiểm số tiền bỏ mục. Exa trả **đoạn trích nguyên văn từ trong trang, chọn theo câu hỏi**, và lọc được tên
miền. Đổi lại, Exa đắt hơn (khoảng 0,007 USD một lượt, Serper 0,001), chưa ai đo công khai với tiếng Việt, và gói thường cho phép họ dùng câu tìm để cải thiện
sản phẩm.

**Bước 1: đo riêng bước tra.** Một thí nghiệm ngoài máy chủ gọi đúng phần viết mục web và luật kiểm của chatbot, **chỉ thay dịch vụ tra**. Bộ đo 42 câu tự viết,
đã thấy, gồm ba loại: câu cần web, câu hỏi kèm hai ý, câu về chỗ ở và quán gần. Luật ghi trước: đếm số câu có mục web **đúng và trả lời được câu hỏi**, do **2
người chấm mù** cùng gắn; Exa phải hơn Serper ít nhất 5 câu. Kết quả: Serper **17**, Exa **25** ⇒ đạt (cần 22). Exa còn tra nhanh hơn (câu chậm 2,2 giây so với
3,1) và không trích trang mạng xã hội nào (Serper: 24 / 91 nguồn). Nhưng kết quả **nhạy**: 5 mục của Exa trích một trang tổng hợp do chính Exa tạo, không ghi
dữ liệu gốc. Bỏ 5 mục đó thì Exa còn 20, dưới ngưỡng. Bản Exa loại hẳn mạng xã hội cũng chỉ được 20.

**Bước 2: code sau cờ.** Thiết kế **Exa trước, Serper dự phòng**: Exa có hạn 3 giây; Exa lỗi, hết giờ hoặc không ra kết quả thì gọi Serper một lần với thời gian
còn lại; tối đa 40 lượt Exa mỗi ngày; thiếu khoá Exa thì dùng Serper. Cờ mặc định vẫn là Serper.

**Bước 3: đo qua máy chủ thật**, cùng 42 câu, mỗi bên một lượt. Luật ghi trước: Exa phải hơn Serper ít nhất 3 câu. Kết quả: Exa **14**, Serper **13** (cần 16)
⇒ **không đạt**. Các sàn đo bằng code đều qua (cờ tắt y như cũ, khoá sai thì Serper đỡ, tra vẫn nhanh hơn: câu chậm 2,26 so với 2,82 giây); phần chấm an
toàn chỉ làm được một phần vì công cụ đo không lưu chữ mục web. Vì vậy **giữ Serper**; phần
code Exa không vào bản chính, chỉ giữ làm hồ sơ.

**Vì sao hai lần đo khác nhau.** Quan sát: qua máy chủ, chỉ những câu **kho đã từ chối** mới được tra (khoảng 30 / 42 câu), nên ít chỗ để Exa hơn Serper. Đoạn
trích dài hơn làm model viết nhiều con số hơn, nên luật kiểm bỏ mục nhiều hơn (13 lượt "không tin cậy" so với 10). Còn nhiễu giữa hai ngày chạy thì là giả
thuyết, chưa tách được vì mỗi bên chỉ chạy một lượt.

**Bài học:** **đo trên đường người dùng thật trước.** Đo riêng một bước bỏ qua cổng web và luật kiểm phía sau, nên thấy lợi mà người dùng không nhận được.
Tiền cả việc: khoảng **0,195 USD** thật (khoảng 4.900 đồng), cộng khoảng 0,82 USD tín dụng dùng thử miễn phí của Exa.

## Chuyện thật thứ ba: hỏi tiếp "mở cửa lúc mấy giờ" mà ra nơi khác (15/11)

**Lỗi anh gặp.** Chiều 15/11 anh tự thử: câu đầu hỏi về một ngôi chùa, trả lời tốt. Câu sau anh gõ đúng năm chữ *"mở cửa lúc mấy giờ"*. Trợ lý nói sổ
không có, còn phần "Từ web" bên dưới lại nói về **nơi khác**. Lúc mình dựng lại đúng ca này thì thấy rõ hơn: trợ lý tìm thêm trong sổ hai lần rồi mới từ
chối, và mục web kể giờ mở cửa của một trung tâm thương mại và Đại Nội, kèm câu "bạn chưa nêu rõ địa điểm". Người hướng dẫn viên thật sẽ hiểu ngay khách đang
hỏi tiếp về ngôi chùa vừa nói.

**Tìm nguyên nhân: ghi lại câu ở từng khâu, không đoán.** Mình cho chạy lại đúng đường anh dùng (cùng một cuộc trò chuyện, hai lượt) và ghi lại mọi câu
mà hệ thống tự viết ra ở ba chỗ: lần tìm đầu trong sổ, các lần model tìm thêm, và câu gửi đi tra web.
- Dựng lại lỗi: **2 / 2 lần** đều ra đúng như anh thấy, kể cả khi câu sau có chữ "nó" ("nó mở cửa mấy giờ").
- **Phần sổ không mất mạch chuyện.** Trong 9 lần model tự tìm thêm ở các câu hỏi tiếp, **cả 9 lần** câu tìm đều có đúng tên nơi của câu trước. Với 7 cặp
  câu mà sổ *có* điều được hỏi, **7 / 7** câu hỏi tiếp được trả lời đúng nơi.
- **Phần web thì mất.** Câu gửi đi tra web được dựng từ **đúng câu của lượt này** — tức là "mở cửa lúc mấy giờ" thêm chữ "Huế", không có tên chùa. Đây là
  thiết kế cũ có chủ ý: không đưa các câu trước vào câu tra web, để tên người dùng lỡ nói ở lượt trước không lọt ra ngoài.
- Vậy lỗi chỉ lộ khi gặp đủ hai điều: **câu hỏi tiếp không nhắc lại tên**, và **sổ không có** điều được hỏi. Bộ câu đo cũ không có loại này.
- Một điều bị nghi đầu tiên (người điều phối đoán) nhưng không phải thủ phạm: lần tìm đầu trong sổ cũng dùng câu cụt và trượt **6 / 7** cặp. Nhưng model tự bù bằng một lần tìm thêm,
  nên câu trả lời vẫn đúng, chỉ chậm hơn một nhịp.

**Hai cách sửa đã đếm thử rồi bỏ** (cách đầu không tốn tiền; cách sau đếm trên 9 lượt tra web thật, khoảng 0,016 USD ≈ 400 đồng):
- *Ghép câu trước với câu sau bằng code.* Thử trên 10 cặp: cứu được câu hỏi tiếp, nhưng **phá 2 / 3 cặp đổi chủ đề thật** (người dùng hỏi sang chuyện khác
  mà câu tìm vẫn dính nơi cũ). Bỏ.
- *Cho bộ kiểm số hiểu các cách viết giờ ("7h", "7:00", "7 giờ").* Mình nghi mục web hay bị thay bằng câu "chưa tra được" vì giờ viết khác kiểu. Đếm trên
  85 mục web có lưu chữ (76 mục cũ + 9 mục mới: 8 câu hỏi giờ và 1 lượt đầu của ca anh): **0 mục** bị chặn vì lý do đó. Không đủ lỗi thì không xây.

**Cách sửa được chọn.** Ở lượt **có câu trước** và model **đã tự tìm thêm trong sổ**, code lấy luôn **câu tìm cuối cùng model vừa viết** (câu này đã có tên
nơi) làm câu tra web, và làm câu đưa cho lần viết mục web. Không thêm lần gọi model nào. Câu đó vẫn đi qua bộ lọc cũ: bỏ email, số điện thoại, cắt 120 ký tự.
Lượt đầu của cuộc trò chuyện, lượt model không tìm thêm, và **lượt hỏi nhiều ý** thì giữ nguyên như trước.

**Đo trước khi bật** (đường thật, tra web thật, một lượt; tiêu chí ghi trước khi chạy; khoảng 0,056 USD ≈ 1.400 đồng):

| Đo gì | Bộ câu | Trước khi sửa | Sau khi sửa | Đọc thế nào |
|---|---|---|---|---|
| Câu tra web có đúng tên nơi đang nói tới | sau: 8 cặp hỏi tiếp mà sổ thiếu (2 cặp dựng lại lỗi + 6 cặp do người điều phối viết; mình không viết, không sửa). Trước: tính bằng code trên 10 cặp hỏi tiếp, gồm cả 2 cặp bị loại | **0 / 10** (chưa sửa thì câu tra web chính là câu gõ) | **8 / 8** (cần ít nhất 7) | lỗi gốc hết |
| Mục web nói lạc sang nơi khác | sau: cùng 8 cặp, mình đọc tay từng mục. Trước: chỉ 2 lượt dựng lại ca của anh | **2 / 2** | **0 / 8** | hết lạc đề |
| Trong 8 mục đó, bao nhiêu mục **dùng được** | cùng 8 cặp | — | **2** có thông tin · 3 nói "đoạn trích không cho biết" · 3 là câu cố định "chưa tra được" | đúng nơi chưa có nghĩa là có câu trả lời |
| Tên người dùng lọt vào câu tra web | 4 lượt có nêu tên mình ở câu trước rồi hỏi câu cần web | 0 | **0 / 4** | **mẫu nhỏ**, chưa loại hẳn được rủi ro |
| Đổi chủ đề thật mà câu tra web còn dính nơi cũ | 1 cặp có mở tra web | — | **0 / 1** | ở cặp này câu model viết trùng câu gõ, nên rủi ro này **thực ra chưa được thử** |

Hai cặp trong bộ của người điều phối bị loại khỏi mẫu theo luật ghi trước: một cặp sổ trả lời được, một cặp cổng web không mở.

**Hai lượt review bắt được gì.** Người review thứ nhất viết một ca thử không tốn tiền và thấy: với **câu hỏi tiếp nhiều ý**, câu tìm cuối của model có thể
thuộc ý mà sổ đã trả lời, trong khi mục web phải viết cho ý còn thiếu — tra web sẽ lệch ý. Bộ đo có phí của mình không có cặp nhiều ý nào nên không lộ. Vì
chưa đo, mình để lượt nhiều ý dùng câu gõ như cũ. Người review thứ hai bắt thêm: câu tìm của model nếu chỉ còn số điện thoại thì sau bộ lọc chỉ còn chữ
"Huế" (đã cho quay về câu gõ), và báo cáo của mình có bốn chỗ nói rộng hơn bằng chứng (đã sửa, ví dụ phải ghi rõ "0 / 4 là mẫu nhỏ").

**Bật.** Anh cho bật lúc **17:50 ngày 15/11**. Người điều phối thử lại đúng ca của anh trên máy chủ: mục web nói **đúng ngôi chùa, kèm giờ**.

**Điều nên nhớ:** khi một câu trả lời sai, hãy ghi lại *chữ thật* đi qua từng khâu rồi mới kết luận khâu nào hỏng. Ở đây phần đáng ngờ nhất (trí nhớ hội
thoại) lại chạy đúng; chỗ hỏng là một quyết định an toàn cũ ở khâu tra web.

## Khi nào hỏng

- **Mục web có thể sai hoặc cũ** dù đã ghi "chưa kiểm". Địa chỉ, số điện thoại trong mục web chưa được kiểm là có trong đoạn trích hay không.
- **Mục web chậm**: khoảng 13 giây tới mục web (bộ kín, 05/11); trên 42 câu tự viết qua máy chủ 12/11, khoảng 18 giây ở trung vị.
- **Một con số không khớp là mất cả mục.** Khoảng 1 / 3 lượt tra mất mục web vì luật kiểm số (đo 12/11, cả với Serper lẫn Exa). Luật này cố ý chặt; chưa thử
  cách chỉ bỏ câu có số sai.
- **Câu hỏi tiếp nhiều ý** (hai ý trong một câu, sổ thiếu một ý) vẫn tra web bằng câu người dùng gõ, nên vẫn có thể cụt như trước 15/11. Chưa đo, chưa sửa.
- **Cùng một câu, mục web mỗi lần một khác.** Đúng ca của anh: ở lượt đo, cả hai cách hỏi (có và không có chữ "nó") đều ra câu cố định "chưa tra được";
  lượt sau hỏi lại câu không có chữ "nó" thì ra đúng ngôi chùa kèm giờ. Kết quả tìm của Serper và chữ model viết đổi giữa các lần; tỉ lệ thật chưa biết.
- **Thứ đi ra web giờ là chữ model viết.** Tên nơi của câu trước đi ra web (đó là chủ đích). Chữ model viết còn có thể thêm điều người dùng không gõ: ở một
  cặp đo, model tự đổi "cuối tuần này" thành ngày cụ thể. Tên người dùng: 0 / 4 lượt đo, mẫu nhỏ, không có rào bằng code cho tên riêng. Nếu sau này bật nhớ
  cả câu trả lời thì phải xét lại cờ này.
- **Luật "ngay lúc này" có thể chặn nhầm** nếu dò quá rộng (ví dụ chữ "đang").
- **Ảnh:** các lăng, các điện trông giống nhau dễ nhầm; ảnh có chữ lừa có thể đánh lừa model; chưa giới hạn số ảnh mỗi người; câu chậm chưa đạt 5 giây. Từ
  15/11: model đưa **một tên mà sai** thì trợ lý trả lời luôn về sai nơi, chỉ còn dòng "có thể sai" nhắc người dùng (đã gặp thật khi thử: ảnh một cổng trong
  Hoàng thành bị đoán thành một lăng); cùng một ảnh gửi nhiều lần có thể ra kết quả khác nhau.
- Bản đóng gói để đưa lên mạng (bài 18) đặt tra web **tắt**.

## Ba điều chính

1. **Tra web chỉ khi kho đã từ chối**, một lần, 5 giây. Mục **"Từ web (chưa kiểm)"** tách riêng. **Code chặn** link lạ, số tiền không có trong đoạn trích, câu
   "ngay lúc này", và thay câu thiên tai bằng câu cố định. Bộ kín: 0 / 7 câu khẳng định thông tin chưa kiểm.
2. **Hỏi bằng ảnh = model đoán tên, câu trả lời vẫn từ kho.** Đoán ra một tên thì trả lời luôn kèm dòng "có thể sai" (một tên đúng 31 / 33 lượt); phân vân
   2–3 tên thì hỏi người dùng chọn. Cách này còn 6 / 66 lượt trả lời sai nơi, so với 14 / 66 nếu lượt nào cũng trả lời luôn. Ảnh không lưu, đã xoá thông tin
   kèm theo.
3. Chuyện thật: những lỗi nguy hiểm nhất (khẳng định lũ, cúp điện) được chặn bằng **luật trong code**, không bằng lời dặn. Thử đổi Serper sang Exa: đo riêng
   bước tra thì đạt (25 so với 17) nhưng nhạy, qua máy chủ thật thì không (14 so với 13) ⇒ giữ Serper. Câu hỏi tiếp "mở cửa lúc mấy giờ" từng tra web bằng
   câu cụt nên lạc sang nơi khác; từ 15/11 dùng câu tìm model vừa viết: câu tra web đúng nơi 8 / 8 (trước 0 / 10), nhưng chỉ 2 / 8 mục có thông tin dùng được.

**Bài sau:** Bài 16 — Kể đồ án trong 2–3 phút (bản đủ), cùng chỗ còn yếu và hướng sửa.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Cổng web: `backend/llm/assistant.py` `web_gate_open`; cờ `tra_web: true`: `backend/config/settings.yaml` [code]
- Tra web: `backend/llm/tra_web.py` (dựng câu tìm, Serper một lần, `tra_web_timeout_seconds: 5`, ≤ 5 kết quả, kiểm `[w n]`, chặn link / HTML, số tiền ⊂ đoạn trích, lưu trú 0 tiền, `la_cau_thoi_gian_thuc`, `la_cau_thien_tai`) [code]; nhãn mục web: `frontend/src/pages.jsx` [code]
- Bộ kín web 0 / 7, 7 / 7; khoảng 13 s; khoảng 0,0018 USD; hai câu cúp điện / lũ vòng đầu; review bắt link thô và thiếu "lụt / áp thấp" (05/11): `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` [đã chạy]
- Đường ra Serper anh chấp nhận: spec Phase 9 §7; `session_prompt/Project_Status.md` §6 [quyết định của anh]
- Hỏi bằng ảnh: `backend/api/routes/anh.py` (kiểu ảnh, 10 MB `max_bytes`, kiểm trước khi đọc, Origin), `backend/llm/nhan_anh.py` (danh sách tên, ≤ 3 mã / `khong_nhan_ra`, kiểm lại mã, thu nhỏ `canh_dai`, xoá EXIF) [code, xem 11/11]; danh sách 42 mục: `data/phase_10/anh/danh_sach_ten.json` (riêng tư; đếm 11/11) [đã chạy]
- Ảnh: 22 / 25 trong 3 gợi ý, ảnh ngoài Huế 2 / 5; SigLIP 2 20 / 25 và 5 / 5; ảnh chữ lừa 1 / 3; khoảng 3 s, câu chậm 6–9 s; khoảng 0,0004 USD / ảnh: `bao_cao_he_thong/08_BAO_CAO_HOI_BANG_ANH.md` (05/11) [đã chạy]
- "Khách sạn gần cầu Trường Tiền" là câu tự đặt.
- Câu hỏi nối tiếp (15/11): dựng lại 2 / 2, câu tìm kho nêu tên 9 / 9, kho có ⇒ 7 / 7, lần tìm đầu trượt 6 / 7, ghép câu phá 2 / 3 cặp đổi chủ đề: `report_agent/2026-11-12_ra_khoang_cach/b_cau_noi_tiep_dem.md` [đã chạy]; 0 / 85 mục bị chặn vì cách viết giờ, ca gốc dao động 2 / 2 ⇒ 1 / 1: `…/b_web_kiem_so_dem.md` [đã chạy]; cách sửa, 8 / 8 ↔ 0 / 10, 0 / 8 ↔ 2 / 2, 2 + 3 + 3, tên 0 / 4, đổi chủ đề 0 / 1, loại 2 cặp, 0,0556 USD, sửa theo hai review: `…/b_web_noi_tiep_implementation.md`, `…/e_review_web_noi_tiep.md`, review thứ hai `data/review_web_noi_tiep_2026-11-15/review.md` (riêng tư) [đã chạy]; kiểm độc lập mục này trước khi ghi: `data/kiem_bai_hoc_2026-11-15/b_kiem_doc_lap.md` (riêng tư; 60 khẳng định: 2 sai, 11 dễ hiểu nhầm — đã sửa); code `backend/llm/assistant.py` `cau_cho_web`, `cong_web`; cờ `web_cau_noi_tiep: true` (bật 17:50 15/11/2026, anh chọn; người điều phối thử ca gốc qua máy chủ) `backend/config/settings.yaml` [code]
- Exa (12/11): 73 lượt log, 44 / 13 / 14, 0 lỗi Serper, 147 ký tự, 32 % mạng xã hội, giá 0,007 ↔ 0,001, điều khoản dùng dữ liệu: `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` §1–2; thí nghiệm 17 / 25 / 20, p95 3,1 / 2,2, mạng xã hội 24 / 91 ↔ 0 / 109, độ nhạy 25 ⇒ 20 khi loại trang tổng hợp của Exa: cùng file §5, §6, §6b; server thật 13 / 14 (cần ≥ 16), không tin cậy 10 / 13, tra p95 2,82 / 2,26, tới sự kiện web 17,9 / 16,9 s, ≈ 30 / 42 câu được tra, 13 / 30 và 10 / 29 lượt mất mục do luật kiểm, ≈ 0,195 USD + ≈ 0,82 tín dụng: §7 [đã chạy]; kiểm thí nghiệm: `…/e_exa_review.md`; kiểm code (Exa trước 3 s, Serper dự phòng, 40 lượt / ngày): `…/e_exa_code_review.md`; nhánh `p9-tra-web-exa` không merge (`tra_web.py` trên `main` không có Exa), tag `hoso/p9-tra-web-exa` [code, theo bản ghi số liệu 13/11]. Bản ghi số liệu: `data/hoc_cung_user_2026-11-10/fact_viec_12_11.md` (riêng tư)
- **Sửa 20:22 13/11/2026:** số "khoảng 13 giây" ghi rõ là bộ kín 05/11, thêm số 12/11 qua máy chủ (khác bộ câu, khác cách đo).

- **Sửa 14:48 11/11/2026:** theo luật anh chốt ("phần chưa xong thì không đưa vào bài học"), gỡ đoạn tả việc chưa làm xong: câu "đang chờ anh quyết lúc deploy" → tả đúng bản đóng gói đã dựng (`HUE_TRA_WEB` "false" trong `data/phase_12/deploy_nhap/compose.yml`).
- **Sửa 21:34 15/11/2026** (luồng hỏi bằng ảnh đổi tối 15/11): viết lại dòng "Hỏi bằng ảnh" ở bảng từ, đoạn ví dụ người hướng dẫn nhìn ảnh, tiêu đề + bước 1 và bước 4 của mục "Hỏi bằng ảnh", mục 2 của "Ba điều chính", thêm đoạn "Vì sao tối 15/11 đổi…" và một ý ở phần giới hạn. Số 14 / 66, 6 / 66, 19 / 66, 31 / 33, 11 / 17: phép đếm lại kết quả đã lưu của bộ 33 ảnh × 2 lượt `data/dem_ten_so_1_2026-11-15/KET_QUA.md` (riêng tư) [đã chạy, không gọi model]; luồng mới + ca đoán sai khi thử: `report_agent/2026-11-12_ra_khoang_cach/e_anh_tra_loi_thang_implementation.md`, `c_anh_dinh_kem_implementation.md`, `c_nut_anh_cong_implementation.md`; code `frontend/src/HoiBangAnh.jsx` [code, xem 15/11].
- **Sửa 20:37 13/11/2026** theo kiểm độc lập (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_13_11.md`, riêng tư): bảng từ còn 3 từ mới: "Tra web", "Hỏi bằng ảnh" đã gặp ở bài 12.

</details>
