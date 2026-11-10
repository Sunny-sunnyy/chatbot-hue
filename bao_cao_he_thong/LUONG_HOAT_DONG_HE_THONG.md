# Luồng hoạt động hiện tại của chatbot Huế (hue_rag)

**Cập nhật lần cuối: 20:52 10/11/2026 — bản 35:** câu có ngày: code tính sẵn ngày trước lần gọi model đầu (merge `1633c18`), công cụ `ngay_lich` chỉ còn dự phòng. Bản 34 (19:30 10/11/2026): hệ thống không đổi; sửa các chỗ cũ theo rà soát 10/11 (tốc độ / tiền theo lượt đo chung 09/11, 4 chốt trước deploy đã có code, log xoay vòng, hỏi bằng ảnh trong sơ đồ + API, mã 429, việc kế tiếp, phiếu build mới). Các bản trước: xem lịch sử git.

File này mô tả hệ thống **đang chạy**. Mỗi lần hành vi đổi (chia đoạn, chỉ mục, cách tìm, prompt, model), file này được cập nhật theo.
Những gì đã thử và bỏ nằm trong báo cáo từng khâu (`BAO_CAO_*.md` cùng thư mục). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

**Tóm tắt (hiện trạng 10/11):**
- **Kho và tìm:** kho 204 file / 8.435 đoạn; tìm bằng vector nghĩa e5-small + từ khoá BM25; đưa tối đa 10 đoạn vào ngữ cảnh; `gpt-6-luna` trả lời có trích dẫn, chữ hiện dần.
- **Người dùng thấy (từ 07/11, cổng đợt 1):** một cổng du lịch thay cho trang hỏi đáp đơn:
  - **trang chủ** có ô hỏi lớn, 5 câu gợi ý, 5 lĩnh vực, ô thời tiết hôm nay;
  - **Khám phá** đọc thẳng 204 bài của kho (danh sách theo lĩnh vực, trang bài, nút "Hỏi trợ lý về điểm này");
  - **Trợ lý Huế** nổi ở góc mọi trang (điện thoại: phủ màn) và có trang riêng — **một cuộc trò chuyện** giữ nguyên khi chuyển trang;
  - **Lên kế hoạch** (bật 07/11): chọn số ngày, người đi cùng, sở thích ⇒ lịch theo buổi từ các điểm trong kho, có nguồn + link bản đồ từng điểm; điểm không xếp được ghi lý do; muốn đổi thì "Sửa — điền lại biểu mẫu";
  - trang **Giới thiệu** (làm được gì, giới hạn, dữ liệu người dùng);
  - **thanh dưới** trên điện thoại.
- **Nguồn:** câu trả lời **không còn số [n] chen trong chữ**; dưới câu có dòng **"Nguồn: <tên> · <tên>"**, bấm tên ⇒ đoạn gốc + "Đọc cả bài". Tầng máy vẫn giữ và kiểm [n] như cũ.
- **Trợ lý (Phase 9):**
  - phân loại câu hỏi (trò chuyện / về Huế / ngoài phạm vi / khẩn cấp — **từ 09/11 câu khẩn cấp đi trợ lý Huế như câu về Huế**, không còn câu soạn sẵn 113 / 114 / 115 / 112);
  - tự tìm thêm trong kho ≤ 2 lần;
  - nhớ câu hỏi 3 lượt;
  - kho không có ⇒ mục "Từ web (chưa kiểm)";
  - **từ 07/11 trả lời câu dự báo thời tiết** bằng số Open-Meteo do code dựng;
  - **từ 09/11 trả lời câu có ngày** ("tối nay", "rằm tháng Giêng tới", "Tết năm nay", lễ ngày âm "năm sau"): code tính ngày + đổi âm ↔ dương lịch Việt Nam. **Từ 10/11 code tính sẵn**
    hôm nay / mai / các ngày trong tuần được hỏi / ngày âm trong câu và trong đoạn kho vừa tìm, đưa model ngay lần đầu ⇒ nhanh hơn (bước 17).
- **Từ 08/11 (giao diện):** nút Dừng khi đang trả lời (máy chủ huỷ lần gọi model), ô hỏi ≤ 500 ký tự, gợi ý cách hỏi dưới câu kho từ chối, dòng "Nguồn" gộp theo bài, nút sao chép / tải lịch trình.
- **Bật từ 08/11:** hỏi bằng ảnh (gợi ý ≤ 3 tên, người dùng bấm xác nhận; ảnh thu nhỏ gửi OpenAI để đoán tên, máy chủ không lưu ảnh, log không ghi nội dung). **Chưa bật:** lịch trình khi gõ câu tự do (chỉ qua biểu mẫu), bản đồ lịch trình (code có, chờ bạn xem), giọng nói.
- **Tốc độ + tiền (lượt đo chung 09/11: 65 câu, trình duyệt thật, một lượt — mục 4):** câu về Huế tới chữ đầu trung vị 2,16 s / p95 4,32 s, 0,00047 USD / câu ⇒ **đạt** sàn 3 / 5 s và trần 0,0005; câu ngoài phạm vi 1,62 / 2,97 s; **câu xã giao p95 7,73 s ⇒ vượt sàn**; **câu có từ chỉ ngày: từ 10/11 trung vị 2,35 s / p95 4,56 s, 0,00036 USD / câu (19 câu, 1 lượt, đo ở máy chủ; trước 5,60 / 10,14 s, 0,00049 USD) ⇒ đạt** (lượt chung 09/11 còn vượt: 5,19 s, 0,00063 USD).
- Phase 8 bạn đóng 14:29 01/11/2026; Phase 9 đang làm (còn B7 đóng gói, mục 5).

---

## 1. Toàn cảnh

```text
CHUẨN BỊ (chạy một lần khi kho đổi):
  204 file Markdown → chia đoạn (8.435 đoạn) → vector nghĩa e5-small + từ khoá BM25 → lưu Qdrant
HỎI ĐÁP (mỗi câu hỏi):
  cổng web (Trợ lý Huế nổi / trang riêng) → API /api/chat/stream (hoặc /api/chat) → chuẩn hóa NFC → gpt-6-luna phân loại câu hỏi
    ├ trò chuyện → gpt-6-luna đáp ngắn, không tìm kho        ├ ngoài phạm vi → câu soạn sẵn   (khẩn cấp → như "hỏi về Huế", từ 09/11)
    └ hỏi về Huế → tìm 10 đoạn bằng câu gốc → ngữ cảnh → gpt-6-luna trả lời (chữ hiện dần), được gọi công cụ:
         tim_kho thêm ≤ 2 lần · thoi_tiet (từ 07/11; số Open-Meteo do code dựng) · ngay_lich (từ 09/11; từ 10/11 chỉ dự phòng)
         (câu có từ chỉ ngày: từ 10/11 code thêm sẵn nguồn "Lịch hệ thống" vào ngữ cảnh TRƯỚC lần gọi model đầu)
       → kiểm trích dẫn [n] → dòng "Nguồn: …" (giao diện bỏ số [n] khỏi chữ)
       → kho từ chối ⇒ tra web một lần ⇒ mục "Từ web (chưa kiểm)"
  biểu mẫu "Lên kế hoạch" (từ 07/11) → /api/chat/stream {bieu_mau, giá trị nút} → KHÔNG định tuyến → code xếp lịch (biểu mẫu chưa có ô ngày đi ⇒ lịch không kèm dòng dự báo — S3 đếm 0 / 24)
       → gpt-6-luna viết lời theo khung, một lần, không công cụ, mức suy luận "low" → code kiểm cuối + nối ghi chú / link bản đồ
  hỏi bằng ảnh (từ 08/11) → POST /api/anh/ung_vien (kiểm cỡ / kiểu, thu nhỏ cạnh dài 1024) → gpt-6-luna gợi ≤ 3 tên trong danh sách 42 mục
       → người dùng bấm đúng tên ⇒ thành câu hỏi thường ở trên (không bấm ⇒ không trả lời; máy chủ không lưu ảnh)
  nút "Cuộc trò chuyện mới" → POST /api/conversation/new (xoá nhớ)   ·   👍 / 👎 → POST /api/feedback
TRANG KHÁC (không gọi model):
  Khám phá → GET /api/kham_pha (204 bài) · /api/kham_pha/bai?id= (một bài)   ·   ô thời tiết → GET /api/thoi_tiet   ·   cờ → GET /api/tinh_nang
```

| Thành phần | Dùng gì | Code |
|---|---|---|
| Kho tri thức | 204 file Markdown tiếng Việt vào chỉ mục (đã sửa hai đợt: 28/10 và 30/10), 5 chủ đề: món ăn, di tích, lễ hội, nghệ thuật biểu diễn, du lịch | `knowledge-base-hue/` (private) |
| Chia đoạn | Theo cấu trúc Markdown (tiêu đề, đoạn, bảng), không chồng lấn | `backend/ingestion/chunking/full_corpus_chunker.py` |
| Vector nghĩa | `intfloat/multilingual-e5-small`, 384 chiều, chạy trên máy (CPU), miễn phí | `backend/embedding/full_corpus.py` |
| Từ khoá | BM25 tự viết, tách theo âm tiết, từ điển 5.631 từ | `backend/scoring/bm25.py` |
| Cơ sở dữ liệu vector | Qdrant `127.0.0.1:6335`, chạy trong Docker Desktop (Windows); collection `hue_full_corpus_7a2_e5_small_384`, 8.435 điểm (từ 05/11 tối); còn một collection thử ảnh `hue_anh_siglip2` (172 điểm, chatbot không dùng, chờ bạn quyết xoá) | `backend/vectorstore/`, `docker-compose.yml` |
| Tìm kiếm | `dense_bm25_rrf` (mục 3) | `backend/retrieval/full_corpus.py` |
| Trả lời | `gpt-6-luna` (OpenAI) | `backend/llm/generator_openai_full_corpus.py` |
| API + giao diện | FastAPI (`/api/chat`, `/api/chat/stream`, `/health`, `/api/feedback`, `/api/conversation/new`; từ 07/11 thêm 4 API chỉ đọc `/api/kham_pha`, `/api/kham_pha/bai`, `/api/thoi_tiet`, `/api/tinh_nang`; từ 08/11 `/api/anh/ung_vien` cho hỏi bằng ảnh); cổng web React + Vite + Tailwind (cổng đợt 1 từ 07/11, bản mẫu "Sông Hương"; điều hướng bằng `#/…`) — FastAPI phục vụ bản build tĩnh `frontend/dist/` (build một lần: `cd frontend && npm ci && npm run build`; thiếu bản build ⇒ API vẫn chạy, log cảnh báo) | `backend/api/` (`routes/cong.py` cho 4 API chỉ đọc, `routes/anh.py` cho ảnh), `frontend/src/` (`App.jsx`, `pages.jsx`, `chat.jsx`, `route.js`) |
| Thời tiết | Open-Meteo (miễn phí), cache 30 phút, số do code dựng; **bật từ 07/11** | `backend/llm/thoi_tiet.py` |
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
   câu trả lời, nguồn, tiền (tiền tính sau từ token theo bảng giá). Thêm < 1 ms mỗi câu. Từ 01/11 ghi thêm token **ghi đệm / đọc đệm** (để tính đúng giá),
   và ở đường stream: thời gian tới sự kiện / chữ đầu tiên, có ngắt giữa chừng không.
8. **Chữ hiện dần (từ 01/11, `POST /api/chat/stream`, trang web dùng đường này):** bước 0–5 như trên; lỗi trước khi model viết vẫn trả JSON như `/api/chat`.
   Khi model viết, server gửi từng mảnh chữ (sự kiện `status` → `delta` … → `sources` → `done`); **bước 6 (kiểm trích dẫn) chạy lúc cuối** — qua thì mới gửi
   nguồn và hiện dòng "Nguồn" (từ 07/11; trước đó là số [n] bấm được trong chữ); **hỏng thì trang web rút lại chữ đã hiện**, lỗi / đứt giữa chừng thì **xoá hết** — cả hai hiện lời báo + nút "Thử lại" (bạn chọn 31/10).
   Người dùng rời trang ⇒ server dừng model, vẫn ghi một dòng log. Trang web chỉ hiện các thẻ Markdown thường (danh sách cho phép) và có chính sách bảo mật
   trang (CSP) — không tự tải ảnh / tài nguyên từ máy khác. `/api/chat` (một lần, JSON) vẫn giữ; API và bộ đánh giá dùng **chung một lõi**
   (`backend/llm/assistant.py` — đổi tên từ `grounded_answer.py` ở Phase 9 B0, merge `1c10111` 19:48 02/11/2026) nên đo và chạy đi đúng một đường.
9. **Phase 9 B0 — nền cho trợ lý agent (merge `1c10111`, 19:48 02/11/2026; người dùng thấy không đổi):** bước "tìm + dựng ngữ cảnh" được gói thành công cụ
   `tim_kho` (code gọi, chưa để model tự gọi); có "sổ nguồn" để sau này ghép nguồn kho với nguồn web. Mỗi câu hỏi, dòng log `chat_metrics` ghi thêm **tuyến**
   (hiện luôn là `tro_ly_hue` — trợ lý Huế), **tiền USD của câu**, số lần gọi model và từng lần gọi (loại đầu ra, ms, USD, 5 loại token), công cụ đã chạy + ms.
   Chứng minh "không đổi": kết quả tìm 158 câu giống từng byte mốc T1 `4d5bbe9e0edc`; chuỗi gửi OpenAI giống từng byte bản cũ trên 176 + 20 câu (B127, review C128).
10. **Phase 9 B1 — phân loại câu hỏi (định tuyến) + dòng nhắc (merge `f01c032`, 03/11/2026):** sau bước 0, **một lần gọi `gpt-6-luna` ngắn** (~580 token vào,
   ~35 ra, ~1,5 s) trả một trong 4 tuyến (`backend/llm/assistant.py` `_pick_route`; `settings.yaml` khối `assistant:`):
   - `tro_ly_hue` (hỏi về Huế) ⇒ bước 1–7 như trên, lời dặn và đoạn kho gửi model **giống từng byte** bản trước;
   - `tro_chuyen` (chào hỏi, cảm ơn) ⇒ model đáp ngắn, không tìm kho, không trích dẫn;
   - `ngoai_pham_vi` ⇒ câu soạn sẵn; `khan_cap` ⇒ **từ 09/11 (phương án B, merge `3b52017`, bạn chấp nhận bỏ câu soạn sẵn 08/11): đi đúng đường `tro_ly_hue`** (log giữ dấu `emergency_by: router`) ⇒ câu trả lời từ kho, hoặc "không đủ thông tin" + mục web, hoặc câu cố định NCHMF / 112 nếu là thiên tai. Trước 09/11: câu soạn sẵn 5 dòng 113 / 114 / 115 / 112;
   - định tuyến lỗi / quá 10 s ⇒ đi `tro_ly_hue` (đường cũ).
   - **từ 03/11 tối (B143, merge `e3cdb96`):** định nghĩa `khan_cap` thêm "vừa bị cướp / giật / trộm / móc túi / hành hung / đe doạ, cần báo công an — dù việc đã xảy ra" (trước đó câu loại này đi `tro_ly_hue` và bị từ chối).
   - (04/11 B154 đổi dòng mở câu soạn sẵn — câu soạn sẵn đã gỡ 09/11.)
   Câu trả lời có nguồn vé / điểm đến / lễ hội ⇒ thêm dòng nhắc "thông tin có thể đã thay đổi" (cờ `may_have_changed_notice`). Log ghi thêm tuyến + lần gọi định tuyến (`llm_calls` có `route: router`).
   **Đã thử, bỏ:** luật từ khoá khẩn cấp không gọi model — bắt 0 / 8 câu khẩn cấp kín, chặn nhầm 2 / 8 câu thường ⇒ tắt, **gỡ hẳn code 09/11**;
   dòng "hôm nay là ngày…" gửi model — từ chối nhầm câu theo ngày không giảm (5,0 ⇒ 4,5, cần giảm ≥ 3) ⇒ tắt (thay bằng công cụ ngày, bước 17).
   **Thử 09/11, không áp dụng:** định tuyến "2 nhóm" (chỉ tách xã giao, agent tự từ chối câu ngoài phạm vi) — 2 / 44 câu ngoài phạm vi đã thấy có mục web (bản cũ 0 / 44) ⇒ giữ 4 tuyến (tag `hoso/p9-g-cong`).
   Kết quả đo (B129 / B131, review C132 / C134): định tuyến đúng 253 / 253 câu đã thấy + 20 / 20 kín; Golden 176: sàn đạt, điểm Đúng đạt, đủ ý TB −0,02 [−0,07; +0,02], từ chối nhầm 12 = mốc, nhưng **6 câu tụt > ngưỡng 5** — lần gọi trả lời giống từng byte bản trước trên 176 / 176 câu ⇒ khác biệt là nhiễu sinh lại, theo spec §4 dùng lại số bậc trước (A quyết, ghi trung thực); bộ an toàn 32: giống từng byte ⇒ dùng lại kết quả 01/11. Tiền B1 ≈ 0,145 USD.
   Lưu ý đo: `evaluation generate` không truyền `--flags` nay theo `settings.yaml` (có định tuyến) ⇒ đo đường RAG 1–8 thuần phải truyền `--flags` rỗng.
11. **Phase 9 B2 — trợ lý tự tìm thêm (merge `00d670e`, 03/11/2026):** tuyến `tro_ly_hue` — code tìm lần đầu bằng câu gốc (như bước 1–4), rồi `gpt-6-luna` được **gọi công cụ `tim_kho`
   thêm tối đa 2 lần** bằng câu tìm nó tự viết (mỗi lần ≤ 10 đoạn mới, cả lượt ≤ 30 đoạn, một ngân sách token; lần thứ 3 nhận "đã hết lượt tìm", không tìm Qdrant); `max_turns` 4, hết lượt ⇒ câu từ chối.
   Đoạn mới đánh số tiếp trong sổ nguồn; kiểm trích dẫn như bước 6. Trang web hiện thẻ "Đang tìm / Đã tìm thông tin…" mỗi lần tìm (cờ `tim_them`, `settings.yaml`).
   Kết quả (B134, review C137 / C141): 18 câu nhiều nguồn đủ ý **+1,17** [+0,44; +2,00] (6 tốt hơn / 12 như cũ / 0 kém); Golden đủ ý / đúng TB +0,22; 0 câu ngoài kho bị trả lời; từ chối nhầm 12 ⇒ 4–6;
   **bộ an toàn: 1 câu sai mới thật** (thêm lời khuyên chung không có trong nguồn, không đảo cảnh báo; luật cho ≤ 2 cả Phase) ⇒ bạn giữ, sửa lời dặn ở B3. Tiền ≈ 0,00031 USD / câu (trước 0,00023).
   **Đã thử, không giữ (B2a):** để model viết lại câu tìm đầu (3 cách) — không cách nào thêm đủ 3 / 12 câu có bằng chứng ở cả hai lượt ⇒ giữ câu gốc (`BAO_CAO_TIM_KIEM.md`).
12. **Phase 9 B3 (merge `a3dabba`, 03/11/2026 tối):** (a) lời dặn trả lời thêm câu hẹp D6 — không tự thêm lời khuyên / lưu ý an toàn mà Bằng chứng không nêu, giữ lời khuyên có trong Bằng chứng (đo 208 câu: từ chối nhầm 4, 0 câu sai điều kiện, câu an toàn lỗi của B2 hết lỗi) — **chạy cho mọi câu**;
   (b) **nhớ hội thoại** (`backend/api/conversations.py`): server giữ 3 lượt gần nhất của một cuộc trong RAM, cookie `HttpOnly` / `SameSite=Strict` 30 phút; định tuyến + trợ lý đọc lịch sử; lần tìm đầu vẫn bằng câu gõ, `tim_kho` thêm bằng câu model viết có tên đối tượng; "Cuộc trò chuyện mới" xoá nhớ —
   **bật từ B3b (merge `9e2ecd9`)** với `nho_cau_tra_loi: false` — chỉ lưu câu hỏi các lượt trước; câu dặn đường có lịch sử: nhận định + trích dẫn chỉ từ đoạn nói đúng đối tượng (B3 trước đó tắt vì 1 / 2 lượt ngoài kho kín bị trả lời bằng đoạn đối tượng khác; B3b: bộ mới 6 / 6 từ chối đúng, từ chối nhầm 0 / 19);
   (c) giao diện nhiều lượt (Bản 1 — Huế hiện đại): lượt nối nhau, số nguồn hiển thị đánh lại 1..k, nút "Cuộc trò chuyện mới". Hồ sơ: `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md`, review `b136_review.md`.
13. **Đánh giá của người dùng + gợi ý (B142, merge `6817897`, 03/11/2026 tối):** mỗi lượt có câu trả lời cuối nhận `turn_id` ngẫu nhiên (RAM, ≤ 2.000; không liên quan mã cuộc; trả trong `/api/chat` và sự kiện `done` của stream); nút 👍 / 👎 gọi `POST /api/feedback` ⇒ một dòng log `chat_feedback` (turn_id, tuyến, kết quả, số nguồn, đánh giá — không chữ). Câu `ngoai_pham_vi` hiện 3 nút câu gợi ý cố định có trong kho. Hồ sơ `b142_phan_hoi_implementation.md`, review `b142_review.md`.
14. **Phase 9 B6 — tra web khi kho không có (merge `7ff8e5a`, BẬT 21:15 05/11/2026):** chỉ khi tuyến `tro_ly_hue` ra câu "không đủ thông tin" của kho ⇒ code tra Serper một lần (hạn 5 s) ⇒ một lần gọi model viết mục **"Từ web (chưa kiểm)"** tách khỏi câu trả lời kho, mã [w n] trỏ link trong sổ kết quả; code kiểm trước khi hiện: link / HTML thô bị chặn, số tiền phải có trong đoạn trích, câu lưu trú 0 số tiền, câu thời gian thực 0 chữ số / ngày giờ, câu thiên tai (lũ, lụt, bão, áp thấp…) ⇒ câu cố định "xem NCHMF / chính quyền, khẩn cấp gọi 112" + link (không chữ do model viết). Câu kho trả lời được: không đổi. Đổi lại: mục web tới sau ~9–18 s; ~0,0016–0,0018 USD / câu đi web.
15. **Thời tiết (B5b, code vào `main` 06/11 tối, BẬT 07/11 — bạn chọn khi merge cổng):** tuyến `tro_ly_hue` có thêm công cụ `thoi_tiet`: model hỏi ngày ⇒ code lấy dự báo Huế từ Open-Meteo (cache 30 phút, một lần gọi, không thử lại), **số do code dựng** thành khối nối sau câu trả lời kèm giờ số liệu + ghi công Open-Meteo; ngoài 7 ngày ⇒ câu cố định; bão / lũ ⇒ câu cố định NCHMF + 112. Ô "Huế hôm nay" ở trang chủ đọc `GET /api/thoi_tiet` (cùng hàm + cache, không gọi model); lỗi ⇒ ẩn ô, không hiện số cũ. Cổng sau khi bật (A, 07/11): câu thời tiết gọi đúng công cụ, ghi Open-Meteo + giờ.
16. **Cổng du lịch đợt 1 (merge `dbfc925`, 07/11/2026):**
   - **Giao diện:** điều hướng bằng `#/…` (không gói router). Trang chủ, Khám phá (5 lĩnh vực, chip lọc loại con, "Xem thêm"), trang bài (Markdown kho qua bộ lọc DOMPurify, link ngoài mở tab mới `rel=noopener noreferrer`), Trợ lý Huế (nút nổi + trang `#/tro-ly`, chung một cuộc), Giới thiệu, thanh dưới điện thoại. Cờ đọc từ `/api/tinh_nang` ⇒ mục nào tắt thì ẩn.
   - **4 API chỉ đọc, không gọi model:** `/api/kham_pha` (danh sách 204 bài = đúng danh sách file của chỉ mục), `/api/kham_pha/bai?id=` (chỉ nhận mã bài **trùng nguyên văn** một file trong danh sách — `..`, `evaluation/`, câu kín, mã hoá lạ ⇒ 404; không ghép đường dẫn từ chữ người dùng), `/api/thoi_tiet`, `/api/tinh_nang` (chỉ đúng / sai).
   - **Nguồn:** mỗi nguồn kèm `bai_id` khi là một bài kho ⇒ "Đọc cả bài" mở trang bài.
   - **Biểu mẫu "Lên kế hoạch" — BẬT 07/11** (bạn duyệt; cờ `lich_trinh_bieu_mau: true`, `a884de4`): chọn số ngày / đi cùng / sở thích ⇒ **code** xếp lịch bằng đúng giá trị nút (không định tuyến, không công cụ, chữ gõ không vào model) ⇒ model chỉ viết lời theo khung. **V5:** luật viết lời đặt trong lời dặn hệ thống + mức suy luận "low" **chỉ ở lượt này** (lượt khác giống byte như trước). Model vẫn từ chối ⇒ code tự dựng lời lịch tối thiểu. "Sửa" ⇒ về biểu mẫu chọn sẵn lựa chọn cũ (sửa lịch bằng chat chưa có).
   - Kiểm: review cả nhánh đạt; 228 / 228 chuỗi gửi model giống byte khi cờ mới tắt; Playwright 7 / 7 đích ≤ 2 lần bấm, 0 lỗi CSP / console, tương phản ≥ 4,5 : 1 (17 cặp), 10 / 10 câu dòng "Nguồn" khớp nguồn API; JS 106 KB gzip; cổng ổn định sau merge (352 test, `/health` 5 / 5, 3 câu thật, 0 câu hỏi trong log, ≈ 0,001 USD).
17. **Ngày + âm lịch (T1, merge `99ea59a`, BẬT 09/11 `7eb1f12`, bạn duyệt):** câu cuối (hoặc câu hỏi liền trước) có từ chỉ ngày ("hôm nay", "tối mai", "tuần sau", "tháng này", "năm sau", "sang năm", "rằm", "mùng", "Tết", "thứ Bảy", "15/1"…; không tính "vua thứ ba", "24/7") ⇒ **từ 10/11 (merge `1633c18`) code tính sẵn trước lần gọi model đầu** (`lich_san`): hôm nay, ngày mai, từng ngày "tuần này / tuần sau" (cả "chủ nhật này", "cuối tuần"), "rằm tháng này / tới", và các ngày âm có trong câu hỏi (Tết, "rằm / mùng … tháng …", "… âm lịch") hoặc trong đoạn kho lần tìm đầu (≤ 6; "mùng N tháng <số>" chỉ tính khi có chữ "âm") — mỗi ngày âm: lần đã qua + lần sắp tới, và đúng năm âm khi câu nói "năm nay / năm sau"; thêm thành nguồn "Lịch hệ thống". Đo 10/11 (19 câu): chữ đầu 5,60 ⇒ 2,35 s trung vị, 10,14 ⇒ 4,56 s p95; 0,00049 ⇒ 0,00036 USD; số câu sai ngày không tăng; model không gọi công cụ lần nào. Công cụ `ngay_lich` vẫn có (≤ 2 lần / câu, thêm 1 vòng trần) làm **dự phòng** cho ngày chưa có trong nguồn đó (dạng ít gặp: "ngày kia", "tháng tới"…). **Code** (`backend/llm/ngay_lich.py`, thư viện `lunar-vn`, lịch Việt Nam UTC+7, năm 1976–2100) trả: hôm nay (thứ, dương, âm, can chi), ngày được đổi + "đã qua N ngày / còn N ngày nữa", khoảng "tuần này / tuần sau / tháng này"; không nêu năm hoặc nói "năm nay" với ngày âm ⇒ cả lần đã qua lẫn lần sắp tới + dòng nhắc ghi rõ năm. Kết quả là một nguồn trong sổ nguồn ("Lịch hệ thống — tính theo giờ Việt Nam") ⇒ câu chỉ có ngày vẫn trích được. Đo: 14 câu mới bớt 9 từ chối nhầm, 0 sai ngày; server thật sau khi bật: "rằm tháng Giêng" ⇒ thứ Bảy 20/02/2027. Giới hạn: câu lịch thuần không nhắc Huế bị định tuyến xếp ngoài phạm vi; "tháng tới / cuối tuần" model tự cộng.

## 4. Chất lượng, tốc độ, tiền đo được

**Bản đang chạy (10 đoạn ngữ cảnh + NFC):**

| Đo gì | Kết quả | Nguồn |
|---|---|---|
| So với bản cũ (5 đoạn) trên 33 câu kín trong kho — câu viết mới, giữ kín tới cuối Phase 8 | điểm Đủ ý **+0,82** [+0,39; +1,33], điểm Đúng **+0,70**, **0 câu tụt**; câu ngoài kho bị trả lời **0 / 3** | `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` |
| Lượt đo mới nhất trên 176 câu Golden (30/10, sau sửa kho đợt 2) | không làm hỏng so với trước đợt 2 (trên 129 câu số chính: 4 câu tốt hơn / 3 kém hơn / 122 như cũ); từ chối nhầm 13 ⇒ 12 câu; 0 lỗi kỹ thuật, 0 lỗi trích dẫn mới; bộ an toàn 32 câu: 0 câu ngoài kho bị trả lời, 0 câu nói sai điều kiện mới | `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` |
| Thời gian chờ (176 câu, hỏi lần lượt, đo trong công cụ đo — **chưa** tính đường mạng tới trang web) | trung vị **2,19 s**, câu chậm (p95) **4,90 s** — trong trần bạn chốt 3 / 5 s; câu trả lời dài (bộ tự viết) trung vị 4,6 s ⇒ chưa đạt | như trên; `BAO_CAO_DANH_GIA.md` |
| Chữ đầu tiên sau B1 (03/11, 10 câu tự viết, `/api/chat/stream`, máy khách tuần tự) | cả 10 câu trung vị **3,05 s** / p95 **5,64 s**; câu về Huế **3,57 / 6,57 s**; trò chuyện 2,63 / 2,82 s; ngoài phạm vi 1,82 / 1,93 s; khẩn cấp 1,63 s. Trước B1: 1,23 / 2,61 s ⇒ vượt sàn cũ 3 / 5 s — Phase 9 chỉ theo dõi (bạn để mặc định 03/11: merge, tối ưu sau B2). Mẫu nhỏ: p95 gần bằng câu chậm nhất | `report_agent/2026-11-02_phase_9_code/b129_b1_implementation.md` §4b |
| Chữ đầu tiên sau B2 (03/11, cùng 10 câu, script gọi API) | cả 10 câu trung vị **3,33 s** / p95 **5,20 s**; câu về Huế **3,50 / 5,33 s** (B1: 3,57 / 6,57) — tìm thêm gần như không làm chậm chữ đầu; vẫn vượt sàn cũ, chỉ theo dõi | `b134_b2_implementation.md` §4c |
| Song song #6 (04/11, bật 05/11) | chữ đầu câu về Huế nhanh hơn trung vị **1,37 s** [0,34; 2,14] so với chờ định tuyến xong | `BAO_CAO_SINH_CAU_TRA_LOI_API.md` mục 05/11 |
| Chữ đầu trên cổng mới (07/11, 10 câu tự viết có nguồn, đồng hồ trình duyệt, máy rảnh) | bấm gửi ⇒ chữ đầu trung vị **2,03 s**, chậm nhất 4,22 s; ⇒ hết câu 2,51 / 6,03 s. Khác bộ câu + cách đo với các dòng trên ⇒ chỉ tham khảo | `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` §5 |
| **Lượt đo chung mới nhất (09/11, `main` sau mọi thay đổi 09/11, 65 câu, trình duyệt thật, một lượt — số hiện hành)** | chữ đầu: câu về Huế trung vị **2,16 s** / p95 **4,32 s** ✓; ngoài phạm vi 1,62 / 2,97 s ✓; **xã giao 3,46 / 7,73 s ✗** (chờ định tuyến ~1,7 s xong mới gọi model trò chuyện); câu có ngày lúc đó (n = 5) 5,19 s ✗ ⇒ **10/11 sau khi code tính sẵn ngày: trung vị 2,35 s / p95 4,56 s, 0,00036 USD / câu (19 câu, 1 lượt, đo ở máy chủ; trước 5,60 / 10,14 s, 0,00049 USD) ✓**. So 07/11 câu về Huế chậm hơn ~0,4 s trung vị (khác bộ câu — tham khảo). Cả lượt 0,0197 USD | `session_prompt/Project_Status.md` §2; `session_prompt/CURRENT_HANDOFF.md` "PHIÊN SAU ĐỌC TRƯỚC" |
| Tiền một câu (giá đủ, cùng lượt 09/11) | câu về Huế **0,00047 USD** (~12 đồng) ✓ trần 0,0005 (sát trần); câu có ngày 0,00063 USD ✗ lúc đó ⇒ **0,00036 USD ✓ từ 10/11**. Trước Phase 9 (01/11): ≈ 0,00025 USD / câu | như trên |

Người chấm: Claude (chấm theo đáp án mẫu). Mốc người: B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp).

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

Xếp theo **mức nặng bạn chốt 28/10**: **M1** sai cảnh báo an toàn / điều kiện vào khu vực > **M2** nói chắc sai / bịa > **M3** trả lời câu ngoài kho > **M4** thiếu ý > **M5** từ chối nhầm.
Ngoài thang đó: **tốc độ / tiền** (yêu cầu bạn chốt: p50 ≤ 3 s, p95 ≤ 5 s, ≤ 0,0005 USD / câu), **thước đo** (giới hạn của bằng chứng — không phải lỗi người dùng thấy, nhưng làm kết luận yếu đi),
**vận hành** (chạy / bảo trì).

**Chất lượng câu trả lời (người dùng thấy)**

- **M1 — có thể nói sai điều kiện / cảnh báo** (vé, giờ, quy định vào khu vực): bộ 32 câu an toàn hiện **0** câu sai mới, 0 câu đảo cảnh báo (30/10); trước đó 2 câu từng nói sai *về nguồn*
  ("nguồn không nêu…") rồi lần sinh lại không sai ⇒ "lúc có lúc không". Bộ này do AI viết, chỉ 28 câu trong kho ⇒ "0 lỗi" chỉ nói được tỉ lệ sai dưới ~12 %.
- **M1 — kho có dữ kiện theo thời điểm** (giá, giờ mở cửa, lịch, tên đơn vị hành chính) có thể đã cũ; hai đợt sửa kho đã sửa 246 chỗ và **không làm hỏng** chatbot, nhưng vẫn còn mục chờ tra ngoài /
  chờ người địa phương.
- **M1 / M5 — model không biết hôm nay là ngày nào — đã xử lý 09/11** (công cụ ngày bật, mục 3 bước 17): 14 câu mới bớt 9 từ chối nhầm, 0 sai ngày; 10/11 code tính sẵn ngày ⇒ nhanh hơn, đạt sàn tốc độ / tiền. Còn: câu lịch thuần không nhắc Huế ⇒ ngoài phạm vi; "tháng tới / cuối tuần" model tự cộng; "dịp lễ sắp tới" cần lịch sự kiện theo ngày.
- **Thử 09/11, không áp dụng:** trợ lý tự yêu cầu tra web phần kho thiếu (T2) — 26 / 29 lần yêu cầu thì vẫn từ chối cả câu ⇒ không lợi (tag `hoso/p9-t2-web`); lịch trình từ câu gõ tự do (T4) — lịch "hợp người đi cùng" 21 / 27 · 15 / 27 (cần 26) ⇒ lịch trình chỉ qua biểu mẫu (tag `hoso/p9-t4-lich`).
- **Biểu mẫu "Lên kế hoạch" (đọc code + bảng 09/11):** nút "dày lịch" gần như không tác dụng (bảng 1 / 28 điểm có thời lượng "ngắn" — chờ bảng v7); nhóm người lớn tuổi / trẻ em không có buổi tối; không nói được "lo mưa", giờ tới / về.
- **M2 — đôi khi thêm chi tiết không có trong nguồn** (thường là nhận xét chung ở câu nhiều nguồn): 1 / 145 câu (Claude chấm, chưa có người đọc). **Bộ kiểm trích dẫn chỉ kiểm định dạng** (`[n]` có, số nguồn
  có thật), không kiểm câu chữ có đúng với nguồn được trích ⇒ "có trích dẫn" nghĩa là *có nguồn*, chưa phải *đã kiểm nghĩa*.
- **M3 — câu ngoài kho:** 0 câu bị trả lời trên mọi bộ đã đo (25 câu ngoài kho) — mẫu nhỏ, cận trên ~12 %.
- **M4 / M5 — câu so sánh / cần nhiều nguồn** điểm thấp hơn rõ, hay bị từ chối cả câu khi chỉ tìm được một vế; đưa 10 đoạn (28/10) đã cải thiện chủ yếu ở loại này, số theo loại câu trên kho hiện tại
  **chưa đo lại**.
- **M5 — từ chối câu mà kho có đáp án:** **4–6 / 158** câu sau khi trợ lý được tìm thêm (B2, 03/11; trước đó 12 / 158 ngày 30/10) — vẫn là lỗi nhiều nhất về số; nguyên nhân chính là **xếp hạng**: đoạn chứa đáp án có trong 30 ứng viên nhưng bị xếp ngoài 10 đoạn đưa model
  (9 / 40 câu thử). Các cách đã thử (lấy 100 ứng viên, xếp lại bằng model, model vector lớn Qwen3-8B, cho trả lời một phần) đều **không qua luật** ⇒ giữ cách hiện tại.
- **M4 / M5 — dòng bảng giá dài** bị tách thành đoạn một dòng ⇒ khó tìm đúng dòng giá; chưa có số riêng ở cấu hình hiện tại.
- **M4 — ~20 % đoạn rất ngắn** (mỗi khối Markdown là một đoạn; đếm trên kho cũ): đã thử 12 cách chia khác, không cách nào tốt hơn ⇒ giữ.
- **Câu gõ không dấu:** ngoài phạm vi (bạn quyết 25/10 — người dùng gõ có dấu); đo được: tìm kiếm gần như hỏng (13 ⇒ 1 / 32 câu đủ đoạn đúng).

**Tốc độ, tiền, tính năng**

- **Tốc độ (đo "tới chữ trả lời đầu tiên trên trình duyệt"; số hiện hành = lượt đo chung 09/11, mục 4):** câu về Huế 2,16 / 4,32 s ⇒ **đạt** sàn 3 / 5 s; **câu xã giao p95 7,73 s ⇒ vượt** (phải chờ định tuyến xong mới gọi model trò chuyện); **câu có ngày: từ 10/11 trung vị 2,35 s / p95 4,56 s, 0,00036 USD / câu (19 câu, 1 lượt, đo ở máy chủ; trước 5,60 / 10,14 s, 0,00049 USD) ⇒ đạt** (09/11 còn 5,19 s, 3–5 lần gọi model / câu); cách làm nhanh câu xã giao đang thử 10/11. Một lượt đo mỗi loại ⇒ số còn thô.
  Trước khi có định tuyến (01/11, 38 câu): 1,23 / 2,61 s; bạn chọn giữ cách hiện chữ dần (lợi ~0,44 s so với chờ đủ câu).
- **Tiền (giá đủ, lượt 09/11):** câu về Huế ≈ **0,00047 USD / câu** ⇒ đạt trần 0,0005 nhưng sát trần; **câu có ngày 0,00036 USD ⇒ đạt từ 10/11** (09/11: 0,00063 vượt). Trước Phase 9 (01/11) ≈ 0,00025 USD / câu. Công cụ đo tính theo giá đủ từ 01/11.
- **Nhớ có giới hạn (từ 03/11 tối):** chỉ nhớ câu hỏi 3 lượt gần nhất, không nhớ câu trả lời ⇒ "ý thứ hai bạn vừa nói…" chưa hiểu; cookie hết hạn 30 phút thì server âm thầm bắt đầu cuộc mới trong khi màn hình còn lượt cũ (chưa xử lý).
- **Một nhà cung cấp sinh** (`gpt-6-luna`), không dự phòng: lỗi hoặc quá 45 s ⇒ báo lỗi, không tự đổi model.
- **Chưa đưa ra ngoài:** chạy máy cá nhân. 4 chốt trước khi đưa link công khai **đã có code từ 09/11** (giới hạn số lượt hỏi / IP / ngày, cookie chỉ qua https, tắt trang `/docs` — 3 chốt này bật bằng biến môi trường lúc deploy, không đặt ⇒ như cũ; log xoay vòng 10 MB × 3 thì luôn bật). Còn chưa có: đăng nhập, hạn mức tiền phía nhà cung cấp (OpenAI / Serper).

**Streaming (chạy từ 01/11)**

- Trong vài giây người dùng thấy chữ **chưa qua bộ kiểm**; nếu bộ kiểm cuối hỏng thì chữ bị rút lại, lỗi giữa chừng thì xoá hết + nút "Thử lại" (bạn chọn 31/10). Lỗi kiểm cuối hôm nay 0 / 489 lần ⇒ hiếm;
  sẽ xem lại nếu > 1 % câu / tuần bị rút / xoá. Ca giao diện "rút lại" và "luồng đứt" chưa kiểm được bằng đường thật (chỉ phát lại luồng). Giao diện **làm lại 02/11** (merge `ed8e6e8`)
  rồi **thành cổng đợt 1 07/11** (merge `dbfc925`) — giữ đủ 17 yêu cầu đó; nguồn nay là dòng "Nguồn" dưới câu (bỏ số trong chữ); nhãn "có thể sai"; lỗi mạng / server lạ báo bằng tiếng Việt.
- **Ảnh cổng (09:58 08/11/2026, `c9931be`):** 7 ảnh thật (6 ảnh Commons trong git + ảnh lễ hội riêng ngoài git; bản tải về dùng ảnh Commons thay), ghi công ở Giới thiệu.
- **Cổng chưa có:** lưu trú, ăn uống theo cơ sở, sự kiện theo ngày (đợt 2); bản đồ lịch trình có code, cờ tắt (chờ bạn tick phiếu toạ độ).

**Thước đo (giới hạn của bằng chứng)**

- **Mốc người chỉ tham khảo:** mọi điểm chất lượng do Claude chấm (khớp `gpt-6-luna` 89–96 %). B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp).
- **Không còn bộ câu chưa ai thấy:** nhóm kiểm 56 câu và 36 câu kín đã dùng ⇒ số hiện tại có thể lạc quan hơn câu thật; **bộ kín mới** 40 câu cũng đã dùng ở lượt đo cuối 01/11 ⇒ lần kiểm sau cần bộ mới nữa.
- **Bộ đo nhỏ:** chỉ 55 / 176 câu có nhãn "đoạn đúng" ⇒ nhiều thí nghiệm ra "chưa rõ" — nghĩa là *chưa chứng minh được*, không phải *đã chứng minh bằng nhau*.
- **Gần như chưa có so sánh nào đo lại trên kho hiện tại:** phần lớn kết luận "giữ" của Phase 8 đo trên kho / cấu hình cũ. **Model sinh chưa từng được so có chấm điểm** (giữ `gpt-6-luna` theo quyết định
  của bạn 24/10).
- Không lưu câu hỏi người dùng ⇒ mọi số đo trên câu tự viết / Golden, chưa có câu hỏi thật.
- Lệnh kiểm Golden báo **1 lỗi đã biết** (1 câu khác kho chỉ ở chữ hoa / thường — không làm sai điểm; bạn chọn giữ nguyên 01/11).

**Vận hành**

- Log xoay vòng từ 09/11 (mỗi file ≤ 10 MB, giữ 3 file cũ); log dùng chung cho test và server. Bộ test không có key OpenAI vẫn báo vài lỗi "bình thường" ⇒ chưa có một lệnh kiểm sạch. Kho không có Git (sửa bằng sao lưu tay + so
  khác). Mã đoạn dạng `<file>#<số>` dồn số khi thêm / xoá đoạn giữa file. Bộ chia đoạn còn giới hạn 256 token của một model đã bỏ.

Chi tiết từng dòng (số đo, nguồn, hướng xử lý) và mọi phương án đã thử: báo cáo khâu (`BAO_CAO_*.md`) và [`BAO_CAO_SO_SANH_PHUONG_AN.md`](BAO_CAO_SO_SANH_PHUONG_AN.md).

**Việc kế tiếp (sau 09/11):**
- **Bạn chốt mốc đóng tính năng** (chưa chốt; A đề xuất 30/11).
- **Khi bạn rảnh (không chặn việc khác):** duyệt bảng điểm v7 (cột thời lượng ⇒ nút "dày lịch" có tác dụng); tick phiếu toạ độ (⇒ bật bản đồ lịch trình); thu 40 câu giọng nói.
- **Đang thử 10/11 (chưa vào chatbot):** cho câu xã giao chạy song song với định tuyến. (Câu có ngày — code tính sẵn ngày — **đã vào chatbot 10/11**, merge `1633c18`.)
- **Còn trước đóng gói:** bản đồ lịch trình, giọng nói, **B7** (so cả hệ với bản RAG 1–8, đóng gói Phase 9 — đang nháp kế hoạch); **deploy AWS chỉ khi hệ thống đủ tính năng, ổn định, đóng gói + Docker đầy đủ** (bạn quyết 08/11; đã thử build Docker trên máy; 4 chốt trước khi đưa link công khai đã có code 09/11). Đợt 2 cổng (lưu trú, ăn gần, sự kiện) chờ mốc đóng tính năng. Đóng code khi bạn nói (dự kiến 25–30/12/2026; đóng = đã chạy trên AWS).
- Biểu mẫu "Lên kế hoạch" (bật 07/11): bộ quyết 24 / 24 sàn code, lời khớp khung 12 / 12 mỗi lượt; lượt chậm 5,77 s ngay sau khởi động đã đo lại 07/11 (10 lượt: chữ đầu 2,30 / 4,22 s — dưới sàn 5 s, không tái tạo được); giới hạn còn lại ở mục 5 trên.
Lịch sử thứ tự cũ (30/10–01/11, đã xong):
1. ~~Hiện chữ dần (streaming)~~ — **xong, chạy từ 01/11** (merge `a80e12d`).
2. **Đóng gói Phase 1–8 — xong, Phase 8 bạn đóng 14:29 01/11/2026:** lượt đo cuối cùng một commit (Golden 176 + lượt lặp cùng ngày, bộ an toàn 32, câu theo ngày, 22 câu qua API, **bộ kín mới 40 câu**) — **xong 01/11, mọi sàn đạt** (`report_agent/2026-10-31_streaming_spec/do_cuoi_implementation.md`; bộ kín cho thấy số dev lạc quan: Đủ 4,18 ↔ 4,58); B0 xong 01/11 (bạn giữ 10 đoạn); báo cáo so sánh phương án (đã đăng 01/11, thêm phần mới khi xong); bảng giới hạn (mục này).
3. ~~Giao diện mới~~ — **xong 02/11** (merge `ed8e6e8`). Từ nhận xét B0: `[n]` chen trong câu khó đọc ⇒ **đã đổi 07/11** thành dòng "Nguồn" (cổng đợt 1).
4. Phase 9 — **đang làm, còn B7 đóng gói** (B0–B3b, B6, thời tiết, cổng đợt 1, biểu mẫu, ngày + âm lịch đã chạy — mục 3). Câu dự trù chi phí: thử hỏi lại người dùng (B4) và tính tiền bằng code (B5c) đều âm, không áp dụng.

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
| Một IP hỏi quá số lượt trong ngày (chỉ khi đặt biến `HUE_LUOT_MOI_NGAY`, từ 09/11) | 429 `rate_limited` | Người dùng thấy câu báo tiếng Việt; đếm trong RAM, không ghi IP vào log |

Code: `backend/api/app.py:65-85` (409 / 503 lúc khởi động), `backend/api/routes/chat.py` (502 / 500 khi hỏi), `backend/api/gioi_han.py` (429).

## Phụ lục — hồ sơ kỹ thuật

- Mã nội bộ: "B1" = việc đưa 10 đoạn + NFC vào chatbot (merge `510e1a8`, 28/10); "B3" = đo trên câu kín (33 câu trong kho); "H8" = giả thuyết
  "từ chối cả câu khi chỉ có một vế" (Phase 7B); "R2" = thử trả lời một phần; "K1" = 100 ứng viên; "K3b-m" = luna chọn 10 / 30; "F2" = lỗi
  bảng giá ngoài top-30 (Phase 6).
- Phiếu build `9921888f2030`, từ điển BM25 `4a8311a2dfef` (cả hai từ 05/11 tối; 30/10: `51fb1ec63cbc` / `c8134c49a648`); ghi `chat_metrics` từ `5100b90` (27/10); kiểm trích dẫn nhận `[Nguồn n]`
  từ `9e6d371` (25/10); API báo đúng mã lỗi từ `1e4acd0` (25/10).
- Spec streaming: `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 5 `00fb57ee01b2` (User duyệt 01/11); code vào `main` merge `a80e12d` (01/11); tổng hợp
  `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
