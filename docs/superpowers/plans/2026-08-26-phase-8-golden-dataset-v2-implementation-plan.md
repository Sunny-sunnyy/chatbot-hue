# Phase 8 Golden Dataset V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch subagents unless the user explicitly asks for delegation.

**Goal:** Build and verify a new 100-case Vietnamese golden dataset plus an exact 20-case smoke subset, with source/section evidence suitable for deterministic Phase 8 retrieval evaluation.

**Architecture:** Preserve the Phase 7 dataset unchanged. Add one strict, readable validation module for the two V2 JSONL files, curate cases directly from the four approved corpus families, and reuse the production dense retriever only for a final real metadata/relevance smoke check.

**Tech Stack:** Python 3.13, `uv`, Pydantic, JSONL, Markdown H2 headings, pytest, existing Hue ingestion/retrieval services and Qdrant.

## Global Constraints

- Canonical spec: `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`.
- Keep `knowledge-base-hue/foods/evaluation/tests.jsonl` and `test2.jsonl` unchanged.
- Full V2 contains exactly 100 answerable cases; smoke contains 20 deep-equal rows selected from full V2.
- Use exactly the nine category counts and source targets in the spec.
- Every case has exactly `case_id`, `question`, `keywords`, `reference_answer`, `category`, and `evidence`.
- Questions must be clear, natural and grounded; no trick questions, forced quota fillers, unsupported inference or live/latest claims.
- Treat the curated Markdown corpus as closed-world truth. Stop and report conflicts or insufficient source material; do not guess.
- Retrieval relevance is binary exact `source + section`; do not use keyword substring or an LLM judge as Phase 8 relevance ground truth.
- Do not add run IDs, timestamps, checksums, registries, annotation tools, semantic validators or LLM labeling machinery.
- Do not mutate the active Qdrant collection.
- Do not use fake data, mocked provider responses, replayed output or fabricated results as implementation or evidence.
- Unit/structural tests use the real V2 files. Final verification uses the real corpus, production chunk metadata and real Qdrant retrieval.
- Preserve unrelated dirty-worktree changes. Use `apply_patch`; do not reset, checkout, stage, commit or push.
- End each task with `git diff --check` and a reviewer checkpoint.

---

## Locked file map

| Path | Responsibility |
|---|---|
| `knowledge-base-hue/foods/evaluation/golden_v2.jsonl` | The approved 100-case full dataset |
| `knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl` | Twenty rows copied unchanged from full V2 |
| `backend/evaluation/golden_dataset.py` | Strict V2 schema, structural/evidence validation and binary relevance helper |
| `backend/evaluation/test.py` | Load `case_id` and optional V2 `evidence` without breaking Phase 7 files |
| `backend/tests/test_evaluation.py` | Focused real-data tests for full/smoke loading, validation and relevance metadata |
| `reports/phase_8_golden_dataset_v2_implementation_report.md` | Concise implementation evidence, conflicts and reviewer decisions |

No existing Phase 7 CSV, judge calibration file or answer subset is regenerated.

---

### Task 1: Add the strict V2 contract and validator

**Files:**
- Create: `backend/evaluation/golden_dataset.py`
- Modify: `backend/evaluation/test.py`
- Modify: `backend/tests/test_evaluation.py`

**Interfaces:**
- Produces: `GoldenCase`, `load_golden(path)`, `validate_full(cases)`, `validate_smoke(full, smoke)`, `document_is_relevant(case, document)`.
- Consumes: runtime document metadata fields `source` and `section` from `RetrievedDocument`.

- [ ] **Step 1: Write failing real-data contract tests**

Add these imports/constants and tests to `backend/tests/test_evaluation.py`:

```python
from evaluation.golden_dataset import (
    CATEGORY_QUOTAS,
    SOURCE_TARGETS,
    document_is_relevant,
    load_golden,
    validate_full,
    validate_smoke,
)

GOLDEN_V2 = REPO / "knowledge-base-hue/foods/evaluation/golden_v2.jsonl"
GOLDEN_V2_SMOKE = REPO / "knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl"


def test_golden_v2_contract_and_distribution():
    cases = load_golden(GOLDEN_V2)
    summary = validate_full(cases)
    assert summary["cases"] == 100
    assert summary["categories"] == CATEGORY_QUOTAS
    assert all(
        summary["source_coverage"][family] >= target
        for family, target in SOURCE_TARGETS.items()
    )


def test_golden_v2_smoke_is_exact_representative_subset():
    full = load_golden(GOLDEN_V2)
    smoke = load_golden(GOLDEN_V2_SMOKE)
    summary = validate_smoke(full, smoke)
    assert summary == {"cases": 20, "categories": 9, "source_families": 4}
```

- [ ] **Step 2: Run the focused tests and observe the expected failure**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run python -m pytest tests/test_evaluation.py -q --tb=short
```

Expected: collection fails because `evaluation.golden_dataset` and the V2 files do not exist.

- [ ] **Step 3: Extend the simple loader compatibly**

Change `backend/evaluation/test.py` to keep Phase 7 working while exposing V2 fields:

```python
from pydantic import BaseModel, Field


class TestQuestion(BaseModel):
    case_id: str = ""
    question: str
    keywords: list[str]
    reference_answer: str
    category: str
    evidence: dict[str, list[str]] = Field(default_factory=dict)
```

Keep `load_tests()` and `DEFAULT_TEST_FILE` behavior unchanged. Pydantic continues to ignore the old `relevant_sources` and `relevant_sections` fields in Phase 7 rows.

- [ ] **Step 4: Implement the strict validator without a framework**

Create `backend/evaluation/golden_dataset.py` with the complete implementation below:

```python
import re
from collections import Counter
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from core.schema import RetrievedDocument

REPO_ROOT = Path(__file__).resolve().parents[2]
KB_ROOT = (REPO_ROOT / "knowledge-base-hue").resolve()
FULL_PATH = KB_ROOT / "foods" / "evaluation" / "golden_v2.jsonl"
SMOKE_PATH = KB_ROOT / "foods" / "evaluation" / "golden_v2_smoke.jsonl"
CASE_ID = re.compile(r"foods-\d{4}")

CATEGORY_QUOTAS = {
    "direct_fact": 18,
    "temporal": 10,
    "comparative": 10,
    "numerical": 8,
    "relationship": 12,
    "spanning": 12,
    "holistic": 8,
    "food_knowledge": 12,
    "guide_planning": 10,
}
SOURCE_TARGETS = {
    "restaurants": 40,
    "cafes": 20,
    "local_specialties": 20,
    "guide": 20,
}
GENERIC_KEYWORDS = {"huế", "quán", "món", "giá", "ở đâu", "ngon", "ăn", "gì", "nào"}


class GoldenCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    question: str
    keywords: list[str] = Field(min_length=2, max_length=4)
    reference_answer: str
    category: str
    evidence: dict[str, list[str]]


def load_golden(path: str | Path) -> list[GoldenCase]:
    cases = []
    with Path(path).open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                cases.append(GoldenCase.model_validate_json(line))
            except Exception as exc:
                raise ValueError(f"invalid golden row at line {line_number}") from exc
    return cases


def _source_path(source: str) -> Path:
    path = (KB_ROOT / source).resolve()
    if path != KB_ROOT and KB_ROOT not in path.parents:
        raise ValueError(f"evidence source escapes knowledge-base-hue: {source}")
    return path


def _source_family(source: str) -> str | None:
    if source == "foods/food-guides.md":
        return "guide"
    for family in ("restaurants", "cafes", "local_specialties"):
        if source.startswith(f"foods/{family}/"):
            return family
    return None


def _h2_sections(path: Path) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {heading: "\n".join(lines).strip() for heading, lines in sections.items()}


def _evidence_text(case: GoldenCase, issues: list[str]) -> tuple[str, set[str]]:
    parts = []
    families = set()
    if not case.evidence:
        issues.append(f"{case.case_id}: evidence is empty")
        return "", families
    for source, declared_sections in case.evidence.items():
        family = _source_family(source)
        if family is None:
            issues.append(f"{case.case_id}: source outside approved families: {source}")
            continue
        families.add(family)
        try:
            path = _source_path(source)
        except ValueError as exc:
            issues.append(f"{case.case_id}: {exc}")
            continue
        if not path.is_file():
            issues.append(f"{case.case_id}: source does not exist: {source}")
            continue
        if not isinstance(declared_sections, list) or not declared_sections:
            issues.append(f"{case.case_id}: evidence sections are empty for {source}")
            continue
        available = _h2_sections(path)
        for section in declared_sections:
            if not isinstance(section, str) or not section.strip():
                issues.append(f"{case.case_id}: empty evidence section for {source}")
            elif section not in available:
                issues.append(f"{case.case_id}: unknown section {section!r} in {source}")
            else:
                parts.append(available[section])
    return "\n".join(parts), families


def _raise_issues(issues: list[str]) -> None:
    if issues:
        raise ValueError("golden validation failed:\n- " + "\n- ".join(issues))


def validate_full(cases: list[GoldenCase]) -> dict:
    issues = []
    if len(cases) != 100:
        issues.append(f"expected 100 cases, found {len(cases)}")

    expected_ids = [f"foods-{index:04d}" for index in range(1, 101)]
    actual_ids = [case.case_id for case in cases]
    if actual_ids != expected_ids:
        issues.append("case IDs must be foods-0001..foods-0100 in file order")

    normalized_questions = [case.question.strip().casefold() for case in cases]
    if len(set(normalized_questions)) != len(normalized_questions):
        issues.append("questions must be unique after strip/casefold")

    category_counts = Counter(case.category for case in cases)
    if dict(category_counts) != CATEGORY_QUOTAS:
        issues.append(
            f"category counts {dict(category_counts)} != {CATEGORY_QUOTAS}"
        )

    source_coverage = Counter()
    for case in cases:
        if not CASE_ID.fullmatch(case.case_id):
            issues.append(f"invalid case_id: {case.case_id}")
        if not case.question.strip():
            issues.append(f"{case.case_id}: question is empty")
        if not case.reference_answer.strip():
            issues.append(f"{case.case_id}: reference_answer is empty")
        if case.category not in CATEGORY_QUOTAS:
            issues.append(f"{case.case_id}: invalid category {case.category}")

        evidence_text, families = _evidence_text(case, issues)
        for family in families:
            source_coverage[family] += 1

        for keyword in case.keywords:
            normalized = keyword.strip().casefold()
            if not normalized:
                issues.append(f"{case.case_id}: keyword is empty")
            if normalized in GENERIC_KEYWORDS:
                issues.append(f"{case.case_id}: generic keyword {keyword!r}")
            if normalized not in case.reference_answer.casefold():
                issues.append(f"{case.case_id}: keyword {keyword!r} missing from reference")
            if normalized not in evidence_text.casefold():
                issues.append(f"{case.case_id}: keyword {keyword!r} missing from evidence")

    for family, target in SOURCE_TARGETS.items():
        if source_coverage[family] < target:
            issues.append(
                f"source coverage {family}={source_coverage[family]} < {target}"
            )

    _raise_issues(issues)
    return {
        "cases": len(cases),
        "categories": dict(category_counts),
        "source_coverage": dict(source_coverage),
    }


def validate_smoke(full: list[GoldenCase], smoke: list[GoldenCase]) -> dict:
    issues = []
    if len(smoke) != 20:
        issues.append(f"expected 20 smoke cases, found {len(smoke)}")
    full_by_id = {case.case_id: case for case in full}
    smoke_ids = [case.case_id for case in smoke]
    if len(set(smoke_ids)) != len(smoke_ids):
        issues.append("smoke case IDs must be unique")
    categories = set()
    families = set()
    for case in smoke:
        full_case = full_by_id.get(case.case_id)
        if full_case is None:
            issues.append(f"smoke case missing from full: {case.case_id}")
        elif case.model_dump() != full_case.model_dump():
            issues.append(f"smoke row differs from full: {case.case_id}")
        categories.add(case.category)
        for source in case.evidence:
            family = _source_family(source)
            if family:
                families.add(family)
    if categories != set(CATEGORY_QUOTAS):
        issues.append(f"smoke categories incomplete: {sorted(categories)}")
    if families != set(SOURCE_TARGETS):
        issues.append(f"smoke source families incomplete: {sorted(families)}")
    _raise_issues(issues)
    return {"cases": len(smoke), "categories": len(categories), "source_families": len(families)}


def document_is_relevant(case: GoldenCase, document: RetrievedDocument) -> bool:
    source = document.metadata.get("source")
    section = document.metadata.get("section")
    return (
        isinstance(source, str)
        and isinstance(section, str)
        and section in case.evidence.get(source, [])
    )


def main() -> None:
    full = load_golden(FULL_PATH)
    print({"full": validate_full(full)})
    smoke = load_golden(SMOKE_PATH)
    print({"smoke": validate_smoke(full, smoke)})


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run the validator tests again**

Run the focused pytest command. Expected now: import succeeds; tests fail only because the two real V2 data files are not present.

- [ ] **Step 6: Check the task diff**

Run `git diff --check`. Expected: no whitespace errors. Stop for reviewer approval of the validator contract before authoring data.

---

### Task 2: Curate the 40 restaurant-primary cases

**Files:**
- Create: `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`

**Interfaces:**
- Consumes: `foods/restaurants/*.md`, the old 104 rows as optional candidates, and the schema/validator from Task 1.
- Produces: rows `foods-0001` through `foods-0040`.

- [ ] **Step 1: Read every restaurant source before selecting cases**

Review all 57 Markdown files under `knowledge-base-hue/foods/restaurants/`. For every candidate, inspect the complete declared H2 section, not a search-result snippet.

- [ ] **Step 2: Curate the restaurant category allocation**

Write 40 JSONL rows with this exact allocation:

```python
{
    "direct_fact": 10,
    "temporal": 6,
    "comparative": 4,
    "numerical": 4,
    "relationship": 7,
    "spanning": 4,
    "holistic": 2,
    "food_knowledge": 3,
    "guide_planning": 0,
}
```

Reuse an old row only after checking question, reference, keywords and every evidence section directly. Rewrite old `relevant_sources`/`relevant_sections` into the single `evidence` object. Do not copy an old annotation without review.

- [ ] **Step 3: Apply the per-case acceptance checklist**

For each row confirm all of the following before keeping it:

```text
one clear user intent
answerable from declared evidence
natural Vietnamese wording
no trick or live/latest wording
2-4 specific keywords in both reference and evidence
concise semantic reference answer
correct category
all alternative valid source/sections included
no unresolved conflict with another curated source
```

- [ ] **Step 4: Run structural validation at the partial checkpoint**

Run a read-only count command from repo root:

```bash
jq -r '.category' knowledge-base-hue/foods/evaluation/golden_v2.jsonl | sort | uniq -c
```

Expected: 40 valid JSON rows with the Task 2 category allocation. Do not run `validate_full()` until all 100 rows exist.

- [ ] **Step 5: Reviewer checkpoint**

Present the 40 rows and any source conflicts to the reviewer. If fewer than 40 natural grounded cases exist, stop and ask the user to add source information or approve redistribution.

- [ ] **Step 6: Check the task diff**

Run `git diff --check`. Expected: no whitespace errors.

---

### Task 3: Curate the 20 cafe-primary cases

**Files:**
- Modify: `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`

**Interfaces:**
- Consumes: all 24 files in `foods/cafes/` and Task 2 rows.
- Produces: rows `foods-0041` through `foods-0060`.

- [ ] **Step 1: Read every cafe source**

Review every Markdown file in `knowledge-base-hue/foods/cafes/` and compare overlapping coffee facts with `foods/local_specialties/ca phe muoi.md` before accepting evidence.

- [ ] **Step 2: Append the exact cafe allocation**

```python
{
    "direct_fact": 5,
    "temporal": 3,
    "comparative": 2,
    "numerical": 2,
    "relationship": 4,
    "spanning": 2,
    "holistic": 1,
    "food_knowledge": 1,
    "guide_planning": 0,
}
```

Use the complete checklist from Task 2 for every row. Cafe coverage is mandatory; do not replace missing cafe cases silently with restaurant cases.

- [ ] **Step 3: Validate the partial file**

Run from repo root:

```bash
wc -l knowledge-base-hue/foods/evaluation/golden_v2.jsonl
jq -r '.case_id' knowledge-base-hue/foods/evaluation/golden_v2.jsonl | tail -n 1
jq -r '.category' knowledge-base-hue/foods/evaluation/golden_v2.jsonl | sort | uniq -c
```

Expected: 60 rows, final ID `foods-0060`, and cumulative category counts equal to Tasks 2+3.

- [ ] **Step 4: Reviewer checkpoint and diff check**

Report insufficient/conflicting cafe information instead of forcing cases. Run `git diff --check`; expected no whitespace errors.

---

### Task 4: Curate the 20 local-specialty-primary cases

**Files:**
- Modify: `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`

**Interfaces:**
- Consumes: all nine files in `foods/local_specialties/` and approved prior rows.
- Produces: rows `foods-0061` through `foods-0080`.

- [ ] **Step 1: Read all local-specialty sources and overlapping venue facts**

Review each complete local-specialty Markdown file. Where a specialty file repeats a restaurant address, hour or price, compare both sources and stop on conflict.

- [ ] **Step 2: Append the exact local-specialty allocation**

```python
{
    "direct_fact": 3,
    "temporal": 1,
    "comparative": 4,
    "numerical": 2,
    "relationship": 1,
    "spanning": 3,
    "holistic": 1,
    "food_knowledge": 5,
    "guide_planning": 0,
}
```

Do not turn temporal facts into numerical questions to fill the numerical quota. Use the Task 2 checklist for every case.

- [ ] **Step 3: Validate the partial file and review**

Run from repo root:

```bash
wc -l knowledge-base-hue/foods/evaluation/golden_v2.jsonl
jq -r '.case_id' knowledge-base-hue/foods/evaluation/golden_v2.jsonl | tail -n 1
jq -r '.category' knowledge-base-hue/foods/evaluation/golden_v2.jsonl | sort | uniq -c
git diff --check
```

Expected: 80 rows, final ID `foods-0080`, cumulative category counts equal to Tasks 2-4, and no whitespace errors. Stop for source insufficiency or conflicts.

---

### Task 5: Curate the 20 food-guide-primary cases and complete full validation

**Files:**
- Modify: `knowledge-base-hue/foods/evaluation/golden_v2.jsonl`

**Interfaces:**
- Consumes: the complete `foods/food-guides.md` and the first 80 approved rows.
- Produces: rows `foods-0081` through `foods-0100` and a validator-clean full dataset.

- [ ] **Step 1: Read the complete food guide**

Review every answer-facing H2 section in `knowledge-base-hue/foods/food-guides.md`. Do not split one list into near-duplicate questions merely to reach 20.

- [ ] **Step 2: Append the exact guide allocation**

```python
{
    "direct_fact": 0,
    "temporal": 0,
    "comparative": 0,
    "numerical": 0,
    "relationship": 0,
    "spanning": 3,
    "holistic": 4,
    "food_knowledge": 3,
    "guide_planning": 10,
}
```

Reference answers are examples rather than the only accepted wording or venue combination. Every listed fact must still be supported by the declared guide section.

- [ ] **Step 3: Run the strict full validator**

From `backend/` run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run python -m evaluation.golden_dataset
```

Expected before the smoke file exists: full validation passes and the command then reports the missing smoke file. If full validation reports a semantic-looking issue, inspect the source; do not weaken the rule to make the file pass.

- [ ] **Step 4: Perform the second manual audit**

Review all new/rewritten cases, all cases inherited from old findings, and every case whose evidence contains more than one section. Check direct source support and alternative valid evidence.

- [ ] **Step 5: Reviewer checkpoint and diff check**

Provide exact category/source counts and unresolved findings. Run `git diff --check`; expected no whitespace errors.

---

### Task 6: Select and validate the exact 20-case smoke subset

**Files:**
- Create: `knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl`

**Interfaces:**
- Consumes: the validator-clean `golden_v2.jsonl`.
- Produces: an exact 20-row subset covering all nine categories and four source families.

- [ ] **Step 1: Select IDs from full V2**

Choose 20 IDs that cover all nine categories, all four source families, direct and multi-section evidence, and both simple and light-synthesis questions. Do not rewrite any selected row.

- [ ] **Step 2: Copy complete rows unchanged**

Copy the complete JSON line for each selected ID from `golden_v2.jsonl` into `golden_v2_smoke.jsonl`. Preserve the full-file order.

- [ ] **Step 3: Run strict full + smoke validation**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run python -m evaluation.golden_dataset
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run python -m pytest tests/test_evaluation.py -q --tb=short
```

Expected: validator reports 100 full cases and 20 smoke cases; focused tests pass.

- [ ] **Step 4: Check exact subset equality**

Run the strict validator a second time after reviewing the selected IDs:

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run python -m evaluation.golden_dataset
```

Expected: the smoke summary reports exactly 20 cases, nine categories and four source families; any altered row fails deep equality.

- [ ] **Step 5: Reviewer checkpoint and diff check**

Run `git diff --check`; expected no whitespace errors. Present the selected 20 IDs and coverage counts.

---

### Task 7: Verify binary relevance with the real runtime

**Files:**
- Modify: `backend/tests/test_evaluation.py`
- Create: `reports/phase_8_golden_dataset_v2_implementation_report.md`

**Interfaces:**
- Consumes: `GoldenCase`, `document_is_relevant`, real `dense_only` retrieval, the real smoke set and a real isolated test collection.
- Produces: runtime evidence that returned documents expose usable `source`/`section` metadata and the gold mapping is deterministic.

- [ ] **Step 1: Add one real retrieval metadata/relevance test**

Add to `backend/tests/test_evaluation.py`:

```python
def test_golden_v2_binary_relevance_uses_real_retrieval_metadata(ingested_collection):
    from conftest import TEST_COLLECTION

    cases = load_golden(GOLDEN_V2_SMOKE)
    services = build_services("dense_only", collection_name=TEST_COLLECTION)
    for case in cases:
        documents = services.retrieval.search(case.question)
        assert documents
        assert all(doc.metadata.get("source") for doc in documents)
        assert all(isinstance(doc.metadata.get("section"), str) for doc in documents)
        relevance = [document_is_relevant(case, doc) for doc in documents]
        assert all(isinstance(value, bool) for value in relevance)
```

This test verifies the contract, not a winner threshold. A real miss remains a measured baseline miss; do not change evidence to make the current model look better.

- [ ] **Step 2: Run structural tests offline**

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q --tb=short -k 'golden_v2 and not binary_relevance'
```

Expected: all selected structural V2 tests pass without paid calls.

- [ ] **Step 3: Run the real retrieval test**

```bash
cd backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py::test_golden_v2_binary_relevance_uses_real_retrieval_metadata -q --tb=short -s
```

Expected: PASS using the real corpus, embedding model and isolated Qdrant test collection. No OpenAI/OpenRouter call is made.

- [ ] **Step 4: Run final validation**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run python -m evaluation.golden_dataset
UV_CACHE_DIR=/tmp/hue-rag-golden-v2-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q --tb=short
git diff --check
git status --short
```

Expected: strict validator passes, test file passes, no whitespace errors, and only approved files plus pre-existing user changes appear.

- [ ] **Step 5: Write the concise implementation report**

Record:

```text
full/smoke paths and counts
category and source coverage
number of reused, rewritten and new cases
source conflicts or user-approved reallocations
validator and pytest commands with real outcomes
real retrieval metadata verification outcome
explicit statement that Phase 7 files and active collection were not mutated
explicit statement that no fake output was used as evidence
```

Do not add a per-case audit package, generated manifest or duplicated result artifact.

- [ ] **Step 6: Final reviewer checkpoint**

Do not stage, commit, push, run Phase 8 model benchmarks or switch any default dataset. Hand the diff and report to the Reviewer for Gate 0 acceptance.
