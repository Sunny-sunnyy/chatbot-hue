# Báo cáo dành cho người dùng

Thư mục này chứa các báo cáo giúp người đang học kỹ thuật AI hiểu từng giai
đoạn của dự án, tự kiểm tra kết quả và quyết định xác nhận hay yêu cầu sửa.

Báo cáo dành cho người dùng không phải bản dịch của báo cáo kỹ thuật. Báo cáo
chỉ giữ thông tin cần để hiểu kết quả và đưa ra quyết định. Chi tiết dành cho
Codex và DeepSeek nằm trong thư mục `reports/` và `guides/`.

## Người viết báo cáo

Chỉ Codex Reviewer tạo hoặc cập nhật các báo cáo trong thư mục này. DeepSeek
viết báo cáo triển khai trong thư mục cha và không sửa báo cáo dành cho người
dùng.

Mọi kết quả phải dựa trên bằng chứng Codex đã tự kiểm tra. Không được ghi một
kiểm tra là đạt nếu chưa chạy hoặc đang không đạt.

## Cấu trúc bắt buộc

Mỗi báo cáo dùng đúng tám mục:

1. Trạng thái hiện tại.
2. Bạn nhận được gì từ giai đoạn này.
3. Hệ thống hoạt động như thế nào.
4. Kết quả Codex đã kiểm tra.
5. Cách bạn tự kiểm tra.
6. Giới hạn hiện tại.
7. Bước tiếp theo và cách xác nhận.
8. Nếu bạn muốn xem chi tiết kỹ thuật.

Mẫu đầy đủ nằm tại `session_prompt/TEMPLATE_USER_REPORT.md`.

## Cách viết

- Viết cho người đang học, không giả định đã hiểu hệ thống.
- Dùng tiếng Việt thông thường và câu ngắn.
- Giải thích thuật ngữ bắt buộc ở lần đầu, sau đó dùng cách gọi tiếng Việt.
- Giải thích ý nghĩa của con số thay vì chỉ liệt kê kết quả.
- Lấy tệp thực hành (notebook) làm cách người dùng tự kiểm tra chính.
- Không đưa mã trạng thái nội bộ vào báo cáo.
- Không đưa chi tiết gỡ lỗi, mã băm hoặc đường dẫn riêng tư.
- Không nối thêm lịch sử cũ nếu lịch sử đó không còn ảnh hưởng đến hiện tại.

## Tên file

```text
reports/user_reports/phase_<id>_<short_name>_user_report.md
```

Mỗi giai đoạn có một báo cáo chính. Khi kết quả thay đổi, Codex viết lại báo
cáo đó thành bản hiện trạng mới nhất.

## Quá trình xác nhận

```text
Codex kiểm tra kỹ thuật và đạt
  -> Codex viết báo cáo dễ hiểu
  -> người dùng chạy tệp thực hành
  -> người dùng xác nhận hoặc yêu cầu sửa
  -> Codex cập nhật trạng thái và tài liệu bàn giao
```

Chỉ sau khi người dùng xác nhận, Codex mới cập nhật `Project_Status.md`, kiểm
tra đúng nhóm file được duyệt và thực hiện bước bàn giao theo quyền người dùng
đã cấp. Xác nhận không cho phép đưa thay đổi ngoài phạm vi vào bản lưu.
