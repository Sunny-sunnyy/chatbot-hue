"""Deterministic tests for durable budget accounting (backend/evaluation/budget.py)."""

import json
import math
from pathlib import Path
import pytest

from evaluation.budget import (
    BUDGET_SCHEMA_VERSION,
    BudgetIntegrityError,
    CallBudget,
    CallBudgetExceeded,
    UnknownModelError,
    compute_pricing_checksum,
    cost_estimate_usd,
)


def _sample_identity():
    return {
        "dataset_checksum": "6d023e0a891e6536d31f7dc70c07f9e1d5cd06f00033f50fa438721344646d8c",
        "config_checksum": "957db8fa70752174c84a86bdf3b586ec45ff6064fe51a2cf6c41b8aa4d1be257",
        "corpus_checksum": "da602fbeee68ff2ea312ce7136ad3f0e4d73088e7e16c01411eaf4d6b5fb8965",
        "collection_name": "hue_foods_e5_small_384",
        "answer_profile": "hybrid_rerank",
        "answer_model": "gpt-5.4-nano",
        "judge_model": "gpt-5.4-mini",
        "generation_prompt_hash": "e6fbcef380d19a273a5a7dc52613d7e79fc94e9f783f98205f2479e0f666f2bf",
        "rubric_version": "v1",
        "rubric_prompt_hash": "4e45983e20084534720977464ce7870a442e3da3424177d54388835848c26fc4",
        "calibration_run_id": "calibration-20260823-120000-judge-6d023e0a",
        "pricing_checksum": compute_pricing_checksum(),
    }


def test_01_create_state_with_valid_identity_and_limits(tmp_path):
    budget_file = tmp_path / "generation-20260823-120000-hybrid_rerank-6d023e0a.json"
    identity = _sample_identity()
    budget = CallBudget.create(budget_file, identity, max_calls=64, max_cost_usd=0.50)

    assert budget_file.exists()
    assert budget.calls == 0
    assert budget.effective_cost_usd == 0.0
    assert budget.max_calls == 64
    assert budget.max_cost_usd == 0.50

    data = json.loads(budget_file.read_text(encoding="utf-8"))
    assert data["schema_version"] == BUDGET_SCHEMA_VERSION
    assert data["package_id"] == "generation-20260823-120000-hybrid_rerank-6d023e0a"
    assert data["limits"]["max_calls"] == 64
    assert data["limits"]["max_cost_usd"] == 0.50
    assert data["identity"]["dataset_checksum"] == identity["dataset_checksum"]


def test_02_duplicate_create_rejected(tmp_path):
    budget_file = tmp_path / "test_run.json"
    identity = _sample_identity()
    CallBudget.create(budget_file, identity, max_calls=64, max_cost_usd=0.50)

    with pytest.raises(FileExistsError, match="already exists"):
        CallBudget.create(budget_file, identity, max_calls=64, max_cost_usd=0.50)


def test_03_reserve_persists_before_call_and_settle_success_updates_actual_cost(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    # Reserve call
    res = budget.reserve(
        stage="generation",
        case_id="foods-0001",
        attempt_number=1,
        model="gpt-5.4-nano",
        estimated_input_tokens=1000,
        estimated_output_tokens=500,
    )
    # Check disk state immediately after reserve
    data = json.loads(budget_file.read_text(encoding="utf-8"))
    assert data["totals"]["calls"] == 1
    assert data["attempts"][0]["status"] == "reserved"
    assert data["attempts"][0]["attempt_id"] == res["attempt_id"]
    assert data["attempts"][0]["reserved_cost_usd"] > 0
    assert budget.calls == 1
    assert budget.unresolved_reserved_usd > 0

    # Provider call succeeds with actual usage
    actual_cost = budget.settle_success(res, usage_tokens={"input": 800, "output": 300})
    assert actual_cost > 0
    assert budget.calls == 1
    assert budget.unresolved_reserved_usd == 0.0
    assert budget.settled_cost_usd == actual_cost
    assert budget.effective_cost_usd == actual_cost

    data_after = json.loads(budget_file.read_text(encoding="utf-8"))
    assert data_after["attempts"][0]["status"] == "settled_success"
    assert data_after["attempts"][0]["usage_is_estimate"] is False
    assert data_after["attempts"][0]["charged_cost_usd"] == actual_cost


def test_04_atomic_write_failure_during_reserve_aborts_call(tmp_path, monkeypatch):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    # Simulate atomic rename/replace failure
    def mock_replace(src, dst):
        raise OSError("Simulated disk write failure")

    monkeypatch.setattr("os.replace", mock_replace)

    provider_called = False
    with pytest.raises(OSError, match="Simulated disk write failure"):
        res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)
        provider_called = True

    assert not provider_called
    assert budget.calls == 0
    assert len(budget.attempts) == 0


def test_05_settle_success_without_usage_charges_reservation_estimate(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=1000, estimated_output_tokens=500)
    cost = budget.settle_success(res, usage_tokens=None)

    assert cost == res["estimate"]
    data = json.loads(budget_file.read_text(encoding="utf-8"))
    assert data["attempts"][0]["status"] == "settled_success"
    assert data["attempts"][0]["usage_is_estimate"] is True
    assert data["attempts"][0]["charged_cost_usd"] == res["estimate"]


def test_06_settle_error_charges_reservation_estimate_and_records_error_type(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    res = budget.reserve("judge", "foods-0001", model="gpt-5.4-mini", estimated_input_tokens=2000, estimated_output_tokens=500)
    cost = budget.settle_error(res, error_type="timeout")

    assert cost == res["estimate"]
    data = json.loads(budget_file.read_text(encoding="utf-8"))
    assert data["attempts"][0]["status"] == "settled_error"
    assert data["attempts"][0]["error_type"] == "timeout"
    assert data["attempts"][0]["charged_cost_usd"] == res["estimate"]


def test_07_unresolved_reservation_counts_call_and_cost_on_reload(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    # Reserve but do NOT settle (simulated process crash)
    res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=2000, estimated_output_tokens=1000)

    # Reload from disk in a fresh instance
    reloaded = CallBudget.load(budget_file, _sample_identity())
    assert reloaded.calls == 1
    assert reloaded.unresolved_reserved_usd == res["estimate"]
    assert reloaded.settled_cost_usd == 0.0
    assert reloaded.effective_cost_usd == res["estimate"]


def test_08_duplicate_or_invalid_attempt_transition_rejected(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)
    budget.settle_success(res)

    # Settling an already settled attempt must fail
    with pytest.raises(BudgetIntegrityError, match="cannot be settled"):
        budget.settle_success(res)

    with pytest.raises(BudgetIntegrityError, match="cannot be settled"):
        budget.settle_error(res, error_type="timeout")


def test_09_duplicate_attempt_id_in_file_fails_load(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)
    res1 = budget.reserve("generation", "foods-0001", attempt_number=1, model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)
    budget.settle_success(res1)

    # Tamper file to duplicate attempt_id
    data = json.loads(budget_file.read_text(encoding="utf-8"))
    data["attempts"].append(dict(data["attempts"][0]))
    budget_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(BudgetIntegrityError, match="duplicate attempt_id"):
        CallBudget.load(budget_file, _sample_identity())


def test_10_tampered_totals_in_file_fails_load(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)
    res1 = budget.reserve("generation", "foods-0001", attempt_number=1, model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)
    budget.settle_success(res1)

    data = json.loads(budget_file.read_text(encoding="utf-8"))
    data["totals"]["calls"] = 999  # Tamper call count
    budget_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(BudgetIntegrityError, match="totals mismatch"):
        CallBudget.load(budget_file, _sample_identity())


def test_11_unknown_model_raises_unknown_model_error():
    with pytest.raises(UnknownModelError, match="no approved price table entry"):
        cost_estimate_usd("gpt-unknown-999", 100, 100)


def test_12_cross_process_persisted_one_call_with_max_calls_1_blocks_next_call(tmp_path):
    budget_file = tmp_path / "test_run.json"
    # Process 1 makes 1 call with max_calls=1
    p1 = CallBudget.create(budget_file, _sample_identity(), max_calls=1, max_cost_usd=0.50)
    res1 = p1.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)
    p1.settle_success(res1)

    # Process 2 resumes with max_calls=1
    p2 = CallBudget.load(budget_file, _sample_identity(), max_calls=1)
    with pytest.raises(CallBudgetExceeded, match="call cap reached"):
        p2.reserve("judge", "foods-0001", model="gpt-5.4-mini", estimated_input_tokens=100, estimated_output_tokens=100)


def test_13_cross_process_cost_cap_reached_blocks_next_reservation(tmp_path):
    budget_file = tmp_path / "test_run.json"
    # Create with very small cost cap
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=10, max_cost_usd=0.0001)

    # Reserve call that exceeds small cap
    with pytest.raises(CallBudgetExceeded, match="cost cap reached"):
        budget.reserve("judge", "foods-0001", model="gpt-5.4-mini", estimated_input_tokens=3000, estimated_output_tokens=700)


def test_14_failed_first_and_success_second_preserves_both_attempts_and_costs(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=10, max_cost_usd=0.50)

    # Attempt 1: fails
    res1 = budget.reserve("generation", "foods-0001", attempt_number=1, model="gpt-5.4-nano", estimated_input_tokens=1000, estimated_output_tokens=500)
    cost1 = budget.settle_error(res1, error_type="timeout")

    # Attempt 2 (retry): succeeds
    res2 = budget.reserve("generation", "foods-0001", attempt_number=2, model="gpt-5.4-nano", estimated_input_tokens=1000, estimated_output_tokens=500)
    cost2 = budget.settle_success(res2, usage_tokens={"input": 900, "output": 400})

    assert budget.calls == 2
    assert budget.effective_cost_usd == round(cost1 + cost2, 8)

    # Reload in new process and assert both attempts are preserved
    reloaded = CallBudget.load(budget_file, _sample_identity())
    assert reloaded.calls == 2
    assert len(reloaded.attempts) == 2
    assert reloaded.attempts[0]["attempt_number"] == 1
    assert reloaded.attempts[0]["status"] == "settled_error"
    assert reloaded.attempts[1]["attempt_number"] == 2
    assert reloaded.attempts[1]["status"] == "settled_success"
    assert reloaded.effective_cost_usd == round(cost1 + cost2, 8)


def test_15_crash_after_provider_return_before_settle_holds_reservation_across_reload(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=2, max_cost_usd=0.50)

    # Process 1 reserves, but crashes before settle
    res1 = budget.reserve("generation", "foods-0001", attempt_number=1, model="gpt-5.4-nano", estimated_input_tokens=1000, estimated_output_tokens=500)

    # Process 2 loads the budget
    p2 = CallBudget.load(budget_file, _sample_identity(), max_calls=2)
    assert p2.calls == 1
    assert p2.unresolved_reserved_usd == res1["estimate"]

    # Process 2 can make 1 retry attempt because max_calls=2
    res2 = p2.reserve("generation", "foods-0001", attempt_number=2, model="gpt-5.4-nano", estimated_input_tokens=1000, estimated_output_tokens=500)
    p2.settle_success(res2, usage_tokens={"input": 800, "output": 400})
    assert p2.calls == 2

    # Process 2 attempting a 3rd call will be blocked
    with pytest.raises(CallBudgetExceeded, match="call cap reached"):
        p2.reserve("judge", "foods-0001", attempt_number=1, model="gpt-5.4-mini", estimated_input_tokens=1000, estimated_output_tokens=500)


def test_16_repeated_resume_does_not_reset_or_double_count_attempts(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=10, max_cost_usd=0.50)

    res1 = budget.reserve("calibration", "s0", model="gpt-5.4-mini", estimated_input_tokens=1000, estimated_output_tokens=300)
    budget.settle_success(res1, usage_tokens={"input": 900, "output": 250})

    # Reload multiple times
    r1 = CallBudget.load(budget_file, _sample_identity())
    r2 = CallBudget.load(budget_file, _sample_identity())
    r3 = CallBudget.load(budget_file, _sample_identity())

    assert r1.calls == 1
    assert r2.calls == 1
    assert r3.calls == 1
    assert r1.effective_cost_usd == r3.effective_cost_usd


def test_17_load_with_mismatched_identity_fails(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=10, max_cost_usd=0.50)

    tampered = _sample_identity()
    tampered["config_checksum"] = "mismatched_config_hash"

    with pytest.raises(BudgetIntegrityError, match="budget identity mismatch"):
        CallBudget.load(budget_file, expected_identity=tampered)


def test_18_load_with_mismatched_limits_fails(tmp_path):
    budget_file = tmp_path / "test_run.json"
    CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    with pytest.raises(BudgetIntegrityError, match="cannot resume with different max_calls"):
        CallBudget.load(budget_file, _sample_identity(), max_calls=128)

    with pytest.raises(BudgetIntegrityError, match="cannot resume with different max_cost_usd"):
        CallBudget.load(budget_file, _sample_identity(), max_cost_usd=1.0)


def test_19_load_with_mismatched_pricing_fails(tmp_path):
    budget_file = tmp_path / "test_run.json"
    CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    data = json.loads(budget_file.read_text(encoding="utf-8"))
    data["identity"]["pricing_checksum"] = "outdated_pricing_hash"
    budget_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(BudgetIntegrityError, match="pricing checksum mismatch"):
        CallBudget.load(budget_file, _sample_identity())


def test_20_load_with_negative_token_counts_or_costs_fails(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)
    res = budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)
    budget.settle_success(res)

    data = json.loads(budget_file.read_text(encoding="utf-8"))
    data["attempts"][0]["charged_cost_usd"] = -0.5
    budget_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(BudgetIntegrityError, match=r"invalid.*cost"):
        CallBudget.load(budget_file, _sample_identity())


def test_21_numeric_validation_rejects_nan_inf_and_negatives(tmp_path):
    budget_file = tmp_path / "test_run.json"

    # Reject NaN and Inf in create
    with pytest.raises(BudgetIntegrityError, match="max_calls"):
        CallBudget.create(budget_file, _sample_identity(), max_calls=float("nan"), max_cost_usd=0.50)

    with pytest.raises(BudgetIntegrityError, match="max_cost_usd"):
        CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=float("nan"))

    with pytest.raises(BudgetIntegrityError, match="max_cost_usd"):
        CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=float("inf"))

    with pytest.raises(BudgetIntegrityError, match="max_cost_usd"):
        CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=-0.50)

    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    # Reject negative / non-integer in reserve
    with pytest.raises(ValueError, match="token estimates"):
        budget.reserve("generation", "foods-0001", model="gpt-5.4-nano", estimated_input_tokens=-10, estimated_output_tokens=100)

    with pytest.raises(ValueError, match="attempt_number"):
        budget.reserve("generation", "foods-0001", attempt_number=0, model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)

    res = budget.reserve("generation", "foods-0001", attempt_number=1, model="gpt-5.4-nano", estimated_input_tokens=100, estimated_output_tokens=100)

    # Reject invalid usage_tokens in settle_success
    with pytest.raises(BudgetIntegrityError, match="invalid usage_tokens"):
        budget.settle_success(res, usage_tokens={"input": -5, "output": 100})


def test_22_persisted_reservations_cannot_be_refunded(tmp_path):
    budget_file = tmp_path / "test_run.json"
    budget = CallBudget.create(budget_file, _sample_identity(), max_calls=64, max_cost_usd=0.50)

    # Verify cancel() method does NOT exist
    assert not hasattr(budget, "cancel")
