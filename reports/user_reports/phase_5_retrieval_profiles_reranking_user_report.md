# Báo cáo dành cho người dùng: Giai đoạn 5 - Tìm kiếm và xếp hạng thông tin món Huế

> **Historical — superseded:** Report này ghi Phase 5 trước coordinated
> simplicity review Phase 4–5. Hiện trạng nằm tại
> `phase_4_5_qdrant_retrieval_simplicity_user_report.md`.

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 12-08-2026 23:41
Tệp thực hành cần kiểm tra: notebooks/05_retrieval_profiles.ipynb
```

Bạn đã xác nhận Giai đoạn 5 sau khi Codex hoàn tất kiểm tra kỹ thuật và cung
cấp notebook safe-default cùng báo cáo kết quả.

## Bạn nhận được gì từ giai đoạn này

Hệ thống nay có ba cách tìm đoạn dữ liệu về món ăn và địa điểm ẩm thực Huế.
Bạn có thể quan sát riêng kết quả tìm kiếm theo ý nghĩa, kết quả kết hợp từ khóa
và kết quả sau khi mô hình xếp hạng lại.

Ví dụ, với câu hỏi về cơm hến, hệ thống có thể lấy các đoạn gần nghĩa trước,
bổ sung điểm khớp từ khóa, rồi chọn lại năm đoạn phù hợp nhất để chuẩn bị cho
phần trả lời ở Giai đoạn 6.

## Hệ thống hoạt động như thế nào

Ba chế độ dùng cùng dữ liệu đã đưa vào Qdrant ở Giai đoạn 4:

```text
dense_only         -> tìm theo ý nghĩa -> 10 đoạn
hybrid_no_rerank   -> 30 ứng viên -> kết hợp ý nghĩa và từ khóa -> 10 đoạn
hybrid_rerank      -> cùng 10 đoạn trên -> MiniLM xếp hạng lại -> 5 đoạn
```

Sau bước tìm kiếm, bộ tạo ngữ cảnh chỉ ghép nguyên đoạn, không cắt giữa nội
dung. Ngữ cảnh có tối đa 5 nguồn và 3.000 ký tự, đồng thời giữ thông tin nguồn
để giai đoạn trả lời sau này có thể dẫn lại đúng tư liệu.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| 99 kiểm thử riêng của Giai đoạn 5 | Đạt | Ba chế độ, công thức điểm, lỗi rõ ràng, xếp hạng lại và giới hạn ngữ cảnh hoạt động đúng với thiết kế offline |
| 217 kiểm thử toàn bộ backend | Đạt | Phần mới không làm hỏng các chức năng đã được chấp nhận ở Giai đoạn 1-4 |
| Các trường hợp lỗi do Codex thử riêng | Đạt | Điểm sai định dạng, điểm vô hạn, đoạn trùng và cấu hình thay đổi đều bị chặn bằng lỗi có phân loại |
| Notebook runtime thật | Đạt | Cả ba profile dùng Qdrant, E5 và MiniLM thật từ local cache. |
| Trạng thái notebook trong repo | Đạt | Không lưu output, mọi execution count rỗng và cell IDs hợp lệ |
| Real Qdrant, E5 và MiniLM | Đạt | Ba profile trả đúng số documents, score fields và context giới hạn. |

Codex cũng kiểm tra mã chỉ lấy các trường dữ liệu cần thiết từ Qdrant, không
ghi câu hỏi hoặc thông tin nhạy cảm vào log, không tự chuyển chế độ khi có lỗi
và không tự tải mô hình MiniLM khi máy thiếu cache.

## Cách bạn tự kiểm tra

Mở `notebooks/05_retrieval_profiles.ipynb` và chạy lần lượt từ cell đầu đến cell
cuối. Notebook dùng Qdrant, E5 và MiniLM thật từ local cache; không cần API key,
không gọi dịch vụ trả phí và không đổi file config.

Bạn cần quan sát các kết quả chính:

- `dense_only` trả 10 đoạn và chỉ có điểm tìm kiếm theo ý nghĩa;
- `hybrid_no_rerank` trả 10 đoạn sau khi xét 30 ứng viên và hiển thị thêm điểm
  từ khóa cùng điểm kết hợp;
- `hybrid_rerank` trả 5 đoạn với điểm xếp hạng lại;
- ngữ cảnh có không quá 5 nguồn, không quá 3.000 ký tự và giữ thông tin nguồn;

Các kết quả này cho thấy pipeline và dữ liệu đi kèm chạy đúng contract trong
môi trường offline. Chúng chưa chứng minh chất lượng tìm kiếm trên bộ câu hỏi
thật; việc đó thuộc Giai đoạn 7-8.

## Giới hạn hiện tại

Codex đã chạy truy vấn thật trên Qdrant và load E5/MiniLM từ cache. Chưa có đo
p95 latency theo 20 lượt; đây là benchmark/resource gate riêng, không phải
quality evaluation.

MiniLM hiện là mô hình nền nhẹ để đo khả năng chạy local. Mô hình này không
được xem là lựa chọn tốt nhất cho tiếng Việt trước khi có đánh giá ở Giai đoạn
7-8. Kiểm tra cấu hình cũ cũng được gọi tường minh theo vòng đời service, không
chạy sau mỗi câu hỏi để tránh tăng độ trễ.

## Bước tiếp theo và cách xác nhận

Giai đoạn 5 đã được bạn xác nhận. Bước tiếp theo là brainstorming Giai đoạn 6
về cách tạo câu trả lời có căn cứ, cấu trúc JSON API, OpenAI Agents SDK và cách
trả lỗi. Implementation Giai đoạn 6 chưa bắt đầu trước khi thiết kế được phê
duyệt.

## Nếu bạn muốn xem chi tiết kỹ thuật

- `guides/phase_5_retrieval_profiles_reranking.md` mô tả contract, ba profile
  và các giới hạn đã được phê duyệt.
- `reports/phase_5_retrieval_profiles_reranking_codex_review.md` ghi các probes,
  lệnh kiểm tra và technical verdict của Codex.
- `backend/core/startup.py` là mã kiểm tra collection, model/config identity và
  snapshot trước khi retrieval stack được sử dụng.
- `backend/retrieval/service.py` là nơi chọn profile và trả danh sách đoạn theo
  đúng stage cuối đã chạy.
