# Review nhánh `p9-quan-kho-cum` `eae898b` (C — +7 quán kho vào bảng quán lịch) · E · 17:32 14/11/2026

Biên bản C: `data/quan_lich_2026-11-14/bien_ban_quan_kho_them.md` (private). Mức nhẹ, 0 USD.

## Kết luận: `ready_for_user_confirmation` — A merge được; 2 minor

## Đã kiểm
- **Nhánh** chỉ đổi comment `settings.yaml` (460 ⇒ 467 quán, md5 `e35d00b6f9fd`) — md5 file thật khớp. Bảng thật qua kiểm khởi động (`nap_bang_quan`: 467 dòng nạp được); `test_quan_lich` + `test_len_ke_hoach_v2` 104 đạt.
- **7 quán mới** (E tính lại khoảng cách tới điểm lịch gần nhất bằng bảng toạ độ điểm): 6 quán trong 0,27 – 1,79 km tới điểm gần nhất, Bánh ép Huệ 0,34 km (lăng Hổ Quyền) ⇒ đúng luật "cụm của điểm gần nhất ≤ 2 km". Toạ độ: 5 "ước" + 1 "vừa" theo file nguồn 13/11; Bánh ép Huệ ước theo số nhà kề (biên bản ghi rõ, sai số vài trăm mét).

## Finding
- **m-1 (nhãn mức toạ độ):** bảng quán lịch **không mang** trường mức toạ độ (`muc_toa_do` có ở file nguồn 13/11 nhưng không chép sang) ⇒ không nhìn bảng mà biết quán nào toạ độ ước. Không hiện ra giao diện (giao diện không in khoảng cách) nên không chặn; nên chép trường này vào bảng (private) ở lần dựng bảng kế để lần đếm / sửa sau phân biệt được.
- **m-2 (cụm ↔ địa chỉ):** 2 quán có địa chỉ một nơi mà gán cụm nơi khác, vì cụm lấy theo điểm lịch gần nhất:
  - một quán ghi "phường Kim Long" ⇒ cụm Kinh thành (gần Đại Nội 1,79 km; điểm cụm khác gần nhất 2,03 km);
  - một quán ghi "phường Thủy Xuân", toạ độ ước trên một đường dài ⇒ cụm Bờ nam (gần Đàn Nam Giao 0,93 km; cụm khác 1,35 km) — C / B đã lưu ý có thể lệch.
  Dòng hiện "Ăn … gần <điểm>" vẫn đúng nghĩa (≤ 2 km); chỉ số "Kim Long 0 %" có thể thấp hơn thật một chút. Không chặn.
