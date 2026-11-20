---
source_name: "data.hue.gov.vn"
source_group: "huegov_culture_and_tourism"
source_file: "CHUA-DIEM-PHUNG--CONG-VIEN-THUY-TU-jpeg,.jpg.rdf"
source_path: "backend/data/huegov_culture_and_tourism/raw/CHUA-DIEM-PHUNG--CONG-VIEN-THUY-TU-jpeg,.jpg.rdf"
source_format: "rdf"
conversion_type: "source_dump"
enrichment_status: "not_enriched"
generated_at: "2026-08-05T12:51:00.172557+00:00"
text_transformations:
  - strip_html
  - decode_html_entities
  - collapse_whitespace
---

# CHÙA DIÊM PHỤNG - CÔNG VIÊN THỦY TÚ

## Source Summary
- Source file: CHUA-DIEM-PHUNG--CONG-VIEN-THUY-TU-jpeg,.jpg.rdf
- Source format: RDF
- Conversion type: source dump
- Enrichment status: not enriched

## Detected Structure
- Format: RDF/XML
- Distribution: https://data.hue.gov.vn/Distribution/CHUA-DIEM-PHUNG--CONG-VIEN-THUY-TU
- Parsed fields: identifier, created, modified, title, issued, description, apiHeader, downloadURL, mediaType, byteSize, ratingStars

## Content
### Parsed Fields
- identifier: 62DBC63B-66E8-4487-8461-35226386D0C2
- created: 2025-12-13
- modified: 2025-12-13
- title: CHÙA DIÊM PHỤNG - CÔNG VIÊN THỦY TÚ
- issued: 2025-12-13T09:21:39
- description: https://htxnongnghiepso.github.io/chua-diem-phung/
- apiHeader: https://htxnongnghiepso.github.io/chua-diem-phung/
- downloadURL: /Upload\Metadata\000.00.14.H57\2025\476388755_929733502647163_8506640129004335523_n_1765592510.jpg
- mediaType: image/jpeg
- byteSize: 147006
- ratingStars: 1

### Raw XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF 
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
xmlns:dcat="http://www.w3.org/ns/dcat#"
xmlns:dcterms="http://purl.org/dc/terms/"
xmlns:foaf="http://xmlns.com/foaf/0.1/"
xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
xmlns:vcard="http://www.w3.org/2006/vcard/ns#"
xmlns:org="http://www.w3.org/ns/org#"
xmlns:hueod="https://data.thuathienhue.gov.vn/">
<dcat:Distribution rdf:about="https://data.hue.gov.vn/Distribution/CHUA-DIEM-PHUNG--CONG-VIEN-THUY-TU">
<dcterms:identifier rdf:datatype="xsd:string">62DBC63B-66E8-4487-8461-35226386D0C2</dcterms:identifier>
<dcterms:created rdf:datatype="xsd:dateTime">2025-12-13</dcterms:created>
<dcterms:modified rdf:datatype="xsd:dateTime">2025-12-13</dcterms:modified>
<dcterms:title xml:lang="vi">CHÙA DIÊM PHỤNG - CÔNG VIÊN THỦY TÚ</dcterms:title>
<dcterms:issued rdf:datatype="xsd:dateTime">2025-12-13T09:21:39</dcterms:issued>
<dcterms:description xml:lang="vi">https://htxnongnghiepso.github.io/chua-diem-phung/</dcterms:description>
<hueod:apiHeader xml:lang="vi">https://htxnongnghiepso.github.io/chua-diem-phung/</hueod:apiHeader>
<hueod:apiMethod rdf:resource="get"/>
<hueod:downloadURL rdf:datatype="xsd:distributionFile">/Upload\Metadata\000.00.14.H57\2025\476388755_929733502647163_8506640129004335523_n_1765592510.jpg</hueod:downloadURL>
<dcat:mediaType xml:lang="vi">image/jpeg</dcat:mediaType>
<dcat:byteSize rdf:datatype="xsd:nonNegativeInteger">147006</dcat:byteSize>
<hueod:ratingStars rdf:datatype="xsd:nonNegativeInteger">1</hueod:ratingStars>
</dcat:Distribution>
</rdf:RDF>
```
