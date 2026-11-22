# Bài 11 — Tìm theo chữ trùng: từ khoá BM25

*Cập nhật 14:17, ngày 22/11/2026 · cơ chế đọc từ chương trình đang chạy, đối chiếu lại lúc 13:49; số của ví dụ lấy từ lần chạy lại riêng bước tìm sáng 22/11 (không gọi model viết); số của các phép so lấy từ báo cáo đo ngày 30/08 và 25/10; người viết không chạy lại phép đo nào.*

**Bài trước đã biết:** mỗi đoạn có một vector; câu hỏi cũng thành một vector; hệ thống lấy 30 đoạn có vector gần câu hỏi nhất, gọi là 30 ứng viên.
**Bài này thêm:** cách chấm thứ hai, theo chữ trùng, áp lên chính 30 ứng viên đó; vì sao nó được tính ngay lúc hỏi; và file thống kê của nó lệch kho thì sao.

## Ý chính

- **BM25** là một công thức chấm điểm một đoạn theo các chữ nó có chung với câu hỏi. Chữ càng hiếm trong kho thì trùng càng được nhiều điểm.
- Nó bù cho chỗ yếu của tìm theo nghĩa ở những chữ cụ thể như tên riêng. Vector mang nghĩa chung của cả đoạn; BM25 nhìn đúng từng chữ.
- Ở hue_rag, BM25 **không tìm trên cả kho**. Nó chỉ **chấm lại 30 ứng viên** mà bước tìm theo nghĩa đã lấy ra, để có một bảng xếp hạng thứ hai. Điểm được chương trình tính ngay lúc hỏi, từ chữ của 30 ứng viên và một **file thống kê** lập lúc chuẩn bị kho. Đoạn không lọt 30 ứng viên thì BM25 không cứu được.
- Ở ví dụ chính, có hai đoạn đứng hạng 18 và 19 theo nghĩa nhưng hạng 4 và 3 theo từ khoá. Nhờ bảng thứ hai, chúng lọt vào 10 đoạn đưa cho model viết.
- "Từ" ở đây là âm tiết: câu được cắt ở mọi chỗ không phải chữ hay số. Đã thử hai cách tách từ "đúng tiếng Việt" hơn; cả hai kém hơn.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| tìm theo từ khoá | **keyword search**, **lexical search**, **sparse retrieval** | chấm đoạn theo chữ trùng với câu hỏi |
| BM25 | **BM25** (Best Matching 25) | công thức chấm điểm theo chữ trùng dùng phổ biến nhất |
| tách từ | **tokenize** | cắt một câu thành các "từ" để đếm; ở đây mỗi từ là một âm tiết |
| từ điển của kho | **vocabulary** | danh sách mọi từ khác nhau có trong kho; hiện 5.954 từ |
| độ hiếm | **IDF** (inverse document frequency) | số cho biết một từ có mặt ở ít hay nhiều đoạn; từ có ở ít đoạn thì độ hiếm cao |
| file thống kê từ khoá | **sparse state** | file ghi từ điển, độ hiếm của từng từ, và độ dài trung bình của một đoạn |

## Tìm theo nghĩa yếu ở những chữ cụ thể

Vector của một đoạn mang nghĩa chung của cả đoạn. Hai đoạn nói về hai loại vé khác nhau có thể có vector rất gần nhau, vì cả hai đều "nói về giá vé". Ở bài 10 đã thấy: trong ví dụ chính, hạng 1 và hạng 30 chỉ chênh nhau 0,02 về độ gần.

Khi câu hỏi nêu đích danh một cái tên, cần một cách chấm nhìn vào đúng chữ đó. BM25 là cách đó. (Với con số thì BM25 ở đây chưa giúp được nhiều; xem mục "Giới hạn đã biết".)

## BM25 cho điểm theo chữ trùng, chữ hiếm được nhiều điểm hơn

BM25 làm ba việc với mỗi đoạn:

1. **Đếm chữ trùng.** Mỗi từ của câu hỏi có mặt trong đoạn thì đoạn được cộng điểm.
2. **Nhân với độ hiếm của từ.** Từ có mặt ở hầu hết các đoạn (như "và") gần như không đem lại điểm; từ có ở khoảng nửa kho (như "huế") đem lại ít điểm. Từ chỉ có ở vài đoạn (như tên một quán) đem lại nhiều điểm.
3. **Trừ bớt cho đoạn dài.** Đoạn dài dễ trùng nhiều chữ chỉ vì nó nhiều chữ, nên bị trừ bớt theo độ dài so với độ dài trung bình của kho.

Để làm được việc 2 và 3, lúc chuẩn bị kho chương trình lập sẵn một **file thống kê từ khoá**: danh sách 5.954 từ khác nhau của kho, độ hiếm của từng từ, và độ dài trung bình của một đoạn (khoảng 67 từ).

## "Từ" ở đây là âm tiết

Cách tách từ rất đơn giản: đổi hết sang chữ thường, rồi cắt ở mọi chỗ không phải chữ hay số. Tiếng Việt viết cách giữa các âm tiết, nên mỗi "từ" thực tế là một âm tiết. Câu ví dụ chính, *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"*, thành 10 từ: giá, vé, tham, quan, đại, nội, huế, là, bao, nhiêu. Cả 10 đều có trong từ điển của kho.

Cách tách này có vẻ thô: "tham quan" bị tách đôi, "Đại Nội" bị tách đôi. Nó được giữ vì đã đo hai cách tách "đúng tiếng Việt" hơn và cả hai kém hơn (mục "Đã so").

## Ở hue_rag, BM25 chỉ chấm lại 30 ứng viên của bước tìm theo nghĩa

BM25 ở đây không tự đi tìm trên 9.458 đoạn. Thứ tự là:

1. Tìm theo nghĩa lấy ra 30 ứng viên (bài 10).
2. BM25 chấm điểm **đúng 30 đoạn đó**, và xếp chúng thành một bảng thứ hai.
3. Hai bảng xếp hạng (theo nghĩa và theo từ khoá) được trộn lại để giữ 10 đoạn (bài 13).

Số thật của ví dụ chính cho thấy bảng thứ hai có ích thế nào:

| Đoạn (trong 10 đoạn cuối cùng) | Hạng theo nghĩa | Hạng theo từ khoá | Hạng sau khi trộn |
|---|---|---|---|
| đoạn về các dịch vụ thu phí riêng trong Đại Nội, có nhắc giá vé vào cổng 200.000 đồng (nguồn số 1) | 1 | 1 | 1 |
| dòng bảng giá vé gộp 3 điểm, 420.000 đồng (nguồn số 5) | 19 | 3 | 5 |
| dòng bảng giá vé gộp 4 điểm, 530.000 đồng (nguồn số 6) | 18 | 4 | 6 |
| một đoạn tư vấn chọn vé (nguồn số 7) | 2 | 22 | 7 |

Hai dòng bảng giá đứng hạng 19 và 18 theo nghĩa. Nếu chỉ lấy 10 đoạn đầu theo nghĩa, chúng bị bỏ. Chúng đứng hạng 3 và 4 theo từ khoá vì trùng nhiều chữ với câu hỏi ("giá", "vé", "tham quan", "Đại Nội", "Huế"), và nhờ đó lọt vào 10 đoạn. Câu trả lời thật đã dùng cả hai đoạn này để nêu giá vé gộp.

Chiều ngược lại cũng có: đoạn tư vấn chọn vé đứng hạng 2 theo nghĩa nhưng hạng 22 theo từ khoá, và sau khi trộn tụt xuống hạng 7.

## Quyết định và lý do

### 1. Vì sao có thêm bảng xếp hạng theo từ khoá, không chỉ tìm theo nghĩa?

- **Đã chọn:** hai bảng xếp hạng (theo nghĩa, theo từ khoá) trộn lại thành 10 đoạn (bài 13).
- **Vì sao:** quyết định đã ghi: ngày 11/09 chủ dự án chốt cách "tìm theo nghĩa rồi chấm lại theo từ khoá" làm cách mốc để so; các lần so cuối tháng 10 không cách nào hơn nên giữ (bài 13). Vì sao cần phần từ khoá ngay từ đầu: chưa thấy ghi lý do. Điều thấy được: ở ví dụ chính, hai dòng bảng giá mà câu trả lời dùng chỉ lọt vào 10 đoạn nhờ bảng thứ hai (hạng 19 và 18 theo nghĩa, hạng 3 và 4 theo từ khoá).
- **Cách khác:** chỉ tìm theo nghĩa: chưa so trên toàn kho. 10 cách trộn khác: đã đo, không cách nào thắng rõ (bài 13).
- **Cái giá:** thêm một file thống kê phải luôn khớp kho; chiều ngược lại cũng có: đoạn tư vấn chọn vé hạng 2 theo nghĩa tụt xuống hạng 7.

### 2. Vì sao BM25 chỉ chấm lại 30 ứng viên, không tự tìm trên cả kho rồi trộn?

- **Đã chọn:** chấm lại đúng 30 đoạn mà bước tìm theo nghĩa đã lấy ra.
- **Vì sao:** đã đo cuối tháng 10: để từ khoá tự tìm trên cả kho rồi trộn thì điểm thứ hạng gần như không đổi (0,726 so với 0,721) mà mất đoạn đúng ở 1 tới 2 câu (bài 13).
- **Cách khác:** tìm độc lập trên cả kho: đã đo, bỏ.
- **Cái giá:** một đoạn trùng chữ y hệt câu hỏi mà không lọt 30 ứng viên theo nghĩa thì không bao giờ được chấm (lượt "cởi giày").

### 3. Vì sao điểm từ khoá do chương trình tính ngay lúc hỏi, không đọc phần từ khoá đã cất sẵn trong Qdrant?

Qdrant cất sẵn cho mỗi đoạn một **vector từ khoá** (dãy số cho việc tìm theo từ, tính từ file thống kê lúc chuẩn bị). Phần đó dùng để tìm trên cả kho.

- **Đã chọn:** lúc hỏi, chương trình tự tính điểm cho 30 ứng viên từ chữ của chúng và file thống kê; file này được nạp một lần lúc bật máy chủ.
- **Vì sao:** hệ quả của quyết định 2: chỉ cách tìm trên cả kho mới cần phần cất sẵn, và cách đó đã bị bỏ. Chấm 30 đoạn mất khoảng 3,5 mili giây ở ví dụ chính, không phải hỏi thêm Qdrant.
- **Cách khác:** đọc phần cất sẵn: chỉ cách tìm thứ hai của hệ thống (đang không dùng) làm vậy.
- **Cái giá:** phần cất sẵn vẫn phải ghi lại mỗi lần sửa kho (1,8 giây cho cả kho) để chỉ mục giống một bản dựng lại và để cách tìm thứ hai không âm thầm sai. File thống kê phải khớp kho (mục "Nếu… thì sao").

### 4. Vì sao "từ" là âm tiết, không tách theo từ ghép tiếng Việt?

- **Đã chọn:** chữ thường, cắt ở mọi chỗ không phải chữ hay số.
- **Vì sao:** đã đo (mục "Đã so"): ghép cặp âm tiết và thư viện tách từ tiếng Việt đều mất đoạn đúng ở 1 câu trên 32 câu; không cách nào tốt lên rõ.
- **Cách khác:** ba cách tách khác: đã đo, bỏ.
- **Cái giá:** "Đại Nội" bị tách đôi; con số "40.000" thành "40" và "000".

### 5. Vì sao hai hằng số là k1 = 1,5 và b = 0,75?

- **Đã chọn:** k1 = 1,5 (mức bão hoà khi một từ lặp nhiều lần), b = 0,75 (mức trừ bớt cho đoạn dài).
- **Vì sao:** đã đo các giá trị khác, không giá trị nào hơn.
- **Cách khác:** k1 1,2 và 1,8 (bản thử nhóm món ăn): giữ 1,5. b 0,5: chưa rõ hơn; b 1,0: mất đoạn đúng ở 1 câu.
- **Cái giá:** k1 mới đo trên nhóm món ăn, chưa đo lại trên toàn kho.

## Nếu… thì sao

Đọc từ chương trình; người viết chưa thử lại các dòng này.

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa / ai làm gì |
|---|---|---|---|
| file thống kê từ khoá thiếu, hoặc lệch bản ghi chỉ mục | lúc bật, máy chủ so dấu vân tay của file với bản ghi; lệch thì phần tìm kho không dùng | mọi câu hỏi: "Dữ liệu tra cứu cần được lập chỉ mục lại." | người vận hành chạy lệnh cập nhật chỉ mục (nó ghi lại file thống kê), rồi khởi động lại (bài 12) |
| chạy lệnh cập nhật chỉ mục trong lúc máy chủ đang chạy | lệnh dừng ngay từ đầu, chưa đọc hay ghi gì: máy chủ đang chạy sẽ trả lời trên chỉ mục ghi dở cùng file thống kê cũ | không đổi gì | tắt máy chủ, chạy lệnh, bật lại (bài 12) |
| câu hỏi có từ không nằm trong từ điển của kho | từ đó được 0 điểm; không từ nào có trong từ điển thì chỉ còn bảng theo nghĩa | câu trả lời dựa vào tìm theo nghĩa | đã có |
| đoạn đúng không lọt 30 ứng viên theo nghĩa | BM25 không thấy đoạn đó | có thể nhận câu từ chối dù kho có | đã có; gốc ở bước tìm theo nghĩa (bài 13) |
| kho lớn gấp mười | mỗi câu vẫn chỉ chấm 30 đoạn; file thống kê lập lại cho cả kho mỗi lần sửa | — | lập luận, chưa đo: lúc hỏi gần như không chậm thêm |

## Dễ nhầm

- **"BM25 tìm trên cả kho."** Ở hệ thống này thì không. Nó chỉ chấm lại 30 ứng viên của bước tìm theo nghĩa.
- **"Có embedding rồi thì không cần từ khoá."** Không. Ở ví dụ chính, hai đoạn được dùng trong câu trả lời chỉ lọt vào 10 đoạn nhờ bảng xếp hạng theo từ khoá.
- **"Phải tách từ đúng ngữ pháp tiếng Việt thì mới tìm tốt."** Đã đo: hai cách tách từ ghép đều làm mất đoạn đúng ở 1 câu trên 32 câu; tách theo âm tiết được giữ.

## Câu hỏi tự kiểm

<details>
<summary>1. BM25 cho điểm một đoạn dựa trên ba điều nào?</summary>

Số chữ trùng với câu hỏi; độ hiếm của từng chữ trong kho (chữ hiếm được nhiều điểm); và độ dài của đoạn so với độ dài trung bình (đoạn dài bị trừ bớt).

</details>

<details>
<summary>2. Ở ví dụ chính, bảng xếp hạng theo từ khoá giúp được gì?</summary>

Hai dòng bảng giá vé gộp đứng hạng 19 và 18 theo nghĩa, nhưng hạng 3 và 4 theo từ khoá; sau khi trộn chúng lọt vào 10 đoạn và được câu trả lời dùng.

</details>

<details>
<summary>3. Vì sao điểm từ khoá được tính lúc hỏi, và việc đó cần thứ gì luôn đúng?</summary>

BM25 chỉ chấm lại 30 ứng viên, nên chương trình tính thẳng từ chữ của chúng, khoảng 3,5 mili giây. Việc đó cần file thống kê (từ điển, độ hiếm, độ dài trung bình) khớp với kho; lệch thì mọi câu hỏi nhận lời báo cần lập chỉ mục lại.

</details>

<details>
<summary>4. Một đoạn trùng chữ y hệt câu hỏi mà vẫn không được lấy ra. Vì sao có thể như vậy?</summary>

BM25 chỉ chấm 30 ứng viên của bước tìm theo nghĩa. Đoạn đó không lọt 30 ứng viên thì không bao giờ được chấm.

</details>

## Cấu hình đang chạy

*Chép từ hệ thống đang chạy sáng 22/11/2026. Cấu hình đổi thì mục này phải chép lại.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Cách tách từ | chữ thường, cắt ở mọi ký tự không phải chữ hay số (thực tế: theo âm tiết) | đơn giản, không cần thư viện tách từ | đã thử ghép cặp âm tiết, thư viện tách từ tiếng Việt, giữ nguyên cụm mã số (mục "Đã so") |
| Hằng số k1 | 1,5 | mức "bão hoà" khi một từ lặp nhiều lần trong đoạn: lặp thêm thì điểm tăng chậm dần | đã thử 1,2 và 1,8 trên bản thử nhóm món ăn: giữ 1,5 |
| Hằng số b | 0,75 | mức trừ bớt cho đoạn dài (0 = không trừ, 1 = trừ hết mức) | đã thử 0,5 và 1,0: 0,5 chưa rõ hơn, 1,0 mất đoạn đúng ở 1 câu |
| Số từ trong từ điển | 5.954 | — | — |
| Độ dài trung bình một đoạn | 66,63 từ | dùng trong phép trừ bớt cho đoạn dài | — |
| Số đoạn được chấm mỗi câu hỏi | 30 (các ứng viên của bước tìm theo nghĩa) | — | đã thử cho từ khoá tự tìm trên cả kho rồi trộn: kém hơn (bài 13) |
| Nơi tính điểm lúc trả lời | chương trình tự tính từ chữ của 30 ứng viên và file thống kê | không phải hỏi thêm cơ sở dữ liệu | — |
| Từ của câu hỏi không có trong từ điển | 0 điểm | — | — |
| Tên cách tìm trong file cấu hình | `retrieval_treatment: dense_bm25_rrf` | "nghĩa lấy ứng viên, BM25 chấm lại, trộn" | bài 13 |

Công thức điểm của một đoạn cho một câu hỏi: cộng trên mọi từ chung giữa hai bên của `độ hiếm × tf × (k1 + 1) / (tf + k1 × (1 − b + b × độ dài đoạn / độ dài trung bình))`, với `tf` là số lần từ đó có mặt trong đoạn. Độ hiếm của một từ: `ln((N − n + 0,5) / (n + 0,5) + 1)`, với `N` là số đoạn của kho và `n` là số đoạn có từ đó.

## Đã so

### Tách từ thế nào

**Vấn đề.** Tách theo âm tiết làm rời các tên ghép: "Đại Nội" thành "đại" và "nội". Giả thuyết: tách đúng từ ghép tiếng Việt thì tên riêng được nhận tốt hơn.

**So gì, trên bộ nào.** Ba cách tách khác, trên 32 câu đã biết đáp án nằm ở đoạn nào (kho cuối tháng 10, thời còn đưa 5 đoạn). Thước: số câu có đủ đoạn đúng trong 5 đoạn. Luật ghi trước: không câu nào được mất đoạn đúng, và phải tốt lên thật.

| Cách tách | Số từ trong từ điển | Câu tốt lên / như cũ / mất đoạn đúng (trên 32) | Kết luận |
|---|---|---|---|
| theo âm tiết (đang dùng) | 5.660 | mốc | **giữ** |
| ghép từng cặp âm tiết liền nhau | 105.999 | 1 / 30 / 1 | kém hơn: mất 1 câu |
| thư viện tách từ tiếng Việt | 14.211 | 0 / 31 / 1 | kém hơn: mất 1 câu |
| giữ nguyên cụm mã số (không cắt ở dấu chấm trong số) | 6.719 | 0 / 32 / 0 | không khác |

**Đọc bảng này thế nào.**
- Không cách nào làm tốt lên rõ; hai cách "đúng tiếng Việt" hơn đều làm mất đoạn đúng ở 1 câu.
- Giữ nguyên cụm số không đổi gì trên 32 câu này.
- Tách theo âm tiết là cách đơn giản nhất và không thua cách nào.

**Đã chọn: giữ tách theo âm tiết.**

**Giới hạn của phép đo.** 32 câu, kho cũ, một lần chạy; chênh lệch 1 câu chưa đủ để phép thử thống kê khẳng định. Cách nói đúng mức: "chưa cách nào tốt hơn", không phải "âm tiết là tốt nhất".

### BM25 hay một công thức khác

Trên bản thử chỉ có nhóm món ăn (45 câu), BM25 đứng một mình tìm tốt hơn công thức TF-IDF đứng một mình: 0,6478 so với 0,6150 theo điểm nDCG@5 (điểm từ 0 tới 1 cho việc đoạn đúng đứng cao tới đâu trong 5 đoạn đầu). TF-IDF không được dùng ở các giai đoạn sau; hồ sơ không ghi lý do, lý do ở đây là suy ra từ con số này. Phép so này chưa được làm lại trên toàn kho.

## Quyết định nhỏ hơn

**Vì sao BM25 mà không TF-IDF?** Chưa thấy ghi lý do; hồ sơ không ghi ai chốt. Điều thấy được: số của bản thử nhóm món ăn ở cuối mục "Đã so".

**Vì sao không dùng công cụ tìm kiếm toàn văn có sẵn (như Elasticsearch)?** Chưa thử. Lập luận, không phải số đo: với việc chỉ chấm lại 30 ứng viên, phép tính mất vài mili giây ngay trong chương trình, không cần thêm một dịch vụ phải vận hành.

**Vì sao không giữ nguyên cụm số ("40.000" là một từ)?** Đã thử: trên 32 câu không đổi gì, nên giữ cách tách đơn giản.

## Giới hạn đã biết

- **Đoạn không lọt 30 ứng viên theo nghĩa thì không được chấm.** Một đoạn trùng chữ y hệt câu hỏi nhưng bị bước tìm theo nghĩa bỏ sót sẽ không bao giờ tới được BM25. Ví dụ "kho có mà tìm không ra" của cả bộ (câu hỏi cởi giày khi vào chùa) thuộc loại này: đoạn có câu trả lời không nằm trong các đoạn được lấy ra ở cả ba lần tìm.
- **Con số bị tách đôi.** Cách tách cắt ở dấu chấm, nên "40.000" thành "40" và "000"; một con số giá không được nhận như một từ riêng. Đã thử giữ nguyên cụm số: trên 32 câu không đổi gì.
- **Từ không có trong từ điển** được 0 điểm, ví dụ tên một nơi chưa có bài nào trong kho nhắc tới.
- **Câu gõ không dấu** vẫn trùng nhiều âm tiết với kho, nhưng là trùng nhầm từ khác ("gia" thay cho "giá") và mất các từ hiếm có dấu (bài 10).

## Chi tiết để tra

- Ở ví dụ chính, bước chấm BM25 cho 30 ứng viên mất khoảng 3,5 mili giây; cả bước tìm 42 mili giây.
- Số thứ hạng trong bảng ví dụ lấy từ lần chạy lại riêng bước tìm sáng 22/11 (không gọi model viết); 10 đoạn giữ lại trùng với 10 đoạn của lượt hỏi thật ngày 21/11.
- Từ điển 5.660 từ trong phép so là của kho cuối tháng 10; kho hiện nay 5.954 từ.
- Khi kho đổi dù chỉ một bài, độ hiếm của các từ và độ dài trung bình đổi theo, nên file thống kê được lập lại cho cả kho. Việc này không cần model và mất khoảng 20 giây cùng với việc cắt đoạn (bài 12).
- Phép so tách từ trên bản thử nhóm món ăn (30/08): tách theo âm tiết và tách bằng một thư viện tách từ cho kết quả gần như nhau; cách âm tiết được chọn vì đơn giản.
- Chưa có phép so "có từ khoá" với "chỉ theo nghĩa" trên toàn kho. Trên bản thử nhóm món ăn (30/08), hồ sơ ghi cách trộn tốt nhất có một nhóm câu tụt quá mức cho phép, nên lúc đó chưa chọn cách trộn nào. Ngày 11/09, khi thiết kế cho toàn kho, chủ dự án chốt cách đang chạy làm cách mốc; cách hai bên tìm độc lập là phương án để so với nó.

**Bài sau (bài 12):** vector, chữ và thông tin gắn kèm của 9.458 đoạn được cất ở đâu, cập nhật thế nào khi kho đổi, và vì sao hệ thống không chịu chạy khi kho và chỉ mục lệch nhau.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Cách tách từ (`\w+` trên chữ thường), k1 1,5, b 0,75, công thức độ hiếm và công thức điểm: `backend/scoring/bm25.py`; `backend/embedding/sparse.py`, hàm `encode_sparse_document`, `encode_sparse_query` [code, đọc 22/11/2026].
- BM25 chấm lại đúng 30 ứng viên của bước tìm theo nghĩa, tính từ chữ của ứng viên và file thống kê: `backend/retrieval/full_corpus.py`, hàm `search`, nhánh `dense_bm25_rrf` [code].
- 5.954 từ, độ dài trung bình 66,63: `data/full_corpus_builds/full_corpus_sparse_state.json`, đọc 10:02 22/11/2026 [đã chạy].
- Bảng thứ hạng của ví dụ chính (1 / 1 / 1; 19 / 3 / 5; 18 / 4 / 6; 2 / 22 / 7), 10 từ của câu hỏi đều có trong từ điển, 3,45 và 42 mili giây: `data/hoc_cung_D/vet_tim_ba_vi_du.json` (chạy bằng `data/hoc_cung_D/tools/vet_tim.py`) [người viết chạy 22/11/2026, 0 đồng]; khớp 10 đoạn của `data/hoc_cung_D/vi_du_di_suot_vet.json`. Hai dòng bảng giá được trích trong câu trả lời (nguồn [5], [6]): cùng file, trường `tra_loi`.
- Phép so tách từ (5.660 / 105.999 / 14.211 / 6.719 từ; 1 / 30 / 1; 0 / 31 / 1; 0 / 32 / 0), k1 và b, BM25 so TF-IDF (0,6478 so 0,6150): `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ N2-11, N2-12, N2-14 [đã chạy; nhãn của báo cáo: "kho, cấu hình cũ", "một lần chạy"].
- Từ khoá tự tìm trên cả kho kém hơn 1–2 câu: `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 5 [đã chạy].
- Cách tìm đang chạy không đọc bản từ khoá cất trong cơ sở dữ liệu; lập lại thống kê cả kho khi kho đổi: `report_agent/2026-11-22/c_cap_nhat_rieng.md` mục 2 [phiên khác đọc code và đo].
- Ví dụ cởi giày: `data/hoc_cung_D/kiem/bai_02_10.md` dòng 26.
- Mục "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn", "Câu hỏi tự kiểm" (thêm 13:49 22/11/2026 theo khuôn mới; gom từ "Đã so", bảng cấu hình, mục "Vì sao không làm cách khác" cũ). Cơ chế "tính lúc hỏi từ 30 ứng viên" đối chiếu lại 13:49: `backend/retrieval/full_corpus.py`, `search` nhánh `dense_bm25_rrf` (vòng `for pid in dense_ranked_ids`, `encode_sparse_document` trên `search_text` của payload) [code]. File thống kê nạp lúc bật, so `state_sha256` và `corpus_identity` với bản ghi, lệch ⇒ `ComponentNotReadyError` ⇒ lời báo lập chỉ mục lại: `build_full_corpus_retrieval_service` bước 2 và `backend/api/app.py` [code, chưa thử]. Lệnh cập nhật dừng khi máy chủ đang chạy: `backend/ingestion/cap_nhat_rieng.py` (`ServerDangChay`) [code]. 1,8 giây ghi lại phần cất sẵn; khởi động lại để nạp thống kê mới và quên câu trả lời đã nhớ: `bai_hoc/VIEC_MOI_XONG.md` mục 32 [đã chạy]. Không từ nào trong từ điển ⇒ chỉ còn bảng theo nghĩa: cùng hàm (`branches` chỉ thêm bảng BM25 khi có đoạn được điểm) [code]. Chủ dự án chốt 11/09 cách "nghĩa lấy ứng viên rồi từ khoá chấm lại" làm cách mốc: `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md` mục Decision Queue #1 ("User xác nhận … 2026-09-11") [quyết định đã ghi]. Lý do cần phần từ khoá ngay từ đầu: người viết dò thẻ T3-02, N2-14 của `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` và kế hoạch Phase 5 `docs/superpowers/plans/2026-09-13-phase-5-full-corpus-retrieval-reranking-implementation-plan.md`, không thấy; thẻ N2-14 ghi "bm25_finalist = None" ở bản món ăn và "không thấy ai chốt / ngày" cho việc bỏ TF-IDF [tài liệu]. 0,726 / 0,721: thẻ T3-02 dòng 7B [đã chạy, chưa kiểm theo cặp].
- Các mục mới đã qua một lượt đối chiếu độc lập (một agent khác chỉ đọc, 22/11/2026), các dòng sai / lệch đã sửa lúc 14:17: `data/hoc_cung_D/kiem/muc_moi_02_07_11_va_phu_luc.md` [riêng tư].

</details>
