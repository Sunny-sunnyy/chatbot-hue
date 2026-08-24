# Implementation Report: Phase 2 Foods Markdown Chunking Simplicity Review

Implementer: Antigravity
Date: 2026-08-24 +07 (Correction round 1)
Canonical guide:

```text
guides/phase_2_foods_markdown_chunking.md
```

Approved design & plan:

```text
docs/superpowers/specs/2026-08-24-phase-2-foods-markdown-chunking-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-2-foods-markdown-chunking-simplicity-implementation.md
```

Codex review:

```text
reports/phase_2_foods_markdown_chunking_simplicity_codex_review.md
```

## 1. Phạm vi

Thực hiện đầy đủ kế hoạch triển khai và hoàn tất toàn bộ correction scope theo yêu cầu của Reviewer tại vòng review 1:
- Tinh giản kiến trúc runtime từ 4 module xuống 2 module trực tiếp (`markdown_chunker.py` và `split_text.py`).
- Chuyển logic parsing Markdown, fail-fast validation tối thiểu và metadata construction trực tiếp vào `markdown_chunker.py`.
- Sửa fail-fast validation: tính `has_answer_h2` sau khi đã lọc bỏ image-only lines qua `_clean_body()`, bảo đảm file chỉ có H2 chứa ảnh và mục nguồn sẽ ném `ValueError` thay vì trả `[]`.
- Xóa bỏ 2 helper modules nội bộ `markdown_parser.py` và `make_metadata.py` mà không để lại wrapper hay compatibility layer.
- Giữ nguyên thuật toán chia tách và boundary logic trong `split_text.py`.
- Tinh gọn test suite `test_markdown_chunker.py`: loại bỏ hard-coded `572`/`91` khỏi permanent test; kiểm tra toàn bộ output equality trong deterministic test; bổ sung regression test cho file chỉ có image H2; dọn sạch import `Path` và helper `_content_of()` không dùng.
- Hoàn nguyên line-ending diff của `backend/evaluation/retrieval_results.csv` sau khi chạy full backend suite để giữ worktree sạch.
- Tinh giản `notebooks/02_foods_data_and_chunking.ipynb` chỉ sử dụng public API `chunk_foods_markdown()`, loại bỏ toàn bộ private imports và helpers nội bộ.
- Không thay đổi curated Markdown, settings, context labels, chunk boundaries, metadata schema 7 fields, deterministic IDs hay thứ tự discovery.
- Không mutate active Qdrant collection `hue_foods_e5_small_384`.
- Bảo toàn nguyên vẹn toàn bộ thay đổi không liên quan trong worktree.

## 2. Thay đổi chính

- **`backend/ingestion/chunking/markdown_chunker.py`**:
  - Tích hợp `_parse_markdown(text)` trực tiếp vào module (xử lý H1 làm title, H2 làm semantic section, giữ H3 trong section body, bỏ qua empty body).
  - Fail-fast validation cho từng file: bắt buộc có H1 (`ValueError`), bắt buộc có ít nhất một mục H2 phục vụ trả lời có nội dung văn bản sau khi lọc ảnh qua `_clean_body()` (`ValueError`), bảo đảm `source` là relative path dưới KB root.
  - Validation invariants cho output corpus trước khi return: kiểm tra text không rỗng, metadata chứa đúng 7 trường bắt buộc, và `chunk_id` là duy nhất trên toàn corpus.
  - Xây dựng metadata dict 7 fields tại chỗ, giữ nguyên context label rules và subcategory mapping.
- **`backend/ingestion/helpers/split_text.py`**:
  - Giữ nguyên toàn bộ logic tách đoạn văn, câu, danh sách, giữ nguyên khối bảng Markdown và giới hạn 400 ký tự.
- **`backend/ingestion/helpers/markdown_parser.py` & `backend/ingestion/helpers/make_metadata.py`**:
  - Đã xóa hoàn toàn 2 file này.
- **`backend/tests/test_markdown_chunker.py`**:
  - 15 test tập trung: 8 test cho các hành vi tách văn bản của `split_text`, 5 test unit cho parser/exclusion/fail-fast validation của chunker (bao gồm test fail-fast khi H2 chỉ chứa ảnh), và 2 test toàn diện cho corpus thật (durable invariants & tính deterministic kiểm tra toàn bộ output).
  - Đã xóa `Path` và `_content_of()`.
- **`notebooks/02_foods_data_and_chunking.ipynb`**:
  - Loại bỏ các import hàm private (`_discover_markdown_files`, `_is_table`, `_split_blocks`).
  - Chỉ gọi `chunk_foods_markdown()`, hiển thị 3 ví dụ trực quan (đoạn văn thường, bảng Markdown và food guide), làm sạch outputs và đặt `execution_count: null`.

## 3. Cách đã chạy thật

Tất cả các bước được chạy trên môi trường thật với Python 3.13 (`uv`), corpus 91 file curated foods Markdown thật, và local Qdrant v1.18.3:

1. **Khóa baseline Before ra ngoài repository**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'import hashlib, json; from pathlib import Path; from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); raw = json.dumps(chunks, ensure_ascii=False, sort_keys=True, separators=(",", ":")); path = Path("/tmp/hue-rag-phase2-before-20260824.json"); path.write_text(raw, encoding="utf-8"); print("chunks", len(chunks)); print("sha256", hashlib.sha256(raw.encode()).hexdigest()); print("path", path)'
   ```

2. **Biên dịch và kiểm tra focused tests**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m py_compile ingestion/chunking/markdown_chunker.py ingestion/helpers/split_text.py
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m pytest tests/test_markdown_chunker.py -q --tb=short
   ```

3. **Đối chiếu ordered corpus equivalence tuyệt đối**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'import hashlib, json; from pathlib import Path; from ingestion.chunking.markdown_chunker import chunk_foods_markdown; before = json.loads(Path("/tmp/hue-rag-phase2-before-20260824.json").read_text(encoding="utf-8")); after = chunk_foods_markdown(); assert len(before) == 572, len(before); assert len(after) == 572, len(after); assert before == after; raw = json.dumps(after, ensure_ascii=False, sort_keys=True, separators=(",", ":")); print("ordered_equal", True); print("chunks", len(after)); print("sha256", hashlib.sha256(raw.encode()).hexdigest())'
   ```

4. **Thực thi Notebook 02 trên bản sao tạm**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run jupyter nbconvert --execute --to notebook notebooks/02_foods_data_and_chunking.ipynb --output /tmp/02_foods_data_and_chunking-phase2-review.ipynb --ExecutePreprocessor.timeout=600
   ```

5. **Kiểm tra tính an toàn và sạch sẽ của Notebook 02 repository**:
   ```bash
   jq -e 'all(.cells[] | select(.cell_type == "code"); .execution_count == null and (.outputs | length == 0))' notebooks/02_foods_data_and_chunking.ipynb
   grep -rnE '/home/|API_KEY|OPENAI_API_KEY|OPENROUTER_API_KEY|_discover_markdown_files|_is_table|_split_blocks' notebooks/02_foods_data_and_chunking.ipynb
   ```

6. **Kiểm tra active Qdrant collection read-only**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s = load_settings(); c = client_from_settings(s); n = s["vector_database"]["collection_name"]; print("active_collection", n, "points", c.count(n, exact=True).count)'
   ```

7. **Kiểm tra downstream smoke tests**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run --env-file ../.env python -m pytest tests/test_ingestion_pipeline.py tests/test_hybrid_index.py tests/test_startup.py tests/test_api_chat.py -q --tb=short
   ```

8. **Kiểm tra toàn bộ test suite backend**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
   ```

9. **Hoàn nguyên line endings file CSV evaluation**:
   ```bash
   git checkout -- backend/evaluation/retrieval_results.csv
   git diff --check
   ```

## 4. Kết quả quan sát

- **Ordered corpus equivalence**:
  - Baseline path: `/tmp/hue-rag-phase2-before-20260824.json`
  - Before SHA-256: `936063a91a69083fe7070096da17656920cff3b93917a3e6fcc4384d697c8fde`
  - After SHA-256: `936063a91a69083fe7070096da17656920cff3b93917a3e6fcc4384d697c8fde`
  - Kết quả: `ordered_equal True`, `chunks 572` (khớp tuyệt đối 100% về thứ tự, `text` và toàn bộ 7 trường metadata).
- **Focused test suite**:
  - `15 passed in 0.17s` (toàn bộ 15 test đều đạt, bao gồm regression test `test_chunk_file_fails_fast_on_image_only_answer_h2`).
- **Notebook 02 execution**:
  - Thực thi thành công qua `nbconvert` mà không phát sinh lỗi.
  - Hiển thị đúng 572 đoạn từ 91 file, phân bổ: `cafes: 162`, `guide: 43`, `local_specialties: 118`, `restaurants: 249`.
  - Hiển thị trực quan 3 ví dụ (đoạn văn thường, bảng menu cà phê muối, gợi ý ẩm thực food guide).
  - Notebook repository cam kết sạch: `execution_count == null`, `outputs == []`, không chứa secret hay đường dẫn cá nhân.
- **Active Qdrant collection**:
  - `active_collection hue_foods_e5_small_384 points 572` (hoàn toàn không bị mutate).
- **Downstream smoke suite**:
  - `79 passed, 3 warnings in 221.33s`.
- **Full backend suite**:
  - `206 passed, 4 warnings in 243.25s` (toàn bộ 206 test backend đều đạt).
- **Worktree hygiene**:
  - `git diff --check` thoát mã 0 (sạch hoàn toàn, không có whitespace lỗi hay line-ending diff thừa).

## 5. Bảng ảnh hưởng Downstream và giới hạn

### Bảng ảnh hưởng Downstream

| Affected Phase | Dependency | Observed Evidence | Concrete Impact | Later Action | Blocks Approval? |
|---|---|---|---|---|---|
| Phase 3–7 | `chunk_foods_markdown()` contract & 7 metadata fields | `ordered_equal True`, `sha256` trùng khớp tuyệt đối, downstream smoke 79/79 passed, full backend 206/206 passed | Không có bất kỳ sai lệch nào đối với embedding, indexing, retrieval, context builder hay chat API | Giữ nguyên downstream verification | Không (No) |
| None | Downstream warnings | 3 deprecation/compatibility warnings từ thư viện bên thứ 3 (`fastapi.testclient` / `starlette`, `qdrant_client` remote version check) | Cảnh báo có sẵn từ trước, không ảnh hưởng logic | Xem xét trong review Phase tương ứng | Không (No) |

Không quan sát thấy bất kỳ regression mới nào do Phase 2 gây ra.

### Lỗi và giới hạn đã biết

- Không có lỗi hoặc giới hạn đã biết trong phạm vi Phase 2 này.
- Qdrant container chạy local qua `docker-compose.yml` (`v1.18.3`, port 6333); active collection `hue_foods_e5_small_384` được giữ read-only ở đúng 572 points.

## 6. Handoff cho Reviewer

Reviewer nên thực hiện audit độc lập theo các bước:

1. **Kiểm tra git diff và deleted files**:
   ```bash
   git diff --stat -- backend/ingestion/chunking/markdown_chunker.py backend/ingestion/helpers/markdown_parser.py backend/ingestion/helpers/make_metadata.py backend/ingestion/helpers/split_text.py backend/tests/test_markdown_chunker.py notebooks/02_foods_data_and_chunking.ipynb
   test ! -e backend/ingestion/helpers/markdown_parser.py && test ! -e backend/ingestion/helpers/make_metadata.py
   git diff --check
   ```

2. **Chạy lại kiểm chứng ordered equality 572 chunks**:
   ```bash
   cd backend
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'import hashlib, json; from pathlib import Path; from ingestion.chunking.markdown_chunker import chunk_foods_markdown; before = json.loads(Path("/tmp/hue-rag-phase2-before-20260824.json").read_text(encoding="utf-8")); after = chunk_foods_markdown(); assert len(before) == 572; assert len(after) == 572; assert before == after; raw = json.dumps(after, ensure_ascii=False, sort_keys=True, separators=(",", ":")); print("ordered_equal", True); print("chunks", len(after)); print("sha256", hashlib.sha256(raw.encode()).hexdigest())'
   ```

3. **Chạy bộ test focused Phase 2**:
   ```bash
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -m pytest tests/test_markdown_chunker.py -q --tb=short
   ```

4. **Chạy kiểm tra thực thi và độ sạch của Notebook 02**:
   ```bash
   cd ..
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run jupyter nbconvert --execute --to notebook notebooks/02_foods_data_and_chunking.ipynb --output /tmp/02_foods_data_and_chunking-phase2-review.ipynb --ExecutePreprocessor.timeout=600
   jq -e 'all(.cells[] | select(.cell_type == "code"); .execution_count == null and (.outputs | length == 0))' notebooks/02_foods_data_and_chunking.ipynb
   ```

5. **Xác nhận số lượng điểm trong active Qdrant collection**:
   ```bash
   cd backend
   UV_CACHE_DIR=/tmp/hue-rag-phase2-uv-cache uv run python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s = load_settings(); c = client_from_settings(s); n = s["vector_database"]["collection_name"]; print("active_collection", n, "points", c.count(n, exact=True).count)'
   ```

Implementer không tự approve phase, không chỉnh sửa canonical guide, Codex review, user report hay `Project_Status.md`, và không commit/push.
