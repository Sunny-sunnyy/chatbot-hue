# Ảnh khách sạn User tự tìm ⇒ bảng lưu trú v6 (E · 15:53 15/11/2026, `date`)

Người làm: E. A giao (User để 10 ảnh ở thư mục private, tên file = tên cơ sở; cơ sở thứ 11 User không tìm được ⇒ để không ảnh). Nhánh `p9-anh-ks-user`. 0 USD.

## 1. Kết quả
- **Ghép 9 / 10 ảnh ⇒ 57 ⇒ 66 / 136 cơ sở có ảnh** (kỳ vọng của A là 67). Bảng mới v6 (private, md5 `e10140f4c4a9`) = v5 + trường ảnh ở đúng 9 dòng; v5 không sửa. So từng dòng v5 ↔ v6: 9 dòng khác, chỉ thêm `anh` + `anh_nguon` ("User cung cấp 15/11/2026"; không có trang nguồn vì User không ghi).
- **1 ảnh CHƯA ghép — cần User / A quyết:** ảnh của một khách sạn 1 sao ở trung tâm (ảnh mặt tiền): **biển hiệu trong ảnh có số điện thoại đọc được** ⇒ phạm luật chọn ảnh (không số điện thoại). Theo lời giao E không tự thay. Đã làm sẵn **bản thử che số** (tô đè phần số trên dải xanh của biển, phần tên + địa chỉ giữ nguyên) ở ô số 10 của tấm ghép — User chọn: dùng bản che / gửi ảnh khác / để trống. Chọn bản che ⇒ thêm 1 dòng vào script, ra 67.
- 9 ảnh còn lại E nhìn từng ảnh: không trẻ em, không người, không số điện thoại. Đều là mặt tiền / toàn cảnh khuôn viên; một ảnh có chữ tên cơ sở in sẵn (đúng tên). E **không tự kiểm được** ảnh có đúng cơ sở hay không (User chọn; luật nới cho ảnh User: mặt tiền / toàn cảnh là được).
- Một ảnh gốc rất nhỏ (299 × 168) ⇒ giữ nguyên cỡ, không phóng to; thẻ sẽ hơi mờ. Một ảnh rất dẹt (480 × 162).
- Ảnh đổi cỡ như ảnh khách sạn đang có: ngang ≤ 480 px, JPEG 82; 17–71 KB / ảnh.
- **Xoá ảnh mồ côi** `590fe0f843.jpg` (của dòng trùng đã gộp ở v5; chỉ còn bảng v4 cũ trỏ). Sau đó: 66 ảnh trong bảng = 66 file, 0 thiếu, 0 mồ côi.
- `settings.yaml`: 1 dòng `lich_trinh_bang_luu_tru` trỏ v6. `dung_trung.py` chạy lại trên v6: `theKhachSanTrung.js` không đổi (tên cơ sở không đổi).

## 2. Hệ quả người dùng thấy (đếm bằng code, 0 USD)
Bộ chọn chỗ ở ưu tiên cơ sở có ảnh trong cùng hạng ⇒ thêm ảnh làm đổi cơ sở được gợi ý. So ô "Nơi ở" v5 ↔ v6 trên 3.840 khung × 4 mức hạng = 15.360 lượt (`tools/so_v5_v6.py`, sửa từ script của C): ô đổi ở **5.926 lượt** (gồm cả lượt chỉ đổi vì cơ sở cũ nay có ảnh). Vào danh sách: một khách sạn 5 sao trung tâm 5.782 lượt, một khách sạn 5 sao khác 179 lượt; ra khỏi danh sách (vẫn ở trang Chỗ ở): bốn khách sạn hạng cao khác (3.036 · 2.567 · 179 · 179 lượt). Đây là hành vi sẵn có của luật xếp, không đổi code.

## 3. Kiểm
| Bước | Kết quả |
|---|---|
| `test_luu_tru_lich.py` + `test_the_khach_san.py`, không khoá / có khoá | 16 đạt / 16 đạt (11 s / 10 s) |
| Nạp bảng v6 bằng `nap_bang_luu_tru` | đạt |
| `npm ci && npm run build` | đạt; `dist/anh/khach_san` 66 file |
| Playwright, test rộng | NOT RUN — nhánh chỉ đổi ảnh + dữ liệu bảng |

Tấm ghép để A nhìn lại 100 % (private): `data/anh_user_2026-11-15_ghep/ghep_anh_se_hien.jpg` (9 ảnh sẽ hiện + ô 10 bản thử che số); ảnh gốc ghép: `ghep_10_goc.jpg`; biên bản tên file ⇒ cơ sở: `bien_ban_ghep.json`; dựng lại: `tools/dung_bang_v6.py <frontend>`.

**Sau merge:** deploy nháp đổi đường bảng lưu trú v5 ⇒ v6 (E làm). **Giải thích ngắn:** 9 khách sạn có thêm ảnh do chính User chọn; một ảnh giữ lại vì trong ảnh có số điện thoại — chờ User chọn cách xử lý.

## 4. Cập nhật 15:55 15/11/2026 (`date`) — ảnh thứ 10 (số ở mục 1–3 là bản 9 ảnh; số hiện hành ở đây)
- A quyết phương án (a): dùng **bản đã che số điện thoại trên biển** cho ảnh mặt tiền khách sạn 1 sao ở trung tâm (tên + địa chỉ trên biển giữ nguyên; vùng che ghi trong `tools/dung_bang_v6.py`, `anh_nguon` của dòng ghi "đã che số điện thoại trên biển"). E nhìn lại ảnh ra (480 × 330): không còn số.
- **Bảng v6 hiện hành: 10 ảnh ⇒ 57 ⇒ 67 / 136, md5 `44d7b14d8fce`** (bản 9 ảnh `e10140f4c4a9` đã bị ghi đè). `settings.yaml` ghi md5 mới. 67 ảnh trong bảng = 67 file.
- Ô "Nơi ở" v5 ↔ v6 (15.360 lượt, 0 USD): đổi ở **8.962 lượt**. Vào: khách sạn 5 sao trung tâm 5.782 · khách sạn 1 sao vừa thêm ảnh 3.575 · một khách sạn 5 sao khác 179. Ra khỏi ô gợi ý (vẫn ở trang Chỗ ở): 3.036 · 2.746 · 2.567 · 539 · 290 · 179 · 179 lượt (bảy cơ sở).
- Kiểm lại: `test_luu_tru_lich.py` + `test_the_khach_san.py` 16 đạt không khoá / 16 đạt có khoá; build đạt (`dist/anh/khach_san` 67 file).
- Giới hạn giữ (A đồng ý): một ảnh gốc nhỏ 299 × 168 (thẻ hơi mờ), một ảnh rất dẹt 480 × 162.
