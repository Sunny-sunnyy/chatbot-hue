# Review nhánh `p9-anh-quan` `496206d` (C — ảnh nhỏ cạnh tên quán ở thẻ bữa) · E · 18:15 14/11/2026

Mức nhẹ, 0 USD. **Kết luận: `ready_for_user_confirmation`** — A merge được; 1 minor (nên sửa, ~2 dòng).

## Đã kiểm
- **Phạm vi:** `quan_lich.py` (trường `anh` kiểm lúc nạp; `_hien` gửi `anh`), `LichV2.jsx` (`anhQuan`), CSS 2 dòng, 6 ảnh `anh/quan/`, 1 test, comment md5 `settings.yaml`. Không chạm chuỗi gửi model: tên quán không vào model, và `test_q1` vẫn đạt.
- **Rào đúng chỗ:**
  - Server chỉ nhận `anh` cho dòng ngoài kho, theo mẫu `quan/[a-z0-9_]{1,40}`.
  - Giao diện kiểm lại cùng mẫu.
  - Quán kho lấy ảnh từ `anhCuaBai(bai_id)` nên không cần trường riêng.
  - Test phủ cả 4 dạng xấu: `../x`, `.jpg`, `https://`, `kp/`. Phủ cả trường hợp quán kho mang `anh` (bị chặn).
- **Test:** `test_quan_lich.py` 15 đạt (11 s). Chạy trên worktree tạm riêng của E, có trỏ `data/` tạm; worktree đó đã gỡ, không đụng worktree của C.
- **6 ảnh ngoài kho (E xem):**
  - 3 ảnh có biển tên đọc được: một biệt thự vàng, một cổng gỗ, một biển quán.
  - 3 ảnh không đọc được tên (cổng gỗ quán cà phê, lối có biển chỉ đường, sảnh cột gỗ). C đã nhìn 100 % và cho qua.
  - Ở khổ 44 px tên trong ảnh cũng không đọc được ⇒ chấp nhận.

## Finding
- **m-1 — ẩn ảnh `kc` ở thẻ bữa:**
  - Ở thẻ bữa, ảnh nằm ngay cạnh tên một quán cụ thể, nên người xem hiểu "đây là quán đó". Đó cũng là lý do ảnh `kc` bị ẩn cạnh câu trả lời trợ lý. Trang Khám phá thì khác: thẻ là cả bài, ảnh chỉ để minh hoạ.
  - Số quán bị ảnh hưởng: 42 quán kho trong bảng, trên main có 13 ảnh `kc`; sau nhánh ảnh v4 còn 11 / 37 quán có ảnh.
  - Đóng khi: trong `anhQuan`, `const a = anhCuaBai(q.bai_id); return a && !a.kc ? a.anh : null;`.
  - Hệ quả: 11 quán chỉ hiện tên, không ảnh. Ảnh sai quán tệ hơn không có ảnh.
