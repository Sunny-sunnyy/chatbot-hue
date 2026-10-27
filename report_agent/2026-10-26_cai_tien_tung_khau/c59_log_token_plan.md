# Plan C59: `/api/chat` ghi một dòng log số đo (token, thời gian theo khâu) cho mỗi câu — không ghi nội dung

Người viết: C (Claude Opus 5.5, `hue-rag-5b`) · 12:03 27/10/2026 +0700 (`date`) · Việc: C59 (A giao). Theo skill
`practical-project-coding`. Trạng thái: **bản nháp chờ B review**, rồi A trình User duyệt (đổi code `main`). **Chưa sửa code; 0 USD lúc viết.**

## Căn cứ để review

1. `backend/api/routes/chat.py` — **toàn bộ** (một hàm `chat`, mọi nhánh `return`).
2. `backend/llm/generator_openai_full_corpus.py` **dòng 35–44** (`GeneratedText`) và **186–218** (đọc usage từ `raw_responses[-1].usage`); `backend/core/logging_setup.py`
   và `backend/config/logging.yaml` (logger `chat` → console + `backend/logs/application.log`; `.gitignore:23` bỏ `logs/`).
3. `report_agent/2026-10-26_cai_tien_tung_khau/c58_latency_theo_khau.md` §2–§4 (vì sao cần: thời gian nằm ở bước sinh, theo token ra; route hiện không ghi usage).
4. `session_prompt/CURRENT_HANDOFF.md` mục "Cổng ổn định sau mỗi gói" và `Session_Prompt.md` §5 (không ghi nội dung câu hỏi / kho / secret).

Người review được chạy lệnh chỉ đọc (đọc code, `git grep`, chạy test không key).

## 1. Vấn đề và mục tiêu

- **Quan sát:** route `/api/chat` không ghi token hay thời gian ⇒ mọi số tiền / tốc độ qua API đều phải **ước** (B65) hoặc **đo tạm** trong worktree (C58). Usage mà generator
  đã có (`GeneratedText.input_tokens`, `output_tokens`, `latency_ms`) bị bỏ đi sau khi trả lời; token **suy luận** chưa được đọc dù SDK có (`agents/usage.py`:
  `output_tokens_details.reasoning_tokens`).
- **Mục tiêu:** mỗi lần gọi `/api/chat` ghi **đúng một dòng** `chat_metrics {json}` vào logger `chat` sẵn có. Không đổi phản hồi API, không đổi hành vi, không thêm hạ tầng.

## 2. Đổi gì (file:dòng ở `main` `a94ebc5`)

### 2.1 `backend/llm/generator_openai_full_corpus.py`

- `GeneratedText` (dòng 35–44): thêm trường cuối `reasoning_tokens: int | None = None` (có mặc định ⇒ chỗ dựng khác, `tests/test_phase6_live_smoke.py:268`, không phải sửa).
- Đọc usage (dòng ~196–200): thêm `reasoning_tokens = getattr(getattr(usage, "output_tokens_details", None), "reasoning_tokens", None)` và truyền vào `GeneratedText`
  (dòng 209). Không đổi `input_tokens` / `output_tokens` (output đã **gồm** token suy luận; trường mới chỉ tách phần đó ra).

### 2.2 `backend/api/routes/chat.py`

- Đầu hàm `chat` (dòng 49): `t0 = time.perf_counter()`; dict `metrics` các trường ở §3.
- Ghi mốc thời gian quanh 4 bước đã có, **không đổi thứ tự hay lời gọi**: `retrieval_service.search` (dòng 70), `context_builder.build` (dòng 82), `generate_answer`
  (dòng 110), `normalize_citations` + `select_cited_sources` (dòng 124–126). Lấy thêm `result.trace.timings_ms["dense_ms"]` (nhúng câu hỏi e5 + Qdrant — số đã có sẵn).
- Một hàm nhỏ trong file: `def _logged(response, metrics, outcome, t0)` — điền `outcome`, `status_code`, `total_ms`, gọi `logger.info("chat_metrics %s", json.dumps(metrics))`
  rồi trả `response`. **Không** ghi 422 do `RequestValidationError` (`api/app.py:149-160`, route không chạy — không có token / thời gian để ghi; handler đó đã log `Invalid API request`). **Mọi** `return` của `chat` (9 chỗ — dòng 51, 59, 75, 86, 98, 103, 115, 131, 149: 422 sau `strip` (gần như không tới được, vì `ChatRequest` đã `str_strip_whitespace` + `min_length=1`), retrieval chưa sẵn sàng, lỗi retrieval 503, ngân sách context 500, không có nguồn ⇒ từ chối không gọi
  model, generator chưa sẵn sàng 502, lỗi sinh 502, lỗi citation 500, thành công 200) đổi thành `return _logged(<response cũ>, metrics, "<mã>", t0)`. Lý do chọn cách
  này thay vì `try/finally` bọc cả hàm: diff nhỏ từng dòng, không thụt lề lại toàn hàm, mỗi nhánh vẫn đọc thẳng.
- Không dùng `EvidenceRecorder` (`llm/evidence_recorder.py`): recorder đó lưu **nguyên văn đoạn trích** (`sources[].excerpts`) và chỉ bật trong smoke test.

## 3. Ghi trường nào — danh sách trắng (whitelist)

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `outcome` | chuỗi cố định | `success` / `refusal_no_sources` / `invalid_request` / `retrieval_unavailable` / `context_budget_error` / `generation_unavailable` / `citation_integrity_error` |
| `status_code` | số | mã HTTP trả về |
| `refusal` | bool / null | câu trả lời 200 có đúng là câu từ chối chuẩn không (`answer.strip() == INSUFFICIENT_ANSWER`); null khi không có câu trả lời |
| `model` | chuỗi | `generated.model` (`gpt-6-luna`) |
| `input_tokens`, `output_tokens`, `reasoning_tokens` | số / null | từ usage provider; null khi không gọi model hoặc lỗi trước khi có usage |
| `n_context_sources`, `n_cited_sources` | số / null | chỉ số đếm |
| `search_ms`, `dense_ms`, `context_ms`, `generation_ms`, `citation_ms`, `total_ms` | số (1 chữ số thập phân) | `total_ms` = từ đầu hàm tới trước `return`; `generation_ms` là thời gian tường quanh `generate_answer` (gồm mạng) |

**Không ghi:** câu hỏi, câu trả lời, tiêu đề / mục / đoạn trích nguồn, `chunk_id`, tên file kho, `response_id`, nội dung exception, header / IP / API key. Chỉ có
chuỗi `outcome` cố định — không ghi `str(exc)` (thông điệp lỗi có thể chứa nội dung). Không tính USD trong log (giá đổi thì log sai); tiền tính sau bằng
`full_corpus_eval.cost_usd` từ token.

**Ghi ở đâu:** logger `chat` sẵn có ⇒ console của uvicorn + `backend/logs/application.log` (`logging.yaml`, đã gitignore). Không thêm handler, file, DB hay cấu hình.

## 4. Test bảo vệ hành vi

- **Mới, không cần key (1 test, `backend/tests/test_api_chat.py`):** `TestClient(create_app(load_settings()))` **không** chạy lifespan (như `test_invalid_requests_use_typed_vietnamese_envelope`) ⇒
  `retrieval_ready` False ⇒ route trả 503 `retrieval_unavailable` mà không gọi Qdrant / model. Gửi `query` hợp lệ chứa một chuỗi đánh dấu; dùng `caplog` bắt logger `chat`: đúng
  **một** dòng `chat_metrics`, JSON parse được, `outcome == "retrieval_unavailable"`, `status_code == 503`, và **chuỗi đánh dấu không xuất hiện** trong bất kỳ dòng log nào. Bẫy: test khác chạy lifespan sẽ gọi `setup_logging()` ⇒ logger `chat` có `propagate: no` (`logging.yaml`) ⇒ `caplog` (gắn ở root)
  không thấy gì; test gắn thẳng `caplog.handler` vào `logging.getLogger("chat")` (gỡ khi xong) để không phụ thuộc thứ tự test. Bảo
  vệ hai điều quan trọng nhất: luôn ghi đúng một dòng, và không lọt nội dung câu hỏi.
- **Không viết test riêng cho đường thành công** (cần model thật): kiểm bằng cổng ổn định §5 trên server thật.
- Chạy lại file test chạm tới: `test_api_chat.py` (phần không key), `test_openai_full_corpus_generator.py` (bộ test cần key — chỉ chạy khi việc cho phép, theo `Project_Status.md` §8),
  `test_phase6_live_smoke.py` (dựng `GeneratedText` — trường mới có mặc định nên không vỡ). Lỗi cũ C-17 (thiếu key) ghi rõ.

## 5. Cổng ổn định (theo `CURRENT_HANDOFF.md`)

1. Test các file chạm (mục 4).
2. Server thật từ `backend/`: `HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8014` (8011 đang bị tiến trình khác chiếm): `/` 200, `/health` 5 / 5 ready,
   1 câu trong kho (200, có `sources`) + 1 câu ngoài kho (từ chối) — câu tự viết, không Golden. Kiểm:
   - phản hồi JSON **giống khuôn cũ** (`answer`, `sources`), không thêm trường;
   - log có đúng **2** dòng `chat_metrics`, mỗi dòng có đủ trường §3; câu trong kho có `output_tokens` > 0 và `reasoning_tokens` là số (hoặc null nếu provider không trả — ghi lại);
   - `grep` hai câu hỏi đã gửi trong `application.log` ⇒ **0** lần xuất hiện;
   - tổng `input_tokens` / `output_tokens` khớp với số đo được bằng `cost_usd` (tiền thật cổng ≈ 0,0003 USD).
3. Không chạm tìm kiếm / chia đoạn ⇒ không cần T1 (ghi lý do).
4. Hành vi người dùng không đổi ⇒ chỉ ghi một dòng ở `LUONG_HOAT_DONG_HE_THONG.md` / `BAO_CAO_SINH_CAU_TRA_LOI_API.md` (A quyết).
5. Hook pre-commit quét trùng; A commit + push.

## 6. Rủi ro và cách giảm

| Rủi ro | Giảm |
|---|---|
| **Lộ nội dung** (câu hỏi, kho, câu trả lời) vào log | Danh sách trắng §3; không ghi `str(exc)`; test §4 kiểm chuỗi đánh dấu không lọt; cổng §5 grep câu hỏi = 0. Log ở `backend/logs/` đã gitignore |
| **Chậm thêm** | Chỉ vài `perf_counter`, một `json.dumps` dict ~15 trường, một dòng log (< 1 ms; C58: kiểm citation + dựng phản hồi ~0 ms, bước sinh 2–5 s). Cổng §5 so `total_ms` với thời gian client |
| **File log phình** | ~350 byte / câu ⇒ ~0,35 MB / 1.000 câu; `FileHandler` không xoay vòng (như hiện nay — file đang 100 KB). Chưa thêm xoay vòng (phòng xa); ghi lại ngưỡng xem lại: khi chạy cho người dùng thật / deploy |
| Lệch nhánh B1 (`p82-b1`, chờ merge sau B0) | B1 không chạm `chat.py` / generator (`git diff 811d25d main` chỉ khác settings, loader, retrieval) ⇒ không xung đột |
| Provider không trả `output_tokens_details` | `getattr` lồng ⇒ `null`, không lỗi; cổng §5 ghi lại giá trị thật |

## 7. Ngoài phạm vi (không làm)

Tính USD trong log; xoay vòng log; dashboard / DB; ghi trace retrieval chi tiết; đổi `EvidenceRecorder`; đổi phản hồi API; streaming.
