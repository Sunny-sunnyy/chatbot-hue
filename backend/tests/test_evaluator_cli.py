"""Deterministic CLI contract tests for the thin evaluation facade."""

import json
from pathlib import Path
import pytest

from evaluation import answer_eval
from evaluation.evaluator import build_parser, cmd_all, cmd_answers, require_retrieval_profile
from evaluation.budget import CallBudget, compute_pricing_checksum
from evaluation.test_loader import LoadedDataset, TestCase as TestCaseRecord

TestCaseRecord.__test__ = False


class _FakeClient:
    def collection_exists(self, *a, **k):
        return True

    def get_collection(self, *a, **k):
        class _Info:
            points_count = 572
            indexed_vectors_count = 572
        return _Info()

    def count(self, *a, **k):
        class _Count:
            count = 572
        return _Count()

    def scroll(self, *a, **k):
        return ([], None)


class _FakeGenerator:
    def __init__(self):
        self.calls = 0

    @property
    def configured(self):
        return True

    async def generate_answer(self, question, context, sources):
        self.calls += 1
        class _Out:
            answer = f"Answer for {question}"
            used_source_ids = ["src1"]
        return _Out()


class _FakeJudge:
    def __init__(self):
        self.calls = 0

    @property
    def configured(self):
        return True

    async def judge(self, question, reference_answer, answer, evidence):
        self.calls += 1
        return {
            "scores": {"accuracy": 5, "completeness": 5, "relevance": 5, "groundedness": 5},
            "feedback": "Good",
            "latency_ms": 10,
            "usage_tokens": {"input": 10, "output": 10},
        }


def _dummy_dataset(tmp_path, count=24):
    cases = [
        TestCaseRecord(
            case_id=f"foods-{i:04d}",
            question=f"Question {i}",
            keywords=["k1"],
            reference_answer=f"Ref {i}",
            category=(
                "direct_fact", "temporal", "comparative", "relationship",
                "spanning", "holistic", "food_knowledge", "guide_planning",
            )[(i - 1) % 8],
            relevant_sources=["foods/restaurants/quan a.md"],
            relevant_sections={"foods/restaurants/quan a.md": ["Thông tin"]},
        )
        for i in range(1, count + 1)
    ]
    test_file = tmp_path / "tests.jsonl"
    test_file.write_text("\n".join(json.dumps({
        "case_id": c.case_id, "question": c.question, "keywords": c.keywords,
        "reference_answer": c.reference_answer, "category": c.category,
        "relevant_sources": c.relevant_sources, "relevant_sections": c.relevant_sections,
    }) for c in cases), encoding="utf-8")
    return LoadedDataset(dataset_path=test_file, cases=cases, dataset_checksum="6d023e0a891e6536d31f7dc70c07f9e1d5cd06f00033f50fa438721344646d8c")


def _dummy_settings(tmp_path, test_path):
    return {
        "knowledge_base": {"root_dir": str(tmp_path)},
        "evaluation": {"test_file": str(test_path), "judge_model": "gpt-5.4-mini"},
        "llm": {"answer_model": "gpt-5.4-nano", "temperature": 0.0, "max_output_tokens": 500, "timeout": 30},
        "vector_database": {
            "url": "http://localhost:6333", "timeout": 5, "collection_name": "hue_foods_e5_small_384",
            "scroll_batch_size": 100,
        },
        "embedding": {"provider": "local_e5", "model": "intfloat/multilingual-e5-small", "dimension": 384},
        "retrieval": {"max_context_documents": 3, "max_context_characters": 1000},
    }


def test_parser_requires_profile_or_profiles_all_for_retrieval():
    parser = build_parser()
    args = parser.parse_args(["retrieval"])
    assert args.profile is None and args.profiles is None  # no implicit profile
    with pytest.raises(SystemExit):
        require_retrieval_profile(parser.parse_args(["retrieval"]))
    args = parser.parse_args(["retrieval", "--profile", "dense_only"])
    assert args.profile == "dense_only"
    args = parser.parse_args(["retrieval", "--profiles", "all", "--quiet"])
    assert args.profiles == "all" and args.quiet is True


def test_parser_answers_requires_answer_profile_and_paid_flag():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["answers"])
    args = parser.parse_args(
        ["answers", "--answer-profile", "hybrid_rerank", "--confirm-paid",
         "--max-calls", "64", "--max-cost-usd", "0.50", "--quiet"])
    assert args.answer_profile == "hybrid_rerank"
    assert args.confirm_paid is True
    assert args.quiet is True


def test_parser_all_has_quiet_and_paid_flags():
    """The `all` subcommand must not lose --quiet/--confirm-paid."""
    parser = build_parser()
    args = parser.parse_args(
        ["all", "--profiles", "all", "--answer-profile", "hybrid_rerank",
         "--confirm-paid", "--quiet"])
    assert args.quiet is True
    assert args.confirm_paid is True
    assert args.command == "all"


def test_cli_answers_without_confirm_paid_makes_zero_calls_and_no_budget(monkeypatch, tmp_path, capsys):
    from evaluation import evaluator
    dataset = _dummy_dataset(tmp_path)
    settings = _dummy_settings(tmp_path, dataset.dataset_path)

    monkeypatch.setattr(evaluator, "_load_cases", lambda: (settings, dataset))
    monkeypatch.setattr(evaluator, "RESULTS_DIR", tmp_path / "results")

    kb_eval = tmp_path / "foods" / "evaluation"
    kb_eval.mkdir(parents=True, exist_ok=True)
    (kb_eval / "answer_subset_v1.json").write_text(
        json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8"
    )

    parser = build_parser()
    args = parser.parse_args(["answers", "--answer-profile", "hybrid_rerank"])  # missing --confirm-paid
    cmd_answers(args)

    out = capsys.readouterr().out
    assert "--confirm-paid missing: no provider call made" in out
    assert not (tmp_path / "results" / "budgets").exists()


def test_cli_answers_resume_without_confirm_paid_fails_consent_gate_zero_calls(monkeypatch, tmp_path, capsys):
    """Resume without --confirm-paid must be rejected at preflight before creating Qdrant/budget."""
    from evaluation import evaluator
    dataset = _dummy_dataset(tmp_path)
    settings = _dummy_settings(tmp_path, dataset.dataset_path)

    monkeypatch.setattr(evaluator, "_load_cases", lambda: (settings, dataset))
    monkeypatch.setattr(evaluator, "RESULTS_DIR", tmp_path / "results")

    kb_eval = tmp_path / "foods" / "evaluation"
    kb_eval.mkdir(parents=True, exist_ok=True)
    (kb_eval / "answer_subset_v1.json").write_text(
        json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8"
    )

    parser = build_parser()
    # Resume missing --confirm-paid
    args = parser.parse_args(["answers", "--answer-profile", "hybrid_rerank", "--resume", "generation-20260823-120000-hybrid_rerank-6d023e0a"])
    cmd_answers(args)

    out = capsys.readouterr().out
    assert "--confirm-paid missing: no provider call made" in out
    assert not (tmp_path / "results" / "budgets").exists()


def test_cli_answers_fresh_with_calibration_flag_rejected(monkeypatch, tmp_path):
    """Fresh paid run cannot specify --calibration reuse."""
    from evaluation import evaluator
    dataset = _dummy_dataset(tmp_path)
    settings = _dummy_settings(tmp_path, dataset.dataset_path)

    monkeypatch.setattr(evaluator, "_load_cases", lambda: (settings, dataset))
    monkeypatch.setattr(evaluator, "RESULTS_DIR", tmp_path / "results")

    kb_eval = tmp_path / "foods" / "evaluation"
    kb_eval.mkdir(parents=True, exist_ok=True)
    (kb_eval / "answer_subset_v1.json").write_text(
        json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8"
    )

    parser = build_parser()
    args = parser.parse_args([
        "answers", "--answer-profile", "hybrid_rerank", "--confirm-paid",
        "--calibration", "calibration-20260823-120000-judge-6d023e0a"
    ])

    with pytest.raises(SystemExit, match="fresh run does not support --calibration reuse"):
        cmd_answers(args)


def test_cli_answers_resume_without_budget_state_fails_closed(monkeypatch, tmp_path):
    from evaluation import evaluator
    dataset = _dummy_dataset(tmp_path)
    settings = _dummy_settings(tmp_path, dataset.dataset_path)

    monkeypatch.setattr(evaluator, "_load_cases", lambda: (settings, dataset))
    monkeypatch.setattr(evaluator, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(evaluator, "get_client", lambda *a, **k: _FakeClient())
    monkeypatch.setattr(evaluator, "compute_corpus_checksum", lambda *a, **k: "corp-hash-1")
    monkeypatch.setattr(evaluator, "config_fingerprint", lambda *a, **k: "cfg-hash-1")

    kb_eval = tmp_path / "foods" / "evaluation"
    kb_eval.mkdir(parents=True, exist_ok=True)
    (kb_eval / "answer_subset_v1.json").write_text(
        json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8"
    )

    parser = build_parser()
    args = parser.parse_args(["answers", "--answer-profile", "hybrid_rerank", "--confirm-paid", "--resume", "generation-20260823-120000-hybrid_rerank-6d023e0a"])

    with pytest.raises(SystemExit, match="no durable budget state found"):
        cmd_answers(args)


def test_cli_answers_resume_with_mismatched_calibration_fails_zero_calls(monkeypatch, tmp_path):
    from evaluation import evaluator
    dataset = _dummy_dataset(tmp_path)
    settings = _dummy_settings(tmp_path, dataset.dataset_path)

    results = tmp_path / "results"
    budget_dir = results / "budgets"
    budget_dir.mkdir(parents=True, exist_ok=True)

    gen_run_id = "generation-20260823-120000-hybrid_rerank-6d023e0a"
    cal_linked_id = "calibration-20260823-120000-judge-6d023e0a"

    # Create valid budget bound to cal_linked_id using real hashes
    identity = {
        "dataset_checksum": dataset.dataset_checksum,
        "config_checksum": "cfg-hash-1",
        "corpus_checksum": "corp-hash-1",
        "collection_name": "hue_foods_e5_small_384",
        "answer_profile": "hybrid_rerank",
        "answer_model": "gpt-5.4-nano",
        "judge_model": "gpt-5.4-mini",
        "generation_prompt_hash": answer_eval.GENERATION_PROMPT_HASH,
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "rubric_prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "calibration_run_id": cal_linked_id,
        "pricing_checksum": compute_pricing_checksum(),
    }
    CallBudget.create(budget_dir / f"{gen_run_id}.json", identity, max_calls=64, max_cost_usd=0.50)

    monkeypatch.setattr(evaluator, "_load_cases", lambda: (settings, dataset))
    monkeypatch.setattr(evaluator, "RESULTS_DIR", results)
    monkeypatch.setattr(evaluator, "get_client", lambda *a, **k: _FakeClient())
    monkeypatch.setattr(evaluator, "compute_corpus_checksum", lambda *a, **k: "corp-hash-1")
    monkeypatch.setattr(evaluator, "config_fingerprint", lambda *a, **k: "cfg-hash-1")

    kb_eval = tmp_path / "foods" / "evaluation"
    kb_eval.mkdir(parents=True, exist_ok=True)
    (kb_eval / "answer_subset_v1.json").write_text(
        json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8"
    )

    parser = build_parser()
    # Pass mismatched calibration with --confirm-paid
    args = parser.parse_args([
        "answers", "--answer-profile", "hybrid_rerank", "--confirm-paid",
        "--resume", gen_run_id,
        "--calibration", "calibration-DIFFERENT-judge-6d023e0a"
    ])

    with pytest.raises(SystemExit, match="calibration mismatch"):
        cmd_answers(args)


def test_cli_all_delegates_cleanly_without_attribute_error(monkeypatch, tmp_path, capsys):
    """cmd_all must not raise AttributeError when delegating to cmd_answers."""
    from evaluation import evaluator
    dataset = _dummy_dataset(tmp_path)
    settings = _dummy_settings(tmp_path, dataset.dataset_path)

    monkeypatch.setattr(evaluator, "_load_cases", lambda: (settings, dataset))
    monkeypatch.setattr(evaluator, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(evaluator, "run_retrieval", lambda *a, **k: None)

    kb_eval = tmp_path / "foods" / "evaluation"
    kb_eval.mkdir(parents=True, exist_ok=True)
    (kb_eval / "answer_subset_v1.json").write_text(
        json.dumps({"cases": [{"case_id": c.case_id} for c in dataset.cases]}), encoding="utf-8"
    )

    parser = build_parser()
    args = parser.parse_args(["all", "--answer-profile", "hybrid_rerank", "--max-cases", "5"])
    cmd_all(args)

    out = capsys.readouterr().out
    assert "--confirm-paid missing: no provider call made" in out
