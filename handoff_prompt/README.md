# Handoff và context full-corpus

`session_prompt/` vẫn giữ bootstrap/workflow và
[`CURRENT_HANDOFF.md`](../session_prompt/CURRENT_HANDOFF.md), nơi duy nhất xác
định task thực thi hiện hành. Thư mục này tập hợp canonical context/prompt và
contracts để user chuyển giữa Reviewer và Implementer; không tự cấp quyền chạy.

| Tài liệu | Vai trò hiện tại |
|---|---|
| [Golden/evaluation reference](FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md) | Completed/user-approved; chỉ là contract lịch sử |
| [Correction 2 Golden/evaluation reference](FULL_CORPUS_IMPLEMENTER_CORRECTION_2_PROMPT.md) | Prompt lịch sử; R1–R3 đã đóng trong khảo sát completed |
| [Prompt Implementer correction 3](FULL_CORPUS_IMPLEMENTER_CORRECTION_3_PROMPT.md) | Prompt lịch sử; correction đã qua Reviewer re-review |
| [Khảo sát sâu schema Golden](FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_DEEP_DIVE_PROMPT.md) | Completed/user-approved sau correction lượt 3 |
| [Correction 1 schema Golden](FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_1_PROMPT.md) | Prompt lịch sử; R1/R5 đạt, R2–R4 còn phần hẹp |
| [Correction 2 schema Golden](FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_2_PROMPT.md) | Prompt lịch sử; R2/R4 và phần lớn R3 đã đạt |
| [Correction 3 schema Golden](FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_3_PROMPT.md) | Prompt lịch sử; R3 đã đóng |
| [Khảo sát simplicity evaluation rag_old_0](FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_SURVEY_PROMPT.md) | Completed/user-approved sau hai correction; prompt lịch sử |
| [Correction 1 simplicity evaluation](FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_CORRECTION_1_PROMPT.md) | Prompt lịch sử; C1–C5 đã được xử lý/review |
| [Correction 2 simplicity evaluation](FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_CORRECTION_2_PROMPT.md) | Prompt lịch sử; survey đã đóng sau independent review |
| [Khảo sát toàn bộ project llm_rag](LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_PROMPT.md) | Prompt gốc; report đã chạm correction ceiling và bị đóng băng non-canonical |
| [Correction 1 khảo sát llm_rag](LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_1_PROMPT.md) | Contract correction lịch sử; không tiếp tục Correction 5 |
| [Verified Architecture Extraction](LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md) | Contract lịch sử; artifact đã thành approved evidence companion sau User closure |
| [Correction 1 extraction](LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md) | Contract correction lịch sử; còn findings trước Correction 2 |
| [Correction 2 extraction](LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_2_PROMPT.md) | Contract correction đã đóng VAE-R1–VAE-R4 qua independent re-review |
| [Prompt tiếp tục Reviewer](FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md) | Bootstrap lịch sử; bốn file chuẩn trong `session_prompt/` nay đủ route session mới |
| [Full-corpus implementation Review Contract](FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md) | Approved 2026-09-11; áp dụng theo từng active wave |
| [Full-corpus RAG Wave 1](FULL_CORPUS_RAG_WAVE_1_IMPLEMENTATION_PROMPT.md) | Approved initial scope; đã qua initial review, không còn là active correction |
| [Wave 1 Correction 1](FULL_CORPUS_RAG_WAVE_1_CORRECTION_1_PROMPT.md) | Đã implement nhưng re-review còn W1-C1-R1..R3 |
| [Wave 1 Correction 2](FULL_CORPUS_RAG_WAVE_1_CORRECTION_2_PROMPT.md) | Prompt lịch sử; còn W1-C2-R1 test-evidence Major |
| [Wave 1 Correction 3](FULL_CORPUS_RAG_WAVE_1_CORRECTION_3_PROMPT.md) | Completed; final finding đã đóng và User closure 2026-09-12 |
| [Context thiết kế](FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md) | Đọc snapshot đầu file trước; lịch sử/evidence phía dưới |
| [Khảo sát parser/locator](FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md) | Completed/user-approved; chỉ là contract lịch sử |
| [Đo hai input VN/QT](FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md) | Completed/user-approved; chỉ là contract lịch sử |

Guide umbrella là [`guides/full_corpus_rag.md`](../guides/full_corpus_rag.md).
Hai tài liệu ngày 2026-09-09 ở `docs/superpowers/` vẫn là decision/experiment
notes, không phải approval artifact. Written Spec, Implementation Plan và Review
Contract ngày 2026-09-11 đã được User duyệt; Wave 1 đã User-closed ngày
2026-09-12. Active scope là Reviewer design gate Phase 3/Wave 2.1, chưa phải
Implementer hoặc live action.
Approval các khảo sát không duyệt runtime toàn corpus hoặc cấp quyền API/index/Git.

Các FULL_CORPUS files dưới `session_prompt/` nay chỉ chứa link chuyển tiếp.
Đường dẫn cũ trong prompt đã copy, report hoặc script lịch sử vẫn tìm được
contract tương ứng. Không sửa artifacts/implementation reports cũ chỉ để
viết lại lịch sử đường dẫn; nội dung canonical chỉ tồn tại ở thư mục này.

Review report Golden/evaluation đã phát hiện R1–R3 cần correction:
[Codex review](../reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md).
Correction lượt 2 đã đóng R1–R3. Reviewer phát hiện R4 mới khi đối chiếu schema
Foods V3; correction lượt 3 đã sửa đạt và R1–R4 đều đóng. User xác nhận khảo sát
ngày 2026-09-10; trạng thái là `approved/completed`. Tại thời điểm khảo sát,
spec/plan chưa approved và task không tạo Golden hoặc triển khai evaluator. User đã thay
Evidence C bằng schema metric-only bốn field, giữ một canonical file đích và P7.

Khảo sát sâu schema đã qua correction 3; simplicity survey `rag_old_0` đã qua
hai correction; cả hai có independent Reviewer review và User confirmation.
Các findings đều đóng. Từ phiên sau chỉ dùng hai report simplicity survey/review
để tham khảo `rag_old_0`, không phân tích lại raw project mặc định.

Survey toàn project `llm_rag` đã nhận bốn verdict `changes_requested`; report
885 dòng còn RR11 Major nên bị đóng băng working/non-canonical sau complexity
reset. Verified Architecture Extraction thay thế đã qua hai correction,
independent review và User closure ngày 2026-09-11. Decision #1 lexical
baseline/sparse consumer, #2 index lifecycle, #3 payload/source locator, #4
retrieval/fusion/reranker matrix và #5 representation B timing đã chốt.
Decision Queue tiền-spec đã hoàn tất qua #6e. Written Spec, Plan và Review
Contract đã được User duyệt ngày 2026-09-11; Wave 1 đã qua Correction 3 và User
closure. `CURRENT_HANDOFF.md` giao Reviewer bắt đầu design gate Phase 3/Wave 2.1,
chưa mở implementation/live gate sau.
Agentic RAG dùng profile/contract riêng, không dùng one-shot budget.

Hai snapshot `/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md`
và `rag_system_pipeline_deep_dive.md` là `reference-only`, không full-read mặc
định và không làm primary evidence. Prompt extraction và Reviewer prompt đều
yêu cầu xác minh claim bằng exact source hiện hành.

Từ 2026-09-12, bốn file bootstrap chuẩn trong `session_prompt/` đủ để tìm task;
`CURRENT_HANDOFF.md` phải gắn active input là `full-read`, `targeted-read` hoặc
`reference-only` theo `Session_Prompt.md`. Chỉ full-read file mới có yêu cầu đọc
tiếp khi tool hiển thị thiếu; không áp câu này cho mọi link/canonical history.
