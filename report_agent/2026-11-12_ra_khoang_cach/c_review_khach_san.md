# Review nhánh `p9-khach-san` @ `954cf63` (B; plan sha `067fc664c753`) — C · 18:45 14/11/2026

**Kết luận: `ready_for_user_confirmation`** — 0 blocker · 0 major · 3 minor. 0 USD.

## Cổng tối thiểu
- Diff: `luu_tru_lich.py`, test, `settings.yaml` (trỏ bảng v2), `LichV2.jsx` + `lkh.css`, 66 jpg `anh/khach_san/`, plan, report. Không ngoài phạm vi. `git merge-tree` với main hiện tại: sạch.
- (1) `chon_co_so` — đọc code: vẫn lọc một khu, cắt `[:so]` theo `SO_THEO_MUC` ⇒ ≤ 5; không trường giá; `anh` chỉ đi khi có trong bảng (ảnh `kc` không vào bảng). [Chạy] `dem_chon.py` của B trên code nhánh (worktree riêng của C): 5 sao 3.036 / 3.036, 3 sao 3.036 / 3.036 lịch trung tâm (khớp report); 12 / 140 cơ sở từng hiện; khu biển 36 lịch. Test `test_luu_tru_lich.py` + `test_len_ke_hoach_v2.py` 98 passed. Test đổi kỳ vọng mức thấp (H "đạt chuẩn" cùng cụm ⇒ G1 "1 sao") khớp plan "1 sao trước đạt chuẩn".
- (2) Mẫu 10 ảnh ngẫu nhiên (hạt giống 1411, `/tmp/c_photon/mau10_ks.jpg`): 10 / 10 hợp cơ sở (6 có biển tên đọc được; 4 khu nghỉ dưỡng khớp trang nguồn); 0 mặt người rõ, 0 trẻ em. Bảng: 66 dòng có ảnh = 66 file, 0 thiếu, 0 mồ côi; md5 `a47c9a751a3e` khớp.
- (3) Toạ độ Places: so bảng E — **0 cơ sở đổi khu**; 14 cơ sở đổi `cum_gan` (chỉ đổi thứ tự trong cùng hạng).
- (5) Giao diện: ảnh chỉ nhận `/anh/khach_san/*.jpg` không `..`; link Bản đồ / Tìm phòng kiểm gốc + `_blank` + `noopener`; 0 chữ ghi công (đọc JSX). Playwright của B: dùng lại (C không chạy lại — giao diện chỉ thêm 1 ảnh + 1 link vào thẻ đã kiểm).

## (4) Lệch plan — lý do có đủ không
- Bỏ "mô tả ngắn do code": thẻ đã hiện tên khu (đầu thẻ), hạng, địa chỉ ⇒ câu mô tả chỉ lặp lại ⇒ **đồng ý bỏ**; tiêu chí plan "mô tả 140 / 140" thành không áp — A ghi nhận lệch plan.
- Link Bản đồ theo tên + địa chỉ thay vì toạ độ: hợp lý hơn plan (58 / 140 toạ độ vẫn ước ~1 km) ⇒ đồng ý.
- Sàn Places ≥ 100 trượt (81) — A đã nhận; toạ độ chỉ dùng xếp trong hạng ⇒ tác động nhỏ.

## Minor
- **m-1:** khu biển: 36 lịch gợi ý cùng lúc "Khách sạn nghỉ dưỡng Villa Louise" (Hòa Duân) + "Khu nghỉ dưỡng Villa Louise Beach" (Phú Thuận) — địa chỉ khác nhau nên chưa chắc trùng; nếu là một nơi thì khách thấy lặp. Kiểm khi gộp dòng trùng (B đã ghi việc sau).
- **m-2:** tiêu chí plan "B mở xem 10 ảnh ngẫu nhiên" đã được thay bằng nhìn lại 100 % ảnh "cao" (chặt hơn) — ghi rõ trong report là thay tiêu chí.
- **m-3 (lượt 2 ảnh, chưa có trong nhánh):** theo chốt vòng tự soi ("đếm người dùng thấy gì trước") — chỉ 12 / 140 cơ sở từng hiện và 97,6 % ô cơ sở hiện ra đã có ảnh. Ảnh cho 74 cơ sở còn lại phần lớn không ai thấy ⇒ đề xuất lượt 2 chỉ làm cơ sở **từng hiện** mà thiếu ảnh (report nói chủ yếu một cơ sở 1 sao), trừ khi 140 cơ sở được dùng ở chỗ khác (nêu rõ chỗ đó).

## Nhánh `p9-khach-san-anh2` (lượt 2 ảnh, B) @ `0977a16` — C · 19:01 14/11/2026
**Kết luận: `ready_for_user_confirmation`** — 0 blocker · 0 major · 1 minor.
- Diff: 5 jpg mới + report; code không đổi. `git diff --check` sạch. Bảng `bang_luu_tru_lich_v2.json` md5 `039c3adebb9b` khớp; 71 dòng có ảnh = 71 file trên nhánh, 0 thiếu, 0 mồ côi.
- C mở cả 5 ảnh mới (`/tmp/c_photon/ks2.jpg`): 4 có biển tên đọc được (Holiday Diamond, Khánh Trang, Carnosa, Hồng Thiện I), La Vela từ website riêng của khách sạn; 0 mặt người rõ, 0 trẻ em, 0 số điện thoại đọc được.
- m-1 / m-2 vòng trước: đã ghi trong report — đóng.
- **Main trước khi merge (A hỏi):** [Chạy] `nap_bang_luu_tru` với code main + bảng dùng chung đã sửa: nạp được (140 cơ sở) — luật nạp chỉ kiểm gốc đường ảnh, không kiểm file ⇒ server **không vỡ**; 5 đường ảnh thiếu file trên main ⇒ chỉ thành ảnh hỏng nếu cơ sở đó hiện, mà cả 5 chưa từng hiện trong 3.840 khung (B đếm: ô có ảnh không đổi). Hết khi merge.
- **m-1:** bảng dùng chung trong `data/` sửa tại chỗ trước merge ⇒ main và nhánh lệch nhau một lúc. Đề xuất rẻ: một test như `test_quan_lich` (mọi đường `anh` của bảng có file trong `frontend/public`) — lần sau lệch sẽ đỏ ngay ở main.
