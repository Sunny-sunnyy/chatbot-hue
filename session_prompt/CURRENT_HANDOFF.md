# Bàn giao hiện hành

Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Base commit: 72c68d16c0b9da17eecd59f780e4b2ea0d33268a
Head commit: worktree
Risk level: medium
Git authorization: commit_and_push

## 1. Mục tiêu

Review correction thay unconditional per-task `using-superpowers` bằng
conditional routing theo session, role và exact handoff. Trạng thái kết thúc là
một exact correction handoff hoặc `ready_for_user_confirmation` kèm Approval
Closure Contract. Không bắt đầu Notebook 08b.

## 2. Quyết định mới nhất

- Dùng `using-superpowers` khi session hoặc workflow chưa có route rõ, không
  reload trong cùng top-level task.
- Exact `implementation`, `correction`, `final_review` và `closure` handoff là
  routing decision đã hoàn thành.
- Implementer không brainstorm hoặc viết lại approved plan.
- Khi Gemini cần tìm/load Superpowers skill phù hợp, tìm tại
  `~/.codex/skills/`.
- Repository hiện tại chỉ có hai project-local skills:
  `practical-project-coding` và `risk-gated-agent-review`.
- Không sửa hai project skills, runtime, `Project_Status.md` hoặc
  `session_prompt_old/`.
- User đã authorize commit và push exact conditional-routing correction;
  `session_prompt_old/` phải bị loại khỏi commit.

## 3. Nguồn canonical

```text
docs/superpowers/specs/2026-08-29-conditional-skill-routing-design.md
docs/superpowers/plans/2026-08-29-conditional-skill-routing-implementation-plan.md
reports/conditional_skill_routing_implementation_report.md
```

## 4. Phạm vi và đường dẫn thay đổi

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/brainstorming.md
session_prompt/CURRENT_HANDOFF.md
docs/superpowers/specs/2026-08-29-conditional-skill-routing-design.md
docs/superpowers/plans/2026-08-29-conditional-skill-routing-implementation-plan.md
reports/conditional_skill_routing_implementation_report.md
```

Hai project skills, runtime, tests, data, notebooks, evaluation artifacts,
`Project_Status.md` và `session_prompt_old/` là protected paths.

## 5. Review Contract

Reviewer phải:

1. xác minh base/worktree state và mọi changed/untracked path;
2. đọc exact diff và map vào bảy acceptance criteria trong design;
3. xác nhận shared policy và hai role workflow không mâu thuẫn;
4. replay bốn routing scenarios trong implementation report;
5. chạy unconditional/conditional scans, canonical path checks,
   trailing-whitespace scan và `git diff --check`;
6. xác nhận protected paths không có diff.

Không chạy backend tests, notebooks, models, Qdrant hoặc API nếu actual diff
không xuất hiện runtime trigger.

## 6. Evidence

Implementation report ghi exact commands và fresh observed results. Producer
đã quan sát:

- unconditional scan không còn match trong bốn active behavior files;
- conditional routing xuất hiện ở đúng shared/role owner;
- referenced skill paths tồn tại;
- `git diff --check` exit `0`;
- protected-path diff rỗng.

Reviewer coi các kết quả này là evidence index và tự chạy lại theo contract.

## 7. Sai lệch và giới hạn

Codex thực hiện docs correction theo direct user authorization thay vì Gemini.
Không có runtime verification vì product behavior không đổi.

## 8. Hành động tiếp theo và điều kiện dừng

Reviewer thực hiện independent medium-risk documentation review. Dừng nếu base
không hợp lệ, có undeclared changed path, acceptance mâu thuẫn, protected path
có diff hoặc evidence không được hỗ trợ. Không sửa runtime hoặc bắt đầu Notebook
08b. Git authorization chỉ áp dụng cho exact paths của correction này và không
bao gồm `session_prompt_old/`.
