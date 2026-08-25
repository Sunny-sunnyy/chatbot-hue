# Codex Review: Phase 4–5 Qdrant & Retrieval Simplicity

Decision: ready_for_user_confirmation
Review round: correction revision 2
Reviewer: Codex
Date: 2026-08-25 +07
Canonical guides: `guides/phase_4_qdrant_ingestion.md`, `guides/phase_5_retrieval_profiles_reranking.md`
Implementation report: `reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md`

## 1. Phạm vi đã review

Đã review exact Revision 2 diff của BM25/ContextBuilder tests và per-test audit,
đồng thời giữ fresh Revision 1 evidence cho runtime/notebooks không đổi. Reviewer
chạy lại focused retained suite, full non-paid backend suite, scoped
diff/compilation checks và final read-only Qdrant safety probe.

## 2. Findings

Không còn blocker hoặc major.

### `minor` — Implementation report còn hai sai lệch evidence nhỏ

- Report ghi `test_evaluation.py (8 tests)` nhưng source và chính danh sách bên
  dưới có 9 tests.
- Report chưa ghi fresh focused/full suite counts. Implementer handoff nói
  `27/91`, nhưng exact canonical selector Reviewer chạy quan sát
  `27 passed` focused và `90 passed, 6 deselected` full. Sáu deselected là ba
  tests trong `TestChatSuccess` cộng answer evaluation, live generator và
  sensitive-response paid tests; tổng collected vẫn là 96.

Hai sai lệch chỉ thuộc implementation report, không ảnh hưởng runtime, data
safety hoặc technical decision. Nên sửa khi chuẩn hóa report cuối; Reviewer
không sửa implementation report thay Implementer.

## 3. Cách Reviewer chạy lại thật

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase45-review-r2-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_ingestion_pipeline.py tests/test_bm25.py \
  tests/test_retrieval_service.py tests/test_context_builder.py -q --tb=short -s

UV_CACHE_DIR=/tmp/hue-rag-phase45-review-r2-uv-cache uv run --env-file ../.env \
  python -m pytest tests -q --tb=short \
  -k 'not TestChatSuccess and not test_answer_evaluation_calls_real_generation_and_judge_models and not test_live_generate_answer_success and not test_no_sensitive_payload_in_responses'
```

Reviewer cũng chạy `py_compile`, scoped `git diff --check`, đọc source/audit từng
affected test và probe read-only exact configured collection, candidate count và
guarded leftovers. Revision 1 đã Run All độc lập Notebook 03–05 và chạy
active/candidate startup/search thật; Revision 2 không đổi các files đó.

## 4. Kết quả quan sát

- BM25: 4 behavior tests rõ ràng cho Vietnamese tokenization, fit/ranking,
  normalization và weights.
- ContextBuilder: 4 behavior tests rõ ràng cho budget/document cap,
  structural/source mapping, empty handling và non-mutation.
- Focused suite: `27 passed, 1 warning in 131.97s`.
- Full non-paid suite: `90 passed, 6 deselected, 19 warnings in 337.52s`.
- Active config vẫn là `hue_foods_e5_small_384`, profile `dense_only`.
- Active và candidate đều 572 points; không có `hue_rag_live_test_` leftovers.
- Stored comparison artifacts giữ 104/104 exact ordered-ID parity cho cả ba
  profiles; retrieval code không đổi trong Revision 2.
- Revision 1 fresh evidence: active/candidate startup/search pass; Notebook 03,
  04 và 05 Run All pass; repository notebooks sạch outputs/counts.
- Scoped compilation và diff whitespace checks pass.

Warnings đều là dependency deprecation/compatibility warnings đã biết; không có
failed hoặc skipped runtime behavior bị che.

## 5. Giới hạn hoặc phần chưa chạy

Không chạy paid generation/judge/chat tests vì Phase 4–5 không đổi generation và
approved plan yêu cầu deselect. Không chạy lại 104 × 3 hoặc notebooks trong
Revision 2 vì exact changes chỉ thuộc test consolidation/report; fresh Revision
1 evidence vẫn áp dụng.

## 6. Decision và bước tiếp theo

Decision là `ready_for_user_confirmation`. Phase 4–5 giữ `under_review` cho tới
khi user đọc user report và Run All notebooks nếu muốn xác minh trực tiếp.

Candidate chưa thành active. Sau user confirmation, config cutover sang
`hue_foods_e5_small_384_dense` vẫn cần một approval rõ riêng. Active collection
cũ phải được giữ read-only làm rollback; cleanup cần approval khác. Không commit
hoặc push.
