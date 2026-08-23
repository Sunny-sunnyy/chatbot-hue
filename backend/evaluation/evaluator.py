"""Phase 7 evaluation CLI facade (thin).

Parses arguments, runs preflight estimation and dispatches to the focused
modules (retrieval_eval.run_retrieval, answer_eval.run_calibration and
run_answer_pipeline). No orchestration logic lives here; nothing here mutates
config, the active collection or the benchmark ledger.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

from core.settings_loader import load_settings
from evaluation import answer_eval, artifacts
from evaluation.test_loader import load_dataset
from evaluation.retrieval_eval import compute_corpus_checksum, config_fingerprint, run_retrieval
from evaluation.answer_eval import (
    BUDGET_SCHEMA_VERSION,
    BudgetIntegrityError,
    CallBudget,
    CalibrationPackageError,
    compute_pricing_checksum,
    cost_estimate_usd,
    generation_reserve_tokens,
    judge_reserve_tokens,
    run_answer_pipeline,
    run_calibration,
)
from vectorstore.qdrant import get_client

VALID_PROFILES = ("dense_only", "hybrid_no_rerank", "hybrid_rerank")
RESULTS_DIR = Path(__file__).resolve().parent / "results"
BACKEND_DIR = Path(__file__).resolve().parents[1]
BASE_CASE_COUNT = 104
DEFAULT_MAX_CALLS = 64
DEFAULT_MAX_COST_USD = 0.50


def _kb_root(settings):
    root = Path(settings["knowledge_base"]["root_dir"])
    return (root if root.is_absolute() else BACKEND_DIR / root).resolve()


def _load_cases():
    settings = load_settings()
    dataset = load_dataset(
        (BACKEND_DIR / settings["evaluation"]["test_file"]).resolve(),
        kb_root=_kb_root(settings),
        expected_count=BASE_CASE_COUNT,
    )
    return settings, dataset


def _load_answer_subset(settings, dataset):
    """Load the fixed 24-case manifest and validate 3 cases per category."""
    manifest_path = _kb_root(settings) / "foods/evaluation/answer_subset_v1.json"
    if not manifest_path.exists():
        raise SystemExit(f"answer subset manifest missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_id = {case.case_id: case for case in dataset.cases}
    chosen = []
    for entry in manifest["cases"]:
        case_id = entry["case_id"] if isinstance(entry, dict) else entry
        if case_id not in by_id:
            raise SystemExit(f"manifest case {case_id} not in dataset")
        chosen.append(by_id[case_id])
    if len(chosen) != 24:
        raise SystemExit(f"manifest must have 24 cases, got {len(chosen)}")
    per_category = {}
    for case in chosen:
        per_category.setdefault(case.category, []).append(case)
    for category in (
        "direct_fact", "temporal", "comparative", "relationship",
        "spanning", "holistic", "food_knowledge", "guide_planning",
    ):
        if len(per_category.get(category, [])) != 3:
            raise SystemExit(f"manifest category {category} must have 3 cases")
    return chosen


def _estimate_run_cost(subset, settings):
    """Preflight estimate; same token bounds as the runtime budget reserves."""
    answer_model = settings["llm"]["answer_model"]
    judge_model = settings["evaluation"]["judge_model"]
    gen_input, gen_output = generation_reserve_tokens(settings)
    judge_input, judge_output = judge_reserve_tokens()
    total = 0.0
    total += cost_estimate_usd(judge_model, judge_input, judge_output) * 8  # calibration
    for _ in subset:  # generation + judge
        total += cost_estimate_usd(answer_model, gen_input, gen_output)
        total += cost_estimate_usd(judge_model, judge_input, judge_output)
    return total


def require_retrieval_profile(args):
    """No implicit profile: retrieval must name one or ask for all."""
    if not (getattr(args, "profile", None) or getattr(args, "profiles", None)):
        raise SystemExit("retrieval requires --profile <name> or --profiles all")


def cmd_retrieval(args):
    require_retrieval_profile(args)
    profiles = list(VALID_PROFILES) if getattr(args, "profiles", None) else [args.profile]
    settings, dataset = _load_cases()
    run_retrieval(
        settings, dataset, profiles,
        results_dir=RESULTS_DIR, quiet=getattr(args, "quiet", False),
        resume=getattr(args, "resume", None),
        max_cases=getattr(args, "max_cases", None),
    )


def cmd_answers(args):
    settings, dataset = _load_cases()
    subset = _load_answer_subset(settings, dataset)
    estimate = _estimate_run_cost(subset, settings)
    print(
        f"[answers] preflight: {len(subset)} cases, estimated provider cost "
        f"~${estimate:.5f} (estimate; re-verify prices before paid runs)"
    )

    # Consent gate: mandatory for both fresh and resume runs before any live/budget/Qdrant operations
    if not getattr(args, "confirm_paid", False):
        print("[answers] --confirm-paid missing: no provider call made")
        return

    resume_id = getattr(args, "resume", None)
    cal_arg = getattr(args, "calibration", None)
    ans_profile = getattr(args, "answer_profile", None) or "dense_only"

    # Reject fresh calibration reuse: fresh runs must execute new calibration
    if not resume_id and cal_arg:
        raise SystemExit(
            "[answers] fresh run does not support --calibration reuse; "
            "fresh runs must execute a new calibration package"
        )

    client = get_client(settings["vector_database"]["url"], settings["vector_database"]["timeout"])
    corpus_checksum = compute_corpus_checksum(settings, client)
    cfg_fingerprint = config_fingerprint(settings, ans_profile)
    samples_path = _kb_root(settings) / "foods/evaluation/judge_calibration_v1.jsonl"
    manifest_path = _kb_root(settings) / "foods/evaluation/answer_subset_v1.json"

    if resume_id:
        gen_run_id = resume_id
        if not gen_run_id.startswith("generation-"):
            raise SystemExit("answer resume run id must start with generation-")
        budget_path = RESULTS_DIR / "budgets" / f"{gen_run_id}.json"
        if not budget_path.exists():
            raise SystemExit(f"cannot resume {gen_run_id}: no durable budget state found at {budget_path}")

        expected_identity = {
            "dataset_checksum": dataset.dataset_checksum,
            "config_checksum": cfg_fingerprint,
            "corpus_checksum": corpus_checksum,
            "collection_name": settings["vector_database"]["collection_name"],
            "answer_profile": ans_profile,
            "answer_model": settings["llm"]["answer_model"],
            "judge_model": settings["evaluation"]["judge_model"],
            "generation_prompt_hash": answer_eval.GENERATION_PROMPT_HASH,
            "rubric_version": answer_eval.RUBRIC_VERSION,
            "rubric_prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        }
        try:
            budget = CallBudget.load(
                budget_path,
                expected_identity=expected_identity,
                max_calls=getattr(args, "max_calls", None),
                max_cost_usd=getattr(args, "max_cost_usd", None),
            )
        except BudgetIntegrityError as exc:
            raise SystemExit(f"cannot resume {gen_run_id}: budget integrity error: {exc}") from exc

        cal_run_id = budget.identity.get("calibration_run_id")
        if not cal_run_id:
            raise SystemExit(f"cannot resume {gen_run_id}: budget state missing calibration_run_id")

        if cal_arg:
            if Path(cal_arg).stem != cal_run_id and cal_arg != cal_run_id:
                raise SystemExit(
                    f"calibration mismatch: requested --calibration {cal_arg} does not match "
                    f"linked budget calibration_run_id {cal_run_id}"
                )

        cal_final_path = RESULTS_DIR / "judges" / f"{cal_run_id}.jsonl"
        try:
            calibration = run_calibration(
                settings, dataset, budget,
                samples_path=samples_path,
                manifest_path=manifest_path,
                results_dir=RESULTS_DIR,
                reuse_path=cal_final_path if cal_final_path.exists() else None,
                print_fn=print,
                judge_model=settings["evaluation"]["judge_model"],
                config_checksum=cfg_fingerprint,
                calibration_run_id=cal_run_id,
                resume=True,
            )
        except (CalibrationPackageError, ValueError) as exc:
            raise SystemExit(f"[calibration] package rejected: {exc}") from exc
        if calibration["gate_passed"] is not True:
            raise SystemExit("[answers] calibration gate FAILED; subset generation/judge aborted")

        judge_run_id = "judge-" + gen_run_id[len("generation-"):]
        run_answer_pipeline(
            settings, dataset, subset, budget,
            answer_profile=ans_profile,
            results_dir=RESULTS_DIR,
            calibration_run_id=cal_run_id,
            resume=gen_run_id,
            quiet=getattr(args, "quiet", False),
        )
        return

    # Fresh run
    tz = datetime.now(timezone(timedelta(hours=7)))
    ts_run = tz.strftime("%Y%m%d-%H%M%S")
    gen_run_id = artifacts.make_run_id("generation", ans_profile, dataset.dataset_checksum, ts_run)
    judge_run_id = artifacts.make_run_id("judge", ans_profile, dataset.dataset_checksum, ts_run)
    calibration_run_id = artifacts.make_run_id("calibration", "judge", dataset.dataset_checksum, ts_run)

    identity = {
        "dataset_checksum": dataset.dataset_checksum,
        "config_checksum": cfg_fingerprint,
        "corpus_checksum": corpus_checksum,
        "collection_name": settings["vector_database"]["collection_name"],
        "answer_profile": ans_profile,
        "answer_model": settings["llm"]["answer_model"],
        "judge_model": settings["evaluation"]["judge_model"],
        "generation_prompt_hash": answer_eval.GENERATION_PROMPT_HASH,
        "rubric_version": answer_eval.RUBRIC_VERSION,
        "rubric_prompt_hash": answer_eval.RUBRIC_PROMPT_HASH,
        "calibration_run_id": calibration_run_id,
        "pricing_checksum": compute_pricing_checksum(),
    }
    budget_path = RESULTS_DIR / "budgets" / f"{gen_run_id}.json"
    max_calls = getattr(args, "max_calls", None) if getattr(args, "max_calls", None) is not None else DEFAULT_MAX_CALLS
    max_cost_usd = getattr(args, "max_cost_usd", None) if getattr(args, "max_cost_usd", None) is not None else DEFAULT_MAX_COST_USD
    budget = CallBudget.create(budget_path, identity, max_calls=max_calls, max_cost_usd=max_cost_usd)

    try:
        calibration = run_calibration(
            settings, dataset, budget,
            samples_path=samples_path,
            manifest_path=manifest_path,
            results_dir=RESULTS_DIR,
            reuse_path=None,
            print_fn=print,
            judge_model=settings["evaluation"]["judge_model"],
            config_checksum=cfg_fingerprint,
            calibration_run_id=calibration_run_id,
        )
    except (CalibrationPackageError, ValueError) as exc:
        raise SystemExit(f"[calibration] package rejected: {exc}") from exc
    if calibration["gate_passed"] is not True:
        raise SystemExit(
            "[answers] calibration gate FAILED; subset generation/judge aborted"
        )
    run_answer_pipeline(
        settings, dataset, subset, budget,
        answer_profile=ans_profile,
        results_dir=RESULTS_DIR,
        calibration_run_id=calibration["run_id"],
        resume=None,
        quiet=getattr(args, "quiet", False),
    )


def cmd_all(args):
    settings, dataset = _load_cases()
    profiles = list(VALID_PROFILES) if getattr(args, "profiles", None) else ["dense_only"]
    run_retrieval(settings, dataset, profiles, results_dir=RESULTS_DIR,
                  quiet=getattr(args, "quiet", False),
                  max_cases=getattr(args, "max_cases", None))
    cmd_answers(args)


def build_parser():
    """Argument parser factory; exposed for deterministic CLI tests."""
    parser = argparse.ArgumentParser(prog="evaluation.evaluator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_retrieval = sub.add_parser("retrieval")
    p_retrieval.add_argument("--profile", choices=VALID_PROFILES)
    p_retrieval.add_argument("--profiles", choices=["all"])
    p_retrieval.add_argument("--resume")
    p_retrieval.add_argument("--max-cases", type=int,
                             help="clip the case list for fast diagnostic subsets; "
                                  "subset runs are partial and never comparison evidence")
    p_retrieval.add_argument("--quiet", action="store_true")

    p_answers = sub.add_parser("answers")
    p_answers.add_argument("--answer-profile", choices=VALID_PROFILES, required=True)
    p_answers.add_argument("--confirm-paid", action="store_true")
    p_answers.add_argument("--max-calls", type=int)
    p_answers.add_argument("--max-cost-usd", type=float)
    p_answers.add_argument("--resume")
    p_answers.add_argument("--calibration", default=None)
    p_answers.add_argument("--quiet", action="store_true")

    p_all = sub.add_parser("all")
    p_all.add_argument("--profiles", choices=["all"])
    p_all.add_argument("--answer-profile", choices=VALID_PROFILES, required=True)
    p_all.add_argument("--confirm-paid", action="store_true")
    p_all.add_argument("--max-calls", type=int)
    p_all.add_argument("--max-cost-usd", type=float)
    p_all.add_argument("--max-cases", type=int,
                       help="clip the retrieval case list for fast diagnostic subsets")
    p_all.add_argument("--quiet", action="store_true")
    p_all.set_defaults(resume=None, calibration=None)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "retrieval":
        cmd_retrieval(args)
    elif args.command == "answers":
        cmd_answers(args)
    else:
        cmd_all(args)


if __name__ == "__main__":
    main()
