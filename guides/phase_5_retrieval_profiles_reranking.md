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
Brainstorming level: Level 3 - deep completed
Owner: Codex Reviewer
Implementer: DeepSeek
```

Thiết kế trong guide này đã được người dùng phê duyệt ngày 2026-08-12 +07.
DeepSeek đã bàn giao correction revision 3; Codex technical review đạt và người
dùng đã xác nhận final approval ngày 2026-08-12 +07. Phase 5 đã hoàn tất; Phase
6 vẫn cần brainstorming Level 2 riêng trước implementation.

## Dependency đã đạt

- Phase 4 có status `approved`.
- Active collection `hue_foods_e5_small_384` có 572 points, named dense vector
  384 chiều cosine và sparse index.
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
- Whole-chunk ContextBuilder có bounded context và source mapping.
- Profile-scoped startup/cache lifecycle.
- Typed errors và safe retrieval debug metadata.
- Unit/integration tests offline và notebook safe-default.

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
| `RetrievalService` | Route profile và enforce component availability | API error mapping hoặc generation |
| `ContextBuilder` | Ghép whole chunks trong budget và giữ source mapping | Retrieval hoặc prompt generation |

Mỗi component nhận dependencies qua constructor hoặc input rõ ràng để tests có
thể dùng fakes mà không mở Qdrant hoặc load model.

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
- Query/document dùng cùng `tokenize()` contract với `SparseEmbedder`.
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

- Chỉ dùng model đã có trong local cache.
- Nếu cache thiếu, dừng và xin user approval trước model download.
- Unit tests và notebook default dùng fake scorer, không load model.
- Real validation có một warm-up không tính vào kết quả.
- Sau warm-up, đo 20 lượt, mỗi lượt rerank đúng 10 pairs trên CPU.
- p95 rerank latency phải không quá 3 giây.
- Cold model-load time được đo và ghi riêng, không trộn vào query latency.
- Nếu không đạt gate, Phase 5 chuyển `changes_requested` hoặc ghi blocker; không
  tự đổi model, depth hoặc device.

## ContextBuilder contract

ContextBuilder nhận ranked documents sau stage cuối và trả một typed result gồm
context text cùng source mapping theo rank.

Rules:

- Tối đa 5 documents và 3.000 characters.
- Character budget tính cả source label và separator.
- Chỉ thêm whole chunk; nếu chunk kế tiếp không vừa thì dừng.
- Không truncate bảng, câu hoặc metadata nguồn để lấp đầy budget.
- Bỏ empty text, giữ rank order và không mutate documents.
- Empty input trả empty context và empty sources.
- Source mapping giữ tối thiểu `chunk_id`, `source`, `title`, `section` và rank.
- Context chỉ chứa curated evidence và safe source label, không chứa debug
  payload hoặc secrets.

Corpus Hue Foods có chunk thường tối đa 400 ký tự; bảng là atomic và bảng dài
nhất đã xác minh ở Phase 2 là 927 ký tự. Whole-chunk policy vì vậy giữ cấu trúc
bảng mà vẫn cho phép khoảng 3–5 evidence trong baseline budget.

## Startup và cache lifecycle

Service initialization theo active profile:

```text
inspect exact collection/schema/count/model/dimension
  -> dense_only: create dense retriever only
  -> hybrid_no_rerank: bounded scroll 572 payloads -> fit BM25 once
  -> hybrid_rerank: same hybrid initialization -> load MiniLM once
  -> expose immutable component status and snapshot
```

Snapshot gồm:

```text
collection_name
point_count
embedding_model
embedding_dimension
corpus_fingerprint
active_profile
bm25_ready
reranker_ready
config_fingerprint
```

Lifecycle rules:

- Scroll theo bounded batches, `with_vectors=False`, chỉ lấy safe payload fields.
- Xác minh đúng 572 unique `chunk_id` và non-empty text.
- Corpus fingerprint tính deterministic từ sorted `chunk_id + text` pairs.
- Config fingerprint tính deterministic từ retrieval depth/fusion settings và
  thêm reranker model/device/top-k khi profile dùng reranker. Baseline dùng
  conservative shared retrieval fingerprint cho mọi profile, nên thay đổi
  fusion config có thể làm `dense_only` stale dù chưa dùng BM25.
- BM25 và reranker giữ immutable trong vòng đời service.
- Collection/config/fingerprint thay đổi làm snapshot stale và yêu cầu tạo
  service mới hoặc restart; không tự refit giữa requests.
- Không thêm persistent cache artifact trong Phase 5.
- Optional component failure không làm profile khác âm thầm đổi semantics.

## Failure policy và typed errors

Phase 5 dùng fail-explicit policy:

| Điều kiện | Kết quả |
|---|---|
| Query rỗng/whitespace | `InvalidQueryError` |
| Profile hoặc config sai | `RetrievalConfigurationError` |
| Required component missing hoặc snapshot stale | `ComponentNotReadyError` |
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
backend/reranking/base.py
backend/reranking/models/cross_encoder.py
backend/reranking/reranker.py
backend/tests/test_bm25.py
backend/tests/test_retrieval_service.py
backend/tests/test_reranker.py
backend/tests/test_context_builder.py
backend/tests/test_startup.py
notebooks/05_retrieval_profiles.ipynb
reports/phase_5_retrieval_profiles_reranking_implementation_report.md
reports/hue_foods_rag_benchmark.md
```

Không tạo `backend/reranking/openrouter_reranker.py` trong Phase 5. Không sửa
ingestion, chunking, embedding model/dimension, Qdrant schema, collection
contents, generation, API hoặc frontend.

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

Chỉ bổ sung context limits và bounded startup scroll size nếu implementation
cần. Không thêm tuning grid hoặc speculative knobs.

## Nhiệm vụ của DeepSeek Implementer

1. Implement BM25 và normalization thuần, kiểm tra bằng known corpus.
2. Implement dense/hybrid retrievers với injected fake Qdrant và fake embedder.
3. Implement profile routing, score metadata và typed errors.
4. Implement reranker contract với fake scorer trước, sau đó wrapper MiniLM.
5. Implement whole-chunk ContextBuilder và source mapping.
6. Implement profile-scoped startup lifecycle và immutable snapshot.
7. Tạo notebook safe-default và implementation report.
8. Chạy smallest relevant tests trước, sau đó full backend regression.
9. Xin approval riêng trước real Qdrant/cached-model validation.

Không copy nguyên code `llm_rag`. Đặc biệt không copy raw-score fusion, broad
exception-to-empty behavior, eager all-component startup, input mutation hoặc
ContextBuilder không tính separator vào budget.

## Notebook bắt buộc

`notebooks/05_retrieval_profiles.ipynb` phải:

- import `RetrievalService` và `ContextBuilder` từ backend;
- giải thích ba profiles bằng tiếng Việt;
- default mode dùng fake dependencies và không mở Qdrant, tải model hoặc gọi
  external API;
- hiển thị score fields đúng với từng stage và whole-chunk bounded context;
- có explicit environment guard cho real local mode;
- real mode chỉ dùng Qdrant local và model đã có trong cache;
- không gọi OpenRouter hoặc bất kỳ paid API nào;
- committed outputs rỗng và mọi `execution_count=null`.

## Tests và validation dự kiến

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/startup.py retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py reranking/base.py reranking/models/cross_encoder.py reranking/reranker.py
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_bm25.py tests/test_retrieval_service.py tests/test_reranker.py tests/test_context_builder.py tests/test_startup.py -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/ -q --tb=short
```

Required test evidence:

- BM25 known corpus, average document length và empty document behavior.
- Min-max normal/constant/non-finite cases và weight validation.
- Candidate depth/output depth chính xác cho từng profile.
- Profile không gọi stage không sử dụng.
- Score fields chỉ xuất hiện khi stage đã chạy.
- Deterministic ties theo `chunk_id`.
- Reranker score count, finite score, duplicate/foreign output và no mutation.
- Context whole-chunk budget tính cả source label/separator và giữ source order.
- Startup bounded scroll, 572 unique IDs, fingerprint và profile-scoped loading.
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

Nếu thiếu local model cache, dừng và xin approval trước download. Nếu real local
validation không được phê duyệt, implementation report phải ghi rõ check chưa
chạy; không suy diễn pass từ mocks.

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
- Local MiniLM chạy CPU và đạt latency gate khi real validation được approve.
- Context whole-chunk, bounded, deterministic và giữ source mapping.
- Typed failures rõ, không biến dependency error thành empty retrieval.
- Notebook an toàn và implementation report đầy đủ.
- Không remote reranker, live API, reindex, tuning grid hoặc winner claim.

Technical review đạt chỉ chuyển phase sang `awaiting_user_confirmation`. Phase 5
chỉ `approved` sau khi người dùng đọc user report và xác nhận notebook/kết quả.

## Reports và benchmark

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
Evidence: User chọn phương án A trong Level 3 brainstorming Phase 5.
Affected scope: Retrieval depth, rerank depth, context size và latency measurement.
Revisit trigger: Phase 7–8 retrieval evidence cho thấy relevant chunks thường nằm ngoài pre-rerank top 10.
```

```text
Decision: Normalize dense và BM25 độc lập bằng min-max trên 30 candidates, constant signal về 0.0 và fusion baseline 0.6/0.4; hoãn weight grid sang Phase 8.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong Level 3 brainstorming Phase 5.
Affected scope: Hybrid score semantics, metadata, tests và benchmark configuration.
Revisit trigger: Controlled evaluation cho thấy min-max hoặc baseline weights không ổn định theo query/category.
```

```text
Decision: Dùng fail-explicit typed errors; chỉ trả [] khi retrieval thành công nhưng không có candidate và cấm silent fallback.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong Level 3 brainstorming Phase 5.
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
```

```text
Decision: MiniLM latency gate là một warm-up, 20 lượt rerank 10 pairs trên CPU, p95 không quá 3 giây; cold-load time ghi riêng và thiếu cache phải xin phép download.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong Level 3 brainstorming Phase 5.
Affected scope: Real local validation, acceptance evidence và model resource policy.
Revisit trigger: Máy local không đạt gate với controlled measurement hoặc resource environment thay đổi.
```

```text
Decision: Khởi tạo components theo active profile, giữ immutable collection/config/corpus snapshot và yêu cầu tạo service mới hoặc restart khi stale.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong Level 3 brainstorming Phase 5.
Affected scope: Startup lifecycle, component availability, cache invalidation và performance tests.
Revisit trigger: Runtime cần hot reload/reindex lifecycle được thiết kế và phê duyệt riêng.
```

```text
Decision: Dùng safe metadata allowlist với stage-conditional scores; Phase 6 không serialize nguyên Qdrant payload.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User chọn phương án A trong Level 3 brainstorming Phase 5.
Affected scope: RetrievedDocument metadata, notebook diagnostics, benchmark artifacts và Phase 6 API sources.
Revisit trigger: User-facing source UI cần thêm một field cụ thể đã được security/data-safety review.
```

## Bước tiếp theo

Brainstorm Phase 6 theo Level 2 về grounded generation, JSON API contract,
OpenAI Agents SDK behavior và error mapping. Model download, real Qdrant probes,
collection mutation, live API, scope change hoặc dependency mới vẫn cần user
approval riêng.
