# C70 — Plan đo "thời gian tới chữ đầu tiên" (streaming) — chưa chạy

Người viết: C (Claude Opus 5.5, `hue-rag-32`) · bản 1 09:27 28/10/2026, **bản 2 09:47 28/10/2026** (`date`) · Việc: C70 (`session_prompt/CURRENT_HANDOFF.md` "### C70").
Người review: B. Plan **chỉ viết**, 0 USD; chạy sau khi A duyệt sha. Không sửa `backend/` trong việc này.
Nhãn: **[N]** = nguồn / code nói (có `file:dòng`); **[S]** = C suy ra, chưa đo.

**Bản 2 sửa theo review B** (`streaming_ttft_plan_review.md`, bản 1 `1e792df347fd`, changes_requested 0 / 1 / 4):
- **M-1:** chỉ số quyết đổi sang phần đo **trong cùng một lần gọi stream** (`S_done − S_first_visible`). Phần thêm của đường stream (`S_done − N_total`) tách ra
  thành dòng theo dõi. Có ghi `cached_tokens`; bỏ lượt 2 lặp đúng prompt (§4, §7).
- **m-1:** cập nhật hiện trạng: B1 đã merge (`510e1a8`), context 10 là production ⇒ bỏ ô context 5 (§2, §4).
- **m-2:** D10 so bằng `t_first_event` và độ trễ ở đuôi luồng, ở context 10 (§4).
- **m-3:** `wait_for` bọc cả vòng `stream_events()`; hết giờ thì `cancel()` (§6).
- **m-4:** thêm dự đoán ghi trước (§7).

## Căn cứ để review

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `backend/llm/generator_openai_full_corpus.py` | `:106-123` (agent, `output_type=AnswerOutput`), `:158-204` (`Runner.run`, timeout, tách JSON, usage) | harness gọi **đúng** agent / input production; đường không stream = mốc |
| `backend/api/routes/chat.py` | `:107-157` (tìm ⇒ dựng context ⇒ sinh), `:176-190` (kiểm citation toàn văn) | các mốc thời gian §3 khớp thứ tự production; định nghĩa "hợp lệ" |
| `.venv/lib/python3.13/site-packages/agents/run.py:375` + `agents/result.py:734, :798` + `agents/models/openai_responses.py:1927-1938` + `agents/usage.py:13-57` | `run_streamed`, `cancel`, `stream_events`, cách SDK gửi schema JSON, `cached_tokens` | đường stream chính dùng được với `max_turns=1`; timeout + hủy; mốc D10 gửi cùng schema; trường cache có thật |
| `data/tinh_nang_moi_2026-10-27/c63_can_cu.md` §1, §2 "Streaming", §4 "Streaming" (private) | luồng hiện tại, 4 kiểu A / B / C / D, rủi ro | plan đo đúng câu hỏi C63 nêu; kiểu B được ước |

Thêm, chỉ khi cần đối chiếu số:
- `report_agent/2026-10-26_cai_tien_tung_khau/b65_latency_dau_cuoi.md` §2 (latency qua API ngày 27/10);
- `c58_latency_theo_khau.md` (sinh ≈ 1,2 s + 11,5 ms / token ra);
- `phase_8_2_b1_merge_implementation.md` (B1 vào `main`).

Bộ câu: `data/streaming_ttft_2026-10-28/questions.jsonl` (private, sha `107620cb30f1`).

## 1. Đo để trả lời câu gì

**Lớp bài toán:** hôm nay người dùng chờ **toàn bộ** câu trả lời mới thấy chữ (p50 3,3 s / p95 5,7 s qua API ở context 5, B65 [N]). Streaming chỉ rút được phần **sau**
chữ đầu tiên. Phần trước nó vẫn phải chờ: tìm, dựng context, model suy luận, và ~1,2 s cố định [S, C63 §1].

Các câu hỏi đo:
1. **Q1:** streaming rút được bao nhiêu giây chờ tới **chữ đầu tiên hiện ra** (kiểu C / D trong C63 — hiện chữ chưa kiểm)?
2. **Q2:** rút được bao nhiêu nếu chỉ hiện **câu đầu tiên đã có `[n]`** (ước kiểu B — gom từng câu tới khi citation đóng)?
3. **Q3:** đường stream có làm **tổng thời gian** dài hơn, hoặc làm tỉ lệ câu trả lời hợp lệ khác đi không (theo dõi, không quyết)?
4. **Q4:** phần chờ trước chữ đầu tiên gồm những gì: thời gian tới sự kiện đầu, thời gian suy luận, token suy luận.

Đây là **đo hiện trạng** để bàn spec streaming, không phải biến thể đưa vào chatbot ⇒ không có luật giữ / gỡ. Ngưỡng diễn giải ghi trước ở §7.

## 2. Hiện trạng liên quan

- [N] **Chatbot từ 28/10 chạy context 10 + NFC**: B1 merge `510e1a8` (spec 8.2 §11 — B0 không chặn; `backend/config/settings.yaml:55` `max_context_documents: 10`).
  B0 sau này có thể đưa về 5 (luật dừng §11). Khi đó số đo ở đây vẫn dùng được cho câu hỏi chính, vì phần chữ hiện ra phụ thuộc độ dài câu trả lời hơn là số đoạn [S].
- [N] Sinh câu trả lời (`generator_openai_full_corpus.py`):
  - gọi `Runner.run(agent, input, max_turns=1, run_config=RunConfig(tracing_disabled=True, …))` trong `asyncio.wait_for(…, 45 s)` (`:162-175`);
  - client `AsyncOpenAI(max_retries=0)` (`:144-148`);
  - `store=False`; không gửi `reasoning` ⇒ dùng mức mặc định của model (`:116-121`);
  - usage lấy từ `raw_responses[-1]` (`:196-204`).
- [N] Đầu ra có cấu trúc `AnswerOutput{answer}` (`:30-32, :122`). SDK gửi `text.format = {type: json_schema, name: "final_output", strict}`
  (`agents/models/openai_responses.py:1935-1938`) ⇒ luồng chữ là **mảnh JSON** `{"answer":"…` [S, C63 §2].
- [N] SDK 0.19.4 có `Runner.run_streamed` (`agents/run.py:375`):
  - trả **ngay** một `RunResultStreaming`; model chạy trong lúc tiêu thụ `stream_events()` (`agents/result.py:798`);
  - hủy bằng `cancel()` (`:734`);
  - sự kiện `raw_response_event` bọc sự kiện Responses API (`agents/stream_events.py:11-19`);
  - usage có `input_tokens_details.cached_tokens` (`agents/usage.py:13-29`);
  - code dự án chưa dùng đường này.
- [N] Retrieval trả cả pool; context builder cắt theo `max_documents` (`retrieval/full_corpus_context.py:88`). NFC nằm trong `search` (`retrieval/full_corpus.py:420`)
  ⇒ harness gọi `retrieval_service.search` là đi qua NFC như production.

## 3. Mốc thời gian (một lần gọi)

Mọi mốc là `time.perf_counter()` phía harness, tính bằng ms từ **t0 = ngay trước khi gọi model** (sau khi đã có context):

| Mốc | Định nghĩa | Ô đo |
|---|---|---|
| `t_first_event` | sự kiện raw đầu tiên (thường `response.created`) | S, D |
| `t_reasoning_done` | `response.output_item.done` có `item.type == "reasoning"` (không có thì `null`) | S, D |
| `t_first_delta` | `response.output_text.delta` đầu tiên (mảnh JSON) | S, D |
| `t_first_visible` | lần đầu chuỗi delta cộng dồn khớp `^\s*\{\s*"answer"\s*:\s*"` **và** có ≥ 1 ký tự sau đó — chữ đầu tiên người dùng thấy được | S, D |
| `t_first_cited_sentence` | tính lại sau, từ delta đã lưu: lần đầu phần `answer` có một citation đóng (`[n]` / `[Nguồn n]`), rồi tới dấu kết câu (`.` `!` `?` theo sau là khoảng trắng / `\n` thoát, hoặc hết chuỗi). Đây là **ước** kiểu B: không xử lý `TP.`, `1.000` (C63 §4) ⇒ có thể sớm / muộn vài token | S |
| `t_last_event` | sự kiện raw cuối (`response.completed`) | S, D |
| `t_done` | vòng `stream_events()` kết thúc / `Runner.run` trả về | S, D, N |

Thêm cho mỗi câu: `search_ms`, `context_ms`, đo như `chat.py:108-126` (gọi `retrieval_service.search` và `context_builder.build` của production).
- Thời gian chờ đầu–cuối **ước** = `search_ms + context_ms + <mốc>`.
- Phần HTTP / JSON / UI không đo [S: nhỏ so với đơn vị giây; B65 đo qua API dùng làm đối chiếu].

## 4. Các ô đo (một lượt, context 10)

| Ô | Đường gọi | Lần gọi | Vai trò |
|---|---|---|---|
| **S10** | `Runner.run_streamed(generator.answer_agent, build_answer_input(q, packed.text), max_turns=1, run_config=` như `:162-165` `)`, tiêu thụ `stream_events()` (§6 timeout) | 10 | stream, đường chính — **ô quyết** |
| **N10** | `generator.generate_answer(q, packed.text)` — đúng hàm production (`Runner.run`) | 10 | mốc không stream, cho dòng theo dõi "phần thêm" |
| **D10** (tùy A) | `generator.client.responses.create(model, instructions=ANSWER_SYSTEM_INSTRUCTIONS, input=…, max_output_tokens=2048, store=False, stream=True, text={"format": cùng schema SDK})` | 10 | tham khảo: lớp SDK Agents thêm trễ bao nhiêu, so bằng `t_first_event` và `t_done − t_last_event` |

- **Thứ tự mỗi câu:** tìm 1 lần ⇒ dựng context ⇒ **S10 trước**, rồi D10, rồi N10 (thứ tự câu xáo bằng seed `20261028`; tuần tự, không gọi đồng thời).
  - Vì sao S trước: cache prompt chỉ có khi cùng phần đầu ≥ 1.024 token [S, theo review B]. Context 10 ≈ 1,6–2 nghìn token vào. Hai lần gọi sau cùng prompt có thể dính
    cache. Người dùng thật hỏi câu mới ⇒ không có cache ⇒ S (ô quyết, và số "chữ đầu tiên đầu–cuối") luôn là lần gọi **đầu** với prompt đó.
  - Hệ quả: D10 / N10 có thể được cache phần đầu vào ⇒ chúng có lợi thế ⇒ "phần thêm" `S_done − N_total` bị ước **lớn** hơn thật (thiên về bất lợi cho streaming,
    chấp nhận được).
  - Mọi dòng ghi `cached_tokens`; số trước chữ đầu tiên báo **tách** dòng có cache / không cache.
- **Bỏ ô context 5** (bản 1 có N5 / S5): context 10 nay là production (m-1); phần lợi trong cùng lần gọi gần như không phụ thuộc số đoạn [S] ⇒ ghi `NOT RUN` kèm lý do.
- **Bỏ lượt 2:** chỉ số quyết đo trong cùng lần gọi nên không cần A/A giữa hai lần gọi. Lượt 2 lặp đúng prompt sẽ dính cache (M-1).
- **D10:** chỉ để biết lớp SDK Agents có thêm trễ đáng kể không. Nếu có ⇒ ghi vào spec. `t_first_event` xảy ra trước khi model suy luận ⇒ ít nhiễu hơn so bằng chữ đầu
  tiên [S]. A bỏ ⇒ ghi `NOT RUN`.
- **Không đo** (ghi `NOT RUN` trong report), kèm lý do:
  - đầu ra văn bản thường thay JSON: đổi hợp đồng generator, có thể đổi chất lượng — C63 §2; tiền tố `{"answer":"` chỉ ~4 token ≈ 50 ms theo C58 [S];
  - kiểu B thật (tách câu + kiểm từng câu);
  - gọi đồng thời;
  - đo qua API / UI (API chưa có route stream);
  - context 5.

## 5. Bộ câu

- `data/streaming_ttft_2026-10-28/questions.jsonl` (private, sha `107620cb30f1`): **10 câu C tự viết** 28/10, không lấy từ Golden / câu kín / bộ B65.
  - Có dấu, kiểu du khách hỏi; mọi câu qua `unicodedata.is_normalized("NFC")` (đã kiểm lúc ghi).
  - `.githooks/overlap_scan.py` với Golden + kho: **0 trùng**.
- Loại câu, để có cả câu trả lời ngắn lẫn dài (streaming lợi nhiều khi câu dài [S]):
  - 8 câu trong kho: 2 hỏi một thông tin ngắn (giá, giờ), 1 kể lịch sử, 1 so sánh, 1 liệt kê, 1 gợi ý quán, 1 giải thích + năm, 1 lễ hội (thời gian + hoạt động);
  - **2 câu ngoài kho**.
  - Chủ đề trong kho đã kiểm bằng `scripts/grep_kb.sh -i -l` (chỉ đếm file, không đọc nội dung).
- B65 thấy 2–5 / 20 câu trong kho bị model **từ chối**, và không tất định [N]. Câu trả lời từ chối (đúng `INSUFFICIENT_ANSWER`, `full_corpus_prompt.py:3-5`) tách riêng
  khỏi số chính; báo số câu từ chối mỗi ô.
- **Mở rộng ghi trước:** nếu CI 95 % của chỉ số quyết **chứa một ngưỡng** (500 hoặc 1.500 ms), hoặc còn < 6 câu trong kho có trả lời, chạy thêm **một lượt S10 + N10 trên
  bộ 22 câu B65** (`data/phase_8_2/latency_2710/questions.jsonl`, `bac5c91db005`; ≈ 44 lần gọi ≈ 0,009 USD, A duyệt trước khi chạy). Gộp với 10 câu (câu khác nhau,
  không lặp prompt). Ngoài trường hợp này không chạy thêm.

## 6. Harness và cách chạy

- **Script:** `backend/experiments/streaming/ttft.py` (mới; skill `practical-project-coding`).
  - Viết **sau** khi plan được duyệt; commit nhánh `c70-ttft`; B kiểm code trước lượt thật.
  - Chạy từ `backend/`: `HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.streaming.ttft run --name <tên>`.
- **Dựng giống `api/app.py:55-108`:**
  - `build_full_corpus_retrieval_service(...)`;
  - `FullCorpusContextBuilder(...)` với `max_documents` lấy từ `settings.yaml` (= 10);
  - `OpenAIFullCorpusGenerator.from_environment(settings)`: một client cho mọi ô, như production.
  - Qdrant chỉ đọc; không đổi `settings.yaml`.
- **Timeout (m-3):** `asyncio.wait_for(consume(result), 45 s)`, trong đó `consume` chạy hết `async for ev in result.stream_events()` rồi trả về. Hết giờ hoặc có lỗi ⇒
  `result.cancel()` (mode mặc định `immediate`) trong `finally` khi luồng chưa xong ⇒ không còn task nền gọi model. D10 làm tương tự: đóng luồng trong `finally`.
- **Thứ tự chạy:** 1 lần gọi khởi động (N10, một câu hỏi tự viết khác bộ — ghi trong script) không tính; sau đó làm như §4.
- **Ghi kết quả:**
  - Mỗi lần gọi một dòng, ghi ngay (append) vào `data/streaming_ttft_2026-10-28/<tên>.jsonl`. Trường: `id, cell, search_ms, context_ms, n_context_sources`, các mốc §3,
    `input_tokens, cached_tokens, output_tokens, reasoning_tokens` (S: usage của `raw_responses[-1]` sau khi stream xong; D: `response.completed`), `refusal`, `valid`,
    `error` (mã lỗi, không thông điệp).
  - `valid` = tách JSON được bằng `parse_structured_output` **và** `select_cited_sources(normalize_citations(text), packed.sources)` không lỗi, hoặc là câu từ chối chuẩn
    — đúng điều kiện trả 200 của `chat.py:176-190`.
  - Delta + mốc ms từng sự kiện ghi file riêng `<tên>.events.jsonl` (private, vì có chữ câu trả lời) để tính lại `t_first_cited_sentence`.
  - Meta `<tên>.meta.json` (commit, sha bộ câu, giờ, model, SDK version), ghi cả khi lỗi.
  - Từ chối ghi đè file đã có (`raise SystemExit('exists')`). Mỗi lần gọi bắt mọi lỗi thành dòng lỗi kèm usage nếu có (`run-experiment` §3.8); không retry / fallback.
- **Pilot trước** (không gộp số): q03 (câu dài) + q09 (ngoài kho) × S10 + D10 = 4 lần gọi. Kiểm:
  - có đủ loại sự kiện ở §3, đặc biệt `output_text.delta` khi có `output_type`, và mục `reasoning`;
  - usage không `null`, có `cached_tokens`;
  - tính được `t_first_visible`.
  Thiếu sự kiện ⇒ dừng, báo A, sửa định nghĩa mốc **trước** lượt thật.
- **Tóm tắt** bằng lệnh `summarize` (cùng file) in bảng; không gõ tay số.

## 7. Tiêu chí ghi trước

```yaml
experiment_id: c70_streaming_ttft
baseline: main (commit lúc chạy; ≥ 510e1a8, context 10 + NFC), Runner.run không stream (N10)
changed_variable: cách nhận đầu ra (Runner.run → Runner.run_streamed); D10 = gọi SDK OpenAI trực tiếp (tham khảo)
unchanged: [corpus, index, retrieval, context builder (10), prompt, model gpt-6-luna, reasoning mặc định, AnswerOutput, timeout 45 s]
data: {file: data/streaming_ttft_2026-10-28/questions.jsonl, sha: 107620cb30f1, n: 10 (8 trong kho + 2 ngoài kho), rounds: 1}
metrics:
  - {name: gain_visible_ms, fn: "S_done − S_first_visible (cùng một lần gọi S10)", on: "câu trong kho, S10 không từ chối, valid", better: up, role: decide}
  - {name: gain_cited_ms, fn: "S_done − S_first_cited_sentence (cùng lần gọi)", on: như trên, better: up, role: decide (phụ, kiểu B)}
  - {name: stream_overhead_ms, fn: "S_done − N_total theo câu (hai lần gọi; N có thể được cache ⇒ ước lớn hơn thật)", role: watch, report_if: "trung vị > +300 ms"}
  - {name: e2e_first_visible_ms, fn: "search_ms + context_ms + S_first_visible", role: watch, note: "p50 / p95; chỉ dòng cached_tokens == 0"}
  - {name: pre_text_ms, fn: "t_first_event, t_reasoning_done, t_first_delta, reasoning_tokens", role: watch (Q4), note: "tách dòng có / không cache"}
  - {name: sdk_overhead_ms, fn: "S10 − D10 ở t_first_event và ở (t_done − t_last_event)", role: watch (D10)}
  - {name: valid_rate, fn: "số dòng valid / số dòng mỗi ô", role: watch, note: "model không tất định (B65) ⇒ khác 1–2 câu không kết luận được"}
  - {name: errors, fn: "số dòng error", role: watch, note: "≠ 0 ⇒ ghi nguyên, không chạy lại để che"}
  - {name: usd_per_call, fn: "token thật × giá", role: watch}
summary: "trung vị theo câu + bootstrap CI 95 % trên câu (10.000 lần, seed 20261028); p50 / p95 trên các dòng"
prediction:   # [S], ghi trước để bắt mốc đo sai khi kết quả lệch xa
  gain_visible: "≈ 1,0–1,5 s = (token ra − token suy luận) × 11,5 ms (C58); log chat_metrics 89–134 token chữ (review B), C63 §1: 113 token ≈ 1,3 s"
  e2e_first_visible: "≈ 2–3,5 s = tìm + context ~0,1 s + ~1,2 s cố định + suy luận 57–196 token × 11,5 ms (0,7–2,3 s)"
  stream_overhead: "≈ 0 (cùng model, cùng request; chỉ khác cách nhận)"
  check: "gain_visible < 0,3 s hoặc > 3 s ⇒ kiểm lại cách tính t_first_visible / tiền tố JSON trước khi diễn giải"
interpretation:   # ghi trước, dùng trung vị gain_visible (ô S10)
  clear: ">= 1500 ms và CI > 0 ⇒ 'streaming rút chờ rõ' — đưa vào brainstorm spec"
  moderate: "500–1500 ms ⇒ 'lợi vừa' — cân với rủi ro hiện chữ chưa kiểm và độ phức tạp của kiểu B"
  small: "< 500 ms hoặc CI chứa 0 ⇒ 'lợi nhỏ / chưa rõ' — khuyên chưa làm streaming, xem tối ưu khác (suy luận, context)"
  overhead_rule: "lợi người dùng thấy = gain − stream_overhead; nếu trung vị stream_overhead > 300 ms ⇒ diễn giải theo (gain − overhead), ghi cả hai"
  cited_note: "gain_cited cùng thang; nếu visible 'rõ' mà cited 'nhỏ' ⇒ ghi: lợi chỉ có khi chấp nhận hiện chữ chưa kiểm (ngược sàn hiện hành) — User quyết"
result: null
conclusion: null
```

**Cỡ mẫu** [S]:
- Chỉ số quyết đo trong cùng một lần gọi ⇒ không mang nhiễu độ dài suy luận giữa hai lần gọi (SD ≈ 808 ms, spec 8.2 §10.2). Dao động còn lại chủ yếu là **chênh thật giữa
  các câu** (độ dài câu trả lời), và đó chính là điều cần đo.
- Ví dụ với 8 câu: nếu phần chữ hiện ra là 60–200 token ⇒ 0,7–2,3 s. Khi đó CI của trung vị rộng cỡ dải đó, đủ phân định dải "nhỏ" khỏi "vừa / rõ", nhưng có thể không
  phân định được "vừa" ↔ "rõ" khi trung vị gần 1,5 s ⇒ áp luật mở rộng §5 (bộ 22 câu B65).
- Câu ngoài kho: báo riêng `t_first_visible` và thời điểm biết là câu từ chối (chuỗi delta khớp trọn `INSUFFICIENT_ANSWER`) — ước rằng với câu từ chối, kiểu B không hiện
  sớm được [S].

## 8. Tiền, trần, điều kiện dừng

- **Giá** `gpt-6-luna`: 0,1 / 0,5 USD mỗi 1M token vào / ra. Ước theo `CURRENT_HANDOFF.md`: ≈ 0,000204 USD mỗi lần gọi context 10.
- **Số lần gọi:** S10 10 + N10 10 + D10 10 + pilot 4 + khởi động 1 = 35 ⇒ **≈ 0,0071 USD**; cận trên ×2 (suy luận dài gấp đôi) ≈ 0,014 USD.
  - Không có D10: 25 lần ≈ 0,0051 USD.
  - Nếu mở rộng (§5): thêm ≈ 0,009 USD (A duyệt trước khi chạy).
  - So với handoff (≈ 0,002 USD = 10 lần gọi): cao hơn vì có mốc N10, D10 và pilot.
- **Trần C70: 0,03 USD** (gồm cả mở rộng), trong trần 1 USD của phiên.
- **Dừng khi:**
  - tiền ước theo pilot (token thật) vượt trần;
  - 2 lỗi provider liên tiếp;
  - pilot thiếu sự kiện §6;
  - `t_first_visible` không tính được ở > 2 dòng không lỗi của lượt thật;
  - đường thật khác dự kiến (ví dụ `run_streamed` cần `max_turns` khác 1).
  Dừng ⇒ ghi report phần đã có, báo A.

## 9. Đầu ra

- **Report** `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_result.md` (tracked: chỉ số đếm, mã câu, loại câu; không chép câu hỏi / câu trả lời):
  - mở đầu 3–5 dòng lời thường cho User;
  - bảng do `summarize` in;
  - `NOT RUN` cho các mục §4 "Không đo";
  - usage + USD từ log; so kết quả với `prediction`.
- **Dữ liệu chạy:** `data/streaming_ttft_2026-10-28/` (private).
- **B kiểm:**
  - chạy lại `summarize` từ file đã lưu;
  - tính lại `t_first_cited_sentence` từ `events.jsonl`;
  - đối chiếu 1–2 dòng với `events.jsonl`;
  - xem diff nhánh `c70-ttft`: harness gọi đúng hàm production, timeout bọc vòng stream + `cancel()`.

## 10. Câu hỏi cho A khi duyệt

1. Giữ D10 (mốc SDK trực tiếp, +0,002 USD)? C khuyên giữ: nếu spec streaming chọn gọi SDK trực tiếp thay Agents thì đã có số.
2. Người viết harness: C (đề xuất); B review code + kết quả.
