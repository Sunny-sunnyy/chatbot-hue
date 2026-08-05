"""Convert huegov_department_of_tourism raw JSON files to Markdown source dumps.

Generic converter: detects the root structure (list / object) of each raw
JSON file and renders it as readable Markdown, then writes an index README.
"""

from datetime import datetime, timezone
from html import unescape
import json
import pathlib
import re

RAW_DIR = pathlib.Path("backend/data/huegov_department_of_tourism/raw")
OUT_DIR = pathlib.Path("knowledge-base-hue/_source-dumps/huegov_department_of_tourism")
RAW_SUBPATH = "backend/data/huegov_department_of_tourism/raw"

SOURCE_NAME = "data.hue.gov.vn"
SOURCE_GROUP = "huegov_department_of_tourism"

# List fields rendered record-by-record inside an object root.
LIST_FIELDS = ("data", "hienthi", "newsList", "chart", "grid")
# Scalar keys rendered as bullets inside an object root.
SCALAR_KEYS = ("code", "message", "totalRows", "totalCount")
# Preferred fields for the record heading title, in priority order.
TITLE_FIELDS = ("title", "ten", "tendoituong", "tendisan", "Ho_va_ten",
                "name", "displayName", "placeTitle", "id")

# Manual diacritic-correct H1 titles (raw filenames are unaccented).
HUMAN_TITLES = {
    "Danh-muc-loai-ve_1757394149.json": "Danh mục loại vé",
    "Danh-sach-cac-diem-du-lich_1731690004 (1).json": "Danh sách các điểm du lịch",
    "Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603 (1).json":
        "Danh sách di sản văn hóa tỉnh Thừa Thiên Huế",
    "Danh-sach-dia-diem-an-uong-tren-dia-ban-tinh_1726311604.json":
        "Danh sách địa điểm ăn uống trên địa bàn tỉnh",
    "Danh-sach-dia-diem-di-tich-tham-quan_1757394149.json":
        "Danh sách địa điểm di tích tham quan",
    "Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601 (1).json":
        "Danh sách địa điểm di tích văn hóa tỉnh Thừa Thiên Huế",
    "Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601 (1).json":
        "Danh sách lễ hội trên địa bàn tỉnh Thừa Thiên Huế",
    "Du-lieu-cac-doanh-nghiep-kinh-doanh-dich-vu-lu-hanh_1704353395.json":
        "Dữ liệu các doanh nghiệp kinh doanh dịch vụ lữ hành",
    "Du-lieu-danh-sach-co-so-kinh-doanh-dich-vu-van-chuyen-1_1731690004.json":
        "Dữ liệu danh sách cơ sở kinh doanh dịch vụ vận chuyển",
    "Gia-ve-dich-vu-di-tich-Hue_1730079840.json": "Giá vé dịch vụ di tích Huế",
    "HuongDanVienDuLich_Hue_2024-06-23_1719914684 (1).json":
        "Hướng dẫn viên du lịch Huế 2024-06-23",
}

# Limited diacritic fixes for clearly Vietnamese strings in the source data.
# Proper nouns, company names, URLs, and foreign text are kept as-is.
DIACRITIC_FIXES = (
    ("Nem chua", "Nem chua"),
    ("Kim chi chay", "Kim chi chay"),
    ("Le Loi", "Lê Lợi"),
    ("Phan Chu Trinh", "Phan Châu Trinh"),
)

_TAG_RE = re.compile(r"<[^>]+>")


def slugify(raw_name):
    """Output filename: lowercase, spaces to dashes, "(1)" to "-1"."""
    stem = pathlib.Path(raw_name).stem
    stem = re.sub(r"\((\d+)\)", r"-\1", stem)
    stem = stem.replace(" ", "-")
    stem = re.sub(r"[^a-zA-Z0-9_-]", "", stem)
    stem = re.sub(r"-{2,}", "-", stem).strip("-")
    return stem.lower() + ".md"


def human_title(raw_name):
    """H1 title: mapped diacritic title first, filename-derived fallback."""
    if raw_name in HUMAN_TITLES:
        return HUMAN_TITLES[raw_name]
    stem = pathlib.Path(raw_name).stem
    stem = re.sub(r"\s*\(1\)", "", stem)
    stem = re.sub(r"_\d{9,10}$", "", stem)
    title = re.sub(r"(?<=[a-zA-Z])-(?=[a-zA-Z])", " ", stem).replace("_", " ")
    return re.sub(r"\s+", " ", title).strip()


def clean_text(value):
    """Strip HTML tags, decode entities, and collapse whitespace."""
    text = _TAG_RE.sub(" ", unescape(value))
    return re.sub(r"\s+", " ", text).strip()


def is_empty(value):
    """True when the value carries no information worth dumping."""
    if value is None or value == "":
        return True
    if isinstance(value, (list, dict)) and not value:
        return True
    if isinstance(value, str) and not clean_text(value):
        return True
    return False


def best_title(record):
    """First non-empty title field, in priority order."""
    for field in TITLE_FIELDS:
        value = record.get(field)
        if not is_empty(value):
            return str(value).strip()
    return None


def json_block(value):
    """Fenced JSON block for nested structures that do not render generically."""
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```"


def render_field_lines(key, value):
    """Bullet lines for one record field; None when the field is empty."""
    if is_empty(value):
        return None
    if isinstance(value, str):
        text = clean_text(value)
        if not text:
            return None
        for plain, accented in DIACRITIC_FIXES:
            text = text.replace(plain, accented)
        return [f"- {key}: {text}"]
    if isinstance(value, (int, float, bool)):
        return [f"- {key}: {value}"]
    if isinstance(value, list):
        if all(isinstance(item, (str, int, float, bool)) for item in value):
            return [f"- {key}: {', '.join(str(item) for item in value)}"]
        return [f"- {key}:", json_block(value)]
    if isinstance(value, dict):
        return [f"- {key}:", json_block(value)]
    return [f"- {key}: {value}"]


def render_record(record, n):
    """Markdown lines for a single record."""
    title = best_title(record)
    heading = f"### Record {n}: {title}" if title else f"### Record {n}"
    lines = [heading]
    for key, value in record.items():
        field_lines = render_field_lines(key, value)
        if field_lines:
            lines.extend(field_lines)
    return lines


def render_list(items):
    """Markdown lines for a list of records."""
    if not items:
        return ["No records found."]
    lines = []
    for n, item in enumerate(items, 1):
        if isinstance(item, dict):
            lines.extend(render_record(item, n))
        else:
            lines.append(f"### Record {n}")
            lines.append(f"- {item}")
        lines.append("")
    return lines


def render_object(obj):
    """Markdown lines for an object root: scalars as bullets, list fields
    as records, anything else as a JSON block."""
    lines = ["### Root Object"]
    for key, value in obj.items():
        if key in SCALAR_KEYS and not is_empty(value):
            lines.append(f"- {key}: {value}")
    for key, value in obj.items():
        if key not in SCALAR_KEYS and key not in LIST_FIELDS and not is_empty(value):
            lines.append(f"- {key}:")
            lines.append(json_block(value))
    for key, value in obj.items():
        if key in LIST_FIELDS:
            if is_empty(value):
                lines.append(f"#### {key}: no records")
                lines.append("No records found.")
            elif isinstance(value, list):
                lines.append(f"#### {key} ({len(value)} records)")
                lines.extend(render_list(value))
    return lines


def render_root(data):
    """Markdown lines for the whole Content section."""
    if isinstance(data, list):
        return render_list(data)
    if isinstance(data, dict):
        return render_object(data)
    return [json_block(data)]


def detect_structure(data):
    """Short description of the JSON structure for the Detected Structure section."""
    if isinstance(data, list):
        lines = ["- Root type: list", f"- Records: {len(data)}"]
        if data and isinstance(data[0], dict):
            lines.append(f"- Sample record keys: {', '.join(data[0].keys())}")
        return "\n".join(lines)
    if isinstance(data, dict):
        lines = ["- Root type: object",
                 f"- Top-level keys: {', '.join(data.keys())}"]
        for key, value in data.items():
            if isinstance(value, list):
                sample = ""
                if value and isinstance(value[0], dict):
                    sample = f" (sample keys: {', '.join(value[0].keys())})"
                lines.append(f"- `{key}`: list of {len(value)} records{sample}")
            elif key in SCALAR_KEYS and not is_empty(value):
                lines.append(f"- {key}: {value}")
        total_rows, payload = data.get("totalRows"), data.get("data")
        if isinstance(total_rows, int) and isinstance(payload, list) \
                and total_rows != len(payload):
            lines.append(f"- Note: totalRows ({total_rows}) differs from actual "
                         f"records ({len(payload)})")
        return "\n".join(lines)
    return f"- Root type: {type(data).__name__}"


def frontmatter(raw_name, generated_at):
    """YAML frontmatter for one output file."""
    return (
        "---\n"
        f'source_name: "{SOURCE_NAME}"\n'
        f'source_group: "{SOURCE_GROUP}"\n'
        f'source_file: "{raw_name}"\n'
        f'source_path: "{RAW_SUBPATH}/{raw_name}"\n'
        'source_format: "json"\n'
        'conversion_type: "source_dump"\n'
        'enrichment_status: "not_enriched"\n'
        f'generated_at: "{generated_at}"\n'
        "---"
    )


def build_markdown(raw_name, data, generated_at):
    """Assemble the full Markdown document for one raw file."""
    parts = [
        frontmatter(raw_name, generated_at),
        "",
        f"# {human_title(raw_name)}",
        "",
        "## Source Summary",
        f"- Source file: {raw_name}",
        "- Source format: JSON",
        "- Conversion type: source dump",
        "- Enrichment status: not enriched",
        "",
        "## Detected Structure",
        detect_structure(data),
        "",
        "## Content",
    ]
    parts.extend(render_root(data))
    return "\n".join(parts).rstrip() + "\n"


def count_records(data):
    """Total records across the list fields (or the list itself)."""
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        return sum(len(value) for value in data.values()
                   if isinstance(value, list))
    return 0


def summary_row(raw_name, data):
    """(markdown name, root type, records description, total records) tuple."""
    md_name = slugify(raw_name)
    if isinstance(data, list):
        return md_name, "list", f"{len(data)} records", len(data)
    if isinstance(data, dict):
        lists = [(key, len(value)) for key, value in data.items()
                 if isinstance(value, list)]
        desc = ", ".join(f"{key}: {n}" for key, n in lists) if lists \
            else ", ".join(data.keys())
        return md_name, "object", desc, count_records(data)
    return md_name, type(data).__name__, "", 0


def write_readme(rows, generated_at):
    """Index README listing every converted file and its detected structure."""
    total = len(rows)
    lines = [
        "# Huegov Department of Tourism — Markdown Source Dumps",
        "",
        f"- Source: {SOURCE_NAME}",
        f"- Source group: {SOURCE_GROUP}",
        "- Conversion type: source dump",
        "- Enrichment status: not enriched",
        f"- Generated at: {generated_at}",
        "",
        f"Converted {total} raw JSON files from `{RAW_SUBPATH}` into Markdown "
        "source dumps. One Markdown file per raw file, no enrichment applied.",
        "",
        "## Converted Files",
        "",
        "| Markdown file | Root type | Records / list fields |",
        "|---|---|---|",
    ]
    for md_name, root, desc, _ in rows:
        lines.append(f"| {md_name} | {root} | {desc} |")
    lines.append("")
    lines.append("## Notes")
    large = [row for row in rows if row[3] > 1000]
    if large:
        lines.append("- Large files (over 1000 records):")
        for md_name, _, desc, _ in large:
            lines.append(f"  - {md_name}: {desc}")
    lines.append("- Diacritic fixes applied on conversion (proper nouns and "
                 "company names kept as-is):")
    for plain, accented in DIACRITIC_FIXES:
        lines.append(f"  - `{plain}` -> `{accented}`")
    mismatch = []
    for raw_path in sorted(RAW_DIR.glob("*.json")):
        data = json.loads(raw_path.read_text(encoding="utf-8"))
        total_rows = data.get("totalRows") if isinstance(data, dict) else None
        payload = data.get("data") if isinstance(data, dict) else None
        if isinstance(total_rows, int) and isinstance(payload, list) \
                and total_rows != len(payload):
            mismatch.append(f"  - {raw_path.name}: totalRows={total_rows} but "
                            f"data list has {len(payload)} records")
    if mismatch:
        lines.append("- Source discrepancy, kept as-is:")
        lines.extend(mismatch)
    (OUT_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    raw_files = sorted(RAW_DIR.glob("*.json"))
    if not raw_files:
        print(f"No JSON files found in {RAW_DIR}")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    rows = []
    for raw_path in raw_files:
        data = json.loads(raw_path.read_text(encoding="utf-8"))
        out_name = slugify(raw_path.name)
        (OUT_DIR / out_name).write_text(
            build_markdown(raw_path.name, data, generated_at), encoding="utf-8")
        rows.append(summary_row(raw_path.name, data))
        print(f"Converted {raw_path.name} -> {out_name}")
    write_readme(rows, generated_at)
    print(f"Done: {len(rows)} files, README.md written to {OUT_DIR}")


if __name__ == "__main__":
    main()
