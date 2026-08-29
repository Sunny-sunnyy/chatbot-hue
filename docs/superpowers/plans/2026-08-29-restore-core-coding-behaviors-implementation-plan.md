# Restore Core Coding Behaviors Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Sub-agents are not authorized for this correction. Steps use checkbox (`- [ ]`) syntax for tracking.

Status: approved for execution
User approval: 2026-08-29 +07

**Goal:** Restore the approved Hue RAG coding, testing, debugging, live-verification and review behaviors while preserving the risk-gated role and handoff architecture.

**Architecture:** Keep `risk-gated-agent-review` as the coordination layer and `practical-project-coding` as the reusable coding foundation. Restore explicit shared Hue RAG policy in `Session_Prompt.md`, role-specific application in the two workflows, and current-only task/state facts in `Project_Status.md` and `CURRENT_HANDOFF.md`.

**Tech Stack:** Markdown, Git read-only inspection, `rg`, `wc`, `test`, `git diff --check`

## Global Constraints

- Canonical specification:
  `docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md`.
- This is a `major` governance correction to the current risk-gated rollout.
- Start by loading `using-superpowers`; Gemini Implementer finds Superpowers
  skills under `~/.codex/skills/`.
- Apply both project-local skills:
  `skills/risk-gated-agent-review/SKILL.md` and
  `skills/practical-project-coding/SKILL.md`.
- Do not modify either project-local skill.
- Do not modify runtime code, tests, dependencies, datasets, notebooks, Qdrant,
  evaluation CSVs or benchmark artifacts.
- Preserve unrelated worktree state, including `session_prompt_old/`; never
  stage, rewrite or delete it.
- Restore behavior by responsibility; do not copy old files verbatim or restore
  superseded phase history.
- `Project_Status.md` and `CURRENT_HANDOFF.md` contain current facts only. Do not
  mention retired evaluation scope or removed dense models.
- Golden V3 has 45 canonical full cases and a 10-row deep-equal smoke subset.
- Current executable dense catalog is E5-small, Huydang DEk21 and E5-base.
- Do not create a validator, linter, parser, CI job, checklist engine or new
  dependency.
- Documentation-only verification does not run backend tests, models, Qdrant or
  notebooks unless the actual diff unexpectedly touches a runtime trigger.
- Git authorization is `none`. Do not stage, commit or push.

## Review Contract

**Risk level:** `medium` because these documents control future agent coding,
review, verification and authority behavior, but the correction does not change
product runtime.

**Expected triggers:** governance behavior, role permissions, skill routing,
test/evidence policy, context routing and handoff authority. No product runtime,
database, model, provider, API or quality-output trigger is expected.

**Implementer evidence required:**

- exact base/worktree state and changed-file list, including untracked files;
- full diff for all allowed governance files;
- section-to-spec acceptance mapping;
- responsibility and duplication audit;
- repository-relative path checks and Superpowers-root check;
- current-state scan for Golden V3 45+10, approved 08a, three-model executable
  catalog, Phase 8 `not_ready` and governance correction before 08b;
- manual behavior scenarios listed in Task 5;
- protected-path no-diff check and `git diff --check`;
- explicit record of failed, skipped, partial and not-verified checks.

**Reviewer minimum independent gate:** resolve the base/head or worktree state,
inspect every changed and untracked path, read the exact diff, map it to this
plan and the spec, identify deviations, run `git diff --check`, repeat the
current-state/path scans and manually replay the Task 5 scenarios.

**Reviewer independent reruns:** documentation, path, diff and manual scenario
checks only. Do not run backend tests, notebooks, models, Qdrant or paid APIs
unless the actual implementation includes an undeclared runtime change.

**Evidence reuse:** current Phase 8 runtime/model/Qdrant evidence is not needed
for this documentation-only correction. Documentation checks must be fresh for
the final diff. During a later correction, an unaffected scenario may be reused
only when its governing text and inputs did not change, and it must not be
described as a fresh rerun.

**New authority required for:** modifying either skill, changing runtime/tests/
dependencies/data/notebooks/artifacts, using a sub-agent, running paid APIs,
mutating Qdrant, production cutover, destructive cleanup, commit or push.

**Approval closure:** Reviewer writes the technical verdict and an exact closure
contract. Only after user confirmation may the authorized role update approval
state and replace the handoff with `next_design` for Notebook 08b research and
brainstorming. Closure does not authorize 08b implementation/run.

---

### Task 1: Restore shared behavior in `Session_Prompt.md`

**Files:**

- Modify: `session_prompt/Session_Prompt.md:1-162`
- Read only: `session_prompt_old/Session_Prompt.md`
- Read only: `docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md`

**Interfaces:**

- Consumes: the current source-of-truth, bootstrap, safety and Git rules plus
  approved design Sections 6, 7 and 10.
- Produces: one stable shared Hue RAG policy that both role workflows apply.

- [ ] **Step 1: Re-read the exact approved inputs and current worktree**

Run:

```bash
git status --short
sed -n '1,240p' docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
sed -n '1,360p' session_prompt_old/Session_Prompt.md
sed -n '1,220p' session_prompt/Session_Prompt.md
```

Expected: the design spec and `session_prompt_old/` are visible as untracked
user/project context; no file is modified by this step.

- [ ] **Step 2: Rewrite the section structure without phase history**

Use `apply_patch` and keep these exact top-level responsibilities:

```markdown
# Session Prompt
## Repository and communication
## Source of truth
## Skill and role routing
## Context loading
## Stable project and data boundaries
## Đơn giản là mặc định
## Test vừa đủ
## Debugging và tự review
## Chạy thật, dữ liệu thật
## Online, paid API và secrets
## Loại bỏ complexity không phục vụ nhu cầu thật
## Python runtime
## Curated data
## Notebook
## Project state, worktree and Git authorization
```

Preserve the current repository/language convention, source-of-truth order,
four-file bootstrap, tiered context loading, active-data safety and exact Git
authorization values.

- [ ] **Step 3: Add the concise skill-loading contract**

The routing section must state all of the following without listing every
Superpowers skill:

```text
Mỗi task bắt đầu bằng using-superpowers.
Reviewer Codex dùng cơ chế native để load Superpowers skills.
Implementer Gemini load Superpowers skills từ ~/.codex/skills/.
Mỗi role đọc skills/risk-gated-agent-review/SKILL.md.
Task implementation/code/test/debug/refactor/notebook/dependency/technical review
đọc skills/practical-project-coding/SKILL.md.
```

Keep `brainstorming -> written spec approval -> writing-plans -> approved-plan
execution` for work with important trade-offs. State that a parallel-agent skill
does not grant authority by itself.

- [ ] **Step 4: Restore the shared simplicity and testing contract**

Add the approved requirements from spec Sections 7.1 and 7.2. The resulting
text must explicitly include:

```text
observed problem -> direct solution is insufficient -> concrete benefit
-> real-system evidence -> proportionate complexity
```

It must distinguish prohibited mock/fake/stub dependencies from small, direct,
valid pure-logic inputs. It must state that smoke 10 is a bounded check and full
45 is required when the Golden V3 quality decision may change. Do not mention
the retired evaluation corpus or old simplicity-campaign sequence.

- [ ] **Step 5: Restore debugging, real evidence and conditional complexity removal**

Add the exact debugging sequence:

```text
tái tạo nhất quán -> thu bằng chứng -> chứng minh nguyên nhân gốc
-> thử một focused fix -> chạy lại exact live path
```

Restore fresh real-system evidence, honest non-PASS reporting, approved online/
paid behavior, secret handling and active-data boundaries. Restore the examples
of mechanisms that must be removed when they serve no real need, while stating
that this is not a permanent blacklist and that approved removal cannot be
evaded by renaming or moving a mechanism.

- [ ] **Step 6: Restore Python, curated-data and notebook behavior**

Require `uv sync`, `uv run`, no `pip install`, no system-Python PASS and no
offline flags without an exact contract. Restore the curated Markdown and
closed-world research boundary. Restore learning-value, one-cell/one-purpose,
backend reuse, clean-output, temporary Run All and secret-safety notebook rules.

- [ ] **Step 7: Verify Session Prompt behavior and scope**

Run:

```bash
rg -n "using-superpowers|~/.codex/skills/|risk-gated-agent-review|practical-project-coding|Đơn giản là mặc định|Test vừa đủ|mock|stub|45|10|nguyên nhân gốc|uv sync|Curated data|Notebook|git_authorization" session_prompt/Session_Prompt.md
rg -n "104|Phase 0–6|Phase 7 trước|MiniLM-L12|Qwen3 Embedding|E5-large|BGE-M3" session_prompt/Session_Prompt.md
git diff --check -- session_prompt/Session_Prompt.md
```

Expected: the first scan finds every required behavior; the second scan has no
output; diff check has no output.

### Task 2: Restore Reviewer-specific review behavior

**Files:**

- Modify: `session_prompt/REVIEWER_WORKFLOW.md:1-129`
- Read only: `session_prompt_old/REVIEWER_WORKFLOW.md`

**Interfaces:**

- Consumes: the shared policies produced by Task 1 and the Reviewer branch of
  `risk-gated-agent-review`.
- Produces: Reviewer-specific simplicity, test, live-evidence, correction,
  notebook, verdict and report behavior without runtime implementation rights.

- [ ] **Step 1: Re-read the Reviewer sources**

Run:

```bash
sed -n '1,380p' session_prompt_old/REVIEWER_WORKFLOW.md
sed -n '1,190p' session_prompt/REVIEWER_WORKFLOW.md
sed -n '45,125p' skills/risk-gated-agent-review/SKILL.md
```

Expected: old operational behavior and current risk-gated ownership are both in
context before editing.

- [ ] **Step 2: Expand the workflow using role-owned sections**

Use `apply_patch` and keep these top-level sections:

```markdown
# Codex Reviewer Workflow
## Purpose and required skills
## Session bootstrap
## Design gate
## Final review gate
## Review tính đơn giản
## Review test và live evidence
## Bug-fix review
## Correction and complexity reset
## CodeGraph
## Notebook review
## Findings, verdicts and reports
## Reviewer ownership and Git boundary
```

Do not duplicate the full shared doctrine. Add the role-specific questions and
actions that make the shared policy operational.

- [ ] **Step 3: Restore the exact simplicity review questions**

Require Reviewer to determine:

```text
Code phục vụ hành vi thật nào?
Có cách trực tiếp, dễ hiểu hơn không?
Data flow có theo dõi được không?
Kỹ thuật nâng cao giải quyết observed problem nào?
Real evidence chứng minh lợi ích nào?
Lợi ích có tương xứng complexity không?
```

State that unjustified over-engineering is a `major`, not a style preference,
and that Reviewer must not request speculative layers, audit state or edge-case
machinery.

- [ ] **Step 4: Restore test, live-system and bug-fix review behavior**

Require Reviewer to audit the real behavior/contract/recurrence risk protected
by each affected test before retaining or running it. Apply no test-double
dependencies, exact affected real path, smoke 10 versus full 45, justified broad
suite and docs-only no-live-run rules. For bug fixes, require reproduction,
root cause, one focused fix and exact rerun.

- [ ] **Step 5: Restore optional CodeGraph and notebook review**

Keep CodeGraph optional, non-blocking and subordinate to source/fresh execution.
Do not authorize init/uninit/index deletion or telemetry changes. Restore
notebook parsing, clean repository state, one-cell/one-purpose, backend reuse,
no validator/test-suite duplication, secret safety and temporary real Run All
when acceptance requires it.

- [ ] **Step 6: Preserve risk-gated findings and lifecycle**

Keep the current severity/verdict values, minimum independent diff gate, exact
correction handoff, four-verdict complexity reset, Approval Closure Contract,
Reviewer document ownership and Git boundary. Keep the six-section Codex review
and five-section user report behavior without copying checklists into reports.

- [ ] **Step 7: Verify Reviewer behavior and non-conflict**

Run:

```bash
rg -n "risk-gated-agent-review|practical-project-coding|Review tính đơn giản|over-engineering|mock|stub|45|10|root cause|CodeGraph|Notebook review|ready_for_user_confirmation|changes_requested|blocked|correction thứ năm|Approval Closure Contract" session_prompt/REVIEWER_WORKFLOW.md
rg -n "104|Phase 0–6|Phase 7 trước|full suite mặc định|spawn sub-agent mặc định" session_prompt/REVIEWER_WORKFLOW.md
git diff --check -- session_prompt/REVIEWER_WORKFLOW.md
```

Expected: required role behavior is present; obsolete/default-expansion scan has
no output; diff check has no output.

### Task 3: Restore Implementer-specific execution behavior

**Files:**

- Modify: `session_prompt/IMPLEMENTER_WORKFLOW.md:1-132`
- Read only: `session_prompt_old/IMPLEMENTER_WORKFLOW.md`

**Interfaces:**

- Consumes: Task 1 shared policy and the Implementer branch of
  `risk-gated-agent-review`.
- Produces: an approved-scope implementation workflow with clear code, useful
  tests, root-cause debugging, real verification, self-review and evidence.

- [ ] **Step 1: Re-read the Implementer sources**

Run:

```bash
sed -n '1,330p' session_prompt_old/IMPLEMENTER_WORKFLOW.md
sed -n '1,190p' session_prompt/IMPLEMENTER_WORKFLOW.md
sed -n '125,168p' skills/risk-gated-agent-review/SKILL.md
```

Expected: old execution behavior and current role/closure boundary are both in
context.

- [ ] **Step 2: Expand the workflow using role-owned sections**

Use `apply_patch` and keep these top-level sections:

```markdown
# Implementer Workflow
## Purpose and required skills
## Session bootstrap
## When implementation may start
## Cách implement
## Test
## Debugging và tự review
## Chạy và xác minh thật
## Python, notebook and CodeGraph
## Self-review, report and handoff
## Corrections
## Approval closure
## Documentation ownership and Git authorization
```

The skill section must tell Gemini that Superpowers skills are under
`~/.codex/skills/`, without listing every skill path.

- [ ] **Step 3: Restore direct implementation behavior**

Require an explainable data flow, smallest complete solution, named
responsibility, reuse of production backend, no second pipeline, no speculative
abstraction/wrapper/validator/flexibility/state/workflow, no unrelated refactor,
and removal of imports/helpers made unnecessary by the current change.

- [ ] **Step 4: Restore useful-test and debugging behavior**

Require behavior/contract/real-bug justification for tests, no test count or
coverage target, no mock/fake/stub dependency, direct valid pure inputs,
canonical integration data/dependency, test audit/removal, exact live path,
smoke 10 versus full 45 and broad-suite blast-radius justification. Restore the
root-cause/focused-fix debugging sequence and credible-risk regression-test
rule.

- [ ] **Step 5: Restore live verification and self-review**

Require canonical data and approved real services, honest non-PASS outcomes,
active-data safety, no provider/model/device/dataset switch to make a run pass,
fresh evidence for changed behavior and explicitly justified reuse for an
unchanged correction path. Require exact diff self-review for scope,
duplication, unnecessary code/tests, speculative complexity, data flow and the
actual security boundary.

- [ ] **Step 6: Restore Python, notebook, CodeGraph and evidence delivery**

Apply the shared `uv`, safe environment, learning-notebook and optional
CodeGraph behavior. Preserve the detailed six-section implementation report,
compact final-review handoff, exact changed files, `git diff --check`, Git state
and one next role/action.

- [ ] **Step 7: Preserve correction, closure and ownership boundaries**

Keep one-batch correction, affected reruns, justified evidence reuse, stop
before correction five, mechanical closure after user confirmation, no
self-approval/risk reduction, protected Reviewer documents and exact Git
authorization.

- [ ] **Step 8: Verify Implementer behavior and non-conflict**

Run:

```bash
rg -n "~/.codex/skills/|risk-gated-agent-review|practical-project-coding|Cách implement|mock|stub|45|10|nguyên nhân gốc|exact live path|uv|CodeGraph|implementation report|CURRENT_HANDOFF|self-approve|correction thứ năm|git_authorization" session_prompt/IMPLEMENTER_WORKFLOW.md
rg -n "104|Phase 0–6|Phase 7 trước|MiniLM-L12|Qwen3 Embedding|E5-large|BGE-M3" session_prompt/IMPLEMENTER_WORKFLOW.md
git diff --check -- session_prompt/IMPLEMENTER_WORKFLOW.md
```

Expected: required role behavior is present; obsolete scan has no output; diff
check has no output.

### Task 4: Synchronize the current-only project snapshot

**Files:**

- Modify: `session_prompt/Project_Status.md:1-171`

**Interfaces:**

- Consumes: approved current facts from Golden V3 and final 08a reports plus the
  correction lifecycle in this plan.
- Produces: a current project snapshot without retired dataset/model history.

- [ ] **Step 1: Reconfirm current facts from final report sections**

Run:

```bash
sed -n '1,120p' reports/phase_8_golden_dataset_v3_codex_review.md
sed -n '440,490p' reports/phase_8_08a_embedding_benchmark_codex_review.md
sed -n '1,100p' reports/user_reports/phase_8_08a_embedding_benchmark_user_report.md
```

Expected: Golden V3 is approved at 45 full + 10 smoke, 08a is approved, the
executable catalog has three models and Phase 8 remains `not_ready`.

- [ ] **Step 2: Remove non-current corpus/model narrative**

Use `apply_patch` to remove the retired evaluation-corpus bullet, removed dense
model history and policy bullets that name excluded dense settings. Preserve
the active production MiniLM cross-encoder reranker because it is a current
runtime component, not the removed dense embedding candidate.

- [ ] **Step 3: Record only the current correction and next boundary**

Keep these current facts:

```text
Golden V3: 45 full + 10 smoke deep-equal
Notebook 08a: approved
Executable dense catalog: E5-small, Huydang DEk21, E5-base
Phase 8: not_ready
Next action: complete this governance correction, then research/brainstorm 08b
08b implementation/run remains unauthorized
```

Add the new spec/plan to the governance canonical map. Do not add correction
history or a revision timeline.

- [ ] **Step 4: Verify the current-only snapshot**

Run:

```bash
rg -n "45|10|08a|e5-small-384|huydang-dek21-embedding-768|e5-base-768|not_ready|governance correction|08b" session_prompt/Project_Status.md
rg -n "legacy evaluation corpus|multilingual-minilm-l12-384|Qwen3 Embedding|E5-large|BGE-M3|historical rejection" session_prompt/Project_Status.md
git diff --check -- session_prompt/Project_Status.md
```

Expected: required current facts are present; retired narrative scan has no
output; diff check has no output.

### Task 5: Complete correction evidence and hand off to Reviewer

**Files:**

- Modify: `reports/risk_gated_agent_review_implementation_report.md`
- Modify: `session_prompt/CURRENT_HANDOFF.md`
- Read only: `docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md`
- Read only: `docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md`

**Interfaces:**

- Consumes: Tasks 1-4 completed governance diff and this Review Contract.
- Produces: a detailed corrected implementation report and one compact
  `final_review` handoff targeted to Reviewer.

- [ ] **Step 1: Resolve the exact base/worktree and allowlist**

Run:

```bash
git rev-parse HEAD
git status --short
git diff --name-only
```

Expected: the execution handoff's base is valid; approved spec/plan and
`session_prompt_old/` remain visible and preserved; implementation changes are
limited to the five governance/status/handoff files and the implementation
report.

- [ ] **Step 2: Update the six-section implementation report**

Keep the existing six headings and rewrite the report as the current corrected
rollout evidence:

```markdown
# Risk-Gated Agent Review Implementation Report
## 1. Phạm vi
## 2. Thay đổi chính
## 3. Cách đã kiểm tra
## 4. Kết quả quan sát
## 5. Lỗi và giới hạn
## 6. Handoff cho Reviewer
```

Record exact changed paths, responsibility mapping, commands and observed
results. State that runtime/live checks were intentionally not run because no
runtime path changed. Do not claim technical approval.

- [ ] **Step 3: Run the responsibility and behavior audit**

Manually map each approved behavior to its canonical file and record the result
in the implementation report. Confirm that the two skills remain unchanged and
that repeated text in role workflows is limited to short skill/safety pointers
and role-specific application.

- [ ] **Step 4: Replay the required scenarios**

Record `PASS`, `FAIL` or `AMBIGUOUS` with exact supporting section for each:

1. Codex Reviewer loads skills natively; Gemini finds Superpowers under
   `~/.codex/skills/`.
2. Documentation-only work does not trigger backend/model/Qdrant execution.
3. Pure deterministic logic uses small valid values without a test-double
   dependency or integration-PASS claim.
4. An integration change selects the exact affected real path.
5. A bounded Golden check may use smoke 10; a quality decision change selects
   full 45.
6. A broad suite requires a shared-contract/blast-radius reason.
7. Unchanged correction evidence may be reused but is not called fresh.
8. Unjustified over-engineering becomes a bounded `major` correction.
9. Implementer cannot self-approve; closure waits for user confirmation.
10. Git work remains prohibited without exact authorization.

- [ ] **Step 5: Run final documentation and protected-path checks**

The approved implementation base is
`b4452dd617757565840622228054b5679eff3713`. Confirm that the starting
implementation handoff contains this exact value, then run:

```bash
git diff --check
git diff --name-only b4452dd617757565840622228054b5679eff3713 -- backend notebooks evaluation/results pyproject.toml uv.lock skills/risk-gated-agent-review/SKILL.md skills/practical-project-coding/SKILL.md
git status --short -- backend notebooks evaluation/results pyproject.toml uv.lock skills/risk-gated-agent-review/SKILL.md skills/practical-project-coding/SKILL.md
test -f skills/risk-gated-agent-review/SKILL.md
test -f skills/practical-project-coding/SKILL.md
test -f docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
test -f docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
test -f /home/minhhieu/.codex/skills/using-superpowers/SKILL.md
```

Expected: `git diff --check`, protected-path diff and protected-path status have
no output; all path checks exit 0. If the starting handoff does not contain the
exact base above, stop and return to Reviewer instead of choosing another base.

- [ ] **Step 6: Replace `CURRENT_HANDOFF.md` with the final-review packet**

Use these metadata values:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Head commit: worktree
Risk level: medium
Git authorization: none
```

Keep the exact 40-character implementation base from the starting handoff.
Point to the approved spec, plan and updated implementation report. Include the
changed-file list, acceptance mapping, observed scenario/check results,
failures/limitations, exact Reviewer reruns and these stop conditions:

```text
Do not modify runtime for Implementer.
Do not begin Notebook 08b.
Do not run backend/model/Qdrant unless an undeclared runtime diff is found.
Do not commit or push.
```

- [ ] **Step 7: Final self-review and stop**

Run:

```bash
git status --short
git diff --check
rg -n "TB[D]|TO[D]O|FIXM[E]|PLACEHOLDE[R]" session_prompt/Session_Prompt.md session_prompt/REVIEWER_WORKFLOW.md session_prompt/IMPLEMENTER_WORKFLOW.md session_prompt/Project_Status.md session_prompt/CURRENT_HANDOFF.md reports/risk_gated_agent_review_implementation_report.md
```

Expected: status lists only preserved unrelated files plus the approved
governance/lifecycle scope; diff check has no output; placeholder scan has no
output. Stop and hand off to Reviewer without running 08b or claiming approval.

## Implementation completion condition

Implementation is ready for independent review only when all five tasks are
complete, every required scenario is `PASS`, current state contains only the
approved 45+10/08a/three-model/Phase-8 facts, protected paths and both skills
have no diff, formatting checks pass, the implementation report is current and
`CURRENT_HANDOFF.md` targets Reviewer with `Head commit: worktree` and
`Git authorization: none`.
