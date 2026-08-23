# Project Status

## Mục tiêu

Hue RAG xây dựng chatbot về văn hóa, du lịch và ẩm thực Huế. Hue Foods RAG là
MVP hiện tại.

## Dữ liệu hiện có

- Curated foods: 57 restaurants, 24 cafes, 9 local specialties và
  `food-guides.md`.
- Chunking hiện tại tạo 572 chunks.
- Active Qdrant collection: `hue_foods_e5_small_384`, 572 points.
- Evaluation dataset đầy đủ: `knowledge-base-hue/foods/evaluation/tests.jsonl`,
  104 câu thuộc 8 category.
- Evaluation dataset chạy thử mới: `test2.jsonl`, dự kiến 20 câu thật phân bổ
  trên 8 category.

## Trạng thái các phase

- Phase 0–6: đã được duyệt theo các vòng trước.
- Phase 7: thiết kế đơn giản mới đã được người dùng duyệt; chờ Implementer xây
  dựng theo đặc tả và kế hoạch mới.
- Phase 8: chưa được bắt đầu.

Trước khi sang Phase 8 phải review lần lượt Phase 6 về Phase 0 để tìm và loại bỏ
over-engineering. Người dùng sẽ cung cấp tài liệu phù hợp riêng cho từng phase.
Code, test và notebook của phase cũ phải được đơn giản hóa nếu review phát hiện
chúng phức tạp quá mức cần thiết.

## Quyết định Phase 7 mới

Kiến trúc Phase 7 cũ gồm nhiều stage, calibration, artifact, cost, resume,
identity, checksum và package matching đã bị người dùng từ chối.

Thiết kế mới đã được duyệt tại:

```text
docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
```

Kế hoạch triển khai đã được duyệt tại:

```text
docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
```

Phase 7 mới chỉ có bốn module chính:

```text
backend/evaluation/test.py
backend/evaluation/template.py
backend/evaluation/eval.py
backend/evaluation/evaluator.py
```

Chỉ giữ một test file:

```text
backend/tests/test_evaluation.py
```

Luồng:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Phạm vi đầu tiên:

- chỉ `dense_only`;
- retrieval chấm MRR/nDCG bằng keyword;
- generation dùng `gpt-5.4-nano`;
- judge dùng `gpt-5.4-mini`;
- judge chỉ có accuracy, completeness, relevance và feedback;
- giao diện có hai nút đánh giá độc lập;
- concurrency mặc định 3;
- kết quả ghi đè `retrieval_results.csv` và `answer_results.csv`;
- chạy 20 câu thật trước, sau đó đổi đường dẫn để chạy 104 câu thật.

## Chính sách toàn hệ thống

- Code phải dễ hiểu, đơn giản, rõ ràng và không over-engineer.
- Cho phép research và tối ưu nâng cao khi có nhu cầu thật và kết quả thật chứng
  minh lợi ích.
- Không dùng fake ID, fake data, fake provider, fake artifact, mock provider
  response, replay hoặc kết quả bịa đặt.
- Implementer và Reviewer được phép chạy online và paid API thật đã được người
  dùng phê duyệt.
- Test không thay thế live integration evidence.
- Không xây cơ chế cost, consent, calibration, resume, identity, timestamp quản
  lý package, checksum, matching package hoặc tamper detection nếu không có nhu
  cầu trực tiếp.

## Tài liệu tham khảo

Code tham khảo trực tiếp cho Phase 7:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation
```

Notebook style:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0
/home/minhhieu/llm_rag/tai_lieu/notebook_simple
```

Hai code reference Phase 7 không áp dụng trực tiếp cho Phase 0–6.

## Báo cáo Phase 7

Hai báo cáo của kiến trúc cũ đã bị xóa để tránh gây nhầm lẫn:

```text
reports/phase_7_retrieval_answer_evaluation_implementation_report.md
reports/phase_7_retrieval_answer_evaluation_codex_review.md
```

Implementer phải tạo implementation report mới sau khi chạy thật. Reviewer chỉ
tạo Codex review report mới sau khi implementation mới được bàn giao.

## Bước tiếp theo

1. Implementer thực hiện đúng implementation plan mới.
2. Chạy test file nhỏ và hai batch thật trên 20 câu.
3. Khi ổn định, chạy hai batch thật trên 104 câu.
4. Viết implementation report mới.
5. Reviewer đọc source và chạy lại độc lập.
6. Người dùng xác nhận Phase 7.
7. Review Phase 6 về Phase 0 trước khi mở Phase 8.
