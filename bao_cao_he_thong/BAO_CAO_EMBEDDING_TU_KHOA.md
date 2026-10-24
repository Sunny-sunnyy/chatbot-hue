# Báo cáo dành cho người dùng: Giai đoạn 3 - Embedding (dense) và sparse/BM25

```text
Trạng thái: Đã đóng (lịch sử) — viết lại 2026-10-24
```

## 1. Bạn nhận được gì

Phase 3 biến mỗi đoạn tri thức thành hai dạng để tìm kiếm. Dạng dense (vector
gần nghĩa) giúp tìm câu cùng ý dù khác chữ. Dạng sparse (BM25) giữ tín hiệu từ khóa,
ví dụ tên món hay tên di tích. Bản đầu (25-08-2026) chỉ làm cho 572 đoạn Foods.
Bản full-corpus (12-09-2026) thử bốn model dense trên mẫu nhỏ và tạo sparse state cho
cả kho. Hôm nay hệ thống chỉ còn hai candidate dense. `e5-small-384` chạy local và đang
phục vụ API. `qwen3-embedding-8b-4096` gọi OpenRouter nhưng chưa có index.

## 2. Hệ thống hoạt động như thế nào

- Dense e5: đoạn tài liệu được thêm chữ `passage: `, câu hỏi được thêm `query: `.
  Model `intfloat/multilingual-e5-small` biến mỗi chuỗi thành vector 384 số, độ dài 1.
- Sparse BM25: hệ thống tự đọc toàn bộ chunk và tách từ đơn giản (chữ thường, cắt theo
  ký tự chữ/số). Nó lập danh sách từ (vocabulary) và độ hiếm của mỗi từ (IDF).
- Kết quả được lưu một lần vào `data/full_corpus_builds/full_corpus_sparse_state.json`.
  Lần build sau phải ra đúng từng byte như file cũ, nếu không build dừng.
- Khi hỏi: dense lấy 30 đoạn gần nhất. BM25 chấm lại 30 đoạn đó theo từ khóa.
  Hai thứ hạng được trộn bằng RRF (`dense_bm25_rrf`, k=60). Retrieval trả 10 đoạn đầu
  (`backend/retrieval/full_corpus.py:627`); bước dựng ngữ cảnh lấy 5 đoạn đầu để sinh câu trả lời.

## 3. Agent đã chạy và quan sát gì

Theo report cũ (không chạy lại hôm nay):

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Foods, 25-08-2026 | 572 x 384, norm 1.0, 26,13 giây CPU | e5-small embed được cả bộ Foods local |
| Full-corpus, 12-09-2026 | 205 file, 8.460 chunk, dense chỉ chạy trên mẫu 12 chunk | Bốn model đúng hợp đồng; chưa chọn model thắng |
| Qwen3-0.6B, 12-09-2026 | CUDA FP16 trên GTX 1650, đỉnh VRAM ~1,23 GB | Máy chạy được Qwen nhỏ trên GPU |
| Sparse, 12-09-2026 | vocabulary 5.662; sinh lặp byte-identical | Sparse state ổn định |

Đã kiểm hôm nay (2026-10-24, chỉ đọc):

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Sparse state hiện hành | `phase_3_sparse_state:v1`, 8.459 document, vocabulary 5.660, k1 1,5, b 0,75 | Fit lại trên corpus đã sửa ở 7A2 (trước 8.460 / 5.662) |
| Build record e5 | `status` complete, `dense.model_id` e5-small, `sparse.vocabulary_size` 5.660 | Record khớp sparse state |
| Qdrant GET `:6335` | 3 collection; index e5 7a2 green, 8.459 point, dense 384 + sparse | Index đang chạy đúng như record |
| Test offline | `test_full_corpus_embedding.py` + `test_full_corpus_sparse.py`: 33 passed | Hợp đồng prefix, vector, sparse vẫn đúng |

## 4. Hôm nay còn đúng không

| Kết quả/quyết định Phase 3 | Hôm nay | Bằng chứng (file:dòng) |
|---|---|---|
| e5-small 384, prefix `passage: `/`query: ` | *còn dùng* | `backend/embedding/full_corpus.py:42-53`, `:81-82`, `:95-96` |
| Bốn candidate (e5-small, e5-base, huydang, Qwen-0.6B) | *đã thay bởi* e5-small + Qwen3-8B OpenRouter (7A2) | `backend/embedding/full_corpus.py:40-66`; `docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md:30` |
| e5-base, huydang, Qwen-0.6B trong code full-corpus | *đã bỏ* (7A2). e5-base và huydang chỉ còn ở benchmark Foods. Grep `*.py` không còn Qwen-0.6B | `backend/embedding/dense_benchmark.py:50-71` |
| Qwen-0.6B CUDA FP16 trên GTX 1650 | *đã bỏ* (lịch sử); nhánh CUDA vẫn còn trong runner nhưng không spec nào dùng | `backend/embedding/full_corpus.py:203-210`, `:240` |
| Module preflight `full_corpus_embedding_preflight.py` | *đã bỏ* (7A2 Gate 2, commit `b781af8`); grep `backend/` không còn import | `reports/phase_7a2_gate_2_reindex_implementation_2026_10_24.md:56` |
| Sparse state schema `phase_3_sparse_state:v1` | *còn dùng*; runtime từ chối record khác schema | `backend/embedding/sparse.py:23`; `backend/retrieval/full_corpus.py:411-413` |
| Tokenizer sparse `\w+` chữ thường | *còn dùng*, không tách từ tiếng Việt | `backend/scoring/bm25.py:6`, `:9-12`; `backend/embedding/sparse.py:24` |
| File `phase_3_sparse_state.json`, vocabulary 5.662 | *đã thay bởi* `full_corpus_sparse_state.json`, 5.660 (7A2) | `backend/ingestion/full_corpus_pipeline.py:55`; `session_prompt/Project_Status.md:69` |
| Sparse ghi một lần, lần sau phải byte-identical | *còn dùng* | `backend/ingestion/full_corpus_pipeline.py:122-131` |
| Hằng số `vocabulary_size == 5662` | *đã bỏ* (7A2); build record là nguồn sự thật | spec 7A2 `:149-151`; grep `5662` trong `backend/*.py`: không thấy |
| "OpenRouter embedding chưa implement" (25-08) | *đã thay bởi* `OpenRouterDenseRunner`, pin Nebius, `data_collection: deny` (7A2) | `backend/embedding/full_corpus.py:295`, `:323-386` |
| Sparse TF-IDF Foods (25-08) | *đã bỏ* (Phase 4–5 simplicity) | `reports/user_reports/phase_3_embedding_sparse_representation_user_report.md:3-6` |
| `E5Embedder` Foods | *còn trong code*, chỉ đường Foods cũ dùng, API full-corpus không gọi | `backend/core/startup.py:11`; `backend/ingestion/pipeline.py:7`; `backend/api/app.py:29` |
| `dense_benchmark.py` và `evaluation/*benchmark*` Foods | *còn trong code*, chỉ test và notebook 08a/b/c gọi; trỏ collection `hue_foods_08a_*` đã xóa | `backend/evaluation/embedding_benchmark.py:39`; `backend/evaluation/sparse_benchmark.py:21`; `backend/embedding/dense_benchmark.py:45` |

## 5. Giới hạn và bước tiếp theo

- Index Qwen3-8B hoãn sang Phase 8. Build không pin trộn provider; pin Nebius gặp 504
  (`session_prompt/Project_Status.md:104`, `guides/full_corpus_rag.md:121-124`).
- BM25 tiếng Việt có tách từ hoặc bigram là giả thuyết cần đo ở Phase 8
  (`session_prompt/Project_Status.md:111`). Tokenizer hiện chỉ cắt theo `\w+`.
- Corpus đổi thì phải xóa sparse state cũ trước khi build lại
  (`session_prompt/Project_Status.md:158`).
- Không chạy lại Qwen GPU, embedding toàn corpus hay benchmark hôm nay.
- Câu "mỗi chunk vừa e5-base 512 / huydang 256" (`session_prompt/Project_Status.md:87`)
  là kết quả quét 2026-09 trên 8.460 chunk; hôm nay chưa kiểm lại trên 8.459 chunk.

## Lệch phát hiện

1. Notebook 03 còn tả bốn model và bounded preflight
   (`notebooks/03_embedding_models.ipynb:11`, `:14`, `:67`, `:141`). Code chỉ còn hai
   spec (`backend/embedding/full_corpus.py:41-66`) và module preflight đã xóa. Lệch này
   đã được ghi trong `session_prompt/Project_Status.md:166-168` ("dọn sau Phase 7").
2. `session_prompt/Project_Status.md:166` chỉ liệt kê notebook 06/08a/08b là gãy. Nhưng
   code `backend/embedding/dense_benchmark.py:45`, `:58`, `:71` vẫn trỏ collection
   `hue_foods_08a_*`. Các collection này đã xóa (`guides/full_corpus_rag.md:126-127`;
   Qdrant GET hôm nay chỉ thấy 3 collection). Tài liệu thiếu ghi phần code này.
3. Không phải mâu thuẫn tài liệu, chỉ là code còn sót: spec 7A2 yêu cầu xóa code chỉ phục
   vụ model đã bỏ (`docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md:158-161`).
   Nhánh CUDA/FP16 (`backend/embedding/full_corpus.py:203-210`) chỉ dùng cho Qwen-0.6B,
   nhưng vẫn còn.
