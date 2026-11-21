# Công cụ "liệt kê bài theo nhóm / cụm từ" cho câu xin danh sách và câu "nơi nào có đặc điểm X" (plan một trang)

Viết: 12:10 21/11/2026 (giờ `date`), phiên B. Người duyệt: phiên điều phối; bật hay không do chủ dự án quyết. Chưa code gì.
Từ dùng: *bài* = một file Markdown của kho (265 bài đang nằm trong chỉ mục) · *đoạn* = mảnh của bài mà bước tìm trả về (10 đoạn mỗi lần tìm) · *nhóm* = thư mục của bài trong kho ·
*thước* = bộ đo agent của phiên đo, chạy trên cả gpt-6-luna lẫn Claude Sonnet 5.5 · *sàn* = điều không được xấu đi.

## 1. Vì sao (số đếm 21/11, 0 đồng — hồ sơ riêng tư `data/…/b_ngu_canh_bai/`)

- Câu xin danh sách: mỗi mục của danh sách thường là MỘT bài riêng, mà 10 đoạn của lần tìm chỉ chạm vài bài — lăng 2 / 8 bài, chùa 1 / 6, chỗ ăn chay 1 / 6, chợ 3 / 6, quán cà phê 3 / 24, lễ hội 0 / 39.
  Đưa nguyên mục hay nguyên bài vào ngữ cảnh không thêm được bài nào mới (đã đếm: phương án đó bỏ).
- Câu "nơi nào có đặc điểm X" (5 câu của bộ mẫu: mở cửa 6–8 giờ sáng, hút chân không, gà rán trong một trung tâm thương mại, cho thuê trang phục, bán một món cụ thể): cả hai model chỉ đạt Đủ ý 2–3 / 5;
  model không biết mình thiếu mục nên Sonnet không tìm tiếp ở 4 / 5 câu.
- Thử cách khác: tìm NGUYÊN CỤM TỪ trên toàn văn từng bài (bằng script tìm kho của dự án): "hút chân không" ⇒ đúng 3 quán của đáp án (+ 1 bài đặc sản); "bột lộn" ⇒ đúng 2 quán; "gà rán" ⇒ đúng 4 thương hiệu;
  "06:00 - 08:00" ⇒ đúng 2 quán; "Hanbok / Kimono" ⇒ 2 quán của đáp án + 5 bài khác có chữ đó. Tức 5 / 5 câu, liệt kê theo cụm từ ở cấp BÀI chạm đủ đáp án — thứ tìm theo đoạn không làm được.

## 2. Đề nghị

Một công cụ thứ sáu, do CODE trả lời từ chính các bài kho đã nạp (không gọi model, không dữ liệu mới, không nhãn tự đặt):

`liet_ke_bai(nhom, cum_tu)`
- `nhom` — một trong chín nhóm = chín thư mục của kho: quán ăn · quán cà phê · món đặc sản · lễ hội · di tích · nghệ thuật biểu diễn · điểm đến · dịch vụ du lịch · vé; hoặc "tất cả". 100 % bài có nhóm (lấy từ đường dẫn).
- `cum_tu` — 0 đến 3 cụm từ. Có cụm từ ⇒ chỉ giữ bài mà TÊN BÀI hoặc TOÀN VĂN chứa ít nhất một cụm (so nguyên cụm, không phân biệt hoa thường; không phải biểu thức, dài tối đa 40 ký tự). Không có ⇒ mọi bài của nhóm.
- Trả về MỘT nguồn có mã [n] (cùng cách công cụ ngày / khoảng cách đang đăng nguồn ⇒ bộ kiểm trích nguồn hiện có không đổi): mỗi bài một dòng "Tên bài — dòng làm chứng", dòng làm chứng là dòng CỦA BÀI chứa cụm từ
  (hoặc dòng "Loại hình" / câu đầu mục "Tóm tắt" khi không có cụm từ; 132 và 110 bài có sẵn hai dòng này, bài còn lại dùng câu đầu tiên). Tối đa 40 dòng; dài hơn ⇒ dòng cuối "còn k bài nữa — thêm cụm từ để thu hẹp".
  Dòng đầu là trạng thái: "có N bài khớp" / "không có bài nào khớp — kho không có thông tin này".
- Model dùng nó cho câu "những … nào / có mấy … / kể hết … / nơi nào có …", rồi gọi `tim_kho` nếu cần chi tiết một nơi. Tối đa 2 lần mỗi câu; lượt có công cụ này được thêm 1 vòng.
- Nguồn dữ liệu lúc chạy: danh sách bài mà server đã nạp sẵn cho trang Khám phá (đã đối chiếu với chỉ mục khi khởi động) ⇒ không đọc gì ngoài kho, không thêm bảng.
- Một cờ `assistant.liet_ke_bai`, mặc định TẮT; tắt ⇒ danh sách công cụ gửi model giống từng byte. Cờ bật ⇒ đưa công cụ ở mọi lượt trợ lý có công cụ (không cổng từ khoá — mô tả công cụ nói rõ khi nào KHÔNG dùng; đo cột "gọi thừa").

Dòng ghi chú "danh sách có thể chưa đủ" (tính năng 20/11): GIỮ NGUYÊN chữ ở bản đầu — danh sách đủ so với KHO, chưa chắc đủ so với thực tế. Đổi chữ là đổi thứ người dùng thấy ⇒ để chủ dự án chọn sau khi có số.

## 3. Tiêu chí ghi TRƯỚC (đo cờ tắt ↔ bật cùng buổi, cả hai model; người chấm luna cho Đủ ý)

- **Phải được:** 7 câu xin danh sách đã đếm ở mục 1 — số bài đúng loại có mặt trong nguồn đưa cho model ≥ 80 % số bài kho có (hôm nay 0–50 %, riêng bãi biển 75 %) · 5 câu "đặc điểm X" của bộ mẫu — Đủ ý ≥ 4 ở ít nhất 4 / 5 câu mỗi model (hôm nay 2–3).
- **Sàn:** câu ngoài kho vẫn bị từ chối, và KHÔNG liệt kê thứ kho không có ("an toàn 10 — ngoài kho bị trả lời" rỗng; thêm 5 câu xin danh sách của thứ kho không có, ví dụ sân golf, hồ bơi: phải ra câu từ chối) · "ngoài phạm vi 10" không đổi ·
  chạm trần vòng vẫn 0 · lỗi trích nguồn 0 · lỗi kỹ thuật rỗng.
- **Không tụt quá nhiễu:** ba dòng "đạt máy" của thước, 85 câu bộ mẫu (Đúng, Đủ ý) — đặc biệt câu một dữ kiện không được chậm / dài ra vì model gọi công cụ thừa: gọi `liet_ke_bai` ở câu một dữ kiện ≤ 1 / 10 câu.
- Người thứ hai đọc tay 12 câu trả lời danh sách: mỗi tên nêu ra đều có trong nguồn [n]; dòng làm chứng không bị đọc ngược nghĩa (ví dụ bài viết "KHÔNG nhận hút chân không").

## 4. Rủi ro

- Cụm từ do MODEL chọn: chọn hẹp quá thì sót ("6h - 8h" ↔ "06:00 - 08:00"), rộng quá thì ra 40 dòng nhiễu. Giảm bằng: nhận tới 3 cụm, và model thấy số bài khớp ở dòng trạng thái để gọi lại lần hai.
- So nguyên cụm không hiểu nghĩa ⇒ có bài khớp chữ mà không khớp ý; vì vậy trả kèm dòng làm chứng và bắt người đọc tay kiểm (mục 3).
- Thêm một công cụ làm mọi lời gọi dài thêm khoảng 150 token và có thể bị gọi thừa ⇒ đo.
- Nguồn [n] của công cụ là "mục lục kho" chứ không phải một bài ⇒ dòng Nguồn dưới câu trả lời sẽ hiện tên nguồn mới này; chữ hiển thị do phiên điều phối chốt trước khi bật.

## 5. Không làm

Bảng thuộc tính có cấu trúc cho quán / điểm (đã ghi giới hạn 19/11, chưa mở lại) · tìm theo nghĩa ở cấp bài · thay bước tìm đoạn hiện có · đổi chữ dòng "danh sách có thể chưa đủ".
Kiểm trước khi xin review: cờ tắt giống byte; mỗi kiểu lượt một ca (lượt đầu, lượt có lịch sử, đường stream) khẳng định có / không có công cụ; hàm lọc thuần có test (không khớp ⇒ trạng thái "không có bài"; cắt trang; cụm từ lạ không thành biểu thức); một lượt thật mỗi model.
