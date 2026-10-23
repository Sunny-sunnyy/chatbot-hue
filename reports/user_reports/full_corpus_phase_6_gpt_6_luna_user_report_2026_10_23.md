# Báo cáo dành cho người dùng: Giai đoạn 6 - Chatbot trả lời bằng gpt-6-luna

```text
Trạng thái: Đã xác nhận (User chọn Option A ngày 23-10-2026), PASS kèm giới hạn
Cập nhật lúc: 23-10-2026 +07
```

## 1. Bạn nhận được gì

Chatbot Huế giờ trả lời trên **toàn bộ kho dữ liệu** (món ăn, di tích, lễ hội,
nghệ thuật biểu diễn, du lịch) bằng model `gpt-6-luna`, rẻ và mạnh hơn bản
`gpt-5.4-nano` trước đây. Mỗi câu trả lời có trích dẫn [n] trỏ đúng tới nguồn
trong kho. Nếu không tìm thấy thông tin, chatbot nói rõ là không đủ thông tin
thay vì bịa.

Qdrant của dự án giờ chạy ở cổng riêng `localhost:6335`
(dashboard: `http://localhost:6335/dashboard`), nên chạy song song được với
mekongai-template ở cổng 6333.

## 2. Hệ thống hoạt động như thế nào

```text
câu hỏi -> tìm đoạn liên quan trong Qdrant (theo nghĩa + từ khóa)
-> chọn tối đa 5 nguồn -> gpt-6-luna viết câu trả lời có trích dẫn
-> backend kiểm tra trích dẫn hợp lệ -> trả {answer, sources}
```

Mọi model OpenAI của dự án, kể cả model chấm điểm cho các phase đánh giá sau,
giờ đều là `gpt-6-luna`.

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Kiểm tra code không tốn phí (141 test) | Đạt (Reviewer chạy lại) | Đổi model/port không làm hỏng gì |
| Dữ liệu Qdrant trước/sau | Nguyên vẹn, 33.840 điểm | Không mất hay sửa dữ liệu |
| Gọi thật `gpt-6-luna`, đúng 5 lượt | 4 Đạt / 1 Không đạt | Chi phí đúng giới hạn bạn duyệt |
| Câu hỏi sự kiện (đồi Vọng Cảnh) | Đạt, trích dẫn đúng | Lỗi 502 lần trước không còn |
| Câu hỏi ngoài phạm vi (tàu điện TP.HCM) | Đạt, từ chối đúng | Không bịa thông tin |
| Câu hỏi tổng hợp (công trình hoàng gia) | Đạt nhưng chỉ dùng 1 nguồn | Chưa chứng minh tổng hợp nhiều nguồn |
| Câu hỏi giá vé + miễn giảm Đại Nội | Không đạt | Bước tìm kiếm không thấy bảng giá vé |
| Mekong | Không bị ảnh hưởng | Hai dự án chạy song song được |

## 4. Cách bạn kiểm tra thêm nếu cần

Không bắt buộc. Nếu muốn tự xem: bật Qdrant bằng `docker compose up -d` tại thư
mục dự án, mở `http://localhost:6335/dashboard` để thấy các collection. Chạy
chatbot sẽ gọi API có phí.

## 5. Giới hạn và bước tiếp theo

- **Bảng giá vé không được tìm thấy:** với câu hỏi gộp "giá vé + miễn giảm",
  đoạn bảng giá vé lẻ Đại Nội không nằm trong 30 kết quả đầu. Đây là điểm yếu
  của bước tìm kiếm với dữ liệu dạng bảng. Phase 8 (benchmark tìm kiếm) sẽ xử
  lý, và câu hỏi này được giữ làm case cụ thể.
- **Tổng hợp nhiều nguồn và giữ điều kiện** chưa được chứng minh bằng bài thử
  nhỏ này. Phase 7 sẽ đo bằng 150–200 câu hỏi chuẩn.
- Model chấm điểm cũng là `gpt-6-luna`, nên khi chấm có thể thiên vị cách viết
  của chính nó. Giới hạn này sẽ được ghi khi báo cáo Phase 7/8.
- Chưa kiểm chứng `gpt-6-luna` có nhận tham số `temperature` của script đánh giá
  Foods cũ hay không; sẽ kiểm khi tới phase đánh giá.
- Bước tiếp theo: thiết kế Phase 7A (bộ câu hỏi chuẩn cho toàn bộ dữ liệu).
  Phase này chỉ bắt đầu sau brainstorming, spec và plan được bạn duyệt.
