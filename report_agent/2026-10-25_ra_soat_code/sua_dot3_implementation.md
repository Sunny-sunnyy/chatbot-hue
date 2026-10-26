# Implementation Report: rà code — đợt 3 (gói 2 + gói 5 + B-12)

Người làm: C (Claude Opus 5.5; commit 1–3 phiên tối 25/10 terminal `hue-rag-7f`, commit 4–12 + docs phiên 26/10 terminal `hue-rag-87`)
Date: 2026-10-26 15:33
Plan: `report_agent/2026-10-25_ra_soat_code/sua_dot3_plan.md` bản 3 sha `7c8c660558e5` (A duyệt 21:53 25/10; review `sua_dot3_plan_review.md`)
Nhánh: `dot3` (rebase lên `main` `71d2450` đầu phiên 26/10, push `--force-with-lease`); người review: B (worktree riêng `/tmp/b_dot3`).
Guide đổi: `guides/full_corpus_rag.md` (mục "Build lại index", dòng CLI evaluator), `guides/phase_6_generation_api.md`; notebook 06 ô 0 (chữ).

## 1. Phạm vi

Làm đủ 12 commit của plan §5 + commit docs B-18. Không build index, không ghi Qdrant, không đổi chất lượng: mọi mục cho đầu ra
giống hệt trên kho hôm nay (trừ B-11 / B-15 — đổi hành vi cho đầu vào mà kho hôm nay không có). Không đụng harness 8.1 / nhánh `p82-b1`.

## 2. Thay đổi chính (theo commit; sha sau rebase)

| # | Commit | Mục | Thay đổi |
|---:|---|---|---|
| 1 | `3a37af4` | C-21 | `build_candidate` ghi sparse state chung **sau** bước kiểm đích; test đỏ → xanh (assert `QdrantSchemaError` + `"target is non-empty"` — lý do dừng thật, lệch thông điệp plan m-4) |
| 2 | `3f29f07` | B-11 | `chunk_document` báo `"Chunk exceeds tokenizer limit: <id>"` ở một vòng kiểm cuối cho mọi nhánh phát đoạn; nhớ kết quả kiểm token (`lru_cache`) để không đếm hai lần |
| 3 | `9219adf` | B-04 | gỡ CLI preview (`generate_preview`, `partition_for_source`, `main`), giữ 3 hàm tokenizer tại chỗ; cắt phần preview của test determinism (m-3) |
| 4 | `3b5df01` | B-20 | test determinism so thêm `compute_corpus_identity` = build record và sparse state tính lại = file runtime từng byte; test discovery so tập file với `record["corpus"]["sources"]` (bỏ ghim 205 / số file từng domain) |
| 5 | `5a99f99` | B-12 | `full_corpus_conditions.json` ⇒ `knowledge-base-hue/meta/` (`cp` + `git rm`); 7 test mẫu chunker đọc chuỗi kỳ vọng từ `meta/chunker_acceptance_samples.json` (private, không `git add`) |
| 6 | `717ef83` | C-19a, C-06 | gỡ `retrieval/full_corpus_smoke.py` + 3 test; nhánh `minilm` trong `search` / builder, tham số `reranker_instance` và import `CrossEncoderReranker` của service (dư sau gỡ); `RerankerMode = Literal["none"]` |
| 7 | `c6e130c` | C-05, C-19b, C-10 | gỡ Representation B (module, prompt, agent / output / tham số generator, setting + loader + test); smoke Phase 6 còn 4 câu (đánh số 1–4, `exact_four_attempts`, schema artifact v3), `make_fits_all_checker`; recorder bỏ `record_generation_success`, `packed_text`; chữ notebook 06, guide 6 |
| 8 | `9f7ad43` | C-04, C-07, B-05, B-07, B-06, B-09, `REPO_ROOT` | gỡ nhánh `apply_chat_template` + 2 test không thể đỏ; `parse_user_scores` + lệnh `parse-user-scores` + test + dòng guide; `verify_build_record_freshness`; dense runner chỉ CPU float32; `FULL_CORPUS_BATCH_SIZE` một nơi; `REPO_ROOT` thừa; tên docker-compose; logger `api` trong `logging.yaml`; guide 6 "Giới hạn đã biết" khớp `1e4acd0` (A dặn 14:5x) |
| 9 | `44f0f80` | C-17, C-18 | gỡ `require_openai_key` ở 3 test dừng trước generator; gỡ marker `live`; 2 test `run_smoke_async(confirm_paid=True)` thêm `monkeypatch.delenv("OPENAI_API_KEY")`; bỏ assert trên list rỗng cục bộ |
| 10 | `cd7c936` | B-14, B-15 | `chunk_document`: một hàm `emit()` thay 7 khối `FullCorpusChunk(...)` (bỏ `chunk_ordinal` — luôn = `len(chunks)`), bỏ 4 kiểm `is not None` luôn đúng, 2 import thừa, chữ "Wave 1"; `markdown_blocks`: bỏ cờ `in_table` / `in_blockquote` (bật-tắt trong cùng nhánh), mục con lấy **trực tiếp** (`nest_open == 2`) + test 3 cấp |
| 11 | `e77c26f` | B-02 | `build_full_corpus_point_batch` chỉ kiểm lô 1..64 rồi dựng `PointStruct`; mọi kiểm đầu vào đã có ở `validate_full_corpus_point_inputs` (pipeline gọi một lần trước khi tạo collection); bỏ tham số `dimension` (dư) |
| 12 | `8f0e5c4` | B-13 | 2 converter HueGov ⇒ `data/tools/huegov_converters/` (private, sha bằng nhau) rồi `git rm` |
| — | (commit docs) | B-18 | `guides/full_corpus_rag.md` mục "Build lại index": C-21 / B-11 / B-02 / B-12 theo code mới, bỏ cảnh báo "build ghi sparse state trước bước kiểm đích" |

12 commit code `71d2450..8f0e5c4`: 37 file, +289 / −2.711 dòng (`git diff --shortstat`; sửa số cũ theo m-1 review B). Code `backend/` (trừ tests, experiments): **8.345 → 6.218** dòng; tests 4.394 → 4.182.

## 3. Cách đã chạy thật

Script đo (private) ở `data/ra_soat_code_2026-10-25/tools/dot3/`, cwd `backend/`, `HF_HUB_OFFLINE=1`; ghi chép từng bước `notes_26_10.md`.

- D1 `uv run python …/dot3/d1_chunks.py` — `chunk_full_corpus()` thật ⇒ số đoạn, lỗi, sha danh sách `[chunk_id, search_text, evidence_parts]`, identity = record.
- D2 `uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/c42/t1.jsonl` (Qdrant chỉ đọc, e5 CPU).
- D3 `uv run python -I …/sua_3/snap_3b.py <out>` — chuỗi gửi model + token context 25 câu tự viết, generator thật, không gọi mạng; so `dot3/3b_base.json`.
- D4 `bash …/dot3/d4_tests.sh` — 15 file `tests/test_*.py` (trừ `test_startup_model_missing.py`), `env -u OPENAI_API_KEY`, liệt kê file.
- D5 `uv run --env-file ../.env python -I …/dot3/gate.py` — uvicorn thật cổng 8011: `/`, `/health`, 1 câu trong kho + 1 câu ngoài kho tự viết, log, tắt.
- D6 `…/dot3_plan/usage.py HEAD <tên…>` (git grep commit) + grep tài liệu hiện hành; D7 `dot3/d7_lines.sh`; D8 `git ls-files knowledge-base-hue` + `kiem_cheo_C/b12_scan_all.py`.
- D9 `bash …/dot3/d9.sh nb` — `--help` 3 CLI + 5 harness 8.1, import g5, Run All notebook 03 / 04 / 06 ra `/tmp/c42/run` (md5 file repo không đổi).
- B-12: `dot3/b12_move_samples.py` (AST: thay literal ≥ 10 ký tự có nguyên văn kho + đường `rel` bằng `S[i]`; kiểm ngược thay lại ⇒ đúng file gốc từng byte).
- B-02: `dot3/b02_points.py` — e5 thật CPU mã hóa 8.459 đoạn **một lần** (201,6 s, `/tmp/c42/dense.npy`), dựng toàn bộ `PointStruct` bằng code trước / sau từ cùng ma trận, so byte. Không ghi Qdrant.
- T-C `test_startup_model_missing.py`: User chạy `!` ở terminal C (auto mode chặn `HF_HOME` rỗng).
- 2 test có key, không gọi mạng (A cho 14:5x, chọn đúng node id): `uv run --env-file ../.env python -m pytest "tests/test_openai_full_corpus_generator.py::test_real_environment_builds_openai_generator" "…::test_empty_or_blank_input_rejected_before_network"`.

## 4. Kết quả quan sát

**Mốc trước khi sửa tiếp (26/10, trên `9219adf` sau rebase):** D1 8.459 đoạn / 0 lỗi / sha `60591acff422ece6` / identity = record; D2 158 dòng sha `cefb2d1ad609` — tái lập đúng mốc 25/10.

| Commit | D1 | D2 T1 | D3 | D4 (không key) | D5 | D9 | Riêng |
|---|---|---|---|---|---|---|---|
| 1–3 (25/10) | giống | giống | giống (C1) | 199→201→200 p / 1 f / 7 e | đạt (C2) | — | xem `STATUS_C` 25/10 |
| 4 | — | — | — | 200 / 1 / 7 | — | — | biết đỏ: bỏ 1 đoạn ⇒ identity, sparse bytes False; bỏ 1 file ⇒ discovery False |
| 5 | giống | giống | — | 200 / 1 / 7 | **đạt** | — | conditions sha `b84a0a637bfc` gốc = backup = mới; 55 chuỗi (round-trip True); biết đỏ: sửa 1 chuỗi ⇒ test đó đỏ (2 lần); thiếu file ⇒ 7 test mẫu `FileNotFoundError` có tên file, 36 đạt; D8 `ls-files kb` 0, test chunker 0 chuỗi |
| 6 | — | giống | — | 197 / 1 / 7 (−3 test smoke) | — | 0 lỗi | T-C (User `!`) **1 passed** 14,96 s |
| 7 | — | — | **giống byte** `932602c35b9f` | 195 / 1 / 7 (−2 test Rep B) | **đạt** | 0 lỗi | 2 test có key: 2 passed 2,69 s |
| 8 | — | giống | giống byte | 193 / 1 / 7 (−2) | **đạt** | 0 lỗi | `--help` 10 lệnh = guide; dòng log `api` ra console + file |
| 9 | — | — | — | **196 / 1 / 4** (error giảm đúng 3) | — | — | 3 test vừa gỡ fixture chạy không key: 3 passed |
| 10 | **giống** (25,2 s) | giống | — | 197 / 1 / 4 (+1 test 3 cấp) | — | — | test 3 cấp đỏ trước sửa (3 mục con ≠ 2), xanh sau |
| 11 | — | — | — | 197 / 1 / 4 | **đạt** | 0 lỗi | **8.459 `PointStruct` giống byte** (`c7466bd83bd3`, dense `08a90dbfd7ba`) |
| 12 | — | — | — | — | — | — | sha converter bằng nhau (`fd4dc5c4261d`, `50eb800c7b92`); D8 toàn repo 0 chuỗi |
| **Cuối đợt** (`8f0e5c4`) | 8.459 / 0 / `60591acff422ece6` / identity True / 23,0 s | 158 / `cefb2d1ad609` | giống byte | 197 / 1 / 4 | **đạt** (5 / 5 ready, [1, 3] = sources, từ chối đúng, log 0 lỗi) | 0 lỗi | 2 test có key 2 passed; D6 0 nơi gọi; D8 0 / 0; `git diff --check main..dot3` sạch; T-C cuối đợt: xem §5 |

D4 còn lại đúng phần cần key (theo thiết kế): `test_phase6_settings.py::test_openai_api_key_exists_without_leaking` (failed) + 4 error
`require_openai_key` (`test_health_is_cached…`, 2 test generator — đã chạy có key: passed, `test_async_client_with_lifespan…`).

D7 (code / tests): `76ff419` 8.345 / 4.394 · C1 8.347 · C2 8.354 · C3 8.109 · C6 7.521 · C7 7.373 · C8 7.273 · C10 7.196 · **C12 6.218 / 4.182**.

**Tiền:** paid chỉ ở D5 — 5 lượt × 2 câu `gpt-6-luna` phiên 26/10 (sau C5, C7, C8, C11, cuối đợt) + 1 lượt 25/10 (C2); route không ghi usage ⇒
**ước** ~0,0002 USD / câu ⇒ ~0,0024 USD cả đợt (trần 0,003). 2 test có key: 0 USD (không gọi mạng). Không gọi OpenRouter.

## 5. Lỗi, lệch plan và giới hạn

- **T-C cuối đợt:** cần User chạy `!` lần hai sau commit 12 (plan D4) — điền kết quả khi có; commit 7–12 không đụng `retrieval/full_corpus.py`
  builder (C8 chỉ gỡ `REPO_ROOT`, C11 đụng `points.py`) nên kết quả sau C6 là bằng chứng chính.
- **Lệch plan (chặt hơn, A chấp nhận 14:4x):** B-12 chuyển literal ≥ **10** ký tự có nguyên văn kho **và** 7 đường file `rel` (plan: ≥ 20) — `overlap_scan`
  cờ một đường file 67 ký tự. Số đoạn trong JSON: 55.
- **Lệch plan nhỏ khác:** C-21 assert `"target is non-empty"` (ghi 25/10); C-06 test trace riêng tư đổi `"minilm"` ⇒ `"none"` (plan chỉ ghi smoke dựng
  service `minilm`); C-18 chọn `delenv OPENAI_API_KEY` thay vì "tách test health / `confirm_paid=False`" (plan ghi "hoặc"): nhỏ nhất, giữ đúng test,
  chặn đường paid cả khi chạy với `--env-file`; C8 thêm gỡ `import re` (evaluator) và `import sys` (test context) do sửa làm dư; C11 bỏ tham số
  `dimension` (dư sau khi bỏ kiểm ma trận); smoke Phase 6 đổi schema artifact `v2` ⇒ `v3` (bỏ lượt Rep B).
- **Sự cố quy trình (C4):** C nối `overlap_scan` với `git commit` bằng `;` ⇒ commit chạy dù scan exit 1. 10 dòng bị cờ là test mẫu có sẵn từ trước
  (đã xử lý ở C5); diff C4 không thêm chuỗi kho (dòng thêm dài nhất 114 ký tự, đều là code / comment). A nhờ B kiểm riêng diff `3b5df01`. Từ C5:
  quét riêng, xem kết quả, rồi mới `git add` / commit.
- **Giữ (theo plan):** `CrossEncoderReranker` (harness g1 / g4_rerank); `ConditionManager` hai lượt kiểm; `ListItemInfo.parent_*`; kiểm lát cắt sau dựng;
  `upsert.py` kiểm sau upsert; nhánh `native_hybrid_rrf`. Nhánh `pass` cho `bullet_list_open` trong vòng gom mục con (vô hại) — để nguyên.
- **Ngoài phạm vi, cho A:** `guides/phase_5_retrieval_profiles_reranking.md:65` vẫn nói "Reranker tùy chọn trong code: MiniLM" — sau C6 service không còn
  nhánh này; `bao_cao_he_thong/` theo plan §8 (B-11 "build dừng khi đoạn vượt", Rep B khỏi `BAO_CAO_CHIA_DOAN.md:136`, smoke Phase 5 trong
  `BAO_CAO_NEN_TANG.md:116`, conditions file chuyển chỗ ở `BAO_CAO_CHIA_DOAN.md:49, 62, 130`); `Project_Status.md` §4 / §8. `guides/full_corpus_rag.md`
  bước 4b còn "cutover cần sửa code (B-06)" — mã B-06 của B26 khác B-06 của plan này, C không đổi.
- Clone public: test chunker mẫu + `load_settings()` cần file trong `knowledge-base-hue/meta/` — như trước B-12 (đã cần kho), không xấu hơn; A quyết không thêm fixture.
- `backend/scripts/__pycache__/` (untracked, bị ignore) còn trên đĩa — không ảnh hưởng.

## 6. Bàn giao cho người kiểm (B)

- Đọc: plan §2–§6, report này, `git log main..dot3` từng commit. Trọng tâm: D1 sha `60591acff422ece6`, D2 `cefb2d1ad609`, D3 25 câu giống byte
  (`3b_base.json` sha `932602c35b9f`), D8 `git ls-files knowledge-base-hue` rỗng + quét chuỗi, diff `3b5df01` (sự cố C4), B-02 so `PointStruct`.
- Chạy lại: script ở `data/ra_soat_code_2026-10-25/tools/dot3/` (sửa đường `/tmp/c42` nếu chạy chỗ khác); `b02_points.py` cần ~3,5 phút e5 CPU nếu
  không có `dense.npy`; `b12_move_samples.py` chạy trên bản `git show 9219adf:backend/tests/test_full_corpus_chunker.py` để kiểm ánh xạ (round-trip).
- File private mới: `knowledge-base-hue/meta/{full_corpus_conditions.json, chunker_acceptance_samples.json (sha 3013c24fd8f4), backup_b12_2026-10-26/}`,
  `data/tools/huegov_converters/`.
- T-C: User `!` ở terminal B nếu B cần tự chạy lại.
