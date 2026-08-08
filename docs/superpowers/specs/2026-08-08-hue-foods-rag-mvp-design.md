# Hue Foods RAG MVP Design

Last updated: `2026-08-08 22:35 +07`

## Purpose

This document defines the design for the first production-oriented RAG MVP for `hue_rag`.

The MVP focuses only on the curated Hue food knowledge base and combines two existing learning references:

- `llm_rag`: modular backend RAG with Qdrant, dense embedding, BM25 hybrid retrieval, reranking, bounded context, FastAPI, and evaluation-ready runtime structure.
- `hue_rag/rag_old`: notebooks, evaluation discipline, test categories, MRR/nDCG/keyword coverage, answer judge, and later Agentic RAG ideas.

The implementation must happen in phases. A phase must pass its validation gate before the next phase starts, unless the user explicitly overrides the gate.

## Scope

MVP scope:

- Runtime Python modules under `backend/`.
- Learning and inspection notebooks under `notebooks/`.
- Config-driven retrieval profiles.
- One active Qdrant collection at a time.
- Food-only indexing from curated Markdown.
- Evaluation for retrieval and answer quality.
- JSON non-streaming backend API.
- Configurable local SentenceTransformer embedding models.
- OpenAI/Agents SDK for answer generation and LLM-as-judge.
- Documentation for benchmark checkpoints and experiment results.

Out of MVP scope:

- Frontend or Gradio UI.
- SSE streaming.
- Agentic RAG implementation.
- OpenRouter provider implementation.
- Qdrant sparse-vector query fusion.
- Multiple Qdrant collections kept in parallel for benchmark.
- OpenAI embeddings.
- Web enrichment or new data curation.

## Primary decisions

### Data source

The MVP indexes only curated food Markdown:

```text
knowledge-base-hue/foods/**/*.md
knowledge-base-hue/foods/food-guides.md
```

The ingestion pipeline must exclude:

```text
knowledge-base-hue/foods/evaluation/
knowledge-base-hue/_source-dumps/
knowledge-base-hue/meta/
```

The pipeline must not chunk source dumps or uncurated raw data.

### Runtime layout

Runtime modules live under `backend/`, and commands run from that directory.

Required command style:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m ingestion.pipeline
```

Imports should follow the `llm_rag` style:

```python
from core.settings_loader import load_settings
from retrieval.context_builder import ContextBuilder
```

### Notebook layout

Learning notebooks live under `notebooks/`. They must import backend modules rather than duplicating runtime logic.

Initial notebook set:

```text
notebooks/
  01_foods_data_and_chunking.ipynb
  02_embedding_models.ipynb
  03_qdrant_ingestion.ipynb
  04_retrieval_profiles.ipynb
  05_generation_and_api.ipynb
  06_evaluation.ipynb
```

Notebook goals:

- inspect inputs and outputs of each stage;
- run the same code used by runtime modules;
- show intermediate chunks, vectors, retrieved documents, context, answers, and evaluation results;
- support learning without becoming a second implementation.

### Config profiles

The MVP compares retrieval variants through config profiles in `backend/config/settings.yaml`.

The active profile is selected by editing:

```yaml
active_profile: dense_only
```

MVP profiles:

| Profile | Index schema | Retrieval | Reranking |
|---|---|---|---|
| `dense_only` | dense + sparse stored | dense vector search only | disabled |
| `hybrid_no_rerank` | dense + sparse stored | dense candidates + BM25 Python score fusion | disabled |
| `hybrid_rerank` | dense + sparse stored | dense candidates + BM25 Python score fusion | enabled |

All profiles use one shared code path. The profile changes behavior through config, not through duplicate scripts.

### Embedding benchmark strategy

The MVP uses local SentenceTransformer models only.

Embedding settings are configurable:

```yaml
embedding:
  model: intfloat/multilingual-e5-small
  vector_size: 384
  device: cpu
  batch_size: 64
```

The user will benchmark multiple Vietnamese or multilingual embedding models. Each benchmark run uses one active Qdrant collection:

1. Set embedding model and vector size in `settings.yaml`.
2. Set `vector_database.reset_collection: true`.
3. Run ingestion.
4. Run evaluation.
5. Record results in the benchmark log.
6. Change model and repeat.

After selecting the best model:

1. Keep the current collection.
2. Set `vector_database.reset_collection: false`.
3. Use that collection for backend/API runtime.

The MVP intentionally does not keep one collection per model because collection creation is fast enough and benchmark results are recorded in Markdown and JSONL outputs.

### Qdrant collection behavior

`backend/config/settings.yaml` must include:

```yaml
vector_database:
  collection_name: hue_foods_rag
  reset_collection: true
  vector_size: 384
  distance: cosine
```

Behavior:

- If `reset_collection: true`, ingestion recreates the active collection before upsert.
- If `reset_collection: false`, ingestion must not delete the existing collection.
- The docs and benchmark log must warn that changing embedding model or vector size requires reset/reindex.

### Chunking strategy

MVP chunking uses Semantic Markdown section chunking.

Rules:

- Parse each curated Markdown file.
- Use `#` as document/entity title.
- Use `##` headings as semantic sections.
- Prefer section-level chunks first.
- Split long section content into smaller paragraph chunks only when necessary.
- Preserve table rows as retrievable text when useful.
- Do not use LLM during ingestion.
- Do not create data that is not present in the Markdown.

Required metadata per chunk:

```text
chunk_id
source
title
section
category
subcategory
chunk_type
```

Metadata examples:

```text
source: foods/restaurants/bun bo hanh.md
title: Bún bò Hạnh
section: Món ăn / trải nghiệm
category: foods
subcategory: restaurants
chunk_type: section
```

No absolute filesystem path should be stored in chunk metadata.

Before implementation of chunking, the implementer must run a mini research/brainstorming pass over representative foods files to confirm edge cases:

- restaurant files;
- cafe files;
- local specialty files;
- `food-guides.md`;
- tables;
- image Markdown;
- missing optional sections.

### Dense and sparse representation

All profiles store dense vectors. The MVP also stores sparse vectors in Qdrant points to keep the index ready for future Qdrant sparse experiments.

The current hybrid retrieval path still uses BM25 in Python, not Qdrant sparse query fusion.

Sparse implementation:

- Tokenize text locally.
- Fit sparse embedder on all chunk texts during ingestion.
- Store sparse vector as `indices` and `values` in Qdrant.
- Fit BM25 from the same corpus during startup/evaluation.

### Retrieval profiles

#### `dense_only`

Flow:

```text
query
  -> dense embedding
  -> Qdrant dense search
  -> RetrievedDocument list
  -> ContextBuilder
```

No BM25 score is used for ranking. No reranker is used.

#### `hybrid_no_rerank`

Flow:

```text
query
  -> dense embedding
  -> Qdrant dense search with candidate_multiplier
  -> BM25 score for each candidate
  -> hybrid score
  -> top_k documents
  -> ContextBuilder
```

Score formula:

```text
hybrid_score = dense_weight * dense_score + bm25_weight * bm25_score
```

The exact weights are config values.

#### `hybrid_rerank`

Flow:

```text
query
  -> dense embedding
  -> Qdrant dense candidates
  -> BM25 score
  -> hybrid score
  -> CrossEncoder rerank
  -> top reranked documents
  -> ContextBuilder
```

Reranking must be optional through config. If disabled or unavailable, runtime must fall back to ranked retrieval output rather than fail the whole request, except where a phase explicitly tests reranking.

### ContextBuilder

The context builder must:

- accept retrieved documents;
- keep at most `max_documents`;
- skip empty text;
- enforce `max_context_length`;
- join chunks with a clear separator;
- return the final context string and enough debug information for notebooks/evaluation.

### LLM generation

MVP generation uses OpenAI directly through the OpenAI/Agents SDK.

OpenAI model IDs must be config-driven:

```yaml
llm:
  provider: openai
  answer_model: gpt-5-nano
  temperature: 0.2
  max_output_tokens: 1024
```

The user mentioned models such as `gpt 5.4 nano` and `gpt 5.4 mini`. Before implementation or execution, exact model IDs must be verified against official OpenAI documentation or the OpenAI models endpoint. Current official OpenAI model documentation should be treated as the source of truth:

- https://developers.openai.com/api/docs/models
- https://platform.openai.com/docs/quickstart/make-your-first-api-request

Prompt style:

- Vietnamese grounded travel assistant.
- Helpful for Hue food, culture, and travel questions.
- Use only retrieved context.
- Do not invent prices, hours, addresses, origin stories, or marketing claims.
- If the context is insufficient, state that the answer is not found in the current data.
- For recommendation or itinerary questions, only recommend from retrieved context.

### API contract

MVP backend API only. No frontend and no SSE in MVP.

Endpoints:

```text
GET /health
POST /api/chat
```

`POST /api/chat` request:

```json
{
  "query": "Lần đầu đến Huế nên ăn gì?",
  "session_id": "optional-session-id"
}
```

`POST /api/chat` response:

```json
{
  "answer": "Câu trả lời tiếng Việt dựa trên context.",
  "sources": [
    {
      "text": "Chunk text rút gọn...",
      "metadata": {
        "source": "foods/food-guides.md",
        "title": "Food Guides Huế",
        "section": "Lần đầu đến Huế nên thử gì?",
        "category": "foods",
        "subcategory": "guide",
        "chunk_type": "section"
      },
      "score": 0.82
    }
  ],
  "session_id": "uuid-or-provided-session",
  "retrieval_debug": {
    "profile": "hybrid_rerank",
    "embedding_model": "intfloat/multilingual-e5-small",
    "top_k": 10,
    "reranking_enabled": true
  }
}
```

The response should expose retrieval debug data for learning. It must not expose secrets.

### Evaluation

The MVP must support both retrieval and answer evaluation using:

```text
knowledge-base-hue/foods/evaluation/tests.jsonl
```

Retrieval metrics:

- MRR
- nDCG
- keyword coverage

Answer judge metrics:

- accuracy
- completeness
- relevance
- feedback

Evaluation model is separate from answer model:

```yaml
evaluation:
  judge_model: gpt-5-mini
```

Evaluation outputs:

```text
backend/evaluation/results/retrieval_<timestamp>.jsonl
backend/evaluation/results/answers_<timestamp>.jsonl
```

Each JSONL row should include:

- question;
- category;
- keywords;
- reference answer;
- retrieved documents and scores;
- generated answer for answer evaluation;
- judge feedback and scores;
- config snapshot without secrets.

The benchmark Markdown log stores summary rows only. Detailed rows live in JSONL.

### Benchmark log

The MVP includes a Markdown benchmark/checkpoint log:

```text
docs/superpowers/plans/2026-08-08-hue-foods-rag-benchmark-log.md
```

The log records:

- active profile;
- embedding model;
- vector size;
- reset/reindex status;
- retrieval metrics;
- answer judge metrics;
- result JSONL file paths;
- notes and next decision.

The log is the human-readable place to compare model/profile choices.

### Validation gates

Each implementation phase must include:

- import checks;
- focused unit tests for core logic;
- smoke checks for the current stage;
- evaluation checkpoint once retrieval/evaluation exists.

The project should not move to the next phase until the current phase passes, unless the user explicitly overrides.

### Git workflow

The agent must not commit automatically.

After a stable checkpoint, the agent should ask:

```text
Logic này ổn định. Commit bây giờ trước khi đi tiếp không?
```

No push unless the user explicitly requests it.

## Proposed backend folder structure

```text
backend/
  api/
    __init__.py
    app.py
    health.py
    routes/
      __init__.py
      chat.py
  config/
    settings.yaml
    logging.yaml
    README_config.md
  core/
    __init__.py
    logging_setup.py
    schema.py
    settings_loader.py
    startup.py
  embedding/
    __init__.py
    batch_embed.py
    embedder.py
    sparse_embedder.py
  evaluation/
    __init__.py
    answer_eval.py
    metrics.py
    retrieval_eval.py
    run_answers.py
    run_retrieval.py
    test_loader.py
    results/
  ingestion/
    __init__.py
    pipeline.py
    chunking/
      __init__.py
      markdown_chunker.py
    helpers/
      __init__.py
      make_metadata.py
      markdown_parser.py
      split_text.py
  llm/
    __init__.py
    generator_openai.py
    prompt.py
  logs/
  reranking/
    __init__.py
    base.py
    reranker.py
    models/
      __init__.py
      cross_encoder.py
  retrieval/
    __init__.py
    context_builder.py
    dense_retriever.py
    hybrid_retriever.py
    service.py
  scoring/
    __init__.py
    bm25.py
  vectorstore/
    __init__.py
    hybrid_index.py
    qdrant.py
    reset.py
    upsert.py
qdrant_storage/
notebooks/
  01_foods_data_and_chunking.ipynb
  02_embedding_models.ipynb
  03_qdrant_ingestion.ipynb
  04_retrieval_profiles.ipynb
  05_generation_and_api.ipynb
  06_evaluation.ipynb
```

## Roadmap after MVP

The following phase is intentionally not implemented in MVP, but the design must leave room for it.

### Agentic RAG phase

Target capabilities:

- Query router:
  - direct fact;
  - guide/planning;
  - multi-hop/spanning;
  - holistic/category-wide.
- Query rewrite:
  - short optimized search query for direct questions.
- Query decomposition:
  - 2-5 sub-queries for multi-hop or broad questions.
- Parent-child retrieval:
  - child chunks optimized for search;
  - parent sections/files used for richer context.
- Retry judge:
  - judge whether an answer is missing key facts;
  - retry retrieval once with refined query.
- Evaluation comparison:
  - baseline MVP profiles vs Agentic RAG profiles.

Agentic RAG must be designed in a later spec before implementation.

## Design approval status

This document captures the design decisions from brainstorming. Implementation should only start after the user approves this spec and the accompanying implementation plan.
