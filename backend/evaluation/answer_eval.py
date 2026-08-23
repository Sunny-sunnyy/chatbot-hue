"""Answer generation and LLM-as-judge helpers.

The generation/judge record builders, rubric scoring, retry policy and judge
input construction are pure; the AnswerJudge class wraps the real OpenAI
Agents SDK call (imported lazily so pure tests and the notebook never need
provider access just to import this module).
"""
import asyncio
import json
import os
import time
from pathlib import Path

from pydantic import BaseModel

JUDGE_DIMENSIONS = ("accuracy", "completeness", "relevance", "groundedness")
JUDGE_MIN_SCORE = 1
JUDGE_MAX_SCORE = 5
JUDGE_PASS_ACCURACY = 4
JUDGE_PASS_GROUNDEDNESS = 4
JUDGE_PASS_MEAN = 4.0
JUDGE_HARD_FLOOR = 3

# One retry max, and only for transient/structural failures. Low judge scores
# are evidence, never a retry reason.
RETRYABLE_ERRORS = (
    "timeout",
    "transient_network",
    "invalid_structured_output",
)

RUBRIC_VERSION = "v1"


def _prompt_hash(system_prompt: str) -> str:
    import hashlib

    return hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------------ hashes
RUBRIC_PROMPT_HASH = None      # filled after RUBRIC_SYSTEM is defined
GENERATION_PROMPT_HASH = None  # filled after RUBRIC_SYSTEM is defined
CALIBRATION_SAMPLE_COUNT = 8


class JudgeTimeoutError(RuntimeError):
    """Raised when the judge call exceeds the provider timeout."""


class JudgeUnavailableError(RuntimeError):
    """Raised when the judge call fails at the provider level."""


class JudgeInvalidOutputError(RuntimeError):
    """Raised when the judge output is not a valid 1-5 structured score."""


def _usage_tokens(result):
    """Compact token summary from the run result when available (same as generator)."""
    for raw in getattr(result, "raw_responses", None) or []:
        usage = getattr(raw, "usage", None)
        if usage is None:
            continue
        tokens_in = getattr(usage, "input_tokens", None)
        tokens_out = getattr(usage, "output_tokens", None)
        if tokens_in is not None and tokens_out is not None:
            return {"input": tokens_in, "output": tokens_out}
    return None


def validate_judge_scores(scores):
    """Validate the four 1-5 integer rubric dimensions; return them as ints."""
    if set(scores) != set(JUDGE_DIMENSIONS):
        raise ValueError(
            f"judge scores must carry exactly {sorted(JUDGE_DIMENSIONS)}"
        )
    validated = {}
    for dimension, value in scores.items():
        if not isinstance(value, int) or not (
            JUDGE_MIN_SCORE <= value <= JUDGE_MAX_SCORE
        ):
            raise ValueError(
                f"judge dimension {dimension!r} must be an integer "
                f"{JUDGE_MIN_SCORE}-{JUDGE_MAX_SCORE}, got {value!r}"
            )
        validated[dimension] = value
    return validated


def judge_passes(scores):
    """One answer passes when floors hold and no dimension under the hard floor."""
    mean = sum(scores.values()) / len(scores)
    return (
        scores["accuracy"] >= JUDGE_PASS_ACCURACY
        and scores["groundedness"] >= JUDGE_PASS_GROUNDEDNESS
        and mean >= JUDGE_PASS_MEAN
        and min(scores.values()) >= JUDGE_HARD_FLOOR
    )


def is_retryable(error_type):
    """Retry only timeout/transient connection/invalid structured output."""
    return error_type in RETRYABLE_ERRORS


def build_judge_input(
    *,
    question,
    reference_answer,
    answer,
    evidence,
    rubric_version,
):
    """Judge input: the current case only; never the full KB or other cases."""
    return {
        "question": question,
        "reference_answer": reference_answer,
        "grounded_answer": answer,
        "evidence": evidence,
        "rubric_version": rubric_version,
    }


def entity_record(source, section, text, score=None):
    """One bounded evidence item exactly as the generator used it."""
    return {
        "source": source,
        "section": section,
        "text": text,
        "score": score,
    }


def generation_record(
    *,
    run_id,
    timestamp_utc_plus_7,
    dataset_path,
    dataset_checksum,
    config_checksum,
    case_id,
    category,
    question,
    reference_answer,
    answer,
    used_sources,
    used_evidence,
    answer_model,
    prompt_hash,
    latency_ms,
    usage_tokens,
    cost_usd,
    corpus_checksum=None,
    collection_name=None,
    calibration_run_id=None,
    usage_is_estimate=False,
    status="complete",
    error_type=None,
    attempts=1,
    cost_usd_total=None,
    attempt_ids=None,
):
    """One generation record; keeps the model/usage/cost evidence."""
    return {
        "run_id": run_id,
        "timestamp_utc_plus_7": timestamp_utc_plus_7,
        "dataset_path": dataset_path,
        "dataset_checksum": dataset_checksum,
        "config_checksum": config_checksum,
        "corpus_checksum": corpus_checksum,
        "collection_name": collection_name,
        "calibration_run_id": calibration_run_id,
        "case_id": case_id,
        "category": category,
        "question": question,
        "reference_answer": reference_answer,
        "generated_answer": answer,
        "used_sources": used_sources,
        "used_evidence": used_evidence,
        "answer_model": answer_model,
        "prompt_hash": prompt_hash,
        "latency_ms": latency_ms,
        "usage_tokens": usage_tokens,
        "cost_usd": cost_usd,
        "cost_usd_total": cost_usd_total if cost_usd_total is not None else cost_usd,
        "usage_is_estimate": usage_is_estimate,
        "status": status,
        "error_type": error_type,
        "attempts": attempts,
        "attempt_ids": attempt_ids or [],
    }


def judge_record(
    *,
    run_id,
    timestamp_utc_plus_7,
    case_id,
    category,
    generation_run_id,
    rubric_version,
    prompt_hash,
    scores,
    feedback,
    judge_model,
    dataset_checksum=None,
    config_checksum=None,
    samples_checksum=None,
    corpus_checksum=None,
    collection_name=None,
    calibration_run_id=None,
    latency_ms=None,
    usage_tokens=None,
    cost_usd=0.0,
    attempts=1,
    cost_usd_total=None,
    attempt_ids=None,
    status="complete",
    error_type=None,
):
    """One judge record; low-scoring rows are kept, never dropped silently.

    samples_checksum binds calibration rows to the exact frozen sample file
    content so a content swap under the same ids cannot pass reuse.
    """
    return {
        "run_id": run_id,
        "timestamp_utc_plus_7": timestamp_utc_plus_7,
        "case_id": case_id,
        "category": category,
        "generation_run_id": generation_run_id,
        "rubric_version": rubric_version,
        "prompt_hash": prompt_hash,
        "scores": scores,
        "feedback": feedback,
        "judge_model": judge_model,
        "dataset_checksum": dataset_checksum,
        "config_checksum": config_checksum,
        "samples_checksum": samples_checksum,
        "corpus_checksum": corpus_checksum,
        "collection_name": collection_name,
        "calibration_run_id": calibration_run_id,
        "latency_ms": latency_ms,
        "usage_tokens": usage_tokens,
        "cost_usd": cost_usd,
        "cost_usd_total": cost_usd_total if cost_usd_total is not None else cost_usd,
        "attempts": attempts,
        "attempt_ids": attempt_ids or [],
        "status": status,
        "error_type": error_type,
    }


# Judge provider integration
RUBRIC_SYSTEM = (
    "Bạn là giám khảo chất lượng cho câu trả lời grounded của trợ lý ẩm thực Huế.\n"
    "Input là một JSON document với trường question, reference_answer, "
    "grounded_answer, evidence và rubric_version.\n"
    "Chấm mỗi dimension thang điểm 1-5: accuracy (Đúng về mặt nội dung so với "
    "reference/evidence; mâu thuẫn không được điểm cao), completeness (bao phủ "
    "ý cần thiết trong reference, không cần sao chép từ ngữ), relevance (trả "
    "đúng câu hỏi, không lạc đề), groundedness (mọi claim phải có support trong "
    "evidence được cung cấp).\n"
    "Feedback ngắn gọn, nêu lỗi chính thực sự (nếu có) dựa trên evidence.\n"
    "Chỉ dựa trên input của case hiện tại; không tham chiếu kiến thức bên ngoài.\n"
    "Trả về đúng schema JSON: accuracy, completeness, relevance, groundedness, "
    "feedback.\n"
)


RUBRIC_PROMPT_HASH = _prompt_hash(RUBRIC_SYSTEM)
import llm.prompt as _llm_prompt

GENERATION_PROMPT_HASH = _prompt_hash(_llm_prompt.SYSTEM_INSTRUCTIONS)


class JudgeOutput(BaseModel):
    """Structured output of the answer judge; 1-5 integers per dimension."""

    accuracy: int
    completeness: int
    relevance: int
    groundedness: int
    feedback: str


class AnswerJudge:
    """Real OpenAI Agents SDK judge over one fixed model and rubric.

    The judge is deliberately separate from the answer generator model. Every
    failure raises a typed error; there is no fake or replay path.
    """

    def __init__(
        self,
        *,
        model: str,
        api_key_env: str = "OPENAI_API_KEY",
        timeout_seconds: float = 45.0,
    ):
        from agents import Agent, ModelSettings, Runner  # lazy: keep pure imports key-free

        self._model = model
        self._timeout_seconds = timeout_seconds
        self._runner = Runner
        self.configured = bool(
            os.environ.get(api_key_env, "").strip()
        )
        self._agent = Agent(
            name="hue_foods_answer_judge",
            instructions=RUBRIC_SYSTEM,
            model=model,
            model_settings=ModelSettings(
                temperature=0.0,
                max_tokens=JUDGE_MAX_OUTPUT_TOKENS,
            ),
            output_type=JudgeOutput,
        )

    @property
    def model(self):
        return self._model

    async def judge(self, question, reference_answer, answer, evidence):
        """Judge one answer; raises typed errors on provider failures."""
        if not self.configured:
            raise RuntimeError("judge is not configured: OPENAI_API_KEY missing")
        payload = build_judge_input(
            question=question,
            reference_answer=reference_answer,
            answer=answer,
            evidence=evidence,
            rubric_version=RUBRIC_VERSION,
        )
        started = time.monotonic()
        try:
            result = await asyncio.wait_for(
                self._runner.run(self._agent, json.dumps(payload, ensure_ascii=False)),
                timeout=self._timeout_seconds,
            )
        except asyncio.TimeoutError as exc:  # provider timeout is real failure
            raise JudgeTimeoutError("judge call timed out") from exc
        except Exception as exc:  # provider/API/connection failures
            raise JudgeUnavailableError("judge call failed") from exc
        output = result.final_output
        if not isinstance(output, JudgeOutput):
            raise JudgeInvalidOutputError("judge returned an unexpected type")
        try:
            scores = validate_judge_scores({
                "accuracy": output.accuracy,
                "completeness": output.completeness,
                "relevance": output.relevance,
                "groundedness": output.groundedness,
            })
        except ValueError as exc:  # out-of-range or missing dimension
            raise JudgeInvalidOutputError(str(exc)) from exc
        if not output.feedback or not output.feedback.strip():
            raise JudgeInvalidOutputError("judge returned blank feedback")
        return {
            "scores": scores,
            "feedback": output.feedback.strip(),
            "latency_ms": round((time.monotonic() - started) * 1000),
            "usage_tokens": _usage_tokens(result),
        }


# ------------------------------------------------------------- orchestration core
from evaluation.budget import (
    BUDGET_SCHEMA_VERSION,
    BudgetIntegrityError,
    CallBudget,
    CallBudgetExceeded,
    UnknownModelError,
    compute_pricing_checksum,
    cost_estimate_usd,
    EST_PRICE_PER_1M,
)

# Judge runtime output bound AND reservation budget (they must match: the
# runtime caps the judge at JUDGE_MAX_OUTPUT_TOKENS, the reserve uses the same
# bound so a real long output can never exceed the reserved estimate).
JUDGE_MAX_OUTPUT_TOKENS = 700


def generation_reserve_tokens(settings):
    """Conservative (input, output) token bounds for one generation call.

    The output bound is the real runtime maximum (llm.max_output_tokens); the
    input bound covers the whole bounded context plus system/answer framing.
    """
    max_output = settings["llm"]["max_output_tokens"]
    max_input = round(settings["retrieval"]["max_context_characters"] / 2.5) + 2048
    return max_input, max_output


def judge_reserve_tokens():
    """Conservative (input, output) token bounds for one judge call."""
    return 3200, JUDGE_MAX_OUTPUT_TOKENS


class CalibrationPackageError(ValueError):
    """Raised when a calibration artifact does not match the exact package."""


def calibration_gate(completed_rows, samples):
    """Good answers keep accuracy/groundedness >=4; bad answers fail <=2 on one.

    Rows and samples are matched by generation_run_id because good and bad
    samples of the same case share case_id.
    """
    good_ids = {s["generation_run_id"] for s in samples if s.get("is_good")}
    bad_ids = {s["generation_run_id"] for s in samples if not s.get("is_good")}
    rows_by_gid = {r["generation_run_id"]: r for r in completed_rows}
    if not (good_ids | bad_ids):
        return False
    for gid in good_ids:
        row = rows_by_gid.get(gid)
        if not row or row.get("status") != "complete":
            return False
        if row["scores"]["accuracy"] < JUDGE_PASS_ACCURACY or row["scores"]["groundedness"] < JUDGE_PASS_GROUNDEDNESS:
            return False
    for gid in bad_ids:
        row = rows_by_gid.get(gid)
        if not row or row.get("status") != "complete":
            return False
        if row["scores"]["accuracy"] > 2 and row["scores"]["groundedness"] > 2:
            return False
    return True


def validate_calibration_package(
    rows,
    samples,
    *,
    dataset_checksum,
    config_checksum,
    samples_checksum,
    judge_model,
    rubric_version,
    prompt_hash,
    summary=None,
):
    """Validate an immutable calibration package; refuse any mismatch.

    Raises CalibrationPackageError on: wrong row count, any non-complete row,
    missing/empty scores, wrong generation_run_id mapping, missing or wrong
    dataset/config/samples checksum on ANY row, missing/wrong/failed summary,
    judge model, rubric version or prompt hash mismatch, impossible gate.
    samples_checksum binds the package to the exact frozen sample content.
    The summary (when given) is a required part of the identity: it must
    exist, record a passing gate and carry the same run/model/rubric/prompt/
    checksums.
    """
    if len(rows) != CALIBRATION_SAMPLE_COUNT or len(samples) != CALIBRATION_SAMPLE_COUNT:
        raise CalibrationPackageError(
            f"calibration must have {CALIBRATION_SAMPLE_COUNT} rows/samples"
        )
    sample_gids = {s["generation_run_id"] for s in samples}
    incomplete = [r for r in rows if r.get("status") != "complete"]
    if incomplete:
        raise CalibrationPackageError("calibration contains incomplete rows")
    row_gids = {r["generation_run_id"] for r in rows}
    if row_gids != sample_gids:
        raise CalibrationPackageError("calibration generation ids mismatch samples")
    run_ids = {r.get("run_id") for r in rows}
    if len(run_ids) != 1 or None in run_ids:
        raise CalibrationPackageError("calibration rows must share one run_id")
    run_id = run_ids.pop()
    for row in rows:
        if not row.get("scores"):
            raise CalibrationPackageError("calibration row has no scores")
        validate_judge_scores(row["scores"])
        if row.get("judge_model") != judge_model:
            raise CalibrationPackageError("calibration judge model mismatch")
        if row.get("rubric_version") != rubric_version:
            raise CalibrationPackageError("calibration rubric version mismatch")
        if row.get("prompt_hash") != prompt_hash:
            raise CalibrationPackageError("calibration prompt hash mismatch")
        if not row.get("dataset_checksum"):
            raise CalibrationPackageError("calibration row missing dataset_checksum")
        if row.get("dataset_checksum") != dataset_checksum:
            raise CalibrationPackageError("calibration dataset checksum mismatch")
        if not row.get("config_checksum"):
            raise CalibrationPackageError("calibration row missing config_checksum")
        if row.get("config_checksum") != config_checksum:
            raise CalibrationPackageError("calibration config checksum mismatch")
        if not row.get("samples_checksum"):
            raise CalibrationPackageError("calibration row missing samples_checksum")
        if row.get("samples_checksum") != samples_checksum:
            raise CalibrationPackageError("calibration samples checksum mismatch")
    if summary is not None:
        if not isinstance(summary, dict):
            raise CalibrationPackageError("calibration summary is missing")
        if summary.get("gate_passed") is not True:
            raise CalibrationPackageError("calibration summary gate is not passed")
        for key, value in (
            ("run_id", run_id),
            ("dataset_checksum", dataset_checksum),
            ("config_checksum", config_checksum),
            ("samples_checksum", samples_checksum),
            ("judge_model", judge_model),
            ("rubric_version", rubric_version),
            ("prompt_hash", prompt_hash),
        ):
            if summary.get(key) != value:
                raise CalibrationPackageError(
                    f"calibration summary {key} mismatch"
                )
    if not calibration_gate(rows, samples):
        raise CalibrationPackageError("calibration gate did not pass")
    return rows


class CircuitBreaker:
    """Open after three consecutive dependency failures; stops stage work."""

    LIMIT = 3

    def __init__(self, limit=LIMIT):
        self.limit = limit
        self.consecutive = 0

    def record(self, failed):
        if failed:
            self.consecutive += 1
        else:
            self.consecutive = 0
        return self.consecutive >= self.limit


# ------------------------------------------------------------------ answer runner
def load_calibration_samples(path):
    """Load the frozen 8-sample calibration file; validated strictly."""
    from pathlib import Path

    samples = [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(samples) != CALIBRATION_SAMPLE_COUNT:
        raise ValueError(
            f"calibration file must have {CALIBRATION_SAMPLE_COUNT} samples, "
            f"got {len(samples)}"
        )
    return samples


def calibration_samples_checksum(path):
    """SHA-256 over the exact sample file bytes (content identity).

    Reuse of a calibration package requires the current sample file to be
    byte-identical to the one the package was built from; ids alone are not
    enough because content under the same ids can be swapped.
    """
    import hashlib
    from pathlib import Path

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def raw_validate_calibration_records(
    raw_records,
    *,
    expected_run_id,
    samples,
    dataset_checksum,
    config_checksum,
    samples_checksum,
    judge_model,
    rubric_version,
    prompt_hash,
    is_final=False,
):
    """Strictly validate raw calibration records before mapping into a dictionary.

    Fails closed on non-dict, duplicate generation_run_id, unexpected IDs, wrong run_id,
    tampered case/category/checksums/model/rubric/prompt, or incomplete final artifacts.
    """
    if not isinstance(raw_records, list):
        raise ValueError("calibration records must be a list")

    samples_by_gid = {s["generation_run_id"]: s for s in samples}
    seen_gids = set()

    for r in raw_records:
        if not isinstance(r, dict):
            raise ValueError("calibration record is not a dict")
        gid = r.get("generation_run_id")
        if not gid or not isinstance(gid, str):
            raise ValueError("calibration record missing valid generation_run_id")
        if gid in seen_gids:
            raise ValueError(f"duplicate generation_run_id {gid!r} in calibration records")
        seen_gids.add(gid)

        sample = samples_by_gid.get(gid)
        if sample is None:
            raise ValueError(f"unexpected generation_run_id {gid!r} not found in calibration samples")

        if r.get("run_id") != expected_run_id:
            raise ValueError(f"calibration row has unexpected run_id {r.get('run_id')!r}, expected {expected_run_id!r}")

        expected_case_id = sample.get("case_id") or gid
        if r.get("case_id") != expected_case_id:
            raise ValueError(f"calibration row {gid} case_id mismatch: expected {expected_case_id}, got {r.get('case_id')}")

        if "category" in sample and r.get("category") != sample["category"]:
            raise ValueError(f"calibration row {gid} category mismatch: expected {sample['category']}, got {r.get('category')}")

        for key, val in (
            ("dataset_checksum", dataset_checksum),
            ("config_checksum", config_checksum),
            ("samples_checksum", samples_checksum),
            ("judge_model", judge_model),
            ("rubric_version", rubric_version),
            ("prompt_hash", prompt_hash),
        ):
            if r.get(key) != val:
                raise ValueError(f"calibration row {gid} {key} mismatch: expected {val!r}, got {r.get(key)!r}")

        status = r.get("status")
        if status not in ("complete", "error"):
            raise ValueError(f"calibration row {gid} has invalid status {status!r}")

        if is_final and status != "complete":
            raise ValueError(f"final calibration row {gid} is incomplete (status={status!r})")

    if is_final and len(seen_gids) != len(samples):
        raise ValueError(f"final calibration package row count mismatch: expected {len(samples)}, got {len(seen_gids)}")


def run_calibration(settings, dataset, budget, *, samples_path, manifest_path=None,
                    results_dir, config_checksum, reuse_path=None, print_fn=print,
                    judge_model=None, timestamp_utc7=None,
                    timestamp_utc_plus_7=None, calibration_run_id=None,
                    resume=False):
    """Run 8 real judge calls OR validate an exact reusable package.

    Returns a dict describing the calibration package: gate_passed, run_id,
    model, rubric version, prompt hash, dataset/config checksum and rows.
    config_checksum is the profile-scoped config fingerprint of the answer
    run this calibration will guard.
    """
    from pathlib import Path

    from evaluation import artifacts

    samples = load_calibration_samples(samples_path)
    samples_checksum = calibration_samples_checksum(samples_path)
    judge_model = judge_model or settings["evaluation"]["judge_model"]

    if reuse_path:
        reuse = Path(reuse_path)
        rows = artifacts.read_records(reuse)
        summary_path = reuse.parent.parent / "summaries" / f"{reuse.stem}.json"
        if not summary_path.exists():
            raise CalibrationPackageError(
                f"calibration summary missing for {reuse.stem}: {summary_path}"
            )
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        validate_calibration_package(
            rows,
            samples,
            dataset_checksum=dataset.dataset_checksum,
            config_checksum=config_checksum,
            samples_checksum=samples_checksum,
            judge_model=judge_model,
            rubric_version=RUBRIC_VERSION,
            prompt_hash=RUBRIC_PROMPT_HASH,
            summary=summary,
        )
        print_fn(f"[calibration] reused package {reuse_path} (gate passed)")
        return {
            "gate_passed": True,
            "run_id": rows[0]["run_id"],
            "rows": rows,
            "judge_model": judge_model,
            "rubric_version": RUBRIC_VERSION,
            "prompt_hash": RUBRIC_PROMPT_HASH,
            "dataset_checksum": dataset.dataset_checksum,
            "config_checksum": config_checksum,
            "samples_checksum": samples_checksum,
        }

    judge = AnswerJudge(model=judge_model)
    from datetime import datetime, timedelta, timezone

    run_id = calibration_run_id or artifacts.make_run_id(
        "calibration", "judge", dataset.dataset_checksum,
        (timestamp_utc7 or _now()).strftime("%Y%m%d-%H%M%S"),
    )
    cal_final = Path(results_dir) / "judges" / f"{run_id}.jsonl"
    cal_partial = Path(results_dir) / "judges" / f"{run_id}.partial.jsonl"
    cal_summary_path = Path(results_dir) / "summaries" / f"{run_id}.json"

    if not resume and cal_final.exists():
        raise FileExistsError(f"calibration package already finalized: {cal_final}")

    rows_by_gid = {}
    if cal_final.exists():
        raw = artifacts.read_records(cal_final)
        raw_validate_calibration_records(
            raw,
            expected_run_id=run_id,
            samples=samples,
            dataset_checksum=dataset.dataset_checksum,
            config_checksum=config_checksum,
            samples_checksum=samples_checksum,
            judge_model=judge_model,
            rubric_version=RUBRIC_VERSION,
            prompt_hash=RUBRIC_PROMPT_HASH,
            is_final=True,
        )
        for r in raw:
            rows_by_gid[r["generation_run_id"]] = r
        rows = [rows_by_gid[s["generation_run_id"]] for s in samples]
        package = {
            "gate_passed": calibration_gate(rows, samples),
            "run_id": run_id,
            "rows": rows,
            "judge_model": judge_model,
            "rubric_version": RUBRIC_VERSION,
            "prompt_hash": RUBRIC_PROMPT_HASH,
            "dataset_checksum": dataset.dataset_checksum,
            "config_checksum": config_checksum,
            "samples_checksum": samples_checksum,
        }
        if not cal_summary_path.exists():
            artifacts.write_summary(cal_summary_path, package)
        print_fn(f"[calibration] resumed completed package {run_id} (gate_passed={package['gate_passed']})")
        return package
    elif cal_partial.exists():
        raw = artifacts.read_records(cal_partial)
        raw_validate_calibration_records(
            raw,
            expected_run_id=run_id,
            samples=samples,
            dataset_checksum=dataset.dataset_checksum,
            config_checksum=config_checksum,
            samples_checksum=samples_checksum,
            judge_model=judge_model,
            rubric_version=RUBRIC_VERSION,
            prompt_hash=RUBRIC_PROMPT_HASH,
            is_final=False,
        )
        for r in raw:
            rows_by_gid[r["generation_run_id"]] = r

    uncompleted = [s for s in samples if rows_by_gid.get(s["generation_run_id"], {}).get("status") != "complete"]
    print_fn(f"[calibration] run={run_id} model={judge_model} calls_needed={len(uncompleted)}/{len(samples)}")
    if uncompleted and not judge.configured:
        raise RuntimeError("OPENAI_API_KEY missing; judge not configured")

    j_in, j_out = judge_reserve_tokens()
    for sample in samples:
        gid = sample["generation_run_id"]
        if gid in rows_by_gid and rows_by_gid[gid].get("status") == "complete":
            continue

        row = None
        case_id = sample.get("case_id") or gid
        attempt_ids = []
        total_sample_cost = 0.0
        for attempt in (1, 2):
            reservation = budget.reserve(
                stage="calibration",
                case_id=case_id,
                generation_run_id=gid,
                attempt_number=attempt,
                model=judge_model,
                estimated_input_tokens=j_in,
                estimated_output_tokens=j_out,
            )
            attempt_ids.append(reservation["attempt_id"])
            try:
                outcome = asyncio.run(judge.judge(
                    question=sample.get("question", ""),
                    reference_answer=sample.get("reference_answer", ""),
                    answer=sample.get("answer") or sample.get("generated_answer", ""),
                    evidence=sample.get("evidence", []),
                ))
                cost = budget.settle_success(reservation, outcome.get("usage_tokens"))
                total_sample_cost += cost
                row = judge_record(
                    run_id=run_id,
                    timestamp_utc_plus_7=timestamp_utc_plus_7
                    or datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S"),
                    case_id=case_id,
                    category=sample.get("category", "calibration"),
                    generation_run_id=gid,
                    rubric_version=RUBRIC_VERSION,
                    prompt_hash=RUBRIC_PROMPT_HASH,
                    scores=outcome["scores"],
                    feedback=outcome["feedback"],
                    judge_model=judge_model,
                    dataset_checksum=dataset.dataset_checksum,
                    config_checksum=config_checksum,
                    samples_checksum=samples_checksum,
                    latency_ms=outcome["latency_ms"],
                    usage_tokens=outcome["usage_tokens"],
                    cost_usd=cost,
                    cost_usd_total=round(total_sample_cost, 8),
                    attempts=len(attempt_ids),
                    attempt_ids=attempt_ids,
                )
                rows_by_gid[gid] = row
                artifacts.replace_partial(cal_partial, list(rows_by_gid.values()))
                break
            except Exception as exc:
                effective = _judge_effective_error(exc)
                cost = budget.settle_error(reservation, error_type=effective)
                total_sample_cost += cost
                if attempt == 2 or not is_retryable(effective):
                    row = judge_record(
                        run_id=run_id,
                        timestamp_utc_plus_7=timestamp_utc_plus_7
                        or datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S"),
                        case_id=case_id,
                        category=sample.get("category", "calibration"),
                        generation_run_id=gid,
                        rubric_version=RUBRIC_VERSION,
                        prompt_hash=RUBRIC_PROMPT_HASH,
                        scores={},
                        feedback="",
                        judge_model=judge_model,
                        dataset_checksum=dataset.dataset_checksum,
                        config_checksum=config_checksum,
                        samples_checksum=samples_checksum,
                        status="error",
                        error_type=effective,
                        attempts=len(attempt_ids),
                        cost_usd=cost,
                        cost_usd_total=round(total_sample_cost, 8),
                        attempt_ids=attempt_ids,
                    )
                    rows_by_gid[gid] = row
                    artifacts.replace_partial(cal_partial, list(rows_by_gid.values()))
                    break

    rows = [rows_by_gid[s["generation_run_id"]] for s in samples if s["generation_run_id"] in rows_by_gid]
    all_complete = len(rows) == len(samples) and all(r.get("status") == "complete" for r in rows)
    if all_complete and not cal_final.exists():
        artifacts.replace_partial(cal_partial, rows)
        check_raw = artifacts.read_records(cal_partial)
        raw_validate_calibration_records(
            check_raw,
            expected_run_id=run_id,
            samples=samples,
            dataset_checksum=dataset.dataset_checksum,
            config_checksum=config_checksum,
            samples_checksum=samples_checksum,
            judge_model=judge_model,
            rubric_version=RUBRIC_VERSION,
            prompt_hash=RUBRIC_PROMPT_HASH,
            is_final=True,
        )
        artifacts.finalize_run(cal_partial, cal_final)

    package = {
        "gate_passed": calibration_gate(rows, samples) if all_complete else False,
        "run_id": run_id,
        "rows": rows,
        "judge_model": judge_model,
        "rubric_version": RUBRIC_VERSION,
        "prompt_hash": RUBRIC_PROMPT_HASH,
        "dataset_checksum": dataset.dataset_checksum,
        "config_checksum": config_checksum,
        "samples_checksum": samples_checksum,
    }
    artifacts.write_summary(cal_summary_path, package)
    print_fn(f"[calibration] gate_passed={package['gate_passed']}")
    return package


def _now():
    from datetime import datetime, timedelta, timezone

    return datetime.now(timezone(timedelta(hours=7)))


def _estimate_generation_usage(question, context, answer):
    """Token estimate of the REAL generation input (system + context + question).

    The input bound must cover the actual prompt: the grounded system
    instructions, the bounded evidence context and the question, not only
    question/reference. Output is estimated from the answer length.
    """
    input_chars = (
        len(GENERATION_SYSTEM_INSTRUCTIONS)
        + len(question)
        + len(context or "")
        + 200  # JSON framing / labels overhead
    )
    return {
        "input": max(1, round(input_chars / 2.5)),
        "output": max(1, round(len(answer or "") / 2.5)),
    }


GENERATION_SYSTEM_INSTRUCTIONS = _llm_prompt.SYSTEM_INSTRUCTIONS


def _generation_effective_error(exc):
    """Map typed generator failures into the retry vocabulary."""
    name = type(exc).__name__
    if name == "GeneratorTimeoutError":
        return "timeout"
    if name == "GeneratorUnavailableError":
        return "transient_network"
    return name


def _judge_effective_error(exc):
    """Map typed judge failures into the retry vocabulary."""
    if isinstance(exc, JudgeTimeoutError):
        return "timeout"
    if isinstance(exc, JudgeUnavailableError):
        return "transient_network"
    if isinstance(exc, JudgeInvalidOutputError):
        return "invalid_structured_output"
    return type(exc).__name__


def run_answer_pipeline(settings, dataset, subset, budget, *, answer_profile,
                        results_dir, calibration_run_id, resume=None,
                        print_fn=print, quiet=False,
                        timestamp_utc7=None, timestamp_utc_plus_7=None):
    """Generation (gpt-5.4-nano) + judge (gpt-5.4-mini) for the fixed subset.

    Sequential, budget-guarded, circuit-broken, resumable by exact run ids.
    Every case has exactly one effective generation row and one judge row
    (latest attempt wins, partial files are rewritten atomically); a resumed
    run re-attempts failed generation/judge rows. Only a fully complete
    package is finalized, and the summary status reflects failed/not-run rows.
    calibration_run_id links this package to the calibration package it was
    gated by.
    """
    from pathlib import Path

    from evaluation import artifacts
    from evaluation import retrieval_eval
    from llm.generator_openai import OpenAIAnswerGenerator
    from retrieval.context_builder import ContextBuilder
    from vectorstore.qdrant import get_client

    from datetime import datetime, timedelta, timezone

    tz = timestamp_utc7 or datetime.now(timezone(timedelta(hours=7)))
    ts = timestamp_utc_plus_7 or tz.strftime("%Y-%m-%d %H:%M:%S")
    ts_run = tz.strftime("%Y%m%d-%H%M%S")

    answer_model = settings["llm"]["answer_model"]
    judge_model = settings["evaluation"]["judge_model"]

    if resume:
        if not resume.startswith("generation-"):
            raise ValueError("answer resume run id must start with generation-")
        gen_run_id = resume
        judge_run_id = "judge-" + resume[len("generation-"):]
    else:
        gen_run_id = artifacts.make_run_id("generation", answer_profile,
                                           dataset.dataset_checksum, ts_run)
        judge_run_id = artifacts.make_run_id("judge", answer_profile,
                                             dataset.dataset_checksum, ts_run)
    gen_final = Path(results_dir) / "generations" / f"{gen_run_id}.jsonl"
    judge_final = Path(results_dir) / "judges" / f"{judge_run_id}.jsonl"
    gen_partial = Path(results_dir) / "generations" / f"{gen_run_id}.partial.jsonl"
    judge_partial = Path(results_dir) / "judges" / f"{judge_run_id}.partial.jsonl"

    if not resume:
        for final in (gen_final, judge_final):
            if final.exists():
                raise ValueError(f"run already completed; refusing to overwrite: {final}")
    elif not (gen_partial.exists() or gen_final.exists() or judge_partial.exists() or judge_final.exists()):
        raise ValueError(f"cannot resume {gen_run_id}: no partial or final artifact found")

    client = get_client(settings["vector_database"]["url"],
                        settings["vector_database"]["timeout"])
    corpus_checksum = retrieval_eval.compute_corpus_checksum(settings, client)
    service = retrieval_eval.build_service(settings, answer_profile, client)
    snapshot = service.snapshot
    meta = {
        "corpus_checksum": corpus_checksum,
        "collection_name": snapshot.collection_name,
        "calibration_run_id": calibration_run_id,
    }
    builder = ContextBuilder(
        max_documents=settings["retrieval"]["max_context_documents"],
        max_characters=settings["retrieval"]["max_context_characters"],
    )
    generator = OpenAIAnswerGenerator(
        model=answer_model,
        temperature=settings["llm"]["temperature"],
        max_output_tokens=settings["llm"]["max_output_tokens"],
        timeout_seconds=settings["llm"]["timeout"],
    )
    if not generator.configured:
        raise RuntimeError("OPENAI_API_KEY missing; generator not configured")
    judge = AnswerJudge(model=judge_model)
    if not judge.configured:
        raise RuntimeError("OPENAI_API_KEY missing; judge not configured")

    subset_by_id = {c.case_id: c for c in subset}
    expected_gids = {f"{gen_run_id}:{c.case_id}": c for c in subset}

    # Partial / final files hold the working records: one row per case, latest attempt
    # wins. Raw rows are strictly validated: duplicates, wrong run_ids,
    # unexpected case_ids, tampered category/question/reference or mismatched
    # corpus/collection/calibration fail closed.
    gen_records = {}
    if gen_final.exists():
        raw_gen = artifacts.read_records(gen_final)
    elif gen_partial.exists():
        raw_gen = artifacts.read_records(gen_partial)
    else:
        raw_gen = []

    seen_gen = set()
    for r in raw_gen:
        if not isinstance(r, dict):
            raise ValueError(f"cannot resume {gen_run_id}: generation row is not a dict")
        if r.get("run_id") != gen_run_id:
            raise ValueError(
                f"cannot resume {gen_run_id}: generation row has unexpected run_id {r.get('run_id')!r}"
            )
        case_id = r.get("case_id")
        if not case_id or not isinstance(case_id, str):
            raise ValueError(f"cannot resume {gen_run_id}: generation row missing valid case_id")
        if case_id in seen_gen:
            raise ValueError(
                f"cannot resume {gen_run_id}: duplicate case_id {case_id} in generation records"
            )
        seen_gen.add(case_id)
        case = subset_by_id.get(case_id)
        if case is None:
            raise ValueError(
                f"cannot resume {gen_run_id}: generation row {case_id} is not in "
                "the manifest subset"
            )
        for key, value in (
            ("dataset_checksum", dataset.dataset_checksum),
            ("config_checksum", snapshot.config_fingerprint),
            ("corpus_checksum", corpus_checksum),
            ("collection_name", snapshot.collection_name),
            ("calibration_run_id", calibration_run_id),
            ("answer_model", answer_model),
            ("prompt_hash", GENERATION_PROMPT_HASH),
            ("category", case.category),
            ("question", case.question),
            ("reference_answer", case.reference_answer),
        ):
            if r.get(key) != value:
                raise ValueError(
                    f"cannot resume {gen_run_id}: generation row {case_id} "
                    f"{key} mismatch"
                )
        gen_records[case_id] = r

    judge_records = {}
    if judge_final.exists():
        raw_judge = artifacts.read_records(judge_final)
    elif judge_partial.exists():
        raw_judge = artifacts.read_records(judge_partial)
    else:
        raw_judge = []

    seen_judge = set()
    for r in raw_judge:
        if not isinstance(r, dict):
            raise ValueError(f"cannot resume {gen_run_id}: judge row is not a dict")
        if r.get("run_id") != judge_run_id:
            raise ValueError(
                f"cannot resume {gen_run_id}: judge row has unexpected run_id {r.get('run_id')!r}"
            )
        gid = r.get("generation_run_id")
        if not gid or not isinstance(gid, str):
            raise ValueError(f"cannot resume {gen_run_id}: judge row missing valid generation_run_id")
        if gid in seen_judge:
            raise ValueError(
                f"cannot resume {gen_run_id}: duplicate generation_run_id {gid} in judge records"
            )
        seen_judge.add(gid)
        case = expected_gids.get(gid)
        if case is None:
            raise ValueError(
                f"cannot resume {gen_run_id}: judge row {gid} not linked to a manifest case"
            )
        if r.get("case_id") != case.case_id:
            raise ValueError(
                f"cannot resume {gen_run_id}: judge row {gid} case_id mismatch: expected {case.case_id}, got {r.get('case_id')}"
            )
        if r.get("category") != case.category:
            raise ValueError(
                f"cannot resume {gen_run_id}: judge row {gid} category mismatch: expected {case.category}, got {r.get('category')}"
            )
        for key, value in (
            ("dataset_checksum", dataset.dataset_checksum),
            ("config_checksum", snapshot.config_fingerprint),
            ("corpus_checksum", corpus_checksum),
            ("collection_name", snapshot.collection_name),
            ("calibration_run_id", calibration_run_id),
            ("judge_model", judge_model),
            ("rubric_version", RUBRIC_VERSION),
            ("prompt_hash", RUBRIC_PROMPT_HASH),
        ):
            if r.get(key) != value:
                raise ValueError(
                    f"cannot resume {gen_run_id}: judge row {gid} {key} mismatch"
                )
        judge_records[gid] = r

    if resume:
        print_fn(f"[answers] resuming {gen_run_id}: {len(gen_records)} generation "
                 f"rows, {len(judge_records)} judge rows")

    print_fn(
        f"[answers] profile={answer_profile} generation_run={gen_run_id} "
        f"judge_run={judge_run_id} budget=calls {budget.max_calls} / "
        f"${budget.max_cost_usd}"
    )
    breaker = CircuitBreaker()
    stopped = False
    for case in subset:
        gid = f"{gen_run_id}:{case.case_id}"
        if stopped:
            if case.case_id not in gen_records:
                gen_records[case.case_id] = _gen_row_base(
                    gen_run_id, ts, settings, dataset, snapshot, case, answer_model,
                    meta=meta, status="not_run", error_type="circuit_open")
                if not gen_final.exists():
                    artifacts.replace_partial(gen_partial, list(gen_records.values()))
                if not quiet:
                    print_fn(f"  {case.case_id} generation not_run (circuit open)")
            continue
        gen_row = gen_records.get(case.case_id)
        if gen_row is not None and gen_row.get("status") == "complete":
            if judge_records.get(gid, {}).get("status") == "complete":
                continue  # this case is fully done
            failed = _judge_case(judge, case, gen_row, gid, judge_model, judge_run_id,
                                 judge_partial, judge_records, budget, ts,
                                 print_fn, quiet, meta)
            if breaker.record(failed):
                stopped = True
                print_fn("[answers] circuit breaker opened (judge); stage stopped")
            continue
        gen_failed, judge_failed = _gen_case(
            case, service, builder, generator, judge, answer_model, judge_model,
            gen_run_id, judge_run_id, gen_partial, gen_records,
            judge_partial, judge_records, budget, ts, dataset, snapshot, settings,
            print_fn, quiet, meta)
        if breaker.record(gen_failed or judge_failed):
            stopped = True
            print_fn("[answers] circuit breaker opened; stage stopped")

    gen_complete = (
        len(gen_records) == len(subset)
        and all(r.get("status") == "complete" for r in gen_records.values())
    )
    if gen_complete:
        if not gen_final.exists():
            artifacts.replace_partial(gen_partial, list(gen_records.values()))
            check_gen = artifacts.read_records(gen_partial)
            if len(check_gen) != len(subset) or len({r["case_id"] for r in check_gen}) != len(subset):
                raise ValueError(f"final generation payload row count mismatch for {gen_run_id}")
            if not all(r.get("status") == "complete" and r.get("run_id") == gen_run_id for r in check_gen):
                raise ValueError(f"final generation payload contains incomplete or wrong-run rows for {gen_run_id}")
            artifacts.finalize_run(gen_partial, gen_final)
        else:
            check_gen = artifacts.read_records(gen_final)
            if len(check_gen) != len(subset) or len({r["case_id"] for r in check_gen}) != len(subset):
                raise ValueError(f"final generation payload row count mismatch for {gen_run_id}")
            if not all(r.get("status") == "complete" and r.get("run_id") == gen_run_id for r in check_gen):
                raise ValueError(f"final generation payload contains incomplete or wrong-run rows for {gen_run_id}")

    judge_complete = (
        len(judge_records) == len(subset)
        and all(r.get("status") == "complete" for r in judge_records.values())
    )
    if judge_complete:
        if not judge_final.exists():
            artifacts.replace_partial(judge_partial, list(judge_records.values()))
            check_judge = artifacts.read_records(judge_partial)
            if len(check_judge) != len(subset) or len({r["generation_run_id"] for r in check_judge}) != len(subset):
                raise ValueError(f"final judge payload row count mismatch for {judge_run_id}")
            if not all(r.get("status") == "complete" and r.get("run_id") == judge_run_id for r in check_judge):
                raise ValueError(f"final judge payload contains incomplete or wrong-run rows for {judge_run_id}")
            artifacts.finalize_run(judge_partial, judge_final)
        else:
            check_judge = artifacts.read_records(judge_final)
            if len(check_judge) != len(subset) or len({r["generation_run_id"] for r in check_judge}) != len(subset):
                raise ValueError(f"final judge payload row count mismatch for {judge_run_id}")
            if not all(r.get("status") == "complete" and r.get("run_id") == judge_run_id for r in check_judge):
                raise ValueError(f"final judge payload contains incomplete or wrong-run rows for {judge_run_id}")

    complete = gen_complete and judge_complete and gen_final.exists() and judge_final.exists()
    summary = _answer_summary(
        gen_run_id, judge_run_id, dataset, snapshot, results_dir,
        list(gen_records.values()), list(judge_records.values()),
        calibration_run_id=calibration_run_id,
        budget=budget,
        cases_total=len(subset),
        status="complete" if complete else "partial")
    print_fn(
        f"[answers] {summary['status']}: generation "
        f"{summary['completed_generation']}/{summary['cases_total']}, "
        f"judge {summary['completed_judge']}/{summary['cases_total']}, "
        f"pass {summary['passed']}/{summary['completed_judge']}"
        + ("" if complete else " (partial; not finalized)")
    )
    return summary


def _gen_row_base(run_id, ts, settings, dataset, snapshot, case, answer_model,
                  *, meta, answer="", used_sources=(), used_evidence=(),
                  latency_ms=None, usage_tokens=None, cost_usd=0.0,
                  cost_usd_total=None, usage_is_estimate=False, status="complete",
                  error_type=None, attempts=1, attempt_ids=None):
    """One generation record carrying the current run identity."""
    return generation_record(
        run_id=run_id, timestamp_utc_plus_7=ts,
        dataset_path=settings["evaluation"]["test_file"],
        dataset_checksum=dataset.dataset_checksum,
        config_checksum=snapshot.config_fingerprint,
        corpus_checksum=meta["corpus_checksum"],
        collection_name=meta["collection_name"],
        calibration_run_id=meta["calibration_run_id"],
        case_id=case.case_id, category=case.category,
        question=case.question, reference_answer=case.reference_answer,
        answer=answer, used_sources=list(used_sources),
        used_evidence=list(used_evidence),
        answer_model=answer_model, prompt_hash=GENERATION_PROMPT_HASH,
        latency_ms=latency_ms, usage_tokens=usage_tokens, cost_usd=cost_usd,
        cost_usd_total=cost_usd_total, usage_is_estimate=usage_is_estimate,
        status=status, error_type=error_type, attempts=attempts, attempt_ids=attempt_ids,
    )


def _gen_case(case, service, builder, generator, judge, answer_model, judge_model,
              gen_run_id, judge_run_id, gen_partial, gen_records,
              judge_partial, judge_records, budget, ts, dataset, snapshot, settings,
              print_fn, quiet, meta):
    """One full generation attempt (retrieval -> generate -> judge)."""
    import asyncio as _asyncio
    import time as _time

    from evaluation import artifacts

    gid = f"{gen_run_id}:{case.case_id}"
    try:
        documents = service.search(case.question)[:10]
    except Exception as exc:
        gen_records[case.case_id] = _gen_row_base(
            gen_run_id, ts, settings, dataset, snapshot, case, answer_model,
            meta=meta, status="error", error_type="retrieval_failed")
        artifacts.replace_partial(gen_partial, list(gen_records.values()))
        if not quiet:
            print_fn(f"  {case.case_id} retrieval FAILED {type(exc).__name__}")
        return True, False
    context_result = builder.build(documents)
    evidence = [
        entity_record(
            source["source"], source["section"],
            next((d.text for d in documents
                  if d.metadata.get("chunk_id") == source["chunk_id"]), ""),
            next((d.score for d in documents
                  if d.metadata.get("chunk_id") == source["chunk_id"]), None),
        )
        for source in context_result.sources
    ]
    if not evidence:
        gen_records[case.case_id] = _gen_row_base(
            gen_run_id, ts, settings, dataset, snapshot, case, answer_model,
            meta=meta, status="no_evidence")
        artifacts.replace_partial(gen_partial, list(gen_records.values()))
        if not quiet:
            print_fn(f"  {case.case_id} no_evidence")
        return False, False

    result = None
    last_error = None
    attempt_ids = []
    total_gen_cost = 0.0
    gen_in, gen_out = generation_reserve_tokens(settings)
    for attempt in (1, 2):
        reservation = budget.reserve(
            stage="generation",
            case_id=case.case_id,
            generation_run_id=None,
            attempt_number=attempt,
            model=answer_model,
            estimated_input_tokens=gen_in,
            estimated_output_tokens=gen_out,
        )
        attempt_ids.append(reservation["attempt_id"])
        try:
            started = _time.monotonic()
            generated = _asyncio.run(generator.generate_answer(
                case.question, context_result.context,
                [source["chunk_id"] for source in context_result.sources]))
            # generation provides no provider usage: reconcile against the
            # conservative reservation (fail-closed, never a char heuristic).
            usage = _estimate_generation_usage(case.question,
                                               context_result.context,
                                               generated.answer)
            cost = budget.settle_success(reservation, None)
            total_gen_cost += cost
            result = (generated, usage, cost, started, attempt)
            break
        except Exception as exc:
            effective = _generation_effective_error(exc)
            cost = budget.settle_error(reservation, error_type=effective)
            total_gen_cost += cost
            last_error = effective
            if attempt == 2 or not is_retryable(effective):
                break
    if result is None:
        error_type = last_error if not is_retryable(last_error) else "retry_exhausted"
        gen_records[case.case_id] = _gen_row_base(
            gen_run_id, ts, settings, dataset, snapshot, case, answer_model,
            meta=meta, status="error", error_type=error_type,
            attempts=len(attempt_ids), cost_usd=cost,
            cost_usd_total=round(total_gen_cost, 8), attempt_ids=attempt_ids)
        artifacts.replace_partial(gen_partial, list(gen_records.values()))
        if not quiet:
            print_fn(f"  {case.case_id} generation FAILED {error_type}")
        return True, False
    generated, usage, cost, started, att = result
    used_ids = list(dict.fromkeys(generated.used_source_ids))
    used_evidence = [e for e in evidence
                     if e["source"] in {src["source"] for src in context_result.sources}]
    gen_row = _gen_row_base(
        gen_run_id, ts, settings, dataset, snapshot, case, answer_model,
        meta=meta,
        answer=generated.answer, used_sources=used_ids, used_evidence=used_evidence,
        latency_ms=round((_time.monotonic() - started) * 1000),
        usage_tokens=usage, cost_usd=cost, cost_usd_total=round(total_gen_cost, 8),
        usage_is_estimate=True, attempts=len(attempt_ids), attempt_ids=attempt_ids)
    gen_records[case.case_id] = gen_row
    artifacts.replace_partial(gen_partial, list(gen_records.values()))
    judge_failed = _judge_case(judge, case, gen_row, gid, judge_model, judge_run_id,
                               judge_partial, judge_records, budget, ts,
                               print_fn, quiet, meta)
    return False, judge_failed


def _judge_case(judge, case, gen_row, gid, judge_model, judge_run_id,
                judge_partial, judge_records, budget, ts,
                print_fn=print, quiet=False, meta=None):
    """Judge one frozen generation; one retry for typed transient errors."""
    import asyncio as _asyncio

    from evaluation import artifacts

    dataset_checksum = gen_row.get("dataset_checksum")
    config_checksum = gen_row.get("config_checksum")
    meta = meta or {}
    j_in, j_out = judge_reserve_tokens()
    attempt_ids = []
    total_judge_cost = 0.0
    for attempt in (1, 2):
        reservation = budget.reserve(
            stage="judge",
            case_id=case.case_id,
            generation_run_id=gid,
            attempt_number=attempt,
            model=judge_model,
            estimated_input_tokens=j_in,
            estimated_output_tokens=j_out,
        )
        attempt_ids.append(reservation["attempt_id"])
        try:
            outcome = _asyncio.run(judge.judge(
                case.question, case.reference_answer,
                gen_row["generated_answer"], gen_row["used_evidence"]))
            cost = budget.settle_success(reservation, outcome["usage_tokens"])
            total_judge_cost += cost
            row = judge_record(
                run_id=judge_run_id, timestamp_utc_plus_7=ts,
                case_id=case.case_id, category=case.category,
                generation_run_id=gid, rubric_version=RUBRIC_VERSION,
                prompt_hash=RUBRIC_PROMPT_HASH, scores=outcome["scores"],
                feedback=outcome["feedback"], judge_model=judge_model,
                dataset_checksum=dataset_checksum,
                config_checksum=config_checksum,
                corpus_checksum=gen_row.get("corpus_checksum"),
                collection_name=gen_row.get("collection_name"),
                calibration_run_id=gen_row.get("calibration_run_id"),
                latency_ms=outcome["latency_ms"],
                usage_tokens=outcome["usage_tokens"], cost_usd=cost,
                cost_usd_total=round(total_judge_cost, 8),
                attempts=len(attempt_ids), attempt_ids=attempt_ids)
            judge_records[gid] = row
            artifacts.replace_partial(judge_partial, list(judge_records.values()))
            if not quiet:
                passed = judge_passes(outcome["scores"])
                print_fn(
                    f"  {case.case_id} sources={gen_row['used_sources']} "
                    f"scores={outcome['scores']} pass={passed} "
                    f"fb={outcome['feedback'][:60]!r}")
            return False
        except Exception as exc:
            effective = _judge_effective_error(exc)
            cost = budget.settle_error(reservation, error_type=effective)
            total_judge_cost += cost
            if attempt == 2 or not is_retryable(effective):
                judge_records[gid] = judge_record(
                    run_id=judge_run_id, timestamp_utc_plus_7=ts,
                    case_id=case.case_id, category=case.category,
                    generation_run_id=gid, rubric_version=RUBRIC_VERSION,
                    prompt_hash=RUBRIC_PROMPT_HASH, scores={}, feedback="",
                    judge_model=judge_model,
                    dataset_checksum=dataset_checksum,
                    config_checksum=config_checksum,
                    corpus_checksum=gen_row.get("corpus_checksum"),
                    collection_name=gen_row.get("collection_name"),
                    calibration_run_id=gen_row.get("calibration_run_id"),
                    status="error", error_type=effective,
                    attempts=len(attempt_ids), cost_usd=cost,
                    cost_usd_total=round(total_judge_cost, 8),
                    attempt_ids=attempt_ids)
                artifacts.replace_partial(judge_partial, list(judge_records.values()))
                if not quiet:
                    print_fn(f"  {case.case_id} judge FAILED {effective}")
                return True
    return True


def _answer_summary(gen_run_id, judge_run_id, dataset, snapshot, results_dir,
                    gen_rows, judge_rows, calibration_run_id, budget=None,
                    cases_total=None, status="complete"):
    """Write the answer/judge summary; only truthful counts, never fake complete.

    failed_generation/failed_judge count against cases_total: a case with no
    judge row at all (e.g. not_run after a breaker) is missing, not ignored.
    """
    from pathlib import Path

    from evaluation import artifacts

    gen_complete = [r for r in gen_rows if r.get("status") == "complete"]
    judge_complete = [r for r in judge_rows if r.get("status") == "complete"]
    passed = [r for r in judge_complete if judge_passes(r["scores"])]
    if cases_total is None:
        cases_total = len(gen_rows)

    budget_snapshot = budget.snapshot() if budget is not None and hasattr(budget, "snapshot") else {}

    summary = {
        "run_id": f"{gen_run_id}+{judge_run_id}",
        "table": "answer_judge",
        "timestamp_utc_plus_7": _now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "generation_run_id": gen_run_id,
        "judge_run_id": judge_run_id,
        "dataset_checksum": dataset.dataset_checksum,
        "collection_name": snapshot.collection_name,
        "config_checksum": snapshot.config_fingerprint,
        "answer_profile": snapshot.active_profile,
        "answer_model": gen_complete[0]["answer_model"] if gen_complete else None,
        "judge_model": judge_complete[0]["judge_model"] if judge_complete else None,
        "rubric_version": judge_complete[0]["rubric_version"] if judge_complete else None,
        "prompt_hash": judge_complete[0]["prompt_hash"] if judge_complete else None,
        "evaluation_override": {"max_results": 10, "concurrency": 1},
        "calibration_run_id": calibration_run_id,
        "cases_total": cases_total,
        "completed_generation": len(gen_complete),
        "failed_generation": cases_total - len(gen_complete),
        "completed_judge": len(judge_complete),
        "failed_judge": cases_total - len(judge_complete),
        "passed": len(passed),
        "not_passed": len(judge_complete) - len(passed),
        "generation_usage_is_estimate": True,
        "provider_calls_total": budget_snapshot.get("calls", len(gen_rows) + len(judge_rows)),
        "provider_cost_usd_total": budget_snapshot.get(
            "effective_cost_usd",
            sum(r.get("cost_usd", 0.0) for r in gen_rows) + sum(r.get("cost_usd", 0.0) for r in judge_rows),
        ),
        "provider_cost_is_estimate": budget_snapshot.get("has_estimate", True),
        "unresolved_attempt_count": budget_snapshot.get("unresolved_count", 0),
        "budget_schema_version": budget_snapshot.get("schema_version", 1),
        "budget_artifact_path": budget_snapshot.get("artifact_path", f"budgets/{gen_run_id}.json"),
        "budget_artifact_checksum": budget_snapshot.get("artifact_checksum"),
    }
    artifacts.write_summary(
        Path(results_dir) / "summaries" / f"{judge_run_id}.json", summary)
    return summary
