# Báo cáo dành cho người dùng

Thư mục này chứa các báo cáo giúp người đang học hiểu kết quả của từng phase,
tự chạy lại luồng thật và xác nhận hoặc yêu cầu sửa. Báo cáo ghi bằng chứng tại
thời điểm review; tiến độ hiện hành luôn xem tại:

```text
session_prompt/Project_Status.md
guides/README.md
```

`reports/README.md` phân biệt report hiện hành của simplicity campaign với
report lịch sử. Một report cũ không tạo requirement mới và không được dùng để
suy ra phase tiếp theo nếu hai nguồn trạng thái trên đã thay đổi.

## Người viết báo cáo

Chỉ Codex Reviewer tạo hoặc cập nhật report trong thư mục này. Implementer viết
implementation report trong thư mục cha và không sửa user report.

Mọi kết quả phải dựa trên bằng chứng Codex đã tự chạy hoặc quan sát trực tiếp.
Không ghi expected result, mock/fake output hoặc kết quả cũ như fresh evidence.

## Cấu trúc hiện hành

Mỗi report mới dùng năm mục theo `session_prompt/TEMPLATE_USER_REPORT.md`:

1. Bạn nhận được gì.
2. Hệ thống hoạt động như thế nào.
3. Codex đã chạy và quan sát gì.
4. Cách bạn chạy lại.
5. Giới hạn và bước tiếp theo.

Các report tám mục được tạo theo workflow cũ được giữ làm lịch sử; không cần
viết lại chỉ để đổi format.

## Cách viết

- Viết tiếng Việt đơn giản cho người đang học.
- Giải thích ý nghĩa của kết quả thay vì chỉ liệt kê số liệu.
- Dùng notebook làm cách user tự kiểm tra khi canonical guide yêu cầu.
- Không đưa mã trạng thái kỹ thuật, audit chi tiết, secret hoặc private path.
- Nói rõ phần failed, skipped hoặc chưa chạy.
- Khi một simplicity report thay report cũ, gắn nhãn `Historical — superseded`
  vào report cũ và trỏ tới report mới; không xóa bằng chứng lịch sử.

## Tên file và lịch sử

```text
reports/user_reports/phase_<id>_<short_name>_user_report.md
```

Một review cycle có một user report canonical. Phase gốc và simplicity review
có thể có hai report nếu report cũ được đánh dấu historical rõ ràng. Report cũ
giữ observed result và quyết định tại thời điểm xác nhận; report mới mô tả
implementation sau simplicity review.

## Quá trình xác nhận

```text
Codex chạy và review hệ thống thật
  -> Codex viết user report
  -> user kiểm tra và xác nhận hoặc yêu cầu sửa
  -> Codex cập nhật guide, guides/README.md và Project_Status.md
```

Xác nhận phase không tự cấp quyền commit/push, active mutation hoặc destructive
action.
