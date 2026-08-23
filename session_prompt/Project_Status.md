# Project Status

Last updated: `2026-08-23 +07`

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
- Phase 7 sẽ dùng thêm `test2.jsonl` gồm 20 câu được chọn nguyên vẹn từ bộ 104.

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
| 0 | `approved` | Đã hoàn thành: kiến trúc và contract nền tảng; sẽ được review đơn giản hóa lại sau Phase 7 |
| 1 | `approved` | Đã hoàn thành: backend skeleton, config, logging và notebook 01; sẽ được review lại sau Phase 7 |
| 2 | `approved` | Đã hoàn thành: curated foods loader, 572 chunks và notebook 02; sẽ được review lại sau Phase 7 |
| 3 | `approved` | Đã hoàn thành: dense/sparse representation và notebook 03; sẽ được review lại sau Phase 7 |
| 4 | `approved` | Đã hoàn thành: Qdrant collection 572 points và notebook 04; sẽ được review lại sau Phase 7 |
| 5 | `approved` | Đã hoàn thành: ba retrieval profiles, context và notebook 05; sẽ được review lại sau Phase 7 |
| 6 | `approved` | Đã hoàn thành: generation, API, lifecycle warm-up và notebook 06; sẽ được review lại sau Phase 7 |
| 7 | `ready` | Thiết kế evaluation đơn giản đã duyệt; chưa có implementation mới được review/approve |
| 8 | `not_ready` | Chưa mở; chỉ bắt đầu sau Phase 7 và review đơn giản hóa Phase 0–6 |
| 9 | `not_ready` | Roadmap Agentic RAG, chưa có implementation scope được duyệt |

Milestone 6.1 Baseline Lifecycle Hardening thuộc Phase 6 và đã được user xác
nhận.

## Trạng thái hiện tại

Governance đơn giản hóa toàn dự án đã được user thiết kế, phê duyệt, review và
cập nhật vào các tài liệu hiện hành. Phase 7 giữ trạng thái canonical `ready`
theo
`guides/phase_7_retrieval_answer_evaluation.md`.

Phase 7 mới phải đi theo luồng:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Existing Phase 7 files và worktree có thể còn code/artifacts của các vòng cũ.
Chúng không phải implementation mới đã được chấp nhận và không thay đổi trạng
thái canonical. Implementer phải đối chiếu exact guide trước khi sửa hoặc xóa.

Phase 8 vẫn đóng.

## Quyết định hiện hành

- Mỗi phase có một guide canonical.
- Code phải rõ ràng, dễ hiểu và không kỹ thuật hơn nhu cầu thật.
- Reviewer phải yêu cầu bỏ over-engineering.
- Chỉ tạo test cho hành vi thật và lỗi quan trọng; không chạy theo số lượng.
- Không dùng mock/fake trong test, implementation hoặc evidence.
- Completion evidence đến từ dữ liệu và hệ thống thật.
- Reviewer/Implementer được dùng online và paid API trong approved phase.
- Không có consent gate, cost cap hoặc cost-estimation code cho run đã nằm
  trong guide.
- Provider/model/scope mới, deploy, active mutation và destructive action cần
  user approval.
- Mỗi implementation Phase 1–8 có một notebook ngắn dành cho con người.
- Xác nhận phase không tự cấp quyền commit/push.
- Sau lần `changes_requested` thứ 4, dừng để audit lại design/guide/plan trước
  vòng sửa thứ 5.
- CodeGraph được giữ như công cụ discovery tùy chọn, không phải blocker.

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
user review governance docs
-> Implementer xây Phase 7 đơn giản theo guide canonical
-> Reviewer đọc source và chạy lại Phase 7 bằng dữ liệu/API thật
-> user chạy notebook 07 và xác nhận
-> review, thiết kế lại khi cần và đơn giản hóa Phase 0 -> Phase 6
-> chạy lại affected Phase 7 evaluation sau mỗi thay đổi liên quan
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

Phase 7:

```text
guides/phase_7_retrieval_answer_evaluation.md
docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
reports/hue_foods_rag_benchmark.md
```
