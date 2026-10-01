"""Request-scoped evidence recorder for auditing generation and grounded evidence.

Provides contextvars-based isolation so that each chat request / live smoke call
captures exact packed evidence (sources, excerpts, tokens, prompt text) and
generation metadata without mutating global production app state.
"""
from __future__ import annotations

import contextvars
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Generator


@dataclass
class RecordedEvidence:
    """Captured evidence for a single chat / generation request."""

    packed_sources_count: int = 0
    packed_token_count: int = 0
    sources: list[dict[str, Any]] = field(default_factory=list)
    packed_text: str = ""
    # Generation metadata
    response_id: str | None = None
    model: str | None = None
    latency_ms: int = 0
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    finish_reason: str | None = None
    status: str = "PENDING"
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "packed_sources_count": self.packed_sources_count,
            "packed_token_count": self.packed_token_count,
            "sources": self.sources,
            "response_id": self.response_id,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "finish_reason": self.finish_reason,
            "status": self.status,
            "error": self.error,
        }


class EvidenceRecorder:
    """Scoped collector for a single generation call."""

    def __init__(self, request_id: str | None = None) -> None:
        self.request_id = request_id
        self.evidence: RecordedEvidence | None = None

    def record_packed_context(self, packed: Any) -> None:
        """Capture the packed sources with full excerpts and metadata."""
        if self.evidence is None:
            self.evidence = RecordedEvidence()
        self.evidence.packed_sources_count = len(getattr(packed, "sources", []))
        self.evidence.packed_token_count = getattr(packed, "input_tokens", 0)
        self.evidence.packed_text = getattr(packed, "text", "")
        self.evidence.sources = [
            {
                "id": source.id,
                "title": source.title,
                "heading_path": list(source.heading_path),
                "excerpts": list(source.excerpts),
            }
            for source in getattr(packed, "sources", [])
        ]

    def record_fallback(self) -> None:
        """Record grounded fallback status."""
        if self.evidence is None:
            self.evidence = RecordedEvidence()
        self.evidence.status = "FALLBACK"

    def record_generation_result(self, generated: Any) -> None:
        """Record model response metadata immediately upon provider return."""
        if self.evidence is None:
            self.evidence = RecordedEvidence()
        self.evidence.response_id = getattr(generated, "response_id", None)
        self.evidence.model = getattr(generated, "model", None)
        self.evidence.latency_ms = getattr(generated, "latency_ms", 0)
        self.evidence.input_tokens = getattr(generated, "input_tokens", None)
        self.evidence.output_tokens = getattr(generated, "output_tokens", None)
        self.evidence.total_tokens = getattr(generated, "total_tokens", None)
        self.evidence.finish_reason = getattr(generated, "finish_reason", None)

    def mark_success(self) -> None:
        """Mark status as SUCCESS."""
        if self.evidence is None:
            self.evidence = RecordedEvidence()
        self.evidence.status = "SUCCESS"

    def record_generation_success(self, generated: Any) -> None:
        """Record model response metadata on success."""
        self.record_generation_result(generated)
        self.mark_success()

    def record_error(self, error_type: str) -> None:
        """Record error code or failure category without wiping existing metadata."""
        if self.evidence is None:
            self.evidence = RecordedEvidence()
        self.evidence.status = "ERROR"
        self.evidence.error = error_type

    def get_evidence(self) -> RecordedEvidence | None:
        return self.evidence


_current_evidence_recorder: contextvars.ContextVar[EvidenceRecorder | None] = (
    contextvars.ContextVar("current_evidence_recorder", default=None)
)


def get_current_recorder() -> EvidenceRecorder | None:
    """Retrieve the recorder bound to the current async task context."""
    return _current_evidence_recorder.get()


@contextmanager
def record_evidence(
    request_id: str | None = None,
) -> Generator[EvidenceRecorder, None, None]:
    """Context manager to bind an EvidenceRecorder to the current async context."""
    recorder = EvidenceRecorder(request_id=request_id)
    token = _current_evidence_recorder.set(recorder)
    try:
        yield recorder
    finally:
        _current_evidence_recorder.reset(token)
