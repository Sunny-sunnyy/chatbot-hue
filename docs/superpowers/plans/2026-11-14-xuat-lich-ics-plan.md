# Plan — xuất lịch .ics từ thẻ lịch (việc agent (4), mức nhẹ)

Viết: E, 14/11/2026. A chốt thứ tự agent đợt 1; User duyệt "4 việc theo thứ tự nhóm". Chỉ giao diện: không đổi backend, không gọi model, không gửi gì ra ngoài.

**Việc.** Nút "Thêm vào lịch (.ics)" đặt trong khối nút `.lich` của `LichV2.jsx`, cạnh Sao chép / Tải về. Code trong trình duyệt dựng file iCalendar (RFC 5545) từ **khung** lịch: tên, giờ, ngày do code xếp, không lấy chữ model làm dữ kiện.
- Mỗi điểm một sự kiện (VEVENT): `SUMMARY` = tên điểm; `LOCATION` = "tên, Huế"; `DESCRIPTION` = câu tả đã qua kiểm (bỏ mã [n]) + "Giờ gợi ý theo thời lượng tham quan — kiểm lại giờ mở cửa trước khi đi." + link Google Maps do code dựng (đã có trong `map_url`).
- Giờ: `m.gio` dạng "HH:MM – HH:MM" ⇒ bắt đầu / kết thúc. Dạng "suất 19:00 / …, khoảng 1 giờ" ⇒ suất đầu, dài 60 phút, ghi "chọn suất khác nếu cần". Không đọc ra giờ ⇒ bỏ sự kiện đó, cuối file ghi số đã bỏ.
- Giờ Việt Nam UTC+7 (không có giờ mùa hè) ⇒ ghi giờ UTC `…Z`, mọi ứng dụng lịch đều đọc được.
- Mục "nghỉ" (tối để trống) không thành sự kiện.
- Lịch **không có ngày đi** ⇒ nút ẩn, thay bằng dòng "Chọn ngày đi ở biểu mẫu để thêm vào lịch điện thoại" (không đoán ngày).
- Tệp tải về `lich-trinh-hue.ics` qua `Blob`, như nút "Tải về (.txt)" có sẵn (CSP không đổi).

**Không làm:** link chia sẻ, đồng bộ Google Calendar (cần đăng nhập / API), nhắc giờ.

**Kiểm (0 USD, ~30 phút):**
1. Hàm thuần `dungIcs(lich, cau)` trong `lich_ics.js`. Kiểm trên khung thật đã lưu của bộ quyết 12 (`data/len_ke_hoach_v2_2026-11-13/nghiem_thu/`): mỗi điểm có giờ ⇒ đúng một VEVENT; ngày, giờ khớp khung; dòng kết thúc CRLF; mỗi dòng ≤ 75 byte (gập dòng); ký tự `,;\` và xuống dòng được thoát. Chạy bằng Playwright gọi đúng module build (không có bộ test JS) và đối chiếu bằng code Python.
2. Parse lại bằng một trình đọc độc lập: `python -m icalendar` nếu có sẵn trong `.venv`; không có ⇒ trình đọc tối giản viết trong script kiểm. Không thêm gói.
3. Playwright 1440 + 390 trên bản build: bấm nút ⇒ có file tải về; lịch không ngày ⇒ thấy dòng thay thế. Mở thử trên Google Calendar: KHÔNG làm (cần đăng nhập — luật cấm). Thay bằng trình đọc ở bước 2; ghi rõ giới hạn này.
4. Review: C.
