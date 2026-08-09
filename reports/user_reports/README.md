# Báo cáo phase dành cho người dùng

## Mục đích

Thư mục này chứa báo cáo tiếng Việt dễ hiểu để người dùng biết dự án đang ở đâu,
mỗi phase giải quyết vấn đề gì, đã xây được chức năng nào, cách hoạt động ra sao,
cách tự kiểm tra bằng notebook và còn giới hạn gì.

Các technical reports ở thư mục cha `reports/` dành cho DeepSeek Implementer và
Codex Reviewer. Người dùng không cần đọc hoặc can thiệp vào các technical report
đó để xác nhận phase.

## Quyền sở hữu

- Chỉ Codex Reviewer tạo hoặc cập nhật user report.
- DeepSeek Implementer chỉ viết technical implementation report trong `reports/`.
- User report phải dựa trên guide, technical reports, code/notebook và validation
  Codex đã kiểm tra độc lập.
- User report không thay guide, không mở rộng scope và không được che failed hoặc
  skipped checks.

## Tên file

```text
reports/user_reports/phase_<id>_<short_name>_user_report.md
```

Mỗi phase có đúng một user report canonical. Nếu phase được mở lại, Codex cập
nhật chính file đó với trạng thái, thời gian, validation và giới hạn mới nhất.

## Vòng đời xác nhận

```text
technical review đạt
  -> Codex tạo user report: pending
  -> guide: awaiting_user_confirmation
  -> user đọc report và kiểm tra notebook
  -> user xác nhận hoặc yêu cầu sửa
  -> confirmed + approved, hoặc changes_requested
```

Chỉ sau khi user xác nhận, Codex mới cập nhật `Project_Status.md`, audit approved
phase package, commit và push. Xác nhận không cho phép đưa thay đổi ngoài scope
vào commit.

## Nội dung bắt buộc

Mỗi report phải theo `session_prompt/TEMPLATE_USER_REPORT.md`, gồm trạng thái,
mục tiêu, vấn đề được giải quyết, deliverables, chức năng, luồng, file quan
trọng, notebook, cách tự kiểm tra, validation thực tế, kỹ thuật, giới hạn,
external API/cost, bước tiếp theo và checklist xác nhận.
