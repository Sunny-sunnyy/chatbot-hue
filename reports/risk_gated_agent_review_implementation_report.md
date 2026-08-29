# Risk-Gated Agent Review Implementation Report

## 1. Phạm vi

Thực hiện `major` governance correction đã được user duyệt trong:

```text
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
```

Correction khôi phục các hành vi coding, test, debugging, live verification,
implementation và review cốt lõi nhưng giữ nguyên kiến trúc
`risk-gated-agent-review`.

Phạm vi implementation:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/Project_Status.md
session_prompt/CURRENT_HANDOFF.md
reports/risk_gated_agent_review_implementation_report.md
```

Không sửa runtime, tests, dependencies, datasets, notebooks, Qdrant, evaluation
artifacts hoặc hai project skills. `session_prompt_old/` là untracked context
được user cung cấp và được giữ nguyên.

## 2. Thay đổi chính

- `Session_Prompt.md` khôi phục shared Hue RAG policy về simplicity, useful
  tests, no mock/fake/stub dependency, root-cause debugging, real evidence,
  online/paid API, secrets, conditional complexity removal, `uv`, curated data,
  notebook và worktree/Git safety.
- `REVIEWER_WORKFLOW.md` khôi phục simplicity questions, test audit, exact live
  verification, bug-fix review, complexity reset, optional CodeGraph, notebook
  review, verdict và report behavior.
- `IMPLEMENTER_WORKFLOW.md` khôi phục direct implementation, useful tests,
  focused debugging, real verification, exact-diff self-review, optional
  CodeGraph, notebook, report và correction behavior.
- Skill routing giữ hai project skills tại repo; Codex Reviewer dùng native
  loading và Gemini Implementer được chỉ root `~/.codex/skills/`.
- `Project_Status.md` chỉ giữ current Golden V3 45+10, approved 08a, executable
  E5-small/Huydang DEk21/E5-base catalog, Phase 8 state và governance-correction
  next action. Retired corpus/model narrative đã được bỏ.
- `CURRENT_HANDOFF.md` được thay bằng compact final-review packet với
  `Git authorization: none`.

## 3. Cách đã kiểm tra

Đã chạy fresh documentation checks:

```text
git rev-parse HEAD
git status --short
git diff --name-only
git diff --stat
wc -w trên bốn stable governance files
required-behavior rg scans cho từng file
obsolete-state rg scans
git diff --check
protected runtime/artifact/skill diff và status checks
repository-relative canonical path checks
manual responsibility và ten-scenario replay
```

Không chạy backend tests, notebooks, models, Qdrant hoặc paid API vì exact diff
chỉ thay governance Markdown và không mở product-runtime trigger.

## 4. Kết quả quan sát

Base được xác nhận:

```text
b4452dd617757565840622228054b5679eff3713
```

Fresh word counts sau correction:

| Stable file | Words |
|---|---:|
| `Session_Prompt.md` | 1,940 |
| `Project_Status.md` | 865 |
| `REVIEWER_WORKFLOW.md` | 1,419 |
| `IMPLEMENTER_WORKFLOW.md` | 1,441 |
| **Tổng** | **5,665** |

Bundle vượt soft target cũ vì user yêu cầu khôi phục explicit core behavior.
Soft context target không phải correctness gate; phase history và retired facts
vẫn không được đưa trở lại.

Fresh checks:

| Check | Observed result |
|---|---|
| Required behavior scans | PASS cho skill routing, simplicity, tests, 45+10, debugging, `uv`, CodeGraph, notebook và lifecycle |
| Obsolete behavior/state scans | PASS, không có active rule cũ trong ba behavior files và không có retired corpus/model narrative trong status |
| `git diff --check` | PASS, không có output |
| Protected runtime/artifact diff | PASS, không có output |
| Protected runtime/artifact status | PASS, không có output |
| Project skill diff | PASS, cả hai skill không đổi |
| Canonical path checks | PASS |
| Active production mutation | Không thực hiện |
| Git checkpoint | Đã commit/push theo yêu cầu riêng của user sau implementation; handoff không cấp quyền Git tiếp theo |

Responsibility audit:

| Concern | Canonical owner |
|---|---|
| Role/risk/handoff protocol | `risk-gated-agent-review` |
| Reusable coding foundation | `practical-project-coding` |
| Shared Hue RAG behavior | `Session_Prompt.md` |
| Reviewer application | `REVIEWER_WORKFLOW.md` |
| Implementer application | `IMPLEMENTER_WORKFLOW.md` |
| Current project facts | `Project_Status.md` |
| Exact active task | `CURRENT_HANDOFF.md` |

Manual scenarios:

| Scenario | Result | Supporting behavior |
|---|---|---|
| Codex/Gemini skill loading | PASS | Session skill routing và hai role skill sections |
| Docs-only task avoids runtime checkpoint | PASS | Reviewer live-evidence rules và Review Contract |
| Pure values are not test-double/integration evidence | PASS | Shared/Implementer test rules |
| Integration change selects exact real path | PASS | Shared và Reviewer verification routing |
| Smoke 10 versus full 45 | PASS | Shared cùng hai role workflows |
| Broad suite needs blast-radius reason | PASS | Shared cùng two-role test rules |
| Unchanged correction evidence reuse | PASS | Shared/Reviewer/Implementer evidence rules |
| Over-engineering creates bounded major correction | PASS | Reviewer simplicity/correction sections |
| Implementer cannot self-approve | PASS | Both role lifecycle boundaries |
| Git work needs exact authorization | PASS | Shared cùng two-role Git boundaries |

## 5. Lỗi và giới hạn

- Codex thực hiện correction sau direct user instruction dù design dự kiến
  Gemini Implementer. Vì vậy một lượt Reviewer độc lập vẫn phải đọc exact diff;
  report này không phải self-approval.
- Không có runtime/live verification vì runtime không đổi. Kết quả Phase 8 cũ
  không được relabel thành fresh evidence cho correction này.
- `session_prompt_old/` vẫn untracked và không thuộc implementation output.
- User đã cấp authorization riêng để commit/push checkpoint sau implementation.
  `CURRENT_HANDOFF.md` dùng symbolic `HEAD` và giữ `Git authorization: none` cho
  lượt Reviewer tiếp theo.

## 6. Handoff cho Reviewer

Reviewer đọc theo four-file bootstrap rồi mở đầy đủ:

```text
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
reports/risk_gated_agent_review_implementation_report.md
```

Thực hiện medium-risk documentation Review Contract trong
`session_prompt/CURRENT_HANDOFF.md`. Không bắt đầu Notebook 08b, không sửa
runtime thay Implementer và không commit/push.
