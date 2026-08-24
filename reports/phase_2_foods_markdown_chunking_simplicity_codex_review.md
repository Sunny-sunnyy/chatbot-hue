# Codex Review: Phase 2 Foods Markdown Chunking Simplicity

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-24 +07
User confirmation: confirmed 2026-08-24 +07
Canonical guide: `guides/phase_2_foods_markdown_chunking.md`
Implementation report: `reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md`

## 1. Phạm vi đã review

Reviewer đã đọc canonical guide, approved design/plan, implementation report,
exact source/diff của chunker, splitter, focused tests và Notebook 02. Review
đã kiểm tra cả ba major và một minor từ correction round 1, deleted helper
imports, temporary Before baseline, downstream consumers, active Qdrant state
và worktree hygiene.

`split_text.py` không đổi. `markdown_parser.py` và `make_metadata.py` đã được
hấp thụ rồi xóa đúng design; không còn live import hoặc compatibility wrapper.

## 2. Findings

Không còn `blocker` hoặc `major` finding.

Correction round 1 đã xử lý đầy đủ findings chặn review:

- fail-fast validation xét answer-facing H2 sau image-only cleanup;
- focused regression test tái hiện đúng lỗi đã quan sát;
- permanent tests không còn khóa 572 chunks hoặc 91 files;
- deterministic test so sánh toàn bộ ordered output;
- test import/helper dư đã được xóa;
- Phase 7 retrieval CSV được hoàn nguyên về zero diff.

Hai `minor` không chặn chức năng:

- `markdown_chunker.py` còn import `Path` nhưng không dùng;
- synthetic wrapped-list fixture có typo `thay vị` thay cho `thay vì`.

Hai dòng này nên được dọn trong lần chỉnh gần nhất, nhưng không ảnh hưởng
runtime, contract, test intent, corpus output hoặc user confirmation.

## 3. Cách Reviewer chạy lại thật

Reviewer đã chạy bằng project `uv` environment, real curated corpus, local
Qdrant và local models:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-review-uv-cache uv run python -m py_compile ingestion/chunking/markdown_chunker.py ingestion/helpers/split_text.py
UV_CACHE_DIR=/tmp/hue-rag-phase2-review-uv-cache uv run python -m pytest tests/test_markdown_chunker.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-phase2-review-uv-cache uv run python -c '<ordered Before/After equality over /tmp/hue-rag-phase2-before-20260824.json>'
UV_CACHE_DIR=/tmp/hue-rag-phase2-review-uv-cache uv run jupyter nbconvert --execute --to notebook notebooks/02_foods_data_and_chunking.ipynb --output /tmp/02_foods_data_and_chunking-phase2-codex-review.ipynb --ExecutePreprocessor.timeout=600
UV_CACHE_DIR=/tmp/hue-rag-phase2-review-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_hybrid_index.py tests/test_startup.py tests/test_api_chat.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-phase2-review-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
```

Reviewer đếm active collection read-only trước và sau verification, đồng thời
chạy notebook cleanliness/sensitive scan, deleted-import scan,
`git diff --check`, conflict-marker scan và zero-diff checks cho Phase 7 CSV.

## 4. Kết quả quan sát

- Affected modules compile thành công.
- Focused suite trước full run: `15 passed, 1 warning in 0.14s`.
- Focused suite sau full run: `15 passed, 1 warning in 0.24s`.
- Ordered equality trước và sau full run: `True`; 572 chunks từ 91 files;
  SHA-256 hai phía là
  `936063a91a69083fe7070096da17656920cff3b93917a3e6fcc4384d697c8fde`.
- Notebook temporary Run All thành công: 572 chunks, 91 files, schema bảy
  fields và ba ví dụ paragraph/table/food guide đúng contract.
- Repository notebook có outputs rỗng, execution counts null và sensitive scan
  sạch.
- Downstream smoke: `79 passed, 3 warnings in 231.46s`.
- Full backend suite: `206 passed, 4 warnings in 244.37s`.
- Active collection trước và sau: `hue_foods_e5_small_384`, 572 points.
- Full suite tái tạo CRLF-only diff đã biết ở `retrieval_results.csv`; Reviewer
  xác nhận nội dung không đổi, hoàn nguyên line endings do reviewer run và kết
  thúc với zero diff.
- Final full-worktree `git diff --check` và scoped merge-marker scan sạch.

Hai test suites rộng là fresh observed evidence theo approved Phase 2 plan,
không phải test-count target hoặc bằng chứng rằng mọi test đều cần thiết.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy Phase 7 evaluation 20/104 câu vì ordered chunks khớp tuyệt đối;
  chunking, retrieval input và RAG quality behavior không đổi.
- Notebook chạy bằng local Jupyter kernel và corpus thật; không gọi Qdrant,
  model API, web hoặc paid provider.
- Các warning là Starlette/httpx deprecation và Qdrant compatibility check đã
  biết; không quan sát ảnh hưởng Phase 2.

## 6. Decision và bước tiếp theo

Technical decision: `ready_for_user_confirmation` sau correction round 1; user
đã xác nhận ngày `2026-08-24 +07`.

Canonical guide đã chuyển sang `approved`. User report nằm tại
`reports/user_reports/phase_2_foods_markdown_chunking_simplicity_user_report.md`.
User đã Run All Notebook 02 và xác nhận. `guides/README.md`, simplicity review
và `Project_Status.md` đã được đồng bộ. Bước tiếp theo là brainstorm simplicity
review Phase 3. Reviewer không sửa runtime code, không commit và không push.
