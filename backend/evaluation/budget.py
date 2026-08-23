"""Durable run-wide provider call and cost budget accounting.

Manages persistent budget states for Phase 7 evaluation runs (calibration +
generation + judge). State is persisted atomically to disk as a JSON artifact
at backend/evaluation/results/budgets/<generation_run_id>.json.

Key invariants enforced:
1. Provider calls are reserved and atomically persisted before API dispatch.
2. Unresolved reservations after a crash count as 1 call and conservative cost.
3. Retries are tracked as new attempts with distinct attempt IDs.
4. Resumed runs hydrate cumulative calls/cost prior to making any provider calls.
5. Limits (max_calls, max_cost_usd) and package identities are frozen and validated.
6. Non-finite numbers (NaN, Inf) and negative values are rejected fail-closed.
7. Persisted reservations are never refunded.
"""

from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import uuid

BUDGET_SCHEMA_VERSION = 1

# Approved price table (USD per 1,000,000 tokens)
EST_PRICE_PER_1M = {
    "gpt-5.4-nano": {"input": 0.15, "output": 0.60},
    "gpt-5.4-mini": {"input": 0.60, "output": 2.50},
}


class CallBudgetExceeded(RuntimeError):
    """Raised before a provider call when either call cap or cost cap would be exceeded."""


class UnknownModelError(RuntimeError):
    """Raised when a model has no approved price table entry (fail closed)."""


class BudgetIntegrityError(ValueError):
    """Raised when a budget state file is corrupted, tampered, or mismatched."""


def _is_finite_nonnegative_number(val: Any) -> bool:
    """Check if value is a finite, non-negative number (int, float, Decimal), rejecting NaN/Inf/bool."""
    if isinstance(val, bool) or not isinstance(val, (int, float, Decimal)):
        return False
    if isinstance(val, (int, float)) and not math.isfinite(val):
        return False
    if isinstance(val, Decimal) and not val.is_finite():
        return False
    return val >= 0


def _is_positive_integer(val: Any) -> bool:
    """Check if value is a positive integer (> 0), rejecting bool/float/non-integers."""
    return isinstance(val, int) and not isinstance(val, bool) and val > 0


def _is_nonnegative_integer(val: Any) -> bool:
    """Check if value is a non-negative integer (>= 0), rejecting bool/float/non-integers."""
    return isinstance(val, int) and not isinstance(val, bool) and val >= 0


def compute_pricing_checksum(price_table: Optional[Dict[str, Dict[str, float]]] = None) -> str:
    """Deterministic SHA-256 fingerprint over the approved price table."""
    table = price_table if price_table is not None else EST_PRICE_PER_1M
    payload = json.dumps(table, sort_keys=True, allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def cost_estimate_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate conservative cost in USD for the given token counts.

    Fails closed with UnknownModelError if the model is not in the price table,
    or ValueError if token counts are negative/non-finite.
    """
    if not _is_nonnegative_integer(input_tokens) or not _is_nonnegative_integer(output_tokens):
        raise ValueError(f"token counts must be non-negative integers, got input={input_tokens!r}, output={output_tokens!r}")
    prices = EST_PRICE_PER_1M.get(model)
    if prices is None:
        raise UnknownModelError(f"no approved price table entry for model {model!r}")
    inp_dec = Decimal(input_tokens) * Decimal(str(prices["input"])) / Decimal("1000000")
    out_dec = Decimal(output_tokens) * Decimal(str(prices["output"])) / Decimal("1000000")
    total = (inp_dec + out_dec).quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)
    return float(total)


class CallBudget:
    """Durable sequential provider call and cost accountant.

    Tracks attempts across calibration, generation, and judge stages with
    atomic disk persistence to prevent cap bypass across crashes and process restarts.
    """

    def __init__(
        self,
        max_calls: int = 64,
        max_cost_usd: float = 0.50,
        *,
        path: Optional[Union[str, Path]] = None,
        package_id: Optional[str] = None,
        identity: Optional[Dict[str, Any]] = None,
    ):
        if not _is_positive_integer(max_calls):
            raise BudgetIntegrityError(f"max_calls must be a positive integer, got {max_calls!r}")
        if not _is_finite_nonnegative_number(max_cost_usd) or max_cost_usd <= 0:
            raise BudgetIntegrityError(f"max_cost_usd must be a positive finite number, got {max_cost_usd!r}")

        self.max_calls = int(max_calls)
        self.max_cost_usd = float(max_cost_usd)
        self.path = Path(path).resolve() if path is not None else None
        self.package_id = package_id or (self.path.stem if self.path is not None else "ephemeral")
        self.identity = identity or {}
        self.schema_version = BUDGET_SCHEMA_VERSION

        self.attempts: List[Dict[str, Any]] = []
        self._calls = 0
        self._settled_cost_usd = Decimal("0.0")
        self._unresolved_reserved_usd = Decimal("0.0")
        self._effective_cost_usd = Decimal("0.0")

    @property
    def calls(self) -> int:
        return self._calls

    @calls.setter
    def calls(self, val: int) -> None:
        self._calls = val

    @property
    def cost_usd(self) -> float:
        return float(self._settled_cost_usd)

    @cost_usd.setter
    def cost_usd(self, val: float) -> None:
        self._settled_cost_usd = Decimal(str(val))

    @property
    def settled_cost_usd(self) -> float:
        return float(self._settled_cost_usd)

    @property
    def unresolved_reserved_usd(self) -> float:
        return float(self._unresolved_reserved_usd)

    @property
    def reserved_usd(self) -> float:
        return float(self._unresolved_reserved_usd)

    @property
    def effective_cost_usd(self) -> float:
        return float(self._effective_cost_usd)

    def _recalculate_totals(self) -> None:
        calls = 0
        settled_dec = Decimal("0.0")
        unresolved_dec = Decimal("0.0")

        for att in self.attempts:
            calls += 1
            status = att.get("status")
            res_cost = att.get("reserved_cost_usd")
            chg_cost = att.get("charged_cost_usd")

            if not _is_finite_nonnegative_number(res_cost) or not _is_finite_nonnegative_number(chg_cost):
                raise BudgetIntegrityError(
                    f"invalid non-finite or negative cost in attempt {att.get('attempt_id')}: "
                    f"reserved={res_cost!r}, charged={chg_cost!r}"
                )

            if status == "reserved":
                unresolved_dec += Decimal(str(res_cost))
            elif status in ("settled_success", "settled_error"):
                settled_dec += Decimal(str(chg_cost))
            else:
                raise BudgetIntegrityError(f"invalid attempt status {status!r} for attempt {att.get('attempt_id')}")

        self._calls = calls
        self._settled_cost_usd = settled_dec.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)
        self._unresolved_reserved_usd = unresolved_dec.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)
        self._effective_cost_usd = (settled_dec + unresolved_dec).quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)

    def _persist(self) -> None:
        self._recalculate_totals()
        if self.path is None:
            return
        payload = {
            "schema_version": self.schema_version,
            "package_id": self.package_id,
            "identity": self.identity,
            "limits": {
                "max_calls": self.max_calls,
                "max_cost_usd": self.max_cost_usd,
            },
            "attempts": self.attempts,
            "totals": {
                "calls": self.calls,
                "settled_cost_usd": float(self._settled_cost_usd),
                "unresolved_reserved_usd": float(self._unresolved_reserved_usd),
                "effective_cost_usd": float(self._effective_cost_usd),
            },
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_name(self.path.name + f".tmp.{os.getpid()}")
        try:
            with open(tmp_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, self.path)
        except Exception:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
            raise

    @classmethod
    def create(
        cls,
        path: Union[str, Path],
        identity: Dict[str, Any],
        max_calls: int = 64,
        max_cost_usd: float = 0.50,
    ) -> "CallBudget":
        """Create a new durable budget state file on disk. Refuses to overwrite."""
        target_path = Path(path).resolve()
        if target_path.exists():
            raise FileExistsError(f"budget state already exists; refusing to overwrite: {target_path}")

        if not _is_positive_integer(max_calls):
            raise BudgetIntegrityError(f"max_calls must be a positive integer, got {max_calls!r}")
        if not _is_finite_nonnegative_number(max_cost_usd) or max_cost_usd <= 0:
            raise BudgetIntegrityError(f"max_cost_usd must be a positive finite number, got {max_cost_usd!r}")

        req_keys = (
            "dataset_checksum", "config_checksum", "corpus_checksum",
            "collection_name", "answer_profile", "answer_model",
            "judge_model", "generation_prompt_hash", "rubric_version",
            "rubric_prompt_hash", "calibration_run_id", "pricing_checksum",
        )
        for k in req_keys:
            if k not in identity or not identity[k]:
                raise BudgetIntegrityError(f"budget identity missing required key {k!r}")

        expected_pricing = compute_pricing_checksum()
        if identity.get("pricing_checksum") != expected_pricing:
            raise BudgetIntegrityError(
                f"pricing checksum mismatch: expected {expected_pricing}, got {identity.get('pricing_checksum')}"
            )

        budget = cls(
            max_calls=max_calls,
            max_cost_usd=max_cost_usd,
            path=target_path,
            package_id=target_path.stem,
            identity=identity,
        )
        budget._persist()
        return budget

    @classmethod
    def load(
        cls,
        path: Union[str, Path],
        expected_identity: Optional[Dict[str, Any]] = None,
        max_calls: Optional[int] = None,
        max_cost_usd: Optional[float] = None,
    ) -> "CallBudget":
        """Load, validate, and hydrate an existing durable budget state file."""
        target_path = Path(path).resolve()
        if not target_path.exists():
            raise FileNotFoundError(f"budget state file not found: {target_path}")

        try:
            data = json.loads(target_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise BudgetIntegrityError(f"cannot read budget state file {target_path}: {exc}") from exc

        if not isinstance(data, dict):
            raise BudgetIntegrityError(f"invalid budget state format in {target_path}: not a JSON object")

        if data.get("schema_version") != BUDGET_SCHEMA_VERSION:
            raise BudgetIntegrityError(
                f"unsupported budget schema version: expected {BUDGET_SCHEMA_VERSION}, "
                f"got {data.get('schema_version')}"
            )

        if data.get("package_id") != target_path.stem:
            raise BudgetIntegrityError(
                f"package_id mismatch: expected {target_path.stem}, got {data.get('package_id')}"
            )

        identity = data.get("identity")
        if not isinstance(identity, dict):
            raise BudgetIntegrityError("budget identity is missing or invalid")

        expected_pricing = compute_pricing_checksum()
        if identity.get("pricing_checksum") != expected_pricing:
            raise BudgetIntegrityError(
                f"pricing checksum mismatch: expected {expected_pricing}, got {identity.get('pricing_checksum')}"
            )

        if expected_identity:
            for k, val in expected_identity.items():
                if k == "pricing_checksum":
                    continue
                if identity.get(k) != val:
                    raise BudgetIntegrityError(
                        f"budget identity mismatch for {k!r}: expected {val!r}, got {identity.get(k)!r}"
                    )

        limits = data.get("limits")
        if not isinstance(limits, dict):
            raise BudgetIntegrityError("budget limits are missing or invalid")

        stored_max_calls = limits.get("max_calls")
        stored_max_cost = limits.get("max_cost_usd")
        if not _is_positive_integer(stored_max_calls):
            raise BudgetIntegrityError(f"budget limits contain invalid max_calls {stored_max_calls!r}")
        if not _is_finite_nonnegative_number(stored_max_cost) or stored_max_cost <= 0:
            raise BudgetIntegrityError(f"budget limits contain invalid max_cost_usd {stored_max_cost!r}")

        if max_calls is not None:
            if not _is_positive_integer(max_calls):
                raise BudgetIntegrityError(f"requested max_calls must be a positive integer, got {max_calls!r}")
            if stored_max_calls != max_calls:
                raise BudgetIntegrityError(
                    f"cannot resume with different max_calls: frozen {stored_max_calls}, requested {max_calls}"
                )
        if max_cost_usd is not None:
            if not _is_finite_nonnegative_number(max_cost_usd) or max_cost_usd <= 0:
                raise BudgetIntegrityError(f"requested max_cost_usd must be a positive finite number, got {max_cost_usd!r}")
            if Decimal(str(stored_max_cost)) != Decimal(str(max_cost_usd)):
                raise BudgetIntegrityError(
                    f"cannot resume with different max_cost_usd: frozen {stored_max_cost}, requested {max_cost_usd}"
                )

        raw_attempts = data.get("attempts", [])
        if not isinstance(raw_attempts, list):
            raise BudgetIntegrityError("attempts must be a list")

        seen_ids = set()
        for att in raw_attempts:
            if not isinstance(att, dict):
                raise BudgetIntegrityError("attempt item is not a dictionary")
            aid = att.get("attempt_id")
            if not aid or not isinstance(aid, str):
                raise BudgetIntegrityError("attempt missing valid attempt_id")
            if aid in seen_ids:
                raise BudgetIntegrityError(f"duplicate attempt_id {aid!r} in budget state")
            seen_ids.add(aid)

            stage = att.get("stage")
            if stage not in ("calibration", "generation", "judge"):
                raise BudgetIntegrityError(f"invalid attempt stage {stage!r}")

            status = att.get("status")
            if status not in ("reserved", "settled_success", "settled_error"):
                raise BudgetIntegrityError(f"invalid attempt status {status!r}")

            att_num = att.get("attempt_number")
            if not _is_positive_integer(att_num):
                raise BudgetIntegrityError(f"invalid attempt_number {att_num!r} in attempt {aid}")

            res_cost = att.get("reserved_cost_usd")
            chg_cost = att.get("charged_cost_usd")
            if not _is_finite_nonnegative_number(res_cost) or not _is_finite_nonnegative_number(chg_cost):
                raise BudgetIntegrityError(f"invalid non-finite or negative cost values in attempt {aid}")

            tokens = att.get("usage_tokens")
            if tokens is not None:
                if (
                    not isinstance(tokens, dict)
                    or not _is_nonnegative_integer(tokens.get("input"))
                    or not _is_nonnegative_integer(tokens.get("output"))
                ):
                    raise BudgetIntegrityError(f"invalid usage_tokens in attempt {aid}")

        budget = cls(
            max_calls=stored_max_calls,
            max_cost_usd=stored_max_cost,
            path=target_path,
            package_id=target_path.stem,
            identity=identity,
        )
        budget.attempts = raw_attempts
        budget._recalculate_totals()

        stored_totals = data.get("totals", {})
        if stored_totals:
            calls_val = stored_totals.get("calls")
            if not _is_nonnegative_integer(calls_val) or calls_val != budget.calls:
                raise BudgetIntegrityError(
                    f"totals mismatch for calls: stored {calls_val!r}, computed {budget.calls}"
                )

            for cost_field, computed_val in (
                ("settled_cost_usd", budget._settled_cost_usd),
                ("unresolved_reserved_usd", budget._unresolved_reserved_usd),
                ("effective_cost_usd", budget._effective_cost_usd),
            ):
                raw_val = stored_totals.get(cost_field)
                if not _is_finite_nonnegative_number(raw_val):
                    raise BudgetIntegrityError(f"totals contains non-finite or negative {cost_field}: {raw_val!r}")
                if Decimal(str(raw_val)).quantize(Decimal("0.00000001")) != computed_val:
                    raise BudgetIntegrityError(
                        f"totals mismatch for {cost_field}: stored {raw_val}, computed {float(computed_val)}"
                    )

        return budget

    def reserve(
        self,
        stage_or_model: Optional[str] = None,
        case_id_or_input_tokens: Any = 0,
        generation_run_id_or_output_tokens: Any = 0,
        attempt_number: int = 1,
        model: Optional[str] = None,
        estimated_input_tokens: int = 0,
        estimated_output_tokens: int = 0,
        stage: Optional[str] = None,
        case_id: Optional[str] = None,
        generation_run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Reserve one provider call against both call and cost caps.

        Supports both positional legacy calls (model, input_tokens, output_tokens)
        and keyword-rich stage/case attempt calls.
        Atomically persists the reservation to disk before returning to caller.
        Raises CallBudgetExceeded if either cap would be reached.
        """
        if (
            isinstance(case_id_or_input_tokens, (int, float))
            and not isinstance(case_id_or_input_tokens, bool)
            and model is None
            and not stage
            and not case_id
            and (stage_or_model in EST_PRICE_PER_1M or not any(k in kwargs for k in ("stage", "case_id")))
        ):
            actual_model = stage_or_model
            inp_tok = case_id_or_input_tokens
            out_tok = generation_run_id_or_output_tokens
            act_stage = kwargs.get("stage", "generation")
            act_case_id = kwargs.get("case_id", "ephemeral")
            gid = kwargs.get("generation_run_id")
            att_num = kwargs.get("attempt_number", attempt_number if attempt_number is not None else 1)
        else:
            act_stage = stage or stage_or_model or kwargs.get("stage", "generation")
            act_case_id = str(case_id or case_id_or_input_tokens or kwargs.get("case_id", "ephemeral"))
            gid = generation_run_id or (
                generation_run_id_or_output_tokens
                if isinstance(generation_run_id_or_output_tokens, str)
                else kwargs.get("generation_run_id")
            )
            actual_model = model or kwargs.get("model")
            inp_tok = estimated_input_tokens
            out_tok = estimated_output_tokens
            att_num = attempt_number if attempt_number is not None else kwargs.get("attempt_number", 1)

        if not _is_nonnegative_integer(inp_tok) or not _is_nonnegative_integer(out_tok):
            raise ValueError(f"token estimates must be non-negative integers, got input={inp_tok!r}, output={out_tok!r}")
        if not _is_positive_integer(att_num):
            raise ValueError(f"attempt_number must be a positive integer, got {att_num!r}")

        if act_stage not in ("calibration", "generation", "judge"):
            raise ValueError(f"unknown stage {act_stage!r}")
        if not actual_model:
            raise ValueError("model must be specified for reservation")

        estimate = cost_estimate_usd(actual_model, int(inp_tok), int(out_tok))
        estimate_dec = Decimal(str(estimate))

        # Check call cap
        if self._calls + 1 > self.max_calls:
            raise CallBudgetExceeded(
                f"call cap reached ({self._calls}/{self.max_calls})"
            )

        # Check cost cap
        if self._effective_cost_usd + estimate_dec > Decimal(str(self.max_cost_usd)):
            raise CallBudgetExceeded(
                f"cost cap reached (${float(self._effective_cost_usd):.6f} + "
                f"~${estimate:.6f} > ${self.max_cost_usd})"
            )

        attempt_id = f"{act_stage}:{act_case_id}:{att_num}:{uuid.uuid4().hex[:8]}"
        attempt = {
            "attempt_id": attempt_id,
            "stage": act_stage,
            "case_id": act_case_id,
            "generation_run_id": gid,
            "attempt_number": int(att_num),
            "model": actual_model,
            "reserved_cost_usd": estimate,
            "charged_cost_usd": 0.0,
            "status": "reserved",
            "usage_tokens": None,
            "usage_is_estimate": True,
            "error_type": None,
        }

        self.attempts.append(attempt)
        try:
            self._persist()
        except Exception:
            self.attempts.pop()
            self._recalculate_totals()
            raise

        return {
            "attempt_id": attempt_id,
            "model": actual_model,
            "estimate": estimate,
            "stage": act_stage,
            "case_id": act_case_id,
        }

    def settle_success(
        self,
        reservation_or_id: Union[str, Dict[str, Any]],
        usage_tokens: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Settle a successful provider call with actual token usage or reservation estimate."""
        attempt_id = (
            reservation_or_id["attempt_id"]
            if isinstance(reservation_or_id, dict)
            else str(reservation_or_id)
        )
        attempt = next((a for a in self.attempts if a.get("attempt_id") == attempt_id), None)
        if attempt is None:
            raise BudgetIntegrityError(f"unknown attempt_id {attempt_id!r}")
        if attempt.get("status") != "reserved":
            raise BudgetIntegrityError(
                f"attempt {attempt_id!r} cannot be settled: status is {attempt.get('status')!r}"
            )

        if usage_tokens is not None:
            if (
                not isinstance(usage_tokens, dict)
                or not _is_nonnegative_integer(usage_tokens.get("input"))
                or not _is_nonnegative_integer(usage_tokens.get("output"))
            ):
                raise BudgetIntegrityError(f"invalid usage_tokens for attempt {attempt_id!r}: {usage_tokens!r}")

            actual = cost_estimate_usd(attempt["model"], int(usage_tokens["input"]), int(usage_tokens["output"]))
            attempt["charged_cost_usd"] = actual
            attempt["usage_tokens"] = {"input": int(usage_tokens["input"]), "output": int(usage_tokens["output"])}
            attempt["usage_is_estimate"] = False
        else:
            attempt["charged_cost_usd"] = attempt["reserved_cost_usd"]
            attempt["usage_is_estimate"] = True

        attempt["status"] = "settled_success"
        self._persist()
        return attempt["charged_cost_usd"]

    def settle_error(
        self,
        reservation_or_id: Union[str, Dict[str, Any]],
        error_type: Optional[str] = None,
    ) -> float:
        """Settle a failed provider call by charging the conservative reservation estimate."""
        attempt_id = (
            reservation_or_id["attempt_id"]
            if isinstance(reservation_or_id, dict)
            else str(reservation_or_id)
        )
        attempt = next((a for a in self.attempts if a.get("attempt_id") == attempt_id), None)
        if attempt is None:
            raise BudgetIntegrityError(f"unknown attempt_id {attempt_id!r}")
        if attempt.get("status") != "reserved":
            raise BudgetIntegrityError(
                f"attempt {attempt_id!r} cannot be settled: status is {attempt.get('status')!r}"
            )

        attempt["charged_cost_usd"] = attempt["reserved_cost_usd"]
        attempt["usage_is_estimate"] = True
        attempt["error_type"] = str(error_type) if error_type else "unknown_error"
        attempt["status"] = "settled_error"
        self._persist()
        return attempt["charged_cost_usd"]

    def settle(
        self,
        reservation_or_id: Union[str, Dict[str, Any]],
        usage_tokens: Optional[Dict[str, Any]] = None,
    ) -> float:
        """Compatibility settle method matching previous in-memory API."""
        if usage_tokens is not None:
            return self.settle_success(reservation_or_id, usage_tokens)
        return self.settle_success(reservation_or_id, None)

    def snapshot(self) -> Dict[str, Any]:
        """Return snapshot summary of current budget state."""
        self._recalculate_totals()
        return {
            "schema_version": self.schema_version,
            "package_id": self.package_id,
            "calls": self.calls,
            "settled_cost_usd": float(self._settled_cost_usd),
            "unresolved_reserved_usd": float(self._unresolved_reserved_usd),
            "effective_cost_usd": float(self._effective_cost_usd),
            "has_estimate": any(a.get("usage_is_estimate", True) for a in self.attempts),
            "unresolved_count": sum(1 for a in self.attempts if a.get("status") == "reserved"),
            "attempts_count": len(self.attempts),
            "artifact_path": f"budgets/{self.package_id}.json",
            "artifact_checksum": self.compute_state_checksum(),
        }

    def compute_state_checksum(self) -> Optional[str]:
        """Compute SHA-256 checksum over the persisted budget state file on disk."""
        if self.path is not None and self.path.exists():
            return hashlib.sha256(self.path.read_bytes()).hexdigest()
        return None
