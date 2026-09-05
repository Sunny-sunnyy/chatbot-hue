Bạn hãy dùng `brainstorming` làm quy trình chính để cùng tôi thảo luận, hỏi thêm, làm rõ yêu cầu.
   - Reviewer tự đọc file này khi user yêu cầu brainstorming; user không cần copy nội dung vào chat. Không reload trong cùng task.
   - "Brainstorming thôi về <chủ đề>" nghĩa là thảo luận và đọc context phù hợp, chưa chỉnh file. Handoff cũ không chặn yêu cầu mới của user.
   - Tập trung một khía cạnh; tự tổng hợp tài liệu và quyết định đã chốt, không hỏi lại. Chi tiết biên tập thông thường do Reviewer xử lý.
   - Khi bắt đầu design session mới hoặc workflow chưa rõ, dùng `using-superpowers` để chọn các process skill liên quan. Không activate lại trong cùng design task.
   - Dùng `brainstorming` làm quy trình chính.
   - Chỉ dùng `rich-elicitation` nếu vẫn còn từ 2 chiều mơ hồ quan trọng trở lên, và mỗi chiều có từ 3 hướng hợp lý.
   - Hãy hỏi cho tới khi bạn nắm đầy đủ hết ngữ cảnh và yêu cầu của người dùng.
   - Mỗi lượt một quyết định, có lựa chọn và khuyến nghị. Dùng công cụ hiển thị lựa chọn nếu có; kèm A/B/C ngắn trong chat để user vẫn trả lời được khi UI không hiện.
   - Không hỏi lan man. Mỗi câu hỏi phải làm thay đổi scope, design, test, hoặc implementation plan.
   - Đừng bắt đầu viết code cho đến khi chúng ta đã thống nhất yêu cầu.

 Phải ưu tiên sử dụng `using-superpowers` và các skill liên quan trong `superpowers` khi phù hợp với tác vụ.

  Core workflow skills:
  - `using-superpowers` - Bootstrap skill usage and workflow selection
  - `brainstorming` - Socratic design refinement
  - `writing-plans` - Detailed implementation plans
  - `executing-plans` - Batch execution with checkpoints
  - `dispatching-parallel-agents` - Concurrent subagent workflows
  - `subagent-driven-development` - Fast iteration with two-stage review
  - `using-git-worktrees` - Parallel development branches
  - `finishing-a-development-branch` - Merge/PR decision workflow

  Quality and validation skills:
  - `test-driven-development` - RED-GREEN-REFACTOR cycle
  - `systematic-debugging` - Root-cause debugging workflow
  - `requesting-code-review` - Pre-review checklist
  - `receiving-code-review` - Responding to feedback
  - `verification-before-completion` - Final verification before completion

Dừng lại trao đổi với tôi, tôi xác nhận mới tạo file

Theo `session_prompt/REVIEWER_WORKFLOW.md`: user duyệt written spec rồi duyệt
plan riêng trước implementation. Không tự bỏ điểm duyệt vì task nhỏ; yêu cầu
trực tiếp cho exact task có thể cho phép sửa docs đã thống nhất mà không tạo
spec/plan riêng. Sự có mặt của skill Git/sub-agent trong danh sách không cấp
quyền sử dụng chúng.

Bạn có thể tự khám phá các file, folder chứa code khác để hiểu rõ thêm về dự án nếu thấy cần thiết hoặc nếu tôi cung cấp thiếu ngữ cảnh
