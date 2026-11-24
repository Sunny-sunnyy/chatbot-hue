# Bài 7 — Kho dữ liệu: 269 bài viết về Huế, ai soạn, lấy từ đâu, kiểm thế nào

*Cập nhật 20:46, ngày 23/11/2026 · mức test theo hệ thống lúc code đứng yên tối 23/11 · bản 20:20: đã áp biên bản kiểm độc lập tối 23/11 · khớp hệ thống 19:49 23/11 (57 tính năng mở, 6 tắt, kho 269 bài / 9.533 đoạn) · hai bài mới (AEON Mall Huế, công viên ven sông Hương) và một dòng tự mâu thuẫn về Quán Nhỏ, ghi kho 18:03, chỉ mục cập nhật riêng 18:05 · lượt cả bộ test xong 20:09 23/11: một file đỏ vì lỗi của chính phép kiểm, đã sửa (bài 38) · các mốc trước: khối Nguồn. · 09:55 24/11/2026: số đoạn của kho trong thân bài 9.533 ⇒ 9.536 (sáng 24/11 ba bài kho được thêm câu; chỉ mục cập nhật 07:30 và 07:49; bản ghi chỉ mục và Qdrant cùng ghi 9.536 — phiên D mở lúc 09:55); các câu có mốc giờ cũ và khối Nguồn giữ nguyên.*

**Bài trước đã biết:** hệ thống gồm những khối nào, và một câu hỏi đi qua chúng ra sao. Mọi câu trả lời chỉ được lấy từ kho.
**Bài này thêm:** mở chính kho ra xem. Trong đó có gì, bài được viết theo luật nào, kho được giữ đúng bằng cách nào, và vì sao làm như vậy.

## Ý chính

- Kho là **269 bài viết tiếng Việt**, mỗi bài một file chữ có tiêu đề và các mục, chia theo 5 chủ đề: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch.
- Bài được **soạn riêng cho hệ thống**, theo mẫu, từ các nguồn công khai; phần lớn bài ghi nguồn ở cuối bài. Câu trả lời từ kho không đọc trang web; chỉ khi kho từ chối, hệ thống mới tra web một lần và để riêng.
- Bài phải viết sao cho **từng câu đọc riêng vẫn hiểu**, vì model viết chỉ đọc vài đoạn nhỏ, không đọc cả bài.
- Đợt thêm 61 bài (14–16/11) có **đo trước và sau** trên cùng bộ câu hỏi, với điều kiện ghi sẵn: câu đang trả lời tốt không được tệ đi. Hai lần thêm bài sau cùng (22/11, 23/11) và sửa nhỏ chỉ hỏi thử vài câu. Khi một giá đổi, có lệnh **đề xuất sửa**: chương trình tìm chỗ và thay số, model chỉ phán chỗ nào đúng là mức giá đó, người duyệt.
- Chất lượng câu trả lời có trần là kho. Kho thiếu thì hệ thống từ chối; kho cũ thì hệ thống trả lời cũ.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| kho | **knowledge base**, **corpus** | tập 269 bài viết; thứ duy nhất phần hỏi đáp được trả lời từ đó |
| file Markdown | **Markdown** | file chữ thường, tiêu đề đánh dấu bằng `#`, bảng và danh sách viết bằng ký hiệu đơn giản |
| mẫu bài | **template** | khung các mục mà mọi bài cùng chủ đề phải theo |
| trả lời trong phạm vi kho | **closed-world**, **grounded answering** | chỉ nói điều kho có; kho không có thì từ chối |

## Kho có 269 bài, chia theo 5 chủ đề

| Chủ đề | Số bài | Gồm |
|---|---:|---|
| Món ăn | 111 | đặc sản, quán ăn, nhà hàng, quán cà phê |
| Di tích | 39 | Đại Nội, Kinh thành, các lăng, chùa, di sản như Nhã nhạc |
| Lễ hội | 40 | lễ hội, ngày hội, lễ tế trong năm |
| Nghệ thuật biểu diễn | 15 | ca Huế, các chương trình biểu diễn |
| Du lịch | 64 | 47 bài địa điểm (biển, đầm phá, chợ, phố đi bộ, công viên…), 12 bài dịch vụ (đi lại, lưu trú…), 5 bài vé |

Cả kho cắt ra thành 9.536 đoạn (bài 8).

Phần hỏi đáp không biết gì ngoài 269 bài này. Có bốn thứ không lấy từ kho, và đều được ghi rõ khi hiện ra: ngày tháng và ngày âm lịch (chương trình tính), dự báo thời tiết (lấy từ một dịch vụ thời tiết), khoảng cách và "gần một điểm có gì" (chương trình tính từ một bảng vị trí riêng), và mục "Từ web (chưa kiểm)" (chỉ có khi kho từ chối). Trang Lên kế hoạch dùng thêm vài bảng dữ liệu riêng: bảng điểm tham quan, bảng chỗ ở, bảng quán ăn (chặng 6).

## Bài được soạn riêng, theo mẫu, có ghi nguồn

Kho không phải bản sao của các trang web. Mỗi bài được viết lại từ các nguồn công khai (cổng thông tin của địa phương, báo, trang du lịch, văn bản quy định giá) theo một **mẫu bài** của chủ đề đó. Ví dụ bài về một món ăn có: món là gì, ăn ở đâu, giá, giờ. Vài luật viết áp cho mọi bài:

- bài bắt đầu bằng tên bài, rồi chia mục;
- **không có mục rỗng:** thông tin nào không có thì bỏ hẳn mục đó, không ghi "đang cập nhật";
- cuối bài có mục **"Nguồn dữ liệu"** ghi thông tin lấy từ đâu (phần lớn bài có mục này; một số bài chưa có).

## Mỗi câu trong bài phải đọc riêng vẫn hiểu

Lúc trả lời, model viết không đọc cả bài. Nó đọc các đoạn nhỏ (10 đoạn ở lần tìm đầu), của nhiều bài. Nếu một đoạn viết "Quán này mở từ 6 giờ sáng" mà không nói quán nào, model không biết "quán này" là quán nào, và có thể gán nhầm sang quán khác.

Vì vậy bài được viết sao cho từng câu, từng dòng mang đủ tên và bối cảnh của nó. Ở ví dụ chính, đoạn số 1 ghi giá vé vào cổng Đại Nội, 200.000 đồng cho người lớn, trong cùng một câu: con số đứng cạnh tên nơi và loại vé.

## Thêm hay sửa kho đi theo bốn bước

Kho đã đổi nhiều lần. Cách làm chung:

1. **Có căn cứ.** Sửa khi có căn cứ ngay trong kho hoặc ở nguồn công khai; chỗ không chắc thì viết nhẹ đi chứ không đoán. Với con số: xem quyết định 5.
2. **Ghi trước điều kiện "không làm hỏng".** Ví dụ: không thêm câu ngoài kho nào bị trả lời, không thêm lỗi ở các câu về vé, giờ, cảnh báo an toàn.
3. **Đo trước và sau** trên cùng bộ câu hỏi (chặng 4) khi thêm bài mới hoặc sửa nhiều; sửa nhỏ thì hỏi thử các câu chạm chỗ sửa.
4. **Cập nhật chỉ mục**, chỉ cho các bài vừa đổi (bài 12). Quên bước này thì từ lần khởi động sau, máy chủ vẫn chạy nhưng mọi câu hỏi nhận lời báo.

Lần gần nhất (tối 23/11) là lần thứ hai đường "phiên soạn nháp ⇒ chủ dự án chọn ghi ⇒ ghi kho ⇒ cập nhật riêng chỉ mục" chạy thật, sau bài Hội An (22/11). Cả hai lần chỉ hỏi thử vài câu, không có lượt đo trước và sau trên bộ câu hỏi (bước 3). Trình tự giờ của lần 23/11: "Chi tiết để tra".

Các đợt đổi kho chính: bảng ở "Chi tiết để tra". Điều rút ra từ đợt rà sửa cuối tháng 10: kho đúng hơn mà điểm không tăng. Điểm chấm chỉ nhìn thấy những gì bộ câu hỏi có hỏi; chỉ khoảng 1 trên 6 câu của bộ chạm vào chỗ sửa. Sửa kho cho đúng vẫn phải làm, kể cả khi điểm không phản ánh.

## Khi một giá đổi: chương trình tìm chỗ, model phán, người duyệt

Cùng một con số có thể nằm ở nhiều bài và là giá của nhiều thứ. Thử trên một bản chép của kho: con số 200.000 có ở 37 chỗ trong 14 bài, nhưng chỉ 9 chỗ là vé vào cổng Đại Nội; các chỗ khác là vé gộp hai lăng, vé một điểm khác, giá quán ăn. Sửa tay thì dễ sót.

Từ 22/11 có hai lệnh chạy tay:

1. **Lệnh đề xuất.** Người vận hành nêu mức giá nào đổi, giá cũ, giá mới, nguồn. Chương trình tìm mọi chỗ có con số cũ. Model trả lời đúng một câu cho từng chỗ: con số này có phải mức giá vừa mô tả không (đúng / không / không rõ). Chương trình thay con số ở các chỗ "đúng" và soạn một bản đề xuất để đọc. Kho chưa đổi chữ nào.
2. **Lệnh duyệt.** Người duyệt đọc bản đề xuất, tắt máy chủ, rồi chạy lệnh thứ hai: các dòng được thay, mỗi bài được sửa có thêm một dòng ghi nguồn và ngày đối chiếu, rồi chỉ mục của các bài đó được cập nhật. Bật lại máy chủ thì câu trả lời dùng giá mới.

Hai lệnh này mới thử trên một bản chép của kho, chưa được dùng trên kho thật.

## Quyết định và lý do

### 1. Vì sao soạn kho riêng từ trước, mà không đọc thẳng các trang web lúc có câu hỏi?

- **Đã chọn:** soạn bài một lần, theo mẫu, từ nguồn công khai; lúc trả lời chỉ đọc kho.
- **Vì sao:** quyết định đã ghi: sản phẩm chỉ trả lời từ kho đã soạn và kiểm. Lý do ghi ở hồ sơ kho: trên mạng cùng một quán có thể có ba giờ mở cửa khác nhau, lẫn quảng cáo và bài cũ; soạn trước thì kiểm được bài nào nói gì, lấy từ đâu, chỗ nào mâu thuẫn.
- **Cách khác:** đọc web lúc hỏi: không làm. Web chỉ là đường phụ khi kho từ chối, để riêng (bài 25).
- **Cái giá:** công soạn; kho thiếu thì từ chối, cũ thì trả lời cũ.

### 2. Vì sao giữ dạng bài viết, không chuyển giá vé và giờ mở cửa sang một bảng dữ liệu?

- **Đã chọn:** mọi thông tin nằm trong bài viết, kể cả bảng giá.
- **Vì sao:** đã đo một lần. Bảng vé và giờ cho 60 điểm trả lời đúng 19 trên 20 câu, nhưng trượt điều kiện về cách model nêu điều kiện đi kèm (6 trên 10); dùng bảng chỉ để kiểm số thì không bắt được số sai nào trên 52 câu thật.
- **Cách khác:** chính bảng đó; bỏ.
- **Cái giá:** sửa một giá phải dò khắp kho.

### 3. Vì sao đợt thêm nhiều bài phải đo lại cả các câu cũ?

- **Đã chọn:** đo trước và sau, với điều kiện "không làm hỏng" ghi trước (61 bài, 14–16/11).
- **Vì sao:** bài mới có thể đẩy đoạn đúng của một câu khác ra khỏi 10 đoạn. Đã đo bù ngày 15/11: 65 câu cũ có 10 đoạn đầu bị đổi vì bài mới; không câu nào tệ đi, 1 câu tốt lên.
- **Cách khác:** chỉ hỏi thử các câu chạm chỗ sửa: dùng cho sửa nhỏ.
- **Cái giá:** công đo mỗi lần thêm bài. Hai lần thêm bài sau cùng (22/11, 23/11) không đo: chưa thấy ghi lý do. Điều thấy được: mỗi lần một hoặc hai bài.

### 4. Vì sao khi giá đổi, chương trình thay số còn model chỉ phán, không để model viết lại dòng?

- **Đã chọn:** cách chia việc ở mục trên.
- **Vì sao:** lý do ghi trong chương trình: phân biệt cùng một con số là vé Đại Nội hay giá một quán ăn là việc chương trình không làm được, nên giao model; còn dòng mới do chương trình dựng, model không viết chữ nào vào kho. Chủ dự án chọn làm việc này tối 21/11.
- **Cách khác:** sửa tay (cách trước đó): dễ sót.
- **Cái giá:** phải biết giá cũ, mỗi lần một mức giá. Câu có con số tính từ giá cũ (tổng hai vé, mức tiết kiệm) chỉ được liệt kê để sửa tay; ca Đại Nội có 13 câu như vậy.

### 5. Vì sao không cập nhật giá trong kho theo web định kỳ?

- **Đã chọn:** chỉ sửa chỗ kho tự mâu thuẫn hoặc thiếu điều người dùng hỏi; một con số chỉ đổi khi một nguồn đáng tin nói rõ, các nguồn nói khác nhau thì giữ nguyên.
- **Vì sao:** chủ dự án đã quyết (09:25 22/11): giá chỉ cần tương đối, không cần đi cập nhật mỗi khi giá đổi. Luật "nguồn đáng tin nói rõ mới đổi" do nhóm chốt cùng buổi sáng.
- **Cách khác:** một lệnh tự tra web để phát hiện giá đổi: không làm. Hai lệnh đề xuất và duyệt giữ làm công cụ, chạy khi cần.
- **Cái giá:** giá trong kho cũ dần. Chỉ câu trả lời trích bài vé, địa điểm, lễ hội hoặc bài "Lưu trú ở Huế" mới kèm dòng nhắc kiểm lại (bài 9).

### 6. Vì sao không bổ sung chỗ đậu ô tô và quy định chụp ảnh?

Lượt đo 21/11 chỉ ra bốn mảng kho thiếu; tối 21/11 chủ dự án chọn bổ sung cả bốn, đọc nháp rồi mới ghi. Hai mảng thành bài ngày 22/11; hai mảng kia trình lại.

- **Đã chọn:** không bổ sung cả hai mảng; ghi thành giới hạn.
- **Vì sao:** chủ dự án chọn "bỏ cả hai" lúc 12:22 23/11: "tôi nghĩ sẽ ít người hỏi các câu này". Lúc trình lại, nhóm báo: nháp chỗ đậu ô tô mỏng; quy định chụp ảnh không có nguồn công khai nào nói dứt khoát.
- **Cách khác:** ghi bài đậu ô tô, bỏ phần chụp ảnh; hoặc chủ dự án đọc nháp mới quyết: có trong câu trình, không được chọn.
- **Cái giá:** kho không có bài riêng; câu hỏi nhận câu từ chối, câu dẫn sang mục web, hoặc được trả lời một phần ("Giới hạn đã biết").

## Nếu… thì sao

Đọc từ chương trình và hồ sơ; người viết chưa thử lại.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| một bài ghi sai giá | trả lời đúng theo bài, kèm số nguồn | giá sai. Bài vé, địa điểm, lễ hội hoặc bài "Lưu trú ở Huế": kèm dòng "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi — hãy kiểm lại với nơi đến trước khi đi." Bài quán ăn: không có dòng nhắc nào | người vận hành chạy lệnh đề xuất, đọc, tắt máy chủ, chạy lệnh duyệt, bật lại máy chủ |
| hai bài ghi hai giá khác nhau cho cùng một thứ | chương trình không so hai bài; nếu cả hai đoạn cùng được đưa cho model thì lời dặn bảo model giữ chỗ mâu thuẫn (chưa thử ca này) | tuỳ đoạn nào được tìm ra: giá này, giá kia, hoặc cả hai | nhóm được tra nguồn rồi sửa; chỗ chưa phân xử được ghi vào một danh sách riêng |
| thêm hay sửa bài mà chưa cập nhật chỉ mục | máy chủ đang chạy thì vẫn trả lời theo chỉ mục cũ; từ lần khởi động sau thì dừng trả lời | trước khởi động lại: bài mới chưa có mặt. Sau: "Dữ liệu tra cứu cần được lập chỉ mục lại." | tắt máy chủ, chạy lệnh cập nhật chỉ mục, bật lại (bài 12). Bài có điểm trong bảng điểm trang Lên kế hoạch mà mã đoạn đổi thì máy chủ không bật được tới khi sửa bảng (bài 6) |
| kho không có điều được hỏi | câu từ chối, rồi tra web một lần | "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này."; khi mục web có nội dung, câu này được thay bằng "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)." | bài mới cần chủ dự án duyệt; chỗ đậu ô tô, quy định chụp ảnh: chọn không bổ sung (quyết định 6) |
| kho lớn gấp mười | mỗi lần cập nhật vẫn cắt lại cả kho | — | bước cắt đoạn (21 giây hiện nay) thành phần chính của lần cập nhật |

## Dễ nhầm

- **"Hệ thống đọc Internet để trả lời."** Không. Nó đọc 269 bài đã soạn; web chỉ là đường phụ khi kho từ chối, để riêng.
- **"Lệnh sửa giá là một agent tự sửa kho."** Không. Đó là một quy trình cố định có một bước model phán đoán và một người duyệt; model không viết chữ nào vào kho.

## Câu hỏi tự kiểm

<details>
<summary>1. Vì sao bài trong kho phải viết sao cho từng câu đọc riêng vẫn hiểu?</summary>

Model viết chỉ đọc vài đoạn nhỏ từ nhiều bài. Câu "quán này mở từ 6 giờ" không nói quán nào thì model có thể gán nhầm.

</details>

<details>
<summary>2. Hai đợt sửa khoảng 250 chỗ mà điểm chấm không đổi. Vậy có nên sửa không?</summary>

Có. Điểm chấm chỉ thấy điều bộ câu có hỏi; chỉ khoảng 1 trên 6 câu chạm chỗ sửa.

</details>

<details>
<summary>3. Giá vé Đại Nội đổi. Ai làm phần nào trong hai lệnh sửa giá?</summary>

Chương trình tìm mọi chỗ có con số cũ và thay số. Model chỉ phán từng chỗ có đúng là vé Đại Nội không. Người duyệt đọc bản đề xuất rồi chạy lệnh duyệt; câu có con số tính từ giá cũ thì sửa tay.

</details>

<details>
<summary>4. Vì sao không cho một lệnh tự tra web để cập nhật giá định kỳ?</summary>

Chủ dự án đã quyết: giá trong kho chỉ cần tương đối. Nhóm chỉ sửa chỗ kho tự mâu thuẫn hoặc thiếu; câu trả lời trích bài vé, địa điểm, lễ hội hoặc bài "Lưu trú ở Huế" kèm dòng nhắc kiểm lại.

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Thư mục kho | `knowledge-base-hue/`, được theo dõi cùng mã của dự án từ 20/11 | mọi lần sửa bài đều có lịch sử và lùi lại được | trước 20/11 thư mục kho nằm cạnh mã nhưng không được theo dõi lịch sử |
| Các thư mục được đưa vào | món ăn · di tích · lễ hội · nghệ thuật biểu diễn · du lịch / địa điểm · du lịch / dịch vụ · du lịch / vé | 7 thư mục, 269 bài (từ 18:05 23/11) | — |
| Thư mục bị loại | bộ câu hỏi chấm · bản thô tải từ trang nguồn · mẫu bài và ghi chú soạn | không phải nội dung cho người dùng | — |
| File bị loại đích danh | 3 file danh mục dùng lúc soạn | chỉ là danh sách tên, không phải nội dung để trả lời | hai file loại từ đầu tháng 9, file thứ ba loại cuối tháng 10; phép đo lúc loại: kết quả tìm không khác |
| Dạng bài | file Markdown, bắt đầu bằng tên bài | đọc thẳng, không cần bước rút chữ từ PDF hay trang web | — |
| Quy tắc gắn lưu ý | 3 quy tắc ở 2 bài (bài 8) | câu lưu ý chung của bài đi kèm từng đoạn giá | — |

## Đã so

**Vấn đề thật đã gặp.** Hệ thống từ chối những câu rất thường: hỏi khách sạn, hỏi một cây cầu hay nhà ga nổi tiếng, hỏi một lễ hội chưa có bài. Đếm trên các câu "về Huế mà kho không có" cho thấy kho thiếu thật ở các mảng đó. Câu hỏi: thêm bài thì các câu này có trả lời được không, và các câu đang tốt có bị tệ đi không?

**So gì, trên bộ nào.** Trước và sau mỗi lần ghi thêm bài (sáu lần ngày 14/11, một lần 16/11), model viết là gpt-6-luna. Hai nhóm câu: nhóm câu nhắm vào bài mới, và các câu cũ có 10 đoạn đầu bị đổi vì bài mới (đo bù ngày 15/11 cho ba lần ghi sau).

| Đo gì | Trước | Sau |
|---|---|---|
| Câu về khách sạn trả lời được (chấm mà không biết bản nào) | 4 trên 12 | 11 trên 12 |
| Câu về đi lại trả lời được (người viết báo cáo tự đọc) | 2 trên 6 | 4 trên 6 |
| Bữa ăn trong lịch có quán thuộc kho (chương trình đếm trên 3.840 lịch mô phỏng, không dính model) | 49,3 % | 69,1 % |
| 65 câu cũ có 10 đoạn đầu bị đổi vì bài mới | — | 8 câu ra đúng chữ cũ; 57 câu khác chữ, trong đó 56 câu cùng ý và 1 câu tốt lên (hết bị từ chối) |

**Đọc bảng này thế nào.**
- Thêm bài đúng chỗ thiếu làm các câu từng bị từ chối trả lời được.
- Mỗi lần ghi có điều kiện "không làm hỏng" ghi trước. Lượt 65 câu là đo bù sau khi ghi, để chắc không câu nào tệ đi.
- Dòng "đi lại" do chính người viết báo cáo tự đọc, độ chắc thấp hơn các dòng khác.

**Giới hạn của phép đo.** Bộ câu do nhóm soạn. Các số trên đo với gpt-6-luna, chưa đo lại với model đang chạy.

## Quyết định nhỏ hơn

**Vì sao kho được theo dõi lịch sử cùng mã của dự án?** Từ 20/11, kho nằm trong kho mã: mọi lần sửa bài có lịch sử và lùi lại được; lệnh duyệt sửa giá lưu một bản ghi lịch sử cho mỗi lần áp.

**Vì sao loại 3 file danh mục khỏi chỉ mục?** Chúng chỉ là danh sách tên dùng lúc soạn, không phải nội dung để trả lời. Đã đo lúc loại: kết quả tìm không khác.

**Vì sao bài mới và việc đổi cấu trúc kho cần chủ dự án duyệt, còn chỗ kho tự mâu thuẫn thì nhóm được sửa?** Quyết định đã ghi: viết hay sửa nội dung kho nằm ở hàng "hỏi chủ dự án trước" của bảng quyền; ngày 22/11 chủ dự án cho nhóm tra nguồn rồi sửa chỗ sai hoặc chưa khớp trong bài đang có. Dòng Quán Nhỏ 23/11 là loại thứ hai: chính bài cẩm nang ẩm thực (ở danh sách bữa sáng) và bài riêng của quán đều ghi 06:00 – 10:00, ba trang công khai đối chiếu ngày 23/11 cũng nói quán đóng trước trưa; bản sửa viết 12:09 nhưng chỉ gộp 18:03, để chỉ mục được cập nhật cùng một bước với hai bài mới. Nơi khác dùng giờ quán này: bảng quán của lịch đã đánh dấu Quán Nhỏ không hợp cả bữa trưa lẫn bữa tối từ trưa 23/11 (bài 30).

**Vì sao lệnh duyệt và lệnh cập nhật chỉ mục bắt tắt máy chủ trước?** Lý do ghi trong chương trình: máy chủ chỉ kiểm chỉ mục một lần lúc bật, nên nếu còn chạy nó sẽ trả lời trên chỉ mục đang ghi dở cùng file thống kê cũ. Hai lệnh dò máy chủ trước khi ghi; thấy đang chạy thì dừng, kho không đổi.

## Giới hạn đã biết

- **Kho thiếu, có chủ ý ở hai mảng.** Lượt đo trợ lý ngày 21/11 chỉ ra bốn thứ kho không có: mức phải leo bậc ở các điểm tham quan, đường từ Huế đi Hội An, chỗ đậu ô tô khu trung tâm, quy định chụp ảnh ở chùa / lăng / bảo tàng. Bài về leo bậc vào kho sáng 22/11, bài về đường đi Hội An vào kho chiều 22/11. Hai thứ còn lại chủ dự án chọn KHÔNG bổ sung (12:22 23/11, quyết định 6): câu hỏi chung thường nhận câu từ chối; mục web có nội dung thì trang hiện câu dẫn "Tư liệu của mình chưa có thông tin này — dưới đây là thông tin từ web (chưa kiểm)." (bài 16). Khoảng 45 bài kho có dòng lẻ về chỗ gửi xe, đỗ xe, và vài bài có lưu ý biển cấm chụp, đèn flash (bài hướng dẫn di sản, lễ hội, biểu diễn; chùa Thiên Mụ; nhà thờ Phủ Cam), nên câu hỏi về đúng những nơi đó có thể được trả lời một phần từ kho. Ví dụ "kho không có" của cả bộ (chỗ đậu ô tô ở chùa Thiên Mụ) thuộc nhóm này.
- **Kho cũ dần.** Giá và giờ đổi theo thời gian. Câu trả lời trích bài vé, địa điểm, lễ hội hoặc bài "Lưu trú ở Huế" luôn kèm dòng "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi…". Giá trong kho được coi là tương đối. Phần lớn mức giá không ghi ngày; vài bảng ghi tháng khảo sát, và bài sửa từ 22/11 ghi ngày đối chiếu ở mục nguồn.
- **Kho còn chỗ chưa phân xử được.** Vài con số mà các nguồn nói khác nhau được giữ nguyên và ghi vào một danh sách riêng.
- **Kho có mà tìm không ra.** Đây là lỗi của bước tìm, và là lỗi hay gặp hơn cả (bài 13).

## Chi tiết để tra

Các lần đổi kho chính:

| Khi nào | Việc | Kết quả đo |
|---|---|---|
| cuối tháng 10 | rà mọi dòng có con số hoặc mốc thời gian: 139 điểm đáng ngờ; hai đợt sửa, khoảng 250 chỗ (phần lớn là tên phường xã mới sau lần sắp xếp 01/07/2025) | điểm chấm gần như không đổi (điểm "đủ ý" chênh chưa tới 0,01 trên thang 5); điều kiện "không làm hỏng" đạt ở cả hai đợt |
| đầu tháng 11 | thêm một dòng giờ mở cửa cho 11 bài điểm tham quan, lấy từ bài vé đã có trong kho | hỏi thử trả đúng giờ, có nguồn; 1 câu của bộ câu mẫu lần đầu bị từ chối, chạy lại hai lần đều đúng |
| 14–16/11 | thêm 61 bài (204 lên 265): khách sạn, quán ăn, địa điểm, lễ hội, những thứ hệ thống từng từ chối | câu về khách sạn trả lời được 11 trên 12 (trước đó 4); đo bù 65 câu cũ: không câu nào tệ đi |
| 22/11 | sửa hai bài về giá (giá thuê thuyền ghi theo từng nhà thuyền; vé một điểm tham quan cho người địa phương); thêm một bài gom những gì kho đã nói về bậc thang, dốc và đi bộ ở các điểm tham quan (265 lên 266 bài); buổi chiều thêm một bài về đường đi từ Huế tới Hội An, chủ dự án đọc bản nháp rồi duyệt (266 lên 267 bài); sửa một dòng ở bài về đèo Hải Vân: dòng đó nói Hải Vân Quan đón khách không thu tiền, trái với chính bài đó và với bài vé (thu 70.000 đồng một người từ tháng 6/2026) | chỉ mục cập nhật riêng trong 37,7 giây cho lần sửa giá (bài 12); bài Hội An: thêm 21 đoạn trong 29 giây, hai câu hỏi thử trên trình duyệt đều được trả lời từ bài mới; dòng Hải Vân Quan: 40 đoạn tính lại trong 28,8 giây, hỏi thử một lần trên trình duyệt thì danh sách điểm miễn phí không còn Hải Vân Quan và câu hỏi giá vé nhận 70.000 đồng, không còn lời "hai nguồn không khớp"; bài Hội An còn có một phép tìm thử ba câu trước / sau khi ghi (không qua model: hai câu về Hội An, tàu vào Đà Nẵng có 10 đoạn đầu đổi; câu đối chứng giá vé Đại Nội giữ y hệt), không có lượt đo trước và sau trên bộ câu hỏi; bài leo bậc: lượt đo 12 vai người dùng mô phỏng 13:50–14:04 (gộp nhiều thay đổi của hai ngày) thấy vai hỏi điểm ít leo bậc từ trượt thành đạt |
| 23/11 | thêm hai bài địa điểm chủ dự án nêu cho buổi tối (AEON Mall Huế; công viên ven sông Hương ở trung tâm Huế): một phiên soạn nháp từ nguồn công khai, phiên điều phối đọc, chủ dự án chọn "Ghi cả hai" (267 lên 269 bài); sửa một dòng ở bài cẩm nang ẩm thực (tour ăn nửa ngày gợi ý Quán Nhỏ cho bữa trưa, trái với chính bài đó và bài riêng của quán) | chỉ mục cập nhật riêng 3 bài lúc 18:05: 65 đoạn tính lại, 32 giây, kho 9.479 ⇒ 9.533 đoạn; lượt trình duyệt 18:48–18:54: ba câu hỏi về AEON, công viên ven sông, chợ Đông Ba buổi tối đều được trả lời từ đúng bài kho, có nguồn, có ảnh; trang Khám phá có hai bài mới, có ảnh; hai bài kho giống từng byte bản nháp; không có lượt đo trước và sau trên bộ câu hỏi |

- Trình tự lần thêm bài 23/11 (chuyển từ thân bài khi áp biên bản kiểm tối 23/11): 15:42 (giờ ghi) chủ dự án chọn "Viết nháp 2–3 bài, tôi đọc rồi ghi (Recommended)"; một phiên soạn hai nháp từ nguồn công khai (17:05 – 17:09); chủ dự án về khoảng 17:53 và chọn "Ghi cả hai (Recommended)" (lời ghi lúc 18:07, sau lần ghi kho; lời commit 18:03 ghi hai bài đã được chủ dự án duyệt sau khi đọc nháp). 18:03 hai bài AEON Mall Huế và công viên ven sông Hương vào kho, cùng một dòng sửa chỗ kho tự lệch về giờ Quán Nhỏ; 18:05 chỉ mục cập nhật riêng 3 bài (65 đoạn, 32 giây).
- Số bài theo thư mục, đếm từ bản ghi chỉ mục 18:05 ngày 23/11: món ăn 111 · di tích 39 · lễ hội 40 · nghệ thuật biểu diễn 15 · địa điểm 47 · dịch vụ 12 · vé 5 (lúc 10:02 ngày 22/11: địa điểm 45, dịch vụ 11). Kho còn được bổ sung nên số có thể lớn hơn khi anh đọc.
- Hai đợt sửa cuối tháng 10: 123 chỗ ở 65 bài, rồi 123 chỗ ở 40 bài.
- Lệnh sửa giá, thử trên bản chép với Claude Sonnet 5.5, hai ca: ca Đại Nội chọn đúng 9 chỗ, để 1 chỗ cho người xem, bỏ qua 27 chỗ; ca vé lăng Tự Đức (có câu ghi chung một giá cho ba lăng) sửa 1 chỗ, để 3 chỗ cho người xem. Không chỗ nào sửa nhầm, không chỗ nào sót so với đáp án gắn tay từ trước.
- Lệnh sửa giá, thêm: chạy ba lần ca Đại Nội, file vá giống nhau từng ký tự; một phiên khác tự chạy lại trên bản chép riêng ra đúng 9 · 1 · 27. Ca Tự Đức có 51 chỗ (1 sửa, 3 không rõ, 47 không phải). Con số viết bằng chữ hoặc viết gọn kiểu "200–250 nghìn" không được tìm thấy. Lệnh đề xuất mất khoảng 20 giây. Hai bài có bảng giá gắn luật điều kiện thì lệnh duyệt dừng và in cách sửa tay.
- Bảng vé và giờ có cấu trúc (đã bỏ): lợi gần như không có, thêm khoảng 120 dòng chương trình và một bảng phải giữ khớp với kho.
- Khoảng 76 trang web nguồn khác nhau, đếm lúc kho có 204 bài; chưa đếm lại.
- Một phép đếm thô ngày 22/11: khoảng 39 bài không có tiêu đề mục nào mang chữ "Nguồn" (chưa đọc tay từng bài).
- Bước chuẩn bị còn hai cách giữ bối cảnh nữa: dòng tiêu đề bảng đi kèm mỗi dòng giá (bài 8), và tên bài cùng tên mục đi kèm mỗi đoạn (bài 9).
- Tình huống hỏng của lệnh sửa giá (chuyển từ bảng "Nếu… thì sao" đêm 23/11, không đổi nội dung): dòng giá cần sửa là một câu mà file quy tắc lưu ý (bài 8) chép nguyên văn để biết gắn lưu ý vào đâu ⇒ lệnh duyệt dừng, chưa áp gì, in cách sửa tay; người dùng thấy: không đổi gì: giá cũ còn; người vận hành sửa tay ở cả hai nơi; nhóm không làm cho lệnh tự sửa trọn, vì giá chỉ cần tương đối.
- Hai mảng không bổ sung: nháp "Đỗ ô tô ở khu trung tâm Huế" đã soạn (ngắn, khoảng 2.600 byte) và giữ nguyên ngoài kho; phần quy định chụp ảnh / quay phim / flycam không soạn được nháp vì đợt tra 21/11 không mở được nguồn nào nêu quy định. Nhóm đã chốt không trình lại.

**Bài sau (bài 8):** bước đầu tiên của giai đoạn chuẩn bị: cắt 269 bài thành 9.536 đoạn.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- 267 bài và số bài theo thư mục: đếm từ danh sách file của `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`, 16:35 22/11/2026 [đã chạy]. Bài về đường đi Hội An (chủ dự án duyệt 16:07, vào chỉ mục 16:15 22/11, thêm 21 đoạn trong 29 giây; hai câu hỏi thử trên trình duyệt 16:21): `session_prompt/HIEN_TRANG.md` mục 1, `bai_hoc/VIEC_MOI_XONG.md` mục 44 [đã chạy, phiên khác]. Dòng Hải Vân Quan (22/11, bản kho `68e806b6`; đúng một dòng đổi; 40 đoạn, 28,8 giây; hai câu hỏi thử trên trình duyệt 16:42–16:44): phiếu của phiên điều phối, `data/bo_sung_kho_2026-11-22/c_x11_hai_van/`, `data/test_cuoi/chay_2026-11-22_e_ngoai_tinh/chay_x.out` [riêng tư; đã chạy, phiên khác; người viết đã đọc bản ghi hai lượt hỏi]. Thư mục đưa vào / loại, file loại: `backend/config/settings.yaml` mục `full_corpus.knowledge_base`.
- Luật viết bài, mẫu bài, "đọc riêng vẫn hiểu", lý do soạn riêng, rà 139 điểm, hai đợt sửa (123 + 123 chỗ; 65 và 40 bài; điểm đủ ý ±0,008; khoảng 1 / 6 câu chạm), giờ mở cửa 11 bài, khoảng 76 trang nguồn: `bai_hoc/01_KHO_DU_LIEU.md` và nguồn gốc `bao_cao_he_thong/02_BAO_CAO_KHO_DU_LIEU.md` [đã chạy; chép qua bài 1 cũ].
- Các lần bổ sung 14–16/11 (61 bài; khách sạn 4 ⇒ 11 / 12 chấm mù; đi lại 2 ⇒ 4 / 6 tự đọc; bữa có quán 49,3 ⇒ 69,1 %; 65 câu đo bù: 56 cùng ý, 1 tốt lên): `bai_hoc/22_BO_SUNG_SO_TAY.md` mục "Ba điều chính" và mục Nguồn [đã chạy].
- Sửa hai bài giá ngày 22/11, luật "có nguồn đáng tin nói rõ mới sửa", danh sách "chưa phân xử được": `session_prompt/HIEN_TRANG.md` mục 4, gạch 08:40 22/11/2026; `session_prompt/VIEC_DANG_MO.md` khối A; lần cập nhật 37,7 giây: `bai_hoc/VIEC_MOI_XONG.md` mục 32.
- Giá trong kho chỉ cần tương đối; hai lệnh đề xuất + duyệt, ca 37 chỗ / 9 chỗ, chưa dùng trên kho thật: `bai_hoc/VIEC_MOI_XONG.md` mục 30 [đã chạy trên bản chép].
- Kho nằm trong kho mã từ 20/11: `AGENTS.md` luật cứng 2.
- Bốn thứ kho thiếu; bài bổ sung đang soạn nháp: `session_prompt/HIEN_TRANG.md` mục 3 và mục 4 (gạch 22:06 21/11/2026).
- Đợt 16:30 23/11/2026 (giờ `date`; người viết đọc cây chính `0586b186` ⇒ `da76649d`, không chạy gì ngoài lệnh đếm):
  - Quyết định 6, gạch "Kho thiếu, có chủ ý ở hai mảng", hàng "kho không có điều được hỏi" của "Nếu… thì sao": `session_prompt/HIEN_TRANG.md` mục 4 gạch "12:22 23/11/2026" điểm (5) ("BỎ CẢ HAI — "tôi nghĩ sẽ ít người hỏi các câu này" ⇒ không ghi kho, thành dòng giới hạn; nháp giữ nguyên … không nhắc lại") và mục 3 câu 1 ("[ĐÃ TRẢ LỜI: bỏ cả hai] … bài nháp chỗ đậu ô tô khu trung tâm (mỏng) và câu về quy định chụp ảnh ở chùa / lăng / bảo tàng (nhóm không tìm được nguồn công khai nào nói dứt khoát)") [quyết định đã ghi; chép, đã mở]. Nguyên văn và ba ô của câu trình ("ghi bài đậu xe + bỏ chụp ảnh / bỏ cả hai / tôi đọc nháp rồi quyết"): `data/loi_user/2026-11-23.md` dòng 19 [riêng tư; đã mở]. Hàng runbook: `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Người dùng hỏi CHỖ ĐẬU Ô TÔ khu trung tâm, hoặc QUY ĐỊNH CHỤP ẢNH…" (commit `0586b186`; "Không trình lại") [chép, đã mở]. "Nhóm đã chốt không trình lại": runbook hàng trên và `HIEN_TRANG.md` điểm (5) "không nhắc lại" — ghi sau dấu ⇒ của phiên điều phối, không phải lời chủ dự án.
  - Hai mảng đã thành bài ngày 22/11 (leo bậc; Hội An): khối Nguồn bên trên và bảng "Các lần đổi kho chính" [chép trong bài].
  - Nháp đỗ ô tô 2.625 byte (`wc -c`); nháp chụp ảnh không soạn vì "không mở được nguồn nào nêu quy định chụp ảnh": `data/bo_sung_kho_2026-11-21/nhap/Đỗ ô tô ở khu trung tâm Huế.md`, `data/bo_sung_kho_2026-11-21/BAO_CAO.md` dòng 7 và mục "Nháp 3" [riêng tư; tự đếm; đã mở báo cáo, không mở nội dung nháp].
  - Câu dẫn sang mục web, câu từ chối: `frontend/src/moDauWeb.js` (`CAU_DAN_WEB`, `CAU_TU_CHOI`) [code]; luật thay câu: bài 16.
  - Dời xuống "Chi tiết để tra" (không bỏ thông tin): số thử hai lệnh sửa giá (9 · 1 · 27; Tự Đức 1 · 3), câu "hai cách giữ bối cảnh" (bài 8, 9); bỏ khỏi thân bài hai câu lặp: danh sách bốn đợt đổi kho (đã có ở bảng "Các lần đổi kho chính"), "đọc thẳng, không cần bước rút chữ" (đã có ở bảng cấu hình, nay thêm "từ PDF hay trang web"), "Máy chủ còn chạy thì lệnh dừng" (đã có ở "Quyết định nhỏ hơn"). Nửa để hiểu 12.999 ⇒ 13.295 ký tự.
  - Áp biên bản 17:03 23/11/2026 (`data/hoc_cung_D/kiem/dot_2311_chieu2_k1_kiem.md` mục "Bài 07" dòng 2, 4, 8 [riêng tư]): quyết định 6 kể đủ trình tự — tối 21/11 chủ dự án chọn bổ sung cả bốn, đọc nháp rồi mới ghi (`session_prompt/HIEN_TRANG.md` mục 4 gạch 22:06 21/11/2026, điểm 2a) [quyết định đã ghi; chép, đã mở]; 12:22 23/11 là lần trình lại. "Cái giá" và gạch "Kho thiếu…": người viết tự dò lại trong lượt áp 16:57–17:04 23/11 bằng `scripts/grep_kb.sh -l -i -E "bãi đỗ|bãi xe|gửi xe|giữ xe|đỗ xe|đậu xe"` ⇒ 45 bài (35 ngoài thư mục món ăn: các chợ Đông Ba, Bến Ngự, An Cựu, Xép; hai phố đi bộ; Khu phố Tây; Đồi Vọng Cảnh; Hổ Quyền; các bãi biển…) và `-n -i -E "đèn flash|cấm chụp|flycam"` + dòng "chụp" trong bài Chùa Thiên Mụ ⇒ dòng lưu ý ở `heritage-guides.md` (biển báo cấm chụp ảnh / đèn flash ở khu bảo vật), `festival-guides.md`, `performing_arts_guides.md` (không bật flash khi diễn), `travel_guides.md` (tôn trọng khu vực cấm chụp), `Nhà thờ chính tòa Phủ Cam.md` (không dùng đèn flash), `Chùa Thiên Mụ.md` (tuân thủ quy định chụp ảnh, quay phim) [tự đếm; chỉ đọc dòng khớp]. Chưa thử câu hỏi thật về một trong các nơi đó — "có thể được trả lời một phần" là suy từ kho, chưa chạy. "Đợt đầu" ⇒ "đợt rà sửa cuối tháng 10" (dòng 8).
  - Số 51 mở / 7 tắt: lệnh đếm của lời giao đợt, 16:21 23/11 trên cây chính `da76649d` và `origin/main` `6619362c` [tự chạy]. Dòng Cập nhật trước (bản 16:30): 16:30, ngày 23/11/2026 · khớp hệ thống 16:21 23/11 (51 tính năng mở, 7 tắt, kho 267 bài) · hai mảng kho thiếu (chỗ đậu ô tô khu trung tâm, quy định chụp ảnh ở chùa / lăng / bảo tàng) nay là giới hạn chủ dự án chọn giữ, không bổ sung (12:22 23/11) · 17:11, ngày 22/11/2026: khớp hệ thống tối 22/11: kho 267 bài (thêm bài đường đi Hội An, sửa một dòng tự mâu thuẫn về Hải Vân Quan) · số bài đếm từ bản ghi chỉ mục; các số đo lấy từ báo cáo của những lần sửa và bổ sung kho từ 25/10 tới 22/11; người viết không chạy lại phép đo nào.
- Bảng vé và giờ có cấu trúc (19 / 20; 52 câu; khoảng 120 dòng): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 31.
- Đoạn số 1 của ví dụ chính: `data/hoc_cung_D/vi_du_di_suot_vet.json`.
- "Quán này mở từ 6 giờ sáng" là ví dụ tự đặt.
- Mục "Khi một giá đổi", "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn", "Câu hỏi tự kiểm" (thêm 13:43 22/11/2026 theo khuôn mới; gom từ mục "Vì sao không làm cách khác" cũ, "Đã so" và các nguồn trên). Hai lệnh sửa giá (chia việc chương trình / model / người duyệt; 37 · 9 · 1 · 27; ca Tự Đức 51 · 1 · 3 · 47; 13 câu tính từ giá cũ; chưa dùng trên kho thật): `bai_hoc/VIEC_MOI_XONG.md` mục 30 [đã chạy trên bản chép]; lý do "model chỉ phán, chương trình dựng dòng" và "chủ dự án chọn 22:22 21/11/2026": chú thích đầu `backend/ops/sua_kho.py` [code]; lệnh duyệt dừng khi dòng sửa nằm trong file điều kiện: `backend/ops/duyet_sua_kho.py` [code]; hai bài bảng giá gắn luật điều kiện, nhóm không làm tự sửa trọn: `session_prompt/HIEN_TRANG.md` mục "câu gác" (G-2, 12:38 22/11/2026). Lời chủ dự án "giá chỉ cần tương đối": `session_prompt/HIEN_TRANG.md` mục 4, gạch 09:25 22/11/2026 [quyết định đã ghi]; nhóm được tra nguồn rồi sửa chỗ sai: cùng mục, gạch 08:40 22/11/2026. Bảng quyền ("viết / sửa nội dung kho" hỏi chủ dự án trước): `AGENTS.md` mục "Quyền thường trực". Máy chủ đang chạy vẫn trả lời theo chỉ mục cũ; kiểm khớp chỉ lúc khởi động: chú thích đầu `backend/ingestion/cap_nhat_rieng.py`; lời báo lập chỉ mục lại: `backend/api/app.py` [code, đọc từ chương trình, chưa thử]. Câu từ chối: `backend/llm/full_corpus_prompt.py` (`INSUFFICIENT_ANSWER`); dòng nhắc: `MAY_HAVE_CHANGED_NOTICE` cùng file [code]. 21 giây cắt đoạn, "kho lớn gấp nhiều lần thì bước cắt thành phần chính": `bai_hoc/VIEC_MOI_XONG.md` mục 32 [đã chạy].
- Các mục mới đã qua một lượt đối chiếu độc lập (một agent khác chỉ đọc, 22/11/2026), các dòng sai / lệch đã sửa lúc 14:17: `data/hoc_cung_D/kiem/muc_moi_02_07_11_va_phu_luc.md` [riêng tư]. Lệnh duyệt dừng khi máy chủ đang chạy ("DỪNG, kho chưa đổi gì: server đang chạy"), lưu bản ghi git: `backend/ops/duyet_sua_kho.py` [code]. Lời dặn giữ điểm mâu thuẫn giữa các nguồn: `backend/llm/full_corpus_prompt.py` (`ANSWER_SYSTEM_INSTRUCTIONS`) [code]. Câu dẫn sang mục web: `frontend/src/moDauWeb.js` [code]. Máy chủ không bật khi đoạn mô tả của bảng điểm không còn trong chỉ mục: `backend/llm/lich_trinh_v2.py` (`kiem_doan_mo_ta`) [code].

- **Đợt đêm 23/11/2026 (cụm X: kho 269 bài).** Người viết đọc cây chính `07bbf67b` / `5a11e3f0`, không chạy test, không chạy server. Dòng Cập nhật trước: "Cập nhật 17:03, ngày 23/11/2026 · khớp hệ thống 16:21 23/11 (51 tính năng mở, 7 tắt, kho 267 bài); chưa gồm các bản gộp từ 16:38 (chờ phiếu) · chỗ đậu ô tô khu trung tâm và quy định chụp ảnh ở chùa / lăng / bảo tàng: chủ dự án chọn không bổ sung (12:22 23/11); đã áp biên bản kiểm độc lập · các mốc trước: khối Nguồn." Đếm 57 mở / 6 tắt: lệnh của lời giao [tự đếm].
  - 269 bài / 9.533 đoạn, số theo thư mục: `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (`corpus.file_count` 269, `chunk_count` 9.533, `qdrant.point_count` 9.533; đếm `corpus.sources` theo thư mục: restaurants 67 + cafes 24 + local_specialties 19 + 1 bài chung = 111, di tích 38 + 1 = 39, lễ hội 39 + 1 = 40, nghệ thuật 14 + 1 = 15, places 47, services 12, tickets 5); bản sao lưu trước lần cập nhật `data/full_corpus_builds/sao_luu/20261123_180502/` (267, 9.479); so `sources` hai bản: đúng 3 file đổi (`foods/food-guides.md`, hai bài `travel/places/` mới) [riêng tư; tự đếm bằng `python3`]. "65 đoạn tính lại, 32 giây": `session_prompt/HIEN_TRANG.md` mục 4 gạch "18:12 23/11/2026" điểm (3) (bản sổ `678f0b16`, 18:57, trước lần viết lại theo chủ đề 19:34; bản hiện tại chỉ còn mục 1 dòng "Kho và chỉ mục", không còn "65 đoạn") [chép sổ; không thấy bản ghi của lệnh trong `data/`; giờ 18:05 khớp tên thư mục sao lưu].
  - Hai bài mới: `git show --stat a8a8820f` (18:03; hai file `knowledge-base-hue/travel/places/`, 65 + 58 dòng; lời commit "written by the measuring session from public sources, read by the coordinator") [code]. Quán Nhỏ: `git show 39476168` (12:09; `foods/food-guides.md` 1 dòng; lời commit "the same guide (breakfast list) and the restaurant's own article both give its hours as 06:00–10:00; three public pages checked on 23/11/2026…", "Not merged until the index can be updated in the same step"), gộp `0ce3fe4f` 18:03 ("written by the coordinator, diff read by session B") [code; chép lời commit]. Quán Nhỏ không hợp bữa trưa ở bảng quán: `data/phase_9/lich_trinh/bang_quan_lich_v5.json` (`khong_bua` `['trua', 'toi']`) [riêng tư; tự đếm].
  - Lời chủ dự án: `data/loi_user/2026-11-23.md` dòng 24 (15:42, ô "Viết nháp 2–3 bài, tôi đọc rồi ghi (Recommended)"), dòng 40 (18:07, ô "Ghi cả hai (Recommended)") [riêng tư; chép]; quyết định đã ghi `HIEN_TRANG.md` mục 4 gạch "18:12 23/11/2026" điểm (3) (bản sổ `678f0b16`) ("GHI CẢ HAI BÀI NHÁP VÀO KHO (phương án khuyến nghị)") [chép sổ]. Nháp và trang tóm tắt: `data/bo_sung_kho_2026-11-23/nhap/` (hai nháp 17:05, 17:08; `TOM_TAT_CHO_CHU_DU_AN.md` 17:09: mục web lệch kho về phố đi bộ, chợ Đông Ba — "tôi KHÔNG sửa bài kho") [riêng tư; đã mở trang tóm tắt, không mở nội dung nháp]. Lần đầu của quy trình (bài Hội An 22/11): dòng Nguồn đầu của bài này [chép trong bài].
  - Lượt trình duyệt: `data/playwright_mcp/luot_2311_toi_v15/NHAT_KY.md` cảnh V6a, V6b, V6c, V7 ("269 bài trong kho tư liệu…"; nguồn "AEON Mall Huế", "Công viên ven sông Hương ở trung tâm Huế", "Chợ Đông Ba"; có ảnh) [riêng tư; đã mở; agent con, chưa có người thứ hai kiểm].
  - Chuyển xuống "Chi tiết để tra" (không bỏ thông tin) để giữ độ dài: hàng "dòng giá cần sửa là một câu mà file quy tắc lưu ý…" của bảng "Nếu… thì sao". Rút gọn trong thân bài: câu "Vài bài kho có dòng lẻ…" của quyết định 6 (đủ ở "Giới hạn đã biết"), "(số ở Chi tiết để tra)", "một bản ghi lịch sử được lưu" (đã ở "Quyết định nhỏ hơn"). Nửa để hiểu 13.298 ⇒ 13.291 ký tự (đo lại lúc áp biên bản: 13.292).
- **Áp biên bản kiểm độc lập tối 23/11/2026 (`data/hoc_cung_D/kiem/dot_2311_dem_k2_xep_lich_kho_kiem.md` mục "Bài 07" hàng 5, 6, 16 và hàng 12, 13 [riêng tư]).** Dòng Cập nhật trước: "Cập nhật 19:51, ngày 23/11/2026 · khớp hệ thống 19:49 23/11 (…)". Báo cáo lượt áp: `data/hoc_cung_D/viet/dot_2311_dem_a2_ap_xep_lich_kho.md` [riêng tư].
  - Không có lượt đo trước – sau trên bộ câu hỏi cho bài Hội An (22/11) và hai bài 23/11: `session_prompt/HIEN_TRANG.md` bản `678f0b16` dòng 108 điểm (3) (ghi kho + cập nhật chỉ mục, không có đo); `data/bo_sung_kho_2026-11-22/` chỉ có `c_ghi_hoi_an/` (`tim_3_cau.py` — "ba phép tìm CHỈ ĐỌC (không model) trước / sau khi ghi bài"; `hang_truoc.json` ↔ `hang_sau.json`: hai câu Hội An / tàu đổi 10 đoạn đầu, câu "giá vé Đại Nội" y hệt [tự so bằng `python3`]); `data/bo_sung_kho_2026-11-23/` chỉ có `nhap/`; không thấy tiêu chí "không làm hỏng" ghi trước cho hai lần này. Lý do bỏ bước đo: chưa thấy ghi [đã tìm các cụm "đo trước", "trước và sau", "trước – sau" trong sổ hiện trạng hai bản, `session_prompt/`, `guides/CACH_LAM_VIEC.md`, `skills/`: 0 chỗ nói về hai lần này]. Lượt 12 vai sau bài leo bậc: `bai_hoc/VIEC_MOI_XONG.md` mục 43 (13:50–14:04 22/11; "vai hỏi "3–4 điểm ít phải leo bậc" trượt cả ba lượt mốc, nay đạt"; đo gộp mọi đổi của hai ngày) [chép].
  - Trình tự giờ 23/11: `data/loi_user/2026-11-23.md` dòng 24 (15:42 "giờ ghi"), dòng 37 ("18:07 23/11/2026 (giờ ghi; chủ dự án về khoảng 17:53)"), dòng 40 ("Ghi cả hai (Recommended)") [riêng tư; chép]; `ls -la` `data/bo_sung_kho_2026-11-23/nhap/` (nháp 17:05, 17:08; tóm tắt 17:09) [riêng tư; tự chạy]; lời commit `a8a8820f` 18:03 ("two new articles the owner approved after reading the drafts") [chép]. Hai bài kho giống từng byte hai nháp: `cmp -s` từng cặp `nhap/<tên>.md` ↔ `knowledge-base-hue/travel/places/<tên>.md` ⇒ giống cả hai [tự chạy; không in nội dung].
  - Quán Nhỏ "cả bữa trưa lẫn bữa tối": `bang_quan_lich_v5.json` Quán Nhỏ `khong_bua` `['trua', 'toi']` [riêng tư; tự đếm].
  - Mọi con trỏ "`session_prompt/HIEN_TRANG.md` mục … gạch [giờ]" của các đợt trước trong khối này đọc ở bản `678f0b16` (18:57 23/11) — sổ viết lại theo chủ đề lúc 19:34 (`6c1e9a4c`); các gạch 08:40 22/11, 09:25 22/11, 22:06 21/11, 12:22 23/11, 18:12 23/11 đều còn ở bản đó. Riêng "câu gác (G-2, 12:38 22/11/2026)" chỉ có ở các bản sổ từ `dc0fd040` (12:38 22/11) tới trước `014c564f` (16:41 22/11) [đã chạy `git log -S`].
  - Để giữ độ dài: trình tự giờ của lần 23/11 chuyển từ thân bài xuống "Chi tiết để tra" (đã sửa thứ tự: chủ dự án chọn trước lần ghi kho 18:03; 18:07 là giờ ghi lời); "Cái giá" quyết định 6 rút gọn (đủ ở "Giới hạn đã biết"); tên mục "Mỗi lần thêm hay sửa kho là một lần đo trước và sau" ⇒ "Thêm hay sửa kho đi theo bốn bước"; tên quyết định 3 "thêm bài nào cũng đo lại" ⇒ "đợt thêm nhiều bài phải đo lại".
- Quét số cũ 20:46 23/11/2026: chỉ câu về mức test ở dòng Cập nhật ("chưa có lượt cả bộ test sau các bản gộp từ 16:20" ⇒ lượt 20:09); thân bài không đổi. Nguồn: `session_prompt/HIEN_TRANG.md` mục 1 và bảng `data/test_rong_2026-11-22/KET_QUA_c475f5e0.tsv` (95 file · 4 bỏ · 91 chạy · 2.307 ca đạt · một file đỏ, 1.171 giây; tự đếm 20:40–20:45 23/11/2026) [riêng tư]; số kho / tính năng của dòng Cập nhật khớp lệnh chạy 20:40 23/11/2026 (269 / 9533; 57 / 6) [đã chạy].
</details>
