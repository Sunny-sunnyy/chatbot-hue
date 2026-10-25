# STATUS B — cập nhật 2026-10-25 13:05 +0700

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
  G2.1b / P2 / G2.3 không khác; P1 kém hơn (phạm sàn OOS); G2.4 đủ: none/low kém hơn (citation), high không khác.
  Chưa commit: `g2_generate.py`, report G2.
- Đang giữ GPU: không (đã nhả 12:33; G4 dùng 11:50–12:29).
- **Bước 2 (A duyệt `a4adfc8eedd9` 11:40, commit `b9789f4`):** mốc byte 11:39 PASS (`cefb2d1a…`, `1fbb5c17…`). Đang
  sửa: `backend/reranking/cross_encoder.py` (kwarg `max_length=None` + property `loaded_device`; mặc định = hành vi cũ),
  `backend/experiments/phase_8_1/g4_rerank.py` (mới), report `phase_8_1_g4_implementation.md` (mới); `pyproject.toml` + `uv.lock`
  (`uv add sentencepiece` → 0.2.2, A duyệt 11:5x cho M2).

## Thay đổi CHƯA COMMIT của B
- `backend/experiments/phase_8_1/g1_retrieval.py` — B16 (`--realism main`, file nhãn cuối).
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` — §7 (B16) + C23 m1/m2.
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` — untracked, sha `a4adfc8eedd9` (vòng sửa 1).
- `session_prompt/sessions/STATUS_B.md` (file này); dòng B + mục B17 trong `CURRENT_HANDOFF.md`.
- `git diff --check` sạch.

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

## Câu hỏi cho A
- Duyệt plan sha `a4adfc8eedd9`. G4-A về số học không thể "tốt hơn" trên dev 30 (tối đa 3 câu cứu) — vẫn chạy để chọn
  model / cách chấm cho G4-B + guardrail + latency. Dev số chính chỉ có 32 câu có đoạn đúng, nên thêm lượt GPU cũng không
  tăng được cỡ mẫu của chỉ số chính (chỉ tăng MRR keyword trên 58 câu còn lại) — B không đề xuất thêm.
- Mâu thuẫn corpus Hải Vân Quan — chờ User.
