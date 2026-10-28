# Phase 7 — Retrieval và Answer Evaluation

> **Guide lịch sử** (gắn nhãn 2026-10-25, rà code B26) **trừ mục "Hiện hành" ngay dưới**: phần sau mục đó tả evaluation Foods
> (08/2026) — file, judge, model và lệnh đã gỡ hoặc đã đổi.

## Hiện hành

Cập nhật 2026-10-27 (C69, theo W29 — guide "Hiện hành" cập nhật cùng lúc hành vi / thước đổi; trước: 2026-10-25). Nguồn chung: `session_prompt/Project_Status.md`
§2–§5, §8; `session_prompt/CURRENT_HANDOFF.md` "Phiên sau — đọc trước nhất"; báo cáo cho User `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` (bản 3).

- **Golden full-corpus (Phase 7A, User-closed 2026-10-23):** 176 case + smoke 10, schema 4 field (`question`, `keywords`, `reference_answer`, `category`), private
  `knowledge-base-hue/evaluation/`; md5 `0f7dbf41b422` sau khi sửa 10 đáp án 2026-10-25 (`Project_Status.md` §2 dòng 8.1). Spec
  `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md`.
- **Evaluator (Phase 7B, User-closed 2026-10-24):** `backend/evaluation/full_corpus_eval.py` — **10** lệnh con (`retrieval`, `generate`, `judge-luna`, `retry`,
  `export-judge-input`, `compare`, `split`, `context-coverage`, `diagnose-refusals`, `summarize`; `add_parser` trong file, đối chiếu 2026-10-27); đồng thời 4
  (`CONCURRENCY` `:50`). Sinh câu trả lời đi đúng thứ tự `api/routes/chat.py` (`answer_case` `:322`: tìm → đóng gói → `gpt-6-luna` → kiểm citation; câu lỗi citation
  vẫn giữ chữ để chấm, ghi `citation_error`). Câu hỏi gửi đi **nguyên văn** (chỉ `strip`, `answer_case` `:338`); NFC chỉ dùng cho khóa câu `question_key` (`:86`) và so keyword (`_fold` `:127`). Prompt judge cố định `backend/evaluation/full_corpus_judge_prompt.md`.
  Spec `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`.
- **Judge:** Claude (session Claude Code / sub-agent mới theo lô), chấm **mù**, mốc và biến thể **cùng một lượt** (`Project_Status.md` §8 "So điểm judge giữa biến
  thể"); `gpt-6-luna` chỉ là judge phụ. **Chưa có mốc người:** B0 (User đọc 20 cặp mù, ghi nhận xét, không chấm điểm) **chưa làm** (`CURRENT_HANDOFF.md` thứ tự việc
  bước 2; spec 8.2 §3 mục 3–4 luật dừng).
- **So hai cấu hình:** theo cặp từng câu — `paired_stats` (`full_corpus_eval.py:634`), bootstrap `:590`, 10.000 vòng (`:55`), Holm khi nhiều biến thể; 120 dev /
  56 test (`knowledge-base-hue/evaluation/phase_8_1/split.json`, sha `e2b1788dfbbc`); nhãn độ tự nhiên (`data/phase_8_1/golden_realism_final.jsonl`, 82 / 65 / 29 — số
  chính bỏ câu không tự nhiên). Test 56 câu chỉ dùng "không làm hỏng" (User 2026-10-27 08:47, spec 8.2 §10.6 Q2).
- **Luật nhận ghi trước** (skill `run-experiment` §1; spec 8.2 §10.2): sàn (0 câu ngoài kho bị trả lời, 0 lỗi kỹ thuật) · mức tụt (TB ≥ −0,1 và số câu tụt ≤ A/A + 3) ·
  chỉ số quyết vượt nhiễu. **Nhiễu A/A context 10, 176 câu** (B1 ↔ G2.1a, `phase_8_2_b1_implementation.md` §4 trên `p82-b1`): Completeness tụt 1, Accuracy tụt 2.
- **Nhãn đoạn đúng — ba bản, mọi số `*_gold_*` ghi kèm bản** (`CURRENT_HANDOFF.md` "Thước đo"):
  - v1 `data/phase_8_1/gold/gold_draft.jsonl` (`bab707b9ab22`, G0.6 khóa — không sửa; `data/phase_8_1/tools/validate_gold.py` tự dừng nếu file đã có, C62);
  - v2 `gold_v2.jsonl` (`2f5a347a71ff`, User duyệt 2026-10-27 13:05, merge `a819789`): v1 + 3 khoảng kho nói lại cùng ý + **luật trúng dòng tiêu đề**;
  - **v3** `gold_v3.jsonl` (`3b1117cf59e9`, **mặc định từ `fa192f8`**): v2 + 2 câu test (`report_agent/2026-10-26_cai_tien_tung_khau/gold_v3_review.md`).
  - Luật đếm: `backend/experiments/phase_8_1/g1_retrieval.py` — `GOLD_PATH` `:47`; trích dẫn là dòng tiêu đề Markdown trúng đoạn mang tiêu đề đó trong
    `heading_path` (`quote_is_chunk_heading` `:76`, `chunk_hits_quote` `:82`); một fact phủ khi **một** trích dẫn bất kỳ trúng, `all` cần mọi fact (`gold_coverage`
    `:93`; test `backend/tests/test_gold_coverage.py`). Mọi harness import `g1_retrieval.GOLD_PATH` (g2, g3, g4, harness 8.2 trên nhánh hồ sơ) ⇒ chạy lại sau
    `fa192f8` đếm theo v3.
  - Số mốc (context, chatbot 10 đoạn B1): dev 40 câu v1 22 / v2 24 / v3 24; test 15 câu v2 7 / v3 9.
- **Chỉ số lỗi citation:** từ gói 1a (`9e6d371`, 2026-10-25 19:58) validator nhận cả `[n]` lẫn `[Nguồn n]` ⇒ số trước / sau gói đó **không so trực tiếp**. Lượt B1 (sinh
  2026-10-25 16:35–16:38) chấm bằng validator **cũ**: 12 / 176 lỗi "no citation" đều qua validator hiện tại (C65,
  `report_agent/2026-10-25_phase_8_2_ap_dung/c65_citation_138_check.md`). Mốc cuối câu kín tách riêng số câu 500 kiểu này mỗi bên.
- **Câu kín** (36 câu, md5 `ddc59587b502`, khóa G0.6 2026-10-25 15:22, manifest `9ea480d0d083`): không đọc khi chưa được giao (`Session_Prompt.md` §5). Plan chạy mốc
  cuối duyệt sha `27e75be5ed44` (`report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b3_plan.md`): người chạy B, câu 500 vì citation = điểm 1 cả hai bên, tập
  quyết 33 câu.
- **Sau đợt sửa kho** (spec `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md`, User duyệt `937cf8969810`; chạy sau khi đóng 8.2): bộ "trước" 176 câu
  trước khi đụng kho (§5 bước 0); T1 mới **`23c58c47635d`** thay `cefb2d1ad609` (bước 6, 28/10 — 204 file / 8.426 đoạn); **gold v4** dựng sau build vì offset lệch (bước 7); Golden sửa từng mục User duyệt (bước 8);
  "sau" chấm cùng lượt + cùng Golden (bước 9); tiêu chí §6 (A/A = 2).
- Baseline 7B và số đo cũ: [`full_corpus_rag.md`](full_corpus_rag.md) mục "Cập nhật Phase 7B".

## Lịch sử (Foods và thiết kế trước 2026-10-23) — các mục dưới không phải hiện trạng

> **(Lịch sử)** **Full-corpus extension gate — 2026-09-12:** chưa active và phụ thuộc Phase 6
> closure. Reviewer phải cập nhật guide này bằng hai package tuần tự:
> Phase 7A Golden P7 và Phase 7B evaluator. Mỗi P7 có spec/plan/review scope riêng,
> Implementer report, full-row Reviewer review và User closure trước P7 kế tiếp;
> evaluator chỉ bắt đầu sau canonical Golden closure. Foods evaluation dưới đây
> vẫn là as-built history.

## Trạng thái

`approved` — baseline correction vòng 1 đã đạt technical review và được người
dùng xác nhận sau khi kiểm tra Notebook 07 ngày 2026-08-24 +07.

`post-simplicity correction approved` — correction hẹp đã được Implementer
hoàn tất, đạt independent technical review và được người dùng xác nhận sau khi
chạy Notebook 07 ngày 2026-08-26 +07. Ghi chú này không mở scope sửa dataset.

*(Lịch sử 08/2026)* Guide này từng là nguồn canonical cho scope, trạng thái và acceptance của Phase 7 Foods.

Đặc tả hỗ trợ:

```text
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-7-post-simplicity-correction-design.md
```

Kế hoạch triển khai hỗ trợ:

```text
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-7-post-simplicity-correction.md
```

## Mục tiêu

Đánh giá Hue Foods RAG bằng một luồng mà người đọc có thể hiểu ngay:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Phase 7 bắt đầu với `dense_only`. Sau khi baseline ổn định mới dùng cùng phép
đánh giá để so sánh:

- `dense_only`
- `hybrid_no_rerank`
- `hybrid_rerank`

## Nguyên tắc thiết kế

- Code đơn giản, rõ ràng và dễ đọc.
- Dùng backend hiện tại, không copy một RAG implementation khác vào project.
- Chỉ thêm file và hàm phục vụ trực tiếp evaluation.
- Không xây hạ tầng phòng xa.
- Có thể tối ưu kỹ thuật nâng cao sau khi chạy thật cho thấy nhu cầu.
- Nếu kỹ thuật nâng cao làm code phức tạp quá mức lợi ích thì phải loại bỏ.

Code reference trực tiếp cho Phase 7:

```text
<repo tham khảo>/tai_lieu/rag_old_0/evaluator2.py
<repo tham khảo>/tai_lieu/rag_old_0/pro_implementation
```

Hai reference này giúp định hướng Phase 7, không phải blueprint cho Phase 0–6.

## Cấu trúc

```text
backend/evaluation/
├── __init__.py
├── test.py
├── template.py
├── eval.py
└── evaluator.py

backend/tests/
└── test_evaluation.py

knowledge-base-hue/foods/evaluation/
├── test2.jsonl
└── tests.jsonl

notebooks/
└── 07_evaluation.ipynb
```

### `test.py`

Đọc câu hỏi từ đường dẫn được truyền vào. Mặc định dùng `test2.jsonl`.

### `template.py`

Chứa prompt của evaluation judge. Production generation prompt vẫn thuộc backend
chính và không được sao chép vào evaluation.

### `eval.py`

Chứa:

- MRR và nDCG keyword-based;
- retrieval evaluation;
- answer generation và judging;
- batch execution;
- summary;
- ghi hai CSV cố định.

### `evaluator.py`

Chứa giao diện Gradio với hai nút:

- `Đánh giá retrieval`
- `Đánh giá câu trả lời`

Hai nút dùng chung slider `Số câu chạy cùng lúc`, mặc định 3.

## Dữ liệu đánh giá

### Chạy thử

`test2.jsonl` chứa 20 câu thật được copy nguyên vẹn từ bộ 104 câu và phủ đủ 8
category hiện hành. Đây là smoke set để kiểm tra pipeline nhanh và tiết kiệm
chi phí, không phải bằng chứng chất lượng cuối cùng.

Audit ngày 2026-08-26 xác nhận smoke set hiện chưa có câu thuộc nhóm cafe và
golden dataset còn các vấn đề annotation/keyword cần thảo luận riêng:

```text
/home/minhhieu/hue_rag/reports/phase_7_golden_dataset_audit.md
```

Không sửa `test2.jsonl`, `tests.jsonl` hoặc tạo golden dataset mới trong
post-simplicity correction cho tới khi user duyệt design dữ liệu ở session
brainstorming riêng.

### Chạy đầy đủ

Sau khi implementation, dataset và smoke run đã sẵn sàng, chỉ thay input path
thành `tests.jsonl` để chạy 104 câu. Không thêm workflow hoặc cấu trúc output
mới cho lần chạy lớn hơn. Full run là evidence đánh giá đầy đủ; không suy rộng
kết luận chất lượng từ smoke set 20 câu.

Loader chỉ cần:

- `question`
- `category`
- `reference_answer`
- `keywords`

## Retrieval evaluation

Với mỗi câu:

1. Gọi real `dense_only` retrieval service.
2. Giữ retrieved chunks theo thứ tự trả về.
3. Tìm từng keyword trong chunk text, không phân biệt hoa thường.
4. Tính reciprocal rank và nDCG riêng cho từng keyword, sau đó lấy trung bình
   trên các keywords; keyword coverage là phần trăm keywords được tìm thấy.
5. Hiển thị row và ghi CSV.

Implementation giữ các biến trung gian như `avg_mrr`, `avg_ndcg`,
`keywords_found`, `total_keywords` và `keyword_coverage` để công thức dễ đọc;
không đổi semantics của `rag_old_0`.

Không dùng gold source hoặc section để tính MRR/nDCG.

Output cố định:

```text
backend/evaluation/retrieval_results.csv
```

Các cột chính:

```text
category, question, keywords, mrr, ndcg,
keywords_found, total_keywords, keyword_coverage, error
```

## Answer evaluation

Với mỗi câu:

1. Gọi retrieval thật.
2. Build labeled context string bằng `ContextBuilder.build(documents)`.
3. Sinh câu trả lời thật với `gpt-5.4-nano`.
4. So sánh generated answer với reference answer bằng `gpt-5.4-mini`.
5. Trả ba điểm 1–5 và feedback.

Ba điểm:

- accuracy: sai thực chất phải là 1; mức chấp nhận được là 3; chỉ hoàn toàn
  chính xác mới là 5;
- completeness: chỉ là 5 khi đủ toàn bộ thông tin quan trọng trong reference;
- relevance: chỉ là 5 khi trả lời trực tiếp và không thêm thông tin ngoài câu
  hỏi.

Relevance evaluation áp dụng answer-style contract của Phase 6: không thưởng
cho greeting, praise, emoji hoặc closing invitation máy móc. Nội dung lặp không
giúp trả lời câu hỏi có thể làm giảm relevance; list chỉ cần khi nhiều items hoặc
steps thực sự rõ hơn paragraph ngắn.

Output schema dùng integer 1–5 với validation bounds và mô tả ngắn cho ba điểm
cùng feedback. Judge không nhận retrieved context nên prompt/schema không được
tuyên bố rằng nó chấm groundedness. Giữ `temperature=0` *(lịch sử Foods; nay không truyền `temperature` — luna trả 400)* để chấm ổn định và
`max_tokens=600` để feedback ngắn có giới hạn rõ ràng.

Generator và judge vẫn dùng OpenAI Agents SDK, nhưng SDK tracing tắt mặc định
theo Phase 6 simplicity decision ngày 2026-08-25. Phase 7 không phụ thuộc Trace
Dashboard và không bật tracing riêng cho evaluation. CSV kết quả cùng safe local
logs là observability đủ cho scope hiện tại.

Evaluator nhận trực tiếp context string; không đọc `.context`, `.sources` hoặc
reconstruct source IDs. Empty string dùng cùng no-context policy với production
route.

Không có groundedness.

Output cố định:

```text
backend/evaluation/answer_results.csv
```

Các cột chính:

```text
category, question, reference_answer, generated_answer,
accuracy, completeness, relevance, feedback, error
```

Nếu một câu lỗi, ghi lỗi vào row và tiếp tục. Không retry, resume hoặc tạo file
trung gian.

## Giao diện

Giao diện hiển thị:

- đường dẫn file câu hỏi;
- một slider concurrency;
- hai nút evaluation độc lập;
- progress;
- bảng kết quả có đúng named columns tương ứng với retrieval hoặc answer;
- summary điểm trung bình;
- đường dẫn CSV đã ghi.

Nhấn nút được phép gọi paid API thật trực tiếp. Không có consent dialog hoặc
cost logic.

## Test

Chỉ giữ:

```text
backend/tests/test_evaluation.py
```

Giữ một nhóm test nhỏ và dễ hiểu cho các hành vi thật:

- đọc 20 và 104 câu từ đúng đường dẫn;
- kiểm tra fields cần dùng;
- kiểm tra MRR;
- kiểm tra nDCG;
- chạy retrieval thật;
- chạy một generation/judge thật;
- kiểm tra số outputs của UI handler.

Không tạo test files riêng cho cơ chế đã loại bỏ. Test pass không thay thế live
batch execution.

## Notebook 07

Notebook giải thích tuần tự:

1. Phase 7 đánh giá gì.
2. Đọc 20 câu thật.
3. Xem một câu hỏi.
4. Chạy retrieval thật.
5. Hiểu MRR/nDCG.
6. Sinh và chấm một câu thật.
7. Xem accuracy, completeness, relevance và feedback.
8. Chạy batch 20 câu.
9. Xem summary.
10. Mở giao diện.

Mỗi cell làm một việc, code ngắn và gọi backend.

Notebook style reference:

```text
<repo tham khảo>/tai_lieu/rag_old_0
<repo tham khảo>/tai_lieu/notebook_simple
```

Notebook không chứa artifact discovery, audit package hoặc test suite.

## Chạy thật, không fake

Implementer và Reviewer được phép dùng internet, Qdrant thật và paid OpenAI API
đã được người dùng cho phép.

Không dùng:

- fake ID, data, artifact, provider hoặc result;
- mock provider response;
- replay output;
- kết quả cũ hoặc bịa đặt làm evidence.

Active Hue Qdrant collection chỉ được đọc. Không in secrets.
Không bật Agents SDK tracing; không ghi full prompt, retrieved context hoặc raw
provider response vào logs/artifacts.

Coordinated Phase 4–5 blue-green verification được user duyệt ngày 2026-08-25
+07 cho phép retrieval-only evaluator nhận optional exact `collection_name` tại
composition root. Hàm copy settings trong memory, chọn profile/collection rồi
build real retrieval service. Override chỉ dùng để chạy fresh 104 questions × 3
profiles trên active baseline và `hue_foods_e5_small_384_dense`; nó không sửa
`settings.yaml`, không áp dụng cho answer evaluation/API và không tạo
multi-collection framework.

## Post-simplicity correction đã được duyệt

Reviewer đã xác nhận Phase 7 hiện dùng đúng contract đơn giản của Phase 6:

- `ContextBuilder.build(documents)` trả labeled context string;
- generator nhận question và context string rồi trả answer string;
- judge chỉ nhận question, reference answer và generated answer;
- tracing vẫn disabled.

Không cần redesign hoặc viết lại Phase 7 lần ba. Correction code chỉ gồm:

1. bỏ tham số `collection_name` khỏi `run_answer_batch()` và
   `run_answer_ui()` cùng các call/test chỉ phục vụ hai public answer paths này;
2. giữ optional collection override cho retrieval-only comparison và các
   guarded retrieval verification cần thiết;
3. không thêm abstraction, compatibility wrapper hoặc validation layer để thực
   hiện việc tách này.

Correction artifact gồm:

1. xóa execution counts và outputs khỏi canonical Notebook 07; bản Run All để
   kiểm chứng phải ghi ra `/tmp`;
2. giữ hai CSV cố định và ghi đúng dataset của lần chạy gần nhất; hiện tại mỗi
   CSV có 20 rows, còn full-run 104 rows trước đây là historical evidence trong
   implementation/review reports;
3. chưa chạy lại paid 104-answer batch cho tới khi scope dữ liệu ở audit được
   user chốt và Implementer/Reviewer sẵn sàng.

User đã duyệt exact correction design ngày 2026-08-26 +07. Implementer chỉ được
triển khai sau khi nhận prompt trỏ tới guide và implementation plan; không được
mở rộng sang dataset, metric, provider/model hoặc architecture khác.

## Những phần bị loại bỏ

Phase 7 mới không có:

- cost accounting hoặc cost estimation;
- consent/confirmation gate;
- calibration;
- resume;
- run ID hoặc generation run ID;
- timestamp quản lý evaluation package;
- checksum;
- package matching;
- tamper detection;
- partial artifact;
- artifact audit;
- validator chồng lớp;
- nhiều test files kỹ thuật.

Không được đổi tên hoặc chuyển nơi để giữ lại những cơ chế này.

## Acceptance

Phase 7 đạt khi:

1. package chỉ còn bốn module đã duyệt;
2. chỉ có một Phase 7 test file;
3. `test2.jsonl` có 20 câu thật thuộc đủ 8 category;
4. hai UI buttons chạy production path thật;
5. retrieval batch 20 câu hoàn thành;
6. answer batch 20 câu hoàn thành bằng nano và mini thật;
7. đổi input path và chạy 104 câu thật;
8. hai CSV có đúng số row và thứ tự câu hỏi;
9. Notebook 07 Run All thật đạt trên bản tạm;
10. repository notebook sạch outputs;
11. implementation report mới ghi đúng observed results và mọi lỗi;
12. Reviewer chạy lại độc lập và người dùng xác nhận.
13. Agents SDK tracing giữ disabled cho cả generator và judge.

Các mục trên ghi acceptance của baseline đã được duyệt. Post-simplicity
correction chỉ được đóng khi:

1. public answer batch/UI không còn collection override;
2. retrieval-only override vẫn chạy đúng exact approved comparison path;
3. Phase 6 context-string/generator-string contract vẫn được giữ;
4. canonical Notebook 07 không có execution count hoặc output;
5. tài liệu ghi đúng row count và nguồn gốc của artifact hiện hành;
6. dataset và full-run acceptance tuân theo design được duyệt ở session dữ liệu
   riêng;
7. Implementer báo cáo observed results, Reviewer kiểm tra độc lập và user xác
   nhận correction.

## Gate trước Phase 8

Sau Phase 7, review Phase 0 đến Phase 6 theo dependency order bằng tài liệu
riêng do người dùng cung cấp. Kiểm tra code, tests, folders và notebooks; đơn
giản hóa hoặc xây dựng lại phần over-engineered. Chạy lại affected Phase 7
evaluation sau thay đổi liên quan. Các review/correction này đã được user
approved; gate còn lại trước Phase 8 benchmark là hoàn tất và phê duyệt golden
dataset V2 implementation/real review theo design/plan đã duyệt, rồi tiếp tục
brainstorm và duyệt exact Phase 8 experiment contract.
