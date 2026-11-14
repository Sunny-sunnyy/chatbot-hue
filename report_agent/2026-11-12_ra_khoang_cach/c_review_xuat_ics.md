# Review — xuất lịch .ics của E (`p9-gd-h1` `9f086d2`)

Người kiểm: C (`hue-rag-b4`) · 12:10 14/11/2026 (`date`) · skill `risk-gated-agent-review` · 0 USD. Plan: `docs/superpowers/plans/2026-11-14-xuat-lich-ics-plan.md`.

**Kết luận: ready_for_user_confirmation — 0 blocker, 0 major, 2 minor.**

## Đã kiểm (phép thử độc lập của C, node + Python, không dùng script của E)
- **Diff:** `lich_ics.js` (hàm thuần), `NutIcs` trong `LichV2.jsx`, 2 dòng CSS.
  - Không gọi mạng, không gọi model; tải về bằng Blob như nút .txt; CSP không đổi.
  - Lịch không có ngày đi ⇒ hiện dòng nhắc, không đoán ngày.
  - Chữ model chỉ vào phần mô tả, sau khi đã bỏ mã [n].
- **Ca khó C tự dựng:**
  - mô tả dài tiếng Việt có `, ; \` và xuống dòng: 0 dòng quá 75 byte, file kết thúc bằng CRLF; trình đọc tối giản của C gỡ gập dòng và gỡ thoát ra **đúng nguyên văn** mô tả;
  - tên có `, ;` được thoát đúng;
  - 06:30 giờ Việt Nam ⇒ `23:30Z` của ngày hôm trước (đúng UTC+7);
  - "suất 19:00 / 20:00 / 21:00" ⇒ 19:00–20:00 kèm câu "chọn suất khác";
  - mục "nghỉ" không thành sự kiện;
  - mục không có giờ ⇒ bỏ, đếm vào `soBo`, nút báo số điểm đã bỏ.
- `icalendar` không có trong `.venv` ⇒ không chạy được trình đọc chuẩn. E đã ghi giới hạn này trong plan; C không thêm gói.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor | `docGio` | Khoảng giờ qua nửa đêm (vd "21:00 – 00:30") ⇒ `null` ⇒ bỏ sự kiện. Bảng điểm hiện tại không có điểm nào như vậy: 5 điểm tối đều kết thúc trước 23:00. | ghi trong chú thích; xử lý khi bảng có điểm như vậy |
| m-2 | minor | `UID` | UID = ngày đầu + `id_muc`. Hai lịch khác nhau cùng ngày bắt đầu, nhập vào cùng một ứng dụng lịch, sẽ ghi đè sự kiện của nhau. Đây thường là điều muốn khi người dùng xếp lại lịch, nhưng code chưa ghi rõ ý định. | một dòng chú thích nói rõ ý định |
