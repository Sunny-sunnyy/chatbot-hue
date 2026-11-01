# Implementation Report: B108 — `cost_usd` theo giá đủ + token đệm trong usage

Người làm: B (Claude Opus 5.5)
Date: 11:29 01/11/2026 (`date`)
Căn cứ: giá `gpt-6-luna` User 30/10 (`Project_Status.md` §5: vào 0,10 · ra 0,50 · đọc đệm 0,01 · ghi đệm 30 phút 0,125 USD / 1M); B95 (30/10, ghi chú private
`data/external_project_notes/doc_rag_du_an_kia_2026-10-30.md` §7). Mục việc: tin A 01/11 (B108).
Nhánh: `dg-cost-usd` từ `830df0e` (nhánh streaming — `chat.py` / generator đã đổi ở đó), commit **`bbbdbf9`**, đã push `origin`. Worktree `/tmp/b_cost`.

## 1. Phạm vi

Sửa chỗ tính tiền + đọc usage ở generator + thêm token đệm vào `chat_metrics`. **Không** sửa số USD cũ trong báo cáo (A ghi chú "giá phẳng"). Không ghi USD vào log (giữ chính sách C59).

## 2. Thay đổi chính

`git grep 'cost_usd|PRICE_|usage_totals|cached_tokens|cache_write'` trước khi sửa ⇒ nơi gọi: `full_corpus_eval.py` (`usage_totals` ⇒ tóm tắt `generate`, `judge-luna`, `retry`),
`experiments/phase_8_1/g2_generate.py`, `experiments/phase_8_1/g4_rerank.py`, `experiments/phase_8_2/b1.py`, `tests/test_full_corpus_eval.py`.

| File | Đổi gì |
|---|---|
| `backend/evaluation/full_corpus_eval.py` | `cost_usd(input, output, cache_write_tokens=0, cached_tokens=0)`: phần vào chia ba (thường 0,10 · ghi đệm 0,125 · đọc đệm 0,01), ra 0,50; `input_tokens` đã gồm phần đệm (cách OpenAI đếm). Không truyền phần đệm ⇒ **giá phẳng như cũ** (dòng kết quả cũ không có trường đệm). `row_cost_usd(row)` (mới) cho một dòng; `usage_totals` cộng thêm 2 trường đệm. Dòng `answer_case` + dòng judge luna thêm `cache_write_tokens`, `cached_tokens` |
| `backend/llm/generator_openai_full_corpus.py` | `GeneratedText` thêm `cached_tokens`, `cache_write_tokens`; `input_cache_tokens(usage)` (mới) đọc `usage.input_tokens_details` — dùng chung cho generator (cả hai đường sinh qua `_generated_text`), judge, rerank luna |
| `backend/api/routes/chat.py` | `METRIC_FIELDS` thêm `cache_write_tokens`, `cached_tokens` (cả route JSON lẫn stream — stream kế thừa danh sách); `_copy_trace_metrics` chép 2 trường này |
| `experiments/phase_8_1/g2_generate.py`, `experiments/phase_8_2/b1.py`, `experiments/phase_8_1/g4_rerank.py` | tính `usd` bằng giá đủ (`row_cost_usd` / `cost_usd` + `input_cache_tokens`) — chỉ ảnh hưởng lần chạy **sau**; file kết quả cũ không đổi |
| `backend/tests/test_full_corpus_eval.py` | +2 test: giá từng loại token; số thật B95 (vào 1.916, ghi đệm 1.913, ra 85): phẳng 0,0002341 ⇒ đủ **0,000281925** (+20 %); `usage_totals` / `row_cost_usd` với dòng mới + dòng cũ thiếu trường + dòng lỗi |
| `backend/tests/test_input_cache_tokens.py` (mới) | `input_cache_tokens` trên đúng hai lớp usage của thư viện (`agents.usage.Usage`, `openai.types.responses.ResponseUsage`) + đối tượng không có trường |

## 3. Cách đã chạy thật

Từ `/tmp/b_cost/backend`, `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`, `--env-file /home/minhhieu/hue_rag/.env`. Dữ liệu: `data/streaming_s1_2026-11-01/b108/` (private).

1. `python -m pytest tests/test_full_corpus_eval.py tests/test_input_cache_tokens.py tests/test_api_chat.py tests/test_chat_stream.py tests/test_grounded_answer.py tests/test_openai_full_corpus_generator.py tests/test_phase6_live_smoke.py tests/test_citations.py -q` (không gọi model).
2. `python -m evaluation.full_corpus_eval generate --cases 1 --out …/b108/answer_case_dev1.jsonl` (1 câu dev, đường không stream qua `answer_case`).
3. `uvicorn api.app:app --port 8792` (log riêng của worktree): 1 câu tự viết qua `/api/chat/stream` + 1 câu tự viết qua `/api/chat`; đọc 2 dòng `chat_metrics` mới; grep câu hỏi trong log; tắt server.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Test | **PASS** 85 passed (5 test mới). 0 lần gọi model |
| `answer_case` câu dev (phần vào 963 token) | `cache_write_tokens` **0**, `cached_tokens` 0, ra 32; `generation_usage` có 2 trường mới; `cost_usd` 0,0001123 |
| Route stream (phần vào 1.848) | `cache_write_tokens` **1.845** (= vào − 3), `cached_tokens` 0, ra 280 |
| Route JSON (phần vào 1.377) | `cache_write_tokens` **1.374** (= vào − 3), `cached_tokens` 0, ra 152 |
| `chat_metrics` | 2 lần gọi ⇒ 2 dòng mới, có 2 trường đệm, không có USD; câu hỏi trong log 0 / 2; server đã tắt |

⇒ SDK **có** chuyển `cache_write_tokens` lên ở cả đường `Runner.run` lẫn `Runner.run_streamed` — đúng mẫu B95 (ghi đệm = vào − 3, đọc đệm 0). Câu dev ra 0 ghi đệm có lẽ vì phần vào
963 < 1.024 token — mức tối thiểu để OpenAI đệm prompt [Suy ra, theo tài liệu prompt caching của OpenAI; B chưa WebFetch kiểm lại hôm nay] — không phải do SDK làm rơi trường.

**Tiền 3 lần gọi:** giá đủ **0,0007313 USD** (giá phẳng cũ sẽ ghi 0,0006508) — trần 0,001.

## 5. Lỗi và giới hạn

- **Số 0 có thể là "không gửi":** Agents SDK điền `cache_write_tokens` / `cached_tokens` = 0 khi provider không gửi trường (`agents/usage.py` `_cache_write_tokens`, `_make_input_tokens_details`)
  ⇒ trong dòng kết quả / log, 0 không phân biệt được "không ghi đệm" với "provider không gửi". Hôm nay 2 / 3 lần có số khác 0 nên trường có tới.
- Giá ghi đệm dùng mức **đệm 30 phút** (0,125). Code không đặt thời gian giữ đệm (mặc định của API); nếu sau này bật đệm 12 giờ (0,25) thì phải đổi hằng.
- Số USD cũ (trước `bbbdbf9`) đều theo giá phẳng 0,10 — thiếu ≈ 20 % ở câu có phần vào ≥ 1.024 token; không sửa lại (A ghi chú).
- `cost_usd` không kiểm `cache_write_tokens + cached_tokens ≤ input_tokens` (dữ liệu từ provider; không thêm rào phòng xa).
- Nhánh `dg-cost-usd` nằm trên nhánh streaming chưa merge: merge sau S4 cùng nhánh streaming (hoặc rebase), A quyết.

## 6. Bàn giao cho người kiểm

- Đọc: `git diff 830df0e bbbdbf9` (8 file, +103 / −22); bảng §4.
- Chạy lại: `pytest tests/test_full_corpus_eval.py tests/test_input_cache_tokens.py -q` (0 USD); muốn đường thật: 1 câu qua `/api/chat` ⇒ `chat_metrics` có `cache_write_tokens` ≈ `input_tokens` − 3 (≈ 0,00025 USD).

**Giải thích ngắn:** trước đây phép tính tiền coi mọi token vào cùng giá 0,10 USD / 1 triệu, trong khi mỗi lần gọi model thật ra phần lớn token vào bị tính giá "ghi vào bộ đệm" 0,125 — nên số tiền
báo cáo thấp hơn thật khoảng 20 %. Nay code đọc đúng số token ghi đệm / đọc đệm mà API trả về và tính theo bảng giá đủ; log ghi thêm hai số token này để sau tính lại được. Chatbot trả lời
không đổi gì.
