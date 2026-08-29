# Risk-Gated Agent Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Do not dispatch sub-agents unless the user separately authorizes them. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable risk-gated Reviewer/Implementer coordination skill and replace Hue RAG's repetitive session bootstrap with a compact, single-handoff workflow.

**Architecture:** A generic shared skill defines the producer/consumer review protocol, while four project documents adapt it to Hue RAG. One `CURRENT_HANDOFF.md` routes the next role and selectively points to canonical context. The implementation changes governance documentation only; runtime behavior and Phase 8 artifacts remain untouched.

**Tech Stack:** Markdown, Git, shell read-only checks (`rg`, `wc`, `git diff`)

## Global Constraints

- Do not modify runtime code, tests, notebooks, dependencies, datasets, Qdrant or Phase 8 benchmark artifacts.
- Do not modify `skills/practical-project-coding/SKILL.md` or duplicate its coding and testing principles.
- Keep `risk-gated-agent-review` generic; Hue RAG paths and phase facts belong in project workflow/status/handoff files.
- Preserve all current source-of-truth, safety, secret, active-data and destructive-action boundaries.
- Keep exactly one active `session_prompt/CURRENT_HANDOFF.md`.
- Treat approximately 4,000 words for the four bootstrap files and 800 words for the handoff as soft diagnostic targets, never correctness gates.
- Do not add a parser, schema library, validator, linter, CI job, orchestration code or new dependency.
- Do not spawn sub-agents during implementation unless the user separately authorizes them.
- Do not commit or push unless the execution handoff or latest user instruction grants the exact Git authorization.
- Use `apply_patch` for edits and preserve unrelated worktree changes.

## Review Contract

**Risk level:** `medium`

**Expected triggers:** project-governance behavior, role permissions, context routing and Git authorization. No runtime, integration, model, database, public API or quality-metric trigger is expected.

**Implementer evidence required:**

- before/after word counts for the four bootstrap files;
- exact changed-file list and scoped diff;
- a responsibility map showing one canonical home for each retained rule;
- four tabletop scenario transcripts: 08b next-design, 08a replay, correction and closure;
- checks for required safety/authority language, handoff metadata and forbidden duplication;
- `git diff --check` and Markdown link/path existence checks;
- explicit confirmation that protected runtime/artifact paths have no diff.

**Reviewer minimum gate:** validate handoff/base/head, inspect every changed file and exact diff, check acceptance mapping, run `git diff --check`, repeat word counts and manually replay the four scenarios.

**Reviewer independent reruns:** documentation checks and tabletop replay only. No backend test, notebook execution, model run, Qdrant call, paid API or web research is required unless the implementation deviates from this plan.

**Evidence reuse during correction:** an unaffected tabletop scenario or document check may be reused when the correction handoff identifies why its inputs and routing rules did not change.

**New user authority required for:** runtime/artifact changes, a second active handoff, automated governance machinery, changing the role approval boundary, commit, push or any destructive operation.

---

## File responsibility map

| File | Responsibility |
|---|---|
| `skills/risk-gated-agent-review/SKILL.md` | Generic risk-gated producer/consumer protocol |
| `session_prompt/Session_Prompt.md` | Stable Hue RAG cross-session invariants and routing |
| `session_prompt/Project_Status.md` | Project README plus current snapshot and canonical map |
| `session_prompt/REVIEWER_WORKFLOW.md` | Reviewer-only authority, gates, verdicts and deliverables |
| `session_prompt/IMPLEMENTER_WORKFLOW.md` | Implementer-only authority, evidence, escalation, closure and Git rules |
| `session_prompt/CURRENT_HANDOFF.md` | The single active task, target role, Review Contract and context map |
| `reports/risk_gated_agent_review_implementation_report.md` | Detailed implementation evidence and tabletop results |

### Task 1: Establish the baseline and create the generic shared skill

**Files:**

- Create: `skills/risk-gated-agent-review/SKILL.md`
- Create: `reports/risk_gated_agent_review_implementation_report.md`

**Interfaces:**

- Consumes: approved design at `docs/superpowers/specs/2026-08-29-risk-gated-agent-review-design.md`
- Produces: one generic skill that both role workflows can reference; a report that later tasks append evidence to

- [ ] **Step 1: Inspect the worktree and capture the baseline**

Run:

```bash
git status --short
wc -w \
  session_prompt/Session_Prompt.md \
  session_prompt/Project_Status.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md
```

Expected: unrelated changes, if any, are identified and preserved. Record the four per-file counts and total in the implementation report. The design-session baseline was 10,540 words; the execution result is authoritative if it differs.

- [ ] **Step 2: Create the report with observed baseline evidence**

Create `reports/risk_gated_agent_review_implementation_report.md` with these exact headings:

```markdown
# Risk-Gated Agent Review Implementation Report

## 1. Phạm vi
## 2. Thay đổi chính
## 3. Cách đã kiểm tra
## 4. Kết quả quan sát
## 5. Lỗi và giới hạn
## 6. Handoff cho Reviewer
```

Under `Kết quả quan sát`, add a baseline table with one row per bootstrap file and one total row. Label the numbers as fresh observed word counts, not targets.

- [ ] **Step 3: Create the skill frontmatter and scope**

Create `skills/risk-gated-agent-review/SKILL.md` beginning with:

```markdown
---
name: risk-gated-agent-review
description: Use when a Reviewer and Implementer collaborate through specification, implementation evidence, independent risk-gated review, correction, approval closure, or cross-session handoff.
---

# Risk-Gated Agent Review
```

Add `Purpose` and `Non-goals` sections. State that the skill coordinates roles and context only. Explicitly defer coding, testing and debugging practices to project governance and applicable coding skills.

- [ ] **Step 4: Add the common bootstrap and handoff protocol**

Define the four-file bootstrap, tiered context loading and single-handoff invariant exactly as approved:

```text
Tier 0: session prompt, project status, role workflow, current handoff
Tier 1: Review Contract and exact base/head diff
Tier 2: affected source, focused checks and linked evidence selected by risk
Tier 3: live systems, external research or broad verification when necessary
```

Require target-role validation before task work. Use `Head commit: HEAD` when the handoff will be included in a checkpoint commit, or `Head commit: worktree` when no checkpoint commit is authorized. State that soft context targets cannot remove requirements or safety boundaries.

- [ ] **Step 5: Add the Reviewer branch**

The Reviewer branch must contain:

1. design gate and Review Contract ownership;
2. minimum independent diff gate;
3. risk-trigger table from the design;
4. delta correction behavior;
5. technical verdict and Approval Closure Contract ownership;
6. no runtime implementation for Implementer;
7. no sub-agent by default.

Do not copy Hue RAG model names, paths, phase numbers or Qdrant rules into the skill.

- [ ] **Step 6: Add the Implementer branch**

The Implementer branch must contain:

1. self-completion inside approved scope;
2. detailed evidence production plus compact handoff index;
3. mandatory deviation and blocker escalation;
4. prohibition on self-approval and risk reduction;
5. delta correction in one batch;
6. mechanical closure and Git operations only under exact authorization.

- [ ] **Step 7: Add evidence, correction and closure contracts**

Include the five handoff kinds (`next_design`, `implementation`, `final_review`, `correction`, `closure`), required metadata, evidence-reuse conditions and the three Git authorization values. Keep the Markdown human-readable; do not define a parser or machine schema.

- [ ] **Step 8: Verify the skill is generic and non-duplicative**

Run:

```bash
rg -n "Hue|Qdrant|Phase 8|E5|pytest|TDD|mock|fake" skills/risk-gated-agent-review/SKILL.md
rg -n "Reviewer|Implementer|CURRENT_HANDOFF|Review Contract|git_authorization" skills/risk-gated-agent-review/SKILL.md
```

Expected: the first command has no project-specific or coding-doctrine matches. The second command shows all coordination concepts. If `TDD`, `mock` or `fake` appears only in a sentence saying the skill does not define coding/test practice, remove the terms rather than preserving a duplicate policy.

- [ ] **Step 9: Record Task 1 evidence**

Update the implementation report with the skill path, section summary and the two verification commands with observed results.

- [ ] **Step 10: Commit Task 1 only when authorized**

If Git authorization is `commit` or `commit_and_push`, run:

```bash
git add skills/risk-gated-agent-review/SKILL.md reports/risk_gated_agent_review_implementation_report.md
git commit -m "docs: add risk-gated agent review skill"
```

If authorization is `none`, leave the files uncommitted and record `not authorized` in the report.

### Task 2: Compact the stable session prompt

**Files:**

- Modify: `session_prompt/Session_Prompt.md`
- Modify: `reports/risk_gated_agent_review_implementation_report.md`

**Interfaces:**

- Consumes: generic skill and existing project invariants
- Produces: stable cross-session routing without phase history; Project Status and role workflows rely on these precedence rules

- [ ] **Step 1: Build a keep/move/delete responsibility inventory**

Before editing, list each current top-level section in the report under one of:

- `keep here`: source of truth, role routing, safety, secrets, worktree, context tiers;
- `move by pointer`: current project/phase facts to Project Status, role behavior to workflows, coding behavior to `practical-project-coding`;
- `remove duplicate/history`: repeated Phase 8 details and completed lifecycle narrative already canonical elsewhere.

Every removed requirement must have a named canonical destination. Do not delete a rule merely to reduce word count.

- [ ] **Step 2: Rewrite the prompt around stable responsibilities**

Use these top-level sections:

```markdown
# Session Prompt
## Repository and communication
## Source of truth
## Role routing
## Context loading
## Stable project boundaries
## Safety, secrets and destructive actions
## Coding and verification routing
## Git authorization
```

Retain the repository path, Vietnamese communication convention, source-of-truth order, active-data read-only rule, safe `.env` handling, worktree preservation and separate authorization for provider/model/scope/deploy/active mutation/destructive action.

Point to `Project_Status.md` for current runtime/phase facts, to the role workflow for role behavior, to `risk-gated-agent-review` for coordination, and to `practical-project-coding` for code/test practice.

- [ ] **Step 3: Remove phase chronology and repeated doctrine**

Remove the long Phase 0–8 history, exact current model matrix, Golden V2/V3 narrative, notebook topology details and repeated test/simplicity lists from this file. Confirm that current facts remain reachable from Project Status or canonical pointers.

- [ ] **Step 4: Verify retained invariants**

Run:

```bash
rg -n "nguồn sự thật|Role routing|CURRENT_HANDOFF|risk-gated-agent-review|practical-project-coding|read-only|secret|commit|push" session_prompt/Session_Prompt.md
rg -n "Golden Dataset V2|Qwen3 Embedding|Notebook 08a|Phase 0–6" session_prompt/Session_Prompt.md
wc -w session_prompt/Session_Prompt.md
```

Expected: every retained invariant is present. Historical phase terms are absent unless a short sentence is required to route to Project Status. The word count is substantially lower; no hard maximum applies.

- [ ] **Step 5: Record Task 2 evidence and commit only when authorized**

Add the inventory summary and new word count to the report. If authorized:

```bash
git add session_prompt/Session_Prompt.md reports/risk_gated_agent_review_implementation_report.md
git commit -m "docs: compact stable session instructions"
```

### Task 3: Rewrite Project Status as project map plus current snapshot

**Files:**

- Modify: `session_prompt/Project_Status.md`
- Modify: `reports/risk_gated_agent_review_implementation_report.md`

**Interfaces:**

- Consumes: current repository state and approved Phase 8 status
- Produces: enough project context for a new agent without historical audit narrative

- [ ] **Step 1: Verify current facts before rewriting**

Read the current status and canonical Phase 8 guide. Confirm the facts that must survive:

- Hue cultural/tourism RAG and Hue Foods RAG MVP goals;
- `raw → curated Markdown → chunks → index → retrieval → context → answer`;
- 572 chunks and active `hue_foods_e5_small_384` read-only collection;
- active E5-small production embedding and current retrieval/generation components;
- Phase 0–7 approved, Phase 8 not ready with 08a approved, Phase 9 not ready;
- Golden V3 45 full plus 10 smoke cases;
- local dense catalog E5-small, Huydang DEk21 and E5-base;
- MiniLM-L12 and Qwen embedding historical rows are not executable scope;
- next action is research/brainstorm exact Notebook 08b;
- no 08b implementation/run, paid API, active mutation or cutover authorization.

If a fact is no longer supported by the repository, record the discrepancy instead of silently copying it.

- [ ] **Step 2: Rewrite with current-only sections**

Use these top-level sections:

```markdown
# Project Status
## Project overview
## System and data map
## Current runtime and data
## Phase status
## Decisions currently in force
## Safety and authorization boundaries
## Canonical document map
## Current next action
```

Keep the phase table compact. Describe only current state and the minimum background needed to interpret it.

- [ ] **Step 3: Remove audit history**

Remove revision-by-revision Phase 0–8 stories, old test counts, detailed correction narratives and retired prompt inventories. Add one sentence explaining that Git and linked canonical artifacts retain history.

- [ ] **Step 4: Verify Project Status as a standalone project map**

Run:

```bash
rg -n "Hue Foods RAG|572|hue_foods_e5_small_384|read-only|45|10|e5-small-384|huydang-dek21-embedding-768|e5-base-768|08b" session_prompt/Project_Status.md
rg -n "lần `changes_requested`|correction vòng|Observed Phase|revision" session_prompt/Project_Status.md
wc -w session_prompt/Project_Status.md
```

Expected: all current facts appear, historical narrative searches return no long audit sections, and the file is materially smaller while still functioning as the repository's README-level map.

- [ ] **Step 5: Record Task 3 evidence and commit only when authorized**

Update the report with preserved facts, removed history categories and word count. If authorized:

```bash
git add session_prompt/Project_Status.md reports/risk_gated_agent_review_implementation_report.md
git commit -m "docs: make project status a current project map"
```

### Task 4: Refactor the paired role workflows

**Files:**

- Modify: `session_prompt/REVIEWER_WORKFLOW.md`
- Modify: `session_prompt/IMPLEMENTER_WORKFLOW.md`
- Modify: `reports/risk_gated_agent_review_implementation_report.md`

**Interfaces:**

- Consumes: shared skill and stable session rules
- Produces: project-specific Reviewer and Implementer authority without duplicated common protocol

- [ ] **Step 1: Rewrite Reviewer Workflow**

Use these top-level sections:

```markdown
# Codex Reviewer Workflow
## Purpose and required skill
## Session bootstrap
## Design gate
## Final review gate
## Hue RAG risk and safety adapter
## Findings and verdicts
## Correction and approval closure
## Reviewer-owned documents
## Git boundary
```

Require reading only the four bootstrap files first. Preserve the three verdicts and severity meanings. Preserve the prohibition on runtime implementation, implementation-report edits, unapproved active mutation, secret exposure and unauthorized Git. Point to the shared skill for generic diff/evidence/risk protocol and to `practical-project-coding` only when reviewing code/tests.

- [ ] **Step 2: Rewrite Implementer Workflow**

Use these top-level sections:

```markdown
# Implementer Workflow
## Purpose and required skill
## Session bootstrap
## When implementation may start
## Work inside approved scope
## Hue RAG safety adapter
## Self-review and evidence
## Corrections
## Approval closure
## Documentation ownership
## Git authorization
```

Preserve Implementer's inability to self-approve or change approved scope. Allow technical docs, report and current handoff edits inside the plan. Preserve active collection safety, secret handling and exact approved-target rules. Route general implementation/test practice to `practical-project-coding` rather than copying it.

- [ ] **Step 3: Check complementary ownership**

Create a two-column table in the implementation report for:

- spec/plan/Review Contract;
- runtime/tests/notebooks/dependencies;
- implementation report and technical docs;
- Codex review/user report/guide/status;
- `CURRENT_HANDOFF.md`;
- closure edits;
- commit/push.

For each item, name decision owner, editing role and authorization condition. Resolve every overlap before proceeding.

- [ ] **Step 4: Verify role boundaries and remove duplicated doctrine**

Run:

```bash
rg -n "risk-gated-agent-review|CURRENT_HANDOFF|ready_for_user_confirmation|changes_requested|blocked|blocker|major|minor|runtime|implementation report|commit|push" session_prompt/REVIEWER_WORKFLOW.md
rg -n "risk-gated-agent-review|CURRENT_HANDOFF|self-review|self-approve|closure|git_authorization|technical" session_prompt/IMPLEMENTER_WORKFLOW.md
rg -n "test-count|coverage|mock|fake|TDD|factory|wrapper" session_prompt/REVIEWER_WORKFLOW.md session_prompt/IMPLEMENTER_WORKFLOW.md
wc -w session_prompt/REVIEWER_WORKFLOW.md session_prompt/IMPLEMENTER_WORKFLOW.md
```

Expected: role and lifecycle terms are present. The third command returns no duplicated coding doctrine except a short pointer explaining where those rules live.

- [ ] **Step 5: Record Task 4 evidence and commit only when authorized**

Update the report with the ownership table, duplicate scan and word counts. If authorized:

```bash
git add session_prompt/REVIEWER_WORKFLOW.md session_prompt/IMPLEMENTER_WORKFLOW.md reports/risk_gated_agent_review_implementation_report.md
git commit -m "docs: adopt risk-gated role workflows"
```

### Task 5: Create the rollout final-review handoff

**Files:**

- Create: `session_prompt/CURRENT_HANDOFF.md`
- Modify: `reports/risk_gated_agent_review_implementation_report.md`

**Interfaces:**

- Consumes: completed governance diff and Review Contract
- Produces: the first active handoff, targeted to Reviewer for independent workflow review

- [ ] **Step 1: Resolve exact Git state**

Run:

```bash
git rev-parse HEAD
git status --short
```

Use the execution handoff's approved base commit as `Base commit`. If the final handoff will be included in an authorized checkpoint commit, write the exact literal `HEAD` as `Head commit`; otherwise write the exact literal `worktree`. `HEAD` avoids requiring a file to contain the hash of the commit that contains that file.

- [ ] **Step 2: Create the handoff metadata**

Begin `session_prompt/CURRENT_HANDOFF.md` with these fixed metadata lines:

```markdown
# Current Handoff

Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Risk level: medium
```

Add `Base commit:` followed by the observed 40-character execution-base SHA.
Add `Head commit: HEAD` when committing the final handoff, or `Head commit:
worktree` when Git authorization is `none`. Add `Git authorization:` followed
by exactly `none`, `commit` or `commit_and_push`, matching current authority.

- [ ] **Step 3: Add the compact evidence packet**

Use the eleven handoff sections from the design. The objective is independent review of the risk-gated workflow rollout. Link the approved design, this plan and implementation report. Include the exact changed-file list, word-count summary, responsibility map, tabletop results, deviations and unverified items.

The Reviewer rerun list is limited to the Review Contract. State explicitly that backend tests, notebooks, Qdrant, models, paid APIs and production cutover are out of scope.

- [ ] **Step 4: Add the proposed post-approval closure**

Describe, but do not execute, the steady-state replacement handoff:

- target role `reviewer`;
- authored by the closure Implementer;
- handoff kind `next_design`;
- objective: research and brainstorm exact Phase 8 Notebook 08b;
- canonical pointers: compact project status, Phase 8 guide, master design/plan and relevant benchmark report sections;
- no authorization for 08b implementation/run, paid API, active Qdrant mutation or production cutover.

- [ ] **Step 5: Verify the handoff**

Run:

```bash
rg -n "^Target role: reviewer$|^Authored by: implementer$|^Handoff kind: final_review$|^State: active$|^Base commit:|^Head commit:|^Risk level: medium$|^Git authorization:" session_prompt/CURRENT_HANDOFF.md
rg -n "TB[D]|TO[D]O|PLACEHOLDE[R]" session_prompt/CURRENT_HANDOFF.md
wc -w session_prompt/CURRENT_HANDOFF.md
```

Expected: all metadata matches; the placeholder scan has no output; the handoff is near the soft target or explains why additional context is needed.

- [ ] **Step 6: Record Task 5 evidence**

Update the report with the resolved base/head state, handoff word count and proposed closure summary. Do not commit yet because final report/tabletop evidence remains.

### Task 6: Run the tabletop replay and complete the report

**Files:**

- Modify: `reports/risk_gated_agent_review_implementation_report.md`
- Modify if a defect is found: the exact governance file responsible for that defect

**Interfaces:**

- Consumes: all completed workflow documents
- Produces: observed evidence that the workflow routes four representative scenarios correctly

- [ ] **Step 1: Replay the 08b next-design scenario**

Read only the proposed steady-state bootstrap bundle. Record whether a fresh Reviewer can identify:

- Phase 8 08a is complete;
- next action is 08b research/brainstorming;
- specs/plans must be created before implementation;
- 08b run, paid API, active mutation and cutover are not authorized.

Record each result as `PASS`, `FAIL` or `AMBIGUOUS` with the exact supporting file/section.

- [ ] **Step 2: Replay the 08a cleanup scenario**

Using the Review Contract matrix, classify removal of unused models, dependency and isolated collections while retained encoding/retrieval/scoring remains unchanged. Confirm the workflow selects:

- exact diff review;
- focused deterministic tests;
- lock resolution check;
- safe read-only Qdrant schema/count inspection when relevant;
- no rerun of unchanged embedding benchmarks.

Record the decision path and supporting rule.

- [ ] **Step 3: Replay a major correction**

Simulate one out-of-scope executable model setting discovered during final review. Confirm Reviewer creates one `correction` handoff containing severity, affected requirement, exact delta, reruns and reusable evidence. Confirm Implementer cannot self-close the finding and the next Reviewer does not restart unrelated verification.

- [ ] **Step 4: Replay approval closure**

Simulate technical readiness followed by user confirmation. Confirm Reviewer authors the closure decision, Implementer changes only exact approved fields, Git work follows authorization, and the final handoff becomes `next_design` for 08b.

- [ ] **Step 5: Measure the final bootstrap**

Run:

```bash
wc -w \
  session_prompt/Session_Prompt.md \
  session_prompt/Project_Status.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md \
  session_prompt/CURRENT_HANDOFF.md
```

Report old total, new four-file total for each role, handoff count, absolute reduction and percentage reduction. If a bundle exceeds the soft target, explain which retained context requires it.

- [ ] **Step 6: Complete all six report sections**

The report must distinguish expected design behavior from observed tabletop results. List every failed, ambiguous, skipped and not-verified item. State explicitly that no runtime test/live service was run because no runtime behavior changed.

### Task 7: Final scope and consistency audit

**Files:**

- Modify only if defects are found: files listed in the File responsibility map

**Interfaces:**

- Consumes: complete governance implementation and evidence
- Produces: a clean, bounded final-review worktree or checkpoint commit

- [ ] **Step 1: Confirm protected paths have no diff**

Run:

```bash
git diff --name-only "$(sed -n 's/^Base commit: //p' session_prompt/CURRENT_HANDOFF.md)" -- \
  backend \
  notebooks \
  evaluation/results \
  pyproject.toml \
  uv.lock \
  skills/practical-project-coding/SKILL.md
```

Expected: no output.

- [ ] **Step 2: Audit the exact changed-file allowlist**

Run:

```bash
git status --short
git diff --name-only "$(sed -n 's/^Base commit: //p' session_prompt/CURRENT_HANDOFF.md)"
```

Expected changed paths are limited to the seven files in the File responsibility map. The approved design/plan may also be modified only for status or consistency corrections authored before implementation; record them separately rather than hiding them in implementation scope.

- [ ] **Step 3: Scan for placeholders, duplicate active handoffs and formatting errors**

Run:

```bash
rg -n "TB[D]|TO[D]O|FIXM[E]|PLACEHOLDE[R]" \
  skills/risk-gated-agent-review/SKILL.md \
  session_prompt/Session_Prompt.md \
  session_prompt/Project_Status.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md \
  session_prompt/CURRENT_HANDOFF.md \
  reports/risk_gated_agent_review_implementation_report.md
find session_prompt -maxdepth 1 -type f -name '*HANDOFF*.md' -print
git diff --check
```

Expected: placeholder scan has no output; exactly `session_prompt/CURRENT_HANDOFF.md` is the active handoff file; `git diff --check` has no output. Historical files whose names contain `HANDOFF` must be retired from the current tree only when they are true operational entrypoints and the plan explicitly identifies them; do not broad-delete documentation.

- [ ] **Step 4: Verify canonical pointers exist**

For every repository-relative Markdown path in the four bootstrap files and current handoff, verify the target exists with `test -e`. Record any external link as not checked unless it is necessary for current behavior. Do not add a permanent link-checker script.

- [ ] **Step 5: Review the full diff for one-home ownership**

Read:

```bash
git diff "$(sed -n 's/^Base commit: //p' session_prompt/CURRENT_HANDOFF.md)" -- \
  skills/risk-gated-agent-review/SKILL.md \
  session_prompt/Session_Prompt.md \
  session_prompt/Project_Status.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md \
  session_prompt/CURRENT_HANDOFF.md \
  reports/risk_gated_agent_review_implementation_report.md
```

For every repeated rule, keep the full rule only in its canonical owner and replace other copies with a pointer. Do not remove a repeated safety boundary when local visibility is necessary to prevent an unsafe action; record that exception in the report.

- [ ] **Step 6: Create the final checkpoint only when authorized**

If authorization is `commit` or `commit_and_push`, stage exactly the seven implementation files and any approved spec/plan status corrections, run `git diff --cached --check`, then commit:

```bash
git add \
  skills/risk-gated-agent-review/SKILL.md \
  session_prompt/Session_Prompt.md \
  session_prompt/Project_Status.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md \
  session_prompt/CURRENT_HANDOFF.md \
  reports/risk_gated_agent_review_implementation_report.md
git diff --cached --check
git commit -m "docs: adopt risk-gated agent review workflow"
```

Include approved design/plan files in the same commit only if their uncommitted diff is limited to user-approved status or consistency changes. If authorization includes push, run `git push` only after the commit succeeds. Otherwise report the exact uncommitted worktree state.

- [ ] **Step 7: Final handoff**

Ensure `CURRENT_HANDOFF.md` contains the actual base and the correct symbolic
head state. A committed checkpoint uses `Head commit: HEAD`; Reviewer resolves
and records the SHA at review start. An uncommitted handoff uses `Head commit:
worktree`. End the implementation report with the exact Reviewer bootstrap
prompt and stop without claiming approval.

## Implementation completion condition

Implementation is ready for Reviewer only when all seven tasks are complete, all four tabletop scenarios are `PASS`, the final handoff is unambiguous, protected paths have no diff, formatting checks pass and every limitation is reported. The Implementer must not begin Phase 8 08b or execute the proposed closure.
