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
            metadata = make_metadata(source, title, heading, subcategory, index)
            chunks.append({"text": piece, "metadata": metadata})
            index += 1
    return chunks


def _clean_body(lines):
    """Join section body lines, dropping image-only lines."""
    kept = [line for line in lines if not IMAGE_LINE.match(line)]
    return "\n".join(kept).strip()


def _subcategory_for(source):
    """Return the folder directly under foods/, or guide for root files."""
    parts = source.split("/")
    return parts[1] if len(parts) > 2 else "guide"
