# Nghiên cứu "cảm giác wow": trang được giới thiết kế khen 2025–2026 + thư viện mẫu hình chuyển động

Người làm: C (`hue-rag-b4`) · 11:51 14/11/2026 (`date`) · A giao theo yêu cầu của User · 0 USD.
Cách làm: Codex tra web (kết quả: `data/tra_cuu_cli/2026-11-14_wow-chuyen-dong/`). C tự mở 3 trang để kiểm: trang công bố giải CSSDA WOTY 2025, hồ sơ CSSDA của T Service (cả hai khớp), trang tin UNESCO (bị chặn 403, chưa kiểm được). B quay video 16 URL C gửi (report riêng của B).

**Kết luận ngắn:** cảm giác "wow" ở các trang được khen đến từ **một khoảnh khắc chính được dàn dựng** (một màn kể chuyện, một chuyển cảnh ảnh, một bản đồ hiện dần), không đến từ nhiều hiệu ứng rải khắp trang.
- Với Huế, 4 mẫu đáng làm thêm, đều bằng CSS + SVG, gần 0 KB (mục 3).
- Không cần WebGL hay thư viện, trừ khi làm màn kể chuyện ghim nhiều bước (xem `c_framework_hieu_ung.md`).

**Từ dùng trong bài:**
- *ghim*: khối đứng yên trong khi cuộn;
- *mặt nạ*: hình cắt che bớt ảnh, rồi mở dần để lộ ảnh;
- *chuyển cảnh có phần tử chung*: ảnh nhỏ ở trang trước "bay" thành ảnh lớn ở trang sau;
- *WebGL*: vẽ 3D / đổ bóng bằng card đồ hoạ.

## 1. Trang đáng học (nguồn ghi nhận có link)

| Nhóm | Trang | Ghi nhận | Điều đáng học | Kỹ thuật (chỉ khi nguồn nói) |
|---|---|---|---|---|
| Sản phẩm / thương hiệu | Dropbox Brand | CSSDA Website of the Year 2025 **hạng 1**, Webby Best UX 2025 **[C mở]** | trang thương hiệu nhiều màu, chuyển động khi cuộn | CSSDA ghi "animated, scroll"; không nêu thư viện |
| Du lịch / sản vật (gần Huế nhất) | The Symphony of Vines (Unseen Studio) | CSSDA WOTY 2025 **hạng 2** **[C mở]** | hành trình điện ảnh tương tác, kể chuyện một vùng trồng nho | WebGL, video, âm thanh |
| Thể thao / nhân vật | Charles Leclerc (Apart & Uprising) | CSSDA WOTY 2025 **hạng 3** **[C mở]** | — (chưa có mô tả) | không rõ |
| Portfolio | Bruno's Portfolio (Bruno Simon) | CSSDA Best Portfolio 2025 **[C mở]** | portfolio dạng thế giới 3D lái xe | không rõ từ nguồn đã mở |
| Agency | We are Büro (Bürocratik) | CSSDA Best Agency 2025 **[C mở]** | — | không rõ |
| Agency / gallery | T Service Audio & Light | CSSDA Special Kudos 16/07/2025 **[C mở]** | lưới bento, gallery masonry có lightbox, parallax | GSAP |
| Kể chuyện | Penumbra: Storytelling in Web | CSSDA Special Kudos 02/2025 (Codex) | câu chuyện thiên thể qua từng đoạn | Lottie + shader |
| Bảo tàng | Rijksmuseum Collection Online | Webby Best UI 2025 (Codex) | so hai tác phẩm cạnh nhau, phóng chi tiết, tự dựng bộ sưu tập thành video | không rõ |
| Di sản | UNESCO Dive into Heritage | UNESCO ra mắt 07/2025 (Codex; trang tin chặn C: 403) | mô hình 3D di sản + bản đồ + ảnh + hoạt hình kể chuyện theo địa điểm | không rõ thư viện |
| Báo chí | The Pudding | bài phê bình 22/09/2026 + hướng dẫn quy trình của họ (Codex) | cuộn kể chuyện: bìa album lớn dần theo bài hát; cảnh báo của chính họ: cuộn nhanh, điện thoại, nhiều trạng thái là chỗ khó | kích hoạt theo bước cuộn |
| Bảo tàng | Australian National Maritime Museum | Good Design Awards 2025 (Codex) | "Stories of the Sea": video + ảnh + lời giám tuyển | không rõ |

**Trang sản phẩm nổi tiếng về chuyển động** (Apple, Linear, Stripe, Vercel, Raycast): Codex **không** tìm được nguồn giải 2025–2026 mở được. C gửi B để quay so cảm giác, ghi rõ là "chưa có nguồn giải".
Awwwards / FWA: Codex không mở được hồ sơ 2025–2026 nên không ghi giải nào của hai nơi này.

## 2. Thư viện 20 mẫu hình chuyển động — cái nào hợp Huế

Cột "làm bằng" ghi cách rẻ nhất đủ dùng. Giá: **0** = CSS / SVG thuần · **nhỏ** = < 5 KB JS tự viết · **vừa** = thư viện 20–50 KB · **nặng** = WebGL / video.

| # | Mẫu | Cảm giác | Làm bằng · giá | Rủi ro trợ năng | Hợp Huế? Trang nào |
|---|---|---|---|---|---|
| 1 | Tiêu đề hiện theo dòng / từ | mở màn có nhịp | CSS · 0 | trình đọc màn hình đọc vụn nếu tách chữ ⇒ tách bằng CSS, giữ chữ liền | **đã có** (`.vao`) |
| 2 | Khối hiện dần khi cuộn tới | trang "thở" | CSS `animation-timeline` + dự phòng IO · 0 | nội dung không được ẩn khi hiệu ứng lỗi | **đã có** (`.hien`) |
| 3 | Ghim một khung, đổi nội dung theo bước | kể chuyện | CSS `sticky` · 0; đồng bộ chính xác ⇒ GSAP · vừa | không khoá cuộn, thứ tự đọc tự nhiên | **có**: "Huế qua các thời kỳ" (Giới thiệu / trang chủ), chỉ dùng dữ kiện trong kho |
| 4 | Ảnh lộ dần qua mặt nạ | hé lộ, sang | CSS `clip-path` theo cuộn · 0 | không giấu thông tin chính | **có**: ảnh đầu bài Khám phá, ảnh từng điểm trong lịch |
| 5 | Thẻ xếp chồng khi cuộn | tuyển tập | CSS `sticky` + `transform` · 0 | sticky dài che nội dung trên điện thoại | tạm không (lịch nhiều ngày dễ rối) |
| 6 | Bộ sưu tập ngang trong khi cuộn dọc | gallery | CSS cuộn ngang có snap · 0 | phải có nút / dấu cuộn ngang | **đã có** trên điện thoại ("Điểm nên đến") |
| 7 | Chuyển cảnh có phần tử chung | "đi theo" ảnh | View Transitions + `view-transition-name` · 0 (Firefox 144+) | không làm mất tiêu điểm | **có**: thẻ Khám phá ⇒ ảnh đầu bài; thẻ điểm ⇒ trang bài |
| 8 | Nút hút theo con trỏ | tinh nghịch | JS nhỏ | chỉ chuột; điện thoại / bàn phím không có | không (trang nhiều chữ, đa số dùng điện thoại) |
| 9 | Thẻ nghiêng 3D theo chuột | chiều sâu | CSS + JS nhỏ | dễ chóng mặt | không |
| 10 | Chữ chạy marquee | không khí lễ hội | CSS · 0 | lặp vô hạn ⇒ WCAG 2.2.2 | không (hoặc chỉ dải lễ hội có nút dừng) |
| 11 | Con trỏ tuỳ biến | cá tính | JS nhỏ | thay con trỏ hệ thống ⇒ khó dùng | không |
| 12 | Số đếm lên | nhấn số | JS nhỏ | đọc nhiều số liên tiếp | không (số duy nhất đáng khoe là "207 bài", không cần chạy) |
| 13 | Shader / hạt WebGL (nước, ánh sáng) | lộng lẫy | WebGL · nặng | nóng máy, hao pin, che chữ | không (CPU điện thoại; hiệu ứng nước đã có bằng sóng SVG) |
| 14 | Parallax nhiều lớp | chiều sâu | CSS · 0 | chuyển động xa ⇒ say | **đã có** một lớp (`.troi-cuon`), không thêm lớp |
| 15 | Ảnh nhỏ ⇒ toàn màn hình | bước vào tác phẩm | View Transitions · 0 | phải có nút thoát + tiêu điểm đúng | **có**: ảnh trong trang bài (bấm phóng) |
| 16 | Đường vẽ dần theo cuộn (SVG) | hành trình | SVG `stroke-dashoffset` + scroll timeline · 0 | có nhãn thay, không chỉ dựa vào màu | **có, đáng nhất**: đường sông Hương vẽ dần nối các điểm của lịch, hoặc nối "3 bước" ở Giới thiệu |
| 17 | Sóng âm / âm thanh theo cuộn | sống động | Web Audio · vừa | không tự phát âm | không (không có âm thanh có quyền) |
| 18 | Kéo so trước ↔ sau | tò mò | CSS `clip-path` + JS nhỏ | phải dùng được bằng bàn phím | có thể: ảnh xưa ↔ nay của một di tích (chỉ khi có cặp ảnh) |
| 19 | Gallery masonry + lightbox | duyệt ảnh | CSS grid + `<dialog>` · nhỏ | giữ tiêu điểm, phím Esc | **có**: trang bài khi có nhiều ảnh |
| 20 | Tự dựng bộ sưu tập thành video | chia sẻ | canvas / video · nặng | điều khiển phát | không |

## 3. Đề xuất áp cho Huế (thứ tự lợi ↔ công)

1. **Đường sông Hương vẽ dần (mẫu 16).** Một đường SVG uốn như sông chạy dọc trang, vẽ dần khi cuộn, nối các mốc. Đặt ở dải "3 bước" của Giới thiệu, và nối các điểm trong lịch theo ngày ở Lên kế hoạch. Đây là "khoảnh khắc chính" riêng của Huế, không trang nào trong danh sách có. CSS + SVG, 0 KB; máy giảm chuyển động ⇒ hiện sẵn cả đường.
2. **Chuyển cảnh có phần tử chung (mẫu 7 + 15).** Bấm thẻ ở Khám phá ⇒ ảnh thẻ bay thành ảnh đầu bài. Nền đã có View Transitions (đợt 0 của E), chỉ cần gắn `view-transition-name` theo mã bài. 0 KB.
3. **Ảnh lộ dần qua mặt nạ (mẫu 4)** cho ảnh đầu bài và ảnh điểm trong lịch: chỉ `clip-path` theo cuộn, 0 KB.
4. **Màn kể chuyện ghim (mẫu 3)**, chỉ khi User muốn và có nội dung kho cho 4–6 mốc thời kỳ. Bản CSS `sticky` trước; GSAP chỉ khi bản CSS không đủ mượt.

**Không làm:** nút hút, nghiêng 3D, con trỏ tuỳ biến, marquee, WebGL, số đếm, âm thanh. Lý do: chỉ chạy với chuột (đa số khách dùng điện thoại), dễ gây say chuyển động, nặng máy, hoặc không có nội dung tương ứng.

## 4. Đã kiểm ↔ chưa kiểm
- **C mở:** thứ hạng CSSDA WOTY 2025 (trang công bố 12/02/2026); hồ sơ T Service (GSAP, parallax, masonry; link trang thật).
- **Chỉ từ Codex:** các dòng còn lại ở mục 1; Codex ghi rõ những chỗ "không rõ thư viện", C không đoán thêm.
- **Chưa:** B quay video 16 URL (report của B); mẫu 16 / 7 / 4 chưa dựng thử. Nếu A / User chọn, C dựng thử mẫu 16 trên bản mẫu Giới thiệu rồi đo 3 phép.
