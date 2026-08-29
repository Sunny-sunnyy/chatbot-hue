# Conditional Skill Routing Design

Date: `2026-08-29`
Status: approved by user

## Mục tiêu

Giữ `using-superpowers` làm router khi một session hoặc workflow chưa được xác
định, nhưng không bắt Reviewer hay Implementer khởi động lại generic routing
cho từng bước khi current handoff đã xác định đúng một role và next action.

Thay đổi này giảm context và ceremony không cần thiết mà vẫn giữ nguyên
`risk-gated-agent-review`, các nguyên tắc coding cốt lõi và independent review.

## Quyết định

### Routing boundary

`using-superpowers` được dùng khi:

- bắt đầu session mới và chưa có route rõ;
- role, objective hoặc loại workflow chưa rõ;
- yêu cầu mới làm thay đổi workflow đã chọn; hoặc
- task cần design mới, architecture, governance hay trade-off quan trọng.

Không bắt buộc dùng hoặc reload `using-superpowers` khi:

- current handoff đã có exact role và một next action;
- skill liên quan đã active trong cùng top-level task;
- đang thực hiện một step của approved plan;
- đang sửa exact correction delta; hoặc
- đang thực hiện mechanical approval closure.

Trong policy này, một top-level task là một objective hoặc một handoff series,
không phải từng tool call, plan step hay correction nhỏ.

### Reviewer

- Dùng `using-superpowers` và `brainstorming` cho `next_design` hoặc design chưa
  được giải quyết.
- Chỉ dùng `writing-plans` sau khi written design được user duyệt.
- Với `final_review` có Review Contract, đi thẳng vào risk-gated review và các
  technical skill thực sự liên quan.
- Chỉ quay lại brainstorming khi diff hoặc evidence cho thấy design flaw hay
  requirement mới.

### Implementer

- Với exact `implementation`, thực hiện approved plan; không brainstorm hoặc
  viết lại plan.
- Với exact `correction`, sửa delta trong một batch; chỉ dùng debugging workflow
  khi có bug thật hoặc root cause chưa rõ.
- Với exact `closure`, thực hiện contract cơ học; không khởi động design/test
  workflow không liên quan.
- Khi cần tìm hoặc load Superpowers skill phù hợp, tìm tại
  `~/.codex/skills/`.
- Trong repository hiện tại chỉ có hai project-local skills:
  `skills/risk-gated-agent-review/SKILL.md` và
  `skills/practical-project-coding/SKILL.md`.

Implementer dừng và trả lại Reviewer/user nếu yêu cầu mới làm đổi requirement,
architecture, provider/model, data contract, risk boundary hoặc authority.

## Context và tương thích

Exact handoff là routing decision của workflow dự án. Sau khi route đã rõ, agent
vẫn nạp context theo Tier 0–3 của `risk-gated-agent-review`; thay đổi này không
bỏ role validation, Review Contract, evidence gate hay stop condition.

Hai project skills giữ nguyên. Không thay đổi runtime, tests, datasets,
notebooks, Qdrant, evaluation artifacts hoặc phase scope.

## Acceptance criteria

1. Ba bootstrap behavior files không còn yêu cầu mọi task luôn khởi động bằng
   `using-superpowers`.
2. Reviewer routing phân biệt design chưa rõ với exact final review.
3. Implementer routing phân biệt implementation, correction và closure.
4. Skill đã active không bị yêu cầu reload trong cùng top-level task.
5. Gemini chỉ được hướng dẫn tìm/load Superpowers skills tại
   `~/.codex/skills/`; không liệt kê từng Superpowers skill path.
6. `session_prompt/brainstorming.md` chỉ bắt đầu routing ở design session mới.
7. `Project_Status.md`, hai project skills, runtime và `session_prompt_old/`
   không đổi.
