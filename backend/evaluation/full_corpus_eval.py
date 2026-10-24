"""Phase 7B evaluator full-corpus: retrieval metrics, sinh câu trả lời, judge luna, tổng hợp.

Chạy từ `backend/`:

    uv run --env-file ../.env python -m evaluation.full_corpus_eval <lệnh> ...

Mỗi case đi đúng đường runtime API (`api/app.py` + `api/routes/chat.py`): cùng
retrieval service, context builder, generator, `settings.yaml`. Kết quả chi tiết là
private, ghi JSONL vào `data/evaluation/phase_7b/`. `case_index` là chỉ số dòng
0-based trong Golden chính thức, dùng chung cho mọi run, judge và tập con.
"""

import argparse
import asyncio
import json
import math
import random
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parents[1]
for _p in (str(REPO_ROOT), str(BACKEND_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from agents import Agent, ModelSettings, RunConfig, Runner
from pydantic import BaseModel, ConfigDict, Field

from core.schema import CitationIntegrityError
from core.settings_loader import load_settings
from llm.citations import select_cited_sources
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus import build_full_corpus_retrieval_service
from retrieval.full_corpus_context import FullCorpusContextBuilder

GOLDEN_DIR = REPO_ROOT / "knowledge-base-hue" / "evaluation"
GOLDEN_FULL = GOLDEN_DIR / "golden_full_corpus.jsonl"
GOLDEN_SMOKE = GOLDEN_DIR / "golden_full_corpus_smoke.jsonl"
RESULTS_DIR = REPO_ROOT / "data" / "evaluation" / "phase_7b"
JUDGE_PROMPT_PATH = Path(__file__).resolve().parent / "full_corpus_judge_prompt.md"

# Giá gpt-6-luna (User 2026-10-24), USD cho 1M token.
PRICE_INPUT_PER_M = 0.1
PRICE_OUTPUT_PER_M = 0.5
RETRIEVAL_K = 10
CONCURRENCY = 4
JUDGE_MAX_OUTPUT_TOKENS = 1024
ANSWER_METRICS = ("accuracy", "completeness", "relevance")
RETRIEVAL_METRICS = ("mrr", "ndcg", "keyword_coverage")
OUT_OF_SCOPE = "out_of_scope"


# ---------- Golden ----------

def load_golden_cases(golden: str) -> list[dict]:
    """Trả case kèm `case_index` theo Golden chính thức; `smoke` là tập con 10 case."""
    full = [json.loads(line) for line in GOLDEN_FULL.read_text(encoding="utf-8").splitlines()]
    cases = [{"case_index": index, **row} for index, row in enumerate(full)]
    if golden == "full":
        return cases
    smoke = [json.loads(line) for line in GOLDEN_SMOKE.read_text(encoding="utf-8").splitlines()]
    # Smoke là bản sao nguyên dòng của Golden chính thức (7A), nên tìm lại vị trí bằng so khớp.
    return [cases[full.index(row)] for row in smoke]


def select_cases(cases: list[dict], case_indexes: list[int] | None) -> list[dict]:
    """`None` = mọi case; danh sách (kể cả rỗng) = đúng các case đó."""
    if case_indexes is None:
        return cases
    by_index = {case["case_index"]: case for case in cases}
    return [by_index[index] for index in case_indexes]


# ---------- Metric thuần ----------

def _fold(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def keyword_mrr(keyword: str, texts: list[str]) -> float:
    keyword = _fold(keyword)
    for rank, text in enumerate(texts, start=1):
        if keyword in _fold(text):
            return 1.0 / rank
    return 0.0


def keyword_ndcg(keyword: str, texts: list[str], k: int = RETRIEVAL_K) -> float:
    keyword = _fold(keyword)
    relevance = [int(keyword in _fold(text)) for text in texts[:k]]
    dcg = sum(value / math.log2(rank + 2) for rank, value in enumerate(relevance))
    ideal = sum(value / math.log2(rank + 2) for rank, value in enumerate(sorted(relevance, reverse=True)))
    return dcg / ideal if ideal else 0.0


def score_retrieval(keywords: list[str], texts: list[str], k: int = RETRIEVAL_K) -> dict:
    """Cùng công thức `evaluation/eval.py` `score_retrieval`: trung bình đều trên keyword."""
    texts = texts[:k]
    mrr_values = [keyword_mrr(keyword, texts) for keyword in keywords]
    ndcg_values = [keyword_ndcg(keyword, texts, k) for keyword in keywords]
    found = sum(value > 0 for value in mrr_values)
    total = len(keywords)
    return {
        "mrr": sum(mrr_values) / total if total else 0.0,
        "ndcg": sum(ndcg_values) / total if total else 0.0,
        "keywords_found": found,
        "total_keywords": total,
        "keyword_coverage": found / total * 100 if total else 0.0,
    }


def is_refusal(answer: str) -> bool:
    # Cùng điều kiện nhánh fallback của `llm/citations.py`.
    return answer.strip() == INSUFFICIENT_ANSWER


def cost_usd(input_tokens: int, output_tokens: int) -> float:
    return (input_tokens * PRICE_INPUT_PER_M + output_tokens * PRICE_OUTPUT_PER_M) / 1_000_000


def mean_by_category(rows: list[dict], fields: tuple[str, ...]) -> dict:
    """Macro-average theo case: tổng (`overall`) và theo category, kèm số case."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["category"]].append(row)

    def mean(group: list[dict]) -> dict:
        return {"n": len(group), **{f: sum(r[f] for r in group) / len(group) for f in fields}}

    summary = {"overall": mean(rows)} if rows else {"overall": {"n": 0}}
    summary.update({category: mean(group) for category, group in sorted(groups.items())})
    return summary


def refusal_rates(rows: list[dict]) -> dict:
    """Từ chối đúng trên `out_of_scope`; từ chối nhầm trên các case còn lại."""
    oos = [row for row in rows if row["category"] == OUT_OF_SCOPE]
    rest = [row for row in rows if row["category"] != OUT_OF_SCOPE]
    return {
        "correct_refusal_rate": sum(row["refusal"] for row in oos) / len(oos) if oos else None,
        "out_of_scope_n": len(oos),
        "false_refusal_rate": sum(row["refusal"] for row in rest) / len(rest) if rest else None,
        "in_scope_n": len(rest),
    }


def citation_error_rates(rows: list[dict]) -> dict:
    """Tỉ lệ case mà API sẽ trả 500 citation_integrity_error cho User."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["category"]].append(row)

    def rate(group: list[dict]) -> dict:
        return {"n": len(group), "rate": sum(bool(r["citation_error"]) for r in group) / len(group)}

    return {"overall": rate(rows), **{c: rate(g) for c, g in sorted(groups.items())}} if rows else {}


def usage_totals(rows: list[dict]) -> dict:
    input_tokens = sum(row.get("input_tokens") or 0 for row in rows)
    output_tokens = sum(row.get("output_tokens") or 0 for row in rows)
    calls = sum(1 for row in rows if row.get("input_tokens") is not None)
    return {
        "calls": calls,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd(input_tokens, output_tokens),
    }


# ---------- JSONL ----------

def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def error_case_indexes(rows: list[dict]) -> list[int]:
    return [row["case_index"] for row in rows if row["error"]]


def merge_retried(existing: list[dict], retried: list[dict]) -> list[dict]:
    """Thay các dòng chạy lại vào đúng vị trí theo `case_index`."""
    by_index = {row["case_index"]: row for row in retried}
    return [by_index.get(row["case_index"], row) for row in existing]


# ---------- Runtime components (giống `api/app.py` create_app) ----------

def build_retrieval(settings: dict, treatment: str):
    runtime = settings["full_corpus_runtime"]
    return build_full_corpus_retrieval_service(
        candidate_id=runtime["candidate_id"],
        retrieval_treatment=treatment,
        reranker=runtime["reranker"],
        settings=settings,
    )


def build_context_builder(settings: dict) -> FullCorpusContextBuilder:
    generation = settings["full_corpus_generation"]
    return FullCorpusContextBuilder(
        load_openai_tokenizer(),
        context_limit=generation["context_limit"],
        reserved_output_tokens=generation["reserved_output_tokens"],
        safety_margin=generation["safety_margin"],
        max_documents=generation["max_context_documents"],
    )


def describe_error(exc: BaseException) -> str:
    # GenerationError che lỗi provider; ghi cả nguyên nhân để biết lỗi gốc.
    text = f"{type(exc).__name__}: {exc}"
    if exc.__cause__ is not None:
        text += f" <- {type(exc.__cause__).__name__}: {exc.__cause__}"
    return text


# ---------- Retrieval eval (local, không tốn tiền) ----------

def run_retrieval_eval(cases: list[dict], treatment: str) -> list[dict]:
    """Retrieval metrics cho mọi case trừ `out_of_scope` (7A §8). Không ghi latency để
    hai lần chạy so được byte với nhau."""
    service = build_retrieval(load_settings(validate_private_paths=False), treatment)
    rows = []
    try:
        for case in cases:
            if case["category"] == OUT_OF_SCOPE:
                continue
            documents = service.search(case["question"]).documents
            rows.append({
                "case_index": case["case_index"],
                "category": case["category"],
                "treatment": treatment,
                "top_chunk_ids": [doc.id for doc in documents[:RETRIEVAL_K]],
                **score_retrieval(case["keywords"], [doc.text for doc in documents]),
            })
    finally:
        service.close()
    return rows


# ---------- Sinh câu trả lời (paid) ----------

async def answer_case(case: dict, service, context_builder, generator) -> dict:
    """Một case theo đúng thứ tự `api/routes/chat.py`: retrieval → context → sinh → citation."""
    row = {
        "case_index": case["case_index"],
        "category": case["category"],
        "answer": None,
        "refusal": None,
        "citation_error": None,
        "context_sources": None,
        "top_chunk_ids": None,
        "input_tokens": None,
        "output_tokens": None,
        "latency_ms": None,
        "response_id": None,
        "error": None,
    }
    question = case["question"].strip()
    try:
        result = await asyncio.to_thread(service.search, question)
        row["top_chunk_ids"] = [doc.id for doc in result.documents[:RETRIEVAL_K]]
        packed = context_builder.build(question, result.documents)
        row["context_sources"] = len(packed.sources)
        if not packed.sources:
            answer = INSUFFICIENT_ANSWER  # API trả fallback, không gọi model.
        else:
            generated = await generator.generate_answer(question, packed.text)
            answer = generated.text
            row.update(
                input_tokens=generated.input_tokens,
                output_tokens=generated.output_tokens,
                latency_ms=generated.latency_ms,
                response_id=generated.response_id,
            )
            try:
                select_cited_sources(answer, packed.sources)
            except CitationIntegrityError as exc:
                # API trả 500 ở đây; vẫn giữ text để chấm (A chốt 2026-10-24).
                row["citation_error"] = str(exc)
        row["answer"] = answer
        row["refusal"] = is_refusal(answer)
    except Exception as exc:  # lỗi kỹ thuật của case: ghi nguyên, run thành incomplete
        row["error"] = describe_error(exc)
    return row


async def run_generation(cases: list[dict]) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    context_builder = build_context_builder(settings)
    generator = OpenAIFullCorpusGenerator.from_environment(settings)
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async def one(case: dict) -> dict:
        async with semaphore:
            return await answer_case(case, service, context_builder, generator)

    try:
        return list(await asyncio.gather(*(one(case) for case in cases)))
    finally:
        service.close()
        await generator.aclose()


# ---------- Judge (prompt dùng chung cho Claude và luna) ----------

class JudgeScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    accuracy: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    feedback: str


def build_judge_message(question: str, reference_answer: str, answer: str) -> str:
    # Đúng định dạng đầu vào ghi trong `full_corpus_judge_prompt.md`.
    return (
        f"Câu hỏi:\n{question.strip()}\n\n"
        f"Đáp án tham chiếu:\n{reference_answer.strip()}\n\n"
        f"Câu trả lời cần chấm:\n{answer.strip()}"
    )


async def judge_case_luna(agent: Agent, case: dict, answer_row: dict) -> dict:
    row = {
        "case_index": case["case_index"],
        "accuracy": None,
        "completeness": None,
        "relevance": None,
        "feedback": None,
        "input_tokens": None,
        "output_tokens": None,
        "error": None,
    }
    message = build_judge_message(case["question"], case["reference_answer"], answer_row["answer"])
    try:
        result = await Runner.run(
            agent,
            input=message,
            max_turns=1,
            run_config=RunConfig(tracing_disabled=True, trace_include_sensitive_data=False),
        )
        usage = result.raw_responses[-1].usage if result.raw_responses else None
        if usage is not None:
            row.update(input_tokens=usage.input_tokens, output_tokens=usage.output_tokens)
        scores = result.final_output
        if not isinstance(scores, JudgeScores):
            scores = JudgeScores.model_validate_json(str(scores))
        row.update(scores.model_dump())
    except Exception as exc:
        row["error"] = describe_error(exc)
    return row


async def run_judge_luna(cases: list[dict], answer_rows: list[dict]) -> list[dict]:
    """Judge phụ: cùng model/provider/client như generation, không tham số sampling."""
    settings = load_settings(validate_private_paths=False)
    generator = OpenAIFullCorpusGenerator.from_environment(settings)
    agent = Agent(
        name="hue_full_corpus_answer_judge",
        instructions=JUDGE_PROMPT_PATH.read_text(encoding="utf-8"),
        model=generator.responses_model,
        model_settings=ModelSettings(
            max_tokens=JUDGE_MAX_OUTPUT_TOKENS, include_usage=True, store=False,
        ),
        output_type=JudgeScores,
    )
    answers = {row["case_index"]: row for row in answer_rows}
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async def one(case: dict) -> dict:
        async with semaphore:
            return await judge_case_luna(agent, case, answers[case["case_index"]])

    try:
        return list(await asyncio.gather(*(one(case) for case in cases)))
    finally:
        await generator.aclose()


def answered_cases(cases: list[dict], answer_rows: list[dict], case_indexes: list[int] | None) -> list[dict]:
    """Case cần chấm: `None` = mọi case đã có câu trả lời; `[]` = không case nào.
    Case lỗi kỹ thuật (chưa có câu trả lời) bị bỏ, vì không có gì để chấm."""
    answered = {row["case_index"] for row in answer_rows if not row["error"]}
    return [case for case in select_cases(cases, case_indexes) if case["case_index"] in answered]


def judge_input_rows(cases: list[dict], answer_rows: list[dict], seed: int) -> list[dict]:
    """File đầu vào cho judge Claude: không category, không run, không điểm; xáo theo seed."""
    answers = {row["case_index"]: row for row in answer_rows}
    rows = [
        {
            "case_index": case["case_index"],
            "question": case["question"],
            "reference_answer": case["reference_answer"],
            "answer": answers[case["case_index"]]["answer"],
        }
        for case in cases
    ]
    random.Random(seed).shuffle(rows)
    return rows


def validate_score_rows(rows: list[dict]) -> list[str]:
    """Kiểm file điểm (Claude hoặc luna) đúng schema: số nguyên 1–5, không trùng case."""
    errors = []
    seen = set()
    for row in rows:
        index = row.get("case_index")
        if index in seen:
            errors.append(f"case {index}: duplicated")
        seen.add(index)
        if row.get("error"):
            errors.append(f"case {index}: error {row['error']}")
            continue
        for metric in ANSWER_METRICS:
            value = row.get(metric)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                errors.append(f"case {index}: {metric}={value!r} is not an integer 1-5")
    return errors


# ---------- Tổng hợp ----------

def summarize_retrieval(rows: list[dict]) -> dict:
    return mean_by_category(rows, RETRIEVAL_METRICS)


def summarize_answers(answer_rows: list[dict], score_rows: list[dict] | None) -> dict:
    ok = [row for row in answer_rows if not row["error"]]
    summary = {
        "cases": len(answer_rows),
        "technical_errors": len(answer_rows) - len(ok),
        "complete": len(ok) == len(answer_rows),
        "refusal": refusal_rates(ok),
        "citation_error": citation_error_rates(ok),
        "generation_usage": usage_totals(answer_rows),
    }
    if score_rows is not None:
        category = {row["case_index"]: row["category"] for row in answer_rows}
        scored = [
            {**row, "category": category[row["case_index"]]}
            for row in score_rows if not row.get("error")
        ]
        summary["scores"] = mean_by_category(scored, ANSWER_METRICS)
        summary["score_errors"] = validate_score_rows(score_rows)
        summary["judge_usage"] = usage_totals(score_rows)
    return summary


# ---------- So điểm giữa hai nguồn (Gate 4, spec 7B §4.4) ----------

def valid_score_map(rows: list[dict]) -> dict[int, dict]:
    """Chỉ giữ dòng không lỗi và đủ ba điểm nguyên 1–5 (dòng hỏng đã được `validate_score_rows` báo)."""
    valid = {}
    for row in rows:
        if row.get("error"):
            continue
        if all(isinstance(row.get(m), int) and not isinstance(row.get(m), bool)
               and 1 <= row[m] <= 5 for m in ANSWER_METRICS):
            valid[row["case_index"]] = row
    return valid


def compare_scores(a_rows: list[dict], b_rows: list[dict], case_indexes: list[int] | None = None) -> dict:
    """So nguồn B với nguồn A trên các case cả hai cùng có điểm hợp lệ.

    Theo từng metric: chênh trung bình có dấu (B − A), tỉ lệ trùng, tỉ lệ lệch ≤1, tỉ lệ lệch ≥2.
    """
    a, b = valid_score_map(a_rows), valid_score_map(b_rows)
    # Mặc định: giao hai nguồn (vd. 176 với chấm lại 30); có --cases thì báo cả case thiếu.
    wanted = set(a) & set(b) if case_indexes is None else set(case_indexes)
    common = sorted(wanted & set(a) & set(b))
    result = {
        "n": len(common),
        "missing_in_a": sorted(wanted - set(a)),
        "missing_in_b": sorted(wanted - set(b)),
    }
    for metric in ANSWER_METRICS:
        diffs = [b[i][metric] - a[i][metric] for i in common]
        n = len(diffs)
        result[metric] = {
            "mean_signed_diff": sum(diffs) / n if n else None,
            "exact_rate": sum(d == 0 for d in diffs) / n if n else None,
            "within_1_rate": sum(abs(d) <= 1 for d in diffs) / n if n else None,
            "diff_ge_2_rate": sum(abs(d) >= 2 for d in diffs) / n if n else None,
        }
    return result


def parse_user_scores(markdown: str, question_to_case: dict[str, int]) -> tuple[list[dict], list[str]]:
    """Đọc dòng `Điểm: a / c / r` (và `Ghi chú:`) dưới mỗi `## Câu N` của file chấm User."""
    rows, errors = [], []
    sections = re.split(r"^## Câu (\d+)[ \t]*$", markdown, flags=re.MULTILINE)
    # re.split với một group: [phần đầu, số câu, nội dung, số câu, nội dung, ...]
    for number, body in zip(sections[1::2], sections[2::2]):
        if number not in question_to_case:
            errors.append(f"Câu {number}: không có trong map")
            continue
        score_lines = re.findall(r"^Điểm:[ \t]*(.*?)[ \t]*$", body, flags=re.MULTILINE)
        if len(score_lines) != 1:
            errors.append(f"Câu {number}: cần đúng một dòng `Điểm:`, thấy {len(score_lines)}")
            continue
        parts = [part.strip() for part in score_lines[0].split("/")]
        if len(parts) != 3 or not all(part in {"1", "2", "3", "4", "5"} for part in parts):
            errors.append(f"Câu {number}: điểm chưa đủ hoặc không hợp lệ: {score_lines[0]!r}")
            continue
        notes = re.findall(r"^Ghi chú:[ \t]*(.*?)[ \t]*$", body, flags=re.MULTILINE)
        rows.append({
            "case_index": question_to_case[number],
            **dict(zip(ANSWER_METRICS, (int(part) for part in parts))),
            "feedback": notes[0] if notes else "",
        })
    missing = sorted(set(question_to_case) - set(sections[1::2]), key=int)
    errors += [f"Câu {number}: không thấy trong file" for number in missing]
    return rows, errors


# ---------- Chẩn đoán từ chối nhầm ----------

def answer_keywords(case: dict) -> list[str]:
    """Keyword mang đáp án: có trong reference_answer, không có trong câu hỏi (cùng luật Golden 7A)."""
    question, reference = _fold(case["question"]), _fold(case["reference_answer"])
    return [k for k in case["keywords"] if _fold(k) not in question and _fold(k) in reference]


def classify_refusal_evidence(keywords: list[str], context_text: str) -> str:
    """`retrieval_miss`: không keyword đáp án nào trong context; `evidence_present`: có đủ;
    `partial_evidence`: có một phần (không kết luận được model sai hay context thiếu)."""
    context = _fold(context_text)
    found = sum(_fold(k) in context for k in keywords)
    if found == 0:
        return "retrieval_miss"
    return "evidence_present" if found == len(keywords) else "partial_evidence"


def diagnose_false_refusals(cases: list[dict], answer_rows: list[dict]) -> list[dict]:
    """Dựng lại đúng context của case bị từ chối nhầm (retrieval local + context builder như
    `answer_case`, không gọi sinh) rồi kiểm keyword có nằm trong context model đã thấy không."""
    by_index = {case["case_index"]: case for case in cases}
    refused = [row for row in answer_rows
               if not row["error"] and row["refusal"] and row["category"] != OUT_OF_SCOPE]
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    context_builder = build_context_builder(settings)
    rows = []
    try:
        for row in refused:
            case = by_index[row["case_index"]]
            question = case["question"].strip()
            result = service.search(question)
            packed = context_builder.build(question, result.documents)
            keywords = answer_keywords(case)
            context = _fold(packed.text)
            rows.append({
                "case_index": case["case_index"],
                "category": case["category"],
                # Retrieval tất định (Gate 1), nên context dựng lại phải trùng lần sinh.
                "same_top_chunks_as_run": [d.id for d in result.documents[:RETRIEVAL_K]] == row["top_chunk_ids"],
                "answer_keywords": len(keywords),
                "answer_keywords_in_context": sum(_fold(k) in context for k in keywords),
                "all_keywords": len(case["keywords"]),
                "all_keywords_in_context": sum(_fold(k) in context for k in case["keywords"]),
                "all_keywords_in_top10": sum(
                    any(_fold(k) in _fold(d.text) for d in result.documents[:RETRIEVAL_K])
                    for k in case["keywords"]
                ),
                "diagnosis": classify_refusal_evidence(keywords, packed.text),
            })
    finally:
        service.close()
    return rows


def count_by_category(rows: list[dict], field: str) -> dict:
    table: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        table["overall"][row[field]] += 1
        table[row["category"]][row[field]] += 1
    return {category: dict(counts) for category, counts in sorted(table.items())}


# ---------- CLI ----------

def _path(name: str) -> Path:
    path = Path(name)
    return path if path.is_absolute() or path.parent != Path(".") else RESULTS_DIR / path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evaluation.full_corpus_eval")
    commands = parser.add_subparsers(dest="command", required=True)

    retrieval = commands.add_parser("retrieval", help="retrieval metrics (local, 0 đồng)")
    retrieval.add_argument("--treatment", default="dense_bm25_rrf",
                           choices=["dense_bm25_rrf", "native_hybrid_rrf"])
    retrieval.add_argument("--golden", default="full", choices=["full", "smoke"])
    retrieval.add_argument("--out", required=True)

    generate = commands.add_parser("generate", help="sinh câu trả lời (paid)")
    generate.add_argument("--golden", default="full", choices=["full", "smoke"])
    generate.add_argument("--cases", type=int, nargs="*", help="case_index cần chạy")
    generate.add_argument("--out", required=True)

    judge = commands.add_parser("judge-luna", help="judge phụ gpt-6-luna (paid)")
    judge.add_argument("--answers", required=True)
    judge.add_argument("--cases", type=int, nargs="*", help="case_index cần chấm")
    judge.add_argument("--out", required=True)

    retry = commands.add_parser("retry", help="chạy lại các dòng có error, ghi đè vào file")
    retry.add_argument("kind", choices=["generate", "judge-luna"])
    retry.add_argument("--file", required=True)
    retry.add_argument("--answers", help="file câu trả lời (bắt buộc với judge-luna)")

    export = commands.add_parser("export-judge-input", help="file đầu vào cho judge Claude")
    export.add_argument("--answers", required=True)
    export.add_argument("--cases", type=int, nargs="*")
    export.add_argument("--seed", type=int, required=True)
    export.add_argument("--out", required=True)

    compare = commands.add_parser("compare", help="so hai file điểm: nhiễu / mức khớp (free)")
    compare.add_argument("--a", required=True, help="nguồn gốc so (ví dụ lần chấm 1)")
    compare.add_argument("--b", required=True, help="nguồn so với A (chênh = B − A)")
    compare.add_argument("--cases", type=int, nargs="*", help="giới hạn case_index")

    user = commands.add_parser("parse-user-scores", help="đọc điểm User từ user_scoring.md")
    user.add_argument("--sheet", default="user_scoring.md")
    user.add_argument("--map", default="user_scoring_map.json")
    user.add_argument("--out", default="user_scores.jsonl")

    diagnose = commands.add_parser("diagnose-refusals", help="chẩn đoán từ chối nhầm (local, free)")
    diagnose.add_argument("--answers", required=True)
    diagnose.add_argument("--out", required=True)

    summary = commands.add_parser("summarize", help="tổng hợp ra JSON (stdout)")
    summary.add_argument("--retrieval")
    summary.add_argument("--answers")
    summary.add_argument("--scores")

    args = parser.parse_args(argv)
    if args.command == "retry" and args.kind == "judge-luna" and not args.answers:
        parser.error("retry judge-luna cần --answers")
    cases = load_golden_cases("full")

    if args.command == "retrieval":
        rows = run_retrieval_eval(load_golden_cases(args.golden), args.treatment)
        write_jsonl(_path(args.out), rows)
        print(json.dumps(summarize_retrieval(rows), ensure_ascii=False, indent=2))
    elif args.command == "generate":
        selected = select_cases(load_golden_cases(args.golden), args.cases)
        rows = asyncio.run(run_generation(selected))
        write_jsonl(_path(args.out), rows)
        print(json.dumps(summarize_answers(rows, None), ensure_ascii=False, indent=2))
    elif args.command == "judge-luna":
        answer_rows = read_jsonl(_path(args.answers))
        selected = answered_cases(cases, answer_rows, args.cases)
        if not selected:
            print("no case to judge")
            return 0
        rows = asyncio.run(run_judge_luna(selected, answer_rows))
        write_jsonl(_path(args.out), rows)
        print(json.dumps(summarize_answers(answer_rows, rows), ensure_ascii=False, indent=2))
    elif args.command == "retry":
        existing = read_jsonl(_path(args.file))
        failed_indexes = error_case_indexes(existing)
        if not failed_indexes:
            print("no error rows")
            return 0
        failed = select_cases(cases, failed_indexes)
        if args.kind == "generate":
            retried = asyncio.run(run_generation(failed))
        else:
            retried = asyncio.run(run_judge_luna(failed, read_jsonl(_path(args.answers))))
        merged = merge_retried(existing, retried)
        write_jsonl(_path(args.file), merged)
        print(json.dumps({"retried": len(failed), "still_error": sum(bool(r["error"]) for r in merged),
                          "retry_usage": usage_totals(retried)}, ensure_ascii=False, indent=2))
    elif args.command == "export-judge-input":
        answer_rows = read_jsonl(_path(args.answers))
        rows = judge_input_rows(answered_cases(cases, answer_rows, args.cases), answer_rows, args.seed)
        write_jsonl(_path(args.out), rows)
        print(f"judge input: {len(rows)} rows")
    elif args.command == "compare":
        result = compare_scores(read_jsonl(_path(args.a)), read_jsonl(_path(args.b)), args.cases)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "parse-user-scores":
        mapping = json.loads(_path(args.map).read_text(encoding="utf-8"))["question_number_to_case_index"]
        rows, errors = parse_user_scores(_path(args.sheet).read_text(encoding="utf-8"), mapping)
        for error in errors:
            print(error)
        if errors:
            return 1
        write_jsonl(_path(args.out), rows)
        print(f"user scores: {len(rows)} rows")
    elif args.command == "diagnose-refusals":
        rows = diagnose_false_refusals(cases, read_jsonl(_path(args.answers)))
        write_jsonl(_path(args.out), rows)
        print(json.dumps({
            "false_refusals": len(rows),
            "same_top_chunks_as_run": sum(r["same_top_chunks_as_run"] for r in rows),
            "diagnosis": count_by_category(rows, "diagnosis"),
        }, ensure_ascii=False, indent=2))
    else:
        result = {}
        if args.retrieval:
            result["retrieval"] = summarize_retrieval(read_jsonl(_path(args.retrieval)))
        if args.answers:
            scores = read_jsonl(_path(args.scores)) if args.scores else None
            result["answers"] = summarize_answers(read_jsonl(_path(args.answers)), scores)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
