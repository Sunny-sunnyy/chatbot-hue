# Prompt chuyển session — Implementer correction 2 reference Golden/evaluation

Bạn là Implementer tại `/home/minhhieu/hue_rag`.

Đọc đầy đủ theo thứ tự dưới đây trước khi sửa. Nếu output bị cắt, đọc tiếp phần
thiếu; không chỉ đọc headings, excerpt hoặc lời tóm tắt trong prompt này:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. `handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`
8. `reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`
   — đọc toàn bộ, đặc biệt mục 7–8 là verdict correction lượt 1 và delta hiện hành.
9. `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`
   — đọc toàn văn bản hiện hành trước và sau khi sửa.
10. `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`
    — đọc snapshot đầu file và mục 37–40 đầy đủ. Mục 1–36 là lịch sử/evidence;
    chỉ mở mục được tài liệu hiện hành dẫn tới khi cần giải quyết mâu thuẫn.
11. `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`
    — đọc đầy đủ; đây là decision draft, chưa phải written spec approved.
12. `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`
    — đọc đầy đủ; đây chưa phải implementation plan/Review Contract approved.

## Exact task hiện hành

Thực hiện toàn bộ correction lượt 2 trong `session_prompt/CURRENT_HANDOFF.md`:

- sửa phần delta R1–R3 còn mở trong
  `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`;
- đồng bộ executive summary, phân tích chi tiết, bảng kế thừa và câu hỏi mở để
  không còn claim trái nhau;
- đổi contract pointer đầu report sang canonical path trong `handoff_prompt/`;
- tự review toàn văn report, không coi lời tự báo “đã đóng” là approval;
- sau khi hoàn tất, thay CURRENT_HANDOFF thành `Target role: reviewer`,
  `Handoff kind: final_review`, giữ `State: active`, liệt kê chính xác sửa đổi,
  evidence reuse, verification và giới hạn. Reviewer mới quyết định verdict.

Không cần và không được đọc lại rộng ba thư mục reference. Reuse evidence đã
được Reviewer xác minh vì inputs/code/data flow không đổi. Chỉ đọc source hẹp
nếu một câu correction không thể giải quyết từ exact pointers đã ghi; báo đúng
phần đã đọc.

## Quyết định Golden mới cần hiểu, chưa được implement

User đã chọn phương án C cho đơn vị evidence. Golden full-corpus vẫn dự kiến là
một file JSONL đơn giản theo tinh thần
`knowledge-base-hue/foods/evaluation/golden_v3.jsonl`. Mỗi expected claim sẽ
gắn với `evidence_groups` gồm exact source spans
`{source, heading_path, start, end, text}` trên source LF đã ingest. Chunk IDs
được ánh xạ theo candidate chunking lúc evaluation, không lưu làm canonical
ground truth.

Quyết định này chỉ là context cho cách viết recommendation trong report.
Written spec và implementation plan chưa approved, nên task này không tạo/sửa
Golden dataset, evaluator, validator, runtime, corpus, index, guide, spec hoặc
plan.

## Quyền và ranh giới

- Chỉ sửa report summary nêu trên và `session_prompt/CURRENT_HANDOFF.md`.
- Không sửa Codex review, contract, context, specs/plans, guides hoặc prompt này.
- Không chạy/import code, model, tokenizer, notebook, tests, API, Qdrant,
  benchmark; không dùng mạng hoặc tải dependency.
- Không đọc `.env`/credentials; không sửa reference, runtime, corpus, Golden,
  index hoặc settings.
- Không thao tác Git ghi, commit/push/reset/checkout; không dùng sub-agent.
- Được kiểm read-only HEAD/status/diff và chạy `git diff --check` theo contract.
- Không mở lại hai khảo sát parser/source locator và Ca Huế VN/QT đã
  approved/completed.

HEAD kỳ vọng: `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`; worktree có thay đổi sẵn.
Report có thể untracked nên phải đọc trực tiếp, không lấy diff rỗng làm PASS.

Kết thúc bằng báo cáo ngắn: sửa gì theo R1–R3, file đã đổi, kiểm tra read-only
đã làm, phần skipped/not verified, và prompt ngắn trả Reviewer đọc bootstrap,
CURRENT_HANDOFF, Codex review mục 7–8 cùng report hiện hành.
