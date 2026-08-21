# Codex Review: Phase 6.1 Baseline Lifecycle Hardening

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-21
Review path:

```text
reports/phase_6_1_baseline_lifecycle_hardening_codex_review.md
```

Implementer report:

```text
reports/phase_6_1_baseline_lifecycle_hardening_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_6_generation_api.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
```

## Tóm Tắt

Correction re-review đạt. Hai major findings của vòng đầu đã được giải quyết:
canonical notebook qua `nbformat.validate`, không còn execution/widget
artifacts, và cache evidence được chụp ngay sau lifespan rồi so sánh sau
`/health` và first `/api/chat`.

Runtime implementation vẫn đúng lifecycle đã duyệt. Reviewer đã chạy 8
targeted lifecycle tests cùng 36 affected tests trên Qdrant/model thật ở vòng
đầu; correction không sửa runtime. Execution copy mới trong `/tmp` có source
cells trùng khớp canonical, không có cell error và cho thấy E5 misses giữ
nguyên `1 -> 1` qua first retrieval; MiniLM giữ `0 -> 0` với `dense_only`.
Technical decision là `ready_for_user_confirmation`.

## Findings

Không có blocker hoặc major findings.

- resolved major: xóa `outputs`/`execution_count` khỏi năm markdown cells,
  xóa `metadata.execution` khỏi code cells và xóa 11 widget-state artifacts.
  Canonical notebook hiện qua nbformat validation; code-cell outputs rỗng và
  execution counts null.
- resolved major: notebook chụp cache tại Evidence A ngay sau lifespan trước
  mọi request, Evidence A2 sau `/health` và Evidence B sau first `/api/chat`;
  hard asserts yêu cầu E5/MiniLM misses của B bằng A.
- minor: checklist cuối notebook nói có hai lần gọi `/health` và đo latency,
  nhưng code hiện gọi một lần và không in health latency. Cached-health
  behavior vẫn được chứng minh bằng cache A2 và equality assert cuối; sai lệch
  diễn đạt này không ảnh hưởng lifecycle correctness hoặc user confirmation.
- minor: executed copy ngoài repo còn các field markdown không hợp lệ từ thứ
  tự execute-then-clean. Source cells của copy khớp byte-for-byte với canonical,
  không có error output và canonical committed file đã sạch/hợp lệ. Khi chạy
  lại, nên execute từ canonical sạch ra một output copy mới.

## Verification

Các validation Reviewer chạy độc lập trong review và correction re-review:

```bash
codegraph status .
# Index is up to date.

codegraph affected backend/core/startup.py
codegraph affected backend/reranking/models/cross_encoder.py
# Affected tests: test_api_chat.py, test_ingestion_pipeline.py,
# test_reranker.py, test_retrieval_service.py, test_startup.py.

cd backend
UV_CACHE_DIR=/tmp/hue-rag-review-uv-cache uv run python -m py_compile \
  core/startup.py reranking/models/cross_encoder.py
# Pass.

UV_CACHE_DIR=/tmp/hue-rag-review-uv-cache uv run python -m pytest \
  tests/test_startup.py tests/test_api_chat.py -q --tb=short -s \
  -k "warm_up or no_model_load or never_load or fails_closed or dead_qdrant or LifecycleWarmup"
# 8 passed, 41 deselected, 2 known warnings in 107.51s.

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-review-uv-cache \
  uv run python -m pytest tests/test_reranker.py \
  tests/test_retrieval_service.py tests/test_ingestion_pipeline.py \
  -q --tb=short -s
# 36 passed, 1 known warning in 102.89s; cleanup operations ok.

UV_CACHE_DIR=/tmp/hue-rag-review-uv-cache uv run python -c \
  "import nbformat; nb=nbformat.read('notebooks/06_generation_and_api.ipynb', as_version=4); nbformat.validate(nb)"
# Pass.

# Structural audit: 9 cells; no invalid markdown fields; no dirty code cells;
# no metadata.execution; no notebook widget state; 12,583 bytes.
# Code cells parse; exactly one /api/chat call site.

# Compare source arrays between canonical and executed /tmp copy.
# Match. Executed copy: no error outputs.
# Evidence: startup E5 misses=1, MiniLM=0; after health 1/0; after first chat
# E5 misses=1, MiniLM=0; chat 200; PASS assertion printed.

UV_CACHE_DIR=/tmp/hue-rag-review-uv-cache uv run python -c \
  'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s=load_settings(); c=client_from_settings(s); n=s["vector_database"]["collection_name"]; print("active_collection", n, "points", c.count(n, exact=True).count)'
# active_collection hue_foods_e5_small_384 points 572

git diff --check
# Clean.
```

Reviewer không chạy lại full 214-test suite hoặc OpenAI paid call trong
correction re-review vì runtime không đổi và `OPENAI_API_KEY` không có trong
Reviewer process environment. Implementer re-run evidence: `214 passed in
241.36s`, năm OpenAI success calls, một dead-provider attempt, không retry,
chi phí ước tính `$0.0039370`, mọi isolated cleanup `ok`.

## Scope Check

Correction chỉ sửa `notebooks/06_generation_and_api.ipynb` và implementation
report; runtime/test diff không thay đổi sau vòng review đầu. Toàn milestone
nằm trong allowlist. Reviewer chỉ sửa guide/index, review report và tạo user
report theo workflow.

Các deletions cũ dưới `knowledge-base/` và thư mục untracked `skills/` nằm ngoài
scope; Reviewer không sửa, reset, stage hoặc include chúng.

## Safety And Quality Check

- Security: không thấy credential, raw provider payload, prompt hoặc full
  retrieved context trong canonical notebook hay changed runtime. Reviewer
  không đọc `.env`; user đã cho phép DeepSeek source key cho live validation.
- Data safety: active collection chỉ được đọc và Reviewer xác nhận còn 572
  points. Isolated collection cleanup được report `ok`.
- Reliability: warm-up fail closed, không retry/fallback/partial publish;
  targeted và affected live tests đạt.
- Performance: one-time startup work bounded theo profile; evidence mới ghi
  startup khoảng 12,4–14,8 giây và first retrieval 17–18 ms, không áp threshold
  ngoài guide.
- Tests: Reviewer độc lập có 44 tests đạt; Implementer correction full suite có
  214 tests đạt.
- Notebooks: canonical JSON hợp lệ và sạch; full-path execution evidence có một
  OpenAI call, chat 200 và cache misses không tăng sau first retrieval.
- Evaluation: không thuộc Milestone 6.1; chưa có quality benchmark hoặc winner
  selection mới.

## Required Changes

Not applicable.

## User Confirmation Readiness

- Technically accepted: runtime lifecycle, tests, notebook 06 và implementation
  report trong allowlist Milestone 6.1.
- Accepted limitation: cold startup khoảng 12–15 giây trên máy validation;
  không có hard latency threshold. Checklist health-latency có một sai lệch
  diễn đạt minor như Findings.
- Canonical notebook: `notebooks/06_generation_and_api.ipynb`; JSON hợp lệ,
  outputs rỗng, execution counts null, không có widget/execution artifacts.
- User report:
  `reports/user_reports/phase_6_1_baseline_lifecycle_hardening_user_report.md`.
- User cần export `OPENAI_API_KEY`, Run All notebook 06, kiểm tra health/chat,
  Evidence A/B và dòng PASS cache misses; mỗi Run All gọi đúng một OpenAI call.
- Phase 7 vẫn đóng. `Project_Status.md` chưa được cập nhật cho milestone này.
