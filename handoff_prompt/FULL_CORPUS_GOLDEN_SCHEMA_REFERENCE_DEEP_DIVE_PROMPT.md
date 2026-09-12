# Implementer — khảo sát sâu cách tạo Golden, schema và evaluation

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Đây là một nhiệm vụ đọc và lập báo cáo mới theo yêu cầu trực tiếp của User để
hỗ trợ quyết định schema tối thiểu cho Golden toàn corpus. Khảo sát reference
Golden/evaluation trước đã `approved/completed`; không mở lại R1–R4 và không sửa
báo cáo cũ. Nhiệm vụ mới phải đi sâu vào cách Golden được hình thành, từng field
được code sử dụng ra sao, nội dung phiên âm dạy gì và evaluation vận hành thế
nào. Không tự chốt S1/S2/S3.

## 1. Bootstrap và skills bắt buộc đọc đầy đủ

Đọc toàn bộ theo đúng thứ tự; nếu output bị cắt, đọc tiếp phần còn thiếu:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. prompt này

Sau bootstrap, đọc toàn bộ các tài liệu canonical trực tiếp liên quan:

8. `handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`
9. `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`
10. `reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`
11. `reports/user_reports/full_corpus_golden_evaluation_reference_user_report_2026_09_10.md`
12. `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`: đọc
    snapshot đầu file và toàn bộ mục 35–45; các mục cũ hơn chỉ mở khi một pointer
    trong phạm vi này yêu cầu.
13. `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`: đọc
    toàn bộ phần Golden/evidence/evaluation và tổ chức P7.
14. `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`:
    đọc toàn bộ phần Golden/evaluation.

Đọc đầy đủ baseline Foods V3 và bằng chứng hình thành nó:

15. `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md`
16. `docs/superpowers/plans/2026-08-27-phase-8-golden-dataset-v3-implementation-plan.md`
17. `reports/phase_8_golden_dataset_v3_implementation_report.md`
18. `reports/phase_8_golden_dataset_v3_codex_review.md`
19. `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`
20. `knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl`
21. Các phần Golden/evaluation liên quan trong
    `guides/phase_7_retrieval_answer_evaluation.md` và
    `guides/phase_8_benchmark_model_selection.md`.
22. Các source hiện hành thực sự load/validate/consume Golden, tối thiểu:
    `backend/evaluation/test.py`, `backend/evaluation/golden_dataset.py`,
    `backend/evaluation/eval.py`, `backend/evaluation/evaluator.py`,
    `backend/evaluation/template.py` và `backend/tests/test_evaluation.py`.

Tài liệu đã approved là context và evidence index, không phải expected answer
để ép kết luận mới khớp theo.

## 2. Reference do User chỉ định — khám phá toàn bộ read-only

Root bắt buộc:

`/home/minhhieu/llm_rag/tai_lieu/rag_old_0`

Các vùng User đặc biệt yêu cầu:

- project code, notebooks và dữ liệu Markdown tiếng Anh dưới root trên;
- phiên âm/tổng hợp bài học tại
  `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc`;
- code đánh giá tại
  `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation`;
- Golden reference tại
  `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/tests.jsonl`.

Dùng `rg --files` lập inventory toàn root. Đọc toàn bộ first-party file có thể
đọc bằng text, gồm `.py`, `.ipynb`, `.md`, `.txt`, `.jsonl`, `.html`, config và
script liên quan. Với notebook, đọc toàn bộ cells, markdown và saved outputs mà
không execute. Với dữ liệu Markdown tiếng Anh, đọc toàn bộ để hiểu Golden dựa
trên loại knowledge nào; không cần audit lại độ đúng của từng câu hỏi với toàn
corpus nếu không có mapping rõ ràng.

Bỏ qua `.env`, credential/secrets, virtual environment, dependency/vendor,
cache, database/vector store, binary và generated build artifacts. Ghi chính
xác phần bỏ qua và lý do. Thư mục `phien_am_bai_hoc` nằm trong root nên không
đếm hai lần trong coverage. Nếu file/output dài bị cắt, tiếp tục đọc phần thiếu;
không suy nội dung từ filename hoặc vài kết quả `rg`.

Không cần đọc lại `/home/minhhieu/llm_rag/tai_lieu/rag_old` trong nhiệm vụ này;
đó là implementation khác đã được khảo sát trước. Trọng tâm mới là truy nguyên
đầy đủ một pipeline `rag_old_0` và sự phát triển từ nó sang Foods V3.

## 3. Câu hỏi báo cáo bắt buộc trả lời

### 3.1 Khái niệm cho User

Giải thích bằng tiếng Việt đơn giản:

- JSONL là gì;
- một `record` là gì, dùng một dòng thật đã rút gọn để minh họa;
- `schema` là gì: field bắt buộc/tùy chọn, kiểu dữ liệu, enum, quan hệ và
  validation;
- vì sao schema phải dựa trên evaluator và quy trình audit thay vì thêm field
  “có thể hữu ích” theo cảm tính.

### 3.2 Golden `tests.jsonl` được tạo như thế nào

Truy nguyên evidence trong code, notebook, Markdown và phiên âm:

- câu hỏi, keywords, reference answer và category được tạo thủ công, từ log,
  bằng LLM hay bằng quy trình nào;
- file hoặc công cụ nào thực sự tạo/ghi `tests.jsonl`; nếu không tìm thấy, chỉ
  kết luận “không tìm thấy trong phạm vi đã đọc” và liệt kê phạm vi;
- ai hoặc bước nào kiểm duyệt question–answer–evidence;
- category được chọn trước hay gán sau;
- bài học nói gì về cập nhật Golden qua phản hồi người dùng;
- phân biệt rõ lời giảng/tài liệu tổng hợp, behavior code, saved notebook output
  và suy luận của Implementer.

### 3.3 Schema thực tế và field usage

Đọc toàn bộ 150 records của `tests.jsonl` để xác định field set, kiểu và biến thể
thực tế. Không cần fact-check cả 150 câu với corpus. Lập bảng cho từng field:

- nơi được load/validate;
- nơi được dùng trong retrieval evaluation;
- nơi được đưa vào generator hoặc answer judge;
- nơi chỉ dùng để breakdown/display;
- nơi không được dùng;
- có thể derive từ file/path/manifest hay bắt buộc lưu ở từng record.

Không dừng ở Pydantic model; lần theo data flow thật qua import đang active và
các call sites. Nếu notebook/code khác nhau, ghi riêng từng phiên bản.

### 3.4 Evaluation vận hành thế nào

Theo luồng thật:

`tests.jsonl → loader → retrieval → relevance → retrieval metrics → generation
→ answer judge → aggregation/dashboard`.

Với từng bước, ghi exact inputs/outputs và source pointer. Làm rõ:

- keywords được dùng ra sao và vì sao không phải exact evidence;
- cutoff của MRR, coverage và nDCG;
- IDCG biết và không biết relevance nào;
- current import Basic hay PRO;
- judge prompt nhận question/reference/generated answer/context/citation nào;
- category ảnh hưởng điểm hay chỉ dùng nhóm kết quả;
- saved notebook outputs minh họa điều gì và không chứng minh điều gì;
- seed/temperature, split, leakage, repetitions và thresholds nếu có.

### 3.5 Từ `rag_old_0` đến Foods V3

Đối chiếu có bằng chứng:

1. schema bốn field của `tests.jsonl`;
2. schema sáu field thật của Foods V3;
3. fields nào Foods V3 giữ, thêm, đổi nghĩa hoặc loại;
4. code hiện hành của Huế thực sự consume từng field nào;
5. phần nào trong Foods V3 được thiết kế từ ý tưởng reference, phần nào là cải
   tiến riêng của Huế; không khẳng định quan hệ nhân quả nếu tài liệu không ghi.

Phân biệt “file trông giống nhau” với “field cần thiết cho evaluator mới”. Không
dùng schema lịch sử làm requirement tự động cho full corpus.

### 3.6 Cơ sở chọn schema tối thiểu cho full corpus

Lập **field-necessity matrix**, mỗi candidate field phải được xếp một trong:

- `must_store_per_record`;
- `derive_or_store_in_manifest`;
- `authoring_only`;
- `omit`;
- `unresolved`.

Ít nhất xét các field đang được thảo luận: `case_id`, `question`, `keywords`,
`reference_answer`, `category`, legacy `evidence`, `partition`, `domain`,
`case_type`, `expected_claims`, `claim_id`, `evidence_groups`, và locator C
`source/heading_path/start/end/text`.

Với mỗi kết luận, nêu consumer hoặc nhu cầu audit/evaluation cụ thể. Chỉ đề xuất
field khi có nhu cầu thật. Nêu rõ field nào có thể suy ra deterministic để tránh
lưu lặp và field nào nếu bỏ sẽ khiến không đo được retrieval, completeness,
partial answer, conflict hoặc citation support.

Đưa 2–4 schema candidates tối giản để Reviewer thảo luận với User. Mỗi candidate
cần có một JSON minh họa nhỏ dựa trên cấu trúc record thật, nhưng phải gắn nhãn
`illustrative only`, không gọi đó là Golden đã tạo. So sánh độ đơn giản, khả năng
human review, validation và metric support. Implementer được khuyến nghị có lý
do nhưng không được tự chọn thay Reviewer/User.

## 4. Output duy nhất

Tạo một report:

`reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`

Report phải có:

1. tóm tắt cho User;
2. coverage map toàn `rag_old_0`, gồm file đã đọc đầy đủ, file bỏ qua và lý do;
3. giải thích JSONL/record/schema;
4. provenance và quy trình tạo `tests.jsonl`;
5. data-flow evaluation cùng bảng field consumers;
6. đối chiếu `tests.jsonl` → Foods V3 → nhu cầu full corpus;
7. field-necessity matrix;
8. 2–4 schema candidates tối giản và ví dụ minh họa;
9. evidence gaps và các quyết định thực sự còn cần User;
10. self-review, phần skipped/not verified và prompt trả Reviewer.

Mọi claim ảnh hưởng schema phải có exact path + line, notebook cell hoặc heading
và đoạn định vị. Không chép dài code, phiên âm hoặc dataset. Khi không tìm thấy
provenance/tool, nêu phạm vi đã kiểm thay vì kết luận tuyệt đối.

## 5. Quyền và giới hạn

- Chỉ đọc và tạo report Markdown nói trên; được cập nhật
  `session_prompt/CURRENT_HANDOFF.md` khi bàn giao về Reviewer.
- Không sửa report khảo sát đã approved, review, user report, canonical spec,
  plan, guide, runtime, tests, corpus, Golden, index, settings hoặc reference.
- Không chạy/import code, notebook, model, tokenizer, API, Qdrant, benchmark hay
  test suite; không đọc `.env`; không dùng mạng/download/dependency.
- Chỉ dùng lệnh đọc text/JSON/notebook và Git read-only. Không commit, push,
  reset, checkout hoặc Git write. Không spawn subagent.
- Giữ nguyên worktree có thay đổi sẵn. Không nhận các file dirty/untracked có
  trước là sản phẩm của task này.

## 6. Review Contract và bàn giao

Risk: low, docs-only research.

Reviewer sẽ kiểm độc lập:

1. coverage map có phản ánh toàn bộ first-party text/source dưới `rag_old_0` và
   mọi omission có lý do;
2. provenance claims không vượt evidence;
3. field usage được lần theo code/call sites, không chỉ dựa vào schema khai báo;
4. evaluator data flow, metric cutoff và judge inputs chính xác;
5. so sánh Foods V3 dùng schema thật và code hiện hành;
6. field-necessity matrix gắn từng field với consumer/requirement cụ thể;
7. schema candidates tối giản, không lặp evidence vô cớ và không tự approval;
8. tuân thủ toàn bộ giới hạn.

Không có yêu cầu chạy tests. Dùng `git diff --check` cho tracked Markdown và tự
kiểm trailing whitespace của report untracked.

Khi hoàn tất, chuyển `session_prompt/CURRENT_HANDOFF.md` về:

- `Target role: reviewer`
- `Authored by: implementer`
- `Handoff kind: final_review`
- `State: active`

Bàn giao phải dẫn report, coverage, skipped/not verified và nhắc rõ S1/S2/S3
đang hoãn để Reviewer thảo luận lại với User sau review. Không tự đánh dấu report
approved hoặc written spec/implementation plan approved.
