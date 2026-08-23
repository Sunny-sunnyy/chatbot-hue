"""Validate the foods test suite (tests.jsonl) against the curated knowledge base.

Checks:
- Each line is a valid JSON object with case_id / question / keywords /
  reference_answer / category / relevant_sources / relevant_sections.
- Category is one of the allowed values.
- Questions are unique; case ids are stable unique foods-NNNN values.
- Keywords are 1-5 terms, not generic, and appear in the curated knowledge base.
- Every keyword appears in the reference answer.
- Reference answer is non-empty and not too long.
- relevant_sources is a non-empty list of existing KB paths; declared sections
  are keys of relevant_sources and exist as headings in the source Markdown.

Usage: UV_CACHE_DIR=/tmp/uv-cache uv run python validate_tests.py
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEST_FILE = HERE / "tests.jsonl"
KB_DIR = HERE.parent
KB_ROOT = HERE.parent.parent  # knowledge-base-hue root; sources are root-relative

CASE_ID_RE = re.compile(r"^foods-\d{4}$")
HEADING_RE = re.compile(r"^#{2,}\s+(.+?)\s*$", re.MULTILINE)

VALID_CATEGORIES = {
    "direct_fact",
    "temporal",
    "comparative",
    "numerical",
    "relationship",
    "spanning",
    "holistic",
    "food_knowledge",
    "guide_planning",
}

GENERIC_KEYWORDS = {"quán", "huế", "món", "giá", "ở đâu", "ngon", "ăn", "gì", "nào"}

MAX_KEYWORDS = 5
# Composite guide questions (e.g. 3-day food tour) legitimately list many venues.
MAX_REFERENCE_LEN = 850


def load_kb_text() -> str:
    """Concatenate all curated markdown files under foods/."""
    parts = []
    for path in sorted(KB_DIR.glob("**/*.md")):
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts).lower()


def load_tests() -> list[dict]:
    """Load tests from tests.jsonl."""
    tests = []
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            data = json.loads(line)
            data["_line"] = line_no
            tests.append(data)
    return tests


def section_names(path: Path) -> set[str]:
    """Return heading names of a curated Markdown file (## and deeper)."""
    return {
        match.group(1).strip() for match in HEADING_RE.finditer(path.read_text(encoding="utf-8"))
    }


def main() -> int:
    kb = load_kb_text()
    tests = load_tests()
    errors: list[str] = []
    seen_questions: set[str] = set()

    seen_case_ids: set[str] = set()

    for test in tests:
        line = test.pop("_line")
        label = f"line {line}"

        required = {
            "case_id",
            "question",
            "keywords",
            "reference_answer",
            "category",
            "relevant_sources",
            "relevant_sections",
        }
        missing = required - set(test)
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
            continue

        case_id = test["case_id"]
        question = test["question"]
        keywords = test["keywords"]
        reference = test["reference_answer"]
        category = test["category"]

        if not isinstance(case_id, str) or not CASE_ID_RE.fullmatch(case_id.strip()):
            errors.append(f"{label}: invalid case_id {case_id!r} (expected foods-NNNN)")
        elif case_id in seen_case_ids:
            errors.append(f"{label}: duplicate case_id {case_id!r}")
        seen_case_ids.add(case_id.strip())

        if not isinstance(question, str) or not question.strip():
            errors.append(f"{label}: question is empty")
        if question in seen_questions:
            errors.append(f"{label}: duplicate question")
        seen_questions.add(question)

        if category not in VALID_CATEGORIES:
            errors.append(f"{label}: invalid category {category!r}")

        if not isinstance(keywords, list) or not 1 <= len(keywords) <= MAX_KEYWORDS:
            errors.append(f"{label}: keywords must be a list of 1-{MAX_KEYWORDS} terms")
        elif not all(isinstance(k, str) and k.strip() for k in keywords):
            errors.append(f"{label}: keywords contain empty entries")
        else:
            for kw in keywords:
                kw = kw.strip()
                if len(kw) == 1 and kw.isascii():
                    errors.append(f"{label}: keyword {kw!r} is a single character")
                if " " not in kw and kw.lower() in GENERIC_KEYWORDS:
                    errors.append(f"{label}: generic keyword {kw!r}")
                if kw.lower() not in kb:
                    errors.append(f"{label}: keyword {kw!r} not found in knowledge base")
                if kw.lower() not in reference.lower():
                    errors.append(f"{label}: keyword {kw!r} not in reference answer")

        if not isinstance(reference, str) or not reference.strip():
            errors.append(f"{label}: reference_answer is empty")
        elif len(reference) > MAX_REFERENCE_LEN:
            errors.append(f"{label}: reference_answer too long ({len(reference)} > {MAX_REFERENCE_LEN})")

        sources = test["relevant_sources"]
        if not isinstance(sources, list) or not sources:
            errors.append(f"{label}: relevant_sources must be a non-empty list")
        else:
            source_files = {}
            for source in sources:
                if not isinstance(source, str) or not source.strip():
                    errors.append(f"{label}: relevant_sources contain an empty entry")
                    continue
                rel = KB_ROOT / source.strip()
                if not rel.is_file():
                    errors.append(f"{label}: relevant source {source!r} does not exist")
                else:
                    source_files[source.strip()] = rel

        sections = test["relevant_sections"]
        if not isinstance(sections, dict):
            errors.append(f"{label}: relevant_sections must be a JSON object")
        else:
            for source, section_list in sections.items():
                if source not in source_files:
                    errors.append(
                        f"{label}: relevant_sections key {source!r} is not in "
                        "relevant_sources"
                    )
                    continue
                names = section_names(source_files[source])
                if not isinstance(section_list, list) or not section_list:
                    errors.append(
                        f"{label}: relevant_sections[{source!r}] must be a non-empty list"
                    )
                    continue
                for section in section_list:
                    if section.strip() not in names:
                        errors.append(
                            f"{label}: section {section!r} of {source!r} is not a "
                            "heading in the source Markdown"
                        )

    if errors:
        print(f"FAIL: {len(errors)} issue(s) found")
        for err in errors:
            print(f"  - {err}")
        return 1

    counts: dict[str, int] = {}
    for test in tests:
        counts[test["category"]] = counts.get(test["category"], 0) + 1

    print(f"PASS: {len(tests)} tests, all checks green")
    for cat in sorted(counts):
        print(f"  {cat}: {counts[cat]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
