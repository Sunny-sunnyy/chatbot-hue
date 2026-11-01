# Review: Streaming S2 — route `POST /api/chat/stream` (SSE)

Decision: **ready_for_user_confirmation**
Người kiểm: agent con ngữ cảnh mới do A giao (Claude Opus 5.5)
Date: 11:35 01/11/2026 (`date`)
Canonical guide: `docs/superpowers/specs/2026-10-31-streaming-design.md` (User duyệt `00fb57ee01b2`) — §4.1–4.8, §5 hàng S2, §6 C4 / C5 / C7, §7, §8, §10
Implementation report: `report_agent/2026-10-31_streaming_spec/s2_stream_route_implementation.md`

## 1. Phạm vi đã review

- Cổng tối thiểu: worktree `/tmp/b_s1` ở `830df0e` (khớp report), nhánh `s1-loi-chung`; untracked trong worktree chỉ là 2 symlink `data`, `knowledge-base-hue` (có sẵn từ S1, không thuộc diff).
  `git diff --name-status 9c83003 830df0e`: M `backend/api/routes/chat.py`, A `backend/llm/answer_stream.py`, M `backend/llm/generator_openai_full_corpus.py`, M `backend/llm/grounded_answer.py`,
  A `backend/tests/test_chat_stream.py`, M `pyproject.toml`, M `uv.lock` — khớp bảng §2 report, không có file ngoài phạm vi. `git diff --check 9c83003 830df0e`: sạch.
- Đọc exact diff cả 7 file; đọc code thư viện liên quan: `starlette/responses.py` `StreamingResponse` (Starlette 1.3.1), `uvicorn/protocols/http/httptools_impl.py` `receive` / `send` /
  `connection_lost` (uvicorn 0.52.1, báo `spec_version` 2.3 ⇒ Starlette đi nhánh task group + `listen_for_disconnect`).
- Đối chiếu từng ý spec: §4.1 luồng, §4.2 cách (b), §4.3 bước 1–5, §4.4 sự kiện, §4.5 hủy, §4.6 log, §4.8 khác biệt của route JSON.
- Tự viết 6 ca dò khác cách người làm (mục 3) + 3 lần gọi thật.

## 2. Findings

Không có blocker. Không có major.

### m-1 (minor) — cặp thoát surrogate `😀` bị cắt giữa hai mảnh ⇒ phát nửa ký tự, luồng lỗi

- **Vị trí:** `backend/llm/answer_stream.py:15` (`PARTIAL_ESCAPE`), `:20-35` (`decode_partial_string`); hệ quả ở `backend/api/routes/chat.py:269` (`sse_event`) và `:370`.
- **Yêu cầu:** spec §4.3 bước 2 (bóc chữ đúng cả khi mảnh cắt giữa `\uXXXX`), §6 C5 (chữ ghép từ `delta` = chữ cuối đã chuẩn hóa).
- **Bằng chứng [Chạy]** (`/tmp/a_s2_probe/p1_extractor.py`, `p1b_surrogate.py`): 10 câu biên × 4 dạng JSON × 400 cách cắt (gồm cắt từng ký tự) = 16.000 lần. Đạt hết **trừ** đúng một
  loại: chữ có ký tự ngoài BMP (ví dụ emoji) **và** JSON thoát kiểu ASCII (`😀`) — 784 / 800 lần hỏng. Mảnh cắt giữa hai nửa ⇒ `json.loads` trả nửa surrogate lẻ ⇒
  `sse_event` ném `UnicodeEncodeError` ⇒ `_answer_events` bắt thành `error{after_text: true}` (`stream_error_after_text`, giao diện sẽ xóa hết theo D3 (b)); đồng thời mảnh sau bị
  lệch một ký tự (ghép ≠ chữ cuối). Dạng UTF-8 thô (`ensure_ascii=False`) không hỏng (provider gửi `str`, không cắt giữa code point).
- **Tác động:** thấp. 7 / 7 lần gọi thật trên luồng (5 của người làm + 2 của tôi) có `delta_matches_final: true`, tức model gửi chữ thô; chỉ xảy ra nếu model thoát ASCII và có ký tự ngoài BMP.
  Không làm hiện chữ chưa kiểm — chỉ làm hỏng một câu đáng lẽ đúng.
- **Tiêu chí đóng (chọn một):** (a) giữ lại đuôi `\uD800–\uDBFF` chưa có nửa sau (hoặc bỏ ký tự surrogate cao ở cuối chữ đã giải mã khi chuỗi chưa đóng) + thêm 1 test cắt giữa cặp
  surrogate; chạy lại `p1_extractor.py` ⇒ 0 hỏng. Hoặc (b) ghi giới hạn này vào report / spec §10 kèm bằng chứng "model gửi chữ thô". Người kiểm nghiêng (a): sửa ~2 dòng, có test.

### m-2 (minor) — trường log `delta_matches_final` nằm ngoài danh sách spec §4.6

- **Vị trí:** `backend/api/routes/chat.py:43`, `:307`.
- **Yêu cầu:** spec §4.6 chỉ nêu 2 trường mới `first_event_ms`, `first_text_ms`.
- **Đánh giá:** giá trị chỉ là `true` / `false` / `null`, không chứa chữ ⇒ **không lộ nội dung** (giữ chính sách C59). Có ích thật: là cách đo C5 từ log không cần lưu chữ, và là
  tín hiệu theo dõi lúc dùng thật cho đúng mục tiêu spec §1 ("chữ còn lại trên màn hình là chữ đã qua kiểm") — giao diện giữ chữ đã hiện, nên lệch là điều cần biết. Chi phí 1 dòng.
  Người kiểm đề xuất **giữ**, không biến lệch thành "rút lại" (đó là đổi hành vi D3, cần User).
- **Tiêu chí đóng:** A ghi quyết định (giữ / bỏ) vào spec §4.6 hoặc mục việc; người làm không cần sửa code nếu giữ.

### Câu hỏi độ đơn giản — không thành finding

- `StreamEvents` (lớp): giữ trạng thái thật (`seq`, chữ đã gửi, `metrics`) và tách được phần không gọi model để test — tương xứng.
- `stopped_early`: có bằng chứng cần (report §4 "chạy hỏng rồi sửa": dựa `is_complete` thì bỏ qua bước đọc nốt).
- Nhánh `GeneratorExit`: tôi chạy được (mục 4, ca dò C) — có lý do tồn tại.
- Hai mã lỗi sau luồng (`generation_unavailable` / `internal_error`) dùng lại mã route JSON đang có, không thêm mã mới.
- `_run_config()`, `_generated_text()`: tách để hai đường gọi model dùng chung, đúng §4.3 bước 1.

### Ghi nhận ngoài phạm vi (không đưa vào correction)

- `EvidenceRecorder` chỉ được gọi ở phần trước model của route stream (qua `prepare_answer` / `_retrieval_not_ready`), không gọi `record_generation_result` / `mark_success` trong luồng.
  Spec §4.8 (4) chỉ ràng route JSON; người làm đã khai. Nếu sau này dùng recorder cho route stream thì phải bổ sung.
- Bộ bóc chữ giải mã lại cả chuỗi mỗi mảnh (O(n²)): đo [Chạy] `p3_cost.py` — 1.500 ký tự / 378 mảnh: 21 ms CPU; 3.000 ký tự: 101 ms; 8.000 ký tự (gần trần 2.048 token): 592 ms cả
  câu, rải theo luồng. Không đáng sửa trên máy cá nhân; xem lại nếu chạy nhiều người đồng thời.
- Cho S4 (không phải lỗi S2): 1 câu trong kho của tôi có `first_text_ms` server 4.077,6 ms; câu so sánh dài bị ngắt ở 3,0 s chưa có chữ. Cả hai là một lần chạy, không phải lượt đo
  D2, nhưng gợi ý C1 (sàn p95 ≤ 5 s đo trên trình duyệt) có thể sát với câu dài — A nên biết trước khi đo.

## 3. Cách người kiểm chạy lại thật

Mọi lệnh chạy từ `/tmp/b_s1/backend` với `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag`. Script ở `/tmp/a_s2_probe/` (ngoài repo).

1. Test không key: `python -m pytest tests/test_chat_stream.py tests/test_api_chat.py tests/test_grounded_answer.py tests/test_full_corpus_eval.py tests/test_citations.py -q`.
2. Ca dò A — `p1_extractor.py`: bộ bóc chữ, 16.000 lần cắt ngẫu nhiên (khác cách người làm: cắt từng ký tự và mảnh 1–9 ký tự; 4 dạng JSON gồm khoảng trắng quanh `:` và thoát ASCII; câu
   biên `[NGUỒN 2]`, `[ nguồn  3 ]`, `[1][2]`, `[[3]]`, `[Nguồn 1, 2]`, `[Ngày lễ]`, đuôi `[ng` / `[Nguồn 1` ở cuối chuỗi, `\\`, `\"`, `\t`, `\n`, xuống dòng giữa `[Nguồn\n1]`, chữ số Ả
   Rập, emoji). Kiểm sau **mỗi** mảnh: chữ đã gửi là tiền tố của chữ cuối; cuối: ghép `.strip()` == `normalize_citations(chữ.strip())`. `p1b_surrogate.py`: tái hiện m-1.
3. Ca dò B — `p2_route.py`: `create_app(load_settings())` **code route thật**, không chạy lifespan, phụ thuộc giả (tìm / dựng ngữ cảnh / generator giả — chỉ trong script dò, không phải
   chỗ nối trong code chính); không Qdrant, không model. Phần 1 (TestClient): 6 nhánh lỗi trước luồng trên cả hai route + từ chối không gọi model + thành công. Phần 2 (uvicorn thật,
   cổng 8792, socket thô): ngắt lúc **đang tìm** (handler chưa trả `StreamingResponse`) ×3, ngắt giữa chừng, ngắt khi server kẹt ở `send` (client không đọc, `SO_RCVBUF` 1–2 KB),
   hết giờ 0,3 s sau khi đã có chữ. `p2c_genexit.py`: lặp ca kẹt `send` với giữ 3 s / 6 s.
4. Ca dò C — `p4_genexit_direct.py`: gọi thẳng `_answer_events`, đọc tới `delta` đầu rồi (i) `aclose()` khi đang đứng ở `yield`, (ii) bỏ rơi generator ⇒ GC + hook asyncgen của loop.
5. Bất biến — `p5_json_parity.py`: cùng 11 đầu vào giả, chạy `/api/chat` trên code S1 (`git archive 9c83003 backend` ra `/tmp/a_s2_probe/s1src`, không đụng repo) và S2 (`/tmp/b_s1`),
   so từng dòng: mã HTTP, thân, số dòng `chat_metrics`, tập trường, giá trị mọi trường trừ `*_ms`.
6. Đường thật (có phí): `uvicorn api.app:app --port 8791` (`--env-file /home/minhhieu/hue_rag/.env`, chỉ truyền đường dẫn), model `gpt-6-luna`, Qdrant thật (chỉ đọc). `/` và `/health`;
   lấy mốc số dòng `logs/application.log` ngay trước; 3 lần `curl -N` lên `/api/chat/stream` với câu **tự viết**: 1 câu trong kho (kiến trúc một lăng), 1 câu ngoài kho (giá vé tàu điện
   ở một thành phố nước ngoài), 1 câu so sánh dài bị ngắt bằng `timeout 3.0 curl -N`. `p6_sse_check.py` kiểm thân SSE. Tắt server bằng `kill` đúng PID của uvicorn cổng 8791 tôi chạy.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Test không key | 53 passed, 1 error = `test_health_is_cached_and_ready_after_real_lifespan` thiếu key (đúng dự kiến của brief) |
| A — bộ bóc chữ | 16.000 lần: đạt hết trừ ca surrogate cắt giữa (m-1). Giữ `[Ngu` / `[Nguồn 1` tới `]` đúng; chữ đã gửi không bao giờ phải sửa; `[Nguồn n]` hoa / thường / khoảng trắng đều chuẩn hóa |
| B phần 1 — lỗi trước luồng | 6 / 6 nhánh (`retrieval_unavailable` 503 mặc định, 409 `corpus_reingest_required`, lỗi tìm 503, `context_budget_error` 500, `generation_unavailable` 502 chưa sẵn sàng, lỗi lạ ⇒ handler 500 `internal_error`): **mã + thân giống hệt** giữa hai route, mỗi lần gọi **1** dòng log, `outcome` / `status_code` đúng. Từ chối không gọi model (generator chưa sẵn sàng): 200, `status, delta, sources, done`, 1 dòng `refusal_no_sources`. Route JSON log 15 trường; route stream 18 |
| B phần 2 — ngắt lúc đang tìm ×3 | 3 / 3: **1** dòng `client_disconnected`, có drain. Lý do (đọc code uvicorn): sau khi đọc thân, uvicorn tạm dừng đọc socket nên chỉ biết client đóng khi `listen_for_disconnect` gọi `receive()` ⇒ luồng luôn kịp bắt đầu ⇒ `finally` chạy. Tôi nghi ca "0 dòng" (generator chưa kịp bắt đầu) — **không** xảy ra trên uvicorn này |
| B — ngắt giữa chừng | 1 dòng `client_disconnected`, log 0,001 s sau khi đóng, `cancel()` gọi, đọc nốt bằng iterator thứ 2 (`iter_calls=2`), drain `finished: true` |
| B — kẹt ở `send` (giữ 3 s, 6 s) | server dừng ở mảnh 72 / 122 (đang chờ ghi); đóng client ⇒ 1 dòng `client_disconnected`, drain xong. Hủy rơi vào lần chờ model chứ không vào `yield` (uvicorn `send` trả êm sau khi mất kết nối, generator chạy tiếp tới `await` kế) |
| B — hết giờ sau khi có chữ | `error` + `done`, 1 dòng `stream_error_after_text`, drain xong |
| C — `GeneratorExit` | (i) `aclose()` ở `yield`: không ném lỗi, **1** dòng `client_disconnected`, token `None`, `cancel()` + drain xong (3,0 ms). (ii) GC: như trên (0,1 ms). ⇒ nhánh người làm ghi "[Code, chưa chạy]" nay **đã chạy** bằng logic thuần; trên uvicorn thật vẫn chưa ép được (thứ tự task) |
| Bất biến — `/api/chat` S1 ↔ S2 | 11 / 11 ca **giống từng dòng** (`diff` rỗng): 6 lỗi trước model, lỗi sinh 502 `generation_failed`, citation hỏng 500, thành công có `[Nguồn 1]` ⇒ `[1]`, từ chối do model, từ chối không gọi model |
| Thật — `/`, `/health` | `/` 200; `/health` 200 `status: ok`, 5 thành phần `ready` |
| Thật — header | `text/event-stream; charset=utf-8`, `cache-control: no-cache`, `x-accel-buffering: no` |
| Thật — câu trong kho | `status{searched,10}`, `status{generating}`, 215 `delta` (`seq` 1…215 liên tục), `sources`, `done{success}`; số trích trong chữ {4,5,6,8} = id trong `sources`; không còn nhãn "Nguồn"; log `success`, `delta_matches_final: true`, `first_event_ms` 36,1, `first_text_ms` 4.077,6 |
| Thật — câu ngoài kho | 19 `delta` câu từ chối chuẩn, `sources []`, `done{success}`; log `refusal: true`, `delta_matches_final: true`, `first_text_ms` 1.128,0 |
| Thật — ngắt ở 3,0 s | client nhận `status, status` (trước chữ đầu); log **1** dòng `client_disconnected`, token `None`, `first_text_ms: null`; `chat_stream_drain {"finished": true, "ms": 0.5}` |
| Đếm log | mốc ngay trước: 229 dòng; sau: +4 dòng = **3** `chat_metrics` (= 3 lần gọi vào handler) + 1 `chat_stream_drain`; không dòng lỗi nào khác |
| Câu hỏi trong log | `grep -cF` từng câu trong toàn bộ `application.log`: 0 / 3; thêm 2 từ khóa riêng: 0 |
| Tắt server | `kill` PID uvicorn cổng 8791 ⇒ `curl /health` exit 7 (không kết nối được), `ss` không còn listener 8791. Server dò 8792 trong script đã dừng (`server stopped: True`) |

**Tiền (đường thật, 3 lần gọi):** log: câu trong kho vào 1.679 / ra 370 (gồm 137 suy luận); câu ngoài kho vào 2.247 / ra 31; lần ngắt không có usage (log `None`) — ước vào ≈ 2.000,
ra ≤ 400. Theo giá User 30/10 (vào tính giá ghi đệm 0,125 · ra 0,50 USD / 1M, cận trên): 0,00040 + 0,00030 + ≤ 0,00045 ⇒ **≈ 0,0011 USD**, dưới trần 0,002.

## 5. Giới hạn hoặc phần chưa chạy

- Nhánh `GeneratorExit` chạy được bằng gọi thẳng `_answer_events` (aclose / GC), chưa ép được trên uvicorn thật (hủy luôn rơi vào lần chờ model). Không ảnh hưởng decision: cả hai đường
  đều cho 1 dòng log + drain.
- Phụ thuộc giả ở ca dò B / C / bất biến chỉ nằm trong script dò để thử code route thật không tốn tiền; chúng không chứng minh hành vi provider. Phần provider dựa vào 3 lần gọi thật + report.
- Không chạy lại T1 158 câu và pilot `incomplete` (người làm đã chạy; phần đó không đổi giữa report và commit — dùng lại bằng chứng của report, không gọi là lần chạy mới). Không chạy
  `/api/chat` trên đường thật (bất biến route JSON kiểm bằng so S1 ↔ S2 trên code thật, phụ thuộc giả; report có 2 câu thật trên route JSON).
- Nhánh lỗi 503 / 409 / 500 / 502 của route stream chỉ kiểm bằng phụ thuộc giả (giới hạn spec §10 vẫn đúng cho đường thật).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.**

- Kết quả: route stream đúng chuỗi sự kiện §4.4, lỗi trước luồng ra cùng mã + thân với `/api/chat` (cùng đoạn code), mọi ca ngắt / hết giờ / lỗi ra đúng một dòng `chat_metrics` và đọc
  nốt có hạn giờ, route JSON không đổi hành vi so với S1 (11 / 11 ca). Câu hỏi không vào log.
- Hai minor không chặn S3: m-1 (người làm sửa ~2 dòng + 1 test, hoặc ghi giới hạn); m-2 (A ghi quyết định về trường `delta_matches_final` vào spec §4.6). Không mở vòng sửa riêng; người
  làm có thể gộp m-1 vào đầu S3.
- Việc rủi ro cao (luồng trả lời cho người dùng) ⇒ A trình User kết quả + giới hạn trên; S3 (giao diện) chỉ mở khi User / A đồng ý. Lưu ý cho S4: `first_text_ms` server ~4,1 s ở một câu
  trong kho (một lần chạy) — sát sàn C1.
- A commit / push file review này sau khi xử lý; người kiểm không commit.
