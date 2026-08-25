# Báo cáo dành cho người dùng: Giai đoạn 3 - Biểu diễn dữ liệu để tìm kiếm

> **Downstream update:** Sau report này, coordinated simplicity review Phase
> 4–5 đã xóa `SparseEmbedder` và stored sparse vectors khỏi target code và
> dense-only candidate. Dense E5 behavior được giữ; Phase 4–5 đã approved và
> Phase 6 là simplicity review tiếp theo.

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 25-08-2026 09:36 +07
Notebook cần kiểm tra: notebooks/03_embedding_models.ipynb
```

## 1. Bạn nhận được gì

572 đoạn dữ liệu ẩm thực Huế có thể được biến thành dense vectors để
tìm nội dung gần nghĩa và sparse TF-IDF vectors để giữ tín hiệu từ khóa.
Dense embedding chạy local bằng multilingual E5 trên CPU; không cần
OpenRouter hay API trả phí.

Mã nguồn nay đi thẳng qua một `E5Embedder`, bỏ các lớp provider,
batching vòng ngoài và adapter remote chưa dùng. Kết quả dễ đọc hơn mà
vẫn truy vấn được active Qdrant hiện tại.

## 2. Hệ thống hoạt động như thế nào

```text
572 đoạn dữ liệu ẩm thực
-> E5 thêm vai trò passage cho tài liệu
-> tạo vector 384 chiều đã chuẩn hóa
-> câu hỏi dùng vai trò query
-> Qdrant tìm các đoạn gần nghĩa
```

Sparse TF-IDF đếm từ trong corpus theo thứ tự ổn định. Biểu diễn
này tạm thời được giữ để tương thích với schema Giai đoạn 4; luồng
tìm kiếm hybrid hiện dùng dense candidates rồi chấm Python BM25.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| E5 và sparse focused checks | 10 checks đạt | Các vai trò query/document, kích thước, norm và TF-IDF hoạt động trên model/code thật |
| Notebook Run All | 572 x 384, norm 1.0, 26.13 giây | Toàn bộ corpus được embed local thành công |
| Ví dụ query/document | Cosine 0.9401 | E5 dùng hai vai trò khác nhau nhưng cùng biểu diễn đúng nội dung |
| Active Qdrant query | 10 kết quả; top là bài Bún bò Huế | Implementation mới tương thích index 572 points hiện tại |
| Downstream/full backend | 59 và 190 checks đạt | Không quan sát regression trong shared runtime |
| An toàn dữ liệu | Active collection vẫn 572 points; không còn test collection | Review không ghi vào active collection |

Thư viện sentence-transformers có cảnh báo đổi tên một method dimension.
Kết quả 384 dimensions vẫn đúng; đây không phải lỗi runtime hiện tại.

## 4. Cách bạn chạy lại

Mở `notebooks/03_embedding_models.ipynb` từ repo root và chọn **Run All**.
Máy cần project environment đã cài bằng `uv`, local E5 model cache và
572 curated foods chunks. Notebook không cần Qdrant, API key, internet hay paid
API.

Kết quả quan trọng cần thấy:

- `chunk_count: 572` và `dense_shape: 572 x 384`;
- `first_vector_norm` xấp xỉ `1.0`;
- query và document đều có 384 dimensions;
- sparse sample có 3 documents, vocabulary size 7 và indices/values hiển thị.

Các kết quả này chứng minh Notebook đang gọi public backend flow trên dữ
liệu và model thật.

## 5. Giới hạn và bước tiếp theo

- OpenRouter embedding chưa được implement; việc chọn candidate và chạy API
  thật thuộc Giai đoạn 8.
- Tại thời điểm report, sparse vectors còn được lưu để giữ compatibility.
  Coordinated simplicity review Phase 4–5 sau đó đã xử lý schema này như ghi
  trong downstream update ở đầu report.
- Phase 7 evaluation không chạy lại vì model, instruction và retrieval
  behavior không đổi; real active query đã đạt.
- Bạn đã xác nhận Giai đoạn 3 ngày 25-08-2026; phase hiện
  `approved`.
- Tại thời điểm report, bước tiếp theo là simplicity review Giai đoạn 4; tiến
  độ hiện hành xem tại `session_prompt/Project_Status.md`. Việc commit/push vẫn
  cần yêu cầu riêng.
