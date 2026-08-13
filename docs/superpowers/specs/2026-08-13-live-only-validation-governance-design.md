# Live-Only Validation Governance Design

Date: 2026-08-13
Status: user-approved design, pending written-spec review

## Goal

Change repository governance so runtime, canonical notebooks, and the future
backend test suite use real dependencies and return real results. Network and
approved provider APIs are allowed. The follow-up migration of the existing
test suite is intentionally delegated to a new DeepSeek Implementer session.

## Approved Decisions

- Validation is live-only: do not use fake/mock clients, fake runners, sample
  vectors, replay fixtures, fake Qdrant clients, or opt-in real-mode guards in
  runtime, canonical notebooks, or the future backend test suite.
- `gpt-5.4-nano` is the generation and API integration-test model.
- `gpt-5.4-mini` is reserved for LLM-as-judge and explicitly identified quality
  evaluation.
- There is no API cost ceiling. A provider key, quota, network, model, or
  Qdrant failure is reported as a real failure and is not replaced by a fake
  fallback.
- Live-run logs may include the full user question, full model answer, model
  ID, latency, usage when available, and estimated cost.
- Logs must never include a credential, system prompt, raw provider payload, or
  full retrieved context.
- The active Hue collection remains read-only. Tests may create, ingest into,
  and remove only a clearly marked isolated Qdrant test collection.
- Test cleanup must report whether the isolated collection was deleted; cleanup
  failure must be reported rather than silently ignored.

## Scope Of This Session

Update these governance/snapshot files only:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/REVIEWER_WORKFLOW.md
```

Do not change runtime code, notebooks, backend tests, settings, guides, or
technical reports. Do not make any network or model call in this documentation
session.

## Governance Changes

### Shared Session Prompt

- Replace the default prohibition on live provider calls with the approved
  live-only policy.
- State the model split, permitted log fields, prohibited secret/sensitive
  fields, and isolated Qdrant collection boundary.
- Replace default-offline notebook/test language with the new policy while
  preserving the requirement not to expose credentials.

### Implementer Workflow

- Require real dependency preflight and live evidence in implementation
  reports.
- Require real Qdrant test-collection lifecycle and explicit cleanup result.
- Require no fake/mock/replay fallback in the rewritten backend test suite.
- Require run logs to include permitted operational evidence only.

### Reviewer Workflow

- Require review of provider/model identity, real-results evidence, safe logging
  boundary, active-collection protection, test-collection isolation, and
  cleanup result.
- Treat provider/network failures as actual validation failures, not occasions
  to substitute offline behavior.

### Project Status

- Record the policy decision at UTC+7.
- Replace obsolete Phase 6 snapshot statements with the existing verified live
  smoke and runtime audit evidence.
- Keep Phase 6 at `awaiting_user_confirmation`; the policy decision does not
  itself approve a phase.
- State the next action: new DeepSeek session migrates the full backend test
  suite to live-only tests under this policy.

## Future Live Test Lifecycle

```text
preflight API key/model/Qdrant
-> create or verify isolated marked Qdrant test collection
-> ingest real test documents and vectors
-> run retrieval, API, and generation through real dependencies
-> log approved operational evidence
-> record result and cost evidence
-> delete isolated test collection and report cleanup outcome
```

The active collection is never reset, reindexed, or written by this lifecycle.
Tests that previously depended on synthetic timeout, malformed output, or other
fake-only conditions must either use a real reproducible condition or be
removed with a documented coverage change; they must not be simulated.

## Session Validation

After editing the four files, run a consistency scan for contradictory
fake/mock/offline/live policy statements in the edited files, run `git diff
--check`, and confirm that no files outside the approved documentation scope
were edited in this session.

## Handoff

Once the user approves this written spec, update the four files and provide a
detailed DeepSeek prompt for the follow-up live-only backend-test migration.
No commit or push is authorized by this design alone.
