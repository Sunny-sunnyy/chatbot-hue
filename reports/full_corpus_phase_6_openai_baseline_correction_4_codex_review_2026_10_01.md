# Codex Review: Phase 6 OpenAI baseline — correction 4

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-10-01 (+07)
Prior review: `reports/full_corpus_phase_6_openai_baseline_correction_3_codex_review_2026_10_01.md`
Implementation report: `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`

## 1. Independent non-paid observations

Reviewer đã inspect correction 4 và chạy lại toàn bộ non-paid gate. Không gọi
OpenAI, không chạy paid runner, không mutate Qdrant/corpus và không commit/push.

- Focused suite: `141 passed, 1 warning in 54.91s`.
- Metadata v2 complete verify: `VERIFIED` cho 33.840 points.
- Exact uvicorn từ `backend/`: `/health` HTTP 200 với 5 components `ready`;
  server được dừng sau kiểm tra.
- SDK/config construction-only: OpenAI 2.53.0, Agents 0.19.4, tiktoken 0.14.0,
  httpx 0.28.1; model `gpt-5.4-nano`, retries 0, caps 2048/256, không set
  temperature/top-p/reasoning/verbosity.
- Vendor hashes khớp pin; notebook có 8 cells/3 code cells, không output và mọi
  execution count `null`; `git diff --check` exit 0.
- Static audit: không `last_chat_trace`, `logger.exception` hoặc `str(exc)` ở
  production correction paths; public API vẫn `{answer,sources}`.
- Prior ignored artifact vẫn là five-call ledger cũ: 3 PASS/2 FAIL, overall
  FAIL. Reviewer không sửa hoặc chạy lại artifact này.

## 2. Closure mapping

### P6-C3-R1 — CLOSED

`backend/api/routes/chat.py` ghi provider metadata bằng
`record_generation_result()` ngay sau `generate_answer()` thành công và trước
`select_cited_sources()`. Citation failure chỉ đổi status/error, không xóa
response ID/model/latency/usage/finish metadata. Pure deterministic regression
kiểm đủ sequence này và PASS.

### P6-C3-R2 — CLOSED

Runner dùng production helpers `build_live_smoke_artifact()` và
`serialize_call_evidence()`. Test gọi trực tiếp artifact helper xác nhận
after-count `None` giữ `null`, đánh `point_count_intact=false` và thêm
`point_count_unverified`. Fresh suite cũng chạy actual FastAPI route qua
ASGITransport với real Qdrant retrieval/context, chặn ở real generator-not-ready
branch trước provider call; recorder nhận non-empty excerpts, ContextVar reset,
app state sạch, public response không lộ evidence và runner serializer giữ
excerpts.

## 3. Architecture and risk conclusion

Request-scoped `ContextVar` thay global mutable trace là phù hợp cho runner tuần
tự hiện tại và an toàn trước task concurrency đã test. Private evidence chỉ đi
vào ignored artifact; production response/state không giữ packed corpus. Atomic
failure ledger và Qdrant immutability checks hiện fail closed.

Không còn blocker/major/minor finding mở trong non-paid scope. Warning duy nhất
là Starlette deprecation về TestClient/httpx, không ảnh hưởng Phase 6 acceptance
và không cần dependency migration trong paid correction boundary này.

## 4. Verdict

Verdict: **READY FOR USER CONFIRMATION**.

Đây chưa phải Phase 6 final PASS. User cần cấp authority riêng cho đúng một lần
replacement sequence gồm tối đa 5 attempted OpenAI calls: một Representation B
và bốn answer cases. Mọi request attempted đều tính kể cả failure; không retry,
không lần chạy thứ hai và không call thứ sáu. Nếu runner dừng sớm hoặc overall
FAIL, giữ artifact và quay lại review, không tự rerun.

## 5. User authorization status

User đã cấp explicit authority ngày 2026-10-01 cho đúng bounded invocation nêu
trên và yêu cầu hoãn execution sang phiên tiếp theo. Authority chưa được tiêu
thụ. `session_prompt/CURRENT_HANDOFF.md` giữ exact command, approval fingerprint,
preflight/stop conditions và post-run handoff cho Implementer ngày mai.
