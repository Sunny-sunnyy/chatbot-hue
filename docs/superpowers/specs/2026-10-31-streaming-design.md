# Streaming câu trả lời — tài liệu thiết kế (NHÁP, chờ review rồi User duyệt)

Người viết: C · Ngày: 31/10/2026 (viết 11:50 31/10/2026, `date`) · Trạng thái: **bản 2 — sửa theo B105 (`report_agent/2026-10-31_streaming_spec/b105_review.md` `16234cd206d0`, 1 major / 4 minor), 12:01 31/10/2026; chờ B kiểm phần đổi ⇒ Codex review một lần (W33) ⇒ User duyệt sha**.
Bản 4 (12:09 31/10/2026): Codex review một lần (`report_agent/2026-10-31_streaming_spec/b106_codex_review.md` `771cb11f4edf`, 2 minor) ⇒ §4.3 bước 5 (nhánh ngắt), §4.6 / C4 / C7 ("vào handler"), §7 + §10 (422 ↔ nhánh lỗi trước luồng). Bản 3 (12:03 31/10/2026): B105 vòng 2 ready (`96bcc907886b`); áp n-1 (§4.5 bước 3: gọi lại `stream_events()`, iterator mới). Bản 1: `6e574410a7bc` (sửa C2 theo A ⇒ `c820ec0e18e7`). Đổi ở bản 2: §4.5 + §4.6 + C7 (M-1, hủy khi ngắt); §4.3 bước 1, 4 + C5 (m-4, m-1); §4.8 + S1 (m-2); C1 / C2 + luật trượt (m-3); §8 tiền theo cỡ mẫu mới.
Gốc: nháp phương án v3 bản 3 (private `data/tinh_nang_moi_2026-10-27/c98_phuong_an_streaming_v3.md`, sha `3b6a9ba09149`, B102 ready). File tracked này **không chép nội dung kho,
câu Golden hay câu kín**; chỉ quy trình, số đo, đường dẫn private.

## Căn cứ để review (`WORKFLOW.md` §9.1)

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `data/tinh_nang_moi_2026-10-27/c98_phuong_an_streaming_v3.md` (`3b6a9ba09149`) | §1, §2, §3, §4, §5, §6 | spec đúng các quyết định User đã chốt dựa trên bảng này; không mất điểm khó / test / giới hạn |
| `session_prompt/CURRENT_HANDOFF.md` | mục "Phiên 31/10 — quyết định + việc đang mở": các dòng "User chốt D1 / D2 / D3", C100 | quyết định + ngày ghi đúng |
| `data/tinh_nang_moi_2026-10-27/c97_doi_chieu_code_streaming.md` (bản 3 `702cc7ed8af4`) | mục 2a, §2 bảng §4 | cách (b) cho lỗi trước luồng; đường hủy |
| code `main` | `backend/api/routes/chat.py`, `backend/llm/{citations.py, generator_openai_full_corpus.py}`, `backend/evaluation/full_corpus_eval.py:322-364`, `frontend/app.js` | `file:dòng` trong spec khớp code |

## 1. Mục tiêu

Hôm nay giao diện chờ model viết **xong cả câu** rồi mới hiện (`frontend/app.js:86-93`). Câu cần trả lời dài (kể, so sánh, liệt kê) chờ trung vị 4,6 s / p95 7,6 s — **vượt** yêu cầu
p95 ≤ 5 s của User (đo harness 28/10). Mục tiêu: **chữ trả lời hiện ngay khi model viết**, để người dùng bắt đầu đọc sớm hơn (đo harness 28/10: sớm hơn trung vị 1,92 s, CI 95 %
1,61–4,31 s, 10 câu tự viết), mà **chữ còn lại trên màn hình khi xong vẫn luôn là chữ đã qua bộ kiểm citation hôm nay**.

Không đổi: khâu tìm, ngữ cảnh (10 đoạn), prompt, model `gpt-6-luna`, đầu ra JSON `AnswerOutput{answer}`, luật kiểm citation, route `POST /api/chat` (bộ đánh giá + máy khác vẫn dùng).

## 2. Quyết định

| Ngày / giờ (A ghi nhận) | Quyết định | Ai |
|---|---|---|
| 30/10/2026 14:39 | Thứ tự: streaming ⇒ hội thoại nhiều lượt ⇒ đóng gói Phase 1–8 ⇒ Phase 9 | User (`Project_Status.md` §5) |
| 31/10/2026 (phiên) | Phạm vi: API + sửa tối thiểu giao diện JS thuần hiện có; giao diện mới (React / Next…) bàn sau khi xong Phase 8 | User |
| 31/10/2026 11:26 | **D1 = PA1:** chữ hiện ngay khi model viết + tiến độ thật; kiểm citation lúc cuối như hôm nay | User |
| 31/10/2026 11:44 | **D2 = (a):** p50 ≤ 3 s / p95 ≤ 5 s áp cho **"tới chữ trả lời đầu tiên hiện trên trình duyệt"**; câu từ chối đo "tới lúc biết chắc là từ chối"; "tới đủ câu" đo + báo, chỉ theo dõi. Đo bằng trình duyệt thật, không harness | User |
| 31/10/2026 11:48 | **D3 = phương án 1:** (a) bộ kiểm cuối hỏng ⇒ **rút lại** chữ đã hiện; (b) lỗi / đứt giữa chừng ⇒ **xóa hết**; cả hai thay bằng lời báo + nút "Thử lại" | User |
| 31/10/2026 | Câu từ chối dùng **cùng sàn** D2, đo "tới lúc biết chắc là từ chối", báo riêng nhóm này (§6 C2) | A (kỹ thuật trong phạm vi D2) |
| 31/10/2026 11:48 | **D5:** xem lại (đề xuất PA3 — chỉ tiến độ, câu trả lời hiện một lần) khi số lần rút / xóa > 1 % câu / tuần dùng thật, hoặc ≥ 3 lần trên ≥ 100 câu; cũng xem lại khi lợi đo qua trình duyệt < 0,5 s | A (báo User) |
| 31/10/2026 11:48 | Không làm nút "Dừng" ở bản này (ô hỏi đã khóa khi đang chờ, `app.js:11-14, :78`) | A |
| 31/10/2026 | Lỗi **trước** khi mở luồng: endpoint là hàm thường, trả `JSONResponse` như hôm nay; qua hết mới trả luồng (cách (b), C97 mục 2a — probe C97 + B100 trên uvicorn thật) | A |
| 31/10/2026 | Ép `response.incomplete` bằng `answer_max_output_tokens` nhỏ khi test **không phải lỗi giả** (model + API thật, chỉ đặt tham số); trần ≤ 0,001 USD | A |
| 31/10/2026 | Không thêm chỗ nối chỉ dùng khi test (không stub model); ca không tạo được bằng đường thật ⇒ test logic thuần + ghi giới hạn | A |
| 31/10/2026 | Giữ đầu ra JSON (không đổi sang chữ thường): JSON stream được trên đúng thư viện đã cài (C97 §0.1) | A |
| 31/10/2026 | Kiểu "model ghi số nguồn trước" (citation-first): để sau — đổi đầu ra ⇒ phải đo lại chất lượng | A |

Yêu cầu phi chức năng giữ nguyên: ≤ 0,0005 USD / câu (User 28/10); thứ tự lỗi: sai cảnh báo an toàn / điều kiện vào khu vực > nói chắc sai / bịa > trả lời câu ngoài kho > thiếu ý >
từ chối nhầm (User 28/10).

**Mức chuẩn ngành cho "tới chữ đầu tiên": TBD** — A điền từ lượt tra Codex; nếu nguồn cho thấy nên chặt hơn p50 3 s / p95 5 s, A báo User trước khi chốt tiêu chí §6.

## 3. Phạm vi

**Trong:**
- route mới `POST /api/chat/stream` (luồng sự kiện SSE); `POST /api/chat` giữ nguyên hành vi;
- gom "tìm → ngữ cảnh → sinh → kiểm" thành **một lõi chung** cho hai route + bộ đánh giá (hôm nay đã có hai bản cùng luồng: `chat.py:86-204` và `answer_case`
  `backend/evaluation/full_corpus_eval.py:322-364`);
- generator thêm cách gọi stream (`Runner.run_streamed`) bên cạnh `generate_answer` hiện có;
- `frontend/app.js` đọc luồng, hiện chữ dần, rút / xóa khi lỗi; `index.html` chỉ sửa nếu cần chỗ hiện tiến độ;
- log `chat_metrics` cho route mới; `pyproject.toml` nâng `fastapi>=0.115.0` ⇒ `>=0.135` (bản cài 0.141.1) để dùng `fastapi.sse.format_sse_event`.

**Ngoài:** nút Dừng; hội thoại nhiều lượt; giao diện mới; deploy / proxy; kiểm nghĩa câu trả lời (bộ kiểm vẫn chỉ kiểm định dạng); đổi prompt / model / đầu ra; `request_id` trong log.

## 4. Thiết kế

### 4.1 Luồng

```text
POST /api/chat/stream {query}
  │   (thân sai — rỗng sau strip / > 500 ký tự — FastAPI trả 422 ở api/app.py:148-159 trước khi vào handler, như hôm nay)
  ├─ (hàm thường) kiểm như hôm nay tới chat.py:153: 422 / 503-409 tìm / 500 context / 502 generator chưa sẵn sàng ⇒ JSONResponse (mã + thân giữ nguyên)
  │   từ chối không gọi model (chat.py:140-144) ⇒ vẫn đi luồng: delta câu chuẩn + sources rỗng + done
  └─ qua hết ⇒ StreamingResponse(gen(), media_type="text/event-stream", headers={Cache-Control: no-cache, X-Accel-Buffering: no})
       gen(): status{searched} → status{generating} → delta… (chữ bóc từ JSON đang stream) → kiểm cuối
              qua  ⇒ sources (chỉ nguồn được trích) → done{success}
              hỏng ⇒ error{citation_integrity_error, after_text: true} → done          (giao diện rút lại — D3 (a))
              lỗi giữa chừng (timeout 45 s, provider, response.incomplete) ⇒ error{…, after_text} → done   (giao diện xóa hết — D3 (b))
              người dùng ngắt ⇒ hủy lần gọi model, không gửi gì thêm
```

### 4.2 Lỗi trước khi mở luồng (cách (b))

- 5 nhánh lỗi trước model đi **một** đường như hôm nay: mã HTTP + thân `{"error": {code, message}}` (`chat.py:53-57`), giao diện bắt bằng `!response.ok` (`app.js:92`).
- **Không** dùng generator `EventSourceResponse` kèm "trả `JSONResponse` khi lỗi trước luồng" — ra 200 thân rỗng (B100 M-1, đã chạy).
- Cái giá: tự đặt 2 header; không có ping 15 s tự động (luồng ≤ 45 s, chữ đầu ~2,4 s ⇒ không cần trên máy cá nhân; xem lại khi deploy); **lỗi gọi model trước chữ đầu** (hôm nay
  `generation_failed` 502, `chat.py:156-168`) chạy trong `gen()` ⇒ thành 200 + `error{after_text: false}` ⇒ giao diện vẫn cần cả hai đường lỗi.

### 4.3 `gen()` — sinh, bóc chữ, kiểm

1. Gọi `Runner.run_streamed` với **cùng** `answer_agent` (`generator_openai_full_corpus.py:112-123`: `output_type=AnswerOutput`, `max_tokens` 2.048, `include_usage`, `store=False`,
   `reasoning` như hôm nay) **và cùng tham số lần gọi** như `Runner.run` (`:162-172`: `max_turns=1`, `RunConfig(tracing_disabled=True, trace_include_sensitive_data=False)`) — hai đường
   gọi model phải giống nhau; `asyncio.wait_for` 45 s bọc **cả** vòng đọc sự kiện. Giữ `max_retries=0`; không bật `ModelSettings.retry` (tránh chữ lặp).
2. Lấy `response.output_text.delta` từ `raw_response_event`; bóc chữ trong `{"answer": "…"}` bằng bộ giải mã chuỗi JSON từng phần đã chạy thật ở C73 (`decode_partial_string`,
   tag `hoso/c70-ttft` `backend/experiments/streaming/ttft.py:88-104`, có test) — đưa vào code chính, không thêm thư viện.
3. Chuẩn hóa `[Nguồn n]` → `[n]` trên chữ đã phát, **chỉ khi `]` đã tới** (mảnh cắt giữa `[Nguồn 1` thì giữ lại tới mảnh sau) — cùng regex `citations.py:11`.
4. Xong luồng: chữ cuối = `parse_structured_output(result.final_output, AnswerOutput)` (`generator_openai_full_corpus.py:49-82`) ⇒ `normalize_citations` ⇒ `select_cited_sources`
   (`citations.py:19-34`) — **đúng** luật hôm nay. `parse_structured_output` đã `.strip()` (`:81`) ⇒ phép so là `"".join(delta).strip()` (sau chuẩn hóa `[Nguồn n]`) == chữ cuối
   đã chuẩn hóa (kiểm ở §6 C5); giao diện giữ chữ đã hiện (khoảng trắng đầu / cuối không đổi nghĩa).
5. `gen()` **tự bắt mọi lỗi thuộc `Exception`** rồi phát `error` + `done`; không để lỗi thoát ra (trên uvicorn thật lỗi thoát ⇒ kết nối đứt giữa chừng, không có `done` — B100 vòng 2).
   **Riêng ngắt** (`asyncio.CancelledError`, không thuộc `Exception`): nhánh `except asyncio.CancelledError` riêng ⇒ gán `outcome = client_disconnected`, token `None`, rồi **raise lại**;
   không nuốt, không `yield` gì lên kết nối đã đóng (Codex B106 #1). Phần dọn ở `finally` theo §4.5.

### 4.4 Sự kiện (SSE `event:` + `data:` JSON, `json.dumps(ensure_ascii=False)`, định dạng bằng `fastapi.sse.format_sse_event`)

| Sự kiện | Khi nào | `data` |
|---|---|---|
| `status` | tìm xong; bắt đầu viết | `{"stage": "searched", "n_sources": n}` · `{"stage": "generating"}` — không gửi tiêu đề nguồn trước (tránh hiểu "dùng cả 10") |
| `delta` | mỗi mảnh chữ | `{"seq": k, "text": "…"}` — `seq` tăng dần, giao diện chỉ nối `seq` mới |
| `sources` | kiểm citation **qua** | danh sách như `SourceResponse` hôm nay (`chat.py:41-45`), chỉ nguồn được trích |
| `error` | lỗi sau khi mở luồng | `{"code", "message", "after_text": bool}` — mã dùng lại `error_response`; chỉ tách mã khi giao diện xử lý khác nhau |
| `done` | luôn là sự kiện cuối (trừ mất kết nối) | `{"outcome"}` |

### 4.5 Hủy và hết giờ

- Người dùng ngắt (đóng tab / rời trang) ⇒ Starlette hủy `gen()` bằng cancel scope của anyio (uvicorn báo ASGI 2.3, `starlette/responses.py:265-280`; < 10 ms lúc generator đang chờ —
  B100 vòng 2). Hủy kiểu này **lặp lại ở mọi `await`** sau đó trong scope: `finally` thường ⇒ `CancelledError` ngay ở `await` đầu ([Chạy] B105, uvicorn thật, không model:
  `finally` thường đọc được 0 / 5 lần; bọc `anyio.CancelScope(shield=True)` ⇒ 5 / 5 trong 101 ms — probe private `data/tinh_nang_moi_2026-10-27/tools/b105_drive.py`). Nên `finally` của `gen()`:
  1. **ghi `chat_metrics` trước mọi `await`** (ghi log là lệnh đồng bộ);
  2. gọi `result.cancel()` (đồng bộ);
  3. đọc nốt bằng cách **gọi lại `result.stream_events()` (iterator mới** — iterator đang chạy đã bị đóng khi Starlette hủy `gen()`; docstring SDK `agents/result.py:757-758`) **trong `anyio.CancelScope(shield=True)` có giới hạn thời gian** (`anyio.move_on_after(…)` bên trong, mức
     vài trăm ms — người làm chọn, ghi trong report) để luồng hỏng không treo server.
- Hủy khi có model thật: token đã sinh vẫn tính tiền; usage của lần hủy không có (không tới `response.completed`) ⇒ log token `None`, không ghi 0.

### 4.6 Log `chat_metrics` (giữ chính sách hiện hành: không ghi câu hỏi / câu trả lời / nguồn / id / USD — `chat.py:24-29`)

- Lỗi trước luồng: ghi ở route như hôm nay. Luồng mở: ghi ở `finally` **của `gen()`**, **trước mọi `await`** (§4.5) (`finally` của route chạy trước khi luồng chạy; nhánh hôm nay đọc `response.answer`, `chat.py:74`, sẽ lỗi
  với đối tượng luồng) ⇒ vẫn **đúng một** dòng mỗi lần gọi **vào handler**, hai chỗ ghi. Thân sai bị FastAPI trả 422 trước handler (`chat.py:36-38` → `api/app.py:148-159`) ⇒ **không** có
  dòng `chat_metrics` — giữ hành vi hôm nay (Codex B106 #2).
- `outcome` đặt tường minh từng nhánh; `status_code` = 200 khi luồng mở; thêm `outcome`: `retracted` (D3 (a)), `stream_error_after_text` (D3 (b)), `client_disconnected`.
- Trường mới: `first_event_ms`, `first_text_ms` (server: từ lúc nhận request tới `delta` đầu được gửi). Test khóa tập trường (`test_api_chat.py`) sửa có chủ đích.
- D5 đếm từ log: `retracted` + `stream_error_after_text` trên tổng lần gọi route stream.

### 4.7 Giao diện (`frontend/app.js`, JS thuần)

- Gửi `fetch` POST như hôm nay tới route mới; `!response.ok` ⇒ nhánh lỗi cũ.
- Đọc `response.body.getReader()` + `TextDecoder` (`stream: true`); parser SSE chịu sự kiện bị cắt giữa nhiều lần `read()` và nhiều sự kiện trong một lần; bỏ dòng chú thích `:`.
- `status` ⇒ chữ trạng thái ở `#status` (`aria-live="polite"` sẵn có, `index.html:25`); không đặt `aria-live` lên `#answer`.
- `delta` ⇒ nối vào buffer; render lại **cả buffer** bằng `marked` + `DOMPurify` theo khung hình (`requestAnimationFrame`), không theo từng mảnh, không `innerHTML +=`.
- `sources` ⇒ `renderSources` + `wireCitations` như hôm nay (`app.js:18-75`): link `[n]` chỉ bật lúc này.
- `error` ⇒ **xóa** chữ đã hiện (D3 cả (a) lẫn (b)), hiện lời báo + nút "Thử lại" (`app.js:95-97`). Luồng đứt không có `done` ⇒ xử lý như `error`.
- Ô hỏi vẫn khóa khi đang chờ (không có hai câu chồng nhau).

### 4.8 Lõi chung — giữ đúng hành vi từng nơi

- **Ít nhất** các khác biệt sau giữa route và `answer_case` mà lõi chung **không được làm đổi** (đổi là đổi thước đo hoặc đổi hành vi API ⇒ ngoài phạm vi):
  1. route chuẩn hóa citation trước khi kiểm (`chat.py:177`), `answer_case` **không** — `select_cited_sources` chạy trên chữ chưa chuẩn hóa (`full_corpus_eval.py:355-359`), chữ đưa vào judge giữ dạng gốc;
  2. `answer_case` vẫn giữ chữ khi citation hỏng để chấm (`full_corpus_eval.py:356-359`), route trả 500;
  3. **lỗi kỹ thuật:** `answer_case` bắt **mọi** lỗi thành `row["error"]` ⇒ lượt chấm incomplete (`full_corpus_eval.py:362-363`); route đổi từng lỗi ra mã riêng (503 / 409 / 500 context / 502, `chat.py:94-168`);
  4. route gọi `EvidenceRecorder` (`get_current_recorder()`, `chat.py:92` và các lần `recorder.…`), `answer_case` không gọi — recorder do `test_phase6_live_smoke.py` dùng;
  5. `answer_case` ghi `response_id`, `latency_ms`, token vào dòng kết quả (`full_corpus_eval.py:348-353`); route **không** log id (chính sách C59, `chat.py:24-25`).
- Tên hàm / chỗ đặt do người làm chọn, ghi trong report.

## 5. Bước làm (mỗi bước review chéo trước bước sau)

| Bước | Làm | Kiểm trước khi qua bước sau |
|---|---|---|
| S1 | Gom lõi chung; `POST /api/chat` + `answer_case` gọi lõi (chưa có stream) | T1 (158 câu) **giống byte** `4d5bbe9e0edc`; test file chạm; cổng ổn định trên `/api/chat` (§6 C4); `answer_case` chạy 2–3 câu: trường ra giống hôm nay về luật (có `[n]` hợp lệ / từ chối đúng); đủ 5 khác biệt §4.8 còn nguyên (đọc diff + test logic: ca lỗi của `answer_case` vẫn ra `row["error"]`); recorder vẫn được gọi ở route — `test_phase6_live_smoke.py` cần key, không chạy thì ghi **NOT RUN** |
| S2 | Generator stream + bộ bóc chữ + chuẩn hóa từng phần + route `/api/chat/stream` + log | test logic §7; cổng ổn định cả hai route; pilot `incomplete` |
| S3 | Giao diện | Playwright trên server thật (§7) |
| S4 | Đo D2 trên trình duyệt | §6 C1–C3; ghi báo cáo + 5 chỗ (`WORKFLOW.md` §6) |

**C1 hoặc C2 trượt** ⇒ dừng trước khi đóng việc (không đo lại để "qua", không tự nới thước); A trình User: giữ PA1 với thước hiện có (nêu số), hay về PA3.

Ước công [Ước]: 2–4 ngày code + test + review (nháp v3 §1). Mỗi bước: khai báo file trong `STATUS_<X>.md`, nhánh riêng, skill `practical-project-coding`, report `<việc>_implementation.md`.

## 6. Tiêu chí nghiệm thu (bằng số)

| # | Tiêu chí | Ngưỡng | Cách đo |
|---|---|---|---|
| C1 | Tới chữ trả lời đầu tiên **hiện trên trình duyệt** (câu có trả lời) | p50 ≤ 3 s, p95 ≤ 5 s (+ mức chuẩn ngành **TBD**); báo `n` cạnh mỗi p50 / p95 | Playwright, `performance.now()` từ lúc bấm gửi tới lúc chữ đầu được vẽ; **40 câu** dev tự nhiên (không câu kín, không nhóm test), gồm ≥ 10 câu cần trả lời dài; câu dev bị model từ chối tính sang C2; chạy tuần tự, không việc nặng song song (W31). Với n ≈ 30–40, p95 gần như là câu chậm thứ hai ⇒ báo cả giá trị lớn nhất |
| C2 | Câu từ chối: tới lúc biết chắc là từ chối (≈ tới đủ câu, vì từ chối do model viết) | **cùng sàn** p50 ≤ 3 s, p95 ≤ 5 s; báo **riêng** nhóm này (A chốt 31/10: D2 (a) ghi câu từ chối trong cùng câu với sàn; số cả câu hôm nay p50 2,2 / p95 4,9 s đã sát sàn) | cùng lượt C1, thêm **≥ 10 câu ngoài kho tự viết** (cộng câu dev bị từ chối); báo `n` cạnh p50 / p95 |
| C3 | Tới đủ câu (sự kiện `done`) | đo + báo (theo dõi, không làm sàn) | cùng lượt C1; báo kèm lợi "đủ câu − chữ đầu" theo cặp, trung vị + CI 95 % (bootstrap) — lợi < 0,5 s ⇒ A xem lại theo D5 |
| C4 | Cổng ổn định | đạt cả 5 ý | (1) test file chạm; (2) `cd backend && HF_HUB_OFFLINE=1 uv run --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port <cổng trống>`: `/` 200, `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho (tự viết) trên **cả hai route**; số dòng `chat_metrics` mới = số lần gọi vào handler; grep câu hỏi trong log = 0; tắt server; (3) T1 giống byte; (4) đủ 5 chỗ báo cáo; (5) hook tự chạy |
| C5 | Chất lượng không đổi | T1 giống byte; trên ≥ 5 câu của C4 / C1: chữ ghép từ `delta` = chữ cuối đã chuẩn hóa (cùng một lần gọi); chữ cuối route stream thỏa **cùng luật** citation / từ chối như route JSON | log + chữ cuối trong lượt đo (lưu private `data/`); không chạy lại 176 câu có judge (bộ đánh giá không qua API; lõi chung giữ T1 + hành vi §4.8) |
| C6 | Tiền / câu | ≤ 0,0005 USD (cùng token như route JSON) | token vào / ra từ log lượt C1, theo giá User 30/10 (vào 0,10 · ra 0,50 · ghi đệm 0,125 USD / 1M) |
| C7 | Một dòng log mỗi lần gọi **vào handler** ở mọi ca | 100 % ca chạy được: xong, từ chối, `incomplete`, ngắt (2 thời điểm) | đếm dòng `chat_metrics` mới; `outcome` đúng ca; ca **ngắt** kiểm thêm: dòng log có mặt **và** bước đọc nốt `stream_events()` xong hay hết hạn (ghi vào report / log debug, không ghi chữ) |

## 7. Cách kiểm

**Đường thật** (server thật, model thật):
- cổng ổn định C4 cả hai route; thân rỗng / quá dài ⇒ 422 — ca này chỉ kiểm **lớp kiểm thân của FastAPI** (trước handler, không có dòng log), **không** kiểm nhánh lỗi trước luồng của
  cách (b). Các nhánh 503 / 409 / 500 context / 502 của route stream chỉ có khi gặp thật (không tắt Qdrant / đổi môi trường để tạo lỗi — `Session_Prompt.md` §8) ⇒ ghi giới hạn
  (§10); route stream dùng **chung** đoạn kiểm trước model với route JSON (lõi chung §4.8) nên đọc diff phải thấy cùng một đoạn code;
- `response.incomplete`: `answer_max_output_tokens` nhỏ trong lệnh thử. Token suy luận cũng tính vào trần ra (C73: 0 / trung vị 81 / lớn nhất 308 token / câu, 35 lần) ⇒ trần quá nhỏ thì
  hết token **trước** chữ đầu (`after_text = false`) ⇒ **pilot chọn trần** (vài giá trị, mỗi lần ~0,0003 USD) để có chữ trước khi hết token; ghi cả hai ca quan sát được;
- ngắt thật 2 thời điểm (trước chữ đầu, giữa chừng) bằng curl / Playwright: một dòng log, `outcome = client_disconnected`, token `None`, server không chạy tiếp;
- giao diện (Playwright, skill `webapp-testing`): chữ hiện dần, link `[n]` bật sau `sources`, ngắt thật, D3 (b) qua ca `incomplete` (nếu pilot ra được chữ trước khi hết token);
  2–3 ca Markdown / XSS (link `javascript:`, HTML lạ) qua DOMPurify;
- đo C1–C3, C6.

**Logic thuần phía server** (input nhỏ hợp lệ, không stub model):
- bộ bóc chữ JSON từng phần (7 ca C73 + thoát `\uXXXX` / `\"` cắt giữa mảnh) và chuẩn hóa `[Nguồn n]` khi `]` chưa tới;
- dựng chuỗi sự kiện từ danh sách mảnh chữ có sẵn: thứ tự `status … delta … sources | error … done`, `seq` tăng;
- D3 (a): chữ cuối không có `[n]` / có `[n]` sai số ⇒ `error{after_text: true}` rồi `done`, không có `sources`;
- lỗi bất kỳ trong `gen()` ⇒ `error` + `done`;
- định dạng SSE: một / nhiều dòng `data`, chữ có dấu không thoát.

**Ghi giới hạn "chưa kiểm bằng đường thật"** (không hứa test trình duyệt): giao diện xử lý D3 (a) (0 / 489 lần sinh trên cấu hình đang chạy; không tham số thật nào ép model bỏ `[n]`);
"luồng đứt không có `done`" (với `gen()` bắt mọi lỗi, chỉ đứt khi server chết / mạng đứt = đổi môi trường); dự án chưa có test JS.

## 8. Quyền và tiền

- Code trên nhánh riêng theo việc; B / C push nhánh riêng khi việc ghi rõ; A commit / push `main`. Đổi dependency nhỏ (`fastapi>=0.135`, bản đã cài): A tự duyệt (`Session_Prompt.md` §4).
- API trả phí (`gpt-6-luna`): pilot `incomplete` ≤ 0,001 USD; cổng ổn định ≈ 0,002 USD; đo C1 + C2 ≈ 50 câu + pilot ≈ 0,014 USD [Ước, 0,00025 USD / câu] ⇒ **trần cả việc 0,02 USD**, trong
  trần phiên. Lượt nào vượt ước > 50 % ⇒ dừng, báo A. Ghi usage token + tiền mỗi lượt.
- Không ghi Qdrant; không đổi kho / Golden.

## 9. Rủi ro

| Rủi ro | Cách giảm |
|---|---|
| Lõi chung làm đổi hành vi route JSON / bộ đánh giá | S1 làm riêng, T1 giống byte + cổng ổn định trước khi thêm stream; giữ 2 khác biệt §4.8 |
| Người dùng **đọc và làm theo** chữ đang chạy trước khi nó bị rút / xóa (câu điều kiện an toàn) | D3 xóa khi lỗi; tần suất đo được rất thấp (lỗi kiểm cuối 0 / 489; chưa từng gặp lỗi giữa chừng trong 8.621 dòng kết quả sinh đã lưu — cận dưới); D5 theo dõi |
| Log ghi sai khi stream (ghi trước khi luồng chạy, hoặc hai dòng) | ghi ở `finally` của `gen()`; C7 đếm mọi ca |
| Hủy không dừng model ⇒ tốn tiền; log ca ngắt bị mất | ghi log trước mọi `await`; `cancel()` + đọc nốt trong vùng che có hạn giờ (§4.5); ngắt thật ở §7, C7 |
| Proxy đệm khi deploy ⇒ mất lợi | header `X-Accel-Buffering: no`; kiểm khi chọn nơi deploy (ngoài phạm vi) |
| Lợi thật qua trình duyệt nhỏ hơn harness | C3 đo theo cặp; < 0,5 s ⇒ A đề xuất PA3 (D5) |

## 10. Giới hạn

- Bộ kiểm chỉ kiểm định dạng `[n]`, không kiểm nghĩa — streaming không làm hệ thống "không bịa" hơn hay kém hơn; trong vài giây người dùng có thể thấy chữ chưa qua kiểm.
- Số lợi 1,92 s là harness 10 câu, chưa qua API / trình duyệt; kho đã đổi 2 đợt từ lúc đo.
- Giao diện xử lý D3 (a) và "luồng đứt không có `done`": chưa kiểm bằng đường thật (§7).
- Nhánh lỗi trước luồng 503 / 409 / 500 context / 502 của route stream: chưa kiểm bằng đường thật (chỉ có khi gặp thật); ca 422 chỉ kiểm lớp FastAPI (§7).
- Hủy với model thật, usage của lần hủy, `incomplete` sau khi đã hiện chữ: suy từ code thư viện, kiểm khi làm (§7).
- Chưa có nghiên cứu người dùng về "hiện rồi rút / xóa"; D3 chọn theo thứ tự lỗi của User.
- Không đo trên điện thoại / mạng yếu / qua proxy; không kiểm trình đọc màn hình.
- Log `FileHandler` không xoay vòng (nợ cũ).
