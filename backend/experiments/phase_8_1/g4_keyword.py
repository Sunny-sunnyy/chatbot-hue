"""Phase 8.1 G4 phần từ khóa — BM25 trong bộ nhớ với cách tách từ / khử dấu / k1, b, k RRF khác nhau; chỉ đọc.

Kế hoạch + tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_keyword_plan.md`. Nhánh dense chạy
một lần mỗi dạng câu hỏi (Qdrant chỉ đọc, lưu top-100); nhánh BM25 tính trong bộ nhớ trên `search_text` của 8.459 đoạn,
công thức chép đúng `embedding/sparse.py` (`fit_sparse_state`, `encode_sparse_document`, `encode_sparse_query`) nhưng có
tham số tách từ / k1 / b. Trộn bằng `reciprocal_rank_fusion` production, context bằng `FullCorpusContextBuilder`.
Không tạo / ghi collection, không gọi API trả phí. Kết quả: JSONL private `data/phase_8_1/g4k/`.

Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_keyword dense --form orig
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_keyword gate
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_keyword run --name n0 --fusion native --tokenizer syllable
"""
import argparse
import json
import math
import random
import re
import time
from collections import Counter, defaultdict

from evaluation.full_corpus_eval import REPO_ROOT, build_context_builder, score_retrieval  # đưa gốc repo vào sys.path
from core.settings_loader import load_settings
from embedding.sparse import encode_sparse_document, encode_sparse_query
from experiments.phase_8_1.g1_retrieval import (
    GOLD_PATH,
    compare,
    gold_coverage,
    holm_adjust,
    keep_realism,
    load_gold,
    load_payloads,
    select_cases,
    transform_query,
)
from experiments.phase_8_1.g4_rerank import packed_chunk_ids
from retrieval.full_corpus import (
    build_full_corpus_retrieval_service,
    build_retrieved_document,
    compute_sparse_dot_product,
    rank_positive_bm25,
    reciprocal_rank_fusion,
)
from scoring.bm25 import B, K1, tokenize

OUT_DIR = REPO_ROOT / "data/phase_8_1/g4k"
G1_DIR = REPO_ROOT / "data/phase_8_1/g1"
SEED = 20261024
TOP_K = 10
DENSE_POOL = 100
RUNTIME_POOL = 30


# ---------- Cách tách từ (plan §3) ----------

_PUNCT_SPLIT = re.compile(r"[.,;:!?()\[\]\"“”\n]")
_CODE = re.compile(r"\S*\d\S*")
_EDGE_PUNCT = re.compile(r"^\W+|\W+$")


def tokenize_bigram(text: str) -> list[str]:
    """Âm tiết + cặp âm tiết liền nhau trong cùng đoạn chữ không bị ngắt bởi dấu câu."""
    tokens = tokenize(text)
    for segment in _PUNCT_SPLIT.split(text):
        syllables = tokenize(segment)
        tokens += [f"{a}_{b}" for a, b in zip(syllables, syllables[1:])]
    return tokens


def tokenize_codes(text: str) -> list[str]:
    """Âm tiết + mỗi chuỗi không khoảng trắng có chữ số (bỏ dấu câu hai đầu) thành một từ riêng."""
    codes = [_EDGE_PUNCT.sub("", m.group(0)).lower() for m in _CODE.finditer(text)]
    return tokenize(text) + [c for c in codes if c]


def tokenize_pyvi(text: str) -> list[str]:
    """Tách từ `pyvi` (từ ghép nối bằng "_"), thay cho âm tiết."""
    from pyvi import ViTokenizer  # import muộn: chỉ biến thể này cần
    return [piece.lower() for piece in ViTokenizer.tokenize(text).split() if re.search(r"\w", piece)]


def tokenize_deaccent(text: str) -> list[str]:
    """Khử dấu (như `transform_query(…, "noaccent")` của G1) rồi tách âm tiết."""
    return tokenize(transform_query(text, "noaccent"))


TOKENIZERS = {"syllable": tokenize, "bigram": tokenize_bigram, "codes": tokenize_codes, "pyvi": tokenize_pyvi,
              "deaccent": tokenize_deaccent}


# ---------- BM25 trong bộ nhớ ----------

class MemoryBM25:
    """Chỉ mục ngược: term → [(point_id, trọng số BM25 của term trong đoạn)].

    Trọng số và idf tính đúng thứ tự phép toán của `fit_sparse_state` / `encode_sparse_document`; điểm một đoạn = tổng
    trọng số các term của câu hỏi có trong đoạn, cộng theo thứ tự term tăng dần (= thứ tự chỉ số từ vựng production) để
    tái lập cả phần làm tròn số thực."""

    def __init__(self, texts: dict[str, str], tokenizer, k1: float = K1, b: float = B):
        self.tokenizer = tokenizer
        counts = {pid: Counter(tokenizer(text)) for pid, text in texts.items()}
        counts = {pid: c for pid, c in counts.items() if c}
        lengths = {pid: sum(c.values()) for pid, c in counts.items()}
        num_docs = len(counts)
        avgdl = sum(lengths.values()) / num_docs
        df = Counter(term for c in counts.values() for term in c)
        self.idf = {t: math.log((num_docs - n + 0.5) / (n + 0.5) + 1.0) for t, n in df.items()}
        self.num_docs, self.avgdl, self.k1, self.b = num_docs, avgdl, k1, b
        self.postings: dict[str, list[tuple[str, float]]] = defaultdict(list)
        for pid, c in counts.items():
            for term, tf in c.items():
                denominator = tf + k1 * (1.0 - b + b * lengths[pid] / avgdl)
                self.postings[term].append((pid, self.idf[term] * (tf * (k1 + 1.0)) / denominator))
        self.weights = {pid: {} for pid in counts}
        for term, plist in self.postings.items():
            for pid, w in plist:
                self.weights[pid][term] = w

    def query_terms(self, query: str) -> list[str]:
        return sorted({t for t in self.tokenizer(query) if t in self.idf})

    def scores(self, query: str, pids=None) -> dict[str, float]:
        """Điểm mọi đoạn có ≥ 1 term chung (`pids` = None) hoặc của đúng tập `pids`."""
        terms = self.query_terms(query)
        if pids is not None:
            return {pid: float(sum(self.weights.get(pid, {}).get(t, 0.0) for t in terms if t in self.weights.get(pid, {})))
                    for pid in pids}
        total: dict[str, float] = defaultdict(float)
        for term in terms:
            for pid, w in self.postings[term]:
                total[pid] += w
        return dict(total)


# ---------- Nhánh dense (chạy một lần mỗi dạng câu hỏi) ----------

def dense_path(form: str):
    return OUT_DIR / f"dense_{form}.jsonl"


def run_dense(form: str) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    service = build_full_corpus_retrieval_service("e5-small-384", "native_hybrid_rrf", settings=settings,
                                                  candidate_pool=DENSE_POOL)
    rows = []
    try:
        for case in select_cases("dev", None):
            query = transform_query(case["question"], form)
            vector = service.dense_runner.embed_queries([query])[0]
            # hai lần hỏi: HNSW cho limit 30 có thể khác 30 đầu của limit 100 (cổng 13:25: 9/10 câu giống) ⇒ runtime dùng
            # đúng kết quả limit 30 như `dense_bm25_rrf`, native dùng limit 100
            ids = {limit: [str(p.id) for p in service.client.query_points(
                collection_name=service.candidate.collection_name, query=vector, using="dense", limit=limit,
                with_payload=False).points] for limit in (RUNTIME_POOL, DENSE_POOL)}
            rows.append({"case_index": case["case_index"], "form": form, "query": query,
                         "dense_ids30": ids[RUNTIME_POOL], "dense_ids": ids[DENSE_POOL]})
    finally:
        service.close()
    return rows


# ---------- Một cấu hình ----------

def run_config(args) -> list[dict]:
    settings = load_settings(validate_private_paths=False)
    service = build_full_corpus_retrieval_service("e5-small-384", "dense_bm25_rrf", settings=settings)
    try:
        payloads = load_payloads(service.client, service.candidate.collection_name)
    finally:
        service.close()
    context_builder = build_context_builder(settings)
    gold = load_gold(GOLD_PATH)
    started = time.perf_counter()
    bm25 = MemoryBM25({pid: p["search_text"] for pid, p in payloads.items()}, TOKENIZERS[args.tokenizer],
                      k1=args.k1, b=args.b)
    fit_s = time.perf_counter() - started
    cases = {c["case_index"]: c for c in select_cases("dev", None)}
    rows = []
    for dense in map(json.loads, dense_path(args.form).read_text(encoding="utf-8").splitlines()):
        case, query = cases[dense["case_index"]], dense["query"]
        t0 = time.perf_counter()
        if args.fusion == "runtime":  # BM25 chỉ chấm lại dense-30 (như `dense_bm25_rrf`)
            dense_ids = dense["dense_ids30"]
            scored = bm25.scores(query, dense_ids)
            sparse_ids = rank_positive_bm25(list(scored.items()))
            pool = RUNTIME_POOL
        else:  # native: sparse top-100 trên cả kho, phá hòa theo point_id (như `order_by_score_then_point_id`)
            dense_ids = dense["dense_ids"][:DENSE_POOL]
            scored = bm25.scores(query)
            sparse_ids = [pid for pid, s in sorted(scored.items(), key=lambda x: (-x[1], x[0])) if s > 0][:DENSE_POOL]
            pool = DENSE_POOL
        branches = [dense_ids] + ([sparse_ids] if sparse_ids else [])
        fused = reciprocal_rank_fusion(branches, k=args.rrf_k, limit=pool)
        top = [build_retrieved_document(payloads[pid], score) for pid, score in fused[:TOP_K]]
        packed = context_builder.build(query, top)
        context_ids = packed_chunk_ids(top, len(packed.sources))
        row = {"case_index": case["case_index"], "category": case["category"], "config": args.name,
               "top_chunk_ids": [d.id for d in top], "context_chunk_ids": context_ids,
               "query_terms": len(bm25.query_terms(query)), "bm25_ms": (time.perf_counter() - t0) * 1000,
               **score_retrieval(case["keywords"], [d.text for d in top])}
        facts = gold.get(case["case_index"])
        if facts:
            by_chunk = {payloads[pid]["chunk_id"]: payloads[pid] for pid in set(dense_ids) | set(sparse_ids)}
            layers = {"pool_dense": [payloads[p]["chunk_id"] for p in dense_ids],
                      "pool_sparse": [payloads[p]["chunk_id"] for p in sparse_ids],
                      "pool_union": list(by_chunk), "top10": row["top_chunk_ids"], "context5": context_ids}
            for layer, ids in layers.items():
                coverage = gold_coverage(facts, [by_chunk[i] for i in ids])  # top-10 / context ⊂ hợp hai nhánh
                row[f"{layer}_gold_all"], row[f"{layer}_gold_frac"] = coverage["all"], coverage["frac"]
        rows.append(row)
    print(json.dumps({"fit_s": round(fit_s, 1), "vocabulary": len(bm25.idf), "num_docs": bm25.num_docs,
                      "avgdl": bm25.avgdl}))
    return rows


# ---------- Cổng tương đương (plan §1, §4 bước 0) ----------

def gate() -> dict:
    """BM25 trong bộ nhớ (âm tiết) vs production: sparse state, 200 cặp điểm, top-10 / context so với G1."""
    settings = load_settings(validate_private_paths=False)
    service = build_full_corpus_retrieval_service("e5-small-384", "dense_bm25_rrf", settings=settings)
    try:
        payloads = load_payloads(service.client, service.candidate.collection_name)
        state = service.sparse_state
        dense30 = [service.client.query_points(collection_name=service.candidate.collection_name,
                                               query=service.dense_runner.embed_queries([d["query"]])[0],
                                               using="dense", limit=RUNTIME_POOL, with_payload=False).points
                   for d in list(map(json.loads, dense_path("orig").read_text().splitlines()))[:10]]
    finally:
        service.close()
    bm25 = MemoryBM25({pid: p["search_text"] for pid, p in payloads.items()}, tokenize)
    out = {"state": {"num_docs": [bm25.num_docs, state.document_count], "avgdl_equal": bm25.avgdl == state.average_document_length,
                     "vocabulary_equal": sorted(bm25.idf) == list(state.vocabulary),
                     "idf_equal": all(bm25.idf[t] == v for t, v in zip(state.vocabulary, state.idf))}}
    dense_rows = list(map(json.loads, dense_path("orig").read_text().splitlines()))
    out["dense30_stored_equals_fresh"] = sum([str(p.id) for p in pts] == d["dense_ids30"] for pts, d in zip(dense30, dense_rows))
    out["dense30_equals_top30_of_100"] = sum(d["dense_ids30"] == d["dense_ids"][:RUNTIME_POOL] for d in dense_rows)
    rng = random.Random(SEED)
    vocab_index = {t: i for i, t in enumerate(state.vocabulary)}
    pids = sorted(payloads)
    worst, exact = 0.0, 0
    for _ in range(200):
        query = rng.choice(dense_rows)["query"]
        pid = rng.choice(rng.choice(dense_rows)["dense_ids"]) if rng.random() < 0.5 else rng.choice(pids)
        prod = compute_sparse_dot_product(encode_sparse_query(query, state),
                                          encode_sparse_document(payloads[pid]["search_text"], state, vocab_index))
        mine = bm25.scores(query, [pid])[pid]
        worst, exact = max(worst, abs(prod - mine)), exact + (prod == mine)
    out["pairs"] = {"n": 200, "max_abs_diff": worst, "bitwise_equal": exact}
    return out


def same_as_g1(name: str, g1_name: str) -> dict:
    mine = {r["case_index"]: r for r in _read(name)}
    ref = {r["case_index"]: r for r in map(json.loads, (G1_DIR / f"{g1_name}.jsonl").read_text().splitlines())}
    common = sorted(mine.keys() & ref.keys())
    diff = lambda key: [i for i in common if mine[i][key] != ref[i][key]]
    return {"n": len(common), "top10_diff": diff("top_chunk_ids"), "context_diff": diff("context_chunk_ids"),
            "mrr_diff": [i for i in common if abs(mine[i]["mrr"] - ref[i]["mrr"]) > 1e-12]}


def analyze(pairs: list[tuple[str, str]], realism: str | None) -> dict:
    """Luật plan §2: chỉ số quyết `context5_gold_all` (Holm chung trên mọi cặp truyền vào), sàn 0 câu mất, keyword
    coverage (thang %) cận dưới CI ≥ −2,0; kèm chỉ số theo dõi."""
    out = {}
    for base, variant in pairs:
        a, b = keep_realism(_read(base), realism), _read(variant)
        res = compare(a, {variant: b}, ["context5_gold_all", "keyword_coverage", "top10_gold_all", "context5_gold_frac",
                                        "pool_sparse_gold_all", "pool_union_gold_all", "mrr", "ndcg"])
        res = {m: v[variant] for m, v in res.items() if variant in v}
        a_map, b_map = {r["case_index"]: r for r in a}, {r["case_index"]: r for r in b}
        lost = [i for i in a_map if a_map[i].get("context5_gold_all") == 1.0 and b_map[i].get("context5_gold_all") == 0.0]
        out[f"{variant} vs {base}"] = {"metrics": res, "lost_cases": lost,
                                       "keyword_ok": res["keyword_coverage"]["ci95"][0] >= -2.0}
    keys = list(out)
    for key, p_holm in zip(keys, holm_adjust([out[k]["metrics"]["context5_gold_all"]["p_value"] for k in keys])):
        decide = out[key]["metrics"]["context5_gold_all"]
        better = p_holm < 0.05 and decide["ci95"][0] > 0
        worse = bool(out[key]["lost_cases"]) or decide["ci95"][1] < 0
        out[key]["p_holm"] = p_holm
        out[key]["verdict"] = ("kém hơn" if worse else "tốt hơn" if better and out[key]["keyword_ok"] else
                               "chưa rõ / không khác")
    return out


def _read(name: str) -> list[dict]:
    return [json.loads(line) for line in (OUT_DIR / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]


def _write(path, rows) -> None:
    if path.exists():
        raise SystemExit(f"{path} exists; choose a new --name")
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8.1 G4 keyword (in-memory BM25, read-only, free)")
    commands = parser.add_subparsers(dest="command", required=True)
    dense = commands.add_parser("dense", help="dense top-100 cho câu dev, một lần mỗi dạng câu hỏi")
    dense.add_argument("--form", required=True, choices=["orig", "noaccent"])
    commands.add_parser("gate", help="BM25 trong bộ nhớ vs production")
    run = commands.add_parser("run")
    run.add_argument("--name", required=True)
    run.add_argument("--fusion", required=True, choices=["runtime", "native"])
    run.add_argument("--tokenizer", required=True, choices=list(TOKENIZERS))
    run.add_argument("--form", default="orig", choices=["orig", "noaccent"])
    run.add_argument("--k1", type=float, default=K1)
    run.add_argument("--b", type=float, default=B)
    run.add_argument("--rrf-k", type=int, default=60)
    same = commands.add_parser("same-as-g1", help="so top-10 / context / MRR với một lượt G1")
    same.add_argument("--name", required=True)
    same.add_argument("--g1", required=True)
    cmp = commands.add_parser("compare")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True, nargs="+")
    cmp.add_argument("--metrics", required=True, nargs="+")
    cmp.add_argument("--realism", choices=["main", "natural"])
    ana = commands.add_parser("analyze", help="bảng quyết theo plan §2 (Holm chung trên mọi cặp)")
    ana.add_argument("--pairs", required=True, nargs="+", help="base:variant")
    ana.add_argument("--realism", choices=["main", "natural"])
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.command == "dense":
        _write(dense_path(args.form), run_dense(args.form))
        print(dense_path(args.form))
    elif args.command == "gate":
        print(json.dumps(gate(), indent=2))
    elif args.command == "run":
        rows = run_config(args)
        _write(OUT_DIR / f"{args.name}.jsonl", rows)
        print(OUT_DIR / f"{args.name}.jsonl", len(rows))
    elif args.command == "same-as-g1":
        print(json.dumps(same_as_g1(args.name, args.g1), indent=2))
    elif args.command == "analyze":
        print(json.dumps(analyze([tuple(p.split(":")) for p in args.pairs], args.realism), ensure_ascii=False, indent=2))
    else:
        a_rows = keep_realism(_read(args.a), args.realism)
        print(json.dumps(compare(a_rows, {n: _read(n) for n in args.b}, args.metrics), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
