# Phase 2 Foods Markdown Chunking Simplicity Design

Date: `2026-08-24 +07`

Status: `approved by user`

## Purpose

Simplify the Phase 2 curated Markdown loader and chunker without changing the
corpus consumed by Phase 3–7. The result must remain a small, deterministic
pipeline that turns the real Hue foods knowledge base into answer-facing text
with enough provenance for indexing, retrieval, citation and evaluation.

This design uses `/home/minhhieu/llm_rag` only as a readability and semantic
chunking reference. Hue RAG keeps curated Markdown, heading boundaries and
deterministic IDs; it does not copy the reference project's JSON-table
chunkers, random UUIDs, timestamps or imagined-shape validators.

## Current phase and before state

Phase 0 and Phase 1 simplicity reviews are approved. Phase 2 retains its
historical approval, but its current task is the pre-implementation simplicity
review described here. Phase 3–6 keep their historical approval and are not in
the implementation scope of this review.

The current Phase 2 runtime:

- discovers 91 curated foods Markdown files in deterministic path order;
- parses H1 titles and H2 answer-facing sections;
- excludes `Nguồn dữ liệu` and image-only lines;
- splits normal content around a 400-character target while keeping tables
  atomic;
- prepends a deterministic title and context label;
- emits 572 chunks with seven metadata fields and stable IDs;
- is consumed by ingestion, notebooks and the later RAG phases.

The current runtime implementation is spread across four files:

```text
backend/ingestion/chunking/markdown_chunker.py
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/helpers/split_text.py
```

The parser and metadata helpers are tiny Phase 2 implementation details. The
splitter has independent behavior worth keeping separate. The existing test
file has 31 tests, including overlapping corpus and invariant checks. Notebook
02 also contains presentation helpers that do not belong to the runtime API.

## Approved constraints

This is a behavior-preserving simplification.

The implementation must preserve all 572 chunks in exact list order. For every
position, both `text` and the complete metadata mapping must be identical to
the pre-change baseline, including `chunk_id`.

The compatibility boundary is:

```python
chunk_foods_markdown() -> list[dict]
```

and the existing seven-field output contract. Internal helper modules and
private functions are not compatibility APIs.

Do not change curated Markdown, chunk boundaries, context labels, metadata,
IDs, discovery order, settings values, embedding, indexing, retrieval,
generation or evaluation behavior in this phase.

## Approved architecture

Use two runtime modules:

```text
settings
-> discover curated foods Markdown in stable order
-> read one file
-> parse and validate H1/H2
-> exclude non-answer content
-> split answer-facing bodies
-> add deterministic text context and metadata
-> validate corpus invariants
-> return the ordered chunk list
```

### `markdown_chunker.py`

This module owns:

- settings-based knowledge-base discovery;
- exact excluded-path handling;
- H1/H2 parsing;
- minimal file-contract validation;
- `Nguồn dữ liệu` and image-only-line exclusion;
- deterministic context labels;
- metadata construction;
- per-file and whole-corpus orchestration;
- the public `chunk_foods_markdown()` entry point.

Keep the code direct. Ordinary small private functions are acceptable when
they make the flow easier to read. Do not introduce loader classes, parser
objects, validator frameworks, registries, factories or dependency injection.

### `split_text.py`

This module owns only the content-splitting algorithm. It remains separate
because paragraph, sentence, list and Markdown-table boundaries form one
coherent behavior that can be understood and tested independently.

### Removed helpers

Delete these modules after confirming that no valid consumer remains:

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
```

Do not add compatibility wrappers for their private functions. Update Phase 2
tests to exercise either the public chunker or the retained splitter.

## Markdown and text contract

H1 and H2 are required as source structure, not as literal answer syntax:

- H1 identifies the document/entity and supplies `metadata.title`;
- H2 defines the semantic section and supplies `metadata.section`;
- H3 and deeper headings remain part of their enclosing H2 body;
- Markdown `#` and `##` markers do not appear in chunk text merely because
  they were parsing boundaries;
- the title and short context label remain in plain chunk text so an isolated
  chunk still identifies its entity and topic.

Final LLM answers are not required to reproduce source headings.

The existing splitting behavior remains unchanged:

- normal body text uses `400` characters as the target maximum;
- prefer blank-line paragraphs, sentence endings and list-line boundaries;
- if a sentence is still too long, split at the nearest usable whitespace;
- never cut inside a word;
- do not overlap adjacent chunks;
- keep a Markdown table atomic even when it exceeds 400 characters;
- do not count the prepended title/context label against the body target.

Keep the current explicit, deterministic context-label rules and their generic
heading fallback. Do not call a model, infer new facts, move the mapping into a
new configuration layer or change label text during this refactor.

## Metadata and source provenance

Every chunk keeps exactly these seven fields:

```text
chunk_id
source
title
section
category
subcategory
chunk_type
```

`source` is required even though semantic matching can operate on text alone.
The live system uses it to form stable IDs, build Qdrant payloads, construct
LLM context, return API sources and trace evidence back to curated Markdown.

Source validation stays minimal:

- the value is the path of the file currently being chunked;
- it is relative to the configured knowledge-base root;
- it cannot expose a private absolute path;
- it participates in `chunk_id = f"{source}|{section}|{index}"`.

Do not add URL checks, external-source schemas or a provenance subsystem.

## Validation and error handling

Validate only failures supported by the real corpus and downstream contract:

1. each discovered file has a non-empty H1 title;
2. each file has at least one non-empty, answer-facing H2 section;
3. each emitted chunk has non-empty text;
4. each chunk has exactly the seven required metadata fields;
5. each source stays under the configured knowledge-base root;
6. no two chunks share a `chunk_id`.

Malformed curated files fail fast. Use an ordinary built-in exception with a
short message containing the affected file and failed invariant. Do not add a
custom exception hierarchy, validator class, recovery mode or silent skipping.

## Test design

Replace overlapping tests with a small behavior-oriented suite. The target is
coverage of meaningful behavior, not a target number of tests.

Representative unit tests cover:

- short text that needs no split;
- natural paragraph and sentence boundaries;
- an overlong sentence split at whitespace;
- wrapped/list-line behavior;
- an atomic Markdown table over the target size;
- H1/H2 parsing with H3 retained in the body;
- answer-source and image-only-line exclusion;
- deterministic metadata and IDs;
- clear failure for malformed curated input.

A corpus integration test runs `chunk_foods_markdown()` against the real
curated foods knowledge base and checks the durable invariants: non-empty
output/text, exact schema, valid relative sources, exclusions and unique stable
IDs.

The permanent suite must not include a committed full-corpus golden snapshot or
digest. It also must not treat 572 as a timeless product invariant. Curated
content may evolve later through an approved data change.

For this refactor, 572 is a mandatory acceptance baseline. Before the
Implementer changes code, capture the ordered output outside the repository.
After implementation, compare every ordered `text` and metadata mapping against
that baseline. The comparison result is review evidence, not a committed test
fixture.

Small synthetic strings are acceptable for deterministic splitter unit tests.
They do not replace the required full-corpus run and cannot be presented as
deployment or completion evidence.

## Notebook design

Keep `notebooks/02_foods_data_and_chunking.ipynb` as a short learning
walkthrough because Phase 2 has genuine visual and educational value.

The notebook:

- imports and calls only `chunk_foods_markdown()` from the Phase 2 runtime;
- shows a compact discovery/corpus summary;
- shows one normal text chunk, one rendered table chunk and one food-guide
  chunk;
- briefly explains H1/H2 roles, the 400-character target, atomic tables,
  context labels and the seven metadata fields;
- does not define private presentation helpers, copy runtime logic, reproduce
  validation or become a test suite;
- contains no web, provider API, Qdrant, secrets or private absolute paths;
- is committed with empty outputs and `execution_count: null`.

The Reviewer executes Run All on a temporary copy and records the real result.

## Scope boundary and downstream policy

Implementation edits are limited to Phase 2 ownership:

```text
backend/ingestion/chunking/markdown_chunker.py
backend/ingestion/helpers/split_text.py
backend/ingestion/helpers/markdown_parser.py        # delete
backend/ingestion/helpers/make_metadata.py           # delete
backend/tests/test_markdown_chunker.py
notebooks/02_foods_data_and_chunking.ipynb
```

Phase 3–7 code may be inspected and tested but not edited in this scope.

Apply a defer-by-ownership policy with a no-regression gate:

- a pre-existing downstream issue is recorded for its owning phase;
- a regression introduced by this Phase 2 implementation blocks Phase 2
  approval and must be removed within Phase 2 compatibility boundaries;
- do not defer a newly broken approved runtime to a later phase.

The Phase 2 simplicity review records downstream findings in one small table
with affected phase, dependency, observed evidence, concrete impact, later
action and whether it blocks approval. Do not create a separate debt registry
or distribute the handoff across code TODO comments. `Project_Status.md` keeps
only the current summary and next action after approval.

## Verification strategy

Verification proceeds by the cheapest real layer that proves the behavior:

```text
compile affected runtime modules
-> run focused Phase 2 tests
-> execute full chunking on the real curated corpus
-> compare all 572 ordered chunks against the pre-change baseline
-> run Notebook 02 on a temporary copy
-> run existing downstream smoke tests
-> run the full backend suite
-> inspect diff, deleted imports and merge markers
```

The active Hue Qdrant collection remains read-only. The user authorizes an
isolated real collection if a downstream smoke failure leaves genuine doubt
about ingestion compatibility. Do not create that collection routinely when
the chunk-layer and existing downstream checks already prove compatibility.

If an isolated collection is needed, use the real local Qdrant service and real
pipeline components. Mocks, fake services or replayed outputs are not
completion evidence.

The paid Phase 7 benchmark is not required because this design preserves every
ordered chunk exactly. If equivalence fails or retrieval behavior changes,
stop rather than expanding the review silently.

## Reviewer and Implementer workflow

The roles remain separate:

1. the Reviewer owns this approved design and the later implementation plan;
2. an Implementer changes only the approved files and reports exact commands
   and observed results;
3. the Reviewer audits the diff independently, performs the before/after
   comparison and runs the exact real verification path;
4. only the user can confirm the final Phase 2 simplicity approval.

The Reviewer does not implement the code under this workflow. Creation of an
implementation plan requires a separate user instruction after this design
file is reviewed.

## Acceptance

Phase 2 simplicity review can be approved only when:

1. the runtime uses the approved two-module structure and remains easy to
   follow;
2. all 572 chunks match the pre-change baseline in exact order, text and full
   metadata;
3. the seven-field contract, relative sources and deterministic IDs remain
   intact;
4. malformed real inputs fail clearly without a validation framework;
5. the focused tests, real-corpus run, Notebook 02 and downstream smoke checks
   pass;
6. no Phase 3–7 file or active collection is mutated;
7. downstream findings are recorded by ownership and no new regression is
   deferred;
8. unrelated worktree changes are preserved;
9. the Reviewer verifies independently and the user confirms the result.

No commit or push is authorized by this design.
