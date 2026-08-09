# Codex Review: Phase 2 Foods Markdown Chunking

Decision: approved
Reviewer: Codex
Date: 2026-08-09
Review path:

```text
reports/phase_2_foods_markdown_chunking_codex_review.md
```

Implementer report:

```text
reports/phase_2_foods_markdown_chunking_implementation_report.md
```

## Tóm Tắt

Reviewed Phase 2 foods Markdown discovery, semantic section chunking, tests, and learning notebook against the approved Hue Foods RAG MVP spec and plan. The implementation stays within Phase 2 scope, discovers only curated foods Markdown, creates stable metadata, excludes configured folders, avoids absolute paths in metadata, and keeps notebook outputs empty.

## Findings

Không có blocker hoặc major findings.

- minor: The notebook imports `_discover_markdown_files`, a private helper, for inspection. This is acceptable for a learning notebook because runtime behavior still lives in backend modules and no duplicate chunking pipeline is implemented.

## Verification

Commands run and important results.

```bash
git status --short
# Worktree already had unrelated knowledge-base deletions and untracked rag_old/skills.
# Phase 2 files are untracked under backend/ingestion, backend/tests, notebooks, and reports/.

sed -n '1,260p' reports/phase_2_foods_markdown_chunking_implementation_report.md
# Implementation report reviewed.

sed -n '130,230p' docs/superpowers/plans/2026-08-08-hue-foods-rag-mvp-plan.md
# Phase 2 plan and gate reviewed.

sed -n '120,210p' docs/superpowers/specs/2026-08-08-hue-foods-rag-mvp-design.md
# Chunking strategy and metadata requirements reviewed.

sed -n '1,260p' skills/karpathy-guidelines/SKILL.md
# Reviewer code-quality guideline read.

sed -n '1,260p' knowledge-base-hue/meta/foods-template.md
sed -n '1,260p' knowledge-base-hue/foods/evaluation/validate_tests.py
# Foods rules and evaluation context reviewed.

cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
# clean

UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0]['metadata'])"
# 366
# {'chunk_id': 'foods/cafes/anh kafe hue.md|Tóm tắt|0', 'source': 'foods/cafes/anh kafe hue.md', 'title': 'ANH KAFE tại Huế', 'section': 'Tóm tắt', 'category': 'foods', 'subcategory': 'cafes', 'chunk_type': 'section'}

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q
# 17 passed in 0.15s

cd ..
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import json; from pathlib import Path; nb=json.loads(Path('notebooks/01_foods_data_and_chunking.ipynb').read_text(encoding='utf-8')); print(nb.get('nbformat'), len(nb.get('cells', []))); print([(c.get('cell_type'), c.get('execution_count'), len(c.get('outputs', []))) for c in nb['cells']]); bad=[]; [bad.append((i,'execution_count')) for i,c in enumerate(nb['cells']) if c.get('cell_type') == 'code' and c.get('execution_count') is not None]; [bad.append((i,'outputs')) for i,c in enumerate(nb['cells']) if c.get('outputs')]; print('bad', bad)"
# 4 9
# bad []

cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from collections import Counter; from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks=chunk_foods_markdown(); required={'chunk_id','source','title','section','category','subcategory','chunk_type'}; print('chunks', len(chunks)); print('files', len({c['metadata']['source'] for c in chunks})); print(Counter(c['metadata']['subcategory'] for c in chunks)); print('empty_text', sum(not c['text'].strip() for c in chunks)); print('missing_meta', sum(not required <= c['metadata'].keys() for c in chunks)); print('absolute_meta', sum(any(str(v).startswith('/') for v in c['metadata'].values()) for c in chunks)); print('excluded', sum(any(p in {'evaluation','_source-dumps','meta'} for p in c['metadata']['source'].split('/')) for c in chunks)); print('source_sections', sum(c['metadata']['section']=='Nguồn dữ liệu' for c in chunks)); print('image_markdown', sum('![' in c['text'] for c in chunks)); print('unique_ids', len({c['metadata']['chunk_id'] for c in chunks}) == len(chunks))"
# chunks 366
# files 91
# Counter({'restaurants': 187, 'cafes': 100, 'local_specialties': 62, 'guide': 17})
# empty_text 0
# missing_meta 0
# absolute_meta 0
# excluded 0
# source_sections 0
# image_markdown 0
# unique_ids True

rg -n "OPENAI_API_KEY|API_KEY|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE|\\.env|dotenv|openai|OpenAI|requests|http://|https://|qdrant|Qdrant|uvicorn|FastAPI|subprocess|curl" backend/ingestion backend/tests notebooks/01_foods_data_and_chunking.ipynb reports/phase_2_foods_markdown_chunking_implementation_report.md
# Only safe documentation text, report text, and one test fixture image URL were found.

git diff --check -- backend/ingestion backend/tests notebooks reports/phase_2_foods_markdown_chunking_implementation_report.md
# clean
```

## Scope Check

The work stayed inside the approved Phase 2 scope:

- created the four runtime chunking modules requested by the plan;
- added `backend/tests/test_markdown_chunker.py`;
- added `notebooks/01_foods_data_and_chunking.ipynb`;
- did not implement embeddings, Qdrant, retrieval, reranking, API, generation, or evaluation runtime.

Accepted implementation decisions:

- `## Nguồn dữ liệu` sections are excluded from chunks. This matches the project rule that source tracking is not answer-facing content for RAG answers.
- Image-only Markdown lines are stripped from chunk text. This avoids indexing URL noise and does not create new factual content.
- `max_chars=1500` remains a local splitter default. The approved plan did not define a chunking config section, and only two current sections split.

## Safety And Quality Check

- Security: no secrets were read, printed, logged, or exposed. No live model/API/web/deploy calls were introduced.
- Data safety: curated foods Markdown was read only; no knowledge base files were modified; metadata stores KB-relative paths only.
- Reliability: discovery is sorted and deterministic; chunk IDs are stable across runs; excluded folders are filtered by path segment; tests cover corpus gates and helper behavior.
- Performance: the chunker performs a bounded local pass over 91 small Markdown files; no model loading or external services.
- Tests: `py_compile`, Phase 2 plan command, focused pytest suite, notebook JSON checks, and additional corpus gate checks all passed.
- Notebooks: JSON parses; all `execution_count` values are `null`; all `outputs` are empty; cells import backend modules and contain no live API, web, Qdrant, deploy, or secret calls.
- Evaluation: not applicable in Phase 2; no retrieval or answer metrics were claimed.

## Required Changes

Not applicable.

## Approval Notes

Approved files:

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/helpers/split_text.py
backend/ingestion/chunking/markdown_chunker.py
backend/tests/test_markdown_chunker.py
notebooks/01_foods_data_and_chunking.ipynb
reports/phase_2_foods_markdown_chunking_implementation_report.md
```

Accepted limitations:

- Chunking config is not yet exposed in `settings.yaml`.
- Notebook uses a private discovery helper for inspection.
- `## Nguồn dữ liệu` sections are not indexed in Phase 2.

Next phase allowed: Phase 3 Embedding and sparse representation.

`Project_Status.md` was updated after approval.
