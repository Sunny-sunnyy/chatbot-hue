# Hướng dẫn các phase của Hue Foods RAG

## Mục đích

Mỗi phase có một guide canonical để người dùng, Implementer và Reviewer cùng
hiểu phase tạo ra gì, phạm vi nào được phép làm và kết quả nào cần xác nhận.

Guide phải rõ ràng và vừa đủ. Không biến guide thành audit log, implementation
report hoặc danh sách edge cases phòng xa.

## Nguồn sự thật

Khi tài liệu khác nhau:

1. Yêu cầu mới nhất đã được user xác nhận.
2. `session_prompt/Session_Prompt.md`.
3. Workflow đúng vai trò.
4. Guide canonical của phase.
5. Design và implementation plan hỗ trợ.
6. Reports làm bằng chứng.
7. `session_prompt/Project_Status.md` làm snapshot hiện tại.

Mỗi phase có đúng một guide canonical. Design/plan không âm thầm override guide.
Report không tạo requirement hoặc quyền mở rộng scope.

## Vai trò

### Người dùng

- Chốt mục tiêu, phạm vi và lựa chọn quan trọng.
- Duyệt design trước implementation.
- Cho phép provider/model/data/run type trong guide.
- Chạy notebook và xác nhận khi phase đó thực sự cần notebook.
- Cấp quyền commit/push riêng khi muốn.

### Implementer

- Chỉ implement phase `ready` hoặc exact correction scope.
- Xem guide là read-only.
- Viết code đơn giản và chạy real system.
- Chỉ tạo/cập nhật notebook khi canonical guide yêu cầu vì có giá trị học tập.
- Viết implementation report.
- Không tự approve, sửa guide/status, user report, commit hoặc push.

### Codex Reviewer

- Review độc lập source, tests, real execution và notebook nếu phase có notebook.
- Coi over-engineering là finding và yêu cầu loại bỏ.
- Không sửa runtime thay Implementer.
- Viết Codex review và user report.
- Chỉ chuyển phase sang `approved` sau user confirmation.
- Không commit/push nếu chưa có yêu cầu riêng.

Chi tiết nằm trong hai role workflows.

## Vòng đời phase

```text
not_ready -> ready -> under_review -> approved
```

Nhánh ngoại lệ:

- `changes_requested`: còn blocker hoặc major cần Implementer sửa;
- `blocked`: thiếu quyền, dữ liệu, dependency hoặc external state cần thiết.

Luồng:

1. User và Reviewer duyệt design; Reviewer chuyển guide sang `ready`.
2. Implementer làm đúng guide và viết report.
3. Reviewer chuyển guide sang `under_review`, đọc source và chạy lại thật.
4. Nếu cần sửa, dùng `changes_requested`.
5. Nếu technical review đạt, guide vẫn `under_review`; user report ghi bằng
   tiếng Việt rằng đang chờ user xác nhận.
6. Sau khi user kiểm tra kết quả, và chạy notebook nếu phase có notebook,
   Reviewer chuyển guide thành `approved` và cập nhật project status.

Sau lần `changes_requested` thứ 4, dừng trước vòng sửa thứ 5 để audit lại
guide, design, plan, acceptance và findings. Nếu thiết kế quá phức tạp hoặc quá
khắt khe, phải thiết kế lại với user thay vì tiếp tục vá.

## Trạng thái Phase 0–9

| Phase | Guide | Trạng thái | Kết quả / bước kế tiếp |
|---:|---|---|---|
| 0 | `phase_0_mvp_foundation.md` | `approved` | Simplicity review đã approved; Phase 1 cũng đã trở lại `approved` |
| 1 | `phase_1_backend_skeleton.md` | `approved` | Simplicity implementation đã chạy thật, review và được user xác nhận |
| 2 | `phase_2_foods_markdown_chunking.md` | `approved` | Simplicity implementation đã chạy thật, review và được user xác nhận |
| 3 | `phase_3_embedding_sparse_representation.md` | `approved` | Simplicity implementation đã chạy thật, review và được user xác nhận |
| 4 | `phase_4_qdrant_ingestion.md` | `approved` | Giữ approval cũ; bước tiếp theo là simplicity review Phase 4 |
| 5 | `phase_5_retrieval_profiles_reranking.md` | `approved` | Giữ approval cũ; chờ review Phase 4 |
| 6 | `phase_6_generation_api.md` | `approved` | Giữ approval cũ; chờ review Phase 5 |
| 7 | `phase_7_retrieval_answer_evaluation.md` | `approved` | Evaluation đơn giản đã chạy thật, review và được user xác nhận |
| 8 | `phase_8_benchmark_model_selection.md` | `not_ready` | Chờ review và đơn giản hóa Phase 0–6 |
| 9 | `phase_9_agentic_rag_roadmap.md` | `not_ready` | Roadmap, chưa có implementation scope |

Milestone 6.1 thuộc Phase 6 và đã được user xác nhận.

## Thứ tự thực hiện

```text
Phase 0 simplicity review đã approved
-> review và đơn giản hóa Phase 1 -> Phase 6
-> chạy lại affected Phase 7 evaluation
-> cân nhắc Phase 8
```

Review Phase 0–6 theo dependency order để thay đổi nền tảng không làm invalid
phase cao vừa sửa. Repo và live system là nguồn đối chiếu chính: guide,
reports, source code, notebook nếu có và real run đủ để bắt đầu. Tài liệu ngoài do
user cung cấp chỉ dùng khi thực sự hữu ích; nếu thiếu mà còn lựa chọn quan
trọng, brainstorm với user trước khi duyệt design thay đổi.

## Code, test và real execution

Quy tắc đầy đủ nằm trong `Session_Prompt.md`:

- code rõ ràng, dễ hiểu và nhỏ nhất cần thiết;
- kỹ thuật nâng cao cần vấn đề thật và lợi ích được chạy thật chứng minh;
- test chỉ bảo vệ hành vi thật, không chạy theo số lượng;
- audit/xóa test theo ownership của phase trước khi chọn verification;
- full backend suite chỉ chạy cho broad shared change hoặc final Phase 0–6 check;
- evaluation 20 câu chỉ chạy khi thay đổi có thể ảnh hưởng chất lượng RAG;
- không mock/fake;
- completion evidence dùng real data, backend, Qdrant, model và API;
- paid API trong approved guide được phép;
- active Hue collection chỉ read-only.

Reviewer phải yêu cầu loại bỏ kỹ thuật over-engineered hoặc khó hiểu hơn mức
cần thiết.

## Notebook

Notebook chỉ tồn tại khi nó giúp con người hiểu hoặc quan sát một luồng quan
trọng tốt hơn code và guide. Canonical guide của từng phase phải nói rõ phase
có cần notebook hay không. Không tạo notebook để đủ số phase.

Phase 1 không cần notebook sau simplicity review. Notebook của Phase 2–8 được
đánh giá tại review của chính phase đó.

Notebook được giữ phải: mỗi cell làm một việc, giải thích ngắn trước code, gọi
hàm backend bằng code ngắn, không chứa validator/audit/test suite, có repository
outputs rỗng và được Run All thật trên temporary copy.

Phong cách bắt buộc:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

## Reports

```text
reports/phase_<id>_<short_name>_implementation_report.md
reports/phase_<id>_<short_name>_codex_review.md
reports/user_reports/phase_<id>_<short_name>_user_report.md
reports/phase_<id>_<short_name>_simplicity_review.md
```

- Implementation report: sáu mục, ghi việc đã làm và observed results.
- Codex review: sáu mục, ghi findings và independent real run.
- User report: năm mục, dễ hiểu và hướng dẫn user kiểm tra kết quả, gồm notebook
  khi phase có notebook.
- Simplicity review: living record ghi Before/After, capability được giữ, phạm
  vi ảnh hưởng, real verification, bug và cách xử lý khi review lại Phase 0–6.

Reports không tạo governance mới, không che lỗi và không dùng expected/fake/old
output làm fresh evidence.

## CodeGraph

CodeGraph là công cụ discovery tùy chọn. Reviewer/Implementer có thể dùng để tìm
call flow và blast radius theo hướng dẫn chi tiết trong workflow. Missing/stale
index không chặn task. Graph không thay source reads hoặc real verification.

## Decision record

Chỉ ghi decision record cho lựa chọn kiến trúc quan trọng, với ba field:

```text
Decision:
Reason:
Date +07:
```

Quyết định nhỏ không cần record riêng. Lịch sử chi tiết xem trong Git.

## Thay đổi guide

Implementer không sửa guide. Reviewer chỉ sửa guide sau:

- design được user duyệt;
- nhận implementation report để chuyển sang `under_review`;
- technical finding cần `changes_requested` hoặc `blocked`; hoặc
- user xác nhận để chuyển sang `approved`.

Mọi thay đổi provider, model, dimension, schema, active collection, destructive
action, phase boundary hoặc acceptance criterion phải được user duyệt.
