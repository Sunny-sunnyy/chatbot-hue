# Implementer Workflow

## Purpose and required skills

Dùng file này khi user giao approved implementation, correction hoặc closure
cho Implementer. Implementer hoàn tất scope, tự review và tạo evidence; không
tự approve.

Khi bắt đầu session mới hoặc role, objective hay workflow chưa rõ, dùng
`using-superpowers`. Với exact `implementation`, `correction` hoặc `closure`
handoff, đi thẳng vào workflow và skill liên quan; không reload skill đã active
trong cùng top-level task.

Khi Implementer Gemini cần tìm hoặc load Superpowers skill phù hợp, tìm tại:

```text
~/.codex/skills/
```

Luôn đọc và áp dụng project coordination skill:

```text
skills/risk-gated-agent-review/SKILL.md
```

Task liên quan code, tests, notebook, dependency, debug hoặc refactor đọc thêm:

```text
skills/practical-project-coding/SKILL.md
```

`risk-gated-agent-review` điều phối scope, handoff, evidence, correction và
closure. `practical-project-coding` áp dụng cho code, tests, notebook,
dependency, debug và refactor. Trong repository hiện tại chỉ có hai
project-local skills nêu trên. Các Superpowers skill khác chỉ load khi exact
handoff, approved plan hoặc conditional routing xác định chúng phù hợp; không
tự dùng sub-agent nếu user hoặc Review Contract chưa cho phép.

## Session bootstrap

Sau khi workflow được xác định, đọc theo thứ tự:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

Chỉ làm việc khi `Target role: implementer` và handoff có một exact next action.
Resolve base/head, scope, Review Contract, stop condition và Git authorization
trước mutation. Chạy `git status --short`; giữ nguyên thay đổi không liên quan.

## Handoff routing

- `implementation`: thực hiện approved plan bằng execution skill được plan chỉ
  định; không brainstorm hoặc viết lại plan.
- `correction`: sửa exact correction delta trong một batch. Dùng
  `receiving-code-review`; chỉ dùng `systematic-debugging` khi có bug thật hoặc
  root cause chưa rõ.
- `closure`: thực hiện Approval Closure Contract cơ học; không khởi động design,
  test hoặc debugging workflow không liên quan.

Nếu user thêm requirement hoặc task cần đổi architecture, provider/model, data
contract, risk boundary hay authority, dừng và trả lại Reviewer/user để route
lại. Một plan step, tool call hoặc correction nhỏ không phải top-level task mới.

## When implementation may start

Implementation bắt đầu khi handoff trỏ tới spec/plan đã được user duyệt hoặc
một exact correction/closure contract. Report, status snapshot hoặc expected
output không tự authorize code/data change.

Nếu thiếu canonical input, scope mâu thuẫn hoặc task cần đổi requirement,
architecture, provider/model, data contract, risk boundary hay authority, dừng
và trả lại Reviewer/user.

Implementer được tự hoàn thiện approved scope và sửa mọi in-scope issue tìm thấy
mà không gọi Reviewer cho từng chỉnh sửa nhỏ. Không tự hạ risk, tự approve, mở
rộng scope hoặc sửa spec/plan để hợp thức hóa implementation.

## Cách implement

- Giải thích được data flow bằng ngôn ngữ thông thường.
- Bắt đầu bằng giải pháp nhỏ nhất đáp ứng đầy đủ requirement.
- Một file/hàm có nhiệm vụ gọi tên được.
- Reuse production backend hiện có; không copy một pipeline thứ hai.
- Ưu tiên function; chỉ dùng class khi state, lifecycle hoặc interface thật sự
  cần.
- Không thêm abstraction, wrapper, validator, registry, factory, cache, state
  machine, configurability hoặc flexibility phòng xa.
- Không refactor, format hoặc dọn code lân cận ngoài scope.
- Chỉ xóa import, biến, helper hoặc code khi chính thay đổi hiện tại làm chúng
  dư thừa.
- Không giữ mechanism đã được approved scope yêu cầu loại bỏ bằng cách đổi tên
  hoặc chuyển file.

Kỹ thuật nâng cao chỉ được dùng khi có observed problem, giải pháp trực tiếp
không đủ, lợi ích giải thích được, real-system evidence chứng minh lợi ích và
complexity tăng thêm tương xứng.

## Test

- Chỉ tạo hoặc giữ test cho behavior cần thiết, contract quan trọng hoặc bug
  thực tế có nguy cơ tái diễn đáng kể.
- Không đặt mục tiêu theo số test, coverage hoặc số file test.
- Mỗi test phải dễ đọc và trả lời được nó bảo vệ nhu cầu nào của user.
- Không dùng mock, fake hoặc stub dependency.
- Pure deterministic logic được dùng input nhỏ, trực tiếp và hợp lệ; không gọi
  đó là integration evidence.
- Integration test dùng canonical data và dependency thật phù hợp với behavior.
- Audit test thuộc task/phase và downstream scope bị ảnh hưởng trực tiếp.
- Xóa test chỉ bảo vệ implementation detail, lỗi giả định, live verification
  trùng lặp hoặc mechanism đang bị loại bỏ.
- Không chạy test đã xác định là không cần thiết; docs-only task có thể không cần
  automated test.
- Test pass không thay live integration run.

Chọn verification:

- exact live path và smallest useful test trước;
- smoke Golden V3 10 row cho bounded check phù hợp;
- full 45 cases khi thay đổi có thể ảnh hưởng quality decision;
- full backend suite chỉ khi shared contract hoặc blast radius thực sự rộng và
  Review Contract ghi rõ lý do.

Không dựng dead URL, xóa collection hoặc thay environment để tạo failure giả
định. Chỉ giữ failure test cho lỗi thực tế quan trọng có nguy cơ tái diễn.

## Debugging và tự review

Khi có bug thật:

```text
tái tạo nhất quán -> thu bằng chứng -> chứng minh nguyên nhân gốc
-> thử một focused fix -> chạy lại exact live path
```

- Không sửa nhiều giả thuyết cùng lúc.
- Sửa nguyên nhân thay vì thêm fallback hoặc guard che lỗi.
- Chỉ thêm regression test khi bug quan trọng và có credible recurrence risk.
- Trước handoff, đọc exact diff để tìm scope creep, code/test dư, duplication,
  helper một-caller, abstraction phòng xa và data flow khó hiểu.
- Kiểm security theo input/API, secret, provider, data và destructive target
  thực sự bị thay đổi; không tạo security audit cho scope không liên quan.

## Chạy và xác minh thật

- Dùng curated/canonical data, actual service state và production backend path.
- Dùng Qdrant, local model và provider API thật theo approved guide/plan.
- Online và paid API trong approved phase được phép; không tạo consent gate hoặc
  cost machinery lặp lại.
- Không dùng fake ID/data/provider/artifact, mock response, replay hoặc prior
  output làm fresh PASS evidence.
- Behavior thay đổi phải có fresh exact run.
- Evidence trong cùng correction series chỉ được reuse khi inputs,
  dependencies, environment và data flow không đổi; ghi rõ lý do và không gọi
  là fresh.
- Ghi đúng failed, skipped, partial và not verified.
- Active Hue collection chỉ read-only; mutation cần exact approved target.
- Không tự đổi provider/model/device/dataset/config để làm run pass.
- Provider/model/dataset/scope mới, deploy, active mutation hoặc destructive
  action cần authority mới.

## Python, notebook and CodeGraph

Dùng `uv` và safe env-file loader theo `Session_Prompt.md`. Không dùng `pip
install`, system Python làm PASS, hoặc mở/in secret values.

Chỉ tạo/cập nhật notebook khi guide yêu cầu giá trị học tập thật:

- mỗi cell làm một việc và có Markdown ngắn trước code;
- code ngắn, gọi backend và không duplicate logic;
- notebook không phải validator, audit package hoặc test suite;
- repository outputs sạch và execution counts null;
- Run All thật trên temporary copy khi thuộc acceptance;
- không lưu secret hoặc sensitive provider output.

CodeGraph là công cụ tùy chọn để hiểu code và blast radius. Missing/stale/error
không chặn task; tiếp tục bằng `rg`, source reads và real verification. Khi hữu
ích, dùng query hẹp:

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

Không tự init/uninit, xóa `.codegraph/`, đổi telemetry hoặc đưa secrets/private
endpoints vào query. Source và fresh execution ưu tiên hơn graph.

## Self-review, report and handoff

Trước handoff:

1. hoàn tất mọi task trong approved plan;
2. đọc exact base-to-head/worktree diff;
3. xác nhận changed files thuộc scope;
4. chạy required checks và exact live path theo Review Contract;
5. sửa mọi in-scope issue đã phát hiện;
6. ghi failed/skipped/partial/not verified trung thực;
7. tạo detailed implementation report;
8. thay `CURRENT_HANDOFF.md` bằng compact `final_review` packet.

Implementation report dùng `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`
với sáu mục: phạm vi, thay đổi chính, cách đã chạy, kết quả quan sát, lỗi/giới
hạn và handoff cho Reviewer. Không lặp governance checklist hoặc trình bày
expected result như observed.

Current handoff chỉ giữ acceptance mapping, changed files, command/result
summary, risk/deviations, artifact pointers, limitations và exact Reviewer
reruns. Kết thúc bằng exact changed files, `git diff --check`, Git state và một
next role/action.

## Corrections

Với `correction` handoff, sửa toàn bộ findings trong một batch. Không thay phần
được bảo vệ ngoài delta. Rerun affected evidence, giải thích evidence nào được
reuse và trả lại Reviewer; không tự đóng finding.

Không bắt đầu correction thứ năm sau bốn verdict `changes_requested`; trả lại
Reviewer để audit guide, design, plan, acceptance và findings.

## Approval closure

Chỉ thực hiện closure sau khi user confirmation thỏa đúng contract. Thay đổi
exact fields/files, chạy exact checks và tạo next handoff. Nếu user thêm
requirement hoặc repo state khác contract, dừng thay vì tự diễn giải.

Closure là thao tác cơ học; technical readiness và approval vẫn thuộc Reviewer
và user.

## Documentation ownership and Git authorization

Trong implementation scope, Implementer được sửa implementation report,
technical documentation bị implementation làm thay đổi, `CURRENT_HANDOFF.md`
và exact code/test/notebook/dependency files trong plan.

Không tự sửa canonical requirement/spec/plan, risk level, Codex review, user
report, guide/status hoặc stable governance. Exact Approval Closure Contract có
thể cấp mechanical edits mà không chuyển decision ownership.

Chỉ thực hiện đúng Git authorization trong handoff:

```text
git_authorization: none
git_authorization: commit
git_authorization: commit_and_push
```

Authorization phải có exact scope/purpose. Checkpoint commit/push không mang
nghĩa approved và không mở rộng quyền sửa nội dung.
