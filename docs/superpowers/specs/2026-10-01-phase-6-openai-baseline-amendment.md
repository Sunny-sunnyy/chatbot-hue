# Phase 6 — OpenAI baseline amendment

**Date:** 2026-10-01 (+07)
**Status:** Approved by User
**Owner:** Codex Reviewer
**Implementation authorization:** Only through approved plan, Review Contract and `CURRENT_HANDOFF.md`
**Approval date:** 2026-10-01 (+07)

## 1. Mục đích

Amendment này đổi baseline sinh câu trả lời của Full-corpus Phase 6 từ
`qwen/qwen3.5-9b` qua OpenRouter sang OpenAI `gpt-5.4-nano`, nhằm dựng một
baseline ổn định trước khi đánh giá Qwen trong Phase 8.

Sau khi được User duyệt, amendment chỉ supersede các lựa chọn liên quan đến
model/provider, generation profile và bounded paid calls trong amendment ngày
2026-09-30. Các contract còn lại được giữ nguyên: Metadata v2, retrieval cell,
context packing nguyên chunk, citation/source integrity, API/UI, security,
private provisioning và acceptance dùng hệ thống thật.

Amendment này là tài liệu thiết kế, không sửa runtime và không tự cấp quyền cho
Implementation Plan hoặc `CURRENT_HANDOFF.md`. Hai artifact thực thi đó phải
được sửa, review và User duyệt ở bước riêng trước khi Implementer làm việc.

## 2. Baseline model contract đã duyệt

```text
Provider: OpenAI direct
SDK boundary: OpenAI Agents SDK for Python
Model: gpt-5.4-nano (floating alias; không khóa snapshot theo quyết định User)
Credential: OPENAI_API_KEY từ process environment
Reasoning effort: không cấu hình/không truyền; dùng mặc định của model/SDK
Temperature/sampling parameters: không cấu hình/không truyền; dùng mặc định
Application retry: none
Model fallback: none
Timeout: 45 seconds
Context limit used by Hue RAG packer: 16384 tokens
Reserved answer budget: 2048 tokens
Answer maximum output: 2048 tokens
Safety margin: 512 tokens
Representation B maximum output: 256 tokens
```

`context limit` ở đây là budget ứng dụng cố ý giữ nhỏ và cố định để bảo vệ
latency/cost và tạo điều kiện so sánh cùng điều kiện; nó không phải context
window tối đa của model. `reserved answer budget` vừa là phần chừa khi pack
context, vừa khớp exact answer output cap. Output cap, context budget, timeout,
structured output schema và số lần gọi vẫn phải explicit. Không thêm các
sampling/reasoning knobs không cần thiết vào baseline.

Nguồn chính thức để re-verify ngay trước implementation:
<https://developers.openai.com/api/docs/models/gpt-5.4-nano>. Project chủ ý dùng
alias `gpt-5.4-nano`, không pin snapshot. Availability, behavior mặc định, SDK
parameter support, pricing và limits phải được kiểm tra lại trước live run;
không tự chuyển sang snapshot hoặc model khác.

## 3. Generation boundary

- Reuse một tool-less `Agent`/`Runner` async và structured one-field
  `AnswerOutput`; Phase 6 không có tool, router, memory hoặc agent loop.
- Khởi tạo model/agent một lần trong application lifespan, không tạo lại theo
  request và không giữ credential trong source/log.
- Pipeline vẫn deterministic ở application layer:
  `retrieve -> pack context -> generate -> validate citations -> serialize`.
- Provider/model/structured-output failure trả typed error; không silent retry,
  đổi model hoặc trả partial success.
- Public success contract tiếp tục chỉ có `{answer, sources}`.

Exact API usage và dependency/version chỉ được khóa trong Implementation Plan
sau khi design này được duyệt và implementation surface được inspect lại.

## 4. Bounded live-evidence contract

Phase 6 tiếp tục có đúng năm paid generation attempts sau toàn bộ non-paid gate:

1. một Representation B call;
2. bốn answer-generation calls theo các case đã khóa trong plan sửa đổi.

Năm calls dùng alias `gpt-5.4-nano`. Phase 6 không gọi Qwen. Failure
không tự động mở call thứ sáu; mọi rerun phải được báo cáo và xin User duyệt.

Evaluation judge vẫn là `gpt-5.4-mini` và không được dùng làm generator fallback.
Judge calls thuộc evaluation phase/authorization riêng, không bị nhập vào năm
attempts của Phase 6.

## 5. Qwen là benchmark bắt buộc, không phải fallback

Qwen không bị loại khỏi dự án. Lifecycle đã duyệt:

```text
Phase 6: dựng và đóng GPT-5.4-nano technical baseline
  -> Phase 7: chạy/freeze full-corpus evaluation baseline
  -> Phase 8: so GPT-5.4-nano với qwen/qwen3.5-9b cùng điều kiện
  -> User chọn model/pipeline
  -> Phase 9 dùng winner đã được duyệt
```

So sánh Phase 8 phải giữ cùng questions/evidence, prompt, structured output,
context/output budgets và metric/judge trong phạm vi provider cho phép; khác
biệt bắt buộc phải được ghi rõ. Báo cáo tối thiểu quality, groundedness,
citation integrity, latency, reliability và cost. Không tự chuyển sang Qwen vì
GPT lỗi, không cho người dùng runtime chọn model và không promote winner nếu
chưa có User approval.

## 6. Những gì amendment không thay đổi

- Không thay đổi embedding, Qdrant collections, Metadata v2 hoặc corpus.
- Không thay đổi retrieval/fusion/reranker cell của Phase 6.
- Không thay đổi source/citation contract và frontend tối giản.
- Không thêm query rewrite, router, decomposition, conversation history,
  recommendation planner, web search hoặc weather tool; các phần này thuộc
  Phase 9 sau dependency gates.
- Không sửa Golden Dataset hoặc đặt threshold trước observed baseline.

## 7. Approval và bước tiếp theo

User đã duyệt design ngày 2026-10-01. Các bước chuẩn bị execution package đã
hoàn tất theo đúng thứ tự:

1. sửa Phase 6 Implementation Plan và Review Contract;
2. thay `CURRENT_HANDOFF.md` bằng handoff phù hợp;
3. rà consistency tài liệu trạng thái;
4. User đã duyệt exact execution package trước khi Implementer sửa code; paid
   calls vẫn chờ complete non-paid gate.

Package sửa đổi đã được User duyệt ngày 2026-10-01. Qwen handoff cũ không được
tiếp tục; execution authority chỉ nằm trong GPT handoff hiện hành.

Revised package đã được User duyệt tại:

```text
docs/superpowers/plans/2026-10-01-phase-6-openai-baseline-implementation-plan.md
handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
```
