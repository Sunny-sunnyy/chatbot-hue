# Codex Review: Phase 1 Backend Skeleton Simplicity

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-24 +07
User confirmation: confirmed 2026-08-24 +07
Canonical guide: `guides/phase_1_backend_skeleton.md`
Implementation report: `reports/phase_1_backend_skeleton_simplicity_implementation_report.md`

## 1. Phạm vi đã review

Đã đọc guide, approved design/plan, implementation report, living simplicity
review, exact source/diff của bốn runtime files và nội dung hai artifact bị
xóa. Đã trace settings loader, logging setup, FastAPI lifespan, ingestion CLI,
evaluation UI và các affected tests. Phase 1 không có notebook theo approved
design.

## 2. Findings

Không có `blocker` hoặc `major` finding. Implementation đúng exact scope, trực
tiếp và không thêm abstraction, wrapper, validator hoặc compatibility layer.

- `minor`: affected test
  `test_retrieval_handler_returns_named_columns_and_rows` gọi UI handler thật,
  từ đó ghi lại canonical `retrieval_results.csv` bằng CRLF. Nội dung 20 rows
  không đổi, nhưng tạo diff line-ending sau test. Reviewer đã hoàn nguyên đúng
  side effect của reviewer run và xác nhận hai CSV kết thúc với zero diff. Đây
  là follow-up thuộc Phase 7 test/evaluation ownership, không phải correction
  scope cho Implementer Phase 1.

## 3. Cách Reviewer chạy lại thật

Từ `backend/`, Reviewer đã chạy:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run python -m py_compile core/settings_loader.py core/logging_setup.py api/app.py ingestion/pipeline.py evaluation/evaluator.py
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run python -c 'from core.settings_loader import load_settings; s=load_settings(); print(s["active_profile"]); print([(n,p["retrieval_mode"],p["use_bm25"],p["use_reranker"]) for n,p in s["profiles"].items()])'
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run python -c 'import api.app; print("import ok")'
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run python -c 'import logging; from core.logging_setup import LOGS_DIR, LOG_FILE_NAME, setup_logging; setup_logging(); logging.getLogger("retrieval").info("phase1 independent reviewer logging check"); path=LOGS_DIR/LOG_FILE_NAME; print(path); print(path.exists()); print(path.stat().st_size)'
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8011
curl --fail --silent --show-error --max-time 5 http://127.0.0.1:8011/health
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run --env-file ../.env python -m evaluation.evaluator
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run --env-file ../.env python -m pytest tests/test_startup.py tests/test_api_chat.py tests/test_ingestion_pipeline.py tests/test_evaluation.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-phase1-review-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
```

Reviewer kiểm tra read-only active collection trước và sau tests bằng Qdrant
client thật, đồng thời chạy `git diff --check`, conflict-marker scan và exact
CSV/source diff. Không chạy 104-question Phase 7 evaluation.

## 4. Kết quả quan sát

- Affected modules compile thành công; canonical settings trả `dense_only` và
  đúng ba profiles cùng flags.
- Import `api.app` không thay đổi size hoặc mtime của existing application log.
- Logging smoke ghi console và tăng log file từ 8210 lên 8293 bytes tại đúng
  `backend/logs/application.log`.
- API load local `intfloat/multilingual-e5-small`; `/health` trả
  `status=ok`, Qdrant/retrieval `ready`, generator `configured`.
- Gradio phục vụ tại `http://127.0.0.1:7860`; startup endpoints trả HTTP 200 và
  process dừng sạch.
- Affected suite: `74 passed, 3 warnings in 295.31s`.
- Full backend suite: `222 passed, 4 warnings in 252.51s`.
- Active collection trước và sau tests:
  `hue_foods_e5_small_384`, `572` points.
- Hai Phase 7 CSV kết thúc với zero diff; repository hygiene và merge-marker
  scan sạch sau khi Reviewer hoàn nguyên line endings do test tạo ra.

Hai suite đã chạy là observed history theo verification scope cũ. Chúng rộng
hơn blast radius Phase 1, không phải acceptance requirement và không chứng
minh mọi test đều cần thiết. Bằng chứng quyết định của Phase 1 là settings,
logging, Uvicorn, Gradio và Qdrant live paths ở trên.

## 5. Giới hạn hoặc phần chưa chạy

- Gradio không mở được browser GUI tự động trong môi trường headless
  (`gio: Operation not supported`), nhưng local server hoạt động bình thường.
- Không chạy paid 104-question evaluation vì guide xác định scope này không
  chạm RAG quality.
- Reviewer không mutate canonical YAML để kích hoạt nhánh invalid-profile;
  nhánh này được đọc trực tiếp và giữ nguyên hành vi `ValueError` của code cũ.

## 6. Decision và bước tiếp theo

Technical decision là `ready_for_user_confirmation` và user đã xác nhận ngày
`2026-08-24 +07`. Phase 1 không cần notebook theo approved design. User report nằm tại
`reports/user_reports/phase_1_backend_skeleton_simplicity_user_report.md`.

Guide đã chuyển sang `approved`. Bước tiếp theo là brainstorm Phase 2; test sẽ
được audit theo ownership và blast radius thay vì chạy full suite mặc định.
Reviewer không sửa runtime code và không commit/push.
