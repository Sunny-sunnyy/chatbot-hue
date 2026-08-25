# Implementation Report: Phase 3 Dense embedding và sparse representation

Implementer: Antigravity
Date: 2026-08-24 +07
Canonical guide:

```text
guides/phase_3_embedding_sparse_representation.md
```

## 1. Phạm vi

Thực hiện toàn bộ phạm vi Phase 3 Embedding and Sparse Representation Simplicity theo implementation plan đã duyệt:
- Đơn giản hóa dense embedding thành một concrete class `E5Embedder` chạy trực tiếp với local `intfloat/multilingual-e5-small` trên CPU, dimension 384, batch size 64.
- Xóa bỏ hoàn toàn provider abstraction (`BaseEmbedder`, `EmbeddingError`), redundant outer batching (`batch_embed.py`) và OpenRouter adapter chưa dùng (`openrouter_embedder.py`).
- Giữ `SparseEmbedder` deterministic và refactor code rõ ràng, có type hints, loại bỏ code dư thừa nhưng bảo toàn contract với Phase 4 point builder.
- Cập nhật configuration trong `backend/config/settings.yaml` chỉ giữ 4 tham số runtime cục bộ (`model`, `vector_size`, `device`, `batch_size`).
- Cập nhật tương thích các consumer trực tiếp: `backend/ingestion/pipeline.py`, `backend/core/startup.py`, `backend/tests/conftest.py`, `backend/tests/test_startup.py`, `backend/tests/test_api_chat.py`.
- Viết lại `notebooks/03_embedding_models.ipynb` thành walkthrough trực tiếp gọi public backend API, chạy trên 572 canonical chunks, lưu sạch outputs.

## 2. Thay đổi chính

- `backend/embedding/base.py`: **Xóa** (loại bỏ `BaseEmbedder` và `EmbeddingError`).
- `backend/embedding/batch_embed.py`: **Xóa** (loại bỏ layer chia batch ngoài, SentenceTransformer tự batching).
- `backend/embedding/openrouter_embedder.py`: **Xóa** (loại bỏ OpenRouter adapter chưa có consumer thực tế ở Phase 3).
- `backend/embedding/embedder.py`: Triển khai `E5Embedder` với instance-owned lazy model, cố định E5 prefixes (`passage: `, `query: `), gọi `SentenceTransformer.encode(batch_size=64, normalize_embeddings=True)` và validation tối thiểu (`ValueError`).
- `backend/embedding/sparse_embedder.py`: Giữ nguyên giải thuật TF-IDF deterministic, refactor biến, kiểu dữ liệu và docstring dễ hiểu, dùng `Counter` và `dict.fromkeys`.
- `backend/config/settings.yaml`: Thu gọn nhóm `embedding` về đúng 4 key runtime; xóa `provider`, `remote`, `document_prefix`, `query_prefix`.
- `backend/ingestion/pipeline.py`: Sử dụng trực tiếp `E5Embedder` và `embed_documents()`.
- `backend/core/startup.py`: Khởi tạo và warm-up trực tiếp instance `E5Embedder`.
- `backend/tests/conftest.py`: Fixture `real_embedder` khởi tạo `E5Embedder`.
- `backend/tests/test_embedder.py`: 4 tests hành vi thật trên model E5 cục bộ (empty/invalid query, shape/order/norm, query vs passage role, wrong dimension fast-fail).
- `backend/tests/test_sparse_embedder.py`: 6 tests kiểm tra tokenization tiếng Việt, TF-IDF trên mini-corpus, tính deterministic, reset khi fit lại, empty/unknown text, và lỗi trước fit.
- `backend/tests/test_startup.py` & `backend/tests/test_api_chat.py`: Cập nhật kiểm tra warm-up theo lifecycle instance-owned của `E5Embedder`.
- `notebooks/03_embedding_models.ipynb`: Viết lại với 11 cell rõ ràng, chạy E5 trên 572 chunks, giải thích dense/sparse qua public API, không truy cập private state, outputs rỗng.

## 3. Cách đã chạy thật

Tất cả các lệnh được chạy từ môi trường ảo `uv` với safe env-file (`.env`) và model offline cache:

1. **Before baseline check:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py tests/test_sparse_embedder.py -q --tb=short
   ```
2. **Active collection verification (read-only):**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; settings = load_settings(); db = settings["vector_database"]; client = client_from_settings(settings); print("collection", db["collection_name"]); print("points", client.count(db["collection_name"], exact=True).count)'
   ```
3. **Focused Phase 3 tests (TDD GREEN):**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedder.py tests/test_sparse_embedder.py -q --tb=short
   ```
4. **Notebook 03 execution via nbconvert:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/03_embedding_models.ipynb --output /tmp/03_embedding_models-phase3-simplicity.ipynb --ExecutePreprocessor.timeout=900
   ```
5. **Real active collection query (read-only):**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from retrieval.service import build_service; settings = load_settings(); service = build_service(settings); documents = service.search("Bún bò Huế có đặc điểm gì?"); print("profile", service.active_profile); print("results", len(documents)); print("top_chunk", documents[0].metadata["chunk_id"] if documents else None)'
   ```
6. **Direct downstream tests:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_startup.py tests/test_hybrid_index.py -q --tb=short
   ```
7. **Full backend test suite:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
   ```
8. **Final safety and test leftovers inspection:**
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase3-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; settings = load_settings(); db = settings["vector_database"]; client = client_from_settings(settings); print("active_collection", db["collection_name"], "points", client.count(db["collection_name"], exact=True).count); print("guarded_leftovers", sorted(c.name for c in client.get_collections().collections if c.name.startswith("hue_rag_live_test_")))'
   ```

## 4. Kết quả quan sát

- **Baseline cũ:** 26 passed in 17.94s.
- **Focused Phase 3 suite:** 10 passed in 12.28s (`test_embedder.py`: 4 passed; `test_sparse_embedder.py`: 6 passed).
- **Notebook 03 execution (`/tmp/03_embedding_models-phase3-simplicity.ipynb`):**
  - Chunks: 572
  - Model: `intfloat/multilingual-e5-small`
  - Dense shape: 572 x 384
  - First vector norm: 1.0 (chuẩn L2)
  - Elapsed seconds: 31.59s
  - Sample "Bún bò Huế": query vs document cosine similarity = 0.9401
  - Sparse TF-IDF sample: 3 documents, 7 vocabulary tokens, `encoded sample: {indices: [0, 1, 2], values: [1.2876820724517808, 2.5753641449035616, 1.6931471805599454]}`
- **Active Qdrant Query:**
  - Profile: `dense_only`
  - Results count: 10
  - Top chunk: `foods/local_specialties/bun bo hue.md|Tóm tắt|0`
- **Downstream affected tests:** 59 passed in 88.58s (`test_ingestion_pipeline.py`, `test_startup.py`, `test_hybrid_index.py`).
- **Full backend suite:** 190 passed, 31 warnings in 196.71s (giảm từ 206 tests lịch sử do xóa các test không cần thiết của OpenRouter adapter, batching hai tầng và mock abstraction).
- **Active Qdrant safety:** `hue_foods_e5_small_384` giữ nguyên 572 points, `guarded_leftovers: []`.
- **Repository notebook hygiene:** `jq -e ...` trả về `true` (outputs rỗng, execution counts null).
- **Code cleanliness:** `git diff --check` sạch lỗi whitespace; không có merge conflict markers.

## 5. Lỗi và giới hạn

- Không có lỗi hoặc giới hạn đã biết trong phạm vi này.
- Các warnings xuất hiện trong test run là deprecation warnings từ `fastapi.testclient` (`httpx2`), `qdrant_client` server version check và `sentence_transformers` (`get_sentence_embedding_dimension`), không ảnh hưởng đến tính đúng đắn của runtime.
- Active collection `hue_foods_e5_small_384` không bị sửa đổi hay ghi đè trong suốt quá trình.

## 6. Handoff cho Reviewer

Reviewer nên kiểm tra:
1. `backend/embedding/` chỉ còn 2 file: `embedder.py` và `sparse_embedder.py`. Ba file `base.py`, `batch_embed.py`, `openrouter_embedder.py` đã bị xóa hoàn toàn, không có alias/wrapper.
2. `E5Embedder` trong `backend/embedding/embedder.py` sở hữu lazy model ở instance, batching giao cho SentenceTransformer.
3. `SparseEmbedder` trong `backend/embedding/sparse_embedder.py` dễ đọc, giữ nguyên TF-IDF contract.
4. `notebooks/03_embedding_models.ipynb` sạch outputs/execution counts, và có thể Run All thành công với `nbconvert`.
5. Active Qdrant collection `hue_foods_e5_small_384` còn nguyên 572 points và không có leftover test collections.
6. Chạy lại real query và test suite để xác nhận độc lập.
