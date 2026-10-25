"""Phase 8.1 G4 — xếp hạng lại (rerank) trên tập câu cố định, chỉ đọc.

Kế hoạch + tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` (bản duyệt
`a4adfc8eedd9`). Gọi code production qua tham số: `build_full_corpus_retrieval_service`, `CrossEncoderReranker`
(model_id, device, max_length), `FullCorpusContextBuilder`, `score_retrieval`. Logic biến thể chỉ có ở đây: đầu vào pool
100 (hợp hai nhánh native), "đoạn kèm mục". Không ghi Qdrant. Kết quả từng câu: JSONL private `data/phase_8_1/g4/`.

Chạy từ `backend/` (GPU: User giới hạn mỗi lượt một cấu hình, ≤ 30 câu):
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_rerank subset
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_rerank run --name a_m1_plain --cases dev30 \
      --input top10 --reranker m1 --text plain --device cuda
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_rerank compare --a base_runtime --b a_m1_plain \
      --metrics context5_gold_all mrr
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, ConfigDict

from evaluation.full_corpus_eval import (  # import này cũng đưa gốc repo + backend/ vào sys.path
    REPO_ROOT,
    build_context_builder,
    cost_usd,
    load_golden_cases,
    score_retrieval,
    split_group_indexes,
)
from core.schema import RetrievedDocument
from core.settings_loader import load_settings
from experiments.phase_8_1.g1_retrieval import (
    GOLD_PATH,
    SPLIT_PATH,
    compare,
    gold_coverage,
    keep_realism,
    load_gold,
    load_payloads,
    load_realism,
)
from reranking.cross_encoder import CrossEncoderReranker
from retrieval.full_corpus import build_full_corpus_retrieval_service, build_retrieved_document
from retrieval.full_corpus_context import FullCorpusContextBuilder

OUT_DIR = REPO_ROOT / "data/phase_8_1/g4"
SUBSET_PATH = OUT_DIR / "subset.json"
SEED = 20261024
TOP_K = 10
MAX_PAIR_TOKENS = 1024  # plan §1.4: cắt cặp (câu hỏi, đoạn) cùng mức cho M1/M2
MODELS = {"m1": "BAAI/bge-reranker-v2-m3", "m2": "AITeamVN/Vietnamese_Reranker"}
FIRST_CASE_LIMIT_S = 60  # plan §0: câu đo đầu > 60 s ⇒ bỏ cấu hình
RUN_LIMIT_S = 20 * 60  # plan §0: cả lượt > 20 phút ⇒ dừng
MAX_GPU_CASES = 30  # User: mỗi lượt GPU ≤ 30 câu
LUNA_INSTRUCTIONS = (
    "Bạn xếp hạng các đoạn văn theo mức hữu ích để trả lời câu hỏi của người dùng về du lịch và văn hóa Huế. "
    "Trả về danh sách số thứ tự của đủ mọi đoạn, mỗi số đúng một lần, đoạn hữu ích nhất đứng đầu."
)


class LunaRanking(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order: list[int]


def luna_rank(client: OpenAI, model: str, max_output_tokens: int, query: str, docs: list) -> dict:
    """Rerank listwise bằng gpt-6-luna (D12). Đầu ra sai (thiếu / lặp / id lạ / bị cắt / lỗi API) là lỗi kỹ thuật:
    trả `error`, không thay bằng thứ tự gốc, không gọi lại (plan §1.4 luna_output_rule)."""
    passages = "\n\n".join(f"[{n}] {d.text}" for n, d in enumerate(docs, 1))
    try:
        response = client.responses.parse(
            model=model, instructions=LUNA_INSTRUCTIONS, text_format=LunaRanking, store=False,
            max_output_tokens=max_output_tokens, input=f"Câu hỏi: {query}\n\nCác đoạn:\n{passages}")
    except OpenAIError as exc:
        return {"error": f"api: {type(exc).__name__}: {exc}"[:500]}
    usage = response.usage
    out = {"input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens,
           "usd": cost_usd(usage.input_tokens, usage.output_tokens), "raw": response.output_text,
           "status": response.status}
    parsed = response.output_parsed
    if response.status != "completed" or parsed is None:
        return {**out, "error": f"status {response.status}, parsed {parsed is not None}"}
    if sorted(parsed.order) != list(range(1, len(docs) + 1)):
        return {**out, "error": "order is not a permutation of 1..n"}
    return {**out, "order": parsed.order}


# ---------- Tập câu (plan §1.1) ----------

def make_subset() -> dict:
    cases = load_golden_cases("full")
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    gold, labels = load_gold(GOLD_PATH), load_realism()
    dev = set(split_group_indexes(split, "dev", cases))
    test = set(split_group_indexes(split, "test", cases))
    dev_main_gold = sorted(i for i in dev if i in gold and labels[i] != "unnatural")
    dev30 = sorted(random.Random(SEED).sample(dev_main_gold, 30))
    pilot = random.Random(SEED).sample(dev30, 10)  # giữ thứ tự rút: 5 câu đầu là tập CPU
    return {"seed": SEED, "dev_main_gold": len(dev_main_gold), "dev30": dev30, "pilot": pilot,
            "pilot_cpu": pilot[:5], "test15": sorted(i for i in test if i in gold)}


def load_cases(name: str) -> list[dict]:
    subset = json.loads(SUBSET_PATH.read_text(encoding="utf-8"))
    # dev30_rest: phần dev 30 ngoài pilot, để luna chạy pilot 10 câu trước rồi mới chạy tiếp (plan §0)
    wanted = [i for i in subset["dev30"] if i not in subset["pilot"]] if name == "dev30_rest" else subset[name]
    by_index = {c["case_index"]: c for c in load_golden_cases("full")}
    return [by_index[i] for i in wanted]


# ---------- Đầu vào, đơn vị chấm, context ----------

def section_texts(payloads: dict[str, dict]) -> dict[str, str]:
    """chunk_id → text cả mục chứa nó: các chunk cùng (source, heading_path) nối theo thứ tự trong file."""
    groups = defaultdict(list)
    for payload in payloads.values():
        order = int(payload["chunk_id"].rsplit("#", 1)[1])
        groups[(payload["source"], tuple(payload["heading_path"]))].append((order, payload))
    texts = {}
    for members in groups.values():
        members.sort(key=lambda item: item[0])
        joined = "\n\n".join(p["search_text"] for _, p in members)
        texts.update({p["chunk_id"]: joined for _, p in members})
    return texts


def packed_chunk_ids(documents: list[RetrievedDocument], packed_count: int) -> list[str]:
    """chunk_id của các nguồn trong context: builder bỏ đoạn không có bằng chứng và giữ thứ tự (C21 m1, C23 m4)."""
    kept = [d.id for d in documents if FullCorpusContextBuilder._source(d, 1) is not None]
    return kept[:packed_count]


def candidates(service, query: str, source: str, payload_by_point: dict[str, dict]) -> tuple[list, list]:
    """(đầu vào cho reranker, top-10 khi không rerank) theo đầu vào đã chọn."""
    result = service.search(query)
    if source == "top10":
        top = result.documents[:TOP_K]
        return top, top
    stages = result.trace.stages
    union = dict.fromkeys([e["point_id"] for e in stages["dense"]] + [e["point_id"] for e in stages["sparse"]])
    return [build_retrieved_document(payload_by_point[pid], 0.0) for pid in union], result.documents[:TOP_K]


# ---------- Kiểm GPU (plan §0, 4 điều) ----------

def gpu_check(reranker: CrossEncoderReranker) -> dict:
    apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader"],
                          capture_output=True, text=True, check=True).stdout.split()
    used = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                          capture_output=True, text=True, check=True).stdout.strip()
    check = {"cuda_available": torch.cuda.is_available(), "model_device": reranker.loaded_device,
             "gpu_pids": apps, "own_pid": str(os.getpid()), "memory_used_mib": int(used)}
    ok = (check["cuda_available"] and check["model_device"].startswith("cuda")
          and check["own_pid"] in apps and len(apps) == 1)
    if not ok:
        raise SystemExit(f"GPU check failed, stop (plan §0): {check}")
    return check


# ---------- Chạy một cấu hình ----------

def run_config(args) -> tuple[list[dict], dict]:
    cases = load_cases(args.cases)
    if args.reranker != "none" and args.device == "cuda" and len(cases) > MAX_GPU_CASES:
        raise SystemExit(f"GPU run limited to {MAX_GPU_CASES} cases")
    settings = load_settings(validate_private_paths=False)
    treatment, pool = ("dense_bm25_rrf", 30) if args.input == "top10" else ("native_hybrid_rrf", 100)
    service = build_full_corpus_retrieval_service("e5-small-384", treatment, settings=settings, candidate_pool=pool)
    context_builder = build_context_builder(settings)
    gold = load_gold(GOLD_PATH)
    meta = {"name": args.name, "cases": args.cases, "input": args.input, "reranker": args.reranker,
            "text": args.text, "device": args.device, "treatment": treatment, "pool": pool,
            "started": time.strftime("%Y-%m-%d %H:%M:%S %z")}
    reranker = luna = None
    if args.reranker == "luna":
        generation = settings["full_corpus_generation"]
        luna = OpenAI(api_key=os.environ[generation["api_key_env"]], timeout=generation["timeout_seconds"], max_retries=0)
        meta.update({"model_id": generation["model"], "max_output_tokens": generation["answer_max_output_tokens"]})
    elif args.reranker != "none":
        reranker = CrossEncoderReranker(MODELS[args.reranker], device=args.device, max_length=MAX_PAIR_TOKENS)
        load_start = time.perf_counter()
        reranker.warm_up()
        meta.update({"model_id": MODELS[args.reranker], "load_ms": (time.perf_counter() - load_start) * 1000,
                     "tokenizer_model_max_length": reranker.load()._model.tokenizer.model_max_length,
                     "max_length": reranker.max_length})
        if args.device == "cuda":
            meta["gpu_check"] = gpu_check(reranker)
    rows = []
    try:
        payload_by_point = load_payloads(service.client, service.candidate.collection_name)
        payload_by_chunk = {p["chunk_id"]: p for p in payload_by_point.values()}
        sections = section_texts(payload_by_point) if args.text == "section" else None

        def one_case(case: dict) -> dict:
            query = case["question"]
            t0 = time.perf_counter()
            pool_docs, top_plain = candidates(service, query, args.input, payload_by_point)
            t1 = time.perf_counter()
            luna_out = None
            if args.reranker == "none":
                top = top_plain
            elif luna is not None:
                luna_out = luna_rank(luna, meta["model_id"], meta["max_output_tokens"], query, pool_docs)
                if "error" in luna_out:
                    return {"case_index": case["case_index"], "category": case["category"], "config": args.name,
                            "luna": luna_out, "rerank_ms": (time.perf_counter() - t1) * 1000}
                top = [pool_docs[n - 1] for n in luna_out["order"]][:TOP_K]
            else:
                scoring = pool_docs if sections is None else [
                    RetrievedDocument(id=d.id, score=d.score, text=sections[d.id], metadata=d.metadata)
                    for d in pool_docs]
                scores = reranker.score_documents(query, scoring)
                # cùng luật phá hòa như CrossEncoderReranker.rerank: điểm giảm dần, rồi chunk_id
                top = [d for _, d in sorted(zip(scores, pool_docs), key=lambda x: (-x[0], x[1].id))][:TOP_K]
            t2 = time.perf_counter()
            packed = context_builder.build(query, top)
            t3 = time.perf_counter()
            context_ids = packed_chunk_ids(top, len(packed.sources))
            row = {"case_index": case["case_index"], "category": case["category"], "config": args.name,
                   "top_chunk_ids": [d.id for d in top], "context_chunk_ids": context_ids,
                   "retrieval_ms": (t1 - t0) * 1000, "rerank_ms": (t2 - t1) * 1000,
                   "context_ms": (t3 - t2) * 1000, "total_ms": (t3 - t0) * 1000,
                   **score_retrieval(case["keywords"], [d.text for d in top])}
            if luna_out is not None:
                row["luna"] = luna_out
            facts = gold.get(case["case_index"])
            if facts:
                layers = {"input": [d.id for d in pool_docs], "top10": row["top_chunk_ids"], "context5": context_ids}
                for layer, ids in layers.items():
                    coverage = gold_coverage(facts, [payload_by_chunk[i] for i in ids])
                    row[f"{layer}_gold_all"], row[f"{layer}_gold_frac"] = coverage["all"], coverage["frac"]
            return row

        if luna is None:
            one_case(cases[0])  # câu khởi động: không tính (plan §1.3); luna gọi API, không cần (và tốn tiền)
        run_start = time.perf_counter()
        for position, case in enumerate(cases):
            row = one_case(case)
            rows.append(row)
            if position == 0 and row.get("total_ms", 0) > FIRST_CASE_LIMIT_S * 1000:
                meta["stopped"] = f"first measured case {row['total_ms']:.0f} ms > {FIRST_CASE_LIMIT_S} s"
                break
            if time.perf_counter() - run_start > RUN_LIMIT_S:
                meta["stopped"] = f"run longer than {RUN_LIMIT_S} s after {len(rows)} cases"
                break
    finally:
        service.close()
    meta["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    meta["n"] = len(rows)
    if luna is not None:
        calls = [r["luna"] for r in rows]
        meta["luna_errors"] = sum("error" in c for c in calls)
        meta["usage"] = {k: sum(c.get(k, 0) for c in calls) for k in ("input_tokens", "output_tokens", "usd")}
    return rows, meta


# ---------- Phân tích ----------

def latency(rows: list[dict]) -> dict:
    rows = [r for r in rows if "total_ms" in r]  # câu luna lỗi không có số đo
    return {key: {"p50": float(np.percentile([r[key] for r in rows], 50)),
                  "p95": float(np.percentile([r[key] for r in rows], 95))}
            for key in ("total_ms", "retrieval_ms", "rerank_ms", "context_ms")} if rows else {}


def table(rows: list[dict]) -> dict:
    keys = ("context5_gold_all", "context5_gold_frac", "top10_gold_all", "input_gold_all", "mrr", "ndcg")
    return {"n": len(rows), **{k: float(np.mean([r[k] for r in rows if k in r])) for k in keys}}


def _read(name: str) -> list[dict]:
    return [json.loads(line) for line in (OUT_DIR / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8.1 G4 rerank (read-only, GPU free)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("subset", help="ghi data/phase_8_1/g4/subset.json (plan §1.1)")
    run = commands.add_parser("run")
    run.add_argument("--name", required=True, help="tên cấu hình = tên file JSONL trong data/phase_8_1/g4/")
    run.add_argument("--cases", required=True, choices=["dev30", "dev30_rest", "pilot", "pilot_cpu", "test15"])
    run.add_argument("--input", required=True, choices=["top10", "pool100"])
    run.add_argument("--reranker", required=True, choices=["none", "m1", "m2", "luna"])
    run.add_argument("--text", default="plain", choices=["plain", "section"])
    run.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    cmp = commands.add_parser("compare")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True, nargs="+")
    cmp.add_argument("--metrics", required=True, nargs="+")
    cmp.add_argument("--realism", choices=["main", "natural"])
    summary = commands.add_parser("summary", help="trung bình metric + latency theo cấu hình")
    summary.add_argument("--names", required=True, nargs="+")
    summary.add_argument("--realism", choices=["main", "natural"])
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.command == "subset":
        if SUBSET_PATH.exists():
            raise SystemExit(f"{SUBSET_PATH} exists; subset is fixed once")
        SUBSET_PATH.write_text(json.dumps(make_subset(), indent=2) + "\n", encoding="utf-8")
        print(SUBSET_PATH, hashlib.sha256(SUBSET_PATH.read_bytes()).hexdigest()[:12])
    elif args.command == "run":
        out = OUT_DIR / f"{args.name}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists; choose a new --name")
        rows, meta = run_config(args)
        out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
        meta["latency"] = latency(rows)
        (OUT_DIR / f"{args.name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                                        encoding="utf-8")
        print(json.dumps({"meta": meta, "summary": table(rows)}, ensure_ascii=False, indent=2))
    elif args.command == "compare":
        a_rows = keep_realism(_read(args.a), args.realism)
        print(json.dumps(compare(a_rows, {n: _read(n) for n in args.b}, args.metrics), ensure_ascii=False, indent=2))
    else:
        out = {}
        for name in args.names:
            rows = keep_realism(_read(name), args.realism)
            meta_path = OUT_DIR / f"{name}.meta.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
            out[name] = {**table(rows), "latency": latency(rows), "stopped": meta.get("stopped")}
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
