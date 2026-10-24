# Luồng hoạt động hiện tại của chatbot Huế (hue_rag)

**Cập nhật lần cuối: 24/10/2026** (sau Phase 7B). File này mô tả hệ thống **đang chạy**. Mỗi lần
hành vi đổi (chunker, index, retrieval, prompt, model), file này được cập nhật theo. Những gì đã
thử và bỏ nằm trong user report từng Phase (`phase_*.md` cùng thư mục).

Tỉ giá ước: 1 USD ≈ 25.000 đồng.

---

## 1. Toàn cảnh

```text
CHUẨN BỊ (chạy một lần khi kho đổi):
  205 file Markdown → chia đoạn (8.459 đoạn) → vector nghĩa e5-small + từ khoá BM25 → lưu Qdrant
HỎI ĐÁP (mỗi câu hỏi):
  giao diện web → API /api/chat → tìm 10 đoạn → giữ 5 đoạn làm ngữ cảnh → gpt-6-luna trả lời
  → kiểm trích dẫn [n] → trả câu trả lời + nguồn
```

| Thành phần | Dùng gì | Code |
|---|---|---|
| Kho tri thức | 205 file Markdown tiếng Việt, 5 chủ đề: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch | `knowledge-base-hue/` (private) |
| Chia đoạn | Theo cấu trúc Markdown (tiêu đề, đoạn, bảng), không chồng lấn | `backend/ingestion/chunking/full_corpus_chunker.py` |
| Vector nghĩa | `intfloat/multilingual-e5-small`, 384 chiều, chạy trên máy (CPU), miễn phí | `backend/embedding/full_corpus.py` |
| Từ khoá | BM25 tự viết, tách theo âm tiết, 5.660 từ | `backend/scoring/bm25.py` |
| Cơ sở dữ liệu vector | Qdrant `127.0.0.1:6335`, collection `hue_full_corpus_7a2_e5_small_384` | `backend/vectorstore/` |
| Tìm kiếm | `dense_bm25_rrf` (mục 3) | `backend/retrieval/full_corpus.py` |
| Trả lời | `gpt-6-luna` (OpenAI), giá 0,1 USD / 1M token vào, 0,5 USD / 1M token ra | `backend/llm/generator_openai_full_corpus.py` |
| API + giao diện | FastAPI (`/api/chat`, `/health`), trang web tĩnh | `backend/api/`, `frontend/` |
| Cấu hình | `backend/config/settings.yaml` (`full_corpus_runtime`, `full_corpus_generation`) | |

## 2. Chuẩn bị kho (khi corpus đổi)

1. Đọc 205 file Markdown, mỗi file chia theo cấu trúc: mỗi đoạn văn / mục danh sách / bảng là một
   đoạn; bảng quá dài thì mỗi dòng một đoạn kèm hàng tiêu đề. Đoạn mang theo tên file và đường tiêu đề
   (ví dụ "Bún bò Huế > Quán nổi tiếng") để tìm dễ hơn.
2. Mỗi đoạn được tạo **vector nghĩa** (e5-small) và **vector từ khoá** (BM25), lưu cùng một điểm
   trong Qdrant kèm 7 trường: chữ để tìm, nguồn, tiêu đề, đường tiêu đề, phần trích dẫn, mã đoạn, chủ đề.
3. Một **build record** ghi lại dấu (hash) của từng file corpus. Khi khởi động, API so dấu với kho
   hiện tại; kho đã sửa mà chưa build lại thì **API từ chối chạy** (để không trả lời bằng dữ liệu cũ).

## 3. Khi người dùng hỏi

1. **Tìm 30 ứng viên** bằng vector nghĩa (câu hỏi được thêm tiền tố `query:` theo hướng dẫn của e5).
2. **Chấm lại bằng BM25** trong chính 30 ứng viên đó, rồi **gộp hai bảng xếp hạng bằng RRF** (k = 60)
   → giữ 10 đoạn. Lưu ý: BM25 chỉ chấm lại đoạn mà vector nghĩa đã tìm thấy, không tìm thêm đoạn mới.
3. **Không xếp lại bằng reranker** (đã thử MiniLM tiếng Anh ở bản Foods, kém hơn).
4. **Đóng gói ngữ cảnh:** lấy **5 đoạn đầu**, nguyên vẹn, đánh số [1]…[5] (thường ~900 token).
5. **gpt-6-luna trả lời** chỉ từ 5 đoạn đó, tiếng Việt, đặt [n] sau mỗi ý. **Nếu thiếu bằng chứng**
   thì trả đúng câu: "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này."
   — kể cả khi chỉ thiếu một phần (prompt "tất cả hoặc không", `backend/llm/full_corpus_prompt.py`).
6. **Kiểm trích dẫn:** mọi [n] phải trỏ tới đoạn có thật; câu trả lời có nội dung mà không có [n], hay
   từ chối mà vẫn có [n] → API báo lỗi 500 thay vì trả câu trả lời không kiểm được.

## 4. Chất lượng đo được (Phase 7B, 176 câu hỏi Golden)

| Đo gì | Kết quả | Ý nghĩa |
|---|---|---|
| Điểm câu trả lời (Đúng / Đủ / Trúng ý, 1–5) | 4,43 / 4,28 / 4,45 | Tốt ở câu một dữ kiện (4,87), kém ở câu ghép nhiều nguồn (3,28) và so sánh (3,68) |
| Từ chối đúng câu ngoài kho | 18 / 18 | Không bịa khi kho không có |
| **Từ chối nhầm** câu kho có đáp án | **22 / 158 (13,9%)** | Lỗi lớn nhất: gần như toàn bộ điểm bị mất nằm ở đây |
| Lỗi trích dẫn (người dùng thấy lỗi 500) | 4 / 176 | Hiếm nhưng có |
| Đoạn chứa đáp án lọt top-10 (keyword proxy) | 92,4% keyword | Truy xuất khá; vấn đề nằm ở 5 đoạn được đưa vào và cách prompt từ chối |
| Chi phí một câu hỏi | ~0,00014 USD (~3,5 đồng) | ~900 token vào, ~70 token ra |

Người chấm: Claude (chấm theo đáp án mẫu), đối chiếu `gpt-6-luna` (trùng 89–96%). Chưa có người chấm tay.

## 5. Giới hạn đã biết

- Câu cần ghép nhiều nguồn / so sánh hay bị từ chối cả câu khi chỉ có một vế (22 câu Golden).
- Dòng bảng giá dài bị tách thành đoạn một dòng, khó tìm (ví dụ vé Đại Nội, lỗi F2 Phase 6).
- 20% đoạn rất ngắn (≤48 token) do chunker vẫn giữ giới hạn 256 token của model HuyDang đã bỏ.
- Chưa có index Qwen3-embedding-8B (hoãn sang Phase 8).
- Hai collection Foods cũ vẫn còn trong Qdrant, không phục vụ API nào (chờ dọn).

Hướng cải thiện các giới hạn này là việc của **Phase 8** (đợt ổn định trước Agentic RAG ở Phase 9).

## 6. Chạy thử

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000
# mở http://127.0.0.1:8000/
```

Qdrant phải chạy ở cổng 6335. Lần đầu cần tokenizer/model e5 trong HF cache.
