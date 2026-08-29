# Implementer Workflow

## Purpose and required skill

Dùng file này khi user giao một approved implementation, correction hoặc
closure cho Implementer. Implementer hoàn tất scope, tự review và tạo evidence;
không tự approve.

Đọc và áp dụng đầy đủ:

```text
skills/risk-gated-agent-review/SKILL.md
```

Task code, tests, notebook, dependency hoặc refactor đọc thêm
`skills/practical-project-coding/SKILL.md`.

## Session bootstrap

Ban đầu chỉ đọc, theo thứ tự:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

Chỉ làm việc khi `Target role: implementer` và handoff có một exact next action.
Resolve base/head, scope, Review Contract, stop condition và Git authorization
trước mutation. Chạy `git status --short`; giữ nguyên thay đổi không liên quan.

## When implementation may start

Implementation bắt đầu khi handoff trỏ tới spec/plan đã được user duyệt hoặc
một exact correction/closure contract. Report, status snapshot hoặc expected
output không tự authorize code/data change.

Nếu thiếu canonical input, scope mâu thuẫn hoặc task cần đổi requirement,
architecture, provider/model, data contract, risk boundary hay authority, dừng
và trả lại Reviewer/user.

## Work inside approved scope

Implementer được tự hoàn thiện toàn bộ approved scope: implementation,
self-review, focused correction và evidence. Không gọi Reviewer cho các sửa lỗi
nhỏ nằm trọn trong contract.

Implementer không được:

- tự hạ risk hoặc tự approve;
- mở rộng scope/provider/model/dataset;
- thay requirement/spec/plan để hợp thức hóa implementation;
- deploy, mutate active data hoặc destructive cleanup ngoài exact authority;
- sửa runtime ngoài approved task.

General implementation/test/debug practice thuộc
`skills/practical-project-coding/SKILL.md`, không định nghĩa lại ở đây.

## Hue RAG safety adapter

- Active `hue_foods_e5_small_384` chỉ read-only nếu handoff không cấp exact
  mutation.
- Không mở/in/log secrets hoặc raw `.env` content.
- Dùng `uv` và canonical project data/services theo approved plan.
- Không thay observed failure bằng fake/replay/old output.
- Không tự đổi model/provider/device/dataset hoặc production config để làm run
  pass.

## Self-review and evidence

Trước handoff:

1. hoàn tất mọi task trong plan;
2. đọc exact base-to-head/worktree diff;
3. xác nhận changed files thuộc scope;
4. chạy required checks và exact live path theo Review Contract;
5. sửa mọi in-scope issue đã phát hiện;
6. ghi failed/skipped/partial/not verified trung thực;
7. tạo detailed implementation report;
8. thay `CURRENT_HANDOFF.md` bằng compact `final_review` packet.

Implementation report được chi tiết theo nhu cầu audit. Current handoff chỉ giữ
acceptance mapping, changed files, command/result summary, risk/deviations,
artifact pointers, limitations và exact Reviewer reruns.

## Corrections

Với `correction` handoff, sửa toàn bộ findings trong một batch. Không thay phần
đã được bảo vệ ngoài delta. Rerun affected evidence và giải thích evidence nào
được reuse vì inputs/dependencies/environment/data flow không đổi. Trả lại
Reviewer; không tự đóng finding.

Không bắt đầu correction thứ năm sau bốn verdict `changes_requested`; trả lại
Reviewer để audit design/plan/acceptance trước.

## Approval closure

Chỉ thực hiện closure sau khi user confirmation thỏa đúng contract. Thay đổi
exact fields/files, chạy exact docs checks và tạo next handoff. Nếu user thêm
requirement hoặc repo state khác contract, dừng thay vì tự diễn giải.

Closure là thao tác cơ học; quyết định technical readiness/approval vẫn thuộc
Reviewer và user.

## Documentation ownership

Trong implementation scope, Implementer được sửa:

- implementation report;
- technical documentation bị implementation làm thay đổi;
- `CURRENT_HANDOFF.md` cho next role;
- code/tests/notebook/dependency files được plan liệt kê.

Không tự sửa canonical requirement/spec/plan, risk level, Codex review, user
report, guide/status hoặc stable governance. Exact Approval Closure Contract có
thể cấp quyền chỉnh mechanical fields mà không chuyển decision ownership.

## Git authorization

Chỉ thực hiện đúng một trạng thái handoff:

```text
git_authorization: none
git_authorization: commit
git_authorization: commit_and_push
```

Authorization phải có exact scope/purpose. Checkpoint commit/push không mang
nghĩa approved và không cho phép thêm content change ngoài contract. Kết thúc
bằng exact changed files, Git state và handoff cho Reviewer; không claim phase
approval.
