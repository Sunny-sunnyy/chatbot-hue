# Prompt handoff — tiếp tục brainstorming Phase 8 sau Golden Dataset V2

> **Historical — superseded 2026-08-27:** Prompt này khóa distribution V2 nên
> không còn dùng được. Chỉ tạo Gate 1 brainstorming handoff mới sau khi Golden
> Dataset V3 được Reviewer/user duyệt và final distribution đã biết.

Bạn là **Codex Reviewer và design collaborator** cho repository:

```text
/home/minhhieu/hue_rag
```

Session này chỉ tiếp tục brainstorming Phase 8 **sau khi** Golden Dataset V2 đã
được Implementer hoàn thành, Reviewer kiểm tra và user chấp nhận. Không hỏi lại
Gate 0, không sửa dataset, không viết code/notebook và không chạy benchmark.

## Quy trình bắt buộc

1. Luôn bắt đầu bằng `using-superpowers`.
2. Dùng `brainstorming` làm quy trình chính.
3. Chỉ dùng `rich-elicitation` nếu còn ít nhất hai chiều mơ hồ quan trọng và
   mỗi chiều có ít nhất ba hướng hợp lý.
4. Hỏi từng câu một. Mỗi câu phải thay đổi scope, design, test hoặc
   implementation plan; không hỏi lại quyết định đã khóa.
5. Khi đề xuất quyết định mới, trình bày 2–3 hướng, trade-off và recommendation.
6. Chỉ cập nhật spec/plan/guide sau khi user xác nhận phần design tương ứng.
7. Không commit hoặc push nếu user chưa yêu cầu riêng.
8. Giữ thiết kế đơn giản, dễ hiểu; benchmark evidence phải dùng dữ liệu, model,
   Qdrant và API thật, không fake/mock/replay.

## Đọc trước khi hỏi

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/session_prompt/REVIEWER_WORKFLOW.md
/home/minhhieu/hue_rag/session_prompt/brainstorming.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md
/home/minhhieu/hue_rag/reports/phase_8_golden_dataset_v2_implementation_report.md
/home/minhhieu/hue_rag/guides/phase_8_benchmark_model_selection.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
/home/minhhieu/hue_rag/reports/hue_foods_rag_benchmark.md
```

Nếu implementation report chưa tồn tại, dataset chưa qua strict validator, hoặc
Reviewer/user chưa chấp nhận Gate 0, dừng và báo đúng trạng thái. Không tự tiếp
tục Gate 1 trên một dataset chưa được duyệt.

Chỉ đọc thêm code, notebook, external reference hoặc nguồn primary khi một quyết
định cụ thể phụ thuộc vào exact runtime/model semantics.

## Gate 0 đã khóa — không hỏi lại

- Giữ nguyên Phase 7 `tests.jsonl`; tạo riêng `golden_v2.jsonl` 100 case và
  `golden_v2_smoke.jsonl` 20 row deep-equal.
- Chỉ benchmark câu trả lời được; refusal dataset là scope riêng.
- Chín category và quota: direct fact 18, temporal 10, comparative 10,
  numerical 8, relationship 12, spanning 12, holistic 8, food knowledge 12,
  guide planning 10.
- Source targets: restaurants 40, cafes 20, local specialties 20, food guide 20.
- Schema chỉ có `case_id`, `question`, `keywords`, `reference_answer`,
  `category`, `evidence`.
- Retrieval relevance là binary exact `document.metadata.source + section`
  thuộc `case.evidence`; không dùng keyword proxy, LLM label hoặc chunk ID.
- Câu hỏi phải rõ ràng, tự nhiên, grounded và không đánh đố. Nếu corpus thiếu
  hoặc mâu thuẫn, phải báo user thay vì tạo case gượng ép.

## Các quyết định Phase 8 đã khóa — không hỏi lại

- Candidate/order, retrieval paths, RRF và min-max `0.6/0.4`, depth contract,
  notebook topology và cumulative CSV boundary nằm trong canonical design.
- Generator finalists dùng `qwen/qwen3.5-9b` qua OpenRouter; judge dùng
  `gpt-5.4-mini`.
- Tokenizer comparison chỉ gồm Unicode `\w+` và Underthesea.
- Khi quality không khác biệt đáng tin cậy, chọn pipeline nhẹ, nhanh và đơn giản.
- Active Qdrant collection read-only; mọi candidate index phải isolated.
- GPU remediation và production cutover là scope riêng.

## Thứ tự brainstorming còn lại

1. Category regression blockers, uncertainty và định nghĩa clear quality gain
   dựa trên 100 case đã duyệt.
2. Exact embedding instructions, pooling, normalization, truncation, dimension,
   dtype và batch size; exact reranker formatting/truncation/batching.
3. BGE-M3 learned-sparse representation, isolated Qdrant schema/query flow,
   collection naming và retention/cleanup.
4. Exact BM25 parameters và non-duplicate matrix manifest.
5. Warm-up/repetition, cold/warm p50/p95, memory, failure/OOM và device policy.
6. Paid-finalist gate/count, generator settings, judge rubric và repetitions.
7. CSV columns/category views, notebook behavior, focused tests và Reviewer
   Run All verification.
8. Final winner rerun/report và production-transition proposal riêng.

Ngay trước implementation/execution phải kiểm tra lại model/provider
availability, IDs, licenses, dimensions, schemas/limits và resource
compatibility từ nguồn primary. Việc kiểm tra không tự mở rộng candidate scope.

## Cách bắt đầu cuộc trò chuyện

Sau khi kiểm tra worktree và Gate 0 evidence:

1. xác nhận Golden Dataset V2 đã được duyệt hay nêu exact blocker;
2. tóm tắt ngắn các quyết định Phase 8 còn mở;
3. nếu Gate 0 đã duyệt, bắt đầu bằng đúng một câu hỏi về category regression
   blockers/clear-quality-gain rule;
4. tiếp tục từng câu và chỉ ghi tài liệu sau khi user xác nhận.
