# Hue RAG Reports Index

Thư mục này giữ bằng chứng implementation và review theo thời điểm. Report
không phải nguồn tiến độ hiện hành và không tạo requirement mới.

## Nguồn trạng thái hiện hành

Đọc theo thứ tự:

1. yêu cầu mới nhất đã được user xác nhận;
2. `session_prompt/Project_Status.md`;
3. `guides/README.md` và guide canonical của phase.

Hiện tại dự án chức năng đã hoàn thành và được xác nhận đến Phase 7. Simplicity
campaign Phase 0–6 và Phase 7 post-simplicity correction đã approved. Phase 8
vẫn `not_ready`, nhưng Golden Dataset V3 Gate 0, Gate 1 common contracts,
Notebooks 08a, 08b và 08c đã được triển khai/review/xác nhận. 08b không chọn
BM25 hoặc TF-IDF finalist; 08c không chọn MiniLM reranker finalist; production
giữ nguyên. Bước tiếp theo là research và brainstorming exact design để hoàn
thiện curated multi-domain data dưới `knowledge-base-hue/`; implementation,
index/Golden creation và benchmark rerun chưa được authorize.

## Evidence hiện hành của simplicity campaign

| Phase | Evidence chính | Trạng thái |
|---:|---|---|
| 0 | `phase_0_mvp_foundation_simplicity_review.md` | Approved |
| 1 | `phase_1_backend_skeleton_simplicity_review.md` và bộ report có `simplicity` trong tên | Approved |
| 2 | `phase_2_foods_markdown_chunking_simplicity_review.md` và bộ report có `simplicity` trong tên | Approved |
| 3 | `phase_3_embedding_sparse_representation_simplicity_review.md`, `phase_3_embedding_sparse_representation_simplicity_implementation_report.md`, `phase_3_embedding_sparse_representation_codex_review.md` | Approved |
| 4–5 | `phase_4_5_qdrant_retrieval_simplicity_implementation.md`, `phase_4_5_qdrant_retrieval_simplicity_codex_review.md`, `user_reports/phase_4_5_qdrant_retrieval_simplicity_user_report.md` | Approved; candidate chưa cutover |
| 6 | Các report Phase 6, Milestone 6.1 và simplicity review | Approved |
| 7 | Bộ report `phase_7_retrieval_answer_evaluation_*` | Approved |
| 8/08a | `phase_8_08a_embedding_benchmark_*` và user report tương ứng | Approved work package; Phase 8 tổng thể chưa approved |
| 8/08b | `phase_8_08b_retrieval_fusion_benchmark_*` và user report tương ứng | Approved work package; không có sparse finalist/cutover |
| 8/08c | `phase_8_08c_reranker_benchmark_*` và user report tương ứng | Approved work package; không có reranker finalist/cutover |

Phase 8 benchmark hiện có approved Gate 0 evidence, common design/sequence
contracts và approved work packages 08a–08c:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md
reports/phase_8_golden_dataset_v3_implementation_report.md
reports/phase_8_golden_dataset_v3_codex_review.md
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
reports/phase_8_08a_embedding_benchmark_codex_review.md
reports/user_reports/phase_8_08a_embedding_benchmark_user_report.md
docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md
docs/superpowers/plans/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-implementation-plan.md
reports/phase_8_08b_retrieval_fusion_benchmark_codex_review.md
reports/user_reports/phase_8_08b_retrieval_fusion_benchmark_user_report.md
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md
reports/phase_8_08c_reranker_benchmark_codex_review.md
reports/user_reports/phase_8_08c_reranker_benchmark_user_report.md
guides/phase_8_benchmark_model_selection.md
reports/phase_7_golden_dataset_audit.md
```

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
