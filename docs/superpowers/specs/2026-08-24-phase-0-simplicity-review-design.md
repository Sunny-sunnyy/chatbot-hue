# Phase 0 Simplicity Review Design

Date: `2026-08-24 +07`

Status: `approved by user`

## Purpose

Review the architecture contract behind Hue Foods RAG before changing Phase
1–6. The review keeps the working MVP capabilities while making simplicity,
readability, real execution and downstream impact explicit project-wide
requirements.

Phase 0 changes documentation and review policy only. It does not change
runtime code, tests, notebooks, data or Qdrant.

## Reference baseline

The project uses `llm_rag` as a readability and pipeline reference, not as a
blueprint to copy:

```text
/home/minhhieu/llm_rag
/home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md
/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md
/home/minhhieu/llm_rag/report
```

The detailed mapping is recorded in:

```text
guides/llm_rag_reference_for_hue_rag.md
```

`llm_rag` demonstrates a direct RAG pipeline that the user can read. Its JSON
chunkers, legacy modules, mock-based tests and unused sparse-vector query path
are not requirements for Hue RAG.

## Project objective

The complete Hue RAG project must:

- be easy for the user to read and trace;
- use the smallest implementation that satisfies real needs;
- avoid over-engineering and future-proofing without a current consumer;
- run with real curated data, Qdrant, local models and provider APIs;
- never use fake or mock behavior as implementation or completion evidence;
- preserve working capabilities while simplifying internals;
- pass relevant tests and real flows without conflicts with out-of-scope work.

## Architecture

The MVP data flow remains:

```text
curated foods Markdown
-> semantic Markdown chunks
-> embeddings and indexing
-> retrieval profile
-> bounded context
-> grounded answer
-> evaluation
-> benchmark
```

Offline ingestion and online query remain separate flows. Each component must
have one visible responsibility and exchange small, readable data contracts.

## Capabilities that must remain

- Curated Hue Foods Markdown is the answer-facing source.
- Chunk IDs and source metadata are stable and traceable.
- Local `intfloat/multilingual-e5-small` remains the dense baseline.
- OpenRouter remains a real future boundary for embedding benchmarks.
- Qdrant ingestion and retrieval remain available.
- `dense_only`, `hybrid_no_rerank` and `hybrid_rerank` remain runnable.
- Python BM25 remains the current lexical path.
- MiniLM remains the local reranker baseline.
- Context remains bounded and grounded in retrieved evidence.
- OpenAI Agents SDK remains the generation framework.
- OpenAI models remain current; OpenRouter/Qwen remains a future answer-model
  boundary.
- JSON API, health behavior, notebooks and the Phase 7 evaluation engine remain.

Internal classes, wrappers, validators and file layouts are not compatibility
requirements when removing them makes the same behavior easier to understand.

## Abstraction policy

Keep an abstraction only when at least two real implementations use it or a
real provider boundary needs it.

- Keep an embedding boundary for local E5 and OpenRouter candidates.
- Keep a generation boundary for OpenAI and future OpenRouter models.
- Keep one small retrieval service for the three real profiles.
- Use a concrete reranker while MiniLM is the only implementation.
- Keep shared schemas limited to data that crosses real component boundaries.
- Remove snapshots, fingerprints, validators and typed errors unless a current
  failure and distinct caller behavior justify them.
- Prefer direct functions and concrete objects over wrapper layers.

## Deferred decisions

The following decisions belong to the phase that owns the implementation:

- Phase 3–5: keep Qdrant sparse storage, remove it, or implement native sparse
  retrieval. Phase 0 does not lock the choice.
- Phase 4: any new collection or reindex. The active Hue collection remains
  read-only until the user separately approves mutation.
- Phase 3/8: exact OpenRouter embedding model and dimension.
- Phase 6/8: exact future Qwen answer model.
- Phase 8: benchmark winner across profiles and models.

The current active collection is safe to keep. Its stored sparse vectors do
not make the present hybrid runtime incorrect; the runtime must be described
truthfully as dense candidates plus Python BM25.

## Per-phase simplicity record

Each Phase 0–6 receives one living simplicity review with:

1. Before state.
2. Preserved capabilities.
3. Simplicity findings.
4. Approved changes.
5. Downstream impact.
6. Verification plan.
7. After state.
8. Before/After comparison.
9. Material bugs, root causes and resolutions.
10. Remaining limitations.
11. Reviewer conclusion.

Historical implementation, Codex and user reports remain unchanged. They are
historical evidence, not substitutes for fresh verification.

The guide holds requirements and lifecycle state. The simplicity review holds
the detailed audit trail. `Project_Status.md` holds only the current snapshot.

## Verification policy

Verification follows the actual blast radius:

```text
targeted real tests
-> canonical notebook Run All on a temporary copy
-> affected downstream flows
-> full backend suite
-> Phase 7 evaluation when RAG quality can change
```

Pure deterministic calculations may be tested without an external service;
that is not fake behavior. Claims about ingestion, retrieval, generation or
API behavior require the real dependency.

Re-run Phase 7 when a change affects chunks, answer-facing metadata,
embeddings, vector space, Qdrant payloads, retrieval, fusion, reranking,
context, prompts or generation. Do not repeat paid 104-question evaluation for
documentation-only changes or a refactor demonstrated not to change behavior.

Every phase ends with the full backend suite and `git diff --check`. Before
editing, agents inspect `git status --short` and the exact file diffs. They
preserve all out-of-scope user changes and check for merge markers.

## Dependency order and blast radius

Review one phase at a time:

```text
Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
```

Default downstream impact:

| Changed phase | Downstream phases to assess |
|---:|---|
| 1 | 2, 3, 4, 5, 6, 7 |
| 2 | 3, 4, 5, 6, 7 |
| 3 | 4, 5, 6, 7 |
| 4 | 5, 6, 7 |
| 5 | 6, 7 |
| 6 | 7 |

Assessment does not mean blindly rerunning everything. The Reviewer records
why each downstream flow needs or does not need fresh execution.

## Lifecycle

Only the phase currently being designed is reopened. Phase 1–6 remain at their
previous approved state until their own simplicity design is approved.

For Phase 1–6:

```text
previously approved
-> ready after new design approval
-> under_review after implementation handoff
-> approved after independent verification and user confirmation
```

The simplicity review preserves the previous approval and explains why the
phase was reopened. Phase 0 remains approved because this review changes only
its architecture documentation and has no Implementer runtime scope.

## User-facing acceptance

The user report for each phase answers only:

- Is the code easier to read?
- Were important capabilities preserved?
- What real data, services and models were run?
- Did the code and notebook finish without errors?
- Were conflicts and out-of-scope changes avoided?
- What limitation, if any, still matters to the user?

Technical implementation details remain in the guide, simplicity review and
implementation report for Reviewer and Implementer.

## Phase 0 completion

Phase 0 is complete when this design, its simplicity review, the canonical
guide and project snapshot agree. No runtime verification is repeated because
Phase 0 changes documentation only. The fresh pre-review baseline remains the
full backend result `222 passed` from `2026-08-24 +07`.

The next task is to inspect and brainstorm Phase 1. No Phase 1 file or runtime
change is authorized by this design.
