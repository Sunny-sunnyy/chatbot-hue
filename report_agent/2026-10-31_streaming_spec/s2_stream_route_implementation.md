# Implementation Report: Streaming S2 — route `POST /api/chat/stream` (SSE)

Người làm: B (Claude Opus 5.5)
Date: 11:18 01/11/2026 (`date`)
Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md` (User duyệt `00fb57ee01b2`); mục việc `CURRENT_HANDOFF.md` "B — S2 streaming".
Nhánh: `s1-loi-chung` (giữ tên, nối sau S1 `9c83003`), commit **`830df0e`**, đã push `origin`. Worktree `/tmp/b_s1`. Không merge `main` (tới hết S4 — A).

## 1. Phạm vi

Đã làm hàng S2 (spec §5): generator stream + bộ bóc chữ JSON từng phần + chuẩn hóa `[Nguồn n]` từng phần + route `/api/chat/stream` + log `chat_metrics`; `fastapi>=0.135`.
Không làm: giao diện (S3), đo D2 trên trình duyệt (S4), `cost_usd`, prompt / model / settings, Qdrant.

## 2. Thay đổi chính

| File | Đổi gì |
|---|---|
| `backend/llm/generator_openai_full_corpus.py` | `start_answer_stream(query, context)` = `Runner.run_streamed` với **cùng** `answer_agent` + cùng `max_turns=1` + cùng `RunConfig` (`_run_config()`, dùng chung với `Runner.run`); `finish_answer_stream(result, started)` = `parse_structured_output` + usage như đường cũ (phần đọc usage tách thành `_generated_text`, hai đường cùng gọi). Hạn giờ + `cancel()` do nơi gọi giữ |
| `backend/llm/answer_stream.py` (mới) | `decode_partial_string` (đưa từ C73 `hoso/c70-ttft`, không thêm thư viện); `displayable_prefix` giữ lại đuôi `[…` còn có thể thành citation; `AnswerTextStream.feed(delta)` trả **phần chữ mới** đã chuẩn hóa — chữ đã gửi không bao giờ phải sửa, ghép lại = `normalize_citations(chữ trong JSON)` |
| `backend/llm/grounded_answer.py` | tách `prepare_answer` (tìm → ngữ cảnh → từ chối nếu rỗng / `GeneratorNotReadyError`) và `check_citations` khỏi `answer_query`; `answer_query` = hai hàm đó + sinh (hành vi S1 giữ nguyên) |
| `backend/api/routes/chat.py` | route JSON giữ đúng luồng S1, chỉ tách 3 hàm dùng chung cho hai route: `_retrieval_not_ready`, `_error_response_for` (4 lớp lỗi ⇒ mã + thân), `_set_outcome`. Route stream: lỗi trước luồng ⇒ JSON qua **cùng** các hàm đó + log ở handler (cách (b)); qua ⇒ `StreamingResponse(media_type="text/event-stream", Cache-Control: no-cache, X-Accel-Buffering: no)`. `StreamEvents` dựng sự kiện + điền `outcome` (logic thuần, test được); `_answer_events` nối nó với luồng model: hạn giờ 45 s **chung cho cả vòng đọc** (`asyncio.timeout_at`), bắt mọi `Exception` ⇒ `error` + `done`, ngắt (`CancelledError` / `GeneratorExit`) ⇒ raise lại; `finally`: ghi `chat_metrics` **trước mọi `await`**, rồi khi tự dừng đọc sớm (ngắt / hết giờ) ⇒ `result.cancel()` + đọc nốt bằng iterator mới trong `anyio.CancelScope(shield=True)` + `move_on_after(0,5 s)`, ghi dòng `chat_stream_drain` |
| `backend/tests/test_chat_stream.py` (mới, 14 test) | logic thuần §7: bóc chữ (tiền tố JSON, `\uXXXX` cắt giữa mảnh, `\"` + `\n` cắt mảnh), `[Nguồn n]` giữ tới `]`, ngoặc không thể thành citation hiện ngay, 300 cách cắt ngẫu nhiên (seed cố định) ⇒ ghép = chữ cuối chuẩn hóa; chuỗi sự kiện (thứ tự, `seq`, chỉ nguồn được trích, D3 (a) không `[n]` / số sai ⇒ `error{after_text:true}` không `sources`, từ chối có / không gọi model, lỗi bất kỳ ⇒ `error` + `done` + `outcome` đúng); định dạng SSE |
| `pyproject.toml`, `uv.lock` | `fastapi>=0.115.0` ⇒ `>=0.135` (`uv add --no-sync`, lock chỉ đổi đúng dòng cận dưới; bản cài 0.141.1 không đổi) |

**Sự kiện (spec §4.4):** `status{stage:"searched", n_sources}` → `status{stage:"generating"}` → `delta{seq, text}`… → `sources[...]` (chỉ nguồn được trích) **hoặc** `error{code, message,
after_text}` → `done{outcome}`. Từ chối trước model: `status` → `delta` câu chuẩn → `sources []` → `done`. Mã lỗi dùng lại: `generation_unavailable` (lỗi sinh / hết giờ / `incomplete`),
`citation_integrity_error` (D3 (a)), `internal_error` (lỗi lạ).

**Log (spec §4.6):** route stream dùng `STREAM_METRIC_FIELDS` = 15 trường cũ + `first_event_ms`, `first_text_ms` + **`delta_matches_final`** (cờ đúng / sai, không chứa chữ — B thêm để đo C5 từ
log; spec chỉ nêu 2 trường mới ⇒ **A xét**). Route JSON giữ đúng 15 trường (test khóa tập trường không đổi). `outcome` mới: `retracted`, `stream_error_after_text`, `client_disconnected`;
lỗi trước chữ đầu dùng `generation_failed` / `internal_error` như route JSON. Dòng phụ `chat_stream_drain {"finished", "ms"}` chỉ ở ca tự dừng đọc sớm (C7).

**m-1 review S1:** `git grep 'raise (RetrievalDependencyError|ContextBudgetError|GeneratorNotReadyError|GenerationError)'` (trừ test): `RetrievalDependencyError` chỉ ở `retrieval/full_corpus.py`
+ `reranking/cross_encoder.py` (bước tìm); `ContextBudgetError` chỉ `retrieval/full_corpus_context.py:98`; `GenerationError` chỉ generator (gồm `parse_structured_output` — trong route stream nó
chạy **trong** `gen()` ⇒ thành sự kiện `error`); `GeneratorNotReadyError` chỉ `grounded_answer.py:70` ⇒ mỗi lớp vẫn chỉ ở đúng bước của nó.

## 3. Cách đã chạy thật

Từ `/tmp/b_s1/backend`, `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`, `--env-file /home/minhhieu/hue_rag/.env` (khi cần). Dữ liệu: `data/streaming_s1_2026-11-01/s2/` (private:
thân SSE `*.sse`, dòng log `c4_metrics.log`, `c5_metrics.log`, `log_tail_cuts_pilot.log`), công cụ `data/streaming_s1_2026-11-01/tools/{run_server.py, summarize_sse.py}`.

1. Test: `python -m pytest tests/test_chat_stream.py tests/test_grounded_answer.py tests/test_api_chat.py tests/test_full_corpus_eval.py tests/test_citations.py tests/test_phase6_live_smoke.py
   tests/test_openai_full_corpus_generator.py tests/test_static_ui.py -q` (có key; các test này **không** gọi model — test generator dùng `monkeypatch` / chặn trước mạng).
2. T1: `python -m evaluation.full_corpus_eval retrieval --out ../data/streaming_s1_2026-11-01/t1_branch_s2.jsonl`.
3. Cổng ổn định C4 cả hai route: `uvicorn api.app:app --port 8765` (production); `/`, `/health`; thân rỗng / 501 ký tự lên route stream; mỗi route 1 câu trong kho + 1 câu ngoài kho (tự viết);
   `curl -N` lưu thân SSE; đếm `chat_metrics` mới (mốc ngay trước); `grep -cF` câu hỏi trong log; tắt server.
4. C5: thêm 3 câu stream tự viết (1 câu món ăn, 1 câu giờ mở cửa, 1 câu so sánh) ⇒ cùng 2 câu stream của C4 = 5 câu.
5. Ngắt thật 2 thời điểm bằng `curl --max-time`: 0,8 s (trước chữ đầu) và 3,8 s (giữa chừng, câu so sánh dài).
6. Pilot `incomplete`: `run_server.py --port 8766 --max-output-tokens 250`, rồi `60` (đổi trong bộ nhớ, không sửa `settings.yaml`), mỗi trần 1 câu so sánh dài.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Test file chạm | **PASS** 82 passed (14 mới). 0 lần gọi model |
| T1 158 câu | **PASS** `4d5bbe9e0edc` (giống byte mốc) |
| C4 cổng ổn định | **PASS** — `/` 200, `/health` 5 / 5; route stream: thân rỗng / quá dài ⇒ 422 thân `invalid_request`, **0** dòng log (đúng: trước handler); 4 câu ⇒ **4** dòng `chat_metrics`; câu hỏi trong log **0 / 4**; header `text/event-stream; charset=utf-8`, `cache-control: no-cache`, `x-accel-buffering: no`. JSON: trong kho trích `[1]`, `[8]` ⇔ nguồn 1, 8; ngoài kho từ chối. Stream: trong kho `status, status, delta×178, sources, done{success}`, số trích trong chữ = id nguồn (3, 4, 5, 7), không còn chữ "Nguồn"; ngoài kho `delta×19` câu từ chối, `sources []`, `refusal: true` |
| C5 (≥ 5 câu) | **PASS** 5 / 5 `delta_matches_final: true`; cả 5: `seq` liên tục, số trích trong chữ = id trong `sources` (cùng luật route JSON), 2 câu từ chối có `sources []` |
| C7 ngắt trước chữ đầu (0,8 s) | **PASS** — client nhận `status, status`; **1** dòng `outcome: client_disconnected`, token `None`, `first_text_ms: null`; `chat_stream_drain {"finished": true, "ms": 0.7}` |
| C7 ngắt giữa chừng (3,8 s) | **PASS** — client nhận `delta×28`, không `done`; **1** dòng `client_disconnected`, token `None`, `first_text_ms` 3.598,7; drain `finished: true`, 0,5 ms |
| Pilot `incomplete` trần 250 | **quan sát ca sau chữ đầu** — `delta×3` rồi `error{generation_unavailable, after_text: true}` + `done{stream_error_after_text}`; log `Answer stream failed: ModelBehaviorError` (SDK ném khi gặp `response.incomplete`) |
| Pilot `incomplete` trần 60 | **quan sát ca trước chữ đầu** — 0 delta, `error{…, after_text: false}` + `done{generation_failed}` (hết token trong phần suy luận) |
| `git diff --check`; hook | sạch; hook quét 7 file ⇒ 0 trùng |

**Chạy hỏng rồi sửa (giữ hồ sơ):** lượt ngắt đầu tiên có dòng `client_disconnected` nhưng **không** có dòng drain: SDK tự `cancel()` (đặt `is_complete = True`) khi lần chờ sự kiện bị hủy
(`agents/result.py` `stream_events`, nhánh `except asyncio.CancelledError`) ⇒ điều kiện cũ `not result.is_complete` bỏ qua bước đọc nốt. Model vẫn đã bị dừng (SDK hủy task nền), nhưng spec
§4.5 + docstring SDK dặn đọc nốt ⇒ sửa điều kiện thành cờ `stopped_early` (mình tự dừng đọc: ngắt / hết giờ) ⇒ chạy lại: có drain. Cùng lượt đó, cách ngắt "giữa chừng" bằng `curl | tee | grep -m 5`
**không** làm đứt kết nối (tee không chết) ⇒ đổi sang `curl --max-time`.

Thời gian (một lần chạy, không phải lượt đo D2 — chỉ để biết): `first_text_ms` server 1.065–2.894 ms trên 6 câu chạy trọn; `first_event_ms` 26–36 ms.

**Tiền:** dòng log có token (8 lần gọi trọn): vào 14.331 / ra 1.563. 5 lần gọi bị ngắt / `incomplete` không có usage (log `None`) — ước trên: vào ≈ 1.850 × 5, ra ≤ 750.
⇒ **≈ 0,0041 USD** (cận trên, phần vào tính giá ghi đệm 0,125; ≈ 0,0034 theo giá phẳng 0,10) — dưới trần 0,005 (pilot 2 lần ≈ 0,0006 ≤ 0,001).

## 5. Lỗi và giới hạn

- **`delta_matches_final`** là trường log thêm ngoài danh sách spec §4.6 (để C5 đo được từ log mà không ghi chữ). Khi `false` route **không** tự rút chữ — chỉ ghi; 5 / 5 lần thật là `true`.
  Nếu muốn coi lệch là "kiểm cuối hỏng" (rút lại như D3 (a)) thì cần A / User quyết.
- Ca `incomplete` / ngắt: token `None` (không có `response.completed`); chưa đọc usage từ sự kiện `response.incomplete` (có thể có) ⇒ tiền các ca này chỉ ước.
- "Server không chạy tiếp" sau khi ngắt: bằng chứng là drain xong < 1 ms + không có dòng log nào thêm; không đo được phía OpenAI đã dừng sinh hay chưa.
- Nhánh lỗi trước luồng 503 / 409 / 500 context / 502 của route stream chưa chạy bằng đường thật (giới hạn spec §10) — đọc diff: dùng **chung** `_retrieval_not_ready` + `_error_response_for` với route JSON.
- `recorder` (`EvidenceRecorder`) chỉ được truyền vào phần trước model của route stream (cùng code với route JSON); trong luồng không gọi recorder (không bên nào dùng recorder với route stream).
- D3 (a) (citation hỏng sau khi đã hiện chữ) chỉ kiểm bằng test logic (0 / 489 lần thật).
- Ngắt đúng lúc generator đứng ở `yield` (⇒ `GeneratorExit`) đã có nhánh xử lý nhưng 2 lần ngắt thật đều rơi vào lúc đang chờ model (`CancelledError`) ⇒ nhánh `GeneratorExit` [Code, chưa chạy].
- Log `chat_stream_drain` là dòng thứ hai của cùng lần gọi (khác tiền tố) — đếm "một dòng mỗi lần gọi" phải đếm theo `chat_metrics`.

## 6. Bàn giao cho người kiểm

- Đọc trước: `git diff 9c83003 830df0e`; spec §4.1–§4.6, §7; bảng §4 trên.
- Chạy lại phần rủi ro: `pytest tests/test_chat_stream.py -q`; cổng ổn định + 1 lần ngắt bằng `curl --max-time` (≈ 0,0005 USD). Ca dò khác cách (W32) gợi ý: ngắt bằng client khác (httpx
  đóng sau N `delta`) để thử nhánh `GeneratorExit`; câu có `[Nguồn n]` trong chữ model.
- Worktree `/tmp/b_s1` giữ cho S3.

**Giải thích ngắn:** thêm đường hỏi thứ hai `/api/chat/stream` gửi chữ trả lời từng mảnh ngay khi model viết, thay vì chờ cả câu; trước khi mở luồng nó kiểm lỗi bằng đúng đoạn code của
đường cũ, cuối luồng vẫn kiểm trích dẫn như cũ và chỉ gửi nguồn khi đạt. Người dùng ngắt giữa chừng thì server dừng model và vẫn ghi đúng một dòng số đo. Đường cũ `/api/chat` không đổi;
giao diện chưa dùng đường mới (việc S3).
