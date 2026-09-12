# Full-corpus RAG Implementation Plan

```text
Status: approved by User 2026-09-11
Written Spec: approved 2026-09-11
Implementation authorization: Wave 1 only through active handoff
Runtime/live authorization: gated below
Sequential wave workflow amendment: approved by User 2026-09-11
```

## 1. Outcome

Triển khai approved
[Full-corpus RAG Written Spec](../specs/2026-09-11-full-corpus-rag-written-spec.md)
theo các wave nhỏ, mỗi wave có artifact, self-verification và independent review.
Kết quả cuối là pipeline full-corpus có locator/citation, hai retrieval
treatments, staged reranker/representation B, UI inline và full evaluation thật.

Plan không thay đổi Written Spec, không tự chọn winner/threshold và không mở
Agentic RAG. Mỗi cơ chế dưới đây phải có consumer hoặc acceptance cụ thể.

## 2. Quyền và ranh giới

Trước khi User duyệt Plan, không giao Implementer và không sửa runtime/data.
Sau approval, chỉ wave hiện hành trong `CURRENT_HANDOFF.md` được phép thực hiện.
Hoàn tất một wave phải bàn giao Reviewer; không tự bắt đầu wave tiếp theo.

Quyền mặc định sau Plan approval:

- được sửa code/config/tests/docs đúng wave đang active;
- được cài dependency đã liệt kê qua lockfile và chạy unit/integration tests;
- không Git commit/push/reset/clean;
- không đọc/in secrets; report không chứa key, header hoặc response nhạy cảm;
- không sửa raw corpus facts ngoài P7 authoring/correction đang active;
- Foods Golden V2/V3 và active Foods Qdrant collections luôn read-only;
- không notebook execution hoặc benchmark ngoài live gate;
- không cleanup/replacement collection nếu chưa có exact target approval.

Reviewer không chạy model/API/Qdrant/tests/frontend/notebook/benchmark theo
authority hiện hành. Reviewer kiểm source/diff/artifacts độc lập và dùng
Implementer execution evidence; User có thể cấp authority mới bằng văn bản.

### 2.1 Design package và closure bắt buộc cho từng wave

Plan này là roadmap/umbrella, không phải một lệnh triển khai liên tục. Trước mỗi
wave sau Wave 1, Reviewer phải dùng kết quả wave trước để soạn một design package
nhỏ nhưng đầy đủ:

1. cập nhật exact guide phase liên quan với dependency, target behavior,
   exclusions và trạng thái `proposed`;
2. exact wave spec/addendum cho behavior và data/public contracts;
3. exact wave implementation plan cho paths, thứ tự, tests/artifacts và stop
   condition;
4. exact Review Contract cho evidence, independent checks, severity và quyền;
5. User approval cho cả package trước khi tạo Implementer handoff.

Sau implementation, Implementer bàn giao report; Reviewer review/correction,
trình User closure rồi đồng bộ guide thành target/observed status. Handoff tiếp
theo quay về Reviewer design gate, không tự nhảy sang Implementer wave kế tiếp.
Không author chi tiết phụ thuộc như thể evidence wave trước đã tồn tại.

Wave 1 đã thỏa design gate bằng approved Written Spec, Plan, Review Contract,
phần full-corpus trong guide Phase 2 và exact Wave 1 implementation prompt. Mọi
wave sau vẫn chưa có implementation authorization.

Dependency order cho các package tiếp theo:

```text
Wave 1 / Phase 2 parser-locator closure
-> Wave 2.1 / Phase 3 dense+sparse representation design and implementation
-> Wave 2.2 / Phase 4 index schema+lifecycle design, then separate live gate
-> Wave 2.3 / Phase 5 retrieval+fusion+reranker design and implementation
-> Wave 3 / Phase 6 context+generation+API+UI, then separate live gate
-> Wave 4 / Phase 7 Golden P7, one approved partition at a time
-> Wave 5A / Phase 7 evaluator
-> Wave 5B / Phase 8 staged real benchmark and selection gates
-> Wave 6 / integrated documentation and final closure
```

Reviewer có thể gộp spec/plan của hai bước chỉ khi dependency đã có evidence và
User duyệt việc gộp; không gộp chỉ để giảm số gate.

## 3. Thiết kế triển khai tối thiểu

### 3.1 Corpus scope

`knowledge_base.root_dir` giữ `../knowledge-base-hue`. Include đúng:

```yaml
include_globs:
  - foods/**/*.md
  - heritages/**/*.md
  - festivals/**/*.md
  - performing_arts/**/*.md
  - travel/places/**/*.md
  - travel/services/**/*.md
  - travel/tickets/**/*.md
exclude_parts:
  - evaluation
  - _source-dumps
  - meta
```

Loại riêng hai file quản lý:

- `travel/services/services-research-and-entities-inventory.md`;
- `travel/tickets/tickets-research-and-entities-inventory.md`.

Section source-tracking hiện hành bị loại theo exact heading contract. Không
dùng heuristic loại cả section chỉ vì heading có từ “quản lý” hoặc “nguồn”.

### 3.2 File/runtime additions dự kiến

Giữ module hiện có khi phù hợp; chỉ tách module khi có một trách nhiệm rõ:

- `backend/config/full_corpus_conditions.json`: selector điều kiện nhỏ;
- `backend/ingestion/source_state.py`: LF/hash/build-record checks;
- `backend/ingestion/chunking/markdown_blocks.py`: block/span extraction;
- `backend/embedding/sparse.py`: deterministic sparse vocabulary/weights;
- `backend/llm/generator_openrouter.py`: concrete Qwen/OpenRouter client;
- `backend/api/errors.py`: typed public error envelope;
- `frontend/index.html`, `frontend/app.js`, `frontend/styles.css`: static UI,
  không Node/npm framework;
- full-corpus tests dưới `backend/tests/`;
- generated build records dưới ignored `data/full_corpus_builds/`.

Tên có thể điều chỉnh trong wave report nếu responsibility không đổi. Không tạo
provider/plugin framework, repository layer, event bus, migration engine hoặc
generic graph abstraction.

### 3.3 Retrieval constants cho comparison

Implementation dùng một contract cố định, khai báo trong config và report:

- metric cutoff: 10;
- candidate depth: 30 cho mỗi dense/sparse branch;
- RRF dùng rank bắt đầu từ 1 và `sum(1 / (60 + rank))`;
- deterministic tie-break cuối: internal chunk ID ascending;
- context output: tối đa 5 primary chunks;
- reranker nhận pre-rerank candidates theo cùng depth và trả ít nhất Top-10 để
  evaluation; context lấy Top-5.

Nếu source/API của library khiến một constant không thể áp dụng đúng, Implementer
dừng wave và báo trade-off; không thay số âm thầm.

### 3.4 Sparse representation

Sparse vectors tái sử dụng `scoring.bm25.tokenize`, `k1=1.5`, `b=0.75` và IDF
formula hiện hành. Vocabulary là các term corpus sắp xếp lexicographic rồi gán
index tuần tự. Document value là IDF nhân BM25 TF saturation; query giữ mỗi term
một lần với value 1.0 để sparse dot product bằng BM25 score. Build record giữ
identity/hash của vocabulary ở cấp build; không lặp vocabulary/model metadata
per-point. Query dùng đúng vocabulary/IDF của collection. Unknown terms bị bỏ;
không cập nhật vocabulary tại request time.

Baseline local BM25 dùng cùng tokenization contract nhưng chỉ chấm 30 dense
candidates. Native hybrid query dense và sparse độc lập, mỗi branch 30, rồi RRF.

## 4. Wave 1 — Discovery, parser, chunker và locator

Mục tiêu: tạo deterministic full-corpus preview, chưa embedding hoặc ghi Qdrant.

Implementation:

1. Thêm `markdown-it-py` với version/range hẹp vào `pyproject.toml` và `uv.lock`.
2. Mở rộng settings loader cho exact corpus scope và validation fail-closed.
3. Thay H2/400-character Foods chunker bằng Markdown block parser có source
   spans, heading path, list/table/blockquote support.
4. Thực hiện semantic grouping/splitting và representation A.
5. Resolve `full_corpus_conditions.json` theo exact file/path/type/text; mỗi
   selector phải match đúng một block.
6. Tạo `EvidencePart`/chunk schema, deterministic chunk ID/UUID5 helper.
7. Preview kiểm H1, empty chunks, duplicate IDs, exact spans, all-model tokenizer
   limits và gom toàn bộ blocking errors trước khi dừng.
8. Tạo source LF/hash/build-record utilities nhưng chưa ghi completion record.

Tests bắt buộc:

- discovery includes/excludes đúng năm domain và deterministic order;
- CRLF/CR normalization, Unicode offsets và repeated-text locator;
- intro trước H2, nested lists, tables, blockquotes, image-only lines;
- condition match success/missing/duplicate/mismatch;
- samples Mệ Kéo, Gia Lạc, Đại Nội, lịch trình biển, Ca Huế và dự toán;
- oversized group chặn toàn preview; không truncate/partial output;
- repeated run cho deep-equal chunks/IDs.

Deliverables:

- code/config/tests của Wave 1;
- preview artifact tĩnh chỉ chứa counts/errors/paths, không dump toàn corpus;
- implementation report ánh xạ acceptance → evidence;
- handoff Reviewer/final_review.

## 5. Wave 2 — Embedding, sparse index, Qdrant lifecycle và retrieval

Mục tiêu: triển khai components/index contract; mutation live chỉ ở gate 5B.

### Wave 2A — code và tests không live collection

1. Khai báo explicit dense candidates:
   `intfloat/multilingual-e5-small`,
   `intfloat/multilingual-e5-base` và
   `CODE4LIFEOFFICIAL/huydang-dek21-embedding`.
2. Kiểm model dimension/preprocessing thực; không truncate.
3. Tạo dense/sparse named-vector Qdrant schema và payload năm field.
4. Tạo deterministic sparse vocabulary/query encoder và build identity.
5. Thay resume/upsert-in-place bằng fresh-target guard; target non-empty bị từ
   chối trừ exact replacement mode đã được approve.
6. Build record chỉ được đánh complete sau point-count/schema/payload validation.
7. Implement baseline dense+BM25-local RRF và native dense/sparse RRF.
8. Implement finalist-only reranker/no-rerank behavior và overlong-pair skip.
9. Mọi component error fail closed; không fallback treatment.

Tests dùng fake/in-memory clients cho schema, vector/payload, fresh-target guard,
RRF/tie-break, sparse vocabulary stability, unknown terms, component failures và
reranker skip-whole-request. Không gọi model hoặc Qdrant live trong 2A.

### Gate 2B — fresh live candidate indexes

Trước write, Implementer nộp preflight:

- exact new collection names, model IDs/dimensions, representation và point count;
- Qdrant target-exists/empty checks;
- preview PASS và build-record destinations;
- lệnh sẽ chạy; xác nhận không target Foods;
- projected local resource use.

Reviewer kiểm tĩnh và User xác nhận exact targets. Sau đó Implementer mới build
ba A collections thật, verify schema/count/build records và bàn giao report.
Không chạy quality benchmark ở gate này.

## 6. Wave 3 — Context, Qwen generation, API/citations và static UI

### Wave 3A — code và tests

1. Thay character context budget bằng tokenizer-aware whole-chunk packing:
   context 16384, output reserve 2048, margin 512, Top-5.
2. Tạo concrete OpenRouter generator cho `qwen/qwen3.5-9b`:
   temperature 0, timeout 90, no automatic retry/failover, explicit upstream.
3. Tạo representation-B generator path với output cap 256, không đưa generated
   text vào `evidence_parts` hoặc citations.
4. Cập nhật grounded prompt cho response-local `[n]` và contradictory evidence.
5. Cập nhật `POST /api/chat` success/error schemas, citation validation và safe
   source whitelist theo Written Spec.
6. Startup kiểm build record/corpus freshness trước khi ready.
7. Serve static `frontend/` từ FastAPI: input/submit/loading, safe Markdown,
   keyboard citation focus, inline source cards và manual retry.
8. Không thêm sessions, streaming, drawer/modal, score/debug panel hoặc tools UI.

Tests dùng mocked provider:

- exact Qwen request profile và explicit upstream;
- token overhead/whole-chunk stop order/first-chunk error;
- B output separation và tokenizer fallback-to-A;
- citation valid/unknown/orphan/uncited-source cases;
- exact HTTP/error envelopes và no-evidence success;
- XSS-safe Markdown, duplicate-submit state, keyboard citation/source mapping;
- startup stale/missing/incomplete build behavior.

### Wave 3B — bounded live smoke

Sau 3A review, Implementer nộp exact upstream/model availability preflight và
bounded call list. User xác nhận paid live smoke. Chỉ chạy số call tối thiểu để
chứng minh OpenRouter request/response, pinning, representation-B schema và
one-shot answer/citation path; đây chưa là official benchmark.

## 7. Wave 4 — Full-corpus Golden P7

Thực hiện đúng thứ tự, mỗi partition là một handoff riêng:

1. `foods`;
2. `heritages`;
3. `festivals`;
4. `performing_arts`;
5. `travel_places`;
6. `travel_services`;
7. `travel_tickets`.

Mỗi working file nằm tại `evaluation/golden_full_corpus_authoring.jsonl` của
nhánh. Row có `question`, `keywords`, `reference_answer`, `category`,
`partition`. Implementer self-review schema, corpus support, keywords,
naturalness, uniqueness và provisional category.

Reviewer và User đọc mọi case, quyết định keep/correct/reclassify/delete. Chỉ sau
User closure partition mới chuyển partition kế tiếp. Không author ahead, padding
quota hoặc merge sớm. Web chỉ giúp cách viết tự nhiên, không thêm fact.

Sau P7 closure:

1. validate all inputs;
2. merge theo P7 order, strip `partition`, reject duplicate question;
3. deterministic shuffle seed 42;
4. ghi `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`;
5. đề xuất 10 smoke rows, mỗi P7 ít nhất một, rồi chờ User/Reviewer approval;
6. tạo smoke deep-equal, giữ relative order.

## 8. Wave 5 — Evaluator và staged real benchmark

### Wave 5A — evaluator implementation

1. Loader canonical bốn field và category vocabulary bảy nhãn.
2. MRR@10, nDCG@10, Keyword Coverage@10 per case.
3. `gpt-5.4-mini` judge qua OpenAI: temperature 0, output cap 600, một
   prompt/case, ba integer scores + feedback.
4. Macro-average overall/category; không composite/micro.
5. Empty successful results dùng 0/1 đúng contract.
6. Technical/timeout/judge/schema failure đánh run `incomplete`; không partial
   official aggregate.
7. Output report ghi config, counts, errors và exact per-case/aggregate results;
   không ghi secrets hoặc raw provider internals.

Tests phải kiểm formulas, schema, deterministic ordering, failure semantics,
judge output validation và không công bố aggregate khi incomplete.

### Wave 5B — paid/live benchmark gate

Trước mỗi paid stage, Implementer nộp:

- exact canonical case count;
- exact configs/collections/upstream/concurrency;
- projected calls/tokens và current provider cost estimate;
- commands, output paths, resume/rerun policy cho failed cases;
- xác nhận targets read-only/write và không đụng Foods.

User xác nhận paid stage trước execution.

Run order:

1. A retrieval: 3 dense models × baseline/native hybrid, full Golden.
2. Reviewer báo exact metrics và đề xuất retrieval/model finalists; User duyệt.
3. Finalists: no-rerank vs one MiniLM reranker.
4. Reviewer đề xuất finalists cho controlled representation A/B; User duyệt.
5. Tạo B thật chỉ cho finalists, fresh indexes mới, rồi full A/B retrieval.
6. End-to-end finalist generation + OpenAI judge trên full Golden.
7. Rerun mọi technical failure; chỉ complete runs có official aggregate.
8. Reviewer đề xuất winner, runtime cutover và 1–3 collections cần giữ; User
   duyệt riêng trước switch/replacement/cleanup.

Không dùng smoke làm official result. Không đặt metric threshold/composite hoặc
winner trước evidence.

## 9. Wave 6 — Documentation và final handoff

Sau khi các gate cần thiết hoàn tất:

- cập nhật settings/comments và canonical guides theo behavior thực;
- ghi exact collections/profiles/results và các mục `Not verified`;
- không sửa report lịch sử;
- implementation report phân biệt task changes với pre-existing worktree state;
- `git diff --check` sạch;
- `CURRENT_HANDOFF.md` target Reviewer/final_review.

Không tự ghi `approved/completed`; Reviewer review và User closure là gate riêng.

## 10. Verification commands dự kiến cho Implementer

Exact commands được khóa trong từng wave handoff. Baseline tối thiểu:

```bash
uv run python -m pytest backend/tests -q --tb=short
git diff --check
```

Wave có frontend phải thêm bounded static/UI contract checks. Wave có Qdrant/API
phải dùng exact approved commands/targets và lưu machine-readable results dưới
`evaluation/results/` hoặc task report path; không sửa notebook outputs.

## 11. Change control

Implementer dừng và trả Reviewer nếu cần:

- đổi Written Spec hoặc metric semantics;
- thêm dependency/framework ngoài `markdown-it-py`;
- đổi provider/model, tokenizer limit hoặc generation budget;
- mutate target không nằm trong approved preflight;
- tăng paid calls ngoài estimate được User xác nhận;
- thêm fallback/retry, agentic behavior, session/memory hoặc metadata field.

Bug fix nội bộ không đổi contract được phép trong active wave và phải ghi report.
Mọi scope expansion cần User approval trước implementation.

## 12. Plan approval effect

User đã duyệt Plan ngày 2026-09-11; Reviewer đã kích hoạt **Wave 1** trong
`CURRENT_HANDOFF.md` và giao Implementer. Các wave sau vẫn cần Reviewer closure
của wave trước; live Qdrant/API/paid gates cần exact preflight/confirmation như
đã nêu. Plan approval không tự cấp quyền cleanup, cutover hoặc Agentic RAG.
