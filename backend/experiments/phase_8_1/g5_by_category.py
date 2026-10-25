"""Phase 8.1 G5 — chỉ số quyết của các gate chính, tách theo loại câu (review G5 M1; spec §6 tiêu chí 2).

Chỉ đọc JSONL đã lưu (G2, G3, G4, G4K), 0 USD. Theo cặp trên câu số chính (bỏ `unnatural`): chênh B − A, thắng/hòa/thua,
n; CI 95% bootstrap (10.000, seed 20261024) chỉ khi n ≥ 10 (A 25/10), còn lại ghi "mô tả".

Chạy từ `backend/`: HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g5_by_category
"""
import json

import numpy as np

from evaluation.full_corpus_eval import BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED, REPO_ROOT, bootstrap_mean_diff
from experiments.phase_8_1.g1_retrieval import keep_realism
from experiments.phase_8_1.g2_generate import attach_labels

DATA = REPO_ROOT / "data/phase_8_1"
CATEGORIES = ("direct_fact", "multi_source", "conditional", "comparative", "out_of_scope")
MIN_N_FOR_CI = 10


def _jsonl(path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def by_category(a_rows: list[dict], b_rows: list[dict], metric: str) -> list[dict]:
    a = {r["case_index"]: r for r in keep_realism(a_rows, "main") if r.get(metric) is not None}
    b = {r["case_index"]: r for r in b_rows if r.get(metric) is not None}
    out = []
    for category in CATEGORIES + ("tất cả",):
        common = sorted(i for i in a.keys() & b.keys() if category == "tất cả" or a[i]["category"] == category)
        if not common:
            continue
        diffs = np.array([float(b[i][metric]) - float(a[i][metric]) for i in common])
        row = {"category": category, "n": len(common), "mean_a": float(np.mean([float(a[i][metric]) for i in common])),
               "mean_b": float(np.mean([float(b[i][metric]) for i in common])), "diff": float(diffs.mean()),
               "wtl": f"{int((diffs > 0).sum())}/{int((diffs == 0).sum())}/{int((diffs < 0).sum())}", "ci": "mô tả"}
        if len(common) >= MIN_N_FOR_CI:
            low, high = bootstrap_mean_diff(diffs, BOOTSTRAP_ROUNDS, BOOTSTRAP_SEED)["ci95"]
            row["ci"] = f"[{low:+.3f}; {high:+.3f}]"
        out.append(row)
    return out


def comparisons() -> list[tuple[str, str, list[dict], list[dict]]]:
    g4, g4k, g3 = DATA / "g4", DATA / "g4k", DATA / "g3"
    return [
        ("G2.1a context 10 — dev", "completeness", attach_labels("g20_baseline"), attach_labels("g2_context10")),
        ("G2.1a context 10 — test", "completeness", attach_labels("t_baseline", "judge_test"),
         attach_labels("t_context10", "judge_test")),
        ("G4-A luna listwise vs runtime (dev 30)", "context5_gold_all", _jsonl(g4 / "base_runtime.jsonl"),
         _jsonl(g4 / "a_luna_plain.jsonl")),
        ("G4-A M1 đoạn trơn vs runtime (dev 30)", "context5_gold_all", _jsonl(g4 / "base_runtime.jsonl"),
         _jsonl(g4 / "a_m1_plain.jsonl")),
        ("G4K E khử dấu · native · câu không dấu", "context5_gold_all", _jsonl(g4k / "n0_na.jsonl"),
         _jsonl(g4k / "e_native_na.jsonl")),
        ("G3 H2 512 vs H1 (ngân sách 750)", "ctxB_gold_all", _jsonl(g3 / "h1.jsonl"), _jsonl(g3 / "h1-h2_512.jsonl")),
        ("G3 B10: H2 512 vs H1 (ngân sách 1.500)", "ctxB10_gold_all", _jsonl(g3 / "b10_h1.jsonl"),
         _jsonl(g3 / "b10_h1-h2_512.jsonl")),
    ]


def main() -> None:
    for title, metric, a_rows, b_rows in comparisons():
        print(f"\n**{title}** — chỉ số `{metric}`\n")
        print("| Loại câu | n | A | B | chênh B − A | thắng/hòa/thua | CI 95% |")
        print("|---|---:|---:|---:|---:|---|---|")
        for r in by_category(a_rows, b_rows, metric):
            print(f"| {r['category']} | {r['n']} | {r['mean_a']:.3f} | {r['mean_b']:.3f} | {r['diff']:+.3f} | {r['wtl']} | {r['ci']} |")


if __name__ == "__main__":
    main()
