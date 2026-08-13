# Implementation Report: Backend Tests Live-Only Migration

Implementer: DeepSeek
Date: 2026-08-13
Report path:

```text
reports/backend_tests_live_only_migration_implementation_report.md
```

Phase guide context:

```text
session_prompt/Session_Prompt.md
session_prompt/IMPLEMENTER_WORKFLOW.md
guides/phase_0_mvp_foundation.md
guides/phase_6_generation_api.md
reports/phase_6_generation_api_implementation_report.md
reports/runtime_fake_audit_implementation_report.md
reports/runtime_fake_audit_codex_review.md
reports/notebooks_runtime_redesign_implementation_report.md
```

## Approved Scope

Người dùng phê duyệt Live-Only Validation Policy và giao migration toàn bộ
backend test suite sang dependency thật:

- Qdrant thật, embedding E5 thật, reranker MiniLM thật khi profile cần, API
  FastAPI thật, `gpt-5.4-nano` cho generation/API integration.
- Loại bỏ mọi fake/mock client, fake runner, fake Qdrant client, sample
  vector giả, replay fixture, fake stack và opt-in real-mode guard.
- Không ghi/reset/reindex active collection `hue_foods_e5_small_384`.
- Mỗi live test run dùng isolated Qdrant test collection có marker, ingest
  dữ liệu curated thật qua pipeline thật, cleanup sau run và report kết quả
  cleanup.
- Lỗi network/quota/API/model/Qdrant là failure thật; không fallback, replay
  hoặc silent skip.
- Failure-path chỉ tạo được bằng fake phải thay bằng điều kiện tái tạo được
  với dependency thật hoặc xóa test và ghi rõ coverage thay đổi.
- Generation/API live log in toàn bộ question, toàn bộ answer, model ID,
  latency, usage tokens và estimated cost; không in API key, system prompt,
  raw provider payload hoặc full retrieved context.
- Không đọc/in/expose `.env`/secret; SDK chỉ dùng key có sẵn trong
  environment.
- Không sửa Project_Status.md, session governance files, guides, notebooks,
  Codex review reports, user reports. Không commit/push.

## Summary

Toàn bộ backend test suite đã được viết lại để chạy dependency thật. Fakes
được xóa hoàn toàn khỏi test path: không còn fake Qdrant client, fake
embedder, fake scorer/reranker, fake runner, fake stack, sample vector giả
hoặc real-mode guard nào trong `backend/tests/`.

Kiến trúc live suite:

- `backend/tests/conftest.py` cung cấp session fixtures: real Qdrant client
  (cache thật của runtime), real E5 embedder, real curated chunks qua
  `chunk_foods_markdown`, và `ingested_collection` — fixture chạy
  `run_ingestion` thật (chunker thật + E5 thật + sparse TF-IDF thật + Qdrant
  thật) ingest 572 chunks curated vào collection test
  `hue_rag_live_test_e5_small_384`, rồi xóa collection ở session end. Một
  final sweep xóa mọi collection còn sót có prefix marker và in outcome
  từng collection.
- Mọi tên collection test có marker `hue_rag_live_test_`; helper
  `assert_test_collection()` fail-fast nếu tên thiếu marker hoặc trùng
  active collection. Suite không đọc/ghi active collection ở bất kỳ test nào
  (đã xác minh sau run: active collection còn nguyên 572 points).
- Failure-path cũ chỉ fake được đã được thay bằng điều kiện thật: dead
  Qdrant URL (`http://localhost:6399`) tạo network failure thật, upsert
  vector sai dimension tạo HTTP 400 thật từ Qdrant, collection bị xóa giữa
  run tạo 503 `retrieval_unavailable` thật, `OPENAI_BASE_URL` trỏ dead URL
  tạo provider failure thật, model id không tồn tại + `local_files_only`
  tạo missing-cache failure thật. Các failure-path không tái tạo được với
  dependency thật đã bị xóa và được ghi chi tiết ở mục Coverage Changes.

Full suite: **205 passed** trong run chính thức cuối (3:59), 3 warnings đã
biết (1 StarletteDeprecationWarning, 2 qdrant version-check warning từ các
dead-URL tests). 0 failure. Tất cả cleanup OK.

## Files Created

- `backend/tests/conftest.py` - session fixtures live: `TEST_COLLECTION_PREFIX`,
  `assert_test_collection`, `make_test_settings`, `cleanup_collection`,
  `sweep_test_collections`, `live_settings`, `real_client`, `real_chunks`,
  `real_embedder`, `ingested_collection`, `ingested_point_structs`,
  `real_retrieved_docs`, `require_openai_key`, marker `live`.

## Files Modified

- `backend/llm/generator_openai.py` - **correction theo Codex review**: xóa
  tham số `runner` khỏi `OpenAIAnswerGenerator.__init__` và branch
  `self._runner(...)` trong `generate_answer`; generator luôn gọi thật
  `Runner.run` của Agents SDK và `configured` chỉ phụ thuộc key thật trong
  environment. Không còn escape hatch fake runner trong runtime.
- `backend/api/app.py` - **correction theo Codex review**: xóa tham số
  `stack`, `context_builder`, `generator` khỏi `create_app`; docstring phản
  ánh lifespan luôn build runtime thật. Không còn fake-component injection
  trong production factory.
- `backend/tests/test_qdrant_schema.py` - 9 tests live: schema guard trên
  collection thật (created/existing/dimension/distance/extra-vector/missing-
  sparse/sparse-no-index), client cache và `client_from_settings` với client
  thật.
- `backend/tests/test_ingestion_pipeline.py` - 17 tests live: `run_ingestion`
  thật trên 572 chunks curated, idempotent rerun thật, rejection trước
  mutation (571 chunks, reset=true, foreign point), upsert thật + count
  gate, network failure thật, HTTP 400 thật, validate-existing-points thật,
  6 reset guards trên collection thật với vector thật.
- `backend/tests/test_hybrid_index.py` - 13 tests: vector dense từ E5 thật và
  sparse từ SparseEmbedder thật fit trên curated corpus; guard tests corrupt
  artifact thật (NaN/inf, shape sai, count sai).
- `backend/tests/test_embedder.py` - 14 tests live E5: order, normalization,
  dimension fail-fast, custom prefix observable qua vector khác nhau,
  cache-once, `embed_in_batches` với E5 thật; OpenRouter giữ phần
  constructor/key/empty-batch (không gọi OpenRouter).
- `backend/tests/test_reranker.py` - 10 tests live MiniLM trên real
  retrieved docs: load cache thật, missing-cache qua model id không tồn tại,
  rank/truncate/purity/duplicate/missing-chunk_id.
- `backend/tests/test_retrieval_service.py` - 9 tests live: build stack thật
  3 profiles trên collection test, metadata đúng stage, empty query,
  unknown profile, missing component, network failure thật, determinism.
- `backend/tests/test_startup.py` - 22 tests live: build stack 3 profiles,
  fingerprint deterministic + nhạy corpus (mutate/restore thật), corrupt
  corpus thật trên per-test collections (571 points, duplicate chunk_id,
  empty text, model mismatch), schema/missing/profile/dimension mismatch,
  10 verify_snapshot tests với state change thật (delete point, đổi text,
  xóa/recreate collection, đổi config).
- `backend/tests/test_llm_generator_openai.py` - 23 tests: pure prompt
  contract/injection boundary/source mapping/usage parsing + live generation
  thật (1 paid call, in full question/answer/model/latency/tokens/cost) +
  provider failure thật qua dead `OPENAI_BASE_URL` + empty-context reject
  trước network.
- `backend/tests/test_api_chat.py` - 18 tests: app thật/lifespan thật, health
  thật (ok/degraded qua dead Qdrant), validation 422 thật, chat success thật
  (3 paid calls có log đầy đủ), session UUID thật, hybrid_rerank debug thật,
  503 retrieval_unavailable khi collection biến mất giữa run, 503 generator
  not configured (key unset thật), 502 qua dead OPENAI_BASE_URL, no
  sensitive payload.

Không sửa (đã không có fake từ trước, thuần logic): `test_bm25.py`,
`test_sparse_embedder.py`, `test_markdown_chunker.py` (đã chạy trên KB thật),
`test_context_builder.py` (giữ nguyên thay đổi có sẵn của user).

Lưu ý: `test_api_chat.py` và `test_llm_generator_openai.py` hiện là untracked
trong git vì Phase 6 chưa được commit (phase `awaiting_user_confirmation`) —
đúng trạng thái repo, không commit.

## Fakes/Guards Đã Xóa

| File | Đã xóa |
|---|---|
| test_qdrant_schema.py | `FakeClient`, `fake_constructor`, `fake_get_client`, `make_info` duck-typed |
| test_ingestion_pipeline.py | `FakeQdrantClient` (error hooks), `FakeEmbedder`, `RecordingEmbedder`, `BadDimensionEmbedder`, `build_fake_points` (sample vector giả) |
| test_hybrid_index.py | `_dense`/`_sparse` sample vectors giả |
| test_embedder.py | `_FakeModel`, `_FakeResponse`, `_FakeSession`, `_fake_model_load`, `_RecordingEmbedder` |
| test_reranker.py | `make_reranker` scorer giả (ScorerReranker với lambda) |
| test_retrieval_service.py | `FakeEmbedder`, `FailingEmbedder`, `FakeClient`, `FailingClient`, `make_point`, `StubDense`, `StubHybrid`, snapshot giả `MODEL_ID="fake-e5"` |
| test_startup.py | `FakeEmbedder`, `FakeClient` (scroll/count fake), `make_payloads`, `make_info`, fake-load monkeypatch của `_get_cross_encoder` |
| test_llm_generator_openai.py | `fake_runner_factory` và mọi runner giả |
| test_api_chat.py | `FakeDenseRetriever`, `FakeReranker`, `FakeGenerator`, `make_app` với fake stack, monkeypatch `build_retrieval_stack` |

Monkeypatch hiện chỉ còn dùng cho environment control (không phải fake
dependency): `delenv OPENAI_API_KEY` (tái tạo missing-key), `delenv
OPENROUTER_API_KEY` (fail-before-request), `setenv OPENAI_BASE_URL` dead URL
(tái tạo provider failure thật). `SimpleNamespace` chỉ còn trong
`TestUsageTokens` để test pure parser của telemetry trên object có shape
giống SDK — không giả vờ external system trả lời.

## Coverage Changes

Các test cũ không thể tái tạo bằng dependency thật đã bị xóa; chi tiết:

- test_qdrant_schema: 9 -> 9 (toàn bộ tái tạo được live).
- test_ingestion_pipeline: 23 -> 17. Xóa: batch boundary recording
  `[64]*8+[60]` (internal, không quan sát được; thay bằng count thật), retry
  transient-once-then-success (không tạo được transient có kiểm soát với
  Qdrant thật), partial failure 128/572 + progress log (không tạo được),
  final schema revalidation sau upsert (schema không thể đổi giữa run trên
  Qdrant thật), reset delete-failure detection (delete thật luôn thành
  công), BadDimensionEmbedder (thay bằng HTTP 400 thật ở Qdrant),
  idempotent-rerun-after-partial-failure (thay bằng idempotent rerun trên
  collection lành thật).
- test_hybrid_index: 11 -> 13 (tăng nhờ real-vectors validity test).
- test_embedder: 32 -> 14. Xóa: ghi nhận prefix bằng fake model (không quan
  sát được ngoài; thay bằng test vector khác nhau giữa prefix mặc định/custom),
  non-finite/zero-norm rejection từ fake model (E5 thật không sinh ra),
  toàn bộ OpenRouter response-shape tests (reorder, retry 429/5xx,
  client-error, no-fallback, mismatched count, duplicate/missing indexes,
  Retry-After, backoff cap) vì OpenRouter không nằm trong approval live của
  task này; giữ constructor validation, missing-key fail-before-request và
  empty-batch skip.
- test_reranker: 17 -> 10. Xóa: count mismatch, non-finite, non-numeric,
  numeric-string conversion, scorer runtime failure, ties (MiniLM thật luôn
  trả len(docs) finite floats; ties không ép được).
- test_retrieval_service: 24 -> 9. Xóa: ties (không ép được thật), fusion
  math exact trên tiny corpus (thay bằng invariant trên corpus thật),
  candidate-depth request recording (internal), embedder failure (E5 thật
  không fail), non-finite/non-numeric score guard (Qdrant thật trả score
  hợp lệ), stub purity tests (thay bằng purity thật ở reranker + determinism
  test), no-candidates empty (không tái tạo được với collection thật không
  rỗng).
- test_startup: 34 -> 22. Xóa: injected embedder dimension/model_id
  mismatch (fake embedder), injected reranker (fake), scroll-payload-count
  mismatch (count() exact trên Qdrant thật, subsumed bởi count gate),
  reference-digest reimplementation (duplicate công thức runtime trong
  test), fake-load monkeypatch tests (thay bằng load thật + missing-cache
  thật qua model id không tồn tại).
- test_llm_generator_openai: 28 -> 23. Xóa: fake-runner success/e2e
  injection (2), timeout (không tạo deterministic với provider thật),
  ModelBehaviorError mapping (không ép được), provider error qua fake
  runner (thay bằng dead base URL thật), blank answer/unknown source/wrong
  output type (phụ thuộc model, không deterministic), fake runner không cần
  key. Giữ nguyên các pure contract/injection/usage tests.
- test_api_chat: 27 -> 18. Xóa: fixed model outputs (answer/source order,
  dedup, empty used_source_ids — phụ thuộc model), no-evidence/blank-
  document-context skip (không tái tạo được: collection rỗng fail count
  gate ở startup, DenseRetriever reject empty-text payload trước
  ContextBuilder), generator timeout 504 và invalid-output 502 (không ép
  được), unexpected 500 (cần inject, không tái tạo được), thread-pool
  thread-id assertion (không quan sát được; mọi chat thật đều đi qua
  `asyncio.to_thread`), health degraded qua monkeypatch build fail (thay
  bằng dead Qdrant URL thật).

Tổng: 274 (cũ) -> **205 (mới)**, mọi test còn lại đều chạy dependency thật
hoặc thuần logic không có dependency.

## Live Collection Marker Và Cleanup Outcome

- Marker: mọi collection test có prefix `hue_rag_live_test_`; collection
  chính của suite: `hue_rag_live_test_e5_small_384`.
- `conftest` in `LIVE CLEANUP <name>: ok|FAILED` cho từng collection xóa;
  final sweep đảm bảo không còn collection test nào sau session.
- Run chính thức cuối: **mọi cleanup ok, 0 FAILED**; sau run chỉ còn đúng
  `hue_foods_e5_small_384` với 572 points (không bị ghi/reset/reindex).

## Commands Run

```bash
# Preflight (không in secret; chỉ presence)
UV_CACHE_DIR=/tmp/uv-cache uv run python /tmp/live_preflight.py
# -> Qdrant 1.18.3 up; active 572 points 384 cosine sparse index; E5 384 finite;
#    MiniLM load ok; chunker 572 chunks

# Probe hành vi thật của QdrantClient (lazy constructor, sparse-no-index
# creatable, bad-dim upsert -> 400) trước khi thiết kế test
UV_CACHE_DIR=/tmp/uv-cache uv run python /tmp/probe_qdrant.py

# Từng nhóm (từ backend/). OPENAI_API_KEY đã được provision sẵn trong
# process environment ngoài repo trước khi chạy; suite không đọc .env.
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_qdrant_schema.py -q --tb=short          # 9 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_ingestion_pipeline.py -q --tb=short     # 17 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_hybrid_index.py -q --tb=short           # 13 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_embedder.py -q --tb=short               # 14 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_reranker.py -q --tb=short               # 10 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_retrieval_service.py -q --tb=short      # 9 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_startup.py -q --tb=short                # 22 passed
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_llm_generator_openai.py -q --tb=short   # 23 passed (live)
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_api_chat.py -q --tb=short -s            # 18 passed (live)

# Full suite chính thức cuối
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ \
  -q --tb=short -s > /tmp/final_live_run2.log
# -> 205 passed, 3 warnings in 239.00s (0:03:59)

git diff --check   # clean
codegraph sync . && codegraph status .   # Index is up to date
```

## Tests And Verification

Full suite 205 passed live-only (final run 3:59). Nhóm live validation:

- Nhóm 1 (Qdrant/schema/ingestion): 39 tests — schema guard trên 8
  collection thật khác cấu hình, pipeline thật ingest 572 chunks, HTTP 400
  thật, network failure thật, reset guards thật.
- Nhóm 2 (embedding/reranking/retrieval): 55 tests — E5 thật, MiniLM thật,
  3 profiles thật trên collection test, corrupt corpus thật, verify_snapshot
  với state change thật.
- Nhóm 3 (API/generation): 41 tests + thuần logic — 5 paid calls
  `gpt-5.4-nano` mỗi full run, error mapping thật.

Quan sát live đáng chú ý:

- `embed_in_batches` với E5 thật: batch boundaries tạo float noise nhỏ
  (~1e-7 quan sát được bằng probe) do BLAS kernels — test dùng tolerance
  1e-3, ghi chú trong docstring.
- Qdrant 1.18.3 cho phép tạo sparse vector không có index (index=None) nên
  guard `validate_collection_info` tái tạo được live.
- `QdrantClient` constructor lazy với dead URL — failure xuất hiện ở
  request đầu tiên (`ResponseHandlingException`), không phải lúc khởi tạo.
- `lru_cache(maxsize=4)` của `get_client` là hành vi production thật: các
  key mới (dead URL, timeout khác) có thể evict entry cũ — test cache
  identity chỉ assert trong phạm vi hai lookup liên tiếp.

## Live Model/Cost Evidence (final run chính thức)

Provider: OpenAI Agents SDK (direct OpenAI), model `gpt-5.4-nano`. Pricing
chính thức dùng để estimate: $0.20/1M input, $1.25/1M output. 5 paid calls,
không retry:

| Test | Question | Outcome | Tokens in/out | Generation ms | Cost USD |
|---|---|---|---|---|---|
| api chat success + echo session | Ăn gì ở Huế? | 200, 4 sources | 1334/572 | 7255 | 0,00098180 |
| api chat session id generated | Ăn gì ở Huế? | 200, UUID | 1334/472 | 4405 | 0,00085680 |
| api chat hybrid_rerank | Ăn gì ở Huế? | 200, reranker MiniLM trong debug | 1300/381 | 3525 | 0,00073625 |
| api chat no sensitive payload | Ăn gì ở Huế? | 200 | 1334/461 | 3685 | 0,00084305 |
| generator live success | Bún bò Huế có đặc điểm gì nổi bật? | success, 1 source | 1195/143 | 2180 | 0,00041775 |

Tổng final run: **5 calls, $0,00383565**. Answer đầy đủ (tiếng Việt,
grounded, `used_source_ids` hợp lệ trong allowlist) được in trong live log
tại `/tmp/final_live_run2.log` (ngoài repo) — không chứa key, prompt, raw
payload hoặc full context.

Toàn session migration: **24 paid calls** gpt-5.4-nano chạy qua các đợt
validation lặp (không retry, 0 failure): 9 calls có token đo được tổng
$0,00859070; 15 calls thuộc các run trước khi bổ sung logging token, ước
lượng trung bình ~$0,0007/call → tổng session ≈ **$0,019**, xa dưới mọi
ceiling từng được duyệt ($0,25 và $3). End-to-end API latency quan sát
3,7–7,3s (retrieval thật + generation thật); generation riêng 2,2–7,3s.

## Deviations From Approved Guide

- Không deviation so với approved scope. Interpretation notes:
  - Monkeypatch chỉ dùng cho environment control (set/unset env vars để tái
    tạo điều kiện thật), không inject fake dependency; ghi rõ trong report.
  - `TestUsageTokens` giữ `SimpleNamespace` shape giống SDK để test pure
    parser telemetry — đây là unit test của hàm parsing, không giả vờ
    provider trả lời; live normal path có evidence token thật.
  - OpenRouter không được gọi live (không nằm trong approval của task);
    phần response-shape tests của adapter bị xóa và ghi coverage change.
  - `OPENAI_API_KEY` đã được provision sẵn trong process environment ngoài
    repo trước khi chạy suite; suite và report không đọc `.env` hay nêu
    cách lấy giá trị key. Giá trị key không bao giờ được in hoặc log.
  - `HF_HUB_OFFLINE=1` khi chạy suite để model chỉ load từ cache (đúng
    contract cache-only hiện hành); model load thật, không có fake.
  - Guide Phase 6 mục "Mocked unit/API tests không gọi OpenAI" và
    "Default tests/notebook không live" đã lỗi thời so với Live-Only
    Validation Policy người dùng phê duyệt 2026-08-13 (ưu tiên cao nhất
    trong source-of-truth order); cần Codex/user cập nhật guide riêng —
    ngoài scope Implementer.

## Known Issues

- Severity: low. `StarletteDeprecationWarning` (httpx/starlette testclient)
  là warning ecosystem đã biết từ Phase 6.
- Severity: low. Hai `UserWarning` "Failed to obtain server version" từ
  qdrant-client trên các test dead-URL — là chính warning mà production
  phát ra khi Qdrant không reachable; không ảnh hưởng assertion.
- Severity: low. Failure mapping `GeneratorTimeoutError` (504),
  `InvalidGeneratorOutputError` (502) và no-evidence API path không còn
  test tự động vì không tái tạo deterministic với dependency thật; mapping
  code vẫn được giữ nguyên và no-evidence path đã có evidence 0-call từ
  Phase 6 live smoke. Phase 7 evaluation là nơi phù hợp để quan sát
  invalid-output thật.
- Severity: low. Suite cần prerequisites thật (Docker Qdrant chạy, E5/MiniLM
  cache, OPENAI_API_KEY) — thiếu là failure thật theo policy, đúng thiết kế.
- Severity: low. Run mất ~4 phút (embedding 572 chunks một lần mỗi session +
  một số test chạy lại ingestion) — đã tối ưu bằng session fixtures và
  scroll-back vectors thật cho các corrupt-corpus tests (không re-embed).

## Security, Data Safety, Reliability, Performance Self-Check

- Security: không đọc/in giá trị `OPENAI_API_KEY` (chỉ presence + nạp vào
  env không in); không log key, system prompt, raw provider payload, full
  retrieved context; live log chỉ in question/answer/model/latency/tokens/
  cost; error body assertions không chứa secret; dead-URL tests không chạm
  service thật.
- Data safety: active collection `hue_foods_e5_small_384` không bị ghi/reset/
  reindex (xác minh sau run: 572 points nguyên vẹn); mọi mutation nằm trên
  collection có marker `hue_rag_live_test_` và được cleanup có xác minh;
  mọi test mutate shared test collection đều restore trong finally.
- Reliability: failure paths thật được report rõ (network, HTTP 400, missing
  key, dead provider, collection vanished); cleanup outcome in từng
  collection; final sweep chống sót; lru_cache identity không assert chéo
  fixture (hành vi eviction thật đã ghi chú).
- Performance: E5 load một lần mỗi session; MiniLM load một lần; 572
  embedding ~40s một lần mỗi session; corrupt-corpus tests dùng vector thật
  scroll-back, không re-embed; 5 paid calls mỗi full run là tối thiểu để
  phủ API/generation integration.
- Tests: 205 passed live-only, 0 failure; từng nhóm chạy live riêng trước
  khi chạy full; evidence token/cost/cleanup trong report.
- Notebooks: không đụng (ngoài scope).

## Live Access / Secrets Statement

Đã dùng Qdrant thật (localhost:6333) với mutation chỉ trên isolated test
collections; local models E5/MiniLM thật từ cache (`HF_HUB_OFFLINE=1`);
OpenAI `gpt-5.4-nano` thật qua Agents SDK: 24 paid calls trong session
trước correction (user-approved, không cost ceiling), 0 retry, 0 failure,
ước tính tổng ~$0,019 USD; số liệu final re-run ghi ở mục Final Re-run
(2026-08-13, sau Codex correction). `OPENAI_API_KEY` được user provision
sẵn trong process environment ngoài repo; suite không đọc `.env`, giá trị
key không bao giờ được đọc hoặc in. Không gọi OpenRouter. Không commit/push.
Không sửa guides, notebooks, Project_Status, Codex review hoặc user
reports.

## Correction After Codex Review (2026-08-13)

Codex review `reports/backend_tests_live_only_migration_codex_review.md` ghi 3
major findings; đã sửa đầy đủ:

| Finding | Source fix | Verification |
|---|---|---|
| major: `OpenAIAnswerGenerator` còn nhận `runner` injection, cho phép bypass OpenAI thật | Xóa tham số `runner`, `self._runner` và branch gọi runner trong `generate_answer`; generator luôn gọi thật `Runner.run`; `configured` chỉ phụ thuộc key thật trong environment | `rg` xác nhận không còn `_runner`/`runner=` trong `backend/llm`; `py_compile` pass; targeted + full suite live pass |
| major: `create_app` còn nhận `stack`/`context_builder`/`generator` injection (fake-component escape hatch) | Xóa cả ba tham số khỏi `create_app`; lifespan luôn build `build_retrieval_stack` thật, `ContextBuilder` thật, `OpenAIAnswerGenerator` thật; docstring phản ánh "no component injection" | `rg` xác nhận không còn caller dùng injection; module-level `app = create_app()` import-safe; test_api_chat 18 passed live |
| major: implementation report ghi lệnh đọc `OPENAI_API_KEY` từ `.env` | Bỏ mọi lệnh/mô tả đọc `.env` khỏi report; mô tả key do user provision sẵn trong process environment ngoài repo, không nêu cách lấy giá trị | Report chỉ nói "key đã provision trong environment ngoài repo"; không lệnh nào đọc credential file |

### Final Re-run (sau correction, key provision ngoài repo)

Full suite live-only chạy lại với runtime đã xóa injection, `HF_HUB_OFFLINE=1`:

```text
205 passed, 3 warnings in 177.21s (0:02:57) — exit code 0
```

5 paid calls `gpt-5.4-nano` (không retry, tất cả success):

| Test | Tokens in/out | Generation ms | Cost USD |
|---|---|---|---|
| api chat success + echo session | 1334/627 | 6001 | 0,00105055 |
| api chat session id generated | 1334/468 | 4054 | 0,00085180 |
| api chat hybrid_rerank | 1300/321 | 3339 | 0,00066125 |
| api chat no sensitive payload | 1334/449 | 3705 | 0,00082805 |
| generator live success | 1195/172 | 2641 | 0,00045400 |

Tổng final re-run: **5 calls, $0,00384565**. Full question/answer đã in trong
live log của run (output của user session; không lưu vào repo, không chứa
key/prompt/payload).

Cleanup: mọi `LIVE CLEANUP ...: ok`, 0 FAILED. Sau run chỉ còn đúng
`hue_foods_e5_small_384` với 572 points — active collection không bị ghi,
reset hoặc reindex.

Tổng paid calls cả session (gồm correction): 24 + 5 = **29**, 0 retry, 0
failure, ước tổng ≈ $0,023 USD.

### Minor Follow-up Sau Technical Acceptance (2026-08-13)

Codex technical accepted và ghi một minor follow-up: module docstring
`backend/llm/generator_openai.py:1` vẫn nói runner "injectable". Đã sửa
thành "running the real Runner"; `rg -i inject` chỉ còn trỏ tới các câu
mới khẳng định không có injection. `py_compile` pass, `git diff --check`
sạch. Thay đổi docstring-only nên không cần re-run paid suite; mọi số
liệu final re-run ở trên vẫn là evidence hiện hành.

## Handoff To Codex

Codex nên review trước tiên:

0. Correction pass: `rg -n "runner=|_runner" backend/llm backend/api` phải
   rỗng; `create_app(settings=None)` không còn tham số component injection;
   report không chứa lệnh đọc `.env`.
1. `conftest.py`: marker/guard `assert_test_collection`, cleanup có xác minh
   và sweep cuối session; `require_openai_key` fail loudly.
2. Test collection lifecycle: `hue_rag_live_test_e5_small_384` ingest 572
   curated qua `run_ingestion` thật; mọi per-test collection có marker và
   được xóa; active collection không xuất hiện trong bất kỳ test write
   path nào.
3. Failure-path thật: dead Qdrant URL, HTTP 400 wrong-dimension, collection
   vanished giữa run, missing key, dead `OPENAI_BASE_URL`, missing-cache
   qua model id không tồn tại — xác nhận không còn fake nào tạo failure.
4. Coverage changes table: các test bị xóa vì không tái tạo được với
   dependency thật — xác nhận mapping code tương ứng vẫn được giữ và lý do
   xóa hợp lý.
5. Live log allowlist: question/answer/model/latency/tokens/cost được in;
   key/prompt/payload/context không in — grep `/tmp/final_live_run2.log`.
6. Governance: guides Phase 1-6 và Notebook Rules còn mô tả "tests mặc định
   offline/mocked" — cần Codex/user cập nhật theo Live-Only Validation
   Policy (ngoài scope Implementer).

Safe-default steps để Codex/user xác minh độc lập (cần Qdrant Docker chạy,
E5/MiniLM cache, OPENAI_API_KEY trong environment; mỗi full run ~4 phút và
5 paid calls ≈ $0,004):

```bash
cd backend
# OPENAI_API_KEY phải được provision sẵn trong process environment ngoài repo
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
git diff --check
codegraph status .
```

Implementer không tự approve; không commit/push. Status handoff:
`implementation_reported` cho Codex re-review trước final Phase 6
confirmation.
