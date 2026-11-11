# Bài 10 — Chấm bước tìm

*Cập nhật lần cuối: 10:24, ngày 11/11/2026 · bài mới.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Thứ hạng trung bình | **MRR** (trong code: `keyword_mrr`) | Đoạn chứa từ khoá đáp án đứng hạng 1 được 1, hạng 2 được 1/2… rồi lấy trung bình (đã gặp ở bài 6). |
| Điểm xếp hạng có trọng số — **mới** | **nDCG** | Giống MRR nhưng tính cả nhiều đoạn đúng; đoạn đúng càng cao càng được nhiều điểm. 1 = hoàn hảo. |
| Tỉ lệ từ khoá tìm thấy — **mới** | **Keyword Coverage** | Trong các từ khoá đáp án của một câu, bao nhiêu phần có mặt trong 10 đoạn. |
| Nhãn đoạn đúng — **mới** | **gold label** (`gold_v5.jsonl`) | Người (agent) đánh dấu chính xác câu chữ nào trong kho là đáp án. |
| Dấu kết quả tìm — **mới** | **mốc T1** (fingerprint) | Một chuỗi ký tự tính từ toàn bộ kết quả tìm của 158 câu; đổi một đoạn là dấu đổi. |
| Mức tối thiểu | **sàn** (floor) | Mức ghi **trước** khi thử; không đạt thì không nhận (đã gặp ở bài 2). |

---

*Bài 9 kể về đề: 176 câu có đáp án mẫu. Bài này kể nửa đầu của việc chấm: chưa cần nhìn câu trả lời, chỉ xem **10 đoạn đưa người viết có chứa đáp án không**.*

## Quay lại người hướng dẫn viên

Khi người hướng dẫn viên trả lời sai, có hai khả năng rất khác nhau:
- họ **rút nhầm thẻ**: thẻ có đáp án vẫn nằm trong hộp, nhưng họ không rút ra;
- họ **rút đúng thẻ mà đọc sai** hoặc nói thiếu.

Muốn sửa đúng chỗ, phải biết là lỗi nào. Vì vậy trước khi nghe họ nói, mình **xem trước 10 thẻ họ rút ra**: thẻ có đáp án có trong đó không? Nằm ở thẻ thứ
mấy? Đây là chấm **bước tìm**, nửa đầu của cách đánh giá hai giai đoạn anh đã học. Bài 11 kể nửa sau: chấm lời họ nói.

## Thước thứ nhất: từ khoá đáp án (nhanh, chạy trên cả bộ)

Mỗi câu trong đề có vài **từ khoá đáp án** (bài 9). Với mỗi từ khoá, máy xem đoạn đầu tiên chứa từ khoá đó đứng hạng mấy trong 10 đoạn, so khớp không phân
biệt hoa thường, đã chuẩn hoá dấu. Từ đó ra ba số:
- **MRR**: trung bình của 1/hạng;
- **nDCG**: tương tự nhưng tính cả việc nhiều đoạn đúng cùng đứng cao;
- **tỉ lệ từ khoá tìm thấy** trong 10 đoạn.

Số hiện nay trên 158 câu có đáp án trong kho (kho sau sửa 05/11):

| Số | Giá trị | Nghĩa là |
|---|---|---|
| MRR | **0,72** | đoạn chứa từ khoá đáp án trung bình đứng khoảng hạng 1–2 |
| nDCG | **0,76** | xếp hạng tốt nhưng chưa hoàn hảo |
| Tỉ lệ từ khoá tìm thấy | khoảng **92 %** (đo trên kho cũ) | trung bình mỗi câu, gần hết từ khoá đáp án có mặt trong 10 đoạn |
| MRR theo loại: một dữ kiện / nhiều nguồn / so sánh | **0,80 / 0,54 / 0,53** | câu cần ghép nhiều chỗ thì kém rõ |

Mốc so sánh: ở bản chatbot đầu tiên (trên kho cũ), ba số này là 0,72 / 0,755 / 92,4 %. Bước tìm gần như **không đổi** suốt Phase 8 và 9. Đó là đúng chủ đích:
mọi thử nghiệm đổi bước tìm đều không qua được sàn (bài 4, 6, 7), nên bước tìm được giữ nguyên.

Điểm mạnh của thước này: rẻ, chạy trên cả 158 câu, không cần người. Điểm yếu: **chỉ là thước gần đúng**. Đoạn chứa từ khoá chưa chắc đủ ý. Đoạn nói đúng đáp án
bằng chữ khác thì bị tính là trượt.

## Thước thứ hai: nhãn đoạn đúng (chính xác, chỉ có trên 55 câu)

Với 55 câu khó (40 thử, 15 kiểm), agent đọc kho và **đánh dấu chính xác câu chữ nào là đáp án** cho từng ý của đáp án mẫu. Một agent khác kiểm chéo, và anh
duyệt khoảng 10 câu. Đó là nhãn đoạn đúng.

Cách chấm:
- một ý "có trong ngữ cảnh" khi ít nhất một chỗ được đánh dấu cho ý đó nằm trong các đoạn được đưa;
- câu "đủ" khi **mọi ý** của câu đều có;
- đo ở **ba tầng**: trong 30 ứng viên → trong 10 đoạn → trong phần thật sự đưa người viết.

Kết quả hiện nay (nhãn bản 5, kho sau sửa 30/10):

| Tầng | Câu có đủ đoạn đúng (40 câu thử) | Nghĩa là |
|---|---:|---|
| Trong 30 ứng viên | **33** | tìm theo nghĩa đã lấy về được phần lớn |
| Trong 10 đoạn đưa người viết | **24** | 9 câu rơi mất ở bước xếp hạng |

Tính trên cả 55 câu: 33 câu đủ; trung bình 76 % số ý có trong ngữ cảnh. Kết luận của thước này giống bài 6: **chỗ nghẽn là xếp hạng**.

**Nhãn phải làm lại khi kho đổi.** Sửa kho làm đổi câu chữ, nên chỗ đánh dấu cũ có thể không còn khớp. Nhãn đã qua 5 bản: mỗi lần kho đổi, hoặc mỗi lần sửa
cách đếm, là một bản mới. Mọi con số luôn ghi kèm bản nhãn. Số chấm bằng bản nhãn khác nhau thì không so thẳng với nhau.

**Sàn khi thử nghiệm:** mọi thử nghiệm đổi bước tìm hay cắt đoạn (bài 2, 3, 4, 6, 7) đều dùng chung một luật ghi trước: **0 câu mất đoạn đúng** trên thước
này. Đây là luật đã loại Qwen3-8B (mất 3 câu thử + 3 câu kiểm), lấy 100 ứng viên (mất 1 câu), và các model xếp lại.

## Dấu kết quả tìm: chứng minh "không đổi gì"

Nhiều thay đổi về sau không định đụng tới bước tìm, ví dụ sửa lời dặn hay thêm công cụ. Làm sao chắc là chúng thật sự không đụng? Máy chạy tìm cho 158 câu,
ghi lại toàn bộ 10 đoạn của mỗi câu theo đúng thứ tự, rồi tính **một dấu** cho tất cả. Đổi dù chỉ một đoạn ở một câu thì dấu đổi. Trước và sau mỗi thay đổi,
nếu dấu **giống hệt** thì bước tìm chắc chắn không đổi. Khi đó không cần chấm lại bước tìm.

Dấu đổi khi kho đổi. Lần gần nhất là 05/11, sau khi thêm giờ mở cửa cho 11 bài.

## Một chuyện thật: thước nhanh chẩn đoán sai

Hồi đầu (bản đầu tiên, đưa 5 đoạn), có 22 câu bị từ chối nhầm. Nhìn theo thước từ khoá, có **4 câu trông như đã đủ từ khoá trong ngữ cảnh mà người viết vẫn từ
chối**. Chẩn đoán lúc đó: "người viết quá rụt rè". Hướng sửa tự nhiên sẽ là dặn người viết bớt rụt rè. Nhưng làm vậy rất nguy hiểm, vì dễ làm nó trả lời cả câu
ngoài kho.

Ngày 25/10, có nhãn đoạn đúng, chấm lại 22 câu đó bằng thước chính xác: **cả 22 câu đều thiếu đoạn đúng trong ngữ cảnh**. 4 câu "đủ từ khoá" thật ra chỉ
trùng chữ, chứ đoạn đó không chứa đáp án. Người viết **không rụt rè**: nó từ chối đúng, vì nó thật sự không được đưa đáp án.

Nhờ chẩn đoán lại, hướng sửa đổi hẳn: không dặn người viết bớt rụt rè, mà **cho nó thấy nhiều chỗ hơn** (10 đoạn, bài 6) và **cho tìm thêm** (bài 13). Cả hai
đều giảm từ chối nhầm mà không làm câu ngoài kho bị trả lời.

Bài học: **thước rẻ dùng để theo dõi, thước chính xác dùng để chẩn đoán**. Chẩn đoán sai thì sửa sai chỗ.

## Khi nào hỏng (giới hạn của thước)

- **Thước từ khoá gần đúng:** đoạn diễn đạt khác chữ bị tính trượt; đoạn trùng chữ mà không chứa đáp án bị tính trúng.
- **Thước đoạn đúng nhỏ:** chỉ 55 câu (40 thử), nên nhiều thí nghiệm chỉ ra được "chưa rõ". Mỗi ý chỉ đánh dấu một chỗ, nên nếu kho có đáp án ở hai chỗ thì chỗ
  thứ hai không được tính.
- **Cả hai thước chỉ nhìn bước tìm.** Đủ đoạn đúng chưa chắc trả lời tốt, vì người viết vẫn có thể đọc thiếu. Phần đó là bài 11.

## Ba điều chính

1. Chấm bước tìm bằng **hai thước**: **từ khoá đáp án** (rẻ, cả 158 câu: MRR 0,72) và **nhãn đoạn đúng** (chính xác, 55 câu: 33 / 40 câu có đáp án trong 30 ứng
   viên nhưng chỉ 24 trong 10 đoạn).
2. Luật chung cho mọi thử nghiệm bước tìm: **0 câu mất đoạn đúng**. Một **dấu kết quả tìm** chứng minh khi nào bước tìm không đổi.
3. Thước rẻ từng **chẩn đoán sai** ("người viết rụt rè"). Thước chính xác cho thấy lỗi nằm ở **bước tìm**, nên sửa bằng 10 đoạn và tìm thêm.

**Bài sau:** Bài 11 — Chấm câu trả lời: ai chấm, chấm theo ba tiêu chí nào, so hai bản thế nào cho công bằng, và mỗi con số tốt tới đâu.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- MRR theo từ khoá, so khớp không phân biệt hoa thường + NFC: `backend/evaluation/full_corpus_eval.py` (`keyword_mrr`, `score_retrieval`, `_fold`) [code, xem 11/11]
- MRR 0,7216 / nDCG 0,7554 (kho 05/11); mốc bản đầu 0,72 / 0,755 / 92,4 %; theo loại 0,80 / 0,543 / 0,527: `bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md`, `10_BAO_CAO_DANH_GIA.md` [đã chạy]. "92 %" là tỉ lệ từ khoá trung bình theo câu, không phải tỉ lệ câu (suy ra từ code).
- Nhãn đoạn đúng 55 câu (40 / 15), cách chấm 3 tầng: `backend/experiments/phase_8_1/g1_retrieval.py` (`chunk_hits_quote`, `gold_coverage`, `GOLD_PATH` = bản 5) [code]; 24 / 40 và 33 / 40; 33 / 55; 0,76: `06_BAO_CAO_TIM_KIEM.md` [đã chạy]
- Agent gắn, agent khác kiểm, anh duyệt khoảng 10 câu: `session_prompt/Project_Status.md` §5 (24/10) [quyết định]
- Dấu kết quả tìm 158 câu `64656a87c109` (05/11): `session_prompt/Project_Status.md` §4 [đã chạy]
- 22 / 22 câu từ chối nhầm thiếu đoạn đúng; chẩn đoán cũ "4 câu đủ mà vẫn từ chối" sai (25/10, Phase 8.1 G1.6): `10_BAO_CAO_DANH_GIA.md`, `06_BAO_CAO_TIM_KIEM.md` [đã chạy]

</details>
