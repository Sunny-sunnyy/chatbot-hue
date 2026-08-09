# Mẫu báo cáo dành cho người dùng

Báo cáo này dành cho người đang học kỹ thuật AI. Phần chính phải đọc được trong
khoảng năm phút, giúp người dùng hiểu kết quả, tự kiểm tra và quyết định xác
nhận hay yêu cầu sửa.

Ưu tiên tiếng Việt thông thường và câu ngắn. Nếu một thuật ngữ tiếng Anh bắt
buộc phải giữ, giải thích ở lần đầu, ví dụ `đoạn dữ liệu (chunk)`, rồi chỉ dùng
cách gọi tiếng Việt. Tên file, đường dẫn, tên hàm, câu lệnh và tên sản phẩm được
giữ nguyên khi dịch có thể làm sai thông tin.

Không chép báo cáo kỹ thuật sang đây. Không đưa mã trạng thái nội bộ, chi tiết
gỡ lỗi, mã băm, đường dẫn riêng tư hoặc kết quả chưa được Codex kiểm tra.

# Báo cáo dành cho người dùng: Giai đoạn <số> - <tên dễ hiểu>

## Trạng thái hiện tại

Dùng tiếng Việt để ghi trạng thái, thời gian cập nhật và tệp thực hành cần kiểm
tra.

```text
Trạng thái: Đang chờ bạn xác nhận
Cập nhật lúc: DD-MM-YYYY HH:MM
Tệp thực hành cần kiểm tra: notebooks/0<số>_<tên>.ipynb
```

Có thể đổi trạng thái thành `Đã được bạn xác nhận` hoặc `Đang chờ sửa theo yêu
cầu` khi tình trạng thực tế thay đổi. Không hiển thị tên biến trạng thái dùng
trong guide hoặc báo cáo kỹ thuật.

## Bạn nhận được gì từ giai đoạn này

Trong một hoặc hai đoạn ngắn, giải thích:

- giai đoạn giải quyết vấn đề gì;
- kết quả người dùng nhận được;
- một ví dụ cụ thể nếu ví dụ giúp hiểu nhanh hơn.

Không tách riêng mục tiêu, vấn đề và danh sách chức năng khi chúng lặp lại cùng
một ý.

## Hệ thống hoạt động như thế nào

Giải thích các bước chính bằng từ thông thường. Có thể dùng sơ đồ chữ ngắn nếu
dễ hiểu hơn đoạn văn.

Chỉ mô tả đến mức người dùng cần để hiểu kết quả. Không chép lại toàn bộ kiến
trúc, thuật toán hoặc tên module từ báo cáo kỹ thuật.

## Kết quả Codex đã kiểm tra

Chỉ ghi bằng chứng Codex đã tự kiểm tra. Khi có từ ba nội dung trở lên, dùng
bảng:

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| <Điều đã kiểm tra> | Đạt, không đạt hoặc chưa chạy | <Kết quả cho người dùng biết điều gì> |

Mỗi con số phải có lời giải thích. Không chỉ ghi số tệp, số đoạn dữ liệu hoặc
số kiểm thử mà không nói chúng chứng minh điều gì.

## Cách bạn tự kiểm tra

Tệp thực hành (notebook) là cách kiểm tra chính từ Giai đoạn 1 đến Giai đoạn 8.
Ghi rõ:

- đường dẫn tệp thực hành;
- cách chạy từ trên xuống;
- kết quả quan trọng cần nhìn thấy;
- kết quả đó chứng minh điều gì;
- tệp thực hành có gọi dịch vụ ngoài hoặc phát sinh chi phí hay không.

Không đưa câu lệnh kỹ thuật dài vào báo cáo mặc định. Chỉ đưa câu lệnh khi
người dùng thật sự cần chạy ngoài notebook.

## Giới hạn hiện tại

Nêu điều chưa làm, lý do và ảnh hưởng thực tế. Phân biệt rõ giới hạn đúng với
phạm vi giai đoạn và lỗi cần sửa.

Không liệt kê những giới hạn kỹ thuật không giúp người dùng đưa ra quyết định.
Nếu có sử dụng dịch vụ hoặc mô hình trả phí, ghi rõ trong mục này; tuyệt đối
không ghi khóa bí mật hoặc thông tin kết nối.

## Bước tiếp theo và cách xác nhận

Nêu đúng việc người dùng cần làm tiếp theo. Khi đang chờ xác nhận, dùng cách
hướng dẫn ngắn:

```text
Sau khi chạy notebook, bạn có thể phản hồi:
- Tôi xác nhận Giai đoạn <số>.
- Tôi muốn sửa: <nội dung cần sửa>.
```

Không dùng danh sách nhiều ô đánh dấu. Khi người dùng xác nhận, Codex cập nhật
trạng thái, thời gian và các tài liệu quản lý theo
`session_prompt/REVIEWER_WORKFLOW.md`.

## Nếu bạn muốn xem chi tiết kỹ thuật

Chỉ dẫn tới những tài liệu người dùng có lý do để mở:

- hướng dẫn của giai đoạn;
- báo cáo kiểm tra của Codex;
- một hoặc hai tệp mã nguồn quan trọng khi cần.

Mỗi đường dẫn phải có một câu giải thích. Không liệt kê toàn bộ file đã thay
đổi.

### Quy tắc viết dễ hiểu

- Viết như đang giải thích trực tiếp cho một người học.
- Mỗi câu chỉ truyền đạt một ý.
- Ưu tiên đoạn văn từ hai đến ba câu.
- Dùng tiếng Việt khi đã có cách diễn đạt rõ.
- Không dùng tiếng Anh chỉ để tạo cảm giác chuyên nghiệp.
- Không dùng giọng quảng bá hoặc kết luận phóng đại.
- Hạn chế chữ đậm, danh sách dài và tiêu đề không cần thiết.
- Cập nhật báo cáo thành bản hiện trạng; không nối thêm lịch sử sửa lỗi không
  còn ảnh hưởng đến người dùng.

| Tránh dùng | Nên viết |
|---|---|
| remediation | phần sửa bổ sung |
| canonical | tài liệu chính hoặc tên file cụ thể |
| gate | điều kiện bắt buộc hoặc kiểm tra cuối |
| runtime | mã xử lý chính |
| schema | cấu trúc dữ liệu |
| payload | dữ liệu đi kèm |
| scope | phạm vi |
| validation | kiểm tra |
| technical review | kiểm tra kỹ thuật |

### Tự kiểm tra trước khi mời người dùng xác nhận

1. Người mới học có hiểu giai đoạn tạo ra kết quả gì không?
2. Có từ tiếng Anh nào thay được bằng tiếng Việt mà không làm sai nghĩa không?
3. Thuật ngữ bắt buộc đã được giải thích ở lần xuất hiện đầu tiên chưa?
4. Có mục nào lặp lại thông tin của mục trước không?
5. Mỗi con số có giải thích ý nghĩa không?
6. Kết quả mong đợi trong tệp thực hành có khớp bằng chứng Codex đã kiểm tra
   không?
7. Các đường dẫn có tồn tại không?
8. Báo cáo có nói rõ người dùng cần làm gì tiếp theo không?
9. Có bí mật, đường dẫn riêng tư hoặc chi tiết gỡ lỗi không cần thiết không?
