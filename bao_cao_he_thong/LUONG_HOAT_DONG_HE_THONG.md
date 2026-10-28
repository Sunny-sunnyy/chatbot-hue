# Luồng hoạt động hiện tại của chatbot Huế (hue_rag)

**Cập nhật lần cuối: 09:38 28/10/2026** (Phase 8.2 B1 vào chatbot, merge `510e1a8`: **ngữ cảnh tối đa 10 đoạn** thay vì 5; câu hỏi được **chuẩn hóa
Unicode NFC** trước khi tìm — câu gõ dạng NFD nay tìm giống hệt câu NFC; kết quả tìm 158 câu giống từng byte mốc cũ; chọn bằng judge Claude, **chưa có mốc
người** — bạn đọc cặp mù sau, spec 8.2 §11). Trước đó 13:27 27/10/2026 (API ghi **một dòng `chat_metrics`** cho mỗi câu hỏi: token vào / ra / suy luận, số nguồn, thời gian từng khâu — không ghi câu hỏi,
câu trả lời hay nội dung kho; merge `5100b90`; câu trả lời **không đổi**). Trước đó 16:0x 26/10/2026 (đợt 3 rà code, merge `421c302`: dựng kho dừng khi có đoạn vượt giới hạn token ở mọi nhánh; build chỉ ghi
từ điển BM25 sau khi kiểm đích; gỡ code không dùng — reranker MiniLM, Representation B, bộ kiểm khói Phase 5; câu trả lời / kết quả tìm **không
đổi**, giống từng byte). Trước đó 21:50 25/10 (gói 1b rà code, `1e4acd0`: API báo đúng loại lỗi; mọi lệnh chạy từ `backend/`). 19:59: sửa bước kiểm trích dẫn nhận cả `[Nguồn n]` (`9e6d371`, gói 1a). Trước đó 14:06 25/10 (Phase 8.1 chỉ thí nghiệm — luồng chatbot **không đổi**, kết quả tìm kiếm giống từng byte mốc cũ, Qdrant còn 1 kho; đề xuất đổi ở 8.2: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_synthesis.md`. Trước đó: 19:58 24/10 sau Phase 7B và dọn code/kho món ăn cũ). File này mô tả hệ thống **đang chạy**. Mỗi lần
hành vi đổi (chunker, index, retrieval, prompt, model), file này được cập nhật theo. Những gì đã
thử và bỏ nằm trong báo cáo từng khâu (`BAO_CAO_*.md` cùng thư mục).

Tỉ giá ước: 1 USD ≈ 25.000 đồng.

---

## 1. Toàn cảnh

```text
CHUẨN BỊ (chạy một lần khi kho đổi):
  205 file Markdown → chia đoạn (8.459 đoạn) → vector nghĩa e5-small + từ khoá BM25 → lưu Qdrant
HỎI ĐÁP (mỗi câu hỏi):
  giao diện web → API /api/chat → chuẩn hóa NFC câu hỏi → tìm 10 đoạn → giữ tối đa 10 đoạn làm ngữ cảnh → gpt-6-luna trả lời
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
3. Đoạn nào vượt giới hạn token, hay quy tắc điều kiện không khớp đúng một chỗ ⇒ **dựng kho dừng** (từ 26/10, mọi nhánh). Từ điển BM25 dùng chung
   chỉ được ghi **sau** khi kiểm chỉ mục đích hợp lệ. Quy trình dựng lại: `guides/full_corpus_rag.md` mục "Build lại index".
4. Một **build record** ghi lại dấu (hash) của từng file corpus. Khi khởi động, API so dấu với kho
   hiện tại; kho đã sửa mà chưa build lại thì **API từ chối chạy** (để không trả lời bằng dữ liệu cũ).

## 3. Khi người dùng hỏi

0. **Chuẩn hóa câu hỏi (từ 28/10):** câu hỏi rỗng bị từ chối; câu còn lại đổi về dạng Unicode **NFC** (kho và chỉ mục đều ở dạng NFC; câu gõ dạng NFD — dấu tách
   rời, có ở một số máy — trước đây làm tìm kiếm tụt, 8.1 đo MRR −0,20). Câu đã NFC giữ nguyên từng byte (`backend/retrieval/full_corpus.py` `normalize_query`).
1. **Tìm 30 ứng viên** bằng vector nghĩa (câu hỏi được thêm tiền tố `query:` theo hướng dẫn của e5).
2. **Chấm lại bằng BM25** trong chính 30 ứng viên đó, rồi **gộp hai bảng xếp hạng bằng RRF** (k = 60)
   → giữ 10 đoạn. Lưu ý: BM25 chỉ chấm lại đoạn mà vector nghĩa đã tìm thấy, không tìm thêm đoạn mới.
3. **Không xếp lại bằng reranker** (đã thử MiniLM tiếng Anh ở bản Foods, kém hơn; 8.1 thử thêm 2 model đa ngôn ngữ + `gpt-6-luna`: chưa qua
   luật). Nhánh MiniLM đã gỡ khỏi chatbot 26/10 — `reranker` chỉ còn `none`.
4. **Đóng gói ngữ cảnh (từ 28/10, Phase 8.2 B1):** lấy tối đa **10 đoạn đầu**, nguyên vẹn, đánh số [1]…[10], trong ngân sách 16.384 token
   (`backend/config/settings.yaml` `max_context_documents: 10`; trước đó 5 đoạn, thường ~900 token). Đọc vào nhiều hơn trước: câu thử 28/10 trong kho
   1.282 token vào (cả prompt + câu hỏi).
5. **gpt-6-luna trả lời** chỉ từ các đoạn đó, tiếng Việt, đặt [n] sau mỗi ý. **Nếu thiếu bằng chứng**
   thì trả đúng câu: "Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này."
   (`backend/llm/full_corpus_prompt.py`). Quan sát ở Phase 7B: bot thường từ chối cả câu khi chỉ
   có một vế (giả thuyết H8, Phase 8 thử).
6. **Kiểm trích dẫn:** model đôi khi chép nhãn ngữ cảnh và viết `[Nguồn n]` thay vì `[n]` — hai dạng cùng nghĩa: backend đổi hết về
   `[n]` (để trang web gắn link) rồi mới kiểm (từ 25/10, `backend/llm/citations.py`). Mọi [n] phải trỏ tới đoạn có thật; câu trả lời
   có nội dung mà không có [n], hay từ chối mà vẫn có [n] → API báo lỗi 500 thay vì trả câu trả lời không kiểm được.
7. **Ghi số đo (từ 27/10, `backend/api/routes/chat.py`):** mỗi lần gọi `/api/chat` — kể cả lỗi 409 / 503 / 500 — ghi đúng **một dòng** `chat_metrics`
   vào log `chat` (màn hình + `backend/logs/application.log`, không commit): kết quả, mã HTTP, có từ chối không, model, token vào / ra / suy luận,
   số nguồn đưa vào / được trích, thời gian tìm / dựng ngữ cảnh / sinh / kiểm trích dẫn / tổng (ms). **Không** ghi câu hỏi, câu trả lời, nguồn,
   tiền (tiền tính sau từ token theo bảng giá). Thêm < 1 ms mỗi câu.

## 4. Chất lượng đo được (Phase 7B, 176 câu hỏi Golden)

| Đo gì | Kết quả | Ý nghĩa |
|---|---|---|
| Điểm câu trả lời (Đúng / Đủ / Trúng ý, 1–5) | 4,43 / 4,28 / 4,45 | Tốt ở câu một dữ kiện (4,87), kém ở câu ghép nhiều nguồn (3,28) và so sánh (3,68) |
| Từ chối đúng câu ngoài kho | 18 / 18 | Không bịa khi kho không có |
| **Từ chối nhầm** câu kho có đáp án | **22 / 158 (13,9%)** | Lỗi lớn nhất: phần lớn điểm bị mất (65–90% tùy tiêu chí) nằm ở đây |
| Lỗi trích dẫn (người dùng thấy lỗi 500) | 4 / 176 ở 7B → **0–2 / 176** sau sửa 25/10 (đếm lại trên câu trả lời đã sinh) | Trước đây mọi lỗi là do dạng `[Nguồn n]`; còn lại chỉ câu thật sự không ghi nguồn |
| Đoạn chứa đáp án lọt top-10 (keyword proxy) | 92,4% keyword | Truy xuất khá; vấn đề nằm ở 5 đoạn được đưa vào (lúc đo) và cách prompt từ chối |
| Chi phí một câu hỏi (đo ở 5 đoạn) | ~0,00014 USD (~3,5 đồng) | ~950 token vào, ~80 token ra. Ở 10 đoạn đọc vào nhiều hơn ⇒ tiền mỗi câu tăng (8.1 ước ~+50 %); chưa đo lại trên bộ lớn |

Người chấm: Claude (chấm theo đáp án mẫu), đối chiếu `gpt-6-luna` (trùng 89–96%). Chưa có người chấm tay.

Bảng trên đo ở bản 5 đoạn. Bản 10 đoạn đang chạy được chọn ở Phase 8.1 (judge Claude): điểm Đủ +0,26 [+0,08; +0,48] trên bộ thử, +0,27 [+0,02; +0,59] trên
bộ kiểm, lợi chủ yếu ở câu nhiều nguồn / so sánh. **Chưa có mốc người** (bạn đọc cặp mù sau, trước buổi bảo vệ). Thời gian chờ: ở 5 đoạn trung vị 3,3 s / câu
chậm 5,7 s (27/10); ở 10 đoạn chưa đo trung vị / câu chậm (2 câu thử 28/10: 5,1 s và 2,5 s) — sẽ đo ở bộ "trước" của đợt sửa kho.

## 5. Giới hạn đã biết

- Câu cần ghép nhiều nguồn / so sánh hay bị từ chối cả câu khi chỉ có một vế (22 câu Golden).
- Dòng bảng giá dài bị tách thành đoạn một dòng, khó tìm (ví dụ vé Đại Nội, lỗi F2 Phase 6).
- ~20% đoạn rất ngắn (≤48 token) vì mỗi khối Markdown là một đoạn, không gộp khối cạnh nhau.
- Chunker còn giữ giới hạn 256 token của model HuyDang (đã bỏ), làm 6 bảng bị tách theo dòng.
- Chưa có index Qwen3-embedding-8B (hoãn sang Phase 8).

Hướng cải thiện các giới hạn này là việc của **Phase 8** (đợt ổn định trước Agentic RAG ở Phase 9).

## 6. Chạy thử

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000
# mở http://127.0.0.1:8000/
```

Qdrant phải chạy ở cổng 6335. Lần đầu cần tokenizer/model e5 trong HF cache. **Mọi lệnh chạy từ `backend/`** (từ 25/10): API, test,
dựng kho (`cd backend && uv run --env-file ../.env python -m ingestion.full_corpus_pipeline build --candidate e5-small-384`).

**Khi có lỗi, API báo gì** (từ 25/10, gói 1b — trước đó một module bị nạp hai lần nên API bắt hụt lỗi, báo sai mã):

| Tình huống | Mã | Ý nghĩa cho người vận hành |
|---|---|---|
| Kho / phiếu build / từ điển BM25 không khớp chỉ mục (lúc khởi động) | 409 `corpus_reingest_required` | Cần dựng lại chỉ mục (trước đây báo nhầm 503) |
| Qdrant tắt, hoặc model tìm kiếm không nạp được (thiếu HF cache) | 503 `retrieval_unavailable` | Lỗi tạm, sửa môi trường — **không** dựng lại chỉ mục (Qdrant lỗi khi đang hỏi trước đây ra 500) |
| Model sinh lỗi | 502 `generation_unavailable` | Lỗi phía OpenAI |
| Câu trả lời không qua kiểm trích dẫn | 500 `citation_integrity_error` | Hiếm (0–2 / 176) |
