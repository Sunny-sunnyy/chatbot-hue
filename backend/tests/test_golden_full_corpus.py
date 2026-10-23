from pathlib import Path

import json
import pytest

from evaluation.golden_full_corpus import (
    check_case,
    check_file,
    merge_authoring,
    select_smoke,
)
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

CORPUS = {
    "heritages/heritage/a.md": "# Lăng Tự Đức\nVé tham quan lăng Tự Đức là 150.000 đồng.",
}


def authoring_row(**changes):
    row = {
        "question": "Vé vào lăng Tự Đức giá bao nhiêu?",
        "keywords": ["150.000 đồng", "Tự Đức"],
        "reference_answer": "Vé tham quan lăng Tự Đức là 150.000 đồng.",
        "category": "direct_fact",
        "partition": "heritages",
        "sources": ["heritages/heritage/a.md"],
    }
    row.update(changes)
    return row


def test_valid_authoring_case_passes():
    assert check_case(authoring_row(), CORPUS, authoring=True) == []


def test_official_file_rejects_authoring_fields():
    errors = check_case(authoring_row(), CORPUS, authoring=False)
    assert errors and "fields must be" in errors[0]


def test_keyword_must_be_verbatim_in_corpus():
    errors = check_case(authoring_row(keywords=["200.000 đồng", "Tự Đức"]), CORPUS, authoring=True)
    assert any("not verbatim in corpus" in e for e in errors)


def test_requires_answer_keyword_absent_from_question():
    row = authoring_row(keywords=["Tự Đức"])
    errors = check_case(row, CORPUS, authoring=True)
    assert any("answer keyword" in e for e in errors)


def test_out_of_scope_rules():
    good = authoring_row(
        question="Giá vé vào Văn Miếu Hà Nội là bao nhiêu?",
        keywords=[],
        reference_answer=INSUFFICIENT_ANSWER,
        category="out_of_scope",
        sources=[],
    )
    assert check_case(good, CORPUS, authoring=True) == []
    bad = dict(good, reference_answer="Không biết.")
    assert any("INSUFFICIENT_ANSWER" in e for e in check_case(bad, CORPUS, authoring=True))


def test_check_file_reports_line_and_duplicates(tmp_path: Path):
    path = tmp_path / "golden.jsonl"
    line = json.dumps(authoring_row(), ensure_ascii=False)
    path.write_text(line + "\n" + line + "\n{bad json\n", encoding="utf-8")
    errors, rows = check_file(path, CORPUS, authoring=True)
    assert len(rows) == 2
    assert any(e.startswith("line 3:") for e in errors)
    assert any("duplicate question" in e for e in errors)


def test_merge_strips_authoring_fields_in_partition_order(tmp_path: Path):
    for partition, rel_dir in (("foods", "foods"), ("heritages", "heritages")):
        folder = tmp_path / rel_dir / "evaluation"
        folder.mkdir(parents=True)
        row = authoring_row(partition=partition, question=f"Câu của {partition}?")
        (folder / "golden_full_corpus_authoring.jsonl").write_text(
            json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    merged = merge_authoring(tmp_path)
    assert [r["question"] for r in merged] == ["Câu của foods?", "Câu của heritages?"]
    assert all(set(r) == {"question", "keywords", "reference_answer", "category"} for r in merged)


def test_select_smoke_copies_exact_lines():
    lines = [f'{{"n": {i}}}' for i in range(1, 21)]
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    assert select_smoke(lines, numbers) == [lines[n - 1] for n in numbers]
    with pytest.raises(ValueError):
        select_smoke(lines, [1, 1, 3, 5, 7, 9, 11, 13, 15, 17])
