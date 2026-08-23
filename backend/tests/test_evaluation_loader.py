"""Pure contract tests for the strict foods evaluation dataset loader.

Known small inputs only; the real 104-case dataset is validated separately by
knowledge-base-hue/foods/evaluation/validate_tests.py and the notebook.
"""

import json
import hashlib

import pytest

from evaluation.test_loader import DatasetValidationError, load_dataset

CASE_ID_RE = "foods-0001"


def make_case(**overrides):
    base = {
        "case_id": CASE_ID_RE,
        "question": "Quán bún bò Mệ Kéo nằm ở đâu?",
        "keywords": ["Mệ Kéo", "Bạch Đằng"],
        "reference_answer": "Quán bún bò Mệ Kéo nằm tại số 20 đường Bạch Đằng.",
        "category": "direct_fact",
        "relevant_sources": ["foods/restaurants/quan bun bo me keo.md"],
        "relevant_sections": {
            "foods/restaurants/quan bun bo me keo.md": ["Thông tin"],
        },
    }
    base.update(overrides)
    return base


def write_dataset(tmp_path, rows):
    """Write rows (dicts or raw strings) as JSONL and return the path."""
    path = tmp_path / "tests.jsonl"
    if isinstance(rows, str):
        path.write_text(rows, encoding="utf-8")
    else:
        path.write_text(
            "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
            encoding="utf-8",
        )
    return path


def write_kb(tmp_path, files):
    """Write fake curated markdown files; kb_root defaults to tmp_path."""
    base = tmp_path / "knowledge-base-hue"
    for rel, content in files.items():
        target = base / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return base


@pytest.fixture()
def kb(tmp_path):
    return write_kb(
        tmp_path,
        {
            "foods/restaurants/quan bun bo me keo.md": (
                "# Quán bún bò Mệ Kéo\n"
                "## Tóm tắt\n"
                "Nội dung tóm tắt.\n"
                "## Thông tin\n"
                "Địa chỉ ví dụ.\n"
            ),
        },
    )


def test_loads_valid_dataset_and_computes_checksum(tmp_path, kb):
    """A valid file loads all fields and the checksum covers exact bytes."""
    row = make_case()
    path = write_dataset(tmp_path, [row])
    loaded = load_dataset(path, kb_root=kb)
    assert len(loaded.cases) == 1
    case = loaded.cases[0]
    assert case.case_id == "foods-0001"
    assert case.question == row["question"]
    assert case.keywords == tuple(row["keywords"])
    assert case.reference_answer == row["reference_answer"]
    assert case.category == "direct_fact"
    assert case.relevant_sources == ("foods/restaurants/quan bun bo me keo.md",)
    assert case.relevant_sections == {
        "foods/restaurants/quan bun bo me keo.md": ("Thông tin",)
    }
    assert loaded.dataset_checksum == hashlib.sha256(path.read_bytes()).hexdigest()
    assert loaded.dataset_path == str(path)


def test_blank_line_reported_with_line_number(tmp_path, kb):
    """Whitespace-only lines are invalid rows and fail with their line number."""
    row = make_case()
    path = write_dataset(tmp_path, [row, ""])
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "line 2" in str(exc_info.value)


def test_malformed_json_reported_with_line_number(tmp_path, kb):
    path = write_dataset(tmp_path, '{"case_id": "foods-0001", "question": "x"\n')
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "line 1" in str(exc_info.value)


def test_missing_or_invalid_case_id_reported(tmp_path, kb):
    """No frontmatter derivation: each row needs an explicit foods-NNNN id."""
    rows = [
        make_case(case_id="FOODS-0001"),
        make_case(case_id="foods-abc"),
        make_case(case_id="case-0001"),
    ]
    path = write_dataset(tmp_path, rows)
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    for lineno in (1, 2, 3):
        assert f"line {lineno}" in str(exc_info.value)


def test_duplicate_case_id_reported(tmp_path, kb):
    path = write_dataset(tmp_path, [make_case(), make_case()])
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "duplicate" in str(exc_info.value)


def test_empty_question_reference_or_category_reported(tmp_path, kb):
    rows = [
        make_case(question=""),
        make_case(reference_answer="   "),
        make_case(category=""),
    ]
    path = write_dataset(tmp_path, rows)
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    for lineno in (1, 2, 3):
        assert f"line {lineno}" in str(exc_info.value)


def test_keywords_validation_reported(tmp_path, kb):
    rows = [
        make_case(keywords="Mệ Kéo"),
        make_case(keywords=[]),
        make_case(keywords=["Mệ Kéo", ""]),
        make_case(keywords=["Mệ Kéo", 42]),
    ]
    path = write_dataset(tmp_path, rows)
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    for lineno in (1, 2, 3, 4):
        assert f"line {lineno}" in str(exc_info.value)


def test_relevant_sources_required_and_must_exist(tmp_path, kb):
    rows = [
        make_case(relevant_sources=[]),
        make_case(relevant_sources=["foods/restaurants/khong ton tai.md"]),
        make_case(relevant_sources=["../outside.md"]),
    ]
    path = write_dataset(tmp_path, rows)
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "line 1" in str(exc_info.value)
    assert "line 2" in str(exc_info.value)
    assert "line 3" in str(exc_info.value)


def test_relevant_section_keys_restricted_to_sources(tmp_path, kb):
    row = make_case(
        relevant_sections={
            "foods/restaurants/quan bun bo me keo.md": ["Thông tin"],
            "foods/restaurants/other.md": ["Thông tin"],
        }
    )
    path = write_dataset(tmp_path, [row])
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "relevant_sections" in str(exc_info.value)


def test_declared_section_must_exist_in_markdown(tmp_path, kb):
    row = make_case(
        relevant_sections={
            "foods/restaurants/quan bun bo me keo.md": ["Giờ mở cửa"],
        }
    )
    path = write_dataset(tmp_path, [row])
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "Giờ mở cửa" in str(exc_info.value)


def test_declared_section_matching_heading_is_valid(tmp_path, kb):
    row = make_case(
        relevant_sections={
            "foods/restaurants/quan bun bo me keo.md": ["Tóm tắt", "Thông tin"],
        }
    )
    path = write_dataset(tmp_path, [row])
    loaded = load_dataset(path, kb_root=kb)
    assert loaded.cases[0].relevant_sections == {
        "foods/restaurants/quan bun bo me keo.md": ("Tóm tắt", "Thông tin")
    }


def test_section_presence_is_check_after_strip(tmp_path, kb):
    """Whitespace around a declared section must not break the existence check."""
    row = make_case(
        relevant_sections={
            "foods/restaurants/quan bun bo me keo.md": ["  Thông tin  "],
        }
    )
    path = write_dataset(tmp_path, [row])
    loaded = load_dataset(path, kb_root=kb)
    assert loaded.cases[0].relevant_sections == {
        "foods/restaurants/quan bun bo me keo.md": ("Thông tin",)
    }


def test_expected_count_mismatch_reported(tmp_path, kb):
    path = write_dataset(tmp_path, [make_case(), make_case()])
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb, expected_count=104)
    assert "104" in str(exc_info.value)
    assert "2" in str(exc_info.value)


def test_all_errors_are_collected_not_silent(tmp_path, kb):
    """One invalid file reports every problem, never skipping rows silently."""
    rows = [make_case(), make_case(question=""), make_case(case_id="bad-id")]
    path = write_dataset(tmp_path, rows)
    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(path, kb_root=kb)
    assert "line 2" in str(exc_info.value)
    assert "line 3" in str(exc_info.value)
