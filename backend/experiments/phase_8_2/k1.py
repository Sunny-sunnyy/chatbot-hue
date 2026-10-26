"""Phase 8.2 §10 K1 — pool dense 30 → 100, giữ cách runtime (BM25 chỉ xếp lại trong pool, RRF k 60).

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_plan.md` (A duyệt sha trước khi chạy).
Mốc: nhánh `p82-b1` `811d25d` (context 10 + NFC); câu trả lời mốc = lượt B1 `data/phase_8_2/b1/b1_{dev,test}.jsonl`.
Tầng tìm gọi lại `g1_retrieval.run_config` / `compare` (không chép logic); tầng trả lời gọi `full_corpus_eval.answer_case`
với retrieval production chỉ đổi `candidate_pool`. Mọi file ghi vào `data/phase_8_2/k1/` và không ghi đè.
Paid: chỉ lệnh `run` (`gpt-6-luna`; pilot 10 câu trước). Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k1 retrieval --name k1_dev --group dev --pool 100
"""
import argparse
import asyncio
import hashlib
import json
import random
import statistics
import time
from collections import defaultdict
from pathlib import Path

from core.schema import CitationIntegrityError
from core.settings_loader import load_settings
from evaluation.full_corpus_eval import (
    ANSWER_METRICS,
    CONCURRENCY,
    GOLDEN_FULL,
    OUT_OF_SCOPE,
    REPO_ROOT,
    answer_case,
    build_context_builder,
    cost_usd,
    load_golden_cases,
    validate_score_rows,
)
from experiments.phase_8_1 import g1_retrieval
from experiments.phase_8_1.g2_generate import read_scores, select, usage, write_batches
from experiments.phase_8_2.b1 import paired, read_jsonl, write_jsonl
from llm.citations import select_cited_sources
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from retrieval.full_corpus import build_full_corpus_retrieval_service
from retrieval.full_corpus_context import PackedSource

OUT_DIR = REPO_ROOT / "data/phase_8_2/k1"
B1_DIR = REPO_ROOT / "data/phase_8_2/b1"
SPLIT_PATH = REPO_ROOT / "knowledge-base-hue/evaluation/phase_8_1/split.json"
BASE_POOL, K1_POOL = 30, 100
SEED = 20261024
# lượt so tầng trả lời: mốc B1 (pool 30) và K1 (pool 100), dev 120 + test 56
RUNS = {
    "base": [B1_DIR / "b1_dev.jsonl", B1_DIR / "b1_test.jsonl"],
    "k1": [OUT_DIR / "k1_dev.answers.jsonl", OUT_DIR / "k1_test.answers.jsonl"],
}
WATCH_CASES = (120, 168)  # sàn "vẫn từ chối" của khâu trả lời không áp cho K1 (A 21:4x) — chỉ theo dõi


def new_file(path: Path) -> Path:
    if path.exists():
        raise SystemExit(f"{path} exists — không ghi đè")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def retrieval_service(settings: dict, pool: int):
    runtime = settings["full_corpus_runtime"]
    return build_full_corpus_retrieval_service(runtime["candidate_id"], runtime["retrieval_treatment"], runtime["reranker"],
                                               settings=settings, candidate_pool=pool)


# ---------- Tầng tìm (free, tất định) ----------

def retrieval(name: str, group: str, pool: int) -> None:
    out = new_file(OUT_DIR / f"{name}.jsonl")
    args = argparse.Namespace(name=name, group=group, pilot=None, treatment="dense_bm25_rrf", pool=pool, rrf_k=60,
                              exact=False, fusion="rrf", sparse_weight=0.3, query_form="orig", nfc=False, minilm=False)
    rows = g1_retrieval.run_config(args)
    out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    print(out, json.dumps(g1_retrieval.summarize(rows), ensure_ascii=False))


def compare(a: str, b: str, metrics: list[str]) -> dict:
    a_rows, b_rows = read_jsonl(OUT_DIR / f"{a}.jsonl"), read_jsonl(OUT_DIR / f"{b}.jsonl")
    result = g1_retrieval.compare(a_rows, {b: b_rows}, metrics)
    base = {r["case_index"]: r for r in a_rows if "top10_gold_all" in r}
    var = {r["case_index"]: r for r in b_rows if "top10_gold_all" in r}
    common = sorted(base.keys() & var.keys())
    result["cases"] = {  # sàn: "mất" = mốc đủ đoạn đúng, K1 không đủ
        "lost": [i for i in common if base[i]["top10_gold_all"] == 1 and var[i]["top10_gold_all"] == 0],
        "won": [i for i in common if base[i]["top10_gold_all"] == 0 and var[i]["top10_gold_all"] == 1],
        "watch": {i: [base[i]["top10_gold_frac"], var[i]["top10_gold_frac"]] for i in WATCH_CASES if i in common},
    }
    top_a = {r["case_index"]: set(r["top_chunk_ids"]) for r in a_rows}
    top_b = {r["case_index"]: set(r["top_chunk_ids"]) for r in b_rows}
    result["top10_set_changed"] = [sum(top_a[i] != top_b[i] for i in top_a.keys() & top_b.keys()), len(top_a.keys() & top_b.keys())]
    return result


def check_base(name: str) -> dict:
    """M2 của plan: lượt mốc của harness này khớp từng câu với G1 `runtime.jsonl` ở các trường không phụ thuộc context
    (cột `context5_*` trên `811d25d` là context 10 nên không so)."""
    mine = {r["case_index"]: r for r in read_jsonl(OUT_DIR / f"{name}.jsonl")}
    g1 = {r["case_index"]: r for r in read_jsonl(g1_retrieval.OUT_DIR / "runtime.jsonl")}
    fields = ["top_chunk_ids", "dense_chunk_ids"] + sorted(k for r in g1.values() for k in r
                                                           if k.startswith(("pool_", "top10_gold_")) and k in r)
    fields = list(dict.fromkeys(fields))
    differ = {f: sorted(i for i in g1 if mine.get(i, {}).get(f) != g1[i].get(f)) for f in fields}
    return {"cases": [len(mine), len(g1)], "fields": fields, "differ": {f: v for f, v in differ.items() if v}}


def latency(name: str, runs: int) -> dict:
    """Mốc và K1 đo cùng phiên, xen kẽ (base → k1 → base → k1); mỗi service bỏ 1 câu khởi động.
    Chỉ số (plan §4): TRUNG BÌNH theo câu của (K1 − mốc), mỗi bên lấy total_ms trung bình các lượt; nhiễu = base lượt cuối − lượt đầu."""
    out = new_file(OUT_DIR / f"{name}.json")
    settings = load_settings(validate_private_paths=False)
    cases = g1_retrieval.select_cases("dev", None)
    services = {"base": retrieval_service(settings, BASE_POOL), "k1": retrieval_service(settings, K1_POOL)}
    ms: dict[str, dict[int, list[float]]] = {k: defaultdict(list) for k in services}
    try:
        for service in services.values():
            service.search(cases[0]["question"].strip())
        for _ in range(runs):
            for key, service in services.items():
                for case in cases:
                    ms[key][case["case_index"]].append(service.search(case["question"].strip()).trace.timings_ms["total_ms"])
    finally:
        for service in services.values():
            service.close()
    mean = {k: {i: statistics.fmean(v) for i, v in per.items()} for k, per in ms.items()}
    diffs = [mean["k1"][i] - mean["base"][i] for i in mean["base"]]
    noise = [ms["base"][i][-1] - ms["base"][i][0] for i in ms["base"]]
    pct = lambda xs, q: statistics.quantiles(xs, n=100)[q - 1]
    result = {"n": len(diffs), "runs": runs, "mean_diff_ms": statistics.fmean(diffs), "p95_diff_ms": pct(diffs, 95),
              "noise_base_mean_diff_ms": statistics.fmean(noise), "noise_base_p95_abs_ms": pct([abs(x) for x in noise], 95),
              **{f"{k}_p50_p95": [statistics.median(v.values()), pct(list(v.values()), 95)] for k, v in mean.items()},
              "per_case_ms": {k: {str(i): v for i, v in per.items()} for k, per in ms.items()}}
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    return {k: v for k, v in result.items() if k != "per_case_ms"}


# ---------- Tầng trả lời (paid: gpt-6-luna) ----------

async def generate(cases: list[dict]) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    service = retrieval_service(settings, K1_POOL)
    context_builder = build_context_builder(settings)
    generator = OpenAIFullCorpusGenerator.from_environment(settings)
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async def one(case: dict) -> dict:
        async with semaphore:
            return await answer_case(case, service, context_builder, generator)

    try:
        return list(await asyncio.gather(*(one(case) for case in cases)))
    finally:
        service.close()
        await generator.aclose()


def run_rows(run: str) -> dict[int, dict]:
    return {r["case_index"]: r for path in RUNS[run] for r in read_jsonl(path)}


def pooled_items() -> tuple[list[dict], dict]:
    """Như `b1.pooled_items` cho cặp mốc / K1: câu trả lời giống hệt chữ trong cùng câu chấm một lần; `item` mờ."""
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


def citation_v2(row: dict) -> bool:
    """Lỗi citation theo validator hiện hành, tính lại cho cả hai lượt (mốc B1 sinh trước validator v2 — gói 3c).
    Validator chỉ cần số nguồn đã đóng gói."""
    if row["error"] or row["refusal"] or not row["context_sources"]:
        return False
    sources = [PackedSource(id=i, title="", heading_path=(), excerpts=("",)) for i in range(1, row["context_sources"] + 1)]
    try:
        select_cited_sources(row["answer"], sources)
        return False
    except CitationIntegrityError:
        return True


def analyze(judge_dir: Path) -> dict:
    mapping = json.loads((judge_dir / "map.json").read_text(encoding="utf-8"))["items"]
    scores = {r["case_index"]: r for r in read_scores(judge_dir, "scores")}
    runs = {run: run_rows(run) for run in RUNS}
    for item, pairs in mapping.items():
        for run, case in pairs:
            runs[run][case].update({m: scores[int(item)][m] for m in ANSWER_METRICS})
    base, k1 = runs["base"], runs["k1"]
    dev = set(json.loads(SPLIT_PATH.read_text(encoding="utf-8"))["dev"])
    dev_main = sorted(r["case_index"] for r in g1_retrieval.keep_realism([base[i] for i in sorted(base) if i in dev], "main")
                      if r["category"] != OUT_OF_SCOPE)
    refused = lambda rows: sorted(i for i in dev_main if rows[i]["refusal"])
    cite = lambda rows: sorted(i for i in rows if citation_v2(rows[i]))
    return {
        "dev_main": {m: paired(k1, base, dev_main, m) for m in ANSWER_METRICS},
        "oos_answered": sorted(i for i in k1 if k1[i]["category"] == OUT_OF_SCOPE and not k1[i]["refusal"]),
        "errors": sorted(i for i in k1 if k1[i]["error"]),
        "refusals_dev_main": {"base": refused(base), "k1": refused(k1)},
        "citation_v2_errors": {"base": cite(base), "k1": cite(k1)},
        "usage": {"base": usage(list(base.values())), "k1": usage(list(k1.values()))},
        "watch": {i: {run: {"refusal": runs[run][i]["refusal"], "context_sources": runs[run][i]["context_sources"]}
                      for run in RUNS} for i in WATCH_CASES},
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.k1")
    commands = parser.add_subparsers(dest="command", required=True)
    ret = commands.add_parser("retrieval", help="tầng tìm một cấu hình (free)")
    ret.add_argument("--name", required=True)
    ret.add_argument("--group", required=True, choices=["dev", "test"])
    ret.add_argument("--pool", required=True, type=int, choices=[BASE_POOL, K1_POOL])
    cmp = commands.add_parser("compare", help="so theo cặp + câu mất / thắng (free)")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True)
    cmp.add_argument("--metrics", required=True, nargs="+")
    chk = commands.add_parser("check-base", help="M2: lượt mốc khớp G1 runtime.jsonl (free)")
    chk.add_argument("--name", required=True)
    lat = commands.add_parser("latency", help="mốc vs K1 cùng phiên, xen kẽ (free)")
    lat.add_argument("--name", required=True)
    lat.add_argument("--runs", type=int, default=2)
    run = commands.add_parser("run", help="sinh câu trả lời K1 (paid)")
    run.add_argument("--cases", required=True, choices=["pilot", "rest", "test_pilot", "test_rest"])
    run.add_argument("--name", required=True)
    merge = commands.add_parser("merge", help="gộp phần thành k1_dev / k1_test .answers.jsonl")
    merge.add_argument("--parts", required=True, nargs="+")
    merge.add_argument("--name", required=True, choices=["k1_dev", "k1_test"])
    export = commands.add_parser("export-judge", help="lô chấm mù mốc + K1")
    export.add_argument("--batch-size", type=int, default=20)
    commands.add_parser("check-judge", help="đủ điểm, đúng schema")
    commands.add_parser("analyze", help="tầng trả lời theo §4 plan (free)")
    args = parser.parse_args()

    judge_dir = OUT_DIR / "judge"
    if args.command == "retrieval":
        retrieval(args.name, args.group, args.pool)
    elif args.command == "compare":
        print(json.dumps(compare(args.a, args.b, args.metrics), ensure_ascii=False, indent=2))
    elif args.command == "check-base":
        print(json.dumps(check_base(args.name), indent=2))
    elif args.command == "latency":
        print(json.dumps(latency(args.name, args.runs), indent=2))
    elif args.command == "run":
        out = new_file(OUT_DIR / f"{args.name}.jsonl")
        started = time.strftime("%Y-%m-%d %H:%M:%S %z")
        rows = asyncio.run(generate(select(args.cases)))
        for row in rows:
            row["usd"] = cost_usd(row["input_tokens"] or 0, row["output_tokens"] or 0)
        write_jsonl(out, rows)
        meta = {"name": args.name, "cases": args.cases, "candidate_pool": K1_POOL, "started": started,
                "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"), "usage": usage(rows),
                "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest()}
        new_file(OUT_DIR / f"{args.name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(out, json.dumps(meta["usage"]))
    elif args.command == "merge":
        rows = [r for part in args.parts for r in read_jsonl(OUT_DIR / f"{part}.jsonl")]
        if len({r["case_index"] for r in rows}) != len(rows):
            raise SystemExit("duplicated case_index across parts")
        out = new_file(OUT_DIR / f"{args.name}.answers.jsonl")
        print(write_jsonl(out, sorted(rows, key=lambda r: r["case_index"])), json.dumps(usage(rows)))
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
    else:
        print(json.dumps(analyze(judge_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
