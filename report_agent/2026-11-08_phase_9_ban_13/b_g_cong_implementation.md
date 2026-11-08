# Implementation Report: Phase 9 bậc G — cổng 2 nhóm (ĐANG LÀM — bản dở)

Người làm: B (Claude Code, `hue-rag-a1`) · cập nhật 12:03 08/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-08-phase-9-g-cong-plan.md` bản 2 `2513df2c6930` (A duyệt sau review sub-agent 2 vòng). Spec bản 13 §12 `5557f0fd7650`.
Nhánh `p9-g-cong` (tách `main` `442f758`): `d0849ce` code · `9c8a7f2` chỉnh định tuyến · `c9f2df4` chỉnh lời dặn agent (chưa đo lại). Mốc: worktree `main` `442f758`.

## 1. Đã làm (thời gian từ `date` / log)

| Bước | Lúc | Kết quả | USD |
|---|---|---|---|
| Code + test 0 USD | ~11:05–11:40 | test rộng **749 đạt** (còn lại = 2 test cần khoá); `test_g_cong.py`: lời dặn mỗi loại lượt, biểu mẫu giống byte `81d3040cf53f`, 3 đường `out_of_scope` chữ đúng 1 lần, `done` không `tu_choi_kho`, không nối khối thời tiết | 0 |
| 1 lượt thật | ~11:42 | câu Huế trả lời có nguồn; câu ngoài phạm vi ⇒ `out_of_scope`, cổng web đóng | 0,0007 |
| Bước 2 chỉ định tuyến | ~11:25–11:40 | mốc ×2: S3 0, xã giao ⇒ Huế 1 / 15. Biến thể bản đầu: S3 0 ×2 nhưng lượt nhắc tên của chuỗi B3 ⇒ Huế 6 / 7 ⇒ **chỉnh 1** (`9c8a7f2`, ROUTER `6b4796f7a35c`): **S3 0 ×2**, xã giao ⇒ Huế 2 / 27 (lịch sử 1 / 7, (a) 1 / 8); A4 / A5 âm lịch (E nhờ) ⇒ `tro_ly_hue` ×2 | 0,128 |
| Bước 3 cả câu (ANSWER `33690e611fd9`) | 11:41–11:55 | xem §2 | 0,301 |
| Chỉnh 2 lời dặn agent (`c9f2df4`, ANSWER `5d70126fdf17`) | 12:02 | **chưa đo** — chờ A / User quyết tiền (dự phóng vượt mức dừng 0,55) | 0 |

**Tiền tới giờ ≈ 0,43 USD** (cộng từ file kết quả).

## 2. Kết quả bước 3 (biến thể ×2 trên ANSWER `33690e611fd9` + mốc ×1) — đếm bằng code

| Sàn | Lượt 1 | Lượt 2 | Mốc | Kết luận |
|---|---|---|---|---|
| S2 ngoài phạm vi bị trả lời (48 lượt / bộ, gồm trùng mẫu 30) | 0 | 0 | — | đạt |
| S2b ngoài phạm vi có mục web | **7** | **5** | 0 (đi tuyến riêng) | **trượt** — agent trả "không đủ thông tin" cho câu di tích / lễ hội / vé / biểu diễn của nơi khác (5 câu Golden) + 1 câu nhờ viết email ⇒ cổng mở, 4–5 câu có mục "Từ web" |
| S2c Huế-kho-thiếu có web (17) | 16 | 15 | 16 | đạt (≥ mốc − 1) |
| S3b câu Huế ra `out_of_scope` (bộ sàn) | 0 | 0 | — | đạt |
| oos_lech / citation_error | 0 / 0 | 0 / 0 | 0 / 0 | — |
| Quan sát khẩn cấp (30 câu, 1 lượt) | 9 câu ra câu ngoài phạm vi | | | xấu — câu khẩn cấp không nêu nơi bị coi là ngoài phạm vi |
| Quan sát A4 / A5 âm lịch | ra câu ngoài phạm vi | ra câu ngoài phạm vi (A4) | | xấu — định tuyến đúng, lời dặn agent sai |
| S1 an toàn · S4 mẫu 30 | chưa chấm (judge mù) | | | NOT RUN |

Chỉnh 2 (`c9f2df4`): lời dặn agent nêu rõ "nơi khác mà không hỏi gì về Huế; nhờ viết code / dịch / soạn thư — kể cả có chữ Huế ⇒ ngoài phạm vi" và "câu không
nêu nơi nào khác (ngày tháng, giờ, an toàn, đi lại, cần giúp gấp…) ⇒ về Huế".

## 3. Việc còn (lệnh ở `session_prompt/sessions/STATUS_B.md` mục 0g)

1. Đo lại bước 3 trên `c9f2df4` (1 lượt: s2 + an toàn + mẫu 30 + (a) + khẩn cấp + A4 / A5 ≈ 0,11 USD) ⇒ đạt thì khoá sha, lượt 2.
2. Chấm S1 (2 judge mù, mẫu `data/phase_9/b2_chay/tools/an_toan_b2.py`) + S4 (mẫu 30 mù) — 0 USD (sub-agent).
3. Kín (A chạy, lệnh trong STATUS_B) ⇒ S5 (báo A trước) ⇒ cổng ổn định ⇒ review cả nhánh.

Dữ liệu: `data/phase_9/g_cong/` (`tools/do_g.py`, `ket_qua/`).
