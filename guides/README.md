# Hướng dẫn các phase của Hue Foods RAG

## Mục đích

Thư mục `guides/` là nguồn hướng dẫn chính thức để người dùng, DeepSeek Implementer và Codex Reviewer cùng hiểu một phase sẽ tạo ra chức năng gì, cần quyết định gì trước khi làm, phải sửa những file nào và bằng chứng nào mới đủ để phê duyệt.

Bộ hướng dẫn này thay thế vai trò điều hành của các tài liệu spec và plan cũ. Mỗi phase có một file duy nhất, viết bằng tiếng Việt có dấu; code mẫu, command, model ID, configuration key, interface và tên file dùng English chuẩn.

## Nguồn sự thật và thứ tự ưu tiên

Khi có khác biệt giữa tài liệu, áp dụng thứ tự sau:

1. Yêu cầu mới nhất đã được người dùng xác nhận.
2. `session_prompt/Session_Prompt.md` và workflow đúng với vai trò hiện tại.
3. `guides/phase_0_mvp_foundation.md` cho các nguyên tắc xuyên suốt MVP.
4. Guide của phase đang làm cho scope, interface, nhiệm vụ và acceptance gate.
5. Codex review report đã phê duyệt phase.
6. DeepSeek implementation report của phase.
7. User report của phase cho bản giải thích dành cho người dùng.
8. `session_prompt/Project_Status.md` cho snapshot bàn giao hiện tại.

`Project_Status.md` không thay thế guide và không phải audit log. Report là bằng chứng của công việc đã thực hiện, không phải quyền tự động mở rộng scope.

## Vai trò của người dùng, DeepSeek Implementer và Codex Reviewer

### Người dùng

- Xác nhận mục tiêu, scope, lựa chọn kỹ thuật quan trọng và chi phí được phép.
- Phê duyệt kết quả brainstorming trước khi implementation bắt đầu.
- Cho phép riêng đối với live API, model download, collection deletion, commit hoặc push.
- Đọc user report, chạy hoặc kiểm tra notebook và xác nhận kết quả cuối của phase.
- Quyết định cuối cùng khi chất lượng, latency và cost tạo ra trade-off không có đáp án tuyệt đối.

### DeepSeek Implementer

- Đọc guide như execution contract chỉ đọc.
- Chỉ implement phase có trạng thái `ready` và đúng scope đã phê duyệt.
- Thực hiện từng phần nhỏ, kiểm chứng sau mỗi phần quan trọng.
- Tạo notebook bắt buộc cho Phase 1–8, giữ output rỗng và không gọi dịch vụ ngoài mặc định.
- Viết `reports/phase_<id>_<short_name>_implementation_report.md` sau khi implementation và validation thực sự hoàn tất.
- Không tạo hoặc sửa file trong `reports/user_reports/`.
- Không tự sửa guide để hợp thức hóa deviation, không tự phê duyệt phase, không cập nhật `Project_Status.md`, không commit và không push.

### Codex Reviewer

- Là gatekeeper và owner của nội dung canonical trong `guides/`.
- Điều phối brainstorming theo đúng mức của phase; ghi rõ quyết định, bằng chứng và revisit trigger.
- Review độc lập code, test, notebook, report, security, data safety, reliability và performance.
- Ghi `reports/phase_<id>_<short_name>_codex_review.md` với verdict rõ ràng.
- Khi technical review đạt, tạo user report dễ hiểu và chuyển phase sang `awaiting_user_confirmation`.
- Chỉ sau khi người dùng xác nhận mới đổi trạng thái tiếng Việt trong user report, chuyển phase sang `approved`, cập nhật `Project_Status.md`, commit và push approved phase package.
- Không implement thay DeepSeek trong một phase runtime, trừ khi người dùng thay đổi scope và giao nhiệm vụ rõ ràng.

## Vòng đời phase

Luồng chuẩn:

```text
not_ready
  -> brainstorming_required
  -> ready
  -> implementing
  -> implementation_reported
  -> under_review
  -> awaiting_user_confirmation
  -> approved
```

Nhánh ngoại lệ:

- `changes_requested`: reviewer tìm thấy blocker hoặc major issue; quay lại implementer sau khi scope vẫn còn hiệu lực.
- User phát hiện vấn đề ở user report hoặc notebook cũng chuyển phase về `changes_requested`.
- `blocked`: không thể tiến triển vì thiếu quyết định, quyền truy cập, dependency, dữ liệu hoặc thay đổi trạng thái bên ngoài.
- `design_only`: chỉ đủ để nghiên cứu và thiết kế; tuyệt đối không phải quyền implement.
- `completed`: milestone nền tảng đã chốt, không có runtime deliverable cần review lại.

Chỉ Codex Reviewer mới thay đổi trạng thái canonical trong guide sau khi có bằng chứng và quyền phù hợp.

Quyền ghi trạng thái được tách rõ:

- Codex Reviewer cập nhật trạng thái canonical trong guide: `not_ready`,
  `brainstorming_required`, `ready`, `under_review`,
  `awaiting_user_confirmation`, `approved`, `changes_requested` hoặc `blocked`.
- `implementing` và `implementation_reported` là trạng thái vận hành do DeepSeek
  ghi trong handoff hoặc implementation report; DeepSeek không sửa guide.
- Khi nhận implementation report, Codex đối chiếu scope rồi chuyển guide từ
  `ready` sang `under_review` trước khi review.
- Sau technical verdict đạt, Codex tạo user report với trạng thái tiếng Việt
  đang chờ xác nhận và chuyển guide sang `awaiting_user_confirmation`. User
  confirmation mới cho phép Codex đổi user report sang trạng thái đã xác nhận,
  chuyển guide sang `approved`, cập nhật
  `Project_Status.md`, commit/push và mở phase tiếp theo.

## Mức brainstorming

| Mức | Ý nghĩa | Yêu cầu tối thiểu |
|---|---|---|
| `Level 0 - locked` | Phase đã hoàn tất hoặc phê duyệt | Không brainstorm lại trừ khi người dùng mở scope mới |
| `Level 1 - focused` | Thay đổi nhỏ, ít trade-off | Xác nhận mục tiêu, file, validation và stop condition |
| `Level 2 - standard` | Có interface hoặc provider decision | Làm rõ data flow, 2–3 hướng hợp lý, lựa chọn, test và failure policy |
| `Level 3 - deep` | Nhiều biến ảnh hưởng chất lượng/cost | Tách experiment groups, controlled variables, metric, budget và rollback |
| `Level 4 - separate approved design` | Architecture mới hoặc agent orchestration | Tạo design riêng, review riêng và phê duyệt lại trước implementation |

Chỉ dùng rich elicitation khi còn ít nhất hai chiều mơ hồ quan trọng và mỗi chiều có ít nhất ba hướng hợp lý. Câu hỏi phải làm thay đổi scope, design, test hoặc implementation plan.

## Danh mục Phase 0–9

| Phase | Guide | Trạng thái hiện tại | Brainstorming | Kết quả chính |
|---:|---|---|---|---|
| 0 | `phase_0_mvp_foundation.md` | `completed` | Level 0 | Kiến trúc, provider boundary, data flow và governance của MVP |
| 1 | `phase_1_backend_skeleton.md` | `approved` | Level 1 | Mã nền, notebook và báo cáo đã được người dùng xác nhận |
| 2 | `phase_2_foods_markdown_chunking.md` | `approved` | Level 2 | 572 đoạn, giới hạn 400 ký tự, bảng và nhãn đã được xác nhận |
| 3 | `phase_3_embedding_sparse_representation.md` | `approved` | Level 2 | Dense embedding provider và sparse representation |
| 4 | `phase_4_qdrant_ingestion.md` | `approved` | Level 2 | Một active Qdrant collection và dense+sparse points |
| 5 | `phase_5_retrieval_profiles_reranking.md` | `approved` | Level 3 | Ba retrieval profiles, BM25, reranking và context |
| 6 | `phase_6_generation_api.md` | `not_ready` | Level 2 | Grounded answer generation và JSON API |
| 7 | `phase_7_retrieval_answer_evaluation.md` | `not_ready` | Level 3 | Retrieval metrics và LLM-as-judge |
| 8 | `phase_8_benchmark_model_selection.md` | `not_ready` | Level 3 | Controlled benchmark và lựa chọn cấu hình cuối |
| 9 | `phase_9_agentic_rag_roadmap.md` | `design_only` | Level 4 | Roadmap thiết kế Agentic RAG sau MVP |

Phase sau không được implement trước khi dependency phase trước đạt gate, trừ khi người dùng phê duyệt một thay đổi thứ tự có phân tích blast radius.

## Quy trình thực hiện, báo cáo, review và cập nhật trạng thái

1. Codex và người dùng brainstorm theo mức của phase.
2. Codex cập nhật guide với quyết định đã chốt và chuyển phase sang `ready`.
3. DeepSeek implement theo guide, chạy validation và tạo implementation report.
4. Codex review độc lập, tạo Codex review report.
5. Nếu technical review đạt, Codex tạo user report với trạng thái tiếng Việt đang chờ xác nhận và chuyển guide sang `awaiting_user_confirmation`.
6. Người dùng đọc user report, kiểm tra notebook và xác nhận hoặc yêu cầu sửa.
7. Khi người dùng xác nhận, Codex đổi trạng thái tiếng Việt trong user report, chuyển guide thành `approved` và cập nhật `Project_Status.md`.
8. Xác nhận hoàn tất phase đồng thời cho phép Codex audit allowlist, commit và push đúng approved phase package.

Tên report bắt buộc:

```text
reports/phase_<id>_<short_name>_implementation_report.md
reports/phase_<id>_<short_name>_codex_review.md
reports/user_reports/phase_<id>_<short_name>_user_report.md
```

Hai nhóm report có audience riêng:

- `reports/*.md` là technical evidence để DeepSeek Implementer và Codex Reviewer đọc và ghi.
- `reports/user_reports/*.md` là bản giải thích tiếng Việt dễ hiểu để người dùng đọc; chỉ Codex Reviewer tạo hoặc cập nhật.

User report không được bịa validation, che giấu failed/skipped checks hoặc thay đổi scope đã phê duyệt. Nếu khác technical evidence, Codex phải sửa user report trước khi xin user confirmation.

Benchmark xuyên phase được tổng hợp tại `reports/hue_foods_rag_benchmark.md`; per-question outputs ở dạng JSONL chỉ được tạo khi phase evaluation tương ứng đã implement.

## CodeGraph trong workflow

CodeGraph được dùng cho runtime discovery và impact analysis từ Phase 4 trở đi.
Reviewer và Implementer kiểm tra `codegraph status .` trước task runtime, rồi
dùng graph để tìm call flow, symbol ownership, affected tests và blast radius.
Graph không thay thế source reads, `rg`, tests, notebooks hoặc technical
evidence và không tự tạo quyền approve phase. Telemetry giữ ở trạng thái tắt;
`.codegraph/` là local ignored artifact.

```text
Decision: Áp dụng CodeGraph cho runtime discovery và impact analysis, nhưng không dùng làm approval evidence duy nhất.
Approved by: User
Approval date +07: 2026-08-12
Evidence: User xác nhận áp dụng CodeGraph trước khi bắt đầu brainstorming Phase 4.
Affected scope: Reviewer/Implementer workflow và Phase 4–8 runtime work.
Revisit trigger: Graph không ổn định, gây context overhead không chấp nhận được hoặc không cải thiện review/implementation workflow.
```

## Quy tắc benchmark và live API approval

- Bắt đầu bằng baseline local nhẹ đã dùng trong `llm_rag` trước khi thử OpenRouter.
- Mỗi experiment group chỉ thay đổi một nhóm biến đã khai báo.
- Thay embedding model hoặc vector dimension bắt buộc reindex; không request-level fallback giữa hai vector space.
- Benchmark không được silent fallback. Model thực tế, provider, profile và lỗi phải được ghi đúng.
- Live OpenAI/OpenRouter call, full answer-judge run, model download và chi phí trả phí đều cần người dùng phê duyệt rõ ràng trước từng đợt chạy.
- Không ghi API key, raw header, private payload hoặc chain-of-thought vào guide, report hay artifact.

## Quy tắc thay đổi guide

Mọi thay đổi làm ảnh hưởng provider, model, dimension, dependency, schema, active collection, destructive reset, live cost, acceptance criterion hoặc phase boundary phải quay lại người dùng và Codex Reviewer.

Mỗi quyết định mới phải ghi:

```text
Decision
Approved by
Approval date +07
Evidence
Affected scope
Revisit trigger
```

Guide của Phase 1–2 giữ nguyên lịch sử kiểm tra kỹ thuật. Phần notebook và báo
cáo dành cho người dùng đã được xác nhận ngày 2026-08-09; không viết lại bằng
chứng kỹ thuật cũ để làm thay đổi lịch sử.
