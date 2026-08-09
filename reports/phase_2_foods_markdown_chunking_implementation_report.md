# Implementation Report: Phase 2 Foods Markdown Discovery And Chunking

Implementer: DeepSeek
Date: 2026-08-09
Report path:

```text
reports/phase_2_foods_markdown_chunking_implementation_report.md
```

Canonical guide context after documentation migration:

```text
guides/phase_0_mvp_foundation.md
guides/phase_2_foods_markdown_chunking.md
```

## Approved Scope

Phase 2 per the approved plan: Foods Markdown discovery and chunking. Parse curated foods Markdown into semantic chunks with stable metadata. Mini research over representative files was mandatory before coding.

Files required by the plan:

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/helpers/split_text.py
backend/ingestion/chunking/markdown_chunker.py
backend/tests/test_markdown_chunker.py
notebooks/01_foods_data_and_chunking.ipynb
```

## Summary

Mini research covered the full corpus: 91 files (57 restaurants, 24 cafes, 9 local_specialties, `food-guides.md`), 908 H2 sections. Confirmed edge cases: all files start with a single `#` heading; no pre-H2 content; no empty sections; 2 image lines in 2 restaurant files; ~40 menu tables plus local-specialty tables; H3 subsections inside H2 sections; only 2 sections exceed 1500 chars (both in `food-guides.md`, max 2298).

Implementation decisions (interpretations within the approved plan, no contract change):

- Chunk granularity is the H2 section; the section heading lives in metadata `section`, the chunk text is the section body. H3 headings and tables stay inside the body.
- `## Nguồn dữ liệu` sections are excluded from chunks: source tracking is not answer-facing content, consistent with the Session_Prompt curated data rules. The exclusion is a module constant `EXCLUDED_SECTIONS` for easy review.
- Image-only lines (`![alt](url)`) are stripped from chunk text; alt text and URLs carry no answer content.
- Long sections are split on blank-line paragraph boundaries with `max_chars=1500`; a block larger than the limit stays whole so tables are never broken. Only 2 corpus sections split.
- `chunk_id = f"{source}|{section}|{index}"` with a per-file running index: deterministic and stable across runs (covered by a test).
- `subcategory` is the folder directly under `foods/`; `food-guides.md` resolves to `guide`, matching the design example.

Result: 366 chunks from 91 files (`restaurants` 187, `cafes` 100, `local_specialties` 62, `guide` 17), all with the 7 required metadata fields, relative `source` paths, no image markdown, no `Nguồn dữ liệu` section.

## Files Created

- `backend/ingestion/helpers/markdown_parser.py` - parses markdown into (title, sections); H2 starts a section, H3 stays in body, empty sections omitted.
- `backend/ingestion/helpers/make_metadata.py` - builds the 7-field chunk metadata dict with stable `chunk_id`.
- `backend/ingestion/helpers/split_text.py` - splits long text into paragraph blocks packed greedily to `max_chars` (default 1500).
- `backend/ingestion/chunking/markdown_chunker.py` - `chunk_foods_markdown()`, `_discover_markdown_files()` resolving `knowledge_base` settings relative to `BACKEND_DIR`, exclusion by path segment, image stripping.
- `backend/tests/test_markdown_chunker.py` - 17 tests (see below).
- `notebooks/01_foods_data_and_chunking.ipynb` - learning notebook importing backend modules; 9 cells; outputs empty; `execution_count` null.

## Files Modified

None. Phase 1 files were not touched.

## Notebooks Created Or Modified

- `notebooks/01_foods_data_and_chunking.ipynb` - created; inspects discovery, metadata schema, corpus stats, sample chunks per document type, and gate checks. Default (only) mode is safe: no live model, web, deploy, or Qdrant calls. Resolves `backend/` from the working directory without depending on a fixed cwd.

## Commands Run

```bash
# repo root: corpus analysis for mini research
UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'EOF' ... EOF

# backend: compile checks
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
# clean

# backend: plan validation command
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0]['metadata'])"
# 366
# {'chunk_id': 'foods/cafes/anh kafe hue.md|Tóm tắt|0', 'source': 'foods/cafes/anh kafe hue.md', 'title': 'ANH KAFE tại Huế', 'section': 'Tóm tắt', 'category': 'foods', 'subcategory': 'cafes', 'chunk_type': 'section'}

# backend: unit tests
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q
# 17 passed in 0.12s

# repo root: notebook rule check (JSON valid, execution_count null, outputs empty, no secret/live-call tokens)
UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'EOF' ... EOF
```

## Tests And Verification

- `py_compile` clean for all 4 runtime modules.
- `pytest tests/ -q`: 17 passed. Coverage: parser (H2 split, intro content, empty-section omission), split_text (short text whole, greedy packing, oversized block whole), metadata fields, image stripping, `Nguồn dữ liệu` exclusion, long-section splitting with unique chunk ids, corpus gate (non-empty text, required metadata, KB-relative sources, excluded folders absent, no absolute paths, unique ids, stable ids across runs, no image markdown).
- Gate checks rerun explicitly: 366 chunks, non-empty text, required metadata present, `chunk_id` format `source|section|index`.
- Notebook JSON validation: `nbformat` 4, all `execution_count` null, all outputs empty, no API key/secret/token/`.env`/http tokens in cell sources.

## Evaluation Results

Not applicable to Phase 2; the phase has no retrieval or answer evaluation.

## Deviations From Plan

None. Decisions documented in Summary are interpretations within the approved plan and are listed in Known Issues for reviewer confirmation.

## Known Issues

- `## Nguồn dữ liệu` sections are excluded from chunks (module constant in `markdown_chunker.py`). Interpretation of the plan/session rules; reviewer should confirm before Phase 3. Severity: none.
- Split threshold `max_chars=1500` is a module default in `split_text.py`, not a settings.yaml value. The plan does not define a chunking config section. Severity: none.
- `backend/tests/` is a new directory with no `__init__.py`; tests run with `python -m pytest tests/` from `backend/` so `ingestion` imports resolve from cwd. Matches the plan's command style.

## Security, Data Safety, Reliability, Performance Self-Check

- Security: no secrets read, printed, logged, or exposed; `.env` never accessed; no absolute private paths in chunks or metadata.
- Data safety: knowledge base files were read only, never modified; chunk text is verbatim KB content (image lines removed, headings stripped into metadata).
- Reliability: file discovery is sorted and deterministic; chunk ids stable across runs (tested); `root_dir` resolved against `BACKEND_DIR`, not process cwd; excluded folders matched by exact path segment.
- Performance: single pass over 91 small files; no model loads, network, or unbounded work.
- Tests: 17 unit tests run without secrets, paid models, deploy, or external services; integration tests read the local KB.
- Notebooks: valid JSON, outputs empty, execution counts null, default cells safe, no duplicate runtime logic (imports backend modules).

## Live Access / Secrets Statement

```text
No live network/model/deploy/secret access occurred.
```

## Handoff To Codex

Review first: `backend/ingestion/chunking/markdown_chunker.py` (exclusion of `Nguồn dữ liệu`, image stripping, split threshold) and `backend/tests/test_markdown_chunker.py`. Specific risk area: the `Nguồn dữ liệu` exclusion decision and the hardcoded 1500-char split limit, both flagged above. Phase 2 gate is met: chunk count non-zero, non-empty text, required metadata, excluded folders absent, no absolute paths.
