# Implementation Report: rà code — gói 1b (một quy ước import + tách lỗi 503 / 409) — B-01 / C-01 + C-11

Người làm: B (Claude Opus 5.5, terminal `hue-rag-c3`)
Date: 2026-10-25 21:28 +0700 (`date`) · nền `main` `83e1aa9` (A commit trước khi sửa) → `47a4e32` (gói 3 của C, commit giữa chừng; không chồng dòng)
· chưa commit (A commit sau review) · paid ~0,0004 USD (ước, §4)
Canonical: plan `report_agent/2026-10-25_ra_soat_code/sua_1b_plan.md` bản 3 (sha `8b36bab7901c`, A duyệt 20:36; C review §7 ready); quy ước **(b)
import trần, chạy từ `backend/`**. Review: C.

## 1. Phạm vi

- Làm đúng §4 plan: (1) 3 test viết trước; (2) một quy ước import; (3) lỗi nạp model ⇒ `RetrievalDependencyError` (503); (4) C-11; (5) lệnh bắt buộc đổi
  phần B được sửa (guide build lại, notebook 03). Không đổi logic nào khác.
- **26 file** (25 sửa: +250 / −373, + 1 test mới): 14 code (`api/app.py`, `api/routes/chat.py`, `embedding/sparse.py`, `evaluation/full_corpus_eval.py`, `ingestion/chunking/full_corpus_chunker.py`,
  `ingestion/full_corpus_pipeline.py`, `ingestion/preview.py`, `ingestion/source_state.py`, `llm/phase6_live_smoke.py`, `reranking/cross_encoder.py`,
  `retrieval/full_corpus.py`, `retrieval/full_corpus_smoke.py`, `vectorstore/points.py`, `vectorstore/upsert.py`; `full_corpus_eval.py` chỉ bỏ
  chèn `sys.path`), harness `experiments/phase_8_1/g3_chunking.py`, 6 test (`conftest.py`, `test_api_chat.py`, `test_full_corpus_embedding.py`,
  `test_full_corpus_qdrant_ingestion.py`, `test_full_corpus_retrieval.py`, `test_full_corpus_sparse.py`) + 1 test mới `test_startup_model_missing.py`,
  3 notebook, `guides/full_corpus_rag.md`.
- `evaluation/full_corpus_eval.py:29-31`: sửa **sau** khi A commit gói 3 (`47a4e32`), như A dặn. Không đụng file nào khác của C.
- **A cần sửa** (governance / báo cáo User): `session_prompt/chạy_môi_trường.md:10-12`, `bao_cao_he_thong/BAO_CAO_KHO_DU_LIEU.md:89` (lệnh build ⇒ `cd backend &&
  uv run python -m ingestion.full_corpus_pipeline …`); `Project_Status.md` §8 bẫy mới (§5).

## 2. Thay đổi chính

1. **Test viết trước** (đỏ trên `main`, xem §4): T-A `test_api_catches_the_same_error_classes_that_retrieval_raises` (tiến trình con sạch, cwd `backend/`,
   `import api.app` như `uvicorn api.app:app`; assert 0 module nạp đôi + từng lớp `api.app` / `api.routes.chat` bắt **là** lớp module ném ra: retrieval,
   reranker, context builder, generator, citations); T-B `test_stale_corpus_at_startup_returns_409` (settings thật, chỉ trong bộ nhớ bỏ domain `foods` khỏi
   discovery ⇒ `POST /api/chat` 409 `corpus_reingest_required`; không key, không gọi OpenAI); T-C file riêng `test_startup_model_missing.py` (tiến trình con
   `HF_HUB_OFFLINE=1`, `HF_HOME` = `tmp_path` rỗng; điều kiện trước: Qdrant có collection runtime; assert lớp `core.schema.RetrievalDependencyError`, thông
   điệp "Dense model readiness failed", có `__cause__`, rồi `POST` 503 `retrieval_unavailable`). T-C do **User chạy `!`** (auto mode chặn B lẫn C).
2. **Một quy ước import:** bỏ 9 khối `try: from backend.X … except ModuleNotFoundError: from X …` — giữ nhánh trần; script chuyển có assert "thân `try` bỏ
   `backend.` = thân `except`" ⇒ không tên nào đổi (`/tmp/b30/drop_fallback*.py`); `full_corpus_pipeline.py` (9 dòng), 4 test, `g3_chunking.py` đổi
   `from backend.X` ⇒ `from X`. Bỏ chèn `sys.path` ở 5 file code (`api/app.py`, `evaluation/full_corpus_eval.py`, `llm/phase6_live_smoke.py`,
   `retrieval/full_corpus.py`, `retrieval/full_corpus_smoke.py`) và dọn hằng / `import sys` không còn dùng; hằng `REPO_ROOT` / `BACKEND_DIR` còn dùng chuyển
   xuống sau khối import. `conftest.py` chỉ chèn `backend/` (bỏ gốc repo). Chuỗi định danh dữ liệu `"backend.scoring.bm25.tokenize:v1"` (ghi trong sparse
   state) **giữ nguyên**. `preview.py`: docstring lệnh `cd backend && …`; `--output` mặc định neo `Path(__file__).resolve().parents[2]` (đường ra không đổi).
   Notebook 03 / 04 import trần + chèn `backend/`; 06 bỏ chèn gốc repo.
3. **Tách lỗi model khỏi 409:** `retrieval/full_corpus.py` — nạp / warm-up e5 và MiniLM lỗi ⇒ `RetrievalDependencyError` (giữ `from exc`; comment vì sao).
   `app.py` đã map lớp này ⇒ 503.
4. **C-11:** bỏ nhánh `except ComponentNotReadyError` ⇒ 409 lúc hỏi trong `api/routes/chat.py` (+ import); bỏ `CrossEncoderReranker.rerank()` (`grep -rn
   "\.rerank("` trong `backend/`, `notebooks/`, gồm test / harness = 0 trước khi gỡ).
5. **Lệnh:** `guides/full_corpus_rag.md` mục "Build lại index" bước 5 ⇒ `cd backend && uv run python -m ingestion.full_corpus_pipeline build …`, dòng 7A2 ghi "(lệnh
   lúc đó …)"; notebook 03 ô cuối cùng lệnh mới.

## 3. Cách đã chạy thật

Mọi lệnh `uv run` trong `.venv`, `HF_HUB_OFFLINE=1`; **không** `--env-file` trừ K6. Qdrant `:6335` chỉ đọc.
- K1: `uv run python -I data/ra_soat_code/tools/dup_modules.py` (tiến trình sạch cho từng điểm vào, cwd + import như lệnh thật); pytest `--collect-only` từ
  `backend/` và từ gốc, đếm `sys.modules`.
- K2 / K3: `cd backend && uv run python -m pytest <15 file liệt kê> -q -p no:cacheprovider -rfE` trước và sau sửa; sau sửa thêm **từng file riêng**. Danh sách 15
  file: `/tmp/b28/test_list.txt` (không gồm `test_startup_model_missing.py`).
- T-C: User chạy `! cd /home/minhhieu/hue_rag/backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_startup_model_missing.py -q -p no:cacheprovider`.
- K4: `cd backend && uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/b30/t1_retrieval.jsonl`; `sha256sum`, `wc -l`.
- K5: `python -m ingestion.full_corpus_pipeline --help`; `prepare_full_corpus_input()` (chỉ đọc) so `corpus_identity` / `sources` với build record;
  `python -m evaluation.full_corpus_eval --help`; `python -m experiments.phase_8_1.{g1_retrieval,g2_generate,g3_chunking,g4_rerank,g4_keyword} --help`; `import
  experiments.phase_8_1.g5_by_category`; `python -m ingestion.preview --help`; notebook: `uv run jupyter nbconvert --to notebook --execute notebooks/<nb>.ipynb
  --output-dir /tmp/b30/run` (3 notebook, bản tạm).
- K6: `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -I /tmp/b30/gate.py` — khởi động `uvicorn api.app:app --port 8011` thật (cổng trống
  trước khi chạy), `GET /`, `/health`, `POST /api/chat` 2 câu tự viết (1 trong kho, 1 ngoài kho), đọc log, SIGTERM.
- K7: `git diff --stat`; lọc mọi dòng diff không phải import / `sys.path` để đọc tay.

## 4. Kết quả quan sát

| # | Tiêu chí | Trước (`main`) | Sau | Đạt |
|---|---|---|---|---|
| K1 | Module nạp đôi | API 3 · evaluator 3 · harness g1 / g2 / g3 / g4_rerank / g5 7, g4_keyword 9 · notebook 06 3 · pytest 14 · build (gốc) 0 · notebook 03 / 04 0 | **0** ở cả 11 điểm vào theo lệnh mới (API, build `backend/`, evaluator, 6 harness, notebook 03-04, 06) + pytest collect 207 test từ `backend/` **0**, từ gốc **0** | ✔ |
| K2 | T-A / T-B / T-C | T-A **đỏ**, T-B **đỏ** (503 thay 409); T-C **đỏ đúng lý do**: `backend.core.schema.ComponentNotReadyError`, "Dense model readiness failed for e5-small-384", có `__cause__` (User chạy `!`, `data/ra_soat_code/b1b_tc_before.txt`) | T-A **xanh**, T-B **xanh**; T-C **xanh** — `1 passed in 14.49s` (User chạy `!` 21:3x, `data/ra_soat_code/b1b_tc_after.txt`): lớp `core.schema.RetrievalDependencyError`, thông điệp đúng, `__cause__`, 503 `retrieval_unavailable` | ✔ |
| K3 | 15 file test (cả nhóm) | 196 passed · 3 failed (T-A, T-B, `test_openai_api_key_exists_without_leaking`) · 7 error | **198 passed · 1 failed · 7 error** — 1 failed + 7 error đều là C-17 (`require_openai_key` / kiểm key khi không key), cùng danh sách trước sửa | ✔ (không tăng) |
| K3 | 15 file test (từng file) | — | cộng lại 198 passed, 1 failed (`test_phase6_settings.py`), 7 error (`test_api_chat.py` 3, `test_openai_full_corpus_generator.py` 2, `test_phase6_live_smoke.py` 2) = cả nhóm | ✔ |
| K4 | T1 retrieval | mốc `cefb2d1ad609…`, 158 dòng | `cefb2d1ad6094913…`, **158** dòng — giống byte | ✔ |
| K5 | Điểm vào | — | pipeline `--help` + `prepare_full_corpus_input`: 8.459 đoạn, identity = record, sources = record; evaluator `--help` (11 lệnh); 5 harness `--help`, g5 import; preview `--help`; notebook 03 / 04 / 06 Run All bản tạm **0 lỗi** (03 dot = BM25 3.75641; 04 `point_count` 8.459, 5 vector mẫu; 06 `/health`), repo outputs rỗng | ✔ |
| K6 | Cổng ổn định | mốc sau 1a | `/` 200 (1.346 byte) · `/health` 200 `ok`, 5 / 5 ready · câu trong kho 200, 4,0 s, marker [1] = `sources` [1], không còn `[Nguồn` · câu ngoài kho 200, 1,8 s, từ chối, 0 nguồn · log 0 dòng `ERROR` / `Traceback` · server tắt bằng SIGTERM | ✔ |
| K7 | Ngoài phạm vi | — | dòng diff ngoài import / `sys.path` chỉ có: 2 chỗ `RetrievalDependencyError` (+ comment), nhánh 409 lúc hỏi và `rerank()` bị gỡ, `preview.py` (docstring + default), di chuyển hằng sau import, lệnh trong guide / notebook | ✔ |

- Lệnh build **cũ** từ gốc repo (`python -m backend.ingestion.full_corpus_pipeline`) giờ báo `ModuleNotFoundError: No module named 'core'` — đúng quy ước (b),
  lỗi rõ, không âm thầm.
- `git diff --check`: sạch.
- **Tiền:** 2 lượt `gpt-6-luna` ở K6 (câu ngoài kho cũng gọi model — 1,8 s, context có nguồn, model từ chối). Route không log usage ⇒ **ước ~0,0004 USD** (theo
  lượt đo ở 1a: 0,000427 USD / 2 câu); trần gói 0,001 USD.

## 5. Lỗi và giới hạn

- "Qdrant lỗi khi đang hỏi ⇒ 503" (trước 500) vẫn chỉ suy ra từ code + T-A (lớp `RetrievalDependencyError` của `chat.py` là lớp retrieval ném); không dựng lỗi
  Qdrant thật.
- Hành vi đổi (A ghi vào `Project_Status.md` §8 + 4 chỗ `bao_cao_he_thong/`): (1) mọi lệnh chạy từ `backend/`, import trần — build: `cd backend && uv run python -m
  ingestion.full_corpus_pipeline build --candidate <id>`; (2) kho lệch lúc khởi động ⇒ 409 đúng thiết kế; model không nạp ⇒ 503; (3) lỗi lúc hỏi chỉ còn
  `RetrievalDependencyError` ⇒ 503 (nhánh `minilm` bị cấm nếu ném `ComponentNotReadyError` lúc hỏi ⇒ 500 `internal_error`). Bẫy mới: tên gói trần chung chung
  (`core`, `api`, `llm`…) có thể trùng thư viện cài sau này (hôm nay 0).
- `retrieval/full_corpus.py:68` hằng `REPO_ROOT` không ai dùng — có từ trước, không thuộc gói (ghi để dọn sau).
- Rebase `p82-b1`: theo plan §6 (xung đột khối import `retrieval/full_corpus.py`, đổi import `test_full_corpus_retrieval.py`, sửa comment `b1.py:23`, chạy lại
  T1–T2 của B1).

## 6. Bàn giao cho người kiểm (C)

- Đọc trước: `git diff -- backend notebooks guides/full_corpus_rag.md`; plan §4–§6; bảng §4.
- Chạy lại (free): `dup_modules.py`; 15 file test liệt kê (không `--env-file`); T1 sha; nếu cần cổng ổn định thì chạy lại (2 câu ~0,0004 USD). T-C: User chạy `!`
  (auto mode chặn), người kiểm đọc kết quả trong report.
- Lệch đã duyệt: không có ngoài plan; `full_corpus_eval.py:29-31` sửa sau commit gói 3 theo A.
