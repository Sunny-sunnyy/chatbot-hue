# Review: B108 — `cost_usd` theo giá đủ (ghi đệm / đọc đệm)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 1 minor không chặn)
Người kiểm: A (Claude Opus 5.5)
Date: trước 11:33 01/11/2026 (giờ commit `ce37bb1`; sửa lúc 11:34 01/11/2026 — bản đầu gõ tay "11:56" không chạy `date`)
Căn cứ: giá `gpt-6-luna` User 30/10 (`Project_Status.md` §5 dòng 2026-10-30 15:07); B95 (ghi đệm ≈ toàn bộ phần vào, đọc đệm 0)
Implementation report: `report_agent/2026-10-31_streaming_spec/b108_cost_usd_implementation.md` (`42ab49f710f4`)

## 1. Phạm vi đã review

Nhánh `origin/dg-cost-usd` một commit `bbbdbf9` trên `830df0e` (nhánh streaming); 8 file: `full_corpus_eval.py` (`cost_usd`, `row_cost_usd`, `usage_totals`, dòng `answer_case` / judge),
`generator_openai_full_corpus.py` (`input_cache_tokens`, 2 trường mới của `GeneratedText`), `chat.py` (`METRIC_FIELDS` + chép 2 trường), 3 harness cũ, 2 file test. `git diff --check` sạch.
Không ghi USD vào log (giữ chính sách); số USD cũ trong báo cáo không sửa (đúng mục việc).

## 2. Findings

- **m-1 (minor):** ngưỡng "dưới 1.024 token thì không ghi đệm" trong report là suy ra, chưa kiểm nguồn — tiêu chí đóng: khi đóng gói ghi vào bảng giới hạn là [suy ra] hoặc kiểm bằng
  `scripts/tra_web_codex.sh`; không ảnh hưởng công thức (công thức đọc số token đệm thật provider trả).

Độ đơn giản: một hàm đọc chi tiết token dùng chung (`input_cache_tokens`) + tham số mặc định 0 giữ tương thích dòng cũ — tương xứng.

## 3. Cách người kiểm chạy lại thật

- Ca dò khác cách (`/tmp/a_b108_probe/probe.py`, ngoài repo, chạy trong `/tmp/b_cost/backend`): 100.000 cặp token ngẫu nhiên — **câu bất biến** "không có phần đệm ⇒ đúng giá phẳng cũ";
  tính tay một lần gọi (1.848 vào / 1.845 ghi đệm / 120 ra) so với hàm; dòng cũ thiếu trường; `usage_totals` có dòng lỗi (`input_tokens` None); usage không có `input_tokens_details`.
- `pytest tests/test_full_corpus_eval.py tests/test_input_cache_tokens.py tests/test_api_chat.py tests/test_chat_stream.py -q` (không key).

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Bất biến giá phẳng | **PASS** — lệch 0 / 100.000 |
| Tính tay ↔ hàm | **PASS** — 0,000290925 USD cả hai |
| Dòng cũ thiếu trường đệm | **PASS** — bằng giá phẳng |
| `usage_totals` | **PASS** — `calls` 1 (dòng lỗi không tính), tổng token + tiền đúng |
| Usage không có chi tiết | **PASS** — `(None, None)` |
| Test (không key) | **47 passed, 1 error** — error là test đã biết cần `OPENAI_API_KEY` |

Dùng lại bằng chứng của B (không chạy lại, lý do: cùng commit, đường thật đã chạy, tránh tốn thêm): 2 lần gọi thật (route stream + route JSON) có `cache_write_tokens` = vào − 3, `cached_tokens` 0;
`chat_metrics` có 2 trường mới, không USD, câu hỏi trong log 0; 0,0007313 USD.

## 5. Giới hạn hoặc phần chưa chạy

A không gọi API thật (0 USD). Nhánh nằm trên nhánh streaming chưa merge ⇒ vào `main` cùng lượt merge streaming (review cả nhánh a1 phải gồm commit này).

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`. Việc trung bình ⇒ A đóng bước, báo User. Merge: gộp vào nhánh streaming trước khi review cả nhánh (A quyết khi S3 / S4 xong).
