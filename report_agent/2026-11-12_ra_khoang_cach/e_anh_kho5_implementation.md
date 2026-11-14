# Ảnh Khám phá cho 23 bài ghi kho 5 · E (+ B phần món) · 19:51 14/11/2026

- Nhánh `p9-anh-kho5`. Việc A giao. Chia việc: B làm 10 bài món, E làm 13 bài địa điểm và gộp cả hai vào một nhánh.
- Tiền:
  - E: Serper 23 lượt ≈ 0,023 USD (9 lượt bị 429 nên phải chạy lại);
  - B: Serper 10 lượt ≈ 0,01 USD;
  - Commons miễn phí, agent con tính vào quota Claude.

## Kết quả
| | Main (sau ghi kho 5) | Nhánh này |
|---|---|---|
| Bài Khám phá có ảnh | 218 / 247 | **238 / 247** |
| Ảnh `kc` | 49 | 50 |
| Ảnh hiện được cạnh câu trả lời | 169 | **188** |

- **13 bài địa điểm ⇒ 10 bài có ảnh:**
  - 1 agent con chọn theo `BRIEF_CHON.md`. Luật: ảnh tự nhận ra được nơi, hoặc ảnh Commons có chú thích của tác giả ghi đúng tên nơi.
  - E nhìn cả 10 ảnh:
    - 6 ảnh có biển tên hoặc công trình đặc trưng đọc được;
    - 4 ảnh Commons có chú thích của tác giả ghi đúng tên nơi.
  - 9 ảnh không `kc`. Ảnh cầu sắt gắn `kc`: agent chấm "vừa", có dấu nước nhỏ ở góc, không rõ chụp nhịp cầu nào.
  - 3 bài vẫn trống: không ảnh nào nhận ra được nơi (chỉ bản đồ, cảnh cồn chụp trên cao không có tên, nón lá chung chung).
- **10 bài món ⇒ 10 / 10 có ảnh:** B chọn và nhìn 100 % (đúng món là đủ). E xem lại 3 tấm ghép của B: đều đúng món, không có người rõ mặt, trẻ em hay số điện thoại.

## Kiểm [Chạy]
- Script sinh `anhBai.js` (đọc thêm bảng v6): 238 ảnh, 50 `kc`; assert không chép chuỗi trùng kho đạt.
- 9 trang nguồn trùng nguồn bài kho được đổi về trang chủ tên miền, như luật cũ.
- 0 file ảnh mồ côi.
- `npm run build` đạt.
- pytest `test_cong_dot_1` + `test_static_ui` + `test_anh_tra_loi` 27 đạt (37 s).
- Không Playwright: không đổi giao diện.

## Hồ sơ (private)
- `data/anh_kho5_2026-11-14/`: `tools/tim.py`, `ung_vien.json`, `bang_ghep/`, `BRIEF_CHON.md`, `chon.json`, `bang_anh_kham_pha_v6.json`;
- phần món của B: `data/mon_an_2026-11-14/anh/`.
