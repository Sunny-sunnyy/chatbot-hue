# Bài 19 — Chấm câu trả lời: ba thang điểm, người chấm là model, và nhiễu

*Cập nhật 17:19, ngày 28/11/2026 · mở rộng lớp chấm bám nguồn ngữ nghĩa Đợt 4A từ 20 câu nền lên **trọn bộ 176 câu mẫu** ở Đợt 6 (28/11/2026, `gpt-6-luna`: đúng **`156/158` (`98,73%`)**, từ chối sạch **`18/18`**, bám nguồn ngữ nghĩa trung bình **`89,99%`**, sạch tuyệt đối **`125/156 = 80,13%`**); cách chấm chung vẫn lấy từ chương trình đo và các lượt từ 24/10 tới 19/11.*

**Bài trước đã biết:** bước tìm được chấm riêng, bằng hai thước do chương trình tính.
**Bài này thêm:** nửa sau: chấm chính câu trả lời. Việc này không tính được bằng chương trình, nên người chấm là một model. Bài này nói nó chấm thế nào, và cách đọc điểm của nó cho khỏi bị lừa.

## Ý chính

- Mỗi câu trả lời được chấm **ba điểm từ 1 tới 5**: đúng (không trái đáp án mẫu), đủ ý (có đủ các ý cần), trọng tâm (trả lời thẳng điều được hỏi).
- **Người chấm là một model**, làm theo một đề chấm cố định, và chấm **mù**: nó không biết câu trả lời nào của bản nào.
- Hai bản của hệ thống được **so theo cặp trên cùng một câu hỏi**, kèm một khoảng tin cậy. Khoảng đó không chứa 0 thì mới nói là khác thật.
- Hệ thống có **nhiễu**: chạy cùng một bản hai lần, điểm vẫn lệch một chút. Một thay đổi phải thắng vượt mức nhiễu mới được coi là tốt hơn.
- Ngoài điểm còn có các **điều kiện không được vỡ**: 0 câu ngoài kho được trả lời, các số của bộ an toàn. Vỡ một điều kiện thì mặc định là bỏ, dù điểm trung bình tăng; vài lần giữ ngoại lệ đều có ghi lý do (bài 20).

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| người chấm là model | **LLM-as-judge** | dùng một model ngôn ngữ để cho điểm câu trả lời theo một đề chấm |
| chấm mù | **blind evaluation** | người chấm không biết câu trả lời đến từ bản nào |
| so theo cặp | **paired comparison** | so điểm của hai bản trên cùng một câu hỏi, rồi mới gộp |
| khoảng tin cậy 95 % | **confidence interval**, tính bằng **bootstrap** | khoảng mà mức chênh thật nhiều khả năng nằm trong; tính bằng cách rút lại bộ câu nhiều lần |
| nhiễu | **noise**; phép đo gọi là **A/A test** | mức điểm tự lệch khi chạy cùng một bản hai lần |

## Ba điểm cho mỗi câu trả lời

Người chấm nhận đúng ba thứ: câu hỏi, đáp án mẫu, và câu trả lời của hệ thống. Nó cho ba điểm nguyên từ 1 tới 5.

| Tiêu chí | 5 điểm nghĩa là | Bị trừ khi |
|---|---|---|
| **Đúng** | không có gì trái với đáp án mẫu | nói ngược, sai số, sai tên |
| **Đủ ý** | có đủ các ý cần của đáp án mẫu | thiếu ý |
| **Trọng tâm** | trả lời thẳng điều được hỏi | lan man, thêm thứ không cần |

Vài luật trong đề chấm quyết định cách đọc điểm:

- Người chấm chỉ dựa vào ba thứ được đưa, không dùng hiểu biết riêng.
- Nó không chấm số nguồn; việc đó chương trình đã kiểm (bài 16).
- Đáp án mẫu là câu từ chối thì hệ thống từ chối là đúng; trả lời như thể biết là sai.
- Đáp án mẫu có nội dung mà hệ thống từ chối thì điểm rất thấp. Vì vậy mỗi câu từ chối nhầm kéo điểm trung bình xuống nhiều.

## Người chấm là model, và chấm mù

Người chấm đã đổi ba lần, và điều này quyết định số nào so được với số nào:

| Thời gian | Người chấm | Ghi chú |
|---|---|---|
| 24/10 tới 19/11 | Claude | chấm bằng cách đọc một file đã xáo thứ tự và che tên bản; gpt-6-luna chấm phụ một lần (24/10) để đối chiếu, hai bên khớp ở mức cao |
| ban ngày 21/11 | gpt-6-luna | dùng cho các phép so lúc đổi model viết sang Claude |
| từ tối 21/11 | Claude Sonnet 5.5, tức chính model đang viết | quyết định sau khi chủ dự án cho dừng gọi gpt-6-luna |

Hầu hết con số trong giáo trình thuộc giai đoạn đầu: model viết là gpt-6-luna, người chấm là Claude.

Khi so hai bản của hệ thống, câu trả lời của cả hai được trộn vào một xấp, che tên bản, xáo thứ tự. Hai câu trả lời giống hệt nhau chỉ chấm một lần. Nhờ vậy người chấm khó thiên vị "bản mới" (vẫn có dấu vết lọt qua, mục "Quyết định và lý do").

Bộ an toàn có một người chấm riêng, chuyên đếm lỗi nặng; người chấm đó được kiểm bằng 15 câu đối chứng (bài 17). Người chấm ba điểm của bài này thì được kiểm bằng hai cách khác: cho chấm lại cùng một câu trả lời xem điểm có đổi không, và so điểm của nó với một model khác.

## So theo cặp, và khoảng tin cậy

So hai con số trung bình với nhau thì dễ bị lừa: một bản có thể hơn ở trung bình chỉ vì vài câu. Cách làm ở đây:

1. Với **mỗi câu hỏi**, lấy điểm của bản mới trừ điểm của bản cũ.
2. Đếm: bao nhiêu câu tốt lên, bao nhiêu như cũ, bao nhiêu tệ đi.
3. Tính trung bình của các hiệu, kèm **khoảng tin cậy 95 %**.

Ví dụ đã gặp: đưa 10 đoạn thay vì 5 làm điểm "đủ ý" tăng 0,26, khoảng tin cậy từ +0,08 tới +0,48. Khoảng này không chứa 0, nên mức tăng là thật. Ngược lại, thử 15 đoạn cho mức chênh −0,008, khoảng từ −0,140 tới +0,116: chứa 0, tức không khác.

Khi thử nhiều bản cùng lúc, ngưỡng được nâng lên: thử năm bản thì dễ có một bản trông như thắng chỉ do may.

## Nhiễu: cùng một bản chạy hai lần vẫn lệch

Model viết không cho ra đúng một câu trả lời mỗi lần (bài 1), và người chấm cũng không chấm y hệt hai lần. Vì vậy trước khi tin một mức chênh, phải biết hệ thống **tự lệch bao nhiêu**.

Phép đo: chạy cùng một bản hai lần trên bộ câu mẫu, chấm cả hai trong cùng một xấp đã che tên, rồi so như hai bản khác nhau. Lần đo ngày 19/11 (model viết gpt-6-luna, bản trợ lý đang chạy, hai lượt cách nhau một ngày): trên 129 câu tính điểm, có 1 câu đổi điểm "đúng", 2 câu đổi điểm "đủ ý", 7 câu đổi điểm "trọng tâm". Ở một cặp lượt không đổi gì chạy sáng 19/11, điểm "đủ ý" trung bình lệch nhau 0,031.

Từ đó có hai luật:

- **Thay đổi không nhằm tăng điểm** (sửa kho, thêm tính năng, làm nhanh hơn) phải qua luật "không làm hỏng": điểm trung bình không tụt quá 0,1, và số câu tệ đi không vượt mức nhiễu cộng 3.
- **Thay đổi nhằm tăng điểm** phải tăng vượt mức nhiễu, có khoảng tin cậy không chứa 0; và trên nhóm câu để kiểm lại nó phải cùng chiều, không làm hỏng gì (bài 17).

## Các điều kiện không được vỡ đứng trên điểm

Điểm trung bình không phải thứ quyết định cuối cùng. Có những điều kiện mà không thay đổi nào được làm vỡ:

- 0 câu ngoài kho được trả lời bằng kho;
- 0 lỗi kỹ thuật, 0 lỗi số nguồn;
- không thêm câu "nói chắc mà sai";
- bộ an toàn: 0 câu nói ngược cảnh báo, 0 câu ngoài kho bị trả lời; không thêm câu thiếu cảnh báo, không thêm câu sai điều kiện (ngưỡng ghi trước cho từng lượt đo).

Và khi phải đánh đổi, thứ tự lỗi ở bài 4 quyết định. Ví dụ ở bài 15: cho trả lời một phần làm từ chối nhầm giảm từ 13 xuống 1 (lỗi nhẹ nhất giảm mạnh) nhưng để 2 câu ngoài kho được trả lời (lỗi nặng hơn xuất hiện), nên bị bỏ.

## Quyết định và lý do

### 1. Vì sao để một model chấm, mà không để người chấm?

- **Đã chọn:** người chấm là model, theo một đề chấm cố định.
- **Vì sao:** hồ sơ đánh giá ghi: cần một người chấm tự động, rẻ, lặp lại được cho mọi lần so. Một lần so là hai bản trên 176 câu, tức khoảng 350 câu trả lời, và dự án có khoảng 45 lần so.
- **Cách khác:** chấm tay khoảng 20 câu có trong kế hoạch ban đầu (24/10); ngày 25/10 chủ dự án chọn thay bằng việc tự đọc 20 cặp câu trả lời đã che tên, làm xong ngày 01/11: phần lớn các cặp như nhau, không cặp nào phân thắng thua.
- **Cái giá:** không có mốc từ người thật cho điểm số. Người chấm là model có thể lệch theo cách riêng của nó.

### 2. Vì sao người chấm lúc đầu là Claude, và vì sao nay là chính model đang viết?

- **Đã chọn:** từ 24/10 tới 19/11, Claude chấm chính, gpt-6-luna chấm phụ để đối chiếu. Từ tối 21/11, Claude Sonnet 5.5 vừa viết vừa chấm.
- **Vì sao:** ngày 24/10, kế hoạch cũ để gpt-6-luna chấm, tức model tự chấm bài mình; chủ dự án đổi sang Claude vì "tiết kiệm; khác họ với model sinh" (khi đó model viết là gpt-6-luna). Tối 21/11 chủ dự án hết tiền cho gpt-6-luna và hỏi "chấm bộ 176 câu mẫu sao không dùng Sonnet luôn".
- **Cách khác:** giữ một người chấm khác họ với model viết: lý do của lần chọn 24/10; tạm không làm được vì gpt-6-luna đã dừng.
- **Cái giá:** quyết định tối 21/11 đi ngược lý do 24/10: một model chấm bài của chính họ mình có thể chấm dễ hơn. Số mới không so thẳng với mọi số trước đó; cần một lượt mốc mới.

### 3. Vì sao chấm mù, trộn hai bản vào một xấp?

- **Đã chọn:** che tên bản, xáo thứ tự; câu trả lời giống hệt nhau chỉ chấm một lần.
- **Vì sao:** lập luận: người chấm biết đâu là "bản mới" thì dễ nghiêng về nó. Có căn cứ đo cho việc chấm cả hai bản trong cùng một lượt: nếu hôm đó người chấm khó tính hơn thì cả hai bản cùng bị khó như nhau; phần lệch do người chấm nhỏ (2 trên 88 câu), so với phần lệch do model viết (10 trên 83 câu).
- **Cách khác:** dùng lại điểm cũ của bản mốc, chỉ chấm bản mới: không làm.
- **Cái giá:** mỗi lần so phải chấm lại cả hai bản. Che tên không che được mọi dấu vết: hồ sơ ghi có lần người chấm có thể đoán bên qua số nguồn [6]–[10], vốn chỉ có ở bản đưa 10 đoạn.

### 4. Vì sao so theo cặp trên từng câu, mà không so hai điểm trung bình?

- **Đã chọn:** với mỗi câu lấy điểm bản mới trừ điểm bản cũ; đếm số câu tốt lên, như cũ, tệ đi; tính khoảng tin cậy trên các hiệu.
- **Vì sao:** luật của bộ đo. Hai trung bình gần bằng nhau có thể che một bản giúp vài câu và làm hỏng vài câu khác. Ví dụ thật: thử một model embedding lớn giúp 2 câu và làm hỏng 3 câu; trung bình gần như không đổi, nhưng 3 câu mất đoạn đúng là đủ để bỏ (bài 10).
- **Cách khác:** so hai điểm trung bình: không dùng.
- **Cái giá:** chỉ so được hai bản chạy trên cùng một bộ câu.

### 5. Vì sao phải đo nhiễu trước khi tin một mức chênh?

- **Đã chọn:** chạy cùng một bản hai lần, coi như hai bản khác nhau, để biết hệ thống tự lệch bao nhiêu.
- **Vì sao:** model viết không cho ra cùng một câu mỗi lần. Đã đo (19/11, gpt-6-luna): 1, 2 và 7 câu tự đổi điểm ở ba tiêu chí. Một thay đổi "làm 2 câu tệ đi" vì thế chưa nói lên điều gì.
- **Cách khác:** dùng một ngưỡng cố định không đo: không dùng.
- **Cái giá:** tốn thêm một lượt chạy và chấm. Số nhiễu đang dùng là của model cũ; chưa đo lại trên model đang chạy, nên luật "mức nhiễu cộng 3" hiện dựa trên số của gpt-6-luna.

### 6. Vì sao các điều kiện không được vỡ đứng trên điểm trung bình?

- **Đã chọn:** xét điều kiện trước; vỡ thì mặc định là bỏ.
- **Vì sao:** thứ tự lỗi do chủ dự án đặt (bài 4). Lập luận: điểm trung bình trộn mọi loại lỗi vào một con số; một câu ngoài kho bị trả lời nặng hơn nhiều câu thiếu ý, nhưng trong trung bình nó chỉ là một câu.
- **Cách khác:** quyết bằng điểm trung bình: không dùng.
- **Cái giá:** đã bỏ những thay đổi có lợi rõ về trung bình. Ví dụ ở bài 15: từ chối nhầm giảm từ 13 xuống 1, nhưng 2 câu ngoài kho bị trả lời.

Hai quyết định nhỏ hơn ở nửa để tra.

## Nếu… thì sao

| Nếu | Phải làm gì, hoặc chuyện gì xảy ra | Đã có chưa |
|---|---|---|
| điểm trung bình tăng nhưng một điều kiện vỡ | bỏ thay đổi đó, trừ vài lần giữ ngoại lệ có ghi lý do (bài 20) | đã có, đã áp nhiều lần |
| mức chênh nhỏ hơn mức nhiễu | kết luận "không khác" hoặc "chưa rõ"; không đưa vào vì lý do chất lượng | đã có |
| đổi người chấm | số chấm bởi người chấm mới không so thẳng với số cũ; phải chấm lại bản mốc bằng người chấm mới | **chưa làm** cho lần đổi tối 21/11 |
| đổi model viết | bảng mốc của bài này (đo với gpt-6-luna) không còn là số của hệ thống đang chạy | **chưa** chấm lại đủ bộ 176 câu trên model đang chạy |
| người chấm chấm sai một câu | không có ai soát từng điểm. Chỗ dựa: chấm lại cùng câu thì ít đổi (2 trên 88), và một lần khớp cao với model khác | chỉ có kiểm gián tiếp |
| một lượt đo cuối không đạt một điều kiện | ghi vào danh sách "chưa đạt" đi kèm mốc; mỗi mục ghi là sửa, để nguyên làm giới hạn, hay chờ người nhận | lượt 18/11: 1 trên 18 câu ngoài kho bị trả lời; mốc 19/11 ghi "để nguyên, chưa ai nhận sửa" |

## Dễ nhầm

- **"Điểm tăng 0,1 là tốt hơn."** Chưa chắc. Phải so với mức nhiễu và nhìn khoảng tin cậy.
- **"Model chấm thì không tin được."** Nó có giới hạn, nhưng nó chấm mù, theo đề chấm cố định; chấm lại cùng một câu thì điểm gần như không đổi; và một lần đã khớp ở mức cao với một model khác.
- **"Trung bình tăng là được nhận."** Không. Số câu tệ đi và các điều kiện không được vỡ được xét trước.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Người chấm cho mấy điểm, theo tiêu chí nào, và nó nhìn thấy gì?</summary>

Ba điểm nguyên từ 1 tới 5: đúng, đủ ý, trọng tâm. Nó chỉ thấy câu hỏi, đáp án mẫu và câu trả lời; không biết câu trả lời của bản nào.

</details>

<details>
<summary>2. Khi nào được nói "bản mới tốt hơn thật"?</summary>

Khi so theo cặp trên cùng câu, mức tăng vượt mức nhiễu và khoảng tin cậy 95 % không chứa 0; đồng thời không điều kiện nào vỡ và trên nhóm kiểm lại nó cùng chiều.

</details>

<details>
<summary>3. Vì sao việc để Claude Sonnet 5.5 chấm từ tối 21/11 là một bước lùi đã biết?</summary>

Ngày 24/10 chủ dự án chọn người chấm khác họ với model viết. Từ 21/11 model viết và người chấm cùng là Claude, có thể chấm dễ hơn; số mới cũng không so thẳng với số cũ, cần một lượt mốc mới.

</details>

<details>
<summary>4. "1, 2 và 7 câu tự đổi điểm" là số gì, và dùng để làm gì?</summary>

Là nhiễu: chạy cùng một bản hai lần (19/11, gpt-6-luna, 129 câu), số câu đổi điểm ở "đúng", "đủ ý", "trọng tâm". Một thay đổi phải hơn mức đó mới được coi là có tác dụng.

</details>

## Cấu hình đang chạy

*Theo chương trình đo sáng 22/11/2026.*

| Mục | Giá trị | Dùng để làm gì, vì sao là giá trị này | Đã thử giá trị khác chưa |
|---|---|---|---|
| Thang điểm | ba tiêu chí, mỗi tiêu chí một điểm nguyên 1–5 | — | — |
| Đề chấm | một file cố định, dùng chung cho mọi model chấm | số của các lượt so được với nhau | — |
| Người chấm | lệnh chấm của chương trình đo mặc định dùng gpt-6-luna; chọn được Claude Sonnet 5.5 (mức suy luận cao). Quyết định từ tối 21/11: dùng Claude Sonnet 5.5. Trước đó: bảng ở mục "Người chấm là model" | chủ dự án cho dừng gọi gpt-6-luna | hai model chấm đã được so với nhau một lần trên 176 câu (24/10): khớp ở mức cao |
| Cách so hai bản | theo cặp trên cùng câu; khoảng tin cậy 95 % bằng cách rút lại bộ câu 10.000 lần; nâng ngưỡng khi thử nhiều bản | — | — |
| Cách nhận ra câu từ chối khi đếm | so nguyên câu với một trong hai câu cố định (kho không có · ngoài phạm vi) | chương trình đếm được, không cần người chấm | — |
| Luật "không làm hỏng" | điểm trung bình không tụt quá 0,1; số câu tệ đi không quá mức nhiễu cộng 3 | cho thay đổi không nhằm tăng điểm | — |
| Số câu của số chính | 129 câu (bỏ câu không tự nhiên và câu ngoài kho, bài 17) | — | — |

## Các con số chính của đường hỏi đáp

Bảng này là mốc mà các bài sau so vào. Mọi dòng đo với model viết gpt-6-luna.

| Đo gì | Giá trị | So với mốc nào | Đọc thế nào |
|---|---|---|---|
| Điểm **đúng**, 129 câu | 4,71 | bản đầu tiên 4,43 | cao; chỉ tính câu được trả lời là 4,96: khi đã trả lời thì gần như không sai |
| Điểm **đủ ý** | 4,58 | bản đầu tiên 4,28 | phần mất chủ yếu ở câu nhiều nguồn và ở từ chối nhầm |
| Điểm **trọng tâm** | 4,72 | bản đầu tiên 4,45 | tốt |
| Đủ ý, riêng **câu nhiều nguồn** | 3,50 | câu một dữ kiện 4,91 · có điều kiện 4,68 · so sánh 4,35 | yếu nhất; là lý do cho trợ lý tự tìm thêm (bài 21) |
| **Từ chối nhầm** trên 158 câu | 3 (lượt đo cả hệ thống 12/11; lượt đo cuối 18/11 cũng ra 3) | 22 khi đưa 5 đoạn; 12 khi đưa 10 đoạn; bản hỏi đáp chạy cùng lượt: 13 (12/11) và 12 (18/11) | khoảng 2 %; là lỗi nhiều nhất còn lại, và là lỗi nhẹ nhất theo thứ tự lỗi |
| **Câu ngoài kho bị trả lời**, câu hỏi một lượt | 0 trên 18 ở bản hỏi đáp (01/11) và ở lượt 12/11; **1 trên 18** ở lượt đo cuối 18/11 của bản trợ lý | điều kiện: 0 | lượt 18/11 không đạt: trợ lý nói "nguồn không nêu" rồi vẫn thêm một lời khuyên có nguồn (không bịa con số); tới 19/11 chưa sửa |
| Đủ ý trên **bộ cất riêng** 40 câu | 4,18 | bộ quen 4,58 | số trên bộ quen lạc quan hơn khoảng 0,4 |

## Quyết định nhỏ hơn

**Vì sao nâng ngưỡng khi thử nhiều bản cùng lúc?** Thử năm bản thì xác suất có ít nhất một bản trông như thắng chỉ do may lớn hơn nhiều so với thử một bản. Bộ đo dùng cách hiệu chỉnh Holm để bù: khi có nhiều bản, mỗi bản phải thắng rõ hơn mới được nhận. Cái giá: cần nhiều câu thắng hơn.

**Vì sao không dùng thước tự động đếm chữ trùng, hay một bộ thư viện đánh giá RAG có sẵn?** Thước tự động đếm xem câu trả lời có bao nhiêu chữ trùng với đáp án mẫu (tên gốc: BLEU, ROUGE): chưa thử; lập luận, không phải số đo: một câu trả lời đúng có thể viết bằng chữ khác hẳn đáp án mẫu. Bộ thư viện đánh giá RAG có sẵn: chưa thử; chưa thấy ghi lý do không xét. Điều có thật: bộ đo của dự án tách bước tìm và câu trả lời, so theo cặp và đếm các điều kiện riêng của sản phẩm.

Luật "không làm hỏng" nói bằng lời thường: số câu bị điểm thấp hơn không được nhiều hơn số câu tự đổi điểm khi chạy lại y nguyên, cộng thêm 3; và điểm trung bình không tụt quá 0,1.

## Đánh giá 3 tầng và lớp chấm bám nguồn ngữ nghĩa (Đợt 4A, 27/11)

Ngoài ba điểm chấm tổng thể trên câu trả lời (đúng, đủ ý, trọng tâm), từ Đợt 4A (27/11) mình bổ sung lớp đánh giá **3 tầng** trên nền bộ 176 câu mẫu:

1. **Tầng 1 — Bám nguồn ngữ nghĩa (không chạy khi khách chat):** chương trình tách câu trả lời thành từng mệnh đề đơn đã khử đại từ ("ở đó", "nơi này" đổi về đúng tên nơi/món) rồi đối chiếu trực tiếp với đúng đoạn nguồn được gắn số trích dẫn `[n]` và toàn bộ tập nguồn đã lấy về. Như vậy máy bắt được cả trường hợp số nguồn `[n]` có thật nhưng nội dung viết ra lại nói sai hoặc suy diễn ngoài đoạn trích.
2. **Tầng 2 — Độ chính xác gọi công cụ (`0 đồng` tiền API):** chấm từ nhật ký cuộc gọi xem model có chọn đúng công cụ và truyền đúng tham số kỳ vọng hay không (bài 32).
3. **Tầng 3 — Điểm trả lời, độ trễ và tiền API:** giữ nguyên bộ chấm ba tiêu chí kết hợp đo thời gian chờ, tiền API thật và tỷ lệ dùng lại bộ nhớ đệm ngữ cảnh.

**Kết quả kiểm định và đo trọn bộ trên `gpt-6-luna`:**
- **Kiểm định người chấm bám nguồn ngữ nghĩa (Đợt 4A, 27/11):** khớp **`15/15` (`100%`)** với nhãn đọc tay của người kiểm, và bắt trúng **`3/3`** ca cố tình gán sai số nguồn `[n]`.
- **Mốc nền 20 câu mẫu (Đợt 4A, 27/11):** điểm bám nguồn trung bình đạt **`88,33%`** (`17/20` câu sạch tuyệt đối, `0` ca gán sai số nguồn, `5` mệnh đề chưa đủ căn cứ).
- **Đo trọn bộ 176 câu mẫu (Đợt 6, 28/11 — `0,153266 USD` gồm `0,093631` chạy 176 câu + `0,059636` chấm 156 câu):**
  - Trả lời đúng **`156/158` (`98,73%`)** câu trong kho (từ chối nhầm chỉ `2` ca, so với mốc 12/11 và 18/11 còn `3/158`), từ chối sạch **`18/18`** câu ngoài phạm vi (vượt hẳn ca `1/18` ở 18/11), `0` lỗi hệ thống.
  - Điểm bám nguồn ngữ nghĩa trung bình đạt **`89,99%`** (cao hơn mốc nền 20 câu `88,33%`), với **`125/156` (`80,13%`)** câu sạch tuyệt đối (không một mệnh đề nào bị gắn cờ).
  - Rà tay toàn bộ `26` câu còn lại bị bộ chấm NLI gắn cờ: chỉ có **`2` ca thật sự tự suy thêm chi tiết ngoài đoạn trích** (một câu đoán lịch sử thành lập làng nghề, một câu tự diễn giải thêm công dụng món ăn) và **`5` ca gắn lệch số nguồn `[n]`**, còn phần lớn (~20 ca) là máy chấm NLI chấm quá chặt khi câu trả lời hợp nhất đúng dữ kiện từ nhiều nguồn hoặc điểm đồng danh — cho thấy bộ chấm tự động bắt tốt lỗi lệch trích dẫn nhưng vẫn cần người kiểm đọc lại các ca bị gắn cờ trước khi kết luận là bịa.

## Giới hạn đã biết

- **Người chấm là model.** Nó có thể chấm lệch. Ở lớp chấm bám nguồn ngữ nghĩa NLI trên trọn 156 câu (Đợt 6), hơn ba phần tư số ca bị gắn cờ thực chất là câu hợp nhất đa nguồn hoặc đồng danh hợp lệ, nên không đọc máy móc con số `80,13%` sạch tuyệt đối như tỷ lệ "không bịa" nếu chưa đọc phân loại tay. Mốc từ người thật cho bảng điểm 3 tiêu chí mới có một lần: chủ dự án tự đọc 20 cặp câu trả lời.
- **Từ tối 21/11, người chấm cùng họ với model viết** khi chấm bằng model đang chạy; riêng bộ bám nguồn ngữ nghĩa ở Đợt 4A và Đợt 6 chạy trên `gpt-6-luna` với đề tách mệnh đề độc lập.
- **Luật "không làm hỏng" chỉ bắt được tụt lan rộng.** Tụt nhỏ dồn vào một loại câu ít có thể lọt.
- **Bộ an toàn nhỏ.** 0 lỗi trên 28 câu chỉ cho biết tỉ lệ lỗi dưới khoảng 10–12 %, chưa cho biết nó rất thấp.
- **Thước chấm 3 tiêu chí (1–5) trên trọn bộ 176 câu chưa chạy lại với cặp người chấm khác họ**, vì Đợt 6 đo trọn bộ theo hướng kiểm tra tỷ lệ trả lời/từ chối và lớp bám nguồn ngữ nghĩa từng mệnh đề.

## Chi tiết để tra

- Lượt mốc của đường hỏi đáp: ngày 01/11. Bản đầu tiên: ngày 24/10 (đáp án mẫu sau đó có sửa, nên hai lượt chỉ so tương đối).
- Đo nhiễu ở cấu hình 10 đoạn (cuối tháng 10, 176 câu): "đủ ý" tự tụt 1 câu, "đúng" tự tụt 2 câu.
- Trước đó, ngày 25/10, ở cấu hình 5 đoạn: riêng người chấm chấm lại cùng một câu trả lời thì đổi điểm "đủ ý" ở 2 trên 88 câu (1 câu ở "đúng", 3 câu ở "trọng tâm"); cho model viết lại rồi chấm lại thì 10 trên 83 câu đổi điểm "đủ ý". Tức phần lớn nhiễu đến từ model viết, không từ người chấm.
- Hai model chấm (Claude và gpt-6-luna) so trên 176 câu ngày 24/10: mức khớp từ 0,892 tới 0,960 tuỳ tiêu chí.
- Giai đoạn 24/10 tới 19/11, "Claude chấm" nghĩa là các agent Claude đọc file câu trả lời đã che tên bản; việc này không qua lệnh chấm của chương trình đo và không tốn tiền gọi model.
- Với thước nhỏ của phần trợ lý (41 câu khó, model đang chạy), mức nhiễu giữa hai lượt cùng bản: số mục đạt lệch nhiều nhất 3; thời gian ở giữa lệch nhiều nhất 3 giây. Luật đọc thước nhỏ: ít nhất ba lượt lặp mỗi bên (bài 32).
- Bộ an toàn ở lượt đo cả hệ thống 12/11 (chạy hai lượt): 0 câu nói ngược cảnh báo, 0 câu ngoài kho bị trả lời, 1 câu thiếu một điều kiện cảnh báo.

**Bài sau (bài 20):** ghép ba bài vừa rồi lại: một lần thử được làm theo các bước nào, và nhìn cả bảng 45 lần so sánh của dự án thì thấy gì.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Đề chấm, ba tiêu chí, các luật của đề chấm: `backend/evaluation/full_corpus_judge_prompt.md`; chấm mù, câu giống hệt chấm một lần, so theo cặp, rút lại 10.000 lần, nâng ngưỡng khi thử nhiều bản, nhận câu từ chối bằng so nguyên câu: `backend/evaluation/full_corpus_eval.py` [code; chép qua `bai_hoc/11_CHAM_CAU_TRA_LOI.md`, bài đã qua kiểm độc lập].
- Người chấm: Claude chính, gpt-6-luna phụ, khớp 0,892–0,960: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ E1. Chọn model chấm theo `provider`: `full_corpus_eval.py` (`JUDGE_PROVIDERS`, `judge_settings`). Từ tối 21/11 chấm bằng model đang chạy; lưu ý "cùng họ có thể chấm dễ hơn": `session_prompt/HIEN_TRANG.md` mục 4, gạch 21:43 21/11/2026.
- Nhiễu 1 / 2 / 7 (19/11) và thước 41 câu: `session_prompt/HIEN_TRANG.md` mục 2 (dòng "Số nhiễu"); lệch 0,031 giữa hai lượt không đổi gì: `bai_hoc/VIEC_MOI_XONG.md` mục 14. Nhiễu cuối tháng 10 (1–2 câu; 2 / 88; 10 / 83), luật "không làm hỏng": `bai_hoc/11_CHAM_CAU_TRA_LOI.md`.
- Bảng số chính (4,71 / 4,58 / 4,72; 4,96; 3,50 và các loại câu; 22 ⇒ 12 ⇒ 3; 13; 0 / 18; 4,18; bộ an toàn 12/11; 20 cặp chủ dự án đọc): `bai_hoc/11_CHAM_CAU_TRA_LOI.md` mục "Mọi con số chính" và "Mốc người" [đã chạy; chép].
- +0,26 [+0,08; +0,48]; 15 đoạn −0,008 [−0,140; +0,116]: `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 10; `bai_hoc/VIEC_MOI_XONG.md` mục 14.
- Bộ an toàn chỉ chứng minh được tỉ lệ dưới khoảng 10–12 %: `bai_hoc/11_CHAM_CAU_TRA_LOI.md` mục "Khi nào hỏng".
- Lịch sử người chấm (Claude đọc file đã che tên 24/10–19/11; gpt-6-luna ban ngày 21/11; quyết định tối 21/11; lệnh chấm mặc định gpt-6-luna), lượt đo cuối 18/11 (từ chối nhầm 3 so với 12; 1 trên 18 câu ngoài kho bị trả lời, chưa sửa tới 19/11), nhiễu tính trên 129 câu, 2 / 88 và 10 / 83 đo ở cấu hình 5 đoạn ngày 25/10, chủ dự án chọn không chấm tay 24/10: `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md`, `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` (thẻ E1, E3, E7), `bai_hoc/VIEC_MOI_XONG.md` mục 10 và 23, `session_prompt/HIEN_TRANG.md` mục 4, `backend/evaluation/full_corpus_eval.py` (`--provider`) — theo biên bản kiểm `data/hoc_cung_D/kiem/bai_17_20.md`.
- Mục "Quyết định và lý do", "Nếu… thì sao", "Quyết định nhỏ hơn" (sửa theo biên bản `data/hoc_cung_D/kiem/muc_moi_05_06_17_20.md` phần bài 19 [riêng tư]): "cần một người chấm tự động, rẻ, lặp lại được", chủ dự án chọn Claude 24/10 "tiết kiệm; khác họ với model sinh", luna phụ khớp 0,892–0,960: `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` thẻ E1; chấm tay 20 câu trong kế hoạch 24/10, thay bằng đọc cặp mù (chủ dự án chọn 25/10), xong 01/11: `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` và thẻ E7; chấm cùng lượt 2 / 88 so với 10 / 83 (thẻ E3), đoán bên qua [6]–[10]: `91_BAO_CAO…` (giới hạn của nhóm B1 / B3); khoảng 45 lần so: `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` (45 hàng); 2 giúp / 3 hỏng: bảng tổng hàng số 2; lời chủ dự án 21:43 21/11: `session_prompt/HIEN_TRANG.md` mục 4; nhiễu chưa đo lại trên model đang chạy: `HIEN_TRANG.md` mục 2; mốc 19/11 kèm danh sách chưa đạt, "để nguyên, chưa ai nhận sửa": `bai_hoc/VIEC_MOI_XONG.md` mục 11 (19/11); Holm: `skills/run-experiment/SKILL.md` (mục cỡ mẫu và mục so theo cặp); tìm `ragas`, `bleu`, `rouge`, `deepeval`, `trulens` trong mã và tài liệu: 0 kết quả (theo biên bản).
- **Đợt 4A (27/11/2026):** bổ sung bộ chấm bám nguồn ngữ nghĩa hai bước (tách mệnh đề đơn khử đại từ qua `EXTRACT_INSTRUCTIONS` → kiểm đối chiếu đúng nguồn trích dẫn `cited_supported` và tập nguồn truy hồi `context_supported`) ở `backend/evaluation/faithfulness_eval.py` cùng unit test `backend/tests/test_faithfulness_eval.py`; kiểm định `15/15 = 100%`, bắt `3/3` ca cố tình gán sai `[n]`, mốc nền Golden 20 câu đạt `88,33%` (`17/20` sạch, `0` gán sai nguồn, `5` mệnh đề thiếu căn cứ gồm tách/gộp `[n]` ở `gb_05`, `gb_17` và thiếu dữ kiện ở `gb_18`) — số đo Đợt 4A từ `session_prompt/HIEN_TRANG.md` và báo cáo kết luận Đợt 4A [đã chạy thật; riêng tư cho bảng chi tiết từng ca].
- **Đợt 6 (28/11/2026):** chạy trọn bộ 176 câu mẫu trên `main` `660de3fc` (`gpt-6-luna`, tổng `0,153266 USD`): `156/158` (`98,73%`) câu kho trả lời đúng, `18/18` câu ngoài phạm vi từ chối sạch, `0` lỗi hệ thống; `faithfulness_eval.py` trên đủ `156` câu đạt trung bình `89,99%`, `125/156` (`80,13%`) sạch tuyệt đối (`0` cờ); trong `26` ca bị gắn cờ còn lại chỉ có `2` ca tự suy ngoài đoạn trích (`case 51, 111`) và `5` ca lệch `[n]` (`case 47, 68, 114, 149, 170`) theo `data/thu_dot6_2026-11-28/BAO_CAO_LOI_GOLDEN_176.md` & `KET_LUAN_DOT6.md`.

</details>
