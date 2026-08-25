# Báo cáo dành cho người dùng: Giai đoạn 2 - Chia dữ liệu ẩm thực Huế

> **Historical — superseded:** Report này ghi Phase 2 trước simplicity review.
> Hiện trạng sau đơn giản hóa nằm tại
> `phase_2_foods_markdown_chunking_simplicity_user_report.md`.

## Trạng thái hiện tại

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 09-08-2026 22:30
Tệp thực hành cần kiểm tra: notebooks/02_foods_data_and_chunking.ipynb
```

Bạn đã chạy tệp thực hành mới nhất. Kết quả cuối là 572 đoạn dữ liệu, không có
đoạn thường vượt 400 ký tự và có 8 bảng dài được giữ nguyên.

## Bạn nhận được gì từ giai đoạn này

Giai đoạn 2 đọc 91 tài liệu về món ăn và quán ở Huế, sau đó chia nội dung thành
các đoạn dữ liệu nhỏ. Trong mã nguồn, một đoạn dữ liệu nhỏ được gọi là `chunk`.

Việc chia nhỏ giúp bước tìm kiếm sau này tập trung vào đúng chủ đề. Ví dụ, câu
hỏi về địa chỉ quán không cần mang theo toàn bộ phần giới thiệu và menu. Mỗi
đoạn còn có một nhãn ngắn như `ANH KAFE tại Huế — địa chỉ` để người đọc biết
nội dung thuộc quán nào và nói về điều gì.

## Hệ thống hoạt động như thế nào

```text
91 tài liệu về ẩm thực Huế
  -> đọc tên tài liệu và từng mục ##
  -> bỏ mục nguồn cùng dòng chỉ chứa ảnh
  -> chia nội dung thường ở mức 400 ký tự
  -> giữ nguyên bảng và các dòng thuộc cùng một mục danh sách
  -> thêm nhãn ngắn cùng thông tin nguồn
  -> 572 đoạn dữ liệu
```

Giới hạn 400 chỉ tính phần nội dung, không tính dòng nhãn. Bảng là ngoại lệ vì
cắt bảng có thể làm món ăn nằm sai cột giá. Một bảng dài hơn 400 ký tự vì thế
được giữ nguyên cả khối.

## Kết quả Codex đã kiểm tra

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Phạm vi dữ liệu | 91 tệp tạo ra 572 đoạn | Hệ thống đọc đủ dữ liệu ẩm thực đã duyệt |
| Giới hạn độ dài | 0 đoạn thường vượt 400 ký tự | Nội dung thường tuân theo mức đã chọn |
| Bảng dài | 8 bảng vượt 400 ký tự được giữ nguyên | Hàng và cột của bảng không bị phá vỡ |
| Bảo toàn nội dung | Đạt | Không mất nội dung khi chia, ngoài phần nguồn và dòng ảnh được chủ ý loại bỏ |
| Mục danh sách | Đạt | Dòng xuống hàng của cùng một mục không bị tách sai |
| Mã đoạn | Không trùng và không đổi khi chạy lại | Các giai đoạn sau có thể lập chỉ mục nhất quán |
| Kiểm thử tự động | 31 kiểm thử đạt | Các quy tắc chia đoạn, bảng, danh sách, nhãn và nguồn đều hoạt động |
| Tệp thực hành | 7 trên 7 ô mã chạy đạt | Ví dụ và phần kiểm tra cuối dùng đúng mã xử lý chính |

Không có mạng, mô hình AI, Qdrant hoặc dịch vụ trả phí nào được gọi.

## Cách bạn tự kiểm tra

Bạn đã chạy tệp `notebooks/02_foods_data_and_chunking.ipynb` từ trên xuống. Tệp
này hiển thị một đoạn văn, một bảng đúng hàng cột và một gợi ý du lịch ẩm thực.

Kết quả quan trọng ở ô cuối gồm ba con số: tổng cộng 572 đoạn, không có đoạn
thường nào vượt 400 ký tự và có 8 bảng vượt 400 ký tự.

Tám bảng vượt giới hạn không phải lỗi. Đây là quyết định có chủ ý để nội dung
bảng vẫn đọc được. Tệp thực hành chỉ đọc dữ liệu trên máy và không cần khóa
API.

## Giới hạn hiện tại

- Mức 400 ký tự đang nằm trực tiếp trong mã nguồn. Giai đoạn 8 mới so sánh mức
  này với 600 hoặc 800 ký tự bằng cùng bộ câu hỏi.
- Một mục danh sách riêng lẻ dài hơn 400 ký tự vẫn phải được chia.
- Giai đoạn này mới chuẩn bị dữ liệu. Chất lượng tìm kiếm chưa được đo vì chưa
  có bước biến văn bản thành dạng số và tìm kiếm thử.
- Các giai đoạn sau phải dùng toàn bộ 572 đoạn mới, không dùng lại con số 366
  của bản cũ.

Đây là các giới hạn đã biết của giai đoạn, không phải lỗi trong kết quả bạn vừa
chạy.

## Bước tiếp theo và cách xác nhận

Bạn đã chạy tệp thực hành, quan sát đúng 572 đoạn, 0 đoạn thường vượt 400 ký tự
và 8 bảng vượt 400 ký tự, sau đó xác nhận Giai đoạn 2. Bước tiếp theo là chuẩn
bị Giai đoạn 3 và dùng toàn bộ 572 đoạn mới.

## Nếu bạn muốn xem chi tiết kỹ thuật

- [Hướng dẫn Giai đoạn 2](../../guides/phase_2_foods_markdown_chunking.md): mô
  tả quy tắc chia 400 ký tự, giữ bảng và tạo nhãn.
- [Kết quả Codex kiểm tra](../phase_2_foods_markdown_chunking_codex_review.md):
  ghi bằng chứng chi tiết cho 572 đoạn và 31 kiểm thử.
- [Mã chia nội dung](../../backend/ingestion/helpers/split_text.py): thực hiện
  việc chia đoạn, giữ bảng và xử lý danh sách.
- [Mã tạo đoạn dữ liệu](../../backend/ingestion/chunking/markdown_chunker.py):
  đọc tài liệu và thêm nhãn cùng thông tin nguồn.
