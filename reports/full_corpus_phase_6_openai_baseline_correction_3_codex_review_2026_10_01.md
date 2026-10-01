# Codex Review: Phase 6 OpenAI baseline — correction 3

Decision: changes_requested
Reviewer: Codex
Date: 2026-10-01 (+07)
Prior review: `reports/full_corpus_phase_6_openai_baseline_correction_2_codex_review_2026_10_01.md`
Implementation report: `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`

## 1. Independent non-paid observations

Reviewer đã inspect correction 3, chạy fresh non-paid gate và không gọi OpenAI,
không mutate Qdrant/corpus, không commit/push.

- Focused suite: `139 passed, 1 warning in 53.04s`.
- Metadata v2 complete verify: `VERIFIED` cho 33.840 points.
- Exact uvicorn từ `backend/`: `/health` HTTP 200, đủ 5 components `ready`;
  server được dừng sau kiểm tra.
- SDK/config: OpenAI 2.53.0, Agents 0.19.4, tiktoken 0.14.0, httpx 0.28.1;
  `gpt-5.4-nano`, retries 0, caps 2048/256, không sampling/reasoning override.
- Vendor hashes, notebook clean state và `git diff --check`: PASS.
- Static audit: không `last_chat_trace`, `logger.exception`, `str(exc)` hoặc
  provider-response mock/fake trong scoped Phase 6 tests.
- Prior ignored artifact vẫn nguyên trạng 5 attempts, status FAIL, 3 PASS/2
  FAIL. Reviewer không chạy paid runner.

## 2. Closure mapping P6-C2-R1..R3

| Finding | Kết luận correction 3 |
|---|---|
| P6-C2-R1 | Đóng phần shared-state/excerpts: `ContextVar` thay global trace và runner ghi full source metadata/excerpts. Còn provider-metadata edge case ở P6-C3-R1 |
| P6-C2-R2 | Code path chính đã sửa: early artifacts, null after-count và safe return. Acceptance regressions còn chưa kiểm actual finalizer ở P6-C3-R2 |
| P6-C2-R3 | Đã đóng: wording chính xác là không mock/fake provider response |

## 3. Findings còn lại

### P6-C3-R1 — major — provider metadata bị mất khi citation validation lỗi

- Vị trí: `backend/api/routes/chat.py:119-142`.
- Requirement: private ledger phải giữ response ID/model/latency/usage/finish
  metadata nếu SDK/provider thực sự trả, kể cả answer bị đánh FAIL sau đó.
- Evidence: route await `generate_answer()`, rồi gọi `select_cited_sources()`
  trong cùng `try`; `record_generation_success(generated)` chỉ chạy sau citation
  validation. Nếu generation thành công nhưng citation integrity fail,
  `record_error()` ghi category nhưng response ID/usage/finish metadata của
  provider đã trả không bao giờ vào recorder/artifact.
- Tác động: một paid attempt có provider response thật vẫn thiếu provenance,
  trái Review Contract và khó phân biệt provider failure với post-generation
  citation failure.
- Tiêu chí đóng: ghi generation metadata ngay sau successful provider return,
  trước citation validation; sau đó error status có thể override status nhưng
  phải giữ metadata. Thêm pure deterministic regression chứng minh sequence
  `generation metadata -> citation error` còn response ID/model/usage/finish.

### P6-C3-R2 — major — hai acceptance tests không chạy code integration được claim

- Vị trí: `backend/tests/test_phase6_live_smoke.py:239-253,286-361`.
- Evidence:
  - `test_run_smoke_after_count_failure...` chỉ tự dựng local `artifact` dict;
    nó không gọi runner, `write_atomic_artifact` hoặc shared artifact builder,
    nên vẫn pass nếu production code quay lại copy `before` thành `after`;
  - concurrency test chỉ gọi recorder trực tiếp và grounded-fallback test dùng
    `SamplePackedContext`; chưa test ContextVar truyền qua actual ASGI route và
    chưa test record do runner serialize. Vì vậy claim “artifact preserves
    excerpts when public sources empty” mới được chứng minh ở object mẫu, không
    ở integration boundary sẽ tiêu thụ paid call.
- Tác động: các regressions quan trọng có thể xanh trong khi wiring/finalizer
  thực tế hỏng.
- Tiêu chí đóng: tách artifact finalization/serialization thành pure production
  helper và test chính helper đó với after-count `None`; thêm non-paid
  ASGITransport integration dùng real retrieval/context nhưng chặn trước
  provider call (ví dụ generator not-ready) để chứng minh recorder nhận packed
  excerpts qua route, ContextVar reset, public response không lộ evidence và
  serialized call record giữ excerpts. Không mock/fake provider response.

## 4. Verdict và bước tiếp theo

Verdict: **CHANGES REQUESTED**.

Correction 3 đã giải quyết đúng kiến trúc shared state và phần lớn failure
handling; phạm vi còn lại nhỏ nhưng bắt buộc trước paid run. Không cấp quyền cho
replacement five-call sequence. Correction 4 chỉ được sửa P6-C3-R1..R2, không
paid call, không Qdrant/corpus mutation, không Git write và không sub-agent.
