"""Build chunk metadata for foods Markdown chunks."""

CATEGORY = "foods"


def make_metadata(source, title, section, subcategory, chunk_index):
    """Return the metadata dict for one chunk with a stable chunk_id."""
    return {
        "chunk_id": f"{source}|{section}|{chunk_index}",
        "source": source,
        "title": title,
        "section": section,
        "category": CATEGORY,
        "subcategory": subcategory,
        "chunk_type": "section" if section else "intro",
    }
