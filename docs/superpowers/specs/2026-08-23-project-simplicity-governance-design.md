# Project Simplicity Governance Design

**Status:** Approved by the user on 2026-08-23.

## 1. Purpose

The project governance must help coding agents build a Hue RAG system that is
clear, readable, simple, and verified through the real system. Governance must
not create technical machinery, review loops, tests, or reports that exceed a
real user need.

This change updates active governance documents. Historical implementation,
review, and user reports remain unchanged as historical evidence.

## 2. Source-of-truth hierarchy

Use this order when documents differ:

1. The user's latest confirmed instruction.
2. `session_prompt/Session_Prompt.md` for whole-project rules.
3. The workflow for the current role.
4. The canonical guide for the current phase.
5. Supporting design and implementation-plan documents.
6. Reports as evidence of completed work.
7. `session_prompt/Project_Status.md` as the current handoff snapshot.

Each phase has one canonical guide. A design or implementation plan supports
the guide but cannot silently override it. Reports record evidence and do not
create new requirements.

## 3. Documentation ownership

- `Session_Prompt.md` owns shared simplicity, real-execution, no-fake, data,
  secret, and scope rules.
- `REVIEWER_WORKFLOW.md` owns independent review, findings, the complexity
  reset, user confirmation, and reviewer handoff.
- `IMPLEMENTER_WORKFLOW.md` owns implementation, minimal testing, real
  verification, and implementer handoff.
- `guides/README.md` owns navigation, role boundaries, and the phase lifecycle.
- Each phase guide owns that phase's scope, status, and acceptance criteria.
- Technical reports contain concise observed evidence.
- User reports explain accepted results and how the user can run them again.
- `Project_Status.md` contains enough current context for a coding agent to
  continue, but no chronological audit log.
- `reports/hue_foods_rag_benchmark.md` keeps useful model information and real
  observed results without artifact-audit machinery.

General rules appear fully in `Session_Prompt.md`. Role workflows add only
role-specific behavior. Guides do not duplicate workflows, reports do not make
policy, and status does not repeat review history.

## 4. Whole-project simplicity rules

Code must be easy to read, explain, and follow. Begin with the smallest solution
that meets the demonstrated requirement. Do not add speculative abstractions,
wrappers, validators, state machines, configurability, or workflows.

Advanced techniques remain allowed only when:

1. a real observed problem exists;
2. the simple solution is insufficient;
3. the benefit is concrete and explained plainly;
4. a real-system run demonstrates the benefit; and
5. the additional complexity is proportionate.

The implementer must not preserve a technique merely because it took effort to
build. The reviewer must require removal when a technique becomes
over-engineered, is harder to understand than necessary, or lacks demonstrated
practical value.

Both roles read and apply `skills/karpathy-guidelines/SKILL.md` for code,
notebook, test, and refactor work. The skill is guidance, not a new checkpoint,
checklist, or report. The user's latest instruction, shared governance, and the
canonical phase guide take priority.

## 5. Tests and real verification

Create tests only for real behavior and important real failure cases.

- Do not target a test count or coverage percentage.
- Do not create many test files for rare technical cases.
- Every test must be readable and explain what user-needed behavior it protects.
- Before retaining an old test, answer: "What behavior does this protect that
  the user actually needs?"
- Documentation-only work or work with no changed logic may need no automated
  test.
- Do not use mocks or fakes in tests or implementation.
- Do not use fake data, providers, identifiers, artifacts, replayed output, old
  output, or expected values as evidence of a new successful run.
- A passing test does not replace a live run through the real project path.

Verification uses canonical project data and the actual backend, Qdrant,
dependencies, models, and APIs appropriate to the approved phase. Real network,
provider, quota, model, or database failures are reported honestly and are not
hidden behind fake fallback behavior.

## 6. Online services, paid APIs, and safety

Reviewer and Implementer may use online services and paid APIs within an
approved phase when the guide states the provider, model, data, and run type.
They do not need repeated consent prompts, cost caps, cost-estimation code, or
per-run approval.

New approval is required for a provider or model change, scope or dataset
expansion, deployment, active-data mutation, or destructive action. The active
Hue Qdrant collection remains read-only unless the user approves an exact
mutation target.

Secrets may be loaded into an approved process through a safe environment-file
loader. Secret values must never be opened, printed, logged, copied into a
command, stored in a notebook/report, or requested in chat.

## 7. Rejected unnecessary mechanisms

Remove mechanisms that do not directly serve a real user need:

- cost accounting and cost-estimation code;
- consent gates for already-approved API use;
- calibration;
- resume workflows;
- run identity and generation-run identity;
- timestamps used to manage evaluation packages;
- checksums;
- package matching;
- tamper detection;
- partial artifacts;
- complex artifact audits;
- layered validators; and
- technical tests that exist only to protect these mechanisms.

Do not rename or relocate a rejected mechanism to preserve it. Removal is
staged within approved work: Phase 7 removes its rejected architecture during
the simple Phase 7 implementation; older phases are reviewed individually
afterward.

## 8. Notebook policy

Every implemented Phase 1 through Phase 8 has one canonical notebook. A
documentation-only governance milestone does not require a new notebook.

- A notebook helps a person understand the system.
- Each cell does one thing.
- Short Markdown explains the next short code cell.
- Code calls clear backend functions instead of duplicating runtime logic.
- A notebook is not a validator, audit package, or test suite.
- Repository outputs remain empty and execution counts remain `null`.
- A real Run All is verified on a temporary copy when reviewing the phase.

Required style references:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

## 9. Phase lifecycle and role boundaries

The canonical lifecycle is:

```text
not_ready -> ready -> under_review -> approved
```

Exceptional states are `changes_requested` and `blocked`.

1. The user and Reviewer approve the design.
2. The Reviewer changes the canonical guide to `ready`.
3. The Implementer implements the approved scope and writes an implementation
   report.
4. The Reviewer changes the guide to `under_review`, reads the source, and
   independently runs the real path.
5. Required corrections use `changes_requested`.
6. When technical review passes, the Reviewer writes a user report whose
   Vietnamese status says it is waiting for confirmation. The guide remains
   `under_review`.
7. After the user runs the notebook and confirms the result, the Reviewer
   changes the guide to `approved` and updates the user report and project
   status.

The Implementer does not change canonical guides, Reviewer reports, user
reports, or project status. The Reviewer does not fix runtime code. Phase
confirmation does not imply permission to commit or push; Git publication
requires a separate user request.

## 10. Complexity reset after repeated review

After the fourth `changes_requested` verdict for one implementation, stop before
a fifth correction cycle. The Reviewer must re-examine:

- the phase guide;
- supporting design and plan;
- acceptance criteria;
- the sequence of prior findings; and
- whether new machinery exists only to protect machinery added in an earlier
  correction.

Separate genuine implementation defects from requirements created by an
over-engineered design. If the design, guide, plan, acceptance criteria, or
review strictness caused the loop, redesign the phase and obtain user approval
before implementation resumes.

## 11. CodeGraph

Keep the existing CodeGraph instructions, commands, and examples in both role
workflows. Change only its governance status:

- CodeGraph is an optional discovery and impact-analysis tool.
- It is not a mandatory start/end checkpoint.
- A missing or stale index is not a blocker.
- Agents may continue with `rg`, direct source reading, and real verification.
- CodeGraph output is not sufficient approval evidence.

## 12. Reports

The implementation report has six concise sections:

1. scope;
2. main changes;
3. how the real system was run;
4. observed results;
5. errors and limitations; and
6. Reviewer handoff.

The Codex review has six concise sections:

1. reviewed scope;
2. findings (`blocker`, `major`, or `minor`);
3. independent real execution;
4. observed results;
5. limitations or checks not run; and
6. decision and next action.

The user report has five simple Vietnamese sections:

1. what the user receives;
2. how the system works;
3. what Codex ran and observed;
4. how the user can run it again through the notebook; and
5. limitations and the next action.

Reports must be readable and must distinguish observed results from expected
results. They preserve real errors, skipped checks, and partial outcomes. They
do not contain formal audit checklists, cost accounting, run identity,
checksums, or package machinery.

## 13. Project status snapshot

`Project_Status.md` must contain enough information for a coding agent to
continue safely:

1. project purpose;
2. important data and components;
3. a short Phase 0-9 status table;
4. the current focus and exact unfinished work;
5. active decisions and permissions;
6. worktree and safety boundaries;
7. the next-action sequence; and
8. the small set of documents to read next.

Remove the chronological update log, historical test counts, costs, checksums,
revision-by-revision findings, and old CodeGraph status. Git and historical
reports preserve that history.

## 14. Phase order

The approved sequence is:

```text
complete governance simplification
-> implement and approve the simple Phase 7 evaluation
-> review and simplify Phase 0 through Phase 6 in dependency order
-> re-run affected Phase 7 evaluation after relevant changes
-> consider Phase 8
```

Phase 7 provides a real measurement tool before older phases are rebuilt. Phase
0 through Phase 6 are then reviewed bottom-up so foundational changes do not
invalidate higher phases that were just simplified. The repository and live
system are the primary evidence: canonical guide, relevant reports, source
code, notebook, and real runs are enough to start. External material supplied
by the user is optional when genuinely useful. If it is absent and an important
choice remains, the Reviewer brainstorms that choice with the user.

## 15. Files in scope

Rewrite concisely:

- `session_prompt/Session_Prompt.md`
- `session_prompt/REVIEWER_WORKFLOW.md`
- `session_prompt/IMPLEMENTER_WORKFLOW.md`
- `session_prompt/Project_Status.md`
- `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`
- `session_prompt/TEMPLATE_CODEX_REVIEW.md`
- `session_prompt/TEMPLATE_USER_REPORT.md`
- `guides/README.md`

Edit selectively:

- `guides/phase_0_mvp_foundation.md`
- `guides/phase_7_retrieval_answer_evaluation.md`
- `reports/hue_foods_rag_benchmark.md`

Delete after transferring all decisions:

- `session_prompt/NEXT_SESSION_SIMPLICITY_GOVERNANCE_BRAINSTORM.md`

Keep historical implementation, review, and user reports unchanged. Keep Phase
7 runtime code, data, tests, notebooks, design, and implementation plan unchanged
during this governance task. Other phase guides change only if a final scan finds
an active statement that directly enforces rejected governance.

## 16. Documentation validation

After editing:

1. read every changed document in full;
2. run `git diff --check`;
3. confirm the old absolute repository path no longer exists;
4. verify referenced paths exist;
5. ensure the Phase 7 status agrees across the guide, guide index, and project
   status;
6. ensure only the simplified lifecycle remains active;
7. ensure rejected mechanisms appear only as prohibitions or historical factual
   results, not active workflows;
8. check paid-API authorization for contradictions;
9. confirm CodeGraph remains documented but optional;
10. confirm the report templates use the approved six/six/five structure;
11. confirm project status provides complete current context without a timeline;
12. delete the temporary brainstorm reminder only after all its approved
    decisions are represented; and
13. preserve unrelated worktree changes.

No backend, model, database, or API run is needed for this documentation-only
change.
