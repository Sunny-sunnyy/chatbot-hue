# Project Status

Last updated: `2026-08-09 12:42 +07`

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
- Phase guide index: `guides/README.md`
- Hue Foods RAG MVP foundation: `guides/phase_0_mvp_foundation.md`
- Detailed phase guides: `guides/phase_1_backend_skeleton.md` đến `guides/phase_9_agentic_rag_roadmap.md`
- Hue Foods RAG benchmark ledger: `reports/hue_foods_rag_benchmark.md`
- Shared session prompt: `session_prompt/Session_Prompt.md`
- Reviewer workflow: `session_prompt/REVIEWER_WORKFLOW.md`
- Implementer workflow: `session_prompt/IMPLEMENTER_WORKFLOW.md`
- Implementation report template: `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`
- Codex review template: `session_prompt/TEMPLATE_CODEX_REVIEW.md`
- User report template: `session_prompt/TEMPLATE_USER_REPORT.md`
- User-facing phase reports: `reports/user_reports/`

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
- Brainstorm và tài liệu hóa Phase 0–9 trong `guides/`: backend modular, semantic chunking, một active Qdrant collection, ba retrieval profiles, local `multilingual-e5-small`/MiniLM baseline trước OpenRouter, OpenAI Agents SDK generation/judge, controlled evaluation và post-MVP Agentic RAG hard gate.
- Tách governance workflow: `session_prompt/Session_Prompt.md` là shared base context + role routing; `session_prompt/REVIEWER_WORKFLOW.md` dành cho Codex reviewer/gatekeeper; `session_prompt/IMPLEMENTER_WORKFLOW.md` dành cho DeepSeek implementer; thêm `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md` và `session_prompt/TEMPLATE_CODEX_REVIEW.md`; reports phase nằm trong `/home/hieu0606sunny/hue_rag/reports/`.
- Technical review Phase 1 đã đạt theo contract cũ: backend skeleton và central configuration đã tạo trong `backend/`, gồm `settings.yaml`, `logging.yaml`, `settings_loader.py`, `logging_setup.py`, `schema.py` và package markers. Final user confirmation đang được mở lại theo governance mới.
- Technical review Phase 2 đã đạt theo contract cũ: foods Markdown discovery và semantic section chunking đã tạo 366 chunks từ 91 curated foods files, kèm unit tests và notebook hiện tại `notebooks/01_foods_data_and_chunking.ipynb`. Notebook đang chờ rename thành `notebooks/02_foods_data_and_chunking.ipynb` trước final user confirmation.
- Hoàn tất migration tài liệu điều hành: `guides/README.md`, 10 phase guides và `reports/hue_foods_rag_benchmark.md` thay thế ba spec/plan/benchmark documents cũ dưới `docs/superpowers/`; workflows, templates và Phase 1–2 report references đã được cập nhật.
- Chốt dual-report governance: technical reports trong `reports/` dành cho coding agents; user reports trong `reports/user_reports/` do Codex viết bằng tiếng Việt dễ hiểu; Phase 1–8 bắt buộc có notebook mang đúng số phase và chỉ `approved` sau user confirmation.

Chưa thực hiện:

- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Hoàn tất Phase 1 remediation notebook và Phase 2 notebook rename; Codex review rồi tạo hai user reports để người dùng xác nhận lại.
- Brainstorm và implement Phase 3–8 của Hue Foods RAG MVP theo guide; Phase 3 đang `not_ready` cho đến khi Phase 1–2 trở lại `approved`.
- Chạy local E5/MiniLM three-profile benchmark rồi mới thử OpenRouter; ledger hiện chưa có benchmark result hoặc winner.
- Enrichment có nguồn xác minh; recommender; Agentic RAG sau MVP.
- Chạy bộ test trên evaluator thật (retrieval MRR/nDCG + LLM-judge) sau khi có pipeline RAG foods.

## Cập nhật gần nhất

### 2026-08-09 12:42 +07

- Trạng thái: Dual-report và hard user-confirmation governance đã được người dùng phê duyệt. Phase 0 `completed`; Phase 1–2 `changes_requested` cho notebook/user-report retrofit nhưng giữ nguyên technical acceptance history; Phase 3–8 `not_ready`; Phase 9 `design_only`.
- File chính: `guides/README.md`, Phase 0–9 guides, `session_prompt/Session_Prompt.md`, hai role workflows, ba report templates và `reports/user_reports/README.md`. Reviewer tự bootstrap context, tạo user report và finalize; Implementer tự bootstrap context, tạo notebook/technical report và không sửa user report.
- Validation: status/index, notebook mapping Phase 1–8, workflow bootstrap, dual-report ownership, 17-section user-report template, Markdown structure, secret/placeholder scan, local references và Git scope đều được kiểm tra; `git diff --check` sạch. Governance patch không sửa hoặc chạy runtime/notebook/model/API.
- Next action: Giao DeepSeek focused remediation: tạo `notebooks/01_backend_foundation.ipynb`, rename notebook Phase 2 thành `notebooks/02_foods_data_and_chunking.ipynb`, cập nhật references và technical implementation reports; sau đó Codex review và tạo hai user reports `pending`.
