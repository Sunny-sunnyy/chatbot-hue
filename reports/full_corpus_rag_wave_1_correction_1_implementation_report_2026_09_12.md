# Implementation Report: Full-corpus RAG Wave 1 Correction 1, 2 & 3

Implementer: Implementer
Date: 2026-09-12
Canonical guide: `guides/full_corpus_rag.md`
Review Report tham chiếu: `reports/full_corpus_rag_wave_1_correction_2_codex_review_2026_09_12.md`
Active Contract: `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_3_PROMPT.md`

---

## 1. Phạm vi

### 1.1. Phạm vi thực hiện
Báo cáo này là một index bằng chứng (evidence index) trung thực, phản ánh chính xác mã nguồn, cấu hình, artifact và các lệnh kiểm thử thực tế đã chạy để giải quyết trọn vẹn:
- 5 Major findings ban đầu (W1-R1 đến W1-R5) trong `reports/full_corpus_rag_wave_1_codex_review_2026_09_12.md`.
- 1 Blocker (W1-C1-R1) và 2 Major findings (W1-C1-R2, W1-C1-R3) trong `reports/full_corpus_rag_wave_1_correction_1_codex_review_2026_09_12.md`.
- 1 Major finding (W1-C2-R1) trong `reports/full_corpus_rag_wave_1_correction_2_codex_review_2026_09_12.md`:
  - Chạy `chunk_full_corpus()` hai lần độc lập để so sánh deep-equal toàn bộ chunks, `chunk_id`, và `point_id`; kiểm tra tính duy nhất, hàm sinh `point_id_for_chunk_id()`, và chuẩn UUID phiên bản 5.
  - Loại bỏ hoàn toàn các phép nối đa chunk (`" ".join(...)`) trong kiểm thử hai tệp mẫu Mệ Kéo và Gia Lạc; chọn đúng exact chunk và kiểm tra quan hệ nội dung trên chính `search_text` và `evidence_parts` của chunk đó.
  - Chứng minh rõ ràng sự tách biệt giữa không gian lịch sử (ngã ba làng Nam Phổ) và không gian phục dựng đương đại (ngã ba Chợ Mai, Nguyễn Đình Tứ) trong Hội xuân Gia Lạc là hai chunk riêng biệt với chunk ID khác nhau.

### 1.2. Ranh giới an toàn
- Không mở rộng sang Wave 2.1 (không tạo Qdrant collection mới, không upsert point, không ghi build record).
- Không can thiệp raw corpus, golden reference datasets, guides, spec, plan hay review report lịch sử.
- Không sửa production code/config hoặc canonical artifact trong phạm vi Correction 3 (chỉ sửa test assertions theo đúng allowed paths).
- Không chạy full backend test suite (`backend/tests`) hoặc integration suite (`test_ingestion_pipeline.py`) vì chúng yêu cầu live Qdrant daemon và live inference API nằm ngoài phạm vi Wave 1 offline.
- Không git commit/push/clean; không sử dụng subagent.
- Phân định rõ ràng các tệp pre-existing modified/untracked trong worktree.

---

## 2. Thay đổi chính

### 2.1. Danh sách tệp thay đổi và tạo mới thuộc Wave 1
1. `backend/config/settings.yaml` (bổ sung cấu hình `full_corpus.embedding_models` và trường `word_segment`).
2. `backend/config/full_corpus_conditions.json` (khai báo 3 condition rules chuẩn schema ngoài corpus).
3. `backend/core/schema.py` (bổ sung `EvidencePart`, `FullCorpusChunk`, và helper UUID5 `point_id_for_chunk_id`).
4. `backend/core/settings_loader.py` (bổ sung fail-closed validation cho cấu hình full_corpus).
5. `backend/ingestion/source_state.py` (chuẩn hóa LF, SHA-256 hash, discovery 205 files, kiểm tra freshness).
6. `backend/ingestion/chunking/markdown_blocks.py` (parser token state `in_tbody`, trích xuất exact slice cho blockquote, table và nested list parent label).
7. `backend/ingestion/chunking/full_corpus_chunker.py` (sentence splitting, lặp leading bold label, exact selector matching `match_block_selector`, schema validation `_validate_selector_schema`, và cache tokenizer checker theo settings `_CHECKER_CACHE`).
8. `backend/ingestion/preview.py` (dynamic local snapshot resolution, phân rã 5 domains & 7 P7 partitions, tách biệt trạng thái `BLOCKED_OVERSIZED_GROUP` và `BLOCKED_ERRORS`, xuất canonical preview byte-deterministic).
9. `backend/tests/conftest.py` (bổ sung sys.path cho backend directory).
10. `backend/tests/test_full_corpus_chunker.py` (bộ 24 tests kỹ thuật toàn diện bao phủ toàn bộ yêu cầu, cập nhật per-chunk assertions cho Mệ Kéo/Gia Lạc và repeated chunk/UUID5 determinism).
11. `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` (canonical artifact đạt PASS, 0 errors, 0 oversized).
12. `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md` (báo cáo này).
13. `session_prompt/CURRENT_HANDOFF.md` (bàn giao trạng thái cho Reviewer).

### 2.2. Chi tiết các điểm kỹ thuật hoàn thiện trong Correction 3 (W1-C2-R1)

1. **Kiểm chứng repeated chunking, chunk IDs, và UUID5:**
   - Trong `test_full_corpus_determinism_and_preview_byte_equality`, pipeline chạy `chunk_full_corpus()` độc lập 2 lần (`chunks_run1` và `chunks_run2`).
   - Thực hiện deep-equality trên từng cặp chunk: so sánh `chunk_id`, `point_id`, `source`, `title`, `heading_path`, `search_text`, và danh sách `evidence_parts`.
   - Kiểm tra chặt chẽ `point_id`:
     - Phải khớp chính xác với giá trị sinh từ helper `point_id_for_chunk_id(chunk_id)`.
     - Phải đạt tính duy nhất tuyệt đối trên toàn bộ 8.460 chunks (không có ID trùng lặp).
     - Phải là định dạng UUID phiên bản 5 chuẩn (`uuid.UUID(point_id).version == 5`).
   - Kiểm tra 100% evidence parts của toàn bộ các chunks khớp byte-for-byte với nguồn chuẩn hóa LF.
   - Kiểm tra sinh preview 2 lần ra 2 file độc lập và so sánh `read_bytes()` bằng nhau 100%.

2. **Per-chunk assertions cho Bún bò Mệ Kéo:**
   - Bỏ hoàn toàn việc nối text đa chunk.
   - Chọn exact chunk cho mệnh đề bún không có thịt bò (`heading_path == ["Món ăn / trải nghiệm"]` và chứa `"không có thịt bò"`): kiểm tra trực tiếp trên `search_text` và `evidence_parts[0].text`, kiểm tra slice `doc.lf_text[start:end]`.
   - Chọn exact chunk cho thành phần nguyên liệu (`heading_path == ["Món ăn / trải nghiệm"]` và chứa `"thịt ba chỉ, chả cua, huyết heo"`): kiểm tra trực tiếp trên `search_text` và `evidence_parts[0].text`, kiểm tra slice `doc.lf_text[start:end]`.
   - Khẳng định 2 mệnh đề này thuộc 2 chunk hoàn toàn riêng biệt (`ch_no_beef.chunk_id != ch_ingr.chunk_id`).

3. **Per-chunk assertions cho Hội xuân Gia Lạc:**
   - Bỏ hoàn toàn việc nối text đa chunk.
   - Chọn exact chunk cho không gian lịch sử dưới `Không gian tổ chức` (chứa `"Không gian lịch sử"` và `"ngã ba làng Nam Phổ"`).
   - Chọn exact chunk cho không gian phục dựng đương đại dưới `Không gian tổ chức` (chứa `"Không gian tái hiện đương đại"`, `"ngã ba Chợ Mai"`, và `"Nguyễn Đình Tứ"`).
   - Khẳng định rõ ràng không gian lịch sử và không gian phục dựng đương đại là 2 chunk độc lập với ID khác nhau (`ch_hist.chunk_id != ch_contemp.chunk_id`).
   - Chọn exact chunk cho tính chất phi thương mại dưới `Thông tin chung` (chứa cả hai yếu tố `"không mang tính thương mại đơn thuần"` và `"cầu may"`).
   - Kiểm tra mọi evidence part là exact source slice `doc.lf_text[start:end]`.

---

## 3. Cách đã chạy thật

Mọi lệnh được thực thi trực tiếp từ thư mục gốc `/home/minhhieu/hue_rag`:

### 3.1. Chạy bộ Wave 1 test suites (Correction 3 exact command)
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction3-uv-cache uv run python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_markdown_chunker.py -q --tb=short
```
- **Exit code:** `0`
- **Thời gian chạy:** `92.77s (0:01:32)`
- **Kết quả:** `39 passed, 1 warning` (24 tests `test_full_corpus_chunker.py` + 15 tests `test_markdown_chunker.py`).
- **Stdout:**
  ```
  .......................................                                  [100%]
  =============================== warnings summary ===============================
  backend/tests/test_full_corpus_chunker.py::test_full_corpus_discovery_and_inventory_exclusions
    /home/minhhieu/hue_rag/.venv/lib/python3.13/site-packages/qdrant_client/qdrant_remote.py:290: UserWarning: Failed to obtain server version. Unable to check client-server compatibility. Set check_compatibility=False to skip version check.
      show_warning(

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  39 passed, 1 warning in 92.77s (0:01:32)
  ```

### 3.2. Sinh preview artifact kiểm chứng theo hợp đồng Correction 3
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction3-uv-cache uv run python -m backend.ingestion.preview --output /tmp/full_corpus_rag_wave_1_preview_correction3.json
```
- **Exit code:** `0`
- **Stdout thực tế (nguyên văn):**
  ```
  Generating full-corpus Wave 1 preview to: /tmp/full_corpus_rag_wave_1_preview_correction3.json
  [transformers] Token indices sequence length is longer than the specified maximum sequence length for this model (265 > 256). Running this sequence through the model will result in indexing errors
  [transformers] Token indices sequence length is longer than the specified maximum sequence length for this model (598 > 512). Running this sequence through the model will result in indexing errors
  Status: PASS
  Total files: 205
  Total chunks: 8460
  Blocking errors: 0
  Oversized groups: 0

  Preview PASS with zero blocking errors. Exiting with code 0.
  ```

### 3.3. So sánh byte-by-byte giữa canonical preview artifact và preview Correction 3
```bash
cmp reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json /tmp/full_corpus_rag_wave_1_preview_correction3.json
```
- **Exit code:** `0`
- **Stdout:** (trống — hai file hoàn toàn giống nhau từng byte).

### 3.4. Kiểm tra khoảng trắng git
```bash
git diff --check
```
- **Exit code:** `0`
- **Stdout:** (trống — không có lỗi cú pháp hoặc khoảng trắng).

### 3.5. Các lệnh KHÔNG CHẠY (Not Run)
- `uv run python -m pytest backend/tests`: **NOT RUN** (Hợp đồng Correction 3 §Acceptance quy định không chạy vì toàn bộ backend suite chứa các bài test của Phase trước phụ thuộc dịch vụ Qdrant daemon và external API keys).
- `uv run python -m pytest backend/tests/test_ingestion_pipeline.py`: **NOT RUN** (Hợp đồng Correction 3 §Acceptance quy định không chạy vì là live suite tương tác trực tiếp với Qdrant daemon).

---

## 4. Kết quả quan sát

### 4.1. Số liệu trích xuất từ canonical preview artifact
Dữ liệu đọc trực tiếp từ `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`:
- **status:** `"PASS"`
- **summary:**
  - `total_files`: 205
  - `total_chunks`: 8460
  - `condition_rules_count`: 3
  - `blocking_errors_count`: 0
  - `oversized_groups_count`: 0
- **domain_breakdown (5 domains):**
  - `festivals`: 27 files, 1.130 chunks
  - `foods`: 91 files, 1.670 chunks
  - `heritages`: 29 files, 1.614 chunks
  - `performing_arts`: 13 files, 724 chunks
  - `travel`: 45 files, 3.322 chunks
  - *(Tổng: 205 files, 8.460 chunks)*
- **p7_breakdown (7 partitions):**
  - `foods`: 91 files, 1.670 chunks
  - `heritages`: 29 files, 1.614 chunks
  - `festivals`: 27 files, 1.130 chunks
  - `performing_arts`: 13 files, 724 chunks
  - `travel_places`: 36 files, 2.718 chunks
  - `travel_services`: 4 files, 147 chunks
  - `travel_tickets`: 5 files, 457 chunks
  - *(Tổng: 205 files, 8.460 chunks)*
- **tokenizer_limits (max observed vs limits):**
  - `intfloat/multilingual-e5-small`: trần 512, quan sát tối đa **366** (PASS)
  - `intfloat/multilingual-e5-base`: trần 512, quan sát tối đa **366** (PASS)
  - `CODE4LIFEOFFICIAL/huydang-dek21-embedding`: trần 256, quan sát tối đa **255** (PASS)

### 4.2. Danh mục 24 hàm kiểm thử trong `backend/tests/test_full_corpus_chunker.py`
1. `test_full_corpus_discovery_and_inventory_exclusions`: 205 files, 5 domains, 7 P7 partitions, inventory và exclude_parts exclusions.
2. `test_lf_normalization_and_hash`: Chuẩn hóa CRLF/CR thành LF và kiểm tra tính toàn vẹn hash.
3. `test_unicode_code_point_offsets_and_repeated_text_locator`: Zero-based code point offsets và định vị chuỗi lặp lại tại các vị trí không giao nhau.
4. `test_markdown_blocks_h1_intro_and_exclusions`: H1 title, intro trước H2 có heading_path rỗng, loại trừ ảnh/separator/Nguồn dữ liệu.
5. `test_markdown_blocks_blockquote_and_exclusions`: Bóc tách blockquote theo heading, exact source slice và loại trừ separator/image.
6. `test_markdown_blocks_table_and_nested_list_extraction`: Trích xuất bảng bằng token state `in_tbody` và nested list parent label.
7. `test_condition_manager_schema_validation`: Fail-closed khi selector thiếu trường hoặc sai kiểu dữ liệu.
8. `test_condition_manager_corpus_validation_and_attachment`: Đối chiếu 3 rules canonical trên 205 tệp và các tình huống lỗi selector.
9. `test_tokenizer_checker_settings_switch`: Kiểm tra chuyển đổi cấu hình checker trong cùng process không bị reuse cache sai.
10. `test_oversized_paragraph_sentence_boundary_split`: Tách đoạn văn dài tại ranh giới câu nguồn không cắt lưng chừng.
11. `test_oversized_table_row_split_preserves_header_and_condition`: Tách bảng theo dòng giữ nguyên header và attached condition trên mỗi sub-chunk.
12. `test_oversized_nested_list_split_preserves_parent_and_sub_items`: Tách nested list giữ nguyên nhãn cha trên mỗi sub-chunk.
13. `test_sentence_boundary_splitting_preserves_label_and_exact_spans`: Tách câu và lặp lại leading bold label dạng header cho bullet item.
14. `test_acceptance_sample_me_keo`: Kiểm tra Bún bò Mệ Kéo với các chunks riêng biệt cho địa chỉ, giá, giờ, mệnh đề không thịt bò và nguyên liệu.
15. `test_acceptance_sample_gia_lac`: Kiểm tra Hội xuân Gia Lạc chứng minh không gian lịch sử và phục dựng đương đại là 2 chunks độc lập, và chunk tính chất phi thương mại.
16. `test_acceptance_sample_dai_noi`: Kiểm tra Đại Nội Huế bảo toàn cấu trúc Ngọ Môn và quan hệ của cả 5 cửa.
17. `test_acceptance_sample_lich_trinh_3n2d`: Kiểm tra Lịch trình 3N2Đ bảo toàn cấu trúc từng ngày.
18. `test_acceptance_sample_ca_hue_performing_art`: Kiểm tra Ca Huế trên sông Hương bảo toàn dàn ngũ tuyệt cổ điển và bộ gõ.
19. `test_acceptance_sample_ca_hue_tickets_and_conditions`: Kiểm tra vé Ca Huế gắn đúng điều kiện cho Bảng A và Bảng B.
20. `test_acceptance_sample_chi_phi_du_lich`: Kiểm tra Chi phí du lịch Huế gắn đúng điều kiện hạn mức kế hoạch cho 3 bảng dự toán.
21. `test_synthetic_oversized_group_blocking`: Kiểm tra đơn vị vượt trần token gây chặn preview (`status: BLOCKED_OVERSIZED_GROUP`, exit 1).
22. `test_generic_condition_or_parser_error_blocks_preview`: Kiểm tra lỗi condition gây chặn preview (`status: BLOCKED_ERRORS`, exit 1).
23. `test_canonical_preview_pass`: Kiểm tra canonical preview artifact tự nhất quán về số lượng tệp, chunks, breakdowns và trần token.
24. `test_full_corpus_determinism_and_preview_byte_equality`: Kiểm tra deep-equality giữa 2 lần chunk full corpus, tính duy nhất và UUID5 của point_id, 100% evidence slicing, và so sánh byte-identical giữa 2 preview artifacts.

---

## 5. Giới hạn và phân định trạng thái

1. **Giới hạn môi trường Offline:**
   - Dịch vụ Qdrant daemon không khởi chạy trong phiên làm việc này; các suite kiểm thử liên quan đến live vectorstore hoặc live inference API đã được xác định nằm ngoài phạm vi Wave 1 offline và không được thực thi.
   - Toàn bộ 39 unit và regression tests của Wave 1 chạy hoàn toàn offline độc lập và đạt tỷ lệ đỗ 100%.

2. **Phân định trạng thái Worktree:**
   - **Tệp thay đổi và tạo mới thuộc Wave 1:** Đã liệt kê chi tiết tại mục 2.1.
   - **Tệp pre-existing được giữ nguyên vẹn:** Toàn bộ raw corpus dưới `knowledge-base-hue/`, toàn bộ golden reference datasets và các tài liệu hướng dẫn (guides) lịch sử.

---

## 6. Handoff cho Reviewer

### 6.1. Tài liệu và mã nguồn cần đọc
1. `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md` (báo cáo này).
2. `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` (canonical preview artifact).
3. Hợp đồng điều khiển:
   - `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_3_PROMPT.md`
   - `reports/full_corpus_rag_wave_1_correction_2_codex_review_2026_09_12.md`
4. Bộ kiểm thử:
   - `backend/tests/test_full_corpus_chunker.py`

### 6.2. Các lệnh kiểm chứng tĩnh và động (theo Correction 3 contract)
```bash
# 1. Chạy bộ Wave 1 test suite
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction3-uv-cache uv run python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_markdown_chunker.py -q --tb=short

# 2. Sinh preview artifact kiểm chứng
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-full-corpus-wave1-correction3-uv-cache uv run python -m backend.ingestion.preview --output /tmp/full_corpus_rag_wave_1_preview_correction3.json

# 3. So sánh byte-identical giữa canonical artifact và preview Correction 3
cmp reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json /tmp/full_corpus_rag_wave_1_preview_correction3.json

# 4. Kiểm tra khoảng trắng git
git diff --check
```

### 6.3. Bàn giao đánh giá
Implementer đã hoàn tất đầy đủ các yêu cầu kỹ thuật của Correction 3 và chuyển giao toàn bộ kết quả kiểm chứng cho Reviewer tiến hành nghiệm thu theo thẩm quyền quy định tại Review Contract.
