# Nút dấu cộng trong ô nhập + dán ảnh (thay nút chữ "Hỏi bằng ảnh") — implementation (C, 19:45 15/11/2026)

Giao: A, tối 15/11, theo góp ý của User khi thử (nút chữ nằm riêng một hàng tốn chỗ; muốn một dấu cộng trong ô nhập và dán ảnh thẳng vào ô). Nhánh `p9-nut-anh-cong`. Chỉ `frontend/` (3 file). Tiền **0,0007 USD** (2 lượt nhận ảnh thật).

## Đổi gì

| Trước | Sau |
|---|---|
| Nút chữ "Hỏi bằng ảnh" một hàng riêng phía trên ô nhập | Nút tròn dấu cộng 44 px ở mép trái TRONG ô nhập (`aria-label` + `title` "Hỏi bằng ảnh"); bấm ⇒ hộp chọn file như cũ |
| Chỉ chọn file | Thêm: dán ảnh (Ctrl+V) vào ô nhập ⇒ đi đúng luồng cũ |
| Thẻ gợi ý nằm dưới nút | Thẻ gợi ý nằm ngay trên ô nhập (chỗ cũ), không đổi nội dung |

- **Cách làm:** `HoiBangAnh.jsx` từ một thành phần thành hook `useHoiBangAnh` trả ba mảnh — nút (đặt trong ô nhập), thẻ gợi ý (đặt trên ô nhập), hàm `onPaste` (gắn vào ô gõ) — vì nút và thẻ nay ở hai chỗ khác nhau của khung nhập. `chat.jsx` 5 dòng; `index.css` thêm kiểu nút, bỏ kiểu nút cũ.
- **Giữ nguyên:** luồng sau khi có ảnh (gợi ý ≤ 3 tên "có thể sai" ⇒ bấm xác nhận mới hỏi), rào kiểu / cỡ file, route, CSP, mục "Hỏi bằng ảnh" ở Trang chủ / Giới thiệu (câu tả vẫn đúng). Không gói npm mới, không menu xổ, không kéo-thả.
- **Tự quyết (A đồng ý):** dán chỉ coi là dán ẢNH khi clipboard có file ảnh **và không có chữ** — bảng tính / trình soạn văn bản thường chép chữ kèm một ảnh chụp, khi đó vẫn dán chữ như thường. Ảnh dán sai kiểu (vd GIF) ⇒ câu lỗi sẵn có "Chọn ảnh JPEG, PNG hoặc WEBP.". Đang nhận diện một ảnh hoặc đang chờ trả lời ⇒ ảnh dán thêm bị bỏ qua.

## Kiểm [đã chạy] — server tạm cổng 8041 từ worktree nhánh (cwd đã kiểm), Playwright một khổ 1440 + chụp khổ 390

| Phép kiểm | Kết quả |
|---|---|
| Nút chữ cũ | 0 nút |
| Nút dấu cộng | 1 nút, 44 × 44, nằm trong ô nhập, bên trái ô gõ |
| Bấm nút ⇒ chọn ảnh ⇒ gợi ý | ra thẻ gợi ý 2 tên + nút "Không phải các tên này" |
| Dán ảnh (không chữ) ⇒ gợi ý | chặn dán mặc định, ra đúng thẻ như trên |
| Dán chữ thật (Ctrl+V) | chữ vào ô, không thẻ |
| Clipboard có cả chữ lẫn ảnh | không chặn, không thẻ |
| Cờ ảnh tắt (sửa câu trả lời `/api/tinh_nang` trong trình duyệt, 0 USD) | 0 nút, dán ảnh không làm gì, 0 lần gọi API ảnh |
| Lỗi console · yêu cầu ra ngoài | 0 · 0 |
| `npm run build` · `test_static_ui.py` | đạt · 4 passed (8 s) |

- Thời gian: build < 1 s; Playwright 19 s; lượt có phí = 2 ảnh trong chính Playwright.
- **Chưa kiểm / giới hạn:** dán ảnh thử bằng sự kiện dán do script dựng (trình duyệt không cho script ghi ảnh JPEG vào clipboard thật) — User nên thử dán một ảnh chụp màn hình thật; chưa thử Safari / Firefox; không chạy test rộng backend (không chạm backend).
- Ảnh chụp (private): `data/nut_anh_cong_2026-11-15/anh/o_nhap_1440.png`, `goi_y_1440.png`, `o_nhap_390.png`, `trang_390.png`; script `pw_nut_anh.py`, `pw_co_tat.py`; kết quả `ket_qua_pw.json`.
