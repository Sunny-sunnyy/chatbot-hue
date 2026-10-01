"""Bounded exactly-five-call live runner for Full-corpus Phase 6 OpenAI baseline."""
import argparse
import asyncio
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BACKEND_DIR.parent
for _p in (str(REPO_DIR), str(BACKEND_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from httpx import ASGITransport, AsyncClient

from api.app import create_app
from core.settings_loader import load_settings
from llm.evidence_recorder import record_evidence
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.representation_b import build_representation_b_search_text
from vectorstore.qdrant import client_from_settings

logger = logging.getLogger("phase6_live_smoke")
CITATION_RE = re.compile(r"\[(\d+)\]")

EXPECTED_CASES_SCHEMA_VERSION = "phase_6_full_corpus_live_cases:v1"
EXPECTED_CASE_IDS = [
    "direct_fact",
    "multi_source_synthesis",
    "conditional_evidence",
    "out_of_scope",
]


def validate_cases_data(cases_data: dict) -> list[dict]:
    """Validate cases schema version, length, exact case IDs and order.

    Fails closed on extra top-level keys or extra/missing case keys.
    """
    if not isinstance(cases_data, dict):
        raise ValueError("Cases file must contain a JSON object.")

    allowed_top_keys = {"schema_version", "cases"}
    extra_top_keys = set(cases_data.keys()) - allowed_top_keys
    if extra_top_keys:
        raise ValueError(
            f"Cases file contains unexpected top-level keys: {sorted(extra_top_keys)}"
        )

    schema_ver = cases_data.get("schema_version")
    if schema_ver != EXPECTED_CASES_SCHEMA_VERSION:
        raise ValueError(
            f"Invalid cases schema_version: expected '{EXPECTED_CASES_SCHEMA_VERSION}', got '{schema_ver}'"
        )

    cases = cases_data.get("cases")
    if not isinstance(cases, list) or len(cases) != len(EXPECTED_CASE_IDS):
        raise ValueError(
            f"Expected exactly {len(EXPECTED_CASE_IDS)} cases, found {len(cases) if isinstance(cases, list) else 'invalid'}"
        )

    allowed_case_keys = {"case_id", "question"}
    for idx, (expected_id, item) in enumerate(zip(EXPECTED_CASE_IDS, cases)):
        if not isinstance(item, dict):
            raise ValueError(f"Case {idx} must be a dictionary.")

        extra_item_keys = set(item.keys()) - allowed_case_keys
        if extra_item_keys:
            raise ValueError(
                f"Case {idx} contains unexpected keys: {sorted(extra_item_keys)}"
            )

        case_id = item.get("case_id")
        if case_id != expected_id:
            raise ValueError(
                f"Case {idx} ID mismatch: expected '{expected_id}', got '{case_id}'"
            )

        question = item.get("question")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"Case '{case_id}' question must be a non-empty string.")

    return cases


def check_point_immutability(before: int, after: int) -> bool:
    """Compare observed before and after point counts for exact match."""
    return before == after


def get_git_info() -> dict:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        status_out = subprocess.check_output(
            ["git", "status", "--porcelain"], text=True
        ).strip()
        return {"commit": commit, "dirty": bool(status_out)}
    except Exception:
        return {"commit": "unknown", "dirty": True}


def make_fits_all_checker():
    from transformers import AutoTokenizer
    from embedding.full_corpus import DENSE_MODEL_SPECS

    tokenizers = [
        (
            AutoTokenizer.from_pretrained(
                spec.model_id, revision=spec.revision, local_files_only=True
            ),
            spec.max_tokens,
        )
        for spec in DENSE_MODEL_SPECS
    ]

    def checker(text: str) -> bool:
        for tok, max_tokens in tokenizers:
            if len(tok.encode(text, truncation=False)) > max_tokens:
                return False
        return True

    return checker


def get_metadata_v2_point_count(settings: dict) -> int:
    client = client_from_settings(settings)
    collection_name = "hue_full_corpus_a_e5_small_384_metadata_v2"
    info = client.get_collection(collection_name)
    return info.points_count


def serialize_call_evidence(evidence: Any) -> dict[str, Any]:
    """Pure production helper to serialize recorded evidence into call record dictionary."""
    if evidence is None:
        return {}
    return {
        "packed_sources_count": getattr(evidence, "packed_sources_count", 0),
        "packed_token_count": getattr(evidence, "packed_token_count", 0),
        "source_ids": [s["id"] for s in getattr(evidence, "sources", [])],
        "sources": getattr(evidence, "sources", []),
        "response_id": getattr(evidence, "response_id", None),
        "finish_reason": getattr(evidence, "finish_reason", None),
        "input_tokens": getattr(evidence, "input_tokens", None),
        "output_tokens": getattr(evidence, "output_tokens", None),
        "total_tokens": getattr(evidence, "total_tokens", None),
        "status": getattr(evidence, "status", None),
        "error": getattr(evidence, "error", None),
    }


def build_live_smoke_artifact(
    git_info: dict[str, Any],
    settings: dict[str, Any] | None,
    before_count: int | None,
    after_count: int | None,
    calls_record: list[dict[str, Any]],
    status: str,
    early_exit_reason: str | None = None,
    checks: dict[str, Any] | None = None,
    unverified: list[str] | None = None,
) -> dict[str, Any]:
    """Pure production helper constructing the complete live smoke artifact dictionary."""
    if unverified is None:
        unverified_list = [
            "cost_accounting_not_provided_by_direct_openai_sdk",
            "custom_reasoning_effort_untested_because_forbidden_by_contract",
            "openrouter_qwen_deferred_to_phase_8",
        ]
    else:
        unverified_list = list(unverified)

    checks_dict = dict(checks) if checks is not None else {}

    if before_count is not None and after_count is not None:
        point_count_intact = check_point_immutability(before_count, after_count)
    else:
        point_count_intact = False
        if "point_count_unverified" not in unverified_list:
            unverified_list.append("point_count_unverified")

    all_calls_pass = len(calls_record) > 0 and all(c.get("status") == "PASS" for c in calls_record)
    exact_five_attempts = len(calls_record) == 5

    checks_dict.setdefault("exact_five_attempts", exact_five_attempts)
    checks_dict.setdefault("point_count_intact", point_count_intact)
    checks_dict.setdefault("all_calls_pass", all_calls_pass)

    config_dict: dict[str, Any] = {
        "collection_contract": "metadata_v2",
    }
    if settings:
        gen_cfg = settings.get("full_corpus_generation", {})
        rt_cfg = settings.get("full_corpus_runtime", {})
        config_dict.update({
            "candidate_id": rt_cfg.get("candidate_id"),
            "retrieval_treatment": rt_cfg.get("retrieval_treatment"),
            "reranker": rt_cfg.get("reranker"),
            "provider": gen_cfg.get("provider"),
            "model": gen_cfg.get("model"),
            "token_encoding": gen_cfg.get("token_encoding"),
            "answer_max_output_tokens": gen_cfg.get("answer_max_output_tokens"),
            "representation_b_max_output_tokens": gen_cfg.get("representation_b_max_output_tokens"),
            "timeout_seconds": gen_cfg.get("timeout_seconds"),
            "context_limit": gen_cfg.get("context_limit"),
            "reserved_output_tokens": gen_cfg.get("reserved_output_tokens"),
            "safety_margin": gen_cfg.get("safety_margin"),
            "max_context_documents": gen_cfg.get("max_context_documents"),
            "max_retries": 0,
            "max_turns": 1,
            "temperature_override": None,
            "reasoning_effort_override": None,
            "top_p_override": None,
        })

    artifact = {
        "schema_version": "phase_6_full_corpus_live_smoke:v2",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git": git_info,
        "configuration": config_dict,
        "qdrant": {"before": before_count, "after": after_count},
        "call_attempt_count": len(calls_record),
        "calls": calls_record,
        "checks": checks_dict,
        "unverified": unverified_list,
        "status": status,
    }
    if early_exit_reason:
        artifact["early_exit_reason"] = early_exit_reason
    return artifact


async def run_smoke_async(cases_path: Path, output_path: Path, confirm_paid: bool) -> int:
    if not confirm_paid:
        print("ERROR: --confirm-paid flag is required to run Phase 6 paid calls.", file=sys.stderr)
        return 1

    git_info = get_git_info()
    before_count: int | None = None
    after_count: int | None = None
    calls_record: list[dict[str, Any]] = []
    checks: dict[str, Any] = {}
    unverified: list[str] = [
        "cost_accounting_not_provided_by_direct_openai_sdk",
        "custom_reasoning_effort_untested_because_forbidden_by_contract",
        "openrouter_qwen_deferred_to_phase_8",
    ]
    settings: dict[str, Any] | None = None

    def write_atomic_artifact(status: str, early_exit_reason: str | None = None) -> None:
        nonlocal after_count
        if after_count is None and settings is not None:
            try:
                after_count = get_metadata_v2_point_count(settings)
            except Exception:
                after_count = None

        artifact = build_live_smoke_artifact(
            git_info=git_info,
            settings=settings,
            before_count=before_count,
            after_count=after_count,
            calls_record=calls_record,
            status=status,
            early_exit_reason=early_exit_reason,
            checks=checks,
            unverified=unverified,
        )

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_output = output_path.with_suffix(".tmp")
            with temp_output.open("w", encoding="utf-8") as f:
                json.dump(artifact, f, ensure_ascii=False, indent=2)
            temp_output.replace(output_path)
            print(f"Atomic evidence written to {output_path}")
        except Exception as write_err:
            logger.error("Failed to write atomic artifact: %s", type(write_err).__name__)


    # Guard 1: Cases file existence
    if not cases_path.is_file():
        print(f"ERROR: Cases file does not exist: {cases_path}", file=sys.stderr)
        write_atomic_artifact("FAIL", early_exit_reason="cases_file_missing")
        return 1

    # Guard 2: Cases file JSON parsing
    try:
        with cases_path.open(encoding="utf-8") as f:
            cases_data = json.load(f)
    except Exception as json_err:
        print(f"ERROR: Failed to parse cases JSON: {type(json_err).__name__}", file=sys.stderr)
        write_atomic_artifact("FAIL", early_exit_reason="cases_json_invalid")
        return 1

    # Guard 3: Cases schema validation
    try:
        cases = validate_cases_data(cases_data)
    except Exception as val_err:
        print(f"ERROR: Cases validation failed: {type(val_err).__name__}", file=sys.stderr)
        write_atomic_artifact("FAIL", early_exit_reason="cases_schema_invalid")
        return 1

    # Guard 4: Settings loading
    try:
        settings = load_settings(validate_private_paths=False)
    except Exception as set_err:
        print(f"ERROR: Failed to load settings: {type(set_err).__name__}", file=sys.stderr)
        write_atomic_artifact("FAIL", early_exit_reason="settings_load_failed")
        return 1

    # Guard 5: Before point count
    try:
        before_count = get_metadata_v2_point_count(settings)
        print(f"Qdrant points before: {before_count}")
    except Exception as q_err:
        logger.error("Failed to read before point count: %s", type(q_err).__name__)
        before_count = None
        write_atomic_artifact("FAIL", early_exit_reason="before_count_failed")
        return 1

    try:
        app = create_app(settings)
        checker = make_fits_all_checker()

        async with app.router.lifespan_context(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Check components readiness
                health_resp = await client.get("/health")
                if health_resp.status_code != 200 or health_resp.json().get("status") != "ok":
                    print(f"ERROR: API health is not ready: {health_resp.status_code}", file=sys.stderr)
                    write_atomic_artifact("FAIL", early_exit_reason="api_health_not_ready")
                    return 1

                generator = app.state.generator
                retrieval_service = app.state.retrieval_service

                # -------------------------------------------------------------
                # Attempt 1: Representation B generation with real retrieval
                # -------------------------------------------------------------
                print("\n--- Executing Attempt 1: Representation B ---")
                rep_b_retrieval = retrieval_service.search(cases[0]["question"])
                if not rep_b_retrieval.documents:
                    write_atomic_artifact("FAIL", early_exit_reason="no_documents_retrieved_for_rep_b")
                    return 1
                rep_b_sample_text = rep_b_retrieval.documents[0].text

                rep_b_call = {
                    "call_number": 1,
                    "call_type": "representation_b",
                    "case_id": "representation_b",
                    "model": generator.model,
                    "status": "FAIL",
                }
                try:
                    gen_b = await generator.generate_search_context(rep_b_sample_text)
                    rep_b_result = build_representation_b_search_text(
                        rep_b_sample_text,
                        gen_b.text,
                        fits_all_embedding_tokenizers=checker,
                    )
                    rep_b_call.update({
                        "status": "PASS" if rep_b_result.search_text else "FAIL",
                        "response_id": gen_b.response_id,
                        "latency_ms": gen_b.latency_ms,
                        "input_tokens": gen_b.input_tokens,
                        "output_tokens": gen_b.output_tokens,
                        "total_tokens": gen_b.total_tokens,
                        "finish_reason": gen_b.finish_reason,
                        "used_representation_b": rep_b_result.used_representation_b,
                        "reason": rep_b_result.reason,
                        "generated_search_context": gen_b.text,
                    })
                    print(f"Attempt 1 PASS: latency={gen_b.latency_ms}ms, tokens={gen_b.total_tokens}")
                except Exception as exc:
                    logger.error("Attempt 1 failed: %s", type(exc).__name__)
                    rep_b_call["error_type"] = type(exc).__name__
                    print(f"Attempt 1 FAIL: {type(exc).__name__}")

                calls_record.append(rep_b_call)

                # -------------------------------------------------------------
                # Attempts 2-5: Four Answer Cases
                # -------------------------------------------------------------
                for idx, case_item in enumerate(cases, start=2):
                    case_id = case_item["case_id"]
                    question = case_item["question"]
                    print(f"\n--- Executing Attempt {idx}: {case_id} ---")
                    ans_call = {
                        "call_number": idx,
                        "call_type": "answer",
                        "case_id": case_id,
                        "question": question,
                        "model": generator.model,
                        "status": "FAIL",
                    }
                    try:
                        t0 = time.monotonic()
                        # Request-scoped evidence recording without touching shared app.state
                        with record_evidence(request_id=case_id) as recorder:
                            resp = await client.post("/api/chat", json={"query": question})
                            evidence = recorder.get_evidence()

                        latency_ms = round((time.monotonic() - t0) * 1000)
                        ans_call["status_code"] = resp.status_code
                        ans_call["latency_ms"] = latency_ms

                        ev_dict = serialize_call_evidence(evidence)
                        if ev_dict:
                            ans_call["response_id"] = ev_dict.get("response_id")
                            ans_call["finish_reason"] = ev_dict.get("finish_reason")
                            ans_call["input_tokens"] = ev_dict.get("input_tokens")
                            ans_call["output_tokens"] = ev_dict.get("output_tokens")
                            ans_call["total_tokens"] = ev_dict.get("total_tokens")
                            ans_call["packed_evidence"] = {
                                "packed_sources_count": ev_dict.get("packed_sources_count", 0),
                                "packed_token_count": ev_dict.get("packed_token_count", 0),
                                "source_ids": ev_dict.get("source_ids", []),
                                "sources": ev_dict.get("sources", []),
                            }
                            if ev_dict.get("error"):
                                ans_call["evidence_error"] = ev_dict["error"]

                        if resp.status_code == 200:
                            payload = resp.json()
                            ans_text = payload.get("answer", "")
                            sources = payload.get("sources", [])
                            ans_call["answer"] = ans_text
                            ans_call["sources"] = sources

                            if case_id == "out_of_scope":
                                if ans_text == INSUFFICIENT_ANSWER and len(sources) == 0:
                                    ans_call["status"] = "PASS"
                                    print("Attempt 5 PASS (Exact out-of-scope fallback, zero sources)")
                                else:
                                    ans_call["status"] = "FAIL"
                                    print(f"Attempt 5 FAIL: answer={ans_text!r}, sources_count={len(sources)}")
                            else:
                                citations = [int(m) for m in CITATION_RE.findall(ans_text)]
                                source_ids = [s["id"] for s in sources]
                                all_cited_exist = bool(citations) and all(cid in source_ids for cid in citations)
                                all_excerpts_non_empty = bool(sources) and all(
                                    all(bool(exc.strip()) for exc in s.get("excerpts", []))
                                    for s in sources
                                )
                                if ans_text and ans_text != INSUFFICIENT_ANSWER and all_cited_exist and all_excerpts_non_empty:
                                    ans_call["status"] = "PASS"
                                    print(f"Attempt {idx} PASS: citations={citations}, sources={source_ids}")
                                else:
                                    ans_call["status"] = "FAIL"
                                    print(f"Attempt {idx} FAIL: citations={citations}, sources={source_ids}")
                        else:
                            ans_call["error_status"] = resp.status_code
                            print(f"Attempt {idx} FAIL: HTTP {resp.status_code}")
                    except Exception as exc:
                        logger.error("Attempt %d failed: %s", idx, type(exc).__name__)
                        ans_call["error_type"] = type(exc).__name__
                        print(f"Attempt {idx} FAIL: {type(exc).__name__}")

                    calls_record.append(ans_call)
    except Exception as exc:
        logger.error("Runner execution aborted due to unexpected error: %s", type(exc).__name__)
        write_atomic_artifact("FAIL", early_exit_reason=f"unexpected_runner_error_{type(exc).__name__}")
        print(f"ERROR: Runner aborted unexpectedly: {type(exc).__name__}", file=sys.stderr)
        return 1

    try:
        after_count = get_metadata_v2_point_count(settings)
        print(f"\nQdrant points after: {after_count}")
    except Exception as q_err:
        logger.error("Failed to read after point count: %s", type(q_err).__name__)
        after_count = None

    # Compute overall checks
    all_calls_pass = len(calls_record) > 0 and all(c.get("status") == "PASS" for c in calls_record)
    exact_five_attempts = len(calls_record) == 5
    if before_count is not None and after_count is not None:
        point_count_intact = check_point_immutability(before_count, after_count)
    else:
        point_count_intact = False
        if "point_count_unverified" not in unverified:
            unverified.append("point_count_unverified")

    checks["exact_five_attempts"] = exact_five_attempts
    checks["point_count_intact"] = point_count_intact
    checks["all_calls_pass"] = all_calls_pass

    overall_status = "PASS" if (all_calls_pass and exact_five_attempts and point_count_intact) else "FAIL"
    print(f"\nFinal Smoke Verification Status: {overall_status}")

    write_atomic_artifact(overall_status)
    return 0 if overall_status == "PASS" else 1


def main():
    parser = argparse.ArgumentParser(description="Full-corpus Phase 6 live smoke runner.")
    parser.add_argument("--cases", type=Path, required=True, help="Path to cases JSON")
    parser.add_argument("--output", type=Path, required=True, help="Path to output JSON")
    parser.add_argument("--confirm-paid", action="store_true", help="Explicit confirmation for bounded paid calls")
    args = parser.parse_args()

    exit_code = asyncio.run(run_smoke_async(args.cases, args.output, args.confirm_paid))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
