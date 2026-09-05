# Bàn giao hiện hành

Target role: reviewer
Authored by: reviewer
Handoff kind: closure
State: completed
Base commit: 45eb7e04b561e7793b025b2fc6dc61040d215a61
Head commit: HEAD
Risk level: low
Git authorization: commit_and_push
Sub-agent authorization: none
Technical verdict: approved

## Objective và authority

Người dùng đã chính thức xác nhận nghiệm thu toàn bộ 28 thực thể di sản văn hóa Huế và cẩm nang du lịch di sản Huế, đồng thời phê duyệt việc tái cấu trúc thư mục domain Heritages theo mô hình chuẩn hóa.
Người dùng cấp quyền thực thi Git trực tiếp: `commit_and_push` đối với hai phân vùng `knowledge-base-hue` và `session_prompt`.

Phạm vi nghiệm thu và xuất bản:
1. Toàn bộ 28 tệp thực thể di sản chuẩn hóa trong `knowledge-base-hue/heritages/heritage/` (PASS 100%).
2. Tệp cẩm nang tổng hợp `knowledge-base-hue/heritages/heritage-guides.md` (khởi tạo hoàn tất theo Hướng 1, tích hợp bảng giá vé HMCC cập nhật tháng 09/2026).
3. Dọn dẹp 3 tệp pre-curation tạm thời trong `knowledge-base-hue/festivals/`.
4. Di chuyển tệp điều phối ranh giới vào `knowledge-base-hue/meta/heritage-entities-inventory.md`.
5. Đồng bộ hóa toàn bộ chứng cứ nghiên cứu và nhật ký kiểm chứng tại `knowledge-base-hue/meta/heritage-research-evidence.md`.

Ranh giới bảo toàn:
- Bảo toàn delta `Lễ hội Áo dài Huế.md` và các tệp untracked khác trong repository.
- Các artifact thuộc workstream `performing_arts` được bảo toàn nguyên vẹn.

## Acceptance và kết quả đối soát

- Đổi tên xóa tiền tố số thứ tự: 100% 28 tệp thực thể di sản đã được chuẩn hóa về tên canonical không có số thứ tự.
- Cấu trúc thư mục: Tách biệt hoàn hảo giữa `knowledge-base-hue/heritages/heritage/` (chứa 28 thực thể) và `knowledge-base-hue/heritages/heritage-guides.md` (cẩm nang tổng quan).
- Cú pháp Git: `git diff --check` -> Mã thoát 0, không có lỗi định dạng hay khoảng trắng thừa.
- Trạng thái Markdown RAG Clean: 100% tệp bắt đầu bằng H1 `#`, không YAML frontmatter, không chứa mục nguồn dữ liệu trong nội dung thực thể.

## Next role và next action

Next role: user.
Next action: Toàn bộ 28 thực thể di sản và cẩm nang di sản Huế đã được người dùng nghiệm thu và xuất bản thành công vào kho lưu trữ. Hệ thống ở trạng thái hoàn tất (`completed`), sẵn sàng chờ chỉ đạo và nhiệm vụ mới từ Người dùng.
