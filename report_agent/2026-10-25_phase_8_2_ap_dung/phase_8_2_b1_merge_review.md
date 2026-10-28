# Review: Phase 8.2 B1 — merge vào `main` (`510e1a8`)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 0 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · việc C71
Date: 09:39 28/10/2026 (`date`)
Canonical guide: spec 8.2 `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` §11 (sha file `5255f3274707`)
Implementation report: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_merge_implementation.md` (A, 09:34 28/10)

## 1. Phạm vi đã review

- Report merge của A (full-read); spec 8.2 §11; `git show 510e1a8`; bằng chứng `data/phase_8_2/b1/merge_2810/` (`retrieval_dense_bm25_rrf.jsonl`,
  `gate.py`, `live_gate.json`, `metrics_before.txt`); các dòng `chat_metrics` 09:31–09:34 của `backend/logs/application.log`.
- Code B1 (`c3d5607`) đã được C review ở `phase_8_2_b1_rebase2_review.md` (ready) ⇒ review này chỉ kiểm **phép merge** và **cổng sau merge**, không review lại
  nội dung B1.
- 0 USD: không chạy lại server (bằng chứng cổng đủ, xem §4).

## 2. Findings

Không có blocker, major hay minor.

Ghi nhận (không phải finding):
- Merge được push trước review này. Spec §11 đặt điều kiện "B1 đạt B1.2 + review chéo"; review code B1 đã có (rebase2, ready), và cây merge trùng đúng kết quả
  merge tự động (§4 mục 1) ⇒ rủi ro thấp. A đã tự ghi điều này ở report §3.
- Log `application.log` dùng chung cho pytest và server: dòng 409 `corpus_reingest_required` lúc 09:32:28 là của `test_api_chat.py:199-208` (test cố ý dựng kho
  lệch trong bộ nhớ, server khởi động rồi dừng ngay ở dòng 1250–1255), **không** phải server cổng. Đếm "37 ⇒ 39" vẫn đúng vì không có test chạy giữa
  `metrics_before.txt` (09:33) và cổng (09:34). Bẫy đã biết (report rebase2 §cổng ghi "5 dòng do pytest").

## 3. Cách người kiểm chạy lại thật

Chạy trên working tree chung, `main` `62c284f` (backend giống `510e1a8`: `git diff --stat 510e1a8 HEAD -- backend/` rỗng; `git status backend/` sạch), Qdrant
`:6335` thật, e5-small CPU, không nạp key:

```bash
git merge-base d922bf7 c3d5607                       # 576f84e…
git merge-tree --write-tree d922bf7 c3d5607          # so với git rev-parse 510e1a8^{tree}
git diff c3d5607 510e1a8 --stat -- backend/          # so với git diff 576f84e d922bf7 --stat -- backend/
git diff --check d922bf7 510e1a8
cd backend
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_retrieval.py tests/test_full_corpus_context.py \
  tests/test_api_chat.py tests/test_r4_numbers.py tests/test_gold_coverage.py -q
HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --out ../data/phase_8_2/b1/merge_2810/c_review/retrieval_dense_bm25_rrf.jsonl
HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.b1 nfd-check --question "$(cat ../data/phase_8_2/b1/nfd_question.txt)"
```

## 4. Kết quả quan sát

| # | Khẳng định của report | Người kiểm thấy (lần chạy mới, trừ khi ghi "đọc file") | Khớp |
|---|---|---|---|
| 1 | Merge không sửa tay | `merge-tree --write-tree` = `1c2ed9ca2f3c…` = `510e1a8^{tree}`; cha 1 `d922bf7`, cha 2 `c3d5607`; `origin/main` `62c284f`, `origin/p82-b1` `c3d5607` | ✓ |
| 2 | Phần `main` thêm không chạm file B1 | `diff c3d5607 510e1a8 -- backend/` = 4 file (`chat.py`, `g1_retrieval.py`, `test_api_chat.py`, `test_gold_coverage.py`), trùng `diff 576f84e d922bf7 -- backend/`; B1 đổi 6 file khác | ✓ |
| 3 | Hành vi đổi = context 10 + NFC | `settings.yaml:55` `max_context_documents: 10`; `settings_loader.py:75` đòi 10; `full_corpus.py:97` `normalize_query`, gọi ở `:420` | ✓ |
| 4 | Test 51 passed + 2 cần key | **1 failed, 51 passed, 1 error** (58 s): failed `test_openai_api_key_exists_without_leaking`, error `test_health_is_cached_and_ready_after_real_lifespan` — đúng 2 test cần key | ✓ |
| 4b | +1 so B71 là test `main` thêm | `test_gold_coverage.py`: 2 hàm test ở `c3d5607` ⇒ 3 ở `510e1a8` | ✓ |
| T1 | 158 dòng, sha `cefb2d1ad609` | file mới của C: sha `cefb2d1ad609`, 158 dòng, `cmp` giống byte file của A | ✓ |
| T5 | `top10_equal`, `packed_equal` true, context 10 | `max_context_documents` 10, `top10_equal` true, `packed_equal` true, `packed_count` NFC 10 / NFD 10 | ✓ |
| cổng | 2 câu: 200 + nguồn; từ chối chuẩn | (đọc file) `live_gate.json`: trong kho 200, 6 nguồn, có `[n]`; ngoài kho 200, câu từ chối chuẩn, 0 nguồn. Log 09:34:28 / :30: `n_context_sources` 10 / 10, `n_cited_sources` 6 / 0, `refusal` false / true, `model` `gpt-6-luna`; server 09:34:20 khởi động đủ retrieval + tokenizer + generator | ✓ |
| cổng | `chat_metrics` +2, grep câu = 0 | (đọc file) `metrics_before.txt` 37; dòng `chat_metrics` của server cổng đúng 2 (09:34:28, :30); `grep -c -F` 2 câu hỏi trong log = 0 / 0 | ✓ |
| cổng | client ≈ `total_ms` | 5.144,5 / 5.139,3 ms và 2.515,8 / 2.514,0 ms | ✓ |
| tiền | ≈ 0,000423 USD | log: vào 1.282 + 1.936 = 3.218, ra 172 + 31 = 203 ⇒ 0,0003218 + 0,0001015 = 0,0004233 | ✓ |
| — | `git diff --check` | sạch | ✓ |

Ý nghĩa: `main` nay chạy context 10 + NFC đúng như nhánh B1 đã review; đường tìm (T1) giống byte mốc nên kết quả tìm của 158 câu không đổi; cổng sống trên
server thật đạt.

Dùng lại (không phải lần chạy mới): cổng sống của A (`live_gate.json` + log) — không chạy lại server vì bằng chứng log đủ trường, đúng giờ, khớp client.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại cổng sống (chọn tiết kiệm, A cho phép chỉ chạy khi thiếu bằng chứng). Latency cổng là 2 câu đơn lẻ; p50 / p95 context 10 chưa đo lại —
  để bộ "trước" của đợt sửa kho (B78), như report §3.
- Không kiểm 5 chỗ báo cáo (A đang sửa song song; C kiểm phần mô tả hành vi khi A nhờ).
- Context 10 chọn bằng judge Claude, chưa có mốc người (B0 dời — spec §11).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Merge `510e1a8` đúng là merge tự động của `d922bf7` + `c3d5607`, không sửa tay; test, T1, T5 tái lập được; cổng sống của A
đủ bằng chứng. Việc trung bình (merge code đã review trong phạm vi spec §11 User duyệt) ⇒ A đóng và báo User. Tiếp: A sửa 5 chỗ báo cáo (context 5 ⇒ 10),
C kiểm phần mô tả hành vi.
