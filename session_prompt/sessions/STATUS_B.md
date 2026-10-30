# STATUS B — phiên 30/10/2026 (mở 10:30 — `date`; nhận B91 10:59 30/10/2026 — `date`)

Terminal 30/10: `hue-rag-24` (A = `hue-rag-0f`, C = `hue-rag-0e`).

## Đang làm (30/10)
- **B91** — dựng bản 4b đợt 2 (CURRENT_HANDOFF "PHIÊN 30/10"), nhận 10:59 30/10/2026. Khai báo sửa: `dot2/edits/dot2.jsonl` (⇒ 4b), `dot2/edits_v4_cdec67127c4d/` (tạo, chép bản 4), `dot2/b90_quyet_dinh.md`, `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` (điền chỗ giữ chỗ). 0 USD.
  - **Xong 11:01 30/10/2026** — chờ C85 vòng 2 (A đã nhận sha, chuyển C). Sha: jsonl 4b `c0b5876ea510` (20 mục / 123 edit / 40 file), plan `26e974dc56ff`, bảng
    `42b89bd818f4`, `apply_edits.py` `8e934bbb2a7a`, `truoc_sau.py` `157f8acc0707` (compile ok), builder `f2049a793093`. Kiểm: bản 4 ↔ 4b chỉ mất D7, D1 (3)(4) thành xóa
    dòng; `apply_edits --edits` thử trong bộ nhớ 0 lỗi, không ghi record; 40 / 40 file bắt đầu `#`, 0 tiêu đề mới, đổi tiêu đề chỉ 2 edit K004.
- **Kiểm C84** — xong 11:04 30/10/2026: `do_loi_nang_aa_review.md` ready 0 / 0 / 2 (m-1 `<T>`, m-2 §6 `/tmp/judge*` — C sửa trong C87). gen-check chạy lại + đếm lại từ nhãn thô khớp. 0 USD.
- **B92** — harness Qwen3-8B (plan `52555da95828` §4, §6), nhận 11:05 30/10/2026. Worktree `/tmp/b92_qwen3`, nhánh `b92-qwen3-harness` từ `e70007b`. Khai báo sửa: file
  trong worktree theo plan §4 (ghi cụ thể sau khi đọc plan); report `report_agent/2026-10-27_phan_ton_phase_cu/qwen3_8b_harness_implementation.md`. 0 USD (không OpenRouter,
  không collection). Dừng khi C85 ready + A duyệt sha ⇒ áp đợt 2 trước.
  - **Tạm dừng 11:16 30/10/2026** — WIP commit `8545650` trên `b92-qwen3-harness` (chưa push): `dense_runner=None` ở `build_candidate` + `build_full_corpus_retrieval_service`,
    g1 `--candidate/--collection/--record/--sparse-state` + `build_parser()`, `experiments/phase_8_2/qwen3_8b.py`, test 3. T1 trước / sau sửa giống byte `23c58c47635d`; 70 test pass.
    Còn: report, push, xem lại pilot / aa; ghi lệch plan (dense_runner ở factory retrieval; mốc e5 §5 là số trước đợt 2 ⇒ phải đo lại).
  - **Xong 11:26 30/10/2026 — chờ C review code.** Push `b92-qwen3-harness` `8545650`. Report `qwen3_8b_harness_implementation.md` (untracked). Thêm: g1 mặc định 108 câu dev cũ ↔
    mới giống hệt; mốc §5 tính lại khớp (40 / 24 / 24 / 33 / 7); `preflight` ok. Hỏi A: lệch §4.2 + mốc e5 sau đợt 2. Worktree `/tmp/b92_qwen3` giữ (symlink) tới khi review xong.
  - 11:28 30/10/2026: A duyệt lệch §4.2 + mốc e5 ⇒ plan `qwen3_8b_plan.md` thêm "Sửa đổi 30/10" (sha `70ee5d44c260`, chờ C review ⇒ A duyệt); code so provider bằng hằng
    (`400ccdc`, đã push); report cập nhật.
  - 11:33 30/10/2026: review C88 `changes_requested` 0/1/1 ⇒ A chọn cách (1) ⇒ sửa `fb0b82c` (push): log trước parse; `split_calls` + `query_latency` + lệnh `latency`; plan mục 6
    (sha `9f3d616e2a59`); report `34b346a665f5`. **C88 vòng 2 ready 0/0/0.** Trước lượt có phí còn: rebase nhánh lên `main` sau đợt 2 ⇒ T1 giống `main` mới; mốc e5 + cỡ mẫu
    (plan "Sửa đổi 30/10" mục 1–2).
- **B94** — xong 11:50 30/10/2026: `data/external_project_notes/doc_rag_du_an_kia_2026-10-30.md` (đọc 3 báo cáo dự án kia, chỉ đọc). Phần đầu prompt cố định ≈ 152–193 token
  (`o200k_base`) ≪ 1.024; nghi `cost_usd` ước thấp nếu bị tính giá ghi đệm (NOT RUN, A quyết); 0 USD.
- **B95** — xong 11:53 30/10/2026 (0,0008073 USD theo công thức): usage thô 4 lần gọi luna ⇒ `cache_write_tokens` = `input_tokens` − 3 mọi lần, `cached_tokens` 0 cả lần lặp ngay;
  API không trả giá ⇒ cần User xem billing; nếu ghi đệm 0,125 thì `cost_usd` thiếu ~20 %. Ghi §7 file B94. Script `/tmp` đã xóa.
  **Tiền B phiên 30/10:** 0,0017045 (B93) + 0,0008073 (B95) = **0,0025118 USD**.
- **Kiểm C89** — xong 11:57 30/10/2026: `data/tinh_nang_moi_2026-10-27/c89_review.md` ready 0/0/3 (mẫu số đúng; B3 đầu chấm lại v2 4/4 qua; m-3 nháp streaming §6.1 dự đoán
  sai nhánh `response.answer`). 0 USD. C sửa xong 3 minor (`575f128f1c86`, `b19f8454e22b`).
- **Kiểm C90** — xong 12:02 30/10/2026: `data/dong_goi_2026-10-30/gioi_han_da_biet_review.md` changes_requested 0/1/4 (M-1: thiếu "model không biết ngày hiện tại" (M1) +
  "API không giới hạn lượt"). 0 USD. Vòng 2 12:03: bản 2 `6113fce7b3fe` ready 0/0/0 (review §5).
- **B96** — xong 12:10 30/10/2026: nháp plan `data/ngay_hien_tai_2026-10-30/plan_nhap.md` `ccaf9b426197` (15 câu + 11 câu an toàn dùng lại; nhãn L1/L2/L3; trần 0,005 USD;
  P1–P3 chưa chọn). Chờ review ⇒ A duyệt; chạy sau đợt 2. 0 USD.
  - 12:16: review C92 0/1/4 ⇒ bản 2 `fd63d9192ef6` (L1 theo `expected_type`, 12 câu quyết, trần 0,01 + pilot 3, User duyệt P1–P3). **C kiểm lại: ready 0/0/0** — chờ A duyệt sha;
    chạy sau đợt 2.
  - Bẫy: gõ tay giờ "12:15" vào header bản 2 rồi mới thấy ⇒ sửa bằng `date` (W30 — hook chỉ cảnh báo khi commit, file `data/` không qua hook).
- **B93** — áp đợt 2 (A giao 11:15 30/10/2026; plan bản 3 `5f30ac7eac16`, bảng `92e5b3caf6f1`, `dot2.jsonl` `c0b5876ea510`). Khai báo sửa: 40 file kho trong
  `dot2.jsonl` (sau backup `knowledge-base-hue/meta/backup_sua_kho_dot2_2026-10-30/`); `data/sua_kho_2026-10-27/dot2/{eval_truoc,eval_sau,backup}/`, `dot2/applied_edits_dot2.jsonl`;
  `knowledge-base-hue/meta/chunker_acceptance_samples.json` nếu chuỗi mẫu chạm edit; Qdrant collection runtime + build record + sparse state (xóa = User `!`, rồi build);
  `data/loi_nang_2026-10-28/an_toan/` thư mục mới cho lượt sinh lại / "sau". Trần 0,10 USD.
  - **Bước 1 xong 11:23 30/10/2026** — dừng trước bước 2 (A: User đi ăn; bước 2–6 phải liền, bước 5 cần `!`). 4 kiểm đạt (T1 `23c58c47635d`, diff backend 0, record / sparse,
    meta). `dot2/eval_truoc/` (+ README, `check_truoc.json`); backup kho 40 + mẫu `backup_sua_kho_dot2_2026-10-30/`; `dot2/backup/` record + sparse + snapshot
    `…-2026-10-30-04-19-43.snapshot` (checksum khớp). Script mới `data/loi_nang_2026-10-28/tools/an_toan_run.py` `7f84db74bec6` (C kiểm diff) ⇒ `an_toan/moc_regen_2026-10-30/`
    S11 / S12 × 3, chưa chấm. Tiền đợt 2 tới giờ **0,0017045 USD**.
  - Bước 5 (User `!` ở terminal B): `curl -s -X DELETE http://127.0.0.1:6335/collections/hue_full_corpus_7a2_e5_small_384 && rm /home/minhhieu/hue_rag/data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json /home/minhhieu/hue_rag/data/full_corpus_builds/full_corpus_sparse_state.json`

## Đã học / bẫy gặp (30/10)
- 10:59–11:0x: lệnh Bash ghép (dry-run + compile + `--help` + sha) bị auto mode chặn ⇒ tách từng lệnh thì chạy. Sau đó lệnh ghi STATUS / handoff bằng script Python bị tầng kiểm
  an toàn chặn "suốt phiên" ⇒ B không lách; A không ghi hộ (đúng luật); Write / Edit chạy lại được từ ~11:04.

---
Phiên 29/10 (giữ để tra):

Terminal: `hue-rag-a7` (A = `hue-rag-f7`, C = `hue-rag-ef`) · Agent: Claude Opus 5.5 · Vai: thực thi. Mã việc = mã A giao.
Kết phiên 28/10 (B78–B89, bẫy, sha): `git show 5af038d:session_prompt/sessions/STATUS_B.md`.

## Đang làm
- **B90** — chuẩn bị đợt 2 sửa kho (mục B90 trong `CURRENT_HANDOFF.md` "PHIÊN 29/10"): **xong 20:51 29/10/2026 (`date`), chờ C85 review.** 0 USD.
  - (a) `tools/apply_edits.py` `8e934bbb2a7a`, `tools/truoc_sau.py` `d02bc33650f5` (bản trước: `tools/truoc_b90/`). Thử: `--edits dot2.jsonl` trong bộ nhớ 124 / 41, 0 lỗi; mặc định
    vẫn trỏ đường dẫn đợt 1 (`touched` dừng ở `touched.json exists`).
  - (b) `dot2/edits/dot2.jsonl` bản 4 `cdec67127c4d` (bản 3 giữ `edits_v3_9b5105b35e8b/`); builder `dot2/tools/build_dot2_b90.py` `a0fafa36e39e`; bảng `dot2/b90_quyet_dinh.md`
    `2e9b25867a06`. B WebFetch PERF (huetourism) 29/10 cho D6.
  - (c) `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` `6d4a5c6293e2` (untracked).
  - Kiểm "còn hiệu lực" (1) diff `backend/` runtime `748c1e3..HEAD` rỗng (20:46), (2) build record + sparse khớp (19:13); (3) T1, (4) meta: chạy ngay trước bước 1.
- **Vòng 2 (sau review C85 vòng 1 `sua_kho_dot2_do_plan_review.md` 0/3/3 + quyết định A):** đã sửa bằng Edit (Bash lỗi server liên tục):
  builder `build_dot2_b90.py` (bỏ D7; D1 (3)(4) xóa cả dòng; chạy lại đọc bản 3 từ thư mục giữ, đòi bản 4 đã chép ở `edits_v4_cdec67127c4d/`); `truoc_sau.py` (`dump-headings`,
  lý do `e` trong `touched`, khóa W6 `truoc`/`sau` + `gold_files`); bảng `b90_quyet_dinh.md` (sửa tay 4 chỗ); plan bản 2 (M-1 thủ tục phân loại, M-2 N_AA = 2, §9).
  **Còn phải chạy (khi Bash chạy lại):** `mkdir edits_v4_cdec67127c4d && cp edits/dot2.jsonl` ⇒ builder ⇒ `apply_edits.py --edits` thử ⇒ `py_compile truoc_sau.py` ⇒ sha ⇒ điền
  chỗ giữ chỗ `SHA_4B`, `SHA_TS`, `COUNT_4B`, `FILES_4B` trong plan + bảng ⇒ báo A + C.

## Đang khai báo sửa
- `data/sua_kho_2026-10-27/tools/apply_edits.py`, `data/sua_kho_2026-10-27/tools/truoc_sau.py` (thêm tham số, mặc định giữ cũ)
- `data/sua_kho_2026-10-27/dot2/edits/dot2.jsonl` (bản mới) + `dot2/edits_v3_9b5105b35e8b/` (giữ bản cũ) + `dot2/b90_quyet_dinh.md` (bảng mục ⇒ quyết định ⇒ nguồn / lý do)
- `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_do_plan.md` (phụ lục plan đo đợt 2)
- dòng B trong `CURRENT_HANDOFF.md`

## Vừa xong
- Mở phiên, kiểm nhanh 19:13: khớp handoff (3 lệch đã báo A).

## Đã học / bẫy gặp (phiên 29/10)
- Ngay sau `date` 20:04: Bash bị lỗi "server error — auto mode cannot determine safety" ⇒ chỉ đọc bằng Read cho tới khi Bash chạy lại.

## Việc dở / câu hỏi cho A
- Chưa làm (ghi trong plan đợt 2 §4): lệnh `dump-headings` + lý do chạm `e` trong `truoc_sau.py` — viết trước bước 1 (dump bên "trước"), C đọc diff.
- Bộ an toàn "sau": harness `an_toan_gen.py` đọc / ghi cứng `an_toan/answers_*.jsonl` — dùng cách C84 tách thư mục `aa_2026-10-29/` (hỏi C).
- D7 (thêm câu "chưa xác minh gia hạn"): nếu A / C coi là khẳng định mới thì bỏ edit đó.
