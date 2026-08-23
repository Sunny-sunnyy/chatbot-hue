"""Atomic, resumable artifact management for evaluation runs.

A run writes one per-case JSONL line (partial file) that is flushed after
every case, so a crash keeps every completed record. Resume only trusts
status-complete records of the same run; finalizing moves the partial to its
immutable final name with os.replace and never overwrites an existing final
file. Nothing here deletes artifacts.
"""
import json
import os
from pathlib import Path

CHECKSUM_TRUNC = 8


class DatasetIntegrityError(ValueError):
    """Raised when an artifact file is not well-formed JSONL."""


def make_run_id(stage, profile, dataset_checksum, timestamp):
    """Immutable run id: stage, UTC+7 timestamp, profile, shortened checksum."""
    return f"{stage}-{timestamp}-{profile}-{dataset_checksum[:CHECKSUM_TRUNC]}"


def append_partial(path, record):
    """Append one record and flush it; the parent directory is created."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()


def load_partial(path):
    """Return the status-complete records of a partial run file."""
    path = Path(path)
    if not path.exists():
        return []
    records = read_records(path)
    return [record for record in records if record.get("status") == "complete"]


def replace_partial(path, records):
    """Atomically rewrite a partial run file with the given records.

    Partial files are mutable by design: a resumed run rewrites the working
    file so each case has exactly one final effective row. The final JSONL
    artifact stays immutable; only the working partial file is replaced.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
    os.replace(tmp, path)


def finalize_run(partial_path, target_path):
    """Atomically rename a partial file to its final name; never overwrites."""
    partial = Path(partial_path)
    target = Path(target_path)
    if target.exists():
        raise FileExistsError(f"refusing to overwrite existing artifact {target}")
    os.replace(partial, target)


def write_summary(path, payload):
    """Atomically write one summary JSON.

    A completed summary (status != "partial") is immutable and never
    overwritten; a running summary (status == "partial") of the same run may
    be replaced atomically, which is how a resumed run completes.
    """
    path = Path(path)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing.get("status") != "partial":
            raise FileExistsError(f"refusing to overwrite existing summary {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=1)
        handle.flush()
    os.replace(tmp, path)


def read_records(path):
    """Read one JSONL artifact, failing loudly on any malformed line."""
    path = Path(path)
    records = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise DatasetIntegrityError(
                    f"{path} line {line_no}: invalid JSON: {exc.msg}"
                ) from exc
    return records
