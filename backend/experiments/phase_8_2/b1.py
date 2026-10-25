"""Phase 8.2 B1 — đo chatbot sau khi đổi context 10 + NFC câu hỏi.

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_plan.md` (A duyệt sha `1a5ac660bd5d`) §3, §4.
Gọi code production, không tham số ghi đè: `full_corpus_eval.run_generation` (context, prompt, reasoning theo `settings.yaml`),
`build_retrieval` + `build_context_builder` cho `nfd-check`. So với G2.1a của 8.1 (cùng context 10, cùng prompt).
Paid: chỉ `gpt-6-luna` ở lệnh `run`. Kết quả: JSONL private `data/phase_8_2/b1/`.

Chạy từ `backend/` (lệnh `run` có phí: pilot 10 câu trước):
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.b1 run --cases pilot --name b1_pilot
"""
import argparse
import asyncio
import hashlib
import json
import random
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np

from evaluation.full_corpus_eval import (
    ANSWER_METRICS,
    BOOTSTRAP_ROUNDS,
    BOOTSTRAP_SEED,
    GOLDEN_FULL,
    OUT_OF_SCOPE,
    REPO_ROOT,
    bootstrap_mean_diff,
    build_context_builder,
    build_retrieval,
    cost_usd,
    load_golden_cases,
    run_generation,
    validate_score_rows,
    verdict,
)
from core.settings_loader import load_settings
from experiments.phase_8_1.g1_retrieval import keep_realism
from experiments.phase_8_1.g2_generate import read_scores, select, usage, write_batches

OUT_DIR = REPO_ROOT / "data/phase_8_2/b1"
G2_DIR = REPO_ROOT / "data/phase_8_1/g2"
SEED = 20261024
# lượt so sánh: B1 (runtime mới) và G2.1a 8.1 (harness, context 10) — dev 120 + test 56
RUNS = {
    "b1": [OUT_DIR / "b1_dev.jsonl", OUT_DIR / "b1_test.jsonl"],
    "g21a": [G2_DIR / "g2_context10.jsonl", G2_DIR / "t_context10.jsonl"],
}
SAME_FIELDS = ("top_chunk_ids", "context_sources", "input_tokens")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return path


def run_rows(run: str) -> dict[int, dict]:
    return {r["case_index"]: r for path in RUNS[run] for r in read_jsonl(path)}


# ---------- T2 / phần T3: so từng câu với G2.1a (free, tất định) ----------

def check() -> dict:
    b1, g21a = run_rows("b1"), run_rows("g21a")
    if set(b1) != set(g21a):
        raise SystemExit(f"case sets differ: b1 {len(b1)} vs g21a {len(g21a)}")
    same = {f: sum(b1[i][f] == g21a[i][f] for i in b1) for f in SAME_FIELDS}
    differ = {f: sorted(i for i in b1 if b1[i][f] != g21a[i][f]) for f in SAME_FIELDS}
    oos = [i for i in b1 if b1[i]["category"] == OUT_OF_SCOPE]
    return {"cases": len(b1), "same": same, "differ_case_index": differ,
            "oos": len(oos), "oos_answered": sorted(i for i in oos if not b1[i]["refusal"]),
            "errors": sorted(i for i in b1 if b1[i]["error"]),
            "citation_errors": {"b1": sorted(i for i in b1 if b1[i]["citation_error"]),
                                "g21a": sorted(i for i in g21a if g21a[i]["citation_error"])},
            "refusals": {"b1": sum(bool(r["refusal"]) for r in b1.values()),
                         "g21a": sum(bool(r["refusal"]) for r in g21a.values())},
            "usage_b1": usage(list(b1.values()))}


# ---------- Judge Claude: xuất lô mù / ghép điểm ----------

def pooled_items() -> tuple[list[dict], dict]:
    """Như `g2_generate.pooled_items` nhưng đọc theo đường dẫn: câu trả lời giống hệt chữ trong cùng câu chấm một lần;
    `item` là số mờ (không lộ lượt); map item → [(lượt, case_index)]."""
    by_case = {c["case_index"]: c for c in load_golden_cases("full")}
    unique: dict[tuple[int, str], list] = defaultdict(list)
    for run in RUNS:
        for row in run_rows(run).values():
            if row["error"] is None:
                unique[(row["case_index"], row["answer"])].append((run, row["case_index"]))
    keys = sorted(unique)
    random.Random(SEED).shuffle(keys)
    items, mapping = [], {}
    for item, key in enumerate(keys, 1):
        case = by_case[key[0]]
        items.append({"case_index": item, "question": case["question"],
                      "reference_answer": case["reference_answer"], "answer": key[1]})
        mapping[item] = unique[key]
    return items, mapping


def scored_rows(judge_dir: Path) -> dict[str, dict[int, dict]]:
    mapping = json.loads((judge_dir / "map.json").read_text(encoding="utf-8"))["items"]
    scores = {r["case_index"]: r for r in read_scores(judge_dir, "scores")}
    out = {run: run_rows(run) for run in RUNS}
    for item, pairs in mapping.items():
        for run, case in pairs:
            out[run][case].update({m: scores[int(item)][m] for m in ANSWER_METRICS})
    return out


def paired(b1: dict[int, dict], g21a: dict[int, dict], cases: list[int], metric: str) -> dict:
    """Chênh theo cặp B1 − G2.1a; `changed` = số câu đổi điểm (nhiễu A/A khi hai lượt cùng cấu hình)."""
    diffs = np.array([b1[i][metric] - g21a[i][metric] for i in cases], dtype=float)
    boot = bootstrap_mean_diff(diffs, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)
    return {"n": len(cases), "mean_diff": float(diffs.mean()), "ci95": boot["ci95"], "verdict": verdict(metric, boot["ci95"]),
            "wins_ties_losses": [int((diffs > 0).sum()), int((diffs == 0).sum()), int((diffs < 0).sum())],
            "changed": int((diffs != 0).sum())}


def analyze(judge_dir: Path) -> dict:
    runs = scored_rows(judge_dir)
    b1, g21a = runs["b1"], runs["g21a"]
    split = json.loads((REPO_ROOT / "knowledge-base-hue/evaluation/phase_8_1/split.json").read_text(encoding="utf-8"))
    dev = set(split["dev"])
    # số chính 8.1: dev, bỏ câu không tự nhiên, trong phạm vi (88 câu) — như `g2_generate.analyze`
    dev_main = {r["case_index"] for r in keep_realism([b1[i] for i in sorted(b1) if i in dev], "main")
                if r["category"] != OUT_OF_SCOPE}
    sets = {"all_176": sorted(b1), "dev_main": sorted(dev_main)}
    return {name: {m: paired(b1, g21a, cases, m) for m in ANSWER_METRICS} for name, cases in sets.items()}


# ---------- T5: câu NFD qua retrieval + context production (free) ----------

def nfd_check(question: str) -> dict:
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    builder = build_context_builder(settings)
    nfc, nfd = unicodedata.normalize("NFC", question), unicodedata.normalize("NFD", question)
    try:
        results = {form: service.search(text) for form, text in (("nfc", nfc), ("nfd", nfd))}
    finally:
        service.close()
    # như `chat.py`: builder nhận đúng chuỗi người dùng gửi
    packed = {form: builder.build(text, results[form].documents).sources for form, text in (("nfc", nfc), ("nfd", nfd))}
    return {"nfd_differs_from_nfc": nfc != nfd, "max_context_documents": settings["full_corpus_generation"]["max_context_documents"],
            "top10_equal": [d.id for d in results["nfc"].documents[:10]] == [d.id for d in results["nfd"].documents[:10]],
            "packed_equal": packed["nfc"] == packed["nfd"],
            "packed_count": {form: len(sources) for form, sources in packed.items()}}


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.b1")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="sinh câu trả lời trên runtime (paid)")
    run.add_argument("--cases", required=True, choices=["pilot", "rest", "test_pilot", "test_rest"])
    run.add_argument("--name", required=True)
    merge = commands.add_parser("merge", help="gộp các phần thành b1_dev / b1_test")
    merge.add_argument("--parts", required=True, nargs="+")
    merge.add_argument("--name", required=True)
    commands.add_parser("check", help="so từng câu với G2.1a; OOS; lỗi (free)")
    export = commands.add_parser("export-judge", help="lô chấm mù B1 + G2.1a")
    export.add_argument("--batch-size", type=int, default=25)
    commands.add_parser("check-judge", help="đủ điểm, đúng schema")
    commands.add_parser("analyze", help="chênh theo cặp B1 − G2.1a (free)")
    nfd = commands.add_parser("nfd-check", help="câu NFD vs NFC qua retrieval + context (free)")
    nfd.add_argument("--question", required=True)
    args = parser.parse_args()

    judge_dir = OUT_DIR / "judge"
    if args.command == "run":
        out = OUT_DIR / f"{args.name}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists")
        started = time.strftime("%Y-%m-%d %H:%M:%S %z")
        rows = asyncio.run(run_generation(select(args.cases)))
        for row in rows:
            row["usd"] = cost_usd(row["input_tokens"] or 0, row["output_tokens"] or 0)
        write_jsonl(out, rows)
        settings = load_settings(validate_private_paths=False)
        meta = {"name": args.name, "cases": args.cases, "started": started,
                "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"), "usage": usage(rows),
                "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest(),
                "max_context_documents": settings["full_corpus_generation"]["max_context_documents"]}
        (OUT_DIR / f"{args.name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(out, json.dumps(meta["usage"]))
    elif args.command == "merge":
        rows = [r for part in args.parts for r in read_jsonl(OUT_DIR / f"{part}.jsonl")]
        if len({r["case_index"] for r in rows}) != len(rows):
            raise SystemExit("duplicated case_index across parts")
        print(write_jsonl(OUT_DIR / f"{args.name}.jsonl", sorted(rows, key=lambda r: r["case_index"])), json.dumps(usage(rows)))
    elif args.command == "check":
        print(json.dumps(check(), ensure_ascii=False, indent=2))
    elif args.command == "export-judge":
        if judge_dir.exists():
            raise SystemExit(f"{judge_dir} exists")
        items, mapping = pooled_items()
        write_batches(judge_dir, items, args.batch_size)
        (judge_dir / "map.json").write_text(json.dumps({"runs": list(RUNS), "items": mapping}, indent=1) + "\n")
        print(json.dumps({"items": len(items), "answers": sum(len(v) for v in mapping.values()),
                          "batches": -(-len(items) // args.batch_size)}))
    elif args.command == "check-judge":
        items = {json.loads(l)["case_index"] for p in judge_dir.glob("batch_*.jsonl") for l in p.read_text().splitlines()}
        scores = read_scores(judge_dir, "scores")
        print(json.dumps({"items": len(items), "score_errors": validate_score_rows(scores),
                          "scores_missing": sorted(items - {r["case_index"] for r in scores})}))
    elif args.command == "analyze":
        print(json.dumps(analyze(judge_dir), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(nfd_check(args.question), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
