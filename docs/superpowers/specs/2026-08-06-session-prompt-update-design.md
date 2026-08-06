# Design: Update Session Prompt

## Context

`Session_Prompt.md` vẫn chứa trạng thái foods cũ, danh sách file đã lỗi thời và
lịch sử commit/push không còn cần cho context mỗi session. `Project_Status.md` đã
được rút gọn và hiện là nguồn trạng thái dự án hiện tại.

## Goal

Cập nhật `Session_Prompt.md` theo hướng surgical để file giữ vai trò context và
workflow, đồng thời tránh duplicate hoặc stale project status.

## Scope

Giữ nguyên:

- Identity, repository path và ngôn ngữ giao tiếp.
- Các file bắt buộc đọc đầu session.
- Raw data paths, source dump paths và pipeline dữ liệu.
- Các quy tắc không sửa raw, không gọi web/enrich khi chưa được yêu cầu và không
  commit/push khi chưa được phép.
- Chuẩn curated foods đã chốt.

Cập nhật:

- Workflow chính cho task thay đổi file, behavior hoặc design:
  `using-superpowers` -> `brainstorming` -> hỏi làm rõ từng câu -> đề xuất 2-3
  approaches -> design approval -> implementation -> validation -> cập nhật
  `Project_Status.md`.
- Task read-only đơn giản được xử lý trực tiếp, không bắt buộc brainstorming.
- `rich-elicitation` chỉ dùng khi còn ít nhất hai chiều mơ hồ quan trọng và mỗi
  chiều có ít nhất ba hướng hợp lý.
- Curation policy: kiểm tra duplicate và slug trước khi tạo, phân biệt entity
  cùng tên theo địa chỉ, xử lý conflict bằng qualifier và không tự bổ sung dữ
  liệu.
- Source policy: chấp nhận `Nội dung người dùng cung cấp` khi không có nguồn cụ
  thể, không nâng claim marketing thành factual claim mạnh hơn dữ liệu gốc.
- Definition of done cho curated file và quy tắc cập nhật status.
- Worktree safety: kiểm tra `git status`, không revert/xóa thay đổi có sẵn và chỉ
  sửa đúng scope.
- Phần task hiện tại chỉ giữ trọng tâm ngắn và trỏ sang `Project_Status.md`.
- Sau khi hoàn tất, thêm một entry ngắn vào `Project_Status.md` theo quy tắc cập
  nhật trạng thái của dự án; không thay đổi phần current-state khác.

Xóa:

- Danh sách 20 file foods cũ.
- Thông tin commit/push history cũ.
- Số liệu foods và next action đã lỗi thời.
- Nội dung chi tiết bị duplicate với `Project_Status.md`.

## Non-goals

- Không sửa raw data.
- Không sửa các file curated foods.
- Không thay đổi phần current-state đã ổn định trong `Project_Status.md`; chỉ thêm
  một entry cập nhật cho task này.
- Không tạo hoặc cập nhật pipeline chunking, embedding, indexing hay recommender.
- Không commit hoặc push.

## Acceptance criteria

- `Session_Prompt.md` không còn danh sách 20 file hoặc commit/push history cũ.
- File trỏ trạng thái hiện tại sang `Project_Status.md` thay vì duplicate số liệu.
- Workflow mới thể hiện rõ approval gate trước mọi thay đổi file.
- Curation/source/worktree policies được ghi ngắn gọn, không mâu thuẫn với
  `Project_Status.md` hoặc `foods-template.md`.
- Không có thông tin “dữ liệu còn thiếu” được ghi như backlog bắt buộc.
- `Project_Status.md` có đúng một entry ngắn ghi nhận task và validation.
- Markdown hợp lệ và diff chỉ chạm các file trong scope đã duyệt.
