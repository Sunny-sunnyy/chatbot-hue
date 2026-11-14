# Review nhánh `p9-anh-lich-thieu` `92e7210` (C — ảnh lịch 24 ⇒ 33 / 34 điểm) · E · 17:23 14/11/2026

Mức nhẹ, 0 USD.

## Kết luận: `ready_for_user_confirmation` — A merge được; 2 minor

## Đã kiểm
- **Phạm vi:** `settings.yaml` trỏ `bang_anh_v2.json`, `lich_trinh_v2.nap_bang_anh`, `LichV2.jsx` (`anhHopLe` chỉ còn kiểm `src` dưới `/anh/lich/`), 9 file ảnh, test. Không chạm tin nhắn gửi model.
- **Luật kiểm bảng ảnh vẫn chặn dòng Commons thiếu ghi công** (E thử trên bảng thật, sửa một dòng Commons): thiếu tác giả ⇒ chặn; thiếu giấy phép ⇒ chặn; **gắn `nguon: "web"` cho dòng có trang Commons mà thiếu tác giả ⇒ vẫn chặn** (không lách được bằng cách đổi nhãn). Ảnh web cần `nguon: "web"` + trang `https://` (test chặn `http://`, `javascript:`, trang lạ không nhãn).
- **Bảng thật nạp được:** 33 / 34 điểm có ảnh; thiếu `bien_thuan_an`. Giao diện chỉ vẽ file tự host — trình duyệt không tải gì từ trang nguồn.
- **Ảnh đúng chủ thể** (E xem cả 9 ảnh mới): bảo tàng Hồ Chí Minh (biển tên trên toà nhà), không gian lưu niệm Lê Bá Đảng (toà nhà trắng trên đồi), trung tâm nghệ thuật Lê Bá Đảng (biển tên), phố Tây và phố Hai Bà Trưng (phố đêm), phố đi bộ Nguyễn Đình Chiểu (cổng phố đi bộ), đồi Vọng Cảnh (sông nhìn từ đồi), thác Nhị Hồ (thác) ⇒ hợp.
- **Test:** `test_len_ke_hoach_v2` + `test_cong_dot_1` 112 đạt (worktree sạch, không khoá).

## Finding
- **m-1:** ảnh "đồi Thiên An" là toà rồng của **hồ Thủy Tiên** (công viên nước bỏ hoang cạnh đồi). Bài kho của đồi có mục về hồ Thủy Tiên nên không sai hẳn, nhưng người xem thấy tên "Đồi Thiên An" cạnh ảnh con rồng sẽ hiểu đó là chính ngọn đồi. Đóng khi: thêm `chu_thich` (vd "Hồ Thủy Tiên dưới chân đồi") để `alt` nói đúng, hoặc chọn ảnh đồi thông / đan viện.
- **m-2:** 2 dòng ảnh web có `trang` chỉ là trang chủ tên miền (đồi Vọng Cảnh, thác Nhị Hồ) ⇒ khi cần gỡ ảnh theo yêu cầu thì khó tìm lại trang chứa ảnh. Ghi trang chứa ảnh thật trong bảng (private) nếu còn; không chặn.
