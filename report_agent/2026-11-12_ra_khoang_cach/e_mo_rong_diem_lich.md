# Đếm trước khi xây: mở rộng bảng điểm của lịch (E · 12:55 15/11/2026, `date`)

A giao (đề xuất E). Chưa sửa gì. Tiền ≈ 0,009 USD (≈ 0,003 A ước; vượt do chạy thêm ca đối chứng, xem mục 2).

## 1. Khoảng trống (0 USD, `data/mo_rong_diem_lich_2026-11-15/tools/dem_can_cu.py` ⇒ `dem_can_cu.json`)
- Bảng điểm lịch (`diem_v8`) có **34 điểm**. Kho có 83 bài nơi / di tích. Bỏ 11 bài không phải nơi đến (di sản tư liệu, phi vật thể, bài tổng, nằm trong điểm khác, nơi trung chuyển) ⇒ **41 nơi thật chưa vào lịch** (chùa, cầu, chợ, đèo, đầm, bãi biển, làng nghề, suối…).
- Căn cứ trong chính bài kho (dò bằng mẫu chữ — **ước**, cần người đọc xác nhận): giờ mở cửa / "tự do" 17 / 41 · **thời lượng tham quan 1 / 41** · nhắc trong nhà / ngoài trời 26 / 41.
- So với 34 điểm hiện có: thời lượng lấy từ **web 24**, kho 8, ước 2; giờ mở phần lớn từ tra cứu (22 / 34 không có dòng kho). ⇒ Thêm điểm mới **cần tra web** cho thời lượng + giờ, như lần dựng bảng trước. Toạ độ (quán / bản đồ) cần Places (~0,001 USD / điểm).

## 2. Người dùng gặp gì hôm nay (giao diện thật, `tools/pw_them.py`, ảnh `anh/them_*.png`)
- Lịch 3 ngày ⇒ "đổi thành 2 ngày" (ca đối chứng): **sửa đúng**.
- "Thêm chùa Từ Hiếu / cầu Trường Tiền / đèo Hải Vân vào lịch": **3 / 3 trả "Không đổi được: «…» chưa có trong danh sách điểm của lịch."** Trung thực, nhưng khách bị từ chối với nơi nổi tiếng ⇒ đúng khoảng trống việc này sẽ lấp.
- **Bẫy của E (ghi để khỏi lặp):** lượt thử đầu bằng `POST /api/chat` (không stream) **không đi vào luồng sửa lịch**. Cả câu đối chứng "đổi thành 2 ngày" ở đó cũng ra lời văn tự do, có câu "thêm … vào ngày 3" mà lịch không đổi. E suýt báo lỗi "nói đã thêm mà không thêm" — **sai, do kịch bản**: giao diện đi đường stream và ở đó sửa lịch chạy đúng. Đếm hành vi sửa lịch phải đi qua giao diện / đường stream. (Đường API không stream có phải chủ đích không thì chưa kiểm; người dùng không đi đường đó.)

## 3. Đề xuất (chờ A / User)
- Chọn ~10 nơi theo hai thước: (a) hay được hỏi thêm — nơi nổi tiếng, như 3 ca trên; (b) theo ý C: chỗ lịch đang thiếu điểm (sở thích ít điểm, cụm thưa). Cần đếm (b) trên mô phỏng 3.840 khung trước khi chọn (0 USD).
- Mỗi điểm: căn cứ kho trước, thiếu thì tra web (Serper / Codex, ghi nguồn + ngày), không ước. Thiếu giờ / thời lượng có căn cứ ⇒ không thêm.
- Sau khi thêm: mô phỏng 3.840 khung (sàn hiện có) + bộ lịch đã thấy. Lịch đổi cho mọi khung có sở thích chạm điểm mới ⇒ cần đo lại cỡ "câu chạm".
