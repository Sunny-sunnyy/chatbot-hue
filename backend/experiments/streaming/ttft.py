"""C70 — đo "thời gian tới chữ đầu tiên" khi stream câu trả lời (chưa đổi chatbot).

Plan + tiêu chí ghi trước: `report_agent/2026-10-27_phan_ton_phase_cu/streaming_ttft_plan.md` (A duyệt sha `9683641b6c38`) §3, §4, §6, §7.
Ba ô, cùng câu, cùng context (production, `settings.yaml` = 10), chạy theo thứ tự S10 → D10 → N10 để S10 luôn là lần gọi đầu với prompt đó
(không dính cache prompt — plan §4):
  S10 = `Runner.run_streamed` với chính `generator.answer_agent` (đường stream sẽ dùng nếu bật streaming);
  D10 = SDK OpenAI `responses.create(stream=True)` trực tiếp, cùng instructions / schema JSON (mốc: lớp Agents SDK thêm trễ bao nhiêu);
  N10 = `generator.generate_answer` — đúng hàm production hôm nay (không stream).
Mốc thời gian tính lại từ sự kiện đã lưu (`timeline`), không từ số ghi tay. Paid: chỉ lệnh `run` (`gpt-6-luna`).

Chạy từ `backend/` (pilot trước, A báo lúc được chạy — không chạy chồng lượt trả phí khác):
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.streaming.ttft run --pilot --name pilot
  HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m experiments.streaming.ttft run --name main
  HF_HUB_OFFLINE=1 uv run python -m experiments.streaming.ttft summarize --names main
"""
import argparse
import asyncio
import hashlib
import json
import random
import re
import subprocess
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
from agents import RunConfig, Runner
from agents.agent_output import AgentOutputSchema

from core.schema import CitationIntegrityError
from core.settings_loader import load_settings
from evaluation.full_corpus_eval import REPO_ROOT, build_context_builder, build_retrieval, cost_usd, is_refusal
from llm.citations import CITATION_PATTERN, normalize_citations, select_cited_sources
from llm.full_corpus_prompt import ANSWER_SYSTEM_INSTRUCTIONS, INSUFFICIENT_ANSWER, build_answer_input
from llm.generator_openai_full_corpus import AnswerOutput, OpenAIFullCorpusGenerator, parse_structured_output

OUT_DIR = REPO_ROOT / "data/streaming_ttft_2026-10-28"
QUESTIONS = OUT_DIR / "questions.jsonl"
SEED = 20261028
CELLS = ("S10", "D10", "N10")
PILOT = {"ids": ("q03", "q09"), "cells": ("S10", "D10")}
# Câu khởi động (không tính): tự viết, không có trong bộ câu, không lấy từ Golden.
WARMUP_QUERY = "Ở Huế buổi sáng nên ăn món gì?"
MAX_CONSECUTIVE_ERRORS = 2  # plan §8: 2 lỗi provider liên tiếp ⇒ dừng
BOOTSTRAP_ROUNDS = 10_000

# Luồng chữ của đầu ra có cấu trúc là JSON `{"answer":"…`: chữ người dùng thấy bắt đầu sau tiền tố này (plan §3).
ANSWER_PREFIX = re.compile(r'^\s*\{\s*"answer"\s*:\s*"')
# Kết câu trong chuỗi JSON thô: dấu câu rồi khoảng trắng / `\n` thoát / hết chuỗi, hoặc xuống dòng thoát, hoặc dấu `"` đóng chuỗi.
# Ước kiểu B (plan §3): không xử lý `TP.` — `1.000` không khớp vì sau dấu chấm là chữ số.
SENTENCE_END = re.compile(r'[.!?](?=\s|\\n|")|\\n|(?<!\\)"')


# ---------- Mốc thời gian từ sự kiện (logic thuần, có test) ----------

def timeline(events: list[dict]) -> dict:
    """Từ danh sách sự kiện `{"ms", "type", "delta"?, "item_type"?}` của một lần gọi stream ⇒ các mốc ms của plan §3 (None nếu không có)."""
    marks = dict.fromkeys(("t_first_event", "t_reasoning_done", "t_first_delta", "t_first_visible",
                           "t_first_cited_sentence", "t_refusal_complete", "t_last_event"))
    if not events:
        return marks
    marks["t_first_event"], marks["t_last_event"] = events[0]["ms"], events[-1]["ms"]
    text = ""
    for event in events:
        if event["type"] == "response.output_item.done" and event.get("item_type") == "reasoning" and marks["t_reasoning_done"] is None:
            marks["t_reasoning_done"] = event["ms"]
        if event["type"] != "response.output_text.delta":
            continue
        if marks["t_first_delta"] is None:
            marks["t_first_delta"] = event["ms"]
        text += event["delta"]
        prefix = ANSWER_PREFIX.match(text)
        if prefix is None:
            continue
        answer = text[prefix.end():]
        if marks["t_first_visible"] is None and answer:
            marks["t_first_visible"] = event["ms"]
        if marks["t_first_cited_sentence"] is None and _has_cited_sentence(answer):
            marks["t_first_cited_sentence"] = event["ms"]
        if marks["t_refusal_complete"] is None and answer.startswith(INSUFFICIENT_ANSWER):
            marks["t_refusal_complete"] = event["ms"]
    return marks


def _has_cited_sentence(answer: str) -> bool:
    citation = CITATION_PATTERN.search(answer)
    return citation is not None and SENTENCE_END.search(answer, citation.end()) is not None


# ---------- Ghi sự kiện ----------

def _elapsed_ms(t0: float) -> float:
    return round((time.perf_counter() - t0) * 1000, 1)


def record_event(event, t0: float, events: list[dict]) -> dict | None:
    """Ghi một sự kiện Responses API; trả usage (dict) khi gặp `response.completed`."""
    row = {"ms": _elapsed_ms(t0), "type": event.type}
    if event.type == "response.output_text.delta":
        row["delta"] = event.delta
    elif event.type == "response.output_item.done":
        row["item_type"] = event.item.type
    events.append(row)
    if event.type == "response.completed":
        # to_dict() bỏ trường provider không gửi ⇒ thiếu `cached_tokens` thì là None ("không đo được"), không phải 0 (review B n-1).
        return event.response.to_dict().get("usage")
    return None


def usage_fields(usage: dict | None) -> dict:
    usage = usage or {}
    return {
        "input_tokens": usage.get("input_tokens"),
        "cached_tokens": (usage.get("input_tokens_details") or {}).get("cached_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "reasoning_tokens": (usage.get("output_tokens_details") or {}).get("reasoning_tokens"),
    }


# ---------- Ba ô đo ----------

async def call_s10(generator: OpenAIFullCorpusGenerator, prompt: str) -> dict:
    # RunConfig giống `_execute_agent` (generator_openai_full_corpus.py:162-165); max_turns=1 như production.
    run_config = RunConfig(tracing_disabled=True, trace_include_sensitive_data=False)
    events: list[dict] = []
    usage = None
    t0 = time.perf_counter()
    result = Runner.run_streamed(generator.answer_agent, input=prompt, max_turns=1, run_config=run_config)

    async def consume():
        nonlocal usage
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                usage = record_event(event.data, t0, events) or usage

    try:
        # run_streamed trả ngay; model chạy trong vòng stream_events ⇒ timeout bọc cả vòng; hết giờ / lỗi thì hủy task nền (review B m-3).
        await asyncio.wait_for(consume(), generator.timeout)
    finally:
        if not result.is_complete:
            result.cancel()
    t_done = _elapsed_ms(t0)
    text = parse_structured_output(result.final_output, AnswerOutput)
    return {"text": text, "t_done": t_done, "events": events, **usage_fields(usage)}


async def call_d10(generator: OpenAIFullCorpusGenerator, prompt: str) -> dict:
    schema = AgentOutputSchema(AnswerOutput)
    events: list[dict] = []
    usage = None
    t0 = time.perf_counter()
    # Cùng tham số Agents SDK gửi cho agent này (`agents/models/openai_responses.py:1927-1938` + ModelSettings ở generator `:116-121`).
    stream = await generator.client.responses.create(
        model=generator.model,
        instructions=ANSWER_SYSTEM_INSTRUCTIONS,
        input=[{"role": "user", "content": prompt}],
        max_output_tokens=generator.answer_max_output_tokens,
        store=False,
        stream=True,
        text={"format": {"type": "json_schema", "name": "final_output",
                         "schema": schema.json_schema(), "strict": schema.is_strict_json_schema()}},
    )

    async def consume():
        nonlocal usage
        async for event in stream:
            usage = record_event(event, t0, events) or usage

    try:
        await asyncio.wait_for(consume(), generator.timeout)
    finally:
        await stream.close()
    t_done = _elapsed_ms(t0)
    raw = "".join(e["delta"] for e in events if e["type"] == "response.output_text.delta")
    return {"text": parse_structured_output(raw, AnswerOutput), "t_done": t_done, "events": events, **usage_fields(usage)}


async def call_n10(generator: OpenAIFullCorpusGenerator, query: str, context: str) -> dict:
    t0 = time.perf_counter()
    generated = await generator.generate_answer(query, context)
    t_done = _elapsed_ms(t0)
    # generate_answer chỉ trả usage qua SDK (cached_tokens mặc định 0 dù provider không gửi) ⇒ ghi None = không đo được.
    return {"text": generated.text, "t_done": t_done, "events": [], "input_tokens": generated.input_tokens,
            "cached_tokens": None, "output_tokens": generated.output_tokens, "reasoning_tokens": generated.reasoning_tokens}


async def measure(cell: str, generator, query: str, packed) -> dict:
    """Một lần gọi ⇒ dòng kết quả. Lỗi bất kỳ ⇒ dòng lỗi (chỉ tên lớp lỗi, không thông điệp), không retry (run-experiment §3.8)."""
    prompt = build_answer_input(query, packed.text)
    try:
        if cell == "S10":
            out = await call_s10(generator, prompt)
        elif cell == "D10":
            out = await call_d10(generator, prompt)
        else:
            out = await call_n10(generator, query, packed.text)
    except Exception as exc:
        chain = type(exc).__name__ + (f" <- {type(exc.__cause__).__name__}" if exc.__cause__ else "")
        return {"error": chain, "events": [], "t_done": None, "refusal": None, "valid": False, "citation_error": None,
                "input_tokens": None, "cached_tokens": None, "output_tokens": None, "reasoning_tokens": None}
    text = out.pop("text")
    try:
        # Đúng điều kiện trả 200 của chat.py:176-190.
        select_cited_sources(normalize_citations(text), packed.sources)
        citation_error = False
    except CitationIntegrityError:
        citation_error = True
    return {**out, "error": None, "refusal": is_refusal(text), "valid": not citation_error, "citation_error": citation_error}


# ---------- Chạy ----------

def sha12(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")
        file.flush()


async def run(name: str, pilot: bool) -> None:
    rows_path, events_path, meta_path = (OUT_DIR / f"{name}{suffix}" for suffix in (".jsonl", ".events.jsonl", ".meta.json"))
    for path in (rows_path, events_path, meta_path):
        if path.exists():
            raise SystemExit(f"exists: {path}")  # không ghi đè lượt cũ
    questions = read_jsonl(QUESTIONS)
    if pilot:
        questions, cells = [q for q in questions if q["id"] in PILOT["ids"]], PILOT["cells"]
    else:
        random.Random(SEED).shuffle(questions)
        cells = CELLS
    meta = {"name": name, "pilot": pilot, "plan_sha": "9683641b6c38", "questions": str(QUESTIONS.relative_to(REPO_ROOT)),
            "questions_sha": sha12(QUESTIONS), "order": [q["id"] for q in questions], "cells": list(cells),
            "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT).stdout.strip(),
            "sdk": {"openai-agents": version("openai-agents"), "openai": version("openai")},
            "started": time.strftime("%H:%M:%S %d/%m/%Y"), "finished": None, "stopped": None}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    context_builder = build_context_builder(settings)
    generator = OpenAIFullCorpusGenerator.from_environment(settings)
    meta["model"], meta["max_context_documents"] = generator.model, settings["full_corpus_generation"]["max_context_documents"]
    consecutive_errors = 0
    try:
        jobs = [({"id": "warmup", "scope": "warmup", "type": "warmup", "query": WARMUP_QUERY}, ("N10",))] if not pilot else []
        jobs += [(q, cells) for q in questions]
        for question, job_cells in jobs:
            t0 = time.perf_counter()
            result = await asyncio.to_thread(service.search, question["query"])
            search_ms = _elapsed_ms(t0)
            t0 = time.perf_counter()
            packed = context_builder.build(question["query"], result.documents)
            context_ms = _elapsed_ms(t0)
            for cell in job_cells:
                out = await measure(cell, generator, question["query"], packed)
                events = out.pop("events")
                row = {"id": question["id"], "scope": question["scope"], "type": question["type"], "cell": cell,
                       "search_ms": search_ms, "context_ms": context_ms, "n_context_sources": len(packed.sources), **out}
                append_jsonl(rows_path, row)
                append_jsonl(events_path, {"id": question["id"], "cell": cell, "events": events})
                marks = timeline(events)
                print(question["id"], cell, "error" if out["error"] else "ok", "first_visible", marks["t_first_visible"],
                      "done", out["t_done"], "cached", out["cached_tokens"], flush=True)
                consecutive_errors = consecutive_errors + 1 if out["error"] else 0
                if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                    meta["stopped"] = f"{MAX_CONSECUTIVE_ERRORS} lỗi liên tiếp"
                    return
    finally:
        rows = read_jsonl(rows_path) if rows_path.exists() else []
        tokens_in = sum(r["input_tokens"] or 0 for r in rows)
        tokens_out = sum(r["output_tokens"] or 0 for r in rows)
        meta.update(finished=time.strftime("%H:%M:%S %d/%m/%Y"), n_rows=len(rows), errors=sum(bool(r["error"]) for r in rows),
                    input_tokens=tokens_in, output_tokens=tokens_out, usd=round(cost_usd(tokens_in, tokens_out), 6),
                    cached_tokens_reported=sum(r["cached_tokens"] is not None for r in rows if r["cell"] != "N10"))
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        service.close()
        await generator.aclose()


# ---------- Tóm tắt (free) ----------

def load_run(names: list[str]) -> list[dict]:
    """Ghép dòng kết quả với mốc tính lại từ `events.jsonl` (nguồn duy nhất của các mốc)."""
    rows = []
    for name in names:
        results = read_jsonl(OUT_DIR / f"{name}.jsonl")
        events = read_jsonl(OUT_DIR / f"{name}.events.jsonl")
        assert [(r["id"], r["cell"]) for r in results] == [(e["id"], e["cell"]) for e in events]
        rows += [{**r, **timeline(e["events"]), "run": name} for r, e in zip(results, events) if r["id"] != "warmup"]
    return rows


def median_ci(values: list[float]) -> dict | None:
    if not values:
        return None
    rng = np.random.default_rng(SEED)
    data = np.array(values, dtype=float)
    medians = np.median(rng.choice(data, size=(BOOTSTRAP_ROUNDS, len(data)), replace=True), axis=1)
    return {"n": len(data), "median": round(float(np.median(data)), 1),
            "ci95": [round(float(np.percentile(medians, 2.5)), 1), round(float(np.percentile(medians, 97.5)), 1)],
            "p95": round(float(np.percentile(data, 95)), 1)}


def band(stat: dict | None) -> str:
    """Ngưỡng diễn giải ghi trước (plan §7 interpretation)."""
    if stat is None:
        return "NOT RUN"
    low = stat["ci95"][0]
    if stat["median"] >= 1500 and low > 0:
        return "clear"
    if stat["median"] >= 500 and low > 0:
        return "moderate"
    return "small_or_unclear"


def summarize(names: list[str]) -> dict:
    rows = load_run(names)
    by = {(r["run"], r["id"], r["cell"]): r for r in rows}
    ok = lambda r: r is not None and r["error"] is None and r["valid"] and not r["refusal"]
    s_main = [r for r in rows if r["cell"] == "S10" and r["scope"] == "in_kb" and ok(r)]
    gain_visible = [r["t_done"] - r["t_first_visible"] for r in s_main if r["t_first_visible"] is not None]
    gain_cited = [r["t_done"] - r["t_first_cited_sentence"] for r in s_main if r["t_first_cited_sentence"] is not None]
    overhead = [r["t_done"] - n["t_done"] for r in s_main if ok(n := by.get((r["run"], r["id"], "N10")))]
    s_rows = [r for r in rows if r["cell"] == "S10" and r["error"] is None]
    uncached = [r for r in s_rows if r["cached_tokens"] == 0]
    sdk_first, sdk_tail = [], []
    for r in s_rows:
        d = by.get((r["run"], r["id"], "D10"))
        if d is not None and d["error"] is None and r["t_first_event"] is not None and d["t_first_event"] is not None:
            sdk_first.append(r["t_first_event"] - d["t_first_event"])
            sdk_tail.append((r["t_done"] - r["t_last_event"]) - (d["t_done"] - d["t_last_event"]))
    gv = median_ci(gain_visible)
    return {
        "runs": names,
        "decide": {"gain_visible_ms": gv, "band": band(gv), "gain_cited_ms": (gc := median_ci(gain_cited)), "band_cited": band(gc)},
        "prediction_check": None if gv is None else ("recheck_marks" if not 300 <= gv["median"] <= 3000 else "within"),
        "watch": {
            "stream_overhead_ms": (so := median_ci(overhead)),
            # plan §7 overhead_rule: trung vị > 300 ms ⇒ diễn giải theo (gain − overhead), ghi cả hai
            "overhead_over_300ms": None if so is None else so["median"] > 300,
            # S10 luôn là lần gọi đầu với prompt ⇒ "all" là số chính; "uncached" chỉ có khi provider báo cached_tokens == 0
            "e2e_first_visible_ms": {
                "all": median_ci([r["search_ms"] + r["context_ms"] + r["t_first_visible"]
                                  for r in s_rows if r["scope"] == "in_kb" and r["t_first_visible"] is not None]),
                "uncached": median_ci([r["search_ms"] + r["context_ms"] + r["t_first_visible"]
                                       for r in uncached if r["scope"] == "in_kb" and r["t_first_visible"] is not None])},
            "pre_text_ms": {key: {"cached_0": median_ci([r[key] for r in s_rows if r["cached_tokens"] == 0 and r[key] is not None]),
                                  "cached_pos": median_ci([r[key] for r in s_rows if (r["cached_tokens"] or 0) > 0 and r[key] is not None]),
                                  "cached_unknown": median_ci([r[key] for r in s_rows if r["cached_tokens"] is None and r[key] is not None])}
                            for key in ("t_first_event", "t_reasoning_done", "t_first_delta", "t_first_visible")},
            "reasoning_tokens_s10": median_ci([r["reasoning_tokens"] for r in s_rows if r["reasoning_tokens"] is not None]),
            "sdk_overhead_ms": {"first_event": median_ci(sdk_first), "tail": median_ci(sdk_tail)},
            "out_of_kb_s10": [{"id": r["id"], "refusal": r["refusal"], "t_first_visible": r["t_first_visible"],
                               "t_refusal_complete": r["t_refusal_complete"], "t_done": r["t_done"]}
                              for r in s_rows if r["scope"] == "out_of_kb"],
            "per_cell": {cell: {"rows": len(cr := [r for r in rows if r["cell"] == cell]),
                                "errors": sum(bool(r["error"]) for r in cr),
                                "refusal_in_kb": sum(bool(r["refusal"]) for r in cr if r["scope"] == "in_kb"),
                                "valid": sum(bool(r["valid"]) for r in cr),
                                "first_visible_missing": sum(r["error"] is None and r["cell"] != "N10" and r["t_first_visible"] is None for r in cr),
                                "cached_tokens": {"zero": sum(r["cached_tokens"] == 0 for r in cr), "positive": sum((r["cached_tokens"] or 0) > 0 for r in cr),
                                                  "unknown": sum(r["cached_tokens"] is None for r in cr)},
                                "usd_per_call": round(sum(cost_usd(r["input_tokens"] or 0, r["output_tokens"] or 0) for r in cr) / max(len(cr), 1), 7)}
                         for cell in CELLS},
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run", help="có phí: gọi gpt-6-luna")
    run_parser.add_argument("--name", required=True)
    run_parser.add_argument("--pilot", action="store_true", help="q03 + q09 × S10 + D10 (4 lần gọi), không gộp số")
    sum_parser = sub.add_parser("summarize", help="free: đọc kết quả đã lưu")
    sum_parser.add_argument("--names", nargs="+", required=True)
    args = parser.parse_args()
    if args.command == "run":
        asyncio.run(run(args.name, args.pilot))
    else:
        summary = summarize(args.names)
        (OUT_DIR / f"{'+'.join(args.names)}.summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
