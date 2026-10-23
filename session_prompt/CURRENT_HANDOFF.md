# Implementation handoff — Phase 7A Golden full-corpus, Task 1–2 (tới GATE P)

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: docs commit Phase 7A spec/plan trên `main` (resolve bằng `git log -1`)
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none cho Task 1–2 (sub-agent chỉ được mở ở Task 3 qua handoff sau)
Paid-call authorization: none
Cross-session messaging: allowed between `hue-rag-66` (Reviewer) and `hue-rag-08` (Implementer)

User duyệt spec, plan và Review Contract Phase 7A ngày 2026-10-23.

## 1. Context routing

- `full-read`: `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md`
- `full-read`: `docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md` (Global Constraints, Task 1, Task 2, Review Contract)
- `full-read`: các file `heritages/` trong curated corpus (29 file theo `discover_full_corpus_files()`), trước khi viết case
- `reference-only`: `reports/phase_7a_golden_reference_rag_old_0_survey_2026_10_23.md`; `backend/evaluation/golden_dataset.py` (Foods V2/V3 lịch sử, không sửa)

## 2. Scope

- Task 1: tạo `backend/evaluation/golden_full_corpus.py` và `backend/tests/test_golden_full_corpus.py` đúng như plan. Code trong plan đã được Reviewer chạy thử ở thư mục tạm (8 passed, CLI probe đúng như mong đợi). Implementer được chỉnh nhỏ nếu có lý do, nhưng phải ghi trong report.
- Task 2: pilot khoảng 20 case `heritages` trong `knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl`; hướng dẫn viết `knowledge-base-hue/meta/golden-full-corpus-writing-guide.md`; report `reports/phase_7a_golden_pilot_implementation_2026_10_23.md` (hoặc ngày thực tế).

User nhấn mạnh: câu hỏi phải tự nhiên như người thật hỏi, thực tế, rõ ràng,
không đánh đố, có một đáp án khách quan. Không dùng câu xin lời khuyên hoặc phụ
thuộc sở thích. Phải đọc `.md` trước khi viết.

## 3. Boundaries

Không sửa curated Markdown, Foods V2/V3, retrieval/generation/API, Qdrant.
Không gọi API. Không commit/push. Report tracked không chép câu hỏi, đáp án hay
excerpt.

## 4. Next action và stop

Làm Task 1 rồi Task 2 theo plan. Sau Task 2 Step 6: thay file này bằng
`Target role: reviewer`, `Handoff kind: final_review` (Task 1–2, GATE P), nhắn
`hue-rag-66` và **dừng**. Không bắt đầu Task 3.
