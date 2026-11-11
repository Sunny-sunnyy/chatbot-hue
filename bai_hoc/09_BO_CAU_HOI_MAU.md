# Bài 9 — Đề kiểm tra: bộ câu hỏi mẫu

*Cập nhật lần cuối: 10:24, ngày 11/11/2026 · bài mới; mở đầu Phần 2 (đánh giá).*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Bộ câu hỏi mẫu | **Golden set** (`golden_full_corpus.jsonl`) | 176 câu hỏi có đáp án mẫu, dùng để chấm (đã gặp ở bài 0). |
| Đáp án mẫu — **mới** | **reference_answer** | Câu trả lời đúng do người soạn viết sẵn, để so với câu chatbot viết. |
| Từ khoá đáp án | **keywords** | Vài chữ phải có trong đoạn tìm được nếu đoạn đó chứa đáp án (dùng ở bài 10). |
| Loại câu — **mới** | **category**: `direct_fact`, `multi_source`, `conditional`, `comparative`, `out_of_scope` | Một dữ kiện · nhiều nguồn · có điều kiện · so sánh · ngoài kho. |
| Nhóm thử / nhóm kiểm — **mới** | **dev / test split** (`split.json`, 120 / 56) | Nhóm để thử và chỉnh; nhóm riêng chỉ để kiểm lại kết quả, không chỉnh theo. |
| Bộ câu kín — **mới** | **sealed set** | Bộ câu người sửa chatbot **không được xem**, chỉ mở một lần để kiểm cuối. |
| Mức đồng ý — **mới** | **Cohen's kappa** | Hai người gắn nhãn đồng ý tới đâu, sau khi trừ phần trùng do may. 1 = đồng ý hoàn toàn, 0 = như đoán bừa. |

---

*Phần 1 (bài 0–8) kể chatbot chạy thế nào. Phần 2 kể làm sao biết nó **tốt tới đâu**, theo đúng hai giai đoạn đánh giá anh đã học. Trước khi chấm được thì
phải có đề. Bài này kể về đề.*

## Quay lại người hướng dẫn viên

Muốn biết người hướng dẫn viên giỏi tới đâu, không thể chỉ hỏi họ "anh có giỏi không". Phải **ra đề**: một xấp câu hỏi khách hay hỏi, mỗi câu kèm đáp án đúng
viết sẵn. Hỏi họ từng câu, rồi so câu họ nói với đáp án.

Đề tốt phải có vài tính chất:
- **câu giống câu khách thật hay hỏi**, không phải câu đánh đố;
- **đủ loại câu**: câu hỏi một chuyện, câu phải ghép nhiều trang, câu có điều kiện, câu so sánh, và cả câu **sổ không có** (để xem họ có dám nói "không biết");
- **có phần đề giấu kín**: nếu luyện mãi trên một đề thì giỏi đề đó chứ chưa chắc giỏi thật. Nên giữ riêng một phần đề người luyện không được xem.

Bộ câu hỏi mẫu của hue_rag được làm theo đúng ba tính chất đó.

## Bộ 176 câu hỏi mẫu (Golden)

Mỗi câu có đúng **4 trường**: câu hỏi · từ khoá đáp án · đáp án mẫu · loại câu. 176 câu chia theo loại:

| Loại câu | Số câu | Ví dụ kiểu câu (tự đặt) | Chatbot phải làm gì |
|---|---:|---|---|
| Một dữ kiện | 75 | "Vé vào [một di tích] bao nhiêu?" | tìm đúng một chỗ, nói đúng |
| Nhiều nguồn | 29 | "[một dịp] nên ăn những món gì?" | ghép thông tin từ nhiều bài |
| Có điều kiện | 29 | "[một nhóm khách] có được miễn vé không?" | giữ đúng điều kiện, ngoại lệ |
| So sánh | 25 | "[món A] và [món B] khác nhau thế nào?" | đặt hai thứ cạnh nhau, đủ cả hai bên |
| Ngoài kho | 18 | câu về Huế mà kho không có | trả đúng câu từ chối cố định |

*(Các ví dụ trên chỉ là khuôn kiểu câu, cố ý để trống tên, không phải câu trong bộ.)*

Bộ được soạn từ kho: câu do AI viết, có người duyệt. Ngoài ra có:
- **bộ 10 câu chạy nhanh** (smoke), lấy từ 176 câu, để kiểm nhanh sau mỗi thay đổi nhỏ;
- **nhóm thử 120 câu / nhóm kiểm 56 câu**, chia sao cho mỗi loại câu có tỉ lệ như nhau ở hai nhóm, và chia cố định (chạy lại vẫn ra cùng cách chia). Khi thử
  một cách mới, mình chỉnh và quyết trên nhóm thử. Nhóm kiểm chỉ dùng để **xác nhận lại**, không chỉnh theo nó. Nhờ vậy kết quả không bị "học tủ".

## Vì sao câu phải giống câu người thật hay hỏi

Ngày 24/10, hai agent **độc lập** đọc từng câu trong 176 câu và gắn nhãn: câu này có giống câu khách thật hay hỏi không.

| Nhãn | Số câu | Nghĩa là |
|---|---:|---|
| tự nhiên | 82 | khách thật hay hỏi đúng kiểu này |
| chỉ để đo năng lực | 65 | không hẳn tự nhiên, nhưng đo được một năng lực cần (ví dụ ghép nhiều nguồn) |
| không tự nhiên | 29 | không ai hỏi như vậy (ví dụ câu ghép gượng ép để đánh đố) |

Mức đồng ý giữa hai agent (kappa) là **0,765**. Nghĩa là: hai bên đồng ý khá cao, vượt xa mức đoán bừa, nên nhãn đáng tin. 9 câu hai bên không đồng ý thì anh
quyết, và anh giữ cả 9 là tự nhiên.

Từ đó có luật: **số chính của mọi lần chấm bỏ 29 câu không tự nhiên**. Còn lại 147 câu, trong đó **129 câu có đáp án trong kho** (bỏ 18 câu ngoài kho). Đây là
lý do các điểm ở bài 0 ghi "khoảng 130 câu". Lý do của luật: đồ án được đánh giá như một sản phẩm thật, nên thước đo phải sát với **người dùng thật hỏi gì**. Một
chatbot giỏi trả lời câu đánh đố mà kém câu thường thì không có giá trị.

## Bộ câu kín

Bộ câu kín là phần đề giấu kín. Agent sửa chatbot **không được đọc** các câu này. Chỉ đúng một người chạy, đúng một lần, ở mốc kiểm cuối, và chỉ báo ra số đếm.
Đã có hai bộ:
- **36 câu** (khoá 25/10), dùng một lần ngày 28/10 để kiểm cuối Phase 8.2. Từ đó chỉ còn dùng để kiểm hồi quy;
- **40 câu** viết theo kiểu người thật hỏi (01/11), dùng một lần ở lượt đo cuối Phase 8.

Hiện **không còn bộ nào "chưa ai thấy"**. Luật mới (05/11) chỉ dùng bộ kín cho những thay đổi **chỉnh lời dặn model qua nhiều vòng**, vì đó là chỗ dễ "học tủ"
nhất. Thay đổi mà code tính, kiểm tất định thì không cần bộ kín.

## Bộ 32 câu an toàn

Một bộ riêng cho **loại lỗi tệ nhất**: sai về vé, giờ, quy định, cảnh báo an toàn. Gồm 28 câu trong kho và 4 câu ngoài kho. Mỗi lần chấm luôn báo đủ **4 số**:

| Số | Lượt đo cuối Phase 8 (01/11) | Mức cho phép | Nghĩa là |
|---|---|---|---|
| Câu đảo ngược cảnh báo (vd kho nói "không được", chatbot nói "được") | **0** | 0 | đạt |
| Câu ngoài kho bị trả lời | **0 / 4** | 0 | đạt |
| Câu nói sai điều kiện, kiểu lỗi mới (vd ghi sai giờ) | **2** | tối đa 2 | đạt sát mức; bản trước sinh lại cũng sai y 2 câu đó |
| Câu tự thêm chi tiết không có trong kho | 2 | chỉ theo dõi | không chặn, nhưng ghi lại |

Bộ này còn có **15 câu đối chứng** để kiểm chính người chấm: 10 câu trả lời cố tình chèn sai, 5 câu chép đúng. Người chấm phải bắt đủ 10 câu sai và không bắt
nhầm 5 câu đúng. Nếu không, kết quả chấm của lượt đó không được dùng.

## Đề cũng phải sửa

Đáp án mẫu không phải lúc nào cũng đúng. Hai lần sửa:
- **25/10:** sửa 10 đáp án theo nguyên tắc "chỉ trả lời điều được hỏi". Đáp án cũ có câu dài dòng, chấm câu trả lời ngắn mà đúng thành "thiếu ý".
- **30/10:** sửa 2 đáp án cho khớp kho sau đợt sửa kho thứ hai. Anh duyệt từng câu.

Mỗi bản bộ câu có một dấu (md5) để biết đang chấm bằng bản nào. Số cũ chấm bằng bản cũ thì không so thẳng với số mới.

## Một chuyện thật: đề quen thì điểm cao hơn thực lực

Ở lượt đo cuối Phase 8 (01/11), chatbot được chấm trên cả bộ 176 câu quen và bộ kín 40 câu mới. Điểm "đủ ý":

| | Bộ quen (Golden) | Bộ kín (40 câu) |
|---|---:|---:|
| Đủ ý, mọi câu | 4,58 | **4,18** |
| Đủ ý, chỉ câu được trả lời | 4,82 | 4,60 |
| Câu một dữ kiện, đủ ý | 4,97 | **4,42** |

Đọc bảng:
- Điểm trên bộ quen **lạc quan hơn thực lực**. Trên câu chưa ai thấy, điểm thấp hơn khoảng 0,4.
- Chênh lệch **không chỉ do từ chối nhầm**: tính riêng câu được trả lời vẫn thấp hơn. Rõ nhất ở câu một dữ kiện (4,97 xuống 4,42), dù không câu nào bị từ chối và
  điểm "đúng" vẫn 5,00. Tức là chatbot **trả lời đúng nhưng thiếu ý**.
- Tính lại theo đúng tỉ lệ loại câu của bộ quen vẫn ra khoảng 4,20. Nên không phải do bộ kín toàn câu khó.
- 40 câu là mẫu nhỏ, nên con số còn dao động. Nhưng hướng thì rõ.

Bài học: **đề quen cho số đẹp, đề kín cho số thật**. Khi kể kết quả, nên kể cả hai.

## Khi nào hỏng (giới hạn của đề)

- **Chưa có câu nào do người dùng thật hỏi.** Mọi câu do AI soạn, kể cả bộ "viết kiểu người thật". Khi có người dùng thật, đây là việc đầu tiên nên bổ sung.
- **Bộ quen đã dễ.** 121 / 176 câu đã đạt điểm tối đa ngay từ bản chatbot đầu tiên, nên bộ này khó thấy được cải tiến nhỏ.
- **Giá vé, giờ mở cửa trong đáp án lấy theo mốc 09/2026.** Ngoài đời đổi thì đáp án cũ dần.
- **Câu không dấu nằm ngoài đề** (anh chốt 25/10).

## Ba điều chính

1. Đề có **176 câu, 5 loại** (một dữ kiện, nhiều nguồn, có điều kiện, so sánh, ngoài kho), chia **120 thử / 56 kiểm**. Số chính **bỏ 29 câu không tự nhiên**,
   vì thước đo phải sát người dùng thật.
2. Có **bộ câu kín** (người sửa không được xem) và **bộ 32 câu an toàn** luôn báo đủ 4 số, kèm câu đối chứng để kiểm cả người chấm.
3. **Đề quen cho số đẹp hơn thực lực**: trên bộ kín, điểm đủ ý thấp hơn khoảng 0,4, kể cả khi chatbot không từ chối.

**Bài sau:** Bài 10 — Chấm bước tìm: đo xem 10 đoạn đưa người viết có chứa đáp án không, bằng hai thước, và vì sao thước nhanh đôi khi chẩn đoán sai.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- 4 trường, 5 loại câu (75 / 29 / 29 / 25 / 18), smoke 10: `backend/evaluation/golden_full_corpus.py` (`OFFICIAL_FIELDS`, `CATEGORIES`, `SMOKE_SIZE`) [code, xem 11/11]; số câu theo loại: `bao_cao_he_thong/09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` [tài liệu]
- Chia 120 / 56 theo loại câu, cố định: `backend/evaluation/full_corpus_eval.py` `make_split`; `knowledge-base-hue/evaluation/phase_8_1/split.json` (riêng tư) [code]
- Nhãn tự nhiên 82 / 65 / 29, kappa 0,765, 9 câu User quyết: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` (24/10); luật bỏ câu không tự nhiên: `session_prompt/Project_Status.md` §5 (24/10 21:58) [đã chạy + quyết định của anh]
- Bộ kín 36 / 40 câu, đã dùng; luật dùng bộ kín (05/11): `09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` §1, `session_prompt/Session_Prompt.md` §7 [tài liệu]
- Bộ an toàn 32 câu, 4 số lượt 01/11, 15 câu đối chứng: `report_agent/2026-10-31_streaming_spec/do_cuoi_b_an_toan_ngay.md` [đã chạy]
- Sửa đáp án 25/10 (10 câu) và 30/10 (2 câu); md5 hiện tại `6331e88fb171`: `session_prompt/Project_Status.md` §4 [đã chạy]
- Bộ quen ↔ bộ kín (01/11): `report_agent/2026-10-31_streaming_spec/do_cuoi_b_bo_kin.md`, `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` [đã chạy]
- 121 / 176 câu đạt tối đa từ bản đầu: `09_BAO_CAO_BO_CAU_HOI_GOLDEN.md` [đã chạy]
- Mọi ví dụ câu trong bài là câu tự đặt, không lấy từ bộ.

</details>
