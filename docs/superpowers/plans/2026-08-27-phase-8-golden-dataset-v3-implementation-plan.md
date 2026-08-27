# Phase 8 Golden Dataset V3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and obtain user/Reviewer approval for a 40-, 45-, or 50-case Vietnamese Golden Dataset V3 plus an exact 10-case smoke subset, using natural tourist questions and canonical Markdown evidence.

**Architecture:** Preserve V2 and add a small V3-specific validation path beside the existing validator. Curate V2 first, establish a quality-approved 40-case baseline, and expand only through explicit five-case gates to 45 and 50. Use deterministic code for structural/evidence checks and full human review for naturalness, tourist likelihood, semantic duplication, and final size.

**Tech Stack:** Python 3.11+, Pydantic v2, pytest, JSONL, Markdown H2 evidence, the existing ingestion/retrieval service, Qdrant isolated test collections.

## Global Constraints

- Canonical design: `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md`.
- Full size must be exactly one of `{40, 45, 50}`; prefer `50 -> 45 -> 40` only while every case passes manual review.
- Full IDs are sequential `foods-v3-0001` through the selected final size.
- Schema is exactly `case_id`, `question`, `keywords`, `reference_answer`, `category`, `evidence`.
- Questions are natural Vietnamese, single-turn, standalone, common, clear, and plausible for tourists visiting Hue.
- Do not author direct price-only or opening-time-only questions.
- Keep all nine existing category names, with no category quota or minimum.
- Source-family numbers and the tourist-needs checklist are qualitative only; code must not enforce them.
- Web search supports research and conflict detection only; unindexed URLs are not Golden evidence.
- New web-discovered knowledge requires a separately approved Markdown update and index before use.
- Evidence is the minimal sufficient canonical `source + H2 section` mapping.
- Keywords number two to four, appear in `reference_answer`, and are not retrieval ground truth.
- Smoke is exactly 10 full rows copied unchanged after full V3 approval; it has no coverage quota.
- Preserve V2 and Phase 7 datasets and their historical validation behavior.
- Active Qdrant collection `hue_foods_e5_small_384` is read-only.
- Use real corpus, real ingestion, and real retrieval for completion evidence; no fake, mock, replay, or fabricated completion output.
- Keep code direct and readable; do not add a semantic judge, annotation platform, registry, manifest, resume engine, or audit framework.
- Do not run Phase 8 model comparison, paid generation, paid judging, production cutover, or active-collection mutation.
- Do not stage, commit, or push unless the user separately authorizes it.

---

## File map

| File | Responsibility |
|---|---|
| `backend/evaluation/golden_dataset.py` | Preserve V2 validation and add the minimal V3 full/smoke validators and V3 paths. |
| `backend/tests/test_evaluation.py` | Focused deterministic V3 contract, smoke, and real retrieval-metadata verification. |
| `knowledge-base-hue/foods/evaluation/golden_v3.jsonl` | User- and Reviewer-approved full V3 dataset. |
| `knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl` | Ten exact rows copied from approved full V3. |
| `reports/phase_8_golden_dataset_v3_implementation_report.md` | Commands, outcomes, counts, conflicts, manual-audit evidence, proposed size, and approval status. |
| `session_prompt/Project_Status.md` | Current Gate 0 status and exact next handoff after V3 review. |
| `session_prompt/Session_Prompt.md` | Current scope, authoritative artifacts, and prohibition on Phase 8 benchmark execution before approval. |

No source Markdown file is pre-authorized for modification by this plan. If web
research discovers missing knowledge, stop and request a separate exact corpus
change before authoring the affected case.

---

### Task 1: Add the minimal V3 validator contract

**Files:**
- Modify: `backend/evaluation/golden_dataset.py:9-233`
- Modify: `backend/tests/test_evaluation.py:13-27`
- Test: `backend/tests/test_evaluation.py`

**Interfaces:**
- Consumes: existing `GoldenCase`, `load_golden`, `_evidence_text`,
  `_source_family`, `_raise_issues`, and `document_is_relevant`.
- Produces: `V3_FULL_PATH`, `V3_SMOKE_PATH`, `ALLOWED_CATEGORIES`,
  `V3_ALLOWED_COUNTS`, `validate_v3_full(cases: list[GoldenCase]) -> dict`, and
  `validate_v3_smoke(full: list[GoldenCase], smoke: list[GoldenCase]) -> dict`.
- Preserves: existing `validate_full` and `validate_smoke` behavior for V2.

- [ ] **Step 1: Add imports and failing V3 error-path tests**

Extend the import block in `backend/tests/test_evaluation.py` with:

```python
from evaluation.golden_dataset import (
    ALLOWED_CATEGORIES,
    CATEGORY_QUOTAS,
    SOURCE_TARGETS,
    V3_ALLOWED_COUNTS,
    document_is_relevant,
    load_golden,
    validate_full,
    validate_smoke,
    validate_v3_full,
    validate_v3_smoke,
)
```

Add these tests before the file-backed Golden tests:

```python
def test_golden_v3_rejects_a_full_size_outside_approved_levels():
    assert V3_ALLOWED_COUNTS == {40, 45, 50}
    with pytest.raises(ValueError, match="expected 40, 45, or 50 cases"):
        validate_v3_full([])


def test_golden_v3_smoke_requires_exactly_ten_rows():
    with pytest.raises(ValueError, match="expected 10 smoke cases"):
        validate_v3_smoke([], [])


def test_golden_v3_keeps_the_nine_diagnostic_category_names_without_quotas():
    assert ALLOWED_CATEGORIES == set(CATEGORY_QUOTAS)
```

Also add `import pytest` near the existing standard-library imports.

- [ ] **Step 2: Run the focused tests and verify RED**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v3_rejects or golden_v3_smoke_requires or golden_v3_keeps'
```

Expected: collection/import ERROR because the V3 names do not exist yet.

- [ ] **Step 3: Add V3 constants without redefining V2**

Add the path/ID/count constants beside the existing V2 path constants in
`backend/evaluation/golden_dataset.py`:

```python
V3_FULL_PATH = KB_ROOT / "foods" / "evaluation" / "golden_v3.jsonl"
V3_SMOKE_PATH = KB_ROOT / "foods" / "evaluation" / "golden_v3_smoke.jsonl"
V3_CASE_ID = re.compile(r"foods-v3-\d{4}")
V3_ALLOWED_COUNTS = {40, 45, 50}
```

Add the category-name set immediately after the complete `CATEGORY_QUOTAS`
dictionary so it cannot be evaluated before that dictionary exists:

```python
ALLOWED_CATEGORIES = set(CATEGORY_QUOTAS)
```

Do not remove `CATEGORY_QUOTAS`, `SOURCE_TARGETS`, `FULL_PATH`, `SMOKE_PATH`, or
the V2 functions because V2 remains historical and testable.

- [ ] **Step 4: Add basic normalization and the V3 full validator**

Add after `_raise_issues`:

```python
def _normalize_question(question: str) -> str:
    return re.sub(r"\s+", " ", question.strip().casefold())


def validate_v3_full(cases: list[GoldenCase]) -> dict:
    issues: list[str] = []
    count = len(cases)
    if count not in V3_ALLOWED_COUNTS:
        issues.append(f"expected 40, 45, or 50 cases, found {count}")

    expected_ids = [f"foods-v3-{index:04d}" for index in range(1, count + 1)]
    actual_ids = [case.case_id for case in cases]
    if actual_ids != expected_ids:
        issues.append("case IDs must be sequential foods-v3-0001.. in file order")

    normalized_questions = [_normalize_question(case.question) for case in cases]
    if len(set(normalized_questions)) != len(normalized_questions):
        issues.append("questions must be unique after whitespace/case normalization")

    category_counts = Counter(case.category for case in cases)
    source_coverage: Counter[str] = Counter()
    for case in cases:
        if not V3_CASE_ID.fullmatch(case.case_id):
            issues.append(f"invalid V3 case_id: {case.case_id}")
        if not case.question.strip():
            issues.append(f"{case.case_id}: question is empty")
        if not case.reference_answer.strip():
            issues.append(f"{case.case_id}: reference_answer is empty")
        if case.category not in ALLOWED_CATEGORIES:
            issues.append(f"{case.case_id}: invalid category {case.category}")

        _, families = _evidence_text(case, issues)
        for family in families:
            source_coverage[family] += 1

        for keyword in case.keywords:
            normalized = keyword.strip().casefold()
            if not normalized:
                issues.append(f"{case.case_id}: keyword is empty")
            elif normalized not in case.reference_answer.casefold():
                issues.append(f"{case.case_id}: keyword {keyword!r} missing from reference")

    _raise_issues(issues)
    return {
        "cases": count,
        "categories": dict(category_counts),
        "source_coverage": dict(source_coverage),
    }
```

This deliberately does not compare category or source counts to quotas and does
not require keyword substrings in evidence.

- [ ] **Step 5: Add the simple V3 smoke validator**

Add after `validate_v3_full`:

```python
def validate_v3_smoke(full: list[GoldenCase], smoke: list[GoldenCase]) -> dict:
    issues: list[str] = []
    if len(smoke) != 10:
        issues.append(f"expected 10 smoke cases, found {len(smoke)}")

    full_by_id = {case.case_id: case for case in full}
    smoke_ids = [case.case_id for case in smoke]
    if len(set(smoke_ids)) != len(smoke_ids):
        issues.append("smoke case IDs must be unique")

    for case in smoke:
        full_case = full_by_id.get(case.case_id)
        if full_case is None:
            issues.append(f"smoke case missing from full: {case.case_id}")
        elif case.model_dump() != full_case.model_dump():
            issues.append(f"smoke row differs from full: {case.case_id}")

    _raise_issues(issues)
    return {"cases": len(smoke)}
```

Do not add category or source-family coverage rules to this function.

- [ ] **Step 6: Run the focused tests and verify GREEN**

Run the same focused command from Step 2.

Expected: `3 passed` and no network/model calls.

- [ ] **Step 7: Run the existing V2 contract tests**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v2_contract or golden_v2_smoke'
```

Expected: the existing V2 tests PASS unchanged. Record the exact count and
outcome; do not claim V3 completion from these unit tests.

- [ ] **Step 8: Reviewer checkpoint**

Show the focused diff and test outputs. Confirm explicitly that the V3 validator
contains no category quota, source quota, checklist quota, semantic judge, or
keyword-in-evidence substring rule.

---

### Task 2: Curate the first 40 high-quality cases

**Files:**
- Read: `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`
- Read: `knowledge-base-hue/foods/restaurants/*.md`
- Read: `knowledge-base-hue/foods/cafes/*.md`
- Read: `knowledge-base-hue/foods/local_specialties/*.md`
- Read: `knowledge-base-hue/foods/food-guides.md`
- Create: `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`
- Create: `reports/phase_8_golden_dataset_v3_implementation_report.md`

**Interfaces:**
- Consumes: the approved V3 design and `GoldenCase` six-field schema.
- Produces: a real 40-row `golden_v3.jsonl` candidate and an implementation
  report containing aggregate reuse decisions, research boundary, conflicts,
  commands, and the current approval state.

- [ ] **Step 1: Confirm the source corpus and historical inputs are unchanged**

Run from the repository root:

```bash
git status --short
find knowledge-base-hue/foods/restaurants -maxdepth 1 -type f -name '*.md' | sort
find knowledge-base-hue/foods/cafes -maxdepth 1 -type f -name '*.md' | sort
find knowledge-base-hue/foods/local_specialties -maxdepth 1 -type f -name '*.md' | sort
wc -l knowledge-base-hue/foods/evaluation/golden_v2.jsonl
```

Expected: preserve all unrelated changes; V2 has 100 rows; no command writes to
the active collection or historical dataset.

- [ ] **Step 2: Review every V2 row against one exact manual rubric**

For each V2 row, inspect the complete declared Markdown H2 section and decide:

```text
KEEP     — already satisfies every V3 question/answer/evidence rule
REWRITE  — intent is useful but wording, answer, keywords, category, or evidence needs correction
REJECT   — forced, duplicated, low-likelihood, unsupported, price-only, or time-only
```

Apply all seven checks before KEEP:

```text
tourist-plausible
standalone and focused
natural non-promotional Vietnamese
not a semantic/template duplicate
direct concise useful reference answer
all answer claims evidence-supported
minimal sufficient evidence
```

Do not persist a separate annotation database. Keep running counts for the
implementation report: `kept`, `rewritten`, `rejected`, and later `new`.

- [ ] **Step 3: Use web research only for the approved purposes**

Search common Hue travel/food-guide language and check material conflicts. Do
not copy publisher names into questions and do not declare URLs as evidence.

If a desirable fact is absent from the indexed Markdown, record:

```text
proposed fact
web source URL and access date
target Markdown file and H2 section
candidate question blocked by the missing corpus fact
```

Then stop that candidate and request approval. Do not edit or ingest the corpus
under this plan.

- [ ] **Step 4: Author the strongest 40 rows**

Write the selected JSONL rows and number them in file order as
`foods-v3-0001` through `foods-v3-0040`. Each line must have the six fields in
the approved schema.

For every row:

- use one primary tourist intent and at most one related condition;
- assign a category only after the question is accepted;
- choose two to four concrete keywords present in the reference answer;
- write a normally two-to-four-sentence answer with the direct answer first;
- declare the smallest source/H2 set that supports every claim;
- omit any claim found only on the web;
- reject the row instead of weakening the quality rubric.

Do not write direct price-only or opening-time-only questions. Do not try to
reach source-family or category counts.

- [ ] **Step 5: Add the real file-backed V3 contract test**

Add paths near the V2 paths in `backend/tests/test_evaluation.py`:

```python
GOLDEN_V3 = REPO / "knowledge-base-hue/foods/evaluation/golden_v3.jsonl"
GOLDEN_V3_SMOKE = REPO / "knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl"
```

Add:

```python
def test_golden_v3_contract_uses_an_approved_size_without_distribution_quotas():
    cases = load_golden(GOLDEN_V3)
    summary = validate_v3_full(cases)
    assert summary["cases"] in V3_ALLOWED_COUNTS
    assert sum(summary["categories"].values()) == summary["cases"]
    assert set(summary["categories"]) <= ALLOWED_CATEGORIES
```

- [ ] **Step 6: Validate the real 40-row file**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py::test_golden_v3_contract_uses_an_approved_size_without_distribution_quotas \
  -q --tb=short
```

Expected: `1 passed`, with all evidence files and H2 sections resolved from the
real corpus.

- [ ] **Step 7: Perform the 40-row manual audit**

Read all 40 complete rows in file order. For each row, re-open all declared H2
sections and apply the seven-check rubric from Step 2. Then inspect the set for:

- semantic duplicates;
- repeated question templates;
- excessive focus on one venue, dish, category, or source family;
- publisher/SEO language;
- multi-part questions;
- answer claims not supported by evidence;
- direct price-only or opening-time-only questions.

Correct or remove failures before the checkpoint. Never add a weak replacement
merely to return to 40; if fewer than 40 cases remain, report the blocker because
40 is the approved minimum.

- [ ] **Step 8: Record and present the 40-case checkpoint**

In the implementation report record:

- full size and category/source-family counts as observations, not targets;
- aggregate `kept`, `rewritten`, `new`, and `rejected` V2 decisions;
- all material corpus/web conflicts and blocked candidates;
- validator command and exact real outcome;
- explicit statement that naturalness remains pending Reviewer/user review.

Treat this as an Implementer quality checkpoint and make the 40 questions
available for inspection. The Implementer may continue to the 45-case gate
without asking the user to approve an intermediate dataset; the mandatory
Reviewer/user content decision applies to the final proposed size.

---

### Task 3: Evaluate the optional 45- and 50-case quality gates

**Files:**
- Modify conditionally: `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`
- Modify: `reports/phase_8_golden_dataset_v3_implementation_report.md`

**Interfaces:**
- Consumes: the validated and manually accepted 40-case baseline.
- Produces: a proposed final full size of exactly 40, 45, or 50 with explicit
  Reviewer/user decision points.

- [ ] **Step 1: Find five passing additions for the 45-case gate**

Assess candidates only for meaningful tourist needs not adequately represented
in the 40-case baseline. Each candidate must independently pass all seven manual
checks and the anti-template review.

If at least five strong additions pass, append the best five and renumber the
file sequentially through `foods-v3-0045`. If fewer than five pass, keep the
40-row file and propose 40 as final. Do not substitute weaker candidates to
make the gate pass and do not build a candidate pool beyond the 50-case ceiling.

- [ ] **Step 2: Validate and review the 45-row state when it exists**

Run the real V3 contract test from Task 2 Step 6. Expected: `1 passed` and
`summary["cases"] == 45` when inspected. Present all five additions plus the
updated full question list to Reviewer/user.

- [ ] **Step 3: Find five passing additions for the 50-case gate after the 45-row state passes internal audit**

Apply the same process. If at least five strong additions pass, append the best
five and renumber through `foods-v3-0050`. Otherwise keep the internally
accepted 45-row file and propose 45 as final. Never skip directly from 40 to 50.

- [ ] **Step 4: Validate and review the 50-row state when it exists**

Run the real V3 contract test from Task 2 Step 6. Expected: `1 passed` and
`summary["cases"] == 50` when inspected. Present all five additions plus the
updated full question list to Reviewer/user.

- [ ] **Step 5: Freeze the user- and Reviewer-approved full file**

Record the exact chosen size and approval outcome in the implementation report.
Do not create smoke, run real retrieval verification, or claim completion until
the user confirms they have read the full question list and accepted the final
40-, 45-, or 50-row content.

---

### Task 4: Create the exact 10-row smoke subset

**Files:**
- Read: `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`
- Create: `knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl`
- Modify: `backend/tests/test_evaluation.py`
- Modify: `reports/phase_8_golden_dataset_v3_implementation_report.md`

**Interfaces:**
- Consumes: the frozen user-approved full V3 file.
- Produces: ten distinct rows that are byte-for-content copies at the parsed
  model level and `validate_v3_smoke(...) == {"cases": 10}`.

- [ ] **Step 1: Select ten strong rows simply**

Choose ten full rows with reasonable ordinary variety. Do not calculate a
coverage score, enforce all categories/source families, or add selection code.
Preserve their full-file order.

- [ ] **Step 2: Copy the ten complete JSON lines**

Copy each selected line unchanged into
`knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl`. Do not reconstruct
or edit fields in the smoke file.

- [ ] **Step 3: Add the real smoke-subset test**

Add to `backend/tests/test_evaluation.py`:

```python
def test_golden_v3_smoke_is_an_exact_ten_row_subset():
    full = load_golden(GOLDEN_V3)
    smoke = load_golden(GOLDEN_V3_SMOKE)
    assert validate_v3_smoke(full, smoke) == {"cases": 10}
```

- [ ] **Step 4: Run the focused smoke test**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py::test_golden_v3_smoke_is_an_exact_ten_row_subset \
  -q --tb=short
```

Expected: `1 passed` using the real full and smoke JSONL files.

- [ ] **Step 5: Record the smoke IDs and outcome**

Add the ten IDs, the exact command, and exact PASS/FAIL outcome to the
implementation report. Do not describe smoke as a quality benchmark.

---

### Task 5: Verify real retrieval metadata on the isolated collection

**Files:**
- Modify: `backend/tests/test_evaluation.py`
- Modify: `reports/phase_8_golden_dataset_v3_implementation_report.md`

**Interfaces:**
- Consumes: `GOLDEN_V3_SMOKE`, `build_services`, `document_is_relevant`, and the
  existing real `ingested_collection` fixture/`TEST_COLLECTION` boundary.
- Produces: observed real retrieval metadata and Boolean exact source/section
  relevance for all 10 smoke questions.

- [ ] **Step 1: Add the V3 real metadata test**

Add beside the existing V2 integration test:

```python
def test_golden_v3_binary_relevance_uses_real_retrieval_metadata(ingested_collection):
    from conftest import TEST_COLLECTION

    smoke = load_golden(GOLDEN_V3_SMOKE)
    assert len(smoke) == 10
    services = build_services("dense_only", collection_name=TEST_COLLECTION)

    for case in smoke:
        documents = services.retrieval.search(case.question)
        assert len(documents) > 0
        for document in documents:
            assert isinstance(document.metadata.get("source"), str)
            assert document.metadata["source"].startswith("foods/")
            assert isinstance(document.metadata.get("section"), str)
            assert isinstance(document_is_relevant(case, document), bool)
```

This test verifies real metadata plumbing. It does not require every gold section
to rank successfully and does not rewrite Golden evidence around baseline
retrieval misses.

- [ ] **Step 2: Run the real isolated integration test**

Run from `backend/`:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache \
  uv run --env-file ../.env python -m pytest \
  tests/test_evaluation.py::test_golden_v3_binary_relevance_uses_real_retrieval_metadata \
  -q --tb=short -s
```

Expected: PASS using the isolated fixture collection. If a service or dependency
fails, report the real failure and use `systematic-debugging`; do not replace it
with a fake test.

- [ ] **Step 3: Record observed retrieval misses separately from gold defects**

For each smoke case, record whether any returned document matched exact
`source + section`. A miss is baseline retrieval evidence, not automatic proof
that the Golden row is wrong. Correct a row only when manual source review finds
an actual annotation defect.

- [ ] **Step 4: Confirm active collection non-mutation**

Record the fixture collection name and cleanup outcome from the real test.
Confirm that `hue_foods_e5_small_384` was not written, recreated, or deleted.

---

### Task 6: Run final focused verification and hand off to Reviewer

**Files:**
- Modify: `reports/phase_8_golden_dataset_v3_implementation_report.md`
- Modify: `session_prompt/Project_Status.md`
- Modify: `session_prompt/Session_Prompt.md`

**Interfaces:**
- Consumes: approved full/smoke files and completed focused tests.
- Produces: exact review evidence and a Reviewer handoff while keeping Phase 8
  `not_ready` until review approval.

- [ ] **Step 1: Run deterministic V3 tests together**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v3 and not binary_relevance'
```

Expected: all selected V3 deterministic tests PASS against the final real files.

- [ ] **Step 2: Re-run the isolated real metadata test**

Run the exact Task 5 Step 2 command. Expected: PASS with the real retrieval
service and isolated collection.

- [ ] **Step 3: Re-run the V2 contract tests as a regression guard**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v2_contract or golden_v2_smoke'
```

Expected: existing V2 contract tests PASS, proving V3 did not redefine the
historical V2 validator.

- [ ] **Step 4: Complete the implementation report**

The report must state:

- final row count and user/Reviewer approval state;
- a direct link to the full dataset and confirmation that the final handoff
  rendered a numbered question-only list for user review, without duplicating
  every full JSONL row in the permanent report;
- observed category and source-family counts, explicitly labeled non-quota;
- aggregate V2 kept/rewritten/new/rejected counts;
- web research performed and any corpus additions separately approved;
- conflicts, blocked candidates, and limitations;
- smoke IDs;
- exact commands and unedited PASS/FAIL outcomes;
- isolated collection name and cleanup result;
- confirmation that V2, Phase 7 data, and active Qdrant were not mutated;
- confirmation that no Phase 8 model benchmark or paid evaluation ran.

- [ ] **Step 5: Update governance without claiming approval prematurely**

Update `Project_Status.md` and `Session_Prompt.md` with:

```text
Golden Dataset V3 implementation: handed off for Reviewer verification
Phase 8: not_ready
Next action: Reviewer reads all V3 rows, checks exact evidence and real command outcomes,
then requests user approval or changes
```

Only after the Reviewer and user approve may governance say Golden Dataset V3
is approved and unblock the next Phase 8 design gate.

- [ ] **Step 6: Perform the final self-review**

Check the complete diff for:

- accidental changes to V2 or Phase 7 datasets;
- category/source quotas reintroduced in code or tests;
- direct price-only/opening-time-only questions;
- repeated question templates and semantic duplicates;
- unsupported answer claims;
- smoke rows that differ from full;
- fake/mock/replay completion evidence;
- active collection mutation;
- benchmark or paid-run scope creep.

Hand off exact findings and remaining risks. Stop; do not begin Phase 8 model
benchmark execution.

---

## Reviewer acceptance checklist

- [ ] User confirmed they read every final V3 question.
- [ ] Final full size is exactly 40, 45, or 50 and is the highest defensible
  quality level.
- [ ] Every row follows the six-field schema and sequential V3 ID contract.
- [ ] Every question passes the seven manual quality checks.
- [ ] No source/category/checklist quota influenced authoring.
- [ ] All reference-answer claims are supported by declared Markdown evidence.
- [ ] Web URLs were not used as unindexed Golden evidence.
- [ ] Full and smoke deterministic validators pass on real files.
- [ ] Smoke contains exactly 10 deep-equal full rows.
- [ ] Real retrieval metadata verification passed on an isolated collection.
- [ ] Retrieval misses were reported rather than hidden by changing gold.
- [ ] V2, Phase 7 data, and active Qdrant remained unchanged.
- [ ] No Phase 8 model benchmark, paid evaluation, production change, staging,
  commit, or push occurred without separate authorization.
