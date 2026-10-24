# Nhật ký 24/10/2026 (tối) — dọn phần món ăn cũ, mở Phase 8.1 rà quyết định

**Cập nhật lần cuối: 19:58 24/10/2026.** Tiền paid phiên tối: 0,0013 USD (~33 đồng; chạy thử 10 câu
sau khi dọn). Cả ngày: ~0,09 USD (~2.300 đồng).

## Tóm tắt

- **Dọn xong phần món ăn cũ:** gỡ 42 file code/test/notebook không còn dùng và 2 kho món ăn trong
  Qdrant. Chatbot chạy **y như trước**: kết quả tìm kiếm giống từng byte, 191 test đạt, API khỏe, chạy
  thử 10 câu không lỗi. Qdrant còn đúng 1 kho đang dùng.
- **Phase 8 tách hai bước:** 8.1 = Claude rà lại mọi quyết định của Phase 0–7 (trước đây AGY/Codex làm),
  thí nghiệm so với cách cũ làm mốc, **chưa đổi chatbot**; 8.2 = cải tiến dựa trên số đo 8.1.
- **Bảng rà 56 quyết định:** chỉ 2 từng được so trên toàn kho; 29 chưa từng so; 16 chọn mặc định không
  ghi lý do. Chỗ đáng lo nhất: cách chia đoạn chưa từng đo, giới hạn 5 đoạn cho model, model sinh chọn
  qua 5 câu, thước đo chưa đủ để kết luận "tốt hơn".
- Đã viết yêu cầu nghiên cứu (21 câu) cho ChatGPT.

## Bạn cần làm gì

- Xác nhận đóng việc dọn món ăn (B9) — đã kiểm chéo đạt.
- Gửi yêu cầu nghiên cứu cho ChatGPT:
  `gửi chatgpt/2026-10-24/tìm thông tin/phase_8_1_decision_audit_2026_10_24.md`.
- Brainstorm tiếp 8.1 (mỗi lần một câu): tách bộ câu hỏi giữ kín; chấm tay 20 câu; gắn đoạn đúng cho
  30–40 câu khó; trả lời phần có căn cứ hay từ chối; có so với model Qwen như cam kết cũ không.
- Gỡ vài thư viện không còn ai dùng (gradio, polars, underthesea…) — cần bạn duyệt.

## Trạng thái

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Dọn món ăn cũ (B9) | Xong, kiểm chéo đạt, commit `1832201` | Repo bớt ~15.000 dòng (code, test, notebook, CSV); chatbot không đổi |
| Báo cáo khâu về mẫu mới | 4 file của C xong; 4 file của B đang làm | Mỗi file có Tóm tắt đầu + checklist 5 mức |
| Bảng rà quyết định 8.1 | Xong, A kiểm đạt | Biết chỗ nào chưa từng được thử |
| Spec 8.1 | Chưa viết | Chờ nghiên cứu + câu trả lời của bạn |

## Giải thích ngắn (để bạn tự nói lại được)

Trước khi cải tiến, mình kiểm xem các lựa chọn cũ có bằng chứng không. Kết quả: phần lớn chưa từng được
so sánh trên toàn kho, nhiều cái chỉ thử trên 45 câu món ăn với cách chia đoạn khác. Vì vậy 8.1 sẽ sửa
thước đo trước, rồi đo lại từng lựa chọn với cách cũ làm mốc; chatbot chỉ đổi ở 8.2.

## Đọc thêm

- `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_KHO_DU_LIEU.md`, `BAO_CAO_LUU_TRU_QDRANT.md`
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` (kỹ thuật)
- `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md` (kiểm chéo dọn món ăn)
