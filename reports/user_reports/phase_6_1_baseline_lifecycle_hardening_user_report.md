# Báo cáo dành cho người dùng: Giai đoạn 6.1 - Chuẩn bị hệ thống trước câu hỏi đầu tiên

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 21-08-2026 22:40 +07
Tệp thực hành cần kiểm tra: notebooks/06_generation_and_api.ipynb
```

## Bạn nhận được gì từ giai đoạn này

Hệ thống giờ chuẩn bị sẵn các mô hình tìm kiếm cần thiết khi ứng dụng khởi
động. Vì vậy câu hỏi đầu tiên không còn phải chờ tải E5 hoặc MiniLM. Thành phần
nào được chuẩn bị phụ thuộc cấu hình tìm kiếm đang dùng, nên hệ thống không tải
MiniLM khi cấu hình không cần xếp hạng lại.

Nếu một mô hình hoặc Qdrant không sẵn sàng, ứng dụng vẫn báo trạng thái nhưng
không nhận câu hỏi. Hệ thống không tự đổi mô hình, đổi cấu hình hoặc tiếp tục
với một phần chưa sẵn sàng.

## Hệ thống hoạt động như thế nào

```text
Kiểm tra Qdrant ở chế độ chỉ đọc
  -> tải và kiểm tra E5
  -> chuẩn bị BM25 nếu dùng tìm kiếm kết hợp
  -> tải và thử MiniLM nếu dùng xếp hạng lại
  -> công bố hệ thống tìm kiếm đã sẵn sàng
  -> nhận câu hỏi
```

Endpoint `/health` chỉ đọc trạng thái đã lưu từ lúc khởi động. Nó không tự tải
mô hình, không chạy tìm kiếm và không gọi OpenAI.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Kiểm tra quy trình khởi động trọng tâm | 8 kiểm thử đạt | E5 và MiniLM được chuẩn bị đúng theo cấu hình; lỗi thành phần phụ thuộc làm khởi động đóng an toàn. |
| Kiểm tra vùng mã bị ảnh hưởng | 36 kiểm thử đạt | Thay đổi không làm hỏng ingestion, retrieval service hoặc reranker hiện có. |
| Cấu trúc notebook | Đạt | Notebook hợp lệ, không lưu output, thời điểm chạy hoặc widget từ lần chạy trước. |
| Bằng chứng trước và sau câu hỏi đầu | Đạt | Số lần E5 phải tải mới giữ nguyên từ 1 đến 1; MiniLM giữ 0 đến 0 với `dense_only`, nên câu hỏi đầu không tải thêm mô hình. |
| An toàn kho dữ liệu vector | Đạt | Collection đang dùng vẫn có đúng 572 điểm dữ liệu sau các kiểm tra. |

DeepSeek cũng chạy lại toàn bộ 214 kiểm thử bằng dependency thật trong 241,36
giây. Năm lần gọi OpenAI thành công, một lần thử provider hỏng được chặn đúng,
không retry; chi phí ước tính khoảng 0,003937 USD. Codex không lặp lại đợt gọi
OpenAI này vì mã xử lý chính không thay đổi trong lần sửa notebook.

## Cách bạn tự kiểm tra

Mở [notebooks/06_generation_and_api.ipynb](../../notebooks/06_generation_and_api.ipynb)
từ Jupyter đã có `OPENAI_API_KEY` trong environment, rồi chọn Run All. Notebook
không đọc hoặc hiển thị giá trị key và mỗi Run All gọi OpenAI đúng một lần.

Bạn cần thấy:

- `/health` trả HTTP 200 và trạng thái `ok`;
- `/api/chat` trả HTTP 200, câu trả lời tiếng Việt và danh sách nguồn;
- Evidence A xuất hiện trước mọi request và cho thấy E5 đã được tải;
- Evidence B có số lần tải mới (`cache miss`) bằng Evidence A;
- dòng `PASS: cache misses unchanged by first retrieval` xuất hiện, xác nhận
  câu hỏi đầu không tải lại mô hình.

Với profile `dense_only` hiện tại, MiniLM phải có `misses=0`. Nếu sau này dùng
`hybrid_rerank`, MiniLM phải được tải ngay trong startup.

## Giới hạn hiện tại

Khởi động lạnh mất khoảng 12–15 giây trên máy đã dùng để kiểm tra. Đây là chi
phí chuyển việc tải mô hình khỏi câu hỏi đầu tiên; giai đoạn này chưa đặt ngưỡng
thời gian bắt buộc vì tốc độ phụ thuộc máy và ổ đĩa.

Notebook có một lỗi diễn đạt nhỏ trong checklist cuối: dòng cuối nói hai lần đo
latency `/health`, trong khi code hiện gọi một lần và kiểm tra cache không đổi.
Điều này không ảnh hưởng bằng chứng mô hình đã được chuẩn bị hoặc kết quả chat.
Chất lượng retrieval và câu trả lời vẫn thuộc Giai đoạn 7–8, chưa được kết luận
từ milestone này.

## Bước tiếp theo và cách xác nhận

Bạn đã xác nhận Milestone 6.1 và yêu cầu Codex hoàn tất tài liệu, commit và
push đúng gói đã phê duyệt. Giai đoạn 7 vẫn chưa được mở; bước tiếp theo là
hoàn tất design gate riêng trước khi cho phép triển khai evaluation.

## Nếu bạn muốn xem chi tiết kỹ thuật

- [Guide Phase 6](../../guides/phase_6_generation_api.md) mô tả lifecycle và
  điều kiện bắt buộc của Milestone 6.1.
- [Codex review](../phase_6_1_baseline_lifecycle_hardening_codex_review.md) ghi
  các lệnh kiểm tra, evidence và verdict kỹ thuật.
- [Startup runtime](../../backend/core/startup.py) là nơi chuẩn bị retrieval
  stack trước khi ứng dụng nhận câu hỏi.
