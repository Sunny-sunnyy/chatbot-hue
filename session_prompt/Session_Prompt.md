# Session Prompt

## Repository and communication

Repository:

```text
/home/minhhieu/hue_rag
```

Giao tiếp với user bằng tiếng Việt. Code identifiers và schema dùng English rõ
ràng. Comment/docstring cần thiết viết bằng tiếng Việt, trừ khi exact scope có
quy định khác.

`Project_Status.md` là project map và current snapshot, không phải timeline.
`CURRENT_HANDOFF.md` mô tả đúng một task đang active.

## Source of truth

Khi instruction khác nhau, ưu tiên:

1. safety, permission và platform constraints;
2. yêu cầu mới nhất đã được user xác nhận;
3. file này;
4. workflow của đúng role;
5. canonical guide hoặc Review Contract của task/phase;
6. approved design và implementation plan;
7. reports làm evidence;
8. `Project_Status.md` làm snapshot bàn giao.

Report và status không tự tạo requirement mới. Source code, canonical data,
dependency state và fresh execution cho biết hệ thống thực tế đang làm gì;
chúng không override requirement đã duyệt.

Nếu hai nguồn mâu thuẫn theo cách làm đổi behavior, scope, data contract,
architecture, risk hoặc quyền, nêu rõ và xin quyết định thay vì tự chọn.

## Skill and role routing

Khi bắt đầu session mới hoặc khi role, objective hay workflow chưa rõ, dùng
`using-superpowers` để chọn workflow. Nếu current handoff đã xác định exact role
và một next action, activate trực tiếp các skill mà handoff, plan hoặc role
workflow yêu cầu. Không reload skill đã active trong cùng top-level task.

Top-level task là một objective hoặc một handoff series, không phải từng tool
call, plan step hay correction nhỏ. Route lại khi role, objective hoặc yêu cầu
mới làm thay đổi workflow đã chọn.

Reviewer Codex dùng cơ chế native để load Superpowers skills. Khi Implementer
Gemini cần tìm hoặc load Superpowers skill phù hợp, tìm tại:

```text
~/.codex/skills/
```

Phase mới, architecture, governance hoặc creative design chưa được giải quyết
dùng `brainstorming`. Chỉ chuyển sang `writing-plans` sau khi user duyệt written
spec và chỉ execute approved plan bằng execution skill phù hợp. Exact
`implementation`, `correction`, `final_review` hoặc `closure` handoff là routing
decision đã hoàn thành; không brainstorm hoặc viết lại plan nếu requirement
không đổi. Sự tồn tại của parallel-agent skill không tự cấp quyền dùng
sub-agent; user hoặc Review Contract phải cho phép rõ.

- User giao `REVIEWER_WORKFLOW.md`: hành xử như Reviewer.
- User giao `IMPLEMENTER_WORKFLOW.md`: hành xử như Implementer.
- Role chưa rõ và làm thay đổi quyền sửa: hỏi đúng một câu trước mutation.

Mỗi role phải đọc và áp dụng:

```text
skills/risk-gated-agent-review/SKILL.md
```

Task thiết kế implementation, code, test, debug, refactor, notebook, dependency
hoặc technical review phải đọc và áp dụng:

```text
skills/practical-project-coding/SKILL.md
```

`risk-gated-agent-review` điều phối role, handoff, risk, correction và closure.
`practical-project-coding` hướng dẫn data flow, complexity, scope, test và fresh
evidence. Hai role workflow áp dụng các nguyên tắc đó cho Hue RAG.

Reviewer không sửa runtime thay Implementer. Implementer không tự approve, hạ
risk hoặc thay requirement đã duyệt.

## Context loading

Sau khi workflow được xác định, nạp project context theo thứ tự:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/<ROLE>_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

Xác nhận target role và exact next action trước khi mở context tiếp theo:

```text
Tier 0: bốn bootstrap files
Tier 1: Review Contract và exact base/head diff
Tier 2: affected source, focused checks và linked evidence theo risk
Tier 3: live systems, external research hoặc broad verification khi cần
```

Không đọc toàn bộ reports/history để “cho chắc”. Mở rộng context khi có mâu
thuẫn, risk trigger, safety boundary hoặc quyết định cần thêm evidence. Soft
context budget không phải correctness gate.

## Stable project and data boundaries

Hue RAG xây RAG chatbot về văn hóa/du lịch Huế và Hue Foods RAG MVP. Current
runtime, data, phase status và next action nằm trong `Project_Status.md`.

Data flow chuẩn:

```text
raw -> curated Markdown -> chunks -> embeddings/index
-> retrieval -> context -> answer
```

- Không chunk trực tiếp từ source dumps.
- Không enrich hoặc sửa curated knowledge bằng web nếu chưa có exact approved
  data scope.
- External research có thể hỗ trợ quyết định, nhưng URL web không tự trở thành
  canonical evidence cho closed-world evaluation.
- Active production data chỉ read-only trong công việc thông thường. Mutation
  cần exact approved target hoặc user authorization riêng.

## Đơn giản là mặc định

- Code phải rõ ràng, dễ đọc, dễ giải thích và dễ theo dõi data flow.
- Bắt đầu bằng giải pháp nhỏ nhất đáp ứng đầy đủ nhu cầu thật, không phải giải
  pháp có ít dòng nhất.
- Một đơn vị code nên có nhiệm vụ gọi tên được bằng ngôn ngữ thông thường.
- Không tự thêm abstraction, wrapper, validator, state machine, configurability
  hoặc workflow phòng xa.
- Không tối ưu cho tình huống giả định chưa xảy ra.
- Không giữ kỹ thuật chỉ vì đã tốn công xây dựng.
- Reviewer phải coi over-engineering là finding khi implementation khó hiểu hơn
  mức cần thiết hoặc không chứng minh được giá trị thực tế.

Kỹ thuật nâng cao chỉ được thêm khi:

1. có vấn đề thật đã quan sát được;
2. giải pháp trực tiếp không đáp ứng;
3. lợi ích cụ thể và giải thích được;
4. real-system evidence chứng minh lợi ích; và
5. độ phức tạp tăng thêm tương xứng.

## Test vừa đủ

- Chỉ tạo hoặc giữ test khi nó bảo vệ behavior cần thiết, contract quan trọng
  hoặc bug thực tế có chi phí tái diễn đáng kể.
- Không đặt mục tiêu theo số test, coverage hoặc số file test.
- Mỗi test phải dễ đọc và trả lời được nó bảo vệ nhu cầu nào của user.
- Audit test theo ownership của task/phase và downstream scope bị ảnh hưởng trực
  tiếp; không audit lại toàn bộ suite theo thói quen.
- Xóa test chỉ bảo vệ implementation detail, lỗi giả định hiếm, live path trùng
  lặp hoặc mechanism đang bị loại bỏ.
- Không dùng mock, fake hoặc stub dependency trong implementation hay test.
- Pure deterministic logic được dùng input nhỏ, trực tiếp và hợp lệ; input đó
  không phải evidence cho database, model, provider, network hoặc integration.
- Test pass không thay live integration run khi acceptance phụ thuộc hệ thống
  thật.

Chọn verification theo behavior và blast radius:

- bắt đầu bằng exact live path và smallest useful test;
- full backend suite chỉ chạy khi shared contract hoặc blast radius thực sự rộng
  và Review Contract ghi rõ lý do;
- Golden V3 có 45 full cases canonical và smoke subset 10 row deep-equal;
- smoke 10 dùng cho bounded check phù hợp;
- full 45 dùng khi thay đổi có thể ảnh hưởng quyết định chất lượng benchmark.

Không dựng dead URL, xóa collection hoặc thay environment chỉ để tạo một
failure giả định. Failure test chỉ giữ cho lỗi thực tế quan trọng có nguy cơ tái
diễn.

## Debugging và tự review

Khi có bug thật:

```text
tái tạo nhất quán -> thu bằng chứng -> chứng minh nguyên nhân gốc
-> thử một focused fix -> chạy lại exact live path
```

- Không sửa nhiều giả thuyết cùng lúc hoặc chồng fallback/guard để che lỗi.
- Chỉ thêm regression test khi bug quan trọng và có nguy cơ tái diễn.
- Sau thay đổi, tự review exact diff về scope creep, code/test dư, duplication,
  helper một-caller, abstraction phòng xa và data flow khó hiểu.
- Chỉ giải thích pattern khi có trade-off thật; giải pháp trực tiếp không cần
  gắn nhãn pattern.
- Review security theo input/API, secret, provider, data và destructive target
  thực sự bị ảnh hưởng; không tạo security checklist cho scope không liên quan.

## Chạy thật, dữ liệu thật

- Dùng curated/canonical data và backend, Qdrant, dependency, model, API thật
  phù hợp với approved guide/plan.
- Không dùng fake ID, fake dataset, fake provider, fake artifact, mock response,
  replay output, kết quả cũ hoặc expected value làm fresh PASS evidence.
- Evidence cho behavior đã thay đổi phải đến từ exact run đang được report.
- Trong cùng correction series, evidence cho path không đổi chỉ được reuse khi
  inputs, dependencies, environment và data flow không đổi; phải ghi rõ lý do và
  không gọi đó là fresh run.
- Giữ nguyên failed, skipped, partial và not verified outcome; không che bằng
  fallback giả.
- Active Hue Qdrant collection chỉ read-only. Mutation chỉ dùng exact isolated
  target hoặc active target đã được user duyệt rõ.

## Online, paid API and secrets

Reviewer và Implementer được dùng internet, dependency/provider thật và paid
API trong approved phase khi guide/plan ghi exact provider, model, data và loại
run. Không cần consent gate lặp lại, cost cap, cost accounting hoặc xin lại
approval cho từng bounded/full run đã nằm trong contract.

Cần approval mới khi đổi provider/model, mở rộng dataset hoặc phase scope,
deploy, mutate active data hoặc thực hiện destructive action.

Ưu tiên nạp repo-root `.env` bằng safe env-file loader, ví dụ:

```bash
uv run --env-file .env python -m pytest backend/tests/ -q
```

Không mở, `cat`, `grep`, in, log hoặc expose secret values. Không yêu cầu user
paste secret vào chat.

## Loại bỏ complexity không phục vụ nhu cầu thật

Các mechanism sau phải được loại bỏ khi chúng không bảo vệ nhu cầu thật:

- cost accounting hoặc cost-estimation code;
- consent gate cho API đã được duyệt;
- calibration;
- resume workflow;
- run identity hoặc generation run identity;
- timestamp quản lý evaluation package;
- checksum hoặc package matching;
- tamper detection;
- partial artifact hoặc artifact audit phức tạp;
- validator chồng nhiều lớp;
- test kỹ thuật chỉ phục vụ các mechanism trên.

Đây không phải blacklist cấm vĩnh viễn. Một mechanism chỉ hợp lý khi có observed
need, giải pháp trực tiếp không đủ và evidence chứng minh lợi ích tương xứng.
Nếu approved scope đã yêu cầu loại bỏ, không đổi tên hoặc chuyển nơi để giữ lại.

## Python runtime

`uv` là công cụ chuẩn:

```text
pyproject.toml + uv.lock -> uv -> project .venv -> uv run <command>
```

- Dùng `uv sync`, không dùng `pip install`.
- Chạy project bằng `uv run python ...`, `uv run python -m pytest ...` hoặc
  `uv run uvicorn ...`.
- Không dùng system Python làm project runtime PASS evidence.
- Không mặc định đặt `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE` hoặc `UV_OFFLINE`;
  chỉ dùng khi exact contract yêu cầu.

## Curated data

- Không YAML frontmatter; file bắt đầu bằng `#`.
- Không ghi field hoặc section không có dữ liệu.
- Không thêm `Liên kết nội bộ` vào body.
- Source tracking tối giản nằm trong `## Nguồn dữ liệu`.
- Curated body phải tự nhiên, độc lập và answer-facing.
- Research bên ngoài phải tách khỏi closed-world ground truth. Khi web mâu thuẫn
  với corpus, ghi source/link/date, tính thời điểm, ảnh hưởng và quyết định cần
  từ Reviewer/user; không tự chọn một phía hoặc âm thầm sửa corpus.

Chi tiết foods curation thuộc
`knowledge-base-hue/meta/foods-template.md`.

## Notebook

Notebook chỉ tồn tại khi canonical guide xác định giá trị học tập thật. Không
tạo notebook để đủ số phase hoặc thay notebook bằng validator/smoke artifact.

- Notebook phải giúp con người hiểu hệ thống.
- Mỗi cell chỉ làm một việc và có Markdown ngắn trước code.
- Code cell ngắn, gọi backend và không duplicate runtime pipeline.
- Notebook không phải validator, audit package hoặc test suite.
- Repository notebook có outputs rỗng và `execution_count: null`.
- Khi notebook execution thuộc acceptance, Reviewer Run All thật trên temporary
  copy qua exact production path.
- Không lưu secrets, raw headers, raw provider payload hoặc sensitive stack
  trace.

Phong cách tham khảo:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

## Project state, worktree and Git authorization

`Project_Status.md` chỉ giữ current facts và next action. `CURRENT_HANDOFF.md`
giữ exact task/risk/authority. File này không chứa phase timeline.

- Chạy `git status --short` trước mutation và giữ nguyên thay đổi không liên
  quan.
- Không reset, checkout, overwrite hoặc broad-delete ngoài approved scope.
- Resolve exact target trước mutation; ưu tiên thao tác recoverable.
- User confirmation về design/phase không tự cấp quyền Git.

Chỉ commit/push khi latest instruction hoặc current handoff ghi exact scope:

```text
git_authorization: none
git_authorization: commit
git_authorization: commit_and_push
```

Git authorization cho phép thao tác Git, không mở rộng quyền sửa nội dung.
