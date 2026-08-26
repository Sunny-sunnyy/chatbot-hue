# Prompt cho Implementer — Phase 7 Post-Simplicity Correction

Bạn đang ở vai trò **Implementer** cho project:

```text
/home/minhhieu/hue_rag
```

Hãy luôn bắt đầu bằng `using-superpowers`, sau đó dùng `executing-plans` để thực
hiện plan theo checkpoint. Không brainstorming lại design đã được user duyệt.

Đọc đầy đủ theo thứ tự:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/minhhieu/hue_rag/guides/README.md
/home/minhhieu/hue_rag/guides/phase_7_retrieval_answer_evaluation.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-7-post-simplicity-correction-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-7-post-simplicity-correction.md
/home/minhhieu/hue_rag/reports/phase_7_golden_dataset_audit.md
```

Sau đó thực hiện **đúng toàn bộ plan**:

```text
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-7-post-simplicity-correction.md
```

Mục tiêu duy nhất:

1. bỏ `collection_name` khỏi public `run_answer_batch()` và
   `run_answer_ui()`;
2. giữ override ở retrieval-only paths và shared composition root cần cho
   guarded verification;
3. làm sạch execution counts/outputs của canonical Notebook 07;
4. chạy focused real verification và Notebook Run All vào `/tmp`;
5. giữ/generate hai CSV 20 câu đúng sự thật;
6. viết report mới:

```text
reports/phase_7_post_simplicity_correction_implementation_report.md
```

Ràng buộc bắt buộc:

- chạy `git status --short` và đọc exact scoped diff trước khi sửa;
- giữ toàn bộ dirty-worktree changes không thuộc scope;
- không sửa `test2.jsonl`, `tests.jsonl`, validator hoặc tạo dataset mới;
- không chạy paid full 104-answer batch;
- không đổi metrics, prompts, models, providers, generation/retrieval semantics;
- không thêm abstraction, wrapper, retry, fallback, dependency hoặc test chỉ
  kiểm tra signature/mechanism;
- dùng Qdrant/OpenAI thật, không mock/fake/replay;
- active `hue_foods_e5_small_384` chỉ được đọc;
- không in secrets hoặc lưu full prompt/context/provider response;
- không sửa canonical guide, Project Status hoặc user report;
- không commit và không push.

Nếu source hiện tại khác plan theo cách làm thay đổi scope hoặc cần sửa dataset,
dừng lại và báo blocker; không tự mở rộng. Khi hoàn thành, trả lại exact files,
commands, observed results, CSV errors và đường dẫn implementation report để
Reviewer kiểm tra độc lập.
