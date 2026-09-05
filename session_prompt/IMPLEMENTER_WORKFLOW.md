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
dependency, debug và refactor. Hai skill này là canonical cho nhiệm vụ tương
ứng. Các Superpowers skill khác chỉ load khi exact
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

Bốn file giúp tìm task, không thay việc đọc spec/plan, correction contract và
canonical inputs mà handoff dẫn tới. Yêu cầu trực tiếp mới khác task cũ được
route theo `Session_Prompt.md`; không tự tiếp tục handoff đã bị thay thế.

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

Được tự quyết naming, chia/gộp function/helper/class và tổ chức logic nội bộ
trong allowed paths. Giữ nguyên requirement, acceptance, public/data contract,
kiến trúc đã chốt và quyền. Gợi ý code trong plan không phải ràng buộc nếu không
được nêu là bắt buộc; nếu ràng buộc thật cần đổi thì trả lại Reviewer. Report
chỉ giải thích trade-off có ý nghĩa, không xin duyệt từng chi tiết code.

## Cách implement

Áp dụng đầy đủ `practical-project-coding`: data flow trực tiếp, trách nhiệm và
naming rõ, giải pháp nhỏ nhất đủ requirement, abstraction có bằng chứng và
thay đổi surgical. Giải thích được code bằng ngôn ngữ thông thường; reuse
production backend, không tạo pipeline thứ hai hoặc cơ chế phòng xa.

Thêm ghi chú/comment/docstring bằng tiếng Việt cho mục đích, bước xử lý hoặc
constraint mà code chưa tự thể hiện. Không chú thích lại từng dòng hiển nhiên
hoặc dùng comment biện hộ cho code khó hiểu. Không dùng line count/số caller làm
lệnh cấm class/helper. Contract đã rõ là nhu cầu thật, không cần đợi sự cố.

Giữ chính sách simplicity và removal trong `Session_Prompt.md`; không đổi tên
hoặc chuyển file để giữ mechanism mà approved scope yêu cầu loại bỏ.

## Test

Chọn test theo behavior/contract và blast radius trong coding skill và Review
Contract, không theo số test, coverage hoặc số file. Audit scope bị ảnh hưởng;
bỏ test chỉ bảo vệ implementation detail/mechanism dư. Không dùng mock, fake
hoặc stub dependency; pure input nhỏ hợp lệ không phải integration evidence.
Integration phải dùng canonical data và dependency thật; test pass không thay
live run. Không dựng failure giả định bằng dead URL/xóa collection/đổi environment.

Áp dụng lựa chọn smoke Golden V3 10/full 45 và full-suite boundary trong
`Session_Prompt.md`. Docs-only kiểm diff, consistency, links và lifecycle theo
contract; không chạy backend/model/API tests chỉ để đủ checkpoint.

## Debugging và tự review

Áp dụng chuỗi reproduction → evidence → root cause → focused fix → exact rerun
trong `Session_Prompt.md`; không sửa nhiều giả thuyết hoặc chồng fallback/guard
che lỗi. Regression test chỉ khi cần bảo vệ bug quan trọng có nguy cơ tái diễn.
Đọc exact diff theo coding skill trước handoff để bỏ scope creep, duplication,
code/test dư và abstraction không có giá trị; kiểm security ở boundary thực sự
bị ảnh hưởng, không tạo audit cho scope không liên quan.

## Chạy và xác minh thật

Áp dụng chính sách dữ liệu thật, online/paid API và secrets trong
`Session_Prompt.md`; evidence reuse theo coordination skill. Behavior thay đổi
cần fresh exact run; không bịa evidence, che failed/skipped/partial/not verified
hoặc tự đổi provider/model/device/dataset/config để làm run pass. Active Hue
collection chỉ read-only nếu chưa có exact approval; scope/provider/model/data
mới, deploy và destructive action cần authority mới.

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
5. sửa in-scope blocker/major; minor xử lý theo coordination skill;
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

Tự cung cấp prompt chuyển tiếp ngắn cho user gửi Reviewer theo
`Session_Prompt.md`; không tạo thêm bản requirement hay tự khởi chạy agent.

## Corrections

Với `correction` handoff, xử lý findings trong một batch bằng sửa đổi hoặc phản
biện có evidence/cách đơn giản hơn theo coordination skill. Không thay phần
được bảo vệ ngoài delta. Rerun affected evidence, giải thích evidence nào được
reuse và trả lại Reviewer; không tự đóng finding. Correction trong requirement,
acceptance và quyền đã duyệt không cần user duyệt riêng.

Minor không chặn hoàn tất; sửa trong scope nếu hữu ích hoặc ghi ngắn lý do giữ
lại. Không mở correction riêng chỉ vì minor. Vấn đề ngoài scope ghi trong report,
không tự sửa; dừng và báo khi ảnh hưởng acceptance hoặc an toàn/quyền. Bất đồng
chưa giải quyết do Reviewer tổng hợp trình user, không phải quyền bỏ qua finding.

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
