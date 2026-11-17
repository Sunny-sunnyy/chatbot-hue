# C — sửa lịch bằng lời: hết "lịch chữ giả" (`p9-chan-lich-gia` + `p9-chua-ho-tro`)

Cập nhật: 10:50 17/11/2026 (C). Việc A giao sáng 17/11 (lỗi nhóm "sửa lịch bằng lời" của `data/tu_thu_2026-11-16/TONG_HOP.md`). Plan
`docs/superpowers/plans/2026-11-17-chua-ho-tro-plan.md` (duyệt `08693a018084`; Sửa đổi 17/11 `5184b3cabb3c`, nhánh `p9-chua-ho-tro-plan-3`).

## 1. Lỗi
- Cuộc có lịch đã lưu, người dùng xin một kiểu sửa mà bộ hành động chưa có (đổi thứ tự / gộp / tách các ngày, dời giờ cả lịch) ⇒ lần "hiểu ý sửa"
  trả RỖNG ⇒ lượt rơi sang đường trả lời thường ⇒ trợ lý tự viết một lịch bằng chữ như thể đã đổi, lịch thật không đổi (tự thử 16/11) — lỗi
  "nói chắc sai". Biến thể: model trả "đổi số ngày" không căn cứ ⇒ rào số ngày chặn ⇒ "Chưa làm: đổi số ngày" (sai việc).
- "Đổi thành N ngày" khi lịch đã N ngày ⇒ rơi đường thường: [code + test] `ap` với số đang có đã ra "Lịch đang đúng…", `loc_hanh_dong` giữ hành
  động ⇒ chỗ thiếu là model trả rỗng.

## 2. Đã thử và BỎ — lưới dạng câu bằng code ở đường "model trả rỗng"
Danh sách đóng các dạng câu (đổi chỗ / gộp / tách ngày, hai mốc ngày + từ chỉ thứ tự, dời giờ cả lịch, "N ngày" bằng số đang có). Bộ dò E (25 chuỗi):
bản đầu sót 9 câu sửa ⇒ sửa theo dạng ⇒ 25 / 25 [hàm]. Bộ kề bên E (20 câu, viết sau khi C sửa): **10 / 20 SAI** — dạng rộng bắt nhầm câu hỏi
thường. Với câu thường, model trả rỗng là đúng thiết kế ⇒ lưới quyết một mình ⇒ kết quả hàm = kết quả đường thật ⇒ dừng theo §8, không lượt có phí.

## 3. Đã vào main (`216c821` + m-1 `e5d557c`)
Chỉ chạy khi MODEL đã nhận lượt là câu sửa (ra hành động, hoặc "đổi số ngày" bị rào chặn): câu có ý đổi chỗ / gộp / tách ngày (dạng chặt) ⇒ dòng
"Chưa làm" nói đúng việc; đi kèm việc làm được ⇒ thêm dòng đó (trước: bỏ lặng). Chữ chép / .txt / .ics bỏ `**`. Review E READY; m-1 (lượt đã đổi số
ngày thì không thêm "Chưa làm: gộp…") đóng bằng 1 dòng. Giới hạn: dạng chặt bắt nhầm 1 câu thường của bộ kề bên (chữ "đảo" là hòn đảo) — chỉ có
hiệu lực nếu model CŨNG nhận câu đó là câu sửa.

## 4. `chua_ho_tro` (cờ `sua_lich_chua_ho_tro`)
- Lần hiểu ý có thêm hành động `chua_ho_tro` (không trường) — MODEL nhận "câu sửa lịch này mà bộ hành động chưa làm được"; code giữ lịch, viết câu cố
  định; đi kèm việc làm được ⇒ áp việc đó + "Chưa làm". Thêm "kể cả khi bằng số ngày lịch đang có" vào dòng `doi_so_ngay`.
- Cờ tắt ⇒ đúng agent cũ, đúng lời gọi cũ (test khoá: lời dặn / khuôn cũ; bản mới khác đúng 2 dòng thêm, 1 dòng bớt). Bật ⇒ agent thứ hai cùng cấu
  hình, khoá đệm riêng (`generator_openai_full_corpus.py` `sua_lich_cht_agent`).

| Đo (cờ bật, `/api/chat/stream`, lượt 1 qua biểu mẫu) | Vòng 1 `6b2c614` | Vòng 2 `8a9c63c` (BỎ) | Sàn |
|---|---|---|---|
| S2 lịch chữ giả — 14 câu xin sửa chưa làm được | **0 / 14** (lịch giữ + "Chưa làm"; E đọc tay 100 %) | 0 / 14 | 0 |
| S1 chặn nhầm — Q5 64 câu an toàn trong cuộc có lịch | **0 / 64** | 0 / 64 | 0 |
| S1 — Q5b 16 câu trộn sửa + khẩn cấp | **0 / 16** (định tuyến nhận khẩn cấp 16 / 16) | chưa đo (không chạm) | 0 |
| S1 — câu thường bộ E (9) + bộ kề bên (12) | 9 / 9 · 11 / 12 — câu lệch CÓ SẴN (cờ tắt 3 / 3 lần ra cùng 2 hành động "thêm điểm") | 9 / 9 · — | 0 do nhánh |
| S3 Q3 pass^2 bộ chuỗi đã thấy | **8 / 10** (mốc 9 / 10, 14/11) | 7 / 10 | vòng 1: ≥ 8; Sửa đổi: ≥ 9 |
| Theo dõi: "N ngày" bằng số đang có | 4 / 5 "Lịch đang đúng…"; 1 câu dặn ngắn vẫn rơi đường thường ⇒ lịch chữ mới | — | — |
| Lần hiểu ý p50 | 1,04 s (Q5, 64 lần) | 1,13 s | — |
| Tiền | 0,142 USD | 0,052 USD | trần 0,30 + 0,08 |

- Vòng 1: Q3 2 chuỗi trượt 2 / 2 lần — model gắn `chua_ho_tro` cho VIỆC LÀM ĐƯỢC (dời hai điểm sang buổi / ngày khác; câu nói theo buổi).
- Vòng 2 (User cho một vòng, luật dừng ghi trước): thêm "dời một ĐIỂM sang buổi / ngày khác là doi_buoi" ⇒ Q3 7 / 10: câu nói theo buổi / "bớt một
  chỗ" vẫn `chua_ho_tro`, câu dời hai điểm 1 / 2, thêm một ca mới (thay điểm ra "không hợp luật", chưa chứng minh do câu mới) ⇒ BỎ (A chọn vòng 1,
  `8ae846a` gỡ câu). Bài học: vá lời dặn theo MỘT loại câu hỏng không chạm loại khác, có thể kéo lệch loại thứ ba.
- **Bật cờ theo luật User chọn ("trượt ⇒ bật + ghi giới hạn")** — giới hạn: ~2 / 10 chuỗi sửa có lượt việc làm được (nói theo buổi, "bớt một chỗ",
  dời hai điểm một câu) bị báo "Chưa làm"; câu dặn "N ngày" bằng số đang có đôi khi rơi đường thường ⇒ lịch chữ mới.

## 5. Bằng chứng khác
- Test file chạm: `test_rao_so_ngay.py`, `test_sua_lich_v2.py`, `test_cong_dot_1.py` 72 passed; 8 file đọc cờ / settings: 421 passed (1 fail môi
  trường: worktree chưa có `frontend/dist`). Test rộng: xem mục 6.
- Kết quả, sổ vết, log server: `data/sua_lich_gia_2026-11-17/ket_qua_cht/` (private). Script: `data/sua_lich_gia_2026-11-17/tools/chay_c.py`,
  `q5_cht.py`; Q3 / Q5b dùng `data/len_ke_hoach_v2_2026-11-13/tools/`.

## 6. Test rộng
- `backend/tests` cả bộ trên `8ae846a` (có `--env-file`, worktree có symlink tạm `data`, kho, `frontend/dist` của cây chính — nhánh không đổi giao
  diện): **1319 passed, 0 failed, 390 s**. [đã chạy]
- Sau đó thêm khoá sổ vết `model_ra` (hành động model trả TRƯỚC khi lọc — review E; chỉ bản ghi local): `len_ke_hoach.py` 2 dòng + 1 test; file chạm
  `test_rao_so_ngay.py` + `test_sua_lich_v2.py` + `test_so_vet.py` 58 passed (không env), 48 passed (có env). Không chạy lại cả bộ (chỉ đổi bản
  ghi sổ vết).
