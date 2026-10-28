# Review: plan C70 — đo "thời gian tới chữ đầu tiên" (streaming)

Decision: **changes_requested** (0 blocker / 1 major / 4 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 09:40 28/10/2026 (`date`) · Việc: A giao 28/10 (review C70, WORKFLOW §9.1).
Bản review: `streaming_ttft_plan.md` sha `1e792df347fd` (B tính lại từ file lúc đọc: khớp; file chưa commit). 0 USD, chỉ đọc.
Chỉ dựa gói "Căn cứ để review" + hai file "thêm khi cần đối chiếu số" (C58, B65) + log `chat_metrics` (chỉ số). Không đọc STATUS_C, tin của C, bộ câu.

## 1. Phạm vi đã review

- Plan: toàn bộ (158 dòng).
- Gói căn cứ, đối chiếu từng `file:dòng` trên `main` `510e1a8`:
  - `backend/llm/generator_openai_full_corpus.py`: `:30-32` `AnswerOutput`; `:112-123` agent (`store=False` `:119`, `reasoning` chỉ khi có `reasoning_effort` `:120`,
    `output_type` `:122`); `:144-148` `AsyncOpenAI(max_retries=0)`; `:166-175` `Runner.run(max_turns=1)` trong `wait_for(timeout)`; `:187` `parse_structured_output`;
    `:196-204` usage lấy từ `raw_responses[-1]` (gồm `reasoning_tokens`).
  - `backend/api/routes/chat.py:107-157`, `:177-189`; `backend/api/app.py` (dựng service / builder / generator).
  - SDK `openai-agents` 0.19.4: `agents/run.py:375` `run_streamed`; `agents/result.py:525` `RunResultStreaming`, `:734` `cancel`, `:798` `stream_events`;
    `agents/models/openai_responses.py:1927-1938` gửi `text.format = json_schema "final_output"`; `agents/stream_events.py:9-19` `RawResponsesStreamEvent`.
  - `data/tinh_nang_moi_2026-10-27/c63_can_cu.md` §1, §2 "Streaming", §4 "Streaming".
- **Đạt (không cần sửa):** mọi `file:dòng` ở §2 đúng code (lệch ±1 dòng không đáng kể); tên hàm / thuộc tính harness dùng đều có (`generator.answer_agent`,
  `generator.client`, `build_answer_input`, `ANSWER_SYSTEM_INSTRUCTIONS`, `parse_structured_output`); không gửi `reasoning` ⇒ mức mặc định đúng (`from_environment`
  không đọc reasoning từ settings); NFC nằm trong `retrieval/full_corpus.py:420` (`search`) ⇒ harness gọi `retrieval_service.search` là đi qua NFC như production.
  "valid" = đúng điều kiện 200 của `chat.py` (tách JSON + `select_cited_sources(normalize_citations(…))`, hoặc câu từ chối chuẩn). Harness ghi từng dòng, từ chối
  ghi đè, không retry, có pilot kiểm sự kiện — đúng `run-experiment` §3.8. Plan trả lời đúng câu C63 nêu (phần suy luận + ~1,2 s không rút được).

## 2. Findings

### M-1 (major) — chỉ số quyết `saving_visible = N_total − S_first_visible` lấy từ **hai lần gọi khác nhau**, nhiễu quá lớn để phân định ngưỡng 1,5 s

- **Vị trí:** §7 `metrics` dòng `saving_visible_ms`, `saving_cited_ms` (role decide); `interpretation`; §7 "Cỡ mẫu".
- **Yêu cầu:** `run-experiment` §1 mục 3, 6 (chỉ số quyết định nghĩa chính xác; cỡ mẫu đủ phân giải trước khi chạy). A hỏi riêng: 10 câu × số lượt có đủ phân giải mức
  "≥ 1,5 s rõ" không.
- **Bằng chứng (*suy ra* từ số có sẵn):**
  - N và S là hai lần gọi model độc lập ⇒ hiệu `N_total − S_first_visible` mang toàn bộ dao động của **một lần gọi**: độ dài suy luận đổi theo lần gọi (log `chat_metrics`
    câu có trả lời: token suy luận 57–196), thời gian ≈ 1,16 s + 11,5 ms × token ra (C58 `c58_latency_theo_khau.md:39`, tương quan 0,97). Cùng đầu vào, SD chênh theo câu
    giữa hai lượt ≈ 808 ms (spec 8.2 §10.2).
  - Bản đủ: mỗi câu TB 2 lượt ⇒ SD ≈ 808 / √2 ≈ 570 ms; 8 câu trong kho, t₇ ≈ 2,36 ⇒ CI 95 % ≈ **±0,48 s** (chưa kể chênh thật giữa các câu). Bản gọn (1 lượt): ≈ **±0,67 s**.
  - Mức lợi ước trước: phần chữ hiện ra ≈ token ra − token suy luận. Log `chat_metrics` (3 câu có trả lời): 89–134 token ⇒ × 11,5 ms ≈ **1,0–1,5 s**. Ví dụ C63 §1: 225 − 112 =
    113 token ⇒ ≈ 1,3 s. ⇒ giá trị thật rất có thể nằm **ngay quanh ngưỡng 1,5 s** (và trên 0,5 s). CI ±0,5–0,7 s phủ cả "vừa" lẫn "rõ" ⇒ kết quả gần như chắc là "không phân
    định được dải", dù chạy bản đủ hay bản gọn.
  - Lượt 2 lặp **đúng** prompt lượt 1 (và N10 / S10 cùng prompt trong một lượt): context 10 ≈ 1,6–2 nghìn token vào ⇒ vượt ngưỡng cache prompt 1.024 token của OpenAI ⇒ lần gọi
    sau có thể được cache phần đầu vào ⇒ chữ đầu tiên sớm hơn. Người dùng thật hỏi câu mới ⇒ không có cache. Xoay vòng thứ tự cân trung bình nhưng thêm nhiễu, và lượt 2
    không còn là lượt lặp độc lập cho phần trước chữ đầu tiên. (Context 5 ≈ 950 token vào — C58 `:37` — dưới ngưỡng.)
- **Tác động:** ô quyết khó ra kết luận dùng được; "2 lượt cho A/A" bị cache làm lệch.
- **Gợi ý (C chọn, hoặc phản biện bằng số):** tách lợi thành hai phần.
  - (1) **Phần trong cùng một lần gọi stream:** `S_done − S_first_visible` (và `S_done − S_first_cited_sentence`). Đây đúng là thời gian sinh phần chữ hiện ra, cùng lần gọi,
    không có nhiễu suy luận giữa hai lần gọi, không bị cache (cache chỉ rút phần trước chữ đầu tiên). Nhiễu còn lại chủ yếu là chênh thật giữa các câu (độ dài câu trả lời)
    ⇒ 10 câu × 1 lượt đủ phân định dải trừ khi giá trị cách ngưỡng < ~0,2 s.
  - (2) **Phần thêm của đường stream:** `S_done − N_total` (đã có: `total_overhead_ms`, watch). Lợi người dùng thấy = (1) − (2). Báo (2) kèm CI riêng; (2) ≈ 0 ⇒ lợi ≈ (1).
  - Ghi `usage.input_tokens_details.cached_tokens` mỗi lần gọi (Responses API trả trong usage) và báo các mốc trước chữ đầu tiên (`t_first_event`, `t_first_delta`,
    `t_first_visible`) **tách** dòng có cache / không cache. Nếu vẫn cần A/A cho phần trước chữ đầu tiên: dùng **câu khác** (ví dụ bộ 22 câu B65) thay vì lặp đúng prompt.
- **Tiêu chí đóng:** chỉ số quyết đổi sang phần trong cùng lần gọi (hoặc giữ cách cũ kèm phép tính độ phân giải cho thấy đủ phân định ngưỡng 500 / 1.500 ms); §7 "Cỡ mẫu" ghi
  phép tính đó; có trường `cached_tokens` và luật báo tách; số lượt / ô chọn lại theo chỉ số mới (bản gọn có thể đủ — xem §6 ý kiến cho A).

### m-1 (minor) — bối cảnh B1 / B0 ở §2 và §4 đã cũ

- `streaming_ttft_plan.md:39-41`, `:69-71` ghi "B0 chưa xong ⇒ chưa biết chatbot chạy context nào", "context 5 dùng nếu B1 không merge". Từ 28/10: spec 8.2 §11 (B0 không chặn
  B1) và `main` `510e1a8` đã merge `p82-b1` (`settings.yaml:55` `max_context_documents: 10`). ⇒ N10 / S10 **là** production; context 5 chỉ còn lý do "B0 sau này có thể đưa
  về 5" (§11 luật dừng).
- **Tiêu chí đóng:** sửa hai đoạn theo hiện trạng; ghi lý do còn giữ context 5 (hoặc bỏ để gọn).

### m-2 (minor) — D5 so "lớp SDK Agents thêm trễ" bằng mốc có nhiễu suy luận

- §4 dòng D5: so D5 với S5 ở `t_first_visible` / `t_done` thì cũng là hai lần gọi khác nhau ⇒ cùng nhiễu ≈ ±0,5 s ở M-1, trong khi trễ lớp SDK (nếu có) nhiều khả năng chỉ vài chục ms
  [S] ⇒ 10 lần gọi không thấy được. Mốc ít nhiễu hơn: `t_first_event` (`response.created`, trước khi model suy luận). D5 chạy context 5 trong khi production nay là 10.
- **Tiêu chí đóng:** nếu giữ D5: chỉ số so = `t_first_event` (và trễ giữa sự kiện raw cuối và lúc `stream_events()` kết thúc), context 10; nếu không, `NOT RUN` như plan đã cho.

### m-3 (minor) — timeout với `run_streamed`

- §4 dòng S5: "`run_streamed(…)` trong `wait_for(45 s)`". `run_streamed` trả ngay `RunResultStreaming` (`agents/run.py:375`), việc chạy nằm ở vòng `async for … stream_events()`
  (`agents/result.py:798`) ⇒ `wait_for` phải bọc **cả vòng tiêu thụ sự kiện**; hết giờ thì gọi `result.cancel()` (`agents/result.py:734`) để không còn task nền gọi model
  (vẫn tính tiền).
- **Tiêu chí đóng:** §6 ghi rõ cách bọc timeout + `cancel()`; người review code (B) kiểm điểm này.

### m-4 (minor) — ghi mức lợi ước trước để đối chiếu

- Plan có ngưỡng diễn giải ghi trước (tốt) nhưng chưa ghi **dự đoán** từ số có sẵn (M-1: ≈ 1,0–1,5 s). Ghi trước giúp phát hiện mốc đo sai (ví dụ `t_first_visible` tính từ JSON
  prefix sai) khi kết quả lệch xa dự đoán.
- **Tiêu chí đóng:** §7 thêm một dòng `prediction` [S] kèm nguồn.

## 3. Cách người kiểm chạy lại thật

Chỉ đọc, 0 USD:
- `sha256sum report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_plan.md | cut -c1-12` ⇒ `1e792df347fd`.
- `grep -n` các dòng ở §1 trong `backend/llm/generator_openai_full_corpus.py`, `backend/api/routes/chat.py`, `backend/api/app.py`, `backend/retrieval/full_corpus.py`, và SDK
  trong `.venv` (`openai_agents` 0.19.4, `METADATA`).
- Log `backend/logs/application.log`: tách dòng `chat_metrics` (chỉ số, không nội dung), lấy câu `status_code == 200` có trả lời ⇒ `output_tokens − reasoning_tokens`
  (3 câu: 89 / 115 / 134), `reasoning_tokens` (57–196).

## 4. Kết quả quan sát

- Mọi khẳng định [N] của plan mà B kiểm đều đúng code (§1 "Đạt").
- Ước độ phân giải và mức lợi ở M-1 là **suy ra** (từ C58, spec 8.2 §10.2, 3 dòng log, ví dụ C63) — chưa đo; cỡ mẫu log nhỏ (3 câu) ⇒ chỉ cho thứ bậc độ lớn.

## 5. Giới hạn hoặc phần chưa chạy

- Không đọc bộ câu `data/streaming_ttft_2026-10-28/questions.jsonl` (ngoài gói căn cứ); không kiểm sha `107620cb30f1`, NFC, overlap của bộ câu.
- Chưa kiểm bằng chạy thật rằng Responses API stream ra `output_text.delta` khi có `output_type` và có mục `reasoning` khi `store=False` — plan đã giao pilot kiểm (đúng chỗ).
- Ngưỡng cache prompt 1.024 token và trường `cached_tokens`: theo tài liệu OpenAI B biết, **chưa** đối chiếu bằng WebFetch trong review này.

## 6. Decision và bước tiếp theo

`changes_requested`: C sửa M-1 (bắt buộc), minor nên gộp; báo sha mới ⇒ B kiểm phần sửa ⇒ A duyệt sha.

Ý kiến cho A (câu A hỏi riêng; A quyết):
- **Bản đủ hay bản gọn:** với chỉ số quyết hiện tại, cả hai đều khó phân định ngưỡng 1,5 s (±0,48 s / ±0,67 s quanh giá trị ước ≈ 1,0–1,5 s) ⇒ thêm lượt 2 **không** mua được
  kết luận, còn bị cache làm lệch. Nếu đổi sang chỉ số trong cùng lần gọi (M-1), **10 câu × 1 lượt, chỉ context 10** (N10 + S10 ≈ 20 lần gọi ≈ 0,004 USD + pilot) là đủ cho câu
  hỏi chính; context 5 chỉ cần nếu A muốn số dự phòng cho trường hợp B0 đưa về 5 (phần chữ hiện ra phụ thuộc độ dài câu trả lời hơn là context).
- **D5:** chỉ đáng giữ nếu so bằng `t_first_event` ở context 10 (m-2); so bằng chữ đầu tiên thì 10 lần gọi không đủ thấy trễ cỡ vài chục ms ⇒ `NOT RUN` không mất gì.

## Vòng 2 — kiểm phần sửa (bản 2, sha `9683641b6c38`)

Decision vòng 2: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor mới — không chặn; C sửa thì là bản mới, B kiểm lại phần đó)
Date: 09:51 28/10/2026 (`date`). B tính lại sha từ file: `9683641b6c38` (226 dòng, chưa commit). Đọc lại toàn bộ plan bản 2 (khối "Bản 2 sửa theo review B" + các mục đổi).

| Finding vòng 1 | Bản 2 | Kết quả |
|---|---|---|
| M-1 chỉ số quyết hai lần gọi; cache | §7: quyết = `S_done − S_first_visible` / `S_done − S_first_cited_sentence` (cùng lần gọi); `stream_overhead_ms = S_done − N_total` thành watch + `overhead_rule` (lợi người dùng thấy = gain − overhead); bỏ lượt 2; S10 luôn gọi **đầu** với prompt đó (D10, N10 sau ⇒ chỉ N / D có thể dính cache ⇒ overhead bị ước lớn — thiên về bất lợi cho streaming, có ghi); `cached_tokens` mọi dòng, số trước chữ đầu tiên tách có / không cache; "Cỡ mẫu" ghi lý do + luật mở rộng ghi trước (CI chứa ngưỡng 500 / 1.500 ms hoặc < 6 câu có trả lời ⇒ +1 lượt S10 + N10 trên bộ 22 câu B65, A duyệt trước) | **đóng** |
| m-1 bối cảnh B1 / B0 cũ | §2: B1 merge `510e1a8`, `settings.yaml:55` = 10; context 5 `NOT RUN` kèm lý do | **đóng** |
| m-2 D5 so bằng mốc nhiễu | D10 ở context 10, so bằng `t_first_event` và `t_done − t_last_event` (`sdk_overhead_ms`) | **đóng** |
| m-3 timeout `run_streamed` | §6: `wait_for(consume(result), 45 s)` bọc cả vòng `stream_events()`; `result.cancel()` (mặc định `immediate`, `agents/result.py:734`) trong `finally` khi luồng chưa xong; D10 đóng luồng trong `finally`; §9 B kiểm điểm này ở code | **đóng** |
| m-4 dự đoán ghi trước | §7 `prediction` + `check` (gain < 0,3 s hoặc > 3 s ⇒ kiểm lại cách tính mốc) | **đóng** |

Kiểm bằng máy (chỉ đọc): `agents/usage.py:13-29` có `input_tokens_details.cached_tokens`; `cancel(mode="immediate")` ở `agents/result.py:734`; `run_streamed` nhận `max_turns`,
`run_config` (`agents/run.py:375-382`); bộ mở rộng `data/phase_8_2/latency_2710/questions.jsonl` sha `bac5c91db005`, 22 dòng — khớp plan. Tiền: 35 × 0,000204 ≈ 0,0071 USD — khớp.

### n-1 (minor mới) — `cached_tokens = 0` có thể là "không có trường", không phải "không cache"

- SDK điền mặc định 0 khi provider không trả trường (`agents/usage.py:15-17`: `getattr(details, "cached_tokens", 0) or 0`; `:3, :9` mặc định 0) ⇒ ở S10 (đọc usage qua SDK),
  pilot "usage … có `cached_tokens`" (§6) **luôn qua**, kể cả khi provider không báo cache. Ảnh hưởng nhỏ: S10 là lần gọi đầu với prompt nên kỳ vọng thật là 0; nhưng luật
  "tách có / không cache" ở N10 / D10 sẽ không phân biệt được nếu trường vắng.
- **Đóng (khi tiện):** pilot kiểm trường có thật ở **sự kiện raw** `response.completed` (D10: `response.usage.input_tokens_details` có khóa `cached_tokens`), ghi kết quả vào meta;
  vắng ⇒ ghi "cache: không đo được" thay vì 0. Không cần vòng review riêng — B kiểm ở code harness (§9).

**Kết luận vòng 2:** M-1 và 4 minor vòng 1 đều đóng; plan bản 2 trả lời được câu A hỏi (độ phân giải) bằng chỉ số trong cùng lần gọi, có luật mở rộng ghi trước khi số rơi gần
ngưỡng. Bản `9683641b6c38` sẵn để A duyệt sha. Câu §10 (giữ D10; người viết harness): ý kiến B như vòng 1 §6 — D10 nay so bằng `t_first_event` nên đáng giữ (+0,002 USD).
