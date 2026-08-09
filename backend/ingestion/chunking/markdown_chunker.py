"""Chunk curated foods Markdown into semantic sections.

Discovers files from the knowledge_base settings, parses each file into
H2 sections, and returns chunk dicts with stable metadata.
"""
import re

from core.settings_loader import BACKEND_DIR, load_settings
from ingestion.helpers.make_metadata import make_metadata
from ingestion.helpers.markdown_parser import parse_document
from ingestion.helpers.split_text import split_text

EXCLUDED_SECTIONS = {"Nguồn dữ liệu"}
IMAGE_LINE = re.compile(r"\s*!\[.*\]\(.*\)\s*$")

# Fixed-rule context labels for known section headings.
_DIRECT_LABELS = {
    "Tóm tắt": "giới thiệu",
    "Menu và giá tham khảo": "menu",
    "Món ăn / trải nghiệm": "trải nghiệm",
    "Thành phần và đặc điểm": "thành phần",
    "Cách làm tóm tắt": "cách làm",
    "Địa điểm tiêu biểu": "địa điểm",
    "Nguồn gốc và bối cảnh": "nguồn gốc",
    "Cách thưởng thức": "cách thưởng thức",
    "Ưu đãi tham khảo": "ưu đãi",
    "Các cơ sở tại Huế": "cơ sở tại Huế",
    "Gợi ý cho người mới": "người mới",
    "Lần đầu đến Huế nên thử gì?": "lần đầu",
    "Gợi ý ăn sáng": "ăn sáng",
    "Gợi ý ăn trưa": "ăn trưa",
    "Gợi ý ăn chiều và ăn vặt": "ăn chiều và ăn vặt",
    "Gợi ý ăn tối": "ăn tối",
    "Gợi ý ăn đêm": "ăn đêm",
    "Cà phê và đồ uống": "cà phê và đồ uống",
    "Gợi ý món chay": "món chay",
    "Gợi ý món ngọt": "món ngọt",
    "Theo ngân sách": "ngân sách",
    "Gợi ý theo nhóm người dùng": "nhóm người dùng",
    "Food tour nửa ngày": "tour nửa ngày",
    "Food tour 1 ngày": "tour 1 ngày",
    "Food tour 2 ngày": "tour 2 ngày",
    "Food tour 3 ngày": "tour 3 ngày",
    "Các loại bánh ép": "các loại bánh ép",
    "Giá tham khảo và lưu ý dinh dưỡng": "giá tham khảo",
    "Các biến tấu": "biến tấu",
    "Biến thể theo vùng miền": "biến thể",
    "Kỹ thuật và dụng cụ truyền thống": "kỹ thuật truyền thống",
    "Bối cảnh văn hóa và cách gọi": "bối cảnh văn hóa",
    "Ghi nhận và lan tỏa": "ghi nhận",
    "Các biến thể liên quan": "biến thể",
    "Các loại mè xửng phổ biến": "các loại phổ biến",
    "Bối cảnh văn hóa và cách thưởng thức": "bối cảnh văn hóa",
    "Mua làm quà": "mua làm quà",
}

_THONG_TIN_TOPICS = (
    ("Địa chỉ", "địa chỉ"),
    ("Giờ hoạt động", "giờ hoạt động"),
    ("Mức giá", "mức giá"),
)


def chunk_foods_markdown():
    """Discover curated foods Markdown and return list of chunk dicts."""
    root, files = _discover_markdown_files()
    chunks = []
    for path in files:
        chunks.extend(_chunk_file(path, root))
    return chunks


def _discover_markdown_files():
    """Resolve the KB root from settings and list included markdown files."""
    kb = load_settings()["knowledge_base"]
    root = (BACKEND_DIR / kb["root_dir"]).resolve()
    exclude_parts = kb["exclude_parts"]
    files = set()
    for pattern in kb["include_globs"]:
        for path in root.glob(pattern):
            if path.is_file() and not _is_excluded(path, exclude_parts, root):
                files.add(path)
    return root, sorted(files, key=lambda path: str(path.relative_to(root)))


def _is_excluded(path, exclude_parts, root):
    """True when any path segment matches an excluded folder name."""
    return any(part in exclude_parts for part in path.relative_to(root).parts)


def _chunk_file(path, root):
    """Chunk one markdown file into section chunks."""
    title, sections = parse_document(path.read_text(encoding="utf-8"))
    source = str(path.relative_to(root)).replace("\\", "/")
    subcategory = _subcategory_for(source)
    chunks = []
    index = 0
    for section in sections:
        heading = section["heading"]
        body = _clean_body(section["body"])
        if not body or heading in EXCLUDED_SECTIONS:
            continue
        for piece in split_text(body):
            label = _context_label(subcategory, heading, piece)
            metadata = make_metadata(source, title, heading, subcategory, index)
            chunks.append({"text": f"{title} — {label}\n{piece}", "metadata": metadata})
            index += 1
    return chunks


def _context_label(subcategory, heading, text):
    """Return a short fixed-rule context label for a chunk.

    Known headings map directly; a generic `Thông tin` section gets a
    specific label only when the chunk covers exactly one topic.
    """
    if heading == "Thông tin":
        found = {label for marker, label in _THONG_TIN_TOPICS if marker in text}
        return found.pop() if len(found) == 1 else "thông tin quán"
    return _DIRECT_LABELS.get(heading, heading.strip().lower())


def _clean_body(lines):
    """Join section body lines, dropping image-only lines."""
    kept = [line for line in lines if not IMAGE_LINE.match(line)]
    return "\n".join(kept).strip()


def _subcategory_for(source):
    """Return the folder directly under foods/, or guide for root files."""
    parts = source.split("/")
    return parts[1] if len(parts) > 2 else "guide"
