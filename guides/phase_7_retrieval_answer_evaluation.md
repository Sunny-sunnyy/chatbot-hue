# Phase 7: Đánh giá retrieval và câu trả lời

## Mục tiêu và giá trị cho người dùng

Phase 7 tạo evaluation harness tái lập cho 104 câu hỏi tiếng Việt: đo retrieval trước, sau đó đánh giá answer quality bằng rubric có cấu trúc. Phase này biến cảm nhận thủ công thành bằng chứng đủ để Phase 8 so sánh model và pipeline.

## Trạng thái

```text
Status: changes_requested
Brainstorming level: Level 3 - deep
Owner: Codex Reviewer
Implementer: DeepSeek
```

## Dependency

- Phase 5 retrieval profiles và Phase 6 generator/API đã được approve.
- Test corpus có 104 JSONL rows tại `knowledge-base-hue/foods/evaluation/tests.jsonl`.
- Mỗi row hiện có `question`, `keywords`, `reference_answer`, `category`.
- Dataset sẽ được nâng cấp trong Phase 7 với explicit `case_id`,
  `relevant_sources` và source-to-section mapping đã được người dùng phê duyệt.
- Answer judge dùng OpenAI Agents SDK với `gpt-5.4-mini`.

## Chức năng phải tạo

- Strict JSONL loader và schema validation.
- Retrieval relevance ground-truth contract.
- Per-question và aggregate Recall@k, MRR, nDCG@k, keyword coverage và latency.
- Category/profile/model breakdown.
- Answer generation tách khỏi judge khi cần kiểm soát cost.
- Structured LLM-as-judge rubric.
- Atomic, resumable và traceable JSONL artifacts.
- Markdown summary trong benchmark ledger.
- Safe evaluation notebook.

## Files dự kiến

```text
backend/evaluation/test_loader.py
backend/evaluation/metrics.py
backend/evaluation/retrieval_eval.py
backend/evaluation/answer_eval.py
backend/evaluation/artifacts.py
backend/evaluation/evaluator.py
backend/evaluation/results/.gitkeep
backend/config/settings.yaml
backend/tests/test_evaluation_loader.py
backend/tests/test_evaluation_metrics.py
backend/tests/test_evaluation_artifacts.py
backend/tests/test_retrieval_evaluation.py
backend/tests/test_answer_evaluation.py
knowledge-base-hue/foods/evaluation/tests.jsonl
knowledge-base-hue/foods/evaluation/answer_subset_v1.json
knowledge-base-hue/foods/evaluation/judge_calibration_v1.jsonl
knowledge-base-hue/foods/evaluation/validate_tests.py
notebooks/07_evaluation.ipynb
reports/hue_foods_rag_benchmark.md
```

## Test-case contract

Approved Phase 7 shape:

```python
{
    "case_id": "foods-0001",
    "question": "Quán bún bò Mệ Kéo nằm ở đâu?",
    "keywords": ["Mệ Kéo", "Bạch Đằng"],
    "reference_answer": "...",
    "category": "direct_fact",
    "relevant_sources": ["foods/restaurants/quan bun bo me keo.md"],
    "relevant_sections": {
        "foods/restaurants/quan bun bo me keo.md": ["Thông tin"],
    },
}
```

Loader requirements:

- đúng 104 non-empty rows cho baseline dataset version;
- explicit unique stable case ID `foods-NNNN`, không derive lại từ question hoặc category;
- non-empty question/reference/category;
- keywords là list non-empty strings;
- invalid row fail với line number, không skip âm thầm;
- source file chỉ read-only trong evaluation run;
- dataset checksum/version được ghi trong run metadata.
- mỗi case có ít nhất một `relevant_sources`; mọi path tồn tại dưới
  `knowledge-base-hue/`;
- key trong `relevant_sections` phải thuộc `relevant_sources`; section được khai
  báo phải tồn tại trong Markdown tương ứng;
- ground truth là tập evidence tối thiểu nhưng đủ hỗ trợ toàn bộ
  `reference_answer`, không phải mọi document cùng chủ đề;
- baseline chỉ được freeze khi validator giữ đủ 104/104 case hợp lệ.

## Retrieval ground truth bắt buộc

Recall, MRR và nDCG dùng gold evidence do Implementer đối chiếu trực tiếp curated
foods KB, Codex audit độc lập và người dùng kiểm tra trong notebook 07. Không dùng
web hoặc LLM để tự suy đoán annotation.

Ground-truth unit:

- source có khai báo section: mỗi cặp `(source, section)` là một evidence unit;
- source không khai báo section: source đó là một evidence unit và section nào
  trong source cũng có thể match;
- retrieved duplicates cùng `(source, section)` chỉ giữ rank xuất hiện đầu tiên;
- relevance là binary `1/0`; Phase 7 không tự gán graded relevance;
- keyword coverage chỉ là lexical diagnostic, không thay gold relevance.

## Retrieval metrics contract

Với relevance judgments đã chốt:

- report `Recall@1`, `Recall@3`, `Recall@5`, `Recall@10`;
- report `MRR@10`, `nDCG@5` và `nDCG@10` với binary relevance;
- primary retrieval metric là macro-average `Recall@5` qua tám category với
  trọng số category bằng nhau;
- secondary overall metrics tính trực tiếp trên 104 cases;
- `keyword_coverage@5/@10` chuẩn hóa Unicode NFC, casefold và whitespace nhưng
  giữ dấu tiếng Việt, dùng exact phrase trên `title + section + text`;
- keyword coverage không tham gia chọn profile;
- latency tách `setup_latency_ms` khỏi per-case `retrieval_latency_ms`; report
  median và p95 retrieval latency theo profile/category.

Metric tests phải bao phủ:

- no relevant result;
- first-rank relevant;
- multiple relevant results;
- fewer than k results;
- duplicate retrieved IDs;
- empty relevant set phải bị loader/validator reject;
- overall và per-category aggregate.

Không tune pipeline trên test result rồi báo cùng run như unbiased evaluation. Mọi config change tạo run ID mới.

## Retrieval run protocol

```text
load and validate 104 cases + gold evidence
  -> freeze dataset checksum
  -> freeze collection/model/profile/config
  -> readiness/warm every required real dependency
  -> retrieve each question in stable case_id order without generation
  -> deduplicate evidence units and record ranked IDs/sources/sections/scores/latency
  -> compute per-case metrics
  -> aggregate overall and per category
  -> atomically write JSONL and summary metadata
  -> Codex verifies artifacts before updating the benchmark ledger
```

Retrieval evaluation không gọi answer model hoặc judge. Initial Phase 7 validation
chạy tuần tự đủ 104 cases cho từng profile `dense_only`,
`hybrid_no_rerank`, `hybrid_rerank` trên cùng active collection. Không sửa
`active_profile` trong config và không có implicit profile default. Evaluation
được phép lấy/rerank tối đa 10 results để tính metric `@10`; override này phải
được ghi rõ trong run metadata và không mutate runtime config.

Case failure được giữ trong artifact. Summary report cả complete-case metrics và
`effective Recall@5` với failed case tính `0`. Chỉ run 104/104 complete mới đủ
điều kiện làm Phase 8 comparison evidence; partial run chỉ là diagnostic.

## Answer generation protocol

Answer evaluation bắt đầu bằng fixed manifest
`knowledge-base-hue/foods/evaluation/answer_subset_v1.json`: đúng 24 case, ba
case mỗi category, gồm một case tương đối trực tiếp, một case nhiều evidence hơn
và một case rộng/khó hơn. Manifest dùng explicit `case_id`, không random lại.
Full 104 answer generation/judge chỉ chạy khi người dùng phê duyệt riêng.

Tách artifacts:

```text
generation JSONL: query, reference, generated answer, used sources, model/config, latency, usage
judge JSONL: generation run ID, rubric version, scores, concise feedback, judge model, latency, usage
```

Nhờ đó có thể re-judge frozen answers mà không trả thêm phí generation.

Initial answer run bắt buộc khai báo `--answer-profile hybrid_rerank`. Đây là
profile được chọn để chạy answer evaluation, không phải Phase 8 winner.

## LLM-as-judge contract

```text
SDK: OpenAI Agents SDK
Judge model: gpt-5.4-mini
Credential: OPENAI_API_KEY
Scale: 1–5 cho mỗi dimension
```

Structured output:

```python
{
    "accuracy": 1,
    "completeness": 1,
    "relevance": 1,
    "groundedness": 1,
    "feedback": "Concise evidence-based feedback",
}
```

Rubric:

- `accuracy`: factual correctness so với reference/evidence; contradiction không được điểm cao.
- `completeness`: bao phủ ý cần thiết trong reference, không cần copy wording.
- `relevance`: trả đúng câu hỏi, không lạc đề.
- `groundedness`: claims có support trong retrieved context/sources.

Judge chỉ nhận question, reference, generated answer, exact bounded evidence đã
được generator dùng cùng source/section labels và rubric version. Judge không
nhận toàn KB, gold source content không được retrieve, chain-of-thought, API
headers hoặc unrelated cases. Rubric version và prompt hash được ghi.

Một answer pass khi `accuracy >= 4`, `groundedness >= 4`, mean bốn dimensions
`>= 4` và không dimension nào dưới `3`. Điểm thấp được giữ làm quality evidence,
không tự làm implementation harness fail.

Một retry tối đa chỉ dành cho timeout, transient connection failure hoặc invalid
structured output. Không retry để tìm điểm đẹp hơn và không retry generation vì
judge chấm thấp. Failed judge row được giữ, không drop khỏi denominator âm thầm.

## Judge quality controls

- Trước batch trả phí, chạy `judge_calibration_v1.jsonl`: bốn representative
  categories (`direct_fact`, `spanning`, `holistic`, `guide_planning`), mỗi case
  có một frozen good answer và một frozen bad answer, tổng tám real judge calls.
- Calibration pass khi good answer có accuracy/groundedness `>= 4`, bad answer
  có accuracy hoặc groundedness `<= 2`, và feedback chỉ ra đúng lỗi chính.
- Calibration fail thì dừng trước subset 24 và sửa rubric/prompt thành version
  mới; không rewrite artifact cũ.
- Judge `gpt-5.4-mini` tách khỏi answer model `gpt-5.4-nano`.
- Nếu re-judge sample, giữ cả hai runs thay vì overwrite.
- Không dùng fake provider, fake runner hoặc replay response làm Phase 7 PASS
  evidence. Hand-calculated ranking chỉ dùng để test metric math.

Initial paid run có normal call count 56 (8 calibration + 24 generation + 24
judge), hard cap 64 calls để dành tối đa tám retry và hard cost cap `$0.50`.
Runner estimate cost trước run, yêu cầu `--confirm-paid`, kiểm tra cap trước mỗi
call và tính lại actual/estimated cost từ provider usage. Toàn evaluation chạy
tuần tự với concurrency `1`.

## Result artifact schema

Mỗi retrieval JSONL record có:

```text
run_id
timestamp_utc_plus_7
dataset_path
dataset_checksum
corpus_checksum
config_checksum
case_id
category
question
profile
embedding_provider
embedding_model
collection_name
retrieved_items
metrics
setup_latency_ms
latency_ms
status
error_type
```

Answer/judge record thêm generation model, judge model, reference, generated answer, used sources, rubric version, prompt hash, attempts, usage và cost. Không lưu secret, raw header, chain-of-thought, full retrieved context hoặc full SDK object.

Artifact layout:

```text
backend/evaluation/results/
  retrieval/<run_id>.jsonl
  retrieval/<run_id>.summary.json
  generations/<run_id>.jsonl
  judges/<run_id>.jsonl
  summaries/<run_id>.json
```

Runner ghi `<run_id>.partial.jsonl`, flush an toàn sau mỗi case, resume chỉ skip
record cùng run ID/case ID và status complete, rồi atomic rename/finalize khi
run hoàn tất. `run_id` chứa timestamp UTC+7, profile và shortened dataset
checksum. Không overwrite, không auto-delete và không tự sửa benchmark ledger.

## Brainstorming Level 3 đã hoàn tất

Codex và người dùng đã chốt gold evidence, binary relevance, metric cutoffs,
macro category `Recall@5`, fixed 24-case answer subset, four-dimension judge
rubric, calibration gate, retry policy, 64-call/`$0.50` cap, artifact layout,
resume/no-overwrite policy, sequential execution và user ground-truth audit.

Mỗi run phải giữ test corpus/config frozen để Phase 8 so sánh công bằng. Phase
7 không tuyên bố profile winner và không đặt quality floor làm implementation
acceptance; điểm thấp là observed evidence cho Phase 8.

## CLI contract

```bash
cd backend
uv run python -m evaluation.evaluator retrieval --profiles all
uv run --env-file ../.env python -m evaluation.evaluator answers --answer-profile hybrid_rerank --confirm-paid --max-calls 64 --max-cost-usd 0.50
uv run --env-file ../.env python -m evaluation.evaluator all --profiles all --answer-profile hybrid_rerank --confirm-paid --max-calls 64 --max-cost-usd 0.50
```

- `evaluator.py` là single user-facing CLI facade; metric/provider/artifact logic
  nằm trong focused modules và notebook import lại modules này;
- retrieval bắt buộc `--profile <name>` hoặc `--profiles all`, không có implicit
  profile;
- `answers` luôn chạy calibration hoặc nhận completed matching calibration
  artifact cùng rubric/prompt hash;
- thiếu `--confirm-paid` thì chỉ in preflight, không gọi OpenAI;
- `--resume <run_id>` tiếp tục incomplete cases; `--quiet` chỉ in progress và
  summary;
- default terminal in per-case status/metric/latency; answer mode in question,
  generated answer, source/section labels, four scores và concise feedback;
- không in full retrieved context và không có fake/dry-run/replay path.

## Nhiệm vụ của DeepSeek Implementer

- TDD metrics bằng known rankings trước khi nối runtime.
- Không copy trực tiếp `rag_old` evaluator; chỉ dùng metric/rubric concepts và sửa provider/schema inconsistencies.
- Giữ `evaluator.py` là thin CLI facade; không gom loader, metric, provider calls,
  artifact lifecycle và terminal rendering thành một monolith kiểu cũ.
- Annotation đủ 104 cases bằng cách đối chiếu trực tiếp curated KB; không dùng
  web hoặc LLM để suy đoán gold evidence.
- Pure metric/loader/artifact tests dùng known inputs; integration và acceptance
  dùng Qdrant/model/provider thật theo Live-Only Validation Policy.
- Chạy bounded live calibration và answer/judge trong exact call/cost cap đã
  approved; giữ mọi failure/partial outcome.
- Không cập nhật ledger bằng estimated/fabricated metrics.
- Report exact commands, artifact paths, completed/failed counts và approval.

## Nhiệm vụ của Codex Reviewer

- Audit ground truth, metric math và denominator policy.
- Audit toàn bộ 104 source/section mappings và recompute representative metric
  cases độc lập.
- Kiểm tra dataset/config checksum và artifact completeness.
- Calibrate judge sample, audit actual model/cost và failed rows.
- Không approve proxy metric bị mô tả như gold relevance.

## Notebook bắt buộc

`notebooks/07_evaluation.ipynb` phải:

- import evaluation modules;
- giải thích ground truth và metrics bằng tiếng Việt, đồng thời hiển thị bảng
  audit đủ 104 mappings theo category cho người dùng kiểm tra;
- minh họa hand-calculated ranking để giải thích metric và ghi rõ đây không phải
  RAG quality evidence;
- kiểm tra live active Qdrant collection read-only và chạy một retrieval probe
  thật;
- bắt buộc đọc exact completed artifacts khớp dataset/config/model checksum,
  recompute summary từ per-case records và fail rõ nếu artifact thiếu/mismatch;
- hiển thị so sánh ba profiles và 24 question/answer/source/judge results;
- không tự gọi lại paid batch khi Run All, không dùng sample/prior output thay
  completed reviewed artifacts và không lưu 104 answers, raw payload hoặc secrets;
- committed outputs rỗng và `execution_count=null`.

## Tests và validation dự kiến

```bash
cd backend
uv run python -m py_compile evaluation/test_loader.py evaluation/metrics.py evaluation/retrieval_eval.py evaluation/answer_eval.py evaluation/artifacts.py evaluation/evaluator.py
uv run --env-file ../.env python -m pytest tests/test_evaluation_loader.py tests/test_evaluation_metrics.py tests/test_evaluation_artifacts.py tests/test_retrieval_evaluation.py tests/test_answer_evaluation.py -q --tb=short
```

Pure deterministic gates pass trước external run. Retrieval command cần local
Qdrant readiness. Answer/judge command dùng standing authorization và exact
approved cost/call caps; provider failure là failure thật, không có fake
fallback. Full relevant backend regression suite cũng phải pass qua `uv run`.

## Security, reliability và performance gates

- No key/header/raw SDK object trong artifacts.
- Sequential concurrency `1`, bounded timeout, retry, call count và cost.
- Failed rows retained với safe error type.
- Atomic output và resumable run.
- Dataset/config checksum chống so sánh nhầm.
- Judge prompt chỉ nhận case hiện tại.
- Full 104 paid run không bao giờ là default.
- Dataset/config/collection/model preflight fail thì abort trước case đầu; per-case
  failure được record và tiếp tục.
- Ba dependency failures liên tiếp mở circuit breaker, dừng stage và đánh dấu
  remaining cases chưa chạy.
- Active collection schema/count được kiểm tra trước/sau; không reset, reindex,
  upsert hoặc delete.

## Tiêu chí phê duyệt Phase 7

- 104 cases load strict, có valid gold source/section evidence và dataset version được ghi.
- `answer_subset_v1.json` có đúng 24 cases, ba case mỗi category; calibration có
  tám approved real judge calls và đạt gate.
- Metrics pass hand-calculated tests.
- Cả ba full retrieval runs đạt 104/104 trên cùng dataset/collection và tạo
  complete JSONL/summary; partial run không dùng làm comparison evidence.
- Initial `hybrid_rerank` answer subset/judge dùng đúng model/rubric, không vượt
  64 calls/`$0.50`, có actual usage/cost/failure evidence.
- Active collection vẫn đúng schema và 572 points sau validation.
- Notebook recompute đúng artifacts, an toàn, outputs sạch và cho phép người dùng
  audit gold ground truth.
- Ledger chỉ ghi kết quả thực.
- User report phản ánh đúng metrics, failed/skipped runs và được người dùng xác nhận cùng notebook.

## Reports và cập nhật trạng thái

```text
reports/phase_7_retrieval_answer_evaluation_implementation_report.md
reports/phase_7_retrieval_answer_evaluation_codex_review.md
reports/hue_foods_rag_benchmark.md
reports/user_reports/phase_7_retrieval_answer_evaluation_user_report.md
```

Sau technical review đạt, Codex tạo user report `pending`; chỉ cập nhật `Project_Status.md` sau khi người dùng xác nhận notebook/report, không phải sau partial live run.

## Quyết định đã phê duyệt

```text
Decision: Phase 7 dùng modular evaluation harness với single evaluator.py CLI,
gold source/section evidence cho 104 cases, macro category Recall@5, fixed
24-case answer subset, real gpt-5.4-nano/gpt-5.4-mini evaluation, bounded
calibration/cost, immutable resumable artifacts và notebook 07 làm audit UI.
Approved by: User
Approval date +07: 2026-08-22
Evidence: Level 3 brainstorming trong Reviewer session; người dùng xác nhận từng
phần architecture, data, metrics, CLI/artifacts, safety, tests/notebook và
acceptance gates.
Affected scope: Phase 7 guide, foods evaluation dataset/validator,
backend/evaluation, relevant tests, config, notebook 07, Phase 7 reports và
verified benchmark summary.
Revisit trigger: Thay ground-truth semantics, metric/threshold, subset/rubric,
provider/model, 64-call hoặc $0.50 cap, artifact compatibility, active
collection contract hay Phase 7/8 boundary.
```

## Bước tiếp theo

Phase 7 tiếp tục `changes_requested` sau Codex re-review revision 9. Consent,
NaN, duplicate partial calibration và `all` regressions của Revision 8 đã sửa.
Tuy nhiên production CLI calibration-final path vẫn bypass raw validator và
không rebuild missing summary; budget loader còn chấp nhận missing totals,
unknown model và calls vượt frozen cap. Attempt linkage chưa được đối chiếu với
journal. Coding agent phải sửa theo hướng dẫn Revision 10 trong
`reports/phase_7_retrieval_answer_evaluation_codex_review.md`, chạy pure tests và
read-only validation rồi dừng trước paid rerun. Phase 8 vẫn `not_ready`.

## Handoff hiện tại

Snapshot: `2026-08-23 +07`.

- Codex revision 9 decision: `changes_requested`; chưa cấp phép paid rerun.
- Evidence đạt: 141 targeted tests; validator 104/104; canonical notebook sạch;
  bốn Revision 8 probes đã pass; Qdrant giữ 572 points.
- Năm reviewer probes mới fail: missing totals, unknown attempt model, calls vượt
  frozen cap, final calibration wrong run/case được accept, và CLI-path final
  missing summary không recover.
- Attempt rows và Cell 15 chưa chứng minh exact journal linkage/distribution.
- Sau pure/read-only re-review đạt mới re-verify official prices và xin exact
  authorization cho 8 calibration + 24 generation + 24 judge calls. Không tạo
  user report, không cập nhật `Project_Status.md`, không commit/push; Phase 8
  tiếp tục đóng.

Handoff chi tiết, required changes và trình tự tiếp tục nằm trong
`reports/phase_7_retrieval_answer_evaluation_codex_review.md`, mục
`Hướng dẫn triển khai Revision 10`.
