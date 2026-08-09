# DeepSeek Implementer Workflow

## Mục Đích

Dùng file này khi user giao session hiện tại cho DeepSeek hoặc implementation
agent khác để implement approved phase/milestone trong `hue_rag`.

Implementer xây đúng approved scope, chạy verification, tạo/cập nhật notebooks
khi phase yêu cầu, và viết implementation report. Implementer không approve
chính work của mình, không cập nhật `Project_Status.md`, không commit và không
push.

## Context Bắt Buộc

Trước khi implement, đọc:

```text
/home/hieu0606sunny/hue_rag/session_prompt/Session_Prompt.md
/home/hieu0606sunny/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/hieu0606sunny/hue_rag/session_prompt/Project_Status.md
/home/hieu0606sunny/hue_rag/session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md
docs/superpowers/specs/2026-08-08-hue-foods-rag-mvp-design.md
docs/superpowers/plans/2026-08-08-hue-foods-rag-mvp-plan.md
docs/superpowers/plans/2026-08-08-hue-foods-rag-benchmark-log.md
the approved phase section in the implementation plan
relevant Codex review feedback, if resubmitting fixes
```

Nếu implement liên quan code runtime, notebooks, tests, hoặc refactor, đọc và áp
dụng:

```text
skills/karpathy-guidelines/SKILL.md
```

Nếu implement liên quan foods curation hoặc foods data, đọc thêm:

```text
knowledge-base-hue/meta/foods-template.md
knowledge-base-hue/foods/evaluation/validate_tests.py
```

Cũng chạy:

```bash
git status --short
```

Giữ nguyên unrelated changes. Không reset, delete, stage, commit, push, hoặc
overwrite files ngoài approved scope.

## Responsibilities

Implementer phải:

- chỉ implement user-approved phase hoặc milestone;
- làm theo spec/plan hiện hành;
- áp dụng `skills/karpathy-guidelines/SKILL.md` khi viết code để giữ assumptions
  rõ ràng, code đơn giản, thay đổi surgical, và success criteria có thể verify;
- trước mỗi phần quan trọng, thực hiện mini research/brainstorming trong repo
  như plan yêu cầu;
- làm surgical changes, không refactor ngoài scope;
- tạo runtime `.py` dưới `backend/` khi phase yêu cầu;
- tạo/cập nhật `.ipynb` dưới `notebooks/` khi phase yêu cầu;
- notebook phải import backend modules, không duplicate runtime logic;
- chạy smallest relevant verification trước, rồi broader checks khi cần;
- tự kiểm tra security, data safety, reliability, performance trước handoff;
- viết implementation report trong `/home/hieu0606sunny/hue_rag/reports/`;
- phản hồi Codex feedback bằng cách sửa code/docs/report của implementer khi
  cần.

Implementer không được:

- sửa Codex review files;
- cập nhật `Project_Status.md`;
- approve chính work của mình;
- commit hoặc push;
- chạy live OpenAI/OpenRouter/model API, web enrichment, deploy, dependency
  install, hoặc external service call nếu user chưa approve rõ;
- đọc hoặc in secrets từ `.env`, credentials, keys, tokens, auth files, hoặc
  private config;
- yêu cầu user paste secret vào chat.

## Live Model/API Policy

Default implementation và tests phải dùng mocks, dry-runs, fixtures, hoặc local
checks.

Không gọi live OpenAI/OpenRouter/model API mặc định.

Chỉ chạy live model/evaluation answer judge khi user approve rõ. Nếu cần API
key, yêu cầu user tự đặt vào `.env` hoặc environment và gửi evidence đã redact.

Retrieval evaluation không cần model judge có thể chạy local nếu Qdrant và local
embedding model đã sẵn sàng.

## Notebook Rules

Phase nào plan yêu cầu notebook thì implementer bắt buộc tạo hoặc cập nhật
notebook tương ứng.

Notebook requirements:

- nằm trong `notebooks/`;
- import backend modules;
- không duplicate runtime pipeline logic;
- outputs rỗng trong repo;
- `execution_count` là `null`;
- default cells không gọi live OpenAI/OpenRouter/model API, web, deploy,
  external services, hoặc secrets;
- real-mode cells nếu có phải opt-in bằng env/config guard rõ;
- không lưu secrets, private paths nhạy cảm, raw headers, raw model payloads lớn,
  hoặc stack traces chứa sensitive data;
- Markdown cells ghi expected output hoặc cách user tự chạy lại nếu cần.

## CodeGraph

CodeGraph chưa bắt buộc cho `hue_rag`.

Khi user bổ sung CodeGraph sau, implementer có thể dùng CodeGraph để hiểu call
flow, symbol ownership, và impact trước khi sửa runtime code.

Không chạy `codegraph init`, `codegraph uninit`, hoặc xóa `.codegraph/` nếu user
chưa yêu cầu rõ.

Khi chưa có CodeGraph, dùng `rg`, file reads, tests, notebooks, và evaluation
evidence.

## Implementation Report

Sau mỗi approved phase hoặc milestone, viết report theo:

```text
session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md
```

Report path:

```text
reports/phase_<id>_<short_name>_implementation_report.md
```

Ví dụ:

```text
reports/phase_1_backend_skeleton_implementation_report.md
reports/phase_4_qdrant_ingestion_implementation_report.md
```

Report phải nêu:

- approved scope;
- files created;
- files modified;
- notebooks created/modified;
- commands run;
- tests run;
- verification evidence;
- known issues;
- deviations from plan;
- whether live network/model/deploy/secret access occurred;
- self-check về security, data safety, reliability, performance, tests, và
  notebooks.

## Self-Check Bắt Buộc Trước Handoff

Trước khi nói phase/milestone sẵn sàng cho Codex review, implementer phải check:

- security: không có secrets bị đọc, in, log, commit, hoặc expose;
- data safety: chunks, metadata, API responses, debug data, model errors, và
  result files chỉ chứa dữ liệu safe/intentional;
- reliability: failure paths deterministic, reset/reindex behavior rõ ràng,
  import paths ổn định, và commands chạy từ `backend/` như plan;
- performance: không thêm repeated expensive model loads, unbounded work, hoặc
  bottlenecks không được document;
- tests: default verification không cần secrets, paid model calls, deploy, hoặc
  external services;
- notebooks: JSON hợp lệ, outputs rỗng, execution counts null, default cells
  safe.

Nếu có accepted local-MVP limitation, ghi trong `Known Issues` với severity và
lý do không block current phase.

## Phản Hồi Codex Feedback

Khi Codex viết review file:

1. Đọc Codex review file.
2. Sửa mọi `blocker` và `major` finding trừ khi user explicitly changes scope.
3. Sửa `minor` findings khi cheap và local.
4. Cập nhật implementation report với:
   - thay đổi sau review;
   - commands/tests mới;
   - remaining known issues.
5. Không sửa Codex review file.
6. Hand work lại cho Codex review lần nữa.

## Commit Và Push

Implementer có thể inspect git status nhưng mặc định không được commit hoặc
push.

Nếu commit hoặc push có vẻ cần thiết, dừng lại và yêu cầu user để Codex review
và approve hành động đó.
