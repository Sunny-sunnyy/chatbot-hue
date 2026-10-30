# Nhật ký 30/10/2026 — áp đợt 2 sửa kho, Qwen3-8B kém hơn, đo ngày hôm nay, đọc khoá học

**Cập nhật lần cuối: 16:12 30/10/2026 (kết phiên).** Tiền paid trong ngày: ≈ 0,061 USD (~1.500 đồng) — đợt 2 ≈ 0,047 (trần 0,10), Qwen3-8B ≈ 0,0089, đo ngày ≈ 0,0037, kiểm giá ≈ 0,0008 (tính theo giá phẳng; thật cao hơn ~20 % phần vào vì ghi đệm).

## Tóm tắt
- Mở phiên 10:30. Bạn xác nhận bối cảnh đồ án (càng giống sản phẩm thật càng tốt; 6–10 tuần tới bảo vệ) và **giữ thứ tự cũ**: đợt 2 sửa kho ⇒ Qwen3-8B ⇒ streaming ⇒ hội
  thoại nhiều lượt ⇒ đóng gói Phase 1–8 ⇒ mới bàn Phase 9.
- **Đợt 2 sửa kho đã vào chatbot** (13:31): 123 chỗ sửa trong 40 file; kho còn 204 file / 8.424 đoạn (−2 đoạn vì bỏ 2 dòng "Đơn vị quản lý"). Đo lại trước ↔ sau trên 176 câu
  Golden + 32 câu an toàn: **không làm hỏng** — 0 câu ngoài kho bị trả lời, 0 câu mới "nói sai", 0 câu đảo cảnh báo, điểm đủ ý gần như không đổi, từ chối nhầm 13 ⇒ 12.
  C đọc tay 8 câu: 0 lỗi nội dung kho. **Bạn đóng đợt 2 lúc 14:39, giữ sao lưu cả hai đợt.**
- **Qwen3-8B (model tạo vector lớn, gọi qua mạng) kém hơn e5-small ⇒ giữ e5-small:** làm mất đoạn đúng ở 3 / 40 câu thử + 3 câu kiểm, không câu nào được lợi rõ; tạo vector câu hỏi
  mất ~2,2 s thay vì 0,02 s. Đã xoá chỉ mục thử và bộ đệm (bạn: chỉ cần ghi kết quả).
- 7 sub-agent đọc khoá AI FDE, khoá AI Coding và cách làm của dự án kia ⇒ 3 đề xuất cải tiến cách làm; bạn cho thử cả 3 (ca dò kiểm theo cách khác; dời lịch sử file mở phiên; Codex review spec streaming một lần).
- Đo "ngày hôm nay": chatbot **không** tự đoán ngày rồi nói sai (0 / 12 + 0 / 11), nhưng từ chối nhầm 6 / 14 câu "tối nay / tuần này" ⇒ bạn quyết để trợ lý Phase 9. Giá ghi bộ
  đệm (bạn dán bảng giá): tiền / câu thật ≈ 0,00025 USD, vẫn dưới trần.

## Bạn cần làm gì
- Đã xong trong ngày: đóng đợt 2; chọn thứ tự; giá ghi đệm; 3 đề xuất cách làm (cho thử cả 3); xoá 6 nhánh cũ.
- Kết phiên: chạy các lệnh `!` A đưa (xoá bộ đệm 8B, tag + xoá nhánh Qwen, commit / push).
- Phiên sau: kết quả ChatGPT về streaming đã có chưa.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Đợt 2 sửa kho | áp xong; trước ↔ sau **không làm hỏng** | kho đúng nguồn hơn (vé / giờ / tên đơn vị), chatbot giữ chất lượng |
| Golden | bạn sửa đáp án mẫu 2 câu theo kho mới; nhãn đoạn đúng bản 5 (bạn duyệt 1 trích dẫn) | thước đo khớp kho mới |
| Qwen3-8B | **kém hơn**, không chọn (0,0089 USD) | giữ e5-small; đúng dự đoán về tốc độ, thêm: chất lượng tìm cũng không hơn |
| Ngày hôm nay | 0 câu nói sai; 6 / 14 từ chối nhầm | an toàn ở mức 1; trả lời theo ngày là việc của trợ lý (Phase 9) |
| Streaming / nhiều lượt | nháp phương án có; lỗi trích dẫn ở cấu hình hiện tại 0 / 489 | rút lại + báo lỗi khi trích dẫn hỏng là đủ; nhiều lượt: trình duyệt giữ lịch sử |
| Giới hạn đã biết | bảng 37 dòng (nháp, B kiểm đạt) | dùng khi đóng gói Phase 1–8 |

## Giải thích ngắn (để bạn tự nói lại được)
Kho có câu mâu thuẫn hoặc thiếu nguồn; đợt 2 chỉ giữ điều có nguồn đọc được và người thứ hai đọc lại khớp, còn lại bớt khẳng định. Sửa kho có thể làm chatbot tìm khác đi,
nên ta đo lại cùng bộ câu trước và sau, chấm mù cùng lượt, so với mức dao động tự nhiên đã đo trước — kết quả nằm trong mức dao động, không câu nào sai thêm. Giới hạn: người
chấm là Claude, chưa có người đọc kiểm; bộ "trước" là câu trả lời sinh từ 28/10 nên phần thay đổi do thời gian không tách riêng được.

## Đọc thêm
- `report_agent/2026-10-27_phan_ton_phase_cu/sua_kho_dot2_implementation.md` (kỹ thuật đợt 2)
- `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN 30/10"
