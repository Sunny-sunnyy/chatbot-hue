# Phase 3 Embedding and Sparse Representation Simplicity Review

Date: `2026-08-25 +07`

Status: `Approved by user`

## 1. Before state

Dense embedding trải trên `BaseEmbedder`, custom `EmbeddingError`, module-global
model cache, outer batching helper và một OpenRouter adapter không có production
consumer/live evidence. YAML giữ provider, remote và prefix config chưa được
local runtime cần. Permanent tests bảo vệ cả các cơ chế này.

Sparse TF-IDF đã deterministic nhưng tên biến/type bị ngắn và Notebook 03
phản ánh kiến trúc provider cũ.

## 2. Capability được giữ

- Local `intfloat/multilingual-e5-small`, CPU, 384 dimensions, batch size 64.
- `passage:` cho documents, `query:` cho queries và normalized vectors.
- Thứ tự vector khớp thứ tự 572 canonical chunks.
- Deterministic TF-IDF sparse indices/values cho Phase 4 compatibility.
- API startup warm-up một model instance và retrieval qua active Qdrant.
- Ba retrieval profiles và Python BM25 lexical path không đổi.

## 3. Thay đổi đã duyệt

- Thay provider framework bằng concrete `E5Embedder` sở hữu lazy model.
- Giao batching trực tiếp cho SentenceTransformer.
- Xóa `base.py`, `batch_embed.py`, `openrouter_embedder.py` và tests/config đi
  kèm.
- Giữ sparse algorithm, làm data flow và type hints dễ đọc hơn.
- Viết lại Notebook 03 thành walkthrough local E5 + public sparse API.

## 4. After state

Dense runtime còn một class 61 dòng với instance-owned model, hai public
embedding methods và validation input/count/dimension tối thiểu. YAML embedding
chỉ còn bốn key local runtime. Ingestion và startup tạo `E5Embedder` trực
tiếp; không cò alias/wrapper hoặc remote provider code.

Sparse runtime dùng ordered `dict.fromkeys` cho document frequency và `Counter`
cho term frequency. Notebook có 11 cells, chỉ gọi public Phase 2/3 APIs và
chạy trên toàn bộ corpus thật.

## 5. Before/After comparison

| Area | Before | After |
|---|---|---|
| Dense architecture | Base class + cache + batch helper + remote adapter | One concrete instance-owned `E5Embedder` |
| Runtime embedding config | Local + provider/remote/prefix keys | 4 local keys |
| Batching | Ingestion outer batches + model batches | One native model batch boundary |
| Provider tests | OpenRouter/cache/custom-prefix mechanisms | Real local E5 behaviors only |
| Sparse output | Deterministic TF-IDF | Same contract, clearer implementation |
| Notebook | Provider-oriented historical walkthrough | 572-chunk local E5/sparse walkthrough |

## 6. Downstream impact

| Phase | Dependency | Observed evidence | Impact | Later action | Blocks? |
|---:|---|---|---|---|---:|
| 4 | Dense/sparse point building | 59 affected tests; real guarded ingestion | Contract preserved | Review stored sparse vectors in Phase 4–5 | No |
| 5–7 | Query embedding and retrieval | Active `dense_only` query returned 10 results | No observed retrieval regression | No Phase 7 rerun for unchanged behavior | No |
| 8 | Future remote embedding | Phase 3 adapter/config removed | Candidate must be designed from real API | Open only after approved experiment scope | No |

## 7. Verification

- Focused E5/sparse: 10 passed, 3 warnings, 12.66s.
- Notebook 03 Run All: 572 x 384, norm 1.0, 26.13s, cosine 0.9401.
- Read-only active query: 10 results; Bún bò Huế top chunk.
- Affected downstream: 59 passed, 8 warnings, 94.94s.
- Full backend: 190 passed, 31 warnings, 204.00s.
- Active Qdrant sau tests: 572 points; no guarded leftovers.
- Scoped whitespace/deleted-import/config/notebook hygiene checks: pass.

## 8. Bugs và cách xử lý

Không phát hiện implementation bug. Qdrant ban đầu không chạy; Reviewer khởi
động Docker Compose service và exact live checks sau đó đạt. Active
collection không bị mutate.

Sentence-transformers phát `FutureWarning` cho tên method dimension cũ. Alias
hiện vẫn đúng và trả 384; đây là minor follow-up khi dependency bỏ alias,
không phải behavior failure hiện tại.

## 9. Giới hạn

- Không chạy Phase 7 evaluation do model/vector space/instructions/retrieval
  behavior được giữ và active query đã pass.
- Global diff check bị CRLF trong retrieval CSV ngoài scope; scoped Phase 3
  check pass và file ngoài scope được giữ nguyên.
- User đã xác nhận Phase 3 ngày `2026-08-25 +07`; phase hiện
  `approved`.
