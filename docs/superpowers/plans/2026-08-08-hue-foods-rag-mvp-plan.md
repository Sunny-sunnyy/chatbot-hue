# Hue Foods RAG MVP Implementation Plan

Last updated: `2026-08-08 22:35 +07`

## Purpose

This plan breaks the Hue Foods RAG MVP into small implementation phases. Each phase has runtime files, notebooks, and validation gates. Do not implement a later phase until the previous phase passes its gate, unless the user explicitly overrides.

Runtime code lives in `backend/`. Learning notebooks live in `notebooks/`.

Commands run from `backend/`:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m ingestion.pipeline
```

## Global constraints

- Communicate in Vietnamese.
- Code, comments, docstrings, and variable names use standard English.
- Do not read or print secrets from `.env` or credential files.
- Do not use web/data enrichment unless the user explicitly requests it.
- Do not commit or push automatically.
- Use `UV_CACHE_DIR=/tmp/uv-cache uv run ...` for Python commands.
- Notebook logic must import backend modules rather than duplicate runtime logic.
- Benchmark results must be recorded in `docs/superpowers/plans/2026-08-08-hue-foods-rag-benchmark-log.md`.

## Phase 0. Design and repository preparation

Goal: create the agreed documentation and confirm the implementation scope.

Files:

```text
docs/superpowers/specs/2026-08-08-hue-foods-rag-mvp-design.md
docs/superpowers/plans/2026-08-08-hue-foods-rag-mvp-plan.md
docs/superpowers/plans/2026-08-08-hue-foods-rag-benchmark-log.md
```

Validation:

```bash
git status --short
find docs/superpowers -maxdepth 3 -type f | sort
```

Checkpoint:

- User reviews and approves spec/plan before code implementation starts.

## Phase 1. Backend skeleton and configuration

Goal: create the backend module structure and central settings loader.

Mini research/brainstorm before coding:

- Inspect current `pyproject.toml`.
- Confirm dependency availability from existing `uv.lock`.
- Confirm no existing `backend/` runtime files conflict with new layout.

Files to create:

```text
backend/config/settings.yaml
backend/config/logging.yaml
backend/core/settings_loader.py
backend/core/logging_setup.py
backend/core/schema.py
backend/*/__init__.py
```

Key config fields:

```yaml
active_profile: dense_only

profiles:
  dense_only:
    retrieval_mode: dense
    use_bm25: false
    use_reranker: false
  hybrid_no_rerank:
    retrieval_mode: hybrid
    use_bm25: true
    use_reranker: false
  hybrid_rerank:
    retrieval_mode: hybrid
    use_bm25: true
    use_reranker: true

knowledge_base:
  root_dir: ../knowledge-base-hue
  include_globs:
    - foods/**/*.md
    - foods/food-guides.md
  exclude_parts:
    - evaluation
    - _source-dumps
    - meta

embedding:
  provider: sentence_transformer
  model: intfloat/multilingual-e5-small
  vector_size: 384
  device: cpu
  batch_size: 64

vector_database:
  url: http://localhost:6333
  collection_name: hue_foods_rag
  reset_collection: true
  distance: cosine

retrieval:
  top_k: 10
  candidate_multiplier: 3
  score_threshold: 0.0
  dense_weight: 0.6
  bm25_weight: 0.4

reranking:
  model: cross-encoder/ms-marco-MiniLM-L-6-v2
  device: cpu
  top_k: 5

llm:
  provider: openai
  answer_model: gpt-5-nano
  temperature: 0.2
  max_output_tokens: 1024

evaluation:
  test_file: ../knowledge-base-hue/foods/evaluation/tests.jsonl
  judge_model: gpt-5-mini
```

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from core.settings_loader import load_settings; print(load_settings()['active_profile'])"
```

Gate:

- Settings load successfully.
- Active profile resolves to a valid profile.
- No secrets are printed.

## Phase 2. Foods Markdown discovery and chunking

Goal: parse curated foods Markdown into semantic chunks with stable metadata.

Mini research/brainstorm before coding:

- Inspect representative files from:
  - `foods/restaurants/`
  - `foods/cafes/`
  - `foods/local_specialties/`
  - `foods/food-guides.md`
- Identify edge cases:
  - image Markdown;
  - tables;
  - missing optional sections;
  - long sections;
  - file names with spaces.

Files to create:

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/helpers/split_text.py
backend/ingestion/chunking/markdown_chunker.py
notebooks/01_foods_data_and_chunking.ipynb
```

Expected chunk object:

```python
{
    "text": "...",
    "metadata": {
        "chunk_id": "...",
        "source": "foods/restaurants/bun bo hanh.md",
        "title": "Bún bò Hạnh",
        "section": "Món ăn / trải nghiệm",
        "category": "foods",
        "subcategory": "restaurants",
        "chunk_type": "section",
    },
}
```

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/chunking/markdown_chunker.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0]['metadata'])"
```

Tests to add:

```text
backend/tests/test_markdown_chunker.py
```

Gate:

- Chunk count is non-zero.
- All chunks have non-empty `text`.
- All chunks have required metadata fields.
- Excluded folders are not indexed.
- No absolute paths appear in metadata.

## Phase 3. Embedding and sparse representation

Goal: implement local SentenceTransformer embeddings and sparse representation.

Mini research/brainstorm before coding:

- Confirm first embedding model and vector size.
- Pick 2-3 candidate Vietnamese/multilingual models for later benchmark.
- Confirm CPU/GPU constraints before large model tests.

Files to create:

```text
backend/embedding/embedder.py
backend/embedding/batch_embed.py
backend/embedding/sparse_embedder.py
notebooks/02_embedding_models.ipynb
```

Runtime behavior:

- `embed_texts(texts)` returns normalized dense vectors.
- Empty input returns an empty list.
- Model is cached in process.
- Sparse embedder fits on the full chunk corpus.
- Sparse encode returns `indices` and `values`.

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile embedding/embedder.py embedding/batch_embed.py embedding/sparse_embedder.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from embedding.embedder import embed_texts; v = embed_texts(['Bún bò Huế']); print(len(v), len(v[0]))"
```

Tests to add:

```text
backend/tests/test_sparse_embedder.py
```

Gate:

- Dense vector length matches `embedding.vector_size`.
- Sparse embedder fit returns non-empty vocabulary.
- Notebook can embed sample foods queries and display vector size/model info.

## Phase 4. Qdrant ingestion and hybrid points

Goal: create one active Qdrant collection and upsert dense+sparse points.

Mini research/brainstorm before coding:

- Confirm Qdrant Docker status.
- Confirm reset behavior and warning copy.
- Confirm whether the active collection already exists.

Files to create:

```text
backend/vectorstore/qdrant.py
backend/vectorstore/hybrid_index.py
backend/vectorstore/upsert.py
backend/vectorstore/reset.py
backend/ingestion/pipeline.py
notebooks/03_qdrant_ingestion.ipynb
```

Ingestion behavior:

- Discover foods Markdown.
- Chunk documents.
- Fit sparse embedder on all chunk texts.
- Build Qdrant points with named vectors:
  - `dense`
  - `sparse`
- If `vector_database.reset_collection: true`, recreate active collection.
- If `reset_collection: false`, do not delete collection.

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m ingestion.pipeline
```

Smoke checks:

```bash
curl -s http://localhost:6333/collections
```

Optional Python check:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from vectorstore.qdrant import get_qdrant_client; print(get_qdrant_client().get_collections())"
```

Gate:

- Qdrant collection exists.
- Collection vector size matches active embedding config.
- Upsert count equals chunk count.
- Reset behavior is documented before use.

## Phase 5. Retrieval profiles and ContextBuilder

Goal: implement `dense_only`, `hybrid_no_rerank`, and `hybrid_rerank` retrieval.

Mini research/brainstorm before coding:

- Run initial retrieval probes against food questions.
- Inspect failures manually before tuning weights.
- Decide initial `top_k`, `candidate_multiplier`, `dense_weight`, `bm25_weight`.

Files to create:

```text
backend/core/startup.py
backend/retrieval/dense_retriever.py
backend/retrieval/hybrid_retriever.py
backend/retrieval/service.py
backend/retrieval/context_builder.py
backend/scoring/bm25.py
backend/reranking/base.py
backend/reranking/models/cross_encoder.py
backend/reranking/reranker.py
notebooks/04_retrieval_profiles.ipynb
```

Retrieval behavior:

- `dense_only`: dense Qdrant search only.
- `hybrid_no_rerank`: dense candidates + BM25 Python score fusion.
- `hybrid_rerank`: hybrid output + CrossEncoder rerank.

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile retrieval/dense_retriever.py retrieval/hybrid_retriever.py retrieval/service.py retrieval/context_builder.py scoring/bm25.py
```

Tests to add:

```text
backend/tests/test_bm25.py
backend/tests/test_context_builder.py
backend/tests/test_retrieval_service.py
```

Gate:

- Each profile returns retrieved documents for representative foods queries.
- `retrieval_debug` includes profile, model, dense score, BM25 score when available, hybrid score when available, and rerank score when available.
- ContextBuilder enforces document and length limits.

## Phase 6. OpenAI generation and JSON backend API

Goal: implement grounded answer generation and non-streaming FastAPI chat.

Mini research/brainstorm before coding:

- Verify official OpenAI model IDs before setting defaults.
- Confirm local environment has API key configured without printing it.
- Confirm answer and judge model separation.

Files to create:

```text
backend/llm/prompt.py
backend/llm/generator_openai.py
backend/api/app.py
backend/api/health.py
backend/api/routes/__init__.py
backend/api/routes/chat.py
notebooks/05_generation_and_api.ipynb
```

API behavior:

```text
GET /health
POST /api/chat
```

`POST /api/chat` returns JSON:

```text
answer
sources
session_id
retrieval_debug
```

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile api/app.py api/health.py api/routes/chat.py llm/prompt.py llm/generator_openai.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import importlib; importlib.import_module('api.app'); print('api.app import ok')"
```

Smoke API check after server is running:

```bash
curl -s http://localhost:8000/health
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Lần đầu đến Huế nên ăn gì?"}'
```

Tests to add:

```text
backend/tests/test_llm_generator_openai.py
backend/tests/test_api_chat.py
```

Gate:

- API imports cleanly.
- `/health` responds.
- `/api/chat` returns grounded JSON with sources.
- Missing context/query cases return safe messages.
- No secret is printed.

## Phase 7. Retrieval and answer evaluation

Goal: evaluate the active profile/model using the existing foods test suite.

Mini research/brainstorm before coding:

- Inspect current `knowledge-base-hue/foods/evaluation/tests.jsonl`.
- Confirm categories and expected metrics.
- Decide whether to run answer judge on all tests or a subset first for cost control.

Files to create:

```text
backend/evaluation/test_loader.py
backend/evaluation/metrics.py
backend/evaluation/retrieval_eval.py
backend/evaluation/answer_eval.py
backend/evaluation/run_retrieval.py
backend/evaluation/run_answers.py
backend/evaluation/results/.gitkeep
notebooks/06_evaluation.ipynb
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

Validation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m evaluation.run_retrieval
UV_CACHE_DIR=/tmp/uv-cache uv run python -m evaluation.run_answers
```

Gate:

- Retrieval JSONL result file is created.
- Answer JSONL result file is created.
- Summary metrics print to terminal.
- Benchmark log is updated manually or by a documented helper.
- Results are reviewed before tuning.

## Phase 8. Benchmark loop

Goal: compare profiles and embedding models through repeatable manual runs.

Benchmark procedure:

1. Edit `backend/config/settings.yaml`.
2. Set:
   - `active_profile`
   - `embedding.model`
   - `embedding.vector_size`
   - `vector_database.reset_collection: true`
3. Run ingestion:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m ingestion.pipeline
```

4. Run retrieval evaluation:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m evaluation.run_retrieval
```

5. Run answer evaluation when needed:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m evaluation.run_answers
```

6. Record summary in:

```text
docs/superpowers/plans/2026-08-08-hue-foods-rag-benchmark-log.md
```

7. Repeat for next model/profile.

Gate:

- A candidate embedding model/profile is chosen from evidence.
- Set `vector_database.reset_collection: false` after final model selection.
- Keep final collection for API runtime.

## Phase 9. Post-MVP Agentic RAG roadmap

This phase is not implemented in MVP. It must get a separate design review before coding.

Planned components:

```text
backend/agentic/
  router.py
  query_rewrite.py
  query_decompose.py
  parent_child.py
  retry_judge.py
```

Future capabilities:

- Query router for direct, planning, multi-hop, and holistic questions.
- Query rewrite for direct lookup.
- Query decomposition for spanning questions.
- Parent-child retrieval inspired by `rag_old`.
- Retry judge that retries retrieval once if answer is incomplete.
- Evaluation comparison against MVP profiles.

Gate before implementation:

- New spec approved by user.
- Parent-child data model agreed.
- Cost and latency limits agreed.
- Evaluation categories for agentic behavior agreed.

## Checkpoint rule

After every stable phase:

```text
Logic này ổn định. Commit bây giờ trước khi đi tiếp không?
```

Do not commit unless the user explicitly confirms.
