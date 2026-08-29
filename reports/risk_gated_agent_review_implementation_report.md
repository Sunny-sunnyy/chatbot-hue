# Risk-Gated Agent Review Implementation Report

## 1. Phạm vi

Triển khai workflow governance dạng risk-gated theo design và plan đã được user
duyệt. Phạm vi chỉ gồm shared skill, bốn tài liệu bootstrap, một current
handoff và báo cáo này; không thay đổi runtime, tests, notebooks, dependencies,
datasets hoặc Phase 8 benchmark artifacts.

## 2. Thay đổi chính

- Tạo generic shared skill `risk-gated-agent-review` với hai role branches,
  tiered context loading, Review Contract, risk-trigger matrix, evidence reuse,
  correction/closure và gated Git contract.
- Skill không chứa tên model, service, phase hoặc coding/test doctrine riêng của
  Hue RAG.
- Rút `Session_Prompt.md` về stable source-of-truth, role/context routing,
  project boundaries, safety, skill pointers và Git authorization.
- Viết lại `Project_Status.md` thành project overview, system/data map, current
  runtime, compact phase table, active decisions, boundaries, canonical map và
  một next action.
- Rút hai role workflows về project-specific authority adapters; shared
  evidence/risk protocol nằm duy nhất trong skill mới.
- Tạo một `CURRENT_HANDOFF.md` target Reviewer cho independent final review,
  chứa Review Contract, acceptance mapping, evidence index và proposed closure
  sang 08b `next_design`.

## 3. Cách đã kiểm tra

Đang thu thập evidence bằng word-count comparison, responsibility mapping,
Markdown/path checks, exact diff audit và bốn tabletop scenarios.

Task 1 đã chạy:

```text
rg project/coding-specific terms trong SKILL.md
rg coordination contract terms trong SKILL.md
skill-creator quick_validate.py skills/risk-gated-agent-review
```

Final governance validation đã chạy:

```text
wc -w trên năm bootstrap/role files
git diff --name-only <base> trên protected và declared paths
git diff --check cùng trailing-whitespace scan cho untracked files
repository-relative path existence checks
single active handoff scan
official skill quick validation
four manual tabletop scenarios
```

## 4. Kết quả quan sát

Fresh baseline trước implementation:

| Bootstrap file | Word count |
|---|---:|
| `session_prompt/Session_Prompt.md` | 3,292 |
| `session_prompt/Project_Status.md` | 4,005 |
| `session_prompt/REVIEWER_WORKFLOW.md` | 1,763 |
| `session_prompt/IMPLEMENTER_WORKFLOW.md` | 1,480 |
| **Tổng bốn file** | **10,540** |

Baseline được đo bằng `wc -w` tại commit `8ef5da5` trước khi sửa workflow.

Task 1 observed results:

- project/coding-specific term scan: không có match;
- coordination terms: có đầy đủ Reviewer, Implementer, Review Contract và Git
  authorization contract;
- official skill validation: `Skill is valid!`;
- không tạo scripts, references, assets, UI metadata hoặc dependency vì skill
  tự chứa đủ protocol cần thiết.

Task 2 observed results:

- `Session_Prompt.md`: giảm từ 3.292 xuống 836 từ;
- retained-invariant scan tìm thấy source-of-truth, role routing,
  `CURRENT_HANDOFF`, hai skill pointers, active read-only, secrets và Git rules;
- history scan cho Golden V2, Qwen embedding, Notebook 08a và Phase 0–6 không có
  match;
- current phase/runtime facts được chuyển trách nhiệm sang `Project_Status.md`,
  không bị biến thành requirement mới trong session prompt.

Task 3 observed results:

- `Project_Status.md`: giảm từ 4.005 xuống 908 từ;
- current-fact scan tìm thấy project goal, 572 chunks, active read-only
  collection, Golden V3 45+10, exact three-model catalog và next 08b boundary;
- audit-history scan không có match cho correction/revision narrative;
- file vẫn đóng vai trò README-level map bằng project overview, current runtime,
  phase table và canonical pointers.

Task 4 observed results:

- `REVIEWER_WORKFLOW.md`: giảm từ 1.763 xuống 656 từ;
- `IMPLEMENTER_WORKFLOW.md`: giảm từ 1.480 xuống 623 từ;
- required-term scans tìm thấy shared-skill pointer, current handoff, verdicts,
  correction/closure, evidence và Git boundaries;
- scan `fake`/`coverage` còn ba match cần thiết: hai safety/severity definitions
  và một câu cấm dùng coverage làm blocker; không lặp implementation doctrine.

Responsibility map:

| Nội dung | Decision owner | Editing role / condition |
|---|---|---|
| Requirement, spec, plan, Review Contract | Reviewer + user approval | Reviewer |
| Runtime, tests, notebooks, dependencies | Approved plan | Implementer trong exact scope |
| Implementation report, technical docs | Implementer | Implementer; escalate nếu đổi contract |
| Codex review, user report, guide/status decision | Reviewer | Reviewer; Implementer chỉ mechanical closure fields |
| `CURRENT_HANDOFF.md` | Outgoing role | Reviewer hoặc Implementer tạo cho next role |
| Approval closure | Reviewer + user confirmation | Implementer thi hành exact contract |
| Commit/push | User/current handoff | Role được cấp exact Git authorization |

Final context measurement:

| File | Words |
|---|---:|
| `Session_Prompt.md` | 836 |
| `Project_Status.md` | 908 |
| `REVIEWER_WORKFLOW.md` | 656 |
| `IMPLEMENTER_WORKFLOW.md` | 623 |
| `CURRENT_HANDOFF.md` | 650 |

Per-role bootstrap comparison:

| Role bundle | Old words | New words | Reduction |
|---|---:|---:|---:|
| Reviewer | 9,060 | 3,050 | 6,010 (66.3%) |
| Implementer | 8,777 | 3,017 | 5,760 (65.6%) |

Hai bundle đều thấp hơn soft target khoảng 4.000 từ mà vẫn giữ project map,
safety/authority boundaries và current task. Handoff thấp hơn soft target 800
từ; không cần cắt thêm context.

Tabletop replay:

| Scenario | Result | Observed routing |
|---|---|---|
| 08b next design | `PASS` | Project Status và proposed closure xác định research/brainstorming; cấm implementation/run, paid API, active mutation và cutover |
| 08a cleanup replay | `PASS` | Dependency/functional triggers chọn exact diff, focused checks, lock và safe integration inspection; unchanged model behavior không bị full rerun |
| Major correction | `PASS` | Reviewer tạo một correction delta với severity, affected requirement, reruns và reusable evidence; Implementer không tự close |
| Approval closure | `PASS` | Reviewer quyết định và khóa contract; sau user confirmation Implementer chỉ update exact fields/Git và chuyển `next_design` |

Final checks observed:

- official skill validator: `Skill is valid!`;
- all explicit repository-relative bootstrap/canonical pointers checked exist;
- exactly one active handoff file: `session_prompt/CURRENT_HANDOFF.md`;
- protected runtime/notebook/evaluation/dependency paths: no diff from base;
- exact implementation scope: four modified bootstrap files plus three new
  files (skill, current handoff, report);
- `git diff --check`: pass; explicit trailing-whitespace scan on untracked files
  has no match;
- no sub-agent, backend test, notebook, Qdrant, model or paid API was run.

## 5. Lỗi và giới hạn

Không chạy runtime tests hoặc live services vì implementation không thay đổi
runtime behavior. Tabletop chỉ chứng minh routing/document contract, không phải
evidence cho product runtime. Codex thực hiện implementation theo yêu cầu trực
tiếp của user; vì vậy một Reviewer session sau vẫn phải dùng handoff và
independent diff gate, không được coi report này là self-approval.

User đã authorize checkpoint commit/push sau implementation. Handoff dùng
`Head commit: HEAD` từ base `8ef5da51affe5dddcbb0d5b83f17443b44a18faf`;
checkpoint không mang nghĩa technical approval.

## 6. Handoff cho Reviewer

Reviewer session mới đọc theo thứ tự:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

Thực hiện đúng medium-risk Review Contract trong current handoff. Không bắt đầu
08b; commit đã push chỉ là immutable review target, không phải approval.
