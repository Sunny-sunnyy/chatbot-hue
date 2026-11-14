# Review nhánh `p9-tien-web` `4656d91` (B — kiểm tiền mục web theo giá trị) · E · 16:31 14/11/2026

Plan `docs/superpowers/plans/2026-11-14-tien-web-chuan-hoa-plan.md` (sha `e34fa9cc0ff0`); report `b_tien_web_chuan_hoa_implementation.md`. Mức nhẹ, 0 USD.

## Kết luận: `ready_for_user_confirmation` — A merge được; 3 minor theo dõi (đều là lỗ CŨ của bộ nhận tiền, không do nhánh)

## Đã kiểm
- **Phạm vi:** 2 file (`llm/tra_web.py`, `tests/test_b6_tra_web.py`); không chạm lời dặn, model, Serper, `assistant.py` ⇒ chuỗi gửi model không đổi.
- **Luật không nới:** vẫn `tiền mục web − tiền đoạn trích ≠ ∅ ⇒ chặn`; chỉ đổi khoá so thành `("gia_tri", số)` hoặc `("chuoi", …)` khi mơ hồ. Đoạn trích không có tiền ⇒ mọi tiền trong mục bị chặn (đúng (d)). Phép kiểm "mọi chuỗi số ⊂ đoạn trích" (`so_ngoai_trich`) giữ nguyên và vẫn là lớp chặn thứ hai.
- **Tính lại V độc lập** (chạy `kiem_muc_web` của main và của nhánh trên 76 mục đã lưu, 0 USD): **43 ⇒ 51** — khớp B. Lỗi `tien_ngoai_trich` 16 ⇒ 4; 4 ca còn chặn đều là số bịa 220.000 (đoạn trích có 160 / 170 / 200 / 250 nghìn) ⇒ (c) đạt.
- **8 mục mới qua** (E in giá trị từng mục): 4 mục "65.000 đồng" (trích có 55 / 65 / 95 nghìn), 4 mục "594.000 / 491.000 / 663.000 đồng" (trích có đúng ba số) ⇒ mọi giá trị ∈ đoạn trích (L = 0).
- **Ca mơ hồ (thử 16 dạng):** "1.500 triệu" ⇒ không đoán (giữ chuỗi) · "1,5 đ", "594.000,5 đồng", "1.234.567,8 đ" ⇒ không đoán · "1,5 / 1.5 / 1,50 triệu" ⇒ 1.500.000 · "12,5k" ⇒ 12.500 · "0,5 triệu" ⇒ 500.000 · "1.000.000đ" = "1,000,000 VND" ⇒ 1.000.000. So bằng đúng, không làm tròn ("1.500.001" ≠ "1,5 triệu" có test).
- **Ca lọt thử thêm** (đoạn trích chỉ có 100.000 VNĐ): "1000000 đồng" (không dấu ngăn), "50.000–100.000 đồng" (cận dưới không đơn vị), "100.000 USD" ⇒ đều bị chặn bởi lớp chuỗi số; "1.000.000 đồng", "150 nghìn", "50k" ⇒ chặn bởi lớp tiền.
- **Test:** `test_b6_tra_web.py` 97 đạt (worktree sạch, không khoá; cần symlink `data/` — 7 test đọc build record).

## Finding (minor, lỗ cũ của `so_tien.tim_so_tien`, không chặn merge)
- **m-1:** "2 triệu rưỡi" được đọc là "2 triệu" ⇒ đoạn trích có "2 triệu" thì mục ghi "2 triệu rưỡi" vẫn qua (bản so chuỗi cũng vậy). Hiếm; theo dõi.
- **m-2:** "150K" (chữ K hoa) không được nhận là tiền ⇒ chỉ lớp chuỗi số chặn; nếu đoạn trích tình cờ có số "150" khác nghĩa (vd "150 năm") thì "150K" bịa lọt. Sửa rẻ khi cần: nhận "K" hoa trong `tim_so_tien` (đụng B5 dùng chung ⇒ việc riêng).
- **m-3:** "1,500 đ" đọc là 1.500 (dấu phẩy ngăn nghìn kiểu Anh) — nhất quán với "594,000"; ghi để biết.

## Tiền
0 USD.
