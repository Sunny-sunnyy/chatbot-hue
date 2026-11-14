# Review trang Trợ lý H1 của B (`p9-gd-h1` @ `d6bc51e`) · E, 14/11/2026

Phạm vi: `chat.jsx` (`TrangTroLy`, bước công cụ thật, ảnh đại diện, "đang gõ"), `tl.css` mới, `App.jsx` (một khối). Cách kiểm: đọc diff; build lại trong worktree của E (JS 117,40 KB gzip); mở `#/tro-ly` trên bản build do FastAPI phục vụ ở 1440 + 390 px (0 lỗi console, không cuộn ngang, có `textarea`). Không chạy lượt có phí: B đã chạy thật 2 khổ màn.

## Kết luận: `changes_requested` (nhẹ) — 0 blocker · 1 major · 3 minor

**Đạt:**
- Bước công cụ chỉ lấy từ sự kiện `status` server đã gửi, đúng thứ tự, gộp bước lặp liền nhau. Lần tìm thứ 2 hiện "tìm thêm"; `n_sources` cộng dồn hiện "có tổng N đoạn". Không bước nào là tự nghĩ ra.
- Giữ `role="status"`, giữ các tên lớp cũ. Hiệu ứng chỉ chạy dưới `.hieu-ung`.
- `App.jsx` chỉ đổi đúng khối trang trợ lý.

**M-1 (major, thuộc ràng buộc plan) — khối "Trợ lý làm được gì" nêu tính năng mà không theo cờ.**
- Hiện mọi lúc: "Xếp lịch", "Xem dự báo thời tiết Huế 7 ngày tới", "Kho chưa có ⇒ tra web". Chỉ dòng ảnh là theo cờ `anh`.
- Plan / GHI_CHU_KHI_CODE ghi rõ: câu về tính năng lấy theo `/api/tinh_nang`, không viết cứng.
- Hôm nay cả ba cờ đều bật nên chưa sai. Nhưng tắt một cờ (vd `tra_web` khi hết tiền Serper) thì trang sẽ hứa điều không có.
- Đóng khi: `TrangTroLy` nhận `tinhNang` (App đã có) và dòng nào cũng theo cờ (`lich_trinh_bieu_mau`, `thoi_tiet`, `tra_web`, `anh`).

**m-1 — trang hẹp hơn mẫu.** `index.css` có `.tro-ly-trang { max-width: 900px }` (rule cũ), nên 2 cột (300 px + khung chat) bị dồn vào 900 px. Ở 1440 px hai bên trống ~270 px, khung chat chỉ rộng ~500 px. Mẫu dùng khung 1280 px. Đóng khi: bỏ / nâng `max-width` cho trang mới (vd `.tro-ly-trang:has(.tl-cot) { max-width: 1280px }` trong `tl.css`, hoặc sửa rule cũ — `index.css` là file chung, B báo E nếu sửa ở đó).

**m-2 — chú thích lạc chỗ** (một phần do E):
- Chú thích của `SourceLine` còn sót một đoạn trong `chat.jsx`, phía trên `WebSection`: "(`bai_id`) ⇒ link sang trang bài…". Lúc E tách `SourceLine` ở đợt 0 đã để sót đoạn này.
- `BuocCongCu` chen vào giữa chú thích "B6 D6" và hàm `WebSection`, nên chú thích B6 giờ nằm trên `BuocCongCu`.
- Đóng khi: dời chú thích về đúng hàm, xoá đoạn của `SourceLine`. E nhận xoá đoạn sót nếu B muốn.

**m-3 — lượt lịch trong chat có thể hiện hai danh sách bước.** Lượt biểu mẫu có `progress` (danh sách bước B5, cũ), giờ có thêm `BuocCongCu` (stage `lich_trinh` = "xếp lịch") khi đang chạy. Lượt lịch giờ chủ yếu hiện ở trang Lên kế hoạch nên ít gặp; trong khung nổi thì vẫn thấy cả hai. Đóng khi: lượt `bieuMau` chỉ hiện một danh sách (giữ `progress` vì chi tiết hơn), hoặc ghi lại là chấp nhận.

Ngoài lề (không phải finding): `style={{ fontSize: 14, … }}` nội tuyến chạy được dưới CSP vì React đặt qua CSSOM. Đưa vào `tl.css` cho đồng bộ thì gọn hơn.

## Kiểm phần sửa `0afcebd` (12:07 14/11/2026)
- M-1: mỗi dòng "Trợ lý làm được gì" theo cờ (`lich_trinh_bieu_mau` / `len_ke_hoach_v2`, `thoi_tiet`, `anh`, `tra_web`). `TrangTroLy` nhận `tinhNang`, App chỉ đổi một prop. **Đóng.**
- m-1: `max-width` 1280 ghi đè rule cũ trong `tl.css`. **Đóng.**
- m-2: đoạn sót của `SourceLine` đã bỏ, chú thích B6 về đúng chỗ. **Đóng.**
- m-3: lượt có `progress` thì không vẽ `BuocCongCu` / dòng "Các bước". **Đóng.**
- E build lại (gồm `.ics` `9f086d2`) và mở `#/tro-ly` ở 1440 + 390: 0 lỗi console, không cuộn ngang. **Kết luận: `ready_for_user_confirmation`, 0 finding mở.**
