# Phase 5: Retrieval profiles, reranking và context

## Mục tiêu và giá trị cho người dùng

Phase 5 tạo retrieval pipeline có ba chế độ so sánh được: dense semantic baseline, dense kết hợp lexical BM25 và hybrid có reranking. Người dùng có thể thấy từng kỹ thuật thêm giá trị gì thay vì chỉ đánh giá một pipeline tổng hợp không biết nguyên nhân.

## Trạng thái

```text
Status: not_ready
Brainstorming level: Level 3 - deep
Owner: Codex Reviewer
Implementer: DeepSeek after Phase 4 approval and Phase 5 readiness
```

## Dependency

- Phase 4 active collection tồn tại và point count/schema đã được approve.
- Query embedder phải dùng cùng model/instruction/dimension với indexed documents.
- Canonical chunks và metadata không đổi trong một comparison group.
- BM25 và reranker models/config phải được ghi trong benchmark ledger.

## Chức năng phải tạo

- Dense Qdrant retriever.
- Corpus-scoped Python BM25 scorer.
- Hybrid score normalization/fusion.
- Profile router/service dùng config đã có.
- Local CrossEncoder reranker baseline và provider boundary cho OpenRouter native rerank.
- Bounded ContextBuilder giữ source mapping.
- Startup/cache lifecycle cho corpus statistics và local models.
- Stable retrieval debug metadata.
- Notebook manual probes không live mặc định.

## Files dự kiến

```text
backend/core/startup.py
backend/retrieval/dense_retriever.py
backend/retrieval/hybrid_retriever.py
backend/retrieval/service.py
backend/retrieval/context_builder.py
backend/scoring/bm25.py
backend/reranking/base.py
backend/reranking/models/cross_encoder.py
backend/reranking/openrouter_reranker.py
backend/reranking/reranker.py
backend/tests/test_bm25.py
backend/tests/test_retrieval_service.py
backend/tests/test_reranker.py
backend/tests/test_context_builder.py
notebooks/04_retrieval_profiles.ipynb
```

OpenRouter reranker file chỉ implement sau exact endpoint/model preflight; mocked provider contract vẫn phải test được.

## Ba retrieval profiles canonical

### `dense_only`

```text
query
  -> query validation
  -> dense query embedding
  -> Qdrant search using named vector dense
  -> threshold/filter
  -> top_k RetrievedDocument list
  -> ContextBuilder
```

Không fit/call BM25. Không load/call reranker. `metadata.bm25_score`, `hybrid_score` và `rerank_score` không được tạo.

### `hybrid_no_rerank`

```text
query
  -> dense query embedding
  -> Qdrant dense search với candidate_depth = top_k * candidate_multiplier
  -> BM25 score từng dense candidate
  -> normalize dense/BM25 scores trong candidate set
  -> weighted fusion
  -> sort deterministic
  -> top_k RetrievedDocument list
  -> ContextBuilder
```

Hybrid hiện tại không query named sparse vector trong Qdrant.

### `hybrid_rerank`

```text
query
  -> cùng hybrid pipeline và cùng pre-rerank candidates
  -> configured reranker score(query, document)
  -> sort deterministic theo rerank score
  -> reranking.top_k
  -> ContextBuilder
```

Để đo incremental effect, `hybrid_rerank` phải dùng cùng embedding collection, candidate depth và hybrid config với `hybrid_no_rerank` trong cùng experiment.

## RetrievedDocument và debug contract

Mọi profile trả `list[RetrievedDocument]`. `score` là final ranking score của stage cuối thực sự chạy.

Metadata chung:

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
```

Score fields có điều kiện:

| Field | Dense | Hybrid | Hybrid + rerank |
|---|---:|---:|---:|
| `dense_score` | Có | Có | Có |
| `bm25_score` | Không | Có | Có |
| `hybrid_score` | Không | Có | Có |
| `rerank_score` | Không | Không | Có |

Tie-breaking phải deterministic, ưu tiên score rồi stable `chunk_id`, để evaluation lặp lại được.

## BM25 contract

Baseline theo `llm_rag`:

```text
k1 = 1.5
b = 0.75
```

BM25 fit trên toàn bộ active corpus chunk texts, không chỉ dense candidates. Average document length được tính từ non-empty documents. Query/document tokenization phải dùng cùng tokenizer contract với sparse representation.

Behavior:

- empty query/document trả `0.0` hoặc bị reject tại service boundary theo quyết định brainstorming;
- score chỉ tính query terms có trong vocabulary và document;
- không fit BM25 mỗi request;
- startup cache gắn với active collection/model/corpus version;
- collection count/version thay đổi làm cache invalid và yêu cầu refit.

## Score normalization và fusion

Không cộng raw cosine score với raw BM25 như hai đại lượng cùng scale. Brainstorming phải chọn và test một normalization rõ ràng, ưu tiên min-max trong candidate set cho MVP nếu không có evidence tốt hơn.

Weighted fusion:

```text
hybrid_score = dense_weight * normalized_dense + bm25_weight * normalized_bm25
```

Invariants:

- weights finite, non-negative và tổng bằng 1 trong tolerance;
- constant-score candidate set có deterministic normalization, không chia zero;
- normalization algorithm/config được ghi vào mỗi benchmark run;
- default 0.6/0.4 chỉ là baseline, không phải winner.

## Reranker contract

Interface:

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

Invariants:

- empty documents trả `[]` mà không load/call model;
- output chỉ chứa input documents, không duplicate;
- input order không bị mutate ngoài contract;
- score count phải bằng document count;
- `rerank_score` là finite float;
- stable tie-breaking;
- actual provider/model ID và latency được ghi.

### Local baseline

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
device: cpu
```

Model nhỏ và đã dùng trong `llm_rag`, nhưng training chủ yếu English/MS MARCO nên phải được xem là latency baseline, không mặc định là tốt cho tiếng Việt. Benchmark Phase 7–8 quyết định giá trị thực tế.

### OpenRouter native rerank

Trước implementation/live run, xác minh native `/rerank` support, exact catalog model, Vietnamese/multilingual evidence, document limit, pricing, timeout và response order. Qwen3-Reranker chỉ được dùng khi OpenRouter native support thực sự được xác minh tại thời điểm Phase 5.

Outside benchmark, runtime có thể fallback từ remote reranker sang approved local reranker nếu policy đã được user chốt và response metadata ghi model thực tế. Trong benchmark, fallback bị cấm: run phải fail và được ghi là failed.

## ContextBuilder contract

Input là ranked documents sau stage cuối. Output gồm bounded context và source mapping đủ để Phase 6 trả citations.

Rules:

- giới hạn `max_documents` và `max_context_length`/token budget;
- bỏ document text rỗng;
- không vượt budget sau khi tính separator/source label;
- không cắt giữa Unicode code unit hoặc làm hỏng source identity;
- giữ rank order;
- không mutate retrieved documents;
- empty input trả empty context và sources;
- context chỉ chứa curated evidence, không chứa debug payload hoặc secrets.

Baseline từ `llm_rag` là tối đa 5 documents và khoảng 3.000 characters; Phase 5 brainstorming phải xác nhận lại với Vietnamese food chunks và generator context budget.

## Startup và cache lifecycle

Startup/service initialization:

```text
inspect active collection metadata/count
  -> load corpus payload texts bằng bounded scroll
  -> fit sparse tokenizer state/BM25
  -> optionally load configured local reranker
  -> expose immutable component status
```

Không buộc `dense_only` phải load BM25 hoặc reranker. Startup failure của optional component không được làm profile khác âm thầm thay nghĩa. Service phải trả error rõ nếu active profile yêu cầu component chưa sẵn sàng.

## Brainstorming Level 3 bắt buộc

Codex và người dùng phải chốt:

1. `top_k`, `candidate_multiplier` và reranker `top_k` baseline.
2. Normalization method và fusion weights experiment grid nhỏ nhất có ý nghĩa.
3. Empty query và Qdrant/provider failure behavior.
4. Context document/character hoặc token budget.
5. Local reranker download/cache availability và CPU latency ceiling.
6. OpenRouter native reranker exact candidate, cost ceiling và fallback policy.
7. Retrieval debug fields được phép trả ra API sau này.

Mỗi lựa chọn phải nêu hypothesis, metric sẽ phân biệt và stop condition để tránh tuning vô hạn.

## Nhiệm vụ của DeepSeek Implementer

- TDD cho BM25 known corpus, normalization edge cases, profile routing, no-unused-stage calls, rerank count/ties và context budget.
- Dùng dependency injection hoặc constructor inputs đủ để mock Qdrant/embedder/reranker; không tạo framework phức tạp.
- Cache corpus/model ngoài request path.
- Không gọi remote API trong default tests/notebook.
- Ghi actual retrieval path; không gọi stored sparse vector là queried sparse retrieval.
- Tạo implementation report với latency sample và failure evidence được redact.

## Notebook bắt buộc

`notebooks/04_retrieval_profiles.ipynb` phải:

- import retrieval service và ContextBuilder;
- giải thích ba profiles bằng tiếng Việt;
- dùng representative food queries và hiển thị score fields theo profile khi real mode được bật;
- có safe default fake/mocked results;
- không gọi OpenRouter hoặc download reranker mặc định;
- committed outputs rỗng, `execution_count=null`.

## Tests và validation dự kiến

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/startup.py retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py reranking/base.py reranking/models/cross_encoder.py reranking/reranker.py
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_bm25.py tests/test_retrieval_service.py tests/test_reranker.py tests/test_context_builder.py -q --tb=short
```

Required test evidence:

- profile flags gọi đúng stages;
- dense candidate depth đúng;
- BM25 fit một lần và score known corpus đúng;
- normalization constant set không lỗi;
- weights validation;
- reranker output/count/ties;
- no silent fallback in benchmark mode;
- context budget và source order;
- Qdrant/provider failure mapping.

Manual real retrieval probes cần Qdrant/local model approval và chỉ là pre-evaluation evidence, không thay Phase 7 metrics.

## Security, reliability và performance gates

- Query không được log nguyên văn ở production-level logs nếu chưa có privacy decision.
- Không log API key, provider headers, full context hoặc raw model payload.
- Candidate depth, batches và context bounded.
- Optional component cache không làm semantic profile drift.
- Benchmark records actual model và failures.
- Remote rerank cần timeout và bounded documents.

## Tiêu chí phê duyệt Phase 5

- Ba profiles có behavior đúng và được test độc lập.
- Hybrid dùng normalized dense + Python BM25, không misleading sparse claim.
- Local reranker baseline chạy CPU trong latency ceiling đã chốt.
- Remote adapter nếu có được mock-test và không silent fallback trong benchmark.
- Context bounded, deterministic và giữ sources.
- Notebook an toàn, report đầy đủ, không live access ngoài approval.
- Representative food queries trả documents; quality winner chưa được tuyên bố trước Phase 7–8.

## Reports và benchmark

```text
reports/phase_5_retrieval_profiles_reranking_implementation_report.md
reports/phase_5_retrieval_profiles_reranking_codex_review.md
reports/hue_foods_rag_benchmark.md
```

Codex chỉ cập nhật `Project_Status.md` sau approval.

## Bước tiếp theo

Sau Phase 5 approval, Phase 6 brainstorm grounded prompt, JSON API contract, OpenAI Agents SDK behavior, error mapping và live-cost gate.
