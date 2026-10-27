"""Phase 8.2 §10 K3 — `gpt-6-luna` xếp lại cả 30 đoạn sau RRF (pool 30, RRF k 60), lấy 10 đầu làm top-10.

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` (A duyệt sha `0a6370204c7d`).
Mốc: nhánh `p82-b1` `811d25d` (context 10 + NFC); tầng tìm mốc = `data/phase_8_2/k1/base_dev.jsonl` (K1, tất định).
Đổi đúng một thứ: thứ tự top-10. Retrieval production (`service.search`) giữ nguyên; 30 đoạn lấy từ `trace.stages["rrf"]`
theo thứ tự RRF, luna xếp bằng `g4_rerank.luna_rank` + `LUNA_INSTRUCTIONS` (8.1, không sửa). Không ghi Qdrant.
Paid: chỉ `--rerank luna` (pilot 10 câu trước). Lỗi đầu ra luna đầu tiên ⇒ dừng lượt (plan §6.3: không gọi lại, không thay
bằng thứ tự RRF). Mọi file ghi vào `data/phase_8_2/k3/` và từ chối ghi đè. Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k3 retrieval --name base_dev --cases dev --rerank none
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k3 check-base --name base_dev
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.k3 retrieval --name l1_pilot --cases pilot --rerank luna
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k3 compare --base base_dev --runs l1_dev l2_dev
"""
import argparse
import hashlib
import json
import os
import time
from pathlib import Path

import numpy as np
from openai import OpenAI

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import (
    BOOTSTRAP_ROUNDS,
    BOOTSTRAP_SEED,
    GOLDEN_FULL,
    REPO_ROOT,
    bootstrap_mean_diff,
    build_context_builder,
    holm_adjust,
    score_retrieval,
)
from experiments.phase_8_1 import g1_retrieval
from experiments.phase_8_1.g4_rerank import luna_rank, packed_chunk_ids
from experiments.phase_8_2.b1 import read_jsonl, write_jsonl
from retrieval.full_corpus import build_full_corpus_retrieval_service, build_retrieved_document

OUT_DIR = REPO_ROOT / "data/phase_8_2/k3"
K1_BASE = REPO_ROOT / "data/phase_8_2/k1/base_dev.jsonl"
POOL, TOP_K = 30, 10
K1_P_VALUE = 0.798  # họ Holm {K1, K3} cố định (plan §4; K1 report §4)
WATCH_CASES = (120, 168)


def new_file(path: Path) -> Path:
    if path.exists():
        raise SystemExit(f"{path} exists — không ghi đè")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def gold_cases(name: str) -> list[dict]:
    """Câu có đoạn đúng: dev (40) / test (15); pilot = 10 câu dev rút như `g1_retrieval --pilot 10`; rest = dev − pilot."""
    if name in ("dev", "test"):
        gold = g1_retrieval.load_gold(g1_retrieval.GOLD_PATH)
        return [c for c in g1_retrieval.select_cases(name, None) if c["case_index"] in gold]
    pilot = g1_retrieval.select_cases("dev", 10)
    if name == "pilot":
        return pilot
    skip = {c["case_index"] for c in pilot}
    return [c for c in gold_cases("dev") if c["case_index"] not in skip]


# ---------- Tầng tìm ----------

def retrieval(name: str, cases_name: str, rerank: str) -> dict:
    out = new_file(OUT_DIR / f"{name}.jsonl")
    meta_path = new_file(OUT_DIR / f"{name}.meta.json")
    settings = load_settings(validate_private_paths=False)
    runtime, generation = settings["full_corpus_runtime"], settings["full_corpus_generation"]
    service = build_full_corpus_retrieval_service(runtime["candidate_id"], runtime["retrieval_treatment"], runtime["reranker"],
                                                  settings=settings, candidate_pool=POOL)
    context_builder = build_context_builder(settings)
    gold = g1_retrieval.load_gold(g1_retrieval.GOLD_PATH)
    meta = {"name": name, "cases": cases_name, "rerank": rerank, "pool": POOL, "started": time.strftime("%Y-%m-%d %H:%M:%S %z"),
            "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest()}
    luna = None
    if rerank == "luna":
        luna = OpenAI(api_key=os.environ[generation["api_key_env"]], timeout=generation["timeout_seconds"], max_retries=0)
        meta.update(model_id=generation["model"], max_output_tokens=generation["answer_max_output_tokens"])
    rows = []
    try:
        payloads = g1_retrieval.load_payloads(service.client, service.candidate.collection_name)
        payload_by_chunk = {p["chunk_id"]: p for p in payloads.values()}
        for case in gold_cases(cases_name):
            query = case["question"].strip()
            t0 = time.perf_counter()
            result = service.search(query)
            t1 = time.perf_counter()
            pool_docs = [build_retrieved_document(payloads[e["point_id"]], e["score"]) for e in result.trace.stages["rrf"]]
            row = {"case_index": case["case_index"], "category": case["category"], "config": name,
                   "pool_chunk_ids": [d.id for d in pool_docs], "retrieval_ms": (t1 - t0) * 1000}
            if luna is None:
                top = pool_docs[:TOP_K]
            else:
                row["luna"] = luna_rank(luna, meta["model_id"], meta["max_output_tokens"], query, pool_docs)
                row["rerank_ms"] = (time.perf_counter() - t1) * 1000
                if "error" in row["luna"]:
                    rows.append(row)
                    meta["stopped"] = f"luna error at case {case['case_index']}: {row['luna']['error']}"
                    break
                top = [pool_docs[n - 1] for n in row["luna"]["order"]][:TOP_K]
            row["total_ms"] = (time.perf_counter() - t0) * 1000  # tìm đầu–cuối = retrieval + rerank
            packed = context_builder.build(query, top)
            row["top_chunk_ids"] = [d.id for d in top]
            row["context_chunk_ids"] = packed_chunk_ids(top, len(packed.sources))
            row.update(score_retrieval(case["keywords"], [d.text for d in top]))
            layers = {"pool": row["pool_chunk_ids"], "top10": row["top_chunk_ids"], "context": row["context_chunk_ids"]}
            for layer, ids in layers.items():
                coverage = g1_retrieval.gold_coverage(gold[case["case_index"]], [payload_by_chunk[i] for i in ids])
                row[f"{layer}_gold_all"], row[f"{layer}_gold_frac"] = coverage["all"], coverage["frac"]
            rows.append(row)
    finally:
        service.close()
    meta["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    meta["n"] = len(rows)
    if luna is not None:
        calls = [r["luna"] for r in rows]
        meta["luna_errors"] = sum("error" in c for c in calls)
        meta["usage"] = {k: sum(c.get(k, 0) for c in calls) for k in ("input_tokens", "output_tokens", "usd")}
        meta["usd_per_call"] = meta["usage"]["usd"] / len(calls) if calls else None
        meta["output_tokens_max"] = max((c.get("output_tokens", 0) for c in calls), default=0)
        ms = [r["rerank_ms"] for r in rows if "error" not in r["luna"]]
        meta["rerank_ms_p50_p95"] = [float(np.percentile(ms, 50)), float(np.percentile(ms, 95))] if ms else None
    write_jsonl(out, rows)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def check_base(name: str) -> dict:
    """M2 (plan §2): lượt `--rerank none` của harness này khớp từng câu với lượt mốc K1 ở `top_chunk_ids` và `top10_gold_*`."""
    mine = {r["case_index"]: r for r in read_jsonl(OUT_DIR / f"{name}.jsonl")}
    k1 = {r["case_index"]: r for r in read_jsonl(K1_BASE) if "top10_gold_all" in r}
    fields = ("top_chunk_ids", "top10_gold_all", "top10_gold_frac")
    differ = {f: sorted(i for i in k1 if mine.get(i, {}).get(f) != k1[i][f]) for f in fields}
    return {"cases": [len(mine), len(k1)], "same_case_set": sorted(mine) == sorted(k1), "differ": differ}


def compare(base: str, runs: list[str]) -> dict:
    """Chỉ số quyết (plan §4): thắng = mốc 0 → 1 ở MỌI lượt; thua = mốc 1 → 0 ở ÍT NHẤT một lượt; bootstrap trên vector
    +1 / −1 / 0, Holm họ {K1, K3}. Sàn: câu mất đoạn đúng ở top-10 hoặc context (lượt nào cũng tính)."""
    base_rows = {r["case_index"]: r for r in read_jsonl(OUT_DIR / f"{base}.jsonl")}
    run_rows = {name: {r["case_index"]: r for r in read_jsonl(OUT_DIR / f"{name}.jsonl")} for name in runs}
    cases = sorted(base_rows)
    missing = {name: sorted(set(cases) - set(rows)) for name, rows in run_rows.items()}
    if any(missing.values()):
        raise SystemExit(f"runs miss cases: {missing}")
    get = lambda rows, i, key: rows[i][key]
    won = [i for i in cases if base_rows[i]["top10_gold_all"] == 0 and all(get(r, i, "top10_gold_all") == 1 for r in run_rows.values())]
    lost = [i for i in cases if base_rows[i]["top10_gold_all"] == 1 and any(get(r, i, "top10_gold_all") == 0 for r in run_rows.values())]
    lost_context = [i for i in cases if base_rows[i]["context_gold_all"] == 1
                    and any(get(r, i, "context_gold_all") == 0 for r in run_rows.values())]
    vector = np.array([1.0 if i in won else -1.0 if i in lost else 0.0 for i in cases])
    stats = bootstrap_mean_diff(vector, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)
    mean = lambda rows, key: float(np.mean([rows[i][key] for i in cases]))
    out = {
        "n": len(cases), "won": won, "lost_top10": lost, "lost_context": lost_context,
        "decide": {**stats, "mean": float(vector.mean()), "p_holm_k1_k3": holm_adjust([K1_P_VALUE, stats["p_value"]])[1]},
        "means": {name: {k: mean(rows, k) for k in ("top10_gold_all", "top10_gold_frac", "context_gold_all", "mrr", "ndcg")}
                  for name, rows in {base: base_rows, **run_rows}.items()},
        "top10_set_changed": {name: sum(set(rows[i]["top_chunk_ids"]) != set(base_rows[i]["top_chunk_ids"]) for i in cases)
                              for name, rows in run_rows.items()},
        "watch": {i: {name: rows[i]["top10_gold_frac"] for name, rows in {base: base_rows, **run_rows}.items()}
                  for i in WATCH_CASES if i in base_rows},
    }
    if len(runs) == 2:  # nhiễu A/A của luna: câu đổi top10_gold_all giữa hai lượt
        a, b = run_rows[runs[0]], run_rows[runs[1]]
        out["aa_changed_top10_gold_all"] = sorted(i for i in cases if a[i]["top10_gold_all"] != b[i]["top10_gold_all"])
    return out


def merge(parts: list[str], name: str) -> dict:
    rows = [r for part in parts for r in read_jsonl(OUT_DIR / f"{part}.jsonl")]
    if len({r["case_index"] for r in rows}) != len(rows):
        raise SystemExit("duplicated case_index across parts")
    write_jsonl(new_file(OUT_DIR / f"{name}.jsonl"), sorted(rows, key=lambda r: r["case_index"]))
    return {"n": len(rows), "usd": sum(r["luna"]["usd"] for r in rows if "luna" in r)}


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.k3")
    commands = parser.add_subparsers(dest="command", required=True)
    ret = commands.add_parser("retrieval", help="tầng tìm; --rerank luna là paid")
    ret.add_argument("--name", required=True)
    ret.add_argument("--cases", required=True, choices=["dev", "pilot", "rest", "test"])
    ret.add_argument("--rerank", required=True, choices=["none", "luna"])
    chk = commands.add_parser("check-base", help="M2: lượt none khớp mốc K1 (free)")
    chk.add_argument("--name", required=True)
    cmp = commands.add_parser("compare", help="chỉ số quyết + sàn tầng tìm (free)")
    cmp.add_argument("--base", required=True)
    cmp.add_argument("--runs", required=True, nargs="+")
    mrg = commands.add_parser("merge", help="gộp pilot + rest thành một lượt")
    mrg.add_argument("--parts", required=True, nargs="+")
    mrg.add_argument("--name", required=True)
    args = parser.parse_args()

    if args.command == "retrieval":
        result = retrieval(args.name, args.cases, args.rerank)
    elif args.command == "check-base":
        result = check_base(args.name)
    elif args.command == "compare":
        result = compare(args.base, args.runs)
    else:
        result = merge(args.parts, args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
