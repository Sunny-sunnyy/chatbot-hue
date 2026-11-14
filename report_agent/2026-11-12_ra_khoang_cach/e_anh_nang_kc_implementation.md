# Nâng ảnh "không chắc" (kc) thành ảnh chắc (đã sửa theo review C) — bài một nơi / món / quán · E · 18:44 14/11/2026

- Nhánh `p9-anh-kc`.
- Việc A giao. Lý do: User muốn "ảnh đầy đủ", mà ảnh `kc` không hiện cạnh câu trả lời trợ lý.
- Tiền: **0 USD** (Codex tính vào gói ChatGPT; không gọi Serper).
- Tiêu chí ghi trước: `data/anh_nang_kc_2026-11-14/TIEU_CHI.md` (private).

## Kết quả
| | Main | Nhánh này |
|---|---|---|
| Ảnh `kc` | 57 | **49** |
| Ảnh hiện được cạnh câu trả lời | 161 | **169** |
| Bài có ảnh | 218 / 224 | 218 / 224 |

Phạm vi là 37 bài một nơi đang `kc`; 20 bài chủ đề (vé, dịch vụ, cẩm nang) vẫn luôn `kc`. Đã nâng **8 / 37** bài, sau khi sửa theo review C (`c_review_anh_kc.md`). Bản đầu nâng 18 bài.

## Thứ tự làm (đếm trước, 0 USD)
- Cách xếp: đếm số câu trong bộ T1 (158 câu, bản sau ghi kho 4) có bài lọt top-10; hoà thì xếp quán có trong bảng quán của lịch lên trước. Kết quả ở `thu_tu.json`.
- 23 / 37 bài từng lọt top-10, nhiều nhất 4 / 158 câu ⇒ lợi ích của việc này có giới hạn.

## Lượt 1 — luật nguồn: 13 bài ⇒ còn 3 sau review C (giữ nguyên ảnh, bỏ `kc`)
- Áp cho ảnh đang dùng lấy từ trang chính thức: `hue.gov.vn`, cổng du lịch tỉnh `khamphahue.com.vn`, trang riêng của nhà hàng, trang chi nhánh chính thức (AEON Huế), hoặc trang bán hàng ShopeeFood do chính quán đăng.
- E nhìn cả 15 ảnh theo luật bỏ ảnh, đọc lại cả danh sách luật (bài học từ v4b).
- Giữ `kc` 2 ảnh:
  - một quán: nhiều người rõ mặt là trọng tâm;
  - biển Thuận An: có trẻ em nhận ra được.
- **Review C M-1 (E nhận):**
  - 10 / 13 ảnh chỉ là món hoặc ly chung, hoặc là cảnh không nhận ra được nơi. Một trang chính thức hay trang bán hàng (ảnh người bán tự đăng, có thể là ảnh mẫu) không đủ khi chính ảnh không nhận ra được quán. Trong 10 ảnh này có cả ảnh múa lân mà E đã bác ở v4.
  - ⇒ 10 ảnh giữ `kc`. Còn 3 ảnh được nâng: 2 ảnh mặt tiền nhà hàng nhận ra được (cổng du lịch tỉnh) và 1 ảnh từ website riêng của quán.
  - Luật sau sửa: nguồn chỉ đủ khi ảnh tự nhận ra được quán / nơi. Riêng bài MÓN thì đúng món là đủ.
- Không dùng agent con ở lượt này: việc là áp luật nguồn, không có nhiều ứng viên để chọn. C review là con mắt thứ hai.

## Lượt 2 — Codex chỉ trang chính thức (5 bài, ảnh mới, không `kc`)
- Codex tra 24 bài còn lại (407 s, 37 trang mở, 0 URL tự khai). Script `tools/lay_anh_muc.py` lấy ảnh đứng ngay sau chỗ nhắc tên mục (trang tổng hợp), hoặc ảnh đại diện og:image (trang riêng). Thu được 49 ảnh; E nhìn cả 49.
- Nhận 5 ảnh, đều từ cổng du lịch tỉnh:
  - Khu phố Tây: cổng "Phố đi bộ – Walking Street" đọc rõ;
  - bánh ép (món): tay chấm nước, không thấy mặt;
  - một quán cà phê: sân thượng, tên quán có trên ảnh;
  - bãi Hàm Rồng: không người;
  - bãi Lộc Bình: người ở xa, nhỏ.
- Bác các ảnh còn lại:
  - ảnh đồ hoạ thông tin (infographic) nhiều quán;
  - ảnh quảng cáo bên lề trang;
  - ảnh có trẻ em hoặc người rõ mặt;
  - ảnh không chắc thuộc đúng mục: từ khoá ngắn khớp nhầm ở nhiều chỗ trong trang.

## Dừng — 29 bài còn `kc` (19 bài lúc dừng + 10 bài review C trả về)
- Lý do dừng: các trang loại a / b Codex chỉ đã dùng hết. Muốn nâng thêm phải tìm tay theo từng quán; tốn nhiều thời gian mà mỗi bài chỉ lọt ≤ 4 / 158 câu T1.
- Từng bài kèm lý do: `bang_anh_kham_pha_v5.json` khoá `giu`.

## Kiểm [Chạy]
- Script sinh `anhBai.js` (thêm đọc v5): 218 ảnh, 49 `kc`; assert không chép chuỗi trùng kho đạt.
- 0 file ảnh mồ côi trong `kp/`.
- `npm run build` đạt.
- pytest `test_cong_dot_1` + `test_static_ui` + `test_anh_tra_loi` 27 đạt (39 s).
- Không Playwright: không đổi giao diện; chỉ đổi 5 file ảnh và cờ `kc`.

## Hồ sơ (private) `data/anh_nang_kc_2026-11-14/`
- `TIEU_CHI.md`, `thu_tu.json`, `ung_vien_nguon.json`;
- `codex_trang.json`, `ung_vien_muc.json`, `bang_anh_kham_pha_v5.json`, `tools/`;
- kết quả Codex: `data/tra_cuu_cli/2026-11-14_anh-kc-24/`.
