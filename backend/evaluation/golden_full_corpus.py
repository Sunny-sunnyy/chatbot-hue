"""Phase 7A Golden full-corpus: kiểm tra và gộp file câu hỏi. Không gọi mạng."""

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from ingestion.source_state import discover_full_corpus_files, read_source_lf
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

CATEGORIES = ("direct_fact", "multi_source", "comparative", "conditional", "out_of_scope")
# Thứ tự khóa cũng là thứ tự ghép file chính thức.
PARTITION_DIRS = {
    "foods": "foods",
    "heritages": "heritages",
    "festivals": "festivals",
    "performing_arts": "performing_arts",
    "travel_places": "travel/places",
    "travel_services": "travel/services",
    "travel_tickets": "travel/tickets",
}
OFFICIAL_FIELDS = ("question", "keywords", "reference_answer", "category")
AUTHORING_FIELDS = OFFICIAL_FIELDS + ("partition", "sources")
AUTHORING_NAME = "golden_full_corpus_authoring.jsonl"
OFFICIAL_NAME = "golden_full_corpus.jsonl"
SMOKE_NAME = "golden_full_corpus_smoke.jsonl"
SMOKE_SIZE = 10


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def load_corpus() -> tuple[Path, dict[str, str]]:
    root, rel_paths = discover_full_corpus_files()
    return root, {rel: nfc(read_source_lf(root / rel)) for rel in rel_paths}


def check_case(row: dict, corpus: dict[str, str], authoring: bool) -> list[str]:
    expected = AUTHORING_FIELDS if authoring else OFFICIAL_FIELDS
    if set(row) != set(expected):
        return [f"fields must be {sorted(expected)}, got {sorted(row)}"]

    errors = []
    question, keywords, answer, category = (row[name] for name in OFFICIAL_FIELDS)
    if not isinstance(question, str) or not question.strip():
        errors.append("question must be a non-empty string")
    if not isinstance(answer, str) or not answer.strip():
        errors.append("reference_answer must be a non-empty string")
    if not isinstance(keywords, list) or not all(isinstance(k, str) and k.strip() for k in keywords):
        errors.append("keywords must be a list of non-empty strings")
    if category not in CATEGORIES:
        errors.append(f"unknown category {category!r}")
    sources = row.get("sources", [])
    if authoring:
        if row["partition"] not in PARTITION_DIRS:
            errors.append(f"unknown partition {row['partition']!r}")
        if not isinstance(sources, list):
            errors.append("sources must be a list")
        else:
            errors += [f"source not in curated corpus: {s}" for s in sources if s not in corpus]
    if errors:
        return errors

    if category == "out_of_scope":
        if keywords:
            errors.append("out_of_scope keywords must be []")
        if answer != INSUFFICIENT_ANSWER:
            errors.append("out_of_scope reference_answer must equal INSUFFICIENT_ANSWER")
        if authoring and sources:
            errors.append("out_of_scope sources must be []")
        return errors

    if not keywords:
        errors.append("keywords must not be empty")
    if authoring and not sources:
        errors.append("sources must not be empty")
    for keyword in keywords:
        if not any(nfc(keyword) in text for text in corpus.values()):
            errors.append(f"keyword not verbatim in corpus: {keyword!r}")
    folded_question, folded_answer = nfc(question).casefold(), nfc(answer).casefold()
    if not any(
        nfc(k).casefold() not in folded_question and nfc(k).casefold() in folded_answer
        for k in keywords
    ):
        errors.append("needs >=1 answer keyword: absent from question, present in reference_answer")
    return errors


def check_file(path: Path, corpus: dict[str, str], authoring: bool) -> tuple[list[str], list[dict]]:
    errors, rows = [], []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {number}: must be a JSON object")
            continue
        errors += [f"line {number}: {e}" for e in check_case(row, corpus, authoring)]
        rows.append(row)
    counts = Counter(nfc(str(r.get("question", ""))) for r in rows)
    errors += [f"duplicate question: {q!r}" for q, n in counts.items() if n > 1]
    return errors, rows


def merge_authoring(kb_root: Path) -> list[dict]:
    merged = []
    for partition, rel_dir in PARTITION_DIRS.items():
        path = kb_root / rel_dir / "evaluation" / AUTHORING_NAME
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            row = json.loads(line)
            if row["partition"] != partition:
                raise ValueError(f"{path} line {number}: partition {row['partition']!r} != {partition!r}")
            merged.append({name: row[name] for name in OFFICIAL_FIELDS})
    return merged


def select_smoke(lines: list[str], line_numbers: list[int]) -> list[str]:
    if len(line_numbers) != SMOKE_SIZE or len(set(line_numbers)) != SMOKE_SIZE:
        raise ValueError(f"smoke needs exactly {SMOKE_SIZE} distinct line numbers")
    if not all(1 <= n <= len(lines) for n in line_numbers):
        raise ValueError("smoke line number out of range")
    return [lines[n - 1] for n in line_numbers]


def print_distribution(rows: list[dict]) -> None:
    print("category:", dict(Counter(r.get("category") for r in rows)))
    if any("partition" in r for r in rows):
        print("partition:", dict(Counter(r.get("partition") for r in rows)))
    print("total:", len(rows))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evaluation.golden_full_corpus")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check")
    check.add_argument("path", type=Path)
    check.add_argument("--authoring", action="store_true")
    commands.add_parser("merge")
    smoke = commands.add_parser("smoke")
    smoke.add_argument("line_numbers", type=int, nargs="+")
    args = parser.parse_args(argv)

    kb_root, corpus = load_corpus()
    official = kb_root / "evaluation" / OFFICIAL_NAME

    if args.command == "check":
        errors, rows = check_file(args.path, corpus, args.authoring)
        print_distribution(rows)
    elif args.command == "merge":
        errors = []
        for rel_dir in PARTITION_DIRS.values():
            path = kb_root / rel_dir / "evaluation" / AUTHORING_NAME
            if path.is_file():
                errors += [f"{path.name} ({rel_dir}): {e}" for e in check_file(path, corpus, True)[0]]
        if not errors:
            merged = merge_authoring(kb_root)
            official.parent.mkdir(parents=True, exist_ok=True)
            official.write_text(
                "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8"
            )
            errors, rows = check_file(official, corpus, authoring=False)
            print_distribution(rows)
    else:
        lines = official.read_text(encoding="utf-8").splitlines()
        selected = select_smoke(lines, args.line_numbers)
        (official.parent / SMOKE_NAME).write_text("".join(l + "\n" for l in selected), encoding="utf-8")
        errors = []
        print("smoke:", len(selected))

    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
