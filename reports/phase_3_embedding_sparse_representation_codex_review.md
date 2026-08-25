# Codex Review: Phase 3 Dense Embedding và Sparse Representation

Decision: `ready_for_user_confirmation`
Reviewer: Codex
Date: `2026-08-25 +07`
Canonical guide: `guides/phase_3_embedding_sparse_representation.md`
Implementation report:
`reports/phase_3_embedding_sparse_representation_simplicity_implementation_report.md`

## 1. Phạm vi đã review

Codex đã đọc approved design/plan, source và exact diff của embedding,
config, ingestion/startup wiring, tests trực tiếp, Notebook 03 và ba guide liên
quan. Review cũ ngày 11-08 cho kiến trúc OpenRouter/mock không được dùng
làm evidence cho verdict này.

## 2. Findings

Không có `blocker` hoặc `major` finding.

- `minor`: `SentenceTransformer.get_sentence_embedding_dimension()` phát
  `FutureWarning` vì thư viện hiện tại đã đổi tên method thành
  `get_embedding_dimension()`. Runtime vẫn trả đúng 384 dimensions; warning
  này không chặn Phase 3 nhưng nên được đổi khi dependency bỏ alias cũ.

Implementation đúng simplicity scope: chỉ còn concrete `E5Embedder`, không
có wrapper/provider code thay thế, batching hai tầng hoặc OpenRouter embedding
dự phòng. `SparseEmbedder` giữ contract Phase 4 với data flow dễ theo dõi.

## 3. Cách Reviewer chạy lại thật

Reviewer dùng project `uv`, local cached
`intfloat/multilingual-e5-small`, 572 canonical foods chunks và Qdrant thật:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-review-phase3-uv-cache uv run python -m compileall -q embedding ingestion/pipeline.py core/startup.py
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-review-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py tests/test_sparse_embedder.py -q --tb=short

cd ..
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-review-phase3-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/03_embedding_models.ipynb --output /tmp/03_embedding_models-phase3-codex-review.ipynb --ExecutePreprocessor.timeout=900

cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-review-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_startup.py tests/test_hybrid_index.py -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-review-phase3-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
```

Reviewer cũng chạy read-only active collection count, guarded-leftover scan và
một query `dense_only` qua `build_service()` sau khi khởi động Qdrant service
đã định nghĩa trong repo.

## 4. Kết quả quan sát

- Compile affected modules: đạt.
- Focused Phase 3: `10 passed, 3 warnings in 12.66s`.
- Notebook 03 temporary Run All: 572 chunks, shape `572 x 384`, norm `1.0`,
  26.13 giây, query/document cosine `0.9401`; sparse mini-corpus có 3
  documents, 7 tokens và output deterministic mong đợi.
- Active query: profile `dense_only`, 10 results, top chunk
  `foods/local_specialties/bun bo hue.md|Tóm tắt|0`.
- Affected downstream: `59 passed, 8 warnings in 94.94s`.
- Full backend: `190 passed, 31 warnings in 204.00s`.
- Sau full suite: active `hue_foods_e5_small_384` vẫn 572 points;
  `guarded_leftovers=[]`.
- Repository notebook: nbformat hợp lệ, 11 cells, mọi code output rỗng và
  `execution_count=null`.
- Scoped `git diff --check`: đạt; scan không cò API/import/config embedding
  đã bị xóa.

## 5. Giới hạn hoặc phần chưa chạy

Qdrant ban đầu không chạy và trả `Connection refused`; Reviewer đã khởi
động service `qdrant` trong Docker Compose rồi chạy lại thành công. Service
hiện vẫn đang chạy.

Không chạy Phase 7 evaluation 20/104 câu vì model, dimension, E5
instructions và retrieval algorithms không đổi; real active query đã chứng minh
compatibility. Global `git diff --check` bị file ngoài scope
`backend/evaluation/retrieval_results.csv` chặn do CRLF/trailing whitespace;
scoped Phase 3 check sạch và Reviewer không sửa file ngoài scope này.

## 6. Decision và bước tiếp theo

Decision là `ready_for_user_confirmation`. Guide Phase 3 giữ
`under_review` cho tới khi user chạy
`notebooks/03_embedding_models.ipynb` và xác nhận. Báo cáo dành cho user:

```text
reports/user_reports/phase_3_embedding_sparse_representation_user_report.md
```

Simplicity review Phase 4 chưa bắt đầu. Reviewer không commit/push và
không chuyển Phase 3 sang `approved` trước user confirmation.
