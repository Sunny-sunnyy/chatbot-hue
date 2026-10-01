# Phase 6 OpenAI Baseline — Implementation Review Contract

**Date:** 2026-10-01 (+07)
**Status:** User-approved
**Owner:** Codex Reviewer
**Approved by:** User
**Approval date:** 2026-10-01 (+07)
**Risk level:** High
**Execution authorization:** Only through `session_prompt/CURRENT_HANDOFF.md`

Contract này đi cùng:

```text
docs/superpowers/specs/2026-10-01-phase-6-openai-baseline-amendment.md
docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md
```

Nó override các mục Qwen/OpenRouter trong Review Contract nhúng ở plan
2026-09-30. Các gate Metadata v2, corpus/Qdrant immutability, citation/API/UI,
private evidence và User closure vẫn giữ nguyên.

## Evidence Implementer phải cung cấp

- base/head/worktree và complete changed/untracked inventory;
- exact diff cùng mapping vào approved spec + revised plan;
- non-paid command ledger với observed exit/result;
- fresh Metadata v2 complete verify và Qdrant counts trước/sau;
- model alias, tiktoken encoding, Agents SDK/OpenAI versions và exact
  generator configuration;
- bằng chứng không gửi temperature/reasoning/sampling/verbosity overrides;
- bằng chứng client `max_retries=0`, Runner `max_turns=1`, tracing disabled;
- startup, cached health, strict API và static UI observations;
- ignored/private JSON ledger của đúng năm attempted GPT calls: one
  Representation B + four answers;
- response ID, model, latency, usage/finish metadata nếu SDK/provider thực sự
  trả; field không có phải ghi `null`, không tạo request bổ sung;
- manual claim/citation-to-excerpt audit cho ba grounded cases;
- out-of-scope fallback audit;
- implementation report, failures, skipped và not-live-verified branches.

Không đưa secrets, raw provider errors, fixed questions, answers, excerpts,
private source paths/payloads/trace vào tracked report/handoff.

## Independent Reviewer minimum gate

Reviewer phải:

1. xác nhận authority, base/head và mọi changed/untracked path;
2. đọc full revised diff và map vào spec/plan;
3. chạy `git diff --check`;
4. chạy focused non-paid settings/tokenizer/context/citation/generator/API/UI/
   retrieval tests;
5. kiểm installed SDK signatures và generator construction không gọi mạng;
6. xác nhận alias `gpt-5.4-nano`, `o200k_base`, reasoning/sampling fields không
   được cấu hình hoặc truyền vào request,
   `max_retries=0`, `max_turns=1` và caps 2048/256;
7. start real read-only API, kiểm `/health` và không gửi paid request;
8. kiểm static asset hashes, sanitization và keyboard citation behavior;
9. inspect ignored five-attempt artifact, đếm attempts và audit citation/excerpt;
10. xác nhận không Qwen/OpenRouter generation import/call, không private-field
    leak và không corpus/Qdrant mutation.

Reviewer có thể reuse exact five-attempt artifact khi timestamp, config, count
và safe metadata nhất quán. Reviewer không tự chạy paid call bổ sung.

## Stop conditions

Dừng ngay trước paid runner nếu:

- User chưa duyệt revised plan/contract hoặc GPT handoff chưa active;
- private corpus/build records/Metadata v2 targets không ready;
- source/build hashes, point counts hoặc schema lệch;
- exact model/tokenizer/assets không resolve;
- focused checks chưa PASS hoặc worktree overlap không bảo toàn được;
- public output có thể lộ path, trace, ID, `chunk_id`, `domain`, score, secret
  hoặc raw provider error;
- cần collection mutation, provider/model change, retry hoặc attempt thứ sáu.

Nếu OpenAI call fail, ghi observed FAIL/incomplete. Không retry, đổi alias,
chuyển Qwen, dùng judge model hoặc tạo fabricated evidence.

## Acceptance verdict

Reviewer chỉ dùng một trong các verdict:

```text
PASS
PASS WITH LIMITATIONS
CHANGES REQUESTED
BLOCKED BY OBSERVED EXTERNAL CONDITION
```

`PASS` hoặc `PASS WITH LIMITATIONS` chỉ tạo
`ready_for_user_confirmation`. Reviewer phải viết review report và Approval
Closure Contract; chỉ User confirmation mới đóng Phase 6.

## Git và scope boundary

- Git authorization: none.
- Sub-agent authorization: none.
- Corpus/Qdrant mutation authorization: none.
- Paid-call authorization: chỉ exact bounded runner sau non-paid gate, và chỉ
  khi GPT Implementer handoff tương lai ghi rõ quyền này.
- Không mở Phase 7/8/9, model benchmark, router, memory, web hoặc tool work.
