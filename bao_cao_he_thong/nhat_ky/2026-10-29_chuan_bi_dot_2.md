# Nhật ký 29/10/2026 — chuẩn bị đợt 2 sửa kho, đo nhiễu thước lỗi nặng

**Cập nhật lần cuối: 21:36 29/10/2026.** Tiền paid trong ngày: ≈ 0,0081 USD (~200 đồng).

## Tóm tắt
- Phiên tối (19:13 → kết phiên). Bạn trả lời 6 câu mở phiên: quyền như 28/10, trần đợt 2 0,10 USD, duyệt thí nghiệm Qwen3-8B (chạy sau đợt 2), gửi ChatGPT yêu cầu streaming,
  nhận bộ 32 câu an toàn làm bộ kiểm bắt buộc.
- Bạn đặt luật cho nội dung kho: **câu nào không chắc thì bỏ hoặc sửa thành câu chắc chắn**. B soạn lại bản sửa đợt 2 theo luật này (21 mục: sửa theo nguồn, làm yếu câu đang mâu
  thuẫn, hoặc không sửa có lý do). A tự đọc lại một nguồn web và thấy bản "sẵn sàng" cũ vẫn còn một con số gắn sai chủ thể — luật của bạn bắt được lỗi mà 2 vòng review cũ bỏ sót.
- C đo nhiễu thước lỗi nặng: chạy lại 32 câu an toàn, chatbot tự dao động ±2 câu "sai về điều kiện / an toàn" giữa hai lượt giống hệt ⇒ sàn đặt theo nhiễu đó, không phải "0".
- **Chưa áp đợt 2 vào kho**: C review vòng 1 yêu cầu sửa 3 chỗ; một bước cần bạn gõ lệnh xóa ở terminal B; và công cụ kiểm an toàn của agent lỗi máy chủ nhiều lần tối nay.

## Bạn cần làm gì
- Gửi ChatGPT yêu cầu streaming (file trong `gửi chatgpt/2026-10-28/tìm thông tin/`), lưu kết quả vào `…/2026-10-28/kết quả nghiên cứu/`.
- Gửi prompt mới cho Claude ở dự án kia (file trong `data/external_project_notes/`, tên có ngày 29/10).
- Phiên sau: có mặt lúc áp đợt 2 (bước xóa 3 đích dữ liệu cũ do bạn gõ).

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Bản sửa đợt 2 (B90) | bản 4 xong; review vòng 1 "cần sửa" (3 major) | chưa đụng kho; phiên sau sửa + review vòng 2 rồi áp |
| Đo nhiễu bộ an toàn (C84) | nhiễu ±2 câu, người chấm ổn định (0 lệch) | sàn: tối đa 2 câu sai mới, câu nào sai mới phải sinh lại 3 lần; đảo cảnh báo = 0 |
| Khoá AI FDE | bạn đưa bản đầy đủ tuần 1–3; đối chiếu với dự án **chưa chạy** (lỗi máy chủ) | phiên sau |

## Giải thích ngắn (để bạn tự nói lại được)
Kho có những câu tự mâu thuẫn hoặc thiếu nguồn. Thay vì đoán phía nào đúng, đợt 2 chỉ giữ điều có nguồn đọc được và người thứ hai đọc lại khớp; còn lại bớt khẳng định. Trước khi
sửa, ta đo xem chatbot tự dao động bao nhiêu trên câu an toàn, để sau khi sửa biết thay đổi là thật hay chỉ là nhiễu. Giới hạn: bộ 32 câu do agent viết, chưa có người đọc kiểm.

## Đọc thêm
- `session_prompt/CURRENT_HANDOFF.md` mục "PHIÊN 29/10"
- `report_agent/2026-10-27_phan_ton_phase_cu/do_loi_nang_aa_implementation.md`, `sua_kho_dot2_do_plan_review.md`
