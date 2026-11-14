# Review: ảnh dưới câu trả lời trợ lý (E, nhánh `p9-anh-tra-loi` `e4c5ec0`)

Cập nhật: 15:53 14/11/2026 (C). Mức nhẹ. Kết luận: **ready_for_user_confirmation**, 0 finding chặn.

## Đã kiểm
- **Diff:** 5 file, đúng phạm vi: chat.jsx, tl.css, anhBai.js, anhTraLoi.js mới, test node. Không đổi backend, không đổi chuỗi gửi model.
- **Luật do code quyết** (`anhTraLoi.js`):
  - Chỉ khi lượt đã xong, trả lời bằng kho, không từ chối, không mục web, không lịch, không hỏi lại.
  - Mọi nguồn được trích phải thuộc đúng một bài, và bài đó thuộc loại một nơi / món.
  - Ảnh có `kc` (người nhìn không chắc ảnh đúng nơi) ⇒ không hiện.
  - Các trường dùng để quyết (`outcome`, `tuChoiKho`, `suaThe`, `lichV2`, `clarify`, `web`, `lich`) đều có thật trong `chat.jsx`, được gán ở sự kiện `done`.
- **`anhBai.js`:** 29 dòng thêm `"kc": 1`, khớp 29 ảnh `minhHoa` trong bảng gốc. Bộ sinh `dung_anh_bai_js.py` đã được E sửa theo (dòng 79–81) ⇒ C sinh lại lần sau vẫn giữ `kc`.
- **Ảnh chụp của E** (`anh_tra_loi_1411/tro_ly_390.png`): một ảnh đúng nơi dưới câu trả lời, khung tỉ lệ cố định, bấm mở bài.

## Ghi nhận (không chặn)
- `test_anh_tra_loi.py` đọc build record ở `data/` (private) ⇒ bản clone không có `data/` sẽ lỗi ở bước tìm mã. Giống các test chunker đọc mẫu kho; chấp nhận được.
- Thứ tự merge: nhánh ảnh v3 của C (đang làm) sinh lại `anhBai.js` ⇒ C rebase lên sau khi nhánh này vào main.
