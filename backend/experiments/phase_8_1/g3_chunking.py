"""Phase 8.1 G3 — biến thể chia đoạn (build e5 local vào `hue_81_g3_*`, đo retrieval, xóa collection).

Kế hoạch + tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g3_plan.md` (bản duyệt
`e089243fb612`). Chunker production không đổi: harness nhận danh sách đoạn của `chunk_full_corpus` rồi biến đổi
(gộp `evidence_parts`, dựng lại `search_text` bằng `build_representation_a_search_text`), build bằng
`build_candidate(chunks=…)` vào collection + build record + sparse state riêng. Kết quả: `data/phase_8_1/g3/` (private).

Biến thể = chuỗi bước nối bằng "-", áp theo thứ tự trên chunker production:
  h1         chunker chỉ kiểm giới hạn e5-small 512 (bỏ e5-base, HuyDang)
  h3         gộp dòng bảng bị tách (cùng bảng, cùng điều kiện) thành nhóm ≤ 256 token e5
  h2_<T>     gộp đoạn liền nhau cùng (source, heading_path), cùng điều kiện, tới T token e5
  p_nearest  tiền tố search_text chỉ còn heading gần nhất · p_none  không tiền tố
  s1 bỏ file inventory performing_arts · s2 thêm đoạn cho code fence bị parser bỏ · s3 bỏ đoạn sau của cặp lặp body

Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking stats --variant h1-h2_256
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking budget
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking build --variant h1
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking run --variant h1 --name h1
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking compare --a base --b h1 --metrics ctxB_gold_all
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g3_chunking drop --variant h1
"""
import argparse
import hashlib
import json
import math
import os
import re
import statistics
import time
from pathlib import Path

import numpy as np

from evaluation.full_corpus_eval import (  # import này cũng đưa gốc repo + backend/ vào sys.path
    REPO_ROOT,
    build_context_builder,
    load_golden_cases,
    score_retrieval,
    split_group_indexes,
)
from core.schema import EvidencePart, FullCorpusChunk
from core.settings_loader import load_settings
from ingestion.chunking.full_corpus_chunker import build_representation_a_search_text, chunk_full_corpus
from ingestion.full_corpus_pipeline import build_candidate
from ingestion.preview import count_tokens_for_chunk, load_tokenizers
from ingestion.source_state import discover_full_corpus_files, read_source_lf
from vectorstore.qdrant import client_from_settings
from experiments.phase_8_1.g1_retrieval import (
    GOLD_PATH,
    SPLIT_PATH,
    compare,
    gold_coverage,
    keep_realism,
    load_gold,
    load_payloads,
)
from experiments.phase_8_1.g4_rerank import packed_chunk_ids
from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus import build_full_corpus_retrieval_service, build_retrieved_document
from retrieval.full_corpus_context import FullCorpusContextBuilder

OUT_DIR = REPO_ROOT / "data/phase_8_1/g3"
BUILD_DIR = REPO_ROOT / "data/phase_8_1/builds"
BUDGET_PATH = OUT_DIR / "budget.json"
COLLECTION_PREFIX = "hue_81_g3_"
MAX_G3_COLLECTIONS = 3  # plan §1
E5_ID = "intfloat/multilingual-e5-small"
H3_LIMIT = 256  # plan §3: nhóm dòng bảng ≤ 256 token e5
INVENTORY_SOURCE = "performing_arts/performing-arts-entities-inventory.md"
FENCE_RE = re.compile(r"^```[^\n]*\n.*?^```[^\n]*$", re.MULTILINE | re.DOTALL)
TOP_K = 10


# ---------- Biến thể: danh sách đoạn ----------

def e5_settings(settings: dict) -> dict:
    fc = settings["full_corpus"]
    models = [m for m in fc["embedding_models"] if m["id"] == E5_ID]
    return {**settings, "full_corpus": {**fc, "embedding_models": models}}


class E5Counter:
    """Đếm token e5-small như checker của chunker (prefix "passage: ", truncation=False)."""

    def __init__(self, settings: dict):
        settings = e5_settings(settings)
        self.models = settings["full_corpus"]["embedding_models"]
        self.tokenizers, errors = load_tokenizers(settings)
        if errors:
            raise RuntimeError(errors)

    def __call__(self, text: str) -> int:
        return count_tokens_for_chunk(text, self.tokenizers, self.models)[E5_ID]


def rebuilt(chunk: FullCorpusChunk, parts: list[EvidencePart]) -> FullCorpusChunk:
    return FullCorpusChunk(chunk_id=chunk.chunk_id, source=chunk.source, title=chunk.title,
                           heading_path=list(chunk.heading_path), evidence_parts=parts,
                           search_text=build_representation_a_search_text(chunk.title, chunk.heading_path, parts))


def condition_key(chunk: FullCorpusChunk) -> tuple:
    return tuple((p.start, p.end) for p in chunk.evidence_parts if p.role == "condition")


def table_header(chunk: FullCorpusChunk) -> EvidencePart | None:
    """Phần header của đoạn dòng-bảng bị tách (header là dòng tiêu đề bảng Markdown)."""
    return next((p for p in chunk.evidence_parts if p.role == "header" and p.text.lstrip().startswith("|")), None)


def group_table_rows(chunks: list[FullCorpusChunk], texts: dict[str, str], ntok: E5Counter) -> list[FullCorpusChunk]:
    """H3: dòng liền nhau của cùng bảng (cùng header, cùng điều kiện) gộp thành một body liên tục ≤ H3_LIMIT."""
    out: list[FullCorpusChunk] = []
    group: list[FullCorpusChunk] = []

    def merged(rows: list[FullCorpusChunk]) -> FullCorpusChunk:
        first = rows[0]
        if len(rows) == 1:
            return first
        bodies = [p for r in rows for p in r.evidence_parts if p.role == "body"]
        start, end = bodies[0].start, bodies[-1].end
        body = EvidencePart(role="body", start=start, end=end, text=texts[first.source][start:end])
        header = table_header(first)
        conds = [p for p in first.evidence_parts if p.role == "condition"]
        parts = [c for c in conds if c.start < header.start] + [header, body] + [c for c in conds if c.start > header.start]
        return rebuilt(first, parts)

    def same_table(a: FullCorpusChunk, b: FullCorpusChunk) -> bool:
        ha, hb = table_header(a), table_header(b)
        return (a.source == b.source and a.heading_path == b.heading_path and ha is not None and hb is not None
                and (ha.start, ha.end) == (hb.start, hb.end) and condition_key(a) == condition_key(b))

    for chunk in chunks:
        if group and same_table(group[-1], chunk) and ntok(merged(group + [chunk]).search_text) <= H3_LIMIT:
            group.append(chunk)
            continue
        if group:
            out.append(merged(group))
        group = [chunk] if table_header(chunk) is not None else []
        if not group:
            out.append(chunk)
    if group:
        out.append(merged(group))
    return out


def merge_same_heading(chunks: list[FullCorpusChunk], limit: int, ntok: E5Counter) -> tuple[list, dict]:
    """H2: gộp tham lam các đoạn liền nhau cùng (source, heading_path) và cùng tập điều kiện, tới `limit` token e5."""
    out: list[FullCorpusChunk] = []
    current: FullCorpusChunk | None = None
    blocked_by_condition = 0
    for chunk in chunks:
        if current is not None and current.source == chunk.source and current.heading_path == chunk.heading_path:
            if condition_key(current) != condition_key(chunk):
                blocked_by_condition += 1
            else:
                seen = {(p.role, p.start, p.end) for p in current.evidence_parts}
                candidate = rebuilt(current, current.evidence_parts
                                    + [p for p in chunk.evidence_parts if (p.role, p.start, p.end) not in seen])
                if ntok(candidate.search_text) <= limit:
                    current = candidate
                    continue
        if current is not None:
            out.append(current)
        current = chunk
    if current is not None:
        out.append(current)
    return out, {"blocked_by_condition": blocked_by_condition}


def with_prefix(chunks: list[FullCorpusChunk], mode: str) -> list[FullCorpusChunk]:
    """Đổi tiền tố search_text (dòng tiêu đề + dòng heading của Representation A); payload/evidence giữ nguyên."""
    out = []
    for chunk in chunks:
        full = chunk.search_text.split("\n")
        body = full[2:] if chunk.heading_path else full[1:]
        head = [] if mode == "p_none" else [chunk.heading_path[-1] if chunk.heading_path else chunk.title]
        out.append(FullCorpusChunk(chunk_id=chunk.chunk_id, source=chunk.source, title=chunk.title,
                                   heading_path=list(chunk.heading_path), evidence_parts=chunk.evidence_parts,
                                   search_text="\n".join(head + body)))
    return out


def add_fences(chunks: list[FullCorpusChunk], texts: dict[str, str]) -> tuple[list, dict]:
    """S2: mỗi code fence bị parser bỏ thành một đoạn, đặt sau đoạn đứng trước nó trong file (heading của đoạn đó)."""
    out = list(chunks)
    added = 0
    for source, text in texts.items():
        for match in FENCE_RE.finditer(text):
            before = [i for i, c in enumerate(out) if c.source == source and c.evidence_parts[0].start < match.start()]
            anchor = out[before[-1]]
            part = EvidencePart(role="body", start=match.start(), end=match.end(), text=match.group(0))
            out.insert(before[-1] + 1, rebuilt(anchor, [part]))
            added += 1
    return out, {"fences_added": added}


def drop_nested_duplicates(chunks: list[FullCorpusChunk]) -> tuple[list, dict]:
    """S3: bỏ đoạn mà body nằm trong body của đoạn trước nó cùng file (blockquote lồng trong list item)."""
    out, dropped = [], []
    for chunk in chunks:
        bodies = [p for p in chunk.evidence_parts if p.role == "body"]
        nested = any(prev.source == chunk.source and all(any(q.role == "body" and q.start <= p.start and p.end <= q.end
                                                              for q in prev.evidence_parts) for p in bodies)
                     for prev in out[-3:])
        (dropped if nested else out).append(chunk)
    return out, {"dropped": [c.chunk_id for c in dropped]}


def renumbered(chunks: list[FullCorpusChunk]) -> list[FullCorpusChunk]:
    """chunk_id = source#thứ-tự sau biến đổi (đoạn đúng chấm theo offset nên không phụ thuộc id)."""
    counters: dict[str, int] = {}
    out = []
    for chunk in chunks:
        n = counters.get(chunk.source, 0)
        counters[chunk.source] = n + 1
        out.append(FullCorpusChunk(chunk_id=f"{chunk.source}#{n}", source=chunk.source, title=chunk.title,
                                   heading_path=list(chunk.heading_path), evidence_parts=chunk.evidence_parts,
                                   search_text=chunk.search_text))
    return out


def make_chunks(variant: str) -> tuple[list[FullCorpusChunk], dict]:
    steps = [] if variant == "base" else variant.split("-")  # base = chunker production, để kiểm harness
    settings = load_settings()
    if steps[:1] == ["h1"]:
        settings = e5_settings(settings)
    chunks, errors = chunk_full_corpus(settings)
    if errors:
        raise ValueError(f"chunking failed: {errors[:3]}")
    root, files = discover_full_corpus_files(settings)
    texts = {rel: read_source_lf(root / rel) for rel in files}
    ntok = E5Counter(settings)
    info: dict = {"steps": steps, "chunks_from_chunker": len(chunks)}
    for step in steps[1:] if steps[:1] == ["h1"] else steps:
        before = len(chunks)
        if step == "h3":
            chunks = group_table_rows(chunks, texts, ntok)
            extra = {}
        elif step.startswith("h2_"):
            chunks, extra = merge_same_heading(chunks, int(step[3:]), ntok)
        elif step in ("p_nearest", "p_none"):
            chunks, extra = with_prefix(chunks, step), {}
        elif step == "s1":
            chunks, extra = [c for c in chunks if c.source != INVENTORY_SOURCE], {}
        elif step == "s2":
            chunks, extra = add_fences(chunks, texts)
        elif step == "s3":
            chunks, extra = drop_nested_duplicates(chunks)
        else:
            raise ValueError(f"unknown step: {step}")
        info[step] = {"before": before, "after": len(chunks), **extra}
    chunks = renumbered(chunks)
    tokens = [ntok(c.search_text) for c in chunks]
    per_leaf: dict[tuple, int] = {}
    for c in chunks:
        per_leaf[(c.source, tuple(c.heading_path))] = per_leaf.get((c.source, tuple(c.heading_path)), 0) + 1
    info.update({"chunk_count": len(chunks), "leaf_count": len(per_leaf),
                 "single_chunk_leaves": sum(n == 1 for n in per_leaf.values()),
                 "e5_tokens": {"p50": float(np.median(tokens)), "p90": float(np.percentile(tokens, 90)),
                               "max": max(tokens), "lt64": sum(t < 64 for t in tokens), "gt512": sum(t > 512 for t in tokens)},
                 "chunk_list_sha": chunk_list_sha(chunks)})
    return chunks, info


def chunk_list_sha(chunks: list[FullCorpusChunk]) -> str:
    data = json.dumps([[c.chunk_id, c.search_text, [[p.role, p.start, p.end] for p in c.evidence_parts]]
                       for c in chunks], ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# ---------- Build / xóa collection biến thể ----------

def variant_paths(variant: str) -> dict[str, Path]:
    folder = BUILD_DIR / variant
    return {"dir": folder, "record": folder / "build_record.json", "sparse": folder / "sparse_state.json",
            "variant": folder / "variant.json"}


def g3_collections(client) -> list[str]:
    return sorted(c.name for c in client.get_collections().collections)


def build(variant: str) -> dict:
    paths = variant_paths(variant)
    if paths["variant"].exists():
        raise SystemExit(f"{paths['variant']} exists; variant already built")
    settings = load_settings()
    client = client_from_settings(settings)
    try:
        before = g3_collections(client)
    finally:
        client.close()
    if sum(name.startswith(COLLECTION_PREFIX) for name in before) >= MAX_G3_COLLECTIONS:
        raise SystemExit(f"already {MAX_G3_COLLECTIONS} {COLLECTION_PREFIX}* collections; drop one first: {before}")
    started = time.perf_counter()
    chunks, info = make_chunks(variant)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    summary = build_candidate("e5-small-384", collection_name=COLLECTION_PREFIX + variant,
                              sparse_state_path=paths["sparse"], record_path=paths["record"], chunks=chunks)
    client = client_from_settings(settings)
    try:
        after = g3_collections(client)
    finally:
        client.close()
    record = {"variant": variant, "info": info, "build": summary, "collections_before": before,
              "collections_after": after, "build_seconds": time.perf_counter() - started,
              "loadavg_end": os.getloadavg(), "finished": time.strftime("%Y-%m-%d %H:%M:%S %z")}
    paths["variant"].write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def drop(variant: str) -> dict:
    target = COLLECTION_PREFIX + variant
    settings = load_settings()
    client = client_from_settings(settings)
    try:
        before = g3_collections(client)
        if target not in before:
            raise SystemExit(f"{target} not found: {before}")
        print("drop target:", target, "| before:", before)
        client.delete_collection(target)
        after = g3_collections(client)
    finally:
        client.close()
    return {"dropped": target, "before": before, "after": after}


# ---------- Đo retrieval ----------

def block_tokens(enc, document) -> int | None:
    """Token o200k của khối đoạn đúng như context builder dựng (None = đoạn không có bằng chứng, builder bỏ)."""
    source = FullCorpusContextBuilder._source(document, 1)
    return None if source is None else len(enc.encode(FullCorpusContextBuilder._block(source)))


def budget_context(enc, documents: list, budget: int) -> tuple[list[str], int, bool]:
    """Context-B: lấy đoạn theo hạng tới khi tổng token ≤ B; đoạn đầu lớn hơn B vẫn lấy (đếm riêng)."""
    ids, total = [], 0
    for document in documents:
        cost = block_tokens(enc, document)
        if cost is None:
            continue
        if ids and total + cost > budget:
            break
        ids.append(document.id)
        total += cost
    return ids, total, bool(ids) and total > budget


def leaf_expanded(documents: list, payload_by_chunk: dict[str, dict]) -> list:
    """Small-to-big: mỗi đoạn trong top-10 thay bằng cả heading lá chứa nó (đoạn anh em theo thứ tự file), bỏ trùng."""
    leaves: dict[tuple, list[dict]] = {}
    for payload in payload_by_chunk.values():
        leaves.setdefault((payload["source"], tuple(payload["heading_path"])), []).append(payload)
    for members in leaves.values():
        members.sort(key=lambda p: p["evidence_parts"][0]["start"])
    out, seen = [], set()
    for document in documents:
        key = (document.metadata["source"], tuple(document.metadata["heading_path"]))
        for payload in leaves[key]:
            if payload["chunk_id"] not in seen:
                seen.add(payload["chunk_id"])
                out.append(build_retrieved_document(payload, 0.0))
    return out


def select_cases(group: str) -> list[dict]:
    cases = load_golden_cases("full")
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    wanted = set(split_group_indexes(split, group, cases))
    return [c for c in cases if c["case_index"] in wanted]


def run(variant: str, group: str, expand: bool, budget: int | None) -> tuple[list[dict], dict]:
    settings = load_settings()
    kwargs = {}
    meta = {"variant": variant, "group": group, "expand": expand, "budget": budget,
            "started": time.strftime("%Y-%m-%d %H:%M:%S %z"), "loadavg_start": os.getloadavg()}
    if variant != "base":
        paths = variant_paths(variant)
        record = json.loads(paths["variant"].read_text(encoding="utf-8"))
        _, info = make_chunks(variant)
        if info["chunk_list_sha"] != record["info"]["chunk_list_sha"]:
            raise SystemExit("chunk list differs from built variant; rebuild")  # plan §1: đo đúng index của biến thể
        kwargs = {"collection_name": COLLECTION_PREFIX + variant, "record_path": paths["record"],
                  "sparse_state_path": paths["sparse"]}
        meta.update({"collection": kwargs["collection_name"], "chunk_list_sha": info["chunk_list_sha"],
                     "chunk_count": info["chunk_count"]})
    service = build_full_corpus_retrieval_service("e5-small-384", "dense_bm25_rrf", settings=settings, **kwargs)
    builders = {5: build_context_builder(settings), 10: build_context_builder(settings, max_documents=10)}
    enc = load_openai_tokenizer()
    gold = load_gold(GOLD_PATH)
    rows = []
    try:
        payload_by_point = load_payloads(service.client, service.candidate.collection_name)
        payload_by_chunk = {p["chunk_id"]: p for p in payload_by_point.values()}
        for case in select_cases(group):
            query = case["question"]
            t0 = time.perf_counter()
            result = service.search(query)
            t1 = time.perf_counter()
            top = result.documents[:TOP_K]
            row = {"case_index": case["case_index"], "category": case["category"], "variant": variant,
                   "top_chunk_ids": [d.id for d in top], "retrieval_ms": (t1 - t0) * 1000,
                   **score_retrieval(case["keywords"], [d.text for d in top])}
            ctx_ids = {}
            for n, builder in builders.items():
                packed = builder.build(query, top)
                ctx_ids[f"ctx{n}"] = packed_chunk_ids(top, len(packed.sources))
            row["ctx5_tokens"] = sum(block_tokens(enc, d) or 0 for d in top if d.id in set(ctx_ids["ctx5"]))
            if budget is not None:
                ranked = leaf_expanded(top, payload_by_chunk) if expand else top
                ctx_ids["ctxB"], row["ctxB_tokens"], row["ctxB_first_over"] = budget_context(enc, ranked, budget)
                texts = [payload_by_chunk[i]["search_text"] for i in ctx_ids["ctxB"]]
                row["ctxB_keyword_coverage"] = score_retrieval(case["keywords"], texts)["keyword_coverage"]
            row.update({f"{k}_chunk_ids": v for k, v in ctx_ids.items()})
            facts = gold.get(case["case_index"])
            if facts:
                stages = result.trace.stages
                sparse = stages.get("sparse", stages.get("bm25", []))  # runtime dense_bm25_rrf gọi tầng này "bm25" (như G1)
                union = dict.fromkeys([e["point_id"] for e in stages["dense"]] + [e["point_id"] for e in sparse])
                layers = {"pool_union": [payload_by_point[p]["chunk_id"] for p in union], "top10": row["top_chunk_ids"],
                          **ctx_ids}
                for layer, ids in layers.items():
                    coverage = gold_coverage(facts, [payload_by_chunk[i] for i in ids])
                    row[f"{layer}_gold_all"], row[f"{layer}_gold_frac"] = coverage["all"], coverage["frac"]
            rows.append(row)
    finally:
        service.close()
    meta.update({"n": len(rows), "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"), "loadavg_end": os.getloadavg(),
                 "retrieval_ms": {"p50": float(np.percentile([r["retrieval_ms"] for r in rows], 50)),
                                  "p95": float(np.percentile([r["retrieval_ms"] for r in rows], 95))}})
    return rows, meta


# ---------- §10 G3.B10: đóng gói lại context từ top-10 đã lưu (không build, không Qdrant) ----------

BUDGET10_PATH = OUT_DIR / "budget10.json"


def variant_payloads(variant: str) -> dict[str, dict]:
    """chunk_id → payload của biến thể, dựng lại bằng make_chunks; sha phải khớp lúc build (đo đúng index đã chạy)."""
    chunks, info = make_chunks(variant)
    if variant != "base":
        built = json.loads(variant_paths(variant)["variant"].read_text(encoding="utf-8"))["info"]["chunk_list_sha"]
        if info["chunk_list_sha"] != built:
            raise SystemExit(f"{variant}: chunk list differs from build ({info['chunk_list_sha'][:12]} != {built[:12]})")
    return {c.chunk_id: c.to_qdrant_payload() for c in chunks}


def budget10() -> dict:
    """B10 = trung vị token khối bằng chứng 10 đoạn context runtime (base.jsonl), dev số chính trong kho, lên bội 50."""
    enc, payloads = load_openai_tokenizer(), variant_payloads("base")
    rows = keep_realism(_read("base"), "main")
    tokens = [sum(block_tokens(enc, build_retrieved_document(payloads[i], 0.0)) or 0 for i in r["ctx10_chunk_ids"])
              for r in rows]
    median = statistics.median(tokens)
    return {"budget": int(math.ceil(median / 50) * 50), "median_ctx10_tokens": median, "n": len(tokens),
            "rule": "plan §10: trung vị token o200k khối bằng chứng 10 đoạn context runtime (base.jsonl), dev số chính trong kho, làm tròn lên bội 50",
            "written": time.strftime("%Y-%m-%d %H:%M:%S %z")}


def rebudget(name: str, variant: str, budget: int, prefix: str) -> list[dict]:
    """Context-<prefix> từ top-10 đã lưu của lượt `name`: đoạn đúng, keyword, token; cộng keyword của ctx10 (baseline)."""
    enc, payloads, gold = load_openai_tokenizer(), variant_payloads(variant), load_gold(GOLD_PATH)
    cases = {c["case_index"]: c for c in load_golden_cases("full")}
    out = []
    for row in (json.loads(line) for line in (OUT_DIR / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()):
        top = [build_retrieved_document(payloads[i], 0.0) for i in row["top_chunk_ids"]]
        ids, total, over = budget_context(enc, top, budget)
        keywords = cases[row["case_index"]]["keywords"]
        new = {"case_index": row["case_index"], "category": row["category"], "variant": variant, "source_run": name,
               "top_chunk_ids": row["top_chunk_ids"], f"{prefix}_chunk_ids": ids, f"{prefix}_tokens": total,
               f"{prefix}_first_over": over, "ctx10_chunk_ids": row["ctx10_chunk_ids"],
               f"{prefix}_keyword_coverage": score_retrieval(keywords, [payloads[i]["search_text"] for i in ids])["keyword_coverage"],
               "ctx10_keyword_coverage": score_retrieval(keywords, [payloads[i]["search_text"] for i in row["ctx10_chunk_ids"]])["keyword_coverage"]}
        facts = gold.get(row["case_index"])
        if facts:
            for layer, layer_ids in ((prefix, ids), ("ctx10", row["ctx10_chunk_ids"])):
                coverage = gold_coverage(facts, [payloads[i] for i in layer_ids])
                new[f"{layer}_gold_all"], new[f"{layer}_gold_frac"] = coverage["all"], coverage["frac"]
        out.append(new)
    return out


def table(rows: list[dict]) -> dict:
    keys = sorted({k for r in rows for k, v in r.items() if isinstance(v, (int, float)) and not isinstance(v, bool)
                   and k not in ("case_index", "retrieval_ms")})
    return {"n": len(rows), **{k: statistics.fmean(r[k] for r in rows if k in r) for k in keys},
            "ctxB_first_over": sum(bool(r.get("ctxB_first_over")) for r in rows)}


def _read(name: str) -> list[dict]:
    """Câu trong kho (plan §2: n = 88 dev số chính); câu out_of_scope không có keyword / đoạn đúng."""
    rows = [json.loads(line) for line in (OUT_DIR / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
    return [r for r in rows if r["category"] != "out_of_scope"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8.1 G3 chunking variants (hue_81_g3_* only, free)")
    commands = parser.add_subparsers(dest="command", required=True)
    stats = commands.add_parser("stats", help="thống kê danh sách đoạn của biến thể (không build)")
    stats.add_argument("--variant", required=True)
    commands.add_parser("budget", help="đo B từ context-5 runtime trên dev số chính (plan §1), ghi một lần")
    for name in ("build", "drop"):
        commands.add_parser(name).add_argument("--variant", required=True)
    runp = commands.add_parser("run")
    runp.add_argument("--variant", required=True, help="'base' = collection runtime")
    runp.add_argument("--name", required=True, help="tên file JSONL trong data/phase_8_1/g3/")
    runp.add_argument("--group", default="dev", choices=["dev", "test"])
    runp.add_argument("--expand", action="store_true", help="small-to-big: mở rộng tới cả heading lá")
    cmp = commands.add_parser("compare")
    cmp.add_argument("--a", required=True)
    cmp.add_argument("--b", required=True, nargs="+")
    cmp.add_argument("--metrics", required=True, nargs="+")
    cmp.add_argument("--realism", default="main", choices=["main", "natural"])
    cmp.add_argument("--a-fields", nargs="*", default=[],
                     help="metric=field: lấy chỉ số của --a từ field khác (§10: ctxB10_gold_all=ctx10_gold_all)")
    commands.add_parser("budget10", help="§10: ghi B10 từ base.jsonl (một lần)")
    reb = commands.add_parser("rebudget", help="§10: đóng gói lại context từ top-10 đã lưu")
    reb.add_argument("--name", required=True, help="lượt đã chạy (JSONL trong data/phase_8_1/g3/)")
    reb.add_argument("--variant", required=True)
    reb.add_argument("--out", required=True)
    reb.add_argument("--budget", type=int, help="mặc định B10; cổng tự kiểm dùng B cũ 750 (prefix ctxB)")
    reb.add_argument("--prefix", default="ctxB10")
    summary = commands.add_parser("summary")
    summary.add_argument("--names", required=True, nargs="+")
    summary.add_argument("--realism", default="main", choices=["main", "natural"])
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.command == "stats":
        print(json.dumps(make_chunks(args.variant)[1], ensure_ascii=False, indent=2))
    elif args.command == "budget":
        if BUDGET_PATH.exists():
            raise SystemExit(f"{BUDGET_PATH} exists; B is fixed once")
        rows, _ = run("base", "dev", False, None)
        tokens = [r["ctx5_tokens"] for r in keep_realism(rows, "main") if r["category"] != "out_of_scope"]
        median = statistics.median(tokens)
        record = {"budget": int(math.ceil(median / 50) * 50), "median_ctx5_tokens": median, "n": len(tokens),
                  "rule": "plan §1: trung vị token o200k khối bằng chứng của 5 đoạn runtime, dev số chính trong kho, làm tròn lên bội 50",
                  "written": time.strftime("%Y-%m-%d %H:%M:%S %z")}
        BUDGET_PATH.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record, ensure_ascii=False, indent=2))
    elif args.command == "build":
        print(json.dumps(build(args.variant), ensure_ascii=False, indent=2))
    elif args.command == "drop":
        print(json.dumps(drop(args.variant), ensure_ascii=False, indent=2))
    elif args.command == "run":
        out = OUT_DIR / f"{args.name}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists; choose a new --name")
        budget = json.loads(BUDGET_PATH.read_text(encoding="utf-8"))["budget"]
        rows, meta = run(args.variant, args.group, args.expand, budget)
        out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
        (OUT_DIR / f"{args.name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                                        encoding="utf-8")
        print(json.dumps({"meta": meta, "summary": table(keep_realism(rows, "main"))}, ensure_ascii=False, indent=2))
    elif args.command == "budget10":
        if BUDGET10_PATH.exists():
            raise SystemExit(f"{BUDGET10_PATH} exists; B10 is fixed once")
        record = budget10()
        BUDGET10_PATH.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record, ensure_ascii=False, indent=2))
    elif args.command == "rebudget":
        out = OUT_DIR / f"{args.out}.jsonl"
        if out.exists():
            raise SystemExit(f"{out} exists; choose a new --out")
        budget = args.budget or json.loads(BUDGET10_PATH.read_text(encoding="utf-8"))["budget"]
        rows = rebudget(args.name, args.variant, budget, args.prefix)
        out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
        print(json.dumps(table(keep_realism([r for r in rows if r["category"] != "out_of_scope"], "main")), indent=2))
    elif args.command == "compare":
        a_rows = keep_realism(_read(args.a), args.realism)
        for pair in args.a_fields:
            metric, field = pair.split("=")
            a_rows = [{**r, metric: r[field]} if field in r else {k: v for k, v in r.items() if k != metric} for r in a_rows]
        print(json.dumps(compare(a_rows, {n: _read(n) for n in args.b}, args.metrics), ensure_ascii=False, indent=2))
    else:
        out = {name: table(keep_realism(_read(name), args.realism)) for name in args.names}
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
