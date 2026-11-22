# Bài 1 — Model ngôn ngữ là gì, và vì sao nó viết trôi chảy mà vẫn sai

*Cập nhật 16:11, ngày 22/11/2026 · phân xử chỗ lệch giữa các bài · trước đó: phần giải thích chung là kiến thức phổ thông về model ngôn ngữ; các con số của hue_rag lấy từ một lượt hỏi thật ngày 21/11 và từ các lượt đo đã ghi; người viết không chạy lại.*

**Bài này mở đầu cả bộ.** Không cần biết gì trước, ngoài việc đã từng dùng một chatbot.
**Bài này thêm:** thứ nằm ở giữa mọi hệ thống kiểu này là một model ngôn ngữ. Bài này nói nó làm được gì, không làm được gì, và vì sao hue_rag phải xây cả một hệ thống quanh nó.

## Ý chính

- **Model ngôn ngữ** là một chương trình được huấn luyện để viết tiếp chữ. Nó viết ra chữ có khả năng cao nhất theo những gì nó đã đọc lúc huấn luyện; nó không tra cứu gì.
- Nó tính độ dài bằng **token**, và mỗi lần gọi được tính tiền theo số token gửi vào và số token viết ra.
- Nó sai theo bốn kiểu mà hue_rag phải xử lý: kiến thức cũ, không biết dữ liệu riêng, viết chắc điều không có, và tính toán sai.
- Nó **không nhớ gì** giữa hai lần gọi. Mọi thứ nó cần biết phải được gửi kèm trong chính lần gọi đó.
- Cả hệ thống hue_rag là câu trả lời cho bốn kiểu sai trên: đưa tài liệu cho model đọc (bài 2), giao việc tính cho chương trình (bài 3), và kiểm chữ model viết.

## Từ dùng trong bài

| Tên trong bài | Tên gốc | Nghĩa |
|---|---|---|
| model ngôn ngữ | **LLM** (large language model) | chương trình viết tiếp chữ, học từ rất nhiều văn bản |
| huấn luyện | **training** | quá trình cho model đọc văn bản để nó học cách viết tiếp; làm một lần, bởi hãng làm model |
| token | **token** | mẩu chữ model dùng để đếm; một âm tiết tiếng Việt thường là một tới vài token |
| viết chắc điều không có | **hallucination** | model viết ra một điều sai hoặc không có căn cứ bằng giọng chắc chắn |
| mốc kiến thức | **knowledge cutoff** | thời điểm dữ liệu huấn luyện dừng lại; model không biết gì xảy ra sau đó |
| lời gọi | **API call** | một lần chương trình gửi chữ cho model và nhận chữ về |

## Model ngôn ngữ viết tiếp chữ, nó không tra cứu

Một model ngôn ngữ được làm ra bằng cách cho nó đọc một lượng văn bản rất lớn và học một việc: cho một đoạn chữ, chữ tiếp theo nhiều khả năng là gì. Khi được hỏi, nó viết lần lượt từng mẩu chữ theo cách đó.

Nó làm việc này rất giỏi: câu trôi chảy, đúng ngữ pháp, đúng giọng. Nhưng "trôi chảy" và "đúng" là hai chuyện. Model không mở một cuốn sách nào ra để kiểm. Thứ nó viết là thứ **nghe hợp lý nhất** theo những gì nó từng đọc.

Ở hue_rag có hai loại model, đừng lẫn với nhau:

- **Model viết:** model lớn, gọi qua mạng tới máy của hãng, tính tiền theo lượt. Hệ thống đã dùng gpt-6-luna của OpenAI, và từ 21/11 đang dùng tạm Claude Sonnet 5.5 của Anthropic (bài 33).
- **Model embedding:** model nhỏ chạy ngay trên máy, không viết được gì, chỉ đổi chữ thành dãy số để tìm (bài 10).

## Model đếm bằng token, và tính tiền theo token

Model không đếm theo chữ hay theo câu mà theo token. Mỗi lần gọi có hai con số: token gửi vào và token viết ra. Tiền của lần gọi tính từ hai con số đó.

Số thật ở ví dụ chính của cả bộ, câu *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"*: lần gọi viết câu trả lời gửi vào 5.085 token (lời dặn, phần mô tả công cụ, câu hỏi, và 10 đoạn tài liệu) và nhận về 425 token. Với giá của Claude Sonnet 5.5, lần gọi này tốn khoảng 0,014 USD, tức khoảng 360 đồng.

Hai hệ quả cho thiết kế: gửi càng nhiều chữ vào thì càng tốn và càng chậm; và model có một giới hạn về lượng chữ đọc được trong một lần gọi. Vì vậy hệ thống không gửi cả kho mà chọn ra một số đoạn. Con số 10 đoạn được chọn bằng một phép so chất lượng với 5 đoạn, không phải vì tiền (bài 13).

## Bốn kiểu sai mà hệ thống phải xử lý

**Kiến thức cũ.** Dữ liệu huấn luyện dừng ở một thời điểm. Giá vé, giờ mở cửa, lịch lễ hội của năm nay thì model không biết, hoặc biết con số của nhiều năm trước.

**Không biết dữ liệu riêng.** Model chưa từng đọc bộ bài viết về Huế của dự án. Hỏi nó một quán cụ thể mở mấy giờ, nó không có gì để dựa.

**Viết chắc điều không có.** Khi không biết, model không im lặng. Nó vẫn viết một câu nghe hợp lý, có thể kèm một con số, và giọng văn giống hệt lúc nó đúng. Người đọc không phân biệt được.

**Tính toán sai.** Model viết chữ, không làm phép tính theo cách một chương trình làm. Ở hue_rag điều này đã được đo: khi việc tính ngày được chuyển từ model sang chương trình, số câu về ngày bị từ chối nhầm bớt đi 9 câu và không còn câu nào sai ngày (bài 24).

Mỗi kiểu sai có một phần của hệ thống đối lại:

| Kiểu sai | hue_rag làm gì | Bài |
|---|---|---|
| kiến thức cũ, không biết dữ liệu riêng | đưa tài liệu của kho cho model đọc trước khi viết | 2 |
| viết chắc điều không có | dặn chỉ dùng tài liệu được đưa, bắt ghi nguồn, kiểm số nguồn có thật bằng chương trình (chưa kiểm được nghĩa), không đủ thì từ chối | 15, 16 |
| tính toán sai | chương trình tính, model chỉ diễn đạt | 3, 24 |

## Model không nhớ gì giữa hai lần gọi

Mỗi lần gọi là một lần mới hoàn toàn. Model không nhớ câu hỏi trước của người dùng, không nhớ câu nó vừa trả lời. Cảm giác "chatbot nhớ cuộc trò chuyện" có được là do chương trình gửi lại các lượt trước trong mỗi lần gọi.

Ở hue_rag, chương trình quyết định gửi lại cái gì: câu hỏi của ba lượt gần nhất, và câu trả lời của lượt liền trước (bài 23). Model không tự giữ được gì, và cũng không học thêm gì từ người dùng.

Một hệ quả nữa: cùng một câu hỏi gửi hai lần có thể nhận hai câu trả lời khác chữ nhau. Vì vậy khi đo chất lượng, một lần chạy chưa đủ để kết luận (bài 19).

## Quyết định và lý do

Bài nền này chưa có cấu hình nào để chọn. Nhưng ba quyết định lớn nhất của cả hệ thống đi thẳng ra từ bốn kiểu sai ở trên; các bài sau giảng kỹ từng cái.

### 1. Vì sao không để model trả lời bằng hiểu biết sẵn có của nó về Huế?

- **Đã chọn:** model chỉ được dùng tài liệu chương trình đưa cho. Kho không có thì từ chối; khi đó chương trình tra web và hiện riêng một mục "Từ web" có ghi nguồn (bài 16, 25).
- **Vì sao:** quyết định đã ghi của chủ dự án (bài 4). Điều thấy được từ bốn kiểu sai: hiểu biết sẵn có của model dừng ở một mốc thời gian, không gồm bộ bài của dự án, và khi không biết nó vẫn viết chắc.
- **Cách khác:** cho model dùng hiểu biết sẵn có: không thử, vì đây là luật nền của sản phẩm.
- **Cái giá:** câu nào kho không có thì phần trả lời từ kho là câu từ chối, kể cả khi model thật ra biết đúng.

### 2. Vì sao không gửi cả kho cho model đọc, mà chỉ chọn 10 đoạn?

- **Đã chọn:** mỗi lần gọi gửi 10 đoạn được chọn. Tin hỏi nhiều ý thì thêm 2 đoạn cho mỗi ý; model xin tìm thêm thì có thêm đoạn, nhiều nhất ba lần (từ 14:47 ngày 22/11; trước là hai).
- **Vì sao:** gửi cả kho thì chưa ai thử; lập luận: kho có hơn chín nghìn đoạn, quá sức một lần gọi và rất tốn. Các bước nhỏ hơn thì đã đo: 5 đoạn kém hơn 10 đoạn; 15 đoạn không hơn; đưa cả bài viết thay vì từng đoạn đắt gấp 5,5 lần nên dừng ngay (bài 13).
- **Cách khác:** 5 đoạn (đã đo 28/10, kém hơn); 15 đoạn, cả mục, cả bài (đã đo 19/11, không hơn).
- **Cái giá:** đoạn có đáp án mà không lọt vào 10 đoạn thì model không thấy; đây là nguồn chính của lỗi từ chối nhầm (bài 18).

### 3. Vì sao việc tính toán giao cho chương trình, không để model tự tính?

- **Đã chọn:** ngày tháng, khoảng cách, xếp lịch do chương trình tính; model chỉ diễn đạt kết quả.
- **Vì sao:** đã đo. Khi việc tính ngày chuyển từ model sang chương trình, số câu về ngày bị từ chối nhầm bớt 9 câu và không còn câu nào sai ngày. Model mạnh hơn cũng không chữa được: trong một lượt rà, cả hai model viết đều tính sai một phép tính tuổi theo năm.
- **Cách khác:** để model tự tính (bản trước đó). Chiều ngược lại cũng đã thử ở một việc khác: cho chương trình tự tính tổng tiền chuyến đi thì phép tính đúng 8 trên 8, nhưng câu về miễn vé bỏ mất điều kiện 3 trên 3 lần, nên bỏ (bài 24).
- **Cái giá:** mỗi loại phép tính phải có một phần chương trình riêng. Loại nào chưa có thì model vẫn tự làm, ví dụ cộng tổng tiền vé.

## Nếu… thì sao

| Nếu | Hệ thống làm gì | Người dùng thấy gì | Đã có chưa |
|---|---|---|---|
| model viết một điều tài liệu không nói | chương trình kiểm được số nguồn [n] có thật hay không; **không** kiểm được câu chữ có đúng với đoạn được trích không | có thể thấy một câu sai kèm nguồn thật | mới có một nửa: kiểm số nguồn (bài 16) |
| model viết một con số thời tiết không có ở công cụ, ở tài liệu, hay trong câu người dùng hỏi | xoá câu có con số đó; không còn gì đứng được thì trả câu từ chối | câu trả lời thiếu câu đó | đã có cho thời tiết; số khoảng cách chỉ được kiểm ở lượt có gọi công cụ khoảng cách (bài 24) |
| cùng một câu hỏi được hỏi hai lần | model có thể viết hai câu trả lời khác chữ | hai câu trả lời khác chữ, cùng nội dung | bình thường; riêng câu mở đầu một cuộc mới trùng một câu đã trả lời trong 24 giờ thì được trả lại đúng câu đã nhớ (bài 34) |
| đổi sang một model viết khác | mọi điều trong bài này vẫn đúng với model mới; các con số đo thì phải đo lại | — | đã đổi một lần (bài 33) |

## Dễ nhầm

- **"Model biết mọi thứ trên Internet."** Không. Nó chỉ có những gì đã đọc lúc huấn luyện, dừng ở một mốc thời gian, và nhớ không chính xác.
- **"Model trả lời chắc chắn thì là đúng."** Không. Giọng chắc chắn là cách nó viết, không phải dấu hiệu của sự đúng.
- **"Model học dần từ người dùng của mình."** Không. Model không đổi sau mỗi lượt hỏi; muốn nó "biết" điều gì thì phải gửi điều đó trong lần gọi.

## Câu hỏi tự kiểm

Thử trả lời bằng lời của mình trước khi bấm mở đáp án.

<details>
<summary>1. Model ngôn ngữ sai theo những kiểu nào, và hue_rag đối lại mỗi kiểu bằng gì?</summary>

Kiến thức cũ và không biết dữ liệu riêng: đưa tài liệu của kho cho model đọc. Viết chắc điều không có: dặn chỉ dùng tài liệu, bắt ghi nguồn, chương trình kiểm số nguồn, không đủ thì từ chối. Tính toán sai: chương trình tính, model chỉ diễn đạt.

</details>

<details>
<summary>2. Vì sao chỉ gửi 10 đoạn cho model, không gửi nhiều hơn?</summary>

Đã đo: 5 đoạn kém hơn; 15 đoạn, cả mục, cả bài đều không hơn, và đưa cả bài đắt gấp 5,5 lần. Cái giá: đoạn có đáp án không lọt vào 10 đoạn thì model không thấy.

</details>

<details>
<summary>3. Model không nhớ gì giữa hai lần gọi. Vậy vì sao trợ lý hiểu được câu hỏi nối tiếp?</summary>

Vì chương trình gửi lại trong mỗi lần gọi: câu hỏi của ba lượt gần nhất và câu trả lời của lượt liền trước. Model không tự giữ gì và không học thêm gì từ người dùng.

</details>

## Chi tiết để tra

- Ví dụ chính là lượt hỏi ngày 21/11/2026 với Claude Sonnet 5.5: 5.085 token vào, 425 token ra, 0,0144 USD cho lần gọi viết (tính 25.000 đồng một USD: khoảng 360 đồng). Giá dùng để tính: 2 USD cho 1 triệu token vào, 10 USD cho 1 triệu token ra; đây là giá ghi trong chương trình, chưa đối chiếu với hoá đơn. Cả lượt hỏi tốn 0,0178 USD vì còn lần gọi xếp loại câu.
- Với gpt-6-luna giá thấp hơn khoảng 20 lần: 0,10 USD và 0,50 USD cho 1 triệu token vào và ra.
- Ở lượt đo cả hệ thống ngày 12/11 (gpt-6-luna), bản có trợ lý cho câu trả lời dùng được ở 27 trên 28 câu có yếu tố ngày, so với 11 trên 28 ở bản hỏi đáp trước đó. Mức chênh này là của cả trợ lý, không riêng của việc tính ngày.
- Model mạnh hơn vẫn tính sai: trong một lượt rà ngày 21/11, cả hai model viết đều tính sai một phép tính tuổi theo năm khi phải tự tính.
- Mức nhiễu giữa hai lần chạy không đổi gì, đo ngày 19/11 trên bộ 176 câu mẫu với gpt-6-luna: số câu được chấm "đúng" lệch 1, "đủ ý" lệch 2, "trọng tâm" lệch 7 (bài 19).

**Bài sau (bài 2):** cách xử lý hai kiểu sai đầu tiên: cho model đọc tài liệu của mình trước khi trả lời. Cách đó tên là RAG.

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Phần giải thích chung về model ngôn ngữ, token, mốc kiến thức, việc model không nhớ giữa hai lần gọi: kiến thức phổ thông, không phải số đo của dự án.
- Ví dụ chính (5.085 / 425 token, 0,01442 USD): `data/hoc_cung_D/vi_du_di_suot_vet.json` [đã chạy]. Bảng giá: `backend/llm/pricing.py`.
- Hai model viết, đổi tạm từ 21/11: `backend/config/settings.yaml` mục `full_corpus_generation`; `session_prompt/HIEN_TRANG.md` mục 1.
- 27 / 28 so với 11 / 28 câu theo ngày (12/11, cả trợ lý so với bản hỏi đáp): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 37. Bớt 9 câu từ chối nhầm, 0 sai ngày khi chương trình tính ngày: cùng bài, hàng số 23. Ba lượt gần nhất, cắt 4.000 ký tự: `backend/api/conversations.py`.
- Cả hai model tính sai năm khi tự tính: `data/thu_bedrock_2026-11-21/c_harness/RA_HARNESS.md` mục (2) [riêng tư, 21/11].
- Lịch sử gửi kèm (câu hỏi các lượt trước, câu trả lời lượt liền trước): `backend/config/settings.yaml` (`nho_hoi_thoai`, `nho_cau_tra_loi`).
- Mức nhiễu 1 / 2 / 7: `session_prompt/HIEN_TRANG.md` mục 2 (dòng "Số nhiễu").
- Mục "Quyết định và lý do" và "Nếu… thì sao" (đã sửa theo biên bản `data/hoc_cung_D/kiem/bai_22_va_muc_moi_01_03_04.md`): 5 / 10 / 15 đoạn, cả mục, cả bài (đắt 5,5 lần): `bai_hoc/19_BANG_TONG_CAC_LAN_SO_SANH.md` hàng số 10, `bai_hoc/VIEC_MOI_XONG.md` mục 14; thêm 2 đoạn mỗi ý: `backend/config/settings.yaml` (`tim_theo_ve`); chương trình tính tổng tiền (8 / 8; 3 / 3): bảng tổng hàng số 20; kiểm con số và điều kiện của nó: `backend/llm/assistant.py` (`kiem_so_sau_khi_viet`); câu đã nhớ 24 giờ: `backend/api/cache_tra_loi.py`; tra web khi kho từ chối: `settings.yaml` (`tra_web`). "Gửi cả kho quá sức một lần gọi" là lập luận, ghi rõ trong bài.

- Cập nhật theo bộ thay đổi mở 14:47 22/11/2026: `bai_hoc/VIEC_MOI_XONG.md` mục 42, 43; `guides/RUNBOOK_BAN_GIAO.md` mục 10.1; `backend/config/settings.yaml` (`so_lan_tim_kho: 3`) [code; người viết không chạy lại].

</details>
