# Plan: rà code — gói 1b (một quy ước import + tách lỗi 503 / 409) — B-01 / C-01 + C-11

Người viết: B (Claude Opus 5.5, terminal `hue-rag-c3`) · 2026-10-25 20:15 +0700 (`date`) · nền `main` `63fec4f` · **chưa sửa code**
Người review: C · duyệt: A (ghi sha vào `CURRENT_HANDOFF.md`, `WORKFLOW.md` §9.1)

## Căn cứ để review

| File | Mục cần đọc |
|---|---|
| `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` | B-01 (phương án a / b / c, cách kiểm) |
| `report_agent/2026-10-25_ra_soat_code/ra_soat_code_C.md` | C-01 (gồm điểm (b) "model không nạp" và (c) hai đầu vào), C-11 |
| `session_prompt/CURRENT_HANDOFF.md` | "Luật chung mọi gói", "Cổng ổn định sau mỗi gói", "Đợt 2" (mục gói 1b) |
| `backend/api/app.py:1-100`, `backend/api/routes/chat.py:55-90`, `backend/retrieval/full_corpus.py:18-112, 760-840` | code bị sửa (đọc trực tiếp) |

Mọi số trong plan tính lại được bằng `data/ra_soat_code/tools/{inventory,dup_modules}.py` (private, chỉ đọc) và các lệnh ghi ở §3.

## 1. Mục tiêu

1. Mỗi module `backend/` chỉ nạp **một lần** ở mọi điểm vào (API, build, evaluator, harness, notebook, pytest) ⇒ lớp lỗi retrieval ném ra
   **là** lớp API bắt.
2. Mã lỗi đúng thiết kế (guide 6, bảng mã lỗi): index không khớp corpus lúc khởi động ⇒ **409** `corpus_reingest_required`; model tìm kiếm không
   nạp được (thiếu HF cache, lỗi tải) ⇒ **503** `retrieval_unavailable` (hiện gắn chung lớp với "index cũ" — C-01 (b)); Qdrant lỗi khi đang hỏi
   ⇒ **503** (hiện ra 500 — suy ra từ code).
3. C-11: bỏ nhánh không tới được — `except ComponentNotReadyError` ⇒ 409 **lúc hỏi** trong route; `CrossEncoderReranker.rerank()` (0 lời gọi).
4. Không đổi kết quả tìm kiếm / câu trả lời: T1 retrieval giống byte mốc.

Không thuộc gói: lệnh trong tài liệu khác ngoài các lệnh bắt buộc đổi theo quy ước chọn (B-17 làm ngay sau, theo quy ước này); nhánh `minilm`
(C-06, đợt 3); sửa harness ngoài phần import.

## 2. Hiện trạng đo được (mốc trước, `main` `63fec4f`, 20:1x)

**Module nạp đôi** (`dup_modules.py`: tiến trình sạch, cwd + câu import đúng như lệnh chạy; đếm tên có cả `X` lẫn `backend.X`):

| Điểm vào (lệnh hiện dùng) | cwd | Nạp đôi |
|---|---|---:|
| API — `uv run uvicorn api.app:app` | `backend/` | **3** (`core`, `core.schema`, `core.settings_loader`) |
| build — `python -m backend.ingestion.full_corpus_pipeline build` | gốc | 0 |
| evaluator — `python -m evaluation.full_corpus_eval` | `backend/` | **3** |
| harness 8.1 G2 / G3 — `python -m experiments.phase_8_1.g2_generate` / `g3_chunking` | `backend/` | **7** (+ `embedding.sparse`, `reranking.cross_encoder`) |
| notebook 03 / 04 (gốc vào `sys.path`, import `backend.*`) | `notebooks/` | 0 |
| notebook 06 (gốc + `backend/` vào `sys.path`, import trần) | `notebooks/` | **3** |
| pytest — `cd backend && python -m pytest --collect-only tests/` (202 test) | `backend/` | **14** |

Gốc: 9 file dùng `try: from backend.X … except ModuleNotFoundError: from X …` (`embedding/sparse.py`, `ingestion/chunking/full_corpus_chunker.py`,
`ingestion/preview.py`, `ingestion/source_state.py`, `reranking/cross_encoder.py`, `retrieval/full_corpus.py`, `retrieval/full_corpus_smoke.py`,
`vectorstore/points.py`, `vectorstore/upsert.py`) + 5 file code chèn `sys.path` (`api/app.py`, `evaluation/full_corpus_eval.py`,
`llm/phase6_live_smoke.py`, `retrieval/full_corpus.py`, `retrieval/full_corpus_smoke.py`) + `tests/conftest.py`, 3 notebook. Khi cả gốc lẫn
`backend/` nằm trong `sys.path`, nhánh `try` thắng ⇒ nạp bản `backend.*` cạnh bản trần.

**Hành vi lỗi (đã quan sát, kiểm chéo `kiem_cheo_B.md` R-05):** kho lệch build record (settings trong bộ nhớ, `exclude_parts += ["foods"]`) ⇒
retrieval ném `backend.core.schema.ComponentNotReadyError` "source state is stale", API bắt hụt ⇒ **503** thay 409. Model e5 không nạp được ⇒
`ComponentNotReadyError` (`retrieval/full_corpus.py:816-823`; MiniLM `:827-834`) ⇒ hôm nay *tình cờ* 503 (cũng nhờ bắt hụt). Qdrant lỗi lúc hỏi
⇒ 500 (chỉ suy ra từ code). Qdrant tắt lúc khởi động ⇒ lỗi kết nối không bọc (`:800`) ⇒ 503 — đúng, không đổi.

**T1 mốc:** `cd backend && HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --out <file>` ⇒ 158 dòng, sha256
`cefb2d1ad609…` (= `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`, B1 T1).

## 3. So sánh hai quy ước

(a) **chỉ `backend.*`**, mọi lệnh chạy từ **gốc repo** (`uv run uvicorn backend.api.app:app`, `python -m backend.evaluation.full_corpus_eval`,
`python -m pytest backend/tests/…`). (b) **import trần** (`core.*`, `retrieval.*`…), mọi lệnh chạy từ **`backend/`** (build đổi thành
`cd backend && python -m ingestion.full_corpus_pipeline build`). Cả hai: bỏ hết `try / except ModuleNotFoundError`; bỏ chèn `sys.path` trong code
(cwd của `python -m` / `uvicorn` / `python -m pytest` đã nằm trong `sys.path`); notebook giữ **một** dòng chèn thư mục gốc import (gốc cho (a),
`backend/` cho (b)) vì Jupyter chạy từ `notebooks/`.

| Chỉ số (đo bằng `inventory.py`, file tracked) | (a) `backend.*`, từ gốc | (b) trần, từ `backend/` |
|---|---:|---:|
| File code phải đổi import (`backend/` trừ test / harness) | **18** | **13** |
| File test phải đổi | 12 | 5 |
| File harness 8.1 phải đổi | 6 (+ lệnh chạy của cả 6) | 1 (`g3_chunking.py`) |
| Notebook phải đổi | 3 (06 đổi import; 03 / 04 chỉ dòng `sys.path`) | 3 (03 / 04 đổi import; 06 dòng `sys.path`) |
| Tài liệu hiện hành có lệnh phải đổi (`bao_cao_he_thong/`, `session_prompt/`, `guides/full_corpus_rag.md`; plan / report cũ không sửa) | 6 file (lệnh API, pytest, evaluator) | 3 file (lệnh build) + 1 ô notebook 03 |
| Lệnh dùng hằng ngày phải đổi | API, pytest, evaluator, harness (4 loại) | build (1 loại) |
| Nhánh `p82-b1` (B1) phải đổi khi rebase | `b1.py` + `test_full_corpus_retrieval.py` sang `backend.*`; lệnh B1 chạy từ gốc | chỉ xung đột import block (§6) |
| Module nạp đôi sau sửa (mục tiêu) | 0 ở mọi điểm vào | 0 ở mọi điểm vào |
| T1 giống byte | phải đạt | phải đạt |
| Rủi ro riêng | uvicorn chạy nhầm từ `backend/` ⇒ `ModuleNotFoundError: backend` (lỗi rõ, không âm thầm) | tên gói trần chung chung (`core`, `api`, `llm`, `evaluation`…) có thể trùng thư viện cài sau này — **hôm nay 0 trùng** (`importlib.util.find_spec` trong `.venv`: cả 12 tên = `None`) |

Cả hai đều chạy được mọi điểm vào (build, API, pytest, harness, notebook) sau khi sửa đúng lệnh; khác nhau ở **số chỗ phải đổi** và **lệnh nào
đổi**. Pytest lấy gốc repo làm rootdir ở cả hai (node id `backend/tests/…` — `Project_Status.md` §8 không đổi).

**Đề xuất: (b) import trần, chạy từ `backend/`** — lý do: (1) ít chỗ đổi hơn khoảng một nửa (13 / 5 / 1 / 3 so với 18 / 12 / 6 / 3; tài liệu 3 so với
6); (2) giữ nguyên 4 lệnh dùng nhiều nhất (API, pytest, evaluator, harness — đều đang chạy từ `backend/`), chỉ đổi lệnh build vốn hiếm và luôn
cần duyệt; (3) rebase B1 nhẹ hơn. Cái giá: lệnh build đổi chỗ chạy; rủi ro trùng tên gói trần là tiềm ẩn (0 hôm nay) — ghi bẫy vào
`Project_Status.md` §8. Chọn (a) nếu A / User muốn mọi lệnh cùng chạy từ gốc repo (đồng nhất với build và notebook) và chấp nhận đổi nhiều hơn.
**A duyệt chọn (a) hay (b) trước khi B sửa.**

## 4. Thay đổi (theo (b); nếu chọn (a), cùng các bước với chiều ngược lại)

1. **Test viết trước, phải đỏ trên `main`** (thêm vào `backend/tests/test_api_chat.py`, không cần key, 0 USD):
   - **T-A danh tính lớp:** tiến trình con sạch, cwd `backend/`, `import api.app` (đúng như `uvicorn api.app:app`) ⇒ assert không tên nào nạp
     đôi (`X` và `backend.X`) và `api.routes.chat.{ComponentNotReadyError, RetrievalDependencyError, InvalidQueryError}` **is** lớp cùng tên trong
     `retrieval.full_corpus`. Trên `main`: đỏ (3 tên nạp đôi, `is` False).
   - **T-B kho đổi ⇒ 409:** `create_app` thật với settings đọc thật rồi **chỉ trong bộ nhớ** `exclude_parts += ["foods"]` (không sửa kho / Qdrant /
     file) ⇒ `POST /api/chat` trả **409** `corpus_reingest_required` (route trả lỗi retrieval trước bước sinh ⇒ không gọi OpenAI). Trên `main`: đỏ
     (503).
   - **T-C (canh hồi quy) model không nạp ⇒ 503:** tiến trình con với `HF_HUB_OFFLINE=1` + `HF_HOME` trỏ thư mục rỗng trong `tmp_path` (đầu vào thật,
     không mock) ⇒ `create_app` ⇒ `POST /api/chat` **503** `retrieval_unavailable`. Trên `main`: **xanh** (nhờ bắt hụt); sửa import mà quên bước 3
     ⇒ đỏ (409) — test này chặn đúng bẫy C-01 (b).
2. **Một quy ước import:** 13 file code + 5 test + `experiments/phase_8_1/g3_chunking.py` đổi `backend.X` ⇒ `X`; bỏ 9 khối `try / except
   ModuleNotFoundError` (giữ đúng một dòng import); bỏ chèn `sys.path` ở 5 file code (API / evaluator / harness chạy từ `backend/` đã có cwd);
   `conftest.py` bỏ chèn gốc repo (giữ `backend/` cho pytest gọi từ gốc); notebook 03 / 04 đổi import + chèn `backend/`, notebook 06 bỏ chèn gốc.
   Không đổi logic nào khác.
3. **Tách lỗi model khỏi 409:** `retrieval/full_corpus.py:816-823` (nạp + warm-up e5) và `:827-834` (MiniLM) ném `RetrievalDependencyError` thay
   `ComponentNotReadyError` (giữ `from exc`). `app.py` đã map `RetrievalDependencyError` ⇒ 503.
4. **C-11:** bỏ `except (ComponentNotReadyError,)` ⇒ 409 trong `api/routes/chat.py:72-80` (chỉ nhánh `minilm` bị cấm ném được lúc hỏi; nếu xảy ra
   ⇒ 500 `internal_error` như lỗi không lường trước); bỏ `CrossEncoderReranker.rerank()` (`reranking/cross_encoder.py:95-114`; `grep -rn
   "\.rerank(" backend notebooks` = 0 — kiểm lại ngay trước khi gỡ, kể cả test / harness).
5. **Lệnh bắt buộc đổi theo quy ước** (để hệ thống chạy được ngay sau gói; đếm 20:2x, `main` + B26 chưa commit). Phần lệnh còn lại (B-17)
   làm ngay sau, cùng quy ước.

   | Nếu chọn | File:dòng | Đổi |
   |---|---|---|
   | (b) | `session_prompt/chạy_môi_trường.md:10-12` (**A sửa** — governance) | "chạy từ gốc repo" + `python -m backend.ingestion.full_corpus_pipeline` ⇒ `cd backend` + `python -m ingestion.full_corpus_pipeline` (`--env-file ../.env`) |
   | (b) | `guides/full_corpus_rag.md:174` (mục build lại, bước 5) | như trên; `:118` (mục 7A2, lịch sử) giữ, thêm "(lệnh lúc đó)" |
   | (b) | `bao_cao_he_thong/BAO_CAO_KHO_DU_LIEU.md:89` | như trên (A sửa — báo cáo User) |
   | (b) | `notebooks/03_embedding_models.ipynb` ô cuối | như trên |
   | (a) | `session_prompt/chạy_môi_trường.md:6` (**A sửa**) | `uv run uvicorn api.app:app` ⇒ chạy từ gốc `uv run uvicorn backend.api.app:app` |
   | (a) | `session_prompt/Project_Status.md:185` (**A sửa**) | `cd backend && … pytest tests/<file>` ⇒ từ gốc `… pytest backend/tests/<file>` |
   | (a) | `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md:85`, `BAO_CAO_SINH_CAU_TRA_LOI_API.md:47`, `BAO_CAO_BO_CAU_HOI_GOLDEN.md:49` | lệnh `uvicorn api.app` / `python -m evaluation.…` ⇒ `backend.…` từ gốc |
   | (a) | `CURRENT_HANDOFF.md` (mục Cổng ổn định — **A sửa**), harness 8.1 / B1 trong report đang mở | `cd backend && … uvicorn api.app:app` ⇒ từ gốc |

## 5. Tiêu chí nghiệm thu (ghi trước) và cổng ổn định

| # | Tiêu chí | Cách đo | Đạt khi |
|---|---|---|---|
| K1 | Không module nạp đôi | `dup_modules.py` (7 điểm vào, lệnh **mới**) + pytest `--collect-only` | 0 ở cả 8 |
| K2 | Lớp lỗi cùng danh tính; 409 / 503 đúng | T-A, T-B, T-C | đỏ trên `main` (T-A, T-B) ⇒ xanh sau sửa; T-C xanh trước và sau |
| K3 | Test các file chạm | liệt kê file: `test_api_chat.py`, `test_full_corpus_retrieval.py`, `test_full_corpus_chunker.py`, `test_full_corpus_embedding.py`, `test_full_corpus_qdrant_ingestion.py`, `test_full_corpus_sparse.py`, `test_bm25.py`, `test_citations.py`, `test_full_corpus_context.py`, `test_full_corpus_eval.py`, `test_golden_full_corpus.py`, `test_phase6_settings.py`; không `--env-file` | đạt; lỗi cũ C-17 (`require_openai_key`) ghi rõ số, không tăng |
| K4 | Kết quả tìm kiếm không đổi | T1 (§2) | sha256 `cefb2d1ad609…`, 158 dòng |
| K5 | Mọi điểm vào chạy được | build: `cd backend && uv run python -m ingestion.full_corpus_pipeline --help` + `prepare_full_corpus_input()` (chỉ đọc, 8.459 đoạn, `corpus_identity` = build record) — **không** build thật (ghi Qdrant); evaluator `--help` + T1; harness 8.1 G1–G5 `--help`; notebook 03 / 04 / 06 Run All bản tạm | chạy hết, 0 lỗi import |
| K6 | **Cổng ổn định** (`CURRENT_HANDOFF.md`) | `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env uvicorn api.app:app --port 8011`: `/` 200, `/health` 5 thành phần ready, 1 câu trong kho (200, marker khớp `sources`) + 1 câu ngoài kho (từ chối) tự viết; log sạch; tắt server | như mốc sau 1a (`63fec4f`) |
| K7 | Không đổi ngoài phạm vi | `git diff --stat`; grep logic | chỉ dòng import / `sys.path` / 2 chỗ lớp lỗi / 2 chỗ gỡ C-11 / lệnh |

Lệch K1–K7 ⇒ **dừng**, tìm nguyên nhân, báo A; không sửa tiêu chí.

## 6. Nhánh `p82-b1` (B1) khi rebase sau gói 1b

B1 chạm `backend/retrieval/full_corpus.py` (thêm `import unicodedata` sát khối import + hàm `normalize_query` + 2 dòng trong `search`),
`backend/tests/test_full_corpus_retrieval.py` (import kiểu `backend.*` — thuộc 5 test phải đổi ở (b)), `backend/core/settings_loader.py`,
`backend/config/settings.yaml`, `backend/tests/test_phase6_settings.py`, thêm `backend/experiments/phase_8_2/b1.py` (import trần — hợp (b)). Khi rebase:
(1) giải xung đột khối import `retrieval/full_corpus.py` theo quy ước mới (giữ `import unicodedata`); (2) đổi import `test_full_corpus_retrieval.py`
phần B1 thêm sang trần; (3) chạy `dup_modules.py` (0); (4) chạy lại **T1–T2 của B1** (free) — không dùng lại bằng chứng B1 cũ vì đầu vào đã đổi
(`Session_Prompt.md` §6). Nếu chọn (a): thêm đổi import `b1.py` + lệnh chạy B1 từ gốc.

## 7. Quyền, tiền, rủi ro, điều kiện dừng

- Sửa code rủi ro trung bình (Phase đã duyệt): A commit + push `main` **trước** khi B sửa (User 18:3x). B không commit. Review: C.
- Tiền: chỉ K6 (2 câu `gpt-6-luna`, ước ~0,0005 USD theo lượt 1a: 0,000427 USD / 2 câu) — trong trần chung 0,05 USD; ghi token + tiền từ log.
- Qdrant chỉ đọc; không build index; không sửa kho; T-B / T-C chỉ đổi đầu vào trong bộ nhớ / `tmp_path`.
- Rủi ro: sót một import ⇒ `ModuleNotFoundError` ở điểm vào ít dùng (đã liệt kê đủ 7 điểm vào trong K1 / K5); test phụ thuộc thứ tự `sys.path`
  (conftest) — chạy từng file và cả nhóm; notebook chạy từ `notebooks/` — Run All bản tạm.
- Dừng khi: T1 lệch; phải sửa logic ngoài §4; phải đụng file C đang khai báo; vượt tiền.

## 8. Đầu ra

`report_agent/2026-10-25_ra_soat_code/sua_1b_implementation.md` (K1–K7 với số thật trước / sau, lệnh, tiền); `STATUS_B.md`; nhắn A. A cập nhật
`Project_Status.md` §8 (bẫy import, lệnh build mới) + 4 chỗ `bao_cao_he_thong/` (mã lỗi đổi hành vi).
