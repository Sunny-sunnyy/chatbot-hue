# Codex Review: Phase 3 Dense Embedding và Sparse Representation

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-11
Review path:

```text
reports/phase_3_embedding_sparse_representation_codex_review.md
```

Implementer report:

```text
reports/phase_3_embedding_sparse_representation_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_3_embedding_sparse_representation.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
```

## Tóm Tắt

Phase 3 đã technical accepted sau corrective review. Implementation cung cấp E5
local dense embedder với prefix tách query/document, batching, normalized vector
và dimension fail-fast; TF-IDF sparse representation deterministic; và OpenRouter
embedding boundary live-ready nhưng mock-tested mặc định.

Corrections đã xử lý notebook schema, zero-norm vectors, remote constructor and
response guards, và rate-limit backoff. Chưa có live OpenRouter, Qdrant hoặc
benchmark run nào. Phase chờ người dùng chạy notebook trước final approval.

## Findings

Không có blocker hoặc major findings.

- minor: Retry-After dạng HTTP-date chưa được parse; adapter ưu tiên giá trị số
  và fallback về exponential backoff capped. Đây là giới hạn chấp nhận được cho
  live-ready MVP và cần xem lại trước remote production-scale run.

## Verification

Đã chạy độc lập:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile embedding/base.py embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py embedding/openrouter_embedder.py
# đạt

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# 74 passed in 3.33s

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from embedding.embedder import SentenceTransformerEmbedder; embedder = SentenceTransformerEmbedder('intfloat/multilingual-e5-small', 384); vector = embedder.embed_query('Bún bò Huế có đặc điểm gì?'); assert len(vector) == 384; assert abs(sum(value * value for value in vector) - 1.0) < 1e-6; print(embedder.model_id, embedder.dimension, len(vector))"
# intfloat/multilingual-e5-small 384 384

cd ..
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import nbformat; from pathlib import Path; notebook = nbformat.read(Path('notebooks/03_embedding_models.ipynb'), as_version=4); nbformat.validate(notebook); assert all(cell.get('execution_count') is None and cell.get('outputs') == [] for cell in notebook.cells if cell.cell_type == 'code')"
# đạt

git diff --check
# đạt
```

Reviewer sandbox không cho Jupyter kernel mở local socket, nên không thể chạy
default notebook độc lập tại đây. Implementer evidence ghi default notebook đã
chạy sạch; reviewer đã xác minh schema hợp lệ, outputs trống, execution counts
null và không có external call ở default mode. User notebook gate vẫn là điều
kiện bắt buộc trước final approval.

## Scope Check

Implementer chỉ tạo/sửa approved Phase 3 package: năm module embedding, một
config file, hai test files, notebook Phase 3 và implementation report. Guide
index, Phase 3 guide, review report và user report là reviewer scope. Các
deletion trong `knowledge-base/`, notebook Phase 1–2, `rag_old/` và `skills/`
là thay đổi có sẵn, không thuộc review package.

## Safety And Quality Check

- Security: tests dùng fake model/session; adapter chỉ đọc environment khi
  request thực sự chạy và không log key. Không có live provider call.
- Data safety: chỉ đọc curated chunks; không mutate Markdown, Qdrant hoặc data
  source.
- Reliability: zero norm, dimension mismatch, malformed remote indexes, invalid
  batch/timeout/retry values và provider retry đều fail-safe hoặc có test.
- Performance: local model lazy-cache một instance/process; batches bounded;
  429/5xx retry dùng delay capped, không hammer provider.
- Tests: 74 tests pass, gồm 43 tests Phase 3 với fake SentenceTransformer,
  HTTP session và sleep injection.
- Notebooks: JSON/schema hợp lệ, outputs rỗng, execution count null; default
  mode không gọi model/API/network, local E5 là opt-in.
- Evaluation: không có retrieval/answer result hoặc claim model winner.

## Required Changes

Not applicable.

## User Confirmation Readiness

- Technically accepted files: `backend/embedding/`,
  `backend/config/settings.yaml`, Phase 3 tests, notebook và implementation
  report trong approved scope.
- Accepted limitations: OpenRouter chưa có live run/dimension evidence; sparse
  state refit mỗi process; retry HTTP-date là minor limitation.
- Canonical notebook: `notebooks/03_embedding_models.ipynb`; committed file
  schema-valid, outputs rỗng và default mode safe.
- User checks: chạy notebook từ trên xuống, xác nhận 572 chunks, vocabulary
  sparse 2093, deterministic result, preserved order và TF-IDF sample match;
  sau đó tùy chọn local E5 mode nếu muốn resource evidence.
- User report: `reports/user_reports/phase_3_embedding_sparse_representation_user_report.md`.
- Phase 4 vẫn đóng. `Project_Status.md` chưa được đánh dấu approved.
