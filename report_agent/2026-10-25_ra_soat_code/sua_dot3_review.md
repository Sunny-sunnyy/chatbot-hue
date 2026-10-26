# Review: rà code — đợt 3 (gói 2 + gói 5 + B-12), toàn nhánh `dot3`

Decision: **ready_for_user_confirmation** (không blocker, không major; 3 minor không chặn)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-3e`)
Date: 2026-10-26 15:50 +0700 (`date`)
Plan: `report_agent/2026-10-25_ra_soat_code/sua_dot3_plan.md` bản 3 — `sha256sum` = `7c8c660558e5` (đúng bản A duyệt; file không đổi từ `76ff419`)
Implementation report: `report_agent/2026-10-25_ra_soat_code/sua_dot3_implementation.md` (trên `dot3`)
Canonical guide: `guides/full_corpus_rag.md` (mục "Build lại index")

## 1. Phạm vi đã review

- Nhánh `origin/dot3` = `dot3` = **`210abd4`**, 13 commit trên `71d2450` (12 commit code của plan §5 + 1 commit docs B-18 / report). Worktree riêng
  `/tmp/b_dot3` (detached), symlink chỉ đọc tới `data/`, `knowledge-base-hue/`; mọi lệnh `uv run --project /home/minhhieu/hue_rag` (`.venv` dự án); đã kiểm
  module nạp từ `/tmp/b_dot3/backend` (in `__file__`).
- Cổng tối thiểu: `git diff --name-status 71d2450..HEAD` (38 file: 5 xóa, 32 sửa, 1 thêm — report), `git diff --check` sạch, worktree sạch (chỉ 2 symlink
  của B). Đọc exact diff của mọi file code không bị xóa: pipeline (C-21), chunker (B-11, B-14), `markdown_blocks` (B-15), `points` / `upsert` (B-02), retrieval
  (C-06, `REPO_ROOT`), context (C-04), embedding (B-07), generator / prompt / recorder / smoke Phase 6 (C-05, C-10, C-19b), config (B-12, B-09, Rep B),
  test của C-17 / C-18 / B-20 / B-12, guide B-18. Không đọc `STATUS_C` (đúng `WORKFLOW.md` §9.1).

## 2. Findings

Không có blocker. Không có major.

| # | Mức | Vị trí | Yêu cầu | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|---|
| m-1 | minor | `sua_dot3_implementation.md` §2 dòng cuối | Report đúng số | Report ghi "39 file, +290 / −2.914". `git diff --shortstat`: `71d2450..8f0e5c4` (12 commit code) = **37 file, +289 / −2.711**; `71d2450..210abd4` = 38 file, +409 / −2.719. Số dòng code D7 thì **đúng** (B đếm lại: 8.345 → 6.218; test 4.394 → 4.182) | chỉ là số tóm tắt | sửa dòng đó theo `git diff --shortstat` (ghi rõ khoảng commit) |
| m-2 | minor | `data/ra_soat_code_2026-10-25/tools/dot3/d9.sh` (private) | `Session_Prompt.md` §10 — mọi Python bằng `uv run` | phần đọc lỗi notebook gọi `python3 -c` hệ thống; đường `/tmp/c42` và `/home/minhhieu/hue_rag/backend` cứng | không đổi kết quả (chỉ đọc JSON), nhưng là đúng loại bẫy B gặp 25/10 | đổi `python3` ⇒ `uv run python`; không cần chạy lại |
| m-3 | minor (ngoài phạm vi C — cho A) | `guides/phase_5_retrieval_profiles_reranking.md:65` (C đã ghi); `PROJECT_DOCUMENT_REGISTRY.md:227-228` (vẫn trỏ 2 converter `backend/scripts/`); `bao_cao_he_thong/BAO_CAO_CHIA_DOAN.md:49, 62, 130`, `BAO_CAO_NEN_TANG.md:45, 116`, `BAO_CAO_SINH_CAU_TRA_LOI_API.md:167` | tài liệu hiện hành khớp code (plan §8) | `git grep` tên đã gỡ trên `210abd4` | người đọc tìm file / hàm không còn | A sửa khi làm 4 chỗ báo cáo; registry: thêm dòng "lịch sử" hoặc sửa đường |

Kiểm riêng **sự cố `;` ở commit `3b5df01` (B-20)** (A dặn): diff commit chỉ thêm import, hằng đường build record, hàm đọc record, 2 assert identity / sparse bytes
và assert tập file — **0 dòng nội dung kho / Golden**. Quét `overlap_scan.py` trên dòng thêm của **từng** commit (13 file) và cả nhánh: **0 trùng**. Quét cả
file test chunker theo phiên bản: `9219adf` 10 dòng trùng kho ⇒ `3b5df01` đúng **10 dòng đó** (lệch +3 dòng do import thêm ở đầu file) ⇒ `5a99f99` và `HEAD`
**0** — khớp giải thích của C (mẫu test có sẵn từ trước, xử lý ở B-12). Các chuỗi này vẫn ở `main` hiện tại và lịch sử git (User: không xóa lịch sử).

Lệch plan đã khai (B kiểm, đồng ý): B-12 ngưỡng ≥ 10 ký tự + 7 đường file (chặt hơn plan; A chấp nhận 14:4x); C-21 assert `"target is non-empty"` (lý do dừng
thật); C-18 `monkeypatch.delenv("OPENAI_API_KEY", raising=False)` — đọc code: hai test `run_smoke_async(confirm_paid=True)` không còn đường tới lượt paid kể cả
khi chạy với `--env-file`; nhỏ hơn phương án "tách test", đúng chữ "hoặc" của plan. C-17: test `…no_last_chat_trace_after_chat` bỏ fixture key vẫn không tới
generator vì `context_limit` 2561 làm đoạn đầu vượt ngân sách (route dựng context **trước** khi kiểm generator — `api/routes/chat.py`). Schema artifact smoke
Phase 6 `v2` ⇒ `v3`: đúng hệ quả gỡ lượt Rep B.

Đọc diff, không thấy lỗi: C-21 `sparse_sha` vẫn được gán trước mọi chỗ dùng (`full_corpus_pipeline.py:189`, dùng ở record `:233`, `:250`); B-02 mọi phép kiểm bỏ khỏi
`build_full_corpus_point_batch` đều có trong `validate_full_corpus_point_inputs` (vector, trùng id, `validate_chunk_id`, point id, 7 field payload, sparse) mà
pipeline gọi một lần trước `create_full_corpus_collection` (`:196`); B-11 vòng kiểm cuối + `lru_cache` theo chuỗi (cache sống trong một lần `chunk_document`);
B-14 `emit()` giữ `chunk_id = <source>#<len(chunks)>` đúng thứ tự cũ; B-15 `nest_open == 2` chỉ lấy mục con trực tiếp; cờ `in_table` / `in_blockquote` luôn
`False` ở chỗ kiểm cũ ⇒ bỏ không đổi hành vi. Độ phức tạp: nhánh giảm 2.127 dòng code, không thêm abstraction mới ngoài `emit()` (thay 7 khối lặp).

## 3. Cách người kiểm chạy lại thật

Cwd `/tmp/b_dot3/backend`, `HF_HUB_OFFLINE=1`, `uv run --project /home/minhhieu/hue_rag …`:

- D1: `python …/tools/dot3/d1_chunks.py` (chunker production, kho thật).
- D2: `python -m evaluation.full_corpus_eval retrieval --out /tmp/b_rev/t1.jsonl` (Qdrant `:6335` chỉ đọc, e5 CPU).
- D3: `env -u OPENAI_API_KEY python -I …/tools/sua_3/snap_3b.py` trên `dot3` **và** trên `main` (`/tmp/b_main` @ `13afcf2`, backend = `71d2450`) — mốc độc lập
  thay vì chỉ dùng `3b_base.json` của C.
- D4: 15 file `tests/test_*.py` (trừ `test_startup_model_missing.py`), `env -u OPENAI_API_KEY python -m pytest <liệt kê file> -q -p no:cacheprovider -rfE --durations=5`.
- D5: `--env-file /home/minhhieu/hue_rag/.env python -I /tmp/b_rev/gate.py` (bản sao `dot3/gate.py`, port **8012** để không đụng C): uvicorn thật, `/`, `/health`,
  1 câu trong kho + 1 câu ngoài kho tự viết, log, tắt server.
- D6: `git grep` các tên / lệnh đã gỡ (module, hàm, lớp, hằng, lệnh CLI, marker `live`, `"minilm"`, đường file conditions cũ) trên `210abd4` (trừ `docs/`, `reports/`, `handoff_prompt/`, `report_agent/`, nhật ký, history) + `git grep` trên `p82-b1`
  (`backend/experiments/`); kiểm nguồn `REPO_ROOT` mà harness 8.1 import.
- D7: đếm dòng `.py` tracked `backend/` (trừ `tests/`, `experiments/`) bằng `git show` tại `71d2450` và `HEAD`.
- D8: `git ls-files knowledge-base-hue`; `overlap_scan.py` (cửa sổ 40) trên dòng thêm từng commit; bản sao `b12_scan_all.py` (literal ≥ 20 ký tự) trỏ cây `dot3`
  và cây `main` (đối chứng).
- D9: `--help` 3 CLI + 5 harness 8.1, import `g5_by_category`.

## 4. Kết quả quan sát

| # | Tiêu chí | Kết quả B (lần chạy mới) | |
|---|---|---|---|
| D1 | 8.459 đoạn, 0 lỗi, sha `60591acff422ece6`, identity = record | **8.459 / 0 / `60591acff422ece6` / identity True**, 22,2 s | PASS |
| D2 | T1 158 dòng sha `cefb2d1ad609` | **158 dòng, `cefb2d1ad609`** | PASS |
| D3 | chuỗi gửi model 25 câu giống byte | `dot3` = `3b_base.json` (`932602c35b9f`) **và** = bản chạy trên `main` (`cmp` giống byte) | PASS |
| D4 | đạt; error key giảm đúng 3 | **197 passed · 1 failed · 4 error** — đúng phần cần key (`test_openai_api_key_exists_without_leaking`; 4 error `require_openai_key`) = report | PASS |
| D5 | cổng ổn định | `/` 200; `/health` 200, 5 / 5 ready; câu trong kho 200, `[1, 3]` = `sources [1, 3]`, 3,3 s; câu ngoài kho từ chối đúng, 1,5 s; log 0 `ERROR` / Traceback; logger `api` ra log (B-09) | PASS |
| D6 | 0 nơi gọi | 0 trong code / test / notebook / harness 8.1 trên `dot3`; 0 trong `p82-b1:backend/experiments/`; `REPO_ROOT` harness lấy từ `evaluation.full_corpus_eval` (còn) | PASS |
| D7 | số dòng | code **8.345 → 6.218**; test **4.394 → 4.182** (= report). Phần giảm (`git diff --numstat`, net): converter −967, smoke Phase 5 −524, `preview.py` −245, Rep B (module + prompt + generator + smoke Phase 6 + config) ≈ −150, `retrieval/full_corpus.py` −66, chunker −64, `full_corpus_eval.py` −43, `source_state.py` −34, còn lại nhỏ — mọi tên đã gỡ đều 0 nơi gọi (D6) | PASS |
| D8 | public | `git ls-files knowledge-base-hue` = **0**; literal ≥ 20 ký tự trùng kho: `dot3` **0** (đối chứng `main`: 131 chuỗi ở 3 file — converter 94, test chunker 37); `overlap_scan` dòng thêm 0; file conditions sha `b84a0a637bfc` = bản ở `71d2450` = `meta/`, có backup `meta/backup_b12_2026-10-26/` | PASS |
| D9 | điểm vào | 8 / 8 `--help` 0 lỗi, `g5` import được; **3 notebook Run All: NOT RUN bởi B** (auto mode chặn lệnh `jupyter nbconvert --execute`) | PARTIAL |

**Tiền:** D5 2 lượt `gpt-6-luna` ≈ **0,0004 USD (ước — route không ghi usage)**, trong trần A cho (≤ 0,0005). Mọi kiểm khác 0 USD.

## 5. Giới hạn hoặc phần chưa chạy

- **Notebook 03 / 04 / 06 Run All** (D9): B không chạy lại (auto mode chặn) ⇒ dựa bằng chứng C (report §4: 0 lỗi sau C6, C7, C8, C11, cuối đợt). Rủi ro thấp:
  B-07 / B-02 / C-05 đã được D1–D5 phủ trên đường production. Nếu A / User muốn bằng chứng của B: User chạy ở terminal B
  `! cd /tmp/b_dot3 && for nb in 03_embedding_models 04_qdrant_ingestion 06_generation_and_api; do env -u OPENAI_API_KEY HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag jupyter nbconvert --to notebook --execute notebooks/$nb.ipynb --output-dir /tmp/b_rev/run; done`.
- **T-C** (`test_startup_model_missing.py`) cuối đợt: chờ User ở terminal C; B không chạy (cùng lý do auto mode). Commit 7–12 không đụng builder retrieval ⇒ kết quả sau C6 (1 passed) là bằng chứng chính, như report ghi.
- B-02 so 8.459 `PointStruct` (C: giống byte): B **không** chạy lại (~3,5 phút e5 CPU) — đọc diff thấy chỉ bỏ kiểm, không đổi phần dựng điểm; D1 (identity) + D2 (T1) đạt.
- B-12 `b12_move_samples.py` round-trip: không chạy lại; B kiểm thay bằng D8 (0 chuỗi) + D4 (7 test mẫu đạt khi có file `meta/`).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Mọi tiêu chí D1–D8 đạt bằng lần chạy mới của B; D9 PARTIAL (notebook theo bằng chứng C). Ba minor không chặn: C sửa m-1
(một dòng report), m-2 (script private); A làm m-3 cùng 4 chỗ `bao_cao_he_thong/` + `Project_Status.md` (plan §8).

Cho A khi merge:
1. `main` đã có `13afcf2` (chỉ `report_agent/2026-10-26_cai_tien_tung_khau/…` + `STATUS_B.md`, không chồng file với `dot3`) ⇒ fast-forward không được; C rebase
   lại (sạch) hoặc A merge. Sau rebase chỉ commit docs đổi sha — D1–D5 không cần chạy lại (backend không đổi; ghi là dùng lại).
2. **`p82-b1` sẽ xung đột thêm** khi rebase: `settings.yaml` / `settings_loader.py` / `test_phase6_settings.py` (gỡ Rep B), `retrieval/full_corpus.py` (gỡ
   `minilm`, `REPO_ROOT`) — ngoài phần đã ghi ở `sua_1b_plan.md` §6. B là người làm B1 ⇒ B xử lý khi 8.2 chạy lại.
3. **Ngoài phạm vi đợt 3, cần A / User quyết:** 5 file JSON lịch sử đang tracked ở `reports/artifacts/` có dòng trùng nguyên văn kho theo `overlap_scan`
   (cửa sổ 40 ký tự): `full_corpus_chunk_samples_2026_09_09.json` 265 dòng, `full_corpus_parser_locator_samples_2026_09_09.json` 122,
   `full_corpus_vn_qt_token_check_2026_09_09.json` 20, `full_corpus_rag_wave_1_preview_2026_09_11.json` 6, `full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json` 5.
   (`evaluation/results/*`, 2 JSON `phase_4_5`, 2 preflight còn lại: 0.) D8 của plan chỉ quét `.py` / notebook nên không thấy. User 19:4x: "nội dung kho ra khỏi
   file tracked từ giờ, không xóa lịch sử git" — gỡ khỏi `HEAD` (cp ra `data/` + `git rm`, như B-13) có thuộc ý đó không là quyết định của User.
4. Quan sát, không phải finding: tên test / docstring mẫu chunker vẫn nêu tên một số mục trong kho (tên quán, tên di tích) — không phải nguyên văn, 0 chuỗi
   ≥ 20 ký tự trùng.

Việc rủi ro trung bình (Phase đã duyệt, gỡ theo luật User) ⇒ A đóng và báo User ("5 gói xong") sau khi merge + cổng ổn định trên `main`.
