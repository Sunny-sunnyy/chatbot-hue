# Nhật ký 24/10/2026 — Phase 7B (thước đo) và tổ chức lại báo cáo

**Cập nhật lần cuối: 17:10 24/10/2026.** Tiền `gpt-6-luna` trong ngày: ~0,09 USD (~2.200 đồng), cộng
smoke của B9 nếu có (xem `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`).

## Tóm tắt

- Có **thước đo chính thức** cho chatbot và **điểm mốc** trên 176 câu: Đúng 4,43 / Đủ 4,28 / Trúng ý
  4,45. Thước đo ổn định (chạy lại chênh ≤ 0,011 điểm).
- Điểm yếu lớn nhất: bot **từ chối nhầm 22/158 câu** kho có đáp án (câu ghép nhiều nguồn, câu so sánh).
- Báo cáo cho bạn gom về **`bao_cao_he_thong/`**, mỗi khâu một file, đã viết lại cho Phase 0 → 7B và
  kiểm lại với code: không có lỗi làm hỏng chatbot, vài tài liệu/test cũ lệch (đã ghi).
- Cách làm việc của A/B/C cập nhật theo kinh nghiệm MekongAI.
- Đang dọn code/test/notebook Foods cũ và 2 collection Foods (B làm, phiên sau C kiểm).

## Bạn cần làm gì

- Phiên sau: mở A, B, C bằng `session_prompt/START_SESSION.md`; trả lời câu hỏi quyền phiên của A;
  brainstorm Phase 8 (hai câu lớn: trả lời phần có căn cứ hay từ chối cả câu; có tách bộ câu hỏi
  thành nhóm phát triển / nhóm giữ kín không).

## Trạng thái

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Phase 7B | Đã đóng (chưa có người chấm tay) | Có mốc để so mọi cải tiến Phase 8 |
| Chẩn đoán từ chối nhầm | 8 không tìm thấy đoạn · 10 có một vế · 4 có đủ mà vẫn từ chối | Chỉ hướng sửa: ngữ cảnh rộng hơn + cách prompt từ chối |
| Thử 10 đoạn ngữ cảnh (0,005 USD) | 10/22 câu hết từ chối | Dấu hiệu tốt, chưa chấm điểm |
| Báo cáo cho bạn | 10 file + mục lục trong `bao_cao_he_thong/` | Đọc một chỗ |
| Dọn Foods | Đang làm | Phiên sau kiểm rồi commit |

## Giải thích ngắn (để bạn tự nói lại được)

Muốn cải tiến chatbot thì trước hết phải có thước đo tin được. Hôm nay dự án dựng bộ chấm tự động:
chatbot trả lời 176 câu chuẩn, Claude chấm theo đáp án mẫu, `gpt-6-luna` chấm phụ để đối chiếu. Chạy
lại cho kết quả gần như y hệt, nên thước đo ổn định. Điểm cao ở câu một dữ kiện; mất điểm gần như do
bot từ chối nhầm khi chỉ tìm thấy một phần thông tin — đó là việc chính của Phase 8.

## Đọc thêm

- `bao_cao_he_thong/README.md` (mục lục), `BAO_CAO_DANH_GIA.md` (Phase 7B)
- `report_agent/2026-10-24_to_chuc_bao_cao/TONG_HOP.md` (kỹ thuật, đợt tổ chức báo cáo)
