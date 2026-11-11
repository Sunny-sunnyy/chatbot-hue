# Bài 11 — Chấm câu trả lời, và mỗi con số tốt tới đâu

*Cập nhật lần cuối: 10:27, ngày 11/11/2026 · bài mới; bài dài hơn vì gom mọi con số chính của đồ án.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước hoặc anh đã biết từ khoá học.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Người chấm — **mới** | **LLM-as-judge** (Claude; đề chấm: `full_corpus_judge_prompt.md`) | Một model khác đọc câu hỏi, đáp án mẫu, câu trả lời rồi cho điểm. |
| Ba tiêu chí | **Accuracy / Completeness / Relevance** | Đúng · Đủ ý · Trúng ý, mỗi tiêu chí 1–5 điểm. |
| Chấm mù — **mới** | **blind pooled judging** | Trộn câu trả lời của mọi bản, che tên bản rồi mới đưa người chấm. |
| So theo cặp — **mới** | **paired comparison** + **bootstrap** + **Holm** | So cùng một câu giữa hai bản; tính khoảng tin cậy; hiệu chỉnh khi thử nhiều bản cùng lúc. |
| Dao động tự nhiên — **mới** | **nhiễu A/A** | Chạy **cùng một bản** hai lần, đếm xem bao nhiêu câu tự đổi điểm. |
| Luật không làm hỏng | **non-inferiority** | Bản mới không được tụt quá dao động tự nhiên. |
| Yêu cầu phi chức năng | **non-functional requirements** | Tốc độ, tiền: p50 ≤ 3 s, p95 ≤ 5 s tới chữ đầu; ≤ 0,0005 USD / câu. |

---

*Bài 10 chấm bước tìm. Bài này chấm nửa sau: **lời người viết nói ra**. Cuối bài gom mọi con số chính của đồ án, mỗi số kèm mốc so sánh, để anh nói được nó tốt
tới đâu.*

## Quay lại người hướng dẫn viên

Giờ mình nghe người hướng dẫn viên trả lời từng câu trong đề, rồi so với đáp án mẫu. Hỏi ba điều:
- **Đúng không?** Có câu nào nói ngược đáp án không.
- **Đủ không?** Đáp án có ba ý mà họ chỉ nói hai thì thiếu.
- **Trúng không?** Có trả lời thẳng điều khách hỏi không, hay lan man.

Muốn so **hai người hướng dẫn viên** (hay hai bản chatbot) cho công bằng, còn phải cẩn thận thêm:
- người chấm **không được biết** câu nào của ai, để khỏi thiên vị;
- so **cùng một câu** giữa hai người, chứ không so trung bình chung chung;
- biết trước **một người tự dao động bao nhiêu** khi trả lời lại cùng câu, để không nhầm dao động là tiến bộ.

## Ai chấm, chấm thế nào

**Người chấm là Claude**, theo một đề chấm cố định. Mỗi lượt Claude nhận đúng ba phần: câu hỏi, đáp án mẫu, câu trả lời. Claude cho ba điểm nguyên từ 1 tới 5:

| Tiêu chí | 5 điểm nghĩa là | Bị trừ khi |
|---|---|---|
| **Đúng** | không có gì trái với đáp án mẫu | nói ngược, sai số, sai tên |
| **Đủ ý** | có đủ các ý cần của đáp án mẫu | thiếu ý |
| **Trúng ý** | trả lời thẳng điều được hỏi | lan man, thêm thứ không cần |

Vài luật quan trọng trong đề chấm:
- chỉ dựa vào ba phần được đưa, **không dùng kiến thức ngoài**;
- chi tiết thêm mà đáp án không xác nhận cũng không phủ nhận thì **không tự bị trừ "đúng"**, chỉ trừ "trúng ý" nếu làm câu trả lời lan man;
- **không chấm ghi nguồn** (đã có code kiểm, bài 8);
- đáp án mẫu là câu từ chối thì chatbot từ chối là đúng, còn trả lời như thể biết là sai;
- đáp án có nội dung mà chatbot từ chối thì câu trả lời **không có gì để chấm**, nên điểm rất thấp. Đây là lý do từ chối nhầm kéo điểm trung bình xuống.

**Chấm mù:** câu trả lời của mọi bản được trộn vào một xấp, che tên bản, xáo thứ tự. Câu giống hệt nhau giữa hai bản chỉ chấm một lần. Người chấm không biết
câu nào của bản cũ hay bản mới.

## So hai bản thế nào cho công bằng

**So theo cặp.** Với mỗi câu, lấy điểm bản mới trừ điểm bản cũ. Rồi xem phân bố của các hiệu đó: trung bình bao nhiêu, bao nhiêu câu tốt lên, bao nhiêu câu tụt.

**Khoảng tin cậy.** Máy rút ngẫu nhiên lại các câu 10.000 lần để xem trung bình hiệu dao động trong khoảng nào (gọi là bootstrap). Ra một khoảng, ví dụ
[+0,08; +0,48]. **Khoảng không chứa 0** thì chênh lệch là thật. **Khoảng chứa 0** thì chưa nói được là khác.

**Thử nhiều bản cùng lúc thì khắt khe hơn.** Thử 5 bản thì dễ có 1 bản "trông như thắng" chỉ do may. Nên khi thử nhiều bản, ngưỡng được nâng lên (cách hiệu
chỉnh Holm).

**Dao động tự nhiên (nhiễu A/A).** Chạy **cùng một bản** hai lần, chấm hai lần. Trên 176 câu ở cấu hình 10 đoạn: chỉ **1–2 câu** tự tụt điểm. Riêng người chấm
chấm lại cùng câu trả lời thì đổi khoảng 2 / 88 câu. Sinh lại câu trả lời rồi chấm lại thì khoảng 10 / 83 câu đổi điểm "đủ ý", vì model viết hơi khác mỗi lần.

Từ đó có **luật "không làm hỏng"**, dùng cho mọi thay đổi không nhằm tăng điểm (sửa kho, thêm tính năng, tối ưu tốc độ):
- điểm trung bình không tụt quá **0,1**;
- **số câu tụt không vượt dao động tự nhiên + 3**.

Còn thay đổi nhằm **tăng điểm** thì phải tăng **vượt dao động**, có khoảng tin cậy không chứa 0, và xác nhận lại trên nhóm kiểm.

## Các mức tối thiểu và thứ tự lỗi

Ngoài điểm, có những **mức tối thiểu** (sàn) mà không thay đổi nào được phạm:
- **0 câu ngoài kho bị trả lời** từ kho;
- 0 lỗi kỹ thuật, 0 lỗi ghi nguồn;
- 0 câu "nói chắc mà sai" mới (câu có điểm "đúng" ≤ 3 mà người dùng thấy);
- bộ an toàn 32 câu: 0 câu đảo cảnh báo, tối đa 2 câu sai điều kiện (bài 9).

Khi phải đánh đổi, lỗi được xếp theo mức tệ (anh chốt 28/10):

**sai cảnh báo an toàn > nói chắc mà sai > trả lời câu ngoài kho > thiếu ý > từ chối nhầm.**

Nghĩa là: thà từ chối nhầm còn hơn thiếu ý; thà thiếu ý còn hơn nói chắc mà sai. Đây là lý do nhiều thử nghiệm giảm được từ chối nhầm vẫn bị bỏ: chúng làm câu
ngoài kho bị trả lời, tức lỗi nặng hơn.

## Mọi con số chính, mỗi số tốt tới đâu

| Số | Giá trị | Mốc so sánh | Tốt tới đâu |
|---|---|---|---|
| Điểm **Đúng** (129 câu, 01/11) | **4,71** | bản đầu tiên 4,43 (đáp án mẫu khác một chút, chỉ để tham khảo) | cao; chỉ tính câu được trả lời thì **4,96**, nghĩa là khi đã trả lời thì gần như không sai |
| Điểm **Đủ ý** | **4,58** | bản đầu 4,28; chỉ tính câu được trả lời 4,82 | tốt; phần mất chủ yếu ở câu nhiều nguồn và từ chối nhầm |
| Điểm **Trúng ý** | **4,72** | bản đầu 4,45 | tốt |
| Đủ ý, **câu nhiều nguồn** | **3,50** | bản đầu 3,00; loại khác: một dữ kiện 4,91 · có điều kiện 4,68 · so sánh 4,35 | **yếu nhất**; chính là lý do làm phần trợ lý "tìm thêm" (bài 13) |
| **Từ chối nhầm** (158 câu) | **4–6** (03/11) | 22 (5 đoạn) → 12 (10 đoạn) → 4–6 (tìm thêm) | khoảng 3 %; còn là lỗi nhiều nhất, nhưng là lỗi **nhẹ nhất** theo thứ tự lỗi |
| **Câu ngoài kho bị trả lời** | **0** | sàn = 0 | đạt trên mọi bộ đã đo |
| **Bộ an toàn** (01/11) | 0 đảo cảnh báo · 0 / 4 ngoài kho · 2 sai điều kiện | sàn: 0 · 0 · tối đa 2 | đạt, nhưng sát mức ở số thứ ba |
| **Bộ kín 40 câu** (01/11), đủ ý | **4,18** | bộ quen 4,58 | thấp hơn khoảng 0,4: số trên bộ quen lạc quan (bài 9) |
| **Chữ đầu tiên**, câu về Huế (09/11) | **2,16 / 4,32 s** (trung vị / 95 %) | yêu cầu 3 / 5 s | đạt |
| Chữ đầu tiên, câu có ngày (10/11) | 2,35 / 4,56 s | yêu cầu 3 / 5 s; trước khi tối ưu 5,60 / 10,14 s | đạt sau khi tối ưu (bài 14) |
| Chữ đầu tiên, câu chào hỏi (09/11) | 3,46 / **7,73 s** | yêu cầu 3 / 5 s | **chưa đạt** ở câu chậm |
| **Tiền** một câu về Huế (09/11) | **0,00047 USD** (khoảng 12 đồng) | trần 0,0005 | đạt nhưng **sát trần** |

## Mốc người: anh tự đọc

Người chấm là Claude. Để có một mốc từ người thật, ngày 01/11 anh đọc **20 cặp câu trả lời** (bản 5 đoạn và bản 10 đoạn), không biết bên nào là bản nào. Kết quả:
phần lớn cặp như nhau; ở 3 cặp, bản 5 đoạn từ chối nhầm còn bản 10 đoạn trả lời được. Luật ghi trước cần ít nhất 5 cặp có phân thắng thua rõ mới kết luận,
thực tế 0 cặp, nên kết quả là "chưa rõ". Anh chọn **giữ 10 đoạn**. Đây là mốc tham khảo, không thay được việc chấm trên cả bộ.

## Một chuyện thật: trung bình tốt mà vẫn bị loại

Ngày 03/11, phần "nhớ câu hỏi trong cuộc trò chuyện" (bài 13) được đo vòng 1. Điểm câu hỏi tiếp theo tốt lên, nhưng **từ chối nhầm lên 7**, vượt mức cho phép 5.
Theo luật "không làm hỏng", bản đó **bị loại** dù có cải thiện. Sửa lời dặn cho hẹp lại, đo vòng 2: từ chối nhầm còn 4, qua luật, rồi mới bật.

Chuyện tương tự ở bài 7: bản để luna tự chọn đoạn tốt hơn ở trung bình nhưng có 5 câu tụt, nên cũng bị loại. Bài học: **luật ghi trước, áp đúng như đã ghi**,
kể cả khi kết quả trông hấp dẫn. Nếu nới luật sau khi thấy số, mọi phép đo đều mất giá trị.

## Khi nào hỏng (giới hạn của thước)

- **Người chấm là model.** Claude có thể chấm lệch. Đã đo dao động của người chấm, và bộ an toàn có câu đối chứng để kiểm người chấm (bài 9). Nhưng mốc người
  mới chỉ có 20 cặp, để tham khảo.
- **Luật "không làm hỏng" chỉ bắt được tụt lan rộng.** Tụt nhỏ dồn vào một loại câu ít (ví dụ 2–3 câu so sánh) có thể lọt.
- **Bộ an toàn nhỏ.** 0 lỗi trên 28 câu trong kho chỉ chứng minh được tỉ lệ sai điều kiện **dưới khoảng 10–12 %**, chưa chứng minh được là rất thấp.
- **Máy nhận câu từ chối bằng cách so khớp đúng nguyên câu.** Lời từ chối viết khác câu chuẩn sẽ không được đếm là từ chối.
- **Bản đang chạy (có phần trợ lý) chưa được chấm lại trên cả 176 câu.** Mỗi phần mới chỉ được đo trên bộ câu riêng của nó trước khi bật. Lượt chấm lại cả bộ
  là bước cuối của Phase 9.

## Ba điều chính

1. **Claude chấm mù** theo 3 tiêu chí (Đúng · Đủ ý · Trúng ý, 1–5). Hai bản được **so theo cặp**, có khoảng tin cậy, và **so với dao động tự nhiên** (chạy cùng bản
   hai lần chỉ 1–2 câu đổi).
2. Có **mức tối thiểu không được phạm** (0 câu ngoài kho bị trả lời, bộ an toàn) và **thứ tự lỗi**: sai cảnh báo > nói chắc sai > trả lời ngoài kho > thiếu ý > từ
   chối nhầm.
3. Số chính: **Đúng 4,71** (4,96 khi đã trả lời), **Đủ ý 4,58** (yếu nhất ở câu nhiều nguồn 3,50), **từ chối nhầm khoảng 3 %**, **chữ đầu 2,2 giây**, **12 đồng /
   câu**. Bộ kín cho thấy số thật thấp hơn khoảng 0,4 điểm đủ ý.

**Bài sau:** Bài 12 — Từ chatbot thành trợ lý: vì sao cần một bước xếp loại câu hỏi, và "công cụ" là gì.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Đề chấm, 3 tiêu chí 1–5, các luật (không kiến thức ngoài, không chấm nguồn, câu từ chối): `backend/evaluation/full_corpus_judge_prompt.md` [code, xem 11/11]
- Chấm mù, câu giống hệt chấm một lần: `backend/experiments/phase_8_1/g2_generate.py` `pooled_items`; `backend/evaluation/full_corpus_eval.py` `judge_input_rows` [code]
- So theo cặp, bootstrap 10.000, Holm, nhận câu từ chối bằng so khớp nguyên câu: `full_corpus_eval.py` (`paired_stats`, `holm_adjust`, `verdict`, `is_refusal`) [code, xem 11/11]
- Nhiễu A/A (176 câu, 10 đoạn: Đủ tụt 1, Đúng tụt 2); người chấm 2 / 88; sinh + chấm lại 10 / 83: `bao_cao_he_thong/10_BAO_CAO_DANH_GIA.md` [đã chạy]
- Luật "không làm hỏng" (TB ≥ −0,1; số câu tụt ≤ A/A + 3): `10_BAO_CAO_DANH_GIA.md`, spec Phase 8.2 §10 [quyết định của anh, 26/10]
- Thứ tự lỗi (28/10), yêu cầu tốc độ / tiền: `session_prompt/Project_Status.md` §1, §5 [quyết định của anh]
- Điểm 01/11: 4,71 / 4,58 / 4,72; câu nhiều nguồn 3,50; chỉ câu được trả lời Đúng 4,96 / Đủ 4,82 (121 câu); bộ kín 4,18: `report_agent/2026-10-31_streaming_spec/do_cuoi_implementation.md`, `do_cuoi_b_bo_kin.md` [đã chạy]. Bản đầu 4,43 / 4,28 / 4,45 (24/10, đáp án mẫu sau đó có sửa): `10_BAO_CAO_DANH_GIA.md` [đã chạy]
- Từ chối nhầm 22 → 12 → 4 và 6 (hai lượt 03/11): `report_agent/2026-11-02_phase_9_code/b134_b2_implementation.md`, `07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` [đã chạy]
- Bộ an toàn 01/11; giới hạn dưới khoảng 10–12 %: `do_cuoi_b_an_toan_ngay.md`, `10_BAO_CAO_DANH_GIA.md` [đã chạy]
- Tốc độ / tiền 09/11 và 10/11: `bao_cao_he_thong/README.md` "Số chính", `07_…` [đã chạy]
- Mốc người B0 (01/11, 20 cặp): `10_BAO_CAO_DANH_GIA.md`, `data/phase_8_2/b0/` (riêng tư) [đã chạy]
- B3 vòng 1 từ chối nhầm 7 > 5, vòng 2 còn 4 (03/11): `07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` [đã chạy]

</details>
