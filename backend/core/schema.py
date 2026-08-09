"""Shared runtime data models."""
from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievedDocument:
    """Document returned by retrieval for prompt context building."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]
