"""Phase 8.2 §10 R1 — mức suy luận `none` cho lượt sinh (runtime không gửi ⇒ `medium`), trên mốc context 10.

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_r1_plan.md` (A duyệt sha trước khi chạy lệnh có phí).
Đổi đúng một thứ: `OpenAIFullCorpusGenerator.from_environment(settings, reasoning_effort="none")`. Mọi khâu khác là code production qua
`full_corpus_eval.answer_case` (retrieval, context 10 theo `settings.yaml` ở `811d25d`, prompt, validator). Khung theo `r2.py` (`origin/p82-r2`).
Mốc: câu trả lời B1 `data/phase_8_2/b1/b1_{dev,test}.jsonl`, chấm lại cùng lượt mù. Luật (a): chỉ số quyết USD / câu và `output_tokens` / câu
(dev 120); chất lượng chỉ có mức tụt. Paid: chỉ `gpt-6-luna` (lệnh `run`). Kết quả: JSONL private `data/phase_8_2/r1/`.

Chạy từ `backend/` (thứ tự plan §3; mỗi lệnh ghi file từ chối ghi đè):
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.r1 run --cases oos_dev --name r1_oos_dev
"""
import argparse
import asyncio
import hashlib
import json
import random
import re
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
    bootstrap_mean_diff,
    build_context_builder,
    build_retrieval,
    cost_usd,
    load_golden_cases,
    paired_stats,
    validate_score_rows,
)
from experiments.phase_8_1.g1_retrieval import keep_realism
from experiments.phase_8_1.g2_generate import citation_error, read_scores, usage, write_batches
from experiments.phase_8_2.b1 import read_jsonl, write_jsonl
from llm.citations import CITATION_PATTERN
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator

OUT_DIR = REPO_ROOT / "data/phase_8_2/r1"
B1_DIR = REPO_ROOT / "data/phase_8_2/b1"
SPLIT_PATH = REPO_ROOT / "knowledge-base-hue/evaluation/phase_8_1/split.json"
SEED = 20261024
REASONING_EFFORT = "none"

# Plan R1 §3 bước 2: 120 / 168 (sàn: context không có fact ⇒ phải vẫn từ chối); 172 (+ 173 trong nhóm U): 8.1 `none` trả lời không citation
# ⇒ API 500 (B55 M-1); 9 câu under-answer của C36 (theo dõi, không dừng) — ở B1 chỉ 6 câu còn Completeness 4 (B55 m-2).
MUST_REFUSE = (120, 168)
UNDER_ANSWER = (28, 38, 41, 51, 65, 66, 93, 141, 173)
UNDER_ANSWER_AT_4 = (38, 51, 65, 66, 141, 173)
EARLY = MUST_REFUSE + (172,) + UNDER_ANSWER
NO_CITATION = "Grounded answer has no citation"
RUNS = {"r1": [OUT_DIR / "r1_dev.jsonl", OUT_DIR / "r1_test.jsonl"], "b1": [B1_DIR / "b1_dev.jsonl", B1_DIR / "b1_test.jsonl"]}
SAME_FIELDS = ("top_chunk_ids", "context_sources", "input_tokens")  # 8.1 G2.4: `none` không đổi đầu vào (120 / 120)


# ---------- Tập câu ----------

def cases_for(name: str) -> list[dict]:
    """oos_dev (bước 1) / early (bước 2) / dev_rest (bước 3) / test_pilot, test_rest (bước 5)."""
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

async def generate(cases: list[dict]) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    context_builder = build_context_builder(settings)
    generator = OpenAIFullCorpusGenerator.from_environment(settings, reasoning_effort=REASONING_EFFORT)
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


def uncited_sentences(answer: str) -> int:
    """Số câu (tách theo dấu kết câu) có chữ mà không có citation — bắt dạng "nguồn không có…" chen vào câu trả lời có `[n]` (theo dõi)."""
    return sum(1 for s in re.split(r"(?<=[.!?])\s+", answer.strip()) if re.search(r"\w", s) and not CITATION_PATTERN.search(s))


def check() -> dict:
    """Bước 3 plan: chỉ reasoning đổi ⇒ `top_chunk_ids`, `context_sources`, `input_tokens` = B1. Sàn: OOS, 120 / 168, câu không citation
    (API 500), lỗi. Theo dõi: câu đổi từ chối ↔ trả lời, citation v2 của cả hai lượt."""
    r1, b1 = run_rows("r1"), run_rows("b1")
    answered_now = sorted(i for i in r1 if b1[i]["refusal"] and not r1[i]["refusal"])
    return {
        "cases": len(r1),
        "differ_from_b1": {f: sorted(i for i in r1 if r1[i][f] != b1[i][f]) for f in SAME_FIELDS},
        "oos_answered": sorted(i for i in r1 if r1[i]["category"] == OUT_OF_SCOPE and not r1[i]["refusal"]),
        "must_refuse_answered": sorted(i for i in MUST_REFUSE if i in r1 and not r1[i]["refusal"]),
        "uncited_non_refusal": sorted(i for i in r1 if r1[i]["citation_error"] == NO_CITATION),
        "errors": sorted(i for i in r1 if r1[i]["error"]),
        "refusal_to_answer": [{"case_index": i, "uncited_sentences": uncited_sentences(r1[i]["answer"])} for i in answered_now],
        "answer_to_refusal": sorted(i for i in r1 if r1[i]["refusal"] and not b1[i]["refusal"]),
        # mức tụt chỉ đếm lỗi v2 KHÁC "no citation" (dạng đó đã là sàn API 500 ở trên — plan §2, B55 M-1)
        "citation_v2_other": {run: sorted(i for i, r in rows.items() if not r["error"]
                                          and citation_error(r["answer"], r["context_sources"], single_source_policy=False)
                                          not in (None, NO_CITATION))
                              for run, rows in (("r1", r1), ("b1", {i: b1[i] for i in r1}))},
        "usage": {"r1": usage(list(r1.values())), "b1": usage([b1[i] for i in r1])},
    }


# ---------- Judge Claude: xuất lô mù / ghép điểm ----------

def group_ids(group: str) -> set[int]:
    return set(json.loads(SPLIT_PATH.read_text(encoding="utf-8"))[group])


def pooled_items(group: str) -> tuple[list[dict], dict]:
    """Như `r2.pooled_items`: câu trả lời R1 + B1 của một nhóm; giống hệt chữ trong cùng câu chấm một lần; item là số mờ."""
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
    out = {run: run_rows(run) for run in RUNS}
    for item, pairs in mapping.items():  # chỉ câu của nhóm đã chấm mới có điểm
        for run, case in pairs:
            out[run][case].update({m: scores[int(item)][m] for m in ANSWER_METRICS})
    return out


def ratio(r1: dict, b1: dict, cases: list[int], field: str) -> dict:
    """TB R1 ÷ TB B1 (chỉ số quyết luật (a)) + CI 95 % của chênh theo câu quy ra phần của TB mốc (chỉ báo)."""
    diffs = np.array([r1[i][field] - b1[i][field] for i in cases], dtype=float)
    base = float(np.mean([b1[i][field] for i in cases]))
    boot = bootstrap_mean_diff(diffs, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)
    return {"n": len(cases), "mean_r1": float(np.mean([r1[i][field] for i in cases])), "mean_b1": base,
            "ratio": 1 + float(diffs.mean()) / base, "ratio_ci95": [1 + v / base for v in boot["ci95"]]}


def analyze(group: str) -> dict:
    """Chênh theo cặp R1 − B1 trên một nhóm (plan R1 §2): chỉ số quyết USD / `output_tokens` (mọi câu có gọi model), mức tụt chất lượng
    trên nhóm chính, theo dõi 9 câu under-answer và latency. Kết luận do người đọc theo plan; `rule_a` chỉ tính sẵn phép so ngưỡng."""
    runs = scored_rows(OUT_DIR / f"judge_{group}")
    r1, b1 = runs["r1"], runs["b1"]
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    ids = [i for i in split[group] if i in r1]
    main = sorted(r["case_index"] for r in keep_realism([b1[i] for i in ids], "main") if r["category"] != OUT_OF_SCOPE)
    out = {"group": group, "n": len(ids), "n_main": len(main)}
    for metric in ANSWER_METRICS:
        out[metric] = paired_stats([b1[i][metric] for i in main], [r1[i][metric] for i in main], metric)
        out[f"{metric}_losses"] = sum(r1[i][metric] < b1[i][metric] for i in main)
    out["false_refusal"] = paired_stats([float(b1[i]["refusal"]) for i in main], [float(r1[i]["refusal"]) for i in main], "false_refusal")
    # mức tụt từ chối nhầm (plan §2, B55 m-3): câu chính B1 trả lời mà R1 từ chối; `false_refusal` ở trên chỉ theo dõi
    out["new_refusals_main"] = sorted(i for i in main if r1[i]["refusal"] and not b1[i]["refusal"])
    under = [i for i in UNDER_ANSWER if i in main]
    out["under_answer"] = {"completeness_diff": {i: r1[i]["completeness"] - b1[i]["completeness"] for i in under},
                           "rose_of_6": sorted(i for i in UNDER_ANSWER_AT_4 if i in main and r1[i]["completeness"] > b1[i]["completeness"]),
                           "dropped_of_9": sorted(i for i in under if r1[i]["completeness"] < b1[i]["completeness"])}

    called = sorted(i for i in ids if r1[i]["output_tokens"] is not None and b1[i]["output_tokens"] is not None)
    usd, tokens = ratio(r1, b1, called, "usd"), ratio(r1, b1, called, "output_tokens")
    out["efficiency"] = {"usd": usd, "output_tokens": tokens,
                         "rule_a": {"usd_le_0_95": usd["ratio"] <= 0.95, "output_tokens_le_0_9": tokens["ratio"] <= 0.9,
                                    "usd_le_1": usd["ratio"] <= 1.0, "output_tokens_le_1": tokens["ratio"] <= 1.0}}
    latency_diff = np.array([r1[i]["latency_ms"] - b1[i]["latency_ms"] for i in called], dtype=float)
    out["latency"] = {  # theo dõi: B1 đo phiên 26/10
        "p50_p95": {arm: [float(np.percentile([rows[i]["latency_ms"] for i in called], q)) for q in (50, 95)]
                    for arm, rows in (("r1", r1), ("b1", b1))},
        "mean_diff_ms": float(latency_diff.mean()),
        **bootstrap_mean_diff(latency_diff, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED),
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.r1")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="sinh câu trả lời R1 (paid)")
    run.add_argument("--cases", required=True, choices=["oos_dev", "early", "dev_rest", "test_pilot", "test_rest"])
    run.add_argument("--name", required=True)
    merge = commands.add_parser("merge", help="gộp các phần thành r1_dev / r1_test")
    merge.add_argument("--parts", required=True, nargs="+")
    merge.add_argument("--name", required=True, choices=["r1_dev", "r1_test"])
    commands.add_parser("check", help="tất định so B1 + sàn + citation v2 (free)")
    export = commands.add_parser("export-judge", help="lô chấm mù R1 + B1 của một nhóm")
    export.add_argument("--group", required=True, choices=["dev", "test"])
    export.add_argument("--batch-size", type=int, default=25)
    check_judge = commands.add_parser("check-judge", help="đủ điểm, đúng schema")
    check_judge.add_argument("--group", required=True, choices=["dev", "test"])
    ana = commands.add_parser("analyze", help="chênh theo cặp R1 − B1 (free)")
    ana.add_argument("--group", required=True, choices=["dev", "test"])
    args = parser.parse_args()

    judge_dir = OUT_DIR / f"judge_{args.group}" if hasattr(args, "group") else None
    if args.command == "run":
        out = OUT_DIR / f"{args.name}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists")
        started = time.strftime("%Y-%m-%d %H:%M:%S %z")
        rows = asyncio.run(generate(cases_for(args.cases)))
        spent = usage(rows)
        write_jsonl(out, rows)
        meta = {"name": args.name, "cases": args.cases, "started": started,
                "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"), "usage": spent,
                "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest(), "reasoning_effort": REASONING_EFFORT}
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
        scores = read_scores(judge_dir, "scores")
        print(json.dumps({"items": len(items), "score_errors": validate_score_rows(scores),
                          "scores_missing": sorted(items - {r["case_index"] for r in scores})}))
    else:
        print(json.dumps(analyze(args.group), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
