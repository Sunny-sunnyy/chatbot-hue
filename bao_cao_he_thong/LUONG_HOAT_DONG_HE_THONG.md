# Luồng hoạt động hiện tại của chatbot Huế (hue_rag)

**Cập nhật lần cuối: 10:25 05/11/2026 — bản 27: **hành vi không đổi**; code công cụ hỏi lại (B4) vào `main` với cờ **tắt** (merge `b019aab`, B4 âm hai vòng) — sẽ dùng lại ở B5 (lịch trình) theo cách code tự hỏi khi thiếu số ngày.** Trước: 20:32 04/11/2026 — bản 26: câu khẩn cấp soạn sẵn đổi dòng mở (phủ người vừa gặp chuyện; merge `4e3cb4e`).** Trước: 20:54 03/11/2026 — bản 25: định tuyến khẩn cấp phủ thêm "vừa bị cướp / giật / trộm / hành hung, cần báo công an" (merge `e3cdb96`, mục 3 bước 10).** Trước: 20:34 03/11/2026 — bản 24: nút 👍 / 👎 + `POST /api/feedback` (log `chat_feedback` không nội dung) và nút gợi ý dưới câu ngoài phạm vi (mục 3 bước 13).** Trước: 19:28 03/11/2026 — bản 23: Phase 9 B3b — **nhớ hội thoại bật** (merge `9e2ecd9`, mục 3 bước 12 (b)): chỉ nhớ câu hỏi, câu dặn nhận định chỉ từ đoạn nói đúng đối tượng.** Trước: 18:31 03/11/2026 — bản 22: Phase 9 B3 vào chatbot (merge `a3dabba`) — câu dặn hẹp (không tự thêm lời khuyên an toàn không có nguồn) + giao diện nhiều lượt Bản 1; **nhớ hội thoại có code nhưng TẮT** (mục 3 bước 12) chờ vòng sửa B3b.** Trước: 11:39 03/11/2026 — bản 21: Phase 9 B2 vào chatbot (merge `00d670e`) — trợ lý được **tự tìm thêm trong kho tối đa 2 lần** sau lần tìm đầu (mục 3 bước 11); câu nhiều nguồn đủ ý +1,17; thử để model viết lại câu tìm — không giữ.** Trước: 09:17 03/11/2026 — bản 20: Phase 9 B1 vào chatbot (merge `f01c032`) — trợ lý phân loại câu hỏi trước khi trả lời (mục 3 bước 10); chữ đầu tiên chậm hơn ~2 s (mục 4).** Trước: 19:48 02/11/2026 — Phase 9 B0 (nền trợ lý, người dùng thấy không đổi). Trước: 10:35 02/11/2026 — bản 19: giao diện web làm lại (React + Vite + Tailwind, merge `ed8e6e8`); API, tìm kiếm, model không đổi.** Trước: 14:33 01/11/2026 — bản 18: B0 xong, Phase 8 bạn đóng 14:29 01/11/2026.** Trước: 13:42 01/11/2026 — bản 17: lượt đo cuối xong (mọi sàn đạt). Trước: 12:50 01/11/2026 — bản 16: streaming vào chatbot (bước 8 mục 3, số tốc độ mới mục 5); công thức tiền giá đủ; việc kế tiếp = đo cuối.** Trước: 11:33 01/11/2026 — bản 15: mục 5 "Giới hạn đã biết" viết lại đầy đủ theo mức nặng (bảng giới hạn bản 4, 01/11); việc kế tiếp: streaming đang code, nhiều lượt dời Phase 9.** Bản 14: 17:10 31/10/2026.
Các bản trước: xem `git log` file này.

File này mô tả hệ thống **đang chạy**. Mỗi lần hành vi đổi (chia đoạn, chỉ mục, cách tìm, prompt, model), file này được cập nhật theo.
Những gì đã thử và bỏ nằm trong báo cáo từng khâu (`BAO_CAO_*.md` cùng thư mục). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

**Tóm tắt hôm nay (03/11):** kho 204 file / 8.424 đoạn; tìm bằng vector nghĩa e5-small + từ khoá BM25; đưa tối đa 10 đoạn vào ngữ cảnh; `gpt-6-luna`
trả lời có trích dẫn, chữ hiện dần trên giao diện web mới (React, 02/11). **Mới 03/11 (Phase 9 B1):** trước khi trả lời, model **phân loại câu hỏi** thành
trò chuyện / hỏi về Huế / ngoài phạm vi / khẩn cấp: câu chào hỏi được đáp tự nhiên (không tìm kho), câu ngoài phạm vi và câu khẩn cấp ra câu soạn sẵn
(khẩn cấp: số 113 / 114 / 115 / 112), câu về Huế đi đường RAG như cũ; câu trả lời có nguồn vé / điểm đến / lễ hội kèm dòng nhắc "thông tin có thể đã thay đổi".
**Mới 03/11 trưa (Phase 9 B2):** câu về Huế — sau lần tìm đầu bằng câu gốc, trợ lý được **tự gọi tìm thêm tối đa 2 lần** bằng câu tìm nó tự viết (câu nhiều nguồn
đủ ý **+1,17** [+0,44; +2,00]; từ chối nhầm 12 ⇒ 4–6 / 158). Đổi lại: **chữ đầu tiên chậm hơn bản RAG cũ** — câu về Huế trung vị 3,50 s / câu chậm 5,33 s (10 câu; trước Phase 9: 1,23 / 2,61 s) — Phase 9 chỉ theo dõi tốc độ (mục 4, 5).
Phase 8 bạn đóng 14:29 01/11/2026; Phase 9 (trợ lý agent có công cụ) đang làm bậc B2 (mục 5).

---

## 1. Toàn cảnh

```text
CHUẨN BỊ (chạy một lần khi kho đổi):
  204 file Markdown → chia đoạn (8.424 đoạn) → vector nghĩa e5-small + từ khoá BM25 → lưu Qdrant
HỎI ĐÁP (mỗi câu hỏi):
  giao diện web → API /api/chat/stream (hoặc /api/chat) → chuẩn hóa NFC → gpt-6-luna phân loại câu hỏi (từ 03/11)
    ├ trò chuyện → gpt-6-luna đáp ngắn, không tìm kho        ├ ngoài phạm vi / khẩn cấp → câu soạn sẵn
    └ hỏi về Huế → tìm 10 đoạn bằng câu gốc → ngữ cảnh → gpt-6-luna (được gọi tìm thêm ≤ 2 lần, từ 03/11) trả lời (chữ hiện dần) → kiểm trích dẫn [n] → nguồn
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
| API + giao diện | FastAPI (`/api/chat`, `/api/chat/stream`, `/health`); trang web React + Vite + Tailwind (từ 02/11) — FastAPI phục vụ bản build tĩnh `frontend/dist/` (build một lần: `cd frontend && npm ci && npm run build`; thiếu bản build ⇒ API vẫn chạy, log cảnh báo) | `backend/api/`, `frontend/src/` |
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
   nguồn và bật link [n]; **hỏng thì trang web rút lại chữ đã hiện**, lỗi / đứt giữa chừng thì **xoá hết** — cả hai hiện lời báo + nút "Thử lại" (bạn chọn 31/10).
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
   - `ngoai_pham_vi` ⇒ câu soạn sẵn; `khan_cap` ⇒ câu soạn sẵn 5 dòng: 113 công an · 114 cháy, cứu nạn · 115 cấp cứu · 112 thiên tai (số kiểm nguồn công khai 02/11) — model **không** viết lời khuyên khẩn cấp;
   - định tuyến lỗi / quá 10 s ⇒ đi `tro_ly_hue` (đường cũ).
   - **từ 03/11 tối (B143, merge `e3cdb96`):** định nghĩa `khan_cap` thêm "vừa bị cướp / giật / trộm / móc túi / hành hung / đe doạ, cần báo công an — dù việc đã xảy ra" (trước đó câu loại này đi `tro_ly_hue` và bị từ chối).
   - **từ 04/11 (B154, merge `4e3cb4e`):** dòng mở câu khẩn cấp = "Nếu bạn hoặc người bên cạnh đang gặp nguy hiểm **hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng)**, hãy gọi ngay số khẩn cấp (miễn phí):" (trước: "…đang gặp nguy hiểm, hãy gọi ngay…").
   Câu trả lời có nguồn vé / điểm đến / lễ hội ⇒ thêm dòng nhắc "thông tin có thể đã thay đổi" (cờ `may_have_changed_notice`). Log ghi thêm tuyến + lần gọi định tuyến (`llm_calls` có `route: router`).
   **Đã thử, tắt (code giữ sau cờ):** luật từ khoá khẩn cấp không gọi model — bắt 0 / 8 câu khẩn cấp kín, chặn nhầm 2 / 8 câu thường ⇒ tắt (định tuyến bắt 10 / 10 câu kín);
   dòng "hôm nay là ngày…" gửi model — từ chối nhầm câu theo ngày không giảm (5,0 ⇒ 4,5, cần giảm ≥ 3) ⇒ tắt.
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

## 4. Chất lượng, tốc độ, tiền đo được

**Bản đang chạy (10 đoạn ngữ cảnh + NFC):**

| Đo gì | Kết quả | Nguồn |
|---|---|---|
| So với bản cũ (5 đoạn) trên 33 câu kín trong kho — câu viết mới, giữ kín tới cuối Phase 8 | điểm Đủ ý **+0,82** [+0,39; +1,33], điểm Đúng **+0,70**, **0 câu tụt**; câu ngoài kho bị trả lời **0 / 3** | `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` |
| Lượt đo mới nhất trên 176 câu Golden (30/10, sau sửa kho đợt 2) | không làm hỏng so với trước đợt 2 (trên 129 câu số chính: 4 câu tốt hơn / 3 kém hơn / 122 như cũ); từ chối nhầm 13 ⇒ 12 câu; 0 lỗi kỹ thuật, 0 lỗi trích dẫn mới; bộ an toàn 32 câu: 0 câu ngoài kho bị trả lời, 0 câu nói sai điều kiện mới | `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` |
| Thời gian chờ (176 câu, hỏi lần lượt, đo trong công cụ đo — **chưa** tính đường mạng tới trang web) | trung vị **2,19 s**, câu chậm (p95) **4,90 s** — trong trần bạn chốt 3 / 5 s; câu trả lời dài (bộ tự viết) trung vị 4,6 s ⇒ chưa đạt | như trên; `BAO_CAO_DANH_GIA.md` |
| Chữ đầu tiên sau B1 (03/11, 10 câu tự viết, `/api/chat/stream`, máy khách tuần tự) | cả 10 câu trung vị **3,05 s** / p95 **5,64 s**; câu về Huế **3,57 / 6,57 s**; trò chuyện 2,63 / 2,82 s; ngoài phạm vi 1,82 / 1,93 s; khẩn cấp 1,63 s. Trước B1: 1,23 / 2,61 s ⇒ vượt sàn cũ 3 / 5 s — Phase 9 chỉ theo dõi (bạn để mặc định 03/11: merge, tối ưu sau B2). Mẫu nhỏ: p95 gần bằng câu chậm nhất | `report_agent/2026-11-02_phase_9_code/b129_b1_implementation.md` §4b |
| Chữ đầu tiên sau B2 (03/11, cùng 10 câu, script gọi API) | cả 10 câu trung vị **3,33 s** / p95 **5,20 s**; câu về Huế **3,50 / 5,33 s** (B1: 3,57 / 6,57) — tìm thêm gần như không làm chậm chữ đầu; vẫn vượt sàn cũ, chỉ theo dõi | `b134_b2_implementation.md` §4c |
| Tiền một câu | ~0,00021 USD (~5 đồng) tính theo giá phẳng 0,10 USD / 1M token vào, 0,50 USD / 1M token ra; nhà cung cấp còn tính phần "ghi đệm" 0,125 USD / 1M nên số thật cao hơn ~20 % (≈ 0,00025 USD / câu), vẫn dưới trần 0,0005. Sửa công thức tính tiền: việc đóng gói Phase 1–8 | `session_prompt/Project_Status.md` §5 (30/10) |

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
- **M1 / M5 — model không biết hôm nay là ngày nào:** câu "tối nay còn mở không?", "tuần sau có…?" — đo 30/10: **0** câu đoán ngày rồi nói sai, nhưng 6 / 14 câu bị **từ chối nhầm** dù ngữ cảnh có lịch ⇒
  để **Phase 9**. B1 (03/11) thử gửi "hôm nay là ngày…" cho model: từ chối nhầm không giảm (5,0 ⇒ 4,5 câu, cần giảm ≥ 3) ⇒ tắt; gốc ở tầng tìm / model, xét lại ở bậc sau.
- **M2 — đôi khi thêm chi tiết không có trong nguồn** (thường là nhận xét chung ở câu nhiều nguồn): 1 / 145 câu (Claude chấm, chưa có người đọc). **Bộ kiểm trích dẫn chỉ kiểm định dạng** (`[n]` có, số nguồn
  có thật), không kiểm câu chữ có đúng với nguồn được trích ⇒ "có trích dẫn" nghĩa là *có nguồn*, chưa phải *đã kiểm nghĩa*.
- **M3 — câu ngoài kho:** 0 câu bị trả lời trên mọi bộ đã đo (25 câu ngoài kho) — mẫu nhỏ, cận trên ~12 %.
- **M4 / M5 — câu so sánh / cần nhiều nguồn** điểm thấp hơn rõ, hay bị từ chối cả câu khi chỉ tìm được một vế; đưa 10 đoạn (28/10) đã cải thiện chủ yếu ở loại này, số theo loại câu trên kho hiện tại
  **chưa đo lại**.
- **M5 — từ chối câu mà kho có đáp án:** **12 / 158** câu (30/10) — lỗi lớn nhất về số; nguyên nhân chính là **xếp hạng**: đoạn chứa đáp án có trong 30 ứng viên nhưng bị xếp ngoài 10 đoạn đưa model
  (9 / 40 câu thử). Các cách đã thử (lấy 100 ứng viên, xếp lại bằng model, model vector lớn Qwen3-8B, cho trả lời một phần) đều **không qua luật** ⇒ giữ cách hiện tại.
- **M4 / M5 — dòng bảng giá dài** bị tách thành đoạn một dòng ⇒ khó tìm đúng dòng giá; chưa có số riêng ở cấu hình hiện tại.
- **M4 — ~20 % đoạn rất ngắn** (mỗi khối Markdown là một đoạn; đếm trên kho cũ): đã thử 12 cách chia khác, không cách nào tốt hơn ⇒ giữ.
- **Câu gõ không dấu:** ngoài phạm vi (bạn quyết 25/10 — người dùng gõ có dấu); đo được: tìm kiếm gần như hỏng (13 ⇒ 1 / 32 câu đủ đoạn đúng).

**Tốc độ, tiền, tính năng**

- **Tốc độ (từ 01/11 đo "tới chữ trả lời đầu tiên trên trình duyệt", streaming):** 38 câu có trả lời: trung vị **1,23 s** / p95 **2,61 s** / chậm nhất 4,74 s ⇒ **đạt** sàn 3 / 5 s và mục tiêu
  1,5 / 3 s; câu từ chối (21 câu) 1,48 / 2,93 s ⇒ đạt; tới đủ câu 1,73 / 3,81 s. Lợi "thấy chữ sớm hơn chờ đủ câu" chỉ ~**0,44 s** (câu thử ngắn, hôm đó model gần như không suy luận trước) —
  bạn chọn giữ cách hiện chữ dần (01/11). Một lần đo, 38 câu ⇒ p95 gần như là câu chậm thứ hai. Trước streaming (cả câu, qua API, 27/10): p50 3,07 / p95 6,04 s — chưa đạt.
- **Tiền:** ≈ **0,00025 USD / câu** theo giá đủ (lượt đo 01/11: TB 0,000247, lớn nhất 0,000339) ⇒ đạt trần 0,0005; công cụ đo **đã tính theo giá đủ** từ 01/11 (trước đó ghi thiếu ≈ 20 %).
- **Nhớ có giới hạn (từ 03/11 tối):** chỉ nhớ câu hỏi 3 lượt gần nhất, không nhớ câu trả lời ⇒ "ý thứ hai bạn vừa nói…" chưa hiểu; cookie hết hạn 30 phút thì server âm thầm bắt đầu cuộc mới trong khi màn hình còn lượt cũ (chưa xử lý).
- **Một nhà cung cấp sinh** (`gpt-6-luna`), không dự phòng: lỗi hoặc quá 45 s ⇒ báo lỗi, không tự đổi model.
- **Chưa đưa ra ngoài:** chạy máy cá nhân; API chưa giới hạn số lượt hỏi, chưa đăng nhập, chưa đặt hạn mức tiền phía nhà cung cấp ⇒ là điều kiện trước khi deploy.

**Streaming (chạy từ 01/11)**

- Trong vài giây người dùng thấy chữ **chưa qua bộ kiểm**; nếu bộ kiểm cuối hỏng thì chữ bị rút lại, lỗi giữa chừng thì xoá hết + nút "Thử lại" (bạn chọn 31/10). Lỗi kiểm cuối hôm nay 0 / 489 lần ⇒ hiếm;
  sẽ xem lại nếu > 1 % câu / tuần bị rút / xoá. Ca giao diện "rút lại" và "luồng đứt" chưa kiểm được bằng đường thật (chỉ phát lại luồng). Giao diện **làm lại 02/11** (merge `ed8e6e8`)
  giữ đủ 17 yêu cầu đó + nguồn hiện bằng số nhỏ bấm được + nhãn "Trợ lý AI… có thể sai"; lỗi mạng / server lạ báo bằng tiếng Việt (`report_agent/2026-11-02_giao_dien_moi_code/`).

**Thước đo (giới hạn của bằng chứng)**

- **Mốc người chỉ tham khảo:** mọi điểm chất lượng do Claude chấm (khớp `gpt-6-luna` 89–96 %). B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp).
- **Không còn bộ câu chưa ai thấy:** nhóm kiểm 56 câu và 36 câu kín đã dùng ⇒ số hiện tại có thể lạc quan hơn câu thật; **bộ kín mới** 40 câu cũng đã dùng ở lượt đo cuối 01/11 ⇒ lần kiểm sau cần bộ mới nữa.
- **Bộ đo nhỏ:** chỉ 55 / 176 câu có nhãn "đoạn đúng" ⇒ nhiều thí nghiệm ra "chưa rõ" — nghĩa là *chưa chứng minh được*, không phải *đã chứng minh bằng nhau*.
- **Gần như chưa có so sánh nào đo lại trên kho hiện tại:** phần lớn kết luận "giữ" của Phase 8 đo trên kho / cấu hình cũ. **Model sinh chưa từng được so có chấm điểm** (giữ `gpt-6-luna` theo quyết định
  của bạn 24/10).
- Không lưu câu hỏi người dùng ⇒ mọi số đo trên câu tự viết / Golden, chưa có câu hỏi thật.
- Lệnh kiểm Golden báo **1 lỗi đã biết** (1 câu khác kho chỉ ở chữ hoa / thường — không làm sai điểm; bạn chọn giữ nguyên 01/11).

**Vận hành**

- Log một file, không xoay vòng; log dùng chung cho test và server. Bộ test không có key OpenAI vẫn báo vài lỗi "bình thường" ⇒ chưa có một lệnh kiểm sạch. Kho không có Git (sửa bằng sao lưu tay + so
  khác). Mã đoạn dạng `<file>#<số>` dồn số khi thêm / xoá đoạn giữa file. Bộ chia đoạn còn giới hạn 256 token của một model đã bỏ.

Chi tiết từng dòng (số đo, nguồn, hướng xử lý) và mọi phương án đã thử: báo cáo khâu (`BAO_CAO_*.md`) và [`BAO_CAO_SO_SANH_PHUONG_AN.md`](BAO_CAO_SO_SANH_PHUONG_AN.md).

**Việc kế tiếp (03/11):** Phase 9 theo spec bản 9 — B0 nền ✓ (02/11), B1 định tuyến ✓, B2 tìm thêm ✓ (03/11) ⇒ **B3 + B3b** ✓ merge 03/11 tối (câu dặn hẹp + giao diện nhiều lượt + nhớ hội thoại bật) ⇒ B4 hỏi lại ⇒ B5 lịch trình ⇒ B6 tra web ⇒ B7 so với RAG cũ; đóng code ~20/12/2026. Tốc độ chữ đầu (câu về Huế 3,50 / 5,33 s, vượt sàn 3 / 5 s): A đề xuất tối ưu sớm, sau B3b.
Lịch sử thứ tự cũ (30/10–01/11, đã xong):
1. ~~Hiện chữ dần (streaming)~~ — **xong, chạy từ 01/11** (merge `a80e12d`).
2. **Đóng gói Phase 1–8 — xong, Phase 8 bạn đóng 14:29 01/11/2026:** lượt đo cuối cùng một commit (Golden 176 + lượt lặp cùng ngày, bộ an toàn 32, câu theo ngày, 22 câu qua API, **bộ kín mới 40 câu**) — **xong 01/11, mọi sàn đạt** (`report_agent/2026-10-31_streaming_spec/do_cuoi_implementation.md`; bộ kín cho thấy số dev lạc quan: Đủ 4,18 ↔ 4,58); B0 xong 01/11 (bạn giữ 10 đoạn); báo cáo so sánh phương án (đã đăng 01/11, thêm phần mới khi xong); bảng giới hạn (mục này).
3. ~~Giao diện mới~~ — **xong 02/11** (merge `ed8e6e8`). Từ nhận xét B0 (đề xuất A, chờ bạn): `[n]` chen trong câu khó đọc ⇒ đổi cách hiển thị nguồn.
4. Phase 9 — **đang làm** (B0, B1 xong): mở bằng nghiên cứu rộng rồi mới thử nghiệm; gồm **hội thoại nhiều lượt / nhớ lịch sử** và **câu cần nhiều nguồn** (agent tách câu con). Từ nhận xét B0 (đề xuất A, chờ bạn): câu dự trù chi phí theo mức ⇒ để trợ lý hỏi lại người dùng.

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
- Spec streaming: `docs/superpowers/specs/2026-10-31-streaming-design.md` bản 5 `00fb57ee01b2` (User duyệt 01/11); code vào `main` merge `a80e12d` (01/11); tổng hợp
  `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`.
