# Phase 5: Retrieval profiles, reranking và context

## Mục tiêu và giá trị cho người dùng

Phase 5 tạo retrieval pipeline local có ba chế độ so sánh được: dense semantic
baseline, dense kết hợp lexical BM25 và hybrid có CrossEncoder reranking. Mỗi
profile chỉ khởi tạo và chạy đúng component cần thiết, nhờ đó người dùng có thể
quan sát giá trị gia tăng và chi phí của từng stage trước khi đánh giá chất
lượng chính thức ở Phase 7–8.

## Trạng thái

```text
Status: approved
Owner: Codex Reviewer
Implementer: DeepSeek
```

> **Lưu ý governance hiện hành:** Các đoạn bên dưới mô tả implementation và
> test contract lịch sử của Phase 5, bao gồm fake dependencies, offline tests
> và per-run approval. Chúng không áp dụng cho công việc mới. Shared governance
> hiện hành cấm mock/fake và cho phép real online/API execution trong approved
> scope. Coordinated simplicity review Phase 4–5 đã hoàn tất và được user xác
> nhận ngày `2026-08-25 +07`.

> **Quyết định coordinated simplification ngày 2026-08-25 +07:** Phase 4 bỏ
> stored sparse vectors khỏi active Qdrant baseline; trong cùng implementation
> scope, Phase 5 nhận lexical tokenization về BM25 ownership. `SparseEmbedder`
> chỉ bị xóa sau khi không còn runtime/test/notebook consumer. BM25 và
> CrossEncoder behavior của ba canonical profiles phải được bảo toàn.

> Phase 4 và phần Phase 5 liên quan trực tiếp được brainstorming chung. Test
> policy ưu tiên pure behavior và real guarded-system evidence; không có test
> count target, mock/fake system evidence hoặc test chỉ bảo vệ implementation
> mechanics không có user-visible need.

> Qdrant client không có module cache: API startup hoặc ingestion composition
> root tạo một client và truyền xuống. CrossEncoder instance cũng không có app
> cache; thư viện model cache chỉ tái sử dụng downloaded files bình thường.
>
> Thiết kế coordinated Phase 4–5 đã được user duyệt ngày `2026-08-25 +07` tại
> `docs/superpowers/specs/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-design.md`.
> Implementation, independent review và user confirmation đã hoàn tất. Approval
> đó không tự cho phép cutover/delete collection, commit hoặc push.

Thiết kế trong guide này đã được người dùng phê duyệt ngày 2026-08-12 +07.
DeepSeek đã bàn giao correction revision 3; Codex technical review đạt và người
dùng đã xác nhận final approval ngày 2026-08-12 +07.

## Dependency đã đạt

- Phase 4 có status `approved`.
- Active collection hiện tại `hue_foods_e5_small_384` có 572 points, named dense
  vector 384 chiều cosine và sparse index lịch sử. Target sau approved Phase 4–5
  simplification là blue-green cutover sang dense-only candidate
  `hue_foods_e5_small_384_dense`; mọi active config transition vẫn cần user
  approval riêng.
- Point payload giữ `embedding_model` để xác minh vector-space identity;
  `embedding_dimension` bị loại vì dense schema/config đã là nguồn chuẩn.
- Query embedder dùng `intfloat/multilingual-e5-small`, prefix `query: ` và cùng
  dimension với indexed document embeddings.
- Canonical corpus gồm 572 chunks với stable `chunk_id` và curated payload.
- `cross-encoder/ms-marco-MiniLM-L-6-v2` đã chạy thành công trên máy local trong
  dự án `llm_rag`; điều này là resource evidence, không phải quality evidence
  cho tiếng Việt hoặc Hue Foods.

## Phạm vi đã phê duyệt

- Dense Qdrant retriever dùng named vector `dense`.
- Corpus-scoped Python BM25 với `k1=1.5`, `b=0.75`.
- Min-max normalization và weighted fusion deterministic.
- Profile router/service cho ba profile canonical.
- Local MiniLM CrossEncoder reranker chạy CPU.
- Whole-chunk ContextBuilder trả bounded labeled context string.
- Profile-scoped startup/cache lifecycle.
- Typed errors và safe retrieval debug metadata.
- Unit/integration tests offline và notebook runtime-real.

Không implement OpenRouter reranker adapter trong Phase 5. Remote reranking,
native Qdrant sparse retrieval, tuning grid, retrieval metrics và winner
selection được hoãn sang Phase 7–8.

## Kiến trúc component

| Component | Trách nhiệm | Không chịu trách nhiệm |
|---|---|---|
| `DenseRetriever` | Embed query, query Qdrant dense và chuẩn hóa kết quả | BM25, fusion, reranking, context |
| `BM25` | Fit corpus statistics và score exact lexical matches | Query Qdrant hoặc normalize score |
| `HybridRetriever` | Score BM25, normalize, fusion và giữ top candidates | Load model hoặc build context |
| `CrossEncoderReranker` | Score 10 query-document pairs và trả top 5 | Retrieval candidate generation |
| `RetrievalService` | Route profile, giữ đúng concrete components và runtime status | API error mapping hoặc generation |
| `ContextBuilder` | Ghép whole chunks thành labeled context string trong budget | Retrieval hoặc prompt generation |

Mỗi component nhận dependencies qua constructor hoặc input rõ ràng. Verification
dùng pure behavior tests hoặc actual guarded Qdrant/models; dependency injection
không phải lý do để tạo fake implementation.

## Ba retrieval profiles canonical

### `dense_only`

```text
query
  -> validate
  -> E5 query embedding
  -> Qdrant dense top 10
  -> deterministic ordering
  -> whole-chunk context, tối đa 5 documents / 3.000 characters
```

Không scroll corpus, fit/call BM25 hoặc load/call reranker. Không tạo BM25,
hybrid hoặc rerank score fields.

### `hybrid_no_rerank`

```text
query
  -> validate
  -> E5 query embedding
  -> Qdrant dense top 30
  -> BM25 score trên 30 dense candidates
  -> normalize dense và BM25 độc lập
  -> fusion 0.6 dense + 0.4 BM25
  -> deterministic top 10
  -> whole-chunk context, tối đa 5 documents / 3.000 characters
```

BM25 fit trên toàn bộ 572 corpus texts, nhưng chỉ score 30 dense candidates ở
request path. Stored sparse vector không được query.

### `hybrid_rerank`

```text
query
  -> cùng hybrid pipeline và cùng pre-rerank top 10
  -> local MiniLM CrossEncoder score 10 pairs
  -> deterministic top 5
  -> whole-chunk context, tối đa 5 documents / 3.000 characters
```

Profile này giữ nguyên collection, dense candidate depth, BM25 và fusion config
của `hybrid_no_rerank`. Chỉ stage reranker được thêm vào.

## Retrieval depth và context baseline

| Tham số | Giá trị |
|---|---:|
| Dense output `top_k` | 10 |
| Hybrid dense candidate depth | 30 |
| Hybrid output trước rerank | 10 |
| CrossEncoder input depth | 10 |
| CrossEncoder output | 5 |
| Context max documents | 5 |
| Context max characters | 3.000 |

Candidate multiplier là 3. Rerank depth 20/30, candidate-depth grid và context
budget alternatives chỉ được mở ở Phase 8 khi có hypothesis và evaluation
evidence rõ.

## BM25 contract

Baseline:

```text
k1 = 1.5
b = 0.75
```

- Fit trên đủ 572 non-empty active corpus chunk texts, không fit mỗi request.
- Query/document dùng chung một lexical `tokenize()` contract do BM25/scoring
  ownership quản lý; retrieval không import từ embedding package.
- Average document length chỉ tính non-empty documents.
- Query terms được deduplicate trước khi cộng BM25 term contributions.
- Term ngoài vocabulary hoặc không xuất hiện trong document đóng góp `0.0`.
- Empty query bị service reject; empty document không được đưa vào corpus hoặc
  candidate result.
- Output phải là finite float.

## Normalization và fusion contract

Dense cosine và BM25 khác scale nên không được cộng raw như `llm_rag`.
Min-max normalization chạy độc lập trên cùng 30-candidate set:

```text
normalized = (score - min_score) / (max_score - min_score)
hybrid_score = 0.6 * normalized_dense + 0.4 * normalized_bm25
```

Invariants:

- Input score phải finite.
- Khi `max_score == min_score`, toàn bộ normalized score của signal đó bằng
  `0.0`; signal không phân biệt được candidates nên không ảnh hưởng ranking.
- Weights phải finite, không âm và tổng bằng `1.0` trong tolerance.
- Sort theo final score giảm dần, sau đó stable `chunk_id` tăng dần.
- Grid `0.8/0.2`, `0.6/0.4`, `0.4/0.6` được hoãn sang Phase 8; Phase 5 không
  tuning weights.

## RetrievedDocument và score contract

Mọi profile trả `list[RetrievedDocument]`. `score` luôn là final score của
stage cuối thực sự chạy:

| Profile | `RetrievedDocument.score` |
|---|---|
| `dense_only` | Raw Qdrant cosine score |
| `hybrid_no_rerank` | Normalized weighted fusion score |
| `hybrid_rerank` | CrossEncoder rerank score |

Safe metadata allowlist:

```text
source
title
section
category
subcategory
chunk_type
chunk_id
retrieval_profile
embedding_model
reranker_model
retrieval_rank
dense_score
normalized_dense_score
bm25_score
normalized_bm25_score
hybrid_score
rerank_score
```

Score/model fields chỉ tồn tại khi stage tương ứng thực sự chạy. Không tạo giá
trị giả hoặc `null` placeholder. Phase 6 chỉ serialize explicit allowlist này,
không trả nguyên Qdrant metadata dictionary.

Không đưa query gốc, full context, absolute path, exception detail, config
dump, headers, credentials hoặc provider payload vào debug metadata.

## Reranker contract

Interface tối thiểu:

```python
class BaseReranker:
    @property
    def model_id(self) -> str: ...

    def rerank(
        self,
        query: str,
        documents: list[RetrievedDocument],
        top_k: int,
    ) -> list[RetrievedDocument]: ...
```

Local baseline:

```text
model: cross-encoder/ms-marco-MiniLM-L-6-v2
device: cpu
input depth: 10
output top_k: 5
```

Invariants:

- Empty documents trả `[]` mà không load/call model.
- Query rỗng bị service reject trước reranker.
- Score count phải bằng document count và mọi score phải finite.
- Output chỉ chứa input documents, không duplicate hoặc foreign document.
- Không mutate input list hoặc input metadata; output dùng result objects mới.
- Tie-breaking theo rerank score giảm dần rồi `chunk_id` tăng dần.
- `reranker_model` ghi actual local model ID.

Model chủ yếu train trên English/MS MARCO nên chỉ là local latency baseline.
Phase 5 không tuyên bố model này tốt cho tiếng Việt.

## Local latency và resource gate

- Profile `hybrid_rerank` load/download MiniLM thật khi cần trong approved run;
  hai profile khác không load model.
- Reranker behavior cần evidence từ MiniLM thật; pure ordering/validation
  logic có thể được test trực tiếp không qua fake scorer.
- Real validation có một warm-up không tính vào kết quả.
- Sau warm-up, đo 20 lượt, mỗi lượt rerank đúng 10 pairs trên CPU.
- p95 rerank latency phải không quá 3 giây.
- Cold model-load time được đo và ghi riêng, không trộn vào query latency.
- Nếu không đạt gate, Phase 5 chuyển `changes_requested` hoặc ghi blocker; không
  tự đổi model, depth hoặc device.

## ContextBuilder contract

ContextBuilder nhận ranked documents sau stage cuối và trả thẳng context string:

```python
def build(documents) -> str:
    ...
```

Rules:

- Tối đa 5 documents và 3.000 characters.
- Character budget tính cả source label và separator.
- Chỉ thêm whole chunk; nếu chunk kế tiếp không vừa thì dừng.
- Không truncate bảng, câu hoặc metadata nguồn để lấp đầy budget.
- Bỏ empty text, giữ rank order và không mutate documents.
- Empty input hoặc không có non-empty chunk trả `""`.
- Mỗi block chỉ có nhãn thứ tự, `title`, `section` và whole chunk content; không
  có `chunk_id`, file path, score, rank metadata hoặc parallel source list.
- Context chỉ chứa curated evidence và safe labels, không chứa debug payload
  hoặc secrets.

Corpus Hue Foods có chunk thường tối đa 400 ký tự; bảng là atomic và bảng dài
nhất đã xác minh ở Phase 2 là 927 ký tự. Whole-chunk policy vì vậy giữ cấu trúc
bảng mà vẫn cho phép khoảng 3–5 evidence trong baseline budget.

## Startup và runtime status

Service initialization theo active profile:

```text
inspect exact collection/schema/count/model/dimension
  -> dense_only: create dense retriever only
  -> hybrid_no_rerank: bounded scroll 572 payloads -> fit BM25 once
  -> hybrid_rerank: same hybrid initialization -> load MiniLM once
  -> construct RetrievalService directly with small immutable runtime status
```

Runtime status chỉ gồm dữ liệu có consumer thật:

```text
collection_name
point_count
embedding_model
embedding_dimension
active_profile
bm25_ready
reranker_ready
```

Lifecycle rules:

- Scroll theo bounded batches, `with_vectors=False`, chỉ lấy safe payload fields.
- Batch size là constant nội bộ 128; không có settings key, function override
  hoặc test chỉ kiểm tuning seam này.
- Xác minh đúng 572 unique `chunk_id` và non-empty text.
- BM25 và reranker giữ immutable trong vòng đời service.
- Collection/config thay đổi yêu cầu restart; không tự refit giữa requests.
- Không tạo corpus/config fingerprint hoặc `verify_snapshot()` vì production
  runtime không có consumer cho cơ chế staleness audit này.
- Không thêm persistent cache artifact trong Phase 5.
- Optional component failure không làm profile khác âm thầm đổi semantics.

## Failure policy và typed errors

Phase 5 dùng fail-explicit policy:

| Điều kiện | Kết quả |
|---|---|
| Query rỗng/whitespace | `InvalidQueryError` |
| Profile hoặc config sai | `RetrievalConfigurationError` |
| Required component missing hoặc startup corpus invalid | `ComponentNotReadyError` |
| Embedder, Qdrant hoặc model failure | `RetrievalDependencyError` |
| Retrieval chạy thành công nhưng không có candidate | `[]` |

Không catch exception rộng rồi trả `[]`. Không tự chuyển profile và không silent
fallback. `dense_only` vẫn hoạt động khi BM25/reranker chưa được khởi tạo vì nó
không phụ thuộc các component đó. Phase 6 chịu trách nhiệm map typed errors sang
API response.

Error message/log không được chứa query nguyên văn, context, credentials, raw
provider payload hoặc private configuration.

## Files được phép tạo hoặc sửa

```text
backend/config/settings.yaml
backend/config/README_config.md
backend/core/schema.py
backend/core/startup.py
backend/retrieval/dense_retriever.py
backend/retrieval/hybrid_retriever.py
backend/retrieval/service.py
backend/retrieval/context_builder.py
backend/scoring/bm25.py
backend/reranking/cross_encoder.py
backend/tests/test_bm25.py
backend/tests/test_retrieval_service.py
backend/tests/test_reranker.py
backend/tests/test_context_builder.py
backend/tests/test_startup.py
notebooks/05_retrieval_profiles.ipynb
reports/phase_5_retrieval_profiles_reranking_implementation_report.md
reports/hue_foods_rag_benchmark.md
```

Không tạo `backend/reranking/openrouter_reranker.py` trong Phase 5. Coordinated
implementation chỉ được chạm Phase 4 Qdrant schema/ingestion và Phase 5 lexical
ownership đã duyệt; không đổi embedding model/dimension, retrieval profile
semantics, generation, API hoặc frontend. Active collection contents vẫn không
được mutate nếu chưa có approval riêng.

## Cấu hình baseline

Giữ config hiện có:

```text
retrieval.top_k = 10
retrieval.candidate_multiplier = 3
retrieval.score_threshold = 0.0
retrieval.dense_weight = 0.6
retrieval.bm25_weight = 0.4
reranking.model = cross-encoder/ms-marco-MiniLM-L-6-v2
reranking.device = cpu
reranking.top_k = 5
```

Giữ context limits hiện có. Startup scroll batch là constant 128 trong code;
không thêm tuning grid hoặc speculative knobs.

## Nhiệm vụ của DeepSeek Implementer

1. Move lexical tokenizer vào BM25 ownership; giữ self-contained BM25 corpus
   statistics và normalization, kiểm tra bằng known corpus.
2. Implement dense/hybrid retrievers và verify bằng guarded Qdrant/E5 thật.
3. Implement profile routing, score metadata và typed errors.
4. Implement một concrete CrossEncoder reranker và verify bằng MiniLM thật.
5. Implement whole-chunk ContextBuilder trả labeled context string.
6. Implement profile-scoped startup lifecycle và small runtime status.
7. Tạo notebook runtime-real và implementation report.
8. Chạy smallest relevant tests trước, sau đó full backend regression.
9. Chạy real guarded Qdrant/model validation trong approved scope; chỉ
   active mutation/destructive transition cần approval riêng.

Không copy nguyên code `llm_rag`. Đặc biệt không copy raw-score fusion, broad
exception-to-empty behavior, eager all-component startup, input mutation hoặc
ContextBuilder không tính separator vào budget.

## Notebook bắt buộc

`notebooks/05_retrieval_profiles.ipynb` phải:

- import `RetrievalService` và `ContextBuilder` từ backend;
- giải thích ba profiles bằng tiếng Việt;
- Run All build cả ba profile bằng Qdrant/E5/MiniLM thật; không
  có fake dependency hoặc config-file mutation;
- hiển thị score fields đúng với từng stage và whole-chunk bounded context;
- không gọi OpenRouter hoặc bất kỳ paid API nào;
- committed outputs rỗng và mọi `execution_count=null`.

## Tests và validation dự kiến

```bash
cd backend
uv run python -m py_compile core/startup.py retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py reranking/cross_encoder.py
uv run pytest tests/test_bm25.py tests/test_retrieval_service.py tests/test_reranker.py tests/test_context_builder.py tests/test_startup.py -q --tb=short
uv run pytest tests/ -q --tb=short
```

Required test evidence:

- BM25 known corpus, average document length và empty document behavior.
- Min-max normal/constant/non-finite cases và weight validation.
- Candidate depth/output depth chính xác cho từng profile.
- Profile không gọi stage không sử dụng.
- Score fields chỉ xuất hiện khi stage đã chạy.
- Deterministic ties theo `chunk_id`.
- Reranker score count, finite score, duplicate/foreign output và no mutation.
- Context whole-chunk budget tính cả labels/separators, giữ document order và
  trả empty string khi không có usable chunk.
- Startup bounded scroll, 572 unique IDs, small runtime status và profile-scoped
  loading.
- Typed errors không bị chuyển thành `[]`.

## Real local validation cần approval riêng

Sau offline tests, reviewer/implementer chỉ chạy khi user cho phép rõ:

- Qdrant read-only probes trên active collection; không reset/reindex/mutate.
- Representative fixed queries lấy từ mỗi category của bộ 104 câu hỏi.
- Cùng query và collection cho cả ba profiles.
- Chỉ kiểm tra contract, non-empty evidence, stable metadata và latency; không
  dùng probes để tuning hoặc tuyên bố quality winner.
- MiniLM warm-up một lượt, đo 20 lượt rerank 10 pairs, p95 không quá 3 giây;
  cold-load time ghi riêng.

Model download/load/predict failure phải được ghi đúng và fail explicit; không
fallback, skip hoặc suy diễn pass. Approved implementation không cần approval
riêng cho từng download/run.

## Hypothesis, metrics và stop conditions

| Hypothesis | Evidence phân biệt | Stop condition Phase 5 |
|---|---|---|
| Dense E5 là baseline vận hành | Contract tests và real probes nếu được phép | Dense profile deterministic, trả valid documents hoặc typed error |
| BM25 bổ sung exact lexical signal | Known-corpus tests và stage metadata | BM25/fusion đúng công thức; chưa kết luận quality delta |
| MiniLM đủ nhanh làm local latency baseline | 20-run CPU latency sample | p95 rerank 10 pairs ≤ 3 giây |
| Whole chunks giữ evidence/source integrity | Context budget tests | Không cắt chunk/bảng, budget và order đúng |

Phase 5 dừng khi contract tests đạt, ba profiles chạy đúng stage, context giữ
source identity, latency gate đạt nếu real validation được phép và không có
silent fallback. Nếu hybrid/reranker có vẻ kém, ghi limitation và chuyển sang
Phase 7–8; không tuning vô hạn trong Phase 5.

## Security, reliability và performance gates

- Không log query nguyên văn, full context, credentials, provider headers hoặc
  raw model payload.
- Default tests/notebook không cần network, secrets, Qdrant hoặc paid API.
- Candidate depth, scroll batch, reranker pairs và context đều bounded.
- Không repeated model load hoặc corpus fit trong request path.
- Không mutate collection, chunks hoặc retrieved input objects.
- Không silent profile/model fallback.
- Benchmark ledger chỉ ghi actual provider/model/profile và evidence đã chạy;
  không ghi estimated results vào bảng actual.

## Tiêu chí technical review

- Ba profiles có semantics đúng và tests độc lập.
- Query E5 dùng đúng prefix/model/dimension của Phase 3–4.
- Hybrid dùng normalized dense + Python BM25, không misleading sparse claim.
- Local MiniLM chạy CPU và đạt latency gate trong real validation.
- Context string whole-chunk, labeled, bounded và deterministic.
- Typed failures rõ, không biến dependency error thành empty retrieval.
- Notebook an toàn và implementation report đầy đủ.
- Không remote reranker, live API, reindex, tuning grid hoặc winner claim.

Technical review đạt giữ phase ở `under_review`. Phase 5 chỉ `approved` sau khi
người dùng đọc user report và xác nhận notebook/kết quả.

## Reports và benchmark

Current coordinated simplicity evidence:

```text
reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md
reports/phase_4_5_qdrant_retrieval_simplicity_codex_review.md
reports/user_reports/phase_4_5_qdrant_retrieval_simplicity_user_report.md
```

Historical Phase 5 evidence trước simplicity review:

```text
reports/phase_5_retrieval_profiles_reranking_implementation_report.md
reports/phase_5_retrieval_profiles_reranking_codex_review.md
reports/hue_foods_rag_benchmark.md
reports/user_reports/phase_5_retrieval_profiles_reranking_user_report.md
```

Benchmark ledger trong Phase 5 chỉ nhận configuration, latency/resource evidence
và safe failure record đã chạy thật. Retrieval quality metrics và winner vẫn
thuộc Phase 7–8.

## Quyết định đã phê duyệt

```text
Decision: Dùng coordinated Phase 4–5 implementation. Phase 4 bỏ stored custom
TF-IDF sparse vectors khỏi active-baseline schema/point/ingestion; Phase 5 chuyển
shared tokenize() sang lexical BM25/scoring ownership. Xóa SparseEmbedder và
tests riêng của nó chỉ sau khi repository không còn consumer.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn phương án A trong Phase 4 simplicity brainstorming.
Capability invariant: Giữ nguyên dense_only, hybrid_no_rerank và hybrid_rerank;
Python BM25 và CrossEncoder không bị xóa hoặc đổi semantics.
Affected scope: backend/scoring/bm25.py, embedding/sparse_embedder.py, Phase 4
schema/point/upsert/ingestion, affected tests/notebooks và import ownership.
Safety boundary: Code/test changes không authorize delete/recreate/reindex active
collection; destructive transition cần exact plan và user approval riêng.
Revisit trigger: Consumer audit phát hiện sparse embedding behavior thật ngoài
Qdrant storage hoặc BM25 tokenization không thể tách mà đổi retrieval semantics.
```

```text
Decision: Dùng blue-green migration. Giữ hue_foods_e5_small_384 read-only trong
khi dense-only candidate tên mới chạy real Phase 4 ingestion và affected Phase 5
retrieval verification. Sau technical review dừng xin user approval trước config
cutover; giữ old collection làm rollback và xin approval khác trước cleanup.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn migration phương án A trong joint Phase 4–5 brainstorming.
Affected scope: schema transition, startup/retrieval verification, active-data
safety và implementation checkpoints.
Revisit trigger: Candidate không chứng minh retrieval tương đương hoặc exact
cutover/rollback plan phát hiện data risk mới.
```

```text
Decision: Phase 5 đọc/validate embedding_model từ corpus payload khi đã scroll
cho BM25; không yêu cầu embedding_dimension trong payload. Dimension/distance
được validate từ Qdrant dense schema và config.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn payload identity phương án A sau llm_rag comparison.
Affected scope: startup corpus projection/validation, retrieval snapshot fields,
tests và notebook diagnostics.
Revisit trigger: Dense-only startup cần một collection-level model identity
mechanism khác hoặc Phase 8 model transition thay đổi contract.
```

```text
Decision: Giữ small immutable runtime status cho API/health/debug nhưng xóa
corpus_fingerprint, config_fingerprint, verify_snapshot() và tests chỉ phục vụ
staleness machinery. Status giữ collection, point count, embedding model/
dimension, active profile và BM25/reranker readiness. Collection/config đổi thì
restart process.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Source audit xác nhận verify_snapshot không có production caller; user
chọn phương án A và cho phép chạy real evidence/xóa code-test vô nghĩa.
Affected scope: core/startup.py, retrieval service status, API debug/health,
startup tests và imports/hash dependencies.
Revisit trigger: Runtime thật cần hot reload hoặc external collection mutation
không thể quản lý bằng explicit restart/deployment lifecycle.
```

```text
Decision: Reranking dùng một concrete reranking/cross_encoder.py với
CrossEncoderReranker instance-owned model. Class trực tiếp load/warm-up/predict,
validate exact finite score count, deterministic sort theo score rồi chunk_id và
trả fresh documents không mutate input. Xóa BaseReranker, ScorerReranker,
models/cross_encoder wrapper, module lru_cache và fake-scorer seam.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Direct source comparison với llm_rag cho thấy base/model wrappers chỉ
có một implementation; user xác nhận đề xuất concrete class.
Failure policy: Model/scoring error fail explicit cho hybrid_rerank, không silent
fallback sang profile khác.
Test boundary: Real MiniLM startup/rerank evidence và pure output invariants cần
thiết; không FakeReranker hoặc test abstraction đã xóa.
Affected scope: reranking package, startup typing/imports, service tests, notebook
và runtime status.
Revisit trigger: Phase 8 duyệt và implement một second real reranker cùng tồn tại;
chỉ lúc đó mới cân nhắc shared interface.
```

```text
Decision: CrossEncoder model loading được phép online trong approved run. Chỉ
hybrid_rerank tạo instance và load/warm-up MiniLM thật; dùng library download
cache bình thường nhưng không app lru_cache, local_files_only gate, preload script
hoặc missing-cache tests. Load/download/predict failure fail explicit.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn model-loading phương án A và đã cho phép real online
execution.
Affected scope: reranking/cross_encoder.py, startup, tests/notebook và resource
documentation.
Revisit trigger: Deployment environment thật yêu cầu offline artifact policy.
```

```text
Decision: scoring/bm25.py tự sở hữu Vietnamese-safe tokenizer, corpus DF/IDF,
BM25 scoring, min-max normalization và fusion-weight validation. Xóa
embedding/sparse_embedder.py và test_sparse_embedder.py sau consumer audit; không
thêm rank_bm25 dependency hoặc giữ SparseEmbedder làm statistics provider.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Source comparison cho thấy llm_rag gắn BM25 vào SparseEmbedder trong
khi Hue BM25 đã tự fit statistics; user chọn phương án A.
Test boundary: Gom về các behavior dễ giải thích: Vietnamese tokenization,
known-corpus ranking, normalization/config validity và real hybrid retrieval;
không giữ 19 micro-tests theo từng implementation branch.
Affected scope: scoring/bm25.py, sparse module deletion, startup imports, BM25/
retrieval tests và Notebook 03/05 references.
Revisit trigger: Approved Phase 8 lexical experiment chọn tokenizer/library khác
và real metrics chứng minh lợi ích.
```

```text
Decision: Giữ DenseRetriever, HybridRetriever và RetrievalService vì chúng ánh
xạ ba hành vi thật; xóa RetrievalStack optional-component container. Startup lắp
đúng components theo active profile rồi trả RetrievalService trực tiếp. Service
sở hữu small runtime status; không test các stack thiếu/sai component được dựng
thủ công ngoài production path.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Caller/source audit cho thấy ba concrete classes có trách nhiệm riêng,
nhưng RetrievalStack chỉ chuyển optional fields sang service; user chọn phương án
A.
Affected scope: core/startup.py, retrieval/service.py, API lifespan/debug access,
type imports và startup/retrieval tests.
Revisit trigger: Một second real composition path cần chia sẻ immutable component
bundle ngoài service.
```

```text
Decision: Giữ ContextBuilder và JSON evidence-block contract vì API, evaluation
và prompt có real consumers. Giữ whole chunks, max 5 documents/3.000 serialized
characters, source mapping, structural isolation và non-mutation. Không đổi sang
plaintext hoặc function chỉ để giảm class count.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Caller/source audit xác nhận implementation chỉ 66 dòng và JSON
structure bảo vệ mapping chunk/source; user chọn phương án A.
Test boundary: Gom test_context_builder về whole-chunk budget/max-documents, JSON
structural safety/source mapping và empty/non-mutation behavior; generator tests
chỉ giữ mapping integration không trùng toàn bộ cases.
Affected scope: test_context_builder.py và overlapping generator tests; runtime
behavior được bảo toàn.
Revisit trigger: Prompt/generator contract thật chuyển khỏi structured evidence.
Status: superseded ngày 2026-08-25 vì Phase 6 prompt/generator contract đã chuyển sang labeled text và public API bỏ sources/debug.
```

```text
Decision: Giữ ContextBuilder class nhưng đơn giản hóa build(documents) -> str. Output là labeled whole-chunk text với title/section; bỏ ContextResult dataclass, JSON evidence array và parallel source mapping. Empty/no-usable input trả empty string.
Approved by: User
Approval date +07: 2026-08-25
Evidence: Phase 6 simplicity brainstorming sau khi public sources, retrieval_debug và model-selected source IDs bị loại bỏ; typed result không còn consumer thật.
Test boundary: Whole-chunk budget/max-documents, labels/order, empty input và non-mutation; không còn JSON/source-mapping tests.
Affected scope: Phase 5 ContextBuilder/tests/notebook và Phase 6–7 callers.
Revisit trigger: Một user-facing provenance feature có contract được phê duyệt và cần mapping song song thật.
```

```text
Decision: Bỏ vector_database.scroll_batch_size, startup override argument và test
override. Giữ bounded Qdrant payload pagination bằng constant nội bộ 128 cho
canonical 572-point corpus; real candidate run phải xác nhận đọc đủ 572 unique
payloads.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn scroll phương án A; không có runtime consumer cần tune batch.
Affected scope: settings/config docs, core/startup.py, startup tests và notebook
runtime explanation.
Revisit trigger: Real Qdrant execution cho thấy batch 128 gây observed latency/
reliability problem hoặc corpus contract tăng đáng kể.
```

```text
Decision: Affected Phase 5 verification chạy fresh retrieval-only evaluation trên
104 canonical questions cho cả ba profiles, trước refactor với active collection
và sau refactor với dense-only candidate. Giữ cùng data/settings và báo metrics,
latency, failures cùng relevant per-query diffs. Không chạy paid generation/judge
vì prompt/generator không đổi.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn comparison phương án A.
Acceptance boundary: Không cần exact floating-point equality nếu model/library có
observed numerical noise, nhưng mọi ranking/metric delta phải được giải thích
trước cutover approval.
Revisit trigger: Retrieval differences ảnh hưởng context selection hoặc source
mapping và cần downstream answer evaluation.
```

```text
Decision: Candidate verification truyền optional exact collection_name qua
ingestion/evaluation composition roots và in-memory settings copy. Production API
vẫn dùng canonical settings.yaml; không sửa config trước cutover, không thêm
candidate settings file hoặc global environment override.
Approved by: User
Approval date +07: 2026-08-25
Evidence: User chọn candidate-targeting phương án A.
Affected scope: service builder inputs, evaluation builder/batch inputs, notebooks
và real comparison commands.
Revisit trigger: Override lan xuống component internals thay vì dừng ở composition
root hoặc tạo multi-collection runtime semantics.
```

```text
Decision: Dùng local-first Phase 5 với E5 dense, Python BM25 và local cross-encoder/ms-marco-MiniLM-L-6-v2; hoãn OpenRouter reranker sang Phase 8.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User xác nhận hướng số 2 sau khi Codex đối chiếu hai tài liệu và source runtime của llm_rag với hue_rag.
Affected scope: Phase 5 retrieval/reranking implementation, notebook, tests và benchmark evidence.
Revisit trigger: Local reranker không đạt latency gate hoặc Phase 7–8 quality evidence cho thấy cần multilingual/remote candidate.
```

```text
Decision: Dùng baseline depth dense 10; hybrid dense candidates 30, fusion top 10; rerank đúng 10 pairs thành top 5; context tối đa 5 documents.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong brainstorming Phase 5.
Affected scope: Retrieval depth, rerank depth, context size và latency measurement.
Revisit trigger: Phase 7–8 retrieval evidence cho thấy relevant chunks thường nằm ngoài pre-rerank top 10.
```

```text
Decision: Normalize dense và BM25 độc lập bằng min-max trên 30 candidates, constant signal về 0.0 và fusion baseline 0.6/0.4; hoãn weight grid sang Phase 8.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong brainstorming Phase 5.
Affected scope: Hybrid score semantics, metadata, tests và benchmark configuration.
Revisit trigger: Controlled evaluation cho thấy min-max hoặc baseline weights không ổn định theo query/category.
```

```text
Decision: Dùng fail-explicit typed errors; chỉ trả [] khi retrieval thành công nhưng không có candidate và cấm silent fallback.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong brainstorming Phase 5.
Affected scope: Retrieval service, startup state, tests và Phase 6 API error mapping.
Revisit trigger: Phase 6 cần bổ sung một public error category nhưng không được thay đổi retrieval semantics.
```

```text
Decision: ContextBuilder chỉ ghép whole chunks, tối đa 5 documents và 3.000 characters tính cả source label/separator, trả context cùng source mapping.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A sau khi Codex xác minh chunk dài nhất 927 ký tự và bảng là atomic từ Phase 2.
Affected scope: ContextBuilder, source contract, tests, notebook và Phase 6 prompt input.
Revisit trigger: Phase 6 token budget hoặc Phase 7 groundedness evidence yêu cầu context policy khác.
Status: source-mapping portion superseded ngày 2026-08-25; whole-chunk, 5-document và 3.000-character limits vẫn giữ.
```

```text
Decision: MiniLM latency gate là một warm-up, 20 lượt rerank 10 pairs trên CPU, p95 không quá 3 giây; cold-load time ghi riêng và thiếu cache phải xin phép download.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong brainstorming Phase 5.
Affected scope: Real local validation, acceptance evidence và model resource policy.
Revisit trigger: Máy local không đạt gate với controlled measurement hoặc resource environment thay đổi.
Superseded in part: Quyết định 2026-08-25 cho phép normal online model load trong
approved run và bỏ cache-only/missing-cache gates; warm-up/latency measurement
vẫn giữ.
```

```text
Decision: Khởi tạo components theo active profile, giữ immutable collection/config/corpus snapshot và yêu cầu tạo service mới hoặc restart khi stale.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong brainstorming Phase 5.
Affected scope: Startup lifecycle, component availability, cache invalidation và performance tests.
Revisit trigger: Runtime cần hot reload/reindex lifecycle được thiết kế và phê duyệt riêng.
Superseded: Quyết định 2026-08-25 chỉ giữ small runtime status và explicit
restart; xóa fingerprints, verify_snapshot và stale-state tests không có
production consumer.
```

```text
Decision: Dùng safe metadata allowlist với stage-conditional scores; Phase 6 không serialize nguyên Qdrant payload.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong brainstorming Phase 5.
Affected scope: RetrievedDocument metadata, notebook diagnostics, benchmark artifacts và Phase 6 API sources.
Revisit trigger: User-facing source UI cần thêm một field cụ thể đã được security/data-safety review.
```

## Bước tiếp theo

Phase 5 đã hoàn thành coordinated simplicity review cùng Phase 4 và giữ
`approved`. Ba canonical profiles vẫn được bảo toàn; dense-only candidate chưa
cutover. Bước tiếp theo của simplicity campaign là Phase 6 theo
`guides/README.md`.
