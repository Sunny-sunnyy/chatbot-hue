# Phase 2 Foods Markdown Chunking Simplicity Review

Date: `2026-08-24 +07`

Status: `Approved by user`

## 1. Before state

Phase 2 đọc 91 curated foods Markdown files và tạo 572 ordered chunks. Runtime
trải trên bốn modules: chunk orchestration, parser, metadata helper và text
splitter. Permanent test file có 31 tests, gồm nhiều checks lặp trên corpus.
Notebook 02 import private runtime helpers để dựng phần trình bày.

## 2. Capability được giữ

- Sorted discovery đúng curated foods scope.
- H1 title, H2 semantic sections và H3 nằm trong H2 body.
- Image-only lines và `Nguồn dữ liệu` bị loại.
- 400-character body target, natural boundaries và atomic Markdown tables.
- Deterministic context labels, ordered chunks, seven metadata fields và stable
  `chunk_id`.
- Public boundary `chunk_foods_markdown()` cho Phase 3–7.

## 3. Thay đổi đã duyệt

- Đưa parsing, minimal validation và metadata construction vào
  `markdown_chunker.py`.
- Giữ `split_text.py` làm helper duy nhất.
- Xóa parser/metadata wrappers không có consumer độc lập.
- Giảm test về distinct durable behaviors, không khóa corpus count lâu dài.
- Notebook 02 chỉ dùng public API và ba ví dụ trực quan.

## 4. After state

Runtime còn hai modules và data flow đi trực tiếp từ settings/discovery qua
parse, cleanup, split, label/metadata rồi corpus invariants. Malformed file
thiếu H1 hoặc không còn answer-facing H2 sau cleanup ném `ValueError` rõ ràng.

Focused suite có 15 tests. Đây là số quan sát hiện tại, không phải target. Hai
helper cũ không còn file/import/wrapper. Notebook repo sạch và Run All được
trên corpus thật.

## 5. Before/After comparison

| Area | Before | After |
|---|---|---|
| Runtime modules | Chunker + parser + metadata + splitter | Chunker + splitter |
| Public API | `chunk_foods_markdown()` | Không đổi |
| Ordered corpus | 572 chunks | Khớp tuyệt đối cả text/metadata/order |
| Permanent tests | 31, có checks lặp | 15 distinct behavior tests |
| Corpus counts | Nằm trong test | Chỉ là acceptance/notebook evidence |
| Notebook | Dùng private helpers | Chỉ dùng public chunker |

## 6. Downstream impact

| Phase | Dependency | Observed evidence | Impact | Later action | Blocks? |
|---:|---|---|---|---|---:|
| 3–7 | Ordered chunks và seven-field metadata | Exact equality; 79 downstream và 206 full tests pass | Không quan sát regression | Không cần Phase 7 quality rerun | Không |

## 7. Verification

- Ordered Before/After equality: 572/572 chunks, cùng SHA-256
  `936063a91a69083fe7070096da17656920cff3b93917a3e6fcc4384d697c8fde`.
- Focused Phase 2: 15 passed trước và sau full suite.
- Notebook 02: Run All thật; 572 chunks, 91 files, ba examples.
- Downstream smoke: 79 passed, 3 warnings.
- Full backend: 206 passed, 4 warnings.
- Active Qdrant: 572 points trước và sau, read-only.
- Final `git diff --check`: sạch.

## 8. Bugs và cách xử lý

Review round 1 phát hiện validation tính raw image-only H2 là answer-facing.
Correction chuyển check sang body sau cleanup và thêm focused regression test.

Full backend tests có side effect đổi retrieval CSV sang CRLF. Nội dung không
đổi; Implementer và Reviewer đều hoàn nguyên line endings sau run. Fix test
side effect thuộc Phase 7 ownership, không mở rộng runtime Phase 2.

## 9. Giới hạn

- Không chạy Phase 7 evaluation vì ordered corpus hoàn toàn không đổi.
- Hai minor không ảnh hưởng behavior: một unused `Path` import và typo trong
  synthetic test fixture.
- User đã xác nhận Phase 2 ngày `2026-08-24 +07`; phase hiện `approved`.
