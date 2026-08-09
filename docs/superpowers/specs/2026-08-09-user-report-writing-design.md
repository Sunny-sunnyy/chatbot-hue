# Thiết kế cách viết báo cáo dành cho người dùng

Ngày thống nhất: 09-08-2026

## Mục đích

Các báo cáo trong `reports/user_reports/` phải giúp một người đang học kỹ thuật
AI hiểu giai đoạn vừa làm được gì, tự kiểm tra kết quả và quyết định xác nhận
hay yêu cầu sửa.

Báo cáo này không phải bản dịch của báo cáo kỹ thuật. Chi tiết phục vụ Codex và
DeepSeek tiếp tục nằm trong `reports/` và `guides/`.

## Hướng đã chọn

Dùng báo cáo hai tầng:

- phần chính đọc trong khoảng năm phút, dùng tiếng Việt đơn giản;
- phần cuối dẫn tới guide, Codex review và mã nguồn nếu người dùng muốn xem sâu
  hơn.

Không giữ cấu trúc dài hiện tại và không rút báo cáo thành một phiếu xác nhận
quá ngắn. Hướng đã chọn cân bằng giữa việc học và việc xác nhận kết quả.

## Cấu trúc báo cáo

Mỗi báo cáo có tám mục theo đúng thứ tự sau.

### 1. Trạng thái hiện tại

Ghi bằng tiếng Việt:

- giai đoạn đang ở đâu;
- Codex đã kiểm tra kỹ thuật chưa;
- người dùng cần làm gì;
- thời gian cập nhật;
- notebook cần kiểm tra.

Không hiển thị các mã nội bộ như `awaiting_user_confirmation`,
`ready_for_user_confirmation`, `pending` hoặc `confirmed`.

Ví dụ:

```text
Trạng thái: Đang chờ bạn xác nhận
Cập nhật lúc: 09-08-2026 21:54
Notebook cần kiểm tra: notebooks/02_foods_data_and_chunking.ipynb
```

### 2. Bạn nhận được gì từ giai đoạn này

Gộp mục tiêu, vấn đề cần giải quyết và kết quả chính vào một phần ngắn. Dùng ví
dụ cụ thể khi ví dụ giúp người học hiểu nhanh hơn.

Không tách riêng các mục “Mục tiêu”, “Vấn đề”, “Đã xây được gì” và “Chức năng
đã có” nếu chúng lặp lại cùng một ý.

### 3. Hệ thống hoạt động như thế nào

Giải thích các bước chính bằng từ thông thường. Có thể dùng sơ đồ chữ ngắn nếu
luồng xử lý dễ hiểu hơn một đoạn văn.

Chỉ mô tả đến mức người dùng cần để hiểu kết quả. Không chép lại kiến trúc hoặc
thuật toán đầy đủ từ báo cáo kỹ thuật.

### 4. Kết quả Codex đã kiểm tra

Khi có từ ba kiểm tra trở lên, dùng bảng:

| Nội dung kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Điều đã kiểm tra | Đạt, không đạt hoặc chưa chạy | Kết quả này cho người dùng biết điều gì |

Mỗi con số phải có ý nghĩa đi kèm. Không chỉ ghi số tệp, số đoạn dữ liệu hoặc
số kiểm thử.

### 5. Cách bạn tự kiểm tra

Notebook là cách kiểm tra chính từ Giai đoạn 1 đến Giai đoạn 8. Phần này ghi:

- đường dẫn notebook;
- cách chạy từ trên xuống;
- kết quả quan trọng cần nhìn thấy;
- ý nghĩa của kết quả;
- việc notebook có gọi dịch vụ ngoài hay phát sinh chi phí hay không.

Không đưa câu lệnh `py_compile`, `pytest` hoặc câu lệnh kiểm tra dài vào báo cáo
mặc định. Chỉ đưa câu lệnh khi người dùng thật sự cần chạy ngoài notebook.

### 6. Giới hạn hiện tại

Nêu điều chưa làm, lý do và ảnh hưởng thực tế. Phân biệt rõ giới hạn đúng với
phạm vi giai đoạn và lỗi cần sửa.

Không liệt kê các giới hạn kỹ thuật không giúp người dùng đưa ra quyết định.

### 7. Bước tiếp theo và cách xác nhận

Nêu đúng một hành động tiếp theo. Khi đang chờ xác nhận, dùng cách hướng dẫn
ngắn:

```text
Sau khi chạy notebook, bạn có thể phản hồi:
- Tôi xác nhận Giai đoạn 2.
- Tôi muốn sửa: <nội dung cần sửa>.
```

Không dùng danh sách nhiều ô đánh dấu.

### 8. Nếu bạn muốn xem chi tiết kỹ thuật

Chỉ dẫn tới những tài liệu người dùng có lý do để mở:

- guide của giai đoạn;
- Codex review;
- một hoặc hai tệp mã nguồn quan trọng khi cần.

Mỗi đường dẫn phải có một câu giải thích ngắn. Không liệt kê toàn bộ tệp đã
thay đổi.

## Quy tắc ngôn ngữ

- Viết như đang giải thích trực tiếp cho một người học.
- Mỗi câu chỉ truyền đạt một ý.
- Ưu tiên đoạn văn ngắn, thường từ hai đến ba câu.
- Dùng tiếng Việt khi đã có cách diễn đạt rõ.
- Thuật ngữ bắt buộc được giải thích ở lần đầu, ví dụ `đoạn dữ liệu (chunk)`;
  sau đó chỉ dùng cách gọi tiếng Việt.
- Giữ nguyên tên file, đường dẫn, tên hàm, câu lệnh và tên sản phẩm khi dịch có
  thể làm sai thông tin.
- Không dùng tiếng Anh chỉ để tạo cảm giác chuyên nghiệp.
- Không dùng giọng quảng bá, câu kết luận phóng đại hoặc câu dẫn chung chung.
- Hạn chế chữ đậm, danh sách dài và tiêu đề không cần thiết.

Tránh các từ sau khi tiếng Việt có thể diễn đạt rõ:

| Tránh dùng | Dùng cách viết |
|---|---|
| remediation | phần sửa bổ sung |
| canonical | tài liệu chính hoặc tên file cụ thể |
| gate | điều kiện bắt buộc hoặc kiểm tra cuối |
| runtime | mã xử lý chính |
| payload | dữ liệu đi kèm |
| scope | phạm vi |
| validation | kiểm tra |
| technical review | kiểm tra kỹ thuật |

## Trạng thái và nguồn thông tin

Mã trạng thái nội bộ tiếp tục được giữ trong guide và Codex review để quản lý
quy trình. Báo cáo dành cho người dùng chỉ diễn giải trạng thái đó bằng tiếng
Việt.

Báo cáo chỉ ghi kết quả Codex đã kiểm tra độc lập. Khi giai đoạn thay đổi, Codex
cập nhật chính báo cáo hiện có thành bản hiện trạng; không nối thêm lịch sử sửa
lỗi nếu lịch sử đó không còn ảnh hưởng đến người dùng.

## Phạm vi triển khai

Các tệp dự kiến sửa:

```text
session_prompt/TEMPLATE_USER_REPORT.md
session_prompt/REVIEWER_WORKFLOW.md
reports/user_reports/README.md
reports/user_reports/phase_1_backend_skeleton_user_report.md
reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
```

Không sửa mã Python, notebook, guide, báo cáo kỹ thuật hoặc
`Project_Status.md` trong nhiệm vụ này.

## Cách kiểm tra chất lượng

Reviewer tự đọc lại từng báo cáo và trả lời các câu hỏi:

1. Người mới học có hiểu giai đoạn tạo ra kết quả gì không?
2. Có từ tiếng Anh nào thay được bằng tiếng Việt mà không làm sai nghĩa không?
3. Thuật ngữ bắt buộc đã được giải thích ở lần xuất hiện đầu tiên chưa?
4. Có mục nào lặp lại thông tin của mục trước không?
5. Mỗi con số có giải thích ý nghĩa không?
6. Kết quả mong đợi trong notebook có khớp bằng chứng Codex đã kiểm tra không?
7. Các đường dẫn có tồn tại không?
8. Báo cáo có nói rõ người dùng cần làm gì tiếp theo không?
9. Có bí mật, đường dẫn riêng tư hoặc chi tiết gỡ lỗi không cần thiết không?

Kiểm tra cuối:

- đối chiếu số liệu Giai đoạn 1 và Giai đoạn 2 với Codex review;
- kiểm tra các đường dẫn Markdown;
- tìm các từ khó hiểu đã thống nhất không sử dụng;
- kiểm tra cách diễn giải trạng thái giữa mẫu, README và hai báo cáo;
- chạy `git diff --check`;
- kiểm tra phạm vi để chắc chắn không sửa mã xử lý.

Không tạo chương trình kiểm tra mới cho thay đổi tài liệu này.

## Điều kiện hoàn tất

Thiết kế đạt khi:

- mẫu mới có đúng tám mục;
- README và quy trình Reviewer dùng cùng một quy tắc;
- hai báo cáo hiện có được viết lại theo mẫu;
- báo cáo không hiển thị mã trạng thái nội bộ;
- notebook là cách tự kiểm tra chính;
- người dùng có thể đọc phần chính trong khoảng năm phút;
- mọi số liệu và đường dẫn đều khớp bằng chứng hiện có;
- không sửa file ngoài phạm vi đã duyệt.
