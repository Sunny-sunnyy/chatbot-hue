# Review: C73 — harness đo "thời gian tới chữ đầu tiên" (nhánh `c70-ttft`)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor — không chặn pilot; C sửa thì B kiểm phần sửa)
Người kiểm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 10:21 28/10/2026 (`date`) · Việc: A giao 28/10 (review code C73). 0 USD.
Đối chiếu: plan `streaming_ttft_plan.md` bản 2 (A duyệt sha `9683641b6c38`); implementation `streaming_ttft_harness_implementation.md`.

## 1. Phạm vi đã review

- `git diff 249d270 origin/c70-ttft` (commit `9ff45d1`): 3 file mới — `backend/experiments/streaming/ttft.py` (395 dòng), `__init__.py` (rỗng),
  `backend/tests/test_streaming_ttft.py` (5 test). Không file production nào đổi.
- Đọc hết `ttft.py` + test; đối chiếu SDK `.venv` (`agents` 0.19.4): `result.py:550` `is_complete`, `:734` `cancel`; `models/openai_responses.py:758-900` (tham số
  SDK gửi `responses.create`); `openai/_models.py` `to_dict(exclude_unset=True)`; `backend/llm/generator_openai_full_corpus.py:49-75` (`parse_structured_output` nhận
  cả object / dict / chuỗi JSON).

## 2. Đạt (theo các điểm C nhờ kiểm, §4 report)

| Điểm | Kết quả |
|---|---|
| S10 đúng `generator.answer_agent` + `max_turns=1`, RunConfig như `_execute_agent` | ✓ `ttft.py:123-145` (2 cờ RunConfig giống `generator…:162-165`) |
| Timeout bọc cả vòng stream + `cancel()` (review B m-3) | ✓ `:131-142`: `wait_for(consume(), generator.timeout)`; `finally: if not result.is_complete: result.cancel()` (`is_complete` có thật, `result.py:550`) |
| D10 cùng tham số như SDK | ✓ đủ phần có ảnh hưởng: `instructions` = `ANSWER_SYSTEM_INSTRUCTIONS` (mặc định của `from_environment`), `input` dạng một tin user (SDK đổi chuỗi thành đúng dạng này), `max_output_tokens` 2048, `store=False`, `text.format` từ `AgentOutputSchema(AnswerOutput)` (như `openai_responses.py:1927-1938`), không `reasoning`. SDK còn gửi `include` rỗng và header User-Agent riêng — không đổi model / đầu ra; D10 chỉ là mốc tham khảo |
| `valid` = điều kiện 200 của `chat.py` | ✓ `:202-209`: tách JSON (`parse_structured_output`, lỗi ⇒ dòng `error`) + `select_cited_sources(normalize_citations(text), packed.sources)`; câu từ chối chuẩn qua validator ⇒ `valid` |
| `summarize` đúng plan §7 | ✓ `gain_visible` = S10, trong kho, không lỗi, `valid`, không từ chối, `t_done − t_first_visible` (cùng lần gọi); `band` khớp dải ghi trước (clear ≥ 1.500 & CI > 0; moderate ≥ 500 & CI > 0; còn lại small / unclear); `prediction_check` 300–3.000 ms; `overhead_over_300ms`; mốc tính lại từ `events.jsonl` (`load_run` khẳng định cùng thứ tự) |
| n-1 `cached_tokens` vắng ⇒ None | ✓ `record_event` đọc `response.completed` qua `to_dict()` (bỏ trường không gửi); N10 luôn None, có ghi lý do |
| Ghi từng dòng, từ chối ghi đè, không retry, meta cả khi lỗi, dừng sau 2 lỗi liên tiếp | ✓ `:222-285` |
| In ra màn hình | chỉ id / ô / số ms / cached — không chữ câu trả lời; chữ chỉ ở `*.events.jsonl` private ✓ |

**Chạy lại:** worktree `/tmp/b_c73` (`origin/c70-ttft`), `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_streaming_ttft.py -q`
⇒ **5 passed**. Không chạy lệnh `run` (có phí) — chờ A, sau bộ "trước" B78.

## 3. Findings

### m-1 — luật mở rộng ghi trước (plan §5) chưa do script in ra

- Plan §5: CI 95 % của chỉ số quyết **chứa 500 hoặc 1.500 ms**, hoặc **< 6 câu trong kho có trả lời** ⇒ đề xuất lượt mở rộng (A duyệt). `summarize` in `gain_visible_ms`
  (n, median, CI) nhưng không in cờ này ⇒ người đọc tự so tay.
- **Đóng:** thêm một trường, ví dụ `"extension_rule": {"ci_contains_threshold": …, "n_in_kb_answered": …, "triggered": …}` trong `decide`.

### m-2 — pilot nên kiểm luồng chữ là UTF-8 thô (không `\uXXXX`)

- `timeline` so chuỗi delta cộng dồn với `INSUFFICIENT_ANSWER` (`:81`) và tìm `[Nguồn n]` bằng `CITATION_PATTERN` (`:87`) **trên chuỗi JSON thô**. Nếu provider thoát ký tự
  có dấu thành `\uXXXX` thì `t_refusal_complete` luôn None và dạng `[Nguồn n]` không khớp (dạng `[n]` vẫn khớp; `t_first_visible` không ảnh hưởng). Thường đầu ra có
  cấu trúc là UTF-8 thô [S, chưa kiểm].
- **Đóng:** pilot kiểm thêm "delta không chứa `\u`" (hoặc `json.loads` của chuỗi delta cộng dồn = chuỗi đó sau tiền tố) và ghi vào meta; có `\u` ⇒ dừng như "thiếu sự kiện".

## 4. Giới hạn

- Không chạy đường thật (provider): loại sự kiện, mục `reasoning`, `cached_tokens`, D10 nhận `text.format` — pilot kiểm (plan §6).
- Không kiểm bộ câu `questions.jsonl` (ngoài phạm vi review code).

## 5. Decision

`ready_for_user_confirmation`: code đi đúng đường production, timeout / hủy đúng, chỉ số đúng định nghĩa ghi trước. 2 minor nên gộp trước pilot (không bắt buộc).

## Vòng 2 — kiểm phần sửa (commit `1f70095`, `ttft.py` sha `7e992e229fc5`)

Decision vòng 2: **ready_for_user_confirmation** (0 / 0 / 0). Date: 10:26 28/10/2026 (`date`). Đọc `git diff 9ff45d1 1f70095` (2 file, +49 / −8).

| Finding | Sửa | Kết quả |
|---|---|---|
| m-1 cờ luật mở rộng | `decide` thêm `n_in_kb_answered` (= số dòng S10 vào `gain_visible`) và `extension_rule_triggered` = CI chứa 500 hoặc 1.500 ms, hoặc < 6 câu, hoặc không có số — đúng plan §5 | **đóng** |
| m-2 chuỗi JSON thô / `\\uXXXX` | sửa tận gốc: `decode_partial_string` tìm dấu `"` đóng chưa thoát, bỏ phần thoát còn dở ở cuối mảnh (số lẻ `\\` kèm tùy chọn `u` + < 4 hex), rồi `json.loads`; chữ đầu, `[Nguồn n]`, câu từ chối, kết câu đều so trên chữ đã giải mã; "hết chuỗi" = chuỗi đã đóng | **đóng** |

Chạy lại (worktree tạm `/tmp/b_c73` ở `1f70095`, đã gỡ): `pytest tests/test_streaming_ttft.py` ⇒ **7 passed**; thử biên `decode_partial_string` (inline, chỉ chuỗi tự viết): `\\\\` chẵn
giữ nguyên, `\\u12` còn dở bị bỏ, `\\"` giải mã thành `"`, gặp `"` đóng ⇒ `closed=True` — đúng. Mốc kết câu mới (`[.!?]` + khoảng trắng, hoặc xuống dòng, hoặc chuỗi đã đóng)
chậm hơn tối đa một mảnh khi dấu chấm nằm cuối mảnh — chấp nhận (thiên về muộn, không sớm). Code sẵn cho pilot khi A cho chạy (sau bộ "trước" B78).
