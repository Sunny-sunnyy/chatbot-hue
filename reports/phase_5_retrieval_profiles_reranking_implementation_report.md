# Implementation Report: Phase 5 Retrieval profiles, BM25, reranking và context

Implementer: DeepSeek
Date: 2026-08-12 (revision 3 - correction pass re-review)
Report path:

```text
reports/phase_5_retrieval_profiles_reranking_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_5_retrieval_profiles_reranking.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
reports/phase_5_retrieval_profiles_reranking_codex_review.md
```

## Approved Scope

Phase 5 đã hoàn tất Level 3 brainstorming và được người dùng phê duyệt ngày
2026-08-12 +07, guide có `Status: ready`. Phạm vi được implement đúng guide:

- Dense Qdrant retriever dùng named vector `dense` (top 10).
- Corpus-scoped Python BM25 `k1=1.5`, `b=0.75`, fit một lần trên 572 texts.
- Min-max normalization và weighted fusion deterministic (0.6/0.4).
- Profile router/service cho ba profile canonical.
- Local MiniLM CrossEncoder reranker chạy CPU, cache-only load.
- Whole-chunk ContextBuilder bounded context và source mapping.
- Profile-scoped startup/cache lifecycle với immutable snapshot.
- Typed errors và safe retrieval debug metadata.
- Unit/integration tests offline và notebook safe-default.

Không implement OpenRouter reranker, native Qdrant sparse retrieval, tuning
grid, retrieval metrics hay winner selection (hoãn sang Phase 7-8).

## Summary

Implement xong retrieval pipeline local ba profile: `dense_only` (dense top 10),
`hybrid_no_rerank` (dense 30 candidates + BM25 fusion 0.6/0.4 -> top 10),
`hybrid_rerank` (cùng hybrid pipeline -> CrossEncoder score 10 pairs -> top 5).
Startup xác minh config identity (gồm cả `embedder.model_id`), collection/
schema/count 572/unique `chunk_id`/non-empty text/embedding model/corpus
fingerprint rồi khởi tạo đúng component theo profile; với `hybrid_rerank`,
MiniLM được load một lần từ local cache (`local_files_only=True`, không bao
giờ tự download) và thiếu cache fail rõ. Snapshot immutable, giờ bao gồm
`config_fingerprint` (semantic retrieval/reranking config); `verify_snapshot()`
phát hiện stale state kể cả khi retrieval/reranking config thay đổi.

Revision 3 (correction pass re-review) sửa các contract gaps Codex tìm thấy:
typed conversion guard cho mọi dense/reranker score (string/None/malformed/
nan/inf/count mismatch -> `RetrievalDependencyError`); reranker reject
duplicate `chunk_id` input trước khi gọi scorer; startup fail-fast khi
injected embedder `model_id` lệch `embedding.model`; `config_fingerprint` cho
semantic config staleness; purity tests dùng stub trả chính captured
list/objects; bỏ unused import.

Toàn bộ validation offline bằng fakes: 217 tests đạt (99 tests Phase 5 + 118
regression), notebook default mode chạy đạt bằng fake dependencies.

## Files Created

- `backend/core/startup.py` - profile-scoped startup: config identity
  (dimension + model_id), schema/count/payload verification, bounded scroll
  `with_vectors=False` với payload projection, BM25 fit một lần, reranker
  cache-only load, `RetrievalSnapshot`/`RetrievalStack` immutable,
  `config_fingerprint` + `verify_snapshot()` stale detection.
- `backend/scoring/bm25.py` - pure BM25 (k1=1.5, b=0.75), min-max normalization,
  weight validation.
- `backend/retrieval/dense_retriever.py` - DenseRetriever: E5 query embedding
  (mọi failure -> `RetrievalDependencyError`), Qdrant dense query với payload
  projection, typed score guard (non-numeric/non-finite -> typed error),
  deterministic order (score desc, `chunk_id` asc), safe metadata allowlist.
- `backend/retrieval/hybrid_retriever.py` - HybridRetriever: BM25 trên
  candidates, normalization độc lập, fusion, result objects mới (không mutate
  dense candidates).
- `backend/retrieval/service.py` - RetrievalService profile router + component
  availability enforcement, output objects mới (không mutate component output)
  + `build_service` factory.
- `backend/retrieval/context_builder.py` - whole-chunk ContextBuilder với
  `ContextResult` (context + sources) typed.
- `backend/reranking/base.py` - `BaseReranker` interface.
- `backend/reranking/reranker.py` - `ScorerReranker` (injected scorer): typed
  score guard (non-numeric/non-finite/count mismatch -> `RetrievalDependencyError`),
  duplicate `chunk_id` input reject trước scorer, tie-break deterministic,
  no mutation, empty -> `[]`.
- `backend/reranking/models/cross_encoder.py` - `CrossEncoderReranker` local
  MiniLM với `local_files_only=True` (downloads disabled), `load()` cache-only
  một lần mỗi process, empty input không load model.
- `backend/tests/test_bm25.py` - 17 tests.
- `backend/tests/test_retrieval_service.py` - 30 tests: depth chính xác, payload
  projection, no-unused-stage, stage-conditional metadata, ties, typed score
  guard (nan/inf/string/None/object), typed error wrapping, purity với stub
  object identity, `[]` policy.
- `backend/tests/test_reranker.py` - 21 tests: typed score guard (kể cả
  string/None/malformed và numeric string conversion), duplicate input reject,
  missing chunk_id reject, count/finite/foreign/duplicate/no-mutation/ties/
  empty/scorer failure wrap/cache-only load/`local_files_only`.
- `backend/tests/test_context_builder.py` - 8 tests.
- `backend/tests/test_startup.py` - 31 tests: bounded scroll + projection,
  572 unique IDs, fingerprint, profile-scoped loading, reranker cache-only
  load/missing-cache, dimension + model_id identity, config staleness
  (weights/top_k/multiplier/rerank model/rerank top_k), `verify_snapshot`.
- `notebooks/05_retrieval_profiles.ipynb` - notebook canonical Phase 5 (cell
  IDs chuẩn nbformat 4.5).
- `reports/phase_5_retrieval_profiles_reranking_implementation_report.md` -
  report này (revision 3).

## Files Modified

- `backend/config/settings.yaml` - bổ sung `vector_database.scroll_batch_size:
  128` và `retrieval.max_context_documents: 5`,
  `retrieval.max_context_characters: 3000` (đúng phạm vi "chỉ bổ sung context
  limits và bounded startup scroll size" của guide).
- `backend/config/README_config.md` - mô tả profile-scoped startup và hai nhóm
  config mới.
- `backend/core/schema.py` - thêm 4 typed errors: `InvalidQueryError`,
  `RetrievalConfigurationError`, `ComponentNotReadyError`,
  `RetrievalDependencyError`.

## Notebooks Created Or Modified

- `notebooks/05_retrieval_profiles.ipynb` - giải thích ba profiles bằng tiếng
  Việt, import `RetrievalService`, `ContextBuilder` và `build_retrieval_stack`
  từ backend, không duplicate runtime logic. Default mode dùng fake embedder +
  fake client (572 payloads hợp lệ) để startup verification chạy thật; không mở
  Qdrant, không tải model, không gọi external API. Cell real mode opt-in bằng
  `HUE_RAG_QDRANT_REAL=1` và chỉ in snapshot, không chạy query. Mọi cell có
  unique `id` (nbformat 4.5); outputs rỗng; mọi `execution_count=null`. User
  kiểm tra bằng cách chạy lại toàn bộ notebook (an toàn) hoặc chạy tests trong
  `backend/`.

## Correction Mapping (Revision 3)

Mỗi required change từ Codex re-review -> source fix -> regression test ->
actual result:

| Finding | Source fix | Regression test | Actual result |
|---|---|---|---|
| 1. Non-numeric dense score thoát `ValueError` | `DenseRetriever._to_document`: `float()` nằm trong typed guard; `TypeError`/`ValueError` -> `RetrievalDependencyError` "retrieved point has a non-numeric score"; `nan/inf` -> "non-finite" | `test_non_numeric_dense_score_rejected_as_dependency_error` (string/None/object), `test_non_finite_dense_score_rejected_as_dependency_error` | 2 tests pass |
| 1. Non-numeric reranker score thoát `TypeError` | `ScorerReranker._to_finite_scores()`: convert từng score qua `float()` trong typed guard; malformed/None/nan/inf/count mismatch -> `RetrievalDependencyError`; numeric string được convert hợp lệ | `test_non_numeric_scores_raise_dependency_error` (string/None/object), `test_numeric_string_scores_are_converted`, `test_score_count_mismatch_raises_dependency_error`, `test_non_finite_score_raises_dependency_error` | 4 tests pass |
| 2. Reranker duplicate output | `ScorerReranker.rerank` validate `chunk_id` uniqueness (và validity) trước khi gọi scorer; duplicate/missing -> `RetrievalDependencyError`; không silent deduplicate | `test_duplicate_input_chunk_ids_are_rejected_before_scorer` (scorer không được gọi), `test_input_missing_chunk_id_is_rejected` | 2 tests pass |
| 3. Injected embedder wrong model ID được accept | `_verify_config_consistency` thêm check `embedder.model_id == embedding.model` -> `RetrievalConfigurationError` | `test_injected_embedder_model_id_mismatch_raises`, `test_injected_embedder_matching_model_id_builds` | 2 tests pass |
| 4. `verify_snapshot` không phát hiện retrieval/reranking config thay đổi | Thêm field `config_fingerprint` vào `RetrievalSnapshot` (SHA-256 của semantic config: top_k, candidate_multiplier, dense_weight, bm25_weight + reranking model/device/top_k khi profile `hybrid_rerank`); `verify_snapshot` so fingerprint hiện tại với snapshot -> `ComponentNotReadyError`; không chạy per-request, không refit | `test_verify_snapshot_detects_fusion_weight_change`, `test_verify_snapshot_detects_candidate_depth_change` (top_k và multiplier), `test_verify_snapshot_detects_rerank_config_change_for_hybrid_rerank` (model và top_k), `test_verify_snapshot_ignores_rerank_config_for_non_rerank_profile`, `test_verify_snapshot_passes_when_unchanged` | 5 tests pass |
| 5. Purity tests không giữ object identity | `StubDense`/`StubHybrid` trả chính captured list/instances; assert snapshot score/text/deep-copied metadata không đổi và output là objects mới (`is not`) | `test_hybrid_does_not_mutate_the_same_captured_objects`, `test_service_does_not_mutate_the_same_captured_objects` | 2 tests pass |
| 6. Unused import `ComponentNotReadyError` trong reranker.py | Xóa import (chỉ còn `RetrievedDocument`, `RetrievalDependencyError`) | `py_compile` | pass |

Ghi chú thêm field snapshot: `RetrievalSnapshot` có thêm `config_fingerprint:
Optional[str] = None` (default None để không phá direct construction; mọi stack
từ `build_retrieval_stack` đều có giá trị thật). `verify_snapshot` chỉ so sánh
fingerprint khi snapshot có giá trị (None -> skip), tương tự corpus_fingerprint.
Codex Reviewer được đề nghị đồng bộ guide nếu chấp nhận.

Về foreign document claim: với scorer API chỉ trả scores, output luôn là
subset của input documents (chọn `ranked[:top_k]` từ `zip(scores, documents)`),
nên foreign document không thể được tạo qua API này; report không claim một
mechanism chống foreign riêng. Duplicate bị chặn bằng reject input.

## Commands Run

```bash
# Từ backend/:
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/schema.py core/startup.py retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py reranking/base.py reranking/models/cross_encoder.py reranking/reranker.py
# -> pass (10 modules)

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_bm25.py tests/test_retrieval_service.py tests/test_reranker.py tests/test_context_builder.py tests/test_startup.py -q --tb=short
# -> 99 passed in 7.52s

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# -> 217 passed in 10.67s

# Từ repo root:
env -u HUE_RAG_QDRANT_REAL UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute notebooks/05_retrieval_profiles.ipynb --output /tmp/nb05_rev3.ipynb --ExecutePreprocessor.timeout=120
# -> default fake mode execute pass, 0 cell errors

UV_CACHE_DIR=/tmp/uv-cache uv run python -c "... nbformat.validate + schema checks ..."
# -> 19 cells, ids unique, outputs rỗng, execution_count null

git diff --check
# -> clean

codegraph status .
# -> Index is up to date (54 python files)
```

## Tests And Verification

Targeted Phase 5 tests (99 passed):

- **test_bm25.py (17)**: BM25 score khớp reference formula, known corpus
  ranking, average document length chỉ tính non-empty docs, empty document
  score 0.0, query term dedup, out-of-vocabulary term 0.0, refit reset, score
  trước fit raise; min-max normal/constant->0.0/empty/non-finite; weights
  finite/non-negative/sum-1.
- **test_retrieval_service.py (30)**: dense_only top-10 depth + payload
  projection; hybrid candidate depth 30 và output 10; hybrid_rerank rerank đúng
  10 pairs -> top 5; fusion math trên known corpus; constant BM25 signal;
  stage-conditional metadata; score = stage cuối; ties theo `chunk_id`; typed
  errors (InvalidQueryError, RetrievalConfigurationError,
  ComponentNotReadyError, RetrievalDependencyError cho EmbeddingError,
  RuntimeError thô từ embedder, transport failure, non-finite dense score,
  non-numeric dense score string/None/object); purity stub object identity cho
  hybrid và service; không có candidate -> `[]`.
- **test_reranker.py (21)**: empty -> `[]` không gọi scorer; typed score guard
  (count mismatch, non-finite, non-numeric string/None/object, numeric string
  conversion); scorer RuntimeError wrap; duplicate `chunk_id` input reject
  trước scorer; missing `chunk_id` reject; unique input -> unique output subset;
  no mutation; ties; top_k truncate/all/invalid; reranker metadata;
  CrossEncoderReranker `model_id`, empty input không load model, `load()` fail
  typed khi cache thiếu, `local_files_only=True` và cache một lần.
- **test_context_builder.py (8)**: budget tính cả label + separator; dừng khi
  chunk kế không vừa; max 5 documents; empty input; empty text skip giữ rank;
  source mapping đủ fields; không mutate documents.
- **test_startup.py (31)**: dense_only chỉ tạo dense retriever; hybrid scroll
  bounded + projection; 572 unique IDs; duplicate/empty-text/model-mismatch;
  count mismatch; scroll count mismatch; missing collection và schema mismatch;
  embedding/db dimension mismatch; injected embedder dimension mismatch;
  injected embedder model_id mismatch + matching build; fingerprint
  deterministic/khác khi corpus đổi/khớp reference digest; scroll batch
  override; components immutable; hybrid_rerank cache-only load một lần,
  missing cache fail, injected reranker không load; `verify_snapshot` pass khi
  không đổi (kể cả dense_only không scroll), phát hiện point count change,
  fingerprint change, missing collection, schema change, config change
  (active_profile, fusion weights, top_k, candidate_multiplier, reranker model,
  reranker top_k), bỏ qua rerank config khi profile không dùng reranker;
  `build_service` factory route đúng profile.

Full backend regression: `217 passed` (118 tests Phase 1-4 giữ nguyên + 99
mới cho Phase 5).

Notebook checks: JSON parse OK; nbformat validate pass; 19 cells (9 code); mọi
`execution_count` null; mọi outputs rỗng; cell ids unique; nbconvert default
mode chạy đạt không có cell error.

`git diff --check` sạch; `git diff --name-only` + `git status --short` chỉ chứa
file thuộc allowlist của guide Phase 5 (các thay đổi có sẵn của user - guides,
knowledge-base deletions, notebooks 01/02, skills/ - giữ nguyên, không stage,
không commit).

CodeGraph: sync theo workflow vì source mới; index up to date với 54 python
files.

## Evaluation Results

Không có retrieval quality benchmark run trong Phase 5. Retrieval metrics
(MRR/nDCG/Recall), answer judge và winner selection thuộc Phase 7-8; guide cấm
chạy benchmark 104 câu ở Phase 5. `reports/hue_foods_rag_benchmark.md` không
được cập nhật vì chưa có actual safe evidence Phase 5.

```text
Retrieval result file: none (deferred to Phase 7-8)
Answer result file: none
Benchmark log updated: no (no actual evidence yet)
```

## Deviations And Interpretation Notes

Không có deviation so với approved guide trong revision 3; các note dưới đây
mô tả interpretation đã đối chiếu với Codex review (không claim "None" tuyệt
đối vì real probes chưa chạy):

- Test command dùng `uv run python -m pytest` thay vì console `uv run pytest`
  vì console entrypoint không hoạt động với local package layout của repo
  (ModuleNotFoundError khi import `core`/`vectorstore`); precedent này đã được
  Reviewer chấp nhận ở Phase 4. Các command còn lại chạy đúng như guide.
- `retrieval.score_threshold: 0.0` giữ nguyên trong config nhưng không được áp
  dụng làm filter trong Phase 5: flow được duyệt quy định depth chính xác
  (top 10/30/10) và threshold filtering có thể trả ít hơn depth đó. Quyết định
  threshold/relevance cần evidence Phase 7-8.
- Stale detection: `verify_snapshot()` là entry point lifecycle explicit (không
  chạy per-request, không refit corpus); giờ bao gồm semantic config
  fingerprint. Re-init với corpus mới hợp lệ (vd sau reindex) tạo fingerprint
  mới và thành công - đây là behavior được test, không phải stale.
- `corpus_fingerprint` là `None` cho `dense_only` (profile không được phép
  scroll toàn corpus); `config_fingerprint` luôn có cho mọi profile.
- Reranker uniqueness: duplicate `chunk_id` input bị reject trước khi scorer
  chạy (`RetrievalDependencyError`); foreign document không thể xảy ra qua
  scorer API (output là subset của input theo thiết kế), report không claim cơ
  chế chống foreign riêng.

## Known Issues

- Severity: low. `uv run pytest` console entrypoint không hỗ trợ local package
  layout; canonical command là `uv run python -m pytest` từ `backend/` (đã có
  precedent Phase 4).
- Severity: low. Latency gate p95 <= 3 giây chưa chạy - đây là real validation
  gate cần approval riêng; không suy diễn pass từ fake scorer. Cold-load time
  của MiniLM chưa được đo.
- Severity: low. MiniLM không được thiết kế cho tiếng Việt và chỉ là local
  latency baseline; guide ghi rõ không tuyên bố chất lượng tiếng Việt ở
  Phase 5.
- Severity: low. `verify_snapshot` phải được gọi tường minh để phát hiện stale;
  service không tự gọi per-request (tránh network overhead mỗi request). Phase
  6 hoặc deployment cần chọn điểm gọi phù hợp.
- Severity: low. Payload projection chặn các field ngoài allowlist ở retrieval
  time, nhưng Qdrant collection vẫn lưu đủ payload từ Phase 4; không thay đổi
  schema collection.
- Severity: low. `config_fingerprint` mới trong snapshot: Codex nên xác nhận
  danh sách semantic config (top_k, candidate_multiplier, weights, rerank
  model/device/top_k) là đủ trước khi guide được đồng bộ.

## Security, Data Safety, Reliability, Performance Self-Check

- Security: không đọc/in/log query nguyên văn, context, credentials, headers
  hoặc provider payload. Error messages cố định, không chứa query hoặc
  exception detail nhạy cảm (exception gốc chỉ nằm trong `__cause__`). Log chỉ
  chứa profile + document count + snapshot fields an toàn. Metadata chỉ lấy
  safe allowlist; Qdrant query/scroll dùng payload projection.
- Data safety: không mutate collection, chunks hoặc retrieved input objects
  (hybrid/service/reranker tạo result objects mới; ContextBuilder chỉ đọc);
  purity đảm bảo bằng stub trả chính captured instances trong tests. Không tạo
  persistent cache artifact. Model load cache-only, không bao giờ download.
- Reliability: failure paths deterministic qua typed errors; non-numeric/
  non-finite scores từ dependency đều typed; không broad catch-to-empty; `[]`
  chỉ khi retrieval thành công không candidate; không silent fallback/profile
  switch; dense_only độc lập khi BM25/reranker chưa khởi tạo;
  config/collection/count/fingerprint thay đổi fail rõ (lúc init hoặc qua
  `verify_snapshot`).
- Performance: BM25 fit một lần lúc startup; không repeated model load
  (lru_cache); scroll bounded batch 128 `with_vectors=False`; candidate depth
  30, rerank 10 pairs, context 5 docs/3000 chars đều bounded; `verify_snapshot`
  không chạy per-request; không có work unbounded trong request path.
- Tests: 99 tests Phase 5 + 217 full regression đều offline bằng fakes, không
  cần secrets, paid API, deploy hoặc external services.
- Notebooks: JSON hợp lệ, nbformat validate pass, outputs rỗng, execution_count
  null, cell ids unique, default cells chỉ dùng fake dependencies, real mode
  opt-in bằng env guard và không chạy query.

## Live Access / Secrets Statement

```text
No live network/model/deploy/secret access occurred.
```

Không có model download, không chạy real Qdrant probes, không load real
E5/MiniLM, không gọi OpenAI/OpenRouter, không đọc `.env` hoặc bất kỳ secret
nào. Real Qdrant probes, E5/MiniLM real validation và latency measurement chưa
chạy vì chưa được user approve; không suy diễn pass từ fake scorer.

## Handoff To Codex

Codex nên re-review lại sau revision 3:

1. **Typed score boundary**: probe lại non-numeric score từ Qdrant (string/
   None) và reranker (string/None/object) - phải ra `RetrievalDependencyError`
   với safe fixed message, không `ValueError`/`TypeError` thô.
2. **Reranker uniqueness**: probe input `['a', 'a', 'b']` - phải bị reject
   trước khi scorer chạy; output với unique input phải unique.
3. **Model identity**: probe injected embedder `model_id="wrong-model"` - phải
   `RetrievalConfigurationError`.
4. **Config staleness**: probe đổi weights 0.7/0.3, top_k, reranking top_k -
   `verify_snapshot` phải `ComponentNotReadyError`; unchanged config vẫn pass.
   Xác nhận danh sách semantic config trong `_semantic_config` là đủ.
5. **Purity**: probe hybrid/service với stub trả cùng instances - objects
   không đổi, output là objects mới.
6. **Notebook**: cell IDs unique, nbformat validate, default mode chạy bằng
   fake, real mode guard `HUE_RAG_QDRANT_REAL=1`.
7. **Benchmark ledger**: chưa cập nhật vì không có actual evidence; chỉ nên
   ghi configuration/latency evidence khi real validation được approve.

Safe-default steps Codex/user dùng để verify phase:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/startup.py retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py reranking/base.py reranking/models/cross_encoder.py reranking/reranker.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_bm25.py tests/test_retrieval_service.py tests/test_reranker.py tests/test_context_builder.py tests/test_startup.py -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# Notebook default mode (an toàn, không cần Qdrant/model):
# mở notebooks/05_retrieval_profiles.ipynb và Run All
```

Real local validation (Qdrant read-only probes + MiniLM cache-only load +
latency gate) chỉ chạy sau khi user approve riêng; nếu chưa approve, report
ghi rõ check chưa chạy như trên. Phase 6 vẫn đóng; không tạo user report;
không cập nhật `Project_Status.md`.

Phase 5 status cho handoff: `implementation_reported` (revision 3). Implementer
không tự tuyên bố Phase 5 approved; technical acceptance chờ Codex re-review
và user confirmation.
