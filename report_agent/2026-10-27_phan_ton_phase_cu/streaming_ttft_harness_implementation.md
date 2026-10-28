# Implementation Report: C73 — harness đo "thời gian tới chữ đầu tiên" (chưa chạy)

Người làm: C (Claude Opus 5.5, `hue-rag-32`) · Date: 10:07 28/10/2026 (`date`) · Trạng thái: B review `9ff45d1` ready 0/0/2 ⇒ **sửa m-1, m-2 ở `1f70095` (10:24 28/10/2026) — chờ B kiểm phần sửa**.
Việc: C73 (`CURRENT_HANDOFF.md` dưới mục C70, A giao 28/10). Plan: `streaming_ttft_plan.md` bản 2, **A duyệt sha `9683641b6c38`**; §10: giữ D10.
Nhánh **`c70-ttft`** commit `9ff45d1` (đã push; gốc `main` `249d270`); worktree `/tmp/c_ttft`. **0 USD** — chưa chạy pilot hay lượt thật: A báo khi được chạy
(sau B80 / B3 và bộ "trước" B78 — không chạy chồng lượt trả phí khác).

## 1. Thay đổi

| File | Vai trò |
|---|---|
| `backend/experiments/streaming/ttft.py` (mới, 395 dòng, sha `96c97827df91`) | lệnh `run` (có phí) và `summarize` (free) |
| `backend/experiments/streaming/__init__.py` (mới, rỗng) | gói |
| `backend/tests/test_streaming_ttft.py` (mới, 5 test) | logic thuần `timeline` |

Không sửa code production, `settings.yaml`, kho hay Qdrant.

## 2. Đối chiếu plan

| Plan | Code |
|---|---|
| §4 ba ô, context 10, thứ tự S10 → D10 → N10 mỗi câu; thứ tự câu xáo seed `20261028`; tuần tự | `run`: `random.Random(SEED).shuffle`, `CELLS`; tìm 1 lần / câu, dựng context bằng `build_context_builder(settings)` (= 10 từ `settings.yaml`) |
| S10 = `Runner.run_streamed(generator.answer_agent, …, max_turns=1)`, RunConfig như production | `call_s10`; RunConfig chép đúng 2 cờ của `_execute_agent` (`generator_openai_full_corpus.py:162-165`) — không gọi được trực tiếp vì dựng bên trong hàm |
| m-3: `wait_for` bọc cả vòng `stream_events()`, `cancel()` khi chưa xong | `call_s10`: `wait_for(consume(), generator.timeout)` + `finally: if not result.is_complete: result.cancel()` |
| D10 cùng instructions / schema | `call_d10`: `responses.create(stream=True)`, `input=[{"role": "user", …}]`, `text.format` từ `AgentOutputSchema(AnswerOutput)` (như `openai_responses.py:1935-1938`), `max_output_tokens`, `store=False`; `finally: stream.close()` |
| N10 = hàm production | `call_n10` = `generator.generate_answer` |
| §3 mốc tính lại từ sự kiện đã lưu | `timeline(events)` (logic thuần); `summarize` chỉ đọc mốc từ `events.jsonl` |
| n-1: `cached_tokens` vắng ⇒ "không đo được", không phải 0 | `record_event`: usage lấy từ sự kiện raw `response.completed` qua `to_dict()` (bỏ trường không gửi) ⇒ vắng = `None`; N10 luôn `None` (`generate_answer` chỉ có usage qua SDK, mặc định 0); meta `cached_tokens_reported` |
| `valid` = điều kiện 200 của `chat.py:176-190` | `measure`: `parse_structured_output` (lỗi ⇒ dòng `error`) + `select_cited_sources(normalize_citations(text), packed.sources)` |
| §6 ghi từng dòng, từ chối ghi đè, không retry, meta cả khi lỗi | `append_jsonl` + flush; `raise SystemExit('exists')` cho 3 file; `finally` ghi meta (token, USD, lỗi); `error` chỉ tên lớp lỗi; dừng sau 2 lỗi liên tiếp (§8) |
| pilot q03 + q09 × S10 + D10, không gộp số; 1 lần khởi động N10 không tính | `--pilot` (4 lần gọi, không khởi động); `run` thường có 1 dòng `warmup` (câu tự viết, khác bộ), `summarize` bỏ |
| §7 chỉ số, dải diễn giải, prediction check, overhead_rule | `summarize`: `gain_visible_ms` / `gain_cited_ms` (trung vị + bootstrap CI 10.000, p95) + `band`; `prediction_check` (300–3.000 ms); `overhead_over_300ms`; e2e "all" + "uncached"; trước chữ đầu tách cached 0 / > 0 / không biết; `sdk_overhead_ms` (`t_first_event`, đuôi luồng); câu ngoài kho; bảng mỗi ô |

Lệch nhỏ, đã khai báo:
- Plan §5 có luật mở rộng (bộ 22 câu B65). Bộ đó có trường `question` / `domain`, không có `query` / `scope`, nên harness **chưa** nhận bộ đó. Nếu A duyệt mở rộng thì thêm
  phần đọc riêng (bộ câu khác ⇒ sửa code ⇒ B kiểm).
- Lỗi khi tìm / dựng context (ví dụ `ContextBudgetError`) dừng cả lượt và vẫn ghi meta; plan không có trường hợp này vì bộ 10 câu đã qua builder ở runtime thật.

## 3. Đã chạy

Trong worktree, `uv run --project /home/minhhieu/hue_rag`, không key:

```bash
cd /tmp/c_ttft/backend
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_streaming_ttft.py -q   # 5 passed
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.streaming.ttft --help          # CLI nạp được, import đủ
git diff --check                                                                                                # sạch; hook quét trùng 0 / 0 lúc commit
```

Thử ngược (script inline, không lưu):
- đổi `SENTENCE_END` thành `[.!?]` ⇒ test `…skips_thousands_separator` **đỏ**;
- đổi `ANSWER_PREFIX` thành rỗng ⇒ test `…waits_for_json_prefix…` **đỏ**.

Cả hai test chỉ đúng khi định nghĩa mốc ở plan §3 được giữ.

## 4. Chưa kiểm (NOT RUN) và việc người review nên làm

- **Đường thật (provider) NOT RUN.** Loại sự kiện thật, `reasoning` item, `cached_tokens` có trong `response.completed` hay không, D10 có nhận `text.format` không: pilot kiểm
  (plan §6), khi A cho chạy. Test chỉ là logic thuần, không phải bằng chứng provider.
- B nên kiểm:
  - `call_s10` đi đúng `generator.answer_agent` + `max_turns=1`;
  - timeout bọc cả vòng + `cancel()`;
  - D10 gửi cùng tham số như SDK — `tools` / `include` rỗng không gửi, xem `openai_responses.py:758-900`;
  - `valid` khớp `chat.py`;
  - `summarize` đúng định nghĩa plan §7 (dòng nào vào `gain_visible`: S10, trong kho, không lỗi, `valid`, không từ chối).
- Tiền: 0 USD.

## 5. Sửa theo review B (`streaming_ttft_harness_review.md`, ready 0 / 0 / 2) — commit `1f70095`, 10:24 28/10/2026

- **m-2** (so `INSUFFICIENT_ANSWER` / `[Nguồn n]` trên chuỗi JSON thô hỏng khi provider thoát `\uXXXX`): sửa tận gốc thay vì chỉ kiểm ở pilot. `timeline` gọi
  `decode_partial_string` để giải mã thân chuỗi JSON đang stream (dừng ở `"` đóng chưa thoát; bỏ chuỗi thoát còn dở ở cuối mảnh — số lẻ `\`, có thể kèm `u` + < 4 hex)
  rồi mới xét chữ đầu, câu có citation, câu từ chối. `SENTENCE_END` nay chạy trên chữ đã giải mã (`[.!?]` + khoảng trắng, hoặc `\n`); "hết chuỗi" = chuỗi đã đóng.
- **m-1:** `summarize` thêm `decide.n_in_kb_answered` và `decide.extension_rule_triggered` (CI chứa 500 hoặc 1.500 ms, hoặc < 6 câu trong kho có trả lời — plan §5).
- **Test:** 7 passed (thêm 2: câu từ chối thoát `\u`, cắt giữa chuỗi thoát; `\n` thoát kết câu có `[Nguồn n]` thoát).
- **Thử ngược:** thay `decode_partial_string` bằng tách chuỗi thô ⇒ 2 test mới **đỏ**; mutant cũ (`SENTENCE_END = [.!?]`) vẫn **đỏ**.
- `ttft.py` sha nay `7e992e229fc5`. 0 USD.
