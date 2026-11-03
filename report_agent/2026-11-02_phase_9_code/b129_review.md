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

## Vòng cuối `7e190d7..dcd1519` (C134 · 09:08 03/11/2026 `date`)

Đầu vào: commit `dcd1519` (đã push, = `origin/p9-b1`), worktree `/tmp/b_p9b1` ở `dcd1519` (chỉ có `data`, `knowledge-base-hue` symlink untracked); report người làm
`b129_b1_implementation.md` §4b (sha `0febf8eb574d`, working tree `main`). Phạm vi theo mục C134: (a) 32 câu an toàn giống byte, (b) sửa m-1 + test, (c) mặc định 2 cờ, (d) ca dò byte P6 + ngắt thật.
Ca dò của C (private): `data/phase_9/c134_review/`. Tiền ≈ 0,0006 USD (3 câu thật; `usd` log 0,000575 + 2 lần trả lời bị huỷ không có usage).

### 1. Cổng tối thiểu

- 1 commit, 4 file: `api/routes/chat.py` (+9 / −6), `config/settings.yaml` (4 dòng cờ), `tests/test_api_chat.py` (+3: generator giả có `route()`), `tests/test_chat_stream.py` (+1 test). Khớp §4b; không file ngoài phạm vi.
- `git diff --check 7e190d7..dcd1519` sạch. Code `main` `22068df` = B0 `1c10111` ở `backend/` + `frontend/src/` (0 file khác).

### 2. Kiểm theo rủi ro

| Mục | Cách C kiểm (khác cách B) | Kết quả |
|---|---|---|
| (b) m-1 — đóng lõi trước dòng log | Đọc `finally` mới: `total_ms` ⇒ `await turn.aclose()` trong `CancelScope(shield=True)` ⇒ `finally` lồng chép số đo + ghi log. Ca dò `probe_m1.py` (`0be033763816`) ở 2 đường **B không thử**: (1) huỷ tác vụ anyio khi lõi đang **chờ** (như Starlette huỷ task group); (2) `aclose` lõi **ném lỗi** | (1) `client_disconnected`, `n_llm_calls` 1, `usd` đúng, **1** dòng log; (2) như vậy, lỗi vẫn đi ra (`RuntimeError`), dòng log **vẫn ghi**. Đạt |
| (b) thứ tự dòng log đổi | `git grep chat_stream_drain` trên `dcd1519` + `grep -r` `data/`, `scripts/`, `bao_cao_he_thong/`, `guides/`, `docs/` | Không code / script nào đọc log theo thứ tự hai dòng; chỉ report cũ (S2) tả "dòng thứ hai" — lịch sử, không phải hợp đồng. Không hỏng gì |
| (a) 32 câu an toàn giống byte | `probe_at.py` (`a54565d9c8bd`): bắt thân **HTTP** ở `httpx.AsyncClient.send` (B bắt kwargs `AsyncResponses.create`), cho định tuyến **thành công** trả `tro_ly_hue` (vá `generator.route`) ⇒ kiểm đường thành công; so lần gọi trả lời 4 cờ tắt ↔ {`router`, `may_have_changed_notice`} | **32 / 32 giống** (`at.json` `0e78a63e962e`); mỗi câu đúng 1 lần gọi trả lời mỗi bên; định tuyến được gọi 1 lần khi bật, 0 khi tắt. qid khớp file B. ⇒ đồng ý dùng lại S-AT 01/11 |
| (c) mặc định cờ | `probe_at.py` assert `AssistantFlags.from_settings(settings.yaml)` = {`router`, `may_have_changed_notice`}; đọc diff | Đạt. `emergency_rule`, `today_line` = false. `answer_case(flags=None)` vẫn tắt cả (như B0); `evaluation generate` không `--flags` **theo `settings.yaml`** ⇒ từ nay có định tuyến (m-1 dưới) |
| (d) P6 ca dò byte HTTP (4 cờ tắt = B0) | `data/phase_9/c132_review/p6_http.py` trên `dcd1519` | `p6_dcd1519.json` sha **`190a6999c43b`** = `main` ×2 = `7e190d7` (C132). Đạt |
| (d) ngắt thật | Server nhánh cổng 8871 (`settings.yaml` mặc định mới), `/` 200, `/health` 5 / 5. 3 câu tự viết: (1) `curl -m 6` cắt **trước chữ đầu** (3 `status`); (2) `curl -m 10` — câu xong trước hạn; (3) client httpx đóng sau **5 `delta`** (cắt giữa chữ) | (1) `client_disconnected`, `llm_calls` = [định tuyến], `chat_stream_drain` finished 0,6 ms **trước** `chat_metrics`; (2) `success`, 2 lần gọi, có sự kiện `notice` (H4c bật) + `sources` + `done`; (3) `client_disconnected`, `chat_stream_drain` finished 0,6 ms, `llm_calls` = [định tuyến]. `/health` 200 sau mỗi lần; `chat_metrics` mới **3 = 3** câu hợp lệ; "Received question" 0; grep chữ câu hỏi trong log **0**. Tắt bằng TaskStop |
| test chạm | `pytest tests/test_chat_stream.py tests/test_assistant.py` (không key) trên worktree | 27 / 27 pass. Test có key: dùng lại 60 / 60 của B (code không đổi sau lần chạy đó) |

**Câu bất biến:** "Mỗi lượt stream — xong, ngắt lúc chờ, ngắt lúc gửi, hay lõi lỗi lúc đóng — ghi **đúng một** dòng `chat_metrics`, không chứa chữ câu hỏi." **Đúng** ở cả 3 ca thật + 3 ca dò.

### 3. Findings (vòng cuối)

**0 blocker · 0 major · 1 minor.** m-1 / m-2 vòng sớm: **đóng** (m-1 sửa + test FAIL cũ / PASS mới theo B, C dò thêm 2 đường; m-2 ngắt thật trước chữ + giữa chữ, B 2 ca + C 2 ca).

#### m-3 (minor, không chặn) — lượt đo Golden bằng `evaluation generate` không `--flags` nay chạy cả định tuyến

- **Vị trí:** `evaluation/full_corpus_eval.py` `run_generation`: `flags_on is None` ⇒ `AssistantFlags.from_settings(settings)`; `dcd1519` bật `router` + `may_have_changed_notice` mặc định.
- **Tác động:** đúng ý B1 (mốc V0 của B2 = B1), nhưng ai chạy lại lệnh cũ của Phase 1–8 để so "RAG 1–8" sẽ có thêm 1 lần gọi / câu (tiền + latency) và nhãn tuyến, không còn là đường B0. `answer_case(flags=None)` vẫn tắt cả ⇒ hai cửa vào cùng hàm cho hai mặc định khác nhau.
- **Tiêu chí đóng:** ghi một dòng ở guide 6 / LUONG khi merge ("`generate` theo `settings.yaml`; đo đường RAG 1–8 ⇒ `--flags` rỗng") và plan B2 / B7 ghi `--flags` tường minh. Không cần sửa code.

### 4. Giới hạn

- Theo phạm vi C134, **không** kiểm lại số P2 (ngày) và P5 (hồi quy 208 + judge) — kết quả + quyết định dùng lại đã có ở report §4 / handoff (A quyết). Nếu A muốn, cần một lượt riêng.
- Ca cắt giữa chữ: lần gọi trả lời bị huỷ không có usage ⇒ `usd` lượt đó chỉ tính định tuyến (đúng spec streaming §4.5, đã biết từ B0) — tiền thật hơi cao hơn log.
- Chữ đầu / latency không đo lại (B131 đã đo; đây là review đúng / sai).

### 5. Kết luận vòng cuối

**`ready_for_user_confirmation`** cho nhánh `p9-b1` `dcd1519` (cùng vòng sớm `7e190d7`). m-3 ghi vào báo cáo lúc merge.
