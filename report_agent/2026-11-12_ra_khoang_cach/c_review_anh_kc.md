# Review nhánh `p9-anh-kc` @ `ea055a0` (E) — C · 18:46 14/11/2026

**Kết luận: `changes_requested`** — 0 blocker · 1 major · 1 minor. 0 USD.

## Cổng tối thiểu
- Diff: `anhBai.js` (18 dòng bỏ `kc`) + 5 jpg đổi + report — trong phạm vi; 0 file ảnh khác đổi.
- C nhìn cả 13 ảnh lượt 1 (`/tmp/e_nang.jpg`, ô 2–4 và 6–15; ô 1, 5 E giữ `kc`) và 5 ảnh lượt 2 (`/tmp/e_kc_5.jpg`) theo thước A đặt cho lượt review này: **đúng nơi / đúng quán thật — biển tên, công trình nhận ra được — không phải ảnh minh hoạ chung**.

## M-1 (major) — "luật nguồn" nâng 10 ảnh mà nhìn ảnh không nhận ra được nơi / quán
- **Ý nghĩa của `kc`:** người nhìn không chắc ảnh đúng chính nơi đó ⇒ không hiện cạnh câu trả lời, vì ở đó ảnh thành lời khẳng định. Luật nguồn thay việc NHÌN bằng việc tin trang nguồn — chỉ đủ khi ảnh tự nó cũng nhận ra được.
- **Không đạt thước (giữ `kc`):**
  - 8 ảnh chỉ là **món ăn / ly chung**, không biển, không không gian quán (9 bài): Phúc Long (2 ly — giống mọi chi nhánh, không thấy cửa hàng Huế), Quán Bà Cú, Bánh lọc Bà Văn, Bánh ép Huệ, Bánh ép 1992, Bánh ép Nhà Su, Cơm tấm Okla, Cơm hến Bà Cẩm, Bánh canh cá lóc Thùy Dương ( ShopeeFood là trang người bán tự đăng, ảnh hay là ảnh mẫu / dùng lại — không kiểm được bằng mắt).
  - Lễ hội Hương xưa làng cổ Phước Tích: **chính ảnh múa lân này E đã bác ở v4** ("không nhận ra đúng làng"); nay nâng chỉ vì nguồn là cổng du lịch tỉnh — trang tổng hợp có thể dùng ảnh minh hoạ ⇒ mâu thuẫn với lần nhìn trước.
- **Đạt (đồng ý nâng):** Không Gian Xưa Minh Mạng (công trình + cổng nhận ra được), Nhà hàng chay Hoa Viên (mặt tiền nhà hàng), An Nhiên Garden (ảnh từ website riêng của quán — chấp nhận); lượt 2: Khu phố Tây (cổng "Phố đi bộ – Walking Street" đọc rõ), Hàm Rồng, Lộc Bình (người xa, nhỏ), bánh ép (món đặc sản — bài về MÓN, không phải quán ⇒ đúng món là đủ), The Time Coffee (tên quán trên ảnh).
- **Tác động nếu giữ như nhánh:** 10 ảnh món / lễ hội chung hiện cạnh câu trả lời như "đây là quán / lễ đó".
- **Tiêu chí đóng:** giữ `kc` cho 10 bài trên (9 bài ảnh món / ly + Phước Tích); kết quả dự kiến: 18 − 10 = 8 bài nâng ⇒ `kc` 57 ⇒ 49, hiện được 161 ⇒ **169** (thay 179). Luật nguồn chỉ dùng kèm điều kiện "ảnh cho thấy công trình / biển / không gian của nơi đó"; món đặc sản (bài về món) được miễn điều kiện này.

## Minor
- **m-1:** The Time Coffee (lượt 2): tên quán là chữ trang trí lớn đè lên ảnh — đúng là tên quán, nhưng chạm luật "chữ to" của chính tiêu chí; chấp nhận được (chữ là tên, không che chủ thể) — ghi để biết.

## Vòng 2 @ `702fcf3` (C · 18:48 14/11/2026)
**Kết luận: `ready_for_user_confirmation`** — M-1 đóng, 0 finding mới.
- [Chạy] so `anhBai.js` main ↔ nhánh: đúng 8 bài bỏ `kc` = 3 ảnh đạt lượt 1 (Không Gian Xưa, Hoa Viên, An Nhiên) + 5 ảnh lượt 2; 0 dòng khác đổi; 5 jpg đổi = 5 ảnh lượt 2. `kc` 49, hiện được 169 — khớp. `git diff --check` sạch.
