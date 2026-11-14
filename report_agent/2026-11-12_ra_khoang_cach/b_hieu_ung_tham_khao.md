# Học chuyển động từ trang du lịch / văn hoá thiết kế đẹp — B · 11:28 14/11/2026

A giao (User hỏi "đã dùng Playwright vào các trang đó test chưa"; mẫu của mình nhạt vì chỉ học TRIPO, gần như không chuyển động). 0 USD.

**Cách làm** (`data/ui_tham_khao_2026-11-14/tools/quay.py`):
- Chromium không màn hình, `permissions=[]`, dò DNS trước. Mỗi trang: quay video 1440 lúc tải ⇒ cuộn chậm (350 px / 0,45 s) hết trang ⇒ rê chuột 3 thẻ có ảnh (đo transform trước / sau) ⇒ mở 1 trang con cùng host. Chụp đầu trang 1440 + 390 và toàn trang 1440.
- Dò thư viện / kỹ thuật bằng code: GSAP / ScrollTrigger, Lenis, Locomotive, Framer, Swiper / Splide / Slick, Lottie, three.js, canvas, video tự chạy, AOS, Barba / Swup; trong CSS: `view-transition`, `animation-timeline`, số `@keyframes`, số quy tắc `transition`, `prefers-reduced-motion`, `scroll-behavior`, phần tử `sticky`. Đếm `document.getAnimations()` lúc tải và lúc cuộn; đếm lần gọi `document.startViewTransition` khi chuyển trang.
- Video được trích thành bảng 16 khung hình (`khung_hinh.jpg`, ffmpeg) để đọc chuyển động.
- **Cookie:** chỉ bấm "Reject all" khi có; không đăng nhập / mua / gửi form.

**Bị chặn — KHÔNG vượt:**
- MySwitzerland: trang CAPTCHA của Fastly;
- japan.travel: CloudFront 403 "Request blocked" với trình duyệt tự động.
Script dừng khi thấy trang chống bot. Hai trang này chỉ còn ảnh trang chặn.

## 1. Từng trang

| Trang | Hiệu ứng thấy được (video / ảnh) | Thư viện / kỹ thuật dò thấy | "Sống" đến từ đâu |
|---|---|---|---|
| **London Museum** (Webby 2025) `06_london_museum` | mở đầu **nền đen + chữ lớn màu bạc hà** "We are London's storytellers" ⇒ **ảnh / video hiện dần phía sau chữ**; khối đầu là **băng chuyền toàn màn**: mỗi địa điểm một ảnh / video nền, tiêu đề in hoa rất lớn, 3 thẻ nhỏ ở góc phải là "slide kế"; dải thông báo chữ chạy ngang trên cùng; bồ câu trắng (linh vật) lặp ở nhiều khối | 2 video tự chạy, 17 `@keyframes`, 96 `transition`, có `prefers-reduced-motion`, `scroll-behavior: smooth`; lúc cuộn tới **15 animation chạy cùng lúc**; không GSAP / Lenis (CSS + JS riêng) | video nền + chữ rất lớn đè ảnh; nhịp chuyển slide tự động; màu nhấn mạnh (tím / bạc hà) trên nền tối |
| **Visit Sanya** `05_sanya` | **video toàn màn** ở đầu trang; menu nổi trong suốt; cuộn **mượt có quán tính** (Lenis); "Top things to do" thẻ ảnh, rê chuột ⇒ **ảnh phóng 1,09**; tiêu đề khối **hiện dần khi cuộn tới** (khung "What's on" mờ ⇒ rõ); thẻ sự kiện hai cột; khung chat linh vật góc phải; chân trang ảnh hoàng hôn toàn khổ | **Lenis**, **Splide** (băng chuyền), 1 video tự chạy, CSS có `view-transition` + `animation-timeline` (cuộn điều khiển hoạt ảnh), 16 `@keyframes`, có `prefers-reduced-motion` | cuộn có quán tính (cảm giác "trôi"); video người thật; chữ hiện theo cuộn |
| **Banff & Lake Louise** (Awwwards Honorable Mention 2023) `08_banff` | khối đầu **ảnh toàn khổ đổi qua lại** (Snowy Adventures ⇒ Winter Celebrations) với **tiêu đề lớn mờ dần / hiện dần**, nút ‹ › và chấm trang; hàng 4 thẻ ảnh ngay dưới; khối "Indigenous…" nền mận đậm, ảnh lớn bên phải; **khối thời tiết hôm nay / mai** có biểu tượng; rê chuột thẻ ⇒ ảnh phóng **1,03** | **Swiper**, CSS `view-transition` + `animation-timeline`, 97 `transition` | ảnh mùa thật cỡ lớn + chữ đè; chuyển slide mờ chéo; bảng màu ấm (kem / mận / cam) |
| **France.fr** (World Travel Tech Award) `02_france` | băng chuyền ảnh đầu trang có ‹ ›, đoạn mở đầu trong khung trắng **đè lên mép ảnh**; "Get inspired" có tab viên thuốc + hàng thẻ trượt ngang; **bản đồ nước Pháp có nhãn vùng** bấm được; khối trợ lý AI có ảnh người; trang con = bản đồ tương tác toàn màn | CSS `animation-timeline`, 10 `@keyframes`, 75 `transition`, `scroll-behavior: smooth`, `prefers-reduced-motion`; hộp đăng ký bản tin bật ra khi cuộn (gây rối — không nên học) | ảnh lớn + khung chữ đè mép; bản đồ như một "đồ chơi" để khám phá |
| **Visit Copenhagen** `03_copenhagen` | trang cuộn **trong một khung** (không cuộn cả tài liệu) ⇒ phép đo cuộn không bắt được; băng chuyền thẻ | **Swiper**, CSS `animation-timeline`, 15 `@keyframes`, 2 phần tử `sticky` | (đo được ít — xem video) |
| **Lithuania Travel** (Awwwards Honorable Mention 06/2025) `07_lithuania` | trang cuộn trong khung + cửa sổ chọn ngôn ngữ chắn ⇒ video ngắn, ít nội dung | CSS `view-transition` + `animation-timeline`, **47 `@keyframes`**, 187 `transition` (nhiều nhất) | chưa đo đủ — giới hạn |
| (Trang danh mục Awwwards du lịch) `00_awwwards_du_lich` | chỉ để chọn 2 trang trên | — | — |

**Không trang nào dùng GSAP, three.js, Lottie hay Framer** (theo phép dò). **Không trang nào gọi `startViewTransition` khi chuyển trang** (0 lần). Chuyển trang vẫn là tải lại cả trang; CSS `view-transition` có ở 3 trang nhưng không thấy chạy trong lượt mở trang con.

## 2. Rút ra (quan sát, không phải nguyên nhân đã chứng minh)
Các trang "đẹp" này khác TRIPO ở **ảnh / video cỡ lớn + chữ to đè lên + nhịp đổi slide**, chứ không ở thư viện hoạt hình nặng. Kỹ thuật lặp lại nhiều nhất:
1. **khối đầu toàn khổ** (ảnh hoặc video) có tiêu đề rất lớn, đổi slide mờ chéo, có ‹ › và chấm;
2. **chữ / khối hiện dần khi cuộn tới** — CSS `animation-timeline` có ở 5 / 6 trang chạy được;
3. **ảnh trong thẻ phóng nhẹ khi rê chuột** (1,03–1,09);
4. **cuộn mượt** (`scroll-behavior: smooth` ở 3 trang; Lenis ở 1);
5. **băng chuyền thẻ** (Swiper / Splide);
6. **mọi trang có `prefers-reduced-motion`**.

## 3. Áp được cho Huế (CSS thuần, không thư viện — đúng A chốt)
| Kỹ thuật | Áp vào đâu ở hue_rag | Tốn |
|---|---|---|
| Khối đầu toàn khổ + tiêu đề lớn + đổi 3–4 ảnh mờ chéo (CSS `@keyframes` opacity, tạm dừng khi giảm chuyển động) | trang chủ (ảnh sông Hương / Ngọ Môn / lăng đã có giấy phép) | nhỏ |
| Hiện dần khi cuộn bằng `animation-timeline: view()` (có đường lui: không hỗ trợ ⇒ hiện luôn) | khối trang chủ, thẻ Khám phá, **từng ngày của lịch** | nhỏ |
| Ảnh phóng 1,03 khi rê chuột thẻ | thẻ Khám phá, ảnh điểm trong lịch | rất nhỏ |
| Khung chữ trắng đè mép ảnh (France) | đầu trang bài / Giới thiệu | nhỏ |
| Khối "thời tiết hôm nay / mai" có biểu tượng (Banff) | trang chủ (đã có dữ liệu thời tiết) | nhỏ |
| Video nền | **không** — không có video giấy phép mở + nặng | — |
| Cuộn có quán tính (Lenis) | **không** — thêm thư viện, đụng Playwright / trợ năng | — |

## 4. 5 video / ảnh tiêu biểu cho User (`data/ui_tham_khao_2026-11-14/`)
1. `06_london_museum/video_1440.webm` (+ `khung_hinh.jpg`) — khối đầu tối, chữ lớn, video nền, băng chuyền địa điểm
2. `05_sanya/video_1440.webm` (+ `khung_hinh.jpg`) — video toàn màn, cuộn có quán tính, chữ hiện dần khi cuộn, thẻ phóng ảnh
3. `08_banff/video_1440.webm` (+ `khung_hinh.jpg`) — ảnh mùa toàn khổ đổi mờ chéo, khối thời tiết
4. `02_france/khung_hinh.jpg` — khung chữ đè mép ảnh, bản đồ có nhãn vùng
5. `08_banff/toan_trang_1440.png` — bố cục cả trang (kem / mận / cam) để so với H1 "Sông Hương"

**Giới hạn:**
- 2 / 8 trang chặn trình duyệt tự động.
- Copenhagen + Lithuania cuộn trong khung nên phép đếm animation lúc cuộn = 0 là **chưa đo được**, không phải "không có".
- Phép dò thư viện dựa trên tên script / biến toàn cục: thư viện đã gói lại đổi tên có thể bị bỏ sót.

## 5. Trang KHÔNG du lịch (A mở rộng, 11:53 14/11/2026) — 17 trang, cùng cách quay + đo FPS lúc cuộn + dung lượng JS

**Danh sách:**
- 8 trang đoạt giải do C gửi (nguồn C kiểm: CSSDA WOTY 2025 hạng 1–3, Best Portfolio, Best Agency, Special Kudos; Codex: WOTD, Kudos): Dropbox Brand · Symphony of Vines · Charles Leclerc · Bruno Simon · Büro · T Service · Penumbra · Creative Website Manual;
- Rijksmuseum (Webby) · UNESCO Dive into Heritage · The Pudding;
- trang sản phẩm: Apple AirPods Pro · Linear · Stripe · Vercel · Raycast · Arc.

Địa chỉ thật lấy từ trang hồ sơ CSSDA. Bảng số đầy đủ: `data/ui_tham_khao_2026-11-14/tong_hop.txt`.

**Cách đọc FPS:** máy WSL **không có GPU**, nên FPS chỉ để so các trang với nhau, không phải số trên máy người dùng. Trang hue_rag cũng sẽ chạy trên máy yếu / điện thoại.

| Nhóm | Trang (FPS trung bình lúc cuộn · khung chậm p95 · JS tải) | Dò thấy |
|---|---|---|
| **WebGL / 3D nặng** | Bruno Simon (0 FPS · 2,4 s · 1,0 MB) · Symphony of Vines (0 · 2,9 s · 0,5 MB — **1 phút 54 giây** mới hiện cảnh đầu) · Penumbra (13 · 133 ms · 0,7 MB) | OGL / three.js, WebGL, Lottie |
| **GSAP + cuộn mượt** | Creative Website Manual (49 · 33 ms) · T Service (57 · 33 ms · 99 KB) · Büro (43 · 50 ms) · Leclerc (30 · 50 ms) | GSAP + ScrollTrigger (2), Lenis (3), Barba (1) |
| **Trang sản phẩm** | Stripe (39 · 67 ms · 1,3 MB, nền WebGL) · Apple (44 · 50 ms · 1,0 MB) · Linear (31 · 100 ms; **549** hoạt ảnh cùng lúc khi cuộn, 231 `@keyframes`) · Vercel (58 · 17 ms) · Raycast · Arc (6,1 MB JS) | Apple / Linear / Vercel: CSS `animation-timeline` + `view-transition`; Stripe: WebGL |
| **Văn hoá / báo chí** | The Pudding (**60** · 17 ms · 67 KB) · UNESCO (55 · 33 ms) · Rijksmuseum (51 · 33 ms, OGL) · Dropbox Brand (57 · 17 ms · 16 KB, OGL) | ít thư viện |

**Rút ra (quan sát):**
1. **Trang càng nặng WebGL thì càng giật trên máy không GPU.** 3 trang 3D gần như không chạy (0–13 FPS, khung chậm 0,1–2,9 s). Trang CSS / ít JS mượt nhất (Pudding, Vercel, Dropbox: 57–60 FPS) ⇒ củng cố hướng **CSS thuần** đã chốt; 3D / WebGL **không** hợp với hue_rag (chạy CPU, người dùng điện thoại).
2. Trang sản phẩm "đỉnh" (Apple, Linear, Vercel) làm chuyển động chủ yếu bằng **CSS** (`animation-timeline`, `view-transition` trong CSS, nhiều `@keyframes`), không phải GSAP.
3. Khoảnh khắc "wow" lặp lại:
   - **chữ rất lớn hiện dần theo dòng khi cuộn tới** (Apple, Creative Manual, Linear);
   - **ảnh / sản phẩm lớn đổi theo vị trí cuộn**: ghim một ảnh, chữ chạy qua (Apple);
   - **ảnh chụp giao diện thật mờ ⇒ rõ** khi tới (Linear);
   - **lưới ảnh kiểu gạch so le** (T Service);
   - **màn chờ có số %** (Creative Manual — không nên học: bắt chờ).
4. Ở 17 trang không thấy lần gọi `startViewTransition` nào khi mở trang con.

### 8 video tiêu biểu cho User (giây đáng xem; file `data/ui_tham_khao_2026-11-14/<trang>/video_1440.webm`, bảng khung hình có giờ `khung_hinh.jpg`)
| # | Trang | Giây đáng xem | Xem gì |
|---|---|---|---|
| 1 | `23_apple_airpods` | 0:00 · 0:14–0:28 · 0:42 · 1:04 | ảnh sản phẩm lớn; vòng sóng màu lan theo cuộn + chữ lớn; chữ đè ảnh người; băng chuyền thẻ ngang |
| 2 | `19_creative_manual` | 0:12 · 0:24–0:49 · 1:01 | chữ rất lớn đổi kiểu; câu hiện dần theo dòng; thẻ dự án |
| 3 | `24_linear` | 0:00–0:10 · 0:15–0:35 | tiêu đề + ảnh giao diện mờ ⇒ rõ; khối tính năng hiện theo cuộn trên nền tối |
| 4 | `06_london_museum` | 0:00–0:10 · 0:30–1:00 | nền đen + chữ lớn ⇒ video hiện sau chữ; băng chuyền địa điểm toàn màn |
| 5 | `05_sanya` | 0:00–0:20 · 0:40–0:55 | video toàn màn; cuộn có quán tính; tiêu đề khối hiện dần |
| 6 | `08_banff` | 0:05–0:20 · 0:40–0:50 | ảnh mùa toàn khổ đổi mờ chéo + tiêu đề lớn; khối thời tiết |
| 7 | `17_tservice` | 0:13–0:28 · 0:31 | lưới ảnh gạch so le; chữ chạy vòng tròn trên ảnh nền |
| 8 | `13_symphony_vines` | 0:00–1:54 · 1:54–2:30 | **ví dụ nên tránh**: 3D đẹp nhưng trên máy không GPU phải chờ gần 2 phút mới thấy cảnh |

**Áp cho Huế:** thêm vào §3 hai ý, đều làm bằng CSS:
- tiêu đề lớn hiện dần theo dòng khi cuộn (`animation-timeline: view()`);
- ghim ảnh lớn (sticky) trong lúc chữ chạy qua — vd trang bài: ảnh di tích đứng yên, đoạn văn cuộn qua.

Vẫn không làm 3D / WebGL / màn chờ.
