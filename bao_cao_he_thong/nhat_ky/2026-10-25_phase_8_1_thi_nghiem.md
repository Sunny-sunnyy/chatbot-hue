# Nhật ký 25/10/2026 (chiều) — Phase 8.1: thử lại các quyết định cũ

**Cập nhật lần cuối: 15:27 25/10/2026 — bạn đã đóng Phase 8.1.** Tiền paid trong ngày: 0,1653 USD (~4.100 đồng), chỉ `gpt-6-luna`.

## Tóm tắt
Chiều nay ba session (A điều phối, B và C làm) chạy hết các thí nghiệm của Phase 8.1. Mỗi thí nghiệm có luật quyết ghi
trước, người khác kiểm lại, rồi mới commit. Chatbot đang chạy **không đổi gì**. Kết quả: chỉ một thay đổi đủ chắc để đề
xuất — **đưa cho model 10 đoạn thay vì 5** (câu trả lời đầy đủ hơn rõ ở cả bộ thử lẫn bộ kiểm). Các thử khác (chia đoạn to
hơn, model xếp hạng lại, đổi cách tách từ, đổi prompt, mức suy luận) không tốt hơn hoặc làm rơi đoạn đúng của vài câu.
Phát hiện lớn nhất: người dùng **gõ không dấu** thì tìm kiếm gần như hỏng — 15:15 bạn quyết để ngoài phạm vi (người dùng gõ có dấu).

## Bạn cần làm gì
- Không có việc gấp. Đã xong hôm nay: bạn duyệt mẫu câu kín bản 5 (15:15), A khóa bộ câu kín + baseline (15:22), bạn đóng
  Phase 8.1 (15:27).
- Phiên sau: brainstorm Phase 8.2 với A. Trước khi đổi chatbot, bạn chấm tay ~20 câu (mốc người).

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Sửa thước đo | Đáp án tham chiếu: sửa 10 câu Golden + 5 đáp án câu kín; câu kín thêm dấu; 9 câu bất đồng giữ | Judge chấm công bằng hơn |
| Xếp hạng lại (GPU + luna) | Không tốt hơn; 2 model GPU làm rơi 1–3 câu | Giữ không xếp hạng lại |
| Sinh câu trả lời | **10 đoạn tốt hơn** (đã xác nhận trên bộ kiểm); prompt / mức suy luận không tốt hơn | Đề xuất 8.2 |
| Từ khóa (BM25) | Không cách tách từ nào tốt hơn; bỏ dấu cứu câu không dấu nhưng hại câu có dấu | Thử "chỉ bỏ dấu khi câu không dấu" ở 8.2 |
| Chia đoạn | 12 cách, không cách nào tốt hơn; đoạn to tìm thấy nhiều hơn nhưng chiếm chỗ | Giữ cách chia hiện tại |

## Giải thích ngắn (để bạn tự nói lại được)
Chatbot tìm 5 đoạn rồi đưa cho model viết câu trả lời. Đo lại cho thấy đoạn đúng thường đã được tìm thấy nhưng bị xếp thấp,
nên không lọt vào 5 đoạn. Cho model đọc 10 đoạn thì nhiều câu có đủ bằng chứng hơn và trả lời đầy đủ hơn, tốn thêm khoảng
một nửa tiền mỗi câu (vẫn dưới 0,0003 USD). Giới hạn: bộ thử nhỏ, điểm do Claude chấm, chưa có người chấm.

## Đọc thêm
- `report_agent/2026-10-24_phase_8_1_ra_soat/TONG_HOP.md` (kỹ thuật), `phase_8_1_g5_synthesis.md` (kết luận + đề xuất 8.2)
- `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md`, `BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `BAO_CAO_CHIA_DOAN.md`,
  `BAO_CAO_EMBEDDING_TU_KHOA.md`, `BAO_CAO_DANH_GIA.md`, `BAO_CAO_BO_CAU_HOI_GOLDEN.md` (B / C đang thêm mục 8.1)
