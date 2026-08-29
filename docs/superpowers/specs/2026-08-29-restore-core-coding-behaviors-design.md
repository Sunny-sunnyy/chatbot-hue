# Restore Core Coding Behaviors Design

Status: approved
Date: 2026-08-29 +07
User approval: 2026-08-29 +07
Scope: governance correction for Hue RAG coding, implementation and review behavior

## 1. Problem

The `risk-gated-agent-review` rollout correctly introduced a compact bootstrap,
one active handoff and risk-based Reviewer/Implementer coordination. During that
refactor, however, the three core governance files lost much of the explicit
behavior that previously governed simplicity, implementation, testing,
debugging, live verification and technical review:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
```

The shared `practical-project-coding` skill retains the general direction, but
the Hue RAG bootstrap no longer makes all project-specific expectations visible
or operational for each role. This is a `major` correction to the current
governance rollout, not an independent enhancement and not a rollback to the
old document structure.

## 2. Goals

1. Restore the approved core behaviors from `session_prompt_old` for clear,
   simple and proportionate code.
2. Restore exact expectations for useful tests, root-cause debugging, fresh
   real-system evidence, notebooks, data safety and role-specific review.
3. Preserve the compact risk-gated bootstrap, Review Contract, correction,
   closure and handoff lifecycle.
4. Keep current project facts separate from stable operating principles.
5. Remove or update superseded phase-specific facts instead of copying old
   text verbatim.
6. Keep the two existing project skills unchanged and non-conflicting.

## 3. Non-goals

This correction does not:

- change runtime code, tests, dependencies, datasets, notebooks, Qdrant or
  benchmark artifacts;
- modify `skills/risk-gated-agent-review/SKILL.md`;
- modify `skills/practical-project-coding/SKILL.md`;
- restore phase timelines or retired model/dataset history to the three
  behavior files;
- create a governance validator, linter, parser, CI job or orchestration layer;
- authorize Phase 8 Notebook 08b implementation or execution;
- authorize paid API use, active collection mutation, production cutover,
  commit or push.

## 4. Selected approach

Use a behavior-preserving merge organized by responsibility.

- Keep the risk-gated coordination architecture.
- Restore shared Hue RAG policies in `Session_Prompt.md`.
- Restore Reviewer-specific enforcement in `REVIEWER_WORKFLOW.md`.
- Restore Implementer-specific execution behavior in
  `IMPLEMENTER_WORKFLOW.md`.
- Keep current facts and next action in `Project_Status.md` and
  `CURRENT_HANDOFF.md`.
- Repeat only short skill and safety pointers where local visibility prevents a
  role from missing a required boundary.

This is preferred over copying the old files nearly verbatim because the old
files mix stable behavior with completed phase history. It is preferred over a
pointer-only bootstrap because that was the cause of the behavior becoming too
implicit.

## 5. Responsibility map

| File | Canonical responsibility |
|---|---|
| `skills/risk-gated-agent-review/SKILL.md` | Role coordination, context tiers, Review Contract, evidence reuse, correction, closure and Git authorization |
| `skills/practical-project-coding/SKILL.md` | Reusable implementation principles for direct data flow, proportional complexity, surgical scope, useful tests and real evidence |
| `session_prompt/Session_Prompt.md` | Stable Hue RAG policies shared by Reviewer and Implementer |
| `session_prompt/REVIEWER_WORKFLOW.md` | Reviewer authority and the operational application of simplicity, test and live-evidence policies |
| `session_prompt/IMPLEMENTER_WORKFLOW.md` | Implementer authority and the operational application of coding, testing, debugging and handoff policies |
| `session_prompt/Project_Status.md` | Current project, phase, runtime, data and next-action snapshot |
| `session_prompt/CURRENT_HANDOFF.md` | One exact active task, role, scope, Review Contract, authority and stop condition |

## 6. Skill loading contract

Every task starts with `using-superpowers`, then loads the four Hue RAG
bootstrap documents and validates the role and handoff.

The two project-local skills remain at:

```text
skills/risk-gated-agent-review/SKILL.md
skills/practical-project-coding/SKILL.md
```

Codex Reviewer uses its native skill-loading mechanism. Gemini Implementer is
explicitly told that Superpowers skills are available under:

```text
~/.codex/skills/
```

`risk-gated-agent-review` is mandatory for role coordination.
`practical-project-coding` is mandatory for implementation design, code, tests,
debugging, refactoring, notebooks, dependencies and technical code review.
Other Superpowers skills are selected by `using-superpowers` only when their
triggers apply. The presence of parallel-agent skills does not grant authority
to use sub-agents; the Review Contract or user must authorize that separately.

## 7. `Session_Prompt.md` design

`Session_Prompt.md` keeps the current source-of-truth order, role routing,
four-file bootstrap and tiered context loading. It adds the following explicit
shared policies.

### 7.1. Simplicity by default

- Code is clear, readable, explainable and easy to trace through its data flow.
- Start with the smallest solution that fully satisfies the real requirement.
- A unit of code has a responsibility that can be named in ordinary language.
- Do not add speculative abstraction, wrapper, validator, state machine,
  configurability or workflow.
- Do not optimize for hypothetical future cases or keep a mechanism because
  effort has already been spent on it.
- Advanced techniques require an observed problem, an inadequate direct
  solution, a concrete benefit, real-system evidence and proportionate added
  complexity.
- Reviewer treats unjustified over-engineering as a finding.

### 7.2. Proportionate tests and verification

- A test protects required user behavior, an important contract or a real bug
  whose recurrence cost is meaningful.
- Do not optimize for test count, coverage or number of test files.
- Do not use mock, fake or stub dependencies. Pure deterministic logic may use
  small, direct and valid values; these values are not integration evidence.
- Test success does not replace a live integration run when acceptance depends
  on a real database, model, provider, API or service.
- Start with the exact live path and the smallest useful test.
- Run the full backend suite only when a shared contract or real blast radius
  justifies it in the Review Contract.
- Golden V3 has 45 canonical full cases and a 10-row deep-equal smoke subset.
  Smoke is suitable for a bounded check; a change that can affect the benchmark
  quality decision requires the full 45 cases.
- Do not fabricate a failure by using a dead URL, deleting a collection or
  changing the environment solely to create an imagined edge case.

### 7.3. Debugging and self-review

Use this sequence for a real bug:

```text
reproduce consistently -> collect evidence -> prove root cause
-> try one focused fix -> rerun the exact live path
```

Do not change several hypotheses at once or hide a failure behind stacked
fallbacks and guards. Add a regression test only for an important bug with a
credible recurrence risk. Review the exact diff for scope creep, duplication,
one-caller helpers, unnecessary code/tests, speculative abstraction, unclear
data flow and the security boundary actually affected.

### 7.4. Real systems, online services and secrets

- Use canonical data and the real approved backend, Qdrant, dependency, model,
  API and provider path.
- Do not use fake IDs, datasets, providers, responses, artifacts, replay or old
  output as fresh PASS evidence.
- Record failed, skipped, partial and not-verified results accurately.
- Active production data is read-only unless an exact target mutation has been
  approved.
- An online or paid run already approved by its guide/plan does not need a
  repeated consent gate, cost cap or cost-accounting mechanism.
- A new provider/model/dataset/scope, deploy, active mutation or destructive
  action requires new authority.
- Load the repository `.env` through a safe env-file mechanism. Never open,
  search, print, log or request secret values in chat.

### 7.5. Remove complexity that serves no real need

Restore the old rule with its original conditional meaning: mechanisms must be
removed when they do not serve a real need. This is not a permanent blacklist.
The examples include cost accounting, repeated consent gates, calibration,
resume workflows, run identities, timestamp packages, checksums, package
matching, tamper detection, partial artifacts, complex artifact audits, layered
validators and tests that exist only to protect those mechanisms.

A mechanism may be justified only through an observed need and proportionate
evidence. A mechanism that an approved scope already requires removing cannot
be retained by renaming or moving it.

### 7.6. Python, curated data and notebooks

- `uv` is the project runtime: `pyproject.toml + uv.lock -> uv -> project
  .venv -> uv run <command>`.
- Use `uv sync`, not `pip install`, and do not use system Python as project PASS
  evidence.
- Offline environment flags are used only when the exact contract requires
  them.
- Curated Markdown starts with `#`, has no YAML frontmatter or empty invented
  fields, keeps minimal source tracking under `## Nguồn dữ liệu`, and remains
  natural and answer-facing.
- External research stays separate from closed-world evidence. A conflict is
  reported with source, date and impact rather than silently changing corpus
  truth.
- A notebook exists only when its guide identifies real learning value. It has
  one purpose per cell, short Markdown before short code, calls backend code,
  does not duplicate the pipeline or become a validator/test suite, stores no
  secrets, and remains clean in the repository.
- When notebook execution is part of acceptance, Reviewer runs a temporary
  copy through the real path.

### 7.7. State and worktree boundaries

Project phase sequence and current facts belong in `Project_Status.md`. Exact
task state belongs in `CURRENT_HANDOFF.md`. `Session_Prompt.md` contains no
timeline. Worktree changes outside scope are preserved, destructive targets are
resolved exactly, and commit/push requires exact authorization.

## 8. `REVIEWER_WORKFLOW.md` design

The Reviewer workflow retains the risk-gated design gate, minimum independent
diff gate, correction and closure lifecycle. It restores these operational
behaviors:

- ask what real behavior code serves, whether a more direct solution exists,
  whether data flow is understandable, what observed problem an advanced
  mechanism solves, what real evidence proves its benefit, and whether the
  benefit is proportionate;
- treat over-engineering as a `major` when it makes the implementation harder
  than the real need or preserves a mechanism without demonstrated value;
- audit a test before running or retaining it and require a clear user behavior,
  important contract or real recurrence risk;
- reject mock/fake/stub dependencies and fake/replayed completion evidence;
- select exact real-system verification for the integration, model, retrieval,
  scoring, API or quality path actually changed;
- use smoke 10 for a justified bounded check and full 45 when a quality
  decision may change;
- avoid full suites and live services for documentation-only or unchanged
  behavior merely to create a checkpoint;
- review bug fixes through reproduction, root cause, one focused correction and
  an exact rerun;
- create one bounded correction delta and reuse only evidence whose inputs,
  dependencies, environment and data flow remain unchanged;
- stop before correction five after four `changes_requested` verdicts and audit
  the guide, design, plan, acceptance, findings and new mechanisms;
- keep CodeGraph optional and subordinate to source and fresh execution;
- review notebooks only when required by the guide and learning contract;
- use project severity and verdicts and produce the canonical Codex review,
  user report and Approval Closure Contract when the lifecycle requires them.

Reviewer never repairs runtime for Implementer, edits the implementation report
or approves before user confirmation.

## 9. `IMPLEMENTER_WORKFLOW.md` design

The Implementer workflow retains approved-plan entry, complete in-scope
execution, detailed evidence, compact handoff, correction and mechanical
closure. It restores these operational behaviors:

- explain the data flow, start with the smallest complete solution, keep clear
  responsibilities and reuse the production backend instead of copying a
  second pipeline;
- avoid speculative abstraction, wrapper, validator, flexibility, state and
  workflow, as well as unrelated refactoring;
- remove imports/helpers/code made unnecessary by the current change and never
  rename or relocate a mechanism to evade an approved removal;
- create and retain only useful tests, reject mock/fake/stub dependencies, use
  direct valid values for pure deterministic logic, and use canonical data and
  real dependencies for integration behavior;
- begin verification with the exact live path and smallest useful test, use the
  10-row smoke subset for bounded checks, use all 45 cases when a quality
  decision may change, and run broad suites only for a justified shared blast
  radius;
- debug through consistent reproduction, root-cause evidence, one focused fix
  and an exact rerun rather than stacked guards or fallbacks;
- self-review the exact diff for scope, duplication, unnecessary code/tests,
  speculative complexity, data-flow clarity and the actual security boundary;
- use canonical data and real approved services, record all non-PASS outcomes,
  keep active data read-only without exact authority, and never change a
  provider/model/device/dataset merely to make a run pass;
- distinguish fresh evidence for changed behavior from explicitly justified
  evidence reuse for an unchanged correction path;
- use `uv`, safe environment loading, learning-focused notebooks and optional
  CodeGraph according to the shared policy;
- finish with the six-section implementation report, compact final-review
  handoff, exact changed files, `git diff --check`, Git state and one next role.

Implementer does not self-approve, lower risk, change requirements/spec/plan to
fit implementation, or modify Reviewer-owned decisions outside an exact
closure contract.

## 10. Compatibility with `risk-gated-agent-review`

The restored behavior is compatible with the coordination skill under these
rules:

1. `using-superpowers` is the platform-level first action; the Hue RAG
   four-file bootstrap remains the first project-context load.
2. The Review Contract selects exact verification inside the stable Hue RAG
   guardrails. It does not turn full suites or full evaluation into defaults.
3. Changed behavior requires fresh evidence. Evidence from an unchanged path in
   the same correction series may be reused only under the skill's stated
   conditions and is never described as a fresh run.
4. Real-system execution is triggered by the actual integration risk. A
   documentation-only change does not run backend/model/Qdrant merely for a
   checkpoint.
5. The skill remains the canonical owner of role coordination; the three
   project files own project policy and role-specific application.

## 11. Current-state updates

`Project_Status.md` is updated only with current facts needed by the next agent:

- Golden V3 has 45 canonical full cases and a 10-row deep-equal smoke subset;
- Notebook 08a is approved;
- the executable dense catalog is E5-small, Huydang DEk21 and E5-base;
- Phase 8 remains `not_ready`;
- this governance correction completes before Notebook 08b research and
  brainstorming.

It does not mention retired datasets, removed models or correction history.

`CURRENT_HANDOFF.md` records the exact governance correction, target role,
scope, Review Contract, authority and stop conditions. It does not carry
unrelated historical evidence. After the written specification and plan are
approved, it becomes an implementation handoff targeted to Implementer.

## 12. Verification and acceptance

This is a governance-only correction. Reviewer does not run backend tests,
models, Qdrant or notebooks unless the actual diff unexpectedly touches a
runtime trigger.

Required checks:

1. changed paths match the approved allowlist and protected runtime/artifact
   paths have no diff;
2. `git diff --check` passes;
3. every repository-relative pointer exists and Gemini's Superpowers root is
   stated as `~/.codex/skills/`;
4. a responsibility audit confirms one canonical owner per rule, with only
   short intentional safety/skill repetition;
5. a behavior audit confirms simplicity, useful testing, no test-double
   dependencies, root-cause debugging, real evidence, runtime/data/notebook
   rules and conditional complexity removal;
6. a state audit confirms only current 45+10, 08a, three-model catalog, Phase 8
   and next-action facts are retained;
7. manual scenarios confirm:
   - documentation-only work does not trigger runtime execution;
   - pure deterministic input is not mislabeled integration evidence;
   - integration changes select the exact real path;
   - smoke 10 and full 45 are selected according to decision risk;
   - broad suites require a real blast-radius reason;
   - unchanged correction evidence may be reused but not called fresh;
   - over-engineering creates a bounded finding/correction;
   - Implementer cannot self-approve and closure waits for user confirmation;
   - Git work requires exact authorization.

No permanent validator, checklist engine or new dependency is added.

## 13. Approved file scope

The later implementation may modify:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/Project_Status.md
session_prompt/CURRENT_HANDOFF.md
```

It may create or update the exact lifecycle spec, plan, implementation report,
Codex review and user-facing report required by the approved correction. The
implementation plan must name those paths explicitly before execution.

## 14. Lifecycle and next gate

This document does not authorize implementation. After the user approves the
written specification, Reviewer uses `writing-plans` to produce an exact
implementation plan and Review Contract. Only after the user approves that plan
may `CURRENT_HANDOFF.md` target Implementer for correction execution.

Git authorization remains `none` unless the user separately grants an exact
commit or push scope.
