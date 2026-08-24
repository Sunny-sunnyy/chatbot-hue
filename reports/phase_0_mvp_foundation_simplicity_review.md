# Phase 0 MVP Foundation Simplicity Review

Date: `2026-08-24 +07`

Status: `approved`

## 1. Before state

Phase 0 previously defined the complete Hue Foods RAG MVP contract. The
working system already had:

- 572 Markdown-derived chunks;
- local E5 dense embeddings with 384 dimensions;
- stored Qdrant dense and sparse vectors;
- Python BM25 and MiniLM reranking;
- three retrieval profiles;
- bounded context and grounded generation;
- OpenAI Agents SDK with `gpt-5.4-nano`;
- Phase 7 retrieval and answer evaluation.

The architecture was functional, but later phases added snapshots,
fingerprints, multiple validators, typed errors and lifecycle contracts that
made the complete system harder to read than the original `llm_rag` baseline.

Historical evidence was read from the Phase 1–7 implementation, Codex and user
reports. Current source and guides were treated as the actual Before state.
The fresh full backend baseline immediately before this review was:

```text
222 passed, 4 warnings in 260.37s
```

Phase 7 was independently verified and approved before Phase 0 was reopened.

## 2. Preserved capabilities

The review preserves:

- curated Markdown ingestion;
- stable chunks and traceable sources;
- local E5 plus future OpenRouter embedding experiments;
- Qdrant;
- all three retrieval profiles;
- Python BM25 and MiniLM baselines;
- bounded grounded generation;
- OpenAI Agents SDK with OpenAI now and OpenRouter/Qwen later;
- JSON API and health behavior;
- notebooks and the Phase 7 evaluation engine.

Internal class names, wrappers, fingerprints and validation layers are not
capabilities.

## 3. Simplicity findings

1. `llm_rag` remains a useful readability reference because its ingestion and
   query flows can be traced directly through small modules.
2. `hue_rag` correctly adapted JSON field chunking to Markdown sections and
   should not copy the JSON implementation.
3. Some abstractions are justified by real variants: embedding providers,
   answer providers and retrieval profiles.
4. MiniLM is the only reranker; an abstract reranker boundary is not required
   unless another implementation becomes real.
5. Retrieval snapshots, corpus/config fingerprints and overlapping readiness
   representations are candidates for removal during their owning phases.
6. Qdrant sparse vectors are stored but not queried. This is not a correctness
   bug; the keep/remove/native-sparse decision needs Phase 3–5 evidence.
7. Historical mock-based evidence from `llm_rag` is not acceptable completion
   evidence for `hue_rag`.

## 4. Approved Phase 0 changes

Phase 0 now defines:

- capability preservation over internal compatibility;
- abstraction only for multiple real implementations or provider boundaries;
- concrete code as the default;
- one simplicity review per phase;
- verification proportional to blast radius;
- downstream impact assessment before approval;
- one-at-a-time review from Phase 0 through Phase 6.

No runtime code, test, notebook, dataset or collection changed in Phase 0.

## 5. Downstream impact

Phase 0 changes the review standard for Phase 1–6 but does not change their
current runtime behavior.

| Future phase | Main review focus created by Phase 0 |
|---:|---|
| 1 | Small configuration, schemas, logging and shared contracts |
| 2 | Direct Markdown parsing/chunking and only real data guards |
| 3 | Real embedding provider boundary and lexical representation |
| 4 | Minimal Qdrant schema, ingestion and safe mutation boundary |
| 5 | Three readable profiles without redundant lifecycle machinery |
| 6 | Direct generation/API flow and only distinct error behavior |
| 7 | Re-run only when an upstream quality-affecting change requires it |

## 6. Verification plan

Each phase will use targeted real verification, its canonical notebook, the
affected downstream flow and the full backend suite. Phase 7 evaluation is
repeated only when the change can affect RAG quality.

Agents must check the dirty worktree, preserve out-of-scope changes, scan for
merge markers, run `git diff --check` and avoid commit/push without separate
authorization.

## 7. After state

The Phase 0 architecture now has one clear objective: preserve the working MVP
while making every phase understandable to the user. Implementation decisions
that belong to Phase 3–5 or Phase 8 are no longer prematurely locked by Phase
0.

The active Qdrant collection remains unchanged and read-only. Phase 1–6 remain
approved until the user approves a new design for the individual phase.

## 8. Before/After comparison

| Area | Before | After Phase 0 review |
|---|---|---|
| Simplicity | General preference | Project-wide acceptance requirement |
| Capability safety | Spread across guides/reports | Explicit preserved-capability list |
| Abstractions | Historical contracts tended to remain | Must have real variants or current need |
| Evidence | Extensive tests and real runs | Real runs retained; repetition follows blast radius |
| Phase history | Old reports only | One Before/After simplicity review per phase |
| Downstream effects | Checked case by case | Required impact map and recorded rationale |
| Sparse storage | Present in baseline contract | Current state retained; final choice deferred to owner phases |
| Phase status | All 0–7 approved | Only each approved redesign reopens its own phase |

## 9. Bugs and resolutions

No runtime bug was introduced or fixed because Phase 0 changed documentation
only. No merge conflict occurred in the authorized files.

## 10. Remaining limitations and decisions

- Phase 1–6 source has not yet been simplified.
- The sparse-storage decision remains open until Phase 3–5 review.
- Exact OpenRouter embedding and future Qwen answer models remain Phase 8
  benchmark inputs.
- Existing out-of-scope worktree changes remain owned by the user.

## 11. Reviewer conclusion

Phase 0 simplicity design is approved. It preserves the full MVP, introduces
no runtime regression and provides an executable review contract for Phase
1–6. Phase 1 backend skeleton and configuration is the next brainstorming
scope.
