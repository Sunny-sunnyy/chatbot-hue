# Phase 2: Khám phá và chunking Foods Markdown

> Full-corpus extension cập nhật 2026-09-12: Written Spec, Plan, Review Contract
> và exact Phase 2 prompt đã được User duyệt. Phase 2 discovery/parser/chunker/
> locator/Representation A preview đã qua ba correction, independent review và
> được User xác nhận closure ngày 2026-09-12. Phase 3 chỉ được triển khai theo
> package và active handoff đã được User duyệt;
> implementation, embedding/Qdrant/live. Khảo sát parser/source locator đã
> approved sau correction lượt 3. [Review/closure](../reports/full_corpus_parser_locator_codex_review_2026_09_09.md)
> là evidence thiết kế. Chọn markdown-it-py/table enabled. Hai input VN/QT đúng
> ranh giới đã đo bổ sung và user-approved: [review](../reports/full_corpus_vn_qt_token_check_codex_review_2026_09_09.md).
> VN: E5 290/290, HuyDang 224, MiniLM orig/long 411/453; QT: 268/268,
> 208, 385/427. Chỉ áp dụng inputs/queries mẫu; không dùng counts input sai.


## Tham chiếu thiết kế mở rộng toàn corpus — cập nhật 2026-09-12

Guide này vẫn là contract đã approved cho Foods Phase 2. Entry point của thiết
kế đa domain là [Full-corpus RAG](full_corpus_rag.md); phần extension cùng
approved Spec/Plan/Review Contract và exact Phase 2 prompt tạo design package
hiện hành. Các mục Foods lịch sử không tự mở rộng quyền ngoài Phase 2 prompt.

MVP mới kế thừa và điều chỉnh MVP Foods trong guides/backend cho toàn bộ curated
corpus, không chỉ đổi glob ingestion. User đã xác nhận hướng chunking baseline:

- discovery ổn định trên năm domain, chỉ lấy tài liệu answer-facing;
- chia theo cấu trúc Markdown H2/H3/H4 và ngân sách token tính cả nhãn/context;
- giữ mục ngắn, list cha/con, bảng và điều kiện liên quan khi phù hợp; không
  mặc định mỗi heading là một chunk hoặc mọi bảng đều được vượt input limit;
- dùng tên tài liệu và heading gốc, bỏ nhãn đặc thù Foods;
- bảo toàn nguyên văn và vị trí nguồn, tách text tìm kiếm khỏi evidence;
- chưa dùng LLM chia đoạn hoặc tự mở rộng context sau Top-5 ở baseline;
- dùng chung bộ chunk cho benchmark E5-small, E5-base và HuyDang; kiểm input
  thực bằng từng tokenizer, giữ preprocessing theo model và evidence gốc;
- đánh giá trên corpus mới; 400 ký tự, bảy metadata fields và 572 chunks không
  phải acceptance của thiết kế full-corpus;
- user chọn chặn ingest trước embedding/ghi index nếu nhóm tối thiểu vẫn
  vượt limit mà chưa chia đủ nghĩa; không ingest thiếu các nhóm đó;
- chuẩn hóa CRLF/CR thành LF cho source locator; đổi kiểu xuống dòng đơn
  thuần không yêu cầu ingest lại, không tự đổi dấu hoặc gộp whitespace.

Nhánh thử nghiệm B sau baseline đã chốt theo hướng có chọn lọc: giữ nguyên
bộ chunk A, chỉ thêm context tìm kiếm do API sinh khi input đầy đủ vừa cả
E5-small, E5-base và HuyDang. Chunk không vừa giữ representation A; không
cắt body/điều kiện hoặc đổi boundaries. Context sinh lưu riêng, không phải
evidence/Golden. Báo cáo tỷ lệ được bổ sung và chất lượng trên toàn bộ tập
câu hỏi. Đây không phải bước lấy thêm điều kiện sau Top-5 hoặc quyền gọi API.

Contract Phase 2 nằm trong Written Spec, Implementation Plan, Review Contract,
initial prompt và correction chain. Observed canonical artifact sau closure ghi
205 sorted/unique files, 8460 chunks, ba condition rules, zero errors/oversized;
max token `366/512`, `366/512`, `255/256`. Implementer báo 39 offline tests pass
và repeated preview byte-identical; Reviewer không rerun dynamic checks. `8460`
 là observed result, không phải hard invariant. Phase 2 chưa embedding, chưa ghi
Qdrant/build record và không cutover Foods runtime.

Phân định trạng thái: Foods Phase 2 bên dưới là as-built history 91 files/572
chunks của runtime hiện hành; full-corpus target là behavior trong approved
Spec/Plan; observed Phase 2 là offline preview 205 files/8460 chunks. Ba lớp này
không được dùng thay thế lẫn nhau.

Các mục bên dưới giữ contract và approval **Foods lịch sử**, được đối chiếu với
simplicity implementation/review/user report. Chúng không khẳng định backend
đã triển khai các thay đổi full-corpus ở trên.

## Mục tiêu và giá trị cho người dùng

Phase 2 chuyển curated Markdown về ẩm thực Huế thành semantic chunks ổn định, answer-facing và có metadata đủ để index, truy xuất, trích nguồn và đánh giá ở các phase sau.

## Trạng thái

```text
Status: approved
Document type: as-built technical history with governance remediation
Implementer: DeepSeek
Reviewer: Codex
Approval date +07: 2026-08-09
Simplicity design approval +07: 2026-08-24
Simplicity technical review +07: passed 2026-08-24
Simplicity confirmation +07: 2026-08-24
```

Phase 2 vẫn giữ approval lịch sử ngày `2026-08-09 +07`. Implementation đơn giản
hóa đã đạt independent technical review sau correction round 1 và được user
xác nhận ngày `2026-08-24 +07`; phase hiện ở `approved`.

## Dependency

- Phase 0 và Phase 1 đã hoàn tất.
- Input chỉ đến từ curated Markdown dưới `knowledge-base-hue/foods/`.
- Không dùng `_source-dumps`, `meta` hoặc evaluation data làm chunk input.
- Không cần embedding, Qdrant, model API hoặc web.

Người dùng đã chạy notebook, yêu cầu cải thiện cách hiển thị mẫu và phê duyệt
thay đổi cách chia đoạn. Phạm vi đó đã được triển khai, review và xác nhận.
Lịch sử kiểm tra kỹ thuật trước thay đổi được giữ nguyên.

## Corpus research đã thực hiện

Mini research kiểm tra toàn corpus:

- 91 Markdown files;
- 57 restaurant files;
- 24 cafe files;
- 9 local specialty files;
- một `food-guides.md`;
- 454 mục H2 tổng cộng;
- 90 mục `Nguồn dữ liệu` bị loại;
- 364 mục H2 dùng để tạo nội dung trả lời;
- hai image-only Markdown lines trong hai restaurant files;
- 24 bảng Markdown; 8 bảng dài hơn 400 ký tự, bảng dài nhất 927 ký tự;
- có H3 subsections nằm trong H2 body;
- chỉ hai sections dài hơn 1.500 ký tự, đều trong `food-guides.md`, dài nhất 2.298 ký tự;
- tất cả files bắt đầu bằng đúng một H1, không có pre-H2 content hoặc empty section trong corpus đã khảo sát.

Phân bố độ dài đã đo trực tiếp trên 364 mục dùng để trả lời:

| Phạm vi | Trung bình | Trung vị | 90% không vượt quá | Lớn nhất |
|---|---:|---:|---:|---:|
| Một mục H2 | 430 | 349 | 800 | 2.298 |
| Một khối đoạn văn hoặc bảng | 258 | 227 | 524 | 1.261 |
| Một bảng Markdown | 391 | 266 | 835 | 927 |

## Chức năng lịch sử đã thực hiện

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

## Phạm vi thay đổi đã được phê duyệt

- Giữ H2 làm ranh giới nội dung chính.
- Đổi giới hạn phần nội dung từ 1.500 xuống 400 ký tự.
- Không tính nhãn ngữ cảnh vào giới hạn 400 ký tự.
- Ưu tiên ngắt tại đoạn văn, cuối câu và giữa các dòng danh sách.
- Nếu một câu vẫn dài hơn 400 ký tự, ngắt tại khoảng trắng gần nhất; không cắt
  giữa từ.
- Không chồng lặp giữa hai chunk liên tiếp.
- Giữ nguyên một bảng Markdown như một khối, kể cả khi dài hơn 400 ký tự.
- Thêm một nhãn ngữ cảnh ngắn vào đầu mỗi chunk bằng quy tắc cố định, không gọi
  AI và không thêm dữ liệu ngoài file nguồn.
- Giữ nguyên bảy trường metadata và công thức `chunk_id` ổn định.
- Cải thiện notebook để người học phân biệt nội dung thật, phần xem trước và cú
  pháp bảng Markdown.

## Files canonical

```text
backend/ingestion/helpers/split_text.py
backend/ingestion/chunking/markdown_chunker.py
backend/tests/test_markdown_chunker.py
notebooks/02_foods_data_and_chunking.ipynb
```

Parsing, minimal validation và metadata construction nằm trực tiếp trong
`markdown_chunker.py`. `split_text.py` là helper duy nhất còn lại vì thuật toán
splitting có hành vi độc lập cần đọc và kiểm tra riêng.

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
    "text": "Tên tài liệu — nhãn ngắn\nNội dung section không rỗng",
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

H2 heading đi vào `metadata.section`. H3 không tạo top-level chunk mới vì nó
thuộc ngữ nghĩa của H2 hiện tại. Chunk text bắt đầu bằng tiêu đề tài liệu và một
nhãn ngữ cảnh ngắn, sau đó mới tới phần nội dung gốc.

### Nhãn ngữ cảnh

Nhãn phải ngắn, tự nhiên và đúng với nội dung thật, ví dụ:

```text
ANH KAFE tại Huế — địa chỉ
```

Quy tắc:

- restaurants/cafes dùng các nhãn như `giới thiệu`, `địa chỉ`,
  `giờ hoạt động`, `mức giá`, `menu`, `trải nghiệm`;
- local specialties dùng các nhãn như `giới thiệu`, `thành phần`, `cách làm`,
  `nguồn gốc`, `địa điểm`;
- food guide dùng chủ đề ngắn của mục như `ăn sáng`, `ăn tối`, `món chay`,
  `tour 1 ngày`;
- mục có tên rõ như menu hoặc nguồn gốc được ánh xạ trực tiếp;
- với mục chung như `Thông tin`, chỉ dùng nhãn cụ thể khi phần nội dung có đúng
  một chủ đề nhận diện được; nếu có nhiều chủ đề thì dùng nhãn chung như
  `thông tin quán`;
- không chép địa chỉ thật vào nhãn và không ghép danh sách dài các chủ đề.

### Source section exclusion

`EXCLUDED_SECTIONS` loại `Nguồn dữ liệu`. Quyết định này phù hợp curated-data rules: source tracking không phải nội dung trực tiếp để trả lời. Payload vẫn giữ `metadata.source` để trace file.

### Image handling

Image-only line `![alt](url)` bị loại vì alt text và URL không cung cấp answer text đáng tin cậy. Surrounding prose vẫn giữ nguyên.

### Long section handling

`split_text` giới hạn phần nội dung thông thường ở `max_chars=400`. Hàm phải
nhận biết đoạn văn, danh sách và bảng; ưu tiên ranh giới tự nhiên, không cắt giữa
từ và không chồng lặp. Bảng là khối nguyên tử và được phép vượt giới hạn.

## Quyết định thiết kế đã chốt

Ba hướng đã được cân nhắc: sao chép nguyên `split_paragraphs()` của `llm_rag`,
giữ mức 1.500 ký tự, hoặc kế thừa nguyên tắc `llm_rag` nhưng điều chỉnh cho
Markdown. Người dùng chọn hướng thứ ba.

Hàm cũ không được sao chép nguyên xi vì có thể cắt cứng giữa bảng, câu hoặc từ.
Mức 400 ký tự được dùng làm cấu hình nền ban đầu vì trung vị của mục H2 hiện là
349 ký tự, tổng dữ liệu dự kiến vẫn nhỏ và đây là mốc đã dùng trong `llm_rag`.
Phase 8 có thể so sánh 400 với 600 hoặc 800 bằng cùng bộ câu hỏi đánh giá.

## Nhiệm vụ của DeepSeek Implementer

DeepSeek chỉ thực hiện phạm vi đã phê duyệt:

- sửa `split_text.py`, `markdown_chunker.py` và tests cần thiết;
- giữ parser và metadata contract nếu không có bằng chứng bắt buộc phải đổi;
- tạo nhãn bằng quy tắc cố định, không dùng model hoặc web;
- không sửa curated Markdown để làm test pass;
- đo lại số chunk và phân bố thật, không giữ cứng con số 366;
- cập nhật notebook Phase 2 với ba ví dụ có chủ đích: một đoạn văn, một bảng và
  một đoạn food guide; dùng hiển thị Markdown để bảng có hàng/cột rõ ràng;
- ghi độ dài phần nội dung, giải thích phần xem trước không cắt dữ liệu thật;
- làm sạch outputs và đưa mọi `execution_count` về `null` trước handoff;
- cập nhật implementation report với file, lệnh và kết quả kiểm tra thật;
- không sửa guide, Codex review, user report hoặc `Project_Status.md`.

## Nhiệm vụ của Codex Reviewer

- Đối chiếu claim với corpus và tests.
- Kiểm tra absolute path, secret/live tokens, image/source exclusion và stable IDs.
- Đánh giá blast radius đến Phase 3–8 nếu chunk output thay đổi.
- Không approve re-chunking mà không nêu yêu cầu reindex và benchmark comparability.

## Notebook contract cho lần sửa này

Notebook giữ tên `notebooks/02_foods_data_and_chunking.ipynb` và import backend
modules, không chép lại logic chia đoạn. Notebook phải:

- hiển thị discovery, metadata schema và số liệu corpus mới;
- hiển thị đúng ba ví dụ: đoạn văn, bảng Markdown đã render và food guide;
- giải thích dấu `|`, hàng `---`, giới hạn 400, ngoại lệ bảng và nhãn ngữ cảnh;
- phân biệt rõ phần xem trước với nội dung chunk thật;
- committed outputs rỗng;
- mọi `execution_count` là `null`;
- không chứa live API, web, Qdrant, secret hoặc private absolute path.

## Kiểm tra lịch sử đã được chấp nhận

```bash
cd backend
uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
uv run python -m pytest tests/ -q
uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0]['metadata'])"
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

Các số liệu 366 chunks và 17 tests chỉ là lịch sử trước thay đổi, không phải kết
quả mong đợi cố định của lần triển khai mới.

## Kiểm tra bắt buộc cho thay đổi mới

- Phần nội dung thông thường không vượt 400 ký tự trước khi thêm nhãn.
- Bảng Markdown giữ nguyên và được phép vượt 400 ký tự.
- Không cắt giữa từ; danh sách ưu tiên ngắt giữa các dòng.
- Mỗi chunk có đúng một nhãn ngắn và nhãn không thêm dữ liệu mới.
- Không có chunk rỗng; đủ bảy metadata fields.
- `chunk_id` unique và stable qua hai lần chạy với cùng input.
- Vẫn xử lý đủ 91 files và loại đúng folders/sections đã chốt.
- Không còn yêu cầu số chunk phải bằng 366; report phải ghi số thật.
- Toàn bộ tests cũ còn phù hợp phải tiếp tục đạt; bổ sung tests cho hành vi mới.
- Notebook JSON hợp lệ, outputs rỗng, execution counts null và không external
  call.

## Accepted deviations và limitations

- Không có deviation khỏi approved phase scope.
- `Nguồn dữ liệu` exclusion tiếp tục được giữ nguyên.
- Giới hạn mới là 400 ký tự cho phần nội dung; bảng là ngoại lệ có chủ ý.
- Threshold tiếp tục nằm trong module; Phase 8 mới thực hiện so sánh có kiểm soát.
- `backend/tests/` không có `__init__.py`; approved command chạy từ `backend/` nên imports resolve đúng.

## Security, data safety, reliability và performance

- Knowledge base chỉ được đọc, không bị sửa.
- Không có web, model, Qdrant, deploy hoặc secret access.
- Discovery sorted và single-pass trên corpus nhỏ.
- Chunk text xuất phát từ curated body, không hallucinate data.
- Stable IDs hỗ trợ repeatable indexing và evaluation.

## Reports và bằng chứng

Current simplicity evidence:

```text
reports/phase_2_foods_markdown_chunking_simplicity_review.md
reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md
reports/phase_2_foods_markdown_chunking_simplicity_codex_review.md
reports/user_reports/phase_2_foods_markdown_chunking_simplicity_user_report.md
```

Historical Phase 2 evidence trước simplicity review:

```text
reports/phase_2_foods_markdown_chunking_implementation_report.md
reports/phase_2_foods_markdown_chunking_codex_review.md
reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
```

Phase 2 gốc được user xác nhận ngày `2026-08-09`; simplicity implementation
được user xác nhận ngày `2026-08-24 +07`. Kết luận hiện hành: `approved`.

## Tiêu chí phê duyệt

- Corpus discovery đúng scope.
- Semantic section chunks có text không rỗng và có nhãn ngữ cảnh ngắn.
- Required metadata đầy đủ và paths an toàn.
- Nội dung thường tuân giới hạn 400; bảng/H3 giữ được ngữ cảnh;
  image/source-only lines không gây noise.
- Tests, notebook safety và deterministic IDs đạt gate.
- Không có external access hoặc data mutation.
- Notebook đúng tên Phase 2, hiển thị ba mẫu đã chốt và đạt quy tắc an toàn.
- User report mô tả đúng validation/limitations và được người dùng xác nhận.

Các tiêu chí kỹ thuật, notebook và xác nhận của người dùng đã đạt ngày
2026-08-09.

## Bước tiếp theo

Foods Phase 2 đã hoàn thành simplicity review và giữ `approved`; production
Foods vẫn là 572 chunks. Full-corpus Phase 2 cũng đã User-closed nhưng chưa
cutover. Phase 3 Written Spec, Plan và Review Contract đã được User duyệt ngày
2026-09-12; active handoff giao Implementer thực hiện bounded dense/sparse
preflight, chưa mở Phase 4 hoặc Qdrant.

## Quyết định được người dùng phê duyệt ngày 2026-08-09

```text
Decision: Dùng H2 làm ranh giới chính; chia phần nội dung thường ở 400 ký tự; giữ nguyên bảng; không chồng lặp; thêm một nhãn ngữ cảnh ngắn.
Approved by: User
Approval date +07: 2026-08-09
Evidence: Brainstorming sau khi người dùng chạy notebook Phase 2 và yêu cầu xem lại cách chia đoạn.
Affected scope: split_text.py, markdown_chunker.py, tests, notebook Phase 2, implementation report, Codex review và user report Phase 2.
Revisit trigger: Kết quả kiểm tra retrieval cho thấy 400 ký tự làm mất ngữ cảnh hoặc Phase 8 bắt đầu so sánh kích thước chunk.
```

```text
Decision: Sửa số liệu corpus thành 454 mục H2 tổng cộng, loại 90 mục Nguồn dữ liệu và dùng 364 mục trả lời.
Approved by: User
Approval date +07: 2026-08-09
Evidence: Đo trực tiếp 91 curated foods files bằng parser hiện tại và được người dùng xác nhận.
Affected scope: Guide, notebook, implementation report, Codex review và user report Phase 2.
Revisit trigger: Curated foods corpus thay đổi.
```
