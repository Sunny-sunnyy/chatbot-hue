# Báo cáo dành cho người dùng: Giai đoạn 6 - Sinh câu trả lời có nguồn và JSON API

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 13-08-2026 18:08 +07
Tệp thực hành cần kiểm tra: notebooks/06_generation_and_api.ipynb
```

## Bạn nhận được gì từ giai đoạn này

Chatbot đã có phần tạo câu trả lời tiếng Việt từ các đoạn dữ liệu được truy
xuất, cùng API JSON tối giản để ứng dụng khác có thể gọi. Câu trả lời chỉ được
phép dùng các nguồn đã đưa vào ngữ cảnh; khi không có bằng chứng, hệ thống trả
lời an toàn thay vì gọi model hoặc suy đoán.

## Hệ thống hoạt động như thế nào

`POST /api/chat` nhận câu hỏi, tìm các đoạn liên quan, giới hạn ngữ cảnh rồi gửi
cho answer generator. Generator trả câu trả lời và các mã nguồn đã dùng; API
chỉ trả các nguồn đó theo thứ tự bằng chứng. Lỗi provider, timeout hoặc output
không đúng cấu trúc đều được trả thành lỗi JSON an toàn, không tự thử lại.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Backend live-only suite | 205 test đạt | Test dùng Qdrant, E5/MiniLM và OpenAI thật khi cần; không còn fake/mock dependency. |
| Notebook runtime thật | Đạt | Notebook đi qua `/api/chat` thật, Qdrant/E5 thật và đúng một OpenAI call. |
| Live smoke | Đạt trong ngân sách | 12 calls được user phê duyệt, tổng chi phí 0,01493875 USD, không retry. |

Live smoke phủ sáu loại câu hỏi. Đợt đầu trả lời đạt cả sáu; đợt đo usage thật
có một output model không hợp lệ và hệ thống chặn đúng thiết kế, không bịa nguồn
hay thử lại. Khi không có bằng chứng, probe xác nhận model không bị gọi.

Migration test live-only sau đó chạy lại toàn suite trong 177,21 giây: 205 test
đạt, năm OpenAI calls thật không retry, mọi collection test được dọn thành công
và active collection giữ nguyên 572 points.

## Cách bạn tự kiểm tra

Mở [notebooks/06_generation_and_api.ipynb](/home/hieu0606sunny/hue_rag/notebooks/06_generation_and_api.ipynb) từ Jupyter process đã có `OPENAI_API_KEY` trong environment, rồi chạy từ trên xuống. Bạn cần thấy health của app sẵn sàng, một câu trả lời tiếng Việt có sources và retrieval debug. Mỗi Run All gọi đúng một lần OpenAI và có chi phí nhỏ trong ngân sách đã duyệt; notebook không đọc hoặc hiển thị key.

## Giới hạn hiện tại

API chưa có streaming, giao diện web, lưu lịch sử hội thoại, xác thực hoặc Agentic RAG. Một output từ model thật đã bị từ chối do sai cấu trúc; đó là hành vi fail-closed đúng contract nhưng Phase 7 cần đánh giá tần suất và chất lượng câu trả lời kỹ hơn. Token usage của Agents SDK đã được audit và runtime log được sửa để đọc số liệu khi provider trả về.

## Bước tiếp theo và cách xác nhận

Bạn đã xác nhận kết quả sau khi chạy notebook. Phase 7 vẫn đóng cho đến khi reviewer hoàn tất design gate và có implementation được phê duyệt riêng.

## Nếu bạn muốn xem chi tiết kỹ thuật

- [Guide Phase 6](/home/hieu0606sunny/hue_rag/guides/phase_6_generation_api.md) mô tả phạm vi và contract API.
- [Codex review](/home/hieu0606sunny/hue_rag/reports/phase_6_generation_api_codex_review.md) ghi evidence kiểm tra và các giới hạn kỹ thuật.
- [Chat route](/home/hieu0606sunny/hue_rag/backend/api/routes/chat.py) là nơi điều phối retrieval, context và generation.
