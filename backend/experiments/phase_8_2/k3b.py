"""Phase 8.2 §10 K3b — `gpt-6-luna` chọn 10 đoạn từ 30 đoạn RRF (chỉ trả 10 số) + hợp đồng đầu ra tất định; hai nhánh mức suy luận.

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_plan.md` (A duyệt sha trước khi chạy lệnh có phí).
Mốc: `811d25d` (context 10 + NFC); tầng tìm mốc = `data/phase_8_2/k3/base_{dev,test}.jsonl` (K3 bước 0, M2 khớp K1).
Nhánh (plan §1): `n` = gửi `reasoning={"effort": "none"}`; `m` = không gửi reasoning (= mặc định, như K3 / runtime); `none` = không rerank (M2').
Vòng lặp tầng tìm như `k3.retrieval` (retrieval production, 30 đoạn từ `trace.stages["rrf"]`, context builder production); chỉ thay lần gọi
rerank bằng `luna_top10` + `apply_contract` (plan §2: đúng 10 số hợp lệ ⇒ dùng; không thì câu đó dùng nguyên top-10 RRF = mốc).
Lỗi kỹ thuật đầu tiên ⇒ dừng lượt; sai hợp đồng cộng dồn theo nhánh vượt trần ⇒ dừng.
Không ghi Qdrant; mọi file ghi vào `data/phase_8_2/k3b/` và từ chối ghi đè. Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k3b retrieval --name base_dev --cases dev --arm none
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k3b check-base --name base_dev
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.k3b retrieval --name n_l1_pilot --cases pilot --arm n
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.k3b compare --arm n --runs n_l1 n_l2
"""
import argparse
import hashlib
import json
import math
import os
import time

import numpy as np
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, ConfigDict

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import (
    BOOTSTRAP_ROUNDS,
    BOOTSTRAP_SEED,
    GOLDEN_FULL,
    REPO_ROOT,
    bootstrap_mean_diff,
    build_context_builder,
    cost_usd,
    holm_adjust,
    score_retrieval,
)
from experiments.phase_8_1 import g1_retrieval
from experiments.phase_8_1.g4_rerank import packed_chunk_ids
from experiments.phase_8_2.b1 import read_jsonl, write_jsonl
from experiments.phase_8_2.k3 import POOL, TOP_K, gold_cases, new_file
from retrieval.full_corpus import build_full_corpus_retrieval_service, build_retrieved_document

OUT_DIR = REPO_ROOT / "data/phase_8_2/k3b"
K3_BASE = {"dev": REPO_ROOT / "data/phase_8_2/k3/base_dev.jsonl", "test": REPO_ROOT / "data/phase_8_2/k3/base_test.jsonl"}
EFFORT = {"n": "none", "m": None}  # None = không gửi tham số reasoning
# Họ Holm nhánh tìm cố định (plan §4): K1 p 0,798; K3 dừng, không có p ⇒ 1; nhánh K3b chưa chạy ⇒ 1.
K1_P_VALUE, K3_P_VALUE = 0.798, 1.0
MAX_VIOLATIONS = 4  # plan §2 / §4: số đếm tuyệt đối cộng dồn mọi lần gọi của một nhánh (dev L1 + L2 + test), bất kể n
WATCH_CASES = (120, 168)
# Plan §1, ghi trước: câu đầu giữ nguyên LUNA_INSTRUCTIONS 8.1, câu sau đổi sang "đúng 10 số".
LUNA_TOP10_INSTRUCTIONS = (
    "Bạn xếp hạng các đoạn văn theo mức hữu ích để trả lời câu hỏi của người dùng về du lịch và văn hóa Huế. "
    "Trả về đúng 10 số thứ tự của 10 đoạn hữu ích nhất, mỗi số đúng một lần, đoạn hữu ích nhất đứng đầu."
)


class LunaTop10(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order: list[int]


def luna_top10(client: OpenAI, model: str, max_output_tokens: int, query: str, docs: list, effort: str | None) -> dict:
    """Một lần gọi rerank. Chỉ trả `error` cho lỗi kỹ thuật (plan §2 loại 1); danh sách trả về giữ nguyên để `apply_contract` xử lý."""
    passages = "\n\n".join(f"[{n}] {d.text}" for n, d in enumerate(docs, 1))
    reasoning = {"reasoning": {"effort": effort}} if effort else {}
    try:
        response = client.responses.parse(
            model=model, instructions=LUNA_TOP10_INSTRUCTIONS, text_format=LunaTop10, store=False,
            max_output_tokens=max_output_tokens, input=f"Câu hỏi: {query}\n\nCác đoạn:\n{passages}", **reasoning)
    except OpenAIError as exc:
        return {"error": f"api: {type(exc).__name__}: {exc}"[:500]}
    usage = response.usage
    out = {"input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens,
           "usd": cost_usd(usage.input_tokens, usage.output_tokens), "raw": response.output_text, "status": response.status}
    parsed = response.output_parsed
    if response.status != "completed" or parsed is None:
        return {**out, "error": f"status {response.status}, parsed {parsed is not None}"}
    return {**out, "order": parsed.order}


def apply_contract(order: list[int], n: int = POOL, k: int = TOP_K) -> tuple[list[int], dict]:
    """Hợp đồng đầu ra (plan §2): đúng k số, mỗi số trong 1..n, không lặp ⇒ dùng thứ tự luna; mọi trường hợp khác ⇒ nguyên top-k RRF
    (1..k, = mốc), không ghép một phần danh sách luna. Trả số thứ tự (1-based) của k đoạn và bộ đếm dạng sai để báo."""
    in_range = [x for x in order if 1 <= x <= n]
    counts = {"n_returned": len(order), "n_out_of_range": len(order) - len(in_range), "n_duplicate": len(in_range) - len(set(in_range))}
    counts["contract_violation"] = len(order) != k or counts["n_out_of_range"] > 0 or counts["n_duplicate"] > 0
    return (list(range(1, k + 1)) if counts["contract_violation"] else list(order)), counts


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> list[float]:
    """CI chính xác cho tỉ lệ k / n (tìm nhị phân trên CDF nhị thức; numpy không có hàm beta ngược, không thêm scipy)."""
    cdf = lambda p, upto: sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(upto + 1))

    def solve(target, upto):  # p mà cdf(p, upto) = target; cdf giảm theo p
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if cdf(mid, upto) > target else (lo, mid)
        return (lo + hi) / 2

    lower = 0.0 if k == 0 else solve(1 - alpha / 2, k - 1)
    upper = 1.0 if k == n else solve(alpha / 2, k)
    return [lower, upper]


# ---------- Tầng tìm ----------

def arm_rows(arm: str) -> list[dict]:
    """Mọi dòng đã ghi của một nhánh (để đếm sai hợp đồng cộng dồn qua L1, L2, test)."""
    return [r for path in sorted(OUT_DIR.glob("*.jsonl")) for r in read_jsonl(path) if r.get("arm") == arm]


def retrieval(name: str, cases_name: str, arm: str) -> dict:
    out = new_file(OUT_DIR / f"{name}.jsonl")
    meta_path = new_file(OUT_DIR / f"{name}.meta.json")
    settings = load_settings(validate_private_paths=False)
    runtime, generation = settings["full_corpus_runtime"], settings["full_corpus_generation"]
    service = build_full_corpus_retrieval_service(runtime["candidate_id"], runtime["retrieval_treatment"], runtime["reranker"],
                                                  settings=settings, candidate_pool=POOL)
    context_builder = build_context_builder(settings)
    gold = g1_retrieval.load_gold(g1_retrieval.GOLD_PATH)
    meta = {"name": name, "cases": cases_name, "arm": arm, "pool": POOL, "started": time.strftime("%Y-%m-%d %H:%M:%S %z"),
            "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest(),
            "instructions_sha12": hashlib.sha256(LUNA_TOP10_INSTRUCTIONS.encode()).hexdigest()[:12]}
    luna = None
    if arm != "none":
        luna = OpenAI(api_key=os.environ[generation["api_key_env"]], timeout=generation["timeout_seconds"], max_retries=0)
        meta.update(model_id=generation["model"], max_output_tokens=generation["answer_max_output_tokens"], reasoning_effort=EFFORT[arm])
        violations = sum(r["contract"]["contract_violation"] for r in arm_rows(arm) if "contract" in r)
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
            row = {"case_index": case["case_index"], "category": case["category"], "config": name, "arm": arm,
                   "pool_chunk_ids": [d.id for d in pool_docs], "retrieval_ms": (t1 - t0) * 1000}
            if luna is None:
                top = pool_docs[:TOP_K]
            else:
                row["luna"] = luna_top10(luna, meta["model_id"], meta["max_output_tokens"], query, pool_docs, EFFORT[arm])
                row["rerank_ms"] = (time.perf_counter() - t1) * 1000
                if "error" in row["luna"]:
                    rows.append(row)
                    meta["stopped"] = f"technical error at case {case['case_index']}: {row['luna']['error']}"
                    break
                picked, row["contract"] = apply_contract(row["luna"]["order"])
                top = [pool_docs[i - 1] for i in picked]
                violations += row["contract"]["contract_violation"]
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
            if luna is not None and violations > MAX_VIOLATIONS:
                meta["stopped"] = f"contract tolerance exceeded for arm {arm}: {violations} violations > {MAX_VIOLATIONS} (plan §6.2)"
                break
    finally:
        service.close()
    meta["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    meta["n"] = len(rows)
    if luna is not None:
        calls = [r["luna"] for r in rows]
        contracts = [r["contract"] for r in rows if "contract" in r]
        meta["technical_errors"] = sum("error" in c for c in calls)
        meta["contract_violations"] = sum(c["contract_violation"] for c in contracts)
        meta["violation_cases"] = [r["case_index"] for r in rows if r.get("contract", {}).get("contract_violation")]
        meta["arm_cumulative_violations"] = violations
        meta["usage"] = {k: sum(c.get(k, 0) for c in calls) for k in ("input_tokens", "output_tokens", "usd")}
        meta["usd_per_call"] = meta["usage"]["usd"] / len(calls) if calls else None
        meta["output_tokens_max"] = max((c.get("output_tokens", 0) for c in calls), default=0)
        ms = [r["rerank_ms"] for r in rows]
        meta["rerank_ms_p50_p95"] = [float(np.percentile(ms, 50)), float(np.percentile(ms, 95))] if ms else None
    write_jsonl(out, rows)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


def check_base(name: str, group: str = "dev") -> dict:
    """M2' (plan §3): lượt `--arm none` của harness này khớp từng câu với mốc K3 ở top-10 và mọi tầng đoạn đúng."""
    mine = {r["case_index"]: r for r in read_jsonl(OUT_DIR / f"{name}.jsonl")}
    base = {r["case_index"]: r for r in read_jsonl(K3_BASE[group])}
    fields = ("top_chunk_ids", "top10_gold_all", "top10_gold_frac", "context_chunk_ids", "context_gold_all", "pool_gold_all")
    differ = {f: sorted(i for i in base if mine.get(i, {}).get(f) != base[i][f]) for f in fields}
    return {"cases": [len(mine), len(base)], "same_case_set": sorted(mine) == sorted(base), "differ": differ}


def compare(arm: str, runs: list[str], group: str, other_arm_p: float) -> dict:
    """Chỉ số quyết `context_gold_all` (plan §4): thắng = mốc 0 → 1 ở MỌI lượt; thua = mốc 1 → 0 ở ÍT NHẤT một lượt; bootstrap trên
    vector +1 / −1 / 0; Holm họ cố định {K1, K3, nhánh này, nhánh kia}. Sàn: mất đoạn đúng ở top-10 hoặc context. Kèm mức tụt hợp đồng."""
    base = {r["case_index"]: r for r in read_jsonl(K3_BASE[group])}
    run_rows = {name: {r["case_index"]: r for r in read_jsonl(OUT_DIR / f"{name}.jsonl")} for name in runs}
    cases = sorted(base)
    missing = {name: sorted(set(cases) - {i for i, r in rows.items() if "context_gold_all" in r}) for name, rows in run_rows.items()}
    if any(missing.values()):
        raise SystemExit(f"runs miss cases (lượt dừng sớm?): {missing}")
    runs_of = lambda i, key: [rows[i][key] for rows in run_rows.values()]
    won = [i for i in cases if base[i]["context_gold_all"] == 0 and all(v == 1 for v in runs_of(i, "context_gold_all"))]
    lost = {layer: [i for i in cases if base[i][f"{layer}_gold_all"] == 1 and any(v == 0 for v in runs_of(i, f"{layer}_gold_all"))]
            for layer in ("context", "top10")}
    vector = np.array([1.0 if i in won else -1.0 if i in lost["context"] else 0.0 for i in cases])
    stats = bootstrap_mean_diff(vector, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)
    contracts = [r["contract"] for r in arm_rows(arm) if "contract" in r]
    violations = sum(c["contract_violation"] for c in contracts)
    mean = lambda rows, key: float(np.mean([rows[i][key] for i in cases]))
    out = {
        "arm": arm, "group": group, "n": len(cases), "won": won, "lost_context": lost["context"], "lost_top10": lost["top10"],
        "decide": {**stats, "mean": float(vector.mean()),
                   "p_holm": holm_adjust([K1_P_VALUE, K3_P_VALUE, stats["p_value"], other_arm_p])[2]},
        "contract_arm_all_calls": {"calls": len(contracts), "violations": violations, "max": MAX_VIOLATIONS,
                                   "ci95": clopper_pearson(violations, len(contracts)) if contracts else None,
                                   "by_kind": {"wrong_length": sum(c["n_returned"] != TOP_K for c in contracts),
                                               "out_of_range": sum(c["n_out_of_range"] > 0 for c in contracts),
                                               "duplicate": sum(c["n_duplicate"] > 0 for c in contracts)}},
        "means": {name: {k: mean(rows, k) for k in ("context_gold_all", "top10_gold_all", "top10_gold_frac", "mrr", "ndcg")}
                  for name, rows in {"base": base, **run_rows}.items()},
        "top10_set_changed": {name: sum(set(rows[i]["top_chunk_ids"]) != set(base[i]["top_chunk_ids"]) for i in cases)
                              for name, rows in run_rows.items()},
        "watch": {i: {name: rows[i]["top10_gold_frac"] for name, rows in {"base": base, **run_rows}.items()}
                  for i in WATCH_CASES if i in base},
    }
    if len(runs) == 2:  # nhiễu A/A của luna
        a, b = run_rows[runs[0]], run_rows[runs[1]]
        out["aa_changed_context_gold_all"] = sorted(i for i in cases if a[i]["context_gold_all"] != b[i]["context_gold_all"])
    return out


def merge(parts: list[str], name: str) -> dict:
    rows = [r for part in parts for r in read_jsonl(OUT_DIR / f"{part}.jsonl")]
    if len({r["case_index"] for r in rows}) != len(rows):
        raise SystemExit("duplicated case_index across parts")
    # bản gộp không mang trường `arm` để `arm_rows` không đếm hai lần các lần gọi của phần gốc
    write_jsonl(new_file(OUT_DIR / f"{name}.merged.jsonl"),
                [{k: v for k, v in r.items() if k != "arm"} for r in sorted(rows, key=lambda r: r["case_index"])])
    return {"n": len(rows), "usd": sum(r["luna"].get("usd", 0) for r in rows if "luna" in r)}


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.k3b")
    commands = parser.add_subparsers(dest="command", required=True)
    ret = commands.add_parser("retrieval", help="tầng tìm; --arm n / m là paid")
    ret.add_argument("--name", required=True)
    ret.add_argument("--cases", required=True, choices=["dev", "pilot", "rest", "test"])
    ret.add_argument("--arm", required=True, choices=["none", "n", "m"])
    chk = commands.add_parser("check-base", help="M2': lượt none khớp mốc K3 (free)")
    chk.add_argument("--name", required=True)
    chk.add_argument("--group", default="dev", choices=["dev", "test"])
    cmp = commands.add_parser("compare", help="chỉ số quyết + sàn + mức tụt hợp đồng (free)")
    cmp.add_argument("--arm", required=True, choices=["n", "m"])
    cmp.add_argument("--runs", required=True, nargs="+", help="tên file đã gộp đủ câu (ví dụ n_l1.merged, n_l2)")
    cmp.add_argument("--group", default="dev", choices=["dev", "test"])
    cmp.add_argument("--other-arm-p", type=float, default=1.0, help="p của nhánh kia (1 nếu chưa chạy)")
    mrg = commands.add_parser("merge", help="gộp pilot + rest thành một lượt (file .merged.jsonl)")
    mrg.add_argument("--parts", required=True, nargs="+")
    mrg.add_argument("--name", required=True)
    args = parser.parse_args()

    if args.command == "retrieval":
        result = retrieval(args.name, args.cases, args.arm)
    elif args.command == "check-base":
        result = check_base(args.name, args.group)
    elif args.command == "compare":
        result = compare(args.arm, args.runs, args.group, args.other_arm_p)
    else:
        result = merge(args.parts, args.name)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
