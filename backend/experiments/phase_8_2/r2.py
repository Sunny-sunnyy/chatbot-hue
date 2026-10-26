"""Phase 8.2 §10 R2 — trả lời phần có căn cứ (chữ E1b) thay vì từ chối cả câu, trên mốc context 10.

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r2_plan.md` (A duyệt sha trước khi chạy lệnh có phí).
Đổi đúng một thứ: câu luật từ chối trong `ANSWER_SYSTEM_INSTRUCTIONS` → chữ E1b (thay như P1 8.1, có `assert`). Mọi khâu khác là code
production qua `full_corpus_eval.answer_case` (retrieval, context 10 theo `settings.yaml` ở `811d25d`, generator, validator).
Mốc: câu trả lời B1 `data/phase_8_2/b1/b1_{dev,test}.jsonl`, chấm lại cùng lượt mù. Paid: chỉ `gpt-6-luna` (lệnh `run`). Tốc độ khâu sinh đo bằng `output_tokens` / câu (spec §10.2 "Đo tốc độ theo khâu").
Kết quả: JSONL private `data/phase_8_2/r2/`.

Chạy từ `backend/` (thứ tự plan §3; mỗi lệnh có phí từ chối ghi đè):
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.r2 run --cases oos_dev --name r2_oos_dev
"""
import argparse
import asyncio
import hashlib
import json
import random
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import (
    ANSWER_METRICS,
    BOOTSTRAP_ROUNDS,
    BOOTSTRAP_SEED,
    CONCURRENCY,
    GOLDEN_FULL,
    OUT_OF_SCOPE,
    REPO_ROOT,
    answer_case,
    build_context_builder,
    bootstrap_mean_diff,
    build_retrieval,
    cost_usd,
    holm_adjust,
    load_golden_cases,
    paired_stats,
    validate_score_rows,
)
from experiments.phase_8_1.g1_retrieval import keep_realism
from experiments.phase_8_1.g2_generate import _REFUSAL_RULE, citation_error, read_scores, usage, write_batches
from experiments.phase_8_2.b1 import read_jsonl, write_jsonl
from llm.full_corpus_prompt import ANSWER_SYSTEM_INSTRUCTIONS, INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator

OUT_DIR = REPO_ROOT / "data/phase_8_2/r2"
B1_DIR = REPO_ROOT / "data/phase_8_2/b1"
SPLIT_PATH = REPO_ROOT / "knowledge-base-hue/evaluation/phase_8_1/split.json"
SEED = 20261024

# Chữ E1b — nguyên văn plan E1 §3 / plan R2 §1, ghi trước 25/10; đổi chữ = biến thể mới (plan mới).
E1B_RULE = (
    "Nếu bằng chứng trả lời trực tiếp được một phần câu hỏi, trả lời phần đó kèm citation, rồi nói rõ phần nào nguồn dữ liệu không "
    "có thông tin bằng một câu riêng không citation. Thông tin chỉ cùng chủ đề mà không trả lời điều được hỏi thì không tính là trả "
    "lời được. Nếu không trả lời trực tiếp được ý nào của câu hỏi, trả đúng duy nhất câu sau, không thêm citation và không viết câu "
    f"báo thiếu nào khác:\n{INSUFFICIENT_ANSWER}"
)
E1B_INSTRUCTIONS = ANSWER_SYSTEM_INSTRUCTIONS.replace(_REFUSAL_RULE, E1B_RULE)
assert E1B_INSTRUCTIONS != ANSWER_SYSTEM_INSTRUCTIONS

# Plan R2 §3 bước 2: 5 câu nhóm P (context có một phần fact, C36) + 120 / 168 (sàn: context không có fact ⇒ phải vẫn từ chối).
EARLY = (48, 67, 68, 113, 120, 167, 168)
MUST_REFUSE = (120, 168)
RUNS = {"r2": [OUT_DIR / "r2_dev.jsonl", OUT_DIR / "r2_test.jsonl"], "b1": [B1_DIR / "b1_dev.jsonl", B1_DIR / "b1_test.jsonl"]}


# ---------- Tập câu ----------

def cases_for(name: str) -> list[dict]:
    """oos_dev (bước 1) / early (bước 2) / dev_rest (bước 3) / test_pilot, test_rest."""
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    cases = {c["case_index"]: c for c in load_golden_cases("full")}
    dev, test = [cases[i] for i in split["dev"]], [cases[i] for i in split["test"]]
    oos = [c for c in dev if c["category"] == OUT_OF_SCOPE]
    if name == "oos_dev":
        return oos
    if name == "early":
        return [cases[i] for i in EARLY]
    if name == "dev_rest":
        skip = {c["case_index"] for c in oos} | set(EARLY)
        return [c for c in dev if c["case_index"] not in skip]
    if name in ("test_pilot", "test_rest"):
        pilot = set(random.Random(SEED).sample(sorted(c["case_index"] for c in test), 10))
        return [c for c in test if (c["case_index"] in pilot) == (name == "test_pilot")]
    raise ValueError(name)


# ---------- Sinh (paid) ----------

async def generate(cases: list[dict], instructions: str) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    context_builder = build_context_builder(settings)
    generator = OpenAIFullCorpusGenerator.from_environment(settings, answer_instructions=instructions)
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async def one(case: dict) -> dict:
        async with semaphore:
            return await answer_case(case, service, context_builder, generator)

    try:
        rows = list(await asyncio.gather(*(one(case) for case in cases)))
    finally:
        service.close()
        await generator.aclose()
    for row in rows:
        row["usd"] = cost_usd(row["input_tokens"] or 0, row["output_tokens"] or 0)
    return rows


# ---------- Kiểm tất định + sàn (free) ----------

def run_rows(run: str) -> dict[int, dict]:
    return {r["case_index"]: r for path in RUNS[run] if path.exists() for r in read_jsonl(path)}


def check() -> dict:
    """Bước 3 plan: chỉ prompt đổi ⇒ `top_chunk_ids`, `context_sources` = B1. Sàn: OOS, 120 / 168, câu không citation (API 500), lỗi."""
    r2, b1 = run_rows("r2"), run_rows("b1")
    same = {f: sorted(i for i in r2 if r2[i][f] != b1[i][f]) for f in ("top_chunk_ids", "context_sources")}
    return {
        "cases": len(r2), "differ_from_b1": same,
        "oos_answered": sorted(i for i in r2 if r2[i]["category"] == OUT_OF_SCOPE and not r2[i]["refusal"]),
        "must_refuse_answered": sorted(i for i in MUST_REFUSE if i in r2 and not r2[i]["refusal"]),
        "uncited_non_refusal": sorted(i for i in r2 if r2[i]["citation_error"] == "Grounded answer has no citation"),
        "errors": sorted(i for i in r2 if r2[i]["error"]),
        "citation_v2": {run: sorted(i for i, r in rows.items() if not r["error"]
                                    and citation_error(r["answer"], r["context_sources"], single_source_policy=False))
                        for run, rows in (("r2", r2), ("b1", b1))},
        "usage": {"r2": usage(list(r2.values())), "b1": usage([b1[i] for i in r2])},
    }


# ---------- Judge Claude: xuất lô mù / ghép điểm ----------

def group_ids(group: str) -> set[int]:
    return set(json.loads(SPLIT_PATH.read_text(encoding="utf-8"))[group])


def pooled_items(group: str) -> tuple[list[dict], dict]:
    """Như `b1.pooled_items` cho hai lượt R2 + B1 của một nhóm (plan §3: dev chấm trước, test chỉ khi dev đạt): câu trả lời giống hệt
    chữ trong cùng câu chấm một lần; item là số mờ."""
    by_case = {c["case_index"]: c for c in load_golden_cases("full")}
    wanted = group_ids(group)
    unique: dict[tuple[int, str], list] = defaultdict(list)
    for run in RUNS:
        for row in run_rows(run).values():
            if row["error"] is None and row["case_index"] in wanted:
                unique[(row["case_index"], row["answer"])].append((run, row["case_index"]))
    keys = sorted(unique)
    random.Random(SEED).shuffle(keys)
    items, mapping = [], {}
    for item, key in enumerate(keys, 1):
        case = by_case[key[0]]
        items.append({"case_index": item, "question": case["question"], "reference_answer": case["reference_answer"], "answer": key[1]})
        mapping[item] = unique[key]
    return items, mapping


def scored_rows(judge_dir: Path) -> dict[str, dict[int, dict]]:
    mapping = json.loads((judge_dir / "map.json").read_text(encoding="utf-8"))["items"]
    scores = {r["case_index"]: r for r in read_scores(judge_dir, "scores")}
    types = {r["case_index"]: r["answer_type"] for r in read_scores(judge_dir, "types")}
    out = {run: run_rows(run) for run in RUNS}
    for item, pairs in mapping.items():  # chỉ câu của nhóm đã chấm mới có điểm
        for run, case in pairs:
            out[run][case].update({m: scores[int(item)][m] for m in ANSWER_METRICS}, answer_type=types.get(int(item)))
    return out


def analyze(group: str) -> dict:
    """Chênh theo cặp R2 − B1 trên nhóm chính (plan R2 §2): chỉ số quyết `false_refusal` (dev), số câu tụt, Holm họ {R2, R3} cố định."""
    runs = scored_rows(OUT_DIR / f"judge_{group}")
    r2, b1 = runs["r2"], runs["b1"]
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    ids = [i for i in split[group] if i in r2]
    main = sorted(r["case_index"] for r in keep_realism([b1[i] for i in ids], "main") if r["category"] != OUT_OF_SCOPE)
    out = {"group": group, "n_main": len(main)}
    out["false_refusal"] = paired_stats([float(b1[i]["refusal"]) for i in main], [float(r2[i]["refusal"]) for i in main],
                                        "false_refusal")
    # Họ Holm {R2, R3} cố định (plan R2 §2): R3 chưa có p ⇒ hiệu chỉnh như họ 2 với p R3 = 1.
    out["false_refusal"]["p_holm_family2"] = holm_adjust([out["false_refusal"]["p_value"], 1.0])[0]
    for metric in ANSWER_METRICS:
        out[metric] = paired_stats([b1[i][metric] for i in main], [r2[i][metric] for i in main], metric)
        out[f"{metric}_losses"] = sum(r2[i][metric] < b1[i][metric] for i in main)
    out["answer_type"] = {arm: {t: sum(rows[i]["answer_type"] == t for i in main) for t in ("full", "partial", "refusal")}
                          for arm, rows in (("r2", r2), ("b1", b1))}
    # Tốc độ khâu sinh (plan R2 §2): output_tokens / câu là mức tụt (≤ +20 %); latency_ms chỉ theo dõi (B1 đo ở phiên khác).
    called = sorted(i for i in split[group] if i in r2 and r2[i]["output_tokens"] is not None and b1[i]["output_tokens"] is not None)
    latency_diff = np.array([r2[i]["latency_ms"] - b1[i]["latency_ms"] for i in called], dtype=float)
    out["speed"] = {
        "n": len(called),
        "output_tokens_ratio": sum(r2[i]["output_tokens"] for i in called) / sum(b1[i]["output_tokens"] for i in called),
        "latency_p50_p95": {arm: [float(np.percentile([rows[i]["latency_ms"] for i in called], q)) for q in (50, 95)]
                            for arm, rows in (("r2", r2), ("b1", b1))},
        "latency_mean_diff_ms": float(latency_diff.mean()),
        **bootstrap_mean_diff(latency_diff, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED),
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.r2")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="sinh câu trả lời R2 (paid)")
    run.add_argument("--cases", required=True, choices=["oos_dev", "early", "dev_rest", "test_pilot", "test_rest"])
    run.add_argument("--name", required=True)
    merge = commands.add_parser("merge", help="gộp các phần thành r2_dev / r2_test")
    merge.add_argument("--parts", required=True, nargs="+")
    merge.add_argument("--name", required=True, choices=["r2_dev", "r2_test"])
    commands.add_parser("check", help="tất định so B1 + sàn + citation v2 (free)")
    export = commands.add_parser("export-judge", help="lô chấm mù R2 + B1 của một nhóm")
    export.add_argument("--group", required=True, choices=["dev", "test"])
    export.add_argument("--batch-size", type=int, default=25)
    check_judge = commands.add_parser("check-judge", help="đủ điểm + answer_type, đúng schema")
    check_judge.add_argument("--group", required=True, choices=["dev", "test"])
    ana = commands.add_parser("analyze", help="chênh theo cặp R2 − B1 (free)")
    ana.add_argument("--group", required=True, choices=["dev", "test"])
    args = parser.parse_args()

    judge_dir = OUT_DIR / f"judge_{args.group}" if hasattr(args, "group") else None
    if args.command == "run":
        out = OUT_DIR / f"{args.name}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists")
        started = time.strftime("%Y-%m-%d %H:%M:%S %z")
        rows = asyncio.run(generate(cases_for(args.cases), E1B_INSTRUCTIONS))
        spent = usage(rows)
        write_jsonl(out, rows)
        meta = {"name": args.name, "cases": args.cases, "started": started,
                "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"), "usage": spent,
                "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest(),
                "instructions_sha12": hashlib.sha256(E1B_INSTRUCTIONS.encode()).hexdigest()[:12]}
        (OUT_DIR / f"{args.name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(out, json.dumps(spent))
    elif args.command == "merge":
        out = OUT_DIR / f"{args.name}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists")
        rows = [r for part in args.parts for r in read_jsonl(OUT_DIR / f"{part}.jsonl")]
        if len({r["case_index"] for r in rows}) != len(rows):
            raise SystemExit("duplicated case_index across parts")
        print(write_jsonl(out, sorted(rows, key=lambda r: r["case_index"])), json.dumps(usage(rows)))
    elif args.command == "check":
        print(json.dumps(check(), ensure_ascii=False, indent=2))
    elif args.command == "export-judge":
        if judge_dir.exists():
            raise SystemExit(f"{judge_dir} exists")
        items, mapping = pooled_items(args.group)
        write_batches(judge_dir, items, args.batch_size)
        (judge_dir / "map.json").write_text(json.dumps({"runs": list(RUNS), "items": mapping}, indent=1) + "\n")
        print(json.dumps({"items": len(items), "answers": sum(len(v) for v in mapping.values()),
                          "batches": -(-len(items) // args.batch_size)}))
    elif args.command == "check-judge":
        items = {json.loads(l)["case_index"] for p in judge_dir.glob("batch_*.jsonl") for l in p.read_text().splitlines()}
        scores, types = read_scores(judge_dir, "scores"), read_scores(judge_dir, "types")
        print(json.dumps({"items": len(items), "score_errors": validate_score_rows(scores),
                          "scores_missing": sorted(items - {r["case_index"] for r in scores}),
                          "types_missing": sorted(items - {r["case_index"] for r in types}),
                          "types_bad": [r for r in types if r.get("answer_type") not in ("full", "partial", "refusal")]}))
    else:
        print(json.dumps(analyze(args.group), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
