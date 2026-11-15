# Review — nút dấu cộng trong ô nhập + dán ảnh (`p9-nut-anh-cong` @ `caccfb7`)

E, 19:49 15/11/2026 (`date`). Người làm: C. Một review cả nhánh (đổi thứ người dùng thấy + xử lý thứ người dùng dán). Nền: origin/main `aa0a9ae`.

**Kết luận: ready_for_user_confirmation** — 0 blocker · 0 major · 2 minor (không chặn).

## Đã kiểm

- Diff 3 file `frontend/` + report; `git diff --check` sạch; không file ngoài phạm vi. Luồng gợi ý + xác nhận giữ nguyên từng dòng (chỉ đổi thụt lề).
- Thứ tự hook: `useState`, 2 `useRef`, 2 `useEffect` đều đứng TRƯỚC `if (!bat) return` ⇒ cờ đổi tắt ⇒ bật sau khi tải `/api/tinh_nang` không đổi số hook. Đạt.
- Cờ tắt ⇒ `onPaste: undefined` ⇒ ô gõ dán như cũ; không nút. Đạt (đọc code; C đã chạy ca cờ tắt).
- **Dán thật (E chạy, server tạm của E từ đúng nhánh, 3 lượt):** ghi ảnh PNG vào clipboard của trình duyệt rồi bấm Ctrl+V trong ô nhập ⇒ 3 / 3 lượt gọi `POST /api/anh/ung_vien` kiểu `image/png`, thẻ gợi ý hiện, chữ đang gõ trong ô được giữ nguyên, không chữ rác lọt vào ô; đóng thẻ ⇒ con trỏ về ô nhập. Ca này trước đó mới thử bằng sự kiện dán do script dựng.
- Dán ảnh GIF (kiểu không nhận) ⇒ lời báo "Chọn ảnh JPEG, PNG hoặc WEBP.", 0 lượt gọi API. Đạt.
- Bàn phím: nút cộng nhận focus, có viền focus 3 px riêng; thứ tự Tab: nút cộng ⇒ ô gõ ⇒ nút Hỏi (ô chọn file ẩn không vào vòng Tab). 0 lỗi console.
- Script + kết quả (private): `data/review_nut_anh_cong_2026-11-15/` (`pw_dan_that.py`, `ra/`, `ra1/`, `ra2/`, 3 dòng `anh_metrics`).

## Finding

- **m-1 (minor, không cần sửa trong nhánh):** nút chỉ có dấu cộng; nghĩa "gửi ảnh" chỉ lộ qua `title` / `aria-label` — màn cảm ứng không có chú giải khi rê chuột. Đúng yêu cầu của User (dấu cộng như các ứng dụng chat quen dùng) ⇒ giữ; nếu User thử thấy khó đoán thì đổi hình trong nút, không đổi luồng. Đóng: A ghi vào danh sách User thử.
- **m-2 (minor, chấp nhận):** dán ảnh lúc ảnh trước còn "Đang nhận diện" hoặc lúc đang gửi câu ⇒ bị bỏ qua im lặng (không dán, không báo). Hiếm, không sai dữ liệu. Không cần sửa.

## Ngoài nhánh (báo A, không phải lỗi của C)

1 / 3 lượt dán của E ra "Mình chưa nhận ra ảnh này" vì bước nhận ảnh trả `loi_model`: phần suy luận của model dùng 994 / 1.024 token đầu ra (hai lượt đạt cũng dùng 829 và 929); hai lượt của C trên ảnh khác chỉ 127–213. Cùng một ảnh nhỏ, cùng code nhận ảnh như main ⇒ trần token đầu ra của bước nhận ảnh sát mép với ảnh khó. Mới 3 lượt, một ảnh — là quan sát, chưa phải nguyên nhân đã chứng minh.

Tiền review: 3 lượt nhận ảnh = 0,0021 USD (từ `anh_metrics`). Server tạm cổng 8896 đã tắt, worktree đã gỡ.
