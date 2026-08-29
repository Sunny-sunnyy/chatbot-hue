---
name: risk-gated-agent-review
description: Use when a Reviewer and Implementer collaborate through specification, implementation evidence, independent risk-gated review, correction, approval closure, or cross-session handoff.
---

# Risk-Gated Agent Review

## Purpose

Reserve Reviewer attention for requirements, decisions and independent checks
whose risk justifies them. Give Implementer responsibility for complete
in-scope execution, self-review and detailed evidence. Use one compact handoff
to carry only the context the next role needs.

This skill coordinates roles and context. It does not define how to write,
test, debug or structure implementation. Follow the project's governance and
applicable implementation skills for those practices.

## Start from the current task

Read the project-defined bootstrap documents in this order:

1. stable session instructions;
2. current project map/status;
3. the workflow for the assigned role;
4. the single current handoff.

Validate `Target role` before doing task work. Stop if it does not match the
assigned role or if the handoff does not identify one next action.

Load context progressively:

```text
Tier 0: bootstrap documents
Tier 1: Review Contract and exact base/head diff
Tier 2: affected source, focused checks and linked evidence selected by risk
Tier 3: live systems, external research or broad verification when necessary
```

Do not load project history or every report for reassurance. Expand context
when a decision, inconsistency, safety boundary or risk trigger requires it.
Soft context budgets never justify omitting a requirement or safety boundary.

## Select the role branch

- Use the **Reviewer branch** for brainstorming, specification, planning,
  findings, independent verification, verdicts and approval closure.
- Use the **Implementer branch** for approved execution, self-review,
  corrections, evidence production and authorized mechanical closure.
- If the assigned role is unclear and the difference changes permissions, ask
  one question and stop.

## Reviewer branch

### Design gate

Before implementation, work with the user to settle important requirements and
trade-offs. Produce the approved specification and plan. Put a short Review
Contract in the plan containing:

- risk level and expected triggers;
- evidence Implementer must produce;
- minimum independent Reviewer checks;
- exact Reviewer reruns;
- correction evidence eligible for reuse;
- actions needing new authority;
- the intended approval closure.

Reviewer owns this contract. Implementer may report a higher observed risk but
cannot lower it.

### Final review gate

For every implementation, independently:

1. validate target role and base/head state;
2. inspect worktree state and every changed path, including untracked files;
3. read the exact diff;
4. map the diff to acceptance criteria;
5. identify out-of-scope changes and deviations;
6. run the repository's diff-format check;
7. identify missing or contradictory evidence.

Then perform only the additional reads and executions required by the Review
Contract or observed risk. An Implementer report is a claim and evidence index,
not automatic proof. Independence comes from the diff gate and targeted
verification, not from repeating every deterministic command.

### Risk-triggered verification

| Trigger | Additional Reviewer work |
|---|---|
| Documentation only | Check consistency, links and lifecycle state |
| Functional behavior | Read the changed path and run the smallest useful deterministic check |
| Dependency/provider | Check resolution, consumers and authoritative contract when needed |
| Database/integration | Run the exact safe live path affected |
| Model/retrieval/scoring | Rerun only the changed model, path or metric |
| Quality/evaluation | Use canonical data and rerun the affected evaluation slice |
| Active data/migration | Verify authority, exact target and before/after state |
| Security/public interface | Verify the affected boundary and observable behavior |
| Deviation/contradiction | Expand review to the sources needed to resolve it |

Use project severity and verdict definitions. Reviewer does not modify runtime
for Implementer or silently broaden the task.

### Correction and closure

For a blocking finding, replace the handoff with one exact correction delta:

- severity and affected requirement;
- affected paths;
- correction acceptance criteria;
- verification to rerun;
- evidence safe to reuse;
- boundaries that must remain unchanged.

After technical readiness, write an Approval Closure Contract. It identifies
the user confirmation required, exact state/document edits, checks, Git
authorization and next handoff. Reviewer makes the decision; Implementer may
perform only the mechanical closure.

Do not dispatch sub-agents by default. Use them only for a high-value audit that
splits into genuinely independent workstreams and has explicit authorization.

## Implementer branch

### Complete the approved scope

Implement the full approved plan, run its checks, review the exact diff and fix
all in-scope issues before handoff. Do not request intermediate Reviewer input
for ordinary corrections inside the contract.

Stop and escalate when progress requires changing a requirement, architecture,
provider/model, data contract, safety boundary, risk level or permission, or
when a real blocker prevents reliable evidence.

Implementer cannot self-approve, lower risk or reinterpret an Approval Closure
Contract.

### Produce evidence in two layers

Keep the detailed implementation report as complete as needed: changes,
commands, observed results, artifacts, failures, limitations and self-review
corrections.

Keep the current handoff compact. Include:

- acceptance-to-evidence mapping;
- changed paths;
- command/result summary;
- risk and deviation flags;
- artifact/report pointers;
- failed, skipped and unverified work;
- exact Reviewer reruns from the Review Contract.

Do not present an expected value, old result or unsupported assertion as a new
observed pass.

### Corrections and closure

Fix one correction handoff as one batch. Rerun affected checks and identify
which prior evidence remains valid and why. Return the delta to Reviewer; do
not close the finding yourself.

After user confirmation, execute an Approval Closure Contract exactly. Stop if
the user adds a requirement or repository state no longer matches the contract.

## Current handoff contract

Use one active, version-controlled handoff. Its metadata includes:

```text
Target role:
Authored by:
Handoff kind:
State: active
Base commit:
Head commit:
Risk level:
Git authorization:
```

`Head commit` may be `HEAD`, an external commit SHA or `worktree`. Resolve
`HEAD` to a SHA when review begins. Supported handoff kinds are:

- `next_design`;
- `implementation`;
- `final_review`;
- `correction`;
- `closure`.

The body contains objective, latest overriding decisions, canonical pointers,
scope, boundaries, Review Contract, acceptance mapping, changed/expected paths,
evidence, deviations, next action and stop conditions. Keep irrelevant sections
brief rather than filling them with boilerplate.

Stop when commits are invalid, the declared diff does not match, inputs are
missing, requirements conflict, undeclared changes cannot be isolated, claimed
evidence is unsupported or requested authority is absent.

## Evidence reuse

Reuse evidence during a correction only when it passed in the same
implementation series and the delta did not change its inputs, dependencies,
environment or data flow. State that reasoning in the handoff. Never relabel
old evidence as a fresh run for changed behavior.

## Git authorization

The handoff declares one value:

```text
git_authorization: none
git_authorization: commit
git_authorization: commit_and_push
```

Authorization must identify exact scope and purpose. It permits the Git
operation, not additional content changes. A checkpoint commit is a review
target, not an approval.

## Completion

Finish with one unambiguous next role and next action. Detailed history remains
in version control and canonical artifacts; do not copy it into the active
handoff.
