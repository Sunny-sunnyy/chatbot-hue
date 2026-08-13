# Báo cáo dành cho người dùng: Giai đoạn 4 - Lưu dữ liệu vào Qdrant

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 12-08-2026 18:06
Tệp thực hành cần kiểm tra: notebooks/04_qdrant_ingestion.ipynb
```

Codex đã hoàn tất kiểm tra kỹ thuật và chạy notebook ở chế độ mặc định lẫn chế
độ đọc collection thật. Bạn đã xác nhận Giai đoạn 4 và chọn không tự chạy
notebook trước khi phê duyệt.

## Bạn nhận được gì từ giai đoạn này

572 đoạn dữ liệu ẩm thực Huế đã được lưu vào Qdrant. Mỗi đoạn có vector ngữ
nghĩa 384 chiều, tín hiệu từ khóa và thông tin nguồn cần thiết cho bước tìm kiếm.

Điểm dữ liệu dùng mã UUID5 ổn định. Chạy lại cùng corpus sẽ cập nhật đúng điểm
cũ thay vì sinh bản sao ngẫu nhiên.

## Hệ thống hoạt động như thế nào

```text
Markdown đã curate
  -> 572 đoạn dữ liệu
  -> E5 local + biểu diễn từ khóa
  -> kiểm tra toàn bộ dữ liệu
  -> ghi từng nhóm 64 điểm vào Qdrant
  -> kiểm tra lại cấu trúc và đúng 572 điểm
```

Ingestion không tự xóa collection. Nếu cấu trúc, model hoặc dữ liệu đang có
không khớp, hệ thống dừng để tránh ghi nhầm.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Kiểm thử tự động | 118 kiểm thử đạt | Các phase cũ không bị hỏng; 44 kiểm thử Phase 4 bao phủ cấu trúc, ID, batch, retry, lỗi một phần và reset guard. |
| Qdrant local | Version 1.18.3, trạng thái collection xanh | Server pinned chạy được và collection sẵn sàng. |
| Số điểm | Đúng 572/572 | Mỗi đoạn đã curate có đúng một điểm, không thiếu hoặc có điểm lạ. |
| Dense và sparse | Dense 384 cosine; sparse index bật | Dữ liệu đã sẵn sàng cho dense retrieval và nghiên cứu hybrid ở phase sau. |
| Danh tính dữ liệu | Toàn bộ 572 UUID5 và payload khớp | Mỗi điểm truy ngược đúng đoạn nguồn, model và dimension. |
| Tệp thực hành | 11 cells, schema hợp lệ, bản repo sạch | Notebook không lưu output hoặc dữ liệu nhạy cảm; Run All chỉ đọc Qdrant thật. |

E5 được chạy offline từ cache. Không có OpenAI, OpenRouter, web hoặc dịch vụ trả
phí nào được gọi.

## Cách bạn tự kiểm tra

Mở `notebooks/04_qdrant_ingestion.ipynb` và chạy từ trên xuống. Notebook kết
nối collection thật theo chế độ read-only; bạn cần thấy `hue_foods_e5_small_384`,
dense 384 cosine, sparse index bật, 572 points và metadata an toàn của hai
payload. Notebook không upsert, reset hoặc delete và không phát sinh chi phí API.

## Giới hạn hiện tại

- Phase này mới lưu và kiểm tra index; chưa đo chất lượng tìm kiếm hay câu trả lời.
- Sparse vector đã được lưu nhưng chưa được truy vấn trực tiếp trong Qdrant.
- Chưa chạy xóa collection thật để test reset guard, vì đó là thao tác phá dữ liệu.
- Chưa chạy ingestion lần hai trên collection thật; khả năng chạy lại an toàn đã được kiểm thử bằng dữ liệu giả lập và UUID5 ổn định.

## Bước tiếp theo và cách xác nhận

Giai đoạn 4 đã được xác nhận. Bước tiếp theo là brainstorming Giai đoạn 5 về ba
retrieval profiles, BM25, reranking và cách tạo context. Phase 5 vẫn đóng cho
đến khi các quyết định Level 3 được bạn phê duyệt.

## Nếu bạn muốn xem chi tiết kỹ thuật

- [Hướng dẫn Giai đoạn 4](../../guides/phase_4_qdrant_ingestion.md): quyết định kiến trúc, reset safety và điều kiện phê duyệt.
- [Kết quả Codex kiểm tra](../phase_4_qdrant_ingestion_codex_review.md): lệnh, live evidence và giới hạn đã chấp nhận.
- [Báo cáo triển khai](../phase_4_qdrant_ingestion_implementation_report.md): files, tests và bàn giao chi tiết từ Implementer.
- [Pipeline ingestion](../../backend/ingestion/pipeline.py): thứ tự kiểm tra, embedding, upsert và postconditions.
