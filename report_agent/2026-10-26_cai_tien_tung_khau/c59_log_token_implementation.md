# Implementation Report: C59 / C60 — `/api/chat` ghi một dòng log số đo mỗi câu (token, thời gian theo khâu)

Người làm: C (Claude Opus 5.5, `hue-rag-5b`) · 2026-10-27 13:12 +0700 (`date`) · Việc: C60 (A giao sau khi User duyệt plan C59).
Plan: `report_agent/2026-10-26_cai_tien_tung_khau/c59_log_token_plan.md` bản 2 sha **`7f1456a1ae55`** (C tính lại từ file trên `main` `2ddd65d` trước khi code: khớp),
review B68 vòng 1–2 + hai minor ghi khi code (m-4, m-5). Theo skill `practical-project-coding`. Nhánh `c59-log` từ `2ddd65d`, **không merge `main`**.
**Tiền thật: 0,0003236 USD** (cổng ổn định, 2 câu; token do chính dòng log ghi). Trạng thái: **chờ review** (B).

File này không chép câu hỏi, câu trả lời hay nội dung kho.

## Cho bạn (3 dòng)

- Từ giờ mỗi câu hỏi tới chatbot để lại **một dòng số đo** trong log: số token đọc / viết / suy luận, số nguồn, thời gian từng khâu. **Không** ghi câu hỏi, câu trả lời hay nội dung kho.
- Câu trả lời người dùng nhận **không đổi** (đã kiểm trên server thật). Phần ghi log gần như không tốn thời gian (tổng trừ các khâu ≈ 0,1 ms ở câu đo trên server thật).
- Nhờ vậy tiền và tốc độ thật qua API đo được trực tiếp, không phải ước như trước (lần đo B65 / C58).

## 1. Thay đổi (3 file, đúng plan)

`git diff --stat 2ddd65d..c59-log` (phần code): `backend/api/routes/chat.py` +54, `backend/llm/generator_openai_full_corpus.py` +5, `backend/tests/test_api_chat.py` +46 / −3.
Không dòng nào của `chat.py` bị xóa (chỉ thêm).

- **`generator_openai_full_corpus.py`:** `GeneratedText.reasoning_tokens: int | None = None` (trường cuối, có mặc định); đọc
  `usage.output_tokens_details.reasoning_tokens` bằng `getattr` lồng (thiếu ⇒ None).
- **`chat.py`:**
  - `METRIC_FIELDS` — danh sách trắng 15 trường (plan §3).
  - Thân hàm cũ đổi tên thành `_answer(body, request, metrics)`, **không sửa `return` nào**; chỉ thêm dòng điền `metrics` quanh tìm kiếm (`search_ms`, `dense_ms` từ trace sẵn có),
    dựng ngữ cảnh (`context_ms`, `n_context_sources`), sinh (`generation_ms`, `model`, token), kiểm citation (`citation_ms`, `n_cited_sources`).
  - Hàm `chat` mỏng mang `@router.post`: `try` gọi `_answer` rồi điền `status_code`, `refusal`, `outcome` (lấy `error.code` của `JSONResponse` hoặc `success`) / `except Exception`
    ⇒ `internal_error`, 500, `raise` (handler chung `app.py` giữ nguyên) / `finally` ⇒ `total_ms` + **một** `logger.info("chat_metrics %s", json.dumps(metrics))`.
- **Khác plan bản 2 — theo minor của B68 vòng 2, ghi khi code:**
  - **m-5:** nhãn `refusal_no_sources` và `generation_failed` gán **thẳng tại nhánh** trong `_answer` (trước `return` từ chối không nguồn; trong `except GenerationError`), wrapper chỉ
    điền `outcome` khi chưa có — thay cho cách suy từ `generation_ms` trong đoạn mã mẫu của plan.
  - **m-4 ("log không được đổi phản hồi"):** mọi giá trị trong `metrics` là int / float / str / bool / None. Thêm một chỗ: token và `model` đọc bằng `getattr(generated, field, None)` như
    `EvidenceRecorder` — xem mục 3, đây là chỗ code ban đầu **đã** làm đổi phản hồi trong một test.

## 2. Cách đã chạy thật

Worktree `/tmp/c_c59` (nhánh `c59-log`), symlink `data/` + `knowledge-base-hue/` tạm; mọi lệnh `uv run --project /home/minhhieu/hue_rag` từ `backend/`.

**Test** (liệt kê đúng file chạm, không `--env-file`):

```bash
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_api_chat.py tests/test_openai_full_corpus_generator.py tests/test_phase6_live_smoke.py -q -p no:cacheprovider
```

| Lượt | Kết quả |
|---|---|
| Mốc trước khi sửa (`2ddd65d`) | 31 passed, 4 errors |
| Sau khi sửa | **32 passed, 4 errors** (+1 test mới) |

4 errors giống hệt mốc, đều do thiếu key (C-17, `conftest.py:33` "OPENAI_API_KEY is not set"): `test_health_is_cached_and_ready_after_real_lifespan`,
`test_real_environment_builds_openai_generator`, `test_empty_or_blank_input_rejected_before_network`, `test_async_client_with_lifespan_context_has_health_ready`.

**Test mới / mở rộng** (`test_api_chat.py`; gắn thẳng `caplog.handler` vào logger `chat` vì `propagate: no` sau `setup_logging()`):
- `test_real_first_chunk_budget_error_has_no_partial_answer` (mở rộng, không key, lifespan thật — câu hỏi đi qua tìm kiếm + dựng ngữ cảnh rồi trả 500): đúng **1** dòng `chat_metrics`,
  `set(keys) == METRIC_FIELDS`, `outcome == "context_budget_error"`, `search_ms` / `dense_ms` là số, token None, **câu hỏi không có trong log** của logger `chat`.
- `test_chat_metrics_logged_when_retrieval_not_ready` (mới, không lifespan ⇒ 503): đúng 1 dòng, `outcome == "retrieval_unavailable"`.
- **Thử ngược:** tạm thêm `metrics["query"] = body.query` ⇒ test mở rộng **đỏ** đúng chỗ (`Extra items in the left set: 'query'`); trả code về, `grep` xác nhận đã gỡ.
- 500 `internal_error` (exception lạ): không dựng lỗi giả (`Session_Prompt.md` §8) ⇒ **kiểm bằng đọc code** (nhánh `except` + `finally`), không chạy.

**Cổng ổn định** (server thật `HF_HUB_OFFLINE=1 uv run --project … --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8014`, context 5 như `main`; 8011 bị tiến trình
khác chiếm):
- `/` 200; `/health` 5 / 5 ready.
- 2 câu tự viết, không Golden: câu trong kho ⇒ 200, khóa phản hồi `["answer", "sources"]`, 2 nguồn (khóa nguồn `excerpts, heading_path, id, title` — như cũ); câu ngoài kho ⇒ 200, câu
  từ chối chuẩn, 0 nguồn. **Khuôn phản hồi không đổi.**
- Dòng `chat_metrics` trong `backend/logs/application.log` của worktree: trước **17** (từ các lượt pytest), sau **19** ⇒ **2 dòng mới**, đủ 15 trường. Hai dòng: `outcome success`,
  `status 200`, `refusal` false / true, `model gpt-6-luna`, token vào 869 / 1.332, ra 149 / 58, **suy luận 65 / 25** (provider có trả `output_tokens_details`), nguồn ngữ cảnh 5 / 5,
  nguồn trích 2 / 0, tìm 43 / 29 ms (dense 40 / 25), ngữ cảnh 1,6 / 1,5 ms, sinh 3.612 / 1.647 ms, citation 0,1 / 0,0 ms, tổng 3.657 / 1.678 ms.
- `total_ms` so thời gian client: 3.657 / 3.662 và 1.678 / 1.679 ms ⇒ chênh 1–4 ms (đo đúng chỗ; C58: ~2 ms).
- `grep -F` hai câu hỏi trong `application.log` và log server: **0** lần. Log server: 0 dòng `error` / `Traceback`.
- Tiền: (869 + 1.332) × 0,1 + (149 + 58) × 0,5 USD / 1M = **0,0003236 USD**.
- Không chạm tìm kiếm / chia đoạn ⇒ không chạy T1 (plan §5.3).

## 3. Lỗi gặp khi làm và cách sửa (một sửa, đúng nguyên nhân)

- **Quan sát:** lượt test đầu sau khi sửa ⇒ `test_chat_returns_bracket_citations_when_model_writes_nguon_label` **từ đạt thành hỏng** (500 `internal_error`).
- **Nguyên nhân (đọc traceback):** test đó thay generator bằng một đối tượng chỉ có `text` (kiểm logic route, không gọi OpenAI). Code ban đầu đọc `generated.model` / `.input_tokens`
  trực tiếp ⇒ `AttributeError` ⇒ log làm **đổi phản hồi** — đúng điều B68 m-4 cấm. Trước khi sửa, route chỉ đòi `generated.text`.
- **Sửa:** đọc 4 trường bằng `getattr(generated, field, None)` (cùng cách `EvidenceRecorder.record_generation_result`). Chạy lại: test đó đạt, tổng 32 passed. Không sửa test.

## 4. Tự kiểm

- `git diff --check` sạch; diff chỉ 3 file trong plan; không đổi `return` nào của route; không đụng file ngoài plan.
- Danh sách trắng: không câu hỏi, câu trả lời, nguồn, `chunk_id`, `response_id`, `str(exc)`, USD. `model` là `generated.model` (`gpt-6-luna`).
- Không xung đột B1 (`p82-b1` không chạm `chat.py` / generator / `test_api_chat.py` — B68 đã kiểm).

## 5. Giới hạn

- Đường 500 `internal_error` chỉ kiểm bằng đọc code. Đường `generation_failed` / `citation_integrity_error` / 409 chưa chạy thật (không có lỗi thật để tạo; `outcome` lấy từ `error.code`
  cố định nên đọc code thấy đúng).
- `FileHandler` không xoay vòng (như hiện nay) — ~400 byte / câu; xem lại khi deploy (plan §6).
- Cổng chạy ở context 5; với context 10 (B1) cùng code route.

## 6. Bàn giao cho người kiểm (B)

- `git diff 2ddd65d..c59-log` (3 file code + report). Đối chiếu plan §2–§5 + m-4 / m-5.
- Kiểm lại 0 USD: chạy 3 file test như mục 2 (kỳ vọng 32 passed / 4 errors cần key); thử ngược thêm trường lạ vào `metrics` ⇒ test mở rộng đỏ.
- Dữ liệu cổng (private): `data/phase_8_2/c60_gate/{server.log, client.json}`.
