"""Strict JSONL loader and schema validator for the foods evaluation dataset.

Every problem is collected and reported with its 1-based line number; no row
is silently skipped. The dataset file itself is only read. The loader never
derives a case id from other fields: each row carries an explicit stable
foods-NNNN id, and the returned cases are frozen so the evaluation run cannot
mutate ground truth.
"""
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

FOODS_CASE_ID_RE = re.compile(r"^foods-\d{4}$")
# Baseline dataset version; the loader accepts an explicit expected_count so
# the same code validates both the full 104-case set and small test inputs.
BASE_CASE_COUNT = 104

# Curated Markdown headings are #-prefixed; a declared section (e.g.
# "Thông tin") matches a `## Thông tin` heading line in the source file.
HEADING_RE = re.compile(r"^#{2,}\s+(.+?)\s*$", re.MULTILINE)


class DatasetValidationError(ValueError):
    """Raised when the dataset is invalid; str() aggregates every problem."""


@dataclass(frozen=True)
class TestCase:
    """One ground-truth case; immutable after loading."""

    case_id: str
    question: str
    keywords: tuple[str, ...]
    reference_answer: str
    category: str
    relevant_sources: tuple[str, ...]
    relevant_sections: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class LoadedDataset:
    """Validated cases plus dataset identity for run metadata."""

    cases: tuple[TestCase, ...]
    dataset_path: str
    dataset_checksum: str


def _heading_names(text):
    """Return the stripped heading names of an ATX heading line."""
    return {
        match.group(1).strip()
        for match in HEADING_RE.finditer(text)
    }


def load_dataset(path, kb_root, expected_count=None):
    """Load and validate JSONL rows; raise DatasetValidationError on any issue.

    kb_root is the knowledge-base-hue directory; relevant_sources paths are
    resolved against it and must stay inside it. expected_count, when given,
    must equal the number of parsed rows exactly.
    """
    path = Path(path)
    kb_root = Path(kb_root).resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:  # non-UTF-8 dataset is unreadable
        raise DatasetValidationError("dataset is not valid UTF-8") from exc

    errors = []
    cases = []
    seen_ids = set()
    parsed_count = 0

    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            errors.append(f"line {line_no}: blank line")
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc.msg}")
            continue
        parsed_count += 1
        case = _validate_row(
            row, line_no, errors, seen_ids, kb_root
        )
        if case is not None:
            cases.append(case)
            seen_ids.add(case.case_id)

    if expected_count is not None and parsed_count != expected_count:
        errors.append(
            f"dataset expected {expected_count} rows, found {parsed_count}"
        )

    if errors:
        raise DatasetValidationError("\n".join(errors))
    return LoadedDataset(
        cases=tuple(cases),
        dataset_path=str(path),
        dataset_checksum=hashlib.sha256(raw).hexdigest(),
    )


def _validate_row(row, line_no, errors, seen_ids, kb_root):
    """Validate one row; return a TestCase or None when any field is invalid."""
    label = f"line {line_no}"
    if not isinstance(row, dict):
        errors.append(f"{label}: row must be a JSON object")
        return None

    case_id = row.get("case_id")
    if not isinstance(case_id, str) or not FOODS_CASE_ID_RE.fullmatch(
        case_id.strip()
    ):
        errors.append(f"{label}: missing or invalid case_id (expected foods-NNNN)")
    elif case_id in seen_ids:
        errors.append(f"{label}: duplicate case_id {case_id!r}")
    if isinstance(case_id, str):
        case_id = case_id.strip()

    valid = True

    question = row.get("question")
    if not isinstance(question, str) or not question.strip():
        errors.append(f"{label}: question is empty")
        valid = False

    reference = row.get("reference_answer")
    if not isinstance(reference, str) or not reference.strip():
        errors.append(f"{label}: reference_answer is empty")
        valid = False

    category = row.get("category")
    if not isinstance(category, str) or not category.strip():
        errors.append(f"{label}: category is empty")
        valid = False

    keywords_data = row.get("keywords")
    keywords = None
    if not isinstance(keywords_data, list) or not keywords_data:
        errors.append(f"{label}: keywords must be a non-empty list")
    else:
        stripped = []
        for item in keywords_data:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{label}: keywords contain an empty entry")
                valid = False
                break
            stripped.append(item.strip())
        else:
            keywords = tuple(stripped)

    sources = _validate_sources(row, label, errors, kb_root)
    sections = _validate_sections(row, label, errors, kb_root, sources)

    base_ok = (
        valid
        and sources is not None
        and sections is not None
        and isinstance(case_id, str)
        and FOODS_CASE_ID_RE.fullmatch(case_id)
    )
    if not base_ok:
        return None
    return TestCase(
        case_id=case_id,
        question=question.strip(),
        keywords=keywords,
        reference_answer=reference.strip(),
        category=category.strip(),
        relevant_sources=sources,
        relevant_sections=sections,
    )


def _validate_sources(row, label, errors, kb_root):
    """Validate relevant_sources; return a tuple of sources or None."""
    sources_data = row.get("relevant_sources")
    if not isinstance(sources_data, list) or not sources_data:
        errors.append(f"{label}: relevant_sources must be a non-empty list")
        return None
    sources = []
    for item in sources_data:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}: relevant_sources contain an empty entry")
            return None
        rel = Path(item.strip())
        target = (kb_root / rel).resolve()
        if not target.is_relative_to(kb_root):
            errors.append(
                f"{label}: source {rel} escapes the knowledge base directory"
            )
            return None
        if not target.is_file():
            errors.append(
                f"{label}: relevant source {rel} does not exist in the KB"
            )
            return None
        sources.append(str(rel))
    return tuple(sources)


def _validate_sections(row, label, errors, kb_root, sources):
    """Validate relevant_sections; return a normalized dict or None."""
    sections_data = row.get("relevant_sections", {})
    if not isinstance(sections_data, dict):
        errors.append(f"{label}: relevant_sections must be a JSON object")
        return None
    sections = {}
    for source, section_list in sections_data.items():
        if sources is None or source not in sources:
            errors.append(
                f"{label}: relevant_sections key {source!r} is not in "
                "relevant_sources"
            )
            continue
        if not isinstance(section_list, list) or not section_list:
            errors.append(
                f"{label}: relevant_sections[{source!r}] must be a non-empty list"
            )
            continue
        markdown = (kb_root / source).read_text(encoding="utf-8")
        names = _heading_names(markdown)
        normalized = []
        for section in section_list:
            if not isinstance(section, str) or not section.strip():
                errors.append(
                    f"{label}: relevant_sections[{source!r}] contain an "
                    "empty section"
                )
                continue
            name = section.strip()
            if name not in names:
                errors.append(
                    f"{label}: section {name!r} of {source!r} is not a "
                    "heading in the source Markdown"
                )
                continue
            normalized.append(name)
        if len(normalized) == len(section_list):
            sections[source] = tuple(normalized)
    if sections_data and len(sections) != len(sections_data):
        return None
    return sections
