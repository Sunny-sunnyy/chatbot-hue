# Phase 7 Simple Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not dispatch subagents unless the user explicitly asks for delegation.

**Goal:** Replace the rejected Phase 7 evaluation subsystem with one small, readable implementation that runs real `dense_only` retrieval, real `gpt-5.4-nano` generation, real `gpt-5.4-mini` judging, and writes two simple CSV reports.

**Architecture:** Keep four evaluation modules: data loading in `test.py`, evaluation prompts in `template.py`, retrieval/answer logic in `eval.py`, and the Gradio UI in `evaluator.py`. Reuse the existing production retrieval, context, and generation services. Start with 20 real questions in `test2.jsonl`; after that run is stable, change only the path to run the existing 104 questions.

**Tech Stack:** Python 3.13, `uv`, Pydantic, OpenAI Agents SDK, Qdrant, Gradio, standard-library CSV and concurrency tools, Jupyter.

## Global Constraints

- The approved specification is `docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md`; it overrides the old Phase 7 plan and guide wherever they conflict.
- Read `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py` and `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation` as direct Phase 7 references before editing.
- Read all notebooks under `/home/minhhieu/llm_rag/tai_lieu/rag_old_0` and `/home/minhhieu/llm_rag/tai_lieu/notebook_simple` as notebook-style references.
- Reuse the current Hue RAG backend; do not copy a second retrieval or generation implementation into `backend/evaluation/`.
- The initial implementation is `dense_only`. Do not build the hybrid comparison UI yet.
- Use `gpt-5.4-nano` for generation and `gpt-5.4-mini` for judging.
- The answer judge returns only `accuracy`, `completeness`, `relevance`, and `feedback`.
- Do not implement cost accounting, consent gates, calibration, resume, run IDs, generation run IDs, evaluation timestamps, checksums, package matching, tamper detection, partial artifacts, or layered validators.
- Do not use fake IDs, fake data, fake providers, fake artifacts, mocked provider responses, replayed outputs, or fabricated results anywhere in implementation or verification.
- Online access and the approved paid OpenAI calls are allowed. Load `.env` safely with `uv --env-file`; never print secret values.
- The active Qdrant collection is read-only.
- Keep only `backend/tests/test_evaluation.py` for Phase 7. Do not maximize test count.
- Preserve unrelated worktree changes. Do not use `git reset`, `git checkout --`, or broad deletion commands.
- Repository workflow says the implementer must not stage, commit, or push. End every task with `git diff --check` and a reviewer checkpoint.
- Use `apply_patch` for file creation, edits, and deletions.

---

## Locked file map

| Path | Responsibility |
|---|---|
| `backend/evaluation/test.py` | Load real JSONL questions from a caller-supplied path |
| `backend/evaluation/template.py` | Own the Phase 7 judge prompts |
| `backend/evaluation/eval.py` | Metrics, production services, single-case evaluation, batches, CSV output |
| `backend/evaluation/evaluator.py` | Gradio UI with two independent buttons |
| `backend/tests/test_evaluation.py` | The only Phase 7 test file |
| `knowledge-base-hue/foods/evaluation/test2.jsonl` | Twenty real questions selected from the 104-question file |
| `notebooks/07_evaluation.ipynb` | Short sequential explanation and real execution |
| `backend/evaluation/retrieval_results.csv` | Fixed retrieval output, overwritten by each run |
| `backend/evaluation/answer_results.csv` | Fixed answer output, overwritten by each run |

The following rejected modules and their dedicated tests are deleted after the new path works:

```text
backend/evaluation/answer_eval.py
backend/evaluation/artifacts.py
backend/evaluation/calibration.py
backend/evaluation/generation_eval.py
backend/evaluation/judge_eval.py
backend/evaluation/metrics.py
backend/evaluation/retrieval_eval.py
backend/evaluation/test_loader.py
backend/evaluation/results/

backend/tests/test_answer_evaluation.py
backend/tests/test_evaluation_artifacts.py
backend/tests/test_evaluation_calibration.py
backend/tests/test_evaluation_controls.py
backend/tests/test_evaluation_generation.py
backend/tests/test_evaluation_invocation_meter.py
backend/tests/test_evaluation_judge.py
backend/tests/test_evaluation_loader.py
backend/tests/test_evaluation_metrics.py
backend/tests/test_evaluation_notebook.py
backend/tests/test_evaluation_summary.py
backend/tests/test_evaluator_cli.py
backend/tests/test_retrieval_evaluation.py
```

---

### Task 1: Create the real 20-question dataset and simple loader

**Files:**
- Create: `knowledge-base-hue/foods/evaluation/test2.jsonl`
- Create: `backend/evaluation/test.py`
- Create: `backend/tests/test_evaluation.py`

**Interfaces:**
- Produces: `TestQuestion`, `DEFAULT_TEST_FILE`, `load_tests(path=DEFAULT_TEST_FILE)`.
- Consumes: the existing real `knowledge-base-hue/foods/evaluation/tests.jsonl`.

- [ ] **Step 1: Select exactly twenty real rows**

Copy the complete, unchanged JSON lines for these real case IDs from
`tests.jsonl` into `test2.jsonl`, in this order:

```python
SELECTED_CASE_IDS = [
    "foods-0001", "foods-0002", "foods-0003",       # direct_fact
    "foods-0015", "foods-0016", "foods-0017",       # temporal
    "foods-0023", "foods-0024", "foods-0025",       # comparative
    "foods-0029", "foods-0030", "foods-0031",       # relationship
    "foods-0039", "foods-0040",                     # spanning
    "foods-0050", "foods-0051",                     # holistic
    "foods-0057", "foods-0058",                     # food_knowledge
    "foods-0065", "foods-0066",                     # guide_planning
]
```

Do not rewrite questions, answers, keywords, categories, or add invented IDs.

- [ ] **Step 2: Write the first loader tests**

Start `backend/tests/test_evaluation.py` with real-data tests:

```python
from pathlib import Path

from evaluation.test import load_tests

REPO = Path(__file__).resolve().parents[2]
SMALL_DATASET = REPO / "knowledge-base-hue/foods/evaluation/test2.jsonl"
FULL_DATASET = REPO / "knowledge-base-hue/foods/evaluation/tests.jsonl"


def test_small_dataset_contains_twenty_real_questions():
    questions = load_tests(SMALL_DATASET)
    assert len(questions) == 20
    assert questions[0].question == "Quán bún bò Mệ Kéo nằm ở đâu?"
    assert questions[-1].question == "Gợi ý food tour 1 ngày ở Huế?"
    assert {q.category for q in questions} == {
        "direct_fact", "temporal", "comparative", "relationship",
        "spanning", "holistic", "food_knowledge", "guide_planning",
    }


def test_questions_have_the_fields_used_by_evaluation():
    for question in load_tests(SMALL_DATASET):
        assert question.question.strip()
        assert question.category.strip()
        assert question.reference_answer.strip()
        assert question.keywords
        assert all(keyword.strip() for keyword in question.keywords)


def test_load_tests_uses_the_supplied_path():
    assert len(load_tests(SMALL_DATASET)) == 20
    assert len(load_tests(FULL_DATASET)) == 104
```

- [ ] **Step 3: Run the tests and observe the missing module**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run python -m pytest tests/test_evaluation.py -q
```

Expected: collection fails because `evaluation.test` does not exist.

- [ ] **Step 4: Implement the loader without extra validation layers**

Create `backend/evaluation/test.py`:

```python
import json
from pathlib import Path

from pydantic import BaseModel


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEST_FILE = (
    REPO_ROOT / "knowledge-base-hue" / "foods" / "evaluation" / "test2.jsonl"
)


class TestQuestion(BaseModel):
    question: str
    keywords: list[str]
    reference_answer: str
    category: str


def load_tests(path: str | Path = DEFAULT_TEST_FILE) -> list[TestQuestion]:
    """Read evaluation questions from one JSONL file."""
    questions = []
    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                questions.append(TestQuestion.model_validate_json(line))
    return questions
```

Pydantic ignores the old source/section fields that are still present in the
104-question file. Do not add checksum or manifest validation.

- [ ] **Step 5: Verify the loader**

Run the same pytest command. Expected: three tests pass.

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run python ../knowledge-base-hue/foods/evaluation/validate_tests.py
```

Expected: the existing 104-question dataset validator passes unchanged.

- [ ] **Step 6: Check the task diff**

Run `git diff --check`. Expected: no whitespace errors. Do not stage or commit.

---

### Task 2: Add the three-score judge prompt and keyword metrics

**Files:**
- Create: `backend/evaluation/template.py`
- Create: `backend/evaluation/eval.py`
- Modify: `backend/tests/test_evaluation.py`

**Interfaces:**
- Consumes: `TestQuestion` from Task 1.
- Produces: `AnswerScores`, `RetrievalScores`, `calculate_mrr`, `calculate_ndcg`, `score_retrieval`, and `build_judge_message`.

- [ ] **Step 1: Add real-text metric tests**

Append to `backend/tests/test_evaluation.py`:

```python
import math

from evaluation.eval import calculate_mrr, calculate_ndcg


def test_mrr_uses_keyword_position_in_real_hue_text():
    texts = [
        "Bún bò Huế — giới thiệu\nNước dùng được nấu từ xương.",
        "Bún bò Mệ Kéo — địa chỉ\nQuán nằm tại 20 Bạch Đằng.",
    ]
    assert calculate_mrr("Mệ Kéo", texts) == 0.5
    assert calculate_mrr("Bạch Đằng", texts) == 0.5


def test_ndcg_uses_binary_keyword_relevance():
    texts = [
        "Bún bò Huế — giới thiệu\nNước dùng được nấu từ xương.",
        "Bún bò Mệ Kéo — địa chỉ\nQuán nằm tại 20 Bạch Đằng.",
    ]
    assert math.isclose(calculate_ndcg("Mệ Kéo", texts), 1 / math.log2(3))
    assert calculate_ndcg("không tồn tại", texts) == 0.0
```

These strings are copied from real Hue foods concepts and addresses. Do not use
invented artifact or case identifiers.

- [ ] **Step 2: Create the evaluation-owned prompts**

Create `backend/evaluation/template.py`:

```python
JUDGE_SYSTEM_PROMPT = """
Bạn là người đánh giá chất lượng câu trả lời của hệ thống RAG về ẩm thực Huế.
Hãy so sánh câu trả lời được sinh với câu trả lời tham khảo.
Chỉ cho điểm 5 khi câu trả lời thực sự xuất sắc ở tiêu chí đó.
""".strip()


def build_judge_message(question, reference_answer, generated_answer):
    return f"""Câu hỏi:
{question}

Câu trả lời tham khảo:
{reference_answer}

Câu trả lời của hệ thống:
{generated_answer}

Hãy chấm ba tiêu chí từ 1 đến 5:
- accuracy: thông tin có chính xác không;
- completeness: câu trả lời có đủ các ý quan trọng không;
- relevance: câu trả lời có đi thẳng vào câu hỏi không.

Đưa ra feedback ngắn gọn, cụ thể và dễ hiểu.
"""
```

Do not add prompt hashes, versions, evidence packages, groundedness, or calibration.

- [ ] **Step 3: Implement the pure metric section of `eval.py`**

Use these exact public models and functions:

```python
import math
from pydantic import BaseModel, Field


class RetrievalScores(BaseModel):
    mrr: float
    ndcg: float
    keywords_found: int
    total_keywords: int
    keyword_coverage: float


class AnswerScores(BaseModel):
    accuracy: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    feedback: str


def calculate_mrr(keyword: str, texts: list[str]) -> float:
    keyword = keyword.casefold()
    for rank, text in enumerate(texts, start=1):
        if keyword in text.casefold():
            return 1.0 / rank
    return 0.0


def calculate_dcg(relevance: list[int]) -> float:
    return sum(value / math.log2(rank + 2) for rank, value in enumerate(relevance))


def calculate_ndcg(keyword: str, texts: list[str], k: int = 10) -> float:
    keyword = keyword.casefold()
    relevance = [int(keyword in text.casefold()) for text in texts[:k]]
    ideal = sorted(relevance, reverse=True)
    ideal_score = calculate_dcg(ideal)
    return calculate_dcg(relevance) / ideal_score if ideal_score else 0.0


def score_retrieval(keywords: list[str], texts: list[str], k: int = 10):
    mrr_values = [calculate_mrr(keyword, texts) for keyword in keywords]
    ndcg_values = [calculate_ndcg(keyword, texts, k) for keyword in keywords]
    found = sum(value > 0 for value in mrr_values)
    total = len(keywords)
    return RetrievalScores(
        mrr=sum(mrr_values) / total if total else 0.0,
        ndcg=sum(ndcg_values) / total if total else 0.0,
        keywords_found=found,
        total_keywords=total,
        keyword_coverage=found / total * 100 if total else 0.0,
    )
```

- [ ] **Step 4: Verify pure calculations**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run python -m pytest tests/test_evaluation.py -q
```

Expected: five tests pass without calling OpenAI.

- [ ] **Step 5: Check the task diff**

Run `git diff --check`. Expected: clean. Do not stage or commit.

---

### Task 3: Connect `eval.py` to real retrieval and fixed CSV output

**Files:**
- Modify: `backend/evaluation/eval.py`
- Modify: `backend/tests/test_evaluation.py`

**Interfaces:**
- Consumes: `load_settings`, `build_service`, `ContextBuilder`, and Task 2 metrics.
- Produces: `EvaluationServices`, `build_services`, `evaluate_retrieval`, `run_retrieval_batch`, `save_csv`, `RETRIEVAL_RESULTS_FILE`.

- [ ] **Step 1: Add one real-Qdrant test**

Append:

```python
from evaluation.eval import build_services, evaluate_retrieval


def test_retrieval_evaluation_uses_the_real_dense_collection():
    question = load_tests(SMALL_DATASET)[0]
    services = build_services("dense_only")
    row = evaluate_retrieval(question, services)
    assert row["question"] == question.question
    assert row["mrr"] >= 0
    assert row["ndcg"] >= 0
    assert row["total_keywords"] == len(question.keywords)
    assert row["error"] == ""
```

This test requires the real Qdrant collection with 572 points. Do not inject a
retriever or substitute sample documents.

- [ ] **Step 2: Add the small service container and real builder**

Add to `eval.py`:

```python
import copy
import csv
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from core.settings_loader import load_settings
from llm.generator_openai import OpenAIAnswerGenerator
from retrieval.context_builder import ContextBuilder
from retrieval.service import build_service


EVALUATION_DIR = Path(__file__).resolve().parent
RETRIEVAL_RESULTS_FILE = EVALUATION_DIR / "retrieval_results.csv"
ANSWER_RESULTS_FILE = EVALUATION_DIR / "answer_results.csv"


@dataclass
class EvaluationServices:
    retrieval: object
    context: ContextBuilder
    generator: OpenAIAnswerGenerator
    judge: object
    judge_model: str


def build_services(profile: str = "dense_only") -> EvaluationServices:
    settings = copy.deepcopy(load_settings())
    settings["active_profile"] = profile
    retrieval = build_service(settings)
    context = ContextBuilder(
        max_documents=settings["retrieval"]["max_context_documents"],
        max_characters=settings["retrieval"]["max_context_characters"],
    )
    generator = OpenAIAnswerGenerator(
        model=settings["llm"]["answer_model"],
        temperature=settings["llm"]["temperature"],
        max_output_tokens=settings["llm"]["max_output_tokens"],
        timeout_seconds=settings["llm"]["timeout"],
    )
    judge_model = settings["evaluation"]["judge_model"]
    judge = None
    return EvaluationServices(retrieval, context, generator, judge, judge_model)
```

Task 4 replaces `judge = None` with `judge = build_judge(judge_model)` when the
real answer path is added. Do not make retrieval setup depend on judge setup, and
do not add identity snapshots or service validators.

- [ ] **Step 3: Implement retrieval evaluation and CSV writing**

```python
RETRIEVAL_COLUMNS = [
    "category", "question", "keywords", "mrr", "ndcg",
    "keywords_found", "total_keywords", "keyword_coverage", "error",
]


def evaluate_retrieval(test, services):
    documents = services.retrieval.search(test.question)
    scores = score_retrieval(test.keywords, [doc.text for doc in documents])
    return {
        "category": test.category,
        "question": test.question,
        "keywords": " | ".join(test.keywords),
        **scores.model_dump(),
        "error": "",
    }


def save_csv(rows, path, columns):
    with Path(path).open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def run_retrieval_batch(test_path, concurrency=3, profile="dense_only"):
    tests = load_tests(test_path)
    services = build_services(profile)

    def run_one(item):
        index, test = item
        try:
            row = evaluate_retrieval(test, services)
        except Exception as exc:
            row = {
                "category": test.category,
                "question": test.question,
                "keywords": " | ".join(test.keywords),
                "mrr": "", "ndcg": "", "keywords_found": "",
                "total_keywords": len(test.keywords), "keyword_coverage": "",
                "error": str(exc),
            }
        return index, row

    with ThreadPoolExecutor(max_workers=max(1, int(concurrency))) as executor:
        completed = list(executor.map(run_one, enumerate(tests)))
    rows = [row for _, row in sorted(completed)]
    save_csv(rows, RETRIEVAL_RESULTS_FILE, RETRIEVAL_COLUMNS)
    return rows, summarize_retrieval(rows)
```

Implement `summarize_retrieval(rows)` as a short function that averages only
numeric successful rows and returns:

```python
{"questions": len(rows), "successful": successful, "failed": failed,
 "mrr": average_mrr, "ndcg": average_ndcg,
 "keyword_coverage": average_coverage}
```

- [ ] **Step 4: Start Qdrant and run the real retrieval tests**

From repo root:

```bash
docker compose up -d
```

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
```

Expected: six tests pass using the real active collection; no collection mutation occurs.

- [ ] **Step 5: Run all twenty real retrieval questions**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -c 'from evaluation.eval import run_retrieval_batch, RETRIEVAL_RESULTS_FILE; rows, summary = run_retrieval_batch("../knowledge-base-hue/foods/evaluation/test2.jsonl", 3); print(summary); print(RETRIEVAL_RESULTS_FILE)'
```

Expected: 20 ordered result rows, a real metric summary, and
`backend/evaluation/retrieval_results.csv` containing 20 data rows.

- [ ] **Step 6: Check the task diff**

Run `git diff --check`. Expected: clean. Do not stage or commit.

---

### Task 4: Add real generation, three-score judging, and answer CSV output

**Files:**
- Modify: `backend/evaluation/eval.py`
- Modify: `backend/tests/test_evaluation.py`

**Interfaces:**
- Consumes: production `OpenAIAnswerGenerator`, `JUDGE_SYSTEM_PROMPT`, `build_judge_message`, and Task 3 services.
- Produces: `build_judge`, `evaluate_answer`, `run_answer_batch`, `summarize_answers`, `ANSWER_RESULTS_FILE`.

- [ ] **Step 1: Add one real-provider answer test**

Append:

```python
import asyncio

from evaluation.eval import evaluate_answer


def test_answer_evaluation_calls_real_generation_and_judge_models():
    question = load_tests(SMALL_DATASET)[0]
    services = build_services("dense_only")
    row = asyncio.run(evaluate_answer(question, services))
    assert row["question"] == question.question
    assert row["generated_answer"].strip()
    assert 1 <= row["accuracy"] <= 5
    assert 1 <= row["completeness"] <= 5
    assert 1 <= row["relevance"] <= 5
    assert row["feedback"].strip()
    assert row["error"] == ""
```

This is intentionally a real paid integration check. Do not replace it with a
mock runner.

- [ ] **Step 2: Build one simple three-score judge**

Add imports and builder to `eval.py`:

```python
from agents import Agent, ModelSettings, Runner

from evaluation.template import JUDGE_SYSTEM_PROMPT, build_judge_message


def build_judge(model):
    return Agent(
        name="hue_foods_answer_judge",
        instructions=JUDGE_SYSTEM_PROMPT,
        model=model,
        model_settings=ModelSettings(temperature=0, max_tokens=600),
        output_type=AnswerScores,
    )
```

In `build_services`, replace `judge = None` with:

```python
judge = build_judge(judge_model)
```

Do not add judge versions, prompt hashes, pass gates, calibration, usage, or cost handling.

- [ ] **Step 3: Implement one readable async answer flow**

```python
async def evaluate_answer(test, services):
    documents = await asyncio.to_thread(services.retrieval.search, test.question)
    context = services.context.build(documents)
    available_ids = [source["chunk_id"] for source in context.sources]
    generated = await services.generator.generate_answer(
        test.question, context.context, available_ids
    )
    judged = await Runner.run(
        services.judge,
        build_judge_message(
            test.question,
            test.reference_answer,
            generated.answer,
        ),
    )
    scores = judged.final_output
    return {
        "category": test.category,
        "question": test.question,
        "reference_answer": test.reference_answer,
        "generated_answer": generated.answer,
        "accuracy": scores.accuracy,
        "completeness": scores.completeness,
        "relevance": scores.relevance,
        "feedback": scores.feedback,
        "error": "",
    }
```

Explain in one nearby comment that `await` simply waits for the online model
without blocking other questions. Do not build a coroutine wrapper hierarchy.

- [ ] **Step 4: Implement bounded concurrent batch execution**

```python
ANSWER_COLUMNS = [
    "category", "question", "reference_answer", "generated_answer",
    "accuracy", "completeness", "relevance", "feedback", "error",
]


async def run_answer_batch(test_path, concurrency=3, profile="dense_only", progress=None):
    tests = load_tests(test_path)
    services = build_services(profile)
    semaphore = asyncio.Semaphore(max(1, int(concurrency)))
    completed = 0

    async def run_one(index, test):
        nonlocal completed
        async with semaphore:
            try:
                row = await evaluate_answer(test, services)
            except Exception as exc:
                row = {
                    "category": test.category,
                    "question": test.question,
                    "reference_answer": test.reference_answer,
                    "generated_answer": "", "accuracy": "",
                    "completeness": "", "relevance": "", "feedback": "",
                    "error": str(exc),
                }
            completed += 1
            if progress:
                progress(completed / len(tests), desc=f"Đã xong {completed}/{len(tests)} câu")
            return index, row

    results = await asyncio.gather(
        *(run_one(index, test) for index, test in enumerate(tests))
    )
    rows = [row for _, row in sorted(results)]
    save_csv(rows, ANSWER_RESULTS_FILE, ANSWER_COLUMNS)
    return rows, summarize_answers(rows)
```

Implement `summarize_answers(rows)` with the same plain pattern as retrieval,
averaging the three scores over successful rows only.

- [ ] **Step 5: Run the single real-provider test**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
```

Expected: all tests pass; the test makes one real nano generation call and one
real mini judge call. Record the observed answer and scores in the implementation
report, without printing secrets or raw provider payloads.

- [ ] **Step 6: Run the 20-question real answer evaluation**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -c 'import asyncio; from evaluation.eval import run_answer_batch, ANSWER_RESULTS_FILE; rows, summary = asyncio.run(run_answer_batch("../knowledge-base-hue/foods/evaluation/test2.jsonl", 3)); print(summary); print(ANSWER_RESULTS_FILE)'
```

Expected: 20 ordered rows produced from real retrieval, generation, and judging;
`backend/evaluation/answer_results.csv` has 20 data rows. Any real provider error
is preserved in its row and reported, not retried or hidden.

- [ ] **Step 7: Check the task diff**

Run `git diff --check`. Expected: clean. Do not stage or commit.

---

### Task 5: Build the one-file Gradio interface

**Files:**
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Rewrite: `backend/evaluation/evaluator.py`
- Modify: `backend/tests/test_evaluation.py`

**Interfaces:**
- Consumes: `run_retrieval_batch`, `run_answer_batch`, the two fixed CSV paths, and the shared test path.
- Produces: `run_retrieval_ui`, `run_answer_ui`, `build_app`, and `main`.

- [ ] **Step 1: Add Gradio through the project package manager**

From repo root run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv add gradio
```

Expected: `pyproject.toml` and `uv.lock` are updated. Do not install pandas; use
lists of dictionaries or rows directly with `gr.Dataframe`.

- [ ] **Step 2: Add a real handler-output test**

Append:

```python
from evaluation.evaluator import run_retrieval_ui


def test_retrieval_handler_returns_exactly_two_ui_outputs():
    output = run_retrieval_ui(SMALL_DATASET, 3)
    assert isinstance(output, tuple)
    assert len(output) == 2
```

This runs the real retrieval handler and protects the old yield/output mismatch
without inspecting Gradio internals or adding a fake callback.

- [ ] **Step 3: Replace `evaluator.py` with a direct UI adapter**

Use this public structure:

```python
from pathlib import Path

import gradio as gr

from evaluation.eval import (
    ANSWER_RESULTS_FILE,
    RETRIEVAL_RESULTS_FILE,
    run_answer_batch,
    run_retrieval_batch,
)
from evaluation.test import DEFAULT_TEST_FILE


def summary_text(title, summary, result_path):
    lines = [f"## {title}"]
    lines.extend(f"- {key}: {value}" for key, value in summary.items())
    lines.append(f"- File kết quả: `{result_path}`")
    return "\n".join(lines)


def run_retrieval_ui(test_path, concurrency, progress=gr.Progress()):
    rows, summary = run_retrieval_batch(test_path, concurrency, "dense_only")
    return summary_text("Kết quả retrieval", summary, RETRIEVAL_RESULTS_FILE), rows


async def run_answer_ui(test_path, concurrency, progress=gr.Progress()):
    rows, summary = await run_answer_batch(
        test_path, concurrency, "dense_only", progress
    )
    return summary_text("Kết quả câu trả lời", summary, ANSWER_RESULTS_FILE), rows


def build_app():
    with gr.Blocks(title="Đánh giá Hue RAG") as app:
        gr.Markdown("# Đánh giá Hue RAG")
        test_path = gr.Textbox(
            value=str(DEFAULT_TEST_FILE), label="File câu hỏi"
        )
        concurrency = gr.Slider(
            minimum=1, maximum=10, value=3, step=1,
            label="Số câu chạy cùng lúc",
        )
        with gr.Row():
            retrieval_button = gr.Button("Đánh giá retrieval")
            answer_button = gr.Button("Đánh giá câu trả lời")
        summary = gr.Markdown()
        results = gr.Dataframe(interactive=False, wrap=True)
        retrieval_button.click(
            run_retrieval_ui, [test_path, concurrency], [summary, results]
        )
        answer_button.click(
            run_answer_ui, [test_path, concurrency], [summary, results]
        )
    return app


def main():
    build_app().launch(inbrowser=True)


if __name__ == "__main__":
    main()
```

If the installed Gradio version represents `blocks` differently, adjust only
the small UI inspection assertion to the real public structure. Do not create a
UI abstraction layer.

- [ ] **Step 4: Run the single test file**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
```

Expected: eight readable tests pass, including real Qdrant and
real OpenAI integration.

- [ ] **Step 5: Launch and inspect the actual UI**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -m evaluation.evaluator
```

Expected: one page with the shared file path, one concurrency slider, and the
two approved buttons. Press both buttons using `test2.jsonl`; verify 20 real rows
and the two fixed CSV files. Stop the server normally after inspection.

- [ ] **Step 6: Check the task diff**

Run `git diff --check`. Expected: clean. Do not stage or commit.

---

### Task 6: Rewrite Notebook 07 in the approved teaching style

**Files:**
- Rewrite: `notebooks/07_evaluation.ipynb`

**Interfaces:**
- Consumes: only the public functions from the new four-file evaluation package.
- Produces: a clean, unexecuted canonical notebook.

- [ ] **Step 1: Replace the technical audit narrative**

Build the notebook with these eleven short sections and no extra audit sections:

```text
1. Phase 7 đánh giá điều gì?
2. Import các hàm cần dùng
3. Đọc 20 câu hỏi thật
4. Xem một câu hỏi
5. Chạy retrieval cho một câu
6. MRR và nDCG có ý nghĩa gì?
7. Sinh và chấm một câu trả lời thật
8. Xem ba điểm và feedback
9. Chạy retrieval cho 20 câu
10. Chạy answer evaluation cho 20 câu
11. Mở giao diện Gradio
```

- [ ] **Step 2: Keep each code cell short**

The notebook should use code shaped like:

```python
from evaluation.test import DEFAULT_TEST_FILE, load_tests
from evaluation.eval import (
    build_services,
    evaluate_answer,
    evaluate_retrieval,
    run_answer_batch,
    run_retrieval_batch,
)

questions = load_tests(DEFAULT_TEST_FILE)
questions[0]
```

```python
services = build_services("dense_only")
retrieval_result = evaluate_retrieval(questions[0], services)
retrieval_result
```

```python
answer_result = await evaluate_answer(questions[0], services)
answer_result
```

```python
retrieval_rows, retrieval_summary = run_retrieval_batch(DEFAULT_TEST_FILE, 3)
retrieval_summary
```

```python
answer_rows, answer_summary = await run_answer_batch(DEFAULT_TEST_FILE, 3)
answer_summary
```

```python
from evaluation.evaluator import build_app
build_app().launch()
```

Explain once in plain Vietnamese that `await` means the notebook waits for the
online model response while allowing other questions to progress.

- [ ] **Step 3: Remove all rejected notebook concepts**

Confirm the notebook contains none of:

```text
artifact, calibration, checksum, identity, package matching,
run_id, generation_run_id, confirm-paid, cost estimate, tamper
```

The notebook must not discover files on disk or recompute an audit package.

- [ ] **Step 4: Validate notebook structure**

Run from repo root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run python -c 'import nbformat; p="notebooks/07_evaluation.ipynb"; n=nbformat.read(p, 4); nbformat.validate(n); assert all(c.get("execution_count") is None for c in n.cells if c.cell_type=="code"); assert all(not c.get("outputs") for c in n.cells if c.cell_type=="code"); print(len(n.cells), "cells, clean")'
```

Expected: valid notebook, all code cells unexecuted, all outputs empty.

- [ ] **Step 5: Perform one real Run All verification on a temporary copy**

Copy the notebook to `/tmp/07_evaluation-live.ipynb` and execute that temporary
copy with the real environment. Do not save live outputs into the repository
notebook.

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file .env jupyter nbconvert --execute --to notebook notebooks/07_evaluation.ipynb --output /tmp/07_evaluation-live.ipynb --ExecutePreprocessor.timeout=1800
```

Expected: the real 20-question paths complete. If launching Gradio would block
Run All, make the final UI cell display `build_app()` instead of calling
`launch()`; keep the launch command in Markdown for the user.

- [ ] **Step 6: Check the task diff**

Run `git diff --check`. Expected: clean. Do not stage or commit.

---

### Task 7: Remove the rejected Phase 7 runtime and tests

**Files:**
- Delete: the rejected modules, test files, and artifact result directories listed in the locked file map

**Interfaces:**
- Consumes: the working four-file Phase 7 implementation from Tasks 1–6.
- Produces: one small evaluation package and one Phase 7 test file.

The session, workflow, status, and Phase 7 guide documents were already
simplified and committed before implementation began. Treat them as approved
instructions; do not rewrite them during this task.

- [ ] **Step 1: Delete only the rejected Phase 7 files**

Use `apply_patch` to delete the exact modules and tests in the locked file map.
Inventory files under the old nested `backend/evaluation/results/` directories,
then delete those old artifact files only after confirming the two new CSV files
exist. Do not delete unrelated reports, knowledge-base content, or backend tests.

- [ ] **Step 2: Confirm the package is small**

Run:

```bash
find backend/evaluation -maxdepth 1 -type f -printf '%f\n' | sort
find backend/tests -maxdepth 1 -type f -name '*evaluation*' -printf '%f\n' | sort
```

Expected Phase 7 source files:

```text
__init__.py
answer_results.csv
eval.py
evaluator.py
retrieval_results.csv
template.py
test.py
```

Expected Phase 7 test file:

```text
test_evaluation.py
```

- [ ] **Step 3: Scan for rejected concepts**

Run:

```bash
rg -n "calibrat|run_id|generation_run_id|checksum|tamper|partial\.jsonl|confirm-paid|cost_usd|InvocationMeter|matching package" backend/evaluation backend/tests/test_evaluation.py notebooks/07_evaluation.ipynb guides/phase_7_retrieval_answer_evaluation.md session_prompt
```

Expected: no rejected implementation remains. Mentions in the approved docs may
only state that a mechanism is prohibited or was rejected.

- [ ] **Step 4: Check the task diff**

Run `git diff --check`. Expected: clean. Do not stage or commit.

---

### Task 8: Complete real acceptance on 20 and then 104 questions

**Files:**
- Overwrite through the real program: `backend/evaluation/retrieval_results.csv`
- Overwrite through the real program: `backend/evaluation/answer_results.csv`
- Modify with observed results: `reports/phase_7_retrieval_answer_evaluation_implementation_report.md`

**Interfaces:**
- Consumes: the completed simple evaluation implementation.
- Produces: fresh real-system evidence for reviewer handoff.

- [ ] **Step 1: Verify active services without mutation**

Run:

```bash
docker compose ps
```

If Qdrant is not running, run `docker compose up -d`. Then from `backend/` run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s=load_settings(); c=client_from_settings(s); name=s["vector_database"]["collection_name"]; print(name, c.count(name, exact=True).count, s["active_profile"], s["llm"]["answer_model"], s["evaluation"]["judge_model"])'
```

Expected: real collection `hue_foods_e5_small_384`, 572 points,
`dense_only`, `gpt-5.4-nano`, `gpt-5.4-mini`.

- [ ] **Step 2: Run the single Phase 7 test file**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q
```

Expected: all small tests pass, including fresh real Qdrant and OpenAI checks.

- [ ] **Step 3: Re-run the 20-question acceptance**

Use the exact Task 3 and Task 4 commands. Inspect both CSV files and confirm:

- exactly 20 data rows each;
- questions remain in input order;
- no fabricated or replayed rows;
- retrieval rows contain keyword metrics;
- successful answer rows contain three scores and feedback;
- failures, if any, are visible in `error`.

Do not retry failed rows automatically. Report the truthful outcome.

- [ ] **Step 4: Switch only the data path and run all 104 real questions**

Run retrieval:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -c 'from evaluation.eval import run_retrieval_batch; rows, summary = run_retrieval_batch("../knowledge-base-hue/foods/evaluation/tests.jsonl", 3); print(summary)'
```

Run answer generation and judging:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run --env-file ../.env python -c 'import asyncio; from evaluation.eval import run_answer_batch; rows, summary = asyncio.run(run_answer_batch("../knowledge-base-hue/foods/evaluation/tests.jsonl", 3)); print(summary)'
```

Expected: real 104-row reports. Do not add cost tracking, a confirmation gate,
resume, or retry because the dataset is larger.

- [ ] **Step 5: Verify the final CSVs and notebook cleanliness**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run python -c 'import csv; from pathlib import Path; base=Path("evaluation"); print("retrieval", sum(1 for _ in csv.DictReader((base/"retrieval_results.csv").open(encoding="utf-8")))); print("answers", sum(1 for _ in csv.DictReader((base/"answer_results.csv").open(encoding="utf-8"))))'
```

Expected after the full run: `retrieval 104` and `answers 104`.

Run the notebook cleanliness validation from Task 6 again. Expected: valid,
unexecuted repository notebook with no saved outputs.

- [ ] **Step 6: Run final narrow compilation and whitespace checks**

From repo root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-simple-uv-cache uv run python -m py_compile backend/evaluation/test.py backend/evaluation/template.py backend/evaluation/eval.py backend/evaluation/evaluator.py backend/tests/test_evaluation.py
git diff --check
```

Expected: both commands succeed.

- [ ] **Step 7: Final reviewer handoff**

The handoff must state plainly:

- what was removed;
- what the four new files do;
- whether all 20 and all 104 real questions completed;
- real retrieval and three-score answer summaries;
- every failed row;
- how to launch the UI;
- that no fake, mock, replay, cost, calibration, resume, identity, checksum,
  package, or tamper path remains;
- that Phase 8 is still blocked pending the Phase 6 -> Phase 0 simplicity reviews.

Do not stage, commit, push, or approve the implementation. Hand it to the Codex
Reviewer for independent source review and real re-execution.

---

## Self-review checklist

- [ ] Every approved Phase 7 file and interface appears in a task.
- [ ] The plan creates only one Phase 7 test file.
- [ ] The plan includes real Qdrant, real nano generation, and real mini judging.
- [ ] The plan never uses fake or mocked evidence.
- [ ] The plan has no calibration, cost, consent, resume, identity, checksum,
      matching-package, or tamper implementation.
- [ ] The UI has exactly the two approved actions and one shared concurrency control.
- [ ] The plan starts with 20 real questions and then switches only the path to 104.
- [ ] Notebook 07 follows the two approved full-path style references.
- [ ] The two Phase 7 code references are not imposed as implementation blueprints on Phase 0–6.
- [ ] Project docs record the Phase 6 -> Phase 0 review gate before Phase 8.
- [ ] Every step contains the exact action, command, interface, and expected result it needs.
