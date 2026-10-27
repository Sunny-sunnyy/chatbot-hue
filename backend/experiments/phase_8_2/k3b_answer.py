"""Phase 8.2 §10 K3b — phụ lục: lượt sinh + judge cho K3b-m (luna chọn 10 / 30 đoạn RRF, không gửi reasoning) so mốc B1.

Plan + tiêu chí ghi trước: `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3b_m_answer_plan.md` (A duyệt sha trước khi chạy lệnh có phí).
Đổi đúng một thứ so B1: retrieval trả 10 đoạn K3b-m thay vì 10 đoạn RRF. `K3bService` bọc retrieval production (khuôn
`g2_generate.DocOrderService`); `full_corpus_eval.answer_case` chạy nguyên (context builder, generator, validator production ở `811d25d`).
Câu có đoạn đúng phát lại thứ tự luna đã ghi (dev: `k3b/m_l1.merged.jsonl`, test: `k3b/m_test.jsonl`; `run-experiment` §3.5); câu khác gọi
`k3b.luna_top10` mới + `k3b.apply_contract`. Ghi từng dòng ngay sau mỗi câu, luôn ghi `.meta.json`; dừng lượt khi phạm sàn. Không ghi Qdrant.
Chạy từ `backend/` (paid: chỉ `run`):
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_2.k3b_answer run --cases pilot --name dev_pilot
"""
import argparse
import asyncio
import dataclasses
import hashlib
import json
import os
import random
import re
import time
from collections import defaultdict

import numpy as np
from openai import OpenAI

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
from experiments.phase_8_1 import g1_retrieval
from experiments.phase_8_1.g2_generate import citation_error, read_scores, select, usage, write_batches
from experiments.phase_8_2.b1 import read_jsonl, write_jsonl
from experiments.phase_8_2.k3 import new_file
from experiments.phase_8_2.k3b import LUNA_TOP10_INSTRUCTIONS, MAX_VIOLATIONS, apply_contract, clopper_pearson, luna_top10
from llm.citations import CITATION_PATTERN
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from retrieval.full_corpus import build_retrieved_document

K3B_DIR = REPO_ROOT / "data/phase_8_2/k3b"
OUT_DIR = K3B_DIR / "answer"
B1_DIR = REPO_ROOT / "data/phase_8_2/b1"
SPLIT_PATH = REPO_ROOT / "knowledge-base-hue/evaluation/phase_8_1/split.json"
REPLAY_FILES = (K3B_DIR / "m_l1.merged.jsonl", K3B_DIR / "m_test.jsonl")  # plan §3: L1 cho dev, ghi trước
RUNS = {"k3b": [OUT_DIR / "answer_dev.jsonl", OUT_DIR / "answer_test.jsonl"], "b1": [B1_DIR / "b1_dev.jsonl", B1_DIR / "b1_test.jsonl"]}
SEED = 20261024
WATCH_CASES = (120, 168)  # plan bản 3 T8: theo dõi (bản 2 đặt 120 là sàn trên tiền đề nhãn thiếu — xem plan "Đổi sau khi thấy số")
WON = {"dev": (17, 38, 48, 67, 70, 85, 156, 159, 167), "test": (20, 95, 130)}  # thắng ở tầng tìm (report K3b §4.3)
# Plan §2 W2: tách câu ở khoảng trắng / cuối chuỗi sau dấu kết câu, GIỮ các `[n]` theo sau dấu kết câu (có thể cách một dấu cách:
# "….[2] Nguồn …", "…. [1]") ở câu trước (B58 m-1, C53 vòng 2 m-4); dấu chấm trong số ("1.100.000") không có khoảng trắng theo sau nên
# không bị tách. Nhận citation đúng như validator production (`llm.citations.CITATION_PATTERN`: không phân biệt hoa thường, cho dấu cách).
SENTENCE_END = re.compile(r"([.!?](?:\s*\[\s*(?:nguồn\s*)?\d+\s*\])*)(?:\s+|$)", re.IGNORECASE)


def uncited_sentences(answer: str) -> int:
    """Số câu có chữ mà không có `[n]` trong một câu trả lời — dấu hiệu "nguồn không có…" chen vào câu trả lời có trích (theo dõi)."""
    parts = SENTENCE_END.split(answer.strip())  # [câu, đuôi câu, câu, đuôi câu, …, câu]
    sentences = [parts[i] + (parts[i + 1] if i + 1 < len(parts) else "") for i in range(0, len(parts), 2)]
    return sum(1 for s in sentences if re.search(r"\w", s) and not CITATION_PATTERN.search(s))


def api_500(row: dict) -> bool:
    """Plan §2 T2 (bản 2): API trả 500 cho mọi lỗi kỹ thuật và mọi `CitationIntegrityError` (`api/routes/chat.py:124-135`)."""
    return bool(row["error"]) or row["citation_error"] is not None


# ---------- Retrieval K3b-m ----------

class K3bService:
    """Bọc retrieval production: 30 đoạn `stages["rrf"]` ⇒ thứ tự luna (phát lại hoặc gọi mới) ⇒ hợp đồng ⇒ 10 đoạn đưa context builder.
    Lỗi kỹ thuật của rerank ném RuntimeError để `answer_case` ghi `error` như mọi lỗi kỹ thuật khác (sàn T2)."""

    def __init__(self, service, payloads: dict, luna: OpenAI, model: str, max_output_tokens: int, replay: dict[int, dict], case_of: dict):
        self._service, self._payloads, self._luna = service, payloads, luna
        self._model, self._max_output_tokens, self._replay, self._case_of = model, max_output_tokens, replay, case_of
        self.info: dict[int, dict] = {}

    def search(self, query: str):
        result = self._service.search(query)
        pool = [build_retrieved_document(self._payloads[e["point_id"]], e["score"]) for e in result.trace.stages["rrf"]]
        case_index = self._case_of[query]
        if case_index in self._replay:
            old = self._replay[case_index]
            info = {"replayed": True, "replay_usd": old["luna"]["usd"], "replay_rerank_ms": old["rerank_ms"]}
            order = old["luna"]["order"]
        else:
            t0 = time.perf_counter()
            call = luna_top10(self._luna, self._model, self._max_output_tokens, query, pool, None)
            info = {"replayed": False, "luna": call, "rerank_ms": (time.perf_counter() - t0) * 1000}
            if "error" in call:
                self.info[case_index] = info
                raise RuntimeError(f"rerank technical error: {call['error']}")
            order = call["order"]
        picked, info["contract"] = apply_contract(order)
        self.info[case_index] = info
        return dataclasses.replace(result, documents=[pool[i - 1] for i in picked])

    def close(self):
        self._service.close()


def replay_rows() -> dict[int, dict]:
    return {r["case_index"]: r for path in REPLAY_FILES for r in read_jsonl(path)}


async def run(cases_name: str, name: str) -> dict:
    out = new_file(OUT_DIR / f"{name}.jsonl")
    meta_path = new_file(OUT_DIR / f"{name}.meta.json")
    settings = load_settings(validate_private_paths=False)
    generation = settings["full_corpus_generation"]
    golden = load_golden_cases("full")
    case_of = {c["question"].strip(): c["case_index"] for c in golden}
    assert len(case_of) == len(golden), "câu hỏi trùng ⇒ không map được query → case"
    base = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    luna = OpenAI(api_key=os.environ[generation["api_key_env"]], timeout=generation["timeout_seconds"], max_retries=0)
    service = K3bService(base, g1_retrieval.load_payloads(base.client, base.candidate.collection_name), luna, generation["model"],
                         generation["answer_max_output_tokens"], replay_rows(), case_of)
    context_builder = build_context_builder(settings)
    generator = OpenAIFullCorpusGenerator.from_environment(settings)
    meta = {"name": name, "cases": cases_name, "started": time.strftime("%Y-%m-%d %H:%M:%S %z"),
            "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest(), "concurrency": CONCURRENCY,
            "rerank_instructions_sha12": hashlib.sha256(LUNA_TOP10_INSTRUCTIONS.encode()).hexdigest()[:12],
            "replay_files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:12] for p in REPLAY_FILES}}
    rows, stop = [], {}
    semaphore = asyncio.Semaphore(CONCURRENCY)
    stream = out.open("x", encoding="utf-8")

    async def one(case: dict) -> None:
        async with semaphore:
            if stop:  # plan §5: phạm sàn ⇒ không gọi tiếp
                return
            t0 = time.perf_counter()
            row = await answer_case(case, service, context_builder, generator)
            row["e2e_ms"] = (time.perf_counter() - t0) * 1000
            row.update(service.info.pop(case["case_index"], {}))
            row["usd_answer"] = cost_usd(row["input_tokens"] or 0, row["output_tokens"] or 0)
            row["usd_rerank"] = 0.0 if row.get("replayed") else row.get("luna", {}).get("usd", 0.0)
            rows.append(row)
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            violations = sum(r.get("contract", {}).get("contract_violation", False) for r in rows)
            if api_500(row):
                stop["reason"] = f"T2 floor at case {case['case_index']}: {row['error'] or row['citation_error']}"[:500]
            elif row["category"] == OUT_OF_SCOPE and not row["refusal"]:
                stop["reason"] = f"T1 floor: out_of_scope case {case['case_index']} answered"
            elif violations > MAX_VIOLATIONS:
                stop["reason"] = f"contract violations {violations} > {MAX_VIOLATIONS}"

    try:
        await asyncio.gather(*(one(case) for case in select(cases_name)))
    except BaseException as exc:  # ghi lại rồi ném tiếp: meta phải có dù lượt dừng vì lỗi không lường trước
        meta["crashed"] = f"{type(exc).__name__}: {exc}"[:500]
        raise
    finally:
        service.close()
        await generator.aclose()
        stream.close()
        new_calls = [r["luna"] for r in rows if "luna" in r]
        meta.update(finished=time.strftime("%Y-%m-%d %H:%M:%S %z"), n=len(rows), stopped=stop.get("reason"),
                    answer_usage=usage(rows), replayed=sum(bool(r.get("replayed")) for r in rows), rerank_new_calls=len(new_calls),
                    rerank_usage={k: sum(c.get(k, 0) for c in new_calls) for k in ("input_tokens", "output_tokens", "usd")},
                    contract_violations=sum(r.get("contract", {}).get("contract_violation", False) for r in rows))
        meta["usd_total"] = meta["answer_usage"]["usd"] + meta["rerank_usage"]["usd"]
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta


# ---------- Kiểm (free) ----------

def run_rows(run_name: str) -> dict[int, dict]:
    return {r["case_index"]: r for path in RUNS[run_name] if path.exists() for r in read_jsonl(path)}


def check() -> dict:
    """Sàn T1 / T2, T6 theo dạng + T8 120 / 168 (theo dõi), phát lại = file gốc, hợp đồng, tiền."""
    k3b, b1, replay = run_rows("k3b"), run_rows("b1"), replay_rows()
    replayed = [i for i in k3b if k3b[i].get("replayed")]
    contracts = [r["contract"] for r in k3b.values() if "contract" in r and not r.get("replayed")]
    v2 = lambda rows: sorted(i for i, r in rows.items() if not r["error"]
                             and citation_error(r["answer"], r["context_sources"], single_source_policy=False))
    return {
        "cases": len(k3b),
        "T1_oos_answered": sorted(i for i in k3b if k3b[i]["category"] == OUT_OF_SCOPE and not k3b[i]["refusal"]),
        "T2_api_500": sorted(i for i in k3b if api_500(k3b[i])),
        "T8_watch_refusal": {i: k3b[i]["refusal"] for i in WATCH_CASES if i in k3b},
        "T6_citation_v2_by_kind": {run_name: {i: citation_error(r["answer"], r["context_sources"], single_source_policy=False) for i, r in rows.items()
                                              if i in v2(rows)}
                                   for run_name, rows in (("k3b", k3b), ("b1", {i: b1[i] for i in k3b}))},
        "replay_mismatch": sorted(i for i in replayed if k3b[i]["top_chunk_ids"] != replay[i]["top_chunk_ids"]),
        "replayed": len(replayed),
        "contract_new_calls": {"calls": len(contracts), "violations": sum(c["contract_violation"] for c in contracts),
                               "ci95": clopper_pearson(sum(c["contract_violation"] for c in contracts), len(contracts)) if contracts else None},
        "usd": {"answer": sum(r["usd_answer"] for r in k3b.values()), "rerank_new": sum(r["usd_rerank"] for r in k3b.values()),
                "rerank_replayed_recorded": sum(r.get("replay_usd", 0.0) for r in k3b.values())},
    }


# ---------- Judge Claude: lô mù K3b-m + B1, ghép điểm ----------

def group_ids(group: str) -> set[int]:
    return set(json.loads(SPLIT_PATH.read_text(encoding="utf-8"))[group])


def pooled_items(group: str) -> tuple[list[dict], dict]:
    """Câu trả lời K3b-m + B1 của một nhóm; giống hệt chữ trong cùng câu chấm một lần; item là số mờ (như `r2.pooled_items`)."""
    by_case = {c["case_index"]: c for c in load_golden_cases("full")}
    wanted = group_ids(group)
    unique: dict[tuple[int, str], list] = defaultdict(list)
    for run_name in RUNS:
        for row in run_rows(run_name).values():
            if row["error"] is None and row["case_index"] in wanted:
                unique[(row["case_index"], row["answer"])].append((run_name, row["case_index"]))
    keys = sorted(unique)
    random.Random(SEED).shuffle(keys)
    items, mapping = [], {}
    for item, key in enumerate(keys, 1):
        case = by_case[key[0]]
        items.append({"case_index": item, "question": case["question"], "reference_answer": case["reference_answer"], "answer": key[1]})
        mapping[item] = unique[key]
    return items, mapping


def analyze(group: str) -> dict:
    """T3–T5, T7 và W1, W2, W4 (plan §2, §4) trên một nhóm. Kết luận do người đọc theo plan."""
    judge_dir = OUT_DIR / f"judge_{group}"
    mapping = json.loads((judge_dir / "map.json").read_text(encoding="utf-8"))["items"]
    scores = {r["case_index"]: r for r in read_scores(judge_dir, "scores")}
    runs = {run_name: run_rows(run_name) for run_name in RUNS}
    for item, pairs in mapping.items():
        for run_name, case in pairs:
            runs[run_name][case].update({m: scores[int(item)][m] for m in ANSWER_METRICS})
    k3b, b1 = runs["k3b"], runs["b1"]
    ids = [i for i in json.loads(SPLIT_PATH.read_text(encoding="utf-8"))[group] if i in k3b]
    main = sorted(r["case_index"] for r in g1_retrieval.keep_realism([b1[i] for i in ids], "main") if r["category"] != OUT_OF_SCOPE)
    out = {"group": group, "n": len(ids), "n_main": len(main)}
    for metric in ANSWER_METRICS:
        out[metric] = paired_stats([b1[i][metric] for i in main], [k3b[i][metric] for i in main], metric)
        out[f"{metric}_losses"] = sum(k3b[i][metric] < b1[i][metric] for i in main)          # T3 / T4
    out["T5_new_refusals_main"] = sorted(i for i in main if k3b[i]["refusal"] and not b1[i]["refusal"])
    out["false_refusal_watch"] = paired_stats([float(b1[i]["refusal"]) for i in main], [float(k3b[i]["refusal"]) for i in main], "false_refusal")
    called = [i for i in ids if k3b[i]["output_tokens"] is not None and b1[i]["output_tokens"] is not None]
    out["T7_output_tokens_ratio"] = sum(k3b[i]["output_tokens"] for i in called) / sum(b1[i]["output_tokens"] for i in called)
    won_main = [i for i in WON[group] if i in main]
    out["W1_won_main"] = {i: {m: [b1[i][m], k3b[i][m]] for m in ("completeness", "accuracy")} for i in won_main}
    out["W2_refusal_to_answer"] = [{"case_index": i, "uncited_sentences": uncited_sentences(k3b[i]["answer"])}
                                   for i in ids if b1[i]["refusal"] and not k3b[i]["refusal"]]
    out["W2_answer_to_refusal"] = sorted(i for i in ids if k3b[i]["refusal"] and not b1[i]["refusal"])
    out["T8_watch_120_168"] = {i: {"refusal": [b1[i]["refusal"], k3b[i]["refusal"]]} for i in WATCH_CASES if i in k3b}
    fresh = [k3b[i]["e2e_ms"] for i in ids if not k3b[i].get("replayed")]
    rng = np.random.default_rng(SEED)
    pct = lambda xs, q: [float(np.percentile(xs, q)),
                         [float(np.percentile([np.percentile(np.array(xs)[rng.integers(0, len(xs), len(xs))], q) for _ in range(10000)], p))
                          for p in (2.5, 97.5)]]
    usd_case = [k3b[i]["usd_answer"] + (k3b[i]["replay_usd"] if k3b[i].get("replayed") else k3b[i]["usd_rerank"]) for i in ids]
    out["W4"] = {"e2e_ms_fresh_p50": pct(fresh, 50), "e2e_ms_fresh_p95": pct(fresh, 95), "n_fresh": len(fresh),
                 "b1_answer_latency_p50_p95": [float(np.percentile([b1[i]["latency_ms"] for i in called], q)) for q in (50, 95)],
                 "usd_per_case_if_live": float(np.mean(usd_case)),
                 "usd_per_case_b1": float(np.mean([cost_usd(b1[i]["input_tokens"] or 0, b1[i]["output_tokens"] or 0) for i in ids]))}
    out["W4"]["usd_ratio"] = out["W4"]["usd_per_case_if_live"] / out["W4"]["usd_per_case_b1"]
    return out


def main() -> None:
    parser = argparse.ArgumentParser(prog="experiments.phase_8_2.k3b_answer")
    commands = parser.add_subparsers(dest="command", required=True)
    run_cmd = commands.add_parser("run", help="sinh câu trả lời K3b-m (paid: rerank mới + sinh)")
    run_cmd.add_argument("--cases", required=True, choices=["pilot", "rest", "test_pilot", "test_rest"])
    run_cmd.add_argument("--name", required=True)
    merge = commands.add_parser("merge", help="gộp phần thành answer_dev / answer_test")
    merge.add_argument("--parts", required=True, nargs="+")
    merge.add_argument("--name", required=True, choices=["answer_dev", "answer_test"])
    commands.add_parser("check", help="sàn + phát lại + hợp đồng + tiền (free)")
    export = commands.add_parser("export-judge", help="lô chấm mù K3b-m + B1 của một nhóm")
    export.add_argument("--group", required=True, choices=["dev", "test"])
    export.add_argument("--batch-size", type=int, default=25)
    check_judge = commands.add_parser("check-judge", help="đủ điểm, đúng schema")
    check_judge.add_argument("--group", required=True, choices=["dev", "test"])
    ana = commands.add_parser("analyze", help="T3–T5, T7, W1, W2, W4 (free)")
    ana.add_argument("--group", required=True, choices=["dev", "test"])
    args = parser.parse_args()

    if args.command == "run":
        result = asyncio.run(run(args.cases, args.name))
    elif args.command == "merge":
        rows = [r for part in args.parts for r in read_jsonl(OUT_DIR / f"{part}.jsonl")]
        if len({r["case_index"] for r in rows}) != len(rows):
            raise SystemExit("duplicated case_index across parts")
        write_jsonl(new_file(OUT_DIR / f"{args.name}.jsonl"), sorted(rows, key=lambda r: r["case_index"]))
        result = {"n": len(rows)}
    elif args.command == "check":
        result = check()
    elif args.command == "export-judge":
        judge_dir = OUT_DIR / f"judge_{args.group}"
        if judge_dir.exists():
            raise SystemExit(f"{judge_dir} exists")
        items, mapping = pooled_items(args.group)
        write_batches(judge_dir, items, args.batch_size)
        (judge_dir / "map.json").write_text(json.dumps({"runs": list(RUNS), "items": mapping}, indent=1) + "\n")
        result = {"items": len(items), "answers": sum(len(v) for v in mapping.values()), "batches": -(-len(items) // args.batch_size)}
    elif args.command == "check-judge":
        judge_dir = OUT_DIR / f"judge_{args.group}"
        items = {json.loads(l)["case_index"] for p in judge_dir.glob("batch_*.jsonl") for l in p.read_text().splitlines()}
        scores = read_scores(judge_dir, "scores")
        result = {"items": len(items), "score_errors": validate_score_rows(scores),
                  "scores_missing": sorted(items - {r["case_index"] for r in scores})}
    else:
        result = analyze(args.group)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
