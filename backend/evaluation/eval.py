import asyncio
import copy
import csv
import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from agents import Agent, ModelSettings, Runner
from pydantic import BaseModel, Field

from core.settings_loader import load_settings
from evaluation.template import JUDGE_SYSTEM_PROMPT, build_judge_message
from evaluation.test import DEFAULT_TEST_FILE, TestQuestion, load_tests
from llm.generator_openai import OpenAIAnswerGenerator
from llm.prompt import INSUFFICIENT_ANSWER
from retrieval.context_builder import ContextBuilder
from retrieval.service import build_service

EVALUATION_DIR = Path(__file__).resolve().parent
RETRIEVAL_RESULTS_FILE = EVALUATION_DIR / "retrieval_results.csv"
ANSWER_RESULTS_FILE = EVALUATION_DIR / "answer_results.csv"

RETRIEVAL_COLUMNS = [
    "category",
    "question",
    "keywords",
    "mrr",
    "ndcg",
    "keywords_found",
    "total_keywords",
    "keyword_coverage",
    "error",
]

ANSWER_COLUMNS = [
    "category",
    "question",
    "reference_answer",
    "generated_answer",
    "accuracy",
    "completeness",
    "relevance",
    "feedback",
    "error",
]


class RetrievalScores(BaseModel):
    mrr: float
    ndcg: float
    keywords_found: int
    total_keywords: int
    keyword_coverage: float


class AnswerScores(BaseModel):
    """Evaluation scores and feedback for generated answers against reference answers."""

    accuracy: int = Field(
        ge=1,
        le=5,
        description="Factual correctness compared to the reference answer (1: substantially wrong, 3: acceptable, 5: perfectly accurate)",
    )
    completeness: int = Field(
        ge=1,
        le=5,
        description="Completeness in covering key reference answer points (5 only if all key information is included)",
    )
    relevance: int = Field(
        ge=1,
        le=5,
        description="Direct relevance to the question without extraneous details (5 only if completely relevant)",
    )
    feedback: str = Field(
        description="Concise, specific feedback explaining the assigned scores",
    )


@dataclass
class EvaluationServices:
    retrieval: object
    context: ContextBuilder
    generator: OpenAIAnswerGenerator
    judge: object
    judge_model: str


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


def score_retrieval(keywords: list[str], texts: list[str], k: int = 10) -> RetrievalScores:
    mrr_values = [calculate_mrr(keyword, texts) for keyword in keywords]
    ndcg_values = [calculate_ndcg(keyword, texts, k) for keyword in keywords]
    keywords_found = sum(value > 0 for value in mrr_values)
    total_keywords = len(keywords)
    avg_mrr = sum(mrr_values) / total_keywords if total_keywords else 0.0
    avg_ndcg = sum(ndcg_values) / total_keywords if total_keywords else 0.0
    keyword_coverage = (keywords_found / total_keywords * 100) if total_keywords else 0.0
    return RetrievalScores(
        mrr=avg_mrr,
        ndcg=avg_ndcg,
        keywords_found=keywords_found,
        total_keywords=total_keywords,
        keyword_coverage=keyword_coverage,
    )


def build_judge(model: str):
    return Agent(
        name="hue_foods_answer_judge",
        instructions=JUDGE_SYSTEM_PROMPT,
        model=model,
        model_settings=ModelSettings(temperature=0, max_tokens=600),
        output_type=AnswerScores,
    )


def build_services(profile: str = "dense_only", collection_name: str | None = None) -> EvaluationServices:
    settings = copy.deepcopy(load_settings())
    settings["active_profile"] = profile
    if collection_name is not None:
        settings["vector_database"]["collection_name"] = collection_name
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
    judge = build_judge(judge_model)
    return EvaluationServices(retrieval, context, generator, judge, judge_model)


def evaluate_retrieval(test: TestQuestion, services: EvaluationServices) -> dict:
    documents = services.retrieval.search(test.question)
    scores = score_retrieval(test.keywords, [doc.text for doc in documents])
    return {
        "category": test.category,
        "question": test.question,
        "keywords": " | ".join(test.keywords),
        **scores.model_dump(),
        "error": "",
    }


async def evaluate_answer(test: TestQuestion, services: EvaluationServices) -> dict:
    documents = await asyncio.to_thread(
        services.retrieval.search,
        test.question,
    )
    context = services.context.build(documents)
    if context:
        generated_answer = await services.generator.generate_answer(
            test.question,
            context,
        )
    else:
        generated_answer = INSUFFICIENT_ANSWER

    judged = await Runner.run(
        services.judge,
        build_judge_message(
            test.question,
            test.reference_answer,
            generated_answer,
        ),
    )
    scores = judged.final_output
    return {
        "category": test.category,
        "question": test.question,
        "reference_answer": test.reference_answer,
        "generated_answer": generated_answer,
        "accuracy": scores.accuracy,
        "completeness": scores.completeness,
        "relevance": scores.relevance,
        "feedback": scores.feedback,
        "error": "",
    }


def save_csv(rows: list[dict], path: str | Path, columns: list[str]) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def summarize_retrieval(rows: list[dict]) -> dict:
    successful_rows = [r for r in rows if r.get("error") == ""]
    successful = len(successful_rows)
    failed = len(rows) - successful
    if successful > 0:
        avg_mrr = sum(float(r["mrr"]) for r in successful_rows) / successful
        avg_ndcg = sum(float(r["ndcg"]) for r in successful_rows) / successful
        avg_coverage = sum(float(r["keyword_coverage"]) for r in successful_rows) / successful
    else:
        avg_mrr = 0.0
        avg_ndcg = 0.0
        avg_coverage = 0.0
    return {
        "questions": len(rows),
        "successful": successful,
        "failed": failed,
        "mrr": round(avg_mrr, 4),
        "ndcg": round(avg_ndcg, 4),
        "keyword_coverage": round(avg_coverage, 2),
    }


def summarize_answers(rows: list[dict]) -> dict:
    successful_rows = [r for r in rows if r.get("error") == ""]
    successful = len(successful_rows)
    failed = len(rows) - successful
    if successful > 0:
        avg_accuracy = sum(float(r["accuracy"]) for r in successful_rows) / successful
        avg_completeness = sum(float(r["completeness"]) for r in successful_rows) / successful
        avg_relevance = sum(float(r["relevance"]) for r in successful_rows) / successful
    else:
        avg_accuracy = 0.0
        avg_completeness = 0.0
        avg_relevance = 0.0
    return {
        "questions": len(rows),
        "successful": successful,
        "failed": failed,
        "accuracy": round(avg_accuracy, 2),
        "completeness": round(avg_completeness, 2),
        "relevance": round(avg_relevance, 2),
    }


def run_retrieval_batch(
    test_path: str | Path = DEFAULT_TEST_FILE,
    concurrency: int = 3,
    profile: str = "dense_only",
    collection_name: str | None = None,
) -> tuple[list[dict], dict]:
    tests = load_tests(test_path)
    services = build_services(profile, collection_name=collection_name)

    def run_one(item):
        index, test = item
        try:
            row = evaluate_retrieval(test, services)
        except Exception as exc:
            row = {
                "category": test.category,
                "question": test.question,
                "keywords": " | ".join(test.keywords),
                "mrr": "",
                "ndcg": "",
                "keywords_found": "",
                "total_keywords": len(test.keywords),
                "keyword_coverage": "",
                "error": str(exc),
            }
        return index, row

    with ThreadPoolExecutor(max_workers=max(1, int(concurrency))) as executor:
        completed = list(executor.map(run_one, enumerate(tests)))
    rows = [row for _, row in sorted(completed)]
    save_csv(rows, RETRIEVAL_RESULTS_FILE, RETRIEVAL_COLUMNS)
    return rows, summarize_retrieval(rows)


async def run_answer_batch(
    test_path: str | Path = DEFAULT_TEST_FILE,
    concurrency: int = 3,
    profile: str = "dense_only",
    progress=None,
    collection_name: str | None = None,
) -> tuple[list[dict], dict]:
    tests = load_tests(test_path)
    services = build_services(profile, collection_name=collection_name)
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
                    "generated_answer": "",
                    "accuracy": "",
                    "completeness": "",
                    "relevance": "",
                    "feedback": "",
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
