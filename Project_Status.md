# Project Status

Last updated: `2026-08-09 08:54 +07`

## Mục tiêu dự án

- RAG Chatbot về văn hóa và du lịch Huế.
- Agentic RAG.
- Hybrid Recommender + LLM cho trải nghiệm du lịch và văn hóa Huế.

## Pipeline dữ liệu

```text
raw -> Markdown source dumps -> curated Markdown -> enrichment có nguồn xác minh -> chunks -> embeddings/index
```

Không chunk trực tiếp từ `_source-dumps` nếu chưa curate.

## Nguồn và cấu trúc chính

- Raw Department of Tourism: `backend/data/huegov_department_of_tourism/raw`
- Raw Culture and Tourism: `backend/data/huegov_culture_and_tourism/raw`
- Source dumps: `knowledge-base-hue/_source-dumps/`
- Curated knowledge base: `knowledge-base-hue/`
- Foods template: `knowledge-base-hue/meta/foods-template.md`
- Food guides spec: `knowledge-base-hue/meta/food-guides-spec.md`
- Evaluation foods: `knowledge-base-hue/foods/evaluation/` (`tests.jsonl` + `validate_tests.py`)
- Hue Foods RAG MVP design: `docs/superpowers/specs/2026-08-08-hue-foods-rag-mvp-design.md`
- Hue Foods RAG MVP implementation plan: `docs/superpowers/plans/2026-08-08-hue-foods-rag-mvp-plan.md`
- Hue Foods RAG benchmark log: `docs/superpowers/plans/2026-08-08-hue-foods-rag-benchmark-log.md`
- Shared session prompt: `Session_Prompt.md`
- Reviewer workflow: `REVIEWER_WORKFLOW.md`
- Implementer workflow: `IMPLEMENTER_WORKFLOW.md`
- Implementation report template: `TEMPLATE_IMPLEMENTATION_REPORT.md`
- Codex review template: `TEMPLATE_CODEX_REVIEW.md`

## Trạng thái foods

- `restaurants/`: 57 file curated.
- `cafes/`: 24 file curated (thêm `quan ca phe muoi.md`).
- `local_specialties/`: 9 file curated: `bun bo hue.md`, `com hen.md`, `com am phu.md`, `banh ep.md`, `me xung.md`, `che heo quay.md`, `banh canh nam pho.md`, `banh nam.md` và `ca phe muoi.md`.
- `food-guides.md`: đã hoàn thiện với 17 sections, tổng hợp từ dữ liệu curated và 4 bài Cẩm nang AEON MALL Huế cập nhật 2026.
- `evaluation/`: bộ test đánh giá RAG foods gồm `tests.jsonl` (104 câu, schema TestQuestion cũ: question / keywords / reference_answer / category, 8 category) và `validate_tests.py` (script kiểm tra chất lượng bộ test, chạy bằng uv).

Chuẩn curated cốt lõi: không YAML frontmatter, file bắt đầu bằng `#`, chỉ ghi dữ liệu có nguồn, source tracking ở `## Nguồn dữ liệu`, không thêm `Liên kết nội bộ` vào body. Riêng `food-guides.md` là guide tổng hợp và không bắt buộc có `## Nguồn dữ liệu`. Tên file trong `restaurants/` và `cafes/` đã được chuẩn hóa bằng cách thay dấu gạch bằng khoảng trắng.

9 món hoặc nhóm món đặc sản đã curate:

- Bún bò Huế
- Cơm hến
- Cơm âm phủ
- Bánh nậm
- Chè heo quay
- Bánh ép
- Mè xửng
- Bánh canh Nam Phổ
- Cà phê muối

## Trạng thái evaluation foods

- Bộ test `knowledge-base-hue/foods/evaluation/tests.jsonl`: 104 câu, tiếng Việt có dấu, không câu hỏi về giá, không câu bẫy.
- Schema giữ nguyên của khóa học: question / keywords / reference_answer / category.
- Category: 7 category cũ (direct_fact, temporal, comparative, numerical, relationship, spanning, holistic) + 2 mới (food_knowledge, guide_planning); bộ test hiện dùng 8 category (không numerical).
- Phân bố: direct_fact 21, relationship 16, spanning 17, guide_planning 13, holistic 11, temporal 10, food_knowledge 10, comparative 6.
- Keywords: 1-5 từ, trích nguyên văn từ KB, viết hoa tên riêng (case-insensitive matching nên không ảnh hưởng), không generic; câu hỏi chủ đề mở (holistic/guide_planning) dùng keyword chủ đề, không gắn quán cụ thể.
- Reference answer: 1-2 câu, chứa toàn bộ keywords của test, ≤ 850 ký tự (tour 3 ngày là exception).
- `validate_tests.py`: kiểm tra JSON hợp lệ, category hợp lệ, question duy nhất, keyword không generic, keyword tồn tại trong KB và trong reference answer. Chạy: `UV_CACHE_DIR=/tmp/uv-cache uv run python knowledge-base-hue/foods/evaluation/validate_tests.py`.

## Trạng thái triển khai

Đã hoàn thành:

- Khảo sát raw data và source dumps của hai nguồn HueGov.
- Tạo source dumps, README ghi chú chuyển đổi và taxonomy folders.
- Chốt template/chuẩn curated cho `foods`.
- Curate 57 restaurants và 24 cafes từ dữ liệu người dùng cung cấp.
- Cập nhật chuẩn `foods-template.md` cho `local_specialties` và exception của `food-guides.md`.
- Tạo spec/plan cho `food-guides.md` tại `knowledge-base-hue/meta/food-guides-spec.md`.
- Curate 9 món đặc sản trong `local_specialties/`, gồm `ca phe muoi.md` (thêm `quan ca phe muoi.md` vào `cafes/` và cập nhật bảng Địa điểm tiêu biểu).
- Hoàn thiện `foods/food-guides.md` (17 sections) và cập nhật `meta/food-guides-spec.md`.
- Thiết kế và tạo bộ test đánh giá foods: `foods/evaluation/tests.jsonl` (104 câu, 8 category) + `foods/evaluation/validate_tests.py`, dựa trên thiết kế evaluation của khóa học cũ (`rag_old/evaluation/`), có research đối chiếu 5 bài Cẩm nang AEON MALL Huế 2026 (giữ dữ liệu theo KB curated).
- Brainstorm và tài liệu hóa thiết kế Hue Foods RAG MVP dựa trên `llm_rag` và `rag_old`: backend modular trong `backend/`, notebooks học tập trong `notebooks/`, Qdrant hybrid, config profiles (`dense_only`, `hybrid_no_rerank`, `hybrid_rerank`), Semantic Markdown section chunking, SentenceTransformer local, OpenAI/Agents SDK, JSON API, retrieval + answer evaluation và benchmark log.
- Tách governance workflow: `Session_Prompt.md` là shared base context + role routing; `REVIEWER_WORKFLOW.md` dành cho Codex reviewer/gatekeeper; `IMPLEMENTER_WORKFLOW.md` dành cho DeepSeek implementer; thêm `TEMPLATE_IMPLEMENTATION_REPORT.md` và `TEMPLATE_CODEX_REVIEW.md`; reports phase nằm trong `/home/hieu0606sunny/hue_rag/reports/`.
- Approve Phase 1 Hue Foods RAG MVP: backend skeleton và central configuration đã tạo trong `backend/`, gồm `settings.yaml`, `logging.yaml`, `settings_loader.py`, `logging_setup.py`, `schema.py` và package markers theo approved design.

Chưa thực hiện:

- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Implement các phase còn lại của Hue Foods RAG MVP runtime: foods Markdown chunking, embedding, Qdrant ingestion, retrieval profiles, reranking, OpenAI generation, API, notebooks và evaluator thật.
- Enrichment có nguồn xác minh; recommender; Agentic RAG sau MVP.
- Chạy bộ test trên evaluator thật (retrieval MRR/nDCG + LLM-judge) sau khi có pipeline RAG foods.

## Cập nhật gần nhất

### 2026-08-09 08:54 +07

- Thay đổi: Cập nhật governance report path theo yêu cầu user. Implementation reports và Codex review reports hiện phải viết trong thư mục gốc `/home/hieu0606sunny/hue_rag/reports/`, với naming `reports/phase_<id>_<short_name>_implementation_report.md` và `reports/phase_<id>_<short_name>_codex_review.md`.
- File chính: `Session_Prompt.md`, `REVIEWER_WORKFLOW.md`, `IMPLEMENTER_WORKFLOW.md`, `TEMPLATE_IMPLEMENTATION_REPORT.md`, `TEMPLATE_CODEX_REVIEW.md`, `Project_Status.md`, `reports/phase_1_backend_skeleton_codex_review.md`.
- Validation: `rg` không còn reference đường dẫn reports cũ trong các file Markdown; `git diff --check` sạch cho các file governance/report đã sửa.
- Next action: Các phase report tiếp theo của DeepSeek và Codex dùng `reports/` ở repo root.

### 2026-08-09 08:48 +07

- Thay đổi: Codex review Phase 1 Backend Skeleton và approve gate. Phase 1 tạo backend package skeleton, central settings loader, logging setup, shared `RetrievedDocument` schema, config profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`, và config docs. Không có blocker hoặc major findings; các giới hạn được chấp nhận là verify OpenAI model IDs trước Phase 6, kiểm Qdrant/Docker ở Phase 4, và defer env overrides đến phase cần secrets/config runtime.
- File chính: `backend/config/settings.yaml`, `backend/config/logging.yaml`, `backend/config/README_config.md`, `backend/core/settings_loader.py`, `backend/core/logging_setup.py`, `backend/core/schema.py`, package markers trong `backend/`, `reports/phase_1_backend_skeleton_implementation_report.md`, `reports/phase_1_backend_skeleton_codex_review.md`.
- Validation: `load_settings()` trả `dense_only`; `py_compile` sạch cho 3 core module; cả 3 profile resolve đúng mode/BM25/rerank flags; invalid profile raise `ValueError` có danh sách profile hợp lệ; logging smoke test ghi console + `backend/logs/application.log` và đã xóa log residue; scope/security scan không thấy secrets.
- Next action: Có thể chuyển sang Phase 2 Foods Markdown discovery and chunking. Logic này ổn định; nên commit approved unit trước khi đi tiếp nếu user đồng ý.

### 2026-08-08 22:57 +07

- Thay đổi: Cập nhật governance workflow cho repo. `Session_Prompt.md` được rút gọn thành shared base context + role routing; tạo `REVIEWER_WORKFLOW.md` cho Codex reviewer/gatekeeper, `IMPLEMENTER_WORKFLOW.md` cho DeepSeek implementer, `TEMPLATE_IMPLEMENTATION_REPORT.md` và `TEMPLATE_CODEX_REVIEW.md`. Quy ước chính: Codex review/approve/update status; DeepSeek implement/write report; reports phase nằm trong `/home/hieu0606sunny/hue_rag/reports/`; notebooks bắt buộc khi phase plan yêu cầu và phải để outputs rỗng; live model/API calls mặc định không chạy nếu user chưa approve rõ; CodeGraph hiện là future/optional.
- File chính: `Session_Prompt.md`, `REVIEWER_WORKFLOW.md`, `IMPLEMENTER_WORKFLOW.md`, `TEMPLATE_IMPLEMENTATION_REPORT.md`, `TEMPLATE_CODEX_REVIEW.md`, `Project_Status.md`, cùng 3 file Hue Foods RAG MVP docs đã tạo trước đó trong `docs/superpowers/`.
- Validation: kiểm tra workflow files không còn sót tên dự án mẫu; placeholder scan không có kết quả; `git diff --check` sạch cho workflow/status/docs; chưa implement code runtime.
- Next action: Commit và push approved governance + RAG MVP planning docs theo yêu cầu của user; sau đó user có thể gửi `Session_Prompt.md` + workflow tương ứng cho Codex reviewer hoặc DeepSeek implementer.
