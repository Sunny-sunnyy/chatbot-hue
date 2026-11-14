# Rà trang "Lên kế hoạch": code trên main ↔ bản mẫu H1 (B, 15:01 14/11/2026)

Người làm: B (`hue-rag-6b`). A giao lúc mở lại phiên 14/11. Việc chỉ đọc, không sửa code giao diện (E đang sửa trang này).
- **Tiền:** 3 lượt xếp lịch thật để chụp và dò, mỗi lượt ≈ 0,0007 USD (log `chat_metrics` ghi 0,000726 cho lượt đầu), tổng ≈ 0,002 USD.
- **Cách làm:** server tạm của B từ `main` `4e6e1ff` (cổng 8877, bản build 13:56). Bản mẫu `data/ui_mau_2026-11-14/h1/len_ke_hoach.html` (cổng 8879).
- **Hồ sơ:** Playwright 1440 + 390 ở `data/ra_lkh_2026-11-14/` (`pw_ra_lkh.py`, `pw_do_mo.py`, `ket_qua.json`, `do_mo_*.json`, ảnh `anh/`).

## 1. Khối "hiện dần" có kẹt mờ không — KHÔNG [Chạy]
- Chromium dùng `animation-timeline: view()`: độ đậm của khối gắn với vị trí cuộn. Ảnh chụp cả trang dùng khung nhìn 900 px, nên khối nằm dưới khung nhìn bị chụp ở trạng thái "chưa vào" (mờ / trống). Kể cả bản mẫu cũng mờ 4 / 6 khối. Vậy vùng trống trong ảnh của A là do cách chụp, không phải lỗi.
- **Dò thật:** cuộn từng bước 100 px qua cả trang và ghi độ đậm lớn nhất mỗi khối đạt được.
  - Lên kế hoạch sau khi xếp lịch 3 ngày: 3 / 3 khối đạt 1,0 ở cả 1440 và 390.
  - Giới thiệu: 9 / 9 khối đạt 1,0 ở 1440.
  - 0 lỗi console.
- **Hệ quả cho người chụp ảnh trình User:** cần bật giả lập giảm chuyển động (`reduced_motion="reduce"`) hoặc cuộn tới từng khối rồi chụp theo khung nhìn. Ảnh chụp cả trang thường sẽ luôn ra "trống".

## 2. Chỗ thiếu so với bản mẫu

| # | Chỗ | Bản mẫu | Code trên main | Dữ liệu có sẵn? |
|---|---|---|---|---|
| 1 | **Lúc chưa xếp lịch** (chỗ thiếu lớn nhất) | cột phải là cả lịch 3 ngày (dòng thời gian, ảnh, sông) | khung nét đứt "Lịch của bạn sẽ hiện ở đây" + 3 dòng. Ở 1440, cột phải trống ~900 px dưới khung. Ở 390, khung nằm **dưới** nút Xếp lịch, người dùng gần như không thấy | có: `xep_v2` tham số cố định (E đang làm "lịch mẫu") |
| 2 | Dòng phụ mỗi ngày | "Thứ Bảy 28/11 · Kinh thành và phía đông" | chỉ "Ngày N" (+ ngày tháng khi có ngày đi) | có: `cum` trong `diem_v8.json` có tên cụm (vd "Kinh thành và bờ bắc sông Hương") — code ghép tên cụm của các điểm trong ngày |
| 3 | Màu chấm theo **loại điểm** (di tích / thiên nhiên / nghệ thuật / ăn / tối) | 5 màu theo loại | màu theo **buổi** (sáng / chiều / tối) | có: `loai` của từng điểm trong bảng |
| 4 | Thanh "đi tới ngày" (Tổng quan · Ngày 1 · Ngày 2…) | có, dạng nút viên | không có; Tổng quan có link từng ngày | không cần dữ liệu mới |
| 5 | Ô "Thời tiết" trong thanh đầu lịch | có ("chưa có dự báo (ngoài 7 ngày)") | không có ô này; ghi chú dự báo nằm dưới từng ngày | có (ghi chú `du_bao`) |
| 6 | Nút "Sửa" ngay trong dòng "Mình hiểu…" | có | chỉ có nút "Sửa — điền lại biểu mẫu" ở cuối lịch, phải cuộn hết lịch mới thấy | không cần |
| 7 | Nguồn | danh sách đánh số 1..14 khớp `[n]` trong câu | một dòng chữ "Nguồn: a · b · c…" | có |
| 8 | Biểu tượng nhỏ ở tiêu đề từng nhóm biểu mẫu (Ai đi? / Đi bao lâu?…) | có | không có | không cần |
| 9 | Nút "Xếp lịch" + tóm tắt gói trong một thẻ | có (thẻ `lc-chot`) | chữ tóm tắt và nút nằm trần dưới biểu mẫu | không cần |
| 10 | Dòng ghi công dưới ảnh của từng điểm | có trong mẫu | có | User cấm ⇒ **bỏ** (E đang làm; mẫu lệch yêu cầu mới) |

Code **có mà bản mẫu không có**:
- nút `.ics`;
- bản đồ thật (mẫu chỉ vẽ ô giữ chỗ);
- khối "Đã đổi / Không đổi được" khi sửa lịch bằng lời;
- sông vẽ dần nối các ngày (đã có, theo `c_nghien_cuu_wow.md` mẫu 16).

Phần giống mẫu: dải đầu có ảnh (cao 210 px, mẫu 230 px), biểu mẫu dính khi cuộn (sticky) ở 1440, ô sở thích có ảnh, kiểu đi có chấm, không cuộn ngang ở cả hai khổ.

## 3. Đề xuất 2–3 điểm nhấn (đều 0 USD, không thư viện, chờ nhóm bàn)
1. **Lịch mẫu "Ví dụ" khi chưa xếp** (chỗ #1; E đang làm). Ở 390 nên đặt **phía trên** biểu mẫu, hoặc thêm một dải "xem lịch ví dụ ↓" ngay dưới dải đầu, vì trên điện thoại khung xem trước đang nằm sau nút Xếp lịch. Thêm một nút "Xếp lịch như ví dụ" để điền sẵn biểu mẫu bằng tham số của lịch mẫu.
2. **Mỗi ngày có "tên chặng" + màu theo loại điểm** (#2 + #3). Code dựng từ `cum` và `loai`, model không viết gì. Lịch nhìn thành "hành trình theo vùng" thay vì một danh sách giờ. Đây là phần mẫu trông "sống" hơn code nhiều nhất, lấy từ dữ liệu sẵn có.
3. **Lịch hiện ra có nhịp:** khi lịch về, các ngày lần lượt hiện (mỗi ngày trễ ~120 ms), ảnh điểm lộ dần qua mặt nạ (`clip-path`, mẫu 4 của C). Thêm thanh "đi tới ngày" dính khi cuộn (#4). Máy giảm chuyển động ⇒ hiện sẵn.

Nhỏ, gộp vào lượt sửa của E: thêm nút "Sửa" vào dòng "Mình hiểu" (#6) và đánh số nguồn (#7).

## 4. Giới hạn
- Chỉ so bố cục và nội dung nhìn thấy, chưa đo CLS / thời gian tải.
- Mỗi khổ màn chỉ xếp 1 lịch (3 ngày, khám phá nhiều, lễ hội + chụp ảnh, không có ngày đi). Lịch có ngày đi trong 7 ngày tới (ô thời tiết, ghi chú dự báo) chưa chụp.
