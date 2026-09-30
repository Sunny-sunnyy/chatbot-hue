# Bàn giao triển khai — Full-corpus Phase 6 trên Metadata v2

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: e91ff56611cde9b0ac569e537bdb6c1afc8f8b60
Head commit: worktree
Risk level: high
Git authorization: none
Sub-agent authorization: none

User đã duyệt Phase 6 Metadata v2 amendment, Implementation Plan và Review
Contract ngày 2026-09-30. Handoff này cấp đúng một implementation scope; không
tự mở Phase 7, cleanup, migration khác hoặc Git write.

## 1. Nhiệm vụ tiếp theo duy nhất

Thực hiện tuần tự toàn bộ plan hiện hành:

```text
docs/superpowers/plans/2026-09-30-phase-6-full-corpus-generation-api-ui-metadata-v2-implementation-plan.md
```

Mục tiêu là đưa canonical Metadata v2 retrieval qua evidence-only context,
Qwen/OpenRouter generation, strict citation/API contract và static UI. Kết thúc
khi implementation, required evidence và report hoàn tất, rồi chuyển handoff về
Reviewer với `Handoff kind: final_review`.

## 2. Canonical inputs

Đọc đúng read levels và thứ tự trong mục `Canonical inputs` của plan. Các nguồn
authority chính:

```text
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/Session_Prompt.md
session_prompt/CURRENT_HANDOFF.md
docs/superpowers/specs/2026-09-30-phase-6-full-corpus-generation-api-ui-amendment.md
docs/superpowers/plans/2026-09-30-phase-6-full-corpus-generation-api-ui-metadata-v2-implementation-plan.md
docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md
docs/superpowers/plans/2026-09-14-phase-6-full-corpus-generation-api-ui-implementation-plan.md
```

Plan ngày 2026-09-30 ưu tiên cho lifecycle, Metadata v2 delta, exact paths,
verification và quyền. Package ngày 2026-09-14 chỉ cung cấp behavior/component
body mà plan mới giữ nguyên.

## 3. Boundary và authority

- Chỉ tạo/sửa các path trong `Planned file map` của plan.
- Giữ nguyên staged deletion/private-corpus transition và mọi dirty-worktree
  thay đổi có trước handoff; không restore, stage hay hoàn tác chúng.
- `knowledge-base-hue/`, Metadata v2 build records, bốn legacy và bốn
  metadata-v2 collections đều immutable/read-only.
- Không mock/fake/stub/replay provider hoặc dependency thật.
- Không commit/push. Không dùng sub-agent.
- Không chạy Qwen call trước khi toàn bộ non-paid gate PASS.
- Paid runner chỉ có đúng năm attempts theo exact command trong Task 6; attempt
  lỗi vẫn tính, không rerun và không có attempt thứ sáu.
- Không đưa question set, corpus text/path, answer/excerpt, payload/trace, secret
  hoặc raw provider error vào tracked artifact.

Nếu private prerequisite thiếu/stale, focused check fail, asset/hash lệch,
worktree overlap không bảo toàn được, cần collection mutation/model change hoặc
cần call thứ sáu: dừng và báo đúng observed blocker.

## 4. Required outputs và return handoff

Required outputs là code/config/tests/UI/notebook, ignored private live-case và
live-evidence JSON, cùng report:

```text
reports/full_corpus_phase_6_generation_api_ui_implementation_2026_09_30.md
```

Trước khi trả task, thực hiện self-review và command ledger đúng Task 6. Sau đó
thay file này bằng concise handoff có:

```text
Target role: reviewer
Handoff kind: final_review
Git authorization: none
Sub-agent authorization: none
```

Handoff cuối phải ghi base/head, complete changed/untracked inventory,
acceptance/evidence map, exact commands/results, ignored evidence path,
implementation report, failures/limits và một next action duy nhất: independent
Phase 6 final review. Không tự claim Phase 6 approved hoặc completed.
