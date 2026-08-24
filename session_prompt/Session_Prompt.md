# Session Prompt

Repo:

```text
/home/minhhieu/hue_rag
```

Giao tiếp với người dùng bằng tiếng Việt. Code, comments, docstrings và tên
biến dùng English chuẩn.

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
bằng web nếu người dùng chưa duyệt phạm vi dữ liệu.

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
skills/karpathy-guidelines/SKILL.md
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
- Task chỉ sửa docs hoặc không đổi logic có thể không cần automated test.
- Không dùng mock hoặc fake trong test hay implementation.
- Test pass không thay thế live integration run.

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
-> mới cân nhắc Phase 8
```
