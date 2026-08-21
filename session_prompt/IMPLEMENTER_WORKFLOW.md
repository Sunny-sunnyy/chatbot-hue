# DeepSeek Implementer Workflow

## Mục Đích

Dùng file này khi user giao session hiện tại cho DeepSeek hoặc implementation
agent khác để implement approved phase/milestone trong `hue_rag`.

Implementer xây đúng approved scope, chạy verification, tạo/cập nhật notebook
bắt buộc cho Phase 1–8, và viết technical implementation report. Implementer không approve
chính work của mình, không cập nhật `Project_Status.md`, không commit và không
push.

## Context Bắt Buộc

Trước khi implement, đọc:

```text
/home/hieu0606sunny/hue_rag/session_prompt/Session_Prompt.md
/home/hieu0606sunny/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/hieu0606sunny/hue_rag/session_prompt/Project_Status.md
/home/hieu0606sunny/hue_rag/session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md
guides/README.md
guides/phase_0_mvp_foundation.md
guide của phase được giao/remediation: guides/phase_<id>_<short_name>.md
reports/hue_foods_rag_benchmark.md nếu phase liên quan model, retrieval, evaluation hoặc benchmark
Codex review report tương ứng nếu đang sửa findings
user report tương ứng nếu đang sửa feedback/remediation: reports/user_reports/phase_<id>_<short_name>_user_report.md
```

## Session Bootstrap Contract

Khi user chỉ cung cấp `Session_Prompt.md` và `IMPLEMENTER_WORKFLOW.md`, implementer tự:

1. xác định repo root và role Implementer;
2. đọc `Project_Status.md`, `guides/README.md` và Phase 0 foundation;
3. suy ra phase được giao từ user request, status snapshot và guide index;
4. đọc current phase guide và implementation-report template;
5. nếu là remediation, đọc Codex review và pending user report liên quan;
6. đọc benchmark ledger khi phase liên quan model, retrieval, evaluation hoặc benchmark.

Nếu không suy ra duy nhất một phase, thiếu file bắt buộc hoặc status không cho
phép implementation/remediation, dừng và hỏi user đúng một câu thay vì đoán.

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
- chỉ bắt đầu khi phase guide có trạng thái `ready`, hoặc `changes_requested`
  kèm exact remediation scope trong guide/Codex review/user feedback;
- xem canonical guide là read-only; mọi scope/interface/acceptance change phải
  quay lại user và Codex Reviewer;
- không sửa trạng thái trong guide; ghi `implementing` và
  `implementation_reported` trong handoff hoặc implementation report để Codex
  cập nhật trạng thái canonical;
- áp dụng `skills/karpathy-guidelines/SKILL.md` khi viết code để giữ assumptions
  rõ ràng, code đơn giản, thay đổi surgical, và success criteria có thể verify;
- trước mỗi phần quan trọng, thực hiện mini research theo guide; brainstorming
  với user phải hoàn tất trước khi phase chuyển sang `ready`;
- làm surgical changes, không refactor ngoài scope;
- tạo runtime `.py` dưới `backend/` khi phase yêu cầu;
- tạo/cập nhật notebook canonical dưới `notebooks/` cho mọi Phase 1–8;
- notebook phải import backend modules, không duplicate runtime logic;
- chạy smallest relevant verification trước, rồi broader checks khi cần;
- tự kiểm tra security, data safety, reliability, performance trước handoff;
- viết implementation report trong `/home/hieu0606sunny/hue_rag/reports/`;
- phản hồi Codex feedback bằng cách sửa code/docs/report của implementer khi
  cần.

Implementer không được:

- sửa Codex review files;
- tạo hoặc sửa file trong `reports/user_reports/`;
- cập nhật `Project_Status.md`;
- approve chính work của mình;
- commit hoặc push;
- chạy web enrichment, deploy hoặc dependency install ngoài approved scope;
- mở, `cat`, in, log hoặc expose nội dung/giá trị secrets từ `.env`,
  credentials, keys, tokens, auth files, hoặc private config; safe env-file
  loading cho approved runtime/validation được phép theo mục bên dưới;
- yêu cầu user paste secret vào chat.

## Python/Runtime (uv) Bắt Buộc

Chuỗi bắt buộc: `pyproject.toml + uv.lock -> uv -> project .venv -> uv run`.
Dựng/đồng bộ dependencies bằng `uv sync`; không dùng `pip`. Mọi lệnh chạy hoặc
xác minh project dùng `uv run python ...`, `uv run pytest ...`,
`uv run uvicorn api.app:app ...`, `uv run python -m <module>`; không gọi
`python`/`python3`/`pytest`/`uvicorn` từ system environment. System Python 3.12
chỉ dùng cho OS-level diagnostic ngoài project; chỉ đánh dấu runtime PASS dựa
trên lệnh chạy qua `uv run`.

## Env Keys Và Online Access

User cấp standing authorization ngày 2026-08-21 để coding agents chạy online,
dùng dependency/provider thật và nạp các key cần thiết đã có trong repo-root
`.env` cho approved implementation/validation scope.

Ưu tiên `uv` env-file loader; không `source` `.env` như shell script:

```bash
# Từ repo root
uv run --env-file .env python -m pytest backend/tests/ -q

# Từ backend/
uv run --env-file ../.env python -m pytest tests/ -q
```

- Chỉ kiểm tra key presence; không in value, `cat`/`grep` `.env`, dump toàn bộ
  environment hoặc đưa secret vào command/report/notebook/log.
- Network, Hugging Face Hub, Qdrant, OpenAI/OpenRouter và exact provider/model
  đã được approved được phép dùng mà không cần xin lại cho từng bounded run.
- Không mặc định đặt `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` hoặc
  `UV_OFFLINE`. Chỉ bật khi guide/test đang xác minh exact cache-only/offline
  contract; report phải nói rõ vì sao dùng và cache miss phải fail thật.
- Standing authorization không cho phép tự đổi provider/model, mở rộng phase,
  chạy full costly benchmark/judge ngoài approved budget, web enrichment,
  deploy, dependency install ngoài scope hoặc mutate active collection.

## Live-Only Validation Responsibilities

Implementer phải chạy runtime, notebook và backend tests qua dependency thật;
không dùng fake/mock client, fake runner, sample vector, replay fixture hoặc
real-mode guard. Preflight phải xác nhận dependency/model/provider thật có thể
truy cập bằng safe env-file loading và chỉ kiểm tra credential presence.

- Validation phải đọc curated/canonical input và actual service state đúng phase
  contract. Fixture, synthetic/sample data, hard-coded expected output hoặc
  output từ run cũ không được dùng làm evidence PASS; mutation test phải dùng
  isolated test data/collection và không thay thế read-only check trên active
  data khi acceptance yêu cầu.
- Evidence phải được thu mới từ exact command/run trong report, gồm actual
  counts, schema/payload observations, metrics và mọi failed/skipped/partial
  outcome; không fabricate, cherry-pick hoặc ghi expected result như observed.
- Dùng `gpt-5.4-nano` cho generation và API integration validation; chỉ dùng
  `gpt-5.4-mini` cho LLM-as-judge hoặc quality evaluation ghi rõ mục đích.
- Lỗi network, quota, provider, model hoặc Qdrant là validation failure thực tế;
  không được thay bằng fallback giả hoặc bỏ qua evidence.
- Active Hue collection chỉ read-only. Test có mutation phải dùng isolated
  Qdrant collection với marker rõ, xác minh exact name trước action và report
  cleanup thành công hay thất bại.
- Live logs được phép ghi full question, full answer, model, latency, usage và
  estimated cost. Không ghi credential, system prompt, raw provider payload hay
  full retrieved context.
- Report phải ghi actual provider, model, profile/config, data source/snapshot,
  call count, latency, usage/cost khi có, và mọi failed/skipped/partial run.

## Notebook Rules

Mọi implementation phase từ Phase 1 đến Phase 8 bắt buộc có notebook canonical
mang đúng số phase. Phase 0 được miễn; Phase 9 chỉ có notebook khi design mới đã
phê duyệt exact implementation scope và filename.

Notebook requirements:

- nằm trong `notebooks/`;
- import backend modules;
- không duplicate runtime pipeline logic;
- outputs rỗng trong repo;
- `execution_count` là `null`;
- Run All dùng runtime thật; thiếu model, Qdrant hay key phải fail actionable.
  Online model access/download được phép khi exact approved contract không yêu
  cầu cache-only. Không dùng fake fallback, replay fixture hoặc real-mode guard.
- Backend tests phải dùng dependency thật theo Live-Only Validation
  Responsibilities. Notebook phải ghi rõ prerequisite và quan sát thật.
- không lưu secrets, private paths nhạy cảm, raw headers, raw model payloads lớn,
  hoặc stack traces chứa sensitive data;
- Markdown cells ghi expected output hoặc cách user tự chạy lại nếu cần.

Notebook canonical:

```text
notebooks/01_backend_foundation.ipynb
notebooks/02_foods_data_and_chunking.ipynb
notebooks/03_embedding_models.ipynb
notebooks/04_qdrant_ingestion.ipynb
notebooks/05_retrieval_profiles.ipynb
notebooks/06_generation_and_api.ipynb
notebooks/07_evaluation.ipynb
notebooks/08_benchmark_model_selection.ipynb
```

## CodeGraph

CodeGraph đã được user phê duyệt và khởi tạo cho `hue_rag`. Implementer dùng
graph để hiểu code trước khi sửa, giới hạn blast radius và chọn tests; graph
không thay guide, source reads hoặc validation thực tế.

### Checkpoint bắt buộc

Tại đầu mọi session mới, chạy từ repo root:

```bash
codegraph status .
```

Xử lý kết quả theo đúng thứ tự:

- `Index is up to date`: tiếp tục công việc.
- Có pending files hoặc index stale: chạy `codegraph sync .`, sau đó chạy lại
  `codegraph status .` và chỉ tiếp tục khi index up to date.
- `Not initialized`: dừng và báo user/Reviewer; không tự chạy `codegraph init`.
- Sync/status lỗi hoặc vẫn stale sau sync: báo blocker; không đoán call graph.

Khi hoàn thành implementation hoặc correction theo một phase guide, trước khi
viết implementation report/handoff, chạy lại checkpoint:

```bash
codegraph status .
# Chỉ khi status báo stale hoặc pending:
codegraph sync .
codegraph status .
```

### Cách dùng trước và trong implementation

Trước khi sửa runtime code, dùng query hẹp theo task:

```bash
codegraph explore "Trace how <entry point> reaches <dependency or side effect>."
codegraph node <symbol-or-file>
codegraph callers <symbol>
codegraph callees <symbol>
codegraph impact <symbol>
```

Sau khi xác định changed files hoặc trước khi chạy tests:

```bash
git diff --name-only | codegraph affected --stdin
codegraph affected backend/path/to/module.py
```

Implementer dùng output để:

- xác định module và interface hiện có cần reuse;
- tìm callers/callees trước khi đổi signature hoặc behavior;
- kiểm tra blast radius có vượt approved guide hay không;
- chọn smallest relevant tests trước, rồi broader tests nếu shared behavior bị
  ảnh hưởng.

### Ví dụ (xác minh trên CodeGraph 1.5.0)

- `codegraph status .`: kết thúc bằng `✓ Index is up to date` khi index sạch;
  dir chưa init hiện `⚠ Not initialized`; thay đổi chưa sync hiện mục
  `### Pending sync:` rồi chạy `codegraph sync .`.
- `codegraph explore "<query>"`: trả về `Found N symbols across X files` kèm
  blast radius (callers + tests liên quan) và verbatim source theo file.
- `codegraph affected <file>`: liệt kê test files bị ảnh hưởng, ví dụ
  `codegraph affected backend/core/startup.py` → 4 test files.
- `codegraph query <keyword>`: tìm symbol khi chưa biết chính xác tên
  (FTS5); dùng trước khi `node`/`callers`/`impact` — nếu `impact` báo
  `Symbol not found`, kiểm tra lại tên bằng `query`.

Nếu CodeGraph chỉ ra scope ngoài approved guide, dừng và báo Reviewer/user;
không tự mở rộng implementation. Nếu graph thiếu symbol hoặc mâu thuẫn với
source, đọc source và dùng test evidence làm nguồn quyết định; ghi giới hạn vào
implementation report nếu ảnh hưởng validation.

Không đưa secrets, tokens, private endpoint hoặc credential path vào query.
Không chạy `codegraph init`, `codegraph uninit`, xóa `.codegraph/` hoặc bật
telemetry nếu user chưa yêu cầu rõ.

## Implementation Report

Sau khi hoàn tất implementation và validation của phase `ready`, hoặc exact
remediation của phase `changes_requested`, viết/cập nhật report để bàn giao
Codex review theo:

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
- notebook path, runtime-real behavior, expected observations và cách user tự kiểm tra;
- commands run;
- tests run;
- verification evidence;
- known issues;
- deviations from approved guide;
- provider/model/Qdrant access, model, call count, latency, usage, estimated cost
  và test-collection cleanup result;
- self-check về security, data safety, reliability, performance, tests, và
  notebooks.

## Self-Check Bắt Buộc Trước Handoff

Trước khi nói phase/milestone sẵn sàng cho Codex review, implementer phải check:

- security: env chỉ được nạp bằng safe loader cho approved command; không có
  secret value bị in, log, commit, dump hoặc expose;
- data safety: chunks, metadata, API responses, debug data, model errors, và
  result files chỉ chứa dữ liệu safe/intentional;
- reliability: failure paths thật được report rõ ràng, reset/reindex behavior
  của isolated test collection rõ ràng, import paths ổn định, và commands chạy
  từ `backend/` như guide;
- performance: không thêm repeated expensive model loads, unbounded work, hoặc
  bottlenecks không được document;
- tests: verification dùng dependency thật, evidence đủ model/cost/cleanup và
  không expose credential;
- notebooks: JSON hợp lệ, outputs rỗng, execution counts null, runtime-real và
  không expose credential;
- scope: `git diff --check` sạch và `git diff --name-only` chỉ chứa files thuộc
  approved guide hoặc deviation đã được user/Codex chấp thuận.

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
