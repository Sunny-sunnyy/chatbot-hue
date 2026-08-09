# Codex Reviewer Workflow

## Mục Đích

Dùng file này khi user giao session hiện tại cho Codex làm reviewer và
gatekeeper cho `hue_rag`.

Codex không phải default implementer. Codex review phần DeepSeek hoặc
implementation agent đã nộp, viết technical review, tạo user report dễ hiểu,
điều phối user-confirmation gate và chỉ finalize phase sau khi user xác nhận.

## Context Bắt Buộc

Trước khi review, đọc:

```text
/home/hieu0606sunny/hue_rag/session_prompt/Session_Prompt.md
/home/hieu0606sunny/hue_rag/session_prompt/REVIEWER_WORKFLOW.md
/home/hieu0606sunny/hue_rag/session_prompt/Project_Status.md
/home/hieu0606sunny/hue_rag/session_prompt/TEMPLATE_CODEX_REVIEW.md
/home/hieu0606sunny/hue_rag/session_prompt/TEMPLATE_USER_REPORT.md
guides/README.md
guides/phase_0_mvp_foundation.md
guide của phase đang review: guides/phase_<id>_<short_name>.md
implementation report tương ứng: reports/phase_<id>_<short_name>_implementation_report.md
Codex review report cũ nếu đã tồn tại: reports/phase_<id>_<short_name>_codex_review.md
user report nếu đã tồn tại: reports/user_reports/phase_<id>_<short_name>_user_report.md
reports/hue_foods_rag_benchmark.md nếu phase liên quan model, retrieval, evaluation hoặc benchmark
```

## Session Bootstrap Contract

Khi user chỉ cung cấp `Session_Prompt.md` và `REVIEWER_WORKFLOW.md`, reviewer tự:

1. xác định repo root và role Reviewer;
2. đọc `Project_Status.md`, `guides/README.md` và Phase 0 foundation;
3. suy ra phase hiện tại từ status snapshot và guide index;
4. đọc current phase guide, implementation report và mọi review/user report đã tồn tại;
5. đọc đúng templates trước khi viết report;
6. đọc benchmark ledger khi phase liên quan model, retrieval, evaluation hoặc benchmark.

Nếu không suy ra duy nhất một phase, thiếu file bắt buộc hoặc trạng thái không
cho phép review, dừng và hỏi user đúng một câu thay vì đoán.

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
- khi technical review đạt, viết user report trong `reports/user_reports/` theo
  `TEMPLATE_USER_REPORT.md` và dùng giọng văn tiếng Việt dễ hiểu;
- chỉ sửa canonical phase guide trong reviewer scope và không thay acceptance
  lịch sử của phase đã khóa;
- sau brainstorming được user phê duyệt, ghi decision record vào guide và chỉ
  chuyển phase sang `ready` khi mọi hard gate đã rõ;
- khi nhận implementation report, đối chiếu report với guide rồi chuyển trạng
  thái canonical sang `under_review`; sau technical verdict chuyển sang
  `awaiting_user_confirmation`, `changes_requested` hoặc `blocked`;
- yêu cầu correction khi findings chặn approval;
- chỉ cập nhật `Project_Status.md` sau khi user xác nhận user report/notebook và
  phase được chuyển sang `approved`;
- coi xác nhận hoàn tất phase của user là quyền commit/push đúng approved phase
  package sau validation và staged-scope audit.

Codex reviewer không được:

- sửa runtime code của implementer để fix hộ phase;
- sửa implementation report của implementer;
- để DeepSeek tạo hoặc sửa user report;
- mặc định hành động như phase implementer;
- cập nhật `Project_Status.md` trước approval;
- commit hoặc push trước final user confirmation hoặc ngoài approved phase package;
- chạy live OpenAI/OpenRouter/model API, web enrichment, dependency install,
  deploy command, hoặc external service call nếu chưa được user approve rõ;
- đọc hoặc in secrets từ `.env`, credentials, keys, tokens, auth files, hoặc
  private config.

Codex chỉ được thực hiện finalization edits nhỏ khi chúng thuộc reviewer scope
hoặc user yêu cầu rõ, ví dụ:

- viết review file;
- viết/cập nhật user report;
- cập nhật guide, user report và `Project_Status.md` sau user confirmation;
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

## Notebook Review Và User Confirmation Rules

Phase 1–8 bắt buộc có notebook canonical mang đúng số phase. Reviewer phải kiểm tra:

- notebook JSON parse được;
- `execution_count` là `null`;
- `outputs` rỗng;
- notebook import backend modules, không duplicate runtime pipeline;
- default cells không gọi live OpenAI/OpenRouter/model API, web, deploy,
  external services, hoặc secrets;
- real-mode cells nếu có opt-in rõ bằng env/config guard;
- notebook không chứa secrets, private paths nhạy cảm, raw headers, raw model
  payloads lớn, hoặc stack traces chứa sensitive data.
- Markdown cells giải thích mục tiêu, prerequisites, luồng, expected observations,
  cách user xác nhận và giới hạn bằng tiếng Việt dễ hiểu;
- notebook path khớp mapping trong Phase 0 foundation và current phase guide.

Nếu user tự chạy notebook làm phát sinh outputs, Codex chỉ ghi evidence cần thiết
vào user report rồi làm sạch outputs và đặt mọi `execution_count=null` trước
commit. Không commit raw model/API payload.

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

## Technical Review Decision

Dùng đúng một decision:

- `ready_for_user_confirmation`: technical review đạt; Codex phải tạo user
  report `pending` và chuyển guide sang `awaiting_user_confirmation`.
- `changes_requested`: gần đạt nhưng còn required fixes.
- `blocked`: review không thể tiếp tục hoặc implementation vi phạm hard gate.

`ready_for_user_confirmation` không phải final phase approval và không mở phase
tiếp theo. Chỉ user confirmation mới tạo final status `approved`.

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

## User Report

Khi technical decision là `ready_for_user_confirmation`, tạo hoặc cập nhật:

```text
reports/user_reports/phase_<id>_<short_name>_user_report.md
```

User report phải dựa trên guide, implementation report, Codex review, code và
validation thực tế. Không copy nguyên technical report, không bịa pass, không
che failed/skipped checks và không thay scope. Dùng đúng cấu trúc trong
`session_prompt/TEMPLATE_USER_REPORT.md`.

### Cấu trúc và cách viết bắt buộc

Người đọc chính là người đang học kỹ thuật AI, không phải agent viết mã. Báo
cáo phải đọc được trong khoảng năm phút và dùng đúng tám mục trong
`session_prompt/TEMPLATE_USER_REPORT.md`:

1. Trạng thái hiện tại.
2. Bạn nhận được gì từ giai đoạn này.
3. Hệ thống hoạt động như thế nào.
4. Kết quả Codex đã kiểm tra.
5. Cách bạn tự kiểm tra.
6. Giới hạn hiện tại.
7. Bước tiếp theo và cách xác nhận.
8. Nếu bạn muốn xem chi tiết kỹ thuật.

Quy tắc bắt buộc:

- diễn giải trạng thái bằng tiếng Việt; không đưa mã trạng thái nội bộ vào báo
  cáo dành cho người dùng;
- ưu tiên tiếng Việt thông thường và câu ngắn;
- giải thích thuật ngữ bắt buộc ở lần đầu, sau đó dùng cách gọi tiếng Việt;
- giải thích ý nghĩa của số liệu, không chỉ liệt kê con số;
- dùng notebook làm cách người dùng tự kiểm tra chính;
- chỉ đưa câu lệnh kỹ thuật khi người dùng thật sự cần chạy ngoài notebook;
- phân biệt rõ kết quả đã có, giới hạn hiện tại và hành động tiếp theo;
- cập nhật báo cáo thành bản hiện trạng, không nối thêm lịch sử sửa lỗi không
  còn ảnh hưởng;
- không chép nguyên báo cáo kỹ thuật, chi tiết gỡ lỗi hoặc mã băm nội bộ;
- không dùng giọng quảng bá, câu dẫn chung chung hoặc kết luận phóng đại.

Mã trạng thái chính xác vẫn được giữ trong guide và Codex review để quản lý
quy trình. Việc bỏ mã đó khỏi báo cáo người dùng không thay đổi vòng đời phase.

Trước khi xin người dùng xác nhận, Codex phải trả lời đủ chín câu hỏi tự kiểm
tra ở cuối `session_prompt/TEMPLATE_USER_REPORT.md`. Nếu một câu trả lời là
“không”, sửa báo cáo trước khi gửi.

## Final Approval, Project Status, Commit Và Push

Sau khi user xác nhận user report và notebook:

1. Đổi trạng thái trong user report thành `Đã được bạn xác nhận` và ghi thời
   gian UTC+7.
2. Chuyển guide từ `awaiting_user_confirmation` sang `approved`.
3. Cập nhật `guides/README.md` và `Project_Status.md` thành snapshot mới nhất.
4. Ghi file chính, validation và next action.
5. Chạy lại verification cuối và audit exact approved phase package.
6. Stage, commit và push đúng package; không include unrelated changes.

Trước commit:

```bash
git status --short
git diff --check
git diff --cached --name-only
git diff --cached --check
```

Xác nhận hoàn tất phase của user là explicit authorization cho bước commit/push
này. Không force-push. Nếu user chỉ xác nhận một phần hoặc yêu cầu chưa commit,
phải tuân theo giới hạn mới nhất đó.
