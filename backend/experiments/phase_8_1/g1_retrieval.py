"""Phase 8.1 G1 — chẩn đoán retrieval chỉ đọc trên index hiện tại.

Kế hoạch + tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_plan.md`.
Gọi code production qua tham số (B11/B13): `build_full_corpus_retrieval_service`, `FullCorpusContextBuilder`,
`score_retrieval`, bootstrap của evaluator. Logic biến thể chỉ có ở đây: DBSF, biến đổi dạng câu hỏi.
Không ghi Qdrant, không gọi API trả phí. Kết quả từng câu ghi JSONL private (`data/phase_8_1/g1/`).

Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g1_retrieval run --name runtime --group dev
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g1_retrieval compare --a runtime --b native_p30 \
      --metrics top10_gold_all mrr
"""
import argparse
import json
import random
import re
import statistics
import unicodedata
from functools import lru_cache
from pathlib import Path

import numpy as np
from qdrant_client import models

from evaluation.full_corpus_eval import (
    BOOTSTRAP_ROUNDS,
    BOOTSTRAP_SEED,
    OUT_OF_SCOPE,
    REPO_ROOT,
    bootstrap_mean_diff,
    build_context_builder,
    holm_adjust,
    load_golden_cases,
    score_retrieval,
    split_group_indexes,
    verdict,
)
from core.settings_loader import load_settings
from embedding.sparse import encode_sparse_query
from reranking.cross_encoder import CrossEncoderReranker
from retrieval.full_corpus import build_full_corpus_retrieval_service, build_retrieved_document

SPLIT_PATH = REPO_ROOT / "knowledge-base-hue/evaluation/phase_8_1/split.json"
KB_ROOT = REPO_ROOT / "knowledge-base-hue"
# Nhãn đoạn đúng bản 4 (đợt sửa kho 28/10: v3 tìm lại nguyên văn trong kho đã sửa + 2 trích dẫn User duyệt). Bản 1 `gold_draft.jsonl` (sha bab707b9ab22)
# giữ nguyên vì manifest G0.6 khóa nó; bản 2 `gold_v2.jsonl` (sha 2f5a347a71ff) và bản 3 `gold_v3.jsonl` (sha 3b1117cf59e9, vị trí theo kho trước sửa) giữ nguyên
# để tái lập số đo cũ.
GOLD_PATH = REPO_ROOT / "data/phase_8_1/gold/gold_v4.jsonl"
OUT_DIR = REPO_ROOT / "data/phase_8_1/g1"
REALISM_PATH = REPO_ROOT / "data/phase_8_1/golden_realism_final.jsonl"  # 2 agent độc lập + User (A, 21:58)
ANSWERS_7B_PATH = REPO_ROOT / "data/evaluation/phase_7b/run1_answers.jsonl"
PILOT_SEED = 20261024
TOP_K = 10


# ---------- Đoạn đúng (gold) ----------

def load_gold(path: Path) -> dict[int, list[list[tuple[str, int, int]]]]:
    """case_index → danh sách fact; mỗi fact là danh sách trích dẫn (source, start, end)."""
    gold = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        evidence = row["evidence"]
        gold[row["case_index"]] = [
            [(evidence[k]["source"], evidence[k]["start"], evidence[k]["end"]) for k in fact["quote_ids"]]
            for fact in row["required_facts"]
        ]
    return gold


@lru_cache(maxsize=None)
def source_text(source: str) -> str:
    """Văn bản file kho theo đúng cách nhãn tính offset (`data/phase_8_1/tools/validate_gold.py`: CRLF → LF)."""
    return (KB_ROOT / source).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def quote_is_chunk_heading(payload: dict, quote_text: str) -> bool:
    """Trích dẫn là một dòng tiêu đề Markdown mà chunk mang trong `heading_path`: model thấy tiêu đề đó trong context dù
    `evidence_parts` chỉ là thân đoạn (ca 143; User duyệt đếm tiêu đề mục 27/10)."""
    return quote_text.startswith("#") and quote_text.lstrip("#").strip() in payload["heading_path"]


def chunk_hits_quote(payload: dict, quote: tuple[str, int, int]) -> bool:
    """Chunk trúng trích dẫn: cùng file và (một evidence_part giao khoảng [start, end) của trích dẫn, hoặc trích dẫn là dòng tiêu đề
    nằm trong heading_path của chunk)."""
    source, start, end = quote
    if payload["source"] != source:
        return False
    if any(part["start"] < end and start < part["end"] for part in payload["evidence_parts"]):
        return True
    return quote_is_chunk_heading(payload, source_text(source)[start:end])


def gold_coverage(facts: list[list[tuple[str, int, int]]], payloads: list[dict]) -> dict:
    """gold_all: mọi fact có ≥1 trích dẫn trúng; gold_frac: tỉ lệ fact được phủ."""
    covered = [any(chunk_hits_quote(p, q) for q in fact for p in payloads) for fact in facts]
    return {"all": float(all(covered)), "frac": sum(covered) / len(covered)}


# ---------- Biến đổi dạng câu hỏi (G1.4) ----------

_TONE_PAIRS = {  # dấu đặt ở nguyên âm đầu ⇄ nguyên âm sau trong oa/oe/uy (kiểu cũ ⇄ kiểu mới)
    f"{first}{second}": f"{base}{toned}"
    for base, second, tones in (("o", "a", "àáảãạ"), ("o", "e", "èéẻẽẹ"), ("u", "y", "ỳýỷỹỵ"))
    for first, toned in zip({"o": "òóỏõọ", "u": "ùúủũụ"}[base], tones)
}
_TONE_PAIRS.update({new: old for old, new in list(_TONE_PAIRS.items())})
_TONE_RE = re.compile("(?<![qQ])(" + "|".join(map(re.escape, _TONE_PAIRS)) + ")")


def transform_query(query: str, form: str) -> str:
    if form == "orig":
        return query
    if form == "nfd":
        return unicodedata.normalize("NFD", query)
    if form == "noaccent":
        stripped = "".join(ch for ch in unicodedata.normalize("NFD", query) if not unicodedata.combining(ch))
        return stripped.replace("đ", "d").replace("Đ", "D")
    if form == "tone_swap":
        return _TONE_RE.sub(lambda m: _TONE_PAIRS[m.group(1)], unicodedata.normalize("NFC", query))
    raise ValueError(f"unknown query form: {form}")


# ---------- DBSF (G1.3, logic biến thể) ----------

def dbsf_scores(stage: list[dict]) -> dict[str, float]:
    """Distribution-based score fusion: chuẩn hóa điểm một nhánh theo [mean − 3σ, mean + 3σ], cắt về [0, 1]."""
    if not stage:
        return {}
    scores = [entry["score"] for entry in stage]
    mean, std = statistics.fmean(scores), statistics.pstdev(scores)
    if std == 0:
        return {entry["point_id"]: 0.5 for entry in stage}
    low, high = mean - 3 * std, mean + 3 * std
    return {entry["point_id"]: min(1.0, max(0.0, (entry["score"] - low) / (high - low))) for entry in stage}


def dbsf_rank(dense_stage: list[dict], sparse_stage: list[dict], sparse_weight: float) -> list[str]:
    dense, sparse = dbsf_scores(dense_stage), dbsf_scores(sparse_stage)
    fused = {pid: (1 - sparse_weight) * dense.get(pid, 0.0) + sparse_weight * sparse.get(pid, 0.0)
             for pid in dense.keys() | sparse.keys()}
    return [pid for pid, _ in sorted(fused.items(), key=lambda item: (-item[1], item[0]))]


# ---------- Chạy một cấu hình ----------

def load_payloads(client, collection: str) -> dict[str, dict]:
    """point_id → payload của toàn collection (scroll chỉ đọc), để chấm đoạn đúng cho mọi tầng."""
    payloads, offset = {}, None
    while True:
        points, offset = client.scroll(collection, limit=1000, offset=offset, with_payload=True, with_vectors=False)
        payloads.update({str(p.id): p.payload for p in points})
        if offset is None:
            return payloads


def select_cases(group: str, pilot: int | None) -> list[dict]:
    cases = load_golden_cases("full")
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    wanted = set(split_group_indexes(split, group, cases)) if group != "all" else {c["case_index"] for c in cases}
    selected = [c for c in cases if c["case_index"] in wanted and c["category"] != OUT_OF_SCOPE]
    if pilot:
        gold = load_gold(GOLD_PATH)
        selected = random.Random(PILOT_SEED).sample([c for c in selected if c["case_index"] in gold], pilot)
    return selected


def sparse_boundary_tie(service, query: str, pool: int) -> bool:
    """Điểm sparse hạng `pool` bằng điểm hạng `pool + 1` (tập ứng viên phụ thuộc cách cắt khi hòa điểm)."""
    sparse_q = encode_sparse_query(query, service.sparse_state)
    if not sparse_q.indices:
        return False
    points = service.client.query_points(
        collection_name=service.candidate.collection_name,
        query=models.SparseVector(indices=list(sparse_q.indices), values=list(sparse_q.values)),
        using="sparse", limit=pool + 1, with_payload=False, with_vectors=False,
    ).points
    return len(points) == pool + 1 and points[pool - 1].score == points[pool].score


def run_config(args) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    treatment = "native_hybrid_rrf" if args.fusion == "dbsf" else args.treatment
    service = build_full_corpus_retrieval_service(
        "e5-small-384", treatment, settings=settings, candidate_pool=args.pool, rrf_k=args.rrf_k,
        search_params=models.SearchParams(exact=True) if args.exact else None,
    )
    context_builder = build_context_builder(settings)
    minilm = CrossEncoderReranker() if args.minilm else None
    gold = load_gold(GOLD_PATH)
    rows = []
    try:
        payloads = load_payloads(service.client, service.candidate.collection_name)
        for case in select_cases(args.group, args.pilot):
            query = transform_query(case["question"], args.query_form)
            if args.nfc:
                query = unicodedata.normalize("NFC", query)
            result = service.search(query)
            stages = result.trace.stages
            if args.fusion == "dbsf":
                ranked = dbsf_rank(stages["dense"], stages.get("sparse", []), args.sparse_weight)[:TOP_K]
                documents = [build_retrieved_document(payloads[pid], 0.0) for pid in ranked]
                top_ids = ranked
            else:
                documents = result.documents[:TOP_K]
                top_ids = [entry["point_id"] for entry in stages["rrf"][:TOP_K]]
            packed = context_builder.build(query, documents)
            context_ids = top_ids[: len(packed.sources)]
            pool_ids = {
                "dense": [e["point_id"] for e in stages["dense"]],
                "sparse": [e["point_id"] for e in stages.get("sparse", stages.get("bm25", []))],
            }
            pool_ids["union"] = list(dict.fromkeys(pool_ids["dense"] + pool_ids["sparse"]))
            row = {
                "case_index": case["case_index"], "category": case["category"], "config": args.name,
                "top_chunk_ids": [payloads[pid]["chunk_id"] for pid in top_ids],
                "dense_chunk_ids": [e["chunk_id"] for e in stages["dense"]],
                "context_chunk_ids": [payloads[pid]["chunk_id"] for pid in context_ids],
                "dense_ms": result.trace.timings_ms.get("dense_ms"),
                **score_retrieval(case["keywords"], [d.text for d in documents]),
            }
            if treatment == "native_hybrid_rrf":
                row["sparse_boundary_tie"] = sparse_boundary_tie(service, query, args.pool)
            if minilm is not None:
                row["minilm_overlength"] = any(
                    minilm.input_token_count(query, payloads[e["point_id"]]["search_text"]) > minilm.max_length
                    for e in stages["rrf"]
                )
            facts = gold.get(case["case_index"])
            if facts:
                layers = {f"pool_{k}": v for k, v in pool_ids.items()}
                layers.update({"top10": top_ids, "context5": context_ids})
                for layer, ids in layers.items():
                    coverage = gold_coverage(facts, [payloads[pid] for pid in ids])
                    row[f"{layer}_gold_all"], row[f"{layer}_gold_frac"] = coverage["all"], coverage["frac"]
            rows.append(row)
    finally:
        service.close()
    return rows


# ---------- Phân tích ----------

def load_realism() -> dict[int, str]:
    """case_index → natural / capability_only / unnatural / disputed_unnatural; rỗng khi chưa có file nhãn."""
    if not REALISM_PATH.is_file():
        return {}
    rows = [json.loads(line) for line in REALISM_PATH.read_text(encoding="utf-8").splitlines()]
    return {row["case_index"]: row["realism"] for row in rows}


def keep_realism(rows: list[dict], realism: str | None) -> list[dict]:
    if realism is None:
        return rows
    labels = load_realism()
    if not labels:
        raise ValueError(f"realism labels not found: {REALISM_PATH}")
    if realism == "main":  # số chính (User 21:58): bỏ câu không tự nhiên; câu đang tranh chấp tạm tính vào
        return [r for r in rows if labels.get(r["case_index"]) != "unnatural"]
    return [r for r in rows if labels.get(r["case_index"]) == realism]


def compare(a_rows: list[dict], variants: dict[str, list[dict]], metrics: list[str]) -> dict:
    """Chênh B − A trên câu cả hai có metric; CI bootstrap + thắng/hòa/thua; Holm khi > 1 biến thể."""
    a = {r["case_index"]: r for r in a_rows}
    result = {}
    for metric in metrics:
        per_variant = {}
        for name, rows in variants.items():
            b = {r["case_index"]: r for r in rows}
            common = sorted(i for i in a if i in b and metric in a[i] and metric in b[i])
            diffs = np.array([b[i][metric] - a[i][metric] for i in common], dtype=float)
            if not len(diffs):
                continue
            stats = bootstrap_mean_diff(diffs, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)
            per_variant[name] = {
                "n": len(diffs), "mean_a": float(np.mean([a[i][metric] for i in common])),
                "mean_b": float(np.mean([b[i][metric] for i in common])), "mean_diff": float(diffs.mean()),
                **stats, "wins": int((diffs > 0).sum()), "ties": int((diffs == 0).sum()),
                "losses": int((diffs < 0).sum()), "verdict": verdict(metric, stats["ci95"]),
            }
        if len(per_variant) > 1:
            names = list(per_variant)
            for name, p_holm in zip(names, holm_adjust([per_variant[n]["p_value"] for n in names])):
                per_variant[name]["p_holm"] = p_holm
                per_variant[name]["verdict_holm"] = per_variant[name]["verdict"] if p_holm < 0.05 else "no_difference"
        result[metric] = per_variant
    return result


def overlap(a_rows: list[dict], b_rows: list[dict]) -> dict:
    """G1.2: trùng top-10 và top-30 dense giữa hai cấu hình (Jaccard theo câu) + latency dense."""
    b = {r["case_index"]: r for r in b_rows}
    jac = lambda x, y: len(set(x) & set(y)) / len(set(x) | set(y)) if x or y else 1.0
    pairs = [(r, b[r["case_index"]]) for r in a_rows if r["case_index"] in b]
    latency = lambda rows: {"p50": float(np.percentile([r["dense_ms"] for r in rows], 50)),
                            "p95": float(np.percentile([r["dense_ms"] for r in rows], 95))}
    return {
        "n": len(pairs),
        "top10_identical": sum(x["top_chunk_ids"] == y["top_chunk_ids"] for x, y in pairs),
        "top10_jaccard_mean": statistics.fmean(jac(x["top_chunk_ids"], y["top_chunk_ids"]) for x, y in pairs),
        "dense30_identical_set": sum(set(x["dense_chunk_ids"]) == set(y["dense_chunk_ids"]) for x, y in pairs),
        "dense30_jaccard_mean": statistics.fmean(jac(x["dense_chunk_ids"], y["dense_chunk_ids"]) for x, y in pairs),
        "dense_ms_a": latency([x for x, _ in pairs]), "dense_ms_b": latency([y for _, y in pairs]),
    }


def failure_layers(rows: list[dict]) -> dict:
    """G1.6 (4 tầng tự động + từ chối 7B Run 1): tầng đầu tiên mà chưa đủ mọi fact, theo câu."""
    answers = {json.loads(line)["case_index"]: json.loads(line)
               for line in ANSWERS_7B_PATH.read_text(encoding="utf-8").splitlines()}
    layers = ("pool_union", "top10", "context5")
    per_case = {}
    for r in rows:
        if "top10_gold_all" not in r:
            continue
        first = next((layer for layer in layers if r[f"{layer}_gold_all"] < 1), None)
        refused = bool(answers[r["case_index"]]["refusal"])
        per_case[r["case_index"]] = first or ("answer_refused" if refused else "reached_answer")
    counts: dict[str, int] = {}
    for label in per_case.values():
        counts[label] = counts.get(label, 0) + 1
    return {"n": len(per_case), "first_failing_layer": counts, "per_case": per_case}


def summarize(rows: list[dict]) -> dict:
    keys = sorted({k for r in rows for k, v in r.items() if isinstance(v, (int, float)) and k != "case_index"})
    return {"n": len(rows), **{k: statistics.fmean(r[k] for r in rows if k in r) for k in keys
                               if any(k in r for r in rows)}}


def _read(name: str) -> list[dict]:
    path = OUT_DIR / f"{name}.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8.1 G1 retrieval diagnostics (read-only, free)")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--name", required=True, help="tên cấu hình = tên file JSONL trong data/phase_8_1/g1/")
    run.add_argument("--group", default="dev", choices=["dev", "test", "all"])
    run.add_argument("--pilot", type=int, help="chỉ N câu dev có đoạn đúng, chọn theo seed cố định")
    run.add_argument("--treatment", default="dense_bm25_rrf", choices=["dense_bm25_rrf", "native_hybrid_rrf"])
    run.add_argument("--pool", type=int, default=30)
    run.add_argument("--rrf-k", type=int, default=60)
    run.add_argument("--exact", action="store_true")
    run.add_argument("--fusion", default="rrf", choices=["rrf", "dbsf"])
    run.add_argument("--sparse-weight", type=float, default=0.3)
    run.add_argument("--query-form", default="orig", choices=["orig", "nfd", "noaccent", "tone_swap"])
    run.add_argument("--nfc", action="store_true")
    run.add_argument("--minilm", action="store_true", help="đếm cặp vượt max_length MiniLM (G1.5)")
    cmp = commands.add_parser("compare")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True, nargs="+")
    cmp.add_argument("--metrics", required=True, nargs="+")
    cmp.add_argument("--realism", choices=["main", "natural", "capability_only", "unnatural"])
    table = commands.add_parser("table", help="trung bình metric theo cấu hình (tổng + theo loại câu)")
    table.add_argument("--names", required=True, nargs="+")
    table.add_argument("--realism", choices=["main", "natural", "capability_only", "unnatural"])
    ovl = commands.add_parser("overlap", help="G1.2: trùng kết quả + latency giữa hai cấu hình")
    ovl.add_argument("--a", required=True)
    ovl.add_argument("--b", required=True)
    lay = commands.add_parser("layers", help="G1.6: tầng lỗi đầu tiên của câu có đoạn đúng")
    lay.add_argument("--name", required=True)
    args = parser.parse_args()

    if args.command == "run":
        rows = run_config(args)
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"{args.name}.jsonl"
        out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
        print(json.dumps(summarize(rows), ensure_ascii=False, indent=2))
    elif args.command == "compare":
        a_rows = keep_realism(_read(args.a), args.realism)
        print(json.dumps(compare(a_rows, {n: _read(n) for n in args.b}, args.metrics), ensure_ascii=False, indent=2))
    elif args.command == "table":
        out = {}
        for name in args.names:
            rows = keep_realism(_read(name), args.realism)
            categories = sorted({r["category"] for r in rows})
            out[name] = {"all": summarize(rows),
                         **{c: summarize([r for r in rows if r["category"] == c]) for c in categories}}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.command == "overlap":
        print(json.dumps(overlap(_read(args.a), _read(args.b)), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(failure_layers(_read(args.name)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
