# Review: Phase 8.2 B1 — rebase lần 2 lên `main` `576f84e` (B71)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor) — merge vẫn **sau B0** (spec 8.2 §5 B1.3)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-86`)
Date: 14:04 27/10/2026 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` §4–§5 (B1); `session_prompt/CURRENT_HANDOFF.md` mục B71 + "Luật chung khi sửa code"
Implementation report: `phase_8_2_b1_rebase2_implementation.md` (trên `origin/p82-b1` `c3d5607`); review trước `phase_8_2_b1_rebase_review.md`

## 1. Phạm vi đã review

- Trạng thái Git: `origin/p82-b1` = `p82-b1` cục bộ = `c3d5607`; `576f84e` là tổ tiên; `576f84e..p82-b1` = 3 commit (`2fa6f16` code B1, `4653013` report gốc,
  `c3d5607` report này). Mục việc ghi đích `473f61e`, B rebase lên `576f84e` (A nhắn; `473f61e..576f84e` chỉ tài liệu) — đã khai báo trong report §1.
- Đường dẫn đổi: `git diff --stat 576f84e origin/p82-b1` = 8 file (6 file B1 + 2 report); không file untracked trên nhánh.
- Exact diff code: `settings.yaml` (`max_context_documents` 5 → 10), `settings_loader.py` (kiểm = 10), `retrieval/full_corpus.py` (`normalize_query` NFC trong
  `search`), 2 file test (test NFC mới; settings = 10), `experiments/phase_8_2/b1.py` (harness). Đọc đủ.
- `git range-diff 43cdcd6..811d25d 576f84e..origin/p82-b1`: commit code chỉ khác ở `backend/experiments/phase_8_2/__init__.py` (bản mới không còn tạo file
  vì `main` đã có cùng blob rỗng `e69de29` từ R4); commit report gốc `=`.
- `git diff --stat 811d25d origin/p82-b1 -- <6 file B1>` rỗng; `git diff --stat 43cdcd6 576f84e -- <6 file B1>` rỗng ⇒ `main` không sửa file nào của B1.
- Ghép với code mới của `main` (log `chat_metrics`, usage generator): `chat.py` đếm `len(packed.sources)` nên tự phản ánh context 10; không có hằng 5 ở phần
  mới (khớp grep của B).
- `main` hiện `719417e` (sau `576f84e` chỉ thêm tài liệu C62 + handoff / STATUS; không chạm file B1) ⇒ merge sau B0 không xung đột ở code.
- `git diff 576f84e origin/p82-b1 --check`: sạch.

## 2. Findings

Không có blocker hoặc major.

### m-1 — bằng chứng log của cổng ổn định không được giữ

- **Vị trí:** report §4 dòng "log `chat_metrics`" và "`n_context_sources` **10**"; `data/phase_8_2/b1/rebase_2710/` chỉ có `live_gate.json` (phản hồi client),
  không có dòng log; worktree `/tmp/b71_b1` (chứa `backend/logs/application.log`) đã gỡ.
- **Yêu cầu:** mục B71 "xem log có ghi số nguồn ≤ 10"; `Session_Prompt.md` §6 (bằng chứng tra lại được).
- **Tác động:** số trong report đúng (C tái lập độc lập, §4) nhưng người sau không tra lại được từ file của B. Không đổi kết luận.
- **Tiêu chí đóng:** không cần sửa lần này (C đã lưu 2 dòng log ở `c_review/`). Lần sau: script cổng chép các dòng `chat_metrics` mới (không chứa nội dung)
  vào thư mục dữ liệu trước khi gỡ worktree.

### m-2 — sau khi merge, vài tài liệu "Hiện hành" sẽ còn ghi context 5

- **Vị trí:** `guides/phase_6_generation_api.md` "Hiện hành" ("context pack tối đa Top 5"); `guides/phase_8_benchmark_model_selection.md` "Hiện hành" ("chatbot vẫn
  context 5", C62); `Project_Status.md` §1 sơ đồ + §4 ("context tối đa 5 whole chunk").
- **Yêu cầu:** `WORKFLOW.md` §6 (4 chỗ báo cáo khi hành vi đổi) — ngoài phạm vi B71 (nhánh chưa merge).
- **Tiêu chí đóng:** A thêm 2 guide trên vào danh sách sửa lúc merge B1 (cùng 4 chỗ báo cáo).

Quan sát (không phải finding): câu ngoài kho vẫn gửi 10 đoạn cho model (log C: 1.936 token vào ↔ 1.251 ở câu trong kho) — cùng hành vi context 5, chỉ nhiều
token hơn; đã biết (report §4 ghi chú). `gate.py` của B có mtime 13:58, sau `live_gate.json` 13:57 — nội dung khớp đầu ra; không ảnh hưởng.

## 3. Cách người kiểm chạy lại thật

Worktree riêng `/tmp/c_b71` (detached `origin/p82-b1` `c3d5607`, symlink tạm `data/`, `knowledge-base-hue/`; đã gỡ), từ `backend/`,
`uv run --project /home/minhhieu/hue_rag`, Qdrant `:6335` thật chỉ đọc, e5-small CPU; xác nhận code nạp từ worktree (`retrieval.full_corpus.__file__` =
`/tmp/c_b71/backend/retrieval/full_corpus.py`).

```bash
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_phase6_settings.py tests/test_full_corpus_retrieval.py \
  tests/test_full_corpus_context.py tests/test_api_chat.py tests/test_r4_numbers.py tests/test_gold_coverage.py -q
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m evaluation.full_corpus_eval retrieval --out /tmp/c_b71_t1.jsonl
ss -ltnp | grep ':80'   # không cổng 80xx bận ⇒ 8016
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8016   # nền, tắt bằng TaskStop
uv run python -I /tmp/c_b71_gate.py   # 2 câu C tự viết (khác câu của B), perf_counter
```

## 4. Kết quả quan sát (lần chạy mới, 14:00–14:04 27/10)

| Kiểm | Kết quả | Khớp report B |
|---|---|---|
| 6 file test (không key) | 50 passed, 1 failed `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`, 1 error `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan` — cả hai cần key | ✓ |
| T1 158 câu | sha256 `cefb2d1ad609` (= mốc), 158 dòng — do C chạy, không dùng file của B | ✓ |
| `/` · `/health` | 200 · `ok`, 5 / 5 `ready` / `alive` | ✓ |
| câu trong kho (C tự viết, loại câu liệt kê món) | 200, 6 nguồn, có `[n]`; log `n_context_sources` **10**, `n_cited_sources` 6, `outcome` `success` | ✓ |
| câu ngoài kho (C tự viết, kiến thức chung) | 200, câu từ chối chuẩn, 0 nguồn; log `refusal` true, `n_context_sources` 10 | ✓ |
| dòng `chat_metrics` | 5 (do pytest) ⇒ **7**: +2 = số câu; grep 2 câu hỏi trong log = 0 | ✓ |
| client ↔ `total_ms` | 4.905,3 / 4.900,2 ms; 1.726,0 / 1.724,3 ms | ✓ |

Tiền (từ token trong log): vào 1.251 + 1.936 = 3.187 × 0,1 / 1M = 0,0003187; ra 225 + 44 = 269 × 0,5 / 1M = 0,0001345 ⇒ **≈ 0,000453 USD** (trần B71 0,005).
Bằng chứng private: `data/phase_8_2/b1/rebase_2710/c_review/` (`gate_c.py`, `chat_metrics_2lines.log` — chỉ số đo, `t1_c.jsonl`).

Dùng lại (không phải lần chạy mới): T2 offline / T3 (judge) / T5 từ report gốc + B71 — hợp lệ vì 6 file B1 giống từng byte nhánh cũ và phần mới của `main` chỉ
thêm đếm / ghi log ở route và trả usage ở generator, không đổi search ⇒ context ⇒ prompt (C đọc diff `43cdcd6..576f84e -- backend`).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy T2 offline, T5, test cần key, full suite. Cổng 2 câu, latency đơn lẻ (không phải p50 / p95; B65 đã đo context 10 ↔ 5).
- Không đọc / mở `khoa.json`, câu kín.

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`: nhánh `p82-b1` `c3d5607` sẵn sàng merge **sau B0** (User đọc cặp mù; A áp luật dừng spec 8.2 §3 mục 4). Lúc merge: cổng ổn
định trên `main` sau merge, 4 chỗ báo cáo + 2 guide ở m-2. Không cần B sửa gì.
