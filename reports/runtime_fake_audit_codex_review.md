# Codex Review: Runtime Fake/Fallback Audit

Decision: accepted
Reviewer: Codex
Date: 2026-08-13
Review path:

```text
reports/runtime_fake_audit_codex_review.md
```

Implementer report:

```text
reports/runtime_fake_audit_implementation_report.md
```

## Tóm Tắt

Audit production xác nhận fake/mock chỉ nằm trong `backend/tests/`; runtime
không có fake fallback hoặc real-mode guard sai contract. Sửa `_usage_tokens()`
đúng SDK 0.19.4 trên path bình thường: live evidence ghi `tokens=421/48`, thay
vì `unknown`.

Initial review tìm thấy một edge case telemetry: usage object thiếu token field
từng trả chuỗi `None/None`. Implementer đã xử lý theo đúng contract và phần
Correction Re-review bên dưới ghi validation acceptance.

## Findings

- resolved minor: `_usage_tokens()` từng coi một usage object thiếu
  `input_tokens` hoặc `output_tokens` là valid. Probe initial review:

  ```text
  _usage_tokens(SimpleNamespace(raw_responses=[SimpleNamespace(
      usage=SimpleNamespace()
  )])) == "None/None"
  ```

  Contract yêu cầu `"unknown"`. Correction đã bỏ qua entry thiếu field, tiếp
  tục tìm entry kế tiếp hợp lệ, rồi trả `unknown` nếu không có entry hoàn chỉnh.

Không có blocker hoặc major finding.

## Verification

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest \
  tests/test_llm_generator_openai.py -q --tb=short
# 26 passed (initial review, trước correction)

UV_CACHE_DIR=/tmp/uv-cache uv run python -c "... _usage_tokens usage object thiếu fields ..."
# None/None (reproduced trước correction)

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# 272 passed, 1 StarletteDeprecationWarning (trước correction)

codegraph callers _usage_tokens
codegraph impact _usage_tokens
# Chỉ ảnh hưởng generator logging và tests liên quan.
```

Reviewer không gọi lại OpenAI. Live evidence `421/48` trong implementation
report đủ xác nhận normal SDK path sau fix.

## Scope Check

Audit giữ đúng scope: runtime, tests telemetry và technical reports. Fake/mock
trong tests được giữ lại đúng purpose offline deterministic. Không có mutation
Qdrant, OpenRouter, notebook, guide, status, commit hoặc push trong
implementation audit.

## Safety And Quality Check

- Security: không có key, raw provider payload hoặc prompt được lưu.
- Data safety: telemetry chỉ log token summary; failure/partial usage không được
  phép fabricate.
- Reliability: normal SDK usage path đạt; partial usage edge case được resolved
  trong Correction Re-review.
- Performance: sửa chỉ ở logging path, không thay request flow.
- Tests: initial review có 272 tests; correction bổ sung coverage missing-field
  và partial-before-complete, đạt 28 targeted / 274 full backend tests.
- Evaluation: không có benchmark claim mới.

## Required Changes

Completed in the correction re-review below: partial usage is skipped, tests
cover the edge cases, and the implementer ran targeted/full tests plus
`git diff --check`. No additional live OpenAI call was needed.

## Correction Re-review (2026-08-13)

Implementer đã sửa đúng finding mà không mở rộng scope: chỉ entry có cả
`input_tokens` và `output_tokens` mới được format; entry partial bị skip và
không có entry đầy đủ trả `unknown`.

Reviewer xác nhận độc lập:

```text
usage object không có token fields -> unknown
partial entry, rồi complete entry 421/48 -> 421/48
```

`tests/test_llm_generator_openai.py` đạt 28 passed. Implementer evidence ghi
full backend suite 274 passed, một `StarletteDeprecationWarning`, `git diff
--check` clean và CodeGraph up to date. Không cần live OpenAI call mới vì sửa
chỉ xử lý missing telemetry fields; live normal path `421/48` đã có evidence.

## User Confirmation Readiness

Audit addendum được accepted và không mở hoặc đóng Phase 7. Phase 6 giữ trạng
thái chờ user confirmation; correction telemetry không còn là điều kiện chặn
technical verdict.
