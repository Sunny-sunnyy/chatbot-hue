# Implementation Report: Phase 4 Qdrant Ingestion

Implementer: DeepSeek
Date: 2026-08-12
Report path:

```text
reports/phase_4_qdrant_ingestion_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_4_qdrant_ingestion.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md  # not modified; ledger update is outside Implementer scope
```

## Approved Scope

Implement Phase 4 Qdrant ingestion theo contract đã được user/Codex phê duyệt tại
`guides/phase_4_qdrant_ingestion.md` (Status: `ready`, Level 2 brainstorming hoàn
tất): đưa 572 canonical food chunks cùng dense/sparse representations vào một
active Qdrant collection `hue_foods_e5_small_384`, với schema kiểm chứng được,
reset safety fail-closed qua command riêng, notebook an toàn và hai live approval
gates tách biệt.

Exact allowlist (sau khi Codex mở rộng `pyproject.toml` và `uv.lock`):

```text
docker-compose.yml
backend/config/settings.yaml
backend/config/README_config.md
backend/vectorstore/qdrant.py
backend/vectorstore/hybrid_index.py
backend/vectorstore/upsert.py
backend/vectorstore/reset.py
backend/ingestion/pipeline.py
backend/tests/test_qdrant_schema.py
backend/tests/test_hybrid_index.py
backend/tests/test_ingestion_pipeline.py
notebooks/04_qdrant_ingestion.ipynb
reports/phase_4_qdrant_ingestion_implementation_report.md
pyproject.toml
uv.lock
```

## Summary

Phase 4 đã implement đủ contract pre-mutation và postcondition:

- `qdrant.py`: client cache theo `(url, timeout)`, availability/schema
  validation, `ensure_collection` chỉ tạo collection khi absent.
- `hybrid_index.py`: deterministic point builder (UUID5 từ `hue-rag:<chunk_id>`),
  validate chunks, dense/sparse vectors và exact payload fields trước khi build.
- `upsert.py`: batch 64, `wait=True`, timeout 30, một retry chỉ cho
  `httpx.TransportError`; partial failure log safe progress và re-raise nguyên
  gốc; exact count gate.
- `reset.py`: destructive command riêng, chỉ delete exact collection sau khi
  confirmation string, schema, payload identity và count đều khớp; verify
  collection biến mất sau delete.
- `ingestion/pipeline.py`: orchestration theo thứ tự bắt buộc — chunk IDs →
  canonical count 572 → sparse fit → dense embed → build_points (validate toàn
  bộ) → client → ensure collection → validate existing subset → upsert → final
  schema revalidate → exact count verify. Không bao giờ delete/recreate.
- `docker-compose.yml`: Qdrant v1.18.3 pinned bằng exact digest, storage riêng
  `./qdrant_storage`.
- Config: `vector_database` canonical (`reset_collection: false`), README bỏ
  hướng dẫn cũ `reset_collection: true`.
- Dependency cleanup: gỡ PyPI `vectorstore==0.0.0` khỏi `pyproject.toml` +
  `uv.lock` bằng `uv remove`; local `backend/vectorstore/` import đúng.

## Files Created

- `docker-compose.yml` - Qdrant v1.18.3 pinned digest, ports 6333/6334, volume `./qdrant_storage`.
- `backend/vectorstore/qdrant.py` - client factory/cache, schema validation, guarded create.
- `backend/vectorstore/hybrid_index.py` - deterministic point builder + chunk/vector validation.
- `backend/vectorstore/upsert.py` - batch upsert, transient-only retry, progress logging, count gate, existing-subset validation.
- `backend/vectorstore/reset.py` - exact-target reset command (CLI) với guards fail-closed.
- `backend/ingestion/pipeline.py` - orchestration Phase 2-4, canonical count 572, final postconditions, CLI entry.
- `backend/tests/test_qdrant_schema.py` - 9 tests (client cache mock hoàn toàn, schema, create/absent, fail-closed).
- `backend/tests/test_hybrid_index.py` - 12 tests (UUID5, chunk/vector validation, exact payload).
- `backend/tests/test_ingestion_pipeline.py` - 23 tests (upsert batch/retry/count, pipeline order, regression, reset guards).
- `notebooks/04_qdrant_ingestion.ipynb` - 15 cells, notebook Phase 4 canonical.
- `reports/phase_4_qdrant_ingestion_implementation_report.md` - report này.

## Files Modified

- `backend/config/settings.yaml` - `vector_database` canonical: `hue_foods_e5_small_384`, `reset_collection: false`, `timeout: 30`, `upsert_batch_size: 64`, `upsert_max_retries: 1`.
- `backend/config/README_config.md` - mô tả `vector_database` mới; thay hướng dẫn reindex cũ bằng quy trình reset command 4 bước; cấm `reset_collection: true`.
- `pyproject.toml` - gỡ dependency `vectorstore` (PyPI 0.0.0 shadowing local package); allowlist mở rộng bởi Codex.
- `uv.lock` - entries `vectorstore` bị xóa bởi `uv remove`; không sửa dependency khác.

## Notebooks Created Or Modified

- `notebooks/04_qdrant_ingestion.ipynb` - tạo mới, 15 cells:
  - Default mode (offline): settings, chunking thật (572 chunks), UUID5
    determinism, build_points trên 2 chunk thật với fake dense vectors +
    `SparseEmbedder` thật, `expected_schema` — không load E5, không gọi Qdrant,
    không network/model API.
  - Real mode opt-in bằng `HUE_RAG_QDRANT_REAL=1`: chỉ inspect read-only
    (`get_collection`, `count`, `scroll`) collection do ingestion tạo. Không có
    reset/delete cell.
  - Outputs rỗng, `execution_count = null`, markdown tiếng Việt kèm expected
    output.
  - User tự kiểm tra: mở notebook, chạy Run All ở default mode — kỳ vọng 572
    chunks, UUID5 deterministic, sample point đúng payload, real-mode cell báo
    skip; sau khi live ingestion, set `HUE_RAG_QDRANT_REAL=1` để inspect
    read-only collection.

## Commands Run

```bash
# Config / compose
docker compose config

# Non-live verification (từ backend/)
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile vectorstore/qdrant.py vectorstore/hybrid_index.py vectorstore/upsert.py vectorstore/reset.py ingestion/pipeline.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_qdrant_schema.py tests/test_hybrid_index.py tests/test_ingestion_pipeline.py -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short

# Dependency cleanup
UV_CACHE_DIR=/tmp/uv-cache uv remove vectorstore

# Notebook verify
UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute --output /tmp/nb04_executed.ipynb notebooks/04_qdrant_ingestion.ipynb

# Live Gate 2 (do Codex chạy, exit code 0)
cd backend
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -m ingestion.pipeline

# CodeGraph checkpoint
codegraph status .
codegraph sync .
codegraph status .
```

Lưu ý canonical test command: `uv run python -m pytest` (từ `backend/`). Console
entrypoint `uv run pytest` không hỗ trợ local package layout — đã được Reviewer
chấp nhận, không phải regression.

## Tests And Verification

Mocked / non-live (đạt):

- `py_compile` 5 module Phase 4: pass.
- 44 Phase 4 tests (12 hybrid_index + 9 qdrant_schema + 23 ingestion_pipeline): pass, không warning Qdrant.
- 118 full backend tests (74 Phase 1-3 + 44 Phase 4): pass, không warning Qdrant.
- `docker compose config`: pass.
- Notebook: 15 cells, schema-valid (nbformat 4.5), outputs rỗng,
  `execution_count=null`, không reset/delete cell, default mode non-live; đã
  execute thành công ở default mode.
- `git diff --check`: sạch.
- Allowlist audit: chỉ files trong approved allowlist được tạo/sửa; governance
  files, deletions `knowledge-base/`, notebooks 01-02 và `skills/` là thay đổi có
  sẵn được giữ nguyên.
- CodeGraph: index up to date (43 files, 513 nodes, 1336 edges theo evidence
  Reviewer).

Live Gate 1 (do Codex Reviewer chạy, approval riêng):

- Container `hue_rag-qdrant-1`, exact image
  `qdrant/qdrant@sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286`,
  Qdrant 1.18.3, REST localhost:6333 HTTP 200, ports 6333/6334 đúng.
- Configured qdrant-client kết nối thành công.
- Trước ingestion server không có collection nào. Không mutation ngoài container start.

Live Gate 2 (do Codex Reviewer chạy, approval riêng):

- `python -m ingestion.pipeline` exit code 0, E5 load từ cache offline
  (`HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`), không download model.
- Collection `hue_foods_e5_small_384` status green; exact point count 572;
  dense `['dense']` size 384 distance Cosine; sparse `['sparse']` index enabled;
  `points_count` metadata 572.
- Read-only full identity audit: 572/572 IDs khớp exact expected set;
  payload identity valid trên toàn bộ points; `embedding_model =
  intfloat/multilingual-e5-small`, `embedding_dimension = 384`; payload keys
  đúng contract (text, chunk_id, source, title, section, category,
  subcategory, chunk_type, embedding_model, embedding_dimension).

Live checks KHÔNG chạy (đúng hard stop):

- Không live rerun để chứng minh idempotency (chỉ mock-tested).
- Không live reset/delete để chứng minh guard (chỉ mock-tested).
- Không gọi OpenAI/OpenRouter/web.
- Không tác động `llm_rag` hoặc `nmk_chatbot_collection`.

## Evaluation Results

Phase 4 không có retrieval/answer evaluation trong scope — các metric
(Recall/MRR/nDCG, LLM-judge) thuộc Phase 5-7. Không tuyên bố retrieval quality,
benchmark winner hoặc native sparse retrieval.

```text
Retrieval result file: (none - Phase 7)
Answer result file: (none - Phase 7)
Benchmark log updated: NO - reports/hue_foods_rag_benchmark.md ngoài Implementer scope; cần Reviewer cập nhật registry/ledger với Gate 2 evidence
```

## Deviations From Approved Guide

```text
1. pipeline.py có thêm CLI entry (`python -m ingestion.pipeline`) - cần thiết
   để live Gate 2 chạy được; đã báo trong non-live handoff.
2. pyproject.toml + uv.lock được sửa để gỡ PyPI `vectorstore==0.0.0`
   (shadowing local package) - allowlist được Codex mở rộng chính thức.
3. `uv run pytest` console entrypoint không hoạt động với local package layout;
   canonical command là `uv run python -m pytest` (đã được Reviewer chấp nhận).
```

Không có deviation nào khác; không thay đổi provider, model, dimension, schema,
collection name, batch/retry policy hoặc acceptance criteria.

## Known Issues

- Reset safety chỉ được chứng minh bằng mocked tests; chưa có live reset test
  (cố ý: không chạy live deletion chỉ để validation). Severity: low - guards
  fail-closed được mock-test đầy đủ, live deletion luôn cần approval riêng.
- Live idempotent rerun chưa chạy; idempotency dựa trên deterministic UUID5 và
  mocked regression test (partial failure -> rerun -> 572). Severity: low -
  không block Phase 4 vì upsert đã đạt exact count 572.
- Collection `hue_foods_e5_small_384` và Qdrant container hiện đang tồn tại/chạy;
  mọi thay đổi model/dimension sau này phải qua reset command + approval.
- Benchmark ledger (`reports/hue_foods_rag_benchmark.md`) chưa được cập nhật -
  ngoài Implementer scope; Reviewer cần nối model/collection metadata và
  ingestion run summary vào ledger.
- Sparse vectors được lưu nhưng KHÔNG có native sparse retrieval run nào; Phase 5
  vẫn dùng dense candidates + Python BM25 (đúng Sparse storage boundary).

## Security, Data Safety, Reliability, Performance Self-Check

- Security: không đọc/in/log secrets, credentials, headers; không có API key
  trong settings/report; no live OpenAI/OpenRouter/web call.
- Data safety: chỉ index curated answer-facing chunks; payload không chứa
  absolute private path; log chỉ chứa count/summary, không log full point,
  vector, payload hoặc corpus.
- Reliability: failure paths deterministic (count gate, schema fail-closed,
  canonical count, pre-mutation validation); partial upsert không báo success;
  rerun idempotent nhờ UUID5; reset fail-closed exact target.
- Performance: batch 64 bounded, một retry transient, không concurrency
  framework; 572 points upsert một pass; không repeated expensive model loads
  (client + model cached một lần).
- Tests: default verification không cần secrets, paid calls, deploy hoặc
  external services; toàn bộ mocked (Qdrant client mock hoàn toàn, không chạm
  live boundary).
- Notebooks: JSON hợp lệ, outputs rỗng, execution counts null, default cells
  safe, real mode opt-in read-only, không reset/delete cell.

## Live Access / Secrets Statement

Live Qdrant preflight (Gate 1) và live ingestion (Gate 2) đã được Codex Reviewer
chạy sau approval riêng, đúng policy: chỉ Qdrant local pinned + E5 offline từ
cache, không gọi OpenAI/OpenRouter/web, không reset/delete, không tác động
`llm_rag`/`nmk_chatbot_collection`. Không có secret nào được đọc, in, log hoặc
commit. Không có dependency install mới ngoài `uv remove vectorstore` (cleanup).

## Handoff To Codex

Codex nên review trước tiên:

1. Live evidence Gate 1/Gate 2 và read-only identity audit đối chiếu với
   `ensure_collection`/`verify_point_count`/postcondition flow.
2. Regression corrections (canonical count, pre-mutation order, final schema
   revalidate, partial-failure logging) trong `pipeline.py` và `upsert.py`.
3. Reset guards trong `reset.py` (chỉ mock-tested - cần xác nhận đây là
   accepted limitation).
4. `pyproject.toml`/`uv.lock` cleanup (surgical, không đụng dependency khác).
5. Cập nhật `reports/hue_foods_rag_benchmark.md` với Gate 2 evidence (ngoài
   Implementer scope).

Canonical notebook: `notebooks/04_qdrant_ingestion.ipynb` - chạy default mode
(offline, 572 chunks, sample point, schema), sau đó real mode read-only với
`HUE_RAG_QDRANT_REAL=1` để inspect collection đã tồn tại.

Risk areas: live rerun idempotency chưa chứng minh live; reset safety chỉ
mock-tested; benchmark ledger chưa nối evidence. Phase 5 vẫn đóng cho đến khi
Phase 4 được technical review và user confirmation.
