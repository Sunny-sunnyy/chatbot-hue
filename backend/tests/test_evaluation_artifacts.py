"""Pure contract tests for evaluation run artifacts (atomic, resumable).

Temp directories only; no real run touches these helpers in tests.
"""

import json

import pytest

from evaluation.artifacts import (
    DatasetIntegrityError,
    append_partial,
    finalize_run,
    load_partial,
    make_run_id,
    read_records,
    write_summary,
)


def test_make_run_id_has_stage_profile_timestamp_and_checksum():
    """run_id carries timestamp UTC+7, profile and shortened dataset checksum."""
    run_id = make_run_id(
        "retrieval",
        "hybrid_rerank",
        "cf601f161a443123198dc66e73d97ab1f2052a01e4b0f87446fef5a86c47862c",
        timestamp="20260822-142157",
    )
    assert run_id == (
        "retrieval-20260822-142157-hybrid_rerank-cf601f16"
    )
    # same inputs -> same id (deterministic for resume)
    assert run_id == make_run_id(
        "retrieval",
        "hybrid_rerank",
        "cf601f161a443123198dc66e73d97ab1f2052a01e4b0f87446fef5a86c47862c",
        timestamp="20260822-142157",
    )


def test_append_partial_flushes_one_record(tmp_path):
    """Every appended record is flushed and stays queryable during a run."""
    path = tmp_path / "retrieval" / "run.partial.jsonl"
    append_partial(path, {"case_id": "foods-0001", "status": "complete"})
    append_partial(path, {"case_id": "foods-0002", "status": "retrieval_error"})
    records = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(records) == 2
    assert records[1]["case_id"] == "foods-0002"
    assert records[1]["status"] == "retrieval_error"


def test_load_partial_returns_only_complete_records(tmp_path):
    path = tmp_path / "retrieval" / "run.partial.jsonl"
    append_partial(path, {"case_id": "foods-0001", "status": "complete"})
    append_partial(path, {"case_id": "foods-0002", "status": "provider_error"})
    done = load_partial(path)
    assert [r["case_id"] for r in done] == ["foods-0001"]
    assert load_partial(path / "does-not-exist.jsonl") == []


def test_finalize_run_moves_partial_and_never_overwrites(tmp_path):
    partial = tmp_path / "retrieval" / "run.partial.jsonl"
    target = tmp_path / "retrieval" / "run.jsonl"
    append_partial(partial, {"case_id": "foods-0001", "status": "complete"})
    finalize_run(partial, target)
    assert not partial.exists()
    assert [json.loads(line) for line in target.read_text().splitlines()][0]["case_id"] == "foods-0001"
    # finalizing into an existing target must fail, never overwrite.
    with pytest.raises(FileExistsError):
        finalize_run(partial, target)


def test_write_summary_is_atomic_and_no_overwrite(tmp_path):
    path = tmp_path / "retrieval" / "run.summary.json"
    write_summary(path, {"status": "complete", "cases": 104})
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == {"status": "complete", "cases": 104}
    with pytest.raises(FileExistsError):
        write_summary(path, {"status": "new"})


def test_read_records_rejects_corrupt_jsonl(tmp_path):
    path = tmp_path / "run.jsonl"
    path.write_text('{"case_id": broken\n', encoding="utf-8")
    with pytest.raises(DatasetIntegrityError):
        read_records(path)
    path.write_text('{"a": 1}\nnot json\n', encoding="utf-8")
    with pytest.raises(DatasetIntegrityError):
        read_records(path)
