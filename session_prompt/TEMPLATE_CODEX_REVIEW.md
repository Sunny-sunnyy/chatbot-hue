# Codex Review: Phase <id> <name>

Decision: ready_for_user_confirmation / changes_requested / blocked
Reviewer: Codex
Date: YYYY-MM-DD
Review path:

```text
reports/phase_<id>_<short_name>_codex_review.md
```

Implementer report:

```text
reports/<implementation_report>.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_<id>_<short_name>.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md  # only when relevant
reports/user_reports/phase_<id>_<short_name>_user_report.md  # if already present
```

## Tóm Tắt

Summarize what was reviewed and the decision.

## Findings

Use severity:

- blocker:
- major:
- minor:

If there are no blocker or major findings, write:

```text
Không có blocker hoặc major findings.
```

## Verification

Commands run and important results.

```bash
# commands
```

## Scope Check

State whether the work stayed inside the approved phase/milestone.

## Safety And Quality Check

Cover:

- Security:
- Data safety:
- Reliability:
- Performance:
- Tests:
- Notebooks:
- Evaluation:

## Required Changes

Only for `changes_requested` or `blocked`.

If not applicable, write:

```text
Not applicable.
```

## User Confirmation Readiness

Only for `ready_for_user_confirmation`.

Include:

- technically accepted files;
- accepted limitations;
- canonical notebook path and notebook safety result;
- user report path to create/update;
- exact checks the user should perform;
- confirmation that next phase remains closed;
- confirmation that `Project_Status.md` was not marked approved yet.
