# STATUS B — cập nhật 2026-10-25 13:55 +0700

Terminal phiên này: `hue-rag-3f` (A = `hue-rag-c6`, C = `hue-rag-a1`; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi
User (25/10, terminal B): việc A giao = User nói "làm đi"; xong báo cáo, nhắn A, chờ việc tiếp.

## Đang làm — B17 (mục "### B17" trong `CURRENT_HANDOFF.md`, A giao 11:22)
- **Bước 1 xong 11:29:** sửa `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` → sha `43086f053db8`
  (bản nháp cũ `c29b547b7417`). Gồm: G4-B được duyệt; tập GPU cố định dev 30 (seed 20261024) + test 15; cỡ mẫu ghi trước
  (G4-A cứu tối đa 3/30 ⇒ không thể "tốt hơn" ở chỉ số chính; G4-B tối đa 17/30); kiểm GPU trước mỗi lượt; latency đúng
  cách; luật lỗi luna; guardrail citation +2 câu (nhiễu 7B); `is_refusal` đã kiểm (khớp hệt) + nhãn `answer_type`; G2.3
  chính sách A chọn; G2.4 thêm `none`.
- Kèm sửa C23 m1/m2 (`phase_8_1_b16_review.md`) ở `phase_8_1_g1_implementation.md` §7.
- **Vòng sửa 1 lúc 11:36** theo C23 (M1 tiêu chí chung G2 §2.1; M2 luật G4 theo spec: MRR@10 VÀ context5 — A quyết;
  M3 mốc native p100 không rerank; m3–m6) ⇒ sha `a4adfc8eedd9`. User giữ cả 9 câu bất đồng (số chính không đổi).
- **Chờ:** C review vòng 2 + A ghi "duyệt bản sha …". Không chạy GPU / paid trước đó.
- **G4 xong 12:33** — report `phase_8_1_g4_implementation.md` (sha `6c70e903c0fa` lúc nhắn C). Kết luận: M1/M2 kém hơn
  (mất 1–3 câu); luna chưa rõ; G4-B kém hơn so runtime / không khác so mốc pool 100. Chờ C review rồi mới G2.
- **G2 xong 13:05** — report `phase_8_1_g2_implementation.md` (sha `56b6afa4c7ce`). Context 10 tốt hơn + xác nhận test;
  G2.1b / P2 / G2.3 không khác; P1 kém hơn (phạm sàn OOS); G2.4 đủ: none/low kém hơn (citation), high không khác. Đã commit `266c105`.
- **B18 (A giao 13:17) plan xong 13:22** — `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_keyword_plan.md` sha
  `f5678965a448`; chờ C review (sau G3) + A duyệt. A 13:2x cho làm trước: harness + cổng tương đương (chưa biến thể).
  Đang sửa: `backend/experiments/phase_8_1/g4_keyword.py` (mới); dữ liệu `data/phase_8_1/g4k/`.
  13:3x: C review ready (2 minor) → sửa, plan sha `d7e53186b364`, chờ A duyệt. Cổng tương đương PASS: R0 = G1 runtime
  108/108; N0 lệch 1 câu (162) do Qdrant float32 phá hòa khác — tập ứng viên giống hệt.
  **13:45 chạy xong** A/E/P (0 USD) — report `phase_8_1_g4_keyword_implementation.md`; không biến thể nào tốt hơn.
  Review G3 §10 → `phase_8_1_g3_b10_review.md` (đã commit `0c19756`). Plan B18 đã commit `68b9db0`.
- **B19 (A giao 13:44) nháp G5 xong 13:50** — `phase_8_1_g5_decision_table_draft.md`; A tự review (C không cần, A 13:5x). G3 §10: B review →
  C sửa → A duyệt `d89a919067ba`.
- **Review G3 xong** — `phase_8_1_g3_review.md` (ready, 2 minor). **B20 (A giao 14:02):** đang sửa
  `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md`, `BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `BAO_CAO_CHIA_DOAN.md`; sau đó review C30.
  **B20 xong 14:15** (3 file, bản 5 / 5 / 3), chờ C review. Tiếp: review C30 (3 file của C) + review G5 của A.
  14:2x: B20 C review ready (2 minor đã sửa, C đóng). Review G5 synthesis → `phase_8_1_g5_review.md` (changes_requested,
  2 major); A giao M1 → `phase_8_1_g5_by_category.md` + `backend/experiments/phase_8_1/g5_by_category.py` (mới).
  Review C30 → `phase_8_1_c30_user_reports_review.md` (ready, 4 minor). G2 report §6: thêm NOT RUN "claim không nguồn".
  Chờ: A vòng 2 G5; C31 (khóa G0.6) khi C nhắn.
- Đang giữ GPU: không (đã nhả 12:33; G4 dùng 11:50–12:29).
- **Bước 2 (A duyệt `a4adfc8eedd9` 11:40, commit `b9789f4`):** mốc byte 11:39 PASS (`cefb2d1a…`, `1fbb5c17…`). Đang
  sửa: `backend/reranking/cross_encoder.py` (kwarg `max_length=None` + property `loaded_device`; mặc định = hành vi cũ),
  `backend/experiments/phase_8_1/g4_rerank.py` (mới), report `phase_8_1_g4_implementation.md` (mới); `pyproject.toml` + `uv.lock`
  (`uv add sentencepiece` → 0.2.2, A duyệt 11:5x cho M2).

## Thay đổi CHƯA COMMIT của B (kiểm `git status` sau commit `0c19756`)
- `backend/experiments/phase_8_1/g4_keyword.py` — mới (B18).
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_keyword_implementation.md` — mới (B18), chờ C review.
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md` — mới (B19), A review.
- B20: 3 file `bao_cao_he_thong/` (TIM_KIEM, SINH_CAU_TRA_LOI_API, CHIA_DOAN); review G3 / G5 / C30; `phase_8_1_g5_by_category.md`;
  `backend/experiments/phase_8_1/g5_by_category.py`; sửa `phase_8_1_g2_implementation.md` §6 (NOT RUN).
- `session_prompt/sessions/STATUS_B.md` (file này); dòng B trong `CURRENT_HANDOFF.md`.
- Đã commit (A): B16 + plan G2/G4 `b9789f4`; G4 + `cross_encoder.py` + sentencepiece `ee557f9`; G2 + minor G4 `266c105`;
  plan B18 `68b9db0`; review G3 §10 `0c19756`.
- Không phải của B (đừng commit nhầm): `full_corpus_pipeline.py`, `g3_chunking.py`, report G3, `STATUS_C.md`,
  `phase_8_1_g4_keyword_plan_review.md` (C), `báo cáo nghiên cứu github.txt` (User).

## Đã xong trước (đã commit)
- B9–B15 (`1832201`, `74270ab`, `b8dbe95`, `0131afb`, `8156395`); chi tiết `PROJECT_HISTORY.md` / đợt `2026-10-24_phase_8_1_ra_soat`.

## File private đang dùng (không commit)
- `data/phase_8_1/g1/*.jsonl` — kết quả G1 từng câu.
- `data/phase_8_1/gold/gold_draft.jsonl` (`bab707b9…`); `data/phase_8_1/golden_realism_final.jsonl` (số chính = bỏ `unnatural`).
- Mốc runtime: `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl` (`cefb2d1a…`); native `1fbb5c17…`.

## Tiền paid phiên (B)
- 25/10: 0,1653212 USD = G4 luna 0,0087972 + G2 0,1565240 (G2: 1.147.055 vào / 83.637 ra). Judge: quota Claude.

## Đã học / bẫy gặp
- Qdrant có thể tắt giữa phiên; pytest vẫn chạy và lỗi môi trường trông như lỗi code: đọc dòng `E` trước.
- pytest: rootdir là gốc repo; chỉ liệt kê file test, không dựa vào `--deselect`.
- Lệnh paid mới: chạy thử không `--env-file` trước để thấy nó định gọi gì.
- Auto-mode chặn `curl -X DELETE` Qdrant / `rm` lớn: dừng, nhờ User chạy `!` trong terminal B.
- Hai session cùng sửa working tree: khi gate cần so byte mà file session khác đang dở, chạy bản HEAD (`git show HEAD:…`
  hoặc `git archive HEAD backend` vào `/tmp` + symlink `data/`, `knowledge-base-hue/` chỉ đọc).
- Script ngoài `backend/` cần `PYTHONPATH=.:..`.
- Qdrant không cam kết thứ tự hòa điểm; runtime và native đã phá hòa theo point_id.
- Validator citation: câu từ chối chuẩn + `[n]` = lỗi.
- `g1_retrieval run` với `--name` đã có sẽ ghi đè JSONL.
- `g1/c_runtime.jsonl` cùng tập câu với `runtime.jsonl` (dev, 108 câu) — không phải tập test; số test lấy theo `split.json`.
- Mở phiên: chưa biết terminal nào là A ⇒ gửi cùng tin cho cả hai peer, hỏi ai là A (25/10, ổn).
- Danh sách "chưa commit" trong STATUS / tin nhắn bị cũ khi A commit giữa chừng (25/10: báo g2_generate.py chưa commit
  trong khi đã ở `266c105`) ⇒ trước khi liệt kê, chạy `git status --short` + `git log --oneline -3`.
- HNSW: kết quả dense phụ thuộc `limit` (30 đầu của `limit=100` ≠ `limit=30` ở 1/108 câu) ⇒ tái lập runtime phải hỏi
  đúng `limit` như production. Qdrant sparse tính float32 ⇒ phá hòa có thể khác float64 trong bộ nhớ.

## Câu hỏi cho A
- Duyệt plan sha `a4adfc8eedd9`. G4-A về số học không thể "tốt hơn" trên dev 30 (tối đa 3 câu cứu) — vẫn chạy để chọn
  model / cách chấm cho G4-B + guardrail + latency. Dev số chính chỉ có 32 câu có đoạn đúng, nên thêm lượt GPU cũng không
  tăng được cỡ mẫu của chỉ số chính (chỉ tăng MRR keyword trên 58 câu còn lại) — B không đề xuất thêm.
- Mâu thuẫn corpus Hải Vân Quan — chờ User.
