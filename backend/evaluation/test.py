import json
from pathlib import Path

from pydantic import BaseModel, Field


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEST_FILE = (
    REPO_ROOT / "knowledge-base-hue" / "foods" / "evaluation" / "test2.jsonl"
)


class TestQuestion(BaseModel):
    case_id: str = ""
    question: str
    keywords: list[str]
    reference_answer: str
    category: str
    evidence: dict[str, list[str]] = Field(default_factory=dict)


def load_tests(path: str | Path = DEFAULT_TEST_FILE) -> list[TestQuestion]:
    """Read evaluation questions from one JSONL file."""
    questions = []
    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                questions.append(TestQuestion.model_validate_json(line))
    return questions
