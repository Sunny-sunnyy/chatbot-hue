# Phase 2 Foods Markdown Chunking Simplicity Implementation Plan

> **For the Implementer:** REQUIRED SUB-SKILL: start with
> `using-superpowers`, then use `executing-plans` task by task. Apply
> `test-driven-development` for the validation/consolidation change,
> `systematic-debugging` for any unexpected failure and
> `verification-before-completion` before handoff.

**Goal:** Reduce Phase 2 to one readable Markdown chunker plus one focused text
splitter while preserving all 572 real corpus chunks in exact order, text and
metadata.

**Architecture:** `chunk_foods_markdown()` remains the only public Phase 2
entrypoint. `markdown_chunker.py` owns discovery, parsing, minimal validation,
cleaning, labels, metadata and orchestration. `split_text.py` remains a separate
pure splitting module. Notebook 02 calls only the public entrypoint.

**Tech Stack:** Python 3.13, pathlib, regex, pytest, Jupyter/nbconvert, Qdrant
only if conditional downstream verification requires it, `uv`.

## Global constraints

- Read `session_prompt/IMPLEMENTER_WORKFLOW.md`,
  `session_prompt/Session_Prompt.md`, `session_prompt/Project_Status.md`,
  `guides/phase_2_foods_markdown_chunking.md` and the approved Phase 2
  simplicity design before editing.
- Run `git status --short` and inspect scoped diffs first. The worktree already
  contains unrelated user deletions and Phase 6 report/notebook edits; preserve
  all of them.
- Do not edit until the ordered 572-chunk Before baseline has been captured
  outside the repository and its path/hash recorded.
- Preserve exact ordered equality for every chunk's `text` and complete
  metadata mapping. Count-only, set-only or ID-only equality is insufficient.
- Keep `chunk_foods_markdown()` as the only public Phase 2 entrypoint. Do not
  add parameters, classes, factories, registries, dependency injection,
  compatibility wrappers or new runtime dependencies.
- Do not change curated Markdown, `settings.yaml`, context labels, splitting
  boundaries, metadata fields, chunk IDs or discovery order.
- Do not edit Phase 3–7 runtime or tests merely to accommodate Phase 2. Record
  pre-existing downstream issues; remove any regression introduced by this
  implementation before handoff.
- Do not mutate the active `hue_foods_e5_small_384` collection. Create an
  isolated real Qdrant collection only if downstream smoke evidence leaves an
  unresolved ingestion-compatibility question.
- Small synthetic unit inputs are allowed. Mocks, fake services and replayed
  results are not completion evidence; the real 91-file corpus run is required.
- Do not run the paid 104-question Phase 7 benchmark while ordered chunk
  equivalence holds.
- Do not edit canonical guides, the approved design, role workflows,
  `Project_Status.md`, historical reports, Codex reviews or user reports.
- Do not stage, commit or push.

## File map

**Modify:**

- `backend/ingestion/chunking/markdown_chunker.py` — consolidate parsing,
  metadata and minimal validation into the public chunking flow.
- `backend/ingestion/helpers/split_text.py` — retain only the existing coherent
  splitting behavior; simplify only where tests and equivalence prove safety.
- `backend/tests/test_markdown_chunker.py` — replace overlapping checks with a
  focused behavior-oriented suite.
- `notebooks/02_foods_data_and_chunking.ipynb` — reduce to a public-API learning
  walkthrough.

**Delete:**

- `backend/ingestion/helpers/markdown_parser.py`
- `backend/ingestion/helpers/make_metadata.py`

**Create:**

- `reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md`

**Verify only:**

- `backend/ingestion/pipeline.py`
- `backend/vectorstore/hybrid_index.py`
- `backend/retrieval/context_builder.py`
- `backend/api/routes/chat.py`
- Phase 3–7 tests and notebooks that consume `chunk_foods_markdown()` or the
  seven-field payload.

---

### Task 1: Lock the Before evidence and scope

**Files:**

- Inspect only: all scoped files in the file map.
- Create outside repository: one temporary ordered JSON baseline under `/tmp`.

**Interfaces:**

- Consumes: current `chunk_foods_markdown()` and the real curated foods corpus.
- Produces: immutable review evidence for exact post-change comparison.

- [ ] **Step 1: Inspect worktree and scoped diffs**

From the repository root:

```bash
git status --short
git diff -- backend/ingestion/chunking/markdown_chunker.py backend/ingestion/helpers/markdown_parser.py backend/ingestion/helpers/make_metadata.py backend/ingestion/helpers/split_text.py backend/tests/test_markdown_chunker.py notebooks/02_foods_data_and_chunking.ipynb
```

Expected: no pre-existing scoped change. If a scoped file already contains an
unrelated user edit, stop and report the overlap instead of overwriting it.

- [ ] **Step 2: Confirm the current focused baseline**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m pytest tests/test_markdown_chunker.py -q --tb=short
```

Expected current result: all 31 tests pass. Record the exact observed count and
warnings; do not rely only on the historical report.

- [ ] **Step 3: Capture the ordered corpus outside the repository**

First ensure the proposed path is unused:

```bash
test ! -e /tmp/hue-rag-phase2-before-20260824.json
```

If it already exists, choose a new explicit `/tmp/hue-rag-phase2-before-...json`
path and record it. Do not overwrite or delete an unknown file.

From `backend/`, capture the live Python output:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'import hashlib, json; from pathlib import Path; from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); raw = json.dumps(chunks, ensure_ascii=False, sort_keys=True, separators=(",", ":")); path = Path("/tmp/hue-rag-phase2-before-20260824.json"); path.write_text(raw, encoding="utf-8"); print("chunks", len(chunks)); print("sha256", hashlib.sha256(raw.encode()).hexdigest()); print("path", path)'
```

Expected: `chunks 572`, followed by a SHA-256 and the exact temporary path.
This file is evidence only and must never be added to the repository.

- [ ] **Step 4: Inspect current consumers before deleting helpers**

From the repository root:

```bash
rg -n 'parse_document|make_metadata|chunk_foods_markdown|split_text' backend notebooks --glob '*.py' --glob '*.ipynb'
```

Expected: runtime consumers outside Phase 2 use `chunk_foods_markdown()`; direct
imports of the two removable helpers are limited to the Phase 2 test file.
Record any unexpected consumer and stop before deletion if it changes scope.

---

### Task 2: Write the focused tests first

**Files:**

- Modify: `backend/tests/test_markdown_chunker.py`
- Test only: current Phase 2 runtime.

**Interfaces:**

- Consumes: public `chunk_foods_markdown()`, public `split_text()` and a small
  temporary-file discovery seam in unit tests.
- Produces: lean executable specifications for the approved contract.

- [ ] **Step 1: Replace overlapping tests with representative behaviors**

Keep one clear test for each distinct splitter behavior:

1. short text remains whole;
2. paragraphs pack and break at the target;
3. long text prefers sentence boundaries and loses no characters;
4. one long sentence breaks at whitespace, never inside a word;
5. list items and wrapped list lines stay together;
6. a Markdown table remains atomic above 400 characters.

Keep focused chunker tests for:

1. H1 supplies title, H2 supplies section and H3 stays in the body;
2. `Nguồn dữ liệu` and image-only lines are excluded;
3. title/context label and the exact seven-field metadata contract are emitted;
4. IDs and discovery order are deterministic;
5. malformed input without H1 fails with the file path;
6. input without a non-empty answer-facing H2 fails with the file path;
7. the real corpus satisfies non-empty text, exact schema, valid relative
   sources, exclusions and unique IDs.

Combine assertions that traverse the same full corpus. Do not call
`chunk_foods_markdown()` repeatedly just to test one field per pass. Do not
retain tests solely to preserve the previous count of 31.

For temporary malformed/valid files, monkeypatch only the discovery result and
then call public `chunk_foods_markdown()`. This is a unit seam, not completion
evidence. Do not add a runtime path parameter for tests.

- [ ] **Step 2: Remove imports of deleted/private helper APIs**

The final test module may import:

```python
from ingestion.chunking import markdown_chunker
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
from ingestion.helpers.split_text import split_text
```

Do not import `parse_document`, `make_metadata`, `_LIST_ITEM`, `_split_blocks`
or other splitter internals. Local test helpers may inspect returned public
chunks but must not copy runtime parsing or splitting logic.

- [ ] **Step 3: Run the new validation tests and observe RED**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m pytest tests/test_markdown_chunker.py -q --tb=short
```

Expected RED: the new missing-H1 and/or missing-answer-H2 tests fail because the
current runtime silently accepts those malformed shapes. Existing behavior
tests should pass. If failures reveal a mistaken expectation about approved
behavior, correct the test design before runtime code.

Do not weaken the ordered 572 acceptance contract to make a test pass.

---

### Task 3: Consolidate the runtime and reach GREEN

**Files:**

- Modify: `backend/ingestion/chunking/markdown_chunker.py`
- Modify only if simplification is evidence-backed:
  `backend/ingestion/helpers/split_text.py`
- Delete: `backend/ingestion/helpers/markdown_parser.py`
- Delete: `backend/ingestion/helpers/make_metadata.py`

**Interfaces:**

- Consumes: Phase 1 settings and curated Markdown files.
- Produces: the unchanged ordered `list[dict]` contract.

- [ ] **Step 1: Move parsing directly into the chunker**

Implement a small private parsing function inside `markdown_chunker.py` that:

- scans lines once;
- captures a non-empty H1 title;
- starts semantic sections only at H2;
- retains H3 and deeper Markdown inside the current H2 body;
- omits empty bodies;
- reports whether a non-empty answer-facing H2 exists.

Keep the result as ordinary tuples/dicts/lists. Do not add a parser class,
dataclass, AST or generic Markdown dependency.

- [ ] **Step 2: Add minimal per-file fail-fast checks**

For each discovered path:

- reject a missing/empty H1;
- reject a file with no non-empty H2 other than `Nguồn dữ liệu`;
- derive `source` with `path.relative_to(root)` so paths outside the KB root
  cannot silently enter metadata;
- raise a built-in `ValueError` with the relative path when available and a
  concise invariant message.

Do not validate imagined heading counts, heading characters, external URLs or
frontmatter schemas.

- [ ] **Step 3: Build metadata locally and preserve exact output**

Construct the existing mapping directly at the chunk creation point or through
one short private function:

```python
{
    "chunk_id": f"{source}|{heading}|{index}",
    "source": source,
    "title": title,
    "section": heading,
    "category": "foods",
    "subcategory": subcategory,
    "chunk_type": "section" if heading else "intro",
}
```

Keep the existing context-label mapping, `Thông tin` topic rule, image cleanup,
subcategory rule and sorted discovery unchanged. Do not change dictionary
field names or text formatting.

- [ ] **Step 4: Validate final corpus invariants directly**

Before returning from `chunk_foods_markdown()`:

- reject empty chunk text;
- require exactly the seven approved metadata keys;
- reject duplicate `chunk_id` values.

Use a short loop/set. Do not add a validator object, schema library or second
public function.

- [ ] **Step 5: Keep the splitter coherent**

Retain `split_text.py` as the only helper module. Its public behavior remains:
paragraph/sentence/whitespace preference, list-item integrity, atomic tables,
400-character default and no overlap.

Only simplify internal names or branches if the focused tests and ordered
corpus comparison prove identical behavior. Do not rewrite the algorithm merely
to make the diff larger.

- [ ] **Step 6: Delete the two absorbed modules**

Use `apply_patch` to delete:

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
```

Do not leave re-export files or deprecated wrappers.

- [ ] **Step 7: Run focused GREEN verification**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m py_compile ingestion/chunking/markdown_chunker.py ingestion/helpers/split_text.py
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m pytest tests/test_markdown_chunker.py -q --tb=short
```

Expected: compile succeeds and every focused test passes. Record the new test
count and explain that removed tests were redundant rather than hidden
failures.

- [ ] **Step 8: Prove exact ordered corpus equivalence immediately**

Use the exact baseline path recorded in Task 1:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'import hashlib, json; from pathlib import Path; from ingestion.chunking.markdown_chunker import chunk_foods_markdown; before = json.loads(Path("/tmp/hue-rag-phase2-before-20260824.json").read_text(encoding="utf-8")); after = chunk_foods_markdown(); assert len(before) == 572, len(before); assert len(after) == 572, len(after); assert before == after; raw = json.dumps(after, ensure_ascii=False, sort_keys=True, separators=(",", ":")); print("ordered_equal", True); print("chunks", len(after)); print("sha256", hashlib.sha256(raw.encode()).hexdigest())'
```

Expected: `ordered_equal True`, `chunks 572`, and the same SHA-256 recorded in
Task 1. If equality fails, inspect the first differing index and fix Phase 2;
do not proceed to downstream work or regenerate the Before file.

- [ ] **Step 9: Confirm deleted imports are gone**

From the repository root:

```bash
test ! -e backend/ingestion/helpers/markdown_parser.py
test ! -e backend/ingestion/helpers/make_metadata.py
rg -n 'markdown_parser|make_metadata|parse_document' backend notebooks --glob '*.py' --glob '*.ipynb'
```

Expected: both `test` commands exit `0`; `rg` returns no live import/reference.
Historical guides and reports are outside this scan and remain untouched.

---

### Task 4: Reduce Notebook 02 to a public-API walkthrough

**Files:**

- Modify: `notebooks/02_foods_data_and_chunking.ipynb`
- Verify only: real Phase 2 runtime and curated corpus.

**Interfaces:**

- Consumes: only `chunk_foods_markdown()` and returned chunks.
- Produces: a clean educational notebook with no runtime duplication.

- [ ] **Step 1: Replace private imports and helpers**

Remove imports/usages of:

```text
_discover_markdown_files
_is_table
_split_blocks
```

Do not replace them with copied notebook implementations. Use returned chunk
metadata/text to select examples and calculate the compact summary.

- [ ] **Step 2: Keep one short learning flow**

Organize the notebook into brief markdown explanations and short code cells:

1. add `backend/` to `sys.path` without printing an absolute path;
2. import `chunk_foods_markdown()` and create `chunks` once;
3. show chunk count, distinct source count and the seven metadata keys;
4. display one ordinary text chunk;
5. display one chunk containing a Markdown table with `IPython.display.Markdown`;
6. display one `subcategory == "guide"` example;
7. explain H1/H2 context, the 400-character body target, atomic table exception
   and why preview display does not alter stored text.

Do not turn the final cell into a validation gate; formal assertions remain in
pytest and the Reviewer comparison.

- [ ] **Step 3: Sanitize the repository notebook**

Ensure every code cell has:

```json
"execution_count": null,
"outputs": []
```

Ensure there is no secret, environment dump, live provider call, Qdrant call,
web call, raw private absolute path or sensitive stack trace.

- [ ] **Step 4: Execute a temporary copy**

From the repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run jupyter nbconvert --execute --to notebook notebooks/02_foods_data_and_chunking.ipynb --output /tmp/02_foods_data_and_chunking-phase2-review.ipynb --ExecutePreprocessor.timeout=600
```

Expected: nbconvert exits `0` using the real curated corpus. Inspect the
temporary output for the 572 count and the three intentional examples. Do not
copy execution outputs back into the repository notebook.

- [ ] **Step 5: Verify notebook cleanliness**

```bash
jq -e 'all(.cells[] | select(.cell_type == "code"); .execution_count == null and (.outputs | length == 0))' notebooks/02_foods_data_and_chunking.ipynb
rg -n '/home/|API_KEY|OPENAI_API_KEY|OPENROUTER_API_KEY|_discover_markdown_files|_is_table|_split_blocks' notebooks/02_foods_data_and_chunking.ipynb
```

Expected: `jq` returns `true`; `rg` returns no match.

---

### Task 5: Run downstream verification and write the Implementer handoff

**Files:**

- Create:
  `reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md`
- Verify only: downstream Phase 3–7 runtime/tests.

**Interfaces:**

- Consumes: simplified Phase 2 output through existing consumers.
- Produces: fresh evidence and a scoped downstream-impact handoff.

- [ ] **Step 1: Reconfirm the active collection is read-only**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s = load_settings(); c = client_from_settings(s); n = s["vector_database"]["collection_name"]; print("active_collection", n, "points", c.count(n, exact=True).count)'
```

Expected current state:

```text
active_collection hue_foods_e5_small_384 points 572
```

If the name/count differs, record the actual read-only observation and stop to
ask the Reviewer before any Qdrant action.

- [ ] **Step 2: Run affected downstream smoke tests**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_hybrid_index.py tests/test_startup.py tests/test_api_chat.py -q --tb=short
```

Expected: all selected tests pass. Record exact counts, warnings, external
service/model observations and any isolated test collection names. Do not
weaken downstream assertions or edit their owning files.

Classify each failure before acting:

- Phase 2 regression: return to Task 3 and restore compatibility;
- pre-existing Phase 3–7 issue: record evidence and owning phase, do not fix;
- uncertain ingestion compatibility: ask the Reviewer whether to use the
  user-authorized isolated real Qdrant collection.

- [ ] **Step 3: Run the full backend suite**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
```

Historical pre-change baseline is `222 passed, 4 warnings`. The final collected
test count may be lower because redundant Phase 2 tests are intentionally
consolidated. Acceptance requires that every retained test passes and that no
test outside `test_markdown_chunker.py` was removed or weakened. Record the
exact fresh result.

- [ ] **Step 4: Re-run the strongest Phase 2 gates after the full suite**

Repeat:

```text
focused Phase 2 pytest
ordered Before/After equality command
repository Notebook 02 cleanliness checks
active collection read-only count
```

Expected: all still pass; ordered equality remains true; active collection is
unchanged.

- [ ] **Step 5: Inspect the final scoped diff**

From the repository root:

```bash
git diff --check
git diff --stat -- backend/ingestion/chunking/markdown_chunker.py backend/ingestion/helpers/markdown_parser.py backend/ingestion/helpers/make_metadata.py backend/ingestion/helpers/split_text.py backend/tests/test_markdown_chunker.py notebooks/02_foods_data_and_chunking.ipynb reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md
git diff -- backend/ingestion/chunking/markdown_chunker.py backend/ingestion/helpers/markdown_parser.py backend/ingestion/helpers/make_metadata.py backend/ingestion/helpers/split_text.py backend/tests/test_markdown_chunker.py
rg -n '^(<<<<<<<|=======|>>>>>>>)' backend notebooks reports docs
git status --short
```

Expected: only approved Phase 2 implementation files and the new Implementer
report appear in the scoped diff. Existing unrelated user changes remain
untouched. There are no whitespace errors or merge markers.

- [ ] **Step 6: Write the six-section implementation report**

Create
`reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md`
with concise sections:

1. **Scope implemented** — files modified/deleted and deliberate non-goals.
2. **Before/After** — four runtime modules to two; old/new focused test count;
   Notebook 02 private imports removed.
3. **Ordered corpus equivalence** — temporary baseline path, both SHA-256
   values, `572`, and direct ordered equality result.
4. **Verification evidence** — exact commands and observed focused, notebook,
   downstream, full-suite and active-collection results.
5. **Downstream impact** — a table with affected phase, dependency, observed
   evidence, concrete impact, later action and approval blocker. State `none
   observed` explicitly if the table is empty.
6. **Limitations and Reviewer handoff** — external conditions, conditional
   Qdrant decision, preserved unrelated changes and exact items Reviewer must
   independently rerun.

Do not claim a command passed unless it was executed in this implementation.
Do not paste secrets, raw provider payloads, full knowledge-base bodies or the
temporary 572-chunk JSON into the report.

- [ ] **Step 7: Stop for independent review**

Do not edit the design, canonical guide, Project Status, Codex review or user
report. Do not stage, commit or push. Hand the exact diff and fresh evidence to
the Reviewer.

## Reviewer checkpoint

The Reviewer independently:

1. checks implementation scope and deleted imports;
2. confirms the Before baseline predates runtime edits;
3. reruns direct ordered equality over all 572 chunks;
4. audits that validation covers only real contracts;
5. runs Notebook 02 from a temporary copy;
6. runs downstream and full-suite verification in proportion to observed risk;
7. confirms the active collection remained unchanged;
8. records downstream effects without fixing Phase 3–7;
9. asks the user for final Phase 2 simplicity approval.

Phase 2 does not become simplicity-approved from the Implementer report alone.

## Completion conditions

The Implementer handoff is ready only when:

1. the approved two-module runtime structure exists;
2. all focused tests are green after an observed RED validation failure;
3. all 572 chunks match the Before baseline in exact order, text and metadata;
4. Notebook 02 uses only the public runtime API and executes successfully;
5. downstream smoke and full backend suites have fresh recorded results;
6. the active collection was not mutated;
7. no Phase 3–7 code was changed and no new regression was deferred;
8. the six-section report is factual and complete;
9. unrelated worktree changes remain intact.

No commit or push is authorized by this plan.
