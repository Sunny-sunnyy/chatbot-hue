"""Pure retrieval metrics: binary relevance, recall/MRR/nDCG and diagnostics.

Relevance is binary (1/0): Phase 7 never assigns graded relevance. Metric
functions accept the real RetrievalService output objects, so the same code
serves tests and live runs. Nothing here touches a provider or a vector
store.
"""
import math
import re
import statistics
import unicodedata

METRIC_KEYS = (
    "recall_at_1",
    "recall_at_3",
    "recall_at_5",
    "recall_at_10",
    "mrr_at_10",
    "ndcg_at_5",
    "ndcg_at_10",
)

_WHITESPACE_RE = re.compile(r"\s+")


def _normalize(text):
    """NFC + casefold + collapsed whitespace; Vietnamese diacritics survive."""
    text = unicodedata.normalize("NFC", text)
    text = text.casefold()
    return _WHITESPACE_RE.sub(" ", text).strip()


def evidence_units(relevant_sources, relevant_sections):
    """Return ground-truth units as (source, section|None) pairs.

    A source with declared sections contributes one unit per section; a
    source without declared sections contributes a single unit matching any
    section of that source.
    """
    units = set()
    for source in relevant_sources:
        if source in relevant_sections:
            units.update((source, section) for section in relevant_sections[source])
        else:
            units.add((source, None))
    return units


def _dedup_ranked(retrieved):
    """Keep the first occurrence of each (source, section) pair in rank order."""
    seen = set()
    ranked = []
    for item in retrieved:
        key = (item.metadata.get("source"), item.metadata.get("section"))
        if key in seen:
            continue
        seen.add(key)
        ranked.append(item)
    return ranked


def matched_units(retrieved, units):
    """Return {unit: first 1-based rank} over deduplicated retrieved items."""
    first_rank = {}
    for rank, item in enumerate(_dedup_ranked(retrieved), start=1):
        source = item.metadata.get("source")
        section = item.metadata.get("section")
        if (source, section) in units:
            unit = (source, section)
        elif (source, None) in units:
            unit = (source, None)
        else:
            continue
        if unit not in first_rank:
            first_rank[unit] = rank
    return first_rank


def _ndcg(matched_ranks, total_units, k):
    """Binary nDCG@k: relevant units are ordered by their first rank."""
    dcg = sum(
        1.0 / math.log2(rank + 1) for rank in matched_ranks if rank <= k
    )
    idcg = sum(
        1.0 / math.log2(i + 1) for i in range(1, min(total_units, k) + 1)
    )
    return dcg / idcg if idcg else 0.0


def case_metrics(retrieved, relevant_sources, relevant_sections):
    """Per-case retrieval metrics for one case against its gold evidence.

    retrieved is the ranked response (RetrievedDocument-like objects).
    Returns recall at 1/3/5/10, MRR@10, nDCG@5/10, first relevant rank and
    unit counts. An empty relevant set is always rejected.
    """
    units = evidence_units(relevant_sources, relevant_sections)
    if not units:
        raise ValueError("case has an empty relevant set; gold evidence is invalid")
    matches = matched_units(retrieved, units)
    matched_ranks = sorted(matches.values())
    return {
        "recall_at_1": sum(rank <= 1 for rank in matched_ranks) / len(units),
        "recall_at_3": sum(rank <= 3 for rank in matched_ranks) / len(units),
        "recall_at_5": sum(rank <= 5 for rank in matched_ranks) / len(units),
        "recall_at_10": sum(rank <= 10 for rank in matched_ranks) / len(units),
        "mrr_at_10": (
            1.0 / matched_ranks[0] if matched_ranks and matched_ranks[0] <= 10 else 0.0
        ),
        "ndcg_at_5": _ndcg(matched_ranks, len(units), 5),
        "ndcg_at_10": _ndcg(matched_ranks, len(units), 10),
        "first_relevant_rank": matched_ranks[0] if matched_ranks else None,
        "total_units": len(units),
        "matched_units": len(matches),
    }


def keyword_coverage(retrieved, keywords, k):
    """Fraction of keyword phrases found in the title+section+text of top k.

    Exact phrase matching over normalized text; a lexical diagnostic only,
    never a substitute for gold relevance and never a profile selector.
    """
    if k <= 0 or not keywords:
        return 0.0
    haystacks = [
        _normalize(
            f"{item.metadata.get('title', '')} "
            f"{item.metadata.get('section', '')} "
            f"{item.text}"
        )
        for item in retrieved[:k]
    ]
    covered = sum(
        1 for keyword in keywords if _normalize(keyword) in _haystack(haystacks)
    )
    if not covered:
        return 0.0
    return covered / len(keywords)


def _haystack(haystacks):
    return "\n".join(haystacks)


def latency_stats(values):
    """Median and nearest-rank p95 over per-case latencies in milliseconds."""
    if not values:
        return {"median_ms": None, "p95_ms": None}
    ordered = sorted(values)
    p95_index = min(math.ceil(0.95 * len(ordered)) - 1, len(ordered) - 1)
    return {
        "median_ms": statistics.median(ordered),
        "p95_ms": ordered[p95_index],
    }


def _mean(values):
    return sum(values) / len(values) if values else None


def aggregate_metrics(records):
    """Mean metrics overall, per category, macro recall@5 and latency stats.

    records must carry case_id, category, status, metrics and latency_ms per
    case (status "complete" or a failing status). The summary reports
    complete-case metrics plus effective Recall@5 where failed cases count 0.
    """
    complete = [r for r in records if r.get("status") == "complete"]

    def _item(items):
        item = {
            key: _mean([r["metrics"][key] for r in items]) for key in METRIC_KEYS
        }
        item["cases_complete"] = len(items)
        return item

    def _effective(items, all_items):
        if not all_items:
            return None
        total = sum(
            (r.get("metrics") or {}).get("recall_at_5", 0.0)
            if r.get("status") == "complete"
            else 0.0
            for r in all_items
        )
        return total / len(all_items)

    overall = _item(complete)
    overall["cases_total"] = len(records)
    overall["effective_recall_at_5"] = _effective(complete, records)

    per_category = {}
    for category in sorted({r["category"] for r in records}):
        cat_records = [r for r in records if r["category"] == category]
        cat_item = _item([r for r in cat_records if r.get("status") == "complete"])
        cat_item["cases_total"] = len(cat_records)
        cat_item["effective_recall_at_5"] = _effective(cat_records, cat_records)
        per_category[category] = cat_item

    macro = (
        _mean([item["effective_recall_at_5"] for item in per_category.values()])
        if per_category
        else None
    )
    return {
        "overall": overall,
        "per_category": per_category,
        "macro_recall_at_5": macro,
        "cases_total": len(records),
    }
