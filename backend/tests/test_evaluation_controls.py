"""Deterministic control-flow tests: budget caps, calibration package, breaker.

Known local inputs only; no provider calls. These encode the Phase 7
orchestration contracts the reviewer required (hard gate, real cost caps,
circuit breaker).
"""

from pathlib import Path
import pytest

from evaluation.answer_eval import (
    CALIBRATION_SAMPLE_COUNT,
    JUDGE_MAX_OUTPUT_TOKENS,
    CallBudget,
    CallBudgetExceeded,
    CircuitBreaker,
    JudgeInvalidOutputError,
    JudgeTimeoutError,
    JudgeUnavailableError,
    RUBRIC_PROMPT_HASH,
    RUBRIC_SYSTEM,
    UnknownModelError,
    _judge_effective_error,
    _prompt_hash,
    calibration_gate,
    generation_reserve_tokens,
    is_retryable,
    judge_reserve_tokens,
    validate_calibration_package,
    CalibrationPackageError,
)

MODEL = "gpt-5.4-nano"
CONFIG = "CFG"


def calib_row(gid, *, scores=None, status="complete", model="gpt-5.4-mini",
              rubric="v1", prompt_hash="HASHPROMPT", dataset_checksum="DS",
              config_checksum=CONFIG, samples_checksum="SAMPCHK",
              run_id="cal-run-1", good=True):
    return {
        "run_id": run_id,
        "generation_run_id": gid,
        "case_id": gid,
        "status": status,
        "scores": scores if scores is not None else (
            {"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5}
            if good else {"accuracy": 1, "completeness": 1, "relevance": 5, "groundedness": 1}),
        "judge_model": model,
        "rubric_version": rubric,
        "prompt_hash": prompt_hash,
        "dataset_checksum": dataset_checksum,
        "config_checksum": config_checksum,
        "samples_checksum": samples_checksum,
    }


def calib_summary(rows, *, gate_passed=None, run_id="cal-run-1",
                  dataset_checksum="DS", config_checksum=CONFIG,
                  samples_checksum="SAMPCHK",
                  judge_model="gpt-5.4-mini", rubric="v1", prompt_hash="HASHPROMPT"):
    """Summary dict for package tests; gate default recomputed from rows."""
    if gate_passed is None:
        gate_passed = calibration_gate(rows, calib_samples())
    return {
        "gate_passed": gate_passed,
        "run_id": run_id,
        "dataset_checksum": dataset_checksum,
        "config_checksum": config_checksum,
        "samples_checksum": samples_checksum,
        "judge_model": judge_model,
        "rubric_version": rubric,
        "prompt_hash": prompt_hash,
    }


def calib_samples():
    return [
        {
            "generation_run_id": f"s{i}",
            "case_id": f"s{i}",
            "is_good": i % 2 == 0,
            "question": f"Question s{i}",
            "reference_answer": f"Ref s{i}",
            "answer": f"Ans s{i}",
            "evidence": [],
        }
        for i in range(CALIBRATION_SAMPLE_COUNT)
    ]


# ---------------------------------------------------------------- CallBudget
def test_budget_allows_within_caps():
    budget = CallBudget(max_calls=4, max_cost_usd=0.05)
    res_a = budget.reserve(MODEL, 2000, 300)
    budget.reserve(MODEL, 2000, 300)
    assert budget.calls == 2
    assert budget.cost_usd == 0.0
    settled = budget.settle(res_a, {"input": 1500, "output": 200})
    assert settled > 0.0
    assert budget.cost_usd == settled


def test_budget_settle_releases_exact_reservation():
    """The settled call's reservation is released, never a net of actuals."""
    budget = CallBudget(max_calls=10, max_cost_usd=1.0)
    res = budget.reserve(MODEL, 2000, 300)  # ~0.00048
    assert budget.reserved_usd > 0.0
    budget.settle(res, {"input": 1500, "output": 200})
    assert budget.reserved_usd == 0.0
    assert budget.cost_usd > 0.0


def test_budget_failed_call_charges_reservation():
    """A failed provider call keeps the conservative charge (fail closed)."""
    budget = CallBudget(max_calls=10, max_cost_usd=1.0)
    res = budget.reserve(MODEL, 2000, 300)
    charged = budget.settle(res)  # no usage returned: charge the reservation
    assert budget.reserved_usd == 0.0
    assert budget.cost_usd == charged
    assert charged > 0.0
    # cap accounting still allows the next call
    budget.reserve(MODEL, 100, 100)
    assert budget.calls == 2


def test_budget_unknown_model_fails_closed():
    """Not in the price table is rejected, never silently $0."""
    budget = CallBudget(max_calls=10, max_cost_usd=1.0)
    with pytest.raises(UnknownModelError):
        budget.reserve("mystery-model", 100, 100)
    assert budget.calls == 0


def test_budget_tracks_output_beyond_reservation():
    """Reconciling a larger observed output still counts real cost exactly."""
    budget = CallBudget(max_calls=10, max_cost_usd=1.0)
    res = budget.reserve(MODEL, 2000, 300)
    settled = budget.settle(res, {"input": 1500, "output": 521})
    assert budget.reserved_usd == 0.0
    assert settled == budget.cost_usd
    assert settled > 0.0


def test_generation_reserve_uses_real_output_bound():
    """Reserve bound is the runtime max_output_tokens, not a 300-token guess."""
    settings = {"llm": {"max_output_tokens": 1024},
                "retrieval": {"max_context_characters": 3000}}
    gen_in, gen_out = generation_reserve_tokens(settings)
    assert gen_out == 1024
    assert gen_in > 3000


def test_judge_reserve_matches_runtime_bound():
    """The reserve bound must equal the runtime judge max_output bound."""
    judge_in, judge_out = judge_reserve_tokens()
    assert judge_in > 0
    assert judge_out == JUDGE_MAX_OUTPUT_TOKENS


def test_budget_call_cap_exceeded():
    budget = CallBudget(max_calls=1, max_cost_usd=1.0)
    budget.reserve(MODEL, 100, 100)
    with pytest.raises(CallBudgetExceeded):
        budget.reserve(MODEL, 100, 100)


def test_budget_cost_cap_exceeded():
    budget = CallBudget(max_calls=100, max_cost_usd=0.0004)
    # one call costs ~0.0005 (2000 in / 300 out)
    with pytest.raises(CallBudgetExceeded):
        budget.reserve(MODEL, 2000, 300)
    # reservation accounting blocks before spend is realized.
    assert budget.calls == 0


def test_budget_reservation_enforced_before_settlement():
    budget = CallBudget(max_calls=10, max_cost_usd=0.0012)
    budget.reserve(MODEL, 2000, 300)  # ~0.00048
    budget.reserve(MODEL, 2000, 300)  # ~0.00048, total reserved ~0.00096
    with pytest.raises(CallBudgetExceeded):
        budget.reserve(MODEL, 2000, 300)  # would exceed 0.0012


# --------------------------------------------------------- calibration gate
def test_calibration_gate_passes_good_and_bad():
    rows = [calib_row("good1", good=True), calib_row("bad1", good=False)]
    samples = [
        {"generation_run_id": "good1", "is_good": True},
        {"generation_run_id": "bad1", "is_good": False},
    ]
    assert calibration_gate(rows, samples) is True


def test_calibration_gate_fails_low_good_groundedness():
    rows = [
        calib_row("good1", good=True,
                  scores={"accuracy": 5, "completeness": 4, "relevance": 5, "groundedness": 3}),
        calib_row("bad1", good=False),
    ]
    samples = [
        {"generation_run_id": "good1", "is_good": True},
        {"generation_run_id": "bad1", "is_good": False},
    ]
    assert calibration_gate(rows, samples) is False


def test_calibration_gate_fails_good_bad_keys_mismatch():
    rows = [calib_row("good1", good=True)]
    samples = [{"generation_run_id": "good1", "is_good": True},
               {"generation_run_id": "bad1", "is_good": False}]
    assert calibration_gate(rows, samples) is False


# -------------------------------------------------  calibration package
def _valid_package_rows():
    return [calib_row(f"s{i}", good=i % 2 == 0)
            for i in range(CALIBRATION_SAMPLE_COUNT)]


def _validate_rows(rows, **summary):
    return validate_calibration_package(
        rows, calib_samples(), dataset_checksum="DS", config_checksum=CONFIG,
        samples_checksum="SAMPCHK",
        judge_model="gpt-5.4-mini", rubric_version="v1", prompt_hash="HASHPROMPT",
        summary=summary or None)


def test_calibration_package_accepts_exact():
    out = _validate_rows(_valid_package_rows())
    assert len(out) == CALIBRATION_SAMPLE_COUNT


def test_calibration_package_accepts_exact_with_summary():
    rows = _valid_package_rows()
    _validate_rows(rows, **calib_summary(rows))
    # an explicit passing summary is part of the accepted package


def test_calibration_package_refuses_one_row():
    rows = [calib_row("s0", good=True)]
    with pytest.raises(CalibrationPackageError, match="8"):
        _validate_rows(rows)


def test_calibration_package_refuses_wrong_model():
    rows = [calib_row(f"s{i}", good=i % 2 == 0, model="gpt-5.4-nano")
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="judge model"):
        _validate_rows(rows)


def test_calibration_package_refuses_wrong_prompt_hash():
    rows = [calib_row(f"s{i}", good=i % 2 == 0, prompt_hash="OTHER")
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="prompt hash"):
        _validate_rows(rows)


def test_calibration_package_refuses_failed_gate_scores():
    rows = [calib_row(f"s{i}", good=False)
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="gate"):
        _validate_rows(rows)


def test_calibration_package_refuses_incomplete_row():
    rows = [calib_row(f"s{i}", good=i % 2 == 0, status="error" if i == 0 else "complete")
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="incomplete"):
        _validate_rows(rows)


def test_calibration_package_refuses_wrong_checksum():
    rows = [calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum="OTHER")
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="checksum"):
        _validate_rows(rows)


def test_calibration_package_refuses_missing_dataset_checksum():
    """Probe: checksum-less rows must be rejected, never accepted."""
    rows = [calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum=None)
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="missing dataset_checksum"):
        _validate_rows(rows)


def test_calibration_package_refuses_missing_config_checksum():
    rows = [calib_row(f"s{i}", good=i % 2 == 0, config_checksum=None)
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="missing config_checksum"):
        _validate_rows(rows)


def test_calibration_package_refuses_wrong_config_checksum():
    rows = [calib_row(f"s{i}", good=i % 2 == 0, config_checksum="OTHER")
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="config"):
        _validate_rows(rows)


def test_calibration_package_refuses_failed_summary_gate():
    """Probe: a summary recording gate_passed=false must block reuse."""
    rows = _valid_package_rows()
    with pytest.raises(CalibrationPackageError, match="summary gate is not passed"):
        _validate_rows(rows, gate_passed=False)


def test_calibration_package_refuses_wrong_summary_run_id():
    rows = _valid_package_rows()
    with pytest.raises(CalibrationPackageError, match="run_id"):
        _validate_rows(rows, **calib_summary(rows, run_id="other-run"))


def test_calibration_package_refuses_wrong_summary_config():
    rows = _valid_package_rows()
    with pytest.raises(CalibrationPackageError, match="config"):
        _validate_rows(rows, **calib_summary(rows, config_checksum="OTHER"))


def test_calibration_package_refuses_missing_samples_checksum():
    """Probe: content swap beneath the same ids must not pass reuse."""
    rows = [calib_row(f"s{i}", good=i % 2 == 0, samples_checksum=None)
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="missing samples_checksum"):
        _validate_rows(rows)


def test_calibration_package_refuses_swapped_samples_content():
    """Content changed but ids kept: samples checksum mismatch must reject."""
    rows = [calib_row(f"s{i}", good=i % 2 == 0, samples_checksum="OTHER")
            for i in range(CALIBRATION_SAMPLE_COUNT)]
    with pytest.raises(CalibrationPackageError, match="samples checksum"):
        _validate_rows(rows)


def test_calibration_package_refuses_wrong_summary_samples_checksum():
    rows = _valid_package_rows()
    with pytest.raises(CalibrationPackageError, match="samples_checksum"):
        _validate_rows(rows, **calib_summary(rows, samples_checksum="OTHER"))


# ------------------------------------------------------------- circuit breaker
def test_circuit_breaker_opens_after_three_consecutive():
    breaker = CircuitBreaker(limit=3)
    assert not breaker.record(True)
    assert not breaker.record(True)
    assert breaker.record(True) is True


def test_circuit_breaker_resets_on_success():
    breaker = CircuitBreaker(limit=3)
    breaker.record(True)
    breaker.record(True)
    assert not breaker.record(False)
    assert not breaker.record(True)


# ------------------------------------------------------- judge retry mapping
def test_judge_error_mapping_to_retry_vocabulary():
    """Typed judge failures must land in the retry vocabulary (probe fix)."""
    assert _judge_effective_error(JudgeTimeoutError("x")) == "timeout"
    assert _judge_effective_error(JudgeUnavailableError("x")) == "transient_network"
    assert _judge_effective_error(JudgeInvalidOutputError("x")) == "invalid_structured_output"
    assert is_retryable(_judge_effective_error(JudgeTimeoutError("x")))
    assert is_retryable(_judge_effective_error(JudgeUnavailableError("x")))
    assert is_retryable(_judge_effective_error(JudgeInvalidOutputError("x")))
    assert not is_retryable(_judge_effective_error(ValueError("x")))


# ------------------------------------------------------------------ prompt hash
def test_rubric_prompt_hash_matches_system():
    assert RUBRIC_PROMPT_HASH == _prompt_hash(RUBRIC_SYSTEM)
    assert len(RUBRIC_PROMPT_HASH) == 64


# ----------------------------------------------- orchestration resume / breaker
import json as _json
from datetime import datetime, timedelta, timezone as _tz

import llm.generator_openai as _gen_mod
import vectorstore.qdrant as _qdrant_mod
from evaluation import answer_eval as _answer_eval
from evaluation import metrics as _metrics
from evaluation import retrieval_eval as _retrieval_eval
from evaluation.test_loader import load_dataset

FIXED_TZ = datetime(2026, 8, 22, 12, 0, 0, tzinfo=_tz(timedelta(hours=7)))


def _dataset(tmp_path, n=4):
    rows = [
        {
            "case_id": f"foods-{i:04d}",
            "question": f"Câu hỏi {i}",
            "keywords": ["Một", "Hai"],
            "reference_answer": f"Trả lời {i}.",
            "category": "direct_fact",
            "relevant_sources": ["foods/restaurants/quan a.md"],
            "relevant_sections": {
                "foods/restaurants/quan a.md": ["Thông tin"]
            },
        }
        for i in range(1, n + 1)
    ]
    path = tmp_path / "tests.jsonl"
    path.write_text("\n".join(_json.dumps(r, ensure_ascii=False) for r in rows),
                    encoding="utf-8")
    kb = tmp_path / "kb"
    (kb / "foods/restaurants").mkdir(parents=True)
    (kb / "foods/restaurants/quan a.md").write_text(
        "# Quán A\n## Thông tin\nĐịa chỉ A.\n", encoding="utf-8")
    return load_dataset(path, kb_root=kb, expected_count=n)


def _settings(tmp_path, dataset_file):
    from core.settings_loader import load_settings
    s = load_settings()
    s["knowledge_base"]["root_dir"] = str(tmp_path / "kb")
    s["evaluation"]["test_file"] = str(dataset_file)
    return s


class _Doc:
    def __init__(self, chunk_id, text, section="Thông tin"):
        self.id = chunk_id
        self.score = 0.8
        self.text = text
        self.metadata = {
            "chunk_id": chunk_id, "source": "foods/restaurants/quan a.md",
            "section": section, "title": "Quán A",
        }


class _Snapshot:
    config_fingerprint = "cfg-1"
    collection_name = "hue_foods_e5_small_384"
    active_profile = "hybrid_rerank"
    point_count = 572
    embedding_model = "m"
    embedding_dimension = 384


class _Service:
    def __init__(self, fail_search=False, fail_pattern=None):
        self.snapshot = _Snapshot()
        self.fail_search = fail_search
        self.fail_pattern = set(fail_pattern or ())
        self.calls = 0

    def search(self, question):
        self.calls += 1
        if self.fail_search or self.calls in self.fail_pattern:
            raise RuntimeError("qdrant down")
        return [_Doc("chunk-1", "Địa chỉ A.")]


class _FakeClient:
    def scroll(self, collection_name, limit, offset, with_payload, with_vectors,
               timeout):
        return [], None


class _Answer:
    answer = "Câu trả lời."
    used_source_ids = ["chunk-1"]


class _FakeGenerator:
    configured = True

    def __init__(self, *args, **kwargs):
        self.calls = 0

    async def generate_answer(self, question, context, ids):
        self.calls += 1
        return _Answer()


class _FakeJudge:
    configured = True

    def __init__(self, model="gpt-5.4-mini", fail=True):
        self.model = model
        self.fail = fail
        self.calls = 0

    async def judge(self, question, reference_answer, answer, evidence):
        self.calls += 1
        if self.fail:
            raise JudgeUnavailableError("provider down")
        return {
            "scores": {"accuracy": 5, "completeness": 5,
                       "relevance": 5, "groundedness": 5},
            "feedback": "ok", "latency_ms": 5,
            "usage_tokens": {"input": 10, "output": 5},
        }


def _patch_services(monkeypatch, profile="dense_only"):
    """Wire deterministic fakes into the orchestration modules."""
    client = _FakeClient()
    monkeypatch.setattr(_qdrant_mod, "get_client", lambda *a, **k: client)
    service = _Service()
    monkeypatch.setattr(_retrieval_eval, "build_service",
                        lambda settings, profile, client:
                        (setattr(service.snapshot, "active_profile", profile)
                         or service))
    return service


def _run_answers(settings, dataset, subset, tmp_path, service, *,
                 generator=None, judge=None, resume=None, budget=None,
                 calibration_run_id="cal-run-1"):
    """Run the answer pipeline with fakes; returns its summary."""
    from evaluation import answer_eval

    gen = generator or _FakeGenerator()
    jg = judge or _FakeJudge(fail=False)
    from evaluation.answer_eval import run_answer_pipeline
    budget = budget or CallBudget(max_calls=100, max_cost_usd=1.0)
    return run_answer_pipeline(
        settings, dataset, subset, budget, answer_profile="hybrid_rerank",
        results_dir=tmp_path / "results",
        calibration_run_id=calibration_run_id,
        resume=resume, print_fn=lambda *a: None,
        quiet=True, timestamp_utc7=FIXED_TZ,
    )


def test_retrieval_resume_one_row_per_case_and_summary_replace(monkeypatch, tmp_path):
    """Probe fix: resuming a partial run must not crash or duplicate rows."""
    dataset = _dataset(tmp_path, n=3)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True

    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    assert first[0]["status"] == "partial"
    assert partial.exists()

    # resume with the service back online; must not raise FileExistsError
    service.fail_search = False
    second = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)
    assert second[0]["status"] == "complete"
    from evaluation import artifacts
    final_rows = artifacts.read_records(
        tmp_path / "results" / "retrieval" / f"{run_id}.jsonl")
    assert len(final_rows) == 3
    assert len({r["case_id"] for r in final_rows}) == 3
    assert all(r["status"] == "complete" for r in final_rows)
    summary = _json.loads(
        (tmp_path / "results" / "retrieval" / f"{run_id}.summary.json")
        .read_text(encoding="utf-8"))
    assert summary["status"] == "complete"


def test_retrieval_resume_failed_row_keeps_checksum_identity(monkeypatch, tmp_path):
    """Failed rows must carry corpus/config checksums like complete rows."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    rows = [
        _json.loads(line)
        for line in (tmp_path / "results" / "retrieval" /
                     f"{first[0]['run_id']}.partial.jsonl")
        .read_text(encoding="utf-8").splitlines()
    ]
    error_row = next(r for r in rows if r["status"] == "error")
    assert error_row["corpus_checksum"]
    assert error_row["config_checksum"] == "cfg-1"


def test_answer_breaker_stops_after_three_failures(monkeypatch, tmp_path):
    """Probe fix: the 4th case is not processed after 3 consecutive failures."""
    dataset = _dataset(tmp_path, n=4)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    service.fail_search = True
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    summary = _run_answers(settings, dataset, list(dataset.cases), tmp_path,
                           service, generator=gen, judge=jg)
    assert summary["status"] == "partial"
    assert service.calls == 3          # 4th case must not reach the service
    gen_rows = [
        _json.loads(line)
        for line in (tmp_path / "results" / "generations" /
                     f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}.partial.jsonl")
        .read_text(encoding="utf-8").splitlines()
    ]
    assert any(r["status"] == "not_run" and r["error_type"] == "circuit_open"
               for r in gen_rows)


def test_answer_resume_retries_failed_judge(monkeypatch, tmp_path):
    """Probe fix: a judge error row is retried on resume, not skipped."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    first = _run_answers(settings, dataset, list(dataset.cases), tmp_path,
                         service, generator=gen, judge=jg)
    assert first["status"] == "partial"
    assert jg.calls == 2              # one retry inside the failed run
    assert gen.calls == 1

    jg.fail = False                   # judge heals; resume must re-attempt judge
    second = _run_answers(settings, dataset, list(dataset.cases), tmp_path,
                          service, generator=gen, judge=jg,
                          resume=f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}")
    assert second["status"] == "complete"
    assert gen.calls == 1             # generation is not regenerated
    assert jg.calls == 3              # one successful judge call on resume
    from evaluation import artifacts
    judge_rows = artifacts.read_records(
        tmp_path / "results" / "judges" /
        f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}.jsonl")
    assert len(judge_rows) == 1       # exactly one effective judge row


def test_run_calibration_reuse_refuses_missing_summary(tmp_path):
    """Reuse path must refuse a package whose summary is missing."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    ds = dataset.dataset_checksum
    rows = [
        calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum=ds, config_checksum="cfg-1")
        for i in range(CALIBRATION_SAMPLE_COUNT)
    ]
    judges_dir = tmp_path / "results" / "judges"
    judges_dir.mkdir(parents=True)
    reuse = judges_dir / "cal-run.jsonl"
    reuse.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    samples_path = tmp_path / "samples.jsonl"
    samples_path.write_text(
        "\n".join(_json.dumps(s, ensure_ascii=False) for s in calib_samples()),
        encoding="utf-8")
    budget = CallBudget(max_calls=10, max_cost_usd=1.0)
    with pytest.raises(CalibrationPackageError, match="summary missing"):
        _answer_eval.run_calibration(
            settings, dataset, budget, samples_path=str(samples_path),
            manifest_path=str(tmp_path / "manifest.json"),
            results_dir=tmp_path / "results", config_checksum="cfg-1",
            reuse_path=str(reuse), print_fn=lambda *a: None)


def test_run_calibration_reuse_accepts_exact_package(tmp_path):
    """Reuse with rows+summary fully matching is accepted (gate recomputed)."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    ds = dataset.dataset_checksum
    samples_path = tmp_path / "samples.jsonl"
    samples_path.write_text(
        "\n".join(_json.dumps(s, ensure_ascii=False) for s in calib_samples()),
        encoding="utf-8")
    sc = _answer_eval.calibration_samples_checksum(str(samples_path))
    rows = [
        calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum=ds,
                  config_checksum="cfg-1", prompt_hash=RUBRIC_PROMPT_HASH,
                  samples_checksum=sc, run_id="cal-run")
        for i in range(CALIBRATION_SAMPLE_COUNT)
    ]
    judges_dir = tmp_path / "results" / "judges"
    summaries_dir = tmp_path / "results" / "summaries"
    judges_dir.mkdir(parents=True)
    summaries_dir.mkdir(parents=True)
    reuse = judges_dir / "cal-run.jsonl"
    reuse.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    summary = calib_summary(rows, run_id="cal-run", dataset_checksum=ds,
                            config_checksum="cfg-1", prompt_hash=RUBRIC_PROMPT_HASH,
                            samples_checksum=sc)
    (summaries_dir / "cal-run.json").write_text(
        _json.dumps(summary), encoding="utf-8")
    budget = CallBudget(max_calls=10, max_cost_usd=1.0)
    package = _answer_eval.run_calibration(
        settings, dataset, budget, samples_path=str(samples_path),
        manifest_path=str(tmp_path / "manifest.json"),
        results_dir=tmp_path / "results", config_checksum="cfg-1",
        reuse_path=str(reuse), print_fn=lambda *a: None)
    assert package["gate_passed"] is True


def test_retrieval_breaker_consecutive_only(monkeypatch, tmp_path):
    """Non-consecutive failures must not open the retrieval breaker."""
    dataset = _dataset(tmp_path, n=5)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_pattern = {1, 3, 4}  # 1 fail, 1 ok, then 2 fails: not 3
    result = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    assert service.calls == 5  # the 5th case is still processed
    partial = tmp_path / "results" / "retrieval" / f"{result[0]['run_id']}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    assert not any(r["status"] == "not_run" for r in rows)


def test_retrieval_breaker_opens_after_three_consecutive(monkeypatch, tmp_path):
    dataset = _dataset(tmp_path, n=5)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_pattern = {1, 2, 3}
    result = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    assert service.calls == 3
    partial = tmp_path / "results" / "retrieval" / f"{result[0]['run_id']}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    not_run = [r for r in rows if r["status"] == "not_run"]
    assert len(not_run) == 2
    assert all(r["error_type"] == "circuit_open" for r in not_run)


def test_retrieval_resume_rejects_mismatched_identity(monkeypatch, tmp_path):
    """Resume must not trust a partial whose identity no longer matches."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    rows[0]["config_checksum"] = "CFG-TAMPERED"
    partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="config"):
        _retrieval_eval.run_retrieval(
            settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
            resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)


def test_retrieval_resume_rejects_edited_question(monkeypatch, tmp_path):
    """A partial row with an edited question must be rejected, not finalized."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    rows[0]["question"] = "Câu hỏi bị sửa?"
    partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="question"):
        _retrieval_eval.run_retrieval(
            settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
            resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)


def test_answer_resume_rejects_calibration_swap(monkeypatch, tmp_path):
    """A partial gated by cal-A cannot be resumed under cal-B."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    service.fail_search = True
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                 generator=gen, judge=jg, calibration_run_id="cal-A")
    with pytest.raises(ValueError, match="calibration_run_id"):
        _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                     generator=gen, judge=jg, calibration_run_id="cal-B",
                     resume=f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}")


def test_answer_summary_counts_missing_judge_rows(monkeypatch, tmp_path):
    """Failed judge count against cases_total must include never-judged cases."""
    dataset = _dataset(tmp_path, n=4)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    service.fail_search = True
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    summary = _run_answers(settings, dataset, list(dataset.cases), tmp_path,
                           service, generator=gen, judge=jg)
    assert summary["cases_total"] == 4
    assert summary["failed_generation"] == 4
    assert summary["completed_judge"] == 0
    assert summary["failed_judge"] == 4  # missing judge rows are counted
    assert summary["status"] == "partial"
    assert summary["calibration_run_id"] == "cal-run-1"


def test_retrieval_resume_rejects_duplicate_case_id(monkeypatch, tmp_path):
    """Resume must reject partial files containing duplicate case_ids."""
    dataset = _dataset(tmp_path, n=2)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    # Duplicate the first row
    rows.append(dict(rows[0]))
    partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        _retrieval_eval.run_retrieval(
            settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
            resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)


def test_retrieval_resume_rejects_wrong_run_id(monkeypatch, tmp_path):
    """Resume must reject partial rows that carry a different run_id."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["run_id"] = "retrieval-20260822-000000-dense_only-OTHER"
    partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="run_id"):
        _retrieval_eval.run_retrieval(
            settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
            resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)


def test_retrieval_resume_rejects_category_tamper(monkeypatch, tmp_path):
    """Resume must reject partial rows whose category was tampered."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["category"] = "TAMPERED"
    partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="category"):
        _retrieval_eval.run_retrieval(
            settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
            resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)


def test_retrieval_resume_rejects_provider_tamper(monkeypatch, tmp_path):
    """Resume must reject partial rows whose embedding_provider was tampered."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    service.fail_search = True
    first = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
        quiet=True, timestamp_utc7=FIXED_TZ)
    run_id = first[0]["run_id"]
    partial = tmp_path / "results" / "retrieval" / f"{run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["embedding_provider"] = "TAMPERED"
    partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="embedding provider"):
        _retrieval_eval.run_retrieval(
            settings, dataset, ["dense_only"], results_dir=tmp_path / "results",
            resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)


def test_answer_resume_rejects_duplicate_generation_case_id(monkeypatch, tmp_path):
    """Answer resume must reject partial generation files containing duplicate case_ids."""
    dataset = _dataset(tmp_path, n=2)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    service.fail_search = True
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                 generator=gen, judge=jg)
    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    gen_partial = tmp_path / "results" / "generations" / f"{gen_run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in gen_partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows.append(dict(rows[0]))
    gen_partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                     generator=gen, judge=jg, resume=gen_run_id)


def test_answer_resume_rejects_duplicate_judge_gid(monkeypatch, tmp_path):
    """Answer resume must reject partial judge files containing duplicate generation_run_ids."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                 generator=gen, judge=jg)
    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run_id = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_partial = tmp_path / "results" / "judges" / f"{judge_run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in judge_partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows.append(dict(rows[0]))
    judge_partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                     generator=gen, judge=jg, resume=gen_run_id)


def test_answer_resume_rejects_generation_category_tamper(monkeypatch, tmp_path):
    """Answer resume must reject partial generation rows whose category was tampered."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    service.fail_search = True
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                 generator=gen, judge=jg)
    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    gen_partial = tmp_path / "results" / "generations" / f"{gen_run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in gen_partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["category"] = "TAMPERED"
    gen_partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="category"):
        _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                     generator=gen, judge=jg, resume=gen_run_id)


def test_answer_resume_rejects_judge_category_tamper(monkeypatch, tmp_path):
    """Answer resume must reject partial judge rows whose category was tampered."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                 generator=gen, judge=jg)
    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run_id = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_partial = tmp_path / "results" / "judges" / f"{judge_run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in judge_partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["category"] = "TAMPERED"
    judge_partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="category"):
        _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                     generator=gen, judge=jg, resume=gen_run_id)


def test_answer_resume_rejects_judge_case_id_mismatch(monkeypatch, tmp_path):
    """Answer resume must reject judge rows whose case_id does not match the manifest case."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=True)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)
    _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                 generator=gen, judge=jg)
    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run_id = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_partial = tmp_path / "results" / "judges" / f"{judge_run_id}.partial.jsonl"
    rows = [_json.loads(l) for l in judge_partial.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows[0]["case_id"] = "foods-9999"
    judge_partial.write_text("\n".join(_json.dumps(r) for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="case_id"):
        _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                     generator=gen, judge=jg, resume=gen_run_id)


def test_retrieval_resume_recovers_when_final_jsonl_exists_without_summary(monkeypatch, tmp_path):
    """Resume must recover idempotently when retrieval JSONL was finalized but summary was missing or crashed."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch)
    results = tmp_path / "results"
    (results / "retrieval").mkdir(parents=True, exist_ok=True)
    run_id = f"retrieval-20260822-120000-dense_only-{dataset.dataset_checksum[:8]}"
    final = results / "retrieval" / f"{run_id}.jsonl"
    summary_file = results / "retrieval" / f"{run_id}.summary.json"
    corpus_checksum = _retrieval_eval.compute_corpus_checksum(settings, _FakeClient())

    case = dataset.cases[0]
    case_metrics = _metrics.case_metrics([], case.relevant_sources, case.relevant_sections)
    case_metrics["keyword_coverage_at_5"] = 1.0
    case_metrics["keyword_coverage_at_10"] = 1.0
    rec = _retrieval_eval.build_retrieval_record(
        run_id=run_id, timestamp_utc_plus_7="2026-08-22 12:00:00",
        dataset_path=str(dataset.dataset_path),
        dataset_checksum=dataset.dataset_checksum,
        corpus_checksum=corpus_checksum,
        config_checksum=service.snapshot.config_fingerprint,
        case_id=case.case_id, category=case.category,
        question=case.question, profile="dense_only",
        embedding_provider=settings["embedding"]["provider"],
        embedding_model=settings["embedding"]["model"],
        collection_name=settings["vector_database"]["collection_name"],
        retrieved_items=[], metrics=case_metrics, setup_latency_ms=10, latency_ms=10,
    )
    final.write_text(_json.dumps(rec) + "\n", encoding="utf-8")
    assert not summary_file.exists()

    # Search should NOT be called because final JSONL already contains complete row
    service.fail_search = True

    summaries = _retrieval_eval.run_retrieval(
        settings, dataset, ["dense_only"], results_dir=results,
        resume=run_id, quiet=True, timestamp_utc7=FIXED_TZ)
    assert len(summaries) == 1
    assert summaries[0]["status"] == "complete"
    assert summary_file.exists()
    saved = _json.loads(summary_file.read_text(encoding="utf-8"))
    assert saved["status"] == "complete"
    assert saved["completed_case_count"] == 1


def test_answer_resume_recovers_when_generation_finalized_and_judge_partial(monkeypatch, tmp_path):
    """Resume must recover when generation was finalized but crash happened before judge was finalized."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=False)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)

    results = tmp_path / "results"
    for sub in ("generations", "judges", "summaries"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run_id = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    cal_run = "cal-run-1"
    corpus_checksum = _retrieval_eval.compute_corpus_checksum(settings, _FakeClient())

    case = dataset.cases[0]
    gen_row = _answer_eval.generation_record(
        run_id=gen_run_id, timestamp_utc_plus_7="2026-08-22 12:00:00",
        dataset_path=str(dataset.dataset_path),
        dataset_checksum=dataset.dataset_checksum,
        config_checksum=service.snapshot.config_fingerprint,
        corpus_checksum=corpus_checksum,
        collection_name=settings["vector_database"]["collection_name"],
        calibration_run_id=cal_run,
        case_id=case.case_id, category=case.category,
        question=case.question, reference_answer=case.reference_answer,
        answer="Completed answer", used_sources=[], used_evidence=[],
        answer_model=settings["llm"]["answer_model"],
        prompt_hash=_answer_eval.GENERATION_PROMPT_HASH,
        latency_ms=50, usage_tokens={"input": 10, "output": 10},
        cost_usd=0.001, status="complete",
    )
    gen_final = results / "generations" / f"{gen_run_id}.jsonl"
    gen_final.write_text(_json.dumps(gen_row) + "\n", encoding="utf-8")

    # Partial judge row
    judge_row = _answer_eval.judge_record(
        run_id=judge_run_id, timestamp_utc_plus_7="2026-08-22 12:00:00",
        case_id=case.case_id, category=case.category,
        generation_run_id=f"{gen_run_id}:{case.case_id}",
        rubric_version=_answer_eval.RUBRIC_VERSION,
        prompt_hash=_answer_eval.RUBRIC_PROMPT_HASH,
        scores={"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
        feedback="good", judge_model=settings["evaluation"]["judge_model"],
        dataset_checksum=dataset.dataset_checksum,
        config_checksum=service.snapshot.config_fingerprint,
        corpus_checksum=corpus_checksum,
        collection_name=settings["vector_database"]["collection_name"],
        calibration_run_id=cal_run, latency_ms=60,
        usage_tokens={"input": 10, "output": 10}, cost_usd=0.001, status="complete",
    )
    judge_partial = results / "judges" / f"{judge_run_id}.partial.jsonl"
    judge_partial.write_text(_json.dumps(judge_row) + "\n", encoding="utf-8")
    judge_final = results / "judges" / f"{judge_run_id}.jsonl"

    # Generator should NOT be called at all
    gen.calls = 0

    summary = _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                           generator=gen, judge=jg, resume=gen_run_id, calibration_run_id=cal_run)
    assert summary["status"] == "complete"
    assert summary["completed_generation"] == 1
    assert summary["completed_judge"] == 1
    assert gen.calls == 0  # No generator calls made!
    assert judge_final.exists()  # Judge finalized successfully
    assert (results / "summaries" / f"{judge_run_id}.json").exists()


def test_answer_resume_recovers_when_both_finalized_without_summary(monkeypatch, tmp_path):
    """Resume must recover when both JSONLs were finalized but summary crashed/missing."""
    dataset = _dataset(tmp_path, n=1)
    settings = _settings(tmp_path, dataset.dataset_path)
    service = _patch_services(monkeypatch, "hybrid_rerank")
    gen = _FakeGenerator()
    jg = _FakeJudge(fail=False)
    monkeypatch.setattr(_gen_mod, "OpenAIAnswerGenerator", lambda **k: gen)
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)

    results = tmp_path / "results"
    for sub in ("generations", "judges", "summaries"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    gen_run_id = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run_id = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    cal_run = "cal-run-1"
    corpus_checksum = _retrieval_eval.compute_corpus_checksum(settings, _FakeClient())
    case = dataset.cases[0]

    gen_row = _answer_eval.generation_record(
        run_id=gen_run_id, timestamp_utc_plus_7="2026-08-22 12:00:00",
        dataset_path=str(dataset.dataset_path),
        dataset_checksum=dataset.dataset_checksum,
        config_checksum=service.snapshot.config_fingerprint,
        corpus_checksum=corpus_checksum,
        collection_name=settings["vector_database"]["collection_name"],
        calibration_run_id=cal_run,
        case_id=case.case_id, category=case.category,
        question=case.question, reference_answer=case.reference_answer,
        answer="Completed answer", used_sources=[], used_evidence=[],
        answer_model=settings["llm"]["answer_model"],
        prompt_hash=_answer_eval.GENERATION_PROMPT_HASH,
        latency_ms=50, usage_tokens={"input": 10, "output": 10},
        cost_usd=0.001, status="complete",
    )
    (results / "generations" / f"{gen_run_id}.jsonl").write_text(_json.dumps(gen_row) + "\n", encoding="utf-8")

    judge_row = _answer_eval.judge_record(
        run_id=judge_run_id, timestamp_utc_plus_7="2026-08-22 12:00:00",
        case_id=case.case_id, category=case.category,
        generation_run_id=f"{gen_run_id}:{case.case_id}",
        rubric_version=_answer_eval.RUBRIC_VERSION,
        prompt_hash=_answer_eval.RUBRIC_PROMPT_HASH,
        scores={"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
        feedback="good", judge_model=settings["evaluation"]["judge_model"],
        dataset_checksum=dataset.dataset_checksum,
        config_checksum=service.snapshot.config_fingerprint,
        corpus_checksum=corpus_checksum,
        collection_name=settings["vector_database"]["collection_name"],
        calibration_run_id=cal_run, latency_ms=60,
        usage_tokens={"input": 10, "output": 10}, cost_usd=0.001, status="complete",
    )
    (results / "judges" / f"{judge_run_id}.jsonl").write_text(_json.dumps(judge_row) + "\n", encoding="utf-8")

    summary = _run_answers(settings, dataset, list(dataset.cases), tmp_path, service,
                           generator=gen, judge=jg, resume=gen_run_id, calibration_run_id=cal_run)
    assert summary["status"] == "complete"
    assert summary["completed_generation"] == 1
    assert summary["completed_judge"] == 1
    assert gen.calls == 0
    assert jg.calls == 0
    assert (results / "summaries" / f"{judge_run_id}.json").exists()


def test_notebook_latent_answer_path_executes_exact_cell_15(tmp_path):
    """Load exact Cell 15 source from 07_evaluation.ipynb and execute end-to-end against a deterministic package."""
    from evaluation import answer_eval
    from evaluation.retrieval_eval import config_fingerprint

    # 1. Read exact Cell 15 from notebook
    repo_root = Path(__file__).resolve().parents[2]
    nb_path = repo_root / "notebooks" / "07_evaluation.ipynb"
    nb = _json.loads(nb_path.read_text(encoding="utf-8"))
    cell15 = next(c for c in nb["cells"] if c.get("id") == "17ca5224")
    cell_source = "".join(cell15["source"])

    # 2. Build 24-case fixture environment
    dataset = _dataset(tmp_path, n=24)
    settings = _settings(tmp_path, dataset.dataset_path)
    results = tmp_path / "backend" / "evaluation" / "results"
    for sub in ("generations", "judges", "summaries"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    manifest_dir = tmp_path / "knowledge-base-hue" / "foods" / "evaluation"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "answer_subset_v1.json"
    manifest_data = [{"case_id": f"foods-{i:04d}"} for i in range(1, 25)]
    manifest_path.write_text(_json.dumps({"cases": manifest_data}), encoding="utf-8")

    expected_gen_cfg = config_fingerprint(settings, "hybrid_rerank")
    gen_run = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    cal_run = f"calibration-20260822-120000-judge-{dataset.dataset_checksum[:8]}"
    common_corpus = "corpus-test-1"

    # Calibration package
    samples_path = manifest_dir / "judge_calibration_v1.jsonl"
    samples_path.write_text("\n".join(_json.dumps(s) for s in calib_samples()), encoding="utf-8")
    sc = answer_eval.calibration_samples_checksum(str(samples_path))
    cal_rows = [
        calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum=dataset.dataset_checksum,
                  config_checksum=expected_gen_cfg, prompt_hash=RUBRIC_PROMPT_HASH,
                  samples_checksum=sc, run_id=cal_run)
        for i in range(CALIBRATION_SAMPLE_COUNT)
    ]
    (results / "judges" / f"{cal_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in cal_rows), encoding="utf-8")
    cal_summary = calib_summary(cal_rows, run_id=cal_run, dataset_checksum=dataset.dataset_checksum,
                                config_checksum=expected_gen_cfg, prompt_hash=RUBRIC_PROMPT_HASH,
                                samples_checksum=sc)
    (results / "summaries" / f"{cal_run}.json").write_text(_json.dumps(cal_summary), encoding="utf-8")

    # Generation rows using real schema (generated_answer)
    gen_rows = [
        answer_eval.generation_record(
            run_id=gen_run, timestamp_utc_plus_7="2026-08-22 12:00:00",
            dataset_path=str(dataset.dataset_path), dataset_checksum=dataset.dataset_checksum,
            config_checksum=expected_gen_cfg, corpus_checksum=common_corpus,
            collection_name=settings["vector_database"]["collection_name"],
            calibration_run_id=cal_run, case_id=c.case_id, category=c.category,
            question=c.question, reference_answer=c.reference_answer,
            answer=f"Generated answer for {c.case_id}", used_sources=["foods/restaurants/quan a.md"],
            used_evidence=[], answer_model=settings["llm"]["answer_model"],
            prompt_hash=answer_eval.GENERATION_PROMPT_HASH,
            latency_ms=100, usage_tokens={"input": 10, "output": 10}, cost_usd=0.001,
            usage_is_estimate=True, status="complete",
        )
        for c in dataset.cases
    ]
    (results / "generations" / f"{gen_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in gen_rows), encoding="utf-8")

    # Judge rows using real schema
    judge_rows = [
        answer_eval.judge_record(
            run_id=judge_run, timestamp_utc_plus_7="2026-08-22 12:00:00",
            case_id=c.case_id, category=c.category, generation_run_id=f"{gen_run}:{c.case_id}",
            rubric_version=answer_eval.RUBRIC_VERSION, prompt_hash=answer_eval.RUBRIC_PROMPT_HASH,
            scores={"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
            feedback="perfect", judge_model=settings["evaluation"]["judge_model"],
            dataset_checksum=dataset.dataset_checksum, config_checksum=expected_gen_cfg,
            corpus_checksum=common_corpus, collection_name=settings["vector_database"]["collection_name"],
            calibration_run_id=cal_run, latency_ms=150, usage_tokens={"input": 20, "output": 10},
            cost_usd=0.002, status="complete", attempts=1,
        )
        for c in dataset.cases
    ]
    (results / "judges" / f"{judge_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in judge_rows), encoding="utf-8")

    # Budget artifact
    budget_file = results / "budgets" / f"{gen_run}.json"
    budget_identity = {
        "dataset_checksum": dataset.dataset_checksum,
        "config_checksum": expected_gen_cfg,
        "corpus_checksum": common_corpus,
        "collection_name": settings["vector_database"]["collection_name"],
        "answer_profile": "hybrid_rerank",
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "generation_prompt_hash": answer_eval.GENERATION_PROMPT_HASH,
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "rubric_prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "calibration_run_id": cal_run,
        "pricing_checksum": answer_eval.compute_pricing_checksum(),
    }
    budget = answer_eval.CallBudget.create(budget_file, budget_identity, max_calls=64, max_cost_usd=0.50)
    for _ in range(56):
        res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=10, estimated_output_tokens=10)
        budget.settle_success(res)

    import hashlib
    budget_chk = hashlib.sha256(budget_file.read_bytes()).hexdigest()

    # Summary
    ans_summary = {
        "run_id": f"{gen_run}+{judge_run}", "table": "answer_judge",
        "timestamp_utc_plus_7": "2026-08-22 12:00:00", "status": "complete",
        "generation_run_id": gen_run, "judge_run_id": judge_run,
        "dataset_checksum": dataset.dataset_checksum,
        "collection_name": settings["vector_database"]["collection_name"],
        "config_checksum": expected_gen_cfg, "answer_profile": "hybrid_rerank",
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "evaluation_override": {"max_results": 10, "concurrency": 1},
        "calibration_run_id": cal_run, "cases_total": 24,
        "completed_generation": 24, "failed_generation": 0,
        "completed_judge": 24, "failed_judge": 0,
        "passed": 24, "not_passed": 0, "generation_usage_is_estimate": True,
        "budget_artifact_path": f"budgets/{gen_run}.json",
        "budget_artifact_checksum": budget_chk,
        "budget_schema_version": 1,
        "provider_calls_total": budget.calls,
        "provider_cost_usd_total": budget.effective_cost_usd,
        "unresolved_attempt_count": 0,
    }
    (results / "summaries" / f"{judge_run}.json").write_text(_json.dumps(ans_summary), encoding="utf-8")

    from evaluation import artifacts

    # Execute exact Cell 15 source code
    scope = {
        "REPO": tmp_path,
        "RESULTS": results,
        "dataset": dataset,
        "settings": settings,
        "common_corpus": common_corpus,
        "config_fingerprint": config_fingerprint,
        "print_table": lambda headers, rows, widths=None: None,
        "json": _json,
        "Path": Path,
        "artifacts": artifacts,
        "answer_eval": answer_eval,
    }
    exec(compile(cell_source, "07_evaluation.ipynb:Cell15", "exec"), scope)
    assert len(scope["result_rows"]) == 24
    assert scope["answer_summary"]["status"] == "complete"
    assert scope["answer_summary"]["passed"] == 24


def test_notebook_latent_answer_path_tamper_fails_closed(tmp_path):
    """Exact Cell 15 source must raise AssertionError if a record in the package is tampered."""
    from evaluation import answer_eval, artifacts
    from evaluation.retrieval_eval import config_fingerprint

    repo_root = Path(__file__).resolve().parents[2]
    nb_path = repo_root / "notebooks" / "07_evaluation.ipynb"
    nb = _json.loads(nb_path.read_text(encoding="utf-8"))
    cell15 = next(c for c in nb["cells"] if c.get("id") == "17ca5224")
    cell_source = "".join(cell15["source"])

    dataset = _dataset(tmp_path, n=24)
    settings = _settings(tmp_path, dataset.dataset_path)
    results = tmp_path / "backend" / "evaluation" / "results"
    for sub in ("generations", "judges", "summaries", "budgets"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    manifest_dir = tmp_path / "knowledge-base-hue" / "foods" / "evaluation"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "answer_subset_v1.json"
    manifest_data = [{"case_id": f"foods-{i:04d}"} for i in range(1, 25)]
    manifest_path.write_text(_json.dumps({"cases": manifest_data}), encoding="utf-8")

    expected_gen_cfg = config_fingerprint(settings, "hybrid_rerank")
    gen_run = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    cal_run = f"calibration-20260822-120000-judge-{dataset.dataset_checksum[:8]}"
    common_corpus = "corpus-test-1"

    samples_path = manifest_dir / "judge_calibration_v1.jsonl"
    samples_path.write_text("\n".join(_json.dumps(s) for s in calib_samples()), encoding="utf-8")
    sc = answer_eval.calibration_samples_checksum(str(samples_path))
    cal_rows = [
        calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum=dataset.dataset_checksum,
                  config_checksum=expected_gen_cfg, prompt_hash=RUBRIC_PROMPT_HASH,
                  samples_checksum=sc, run_id=cal_run)
        for i in range(CALIBRATION_SAMPLE_COUNT)
    ]
    (results / "judges" / f"{cal_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in cal_rows), encoding="utf-8")
    cal_summary = calib_summary(cal_rows, run_id=cal_run, dataset_checksum=dataset.dataset_checksum,
                                config_checksum=expected_gen_cfg, prompt_hash=RUBRIC_PROMPT_HASH,
                                samples_checksum=sc)
    (results / "summaries" / f"{cal_run}.json").write_text(_json.dumps(cal_summary), encoding="utf-8")

    # Budget artifact
    budget_file = results / "budgets" / f"{gen_run}.json"
    budget_identity = {
        "dataset_checksum": dataset.dataset_checksum,
        "config_checksum": expected_gen_cfg,
        "corpus_checksum": common_corpus,
        "collection_name": settings["vector_database"]["collection_name"],
        "answer_profile": "hybrid_rerank",
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "generation_prompt_hash": answer_eval.GENERATION_PROMPT_HASH,
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "rubric_prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "calibration_run_id": cal_run,
        "pricing_checksum": answer_eval.compute_pricing_checksum(),
    }
    budget = answer_eval.CallBudget.create(budget_file, budget_identity, max_calls=64, max_cost_usd=0.50)
    for _ in range(56):
        res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=10, estimated_output_tokens=10)
        budget.settle_success(res)

    import hashlib
    budget_chk = hashlib.sha256(budget_file.read_bytes()).hexdigest()

    gen_rows = [
        answer_eval.generation_record(
            run_id=gen_run, timestamp_utc_plus_7="2026-08-22 12:00:00",
            dataset_path=str(dataset.dataset_path), dataset_checksum=dataset.dataset_checksum,
            config_checksum=expected_gen_cfg, corpus_checksum=common_corpus,
            collection_name=settings["vector_database"]["collection_name"],
            calibration_run_id=cal_run, case_id=c.case_id, category=c.category,
            question=c.question, reference_answer=c.reference_answer,
            answer=f"Generated answer for {c.case_id}", used_sources=["foods/restaurants/quan a.md"],
            used_evidence=[], answer_model=settings["llm"]["answer_model"],
            prompt_hash=answer_eval.GENERATION_PROMPT_HASH,
            latency_ms=100, usage_tokens={"input": 10, "output": 10}, cost_usd=0.001,
            usage_is_estimate=True, status="complete",
        )
        for c in dataset.cases
    ]
    # Tamper the category of row 0
    gen_rows[0]["category"] = "TAMPERED"
    (results / "generations" / f"{gen_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in gen_rows), encoding="utf-8")

    judge_rows = [
        answer_eval.judge_record(
            run_id=judge_run, timestamp_utc_plus_7="2026-08-22 12:00:00",
            case_id=c.case_id, category=c.category, generation_run_id=f"{gen_run}:{c.case_id}",
            rubric_version=answer_eval.RUBRIC_VERSION, prompt_hash=answer_eval.RUBRIC_PROMPT_HASH,
            scores={"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
            feedback="perfect", judge_model=settings["evaluation"]["judge_model"],
            dataset_checksum=dataset.dataset_checksum, config_checksum=expected_gen_cfg,
            corpus_checksum=common_corpus, collection_name=settings["vector_database"]["collection_name"],
            calibration_run_id=cal_run, latency_ms=150, usage_tokens={"input": 20, "output": 10},
            cost_usd=0.002, status="complete", attempts=1,
        )
        for c in dataset.cases
    ]
    (results / "judges" / f"{judge_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in judge_rows), encoding="utf-8")

    ans_summary = {
        "run_id": f"{gen_run}+{judge_run}", "table": "answer_judge",
        "timestamp_utc_plus_7": "2026-08-22 12:00:00", "status": "complete",
        "generation_run_id": gen_run, "judge_run_id": judge_run,
        "dataset_checksum": dataset.dataset_checksum,
        "collection_name": settings["vector_database"]["collection_name"],
        "config_checksum": expected_gen_cfg, "answer_profile": "hybrid_rerank",
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "evaluation_override": {"max_results": 10, "concurrency": 1},
        "calibration_run_id": cal_run, "cases_total": 24,
        "completed_generation": 24, "failed_generation": 0,
        "completed_judge": 24, "failed_judge": 0,
        "passed": 24, "not_passed": 0, "generation_usage_is_estimate": True,
        "budget_artifact_path": f"budgets/{gen_run}.json",
        "budget_artifact_checksum": budget_chk,
        "budget_schema_version": 1,
        "provider_calls_total": budget.calls,
        "provider_cost_usd_total": budget.effective_cost_usd,
        "unresolved_attempt_count": 0,
    }
    (results / "summaries" / f"{judge_run}.json").write_text(_json.dumps(ans_summary), encoding="utf-8")

    scope = {
        "REPO": tmp_path,
        "RESULTS": results,
        "dataset": dataset,
        "settings": settings,
        "common_corpus": common_corpus,
        "config_fingerprint": config_fingerprint,
        "print_table": lambda headers, rows, widths=None: None,
        "json": _json,
        "Path": Path,
        "artifacts": artifacts,
        "answer_eval": answer_eval,
    }
    with pytest.raises(AssertionError, match="category mismatch"):
        exec(compile(cell_source, "07_evaluation.ipynb:Cell15", "exec"), scope)


def test_calibration_partial_resume_skips_completed_samples(monkeypatch, tmp_path):
    """Resuming calibration with partial rows skips completed samples and only runs remaining."""
    dataset = _dataset(tmp_path, n=24)
    settings = _settings(tmp_path, dataset.dataset_path)
    results = tmp_path / "results"
    for sub in ("judges", "summaries", "budgets"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    samples = calib_samples()
    samples_path = tmp_path / "judge_calibration_v1.jsonl"
    samples_path.write_text("\n".join(_json.dumps(s) for s in samples), encoding="utf-8")
    manifest_path = tmp_path / "answer_subset_v1.json"
    manifest_path.write_text(_json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8")

    cal_run = f"calibration-20260823-120000-judge-{dataset.dataset_checksum[:8]}"
    sc = _answer_eval.calibration_samples_checksum(str(samples_path))
    cfg = _retrieval_eval.config_fingerprint(settings, "hybrid_rerank")

    # 4 rows already completed in partial file
    partial_rows = [
        calib_row(samples[i]["generation_run_id"], good=samples[i]["is_good"],
                  dataset_checksum=dataset.dataset_checksum, config_checksum=cfg,
                  prompt_hash=RUBRIC_PROMPT_HASH, samples_checksum=sc, run_id=cal_run)
        for i in range(4)
    ]
    partial_file = results / "judges" / f"{cal_run}.partial.jsonl"
    partial_file.write_text("\n".join(_json.dumps(r) for r in partial_rows), encoding="utf-8")

    class _CalJudge:
        configured = True
        def __init__(self):
            self.calls = 0
        async def judge(self, question, reference_answer, answer, evidence):
            self.calls += 1
            is_good = any(f"s{i}" in question for i in (0, 2, 4, 6))
            scores = (
                {"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5}
                if is_good
                else {"accuracy": 1, "completeness": 1, "relevance": 5, "groundedness": 1}
            )
            return {
                "scores": scores,
                "feedback": "ok",
                "latency_ms": 5,
                "usage_tokens": {"input": 10, "output": 5},
            }

    jg = _CalJudge()
    monkeypatch.setattr(_answer_eval, "AnswerJudge", lambda **k: jg)

    budget = CallBudget(max_calls=64, max_cost_usd=0.50)
    package = _answer_eval.run_calibration(
        settings, dataset, budget,
        samples_path=samples_path, manifest_path=manifest_path,
        results_dir=results, config_checksum=cfg,
        calibration_run_id=cal_run, resume=True,
    )

    assert package["gate_passed"] is True
    assert len(package["rows"]) == 8
    assert jg.calls == 4  # ONLY 4 remaining samples called!
    assert (results / "judges" / f"{cal_run}.jsonl").exists()


def test_raw_validate_calibration_records_rejects_duplicate_or_invalid_rows():
    """raw_validate_calibration_records must fail closed on corrupt or tampered raw lists."""
    from evaluation.answer_eval import raw_validate_calibration_records

    samples = calib_samples()
    sc = "SAMPCHK"
    cfg = "CFG"
    run_id = "cal-run-1"

    valid_rows = [
        calib_row(samples[i]["generation_run_id"], good=samples[i]["is_good"],
                  dataset_checksum="DS", config_checksum=cfg,
                  prompt_hash=RUBRIC_PROMPT_HASH, samples_checksum=sc, run_id=run_id)
        for i in range(8)
    ]

    # Valid list passes
    raw_validate_calibration_records(
        valid_rows, expected_run_id=run_id, samples=samples,
        dataset_checksum="DS", config_checksum=cfg, samples_checksum=sc,
        judge_model="gpt-5.4-mini", rubric_version="v1", prompt_hash=RUBRIC_PROMPT_HASH,
        is_final=True,
    )

    # Duplicate generation_run_id
    dup_rows = list(valid_rows)
    dup_rows.append(dict(valid_rows[0]))
    with pytest.raises(ValueError, match="duplicate generation_run_id"):
        raw_validate_calibration_records(
            dup_rows, expected_run_id=run_id, samples=samples,
            dataset_checksum="DS", config_checksum=cfg, samples_checksum=sc,
            judge_model="gpt-5.4-mini", rubric_version="v1", prompt_hash=RUBRIC_PROMPT_HASH,
        )

    # Wrong run_id
    bad_run = [dict(r) for r in valid_rows]
    bad_run[0]["run_id"] = "WRONG_RUN"
    with pytest.raises(ValueError, match="unexpected run_id"):
        raw_validate_calibration_records(
            bad_run, expected_run_id=run_id, samples=samples,
            dataset_checksum="DS", config_checksum=cfg, samples_checksum=sc,
            judge_model="gpt-5.4-mini", rubric_version="v1", prompt_hash=RUBRIC_PROMPT_HASH,
        )

    # Non-dict row
    with pytest.raises(ValueError, match="not a dict"):
        raw_validate_calibration_records(
            ["not_a_dict"], expected_run_id=run_id, samples=samples,
            dataset_checksum="DS", config_checksum=cfg, samples_checksum=sc,
            judge_model="gpt-5.4-mini", rubric_version="v1", prompt_hash=RUBRIC_PROMPT_HASH,
        )


def test_calibration_final_without_summary_rebuilds_summary_with_zero_calls(tmp_path):
    """When final calibration exists but summary is missing, resume rebuilds summary with 0 calls."""
    dataset = _dataset(tmp_path, n=24)
    settings = _settings(tmp_path, dataset.dataset_path)
    results = tmp_path / "results"
    for sub in ("judges", "summaries", "budgets"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    samples = calib_samples()
    samples_path = tmp_path / "judge_calibration_v1.jsonl"
    samples_path.write_text("\n".join(_json.dumps(s) for s in samples), encoding="utf-8")

    cal_run = f"calibration-20260823-120000-judge-{dataset.dataset_checksum[:8]}"
    sc = _answer_eval.calibration_samples_checksum(str(samples_path))
    cfg = _retrieval_eval.config_fingerprint(settings, "hybrid_rerank")

    # 8 complete rows in final file
    final_rows = [
        calib_row(samples[i]["generation_run_id"], good=samples[i]["is_good"],
                  dataset_checksum=dataset.dataset_checksum, config_checksum=cfg,
                  prompt_hash=RUBRIC_PROMPT_HASH, samples_checksum=sc, run_id=cal_run)
        for i in range(8)
    ]
    final_file = results / "judges" / f"{cal_run}.jsonl"
    final_file.write_text("\n".join(_json.dumps(r) for r in final_rows), encoding="utf-8")

    summary_file = results / "summaries" / f"{cal_run}.json"
    assert not summary_file.exists()

    budget = CallBudget(max_calls=64, max_cost_usd=0.50)
    package = _answer_eval.run_calibration(
        settings, dataset, budget,
        samples_path=samples_path,
        results_dir=results, config_checksum=cfg,
        calibration_run_id=cal_run, resume=True,
    )

    assert package["gate_passed"] is True
    assert summary_file.exists()
    assert budget.calls == 0  # 0 provider calls made!


def test_generation_and_judge_rows_preserve_attempts_and_total_cost():
    """generation_record and judge_record must include attempts, cost_usd_total, and attempt_ids."""
    gen = _answer_eval.generation_record(
        run_id="gen-1", timestamp_utc_plus_7="2026-08-23 12:00:00",
        dataset_path="tests.jsonl", dataset_checksum="ds1", config_checksum="cfg1",
        case_id="foods-0001", category="direct_fact", question="q", reference_answer="ref",
        answer="ans", used_sources=["s1"], used_evidence=[], answer_model="gpt-5.4-nano",
        prompt_hash="p1", latency_ms=10, usage_tokens={"input": 10, "output": 10},
        cost_usd=0.0001, cost_usd_total=0.0002, attempts=2,
        attempt_ids=["generation:foods-0001:1:aaa", "generation:foods-0001:2:bbb"],
    )
    assert gen["attempts"] == 2
    assert gen["cost_usd_total"] == 0.0002
    assert len(gen["attempt_ids"]) == 2

    judge = _answer_eval.judge_record(
        run_id="judge-1", timestamp_utc_plus_7="2026-08-23 12:00:00",
        case_id="foods-0001", category="direct_fact", generation_run_id="gen-1:foods-0001",
        rubric_version="v1", prompt_hash="p1", scores={"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
        feedback="ok", judge_model="gpt-5.4-mini", dataset_checksum="ds1", config_checksum="cfg1",
        cost_usd=0.0001, cost_usd_total=0.0002, attempts=2,
        attempt_ids=["judge:foods-0001:1:ccc", "judge:foods-0001:2:ddd"],
    )
    assert judge["attempts"] == 2
    assert judge["cost_usd_total"] == 0.0002
    assert len(judge["attempt_ids"]) == 2


def test_cell_15_mandatory_budget_validation_fails_on_tamper(tmp_path):
    """Cell 15 must fail closed on missing budget path, bad checksum, or identity tamper."""
    import hashlib
    from evaluation import answer_eval, artifacts
    from evaluation.retrieval_eval import config_fingerprint

    repo_root = Path(__file__).resolve().parents[2]
    nb_path = repo_root / "notebooks" / "07_evaluation.ipynb"
    nb = _json.loads(nb_path.read_text(encoding="utf-8"))
    cell15 = next(c for c in nb["cells"] if c.get("id") == "17ca5224")
    cell_source = "".join(cell15["source"])

    dataset = _dataset(tmp_path, n=24)
    settings = _settings(tmp_path, dataset.dataset_path)
    results = tmp_path / "backend" / "evaluation" / "results"
    for sub in ("generations", "judges", "summaries", "budgets"):
        (results / sub).mkdir(parents=True, exist_ok=True)

    manifest_dir = tmp_path / "knowledge-base-hue" / "foods" / "evaluation"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "answer_subset_v1.json"
    manifest_data = [{"case_id": f"foods-{i:04d}"} for i in range(1, 25)]
    manifest_path.write_text(_json.dumps({"cases": manifest_data}), encoding="utf-8")

    expected_gen_cfg = config_fingerprint(settings, "hybrid_rerank")
    gen_run = f"generation-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    judge_run = f"judge-20260822-120000-hybrid_rerank-{dataset.dataset_checksum[:8]}"
    cal_run = f"calibration-20260822-120000-judge-{dataset.dataset_checksum[:8]}"
    common_corpus = "corpus-test-1"

    samples_path = manifest_dir / "judge_calibration_v1.jsonl"
    samples_path.write_text("\n".join(_json.dumps(s) for s in calib_samples()), encoding="utf-8")
    sc = answer_eval.calibration_samples_checksum(str(samples_path))
    cal_rows = [
        calib_row(f"s{i}", good=i % 2 == 0, dataset_checksum=dataset.dataset_checksum,
                  config_checksum=expected_gen_cfg, prompt_hash=RUBRIC_PROMPT_HASH,
                  samples_checksum=sc, run_id=cal_run)
        for i in range(CALIBRATION_SAMPLE_COUNT)
    ]
    (results / "judges" / f"{cal_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in cal_rows), encoding="utf-8")
    cal_summary = calib_summary(cal_rows, run_id=cal_run, dataset_checksum=dataset.dataset_checksum,
                                config_checksum=expected_gen_cfg, prompt_hash=RUBRIC_PROMPT_HASH,
                                samples_checksum=sc)
    (results / "summaries" / f"{cal_run}.json").write_text(_json.dumps(cal_summary), encoding="utf-8")

    budget_file = results / "budgets" / f"{gen_run}.json"
    budget_identity = {
        "dataset_checksum": dataset.dataset_checksum,
        "config_checksum": expected_gen_cfg,
        "corpus_checksum": common_corpus,
        "collection_name": settings["vector_database"]["collection_name"],
        "answer_profile": "hybrid_rerank",
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "generation_prompt_hash": answer_eval.GENERATION_PROMPT_HASH,
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "rubric_prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "calibration_run_id": cal_run,
        "pricing_checksum": answer_eval.compute_pricing_checksum(),
    }
    budget = answer_eval.CallBudget.create(budget_file, budget_identity, max_calls=64, max_cost_usd=0.50)
    for _ in range(56):
        res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=10, estimated_output_tokens=10)
        budget.settle_success(res)

    gen_rows = [
        answer_eval.generation_record(
            run_id=gen_run, timestamp_utc_plus_7="2026-08-22 12:00:00",
            dataset_path=str(dataset.dataset_path), dataset_checksum=dataset.dataset_checksum,
            config_checksum=expected_gen_cfg, corpus_checksum=common_corpus,
            collection_name=settings["vector_database"]["collection_name"],
            calibration_run_id=cal_run, case_id=c.case_id, category=c.category,
            question=c.question, reference_answer=c.reference_answer,
            answer=f"Generated answer for {c.case_id}", used_sources=["foods/restaurants/quan a.md"],
            used_evidence=[], answer_model=settings["llm"]["answer_model"],
            prompt_hash=answer_eval.GENERATION_PROMPT_HASH,
            latency_ms=100, usage_tokens={"input": 10, "output": 10}, cost_usd=0.001,
            usage_is_estimate=True, status="complete",
        )
        for c in dataset.cases
    ]
    (results / "generations" / f"{gen_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in gen_rows), encoding="utf-8")

    judge_rows = [
        answer_eval.judge_record(
            run_id=judge_run, timestamp_utc_plus_7="2026-08-22 12:00:00",
            case_id=c.case_id, category=c.category, generation_run_id=f"{gen_run}:{c.case_id}",
            rubric_version=answer_eval.RUBRIC_VERSION, prompt_hash=answer_eval.RUBRIC_PROMPT_HASH,
            scores={"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
            feedback="perfect", judge_model=settings["evaluation"]["judge_model"],
            dataset_checksum=dataset.dataset_checksum, config_checksum=expected_gen_cfg,
            corpus_checksum=common_corpus, collection_name=settings["vector_database"]["collection_name"],
            calibration_run_id=cal_run, latency_ms=150, usage_tokens={"input": 20, "output": 10},
            cost_usd=0.002, status="complete", attempts=1,
        )
        for c in dataset.cases
    ]
    (results / "judges" / f"{judge_run}.jsonl").write_text("\n".join(_json.dumps(r) for r in judge_rows), encoding="utf-8")

    # Tamper 1: summary has checksum mismatch
    ans_summary = {
        "run_id": f"{gen_run}+{judge_run}", "table": "answer_judge",
        "timestamp_utc_plus_7": "2026-08-22 12:00:00", "status": "complete",
        "generation_run_id": gen_run, "judge_run_id": judge_run,
        "dataset_checksum": dataset.dataset_checksum,
        "collection_name": settings["vector_database"]["collection_name"],
        "config_checksum": expected_gen_cfg, "answer_profile": "hybrid_rerank",
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "evaluation_override": {"max_results": 10, "concurrency": 1},
        "calibration_run_id": cal_run, "cases_total": 24,
        "completed_generation": 24, "failed_generation": 0,
        "completed_judge": 24, "failed_judge": 0,
        "passed": 24, "not_passed": 0, "generation_usage_is_estimate": True,
        "budget_artifact_path": f"budgets/{gen_run}.json",
        "budget_artifact_checksum": "mismatched_checksum_abc123",
        "budget_schema_version": 1,
        "provider_calls_total": budget.calls,
        "provider_cost_usd_total": budget.effective_cost_usd,
        "unresolved_attempt_count": 0,
    }
    (results / "summaries" / f"{judge_run}.json").write_text(_json.dumps(ans_summary), encoding="utf-8")

    scope = {
        "REPO": tmp_path, "RESULTS": results, "dataset": dataset, "settings": settings,
        "common_corpus": common_corpus, "config_fingerprint": config_fingerprint,
        "print_table": lambda *a, **k: None, "json": _json, "Path": Path,
        "artifacts": artifacts, "answer_eval": answer_eval,
    }
    with pytest.raises(AssertionError, match="budget checksum mismatch"):
        exec(compile(cell_source, "07_evaluation.ipynb:Cell15", "exec"), scope)
