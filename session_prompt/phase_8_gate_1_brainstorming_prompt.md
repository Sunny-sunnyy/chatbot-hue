# Phase 8 Gate 1 — Brainstorming Handoff

Bạn đang mở session thiết kế Gate 1 cho Phase 8 Benchmark Model Selection của
dự án Hue RAG tại:

```text
/home/minhhieu/hue_rag
```

## Trạng thái đầu vào đã khóa

- Phase 0–7 đã `approved`.
- Golden Dataset V3 Gate 0 đã được Reviewer xác minh và User phê duyệt ngày
  `2026-08-28 +07`.
- Final full dataset có đúng `45` câu; smoke dataset có đúng `10` row
  deep-equal.
- Technical review: `ready_for_user_confirmation`; user đã xác nhận final
  content và size, nên lifecycle Gate 0 là `approved`.
- Đây là Gate 1 brainstorming, không phải correction V2/V3 và không phải
  implementation hoặc benchmark execution.

## Quy trình bắt buộc

Luôn bắt đầu bằng `using-superpowers`. Đọc đầy đủ và tuân thủ `brainstorming`;
dùng `verification-before-completion` trước mọi tuyên bố hoàn tất tài liệu.
Brainstorm với User từng quyết định có ảnh hưởng thật đến scope, design, test
hoặc implementation plan. Ưu tiên một câu hỏi rõ ràng mỗi lượt và nêu lựa chọn
khuyến nghị cùng trade-off.

Không tạo hoặc sửa design, plan, code hay notebook trước khi User xác nhận nội
dung đã brainstorm. Khi User mới chỉ đang thảo luận, dừng ở proposal và câu hỏi
tiếp theo.

## Tài liệu phải đọc trước khi hỏi câu đầu tiên

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/brainstorming.md
guides/phase_8_benchmark_model_selection.md
reports/hue_foods_rag_benchmark.md
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
reports/phase_8_golden_dataset_v3_implementation_report.md
reports/phase_8_golden_dataset_v3_codex_review.md
knowledge-base-hue/foods/evaluation/golden_v3.jsonl
knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl
```

`reports/hue_foods_rag_benchmark.md` là baseline/benchmark summary canonical;
dùng nó để giữ Gate 1 bám vào pipeline và real evidence hiện có, không xem các
candidate hoặc winner chưa được duyệt trong file này là authorization chạy.

Đọc thêm source code, tests, notebook references hoặc tài liệu chính thức chỉ
khi cần để trả lời đúng một quyết định đang brainstorm. Trước mọi kiểm tra web
về model/provider, ưu tiên nguồn chính thức và ghi rõ đó là research cho design,
không phải authorization tải model hoặc chạy API.

## Mục tiêu Gate 1

Dùng final V3 distribution để khóa lần lượt các contract còn mở trong
`guides/phase_8_benchmark_model_selection.md#backlog-brainstorming-sau-gate-0-implementation`:

1. category regression blockers, uncertainty và clear-quality-gain rule;
2. embedding instructions, pooling, normalization, truncation, dimension,
   dtype và batch size;
3. reranker input formatting, truncation và batching;
4. BGE-M3 learned-sparse representation, isolated storage/query path,
   collection naming và retention/cleanup;
5. BM25 parameters cho Unicode tokenizer và Underthesea;
6. exact non-duplicate matrix manifest và execution order;
7. warm-up/repetition, latency, memory, failures/OOM và device policy;
8. paid finalist gate/count, Qwen generation settings, GPT judge rubric và
   repetition policy;
9. readable CSV columns/category views, notebook behavior, focused tests và
   Reviewer reruns;
10. final winner rerun/report/handoff và production-transition proposal riêng.

Không hỏi lại những quyết định đã khóa trong canonical guide/design, trừ khi có
evidence mới chứng minh contract hiện tại không khả thi hoặc mâu thuẫn. Nếu có,
trình exact evidence và xin User cho phép reopen quyết định đó.

## Boundary

Trong session brainstorming này, không:

- sửa Golden Dataset V3, V2, Phase 7 data hoặc curated Markdown;
- viết implementation code/tests/notebooks;
- tải model, cài dependency, CUDA hoặc PyTorch;
- chạy benchmark, paid generation/judge hoặc gọi paid API;
- tạo/mutate/xóa Qdrant collection, đặc biệt active collection
  `hue_foods_e5_small_384`;
- production cutover;
- commit hoặc push nếu chưa có yêu cầu riêng.

Gate 0 approval không cấp các quyền trên. Phase 8 tổng thể vẫn `not_ready`.

## Kết quả mong đợi

Sau khi mọi quyết định Gate 1 đã được User xác nhận:

1. cập nhật canonical guide và master design để phản ánh exact contracts;
2. viết hoặc cập nhật implementation plan có checkpoints và verification rõ;
3. trình User duyệt design/plan;
4. chỉ tạo handoff Implementer hoặc authorize exact run group sau approval
   riêng của User.

Bắt đầu session bằng cách tóm tắt ngắn trạng thái đã khóa, xác nhận không có
quyền execution, rồi hỏi đúng quyết định Gate 1 đầu tiên có ảnh hưởng lớn nhất.
