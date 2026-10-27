# Review: Plan C59 — `/api/chat` ghi một dòng log số đo (token, thời gian theo khâu)

Decision: **changes_requested** (0 blocker / 2 major / 3 minor) — hướng đúng, nhỏ, đúng ranh giới dữ liệu; hai chỗ làm số đo sai hoặc thiếu so với chính mục tiêu "mỗi lần gọi đúng một dòng"
Người kiểm: B (Claude Opus 5.5, `hue-rag-31`) · Việc: B68 (A giao 27/10)
Date: 2026-10-27 12:08 +0700 (`date`)
Plan được review: `c59_log_token_plan.md` sha **`3cafe700ccec`** (tính từ file lúc đọc)
Theo: `practical-project-coding`, `risk-gated-agent-review`. Chỉ dựa trên mục "Căn cứ để review" của plan.

## 1. Phạm vi đã review

- Đọc hết plan.
- `backend/api/routes/chat.py` toàn bộ (`main` `a94ebc5`, 149 dòng, 9 `return`). Đọc thêm `backend/api/app.py` dòng 40–82 và 148–172 (chỗ plan dẫn, và
  chỗ đặt `retrieval_error_*`, handler lỗi chung).
- `generator_openai_full_corpus.py` dòng 35–44 (`GeneratedText`) và 186–218 (đọc usage).
- `config/logging.yaml` (logger `chat`: console + file, `propagate: no`), `core/logging_setup.py`, `.gitignore:23` (`logs/`).
- `c58_latency_theo_khau.md` §2–§4; `CURRENT_HANDOFF.md` "Cổng ổn định"; `Session_Prompt.md` §5.
- `backend/tests/test_api_chat.py` (các test hiện có).
- B1: `git diff --stat 811d25d main` và `43cdcd6..811d25d` trên `backend/api`, `backend/llm`, `test_api_chat.py`, `logging.yaml`, `logging_setup.py`.
- Chỉ đọc, 0 USD, không chạy server.

## 2. Findings

**M-1 (major) — `outcome` gắn cứng sai ở nhánh "retrieval chưa sẵn sàng" (dòng 56–67).**
- Bằng chứng: nhánh này trả mã lấy từ `state.retrieval_error_code`. Trong `api/app.py`:
  - dòng 44 / 75 / 81: `retrieval_unavailable` (503);
  - dòng **67–68**: **409 `corpus_reingest_required`** (index lệch kho).
- Plan §2.2 / §3 liệt kê 7 `outcome` cố định, không có `corpus_reingest_required`, và gán nhánh dòng 59 là "retrieval chưa sẵn sàng". Gắn cứng thì
  một lần 409 bị ghi thành `retrieval_unavailable` với `status_code` 409, tức sai nhãn đúng ở lỗi vận hành đáng chú ý nhất.
- Tiêu chí đóng: `outcome` lấy **đúng mã lỗi route trả về**. Đây là chuỗi cố định do code đặt, không phải nội dung, nên vẫn trong danh sách trắng. Ví
  dụ ở nhánh này dùng `getattr(state, "retrieval_error_code", "retrieval_unavailable")`. Bảng §3 liệt kê đủ các giá trị, gồm `corpus_reingest_required`
  và `internal_error` (M-2).
- Cũng nên tách `generation_failed` (dòng 111–119, lỗi khi gọi) khỏi `generation_unavailable` (dòng 100–107, chưa sẵn sàng). Response trả cùng mã,
  nhưng recorder đã tách hai trường hợp này, và log số đo dùng để chẩn đoán.

**M-2 (major) — "mỗi lần gọi ghi đúng một dòng" không đúng với lỗi không lường trước; 9 chỗ sửa dễ sót.**
- Bằng chứng: `app.py:161–172` có `exception_handler(Exception)` trả 500 `internal_error`. Exception không thuộc 4 lớp route bắt sẽ đi qua handler
  này, không qua `return` nào của `chat` ⇒ với `_logged` ở 9 `return` thì **không có dòng số đo**. Ví dụ lỗi trong `normalize_citations`, hay lỗi
  provider không bọc thành `GenerationError`. Đó lại là trường hợp cần số đo nhất.
- Thêm nữa, test §4 chỉ đi qua 1 / 9 `return` (503). Nếu sau này thêm một `return` mới mà quên `_logged`, test vẫn xanh.
- Cách nhỏ hơn, không thụt lề lại hàm: giữ nguyên thân hàm hiện tại dưới tên khác. Ví dụ đổi `async def chat(body, request)` thành
  `async def _answer(body, request, metrics)` và chỉ thêm các dòng điền `metrics`. Thêm một hàm `chat` mỏng có `@router.post`:

  ```python
  t0 = perf_counter(); metrics = {...}
  try:
      response = await _answer(body, request, metrics)
      metrics.update(outcome=<mã lỗi nếu JSONResponse | "success" / "refusal_no_sources">, status_code=…)
      return response
  except Exception:
      metrics.update(outcome="internal_error", status_code=500)
      raise
  finally:
      metrics["total_ms"] = …
      logger.info("chat_metrics %s", json.dumps(metrics))
  ```

  - Một điểm ghi duy nhất, nên mọi `return` hiện có và sau này đều có dòng.
  - `outcome` lấy từ `content["error"]["code"]` của `JSONResponse` (chính các chuỗi cố định ở `error_response`), nên M-1 tự đúng.
  - `raise` giữ nguyên hành vi handler chung.
  - Test §4 khi đó bảo vệ đúng điểm ghi duy nhất.
- Tiêu chí đóng: một trong hai.
  - (a) Đổi sang một điểm ghi có `finally`, như trên hoặc tương đương.
  - (b) Giữ `_logged`, nhưng ghi rõ trong plan rằng lỗi 500 `internal_error` không có dòng số đo, và vì sao chấp nhận.

  B khuyên (a): cùng cỡ diff, đúng mục tiêu hơn, không phải phòng xa vì handler 500 là đường có thật trong `app.py`.

**m-1 (minor) — test "không lọt nội dung" chạy ở nhánh câu hỏi chưa đi đâu cả.**
- Ở nhánh 503 (`retrieval_ready` False), `query` dừng ở `strip`, không vào tìm kiếm, ngữ cảnh hay sinh ⇒ chuỗi đánh dấu gần như chắc chắn không lọt.
  Test xanh nhưng bảo vệ yếu.
- Đã có sẵn test **không cần key** đi sâu hơn: `test_real_first_chunk_budget_error_has_no_partial_answer` (`test_api_chat.py:47`). Test này chạy
  lifespan thật (Qdrant, e5), câu hỏi qua `search` + `context_builder`, rồi trả 500 `context_budget_error` trước khi gọi model.
- Tiêu chí đóng: thêm kiểm "đúng một dòng `chat_metrics`, `outcome == context_budget_error`, chuỗi đánh dấu (hoặc chính câu hỏi) không có trong log"
  vào test đó, hoặc một test cùng kiểu. Nhớ dùng cách gắn `caplog.handler` vào logger `chat` như plan đã ghi (bẫy `propagate: no`).

**m-2 (minor) — khóa danh sách trắng bằng test.**
- Trong test mới, kiểm `set(json.loads(...).keys()) == {…danh sách §3…}`. Như vậy ai thêm trường mới (ví dụ `query`) vào `metrics` thì test đỏ, phải
  sửa cả danh sách trắng có chủ đích. Chi phí: một dòng.

**m-3 (minor) — cổng ổn định "log có đúng 2 dòng".**
- `logs/application.log` dùng `FileHandler` ghi nối vào cuối file, nên file đã có dòng của các lần chạy trước.
- Tiêu chí đóng: ghi rõ "đếm dòng `chat_metrics` **mới** (số dòng trước / sau, hoặc theo mốc giờ khởi động)".
- Thêm, không bắt buộc: so `total_ms` với thời gian client đo (C58: chênh ~2 ms) để kiểm đo đúng chỗ.

## 3. Trả lời năm điểm A hỏi

1. **Danh sách trắng có lọt nội dung không:** các trường §3 đều là số, bool hoặc chuỗi cố định do code đặt. `model` lấy `self.model` từ settings.
   Không có câu hỏi, câu trả lời, nguồn hay `response_id`. Plan cấm ghi `str(exc)`, đúng. Các log hiện có trong route chỉ là chuỗi cố định
   (`"Retrieval dependency error"`…). Handler 422 chỉ ghi đường dẫn. Log nằm ở `backend/logs/`, đã gitignore. ⇒ **Không lọt**, với điều kiện M-1 lấy
   `outcome` từ mã lỗi cố định (vẫn không có nội dung), còn m-1 / m-2 khóa lại bằng test.
2. **`_logged` ở 9 `return`:** không phải over-engineer (một hàm nhỏ, lý do ghi rõ). Nhưng **không phải cách nhỏ nhất đủ yêu cầu**: thiếu đường lỗi
   500 và dễ sót `return` mới (M-2). Một điểm ghi với `finally` cùng cỡ diff và đúng mục tiêu hơn.
3. **Test không key:** đủ cho "ghi đúng một dòng ở nhánh 503", **chưa đủ** cho "không lọt nội dung" (m-1) và "đúng danh sách trắng" (m-2). Đường
   thành công cần model thật, để cổng §5 kiểm là đúng (`Session_Prompt.md` §6 / §8, không mock).
4. **USD hay chỉ token: đồng ý chỉ token**, như plan và A nghiêng. Lý do:
   - log đã có `model` + `input_tokens` / `output_tokens` / `reasoning_tokens`, nên tính tiền sau bằng `full_corpus_eval.cost_usd` cho đúng giá lúc tính;
   - ghi USD vào log thì khi giá đổi, log cũ mang số sai;
   - đồng thời phải giữ giá ở hai chỗ, trái `practical-project-coding` (một nguồn sự thật).
5. **Cổng ổn định / xung đột B1:**
   - Cổng §5 đủ ý (test, server thật, khuôn phản hồi không đổi, grep câu hỏi = 0, token khớp `cost_usd`), sau khi sửa m-3.
   - **Không xung đột B1:** `git diff 811d25d main` và `43cdcd6..811d25d` trên `backend/api`, `backend/llm`, `test_api_chat.py`, `logging.yaml`,
     `logging_setup.py` đều **rỗng**. B1 chỉ đổi settings / loader / retrieval / 2 test khác.
   - Thứ tự merge (C59 trước hay sau B1) không đổi kết quả. Nếu C59 vào trước, merge B1 sau B0 vẫn sạch (B63 đã thử rebase lên `main`).

## 4. Không có giới hạn review đã biết ngoài các điểm sau

- Không chạy test hay server (plan chưa có code).
- Không kiểm SDK có thật sự trả `output_tokens_details.reasoning_tokens` cho `gpt-6-luna` hay không. Plan đã để cổng §5 ghi lại (null nếu không có),
  hợp lý.

## 5. Decision

**changes_requested.** C sửa M-1, M-2 (chọn (a) hoặc (b) kèm lý do), m-1–m-3, rồi báo sha mới ⇒ B kiểm phần sửa ⇒ A trình User.

## Vòng 2 — kiểm phần sửa (B, 2026-10-27, plan bản 2 sha `7f1456a1ae55`)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major; 2 minor mới, không mở vòng sửa riêng)
Bản kiểm: `7f1456a1ae55`, tính từ file. Bản 1 `3cafe700ccec` khớp `git show 5191c20:`. Cách kiểm: `git diff 5191c20` (toàn bộ thay đổi), đối chiếu từng tiêu
chí đóng với code `chat.py` / `app.py` ở `main`.

| Finding | Tiêu chí đóng | Bản 2 | |
|---|---|---|---|
| M-1 | `outcome` = mã thật route trả; có `corpus_reingest_required`; tách `generation_failed` | `outcome = json.loads(response.body)["error"]["code"]` cho mọi `JSONResponse`. Mọi lỗi route đều qua `error_response(...)` (B đếm: 9 `return` = 7 `return error_response(...)` ở `chat.py:51, 59, 75, 86, 103, 115, 131` + 2 `return ChatResponse` ở `:98, :149`), nên 409 `app.py:67–68` được ghi đúng. Bảng §3 đủ mã. `generation_failed` tách bằng `generation_ms` (xem (b)) | ✓ đóng |
| M-2 | một điểm ghi có `finally`, hoặc ghi rõ chấp nhận | (a) — `chat` mỏng + `_answer`; 9 `return` không sửa | ✓ đóng (xem (a)) |
| m-1 | kiểm lọt nội dung ở test đi sâu | mở rộng `test_real_first_chunk_budget_error_has_no_partial_answer` (lifespan thật, qua search + context, 500 trước model): đúng một dòng mới, đúng `outcome`, câu hỏi không có trong log `chat` | ✓ đóng |
| m-2 | khóa tập khóa | `set(keys) == METRIC_FIELDS` | ✓ đóng |
| m-3 | đếm dòng mới | cổng §5 đếm dòng mới (trước / sau hoặc mốc giờ) + so `total_ms` với client | ✓ đóng |

**(a) `chat` mỏng có giữ nguyên hành vi trả về và handler 500 chung không — có.**
- `try` lấy `response` rồi `return response`. `finally` chạy trước khi giá trị trả ra, và không đổi `response`.
- Exception từ `_answer` đi vào `except Exception`, gán `internal_error` / 500, rồi `raise` nguyên exception. `finally` ghi log, rồi exception đi tiếp tới
  `exception_handler(Exception)` ở `app.py:161–172` như hiện nay (cùng 500, cùng thông điệp).
- `RequestValidationError` vẫn xảy ra trước khi gọi route, nên đúng như plan: không có dòng.
- `chat` giữ tham số `body: ChatRequest, request: Request` và `@router.post(..., response_model=ChatResponse)`. `ChatResponse` trả từ `_answer` vẫn được
  FastAPI kiểm như cũ; `JSONResponse` đi thẳng. ⇒ Phản hồi API không đổi.
- **m-4 (minor, ghi khi code):** đoạn suy `outcome` nằm **trong** `try`. Nếu chính nó ném lỗi, ví dụ đọc `response.body` sai kiểu, thì một phản hồi đúng sẽ
  thành 500 `internal_error`. Tương tự, `json.dumps(metrics)` trong `finally` mà ném lỗi thì sẽ thay giá trị trả về. Rủi ro thực tế thấp: `body` là
  bytes JSON do chính `error_response` tạo, và mọi giá trị là int / float / str / bool / None. Nhưng nguyên tắc là **log không được đổi phản hồi**.
  - Cách giữ đơn giản: chỉ đặt giá trị kiểu thường vào `metrics` (`round(...)` ra float, token là int).
  - Kiểm ở cổng §5: phản hồi 200 thật vẫn đúng khuôn. Đường thành công là nơi duy nhất test không key không chạm.
  - Không cần thêm `try` bọc phòng xa.
- Ghi chú (không phải finding): `asyncio.CancelledError` (client ngắt) là `BaseException`, không vào `except Exception`. `finally` vẫn ghi một dòng với
  `outcome` = null — chấp nhận được và thật hơn là đoán.

**(b) Phân biệt `success` / `refusal_no_sources` / `generation_failed` bằng `generation_ms` — đúng hôm nay, nhưng dựa vào suy diễn ⇒ m-5 (minor).**
- Đúng theo code hiện tại:
  - `refusal_no_sources` là nhánh `chat.py:95–98`, trả trước khi gọi model, nên `generation_ms` = None.
  - `success` là `ChatResponse` sau `generate_answer`, nên `generation_ms` có số. Câu từ chối do model viết vẫn là `success` + `refusal: true`, đúng ý §3.
  - `generation_failed` là 502 sau khi đã gọi `generate_answer`: plan đặt `generation_ms` cả khi `GenerationError`. Còn `generation_unavailable` là 502
    ở `chat.py:100–107`, trước khi gọi, nên `generation_ms` = None.
- Dễ vỡ ở chỗ: nhãn được **suy** từ việc một trường thời gian có được đặt hay không. Sau này ai đổi chỗ đo `generation_ms` (ví dụ đặt sớm hơn, hoặc đặt cả ở
  nhánh "chưa sẵn sàng") thì nhãn sai mà không test nào đỏ: hai test không key đều không đi qua ba nhánh này.
- Cách trực tiếp hơn, cùng cỡ: trong `_answer`, gán thẳng `metrics["outcome"] = "refusal_no_sources"` ngay trước `return` ở dòng 98, và
  `metrics["outcome"] = "generation_failed"` trong `except GenerationError` (dòng 111). Đây là thêm dòng, **không sửa `return`**. Wrapper chỉ điền `outcome`
  từ `error.code` / `"success"` khi chưa có. Nhãn đặt đúng tại nhánh, nên đọc là thấy, không phải suy.
- Không chặn. C chọn khi code; nếu giữ cách suy thì thêm một dòng comment nói `generation_ms` là căn cứ phân loại.

**Ngoài phạm vi:** không có. Phần thêm `total_ms` so với client là từ gợi ý của B68 m-3. Danh sách trắng chỉ thêm giá trị `outcome`, không thêm trường.

⇒ Plan bản 2 đủ để A trình User duyệt (sha `7f1456a1ae55`). m-4 / m-5 ghi lại cho lúc code và review code.
