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

Reviewer research và brainstorming exact Notebook 08c reranker benchmark trên
fixed pre-rerank inputs. Trước tiên phải đọc canonical Phase 8 guide cùng
existing high-level 08c design context, kiểm tra current reranker library/model
compatibility và trình bày các trade-off cần user quyết định.

Không được bắt đầu implementation, benchmark run, model download mới, paid API,
active Qdrant mutation, production cutover hoặc sửa Golden V3 trong handoff này.

## 3. Design gate

Reviewer phải:

1. xác nhận exact 08c scope và dependencies từ current repo/live environment;
2. brainstorm các quyết định ảnh hưởng candidates, fixed inputs, metrics,
   resource limits và acceptance;
3. trình bày 2–3 hướng cùng khuyến nghị;
4. chỉ viết exact spec sau user duyệt design;
5. chỉ viết implementation plan/Review Contract sau user duyệt spec;
6. chỉ tạo Implementer handoff sau user duyệt plan.

## 4. Boundaries phải giữ

- Reuse approved Golden V3 45 full + 10 smoke cases.
- 08b artifacts là immutable evidence; không chọn sparse finalist sau approval.
- Active `hue_foods_e5_small_384` read-only.
- Không silent fallback, fake provider/data hoặc đổi experiment inputs để tạo
  winner.
- Phase 8 và 08c implementation/run vẫn chưa authorized.
- Git authorization là `none` cho next-design work.
