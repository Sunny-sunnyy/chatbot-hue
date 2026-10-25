# Review: plan gói 1b (một quy ước import + tách lỗi 503 / 409) — B-01 / C-01 + C-11

Decision: **changes_requested** — 2 điểm phải sửa trước khi code (P1, P2: hai test nghiệm thu của K2 như đang viết không chứng minh được
điều cần chứng minh), 4 điểm `minor`. Phần còn lại (số đếm, đề xuất (b), các bước, rebase, tiền, dừng) **đạt**. Sửa xong C chỉ kiểm phần đổi.
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-7f`)
Date: 2026-10-25 20:25 (`date`)
Bản được review: `report_agent/2026-10-25_ra_soat_code/sua_1b_plan.md` **sha `aa9bbf3650d6`** (A báo 20:2x: bản trước `97bf89fc5926` chỉ khác
bảng lệnh §4 bước 5 — C đã đọc bản trước rồi kiểm thêm bảng đó trên bản mới).
Cách review (`WORKFLOW.md` §9.1): chỉ dựa vào "Căn cứ để review" của plan + code + lệnh chỉ đọc. Không đọc `STATUS_B`, không đọc tin của B,
không chạy script của B (`data/ra_soat_code/tools/{inventory,dup_modules}.py`) — mọi số dưới đây do script riêng của C
(`/tmp/c37/`, bản dùng lại `data/ra_soat_code_2026-10-25/tools/review_1b_plan/`). 0 USD, không sửa code.

## 1. Phạm vi đã review

- Căn cứ: B-01 (`ra_soat_code_B.md`), C-01 + C-11 (`ra_soat_code_C.md`), "Luật chung mọi gói" / "Cổng ổn định" / "Đợt 2" (`CURRENT_HANDOFF.md`),
  code `api/app.py:1-100`, `api/routes/chat.py:55-90`, `retrieval/full_corpus.py:18-112, 760-840`. Đọc thêm khi cần trả lời câu A hỏi:
  `embedding/full_corpus.py:103-125, 389-393`, `ingestion/full_corpus_pipeline.py:52-53`, `core/settings_loader.py:7, 93, 114`,
  `ingestion/source_state.py:57`, `ingestion/preview.py:4, 312-315`, `experiments/phase_8_1/*` (đầu file), notebook 03 / 04 / 06 (ô đầu),
  `git diff main...p82-b1`.

## 2. Findings

### P1 (phải sửa) — T-A tham chiếu tên mà `api.routes.chat` không có (và sẽ càng không có sau C-11)
- Vị trí: plan §4 bước 1, T-A: "`api.routes.chat.{ComponentNotReadyError, RetrievalDependencyError, InvalidQueryError}` **is** lớp cùng tên trong
  `retrieval.full_corpus`".
- Bằng chứng: `api/routes/chat.py:9-15` import `CitationIntegrityError, ComponentNotReadyError, ContextBudgetError, GenerationError,
  RetrievalDependencyError` — **không** có `InvalidQueryError` (`grep -n InvalidQueryError api/` = 0). Bước 4 (C-11) bỏ nhánh `except
  ComponentNotReadyError` trong route ⇒ import đó thành thừa và sẽ bị gỡ ⇒ T-A viết như plan ra `AttributeError` (đỏ vì sai test, không phải
  vì lỗi C-01) cả trước lẫn sau sửa.
- Tác động: K2 không đo được.
- Tiêu chí đóng: T-A so đúng các lớp mà API **bắt**: `api.app.{ComponentNotReadyError, RetrievalConfigurationError, RetrievalDependencyError}`
  (`app.py:21-25, 70-84`) và `api.routes.chat.RetrievalDependencyError` (`chat.py:81`) `is` lớp cùng tên trong `retrieval.full_corpus`; giữ thêm
  assert "không tên nào nạp đôi" (đã đủ mạnh một mình).

### P2 (phải sửa) — T-C có thể xanh giả: 503 không chứng minh nhánh "model không nạp"
- Vị trí: plan §4 bước 1, T-C; K2.
- Bằng chứng (đọc code): `build_full_corpus_retrieval_service` chỉ nạp model ở **bước 4** (`retrieval/full_corpus.py:815-823`), sau build record,
  sparse state, collection Qdrant (`:761-811`). `create_dense_runner` ⇒ `resolve_snapshot(allow_download=False)` ⇒ `snapshot_download(…,
  local_files_only=True)` (`embedding/full_corpus.py:115-122, 393`) ⇒ `HF_HOME` rỗng **là** đầu vào thật, không mock (đúng như plan nói). Nhưng nếu
  Qdrant không chạy, hoặc bất kỳ lỗi nào trước bước 4 rơi xuống `except Exception` (`app.py:84-90`), API cũng trả 503 ⇒ T-C đạt mà không chạm nhánh
  model. Sau sửa, Qdrant tắt lúc khởi động cũng ⇒ 503 (plan §2 nói "đúng, không đổi").
- Tiêu chí đóng: T-C kiểm thêm **nguyên nhân**, không chỉ mã HTTP — ví dụ trong cùng tiến trình con gọi `build_full_corpus_retrieval_service`
  và assert lớp lỗi là `RetrievalDependencyError` (sau sửa) với thông điệp "Dense model readiness failed" (hoặc `__cause__` là lỗi
  không tìm thấy snapshot); và test ghi rõ cần Qdrant `:6335` đang chạy (giống các test retrieval khác).
- Ghi chú: C **không chạy được** T-C trên `main` để xem trước — lệnh với `HF_HOME` rỗng bị lớp kiểm an toàn của auto mode chặn trong session
  này (sub-agent S1 cũng gặp ở C34). B chạy được thì ghi kết quả "trước" vào report.

### m1 — K1 / K5 chưa liệt kê đủ harness 8.1
- Bằng chứng (`dup_entry.py`, tiến trình con `-I`, cwd + import như lệnh thật): nạp đôi hôm nay — g1 7, g2 7, g3 7, g4_rerank 7, **g4_keyword 9**
  (+ `scoring`, `scoring.bm25`), g5 7. Plan §2 / K1 chỉ nêu G2 / G3; K5 ghi "G1–G5 `--help`" nhưng `g5_by_category.py` không có argparse.
- Tiêu chí đóng: K1 đo cả 6 harness (import); K5 dùng `import` cho g5.

### m2 — K3 thiếu file test bị ảnh hưởng
- Bằng chứng: plan §4 bước 2 đổi `sys.path` trong `llm/phase6_live_smoke.py` và `retrieval/full_corpus_smoke.py`, và sửa `tests/conftest.py` (ảnh
  hưởng **mọi** test). K3 không có `test_phase6_live_smoke.py` (test của `phase6_live_smoke.py`), `test_static_ui.py`,
  `test_openai_full_corpus_generator.py`. `backend/tests/` có 15 file test + `conftest.py`.
- Tiêu chí đóng: K3 chạy **cả 15 file** (liệt kê từng file, không `--env-file`, không `--deselect` — miễn phí; `test_phase6_live_smoke.py` an toàn khi
  không key, xem C-18), chạy từng file và cả nhóm (thứ tự `sys.path`); số error do `require_openai_key` (C-17) ghi rõ, không tăng.

### m3 — `ingestion/preview.py` có lệnh trong docstring + đường ra mặc định phụ thuộc cwd
- Bằng chứng: `preview.py:4` docstring `uv run python -m backend.ingestion.preview --output reports/artifacts/…`; `:312-315` `--output` mặc định
  `reports/artifacts/…` (tương đối cwd). Theo (b), chạy từ `backend/` sẽ ghi vào `backend/reports/…`. Mọi đường dẫn khác trong code neo theo
  `__file__` (`settings_loader.py:7, 93, 114`, `source_state.py:57`, `full_corpus_pipeline.py:52-53`, harness `REPO_ROOT / …`) ⇒ (b) không làm hỏng
  build / harness; chỉ 2 converter `backend/scripts/` (B-13, không ai gọi) dùng đường dẫn tương đối gốc repo.
- Tiêu chí đóng: sửa docstring cùng đợt; đường ra mặc định để gói 2 (B-04) hoặc neo theo `REPOSITORY_ROOT` — ghi lựa chọn trong report.

### m4 — rebase `p82-b1`: thêm một dòng việc
- Bằng chứng: `git show p82-b1:backend/experiments/phase_8_2/b1.py:23` comment "import này cũng đưa gốc repo + `backend/` vào `sys.path`" — sau (b)
  bỏ chèn `sys.path` trong evaluator thì câu này sai (b1 vẫn chạy được vì cwd `backend/`, import trần). Phần còn lại §6 đúng: nhánh chỉ thêm
  `import unicodedata` vào khối import thư viện chuẩn (`full_corpus.py:16`) + `normalize_query`; test thêm import kiểu `backend.*` (thuộc 5 test phải đổi).
- Tiêu chí đóng: §6 thêm "sửa / bỏ comment `b1.py:23`".

## 3. Trả lời 6 điểm A hỏi

1. **Số đếm (a) / (b) — khớp B.** Nạp đôi (script C): API 3, build 0, evaluator 3, harness G2 / G3 7, notebook 03 0 / 04 0 / 06 3, pytest
   `--collect-only` (202 test) **14** — đúng từng số trong plan §2 (thêm g1 / g4r / g5 7, g4k 9 — m1). File phải đổi (`count_change.py`, AST, mọi
   import kể cả trong hàm / try): (a) code **18**, test **12**, harness **6**, notebook 1 đổi import (+ 2 notebook chỉ dòng `sys.path`) — khớp; (b) code
   10 + test 4 có import `backend.*`, cộng 3 file code + `conftest.py` chỉ đổi dòng chèn `sys.path` (`api/app.py`, `evaluation/full_corpus_eval.py`,
   `llm/phase6_live_smoke.py`) = **13 / 5**, harness **1** (`g3_chunking.py`), notebook 03 / 04 — khớp. 11 tên gói trần: `find_spec` trong `.venv` (cwd
   `/tmp`) đều `None` — khớp.
2. **(b) và lệnh build `cd backend && …`:** chạy được — mọi đường dẫn dữ liệu trong code neo theo `__file__` (m3), không theo cwd. Harness 8.1: hôm
   nay đã chạy từ `backend/` với import trần (trừ `g3_chunking.py:46` `from backend.ingestion.preview …` — plan đã liệt kê); đường dữ liệu dùng
   `REPO_ROOT` ⇒ không đổi. Notebook: 03 / 04 hôm nay import `backend.*` với gốc trong `sys.path` ⇒ phải đổi import + chèn `backend/` (plan có);
   06 bỏ chèn gốc (plan có). Bảng lệnh §4 bước 5 (bản mới): grep `python -m backend\.` trong tài liệu hiện hành (`session_prompt/`, `bao_cao_he_thong/`,
   `guides/full_corpus_rag.md`, `AGENTS.md`, `skills/`, notebook) ra đúng 4 chỗ của (b) + dòng lịch sử `full_corpus_rag.md:118` — **đủ**; số dòng khớp.
3. **T-C có phải đầu vào thật:** **có** (`snapshot_download(local_files_only=True)` trên `HF_HOME` rỗng — thiếu file thật, không mock). Nhưng 503 một
   mình không chứng minh nhánh model ⇒ **P2**.
4. **Gỡ nhánh 409 lúc hỏi + `rerank()`:** đủ bằng chứng. `search()` chỉ ném `ComponentNotReadyError` ở nhánh `minilm` (`full_corpus.py:651`, runtime
   cấm — `settings_loader.py:36`); các module `search()` gọi (`embedding/`, `scoring/`, `vectorstore/`) không có `raise ComponentNotReadyError`
   (grep = 0); model nạp sẵn lúc khởi động nên `embed_queries` không nạp lại lúc hỏi. `rerank()`: `grep -rn "\.rerank(\|getattr(.*rerank"` trên
   `backend/`, `notebooks/` = 0 lời gọi (chỉ còn chữ "rerank" là tên stage trace `full_corpus.py:681`, `test_full_corpus_retrieval.py:831`; 2 plan cũ
   trong `docs/` nhắc tên — lịch sử). Hệ quả gỡ 409 lúc hỏi ghi đúng trong plan (minilm ⇒ 500 `internal_error`). Nhớ cập nhật T-A (P1).
5. **Rebase `p82-b1`:** cách trong §6 đúng và đủ (giải xung đột khối import, đổi import test phần B1, `dup_modules`, chạy lại T1–T2 của B1, không
   dùng lại bằng chứng cũ); thêm m4.
6. **K1–K7 có đủ cho cổng ổn định:** cổng (1) test ⇒ K3 — **chưa đủ** (m2); (2) uvicorn thật ⇒ K6 — đủ (cùng lệnh cổng, chạy từ `backend/` hợp (b));
   (3) chạm tìm kiếm ⇒ K4 T1 giống byte + K5 `corpus_identity` = build record — đủ; (4) 4 chỗ `bao_cao_he_thong/` ⇒ plan §8 (A) — đủ (mã lỗi đổi
   hành vi); (5) A commit — §7. Sau P1, P2, m1, m2: đủ.

## 4. Kết quả quan sát (chạy thật, chỉ đọc)

| Đo | Kết quả |
|---|---|
| `dup_entry.py` (9 điểm vào) | API 3 · build 0 · evaluator 3 · g1 / g2 / g3 / g4r / g5 7 · g4k 9 |
| `dup_nb.py` (mô phỏng ô đầu + import của notebook, cwd `notebooks/`) | 03: 0 · 04: 0 · 06: 3 |
| pytest `--collect-only` + plugin đếm `sys.modules` | 202 test, 14 tên nạp đôi (`core`, `ingestion.*`, `retrieval.*`, `scoring.*`, `vectorstore.*`) |
| `count_change.py` (AST, file tracked) | (a) 18 / 12 / 6 / 1 (+2) · (b) 10 + 3 `sys.path` / 4 + conftest / 1 / 2 |
| `find_spec` 13 tên trần trong `.venv` | tất cả `None` |
| T-C trên `main` | **NOT RUN** (auto mode chặn) — trả lời bằng đọc code |

## 5. Giới hạn

- T-C chưa chạy (xem P2). Không chạy pytest đầy đủ (không cần cho review plan). Đếm "file phải đổi" của C dựa trên AST import; không đếm chuỗi
  lệnh trong docstring (m3 là ví dụ).

## 6. Decision và bước tiếp theo

**changes_requested** — B sửa P1, P2 (bắt buộc) và m1–m4 (một lượt), ra sha mới; C kiểm lại đúng các phần đổi; rồi A duyệt sha + chọn (a) / (b).
Khuyến nghị của C về quy ước: **đồng ý (b)** — số đếm của B đúng, (b) không làm hỏng đường dẫn nào (m3), rủi ro trùng tên = 0 hôm nay.

## 7. Kiểm lại bản 3 (sha `8b36bab7901c`) — C, 2026-10-25 20:35

**ready_for_user_confirmation** (A duyệt sha). Chỉ kiểm phần đổi:
- **P1 — đóng.** §4.1 T-A so `getattr(nơi_bắt, tên) is getattr(module_ném, tên)` theo bảng lớp **API thật sự bắt**: `api.app` khởi động 3 lớp
  (`app.py:21-25, 70-84`), `api.routes.chat` `RetrievalDependencyError` + `ContextBudgetError` / `GenerationError` / `CitationIntegrityError`; bỏ
  `InvalidQueryError` và `ComponentNotReadyError` của `chat.py`. Module ném đúng (`reranking/cross_encoder.py` ném cả `ComponentNotReadyError` /
  `RetrievalDependencyError` — C đã đọc ở C34).
- **P2 — đóng.** T-C file riêng `tests/test_startup_model_missing.py`; điều kiện trước Qdrant `:6335` có collection runtime (assert, không skip ⇒ Qdrant tắt
  là đỏ có thông điệp, không xanh giả); assert lớp `core.schema.RetrievalDependencyError` + "Dense model readiness failed" + `__cause__`, rồi 503; đỏ
  trên `main` vì đúng lý do (lớp `backend.core.schema.ComponentNotReadyError`). User chạy bằng `!` (auto mode chặn cả B lẫn C) — đúng
  `WORKFLOW.md` §3.6.
- **m1 — đóng** (§2 thêm g1 / g4_rerank / g5 7, g4_keyword 9; K1 11 điểm vào; K5 g5 dùng import). **m2 — đóng** (K3 cả 15 file). **m3 — đóng**
  (`preview.py` docstring + `--output` neo gốc repo — đường ra không đổi khi chạy từ gốc, đúng khi chạy từ `backend/`). **m4 — đóng** (§6 bước 3).
  Dòng (a) ở §4.5 đã bỏ, header ghi quy ước (b).
- Không có điểm mới.
