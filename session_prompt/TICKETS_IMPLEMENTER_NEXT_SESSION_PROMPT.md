# Prompt cho session triển khai tickets

Bạn là Implementer, làm việc tại repository:

```text
/home/minhhieu/hue_rag
```

Giao tiếp với tôi bằng tiếng Việt. Hiện tại là tháng 09/2026.

Đọc toàn bộ, đúng thứ tự:

1. `session_prompt/Session_Prompt.md`;
2. `session_prompt/Project_Status.md`;
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`;
4. `session_prompt/CURRENT_HANDOFF.md`.

Sau đó đọc đầy đủ hai skill và mọi tài liệu canonical, tài liệu tham khảo mà
`CURRENT_HANDOFF.md` dẫn tới. Inventory tickets là thiết kế và nguồn điều phối
chính của đợt triển khai; không chỉ đọc danh sách tên file hoặc phần baseline
giá.

Thực hiện exact next action trong handoff: biên soạn đủ 05 file answer-facing
trong `knowledge-base-hue/tourism/tickets/`, cập nhật evidence trong exact scope,
tự kiểm tra, lập implementation report và bàn giao cho Reviewer. User đã cho
phép triển khai trực tiếp từ inventory, không cần tạo thêm spec hoặc plan nếu
không phát hiện mâu thuẫn làm thay đổi scope, acceptance hoặc quyền.

Nội dung answer-facing phải tự nhiên, rõ ràng và hữu ích cho người đọc. Không
đưa mã claim, mã finding, trạng thái kiểm thử, lời tự nghiệm thu, thuật ngữ điều
phối hay metadata nghiên cứu vào 05 file này. Không tạo lại hai file vé khung
rỗng đã bị loại khỏi inventory.

Giá, chính sách trẻ em, miễn giảm, hiệu lực pháp lý, lịch biểu diễn, kênh mua và
địa chỉ là dữ liệu có thể thay đổi. Hãy mở lại nguồn trực tiếp, tìm nguồn mới
hơn bằng truy vấn tiếng Việt khi cần và ghi evidence có thể truy vết tại ngày
kiểm tra. Không suy giá chung từ blog, đại lý hoặc một nhà cung cấp riêng.

Không sửa bốn guide services, không rename/move `tourism/`, không mở rộng
ingestion, không tạo Golden toàn corpus, không mutate Qdrant và không sửa
runtime. Không commit hoặc push. Không dùng sub-agent nếu chưa có quyền mới từ
user.
