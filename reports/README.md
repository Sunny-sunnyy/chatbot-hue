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
giữ nguyên. Curation/taxonomy toàn corpus đã hoàn tất. Các khảo sát full-corpus
trước survey toàn project `llm_rag` đã qua correction/review và được User xác
nhận. Survey dài `llm_rag` đã chạm correction ceiling và bị đóng băng
working/non-canonical. Verified Architecture Extraction thay thế đã qua hai
correction, independent review và User closure ngày 2026-09-11; đây là approved
evidence companion. Decision Queue tiền-spec đã hoàn tất qua #6e. Written Spec
đã được User duyệt ngày 2026-09-11. Plan + Review Contract cũng đã được duyệt.
Wave 1 đã qua ba correction, independent static review và được User xác nhận
closure ngày 2026-09-12. Active handoff chuyển sang Reviewer/`next_design` cho
Phase 3/Wave 2.1; chưa authorize implementation hoặc live gate.
Agentic RAG dùng
profile/contract riêng. Index/Golden creation, live systems và benchmark rerun
chưa được authorize.

Final Wave 1 review là
`full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`; User report là
`user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`. Canonical preview
`PASS`/205/8460/zero errors đã được closure trong đúng phạm vi offline Wave 1;
không chứng minh Wave 2+ hoặc live runtime.

Guide trạng thái của workstream là `guides/full_corpus_rag.md`. Khảo sát
Golden/evaluation reference, schema deep-dive và simplicity evaluation
`rag_old_0` đều đã `approved/completed`. Report của Implementer không tự tạo
technical approval. Approval Plan hiện hành không tự mở Wave 2 hoặc live gate.
Sau mỗi wave, report chỉ cung cấp evidence cho Reviewer review/User closure;
detailed guide và design package wave kế tiếp phải được cập nhật/duyệt riêng.

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

## Evidence thiết kế full-corpus hiện hành

- `full_corpus_rag_wave_1_codex_review_2026_09_12.md`: initial Wave 1 verdict
  `changes_requested`, W1-R1..R5.
- `full_corpus_rag_wave_1_correction_1_codex_review_2026_09_12.md`: active review
  history W1-C1-R1..R3 và route sang Correction 2.
- `full_corpus_rag_wave_1_correction_2_codex_review_2026_09_12.md`: đóng hai
  production/report branches, giữ W1-C2-R1 test-evidence Major.
- `full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`: final static
  review, không còn Blocker/Major; Approval Closure Contract đã được User xác nhận.
- `full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`:
  final evidence index sau Correction 3; execution evidence, không tự là proof.
- `artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`: artifact hiện ghi
  PASS/205/8460/zero errors; User-closed trong phạm vi offline Wave 1.
- `user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`: summary và
  limitations được User xác nhận ngày 2026-09-12.

- `full_corpus_parser_locator_codex_review_2026_09_09.md`: completed và User
  approved; parser/source locator design evidence.
- `full_corpus_vn_qt_token_check_codex_review_2026_09_09.md`: completed và User
  approved; chỉ chứng minh hai exact inputs vừa các limits đã đo.
- `full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`: R1–R4
  đã đóng, survey completed và User approved.
- `full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`: implementation
  report khảo sát sâu schema đã hoàn tất correction lượt 3.
- `full_corpus_golden_schema_reference_deep_dive_codex_review_2026_09_10.md`:
  independent review đã approved sau User confirmation.
- `full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md` và Codex
  review tương ứng: nguồn tham khảo canonical cho `rag_old_0`; không cần đọc lại
  raw project nếu không có yêu cầu mới.
- `llm_rag_full_project_reference_survey_2026_09_11.md`: working/non-canonical;
  đã chạm correction ceiling và không được tiếp tục vá hoặc dùng làm basis cho
  Spec/Plan.
- `llm_rag_full_project_reference_survey_codex_review_2026_09_11.md`: nguồn
  review/complexity-reset; §9–10 ghi RR11 và User confirmation.
- `llm_rag_verified_architecture_extraction_2026_09_11.md`: artifact thay thế đã
  qua hai correction, independent review và User closure; approved evidence
  companion cho design, không phải approval runtime/Spec/Plan.
- `llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`: review
  chain, technical closure và Approval Closure Contract đã được User xác nhận.
- Initial implementation report và evidence index hợp nhất Correction 1–3 ghi
  lịch sử triển khai; final acceptance dựa trên independent Correction 3 review
  cùng User closure, không dựa riêng vào report Implementer.

Các report completed cung cấp evidence cho written spec sau này. Chúng không
thay `CURRENT_HANDOFF.md`, không chọn schema và không cấp quyền implementation.

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
