# Báo cáo một việc xong — khuôn bốn ý (viết cho chủ dự án, lời thường)

**Việc:** <tên việc> · **Xong khi (ghi từ trước):** <lệnh … in ra … / người dùng làm X thì thấy Y> · **Giờ:** <lấy bằng lệnh `date`>

## 1. Người dùng thấy gì khác
Trước: <…>. Sau: <…>. Một ví dụ thật: <đầu vào ⇒ đầu ra>.

## 2. Bằng chứng
| Đo gì | Kết quả | So với mốc nào | Nhãn độ tin |
|---|---|---|---|
| test bằng đồ giả (không gọi model / dịch vụ thật) | <n đạt / m> | <mốc trước khi sửa> | [máy kiểm] |
| lượt thật (hệ thống + model thật) | <n lượt: … đạt, … trượt> | <mốc> | [máy kiểm] / [người thứ hai kiểm] / [chưa kiểm] |
| <số khác: tốc độ, tiền…> | <…> | <…> | <…> |

Cột "kết thúc kiểu gì" nếu có bảng từng ca: bình thường / chạm trần / lỗi. Ca sai tiêu biểu (2–3 ca, nguyên văn, không chép dữ liệu riêng): <…>
Ai kiểm: <phiên / người khác người viết> — <đã chạy lại gì>.

## 3. Chưa làm / giới hạn
- Chưa làm: <…>
- Tự hoãn + lý do: <…>
- Giới hạn đã biết: <tình huống → hệ quả → vì sao chấp nhận>

## 4. Cách thử trong 2 phút
1. Mở <đâu>. 2. Gõ / bấm <gì>. 3. Thấy <gì> là đúng; thấy <gì> là sai ⇒ báo lại.

---
Khi báo cho phiên điều phối / trong chat (không phải cho chủ dự án), dùng bảng ngắn: **đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra**.
