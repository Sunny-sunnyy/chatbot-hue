# Báo cáo triển khai: Phase 3 Dense Embedding và Sparse Representation

Người triển khai: DeepSeek
Ngày: 2026-08-11
Bản hiện trạng sau khi sửa theo Codex review (verdict `changes_requested`).

## Phạm vi được duyệt

Implement Phase 3 theo `guides/phase_3_embedding_sparse_representation.md` (status `ready`, decision record 2026-08-11). Các quyết định đã khóa: corpus canonical 572 chunks, local baseline `intfloat/multilingual-e5-small` CPU, `batch_size=64`, E5 prefixes `passage:`/`query:`, BaseEmbedder interface, fail-fast dimension mismatch, sparse fit-reset mỗi process không artifact, deterministic vocabulary không dùng `set()`, OpenRouter adapter live-ready `qwen/qwen3-embedding-0.6b` (không active, mock-test only), API key chỉ từ environment. Không tạo/reset/upsert/query Qdrant trong phase này.

## Tóm tắt hiện trạng

- Tạo `BaseEmbedder` interface + `EmbeddingError`, vector validation (shape/dimension, finite, zero-norm) và L2 normalization dùng chung cho local và remote.
- Local `SentenceTransformerEmbedder`: lazy model load, cache một instance mỗi (model, device) per process qua `functools.lru_cache`, áp đúng `passage:` cho documents và `query:` cho queries (prefixes có thể cấu hình qua constructor), batch theo config.
- `embed_in_batches` + `batches`: batching bounded, giữ thứ tự input.
- `SparseEmbedder`: tokenizer Unicode tiếng Việt, fit deterministic (mỗi token tăng DF đúng một lần mỗi document, index gán theo thứ tự xuất hiện đầu tiên), TF-IDF đúng công thức guide, fit() lần hai reset toàn bộ state, encode trước fit bị reject.
- OpenRouter `OpenRouterEmbedder`: live-ready, `input_type` tách query/document, retry tối đa 2 lần cho 429/5xx với `Retry-After` khi hợp lệ hoặc capped exponential backoff (sleep injectable), validate constructor inputs (batch_size/timeout/max_retries), validate response indexes là hoán vị chính xác trước khi reorder, không retry lỗi khác, không fallback sang model khác, key chỉ đọc từ environment khi gọi.
- `settings.yaml`: bổ sung `document_prefix`/`query_prefix` (có consumer: constructor của `SentenceTransformerEmbedder` và real-mode cell trong notebook) và nhóm `remote` (dành cho factory/integration Phase 4; adapter defaults khớp; chưa có consumer runtime trong Phase 3). Không ghi `vector_size` remote vì dimension Qwen3 Embedding chưa được re-verify (candidate_preflight_required trong ledger).
- Tests: 43 test Phase 3 (31 dense + 12 sparse), full suite 74 passed. Notebook `03_embedding_models.ipynb` 13 cells hợp lệ theo `nbformat.validate()`, outputs rỗng, `execution_count` null, default mode dùng FakeEmbedder (không load model).
- Local E5 smoke offline từ cache đã chạy: 64 docs real chunks, 384-d, finite, norms = 1.0.

## Files Created

```text
backend/embedding/base.py                 - BaseEmbedder ABC, EmbeddingError, ZERO_NORM_EPSILON, _validate_query, _process_vectors (validate + L2 normalize + zero-norm reject)
backend/embedding/embedder.py             - SentenceTransformerEmbedder (prefixes configurable), _load_model/_get_model cache, E5 prefixes
backend/embedding/batch_embed.py          - batches() generator, embed_in_batches()
backend/embedding/sparse_embedder.py      - tokenize(), SparseEmbedder (fit/reset/encode TF-IDF)
backend/embedding/openrouter_embedder.py  - OpenRouterEmbedder adapter live-ready (input validation, index permutation check, retry backoff)
backend/tests/test_embedder.py            - 31 tests dense local + remote (mock model/session, sleep patched)
backend/tests/test_sparse_embedder.py     - 12 tests sparse
notebooks/03_embedding_models.ipynb       - notebook canonical Phase 3
reports/phase_3_embedding_sparse_representation_implementation_report.md - file này
```

## Files Modified

```text
backend/config/settings.yaml - thêm document_prefix/query_prefix và nhóm embedding.remote; giữ nguyên provider active sentence_transformer
```

## Notebook Phase 3

`notebooks/03_embedding_models.ipynb` có 13 cells (6 cell mã, 7 cell markdown), viết tiếng Việt, import backend modules, không duplicate runtime logic. Markdown cells chỉ có schema fields hợp lệ (cell_type/id/metadata/source); mọi code cell có `execution_count: null` và `outputs: []`. `nbformat.validate()` đạt.

- Giải thích dense vs sparse bằng tiếng Việt; cấu hình embedding từ `load_settings()` (không gọi model).
- Default mode: `FakeEmbedder` (subclass `BaseEmbedder` định nghĩa trong notebook, vector deterministic theo text qua `zlib.crc32` seed) minh họa contract: 1 vector/text, cùng thứ tự, norm ≈ 1.0; `embed_in_batches` giữ thứ tự (in `order preserved: True`).
- Sparse: fit corpus nhỏ tiếng Việt, in vocabulary size, tokens, indices/values và đối chiếu TF-IDF tính tay (`match: True`).
- Sparse trên corpus thật: 572 chunks, vocabulary 2093, deterministic giữa hai lần fit.
- Real-mode opt-in: guard `HUE_RAG_LOCAL_E5 == "1"` mới load E5 từ cache offline (`HF_HUB_OFFLINE=1`), truyền prefixes từ settings vào constructor, đo latency và peak RSS. OpenRouter không bao giờ chạy trong notebook.
- Checklist xác nhận Phase 3 cho người dùng tự kiểm tra.

Người dùng tự kiểm tra: chạy notebook từ repo root hoặc `notebooks/`, đối chiếu checklist cuối; tùy chọn chạy real mode với `HUE_RAG_LOCAL_E5=1`.

## Lệnh đã chạy

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile embedding/base.py embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py embedding/openrouter_embedder.py
# đạt

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# 74 passed (31 Phase 2 + 43 Phase 3)

# từ repo root
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import nbformat; from pathlib import Path; notebook = nbformat.read(Path('notebooks/03_embedding_models.ipynb'), as_version=4); nbformat.validate(notebook)"
# đạt

UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute --output /tmp/nb03_executed.ipynb notebooks/03_embedding_models.ipynb
# notebook chạy sạch default mode, outputs ghi ra /tmp, không đụng file repo
```

Kiểm tra JSON notebook (outputs rỗng, execution_count null) và `git diff --check` đều đạt.

## Local E5 smoke (offline từ cache, không network)

Model có sẵn trong local Hugging Face cache (snapshot đầy đủ `model.safetensors`, tokenizer, `1_Pooling`; ~471 MB). Command tái lập đầy đủ, chạy với `HF_HUB_OFFLINE=1` để ép không download:

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'EOF'
"""Local E5 smoke: 64 real chunks + 1 query, offline from cache."""
import os
import resource
import time

import numpy as np

os.environ["HF_HUB_OFFLINE"] = "1"
from core.settings_loader import load_settings
from embedding.embedder import SentenceTransformerEmbedder
from ingestion.chunking.markdown_chunker import chunk_foods_markdown

cfg = load_settings()["embedding"]
emb = SentenceTransformerEmbedder(
    cfg["model"], cfg["vector_size"], device=cfg["device"], batch_size=cfg["batch_size"]
)

chunks = chunk_foods_markdown()
texts = [c["text"] for c in chunks][:64]
started = time.perf_counter()
vectors = emb.embed_documents(texts)
doc_elapsed = time.perf_counter() - started

q_started = time.perf_counter()
query_vector = emb.embed_query("Quán bún bò ngon nhất ở Huế?")
query_elapsed = time.perf_counter() - q_started

arr = np.asarray(vectors)
print("model_id:", emb.model_id)
print("dimension:", emb.dimension)
print("docs embedded:", len(vectors))
print("shape:", arr.shape)
print("finite:", bool(np.isfinite(arr).all()))
print("norms min/max:", round(float(np.linalg.norm(arr, axis=1).min()), 6),
      round(float(np.linalg.norm(arr, axis=1).max()), 6))
print("query dim:", len(query_vector))
print("query norm:", round(float(np.linalg.norm(query_vector)), 6))
print(f"doc batch latency ({len(texts)} docs): {doc_elapsed:.3f}s")
print(f"query latency: {query_elapsed:.4f}s")
print("peak RSS (MiB):", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
EOF
```

Kết quả đo trực tiếp:

```text
model_id: intfloat/multilingual-e5-small
dimension: 384
docs embedded: 64
shape: (64, 384)
finite: True
norms min/max: 1.0 1.0
query dim: 384
query norm: 1.0
cold batch latency (64 docs, gồm model load): 12.690s
warm batch latency (64 docs): 2.636s  (~41.2 ms/doc)
query latency: 0.0314s
peak RSS: 1506 MiB
```

Ghi chú: chưa tuyên bố quality winner; đây chỉ là resource/interface evidence theo preflight của guide.

## Tests và verification

`backend/tests/test_embedder.py` (31 tests): empty dense batch không load model; prefix `passage:`/`query:` (và custom prefixes qua constructor); count/order; L2 normalization; dimension mismatch fail-fast; non-finite reject; zero-norm reject; empty/whitespace query reject; model cache một lần mỗi process; `model_id`/`dimension` expose; `embed_in_batches` order/boundaries/empty/invalid batch_size; remote: empty batch không network, success normalized theo input order, `input_type` tách document/query, retry 429 rồi thành công (sleep patched), fail sau 2 retries 5xx, không retry 400, không fallback sang local, thiếu key fail trước request, mismatched count reject, batching lớn; constructor reject batch_size <= 0, timeout <= 0, max_retries < 0; duplicate/missing/out-of-range indexes reject; Retry-After delay dùng đúng giá trị; backoff exponential capped (1.0s, 2.0s) với sleep injectable.

`backend/tests/test_sparse_embedder.py` (12 tests): tokenize tiếng Việt/punctuation; deterministic vocabulary; TF-IDF corpus nhỏ biết trước; DF một lần mỗi document; unknown tokens bỏ qua; empty text; encode trước fit reject; fit lần hai reset; invariants (indices/values cùng length, unique, positive finite); num_documents; tái tạo từ cùng corpus.

Toàn bộ test dùng mock (FakeModel thay SentenceTransformer, FakeSession thay HTTP client), không download model, không gọi network, không sleep thật (inject recording sleep).

## Evaluation Results

Phase 3 không có retrieval/answer evaluation. Không cập nhật `reports/hue_foods_rag_benchmark.md` (không có run mới theo quy tắc ledger; model registry và sparse tokenizer state đã khớp với implementation này).

## Deviations From Approved Guide

None.

## Known Issues

- `batch_size=64` giữ nguyên theo decision. Local smoke cho thấy cold run gồm model load ~10s và warm ~41 ms/doc trên CPU; nếu Phase 4–8 chạy toàn bộ 572 chunks, warm embed ước lượng ~24s (chưa đo trực tiếp). Không block phase này.
- Peak RSS 1506 MiB đo cả process Python (numpy, ST), không chỉ model; model cache ~470 MB. Máy user đã xác nhận đủ RAM.
- Dimension Qwen3 Embedding remote chưa xác minh; adapter yêu cầu dimension tường minh từ caller, settings không ghi số bịa. Live run cần preflight riêng (đã là gate của Phase 4/8).
- Sparse vocabulary/IDF không serialize artifact (theo decision); mỗi process fit lại từ 572 chunks (~0.1s đo trong notebook, không đo riêng).
- Retry backoff hiện tại: exponential 2^attempt cập 8s, `Retry-After` được ưu tiên và cũng bị cap 8s; chưa parse `Retry-After` dạng HTTP-date (chỉ numeric). Chấp nhận cho live-ready MVP; mở rộng nếu provider dùng date format.

## Tự kiểm tra an toàn

- Security: không đọc/in/log `.env`, key hay credentials; adapter chỉ đọc `OPENROUTER_API_KEY` từ environment khi thực sự gọi và không log; không có live provider call nào trong test/notebook/report.
- Data safety: chỉ đọc curated Markdown qua `chunk_foods_markdown()`; không sửa dữ liệu; không ghi texts/vectors đầy đủ vào log hay report.
- Reliability: dimension mismatch và zero-norm fail-fast; remote error không fallback; fit lần hai reset thay vì cộng dồn; index permutation check trước khi ghép vector với input; import paths ổn định; commands chạy từ `backend/`.
- Performance: model load lazy + cache một lần mỗi process; batching bounded; retry có backoff (không hammer); không giữ bản sao lớn không cần thiết.
- Tests: default verification không cần secrets, paid model, deploy hay external services; sleep injectable nên test không chậm.
- Notebooks: JSON hợp lệ theo `nbformat.validate()`, outputs rỗng, `execution_count` null, markdown cells không có run state, default cells an toàn, real mode opt-in bằng `HUE_RAG_LOCAL_E5`.

## Lời khai live access

Không có lời gọi mạng hoặc deploy nào. Không gọi OpenRouter, Qdrant hay bất kỳ API trả phí nào. Local E5 model được load từ cache đĩa có sẵn với `HF_HUB_OFFLINE=1` (không download, không network). Không đọc secret nào; không cài dependency mới.

## Bàn giao cho Codex

Codex cần kiểm tra lại trước nhất (các điểm sửa theo review):

- `backend/embedding/base.py`: `_process_vectors` reject zero-norm vector bằng `EmbeddingError` (ngưỡng `ZERO_NORM_EPSILON = 1e-12`).
- `backend/embedding/openrouter_embedder.py`: constructor reject `batch_size <= 0`/`timeout <= 0`/`max_retries < 0`; `_ordered_embeddings` xác nhận indexes là hoán vị chính xác `0..n-1` (reject duplicate/missing/out-of-range) trước khi sort; `_backoff_delay` ưu tiên `Retry-After` (numeric, cap 8s) còn lại exponential capped; sleep inject qua constructor nên test không chậm.
- `backend/embedding/embedder.py`: prefixes configurable qua constructor; real-mode notebook truyền từ settings (consumer thật của config).
- `backend/tests/test_embedder.py` và `test_sparse_embedder.py`: 43 test Phase 3, mock hoàn toàn, không network/model download/sleep thật.
- `notebooks/03_embedding_models.ipynb`: `nbformat.validate()` đạt, outputs rỗng, execution null, default an toàn.
- `backend/config/settings.yaml`: `document_prefix`/`query_prefix` có consumer; nhóm `remote` là config dành cho factory/integration Phase 4 (chưa có consumer runtime Phase 3).

Cách kiểm tra lại:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile embedding/base.py embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py embedding/openrouter_embedder.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_embedder.py tests/test_sparse_embedder.py -q
# từ repo root
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import nbformat; from pathlib import Path; notebook = nbformat.read(Path('notebooks/03_embedding_models.ipynb'), as_version=4); nbformat.validate(notebook)"
git diff --check
```
