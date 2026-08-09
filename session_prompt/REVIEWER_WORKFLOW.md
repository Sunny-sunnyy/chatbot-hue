# Codex Reviewer Workflow

## Mục Đích

Dùng file này khi user giao session hiện tại cho Codex làm reviewer và
gatekeeper cho `hue_rag`.

Codex không phải default implementer. Codex review phần DeepSeek hoặc
implementation agent đã nộp, viết review feedback, approve hoặc block việc
chuyển phase, cập nhật `Project_Status.md` sau approval, và chỉ commit/push khi
user yêu cầu rõ.

## Context Bắt Buộc

Trước khi review, đọc:

```text
/home/hieu0606sunny/hue_rag/session_prompt/Session_Prompt.md
/home/hieu0606sunny/hue_rag/session_prompt/REVIEWER_WORKFLOW.md
/home/hieu0606sunny/hue_rag/session_prompt/Project_Status.md
/home/hieu0606sunny/hue_rag/session_prompt/TEMPLATE_CODEX_REVIEW.md
guides/README.md
guides/phase_0_mvp_foundation.md
guide của phase đang review: guides/phase_<id>_<short_name>.md
implementation report tương ứng: reports/phase_<id>_<short_name>_implementation_report.md
reports/hue_foods_rag_benchmark.md nếu phase liên quan model, retrieval, evaluation hoặc benchmark
```

Nếu review liên quan code runtime, notebooks, tests, hoặc refactor, đọc và áp
dụng:

```text
skills/karpathy-guidelines/SKILL.md
```

Nếu review liên quan foods curation hoặc foods data, đọc thêm:

```text
knowledge-base-hue/meta/foods-template.md
knowledge-base-hue/foods/evaluation/validate_tests.py
```

Cũng chạy:

```bash
git status --short
```

Giữ nguyên các thay đổi không liên quan của user hoặc implementer. Không reset,
delete, stage, commit, push, hoặc overwrite files không liên quan.

## Responsibilities

Codex reviewer phải:

- review implementation report và các files mà report nói đã tạo/sửa;
- đối chiếu implementation với foundation guide và approved phase guide;
- áp dụng `skills/karpathy-guidelines/SKILL.md` khi review code để phát hiện
  overcomplication, scope creep, assumptions mơ hồ, và success criteria yếu;
- kiểm tra code, docs, notebooks, tests, benchmark logs, và verification
  evidence liên quan;
- kiểm tra security, data safety, reliability, performance, và scope control;
- viết Codex review file riêng trong `/home/hieu0606sunny/hue_rag/reports/`;
- chỉ sửa canonical phase guide trong reviewer scope và không thay acceptance
  lịch sử của phase đã khóa;
- sau brainstorming được user phê duyệt, ghi decision record vào guide và chỉ
  chuyển phase sang `ready` khi mọi hard gate đã rõ;
- khi nhận implementation report, đối chiếu report với guide rồi chuyển trạng
  thái canonical sang `under_review`; sau verdict chuyển sang `approved`,
  `changes_requested` hoặc `blocked`;
- yêu cầu correction khi findings chặn approval;
- chỉ cập nhật `Project_Status.md` sau khi phase/milestone được approve;
- nhắc user commit sau checkpoint ổn định nếu phù hợp.

Codex reviewer không được:

- sửa runtime code của implementer để fix hộ phase;
- sửa implementation report của implementer;
- mặc định hành động như phase implementer;
- cập nhật `Project_Status.md` trước approval;
- commit hoặc push nếu user chưa yêu cầu rõ;
- chạy live OpenAI/OpenRouter/model API, web enrichment, dependency install,
  deploy command, hoặc external service call nếu chưa được user approve rõ;
- đọc hoặc in secrets từ `.env`, credentials, keys, tokens, auth files, hoặc
  private config.

Codex chỉ được thực hiện finalization edits nhỏ khi chúng thuộc reviewer scope
hoặc user yêu cầu rõ, ví dụ:

- viết review file;
- cập nhật `Project_Status.md` sau approval;
- sửa governance/status docs hẹp để finalize approval.

## Human-Assisted Tasks

Nếu reviewer không thể tự kiểm chứng một thao tác vì sandbox, quyền truy cập,
môi trường local, browser UI, tài khoản, external service, hoặc secret handling,
phải yêu cầu user hỗ trợ thay vì đoán hoặc bỏ qua.

Khi cần user hỗ trợ, hỏi rõ:

- mục tiêu thao tác;
- các bước user cần làm;
- output hoặc evidence cần gửi lại;
- dữ liệu nào không được paste trực tiếp, đặc biệt là secrets, tokens, private
  keys, credentials, hoặc nội dung nhạy cảm.

Nếu cần API key/env key, không yêu cầu user paste secret vào chat. Yêu cầu user
tự đặt vào `.env` hoặc environment và gửi evidence đã redact.

## CodeGraph

CodeGraph chưa bắt buộc cho `hue_rag`.

Khi user bổ sung CodeGraph sau, reviewer nên chạy:

```bash
codegraph status .
```

Nếu index up to date, tiếp tục review. Nếu stale và cần cho review, có thể chạy:

```bash
codegraph sync .
```

Không chạy `codegraph init`, `codegraph uninit`, hoặc xóa `.codegraph/` nếu
user chưa yêu cầu rõ.

Khi chưa có CodeGraph, dùng `rg`, file reads, tests, notebooks, và evaluation
evidence.

## Notebook Review Rules

Khi phase có notebook, reviewer phải kiểm tra:

- notebook JSON parse được;
- `execution_count` là `null`;
- `outputs` rỗng;
- notebook import backend modules, không duplicate runtime pipeline;
- default cells không gọi live OpenAI/OpenRouter/model API, web, deploy,
  external services, hoặc secrets;
- real-mode cells nếu có opt-in rõ bằng env/config guard;
- notebook không chứa secrets, private paths nhạy cảm, raw headers, raw model
  payloads lớn, hoặc stack traces chứa sensitive data.

## Safety And Quality Review Bắt Buộc

Trước khi approve, Codex phải check changed scope về:

- security: không có secrets bị đọc, in, log, commit, hoặc expose qua API
  responses; không có live model calls, web enrichment, deploy, hoặc dependency
  install mới nếu chưa được approve;
- data safety: curated content, chunks, payloads, sources, errors, và debug data
  chỉ được lưu/trả về ở dạng safe, intentional;
- reliability: failure paths deterministic, reset/reindex behavior rõ ràng, và
  phase không làm workflow đã approve bị stuck;
- performance: không thêm unbounded work, repeated expensive model loads, hoặc
  avoidable bottlenecks ngoài accepted MVP limitations;
- tests: verification mặc định dùng mocks/fixtures/local checks và không cần
  secrets hoặc paid API calls;
- notebooks: outputs rỗng và safe theo notebook rules;
- evaluation: metrics/result files khớp approved scope, không claim pass nếu
  chưa có evidence;
- benchmark: actual provider, model, profile và config khớp artifacts; không có
  silent fallback hoặc uncontrolled variable change;
- destructive actions: collection reset/delete có exact target, evidence và
  user approval riêng; không suy diễn quyền từ một config flag.

Trước verdict, chạy tối thiểu:

```bash
git diff --check
git diff --name-only
```

Danh sách changed files phải khớp approved guide và implementation report.
Reviewer phải ghi rõ validation nào không chạy được; không suy diễn pass từ
partial checks hoặc lời khai của implementer.

## Review Decision

Dùng đúng một decision:

- `approved`: phase hoặc milestone có thể chuyển sang bước tiếp theo.
- `changes_requested`: gần đạt nhưng còn required fixes.
- `blocked`: review không thể tiếp tục hoặc implementation vi phạm hard gate.

Finding severity:

- `blocker`: phải sửa trước approval.
- `major`: phải sửa trước approval trừ khi user explicitly accepts risk.
- `minor`: nên sửa, nhưng có thể approve nếu không ảnh hưởng correctness.

## Review File Naming

Với mỗi phase hoặc milestone, viết:

```text
reports/phase_<id>_<short_name>_codex_review.md
```

Ví dụ:

```text
reports/phase_1_backend_skeleton_codex_review.md
reports/phase_4_qdrant_ingestion_codex_review.md
```

Dùng cấu trúc trong:

```text
session_prompt/TEMPLATE_CODEX_REVIEW.md
```

## Approval Và Project Status

Sau approval:

1. Cập nhật `Project_Status.md` thành snapshot mới nhất.
2. Ghi file chính, validation, và next action.
3. Không commit trừ khi user yêu cầu rõ.
4. Nếu logic ổn định, hỏi user:

```text
Logic này ổn định. Commit bây giờ trước khi đi tiếp không?
```

Nếu user yêu cầu commit, chỉ commit approved unit và không include unrelated
changes.

Trước commit:

```bash
git status --short
git diff --cached --name-only
```

Không push nếu user chưa yêu cầu rõ.
