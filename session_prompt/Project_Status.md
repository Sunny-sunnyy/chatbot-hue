# Project Status

Last updated: `2026-08-30 +07`

## Project overview

`hue_rag` xây dựng hệ thống RAG về văn hóa và du lịch Huế. Milestone hiện tại
là Hue Foods RAG MVP: truy vấn dữ liệu ẩm thực đã curate, tìm đúng evidence,
tạo context có giới hạn và sinh câu trả lời grounded. Sau khi MVP ổn định,
roadmap mới mở rộng sang Hybrid Recommender và Agentic RAG.

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
- `food-guides.md` với 17 sections;
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

Phase 8 Notebook 08a đã benchmark local dense embeddings trên CPU FP32 với 45
Golden V3 cases và 572 chunks. Executable catalog hiện chỉ gồm:

1. `e5-small-384` — control 384D;
2. `huydang-dek21-embedding-768` — candidate 768D;
3. `e5-base-768` — candidate 768D.

Mỗi model có 3/3 repetition evidence trên 45 Golden V3 cases và 572 chunks.

Phase 8 Notebook 08b đã hoàn tất 20-setting retrieval/fusion matrix với 70
calibration rows, 200 result rows và 900 per-case records. Unicode tokenizer
được giữ vì Underthesea không cải thiện đủ để tăng complexity. Hybrid tăng
overall recall nhưng cả BM25 và TF-IDF finalist đều `None`: category
`relationship` có nDCG@5 delta `-0.0279273`, thấp hơn guardrail `-0.02`.
Production config và active collection không thay đổi.

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
| 8 | `not_ready` | Gate 0, Gate 1, Notebook 08a và 08b approved; exact 08c design/spec approved, implementation plan chờ user review; chưa authorize implementation/run |
| 9 | `not_ready` | Agentic RAG roadmap chưa có approved scope |

Git và canonical artifacts giữ lifecycle history; file này chỉ mô tả trạng thái
đang có hiệu lực.

## Decisions currently in force

- Mỗi phase có một canonical guide; reports/status không tự tạo requirement.
- Golden Dataset V3 45+10 đã approved và không được sửa trong Phase 8 benchmark
  nếu chưa có scope riêng.
- Main local benchmark profile là CPU FP32; failed/OOM phải được ghi đúng, không
  silent fallback hoặc đổi setting.
- Khi quality không khác biệt đáng tin cậy, ưu tiên model nhẹ, nhanh và đơn giản.
- Local dense Phase 8 chỉ có ba model executable hiện hành nêu trên.
- Active reranker comparison chỉ có no-rerank và current local
  `cross-encoder/ms-marco-MiniLM-L-6-v2`; BGE/Qwen rerankers không còn thuộc
  08c/08d scope.
- Initial fusion comparison dùng RRF và independent min-max weighted sum
  `0.6 dense / 0.4 sparse`; không weight grid khi chưa có observed need.
- Notebook 08b chỉ so sánh tokenizer BM25 Unicode `\w+` hiện hành với
  Underthesea `word_tokenize(..., format="text")`; không mở tokenizer grid.
- Notebook 08b có exact 20-setting matrix trên 45 Golden V3 cases. `900`
  per-case records là một record cho mỗi setting/case để audit ranking và
  fusion, không phải mở rộng Golden Dataset lên 900 câu.
- Implementer 08b được chia run thành số batch tùy tài nguyên, persist atomically
  sau từng setting, resume theo exact provenance và giải phóng tài nguyên giữa
  batch. Không shortlist trước khi reconcile đủ matrix.
- Canonical notebooks là learning documents, gọi backend trực tiếp và giữ sạch
  outputs/execution counts trong repo.
- Runtime/code/test practice dùng `skills/practical-project-coding/SKILL.md`.
- Reviewer/Implementer coordination dùng
  `skills/risk-gated-agent-review/SKILL.md` và một current handoff.
- Không thêm cost accounting, repeated consent gate, resume/run-identity,
  checksum/tamper audit hoặc validator machinery nếu exact approved scope không
  có observed need tương xứng.

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

Exact 08c written specification approved by the user on `2026-08-30 +07`:

```text
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
```

Governance designs and plans:

```text
docs/superpowers/specs/2026-08-29-risk-gated-agent-review-design.md
docs/superpowers/plans/2026-08-29-risk-gated-agent-review-implementation-plan.md
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
```

## Current next action

Notebook 08b đã được triển khai, review độc lập và user xác nhận ngày
`2026-08-30 +07`. Exact Notebook 08c conversational design đã được user xác
nhận và written spec nằm tại
`docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md`.
Current next action là user review implementation plan cùng Review Contract tại
`docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md`.
Chưa có authorization cho implementation, benchmark run, paid API, active
mutation hoặc production cutover cho 08c.

Post-08c queued reviewer workstream: hoàn thiện toàn bộ curated answer-facing
Markdown dưới `knowledge-base-hue/` cho Foods, Festivals, Heritage, Tourism,
Performing Arts và các domain được duyệt khác; sau đó cập nhật domain-aware
chunking/metadata, tạo embedding mới và isolated full-corpus index. Một Combined
Golden Dataset mới phải có quota/evidence trên tất cả domain để báo cáo overall
và per-domain. Evaluation bắt đầu lại từ Phase 7 baseline rồi chạy lại các phần
Phase 8 bị ảnh hưởng. Kết quả hiện tại chỉ là Foods historical evidence.

Chưa có authorization thay đổi corpus/code, tạo embedding/index/Golden mới,
mutate Qdrant hoặc chạy benchmark đa lĩnh vực; exact post-08c design bắt đầu sau
khi lifecycle 08c Foods đóng.
