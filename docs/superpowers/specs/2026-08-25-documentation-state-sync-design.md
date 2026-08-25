# Documentation State Synchronization Design

Date: `2026-08-25 +07`

Status: Approved by user

## Mục tiêu

Đồng bộ tài liệu với trạng thái hiện tại: dự án chức năng đã hoàn thành đến
Phase 7; simplicity review đã hoàn thành Phase 0–5 và Phase 6 là bước tiếp
theo. Tài liệu phải phân biệt rõ trạng thái hiện hành với bằng chứng lịch sử.

## Thiết kế đã duyệt

- `Project_Status.md`, `guides/README.md` và guide canonical giữ trạng thái và
  bước tiếp theo hiện hành.
- Technical reports được giữ nguyên làm bằng chứng tại thời điểm chúng được
  tạo; không sửa số liệu lịch sử thành hiện trạng mới.
- `reports/README.md` phân loại current simplicity evidence và historical
  evidence, đồng thời trỏ người đọc về nguồn trạng thái hiện hành.
- User reports đã bị simplicity report thay thế được gắn nhãn historical/
  superseded và trỏ tới report mới, không xóa hoặc di chuyển.
- `reports/user_reports/README.md` dùng cấu trúc năm mục hiện hành và giải thích
  lifecycle của report lịch sử.

## Phạm vi

- Documentation-only; không đổi runtime, test, notebook, config hoặc Qdrant.
- Không cutover candidate collection.
- Không xóa report hoặc làm hỏng liên kết lịch sử.
- Không commit hoặc push nếu chưa có yêu cầu riêng.

## Verification

- Tìm lại các câu trạng thái lỗi thời trong tài liệu hiện hành.
- Kiểm tra mọi Markdown path được thêm vẫn tồn tại.
- Chạy `git diff --check` và review exact changed files.
- Không chạy backend tests vì không có runtime change.
