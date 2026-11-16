# Plan mức nhẹ — bật bản đồ lịch (C, 14:49 16/11/2026)

A giao 16/11 (mốc 30/11 cần bản đồ lịch). Mức nhẹ (`Session_Prompt.md` §7): A đọc rồi duyệt khi đã có host; không review plan. Trần **0,05 USD**.
Đánh giá nền: `data/ban_do_lich_2026-11-16/danh_gia.md` (private). Plan gốc của tính năng: `2026-11-08-ban-do-lich-trinh-plan.md` (tiêu chí Q-M1–Q-M7 giữ nguyên).

## 1. Lỗi có thật (đã đo, 0 USD)
Từ máy User 16/11: `tile.openstreetmap.org` và `www.openstreetmap.org` nối TCP được nhưng **bắt tay TLS thất bại**; cùng một ô từ CARTO, Esri, OSM Pháp, OSM Đức trả 200. Ô bản đồ do trình duyệt người xem tải ⇒ nếu nhà mạng chặn thì bật cờ ra khung xám. A đang hỏi User thử link trên điện thoại.

## 2. Đổi gì (một nhánh `p11-ban-do-bat`)
- **(a) Host ô bản đồ: `<HOST — chờ User / A chọn>`** — sửa 4 chỗ cùng nhau: `TILE` + `GHI_CONG` (`frontend/src/BanDoLich.jsx`), `TILE_HOST` (`backend/api/app.py`, CSP `img-src` vẫn chỉ thêm đúng một host), câu đường ra ở trang Giới thiệu (`GioiThieu.jsx`, tên nhà cung cấp mới). Host có nhiều tên con (`a.` / `b.` …) ⇒ dùng **một** tên con cố định để CSP chỉ có một host.
  Ứng viên (tra 16/11 — `data/tra_cuu_cli/2026-11-16_o-ban-do/`; C tự mở trang điều khoản CARTO + trang OSM Đức):
  | Host | Điều khoản (đã mở) | Khoá | Ghi công |
  |---|---|---|---|
  | CARTO Voyager | giáo dục / học thuật = phi thương mại, **5 triệu ô / tháng** miễn phí; không khoá ⇒ có thể bị đóng dấu chìm (cập nhật 29/09/2026) | **cần khoá CARTO cấp** (xin qua email; khoá nằm trong JS công khai — bình thường với khoá ô bản đồ) | OSM + CARTO, "nổi bật" |
  | OSM Đức (FOSSGIS) | chỉ phi thương mại, cho "ứng dụng web nhỏ"; giới hạn tốc độ theo IP, không công bố số | không | © OpenStreetMap contributors |
  | OSM Pháp (HOT / osmfr) | theo Codex: miễn phí nếu công khai, phi lợi nhuận, lưu lượng vừa phải; **C chưa tự mở được** (wiki ở openstreetmap.org — bị chặn ở đây) | không | theo wiki |
  C khuyên **OSM Đức** nếu User không muốn xin khoá (không đăng ký, điều khoản khớp "ứng dụng web nhỏ phi thương mại"); **CARTO** nếu xin được khoá trước buổi chấm (hạn mức rõ bằng số). Chọn host là quyết định đường ra ⇒ User chọn.
- **(b) Kéo trên điện thoại:** `L.map(…, { dragging: !L.Browser.mobile, scrollWheelZoom: false })` (E 16/11 lúc code: **không** đặt `tap` — iOS cần handler tap để bấm ghim mở ô tên) — trên điện thoại vuốt qua khung là cuộn trang; vẫn phóng to / thu nhỏ bằng nút, bấm ghim mở ô tên. Một khổ 390 thử bằng tay (Playwright chạm + vuốt) trước khi sửa, để biết lỗi có thật.
- **(c) Kiểm "0 lỗi console" + ô bản đồ 200** (Q-M2 của plan gốc) — lần đầu kiểm được trên máy này.
- Không đổi: dữ liệu toạ độ v9, server, chữ gửi model (cờ tắt / bật đều giống byte — test sẵn có), ghim quán / khách sạn (để sau 30/11 — A chốt).

## 3. Bộ đo + tiêu chí (ghi trước)
| Vai | Kiểm | Ngưỡng |
|---|---|---|
| Test (0 USD) | `test_ban_do_lich.py` (CSP: cờ tắt giống byte; cờ bật thêm đúng một host) + `test_static_ui.py` | đạt |
| Q-M1 (≈ 0,0015 USD) | 3 lượt biểu mẫu thật 1 / 2 / 3 ngày trên server tạm 8041, cờ bật | số ghim mỗi ngày = số điểm có toạ độ; số trên ghim = thứ tự |
| Q-M2 | Playwright 1440 + 390: lỗi CSP / console / pageerror; request ô | **0 lỗi**; mọi ô 200 từ đúng host mới; không host lạ |
| Q-M3 / Q-M4 / Q-M6 | ghi công hiện ở 2 khổ · câu thường 0 request ô + không tải chunk bản đồ · chữ câu hỏi không có trong request ô | đạt |
| (b) điện thoại | Playwright 390 có chạm: vuốt dọc trên khung ⇒ trang cuộn (`scrollY` tăng), tâm bản đồ không đổi; ca đối chứng: khổ 1440 kéo chuột ⇒ tâm bản đồ đổi | đạt cả hai |
| Q-M7 | ảnh 3 lịch × 2 khổ ⇒ A đưa User xem ghim đúng chỗ (7 điểm Serper 15/11 chưa ai nhìn) | nhận xét của User |
Đạt hết ⇒ đề xuất bật `ban_do_lich: true` (một commit riêng, User duyệt). Toạ độ lệch ⇒ sửa bảng v9 theo `WORKFLOW.md` §3.4 và dựng lại bảng khoảng cách (một lần gọi OSRM).

## 4. Tiền + giờ
≈ 0,0015 USD (3 lượt biểu mẫu) + chạy lại nếu sửa ⇒ ≤ 0,005; trần 0,05. Giờ ≈ 2–3 giờ code + đo, cộng thời gian chờ User chọn host và xem ảnh.

## 5. Cần trước khi code
1. User thử link ô `tile.openstreetmap.org` trên điện thoại (A đang hỏi).
2. User / A chọn host (bảng mục 2a). Chọn CARTO ⇒ User xin khoá CARTO (C không xin hộ).
