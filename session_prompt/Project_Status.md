# Project Status

Last updated: `2026-08-25 +07`

## Mục tiêu

`hue_rag` xây dựng:

- RAG Chatbot về văn hóa và du lịch Huế;
- Hue Foods RAG MVP;
- Hybrid Recommender + LLM;
- Agentic RAG sau khi MVP ổn định.

Trọng tâm hiện tại là hoàn thành Hue Foods RAG theo hướng code đơn giản, dễ
hiểu và được chạy bằng dữ liệu, database, model và API thật.

## Dữ liệu và thành phần hiện có

Luồng dữ liệu:

```text
raw -> Markdown source dumps -> curated Markdown
-> chunks -> embeddings/index -> retrieval -> context -> answer
```

Dữ liệu foods:

- 57 restaurants;
- 24 cafes;
- 9 local specialties;
- `food-guides.md` gồm 17 sections;
- `knowledge-base-hue/foods/evaluation/tests.jsonl` gồm 104 câu thật;
- Phase 7 dùng thêm `test2.jsonl` gồm 20 câu được chọn nguyên vẹn từ bộ 104.

Runtime hiện có:

- 572 chunks từ curated foods Markdown;
- local dense embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- deterministic sparse representation;
- Qdrant collection `hue_foods_e5_small_384`, 572 points;
- profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`;
- local BM25 và MiniLM reranker;
- bounded context;
- grounded generation bằng `gpt-5.4-nano`;
- JSON API và startup warm-up.

Active Hue Qdrant collection chỉ read-only trong implementation, test và review
thông thường.

## Trạng thái Phase 0–9

| Phase | Trạng thái | Kết quả hiện có / việc còn lại |
|---:|---|---|
| 0 | `approved` | Simplicity review đã approved; docs-only, không đổi runtime hoặc active collection |
| 1 | `approved` | Backend foundation đã đơn giản hóa, chạy thật, review và được user xác nhận |
| 2 | `approved` | Foods Markdown chunking đã đơn giản hóa, chạy thật, review và được user xác nhận |
| 3 | `approved` | Embedding/sparse đã được đơn giản hóa, chạy thật, review và được user xác nhận |
| 4 | `approved` | Giữ approval cũ; bước tiếp theo là simplicity review Phase 4 |
| 5 | `approved` | Giữ approval cũ; chờ review Phase 4 |
| 6 | `approved` | Giữ approval cũ; chờ review Phase 5 |
| 7 | `approved` | Evaluation đơn giản đã chạy thật, đạt technical review và được user xác nhận |
| 8 | `not_ready` | Chưa mở; chỉ bắt đầu sau Phase 7 và review đơn giản hóa Phase 0–6 |
| 9 | `not_ready` | Roadmap Agentic RAG, chưa có implementation scope được duyệt |

Milestone 6.1 Baseline Lifecycle Hardening thuộc Phase 6 và đã được user xác
nhận.

## Trạng thái hiện tại

Governance đơn giản hóa toàn dự án đã được user thiết kế, phê duyệt, review và
cập nhật vào các tài liệu hiện hành. Phase 7 hiện ở `approved` theo
`guides/phase_7_retrieval_answer_evaluation.md`: implementation đơn giản đã
chạy real Qdrant, nano/mini, 20/104 questions và Notebook 07; correction vòng 1
đã đạt technical review và được user xác nhận ngày 2026-08-24 +07.

Phase 7 mới phải đi theo luồng:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Hai CSV cố định hiện giữ fresh full-run 104 rows. Một answer row ghi đúng lỗi
model tham chiếu source ID không hợp lệ; batch vẫn hoàn thành và không dùng
retry hoặc fallback giả.

Phase 8 vẫn đóng.

Phase 0 simplicity review đã được user duyệt ngày `2026-08-24 +07`. Review giữ
nguyên capability của MVP, đặt concrete code làm mặc định, chỉ giữ abstraction
cho nhiều implementation thật hoặc provider boundary thật, và yêu cầu mỗi
Phase 1–6 có một hồ sơ Before/After. Không có runtime change; baseline mới nhất
vẫn là full backend `222 passed, 4 warnings`.

Phase 1 simplicity implementation đã được review và user xác nhận ngày
`2026-08-24 +07`. YAML/settings/schema/package layout được giữ; logging chung
đã kết nối tại API lifespan, ingestion main và evaluation main; active-profile
validation đã inline; Notebook 01 và config README trùng lặp đã xóa. Live
settings/logging/Uvicorn/Gradio/Qdrant checks đạt và active collection vẫn 572
points. Hai suite 74/222 tests đã chạy là observed history quá rộng, không phải
acceptance target hoặc bằng chứng rằng mọi test đều cần thiết.

Phase 2 simplicity implementation đã được review và user xác nhận ngày
`2026-08-24 +07`. Parser và metadata helper đã được hấp thụ vào chunker, text
splitter được giữ riêng, Notebook 02 chỉ gọi public API và ordered corpus vẫn
khớp tuyệt đối 572 chunks từ 91 files. Focused suite 15 tests bảo vệ distinct
Phase 2 behaviors; downstream 79 và full 206 test runs chỉ là observed evidence
theo blast radius của refactor, không phải acceptance target hoặc checkpoint
mặc định cho các lần chạy sau.

Phase 3 simplicity implementation đã được review và user xác nhận ngày
`2026-08-25 +07`. Dense runtime nay chỉ còn concrete `E5Embedder` với
instance-owned lazy model, E5 prefixes cố định và native batching; provider
abstraction, outer batching và OpenRouter adapter/config/tests đã bị xóa. Sparse
TF-IDF được làm rõ hơn nhưng giữ Phase 4 compatibility.

Observed Phase 3 result:

- Notebook 03 Run All: 572 x 384, norm 1.0, 26.13 giây;
- active `dense_only` query trả 10 results với top chunk Bún bò Huế;
- focused 10, affected 59 và full backend 190 tests đã pass;
- active `hue_foods_e5_small_384` vẫn 572 points và không còn guarded
  test collection;
- không chạy lại Phase 7 evaluation vì model, dimension, instructions và
  retrieval behavior được giữ; real active query đã pass.

## Quyết định hiện hành

- Mỗi phase có một guide canonical.
- Code phải rõ ràng, dễ hiểu và không kỹ thuật hơn nhu cầu thật.
- Reviewer phải yêu cầu bỏ over-engineering.
- Chỉ tạo test cho hành vi thật và lỗi quan trọng; không chạy theo số lượng.
- Audit test theo ownership của phase; xóa và không chạy test không bảo vệ nhu
  cầu người dùng, chỉ dựng lỗi giả định hoặc chỉ phục vụ cơ chế bị loại bỏ.
- Exact live path là bằng chứng chính; một phase có thể không cần automated
  test.
- Full backend suite chỉ chạy cho shared runtime/data contract có blast radius
  rộng hoặc final Phase 0–6 check.
- Evaluation 20 câu chỉ chạy khi thay đổi có thể ảnh hưởng chất lượng RAG;
  không mặc định chạy bộ 104 câu trong simplicity review.
- Không dùng mock/fake trong test, implementation hoặc evidence.
- Completion evidence đến từ dữ liệu và hệ thống thật.
- Reviewer/Implementer được dùng online và paid API trong approved phase.
- Không có consent gate, cost cap hoặc cost-estimation code cho run đã nằm
  trong guide.
- Provider/model/scope mới, deploy, active mutation và destructive action cần
  user approval.
- Chỉ phase có giá trị học tập thật mới có notebook; canonical guide quyết định.
- Xác nhận phase không tự cấp quyền commit/push.
- Sau lần `changes_requested` thứ 4, dừng để audit lại design/guide/plan trước
  vòng sửa thứ 5.
- CodeGraph được giữ như công cụ discovery tùy chọn, không phải blocker.
- Chỉ giữ abstraction khi có nhiều implementation thật hoặc provider boundary
  thật; internal wrappers không phải compatibility requirement.
- Mỗi Phase 0–6 có một simplicity review ghi Before/After, capability được giữ,
  ảnh hưởng downstream, verification, bug và cách xử lý.
- Verification đi theo blast radius; chỉ chạy lại Phase 7 evaluation khi thay
  đổi có thể ảnh hưởng chất lượng RAG.
- Quyết định giữ, bỏ hoặc dùng native Qdrant sparse vectors thuộc review Phase
  3–5; collection hiện tại được giữ nguyên trong Phase 0.
- Lexical target đã được user chốt: Qdrant dense candidates -> Python BM25
  fusion -> optional CrossEncoder. Stored sparse vectors tạm giữ trong Phase 3
  và sẽ được xử lý có phối hợp ở review Phase 4–5.
- OpenRouter embedding không còn là Phase 3 runtime boundary. Phase 8 mới xác
  minh exact API/model/dimension/limits/pricing và tạo adapter/config theo
  candidate được duyệt.

Các cơ chế cost accounting, consent gate, calibration, resume, run identity,
timestamp package, checksum, package matching, tamper detection, partial
artifact, complex artifact audit, layered validators và tests chỉ phục vụ chúng
phải được loại bỏ trong đúng approved scope, không đổi tên hoặc di chuyển để
giữ lại.

## Worktree và an toàn

Worktree hiện không sạch và chứa nhiều thay đổi từ các vòng Phase 7 trước cùng
một số thay đổi không liên quan. Coding agent phải:

- chạy `git status --short` trước khi sửa;
- đọc diff của exact files trong scope;
- giữ nguyên thay đổi không liên quan;
- không reset, checkout, broad-delete, stage, commit hoặc push ngoài quyền;
- không mở hoặc expose secret values;
- giữ active Hue Qdrant collection read-only.

## Next action

```text
Phase 3 simplicity review đã approved
-> tiếp tục simplicity review Phase 4 -> Phase 6
-> chạy Phase 7 evaluation 20 câu khi thay đổi có thể ảnh hưởng chất lượng RAG
-> chạy final full backend suite sau khi Phase 0–6 hoàn tất
-> chỉ sau đó mới cân nhắc Phase 8
```

Khi review Phase 0–6, Repo và live system là nguồn đối chiếu chính: guide,
reports, source code, notebook và real run đủ để bắt đầu. Tài liệu ngoài do
user cung cấp chỉ dùng khi thực sự hữu ích. Nếu không có và vẫn còn lựa chọn
quan trọng, Reviewer brainstorm với user trước khi duyệt design thay đổi.
Không dùng Phase 7 reference làm blueprint cho phase khác.

## Tài liệu đọc tiếp

Mọi coding agent:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
workflow đúng với vai trò
guides/README.md
guides/phase_0_mvp_foundation.md
guide canonical của phase đang làm
```

Review đơn giản hóa Phase 1–6:

```text
docs/superpowers/specs/2026-08-24-phase-0-simplicity-review-design.md
reports/phase_0_mvp_foundation_simplicity_review.md
guides/llm_rag_reference_for_hue_rag.md
docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-1-backend-foundation-simplicity-implementation.md
reports/phase_1_backend_skeleton_simplicity_review.md
docs/superpowers/specs/2026-08-24-phase-2-foods-markdown-chunking-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-2-foods-markdown-chunking-simplicity-implementation.md
reports/phase_2_foods_markdown_chunking_simplicity_review.md
docs/superpowers/specs/2026-08-24-phase-3-embedding-sparse-representation-simplicity-design.md
docs/superpowers/plans/2026-08-24-phase-3-embedding-sparse-representation-simplicity-implementation.md
reports/phase_3_embedding_sparse_representation_simplicity_review.md
guides/phase_3_embedding_sparse_representation.md
```

Phase 7:

```text
guides/phase_7_retrieval_answer_evaluation.md
docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
reports/hue_foods_rag_benchmark.md
```
