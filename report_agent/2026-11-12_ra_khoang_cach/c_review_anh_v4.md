# Review nhánh `p9-anh-v4` @ `d5fd9b3` (E) — C · 18:15 14/11/2026

**Kết luận: `ready_for_user_confirmation`** — 0 blocker · 0 major · 3 minor (2 có từ trước, ngoài nhánh). 0 USD.

## Cổng tối thiểu
- Diff: `anhBai.js` + 29 jpg mới + 7 jpg đổi + report. Không file code / test / cấu hình khác ⇒ trong phạm vi.
- Đổi bài ngoài phạm vi? [Chạy] so `anhBai.js` main ↔ nhánh: 11 dòng bỏ `kc` = đúng 6 bài đổi ảnh + 5 bài giữ ảnh (khớp report); 6 jpg `M` đều thuộc 6 bài đổi ảnh; 0 dòng khác đổi.
- Sàn "người giao nhìn lại 100 % ảnh sẽ hiện": C nhìn lại cả 19 ảnh E đã xem (`/tmp/e_v4_xem_0.jpg`, `_1.jpg`) — 16 giữ không `kc` đều đúng nơi / quán; 3 E bác về `kc` (múa lân, 2 quán cà phê không biển tên) — C đồng ý.
  - Đối chiếu kho (`scripts/grep_kb.sh`): biển Bánh mì Ba Bự "39 Bến Nghé" và Bánh mì Trường Tiền O Tho "14 Trần Cao Vân" khớp địa chỉ bài.
  - Nguồn: Lễ Ban Sóc — trang tái hiện lễ đó ở Ngọ Môn; An Truyền — bài "lễ Thu tế làng Chuồn" (= An Truyền); Wonderverse — bài khai mạc 2026. Xã Tắc: link chỉ còn trang chủ tên miền (luật đổi link trùng kho) ⇒ không lần lại được trang gốc; ảnh hợp lễ tế đàn — chấp nhận.
- Mẫu 10 ngẫu nhiên (hạt giống 1411) trong 138 ảnh không `kc` của nhánh (`/tmp/c_photon/mau10_v4.jpg`): 10 / 10 đúng chủ thể; 2 lưu ý ở m-1, m-2.
- Ảnh lịch Thuận An vẫn 33 / 34 theo tiêu chí ghi trước: đồng ý (ảnh biển chung, `kc`).

## Minor
- **m-1 (có từ trước, ngoài nhánh):** bài cẩm nang `travel/places/travel_guides.md` mang ảnh Ngọ Môn KHÔNG `kc` từ main — trái luật v4 "bài chủ đề luôn `kc`". Nếu code ảnh-dưới-câu-trả-lời coi bài này là "một nơi" thì câu trả lời từ cẩm nang sẽ hiện ảnh Ngọ Môn. Đề xuất: gắn `kc` cùng nhánh sau.
- **m-2 (có từ trước, ngoài nhánh):** ảnh Cơm hến Đập Đá (không `kc`) có bảng giá trên biển "8.000 / 10.000" trong khi bài kho ghi "10.000 – 20.000 VNĐ" ⇒ ảnh hiện cạnh câu trả lời mâu thuẫn số kho. Đề xuất: `kc` hoặc đổi ảnh.
- **m-3:** biển Bánh O Lé (mới, không `kc`) có số điện thoại chữ nhỏ; bài kho không ghi điện thoại. Ở Khám phá / câu trả lời đọc được khi phóng to; ở thẻ bữa (44 px) không đọc được. Không chặn; nếu muốn chặt như thẻ bữa thì cắt viền dưới biển.
