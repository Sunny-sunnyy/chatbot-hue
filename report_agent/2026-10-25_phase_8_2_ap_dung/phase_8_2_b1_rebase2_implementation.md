# Implementation Report: Phase 8.2 B1 — rebase lần 2 lên `main` `576f84e` (B71)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-2d`)
Date: 2026-10-27 13:58 +0700 (`date`)
Việc: `session_prompt/CURRENT_HANDOFF.md` mục "B71 — rebase B1 lên `main` trước B0" (A giao 13:50 27/10). Spec 8.2 §4, §5 B1; report gốc
`phase_8_2_b1_implementation.md` (§4 lần đo đầu, §7 rebase B41); review `phase_8_2_b1_rebase_review.md`.
Trạng thái: **chờ review** (người kiểm: C). Không merge `main` (spec 8.2 §5 B1.3: merge sau B0).

## 1. Phạm vi

Rebase `p82-b1` (`811d25d`, gốc `43cdcd6`) lên `main` `576f84e`. Phần mới của `main` gồm log `chat_metrics` (`5100b90`), gold v2 (`a819789`), R4
(`2c7ecfd`) và tài liệu. Mục việc ghi `473f61e`; A nhắn `576f84e` (mới hơn, chỉ thêm tài liệu) ⇒ rebase lên `576f84e`. Làm trong worktree `/tmp/b71_b1`.
Không đổi hành vi ngoài B1, không chạy thí nghiệm, không mở `khoa.json` / câu kín.

## 2. Thay đổi chính

- **Không có xung đột.** Hai commit `e1e16b3`, `811d25d` ⇒ `2fa6f16`, `4653013`.
- `git diff 576f84e HEAD` gồm 7 file (trước là 8): `backend/experiments/phase_8_2/__init__.py` đã có trên `main` (commit R4 `2c7ecfd`, cùng blob rỗng
  `e69de29`), nên không còn trong diff.
- Phần diff còn lại **giống từng dòng** với `git diff 43cdcd6 811d25d` (bỏ dòng `index`). Không file B1 nào bị `main` sửa từ `43cdcd6`:
  `git diff 811d25d HEAD` trên 6 file B1 rỗng ⇒ nội dung các file B1 sau rebase giống hệt nhánh cũ.
- Phần mới của `main` không giả định context 5: `grep` `max_context` / `context_documents` trong `api/routes/chat.py`, `experiments/phase_8_2/r4_numbers.py`,
  `llm/generator_openai_full_corpus.py`, `tests/test_api_chat.py`, `tests/test_r4_numbers.py` không ra dòng nào.
- Commit duy nhất B thêm trên nhánh: report này.

## 3. Cách đã chạy thật

Từ `/tmp/b71_b1/backend` (`data/`, `knowledge-base-hue/` là symlink tạm về working tree chung), `uv run --project /home/minhhieu/hue_rag`, Qdrant `:6335`
thật (chỉ đọc), e5-small CPU. Code nạp từ worktree (`retrieval.full_corpus.__file__` = `/tmp/b71_b1/backend/...`).

```bash
# 1. test (không key) — nhánh và main, cùng 6 file
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_retrieval.py \
  tests/test_full_corpus_context.py tests/test_api_chat.py tests/test_r4_numbers.py tests/test_gold_coverage.py -q
# 2. T1
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m evaluation.full_corpus_eval retrieval \
  --out /home/minhhieu/hue_rag/data/phase_8_2/b1/rebase_2710/retrieval_dense_bm25_rrf.jsonl
# 3. T5 (free)
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m experiments.phase_8_2.b1 nfd-check --question "$(cat .../data/phase_8_2/b1/nfd_question.txt)"
# 4. cổng ổn định: ss -ltn (không cổng 80xx bận) ⇒ 8013
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8013   # nền, tắt bằng TaskStop
uv run python data/phase_8_2/b1/rebase_2710/gate.py data/phase_8_2/b1/rebase_2710/live_gate.json   # 2 câu tự viết, perf_counter
```

## 4. Kết quả quan sát (lần chạy mới, 13:53–13:58 27/10)

| # | Kiểm | Kết quả | Đạt |
|---|---|---|---|
| — | 6 file test, nhánh | **50 passed**, 1 failed (`test_phase6_settings.py::test_openai_api_key_exists_without_leaking`), 1 error (`test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`) — cả hai cần key | ✓ |
| — | cùng 6 file, `main` `576f84e` | 49 passed, **cùng** 1 failed + 1 error ⇒ +1 = test NFC của B1 | ✓ |
| T1 | retrieval 158 câu giống byte mốc | sha256 `cefb2d1ad6094913…826e4`, **158** dòng | ✓ |
| T5 | `nfd-check` câu tự viết | `top10_equal` true, `packed_equal` true, 10 / 10, `max_context_documents` 10 | ✓ |
| cổng | `/` · `/health` | 200 · `ok`, 5 / 5 thành phần `ready` / `alive` | ✓ |
| cổng | câu trong kho (tự viết, loại câu hỏi thành phần món ăn) | 200; 4 nguồn trả về, có `[n]`; log `n_context_sources` **10**, `n_cited_sources` 4 | ✓ |
| cổng | câu ngoài kho (tự viết, câu tài chính) | 200; câu từ chối chuẩn; 0 nguồn; log `refusal` true | ✓ |
| cổng | log `chat_metrics` | trước 5 dòng (do `test_api_chat.py` ghi lúc chạy pytest) ⇒ sau **7**: +2 = số câu; grep 3 cụm chữ của 2 câu hỏi trong log = 0 | ✓ |
| cổng | thời gian client ↔ `total_ms` | 4.383,8 / 4.378,3 ms; 1.671,0 / 1.669,1 ms | ✓ |

Ghi chú: câu ngoài kho cũng có `n_context_sources` 10 — tìm kiếm luôn trả đoạn, model mới là bên từ chối (giống context 5, chỉ nhiều đoạn hơn).
Câu ngoài kho: 797 token vào; câu trong kho: 1.435 token vào (context 10).

**Tiền thật (tính từ token trong log):** vào 1.435 + 797 = 2.232 token × 0,1 USD / 1M = 0,0002232; ra 173 + 31 = 204 token × 0,5 USD / 1M = 0,000102
(token suy luận đã nằm trong token ra) ⇒ **≈ 0,000325 USD** ≤ trần 0,005.

Dữ liệu: `data/phase_8_2/b1/rebase_2710/` — `retrieval_dense_bm25_rrf.jsonl`, `nfd_check_after_rebase2.txt`, `live_gate.json`, `gate.py`.

## 5. Lỗi và giới hạn

- Không đo lại T2 / T3 (đầu vào model, điểm judge): các file B1 giống từng byte với nhánh cũ, và phần mới của `main` không đụng đường search ⇒ context ⇒
  prompt (chỉ thêm đếm / ghi log ở `chat.py` và trả usage ở generator). **Dùng lại** bằng chứng §4 / §7 của report gốc. Lý do: đầu vào, code đường này và
  môi trường không đổi. C có thể muốn chạy lại `t2_offline.py` (miễn phí) nếu thấy cần.
- Cổng chỉ 2 câu; latency đơn lẻ, không phải p50 / p95 (B65 đã đo context 10 ↔ 5 qua API: không khác).
- Không chạy full suite; các test cần key (`require_openai_key`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`) không chạy.
- Chatbot đang chạy trên máy User chưa đổi (nhánh chưa merge).

## 6. Bàn giao cho người kiểm

- Nhánh `p82-b1` sau rebase: `576f84e..p82-b1` = `2fa6f16` (code B1), `4653013` (report gốc), cộng commit report này. Push `--force-with-lease`.
- Kiểm rẻ nhất: `git range-diff 43cdcd6..811d25d 576f84e..p82-b1` (chỉ khác `__init__.py`); `git diff 811d25d p82-b1 -- backend/` (chỉ là phần mới của
  `main`); T1 (free, ~20 s).
- Sau B0 (không dừng): A merge ⇒ chatbot context 10 + NFC ⇒ A sửa đủ 4 chỗ báo cáo.
