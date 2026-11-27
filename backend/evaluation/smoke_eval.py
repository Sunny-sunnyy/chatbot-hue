"""Lệnh smoke eval gọn nhẹ (~14 ca cốt lõi, 0 câu kín) kiểm nhanh `/api/chat`.

Chạy từ `backend/`:
    uv run python -m evaluation.smoke_eval --base-url http://127.0.0.1:8010
    uv run python -m evaluation.smoke_eval --base-url http://127.0.0.1:8010 --dry-run

Chấm tất định bằng code (0 gọi LLM judge): HTTP 200, câu trả lời không rỗng,
từ chối đúng chuẩn cho câu ngoài kho/ngoài tỉnh, câu trong kho không từ chối +
có nguồn + không lộ mã `[n]` trần/mồ côi, lập lịch biểu mẫu hợp lệ, kiểm từ khoá
mềm (hit/miss), đo độ trễ p50/p95, ghi JSON chi tiết vào `data/smoke_eval/`.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import sys
import time
import unicodedata
from typing import Any

import httpx

from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER, REFUSAL_ANSWERS

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_SMOKE_PATH = REPO_ROOT / "knowledge-base-hue" / "evaluation" / "golden_full_corpus_smoke.jsonl"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "smoke_eval"

_RAW_PLACEHOLDER_RE = re.compile(r"\[n\]", re.IGNORECASE)
_UNNORMALIZED_NGUON_RE = re.compile(r"\[\s*nguồn\s*\d+\s*\]", re.IGNORECASE)
_WEB_CITATION_RE = re.compile(r"\[\s*w\s*\d+\s*\]", re.IGNORECASE)
_NUMERIC_CITATION_RE = re.compile(r"\[(\d+)\]")


@dataclass(frozen=True)
class SmokeCase:
    case_id: str
    kind: str  # "in_corpus" | "refusal" | "small_talk" | "itinerary"
    query: str
    payload: dict[str, Any]
    keywords: tuple[str, ...] = ()
    expected_days: int | None = None
    source_label: str = "product"


@dataclass
class CaseScore:
    case_id: str
    kind: str
    query: str
    passed: bool
    http_status: int | None
    latency_ms: float
    is_refusal: bool
    n_sources: int
    dangling_citations: list[str] = field(default_factory=list)
    keyword_hits: list[str] = field(default_factory=list)
    keyword_misses: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    answer_preview: str = ""


def _nfc_fold(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


def is_standard_refusal(answer: str) -> bool:
    """True khi câu trả lời khớp câu từ chối chuẩn hoặc mở đầu đúng khung từ chối."""
    text = unicodedata.normalize("NFC", answer or "").strip()
    if not text:
        return False
    normalized_refusals = tuple(unicodedata.normalize("NFC", r) for r in REFUSAL_ANSWERS)
    return text in normalized_refusals or any(text.startswith(r) for r in normalized_refusals)


def find_citation_leaks(answer: str, source_ids: set[int]) -> list[str]:
    """Phát hiện mã `[n]` trần, `[Nguồn n]` chưa chuẩn hoá, `[w n]` hoặc mã `[k]` không có trong `sources`."""
    leaks: list[str] = []
    if _RAW_PLACEHOLDER_RE.search(answer):
        leaks.append("[n]")
    if _UNNORMALIZED_NGUON_RE.search(answer):
        leaks.extend(m.group(0) for m in _UNNORMALIZED_NGUON_RE.finditer(answer))
    if _WEB_CITATION_RE.search(answer):
        leaks.extend(m.group(0) for m in _WEB_CITATION_RE.finditer(answer))
    for match in _NUMERIC_CITATION_RE.finditer(answer):
        cid = int(match.group(1))
        if cid not in source_ids:
            leaks.append(match.group(0))
    return leaks


def check_soft_keywords(answer: str, keywords: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """Kiểm từ khoá mềm (không phân biệt hoa/thường, chuẩn NFC, bỏ `[k]` trước khi dò)."""
    cleaned = _NUMERIC_CITATION_RE.sub("", answer or "")
    folded_answer = _nfc_fold(cleaned)
    hits: list[str] = []
    misses: list[str] = []
    for kw in keywords:
        if _nfc_fold(kw) in folded_answer:
            hits.append(kw)
        else:
            misses.append(kw)
    return hits, misses


def load_smoke_cases(golden_smoke_path: Path = GOLDEN_SMOKE_PATH) -> list[SmokeCase]:
    """Nạp 10 câu công khai từ `golden_full_corpus_smoke.jsonl` + 4 ca sản phẩm cốt lõi (0 câu kín)."""
    lines = [line for line in golden_smoke_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    cases: list[SmokeCase] = []
    for idx, line in enumerate(lines, start=1):
        row = json.loads(line)
        kind = "refusal" if row.get("category") == "out_of_scope" else "in_corpus"
        cases.append(
            SmokeCase(
                case_id=f"golden_{idx:02d}",
                kind=kind,
                query=row["question"],
                payload={"query": row["question"]},
                keywords=tuple(row.get("keywords") or ()),
                source_label=row.get("category", "golden"),
            )
        )

    product_cases = [
        SmokeCase(
            case_id="prod_out_of_province",
            kind="refusal",
            query="Ở Hội An nên ăn món gì?",
            payload={"query": "Ở Hội An nên ăn món gì?"},
            source_label="product_out_of_province",
        ),
        SmokeCase(
            case_id="prod_small_talk",
            kind="small_talk",
            query="Xin chào",
            payload={"query": "Xin chào"},
            source_label="product_small_talk",
        ),
        SmokeCase(
            case_id="prod_itinerary_form",
            kind="itinerary",
            query="lên lịch (2 ngày, 2 người lớn)",
            payload={
                "query": "lên lịch",
                "bieu_mau": True,
                "truong": {
                    "so_ngay": "2",
                    "nguoi_lon": 2,
                    "tre_em": 0,
                    "lon_tuoi": False,
                },
            },
            expected_days=2,
            source_label="product_itinerary_form",
        ),
        SmokeCase(
            case_id="prod_dai_noi_ticket",
            kind="in_corpus",
            query="Vé tham quan Đại Nội bao nhiêu?",
            payload={"query": "Vé tham quan Đại Nội bao nhiêu?"},
            keywords=("Đại Nội", "200.000"),
            source_label="product_ticket",
        ),
    ]
    return cases + product_cases


def _validate_itinerary_payload(body: dict[str, Any], expected_days: int | None) -> list[str]:
    errors: list[str] = []
    lich_trinh = body.get("lich_trinh")
    if not isinstance(lich_trinh, dict):
        return ["missing lich_trinh object"]
    lich = lich_trinh.get("lich")
    if not isinstance(lich, dict):
        return ["missing lich_trinh.lich object"]
    ngay = lich.get("ngay")
    if not isinstance(ngay, list) or not ngay:
        return ["missing lich_trinh.lich.ngay list"]
    if expected_days is not None and len(ngay) != expected_days:
        errors.append(f"expected {expected_days} days, got {len(ngay)}")
    for idx, day in enumerate(ngay, start=1):
        if not isinstance(day, dict):
            errors.append(f"day {idx} is not an object")
            continue
        muc = day.get("muc")
        if not isinstance(muc, list) or not muc:
            errors.append(f"day {idx} has no itinerary items")
    return errors


def score_case(
    case: SmokeCase,
    http_status: int | None,
    body: dict[str, Any] | None,
    latency_ms: float,
    request_error: str | None = None,
) -> CaseScore:
    """Chấm tất định 1 ca theo loại ca và phản hồi JSON từ `/api/chat`."""
    reasons: list[str] = []
    if request_error:
        reasons.append(f"request_error: {request_error}")
    if http_status != 200:
        reasons.append(f"http_status={http_status} (expected 200)")

    body_dict = body if isinstance(body, dict) else {}
    answer = str(body_dict.get("answer") or "").strip()
    sources = body_dict.get("sources")
    sources_list = sources if isinstance(sources, list) else []
    source_ids = {s["id"] for s in sources_list if isinstance(s, dict) and isinstance(s.get("id"), int)}

    if not answer:
        reasons.append("empty answer")

    refused = is_standard_refusal(answer)
    leaks = find_citation_leaks(answer, source_ids)
    if leaks:
        reasons.append(f"citation_leak: {leaks}")

    if case.kind == "refusal":
        if answer and not refused:
            reasons.append("expected standard refusal")
    elif case.kind == "small_talk":
        if refused:
            reasons.append("unexpected refusal on small_talk")
    elif case.kind in ("in_corpus", "itinerary"):
        if refused:
            reasons.append("unexpected refusal on in_corpus/itinerary")
        if not sources_list:
            reasons.append("empty sources")
        if case.kind == "itinerary" and http_status == 200:
            reasons.extend(_validate_itinerary_payload(body_dict, case.expected_days))

    hits, misses = check_soft_keywords(answer, case.keywords)
    return CaseScore(
        case_id=case.case_id,
        kind=case.kind,
        query=case.query,
        passed=not reasons,
        http_status=http_status,
        latency_ms=round(latency_ms, 1),
        is_refusal=refused,
        n_sources=len(sources_list),
        dangling_citations=leaks,
        keyword_hits=hits,
        keyword_misses=misses,
        reasons=reasons,
        answer_preview=answer[:140].replace("\n", " "),
    )


def percentile_ms(values: list[float], pct: float) -> float | None:
    """Tính phân vị độ trễ (ms) theo nội suy tuyến tính."""
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return round(ordered[0], 1)
    pos = (len(ordered) - 1) * (pct / 100.0)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return round(ordered[lo], 1)
    frac = pos - lo
    return round(ordered[lo] * (1.0 - frac) + ordered[hi] * frac, 1)


def _dry_run_fixture(case: SmokeCase) -> tuple[int, dict[str, Any], float]:
    """Phản hồi mẫu cho chế độ `--dry-run` (0 USD)."""
    if case.kind == "refusal":
        ans = OUT_OF_SCOPE_ANSWER if case.case_id == "prod_out_of_province" else INSUFFICIENT_ANSWER
        return 200, {"answer": ans, "sources": []}, 120.0
    if case.kind == "small_talk":
        return 200, {"answer": "Xin chào! Mình có thể hỗ trợ bạn tìm hiểu về văn hoá và du lịch Huế.", "sources": []}, 95.0
    if case.kind == "itinerary":
        return (
            200,
            {
                "answer": "Mình hiểu: 2 ngày · 2 người lớn. Ngày 1: Đại Nội [1]. Ngày 2: Chùa Thiên Mụ [2].",
                "sources": [{"id": 1, "title": "Đại Nội Huế"}, {"id": 2, "title": "Chùa Thiên Mụ"}],
                "lich_trinh": {
                    "phien_ban": 2,
                    "lich": {
                        "ngay": [
                            {"ngay": 1, "muc": [{"id_muc": "n1_s1", "ten": "Đại Nội Huế"}]},
                            {"ngay": 2, "muc": [{"id_muc": "n2_s1", "ten": "Chùa Thiên Mụ"}]},
                        ]
                    },
                },
            },
            310.0,
        )
    kw_hint = " — ".join(case.keywords) if case.keywords else case.query
    return (
        200,
        {
            "answer": f"Theo tư liệu Huế, {kw_hint} [1].",
            "sources": [{"id": 1, "title": "Nguồn mẫu"}],
        },
        180.0,
    )


def run_dry_run(cases: list[SmokeCase]) -> tuple[list[CaseScore], CaseScore, bool]:
    """Chạy bộ chấm trên toàn bộ tập câu mẫu + 1 ca cố tình FAIL làm đối chứng."""
    results: list[CaseScore] = []
    for case in cases:
        status, body, latency = _dry_run_fixture(case)
        results.append(score_case(case, status, body, latency))

    control_case = SmokeCase(
        case_id="control_intentional_fail",
        kind="in_corpus",
        query="Ca đối chứng cố tình lỗi (thiếu nguồn + lộ [n] trần)",
        payload={"query": "Ca đối chứng"},
        keywords=("Đại Nội",),
        source_label="dry_run_control",
    )
    control_score = score_case(
        control_case,
        http_status=200,
        body={"answer": "Giá vé là 200.000 đồng [n] [99].", "sources": []},
        latency_ms=50.0,
    )
    dry_ok = all(r.passed for r in results) and (not control_score.passed)
    return results, control_score, dry_ok


def run_live(cases: list[SmokeCase], base_url: str, timeout: float = 60.0) -> list[CaseScore]:
    """Gọi lần lượt từng ca tới `POST <base_url>/api/chat` (xoá cookie giữa mỗi ca để độc lập)."""
    url = base_url.rstrip("/") + "/api/chat"
    results: list[CaseScore] = []
    with httpx.Client(timeout=timeout) as client:
        for case in cases:
            client.cookies.clear()
            started = time.perf_counter()
            http_status: int | None = None
            body: dict[str, Any] | None = None
            err: str | None = None
            try:
                resp = client.post(url, json=case.payload)
                http_status = resp.status_code
                try:
                    body = resp.json()
                except ValueError:
                    body = None
            except Exception as exc:
                err = f"{type(exc).__name__}: {exc}"
            elapsed_ms = (time.perf_counter() - started) * 1000.0
            results.append(score_case(case, http_status, body, elapsed_ms, request_error=err))
    return results


def default_output_path(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return output_dir / f"smoke_eval_{stamp}.json"


def format_summary_table(
    results: list[CaseScore],
    p50: float | None,
    p95: float | None,
    control_score: CaseScore | None = None,
) -> str:
    header = (
        f"{'CASE_ID':<26} {'KIND':<11} {'RES':<5} {'HTTP':<4} {'MS':>7} "
        f"{'SRC':>3} {'REF':>3} {'KW':>5}  NOTE"
    )
    lines = [header, "-" * len(header)]
    all_rows = [*results, *([control_score] if control_score is not None else [])]
    for r in all_rows:
        res = "PASS" if r.passed else "FAIL"
        http_str = "-" if r.http_status is None else str(r.http_status)
        total_kw = len(r.keyword_hits) + len(r.keyword_misses)
        kw_str = f"{len(r.keyword_hits)}/{total_kw}" if total_kw else "-"
        ref_str = "Y" if r.is_refusal else "N"
        note = "; ".join(r.reasons) if r.reasons else (f"miss={r.keyword_misses}" if r.keyword_misses else "ok")
        lines.append(
            f"{r.case_id:<26} {r.kind:<11} {res:<5} {http_str:<4} {r.latency_ms:>7.1f} "
            f"{r.n_sources:>3} {ref_str:>3} {kw_str:>5}  {note}"
        )
    passed_count = sum(1 for r in results if r.passed)
    lines.append("-" * len(header))
    lines.append(
        f"Summary: {passed_count}/{len(results)} PASS | p50={p50} ms | p95={p95} ms"
        + (f" | control_fail={'CAUGHT' if control_score and not control_score.passed else 'MISSED'}" if control_score else "")
    )
    return "\n".join(lines)


def build_report(
    *,
    mode: str,
    base_url: str,
    results: list[CaseScore],
    overall_passed: bool,
    control_score: CaseScore | None = None,
) -> dict[str, Any]:
    latencies = [r.latency_ms for r in results]
    p50 = percentile_ms(latencies, 50.0)
    p95 = percentile_ms(latencies, 95.0)
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "base_url": base_url,
        "total_cases": len(results),
        "passed_cases": sum(1 for r in results if r.passed),
        "failed_cases": sum(1 for r in results if not r.passed),
        "overall_passed": overall_passed,
        "latency_ms": {"p50": p50, "p95": p95},
        "control_case": asdict(control_score) if control_score is not None else None,
        "results": [asdict(r) for r in results],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke eval tất định cho hue_rag (/api/chat).")
    parser.add_argument("--base-url", default="http://127.0.0.1:8010", help="Địa chỉ server đang chạy.")
    parser.add_argument("--dry-run", action="store_true", help="Chạy 0 USD trên phản hồi mẫu + ca đối chứng FAIL.")
    parser.add_argument("--output", type=Path, default=None, help="Đường dẫn file JSON kết quả (mặc định data/smoke_eval/).")
    parser.add_argument("--timeout", type=float, default=60.0, help="Timeout mỗi yêu cầu HTTP (giây).")
    args = parser.parse_args(argv)

    cases = load_smoke_cases()
    control_score: CaseScore | None = None
    if args.dry_run:
        results, control_score, overall_passed = run_dry_run(cases)
        mode = "dry_run"
    else:
        results = run_live(cases, base_url=args.base_url, timeout=args.timeout)
        overall_passed = all(r.passed for r in results)
        mode = "live"

    report = build_report(
        mode=mode,
        base_url=args.base_url,
        results=results,
        overall_passed=overall_passed,
        control_score=control_score,
    )
    out_path = args.output if args.output is not None else default_output_path()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    table = format_summary_table(
        results,
        p50=report["latency_ms"]["p50"],
        p95=report["latency_ms"]["p95"],
        control_score=control_score,
    )
    print(table)
    print(f"JSON report: {out_path}")
    return 0 if overall_passed else 1


if __name__ == "__main__":
    sys.exit(main())
