# Hue Foods RAG Benchmark Log

Last updated: `2026-08-08 22:35 +07`

## Purpose

This file records manual benchmark runs for the Hue Foods RAG MVP.

Use this log when comparing:

- embedding models;
- retrieval profiles;
- reranking on/off;
- dense-only vs hybrid retrieval;
- answer generation and judge quality.

Detailed per-question outputs should be stored as JSONL under:

```text
backend/evaluation/results/
```

This Markdown file stores summaries and decisions only.

## Safety rules

Before changing embedding model or vector size:

1. Edit `backend/config/settings.yaml`.
2. Set `vector_database.reset_collection: true`.
3. Re-run ingestion.
4. Re-run evaluation.
5. Record results here.

After selecting the final model/profile:

1. Keep the active Qdrant collection.
2. Set `vector_database.reset_collection: false`.
3. Use the current collection for API/runtime.

Do not record secrets or API keys in this file.

## Active benchmark command sequence

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m ingestion.pipeline
UV_CACHE_DIR=/tmp/uv-cache uv run python -m evaluation.run_retrieval
UV_CACHE_DIR=/tmp/uv-cache uv run python -m evaluation.run_answers
```

## Profiles

| Profile | Dense retrieval | BM25 hybrid score | CrossEncoder rerank | Purpose |
|---|---:|---:|---:|---|
| `dense_only` | yes | no | no | Baseline semantic retrieval |
| `hybrid_no_rerank` | yes | yes | no | Test keyword-sensitive retrieval |
| `hybrid_rerank` | yes | yes | yes | Highest-quality MVP profile |

## Candidate embedding models

Record candidate models here before running benchmark.

| Model | Vector size | Notes |
|---|---:|---|
| `intfloat/multilingual-e5-small` | 384 | Initial baseline from `llm_rag` |

## Benchmark results

No benchmark run has been recorded yet.

| Run ID | Date +07 | Profile | Embedding model | Vector size | Reset collection | Chunk count | Retrieval MRR | Retrieval nDCG | Keyword coverage | Answer accuracy | Answer completeness | Answer relevance | Retrieval JSONL | Answer JSONL | Decision |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|

## Run notes

Use one section per benchmark run.

### Run template

```text
Run ID:
Date +07:
Profile:
Embedding model:
Vector size:
Config changes:
Collection reset:
Chunk count:
Retrieval result file:
Answer result file:
Metrics:
Observations:
Decision:
Next action:
```

## Final selection

Record the final selected profile and embedding model here after benchmark comparison.

```text
Selected profile:
Selected embedding model:
Selected vector size:
Reason:
Collection status:
reset_collection after selection:
```
