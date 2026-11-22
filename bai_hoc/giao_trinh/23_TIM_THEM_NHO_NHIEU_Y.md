# Bài 23 — Tìm thêm, nhớ câu hỏi trước, và câu hỏi nhiều ý

*Cập nhật 17:11, ngày 22/11/2026 · khớp hệ thống 16:35 22/11 (47 tính năng, kho 267 bài); nhớ câu trả lời liền trước cả trong cuộc đã lập lịch (mở 16:08) · cơ chế đọc từ chương trình và cấu hình đang chạy; số đo chép từ các báo cáo 03/11–22/11, ghi model ở từng số; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** harness (bài 21): model được tự tìm kho thêm tối đa 3 lần (trước 14:47 ngày 22/11: 2); bước xếp loại câu (bài 22) chọn tuyến cho từng tin.
**Bài này thêm:** hai loại tin mà tìm một lần bằng chính tin đó là không đủ: tin nối tiếp ("còn chỗ đó thì sao?") và tin hỏi nhiều điều một lúc. Hệ thống nhớ gì, ai dùng phần nhớ đó, và tin nhiều ý được xử lý ra sao.

## Ý chính

- 10 đoạn ở lần tìm đầu; trợ lý được tìm thêm tối đa 3 lần bằng câu tìm model tự viết (bài 21); tin nhiều ý được nối thêm 2 đoạn mỗi ý. Cả bài dựa trên quyền đó.
- **Máy chủ nhớ 3 lượt gần nhất** của một cuộc trò chuyện, trong 30 phút. Lượt cũ được gửi lại dưới dạng câu hỏi; riêng lượt liền trước kèm câu trả lời (bỏ số nguồn, cắt 4.000 ký tự, có nhãn "không phải nguồn"); từ 16:08 22/11 cả trong cuộc đã lập lịch, trừ lượt sửa lịch.
- **Lịch sử chỉ để hiểu câu hỏi nói về cái gì**, không làm nguồn. Lần tìm đầu vẫn dùng đúng câu gõ; model đọc lịch sử rồi tự viết câu tìm có tên đối tượng.
- Lượt mà lịch sử gửi kèm có câu trả lời liền trước, nếu bị rút ở bước kiểm sau khi viết, thì **chạy lại đúng một lần** không kèm câu trả lời đó (chỉ ở ô chat, không ở lượt sửa lịch; bài 16).
- **Tin nhiều ý** (chương trình đếm được từ hai vế hỏi): trả lời ý kho có, ghi "Tư liệu chưa có thông tin về: …" cho ý thiếu; từ 22/11 mỗi vế được nối thêm 2 đoạn, nhiều nhất 6 vế. Từ 14:47 ngày 22/11: vế cụt (không có chủ thể) không được tìm riêng; câu tìm gộp nhiều nơi của model được tìm thêm theo từng phần.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| mã cuộc trò chuyện | **conversation id** (cất trong **cookie**) | chuỗi ngẫu nhiên máy chủ đưa trình duyệt cất; trình duyệt gửi kèm mỗi câu hỏi để máy chủ biết câu đó thuộc cuộc nào |
| lịch sử | **history** | phần cuộc trò chuyện được gửi kèm cho model ở lượt mới |
| vế hỏi | — | một câu hỏi con trong tin, có từ hỏi riêng ("bao nhiêu", "ở đâu", "không"…) |
| dòng ý thiếu | — | dòng mở đầu bằng "Tư liệu chưa có thông tin về:" model viết cho vế kho không có |
| vế cụt | — | vế đứng riêng không còn biết hỏi về cái gì ("giờ mở cửa ko?", "mất bao lâu?") |
| câu tìm gộp | — | câu tìm model viết nhắc hai nơi hoặc hai ý cùng lúc ("giá vé Đại Nội và Lăng Tự Đức") |

## Tìm thêm là chỗ dựa: ba điều cần mang theo từ bài 21

Ví dụ "phải tìm thêm" ở bài 21 cho ba điều dùng lại ở dưới:

1. **Lần tìm đầu luôn bằng đúng câu gõ.** Câu "còn chỗ đó thì sao?" không có tên nơi nào để tìm.
2. **Câu tìm thêm do model viết**, và model có đọc lịch sử: đó là đường tên của lượt trước đi vào câu tìm.
3. **Tìm một lần bằng cả tin thì các đoạn dồn về vế chính** của tin nhiều ý.

## Máy chủ nhớ ba lượt gần nhất, và chỉ một câu trả lời

Tin đầu tiên làm máy chủ tạo một mã cuộc trò chuyện; các tin sau mang mã đó. Phần nhớ nằm trong bộ nhớ của máy chủ (bài 6). Mỗi lượt xong được cất thành cặp: câu hỏi và một ô đi kèm:

| Ô đi kèm | Khi nào |
|---|---|
| câu trả lời, đã bỏ số nguồn, cắt 4.000 ký tự, sau dòng nhãn do chương trình viết: "[Lời trợ lý ở lượt trước — chỉ để hiểu câu hỏi tiếp; KHÔNG phải nguồn, không được trích hay coi là bằng chứng]" | chỉ lượt **liền trước**, và chỉ khi đó là câu trả lời thường từ kho |
| dòng ghi chú tên nơi do chương trình dựng từ tên các bài riêng đã trích (nhiều nhất 5): "[Ghi chú hệ thống — câu trả lời lượt này có trích bài kho của các nơi: …]" | các lượt cũ hơn |
| để trống | lượt không trích bài riêng của nơi nào |

Cuộc giữ 3 lượt; 30 phút không hỏi thì bị xoá. **Không giữ câu trả lời** của câu cố định (từ chối, ngoài phạm vi, hỏi lại), lượt lịch và sửa lịch, và lượt dùng nguồn đổi theo giờ: thời tiết, ngày và âm lịch, sự kiện theo ngày, khoảng cách.

**Cuộc đã lập lịch** (cuộc mà người dùng đã lập một lịch ở trang Lên kế hoạch rồi hỏi tiếp trong đó): mọi lượt hỏi thường của cuộc này đều mang thêm nguồn "lịch bạn đang có". Trước 16:08 22/11, vì luật "lượt dùng lịch không giữ câu trả lời", cả cuộc mất việc nhớ này. Từ 16:08 22/11 câu hỏi thường trong cuộc đó cũng được nhớ; chỉ không nhớ lượt thật sự sửa lịch và câu trả lời có trích nguồn của lịch.

Ví dụ đo 22/11 (Claude Sonnet 5.5): *"Kể cho mình ba quán cơm hến hoặc bún hến ở Huế"* rồi *"quán thứ hai bạn vừa kể ở đường nào?"*. Không có câu trả lời cũ: không xác định được quán thứ hai. Có nó: nêu đúng quán và đường, trích nguồn của lượt mới (8,8 xuống 3,9 giây). Trong cuộc đã lập lịch, *"Kể các quán chè ở Huế"* rồi *"Bỏ quán đầu đi rồi viết lại danh sách"*: 9 lượt thật (22/11, Claude), lịch không đổi 3 trên 3, danh sách bỏ đúng quán đầu 3 trên 3; đã nhìn trên trình duyệt cùng ngày.

## Lịch sử giúp hiểu câu hỏi, không làm nguồn

| Chỗ trong một lượt | Dùng lịch sử thế nào |
|---|---|
| xếp loại câu (bài 22) | thấy lịch sử, kèm câu dặn "chỉ chọn tuyến cho tin nhắn cuối cùng" |
| lần tìm đầu | **không dùng**: chỉ câu gõ |
| chọn công cụ đưa cho model (bài 24) | xét câu gõ **và câu hỏi liền trước**: "còn tuần sau thì sao?" sau một câu thời tiết vẫn có công cụ thời tiết |
| model trả lời | thấy lịch sử, kèm một đoạn dặn: câu tìm thêm phải nêu đúng tên đối tượng lấy từ các lượt trước; mỗi nhận định phải lấy từ bằng chứng nói đúng về đối tượng đó |

Vì vậy tin nối tiếp thường cần thêm một lần model xin tìm kho: lần tìm đầu bằng câu cụt thường trượt, model xin tìm thêm bằng câu có tên nơi (số đo ở "Chi tiết để tra"). Luật "lịch sử không làm nguồn" được giữ bằng bước kiểm số nguồn (bài 16): câu trả lời cũ đã mất hết số nguồn.

## Mang câu trả lời liền trước có một tác dụng phụ: chạy lại đúng một lần

Trợ lý vừa kể một lộ trình bằng chữ, người dùng gõ *"Bỏ Chợ Đông Ba đi"*: model có lúc chép lại lộ trình cũ mà không trích nguồn, câu bị rút (3 trên 7 lần đo sáng 22/11). Nay ở ô chat, lượt như vậy được chạy lại cả lượt **một lần** không kèm câu trả lời cũ; đo lại 0 trên 5 lần ra màn hình lỗi (bài 16, quyết định 4; chi tiết ở "Chi tiết để tra").

## Tin nhiều ý được trả lời theo từng ý

Lời dặn gốc: bằng chứng không đủ thì trả một câu từ chối. Hỏi *"vé Đại Nội bao nhiêu, dịp Tết có chương trình gì?"* mà kho chỉ có giá vé thì mất luôn giá vé (14/11, gpt-6-luna: phần kho có được trả lời 4 trên 10 tin). Bốn bước hiện nay:

1. **Chương trình đếm vế**: tách ở dấu phẩy, dấu chấm phẩy, dấu hỏi và ở "và / còn / với"; một phần là một vế khi chính nó có từ hỏi (luật đủ ở "Chi tiết để tra").
2. **Từ hai vế, model nhận lời dặn theo ý**: ý có bằng chứng thì trả lời; ý không có thì một dòng riêng mở đầu đúng bằng "Tư liệu chưa có thông tin về:", không số nguồn, không đoán.
3. **Chương trình chốt**: mọi dòng đều là dòng ý thiếu thì đổi cả câu về câu từ chối chuẩn, và chỉ lúc đó mới tra web (bài 25). Trả lời được một phần thì giữ dòng ý thiếu, không tra web.
4. **Tìm theo vế (từ 22/11)**: 10 đoạn của cả tin giữ nguyên; chương trình tìm riêng từng vế (nhiều nhất 6), nối 2 đoạn đầu mỗi vế vào sau. Model đọc khoảng 15 đoạn (10 cũ + trung vị 6 đoạn thêm); không thêm lần gọi model. Từ 14:47 ngày 22/11, vế cụt không được tìm riêng.
5. **Tách câu tìm gộp của model (từ 14:47 ngày 22/11)**: lần tìm cả câu giữ nguyên; mỗi phần được tìm riêng, 2 đoạn đầu nối thêm.

Bước 4 có vì một phép đếm tối 21/11 (Claude Sonnet 5.5): 86 % lượt nhiều ý có dòng ý thiếu, khoảng một phần tư tới một phần ba số dòng đó sai (kho có; ví dụ ở "Chi tiết để tra").

Hai sửa sau đến từ một tin 4 ý của một gia đình: câu tìm gộp không kéo được đoạn giá vé, còn vế cụt kéo về đoạn không liên quan ("Chi tiết để tra"; số ở "Đã so" dòng 10–11).

## Quyết định và lý do

### 1. Vì sao lịch sử chỉ mang câu trả lời của lượt liền trước?

- **Đã chọn:** chỉ câu trả lời của lượt liền trước; lượt cũ hơn còn câu hỏi và tên nơi.
- **Vì sao:** bản nhớ cả ba câu trả lời (03/11, gpt-6-luna) từng trả lời một tin ngoài kho bằng đoạn của đối tượng khác; sửa lời dặn xong, lợi vẫn chưa chắc (Đã so dòng 1b). Đếm 20/11 trên 122 lượt hỏi tiếp của nhóm: thiếu câu trả lời cũ làm hỏng 3 lượt, cả ba trỏ vào câu trả lời vừa rồi.
- **Cách khác:** chỉ nhớ câu hỏi (03/11 – 22/11): đã đo, tin hỏi tiếp khá hơn không nhớ (Đã so dòng 1), nhưng không hiểu "quán thứ hai". Nhớ ba lượt: đã đo, bỏ.
- **Cái giá:** lượt có lịch sử dài thêm khoảng 400–500 token; câu trả lời của hai lượt trước không còn.

### 2. Vì sao lượt có thời tiết, ngày, khoảng cách không được giữ câu trả lời?

- **Đã chọn:** câu trả lời dùng nguồn đổi theo giờ không vào lịch sử.
- **Vì sao:** đo 21/11 (Claude Sonnet 5.5): hỏi tiếp về "con số khả năng mưa bạn vừa đưa" khi có câu trả lời cũ thì model tự từ chối 8 trên 10 lần, vì số đã nằm trong phần "không phải nguồn" nên nó không gọi lại công cụ; không có câu trả lời cũ: 0 trên 6. Luật ghi trong chương trình: số dự báo phải đến từ công cụ của lượt này.
- **Cách khác:** giữ cả câu có số dự báo: đã đo, bỏ.
- **Cái giá:** hỏi tiếp về con số vừa đưa phải gọi lại công cụ, chậm hơn một vòng.

### 3. Vì sao chương trình đếm vế và chốt kết quả, không chỉ đổi lời dặn?

- **Đã chọn:** chỉ tin từ hai vế mới nhận lời dặn theo ý; câu toàn dòng ý thiếu bị đổi về câu từ chối chuẩn.
- **Vì sao:** vòng đầu 14/11 đổi lời dặn cho mọi tin (gpt-6-luna): tin nhiều ý được trả lời 10 trên 10, nhưng 3 trên 18 câu ngoài kho của bộ câu mẫu bị trả lời. Vòng hai để chương trình quyết: vẫn 10 trên 10, bộ kín 0 trên 10. Chủ dự án chọn bật.
- **Cách khác:** lời dặn theo ý cho mọi tin: đã đo, bỏ. Để model tự nói tin có mấy ý: chưa thử.
- **Cái giá:** tin hai ý mà một vế không có từ hỏi riêng ("… bao xa, rồi ghé chợ nữa") bị đếm là một vế, có lần bị từ chối cả câu.

### 4. Vì sao bỏ vế cụt và tách câu tìm gộp, thay vì chỉ cho model tìm thêm?

- **Đã chọn:** vế cụt không được tìm riêng; câu tìm gộp của model được tìm thêm theo từng phần, giữ lần tìm cả câu. Mở 14:47 ngày 22/11 cùng trần 3 và bước viết lại (bài 21).
- **Vì sao:** đã đo (đoạn trên): gốc nằm ở câu tìm, không ở số lần tìm. Bằng chứng còn gọn hơn (nguồn trung vị 20 ⇒ 16), không kém ở tin nào khác của lượt đo.
- **Cách khác:** chỉ nâng trần tìm lên 3: đã đo, không có ích (bài 21). Ghép chủ thể vào vế cụt: đã đếm trên 20 đoạn, chỉ đúng 6; chưa làm. Hai cách khác nữa ở "Chi tiết để tra".
- **Cái giá:** thứ vế cụt thật sự hỏi không được tìm riêng; vài vế bị lọc oan, nhưng tin vẫn được tìm bằng cả câu. Mỗi lần tìm của model dài thêm khoảng 2 đoạn.

## Nếu… thì sao

Tình huống kể trọn: hỏi về một ngôi chùa, 40 phút sau gõ *"chỗ đó mở cửa mấy giờ?"*. Cuộc đã bị xoá; model không biết "chỗ đó" là đâu nên từ chối hoặc nói không rõ nơi nào, trong khi màn hình vẫn còn các lượt cũ. Đọc từ chương trình, chưa thử thật.

| Nếu | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|
| 30 phút không hỏi, hoặc máy chủ khởi động lại | tin nối tiếp không được hiểu | **chưa có** cách báo hay giữ lâu hơn |
| tải lại trang | màn hình trống; giao diện gọi "Cuộc trò chuyện mới" nên máy chủ cũng quên | đã có từ 15/11 (trước đó 3 trên 3 lần tái hiện bị từ chối) |
| lượt mang câu trả lời cũ bị rút, lần chạy lại cũng bị rút | "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" | người dùng bấm "Thử lại" hoặc hỏi lại bằng tên nơi |
| tin dài nhiều ý, model đã tự tìm ít nhất một lần (thường là đã hết lượt) mà chữ nộp không có số nguồn | dòng trạng thái đứng lâu hơn, rồi câu viết lại từ các đoạn đã gom (bài 21); cả lượt tới 25–37 giây | có từ 14:47 22/11; mới đo trên một tin; giữ chữ từ 15:42 nên đoạn chữ giữ chỗ không còn hiện; ca viết lại: theo test và một lượt thật, chưa nhìn trên trình duyệt |
| tin nhiều ý mà không vế nào kho có | câu dẫn "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)." rồi mục web; mục web không có gì thì câu từ chối chuẩn (bài 25) | đã có |

## Dễ nhầm

- **"Trợ lý nhớ cả cuộc trò chuyện."** Không. 3 lượt gần nhất, trong 30 phút; chỉ lượt liền trước có câu trả lời.
- **"Câu trả lời trước được dùng làm nguồn."** Không. Nó mất số nguồn và mang nhãn "không phải nguồn"; dữ kiện phải trích đoạn tìm ở lượt này.
- **"Model tự chia ý."** Chương trình đếm vế và chọn lời dặn; model chỉ viết từng ý.

## Câu hỏi tự kiểm

<details>
<summary>1. Tin "còn chỗ đó thì sao?": lần tìm đầu bằng câu nào, tên nơi vào câu tìm bằng đường nào?</summary>

Lần tìm đầu bằng đúng câu gõ. Model đọc lịch sử rồi xin tìm thêm bằng câu có tên nơi của lượt trước.

</details>

<details>
<summary>2. Vì sao câu trả lời của một lượt xem thời tiết không được giữ?</summary>

Số dự báo phải đến từ công cụ của lượt mới. Có câu trả lời cũ thì model tự từ chối 8 trên 10 lần thay vì gọi lại công cụ.

</details>

<details>
<summary>3. Tin hai ý, kho có ý đầu. Câu trả lời trông thế nào, có mục web không?</summary>

Ý đầu có số nguồn; ý sau là dòng "Tư liệu chưa có thông tin về: …". Không có mục web: web chỉ mở khi cả câu bị từ chối.

</details>

<details>
<summary>4. Model viết câu tìm "giá vé Đại Nội và Lăng Tự Đức". Chương trình tìm những gì?</summary>

Tìm cả câu như cũ, rồi tìm riêng "giá vé Đại Nội" và "Lăng Tự Đức", nối 2 đoạn đầu mỗi phần: câu gộp hay không kéo được đoạn giá của từng nơi.

</details>

## Cấu hình đang chạy

*Theo chương trình và cấu hình 22/11/2026 (sau 16:08).*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Tự tìm thêm (`tim_them`), số lần (`so_lan_tim_kho`) | bật; 3 (từ 14:47 22/11; trước là 2) | bài 21 | bài 21 |
| Nhớ cuộc trò chuyện (`nho_hoi_thoai`) | bật (từ 03/11) | hiểu tin nối tiếp | đã so bật / tắt (mục "Đã so", dòng 1) |
| Số lượt giữ mỗi cuộc | 3 | kế hoạch ghi "6 tin", theo lộ trình đặt 4–6 tin | chưa so |
| Hết hạn | 30 phút từ lượt cuối | theo bản thiết kế phần nhớ | chưa so |
| Số cuộc giữ cùng lúc | 500; quá thì bỏ cuộc cũ nhất | để bộ nhớ của máy chủ có giới hạn | chưa so |
| Trần token của lịch sử | không còn (gỡ 19/11, theo lời chủ dự án "chất lượng trước") | — | trước 19/11 là 1.500 token; chưa lượt nào từng chạm (lớn nhất 105) |
| Giữ câu trả lời liền trước (`nho_cau_tra_loi`) | bật 09:40 22/11 | hiểu "quán thứ hai bạn vừa kể" | dòng 3 |
| Nhớ câu trả lời liền trước cả trong cuộc đã lập lịch (`nho_dap_cuoc_co_lich`) | bật 16:08 22/11 | câu hỏi thường trong cuộc đã lập lịch cũng được nhớ câu trả lời liền trước, và lượt bị rút được chạy lại một lần; không nhớ / không chạy lại: lượt thật sự sửa lịch, câu trả lời có trích nguồn của lịch | dòng 12; tắt (trước 16:08): cả cuộc không nhớ |
| Cắt câu trả lời liền trước | 4.000 ký tự | 20/11 đặt 1.200 (gpt-6-luna trả lời ngắn); 21/11 với Claude, 2 trên 7 câu trả lời của một lượt tự kiểm dài hơn 1.200 (dài nhất 2.229) ⇒ nâng lên để mục cuối danh sách không mất | 1.200, bỏ |
| Nhớ tên nơi đã trích (`nho_ten_goi_y`) | bật 19/11; nhiều nhất 5 tên | lượt cũ biết đã nhắc nơi nào; câu xin "kể lại các nơi vừa nêu" và câu gõ lại nguyên văn một câu cũ thì lượt đó không nhận dòng này | dòng 2 |
| Lần chạy lại khi bị rút | 1 lần; chỉ khi lịch sử đang mang câu trả lời cũ; mọi lỗi của bước kiểm sau khi viết; chỉ ở ô chat (đường gửi chữ từng mảnh, kể cả với Claude); không ở lượt có câu cố định, lượt sửa lịch (cuộc có lịch lưu: chạy lại câu hỏi thường từ 16:08 22/11, trước đó không) | tệ nhất bằng lúc không giữ câu trả lời | dòng 4 |
| Lời dặn theo ý (`cau_nhieu_y`) | bật 14/11; từ 2 vế | dòng 5 | dòng 5 |
| Tra web cho tin trả lời được một phần (`web_chi_khi_tu_choi`) | không tra (từ 21/11) | dòng 6 | dòng 6 |
| Tìm theo vế (`tim_theo_ve`) | bật 09:47 22/11; 2 đoạn mỗi vế; nhiều nhất 6 vế | dòng 7 | 2, 3, 4 đoạn: cùng kết quả (đếm 0 đồng) |
| Bỏ vế cụt khỏi lần tìm riêng (`tim_ve_bo_cut`) | bật 14:47 22/11 | vế không tên riêng, còn dưới hai từ mang nội dung sau khi bỏ từ hỏi, từ đệm, từ chung (giờ, giá, vé…) thì không tìm riêng; một danh sách chủ thể ngắn ("taxi", "chợ đêm", "vé xe buýt"…) vẫn được tìm | dòng 10 |
| Tách câu tìm gộp của model (`tach_cau_tim_model`) | bật 14:47 22/11; 2 đoạn mỗi phần; nhiều nhất 3 phần | câu tìm có "và", ";", "+" ⇒ mỗi phần (từ 6 ký tự) tìm riêng, nối sau kết quả cả câu | dòng 10, 11 |

## Đã so

**Vấn đề thật đã gặp.** Tin nối tiếp không có tên đối tượng bị từ chối hoặc trả lời về nơi khác; tin nhiều ý mất cả phần kho có, hoặc bị ghi "chưa có" sai cho vế phụ.

| # | Thử gì, so với gì | Bộ câu, model, ngày | Kết quả | Giữ / bỏ |
|---|---|---|---|---|
| 1 | chỉ nhớ câu hỏi, so với không nhớ | bộ tin hỏi tiếp; gpt-6-luna; 03/11 | điểm tin hỏi tiếp +0,80 [+0,25; +1,50]; câu bẫy (tiền đề sai) từ chối đúng 6 / 6 (không nhớ: 3 / 6); từ chối nhầm 0 / 19 (không nhớ: 5 / 19) | **giữ** |
| 1b | nhớ cả câu trả lời của ba lượt | cùng bộ + bộ câu kín; gpt-6-luna; 03/11 | một lượt kín: tin ngoài kho được trả lời bằng đoạn của đối tượng khác; sau câu dặn thêm: +0,50 [−0,15; +1,20], chứa 0 | bỏ |
| 2 | nhớ tên nơi đã trích, so với không | 17 chuỗi; gpt-6-luna; 19/11 | lượt hỏi tiếp nói đúng nơi 15 / 17 (không: 2 / 17); 0 lượt nói chắc về sai nơi | **giữ** (chủ dự án chọn bật) |
| 3 | giữ câu trả lời liền trước, so với không | 4 chuỗi × 3 lượt, 24 lượt; Claude Sonnet 5.5; 22/11 | chuỗi "quán thứ hai": không giữ thì không xác định được, giữ thì đúng; ba chuỗi còn lại như nhau; 0 lỗi; 0 lượt lấy câu trả lời cũ làm nguồn | **giữ** (nhóm đã chốt; báo cáo tự ghi là "lợi nhỏ" theo tiêu chí chặt) |
| 4 | chạy lại một lần khi bị rút | chuỗi "lộ trình ⇒ Bỏ Chợ Đông Ba đi" × 5; Claude Sonnet 5.5; 22/11 | màn hình lỗi 3 / 7 (trước) ⇒ 0 / 5; chạy lại thật 2 / 5, cả hai ra câu trả lời | **giữ** |
| 5 | lời dặn theo ý cho mọi tin (vòng 1), so với chương trình đếm vế rồi chốt (vòng 2) | 10 tin nhiều ý + bộ 176 câu mẫu + bộ kín 10 câu; gpt-6-luna; 14/11 | vòng 1: 10 / 10 tin, nhưng 3 / 18 câu ngoài kho bị trả lời, 2 lỗi trích dẫn. Vòng 2: 10 / 10, kín 0 / 10, 0 câu của bộ 176 đi vào luật mới | **giữ vòng 2** |
| 6 | tin trả lời được một phần không tra web, so với tra | 11 tin nhiều ý; Claude Sonnet 5.5; 21/11 | đi tra web 11 / 11 ⇒ 0 / 11; nhanh hơn ở 11 / 11 tin, câu đứng giữa 5,8 giây; ba lượt mốc trước đó: mục web đáp đúng điều thiếu 1 / 66 dòng | **giữ** |
| 7 | tìm theo vế, so với tìm một lần bằng cả tin | đếm 0 đồng 8 dòng "chưa có" sai + lượt thật 8 tin × 3 lượt; Claude Sonnet 5.5; 21–22/11 | đoạn đúng vào ngữ cảnh 1 / 8 ⇒ 5 / 8 (tách vế như bộ đếm ý: 3 / 8); nêu được dữ kiện 3 / 24 ⇒ 15 / 24; bỏ hai tin quán ăn (bên tắt đã khá hơn nhờ công cụ "gần một điểm"): 3 ⇒ 9 trên 18 | **giữ** |
| 8 | model viết lại câu tìm trước lần tìm đầu (3 cách), so với tìm bằng câu gốc | 12 câu; gpt-6-luna; 03/11 | chỉ thêm 0–1 / 12 câu đủ từ khoá (cần ít nhất 3) | bỏ |
| 9 | cho model gọi hai lần tìm cùng một lúc, so với lần lượt | 176 câu mẫu + 32 câu an toàn; gpt-6-luna; ghi vào bảng tổng 15/11 | model gần như không dùng: 1 / 176 câu; 7 câu nhanh hơn 2,3 giây nhưng vì model tìm 1 lần thay vì 2 | bỏ |
| 10 | bỏ vế cụt + tách câu tìm gộp, so với bản đang chạy (lượt ba bên: ba bản chạy cùng lúc trên cùng bộ tin; bên thứ ba thêm bước viết lại của bài 21, bản đầu của bước viết lại) | tin của gia đình × 6 mỗi bên + tin nhiều ý khác, tin kho thiếu, tin thường (57 câu); Claude Sonnet 5.5; 22/11 | đoạn giá vé Đại Nội vào bằng chứng 2 · 6 · 6 trên 6; "Thử lại" 5 · 3 · 0; đủ cả hai ý 0 · 1 · 1; nguồn trung vị 20 ⇒ 16; tin khác không lỗi, không bịa | **giữ** (mở cùng bộ) |
| 11 | thêm trần tìm 3 lên trên dòng 10 | tin của gia đình × 6 (9 câu); Claude Sonnet 5.5; 22/11 | đủ cả hai ý 6 / 6, không "Thử lại", chậm thêm khoảng 2 giây | **giữ** (mở 14:47 22/11) |
| 12 | nhớ câu trả lời liền trước cả trong cuộc đã lập lịch, so với cả cuộc không nhớ | chuỗi "Kể các quán chè ở Huế" ⇒ "Bỏ quán đầu đi rồi viết lại danh sách" × 3, trong cuộc đã lập lịch; 9 lượt thật; Claude Sonnet 5.5; 22/11 (một phiên chạy, một phiên đọc code, phiên đo chấm) | lịch không đổi 3 / 3; bỏ đúng quán đầu và đủ các quán còn lại 3 / 3 (2 lần khớp đúng danh sách cũ, 1 lần thêm một mục có nguồn — người chấm ghi: đọc chặt tiêu chí thì lần đó không đạt; không lần nào là danh sách sai); bên tắt: câu "không xác định được quán đầu"; lệnh "Bỏ Chùa Thiên Mụ đi" sau đó vẫn sửa lịch đúng một lần. Trên trình duyệt 22/11, một cuộc sáu tin: danh sách quán 5 còn đúng 4, danh sách điểm miễn phí bỏ đúng điểm đầu còn đủ 7, lịch đứng yên; hai lệnh sửa thật đổi lịch đúng | **giữ** (nhóm đã chốt mở 16:08 22/11) |

**Đọc bảng thế nào.** Dòng 1–3 là ba bước nới dần phần nhớ: câu hỏi, rồi tên nơi, rồi một câu trả lời. Mỗi bước chỉ thêm đúng thứ đã thấy thiếu. Dòng 5 và 7 cho cùng một bài học: muốn sửa tin nhiều ý thì sửa ở chỗ chương trình quyết (đếm vế, tìm theo vế), không nới lời dặn cho mọi tin.

**Giới hạn của các phép đo.** Bộ nhỏ (4 tới 17 chuỗi, 8 tới 11 tin), phần lớn do nhóm soạn. Dòng 1, 2, 5 đo với gpt-6-luna, chưa đo lại trên Claude. Dòng 3 và 7 chưa đo trên gpt-6-luna. Dòng 7 mới đo với tin gửi như tin đầu cuộc; lượt giữa cuộc có lịch sử chưa đo. Dòng 10–11: lợi mới đo trên MỘT tin dài; chính bản đang chạy với tin đó trong ngày tự dao động 3, 4, 5 lần "Thử lại" trên 6, nên căn cứ mở là cơ chế (đúng đoạn vào bằng chứng), không phải "giảm lỗi"; các tin dài khác của lượt đo không có câu tìm gộp; cuộc đã có lịch lưu và model cũ chưa đo. Dòng 12: một chuỗi tin, 3 lần; mỗi chuỗi trên trình duyệt chạy một lần; model cũ chưa đo.

## Quyết định nhỏ hơn

**Vì sao lần tìm đầu không ghép câu hỏi trước?** Lần tìm đầu chỉ dùng câu gõ; tên của lượt trước vào câu tìm qua model, ở lần tìm thêm. Chưa thấy ghi lý do cho riêng lần tìm đầu. Điều thấy được: khi sửa câu tra web (15/11), cách ghép câu trước với câu sau bằng chương trình làm hỏng 2 trên 3 cặp người dùng đổi chủ đề thật. Cách khác: ghép bằng chương trình cho lần tìm đầu trong kho: chưa thử; cho model viết lại câu tìm trước lần tìm đầu (3 cách): đã đo, chỉ thêm 0–1 trên 12 câu đủ từ khoá (cần ít nhất 3), bỏ. Cái giá: tin nối tiếp tốn thêm một vòng model.

**Vì sao chạy lại đúng một lần, chỉ ở lượt đang mang câu trả lời cũ?** Giảng đủ ở bài 16, quyết định 4. Tóm lại: chạy lại cả lượt một lần, không kèm câu trả lời cũ, khi lượt bị rút vì bất kỳ phép kiểm nào sau khi viết; chỉ ở ô chat (đường gửi chữ từng mảnh mà giao diện dùng, kể cả với Claude, dù cả câu tới trong một mảnh); lượt có câu cố định và lượt sửa lịch thì không (cuộc có lịch lưu: trước 16:08 22/11 không chạy lại; từ đó chạy lại câu hỏi thường, lần hai đi thẳng đường trả lời thường, không hiểu ý sửa lịch lần nữa). Lượt mà bước viết lại của bài 21 đã xử lý (ra câu viết lại hoặc câu từ chối) thì không cần chạy lại, vì bước viết lại chạy trước. Lý do: lỗi do chính câu trả lời cũ gây ra; bỏ nó đi thì lần hai tệ nhất cũng bằng lúc chưa giữ câu trả lời. "Giữ chữ tới khi kiểm xong" lúc đó không chọn vì nó đổi cách hiện chữ của mọi tin nối tiếp (từ 15:42 22/11 đã làm riêng cho model đang chạy; bài 6, quyết định 4); nới bước kiểm cho câu chép lại: không làm. Cái giá: gấp đôi lần gọi model, chờ thêm khoảng 5 giây (dòng tiến độ lặp lại một nhịp); đo lại 5 lần: 0 màn hình lỗi, chạy lại thật 2 lần, cả hai ra câu trả lời.

**Vì sao mở việc nhớ câu trả lời liền trước cả trong cuộc đã lập lịch, mà vẫn chặn lượt sửa lịch?** Đã chọn: từ 16:08 22/11, trong cuộc đã lập lịch, câu hỏi thường được nhớ câu trả lời liền trước và được chạy lại một lần khi bị rút; lượt thật sự sửa lịch và câu trả lời có trích nguồn của lịch thì không. Vì sao: lỗi thấy thật chiều 22/11 — trong cuộc đã lập lịch, "Kể các quán chè ở Huế" rồi "Bỏ quán đầu đi rồi viết lại danh sách" chỉ nhận câu "không xác định được quán đầu", vì việc nhớ đã tắt ngầm cho cả cuộc; mà lập lịch rồi hỏi tiếp có trong danh sách chủ dự án tự thử ngày 23/11 (nhóm soạn). Chặn lượt sửa lịch vì chữ của lượt đó do chương trình dựng; câu hỏi về lịch mà chỉ trích bài kho thì vẫn được nhớ, không sinh câu trả lời cũ sai, vì lịch chỉ đổi qua một lượt sửa, và lượt sửa làm rơi câu trả lời đã nhớ (chú thích trong chương trình). Cách khác: để tắt như trước 16:08 — đã đo cùng chuỗi (dòng 12), bỏ. Cái giá: lượt "viết lại danh sách" lâu và tốn hơn, danh sách dài có thể thiếu mục ("Giới hạn đã biết"); nhóm đã chốt mở.

**Vì sao tách câu tìm gộp bằng luật chữ, không nhờ model tách hay dặn model viết câu tìm một ý?** Ghi trong chương trình: cắt hỏng (vị ngữ rơi sang phần kia) chỉ tốn vài đoạn thừa, vì lần tìm cả câu vẫn chạy nguyên như cũ; không thêm lần gọi model. Nhờ model tách hay dặn thêm: chưa thử.

**Vì sao nối thêm 2 đoạn mỗi vế, không chia lại 10 đoạn?** Giữ nguyên 10 đoạn của cả tin, nối 2 đoạn đầu của mỗi vế, nhiều nhất 6 vế. Bản được giao ban đầu "4 đoạn của cả tin + 2 đoạn mỗi vế" đã đếm và bỏ: nó làm mất đoạn đang dùng ở 3 trên 13 tin. Đếm 0 đồng: 2, 3 hay 4 đoạn mỗi vế cho cùng kết quả; 6 là số vế nhiều nhất trong 65 tin nhiều ý đã ghi. Lượt thật (dòng 7 của "Đã so"): 3 trên 24 thành 15 trên 24, 6 tin khác không mất dữ kiện đang đúng. Cái giá: chờ thêm 0,75 giây ở câu đứng giữa; tổng số dòng ý thiếu gần như không đổi (24 xuống 21).

**Vì sao lịch sử nằm ở máy chủ, không để trình duyệt gửi lại?** Kế hoạch phần nhớ ghi: trình duyệt gửi lại lịch sử thì trình duyệt sửa được "trợ lý đã nói…", tức thành chỗ cài lệnh vào lời gọi model; không chọn. Cái giá: khởi động lại máy chủ là mất (bài 6).

**Vì sao lượt lỗi, lượt bị ngắt, lượt bị rút không được ghi vào lịch sử?** Kế hoạch phần nhớ ghi: lượt lỗi / ngắt không lưu; câu cố định (từ chối, ngoài phạm vi) thì lưu để lượt sau hiểu mạch. Nhờ vậy bấm "Thử lại" là hỏi lại như lượt đó chưa từng có. Cái giá: lượt bị ngắt mất khỏi ngữ cảnh của lượt sau.

## Giới hạn đã biết

- **Chỉ nhớ câu trả lời LIỀN TRƯỚC.** Tin trỏ theo thứ tự vào câu trả lời của hai lượt trước không hiểu được; dòng ghi chú tên nơi tự khai "không theo thứ tự trong câu trả lời". Chuỗi "kể quán ⇒ quán thứ hai ở đâu ⇒ viết gọn lại ⇒ còn quán thứ ba?" thì tin cuối trả lời đúng chỗ một phần nhờ may.
- **Nhờ "viết lại danh sách" thì trợ lý tra kho lại và viết lại từng mục**, không chỉ xoá một dòng: lượt đó mất khoảng 17–24 giây (trên trình duyệt 22/11: 17,3 và 24,1 giây; lượt thật: 19–20 giây, khoảng 0,13–0,17 USD; bên không nhớ: 10–12 giây cho một câu "không xác định được"). Danh sách DÀI có thể thiếu mục: một lượt thử 8 điểm, bỏ 1, chỉ còn 4 — trợ lý nói rõ nó chỉ giữ điểm tìm lại được nguồn, câu đó có thể bị đọc nhầm thành "ba điểm kia chưa chắc miễn phí"; lần nhìn trên trình duyệt thì còn đủ 7.
- **Lệnh sửa lịch mơ hồ nay thành câu hỏi thường** (rào của bài 31): "Bỏ điểm này", "Bớt lăng đi", "Bỏ điểm đầu tiên đi" không sửa lịch; muốn sửa thì nhắn kèm tên điểm hoặc "của ngày 2" / "khỏi lịch".
- **Lúc chờ ở tin dài chỉ có một dòng trạng thái đứng yên, 20–30 giây** (giá của việc giữ chữ tới khi kiểm, bài 16). Ý "đổi dòng theo từng lần tìm" đã ghi, chưa làm.
- **Lần chạy lại trong cuộc đã lập lịch mới có ca test**, chưa có lượt thật nào trúng.
- **Nơi chỉ được nêu qua một bài tổng hợp** (cẩm nang) không có trong dòng ghi chú tên nơi.
- **Vế bị tách ra có thể mất tên nơi** ("có bậc nhiều không?"): đã gặp ⇒ đã chữa. Đếm trưa 22/11: 327 trên 1.240 vế tìm (26 %) không có chủ thể, 65 % tin nhiều ý có ít nhất một vế như vậy, đọc tay 20 trên 28 đoạn chúng kéo về không liên quan. Từ 14:47 ngày 22/11 vế cụt không được tìm riêng (chưa có số đếm lại sau khi mở). Còn lại: thứ vế cụt thật sự hỏi không được tìm riêng; dưới 2 % số vế bị lọc là lọc oan ("mai mưa thì đi đâu trong nhà"); một ô của phép đo sáng 22/11 từng được cứu nhờ một đoạn không liên quan do vế cụt kéo về, lọc thì mất ô đó.
- **Câu tìm gộp được tách bằng luật chữ** ("và", ";", "+"). Đếm trên các câu tìm model đã viết: 231 trên 396 (58 %) là câu gộp; trong 32 câu gộp về vé Đại Nội, đoạn có giá vào kết quả 16 câu khi để nguyên, 27 câu khi nối thêm theo phần, không câu nào mất; mỗi lần tìm dài thêm khoảng 2 đoạn (10 lên 12). Cắt bằng luật: cắt hỏng chỉ tốn vài đoạn thừa, lần tìm cả câu vẫn chạy như cũ. Một phiên khác đếm trên 1.116 câu tìm của model: 41 % là câu gộp, 6 % số phần tách ra là mẩu cụt.
- **Câu phải gom nhiều bài để so** ("lăng nào ít leo bậc") không được tìm theo vế cứu: 0 ⇒ 1 trên 13 tin.
- **Người dùng không được báo khi máy chủ đã quên** (quá 30 phút, máy chủ khởi động lại).

## Chi tiết để tra

- Luật đếm vế: tách ở dấu phẩy, chấm phẩy, dấu hỏi, rồi ở "và / còn / với"; một phần là một vế khi chính nó có từ hỏi hoặc kết thúc bằng "không / chưa / nhỉ / vậy / hả". *"Bún bò và bánh khoái giá bao nhiêu"* vẫn là một vế. Vế cụt bị bỏ khỏi lần tìm riêng; vế có chủ thể, kể cả một từ như "taxi", "chợ đêm", vẫn được tìm. Câu tìm gộp được cắt ở "và", dấu chấm phẩy, dấu cộng; nhiều nhất 3 phần.
- Ví dụ của tìm theo vế: vế "con trưởng vua Tự Đức có nối ngôi không" trong một tin hỏi về lăng Khải Định trước nhận dòng ý thiếu, nay được trả lời từ đoạn của chính vế đó.
- Tin 4 ý của gia đình (gốc của hai sửa 14:47 22/11): tổng vé Đại Nội + Tự Đức, bà có được giảm không, điểm nào ít bậc. Câu tìm gộp của model không kéo được đoạn giá vé, nên model tiêu 2–3 lần tìm vào cùng giá vé, hết lượt rồi nộp chữ giữ chỗ (bài 21); còn vế cụt kéo về phần lớn đoạn không liên quan.
- Quyết định 4, hai cách khác: bảng từ xưng hô ("bà" ⇒ "người cao tuổi"): chưa viết. Vế là lời nhờ không có từ hỏi ("chọn giúp 1–2 điểm ít bậc"): đã viết, để tắt, chỉ chạm 4 trên 364 tin.
- Tin nối tiếp: lần tìm đầu bằng câu cụt trượt 6 trên 7 cặp; model xin tìm thêm bằng câu có tên nơi 9 trên 9 lần (dựng lại 15/11, gpt-6-luna).
- Tin nhiều ý được đếm bằng một luật; vế để TÌM thì được tách bằng luật rộng hơn: cắt cả ở dấu chấm, chấm than, xuống dòng; nhận từ hỏi gõ tắt ("ko", "bn", "j"); bỏ vế ngắn dưới 8 ký tự; bỏ vế trùng. Lý do ghi trong chương trình: nhận nhầm một vế chỉ tốn hai đoạn thừa, bỏ sót một vế là mất đoạn của vế đó.
- Tìm theo vế chỉ chạy khi lần tìm chính có ít nhất một nguồn; không có thì giữ đường từ chối cũ.
- Đoạn của các vế được xếp xoay vòng: đoạn đứng đầu của mọi vế trước, rồi tới đoạn thứ hai; hai vế ra cùng một đoạn thì chỉ đưa một lần.
- Thời gian tìm khi có tìm theo vế: 36 lên 143 mili giây (đếm 0 đồng 21/11 trên 65 tin nhiều ý); trung vị thêm 6 đoạn, nhiều nhất 10.
- Với tin nhiều ý, khi mục web có mở (cả câu bị từ chối), câu gửi dịch vụ tìm web vẫn là câu gõ, không phải câu tìm cuối của model (bài 25).
- Model viết câu trả lời "phần tìm được + câu từ chối chuẩn ở cuối" thì chương trình gỡ câu từ chối ở cuối, giữ phần có nguồn (thấy 1 trên 3 lượt của một câu ngày 21/11).
- Đếm ngày 20/11 trên 122 lượt hỏi tiếp của sổ lượt (kịch bản của nhóm): 6 lượt trỏ vào nội dung câu trả lời trước; dòng ghi chú tên nơi có mặt ở 58 lượt.
- Cùng một lần dựng lại (15/11), với 7 cặp mà kho có điều được hỏi, 7 trên 7 tin hỏi tiếp được trả lời đúng nơi (gpt-6-luna).
- Đường hỏi đáp không hiện chữ dần (giao diện không dùng) không có lần chạy lại.
- Hai yêu cầu cùng một cuộc chạy song song thì lượt xong sau ghi sau; không có khoá, vì một cuộc là của một người.

**Bài sau (bài 24):** việc phải đúng thì chương trình tính: ngày âm lịch làm mẫu, rồi thời tiết, khoảng cách và các công cụ khác.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Ví dụ "áo dài" (3 vòng, 7,5 giây, nguồn [25]): `data/hoc_cung_D/vi_du_tim_them_vet.json` [riêng tư; đã chạy 20/11, gpt-6-luna]; giảng kỹ ở bài 21.
- Kho nhớ: `backend/api/conversations.py` (`TTL_SECONDS`, `MAX_CONVERSATIONS`, `MAX_TURNS`, `NHAN_LOI_TRUOC` nguyên văn, `CAT_LOI_TRUOC` và chú thích 1.200 ⇒ 4.000, `stored_answer`, `CONG_CU_KHONG_NHO_DAP`, `dap_duoc_nho` và chú thích 8 / 10 ↔ 0 / 6, `append` "không còn trần token của lịch sử (User 19/11/2026)", `history_khong_dap`) [code, đọc 22/11]. Chú thích đầu file vẫn ghi "≤ 1.500 token" — đã cũ so với `append`. Dựng kho với `keep_answers=False, chi_dap_lien_truoc=flags.nho_cau_tra_loi`: `backend/api/app.py` [code].
- Ghi lượt, đặt lịch sử, lịch sử để lùi: `backend/api/routes/chat.py` (`_start_conversation`, `_remember`, `REMEMBERED_OUTCOMES`, cookie HttpOnly / SameSite=Strict / path `/api`, `_set_cookie`) [code].
- Dòng ghi chú tên nơi, 5 tên, bỏ ở câu xin liệt kê lại và câu gõ lại: `backend/llm/ten_goi_y.py` (`TIEN_TO_GHI_CHU`, `TOI_DA`, `ghi_chu_goi_y`, `lich_su_cho_luot`, `la_cau_go_lai`) [code].
- Lịch sử thành các tin user / assistant: `backend/llm/generator_openai_full_corpus.py` `with_history`; bộ xếp loại nhận lịch sử + `ROUTER_HISTORY_NOTE`; trợ lý nhận `ASSISTANT_HISTORY_NOTE` nguyên văn: `backend/llm/full_corpus_prompt.py` [code]. Lần tìm đầu dùng `trace.search_query or query`: `backend/llm/assistant.py` `prepare_answer`; cổng công cụ xét câu liền trước: `_lich_extra`, `nl.co_tu_ngay_luot`, `tt.co_tu_khoa_luot` [code].
- Tải lại trang: `frontend/src/chat.jsx` (gọi `/api/conversation/new` lúc nạp, `resetting` khoá nút Hỏi) [code]; 3 / 3: `bai_hoc/13_TIM_THEM_VA_NHO_CAU_HOI.md` mục "Tải lại trang…" (nguồn gốc `report_agent/2026-11-12_ra_khoang_cach/c_f5_cuoc_moi_implementation.md`) [đã chạy 15/11].
- Câu cụt trượt 6 / 7, 9 / 9 câu tìm có tên nơi, 7 / 7 đúng nơi, ghép bằng chương trình phá 2 / 3 cặp đổi chủ đề (đo cho câu tra web): `bai_hoc/15_TRA_WEB_VA_HOI_BANG_ANH.md` "Chuyện thật thứ ba" [đã chạy 15/11, gpt-6-luna; chép].
- Ví dụ "quán thứ hai" (8,8 ⇒ 3,9 giây), 24 lượt 0 lỗi, khoảng 400–500 token thêm: `bai_hoc/VIEC_MOI_XONG.md` mục 35; dòng `nho_cau_tra_loi` của `backend/config/settings.yaml` [đã chạy 22/11, Claude Sonnet 5.5; chép]. 3 / 122 lượt, 6 lượt trỏ, 58 / 122 có ghi chú, "bắt buộc (hỏi + đáp)" của chủ dự án 02/11: `report_agent/2026-11-20/b_nho_cau_tra_loi_plan.md` mục 2–3 [đã chạy 20/11, đếm 0 đồng].
- Lần chạy lại: `backend/llm/assistant.py` `answer_turn_stream_parallel` (chú thích đầu hàm), `TEN_CHAY_LAI`; 3 / 7 ⇒ 0 / 5, 2 / 5, chậm khoảng 5 giây, đường "giữ chữ" không chọn, 5 / 72: `report_agent/2026-11-22/b_nho_dap_chay_lai.md` mục 1, 2, 4, 5 [đã chạy 22/11; người thứ hai kiểm].
- Số của nhớ câu hỏi / nhớ cả ba lượt (03/11): `report_agent/2026-11-20/b_nho_cau_tra_loi_plan.md` mục 1 (nguồn gốc `bao_cao_he_thong/07_BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `report_agent/2026-11-02_phase_9_code/b138_b3b_implementation.md`) [đã chạy; chép]. Nhớ tên nơi 15 / 17 ↔ 2 / 17: dòng `nho_ten_goi_y` của `settings.yaml` [đã chạy 19/11].
- 3 lượt = "6 tin — roadmap 4–6", 30 phút theo spec, 500 cuộc: `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` dòng 40, 49 [kế hoạch]. Gỡ trần token theo "chất lượng trước": chú thích `append` + `bai_hoc/VIEC_MOI_XONG.md` mục 9.
- Tin nhiều ý: đếm vế `so_y`, `_VE_HOI`, `_CUOI_HOI`, `_LIEN_TU`; chốt `chi_y_thieu`, `bo_cau_tu_choi_cuoi`; cổng web `web_gate_open` + `web_chi_khi_tu_choi`; tìm theo vế `cac_ve_tim`, `SO_DOAN_MOI_VE`, `TRAN_SO_VE_TIM` (chú thích 65 tin, 2 / 3 / 4 đoạn, 1 / 8 ⇒ 3 / 8 ⇒ 5 / 8), `search_into_trace` (`ve_them`, xoay vòng `zip_longest`): `backend/llm/assistant.py` [code]. Lời dặn theo ý nguyên văn: `backend/llm/full_corpus_prompt.py` `_LUAT_NHIEU_Y`, `CAU_Y_THIEU` [code].
- Số tin nhiều ý 14/11 (4 / 10, vòng 1, vòng 2, chủ dự án chọn bật; 1 / 2 lần từ chối cả câu ở tin "bao xa, rồi ghé…"): `bai_hoc/25_TRO_LY_LAM_VIEC_THAT.md` mục 2; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 [đã chạy, gpt-6-luna; chép]. Web chỉ khi từ chối (11 / 11 ⇒ 0 / 11, 5,8 giây, 1 / 66): `bai_hoc/VIEC_MOI_XONG.md` mục 29 [đã chạy 21/11, Claude]. Tìm theo vế (86 %, một phần tư tới một phần ba, 3 / 24 ⇒ 15 / 24, 9 / 18, 24 ⇒ 21, 13,85 ⇒ 14,6, 36 ⇒ 143 ms, bản 4 + 2 bỏ, 0 ⇒ 1 / 13, ví dụ vua Tự Đức): `report_agent/2026-11-22/b_tim_theo_ve.md` mục 1–5, `bai_hoc/VIEC_MOI_XONG.md` mục 38 [đã chạy 21–22/11, Claude; người viết báo cáo tự đọc tay, chưa người thứ hai].
- Câu hỏi tự kiểm: thêm theo khuôn chủ dự án chọn trưa 22/11; đáp án chỉ nhắc lại nội dung bài.
- Cuộc có lịch lưu: trước 16:08 22/11 không nhớ câu trả lời (`assistant.py` `_before_model`: `lich_vao_hoi_thuong` ⇒ `_nguon_lich_dang_co` thêm mục `lich_dang_co`; `conversations.py` `CONG_CU_KHONG_NHO_DAP`). Từ 16:08 22/11 (`nho_dap_cuoc_co_lich: true`, `backend/config/settings.yaml` dòng 76 và chú thích): `backend/api/conversations.py` dòng 53–72 `dap_duoc_nho(…, mo_cho_cuoc_co_lich=…)` — chỉ chặn lượt có hành động sửa / khẩn cấp và câu trả lời trích `NGUON_LICH_SOURCE`, bỏ `lich_dang_co` khỏi danh sách chặn; gọi từ `backend/api/routes/chat.py` dòng 229; chạy lại: `assistant.py` dòng 2114–2131 (không chạy lại khi `trace.sua_chon` hoặc `n_hanh_dong`; lần hai `_answer_core`, không gọi lại bước hiểu ý sửa lịch); test `backend/tests/test_nho_dap_cuoc_co_lich.py` (không chạy) [code, mở 16:49 22/11]. Lý do mở và "đúng cách chủ dự án định thử": `bai_hoc/VIEC_MOI_XONG.md` mục 44 ý 1 ("đúng kiểu anh sẽ demo") [chép]. Số 9 lượt thật, bốn giới hạn (a)–(d): `guides/RUNBOOK_BAN_GIAO.md` mục 10.2 hàng `nho_dap_cuoc_co_lich` ( nguồn gốc `data/thu_bedrock_2026-11-21/k10_cuoc_co_lich_2026-11-22/thu_lai_KET_QUA_SO_MAY.md`, `thu_lai_CHAM_E.md` [riêng tư, chưa mở]) [đã chạy, phiên khác; chép]. Trên trình duyệt 16:17–16:21 22/11 (cuộc sáu tin; 17,3 và 24,1 giây; chuỗi "quán thứ ba" nhờ may; dòng trạng thái 20–30 giây; lệnh mơ hồ): `bai_hoc/VIEC_MOI_XONG.md` mục 44 (dòng 19–45); `data/test_cuoi/chay_2026-11-22_e_nhin_gom/KET_QUA.md` [riêng tư, chưa mở; đã chạy, phiên đo]. Lần chạy lại chỉ ở đường stream, điều kiện `trace.citation_error`, tiền hai lần: `answer_turn_stream_parallel`; `answer_turn` không có [code].
- Dòng 8, 9 của "Đã so": `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng 34, 43 [chép]. Lịch sử ở máy chủ, lượt lỗi không lưu: `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` D1 (dòng 44), D2 (dòng 47) [kế hoạch]; trần 1.500 chưa từng chạm (lớn nhất 105): `bai_hoc/VIEC_MOI_XONG.md` mục 9 [chép].
- Bài đã qua một lượt đối chiếu độc lập với chương trình và số đo ngày 22/11 (36 dòng: 3 lệch, đã sửa): `data/hoc_cung_D/kiem/bai_23_26.md` [riêng tư].
- Đã qua một lượt kiểm chéo sau lượt cập nhật 14:47 (`data/hoc_cung_D/kiem/cap_nhat_14h47.md`) [riêng tư]. Theo đó: dòng Nếu của tin dài sửa điều kiện ("đã tự tìm ít nhất một lần"), thời gian (25–37 giây khi viết lại) và thứ người dùng thấy (chữ giữ chỗ khoảng 15–17 giây — `bai_hoc/VIEC_MOI_XONG.md` mục 42, đính chính 15:14; runbook 10.1 hàng "Lưới viết lại"; suy từ chương trình và sổ máy chủ, chưa chụp màn hình). Cắt nửa để hiểu: quyết định 2 (lần tìm đầu không ghép) và 4 (chạy lại) cũ chuyển xuống "Quyết định nhỏ hơn"; đoạn chạy lại và đoạn "Hai sửa sau…" rút còn cơ chế, số ở "Đã so" dòng 10–11 và "Giới hạn đã biết"; câu hỏi tự kiểm về lần chạy lại bỏ (bài 16 có). Thêm: cách khác "lời nhờ không có từ hỏi" (`VIEC_MOI_XONG.md` mục 42 ý 3: 4 / 364 tin), quyết định nhỏ "tách bằng luật chữ" (chú thích `cac_phan_cau_tim`).
- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 (hàng "Vế tìm cụt bị lọc…", "Tin DÀI nhiều ý"); `backend/config/settings.yaml` (`tim_ve_bo_cut`, `tach_cau_tim_model`, `so_lan_tim_kho: 3` và chú thích) [code; số đo: đã chạy, phiên đo; người viết không chạy lại]. Luật vế cụt: `backend/llm/assistant.py` `_ve_cut`, `_TU_DEM_VE`, `_TU_CHUNG_VE`, `_CHU_DE_VE`, `cac_ve_tim(query, flags.tim_ve_bo_cut)`; tách câu tìm: `cac_phan_cau_tim`, `_NOI_CAU_TIM`, `TRAN_PHAN_CAU_TIM = 3`, `search_into_trace` (phần của câu tìm model vẫn được tìm khi cả câu không mang đoạn mới) [code]. Số 327 / 1.240, 65 %, 20 / 28, 231 / 396, 16 ⇒ 27 / 32, 1.116 câu (41 %, 6 %), 2 ⇒ 6 / 6, 20 ⇒ 16, ô "17h30", lọc oan dưới 2 %, ghép chủ thể 6 · 12 · 2 / 20: `VIEC_MOI_XONG.md` mục 42 ý 2–3; runbook 10.1; chú thích `tim_ve_bo_cut` trong `assistant.py`; `data/review_khac_hang/2026-11-22_moc_sang/c_dem/KET_QUA_DEM.md` [riêng tư, chưa mở; chép qua runbook].

- "Đường chữ hiện dần" đổi thành "ô chat (đường gửi chữ từng mảnh)" và thêm "lượt có câu cố định" cho khớp bài 16: `backend/llm/assistant.py` `answer_turn_stream_parallel` (lúc 15:18: điều kiện `trace.fixed_outcome is not None or trace.lich_luu is not None` ⇒ không chạy lại; từ 16:08 22/11 vế `lich_luu` chỉ còn chặn khi tính năng `nho_dap_cuoc_co_lich` tắt hoặc lượt là lượt sửa lịch — `assistant.py` dòng 2125–2131); đường không stream `/api/chat` giao diện không dùng: `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 [code + chép, 15:18 22/11/2026].

- Giữ chữ tới khi qua bước kiểm nguồn (mở 15:42 22/11/2026; đoạn chữ giữ chỗ không còn hiện ở lượt viết lại): `backend/config/settings.yaml` dòng `giu_chu_toi_kiem`; runbook 10.1 hàng "Lưới viết lại" [code + chép; lượt thường đã nhìn trên trình duyệt 22/11, ca viết lại chưa trúng — runbook dòng 329].

</details>
