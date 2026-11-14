# Review đợt 1 giao diện của C (`p9-gd-h1` @ `d72e7f0`) · E, 14/11/2026

Phạm vi: `KhamPha.jsx` (danh sách, trang bài), `GioiThieu.jsx`, `anhBai.js`, `kp.css`, `gt.css`.

Cách kiểm:
- Đọc hết 5 file, so với bản trước (`d72e7f0^`).
- Build lại trong worktree của E, FastAPI phục vụ ở cổng 8871.
- Đo thật:
  - Gọi `/api/kham_pha/bai` cho cả **207 bài**, rồi chạy lại đúng luật `tachThongTin` bằng Python.
  - Playwright: (1) bắt lúc trình duyệt chụp View Transition; (2) mở 4 route + trang bài ở 1440 / 390, xem lỗi console và cuộn ngang.
- 0 USD.

## Kết luận: `changes_requested` — 0 blocker · 2 major · 2 minor

**Đạt:**
- Tìm bỏ dấu và lọc lĩnh vực / loại có số đếm thật.
- Ô giữ chỗ chống CLS.
- Bài không có ảnh: ô màu + biểu tượng, không mượn ảnh của bài khác.
- `anhBai.js` dùng khoá băm, không ghi đường dẫn file kho vào repo.
- Ghi công ảnh đủ: tác giả, link giấy phép, trang Commons, "đã thu nhỏ".
- Nút "Báo thông tin chưa đúng" và luật "mã bài phải có trong danh sách rồi mới gọi server" vẫn giữ.
- Các câu về ảnh / bản đồ theo cờ.
- Đo trên 4 route + trang bài ở 1440 và 390: 0 lỗi console, không cuộn ngang.

**M-1 (major) — thẻ "Thông tin nhanh" làm mất nội dung bài.**
- Cách code chạy: `tachThongTin` **xoá cả mục** "Thông tin chung" khỏi thân bài, nhưng thẻ bên phải chỉ hiện các dòng có dạng `- **Tên:** giá trị`, và chỉ 7 dòng đầu.
- Đo trên 207 bài thật: 103 bài có thẻ. Trong đó:
  - **51 bài mất dòng.** Tổng số dòng mất: 179 dòng thụt đầu (danh sách con), 71 dòng `- **Tên:**` để trống vì giá trị nằm ở danh sách con bên dưới, 26 gạch đầu dòng khác.
  - **29 bài có hơn 7 dòng**, phần từ dòng thứ 8 trở đi bị cắt.
- Vì sao nặng: danh sách con thường chính là giờ mở cửa theo mùa hay giá vé theo nhóm khách. Người đọc chỉ thấy "Giờ mở cửa:" mà không có giờ, cả ở thân bài lẫn ở thẻ.
- Đóng khi bài nào cũng không mất chữ. Một trong hai cách:
  - (a) Chỉ tách khi **mọi** dòng của mục đều khớp và số dòng ≤ 7. Không đạt thì giữ nguyên mục trong thân bài và không vẽ thẻ.
  - (b) Thẻ nhận cả danh sách con: hiện dưới `dd`, không giới hạn 7 dòng.
- Kiểm lại bằng script của E (`/tmp/e_rv/kiem_tach.py`, gọi API thật), mục tiêu: "bài mất dòng 0, bài bị cắt 0".

**M-2 (major, cùng loại M-1 của B) — "Trợ lý làm được gì" ở Giới thiệu hứa tính năng mà không theo cờ.**
- Thẻ "Lên kế hoạch" và "Tra thêm trên web" luôn hiện.
- Bản cũ có điều kiện bằng lời: "(khi tính năng Lên kế hoạch bật)", "có thể tra thêm". Bản mới bỏ điều kiện đó.
- Hôm nay mọi cờ đều bật nên chưa sai. Nhưng tắt `tra_web` (vd khi hết tiền Serper) hay tắt `lich_trinh_bieu_mau` thì trang sẽ hứa điều không có.
- Đóng khi: `GioiThieu` nhận `tinhNang`, thẻ "Lên kế hoạch" theo `lich_trinh_bieu_mau`, thẻ "Tra thêm trên web" theo `tra_web`. App chỉ đổi một prop. B đã làm đúng như vậy ở `0afcebd`.

**m-1 — hiệu ứng "ảnh thẻ bay sang ảnh đầu bài" không chạy.**
- Đo: lúc View Transition chụp trạng thái mới, trang bài còn là khung chờ (bài chưa tải về), nên có **0** phần tử mang tên `kp-anh-…`. Kết quả: trình duyệt chỉ mờ chuyển cả trang, không có ảnh nào bay.
- Đo bằng `/tmp/e_rv/kiem_vt.py`, bấm thẻ có ảnh ở `#/kham-pha/heritages`, máy có `html.hieu-ung`.
- Commit ghi hiệu ứng này là "đã làm", nên cần sửa hoặc ghi lại cho đúng.
- Đóng khi khung chờ vẽ sẵn ảnh thật. `anhCuaBai(baiId)` đã biết ảnh ngay, không cần chờ tải. Đặt `<img>` cùng `viewTransitionName` vào `kp2-ben-anh` của khung chờ, thay cho ô `kp2-cho-anh`. Làm vậy còn đỡ một lần ảnh nhảy lúc bài tải xong.

**m-2 — trang "Khám phá" (tất cả) không báo lỗi khi danh sách tải hỏng.**
- `App.jsx:109` gọi `<KhamPha bai={bai} />` mà không truyền `loi={baiLoi}`. Route theo lĩnh vực thì có truyền.
- Hậu quả: khi `/api/kham_pha` lỗi, `bai` mãi là `null`, trang hiện 8 ô chờ `aria-busy` mãi, không có chữ báo lỗi.
- Đóng khi: truyền thêm `loi={baiLoi}`. Khi có lỗi thì không vẽ ô chờ.

Ngoài lề (không phải finding):
- Dòng "Giờ mở cửa, giá vé có thể đã đổi" hiện cả ở bài món ăn. Có thể đổi chữ theo lĩnh vực nếu C muốn.
- Ở trang chủ, ô thời tiết và phần CLS của E: C đã đo lại `6f37756` và đạt.

## Kiểm phần sửa `ff2ebe9` (12:22 14/11/2026)
- M-1: `tachThongTin` chỉ tách khi mọi dòng của mục khớp `- **Tên:** giá trị` và có 2–7 dòng. E chạy lại script trên 207 bài qua API thật: 28 bài có thẻ, **0 bài mất dòng, 0 bài bị cắt**. **Đóng.**
- M-2: `GioiThieu` nhận `tinhNang`. Các thẻ "Lên kế hoạch" / "Tra thêm trên web" / "Hỏi bằng ảnh" theo cờ `lich_trinh_bieu_mau` / `tra_web` / `anh`. **Đóng.**
- m-1: chạy lại `kiem_vt.py`. Lúc View Transition chụp, trang mới có **1** phần tử `kp-anh-…` (trước là 0) ⇒ ảnh bay được. **Đóng.**
- m-2: `App.jsx:109` đã truyền `loi={baiLoi}`. **Đóng.**
- Build lại đạt. **Kết luận: `ready_for_user_confirmation`, 0 finding mở.**
