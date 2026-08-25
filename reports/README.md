# Hue RAG Reports Index

Thư mục này giữ bằng chứng implementation và review theo thời điểm. Report
không phải nguồn tiến độ hiện hành và không tạo requirement mới.

## Nguồn trạng thái hiện hành

Đọc theo thứ tự:

1. yêu cầu mới nhất đã được user xác nhận;
2. `session_prompt/Project_Status.md`;
3. `guides/README.md` và guide canonical của phase.

Hiện tại dự án chức năng đã hoàn thành và được xác nhận đến Phase 7. Simplicity
campaign đã hoàn thành Phase 0–5; Phase 6 là bước tiếp theo. Phase 8 vẫn đóng.

## Evidence hiện hành của simplicity campaign

| Phase | Evidence chính | Trạng thái |
|---:|---|---|
| 0 | `phase_0_mvp_foundation_simplicity_review.md` | Approved |
| 1 | `phase_1_backend_skeleton_simplicity_review.md` và bộ report có `simplicity` trong tên | Approved |
| 2 | `phase_2_foods_markdown_chunking_simplicity_review.md` và bộ report có `simplicity` trong tên | Approved |
| 3 | `phase_3_embedding_sparse_representation_simplicity_review.md`, `phase_3_embedding_sparse_representation_simplicity_implementation_report.md`, `phase_3_embedding_sparse_representation_codex_review.md` | Approved |
| 4–5 | `phase_4_5_qdrant_retrieval_simplicity_implementation.md`, `phase_4_5_qdrant_retrieval_simplicity_codex_review.md`, `user_reports/phase_4_5_qdrant_retrieval_simplicity_user_report.md` | Approved; candidate chưa cutover |
| 6 | Các report Phase 6 và Milestone 6.1 hiện là functional/history evidence | Simplicity review là bước tiếp theo |
| 7 | Bộ report `phase_7_retrieval_answer_evaluation_*` | Approved |

## Historical evidence

Các implementation, Codex review và user report cũ được giữ nguyên vì chúng
ghi lại code, test policy, runtime và giới hạn tại thời điểm phase gốc được xác
nhận. Những mô tả như mock/fake tests, stored sparse vectors, retry,
fingerprints, cost gates hoặc “phase tiếp theo còn đóng” có thể đã bị
simplicity review hay governance mới thay thế.

Không dùng historical report làm hướng dẫn implementation mới. Khi historical
report khác source hiện tại hoặc guide canonical, ưu tiên source, live system
và thứ tự nguồn sự thật trong `session_prompt/Session_Prompt.md`.

## Quy tắc bảo toàn

- Không sửa số liệu cũ thành kết quả hiện tại.
- Không xóa hoặc di chuyển report chỉ vì implementation đã thay đổi.
- User report bị thay thế phải có banner trỏ tới report mới.
- Chỉ xóa report khi user duyệt exact targets và mọi reference đã được xử lý.
