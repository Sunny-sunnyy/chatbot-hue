"""Citation validation, sentence-level citation check (`CIT_CAU`), and cited-source mapping."""
import re
import unicodedata
from collections.abc import Sequence

from core.schema import CitationIntegrityError
from llm.full_corpus_prompt import CAU_Y_THIEU, INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER
from retrieval.full_corpus_context import PackedSource

# Context gắn nhãn mỗi nguồn là "[Nguồn n]" nên model đôi khi trích đúng dạng đó thay vì "[n]";
# hai dạng cùng nghĩa (C-09, rà code 25/10).
CITATION_PATTERN = re.compile(r"\[\s*(?:nguồn\s*)?(\d+)\s*\]", re.IGNORECASE)
_LEADING_CITS_RE = re.compile(r"^((?:\[\s*(?:nguồn\s*)?\d+\s*\]\s*)+)", re.IGNORECASE)
_WEATHER_BLOCK_RE = re.compile(
    r"\n*\*\*Dự báo thời tiết Huế\*\*.*?(?=\n\n(?:Với bão, lũ, ngập:|Mình chỉ có dự báo 7 ngày tới)|$)",
    re.DOTALL,
)
_SYSTEM_LINE_PREFIXES = (
    "Với bão, lũ, ngập:",
    "Mình chỉ có dự báo 7 ngày tới",
    "Mình không theo dõi được tin bão / lũ hiện tại — dưới đây là thông tin chung từ tài liệu.",
    "Dưới đây là dự báo thời tiết Huế cho thời gian bạn hỏi",
    "Dưới đây là dự báo thời tiết Huế",
)
_ABBREV_PATTERNS = (
    r"\bvd\.", r"\bv\.v\.", r"\bTP\.", r"\bT\.P\.", r"\bTX\.", r"\bTT\.",
    r"\bQ\.", r"\bP\.", r"\bĐ\.", r"\bTh\.S\.", r"\bTS\.", r"\bGS\.",
    r"\bPGS\.", r"\bBS\.", r"\bKTS\.", r"\bStt\.", r"\bSTT\.", r"\btr\.",
    r"\bMr\.", r"\bMrs\.", r"\bMs\.", r"\bDr\.", r"\betc\.", r"\be\.g\.",
    r"\bi\.e\.", r"\bkm\.", r"\btr\.đ", r"\bTAN\.",
)
_ABBREV_RE = re.compile(r"(" + "|".join(_ABBREV_PATTERNS) + r")(?=\s|$)", re.IGNORECASE)
_LIST_NUM_RE = re.compile(r"^(\s*\d+)\.\s+")
_DOT_TOKEN = "\uE000"
_SHORT_VERDICTS = {
    "có.", "không.", "chưa.", "được.", "không được.", "có thể.",
    "không hẳn.", "không hoàn toàn.", "không phải suốt cả triều nguyễn.",
    "không phải tuyệt đối.", "không thể nói là chắc chắn mỗi tối.",
}


def normalize_citations(answer: str) -> str:
    """Đưa mọi citation về dạng "[n]" — dạng UI tách thành link."""
    return CITATION_PATTERN.sub(r"[\1]", answer)


def select_cited_sources(
    answer: str, sources: Sequence[PackedSource]
) -> tuple[PackedSource, ...]:
    markers = [int(value) for value in CITATION_PATTERN.findall(answer)]
    if INSUFFICIENT_ANSWER in answer:
        if markers:
            raise CitationIntegrityError("Fallback answer must not contain citations")
        if answer.strip() == INSUFFICIENT_ANSWER:
            return ()
    if not markers:
        raise CitationIntegrityError("Grounded answer has no citation")
    by_id = {source.id: source for source in sources}
    unknown = sorted(set(markers) - set(by_id))
    if unknown:
        raise CitationIntegrityError(f"Unknown citation IDs: {unknown}")
    return tuple(by_id[source_id] for source_id in sorted(set(markers)))


def _strip_system_blocks(text: str) -> str:
    t = unicodedata.normalize("NFC", text or "").strip()
    t = _WEATHER_BLOCK_RE.sub("", t)
    lines = [
        line for line in t.splitlines()
        if not any(line.strip().startswith(prefix) for prefix in _SYSTEM_LINE_PREFIXES)
    ]
    return "\n".join(lines).strip()


def _is_skip_line(line: str) -> tuple[bool, str | None]:
    s = line.strip()
    if not s:
        return True, "blank"
    if s.startswith(CAU_Y_THIEU):
        return True, "cau_y_thieu"
    if s == INSUFFICIENT_ANSWER or s == OUT_OF_SCOPE_ANSWER:
        return True, "fixed_refusal"
    if re.match(r"^#{1,6}\s+", s):
        return True, "markdown_heading"
    if re.match(r"^[-*_]{3,}$", s):
        return True, "hr"
    if s.startswith("|") and s.endswith("|") and re.match(r"^\|[\s:\-\|]+\|$", s):
        return True, "md_table_sep"
    s_no_bold = re.sub(r"^\s*[-*•]\s*", "", s).replace("**", "").strip()
    if s_no_bold.endswith(":") and len(s_no_bold) <= 90 and not CITATION_PATTERN.search(s_no_bold):
        return True, "heading_colon"
    if s.startswith("**") and s.endswith("**") and len(s) <= 85 and "." not in s and not re.search(r"\d", s):
        return True, "bold_heading"
    return False, None


def _protect_dots(line: str) -> str:
    s = re.sub(r"(?<=\d)\.(?=\d)", _DOT_TOKEN, line)
    s = s.replace("...", _DOT_TOKEN * 3)
    s = _LIST_NUM_RE.sub(lambda m: m.group(1) + _DOT_TOKEN + " ", s)
    s = _ABBREV_RE.sub(lambda m: m.group(1).replace(".", _DOT_TOKEN), s)
    s = re.sub(r"(\b[a-z0-9-]+)\.(vn|com|net|org|gov|edu|io)\b", lambda m: f"{m.group(1)}{_DOT_TOKEN}{m.group(2)}", s, flags=re.IGNORECASE)
    return s


def split_sentences_vi(text: str) -> list[dict]:
    """Tách văn bản tiếng Việt thành các đơn vị câu cần kiểm citation (bỏ qua tiêu đề, dòng thiếu, khối hệ thống)."""
    cleaned = _strip_system_blocks(text)
    if not cleaned:
        return []
    units: list[dict] = []
    for li, raw_line in enumerate(cleaned.splitlines()):
        skip, _ = _is_skip_line(raw_line)
        if skip:
            continue
        protected = _protect_dots(raw_line.strip())
        parts = re.split(r"(?<=[.!?…])\s+(?=(?:[\"\'\(\[\-\*•\d]|[^\W\d_]))", protected)
        merged: list[str] = []
        for p in parts:
            p_restored = p.replace(_DOT_TOKEN, ".").strip()
            if not p_restored:
                continue
            m_lead = _LEADING_CITS_RE.match(p_restored)
            if merged and m_lead:
                lead_cits = m_lead.group(1).strip()
                rest = p_restored[m_lead.end():].strip()
                merged[-1] = f"{merged[-1]} {lead_cits}".strip()
                if rest and not re.fullmatch(r"[.!?]+", rest):
                    merged.append(rest)
                elif rest and re.fullmatch(r"[.!?]+", rest):
                    merged[-1] = f"{merged[-1]}{rest}"
            else:
                merged.append(p_restored)
        for idx_in_line, sent in enumerate(merged):
            cits = [int(m.group(1)) for m in CITATION_PATTERN.finditer(sent)]
            units.append({
                "line_idx": li,
                "sent_idx": idx_in_line,
                "line_total": len(merged),
                "text": sent,
                "citations": cits,
            })
    return units


def _is_short_verdict_before_cited(u: dict, all_units: list[dict], pos: int) -> bool:
    """Câu chốt ngắn mở đầu ('Có.', 'Không.', 'Chưa.', 'Không hẳn.') ngay trước câu có [n] cùng dòng."""
    t_norm = unicodedata.normalize("NFC", u["text"]).strip().casefold()
    words = re.findall(r"\w+", t_norm)
    is_verdict = (t_norm in _SHORT_VERDICTS) or (len(words) <= 3 and not re.search(r"\d", t_norm))
    if not is_verdict or pos + 1 >= len(all_units):
        return False
    nxt = all_units[pos + 1]
    return nxt["line_idx"] == u["line_idx"] and bool(nxt["citations"])


def _is_non_factual_meta(sent: str) -> bool:
    s = sent.strip()
    if s.endswith("?") and not re.search(r"\d", s) and len(s) <= 100:
        return True
    lower = s.casefold()
    meta_prefixes = (
        "nếu bạn muốn", "bạn có thể hỏi thêm", "bạn muốn biết thêm",
        "tư liệu chưa có", "hiện tư liệu chưa", "nguồn tư liệu chưa",
        "trong tư liệu hiện có không nêu",
    )
    return any(lower.startswith(p) for p in meta_prefixes) and not re.search(r"\d", s)


def check_sentence_citations(answer: str, *, exempt_short_verdict: bool = True, exempt_meta: bool = True) -> dict:
    """Kiểm từng câu trong `answer` xem có ít nhất 1 mã `[n]` không (`verdict_meta_exempt`)."""
    units = split_sentences_vi(answer)
    missing = []
    exempted = []
    for i, u in enumerate(units):
        if u["citations"]:
            continue
        if exempt_short_verdict and _is_short_verdict_before_cited(u, units, i):
            exempted.append({"reason": "short_verdict", **u})
            continue
        if exempt_meta and _is_non_factual_meta(u["text"]):
            exempted.append({"reason": "meta", **u})
            continue
        missing.append(u)
    return {
        "passed": len(missing) == 0,
        "total_sentences": len(units),
        "missing_count": len(missing),
        "missing_sentences": missing,
        "exempted": exempted,
    }
