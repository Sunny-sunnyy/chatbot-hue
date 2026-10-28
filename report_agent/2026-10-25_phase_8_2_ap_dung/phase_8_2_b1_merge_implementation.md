# Implementation Report: Phase 8.2 B1 — merge vào `main` (A, 28/10)

Người làm: A (Claude Opus 5.5, terminal `hue-rag-bf`) · Date: 09:34 28/10/2026 (`date`) · Trạng thái: **chờ review** (người kiểm: C, việc C71).
Căn cứ: User 28/10 chọn PA3 — B0 không chặn B1 (spec 8.2 §11, sha `5255f3274707`, commit `d922bf7`). Code B1 = nhánh `p82-b1` `c3d5607` (C review ready
`phase_8_2_b1_rebase2_review.md`).

## 1. Phạm vi

`git merge --no-ff p82-b1` trên `main` `d922bf7` ⇒ **`510e1a8`** (đã push). Không sửa tay dòng nào; `git merge-tree` báo sạch trước khi merge. Hành vi đổi:
`max_context_documents` 5 ⇒ 10 (`backend/config/settings.yaml`, `backend/core/settings_loader.py`), câu hỏi chuẩn hóa NFC trước khi tìm
(`backend/retrieval/full_corpus.py` `normalize_query`). Phần `main` thêm sau gốc rebase `576f84e`: `api/routes/chat.py` (`dense_ms` làm tròn),
`experiments/phase_8_1/g1_retrieval.py` (gold v3), `tests/test_api_chat.py`, `tests/test_gold_coverage.py` — không chạm file B1.

## 2. Kiểm đã chạy (09:2x–09:34 28/10, `main` `510e1a8`, Qdrant `:6335` thật, e5-small CPU)

| # | Kiểm | Kết quả | Đạt |
|---|---|---|---|
| 1 | 6 file test như B71 (`test_phase6_settings`, `test_full_corpus_retrieval`, `test_full_corpus_context`, `test_api_chat`, `test_r4_numbers`, `test_gold_coverage`), không key | **51 passed**, 1 failed + 1 error = đúng 2 test cần key (`test_openai_api_key_exists_without_leaking`, `test_health_is_cached_and_ready_after_real_lifespan`); B71 50 passed — +1 là test `main` thêm ở `test_gold_coverage.py` | ✓ |
| T1 | `evaluation.full_corpus_eval retrieval` | sha256 `cefb2d1ad609…`, 158 dòng = mốc | ✓ |
| T5 | `experiments.phase_8_2.b1 nfd-check` (câu NFD đã lưu) | `top10_equal` true, `packed_equal` true, `max_context_documents` 10 | ✓ |
| cổng | uvicorn `:8013` (`ss -ltn`: không cổng 80xx bận) — `/` · `/health` | 200 · `ok`, 5 / 5 `ready` / `alive` | ✓ |
| cổng | câu trong kho tự viết (loại: liệt kê món) | 200, 6 nguồn, có `[n]`; log `n_context_sources` 10, `n_cited_sources` 6; client 5.144,5 ms / `total_ms` 5.139,3 | ✓ |
| cổng | câu ngoài kho tự viết (địa lý nước ngoài) | 200, câu từ chối chuẩn, 0 nguồn; log `refusal` true; client 2.515,8 / 2.514,0 ms | ✓ |
| cổng | `chat_metrics` | 37 ⇒ 39 dòng (+2 = số câu); grep 2 câu hỏi trong log = 0 | ✓ |

Lệnh: như `phase_8_2_b1_rebase2_implementation.md` §3, chạy từ `backend/` của working tree chung; server `--env-file` đường dẫn tuyệt đối (đường tương
đối `../.env` lỗi khi chạy nền). Dữ liệu: `data/phase_8_2/b1/merge_2810/` (`retrieval_dense_bm25_rrf.jsonl`, `gate.py`, `live_gate.json`, `metrics_before.txt`).

**Tiền thật (token log):** vào 1.282 + 1.936 = 3.218 × 0,1 / 1M = 0,0003218; ra 172 + 31 = 203 × 0,5 / 1M = 0,0001015 ⇒ **≈ 0,000423 USD**.

## 3. Giới hạn

- Context 10 chọn bằng judge Claude, **chưa có mốc người** (B0 dời — spec 8.2 §11).
- Cổng 2 câu: latency đơn lẻ, không phải p50 / p95. Câu trong kho 5,1 s (context 5 B65: p95 5,7 s) — đo p50 / p95 context 10 ở bộ "trước" của đợt sửa kho (B78).
- Không chạy T2 / T3 (đường search ⇒ context ⇒ prompt không đổi so với `c3d5607`; dùng lại bằng chứng B1 / B71, lý do: file B1 giống byte, phần mới của
  `main` chỉ chạm log và nhãn gold).
- Merge đã push trước review của C (code B1 đã C review ready; review này kiểm phép merge + cổng).
