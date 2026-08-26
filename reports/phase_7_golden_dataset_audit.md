# Phase 7 Golden Dataset Audit

Date: `2026-08-26 +07`

Status: `discussion_input`

## 1. Mục đích

Tài liệu này ghi lại đánh giá hiện trạng của hai bộ câu hỏi Phase 7:

```text
knowledge-base-hue/foods/evaluation/test2.jsonl
knowledge-base-hue/foods/evaluation/tests.jsonl
```

Mục tiêu hiện tại là xác định vấn đề bằng bằng chứng trước khi quyết định sửa
từng phần hay tạo lại golden dataset. Tài liệu này không cấp quyền sửa JSONL,
validator, evaluation code, notebook hoặc chạy paid evaluation.

User đã chọn phạm vi A: chỉ chuẩn bị correction đủ cho Phase 7. Chưa mở một
chiến dịch làm lại toàn bộ 104 câu cho Phase 8.

Các quyết định brainstorming đã được user xác nhận:

- không thêm category hoặc câu hỏi `numerical` trong correction Phase 7;
- chọn lại smoke set 20 câu để phủ cả tám category hiện hành và bốn nhóm nguồn;
- smoke set dùng để xác nhận pipeline chạy đúng, nhanh và tiết kiệm chi phí;
- full set mới là bằng chứng chất lượng cuối khi Implementer và Reviewer sẵn
  sàng;
- giữ 104 case IDs; giữ question/reference answer nếu curated data hỗ trợ, sửa
  category, keywords, sources và sections bằng bằng chứng trực tiếp;
- chỉ thay nội dung một case hiện hữu khi chứng minh nó mơ hồ hoặc không
  grounded.
- quyết định sửa hay tạo dataset mới dựa trên bản chất vấn đề, không dựa trên
  một tỷ lệ lỗi tùy ý: tiếp tục sửa nếu schema, taxonomy và keyword-based Phase
  7 evaluation vẫn phù hợp; tạo dataset mới nếu phải thay mục tiêu đánh giá,
  schema hoặc cách gán relevance trên diện rộng.
- việc audit sâu từng case và brainstorming dữ liệu đánh giá phù hợp với Hue
  RAG được chuyển sang một session riêng.

## 2. Nguồn tham khảo và đối chiếu

Phase 7 dùng các tài liệu trong khóa học cũ làm reference về luồng học tập và
evaluation đơn giản:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/test.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/answer.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day5.txt
```

Các reference này nhấn mạnh:

```text
golden questions -> retrieve -> MRR/nDCG/coverage
golden questions -> generate -> LLM judge -> answer scores
measure -> identify weakness -> change -> re-evaluate
```

Điểm cần giữ là data flow dễ đọc và việc cải tiến dựa trên số liệu. Không sao
chép dashboard, concurrency, provider hoặc advanced RAG machinery từ
`rag_old_0` nếu Hue RAG chưa có nhu cầu thật.

Nguồn đối chiếu trong project:

```text
guides/phase_7_retrieval_answer_evaluation.md
backend/evaluation/test.py
backend/evaluation/eval.py
knowledge-base-hue/foods/evaluation/validate_tests.py
knowledge-base-hue/meta/foods-template.md
knowledge-base-hue/foods/**/*.md
```

## 3. Kết quả audit hiện tại

Validator hiện hành đạt:

```text
PASS: 104 tests, all checks green
```

Các thuộc tính tốt đã quan sát:

- 104 `case_id` hợp lệ và không trùng;
- 104 câu hỏi không trùng;
- reference answer không rỗng, trung bình khoảng 147 ký tự;
- mỗi câu có 2 hoặc 3 keywords;
- mọi path trong `relevant_sources` tồn tại;
- mọi heading trong `relevant_sections` tồn tại;
- `test2.jsonl` gồm 20 dòng được copy nguyên vẹn từ `tests.jsonl`;
- full set có độ phủ nguồn tương đối cân bằng.

| Nhóm nguồn chính | Số câu |
|---|---:|
| Local specialties | 29 |
| Cafes | 29 |
| Food guides | 24 |
| Restaurants | 22 |

Phân bố category hiện tại:

| Category | Số câu |
|---|---:|
| `direct_fact` | 21 |
| `temporal` | 10 |
| `comparative` | 6 |
| `relationship` | 16 |
| `spanning` | 17 |
| `holistic` | 11 |
| `food_knowledge` | 10 |
| `guide_planning` | 13 |
| `numerical` | 0 |

## 4. Findings

### 4.1. Bộ 20 câu không còn đại diện cho corpus hiện tại

`test2.jsonl` phủ tám category đang có, nhưng phân bố nguồn là:

| Nhóm nguồn chính | Số câu trong test2 |
|---|---:|
| Local specialties | 11 |
| Restaurants | 5 |
| Food guides | 4 |
| Cafes | 0 |

Full set hiện có 29 câu cafe, nhưng smoke set không có một câu nào lấy từ
`foods/cafes/`. Vì vậy batch 20 câu sau Phase 6 không kiểm tra trực tiếp phần
cafe hoặc nhóm dữ liệu cà phê muối mới hơn.

Đây là finding chắc chắn cần xử lý nếu `test2.jsonl` tiếp tục là smoke set đại
diện cho Hue Foods RAG.

### 4.2. Category có một lỗi rõ và một khoảng trống

- `foods-0098` hỏi khung giờ mở cửa nhưng đang mang category `direct_fact`;
  `temporal` phù hợp hơn với taxonomy hiện hành.
- Validator cho phép `numerical`, nhưng dataset không có câu nào thuộc category
  này.

Khoảng trống `numerical` chưa tự động tạo requirement phải thêm câu. Cần xác
định Phase 7 có thật sự cần đánh giá câu hỏi giá, số lượng hoặc khoảng số hay
không trước khi bổ sung.

### 4.3. Một số source/section annotations sai hoặc thiếu

Các trường hợp chắc chắn đã đối chiếu trực tiếp với curated Markdown:

| Case | Vấn đề |
|---|---|
| `foods-0087` | Reference answer nói về quán phù hợp làm việc/học tập, nhưng chỉ khai báo `foods/food-guides.md`; keyword `làm việc` không có trong source này. Các bằng chứng thật nằm trong các file cafe riêng. |
| `foods-0088` | Reference answer liệt kê sáu quán trong AEON MALL nhưng chỉ khai báo `foods/cafes/koi the hue.md`, file này chỉ chứng minh phần KOI Thé. |
| `foods-0101` | Hai người sáng tạo cà phê muối nằm trong section `Nguồn gốc và bối cảnh`, không phải `Tóm tắt` như annotation hiện tại. |
| `foods-0064` | Keyword `lá dong` và bằng chứng tương ứng nằm trong `Thành phần và đặc điểm`, không phải `Tóm tắt`. |

Audit tự động còn tìm thấy 44 keyword/declared-section mismatches. Không được
coi cả 44 là lỗi: nhiều entity name nằm ở heading cấp `#` nên không lặp lại
trong body của section. Mỗi trường hợp phải được đọc trực tiếp trước khi sửa.

### 4.4. Validator kiểm tra cấu trúc tốt nhưng chưa xác minh annotation semantics

Validator hiện kiểm tra:

- keyword xuất hiện ở đâu đó trong toàn foods knowledge base;
- keyword xuất hiện trong reference answer;
- source file tồn tại;
- section heading tồn tại.

Validator chưa kiểm tra keyword/reference claim có thực sự được source và
section đã khai báo hỗ trợ hay không. Vì vậy kết quả `all checks green` chỉ xác
nhận structural validity, chưa xác nhận đây là ground-truth annotation đúng.

Không nên lập tức thêm validator ngữ nghĩa phức tạp. Trước tiên cần sửa các lỗi
chắc chắn bằng source review; chỉ thêm một check tự động nhỏ nếu nó bảo vệ một
lỗi quan trọng có nguy cơ tái diễn.

### 4.5. Một số keywords quá rộng cho retrieval metric

Metric Phase 7 tìm substring keyword trong retrieved chunk. Audit theo curated
file cho thấy 21 keyword occurrences nằm trong ít nhất 15 files. Ví dụ:

| Keyword | Số curated files có keyword |
|---|---:|
| `sả` | 44 |
| `cà phê` | 28 |
| `cà phê muối` | 22 |
| `10:00` | 21 |
| `bột lọc` | 20 |

Một chunk sai entity vẫn có thể nhận điểm nếu chứa từ rộng như `cà phê`. Vì
vậy MRR/nDCG/coverage hiện hữu là keyword-based proxy, không phải gold relevance
judgment. Điều này phù hợp với Phase 7 đơn giản, nhưng keyword của từng câu cần
đủ đặc trưng để proxy có ý nghĩa.

Không nên đổi metric hoặc thêm framework labeling trong correction Phase 7 nếu
chỉ cần thay một số keyword yếu bằng phrase/entity cụ thể hơn.

### 4.6. Bộ câu hỏi thiên về các mẫu dễ và lặp cấu trúc

Quan sát theo hình thức câu hỏi:

- khoảng 25 câu địa chỉ;
- khoảng 12 câu thời gian;
- khoảng 25 câu selection/list/planning;
- phần còn lại là relationship, comparison và food knowledge.

Độ phủ này đủ cho baseline học tập và smoke verification. Nó chưa phải bằng
chứng mạnh để phân biệt các retrieval profile hoặc model gần nhau trong Phase
8. Việc nâng lên benchmark-grade thuộc một scope riêng sau Phase 7 correction.

## 5. Đánh giá tổng thể

### Đủ tốt cho mục tiêu nào

- Full set 104 câu: đủ làm baseline Phase 7 sau khi sửa các lỗi annotation và
  category chắc chắn.
- Small set 20 câu: chưa đủ đại diện vì thiếu hoàn toàn cafe; nên chọn lại từ
  chính 104 câu, không viết câu giả hoặc thay đổi nội dung nguồn.
- Phase 8 model/profile selection: chưa nên coi keyword metrics hiện tại là
  ground truth duy nhất.

### Không nên làm lúc này

- không viết lại toàn bộ 104 câu chỉ vì một số annotations sai;
- không thêm embedding/LLM validator cho golden dataset;
- không thêm version, checksum, manifest, audit package hoặc dataset registry;
- không mở rộng metric ngoài MRR, nDCG và coverage trong correction Phase 7;
- không dùng web để sửa factual claims nếu user chưa duyệt data-enrichment
  scope.

## 6. Tiêu chí quyết định sửa hay tạo lại

Ưu tiên **sửa surgical** nếu audit đầy đủ xác nhận:

- phần lớn reference answers được curated sources hỗ trợ;
- lỗi tập trung ở source/section annotations, category và keyword selection;
- có thể chọn lại 20 câu đại diện từ 104 câu hiện hữu;
- không cần thay đổi mục tiêu hoặc metric Phase 7.

Chỉ cân nhắc **tạo lại dataset** nếu phát hiện một trong các điều sau:

- nhiều reference answers không được curated corpus hỗ trợ;
- taxonomy category không còn phản ánh câu hỏi người dùng cần đánh giá;
- phần lớn keywords không thể làm proxy retrieval có ý nghĩa;
- full set không đại diện cho corpus hoặc use cases hiện hành;
- Phase 8 yêu cầu gold relevance labels khác hẳn Phase 7 keyword evaluation.

Evidence hiện tại nghiêng rõ về sửa surgical, chưa có bằng chứng cần tạo lại
104 câu.

Nếu audit đầy đủ sau đó cho thấy dataset hiện tại không đủ chất lượng ở mức hệ
thống, không biến việc correction thành một lần âm thầm viết lại
`tests.jsonl`. Dataset hiện tại phải được giữ nguyên để bảo toàn baseline và
lịch sử đánh giá. Một golden dataset mới sẽ dùng file riêng; tên file, schema,
case selection, migration và acceptance sẽ được user và Reviewer brainstorming
trong session tiếp theo trước khi tạo hoặc triển khai.

## 7. Phạm vi đang được thảo luận

Correction dataset Phase 7 có thể gồm:

1. đọc và audit trực tiếp 104 rows với declared sources/sections;
2. sửa các annotation/category/keyword sai đã được chứng minh;
3. chọn lại 20 rows nguyên vẹn từ full set để phủ restaurants, local
   specialties, food guides và cafes;
4. giữ case IDs của full set ổn định;
5. chạy validator structural và kiểm tra exact subset;
6. chỉ sau implementation mới chạy retrieval/answer verification theo scope
   được user duyệt.

Các lựa chọn dành cho session brainstorming dữ liệu tiếp theo:

- audit đầy đủ từng case với curated source và section;
- danh sách chính xác 20 case cho smoke set;
- có cần một check nhỏ cho source/section consistency hay chỉ dùng manual audit;
- exact commands và acceptance cho full 104-question run;
- full set hiện tại chỉ cần sửa surgical hay có lỗi thiết kế mang tính hệ thống.

## 8. Golden dataset mới nếu dataset hiện tại không đạt

Việc tạo golden dataset mới là một scope riêng cho session tiếp theo, chỉ kích
hoạt nếu audit đầy đủ và đối chiếu bài học chứng minh lỗi mang tính hệ thống.
Session đó phải tham khảo các tiêu chí, cách đánh giá và evaluation loop trong
`rag_old_0`, rồi điều chỉnh cho curated data, retrieval contract và mục tiêu
thực tế của Hue RAG. Khi đó:

1. giữ nguyên `knowledge-base-hue/foods/evaluation/tests.jsonl`;
2. không tái sử dụng cùng path để che việc thay baseline;
3. brainstorming lại mục tiêu đánh giá, taxonomy, case distribution, keyword
   hoặc relevance labels và relationship với Phase 8;
4. chọn một path mới sau khi user duyệt design;
5. tạo spec và implementation plan riêng trước khi Implementer viết dataset;
6. không dùng web hoặc enrich curated facts nếu user chưa duyệt data scope.

Chưa tạo path hoặc file golden dataset mới trong session hiện tại.

Chưa tạo implementation plan hoặc prompt cho Implementer cho đến khi các lựa
chọn này được brainstorming và user duyệt.
