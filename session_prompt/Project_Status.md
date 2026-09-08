# Project Status

Last updated: `2026-09-08 +07`

## Project overview

`hue_rag` xây dựng hệ thống RAG về văn hóa và du lịch Huế. Baseline đã có là
Hue Foods RAG MVP. Dự án đang bổ sung dữ liệu trong `knowledge-base-hue` để mở
rộng sang toàn bộ corpus. Hybrid Recommender và Agentic RAG là roadmap chưa có
scope triển khai trong nhiệm vụ governance hiện hành.

Project ưu tiên code/data flow dễ hiểu, complexity tương xứng nhu cầu và bằng
chứng từ dữ liệu, database, model cùng API thật.

## System and data map

Luồng chính:

```text
raw sources -> curated foods Markdown -> 572 chunks
-> embeddings/Qdrant + optional local lexical scoring
-> retrieval -> optional reranking -> bounded context
-> grounded generation -> answer-only API
```

Foods corpus hiện gồm:

- 57 restaurants;
- 24 cafes;
- 9 local specialties;
- `food-guides.md` với 18 sections;
- 91 curated Markdown files tạo 572 deterministic chunks;
- Golden Dataset V3 canonical có 45 full cases và 10 smoke rows deep-equal.

Không chunk trực tiếp từ source dumps. Curated Markdown là closed-world source
cho retrieval/evaluation; web research không tự trở thành Golden evidence.

## Current runtime and data

Production baseline hiện dùng:

- local embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- active Qdrant collection `hue_foods_e5_small_384`, 572 points;
- profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`;
- Python BM25 và concrete local MiniLM cross-encoder reranker;
- bounded whole-chunk context;
- grounded generation bằng `gpt-5.4-nano`;
- answer-only JSON API và startup warm-up.

Active collection còn legacy sparse vector state từ các phase trước nhưng là
read-only trong implementation/review thông thường. Dense-only candidate
`hue_foods_e5_small_384_dense` tồn tại làm blue-green evidence; production chưa
cutover.

Notebooks 08a/08b/08c đã có evidence benchmark trên Foods; kết quả và artifact
chi tiết nằm trong canonical map phía dưới. Evidence này không chứng minh chất
lượng trên toàn bộ dữ liệu đang bổ sung. Baseline trên được giữ từ trạng thái
đã ghi nhận, không được chạy lại trong session docs-only này.

## Phase status

| Phase | Status | Current result / next boundary |
|---:|---|---|
| 0 | `approved` | MVP foundation và simplicity governance |
| 1 | `approved` | Backend foundation |
| 2 | `approved` | Foods Markdown chunking |
| 3 | `approved` | Dense embedding và sparse representation simplification |
| 4 | `approved` | Qdrant ingestion; dense-only candidate chưa cutover |
| 5 | `approved` | Retrieval profiles và reranking |
| 6 | `approved` | Context, generation và answer-only API |
| 7 | `approved` | Retrieval/answer evaluation baseline |
| 8 | `not_ready` | Gate 0, Gate 1 và Notebooks 08a/08b/08c approved; mở rộng toàn corpus chưa có approved implementation scope |
| 9 | `not_ready` | Agentic RAG roadmap chưa có approved scope |

Git và canonical artifacts giữ lifecycle history; file này chỉ mô tả trạng thái
đang có hiệu lực.

## Decisions currently in force

- Mỗi phase có canonical guide; report/status không tự tạo requirement.
- User đã chỉ đạo và hoàn tất Taxonomy Migration ngày 08/09/2026:
  Cấu trúc `knowledge-base-hue/tourism/` đã được di chuyển hoàn toàn sang
  `knowledge-base-hue/travel/` với ba nhánh con: `travel/places/`,
  `travel/services/` và `travel/tickets/`. Toàn bộ 47 file đã được phân bổ
  và đồng bộ đường dẫn; thư mục cũ `tourism/` đã được thu hồi.
- Golden V3 45+10 và benchmark hiện tại thuộc Foods. Tạo Golden mới cho toàn bộ
  dữ liệu cần scope và thiết kế riêng; chưa thay Golden hiện hành.
- Chi tiết experiment/model/matrix đã duyệt nằm trong guide/spec/plan Phase 8
  được dẫn dưới đây; không chép lại thành requirement độc lập trong status.
- Coding/testing dùng `skills/practical-project-coding/SKILL.md`; điều phối dùng
  `skills/risk-gated-agent-review/SKILL.md` và các workflow.
- Nhiệm vụ và next action duy nhất nằm trong `session_prompt/CURRENT_HANDOFF.md`.

## Safety and authorization boundaries

- Active `hue_foods_e5_small_384` chỉ read-only nếu không có exact user approval.
- Không expose secret hoặc đọc raw `.env` content.
- Không dùng fake provider/data/artifact hoặc old output làm fresh PASS evidence.
- Provider/model/dataset mới, paid run ngoài approved guide, deploy, active
  mutation, destructive cleanup và production cutover cần authority mới.
- Commit/push chỉ thực hiện khi latest user instruction hoặc current handoff ghi
  exact Git authorization.
- Implementer không tự approve; Reviewer không sửa runtime thay Implementer.

## Canonical document map

Bootstrap và role governance:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
skills/risk-gated-agent-review/SKILL.md
skills/practical-project-coding/SKILL.md
```

Project/Phase 8 entrypoints:

```text
guides/README.md
guides/phase_0_mvp_foundation.md
guides/phase_8_benchmark_model_selection.md
reports/hue_foods_rag_benchmark.md
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
```

Golden V3 and completed 08a:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
reports/phase_8_golden_dataset_v3_codex_review.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
reports/phase_8_08a_embedding_benchmark_codex_review.md
evaluation/results/phase8_embedding_results.csv
```

Approved 08b work package:

```text
docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md
docs/superpowers/plans/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-implementation-plan.md
notebooks/08b_retrieval_fusion_benchmark.ipynb
reports/phase_8_08b_retrieval_fusion_benchmark_codex_review.md
reports/user_reports/phase_8_08b_retrieval_fusion_benchmark_user_report.md
evaluation/results/phase8_sparse_manifest.json
evaluation/results/phase8_sparse_calibration.csv
evaluation/results/phase8_sparse_results.csv
evaluation/results/phase8_sparse_cases.jsonl
```

Approved 08c work package, confirmed by the user on `2026-08-30 +07`:

```text
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md
notebooks/08c_reranker_benchmark.ipynb
evaluation/results/phase8_reranker_results.csv
evaluation/results/phase8_reranker_cases.jsonl
reports/phase_8_08c_reranker_benchmark_codex_review.md
reports/user_reports/phase_8_08c_reranker_benchmark_user_report.md
```

Governance designs and plans:

```text
docs/superpowers/specs/2026-08-29-risk-gated-agent-review-design.md
docs/superpowers/plans/2026-08-29-risk-gated-agent-review-implementation-plan.md
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
```

## Workstream và roadmap

**Dữ liệu:** đang bổ sung và curate `knowledge-base-hue`. Sau khi dữ liệu hoàn
tất và được review, tạo lại Golden evaluation cho toàn bộ dữ liệu mới, rồi
nghiên cứu/thiết kế lại chunking, embedding, indexing/ingestion, retrieval,
context/generation và evaluation — các phần đã làm từ Phase 2 đến Phase 7,
nhưng áp dụng cho toàn corpus. Đây là định hướng user xác nhận, chưa phải quyền
chạy benchmark, thay Golden, mutate index hay triển khai runtime.

Dự án đã hoàn tất bước Taxonomy Migration từ `knowledge-base-hue/tourism/`
sang `knowledge-base-hue/travel/` ngày 08/09/2026 với ba nhánh con rõ ràng:
- `travel/places/`: 35 file entity điểm đến + cẩm nang `travel_guides.md` (được đổi tên từ `tourism_guides.md`).
- `travel/services/`: 04 cẩm nang dịch vụ du lịch + 01 inventory.
- `travel/tickets/`: 05 cẩm nang vé du lịch + 01 inventory.
Thư mục cũ `tourism/` đã được dọn sạch hoàn toàn, cố định cấu trúc đường dẫn canonical
trước khi khởi chạy pipeline chunking cho toàn bộ corpus.

Trạng thái biên soạn dữ liệu theo domain tại ngày 08/09/2026:

- `foods`: 91 file Markdown curated, gồm guide và các entity thực phẩm; đây vẫn
  là corpus duy nhất đang được runtime ingestion sử dụng.
- `heritages`: đã hoàn tất 28 entity trong `heritages/heritage/` và
  `heritage-guides.md`.
- `festivals`: đã có 26 entity trong `festivals/festival/` và
  `festival-guides.md`.
- `performing_arts`: đã có 11 entity trong `performing_arts/arts/` và
  `performing_arts_guides.md`.
- `travel/places`: 35 entity điểm đến và cẩm nang tổng quan `travel_guides.md` đã hoàn tất thẩm định.
- `travel/services`: 04 guide answer-facing và 01 inventory.
- `travel/tickets`: 05 file answer-facing đã hoàn tất biên soạn, thẩm định độc
  lập 2 lượt (reports/tickets_codex_review_2026_09_08.md và
  reports/tickets_codex_rereview_2026_09_08.md), khắc phục 100% (06/06) findings,
  lập User Report và được người dùng chính thức phê duyệt nghiệm thu ngày 08/09/2026.
  Bao gồm 05 cẩm nang answer-facing, 01 danh mục thực thể kiểm soát (inventory) và
  hồ sơ kiểm chứng tại mục XLIV–XLVIII của evidence.

Giai đoạn biên soạn và chuẩn hóa dữ liệu (Data Curation) cùng bước Taxonomy Migration
của toàn bộ kho tri thức `knowledge-base-hue` (gồm 5 domain: `foods`, `heritages`,
`festivals`, `performing_arts`, `travel`) đã HOÀN TẤT 100%.

**Định hướng và lộ trình tiếp theo đã được người dùng xác nhận:**

1. **Mở rộng Phase 2 (Markdown Chunking toàn corpus):**
   Mở rộng quy trình từ `guides/phase_2_foods_markdown_chunking.md` áp dụng cho
   toàn bộ corpus đa domain (`foods`, `heritages`, `festivals`, `performing_arts`,
   `travel`), phân tích cấu trúc H1/H2 và tạo ra các deterministic semantic chunks
   kèm metadata phong phú.

2. **Thiết kế Golden Datasets đa domain:**
   Thiết kế các bộ Golden Dataset đánh giá cho từng domain mới (`heritages`,
   `festivals`, `performing_arts`, `travel`) tương tự như cấu trúc chuẩn
   `knowledge-base-hue/foods/evaluation/golden_v3.jsonl` để làm căn cứ đánh giá
   (ground truth) cho retrieval và answer evaluation ở các phase sau.

Chi tiết tiến độ và các artifact nghiệm thu nằm tại:

- `knowledge-base-hue/travel/services/services-research-and-entities-inventory.md`;
- `knowledge-base-hue/travel/tickets/tickets-research-and-entities-inventory.md`;
- `knowledge-base-hue/meta/tourism-research-evidence.md`;
- `reports/tourism_guides_implementation_report_2026_09_07.md`;
- `reports/services_batches_01_03_minimal_reset_implementation_report_2026_09_08.md`;
- `reports/tickets_codex_review_2026_09_08.md`;
- `reports/tickets_codex_rereview_2026_09_08.md`;
- `session_prompt/CURRENT_HANDOFF.md`.
