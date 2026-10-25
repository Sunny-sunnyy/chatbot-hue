# STATUS C — cập nhật 2026-10-25 22:29 (KẾT PHIÊN tối 25/10; đợt 3 DỞ — 3 / 12 commit trên nhánh `dot3`)

Terminal: `hue-rag-7f` (mở 18:2x 25/10; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi.
User 25/10: C làm việc và báo cáo trực tiếp cho A; việc A giao = "làm đi"; xong báo cáo, nhắn A, chờ việc. User 18:3x: rà code chỉ đề xuất; User 19:4x duyệt 5 gói sửa.

## Phiên sau C làm gì đầu tiên

1. `git switch dot3` (đã push, `origin/dot3` = **`5e237bb`**, nền `main` `76ff419`); kiểm `git log --oneline main..dot3` = 3 commit; chạy lại mốc nhanh (D1 sha đoạn
   `60591acff422ece6`, D2 T1 `cefb2d1ad609`) trước khi sửa tiếp — script ở **`data/ra_soat_code_2026-10-25/tools/dot3/`** (chép từ `/tmp/c42/`; sửa đường `/tmp/c42` trong `.sh`).
2. Làm tiếp **commit 4 (B-20)** theo plan `report_agent/2026-10-25_ra_soat_code/sua_dot3_plan.md` (sha `7c8c660558e5`, A duyệt 21:53) — dùng
   `embedding/sparse.py` `serialize_sparse_state(fit_sparse_state(chunks))` so byte với `data/full_corpus_builds/full_corpus_sparse_state.json`; `compute_corpus_identity`
   = record; discovery `set(files) == set(record["corpus"]["sources"])`. Rồi 5 → 12, cổng D theo plan; report `sua_dot3_implementation.md` commit trên `dot3`.
3. Không commit `main`, không merge (A merge sau khi B review cả nhánh).

## Đợt 3 — trạng thái từng commit (nhánh `dot3`)

| # | Commit | Mục | Cổng D đã chạy |
|---:|---|---|---|
| 1 | `4f8c71c` | C-21 ghi sparse state sau kiểm đích + test (đỏ → xanh) | D2 T1 `cefb2d1ad609`; D3 25 câu giống byte; D4 199 passed / 1 failed / 7 error (C-17) |
| 2 | `749459d` | B-11 chunker báo lỗi đoạn vượt token (+ cache kết quả kiểm mỗi tài liệu) + 3 test `chunk_document` thật | D1 8.459 / 0 lỗi / sha `60591acff422ece6` / identity = record; thời gian chia 23,8 s (mốc 25,7; không cache 50,7); D2; D4 201 passed; **D5 cổng ổn định** đạt (5 / 5 ready, [1, 3] = sources, từ chối đúng, log 0 lỗi) |
| 3 | `5e237bb` | B-04 gỡ CLI preview (giữ 3 hàm tokenizer), test lỗi condition gọi `chunk_full_corpus`, bỏ test file tĩnh + phần preview của test determinism (m-3) | D1 sha giống; D2; D4 200 passed (−1 test file tĩnh), 96 s (mốc 150 s); D6 `generate_preview` / `partition_for_source` = 0 |
| 4–12 | — | B-20; B-12 (`cp` + `git rm`, sao lưu + sha); C-19a + C-06; C-05 + C-19b + C-10; C-04 / C-07 / B-05 / B-07 / B-06 / B-09 / `REPO_ROOT`; C-17 / C-18; B-14 / B-15; B-02; B-13; docs B-18 | **chưa làm** |

**Mốc đo trước đợt (`76ff419`):** D1 8.459 đoạn, 0 lỗi, sha `60591acff422ece6`, 25,7 s · D2 T1 `cefb2d1ad609` (158 dòng) · D3 = `3b_before.json` gói 3 · D4 15 file
198 passed / 1 failed / 7 error · D7 code `backend/` (trừ tests, experiments) **8.345** dòng, tests 4.394 · D8 `git ls-files knowledge-base-hue` 0; chuỗi kho: 2 converter
(54 / 40 chuỗi), test chunker 37 chuỗi.

**Lệch plan đã gặp (ghi vào report đợt 3):** test C-21 — plan (m-4) ghi assert `"Target collection already exists"`, nhưng `require_fresh_full_corpus_target` ném
`QdrantSchemaError("target is non-empty: …")` **trước** dòng đó ⇒ test assert `QdrantSchemaError` + `"target is non-empty"` (lý do dừng thật). Không đổi hướng plan.

**Script đo — đã chép sang `data/ra_soat_code_2026-10-25/tools/dot3/` (22:3x, A dặn; gồm mốc `t1_base.jsonl`, `3b_base.json`; chạy `d4_tests.sh` / `d9.sh` / `d8.sh` như cũ — các file `.sh` vẫn gọi `/tmp/c42/…` ⇒ sửa đường dẫn sang thư mục mới trước khi chạy):** `d1_chunks.py` (cwd `backend/`: `chunk_full_corpus()` ⇒ số đoạn, lỗi, sha256 của danh sách
`[chunk_id, search_text, [[role,start,end,text]…]]`, `compute_corpus_identity` = record, giây); `d4_tests.sh` (15 file `tests/test_*.py` trừ `test_startup_model_missing.py`,
`env -u OPENAI_API_KEY HF_HUB_OFFLINE=1 … pytest -q -p no:cacheprovider -rfE`); `d9.sh` (`--help` 3 CLI + 5 harness, import g5; tùy chọn Run All 3 notebook ra `/tmp`);
`d8.sh` (`git ls-files knowledge-base-hue` + `tools/kiem_cheo_C/b12_scan_all.py`). Còn giữ (private): `data/ra_soat_code_2026-10-25/tools/sua_3/{snap_3b.py,gate.py}`
(D3, D5), `tools/dot3_plan/usage.py` (D6 — **đọc HEAD đã commit**, chạy sau commit).

## Việc đã xong phiên tối 25/10 (chi tiết trong report; đã commit trên `main` trừ khi ghi khác)

- C34 rà code luồng trả lời + đánh giá (`ra_soat_code_C.md`, 18 finding); kiểm chéo B25 (`kiem_cheo_C.md`); review B26 (`sua_4_review.md`); review plan 1b
  (`sua_1b_plan_review.md`) + review gói 1b (`sua_1b_review.md`, ready); C35 gói 1a citation `[Nguồn n]` (`9e6d371`); gói 3a / 3b `paired_stats` + `build_answer_input`
  (`47a4e32`); 3c phần free citation v2 (`sua_3c_citation_v2.md`, `data/ra_soat_code_2026-10-25/citation_v2/`); danh sách ứng viên (`ung_vien_cai_tien_C.md`); plan đợt 3
  (`sua_dot3_plan.md` bản 3).
- Còn treo từ trước: **C33 plan E1** (`phase_8_2_e1_plan.md` sha `f86240418ca1`) phải sửa khi 8.2 chạy lại — dùng `paired_stats` + `false_refusal` (C-02 / gói 3a), số
  citation theo v2 ⇒ sha mới. C32 rà kho: hồ sơ, chờ User.
- **C chưa đọc nội dung câu kín** (md5 `ddc59587b502`, manifest `9ea480d0d083`).

## Câu hỏi cho A / User

- 3c: xin lượt xác nhận reasoning `none` trên test (~0,007 USD ở context 5) — A đưa vào tài liệu thiết kế đợt cải tiến (A 20:5x).
- C32: `performing_arts/performing-arts-entities-inventory.md` tự ghi phải loại khỏi ingestion nhưng đang trong index — loại ở lần build lại?
- E1 plan Q1–Q3 (§10 plan) — khi 8.2 chạy lại.

## File private C tạo phiên này (không commit)

- `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `brief_common.md`, `nguon_count.py`, `cite_shapes.py`, `recheck_both.py`,
  `c01_probe_*.py`; thư mục `kiem_cheo_C/`, `review_4/`, `review_1b_plan/`, `review_1b/`, `sua_1a/`, `sua_3/`, `citation_v2/`, `dot3_plan/`); `data/ra_soat_code_2026-10-25/citation_v2/`.
- Trước đó: `data/ra_soat_kho_2026-10-25/` (C32), `data/phase_8_2/e1_plan/` (C33).
- Tạm: `/tmp/c34`, `/tmp/c34x`, `/tmp/c35`–`/tmp/c42` (mất khi tắt máy; không nội dung private ngoài số đếm).

## Ý cải tiến (A xin danh sách sau 5 gói — chỉ là ý, chưa thử; bản đầy đủ `ung_vien_cai_tien_C.md`)

- **Route API ghi usage (token, latency, số nguồn) mỗi câu vào log** — cổng ổn định gói 3 / 1b / đợt 3 đều phải **ước** tiền; không ghi nội dung câu hỏi.
- **Nhãn context `[Nguồn n]` ↔ prompt `[n]`** (C-09): thử khớp nhãn — thí nghiệm, đo lỗi "không ngoặc số" (14 / 1.600) + Completeness.
- **14 câu "không có ngoặc số"** còn lại sau 1a đều ở context 5 nguồn — xem có phải câu liệt kê / một ý.
- **Bộ đếm token context nhận instructions** khi harness đổi prompt (C-03 phần 2) — khi 8.2 E1 cần.
- **Kiểm token mỗi đoạn tốn gấp đôi thời gian chia nếu không nhớ kết quả** (đợt 3 commit 2) — đã cache; nếu sau này đổi chunker, đo lại thời gian.

## Đã học / bẫy gặp (đầu vào vòng cải tiến)

- **Plan ghi thông điệp lỗi phải đối chiếu đúng dòng ném đầu tiên** (đợt 3 commit 1: plan m-4 ghi `"Target collection already exists"`, thực tế
  `require_fresh_full_corpus_target` ném trước với `"target is non-empty"`) ⇒ khi viết test "đúng lý do", chạy thử một lần để thấy thông điệp thật trước khi ghi vào plan.
- **Thêm một phép kiểm vào vòng lặp nóng: đo thời gian trước / sau** (B-11 gấp đôi thời gian chia đoạn cho tới khi cache) — plan có ghi "đo giây" nên thấy ngay.
- **`git mv` sang thư mục bị gitignore vẫn đưa file vào index** (B tìm, M-1 plan đợt 3) ⇒ chuyển dữ liệu sang chỗ private bằng `cp` + `git rm`, kiểm `git ls-files`.
- **Script đo đọc `HEAD` chỉ đúng sau khi commit** (`usage.py` dùng `git grep <rev>`): D6 chạy sau commit, hoặc grep working tree.
- **Lệnh với `HF_HOME` rỗng bị auto mode chặn** trong session C (và B) ⇒ test kiểu đó để User chạy `!` (WORKFLOW §3.6), ghi rõ "dùng lại kết quả User" khi review.
- **Chỉ số lỗi do validator đếm: phân loại theo hình dạng output trước khi kết luận nguyên nhân** (C-09: 8.1 ghi "model quên `[n]`", thực tế viết `[Nguồn n]`).
- **Đọc đúng tài liệu trước khi phản biện** (sua_4 m3: C đọc nhầm plan G3, B đúng — H1 mới là bước bỏ huydang).
- **Import hai kiểu (`backend.X` / `X`) tạo hai bản module** ⇒ `except` / `isinstance` hụt — đã sửa ở gói 1b (quy ước import trần, chạy từ `backend/`).
- **Hàm so cặp của harness 8.1 không đổi dấu cho chỉ số "càng thấp càng tốt"** — từ gói 3a dùng `paired_stats` với tên `false_refusal`.
- `grep` ở máy là ugrep: regex dài báo "exceeds complexity limits" ⇒ tách ngắn hoặc dùng Python.
- Giữ từ trước: repo public (không chép nội dung kho / Golden / câu kín / dự án khác vào file tracked); giờ lấy bằng `date`; không báo "đã xong" trước khi lệnh ghi
  file trả kết quả; đọc tin mới trước bước đo / thay đổi; chạy GPU phải được A ghi rõ.

## Tiền

Paid API C phiên tối 25/10: **≈ 0,0016 USD** — đo: 0,000427 (C35, 2 lượt `gpt-6-luna`); ước (route không log usage): 3 lượt cổng ổn định × 2 câu × ~0,0002
(gói 3, review 1b, đợt 3 commit 2) ≈ 0,0012. Trần chung gói 1–5: 0,05 USD; đợt 3: ≤ 0,003 (đã dùng ~0,0004). Phiên chiều 25/10: 0 USD.
Quota Claude Code cho sub-agent: C34 3 sub-agent (S1–S3) phiên tối; C32 ~2,1M token phiên chiều.
