"""Parse curated Markdown into a document title and semantic sections."""


def parse_document(text):
    """Parse markdown text into (title, sections).

    The H1 line becomes the title. Each H2 heading starts a new section
    dict with keys "heading" (heading text) and "body" (remaining lines).
    Content before the first H2 is returned as a section with an empty
    heading. H3 and deeper headings stay inside the section body.
    Sections without body content are omitted.
    """
    title = ""
    sections = []
    current = {"heading": "", "body": []}
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            sections.append(current)
            current = {"heading": line[3:].strip(), "body": []}
        else:
            current["body"].append(line)
    sections.append(current)
    return title, [
        section for section in sections if "\n".join(section["body"]).strip()
    ]
