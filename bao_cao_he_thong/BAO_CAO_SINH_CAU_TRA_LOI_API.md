# Báo cáo cho bạn: Sinh câu trả lời, API và giao diện (Phase 6)

**Cập nhật lần cuối: 09:38 28/10/2026 — bản 12: chatbot đưa tối đa 10 đoạn vào ngữ cảnh (trước 5) + chuẩn hóa chữ câu hỏi (NFC), merge `510e1a8`; bạn chọn
(PA3, 28/10) không chờ đọc cặp mù — chọn bằng judge Claude, chưa có mốc người.** Bản 11 (13:27 27/10/2026): API ghi một dòng số đo cho mỗi câu hỏi (token, thời gian từng khâu; không ghi nội dung); đo thời gian chờ thật qua API:
trung vị ~3,3 s, câu chậm ~5,7–6,2 s, gần hết là thời gian model viết; câu trả lời không đổi. Bản 10 (11:17 27/10/2026): chốt đợt cải tiến từng khâu — thử "trả lời ngay, không suy luận" (kém hơn: trả lời vòng một câu lẽ ra phải từ chối); đo câu trả lời khi "luna chọn 10 đoạn" (kém hơn theo luật dù trung bình tăng); đo lỗi sai số liệu (0 / 68 câu thấy được); thử luật kiểm sau sinh (gác); **chatbot không đổi**, bước tiếp là bạn đọc cặp mù rồi đưa 10 đoạn vào chatbot.** Bản 9 (22:31 26/10): phân loại lỗi trả lời; thử lại "trả lời phần có căn cứ" (R2) — kém hơn, gác; "nêu đủ chi tiết" (R3) không đủ câu; chatbot không đổi.** Bản 8 (16:0x 26/10): đợt 3 rà code — gỡ "Representation B"; chuỗi gửi model giống từng byte (25 câu).** Bản 7 (21:50 25/10): API báo đúng loại lỗi (gói 1b). Bản 6 (19:59): sửa lỗi trích dẫn `[Nguồn n]`; đính chính
nguyên nhân "quên ghi `[n]`" của 8.1. Bản 5 (14:10): kết quả Phase 8.1.
Người viết: A (bản 12, qua sub-agent), C (bản 10), A (bản 6), B (bản 5; bản 1–4: C) · Review: A (bản 10), C (bản 6: sửa code C làm, B review). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chatbot Huế **trả lời câu hỏi trên toàn bộ kho dữ liệu** (món ăn, di tích, lễ
  hội, nghệ thuật, du lịch) qua một API và một trang web đơn giản. Mỗi câu trả lời có trích dẫn `[1]`,
  `[2]`… trỏ tới đoạn nguồn thật; không tìm thấy thông tin thì nói không đủ thông tin, không bịa.
- **Đang chạy cách nào:** lấy tối đa **10 đoạn** nguyên vẹn từ bước tìm kiếm (từ 28/10; trước 5) → `gpt-6-luna` (OpenAI) viết
  câu trả lời chỉ từ các đoạn đó → backend kiểm từng `[n]`. Trạng thái: Phase 6 đóng 23/10/2026, đạt kèm hai
  giới hạn (bảng giá, tổng hợp nhiều nguồn); 10 đoạn vào chatbot 28/10 (Phase 8.2 B1, `510e1a8`).
- **Đo được (Phase 7B, 176 câu, bản 5 đoạn):** Đúng / Đủ / Trúng ý **4,43 / 4,28 / 4,45** (thang 1–5); khi đã trả
  lời thì gần tối đa (~4,9). Từ chối đúng 18/18 câu ngoài kho. Lỗi trích dẫn 4/176 lúc đo — **sau sửa 25/10 còn 0–2/176** (mục 4, bản 6).
- **Giới hạn chính:** **từ chối nhầm** câu có trong kho — nguồn mất điểm lớn nhất (22/158 ở 5 đoạn, Phase 7B; **12/158 ở 10 đoạn**, B1); không tìm ra
  bảng giá; câu cần nhiều nguồn lúc đóng chỉ dùng 1 nguồn.
- **Chi phí:** sinh 176 câu ~0,024 USD ở 5 đoạn; **0,0369 USD ở 10 đoạn** (B1, ~920 đồng). Mỗi câu hỏi trên web có phí rất nhỏ.
- **Thời gian chờ thật qua API (27/10, bản 5 đoạn):** trung vị ~3,3 s, câu chậm ~5,7–6,2 s (đã vượt mức theo dõi 5 s); ~98 % là thời gian model viết.
  Bản 10 đoạn chưa đo trung vị / câu chậm trên chatbot thật (2 câu thử 28/10: 5,1 s và 2,5 s) — sẽ đo ở bộ "trước" của đợt sửa kho.
  Từ 27/10 API ghi **một dòng số đo mỗi câu** (token, thời gian từng khâu; không ghi nội dung) ⇒ tiền / thời gian đọc từ log.
- **Phase 8.1 đã thử (25/10, 0,157 USD):** 5 cách trả lời trên 120 câu thử, chấm mù bằng Claude. **Một cách thắng và đã
  xác nhận trên bộ kiểm: đưa 10 đoạn thay vì 5** — điểm Đủ +0,26 (thử) / +0,27 (kiểm) trên thang 5, từ chối nhầm giảm gần
  một nửa, tốn thêm ~50%/câu (≈ 5 đồng). Các cách khác không khác hoặc kém hơn. **Đã đưa vào chatbot 28/10.**
- **Đợt cải tiến từng khâu (26–27/10, trên mốc 10 đoạn) — đã chốt, không nhận thêm cách nào:**
  - "Trả lời phần có căn cứ" và "trả lời ngay, không suy luận" đều **kém hơn** vì cùng một lỗi: với câu lẽ ra phải từ chối, model nêu một thông
    tin có thật nhưng không phải điều được hỏi, rồi thêm câu "nguồn không nêu…". Lợi của bản "không suy luận" cũng nhỏ: tiền mỗi câu chỉ giảm 3–6 %.
  - "Luna chọn 10 đoạn" (khâu tìm, `BAO_CAO_TIM_KIEM.md` bản 8): câu trả lời **trung bình tốt lên** (đủ ý +0,22, đúng +0,25 / 5; từ chối nhầm 7 → 2 / 88)
    nhưng **5 câu bị chấm thấp hơn**, quá 4 câu cho phép ⇒ **kém hơn theo luật**. Giá: chờ ~6,5 s (có lúc 9 s), tiền ×3,8.
  - **Sai số liệu** (giá, giờ, năm…): ở bản 10 đoạn, **0 / 68** câu trả lời có số bị thấy sai.
  - Tiền cả đợt Phase 8.2 tới giờ ≈ **0,21 USD** (≈ 5.300 đồng) / trần 0,5.
- **Bạn cần làm:** không có việc gấp. Chatbot **đang chạy 10 đoạn + chuẩn hóa chữ câu hỏi** từ 28/10 (bạn chọn PA3: không chờ đọc cặp mù). **Giới hạn:**
  chọn bằng judge Claude, **chưa có mốc người**; tiền mỗi câu tăng (đọc vào nhiều hơn). Khi rảnh, trước buổi bảo vệ: **bạn đọc cặp mù** (20 câu, ~30–45 phút) —
  nếu bạn thấy ngược judge nhiều (luật dừng spec 8.2 §11) thì A trình bạn chọn giữ 10 đoạn hay quay về 5 (đổi một dòng cấu hình).

## 2. Hoạt động thế nào (bản đang chạy)

```text
trang web / POST /api/chat {"query": "..."}
 → chuẩn hóa chữ câu hỏi (NFC) → tìm 10 đoạn (Phase 5) → lấy tối đa 10 đoạn nguyên vẹn, vừa ngân sách token
 → gpt-6-luna viết câu trả lời, chỉ dùng các đoạn đó, đặt [n] sau mỗi ý
 → backend kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources} — hoặc lỗi có mã rõ ràng (vd. 500 nếu trích dẫn hỏng)
```

- Khi khởi động, hệ thống so "dấu vân tay" dữ liệu với chỉ mục; dữ liệu đổi mà chưa build lại thì
  từ chối chạy.
- Câu hỏi 1–500 ký tự (sau khi bỏ khoảng trắng đầu/cuối).
- Ví dụ: hỏi về đồi Vọng Cảnh → câu trả lời có `[1]`; bấm `[1]` trên trang web sẽ cuộn tới thẻ nguồn
  ghi tiêu đề, mục và đoạn trích nguyên văn.
- Code: `backend/api/routes/chat.py` (API), `backend/retrieval/full_corpus_context.py` (chọn tối đa 10 đoạn; số đoạn ở `backend/config/settings.yaml` `max_context_documents`),
  `backend/llm/full_corpus_prompt.py` (prompt), `backend/llm/generator_openai_full_corpus.py` (gọi
  model), `backend/llm/citations.py` (kiểm trích dẫn), `frontend/` (trang web).

Tự hỏi chatbot (không bắt buộc): bật Qdrant (`docker compose up -d`), chạy API từ `backend/`
(`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`), mở
`http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (có phí rất nhỏ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu có đủ bằng chứng trong các đoạn ngữ cảnh → trả lời kèm `[n]` | **Đã xử lý, đóng gói** | 4,43 / 4,28 / 4,45 trên 176 câu (7B, đo ở 5 đoạn); khi đã trả lời ~4,9 |
| Câu ngoài kho → từ chối, không bịa | **Đã xử lý, đóng gói** | 18/18 từ chối đúng |
| Kiểm `[n]` trỏ đúng nguồn, lỗi thì trả mã rõ ràng | **Đã xử lý, đóng gói** | nhận cả `[Nguồn n]`, đổi về `[n]` (25/10); lỗi 500 còn 0–2/176 (trước 4–8); `backend/llm/citations.py` |
| Trang web bấm `[n]` tới thẻ nguồn | **Đã xử lý, đóng gói** | `frontend/`; `backend/api/app.py:147–151` |
| Dữ liệu lệch chỉ mục → từ chối khởi động | **Đã xử lý, đóng gói** | báo đúng 409 "cần lập chỉ mục lại" từ 25/10 (trước báo nhầm 503); test `test_api_chat.py` (kho đổi ⇒ 409) |
| Qdrant / model tìm kiếm lỗi → báo lỗi tạm | **Đã xử lý, đóng gói** | 503 `retrieval_unavailable` (trước: Qdrant lỗi khi hỏi ra 500; thiếu model sẽ thành 409 nếu chỉ sửa nửa vời); test `test_startup_model_missing.py` (User chạy `!`) |
| Câu có một vế có bằng chứng, vế kia thiếu | **Đã thử, chưa áp dụng** | Prompt bắt từ chối cả câu (`full_corpus_prompt.py:14`). 8.1 thử prompt "trả lời phần có căn cứ": từ chối nhầm 13 → 1 câu (120 câu thử), nhưng **trả lời cả 2 câu ngoài kho** ⇒ phạm luật, chưa dùng. **26/10 (R2, chữ prompt siết hơn, mốc 10 đoạn):** vẫn trả lời 1 / 12 câu ngoài kho cùng kiểu lỗi ⇒ dừng ngay bước đầu (0,0027 USD); **hướng này gác**. **27/10:** luật kiểm bằng code sau khi sinh **không tách được** câu lạc đề với câu trả lời một phần có ích ⇒ không mở lại được hướng này |
| Đoạn chứa đáp án nằm ngoài các đoạn ngữ cảnh | **Xử lý một phần** | 8.1 đo bằng đoạn đúng: **cả 22/22** câu từ chối nhầm ở 7B đều thiếu ít nhất một đoạn đúng trong 5 đoạn — gốc là khâu tìm/xếp đoạn. 28/10 nới lên 10 đoạn (dòng dưới); đoạn đúng xếp ngoài 10 đoạn đầu vẫn còn (`BAO_CAO_TIM_KIEM.md`) |
| Có đủ bằng chứng mà vẫn từ chối | **Đính chính (8.1)** | Chẩn đoán 7B (theo keyword) ghi 4/22; đo lại bằng đoạn đúng: **0 câu** |
| Đưa 10 đoạn ngữ cảnh thay vì 5 | **Đã xử lý, đóng gói** (28/10; đang chạy, đã kiểm) — chưa có mốc người | 8.1: điểm Đủ +0,26 (120 câu thử) / +0,27 (56 câu kiểm); từ chối nhầm 13 → 7; 0 câu ngoài kho bị trả lời; lỗi trích dẫn không tăng. Merge `510e1a8` (kèm chuẩn hóa chữ câu hỏi): 51 test đạt, kết quả tìm 158 câu giống từng byte, chạy thật 2 câu đạt. **Giới hạn:** chọn bằng judge Claude, **chưa có mốc người** (bạn đọc cặp mù sau, PA3 28/10); tiền mỗi câu tăng; thời gian chờ ở 10 đoạn chưa đo trung vị / câu chậm. Đổi ngược được: `settings.yaml` `max_context_documents` 10 ⇒ 5 |
| Xếp 5 đoạn gom theo tài liệu | **Đã thử, chưa áp dụng** | 8.1: không khác |
| Thêm 2 luật cũ của spec Phase 6 (không dùng tiêu đề làm bằng chứng; đoạn văn ngắn) | **Đã thử, chưa áp dụng** | 8.1: không khác; lỗi trích dẫn 4 → 1 (chưa đủ chắc) |
| Mức suy luận của model (`none` / `low` / `high`) | **Đã thử, chưa áp dụng** | 8.1 (5 đoạn): `none` đầy đủ hơn chút; `low` / `high` không khác hoặc kém. **27/10, `none` trên mốc 10 đoạn:** **kém hơn** — câu 168 lẽ ra phải từ chối (kho không có thông tin) bị trả lời vòng; dừng ở 24 câu đầu, 0,0049 USD. Lợi đo được nhỏ: token model viết ra ~0,72×, tiền mỗi câu chỉ ~0,94–0,97× (tiền chủ yếu ở phần đọc vào). Muốn dùng còn phải đổi quy ước Phase 6 "không truyền mức suy luận" |
| Câu trả lời quá gọn, bỏ chi tiết có trong nguồn (giờ, năm, tên riêng…) | **Chưa thực hiện** | 26/10 phân loại lỗi: 9 / 88 câu điểm 4 vì bỏ chi tiết. Thử câu prompt "nêu đủ chi tiết" (R3) **không chạy**: ở mốc 10 đoạn chỉ 6 câu có thể đổi, dưới số câu cần để kết luận ⇒ cần thêm câu tự nhiên |
| Câu trả lời ghi sai con số (giá, giờ, năm, khoảng cách) | **Xử lý một phần** (đo được, chưa có rào chặn) | 27/10 (mốc 10 đoạn, 120 câu thử): 68 câu trả lời có số; máy nghi 4 câu, đọc lại cả 4 là phép tính **đúng**; đọc thêm 10 câu ngẫu nhiên: 10 / 10 đúng ⇒ **0 câu sai số thấy được**. Thước đếm số chỉ dùng làm danh sách đọc lại (mọi cờ là báo nhầm). Chưa đo sai về chữ (tên, sự kiện) |
| Kiểm bằng code sau khi sinh để chặn "trả lời vòng" | **Đã thử, chưa áp dụng** | 27/10 (0 USD, đọc lại mọi lượt đã ghi): một luật bắt được 2 câu lỗi đã biết (sau khi chỉnh trên chính 2 câu đó), 0 cờ ở chatbot 10 đoạn; nhưng 7 / 10 câu bị cờ trong mẫu đọc tay là câu có ích ⇒ **gác** (không thêm vào chatbot) |
| "Luna chọn 10 đoạn" — ảnh hưởng tới câu trả lời | **Đã thử, chưa áp dụng** | 27/10, 120 câu thử: trung bình tốt lên (đủ ý +0,22, đúng +0,25, trúng ý +0,23 / 5), từ chối nhầm 7 → 2 / 88, 0 câu ngoài kho bị trả lời, 0 lỗi 500; nhưng **5 câu đủ ý thấp hơn** > 4 cho phép ⇒ kém hơn theo luật, không chạy bộ kiểm. Chờ ~6,5 s / câu, tiền ×3,8. Chi tiết bước tìm: `BAO_CAO_TIM_KIEM.md` bản 8 |
| Chính sách trích dẫn "chỉ có một nguồn thì gán nguồn đó" | **Đã thử, chưa áp dụng** | 8.1 phát lại trên câu trả lời đã lưu: 0 câu đổi. (Đính chính 25/10: lỗi lúc đó **không** phải "quên `[n]`" mà là dạng `[Nguồn n]` — đã sửa, mục 4 bản 6) |
| Câu tổng hợp nhiều nguồn | **Xử lý một phần** | Lúc đóng đạt nhưng chỉ dùng 1 nguồn; chưa chứng minh tổng hợp |
| Câu hỏi giá vé + miễn giảm (bảng giá) | **Chưa thực hiện** | Không tìm ra bảng giá (xem `BAO_CAO_TIM_KIEM.md`) |
| Tách câu hỏi hai ý | **Chưa thực hiện** | Phase 8 thử |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 28/10/2026 — Đưa 10 đoạn + chuẩn hóa chữ câu hỏi vào chatbot (bản 12)

- **Vì sao bây giờ:** bạn chưa rảnh đọc cặp mù và muốn xong phần tồn sớm; việc đọc cặp mù đang chặn cả chuỗi (mốc cuối 8.2 ⇒ sửa kho ⇒ Qwen3-8B). Bạn chọn
  **PA3** (09:29 28/10, spec 8.2 §11): đưa vào theo judge Claude, đọc cặp mù làm sau. Cái giá: tới khi bạn đọc, kết quả này **chưa có mốc người**.
- **Đã kiểm trên `main` `510e1a8`:** 51 test đạt (2 test còn lại cần key — đúng như trước); kết quả tìm 158 câu giống từng byte mốc cũ; câu dạng NFD cho
  đúng 10 đoạn và đúng ngữ cảnh như câu NFC; chạy thật 2 câu tự viết: câu trong kho 200, 10 đoạn đưa vào, 6 nguồn được trích (5,1 s); câu ngoài kho từ
  chối đúng (2,5 s); log mỗi câu một dòng, không chứa câu hỏi. Tiền ≈ **0,000423 USD**.
- **Còn chờ:** đo trung vị / câu chậm ở 10 đoạn trong bộ "trước" của đợt sửa kho.

### 27/10/2026 (chiều) — Đo thời gian chờ thật + API ghi số đo (bản 11)

- **Thời gian chờ thật qua API** (22 câu tự viết, không lấy từ bộ chấm; B65 / C57): bản đang chạy (5 đoạn) trung vị **3,3 s**, câu chậm (p95) **5,7 s**
  khi hỏi lần lượt, 3,6 / 6,2 s khi 4 câu cùng lúc — **đã vượt mức theo dõi 5 s**. Bản 10 đoạn (chờ bạn đọc cặp mù) **không chậm hơn** (chênh nằm trong dao
  động). 0 lỗi, 2 / 2 câu ngoài kho từ chối đúng. ≈ 0,016 USD (ước).
- **Thời gian nằm ở đâu** (C58 / B67): gọi model ≈ **98 %**; tìm đoạn ~40 ms, dựng ngữ cảnh ~2 ms, kiểm trích dẫn ~0 — *đã chứng minh* phần dư không ở đường API.
  Thời gian viết đi theo số token model viết ra (~1,2 s + 11,5 ms / token, tương quan 0,97 — *giải thích được, chưa thử đổi*). Muốn nhanh hơn: bớt chữ model viết
  (cần thí nghiệm — bản "không suy luận" đã phạm sàn) hoặc hiện chữ dần (streaming, phải đổi cách kiểm trích dẫn). 0,0075 USD.
- **API ghi số đo mỗi câu** (bạn duyệt 27/10; C60 code, B70 review, merge `5100b90`; cổng ổn định trên `main`: câu trong kho 200 có 2 nguồn, câu ngoài kho từ chối,
  khuôn phản hồi không đổi, mỗi câu đúng một dòng log, câu hỏi không có trong log). Từ nay tiền / thời gian mỗi câu đọc được từ log, không phải ước.

### 27/10/2026 — Chốt đợt cải tiến từng khâu (bản 10)

Mốc so sánh: bản 10 đoạn + chuẩn hóa chữ câu hỏi (chưa vào chatbot), 120 câu thử (88 câu chính). Mọi luật ghi trước khi chạy, người khác kiểm
lại. Chatbot **không đổi**. Tiền thật lấy từ usage log.

- **Trả lời ngay, không suy luận (R1) — kém hơn.**
  - Ý tưởng: bỏ phần suy nghĩ ẩn của model để rẻ / nhanh hơn, với điều kiện chất lượng không tụt.
  - Quan sát: 12 / 12 câu ngoài kho vẫn từ chối đúng; nhưng câu 168 — kho không có thông tin được hỏi, bản hiện tại từ chối đúng — bị trả lời vòng (nêu
    một mức giá có nguồn nhưng không phải khoản được hỏi, rồi "nguồn không nêu…"). Phạm sàn ⇒ dừng ở 24 câu đầu. **0,0049 USD.**
  - Số theo dõi trên 24 câu (không dùng để kết luận): token model viết ra ~0,72×; tiền mỗi câu ~0,94–0,97×.
- **Câu trả lời khi "luna chọn 10 đoạn" (K3b-m) — kém hơn theo luật.**
  - Luật: không câu ngoài kho nào bị trả lời, 0 lỗi 500, và mỗi chỉ số chỉ được tụt tối đa (số câu dao động giữa hai lượt chạy giống hệt + 3) — đủ ý ≤ 4 câu.
  - Kết quả: đạt mọi sàn; điểm đúng, từ chối nhầm, độ dài câu trả lời đạt; **đủ ý tụt 5 câu** ⇒ kém hơn, dừng, không chạy bộ kiểm.
  - Đọc lại 5 câu tụt (người kiểm, một người): 1 câu bỏ mất ý chính; 3 câu thiếu một chi tiết nhỏ; 1 câu nhiều khả năng do người chấm không nhất quán
    (hai câu trả lời cùng thiếu một ý, một bên 5 điểm, một bên 4) — *quan sát*, không đổi kết luận.
  - **Chỉ báo (không dùng để quyết):** đủ ý +0,22 [+0,02; +0,44], đúng +0,25 [+0,07; +0,47], trúng ý +0,23 [+0,05; +0,44] / 5 (khoảng tin cậy 95 %); từ chối
    nhầm 7 → 2 / 88; 6 câu trước bị từ chối nay được trả lời và chấm 5 / 5, không câu nào trả lời vòng.
  - **Giá:** thời gian chờ cả câu (tìm + chọn đoạn + viết) p50 **6,5 s**, p95 **9,1 s** (đo khi chạy 4 câu song song; mốc 10 đoạn chỉ có bước viết câu trả lời, p50 ~1,8 s).
    **Tiền lượt đo: 0,0749 USD** (≈ 1.900 đồng). **Tiền mỗi câu nếu chạy thật: ≈ 0,00078 USD, gấp 3,8 lần** — con số này đã cộng tiền chọn đoạn của 40 câu
    dùng lại kết quả lượt trước (tiền đó trả ở lượt bước tìm, không tính lại vào 0,0749).
- **Sai số liệu trong câu trả lời (C48) — đo hiện trạng, 0 USD:** 99 câu trả lời, 68 câu có số; máy nghi 4 câu (đều là phép tính đúng, ví dụ hiệu hai giá);
  đọc thêm 10 câu: đúng hết ⇒ **0 / 68 câu sai số thấy được**. *Suy ra*: lỗi này hiếm ở bản 10 đoạn, nhưng một lượt cũ từng có 2 câu sai số thật ⇒ có dao động.
- **Luật kiểm sau sinh (C51) — gác, 0 USD:** bắt được kiểu "một câu có nguồn + một câu nói nguồn không có…", nhưng không phân biệt câu lạc đề với câu
  trả lời một phần có ích (mẫu đọc tay: 7 / 10 cờ là câu có ích). A gác hướng "không suy luận + luật kiểm".
- **Kết luận đợt (bạn chọn 27/10):** không thử thêm; chatbot giữ nguyên; bước tiếp là bạn đọc cặp mù rồi đưa 10 đoạn vào chatbot.

### 26/10/2026 (tối) — Phân loại lỗi trả lời; thử lại trả lời một phần (bản 9)

- **Phân loại lỗi (C36, 0 USD):** 88 câu thử chính, mốc 10 đoạn: 10 câu kém, **cả 10 thiếu thông tin trong 10 đoạn** (model không bịa, citation sai
  rất ít). Điểm "đủ ý" mất 46: 20 do từ chối khi có một phần thông tin (5 câu), 9 do trả lời quá gọn (9 câu), 17 do thiếu thông tin hẳn.
- **R2 — trả lời phần có căn cứ:** kém hơn, phạm sàn ngay bước đầu (1 câu ngoài kho bị trả lời), 0,0027 USD; gác.
- **R3 — nêu đủ chi tiết:** NOT RUN (6 câu có thể đổi). **R4:** thước kiểm số liệu trong câu trả lời có trong nguồn được trích — chỉ dùng để chọn câu
  đọc lại (ngoài mẫu đúng 0 / 5).
- Tốc độ khâu sinh đo bằng **số token model viết ra** (thời gian chờ provider dao động ~0,8 s / câu, không phân biệt được chênh lệch nhỏ).
- Hồ sơ: `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_C.md`, nhánh `p82-r2`, `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r{3,4}_*`.

### 25/10/2026 — API báo đúng loại lỗi (bản 7, rà code gói 1b)
- **Lỗi:** cùng một module bị nạp hai lần dưới hai tên ⇒ API không nhận ra lỗi của bước tìm kiếm: Qdrant lỗi khi hỏi ⇒ 500 thay 503; kho
  đổi chưa dựng lại ⇒ 503 thay 409. Chatbot vẫn an toàn (không trả lời bừa), chỉ báo sai lý do.
- **Sửa:** một cách import duy nhất (chạy mọi lệnh từ `backend/`); lỗi "model không nạp" tách khỏi "cần lập chỉ mục lại"; bỏ nhánh 409 lúc hỏi
  không bao giờ chạy. Hai cách import được so bằng số file / lệnh phải đổi trước khi chọn (cách được chọn đổi ít hơn: 13 so với 18 file code).
- **Đo (tiêu chí ghi trước trong plan):** module nạp đôi 3–14 ⇒ 0 ở 12 điểm chạy; 3 test mới đỏ trước / xanh sau; 15 file test 196 ⇒ 198 đạt
  (8 lỗi còn lại cũ — test cần key); kết quả tìm kiếm giống từng byte; chạy thật đạt. **PASS** — B làm, C review. Tiền ~0,0008 USD.

### 25/10/2026 — Sửa lỗi trích dẫn `[Nguồn n]` (bản 6, rà code gói 1a)
- **Lỗi:** ngữ cảnh gửi model ghi nhãn mỗi đoạn là "[Nguồn n]", model đôi khi trích đúng dạng đó; bộ kiểm chỉ hiểu "[n]" ⇒ người dùng
  nhận lỗi 500 dù câu trả lời có nguồn. Phát hiện khi rà code (C), A và B đếm lại độc lập.
- **Sửa:** bộ kiểm nhận cả hai dạng; API đổi mọi trích dẫn về "[n]" trước khi trả trang web. Không đổi prompt, không đổi câu trả lời.
- **Đo (tiêu chí ghi trước: câu đang đạt không được thành lỗi, không đổi nguồn):** trên 1.600 câu trả lời đã sinh (7B, 8.1, 8.2 B1) lỗi
  **69 → 14**, 0 câu đạt bị đổi; cấu hình chatbot đang chạy 4–8 → **0–2 / 176**; 14 lỗi còn lại đều là câu thật sự không ghi nguồn.
  2 câu hỏi thật qua API: đạt, 0,000427 USD. Test: 39 đạt (3 lỗi cũ do thiếu key, đã biết). **PASS** — C làm, B review.
- **Hệ quả:** con số "lỗi trích dẫn" của 7B / 8.1 đếm theo cách cũ, không so trực tiếp với số mới; quyết định 8.1 bỏ "suy luận `none`"
  (vì lỗi trích dẫn 4 → 8) có thể phải xem lại — đếm lại là 0 → 2 (giả thuyết, cần thí nghiệm; A sẽ ước tiền và hỏi bạn).

### 25/10/2026 — Phase 8.1: thử 5 cách trả lời (bản 5)

Chatbot không đổi; chỉ thí nghiệm. **Luật ghi trước:** chỉ số quyết là điểm **Đủ** (Completeness) do Claude chấm mù
(không biết câu trả lời thuộc cách nào), so theo cặp từng câu, có hiệu chỉnh khi thử nhiều cách; **rào chắn:** không được trả
lời câu ngoài kho, điểm Đúng không tụt, lỗi trích dẫn tăng tối đa 2 câu (bằng mức dao động đo được giữa hai lần chạy 7B), tiền
mỗi câu không quá gấp đôi. Bộ: 120 câu thử (88 câu có trong kho tính số chính, bỏ câu hỏi không tự nhiên); cách "tốt hơn"
phải xác nhận trên 56 câu kiểm. Mỗi lượt có phí chạy thử 10 câu trước.

| Cách | Điểm Đủ (thử) | Rào chắn | Kết luận |
|---|---|---|---|
| **10 đoạn ngữ cảnh** | **+0,26** (chắc) | đạt cả 4; tiền ×1,5 | **tốt hơn**; bộ kiểm **+0,27** ⇒ **đã xác nhận** |
| Xếp 5 đoạn gom theo tài liệu | −0,02 | đạt | không khác |
| Prompt "trả lời phần có căn cứ" | +0,11 (chưa chắc) | **trả lời 2 câu ngoài kho** | **kém hơn** (dù từ chối nhầm 13 → 1) |
| Prompt thêm 2 luật cũ | 0,00 | đạt; lỗi trích dẫn 4 → 1 | không khác |
| Mức suy luận `none` | +0,14 (chắc) | **lỗi trích dẫn 4 → 8** | **kém hơn** |
| Mức suy luận `low` / `high` | +0,02 / +0,02 | `low`: lỗi trích dẫn 4 → 9 | `low` kém hơn; `high` không khác |
| Chính sách trích dẫn "một nguồn thì gán" | — | — | không khác (0 câu đổi khi phát lại) |

Thêm: lợi của 10 đoạn nằm ở các câu mà 5 đoạn **chưa đủ** bằng chứng; câu đã đủ bằng chứng không bị hỏng (0 câu thua). Người
chấm (Claude) chấm lại cùng câu trả lời thì chỉ 2/88 câu đổi điểm Đủ. **Tiền:** 0,157 USD (≈ 3.900 đồng) cho ≈ 1.070 câu trả
lời `gpt-6-luna` (8 lượt × 120 câu thử + 2 lượt × 56 câu kiểm); chấm bằng Claude không tốn tiền.

Đính chính: chẩn đoán 7B "4/22 câu có đủ bằng chứng mà vẫn từ chối" dựa trên keyword; đo lại bằng **đoạn đúng** (8.1) thì
**0 câu** — mọi câu từ chối nhầm đều thiếu ít nhất một đoạn đúng trong ngữ cảnh.

### 24/10/2026 — Dọn code món ăn sau Phase 7 (bản 4)
Gỡ đường sinh câu trả lời bản món ăn (hỏng từ trước) cùng code/test món ăn. Đường sinh câu trả lời
toàn kho không đổi; lượt sinh thử 10 câu sau dọn chạy đủ, 0 lỗi kỹ thuật (~0,0013 USD, do B chạy) ·
**PASS**. Không đổi số đo nào.

### 24/10/2026 — Đính chính về "Representation B" (bản 3)
Khi rà quyết định Phase 8.1: phần sinh ngữ cảnh B đã được gọi thử thật 1 lần ở Phase 6 (đạt); cái chưa
có là chỉ mục dựng từ B và phép đo tìm kiếm. Bản 2 ghi "chưa từng dùng" là nhầm. Không đổi số đo nào.

### 24/10/2026 — Đo đủ 176 câu (Phase 7B, cùng code Phase 6, chỉ mục 7A2)
Cách đo: chatbot thật trả lời, Claude chấm so với đáp án mẫu · kết quả: đo mốc (chưa đặt ngưỡng) —
Đúng/Đủ/Trúng ý 4,43 / 4,28 / 4,45; từ chối đúng 18/18; từ chối nhầm 22/158 (8 đoạn đáp án không vào
ngữ cảnh, 10 có một vế thiếu vế kia, 4 có đủ mà vẫn từ chối); lỗi trích dẫn 4/176 · tiền sinh 176 câu
~0,024 USD (~600 đồng).
Thử nhanh 10 đoạn ngữ cảnh trên 22 câu từ chối nhầm: 10/22 câu hết từ chối — **chưa chấm** đúng/sai,
chỉ là dấu hiệu; **chưa áp dụng**, chờ Phase 8.

### 23/10/2026 — Đóng Phase 6 trên `gpt-6-luna`
Cách đo: 5 câu thật · kết quả: **PARTIAL** — 4 đạt / 1 không đạt (câu "giá vé + miễn giảm": không tìm
ra bảng giá); câu tổng hợp nhiều nguồn đạt nhưng chỉ dùng 1 nguồn · giữ, đóng kèm hai giới hạn.

### Trước 23/10/2026 — Đổi model sinh nhiều lần (bản toàn kho)
Qwen 3.5-9B qua OpenRouter → `gpt-5.4-nano` → `gpt-6-luna` · hai model đầu **đã bỏ**, thay bằng
`gpt-6-luna` (quyết định 23/10).

### 08/2026 — Bản món ăn (`gpt-5.4-nano`)
Nay **đã bỏ** và hỏng thật: đường sinh câu trả lời bản món ăn gửi tham số `temperature` nên
`gpt-6-luna` trả lỗi 400; code đã gỡ khi dọn sau Phase 7 (24/10).

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`, sau dọn) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| API `POST /api/chat`, trả `{answer, sources}`, câu hỏi 1–500 ký tự | **còn dùng** | `backend/api/routes/chat.py:24–26,48` |
| Model sinh `gpt-6-luna` (OpenAI) | **còn dùng** | `backend/config/settings.yaml:47` |
| Tối đa 5 đoạn nguyên vẹn, ngân sách 16.384 token | **đã thay** 28/10 bởi **tối đa 10 đoạn** (cùng ngân sách 16.384 token; merge `510e1a8`, PA3 — chưa có mốc người) | `settings.yaml:52,55`; `backend/retrieval/full_corpus_context.py` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng**; 8.1 và 26/10 thử bản "trả lời phần có căn cứ": kém hơn (trả lời câu ngoài kho); luật kiểm sau sinh 27/10 không cứu được hướng này | `backend/llm/full_corpus_prompt.py:14` |
| Không gửi mức suy luận (để model tự chọn) | **còn dùng**; 27/10 thử `none` trên mốc 10 đoạn: kém hơn (trả lời vòng câu 168), lợi tiền nhỏ (~3–6 %) | `backend/llm/generator_openai_full_corpus.py` |
| Chẩn đoán 7B "4/22 câu có đủ bằng chứng mà vẫn từ chối" | **đã thay** bởi số đo theo đoạn đúng của 8.1: 0/22 | `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` G1.6 |
| Backend kiểm trích dẫn, lỗi trả mã rõ ràng | **còn dùng** | `backend/llm/citations.py:12`; `backend/api/routes/chat.py` |
| Trang web tối giản, bấm `[n]` tới thẻ nguồn | **còn dùng** | `frontend/`; `backend/api/app.py:147–151` |
| Từ chối chạy khi dữ liệu lệch chỉ mục | **còn dùng** | `backend/retrieval/full_corpus.py:353,415` |
| Qdrant cổng 6335 | **còn dùng** | `settings.yaml` `vector_database.url` |
| Qwen 3.5-9B qua OpenRouter, `gpt-5.4-nano` | **đã thay** bởi `gpt-6-luna` (quyết định 23/10) | [R3] |
| Collection metadata v2 (8.460 đoạn) mà Phase 6 đóng trên đó | **đã thay** bởi chỉ mục 7A2 (8.459 đoạn) | `Project_Status.md` §4 |
| "Representation B" (LLM viết thêm ngữ cảnh cho đoạn) | **đã gỡ** 26/10 (gọi thử 1 lần ở Phase 6, chưa từng có chỉ mục; bạn duyệt gỡ 19:4x 25/10) | đợt 3 rà code, commit `c6e130c`; bộ chạy kiểm khói Phase 6 còn 4 câu |
| API/sinh câu trả lời bản món ăn | **đã gỡ** khi dọn sau Phase 7 (trước đó hỏng thật: gửi `temperature` → lỗi 400) | commit `1832201` (xóa `backend/llm/generator_openai.py`) |

## 6. Việc còn lại / cần quyết

- **10 đoạn + chuẩn hóa chữ câu hỏi đã vào chatbot 28/10** (bản 12). Còn: **bạn đọc cặp mù** (20 câu, ~30–45 phút, khi rảnh, trước buổi bảo vệ) — làm mốc
  người; nếu bạn ngược judge nhiều (luật dừng spec 8.2 §11) ⇒ A trình giữ 10 / quay về 5. Đo trung vị / câu chậm ở 10 đoạn trong bộ "trước" của đợt sửa kho.
- Hướng đã thử và gác (chỉ mở lại khi có ý mới đã kiểm trước): "trả lời phần có căn cứ"; "trả lời ngay, không suy luận"; luật kiểm sau sinh; "luna chọn 10
  đoạn" (tốn ×3,8 và chờ ~6,5 s, khâu trả lời kém hơn theo luật).
- Còn mở, không gấp: câu trả lời quá gọn (cần thêm câu hỏi tự nhiên để đo được); bảng giá và tổng hợp nhiều nguồn (gốc ở khâu tìm, `BAO_CAO_TIM_KIEM.md`);
  sai về chữ (tên, sự kiện) chưa có cách đo rẻ; API ghi token mỗi câu từ 27/10 (`chat_metrics`), chưa ghi USD.

## Phụ lục — hồ sơ kỹ thuật

- **Bản 12 (28/10/2026):** spec 8.2 §11 (PA3, commit `d922bf7`); merge `510e1a8` = nhánh `p82-b1` `c3d5607`; report
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_merge_implementation.md` (C71 review ready `phase_8_2_b1_merge_review.md`); dữ liệu `data/phase_8_2/b1/merge_2810/` (private).
- **Bản 10 (C55, 27/10/2026):** spec 8.2 §10 (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`, bản `cd910c4c4169`); mốc B1 nhánh `p82-b1`
  `811d25d`. Report trong `report_agent/2026-10-25_phase_8_2_ap_dung/`:
  - **R1** (biến thể mức suy luận của đợt cải tiến — khác tài liệu tham chiếu [R1] bên dưới) `reasoning_effort="none"`: plan `phase_8_2_r1_plan.md` (sha `8e76e77e0448`), report trên nhánh `p82-r1` `63a472f`, review B58 (A đóng `d665a5b`);
    sàn phạm: câu 168. 0,0049030 USD.
  - **K3b-m khâu trả lời:** plan `phase_8_2_k3b_m_answer_plan.md` bản 3 (sha `2a3b22b38ab6`; bản 2 dừng ở pilot vì sàn câu 120 đặt trên tiền đề nhãn thiếu),
    report nhánh `p82-k3b` `a6f609c`, review `phase_8_2_k3b_m_answer_review.md` (C54). Mức tụt T3: 5 câu (26, 66, 93, 112, 134) > 4. Tiền 0,0749297 USD
    (bản 2 pilot 0,0047854 + v3 0,0701443). Khâu tìm: `BAO_CAO_TIM_KIEM.md` bản 8.
  - **C48** `report_agent/2026-10-26_cai_tien_tung_khau/c48_so_trong_cau_tra_loi.md`; **C51** `…/c51_kiem_sau_sinh_kha_thi.md`.
  - Tổng hợp đợt: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.
- Mã giới hạn: tổng hợp nhiều nguồn = **F1**; bảng giá = **F2**. Câu hỏi "trả lời một phần" = **H8**
  trong [R1].
- [R1] giả thuyết Phase 8: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- [R3] đổi model: `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md`.
- Chẩn đoán từ chối nhầm: `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`; thử 10 đoạn:
  `reports/phase_8_probe_context_top10_2026_10_24.md`.
- Bản 5 (B20, 25/10/2026): Phase 8.1 G2 — `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_implementation.md`
  §4 (G2.1a context 10 = **tốt hơn, xác nhận test**; G2.1b, G2.2 P1/P2, G2.3, G2.4), review `phase_8_1_g2_review.md`; luật
  ghi trước: plan `phase_8_1_g2_g4_plan.md` §2.1 (sha `a4adfc8eedd9`); đính chính từ G1.6 (`phase_8_1_g1_implementation.md`).
  Golden md5 `0f7dbf41b422` (10 đáp án sửa 25/10).
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 3 (C12): đính chính theo `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` dòng 6.10 và §6 mục 13. Bản 4 (C13b): sau dọn B9 (commit `1832201`).
- **Lệch phát hiện (24/10):**
  - Spec umbrella `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` §1, Decision #6a
    cho phép "trả phần có căn cứ", nhưng spec Phase 6 (2026-09-14 §10) và prompt bắt từ chối cả câu.
    Code đúng theo spec Phase 6; đã báo A từ C1.
  - Guide `guides/full_corpus_rag.md` (Decision #6d, lịch sử) còn ghi "dùng `AsyncOpenAI` trực tiếp,
    không Agent/Runner"; code dùng OpenAI Agents SDK một lượt, không tool
    (`backend/llm/generator_openai_full_corpus.py`) — **đúng** theo amendment 2026-10-01 §SDK boundary
    (`docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md:29,59`). Không phải lỗi
    code; chỉ là đoạn guide lịch sử dễ gây hiểu nhầm.
