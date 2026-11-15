# Review — `p9-tuan-sau` (B, `b38f5ad`) · E · 12:32 15/11/2026 (`date`)

- **Kết luận: `ready_for_user_confirmation`, 0 finding.** Nhánh nhỏ (luật 15/11): đọc diff, không chạy lại test; `git diff --check` sạch; dựng trên `c842861` ⇒ rebase. Đúng hướng nhóm chốt: code tính giao "tuần sau" ∩ 7 ngày dự báo, không theo luật "chỉ khi hôm nay là thứ Hai".
- Đối chiếu tay cả 7 thứ: `dau = 7 − weekday`. Thứ Hai ⇒ 7 > 6 ⇒ ngoài 7 ngày. Thứ Ba ⇒ (6, 6) = đúng thứ Hai tuần sau. Chủ nhật ⇒ (1, 6) = thứ Hai…thứ Bảy, dòng "Dự báo chỉ có tới thứ Bảy" đúng. Regex `tuần\s+sau\b(?!\s+nữa)` ⇒ "tuần sau nữa" vẫn ngoài. "tuần sau" kèm "tháng sau" ⇒ `_XA` vẫn bắt ⇒ ngoài, và `tuan_sau` chỉ đặt khi không ngoài.
- Rủi ro đã loại: `khoi_du_bao` đọc `du_bao.ngay[den]` với `den = 6` ⇒ an toàn vì bước parse bắt buộc đúng 7 ngày (`thoi_tiet.py:148` ⇒ `ValueError("do_dai")`). Code đặt khoảng ngày, bỏ số ngày model gửi: đúng luật "phép tính ⇒ code".
- Số đo B báo (X01 ×3: gọi công cụ 3 / 3, 0 số lạ; an toàn 0 đổi lớp; 1.064 test) đủ cho nhánh này. 2 test cũ B sửa là test khẳng định hành vi cũ đã bỏ ⇒ sửa đúng, không nới tiêu chí. Hai mã `cham_b5b` ở X01 do nhãn cũ ⇒ cần cập nhật nhãn bộ chấm (việc riêng, nhỏ).
