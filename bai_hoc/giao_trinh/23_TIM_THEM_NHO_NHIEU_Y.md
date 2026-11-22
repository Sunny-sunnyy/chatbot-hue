# Bài 23 — Tìm thêm, nhớ câu hỏi trước, và câu hỏi nhiều ý

*Cập nhật 12:54, ngày 22/11/2026 · sửa theo một lượt đối chiếu độc lập · cơ chế đọc từ chương trình và cấu hình đang chạy trưa 22/11; số đo chép từ các báo cáo 03/11 – 22/11, ghi rõ model ở từng con số (tới trưa 21/11 là gpt-6-luna, sau đó là Claude Sonnet 5.5); người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** harness (bài 21): model được tự tìm kho thêm tối đa 2 lần; bước xếp loại câu (bài 22) chọn tuyến cho từng tin.
**Bài này thêm:** hai loại tin mà tìm một lần bằng chính tin đó là không đủ: tin nối tiếp ("còn chỗ đó thì sao?") và tin hỏi nhiều điều một lúc. Hệ thống nhớ gì, ai dùng phần nhớ đó, và tin nhiều ý được xử lý ra sao.

## Ý chính

- 10 đoạn ở lần tìm đầu; trợ lý được tìm thêm tối đa 2 lần bằng câu tìm model tự viết (bài 21). Cả bài dựa trên quyền đó.
- **Máy chủ nhớ 3 lượt gần nhất** của một cuộc trò chuyện, trong 30 phút. Lượt cũ được gửi lại dưới dạng câu hỏi; riêng lượt liền trước kèm câu trả lời (bỏ số nguồn, cắt 4.000 ký tự, có nhãn "không phải nguồn").
- **Lịch sử chỉ để hiểu câu hỏi nói về cái gì**, không làm nguồn. Lần tìm đầu vẫn dùng đúng câu gõ; model đọc lịch sử rồi tự viết câu tìm có tên đối tượng.
- Lượt mà lịch sử gửi kèm có câu trả lời liền trước, nếu bị rút ở bước kiểm sau khi viết, thì **chạy lại đúng một lần** không kèm câu trả lời đó (ở đường chữ hiện dần mà giao diện dùng).
- **Tin nhiều ý** (chương trình đếm được từ hai vế hỏi): trả lời ý kho có, ghi "Tư liệu chưa có thông tin về: …" cho ý thiếu; từ 22/11 mỗi vế được nối thêm 2 đoạn, nhiều nhất 6 vế.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| mã cuộc trò chuyện | **conversation id** (cất trong **cookie**) | chuỗi ngẫu nhiên máy chủ đưa trình duyệt cất; trình duyệt gửi kèm mỗi câu hỏi để máy chủ biết câu đó thuộc cuộc nào |
| lịch sử | **history** | phần cuộc trò chuyện được gửi kèm cho model ở lượt mới |
| vế hỏi | — | một câu hỏi con trong tin, có từ hỏi riêng ("bao nhiêu", "ở đâu", "không"…) |
| dòng ý thiếu | — | dòng mở đầu bằng "Tư liệu chưa có thông tin về:" model viết cho vế kho không có |

## Tìm thêm là chỗ dựa: ba điều cần mang theo từ bài 21

Ví dụ "phải tìm thêm" (*"Mặc áo dài vào Đại Nội có được miễn vé không?"*): model xin tìm hai lần bằng câu tự viết rồi trích đoạn số 25, đoạn chỉ có nhờ lần tìm thứ hai (lượt thật 20/11, gpt-6-luna, 7,5 giây). Ba điều dùng lại ở dưới:

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

Cuộc giữ 3 lượt; 30 phút không hỏi thì bị xoá. **Không giữ câu trả lời** của câu cố định (từ chối, ngoài phạm vi, hỏi lại), lượt lịch và sửa lịch, và lượt dùng nguồn đổi theo giờ: thời tiết, ngày và âm lịch, sự kiện theo ngày, khoảng cách. Cuộc đã có lịch lưu từ trang Lên kế hoạch thì mọi lượt hỏi thường đều mang nguồn "lịch bạn đang có", nên cũng không được giữ câu trả lời.

Ví dụ đo 22/11 (Claude Sonnet 5.5): *"Kể cho mình ba quán cơm hến hoặc bún hến ở Huế"* rồi *"quán thứ hai bạn vừa kể ở đường nào, mở mấy giờ?"*. Không có câu trả lời cũ: trợ lý không xác định được quán thứ hai. Có nó: nêu đúng quán và đường, trích nguồn của lượt mới, nhanh hơn (8,8 xuống 3,9 giây).

## Lịch sử giúp hiểu câu hỏi, không làm nguồn

| Chỗ trong một lượt | Dùng lịch sử thế nào |
|---|---|
| xếp loại câu (bài 22) | thấy lịch sử, kèm câu dặn "chỉ chọn tuyến cho tin nhắn cuối cùng" |
| lần tìm đầu | **không dùng**: chỉ câu gõ |
| chọn công cụ đưa cho model (bài 24) | xét câu gõ **và câu hỏi liền trước**: "còn tuần sau thì sao?" sau một câu thời tiết vẫn có công cụ thời tiết |
| model trả lời | thấy lịch sử, kèm một đoạn dặn: câu tìm thêm phải nêu đúng tên đối tượng lấy từ các lượt trước; mỗi nhận định phải lấy từ bằng chứng nói đúng về đối tượng đó |

Vì vậy tin nối tiếp thường cần thêm một lần model xin tìm kho, nên chậm hơn tin đầu: lần tìm đầu bằng câu cụt thường trượt (dựng lại 15/11, gpt-6-luna: 6 trên 7 cặp), model xin tìm thêm bằng câu có tên nơi (9 trên 9 lần đúng tên). Luật "lịch sử không làm nguồn" được giữ bằng bước kiểm số nguồn (bài 16): câu trả lời cũ đã mất hết số nguồn.

## Câu trả lời được nhớ có một tác dụng phụ: chạy lại đúng một lần

Trợ lý vừa kể một lộ trình hai ngày bằng chữ, người dùng gõ *"Bỏ Chợ Đông Ba đi"*. Từ khi giữ câu trả lời liền trước (sáng 22/11), model có lúc chép lại lộ trình cũ mà không trích nguồn nào. Bước kiểm số nguồn rút câu đó, và người dùng nhận màn hình lỗi ở 3 trên 7 lần đo. Cách sửa không nới bước kiểm: lượt mà lịch sử có câu trả lời cũ, nếu bị rút ở bước kiểm sau khi viết (vì số nguồn hay phép kiểm khác), thì chương trình gỡ chữ vừa hiện, chạy lại cả lượt **một lần** với lịch sử không có câu trả lời cũ, lấy kết quả lần hai; tiền tính cả hai lần. Lần hai cũng bị rút thì báo lỗi như cũ. Đo lại 5 lần (Claude Sonnet 5.5): 0 màn hình lỗi; chạy lại thật 2 lần, cả hai ra câu trả lời; dòng tiến độ lặp lại một nhịp, chờ thêm khoảng 5 giây.

## Tin nhiều ý được trả lời theo từng ý

Lời dặn gốc: bằng chứng không đủ thì trả một câu từ chối. Hỏi *"vé Đại Nội bao nhiêu, dịp Tết có chương trình gì?"* mà kho chỉ có giá vé thì mất luôn giá vé (14/11, gpt-6-luna: phần kho có được trả lời 4 trên 10 tin). Bốn bước hiện nay:

1. **Chương trình đếm vế**: tách ở dấu phẩy, chấm phẩy, dấu hỏi, rồi ở "và / còn / với"; một phần là một vế khi chính nó có từ hỏi hoặc kết thúc bằng "không / chưa / nhỉ / vậy / hả". *"Bún bò và bánh khoái giá bao nhiêu"* vẫn là một vế.
2. **Từ hai vế, model nhận lời dặn theo ý**: ý có bằng chứng thì trả lời; ý không có thì một dòng riêng mở đầu đúng bằng "Tư liệu chưa có thông tin về:", không số nguồn, không đoán.
3. **Chương trình chốt**: mọi dòng đều là dòng ý thiếu thì đổi cả câu về câu từ chối chuẩn, và chỉ lúc đó mới tra web (bài 25). Trả lời được một phần thì giữ dòng ý thiếu, không tra web.
4. **Tìm theo vế (từ 22/11)**: 10 đoạn của cả tin giữ nguyên; chương trình tìm riêng từng vế (nhiều nhất 6), nối 2 đoạn đầu mỗi vế vào sau. Model đọc khoảng 15 đoạn (10 cũ + trung vị 6 đoạn thêm); không thêm lần gọi model.

Bước 4 có vì một phép đếm tối 21/11 (Claude Sonnet 5.5): 86 % lượt nhiều ý có dòng ý thiếu, khoảng một phần tư tới một phần ba số dòng đó sai (kho có). Ví dụ: vế "con trưởng vua Tự Đức có nối ngôi không" trong một tin hỏi về lăng Khải Định trước nhận dòng ý thiếu, nay được trả lời từ đoạn của chính vế đó.

## Quyết định và lý do

### 1. Vì sao lịch sử chỉ mang câu trả lời của lượt liền trước?

- **Đã chọn:** chỉ câu trả lời của lượt liền trước; lượt cũ hơn còn câu hỏi và tên nơi.
- **Vì sao:** bản nhớ cả ba câu trả lời (03/11, gpt-6-luna) từng trả lời một tin ngoài kho bằng đoạn của đối tượng khác; sửa lời dặn xong, lợi vẫn chưa chắc (+0,50, khoảng tin cậy −0,15 tới +1,20). Đếm 20/11 trên 122 lượt hỏi tiếp của nhóm: thiếu câu trả lời cũ làm hỏng 3 lượt, cả ba trỏ vào câu trả lời vừa rồi.
- **Cách khác:** chỉ nhớ câu hỏi (03/11 – 22/11): đã đo, tin hỏi tiếp +0,80 [+0,25; +1,50] so với không nhớ, nhưng không hiểu "quán thứ hai". Nhớ ba lượt: đã đo, bỏ.
- **Cái giá:** lượt có lịch sử dài thêm khoảng 400–500 token; câu trả lời của hai lượt trước không còn.

### 2. Vì sao lần tìm đầu không ghép câu hỏi trước?

- **Đã chọn:** lần tìm đầu chỉ dùng câu gõ; tên của lượt trước vào câu tìm qua model, ở lần tìm thêm.
- **Vì sao:** chưa thấy ghi lý do cho riêng lần tìm đầu. Điều thấy được: khi sửa câu tra web (15/11), cách ghép câu trước với câu sau bằng chương trình làm hỏng 2 trên 3 cặp người dùng đổi chủ đề thật.
- **Cách khác:** ghép bằng chương trình cho lần tìm đầu trong kho: chưa thử. Cho model viết lại câu tìm trước lần tìm đầu (3 cách): đã đo, chỉ thêm 0–1 trên 12 câu đủ từ khoá (cần ít nhất 3), bỏ.
- **Cái giá:** tin nối tiếp tốn thêm một vòng model.

### 3. Vì sao lượt có thời tiết, ngày, khoảng cách không được giữ câu trả lời?

- **Đã chọn:** câu trả lời dùng nguồn đổi theo giờ không vào lịch sử.
- **Vì sao:** đo 21/11 (Claude Sonnet 5.5): hỏi tiếp về "con số khả năng mưa bạn vừa đưa" khi có câu trả lời cũ thì model tự từ chối 8 trên 10 lần, vì số đã nằm trong phần "không phải nguồn" nên nó không gọi lại công cụ; không có câu trả lời cũ: 0 trên 6. Luật ghi trong chương trình: số dự báo phải đến từ công cụ của lượt này.
- **Cách khác:** giữ cả câu có số dự báo: đã đo như trên, bỏ.
- **Cái giá:** hỏi tiếp về con số vừa đưa phải gọi lại công cụ, chậm hơn một vòng.

### 4. Vì sao chạy lại đúng một lần, và chỉ ở lượt đang mang câu trả lời cũ?

- **Đã chọn:** chạy lại cả lượt một lần, không kèm câu trả lời cũ, khi lượt bị rút vì bất kỳ phép kiểm nào sau khi viết; chỉ ở đường chữ hiện dần; cuộc có lịch lưu thì không.
- **Vì sao:** lỗi do chính câu trả lời cũ gây ra; bỏ nó đi thì lần hai tệ nhất cũng bằng lúc chưa giữ câu trả lời, và một lần thì không thể lặp mãi. "Giữ chữ tới khi kiểm xong" không chọn vì nó đổi cách hiện chữ của mọi tin nối tiếp.
- **Cách khác:** nới bước kiểm cho câu chép lại: không làm (câu không nguồn không được tới người dùng như câu trả lời). Chạy lại mọi lượt bị rút: chưa thử.
- **Cái giá:** lượt chạy lại tốn gấp đôi lần gọi model, chờ thêm vài giây.

### 5. Vì sao chương trình đếm vế và chốt kết quả, không chỉ đổi lời dặn?

- **Đã chọn:** chỉ tin từ hai vế mới nhận lời dặn theo ý; câu toàn dòng ý thiếu bị đổi về câu từ chối chuẩn.
- **Vì sao:** vòng đầu 14/11 đổi lời dặn cho mọi tin (gpt-6-luna): tin nhiều ý được trả lời 10 trên 10, nhưng 3 trên 18 câu ngoài kho của bộ câu mẫu bị trả lời. Vòng hai để chương trình quyết: vẫn 10 trên 10, bộ kín 0 trên 10. Chủ dự án chọn bật.
- **Cách khác:** lời dặn theo ý cho mọi tin: đã đo, bỏ. Để model tự nói tin có mấy ý: chưa thử.
- **Cái giá:** tin hai ý mà một vế không có từ hỏi riêng ("… bao xa, rồi ghé chợ nữa") bị đếm là một vế, có lần bị từ chối cả câu.

## Nếu… thì sao

Tình huống kể trọn: hỏi về một ngôi chùa, 40 phút sau gõ *"chỗ đó mở cửa mấy giờ?"*. Cuộc đã bị xoá; model không biết "chỗ đó" là đâu nên từ chối hoặc nói không rõ nơi nào, trong khi màn hình vẫn còn các lượt cũ. Đọc từ chương trình, chưa thử thật.

| Nếu | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|
| 30 phút không hỏi, hoặc máy chủ khởi động lại | tin nối tiếp không được hiểu | **chưa có** cách báo hay giữ lâu hơn |
| tải lại trang | màn hình trống; giao diện gọi "Cuộc trò chuyện mới" nên máy chủ cũng quên | đã có từ 15/11 (trước đó 3 trên 3 lần tái hiện bị từ chối) |
| lượt mang câu trả lời cũ bị rút, lần chạy lại cũng bị rút | "Câu trả lời không đáp ứng yêu cầu trích dẫn." và nút "Thử lại" | người dùng bấm "Thử lại" hoặc hỏi lại bằng tên nơi |
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
<summary>3. Lượt nào được chạy lại, mấy lần, người dùng thấy gì?</summary>

Lượt đang mang câu trả lời cũ mà bị rút vì số nguồn; một lần, không kèm câu trả lời cũ. Dòng tiến độ lặp lại, chờ thêm vài giây.

</details>

<details>
<summary>4. Tin hai ý, kho có ý đầu. Câu trả lời trông thế nào, có mục web không?</summary>

Ý đầu có số nguồn; ý sau là dòng "Tư liệu chưa có thông tin về: …". Không có mục web: web chỉ mở khi cả câu bị từ chối.

</details>

## Cấu hình đang chạy

*Theo chương trình và cấu hình trưa 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Tự tìm thêm (`tim_them`), số lần (`so_lan_tim_kho`) | bật; 2 | bài 21 | bài 21 |
| Nhớ cuộc trò chuyện (`nho_hoi_thoai`) | bật (từ 03/11) | hiểu tin nối tiếp | đã so bật / tắt (mục "Đã so", dòng 1) |
| Số lượt giữ mỗi cuộc | 3 | kế hoạch ghi "6 tin", theo lộ trình đặt 4–6 tin | chưa so |
| Hết hạn | 30 phút từ lượt cuối | theo bản thiết kế phần nhớ | chưa so |
| Số cuộc giữ cùng lúc | 500; quá thì bỏ cuộc cũ nhất | để bộ nhớ của máy chủ có giới hạn | chưa so |
| Trần token của lịch sử | không còn (gỡ 19/11, theo lời chủ dự án "chất lượng trước") | — | trước 19/11 là 1.500 token; chưa lượt nào từng chạm (lớn nhất 105) |
| Giữ câu trả lời liền trước (`nho_cau_tra_loi`) | bật 09:40 22/11 | hiểu "quán thứ hai bạn vừa kể" | dòng 3 |
| Cắt câu trả lời liền trước | 4.000 ký tự | 20/11 đặt 1.200 (gpt-6-luna trả lời ngắn); 21/11 với Claude, 2 trên 7 câu trả lời của một lượt tự kiểm dài hơn 1.200 (dài nhất 2.229) ⇒ nâng lên để mục cuối danh sách không mất | 1.200, bỏ |
| Nhớ tên nơi đã trích (`nho_ten_goi_y`) | bật 19/11; nhiều nhất 5 tên | lượt cũ biết đã nhắc nơi nào; câu xin "kể lại các nơi vừa nêu" và câu gõ lại nguyên văn một câu cũ thì lượt đó không nhận dòng này | dòng 2 |
| Lần chạy lại khi bị rút | 1 lần; chỉ khi lịch sử đang mang câu trả lời cũ; mọi lỗi của bước kiểm sau khi viết; chỉ đường chữ hiện dần; không ở cuộc có lịch lưu | tệ nhất bằng lúc không giữ câu trả lời | dòng 4 |
| Lời dặn theo ý (`cau_nhieu_y`) | bật 14/11; từ 2 vế | dòng 5 | dòng 5 |
| Tra web cho tin trả lời được một phần (`web_chi_khi_tu_choi`) | không tra (từ 21/11) | dòng 6 | dòng 6 |
| Tìm theo vế (`tim_theo_ve`) | bật 09:47 22/11; 2 đoạn mỗi vế; nhiều nhất 6 vế | dòng 7 | 2, 3, 4 đoạn: cùng kết quả (đếm 0 đồng) |

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

**Đọc bảng thế nào.** Dòng 1–3 là ba bước nới dần phần nhớ: câu hỏi, rồi tên nơi, rồi một câu trả lời. Mỗi bước chỉ thêm đúng thứ đã thấy thiếu. Dòng 5 và 7 cho cùng một bài học: muốn sửa tin nhiều ý thì sửa ở chỗ chương trình quyết (đếm vế, tìm theo vế), không nới lời dặn cho mọi tin.

**Giới hạn của các phép đo.** Bộ nhỏ (4 tới 17 chuỗi, 8 tới 11 tin), phần lớn do nhóm soạn. Dòng 1, 2, 5 đo với gpt-6-luna, chưa đo lại trên Claude. Dòng 3 và 7 chưa đo trên gpt-6-luna. Dòng 7 mới đo với tin gửi như tin đầu cuộc; lượt giữa cuộc có lịch sử chưa đo.

## Quyết định nhỏ hơn

**Vì sao nối thêm 2 đoạn mỗi vế, không chia lại 10 đoạn?** Giữ nguyên 10 đoạn của cả tin, nối 2 đoạn đầu của mỗi vế, nhiều nhất 6 vế. Bản được giao ban đầu "4 đoạn của cả tin + 2 đoạn mỗi vế" đã đếm và bỏ: nó làm mất đoạn đang dùng ở 3 trên 13 tin. Đếm 0 đồng: 2, 3 hay 4 đoạn mỗi vế cho cùng kết quả; 6 là số vế nhiều nhất trong 65 tin nhiều ý đã ghi. Lượt thật (dòng 7 của "Đã so"): 3 trên 24 thành 15 trên 24, 6 tin khác không mất dữ kiện đang đúng. Cái giá: chờ thêm 0,75 giây ở câu đứng giữa; tổng số dòng ý thiếu gần như không đổi (24 xuống 21).

**Vì sao lịch sử nằm ở máy chủ, không để trình duyệt gửi lại?** Kế hoạch phần nhớ ghi: trình duyệt gửi lại lịch sử thì trình duyệt sửa được "trợ lý đã nói…", tức thành chỗ cài lệnh vào lời gọi model; không chọn. Cái giá: khởi động lại máy chủ là mất (bài 6).

**Vì sao lượt lỗi, lượt bị ngắt, lượt bị rút không được ghi vào lịch sử?** Kế hoạch phần nhớ ghi: lượt lỗi / ngắt không lưu; câu cố định (từ chối, ngoài phạm vi) thì lưu để lượt sau hiểu mạch. Nhờ vậy bấm "Thử lại" là hỏi lại như lượt đó chưa từng có. Cái giá: lượt bị ngắt mất khỏi ngữ cảnh của lượt sau.

## Giới hạn đã biết

- **Tin trỏ theo thứ tự vào câu trả lời của hai lượt trước** không hiểu được; dòng ghi chú tên nơi tự khai "không theo thứ tự trong câu trả lời".
- **Nơi chỉ được nêu qua một bài tổng hợp** (cẩm nang) không có trong dòng ghi chú tên nơi.
- **Vế bị tách ra có thể mất tên nơi** ("có bậc nhiều không?"): 2 đoạn của vế đó có thể không liên quan.
- **Câu phải gom nhiều bài để so** ("lăng nào ít leo bậc") không được tìm theo vế cứu: 0 ⇒ 1 trên 13 tin.
- **Cuộc có lịch lưu không nhớ câu trả lời liền trước.** Mọi lượt hỏi thường của cuộc đó mang nguồn lịch, mà lượt có nguồn lịch không được giữ câu trả lời; hỏi "quán thứ hai bạn vừa kể" trong cuộc đó sẽ không hiểu được. Cuộc đó cũng không có lần chạy lại. Đọc từ chương trình, chưa thử thật.
- **Người dùng không được báo khi máy chủ đã quên** (quá 30 phút, máy chủ khởi động lại).

## Chi tiết để tra

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
- Cuộc có lịch lưu không nhớ câu trả lời: `assistant.py` `_before_model` (`lich_vao_hoi_thuong` ⇒ `_nguon_lich_dang_co` thêm mục `lich_dang_co`), `conversations.py` `CONG_CU_KHONG_NHO_DAP` [suy từ code, chưa thử]. Lần chạy lại chỉ ở đường stream, điều kiện `trace.citation_error`, tiền hai lần: `answer_turn_stream_parallel`; `answer_turn` không có [code].
- Dòng 8, 9 của "Đã so": `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng 34, 43 [chép]. Lịch sử ở máy chủ, lượt lỗi không lưu: `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` D1 (dòng 44), D2 (dòng 47) [kế hoạch]; trần 1.500 chưa từng chạm (lớn nhất 105): `bai_hoc/VIEC_MOI_XONG.md` mục 9 [chép].
- Bài đã qua một lượt đối chiếu độc lập với chương trình và số đo ngày 22/11 (36 dòng: 3 lệch, đã sửa): `data/hoc_cung_D/kiem/bai_23_26.md` [riêng tư].

</details>
