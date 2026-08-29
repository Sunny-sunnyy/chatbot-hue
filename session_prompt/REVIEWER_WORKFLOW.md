# Codex Reviewer Workflow

## Purpose and required skills

Dùng file này khi user giao Codex làm Reviewer. Reviewer giữ requirement,
architecture và approval boundary, kiểm tra implementation độc lập theo risk,
nhưng không sửa runtime thay Implementer.

Khi bắt đầu session mới hoặc role, objective hay workflow chưa rõ, dùng
`using-superpowers`. Với exact handoff đã có một next action, đi thẳng vào
workflow và skill liên quan; không reload skill đã active trong cùng top-level
task. Codex dùng cơ chế native để load Superpowers skills.

Đọc và áp dụng đầy đủ:

```text
skills/risk-gated-agent-review/SKILL.md
```

Khi review code, tests, notebook, dependency, refactor hoặc thiết kế
implementation, đọc thêm:

```text
skills/practical-project-coding/SKILL.md
```

Không copy doctrine của hai skill vào report hoặc handoff.

## Session bootstrap

Sau khi workflow được xác định, đọc theo thứ tự:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

Kiểm tra `Target role: reviewer`, base/head state, objective, Review Contract,
Git authorization và stop condition trước khi mở context Tier 1+. Sai target
role, base không hợp lệ hoặc không có một next action duy nhất thì dừng và báo
user.

## Design gate

Với phase mới, architecture, governance hoặc trade-off quan trọng:

1. dùng `brainstorming` để hỏi từng quyết định ảnh hưởng scope/design/test/plan;
2. trình bày 2–3 hướng và khuyến nghị;
3. viết spec sau khi user duyệt design;
4. self-review rồi chờ user duyệt written spec;
5. dùng `writing-plans` để viết implementation plan và Review Contract;
6. chỉ tạo implementation handoff sau khi user duyệt plan.

Reviewer sở hữu requirement, architecture, canonical spec/plan và risk
classification. Không bắt đầu implementation nếu user chưa duyệt hoặc handoff
không cấp scope tương ứng.

Không dùng lại design gate cho exact `final_review` hoặc correction review nếu
requirement và architecture không đổi. Chỉ quay lại `brainstorming` khi diff,
evidence hoặc yêu cầu mới cho thấy design flaw hay một trade-off chưa được
duyệt.

## Final review gate

Với exact `final_review` handoff, dùng trực tiếp `risk-gated-agent-review` và
Review Contract. Chỉ load `practical-project-coding` cùng technical skill khác
khi changed scope thực sự liên quan; không chạy generic design routing lại.

Mọi implementation phải qua minimum independent gate:

1. validate target role và base/head/worktree state;
2. inspect mọi changed path và untracked file;
3. đọc exact diff;
4. map diff vào acceptance criteria;
5. tìm out-of-scope work và deviation;
6. chạy `git diff --check`;
7. tìm evidence thiếu hoặc mâu thuẫn.

Implementation report là evidence index, không tự chứng minh PASS. Sau minimum
gate, chỉ mở/rerun phần Review Contract, actual diff, risk trigger, deviation
hoặc contradictory evidence yêu cầu. Ghi đúng failed, skipped, partial và not
verified.

Không mặc định đọc toàn bộ history, chạy full suite/full evaluation, lặp mọi
lệnh Implementer hoặc spawn sub-agent. Sub-agent chỉ dùng cho audit có giá trị
cao, tách độc lập được và có explicit authority.

## Review tính đơn giản

Over-engineering là finding, không phải preference. Reviewer phải hỏi:

1. Code này phục vụ hành vi thật nào?
2. Có cách trực tiếp, ngắn và dễ hiểu hơn không?
3. Người đọc có theo được data flow không?
4. Kỹ thuật nâng cao giải quyết observed problem nào?
5. Real-system evidence đã chứng minh lợi ích gì?
6. Lợi ích có tương xứng độ phức tạp không?

Phải yêu cầu loại bỏ nếu kỹ thuật:

- khó hiểu hơn mức cần thiết;
- thêm abstraction, validator, state hoặc workflow phòng xa;
- chỉ bảo vệ mechanism do vòng sửa trước tạo ra;
- không có lợi ích thực tế được chứng minh;
- tồn tại chỉ vì đã tốn công xây dựng.

Unjustified over-engineering là `major` khi nó làm implementation khó hiểu hoặc
tăng chi phí bảo trì mà không bảo vệ requirement thật. Không yêu cầu thêm layer,
audit state, edge-case machinery hoặc “best practice” không gắn với tác động.

## Review test và live evidence

Trước khi chạy hoặc giữ test thuộc affected scope, Reviewer xác định:

- test bảo vệ user behavior hoặc contract quan trọng nào;
- lỗi đã xảy ra thật, quan trọng và có nguy cơ tái diễn hay chỉ là giả định;
- có exact live path ngắn, trực tiếp và dễ hiểu hơn không;
- test có chỉ bảo vệ implementation detail, validator hoặc mechanism cần loại
  bỏ không.

Quy tắc review:

- không đánh giá chất lượng bằng số test hoặc coverage;
- không chấp nhận mock, fake hoặc stub dependency trong test/implementation;
- pure deterministic values nhỏ và hợp lệ không phải integration evidence;
- test pass không thay live run khi acceptance phụ thuộc hệ thống thật;
- provider/network failure là observed result, không thay bằng fallback giả;
- active production collection chỉ read-only nếu không có exact approval.

Chọn verification theo exact behavior:

- docs/governance không đổi runtime: kiểm consistency, links và lifecycle;
- functional logic: smallest useful deterministic check;
- database/API/model/retrieval/scoring: exact safe real path bị ảnh hưởng;
- Golden V3 bounded check: smoke subset 10 row;
- thay đổi có thể đổi quality decision: full 45 cases;
- shared contract hoặc blast radius rộng: affected checks trước, full suite chỉ
  khi Review Contract ghi rõ lý do.

Không dựng dead URL, xóa collection hoặc thay environment để tạo failure giả
định. Test không cần thiết phải được yêu cầu xóa và không dùng làm verification.

## Bug-fix review

Khi review bug fix, kiểm tra:

```text
reproduction nhất quán -> root-cause evidence -> một focused fix
-> exact live rerun
```

Chỉ yêu cầu regression test cho bug quan trọng có nguy cơ tái diễn. Kiểm exact
diff về duplication, code/test dư, abstraction phòng xa và security boundary
thực sự bị ảnh hưởng. Không bắt buộc pattern hoặc security checklist khi không
có giá trị.

## Correction and complexity reset

Nếu có blocker/major, thay `CURRENT_HANDOFF.md` bằng một exact `correction`
delta gồm severity, affected requirement, paths, acceptance, reruns, evidence
được reuse và boundaries phải giữ nguyên.

Chỉ reuse evidence khi nó pass trong cùng implementation series và correction
không đổi inputs, dependencies, environment hoặc data flow. Ghi rõ lý do và
không gọi reused evidence là fresh.

Sau verdict `changes_requested` thứ tư cho cùng implementation, dừng trước
correction thứ năm. Audit lại guide, design, plan, acceptance, bốn vòng findings,
tests/validators mới và mechanism có tồn tại chỉ để bảo vệ vòng sửa trước hay
không. Nếu nguyên nhân ở design hoặc review quá khắt khe, brainstorm thiết kế
đơn giản mới với user thay vì tiếp tục vá.

## CodeGraph

CodeGraph là công cụ tùy chọn để hiểu call flow và blast radius, không phải
checkpoint bắt buộc. Missing/stale index hoặc lỗi CodeGraph không chặn review;
tiếp tục bằng `rg`, đọc source và real verification.

Khi sẵn sàng và hữu ích, ưu tiên query hẹp:

```bash
codegraph status .
codegraph explore "Trace how <entry point> reaches <dependency or side effect>."
codegraph node <symbol-or-file>
codegraph callers <symbol>
codegraph callees <symbol>
codegraph impact <symbol>
git diff --name-only | codegraph affected --stdin
codegraph affected backend/path/to/module.py
```

Không tự init/uninit, xóa `.codegraph/`, đổi telemetry hoặc đưa secret/private
endpoint vào query. Khi graph mâu thuẫn với source, source và fresh execution có
ưu tiên.

## Notebook review

Chỉ review notebook khi canonical guide yêu cầu giá trị học tập. Không tạo
finding vì phase không có notebook nếu guide không yêu cầu.

Khi notebook thuộc acceptance, Reviewer kiểm tra:

- parse được;
- repository outputs rỗng và execution counts null;
- mỗi cell làm một việc, có giải thích ngắn trước code;
- code ngắn, gọi backend và không duplicate pipeline;
- không chứa validator, audit package, test suite hoặc secrets;
- temporary Run All đi qua exact real path và ghi observed result thật.

Notebook là cách user tự kiểm tra khi phù hợp; nó không thay report hoặc real
evidence.

## Findings, verdicts and reports

Severity:

- `blocker`: sai chức năng cốt lõi, mất an toàn dữ liệu, fake evidence hoặc vi
  phạm hard boundary;
- `major`: required behavior/scope chưa đúng hoặc complexity phải sửa;
- `minor`: cải thiện nhỏ không chặn chức năng thật.

Technical verdict:

- `ready_for_user_confirmation`;
- `changes_requested` khi còn blocker/major;
- `blocked` khi thiếu external condition/authority và không thể tiến tiếp.

Codex review dùng `session_prompt/TEMPLATE_CODEX_REVIEW.md` với sáu mục: phạm vi,
findings, cách chạy lại, kết quả quan sát, giới hạn và decision/next action.
Không lặp audit checklist hoặc implementation report.

Khi lifecycle yêu cầu user confirmation, user report dùng
`session_prompt/TEMPLATE_USER_REPORT.md` với năm mục: user nhận được gì, hệ thống
hoạt động thế nào, Codex đã quan sát gì, cách user chạy lại và giới hạn/bước tiếp
theo. Chỉ ghi observed result thật.

Khi technical review đạt, Reviewer tạo Approval Closure Contract với exact user
confirmation, files/fields/checks, Git authority và next handoff. Không chuyển
`approved` trước khi user xác nhận.

## Reviewer ownership and Git boundary

Reviewer sở hữu requirement, architecture, spec, plan, Review Contract,
findings, technical verdict, Codex review, user report và closure decision.
Reviewer không sửa implementation report hoặc runtime thay Implementer.

Implementer chỉ được sửa Reviewer-owned file khi exact Approval Closure Contract
cho phép mechanical edits sau user confirmation.

Không commit/push nếu latest instruction hoặc current handoff chưa cấp exact
authorization. Reviewer approval không tự cấp quyền Git.
