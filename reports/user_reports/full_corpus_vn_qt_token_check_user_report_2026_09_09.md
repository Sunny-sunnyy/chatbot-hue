# Hai mẫu giá vé Ca Huế đã đo lại đúng ranh giới

Trạng thái: user đã xác nhận; khảo sát approved/completed.

## 1. Bạn nhận được gì

Cả mẫu khách Việt Nam và khách quốc tế giữ câu dẫn khảo sát tháng 09/2026,
header bảng, nguyên hàng giá và Không bao gồm, đồng thời vừa giới hạn input
của ba embedding models và MiniLM với hai câu hỏi đã chọn.

## 2. Cách khảo sát hoạt động

Implementer lấy nguyên input từ artifact parser đã sửa, đối chiếu nguồn rồi
đếm token bằng tokenizer local. Không chạy model trả lời hoặc thay index.

## 3. Codex đã kiểm và quan sát gì

Reviewer đọc code/kết quả, đối chiếu hai inputs với artifact gốc và tám đoạn
bằng chứng với nguồn: khớp. Counts do Implementer đo: VN 290/290/224 cho ba
embedding models, MiniLM 411/453; QT 268/268/208, MiniLM 385/427. Tất cả vừa
limits tương ứng. Reviewer không chạy lại tokenizer vì không có mâu thuẫn.

## 4. Cách bạn kiểm tra thêm

Không bắt buộc tự chạy lại. Chi tiết và giới hạn tại
[Codex review](../full_corpus_vn_qt_token_check_codex_review_2026_09_09.md).

## 5. Giới hạn và bước tiếp theo

Đạt độ dài input không chứng minh câu trả lời chính xác hoặc mọi câu hỏi đều
vừa. Đây không phải approval written spec/plan hoặc runtime toàn corpus.
User đã xác nhận khảo sát hai input. Reviewer đóng khảo sát và tiếp tục
hoàn thiện written spec; không cần thêm một lượt xác nhận hoặc chạy lại.
