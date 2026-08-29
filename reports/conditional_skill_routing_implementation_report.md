# Implementation Report: Conditional Skill Routing

Implementer: Codex theo direct user authorization
Date: `2026-08-29`
Canonical design:

```text
docs/superpowers/specs/2026-08-29-conditional-skill-routing-design.md
```

## 1. Phạm vi

Thay unconditional “mỗi task bắt đầu bằng `using-superpowers`” bằng conditional
routing theo session, role và exact handoff. Correction chỉ sửa shared session
policy, hai role workflow, design prompt, amendment/plan, report và current
handoff.

Không sửa hai project skills, `Project_Status.md`, runtime, tests, datasets,
notebooks, Qdrant, evaluation artifacts hoặc `session_prompt_old/`.

## 2. Thay đổi chính

- `Session_Prompt.md` định nghĩa top-level task, các điều kiện route/re-route và
  exact handoff như một routing decision đã hoàn thành.
- `REVIEWER_WORKFLOW.md` phân biệt design gate với exact final/correction
  review.
- `IMPLEMENTER_WORKFLOW.md` đi thẳng vào approved implementation, correction
  hoặc closure; không brainstorm hay viết lại plan khi requirement không đổi.
- Gemini được hướng dẫn tìm/load Superpowers skill phù hợp tại
  `~/.codex/skills/`. Hai project-local skills trong repository được nêu rõ.
- `brainstorming.md` chỉ dùng `using-superpowers` khi bắt đầu design session mới
  hoặc workflow chưa rõ.

## 3. Cách đã chạy thật

Đã chạy các kiểm tra documentation-only sau:

```bash
rg -n 'Mỗi task bắt đầu|Luôn bắt đầu bằng' \
  session_prompt/Session_Prompt.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md \
  session_prompt/brainstorming.md

rg -n 'session mới|exact `implementation`|exact `final_review`|Handoff routing|Không reload|không reload|~/.codex/skills/|project-local skills' \
  session_prompt/Session_Prompt.md \
  session_prompt/REVIEWER_WORKFLOW.md \
  session_prompt/IMPLEMENTER_WORKFLOW.md \
  session_prompt/brainstorming.md

test -f <từng project/Superpowers skill được tham chiếu>
git diff --check
git status --short
git diff --name-only -- skills backend evaluation notebooks knowledge-base-hue session_prompt_old
```

Đã quét trailing whitespace trên toàn bộ tám file thuộc correction. Một
trailing space trong `brainstorming.md` được phát hiện và xóa trước handoff;
fresh final scan không còn match.

## 4. Kết quả quan sát

- Không còn match cho hai câu unconditional trong bốn active behavior files.
- Conditional routing, exact handoff routing và Gemini skill root đều xuất hiện
  ở đúng role/shared owner.
- Tất cả project/Superpowers skill paths được tham chiếu đều tồn tại.
- `git diff --check` exit `0`.
- Protected-path diff cho skills, runtime, evaluation, notebooks, curated data
  và `session_prompt_old/` rỗng.
- Worktree chỉ có bốn behavior files đã sửa, hai amendment files mới, report và
  current handoff của correction này; `session_prompt_old/` vẫn là untracked
  context không liên quan.

## 5. Lỗi và giới hạn

Không chạy backend tests, notebook, model, Qdrant hoặc live API vì correction
không đổi product runtime.

## 6. Handoff cho Reviewer

Reviewer đọc design amendment, implementation plan và exact worktree diff. Chạy
lại unconditional/conditional routing scans, path checks, protected-path diff,
trailing-whitespace scan và `git diff --check`. Kiểm bốn scenario:

1. session design mới route qua `using-superpowers` và `brainstorming`;
2. exact implementation không brainstorm hoặc viết lại approved plan;
3. exact final review đi thẳng vào Review Contract;
4. role/objective/requirement thay đổi thì route lại.

User đã authorize commit và push exact conditional-routing correction sau
implementation handoff. `session_prompt_old/` không thuộc commit scope.
