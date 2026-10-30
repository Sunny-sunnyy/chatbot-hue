# Nhật ký 30/10/2026 — áp đợt 2 sửa kho, chuẩn bị Qwen3-8B, đọc khoá học

**Cập nhật lần cuối: 14:17 30/10/2026.** Tiền paid trong ngày: ≈ 0,048 USD (~1.200 đồng) — đợt 2 ≈ 0,047 (trần 0,10), kiểm giá phần vào ≈ 0,0008.

## Tóm tắt
- Mở phiên 10:30. Bạn xác nhận bối cảnh đồ án (càng giống sản phẩm thật càng tốt; 6–10 tuần tới bảo vệ) và **giữ thứ tự cũ**: đợt 2 sửa kho ⇒ Qwen3-8B ⇒ streaming ⇒ hội
  thoại nhiều lượt ⇒ đóng gói Phase 1–8 ⇒ mới bàn Phase 9.
- **Đợt 2 sửa kho đã vào chatbot** (13:31): 123 chỗ sửa trong 40 file; kho còn 204 file / 8.424 đoạn (−2 đoạn vì bỏ 2 dòng "Đơn vị quản lý"). Đo lại trước ↔ sau trên 176 câu
  Golden + 32 câu an toàn: **không làm hỏng** — 0 câu ngoài kho bị trả lời, 0 câu mới "nói sai", 0 câu đảo cảnh báo, điểm đủ ý gần như không đổi, từ chối nhầm 13 ⇒ 12.
  Đợt 2 chờ C đọc xong danh sách câu cần xem tay rồi bạn đóng.
- Code thí nghiệm Qwen3-8B viết xong và qua kiểm 2 vòng; **chưa chạy** (chạy sau đợt 2).
- 7 sub-agent đọc khoá AI FDE, khoá AI Coding và cách làm của dự án kia ⇒ 3 đề xuất cải tiến cách làm chờ bạn duyệt.
- Phát hiện mới: chatbot **không biết hôm nay là ngày nào** (câu "hôm nay có mở cửa không" có thể bị trả lời chắc mà sai — lỗi mức nặng nhất); mỗi lần gọi model đều ghi
  bộ đệm mà không đọc lại (tiền / câu có thể đang ghi thiếu ~20 %).

## Bạn cần làm gì
- Đóng đợt 2 (sau khi C đọc xong) — A trình.
- Chọn: đo "ngày hôm nay" trước hay Qwen3-8B trước.
- Xem billing OpenAI: `gpt-6-luna` tính giá phần "cache write" thế nào.
- Duyệt 3 đề xuất cách làm (Đ1–Đ3); 2 lệnh `!` xoá 6 nhánh hồ sơ cũ (tag `hoso/*` đã có).

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Đợt 2 sửa kho | áp xong; trước ↔ sau **không làm hỏng** | kho đúng nguồn hơn (vé / giờ / tên đơn vị), chatbot giữ chất lượng |
| Golden | bạn sửa đáp án mẫu 2 câu theo kho mới; nhãn đoạn đúng bản 5 (bạn duyệt 1 trích dẫn) | thước đo khớp kho mới |
| Qwen3-8B | code + plan duyệt, chưa chạy | dự đoán: khó qua điều kiện tốc độ (tạo vector câu hỏi qua mạng ~1–3 s) |
| Ngày hôm nay | plan đo duyệt (15 câu tự viết, trần 0,01 USD), chưa chạy | nếu có lỗi ⇒ thí nghiệm thêm ngày vào prompt (bạn duyệt) |
| Streaming / nhiều lượt | nháp phương án có; lỗi trích dẫn ở cấu hình hiện tại 0 / 489 | rút lại + báo lỗi khi trích dẫn hỏng là đủ; nhiều lượt: trình duyệt giữ lịch sử |
| Giới hạn đã biết | bảng 36 dòng (nháp, B kiểm) | dùng khi đóng gói Phase 1–8 |

## Giải thích ngắn (để bạn tự nói lại được)
Kho có câu mâu thuẫn hoặc thiếu nguồn; đợt 2 chỉ giữ điều có nguồn đọc được và người thứ hai đọc lại khớp, còn lại bớt khẳng định. Sửa kho có thể làm chatbot tìm khác đi,
nên ta đo lại cùng bộ câu trước và sau, chấm mù cùng lượt, so với mức dao động tự nhiên đã đo trước — kết quả nằm trong mức dao động, không câu nào sai thêm. Giới hạn: người
chấm là Claude, chưa có người đọc kiểm; bộ "trước" là câu trả lời sinh từ 28/10 nên phần thay đổi do thời gian không tách riêng được.

## Đọc thêm
- `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` (kỹ thuật đợt 2)
- `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN 30/10"
