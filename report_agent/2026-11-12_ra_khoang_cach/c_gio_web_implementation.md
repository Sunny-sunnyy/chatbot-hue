# C — giờ khác cách viết không còn làm mất mục web (`p9-gio-web`)

Cập nhật: 08:40 17/11/2026 (C). Việc A giao sáng 17/11: lỗi #3 `data/tu_thu_2026-11-16/TONG_HOP.md` (hỏi tiếp "Mở cửa lúc mấy giờ?" ⇒ từ chối + web trắng).

## 1. Tái tạo (8010, sổ vết, sha `95f105b`, đường stream)

- 3 / 3 cuộc "câu nhiều ý về một ngôi chùa ⇒ Mở cửa lúc mấy giờ?": model hiểu đúng nơi (câu tìm kho do model viết có tên nơi; câu gửi web có tên nơi); kho từ chối ĐÚNG (`scripts/grep_kb.sh`: bài của nơi đó 0 dòng giờ mở cửa); mục web 3 / 3 đạt ⇒ hôm nay không tái hiện web trắng. [đã chạy]
- Web trắng tối 16/11 (8011, không sổ vết) = `WEB_KHONG_TIN_CAY_TEXT` (kiểm cuối gạt mục model viết). Đếm `chat_metrics` 15–17/11 (`web_outcome`, `web_kiem`): đường câu-từ-model (lượt hỏi tiếp) 7 / 26 `khong_tin_cay` ↔ đường câu gõ 3 / 54 (**đính chính 11:26 17/11/2026:** đúng là **3 / 40** lượt thật — 14 trong 54 lượt là lượt test dùng model giả `model: "probe"`; kiểm độc lập `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_15_25_1711.md`). Mã: `so_ngoai_trich` 5 (4 + 1), `gia_luu_tru` 4 (2 + 2), `tien_ngoai_trich` 1. [đếm từ log]
- Gốc [chạy hàm thuần]: `tra_web._chuoi_so` so số theo cách viết — trích "8h - 18h" ⇒ {8, 18}, model "8h00–18h00" ⇒ {800, 1800} ⇒ `so_ngoai_trich` dù cùng giờ. Chưa chứng minh đúng ca tối 16/11 (không còn chữ model) — cơ chế đã chạy + số đếm khớp.

## 2. Sửa (`backend/llm/tra_web.py`)

`_GIO` + `_gio_gon`: trước khi tách chuỗi số, giờ "H:MM" / "HhMM" / "H giờ MM" (H 0–24, MM 00–59) ⇒ phút 00 thành giờ trần ("8:00", "08:00", "8h00" ⇒ "8", như "8h" / "8 giờ" vốn ra "8"), phút khác bỏ số 0 đầu ("07:30" ⇒ "7:30"). Áp cho cả chữ model lẫn tiêu đề + đoạn trích. Không nới luật nào khác: giờ khác vẫn `so_ngoai_trich`.

## 3. Bằng chứng

| Bước | Kết quả | Thời gian |
|---|---|---|
| Bộ dò E `data/gio_web_2026-11-17/bo_do.jsonl` (41 ca, người không viết code soạn) | bản đầu 3 SAI bắt buộc ("8 giờ 30", "24:00") ⇒ sửa ⇒ **0 SAI bắt buộc** · 35 đúng · 3 gạt nhầm được phép (giờ chiều / tối viết chữ) · 2 giới hạn (cũng qua ở main) · 1 không tính; main: 16 SAI | < 2 s |
| 18 mục web thật trong sổ vết 16–17/11, kiểm bằng bản cũ ↔ mới | 0 khác | < 2 s |
| `tests/test_b6_tra_web.py` (có / không `--env-file`, worktree có symlink tạm) | 127 passed / 127 passed | 23 s / 27 s |

Không test rộng (§8: nhánh chỉ đổi một hàm thuần + test của nó). Không lượt có phí trên nhánh. Sau merge, 1 cuộc thật trên 8010 (`05ec2f5`, sổ vết): mục web `co_muc`, nêu giờ 8:00–18:00 của đúng nơi. [đã chạy]

## 4. Giới hạn

- (review E m-1, A ghi giới hạn khi merge `05ec2f5`) giờ phút 00 rút về số trần ⇒ giờ model viết khớp cả số không phải giờ trong trích ("Mở 2:00" ↔ "2 km", "8:00" ↔ "8 phòng"); cùng loại lỗ đã có với "8h" / "8 giờ". Đã thử chuẩn hoá ngược (mọi giờ ⇒ "H:MM", commit `a935c58` trên `p9-gio-web`, test 128 passed): gạt nhầm ca 33 bộ E (thời lượng "tour 8h" ↔ "8 tiếng") ⇒ BỎ, không merge — thời lượng hay gặp trong trang du lịch, còn lỗ m-1 cần model bịa đúng số có sẵn trong trích.
- Giờ viết bằng chữ buổi ("5 giờ chiều" ↔ "17h", "9h tối" ↔ "21:00") vẫn bị gạt (phía an toàn); "9h tối" ↔ "9:00" vẫn qua (như main).
- Lỗi mở đầu "Tôi không tìm thấy đủ thông tin…" khi mục web có giờ = mục (f) `TONG_HOP.md`, không thuộc nhánh này.
- `gia_luu_tru` ở đường hỏi tiếp (2 lượt): luật xét cả câu model viết ⇒ chặt hơn, đúng thiết kế; chưa xem kỹ.

Tiền: 0,0116 USD (6 lượt tái tạo, `usd` theo sổ vết). Script tạm `/tmp/c_mocua/`.
