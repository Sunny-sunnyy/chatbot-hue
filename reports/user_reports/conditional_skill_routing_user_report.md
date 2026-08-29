# Báo cáo dành cho người dùng: Conditional Skill Routing

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 29-08-2026 19:11 +07
Notebook cần kiểm tra: Không có — đây là thay đổi tài liệu điều phối
```

## 1. Bạn nhận được gì

Các agent không còn phải khởi động lại quy trình chọn skill cho mọi bước nhỏ.
Khi handoff đã chỉ rõ vai trò và một hành động kế tiếp, agent đi thẳng vào đúng
workflow; khi session hoặc yêu cầu chưa rõ, router chung vẫn được dùng.

## 2. Hệ thống hoạt động như thế nào

Session policy quyết định khi nào cần route hoặc route lại. Reviewer đi thẳng
vào Review Contract cho final review; Implementer đi thẳng vào implementation,
correction hoặc closure đã được duyệt. Nếu requirement, kiến trúc hoặc quyền
thay đổi, workflow phải được chọn lại.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Exact diff | Đạt — đúng 8 path đã khai báo | Correction không lan sang runtime hoặc dữ liệu |
| Routing scans | Đạt — không còn câu unconditional | Skill không bị reload cho từng bước nhỏ |
| Bốn routing scenarios | Đạt | Design, implementation, final review và workflow change đi đúng nhánh |
| Skill paths | Đạt — tất cả đều tồn tại | Hướng dẫn không trỏ tới skill path hỏng |
| Formatting và protected paths | Đạt | Diff sạch và không sửa khu vực được bảo vệ |

Không chạy backend, notebook, model, Qdrant hoặc API vì product runtime không
thay đổi.

## 4. Cách bạn kiểm tra lại

Không có notebook cho correction này. Bạn có thể đọc ba behavior files:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
```

Điểm cần nhìn thấy là routing chỉ bắt đầu lại khi session/workflow chưa rõ hoặc
yêu cầu thay đổi; exact handoff đi thẳng vào workflow tương ứng.

## 5. Giới hạn và bước tiếp theo

Correction chỉ thay đổi cách agent chọn workflow, không thay đổi Hue RAG runtime.
Bạn đã xác nhận correction ngày 29-08-2026. Handoff mới mở research cùng
brainstorming Notebook 08b; việc implement/run 08b vẫn chưa được cấp quyền.
