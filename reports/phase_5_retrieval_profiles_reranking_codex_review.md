# Codex Review: Phase 5 Retrieval Profiles And Reranking

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-12 +07
Review round: revision 3 re-review
Review path:

```text
reports/phase_5_retrieval_profiles_reranking_codex_review.md
```

Implementer report:

```text
reports/phase_5_retrieval_profiles_reranking_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_5_retrieval_profiles_reranking.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
```

## Tóm Tắt

Revision 3 đã sửa các findings còn lại của vòng trước. Reviewer probes xác nhận
non-numeric/non-finite scores đều thành typed errors, duplicate reranker input
bị reject trước scorer, wrong embedder model ID bị reject và semantic retrieval
config changes làm snapshot stale. Purity tests hiện giữ đúng object identity.

Technical verdict là `ready_for_user_confirmation`. BM25/fusion, ba profile,
context builder, startup lifecycle, payload projection, cache-only reranker,
typed failures và notebook safe-default đạt contract offline. Targeted tests
đạt 99/99; full backend regression đạt 217/217.

Real Qdrant probes, E5/MiniLM validation và p95 latency gate chưa chạy. Codex
không yêu cầu mở real gate trong vòng review này vì offline blockers phải được
sửa trước.

## Findings

Không có blocker hoặc major findings.

- minor, accepted for MVP: `config_fingerprint` dùng một conservative shared
  retrieval config cho mọi profile. Vì vậy `dense_only` cũng được đánh dấu
  stale nếu chỉ fusion weights/candidate multiplier thay đổi dù profile này
  không dùng BM25. Behavior này không làm sai retrieval result, không chạy mỗi
  request và chỉ yêu cầu restart dư khi lifecycle verifier được gọi. Có thể làm
  fingerprint profile-aware sau nếu vận hành thực tế cần giảm false-stale.

- minor, accepted for MVP: `config_fingerprint` có default `None` để hỗ trợ
  direct test construction; snapshot tạo qua canonical
  `build_retrieval_stack()` luôn có fingerprint thật. Production/service code
  phải tiếp tục dùng factory để semantic config verification không bị skip.

## Verification

Các lệnh chính đã chạy:

```bash
codegraph status .

cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile core/schema.py core/startup.py retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py reranking/base.py reranking/models/cross_encoder.py reranking/reranker.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_bm25.py tests/test_retrieval_service.py tests/test_reranker.py tests/test_context_builder.py tests/test_startup.py -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short

cd ..
env -u HUE_RAG_QDRANT_REAL UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute notebooks/05_retrieval_profiles.ipynb --output /tmp/phase5-revision3-review-executed.ipynb --ExecutePreprocessor.timeout=120
git diff --check
git status --short
```

Kết quả:

- CodeGraph index up to date: 54 Python files, 834 nodes, 2,424 edges.
- `py_compile`: pass.
- Targeted Phase 5 tests: 99 passed in 5.28s.
- Full backend regression: 217 passed in 8.69s.
- Notebook default fake mode: execute pass; không bật real Qdrant/model mode.
- Notebook committed state: 19 cells, 9 code cells, 0 outputs, mọi
  `execution_count=null`, unique cell IDs và `nbformat.validate` pass.
- `git diff --check`: pass.
- Reviewer probes xác nhận string/`None`/object/`nan`/`inf` scores đều thành
  `RetrievalDependencyError`; duplicate input bị reject trước scorer; wrong
  embedder model thành `RetrievalConfigurationError`; weights/top-k/candidate
  multiplier changes thành `ComponentNotReadyError`.
- So sánh độc lập với các module tương ứng trong `llm_rag` không thấy file nào
  identical; implementation có cấu trúc và contract riêng, không có evidence
  copy nguyên code.

Không chạy:

- real Qdrant read-only probes;
- real E5/MiniLM model load;
- MiniLM warm-up và 20-run p95 latency gate;
- OpenAI/OpenRouter hoặc bất kỳ live/paid API nào.

## Scope Check

Các file Phase 5 mà implementer báo cáo khớp allowlist của guide. Không có
OpenRouter reranker, reindex, collection mutation, generation/API hoặc benchmark
winner claim. Benchmark ledger không bị cập nhật bằng estimated evidence.

Worktree còn có các thay đổi tồn tại trước hoặc thuộc reviewer governance:
guide Phase 0/5, guide index, các deletions dưới `knowledge-base/`, notebooks
01/02 và thư mục `skills/`. Codex không sửa, stage, revert hoặc quy các thay đổi
đó cho implementation package Phase 5.

## Safety And Quality Check

- Security: Không thấy secrets, credentials, query nguyên văn, raw provider
  payload hoặc headers bị log. CrossEncoder đã ép `local_files_only=True`, nên
  correction không còn đường tự download model.
- Data safety: Output retrieval dùng metadata allowlist và Qdrant query/scroll
  đều dùng explicit payload projection. Hybrid/service/reranker/context source
  đều không mutate inputs theo source review.
- Reliability: Không có exception-to-empty fallback; non-numeric/non-finite
  dependency scores đều typed; duplicate input bị reject; snapshot kiểm tra
  collection, count, schema, corpus và semantic config.
- Performance: Candidate depths, context và scroll batch đều bounded; BM25 fit
  ngoài request path. Reranker cache-only load một lần ở startup; explicit
  `verify_snapshot()` không chạy per-request. Real latency chưa được xác minh.
- Tests: 99 targeted và 217 full tests đều pass; purity tests dùng stub trả đúng
  captured instances và xác nhận output objects mới.
- Notebooks: Default fake mode an toàn và chạy đạt; cell IDs/schema/committed
  outputs đều sạch. Real mode vẫn opt-in và không được bật trong review này.
- Evaluation: Chưa có quality claim hoặc benchmark actual giả. Latency gate
  được ghi skipped đúng approval policy.

## Required Changes

Not applicable.

## User Confirmation Readiness

Technically accepted Phase 5 files gồm retrieval/scoring/reranking/startup
runtime, năm test modules, config additions, notebook canonical và
implementation report revision 3 trong approved allowlist.

Accepted limitations:

- Real Qdrant/E5/MiniLM probes và p95 latency gate chưa chạy vì chưa có approval
  riêng; không suy diễn pass từ fakes.
- MiniLM là local latency baseline, chưa có quality evidence cho tiếng Việt.
- `verify_snapshot()` là explicit lifecycle check, không chạy per-request.
- Conservative config fingerprint có thể tạo false-stale cho unused dense-only
  hybrid settings như minor finding.

Canonical notebook:

```text
notebooks/05_retrieval_profiles.ipynb
```

Notebook JSON/schema/default fake execution đều đạt; committed outputs rỗng,
execution counts null, unique cell IDs và không gọi external service/model.

User report:

```text
reports/user_reports/phase_5_retrieval_profiles_reranking_user_report.md
```

Người dùng cần chạy notebook từ trên xuống, kiểm tra ba profile trả đúng depth
10/10/5, score fields đúng stage, context tối đa 5 sources/3.000 ký tự và real
mode được skip. Sau đó người dùng xác nhận hoặc yêu cầu sửa.

Phase 6 vẫn đóng. `Project_Status.md` chưa được đánh dấu Phase 5 approved và
chỉ được cập nhật sau user confirmation.
