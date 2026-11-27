"""Bộ chấm Faithfulness NLI 2 bước (offline) cho `hue_rag`.

Kiểm độ bám nguồn ngữ nghĩa thay vì chỉ kiểm cú pháp `[n]`:
1. Bước 1 (Statement Extraction): tách câu trả lời đã gán `[n]` thành các mệnh đề đơn
   độc lập (khử đại từ), giữ danh sách mã nguồn `[n]` gắn với từng mệnh đề.
2. Bước 2 (NLI Verification): đối chiếu từng mệnh đề với:
   - đúng các `[Nguồn n]` mà mệnh đề đó trích dẫn (`cited_supported` — bắt lỗi gán sai `[1]`
     hoặc bịa chi tiết ngoài `[1]`);
   - toàn bộ tập nguồn đã truy hồi (`context_supported` — phân biệt bịa hoàn toàn vs
     trích nhầm số nguồn).

Chạy được trên:
- JSONL đầu ra của `evaluation.full_corpus_eval` (`top_chunk_ids` + `context_sources`, giải
  mã payload trực tiếp từ Qdrant theo `point_id_for_chunk_id`, không gọi embedding);
- JSONL / JSON đo Đợt 4A (đã lưu sẵn `sources` từ `/api/chat` hoặc nhãn tay như
  `bo_kiem_faithfulness_15.json`).

Hỗ trợ `--dry-run` (0 USD) và ghi đủ `input_tokens`, `cached_tokens`, `output_tokens`, `usd`
qua `llm.pricing.cost_usd`.
"""
from __future__ import annotations

import argparse
import asyncio
from collections.abc import Callable, Sequence
import json
from pathlib import Path
import re
import sys
from typing import Any

from agents import Agent, ModelSettings, RunConfig, Runner
from pydantic import BaseModel, ConfigDict, Field

from core.schema import RetrievedDocument, point_id_for_chunk_id
from core.settings_loader import load_settings
from evaluation.full_corpus_eval import (
    CONCURRENCY,
    describe_error,
    is_refusal,
    load_golden_cases,
    read_jsonl,
)
from llm.citations import CITATION_PATTERN, normalize_citations
from llm.full_corpus_prompt import CAU_Y_THIEU
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator, input_cache_tokens
from llm.pricing import cost_usd
from llm import thoi_tiet as tt
from retrieval.full_corpus import build_retrieved_document
from retrieval.full_corpus_context import FullCorpusContextBuilder, PackedSource
from vectorstore.qdrant import client_from_settings

EXTRACT_INSTRUCTIONS = f"""
Bạn là bộ tách mệnh đề cho hệ thống kiểm chứng bám nguồn tiếng Việt.
Nhiệm vụ: đọc Câu hỏi (để hiểu ngữ cảnh đại từ) và Câu trả lời cần kiểm (có mã trích dẫn dạng [1], [2]…),
rồi tách phần nội dung khẳng định sự thật thành danh sách các mệnh đề đơn (atomic statements).

Quy tắc bắt buộc:
1. Mỗi mệnh đề chỉ nêu MỘT ý/sự thật độc lập, rõ chủ ngữ, đã khử đại từ ("nơi này", "chùa", "quán đó", "ông ấy"… → thay bằng tên cụ thể từ câu trước hoặc câu hỏi).
2. Không để mã [1], [2] nằm trong chuỗi `statement`; đưa các số nguyên trích dẫn gắn với ý đó vào `cited_ids` (ví dụ `[1][3]` → `[1, 3]`). Nếu mệnh đề không có mã trích dẫn nào đi kèm, để `cited_ids = []`.
3. KHÔNG tách các dòng thuần túy báo thiếu thông tin hoặc từ chối (ví dụ dòng mở đầu bằng "{CAU_Y_THIEU}", câu "Tôi không tìm thấy đủ thông tin…", hoặc câu nhắc chung không chứa khẳng định sự kiện cụ thể như "bạn nên kiểm tra lại giờ mở cửa trước khi đi").
4. Không suy diễn thêm chi tiết không có trong câu trả lời gốc; giữ nguyên con số, đơn vị, tên riêng, điều kiện trong câu trả lời.
5. Nếu câu trả lời không có khẳng định sự thật nào (chỉ từ chối hoặc xã giao), trả `statements = []`.
""".strip()

NLI_INSTRUCTIONS = """
Bạn là người kiểm chứng NLI (Natural Language Inference) cho hệ thống RAG du lịch – văn hóa Huế.
Bạn nhận danh sách các Nguồn (`[Nguồn 1]`, `[Nguồn 2]`…) và danh sách các Mệnh đề đơn cần kiểm (`index`, `statement`, `cited_ids`).

Với MỖI mệnh đề, hãy đánh giá độc lập HAI mức theo đúng nguyên văn các nguồn được cung cấp (tuyệt đối không dùng kiến thức bên ngoài):
1. `cited_supported` (boolean): mệnh đề có được suy ra / hỗ trợ trực tiếp CHỈ từ tập các nguồn có ID nằm trong `cited_ids` của chính mệnh đề đó hay không?
   - Nếu `cited_ids` rỗng, hoặc ID trong `cited_ids` không tồn tại trong danh sách nguồn, hoặc sự kiện nằm ở `[Nguồn 2]` nhưng mệnh đề lại trích `[1]` → `cited_supported = false`.
   - Mọi chi tiết cụ thể (tên, số, giá, giờ, năm, địa chỉ, điều kiện, khẳng định) trong mệnh đề phải có căn cứ rõ trong đúng các nguồn được trích; nếu gán thêm chi tiết ngoài các nguồn đó → `cited_supported = false`.
2. `context_supported` (boolean): mệnh đề có được suy ra / hỗ trợ trực tiếp từ BẤT KỲ nguồn nào trong toàn bộ danh sách nguồn đã cung cấp hay không?
3. `reason`: 1 câu tiếng Việt ngắn gọn nêu rõ nguồn nào đỡ hoặc chi tiết nào thiếu/lệch.

Trả kết quả đúng số lượng và đúng thứ tự `statement_index` của các mệnh đề đầu vào.
""".strip()

_WEATHER_BLOCK_RE = re.compile(
    r"\n*\*\*Dự báo thời tiết Huế\*\*.*?(?=\n\n(?:Với bão, lũ, ngập:|Mình chỉ có dự báo 7 ngày tới)|$)",
    re.DOTALL,
)


class StatementItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    statement: str
    cited_ids: list[int] = Field(default_factory=list)


class StatementsOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    statements: list[StatementItem] = Field(default_factory=list)


class NLIVerdict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    statement_index: int
    cited_supported: bool
    context_supported: bool
    reason: str


class NLIOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdicts: list[NLIVerdict] = Field(default_factory=list)


def strip_code_appended_blocks(answer: str) -> str:
    """Loại bỏ các khối chữ cố định do code nối thêm sau câu model (dự báo Open-Meteo, câu bão/lũ 112, dòng ý thiếu)."""
    text = (answer or "").strip()
    if not text:
        return ""
    if text.startswith(tt.CAU_DAU_BAO_LU):
        text = text[len(tt.CAU_DAU_BAO_LU):].lstrip()
    text = _WEATHER_BLOCK_RE.sub("", text)
    for fixed_line in (tt.CAU_BAO_LU, tt.CAU_NGOAI_7_NGAY, tt.CAU_LOI):
        text = text.replace(fixed_line, "")
    kept_lines = [
        line for line in text.splitlines()
        if not line.strip().startswith(CAU_Y_THIEU)
    ]
    return "\n".join(kept_lines).strip()


def _source_from_dict(item: dict[str, Any], default_id: int) -> PackedSource | None:
    sid = item.get("id", default_id)
    if not isinstance(sid, int) or isinstance(sid, bool):
        return None
    title = str(item.get("title") or "")
    heading_raw = item.get("heading_path") or ()
    heading_path = (heading_raw,) if isinstance(heading_raw, str) else tuple(str(h) for h in heading_raw)
    excerpts_raw = item.get("excerpts")
    if excerpts_raw is None and isinstance(item.get("text"), str):
        excerpts_raw = [item["text"]]
    excerpts = tuple(str(x).strip() for x in (excerpts_raw or ()) if str(x).strip())
    if not excerpts and not title:
        return None
    return PackedSource(
        id=sid,
        title=title,
        heading_path=heading_path,
        excerpts=excerpts or (title,),
        source=str(item.get("source") or item.get("bai_id") or ""),
    )


def format_sources_for_nli(sources: Sequence[PackedSource]) -> str:
    """Định dạng tập `PackedSource` thành các khối `[Nguồn n]` chuẩn giống prompt runtime."""
    return "\n\n".join(FullCorpusContextBuilder._block(src) for src in sources)


class QdrantChunkResolver:
    """Giải mã `top_chunk_ids` thành `PackedSource` bằng Qdrant `retrieve` (0 embedding)."""

    def __init__(self, settings: dict[str, Any] | None = None, client: Any = None) -> None:
        self._settings = settings or load_settings(validate_private_paths=False)
        self._client = client if client is not None else client_from_settings(self._settings)
        self._owns_client = client is None
        cand = self._settings["full_corpus_runtime"]["candidate_id"]
        from ingestion.full_corpus_pipeline import candidate_by_id
        self._collection = candidate_by_id(cand).collection_name
        self._cache: dict[str, RetrievedDocument | None] = {}

    def resolve(self, chunk_ids: Sequence[str], limit: int | None = None) -> list[PackedSource]:
        wanted = list(chunk_ids[:limit] if limit is not None else chunk_ids)
        missing = [cid for cid in wanted if cid not in self._cache]
        if missing:
            point_ids = [point_id_for_chunk_id(cid) for cid in missing]
            points = self._client.retrieve(
                collection_name=self._collection,
                ids=point_ids,
                with_payload=["source", "title", "heading_path", "evidence_parts", "chunk_id", "domain", "search_text"],
            )
            by_chunk = {}
            for pt in points:
                payload = getattr(pt, "payload", None) or {}
                cid = payload.get("chunk_id")
                if cid:
                    by_chunk[cid] = build_retrieved_document(
                        {**payload, "search_text": payload.get("search_text") or ""},
                        1.0,
                    )
            for cid in missing:
                self._cache[cid] = by_chunk.get(cid)

        sources: list[PackedSource] = []
        for cid in wanted:
            doc = self._cache.get(cid)
            if doc is None:
                continue
            packed = FullCorpusContextBuilder._source(doc, len(sources) + 1)
            if packed is not None:
                sources.append(packed)
        return sources

    def close(self) -> None:
        if self._owns_client and hasattr(self._client, "close"):
            self._client.close()


def resolve_row_sources(
    row: dict[str, Any],
    resolver: Callable[[Sequence[str], int | None], list[PackedSource]] | None = None,
) -> list[PackedSource]:
    """Lấy danh sách `PackedSource` từ `row['sources']` sẵn có hoặc giải mã `row['top_chunk_ids']`."""
    raw_sources = row.get("sources")
    if isinstance(raw_sources, list) and raw_sources:
        parsed = []
        for idx, item in enumerate(raw_sources, start=1):
            if isinstance(item, PackedSource):
                parsed.append(item)
            elif isinstance(item, dict):
                src = _source_from_dict(item, idx)
                if src is not None:
                    parsed.append(src)
        return parsed
    if isinstance(raw_sources, dict) and raw_sources:
        parsed = []
        for k, v in raw_sources.items():
            sid = int(k)
            if isinstance(v, dict):
                src = _source_from_dict({**v, "id": v.get("id", sid)}, sid)
            else:
                src = PackedSource(id=sid, title=f"Nguồn {sid}", heading_path=(), excerpts=(str(v).strip(),))
            if src is not None:
                parsed.append(src)
        return sorted(parsed, key=lambda s: s.id)
    chunk_ids = row.get("top_chunk_ids") or []
    if chunk_ids and resolver is not None:
        limit = row.get("context_sources")
        return resolver(chunk_ids, limit if isinstance(limit, int) and limit > 0 else None)
    return []


def extract_statements_agent(model: Any) -> Agent:
    return Agent(
        name="hue_faithfulness_statement_extractor",
        instructions=EXTRACT_INSTRUCTIONS,
        model=model,
        model_settings=ModelSettings(
            include_usage=True,
            store=False,
            extra_args={"prompt_cache_key": "hue_eval_faith_extract_v1"},
        ),
        output_type=StatementsOutput,
    )


def nli_judge_agent(model: Any) -> Agent:
    return Agent(
        name="hue_faithfulness_nli_judge",
        instructions=NLI_INSTRUCTIONS,
        model=model,
        model_settings=ModelSettings(
            include_usage=True,
            store=False,
            extra_args={"prompt_cache_key": "hue_eval_faith_nli_v1"},
        ),
        output_type=NLIOutput,
    )


def build_extract_message(question: str, answer: str) -> str:
    norm_answer = normalize_citations(answer)
    return f"Câu hỏi:\n{question.strip()}\n\nCâu trả lời cần tách:\n{norm_answer.strip()}"


def build_nli_message(statements: Sequence[StatementItem], sources: Sequence[PackedSource]) -> str:
    sources_text = format_sources_for_nli(sources)
    stmt_lines = [
        f"- [{idx}] (trích dẫn: {item.cited_ids}) {item.statement}"
        for idx, item in enumerate(statements)
    ]
    return (
        f"Danh sách nguồn:\n{sources_text}\n\n"
        f"Danh sách mệnh đề cần kiểm (tổng {len(statements)}):\n" + "\n".join(stmt_lines)
    )


def _usage_from_result(result: Any) -> dict[str, int]:
    usages = [u for u in (getattr(r, "usage", None) for r in getattr(result, "raw_responses", ()) or ()) if u is not None]
    if not usages:
        return {"input_tokens": 0, "output_tokens": 0, "cache_write_tokens": 0, "cached_tokens": 0}
    in_tok = sum(getattr(u, "input_tokens", 0) or 0 for u in usages)
    out_tok = sum(getattr(u, "output_tokens", 0) or 0 for u in usages)
    cached_list = [input_cache_tokens(u) for u in usages]
    cached_tok = sum((c[0] or 0) for c in cached_list)
    write_tok = sum((c[1] or 0) for c in cached_list)
    return {
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cache_write_tokens": write_tok,
        "cached_tokens": cached_tok,
    }


def _add_usage(total: dict[str, int], part: dict[str, int]) -> None:
    for k in ("input_tokens", "output_tokens", "cache_write_tokens", "cached_tokens"):
        total[k] += part.get(k, 0)


def _parse_output(final_output: Any, schema: type[BaseModel]) -> Any:
    if isinstance(final_output, schema):
        return final_output
    if isinstance(final_output, str):
        return schema.model_validate_json(final_output)
    return schema.model_validate(final_output)


def _row_identity(row: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in ("id", "case_index", "category", "subgroup", "expected_faithful"):
        if key in row:
            out[key] = row[key]
    return out


def _empty_eval_row(row: dict[str, Any], status: str, *, error: str | None = None) -> dict[str, Any]:
    return {
        **_row_identity(row),
        "status": status,
        "faithfulness_score": None,
        "faithfulness_cited": None,
        "faithfulness_context": None,
        "is_faithful": None,
        "num_statements": 0,
        "cited_supported_count": 0,
        "context_supported_count": 0,
        "misattributed_count": 0,
        "hallucinated_count": 0,
        "statements": [],
        "input_tokens": 0,
        "cached_tokens": 0,
        "cache_write_tokens": 0,
        "output_tokens": 0,
        "usd": 0.0,
        "error": error,
    }


async def evaluate_row_faithfulness(
    row: dict[str, Any],
    *,
    extract_agent: Agent,
    nli_agent: Agent,
    question_by_index: dict[int, str] | None = None,
    resolver: Callable[[Sequence[str], int | None], list[PackedSource]] | None = None,
    provider: str = "openai",
) -> dict[str, Any]:
    """Chấm Faithfulness NLI 2 bước cho một bản ghi kết quả."""
    if row.get("error"):
        return _empty_eval_row(row, "skipped_error")

    raw_answer = str(row.get("answer") or "")
    if row.get("refusal") is True or row.get("is_refusal") is True or is_refusal(raw_answer):
        return _empty_eval_row(row, "skipped_refusal")

    cleaned_answer = strip_code_appended_blocks(raw_answer)
    if not cleaned_answer or is_refusal(cleaned_answer):
        return _empty_eval_row(row, "skipped_refusal")

    sources = resolve_row_sources(row, resolver=resolver)
    if not sources:
        return _empty_eval_row(row, "no_sources", error="missing sources/top_chunk_ids")

    question = str(row.get("question") or row.get("query") or "")
    if not question and isinstance(row.get("case_index"), int) and question_by_index:
        question = question_by_index.get(row["case_index"], "")

    usage_total = {"input_tokens": 0, "output_tokens": 0, "cache_write_tokens": 0, "cached_tokens": 0}
    run_cfg = RunConfig(tracing_disabled=True, trace_include_sensitive_data=False)

    try:
        extract_res = await Runner.run(
            extract_agent,
            input=build_extract_message(question, cleaned_answer),
            max_turns=1,
            run_config=run_cfg,
        )
        _add_usage(usage_total, _usage_from_result(extract_res))
        extracted: StatementsOutput = _parse_output(extract_res.final_output, StatementsOutput)
    except Exception as exc:
        usd_val = cost_usd(**usage_total, provider=provider)
        out = _empty_eval_row(row, "error", error=describe_error(exc))
        out.update(**usage_total, usd=round(usd_val, 8))
        return out

    # Lọc các dòng thuần túy từ chối nếu model lỡ tách nhầm.
    statements = [
        item for item in extracted.statements
        if item.statement.strip() and not item.statement.strip().startswith(CAU_Y_THIEU)
    ]
    if not statements:
        usd_val = cost_usd(**usage_total, provider=provider)
        out = _empty_eval_row(row, "no_claims")
        out.update(**usage_total, usd=round(usd_val, 8))
        return out

    try:
        nli_res = await Runner.run(
            nli_agent,
            input=build_nli_message(statements, sources),
            max_turns=1,
            run_config=run_cfg,
        )
        _add_usage(usage_total, _usage_from_result(nli_res))
        nli_out: NLIOutput = _parse_output(nli_res.final_output, NLIOutput)
    except Exception as exc:
        usd_val = cost_usd(**usage_total, provider=provider)
        out = _empty_eval_row(row, "error", error=describe_error(exc))
        out.update(**usage_total, usd=round(usd_val, 8))
        return out

    source_ids = {s.id for s in sources}
    verdict_map = {v.statement_index: v for v in nli_out.verdicts}
    details: list[dict[str, Any]] = []
    cited_ok = 0
    context_ok = 0
    misattributed = 0
    hallucinated = 0

    for idx, stmt in enumerate(statements):
        v = verdict_map.get(idx)
        # Ràng buộc tất định: không có citation hợp lệ trỏ vào `source_ids` ⇒ không thể `cited_supported`.
        valid_cited_ids = [cid for cid in stmt.cited_ids if cid in source_ids]
        has_valid_citation = bool(valid_cited_ids) and len(valid_cited_ids) == len(stmt.cited_ids)
        raw_cited_ok = bool(v.cited_supported) if v is not None else False
        raw_ctx_ok = bool(v.context_supported) if v is not None else False
        cited_supported = bool(has_valid_citation and raw_cited_ok)
        context_supported = bool(raw_ctx_ok or cited_supported)
        reason = v.reason if v is not None else "missing NLI verdict"
        if not stmt.cited_ids:
            reason = f"Không có mã trích dẫn [n]; {reason}"
        elif not has_valid_citation:
            missing_ids = [cid for cid in stmt.cited_ids if cid not in source_ids]
            reason = f"Trích mã nguồn không tồn tại {missing_ids}; {reason}"

        if cited_supported:
            cited_ok += 1
        if context_supported:
            context_ok += 1
        if not cited_supported and context_supported:
            misattributed += 1
        if not context_supported:
            hallucinated += 1

        details.append({
            "statement_index": idx,
            "statement": stmt.statement,
            "cited_ids": list(stmt.cited_ids),
            "cited_supported": cited_supported,
            "context_supported": context_supported,
            "reason": reason,
        })

    n_stmt = len(statements)
    f_cited = round(cited_ok / n_stmt, 6)
    f_ctx = round(context_ok / n_stmt, 6)
    usd_val = cost_usd(**usage_total, provider=provider)
    return {
        **_row_identity(row),
        "status": "ok",
        "faithfulness_score": f_cited,
        "faithfulness_cited": f_cited,
        "faithfulness_context": f_ctx,
        "is_faithful": hallucinated == 0 and misattributed == 0,
        "num_statements": n_stmt,
        "cited_supported_count": cited_ok,
        "context_supported_count": context_ok,
        "misattributed_count": misattributed,
        "hallucinated_count": hallucinated,
        "statements": details,
        **usage_total,
        "usd": round(usd_val, 8),
        "error": None,
    }


def summarize_faithfulness(rows: Sequence[dict[str, Any]], provider: str = "openai") -> dict[str, Any]:
    """Tổng hợp kết quả chấm Faithfulness và độ khớp người–máy (nếu có `expected_faithful`)."""
    data = list(rows)
    evaluated = [r for r in data if r.get("status") == "ok" and r.get("faithfulness_cited") is not None]
    totals = {
        k: sum(int(r.get(k) or 0) for r in data)
        for k in ("input_tokens", "output_tokens", "cache_write_tokens", "cached_tokens")
    }
    summary: dict[str, Any] = {
        "total_rows": len(data),
        "evaluated": len(evaluated),
        "skipped_refusal": sum(r.get("status") == "skipped_refusal" for r in data),
        "skipped_error": sum(r.get("status") == "skipped_error" for r in data),
        "no_claims": sum(r.get("status") == "no_claims" for r in data),
        "no_sources": sum(r.get("status") == "no_sources" for r in data),
        "errors": sum(r.get("status") == "error" for r in data),
        "mean_faithfulness_cited": (
            round(sum(r["faithfulness_cited"] for r in evaluated) / len(evaluated), 6) if evaluated else None
        ),
        "mean_faithfulness_context": (
            round(sum(r["faithfulness_context"] for r in evaluated) / len(evaluated), 6) if evaluated else None
        ),
        "strict_faithful_rate": (
            round(sum(bool(r["is_faithful"]) for r in evaluated) / len(evaluated), 6) if evaluated else None
        ),
        "total_statements": sum(int(r.get("num_statements") or 0) for r in evaluated),
        "total_misattributed": sum(int(r.get("misattributed_count") or 0) for r in evaluated),
        "total_hallucinated": sum(int(r.get("hallucinated_count") or 0) for r in evaluated),
        **totals,
        "cost_usd": round(cost_usd(**totals, provider=provider), 8),
    }

    labeled = [r for r in evaluated if isinstance(r.get("expected_faithful"), bool)]
    if labeled:
        tp = sum(bool(r["is_faithful"]) and r["expected_faithful"] is True for r in labeled)
        tn = sum((not r["is_faithful"]) and r["expected_faithful"] is False for r in labeled)
        fp = sum(bool(r["is_faithful"]) and r["expected_faithful"] is False for r in labeled)
        fn = sum((not r["is_faithful"]) and r["expected_faithful"] is True for r in labeled)
        summary["agreement"] = {
            "n": len(labeled),
            "matched": tp + tn,
            "agreement_rate": round((tp + tn) / len(labeled), 6),
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn,
        }
    return summary


def load_eval_input(path: Path) -> list[dict[str, Any]]:
    """Đọc file đầu vào dạng JSONL, JSON list, hoặc JSON dict có khoá `results`/`cases`."""
    p = Path(path)
    raw = p.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    if p.suffix.lower() != ".jsonl" and (raw.startswith("{") or raw.startswith("[")):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return read_jsonl(p)
        if isinstance(data, list):
            return [r for r in data if isinstance(r, dict)]
        if isinstance(data, dict):
            for key in ("results", "cases", "rows"):
                if isinstance(data.get(key), list):
                    return [r for r in data[key] if isinstance(r, dict)]
            return [data]
    return read_jsonl(p)


def filter_rows(
    rows: list[dict[str, Any]],
    *,
    cases: Sequence[int] | None = None,
    ids: Sequence[str] | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    selected = rows
    if cases is not None:
        wanted = set(cases)
        selected = [r for r in selected if r.get("case_index") in wanted]
    if ids is not None:
        wanted_ids = set(ids)
        selected = [r for r in selected if r.get("id") in wanted_ids]
    if limit is not None:
        selected = selected[:limit]
    return selected


def dry_run_faithfulness(
    rows: Sequence[dict[str, Any]],
    *,
    question_by_index: dict[int, str] | None = None,
    resolver: Callable[[Sequence[str], int | None], list[PackedSource]] | None = None,
) -> dict[str, Any]:
    """Kiểm tra hợp lệ đầu vào (0 USD, không gọi LLM) và ước lượng số câu sẽ chấm."""
    eligible = 0
    skipped_refusal = 0
    skipped_error = 0
    missing_sources = 0
    total_citations = 0

    for row in rows:
        if row.get("error"):
            skipped_error += 1
            continue
        ans = str(row.get("answer") or "")
        if row.get("refusal") is True or row.get("is_refusal") is True or is_refusal(ans):
            skipped_refusal += 1
            continue
        cleaned = strip_code_appended_blocks(ans)
        if not cleaned or is_refusal(cleaned):
            skipped_refusal += 1
            continue
        sources = resolve_row_sources(row, resolver=resolver)
        if not sources and not (row.get("sources") or row.get("top_chunk_ids")):
            missing_sources += 1
            continue
        if not sources and row.get("top_chunk_ids") and resolver is not None:
            missing_sources += 1
            continue
        eligible += 1
        total_citations += len(CITATION_PATTERN.findall(cleaned))

    return {
        "dry_run": "ok",
        "usd": 0.0,
        "total_rows": len(rows),
        "eligible_to_score": eligible,
        "skipped_refusal": skipped_refusal,
        "skipped_error": skipped_error,
        "missing_sources": missing_sources,
        "total_citations_in_eligible": total_citations,
        "question_lookup_size": len(question_by_index or {}),
    }


async def run_faithfulness_eval(
    rows: Sequence[dict[str, Any]],
    *,
    out_path: Path | None = None,
    question_by_index: dict[int, str] | None = None,
    resolver: Callable[[Sequence[str], int | None], list[PackedSource]] | None = None,
    concurrency: int = CONCURRENCY,
    provider: str = "openai",
    generator: OpenAIFullCorpusGenerator | None = None,
) -> list[dict[str, Any]]:
    """Chạy chấm Faithfulness NLI 2 bước trên danh sách dòng; ghi từng dòng ngay ra `out_path` nếu có."""
    if out_path is not None and out_path.exists():
        raise SystemExit(f"exists: {out_path}")

    settings = load_settings(validate_private_paths=False)
    owns_generator = generator is None
    gen = generator or OpenAIFullCorpusGenerator.from_environment(settings)
    extract_agent = extract_statements_agent(gen.responses_model)
    nli_agent = nli_judge_agent(gen.responses_model)
    semaphore = asyncio.Semaphore(max(1, concurrency))

    async def one(idx: int, row: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        async with semaphore:
            res = await evaluate_row_faithfulness(
                row,
                extract_agent=extract_agent,
                nli_agent=nli_agent,
                question_by_index=question_by_index,
                resolver=resolver,
                provider=provider,
            )
            return idx, res

    out_fh = None
    try:
        if out_path is not None:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_fh = out_path.open("w", encoding="utf-8")

        results: list[dict[str, Any] | None] = [None] * len(rows)
        tasks = [asyncio.create_task(one(i, r)) for i, r in enumerate(rows)]
        for fut in asyncio.as_completed(tasks):
            idx, res = await fut
            results[idx] = res
            if out_fh is not None:
                out_fh.write(json.dumps(res, ensure_ascii=False) + "\n")
                out_fh.flush()
        return [r for r in results if r is not None]
    finally:
        if out_fh is not None:
            out_fh.close()
        if owns_generator:
            await gen.aclose()


def _load_question_map(golden_path: Path | None) -> dict[int, str]:
    if golden_path is None:
        cases = load_golden_cases("full")
        return {c["case_index"]: c["question"] for c in cases}
    if not golden_path.is_file():
        return {}
    rows = read_jsonl(golden_path)
    return {idx: row["question"] for idx, row in enumerate(rows) if "question" in row}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="evaluation.faithfulness_eval", description="Chấm Faithfulness NLI 2 bước offline")
    ap.add_argument("--input", type=Path, required=True, help="JSONL/JSON đầu ra của full_corpus_eval hoặc Đợt 4A")
    ap.add_argument("--out", type=Path, default=None, help="File JSONL đầu ra (bắt buộc khi không --dry-run)")
    ap.add_argument("--golden", type=Path, default=None, help="JSONL Golden để tra câu hỏi theo case_index")
    ap.add_argument("--cases", type=int, nargs="*", default=None, help="Lọc theo danh sách case_index")
    ap.add_argument("--ids", nargs="*", default=None, help="Lọc theo danh sách id")
    ap.add_argument("--limit", type=int, default=None, help="Giới hạn số dòng đầu")
    ap.add_argument("--concurrency", type=int, default=CONCURRENCY, help="Số tác vụ song song")
    ap.add_argument("--provider", default="openai", choices=["openai", "bedrock"])
    ap.add_argument("--no-qdrant", action="store_true", help="Không kết nối Qdrant (dùng khi input đã có sẵn sources)")
    ap.add_argument("--dry-run", action="store_true", help="Kiểm tra hợp lệ đầu vào (0 USD, không gọi LLM)")
    ap.add_argument("--summary-json", type=Path, default=None, help="Ghi thêm file JSON tóm tắt")
    args = ap.parse_args(argv)

    if not args.dry_run and args.out is None:
        ap.error("--out is required unless --dry-run is set")
    if args.out is not None and args.out.exists():
        raise SystemExit(f"exists: {args.out}")

    rows = filter_rows(load_eval_input(args.input), cases=args.cases, ids=args.ids, limit=args.limit)
    q_map = _load_question_map(args.golden)
    needs_qdrant = (not args.no_qdrant) and any(
        (not r.get("sources")) and bool(r.get("top_chunk_ids")) for r in rows
    )

    resolver_obj: QdrantChunkResolver | None = None
    try:
        if needs_qdrant:
            resolver_obj = QdrantChunkResolver()
        resolver_fn = resolver_obj.resolve if resolver_obj is not None else None

        if args.dry_run:
            report = dry_run_faithfulness(rows, question_by_index=q_map, resolver=resolver_fn)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0

        scored = asyncio.run(
            run_faithfulness_eval(
                rows,
                out_path=args.out,
                question_by_index=q_map,
                resolver=resolver_fn,
                concurrency=args.concurrency,
                provider=args.provider,
            )
        )
        summary = summarize_faithfulness(scored, provider=args.provider)
        if args.summary_json is not None:
            if args.summary_json.exists():
                raise SystemExit(f"exists: {args.summary_json}")
            args.summary_json.parent.mkdir(parents=True, exist_ok=True)
            args.summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    finally:
        if resolver_obj is not None:
            resolver_obj.close()


if __name__ == "__main__":
    raise SystemExit(main())
