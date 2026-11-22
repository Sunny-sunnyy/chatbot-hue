# Bài 20 — Một thí nghiệm được làm thế nào, và nhìn cả bảng các lần so sánh thấy gì

*Cập nhật 15:16, ngày 22/11/2026 · các bước lấy từ quy trình đo của dự án; các ví dụ và con số lấy từ bảng tổng 45 lần so sánh đã ghi (từ cuối tháng 8 tới 19/11), phần lớn đo với gpt-6-luna; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** đề (bài 17), cách chấm bước tìm (bài 18), cách chấm câu trả lời và mức nhiễu (bài 19).
**Bài này thêm:** ghép ba thứ đó thành một cách làm. Mỗi dòng "đã thử, giữ" hay "đã thử, bỏ" trong giáo trình đều đi qua cùng một chuỗi bước. Cuối bài nhìn cả bảng các lần so sánh để thấy điều gì lặp lại.

## Ý chính

- Mỗi thay đổi ở một khâu đo được (cắt đoạn, tìm, ngữ cảnh, lời dặn, model, công cụ, cách chấm) là một **thí nghiệm**: ghi điều kiện đạt hay trượt **trước khi chạy**, đo bản đang chạy làm mốc, **đổi đúng một thứ**, đo lại cùng cách, rồi kết luận theo điều kiện đã ghi. Sửa một lỗi nhỏ đã rõ nguyên nhân thì không cần.
- Điều kiện có hai lớp: **điều kiện không được vỡ** (gồm các sàn bằng 0 và mức tụt cho phép; vỡ thì mặc định là bỏ, dù trung bình tốt hơn) và **mức phải đạt** của đúng thứ thay đổi nhắm tới (chất lượng thì phải vượt mức nhiễu; tốc độ thì phải nhanh hơn một mức ghi trước).
- Thắng trên nhóm câu để thử thì trên nhóm câu để kiểm lại phải **cùng chiều và không làm hỏng gì**.
- Kết quả âm cũng được giữ hồ sơ. Hơn một nửa số lần thử của dự án kết thúc bằng "bỏ"; đó là căn cứ để trả lời "vì sao không làm cách X".
- Nhìn cả bảng 45 dòng: phần lớn các lần thắng về chất lượng thuộc hai kiểu, đưa model **thêm bằng chứng** hoặc **giao việc dễ sai cho chương trình**. Model embedding lớn hơn và các cách xếp lại "thông minh hơn" chưa thắng lần nào.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| mốc | **baseline** | kết quả của bản đang chạy, đo lại ngay trước khi thử, để so vào |
| điều kiện ghi trước | **pre-registered criteria** | thế nào là đạt, thế nào là trượt, viết ra trước khi thấy con số nào |
| biến thể | **variant** | một bản của hệ thống khác bản đang chạy đúng một điểm |
| câu tệ đi | **regression** | câu mà biến thể trả lời kém hơn mốc |

## Sáu bước của một thí nghiệm

1. **Nêu lớp vấn đề, không nêu một câu.** "Dòng bảng giá bị tách nên bước tìm bỏ sót" là một lớp vấn đề. "Câu số 81 trả lời sai" thì không: sửa cho một câu dễ thành sửa để qua đúng câu đó.
2. **Ghi điều kiện trước khi chạy.** Đo bằng thước nào, so với mốc nào, tăng bao nhiêu thì gọi là thắng, và những điều nào không được vỡ.
3. **Đo mốc.** Chạy lại bản đang chạy, cùng bộ câu, cùng cách đo, cùng người chấm. Ở khâu có model (lời dặn, ngữ cảnh, model viết), mốc phải chạy cùng buổi với bản thử, vì model tự lệch giữa các lần chạy. Ở khâu chương trình tính (bước tìm), mốc cũ dùng lại được nếu chạy lại ra đúng y kết quả cũ.
4. **Đổi đúng một thứ**, rồi đo lại đúng những câu đó.
5. **So theo cặp, theo tầng.** Từng câu một, biến thể so với mốc (bài 19); và nếu lỗi có thể nằm ở nhiều chỗ thì tách bước tìm khỏi câu trả lời (bài 18).
6. **Kết luận theo điều kiện đã ghi**, bằng một trong bốn chữ: tốt hơn, không khác, kém hơn, chưa rõ. Thắng trên nhóm để thử thì chạy thêm nhóm để kiểm lại. Ghi hồ sơ, kể cả khi bỏ.

Trước bước 3 còn một bước rẻ: **đếm cỡ mẫu**. Trong bộ câu có bao nhiêu câu thật sự có thể đổi kết quả nhờ thay đổi này? Nếu chỉ có 3 câu thì dù thắng cả 3 cũng chưa kết luận được gì. Khi đó phải ghi trước rằng kết quả có thể chỉ là "chưa rõ", và mở rộng bộ câu hoặc đổi câu hỏi của thí nghiệm trước khi chạy.

## Vì sao phải ghi điều kiện trước

Khi đã thấy con số, rất dễ tìm ra một cách đọc khiến nó trông như thắng: đổi thước, bỏ vài câu, nới một ngưỡng. Ghi trước thì không làm vậy được.

Ví dụ thật ở bài 14. Bản "để model viết chọn 10 trong 30 đoạn" tăng điểm trung bình và chữa gần hết lỗi thứ tự. Nếu chỉ nhìn kết quả, nó là một lần thắng. Nhưng điều kiện ghi trước nói: nhiều nhất 4 câu được phép tệ đi. Có 5 câu. Nó bị gác.

Ví dụ thật ở bài 15. Một câu dặn mới chữa được một lỗi an toàn, nhưng bản dặn rộng làm số câu từ chối nhầm lên 7, vượt ngưỡng 5 đã ghi. Bản đó bị bỏ; bản dặn hẹp hơn qua được điều kiện thì mới được giữ.

Nếu ngưỡng được nới sau khi thấy số, mọi con số khác của dự án cũng mất giá trị, vì không ai biết ngưỡng nào đã được nới.

## Hai lớp điều kiện: không được vỡ, và phải thắng

**Điều kiện không được vỡ** áp cho mọi thí nghiệm, dù nó nhằm vào việc gì:

- 0 câu ngoài kho được trả lời bằng kho;
- bộ an toàn không xấu đi;
- ở bước tìm: 0 câu đang đủ đoạn đúng thành thiếu;
- số câu tệ đi không vượt một ngưỡng tính từ mức nhiễu.

**Mức phải đạt** áp cho đúng thứ mà thay đổi nhắm tới:

- thay đổi nhằm tăng chất lượng: mức tăng phải vượt mức nhiễu, khoảng tin cậy không chứa 0, và trên nhóm để kiểm lại phải cùng chiều;
- thay đổi nhằm tốc độ hay tiền: phải nhanh hơn hoặc rẻ hơn một mức ghi trước. Ví dụ thật: một cách làm nhanh hơn 0,87 giây trong khi mức ghi trước là 1,5 giây, nên bị bỏ dù không làm hỏng gì;
- sửa kho, thêm tính năng: chỉ cần qua lớp thứ nhất.

Phần lớn các lần "bỏ" của dự án là do vỡ lớp thứ nhất, không phải do trung bình kém: gộp đoạn to, model embedding lớn, xếp lại bằng model, trả lời một phần, tắt phần suy luận ở bước xếp loại câu.

## Đếm trước khi xây

Một thí nghiệm tốn công xây biến thể và tốn tiền chạy. Trước đó thường có một phép đếm không tốn gì, trên dữ liệu đã có: lỗi mà thay đổi này nhắm tới xảy ra bao nhiêu lần?

Ví dụ thật: trước khi đổi cách đưa công cụ cho model, nhóm chạy lại luật chọn công cụ trên 310 câu khác nhau đã được gõ vào hệ thống trên máy phát triển (chủ dự án và nhóm gõ khi dùng thử), xem cách hiện tại bỏ sót bao nhiêu: 4 trên 60 câu cần công cụ (bài 21). Ngày 12/11, ba ý tưởng bị dừng ngay ở bước đếm này: lỗi tưởng là có thì không đủ nhiều để đáng xây.

## Nhìn cả bảng các lần so sánh thấy gì

Dự án giữ một bảng tổng 45 lần so sánh chính, từ kho tới trợ lý (phụ lục C sẽ chép đủ). Bảy điều lặp lại trong bảng đó:

1. **Phần lớn các lần thắng về chất lượng thuộc hai kiểu.** Đưa model thêm bằng chứng (10 đoạn thay vì 5; cho tìm thêm), hoặc giao việc dễ sai cho chương trình (ngày tháng, xếp lịch, luật tra web). Model embedding lớn hơn và các cách xếp lại thông minh hơn đều chưa thắng. (Ngoài bảng này, việc đổi model viết sang Claude Sonnet 5.5 ngày 21/11 cho số tốt hơn ở một thước nhỏ của phần trợ lý; đó là đổi tạm và chưa so trên cả bộ, bài 33.)
2. **Phần lớn lần bỏ là vì vỡ một điều kiện**, không phải vì trung bình kém.
3. **Thêm một thứ vào lời dặn hay vào bộ công cụ có thể làm hỏng một câu an toàn ở chỗ khác.** Vì vậy mọi lần thử ở phần trợ lý đều có tầng an toàn: chạy lại bộ câu an toàn, hoặc chứng minh chuỗi chữ gửi model không đổi rồi dùng lại số cũ.
4. **Đo riêng một bước có thể đánh lừa.** Một dịch vụ tìm web khác thắng khi đo riêng bước tra; đi qua cả đường của người dùng thì lợi biến mất.
5. **Có những thứ không cần thử**, vì phép đếm trước đã cho thấy lỗi không đủ nhiều.
6. **Người chấm chỉ chấm được thứ họ thấy.** Một luật chọn khu ở từng được chấm 10 trên 10, nhưng bảng đưa cho người chấm thiếu cột buổi tối; người đọc lại lịch mẫu mới bắt được lỗi.
7. **Vài thứ đáng thử lại**, vì lần thử cũ làm ở một cấu hình đã khác: xếp lại bằng model chạy trên máy mới thử thời còn đưa 5 đoạn.

## Quyết định và lý do

### 1. Vì sao phải ghi điều kiện trước, mà không cứ thử rồi nhìn kết quả mà quyết?

- **Đã chọn:** thế nào là đạt, thế nào là trượt được viết ra trước khi có con số nào.
- **Vì sao:** quyết định đã ghi trong cách làm việc của dự án. Đã thấy con số rồi thì rất dễ tìm một cách đọc khiến nó trông như thắng. Hai ví dụ thật ở trên (model viết chọn đoạn; câu dặn rộng) là hai lần mà nhìn kết quả thì sẽ nhận, còn điều kiện ghi trước thì loại.
- **Cách khác:** quyết sau khi nhìn kết quả: không dùng.
- **Cái giá:** luật ghi trước không phân biệt "quá một câu" với "quá mười câu". Có lần một thay đổi tăng điểm trung bình vẫn bị bỏ vì có 5 câu tệ đi, quá ngưỡng 4 đúng một câu (bản đó cũng chậm hơn và tốn gấp 3,8 lần, nên bỏ không tiếc).

### 2. Vì sao mỗi lần chỉ đổi một thứ?

- **Đã chọn:** biến thể khác bản đang chạy ở đúng một điểm.
- **Vì sao:** đổi vài thứ cùng lúc thì không biết thứ nào gây ra kết quả. Đã gặp: mức giảm từ chối nhầm từ 22 xuống 12 gộp ba thay đổi (10 đoạn thay vì 5, chuẩn hoá chữ có dấu, bản mới của bộ kiểm số nguồn), nên không tách được phần của riêng "10 đoạn" (bài 13).
- **Cách khác:** đổi nhiều thứ một lần: chính là ca vừa kể.
- **Cái giá:** chậm. Ba ý tưởng là ba lần đo.

### 3. Vì sao giữ hồ sơ cả những lần bị bỏ, và đếm trước khi xây?

- **Đã chọn:** mỗi lần thử, kể cả lần âm, có một dòng trong bảng tổng: thử gì, so với gì, ra số nào, vì sao bỏ. Trước khi dựng một biến thể, đếm trên dữ liệu đã có xem lỗi nó nhắm tới xảy ra bao nhiêu lần.
- **Vì sao:** hồ sơ lần bỏ là căn cứ để trả lời "vì sao không làm cách X", và để không thử lại thứ đã thử; hơn một nửa số dòng của bảng là lần bỏ. Phép đếm không tốn tiền, còn dựng và đo thì tốn công và tiền (lập luận); ngày 12/11 ba ý tưởng dừng ở bước đếm.
- **Cách khác:** chỉ ghi lần thắng; dựng thử ngay mọi ý tưởng: không dùng.
- **Cái giá:** công ghi chép; một kết luận "bỏ" có thể đã cũ khi cấu hình đổi, nên bảng phải ghi dòng nào đáng thử lại. Phép đếm chỉ thấy lỗi đã có dấu vết trong dữ liệu cũ.

### 4. Vì sao có lúc vẫn giữ một thay đổi dù một điều kiện bị vỡ?

- **Đã chọn:** vỡ điều kiện thì mặc định bỏ; chỉ giữ khi chứng minh được chỗ vỡ không do thay đổi, hoặc khi đổi cách dùng để người dùng chặn được lỗi đó, và luôn ghi lý do.
- **Vì sao:** hai ca thật. Một thay đổi ở phần trợ lý làm 3 câu đổi sang từ chối, tức vỡ theo chữ; nhưng chạy lại bản chưa đổi cũng ra đúng 3 câu đó (bài 21). Chức năng hỏi bằng ảnh gán tên Huế cho 2 trên 5 ảnh không phải Huế, quá ngưỡng 1; nó được giữ ở dạng có bước xác nhận (bài 26): lúc đầu người dùng phải bấm xác nhận mọi tên hệ thống đoán; nay đoán ra một tên thì hỏi luôn kèm dòng báo "có thể sai", hai ba tên mới phải bấm chọn.
- **Cách khác:** không bao giờ có ngoại lệ: hai thay đổi trên sẽ bị bỏ.
- **Cái giá:** mỗi ngoại lệ làm luật yếu đi một chút, nên phải có người kiểm độc lập đồng ý.

### 5. Vì sao từ 21/11 bớt số lượt đo?

- **Đã chọn:** thay đổi rủi ro cao hay chạm nhiều đường thì thử nhiều, thay đổi nhỏ thì thử ít; bỏ các lượt đo lặp lại không làm đổi quyết định nào.
- **Vì sao:** chủ dự án nhận xét tối 21/11: nhóm đo phần hỏi đáp quá nhiều mà không thực sự cần, mất thời gian, ảnh hưởng tiến độ; đồng thời dặn không đặt con số cố định và không để chất lượng tụt vì bớt đo.
- **Cách khác:** số lượt đo cố định: chủ dự án dặn không làm.
- **Cái giá:** ít lượt lặp hơn thì kết luận ở thay đổi nhỏ kém chắc hơn.

Bốn quyết định nhỏ hơn ở nửa để tra.

## Nếu… thì sao

| Nếu | Phải làm gì | Đã có chưa |
|---|---|---|
| kết quả là "chưa rõ" | không đưa vào vì lý do chất lượng; ghi hồ sơ; muốn biết thì mở rộng bộ câu rồi đo lại | đã có |
| thắng trên nhóm để thử nhưng ngược chiều trên nhóm để kiểm lại | không nhận | đã có luật; chưa thấy lần nào bị loại vì lý do này |
| một điều kiện vỡ nhưng nghi không do thay đổi | chạy lại bản chưa đổi; nếu nó cũng ra đúng những câu đó thì chỗ vỡ không do thay đổi | đã làm một lần (quyết định 4) |
| đo riêng một bước thì thắng, đo cả đường của người dùng thì không | theo kết quả của cả đường | đã gặp: một dịch vụ tìm web khác thắng khi đo riêng, gần như hoà khi qua máy chủ thật (bài 25); nay thành luật (nửa để tra) |
| người chấm không được đưa đủ thứ để chấm | một người đọc lại vài mẫu bằng mắt | đã gặp ở luật chọn khu ở (ý 6 ở trên; bài 30) |
| đổi model viết | mốc cũ không so thẳng được; phải đo mốc mới. Các kết luận "bỏ" cũ có thể không còn đúng với model mới | đã đổi model; mốc mới trên cả bộ **chưa có** |

## Dễ nhầm

- **"Thử thấy tốt hơn là đưa vào."** Không. Phải qua điều kiện ghi trước, và thắng lại trên nhóm để kiểm lại.
- **"Kết quả âm là công cốc."** Không. Nó là căn cứ để nói "đã thử cách đó, và đây là lý do không dùng".

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Kể sáu bước của một thí nghiệm.</summary>

Nêu lớp vấn đề · ghi điều kiện trước · đo mốc (cùng buổi nếu khâu đó có model) · đổi đúng một thứ · so theo cặp và theo tầng · kết luận theo điều kiện đã ghi, giữ hồ sơ cả khi bỏ.

</details>

<details>
<summary>2. Hai lớp điều kiện là gì?</summary>

Điều kiện không được vỡ, áp cho mọi thay đổi (0 câu ngoài kho được trả lời, bộ an toàn không xấu đi, 0 câu mất đoạn đúng, số câu tệ đi trong ngưỡng). Và mức phải đạt của đúng thứ thay đổi nhắm tới: chất lượng thì vượt nhiễu, tốc độ thì nhanh hơn một mức ghi trước.

</details>

<details>
<summary>3. Vì sao bản "để model chọn 10 trong 30 đoạn" bị gác dù điểm trung bình tăng?</summary>

Điều kiện ghi trước cho phép nhiều nhất 4 câu tệ đi; bản đó có 5. Nó cũng chậm hơn và tốn gấp 3,8 lần.

</details>

<details>
<summary>4. Nhìn cả bảng 45 lần so sánh, phần lớn lần thắng về chất lượng thuộc kiểu nào?</summary>

Đưa model thêm bằng chứng (10 đoạn, cho tìm thêm), hoặc giao việc dễ sai cho chương trình (ngày tháng, xếp lịch, luật tra web). Model embedding lớn hơn và các cách xếp lại chưa thắng lần nào.

</details>

## Các điều kiện đang dùng

| Điều kiện | Giá trị | Áp cho |
|---|---|---|
| Câu ngoài kho được trả lời bằng kho | 0 | mọi thay đổi |
| Bộ an toàn: câu nói ngược cảnh báo; câu ngoài kho bị trả lời | 0 và 0 | mọi thay đổi ở phần hỏi đáp và trợ lý |
| Bộ an toàn: câu thiếu cảnh báo mới; câu sai điều kiện mới | ngưỡng ghi trước cho từng lượt (lượt 18/11: 0 và 0) | như trên |
| Câu mất đoạn đúng ở bước tìm | 0 | thay đổi ở cắt đoạn, embedding, tìm, xếp lại |
| Điểm trung bình tụt | không quá 0,1 | mọi thay đổi |
| Số câu tệ đi | không quá mức nhiễu cộng 3 | mọi thay đổi |
| Mức tăng | vượt mức nhiễu; khoảng tin cậy không chứa 0; cùng chiều trên nhóm để kiểm lại | thay đổi nhằm tăng điểm |
| Mức nhanh hơn, rẻ hơn | một mức ghi trước cho từng lần thử | thay đổi nhằm tốc độ hay tiền |
| Số lượt lặp khi dùng một bộ đo nhỏ | ít nhất ba lượt mỗi bên | các bộ đo nhỏ của phần trợ lý (bài 32) |
| Mốc | bản đang chạy, cùng người chấm; đo lại cùng buổi ở khâu có model | mọi thí nghiệm |

## Quyết định nhỏ hơn

**Vì sao không thử trên người dùng thật, đưa hai bản cho hai nhóm người?** Chưa làm được: hệ thống chưa đưa lên mạng, chưa có người dùng thật. Cái giá: mọi kết luận "tốt hơn" là tốt hơn trên bộ câu của nhóm. Lưu ý: câu dùng ở các phép đếm (ví dụ 310 câu) là câu đã gõ vào hệ thống trên máy phát triển, do chủ dự án và nhóm gõ khi dùng thử, không phải câu của người dùng thật.

**Vì sao không để máy tự dò mọi tổ hợp tham số?** Mỗi lần thử do người và agent chọn, có lý do. Đã thử cho máy tự dò ngày 19/11: 15 cấu hình của bước tìm (bản đang chạy cộng 14 cách chỉnh), 0 đồng, không tìm ra cách nào hơn bản đang chạy vượt mức nhiễu (bản đang chạy 22 trên 38 câu khó đủ đoạn đúng). Đọc đúng là "không thấy khác", không phải "bản đang chạy là tốt nhất": 38 câu là quá ít để phân biệt. Cái giá: lần dò chỉ thử các nút chỉnh lúc hỏi; chưa dò cách cắt đoạn, model vector hay bước xếp lại.

**Vì sao mốc phải đo cùng buổi ở khâu có model, còn khâu chương trình tính thì dùng lại mốc cũ được?** Luật của bộ đo: khâu có model thì cùng một model mỗi lần trả lời hơi khác, nên bản đang chạy phải được chạy lại ngay trong buổi thử, cùng lúc với bản mới; so với số cũ của hôm khác thì không biết chênh do thay đổi hay do model tự lệch. Khâu chương trình tính ra y hệt mỗi lần, không cần đo lại. Cái giá: mỗi lần thử ở khâu có model tốn gấp đôi lượt chạy.

**Vì sao lần đo đầu khi chọn một nhà cung cấp phải chạy qua đường của người dùng thật?** Luật thêm sau ca dịch vụ tìm web (bảng "Nếu… thì sao", dòng 4): thắng khi đo riêng bước tra, hoà khi đi qua máy chủ. Nay chọn nhà cung cấp hay tham số thì lượt đầu đo qua máy chủ, không chỉ một bước tách riêng.

Ý 3 của mục "Nhìn cả bảng", nói rõ hơn: "chứng minh chuỗi chữ gửi model không đổi" nghĩa là chứng minh rằng với các câu của bộ an toàn, thứ gửi cho model y hệt từng chữ như trước khi đổi, nên kết quả an toàn cũ vẫn dùng được.

Một dòng bảng còn lại: thay đổi rất nhỏ, rõ nguyên nhân thì sửa và chạy bộ test, không cần cả sáu bước (đã có).

## Giới hạn đã biết

- **Bộ câu nhỏ ở nhiều lần thử.** Nhiều kết luận là "chưa rõ" vì chỉ có vài câu có thể đổi kết quả.
- **Phần lớn lần thử ở bước tìm và xếp lại** làm cuối tháng 10, trên kho của thời điểm đó và thời còn đưa 5 đoạn. Bảng tổng ghi rõ dòng nào có thể khác đi ở cấu hình hiện nay.
- **Gần như mọi lần thử đo với gpt-6-luna.** Từ tối 21/11 các phép đo mới chạy và chấm bằng Claude Sonnet 5.5; số của hai giai đoạn không so thẳng với nhau.
- **Có lần giữ dù một ngưỡng không đạt, và đều ghi lý do.** Rõ nhất: một thay đổi được giữ dù một điều kiện bị vỡ theo chữ, vì chạy lại bản chưa đổi cũng ra đúng những câu đó, tức chỗ vỡ không do thay đổi (bài 21, dòng 3). Chức năng hỏi bằng ảnh cũng không đạt một ngưỡng, và được giữ ở dạng khác: có bước xác nhận tên mà hệ thống đoán — nay một tên thì hỏi luôn kèm dòng "có thể sai", hai ba tên thì bấm chọn (bài 26).
- **Liều lượng đo từng bị chủ dự án nhận xét là quá tay.** Từ 21/11 luật là: thay đổi rủi ro cao thì thử nhiều, thay đổi nhỏ thì thử ít, bỏ các lượt đo lặp lại không đổi quyết định nào; chất lượng không được tụt vì bớt đo.

## Chi tiết để tra

- Bảng tổng có 12 dòng cho đường hỏi đáp và 33 dòng cho phần trợ lý, lên kế hoạch; ngoài ra còn khoảng 55 lần thử nhỏ hơn (đổi hằng số, sửa kho, đổi cách đo) nằm trong hồ sơ làm việc.
- Lần thắng về điểm câu trả lời duy nhất của đợt rà lại mọi lựa chọn cuối tháng 10 là "10 đoạn thay vì 5" (bài 13); cùng đợt còn giữ việc chuẩn hoá chữ có dấu, là sửa một lỗi chứ không tăng điểm trên câu thường (bài 10).
- Đếm lại bảng tổng: 25 dòng bỏ, 15 dòng giữ, 1 dòng vừa giữ vừa bỏ, 4 dòng không thuộc loại giữ hay bỏ.
- Ba ý tưởng bị dừng ở bước đếm ngày 12/11, và thêm một lần ngày 14/11 (đổi cách tìm web cho câu kho không có: cách tốt nhất chỉ cho 6 trên 16 lượt có ích).
- Dịch vụ tìm web khác: đo riêng bước tra thì 25 so với 17 (cần 22); qua máy chủ thật thì 14 so với 13 (cần 16); bài 25.
- Luật chọn khu ở theo buổi tối: lần đầu 8 trên 10 (cần 9), lần hai 10 trên 10; bài 30.

**Bài sau (bài 21):** hết chặng đo. Chặng 5 quay lại hệ thống: từ đường hỏi đáp "tìm một lần, viết một lần" thành một trợ lý có công cụ.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Sáu bước, đếm cỡ mẫu trước, mốc đo cùng buổi, so theo cặp và theo tầng, bốn chữ kết luận, giữ hồ sơ cả phương án bị bỏ: `skills/run-experiment/SKILL.md` mục 1, 3, 4, 5 [quy trình của dự án].
- Các điều kiện (0 câu ngoài kho; bộ an toàn; 0 câu mất đoạn đúng; tụt không quá 0,1; số câu tệ đi không quá mức nhiễu + 3; ba lượt lặp cho bộ đo nhỏ): `bai_hoc/11_CHAM_CAU_TRA_LOI.md`, `bai_hoc/10_CHAM_BUOC_TIM.md`, `session_prompt/HIEN_TRANG.md` mục 2.
- Bảy điều "nhìn cả bảng", 45 dòng (12 + 33), khoảng 55 lần thử nhỏ, "hơn một nửa là bỏ", ngoại lệ duy nhất (hàng số 35): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` mục "Đọc bảng thế nào", hai bảng, và mục "Nhìn cả bảng thấy gì" [đã chạy; bài đã qua kiểm độc lập].
- Ví dụ model viết chọn đoạn (5 câu, ngưỡng 4), câu dặn rộng (7, ngưỡng 5): cùng bài, hàng số 9 và 16.
- Đếm 310 câu, sót 4 / 60: `report_agent/2026-11-21/c_cong_cong_cu.md`. Ba ý tưởng dừng ở bước đếm 12/11, lần 14/11 (6 / 16): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` ý 6.
- Dịch vụ tìm web (25 / 17 / 22; 14 / 13 / 16), khu ở theo buổi tối (8 / 10; 10 / 10): cùng bài, hàng số 36, 40, 41.
- Máy tự dò cấu hình bước tìm (19/11, không dùng): `bai_hoc/VIEC_MOI_XONG.md` mục 10.
- Nhận xét của chủ dự án về liều lượng đo và luật mới: `session_prompt/HIEN_TRANG.md` mục 4, gạch 22:45 21/11/2026.
- Mốc cùng buổi chỉ bắt buộc ở khâu có model; mức phải đạt riêng cho thay đổi nhằm tốc độ (hàng số 38 của bảng tổng: 0,87 so với 1,5 giây); xác nhận trên nhóm kiểm lại là "cùng chiều, không làm hỏng"; hàng số 25 giữ ở dạng chờ xác nhận; đếm 25 / 15 / 1 / 4: `skills/run-experiment/SKILL.md`, `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md`, `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` (theo biên bản kiểm `data/hoc_cung_D/kiem/bai_17_20.md`). Số tốt hơn của Claude Sonnet 5.5 ở thước nhỏ: `bai_hoc/VIEC_MOI_XONG.md` mục 23.
- Mục "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn" (sửa theo biên bản `data/hoc_cung_D/kiem/muc_moi_05_06_17_20.md` phần bài 20 [riêng tư]): bản chọn đoạn 5 câu tụt, ngưỡng 4, chậm và tốn 3,8 lần: bảng tổng hàng số 9; ba thay đổi gộp (10 đoạn, NFC, bộ kiểm trích dẫn v2): `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` (giới hạn của nhóm B1 / B3); hai ngoại lệ: bảng tổng hàng số 35 (3 câu, chạy lại bản cờ tắt, người kiểm độc lập đồng ý) và hàng số 25 (2 / 5 ảnh, ngưỡng ≤ 1, giữ dạng chờ xác nhận); lời chủ dự án về đo / test (22:45 và 22:48 21/11): `session_prompt/HIEN_TRANG.md` mục 4; 310 câu là "câu gõ khác nhau trong sổ vết": `report_agent/2026-11-21/c_cong_cong_cu.md`; máy tự dò (15 cấu hình, 0 hơn, 22 / 38, 0 đồng, chỉ nút chỉnh lúc hỏi): `bai_hoc/VIEC_MOI_XONG.md` mục 10 (19/11) [máy kiểm, chưa ai chạy lại]; mốc cùng buổi, khâu tất định không cần A/A, lượt đầu qua server khi chọn nhà cung cấp: `skills/run-experiment/SKILL.md` (mục 0 và mục mốc); "chưa thấy lần nào bị loại vì ngược chiều trên nhóm kiểm": người kiểm đọc lướt cột kết quả bảng tổng, không đếm hết.

- Hai câu về hỏi bằng ảnh sửa theo bài 26 (cách lai: một tên thì hỏi luôn kèm "có thể sai"; 2–3 tên bấm chọn), bài 26 đọc từ chương trình giao diện [chép qua bài 26; người viết không mở lại code giao diện]. Bộ thay đổi mở 14:47 22/11/2026 không chạm bài này.

</details>
