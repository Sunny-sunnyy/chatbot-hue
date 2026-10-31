# Review: B105 — spec streaming (`docs/superpowers/specs/2026-10-31-streaming-design.md`)

Decision: **changes_requested** (1 major, 4 minor; không có blocker)
Người kiểm: B (Claude Opus 5.5) · Date: 11:58 31/10/2026 (`date`)
Việc được kiểm: spec bản 1 `c820ec0e18e7` (C viết, chưa commit). Căn cứ: mục "Căn cứ để review" đầu spec + các dòng "User chốt D1 / D2 / D3" và mục C100 trong
`CURRENT_HANDOFF.md` + code `main` theo `file:dòng` spec ghi. **Không** đọc `STATUS_C.md` / tin nhắn của C. Phần "mức chuẩn ngành cho chữ đầu tiên" đang `TBD` — bỏ qua vòng này (A điền sau).
File này tracked: không chép nội dung kho, câu Golden / câu kín, hay chi tiết dự án khác.

## 1. Phạm vi đã review

- Đọc hết spec (203 dòng). Đối chiếu năm ưu tiên A ghi ở B105: (1) khớp đúng quyết định User, không thêm / bớt; (2) C1–C7 đo được bằng đường thật; (3) S1 giữ đúng các khác biệt
  `answer_case` ↔ route (§4.8); (4) test không va `Session_Prompt.md` §6 / §8; (5) repo public.
- `uv run python .githooks/overlap_scan.py <spec>` ⇒ **0 dòng trùng** với Golden / kho / câu kín ✓. Không thấy chi tiết dự án khác.
- Một probe chạy thật (uvicorn, không model, 0 USD) cho M-1.

## 2. Findings

### M-1 (major) — §4.5 "`finally` gọi `result.cancel()` rồi **đọc nốt** `stream_events()`" không chạy được như viết khi người dùng ngắt

- **Vị trí:** spec §4.5 gạch 1; liên quan §4.6 ("ghi log ở `finally` của `gen()`") và §9 dòng "Hủy không dừng model".
- **Yêu cầu bị ảnh hưởng:** hủy đúng cách theo docstring SDK (`agents/result.py:757-758` "continue consuming stream_events()"); C7 "một dòng log mỗi lần gọi ở mọi ca, kể cả ngắt".
- **Bằng chứng [Chạy, B 31/10, uvicorn 0.52.1 + Starlette 1.3.1 thật, không model]:** probe private `data/tinh_nang_moi_2026-10-27/tools/b105_drive.py` + `b105_app.py`. Generator của
  `StreamingResponse` gửi một sự kiện rồi `await` (đứng chỗ "đang chờ model"); client ngắt sau 0,5 s; trong `finally` gọi một hàm có 5 lần `await` (đứng chỗ "đọc nốt").
  - `finally` thường ⇒ **`CancelledError` ngay ở `await` đầu**, không đọc được lần nào.
  - bọc `with anyio.CancelScope(shield=True):` ⇒ đọc đủ **5 / 5**, 101 ms.
  - Lý do: Starlette hủy bằng cancel scope của anyio (`starlette/responses.py:265-280`, nhánh ASGI < 2.4). Hủy kiểu này lặp lại ở **mọi** điểm `await` sau đó trong scope.
- **Tác động:** bước "đọc nốt" của §4.5 sẽ luôn bị bỏ. Nặng hơn: mọi việc trong `finally` đặt **sau** một `await` (kể cả ghi `chat_metrics` nếu đặt sau `await drain`) cũng không chạy ⇒
  dòng log ca `client_disconnected` mất, C7 trượt. Lỗi này chỉ lộ khi ngắt thật — C7 có ca ngắt nên sẽ thấy lúc nghiệm thu, nhưng spec đang chỉ người làm đi đường không chạy được.
- **Tiêu chí đóng:** §4.5 ghi rõ: (1) trong `finally`, ghi `chat_metrics` **trước** mọi `await` (hoặc trong vùng che); (2) `result.cancel()` (đồng bộ) rồi đọc nốt `stream_events()`
  **trong `anyio.CancelScope(shield=True)` có giới hạn thời gian** (ví dụ `anyio.move_on_after(…)` bên trong), để luồng hỏng không treo server; (3) C7 ca "ngắt" kiểm cả việc dòng log có mặt
  lẫn việc đọc nốt xong / hết hạn (ghi ra log debug hoặc report, không ghi chữ).

### m-1 (minor) — C5 "chữ ghép từ `delta` = chữ cuối đã chuẩn hóa" sẽ báo sai khi model viết khoảng trắng đầu / cuối

- **Vị trí:** spec §4.3 bước 4; §6 C5.
- **Bằng chứng:** chữ cuối lấy qua `parse_structured_output` ⇒ `return str(val).strip()` (`backend/llm/generator_openai_full_corpus.py:81`). Còn `delta` là chữ bóc từ JSON đang chạy, chưa `strip`.
- **Tiêu chí đóng:** viết rõ phép so: `"".join(delta).strip()` (sau chuẩn hóa `[Nguồn n]`) == chữ cuối. Hoặc nói rõ giao diện hiện chữ nào khi khác nhau.

### m-2 (minor) — §4.8 chỉ kể 2 khác biệt `answer_case` ↔ route; code còn ít nhất 3

- **Vị trí:** spec §4.8 ("Hai chỗ hiện khác nhau mà lõi chung **không được làm đổi**"); §5 S1.
- **Bằng chứng (đọc code, khác chỗ người viết):**
  - (3) **lỗi kỹ thuật:** `answer_case` bắt **mọi** lỗi thành `row["error"]` ⇒ lượt chấm thành incomplete (`backend/evaluation/full_corpus_eval.py:362-363`); route đổi từng lỗi ra mã riêng
    (503 / 409 / 500 context / 502, `backend/api/routes/chat.py:94-168`);
  - (4) **route gọi `EvidenceRecorder`** ở 10 chỗ (`chat.py`, `recorder.…`), `answer_case` không gọi. Recorder chỉ do `test_phase6_live_smoke.py` dùng;
  - (5) `answer_case` ghi `response_id`, `latency_ms`, token vào dòng kết quả (`full_corpus_eval.py:348-353`); route **không** log id (chính sách C59, `chat.py:22-25`).
  Hai khác biệt spec đã ghi (chuẩn hóa citation, giữ chữ khi citation hỏng) đúng: `full_corpus_eval.py:355-359` gọi `select_cited_sources(answer, …)` trên chữ **chưa** chuẩn hóa.
- **Tiêu chí đóng:** §4.8 liệt kê đủ (hoặc ghi "ít nhất các khác biệt sau", kèm 3 ý trên). S1 thêm kiểm: ca lỗi của `answer_case` vẫn ra `row["error"]` (không đổi thành mã HTTP), và
  recorder vẫn được gọi ở route (live smoke cần key — nếu không chạy thì ghi NOT RUN).

### m-3 (minor) — C1 / C2: chưa ghi cỡ nhóm câu từ chối, và không nói làm gì khi C1 trượt

- **Vị trí:** spec §6 C1, C2.
- **Bằng chứng:** C1 = 40 câu (≥ 10 câu dài). C2 lấy "cùng lượt C1 (bộ 40 câu có câu ngoài kho tự viết…)" nhưng không ghi **bao nhiêu** câu từ chối. Với ~30 câu có trả lời, p95 gần như là
  câu chậm thứ hai. Với vài câu từ chối, p95 không có nghĩa. Số "chữ đầu" đã có (harness, 10 câu) p95 4,80 s đã sát 5 s trước khi cộng API + trình duyệt ⇒ C1 có thể trượt thật. Spec chỉ có
  luật xem lại cho C3 (lợi < 0,5 s), không có luật cho C1 / C2 trượt.
- **Tiêu chí đóng:** ghi số câu từ chối (ví dụ ≥ 10) và báo `n` cạnh mỗi p50 / p95. Thêm một dòng: "C1 hoặc C2 trượt ⇒ dừng trước bước giao diện cuối / đo lại, A trình User (giữ PA1 với thước
  hiện có / về PA3)". Không tự nới thước.

### m-4 (minor) — §4.3 gán sai chỗ hai tham số của lần gọi model

- **Vị trí:** spec §4.3 bước 1: "`answer_agent` hiện có (`generator_openai_full_corpus.py:112-123`: `output_type`, `max_tokens` 2.048, `store=False`, `max_turns=1`, `tracing_disabled=True`)".
- **Bằng chứng:** định nghĩa agent (`:112-123`) có `max_tokens`, `include_usage`, `store=False`, `reasoning`, `output_type`. Còn `max_turns=1` và `RunConfig(tracing_disabled=True,
  trace_include_sensitive_data=False)` nằm ở **lần gọi** `Runner.run` (`:162-172`).
- **Tác động:** gọi `Runner.run_streamed` chỉ với agent sẽ mất `max_turns=1` và `tracing_disabled` (mặc định SDK khác) ⇒ hai đường gọi model khác nhau.
- **Tiêu chí đóng:** ghi "`Runner.run_streamed` với **cùng** `answer_agent` **và cùng** `max_turns=1` + `RunConfig` như `:162-172`".

## 3. Đã dò, đúng (không phải finding)

| Ưu tiên | Khẳng định spec | Cách B dò | Kết quả |
|---|---|---|---|
| (1) | §2 bảng quyết định: D1 = PA1 (11:26), D2 = (a) (11:44), D3 = phương án 1 (11:48), D5 1 % / ≥ 3 trên ≥ 100, không nút Dừng, lỗi trước luồng cách (b), `incomplete` không phải lỗi giả, không chỗ nối test, giữ JSON | so nguyên văn các dòng "User chốt …" + C100 trong `CURRENT_HANDOFF.md` | ✓ khớp, không thêm / bớt. Điều kiện xem lại của D1 (lợi < 0,5 s; xóa > D5) có ở dòng D5 |
| (1) | C2 "cùng sàn" là A chốt (kỹ thuật trong D2) | D2 của User ghi "(câu từ chối: tới lúc biết chắc là từ chối)" ngay trong câu sàn | ✓ ghi đúng người quyết |
| (2) | C4 cổng ổn định, C5 T1 giống byte, C7 đếm dòng log mọi ca | đều chạy bằng server / model thật; ca `incomplete` có pilot | ✓ — trừ M-1 (ca ngắt) và m-1 (phép so C5) |
| (4) | §7 tách đường thật / logic thuần / giới hạn; không tắt Qdrant; `incomplete` bằng tham số thật; không chỗ nối test | đối chiếu quyết định A (B102) | ✓ |
| — | §4.2 lỗi trước luồng: 5 nhánh tới `chat.py:153`; `generation_failed` 502 `chat.py:156-168` thành 200 + `error{after_text:false}` | đọc `chat.py:86-168` | ✓ |
| — | §4.7 `app.js:18-75` (`renderSources` 18, `wireCitations` 39, `renderResponse` 71), `:86-93`, `:95-97`, `:11-14`, `:78`; `index.html:25` | `grep ^function` + đọc | ✓ |
| — | §4.6 test khóa tập trường | `backend/tests/test_api_chat.py:88` `assert set(lines[0]) == set(METRIC_FIELDS)` | ✓ |
| — | §4.4 / §4.5 hủy < 10 ms (B100 vòng 2) | là số đo lúc generator đang chờ; M-1 bổ sung chuyện **sau** khi bị hủy | ✓ (xem M-1) |
| (5) | public | quét trùng 0; chỉ trỏ đường dẫn `data/…`, không chép nội dung | ✓ |

**Câu bất biến:** spec không đổi hệ thống đang chạy (tài liệu, chưa code). `POST /api/chat` giữ nguyên ghi rõ ở §1, §3 ✓.

## 4. Cách người kiểm chạy lại thật

- `uv run --project /home/minhhieu/hue_rag python -I data/tinh_nang_moi_2026-10-27/tools/b105_drive.py`: mở uvicorn ở cổng trống, 2 endpoint (`/plain`, `/shield`), client httpx ngắt sau
  0,5 s, đọc log probe, tắt server. 0 USD. Kết quả: `{"mode": "plain", "drained": "FAILED", "err": "CancelledError"}` · `{"mode": "shield", "drained": 5, "ms": 101}`.
- `uv run python .githooks/overlap_scan.py docs/superpowers/specs/2026-10-31-streaming-design.md` ⇒ 0 trùng.

## 5. Giới hạn

- Probe M-1 dùng `asyncio.sleep` thay `stream_events()` thật. Hành vi hủy của anyio không phụ thuộc thứ được `await` ⇒ kết luận áp dụng, nhưng thời gian đọc nốt với model thật chưa đo.
- Phần `TBD` (mức chuẩn ngành) chưa review — vòng sau.

## 6. Decision

`changes_requested` — C sửa M-1 + m-1…m-4 trong một lượt, báo sha mới. B kiểm lại §4.3, §4.5, §4.6, §4.8, §5 S1, §6 C1 / C2 / C5 / C7 + phần `TBD` khi A điền. Sau ready ⇒ Codex review
một lần (W33, gói `data/tinh_nang_moi_2026-10-27/b104_codex_review_spec.md`) ⇒ User duyệt sha.

---

# Vòng 2 — kiểm spec bản 2 (`e243371b57eb`)

Decision: **ready_for_user_confirmation** (M-1 + m-1…m-4 đóng; 1 ghi chú nhỏ, không mở vòng; phần `TBD` chưa review — vòng sau khi A điền) · Người kiểm: B · Date: 12:03 31/10/2026 (`date`)

## R2.1 Đóng finding vòng 1

| Finding | Chỗ sửa ở bản 2 | Đóng? |
|---|---|---|
| M-1 | §4.5 viết lại: nêu cơ chế hủy của anyio + số probe B105 (0 / 5 ↔ 5 / 5, 101 ms); `finally` theo thứ tự (1) ghi `chat_metrics` **trước mọi `await`** (đồng bộ), (2) `result.cancel()` (đồng bộ), (3) đọc nốt `stream_events()` trong `anyio.CancelScope(shield=True)` + `anyio.move_on_after(…)` bên trong; §4.6 thêm "trước mọi `await`"; C7 ca ngắt kiểm cả dòng log lẫn đọc nốt xong / hết hạn; §9 dòng hủy sửa | ✓ đúng tiêu chí đóng |
| m-1 | §4.3 bước 4: so `"".join(delta).strip()` (sau chuẩn hóa) với chữ cuối, dẫn `:81` | ✓ |
| m-2 | §4.8 "**ít nhất**" 5 khác biệt, kèm `file:dòng` (`full_corpus_eval.py:348-353, :355-359, :362-363`; `chat.py:92, :94-168, :24-25`); S1 kiểm 5 khác biệt + recorder, live smoke NOT RUN nếu không chạy | ✓ — B kiểm lại `chat.py:92` = `recorder = get_current_recorder()` |
| m-3 | C1 / C2 báo `n` + giá trị lớn nhất; C2 thêm ≥ 10 câu ngoài kho tự viết + câu dev bị từ chối; luật "**C1 hoặc C2 trượt** ⇒ dừng trước khi đóng việc, không đo lại để qua, không tự nới thước; A trình User" (dòng 154); §8 tiền theo ~50 câu (≈ 0,014 USD, trần việc vẫn 0,02) | ✓ |
| m-4 | §4.3 bước 1 tách tham số của agent (`:112-123`) và tham số của lần gọi (`:162-172`: `max_turns=1`, `RunConfig(tracing_disabled=True, trace_include_sensitive_data=False)`) | ✓ |

Ngoài các chỗ khai báo, B không thấy chỗ đổi nào khác (đọc lại §4.3–§4.8, §5 S1, §6, §7, §8, §9). Quét trùng: `overlap_scan.py` ⇒ **0 trùng**; 0 dòng có khoảng trắng cuối.

## R2.2 Dò khác cách (cho phần mới ở §4.5)

- Đọc `agents/result.py` (0.19.4 đã cài): `cancel(mode="immediate")` hủy task nền ngay (đồng bộ) rồi đẩy `QueueCompleteSentinel`. Các chỗ `stream_events()` chờ task nền đều qua
  `_await_task_safely` (bỏ qua `CancelledError` của task đã bị hủy) ⇒ đọc nốt sẽ xong nhanh. `move_on_after` chỉ là rào cho ca lạ ⇒ thiết kế hợp lý.
- **n-1 (ghi chú, không mở vòng):** tài liệu SDK (trang Streaming, B99 đã trích) dặn đọc nốt bằng **iterator mới** — "Use a fresh iterator in case cancellation already closed the
  original". Khi Starlette hủy `gen()` đúng lúc đang `async for … in result.stream_events()`, iterator đó đã nhận `CancelledError` và đóng. Nên §4.5 bước 3 thêm mấy chữ "gọi lại
  `result.stream_events()` (iterator mới)". Người làm sửa luôn khi code cũng được; C7 ca ngắt sẽ thấy nếu sai.

## R2.3 Decision

`ready_for_user_confirmation` cho phần đã có (phần `TBD` "mức chuẩn ngành chữ đầu tiên" review vòng sau). Bước tiếp theo W33: Codex review một lần theo gói
`data/tinh_nang_moi_2026-10-27/b104_codex_review_spec.md`, trên **đúng** bản `e243371b57eb` (hoặc bản sau khi A điền `TBD` — sha mới thì B kiểm phần đổi trước) ⇒ User duyệt sha.
