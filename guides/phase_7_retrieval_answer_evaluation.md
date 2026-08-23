# Phase 7 — Retrieval và Answer Evaluation

## Trạng thái

`ready` — thiết kế đơn giản mới đã được người dùng duyệt và sẵn sàng để
Implementer xây dựng.

Guide này là nguồn canonical cho scope, trạng thái và acceptance của Phase 7.

Đặc tả hỗ trợ:

```text
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
```

Kế hoạch triển khai hỗ trợ:

```text
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
```

## Mục tiêu

Đánh giá Hue Foods RAG bằng một luồng mà người đọc có thể hiểu ngay:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Phase 7 bắt đầu với `dense_only`. Sau khi baseline ổn định mới dùng cùng phép
đánh giá để so sánh:

- `dense_only`
- `hybrid_no_rerank`
- `hybrid_rerank`

## Nguyên tắc thiết kế

- Code đơn giản, rõ ràng và dễ đọc.
- Dùng backend hiện tại, không copy một RAG implementation khác vào project.
- Chỉ thêm file và hàm phục vụ trực tiếp evaluation.
- Không xây hạ tầng phòng xa.
- Có thể tối ưu kỹ thuật nâng cao sau khi chạy thật cho thấy nhu cầu.
- Nếu kỹ thuật nâng cao làm code phức tạp quá mức lợi ích thì phải loại bỏ.

Code reference trực tiếp cho Phase 7:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation
```

Hai reference này giúp định hướng Phase 7, không phải blueprint cho Phase 0–6.

## Cấu trúc

```text
backend/evaluation/
├── __init__.py
├── test.py
├── template.py
├── eval.py
└── evaluator.py

backend/tests/
└── test_evaluation.py

knowledge-base-hue/foods/evaluation/
├── test2.jsonl
└── tests.jsonl

notebooks/
└── 07_evaluation.ipynb
```

### `test.py`

Đọc câu hỏi từ đường dẫn được truyền vào. Mặc định dùng `test2.jsonl`.

### `template.py`

Chứa prompt của evaluation judge. Production generation prompt vẫn thuộc backend
chính và không được sao chép vào evaluation.

### `eval.py`

Chứa:

- MRR và nDCG keyword-based;
- retrieval evaluation;
- answer generation và judging;
- batch execution;
- summary;
- ghi hai CSV cố định.

### `evaluator.py`

Chứa giao diện Gradio với hai nút:

- `Đánh giá retrieval`
- `Đánh giá câu trả lời`

Hai nút dùng chung slider `Số câu chạy cùng lúc`, mặc định 3.

## Dữ liệu đánh giá

### Chạy thử

`test2.jsonl` chứa 20 câu thật được copy nguyên vẹn từ bộ 104 câu và phân bổ
tương đối đều trên 8 category.

### Chạy đầy đủ

Sau khi 20 câu ổn định, chỉ thay input path thành `tests.jsonl` để chạy 104 câu.
Không thêm workflow hoặc cấu trúc output mới cho lần chạy lớn hơn.

Loader chỉ cần:

- `question`
- `category`
- `reference_answer`
- `keywords`

## Retrieval evaluation

Với mỗi câu:

1. Gọi real `dense_only` retrieval service.
2. Giữ retrieved chunks theo thứ tự trả về.
3. Tìm từng keyword trong chunk text, không phân biệt hoa thường.
4. Tính MRR, nDCG và keyword coverage.
5. Hiển thị row và ghi CSV.

Không dùng gold source hoặc section để tính MRR/nDCG.

Output cố định:

```text
backend/evaluation/retrieval_results.csv
```

Các cột chính:

```text
category, question, keywords, mrr, ndcg,
keywords_found, total_keywords, keyword_coverage, error
```

## Answer evaluation

Với mỗi câu:

1. Gọi retrieval thật.
2. Build context bằng backend hiện tại.
3. Sinh câu trả lời thật với `gpt-5.4-nano`.
4. So sánh generated answer với reference answer bằng `gpt-5.4-mini`.
5. Trả ba điểm 1–5 và feedback.

Ba điểm:

- accuracy;
- completeness;
- relevance.

Không có groundedness.

Output cố định:

```text
backend/evaluation/answer_results.csv
```

Các cột chính:

```text
category, question, reference_answer, generated_answer,
accuracy, completeness, relevance, feedback, error
```

Nếu một câu lỗi, ghi lỗi vào row và tiếp tục. Không retry, resume hoặc tạo file
trung gian.

## Giao diện

Giao diện hiển thị:

- đường dẫn file câu hỏi;
- một slider concurrency;
- hai nút evaluation độc lập;
- progress;
- bảng kết quả;
- summary điểm trung bình;
- đường dẫn CSV đã ghi.

Nhấn nút được phép gọi paid API thật trực tiếp. Không có consent dialog hoặc
cost logic.

## Test

Chỉ giữ:

```text
backend/tests/test_evaluation.py
```

Giữ một nhóm test nhỏ và dễ hiểu cho các hành vi thật:

- đọc 20 và 104 câu từ đúng đường dẫn;
- kiểm tra fields cần dùng;
- kiểm tra MRR;
- kiểm tra nDCG;
- chạy retrieval thật;
- chạy một generation/judge thật;
- kiểm tra số outputs của UI handler.

Không tạo test files riêng cho cơ chế đã loại bỏ. Test pass không thay thế live
batch execution.

## Notebook 07

Notebook giải thích tuần tự:

1. Phase 7 đánh giá gì.
2. Đọc 20 câu thật.
3. Xem một câu hỏi.
4. Chạy retrieval thật.
5. Hiểu MRR/nDCG.
6. Sinh và chấm một câu thật.
7. Xem accuracy, completeness, relevance và feedback.
8. Chạy batch 20 câu.
9. Xem summary.
10. Mở giao diện.

Mỗi cell làm một việc, code ngắn và gọi backend.

Notebook style reference:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0
/home/minhhieu/llm_rag/tai_lieu/notebook_simple
```

Notebook không chứa artifact discovery, audit package hoặc test suite.

## Chạy thật, không fake

Implementer và Reviewer được phép dùng internet, Qdrant thật và paid OpenAI API
đã được người dùng cho phép.

Không dùng:

- fake ID, data, artifact, provider hoặc result;
- mock provider response;
- replay output;
- kết quả cũ hoặc bịa đặt làm evidence.

Active Hue Qdrant collection chỉ được đọc. Không in secrets.

## Những phần bị loại bỏ

Phase 7 mới không có:

- cost accounting hoặc cost estimation;
- consent/confirmation gate;
- calibration;
- resume;
- run ID hoặc generation run ID;
- timestamp quản lý evaluation package;
- checksum;
- package matching;
- tamper detection;
- partial artifact;
- artifact audit;
- validator chồng lớp;
- nhiều test files kỹ thuật.

Không được đổi tên hoặc chuyển nơi để giữ lại những cơ chế này.

## Acceptance

Phase 7 đạt khi:

1. package chỉ còn bốn module đã duyệt;
2. chỉ có một Phase 7 test file;
3. `test2.jsonl` có 20 câu thật thuộc đủ 8 category;
4. hai UI buttons chạy production path thật;
5. retrieval batch 20 câu hoàn thành;
6. answer batch 20 câu hoàn thành bằng nano và mini thật;
7. đổi input path và chạy 104 câu thật;
8. hai CSV có đúng số row và thứ tự câu hỏi;
9. Notebook 07 Run All thật đạt trên bản tạm;
10. repository notebook sạch outputs;
11. implementation report mới ghi đúng observed results và mọi lỗi;
12. Reviewer chạy lại độc lập và người dùng xác nhận.

## Gate trước Phase 8

Sau Phase 7, review Phase 0 đến Phase 6 theo dependency order bằng tài liệu
riêng do người dùng cung cấp. Kiểm tra code, tests, folders và notebooks; đơn
giản hóa hoặc xây dựng lại phần over-engineered. Chạy lại affected Phase 7
evaluation sau thay đổi liên quan. Chỉ mở Phase 8 khi toàn bộ gate này hoàn tất.
