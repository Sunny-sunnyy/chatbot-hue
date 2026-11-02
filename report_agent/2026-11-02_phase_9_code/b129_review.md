# Review: Phase 9 B1 (nhánh `p9-b1`, B129)

Người kiểm: C (Claude Opus 5.5, `hue-rag-cc`). Skill `risk-gated-agent-review`. Căn cứ: plan B1 bản 2 `0c9e137b56af`, report `b129_b1_implementation.md` (§6 "Khoá"), diff code.

## Vòng sớm `7e190d7` (C132 · 20:34 02/11/2026 `date`)

Phạm vi (A giao): phần đã khoá của nhánh, diff `a406bea..7e190d7`, gồm 2 commit `d7a4382` và `7e190d7`, 16 file, +642 / −177.
- Có review: định tuyến, trò chuyện, ngoài phạm vi, H4c; vòng stream trong lõi (D6), câu 503, nhãn `routing` trong `App.jsx`; m-1 (ghi mọi lần gọi ở `finally`); P6.
- **Chưa review:** phần ngày (P2, B còn làm) và P5. Review cuối chỉ cần xem phần đổi sau `7e190d7`.
- 0 USD: chỉ đọc, chạy test, chạy ca dò không gọi mạng. Worktree riêng của C ở `7e190d7` và `a406bea` (đã gỡ). Không dùng worktree của B.

### 1. Đối chiếu code với plan bản 2

| Mục plan | Code `7e190d7` | Kết luận |
|---|---|---|
| D9 cờ, mặc định tắt | `settings.yaml` khối `assistant:` 4 cờ `false` + `router_timeout_seconds: 10`; `AssistantFlags.from_settings` (`assistant.py`) | khớp |
| D1 thứ tự | `_pick_route`: luật (nếu bật) ⇒ định tuyến (nếu bật) ⇒ `khan_cap` cho Bản 1, `ngoai_pham_vi` cho câu cố định. Câu cố định trả ngay, không gọi model trả lời | khớp |
| D3 định tuyến | `RouteOutput` `Literal` 4 tuyến, `extra="forbid"`; agent riêng, không công cụ, `store=False`, `max_tokens` 512; `route()` bọc mọi lỗi / hết giờ / đầu ra hỏng thành `GenerationError` ⇒ `_pick_route` đi `tro_ly_hue` + `route_error="router_failed"`; lần gọi đã xong vẫn ghi `llm_calls` ở `finally` | khớp |
| D4 trò chuyện | agent riêng, `{answer}`, không ngữ cảnh / lịch sử; không kiểm `[n]` (m-5, A quyết); `cited = ()` | khớp |
| D5 ngoài phạm vi | `OUT_OF_SCOPE_ANSWER`; `REFUSAL_ANSWERS` (2 câu) dùng ở `is_refusal`, `chat_metrics.refusal`, cả stream | khớp |
| D6 vòng stream trong lõi | `answer_turn_stream` phát `status` / `delta`; route chỉ đổi sang SSE. Hạn giờ bọc cả vòng; tự dừng ⇒ `cancel()` + đọc nốt trong vùng che (chuyển từ route vào lõi). Route `aclose()` lõi trong vùng che | khớp, có 1 minor (m-1) |
| D6 câu 503 | `RETRIEVAL_UNAVAILABLE_MESSAGE` = "Hệ thống tra cứu tạm thời không khả dụng." dùng ở JSON lẫn sự kiện `error` giữa luồng; `failure()` ánh xạ mã | khớp |
| D6 `router` tắt | `routing` chỉ phát khi `flags.router` (và luật không bắt) | khớp |
| D7 ngày | `build_answer_input(…, today=None)` ⇒ đúng chuỗi B0; đếm token và chuỗi gửi đi cùng một `today` | khớp |
| D8 H4c | `PackedSource.source` (không vào chữ ngữ cảnh); `set_notice` chỉ khi cờ bật **và** có nguồn được trích thuộc 3 thư mục; `ChatResponse.notice` + sự kiện `notice`; giao diện hiện dạng chữ (React tự thoát ký tự) | khớp |
| m-1 C128 | `answer_query` / `answer_turn` / `_pick_route` tạo `CallLog` rồi ghi ở `finally`; generator nhận `call_log` từ nơi gọi; test `test_calls_already_made_are_logged_when_answer_fails` | khớp |
| m-3 giao diện | `App.jsx`: thêm nhãn `routing`; `setPhase(data.stage in STATUS_TEXT ? …)` | khớp |

Không thấy thay đổi ngoài phạm vi. `git diff --check a406bea..7e190d7`: sạch.

### 2. Kiểm chạy lại (0 USD)

| Kiểm | Cách | Kết quả |
|---|---|---|
| **P6** (4 cờ tắt = B0), ca dò khác cách B | B bắt kwargs; **C bắt byte thân HTTP** ở `httpx.AsyncClient.send` (như C128), chỉ chuẩn hoá `prompt_cache_key`, ném lỗi trước khi gửi.<br>Đường thường: `answer_case` (cờ mặc định). Đường stream:<br>• nhánh: **`answer_turn_stream(AssistantFlags())`** (vòng stream mới trong lõi);<br>• `main`: `prepare_answer` → `start_answer_stream` (đúng route B0).<br>10 câu smoke × 2 đường; chạy `a406bea`, `7e190d7`, rồi `a406bea` lại (`data/phase_9/c132_review/p6_*.json`) | **PASS**: 3 file **giống hệt nhau** (sha `190a6999c43b`); mỗi câu đúng 1 thân `POST /v1/responses` mỗi đường |
| Test không key | `pytest tests/test_assistant.py test_assistant_boundary.py test_chat_stream.py test_api_chat.py test_openai_full_corpus_generator.py test_emergency.py -q` | **48 passed / 3 error**; 3 error đúng 3 test cần key (như B0). Có test cho: luật không gọi model, câu cố định bỏ qua model trả lời, trò chuyện không tìm kho, định tuyến lỗi ⇒ đường kho, cờ tắt = đường B0, lần gọi đã xong vẫn được ghi khi trả lời lỗi, H4c chỉ cho 3 thư mục |
| Khoá phần kín | sha 4 file khoá + 2 công cụ trên `7e190d7` (C131) | 6 / 6 khớp |

**Câu bất biến đã kiểm:** "Tắt cả 4 cờ thì thân yêu cầu gửi OpenAI giống B0, kể cả khi đường stream đi qua `answer_turn_stream` mới." **Đúng.**

### 3. Findings (vòng sớm)

**0 blocker · 0 major · 2 minor.**

#### m-1 (minor) — route ghi dòng `chat_metrics` **trước** khi đóng lõi ⇒ một ca ngắt kết nối có thể mất mục `llm_calls` của lần gọi trả lời

- **Vị trí:** `api/routes/chat.py` `_answer_events` `finally`: `_copy_trace_metrics` + `logger.info("chat_metrics …")` **rồi mới** `await turn.aclose()`. Lõi chỉ ghi `call_log.calls` vào `trace` ở `finally` của chính nó (`assistant.py` `answer_turn_stream`).
- **Ca bị ảnh hưởng** [Code, chưa chạy]: người dùng ngắt **đúng lúc route đang ở `yield`** (gửi một mảnh chữ) trong khi lõi đứng ở `yield` của nó. Khi đó route nhận `GeneratorExit` và ghi log, rồi mới `aclose()` lõi.
  - Nếu lần gọi model đã xong (`on_llm_end` đã chạy, ví dụ đúng mảnh cuối) thì mục đó **không** có trong dòng log.
  - Ca ngắt lúc đang chờ model (`CancelledError` đi thẳng vào lõi) thì không bị ảnh hưởng, vì `finally` của lõi chạy trước.
  - Hôm nay (B0) thứ tự là "ghi `llm_calls` rồi log", nên đây là một chỗ lùi nhỏ của D6.
- **Tác động:** nhỏ. Ca hiếm, và `usd` sẽ là `None` (không đoán), không phải số sai.
- **Tiêu chí đóng (B chọn):** (a) route `aclose()` lõi (trong vùng che) **trước** khi ghi log; hoặc (b) ghi giới hạn này vào report.

#### m-2 (minor) — đường ngắt giữa stream qua lõi mới chưa chạy thật

- D6 dời "huỷ + đọc nốt" từ route vào lõi. C128 đã chạy thật trên B0, nhưng ở B1 đây là code mới và chưa có lần chạy thật.
- **Tiêu chí đóng:** ở cổng ổn định cuối, chạy 1 câu `curl -m` cắt giữa chữ (như C128 §3 bước 4), kiểm `outcome: client_disconnected` + dòng `chat_stream_drain` + server không treo. Tốn ≈ 0,0003 USD.

### 4. Giới hạn

- P2 (ngày) và P5 (hồi quy 208) chưa review, vì B còn làm.
- Lời dặn định tuyến / trò chuyện chỉ đọc, không đánh giá chất lượng. Chất lượng đo ở P1 / P5; P1 kín đã đạt (C131).
- Chưa chạy thật đường ngắt (m-2), và chưa xem giao diện (B đã có ảnh Playwright ở cổng).

### 5. Kết luận vòng sớm

**Phần đã khoá `7e190d7`: không có finding chặn.** 2 minor B sửa hoặc ghi lại ở bản cuối. Review cuối (phiên sau) chỉ xem diff `7e190d7..<commit cuối>` (P2, P5, sửa m-1 / m-2), cộng cổng ổn định.
