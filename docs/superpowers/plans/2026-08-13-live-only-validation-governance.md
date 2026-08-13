# Live-Only Validation Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align shared governance and the project handoff snapshot with the user-approved live-only validation policy before a separate session migrates the backend test suite.

**Architecture:** This is a documentation-only change. The session prompt defines global policy, the role workflows define execution and review duties, and `Project_Status.md` records verified state without approving Phase 6 prematurely.

**Tech Stack:** Markdown, `rg`, Git diff validation.

## Global Constraints

- Modify only `session_prompt/Session_Prompt.md`, `session_prompt/Project_Status.md`, `session_prompt/IMPLEMENTER_WORKFLOW.md`, and `session_prompt/REVIEWER_WORKFLOW.md`.
- Do not modify runtime code, notebooks, tests, settings, guides, technical reports, or data.
- Do not call provider APIs, models, web services, or Qdrant in this session.
- Never read, print, or store credentials.
- Do not commit or push; the user has not authorized a commit.
- The active Hue Qdrant collection remains read-only. A future marked isolated test collection alone may be created, written, or deleted.
- Live logs may include full question, full answer, model ID, latency, usage, and estimated cost; never include credentials, system prompt, raw provider payload, or full retrieved context.

---

### Task 1: Update the shared live-only policy

**Files:**
- Modify: `session_prompt/Session_Prompt.md`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-08-13-live-only-validation-governance-design.md`.
- Produces: global policy for both role workflows.

- [ ] **Step 1: Replace default API/test rules**

Add an explicit `Live-Only Validation Policy` section that states runtime, canonical notebooks, and backend tests use real dependencies and results; prohibits fake/mock clients, fake runners, sample vectors, replay fixtures, fake Qdrant clients, and opt-in real-mode guards; permits network/provider APIs; and classifies provider/network/quota/model errors as real failures without a fake fallback.

- [ ] **Step 2: Specify model, logging, and Qdrant boundaries**

State that `gpt-5.4-nano` serves generation/API integration validation, `gpt-5.4-mini` is only for identified judge/quality evaluation, permitted log fields are question/answer/model/latency/usage/cost, prohibited fields are credentials/system prompt/raw provider payload/full context, and only an isolated marked test collection may be mutated or deleted.

- [ ] **Step 3: Validate Task 1**

Run:

```bash
rg -n -i 'fake|mock|fixture|offline|live-only|gpt-5\.4|qdrant' session_prompt/Session_Prompt.md
```

Expected: no active rule permits fake/mock/offline default behavior.

### Task 2: Update Implementer and Reviewer duties

**Files:**
- Modify: `session_prompt/IMPLEMENTER_WORKFLOW.md`
- Modify: `session_prompt/REVIEWER_WORKFLOW.md`

**Interfaces:**
- Consumes: Task 1 global policy.
- Produces: role duties aligned with live-only validation.

- [ ] **Step 1: Replace Implementer test/live policy**

Require dependency preflight, real Qdrant/model/provider paths, permitted operational logs, report evidence for model/call/latency/usage/cost, and isolated collection cleanup result. Remove default mock/dry-run/fixture/offline testing language.

- [ ] **Step 2: Replace Reviewer validation policy**

Require verification of live evidence, provider/model identity, safe logging, active-collection protection, isolated collection lifecycle and cleanup. State a provider/network error is a validation failure, never a trigger to use a fake result.

- [ ] **Step 3: Validate Task 2**

Run:

```bash
rg -n -i 'fake|mock|fixture|offline|dry-run|live|collection|cleanup|gpt-5\.4' session_prompt/IMPLEMENTER_WORKFLOW.md session_prompt/REVIEWER_WORKFLOW.md
```

Expected: fake/mock references are prohibitions or historical context only.

### Task 3: Refresh the Project Status snapshot

**Files:**
- Modify: `session_prompt/Project_Status.md`

**Interfaces:**
- Consumes: existing Phase 6 live-smoke/runtime-audit evidence and Tasks 1–2 policy.
- Produces: UTC+7 snapshot and future migration handoff.

- [ ] **Step 1: Replace obsolete Phase 6 claims**

Replace `blocked`, absent-credential, and default-fake notebook claims with verified live evidence: 12 Phase 6 smoke calls costing `$0.01493875`, one audit live call reporting `421/48`, runtime-real notebooks 01–06, and 274 backend tests. Keep Phase 6 `awaiting_user_confirmation`, not `approved`.

- [ ] **Step 2: Record policy and next action**

Add a UTC+7 policy decision covering unrestricted approved live testing, model split, verbose safe logs, isolated test collection, active collection protection, and the future DeepSeek full test-suite migration.

- [ ] **Step 3: Validate Task 3**

Run:

```bash
rg -n -i 'blocked|awaiting_user_confirmation|fake mode|live smoke|274|next action' session_prompt/Project_Status.md
```

Expected: current snapshot does not contradict verified live evidence or the new policy.

### Task 4: Cross-file validation and handoff prompt

**Files:**
- Modify: the four approved governance files only.

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: coherent policy and a user-copyable DeepSeek prompt.

- [ ] **Step 1: Scan for policy contradictions**

Run:

```bash
rg -n -i 'default.*offline|tests.*offline|default.*fake|mock.*test|fake.*test|real-mode guard' session_prompt/Session_Prompt.md session_prompt/Project_Status.md session_prompt/IMPLEMENTER_WORKFLOW.md session_prompt/REVIEWER_WORKFLOW.md
```

Expected: no active instruction permits fake/mock/fallback test behavior.

- [ ] **Step 2: Audit scope and diff**

Run:

```bash
git diff --check
git diff --name-only -- session_prompt/Session_Prompt.md session_prompt/Project_Status.md session_prompt/IMPLEMENTER_WORKFLOW.md session_prompt/REVIEWER_WORKFLOW.md
```

Expected: clean Markdown diff; only approved governance files are edited by this execution, apart from pre-existing worktree changes.

- [ ] **Step 3: Provide detailed DeepSeek prompt**

Require inventory/replacement of existing backend test fakes/mocks, real dependency preflight, isolated Qdrant lifecycle, `gpt-5.4-nano` generation/API tests, reserved `gpt-5.4-mini` judge tests, safe verbose logs, secret protection, implementation report evidence, and no commit/push.
