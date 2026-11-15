# Đếm: hỏi đích danh cơ sở lưu trú có bị từ chối không (E · 12:29 15/11/2026, `date`)

A giao (C thấy một câu đích danh một khu nghỉ dưỡng ven biển bị kho từ chối, dù bài lưu trú có nhắc). Lõi trợ lý thật, cờ theo `settings.yaml`, tra web thật.
Script `data/dem_ten_ks_2026-11-15/tools/hoi.py` + `hoi_vedana.py`; kết quả `ket_qua.jsonl`, `ket_qua_vedana.jsonl` (private). **Tiền: 18 câu ≈ 0,02 USD.** Chưa sửa gì.

## Kết quả
- 15 cơ sở có tên trong 5 bài lưu trú (đủ hạng 2–5 sao; trung tâm, phía tây, ven biển hai phía). Câu "Khách sạn X ở đâu, có tốt không?":
  - **Từ chối: 0 / 15.** Mọi câu trả lời bằng bài lưu trú (địa chỉ + hạng sao theo danh mục, có trích dẫn).
  - **Bước tìm:** top 10 của lần tìm đầu có đoạn chứa tên ở **15 / 15** câu (14 câu ở hạng 1–2; 1 câu ở hạng 4).
  - **Mục web: 14 / 15.** Lý do: phần "có tốt không" (nhận xét của khách) kho không có ⇒ trả lời ghi "Tư liệu chưa có thông tin về: đánh giá…" ⇒ mở mục web cho ý thiếu. Đúng thiết kế "câu nhiều ý" (bật 14/11). Câu không mở web: cơ sở mà kho có mô tả đủ để kết luận cao cấp (5 sao + tiện ích).
- Thêm 3 cách hỏi ngắn cho chính cơ sở C thấy bị từ chối (không có chữ "Khách sạn"; "ở đâu?"; "có tốt không?"; "cho mình biết về…"): **0 / 3 từ chối**, 0 / 3 mục web, tên ở top 10 cả 3 lần.

## Kết luận
- **Không tái tạo được lỗi từ chối** (0 / 18). Bước tìm đưa đúng đoạn lên top 10 ở mọi câu. Nếu ca C thấy là thật, khả năng là (a) trước lần dựng chỉ mục 11:22 (kho đổi), hoặc (b) nhiễu từ chối của model (đã biết, ví dụ case Golden 67). E chưa có câu nguyên văn của C để chạy lại ×5 ⇒ đề xuất: C gửi đúng câu đó, chạy ×5 trên main (≈ 0,005 USD).
- Không thấy lỗi ở bước tìm cho tên khách sạn. Không cần sửa kho hay chỉ mục vì việc này.
