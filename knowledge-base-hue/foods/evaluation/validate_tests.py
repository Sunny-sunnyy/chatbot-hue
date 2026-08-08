"""Validate the foods test suite (tests.jsonl) against the curated knowledge base.

Checks:
- Each line is a valid JSON object with question / keywords / reference_answer / category.
- Category is one of the allowed values.
- Questions are unique.
- Keywords are 1-5 terms, not generic, and appear in the curated knowledge base.
- Every keyword appears in the reference answer.
- Reference answer is non-empty and not too long.

Usage: UV_CACHE_DIR=/tmp/uv-cache uv run python validate_tests.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEST_FILE = HERE / "tests.jsonl"
KB_DIR = HERE.parent

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


def main() -> int:
    kb = load_kb_text()
    tests = load_tests()
    errors: list[str] = []
    seen_questions: set[str] = set()

    for test in tests:
        line = test.pop("_line")
        label = f"line {line}"

        required = {"question", "keywords", "reference_answer", "category"}
        missing = required - set(test)
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
            continue

        question = test["question"]
        keywords = test["keywords"]
        reference = test["reference_answer"]
        category = test["category"]

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
