"""Phase 8.2 §10 R4 — thước "số trong câu trả lời có trong đoạn được trích" (theo dõi, không chặn).

Spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` §10.3 dòng R4; C37 §3. Bắt hai lỗi judge hay bỏ sót:
con số model tự suy ra sai, và con số đúng với context nhưng nằm ở đoạn không được trích. Số trong câu hỏi không tính (model
nhắc lại câu hỏi); khoảng số "3–5" tách thành từng số để khớp cách viết "3 đến 5" của nguồn.

Không gọi API: đọc câu trả lời đã lưu, dựng lại đúng context model đã thấy bằng context builder production từ `top_chunk_ids`
(kiểm `input_tokens` khớp số đã lưu), rồi so số. Kết quả private ở `data/phase_8_2/r4/`.

Chạy từ `backend/`:
  HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_2.r4_numbers \
      ../data/phase_8_2/b1/b1_dev.jsonl ../data/phase_8_1/g2/g2_context10.jsonl
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import REPO_ROOT, build_context_builder, load_golden_cases
from ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from ingestion.full_corpus_pipeline import _phase4_settings
from llm.citations import CITATION_PATTERN
from retrieval.full_corpus import build_retrieved_document
from retrieval.full_corpus_context import PackedSource

OUT_DIR = REPO_ROOT / "data/phase_8_2/r4"

# Một số: chữ số, có thể có dấu ngăn nghìn / thập phân / giờ ở giữa ("95.000", "2,5", "08:00"). Dấu gạch / "–" giữa hai số là khoảng
# số ⇒ không nằm trong token, nên "100.000–700.000" ra hai số.
NUMBER_RE = re.compile(r"\d+(?:[.,:]\d+)*")
THOUSANDS_RE = re.compile(r"[.,](?=\d{3}(?:\D|$))")


def normalize_number(token: str) -> str:
    """"95.000" / "95,000" / "95000" ⇒ "95000"; "2,5" ⇒ "2.5"; "08:00" ⇒ "8:00"."""
    if ":" in token:
        hours, _, rest = token.partition(":")
        return f"{int(hours)}:{rest}"
    token = THOUSANDS_RE.sub("", token).replace(",", ".")
    whole, dot, fraction = token.partition(".")
    return f"{int(whole)}{dot}{fraction}"


def number_tokens(text: str) -> set[str]:
    """Các số (đã chuẩn hóa) trong một đoạn chữ, bỏ nhãn citation `[n]` / `[Nguồn n]`."""
    text = CITATION_PATTERN.sub(" ", unicodedata.normalize("NFC", text))
    return {normalize_number(token) for token in NUMBER_RE.findall(text)}


def source_text(source: PackedSource) -> str:
    """Chữ model thấy cho một nguồn (tiêu đề + mục + bằng chứng, như `FullCorpusContextBuilder._block`)."""
    return "\n".join([source.title, *source.heading_path, *source.excerpts])


def unsupported_numbers(answer: str, question: str, sources: tuple[PackedSource, ...]) -> list[str]:
    """Số trong câu trả lời không có trong câu hỏi và không có trong các nguồn được trích. Câu không trích nguồn ⇒ []."""
    cited = {int(value) for value in CITATION_PATTERN.findall(answer)}
    if not cited:
        return []
    supported = number_tokens(question)
    for source in sources:
        if source.id in cited:
            supported |= number_tokens(source_text(source))
    return sorted(number_tokens(answer) - supported)


def check_file(path: Path, builder, documents_by_chunk: dict, questions: dict[int, str]) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    out, token_offsets = [], set()
    for row in rows:
        question = unicodedata.normalize("NFC", questions[row["case_index"]])
        packed = builder.build(question, [documents_by_chunk[cid] for cid in row["top_chunk_ids"]])
        # Context dựng lại phải đúng cái model đã thấy, nếu không thì phép so vô nghĩa. `input_tokens` đã lưu là số provider đếm,
        # lớn hơn bộ đếm của builder một hằng số (khung tin nhắn) ⇒ kiểm số nguồn bằng nhau và độ lệch token như nhau mọi câu.
        if len(packed.sources) != row["context_sources"]:
            raise ValueError(f"{path.name} case {row['case_index']}: rebuilt {len(packed.sources)} sources, saved {row['context_sources']}")
        token_offsets.add(row["input_tokens"] - packed.input_tokens)
        flagged = [] if row["refusal"] or row["error"] else unsupported_numbers(row["answer"], question, packed.sources)
        out.append({"case_index": row["case_index"], "category": row["category"], "flagged": flagged})
    if len(token_offsets) != 1:
        raise ValueError(f"{path.name}: rebuilt context differs from saved run (token offsets {sorted(token_offsets)})")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path, help="JSONL câu trả lời đã lưu (answer, top_chunk_ids, context_sources…)")
    args = parser.parse_args()
    existing = [str(OUT_DIR / path.name) for path in args.files if (OUT_DIR / path.name).exists()]
    if existing:
        raise SystemExit(f"output exists (không ghi đè): {existing}")

    settings = load_settings(validate_private_paths=False)
    builder = build_context_builder(settings, max_documents=10)
    chunks, errors = chunk_full_corpus(_phase4_settings())
    if errors:
        raise ValueError(f"chunking failed: {errors}")
    documents_by_chunk = {c.chunk_id: build_retrieved_document(c.to_qdrant_payload(), 0.0) for c in chunks}
    questions = {case["case_index"]: case["question"] for case in load_golden_cases("full")}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in args.files:
        result = check_file(path, builder, documents_by_chunk, questions)
        (OUT_DIR / path.name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in result), encoding="utf-8")
        flagged = [r["case_index"] for r in result if r["flagged"]]
        print(json.dumps({"file": path.name, "n": len(result), "flagged": len(flagged), "case_index": flagged}))


if __name__ == "__main__":
    main()
