"""Convert huegov_culture_and_tourism raw files (JSON, XLSX, RDF) to Markdown
source dumps.

Generic converter using only the standard library:
- JSON: reuses the department converter pattern (list / object roots).
- XLSX: parsed from the zip XML via zipfile + xml.etree.ElementTree,
  rendering each sheet as record bullets.
- RDF/XML: parsed via ElementTree, rendering parsed DCAT/DCTERMS fields plus
  the raw XML block.
Writes one Markdown file per raw file and an index README.
"""

from datetime import datetime, timezone
from html import unescape
import json
import pathlib
import re
import xml.etree.ElementTree as ET
import zipfile

RAW_DIR = pathlib.Path("backend/data/huegov_culture_and_tourism/raw")
OUT_DIR = pathlib.Path("knowledge-base-hue/_source-dumps/huegov_culture_and_tourism")
RAW_SUBPATH = "backend/data/huegov_culture_and_tourism/raw"

SOURCE_NAME = "data.hue.gov.vn"
SOURCE_GROUP = "huegov_culture_and_tourism"

JSON_SUFFIX, XLSX_SUFFIX, RDF_SUFFIX = ".json", ".xlsx", ".rdf"

# List fields rendered record-by-record inside an object root.
LIST_FIELDS = ("data", "hienthi", "newsList", "chart", "grid")
# Scalar keys rendered as bullets inside an object root.
SCALAR_KEYS = ("code", "message", "totalRows", "totalCount")
# Preferred fields for the record heading title, in priority order.
TITLE_FIELDS = ("title", "ten", "tendoituong", "tendisan", "Ho_va_ten",
                "name", "displayName", "placeTitle", "id")

# Manual diacritic-correct H1 titles for the culture-specific JSON files.
HUMAN_TITLES = {
    "Ban_Nha_Nhac_1744278156.json": "Bản nhạc Nhã nhạc",
    "Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json":
        "Danh sách di sản văn hóa tỉnh Thừa Thiên Huế",
    "Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json":
        "Danh sách địa điểm di tích văn hóa tỉnh Thừa Thiên Huế",
    "Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json":
        "Danh sách lễ hội trên địa bàn tỉnh Thừa Thiên Huế",
    "Du-lieu-ve-gia-ve-tham-quan-di-tich-cua-Trung-tam-Bao-ton-di-tich-Co-do-Hue-1_1785085393.json":
        "Dữ liệu về giá vé tham quan di tích của Trung tâm Bảo tồn di tích Cố đô Huế",
    "Du-lieu-ve-luot-khach-tham-quan-cac-diem-Di-tich-cua-Trung-tam-Bao-ton-Di-tich-Co-do-Hue-2_1785207796 (1).json":
        "Dữ liệu về lượt khách tham quan các điểm Di tích của Trung tâm Bảo tồn Di tích Cố đô Huế",
    "Nghe_nhan_Nha_Nhac_1744278182.json": "Nghệ nhân Nhã nhạc",
    "Nhac_Chuong_Nha_Nhac_1744278211.json": "Nhạc chương Nhã nhạc",
    "Nhac_cu_Nha_Nhac_1744278236.json": "Nhạc cụ Nhã nhạc",
}

# Duplicate files with the department source dumps (byte-identical, md5 match).
DUPLICATE_WITH_DEPARTMENT = {
    "Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json":
        "Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603 (1).json",
    "Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json":
        "Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601 (1).json",
    "Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json":
        "Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601 (1).json",
}

# Empty datasets that still need a Markdown file.
EMPTY_DATASETS = ("Nhac_Chuong_Nha_Nhac_1744278211.json",)

_TAG_RE = re.compile(r"<[^>]+>")

# SpreadsheetML namespaces.
_NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_NS_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

# RDF field namespaces: (namespace URI, local name) -> label.
RDF_FIELDS = {
    ("http://purl.org/dc/terms/", "identifier"): "identifier",
    ("http://purl.org/dc/terms/", "created"): "created",
    ("http://purl.org/dc/terms/", "modified"): "modified",
    ("http://purl.org/dc/terms/", "title"): "title",
    ("http://purl.org/dc/terms/", "issued"): "issued",
    ("http://purl.org/dc/terms/", "description"): "description",
    ("https://data.thuathienhue.gov.vn/", "apiHeader"): "apiHeader",
    ("https://data.thuathienhue.gov.vn/", "apiMethod"): "apiMethod",
    ("https://data.thuathienhue.gov.vn/", "downloadURL"): "downloadURL",
    ("https://data.thuathienhue.gov.vn/", "ratingStars"): "ratingStars",
    ("http://www.w3.org/ns/dcat#", "mediaType"): "mediaType",
    ("http://www.w3.org/ns/dcat#", "byteSize"): "byteSize",
}
_RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"


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


# --- JSON rendering (same pattern as the department converter) ---

def render_field_lines(key, value):
    """Bullet lines for one record field; None when the field is empty."""
    if is_empty(value):
        return None
    if isinstance(value, str):
        text = clean_text(value)
        if not text:
            return None
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


def render_json_root(data):
    """Markdown lines for the whole JSON Content section."""
    if isinstance(data, list):
        return render_list(data)
    if isinstance(data, dict):
        return render_object(data)
    return [json_block(data)]


def detect_json_structure(data):
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
        return "\n".join(lines)
    return f"- Root type: {type(data).__name__}"


# --- XLSX rendering (standard library only) ---

def col_index(ref):
    """Column index (0-based) from a cell reference like "A3"."""
    letters = re.match(r"[A-Z]+", ref or "")
    if not letters:
        return None
    index = 0
    for ch in letters.group():
        index = index * 26 + (ord(ch) - ord("A") + 1)
    return index - 1


def cell_text(cell, shared_strings):
    """Text content of one cell: inline strings, shared strings, raw values."""
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(t.text or "" for t in cell.iter(_NS_MAIN + "t"))
    if cell_type == "s" and shared_strings is not None:
        raw = cell.findtext(_NS_MAIN + "v")
        try:
            index = int(raw)
        except (TypeError, ValueError):
            return ""
        if 0 <= index < len(shared_strings):
            return shared_strings[index]
        return ""
    value = cell.findtext(_NS_MAIN + "v")
    return value or ""


def parse_workbook(zf):
    """List of (sheet_name, sheet_rows) from an XLSX zip, in sheet order.

    sheet_rows: list of (row_number, [(col_index, value), ...]).
    """
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    targets = {}
    for rel in rels:
        if rel.get("Type", "").endswith("/worksheet"):
            targets[rel.get("Id")] = rel.get("Target")
    if "xl/sharedStrings.xml" in zf.namelist():
        shared_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        shared_strings = [
            "".join(t.text or "" for t in si.iter(_NS_MAIN + "t"))
            for si in shared_root
        ]
    else:
        shared_strings = None

    sheets = []
    for sheet in workbook.iter(_NS_MAIN + "sheet"):
        sheet_id = sheet.get(_NS_REL + "id")
        target = targets.get(sheet_id)
        if not target:
            continue
        if not target.startswith("xl/"):
            target = "xl/" + target.lstrip("/")
        sheet_root = ET.fromstring(zf.read(target))
        rows = []
        sheet_data = sheet_root.find(_NS_MAIN + "sheetData")
        if sheet_data is not None:
            for row in sheet_data.findall(_NS_MAIN + "row"):
                cells = []
                for cell in row.findall(_NS_MAIN + "c"):
                    text = clean_text(cell_text(cell, shared_strings))
                    index = col_index(cell.get("r"))
                    if index is None:
                        index = len(cells)
                    cells.append((index, text))
                cells.sort()
                rows.append((row.get("r"), cells))
        sheets.append((sheet.get("name"), rows))
    return sheets


def sheet_layout(rows):
    """(title, headers, data_rows) for one sheet, tolerantly detected.

    A leading row with a single non-empty cell is treated as the sheet title;
    the next row is treated as the header; the rest are data rows.
    """
    def non_empty(cells):
        return [(idx, value) for idx, value in cells if value]

    rows = [(r or n + 1, non_empty(cells)) for n, (r, cells) in enumerate(rows)]
    title = None
    if rows and len(rows[0][1]) == 1:
        title = rows.pop(0)[1][0][1]
    headers = {}
    if rows and rows[0][1]:
        header_row = rows.pop(0)
        for index, value in header_row[1]:
            headers[index] = value
    return title, headers, rows


def render_sheet(sheet_name, rows):
    """Markdown lines for one sheet: title + header + record bullets."""
    title, headers, data_rows = sheet_layout(rows)
    lines = [f"### Sheet: {sheet_name}"]
    if title:
        lines.append(f"- Sheet title: {title}")
    if headers:
        lines.append(f"- Header: {', '.join(headers.get(i) for i in sorted(headers))}")
    lines.append(f"- Data rows: {len(data_rows)}")
    lines.append("")
    if not data_rows:
        lines.append("No rows found.")
        return lines
    for row_number, cells in data_rows:
        lines.append(f"#### Row {row_number}")
        seen_in_row = {}
        for index, value in cells:
            if index in headers:
                header = headers[index]
                count = seen_in_row.get(header, 0) + 1
                seen_in_row[header] = count
                if count > 1:
                    header = f"{header} ({count})"
                lines.append(f"- {header}: {value}")
            else:
                lines.append(f"- Cell {index + 1}: {value}")
        lines.append("")
    return lines


def detect_xlsx_structure(sheets):
    """Short description of the XLSX structure for the Detected Structure section."""
    lines = [f"- Sheets: {len(sheets)}"]
    for sheet_name, rows in sheets:
        title, headers, data_rows = sheet_layout(rows)
        details = f"`{sheet_name}`: {len(data_rows)} data rows"
        if title:
            details += f", title \"{title}\""
        if not rows and not title:
            details += ", empty sheet"
        lines.append(f"- {details}")
    return "\n".join(lines)


def summary_xlsx(sheets):
    """Sheet description for the README table."""
    return "; ".join(
        f"{sheet_name}: {len(sheet_layout(rows)[2])} data rows"
        for sheet_name, rows in sheets)


# --- RDF rendering ---

def parse_rdf_fields(xml_text):
    """(distribution_about, [(label, value), ...]) from RDF/XML text."""
    root = ET.fromstring(xml_text)
    about = None
    for element in root.iter():
        about_attr = element.get(f"{{{_RDF_NS}}}about")
        if about_attr:
            about = about_attr
    fields = []
    for element in root.iter():
        local = element.tag.split("}")[-1]
        ns = element.tag.split("}")[0].lstrip("{") if "}" in element.tag else ""
        label = RDF_FIELDS.get((ns, local))
        if label is None:
            if not (element.text or "").strip() and not list(element):
                continue
            label = local if ns == _RDF_NS or not ns else f"{local}"
        text = clean_text(element.text or "")
        if not text:
            continue
        fields.append((label, text))
    return about, fields


def render_rdf_content(about, fields, xml_text):
    """Markdown lines for the RDF Content section."""
    lines = ["### Parsed Fields"]
    for label, value in fields:
        lines.append(f"- {label}: {value}")
    lines.append("")
    lines.append("### Raw XML")
    excerpt = xml_text if len(xml_text) <= 12000 else xml_text[:12000] + "\n...(truncated)"
    lines.append("```xml")
    lines.append(excerpt)
    lines.append("```")
    return lines


# --- Markdown assembly ---

def frontmatter(raw_name, source_format, generated_at):
    """YAML frontmatter for one output file."""
    return (
        "---\n"
        f'source_name: "{SOURCE_NAME}"\n'
        f'source_group: "{SOURCE_GROUP}"\n'
        f'source_file: "{raw_name}"\n'
        f'source_path: "{RAW_SUBPATH}/{raw_name}"\n'
        f'source_format: "{source_format}"\n'
        'conversion_type: "source_dump"\n'
        'enrichment_status: "not_enriched"\n'
        f'generated_at: "{generated_at}"\n'
        "text_transformations:\n"
        "  - strip_html\n"
        "  - decode_html_entities\n"
        "  - collapse_whitespace\n"
        "---"
    )


def build_markdown(raw_name, source_format, title, detected_structure,
                   content_lines, generated_at):
    """Assemble the full Markdown document for one raw file."""
    format_label = source_format.upper()
    parts = [
        frontmatter(raw_name, source_format, generated_at),
        "",
        f"# {title}",
        "",
        "## Source Summary",
        f"- Source file: {raw_name}",
        f"- Source format: {format_label}",
        "- Conversion type: source dump",
        "- Enrichment status: not enriched",
        "",
        "## Detected Structure",
        detected_structure,
        "",
        "## Content",
    ]
    parts.extend(content_lines)
    return "\n".join(parts).rstrip() + "\n"


def convert_file(raw_path, generated_at):
    """Convert one raw file; returns (summary_row, output name)."""
    suffix = raw_path.suffix.lower()
    raw_name = raw_path.name
    if suffix == JSON_SUFFIX:
        data = json.loads(raw_path.read_text(encoding="utf-8"))
        md_text = build_markdown(
            raw_name, "json", human_title(raw_name),
            detect_json_structure(data), render_json_root(data), generated_at)
        summary = summary_json(raw_name, data)
    elif suffix == XLSX_SUFFIX:
        with zipfile.ZipFile(raw_path) as zf:
            sheets = parse_workbook(zf)
        title = sheet_layout(sheets[0][1])[0] if sheets else None
        if not title:
            title = human_title(raw_name)
        content_lines = []
        for sheet_name, rows in sheets:
            content_lines.extend(render_sheet(sheet_name, rows))
            content_lines.append("")
        md_text = build_markdown(
            raw_name, "xlsx", title, detect_xlsx_structure(sheets),
            content_lines, generated_at)
        summary = summary_xlsx(sheets)
    else:
        xml_text = raw_path.read_text(encoding="utf-8")
        about, fields = parse_rdf_fields(xml_text)
        titles = [value for label, value in fields if label == "title"]
        descriptions = [value for label, value in fields if label == "description"]
        title = titles[0] if titles else descriptions[0] if descriptions \
            else human_title(raw_name)
        structure = [
            "- Format: RDF/XML",
            f"- Distribution: {about}" if about else "- Distribution: not found",
            f"- Parsed fields: {', '.join(label for label, _ in fields)}",
        ]
        md_text = build_markdown(
            raw_name, "rdf", title, "\n".join(structure),
            render_rdf_content(about, fields, xml_text), generated_at)
        summary = f"{len(fields)} parsed fields"
    out_name = slugify(raw_name)
    (OUT_DIR / out_name).write_text(md_text, encoding="utf-8")
    return raw_name, out_name, suffix[1:], summary


def summary_json(raw_name, data):
    """Structure description for the README table."""
    if isinstance(data, list):
        return f"list, {len(data)} records"
    if isinstance(data, dict):
        lists = [(key, len(value)) for key, value in data.items()
                 if isinstance(value, list)]
        return ", ".join(f"{key}: {n}" for key, n in lists) if lists \
            else "object, " + ", ".join(data.keys())
    return type(data).__name__


def notes_for(raw_name):
    """README notes column value for one raw file."""
    notes = []
    if raw_name in EMPTY_DATASETS:
        notes.append("empty dataset")
    if raw_name in DUPLICATE_WITH_DEPARTMENT:
        notes.append("duplicate with department")
    return ", ".join(notes)


def write_readme(rows, generated_at):
    """Index README listing every converted file and its detected structure."""
    counts = {fmt: 0 for fmt in ("json", "xlsx", "rdf")}
    for _, _, fmt, _ in rows:
        counts[fmt] += 1
    lines = [
        "# Huegov Culture and Tourism — Markdown Source Dumps",
        "",
        f"- Source: {SOURCE_NAME}",
        f"- Source group: {SOURCE_GROUP}",
        "- Conversion type: source dump",
        "- Enrichment status: not enriched",
        f"- Generated at: {generated_at}",
        "",
        f"Converted {len(rows)} raw files "
        f"({counts['json']} JSON, {counts['xlsx']} XLSX, {counts['rdf']} RDF) "
        f"from `{RAW_SUBPATH}` into Markdown source dumps. One Markdown file "
        "per raw file, no enrichment applied.",
        "",
        "## Converted Files",
        "",
        "| Markdown file | Source format | Detected structure | Notes |",
        "|---|---|---|---|",
    ]
    for raw_name, out_name, fmt, summary in rows:
        lines.append(f"| {out_name} | {fmt} | {summary} | {notes_for(raw_name)} |")
    lines.append("")
    lines.append("## Notes")
    lines.append("- No enrichment applied: content kept as-is from raw files; "
                 "only light text transformations (strip HTML, decode HTML "
                 "entities, collapse whitespace).")
    if EMPTY_DATASETS:
        lines.append("- Empty datasets (Markdown generated with "
                     "\"No records found.\"):")
        for raw_name in EMPTY_DATASETS:
            lines.append(f"  - {raw_name}")
    if DUPLICATE_WITH_DEPARTMENT:
        lines.append("- Duplicates with the department source dumps "
                     "(identical content, md5 match; converted anyway):")
        for raw_name, dept_name in DUPLICATE_WITH_DEPARTMENT.items():
            lines.append(f"  - {raw_name} == "
                         f"`huegov_department_of_tourism/raw/{dept_name}`")
    (OUT_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    raw_files = sorted(
        RAW_DIR.iterdir(),
        key=lambda p: p.name.lower())
    raw_files = [p for p in raw_files if p.suffix.lower() in
                 (JSON_SUFFIX, XLSX_SUFFIX, RDF_SUFFIX)]
    if not raw_files:
        print(f"No JSON/XLSX/RDF files found in {RAW_DIR}")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    rows = []
    for raw_path in raw_files:
        raw_name, out_name, fmt, summary = convert_file(raw_path, generated_at)
        rows.append((raw_name, out_name, fmt, summary))
        print(f"Converted {raw_name} -> {out_name}")
    write_readme(rows, generated_at)
    print(f"Done: {len(rows)} files, README.md written to {OUT_DIR}")


if __name__ == "__main__":
    main()
