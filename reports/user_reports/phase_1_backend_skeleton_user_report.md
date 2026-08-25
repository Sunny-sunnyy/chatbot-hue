# Báo cáo dành cho người dùng: Giai đoạn 1 - Nền tảng mã xử lý phía sau

> **Historical — superseded:** Report này ghi Phase 1 trước simplicity review.
> Hiện trạng sau đơn giản hóa nằm tại
> `phase_1_backend_skeleton_simplicity_user_report.md`.

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 09-08-2026 22:30
Tệp thực hành cần kiểm tra: notebooks/01_backend_foundation.ipynb
```

Bạn đã chạy tệp thực hành và kết quả quan sát phù hợp với kết quả Codex kiểm
tra.

## Bạn nhận được gì từ giai đoạn này

Giai đoạn 1 tạo phần `backend`, tức phần mã Python xử lý phía sau hệ thống. Đây
là nền móng để các bước đọc dữ liệu, tìm kiếm và tạo câu trả lời dùng chung một
cách tổ chức.

Ví dụ, dự án có ba cách tìm kiếm dự kiến. Giai đoạn này đặt chúng trong cùng
một tệp cấu hình và báo lỗi ngay khi tên cấu hình bị viết sai. Nhờ vậy, các giai
đoạn sau không tự hiểu cấu hình theo những cách khác nhau.

## Hệ thống hoạt động như thế nào

```text
Tệp cấu hình
  -> đọc và kiểm tra tên cấu hình
  -> cung cấp cùng một cấu hình cho các phần phía sau

Dữ liệu của một kết quả tìm kiếm
  -> đưa vào RetrievedDocument
  -> nhận một đối tượng có nội dung, điểm số và thông tin nguồn
```

Hệ thống cũng có nơi ghi nhật ký hoạt động. Nhật ký giúp kiểm tra chương trình
đã chạy đến bước nào khi xảy ra lỗi.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Cấu trúc mã phía sau | Có 10 gói Python | Các phần chính đã có vị trí rõ ràng để phát triển tiếp |
| Cấu hình đang dùng | `dense_only` | Hệ thống đọc đúng lựa chọn hiện tại |
| Ba cách tìm kiếm | Đủ ba cấu hình và đúng các lựa chọn đã đặt | Các bước sau có thể dùng chung cấu hình |
| Tên cấu hình sai | Trả về `ValueError` và liệt kê tên hợp lệ | Hệ thống phát hiện lỗi sớm thay vì tiếp tục chạy sai |
| Nhật ký thử nghiệm | Tạo được rồi tự xóa | Chức năng ghi hoạt động đúng nơi và không để lại tệp thử |
| `RetrievedDocument` | Tạo thành công | Khuôn kết quả tìm kiếm có thể dùng ở các giai đoạn sau |
| Sáu ô mã trong tệp thực hành | Chạy đạt | Tệp này gọi đúng mã trong `backend` thay vì chép lại cách xử lý |

Không có mạng, mô hình AI, Qdrant hoặc dịch vụ trả phí nào được gọi trong các
kiểm tra này.

## Cách bạn tự kiểm tra

Bạn đã chạy tệp `notebooks/01_backend_foundation.ipynb` từ trên xuống. Các kết
quả quan trọng cần thấy là:

- tệp thực hành tìm thấy 10 gói Python;
- cấu hình đang dùng là `dense_only`;
- tên `not_a_profile` bị từ chối bằng `ValueError` và thông báo liệt kê ba tên
  hợp lệ;
- tệp nhật ký thử nghiệm được tạo rồi tự xóa;
- `RetrievedDocument` được tạo thành công.

`ValueError` trong ví dụ này là kết quả đúng. Nó chứng minh hệ thống không chấp
nhận một tên cấu hình không tồn tại.

## Giới hạn hiện tại

- Giai đoạn này chưa đọc dữ liệu ẩm thực Huế.
- Chưa biến văn bản thành dạng số để tìm kiếm.
- Chưa kết nối Qdrant và chưa tìm kiếm tài liệu.
- Chưa tạo câu trả lời bằng mô hình AI.
- Một số tên mô hình trong tệp cấu hình mới là giá trị dự kiến và phải được
  kiểm tra trước khi dùng.

Đây là những việc thuộc các giai đoạn sau, không phải lỗi của Giai đoạn 1.

## Bước tiếp theo và cách xác nhận

Bạn đã chạy tệp thực hành và xác nhận Giai đoạn 1. Không còn việc nào cần làm
thêm trong giai đoạn này. Bước tiếp theo là chuẩn bị Giai đoạn 3 sau khi gói
Giai đoạn 1–2 được lưu và đẩy lên kho mã nguồn.

## Nếu bạn muốn xem chi tiết kỹ thuật

- [Hướng dẫn Giai đoạn 1](../../guides/phase_1_backend_skeleton.md): mô tả yêu
  cầu và giới hạn kỹ thuật của giai đoạn.
- [Kết quả Codex kiểm tra](../phase_1_backend_skeleton_codex_review.md): ghi các
  lệnh và bằng chứng kiểm tra chi tiết.
- [Mã đọc cấu hình](../../backend/core/settings_loader.py): đọc cấu hình và phát
  hiện tên không hợp lệ.
- [Khuôn kết quả tìm kiếm](../../backend/core/schema.py): định nghĩa dữ liệu mà
  bước tìm kiếm sau này trả về.
