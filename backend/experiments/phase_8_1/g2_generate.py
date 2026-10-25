"""Phase 8.1 G2 — sinh câu trả lời với retrieval cố định = runtime; đo prompt / context / reasoning effort.

Kế hoạch + tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` (bản duyệt
`a4adfc8eedd9`) §2, §2.1. Gọi code production qua tham số: `answer_case` của evaluator (retrieval → context →
`OpenAIFullCorpusGenerator` → validator citation), `build_context_builder(settings, max_documents)`,
`OpenAIFullCorpusGenerator.from_environment(answer_instructions=…, reasoning_effort=…)`. Logic biến thể chỉ có ở đây:
xếp 5 đoạn gom theo tài liệu, hai prompt P1/P2, chính sách citation thay thế (phát lại). Paid: chỉ `gpt-6-luna`.
Kết quả: JSONL private `data/phase_8_1/g2/`.

Chạy từ `backend/` (mỗi lượt có phí: pilot 10 câu trước, rồi phần còn lại):
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.phase_8_1.g2_generate run --variant baseline \
      --cases pilot --name g20_baseline_pilot
"""
import argparse
import asyncio
import dataclasses
import hashlib
import json
import random
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

from evaluation.full_corpus_eval import (  # import này cũng đưa gốc repo + backend/ vào sys.path
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
    holm_adjust,
    is_refusal,
    load_golden_cases,
    split_group_indexes,
    validate_score_rows,
    verdict,
)
from core.schema import CitationIntegrityError
from core.settings_loader import load_settings
from experiments.phase_8_1.g1_retrieval import GOLD_PATH, SPLIT_PATH, keep_realism, load_gold
from experiments.phase_8_1.g4_rerank import packed_chunk_ids
from llm.citations import select_cited_sources
from llm.full_corpus_prompt import ANSWER_SYSTEM_INSTRUCTIONS, INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from retrieval.full_corpus_context import PackedSource

OUT_DIR = REPO_ROOT / "data/phase_8_1/g2"
SEED = 20261024

_REFUSAL_RULE = f"Nếu bằng chứng không đủ, trả đúng duy nhất câu sau, không thêm citation:\n{INSUFFICIENT_ANSWER}"
assert _REFUSAL_RULE in ANSWER_SYSTEM_INSTRUCTIONS
# plan §2 G2.2 — chữ của hai prompt ghi trước, không sửa sau khi thấy số.
P1_PARTIAL = ANSWER_SYSTEM_INSTRUCTIONS.replace(_REFUSAL_RULE, (
    "Nếu bằng chứng chỉ đủ cho một phần câu hỏi, trả lời phần có căn cứ kèm citation, rồi nói rõ phần nào nguồn dữ "
    "liệu không có thông tin bằng một câu riêng không citation. Chỉ khi không có bằng chứng liên quan nào, trả đúng "
    f"duy nhất câu sau, không thêm citation:\n{INSUFFICIENT_ANSWER}"))
P2_SPEC_RULES = ANSWER_SYSTEM_INSTRUCTIONS.replace(_REFUSAL_RULE, (
    "Không dùng tiêu đề hoặc tên mục làm bằng chứng nếu phần Bằng chứng không hỗ trợ.\n"
    "Dùng đoạn văn ngắn cho câu hỏi đơn giản; chỉ dùng danh sách khi câu trả lời thật sự có nhiều mục hoặc bước.\n"
    + _REFUSAL_RULE))

# biến thể → (max_context_documents, answer_instructions, reasoning_effort, xếp theo tài liệu)
VARIANTS = {
    "baseline": (None, ANSWER_SYSTEM_INSTRUCTIONS, None, False),
    "context10": (10, ANSWER_SYSTEM_INSTRUCTIONS, None, False),
    "doc_order": (None, ANSWER_SYSTEM_INSTRUCTIONS, None, True),
    "p1_partial": (None, P1_PARTIAL, None, False),
    "p2_spec_rules": (None, P2_SPEC_RULES, None, False),
    "reasoning_none": (None, ANSWER_SYSTEM_INSTRUCTIONS, "none", False),
    "reasoning_low": (None, ANSWER_SYSTEM_INSTRUCTIONS, "low", False),
    "reasoning_high": (None, ANSWER_SYSTEM_INSTRUCTIONS, "high", False),
}


# ---------- Tập câu ----------

def group_cases(group: str) -> list[dict]:
    cases = load_golden_cases("full")
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    wanted = set(split_group_indexes(split, group, cases))
    return [c for c in cases if c["case_index"] in wanted]


def select(name: str) -> list[dict]:
    """dev = 120 câu (gồm out_of_scope); pilot = 10 câu rút theo seed; rest = phần còn lại.
    test / test_pilot / test_rest: như trên cho 56 câu test (chỉ để xác nhận phương án "tốt hơn")."""
    group = "test" if name.startswith("test") else "dev"
    cases = group_cases(group)
    pilot = set(random.Random(SEED).sample(sorted(c["case_index"] for c in cases), 10))
    if name.endswith("pilot"):
        return [c for c in cases if c["case_index"] in pilot]
    if name.endswith("rest"):
        return [c for c in cases if c["case_index"] not in pilot]
    return cases


# ---------- Biến thể "xếp theo tài liệu" (G2.1b) ----------

class DocOrderService:
    """Bọc retrieval runtime: giữ nguyên tập 5 đoạn đưa model, chỉ xếp lại gom theo tài liệu (thứ tự xuất hiện đầu).
    Đoạn ngoài 5 đoạn giữ thứ tự cũ phía sau (builder chỉ lấy 5 đoạn đầu có bằng chứng)."""

    def __init__(self, service, max_documents: int):
        self._service, self._max = service, max_documents

    def search(self, query: str):
        result = self._service.search(query)
        docs = list(result.documents)
        chosen = set(packed_chunk_ids(docs, self._max))  # 5 đoạn builder sẽ lấy (đã có bằng chứng)
        first = [d for d in docs if d.id in chosen]
        order = list(dict.fromkeys(d.metadata["source"] for d in first))
        grouped = sorted(first, key=lambda d: order.index(d.metadata["source"]))  # sort ổn định: giữ hạng trong tài liệu
        return dataclasses.replace(result, documents=grouped + [d for d in docs if d.id not in chosen])

    def close(self):
        self._service.close()


# ---------- Chạy một lượt ----------

async def run_variant(variant: str, cases: list[dict]) -> list[dict]:
    max_docs, instructions, effort, doc_order = VARIANTS[variant]
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    if doc_order:
        service = DocOrderService(service, settings["full_corpus_generation"]["max_context_documents"])
    context_builder = build_context_builder(settings, max_docs)
    generator = OpenAIFullCorpusGenerator.from_environment(
        settings, answer_instructions=instructions, reasoning_effort=effort)
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
        row["variant"] = variant
        row["usd"] = cost_usd(row["input_tokens"] or 0, row["output_tokens"] or 0)
    return rows


def usage(rows: list[dict]) -> dict:
    called = [r for r in rows if r["input_tokens"] is not None]
    total_in, total_out = sum(r["input_tokens"] for r in called), sum(r["output_tokens"] for r in called)
    return {"n": len(rows), "called": len(called), "errors": sum(bool(r["error"]) for r in rows),
            "input_tokens": total_in, "output_tokens": total_out, "usd": cost_usd(total_in, total_out),
            "usd_per_case": cost_usd(total_in, total_out) / len(rows) if rows else 0.0,
            "output_tokens_mean": total_out / len(called) if called else 0.0}


# ---------- Judge Claude + nhãn answer_type: xuất / nhập (mù biến thể) ----------

def pooled_items(names: list[str]) -> tuple[list[dict], dict]:
    """Gộp câu trả lời của nhiều lượt; câu trả lời giống hệt từng ký tự trong cùng câu hỏi chỉ chấm một lần.
    `item` là số mờ (không lộ biến thể); map item → [(lượt, case_index)] để nhập điểm lại."""
    by_case = {c["case_index"]: c for c in load_golden_cases("full")}
    unique: dict[tuple[int, str], list] = defaultdict(list)
    for name in names:
        for row in _read(name):
            if row["error"] is None:
                unique[(row["case_index"], row["answer"])].append((name, row["case_index"]))
    keys = sorted(unique)
    random.Random(SEED).shuffle(keys)
    items, mapping = [], {}
    for item, key in enumerate(keys, 1):
        case = by_case[key[0]]
        items.append({"case_index": item, "question": case["question"],
                      "reference_answer": case["reference_answer"], "answer": key[1]})
        mapping[item] = unique[key]
    return items, mapping


def write_batches(directory: Path, items: list[dict], size: int) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for start in range(0, len(items), size):
        path = directory / f"batch_{start // size + 1:02d}.jsonl"
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in items[start:start + size]),
                        encoding="utf-8")


def read_scores(directory: Path, prefix: str) -> list[dict]:
    return [json.loads(line) for path in sorted(directory.glob(f"{prefix}_*.jsonl"))
            for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# ---------- G2.3 phát lại validator citation ----------

def citation_error(answer: str, n_sources: int, single_source_policy: bool) -> str | None:
    """Validator production trên id nguồn thật của lượt (1..n). Chính sách thay thế (A 11:22): context chỉ có một
    nguồn và câu trả lời không có `[n]` ⇒ gán nguồn đó thay vì lỗi. (Vế "mọi câu thiếu [n] thuộc một nguồn duy nhất
    được trích" không đổi gì: validator chỉ báo "no citation" khi câu trả lời không có `[n]` nào.)"""
    sources = [PackedSource(id=i, title="", heading_path=(), excerpts=("",)) for i in range(1, n_sources + 1)]
    try:
        select_cited_sources(answer, sources)
    except CitationIntegrityError as exc:
        if single_source_policy and n_sources == 1 and str(exc) == "Grounded answer has no citation":
            return None
        return str(exc)
    return None


# ---------- Phân tích ----------

def attach_labels(name: str, judge: str = "judge") -> list[dict]:
    """Câu trả lời của lượt + điểm judge + answer_type (theo map) + nhóm (a)/(b) theo đoạn đúng trong context."""
    mapping = json.loads((OUT_DIR / judge / "map.json").read_text(encoding="utf-8"))["items"]
    scores = {r["case_index"]: r for r in read_scores(OUT_DIR / judge, "scores")}
    types = {r["case_index"]: r["answer_type"] for r in read_scores(OUT_DIR / judge, "types")}
    owner = {(run, case): int(item) for item, pairs in mapping.items() for run, case in pairs}
    gold, g4 = load_gold(GOLD_PATH), _g4_context_gold()
    rows = []
    for row in _read(name):
        item = owner.get((name, row["case_index"]))
        if item is not None and item in scores:
            row.update({k: scores[item][k] for k in ("accuracy", "completeness", "relevance")})
            row["answer_type"] = types.get(item)
        if row["case_index"] in gold:
            row["has_gold"] = True
            row["context_gold"] = g4.get(row["case_index"])
        rows.append(row)
    return rows


def _g4_context_gold() -> dict[int, float]:
    """Đoạn đúng đủ trong 5 đoạn runtime (G1 `runtime.jsonl`, dev, tất định) — để tách nhóm (a)/(b)."""
    path = REPO_ROOT / "data/phase_8_1/g1/runtime.jsonl"
    return {r["case_index"]: r["context5_gold_all"] for r in map(json.loads, path.read_text().splitlines())
            if "context5_gold_all" in r}


def paired(a_rows: list[dict], b_rows: list[dict], metric: str, filt=lambda r: True) -> dict | None:
    a = {r["case_index"]: r for r in a_rows if filt(r) and r.get(metric) is not None}
    b = {r["case_index"]: r for r in b_rows if filt(r) and r.get(metric) is not None}
    common = sorted(a.keys() & b.keys())
    if not common:
        return None
    diffs = np.array([float(b[i][metric]) - float(a[i][metric]) for i in common])
    stats = bootstrap_mean_diff(diffs, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)
    return {"n": len(common), "mean_a": float(np.mean([float(a[i][metric]) for i in common])),
            "mean_b": float(np.mean([float(b[i][metric]) for i in common])), "mean_diff": float(diffs.mean()),
            **stats, "wins": int((diffs > 0).sum()), "ties": int((diffs == 0).sum()),
            "losses": int((diffs < 0).sum()), "verdict": verdict(metric, stats["ci95"])}


def analyze(base: str, variants: list[str], realism: str | None, judge: str = "judge") -> dict:
    a_all = attach_labels(base, judge)
    a = keep_realism(a_all, realism)
    out = {"base": base, "realism": realism, "variants": {}}
    in_scope = lambda r: r["category"] != OUT_OF_SCOPE
    for name in variants:
        b_all = attach_labels(name, judge)
        b = keep_realism(b_all, realism)
        a_err = {r["case_index"] for r in a_all if r["citation_error"]}
        b_err = {r["case_index"] for r in b_all if r["citation_error"]}
        res = {m: paired(a, b, m, in_scope) for m in ("completeness", "accuracy", "relevance")}
        res["refusal_in_scope"] = paired(a, b, "refusal", in_scope)
        res["group_a_completeness"] = paired(a, b, "completeness", lambda r: r.get("context_gold") == 1.0)
        res["group_b_completeness"] = paired(a, b, "completeness", lambda r: in_scope(r) and r.get("context_gold") != 1.0)
        res["guardrails"] = {
            "oos_answered": sum(1 for r in b_all if r["category"] == OUT_OF_SCOPE and not r["refusal"]),
            "oos_answered_base": sum(1 for r in a_all if r["category"] == OUT_OF_SCOPE and not r["refusal"]),
            "citation_errors": len(b_err), "citation_errors_base": len(a_err),
            "citation_new": len(b_err - a_err), "citation_fixed": len(a_err - b_err),
            "usd_per_case": usage(b_all)["usd_per_case"], "usd_per_case_base": usage(a_all)["usd_per_case"],
            "output_tokens_mean": usage(b_all)["output_tokens_mean"],
            "output_tokens_mean_base": usage(a_all)["output_tokens_mean"],
        }
        res["answer_type"] = {t: sum(r.get("answer_type") == t for r in b if in_scope(r)) for t in ("full", "partial", "refusal")}
        res["answer_type_base"] = {t: sum(r.get("answer_type") == t for r in a if in_scope(r)) for t in ("full", "partial", "refusal")}
        res["contains_refusal_sentence"] = sum(INSUFFICIENT_ANSWER in (r["answer"] or "") and not r["refusal"] for r in b)
        res["unscored"] = sum(r.get("completeness") is None for r in b_all if not r["error"])
        out["variants"][name] = res
    if len(variants) > 1:  # Holm trong nhóm (plan §2.1)
        for metric in ("completeness", "accuracy"):
            names = [n for n in variants if out["variants"][n][metric]]
            for n, p in zip(names, holm_adjust([out["variants"][n][metric]["p_value"] for n in names])):
                out["variants"][n][metric]["p_holm"] = p
                out["variants"][n][metric]["verdict_holm"] = out["variants"][n][metric]["verdict"] if p < 0.05 else "no_difference"
    return out


def _read(name: str) -> list[dict]:
    return [json.loads(line) for line in (OUT_DIR / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]


def _write(name: str, rows: list[dict]) -> Path:
    path = OUT_DIR / f"{name}.jsonl"
    if path.exists():
        raise SystemExit(f"{path} exists; choose a new --name")
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8.1 G2 generation experiments")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="sinh câu trả lời (paid gpt-6-luna)")
    run.add_argument("--variant", required=True, choices=list(VARIANTS))
    run.add_argument("--cases", required=True, choices=["pilot", "rest", "dev", "test_pilot", "test_rest", "test"])
    run.add_argument("--name", required=True)
    merge = commands.add_parser("merge", help="gộp pilot + rest thành một lượt 120 câu")
    merge.add_argument("--parts", required=True, nargs="+")
    merge.add_argument("--name", required=True)
    export = commands.add_parser("export-judge", help="gộp mù các lượt → lô chấm + lô answer_type")
    export.add_argument("--names", required=True, nargs="+")
    export.add_argument("--batch-size", type=int, default=20)
    export.add_argument("--judge", default="judge", help="thư mục lô chấm trong data/phase_8_1/g2/")
    check = commands.add_parser("check-judge", help="kiểm đủ điểm + nhãn cho mọi item")
    check.add_argument("--judge", default="judge")
    ana = commands.add_parser("analyze")
    ana.add_argument("--base", required=True)
    ana.add_argument("--b", required=True, nargs="+")
    ana.add_argument("--realism", choices=["main", "natural"])
    ana.add_argument("--judge", default="judge")
    replay = commands.add_parser("replay-citation", help="G2.3: validator hiện tại vs chính sách một nguồn")
    replay.add_argument("--files", required=True, nargs="+", help="file câu trả lời JSONL (đường dẫn)")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.command == "run":
        started = time.strftime("%Y-%m-%d %H:%M:%S %z")
        rows = asyncio.run(run_variant(args.variant, select(args.cases)))
        path = _write(args.name, rows)
        meta = {"name": args.name, "variant": args.variant, "cases": args.cases, "started": started,
                "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"), "usage": usage(rows),
                "golden_md5": hashlib.md5(GOLDEN_FULL.read_bytes()).hexdigest(),
                "definition": dict(zip(("max_context_documents", "answer_instructions", "reasoning_effort",
                                        "doc_order"), VARIANTS[args.variant]))}
        (OUT_DIR / f"{args.name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                                        encoding="utf-8")
        print(path, json.dumps({k: meta[k] for k in ("usage", "golden_md5")}, ensure_ascii=False))
    elif args.command == "merge":
        rows = [r for part in args.parts for r in _read(part)]
        if len({r["case_index"] for r in rows}) != len(rows):
            raise SystemExit("duplicated case_index across parts")
        print(_write(args.name, sorted(rows, key=lambda r: r["case_index"])), json.dumps(usage(rows)))
    elif args.command == "export-judge":
        items, mapping = pooled_items(args.names)
        judge_dir = OUT_DIR / args.judge
        if judge_dir.exists():
            raise SystemExit(f"{judge_dir} exists")
        write_batches(judge_dir, items, args.batch_size)
        (judge_dir / "map.json").write_text(json.dumps({"names": args.names, "items": mapping}, indent=1) + "\n")
        print(json.dumps({"items": len(items), "answers": sum(len(v) for v in mapping.values()),
                          "batches": -(-len(items) // args.batch_size)}))
    elif args.command == "check-judge":
        judge_dir = OUT_DIR / args.judge
        items = {json.loads(l)["case_index"] for p in judge_dir.glob("batch_*.jsonl") for l in p.read_text().splitlines()}
        scores, types = read_scores(judge_dir, "scores"), read_scores(judge_dir, "types")
        print(json.dumps({"items": len(items), "score_errors": validate_score_rows(scores),
                          "scores_missing": sorted(items - {r["case_index"] for r in scores}),
                          "types_missing": sorted(items - {r["case_index"] for r in types}),
                          "types_bad": [r for r in types if r.get("answer_type") not in ("full", "partial", "refusal")]}))
    elif args.command == "analyze":
        print(json.dumps(analyze(args.base, args.b, args.realism, args.judge), ensure_ascii=False, indent=2))
    else:
        out = {}
        for file in args.files:
            rows = [json.loads(l) for l in Path(file).read_text(encoding="utf-8").splitlines()]
            rows = [r for r in rows if r.get("answer") and r.get("context_sources")]
            now = {r["case_index"] for r in rows if citation_error(r["answer"], r["context_sources"], False)}
            alt = {r["case_index"] for r in rows if citation_error(r["answer"], r["context_sources"], True)}
            stored = {r["case_index"] for r in rows if r.get("citation_error")}
            out[file] = {"n": len(rows), "stored_errors": len(stored), "replay_current": len(now),
                         "replay_matches_stored": now == stored, "single_source_policy": len(alt),
                         "changed_cases": sorted(now - alt)}
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
