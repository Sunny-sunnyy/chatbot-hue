# Phase 2: Khám phá và chunking Foods Markdown

## Mục tiêu và giá trị cho người dùng

Phase 2 chuyển curated Markdown về ẩm thực Huế thành semantic chunks ổn định, answer-facing và có metadata đủ để index, truy xuất, trích nguồn và đánh giá ở các phase sau.

## Trạng thái

```text
Status: approved
Document type: as-built, locked
Brainstorming level: Level 0 - locked
Implementer: DeepSeek
Reviewer: Codex
Approval date +07: 2026-08-09
```

## Dependency

- Phase 0 và Phase 1 đã hoàn tất.
- Input chỉ đến từ curated Markdown dưới `knowledge-base-hue/foods/`.
- Không dùng `_source-dumps`, `meta` hoặc evaluation data làm chunk input.
- Không cần embedding, Qdrant, model API hoặc web.

## Corpus research đã thực hiện

Mini research kiểm tra toàn corpus:

- 91 Markdown files;
- 57 restaurant files;
- 24 cafe files;
- 9 local specialty files;
- một `food-guides.md`;
- 908 H2 sections trước exclusion/aggregation;
- hai image-only Markdown lines trong hai restaurant files;
- khoảng 40 menu tables cùng các bảng local specialty;
- có H3 subsections nằm trong H2 body;
- chỉ hai sections dài hơn 1.500 ký tự, đều trong `food-guides.md`, dài nhất 2.298 ký tự;
- tất cả files bắt đầu bằng đúng một H1, không có pre-H2 content hoặc empty section trong corpus đã khảo sát.

## Chức năng đã thực hiện

- Discover Markdown deterministically theo sorted path.
- Parse H1 thành document title.
- Parse H2 thành semantic section boundary.
- Giữ H3 headings, paragraph và table trong section body.
- Loại `## Nguồn dữ liệu` khỏi answer-facing chunks.
- Loại image-only Markdown lines khỏi chunk text.
- Split long sections theo blank-line paragraph boundaries với `max_chars=1500`.
- Không tách một block đơn lẻ lớn hơn limit để tránh phá table.
- Tạo stable metadata và deterministic `chunk_id`.
- Tạo learning notebook chỉ import runtime modules.

## Files canonical

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/helpers/split_text.py
backend/ingestion/chunking/markdown_chunker.py
backend/tests/test_markdown_chunker.py
notebooks/01_foods_data_and_chunking.ipynb
```

## Input contract

Curated food file:

- không có YAML frontmatter;
- bắt đầu bằng `# <title>`;
- H2 là semantic section;
- section optional không có dữ liệu thì không xuất hiện;
- `## Nguồn dữ liệu` phục vụ source tracking nhưng không answer-facing;
- không thêm content mới hoặc suy diễn ngoài Markdown.

Discovery config dùng KB-relative paths và exclude exact path segments:

```text
evaluation
_source-dumps
meta
```

## Output contract

Mỗi chunk có shape:

```python
{
    "text": "Nội dung section không rỗng",
    "metadata": {
        "chunk_id": "foods/cafes/example.md|Tóm tắt|0",
        "source": "foods/cafes/example.md",
        "title": "Tên tài liệu",
        "section": "Tóm tắt",
        "category": "foods",
        "subcategory": "cafes",
        "chunk_type": "section",
    },
}
```

Metadata invariants:

- đúng bảy required fields;
- `source` là path tương đối với `knowledge-base-hue/`, không phải absolute path;
- `subcategory` là folder trực tiếp dưới `foods/`;
- `food-guides.md` dùng `subcategory=guide`;
- `chunk_id = f"{source}|{section}|{index}"` với running index theo file;
- IDs unique và stable khi input không đổi.

## Parsing và splitting decisions

### Section boundary

H2 heading đi vào `metadata.section`; chunk text chỉ chứa body. H3 không tạo top-level chunk mới vì nó thuộc ngữ nghĩa của H2 hiện tại.

### Source section exclusion

`EXCLUDED_SECTIONS` loại `Nguồn dữ liệu`. Quyết định này phù hợp curated-data rules: source tracking không phải nội dung trực tiếp để trả lời. Payload vẫn giữ `metadata.source` để trace file.

### Image handling

Image-only line `![alt](url)` bị loại vì alt text và URL không cung cấp answer text đáng tin cậy. Surrounding prose vẫn giữ nguyên.

### Long section handling

`split_text` greedily pack paragraph blocks đến `max_chars=1500`. Oversized atomic block được giữ nguyên, tránh phá Markdown table hoặc làm mất cấu trúc.

## Brainstorming

Không brainstorm lại Phase 2. Các interpretation trên đã được Codex phê duyệt.

Nếu thay threshold, exclusion rule, chunk granularity, metadata fields hoặc ID formula, phải:

1. mở scope mới;
2. đánh giá ảnh hưởng đến embedding/index/evaluation artifacts;
3. quyết định có cần reindex và regenerate relevance judgments;
4. cập nhật guide qua Codex trước implementation.

## Nhiệm vụ của DeepSeek Implementer

Phase đã hoàn tất. Với scope mới, implementer phải giữ deterministic behavior, thêm test trước khi sửa parser/splitter và không sửa curated data để làm test pass.

## Nhiệm vụ của Codex Reviewer

- Đối chiếu claim với corpus và tests.
- Kiểm tra absolute path, secret/live tokens, image/source exclusion và stable IDs.
- Đánh giá blast radius đến Phase 3–8 nếu chunk output thay đổi.
- Không approve re-chunking mà không nêu yêu cầu reindex và benchmark comparability.

## Notebook contract đã đạt

`notebooks/01_foods_data_and_chunking.ipynb`:

- 9 cells;
- import backend modules, không duplicate parser/chunker;
- hiển thị discovery, schema, corpus statistics và sample theo document type khi người dùng tự chạy;
- committed outputs rỗng;
- mọi `execution_count` là `null`;
- không chứa live API, web, Qdrant, secret hoặc private absolute path.

## Validation đã được phê duyệt

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0]['metadata'])"
```

Accepted evidence:

- 366 chunks từ 91 files;
- distribution: restaurants 187, cafes 100, local_specialties 62, guide 17;
- 17 tests passed;
- non-empty text và đủ metadata;
- no absolute source paths;
- excluded folders không xuất hiện;
- no image Markdown trong chunk text;
- `Nguồn dữ liệu` không trở thành chunk;
- IDs unique và stable qua repeated runs.

## Accepted deviations và limitations

- Không có deviation khỏi approved phase scope.
- `Nguồn dữ liệu` exclusion và 1.500-character default là approved interpretations.
- Threshold nằm trong module default thay vì `settings.yaml`; thay đổi sau này cần controlled chunking experiment.
- `backend/tests/` không có `__init__.py`; approved command chạy từ `backend/` nên imports resolve đúng.

## Security, data safety, reliability và performance

- Knowledge base chỉ được đọc, không bị sửa.
- Không có web, model, Qdrant, deploy hoặc secret access.
- Discovery sorted và single-pass trên corpus nhỏ.
- Chunk text xuất phát từ curated body, không hallucinate data.
- Stable IDs hỗ trợ repeatable indexing và evaluation.

## Reports và bằng chứng

```text
reports/phase_2_foods_markdown_chunking_implementation_report.md
reports/phase_2_foods_markdown_chunking_codex_review.md
```

Codex verdict: `approved`.

## Tiêu chí phê duyệt

- Corpus discovery đúng scope.
- Semantic section chunks có text không rỗng.
- Required metadata đầy đủ và paths an toàn.
- Tables/H3 giữ được ngữ cảnh; image/source-only lines không gây noise.
- Tests, notebook safety và deterministic IDs đạt gate.
- Không có external access hoặc data mutation.

Tất cả tiêu chí đã đạt ngày 2026-08-09.

## Bước tiếp theo

Phase 3 phải dùng 366 canonical chunks này làm baseline input và hoàn tất Level 2 brainstorming trước implementation.
