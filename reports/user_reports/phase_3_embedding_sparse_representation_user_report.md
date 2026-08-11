# Báo cáo dành cho người dùng: Giai đoạn 3 - Biểu diễn dữ liệu để tìm kiếm

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 11-08-2026 16:43
Tệp thực hành cần kiểm tra: notebooks/03_embedding_models.ipynb
```

Kiểm tra kỹ thuật đã đạt và bạn đã chạy, xác nhận tệp thực hành. Giai đoạn 3
đã hoàn tất.

## Bạn nhận được gì từ giai đoạn này

Hệ thống giờ có hai cách biểu diễn mỗi đoạn dữ liệu ẩm thực Huế. Dense vector
giúp tìm nội dung gần nghĩa; sparse vector giữ tín hiệu từ khóa như tên món,
tên quán và địa điểm.

Giai đoạn này cũng chuẩn bị một adapter OpenRouter để dùng trong benchmark sau.
Adapter chưa gọi dịch vụ ngoài và chưa tạo chi phí.

## Hệ thống hoạt động như thế nào

```text
572 đoạn dữ liệu đã curate
  -> E5 local tạo dense vector đã chuẩn hóa
  -> TF-IDF tạo sparse vector từ từ khóa
  -> Giai đoạn 4 sẽ lưu cả hai vào Qdrant
```

E5 dùng tiền tố khác nhau cho tài liệu và câu hỏi để mô hình phân biệt hai mục
đích. Nếu vector sai kích thước, không hợp lệ hoặc không thể chuẩn hóa, hệ thống
dừng ngay thay vì tạo dữ liệu tìm kiếm sai.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Kiểm thử tự động | 74 kiểm thử đạt | Dense, sparse, batching, lỗi kích thước, zero vector và lỗi adapter remote đều có kiểm tra cục bộ. |
| E5 local offline | 384 số cho một câu hỏi, norm bằng 1 | Vector phù hợp với cấu hình cosine và không cần tải model từ mạng. |
| Sparse vector | Kiểm tra TF-IDF và thứ tự vocabulary đạt | Từ khóa tiếng Việt được biểu diễn ổn định giữa các lần fit cùng corpus. |
| Tệp thực hành | Schema hợp lệ, 13 cells, outputs trống | Tệp an toàn để bạn chạy; bản lưu trong repo không chứa kết quả hay dữ liệu nhạy cảm. |
| Dịch vụ ngoài | Không có lệnh gọi nào | Không phát sinh phí OpenRouter, không dùng Qdrant và không cần API key ở chế độ mặc định. |

## Cách bạn tự kiểm tra

Mở `notebooks/03_embedding_models.ipynb` và chạy từ trên xuống. Ở chế độ mặc
định, notebook chỉ dùng vector minh họa và dữ liệu cục bộ; không tải model,
không gọi OpenRouter và không phát sinh chi phí.

Bạn cần thấy 572 đoạn dữ liệu, sparse vocabulary 2093 từ, kết quả ổn định khi
fit lại, thứ tự vector được giữ nguyên và ví dụ TF-IDF tính tay khớp. Các kết
quả này cho thấy dữ liệu đã sẵn sàng cho bước lập chỉ mục ở Giai đoạn 4.

Bạn có thể bật `HUE_RAG_LOCAL_E5=1` nếu muốn chạy E5 từ cache local. Đây vẫn là
chế độ offline nhưng cần khoảng 1,5 GiB RAM cho process; không cần dùng API key.

## Giới hạn hiện tại

- Chưa có Qdrant, truy xuất hay câu trả lời chatbot; đây là các giai đoạn sau.
- Adapter OpenRouter mới sẵn sàng về mặt mã nguồn. Chưa có live request, chưa
  đo chất lượng và chưa xác minh dimension thực tế của model remote.
- Sparse vocabulary/IDF được tạo lại mỗi khi process khởi động. Với 572 đoạn
  hiện tại, đây là chi phí nhỏ và tránh dùng artifact cũ.

## Bước tiếp theo và cách xác nhận

Bạn đã xác nhận Giai đoạn 3. Bước tiếp theo là brainstorming Giai đoạn 4 để
chốt collection Qdrant và ingestion; Giai đoạn 4 chưa được mở để implement.

## Nếu bạn muốn xem chi tiết kỹ thuật

- [Hướng dẫn Giai đoạn 3](../../guides/phase_3_embedding_sparse_representation.md): phạm vi, quyết định và điều kiện kiểm tra.
- [Kết quả Codex kiểm tra](../phase_3_embedding_sparse_representation_codex_review.md): lệnh và bằng chứng kỹ thuật.
- [Báo cáo triển khai](../phase_3_embedding_sparse_representation_implementation_report.md): chi tiết implementation và giới hạn đã biết.
- [Dense embedder](../../backend/embedding/embedder.py): E5 local, prefix và model cache.
- [Sparse embedder](../../backend/embedding/sparse_embedder.py): cách tạo sparse vector từ từ khóa.
