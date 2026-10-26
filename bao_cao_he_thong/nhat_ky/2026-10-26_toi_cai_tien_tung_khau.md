# Nhật ký 26/10/2026 (tối) — đợt cải tiến từng khâu: phân loại lỗi, luật nhận, ba thí nghiệm đầu

**Cập nhật lần cuối: 22:31 26/10/2026.** Tiền paid tối nay: 0,0027 USD (~70 đồng), đo từ log.

## Tóm tắt

- Trước khi thử cải tiến, nhóm **phân loại lỗi** trên chatbot dùng 10 đoạn context. Trên 88 câu thử chính còn 10 câu kém, và cả 10 đều kém vì
  **khâu tìm không đưa đủ thông tin cho model**, không phải vì model trả lời sai. Phần lỗi riêng của khâu trả lời thì nhỏ.
- Vì vậy bạn chọn **phạm vi B**: thử ở khâu trả lời **và** ở khâu tìm, không ghi gì vào Qdrant. Mọi thứ ghi thành **mục 10 của spec 8.2**, có luật
  nhận ghi trước và người khác kiểm trước khi chạy.
- Bạn đặt ba nguyên tắc dùng chung cho mọi phần sau này: **chất lượng cần thiết trước, rồi mới tối ưu**; **hiệu suất = tiền và tốc độ**; **đo theo mục
  tiêu sản phẩm cuối cùng**.
- Ba thí nghiệm đầu đều **không qua**, và đều dừng sớm đúng luật nên gần như không tốn tiền: nới nhóm ứng viên lên 100 đoạn (K1) làm mất 1 câu;
  "trả lời phần có căn cứ" (R2) lại trả lời 1 câu ngoài kho; "nêu đủ chi tiết" (R3) không đủ câu để kết luận nên không chạy.
- Điều học được lớn nhất: đoạn đúng **đã nằm trong nhóm ứng viên** nhưng bị **xếp hạng thấp**. Thí nghiệm tiếp theo (K3: cho model xếp lại) đã có kế
  hoạch được duyệt, để phiên sau.
- Hook git giờ tự chặn mọi dòng mới chép trùng Golden, kho hoặc câu kín.
- **Chatbot không đổi.**

## Bạn cần làm gì

- Khi tiện: trả lời 4 câu **mục tiêu sản phẩm** (`session_prompt/Project_Status.md` §1): người dùng chính là ai; câu trả lời thế nào là "dùng được";
  lỗi nào tệ nhất; chờ tối đa bao lâu, tiền tối đa bao nhiêu mỗi câu, chạy ở đâu.
- **Q2:** có đồng ý nhóm test chỉ dùng để xác nhận "không làm hỏng" không (A khuyên đồng ý — nhóm test quá nhỏ để thấy "tốt hơn").
- **B0:** đọc cặp mù 20 câu (`data/phase_8_2/b0/nhan_xet_user.md`, ~30–45 phút) — cần trước khi chatbot dùng 10 đoạn context.
- Xóa nhánh `dot3` (đã nằm trong `main`): `! git push origin --delete dot3 && git branch -d dot3`.
- Phiên sau: cấp lại quyền phiên (điều phối, trần tiền).

## Trạng thái

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Phân loại lỗi khâu trả lời (C36) | Đã xử lý | 10 / 88 câu kém, cả 10 thiếu thông tin; 5 câu từ chối khi có một phần thông tin; 9 câu trả lời quá gọn |
| Phân loại lỗi khâu tìm (B42) | Đã xử lý | 18 / 40 câu thiếu đoạn đúng ở 10 đoạn: nửa ngoài nhóm 30 ứng viên, nửa bị xếp sau; câu tự nhiên không lợi từ 10 đoạn |
| Phần code "10 đoạn + NFC" lên `main` mới (B41) | Đã xử lý (chưa vào chatbot) | Kiểm lại đạt, 0 USD; vào chatbot sau khi bạn đọc cặp mù |
| K1 — nới nhóm ứng viên 30 → 100 | Đã thử, chưa áp dụng | Kém hơn: thêm 2 câu nhưng mất 1 câu; chỗ nghẽn là xếp hạng |
| R2 — trả lời phần có căn cứ | Đã thử, chưa áp dụng | Kém hơn: trả lời 1 câu ngoài kho (cùng kiểu lỗi 8.1); hướng này gác lại |
| R3 — nêu đủ chi tiết | Chưa thực hiện | Không đủ câu để kết luận (6 câu); cần thêm câu tự nhiên |
| R4 — thước kiểm số liệu trong câu trả lời | Đã xử lý | Chỉ dùng để chọn câu đọc lại, không phải chỉ số tự động |
| K3 — model xếp lại 30 đoạn | Chưa thực hiện | Kế hoạch duyệt, trần 0,20 USD; chạy phiên sau |
| Hook quét trùng Golden / kho / câu kín | Đã xử lý, đóng gói | Máy tự chặn khi commit; < 1 giây; 0 báo nhầm |

## Giải thích ngắn (để bạn tự nói lại được)

Chatbot trả lời kém chủ yếu vì 10 đoạn đưa cho model thiếu thông tin cần thiết. Nới rộng nhóm đoạn ứng viên giúp tìm thấy đoạn đúng nhiều hơn
(31 → 37 / 40 câu) nhưng không đưa được chúng lên 10 đoạn đầu (22 → 23), lại đẩy mất một đoạn đúng của câu khác — nên vấn đề là **cách xếp hạng**.
Sửa ở khâu trả lời (cho model trả lời một phần) vướng rủi ro trả lời cả câu ngoài kho, nên gác. Giới hạn: bộ thử nhỏ và điểm do Claude chấm — kết
luận là tạm cho tới khi có đánh giá của bạn (B0).

## Đọc thêm

- `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md` (kỹ thuật, theo giờ)
- `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` §10 (luật nhận, biến thể)
- `bao_cao_he_thong/BAO_CAO_TIM_KIEM.md`, `BAO_CAO_SINH_CAU_TRA_LOI_API.md` (mục "đã thử")
