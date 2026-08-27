# Prompt handoff — Implement Golden Dataset V2

> **Historical — superseded 2026-08-27:** Không dùng prompt này để bắt đầu
> session mới. User đã duyệt Golden Dataset V3 complexity reset. Dùng
> `session_prompt/phase_8_golden_dataset_v3_implementer_prompt.md`.

Bạn là **Codex Implementer** cho repository:

```text
/home/minhhieu/hue_rag
```

Nhiệm vụ duy nhất của session này là thực hiện Golden Dataset V2 theo spec và
implementation plan đã được user duyệt. Không brainstorming lại các quyết định
đã khóa, không chạy Phase 8 model benchmark và không chuyển production.

## Quy trình bắt buộc

1. Luôn bắt đầu bằng `using-superpowers`.
2. Dùng `executing-plans` làm quy trình thực thi chính và làm từng task theo đúng
   checkpoint trong plan. Không dispatch subagents nếu user không yêu cầu rõ
   trong session này.
3. Dùng `test-driven-development` cho validator/loader/test code và
   `verification-before-completion` trước mọi tuyên bố hoàn tất.
4. Dùng `systematic-debugging` nếu test hoặc real integration thất bại; không
   làm yếu contract để ép test qua.
5. Kết thúc bằng checklist của `requesting-code-review` và bàn giao cho Reviewer.
6. Không stage, commit hoặc push nếu user không yêu cầu riêng trong session.

## Đọc đầy đủ trước khi sửa

Theo thứ tự:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md
/home/minhhieu/hue_rag/reports/phase_7_golden_dataset_audit.md
/home/minhhieu/hue_rag/guides/phase_7_retrieval_answer_evaluation.md
/home/minhhieu/hue_rag/guides/phase_8_benchmark_model_selection.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
```

Sau đó kiểm tra exact code/data mà plan sẽ chạm:

```text
/home/minhhieu/hue_rag/backend/evaluation/test.py
/home/minhhieu/hue_rag/backend/evaluation/eval.py
/home/minhhieu/hue_rag/backend/core/schema.py
/home/minhhieu/hue_rag/backend/tests/test_evaluation.py
/home/minhhieu/hue_rag/backend/tests/conftest.py
/home/minhhieu/hue_rag/backend/ingestion/chunking/markdown_chunker.py
/home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation/tests.jsonl
/home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation/test2.jsonl
/home/minhhieu/hue_rag/knowledge-base-hue/foods/restaurants
/home/minhhieu/hue_rag/knowledge-base-hue/foods/cafes
/home/minhhieu/hue_rag/knowledge-base-hue/foods/local_specialties
/home/minhhieu/hue_rag/knowledge-base-hue/foods/food-guides.md
```

Old Phase 7 rows are candidates only. Direct curated Markdown evidence is the
closed-world source of truth.

## Trạng thái và scope đã khóa

- Phase 0–7 đã approved; Phase 8 vẫn `not_ready`.
- Giữ nguyên `tests.jsonl` và `test2.jsonl`.
- Tạo `golden_v2.jsonl` đúng 100 case và `golden_v2_smoke.jsonl` đúng 20 row
  copy nguyên vẹn từ full dataset.
- Main benchmark chỉ có câu trả lời được. Không tạo refusal dataset trong scope.
- Schema đúng sáu field: `case_id`, `question`, `keywords`,
  `reference_answer`, `category`, `evidence`.
- ID tuần tự `foods-0001` đến `foods-0100`.
- Dùng exact category quotas, source targets và authoring matrix trong spec.
- Câu hỏi phải rõ ràng, tự nhiên, không đánh đố và được evidence hỗ trợ trực
  tiếp. Không ép quota bằng câu gượng hoặc suy diễn.
- `keywords` có 2–4 cụm cụ thể và xuất hiện trong reference lẫn evidence; chúng
  không phải Phase 8 retrieval ground truth.
- Binary relevance duy nhất:

```text
document.metadata.source có trong case.evidence
AND document.metadata.section có trong case.evidence[source]
```

- Đúng source nhưng sai section là nonrelevant. Không dùng LLM judge, keyword
  proxy hoặc stored chunk IDs để gán retrieval relevance.
- Active Qdrant collection read-only. Real integration chỉ dùng isolated test
  collection có marker theo fixture hiện hành và phải cleanup/report kết quả.
- Không dùng fake, mock, replay hay fabricated output làm implementation hoặc
  completion evidence.
- Không thêm UUID, run ID, timestamp, manifest, registry, semantic validator,
  annotation UI hoặc audit framework.

## Cách thực hiện

1. Chạy `git status --short`, đọc diff exact files và bảo toàn mọi thay đổi ngoài
   scope. Không reset/checkout/xóa rộng.
2. Thực hiện từng Task 1–7 trong implementation plan, theo thứ tự và checkbox.
3. Sau contract validator, sau từng source block 40/20/20/20 và sau smoke subset,
   dừng ở reviewer checkpoint đã ghi trong plan; trình bày counts và findings.
4. Đọc toàn bộ file nguồn liên quan trước khi giữ một case. Không dùng search
   snippet thay cho complete declared H2 section.
5. Với mỗi row cũ được tái sử dụng, kiểm tra lại question, category, keywords,
   reference và toàn bộ evidence. Không copy annotation cũ như ground truth.
6. Nếu nguồn thiếu dữ kiện để tạo case tự nhiên hoặc có mâu thuẫn, dừng và báo:
   source/section, số case còn thiếu, category/source target bị ảnh hưởng và loại
   thông tin user cần bổ sung hoặc xác nhận. Không tự phân bổ lại quota.
7. Manual audit đủ 100 case vẫn bắt buộc; validator chỉ bảo vệ contract cấu trúc
   và lỗi evidence có thể kiểm tra deterministic.
8. Chạy real retrieval metadata verification đúng plan. Retrieval miss là
   baseline evidence, không được sửa gold để chiều theo model.
9. Viết
   `reports/phase_8_golden_dataset_v2_implementation_report.md` với exact real
   commands/outcomes, counts, reused/rewritten/new totals, conflicts và giới hạn.

## Giới hạn dừng

Không thực hiện các việc sau:

- không chạy embedding/retrieval/reranker comparison Phase 8;
- không gọi paid generator hoặc judge;
- không sửa model/profile/settings production;
- không mutate active collection;
- không bắt đầu brainstorming Gate 1;
- không tuyên bố Gate 0 approved thay Reviewer/user.

## Bàn giao cuối session

Trình bày ngắn gọn:

1. task/checkpoint nào đã hoàn thành;
2. exact files đã tạo/sửa;
3. số case theo category và source family;
4. validator/tests/real commands cùng PASS/FAIL thật;
5. conflicts, thiếu dữ liệu hoặc retrieval misses còn lại;
6. xác nhận Phase 7 files và active collection không bị mutate;
7. link implementation report và yêu cầu Reviewer kiểm tra Gate 0.

Nếu bị chặn tại checkpoint, bàn giao partial state trung thực và câu hỏi quyết
định duy nhất cần user trả lời; không tự mở rộng scope để tiếp tục.
