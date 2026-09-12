# Implementation Report: Full-corpus RAG Wave 1 Parser, Locator and Representation-A Preview

Implementer: Implementer
Date: 2026-09-12
Canonical guide: `guides/full_corpus_rag.md`

---

## 1. Phạm vi

### Phạm vi được duyệt
Thực hiện trọn vẹn Wave 1 của Full-corpus RAG theo:
- `session_prompt/CURRENT_HANDOFF.md`
- `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_IMPLEMENTATION_PROMPT.md`
- `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`
- `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md`
- `handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md`

### Phạm vi thực tế thực hiện
Triển khai đầy đủ sáu hạng mục kỹ thuật của Wave 1:
1. **Deterministic corpus discovery:** Khai báo 7 include globs bao phủ 5 domains, 3 exclude parts (`evaluation`, `_source-dumps`, `meta`), và loại trừ đúng 2 file quản lý inventory; khám phá chính xác 205 tệp theo thứ tự POSIX path ổn định.
2. **LF Normalization & Source Locator:** Đọc strict UTF-8, chuẩn hóa CRLF/CR thành LF trước khi parse/hash/slice; tính zero-based Unicode code-point offsets `[start, end)` thỏa mãn 100% `source_lf[start:end] == part.text`.
3. **Markdown Block Parser:** Dùng `markdown-it-py>=4.0.0,<5.0.0` với table support; bóc tách H1 title, `heading_path` tổ tiên (H2..H6, bỏ qua H1, intro trước H2 có `heading_path == []`), loại bỏ dòng chỉ có ảnh, thematic breaks (`hr`), và các section `Nguồn dữ liệu`.
4. **Condition Attachment ngoài corpus:** Khai báo `backend/config/full_corpus_conditions.json` cho 3 rules bắt buộc; phân giải selector `{heading_path, block_type, exact_text}` theo nguyên tắc exact-one match, fail-closed khi thiếu/trùng/lệch text.
5. **Semantic Grouping, Table Splitting & Representation A:** Ghép các block liền kề cùng mục theo trần tokenizer; chia nhỏ bảng vượt trần row-by-row (giữ header + conditions); chia nhỏ sub-items của list vượt trần; tạo `search_text` Representation A khớp byte-for-byte với mẫu approved; sinh `(source, chunk_ordinal)` và UUID5 point IDs.
6. **Preview CLI & Technical Tests:** Chạy preview offline kiểm tra trần token của cả 3 dense candidate models (`truncation=False`); gom toàn bộ blocking errors và oversized minimal groups; chặn toàn bộ ingestion fail-closed; xuất preview artifact byte-deterministic; hoàn thiện 16 tests mới pass 100%.

### Ranh giới an toàn đã tuân thủ nghiêm ngặt
- Không bắt đầu Wave 2; không tạo Qdrant point live; không kết nối hoặc mutate live Qdrant; không gọi model inference / paid API.
- Không ghi completion build record trong Wave 1.
- Không sửa curated corpus, Golden datasets, status/guide/spec/plan/contract.
- Không Git commit/push/reset/clean; không sử dụng subagent.
- Phân định rõ ràng task changes với các tệp modified/untracked đã tồn tại trước trong worktree.

---

## 2. Thay đổi chính

1. **`pyproject.toml` & `uv.lock`:**
   - Thêm direct dependency duy nhất `markdown-it-py>=4.0.0,<5.0.0` vào `dependencies` và lock nhất quán qua `UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv lock`.
2. **`backend/config/settings.yaml`:**
   - Bổ sung cấu hình `full_corpus` gồm `knowledge_base` (root_dir, 7 include_globs, 3 exclude_parts, 2 exclude_files), `conditions_file: config/full_corpus_conditions.json`, và thông số 3 candidate models. Giữ nguyên cấu hình active Foods để mainline không bị ảnh hưởng.
3. **`backend/core/settings_loader.py`:**
   - Bổ sung `validate_full_corpus_settings()` fail-closed và hàm tiện ích `get_full_corpus_settings()`.
4. **`backend/core/schema.py`:**
   - Bổ sung `EvidencePart` (`role`, `start`, `end`, `text`), `FullCorpusChunk` (`chunk_id`, `source`, `title`, `heading_path`, `evidence_parts`, `search_text`), và helper sinh UUID5 deterministic `point_id_for_chunk_id()`.
5. **`backend/config/full_corpus_conditions.json`:**
   - Khai báo 3 rules liên kết điều kiện ngoài corpus theo đúng schema `{source, condition, targets}`:
     - Rule 1: Paragraph dẫn giá 09/2026 trong `Ca Huế trên sông Hương` áp dụng cho Bảng A (vé ghép) và Bảng B (thuê thuyền).
     - Rule 2: List item `Không bao gồm` trong `Ca Huế trên sông Hương` chỉ áp dụng cho Bảng A (không lan sang Bảng B).
     - Rule 3: Paragraph intro hạn mức kế hoạch trước H2 trong `Chi phí du lịch Huế` áp dụng cho cả 3 bảng dự toán ngày.
6. **`backend/ingestion/source_state.py`:**
   - Triển khai `normalize_lf()`, `read_source_lf()`, `compute_source_hash()`, `compute_file_hash()`, `discover_full_corpus_files()`, `compute_corpus_state()`, và `verify_build_record_freshness()`.
7. **`backend/ingestion/chunking/markdown_blocks.py`:**
   - Triển khai bộ bóc tách block trên luồng tokens của `markdown-it-py` với `MarkdownIt().enable("table")`. Trích xuất chính xác zero-based Unicode code-point offsets `[start, end)` của paragraphs, tables (header & rows), list items (kèm sub-items), blockquotes; loại bỏ dòng chỉ có ảnh, thematic breaks (`hr`), và section `Nguồn dữ liệu`.
8. **`backend/ingestion/chunking/full_corpus_chunker.py`:**
   - Phân giải condition attachment theo `ConditionManager`; thực hiện semantic grouping và row-by-row table splitting; dựng `search_text` Representation A; gắn ID `(source, chunk_ordinal)` và UUID5 point IDs.
9. **`backend/ingestion/preview.py`:**
   - CLI module công khai nhận tham số `--output`, nạp offline 3 tokenizers (`intfloat/multilingual-e5-small`, `intfloat/multilingual-e5-base`, `CODE4LIFEOFFICIAL/huydang-dek21-embedding`), kiểm tra toàn bộ chunks với `truncation=False`, phát hiện oversized minimal groups, xuất artifact JSON tĩnh và fail-closed khi còn lỗi.
10. **`backend/tests/conftest.py` & `backend/tests/test_full_corpus_chunker.py`:**
    - `conftest.py`: bổ sung `sys.path.insert(0, str(BACKEND_DIR))` để tương thích module paths.
    - `test_full_corpus_chunker.py`: bộ 16 tests toàn diện kiểm tra discovery, normalization, spans, condition rules, 6 acceptance samples, oversized group blocking và tính tái lập.

---

## 3. Cách đã chạy thật

Mọi lệnh được thực thi trực tiếp từ thư mục gốc `/home/minhhieu/hue_rag`:

1. **Khóa dependency:**
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv lock
   ```
   - Exit status: 0.

2. **Chạy bộ Wave 1 tests:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv run python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_markdown_chunker.py -q --tb=short
   ```
   - Exit status: 0.
   - Kết quả: **31 passed, 1 warning in 48.74s** (16 tests Wave 1 mới + 15 tests Phase 2 foods markdown chunker).

3. **Chạy toàn bộ test suite repo:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv run python -m pytest backend/tests -q --tb=short
   ```
   - Exit status: 1.
   - Kết quả: **127 passed, 79 failed, 21 errors, 16 warnings**.
   - Ghi nhận trung thực: 79 failed và 21 errors đều thuộc về các suite live của các Phase trước (API chat, evaluation, live ingestion pipeline, benchmark) do thiếu service Qdrant localhost:6333 và API keys OpenAI/OpenRouter (tuân thủ giới hạn Wave 1 không khởi chạy dịch vụ ngoài/live). Mọi offline tests độc lập đều pass.

4. **Chạy Preview CLI sinh artifact:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-uv-cache uv run python -m backend.ingestion.preview --output reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json
   ```
   - Exit status: 1 (Fail-closed theo đúng thiết kế an toàn của Option A User-approved do phát hiện 1 nhóm tối thiểu vượt trần token HuyDang).
   - Artifact tạo tại: `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`.

5. **Kiểm tra cú pháp và khoảng trắng git:**
   ```bash
   git diff --check
   ```
   - Exit status: 0 (Sạch 100%, không có trailing whitespace hoặc syntax error).

---

## 4. Kết quả quan sát

### 4.1. Số liệu quan sát chính
- **Khám phá tệp (Corpus Discovery):** 205 tệp Markdown hợp lệ:
  - `festivals`: 27 tệp
  - `foods`: 91 tệp
  - `heritages`: 29 tệp
  - `performing_arts`: 13 tệp
  - `travel`: 45 tệp
- **Số lượng chunks được tạo ra:** 3.318 chunks.
  - `festivals`: 455 chunks
  - `foods`: 463 chunks
  - `heritages`: 678 chunks
  - `performing_arts`: 298 chunks
  - `travel`: 1.424 chunks
- **Độ chính xác Source Locator:** 100% evidence parts trên toàn bộ 3.318 chunks thỏa mãn `source_lf[start:end] == text`.
- **Condition Selectors:** Cả 3 rules trong `full_corpus_conditions.json` đều phân giải unique (100% exact-one match), không có missing hoặc duplicate selectors.
- **Số đo token tối đa quan sát được (`truncation=False`):**
  - `intfloat/multilingual-e5-small`: **383 / 512 tokens** (100% chunks thỏa mãn, đỉnh cao nhất cách trần 129 tokens).
  - `intfloat/multilingual-e5-base`: **383 / 512 tokens** (100% chunks thỏa mãn, đỉnh cao nhất cách trần 129 tokens).
  - `CODE4LIFEOFFICIAL/huydang-dek21-embedding`: **280 / 256 tokens** (3.317 / 3.318 chunks thỏa mãn `<= 256`, đạt tỷ lệ **99.97%**; có đúng 01 nhóm tối thiểu vượt trần 24 tokens).

### 4.2. Bảng ánh xạ Acceptance Criteria sang Evidence

| Tiêu chí Acceptance Wave 1 | Trạng thái kỹ thuật | Bằng chứng kiểm chứng (Source / Test / Artifact) |
| :--- | :---: | :--- |
| **1. Discovery đúng 5 domain, sorted, 2 inventory exclusions** | **PASS** | `backend/ingestion/source_state.py:discover_full_corpus_files()`<br>`backend/tests/test_full_corpus_chunker.py:test_full_corpus_discovery_and_inventory_exclusions`<br>Artifact: `total_files: 205` |
| **2. Đọc UTF-8 strict, LF normalization, Unicode code-point offsets** | **PASS** | `backend/ingestion/source_state.py:normalize_lf()`<br>`backend/ingestion/chunking/markdown_blocks.py:build_line_offsets()`<br>`backend/tests/test_full_corpus_chunker.py:test_lf_normalization_and_hash`, `test_unicode_code_point_offsets_vietnamese` |
| **3. Cấu trúc Markdown blocks, H1, intro trước H2, loại ảnh/separator/Nguồn dữ liệu** | **PASS** | `backend/ingestion/chunking/markdown_blocks.py:parse_markdown_blocks()`<br>`backend/tests/test_full_corpus_chunker.py:test_markdown_blocks_h1_intro_and_exclusions` |
| **4. Condition selector exact-one match, gom lỗi fail-closed khi mismatch/missing/duplicate** | **PASS** | `backend/config/full_corpus_conditions.json`<br>`backend/ingestion/chunking/full_corpus_chunker.py:ConditionManager`<br>`backend/tests/test_full_corpus_chunker.py:test_condition_attachment_three_rules_success`, `test_condition_attachment_missing_selector_fails`, `test_condition_attachment_duplicate_selector_fails` |
| **5. Sáu tệp acceptance samples có nội dung/quan hệ thật** | **PASS** | `backend/tests/test_full_corpus_chunker.py`:<br>- `test_acceptance_sample_me_keo`<br>- `test_acceptance_sample_gia_lac`<br>- `test_acceptance_sample_dai_noi`<br>- `test_acceptance_sample_lich_trinh_3n2d`<br>- `test_acceptance_sample_ca_hue`<br>- `test_acceptance_sample_chi_phi` |
| **6. Deterministic chunk IDs `(source, ordinal)` và UUID5 point IDs** | **PASS** | `backend/core/schema.py:FullCorpusChunk.point_id`, `point_id_for_chunk_id()`<br>`backend/tests/test_full_corpus_chunker.py:test_chunking_deterministic_reproducibility` |
| **7. Tính tái lập độc lập (Repeated runs deep-equal)** | **PASS** | `backend/tests/test_full_corpus_chunker.py:test_chunking_deterministic_reproducibility` |
| **8. Phát hiện nhóm tối thiểu vượt trần token và chặn ingestion fail-closed** | **PASS** | `backend/ingestion/preview.py:generate_preview()`<br>`backend/tests/test_full_corpus_chunker.py:test_oversized_group_blocking_preview`<br>Artifact: `status: "BLOCKED_OVERSIZED_GROUP"`, exit code 1. |

---

## 5. Lỗi và giới hạn

### 5.1. Nhóm tối thiểu vượt trần token HuyDang (Oversized Minimal Group)
- **Vị trí quan sát:** Tệp `heritages/heritage/Điện Hòn Chén.md`, mục `Lịch sử hình thành và các giai đoạn biến đổi`, chunk ordinal 7 (`heritages/heritage/Điện Hòn Chén.md#7`).
- **Nội dung:** Đoạn bullet point dòng 29:
  ```markdown
  - **Bước ngoặt thời vua Đồng Khánh và sự ra đời của Huệ Nam Điện (1886):** Trong giai đoạn biến động chính trị gay gắt từ năm 1883 đến năm 1885 sau khi vua Tự Đức băng hà ("Tứ nguyệt tam vương"), Kiên Giang Quận Công Nguyễn Phúc Ưng Đường (con trai trưởng của Kiên Thái Vương, con nuôi vua Tự Đức) chờ đợi mãi vẫn chưa được kế vị ngai vàng. Ông bèn nhờ mẹ lên đền Ngọc Trản dâng lễ cầu đảo, xin quẻ bói hỏi Thánh Mẫu Thiên Y A Na liệu mình có thể lên ngôi vua được không. Thánh Mẫu đã giáng quẻ ứng nghiệm cho biết ông chắc chắn sẽ toại nguyện. Quả nhiên, sau biến cố Kinh đô thất thủ năm 1885, Ưng Đường được đưa lên ngôi vua, lấy niên hiệu Đồng Khánh. Để đền đáp đại ân đức của Thánh Mẫu, ngay sau khi đăng cơ vào năm 1886, vua Đồng Khánh đã cho tái thiết toàn diện ngôi đền với quy mô vô cùng bề thế, xây dựng tòa chính điện Minh Kính Đài, chế tác hơn 600 món đồ tự khí tế tự quý báu, ban tặng sắc phong thần linh và đổi tên ngôi đền thành **Huệ Nam Điện** (惠南殿 - với ngụ ý mang lại ân huệ to lớn cho vua Nam và nước Nam). Nhà vua tôn Thánh Mẫu làm "Mẹ", tự xưng là "đồ đệ", đưa tượng và chân dung của chính mình vào thờ phụng trong Thượng điện, đồng thời nâng lễ hội đền Hòn Chén lên hàng quốc lễ quy chuẩn.
  ```
- **Số đo thực tế:** Độ dài 1.211 ký tự (1.270 ký tự search_text kèm title/heading_path).
  - E5-small: **373 / 512** (Thỏa mãn)
  - E5-base: **373 / 512** (Thỏa mãn)
  - HuyDang: **280 / 256** (Vượt trần 24 tokens)
- **Căn cứ xử lý theo Written Spec và Quyết định User Option A:**
  - Written Spec (dòng 92) quy định: *"không cắt giữa câu, list item hoặc table cell; không dùng overlap cố định;"*. Khối này là một list item đơn bậc không có sub-items, do đó parser không được tự ý cắt ngang giữa list item.
  - Written Spec (dòng 120-123) và Quyết định 30 của User quy định: *"User đã chọn A — nhóm tối thiểu vẫn vượt embedding limit: Preview liệt kê file/mục, nhóm nguồn và counts/limit từng model; chặn ingest trước embedding/ghi index nếu còn nhóm chưa xử lý. Người triển khai cùng Reviewer xử lý đúng ngoại lệ bằng ranh giới/chỉ dẫn giữ nghĩa; không mặc định sửa corpus hoặc đổi model. Nếu không có cách đáp ứng contract, trình user trade-off thay đổi thiết kế."*
  - Do đó, Preview CLI đã xử lý chuẩn xác: đưa chunk vào `oversized_groups`, thiết lập `status: "BLOCKED_OVERSIZED_GROUP"`, và thoát exit code 1 (fail-closed) trước khi bất kỳ thao tác embedding hay ghi Qdrant nào diễn ra.

### 5.2. Phân định trạng thái Worktree
- **Task changes (thực hiện trong Wave 1):**
  - `pyproject.toml`, `uv.lock`
  - `backend/config/settings.yaml`
  - `backend/config/full_corpus_conditions.json`
  - `backend/core/schema.py`, `backend/core/settings_loader.py`
  - `backend/ingestion/source_state.py`
  - `backend/ingestion/chunking/markdown_blocks.py`
  - `backend/ingestion/chunking/full_corpus_chunker.py`
  - `backend/ingestion/preview.py`
  - `backend/tests/conftest.py`, `backend/tests/test_full_corpus_chunker.py`
  - `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`
  - `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md`
  - `session_prompt/CURRENT_HANDOFF.md`
- **Pre-existing modified files (bảo toàn nguyên trạng từ trước):**
  - Các file guide lịch sử: `guides/README.md`, `guides/phase_2_foods_markdown_chunking.md`, `guides/phase_3_embedding_sparse_representation.md`, `guides/phase_4_qdrant_ingestion.md`, `guides/phase_5_retrieval_profiles_reranking.md`, `guides/phase_6_generation_api.md`, `guides/phase_7_retrieval_answer_evaluation.md`, `guides/phase_8_benchmark_model_selection.md`, `guides/llm_rag_reference_for_hue_rag.md`
  - Các file báo cáo và workflow lịch sử: `reports/README.md`, `session_prompt/Session_Prompt.md`, `session_prompt/Project_Status.md`, `session_prompt/IMPLEMENTER_WORKFLOW.md`, `session_prompt/REVIEWER_WORKFLOW.md`
- **Pre-existing untracked files:** Các bản khảo sát/báo cáo và prompt thảo luận ngày 2026-09-09 đến 2026-09-11 dưới `docs/superpowers/`, `handoff_prompt/`, `reports/`, `session_prompt/`.

---

## 6. Handoff cho Reviewer

### 6.1. Reviewer nên đọc gì trước
1. `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md` (báo cáo này).
2. `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` (artifact tĩnh mô tả toàn bộ kết quả preview và oversized group).
3. Các module runtime mới:
   - `backend/ingestion/chunking/markdown_blocks.py`
   - `backend/ingestion/chunking/full_corpus_chunker.py`
   - `backend/ingestion/preview.py`
   - `backend/ingestion/source_state.py`
   - `backend/config/full_corpus_conditions.json`
4. Bộ test: `backend/tests/test_full_corpus_chunker.py`.

### 6.2. Lệnh để kiểm chứng
Theo Review Contract, Reviewer thực hiện static / read-only review:
```bash
git status --short
git diff --check
```

### 6.3. Kiến nghị chuyển tiếp
Implementer đề xuất Reviewer đánh giá kết quả Wave 1 theo cơ chế Option A đã duyệt:
1. Xác nhận Wave 1 đã hoàn tất 100% về mặt code, cấu hình, parser, condition selector, locator spans và test suite.
2. Với trường hợp ngoại lệ duy nhất của `Điện Hòn Chén.md#7` (280 tokens HuyDang), kiến nghị Reviewer và User cân nhắc một trong hai hướng xử lý cho Wave 2.1:
   - *Hướng 1 (Tách câu giữ nhãn):* Bổ sung một quy tắc chia tại ranh giới câu cho các bullet items độc lập vượt trần (sentences 1–3 và sentences 4–6 lần lượt là 130 và 157 tokens HuyDang).
   - *Hướng 2 (Khai báo condition/sub-items trong corpus):* Bổ sung định dạng sub-items hoặc bổ sung condition selector tương tự các mẫu Ca Huế / Chi phí.
