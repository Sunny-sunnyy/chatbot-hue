# So thư viện hiệu ứng cho giao diện mới — có cần thư viện, hay CSS thuần đủ?

Người làm: C (`hue-rag-b4`) · 11:27 14/11/2026 (`date`) · A giao theo câu User hỏi "đã nghiên cứu các framework chưa" · 0 USD (Codex tra web + C đo trên máy).
Không cài gói nào vào repo: mọi phép đo chạy trong `/tmp/c_fw` (xoá khi xong).

**Kết luận ngắn: CSS thuần (cộng khoảng 30 dòng JS của mình) đủ cho mức hiệu ứng User vừa nói "đã ổn hơn". Chưa nên thêm thư viện.**
Chỉ khi User muốn **một màn "cuộn kể chuyện"** (khối ghim lại, nhiều bước chạy theo vị trí cuộn, ví dụ dòng thời gian lịch sử Huế) thì mới thêm, và lúc đó chọn
**GSAP + ScrollTrigger**, chỉ tải ở trang có màn đó.

**Từ dùng trong bài:**
- *gzip*: kích thước sau nén, tức số byte trình duyệt thật sự tải.
- *CSP*: luật bảo mật của trang, chỉ cho chạy script và kiểu chữ từ chính máy chủ mình.
- *giảm chuyển động*: cài đặt của máy, người dùng chọn để không thấy hiệu ứng động.
- *ghim / scrub*: khối đứng yên trong khi cuộn, và hiệu ứng chạy tới / lùi theo đúng vị trí cuộn.

## 1. Bảng so (6 thư viện)

Cột gzip là **số C đo** (esbuild 0.28 nén nhỏ + gzip -9, không tính React, đúng phần thường import). Cột CSP là **C thử thật** trên Chromium với đúng luật CSP của trang (`script-src 'self'; style-src 'self'`) hoặc đọc mã đã đóng gói. Các cột khác lấy từ tra cứu Codex; C tự mở lại 3 ý chính, đánh dấu **[C mở]**.

| Thư viện (bản) | Làm được gì mà CSS khó làm | gzip C đo | Giấy phép | CSP của mình | Giảm chuyển động | Ghi chú |
|---|---|---|---|---|---|---|
| **Motion** 14.14 (`motion/react`) | hiệu ứng khai báo trong React, cử chỉ kéo, **layout animation** (phần tử đổi chỗ trượt mượt), phần tử dùng chung giữa hai màn, spring | đầy đủ **51,8 KB** · `LazyMotion` + `domAnimation` 31,2 KB · bản mini `useAnimate` 3,4 KB · bản không React (`animate`, `scroll`, `inView`) 28,9 KB | MIT | bản không React: **0 vi phạm** khi chạy `animate` / `scroll` / `inView`. Bản React có đoạn tạo thẻ `<style>` + `insertRule` (đường `AnimatePresence` chế độ `popLayout`) ⇒ có thể bị chặn nếu dùng đúng chế độ đó (chưa thử) | có sẵn `useReducedMotion`, `MotionConfig reducedMotion="user"` | tài liệu: thẻ `motion` không xuống dưới 43 KB; `m` + `LazyMotion` khởi đầu ~5 KB, +24 KB với `domAnimation` **[C mở]** |
| **GSAP 3.15 + ScrollTrigger** | **cuộn kể chuyện: ghim / scrub / snap**, dòng thời gian nhiều bước, Flip cho layout | lõi **27,0 KB** · lõi + ScrollTrigger **44,2 KB** | **miễn phí cả dùng thương mại, kể cả plugin trước đây trả phí** (giấy phép riêng "standard no-charge" của GreenSock, không phải MIT) **[C mở]** | thử ghim + scrub thật: **0 vi phạm**, chạy đúng. Mã có một chỗ `setAttribute("style")`, chưa gặp trong phép thử | không tự tắt; phải tự kiểm `prefers-reduced-motion` rồi tắt timeline | mạnh nhất cho "cuộn kể chuyện" |
| **Lenis** 1.3.27 | cuộn mượt (quán tính) | **5,3 KB** | MIT | không chạm style kiểu bị chặn (đọc mã) | **có sẵn, bật mặc định**: máy giảm chuyển động ⇒ cuộn 1 : 1 | cuộn mượt hay bị phàn nàn: đổi cảm giác cuộn của trình duyệt, dễ vướng phím / trình đọc màn hình ⇒ **không đề xuất** cho trang đọc nhiều chữ |
| **AutoAnimate** 0.10.2 | thêm / xoá / đổi chỗ phần tử trong danh sách tự trượt mượt (FLIP) | **3,4 KB** | MIT | không chạm style kiểu bị chặn (đọc mã) | **có sẵn, mặc định tắt khi máy giảm** | hợp nhất cho việc "lọc thẻ ở Khám phá" |
| **React Spring** 10.1.2 | chuyển động kiểu lò xo, đổi hướng giữa chừng tự nhiên | **17,4 KB** | MIT | không chạm style kiểu bị chặn (đọc mã) | chưa xác minh được | CSS `linear()` đã giả lập được đường lò xo cho hiệu ứng đơn giản |
| **Lottie** (lottie-web 5.13) | phát hoạt hình vẽ sẵn (xuất từ After Effects) | không đo (lớn; số công khai cũ năm 2018 ~60 KB) | MIT | chưa thử | không tự tắt | cần người vẽ hoạt hình ⇒ không hợp dự án |

Không có nguồn nào cho thấy thư viện nào cần `eval` / `new Function`. C đã tìm trong cả 8 bản đóng gói: **0 chỗ**.
Thư viện đổi kiểu bằng cách gán thuộc tính style qua JavaScript, và CSP của mình cho phép cách đó. Thứ bị chặn là thẻ `<style>` và thuộc tính `style=` viết trong HTML. Lượt thử đầu của C báo vi phạm vì chính trang thử có viết `style=`; bỏ đi thì còn 0.
**Trang du lịch / bảo tàng nổi tiếng nào dùng các thư viện này:** Codex không tìm được nguồn xác nhận nào. Không ghi đoán.

## 2. Trình duyệt hỗ trợ tới đâu (tháng 11/2026) — quyết định "CSS có đủ không"

| Tính năng CSS / API | Chrome / Edge | Safari | Firefox | Nguồn |
|---|---|---|---|---|
| Hiệu ứng chạy theo vị trí cuộn (`animation-timeline: view()` / `scroll()`) | 115 | **26.0** (cả iOS) | **159** | caniuse **[C mở]** |
| Chuyển cảnh cùng trang (`document.startViewTransition`, đúng kiểu web mình: đổi trang bằng hash) | 111 | 18.0 | 144 | caniuse (Codex) |
| Chuyển cảnh giữa hai trang (`@view-transition`) | 126 | 18.2 | chưa | caniuse + web-features (Codex) |

Máy chưa hỗ trợ thì lớp hiệu ứng chung của E dùng IntersectionObserver làm đường lui. Chuyển cảnh cùng trang thì không cần đường lui: trình duyệt không hỗ trợ chỉ đổi trang như cũ.

## 3. Những gì User muốn — CSS đã làm được chưa

Bản hiệu ứng 2 của E (User: "đã ổn hơn") gồm: ảnh đầu trang phóng chậm, trôi nhẹ khi cuộn, tiêu đề / ô hỏi hiện lần lượt, khối trượt vào khi cuộn tới, thẻ nhấc + lớp màu trượt khi rê chuột, menu đổi nền khi cuộn, nút lún khi nhấn, chuyển trang mượt.
**Tất cả chạy bằng CSS + khoảng 30 dòng JS, không thư viện.** C đo trên 6 trang mẫu:
- tương phản 0 trượt, ở cả 1440 / 390 và khung cuối của ảnh phóng;
- dịch chuyển bố cục (CLS) ≤ 0,034;
- máy giảm chuyển động ⇒ 0 hiệu ứng chạy.

| Việc thư viện làm hơn CSS | Mình có cần chưa | Nếu cần |
|---|---|---|
| Cuộn kể chuyện có ghim + nhiều bước | chưa có màn nào như vậy | GSAP + ScrollTrigger (+44 KB, chỉ tải ở trang đó) |
| Danh sách trượt mượt khi lọc (thẻ Khám phá đổi chỗ) | có thể có ích khi bấm lọc lĩnh vực | AutoAnimate (+3,4 KB); hoặc chuyển cảnh cùng trang của trình duyệt (0 KB) |
| Phần tử dùng chung giữa hai màn (ảnh thẻ phóng thành ảnh đầu bài) | chưa làm | chuyển cảnh cùng trang có `view-transition-name` làm được, 0 KB (Firefox 144+) |
| Lò xo, kéo thả | không có tương tác kéo thả | — |
| Cuộn mượt | không nên (đọc chữ, trợ năng) | — |

## 4. Khuyến nghị (để A trình User)

1. **Giữ CSS thuần** cho bản đang làm. Lý do:
   - mọi hiệu ứng User đã thấy và khen đều làm được;
   - thêm 0 KB, so với Motion đầy đủ +51,8 KB (≈ +49 % gói JS hiện ~106 KB) hay GSAP + ScrollTrigger +44,2 KB (≈ +42 %);
   - không thêm phụ thuộc phải cập nhật.

   Khi nào sai: User muốn một màn kể chuyện ghim nhiều bước. Chọn khác thì mất 30–50 KB tải thêm ở mọi trang, nếu không chia gói.
2. **Bản "có thư viện" để đặt cạnh, nếu User muốn so:** **GSAP + ScrollTrigger** cho **một** màn kể chuyện, ví dụ "Huế qua các thời kỳ" ở trang chủ hoặc Giới thiệu, chỉ dùng dữ kiện có trong kho. Lý do chọn GSAP:
   - đây là việc duy nhất CSS khó làm gọn;
   - miễn phí kể cả plugin;
   - C thử ghim + scrub dưới đúng CSP của mình: 0 vi phạm;
   - tải bằng `import()` chỉ ở màn đó, các trang khác không nặng thêm.

   Cái giá: tự viết phần tắt khi máy giảm chuyển động. Thêm nhỏ nếu muốn thẻ Khám phá trượt khi lọc: AutoAnimate (3,4 KB, tự tôn trọng giảm chuyển động).
3. **Không đề xuất:** Lenis (cuộn mượt hại trợ năng trên trang nhiều chữ), Lottie (cần người vẽ hoạt hình), React Spring (không có việc cần lò xo), Motion đầy đủ (nặng nhất, và đường `<style>` của bản React có thể vướng CSP).

## 5. Đã kiểm ↔ chưa kiểm
- **Đã chạy (C):** dung lượng gzip của 8 cách import; tìm `eval` / `new Function` / chèn `<style>` / `setAttribute("style")` trong bản đóng gói; thử thật dưới CSP: GSAP ghim + scrub, Motion bản không React.
- **C mở trang kiểm:** giấy phép GSAP (README GitHub), hỗ trợ trình duyệt của hiệu ứng theo cuộn (caniuse), số dung lượng Motion (tài liệu motion.dev).
- **Chỉ từ Codex:** hỗ trợ trình duyệt của chuyển cảnh (caniuse), giảm chuyển động của Lenis / AutoAnimate, số Lottie. Codex mở 21 trang, có 12 URL tự khai. Kết quả: `data/tra_cuu_cli/2026-11-14_fw-hieu-ung/`.
- **Chưa thử:** `AnimatePresence popLayout` của Motion dưới CSP; Lottie; số đo trong bản build Vite thật (Rollup có thể nhỏ hơn esbuild một chút).

## Bổ sung 11:29 14/11/2026 — đối chiếu với trang thật (B)
B chạy Playwright trên 8 trang thiết kế đẹp (`b_hieu_ung_tham_khao.md`; 2 trang chặn trình duyệt tự động, B không vượt):
- 0 / 6 trang chạy được dùng GSAP / three.js / Lottie / Framer Motion;
- 5 / 6 dùng hiệu ứng CSS theo vị trí cuộn (`animation-timeline`);
- băng chuyền dùng Swiper / Splide;
- Lenis chỉ có ở 1 trang;
- mọi trang đều tôn trọng `prefers-reduced-motion`.

Khớp kết luận mục 4: CSS thuần đủ.
