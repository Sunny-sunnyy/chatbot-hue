# Bài 18 — Chấm bước tìm: đoạn đúng có lọt vào 10 đoạn không

*Cập nhật 12:15, ngày 22/11/2026 · cách chấm đọc từ chương trình đo; các số đo lấy từ các báo cáo từ 24/10 tới đầu tháng 11, trên kho của thời điểm đó; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** đề gồm 176 câu có đáp án mẫu, chia nhóm để thử và nhóm để kiểm lại.
**Bài này thêm:** nửa đầu của việc chấm. Chưa cần nhìn câu trả lời; chỉ xem 10 đoạn đưa cho model viết có chứa đáp án không. Chấm riêng bước này để biết khi một câu trả lời hỏng thì hỏng ở tìm hay ở viết.

## Ý chính

- Hệ thống được chấm ở **hai tầng riêng**: bước tìm (bài này) và câu trả lời (bài 19). Một câu trả lời hỏng có thể do tìm không ra đoạn đúng, hoặc do tìm ra mà viết sai; hai lỗi đó sửa ở hai chỗ khác nhau.
- Bước tìm có **hai thước**. Thước nhanh: dò từ khoá của đáp án trong 10 đoạn, chạy được trên cả 158 câu có đáp án trong kho. Thước chính xác: đánh dấu từng chỗ trong kho chứa đáp án (một agent đánh dấu, một agent khác kiểm lại, chủ dự án duyệt mẫu), chỉ có cho 55 câu khó.
- Thước nhanh dùng để theo dõi; thước chính xác dùng để chẩn đoán. Thước nhanh đã từng chẩn đoán sai.
- Mọi lần thử đổi cách cắt đoạn hay cách tìm dùng chung một điều kiện: **không câu nào đang đủ đoạn đúng được phép thành thiếu.**
- Kết quả trên 40 câu khó (kho cuối tháng 10): 33 câu có đủ đoạn đúng trong 30 ứng viên, nhưng chỉ 24 câu có đủ trong 10 đoạn. Lần đo gần nhất (19/11, 38 câu): 22 câu đủ trong 10 đoạn.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| điểm thứ hạng | **MRR** (mean reciprocal rank) | lấy 1 chia cho hạng của đoạn đúng đầu tiên (hạng 1 được 1, hạng 2 được 0,5…), rồi lấy trung bình; bằng 1 nghĩa là đoạn đúng luôn đứng đầu. Ở đây "đoạn đúng" tính cho từng từ khoá của đáp án (đoạn đầu tiên chứa từ khoá đó), trung bình trên các từ khoá của câu, rồi trên các câu |
| nDCG | **nDCG** (normalized discounted cumulative gain) | giống điểm thứ hạng nhưng tính cả việc nhiều đoạn đúng cùng đứng cao; từ 0 tới 1 |
| tỉ lệ tìm thấy | **recall** | trong những thứ cần tìm, tìm được bao nhiêu phần |
| nhãn đoạn đúng | **gold passages**, **relevance labels** | dấu do người (hoặc agent có người duyệt) đánh trong kho: chính chỗ này chứa đáp án của câu này |

## Chấm riêng bước tìm để biết hỏng ở đâu

Khi hệ thống trả lời sai hoặc từ chối một câu kho có, có hai khả năng rất khác nhau:

- **Tìm trượt:** đoạn có đáp án nằm trong kho nhưng không lọt vào 10 đoạn.
- **Viết trượt:** đoạn có đáp án đã ở trong 10 đoạn, nhưng model đọc sót hoặc viết sai.

Tìm trượt thì phải sửa bước tìm. Viết trượt thì phải sửa lời dặn hoặc model. Sửa nhầm chỗ thì vừa không chữa được, vừa có thể làm hỏng thứ khác. Vì vậy trước khi nhìn câu trả lời, phải biết 10 đoạn có đủ chưa.

## Thước nhanh: dò từ khoá của đáp án

Mỗi câu trong đề có vài từ khoá của đáp án (bài 17). Với mỗi từ khoá, chương trình xem đoạn đầu tiên chứa từ khoá đó đứng hạng mấy trong 10 đoạn. Từ đó ra ba con số trên 158 câu có đáp án trong kho (lần đo trên kho ngày 14/11):

| Số | Giá trị | Nghĩa |
|---|---|---|
| điểm thứ hạng (MRR) | 0,72 | đoạn chứa từ khoá của đáp án thường đứng hạng 1 hoặc 2 |
| nDCG | 0,75 | thứ tự tốt nhưng chưa hoàn hảo |
| tỉ lệ từ khoá tìm thấy trong 10 đoạn | khoảng 92 % | trung bình mỗi câu, gần hết từ khoá của đáp án có mặt |

Theo loại câu, điểm thứ hạng là 0,80 với câu một dữ kiện, 0,54 với câu nhiều nguồn, 0,53 với câu so sánh. Câu cần ghép nhiều chỗ thì kém rõ.

Thước này rẻ (không gọi model nào), chạy trên cả bộ, không cần người. Nhưng nó chỉ gần đúng: một đoạn chứa từ khoá chưa chắc chứa đáp án, và một đoạn nói đúng đáp án bằng chữ khác thì bị tính là trượt.

## Thước chính xác: đánh dấu đoạn nào chứa đáp án

Với 55 câu khó (40 để thử, 15 để kiểm lại), mỗi ý của đáp án mẫu được **đánh dấu từng chỗ** trong kho: chính câu chữ nào chứa ý đó. Một agent đánh dấu, một agent khác kiểm lại cả 55 câu, và chủ dự án duyệt khoảng 10 câu.

Cách chấm: một ý được coi là "có" khi chỗ được đánh dấu nằm trong các đoạn đang xét; một câu được coi là "đủ" khi **mọi** ý của nó đều có. Chấm ở hai tầng:

| Tầng | Số câu đủ đoạn đúng (trên 40 câu để thử) | Nghĩa |
|---|---:|---|
| trong 30 ứng viên | 33 | bước tìm theo nghĩa đã lấy về được phần lớn |
| trong 10 đoạn đưa cho model viết | 24 | 9 câu rơi mất ở khâu xếp thứ tự |

Đây là căn cứ của kết luận ở bài 13: 16 câu thiếu, trong đó 9 câu vì thứ tự, 7 câu vì không lọt cả 30 ứng viên.

Nhãn này phải làm lại mỗi khi kho đổi, vì sửa kho làm đổi câu chữ và chỗ đánh dấu cũ có thể không còn khớp. Nhãn đã qua sáu bản (bản thứ sáu làm ngày 14/11); chương trình đo hiện vẫn đọc bản thứ năm. Số chấm bằng hai bản nhãn khác nhau không so thẳng với nhau.

Với tin hỏi nhiều ý, từ 22/11 model được nối thêm tối đa 2 đoạn cho mỗi vế hỏi (bài 23); hai thước của bài này vẫn chỉ xét 10 đoạn đầu.

## Điều kiện chung cho mọi lần thử: không câu nào được mất đoạn đúng

Mọi lần thử đổi cách cắt đoạn, đổi model embedding, đổi cách trộn hay thêm bước xếp lại (bài 8 tới 14) đều dùng chung một điều kiện ghi trước, đo bằng thước chính xác: **0 câu đang đủ đoạn đúng thành thiếu.**

Điều kiện này đã loại: model embedding lớn (mất 3 câu), lấy 100 ứng viên (mất 1 câu), gộp đoạn to (mất 4 tới 6 câu), các model xếp lại chạy trên máy (mất 1 tới 3 câu).

Một cách dùng khác của cùng ý tưởng: nhiều thay đổi về sau không định đụng tới bước tìm (sửa lời dặn, thêm công cụ). Để chắc chúng thật sự không đụng, chương trình chạy bước tìm cho 158 câu, ghi lại 10 đoạn của từng câu theo thứ tự, rồi tính một dấu vân tay cho tất cả. Trước và sau thay đổi mà dấu giống hệt thì bước tìm không đổi, không cần chấm lại.

## Thước nhanh đã từng chẩn đoán sai

Ở bản đầu tiên (đưa 5 đoạn), 22 câu kho có bị từ chối. Nhìn bằng thước từ khoá, có 4 câu trông như đã đủ từ khoá trong ngữ cảnh mà model vẫn từ chối. Chẩn đoán lúc đó: "model viết quá rụt rè". Hướng sửa tự nhiên là dặn nó bớt rụt rè; làm vậy thì dễ khiến nó trả lời cả câu ngoài kho.

Khi có nhãn đoạn đúng, 22 câu đó được chấm lại bằng thước chính xác: **cả 22 câu đều thiếu đoạn đúng.** Bốn câu "đủ từ khoá" chỉ trùng chữ; đoạn đó không chứa đáp án. Model đã từ chối đúng, vì nó thật sự không được đưa đáp án.

Hướng sửa vì thế đổi hẳn: không dặn model bớt rụt rè, mà cho nó thấy nhiều đoạn hơn (10 đoạn, bài 13) và cho nó tìm thêm (bài 21).

## Quyết định và lý do

### 1. Vì sao chấm riêng bước tìm, mà không chỉ chấm câu trả lời cuối cùng cho gọn?

- **Đã chọn:** hai tầng chấm: bước tìm trước, câu trả lời sau (bài 19).
- **Vì sao:** đã gặp cái giá của việc chỉ nhìn câu trả lời. 22 câu từ chối nhầm từng được chẩn đoán là "model rụt rè"; chấm riêng bước tìm bằng nhãn đoạn đúng thì cả 22 câu đều thiếu đoạn đúng. Hai chẩn đoán dẫn tới hai hướng sửa ngược nhau.
- **Cách khác:** chỉ chấm câu trả lời cuối: đó là cách đã dẫn tới chẩn đoán sai ở trên.
- **Cái giá:** phải có nhãn đoạn đúng, là thứ tốn công làm và phải làm lại khi kho đổi.

### 2. Vì sao giữ cả hai thước, một nhanh một chính xác?

- **Đã chọn:** thước từ khoá cho cả 158 câu; thước nhãn đoạn đúng cho 55 câu khó.
- **Vì sao:** thước từ khoá không cần ai đánh dấu nên chạy được trên cả bộ, sau mọi thay đổi, không tốn tiền; nhưng nó đã chẩn đoán sai ở 4 câu. Thước chính xác sát hơn nhiều, nhưng chỉ có cho 55 câu, và cũng có chỗ hụt: một ý chỉ được đánh dấu ở một chỗ, nên đoạn khác trong kho nói lại cùng ý vẫn bị tính là thiếu.
- **Cách khác:** đánh dấu đoạn đúng cho cả 176 câu: chưa làm. Để một model tự phán "đoạn này có chứa đáp án không" ở mỗi lần đo, thay cho bộ nhãn cố định: chưa thử. (Bộ nhãn hiện có cũng do agent gắn, nhưng gắn một lần, có agent khác kiểm cả 55 câu và chủ dự án xem mẫu, rồi giữ cố định.)
- **Cái giá:** hai thước có thể nói khác nhau; khi đó tin thước chính xác.

### 3. Vì sao chấm ở hai chỗ: trong 30 ứng viên và trong 10 đoạn?

Bước tìm lấy về 30 đoạn ứng viên, rồi chỉ giữ 10 đoạn đứng đầu để đưa cho model (bài 13). Đoạn đúng có thể mất ở một trong hai chặng đó.

- **Đã chọn:** thước chính xác xem hai chỗ: đoạn đúng có nằm trong 30 đoạn lấy về không, và có còn nằm trong 10 đoạn được giữ lại không.
- **Vì sao:** để tách lỗi "không lấy về" khỏi lỗi "lấy về mà xếp thấp". Kết quả đã đổi hướng sửa: 33 trên 40 câu đủ trong 30 ứng viên nhưng chỉ 24 trong 10 đoạn, tức chỗ nghẽn là khâu xếp thứ tự; đây là căn cứ cho cả loạt thử bước xếp lại về sau (bài 14).
- **Cách khác:** chỉ chấm 10 đoạn cuối: không biết đoạn đúng mất ở chặng nào.
- **Cái giá:** thêm một tầng số phải đọc; tầng 30 ứng viên không nói gì về thứ model thật sự thấy.

### 4. Vì sao điều kiện là "0 câu mất đoạn đúng", mà không phải "trung bình tốt hơn"?

- **Đã chọn:** một thay đổi ở bước tìm bị loại nếu nó làm bất kỳ câu nào đang đủ đoạn đúng thành thiếu.
- **Vì sao** (lập luận): người dùng không gặp "trung bình"; họ gặp từng câu. Ví dụ thật: model embedding lớn giúp 2 câu và làm hỏng 3 câu đang tốt; tính gộp gần như hoà, nhưng với người hỏi 3 câu đó là hệ thống tệ đi.
- **Cách khác:** nhận thay đổi khi điểm trung bình tăng: không dùng ở bước tìm.
- **Cái giá:** điều kiện rất khắt khe. Cách xếp hạng 10 đoạn đầu cho câu một ý hầu như đứng yên từ cuối tháng 10, dù vẫn còn 16 trên 40 câu khó thiếu đoạn đúng. Đổi duy nhất ở bước tìm từ đó là việc tìm thêm theo từng vế cho tin hỏi nhiều ý (22/11); nó chỉ chạm tin nhiều ý nên được đo bằng một thước riêng trên tám tin, không bằng điều kiện của bài này.

Ba quyết định nhỏ hơn ở nửa để tra.

## Nếu… thì sao

| Nếu | Phải làm gì, hoặc chuyện gì xảy ra | Đã có chưa |
|---|---|---|
| một câu trả lời hỏng | trước hết xem 10 đoạn của câu đó có chứa đáp án không: thiếu thì sửa bước tìm, đủ thì sửa lời dặn hoặc xem lại model | đã có cách làm; với câu ngoài 55 câu có nhãn thì phải đọc bằng mắt |
| kho đổi câu chữ ở một bài | chỗ đánh dấu cũ có thể không còn khớp; phải làm bản nhãn mới | đã làm tới bản thứ sáu (14/11); chương trình đo **chưa** đọc bản đó; lần sửa kho 22/11 chưa có bản nhãn mới |
| kho thêm bài mới có đáp án tốt hơn cho một câu | nhãn cũ không biết bài mới; hệ thống tìm ra bài mới vẫn bị tính là trượt | **chưa có**: chưa bản nhãn nào xét lại xem bài mới thêm vào kho có chứa đáp án tốt hơn không |
| một thay đổi lẽ ra không đụng bước tìm mà dấu vân tay lại khác | dừng lại, tìm xem câu nào đổi 10 đoạn, trước khi đo tiếp | đã có |
| trợ lý tự tìm thêm, hoặc tin nhiều ý được nối thêm đoạn | hai thước không thấy; chúng chỉ chấm 10 đoạn của lần tìm đầu | chưa đổi thước; phần trợ lý đo bằng thước khác (bài 32) |
| kho lớn gấp mười | chạy lại thước nhanh (không tốn tiền) sẽ cho biết đoạn đúng của 158 câu cũ có bị bài mới đẩy ra khỏi 10 đoạn không; phần bài mới thì bộ câu chưa có câu để đo | chưa đo |

## Dễ nhầm

- **"Điểm thứ hạng cao là câu trả lời tốt."** Không. Nó chỉ nói đoạn đúng đứng cao; model vẫn có thể viết thiếu. Và nó thưởng cho một đoạn đúng đứng đầu, trong khi câu trả lời cần đủ mọi mảnh (bài 14).
- **"Dò từ khoá là đủ để biết tìm đúng hay sai."** Không. Nó từng cho ra một chẩn đoán sai ở 4 câu.
- **"Chấm bước tìm cần gọi model."** Không. Cả hai thước đều do chương trình tính, không tốn tiền.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Một câu kho có bị từ chối. Làm sao biết lỗi ở bước tìm hay ở bước viết?</summary>

Xem 10 đoạn đưa cho model có chứa đáp án không. Thiếu thì lỗi ở bước tìm, phải sửa bước tìm; đủ mà vẫn từ chối thì lỗi ở bước viết, phải sửa lời dặn hoặc xem lại model.

</details>

<details>
<summary>2. Thước nhanh và thước chính xác khác nhau thế nào?</summary>

Thước nhanh dò từ khoá của đáp án trong 10 đoạn, chạy trên cả 158 câu, không cần người, nhưng chỉ gần đúng. Thước chính xác dựa trên chỗ đã đánh dấu trong kho, chỉ có cho 55 câu khó. Nhanh để theo dõi, chính xác để chẩn đoán.

</details>

<details>
<summary>3. Chuyện "model rụt rè" đã dạy điều gì?</summary>

Thước từ khoá cho thấy 4 câu như đã đủ mà model vẫn từ chối. Chấm bằng nhãn đoạn đúng thì cả 22 câu từ chối nhầm đều thiếu đoạn đúng. Hướng sửa đổi từ "dặn model bớt rụt rè" sang "cho model thấy nhiều đoạn hơn và cho tìm thêm".

</details>

<details>
<summary>4. Vì sao 33 câu đủ trong 30 ứng viên mà chỉ 24 câu đủ trong 10 đoạn lại quan trọng?</summary>

Nó cho thấy đoạn đúng phần lớn đã được lấy về nhưng bị xếp thấp, nên chỗ cần sửa là khâu xếp thứ tự, không phải khâu lấy ứng viên.

</details>

## Cấu hình đang chạy

*Theo chương trình đo sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Thước nhanh | dò từ khoá của đáp án trong 10 đoạn; không phân biệt hoa thường; đã chuẩn hoá chữ có dấu | rẻ, chạy trên cả 158 câu | — |
| Thước chính xác | nhãn đoạn đúng cho 55 câu (40 để thử, 15 để kiểm lại) | chẩn đoán, và làm điều kiện cho mọi lần thử ở bước tìm | — |
| Bản nhãn chương trình đo đang đọc | bản thứ năm; bản thứ sáu (14/11) đã có trong dữ liệu nhưng chưa được nối vào chương trình đo | — | — |
| Các tầng được chấm | trong 30 ứng viên · trong 10 đoạn | tách lỗi "không lấy về" khỏi lỗi "lấy về mà xếp thấp" | — |
| Điều kiện cho mọi lần thử ở bước tìm | 0 câu mất đoạn đúng | một thay đổi "trung bình tốt hơn" không được làm hỏng câu đang tốt | — |
| Dấu vân tay của kết quả tìm | tính trên 10 đoạn của 158 câu | chứng minh một thay đổi không đụng tới bước tìm | — |

## Đã so

**Vấn đề thật đã gặp.** 22 câu kho có bị từ chối, và có hai cách giải thích trái nhau: model rụt rè, hay bước tìm không lấy ra đoạn đúng.

**So gì.** Cùng 22 câu, chấm bằng hai thước.

| Thước | Kết luận về 22 câu từ chối nhầm |
|---|---|
| từ khoá của đáp án | 4 câu "đã đủ từ khoá mà vẫn bị từ chối" ⇒ nghi model rụt rè |
| nhãn đoạn đúng | 0 câu đủ đoạn đúng; cả 22 đều thiếu ⇒ lỗi ở bước tìm |

**Đã chọn:** dùng nhãn đoạn đúng cho mọi chẩn đoán và mọi điều kiện ở bước tìm; giữ thước từ khoá để theo dõi trên cả bộ.

**Giới hạn của phép đo.** Làm cuối tháng 10, thời còn đưa 5 đoạn, model gpt-6-luna.

## Quyết định nhỏ hơn

**Vì sao tính một "dấu vân tay" cho kết quả tìm?** Ghi lại 10 đoạn của 158 câu theo thứ tự, gộp thành một chuỗi ký tự ngắn; chỉ cần một đoạn đổi chỗ là chuỗi đó đổi. Nhiều thay đổi không định đụng tới bước tìm (sửa lời dặn, thêm công cụ); so dấu trước và sau là cách rẻ để chứng minh điều đó: không gọi model, không cần chấm lại. Cái giá: dấu chỉ nói "có đổi hay không", không nói đổi tốt hay xấu.

**Vì sao chỉ 55 câu khó có nhãn?** Chưa thấy ghi lý do; hồ sơ chỉ ghi việc "gắn đoạn đúng cho 55 câu khó" ngày 24/10. Lập luận, không phải số đo: đánh dấu từng chỗ tốn công, nên làm cho loại câu dễ hỏng nhất.

**Vì sao chương trình đo vẫn đọc bản nhãn thứ năm khi bản thứ sáu đã có từ 14/11?** Chưa thấy ghi lý do; chưa ai nối bản sáu vào chương trình đo. Hệ quả: số 22 trên 38 ngày 19/11 chấm bằng bản năm.

Các lần thử bị điều kiện "0 câu mất đoạn đúng" loại, đủ danh sách: gộp đoạn to (mất 4 tới 6 câu), model embedding lớn (mất 3 câu), đổi cách tách từ cho tìm theo từ khoá (mỗi cách mất 1 câu), tìm độc lập toàn kho khi thử các cách trộn (mất 1 tới 2 câu), lấy 100 ứng viên (mất 1 câu), các model xếp lại chạy trên máy (mất 1 tới 3 câu).

## Giới hạn đã biết

- **Thước chính xác nhỏ:** 55 câu, nên nhiều lần thử chỉ ra được kết luận "chưa rõ". Một ý có thể chỉ được đánh dấu ở một chỗ; chỗ khác trong kho nói lại cùng ý mà chưa ai đánh dấu thì không được tính.
- **Thước nhanh gần đúng:** đoạn diễn đạt khác chữ bị tính trượt; đoạn trùng chữ mà không chứa đáp án bị tính trúng.
- **Các số của bài này đo trên kho từ cuối tháng 10 tới giữa tháng 11.** Từ đó kho thêm vài chục bài. Bản nhãn mới nhất (bản thứ sáu, 14/11) chỉ dời vị trí đánh dấu theo các bài đã sửa, chưa xét các bài thêm sau đó.
- **Cả hai thước chỉ nhìn bước tìm đầu tiên.** Chúng không đo việc trợ lý tự tìm thêm (bài 21).

## Chi tiết để tra

- Ba số của thước nhanh qua các lần đo: bản đầu tiên của hệ thống 0,72 / 0,755 / 92,4 %; kho đầu tháng 11: điểm thứ hạng 0,7216, nDCG 0,7554; kho ngày 14/11: 0,7188 / 0,7534 / 92,04 %. Cách xếp hạng 10 đoạn đầu gần như không đổi qua các giai đoạn: mọi lần thử đổi cách cắt đoạn, model embedding, cách trộn hay thêm bước xếp lại đều không qua được điều kiện; chỉ có việc chuẩn hoá chữ và số đoạn đưa cho model là được đổi.
- "92 %" là tỉ lệ từ khoá trung bình theo câu, không phải tỉ lệ câu.
- Trên cả 55 câu: 33 câu đủ đoạn đúng trong 10 đoạn; trung bình 76 % số ý có mặt.
- Số 24 trên 40 là theo bản nhãn thứ năm; bài 14 dùng số 22 trên 40 của một bản nhãn trước đó.
- Sau lần cập nhật riêng chỉ mục ngày 22/11, 176 câu mẫu cho cùng 10 đoạn như một lần lập lại toàn bộ (bài 12): đó là một lần dùng ý "so kết quả tìm" để chứng minh hai cách làm cho cùng kết quả.

**Bài sau (bài 19):** nửa sau của việc chấm: ai chấm câu trả lời, theo tiêu chí nào, và một lần chạy lệch bao nhiêu so với chính nó.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Hai thước, cách tính, ba tầng, dấu vân tay của kết quả tìm: `backend/evaluation/full_corpus_eval.py` (`keyword_mrr`, `score_retrieval`), `backend/experiments/phase_8_1/g1_retrieval.py` [code; chép qua `bai_hoc/10_CHAM_BUOC_TIM.md`, bài đã qua kiểm độc lập].
- Các con số (0,72 / 0,76 / 92 %; 0,80 / 0,54 / 0,53; 33 và 24 trên 40; 33 trên 55; 76 %; năm bản nhãn; chủ dự án duyệt khoảng 10 câu): `bai_hoc/10_CHAM_BUOC_TIM.md` và nguồn gốc `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md`, `10_BAO_CAO_DANH_GIA.md` [đã chạy].
- 22 câu từ chối nhầm, 4 câu "đủ từ khoá", chấm lại cả 22 đều thiếu: `bai_hoc/10_CHAM_BUOC_TIM.md` mục "Một chuyện thật"; `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 12 [đã chạy 25/10].
- Các lần thử bị điều kiện "0 câu mất đoạn đúng" loại: bài 8, 10, 13, 14 của giáo trình và nguồn của chúng.
- 16 = 9 + 7: `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_implementation.md`.
- 176 câu cho cùng 10 đoạn sau lần cập nhật riêng: `bai_hoc/VIEC_MOI_XONG.md` mục 32.
- Sáu bản nhãn, bản thứ sáu ngày 14/11 (chỉ dời vị trí, chưa thêm bài mới làm bằng chứng): `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` (theo biên bản kiểm `data/hoc_cung_D/kiem/bai_17_20.md`, bài 18 dòng 18); chương trình đo vẫn đọc bản thứ năm: `backend/experiments/phase_8_1/g1_retrieval.py` (`GOLD_PATH`). 22 trên 38 câu (19/11): `bai_hoc/VIEC_MOI_XONG.md` mục 10. Số của kho 14/11 (0,7188 / 0,7534 / 92,04 %): `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md`.
- Mục "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn" (sửa theo biên bản `data/hoc_cung_D/kiem/muc_moi_05_06_17_20.md` phần bài 18 [riêng tư]): gom từ các nguồn trên. "Thiếu thì sửa bước tìm, đủ thì sửa lời dặn" là cách làm ghi ở `skills/run-experiment/SKILL.md` (đo theo tầng). Ví dụ thật 2 giúp / 3 hỏng, danh sách lần thử bị loại (hàng 1, 2, 3, 5, 6, 8), chẩn đoán nghẽn ở xếp hạng (hàng 7): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md`. Nhãn do agent gắn, agent khác kiểm 55 / 55, chủ dự án xem mẫu (24/10): `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md`. Tìm theo vế (MỞ 09:47 22/11; 2 đoạn đầu mỗi vế, chỉ đoạn chưa có, nhiều nhất 6 vế; đoạn đúng vào ngữ cảnh 1 / 8 ⇒ 5 / 8): `backend/config/settings.yaml` (`tim_theo_ve`), `report_agent/2026-11-22/b_tim_theo_ve.md` [đã chạy]. Sửa kho 22/11 không kèm bản nhãn mới: `report_agent/2026-11-22/TONG_HOP.md` (không có dòng nào về nhãn). Lý do 55 câu và lý do vẫn đọc bản năm: không tìm thấy trong hồ sơ.

</details>
