# Risk-Gated Agent Review Design

Status: approved for implementation planning
Date: 2026-08-29 +07
Scope: reusable Reviewer/Implementer coordination and context optimization

## 1. Problem

The project uses Codex as an independent Reviewer and Gemini as Implementer.
Codex is the scarce resource: a small number of long review turns can consume a
large share of the ChatGPT five-hour usage allowance, while Gemini can perform
implementation and deterministic verification more freely.

The current workflow makes every Reviewer session reload a large project
history, multiple overlapping governance files, phase documents and reports.
It also asks Reviewer to repeat much of the Implementer's inspection and live
verification even when a correction does not affect runtime behavior. This is
safe but inefficient. It spends Reviewer context on discovery and repetition
instead of decisions, architecture, specification and high-risk verification.

The new workflow must reduce that cost without allowing Implementer to
self-approve or replacing independent review with trust in a narrative report.

## 2. Goals

1. Reserve Reviewer capacity for brainstorming, requirements, architecture,
   specifications, plans, risk decisions and final independent review.
2. Let Implementer complete implementation, self-review, corrections,
   verification and detailed evidence preparation inside approved scope.
3. Give every new session a small, reliable and version-controlled entrypoint.
4. Select Reviewer verification according to observed risk and blast radius.
5. Preserve an independent minimum diff review for every implementation.
6. Make correction reviews incremental rather than restarting from the full
   project history.
7. Delegate mechanical closure and Git operations when explicitly authorized.
8. Keep the skill generic enough to reuse in other projects.

## 3. Non-goals

This work does not:

- redefine coding, testing, debugging or simplicity principles;
- replace project-specific governance or safety boundaries;
- allow Implementer to approve its own work or lower a risk classification;
- build a risk engine, parser, linter, CI system or agent orchestrator;
- require multi-agent delegation;
- modify Hue RAG runtime code, tests, notebooks or benchmark artifacts;
- remove detailed implementation reports;
- impose a hard word limit that can omit necessary context.

Coding and verification practices remain owned by the project's existing
session instructions, role workflows and `practical-project-coding` skill.

## 4. Selected approach

Use a lean risk-gated operating model with:

- one reusable shared skill, `risk-gated-agent-review`;
- one active, version-controlled `CURRENT_HANDOFF.md`;
- four compact bootstrap files per session;
- a Review Contract fixed during specification and planning;
- detailed evidence produced by Implementer and selectively consumed by
  Reviewer;
- a minimum independent diff gate for all reviews;
- additional Reviewer execution only when a declared or observed risk trigger
  requires it;
- delta correction review and delegated approval closure.

This approach is preferred over adding only a handoff file because the existing
bootstrap documents themselves contain substantial duplication and history. It
is preferred over automated governance because the latter would introduce code,
schema maintenance and new mechanisms before a demonstrated need exists.

## 5. Components

### 5.1 Shared skill

Create:

```text
skills/risk-gated-agent-review/SKILL.md
```

The skill defines only the generic coordination contract. It has two branches:

- **Reviewer consumer:** design, Review Contract, independent diff gate,
  risk-triggered verification, findings and closure contract;
- **Implementer producer:** in-scope execution, self-review, detailed evidence,
  compact handoff, deviation escalation and authorized closure/Git work.

Project-specific paths, models, services, phase names and permissions remain in
the project workflows, canonical documents and current handoff. The skill must
not copy the coding rules from `practical-project-coding`.

### 5.2 Bootstrap documents

Every new session starts with exactly these four documents:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/<ROLE>_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

The first three are relatively stable. The handoff is dynamic and appears last
in the prompt. Other documents are loaded only through the handoff's context map
or because a risk trigger makes them necessary.

### 5.3 Session Prompt

`Session_Prompt.md` keeps stable, cross-project-session invariants:

- source-of-truth order;
- role routing and permission boundaries;
- data and destructive-action safety;
- tiered context-loading rule;
- pointers to the shared review skill and coding skill;
- repository-wide conventions that truly apply to most tasks.

It does not contain phase timelines, completed correction histories or repeated
details from role workflows and canonical guides.

### 5.4 Project Status

`Project_Status.md` acts as both project README and current snapshot because the
repository has no separate README. It contains:

- the problem and intended product;
- system and data-flow map;
- current runtime, data and important infrastructure;
- a compact phase-status table;
- decisions and safety boundaries currently in force;
- a canonical document map;
- one current next action.

It is not an audit log. Detailed history remains available through Git and the
canonical guide, spec, plan and report files.

### 5.5 Role workflows

`REVIEWER_WORKFLOW.md` contains only Reviewer authority, the two gates, minimum
diff review, risk verification, severity/verdict rules and role-specific
deliverables. It points to the shared skill and does not repeat general coding
or test philosophy.

`IMPLEMENTER_WORKFLOW.md` contains only Implementer authority, self-completion
inside approved scope, evidence production, escalation conditions, technical
documentation ownership, closure and gated Git permissions. It also points to
the shared skill instead of duplicating its protocol.

### 5.6 Current handoff

Create one active file:

```text
session_prompt/CURRENT_HANDOFF.md
```

Handoffs are categorized by their target role rather than kept in separate
Reviewer and Implementer files. Replacing the file makes the next action
unambiguous; Git preserves prior handoffs.

Required metadata:

```text
Target role:
Authored by:
Handoff kind:
State: active
Base commit:
Head commit: `HEAD`, an external commit SHA, or `worktree`
Risk level:
Git authorization:
```

Required content:

1. objective and terminal state;
2. latest user decisions that supersede older material;
3. canonical input pointers, including exact sections when practical;
4. in-scope and out-of-scope work;
5. safety and permission boundaries;
6. Review Contract;
7. acceptance-to-evidence mapping;
8. changed or expected files;
9. evidence index with commands, observed results and artifact paths;
10. deviations, failures and unverified items;
11. exact next action and stop conditions.

The content is adapted to the handoff kind; irrelevant sections remain short or
explicitly `not applicable`, not filled with boilerplate.

## 6. Lifecycle

### 6.1 Design gate

Reviewer and user brainstorm the next bounded task. Reviewer writes the approved
specification, implementation plan and Review Contract. Reviewer then replaces
the current handoff with an `implementation` handoff targeted to Implementer.

### 6.2 Implementation interval

Implementer may implement, test, run the live path, self-review and correct all
issues inside the approved contract without asking Reviewer for intermediate
approval. Implementer stops only for a real blocker or a required change to
requirements, architecture, provider/model, data contract, risk boundary or
authority.

When ready, Implementer writes a detailed implementation report and replaces the
handoff with a compact `final_review` evidence packet targeted to Reviewer. A
checkpoint commit/push is allowed only when the handoff or latest user decision
contains matching Git authorization. A checkpoint never means approval.

### 6.3 Final review gate

Reviewer loads the four bootstrap documents, the Review Contract and exact
base-to-head diff. Reviewer performs the minimum independent gate, then expands
source reads and execution only for applicable risk triggers, deviations or
contradictory evidence.

If review succeeds, Reviewer records `ready_for_user_confirmation` and creates
an Approval Closure Contract. If review finds a blocker or major issue, Reviewer
creates a `correction` handoff with an exact delta instead of restarting the
whole implementation lifecycle.

### 6.4 Correction

Implementer fixes all findings in one batch, reruns affected verification and
returns a new final-review handoff. Reviewer reads the correction diff and only
rechecks affected behavior. Evidence may be reused when the handoff demonstrates
that the correction did not change its inputs, dependency, environment or data
flow.

### 6.5 Closure

Reviewer alone makes the technical decision and writes the Approval Closure
Contract. After the user confirms, Implementer may mechanically update the exact
status and documentation fields named by that contract, run documentation
checks and perform authorized Git operations. Implementer stops if the user's
confirmation adds a new requirement or repository state no longer matches the
contract.

After closure, `CURRENT_HANDOFF.md` describes the next real task. For Hue RAG's
initial rollout, it targets a Reviewer session for Phase 8 Notebook 08b
research and brainstorming.

## 7. Handoff state machine

Supported handoff kinds:

| Kind | Author → target | Purpose |
|---|---|---|
| `next_design` | Reviewer/Implementer → Reviewer | Start the next research or design task |
| `implementation` | Reviewer → Implementer | Execute an approved spec and plan |
| `final_review` | Implementer → Reviewer | Review implementation and evidence |
| `correction` | Reviewer → Implementer | Fix an exact blocker/major delta |
| `closure` | Reviewer → Implementer | Apply approved mechanical state changes |

Only one handoff is active. An agent must stop and report a handoff problem when:

- the target role does not match the assigned role;
- the base commit is invalid, or the head is neither `HEAD`, a valid external
  commit nor `worktree`, or the declared range does not match the diff;
- canonical inputs do not exist;
- current requirements conflict with the latest user decision;
- the worktree contains undeclared changes that cannot be isolated safely;
- implementation deviates beyond approved authority;
- requested Git work lacks authorization;
- claimed PASS evidence is unsupported or contradictory.

## 8. Tiered context loading

```text
Tier 0: four bootstrap documents
Tier 1: Review Contract and exact base/head diff
Tier 2: changed source, focused tests and linked evidence required by risk
Tier 3: live systems, external research or broad verification when necessary
```

Agents must not load all reports or project history merely for reassurance.
They may expand context whenever a decision, inconsistency, safety boundary or
risk trigger requires it. Missing important context is a correctness failure;
the objective is relevance, not minimal word count at any cost.

The four bootstrap files have a soft combined target of about 4,000 words, and
the current handoff has a soft target of about 800 words. These are diagnostic
targets, not validity gates. Necessary excess is allowed with a short reason.

## 9. Review Contract

Every implementation plan contains a short Review Contract fixed by Reviewer:

- risk level: `low`, `medium` or `high`;
- expected risk triggers;
- required Implementer evidence;
- minimum Reviewer checks;
- independent reruns required from Reviewer;
- evidence eligible for reuse during correction;
- actions requiring new user authority;
- approval closure fields.

Implementer reports deviations and may recommend raising risk, but cannot lower
the contract. Reviewer may raise risk when actual changes differ from the plan.

### 9.1 Risk levels

- **Low:** documentation, status, handoff, notebook cleanup, formatting or other
  changes that do not open behavior.
- **Medium:** contained implementation, dependency cleanup, behavior-preserving
  refactor, non-active data/collection or internal contract.
- **High:** production configuration or public API, active data, migration or
  destructive action, security/secrets, provider or paid API, model encoding,
  retrieval/reranking/scoring, evaluation metrics or quality decisions.

The trigger is more important than the label. A task may have several triggers,
and observed deviations can elevate its review.

## 10. Independent review gates

### 10.1 Minimum gate for every review

Reviewer independently:

1. validates target role and base/head commits;
2. checks worktree and the complete changed-file list, including untracked
   files;
3. reads the exact diff;
4. maps changes to acceptance criteria;
5. detects out-of-scope work and deviations;
6. runs `git diff --check`;
7. identifies missing or contradictory evidence.

### 10.2 Triggered verification

| Trigger | Additional Reviewer work |
|---|---|
| Documentation only | Check consistency, links and lifecycle state; no test by default |
| Functional code | Read the changed functional path and run the smallest useful deterministic check |
| Dependency/provider | Check lock/resolution, consumers and authoritative contract when needed |
| Database/integration | Run the exact safe live path affected |
| Model/retrieval/scoring | Rerun only the changed model, path or metric |
| Quality/evaluation | Use canonical data and rerun the affected evaluation slice |
| Active data/migration | Verify authorization, exact target and before/after state |
| Security/public API | Verify the affected boundary and observable behavior |
| Deviation/contradiction | Expand review to the sources needed to resolve it |

Reviewer does not spawn sub-agents by default. Sub-agents require a high-value,
independently partitionable audit and explicit authorization in the Review
Contract or from the user.

## 11. Role ownership

### 11.1 Reviewer

Reviewer owns requirements, architecture, spec, plan, Review Contract, review
findings, technical verdict, user-facing decision and closure contract. Reviewer
does not implement runtime changes for Implementer.

### 11.2 Implementer

Within approved scope, Implementer owns code, tests, notebooks, dependencies,
implementation report, technical documentation, self-review and evidence.
Implementer may update the current handoff for the next role.

Project-specific governance decides exact protected files. For Hue RAG,
Implementer does not independently change approved requirements/specs/plans,
risk level, canonical guide/status, Codex review, user report or stable
governance. A closure contract may authorize exact mechanical changes without
transferring decision ownership.

## 12. Evidence contract

Implementer evidence has two layers.

The detailed implementation report may include complete data flow, commands,
outputs, artifacts, failures, limitations and self-review history. It should be
as detailed as necessary for audit and debugging.

The current handoff is an index, not a second long report. It contains concise
acceptance mapping, results, changed files, risks, deviations and pointers.
Reviewer opens detailed evidence selectively. Efficiency comes from selective
consumption, not weaker evidence production.

No expected value, old output or unsupported claim is presented as an observed
PASS. Correction evidence is reused only under the conditions in the Review
Contract.

## 13. Git authorization

The handoff declares exactly one value:

```text
git_authorization: none
git_authorization: commit
git_authorization: commit_and_push
```

Authorization includes exact scope and purpose. It does not broaden content
ownership. Implementer may perform Git operations for its implementation or for
already-written Reviewer closure edits, but may not silently add content changes.

## 14. Validation

The initial implementation is validated without creating automation machinery.

### 14.1 Tabletop scenarios

1. **08b next design:** a new Reviewer identifies research/brainstorming as the
   only next action from the four bootstrap files and does not implement or run
   08b.
2. **08a replay:** catalog/dependency cleanup selects diff review, focused tests,
   lock verification and safe Qdrant inspection without rerunning unchanged
   embedding models.
3. **Correction:** a major finding produces one bounded correction handoff and
   the next review consumes only the affected delta.
4. **Closure:** after user confirmation, Implementer applies exact status/docs
   updates and authorized Git work without making an approval decision.

### 14.2 Success criteria

- The bootstrap bundle identifies project, role, task and next action without
  chat history.
- Soft context targets are met or justified without losing material context.
- Every rule has one canonical home; other files link instead of copying it.
- Reviewer always performs an independent diff gate.
- Risky behavior receives exact independent verification.
- Low-risk work does not trigger broad source reads or duplicate live runs.
- Detailed Implementer evidence remains available without being mandatory
  context.
- Only one current handoff and one next action exist.
- The skill contains no duplicated coding/testing doctrine.
- No validator, linter, CI or orchestration code is added.

The tabletop records the old and new bootstrap word counts and lists which
documents and commands the Reviewer avoids in each scenario. The counts measure
directional improvement; they are not hard acceptance thresholds.

## 15. Rollout scope

Create:

```text
skills/risk-gated-agent-review/SKILL.md
session_prompt/CURRENT_HANDOFF.md
reports/risk_gated_agent_review_implementation_report.md
```

Refactor only as needed:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
```

Do not modify:

```text
skills/practical-project-coding/SKILL.md
runtime code
tests
notebooks
Phase 8 benchmark artifacts
```

During rollout, Implementer first creates a `final_review` handoff so Reviewer
can verify the workflow implementation. The Approval Closure Contract then
replaces it with the first steady-state handoff: a `next_design` handoff that
asks Reviewer to research and brainstorm Phase 8 Notebook 08b. The 08b handoff
does not authorize implementation, benchmark execution, paid API use, active
collection mutation or production cutover.

## 16. Research basis

The design follows three relevant findings:

- OpenAI reports that leaner system prompts reduced tokens substantially in
  internal coding-agent evaluations and recommends stating instructions once.
- OpenAI's harness guidance recommends giving agents a navigable map rather
  than a large monolithic manual and preserving stable prompt prefixes.
- Anthropic reports that multi-agent research can consume far more tokens than
  ordinary chat, so delegation is not a default quota-saving mechanism.

References:

- https://developers.openai.com/api/docs/guides/latest-model
- https://openai.com/index/harness-engineering/
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://www.anthropic.com/engineering/multi-agent-research-system
- https://arxiv.org/abs/2402.02172

## 17. Implementation planning gate

This approved design authorizes writing a detailed implementation plan only
after the user reviews the committed specification. It does not yet authorize
creation of the skill, handoff or workflow refactor.
