# Implementation Report: C64 mục 2 — `dense_ms` trong log `chat_metrics` làm tròn 1 chữ số (B70 m-2)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-86`) · Date: 14:24 27/10/2026 (`date`) · Việc: `session_prompt/CURRENT_HANDOFF.md` → C64 mục 2 (A giao 14:15).
Trạng thái: **chờ review** (B). Không commit (A commit). 0 USD ngoài cổng ổn định.

## 1. Thay đổi

- `backend/api/routes/chat.py:111-112`: `dense_ms` lấy từ trace tìm kiếm (giữ 3 chữ số, `retrieval/full_corpus.py:449`) giờ làm tròn 1 chữ số trước khi ghi
  log, như mọi trường `*_ms` khác (`_elapsed_ms`, `chat.py:32-33`). Thiếu khóa trong trace ⇒ vẫn `null` như trước (log không được đổi phản hồi).
- `backend/tests/test_api_chat.py:91`: thêm một dòng ghim trong test sẵn có `test_real_first_chunk_budget_error_has_no_partial_answer` (test đi qua tìm kiếm thật).
- Không đổi phản hồi API, không đổi tìm kiếm / ngữ cảnh / sinh. Trace (`RetrievalTrace.timings_ms`) không đổi.

## 2. Cách đã chạy thật

```bash
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_api_chat.py -q            # mốc trước sửa + sau sửa
# thử ngược: chat.py bản HEAD + test mới ⇒ phải đỏ
cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8016      # nền, tắt bằng TaskStop
uv run python -I data/phase_8_2/c64_gate/gate.py                                             # 2 câu tự viết, perf_counter
```

## 3. Kết quả quan sát (lần chạy mới, xong trước 14:23 27/10)

| Kiểm | Kết quả | Đạt |
|---|---|---|
| `test_api_chat.py` trước sửa | 9 passed, 1 error (`test_health_is_cached_and_ready_after_real_lifespan`, cần key) | mốc |
| thử ngược (code HEAD + test mới) | 1 failed: `assert 25.467 == 25.5` ⇒ test bắt đúng lỗi | ✓ |
| `test_api_chat.py` sau sửa | 9 passed, 1 error — giống mốc | ✓ |
| `git diff --check` | sạch | ✓ |
| cổng: `/` · `/health` | 200 · `ok`, 5 / 5 `ready` / `alive` | ✓ |
| cổng: câu trong kho (tự viết, loại câu liệt kê) | 200, 2 nguồn, có `[n]`; log `dense_ms` **37.1**, `n_context_sources` 5 | ✓ |
| cổng: câu ngoài kho (tự viết, kiến thức chung) | 200, câu từ chối chuẩn, 0 nguồn; log `refusal` true, `dense_ms` **21.3** | ✓ |
| dòng `chat_metrics` | 25 ⇒ 27: +2 = số câu; grep 2 câu hỏi trong log = 0 | ✓ |
| client ↔ `total_ms` | 5.658,1 / 5.652,8 ms; 1.743,2 / 1.741,5 ms | ✓ |

Tiền (token trong log): vào 833 + 1.054 = 1.887 × 0,1 / 1M = 0,0001887; ra 330 + 51 = 381 × 0,5 / 1M = 0,0001905 ⇒ **≈ 0,000379 USD**.
Bằng chứng private: `data/phase_8_2/c64_gate/` (`gate.py`, `chat_metrics_2lines.log` — chỉ số đo).

## 4. Giới hạn

- Không chạy test cần key, full suite. Cổng 2 câu trên `main` (context 5); nhánh `p82-b1` không có sửa này — khi merge B1 không xung đột (B1 không chạm
  `chat.py` / `test_api_chat.py`).
- B70 m-1 (test danh sách trường chưa đi qua generator): theo mục việc **không viết code** — A ghi bẫy.
