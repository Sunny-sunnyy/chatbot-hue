# Báo cáo cho bạn: Sinh câu trả lời, API và giao diện (Phase 6)

**Cập nhật lần cuối: 16:0x 26/10/2026 — bản 8: đợt 3 rà code — gỡ "Representation B"; chuỗi gửi model giống từng byte (25 câu).** Bản 7 (21:50 25/10): API báo đúng loại lỗi (gói 1b). Bản 6 (19:59): sửa lỗi trích dẫn `[Nguồn n]`; đính chính
nguyên nhân "quên ghi `[n]`" của 8.1. Bản 5 (14:10): kết quả Phase 8.1.
Người viết: A (bản 6), B (bản 5; bản 1–4: C) · Review: C (bản 6: sửa code C làm, B review). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chatbot Huế **trả lời câu hỏi trên toàn bộ kho dữ liệu** (món ăn, di tích, lễ
  hội, nghệ thuật, du lịch) qua một API và một trang web đơn giản. Mỗi câu trả lời có trích dẫn `[1]`,
  `[2]`… trỏ tới đoạn nguồn thật; không tìm thấy thông tin thì nói không đủ thông tin, không bịa.
- **Đang chạy cách nào:** lấy tối đa 5 đoạn nguyên vẹn từ bước tìm kiếm → `gpt-6-luna` (OpenAI) viết
  câu trả lời chỉ từ 5 đoạn đó → backend kiểm từng `[n]`. Trạng thái: đã đóng 23/10/2026, đạt kèm hai
  giới hạn (bảng giá, tổng hợp nhiều nguồn).
- **Đo được (Phase 7B, 176 câu):** Đúng / Đủ / Trúng ý **4,43 / 4,28 / 4,45** (thang 1–5); khi đã trả
  lời thì gần tối đa (~4,9). Từ chối đúng 18/18 câu ngoài kho. Lỗi trích dẫn 4/176 lúc đo — **sau sửa 25/10 còn 0–2/176** (mục 4, bản 6).
- **Giới hạn chính:** **từ chối nhầm 22/158** câu có trong kho — nguồn mất điểm lớn nhất; không tìm ra
  bảng giá; câu cần nhiều nguồn lúc đóng chỉ dùng 1 nguồn.
- **Chi phí:** sinh 176 câu ~0,024 USD (~600 đồng). Mỗi câu hỏi trên web có phí rất nhỏ.
- **Phase 8.1 đã thử (25/10, 0,157 USD):** 5 cách trả lời trên 120 câu thử, chấm mù bằng Claude. **Một cách thắng và đã
  xác nhận trên bộ kiểm: đưa 10 đoạn thay vì 5** — điểm Đủ +0,26 (thử) / +0,27 (kiểm) trên thang 5, từ chối nhầm giảm gần
  một nửa, tốn thêm ~50%/câu (≈ 5 đồng). Các cách khác (xếp đoạn theo tài liệu, thêm 2 luật cũ, "trả lời phần có căn cứ",
  đổi mức suy luận, chính sách trích dẫn mới) không khác hoặc kém hơn. Chatbot **chưa đổi**.
- **Bạn cần quyết gì (8.2):** có đưa "10 đoạn ngữ cảnh" vào chatbot không; "trả lời phần có căn cứ" có thử tiếp không
  (8.1: hết gần sạch từ chối nhầm nhưng trả lời cả 2 câu ngoài kho) — xem §6.

## 2. Hoạt động thế nào (bản đang chạy)

```text
trang web / POST /api/chat {"query": "..."}
 → tìm 10 đoạn (Phase 5) → lấy tối đa 5 đoạn nguyên vẹn, vừa ngân sách token
 → gpt-6-luna viết câu trả lời, chỉ dùng 5 đoạn đó, đặt [n] sau mỗi ý
 → backend kiểm từng [n] có trỏ đúng nguồn đã đưa không
 → trả {answer, sources} — hoặc lỗi có mã rõ ràng (vd. 500 nếu trích dẫn hỏng)
```

- Khi khởi động, hệ thống so "dấu vân tay" dữ liệu với chỉ mục; dữ liệu đổi mà chưa build lại thì
  từ chối chạy.
- Câu hỏi 1–500 ký tự (sau khi bỏ khoảng trắng đầu/cuối).
- Ví dụ: hỏi về đồi Vọng Cảnh → câu trả lời có `[1]`; bấm `[1]` trên trang web sẽ cuộn tới thẻ nguồn
  ghi tiêu đề, mục và đoạn trích nguyên văn.
- Code: `backend/api/routes/chat.py` (API), `backend/retrieval/full_corpus_context.py` (chọn 5 đoạn),
  `backend/llm/full_corpus_prompt.py` (prompt), `backend/llm/generator_openai_full_corpus.py` (gọi
  model), `backend/llm/citations.py` (kiểm trích dẫn), `frontend/` (trang web).

Tự hỏi chatbot (không bắt buộc): bật Qdrant (`docker compose up -d`), chạy API từ `backend/`
(`HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8000`), mở
`http://localhost:8000`. Mỗi câu hỏi gọi `gpt-6-luna` (có phí rất nhỏ).

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu có đủ bằng chứng trong 5 đoạn → trả lời kèm `[n]` | **Đã xử lý, đóng gói** | 4,43 / 4,28 / 4,45 trên 176 câu; khi đã trả lời ~4,9 |
| Câu ngoài kho → từ chối, không bịa | **Đã xử lý, đóng gói** | 18/18 từ chối đúng |
| Kiểm `[n]` trỏ đúng nguồn, lỗi thì trả mã rõ ràng | **Đã xử lý, đóng gói** | nhận cả `[Nguồn n]`, đổi về `[n]` (25/10); lỗi 500 còn 0–2/176 (trước 4–8); `backend/llm/citations.py` |
| Trang web bấm `[n]` tới thẻ nguồn | **Đã xử lý, đóng gói** | `frontend/`; `backend/api/app.py:147–151` |
| Dữ liệu lệch chỉ mục → từ chối khởi động | **Đã xử lý, đóng gói** | báo đúng 409 "cần lập chỉ mục lại" từ 25/10 (trước báo nhầm 503); test `test_api_chat.py` (kho đổi ⇒ 409) |
| Qdrant / model tìm kiếm lỗi → báo lỗi tạm | **Đã xử lý, đóng gói** | 503 `retrieval_unavailable` (trước: Qdrant lỗi khi hỏi ra 500; thiếu model sẽ thành 409 nếu chỉ sửa nửa vời); test `test_startup_model_missing.py` (User chạy `!`) |
| Câu có một vế có bằng chứng, vế kia thiếu | **Đã thử, chưa áp dụng** | Prompt bắt từ chối cả câu (`full_corpus_prompt.py:14`). 8.1 thử prompt "trả lời phần có căn cứ": từ chối nhầm 13 → 1 câu (120 câu thử), nhưng **trả lời cả 2 câu ngoài kho** ⇒ phạm luật, chưa dùng |
| Đoạn chứa đáp án nằm ngoài 5 đoạn ngữ cảnh | **Xử lý một phần** | 8.1 đo bằng đoạn đúng: **cả 22/22** câu từ chối nhầm ở 7B đều thiếu ít nhất một đoạn đúng trong 5 đoạn — gốc là khâu tìm/xếp đoạn |
| Có đủ bằng chứng mà vẫn từ chối | **Đính chính (8.1)** | Chẩn đoán 7B (theo keyword) ghi 4/22; đo lại bằng đoạn đúng: **0 câu** |
| Đưa 10 đoạn ngữ cảnh thay vì 5 | **Đã thử, chưa áp dụng** — **thắng, đã xác nhận** | 8.1: điểm Đủ +0,26 (120 câu thử) / +0,27 (56 câu kiểm); từ chối nhầm 13 → 7; 0 câu ngoài kho bị trả lời; lỗi trích dẫn không tăng; chờ bạn duyệt đưa vào chatbot |
| Xếp 5 đoạn gom theo tài liệu | **Đã thử, chưa áp dụng** | 8.1: không khác |
| Thêm 2 luật cũ của spec Phase 6 (không dùng tiêu đề làm bằng chứng; đoạn văn ngắn) | **Đã thử, chưa áp dụng** | 8.1: không khác; lỗi trích dẫn 4 → 1 (chưa đủ chắc) |
| Mức suy luận của model (`none` / `low` / `high`) | **Đã thử, chưa áp dụng** | 8.1: `none` đầy đủ hơn chút nhưng quên ghi `[n]` gấp đôi (4 → 8); `low` 4 → 9; `high` không khác, tốn hơn 11% |
| Chính sách trích dẫn "chỉ có một nguồn thì gán nguồn đó" | **Đã thử, chưa áp dụng** | 8.1 phát lại trên câu trả lời đã lưu: 0 câu đổi. (Đính chính 25/10: lỗi lúc đó **không** phải "quên `[n]`" mà là dạng `[Nguồn n]` — đã sửa, mục 4 bản 6) |
| Câu tổng hợp nhiều nguồn | **Xử lý một phần** | Lúc đóng đạt nhưng chỉ dùng 1 nguồn; chưa chứng minh tổng hợp |
| Câu hỏi giá vé + miễn giảm (bảng giá) | **Chưa thực hiện** | Không tìm ra bảng giá (xem `BAO_CAO_TIM_KIEM.md`) |
| Tách câu hỏi hai ý | **Chưa thực hiện** | Phase 8 thử |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

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
| Tối đa 5 đoạn nguyên vẹn, ngân sách 16.384 token | **còn dùng**; 8.1 đo: 10 đoạn tốt hơn, đã xác nhận — chờ bạn duyệt đổi ở 8.2 | `settings.yaml:53,56`; `backend/retrieval/full_corpus_context.py` |
| Prompt "thiếu bằng chứng thì từ chối cả câu" | **còn dùng**; 8.1 thử bản "trả lời phần có căn cứ": kém hơn (trả lời câu ngoài kho) | `backend/llm/full_corpus_prompt.py:14` |
| Không gửi mức suy luận (để model tự chọn) | **còn dùng**; 8.1: `none` / `low` làm tăng lỗi trích dẫn, `high` không khác | `backend/llm/generator_openai_full_corpus.py` |
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

Đề xuất cho Phase 8.2 (đổi chatbot cần bạn duyệt):
- **Đưa 10 đoạn ngữ cảnh vào chatbot** — cách duy nhất ở 8.1 thắng và đã xác nhận trên bộ kiểm. Tốn thêm ~50% mỗi câu
  (≈ 0,00007 USD); giới hạn: người chấm là Claude, chưa có bạn chấm mốc.
- **"Trả lời phần có căn cứ"**: hết gần sạch từ chối nhầm nhưng trả lời cả câu ngoài kho. Nếu muốn thử tiếp, cần bản prompt
  giữ được từ chối câu ngoài kho; đây cũng là đổi quy tắc của spec Phase 6 (bạn quyết).
- ~~Lỗi quên ghi `[n]`~~ — **đã sửa 25/10** (nguyên nhân thật là dạng `[Nguồn n]`, bản 6). Còn 0–2/176 câu thật sự không ghi nguồn.
- **Xem lại "suy luận `none`"** sau khi đếm lại lỗi trích dẫn (giả thuyết; thí nghiệm có phí nhỏ — hỏi bạn trước).
- Trước khi quyết theo điểm câu trả lời: nên có **20 câu bạn chấm tay** làm mốc.
- Bảng giá và tổng hợp nhiều nguồn: gốc ở khâu tìm/xếp đoạn (`BAO_CAO_TIM_KIEM.md`).

## Phụ lục — hồ sơ kỹ thuật

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
