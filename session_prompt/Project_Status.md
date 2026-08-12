# Project Status

Last updated: `2026-08-12 18:06 +07`

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
- Giai đoạn 1 `approved`: backend skeleton, cấu hình chung, logging, shared schema và `notebooks/01_backend_foundation.ipynb` đã được Codex kiểm tra; người dùng đã chạy notebook và xác nhận.
- Giai đoạn 2 `approved`: đọc 91 curated foods files và tạo 572 đoạn; nội dung thường giới hạn 400 ký tự, bảng được giữ nguyên, mỗi đoạn có nhãn ngữ cảnh ngắn; 31 kiểm thử và `notebooks/02_foods_data_and_chunking.ipynb` đã đạt; người dùng quan sát đúng 572 đoạn, 0 đoạn thường vượt 400 và 8 bảng vượt 400 rồi xác nhận.
- Giai đoạn 3 `approved`: dense E5 local với vector 384 chiều đã chuẩn hóa, sparse TF-IDF deterministic trên 572 đoạn và OpenRouter embedding adapter live-ready đã được kiểm tra bằng mock; 74 kiểm thử đạt. Người dùng đã chạy `notebooks/03_embedding_models.ipynb` ở default mode, quan sát 572 đoạn, vocabulary 2093, kết quả deterministic, thứ tự vector được giữ và TF-IDF khớp.
- Giai đoạn 4 `approved`: Qdrant 1.18.3 chạy local bằng Docker Compose pinned image; collection `hue_foods_e5_small_384` có 572 points, named dense vector 384 chiều cosine và sparse index. Codex đã kiểm tra notebook ở default mode và real read-only mode; người dùng xác nhận phase và chọn không tự chạy notebook trước khi phê duyệt.
- Hoàn tất migration tài liệu điều hành: `guides/README.md`, 10 phase guides và `reports/hue_foods_rag_benchmark.md` thay thế ba spec/plan/benchmark documents cũ dưới `docs/superpowers/`; workflows, templates và Phase 1–2 report references đã được cập nhật.
- Chốt dual-report governance: technical reports trong `reports/` dành cho coding agents; user reports trong `reports/user_reports/` do Codex viết bằng tám mục, tiếng Việt dễ hiểu, không hiển thị mã trạng thái nội bộ; Phase 1–8 bắt buộc có notebook mang đúng số phase và chỉ `approved` sau user confirmation.

Chưa thực hiện:

- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Brainstorm và implement Phase 5–8 của Hue Foods RAG MVP theo guide; Phase 5
  đang `not_ready` và cần brainstorming Level 3 trước implementation.
- Chạy local E5/MiniLM three-profile benchmark rồi mới thử OpenRouter; ledger hiện chưa có benchmark result hoặc winner.
- Enrichment có nguồn xác minh; recommender; Agentic RAG sau MVP.
- Chạy bộ test trên evaluator thật (retrieval MRR/nDCG + LLM-judge) sau khi có pipeline RAG foods.

## Cập nhật gần nhất

### 2026-08-12 18:06 +07

- Trạng thái: Giai đoạn 4 `approved`. Người dùng xác nhận kết quả và cho phép commit/push dù chưa tự chạy notebook; Codex đã chạy notebook ở default mode và real read-only mode trước approval. Giai đoạn 5 vẫn `not_ready`.
- File chính: `backend/vectorstore/`, `backend/ingestion/pipeline.py`, `docker-compose.yml`, `notebooks/04_qdrant_ingestion.ipynb`, guide và ba báo cáo Phase 4.
- Validation: 44 kiểm thử Phase 4 và 118 kiểm thử toàn backend đạt; `py_compile` năm module đạt; Docker Compose config hợp lệ; Qdrant 1.18.3 có collection green với đúng 572 points, dense 384 cosine, sparse index và 572/572 identity hợp lệ; notebook schema sạch và chạy đạt ở default mode cùng real read-only mode; `git diff --check` sạch; CodeGraph index up to date với 43 files, 513 nodes và 1.336 edges. Chưa live-test ingestion rerun hoặc reset collection.
- Next action: Brainstorm Giai đoạn 5 theo Level 3; chưa implement retrieval profiles, reranking hoặc retrieval benchmark trước khi user phê duyệt design.

### 2026-08-12 15:19 +07

- Trạng thái: CodeGraph workflow đã được chi tiết hóa cho Reviewer và Implementer; Phase 4 vẫn `not_ready` và chưa bắt đầu brainstorming/implementation.
- File chính: `session_prompt/REVIEWER_WORKFLOW.md` và `session_prompt/IMPLEMENTER_WORKFLOW.md`. `rag_old/` đã được chuyển sang `llm_rag/tai_lieu/rag_old` theo yêu cầu của user.
- Validation: thư mục đích có đủ 88 files và không còn `rag_old/` trong repo hoặc temporary backup; hai workflow yêu cầu status/sync ở đầu session và cuối guide handoff; `git diff --check` sạch.
- Next action: Mở session Reviewer mới, chạy CodeGraph checkpoint rồi brainstorm Phase 4 theo Level 2.

### 2026-08-12 15:10 +07

- Trạng thái: Phase 1–3 giữ `approved`; Phase 4 vẫn `not_ready` và sẽ brainstorm trong session mới. User xác nhận 572 chunks cùng giới hạn 400 ký tự là contract đúng cho Phase 4–8.
- File chính: `guides/phase_4_qdrant_ingestion.md`, `reports/hue_foods_rag_benchmark.md`, shared session context và role workflows. `rag_old/` đã được đưa ra khỏi repo; các thay đổi có sẵn khác của user được giữ nguyên.
- Validation: CodeGraph 1.5.0 đã init local với telemetry tắt; index up to date gồm 34 files, 352 nodes và 824 edges; truy vấn thử nhận diện đúng chunking/sparse embedding flow; contract active không còn dùng 366 chunks hoặc giới hạn 1.500 ký tự; `git diff --check` sạch.
- Next action: Mở session Reviewer mới, đọc context rồi brainstorm Phase 4 theo Level 2. Không implement hoặc mutate Qdrant trước khi Phase 4 được user phê duyệt thành `ready`.

### 2026-08-11 16:43 +07

- Trạng thái: Phase 0 `completed`; Giai đoạn 1–3 `approved`; Giai đoạn 4–8 `not_ready`; Giai đoạn 9 `design_only`. Người dùng đã chạy và xác nhận ba notebook đầu.
- File chính: `backend/embedding/`, `backend/config/settings.yaml`, `notebooks/03_embedding_models.ipynb`, guide/báo cáo kỹ thuật/Codex và user report Phase 3.
- Validation: 74 tests đạt; `py_compile` năm module embedding đạt; local E5 offline trả vector 384 chiều norm 1; notebook schema hợp lệ, outputs được làm sạch sau user run; `git diff --check` sạch. Không gọi OpenRouter, Qdrant hoặc dịch vụ trả phí.
- Next action: Brainstorm Giai đoạn 4 theo `guides/phase_4_qdrant_ingestion.md`; Qdrant collection mutation hoặc model/API live run vẫn cần approval riêng.
