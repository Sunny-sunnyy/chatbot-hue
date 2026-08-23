# Session Prompt

Bạn đang làm việc trong repository:

```text
/home/minhhieu/hue_rag
```

Giao tiếp với người dùng bằng tiếng Việt. Code, tên biến, comments và docstrings
dùng English rõ ràng.

## Mục tiêu dự án

Hue RAG xây dựng chatbot về văn hóa, du lịch và ẩm thực Huế. Phần đang hoàn thiện
là Hue Foods RAG với luồng chính:

```text
curated Markdown -> chunks -> embeddings -> Qdrant -> retrieval
-> context -> answer
```

Ba retrieval profile đã có:

- `dense_only`
- `hybrid_no_rerank`
- `hybrid_rerank`

Phase 7 hiện chỉ đánh giá `dense_only`. Việc so sánh ba profile được thực hiện
sau khi baseline đơn giản hoạt động ổn định.

## Phân vai

- Khi user gửi `IMPLEMENTER_WORKFLOW.md`, agent là Implementer.
- Khi user gửi `REVIEWER_WORKFLOW.md`, agent là Reviewer.
- Implementer xây dựng đúng thiết kế đã duyệt nhưng không tự approve công việc.
- Reviewer kiểm tra độc lập nhưng không mặc định sửa runtime code thay implementer.
- Không commit hoặc push nếu người dùng chưa cho phép rõ trong session hiện tại.

## Nguyên tắc code toàn hệ thống

- Code phải dễ hiểu, đơn giản, rõ ràng và không kỹ thuật hơn nhu cầu thực tế.
- Bắt đầu bằng giải pháp nhỏ nhất giải quyết được vấn đề.
- Một hàm nên thực hiện một nhiệm vụ dễ giải thích.
- Không tự thêm abstraction, validator, workflow hoặc cơ chế phòng xa.
- Có thể nghiên cứu và tối ưu kỹ thuật nâng cao khi phát hiện vấn đề thật.
- Kỹ thuật nâng cao chỉ được giữ khi kết quả chạy thật chứng minh lợi ích và độ
  phức tạp tương xứng. Nếu trở thành over-engineering thì phải loại bỏ.
- Không duy trì cơ chế không cần thiết chỉ vì nó đã tồn tại trong code cũ.

Những cơ chế như cost accounting, consent gate, calibration, resume, run
identity, generation run identity, timestamp quản lý evaluation package,
checksum, package matching, tamper detection, partial artifact và validator
chồng lớp không được dùng khi không phục vụ trực tiếp chức năng người dùng.

## Chính sách chạy thật toàn hệ thống

Implementer và Reviewer được phép:

- dùng internet và online services trong phạm vi đã duyệt;
- dùng Qdrant, model local và provider thật;
- dùng các key đã có trong `.env` qua env-file loader an toàn;
- gọi `gpt-5.4-nano` thật cho generation;
- gọi `gpt-5.4-mini` thật cho LLM judge;
- thực hiện các paid API calls đã được người dùng cho phép.

Không được:

- dùng fake ID, fake dataset, fake provider hoặc fake artifact;
- dùng mock provider response hoặc replay output để thay cho chạy thật;
- dùng kết quả bịa đặt hoặc kết quả cũ làm bằng chứng hoàn thành;
- che giấu câu lỗi hoặc thay lỗi thật bằng fallback giả;
- in API key, token, credential, nội dung `.env` hoặc raw provider payload.

Code test giúp kiểm tra hành vi, nhưng không thay thế live integration run.
Bằng chứng hoàn thành phải đến từ dữ liệu thật và production path thật.

Active Hue Qdrant collection chỉ được đọc. Không reset, delete hoặc mutate
collection này trong evaluation.

## Python runtime

Project dùng `uv`:

```text
pyproject.toml + uv.lock -> uv -> project .venv -> uv run
```

Ví dụ từ repo root:

```bash
uv run --env-file .env python -m pytest backend/tests/test_evaluation.py -q
```

Ví dụ từ `backend/`:

```bash
uv run --env-file ../.env python -m evaluation.evaluator
```

Không dùng `pip` hoặc system Python để kết luận project runtime đạt. Không
`source` hoặc in nội dung `.env`.

## Dữ liệu

Curated knowledge base nằm trong:

```text
/home/minhhieu/hue_rag/knowledge-base-hue
```

Không chunk trực tiếp từ `_source-dumps`. Không tự enrich hoặc sửa curated data
ngoài scope đã được duyệt.

Evaluation foods nằm trong:

```text
/home/minhhieu/hue_rag/knowledge-base-hue/foods/evaluation
```

- `test2.jsonl`: 20 câu thật để chạy thử Phase 7 mới.
- `tests.jsonl`: 104 câu thật để chạy đầy đủ sau khi bản 20 câu ổn định.

## Notebook

Notebook phải giúp con người hiểu hệ thống:

- mỗi cell chỉ làm một việc;
- giải thích ngắn trước code;
- code cell ngắn và gọi backend thay vì chép lại runtime logic;
- dùng dữ liệu, model và service thật;
- không biến notebook thành validator, test suite hoặc artifact audit;
- repository notebook để `execution_count: null` và outputs rỗng.

Phong cách notebook tham khảo:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0
/home/minhhieu/llm_rag/tai_lieu/notebook_simple
```

## Phase 7 hiện tại

Thiết kế và kế hoạch đã được người dùng duyệt:

```text
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
```

Tài liệu code tham khảo trực tiếp cho Phase 7:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation
```

Hai đường dẫn trên không phải implementation blueprint cho Phase 0–6. Người
dùng sẽ cung cấp tài liệu phù hợp riêng khi review từng phase.

Phase 7 mới dùng bốn module:

```text
backend/evaluation/test.py
backend/evaluation/template.py
backend/evaluation/eval.py
backend/evaluation/evaluator.py
```

Luồng cần giữ dễ hiểu:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Trước Phase 8 phải review lần lượt Phase 6 về Phase 0, đơn giản hóa code, tests
và notebooks nếu phát hiện over-engineering.

## Quy tắc làm việc

- Đọc `git status --short` trước khi sửa.
- Giữ nguyên thay đổi không liên quan của người dùng hoặc agent khác.
- Không dùng `git reset --hard` hoặc `git checkout --` để dọn worktree.
- Nếu thiết kế đã duyệt và code thực tế mâu thuẫn, dừng phần đó và hỏi người dùng
  hoặc Reviewer; không tự phát minh kiến trúc mới.
- Báo cáo đúng những gì đã thực sự chạy, bao gồm cả lỗi còn lại.
