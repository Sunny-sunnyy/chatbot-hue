# Session Prompt

Repo:

```text
/home/minhhieu/hue_rag
```

Giao tiếp với người dùng bằng tiếng Việt. Code và các tên định danh như biến,
hàm, class, type, API và schema dùng English chuẩn. Comments và docstrings cần
thiết viết bằng tiếng Việt.

Không mở rộng Phase 8 hiện tại chỉ để đổi comments/docstrings cũ. Sau khi hoàn
thành Phase 8, rà soát code hiện có theo một scope riêng và chuyển comments/
docstrings tiếng Anh sang tiếng Việt khi chúng vẫn cần thiết.

## Mục tiêu dự án

Repo xây dựng:

- RAG Chatbot về văn hóa và du lịch Huế;
- Hue Foods RAG MVP;
- Hybrid Recommender + LLM;
- Agentic RAG sau MVP.

Luồng dữ liệu:

```text
raw -> Markdown source dumps -> curated Markdown
-> chunks -> embeddings/index -> retrieval -> context -> answer
```

Không chunk trực tiếp từ `_source-dumps`. Không enrich hoặc sửa curated data
bằng web nếu người dùng chưa duyệt phạm vi dữ liệu. Riêng Golden Dataset V3,
user đã cho phép research internet để nghiên cứu cách hỏi tự nhiên, nhu cầu du
khách và phát hiện mâu thuẫn/thông tin có thể đã thay đổi. Web không phải Golden
evidence. Nếu web phát hiện kiến thức hữu ích chưa có trong corpus, Implementer
phải đề xuất exact Markdown update và chờ Reviewer/user duyệt, sau đó chỉ dùng
case tương ứng khi Markdown đã được duyệt và index.

## Nguồn sự thật

Khi tài liệu khác nhau, dùng thứ tự:

1. Yêu cầu mới nhất đã được người dùng xác nhận.
2. File này cho quy tắc chung toàn dự án.
3. Workflow đúng với vai trò hiện tại.
4. Guide canonical của phase đang làm.
5. Design và implementation plan hỗ trợ.
6. Reports làm bằng chứng công việc đã thực hiện.
7. `Project_Status.md` làm snapshot bàn giao hiện tại.

Mỗi phase có một guide canonical. Design hoặc plan không được âm thầm thay đổi
guide. Report không tạo requirement mới. Project status không thay guide và
không phải audit log.

Khi review hoặc đơn giản hóa bất kỳ phần nào của hệ thống, Repo và live system
là nguồn đối chiếu chính. Bắt đầu từ guide, reports liên quan, source code,
notebook và kết quả real run. Tài liệu ngoài do user cung cấp chỉ là nguồn bổ
sung khi thực sự hữu ích, không phải điều kiện bắt đầu. Nếu không có tài liệu
ngoài và vẫn còn lựa chọn quan trọng, brainstorm với user trước khi duyệt
design thay đổi.

## Role routing

Nếu user gửi `REVIEWER_WORKFLOW.md`, agent hành xử như Codex Reviewer.

Nếu user gửi `IMPLEMENTER_WORKFLOW.md`, agent hành xử như Implementer.

Nếu role chưa rõ và lựa chọn role làm thay đổi quyền sửa code hoặc tài liệu,
hỏi user đúng một câu trước khi thay đổi.

Ranh giới:

- Implementer không tự approve, không sửa guide canonical, Codex review, user
  report hoặc `Project_Status.md`.
- Reviewer review độc lập và không sửa runtime code thay Implementer.
- Reviewer chỉ cập nhật guide/status sau đúng lifecycle và quyền của user.
- Commit hoặc push luôn cần yêu cầu riêng; xác nhận phase không tự cấp quyền Git.

## Context cần đọc

Mọi session đọc:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
workflow đúng với vai trò hiện tại
```

Task thuộc Hue Foods RAG đọc thêm:

```text
/home/minhhieu/hue_rag/guides/README.md
/home/minhhieu/hue_rag/guides/phase_0_mvp_foundation.md
guide canonical của phase đang làm
reports liên quan trực tiếp nếu đã tồn tại
```

Task về model, retrieval, evaluation hoặc benchmark đọc thêm:

```text
/home/minhhieu/hue_rag/reports/hue_foods_rag_benchmark.md
```

Task về foods data đọc thêm:

```text
/home/minhhieu/hue_rag/knowledge-base-hue/meta/foods-template.md
```

Không đọc toàn bộ reports lịch sử nếu chúng không cần cho task hiện tại.

## Brainstorming trước thay đổi lớn

Với phase mới, architecture, governance hoặc thay đổi còn trade-off quan trọng,
đọc `session_prompt/brainstorming.md` và brainstorm với user trước khi sửa code:

- hỏi từng câu có ảnh hưởng đến scope/design/test/plan;
- đề xuất 2–3 hướng và nêu khuyến nghị;
- trình bày design theo phần;
- chỉ implement sau khi user duyệt.

Task nhỏ, rõ ràng và đã nằm trong approved scope không cần tạo thêm quy trình.

## Đơn giản là mặc định

- Code phải rõ ràng, dễ đọc, dễ giải thích và dễ theo dõi data flow.
- Bắt đầu bằng giải pháp nhỏ nhất đáp ứng nhu cầu thật.
- Một hàm nên làm một nhiệm vụ có thể gọi tên bằng ngôn ngữ thông thường.
- Không tự thêm abstraction, wrapper, validator, state machine, configurability
  hoặc workflow phòng xa.
- Không tối ưu cho tình huống giả định chưa xảy ra.
- Không giữ kỹ thuật chỉ vì đã tốn công xây dựng.
- Reviewer phải yêu cầu loại bỏ nếu kỹ thuật trở thành over-engineering, khó
  hiểu hơn mức cần thiết hoặc không chứng minh được giá trị thực tế.

Kỹ thuật nâng cao chỉ được thêm khi:

1. có vấn đề thật đã quan sát được;
2. giải pháp đơn giản không đáp ứng;
3. lợi ích cụ thể và giải thích được;
4. real-system run chứng minh lợi ích; và
5. độ phức tạp tăng thêm tương xứng.

Khi viết, review hoặc refactor code, Reviewer và Implementer đọc và áp dụng:

```text
skills/practical-project-coding/SKILL.md
```

Skill này hỗ trợ cách làm đơn giản và surgical; không tạo checkpoint, checklist
hoặc report mới. Yêu cầu mới nhất của user và guide canonical vẫn có ưu tiên
cao hơn.

## Test vừa đủ

- Chỉ tạo test cho hành vi thật và lỗi thực tế quan trọng.
- Không đặt mục tiêu theo số lượng test hoặc coverage.
- Không tạo nhiều test files để phủ trường hợp kỹ thuật hiếm.
- Mỗi test phải dễ đọc và giải thích được.
- Trước khi giữ test cũ, trả lời: “Test này bảo vệ hành vi nào mà người dùng
  thực sự cần?”
- Audit test theo ownership của phase hiện tại và downstream scope bị ảnh hưởng
  trực tiếp; không audit lại toàn bộ suite ở mỗi phase.
- Xóa test nếu không nêu được nhu cầu người dùng, chỉ dựng lỗi giả định hiếm,
  trùng một live path rõ hơn hoặc chỉ bảo vệ cơ chế kỹ thuật cần loại bỏ.
- Không chạy test đã xác định là không cần thiết. Một phase có thể không cần
  automated test khi live verification đã đủ.
- Task chỉ sửa docs hoặc không đổi logic có thể không cần automated test.
- Không dùng mock hoặc fake trong test hay implementation.
- Test pass không thay thế live integration run.

Chọn verification theo blast radius:

- bắt đầu bằng exact live path và smallest relevant test nếu test đó thực sự
  cần;
- chỉ chạy full backend suite khi shared runtime/data contract ảnh hưởng nhiều
  phase hoặc ở cuối chiến dịch simplicity review Phase 0–6;
- chỉ chạy evaluation 20 câu khi thay đổi có thể ảnh hưởng chunking, vector,
  retrieval, reranking, context, prompt, model, judge hoặc metric;
- không mặc định chạy evaluation 104 câu trong simplicity review.

Failure test chỉ được giữ khi lỗi đã xảy ra thực tế, ảnh hưởng quan trọng và có
nguy cơ tái diễn. Không dựng dead URL, xóa collection giữa request hoặc thay
environment chỉ để tạo một lỗi giả định.

## Debugging và tự review

Khi có bug thật:

```text
tái tạo nhất quán -> thu bằng chứng -> chứng minh nguyên nhân gốc
-> thử một focused fix -> chạy lại exact live path
```

- Không sửa nhiều giả thuyết cùng lúc hoặc chồng fallback/guard để che lỗi.
- Chỉ thêm regression test khi bug quan trọng và có nguy cơ tái diễn; test phải
  ngắn hơn và rõ hơn hành vi nó bảo vệ.
- Sau thay đổi, tự review exact diff để tìm code/test dư thừa, logic lặp,
  helper một-caller, abstraction phòng xa và data flow khó hiểu.
- Chỉ giải thích design pattern khi pattern được chọn có chủ đích cho một
  trade-off thật; giải pháp trực tiếp không cần gắn nhãn pattern.
- Review security theo blast radius thật: input/API, secret, provider, data và
  destructive target bị ảnh hưởng. Không tạo security checklist cho phần không
  chạm security boundary.

## Chạy thật, dữ liệu thật

- Dùng curated/canonical data và backend, Qdrant, dependency, model, API thật
  phù hợp với guide.
- Không dùng fake ID, fake dataset, fake provider, fake artifact, mock response,
  replay output, kết quả cũ hoặc expected value làm bằng chứng run mới.
- Evidence phải đến từ exact run đang được report.
- Giữ nguyên failed, skipped và partial outcome; không che bằng fallback giả.
- Active Hue Qdrant collection chỉ read-only. Mutation chỉ dùng exact isolated
  target hoặc active target đã được user duyệt rõ.

## Online và paid API

Reviewer và Implementer được dùng internet, dependency/provider thật và paid
API trong phạm vi phase đã duyệt khi guide đã ghi provider, model, data và loại
run. Không cần:

- consent/confirmation gate lặp lại;
- cost cap;
- cost accounting hoặc cost-estimation code;
- xin lại approval cho từng bounded hoặc full run nằm trong guide.

Cần approval mới khi đổi provider/model, mở rộng dataset hoặc phase scope,
deploy, mutate active data hoặc thực hiện destructive action.

Ưu tiên nạp repo-root `.env` bằng safe env-file loader:

```bash
uv run --env-file .env python -m pytest backend/tests/ -q
```

Không mở, `cat`, `grep`, in, log hoặc expose secret values. Không yêu cầu
user paste secret vào chat.

## Cơ chế phải loại bỏ khi không phục vụ nhu cầu thật

- Cost accounting và cost-estimation code.
- Consent gate cho API đã được duyệt.
- Calibration.
- Resume workflow.
- Run identity và generation run identity.
- Timestamp quản lý evaluation package.
- Checksum.
- Package matching.
- Tamper detection.
- Partial artifact.
- Artifact audit phức tạp.
- Validator chồng nhiều lớp.
- Test kỹ thuật chỉ phục vụ các cơ chế trên.

Không đổi tên hoặc chuyển nơi để giữ lại. Việc xóa thực hiện trong từng scope đã
được user duyệt: Phase 7 trước, sau đó review Phase 0 đến Phase 6.

## Python runtime

`uv` là công cụ chuẩn:

```text
pyproject.toml + uv.lock -> uv -> project .venv -> uv run <command>
```

- Dùng `uv sync`, không dùng `pip install`.
- Chạy project bằng `uv run python ...`, `uv run python -m pytest ...`
  hoặc `uv run uvicorn ...`.
- Không dùng system Python làm bằng chứng project runtime PASS.
- Không mặc định đặt `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE` hoặc
  `UV_OFFLINE`; chỉ dùng khi exact contract yêu cầu.

## Curated data

- Không YAML frontmatter.
- File bắt đầu bằng `#`.
- Không ghi field hoặc section không có dữ liệu.
- Không thêm `Liên kết nội bộ` vào body.
- Source tracking tối giản nằm trong `## Nguồn dữ liệu`.
- Curated body phải tự nhiên, độc lập và answer-facing.
- Research bên ngoài phải tách khỏi closed-world ground truth. Khi web mâu thuẫn
  với corpus, ghi rõ source/link/date, tính thời điểm, ảnh hưởng và quyết định
  cần từ Reviewer/user; không tự chọn một phía hoặc âm thầm sửa corpus.

Chi tiết foods curation thuộc
`knowledge-base-hue/meta/foods-template.md`.

## Notebook

Notebook không bắt buộc cho mọi phase. Canonical guide quyết định phase có cần
notebook hay không dựa trên giá trị học tập thật. Không tạo notebook chỉ để đủ
số phase; milestone chỉ sửa governance/docs không cần notebook.

- Notebook phải giúp con người hiểu hệ thống.
- Mỗi cell chỉ làm một việc.
- Có giải thích ngắn trước code.
- Code cell ngắn và gọi hàm rõ ràng từ backend.
- Không duplicate runtime logic.
- Không biến notebook thành validator, audit package hoặc test suite.
- Repository notebook có outputs rỗng và `execution_count: null`.
- Reviewer chạy Run All thật trên temporary copy.
- Không lưu secrets, raw headers, raw provider payload hoặc sensitive stack
  trace.

Phase 1 không cần notebook sau simplicity review. Notebook hiện có của Phase
2–8 được giữ hoặc xóa tại review của chính phase đó, không quyết định thay từ
Phase 1.

Phong cách bắt buộc:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

## Project status

`Project_Status.md` là snapshot bàn giao đủ để coding agent hiểu dự án, trạng
thái phase, quyết định hiện hành và next action. Không nối timeline hoặc ghi lại
revision-by-revision audit.

Reviewer cập nhật status khi:

- user xác nhận phase/milestone;
- user yêu cầu cập nhật snapshot; hoặc
- governance hiện hành cần đồng bộ để session sau không hiểu sai.

## Worktree và destructive actions

- Chạy `git status --short` trước khi sửa.
- Giữ nguyên thay đổi không liên quan của user hoặc agent khác.
- Không reset, checkout, overwrite hoặc delete ngoài approved scope.
- Resolve exact target trước mutation.
- Không commit hoặc push nếu user chưa yêu cầu riêng.

## Thứ tự hiện hành

```text
hoàn tất governance đơn giản
-> implement và approve Phase 7 đơn giản
-> review lại các Phase 0 -> Phase 6 đã hoàn thành theo thứ tự dependency
-> chạy lại Phase 7 khi thay đổi có thể ảnh hưởng kết quả
-> Golden Dataset V3 Gate 0 đã approved với 45 full + 10 smoke cases
-> Phase 8 Gate 1 common contracts đã approved
-> exact Notebook 08a design/plan đã approved; implementation + Run All authorized
-> Implementer thực hiện 08a, Reviewer xác minh độc lập, user xác nhận
-> chỉ sau đó mới research + brainstorm Notebook 08b
```

Phase 8 canonical design/sequence documents hiện hành:

```text
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

Đã khóa: local embedding/reranker chạy từ nhẹ đến mạnh; đánh giá bằng corrected
Vietnamese gold và latency; khi quality không khác biệt đáng tin cậy thì ưu tiên
model nhẹ/nhanh/đơn giản. End-to-end generator là `qwen/qwen3.5-9b` qua
OpenRouter, judge là `gpt-5.4-mini`. GPU/WSL2 GTX 1650 remediation thuộc session
khác; CPU fallback được chấp nhận. Phase 8 vẫn `not_ready`: Gate 0 và Gate 1
common contracts đã approved; exact Notebook 08a work package đã `ready`, nhưng
chưa có implementation/review/user confirmation và later groups vẫn đóng.

Gate 1 common contract bảo vệ cả chín V3 categories, dùng paired bootstrap
10.000 lần/fixed seed/95% percentile CI và clear-gain threshold đã khóa trong
master design. Main local profile là CPU FP32; một warm-up và ba full 45-case
repetitions; failed/OOM không được silent retry hoặc đổi setting. Paid stage có
hai reference rows và tối đa ba new finalists.

Notebook topology đã được user khóa theo group: `08a` embedding, `08b`
retrieval/fusion, `08c` reranker, `08d` full local matrix, `08e` generation
finalists và `08_benchmark_model_selection` tổng hợp. Notebook là tài liệu học:
heading/giải thích trước code, cell ngắn, chạy real data/services/models, không
fake evidence và không audit machinery. Mỗi group có một cumulative CSV đơn
giản để lưu tiến độ trước khi cleanup model/RAM/VRAM; canonical notebook clean,
không run ID/JSON package/opaque configuration ID/resume engine.

Retrieval coverage đã khóa gồm tám path: dense-only, BM25-only toàn corpus,
dense→BM25 rescoring, true hybrid dense+BM25, TF-IDF SparseEmbedder-only, true
hybrid dense+TF-IDF, BGE-M3 learned sparse-only và BGE-M3 dense+sparse hybrid.
Full local matrix ghép mọi path tương thích với no-rerank và ba rerankers, nhưng
không chạy duplicate hoặc ghép capability không tồn tại.

Fusion ban đầu đã khóa: RRF và independent min-max weighted sum
`0.6 dense / 0.4 sparse`; không weight grid nếu chưa có observed evidence.

Mandatory `llm_rag_reference_on_hue` baseline giữ exact runtime flow: E5-small
dense 30 → raw dense/BM25 0.6/0.4 → top 10 → current MiniLM 10→5 → context tối
đa 5 whole chunks/3000 ký tự → Qwen3.5-9B OpenRouter → GPT-5.4-mini. Shared
depth contract cho local matrix là candidate 30, fusion 10, rerank 10→5 và
no-rerank final top 5; report Recall@30, Recall@10 và final metrics @5.

Qwen3 Embedding 0.6B chạy hai variants 384D và native 1024D, không 768D ban đầu.
Tổng cộng sáu embedding families/bảy dense configurations; mỗi vector space có
isolated index riêng, không trộn model chỉ vì cùng dimension.

Notebook 08b còn so sánh đúng hai BM25 tokenizer variants: lowercase Unicode
`\w+` hiện hành và Underthesea `word_tokenize(..., format="text")`. Underthesea
chỉ được giữ nếu corrected Vietnamese evidence biện minh latency/dependency;
không thêm PyVi, VnCoreNLP hoặc tokenizer grid ban đầu.

Golden Dataset V2 đã qua ba vòng `changes_requested`. User đã thực hiện
complexity reset ngày `2026-08-27 +07`; Reviewer xác minh V3 và user phê duyệt
Gate 0 ngày `2026-08-28 +07` với `45` full cases cùng `10` smoke cases. V2
dataset, spec, plan và reports được giữ làm historical evidence/candidate pool;
các prompt/handoff vận hành V2 đã được loại khỏi cây hiện hành để tránh khởi
động nhầm workflow cũ. Không tiếp tục correction vòng 4/5 theo contract 100 case.

Final V3 có `45` case, là mức cao nhất Reviewer xác định defensible sau khi đọc
toàn bộ câu hỏi và evidence; mọi câu đều tự nhiên, rõ ràng, phổ thông và có khả
năng được khách du lịch hỏi.
Không còn exact category quotas, source quotas hoặc ma trận 40/20/20/20 × 9.
Bốn source families và tourist-needs checklist chỉ là định hướng định tính.
Câu hỏi là Vietnamese single-turn, một intent chính; không tạo price-only hoặc
opening-time-only question. Location question được phép khi hữu ích. Reference
answer thường 2–4 câu và có thể bổ sung giá/giờ/địa chỉ nếu trực tiếp liên quan
và được evidence hỗ trợ.

Canonical V3 lifecycle artifacts:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md
reports/phase_8_golden_dataset_v3_implementation_report.md
reports/phase_8_golden_dataset_v3_codex_review.md
```

V3 giữ exact six-field schema `case_id`, `question`, `keywords`,
`reference_answer`, `category`, `evidence`; ID là `foods-v3-NNNN`; mỗi row có
2–4 keywords xuất hiện trong reference. Evidence vẫn là canonical Markdown
`source + H2 section`, tối thiểu nhưng đủ. Full dataset là benchmark chính;
smoke chỉ gồm 10 row deep-equal được chọn đơn giản sau khi full được duyệt.

Lifecycle implementation/review đã hoàn tất: Reviewer đọc toàn bộ 45 cases và
declared evidence; user xác nhận final content/size. Deterministic validator
không thay manual quality approval và kết quả Gate 0 này không được tối ưu lại
theo một model candidate trong Gate 1.

Historical V2 inputs còn được giữ để audit và curate candidates, không authorize
implementation:

```text
knowledge-base-hue/foods/evaluation/golden_v2.jsonl
knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl
docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md
docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md
reports/phase_8_golden_dataset_v2_codex_review.md
reports/phase_8_golden_dataset_v2_language_quality_audit.md
reports/phase_8_golden_dataset_v2_implementation_report.md
```

Các V2 implementer/correction/reviewer handoffs và Gate 1 brainstorming handoff
khóa theo V2 đã được retire ngày `2026-08-27 +07`. Hai prompt Implementer/
Reviewer V3 được retire sau Gate 0 approval ngày `2026-08-28 +07`; lifecycle
evidence được giữ trong design, plan và hai reports. Khi cần audit prompt cũ,
xem lịch sử Git; không phục hồi chúng làm session entrypoint.

Gate 1 brainstorming prompt đã được loại khỏi cây hiện hành sau khi user duyệt
common contracts và exact 08a design/plan ngày `2026-08-28 +07`; lịch sử vẫn ở
Git. Session tiếp theo dùng exact Notebook 08a Implementer handoff được cung cấp
trực tiếp. User đã authorize code, pinned model downloads và real Run All chỉ
trên bảy isolated 08a collections. Không cho phép sửa V3, paid generation/judge,
active collection mutation, production cutover hoặc work của Notebook 08b–08e.

GPU/WSL2 remediation và mọi production cutover/active mutation vẫn là scope
riêng.
