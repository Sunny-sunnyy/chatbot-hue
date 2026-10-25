# Review: gói 1b (một quy ước import + tách lỗi 503 / 409) — B-01 / C-01 + C-11

Decision: **ready_for_user_confirmation** — K1–K7 đạt khi C chạy lại bằng script riêng; không blocker / major; 2 ghi chú `minor` (không chặn).
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-7f`)
Date: 2026-10-25 21:48 (`date`)
Canonical: plan `report_agent/2026-10-25_ra_soat_code/sua_1b_plan.md` bản 3 (sha `8b36bab7901c`, A duyệt 20:36), quy ước (b)
Implementation report: `report_agent/2026-10-25_ra_soat_code/sua_1b_implementation.md` (B, 21:28)

## 1. Phạm vi đã review

- Git: nền `main` `47a4e32`; working tree chưa commit. File của gói: 21 file `backend/` + test mới `backend/tests/test_startup_model_missing.py`, 3 notebook,
  `guides/full_corpus_rag.md` — khớp danh sách report. Cũng đang đổi (không thuộc B): `session_prompt/chạy_môi_trường.md`,
  `bao_cao_he_thong/BAO_CAO_KHO_DU_LIEU.md` (A sửa lệnh build — governance / báo cáo User), `CURRENT_HANDOFF.md`, `STATUS_B/C`.
- Không đọc `STATUS_B`; không chạy script của B (`data/ra_soat_code/tools/dup_modules.py`, `/tmp/b30/*`). Script của C: `/tmp/c41/`, bản dùng lại
  `data/ra_soat_code_2026-10-25/tools/review_1b/` + `review_1b_plan/` (plugin pytest, mô phỏng notebook), `sua_3/gate.py`. 0 USD trừ cổng ổn định.
- Đọc: mọi dòng diff `backend/` **không phải** import / `sys.path` (lọc bằng grep, đọc tay); `api/app.py` diff đầy đủ; danh sách `raise` trong
  `build_full_corpus_retrieval_service`; `reranking/cross_encoder.py` (lớp ném); `test_startup_model_missing.py`; 2 file kết quả T-C của User.

## 2. Findings

Không có blocker / major.

- **m1 (minor, ghi nhận — không thuộc gói):** sau khi hết bắt hụt, **`RetrievalConfigurationError` lúc khởi động** (candidate / treatment / reranker lạ —
  `retrieval/full_corpus.py:705-712`) giờ thực sự ra **409** `corpus_reingest_required` "Dữ liệu tra cứu cần được lập chỉ mục lại" theo đúng `app.py:66-72`
  (trước đây 503 do bắt hụt). Thông điệp không khớp nguyên nhân (lỗi cấu hình, không phải index cũ), nhưng **không tới được** với settings thật vì
  `settings_loader.py` đã ép đúng tổ hợp runtime. Ánh xạ này có từ Phase 6, không do 1b. Tiêu chí đóng (nếu A muốn): ghi vào danh sách dọn sau; không sửa trong 1b.
- **m2 (minor):** hằng `REPO_ROOT` không ai dùng (`retrieval/full_corpus.py:68` — B đã ghi §5; cũng là m-6 của review plan đợt 3). Dọn ở đợt 3.

## 3. Cách người kiểm chạy lại thật

Từ `backend/` trừ khi ghi khác, `HF_HUB_OFFLINE=1`, **không** `--env-file` trừ cổng ổn định; Qdrant `:6335` chỉ đọc:

- K1: `python3 /tmp/c41/dup_entry.py` (tiến trình con `-I`, cwd + import như lệnh **mới**, 12 điểm vào: API, build, preview, smoke Phase 6, evaluator, 6 harness)
  + `dup_nb.py` (mô phỏng ô đầu + import của 3 notebook, cwd `notebooks/`, đúng `sys.path` notebook giờ chèn) + pytest `--collect-only` với plugin đếm
  `sys.modules` (từ `backend/` và từ gốc).
- K3: `uv run python -m pytest <15 file tests/test_*.py trừ test_startup_model_missing.py> -q -p no:cacheprovider -rfE` (không key: `env -u OPENAI_API_KEY`).
- K4: `uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/c41/t1.jsonl`; `sha256sum`, `wc -l`.
- K5 / (d): `uv run python -m <m> --help` cho `ingestion.full_corpus_pipeline`, `ingestion.preview`, `evaluation.full_corpus_eval`, 5 harness 8.1 có argparse,
  `llm.phase6_live_smoke`; `import experiments.phase_8_1.g5_by_category`; `prepare_full_corpus_input()` so `corpus_identity` / `sources` với build record;
  từ gốc: `python -m backend.ingestion.full_corpus_pipeline --help` (lệnh cũ); 3 notebook `jupyter nbconvert --execute` ra `/tmp/c41/run` + md5 file repo.
- (c): `grep -rn "\.rerank(\|def rerank\b" backend notebooks`; `grep -n "corpus_reingest_required\|409" api/routes/chat.py api/app.py`.
- Cổng ổn định: `uv run --env-file ../.env python -I /tmp/c38/gate.py` (uvicorn `api.app:app` thật `:8011`, cổng trống trước khi chạy, 2 câu tự viết, tắt server).
- **T-C: dùng lại** kết quả User chạy `!` trong terminal B (`data/ra_soat_code/b1b_tc_before.txt`, `b1b_tc_after.txt`) — **không phải lượt chạy của C** (lệnh
  đặt `HF_HOME` rỗng bị auto mode chặn trong session C, 20:2x). C đọc file test để xác nhận nó kiểm đúng điều plan duyệt.

## 4. Kết quả quan sát

| # | Tiêu chí | Kết quả của C | Đạt |
|---|---|---|---|
| K1 | Không module nạp đôi | **0** ở cả 12 điểm vào theo lệnh mới (thêm preview + smoke Phase 6 so với plan) · notebook 03 / 04 / 06: **0** (ô đầu chỉ chèn `backend/`) · pytest collect **207** test: **0** từ `backend/`, **0** từ gốc. Trước (C đo 20:2x trên `main`): API 3, evaluator 3, harness 7 / g4k 9, nb06 3, pytest 14 | ✔ |
| K2 | T-A / T-B / T-C | T-A, T-B **đạt** (trong lượt K3). T-C (dùng lại, User): trước **đỏ đúng lý do** (`backend.core.schema.ComponentNotReadyError`, "Dense model readiness failed…", có `__cause__`), sau `1 passed in 14.49s`. File test: điều kiện trước Qdrant có collection runtime (assert); tiến trình con `HF_HUB_OFFLINE=1` + `HF_HOME=tmp_path` (đầu vào thật); assert lớp `core.schema.RetrievalDependencyError` + thông điệp + `__cause__` + 503 `retrieval_unavailable` — đúng plan §4.1 | ✔ |
| K3 | 15 file test | **198 passed · 1 failed · 7 error** (148 s) — 1 failed `test_phase6_settings.py::test_openai_api_key_exists_without_leaking`, 7 error `require_openai_key` (`test_api_chat.py` 3, `test_openai_full_corpus_generator.py` 2, `test_phase6_live_smoke.py` 2) = **C-17**, đúng danh sách B; trước sửa (B): 196 / 3 / 7 — +2 passed là T-A, T-B | ✔ |
| K4 | T1 retrieval | sha256 `cefb2d1ad609…`, **158** dòng — giống byte mốc | ✔ |
| K5 | Mọi điểm vào | 9 CLI `--help` rc 0; g5 import; `prepare_full_corpus_input`: 8.459 đoạn, identity = record **True**, sources = record **True**; lệnh build cũ từ gốc ⇒ `ModuleNotFoundError: No module named 'core'` (lỗi rõ, đúng (b)); 3 notebook Run All bản tạm **0 lỗi** (03 BM25 3.75641; 04 8.459 đoạn khớp record, `point_count` / `payloads_verified` 8.459, 5 vector mẫu; 06 `gpt-6-luna`, `/health` 200), md5 3 file repo không đổi | ✔ |
| K6 | Cổng ổn định (C chạy lại) | `/` 200 (1.346 byte) · `/health` 200 `ok`, 5 / 5 `ready` · câu trong kho 200, 4,0 s, marker [1, 3] = `sources` [1, 3] · câu ngoài kho 200, 2,1 s, từ chối, 0 nguồn · log 0 `ERROR` / `Traceback` · server tắt (SIGTERM). Tiền: 2 lượt, route không log usage ⇒ **ước ~0,0004 USD** | ✔ |
| K7 | Ngoài phạm vi | dòng diff ngoài import / `sys.path`: 2 chỗ `ComponentNotReadyError` ⇒ `RetrievalDependencyError` (nạp e5, MiniLM; giữ `from exc`); gỡ nhánh `except ComponentNotReadyError` ⇒ 409 trong `chat.py` + gỡ `rerank()` (`cross_encoder.py`); `preview.py` docstring + `--output` neo gốc repo; dời `REPO_ROOT` / `BACKEND_DIR` xuống sau import; 2 test mới + 1 file test mới — **đúng plan §4**, không có logic khác | ✔ |

**(b) Có nhánh nào đổi mã lỗi ngoài ý muốn không** — liệt kê mọi `raise` của `build_full_corpus_retrieval_service` (`retrieval/full_corpus.py:700-790`) và lớp
`app.py` bắt (`:66-90`):

| Lỗi lúc khởi động | Lớp | Mã hôm nay (bắt hụt) | Sau 1b | Đúng thiết kế? |
|---|---|---|---|---|
| build record thiếu / đọc lỗi; sparse state thiếu / sha lệch / identity lệch; collection không có / schema sai / số point lệch; kho lệch record (freshness) | `ComponentNotReadyError` | 503 | **409** | ✔ (index cần build lại) |
| e5 không nạp / warm-up lỗi hoặc sai chiều; MiniLM không nạp | `RetrievalDependencyError` (đổi ở 1b) | 503 (tình cờ) | **503** | ✔ |
| Qdrant tắt (`collection_exists` / `get_collection` / `count` không bọc) | `Exception` khác | 503 | 503 | ✔ |
| candidate / treatment / reranker lạ | `RetrievalConfigurationError` | 503 | 409 | m1 (không tới được) |

Lúc hỏi: `RetrievalDependencyError` ⇒ **503** (trước 500 — suy ra từ code, như B ghi); `ContextBudgetError` / `GenerationError` / `CitationIntegrityError` cùng lớp như
trước (T-A); `ComponentNotReadyError` chỉ còn nhánh `minilm` (bị cấm) ⇒ 500 `internal_error` — trước cũng 500 (lớp lệch). Harness / evaluator không bắt lỗi theo lớp
(S3 C34) ⇒ không bị ảnh hưởng. **Kết luận (b): không có nhánh đổi mã ngoài ý muốn.**

**(c)** `rerank()`: 0 định nghĩa, 0 lời gọi trong `backend/`, `notebooks/`; `409` / `corpus_reingest_required` chỉ còn ở `app.py:67-68` (khởi động).
**(d)** harness 8.1: 5 `--help` + g5 import đạt; notebook: 3 / 3 Run All đạt.

`git diff --check`: sạch.

## 5. Giới hạn

- T-C không phải lượt chạy của C (dùng lại kết quả User — đầu vào, code và môi trường không đổi từ lúc User chạy sau sửa: working tree cùng diff).
- "Qdrant lỗi lúc hỏi ⇒ 503" chỉ suy ra từ code + T-A (không dựng lỗi Qdrant thật — `Session_Prompt.md` §8).
- Tiền cổng ổn định là ước (route không log usage — ứng viên cải tiến mục 5).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** (rủi ro trung bình ⇒ A đóng, báo User). A commit; A sửa `Project_Status.md` §8 (lệnh mới, bẫy tên gói trần) + 4 chỗ
`bao_cao_he_thong/` (mã lỗi đổi hành vi: kho lệch ⇒ 409, model không nạp ⇒ 503, Qdrant lỗi lúc hỏi ⇒ 503). m1, m2 vào danh sách dọn đợt 3.
