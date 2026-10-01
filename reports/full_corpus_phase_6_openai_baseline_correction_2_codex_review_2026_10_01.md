# Codex Review: Phase 6 OpenAI baseline — correction 2

Decision: changes_requested
Reviewer: Codex
Date: 2026-10-01 (+07)
Prior review: `reports/full_corpus_phase_6_openai_baseline_correction_1_codex_review_2026_10_01.md`
Implementation report: `reports/full_corpus_phase_6_openai_baseline_implementation_2026_10_01.md`

## 1. Independent non-paid observations

Reviewer đã inspect toàn bộ correction paths và chạy lại gate mà không gọi
OpenAI, không mutate Qdrant/corpus và không commit/push.

- Focused suite: `130 passed, 1 warning in 41.51s`.
- Metadata v2 complete verify: `VERIFIED` cho 33.840 points.
- Exact uvicorn từ `backend/`: startup thành công; `/health` HTTP 200 với 5
  components `ready`; server được dừng sau kiểm tra.
- SDK/config construction-only: OpenAI 2.53.0, Agents 0.19.4, tiktoken 0.14.0,
  httpx 0.28.1; model `gpt-5.4-nano`, retries 0, caps 2048/256, không set
  temperature/top-p/reasoning/verbosity, `store=False`, usage enabled.
- Vendor hashes khớp pin; notebook có 8 cells/3 code cells, không output và
  execution counts đều `null`; `git diff --check` exit 0.
- Prior ignored live artifact vẫn nguyên trạng `FAIL`, đúng 5 attempts, 3 PASS/
  2 FAIL. Reviewer không chạy paid runner.

## 2. Closure mapping P6-C1-R1..R4

| Finding | Kết luận correction 2 |
|---|---|
| P6-C1-R1 | Đóng: runner quản lý app lifespan thật trên cùng event loop; regression và production startup đều PASS |
| P6-C1-R2 | Đóng: provider mocks/fakes đã được loại; structured parser có pure fail-closed tests |
| P6-C1-R3 | Đóng: default settings được resolve trong lifespan, production command hoạt động và raw cleanup payload đã bỏ |
| P6-C1-R4 | Chưa đóng: schema/logging tốt hơn, nhưng evidence vẫn ở shared app state, thiếu excerpts và failure persistence chưa fail-closed |

## 3. Findings còn lại

### P6-C2-R1 — blocker — replacement run không tạo evidence đủ để audit

- Vị trí: `backend/api/routes/chat.py:53-55,93-156` và
  `backend/llm/phase6_live_smoke.py:308-322`.
- Requirement: Review Contract bắt buộc manual claim/citation-to-excerpt audit
  cho ba grounded cases; prior correction yêu cầu per-call evidence theo scope
  request/runner, không dùng shared production state.
- Evidence: route vẫn ghi `last_chat_trace` lên global `app.state`. Reset/clear
  làm giảm stale data nhưng không biến nó thành request-scoped và vẫn race khi
  có request đồng thời. Trace chỉ chứa count/token/source IDs; runner vì vậy chỉ
  ghi IDs vào `packed_evidence`, không có packed source title/path/excerpts hoặc
  exact packed text. Với grounded fallback như `conditional_evidence`, public
  response có `sources: []`, nên artifact mới vẫn không thể chứng minh model đã
  thấy evidence nào hoặc audit claim/citation-to-excerpt.
- Tác động: đúng một paid replacement sequence có thể tiêu thụ hết 5 slots
  nhưng vẫn tạo artifact không nghiệm thu được; đây là blocker trước paid run.
- Tiêu chí đóng: loại `last_chat_trace` khỏi production shared state; dùng
  runner/request-scoped recorder để bắt đúng packed evidence được gửi cho từng
  real generation call. Ignored private artifact phải giữ đủ packed excerpts và
  safe source metadata cho cả success, fallback và error path; public envelope
  vẫn chỉ `{answer,sources}`. Thêm non-paid concurrency/isolation regression và
  structural test chứng minh artifact record có evidence audit được.

### P6-C2-R2 — major — atomic failure artifact chưa bao phủ và có thể ghi sai

- Vị trí: `backend/llm/phase6_live_smoke.py:138-180,226-237,361-364`.
- Evidence:
  - sau khi `confirm_paid=True`, missing/invalid case file tại lines 143-154 vẫn
    return mà không ghi artifact;
  - JSON/settings/before-count/checker failures xảy ra trước protected runner
    block và không được persist;
  - nếu after-count read thất bại, `write_atomic_artifact` gán
    `after_count = before_count`, biến trạng thái chưa xác minh thành bằng chứng
    point count bằng nhau;
  - unexpected runner error được ghi rồi re-raise, làm CLI phát traceback/raw
    exception thay vì kết thúc bằng safe typed failure.
- Tác động: ledger có thể mất hoặc báo immutability sai đúng tại failure path.
- Tiêu chí đóng: tạo minimal atomic artifact cho mọi exit sau paid confirmation;
  lưu after count là `null`/unverified khi không đo được, không suy diễn bằng
  before count; giữ attempted-call count trung thực; main kết thúc nonzero bằng
  safe category mà không re-raise raw traceback. Thêm pure/non-paid tests cho
  missing/invalid cases, health failure, after-count failure và unexpected
  exception.

### P6-C2-R3 — minor — báo cáo nói “0 mock trong toàn suite” quá rộng

- Vị trí: `session_prompt/CURRENT_HANDOFF.md` §§1/3 và implementation report
  §§3–4.
- Evidence: provider/generator correction tests không còn mock, nhưng focused
  suite vẫn gồm `test_full_corpus_metadata_v2.py`, nơi có nhiều `monkeypatch`
  deterministic cho CLI/filesystem paths.
- Tác động: không vi phạm provider hard boundary, nhưng statement hiện tại
  không đúng theo nghĩa literal.
- Tiêu chí đóng: ghi chính xác “không mock/fake provider response trong Phase 6
  acceptance tests”; không cần xóa các deterministic Metadata v2 tests.

## 4. Verdict và next action

Verdict: **CHANGES REQUESTED**.

Non-paid runtime gate khỏe hơn rõ rệt, nhưng chưa `ready_for_paid_authorization`.
Không cấp quyền cho replacement five-call sequence. Implementer cần correction
3 tối thiểu, chỉ xử lý P6-C2-R1..R3; không paid call, không Qdrant/corpus
mutation, không Git write và không sub-agent. Sau fresh independent review đạt,
Reviewer mới xin User authority cho đúng một replacement five-call sequence.
