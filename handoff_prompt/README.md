# Handoff Prompt Index

Thư mục này lưu context và prompt đã dùng để chuyển việc giữa User, Reviewer và
Implementer. **Prompt ghi chỉ dẫn tại một thời điểm, không phải kết luận kỹ
thuật và không tự chứng minh công việc đã hoàn tất.**

> **Phạm vi của index này — 2026-09-12:** đây là entrypoint định tuyến tạm thời,
> chưa phải quyết định giữ/xóa cuối cùng cho toàn bộ `handoff_prompt/`.

Audit contract và registry hợp nhất đang được xây dựng tại
[`PROJECT_DOCUMENT_REGISTRY.md`](../PROJECT_DOCUMENT_REGISTRY.md).

## Nguồn task duy nhất

Task, role, authority và next action hiện hành chỉ lấy từ
[`session_prompt/CURRENT_HANDOFF.md`](../session_prompt/CURRENT_HANDOFF.md).
Không tiếp tục một prompt trong thư mục này chỉ vì tên hoặc nội dung của nó nói
“next”, “implementation” hay “correction”.

Trạng thái hiện tại:

- Full-corpus Phase 2 đã được User xác nhận closure ngày 2026-09-12.
- Phase 3 đã independent review và User-closed.
- Phase 4 conceptual design, Written Spec, Plan và Review Contract đã được User duyệt.
- Active handoff là **Implementer/implementation cho Phase 4 Tasks 1–6**, risk
  `high`, gồm exact read-only preflight trên bốn full-corpus targets.
- Chưa có quyền dense toàn corpus, Qdrant write, live cutover hoặc Git write.
- Lead Implementer được User cấp standing authorization để tự quyết dùng
  sub-agent; sub-agent không có scope/authority rộng hơn task cha.
- Tài liệu active/tương lai chỉ dùng `Phase`; chuỗi `WAVE` trong exact filename
  cũ được giữ để bảo toàn link và audit trail, nhưng các file đó là Phase 2 history.

## Cách định tuyến

| Cần làm/hiểu | Mở trước | Vai trò của prompt cũ |
|---|---|---|
| Thực hiện Phase 4 Tasks 1–6 | `CURRENT_HANDOFF.md`, guide Phase 4, exact Phase 4 spec/plan ngày 2026-09-12 | Không dùng prompt Phase 3 để mở live-write scope |
| Hiểu quyết định full-corpus | Umbrella written spec/plan và exact Phase spec/plan | `FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md` chỉ là context lịch sử hữu ích |
| Tra cứu `llm_rag` | Hai verified architecture extraction reports trong `reports/` | Survey/correction prompts chỉ cho biết yêu cầu đã giao |
| Tra cứu `rag_old_0` | Hai final simplicity survey/review reports trong `reports/` | Correction prompts không phải kết luận canonical |
| Kiểm tra closure Phase 2 | Final Correction 3 Codex review, user report và preview artifact | Prompt implementation/correction chỉ phục vụ audit trail |

## Phân loại hiện tại của các prompt

Các nhãn dưới đây mô tả **cách sử dụng hiện tại**, chưa phải retention verdict:

- `REFERENCE_CONTEXT`: có giá trị giải thích quyết định, chỉ đọc khi cần.
- `HISTORICAL_PROMPT`: công việc đã hoàn tất hoặc đã bị thay thế; không thực thi.
- `HISTORICAL_CONTRACT`: contract từng được duyệt nhưng không còn là active task.
- `SUPERSEDED_BOOTSTRAP`: bootstrap cũ, đã được bốn file chuẩn trong
  `session_prompt/` thay thế.

### Full-corpus context và governance

| Tài liệu | Phân loại | Cách dùng |
|---|---|---|
| [Context brainstorming](FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md) | `REFERENCE_CONTEXT` | Lịch sử thiết kế quan trọng; ưu tiên spec/plan đã duyệt cho requirement hiện hành |
| [Review Contract full-corpus](FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md) | `HISTORICAL_CONTRACT` | Umbrella contract được duyệt 2026-09-11; exact Review Contract Phase 3 nằm trong plan Phase 3 |
| [Prompt tiếp tục Reviewer](FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md) | `SUPERSEDED_BOOTSTRAP` | Không dùng mở phiên mới; bootstrap bằng `session_prompt/` |

### Phase 2 implementation history

Các exact filename bên dưới chứa `WAVE_1` vì là tên lịch sử. Tất cả đều thuộc
Phase 2 và không phải active Phase 3 input mặc định.

| Tài liệu | Phân loại | Trạng thái |
|---|---|---|
| [Initial implementation](FULL_CORPUS_RAG_WAVE_1_IMPLEMENTATION_PROMPT.md) | `HISTORICAL_PROMPT` | Scope ban đầu đã hoàn tất |
| [Correction 1](FULL_CORPUS_RAG_WAVE_1_CORRECTION_1_PROMPT.md) | `HISTORICAL_PROMPT` | Findings đã được xử lý tiếp |
| [Correction 2](FULL_CORPUS_RAG_WAVE_1_CORRECTION_2_PROMPT.md) | `HISTORICAL_PROMPT` | Findings đã được xử lý tiếp |
| [Correction 3](FULL_CORPUS_RAG_WAVE_1_CORRECTION_3_PROMPT.md) | `HISTORICAL_PROMPT` | Final finding đã đóng; User closure 2026-09-12 |

Final evidence không nằm trong các prompt này. Dùng:

- `reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`;
- `reports/user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`;
- `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`.

### Golden/evaluation và parser research history

| Tài liệu/chuỗi | Phân loại | Nguồn kết quả thay thế |
|---|---|---|
| [Golden/evaluation handoff](FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md) và Correction 2–3 | `HISTORICAL_PROMPT` | `reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md` |
| [Golden schema deep-dive](FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_DEEP_DIVE_PROMPT.md) và Correction 1–3 | `HISTORICAL_PROMPT` | Final deep-dive report và Codex review ngày 2026-09-10 |
| [Parser/locator survey](FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md) | `HISTORICAL_PROMPT` | `reports/full_corpus_parser_locator_codex_review_2026_09_09.md` |
| [VN/QT token check](FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md) | `HISTORICAL_PROMPT` | `reports/full_corpus_vn_qt_token_check_codex_review_2026_09_09.md` |

### `rag_old_0` history

| Tài liệu | Phân loại | Cách dùng |
|---|---|---|
| [Survey prompt](FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_SURVEY_PROMPT.md) | `HISTORICAL_PROMPT` | Không dùng như kết luận |
| [Correction 1](FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_CORRECTION_1_PROMPT.md) | `HISTORICAL_PROMPT` | C1–C5 đã được xử lý/review |
| [Correction 2](FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_CORRECTION_2_PROMPT.md) | `HISTORICAL_PROMPT` | Survey đã đóng sau independent review |

Nguồn cần đọc là
`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md` và
Codex review tương ứng.

### `llm_rag` history

| Tài liệu | Phân loại | Cách dùng |
|---|---|---|
| [Full-project survey](LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_PROMPT.md) | `HISTORICAL_PROMPT` | Report dài đã đóng băng working/non-canonical |
| [Survey Correction 1](LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_1_PROMPT.md) | `HISTORICAL_PROMPT` | Không tiếp tục correction chain |
| [Verified extraction](LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md) | `HISTORICAL_PROMPT` | Artifact kết quả đã được User đóng |
| [Extraction Correction 1](LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md) | `HISTORICAL_PROMPT` | Findings trước Correction 2 |
| [Extraction Correction 2](LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_2_PROMPT.md) | `HISTORICAL_PROMPT` | Findings đã đóng qua independent re-review |

Nguồn cần đọc là
`reports/llm_rag_verified_architecture_extraction_2026_09_11.md` và Codex review
tương ứng. Survey dài chỉ mở khi cần raw history, không dùng làm basis cho
spec/plan mới.

## Quy tắc bảo toàn trước audit

- Không thực thi prompt lịch sử.
- Không suy ra completion từ implementation prompt/report nếu thiếu independent
  review và User closure.
- Không xóa prompt chỉ vì đã completed: trước hết kiểm tra nội dung unique,
  canonical replacement và inbound references.
- Không đổi tên exact file lịch sử chỉ để thay thuật ngữ; active prose dùng
  `Phase`, tên file cũ được giữ nguyên.
- Registry hợp nhất đang ở trạng thái `audit_in_progress`; sau audit nó sẽ ghi
  exact vai trò, thời điểm cần đọc, canonical replacement và retention decision
  của những file thực sự quan trọng.
