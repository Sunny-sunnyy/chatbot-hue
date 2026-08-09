# Phase 7: Đánh giá retrieval và câu trả lời

## Mục tiêu và giá trị cho người dùng

Phase 7 tạo evaluation harness tái lập cho 104 câu hỏi tiếng Việt: đo retrieval trước, sau đó đánh giá answer quality bằng rubric có cấu trúc. Phase này biến cảm nhận thủ công thành bằng chứng đủ để Phase 8 so sánh model và pipeline.

## Trạng thái

```text
Status: not_ready
Brainstorming level: Level 3 - deep
Owner: Codex Reviewer
Implementer: DeepSeek after Phase 6 approval and Phase 7 readiness
```

## Dependency

- Phase 5 retrieval profiles và Phase 6 generator/API đã được approve.
- Test corpus có 104 JSONL rows tại `knowledge-base-hue/foods/evaluation/tests.jsonl`.
- Mỗi row hiện có `question`, `keywords`, `reference_answer`, `category`.
- Dataset chưa có canonical `relevant_sources` hoặc `relevant_chunk_ids`; đây là design decision bắt buộc trước proper retrieval metrics.
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
backend/evaluation/run_retrieval.py
backend/evaluation/run_answers.py
backend/evaluation/results/.gitkeep
backend/tests/test_evaluation_loader.py
backend/tests/test_evaluation_metrics.py
backend/tests/test_answer_judge.py
notebooks/06_evaluation.ipynb
```

## Test-case contract

Current shape:

```python
{
    "question": "Quán bún bò Mệ Kéo nằm ở đâu?",
    "keywords": ["Mệ Kéo", "Bạch Đằng"],
    "reference_answer": "...",
    "category": "direct_fact",
}
```

Loader requirements:

- đúng 104 non-empty rows cho baseline dataset version;
- unique stable case ID được derive deterministically hoặc thêm explicit field sau approval;
- non-empty question/reference/category;
- keywords là list non-empty strings;
- invalid row fail với line number, không skip âm thầm;
- source file chỉ read-only trong evaluation run;
- dataset checksum/version được ghi trong run metadata.

## Retrieval ground truth bắt buộc

Recall, MRR và nDCG chỉ có ý nghĩa khi relevance definition rõ. Brainstorming phải chọn một hướng và ghi limitation:

1. Gold `relevant_sources`/`relevant_chunk_ids` do người dùng review: chính xác và được khuyến nghị, nhưng cần annotation effort.
2. Deterministic keyword match trên title/text: nhanh và tương thích dữ liệu hiện tại, nhưng chỉ là lexical relevance proxy.
3. LLM relevance labels: linh hoạt nhưng tăng cost/variance, không phù hợp làm primary ground truth ban đầu.

Khuyến nghị canonical là gold relevant sources cho primary metrics và keyword coverage làm diagnostic. Nếu chưa annotation đủ, có thể chạy keyword-proxy baseline nhưng report phải gọi đúng là proxy; không tuyên bố proper semantic Recall/MRR/nDCG.

## Retrieval metrics contract

Với relevance judgments đã chốt:

- `Recall@k`: tỷ lệ relevant items trong top-k.
- `MRR`: reciprocal rank của relevant item đầu tiên, mean qua cases.
- `nDCG@k`: ranking quality với binary/graded relevance đã định nghĩa trước.
- `keyword_coverage`: diagnostic tỷ lệ expected keywords trong retrieved title/text.
- latency: wall-clock retrieval latency; report median và p95 ngoài mean.

Metric tests phải bao phủ:

- no relevant result;
- first-rank relevant;
- multiple relevant results;
- fewer than k results;
- duplicate retrieved IDs;
- empty relevant set theo explicit reject/exclude policy;
- overall và per-category aggregate.

Không tune pipeline trên test result rồi báo cùng run như unbiased evaluation. Mọi config change tạo run ID mới.

## Retrieval run protocol

```text
load and validate 104 cases
  -> freeze dataset checksum
  -> freeze collection/model/profile/config
  -> retrieve each question without generation
  -> record ranked IDs/sources/scores and latency
  -> compute per-case metrics
  -> aggregate overall and per category
  -> atomically write JSONL and summary metadata
  -> append summary/decision to benchmark ledger
```

Retrieval evaluation không gọi answer model hoặc judge, nên chạy toàn bộ 104 cases cho mỗi valid profile/model comparison.

## Answer generation protocol

Answer evaluation bắt đầu bằng stratified subset theo `category`. Exact subset size được chốt trước live run dựa trên category distribution và cost estimate. Full 104 answer generation/judge chỉ chạy khi người dùng phê duyệt riêng.

Tách artifacts:

```text
generation JSONL: query, reference, generated answer, used sources, model/config, latency, usage
judge JSONL: generation run ID, rubric version, scores, concise feedback, judge model, latency, usage
```

Nhờ đó có thể re-judge frozen answers mà không trả thêm phí generation.

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

Judge nhận question, reference, generated answer và bounded evidence. Không nhận chain-of-thought, API headers hoặc unrelated cases. Rubric version và prompt hash được ghi.

Một retry tối đa chỉ dành cho timeout/invalid structured output nếu được chốt; không retry để tìm điểm đẹp hơn. Failed judge row được giữ, không drop khỏi denominator âm thầm.

## Judge quality controls

- Unit tests dùng fake structured responses.
- Trước batch trả phí, chạy approved calibration sample có clear good/bad answers.
- User/Codex review sample feedback để phát hiện rubric drift.
- Judge `gpt-5.4-mini` tách khỏi answer model `gpt-5.4-nano`.
- Nếu re-judge sample, giữ cả hai runs thay vì overwrite.

## Result artifact schema

Mỗi retrieval JSONL record có:

```text
run_id
timestamp_utc_plus_7
dataset_path
dataset_checksum
case_id
category
question
profile
embedding_provider
embedding_model
collection_name
retrieved_items
metrics
latency_ms
status
error_type
```

Answer/judge record thêm generation model, judge model, reference, generated answer, used sources, rubric version, usage và cost. Không lưu secret, raw header, chain-of-thought hoặc full SDK object.

Artifact write dùng temp file + atomic rename hoặc cơ chế tương đương. Resume chỉ skip record cùng run ID/case ID và status complete.

## Brainstorming Level 3 bắt buộc

Codex và người dùng phải chốt:

1. Gold relevance annotation hay keyword-proxy baseline, cùng limitation.
2. Các giá trị k cho Recall/MRR/nDCG.
3. Aggregate và primary selection metric.
4. Stratified subset size và category allocation.
5. Judge rubric, pass threshold và retry policy.
6. Maximum OpenAI calls/cost cho calibration, subset và full run.
7. Artifact naming, overwrite/resume và retention policy.

Mỗi decision phải giữ test corpus/config frozen để Phase 8 so sánh công bằng.

## Nhiệm vụ của DeepSeek Implementer

- TDD metrics bằng known rankings trước khi nối runtime.
- Không copy trực tiếp `rag_old` evaluator; chỉ dùng metric/rubric concepts và sửa provider/schema inconsistencies.
- Mock generator/judge trong default tests.
- Không tự chạy live answer/judge.
- Không cập nhật ledger bằng estimated/fabricated metrics.
- Report exact commands, artifact paths, completed/failed counts và approval.

## Nhiệm vụ của Codex Reviewer

- Audit ground truth, metric math và denominator policy.
- Recompute sample cases độc lập.
- Kiểm tra dataset/config checksum và artifact completeness.
- Calibrate judge sample, audit actual model/cost và failed rows.
- Không approve proxy metric bị mô tả như gold relevance.

## Notebook bắt buộc

`notebooks/06_evaluation.ipynb` phải:

- import evaluation modules;
- giải thích ground truth và metrics bằng tiếng Việt;
- minh họa hand-calculated fake rankings mặc định;
- có opt-in cells cho local retrieval artifacts;
- live generation/judge cells guard riêng;
- không lưu 104 answers, raw payload hoặc secrets;
- committed outputs rỗng và `execution_count=null`.

## Tests và validation dự kiến

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile evaluation/test_loader.py evaluation/metrics.py evaluation/retrieval_eval.py evaluation/answer_eval.py evaluation/run_retrieval.py evaluation/run_answers.py
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_evaluation_loader.py tests/test_evaluation_metrics.py tests/test_answer_judge.py -q --tb=short
```

Offline/mock gate pass trước external run. Retrieval command cần local Qdrant readiness. Answer/judge command cần user approval và cost estimate trước execution.

## Security, reliability và performance gates

- No key/header/raw SDK object trong artifacts.
- Bounded concurrency, timeout và call count.
- Failed rows retained với safe error type.
- Atomic output và resumable run.
- Dataset/config checksum chống so sánh nhầm.
- Judge prompt chỉ nhận case hiện tại.
- Full 104 paid run không bao giờ là default.

## Tiêu chí phê duyệt Phase 7

- 104 cases load strict và dataset version được ghi.
- Relevance definition minh bạch; proxy không bị gọi là gold metric.
- Metrics pass hand-calculated tests.
- Full retrieval run tạo complete JSONL và summary.
- Approved answer subset/judge dùng đúng model/rubric, có cost/failure evidence.
- Notebook an toàn, outputs sạch.
- Ledger chỉ ghi kết quả thực.

## Reports và cập nhật trạng thái

```text
reports/phase_7_retrieval_answer_evaluation_implementation_report.md
reports/phase_7_retrieval_answer_evaluation_codex_review.md
reports/hue_foods_rag_benchmark.md
```

Codex cập nhật `Project_Status.md` sau approval, không phải sau partial live run.

## Bước tiếp theo

Sau Phase 7 approval, Phase 8 chạy controlled benchmark local-first rồi remote, chọn winner và rebuild final active collection.
