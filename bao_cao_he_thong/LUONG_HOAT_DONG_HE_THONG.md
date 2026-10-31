# Luồng hoạt động hiện tại của chatbot Huế (hue_rag)

**Cập nhật lần cuối: 17:10 31/10/2026 — bản 14: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này.

File này mô tả hệ thống **đang chạy**. Mỗi lần hành vi đổi (chia đoạn, chỉ mục, cách tìm, prompt, model), file này được cập nhật theo.
Những gì đã thử và bỏ nằm trong báo cáo từng khâu (`BAO_CAO_*.md` cùng thư mục). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

**Tóm tắt hôm nay (31/10):** Phase 8 (8.1, 8.2) đã đóng 28/10; chatbot không đổi từ 30/10 — kho 204 file / 8.424 đoạn; tìm bằng vector nghĩa e5-small + từ khoá BM25;
đưa tối đa 10 đoạn vào ngữ cảnh; `gpt-6-luna` trả lời có trích dẫn. Việc kế tiếp: **hiện chữ dần (streaming)** — mới là bản thiết kế,
**chưa có code** (mục 5).

---

## 1. Toàn cảnh

```text
CHUẨN BỊ (chạy một lần khi kho đổi):
  204 file Markdown → chia đoạn (8.424 đoạn) → vector nghĩa e5-small + từ khoá BM25 → lưu Qdrant
HỎI ĐÁP (mỗi câu hỏi):
  giao diện web → API /api/chat → chuẩn hóa NFC câu hỏi → tìm 10 đoạn → đưa tối đa 10 đoạn làm ngữ cảnh → gpt-6-luna trả lời
  → kiểm trích dẫn [n] → trả câu trả lời + nguồn (trả một lần khi xong cả câu; chưa hiện chữ dần)
```

| Thành phần | Dùng gì | Code |
|---|---|---|
| Kho tri thức | 204 file Markdown tiếng Việt vào chỉ mục (đã sửa hai đợt: 28/10 và 30/10), 5 chủ đề: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch | `knowledge-base-hue/` (private) |
| Chia đoạn | Theo cấu trúc Markdown (tiêu đề, đoạn, bảng), không chồng lấn | `backend/ingestion/chunking/full_corpus_chunker.py` |
| Vector nghĩa | `intfloat/multilingual-e5-small`, 384 chiều, chạy trên máy (CPU), miễn phí | `backend/embedding/full_corpus.py` |
| Từ khoá | BM25 tự viết, tách theo âm tiết, từ điển 5.631 từ | `backend/scoring/bm25.py` |
| Cơ sở dữ liệu vector | Qdrant `127.0.0.1:6335`, chạy trong Docker Desktop (Windows); collection `hue_full_corpus_7a2_e5_small_384`, 8.424 điểm | `backend/vectorstore/`, `docker-compose.yml` |
| Tìm kiếm | `dense_bm25_rrf` (mục 3) | `backend/retrieval/full_corpus.py` |
| Trả lời | `gpt-6-luna` (OpenAI) | `backend/llm/generator_openai_full_corpus.py` |
| API + giao diện | FastAPI (`/api/chat`, `/health`), trang web tĩnh | `backend/api/`, `frontend/` |
| Cấu hình | `backend/config/settings.yaml` (`full_corpus_runtime`, `full_corpus_generation`) | |

## 2. Chuẩn bị kho (khi corpus đổi)

1. Đọc 204 file Markdown (3 file danh mục biên soạn bị loại — `settings.yaml:18-21`), mỗi file chia theo cấu trúc: mỗi đoạn văn / mục
   danh sách / bảng là một đoạn; bảng quá dài thì mỗi dòng một đoạn kèm hàng tiêu đề. Đoạn mang theo tên file và đường tiêu đề
   (ví dụ "Bún bò Huế > Quán nổi tiếng") để tìm dễ hơn.
2. Mỗi đoạn được tạo **vector nghĩa** (e5-small) và **vector từ khoá** (BM25), lưu cùng một điểm trong Qdrant kèm 7 trường: chữ để tìm,
   nguồn, tiêu đề, đường tiêu đề, phần trích dẫn, mã đoạn, chủ đề.
3. Đoạn nào vượt giới hạn token, hay quy tắc điều kiện không khớp đúng một chỗ ⇒ **dựng kho dừng**. Từ điển BM25 dùng chung chỉ được ghi
   **sau** khi kiểm chỉ mục đích hợp lệ. Quy trình dựng lại: `guides/full_corpus_rag.md` mục "Build lại index khi corpus đổi".
4. Một **phiếu build** ghi dấu (hash) của từng file corpus. Khi khởi động, API so dấu với kho hiện tại; kho đã sửa mà chưa build lại thì
   **API từ chối chạy** (để không trả lời bằng dữ liệu cũ).

## 3. Khi người dùng hỏi

0. **Chuẩn hóa câu hỏi:** câu hỏi rỗng bị từ chối; câu còn lại đổi về dạng Unicode **NFC** (kho và chỉ mục đều ở dạng NFC; câu gõ dạng
   NFD — dấu tách rời, có ở một số máy — trước đây làm tìm kiếm tụt). Câu đã ở NFC giữ nguyên từng byte
   (`backend/retrieval/full_corpus.py:97` `normalize_query`).
1. **Tìm 30 ứng viên** bằng vector nghĩa (câu hỏi được thêm tiền tố `query:` theo hướng dẫn của e5).
2. **Chấm lại bằng BM25** trong chính 30 ứng viên đó, rồi **gộp hai bảng xếp hạng bằng RRF** (k = 60) → giữ 10 đoạn đầu
   (`backend/retrieval/full_corpus.py:483-602`). Lưu ý: BM25 chỉ chấm lại đoạn mà vector nghĩa đã tìm thấy, không tìm thêm đoạn mới.
3. **Không xếp lại bằng reranker** (`settings.yaml:44` `reranker: none`) — các cách xếp lại đã thử đều chưa đáng đưa vào (mục 4).
4. **Đóng gói ngữ cảnh:** lấy tối đa **10 đoạn đầu**, nguyên vẹn, đánh số [1]…[10], trong ngân sách 16.384 token
   (`settings.yaml:53`, `:56` `max_context_documents: 10`). Trung bình ~1.655 token vào mỗi câu (176 câu Golden, đo ở bản 10 đoạn).
5. **gpt-6-luna trả lời** chỉ từ các đoạn đó, tiếng Việt, đặt [n] sau mỗi ý. **Nếu thiếu bằng chứng** thì trả đúng câu: "Tôi không tìm thấy
   đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này." (`backend/llm/full_corpus_prompt.py:4`). Câu hỏi ghép nhiều vế mà kho chỉ có
   một vế thường bị từ chối cả câu (mục 5).
6. **Kiểm trích dẫn:** model đôi khi viết `[Nguồn n]` thay vì `[n]` — hai dạng cùng nghĩa: backend đổi hết về `[n]` (để trang web gắn
   link) rồi mới kiểm (`backend/llm/citations.py`). Mọi [n] phải trỏ tới đoạn có thật; câu trả lời có nội dung mà không có [n], hay từ chối
   mà vẫn có [n] → API báo lỗi 500 thay vì trả câu trả lời không kiểm được.
7. **Ghi số đo:** mỗi lần gọi `/api/chat` — kể cả lỗi 409 / 503 / 500 — ghi đúng **một dòng** `chat_metrics` vào log `chat` (màn hình +
   `backend/logs/application.log`, không commit; `backend/api/routes/chat.py:24-83`): kết quả, mã HTTP, có từ chối không, model, token vào /
   ra / suy luận, số nguồn đưa vào / được trích, thời gian tìm / dựng ngữ cảnh / sinh / kiểm trích dẫn / tổng (ms). **Không** ghi câu hỏi,
   câu trả lời, nguồn, tiền (tiền tính sau từ token theo bảng giá). Thêm < 1 ms mỗi câu.

## 4. Chất lượng, tốc độ, tiền đo được

**Bản đang chạy (10 đoạn ngữ cảnh + NFC):**

| Đo gì | Kết quả | Nguồn |
|---|---|---|
| So với bản cũ (5 đoạn) trên 33 câu kín trong kho — câu viết mới, giữ kín tới cuối Phase 8 | điểm Đủ ý **+0,82** [+0,39; +1,33], điểm Đúng **+0,70**, **0 câu tụt**; câu ngoài kho bị trả lời **0 / 3** | `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` |
| Lượt đo mới nhất trên 176 câu Golden (30/10, sau sửa kho đợt 2) | không làm hỏng so với trước đợt 2 (trên 129 câu số chính: 4 câu tốt hơn / 3 kém hơn / 122 như cũ); từ chối nhầm 13 ⇒ 12 câu; 0 lỗi kỹ thuật, 0 lỗi trích dẫn mới; bộ an toàn 32 câu: 0 câu ngoài kho bị trả lời, 0 câu nói sai điều kiện mới | `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` |
| Thời gian chờ (176 câu, hỏi lần lượt, đo trong công cụ đo — **chưa** tính đường mạng tới trang web) | trung vị **2,19 s**, câu chậm (p95) **4,90 s** — trong trần bạn chốt 3 / 5 s; câu trả lời dài (bộ tự viết) trung vị 4,6 s ⇒ chưa đạt | như trên; `BAO_CAO_DANH_GIA.md` |
| Tiền một câu | ~0,00021 USD (~5 đồng) tính theo giá phẳng 0,10 USD / 1M token vào, 0,50 USD / 1M token ra; nhà cung cấp còn tính phần "ghi đệm" 0,125 USD / 1M nên số thật cao hơn ~20 % (≈ 0,00025 USD / câu), vẫn dưới trần 0,0005. Sửa công thức tính tiền: việc đóng gói Phase 1–8 | `session_prompt/Project_Status.md` §5 (30/10) |

Người chấm: Claude (chấm theo đáp án mẫu). **Chưa có mốc người** — bạn đọc cặp mù sau, trước buổi bảo vệ.

**Mốc cũ để so (Phase 7B, bản 5 đoạn, 176 câu Golden):** Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45 (tốt ở câu một dữ kiện 4,87, kém ở câu
ghép nhiều nguồn 3,28 và so sánh 3,68); từ chối đúng 18 / 18 câu ngoài kho; từ chối nhầm 22 / 158 câu kho có đáp án; đoạn chứa đáp án lọt
top-10 92,4 % (đo theo từ khoá); ~0,00014 USD / câu; thời gian chờ trung vị 3,3 s / p95 5,7 s (27/10). Bản 10 đoạn được chọn ở Phase 8.1
vì điểm Đủ ý tăng +0,26 [+0,08; +0,48] trên bộ thử, +0,27 [+0,02; +0,59] trên bộ kiểm, lợi chủ yếu ở câu nhiều nguồn / so sánh.

**Đã thử, không đưa vào chatbot** (chi tiết ở báo cáo khâu):

- Xếp lại kết quả (reranker): MiniLM tiếng Anh (bản món ăn) kém hơn; 2 model đa ngôn ngữ + `gpt-6-luna` (Phase 8.1) chưa qua luật; để
  `gpt-6-luna` chọn 10 / 30 đoạn (27/10) tìm tốt hơn nhưng câu trả lời kém hơn, chậm (p95 9,1 s khi 4 câu gọi cùng lúc), tốn 3,8× ⇒ bỏ (`BAO_CAO_TIM_KIEM.md`).
- Lấy 100 ứng viên thay 30; cho trả lời một phần khi kho chỉ có một vế (vi phạm sàn câu ngoài kho) ⇒ kém hơn, bỏ
  (`report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`).
- Model vector lớn Qwen3-Embedding-8B (30/10): 3 / 40 câu thử mất đoạn đúng (luật: 0 câu), bước biến câu hỏi thành vector chậm từ
  0,02 s lên ~2,2 s; tiền 0,0089 USD; chỉ mục thử đã xoá ⇒ giữ e5-small (`BAO_CAO_EMBEDDING_TU_KHOA.md`).

## 5. Giới hạn đã biết và việc kế tiếp

- Câu cần ghép nhiều nguồn / so sánh hay bị từ chối cả câu khi kho chỉ có một vế.
- Câu hỏi theo ngày tương đối ("hôm nay", "tuần này"…): không nói sai, nhưng 6 / 14 câu thử bị từ chối nhầm ⇒ để Phase 9.
- Dòng bảng giá dài bị tách thành đoạn một dòng, khó tìm (ví dụ vé Đại Nội).
- ~20 % đoạn rất ngắn (≤ 48 token; đếm trên kho cũ, chưa đo lại) vì mỗi khối Markdown là một đoạn, không gộp khối cạnh nhau (Phase 8.1 thử 12 cách chia khác, không
  cách nào thắng — `BAO_CAO_CHIA_DOAN.md`).
- Bộ chia đoạn còn giữ giới hạn 256 token của model HuyDang (không chạy ở chatbot; `settings.yaml:32-35`), làm 6 bảng bị tách theo dòng (đếm trên kho cũ, chưa đo lại).
- Trả lời một lần khi xong cả câu; chưa nhớ hội thoại nhiều lượt.

**Việc kế tiếp (thứ tự bạn chốt 30/10, giữ 31/10):**
1. **Hiện chữ dần (streaming):** bản thiết kế bản 4 đã được kiểm đạt; bạn đã chốt cách hiện chữ (chữ hiện ngay + tiến độ, kiểm trích dẫn ở
   cuối), thước tốc độ (p50 ≤ 3 s / p95 ≤ 5 s tính tới **chữ trả lời đầu tiên** hiện trên trình duyệt), và khi lỗi thì rút / xoá câu trả lời.
   Còn **1 câu bạn trả lời** (mục tiêu thời gian tới chữ đầu tiên) + bạn duyệt bản thiết kế ⇒ mới viết code.
2. Hội thoại nhiều lượt (mới có bản nháp phương án).
3. Đóng gói Phase 1–8: bảng giới hạn đầy đủ, báo cáo so sánh phương án, sửa công thức tính tiền.
4. Phase 9: mở bằng nghiên cứu rộng (đề tài, dự án, paper, ứng dụng thật cho du lịch / văn hoá) rồi mới thử nghiệm.

## 6. Chạy thử

```bash
# 1) Bật Docker Desktop (Windows) — tắt thì WSL không có lệnh docker, chatbot không tìm được
cd /home/minhhieu/hue_rag && docker compose up -d qdrant     # Qdrant ở 127.0.0.1:6335
# 2) Chạy API
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000
# mở http://127.0.0.1:8000/
```

Lần đầu cần tokenizer / model e5 trong HF cache. **Mọi lệnh chạy từ `backend/`**: API, test, dựng kho
(`cd backend && uv run --env-file ../.env python -m ingestion.full_corpus_pipeline build --candidate e5-small-384` — chỉ khi kho đổi,
theo quy trình trong guide).

**Khi có lỗi, API báo gì:**

| Tình huống | Mã | Ý nghĩa cho người vận hành |
|---|---|---|
| Kho / phiếu build / từ điển BM25 không khớp chỉ mục (lúc khởi động) | 409 `corpus_reingest_required` | Cần dựng lại chỉ mục |
| Qdrant tắt (vd Docker Desktop chưa bật), hoặc model tìm kiếm không nạp được (thiếu HF cache) | 503 `retrieval_unavailable` | Lỗi tạm, sửa môi trường — **không** dựng lại chỉ mục |
| Model sinh lỗi | 502 `generation_unavailable` | Lỗi phía OpenAI |
| Câu trả lời không qua kiểm trích dẫn | 500 `citation_integrity_error` | Hiếm (lượt 30/10: 0 lỗi mới) |

Code: `backend/api/app.py:65-85` (409 / 503 lúc khởi động), `backend/api/routes/chat.py` (502 / 500 khi hỏi).

## Phụ lục — hồ sơ kỹ thuật

- Mã nội bộ: "B1" = việc đưa 10 đoạn + NFC vào chatbot (merge `510e1a8`, 28/10); "B3" = đo trên câu kín (33 câu trong kho); "H8" = giả thuyết
  "từ chối cả câu khi chỉ có một vế" (Phase 7B); "R2" = thử trả lời một phần; "K1" = 100 ứng viên; "K3b-m" = luna chọn 10 / 30; "F2" = lỗi
  bảng giá ngoài top-30 (Phase 6).
- Phiếu build `51fb1ec63cbc` (30/10), từ điển BM25 `c8134c49a648`; ghi `chat_metrics` từ `5100b90` (27/10); kiểm trích dẫn nhận `[Nguồn n]`
  từ `9e6d371` (25/10); API báo đúng mã lỗi từ `1e4acd0` (25/10).
- Spec streaming: `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 4 `cf1ae9ef6c2c`; tổng hợp
  `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
