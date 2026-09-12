# Implementer — khảo sát toàn bộ evaluation `rag_old_0` và reset complexity

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Đây là nhiệm vụ khảo sát docs/source read-only do User trực tiếp yêu cầu. Mục
tiêu là đọc đầy đủ implementation evaluation nguyên bản của `rag_old_0`, giải
thích thật rõ hai nhánh Retrieval Evaluation và Answer Evaluation, xác định
chính xác mỗi metric consume field nào, rồi đề xuất schema Golden nhỏ nhất đủ
cho nhu cầu hiện tại. Không bảo vệ các đề xuất cũ chỉ vì chúng đã được viết;
phải chỉ ra phần nào đang over-engineered và có thể bỏ.

Khảo sát sâu schema trước đã `approved/completed`; task mới này không mở lại
findings R1–R5. Nó là một complexity reset theo yêu cầu mới nhất của User. Chỉ
Reviewer/User mới được sửa hoặc thay quyết định kiến trúc sau khi đọc report.

## 1. Bootstrap bắt buộc

Đọc đầy đủ theo thứ tự, tiếp tục phần thiếu nếu output bị cắt:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. prompt này

Đọc thêm đúng context thiết kế cần đối chiếu:

8. `guides/full_corpus_rag.md`
9. phần Golden/evidence/evaluation trong
   `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`
10. snapshot và mục 39–45, 51–53 trong
    `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`

Hai file trong `docs/superpowers/` là working notes, chưa phải written spec hay
implementation plan approved. Không sửa chúng.

## 2. Phạm vi reference phải khám phá đầy đủ

Root read-only:

`/home/minhhieu/llm_rag/tai_lieu/rag_old_0`

Trước hết dùng `rg --files` lập inventory toàn root, phân loại rõ file nằm trong
reading scope và phần data bị loại. Sau đó đọc **toàn văn mọi first-party text/
source ngoài knowledge-base data**, tối thiểu gồm:

- toàn bộ `evaluation/`, gồm code và đọc đủ mọi record của
  `evaluation/tests.jsonl`;
- toàn bộ `implementation/`;
- toàn bộ `pro_implementation/`;
- toàn bộ `app.py`, `evaluator.py`, `evaluator2.py`;
- toàn bộ năm notebook `day1.ipynb` đến `day5.ipynb`: đọc mọi Markdown cell,
  code cell và saved output, không execute;
- toàn bộ năm phiên âm/tổng hợp bài học trong `phien_am_bai_hoc/`;
- mọi README, config, dependency declaration, script hoặc first-party text khác
  ngoài vùng data nếu có.

### Phần data không cần đọc

Không đọc nội dung các file dữ liệu tiếng Anh dưới `knowledge-base/`, đặc biệt
`knowledge-base/**/*.md`. Chỉ inventory số lượng/path để chứng minh đã loại đúng
scope; không mở nội dung, không fact-check câu hỏi với knowledge base. Đây là
chủ ý của User vì task tập trung evaluator và schema, không audit dữ liệu tiếng
Anh.

`evaluation/tests.jsonl` **không thuộc phần loại**: đây là input trực tiếp của
evaluator nên phải đọc đầy đủ để xác định schema, biến thể và field usage.

Bỏ qua `.env`, credentials/secrets, virtual environment, dependencies/vendor,
cache, database/vector store, binary và generated build artifacts. Ghi rõ exact
paths hoặc nhóm bị bỏ cùng lý do. Không suy nội dung từ filename hoặc vài kết
quả search; file dài/output bị cắt phải đọc tiếp đến hết.

Không cần đọc `/home/minhhieu/llm_rag/tai_lieu/rag_old` hoặc các project reference
khác. Không mở rộng task sang corpus Huế hay runtime Huế.

## 3. Câu hỏi phải trả lời bằng data flow thật

### 3.1 Hai nhánh evaluation

Truy nguyên riêng và thật đơn giản:

```text
tests.jsonl -> Retrieval Evaluation
tests.jsonl -> Answer Evaluation
```

Với mỗi nhánh, nêu loader, function/call site, input, output, aggregation và nơi
hiển thị. Phân biệt Basic và PRO nếu code đang dùng khác nhau. Không dựng kiến
trúc mới.

### 3.2 Retrieval Evaluation

Xác minh chính xác:

- các metric thực tế là gì; làm rõ “Retrieval Evaluation” là tên nhánh hay tên
  một metric;
- công thức và data flow của Mean Reciprocal Rank (MRR), normalized DCG (nDCG)
  và keyword coverage/metric thứ ba nếu code có;
- cutoff `k` áp dụng ở đâu, metric nào không thật sự cắt theo `k`;
- relevance được xác định từ `keywords` như thế nào;
- MRR/nDCG được tính per keyword, per document hay per test case rồi aggregate
  ra sao;
- IDCG biết gì và không biết gì về relevant documents ngoài retrieved list;
- với đúng implementation `rag_old_0`, có cần `evidence`, `expected_claims`,
  source path, heading hoặc chunk ID trong Golden để tái tạo các metric hiện tại
  hay không;
- nếu không cần, nói thẳng `không cần` và giải thích giới hạn của keyword-based
  relevance. Không tự biến giới hạn đó thành requirement cho schema phức tạp.

Phải phân biệt rõ:

1. metric mà `rag_old_0` thực sự tính từ keywords;
2. metric chuẩn yêu cầu một tập relevant items đầy đủ;
3. claim nào hệ thống hiện tại có thể và không thể đưa ra khi không có explicit
   evidence/relevance labels.

### 3.3 Answer Evaluation

Xác minh chính xác:

- generator nhận gì và sinh gì;
- LLM Judge nhận đúng những field/input nào;
- cách chấm Accuracy, Completeness và Relevance;
- thang điểm, aggregation và category breakdown;
- `keywords`, `category`, retrieved context, source/citation hoặc evidence có
  được đưa vào Judge hay không;
- với implementation hiện tại, `question` + generated answer +
  `reference_answer` có đủ để tạo ba điểm hay không;
- seed, temperature, repetitions và giới hạn tính tái lập nếu code có.

Nếu answer thiếu ý và vì vậy Completeness thấp, chỉ mô tả đúng behavior quan
sát được; không tự đề xuất routing, `case_type`, claim judge hoặc nhiều rubric
nếu không có consumer thật.

### 3.4 Golden schema tối thiểu

Lập bảng ngắn cho các field `question`, `keywords`, `reference_answer`,
`category`, `case_id`, `evidence`, `expected_claims`. Với mỗi field chỉ ghi:

- consumer thực tế trong `rag_old_0`;
- cần hay không cần cho đúng mục tiêu metric hiện tại của User;
- điều gì mất đi nếu bỏ;
- kết luận `required`, `optional` hoặc `omit`.

Đưa 2–3 phương án thực sự đơn giản, bắt buộc có phương án baseline giống
`tests.jsonl` gồm `question`, `keywords`, `reference_answer` và optional
`category`. Nếu đề xuất thêm field, phải chỉ ra consumer/metric thật; không dùng
lý do “có thể hữu ích sau này”.

Đối chiếu thẳng với các working decisions hiện hành:

- `expected_claims`/claim-level exact spans phục vụ metric nào đã được User nêu;
- phần nào chỉ phục vụ groundedness/citation/partial-answer analysis ngoài sáu
  metric User vừa xác định;
- `evidence_groups`, OR/AND alternatives, `case_type`, `partition`, `domain`,
  `claim_id` có consumer thật hay đang là complexity không cần thiết;
- cách reset nhỏ nhất nếu Reviewer/User quyết định quay về schema đơn giản.

Không tự thay đổi quyết định Evidence C hoặc schema hiện hành. Chỉ cung cấp
evidence và khuyến nghị để Reviewer/User quyết định sau.

### 3.5 Notebooks và phiên âm

Tổng hợp đầy đủ nhưng không kể lại dài dòng:

- năm ngày xây pipeline theo trình tự nào;
- Golden được bài học hướng dẫn tạo/cập nhật ra sao;
- notebooks chạy Basic hay PRO tại từng chỗ quan trọng;
- saved outputs chứng minh điều gì và không chứng minh điều gì;
- evaluator/dashboard dùng category và thresholds ra sao;
- bài học nào liên quan trực tiếp tới lựa chọn schema/metrics tối giản.

Dùng record thật sau làm ví dụ xuyên report, nhưng vẫn phải đọc toàn bộ
`tests.jsonl` và không suy toàn dataset từ một dòng:

```json
{"question":"Who won the prestigious IIOTY award in 2023?","keywords":["Maxine","Thompson","IIOTY"],"reference_answer":"Maxine Thompson won the prestigious Insurellm Innovator of the Year (IIOTY) award in 2023.","category":"direct_fact"}
```

## 4. Output duy nhất

Tạo đúng một report:

`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`

Report gồm:

1. kết luận ngắn cho User;
2. coverage map: toàn bộ file ngoài data đã đọc, data/artifacts đã bỏ;
3. sơ đồ/data flow hai nhánh Retrieval và Answer;
4. bảng metric -> công thức -> input fields -> aggregation -> giới hạn;
5. bảng field necessity theo consumer thật;
6. đối chiếu Basic/PRO, notebooks và phiên âm;
7. 2–3 schema candidates tối giản và khuyến nghị;
8. danh sách complexity hiện hành nên giữ, bỏ hoặc hoãn kèm lý do;
9. evidence gaps, skipped/not verified và handoff cho Reviewer.

Mọi claim về code/metric phải có exact path + line hoặc notebook cell/heading.
Không chép dài source, transcript hoặc dataset. Dùng ngôn ngữ trung tính, dễ
hiểu; không thêm framework, manifest, state machine, validator nhiều tầng,
alternative evidence logic hoặc future-proofing không có consumer.

## 5. Quyền và giới hạn

- Chỉ đọc và tạo report Markdown nói trên; được cập nhật
  `session_prompt/CURRENT_HANDOFF.md` khi trả task về Reviewer.
- Không sửa guide, decision notes, context, Project Status, review, user report,
  runtime, tests, notebooks, corpus, Golden, index, settings hoặc reference.
- Không chạy/import Python, code, script, notebook, model, tokenizer, API,
  Qdrant, tests hoặc benchmark.
- Không đọc `.env`, không mạng/download/dependency.
- Chỉ dùng lệnh đọc text và Git read-only; không commit, push, checkout, reset
  hoặc Git write.
- Không spawn subagent.
- Giữ nguyên mọi thay đổi dirty/untracked có trước và không nhận chúng là sản
  phẩm của task.

## 6. Review Contract

Risk: low, docs-only research.

Reviewer sẽ kiểm độc lập:

1. inventory bao phủ toàn root và full-reading bao phủ mọi first-party
   non-data file; `knowledge-base/**/*.md` được loại rõ chứ không bị claim đã
   đọc;
2. `evaluation/tests.jsonl`, ba vùng code, ba evaluator/app, năm notebook và năm
   transcript đều được đọc hết;
3. Retrieval/Answer data flow, formulas, cutoff và actual field consumers đúng
   source;
4. report trả lời trực tiếp evidence/expected_claims có thật sự cần cho các
   metric User nêu hay không, không đánh tráo metric chuẩn với implementation
   keyword-based;
5. schema candidates nhỏ, mỗi field có consumer thật và không over-engineer;
6. observed behavior, lesson guidance và recommendation được phân biệt;
7. toàn bộ giới hạn được tuân thủ, không tự approval hay sửa quyết định canonical.

Không có yêu cầu chạy tests. Dùng `git diff --check` cho tracked Markdown và
kiểm trailing whitespace của report untracked bằng lệnh text read-only.

Khi hoàn tất, cập nhật CURRENT_HANDOFF thành:

- `Target role: reviewer`
- `Authored by: implementer`
- `Handoff kind: final_review`
- `State: active`

Bàn giao phải dẫn report, coverage, commands/read method, skipped/not verified,
schema recommendation và exact phần Reviewer cần kiểm lại. Không tạo Codex
review/user report, không claim PASS/approval/closure và không tự sửa các quyết
định trước đó.
