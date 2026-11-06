# Báo cáo cho bạn: Sinh câu trả lời, API và giao diện (Phase 6, cải tiến ở Phase 8)

**Cập nhật lần cuối: 21:33 06/11/2026 — bản 38: sửa lỗi lịch trình (B171) vào `main` với cờ lịch trình **tắt** (merge `dbb4004`) — người dùng chưa thấy đổi.** Trước: **21:03 06/11/2026 — bản 37: thời tiết B5b vào `main` với cờ **tắt** (merge `db77f32`) — người dùng chưa thấy đổi; chờ bạn quyết bật.** Trước: **12:15 06/11/2026 — bản 36: lịch trình B5 chấm bằng 2 agent ⇒ bạn thấy câu đo không tự nhiên ⇒ gác, làm bộ câu mới; sửa lỗi lịch trình + thời tiết trên nhánh (chưa vào chatbot).** Trước: **21:15 05/11/2026 — bản 35: **tra web bật** (câu kho không có ⇒ mục "Từ web (chưa kiểm)").** Trước: **21:10 05/11/2026 — bản 34: tra web B6 vào `main` cờ tắt (đạt luật ghi trước; bật = bạn quyết).** Trước: **21:00 05/11/2026 — bản 33: thử tắt ghi đệm OpenAI **âm** (lượt tìm thêm đang đọc lại đệm, tắt đi đắt hơn) — giữ như cũ.** Trước: **14:20 05/11/2026 — bản 32: B5c tính tiền **âm cả vòng 2** (câu miễn vé trẻ nhỏ mất điều kiện) ⇒ dừng, lưu nhánh; câu chi phí giữ như cũ.** Trước: 13:55 05/11/2026 — bản 31: **B5c tính tiền bằng code — âm lần 1** (phép tính đúng 8 / 8, nhưng 1 câu giá vé biểu diễn mất giá + 1 câu an toàn thiếu cảnh báo) ⇒ đang thử vòng 2 (chỉ đưa công cụ khi câu có dấu hiệu chi phí). Người dùng chưa thấy đổi.** Trước: 13:22 05/11/2026 — bản 30: **bật tốc độ #6** (viết câu trả lời song song với bước định tuyến; bạn duyệt; merge + bật trên `main`): chữ đầu câu về Huế nhanh hơn ~1,4 s; câu khẩn cấp / ngoài phạm vi không đổi chữ.** Trước: 13:02 05/11/2026 — bản 29: **B5 lịch trình vào `main` với cờ tắt** (merge `d66f6a3`) — mọi sàn máy đếm đạt (đã thấy + kín + hồi quy + an toàn); **chờ bạn chấm 5 lịch kín (Q3)** rồi mới bật; người dùng hiện chưa thấy đổi.** Trước: 10:23 05/11/2026 — bản 28: trợ lý **hỏi lại người dùng** (B4) thử hai vòng — **âm cả hai** (vòng 1: câu chi phí tự ghi dòng "Tổng"; vòng 2 chỉ câu lịch trình: thiếu cảnh báo an toàn ở 2 câu nhiều hơn bản đang chạy) ⇒ **người dùng không thấy đổi**; code vào `main` với cờ **tắt** (merge `b019aab`) để B5 dùng lại thẻ hỏi lại, lần này **code tự quyết hỏi** khi thiếu số ngày.** Trước: 20:38 04/11/2026 — bản 27: thử tắt suy luận ở bước định tuyến để chữ đầu nhanh hơn — **âm, không áp dụng** (2 câu an toàn về Huế bị xếp nhầm ngoài phạm vi).** Trước: 20:32 04/11/2026 — bản 26: câu khẩn cấp soạn sẵn đổi dòng mở để phủ cả người **vừa** gặp chuyện (bạn chọn PA1; merge `4e3cb4e`).** Trước: 20:54 03/11/2026 — bản 25: sửa an toàn định tuyến khẩn cấp (merge `e3cdb96`): câu "vừa bị cướp / giật / trộm, cần báo công an" nay ra câu khẩn cấp 113 (trước đi trợ lý thường và bị từ chối).** Trước: 20:34 03/11/2026 — bản 24: nút 👍 / 👎 dưới mỗi câu trả lời (chỉ lưu đánh giá, không lưu chữ) + 3 nút gợi ý dưới câu ngoài phạm vi (merge `6817897`, bạn chọn).** Trước: 19:28 03/11/2026 — bản 23: Phase 9 B3b — **nhớ hội thoại bật** (merge `9e2ecd9`): chỉ nhớ câu hỏi + câu dặn "nhận định chỉ từ đoạn nói đúng đối tượng"; lỗi mượn nguồn đối tượng khác hết trên bộ mới (6 / 6 từ chối đúng).** Trước: 18:31 03/11/2026 — bản 22: Phase 9 B3 vào chatbot (merge `a3dabba`) với **nhớ hội thoại TẮT**: câu dặn hẹp (không tự thêm lời khuyên an toàn không có nguồn) chạy cho mọi câu; giao diện nhiều lượt (Bản 1 — Huế hiện đại, số nguồn đánh lại 1, 2, 3…, nút "Cuộc trò chuyện mới"); nhớ chưa bật vì 1 lượt kín mượn nguồn đối tượng khác — đang sửa (B3b).** Trước: 11:39 03/11/2026 — bản 21: Phase 9 B2 vào chatbot (merge `00d670e`): trợ lý tự gọi tìm thêm trong kho ≤ 2 lần; câu nhiều nguồn đủ ý +1,17; 1 câu an toàn sai mới (thêm lời khuyên chung) — sửa ở B3.** Trước: 09:17 03/11/2026 — bản 20: Phase 9 B1 vào chatbot (merge `f01c032`): model phân loại câu hỏi trước (trò chuyện / hỏi về Huế / ngoài phạm vi / khẩn cấp), câu khẩn cấp ra câu soạn sẵn có số 113 / 114 / 115 / 112, dòng nhắc "thông tin có thể đã thay đổi"; chữ đầu tiên chậm hơn ~2 s.** Trước: 19:48 02/11/2026 — bản 19: Phase 9 B0 vào chatbot (merge `1c10111`): một lõi `backend/llm/assistant.py`, công cụ `tim_kho`, log ghi thêm tuyến + USD mỗi câu và mỗi lần gọi model; câu trả lời người dùng thấy không đổi (chuỗi gửi model giống từng byte).** Trước: 10:35 02/11/2026 — bản 18: giao diện web làm lại (React + Vite + Tailwind, merge `ed8e6e8`; review cả nhánh đạt).** Trước: 14:33 01/11/2026 — bản 17: B0 (bạn giữ 10 đoạn), Phase 8 bạn đóng 14:29 01/11/2026.** Trước: 12:51 01/11/2026 — bản 16: streaming vào chatbot; tốc độ tới chữ đầu tiên đạt; công thức tiền giá đủ.** Trước: 11:07 01/11/2026 — bản 15: streaming đã duyệt spec, bước 1 / 4 (gom lõi chung) xong trên nhánh; sửa số tốc độ qua API (chưa đạt p95 5 s); sửa câu "mọi thí nghiệm có luật ghi trước".** Bản 14: 17:10 31/10/2026.
Các bản trước: xem `git log` file này. Người viết: sub-agent của A (bản 14) · Review: agent con ngữ cảnh mới (31/10). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (đúng hiện trạng 05/11/2026)

- **Khâu này làm gì:** chatbot Huế trả lời câu hỏi trên toàn bộ kho (món ăn, di tích, lễ hội, nghệ thuật, du lịch) qua một API và một trang
  web đơn giản. Mỗi ý có trích dẫn `[1]`, `[2]`… trỏ tới đoạn nguồn thật; thiếu thông tin thì trả đúng một câu từ chối cố định, không bịa.
- **Đang chạy cách nào:** chuẩn hóa chữ câu hỏi (NFC — gộp dấu tiếng Việt về một dạng) → **từ 03/11 (B1):** `gpt-6-luna` phân loại câu hỏi (một lần gọi ngắn ~1,5 s): chào hỏi ⇒ đáp ngắn không tìm kho;
  ngoài phạm vi ⇒ câu soạn sẵn; khẩn cấp ⇒ câu soạn sẵn 5 dòng (113 công an · 114 cháy, cứu nạn · 115 cấp cứu · 112 thiên tai — model không viết lời khuyên); hỏi về Huế ⇒ tìm đoạn (từ 03/11 trưa, B2: model được gọi tìm thêm ≤ 2 lần bằng câu tự viết, đoạn mới đánh số tiếp) → lấy tối đa **10 đoạn** nguyên vẹn vừa
  ngân sách 16.384 token → `gpt-6-luna` (OpenAI, để mức suy luận mặc định) viết câu trả lời chỉ từ các đoạn đó → backend kiểm từng `[n]` →
  trả câu trả lời + nguồn. Mỗi lần hỏi, API ghi **một dòng số đo** (token, thời gian từng khâu, **tiền USD của câu và của từng lần gọi model, tuyến, công cụ đã chạy** — từ Phase 9 B0; không ghi nội dung câu hỏi / trả lời).
  **Từ B3 (03/11 tối, merge `a3dabba`):** câu dặn trả lời thêm một ý hẹp — không tự thêm lời khuyên / lưu ý an toàn mà nguồn không nêu, giữ lời khuyên có trong nguồn. **nhớ hội thoại BẬT từ B3b (merge `9e2ecd9`)**: server giữ **câu hỏi** của 3 lượt gần nhất (không giữ câu trả lời — `nho_cau_tra_loi: false`), cookie 30 phút; câu dặn thêm cho đường có lịch sử: mọi nhận định và trích dẫn chỉ từ đoạn nói đúng đối tượng được hỏi.
  Trang web: **làm lại 02/11** (merge `ed8e6e8`) bằng React + Vite + Tailwind, chỉ trang hỏi đáp + khung nguồn bên cạnh; **từ 03/11 tối (B3) dạng nhiều lượt theo Bản 1 — Huế hiện đại**: các lượt hỏi–đáp xếp nối nhau, số nguồn hiển thị đánh lại 1..k theo thứ tự xuất hiện (tầng máy vẫn số gốc), bấm số ở lượt cũ mở nguồn của lượt đó, nút "Cuộc trò chuyện mới", 5 chủ đề gợi ý; nguồn hiện bằng số nhỏ bấm được (tầng máy vẫn `[n]`); nhãn "Trợ lý AI… có thể sai"; lỗi luôn báo bằng tiếng Việt; máy chạy cần build một lần `cd frontend && npm ci && npm run build`. Một lượt hỏi – đáp, **chữ hiện dần (streaming) từ 01/11** qua `POST /api/chat/stream`: kiểm trích dẫn ở cuối, hỏng thì rút lại, lỗi / đứt thì xoá + "Thử lại"; `/api/chat` (JSON một lần) vẫn giữ.
- **Đo được trên bản đang chạy** (10 đoạn, kho đã sửa hai đợt; 176 câu Golden; 30/10):
  - từ chối nhầm câu có trong kho **12 / 158**; **0** câu ngoài kho bị trả lời; câu sai điều kiện (giờ, vé, cảnh báo) trên bộ 32 câu an toàn: **0**;
  - lỗi trích dẫn (người dùng nhận lỗi 500): **0 / 489** lần sinh, đếm trên mọi lượt đo đã lưu;
  - so với chatbot đầu Phase 8.2 (5 đoạn) trên 33 câu kín: điểm Đủ **+0,82**, Đúng **+0,70** (thang 1–5), 0 câu tụt (28/10);
  - **tới chữ trả lời đầu tiên, sau B1 (03/11, 10 câu tự viết, đường stream):** cả 10 trung vị **3,05 s** / p95 **5,64 s**; câu về Huế **3,57 / 6,57 s**; trò chuyện 2,63 / 2,82 s; ngoài phạm vi 1,82 / 1,93 s; khẩn cấp 1,63 s — mẫu nhỏ;
    trước B1 (01/11, 38 câu, trình duyệt): 1,23 / 2,61 s; phần thêm là lần gọi phân loại (~1,5 s, chủ yếu chờ mạng / OpenAI — model chỉ suy luận ~14 token);
    **sau B2 (03/11 trưa, cùng 10 câu):** cả 10 3,33 / 5,20 s, câu về Huế 3,50 / 5,33 s;
  - **B2 tìm thêm (03/11):** 18 câu nhiều nguồn đủ ý **+1,17** [+0,44; +2,00]; Golden đủ ý / đúng +0,22; từ chối nhầm 12 ⇒ 4–6 / 158; bộ an toàn: **1 câu sai điều kiện mới thật** (thêm lời khuyên chung không có trong nguồn) — luật cho ≤ 2 cả Phase, đã dùng 1; tiền ≈ 0,00031 USD / câu;
  - tiền: **≈ 0,00025 USD / câu** theo giá đủ (lượt đo 01/11: TB 0,000247); công cụ đo **tính giá đủ từ 01/11** (trước ghi thiếu ≈ 20 %, số USD cũ trong báo cáo đếm giá phẳng).
  - Điểm Đúng / Đủ / Trúng ý trung bình tuyệt đối chỉ có ở mốc cũ 7B (5 đoạn, 24/10): **4,43 / 4,28 / 4,45**; các lượt đo sau báo chênh theo cặp, không báo lại điểm tuyệt đối.
- **So với yêu cầu** (bạn chốt 28/10, đổi thước 31/10 D2: sàn trung vị ≤ 3 s / p95 ≤ 5 s **tới chữ trả lời đầu tiên trên trình duyệt**; ≤ 0,0005 USD / câu): **từ B1 (03/11) vượt sàn** ở câu về Huế (3,57 / 6,57 s) —
  spec Phase 9 để tốc độ **chỉ theo dõi** (chất lượng trước), bạn để mặc định 03/11: merge, xét tối ưu sau B2; trước B1 (01/11): đạt cả sàn lẫn mục tiêu 1,5 / 3 s; tiền **đạt** (định tuyến thêm ~0,000075 USD / câu). Bạn chọn giữ sàn 3 / 5 s (không nâng — mức dư nhỏ, hôm đo model gần như không suy luận trước) và giữ cách hiện chữ dần dù lợi chỉ ~0,44 s.
  Trước streaming (cả câu qua API, 27/10): 3,1 / 6,0 s — chưa đạt.
- **Giới hạn chính:** từ chối nhầm vẫn là chỗ mất điểm lớn nhất (gốc ở khâu tìm: đoạn có đáp án không vào 10 đoạn); câu hỏi theo ngày tương đối
  ("tối nay", "tuần này") bị từ chối dù kho có lịch (6 / 14 câu) — an toàn nhưng chưa trả lời được ⇒ Phase 9; bảng giá và câu tổng hợp nhiều nguồn còn yếu;
  10 đoạn được chọn bằng người chấm Claude; mốc người B0 (01/11) chỉ tham khảo — phần lớn cặp như nhau, 3 cặp bản 5 đoạn từ chối nhầm còn bản 10 trả lời được ⇒ bạn giữ 10.
- **Tối ưu tốc độ (04/11):** thí nghiệm #1 (tắt suy luận khi định tuyến) **âm** — nhanh hơn ~0,2–0,35 s nhưng phạm sàn an toàn ⇒ bỏ (mục 04/11). Đang viết plan #6: viết câu trả lời song song với định tuyến, xếp sai thì bỏ.
- **Hỏi lại người dùng (B4, 04–05/11) — chưa bật:** trợ lý được một công cụ "hỏi lại" (thẻ có nút chọn số ngày, số người…) khi câu lịch trình / chi phí thiếu thông tin. Hai vòng đo đều **âm** theo luật ghi trước (chi tiết mục 4, 05/11) ⇒ cờ `hoi_lai: false`, người dùng thấy **y như trước** (kiểm 228 câu: chuỗi gửi model giống từng byte). Code + thẻ giao diện ở `main` (`b019aab`) để **B5 (lịch trình)** dùng lại theo cách mới: **code** tự bật thẻ hỏi khi thiếu số ngày, không thêm lời dặn vào mọi câu. Câu chi phí ⇒ bậc mới **B5c: code tính tiền** (model không tự nhân / cộng).
- **Lịch trình (B5) — chưa bật, đang làm lại phần đo (06/11):** 2 agent chấm độc lập 5 lịch kín (khớp nhau 15 / 15 ô): đúng luật xếp 5 / 5, có nguồn 5 / 5, **hợp người đi cùng 3 / 5** (cần ≥ 4 / 5). Nhưng bạn đọc phiếu thấy **câu hỏi kín không tự nhiên** ⇒ kết quả này **không dùng để quyết**. Đang: bộ câu mới theo cách người thật hỏi (E tra 20 lượt hỏi thật trên diễn đàn + biểu mẫu TRIPO; bạn duyệt giọng 8 câu mẫu 06/11) + sửa 2 loại lỗi code đã thấy — **vào `main` 21:33 06/11/2026** (merge `dbb4004`, cờ vẫn tắt): sáng ưu tiên điểm hợp sở thích, câu lấp đúng sự thật; xin buổi tối mà luật không xếp ⇒ dòng "Buổi tối: để trống — <lý do>" + kiểm cuối bắt lời nói ngược; model từ chối cả lịch ⇒ code dựng lịch tối thiểu từ khung. Review C 2 vòng đạt; Q1 228 / 228 giống byte; cổng sau merge đạt (360 test, server thật 2 câu, 0 câu hỏi trong log). Giới hạn đã biết: lời model kiểu "buổi tối có thể nghỉ / đi bộ ngắn" còn lọt kiểm — để bộ kín v2 đo. Bạn đang duyệt lại bộ kín v2 (K2–K5 E viết ngắn lại theo ý bạn).
- **Thời tiết (B5b) — vào `main` cờ tắt (21:03 06/11/2026, merge `db77f32`):** công cụ `thoi_tiet` (Open-Meteo; số do code dựng, ghi giờ số liệu; ngoài 7 ngày ⇒ câu cố định; bão / lũ ⇒ NCHMF + 112). Cờ `thoi_tiet: false` ⇒ người dùng thấy y như trước. Review cả nhánh đạt sau sửa 4 lỗi; cổng sau merge: 196 test đạt, build giao diện, server thật 1 câu trong kho + 1 câu ngoài kho đúng, log 2 dòng số đo, 0 câu hỏi trong log (≈ 0,0006 USD).
- **Bạn cần quyết (tối 06/11):** duyệt lại 5 câu kín v2 (mục "Vòng 2" trong `data/phase_9/b5_v2/duyet_tu_nhien_user.md`, bàn trực tiếp với E); có bật thời tiết không.

## 2. Hoạt động thế nào (bản đang chạy)

```text
trang web / POST /api/chat/stream (từ 01/11) hoặc /api/chat {"query": "..."}   (1–500 ký tự; hai route dùng chung lõi backend/llm/assistant.py — tên cũ grounded_answer.py tới B0)
 → chuẩn hóa NFC → tìm đoạn (dense + từ khóa, trộn RRF) → lấy tối đa 10 đoạn nguyên vẹn, vừa ngân sách 16.384 token
 → gpt-6-luna viết câu trả lời, chỉ dùng các đoạn đó, đặt [n] sau mỗi ý (hoặc trả đúng câu từ chối)
 → backend đổi [Nguồn n] về [n], kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources}; lỗi có mã rõ ràng: 422 câu hỏi không hợp lệ · 409 chỉ mục lệch kho · 503 tìm kiếm tạm lỗi · 500 trích dẫn hỏng
 → ghi một dòng chat_metrics (backend/logs/application.log)
Stream: lỗi trước khi model viết = JSON như trên; sau đó sự kiện status → delta… → (kiểm trích dẫn) sources → done, hoặc error{after_text} → done
```

- Khi khởi động, hệ thống so "dấu vân tay" kho với hồ sơ chỉ mục; kho đổi mà chưa dựng lại chỉ mục thì từ chối chạy.
- Bấm `[n]` trên trang web cuộn tới thẻ nguồn ghi tiêu đề, mục và đoạn trích nguyên văn.
- Code: `backend/api/routes/chat.py` (API; kiểm câu hỏi `:36–38`, route `:60`, kiểm trích dẫn `:177–188`), `backend/retrieval/full_corpus_context.py`
  (chọn đoạn theo ngân sách), `backend/config/settings.yaml:48` (model), `:53` (ngân sách), `:56` (`max_context_documents: 10`),
  `backend/llm/full_corpus_prompt.py:7–16` (prompt), `backend/llm/generator_openai_full_corpus.py` (gọi model), `backend/llm/citations.py:11` (mẫu bắt
  `[n]` và `[Nguồn n]`), `frontend/src/` (trang web React; bản build `frontend/dist/` phục vụ ở `backend/api/app.py:159–166`).

Tự hỏi chatbot (không bắt buộc): bật Docker Desktop, `docker compose up -d qdrant`; từ `backend/` chạy
`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`; mở `http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (phí rất nhỏ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu có đủ bằng chứng → trả lời kèm `[n]` | **Đã xử lý, đóng gói** | mốc 7B (5 đoạn) 4,43 / 4,28 / 4,45; câu kín 28/10 (10 đoạn) Đủ +0,82, Đúng +0,70 so với 5 đoạn |
| Câu ngoài kho → từ chối, không bịa | **Đã xử lý, đóng gói** | 30/10: 0 câu ngoài kho bị trả lời (Golden; bộ an toàn 0 / 4); câu từ chối cố định `full_corpus_prompt.py:3–5,14–15` |
| Kiểm `[n]` trỏ đúng nguồn, lỗi thì trả mã rõ ràng | **Đã xử lý, đóng gói** | nhận cả `[Nguồn n]`, đổi về `[n]` (từ 25/10); bản đang chạy 0 / 489 lần sinh lỗi; dạng lỗi còn thấy ở bản cũ chỉ là "không gắn `[n]` nào"; `citations.py:11`, `chat.py:177–188` |
| Trang web bấm số nguồn tới thẻ nguồn | **Đã xử lý, đóng gói** (giao diện mới 02/11) | số chỉ thành link sau khi nguồn về; bắt cả `[n]` lẫn `[Nguồn n]`; `frontend/src/markdown.js`, `App.jsx`; `api/app.py:159–166` |
| Kho lệch chỉ mục → từ chối khởi động | **Đã xử lý, đóng gói** | API báo 409 "cần lập chỉ mục lại"; `retrieval/full_corpus.py:383–385`; test `test_api_chat.py` |
| Qdrant / model tìm kiếm lỗi → báo lỗi tạm | **Đã xử lý, đóng gói** | 503 `retrieval_unavailable` (`chat.py:96–119`); test `test_startup_model_missing.py` (bạn chạy `!`) |
| Đưa 10 đoạn thay vì 5 + chuẩn hóa NFC | **Đã xử lý, đóng gói** (từ 28/10) — B0 01/11: bạn giữ 10 (tham khảo) | 8.1: Đủ +0,26 (thử) / +0,27 (kiểm); câu kín +0,82; trung vị / p95 2,19 / 4,90 s. Đổi ngược về 5: sửa `settings.yaml:56` **và** chốt kiểm ở `core/settings_loader.py:75` (đang ép đúng 10) |
| Câu có một vế có bằng chứng, vế kia thiếu | **Đã thử, chưa áp dụng** | prompt bắt từ chối cả câu (`full_corpus_prompt.py:14`). Hai lần thử "trả lời phần có căn cứ" đều trả lời câu ngoài kho ⇒ gác; luật kiểm sau sinh không cứu được (mục 4) |
| Đoạn chứa đáp án nằm ngoài các đoạn đưa model | **Xử lý một phần** | mọi câu từ chối nhầm đo ở 8.1 đều thiếu ít nhất một đoạn đúng — gốc ở khâu tìm; 10 đoạn giảm gần một nửa; phần còn lại: `BAO_CAO_TIM_KIEM.md` |
| Mức suy luận của model | **Đã thử, chưa áp dụng** | giữ mặc định (không gửi tham số: `generator_openai_full_corpus.py:98–99,120`); `none` kém hơn (trả lời vòng câu lẽ ra từ chối), lợi tiền chỉ 3–6 % (mục 4) |
| Câu trả lời quá gọn, bỏ chi tiết có trong nguồn | **Chưa thực hiện** | 26/10: 9 / 88 câu mất điểm vì bỏ chi tiết; thử "nêu đủ chi tiết" không chạy được (chỉ 6 câu đổi được, quá ít để kết luận) |
| Câu trả lời ghi sai con số (giá, giờ, năm) | **Xử lý một phần** (đo được, chưa có rào chặn) | 27/10, 10 đoạn: 0 / 68 câu có số bị thấy sai; chưa đo sai về chữ (tên, sự kiện) |
| Kiểm bằng code sau khi sinh để chặn "trả lời vòng" | **Đã thử, chưa áp dụng** | 7 / 10 câu bị cờ là câu có ích ⇒ gác |
| Để model chọn 10 / 30 đoạn trước khi trả lời | **Đã thử, chưa áp dụng** | trung bình tốt lên nhưng 5 câu tụt > 4 cho phép; chờ ~6,5 s, tiền ×3,8 (mục 4) |
| Xếp đoạn gom theo tài liệu; 2 luật cũ của prompt Phase 6; "một nguồn thì gán nguồn đó" | **Đã thử, chưa áp dụng** | 8.1: không khác (mục 4) |
| Câu tổng hợp nhiều nguồn | **Xử lý một phần** | lúc đóng Phase 6 chỉ dùng 1 nguồn; 8.1: lợi của 10 đoạn nằm nhiều ở câu nhiều nguồn / so sánh; chưa có phép đo riêng "tổng hợp đúng" |
| Câu hỏi giá vé + miễn giảm (bảng giá) | **Đã thử, chưa áp dụng** | không tìm ra dòng bảng giá; 8.1 thử gộp dòng bảng khi chia đoạn: không khác (`BAO_CAO_TIM_KIEM.md`); chưa đo lại riêng ở 10 đoạn |
| Tách câu hỏi hai ý | **Chưa thực hiện** | Phase 8 không làm; giả thuyết xếp "cân nhắc cho Phase 9" (`reports/phase_8_candidate_hypotheses_2026_10_24.md:68`) |
| Câu hỏi theo ngày tương đối ("tối nay", "tháng sau") | **Xử lý một phần** (an toàn; chưa trả lời được) — Phase 9 | 30/10: 0 câu đoán ngày rồi nói sai; 6 / 14 câu có trong kho bị từ chối (4 câu có lịch ngay trong đoạn model đọc). Prompt không có ngày hôm nay (`full_corpus_prompt.py:7–16`) |
| Hiện chữ dần (streaming) | **Đã xử lý, đóng gói** (01/11, merge `a80e12d`) — 4 bước + review cả nhánh đạt; S4 đạt sàn + mục tiêu | trước: bước 1 / 4 (01/11 sáng) — bạn duyệt spec 01/11 (`00fb57ee01b2`); bước 1 gom lõi chung: review đạt, hành vi không đổi; bước 2–4 (luồng chữ, giao diện, đo) đang làm (mục 6) |
| Câu khẩn cấp "vừa bị cướp / giật / trộm / hành hung, cần báo công an" | **Đã xử lý, đóng gói** (03/11 tối, B143 merge `e3cdb96`) | trước: câu tự viết loại này đi trợ lý thường (2 / 2 lượt) ⇒ "không tìm thấy thông tin"; sửa một dòng định nghĩa `khan_cap` trong lời dặn định tuyến; 24 câu khẩn cấp × 2 lượt đúng hết, 6 câu mới cùng loại đúng hết, câu thường dễ nhầm 0, Golden 176 đổi tuyến 0; review C159 `ready` |
| Người dùng đánh giá câu trả lời (👍 / 👎) | **Đã xử lý, đóng gói** (03/11 tối, B142 merge `6817897`) | `POST /api/feedback` {mã lượt, up / down}; mỗi lần bấm một dòng log `chat_feedback` (mã lượt ngẫu nhiên, tuyến, kết quả, số nguồn, đánh giá) — không chữ câu hỏi / trả lời, không mã cuộc; đổi ý được; cổng: 200 / 422 đúng, log 0 nội dung. Chưa nối được với dòng số đo cùng lượt |
| Câu ngoài phạm vi kèm gợi ý | **Đã xử lý, đóng gói** (03/11 tối, B142) | 3 nút câu gợi ý cố định có trong kho (chỉ giao diện, không đổi model / lời dặn); bạn chọn web chỉ cho câu **về Huế** (B6) |
| Hội thoại nhiều lượt — giao diện | **Đã xử lý, đóng gói** (03/11 tối, B3 merge `a3dabba`) | Bản 1 bạn chọn; Playwright server thật: CSP 0 vi phạm, 0 request ra ngoài, điện thoại không cuộn ngang; review C147 `ready` |
| Hội thoại nhiều lượt — trợ lý nhớ câu trước | **Đã xử lý, đóng gói** (03/11 tối, B3b merge `9e2ecd9`; chỉ nhớ câu hỏi) — trước đó cờ tắt vì sàn kín phạm | đã thấy: nhớ tên 6 / 6, hỏi tiếp đủ ý +0,65; kín: nhớ tên cộng 10 / 10, hỏi tiếp +0,60 (không ngược chiều), 0 đảo cảnh báo; **1 / 2 lượt ngoài kho kín bị trả lời bằng đoạn nguồn của đối tượng khác** ⇒ sàn phạm ⇒ không bật (luật ghi trước); bạn chọn sửa lời dặn, đo trên bộ chuỗi mới |
| Không tự thêm lời khuyên an toàn thiếu nguồn | **Đã xử lý, đóng gói** (03/11 tối, B3) | câu dặn hẹp; 208 câu: từ chối nhầm 4, Đủ / Đúng không tụt, 0 câu sai điều kiện; câu an toàn lỗi của B2 hết lỗi |
| Giao diện web mới (React + Vite + Tailwind) | **Đã xử lý, đóng gói** (02/11, merge `ed8e6e8`) | 19 yêu cầu (17 của streaming + nguồn số nhỏ + nhãn AI); CSP không nới, 0 gói Radix / shadcn (2 / 5 linh kiện vi phạm CSP khi dò); B tự kiểm + C review độc lập (build lại từ lockfile, server thật, ca dò khác cách): đạt; `report_agent/2026-11-02_giao_dien_moi_code/` |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (mới ở trên)

Mỗi dòng: thử gì · kết quả · giữ / bỏ vì sao · hồ sơ. Thí nghiệm chọn / bỏ phương án có luật ghi trước khi chạy và người khác kiểm lại; các lượt **đo hiện trạng** (tốc độ, giá, token) chỉ đo — không có luật giữ / bỏ ghi trước.

### 06/11/2026 — lịch trình B5: chấm bằng agent, câu đo không tự nhiên ⇒ làm lại bộ câu; sửa lỗi lịch trình + thời tiết (trên nhánh)
- **Chấm 5 lịch kín (bạn chọn 10:03 06/11/2026: agent chấm trước, bạn đọc chỗ lệch):** 2 sub-agent Claude ngữ cảnh mới, chưa từng làm B5, chấm riêng không xem của nhau — khớp **15 / 15 ô**. Đúng luật xếp 5 / 5 · có nguồn 5 / 5 · **hợp người đi cùng 3 / 5**: một lịch bỏ qua sở thích / kiểu đi người dùng nói (lỗi ở code xếp + bảng điểm thiếu thời lượng; độ chắc cao), một lịch lời trả lời nói "được" với buổi tối trong khi code không xếp buổi tối vì có trẻ nhỏ (lỗi model + code thiếu câu báo; độ chắc vừa). 0 USD (quota Claude). Lý do chi tiết: `data/phase_9/b5/kin/cham_agent_{1,2}.md` (private).
- **Bạn đọc phiếu: câu hỏi kín không tự nhiên** ⇒ theo luật "câu đo phải giống người thật hỏi" (24/10), kết quả trên không dùng để quyết bật / không bật. Bài học: người viết bộ, người review plan, 2 người chấm đều không bắt lỗi này ⇒ phiên sau thêm bước bạn duyệt độ tự nhiên **trước** khi khoá bộ kín.
- **Làm lại bộ câu (E19):** Huế TRIPO vòng 4 (biểu mẫu lập kế hoạch, tab lưu trú / ăn uống / dịch vụ, bộ lọc, bản đồ) + 20 lượt hỏi thật trên diễn đàn VOZ 2023–2026 (E tự mở kiểm 3 chủ đề) ⇒ người thật kể hoàn cảnh trước, ràng buộc rải trong câu, hỏi kèm đi lại / chỗ ở / giờ tới, có ý né, viết tắt "3N2Đ" / "ko". Phát hiện: công cụ lịch trình chỉ hiểu 4 loại (số ngày, đi cùng ai, kiểu đi, sở thích) ⇒ bộ mới đo cả việc chatbot **nói thật phần không làm được**. Bạn duyệt giọng 8 câu mẫu (06/11); A chốt: bộ kín không có câu hai lượt, ≥ 2 / 5 câu có phần ngoài lịch. Hồ sơ `report_agent/2026-11-06_b5_cau_tu_nhien/e19_implementation.md`.
- **Sửa lỗi lịch trình bằng code (B171, nhánh `p9-b5-sua`, chưa vào chatbot):** (1) buổi sáng ưu tiên điểm hợp sở thích, câu giải thích "lấp chỗ trống" nói đúng sự thật; (2) người dùng xin buổi tối mà luật không xếp ⇒ code tự nối câu lý do + kiểm cuối bắt lời nói ngược. Review (C): kiểm (2) **bắt nhầm** 5 / 10 câu đúng ("Buổi tối: tự do") ⇒ đang sửa; thêm: câu "tối có … được không?" với người lớn tuổi ⇒ model từ chối cả lịch ⇒ A chọn code dựng lời lịch tối thiểu khi model từ chối. Tiền ≈ 0,018 USD.
- **Tối 06/11 — B171 (21:33 06/11/2026):** merge `dbb4004` vào `main`, cờ `lich_trinh` tắt; C review vòng 2 ready (`report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` §8); tiền B171 ≈ 0,029 / 0,04 USD.
- **Tối 06/11 (21:03 06/11/2026):** B5b merge `db77f32` vào `main`, cờ tắt (không cần đưa lại lên `main` mới — `main` chỉ đổi tài liệu); cổng ổn định đạt (mục 1).
- **Thời tiết B5b:** review cả nhánh (C) bắt 1 lỗi lớn — 4 / 20 lượt câu dự báo hiện câu từ chối rồi ngay sau là bảng số ⇒ code thay bằng câu dẫn cố định (đo lại 0 / 4) — + 3 lỗi nhỏ, sửa xong, kiểm lại đạt. Tiền B5b ≈ 0,054 / 0,07 USD. Hồ sơ `report_agent/2026-11-02_phase_9_code/b168_b5b_implementation.md` §12–§13, `b168_b5b_review.md`.

### 05/11/2026 tối — Phase 9 B6: tra web khi kho không có — ĐẠT luật ghi trước, merge `7ff8e5a`, **BẬT 21:15 05/11/2026** (bạn duyệt)
- **Làm gì:** khi kho trả câu "không đủ thông tin" cho câu về Huế, code tra web một lần (Serper) ⇒ model viết mục **"Từ web (chưa kiểm)"** tách khỏi câu trả lời kho, có mã [w n] trỏ tới link; code kiểm: link phải nằm trong sổ kết quả tra, số tiền phải có trong đoạn trích, câu lưu trú 0 số tiền, câu thời gian thực (cúp điện, tuần này…) 0 chữ số / ngày giờ, câu thiên tai (lũ, lụt, bão, áp thấp…) ⇒ **không** chữ do model viết, chỉ câu cố định "xem nguồn chính thức / gọi 112" + link.
- **Đo:** bộ đã thấy ×2 — vòng đầu phạm 1 sàn (2 câu khẳng định thông tin chưa xác minh: lịch cúp điện, mức lũ) ⇒ vòng chỉnh 1 bằng **code** (luật thiên tai / thời gian thực) ⇒ đạt; kín ×2 đạt (0 / 7 khẳng định, 7 / 7 trả lời được); hồi quy: 0 câu từ chối nhầm thêm, 0 / 11 mục web nói "an toàn / được phép" sai; server thật + trình duyệt đạt. Review E 2 vòng bắt 2 lỗi code (link HTML thô lọt qua; thiếu "lụt" / "áp thấp") — đã sửa trước merge.
- **Giới hạn:** mục web tới sau **~13 s** (trung vị, kín) vì chờ kho từ chối ⇒ tra ⇒ viết; ~0,0018 USD / câu đường web; địa chỉ / số điện thoại trong mục web chưa kiểm là có trong đoạn trích; thêm "đang" vào luật thời gian thực sẽ chặn nhầm 1 câu đúng ⇒ chưa thêm. Tiền B6 ≈ 0,19 / 0,22 USD. **Bật 21:15 05/11/2026**; cổng sau khi bật (server thật, 3 câu tự viết): câu quán ăn kho không có ⇒ mục web 1 nguồn, 18,2 s, 0,0018 USD; câu "đang lụt" ⇒ câu cố định thiên tai, 9,1 s; câu giờ mở cửa kho có ⇒ không tra web, 3,1 s; log 0 chữ câu hỏi, 0 khoá. Hồ sơ `report_agent/2026-11-02_phase_9_code/b165_b6_implementation.md`, `b165_review.md`.

### 05/11/2026 tối — thử tắt ghi đệm của OpenAI (C202) — ÂM, giữ như cũ
- **Thử gì:** tham số `prompt_cache_options` chế độ `explicit` (không điểm ngắt) ⇒ OpenAI không ghi đệm, khỏi trả giá ghi đệm 1,25× cho phần đọc vào. Ý từ đo 02/11 (khi đó 0 lần đọc đệm). Tiêu chí ghi trước: 0 ghi đệm, cờ tắt giống byte, tiền / câu giảm, chữ đầu không chậm hơn.
- **Kết quả:** tắt ghi đệm được, nhưng tiền / câu **tăng** (0,000315 so với 0,000305 USD). Lý do (C đếm lại 78 lượt đã lưu, 0 USD): từ khi trợ lý tự tìm thêm (B2), **45 % lượt gọi model ≥ 2 lần** và **mọi lần gọi sau đều đọc lại đệm** của lần đầu ⇒ 81 % phần đọc vào tính giá đọc đệm rẻ. Ghi đệm lần đầu là cái giá để các lần sau rẻ; tắt đi đắt hơn ~21 % phần vào. Định tuyến vốn không ghi đệm (lời nhắc < 1.024 token).
- **Giữ như hiện nay.** Xét lại nếu tắt tìm thêm. Tiền thử 0,0031 USD. Hồ sơ `report_agent/2026-11-02_phase_9_code/c202_ghi_dem.md`.

### 05/11/2026 — Phase 9 B5c: tính tiền bằng code — ÂM hai vòng, dừng (nhánh lưu bằng tag `hoso/p9-b5c`, không vào `main`)
- **Làm gì:** câu chi phí ("2 người đi 3 ngày hết bao nhiêu", "vé Đại Nội cho 2 người lớn 1 trẻ em") ⇒ công cụ `tinh_tien`: **code** đọc bảng dự toán (tính cho một người) + bảng vé lẻ Quần thể trong kho, tự hỏi số người / ngày khi thiếu, tự nhân / cộng theo luật nhóm của kho, nối bảng có `[n]` + ngày nguồn; model chỉ viết lời, không nhận con số nào; code kiểm mọi số tiền trong chữ model.
- **Đạt:** phép tính khớp đáp án C tính tay **8 / 8**; câu ngoài phạm vi dữ liệu ra câu cố định 4 / 4; chuỗi gõ số người không bị hỏi lần hai; 62 câu thường không bị gọi nhầm công cụ, không rút lại nhầm.
- **Phạm (luật ghi trước ⇒ âm):** (1) câu giá vé một suất biểu diễn (giá có trong kho nhưng **ngoài** bảng vé lẻ) ⇒ luật "không tự viết số tiền" làm model bỏ luôn giá có nguồn ⇒ thiếu ý (lỗi thiết kế); (2) bộ an toàn: 1 câu về miễn giảm vé thiếu cảnh báo nhiều hơn bản đang chạy (1 / 3 ↔ 0 / 3; câu này không gọi công cụ — chỉ việc có thêm công cụ làm model tìm kho khác đi, giống B4b). Tiền ≈ 0,079 USD.
- **Vòng 2 (A quyết, thí nghiệm mới, không sửa kết quả cũ):** sửa (1) — ngoài bảng thì nêu giá có trong tài liệu kèm `[n]`; và **chỉ đưa công cụ khi code thấy dấu hiệu chi phí** ⇒ câu khác (gồm câu an toàn) gửi model **y hệt** bản đang chạy — chặn đúng kiểu lỗi (2). **Vòng 2 (14:20 05/11/2026) — âm:** câu không dấu hiệu chi phí gửi model y hệt bản đang chạy (21 / 32 câu an toàn) ⇒ sạch; Golden 30 sạch (câu giá vé biểu diễn nay nêu giá kho). Nhưng câu **miễn vé trẻ nhỏ khi nghe ca Huế** (có chữ "vé" nên được đưa công cụ) bỏ điều kiện chiều cao / ngồi cùng người lớn **3 / 3** lần ↔ bản đang chạy 1 / 3 ⇒ âm. Tổng tiền B5c ≈ 0,128 USD. **Dừng B5c** (lần thử thứ 3 thì dừng theo luật tự soi); hướng cho lần sau: **code nối dòng điều kiện miễn giảm** của bảng vé vào kết quả công cụ (điều kiện bắt buộc ⇒ code). Câu chi phí hiện vẫn đi như bản đang chạy (liệt kê giá có nguồn). Bài học chung (B4b, B5c): **mỗi công cụ thêm vào mọi câu đều làm đổi cách model trả lời câu an toàn** ⇒ công cụ nào chỉ cần cho một loại câu thì code bật theo loại câu (như B5b thời tiết). Hồ sơ: `report_agent/2026-11-02_phase_9_code/b162_b5c_implementation.md`.

### 05/11/2026 — Tốc độ #6: viết câu trả lời song song với định tuyến — ĐẠT, bật trên `main` (13:22 05/11/2026)
- **Đổi gì:** trước, định tuyến (~1,5 s) xong mới tìm kho + viết câu trả lời; nay đường stream chạy phần "trợ lý Huế" **cùng lúc** với định tuyến; định tuyến ra khẩn cấp / ngoài phạm vi / trò chuyện ⇒ bỏ phần đã chạy, trả đúng câu như trước.
- **Đo (04/11, luật ghi trước):** chữ đầu câu về Huế nhanh hơn trung vị **1,37 s** [0,34; 2,14] (15 / 20 cặp nhanh hơn; hôm đo provider chậm: p50 5,36 ⇒ 3,53 s, p95 8,69 ⇒ 7,72 s — vẫn trên sàn 3 / 5 s); an toàn 90 lượt 0 vi phạm, khẩn cấp không đổi (1,83 ↔ 1,80 s); 228 / 228 chuỗi gửi model giống byte cả cờ tắt lẫn bật. Review (B) 2 vòng đạt — vòng 1 bắt lỗi mất trường nút bấm khi đưa lên bản có B4b / B5, đã sửa + test.
- **Đánh đổi:** câu không về Huế tốn thêm một lần viết bị bỏ (~+0,00023 USD; cả câu ≈ 0,0003 ≤ 0,0005); câu khẩn cấp / ngoài phạm vi cũng gửi kèm đoạn kho tới OpenAI. Cổng `main` (13:22 05/11/2026): câu về Huế chữ đầu 2,75 s · câu khẩn cấp ra đúng câu soạn sẵn · câu ngoài phạm vi đúng · log không có chữ câu hỏi. Hồ sơ: `report_agent/2026-11-02_phase_9_code/c172_toc_do_song_song.md`, `c172_review.md`.

### 05/11/2026 — Phase 9 B5: gợi ý lịch trình — đạt sàn máy, code vào cờ tắt (merge `d66f6a3`), chờ bạn chấm
- **Làm gì:** câu "lên lịch Huế 2 ngày…" ⇒ trợ lý gọi công cụ `lich_trinh`: **code** chọn điểm từ bảng 28 điểm bạn duyệt (cột tên khác), xếp theo buổi (≤ 2 cụm / ngày, buổi cấm theo người đi cùng), gắn giờ có nguồn, dựng link Google Maps; thiếu số ngày ⇒ **code** bật thẻ hỏi lại (không lời dặn thêm); "Trả lời luôn" ⇒ tạm 1 ngày + dòng giả định; model chỉ viết lời theo khung; **code kiểm cuối** (điểm ngoài khung, giờ ngoài tập, giá, trích dẫn) — sai ⇒ rút lại + "Thử lại"; giao diện hiện dòng tiến độ **chỉ bước code đã làm** + nút "Sửa".
- **Đo:** đã thấy 13 câu gọi công cụ 10 / 10, kiểm cuối 0 lỗi, ngoài Huế từ chối 3 / 3; kín 5 câu gọi công cụ 5 / 5, nội dung 0 điểm ngoài khung (1 / 5 bị rút lại **nhầm** — bộ kiểm tưởng tên điểm nhắc trong câu lịch sử là điểm thêm ⇒ sửa B5.1 bằng câu tự viết; review bắt 5 kẽ hở của bản sửa ⇒ sửa tiếp, thử thêm 5 kẽ hở mới đều bắt); hồi quy Golden 30 sạch (theo dõi: 1 câu từ chối mới), an toàn 32 thủ tục kiểm lại **đạt** (bản mới ≤ bản đang chạy ở mọi câu). Theo dõi: qua server 1 / 4 câu lịch bị rút lại (model ghi sai số nguồn — kiểm cuối bắt đúng). Tiền ≈ 0,104 USD. Review cả nhánh (C) 2 vòng đạt.
- **Cập nhật 06/11:** bộ kín này bị gác (câu không tự nhiên) — xem mục 06/11 ở trên. Hồ sơ: `report_agent/2026-11-02_phase_9_code/b160_b5_implementation.md`, `b160_review.md`.

### 04–05/11/2026 — Phase 9 B4: trợ lý hỏi lại người dùng — ÂM hai vòng, code vào với cờ tắt (merge `b019aab`)
- **Thử gì:** câu lịch trình / chi phí thiếu số ngày, số người ⇒ trợ lý gọi công cụ `hoi_lai` ⇒ giao diện hiện thẻ có nút chọn ⇒ người dùng bấm ⇒ câu đủ ý đi đường trả lời thường. Câu chi phí theo **Cách A** (bạn chọn 03/11): liệt kê giá có nguồn, không cộng tổng — dặn bằng lời trong lời dặn.
- **Vòng 1 (khoá 3, 04–05/11) — âm:** hỏi lại đúng đạt (đã thấy 8 / 10, kín 4 / 5), câu đủ không bị hỏi thừa, 60 câu thường không bị hỏi sai chỗ, 30 câu Golden không ảnh hưởng. **Phạm:** (a) 1 / 2 câu chi phí kín, sau khi chọn "2 người", trợ lý **tự ghi dòng "Tổng"** bằng số tự tính (phép ×2 khớp luật kho — bảng tính cho một người — nhưng luật đo cấm con số tổng); (b) người dùng **gõ** "3 người, đi 3 ngày" thay vì bấm ⇒ bị hỏi lại lần nữa (4 / 4 lần). Kết luận: lời dặn không giữ được model khỏi tự tính.
- **Vòng 2 (B4b, bạn chọn "Tách — giữ lịch trình", khoá `990825e`) — âm:** chỉ hỏi lại câu lịch trình. Đạt: lịch trình đã thấy 4 / 5, kín 3 / 3; câu chi phí không bị hỏi 0 / 12; câu đủ 0 / 10; 60 câu thường 0 / 60; Golden 30 sạch; an toàn các lượt ghép 0 ý sai giá / giờ / điều kiện. **Phạm:** bộ an toàn 32 câu — **2 câu mới bị chấm "thiếu cảnh báo"** (ngưỡng ≤ 1) ⇒ thủ tục kiểm lại ghi trước (mỗi câu 3 lần bản mới ↔ 3 lần bản đang chạy, 2 judge chấm mù): bản mới thiếu nhiều hơn ở cả hai câu (2 / 3 ↔ 1 / 3; 3 / 3 ↔ 2 / 3) ⇒ âm. Giới hạn: mỗi bên chỉ 3 lần, chênh 1 lần mỗi câu, bản đang chạy cũng thiếu 3 / 6 ⇒ không chứng minh tệ hơn, cũng không loại được. **Giả thuyết** (chưa chứng minh): đoạn dặn "khi nào hỏi lại" thêm vào lời dặn **mọi** câu làm model lơ phần cảnh báo (1 câu: bản mới tìm thêm 3 / 3 lần, câu trả lời ngắn hơn).
- **Bạn chọn (05/11): "Merge cờ tắt + code tự hỏi"** ⇒ code vào `main` với `hoi_lai: false` (cổng: 228 câu giống byte, test 64 đạt, câu thật trong / ngoài kho đúng, log không chứa câu hỏi); **B5** dùng lại thẻ + nút, nhưng **code** quyết hỏi khi công cụ lịch trình thiếu số ngày (khung AI FDE: trường bắt buộc ⇒ code). Câu chi phí ⇒ **B5c tính tiền bằng code**.
- Tiền: vòng 1 ≈ 0,205 · vòng 2 ≈ 0,088 USD. Hồ sơ: `report_agent/2026-11-02_phase_9_code/b144_b4_implementation.md` (§2e–§2g), review nhánh `b157_b4b_review.md`; plan `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 8.

### 04/11/2026 — thử tắt suy luận ở bước định tuyến (thí nghiệm tốc độ #1) — ÂM, không áp dụng
- **Thử gì:** bước định tuyến (chọn trò chuyện / về Huế / ngoài phạm vi / khẩn cấp) chạy `gpt-6-luna` với mức suy luận "none" thay mặc định. Luật ghi trước: không câu khẩn cấp, không câu an toàn nào đổi tuyến sai; đạt mới đo chữ đầu.
- **Kết quả:** 123 câu × 2 lượt + 50 lượt có lịch sử: khẩn cấp đúng hết, nhưng **2 câu an toàn về Huế bị xếp "ngoài phạm vi"** (một câu 2 / 2 lượt, một câu 1 / 2; bản hiện tại đúng 2 / 2) ⇒ phạm sàn ⇒ bỏ, chữ đầu không đo (NOT RUN). Theo dõi: định tuyến trung vị 1,7 ⇒ 1,3–1,5 s, tiền / lần −16 %. Giả thuyết (chưa chứng minh): phần suy luận giúp phân biệt câu an toàn về Huế với câu ngoài phạm vi. Tiền 0,057 USD. Review B155 đạt. `report_agent/2026-11-02_phase_9_code/c156_toc_do_dinh_tuyen.md`; code giữ bằng tag `hoso/p9-toc-do-1`.

### 04/11/2026 — dòng mở câu khẩn cấp soạn sẵn (merge `4e3cb4e`)
- **Đổi gì:** chỉ dòng mở của câu khẩn cấp thành "Nếu bạn hoặc người bên cạnh đang gặp nguy hiểm **hoặc vừa gặp chuyện (bị cướp, tai nạn, cháy, ốm nặng)**, hãy gọi ngay số khẩn cấp (miễn phí):"; 4 dòng còn lại (4 số, "nói rõ bạn đang ở đâu", "không gọi hộ được", dòng tiếng Anh) giữ nguyên. Bạn chọn PA1 trong 3 phương án chữ (C162). Không đổi định tuyến.
- **Kiểm:** test khoá đủ 5 dòng (12 / 12 đạt); định tuyến không đổi ⇒ dùng lại đo hôm nay (mốc thí nghiệm tốc độ: 24 / 24 câu khẩn cấp + 6 / 6 lượt có lịch sử vào đúng nhánh khẩn cấp cả 2 lượt); cổng `main` (A): câu tự viết "vừa bị giật túi xách" ⇒ chữ mới; câu trong kho ⇒ trả lời có nguồn; câu ngoài kho ⇒ từ chối (≈ 0,001 USD). Review C168 đạt (`report_agent/2026-11-02_phase_9_code/b154_review.md`).

### 03/11/2026 tối — sửa an toàn định tuyến khẩn cấp (merge `e3cdb96`)
- **Phát hiện** khi đo mốc cho thí nghiệm tốc độ (luật dừng "mốc phạm sàn khẩn cấp"): câu tự viết "vừa bị giật túi xách có hộ chiếu, báo công an ở đâu" đi trợ lý thường ⇒ câu từ chối, không có số 113. Bộ 10 câu khẩn cấp tự viết (02/11) chưa từng vào bộ đo định tuyến ⇒ lỗ hổng có từ B1 (sáng 03/11). Ca cùng loại trên lời dặn cũ chỉ đúng 4 / 6 ⇒ lỗi theo loại, không riêng một câu.
- **Sửa:** chỉ dòng định nghĩa `khan_cap` trong lời dặn định tuyến — thêm "vừa bị cướp / giật / trộm / móc túi / hành hung / đe doạ, cần báo công an — dù việc đã xảy ra"; không luật từ khoá, không đổi câu soạn sẵn. Luật ghi trước đạt hết (mục 3). Cổng `main` (A): câu đó ⇒ câu khẩn cấp; câu thường ⇒ trả lời có nguồn. ≈ 0,042 USD. `report_agent/2026-11-02_phase_9_code/b143_khan_cap_implementation.md`, `b143_review.md`.
- **Còn mở:** ~~câu soạn sẵn chưa sát người vừa bị giật đồ~~ (đã sửa 04/11, mục trên); định tuyến quá 10 s ⇒ đi trợ lý thường — nếu rơi vào câu khẩn cấp sẽ mất câu soạn sẵn (hiếm: 1 / 246 lần, câu ngoài phạm vi).

### 03/11/2026 tối — nút 👍 / 👎 + gợi ý dưới câu ngoài phạm vi (merge `6817897`)
- Từ nghiên cứu sản phẩm thật (Tokyo EDO có nút báo sai; Huế TRIPO không có). Bạn chọn "chỉ lưu đánh giá". B code, C review 0 finding (mã lượt ngẫu nhiên riêng, không lộ mã cuộc; lượt lỗi / rút lại không có mã), cổng trên `main` (A) đạt. Tiền ≈ 0,002 USD. `report_agent/2026-11-02_phase_9_code/b142_phan_hoi_implementation.md`.

### 03/11/2026 tối — Phase 9 B3b: nhớ hội thoại bật (merge `9e2ecd9`)
- **Vòng 1** (câu dặn "nhận định chỉ từ đoạn nói đúng đối tượng", nhớ cả câu trả lời): đã thấy đạt mọi sàn nhưng **hỏi tiếp +0,50 [−0,15; +1,20] — không đạt luật** (cận dưới phải > 0) ⇒ đường kết quả âm ghi trước:
- **Vòng (a) — chỉ nhớ câu hỏi** + câu dặn: đã thấy nhớ tên 6 / 6, hỏi tiếp **+0,80 [+0,25; +1,50]**, 0 câu ngoài kho bị trả lời, 0 đảo cảnh báo ⇒ đạt; **bộ chuỗi mới** (C viết, B không xem; 12 chuỗi nhắm đúng lỗi): bên có nhớ **từ chối đúng 6 / 6** lượt bẫy (bên không lịch sử dính 3 / 6), từ chối nhầm 0 / 19 ↔ 5 / 19 ⇒ **bật** (bạn chọn "đạt ⇒ bật"). Review C154 `ready`. Tiền B3 + B3b ≈ 0,47 USD (trần 0,50).
- **Giới hạn:** bộ mới chỉ 6 lượt bẫy; chưa thấy ca "bác tiền đề bằng đúng nguồn"; không nhớ câu trả lời ⇒ câu "ý thứ hai bạn vừa nói…" chưa hỗ trợ; cookie hết 30 phút thì âm thầm bắt đầu cuộc mới. `report_agent/2026-11-02_phase_9_code/b138_b3b_implementation.md`.

### 03/11/2026 tối — Phase 9 B3 vào chatbot (merge `a3dabba`), nhớ hội thoại tắt (đã bật ở B3b)
- **Phần kín** (C chạy 15 chuỗi, 3 bên, 0,032 USD): nhớ tên 4 / 4 (cộng 10 / 10, sàn ≥ 9); hỏi tiếp có nhớ ↔ câu gõ không lịch sử +0,60 [0,00; +1,40] (luật: không ngược chiều — đạt); câu điều kiện 0 đảo cảnh báo; đổi chủ đề tụt 0. **Câu ngoài kho: 1 / 2 lượt bên có nhớ bị trả lời** — chạy lại có lưu ngữ cảnh: bot mượn đoạn của **đối tượng khác** để trả lời câu hỏi tiếp mang tiền đề sai (hai bên không lịch sử từ chối đúng) ⇒ sàn phạm ⇒ **cờ nhớ không bật** (luật ghi trước). Lúc đầu nghi nhãn bộ đo sai — kiểm có ngữ cảnh bác bỏ.
- **Bạn chọn (18:31 03/11/2026):** merge code + giao diện với nhớ tắt; vòng sửa **B3b** — C viết bộ chuỗi mới nhắm đúng loại lỗi (B không xem), B thêm một câu vào lời dặn đường có lịch sử ("mỗi ý về một đối tượng phải từ đoạn nói đúng đối tượng đó"), đo lại; đạt ⇒ bật. Trần B3 0,40 ⇒ 0,50 USD.
- **Giao diện nhiều lượt + cổng:** Playwright server thật đạt (CSP 0, ngoài 0); cổng có nhớ bật trên bản sao cấu hình (cookie thật, "cuộc mới" xoá nhớ, log 0 nội dung) đạt; câu gợi ý "tháng này…" đổi thành câu không cần ngày hôm nay (A quyết). Cổng sau merge trên `main` (A): `/` 200, `/health` 5 / 5, 1 câu trong kho (6 nguồn) + 1 câu ngoài phạm vi đúng, log +2 dòng, 0 chữ câu hỏi. Tiền B3 ≈ 0,30 USD.

### 03/11/2026 chiều — Phase 9 B3 (nhớ hội thoại) thử trên nhánh `p9-b3`
- **Câu dặn mới chống "thêm lời khuyên chung"** (sửa lỗi an toàn của B2): bản 1 "chỉ nêu điều có trong bằng chứng…" sửa được lỗi nhưng **trượt** sàn từ chối nhầm (4 ⇒ 7) + đọc chữ thấy mở "Có." rồi nói ngược, bỏ lời khuyên có nguồn ⇒ **bản hẹp** (chỉ chặn lời khuyên / lưu ý an toàn không có nguồn, giữ lời khuyên có nguồn) **đạt cả 5 luật**: từ chối nhầm 4, Đủ / Đúng không tụt, 0 câu sai điều kiện, câu an toàn của B2 hết lỗi ⇒ **giữ** (≈ 0,19 USD cả hai vòng).
- **Nhớ hội thoại** (đo 25 chuỗi đã thấy): nhớ tên 6 / 6; câu hỏi tiếp có nhớ ↔ gửi câu gõ không lịch sử: đủ ý **+0,65** [+0,15; +1,25]; 0 câu ngoài kho bị trả lời; đổi chủ đề 0 câu tụt. Còn: phần kín, cổng ổn định, giao diện nhiều lượt (Bản 1 bạn chọn) ⇒ mới bật.
  `report_agent/2026-11-02_phase_9_code/b136_b3_implementation.md`.

### 03/11/2026 trưa — Phase 9 B2 vào chatbot (merge `00d670e`)
- **B2a — model viết lại câu tìm đầu** (3 cách, 2 lượt × 61 câu, ≈ 0,069 USD): không cách nào qua luật ⇒ **không giữ**, tìm bằng câu gốc (`BAO_CAO_TIM_KIEM.md` mục 4).
- **B2b — trợ lý tự gọi `tim_kho` thêm ≤ 2 lần** (luật ghi trước; nhiễu đo bằng 2 lượt của chính đường công cụ): đủ ý câu nhiều nguồn +1,17, Golden không tụt quá nhiễu, 0 câu ngoài kho bị trả lời ⇒ **giữ**;
  1 câu an toàn sai mới thật (2 / 3 lần sinh lại, bản cũ 0 / 3) — bạn chọn giữ + sửa lời dặn ở B3 (11:16 03/11). Cổng ổn định: 2 ca ngắt thật (giữa vòng công cụ / giữa chữ), log đúng. Review C137 + C141 `ready`. Tiền B2 ≈ 0,255 USD.
  `report_agent/2026-11-02_phase_9_code/b134_b2_implementation.md`, `b134_review.md`.

### 03/11/2026 — Phase 9 B1 vào chatbot (merge `f01c032`)
- **B131 hoàn tất + review C134** (`ready`, 0 blocker / 0 major): bộ an toàn 32 câu — lần gọi trả lời giống từng byte bản trước ⇒ dùng lại kết quả 01/11; sửa log khi người dùng ngắt giữa chừng (đóng lõi trước rồi mới ghi, +1 test); bật mặc định định tuyến + dòng nhắc;
  cổng ổn định 2 ca ngắt thật; chữ đầu 10 câu (mục 1). 0,0029 + 0,0006 USD · **giữ** · `b129_b1_implementation.md` §4b, `b129_review.md` "Vòng cuối".
- Lưu ý đo (C134 m-3): `evaluation generate` không truyền `--flags` nay chạy theo `settings.yaml` (có định tuyến) ⇒ muốn đo đường RAG 1–8 thuần phải truyền `--flags` rỗng.

### 02/11/2026 tối — Phase 9 (B0 vào chatbot; B1 đo xong phần lớn — vào chatbot 03/11)
- **B0** (merge `1c10111`): một lõi `assistant.py`, `tim_kho`, log USD + ms mỗi lần gọi model · câu trả lời không đổi (giống byte) · **giữ** · `report_agent/2026-11-02_phase_9_code/b127_*`.
- **Câu khẩn cấp, chatbot hiện tại** (10 câu tự viết, 0,0025 USD): 10 / 10 chỉ từ chối, không chỉ số gọi · **bạn: lỗi** ⇒ B1 trả câu soạn sẵn 113 / 114 / 115 / 112 (số kiểm nguồn chính thức) · `c122_khan_cap_buoc0.md`.
- **B1, nhánh `p9-b1`** (luật ghi trước, phần kín do C giữ; ≈ 0,142 USD): **định tuyến** 4 tuyến đúng 253 / 253 đã thấy + 20 / 20 kín ⇒ **bật**; dòng nhắc "có thể đã thay đổi" (vé / nơi / lễ hội) ⇒ **bật**;
  **luật từ khoá khẩn cấp**: đã thấy 14 / 14, kín **0 / 8 + chặn nhầm 2 / 8** ⇒ **bỏ** (câu khẩn cấp vẫn ra câu soạn sẵn nhờ định tuyến bắt 10 / 10 kín; thêm 1 lần gọi phân loại);
  **dòng ngày hôm nay**: từ chối nhầm 5,0 ⇒ 4,5 (cần giảm ≥ 3) ⇒ **bỏ** (gốc ở tầng tìm / model, như 30/10). Hồi quy 176 câu: sàn đạt, từ chối nhầm 12 = 12; Đủ 6 câu tụt (ngưỡng 5) nhưng lần gọi trả lời giống byte
  bản cũ ⇒ coi là nhiễu, dùng lại số cũ (spec §4). **Tốc độ:** định tuyến thêm ~1,7 s (p95 2,7 s) mỗi câu ⇒ chữ đầu có thể vượt 5 s — chỉ theo dõi (chất lượng trước). Merge 03/11.
  `b129_b1_implementation.md`, `b129_review.md`, `c131_kin_b1.md`.

### 30/10/2026
- **Câu hỏi theo ngày tương đối** (15 câu tự viết + 11 câu bộ an toàn, 2 người chấm Claude không biết ngày chạy; 0,0037 USD): 0 câu tự đoán ngày rồi nói chắc,
  0 câu tính sai thứ / âm lịch; nhưng 6 / 14 câu có trong kho bị từ chối, cùng thông tin hỏi không kèm ngày thì trả lời đúng. **Bạn quyết (14:44):** không sửa prompt ở
  Phase 8; Phase 9 thêm công cụ "hôm nay là ngày nào", bộ câu này làm mốc. `report_agent/2026-10-27_phan_ton_phase_cu/ngay_hien_tai_implementation.md`.
- **Đếm lại lỗi trích dẫn** trên mọi lượt đo đã lưu (0 USD): bản đang chạy 0 / 489 lần sinh; bản 5 đoạn cũ 2 / 528. Lỗi còn lại chỉ là câu không gắn `[n]` nào, chỉ
  biết khi câu đã viết xong ⇒ căn cứ cho streaming "hiện chữ trước, kiểm cuối". `report_agent/2026-10-27_phan_ton_phase_cu/TONG_HOP.md` §8.2.
- **Giá đủ của `gpt-6-luna` (đo 30/10, trước khi có tìm thêm):** mỗi câu bị tính giá **ghi đệm** cho gần hết phần đọc vào, không được giảm giá đọc đệm ⇒ tiền thật ≈ 0,00025 USD / câu (từ Phase 9 B2, các lần gọi sau trong cùng câu đọc lại đệm — xem thử 05/11 tối ở mục 4), công cụ đo ghi
  thiếu ≈ 20 %; mọi số USD cũ trong báo cáo này đếm theo giá phẳng. Sửa công thức: việc đóng gói Phase 1–8. `Project_Status.md` §5 (30/10 15:07).

### 28/10/2026
- **Đưa 10 đoạn + chuẩn hóa NFC vào chatbot** (merge `510e1a8`): bạn chọn đưa vào theo người chấm Claude, đọc cặp mù làm sau. Kiểm trên `main`: 51 test đạt, kết quả
  tìm 158 câu giống từng byte, câu gõ dấu tách rời cho đúng ngữ cảnh như câu thường, chạy thật 2 câu đạt (≈ 0,0004 USD). **Giữ.**
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_merge_implementation.md`.
- **Đo thử "chữ đầu tiên" nếu có streaming** (đo trong script, chưa trên trình duyệt; 7–8 câu tự viết, phần lớn trả lời dài): chữ đầu hiện sớm hơn lúc xong câu
  ~**1,9 s** (trung vị); tới chữ đầu p50 2,4 / p95 4,8 s, so với chờ đủ câu 4,6 / 7,6 s ⇒ lý do làm streaming.
  `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_implementation.md`.

### 27/10/2026
- **Thời gian chờ thật qua API** (22 câu tự viết, bản 5 đoạn lúc đó): trung vị 3,3 s / p95 5,7 s tuần tự; ~98 % là lúc model viết (tăng theo số chữ model viết ra: ≈ 11,5 ms mỗi token, tương quan 0,97 — `report_agent/2026-10-26_cai_tien_tung_khau/c58_latency_theo_khau.md`), tìm ~40 ms, dựng ngữ cảnh ~2 ms;
  thời gian viết đi theo số token viết ra. Số này của cấu hình cũ — số hiện hành ở mục 1. `report_agent/2026-10-26_cai_tien_tung_khau/b65_latency_dau_cuoi.md`, `c58_latency_theo_khau.md`.
- **API ghi số đo mỗi câu** (bạn duyệt; merge `5100b90`): một dòng log mỗi lần hỏi, không chứa câu hỏi. **Giữ.** `report_agent/2026-10-26_cai_tien_tung_khau/c59_log_token_implementation.md`.
- **Trả lời ngay, không suy luận** (mốc 10 đoạn): một câu lẽ ra phải từ chối bị trả lời vòng ⇒ phạm sàn, dừng ở 24 câu (0,0049 USD); lợi nhỏ (token viết ra ~0,72×,
  tiền ~0,94–0,97×). **Bỏ.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md`.
- **Model chọn 10 / 30 đoạn rồi mới trả lời** (120 câu thử): đủ ý +0,22, đúng +0,25 trung bình, từ chối nhầm 7 → 2 / 88, nhưng **5 câu đủ ý tụt** > 4 cho phép ⇒ kém
  hơn theo luật; chờ p50 6,5 / p95 9,1 s, tiền ×3,8 (0,0749 USD). **Bỏ.** `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_m_answer_review.md`.
- **Sai số liệu trong câu trả lời** (đo hiện trạng, 0 USD): 0 / 68 câu có số bị thấy sai (máy nghi 4 câu, đều là phép tính đúng). Không cần rào chặn lúc này.
  `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md`.
- **Luật kiểm sau sinh chặn "trả lời vòng"** (0 USD): không tách được câu lạc đề với câu trả lời một phần có ích (7 / 10 cờ là câu có ích). **Bỏ.**
  `report_agent/2026-10-26_cai_tien_tung_khau/c51_kiem_sau_sinh_kha_thi.md`.
- Bạn chốt đợt cải tiến từng khâu: không cách nào vào chatbot. Tổng hợp: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.

### 26/10/2026
- **Phân loại lỗi** (88 câu, mốc 10 đoạn): 10 câu kém đều thiếu thông tin trong 10 đoạn; model không bịa. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md`.
- **Trả lời phần có căn cứ, chữ prompt siết hơn:** vẫn trả lời 1 / 12 câu ngoài kho ⇒ dừng ngay bước đầu (0,0027 USD). **Bỏ.**
- **Nêu đủ chi tiết:** không chạy (chỉ 6 câu đổi được). **Thước kiểm số liệu có trong nguồn:** chỉ dùng chọn câu đọc lại. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r3_plan.md`, `phase_8_2_r4_implementation.md`.

### 25/10/2026
- **API báo đúng loại lỗi** (rà code): một module bị nạp hai lần làm Qdrant lỗi ra 500 thay 503, kho đổi ra 503 thay 409 ⇒ sửa về một cách import, chạy mọi lệnh từ
  `backend/`. **PASS.** `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`.
- **Lỗi trích dẫn `[Nguồn n]`:** model đôi khi trích đúng nhãn ngữ cảnh "[Nguồn n]", bộ kiểm chỉ hiểu "[n]" ⇒ người dùng nhận 500. Sửa: nhận cả hai dạng, đổi về `[n]`.
  Trên 1.600 câu đã sinh: lỗi 69 → 14, 0 câu đạt bị đổi. **PASS, giữ.** Số "lỗi trích dẫn" trước ngày này đếm theo bộ kiểm cũ.
- **Phase 8.1 — thử 5 cách trả lời** (120 câu thử, chấm mù bằng Claude, so theo cặp; "tốt hơn" phải xác nhận trên 56 câu kiểm; 0,157 USD):

  | Cách | Điểm Đủ (thử) | Rào chắn | Kết luận |
  |---|---|---|---|
  | **10 đoạn ngữ cảnh** | **+0,26** | đạt; tiền ×1,5 | **tốt hơn**, bộ kiểm +0,27 ⇒ **đã đưa vào 28/10** |
  | Xếp 5 đoạn gom theo tài liệu | −0,02 | đạt | không khác ⇒ bỏ |
  | Prompt "trả lời phần có căn cứ" | +0,11 | trả lời 2 câu ngoài kho | kém hơn ⇒ bỏ |
  | Prompt thêm 2 luật cũ | 0,00 | đạt | không khác ⇒ bỏ |
  | Mức suy luận `none` / `low` / `high` | +0,14 / +0,02 / +0,02 | `none`, `low`: lỗi trích dẫn tăng (đếm theo bộ kiểm cũ) | không dùng; `none` thử lại 27/10 vẫn kém |
  | "Một nguồn thì gán nguồn đó" | — | — | 0 câu đổi ⇒ bỏ |

  Đính chính: chẩn đoán 7B "4 / 22 câu có đủ bằng chứng mà vẫn từ chối" (theo từ khóa) — đo bằng đoạn đúng thì **0 câu**. `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md`.

### 24/10/2026 và trước
- **Phase 7B — mốc 176 câu** (5 đoạn): Đúng / Đủ / Trúng ý 4,43 / 4,28 / 4,45; từ chối đúng 18 / 18 câu ngoài kho; từ chối nhầm 22 / 158; lỗi trích dẫn 4 / 176
  (bộ kiểm cũ); ~0,024 USD. `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`.
- **Dọn code sau Phase 7:** gỡ đường sinh câu trả lời bản món ăn (đã hỏng: gửi `temperature` ⇒ lỗi 400) cùng code / test món ăn; đường toàn kho không đổi.
  `reports/phase_7_cleanup_inventory_2026_10_24.md`.
- **23/10 — đóng Phase 6 trên `gpt-6-luna`:** 5 câu thật, 4 đạt / 1 không (câu giá vé + miễn giảm: không tìm ra bảng giá); câu nhiều nguồn đạt nhưng chỉ dùng 1 nguồn.
- **Đổi model sinh:** Qwen 3.5-9B (OpenRouter) → `gpt-5.4-nano` → `gpt-6-luna` (23/10). Hai model đầu **đã bỏ**.
  `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`.

## 5. Hôm nay còn đúng không

Kiểm với code `main` (`1985a81`) lúc 17:10 31/10/2026 và `session_prompt/Project_Status.md` §4.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| API `POST /api/chat`, trả `{answer, sources}`, câu hỏi 1–500 ký tự | **còn dùng** | `backend/api/routes/chat.py:36–38,48–50,60` |
| Model sinh `gpt-6-luna`, không gửi mức suy luận | **còn dùng** | `settings.yaml:48`; `generator_openai_full_corpus.py:98–99,120` |
| Tối đa 10 đoạn, ngân sách 16.384 token (thay 5 đoạn từ 28/10) | **còn dùng** — B0 01/11: bạn giữ 10 | `settings.yaml:53,56`; `core/settings_loader.py:69–76` |
| Chuẩn hóa NFC câu hỏi trước khi tìm | **còn dùng** (từ 28/10) | `backend/retrieval/full_corpus.py:97–102` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng** | `full_corpus_prompt.py:14` |
| Kiểm trích dẫn nhận cả `[n]` và `[Nguồn n]` | **còn dùng** (từ 25/10) | `citations.py:11–16`; `chat.py:177–188` |
| Ghi `chat_metrics` mỗi câu, không ghi nội dung | **còn dùng** (từ 27/10); **từ B0 02/11 ghi thêm** `route`, `usd`, `n_llm_calls`, `llm_calls`, `tools` (trước đó không ghi USD) | `chat.py:38–45,216`; `generator_openai_full_corpus.py` `CallLog` |
| Câu bị ngắt giữa stream, hoặc `/api/chat` lỗi sau khi model đã trả lời: `usd` ghi rỗng (có tốn tiền thật) | **sửa ở B1** (03/11): log ghi sau khi đóng lõi, có `llm_calls`; lần gọi bị huỷ giữa chừng vẫn không có usage ⇒ `usd` lượt đó hơi thấp hơn thật | `b127_review.md`, `b129_review.md` |
| Trợ lý tự gọi tìm thêm ≤ 2 lần (`tim_them`) | **còn dùng** (từ 03/11 trưa, merge `00d670e`); câu tìm đầu vẫn là câu gốc | `backend/llm/assistant.py` `tool_for_turn`; `settings.yaml` `tim_them` |
| Công cụ hỏi lại `hoi_lai` + thẻ nút | **có code, TẮT** (merge `b019aab` 05/11; B4 âm hai vòng); B5 dùng lại thẻ với cách code tự hỏi | `backend/llm/hoi_lai.py`; `settings.yaml` `hoi_lai: false` |
| Định tuyến 4 tuyến trước khi trả lời; dòng nhắc "có thể đã thay đổi" | **còn dùng** (từ 03/11, merge `f01c032`); luật từ khoá khẩn cấp + dòng ngày hôm nay: code giữ, **tắt** | `backend/llm/assistant.py` `_pick_route`; `settings.yaml` khối `assistant:` |
| Từ chối khởi động khi kho lệch chỉ mục | **còn dùng** | `retrieval/full_corpus.py:383–385` |
| Chỉ mục đang dùng | **còn dùng**: `hue_full_corpus_7a2_e5_small_384`, 8.435 đoạn (dựng lại 05/11 tối), Qdrant cổng 6335 | `Project_Status.md` §4; `settings.yaml:38` |
| `cost_usd` của công cụ đo | **Đã sửa 01/11** — giá đủ (ghi đệm 0,125 · đọc đệm 0,01 · thường 0,10 · ra 0,50 USD / 1M); `chat_metrics` ghi token đệm | `backend/evaluation/full_corpus_eval.py` `cost_usd`; review `b108_cost_usd_review.md` |
| Chẩn đoán 7B "4 / 22 câu đủ bằng chứng vẫn từ chối" | **đã thay** bởi số đo theo đoạn đúng của 8.1: 0 / 22 | `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` |
| "Representation B" (LLM viết thêm ngữ cảnh cho đoạn) | **đã gỡ** 26/10 | commit `c6e130c` |

## 6. Việc còn lại / cần quyết

- **Streaming — xong, chạy từ 01/11** (spec `00fb57ee01b2`, merge `a80e12d`). Giới hạn ghi lại (không sửa ở Phase 8, giao diện sẽ làm lại): một vài lỗi hiếm ngoài SDK chưa huỷ lần gọi model; route stream ghi bản ghi bằng chứng nửa chừng; rút lại / luồng đứt chỉ kiểm bằng phát lại. Yêu cầu cho giao diện mới:
  `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md`; review cả nhánh `streaming_final_branch_review.md`; đo `s4_do_d2_implementation.md`.
- **Hội thoại nhiều lượt:** **dời sang Phase 9** (phần trợ lý / agent — bạn chọn 11:20 01/11/2026); nháp spec giữ làm tư liệu, không làm ở Phase 1–8.
- **Đóng gói Phase 1–8 — xong:** lượt đo cuối mọi sàn đạt; B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp). **Phase 8 bạn đóng 14:29 01/11/2026.**
- **Từ nhận xét B0:** câu dự trù chi phí theo mức ⇒ để trợ lý hỏi lại người dùng (Phase 9 — spec đang viết); `[n]` chen trong câu khó đọc ⇒ **xong ở giao diện mới 02/11** (số nhỏ bấm được, vẫn giữ `[n]` ở tầng kiểm).
- **Giao diện mới — giới hạn:** chỉ làm cho laptop (điện thoại không vỡ, chưa tối ưu); hộp thoại cho Phase 9 phải tự viết (Radix Dialog vi phạm CSP); ca "rút lại" / luồng đứt giữa chừng vẫn kiểm bằng luồng tự dựng.
- **Phase 9 (cập nhật 05/11):** B0–B3b, 👍 / 👎, sửa khẩn cấp xong; **B4 âm hai vòng** (code vào, cờ tắt). Tiếp theo (spec bản 12 bạn duyệt 05/11): **B5 lịch trình** (plan bản 7 duyệt, kèm dòng tiến độ chỉ hiện bước đã chạy thật; code tự hỏi số ngày) ⇒ **B5c tính tiền bằng code** ⇒ sửa lịch nhiều lượt ⇒ B5b thời tiết ⇒ B6 tra web ⇒ B7 so sánh cuối. Thử tốc độ #6 (song song) đạt, chờ bạn quyết bật. Phase 10 (ảnh, giọng nói), 11 (trải nghiệm Huế), 12 (vận hành, deploy AWS): `DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md`.
- **Còn mở, không gấp:** câu trả lời quá gọn (cần thêm câu tự nhiên để đo); bảng giá và câu nhiều nguồn (gốc ở khâu tìm); sai về chữ (tên, sự kiện) chưa có cách đo rẻ.
- Hướng đã gác (chỉ mở lại khi có ý mới đã kiểm trước): trả lời phần có căn cứ; trả lời không suy luận; luật kiểm sau sinh; model chọn 10 / 30 đoạn.

## Phụ lục — hồ sơ kỹ thuật

- **Mã việc ở mục 4:** ngày tương đối = C93 (plan B96); đếm lại trích dẫn = C89; giá đủ = B95; 10 đoạn + NFC = Phase 8.2 B1 (nhánh `p82-b1` `c3d5607`, spec 8.2 §11 "PA3"
  — đưa vào không chờ B0, commit `d922bf7`); đo chữ đầu = probe TTFT; latency 27/10 = B65 / C58; log số đo = C59 / C60 (review B70); không suy luận = **R1**
  (plan sha `8e76e77e0448`, nhánh `p82-r1` `63a472f`); model chọn đoạn = **K3b-m** khâu trả lời (plan bản 3 sha `2a3b22b38ab6`, nhánh `p82-k3b` `a6f609c`, review C54;
  5 câu tụt theo chỉ số T3); sai số liệu = C48; luật kiểm sau sinh = C51; phân loại lỗi = C36; trả lời một phần = **R2** (nhánh `p82-r2`) / H8; nêu đủ chi tiết = **R3**
  (NOT RUN); thước số = **R4**; API báo đúng lỗi = rà code gói 1b (`1e4acd0`); `[Nguồn n]` = gói 1a (`9e6d371`); 8.1 = G2 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md`
  §4, luật ghi trước `phase_8_1_g2_g4_plan.md` §2.1 sha `a4adfc8eedd9`).
- **B0** = lượt bạn đọc cặp câu trả lời mù (mốc người); luật dừng ở spec 8.2 §11 (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`).
- Mã giới hạn: tổng hợp nhiều nguồn = **F1**; bảng giá = **F2**; tách câu hai ý = giả thuyết **H13**.
- Thử 10 đoạn đầu tiên (24/10, 22 câu từ chối nhầm, 10 / 22 hết từ chối, chưa chấm): `reports/phase_8_probe_context_top10_2026_10_24.md`.
- **Lệch tài liệu đã biết (24/10, còn đúng 31/10):**
  - Spec umbrella `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` §1 cho phép "trả phần có căn cứ"; spec Phase 6 và prompt bắt từ chối cả câu.
    Code theo spec Phase 6.
  - `guides/full_corpus_rag.md:500` (đoạn lịch sử) còn ghi "direct `AsyncOpenAI`, không Agent/Runner"; code dùng OpenAI Agents SDK một lượt, không tool — đúng theo
    `docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md`. Không phải lỗi code.
