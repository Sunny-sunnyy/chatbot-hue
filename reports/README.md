# Hue RAG Reports Index

Thư mục này lưu **evidence theo thời điểm**: implementation report, independent
review, user report và artifact. Report không tự tạo requirement, không tự cấp
quyền triển khai và không phải nguồn xác định task hiện hành.

> **Phạm vi của index này — 2026-09-12:** đây là entrypoint định tuyến tạm thời,
> chưa phải kết quả audit giữ/xóa cho toàn bộ `reports/`. Không suy ra rằng một
> file được giữ vĩnh viễn chỉ vì nó đang tồn tại hoặc được nhắc ở đây.

Audit contract và registry hợp nhất đang được xây dựng tại
[`PROJECT_DOCUMENT_REGISTRY.md`](../PROJECT_DOCUMENT_REGISTRY.md).

## Đọc gì trước

1. Task/authority hiện tại: `session_prompt/CURRENT_HANDOFF.md`.
2. Trạng thái tổng quan: `session_prompt/Project_Status.md`.
3. Requirement: guide, written spec và implementation plan canonical của Phase.
4. Chỉ sau đó mới mở report được định tuyến bên dưới để kiểm tra evidence.

Không full-read toàn bộ thư mục. Prompt của Implementer là chỉ dẫn công việc tại
một thời điểm; report kết quả và independent review mới là evidence của công
việc đó. Khi các nguồn mâu thuẫn, áp dụng thứ tự nguồn sự thật trong
`session_prompt/Session_Prompt.md`.

## Trạng thái hiện hành

- Dự án chức năng đã được User xác nhận đến Phase 7; Phase 8 tổng thể vẫn
  `not_ready`, dù các work package Golden V3 và 08a–08c đã được review/đóng trong
  phạm vi riêng.
- Full-corpus Phase 2 đã được User xác nhận closure ngày 2026-09-12. Evidence
  quan sát: 205 file, 8.460 chunks, ba condition rules, zero errors/oversized.
- Full-corpus Phase 3 đã independent review và User-closed ngày 2026-09-12.
- Phase 4 conceptual design, Written Spec, Plan và Review Contract đã được User
  duyệt; `CURRENT_HANDOFF.md` giao **Implementer/implementation** Tasks 1–6,
  risk `high`, Git `none` và exact four-target read-only preflight.
- Chưa cấp quyền dense toàn corpus, Qdrant write, benchmark winner hoặc cutover.
- Tài liệu active/tương lai chỉ dùng thuật ngữ `Phase`. Chuỗi `wave` chỉ còn
  xuất hiện trong exact filename lịch sử đã đóng và không phải lifecycle mới.

## Bản đồ định tuyến theo chủ đề

| Cần biết | Nguồn nên đọc | Không dùng làm nguồn chính |
|---|---|---|
| Task Phase 4 hiện tại | `session_prompt/CURRENT_HANDOFF.md`; `guides/phase_4_qdrant_ingestion.md`; exact Phase 4 spec/plan ngày 2026-09-12 | Report/prompt Phase 3 không mở live-write scope |
| Full-corpus decisions | Umbrella spec/plan và exact Phase 4 spec/plan | Brainstorming context chỉ là reference lịch sử |
| Closure Phase 2 | `full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`; `user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`; preview JSON | Initial/correction reports riêng lẻ nếu không điều tra lịch sử finding |
| Kiến trúc `llm_rag` | `llm_rag_verified_architecture_extraction_2026_09_11.md`; Codex review tương ứng | Survey dài `llm_rag_full_project_reference_survey_2026_09_11.md` là working/non-canonical |
| Simplicity của `rag_old_0` | `full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`; Codex review tương ứng | Các correction prompt là lịch sử chỉ dẫn, không phải kết luận |
| Parser/source locator | `full_corpus_parser_locator_codex_review_2026_09_09.md` | Prompt khảo sát hoặc report trung gian nếu không cần audit trail |
| Golden/evaluation reference | `full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md` | Các prompt correction đã hoàn tất |
| Golden schema deep-dive | `full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`; Codex review tương ứng | Correction prompts và findings trung gian |

Tên file lịch sử Phase 2 có `wave_1` được giữ nguyên để không phá link, hash và
audit trail; ý nghĩa hiện hành của chúng là **Phase 2 evidence**.

## Evidence Phase 2 full-corpus

- `full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`: final static
  review; không còn Blocker/Major trong scope và User đã xác nhận closure.
- `user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`: summary,
  limitations và User closure.
- `artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`: canonical preview
  `PASS`/205/8.460/zero errors trong phạm vi offline Phase 2.
- Initial review, Correction 1–2 và implementation reports còn lại chỉ phục vụ
  truy vết finding; không phải điểm vào mặc định.

Evidence Phase 2 không chứng minh dense embedding, Qdrant, retrieval hoặc live
runtime. Counts là observed evidence, không phải invariant được hard-code.

## Evidence `llm_rag` và `rag_old_0`

### `llm_rag`

- `llm_rag_verified_architecture_extraction_2026_09_11.md` và
  `llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md` là cặp
  approved evidence companion sau correction và User closure.
- `llm_rag_full_project_reference_survey_2026_09_11.md` đã chạm correction
  ceiling, bị đóng băng working/non-canonical; chỉ mở khi cần lịch sử/raw lead.
- Codex review của survey dài ghi lý do complexity reset, không biến survey đó
  thành source canonical.

### `rag_old_0`

- `full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md` và
  `full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md`
  là nguồn tham khảo canonical hiện có.
- Các file `...CORRECTION_*_PROMPT.md` trong `handoff_prompt/` chỉ là lịch sử
  giao việc; không cần đọc lại raw project mặc định.

## Evidence các Phase chức năng

| Phase/work package | Điểm vào evidence | Trạng thái phạm vi |
|---:|---|---|
| 0 | `phase_0_mvp_foundation_simplicity_review.md` | Approved |
| 1 | Các report Phase 1 có `simplicity` trong tên | Approved |
| 2 Foods | `phase_2_foods_markdown_chunking_simplicity_review.md` | Approved |
| 3 Foods | `phase_3_embedding_sparse_representation_codex_review.md` và cặp simplicity report | Approved historical baseline |
| 4–5 | `phase_4_5_qdrant_retrieval_simplicity_codex_review.md` và user report | Approved; candidate chưa cutover |
| 6 | Các final Phase 6/Milestone 6.1 simplicity reviews | Approved |
| 7 | Bộ final `phase_7_retrieval_answer_evaluation_*` | Approved |
| 8/08a–08c | Final Codex review và user report của từng work package | Work package approved; Phase 8 tổng thể `not_ready` |

Các tên chung như “các report” ở bảng này sẽ được thay bằng exact retained-file
mapping sau đợt audit tài liệu. Trước lúc đó, không dùng bảng để quyết định xóa.

## Quy tắc bảo toàn trước audit

- Không sửa số liệu lịch sử thành kết quả hiện tại.
- Không xóa/di chuyển file chỉ vì implementation đã thay đổi hoặc tên có vẻ cũ.
- Không coi implementation report là technical approval nếu thiếu independent
  review và User closure tương ứng.
- Mọi quyết định xóa cần exact path, lý do, canonical replacement, inbound
  references và User approval.
- Registry hợp nhất hiện ở trạng thái `audit_in_progress`; Reviewer chỉ chốt
  retained-file mapping sau khi audit toàn bộ `reports/` cùng `handoff_prompt/`.
  README này vẫn chỉ là directory index.
