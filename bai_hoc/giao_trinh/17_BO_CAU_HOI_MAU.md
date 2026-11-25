# Bài 17 — Bộ 176 câu hỏi mẫu: đề kiểm tra của hệ thống

*Cập nhật 20:30, ngày 25/11/2026 · cập nhật trạng thái các bộ câu kín của phần trợ lý sau lượt đo 25/11/2026 trên `gpt-6-luna` (bài 32, 40) · mốc trước: 20:46 23/11/2026 (số kho 269 bài; cấu tạo bộ câu đọc từ chương trình đo; các số đo lấy từ các báo cáo từ 24/10 tới 12/11, model viết gpt-6-luna; người viết không mở nội dung bộ câu và không chạy lại phép đo nào).*

**Bài trước đã biết:** đường hỏi đáp: tìm, viết, kiểm. Ở mỗi bài đều có những dòng "đã thử cách này, điểm tăng bao nhiêu, bỏ vì mấy câu tệ đi".
**Bài này thêm:** những con số đó đo trên cái gì. Trước khi chấm được thì phải có đề. Bài này nói về đề; hai bài sau nói về cách chấm.

## Ý chính

- Đề chính là **bộ 176 câu hỏi mẫu**: mỗi câu kèm đáp án mẫu, chia năm loại. Trong đó 18 câu là câu kho không có, để kiểm hệ thống có từ chối đúng không.
- Bộ được chia cố định thành **120 câu để thử** và **56 câu để kiểm lại**. Ở đợt rà soát cuối tháng 10, mọi lần thử chỉnh và quyết định trên nhóm thử; nhóm kiểm lại chỉ để xác nhận. Từ khi nhóm kiểm lại đã dùng, các lần thử về sau chạy trên cả bộ.
- Số chính của mọi lần chấm **bỏ 29 câu không tự nhiên** (câu không ai hỏi như vậy), vì thước đo phải sát với câu người dùng thật hỏi.
- Có thêm **bộ 32 câu an toàn** cho loại lỗi nặng nhất (vé, giờ, quy định, cảnh báo), và các **bộ câu cất riêng** mà người sửa hệ thống không được xem.
- Điểm trên bộ quen cao hơn thực lực: trên một bộ cất riêng, điểm "đủ ý" thấp hơn khoảng 0,4 trên thang 5.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| bộ câu hỏi mẫu | **golden set**, **evaluation set** | tập câu hỏi kèm đáp án đúng viết sẵn, dùng để chấm hệ thống |
| đáp án mẫu | **reference answer** | câu trả lời đúng viết sẵn cho một câu hỏi |
| nhóm để thử, nhóm để kiểm lại | **dev set**, **test set** | hai phần cố định của bộ câu: một phần để chỉnh hệ thống, một phần chỉ để xác nhận |
| bộ câu cất riêng | **held-out set** | bộ câu mà người sửa hệ thống không được đọc, chỉ dùng để chấm ở mốc cuối |
| học tủ | **overfitting** (với bộ đo) | hệ thống được chỉnh cho hợp đúng bộ câu đang dùng, nên điểm cao hơn thực lực |

## Bộ 176 câu, năm loại

Mỗi câu của bộ có bốn phần: câu hỏi, các từ khoá của đáp án, đáp án mẫu, và loại câu.

| Loại câu | Số câu | Hệ thống phải làm gì |
|---|---:|---|
| Một dữ kiện | 75 | tìm đúng một chỗ, nói đúng |
| Nhiều nguồn | 29 | ghép thông tin từ nhiều bài |
| Có điều kiện | 29 | giữ đúng điều kiện và ngoại lệ |
| So sánh | 25 | đặt hai thứ cạnh nhau, đủ cả hai bên |
| Ngoài kho | 18 | trả đúng câu từ chối cố định |

Ví dụ chính của giáo trình (hỏi giá vé một di tích) thuộc kiểu "một dữ kiện". Ví dụ "phải tìm thêm" (mặc áo dài có được miễn vé không) thuộc kiểu "có điều kiện".

Câu hỏi do AI soạn từ kho, có người duyệt. 158 câu có đáp án trong kho; 18 câu còn lại là câu về Huế mà kho không có.

## 120 câu để thử, 56 câu để kiểm lại

Nếu vừa chỉnh hệ thống vừa chấm trên cùng một bộ câu, sớm muộn hệ thống sẽ hợp với đúng bộ đó chứ không tốt lên thật. Để tránh, bộ 176 câu được chia một lần, cố định, giữ nguyên tỉ lệ các loại câu ở hai phần:

- **120 câu để thử:** ở đợt rà soát cuối tháng 10, mỗi lần thử một cách mới đều chỉnh và quyết định ở đây.
- **56 câu để kiểm lại:** không chỉnh theo. Chỉ chạy khi một cách mới đã thắng trên nhóm thử, để xem ở đây nó có cùng chiều và không làm hỏng gì không. Nhóm này nhỏ, nên không đòi thắng rõ thêm lần nữa.

Ví dụ đã gặp ở bài 13: đưa 10 đoạn thay vì 5 tăng 0,26 điểm trên nhóm thử, và tăng 0,27 trên nhóm kiểm lại. Nhóm kiểm lại cũng tăng, cùng chiều, và khoảng tin cậy của nó vẫn nằm trên 0 dù rộng (từ +0,02 tới +0,59). Đó là dấu hiệu mức tăng không chỉ do hợp với riêng nhóm thử.

Một nhóm kiểm lại chỉ dùng được một lần theo nghĩa này: đã nhìn kết quả trên nó thì nó không còn là "câu chưa ai thấy". Từ khi nhóm kiểm lại đã dùng, các lần thử về sau chạy trên cả bộ (129 câu tính điểm, mục kế tiếp) và chỉ trả lời được câu "thay đổi này có làm hỏng gì không" trên một bộ đã quen.

## Số chính bỏ 29 câu không tự nhiên

Hai agent đọc độc lập gắn nhãn cho từng câu: câu này có giống câu người dùng thật hay hỏi không.

| Nhãn | Số câu | Nghĩa |
|---|---:|---|
| tự nhiên | 82 | người dùng thật hay hỏi đúng kiểu này |
| chỉ để đo năng lực | 65 | không hẳn tự nhiên, nhưng đo được một năng lực cần (ví dụ ghép nhiều nguồn) |
| không tự nhiên | 29 | không ai hỏi như vậy (câu ghép gượng để đánh đố) |

Hai agent đồng ý với nhau ở mức cao (hệ số kappa 0,765; bằng 1 là đồng ý hoàn toàn, bằng 0 là như đoán bừa).

Luật rút ra: **số chính của mọi lần chấm bỏ 29 câu không tự nhiên.** Còn 147 câu, trong đó **129 câu có đáp án trong kho**. Vì vậy ở nhiều bảng của giáo trình, điểm được ghi là "trên 129 câu". Lý do: sản phẩm được đo như một sản phẩm thật; giỏi câu đánh đố mà kém câu thường thì không có giá trị.

## Bộ 32 câu an toàn, và bộ câu cất riêng

**Bộ 32 câu an toàn** dành cho loại lỗi nặng nhất theo thứ tự ở bài 4: sai về vé, giờ, quy định, cảnh báo. Gồm 28 câu kho có và 4 câu kho không có. Mỗi lần chấm bộ này báo đủ bốn số: số câu nói ngược cảnh báo của kho; số câu ngoài kho bị trả lời; số câu sai điều kiện (mới xuất hiện và đã hết); số câu thiếu cảnh báo (mới xuất hiện và đã hết). Hai số đầu luôn phải bằng 0. Hai số sau có ngưỡng ghi trước cho từng lượt đo: lượt 01/11 cho phép nhiều nhất 2 câu sai điều kiện mới; lượt 18/11 đòi cả hai bằng 0.

Bộ này có một người chấm riêng, chuyên đếm lỗi nặng. Người chấm đó được kiểm bằng 15 câu đối chứng: 10 câu trả lời bị cố ý chèn sai, 5 câu chép đúng. Nó phải bắt được ít nhất 9 trong 10 câu chèn sai và báo nhầm nhiều nhất 1 trong 5 câu đúng; nếu không, kết quả chấm của lượt đó không được dùng. Các lượt đã chạy đều bắt đủ 10 và không nhầm câu nào.

**Bộ câu cất riêng** là phần đề mà người sửa hệ thống (kể cả các coding agent) không được đọc. Chỉ một người chạy, ở mốc kiểm cuối, và chỉ báo ra số đếm. Bộ 176 câu có hai bộ cất riêng đi kèm, 36 câu và 40 câu; mỗi bộ đã mở một lần làm phép kiểm cuối (bộ 36 câu sau đó chỉ còn dùng để kiểm xem có làm hỏng gì không). Các tính năng của trợ lý có bộ câu kín riêng (bài 22, 25, 32).

## Đề quen cho số đẹp hơn thực lực

Ở lượt đo cuối của đường hỏi đáp (đầu tháng 11, model gpt-6-luna), hệ thống được chấm trên cả bộ quen và bộ cất riêng 40 câu:

| Điểm "đủ ý" (thang 1–5) | Bộ quen | Bộ cất riêng (34 câu kho có, trong 40 câu) |
|---|---:|---:|
| mọi câu | 4,58 | 4,18 |
| chỉ câu được trả lời | 4,82 | 4,60 |
| câu một dữ kiện | 4,97 | 4,42 |

Trên câu chưa ai thấy, điểm thấp hơn khoảng 0,4. Chênh lệch không chỉ do từ chối nhầm: tính riêng câu được trả lời vẫn thấp hơn. Mẫu của bộ cất riêng nhỏ (34 câu), nên con số của nó còn dao động. Khi nêu kết quả của hệ thống, nên nêu cả hai con số.

## Quyết định và lý do

### 1. Vì sao bộ câu do AI soạn từ chính kho, mà không lấy bộ có sẵn hay câu của người thật?

- **Đã chọn:** 176 câu do AI soạn từ kho của dự án, có người duyệt; đáp án mẫu viết từ chính kho.
- **Vì sao:** hệ thống chỉ trả lời từ kho của nó; một bộ câu có sẵn ở nơi khác sẽ hỏi những điều kho không có, hoặc có đáp án khác với kho (lập luận). Câu của người thật thì chưa có: hệ thống chưa đưa lên mạng.
- **Cách khác:** dùng một bộ câu có sẵn: chưa thử. Lấy câu người dùng thật hỏi: chưa làm được; khi có người dùng thật, đây là việc đầu tiên nên bổ sung.
- **Cái giá:** phải tự soạn, tự duyệt, tự sửa đáp án khi kho đổi. Câu AI soạn có thể không giống cách người thật hỏi; việc gắn nhãn "tự nhiên" bù được một phần.

### 2. Vì sao bỏ 29 câu không tự nhiên khỏi số chính, thay vì chấm cả 176 câu?

- **Đã chọn:** số chính tính trên 147 câu (129 câu có đáp án trong kho).
- **Vì sao:** chủ dự án quyết ngày 24/10: thước đo phải sát với câu người dùng thật hỏi. Giỏi câu đánh đố mà kém câu thường thì không có giá trị với sản phẩm.
- **Cách khác:** chấm cả 176 câu; hoặc chỉ chấm 82 câu tự nhiên: cách sau được giữ làm số phụ.
- **Cái giá** (lập luận, chưa đo): thước có thể dễ hơn một chút, vì câu ghép gượng để đánh đố không còn nằm trong số chính; 65 câu "đo năng lực" thì vẫn được giữ.

### 3. Vì sao trong đề có 18 câu mà kho không có đáp án?

- **Đã chọn:** 18 trên 176 câu là câu về Huế nhưng ngoài kho; đáp án mẫu của chúng là câu từ chối.
- **Vì sao:** luật gốc của sản phẩm là "0 câu ngoài kho được trả lời bằng kho" (bài 4). Không có loại câu này trong đề thì luật đó không đo được.
- **Cách khác:** chỉ đo từ chối bằng bộ an toàn (4 câu ngoài kho): chưa thấy ghi là đã cân.
- **Cái giá:** 18 câu là ít; trượt 1 câu đã là 1 trên 18. Lượt đo ngày 18/11 trượt đúng như vậy (bài 19).

### 4. Vì sao chia cố định thành nhóm để thử và nhóm để kiểm lại?

- **Đã chọn:** 120 và 56 câu, chia một lần (24/10), giữ tỉ lệ loại câu.
- **Vì sao:** lập luận chuẩn của việc đo, có từ lúc chia: chỉnh và chấm trên cùng một bộ thì hệ thống hợp dần với đúng bộ đó. Bằng chứng về sau cho thấy nỗi lo này có thật: ngày 01/11, trên bộ cất riêng, điểm "đủ ý" thấp hơn bộ quen khoảng 0,4.
- **Cách khác:** thử và chấm trên cả bộ: cách đang dùng từ khi nhóm kiểm lại đã dùng.
- **Cái giá:** nhóm kiểm lại nhỏ nên khoảng tin cậy rộng. Khi nhóm đã nhìn kết quả trên nhóm kiểm lại, nó không còn là câu "chưa ai thấy", nên lần sau dùng nó không chứng minh được điều gì mới.

### 5. Vì sao có bộ câu mà cả coding agent cũng không được đọc?

- **Đã chọn:** bộ câu cất riêng; chỉ một người chạy, ở mốc kiểm cuối, chỉ báo ra số đếm.
- **Vì sao:** người và agent sửa hệ thống đều đọc được bộ quen, nên có thể vô tình sửa cho hợp bộ đó. Bộ cất riêng là cách dự án dùng để có một con số không bị ảnh hưởng bởi việc đã đọc đề (lập luận).
- **Cách khác:** không có bộ cất riêng, chỉ chấm trên bộ quen: khi đó không biết được mức 0,4 ở trên.
- **Cái giá:** mỗi bộ chỉ "mới" được một lần. Hai bộ đi kèm bộ 176 câu đều đã dùng và chưa có bộ mới; từ 05/11 luật là chỉ cần bộ kín cho thay đổi chỉnh lời dặn qua nhiều vòng, vì đó là chỗ dễ học tủ nhất.

### 6. Vì sao cần riêng một bộ 32 câu an toàn?

- **Đã chọn:** một bộ nhỏ chỉ gồm câu về vé, giờ, quy định, cảnh báo, có người chấm riêng đếm lỗi nặng.
- **Vì sao** (lập luận; hồ sơ chỉ ghi bộ này dành cho loại lỗi tệ nhất): loại lỗi nặng nhất (bài 4) hiếm; trong bộ chung không đủ câu để thấy nó. Một điểm trung bình cao có thể che mất một câu sai cảnh báo.
- **Cách khác:** chỉ dựa vào bộ 176 câu: chưa thấy ghi là đã cân.
- **Cái giá:** bộ nhỏ: 0 lỗi trên 28 câu mới chỉ cho biết tỉ lệ lỗi dưới khoảng 10–12 % (bài 19).

Hai quyết định nhỏ hơn ở nửa để tra.

## Nếu… thì sao

| Nếu | Phải làm gì | Đã có chưa |
|---|---|---|
| kho sửa một giá vé hay giờ mở cửa | soát và sửa đáp án mẫu của các câu liên quan; sửa đáp án là đổi đề, nên điểm chấm trên đề cũ và đề mới không đặt cạnh nhau để so được | đã soát hai lần, bằng tay, sau hai đợt sửa kho (28/10: 0 câu phải sửa; 30/10: sửa 2 câu); sau lần sửa kho 22/11 (giá thuê thuyền, một giá vé) đã dò các con số cũ trên cả 176 câu: 0 câu có đáp án lệch giá mới |
| kho thêm bài mới | bộ câu không có câu nào về bài mới, nên không đo được phần đó | **chưa có**: số câu của bộ vẫn là 176 từ khi soạn, trong khi kho nay có 269 bài (từ 18:05 23/11) |
| đổi model viết | bộ câu dùng lại được; mọi con số phải đo lại | đã đổi model; bộ 176 câu chưa được chấm lại đủ trên model đang chạy |
| người chấm của bộ an toàn không bắt đủ câu đối chứng | bỏ kết quả chấm của lượt đó | đã có; chưa lượt nào bị bỏ |
| một người hay agent sửa hệ thống lỡ đọc bộ cất riêng | bộ đó chỉ còn giá trị như bộ quen; phải soạn bộ mới | có luật cấm mở; một lệnh tìm chữ riêng chỉ tìm trong bài của kho, bỏ qua các file đề; rào máy chặn đưa các bộ đó lên kho mã công khai |
| có người dùng thật | lấy câu họ hỏi làm đề, thay dần câu do AI soạn | chưa có người dùng thật |

## Dễ nhầm

- **"Điểm trên bộ 176 câu là chất lượng thật."** Đó là chất lượng trên một bộ đã quen. Trên bộ cất riêng thấp hơn khoảng 0,4.
- **"Bộ câu càng khó càng tốt."** Không. 29 câu không tự nhiên bị bỏ khỏi số chính chính vì chúng không giống câu người dùng hỏi.
- **"Nhóm kiểm lại dùng để chỉnh tiếp."** Không. Chỉnh theo nó là mất luôn tác dụng xác nhận.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Bộ 176 câu gồm những loại câu nào, và vì sao có 18 câu kho không có đáp án?</summary>

Một dữ kiện 75, nhiều nguồn 29, có điều kiện 29, so sánh 25, ngoài kho 18. Có 18 câu ngoài kho để đo luật "0 câu ngoài kho được trả lời bằng kho"; đáp án mẫu của chúng là câu từ chối.

</details>

<details>
<summary>2. "Điểm trên 129 câu" nghĩa là gì?</summary>

Số chính bỏ 29 câu không tự nhiên (còn 147 câu), rồi chỉ tính các câu có đáp án trong kho: 129 câu. Chủ dự án quyết như vậy để thước sát với câu người dùng thật hỏi.

</details>

<details>
<summary>3. Vì sao điểm trên bộ quen cao hơn thực lực, và dự án biết điều đó bằng cách nào?</summary>

Hệ thống được chỉnh dần trên bộ quen. Dự án biết nhờ bộ cất riêng 40 câu: ngày 01/11 điểm "đủ ý" ở đó là 4,18, so với 4,58 trên bộ quen.

</details>

<details>
<summary>4. Kho sửa một giá vé thì bộ câu phải làm gì?</summary>

Soát đáp án mẫu của các câu liên quan, sửa nếu lệch. Sửa đáp án là đổi đề, nên điểm trước và sau không so thẳng được. Đã soát ba lần (28/10, 30/10, 22/11). Lần 22/11: dò 9 mẫu con số cũ của hai chỗ sửa trên cả 176 câu; 2 câu chạm bài thuê thuyền, 0 câu chạm bài vé; 0 câu có đáp án lệch giá mới (hai câu chạm bài thuyền không dựa vào giá thuê). Phép này chưa cho biết câu trả lời của trợ lý cho hai câu đó có đổi sau khi sửa kho hay không.

</details>

## Cấu hình đang chạy

*Theo chương trình đo sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Số câu của bộ | 176 | — | thời hệ thống chỉ có nhóm món ăn dùng các bộ 104 câu và 45 câu (bộ 45 câu chỉ đo bước tìm); không so thẳng với bộ này |
| Các phần của một câu | câu hỏi · từ khoá đáp án · đáp án mẫu · loại câu | từ khoá dùng cho thước nhanh của bước tìm (bài 18); đáp án mẫu dùng để chấm câu trả lời (bài 19) | — |
| Chia nhóm | 120 để thử / 56 để kiểm lại, cùng tỉ lệ loại câu, cố định | chạy lại vẫn ra cùng cách chia | — |
| Bộ chạy nhanh | 10 câu lấy từ 176 câu | kiểm nhanh sau một sửa nhỏ | — |
| Câu bị bỏ khỏi số chính | 29 câu "không tự nhiên" | số chính sát với câu người dùng thật | — |
| Bộ an toàn | 32 câu (28 kho có, 4 kho không có) + 15 câu đối chứng | đo loại lỗi nặng nhất | — |
| Bộ cất riêng | 36 câu và 40 câu, đi kèm bộ 176 câu; cả hai đã dùng | số không bị học tủ | ở mốc 18/11, các bộ câu kín của phần trợ lý chưa chạy (`NOT RUN`); ngày 25/11, các bộ kín hỏi đáp và hội thoại (theo ngày, ngoài phạm vi, định tuyến – xã giao, chuỗi hỏi tiếp) đã chạy một lần trên `gpt-6-luna`, còn bộ kín sửa lịch vẫn chưa chạy được do bảng điểm đã đổi (bài 32) |
| Dấu của bản bộ câu | mỗi bản có một dấu vân tay | số chấm bằng bản cũ không so thẳng với số chấm bằng bản mới | — |

## Quyết định nhỏ hơn

**Vì sao bộ câu chỉ có câu gõ có dấu?** Chủ dự án quyết ngày 25/10: câu hỏi không dấu nằm ngoài phạm vi, vì thiết kế giả định người dùng gõ có dấu; cùng ngày chủ dự án cho thêm dấu vào mọi câu của bộ câu kín, thay cho bản "không dấu" của kế hoạch cũ. Cái giá đã đo: ở bước tìm, trên 32 câu, có dấu thì 13 câu có đủ đoạn đúng, bỏ dấu còn 1 câu (bài 10). Người gõ không dấu sẽ hay nhận câu từ chối.

**Vì sao mỗi bản bộ câu có một dấu vân tay?** Đáp án mẫu đã sửa hai lần (25/10: 10 đáp án cho gọn; 30/10: 2 đáp án cho khớp kho), nên điểm chấm bằng bản trước và bản sau không so thẳng được. Dấu vân tay (một chuỗi ký tự ngắn tính từ nội dung bộ câu) cho biết hai lần chấm có dùng cùng một bản hay không. Lý do này đọc ra từ hồ sơ hai lần sửa; chưa thấy một dòng ghi riêng vì sao làm dấu.

## Giới hạn đã biết

- **Chưa có câu nào do người dùng thật hỏi.** Mọi câu do AI soạn, kể cả bộ "viết theo kiểu người thật".
- **Bộ quen đã dễ.** 121 trên 176 câu đạt điểm tối đa ngay từ bản đầu tiên của hệ thống, nên bộ này khó thấy được cải tiến nhỏ.
- **Đáp án mẫu cũng cũ dần.** Giá vé, giờ mở cửa trong đáp án lấy theo kho của một thời điểm; kho sửa thì đáp án phải sửa theo. Đã sửa đáp án hai lần: 10 câu cho gọn, đúng điều được hỏi (25/10); và 2 câu cho khớp kho sau một đợt sửa kho (30/10).
- **Hai bộ cất riêng của bộ 176 câu đều đã dùng.** Luật hiện nay: chỉ cần bộ cất riêng cho những thay đổi chỉnh lời dặn qua nhiều vòng, là chỗ dễ học tủ nhất.
- **Bộ 176 câu chỉ có câu hỏi một lượt.** Hội thoại nhiều lượt và các việc của trợ lý được đo bằng các bộ khác (bài 32).

## Chi tiết để tra

- Việc gắn nhãn tự nhiên làm ngày 24/10; 9 câu hai lượt đọc không đồng ý được chủ dự án quyết, cả 9 giữ là tự nhiên.
- Bộ cất riêng 36 câu dùng ngày 28/10; bộ 40 câu dùng ở lượt đo ngày 01/11.
- Bộ an toàn ở lượt đo ngày 01/11: 0 câu nói ngược cảnh báo; 0 trên 4 câu ngoài kho bị trả lời; 2 câu sai điều kiện (mức cho phép lúc đó là nhiều nhất 2).
- Tính lại điểm của bộ cất riêng theo đúng tỉ lệ loại câu của bộ quen vẫn ra khoảng 4,20, nên chênh lệch không phải do bộ cất riêng nhiều câu khó hơn.
- Từ tối 21/11, nhóm quyết định chạy và chấm mọi phép đo mới bằng model đang chạy (Claude Sonnet 5.5); số mới không so thẳng với các số trong bài này (bài 19 kể đủ lịch sử người chấm).

**Bài sau (bài 18):** nửa đầu của việc chấm: chưa nhìn câu trả lời, chỉ xem 10 đoạn đưa cho model có chứa đáp án không.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Cấu tạo bộ câu (4 phần, 5 loại, 75 / 29 / 29 / 25 / 18, bộ 10 câu), cách chia 120 / 56: `backend/evaluation/golden_full_corpus.py`, `backend/evaluation/full_corpus_eval.py` (`make_split`) [code; chép qua `bai_hoc/09_BO_CAU_HOI_MAU.md`, bài đã qua kiểm độc lập].
- Nhãn tự nhiên 82 / 65 / 29, kappa 0,765, 9 câu chủ dự án quyết, luật bỏ 29 câu, 147 / 129 câu: `bai_hoc/09_BO_CAU_HOI_MAU.md` và nguồn gốc `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` [đã chạy 24/10].
- Bộ an toàn (32 câu, 4 số, 15 câu đối chứng, kết quả 01/11), bộ cất riêng (36 / 40 câu, luật dùng), sửa đáp án (10 câu, 2 câu), bảng bộ quen so với bộ cất riêng, 121 / 176 câu đạt tối đa: `bai_hoc/09_BO_CAU_HOI_MAU.md` [đã chạy; chép].
- +0,26 nhóm thử, +0,27 nhóm kiểm lại: `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 10.
- Mọi phép đo từ tối 21/11 chạy và chấm bằng model đang chạy: `session_prompt/HIEN_TRANG.md` mục 4, gạch 21:43 và 21:50 21/11/2026.
- Người viết không mở file bộ câu; bài không chép câu nào của bộ.
- Mục "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn" (sửa theo biên bản `data/hoc_cung_D/kiem/muc_moi_05_06_17_20.md` phần bài 17 [riêng tư]): chủ dự án quyết bỏ câu không tự nhiên 24/10 21:40, "chỉ tự nhiên" là số phụ (24/10 21:58), không dấu ngoài phạm vi và thêm dấu cho câu kín (25/10 15:15 và chiều 25/10): `session_prompt/Project_Status.md` (bảng quyết định); chia 120 / 56 từ 24/10: `Project_Status.md` dòng về đợt 8.1; luật bộ kín 05/11, "khi có người dùng thật": `bai_hoc/09_BO_CAU_HOI_MAU.md`; soát đáp án sau sửa kho 28/10 (0 câu) và 30/10 (2 câu): `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md`; sửa kho 22/11 (thuyền, vé Lê Bá Đảng) và "176 câu mẫu 0 lệch" là phép so bước tìm, không phải soát đáp án: `report_agent/2026-11-22/TONG_HOP.md`; không tìm thấy hồ sơ soát đáp án theo lần sửa này (tìm trong `report_agent/2026-11-22/`, `VIEC_DANG_MO.md`; không mở bộ câu); lượt 18/11 trượt 1 / 18: `bai_hoc/VIEC_MOI_XONG.md`; 267 bài: `session_prompt/HIEN_TRANG.md` mục 1; 13 ⇒ 1 câu không dấu: bài 10 mục "Giới hạn đã biết". Phần cũ gom từ biên bản kiểm `data/hoc_cung_D/kiem/bai_17_20.md` (nhóm kiểm lại đã dùng, khoảng tin cậy +0,024 tới +0,585; bốn số của bộ an toàn theo `skills/run-experiment/SKILL.md`; ngưỡng câu đối chứng 9 / 10 và 1 / 5; bộ 104 và 45 câu thời nhóm món ăn; 34 câu kho có của bộ cất riêng; lý do hai lần sửa đáp án). Luật câu kín và lệnh tìm riêng: `AGENTS.md` luật cứng 3. "Số câu của bộ vẫn là 176": `backend/evaluation/golden_full_corpus.py` [người viết không mở nội dung].

- Soát đáp án mẫu sau lần sửa kho 22/11 (9 mẫu số cũ, 176 câu, 2 câu chạm, 0 câu lệch): phiên đo đếm 12:27 22/11/2026, một phiên, không tốn tiền; phiên điều phối chuyển lời [đã chạy; người viết chép từ tin, chưa tự mở kết quả].
- Quét số cũ 20:46 23/11/2026: bảng "Nếu… thì sao" hàng "kho thêm bài mới": "kho nay có 267 bài" ⇒ 269. Lệnh: `corpus.file_count` / `corpus.chunk_count` của `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json` (269 / 9533) và đếm dòng `: true` / `: false` dưới `assistant:` của `backend/config/settings.yaml` (57 / 6), chạy 20:40 23/11/2026 trên cây chính `03229b64` [đã chạy].
- Cập nhật 20:30 25/11/2026: trạng thái bộ câu kín của phần trợ lý ở bảng "Cấu hình đang chạy" theo `report_agent/2026-11-25/E_BO_CAU_KIN_LUNA_2511.md` (chạy 25/11 trên `main` `ea96e47c`, `gpt-6-luna`; Mốc 1 18/11 là `NOT RUN`; Mốc 2 25/11 chạy K, S ×2, T, C kín, còn L kín `NOT RUN`) [đã duyệt].

</details>
