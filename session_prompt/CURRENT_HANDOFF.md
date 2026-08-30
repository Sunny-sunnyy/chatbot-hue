# Bàn giao hiện hành

Target role: reviewer
Authored by: reviewer
Handoff kind: next_design
State: ready
Base commit: worktree
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none

---

## 1. Trạng thái đã đóng

Notebook 08b retrieval/fusion benchmark đã được user xác nhận ngày
`2026-08-30 +07` và work package hiện `approved`.

Kết luận giữ nguyên:

- Unicode tokenizer được chọn;
- BM25 finalist: `None`;
- TF-IDF finalist: `None`;
- relationship nDCG@5 delta `-0.0279273` vi phạm guardrail `-0.02`;
- production config và active collection không cutover hoặc mutate.

Phase 8 tổng thể vẫn `not_ready`.

## 2. Next action duy nhất

User review implementation plan cùng Review Contract cho exact Notebook 08c:

```text
docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md
```

Conversational design, written specification approval, documentation sync và
implementation plan đã hoàn tất. Implementer handoff chỉ được tạo sau khi user
duyệt plan.

Không được bắt đầu implementation, benchmark run, model download mới, paid API,
active Qdrant mutation, production cutover hoặc sửa Golden V3 trong handoff này.

## 3. Design gate

Đã hoàn tất:

1. exact scope/dependency research;
2. candidates, fixed inputs, metrics, resource và acceptance brainstorming;
3. comparison of three approaches và user selection;
4. written exact specification cùng Reviewer documentation sync.

Còn lại:

1. user review implementation plan/Review Contract;
2. Implementer handoff chỉ sau plan approval.

## 4. Boundaries phải giữ

- Reuse approved Golden V3 45 full + 10 smoke cases.
- 08b artifacts là immutable evidence; không chọn sparse finalist sau approval.
- Active 08c scope chỉ có no-rerank và current MiniLM trên ba fixed Top-10
  inputs đã duyệt; BGE/Qwen rerankers không còn trong 08c/08d.
- Active `hue_foods_e5_small_384` read-only.
- Không silent fallback, fake provider/data hoặc đổi experiment inputs để tạo
  winner.
- Phase 8 và 08c implementation/run vẫn chưa authorized.
- Git authorization là `none` cho next-design work.
- Sau khi 08c Foods đóng, next workstream không còn là festivals-only pilot mà
  là hoàn thiện toàn bộ answer-facing `knowledge-base-hue/`, tạo embedding/index
  mới và Combined Golden Dataset cân bằng trên Foods, Festivals, Heritage,
  Tourism, Performing Arts cùng các domain được duyệt khác. Evaluation bắt đầu
  lại từ Phase 7 rồi rerun các phần Phase 8 bị ảnh hưởng.
- Foods 07/08 results chỉ là historical domain evidence; post-08c corpus,
  chunking, index, Golden và benchmark work chưa được authorize trong handoff
  hiện tại.
