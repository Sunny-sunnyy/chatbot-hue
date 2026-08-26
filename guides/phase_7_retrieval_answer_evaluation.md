# Phase 7 — Retrieval và Answer Evaluation

## Trạng thái

`approved` — baseline correction vòng 1 đã đạt technical review và được người
dùng xác nhận sau khi kiểm tra Notebook 07 ngày 2026-08-24 +07.

`post-simplicity correction approved` — correction hẹp đã được Implementer
hoàn tất, đạt independent technical review và được người dùng xác nhận sau khi
chạy Notebook 07 ngày 2026-08-26 +07. Ghi chú này không mở scope sửa dataset.

Guide này là nguồn canonical cho scope, trạng thái và acceptance của Phase 7.

Đặc tả hỗ trợ:

```text
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-26-phase-7-post-simplicity-correction-design.md
```

Kế hoạch triển khai hỗ trợ:

```text
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-7-post-simplicity-correction.md
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

`test2.jsonl` chứa 20 câu thật được copy nguyên vẹn từ bộ 104 câu và phủ đủ 8
category hiện hành. Đây là smoke set để kiểm tra pipeline nhanh và tiết kiệm
chi phí, không phải bằng chứng chất lượng cuối cùng.

Audit ngày 2026-08-26 xác nhận smoke set hiện chưa có câu thuộc nhóm cafe và
golden dataset còn các vấn đề annotation/keyword cần thảo luận riêng:

```text
/home/minhhieu/hue_rag/reports/phase_7_golden_dataset_audit.md
```

Không sửa `test2.jsonl`, `tests.jsonl` hoặc tạo golden dataset mới trong
post-simplicity correction cho tới khi user duyệt design dữ liệu ở session
brainstorming riêng.

### Chạy đầy đủ

Sau khi implementation, dataset và smoke run đã sẵn sàng, chỉ thay input path
thành `tests.jsonl` để chạy 104 câu. Không thêm workflow hoặc cấu trúc output
mới cho lần chạy lớn hơn. Full run là evidence đánh giá đầy đủ; không suy rộng
kết luận chất lượng từ smoke set 20 câu.

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
4. Tính reciprocal rank và nDCG riêng cho từng keyword, sau đó lấy trung bình
   trên các keywords; keyword coverage là phần trăm keywords được tìm thấy.
5. Hiển thị row và ghi CSV.

Implementation giữ các biến trung gian như `avg_mrr`, `avg_ndcg`,
`keywords_found`, `total_keywords` và `keyword_coverage` để công thức dễ đọc;
không đổi semantics của `rag_old_0`.

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
2. Build labeled context string bằng `ContextBuilder.build(documents)`.
3. Sinh câu trả lời thật với `gpt-5.4-nano`.
4. So sánh generated answer với reference answer bằng `gpt-5.4-mini`.
5. Trả ba điểm 1–5 và feedback.

Ba điểm:

- accuracy: sai thực chất phải là 1; mức chấp nhận được là 3; chỉ hoàn toàn
  chính xác mới là 5;
- completeness: chỉ là 5 khi đủ toàn bộ thông tin quan trọng trong reference;
- relevance: chỉ là 5 khi trả lời trực tiếp và không thêm thông tin ngoài câu
  hỏi.

Relevance evaluation áp dụng answer-style contract của Phase 6: không thưởng
cho greeting, praise, emoji hoặc closing invitation máy móc. Nội dung lặp không
giúp trả lời câu hỏi có thể làm giảm relevance; list chỉ cần khi nhiều items hoặc
steps thực sự rõ hơn paragraph ngắn.

Output schema dùng integer 1–5 với validation bounds và mô tả ngắn cho ba điểm
cùng feedback. Judge không nhận retrieved context nên prompt/schema không được
tuyên bố rằng nó chấm groundedness. Giữ `temperature=0` để chấm ổn định và
`max_tokens=600` để feedback ngắn có giới hạn rõ ràng.

Generator và judge vẫn dùng OpenAI Agents SDK, nhưng SDK tracing tắt mặc định
theo Phase 6 simplicity decision ngày 2026-08-25. Phase 7 không phụ thuộc Trace
Dashboard và không bật tracing riêng cho evaluation. CSV kết quả cùng safe local
logs là observability đủ cho scope hiện tại.

Evaluator nhận trực tiếp context string; không đọc `.context`, `.sources` hoặc
reconstruct source IDs. Empty string dùng cùng no-context policy với production
route.

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
- bảng kết quả có đúng named columns tương ứng với retrieval hoặc answer;
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
Không bật Agents SDK tracing; không ghi full prompt, retrieved context hoặc raw
provider response vào logs/artifacts.

Coordinated Phase 4–5 blue-green verification được user duyệt ngày 2026-08-25
+07 cho phép retrieval-only evaluator nhận optional exact `collection_name` tại
composition root. Hàm copy settings trong memory, chọn profile/collection rồi
build real retrieval service. Override chỉ dùng để chạy fresh 104 questions × 3
profiles trên active baseline và `hue_foods_e5_small_384_dense`; nó không sửa
`settings.yaml`, không áp dụng cho answer evaluation/API và không tạo
multi-collection framework.

## Post-simplicity correction đã được duyệt

Reviewer đã xác nhận Phase 7 hiện dùng đúng contract đơn giản của Phase 6:

- `ContextBuilder.build(documents)` trả labeled context string;
- generator nhận question và context string rồi trả answer string;
- judge chỉ nhận question, reference answer và generated answer;
- tracing vẫn disabled.

Không cần redesign hoặc viết lại Phase 7 lần ba. Correction code chỉ gồm:

1. bỏ tham số `collection_name` khỏi `run_answer_batch()` và
   `run_answer_ui()` cùng các call/test chỉ phục vụ hai public answer paths này;
2. giữ optional collection override cho retrieval-only comparison và các
   guarded retrieval verification cần thiết;
3. không thêm abstraction, compatibility wrapper hoặc validation layer để thực
   hiện việc tách này.

Correction artifact gồm:

1. xóa execution counts và outputs khỏi canonical Notebook 07; bản Run All để
   kiểm chứng phải ghi ra `/tmp`;
2. giữ hai CSV cố định và ghi đúng dataset của lần chạy gần nhất; hiện tại mỗi
   CSV có 20 rows, còn full-run 104 rows trước đây là historical evidence trong
   implementation/review reports;
3. chưa chạy lại paid 104-answer batch cho tới khi scope dữ liệu ở audit được
   user chốt và Implementer/Reviewer sẵn sàng.

User đã duyệt exact correction design ngày 2026-08-26 +07. Implementer chỉ được
triển khai sau khi nhận prompt trỏ tới guide và implementation plan; không được
mở rộng sang dataset, metric, provider/model hoặc architecture khác.

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
13. Agents SDK tracing giữ disabled cho cả generator và judge.

Các mục trên ghi acceptance của baseline đã được duyệt. Post-simplicity
correction chỉ được đóng khi:

1. public answer batch/UI không còn collection override;
2. retrieval-only override vẫn chạy đúng exact approved comparison path;
3. Phase 6 context-string/generator-string contract vẫn được giữ;
4. canonical Notebook 07 không có execution count hoặc output;
5. tài liệu ghi đúng row count và nguồn gốc của artifact hiện hành;
6. dataset và full-run acceptance tuân theo design được duyệt ở session dữ liệu
   riêng;
7. Implementer báo cáo observed results, Reviewer kiểm tra độc lập và user xác
   nhận correction.

## Gate trước Phase 8

Sau Phase 7, review Phase 0 đến Phase 6 theo dependency order bằng tài liệu
riêng do người dùng cung cấp. Kiểm tra code, tests, folders và notebooks; đơn
giản hóa hoặc xây dựng lại phần over-engineered. Chạy lại affected Phase 7
evaluation sau thay đổi liên quan. Chỉ mở Phase 8 khi toàn bộ gate này hoàn tất.
