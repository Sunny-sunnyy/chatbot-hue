# Khảo sát reference cho Phase 7A Golden: `rag_old_0` và phiên âm bài học

Implementer: Claude Opus 5.5 (session `hue-rag-08`)
Date: 2026-10-23 (+07)
Base commit: `6da56b4` (worktree; report chỉ đọc, không sửa code/corpus/Golden)
Handoff: `session_prompt/CURRENT_HANDOFF.md` (survey `next_design`, risk low)

Viết tắt dùng trong report:

- `R0` = `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`
- `dN:L` = `R0/phien_am_bai_hoc/dayN.txt`, dòng L
- `FC` = `guides/full_corpus_rag.md`; `PS` = `session_prompt/Project_Status.md`;
  `P7G` = `guides/phase_7_retrieval_answer_evaluation.md`;
  `SPEC` = `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`

**Phạm vi đã đọc.**

- Full-read: `d1`–`d5`, `R0/evaluation/eval.py`, `R0/evaluation/test.py`,
  `R0/evaluator.py`, `R0/evaluator2.py`.
- Targeted-read: `R0/evaluation/tests.jsonl` (profile toàn bộ 150 dòng và 11
  dòng mẫu); các cell evaluation trong `day4.ipynb` và `day5.ipynb` (day1–3
  không có cell nào về test set hay evaluation); bullet Golden trong `PS`; `FC`
  dòng 86–102 và 151–286; `P7G` theo heading.
- Thêm ngoài danh sách input: grep `RETRIEVAL_K`, `FINAL_K` và `MODEL` trong
  `R0/implementation/answer.py` và `R0/pro_implementation/answer.py`, vì cần các
  giá trị này để hiểu metric.
- Reference-only: ba report thời Codex, chỉ xem heading, phần nguồn gốc dữ liệu
  và phần khả năng tái lập.
- Không chạy code `R0`, không gọi API, không chép nội dung private corpus Hue.

**Lưu ý về nguồn.** `phien_am_bai_hoc` là bản tổng hợp do AI tutor viết (mở đầu
"Chào Hieu", có phần "Kiến thức liên quan & mở rộng"), không phải lời giảng
nguyên văn. Report gán nhận định cho chính tài liệu này. Code trong phiên âm có
chỗ lệch code thật, ví dụ ngưỡng màu `d4:633-636` là 0.9/0.8 trong khi
`evaluator.py:11-20` là 0.9/0.75; khi lệch, code thật được ưu tiên.

## 1. `rag_old_0` tạo bộ câu hỏi thế nào

| Khía cạnh | Fact quan sát | Nguồn |
|---|---|---|
| File | Một file tĩnh `evaluation/tests.jsonl`, 150 dòng, không trùng câu hỏi | profile JSONL |
| Schema | Mọi dòng có đúng 4 field `question`, `keywords`, `reference_answer`, `category`; Pydantic `TestQuestion` chỉ load, không có field khác | `test.py:8-14` |
| Ai/cái gì tạo | Không có script hay notebook nào tạo hoặc ghi `tests.jsonl`; `day4.ipynb` chỉ `load_tests()`, đếm category và chạy thử 1 case. Kết luận này khớp với deep dive thời Codex §4.1 | `day4.ipynb` cells 1–13 |
| Nguồn dữ liệu nền | Knowledge base Insurellm là dữ liệu tổng hợp do LLM tạo | `d1:155` |
| Category | 7 nhãn, chia 70/20/20/10/10/10/10: `direct_fact` 70, `temporal` 20, `spanning` 20, `comparative` 10, `numerical` 10, `relationship` 10, `holistic` 10. File xếp theo khối category (65 `direct_fact` đầu, …, 10 `holistic` cuối) | profile JSONL |
| Định nghĩa category | Không có định nghĩa; chỉ có ví dụ trong mô tả field "direct_fact, spanning, temporal" | `test.py:14` |
| Keywords | 2–5 keyword/dòng (99 dòng có 2), tổng 376. **187/376 (50%) xuất hiện nguyên văn trong chính câu hỏi**; 7 dòng có *mọi* keyword đã nằm trong câu hỏi. 8 keyword không nguyên văn trong `reference_answer`. Có từ chung chung như `contracts`, `employees`, `products`, `founded`, `total`, `states` | profile JSONL |
| Reference answer | 1 câu ngắn đến vừa (30–226 ký tự, trung vị 78) | profile JSONL |
| Câu không trả lời được | **0/150** reference answer có ý "không có thông tin" | profile JSONL (regex) |
| Lỗi nội dung đã biết | Deep dive thời Codex đã ghi 2 dòng lệch corpus (dòng 101 và 141, đánh số từ 1) | reference-only §4.2 |

Mẫu đại diện (index đánh số từ 0):

- `[0]` direct_fact: hỏi ai thắng IIOTY 2023 → keywords
  `["Maxine","Thompson","IIOTY"]`.
- `[40]` direct_fact: chức danh của Emily Carter → `["Account Executive","Emily"]`.
- `[66]` temporal: James Wilson vào công ty khi nào →
  `["January 2017","James","Wilson"]`.
- `[92]` numerical: phần trăm quota → `["78%","Jennifer"]`.
- `[97]` relationship: Jessica Liu làm cho sản phẩm nào → `["Rellm","Jessica"]`.
- `[101]` spanning: technical lead của sản phẩm Standard Tier $10,000 →
  `["Robert","Chen","Homellm","$10,000"]`.
- `[141]` holistic: tổng giá trị mọi hợp đồng Healthllm →
  `["Healthllm","contract value"]`, reference liệt kê 4 hợp đồng và tổng.

## 2. Bài học dạy gì về thiết kế bộ câu hỏi và đánh giá

**Nguyên tắc**

- Evals là "Sao Bắc Đẩu". Không có số liệu thì chỉ còn "đập chuột chũi", sửa lỗi
  này sinh lỗi khác (`d4:7-8`; `d3:237`, `d3:264`).
- Đo riêng hai giai đoạn: retrieval và answer (`d4:9`, `d4:58`). Retrieval nằm
  trong tầm kiểm soát của kỹ sư nhưng chưa phải mục tiêu cuối; answer sát mục
  tiêu người dùng nhưng khó debug (`d4:105-106`).
- Quy trình gồm 4 bước: test set (câu hỏi, ngữ cảnh cần tìm, reference), đo
  retrieval, đo answer, rồi lặp lại (`d4:16-20`).
- Golden gồm câu hỏi điển hình, reference "hoàn hảo" và keywords "bắt buộc phải
  xuất hiện trong ngữ cảnh truy xuất" (`d4:64-66`).
- Nguồn câu hỏi: tự biên soạn từ tài liệu, hoặc **tốt nhất là câu hỏi thật của
  người dùng cùng câu trả lời của chuyên gia** (`d4:67`).
- Test set phải "hàng trăm câu hỏi đa dạng" và là tài sản quý nhất của kỹ sư RAG
  (`d4:47`).
- Phân tích theo category để tìm điểm yếu (`d4:432`, `d4:603`).
- Chụp baseline và chỉ nhận thay đổi làm số tăng; không tin cảm giác
  (`d4:669-670`, `d4:737`).

**Cạm bẫy và lý do**

- *Tổng quát hóa:* điểm cao trên test set nhưng thất bại với câu mới, nên test
  set phải là "living, breathing document"; phản hồi 👍/👎 của người dùng là
  nguồn Golden tương lai (`d4:104`, `d4:107`).
- *Điểm yếu cố hữu:* RAG cơ bản yếu ở `spanning` (dữ kiện rải nhiều file) và
  `holistic` (cần toàn kho) (`d4:497-499`, `d4:665-667`); cả `relationship`
  cũng yếu (`d4:604`).
- *Loại câu khó retrieval:* câu về sự kiện theo thời gian và **bảng biểu**
  (`d5:621`). Bảng nên được viết lại thành văn xuôi trước khi vector hóa
  (`d5:105`).
- *Chunk mất định danh:* chunk có fact nhưng không có tên thực thể, vì tên nằm ở
  đầu tài liệu (`d3:244-246`; `d4:37`).
- *Biến thể tên và lỗi chính tả:* keyword matching gãy khi gọi khác tên, vector
  thì chịu được (`d1:173`, `d1:229-232`; `d3:170`).
- *Bẫy lịch sử hội thoại:* LLM trả lời đúng nhờ lịch sử chứ không nhờ retrieval;
  khi test phải xóa lịch sử (`d1:226-227`). Câu hỏi nối tiếp và đổi chủ đề làm
  hỏng truy vấn kết hợp (`d3:241-252`).
- *Dữ liệu tổng hợp:* LLM có xu hướng "effusive"; muốn đa dạng thì prompt phải
  có chủ đích (`d1:157`).
- *Giám khảo:* "giám khảo phải giỏi hơn thí sinh" (`d4:589`). Khi so sánh các
  phiên bản thì giữ nguyên judge "để đảm bảo tính khách quan" (`d5:642`).
- *So sánh công bằng:* đổi chunk size thì đổi K để giữ tổng ngữ cảnh ("táo với
  táo") (`d4:681`).
- *Pseudoscience:* đừng thêm 10 bước để lấy 1–2% (`d5:191-195`).

## 3. Bộ câu hỏi được dùng để chấm ra sao

**Retrieval** (`eval.py:45-114`): mỗi keyword được so khớp substring không phân
biệt hoa/thường trên `doc.page_content` của từng chunk retrieved theo thứ tự.

- MRR = reciprocal rank của chunk *đầu tiên* chứa keyword, trung bình trên các
  keyword của case.
- nDCG@10 dùng binary relevance theo từng keyword, rồi lấy trung bình.
- Keyword coverage = % keyword tìm thấy trong danh sách retrieved.
- Dashboard lấy trung bình trên các case (`evaluator.py:79-101`).
- Độ sâu thực tế phụ thuộc `fetch_context`: bản basic lấy `RETRIEVAL_K = 5`
  (`implementation/answer.py:17`), nên MRR và coverage thực chất là @5. Bản pro
  trả `FINAL_K = 10` sau rerank (`pro_implementation/answer.py:28,134`).

**Answer** (`eval.py:117-161`): judge nhận `question`, generated answer và
`reference_answer` (không nhận retrieved context, dù mô tả field `feedback` nói
"evaluating based on the retrieved context", `eval.py:32-33`). Judge trả
structured output `feedback` cùng ba điểm `float` 1–5:

| Tiêu chí | Neo thang điểm trong code |
|---|---|
| Accuracy | "any wrong answer must score 1", "acceptable answer would score 3", 5 là "perfectly accurate" (`eval.py:34-36`, `eval.py:152`) |
| Completeness | 5 chỉ khi có đủ mọi thông tin của reference (`eval.py:37-39`) |
| Relevance | 5 chỉ khi trả lời trực tiếp và "gives no additional information" (`eval.py:40-42`) |

**Model, tái lập và tổng hợp**

- Judge `MODEL = "gpt-5-nano"` (`eval.py:14`). Generator bản pro cũng là
  `openai/gpt-5-nano` (`pro_implementation/answer.py:12`), nên **judge và
  generator trong code hiện tại là cùng một model**. Phiên âm lại ghi judge
  `gpt-4.1-nano` (`d4:169`) hoặc `gpt-4o-mini` (`d5:642`).
- Không đặt temperature hay seed cho judge. `evaluator2.py:41-60` thêm
  `seed=42` và `temperature=0` cho generator theo kiểu best-effort.
- Ngưỡng màu chỉ để hiển thị: MRR/nDCG/coverage 0.9 và 0.75; answer 4.5 và 4.0
  (`evaluator.py:11-20`).
- `evaluator.py` chia trung bình cho mọi case. `evaluator2.py:262-268` **loại
  case lỗi khỏi mẫu số** (chia cho `successful`).
- Breakdown theo category chỉ cho MRR và Accuracy (`evaluator.py:93,140`).
- Generator bản pro được báo trước rằng câu trả lời sẽ bị chấm theo accuracy,
  relevance và completeness (`day5.ipynb` cell 40).

## 4. Đối chiếu quyết định Golden Hue hiện hành

Cột "So với R0" so với code/dữ liệu `R0`; cột "So với bài học" so với phiên âm.
"Lý do trong Hue" chỉ ghi lý do mà tôi thấy trong các phần đã đọc, kèm path.

| # | Quyết định Hue (nguồn) | So với R0 | So với bài học | Lý do trong Hue |
|---|---|---|---|---|
| 1 | Một canonical JSONL; author/review theo 7 partition P7 tuần tự, rồi merge (`FC:153-159`, `FC:240-247`) | Giống ở chỗ chỉ có 1 file; partition authoring thì R0 không có | Không đề cập | Có: review từng partition (`FC:157`, `FC:242-247`) |
| 2 | Schema đúng 4 field `question`, `keywords`, `reference_answer`, `category` (`FC:167`; `PS` Golden) | **Giống** (`test.py:8-14`) | Giống (`d4:449-456`) | Không cần (giống reference) |
| 3 | Không `case_id`, claims, evidence spans hay chunk ID; `partition` bị strip khi merge (`FC:163-172`) | Giống (R0 không có các field này) | Không đề cập | Có: không có consumer, tránh annotation (`FC:93-102`) |
| 4 | Keywords: nguyên văn trong corpus, được reference hỗ trợ, không dùng từ chung chung, giữ thực thể trung tâm, không quota (`FC:175-185`) | **Khác (chặt hơn).** R0 có từ chung chung, 8 keyword không nằm trong reference, 50% keyword trùng chữ trong câu hỏi | Bài học chỉ nói keyword "phải xuất hiện trong ngữ cảnh" (`d4:66`) | Một phần: nêu quy tắc và lý do trọng số ngang nhau (`FC:182-184`); **không bàn việc keyword trùng chữ với câu hỏi** |
| 5 | 7 nhãn category giống R0, mỗi case đúng 1 nhãn, có định nghĩa theo thao tác chính (`FC:211-231`) | Giống tên nhãn; khác ở chỗ R0 không có định nghĩa | Bài học nêu `spanning`/`holistic` là điểm yếu (`d4:497-499`) | Có định nghĩa và quy tắc phân biệt (`FC:215-231`) |
| 6 | Không hard quota; planning target 150–200 (`PS`; `FC:281-282`) | **Khác.** R0 có 150 câu, phân bố tròn 70/20/20/10×4 (nhiều khả năng đã định trước — đây là diễn giải) | Bài học: "hàng trăm câu đa dạng" (`d4:47`) | Không thấy lý do cho "không quota" trong các phần đã đọc |
| 7 | Không chia dev/test; smoke đúng 10 dòng deep-equal, không thay full run (`PS`; `FC:265-272`) | Giống ở chỗ không split; R0 không có smoke | **Khác về rủi ro:** bài học cảnh báo overfit test set và muốn Golden sống (`d4:104`) | Smoke có lý do (`FC:269`). **Không thấy lý do cho "không dev/test"** trong các phần đã đọc |
| 8 | Merge rồi deterministic shuffle seed 42; không ID, manifest hay checksum (`FC:273-280`) | Khác: R0 xếp theo khối category; không có merge | Không đề cập | Có yêu cầu byte-identical (`FC:278-279`); mục đích của shuffle không được nêu |
| 9 | Retrieval: keyword-proxy MRR@10, nDCG@10, Coverage@10 với K=10 (`FC:189`; `PS`) | **Giống công thức** (`eval.py:45-114`); Hue cố định K=10, còn R0 phụ thuộc `fetch_context` (5 hoặc 10) | **Khác:** bài học định nghĩa MRR theo chunk liên quan đầu tiên *của câu hỏi* (`d4:25`, `d4:88-89`) và có Precision@K, Recall@K (`d4:27-28`); code lấy trung bình theo keyword | Có: keywords chỉ là relevance proxy, không phải ground truth (`FC:173-174`) |
| 10 | Ba answer metric dùng điểm nguyên 1–5, chấm riêng, không composite, không pass/fail (`FC:191-193`) | Giống ba tiêu chí; khác ở chỗ R0 dùng `float` | Giống (`d4:80-83`, `d4:101`) | Có: "như reference `rag_old_0`" (`FC:191`) |
| 11 | Rubric đủ 5 mức cho mỗi metric; Accuracy 3 = "đúng một phần, có ít nhất một sai lệch thực chất" (`FC:196-204`) | **Khác.** R0 neo "sai là 1", "chấp nhận được là 3" (`eval.py:34-36`); Foods Phase 7 cũng theo neo này (`P7G` mục Answer) | Bài học chỉ có thang 1–5 (`d4:101`) | Không thấy lý do đổi neo trong các phần đã đọc |
| 12 | Judge chỉ nhận question, answer và reference; không phải groundedness (`FC:194-210`; `SPEC:334`) | Giống (code); R0 có mô tả field nhắc tới context nhưng code không truyền | Giống (`d4:519`) | Có (`FC:208-210`) |
| 13 | Judge model: `SPEC:334` ghi `gpt-5.4-mini`; amendment 2026-10-23 đổi sang `gpt-6-luna`, **trùng generator** | Giống code R0 (judge cũng là generator `gpt-5-nano`) | **Khác:** judge phải mạnh hơn thí sinh (`d4:589`) và cố định khi so sánh (`d5:642`) | Có: User chấp nhận và ghi limitation (amendment `2026-10-23-phase-6-gpt-6-luna-amendment.md` §5 R5) |
| 14 | Judge `temperature=0`, cap 600 tokens (`SPEC:338`; `P7G`) | Khác: R0 không đặt temperature cho judge | Không đề cập (bài học nói temp=0 cho generator, `d3:55`) | Có (`P7G` mục Answer). Với `gpt-6-luna`, temperature chưa được xác minh (R4) |
| 15 | Macro-average theo case; lỗi kỹ thuật làm run `incomplete`, không bị loại khỏi mẫu số (`PS`; `SPEC:345-348`) | Giống `evaluator.py`; **khác `evaluator2.py`** (loại case lỗi) | Không đề cập | Có, nêu rõ (`PS`) |
| 16 | Chưa đặt metric threshold trước full-corpus baseline (`PS`) | Khác: R0 có ngưỡng màu chỉ để hiển thị | Bài học có ngưỡng xanh/vàng/đỏ (`d4:611`) | Có ngầm: chờ baseline (`PS`) |
| 17 | Implementer author từ corpus; web chỉ để học văn phong; User và Reviewer đọc từng case (`FC:232-239`) | Khác: R0 không có provenance hay quy trình review | **Khác một phần:** bài học khuyên nguồn tốt nhất là câu hỏi thật của người dùng (`d4:67`); Hue chưa có người dùng production | Có quy trình review; lý do không dùng câu hỏi thật chưa được nêu |
| 18 | Phải chạy full cả 6 metric trên mọi case; smoke không thay (`FC:281-286`) | Giống (R0 chạy toàn bộ 150) | Giống (`d4:609`) | Có (`FC:285`) |
| 19 | Câu hỏi single-turn (schema chỉ có `question`) | Giống | Bài học dạy history/follow-up là failure mode (`d3:241-252`) | Phù hợp với API Phase 6 không có history (diễn giải) |
| 20 | Case không trả lời được / out-of-scope | R0: 0 case | Không đề cập | **Không đề cập** trong quyết định Golden; Phase 6 có fallback `INSUFFICIENT_ANSWER` nhưng Golden không có case kiểm nó |

## 5. Ý tưởng từ nguồn mà Hue chưa có (chỉ là lựa chọn)

| Ý tưởng | Nguồn | Phù hợp với Hue | Chi phí và rủi ro |
|---|---|---|---|
| A. Thêm case không trả lời được / out-of-scope | Ngược với R0 (0 case); Phase 6 live smoke đã có case `out_of_scope` | Kiểm hành vi từ chối mà API đã cam kết | Schema bắt `keywords` không rỗng (`FC:175`), nên retrieval metric không có nghĩa cho case này. Phải chọn: thêm quy tắc riêng (đổi contract 7B) hoặc giữ ngoài Golden |
| B. Quy tắc keyword chống trùng câu hỏi, ví dụ mỗi case có ≥1 keyword mang đáp án và không có trong câu hỏi | Quan sát R0: 50% keyword trùng chữ câu hỏi; 7 case trùng toàn bộ | Làm MRR và coverage phản ánh việc tìm được *đáp án* chứ không chỉ tên thực thể; khớp tinh thần `FC:176` | Rẻ (kiểm tra lúc author). Có thể mâu thuẫn với "giữ thực thể trung tâm" (`FC:180`) nếu áp quá cứng |
| C. Chủ động có case mà đáp án nằm trong bảng (giá vé, giờ mở cửa…) theo từng P7 có bảng | `d5:105`, `d5:621`; Phase 6 F2 (retrieval miss trên chunk bảng giá, review 2026-10-23) | Bao phủ đúng điểm yếu đã quan sát thật | Rẻ khi author; đây chỉ là ưu tiên bao phủ, không phải quota |
| D. Case "chunk mất định danh": fact nằm xa tên thực thể trong tài liệu | `d3:244-246` | Kiểm việc `heading_path`/`search_text` có giữ định danh không | Rẻ; cần người author biết cấu trúc tài liệu |
| E. Biến thể cách gọi tên (tên gọi khác, không dấu, viết tắt) trong câu hỏi | `d1:173`, `d3:170` | Hợp với người dùng Việt gõ không dấu hoặc gọi tên địa phương | Keyword vẫn phải giữ nguyên văn corpus (`FC:177-179`); chỉ đổi câu hỏi. Rủi ro: câu không tự nhiên |
| F. Judge khác generator, giữ cố định khi so sánh trong Phase 8 | `d4:589`, `d5:642` | Phase 8 so Qwen với `gpt-6-luna`; nếu judge là `gpt-6-luna` thì có thiên vị tự chấm (R5) | Cần User quyết model/provider (đổi authority). Thêm chi phí judge |
| G. Golden "sống": thêm case từ lỗi quan sát được (👎, review) qua lifecycle riêng | `d4:104`, `d4:107` | Chưa có người dùng production; có thể dùng lỗi từ review (như F2) | Cần quy trình version và closure; mâu thuẫn với canonical cố định nếu làm trong 7A |
| H. Dev/test hoặc holdout để giảm overfit khi tune ở Phase 8 | `d4:104` (diễn giải) | Phase 8 sẽ chọn model/treatment trên chính Golden | Đi ngược quyết định "không dev/test" đã chốt; giảm cỡ mẫu mỗi tập |
| I. Kiểm Unicode NFC cho keyword/reference khi merge | Quan sát Hue: 8/255 file `.md` không NFC, cả 8 nằm trong `_source-dumps/`; mọi file ngoài đó đều NFC | Substring match không bỏ dấu và không normalize (`FC:178-179`; `SPEC:65`) dễ hỏng âm thầm nếu text author ở dạng NFD | Rất rẻ (một phép so `unicodedata`); rủi ro hiện tại thấp |
| J. Precision@K/Recall@K như bài học | `d4:27-28` | Ít phù hợp: keyword proxy không định nghĩa được "chunk liên quan" | Thêm metric thì đổi contract 7B; khuyến nghị không thêm (diễn giải) |
| K. Breakdown theo category cho mọi metric (R0 chỉ có MRR và Accuracy) | `evaluator.py:93,140` | Hue đã có category breakdown (`SPEC:345`) | Không cần làm gì |

Không đưa vào lựa chọn: báo trước cho generator rằng sẽ bị chấm theo tiêu chí
(`day5.ipynb` cell 40). Đây là quyết định prompt của Phase 6/8, không phải của
Golden, và có rủi ro "dạy theo đề".

## 6. Fact và diễn giải; điểm chưa rõ

**Fact (đã kiểm trực tiếp):** schema và số liệu `tests.jsonl` ở §1; công thức
metric, prompt judge, model, ngưỡng màu và cách chia mẫu số ở §3 (dẫn dòng
code); trạng thái NFC của corpus Hue (chỉ đếm, không chép nội dung); các quyết
định Hue dẫn từ `FC`, `PS`, `SPEC` và `P7G`.

**Diễn giải (không phải fact):**

- Phân bố 70/20/20/10×4 có vẻ đã được định trước.
- Việc 50% keyword trùng chữ câu hỏi làm metric retrieval "dễ" hơn thực tế.
- Câu hỏi single-turn phù hợp với API Hue.
- Precision@K không hợp với keyword proxy.
- Tác động của các ý tưởng ở §5.

**Điểm chưa rõ:**

1. Ai và cách nào tạo `tests.jsonl` (tay hay LLM): không có bằng chứng trong `R0`.
2. Phiên âm không phải transcript gốc; các model nó nêu (`gpt-4.1-nano`,
   `gpt-4o-mini`) lệch code hiện tại (`gpt-5-nano`), nên không biết số liệu
   MRR 0.73 → 0.91 (`d5:613-615`) ứng với model nào.
3. Lý do Hue đổi neo rubric Accuracy (#11), bỏ quota (#6), không chia dev/test
   (#7) và shuffle seed 42 (#8): không thấy trong các phần đã đọc. Có thể nằm
   trong report thời Codex (reference-only) hoặc spec/plan chưa mở.
4. `SPEC:334` vẫn ghi judge `gpt-5.4-mini`, trong khi amendment 2026-10-23 đổi
   sang `gpt-6-luna`; spec và guide 7B chưa được cập nhật theo.
5. Hue Implementer là một LLM, nên Golden Hue thực chất do LLM author rồi người
   review. Bài học khuyên dùng câu hỏi thật làm nguồn tốt nhất; việc này có cần
   ghi thành limitation không là quyết định của Reviewer/User.
