# Review: Streaming — cả nhánh `streaming-final` trước khi merge vào `main`

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 6 minor — minor không chặn merge, không mở vòng sửa riêng)
Người kiểm: agent con ngữ cảnh mới do A giao — review cả nhánh trước merge
Date: 12:42 01/11/2026
Canonical guide: `docs/superpowers/specs/2026-10-31-streaming-design.md` §3, §4, §6 (C1–C7); `skills/practical-project-coding/SKILL.md`; `skills/risk-gated-agent-review/SKILL.md`
Implementation report: cố ý không đọc (A giao: chỉ diff + skill + spec; không đọc report / STATUS / tin nhắn người làm)

## 1. Phạm vi đã review

- Git: `origin/streaming-final` = `6a0c842`; merge-base với `main` = `74a6082` (khớp brief). 8 commit (S1 lõi chung, S2 route stream + sửa
  m-1, S3 giao diện + CSP / lọc HTML theo danh sách cho phép, B108 `cost_usd`). `git merge-tree` vào `main` hiện tại: **không xung đột**
  (`main` từ lúc tách chỉ đổi tài liệu + `.githooks/pre-push` + `scripts/tra_web_codex.sh`, không chồng file của nhánh).
- Đọc **toàn bộ** `git diff main...origin/streaming-final` (19 file, +1070 / −166): `backend/api/{app.py, routes/chat.py}`,
  `backend/core/schema.py`, `backend/llm/{answer_stream.py (mới), grounded_answer.py (mới), generator_openai_full_corpus.py}`,
  `backend/evaluation/full_corpus_eval.py`, 3 file `backend/experiments/…` (chỉ đổi nơi gọi `cost_usd`), 6 file test, `frontend/app.js`,
  `pyproject.toml`, `uv.lock`. Không có file untracked trong nhánh; worktree `/tmp/b_final` sạch (chỉ `data/`, `knowledge-base-hue/` untracked
  như mọi bản sao).
- Đọc thêm code thư viện liên quan (chỉ đọc): `agents/result.py` (`cancel`, `stream_events`), `agents/usage.py`, `starlette/responses.py`
  (`StreamingResponse`), `fastapi.sse.format_sse_event`, `openai…InputTokensDetails`.
- `git grep` mọi nơi gọi các hàm dùng chung bị đổi: `answer_case` (bộ đánh giá + `experiments/phase_8_1/g2_generate.py`), `answer_query` /
  `prepare_answer` (2 route), `cost_usd` / `row_cost_usd` / `usage_totals` (bộ đánh giá + `g2_generate.py`, `g4_rerank.py`, `phase_8_2/b1.py`) —
  mọi nơi gọi đã được cập nhật.
- `git diff --check main...origin/streaming-final`: sạch (exit 0).

## 2. Findings

**Không có blocker, không có major.**

Đối chiếu nhanh với spec:

| Spec | Kết quả đọc diff + chạy |
|---|---|
| §3 phạm vi | Đúng: route mới, lõi chung, cách gọi stream bên cạnh `generate_answer`, `app.js`, log, `fastapi>=0.135`. Thêm ngoài danh sách §3: CSP ở `api/app.py` + lọc HTML theo danh sách cho phép ở `app.js` (theo commit message, do rà bảo mật C106 R2 / review C107 yêu cầu; nhỏ, có test) và nhóm `dev = [playwright]` (m-4). `index.html` không đổi |
| §4.1–4.2 lỗi trước luồng = JSON như `/api/chat` | Đạt — đầu dò của tôi: 503 / 422 / 502 "chưa sẵn sàng" trên route stream ra **cùng mã + cùng thân** với `/api/chat`; 422 không có dòng log ở cả hai route |
| §4.3 sinh + bóc chữ + kiểm cuối | Đạt — cùng `answer_agent`, `max_turns=1`, `_run_config()` dùng chung; hạn giờ chung cho cả vòng đọc; chữ cuối qua `parse_structured_output` ⇒ `check_citations` |
| §4.4 sự kiện | Đạt — đúng tên / `data`; `sources` dùng `SourceResponse` |
| §4.5 hủy | Đạt theo đọc code + đầu dò (log trước mọi `await`, `cancel()`, đọc nốt bằng iterator mới trong `CancelScope(shield=True)` + `move_on_after(0,5 s)`); trừ một khe nhỏ m-1 |
| §4.6 log | Đạt — một dòng `chat_metrics` mỗi lần vào handler ở mọi ca tôi tạo được (kể cả ngắt khi đang tìm); không chữ người dùng; thêm cờ `delta_matches_final` (đúng / sai, không chữ) |
| §4.7 giao diện | Đạt — đọc luồng + parser chịu sự kiện cắt / gộp, bỏ dòng `:`; render cả buffer theo khung hình qua DOMPurify; `[n]` chỉ bật sau `sources`; `error` / đứt ⇒ xóa + "Thử lại"; ô hỏi khóa (m-3 về lời báo) |
| §4.8 5 khác biệt route ↔ `answer_case` | Còn nguyên: (1) bộ đánh giá giữ chữ gốc, route chuẩn hóa ở phản hồi — kiểm citation chuyển sang chữ gốc ở cả hai, tương đương vì `CITATION_PATTERN` nhận cả `[n]` lẫn `[Nguồn n]` và `INSUFFICIENT_ANSWER` không có `[`; (2) giữ chữ khi citation hỏng ↔ 500; (3) mọi lỗi ⇒ `row["error"]` (đầu dò: dòng lỗi giống hệt `main`); (4) recorder chỉ route; (5) id / token chỉ ở dòng kết quả |

### m-1 (minor) — Lỗi không đến từ SDK trong vòng đọc thì lần gọi model không bị hủy

- Vị trí: `backend/api/routes/chat.py:342-393` (`stopped_early` chỉ bật ở `TimeoutError` dòng 366 và nhánh ngắt dòng 383; hủy ở dòng 393).
- Yêu cầu: spec §4.5 / rủi ro §9 "hủy không dừng model ⇒ tốn tiền".
- Bằng chứng: nếu `extractor.feed(...)` (dòng 369) hay `stream.delta(...)` (dòng 371) ném lỗi, lỗi đi vào `except Exception` (dòng 385) ⇒ giao diện
  nhận `error` + `done` đúng, nhưng `stopped_early = False` ⇒ không `result.cancel()`; `events` bị bỏ dở, tác vụ chạy model của SDK chạy tiếp tới hết.
  Đầu dò: `AnswerTextStream().feed('{"answer":"a\\x')` ⇒ `JSONDecodeError` (mảnh JSON sai thoát); ký tự surrogate đứng lẻ giữa chữ ⇒
  `UnicodeEncodeError` khi mã hóa SSE. Fuzz 20.000 ca mảnh cắt ngẫu nhiên trên JSON **hợp lệ** (cả `ensure_ascii` bật / tắt, ký tự điều khiển,
  `\`, `"`, emoji, `[Nguồn`…): 0 lỗi, 0 lệch — nên khe này chỉ mở khi provider gửi JSON sai, hiếm với đầu ra có cấu trúc.
- Tác động: hiếm; khi xảy ra tốn token tới hết câu (≤ 45 s) và một tác vụ nền chạy tiếp; log vẫn đúng một dòng.
- Tiêu chí đóng: hủy dựa trên "chưa đọc hết luồng" thay vì liệt kê lỗi (vd đặt `stopped_early = True` trước vòng, `False` khi gặp
  `StopAsyncIteration`), hoặc ghi rõ giới hạn này trong report S2. Không cần đo lại trả phí.

### m-2 (minor) — Chưa có test không key cho dòng log của route stream ở nhánh lỗi trước luồng

- Vị trí: `backend/tests/test_api_chat.py` (chỉ gọi `/api/chat`); `backend/tests/test_chat_stream.py` dựng `metrics` từ chính `STREAM_METRIC_FIELDS` nên không khóa gì.
- Yêu cầu: spec §4.6 "đúng một dòng mỗi lần gọi vào handler, hai chỗ ghi"; "test khóa tập trường".
- Bằng chứng: không test nào gửi request vào `/api/chat/stream` rồi đếm dòng `chat_metrics`. Đầu dò của tôi (0 USD) cho thấy hiện **đúng**
  (503 không lifespan: 1 dòng, tập trường = `STREAM_METRIC_FIELDS`, 0 lần lọt câu hỏi), nhưng hai chỗ ghi log (route + `finally` của luồng) là chỗ
  dễ vỡ nhất khi sửa sau này.
- Tác động: hồi quy "0 hoặc 2 dòng" / thêm trường log không bị test bắt.
- Tiêu chí đóng: thêm 1–2 test không key như `test_chat_metrics_logged_when_retrieval_not_ready` và
  `test_real_first_chunk_budget_error_has_no_partial_answer` nhưng gọi `/api/chat/stream` (503 + 500 ngân sách): 1 dòng, tập trường đúng, không có câu hỏi trong log.

### m-3 (minor) — Đứt mạng giữa chừng hiện lời lỗi thô của trình duyệt thay vì "Kết nối bị gián đoạn"

- Vị trí: `frontend/app.js:158-161` (`catch (error) { reader.cancel()…; throw error; }`).
- Yêu cầu: spec §4.7 "luồng đứt không có `done` ⇒ xử lý như `error`" — code có `INTERRUPTED_MESSAGE` (dòng 71) cho đúng ca này.
- Bằng chứng (đọc code; chưa chạy trình duyệt): luồng đóng sạch không có `done` ⇒ dòng 162 ném `INTERRUPTED_MESSAGE` (đúng). Nhưng khi
  `reader.read()` **bị từ chối** (mất mạng, server chết giữa chunk — trình duyệt báo `TypeError` kiểu "network error") hoặc `JSON.parse` lỗi, lỗi
  gốc được ném lại ⇒ `#status` hiện chữ tiếng Anh của trình duyệt. Vẫn xóa chữ + hiện "Thử lại" đúng D3 (b).
- Tác động: chỉ là lời báo; hành vi an toàn (xóa chữ) vẫn đúng.
- Tiêu chí đóng: lỗi không do sự kiện `error` của server ⇒ ném `INTERRUPTED_MESSAGE`; hoặc ghi nhận là giới hạn (spec §10 đã ghi ca này chưa kiểm bằng đường thật).

### m-4 (minor) — `playwright` vào nhóm `dev` ⇒ mọi `uv sync` / `uv run` đều cài, mà code tracked không dùng

- Vị trí: `pyproject.toml:36-38`, `uv.lock` (+`playwright`, `greenlet`, `pyee`).
- Yêu cầu: spec §3 chỉ ghi đổi dependency `fastapi>=0.135` (đã đúng, bản cài 0.141.1); brief: "`pyproject.toml` / `uv.lock` đổi đúng phần cần".
- Bằng chứng: `git grep -i playwright` (trừ `uv.lock`) trong nhánh: chỉ `pyproject.toml` + tài liệu — không có script / test tracked nào import.
  uv mặc định kèm nhóm `dev` khi `uv sync` / `uv run` (không có `default-groups` trong `pyproject.toml`).
- Tác động: máy khác / CI cài thêm 3 gói không dùng; nhỏ.
- Tiêu chí đóng: chuyển sang nhóm không mặc định (vd `browser = ["playwright==1.58.*"]`, dùng `uv run --group browser`, như nhóm `evaluation`
  đang làm) hoặc A ghi quyết định giữ.

### m-5 (minor, ghi nhận ranh giới khâu) — Route API biết chi tiết sự kiện / lỗi của Agents SDK

- Vị trí: `backend/api/routes/chat.py:321` (phân loại `AgentsException`, `OpenAIError`), `:354-371` (đọc `raw_response_event` /
  `response.output_text.delta`, hạn giờ, `cancel()` + đọc nốt).
- Yêu cầu: skill `practical-project-coding` "Ranh giới theo khâu pipeline" — khâu sinh bọc SDK; đường không stream đã bọc mọi lỗi SDK thành
  `GenerationError` bên trong generator.
- Bằng chứng: đường stream để route vừa lọc sự kiện SDK, vừa giữ hạn giờ 45 s, vừa bắt lỗi thô của SDK. Đây **đúng thiết kế spec** (§4.3 bước 1,
  §4.5 đặt hạn giờ / hủy trong `gen()`), và hiện chỉ có một nơi dùng, nên không đòi sửa.
- Tác động: nơi thứ hai muốn stream (harness đo, notebook) sẽ phải chép phần đọc sự kiện + hủy.
- Tiêu chí đóng: không bắt buộc trước merge; khi có nơi dùng thứ hai thì chuyển phần "lọc sự kiện chữ + bọc lỗi SDK" vào generator. Ghi vào report là đủ.

### m-6 (minor) — Route stream ghi `EvidenceRecorder` nửa chừng; nhánh `if not query` chép thêm một chỗ không bao giờ chạy

- Vị trí: `backend/api/routes/chat.py:237-248` (truyền `recorder` vào `_retrieval_not_ready`, `prepare_answer`, `_error_response_for`), `:232-235`.
- Bằng chứng: luồng mở rồi thì không còn `record_generation_result` / `mark_success` / `record_error("citation_integrity_failed")` ⇒ nếu
  recorder được bật cho route stream, bản ghi chỉ có ngữ cảnh. Hiện chỉ `phase6_live_smoke` bật recorder và nó gọi `/api/chat` ⇒ chưa gây sai.
  `if not query` ở route stream không chạy được: `ChatRequest` có `str_strip_whitespace=True` + `min_length=1` nên FastAPI trả 422 trước handler
  (đầu dò: `"   "` ⇒ 422, 0 dòng log ở cả hai route); `_answer` trên `main` cũng có nhánh chết này.
- Tác động: không có tác động lên người dùng; code thừa / gây hiểu nhầm.
- Tiêu chí đóng: route stream truyền `None` cho recorder (hoặc ghi một dòng docstring "recorder chỉ hỗ trợ `/api/chat`"); bỏ nhánh chết ở route
  stream (tùy người làm). Không cần chạy lại gì ngoài test file chạm.

### Ngoài spec streaming — sửa `cost_usd` (B108): đạt

- Công thức: `input_tokens` gồm phần đệm; phần thường × 0,10 + ghi đệm × 0,125 + đọc đệm × 0,01 + ra × 0,50 (USD / 1M) — **khớp** bảng giá User
  30/10 ghi ở `session_prompt/Project_Status.md` (dòng 2026-10-30 15:07). Không truyền phần đệm ⇒ giá phẳng như cũ (dòng kết quả cũ giữ số cũ).
- `input_cache_tokens` đọc đúng trường có thật trong thư viện đã cài (`openai` `InputTokensDetails` có `cached_tokens`, `cache_write_tokens`;
  `agents.usage.Usage` điền 0 khi provider không gửi — đã ghi trong docstring). Mọi nơi gọi `cost_usd` đã đổi; test kiểm cả số thật B95.
- `/api/chat` log thêm `cache_write_tokens`, `cached_tokens` (số đếm, không nội dung) — đúng chính sách log.

## 3. Cách người kiểm chạy lại thật

Tất cả 0 USD, không key, không server, không mở `.env` / file `*sealed*`; Qdrant local chỉ đọc + e5 local (`HF_HUB_OFFLINE=1`). Script đầu dò để
ngoài repo (`/tmp/review_probe_sf/`), chạy từ `backend/` của worktree tương ứng.

1. `cd /tmp/b_final/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_chat_stream.py tests/test_api_chat.py tests/test_grounded_answer.py tests/test_full_corpus_eval.py tests/test_citations.py tests/test_input_cache_tokens.py tests/test_static_ui.py -q`
2. `probe_api.py` (TestClient, `6a0c842`): so `/api/chat` ↔ `/api/chat/stream` ở 503 (không lifespan), 422 (`"   "`, 501 ký tự), 502 chưa sẵn
   sàng (lifespan không key); rồi generator **lớp thật** `OpenAIFullCorpusGenerator` + `AsyncOpenAI` thật trỏ vào cổng local đóng (lỗi kết nối) và
   cổng local nhận mà không trả lời (hạn giờ đặt 1 s). Đây là đầu dò **đường code**, không phải bằng chứng provider.
3. `probe_json_route.py`: cùng 6 ca không tốn tiền của `/api/chat` chạy trên `main` (`/home/minhhieu/hue_rag`) và trên nhánh, `diff` kết quả.
4. `probe_case.py`: `answer_case` với generator lớp thật trỏ cổng đóng, 2 câu tự viết, trên `main` và nhánh, `diff` dòng kết quả (bỏ 2 trường đệm mới).
5. `probe_early_disconnect.py`: gọi ASGI trong tiến trình (`spec_version` 2.3 như uvicorn), `http.disconnect` đã xếp hàng sẵn khi route trả
   `StreamingResponse` (người dùng đóng tab lúc đang tìm) + ca đối chứng không ngắt; đếm dòng `chat_metrics`.
6. `fuzz_extract.py`: 20.000 câu ngẫu nhiên từ bảng ký tự "khó" × điểm cắt ngẫu nhiên × `ensure_ascii` bật / tắt × khoảng trắng quanh `"answer"`.
7. `git diff --check main...origin/streaming-final`; `git merge-tree --write-tree main origin/streaming-final`; `git grep` nơi gọi; đọc code thư viện.

## 4. Kết quả quan sát

- (1) **61 passed, 1 error** — lỗi duy nhất là `test_health_is_cached_and_ready_after_real_lifespan` thiếu `OPENAI_API_KEY` (đúng như brief báo trước).
- (2) Route stream: 503 / 422 / 502 cùng mã + thân với `/api/chat`; 503 có đúng 1 dòng log, tập trường = `STREAM_METRIC_FIELDS`, 0 lần lọt câu
  hỏi; 422 có 0 dòng ở cả hai route. Cổng đóng: `/api/chat` 502 `generation_unavailable` (log `generation_failed`); route stream 200
  `text/event-stream` với `status{searched, n_sources 10}` → `status{generating}` → `error{generation_unavailable, after_text: false}` →
  `done{generation_failed}`, đúng §4.2. Hạn giờ 1 s: cùng chuỗi sự kiện, header `Cache-Control: no-cache`, `X-Accel-Buffering: no`, 1 dòng
  `chat_metrics` (`generation_ms` ≈ 1003) + 1 dòng `chat_stream_drain {"finished": true, "ms": 0.5}`; log lỗi chỉ ghi tên lớp (`TimeoutError`,
  `APIConnectionError`). Không dòng log nào chứa câu hỏi.
- (3) `/api/chat` trên `main` ↔ nhánh: **giống hệt** ở 6 ca (503, 422 × 2, 500 ngân sách ngữ cảnh, 502 chưa sẵn sàng, 502 lỗi kết nối).
- (4) `answer_case` trên `main` ↔ nhánh: dòng kết quả **giống hệt** (lỗi `GenerationError <- APIConnectionError`, `top_chunk_ids` có,
  `context_sources` 10, token / id `None`).
- (5) Ngắt đã xếp hàng trước khi luồng chạy: 1 dòng `chat_metrics`, `outcome = client_disconnected` (giả thuyết của tôi "luồng chưa chạy thì
  mất dòng log" **bị bác**); đối chứng không ngắt: 1 dòng `generation_failed`, đủ `status, status, error, done`.
- (6) Fuzz: 20.000 ca, **0** lỗi, **0** lệch "ghép các mảnh = `normalize_citations(chữ cuối)`", mọi mảnh mã hóa UTF-8 được. Hai đầu vào JSON
  **sai** ném `JSONDecodeError` (cơ sở của m-1).
- (7) `git diff --check` sạch; merge vào `main` không xung đột; mọi nơi gọi hàm dùng chung đã cập nhật.

Câu bất biến đã kiểm: "`/api/chat` và `answer_case` cho cùng mã / thân / dòng kết quả như `main` ở mọi nhánh chạy được không tốn tiền" — giữ
ở (3), (4). Câu bất biến thứ hai: "mỗi lần vào handler của route stream có đúng một dòng `chat_metrics`" — giữ ở (2), (5).

## 5. Giới hạn hoặc phần chưa chạy

- Không gọi model thật ⇒ **chưa tự kiểm** bằng đường thật: luồng chữ thật, C4 (cổng ổn định trên uvicorn thật cả hai route), C5 (chữ ghép từ
  `delta` = chữ cuối trên câu thật), C7 ca `incomplete` và ngắt thật 2 thời điểm, hành vi giao diện trên trình duyệt. Các phần này là bằng
  chứng của người làm (report S1–S3, tôi cố ý không đọc) — A đối chiếu khi trình User.
- C1 / C2 / C3 / C6 thuộc S4 (đo trên trình duyệt) đang làm: nhánh này **chưa** có số đo. Spec §5: C1 hoặc C2 trượt ⇒ dừng trước khi đóng việc.
  Merge trước S4 nghĩa là `main` đổi giao diện sang `/api/chat/stream` trước khi biết C1 / C2 — `/api/chat` vẫn còn nên quay về PA3 / route cũ là
  sửa một dòng `fetch` ở `app.js`; A / User quyết thứ tự.
- Đầu dò lỗi provider dùng endpoint local (cổng đóng / treo): kiểm đường code, không chứng minh cách provider thật báo lỗi.
- Không chạy T1 (158 câu) — diff không đổi code khâu tìm (`retrieval/` không nằm trong diff; `prepare_answer` gọi cùng `retrieval_service.search`).
- `test_phase6_live_smoke.py` (recorder trên `/api/chat`) cần key ⇒ không chạy; recorder được kiểm bằng đọc diff (thứ tự gọi giữ như `main`).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Code đúng spec §3–§4 ở mọi chỗ tôi kiểm được bằng đọc diff và chạy 0 USD; route JSON và bộ đánh giá giữ hành vi
cũ (so trực tiếp với `main`); log không lộ chữ người dùng / khóa; giao diện không tự tải từ máy khác (CSP `default-src 'self'` trên `/` và
`/static/index.html`, DOMPurify theo danh sách cho phép, vendor không `eval`, CSS không `url()` / `@import`). Sửa `cost_usd` đúng bảng giá User 30/10.

6 minor không chặn: người làm có thể gom m-1, m-2, m-6 (nhỏ, không tốn tiền) vào một commit trước hoặc sau merge; m-3, m-4 sửa nhanh hoặc A ghi
quyết định; m-5 chỉ ghi nhận. Đây là việc rủi ro cao (đổi giao diện người dùng + route mới) ⇒ A trình User: kết quả trên, bằng chứng đường thật
của report S1–S3 (C4, C5, C7), giới hạn §5 (đặc biệt C1 / C2 của S4 chưa có) — **User xác nhận merge** và thứ tự merge ↔ S4.

**Giải thích ngắn:** nhánh này cho chatbot hiện chữ trả lời ngay khi model viết (route mới `/api/chat/stream` + giao diện đọc luồng), dùng chung
một lõi "tìm → ngữ cảnh → sinh → kiểm trích dẫn" với route cũ và bộ đánh giá nên hai nơi đó không đổi hành vi, và tính tiền đúng giá ghi / đọc đệm;
còn vài điểm nhỏ (một khe hủy model hiếm gặp, thiếu test log cho route mới, lời báo đứt mạng) không chặn merge.
