# Ảnh đính kèm tin nhắn — bấm Hỏi mới xử lý — implementation (C, 20:44 15/11/2026)

Giao: A, tối 15/11, theo lời User: "khi tải ảnh lên hệ thống không làm gì cả; người dùng nhập câu hỏi, bấm Hỏi thì hệ thống mới bắt đầu xử lý". Nhánh `p9-anh-dinh-kem`. Chỉ `frontend/` (3 file, +48 / −15 dòng). Tiền **0,0019 USD** (2 lượt nhận ảnh + 2 lượt hỏi thật). Nháp 3 phương án: `data/anh_dinh_kem_2026-11-15/nhap_thiet_ke.md` (private) — User không chọn nguyên phương án nào; làm theo mô tả A chốt.

## Luồng mới

1. Chọn ảnh (nút dấu cộng) hoặc dán ảnh ⇒ ảnh nhỏ 44 px nằm trong ô nhập, có nút × "Bỏ ảnh". **Chưa gọi API nào.** Kiểu / cỡ file sai ⇒ báo ngay (kiểm ở trình duyệt). Một ảnh mỗi câu; ảnh mới thay ảnh cũ.
2. Gõ câu (hoặc để trống) ⇒ bấm Hỏi / Enter ⇒ **lúc này** mới gửi ảnh đi nhận diện; thẻ trên ô nhập ghi "Đang xem ảnh…".
3. Thẻ "Trong ảnh là (có thể sai) — chọn đúng tên:" + ≤ 3 tên + "Không phải các tên này — tôi gõ tên" (một tên vẫn hiện thẻ). Chữ đang gõ vẫn nằm trong ô.
4. Bấm tên ⇒ gửi "<câu đã gõ> (Trong ảnh: <tên>)"; ô rỗng ⇒ "Giới thiệu về <tên>" (khuôn ghép câu không đổi).
5. Chưa nhận ra / lỗi ⇒ lời báo, ảnh gỡ, chữ đã gõ giữ nguyên; bấm Hỏi lần nữa ⇒ câu chữ đi như câu thường.

- Bấm Hỏi khi thẻ đang chờ hoặc đang chờ chọn tên ⇒ không gửi câu trần (phải chọn tên hoặc "Không phải…").
- **Không đổi:** route nhận ảnh, lời dặn, rào server, chuỗi gửi model, mục "Hỏi bằng ảnh" ở Trang chủ / Giới thiệu (câu tả vẫn đúng). Cờ ảnh tắt ⇒ không nút, dán ảnh không làm gì (đường cũ, không chạm).
- Cách làm: hook `useHoiBangAnh` thêm trạng thái "đã đính kèm" + hai mảnh trả ra: `kem` (ảnh nhỏ) và `gui()` (ô nhập gọi khi bấm Hỏi).

## Kiểm [đã chạy] — server tạm cổng 8041 từ worktree nhánh (cwd đã kiểm), Playwright 1440

| Phép kiểm | Kết quả |
|---|---|
| Chọn ảnh | 1 ảnh nhỏ trong ô nhập · 0 thẻ · **0 lần gọi API ảnh** · 0 lần gọi chat |
| Bấm × | ảnh gỡ, chữ đã gõ còn nguyên, 0 lần gọi API |
| Dán ảnh rồi chờ | 0 lần gọi API trước khi bấm Hỏi |
| Bấm Hỏi | có dòng "Đang xem ảnh…" ⇒ đúng 1 lần gọi API ảnh ⇒ thẻ 2 tên; chữ còn trong ô; chưa gửi chat |
| Bấm Hỏi lần nữa khi thẻ mở | không gửi gì thêm |
| Bấm tên | câu gửi đúng khuôn "<câu đã gõ> (Trong ảnh: <tên>)"; ô nhập trống |
| Ảnh + ô rỗng ⇒ Hỏi ⇒ bấm tên | câu gửi "Giới thiệu về <tên>" |
| Dán file kiểu sai | lời báo ngay, 0 lần gọi API, không có ảnh nhỏ |
| Chưa nhận ra (chặn câu trả lời của route ảnh trong trình duyệt, 0 USD; khổ 390) | lời báo, ảnh gỡ, chữ còn nguyên; bấm Hỏi ⇒ câu chữ đi như thường, thẻ đóng |
| Lỗi console | 0 |
| `npm run build` · `test_static_ui.py` | đạt · 4 passed (8 s) |

- Thời gian: build < 1 s; Playwright ~60 s.
- **Chưa kiểm / giới hạn:** cờ ảnh tắt không chạy lại (nhánh không chạm đường đó; đã kiểm ở nhánh nút dấu cộng); dán ảnh bằng sự kiện do script dựng (E đã thử dán PNG thật ở nhánh trước); Safari / Firefox chưa thử; nhận diện mất vài giây tới ~12 giây (E đo) và nay người dùng chờ SAU khi bấm Hỏi — hệ quả của lựa chọn "không xử lý lúc tải lên".
- Ảnh chụp (private): `data/anh_dinh_kem_2026-11-15/anh/dinh_kem_1440.png` (ảnh nhỏ trong ô nhập), `the_ten_1440.png` (thẻ tên sau khi bấm Hỏi), `dinh_kem_390.png`, `trang_1440.png`; script `pw_dinh_kem.py`, `pw_khong_nhan_ra.py`.

## Sau review của B — hai minor (nhánh `p9-anh-dinh-kem-2`, C 20:49 15/11/2026, 0 USD)

- **m-1:** thẻ tên đang mở mà bấm Hỏi / Enter ⇒ trước không có gì xảy ra (dễ tưởng treo) ⇒ nay thẻ hiện thêm dòng "Chọn một tên ở trên để mình trả lời."; vẫn không gửi câu trần, chữ đang gõ giữ nguyên.
- **m-2:** nút "Cuộc trò chuyện mới" gỡ ảnh đang đính kèm và đóng thẻ đang mở.
- **Giới hạn giữ (A chốt không làm tối nay):** chưa có nút huỷ lúc "Đang xem ảnh…".
- **Kiểm [đã chạy]** (Playwright 1440, chặn route ảnh + chat trong trình duyệt nên 0 USD; `data/anh_dinh_kem_2026-11-15/pw_hai_minor.py`): trước khi bấm Hỏi không có dòng nhắc ⇒ sau khi gõ câu khác + Enter có dòng nhắc, 0 câu gửi đi, chữ còn; bấm tên ⇒ gửi "<câu vừa gõ> (Trong ảnh: <tên>)"; "Cuộc trò chuyện mới" khi có ảnh đính kèm ⇒ 0 ảnh nhỏ, 0 thẻ; khi thẻ đang mở ⇒ 0 ảnh nhỏ, 0 thẻ; 0 lỗi console; build + `test_static_ui.py` 4 passed. Diff 9 dòng thêm / 4 dòng bớt, 2 file.
