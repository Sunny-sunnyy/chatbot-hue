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

V3_FULL_PATH = KB_ROOT / "foods" / "evaluation" / "golden_v3.jsonl"
V3_SMOKE_PATH = KB_ROOT / "foods" / "evaluation" / "golden_v3_smoke.jsonl"
V3_CASE_ID = re.compile(r"foods-v3-\d{4}")
V3_ALLOWED_COUNTS = {40, 45, 50}

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
ALLOWED_CATEGORIES = set(CATEGORY_QUOTAS)
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
