# Báo cáo dành cho người dùng: Giai đoạn 6 - Câu trả lời và API đơn giản

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 26-08-2026 09:09 +07
Notebook cần kiểm tra: notebooks/06_generation_and_api.ipynb
```

## 1. Bạn nhận được gì

Chatbot nhận một câu hỏi về ẩm thực Huế và trả về JSON chỉ có câu trả lời:
`{"answer": "..."}`. Các chi tiết kỹ thuật như source mapping, session ID và
retrieval debug đã được bỏ khỏi public response để API nhỏ và dễ dùng hơn.

Nếu không tìm được ngữ cảnh phù hợp, hệ thống trả câu thông báo cố định mà
không gọi model. Lỗi retrieval hoặc OpenAI được trả bằng thông báo an toàn,
không để lộ chi tiết nội bộ.

## 2. Hệ thống hoạt động như thế nào

Câu hỏi đi qua retrieval để lấy các đoạn dữ liệu liên quan. ContextBuilder ghép
tối đa năm đoạn nguyên vẹn trong giới hạn 3.000 ký tự, sau đó `gpt-5.4-nano`
sinh câu trả lời tiếng Việt. API chỉ gửi câu trả lời cho client; các bước và lỗi
kỹ thuật được ghi ở backend log.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused runtime suite | 10 test đạt trong 54,35 giây | Context, validation và một API call thật hoạt động cùng nhau |
| Notebook 05 | Ba retrieval profile chạy thành công | Contract context string hoạt động với dense, BM25 và MiniLM thật |
| Notebook 06 | Health `ok`, HTTP 200, chỉ có `answer` | Luồng đầy đủ Qdrant → E5 → OpenAI hoạt động đúng public contract |
| An toàn dữ liệu | Active collection vẫn 572 points | Review không thay đổi dữ liệu Qdrant đang dùng |

Hai notebook trong repo vẫn sạch output. Scoped source/notebook/report diff
không có lỗi định dạng.

## 4. Cách bạn chạy lại

Mở
[notebooks/06_generation_and_api.ipynb](/home/minhhieu/hue_rag/notebooks/06_generation_and_api.ipynb)
bằng Jupyter được khởi động từ environment có `OPENAI_API_KEY`; Qdrant local và
collection `hue_foods_e5_small_384` cần đang sẵn sàng.

Bạn có thể sửa biến `question` tại cell “Câu hỏi”, rồi chọn **Run All** từ trên
xuống. Kết quả quan trọng cần thấy:

- `OPENAI_API_KEY present: True`;
- health có trạng thái `ok`;
- chat status là `200`;
- response fields chỉ là `['answer']`;
- câu trả lời tiếng Việt dựa trên dữ liệu Huế.

Mỗi lần Run All gọi một OpenAI API call thật và có phát sinh chi phí nhỏ.
Notebook không đọc hoặc hiển thị giá trị secret.

## 5. Giới hạn và bước tiếp theo

API hiện là single-turn: chưa có streaming, lịch sử hội thoại, frontend hoặc
Agentic RAG. Full backend suite và batch đánh giá 20 câu không được chạy lại ở
correction này vì thay đổi chỉ liên quan exception boundary và notebook, không
đổi success path tạo câu trả lời.

Hai CSV đang có khác biệt line ending trong worktree nên full-worktree format
check vẫn báo lỗi; điều này không ảnh hưởng API và Reviewer không sửa file dữ
liệu ngoài correction scope. Phase 8 vẫn đóng.

Bạn đã chạy Notebook 06 và xác nhận Giai đoạn 6 ngày 26-08-2026. Phase 6 đã
hoàn tất; Phase 8 vẫn đóng cho đến khi bước kiểm tra cuối Phase 0–6 được xử lý.
