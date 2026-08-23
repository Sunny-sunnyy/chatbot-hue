# Nhắc Việc Session Sau — Brainstorm Quy Tắc Đơn Giản Hóa Toàn Dự Án

## Mục đích của file này

File này lưu lại toàn bộ định hướng mà người dùng và Codex đã thống nhất trong
session thiết kế lại Phase 7.

Ở session tiếp theo, dùng file này cùng hai tài liệu Phase 7 đã duyệt để
brainstorm việc điều chỉnh bốn tài liệu governance:

```text
/home/minhhieu/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/minhhieu/hue_rag/session_prompt/REVIEWER_WORKFLOW.md
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
```

Hai tài liệu Phase 7 cần đọc cùng:

```text
/home/minhhieu/hue_rag/docs/superpowers/specs/2026-08-23-phase-7-simple-evaluation-design.md
/home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-23-phase-7-simple-evaluation-implementation.md
```

Không tự động thay toàn bộ bốn file governance. Phải đọc nội dung hiện tại,
brainstorm với người dùng, xác định phần nào cần giữ cho toàn dự án và phần nào
thực sự over-engineered, rồi mới sửa sau khi người dùng duyệt.

## Vì sao cần thay đổi

Phase 7 đã trải qua nhiều vòng implementation và review nhưng ngày càng dài,
khó đọc và khó hiểu. Luồng cần thiết vốn chỉ là:

```text
question -> retrieve -> build context -> generate -> judge -> report
```

Trong quá trình review, nhiều lớp kỹ thuật được thêm vào để giải quyết các vấn
đề do chính kiến trúc phức tạp tạo ra. Kết quả là code evaluation có nhiều file,
nhiều validator và hơn một trăm test nhưng người dùng không còn đọc và hiểu được
hệ thống.

Người dùng hiểu rõ luồng RAG cơ bản và muốn code giữ được tính “con người”:
ngắn, rõ, dễ đọc, dễ chạy và cho kết quả thật.

## Nguyên tắc code toàn hệ thống

- Code phải đơn giản, rõ ràng và dễ hiểu.
- Một người đọc code phải theo được data flow mà không cần biết nhiều thuật ngữ
  kiến trúc hoặc audit.
- Tên file, hàm và biến phải nói đúng việc chúng làm.
- Một hàm nên làm một nhiệm vụ dễ giải thích.
- Bắt đầu bằng giải pháp nhỏ nhất giải quyết được nhu cầu thật.
- Không tự thêm abstraction, wrapper, validator, state machine hoặc workflow
  phòng xa.
- Không chia nhỏ thành nhiều file nếu việc chia nhỏ khiến luồng khó theo dõi hơn.
- Không gom tất cả vào một file nếu file đó đã trở nên khó đọc; tách theo nhiệm
  vụ mà con người có thể gọi tên và giải thích.
- Không tối ưu cho các tình huống giả định chưa xảy ra.
- Không giữ code chỉ vì code đó đã tốn nhiều công sức để xây dựng.
- Khi một cơ chế không còn phục vụ nhu cầu người dùng, xóa nó thay vì đổi tên
  hoặc chuyển sang file khác.

## Kỹ thuật nâng cao vẫn được phép

Định hướng đơn giản không có nghĩa là cấm research hoặc kỹ thuật nâng cao.

Implementer có thể nghiên cứu, tối ưu hoặc đề xuất kỹ thuật mới khi:

1. có một vấn đề thật đã quan sát được;
2. giải pháp đơn giản hiện tại không đáp ứng được;
3. kỹ thuật mới có lợi ích cụ thể;
4. có thể giải thích bằng ngôn ngữ thông thường;
5. kết quả chạy thật chứng minh lợi ích;
6. độ phức tạp tăng thêm tương xứng với lợi ích.

Reviewer phải yêu cầu loại bỏ nếu kỹ thuật trở thành over-engineering hoặc khó
hiểu hơn mức cần thiết.

## Tài liệu code tham khảo cho Phase 7

Hai đường dẫn sau là tài liệu thiết kế và coding style trực tiếp cho Phase 7
evaluation:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation
```

Điểm cần học:

- code đi theo luồng thực tế;
- function có tên và nhiệm vụ rõ;
- giao diện gọi trực tiếp các hàm evaluation;
- progress và concurrency được trình bày theo cách dễ hiểu;
- không có hệ thống audit hoặc package phức tạp bao quanh luồng RAG.

Hai đường dẫn này chỉ là reference trực tiếp cho Phase 7. Không dùng chúng như
implementation blueprint cho Phase 0–6 hoặc toàn bộ backend.

Khi review Phase 6 về Phase 0, người dùng sẽ cung cấp tài liệu phù hợp riêng cho
từng phase.

## Cách tổ chức file Python Phase 7 đã duyệt

Phase 7 mới chỉ có bốn module chính:

```text
backend/evaluation/
├── __init__.py
├── test.py
├── template.py
├── eval.py
└── evaluator.py
```

### `test.py`

Chỉ đọc file câu hỏi được truyền vào. Mặc định dùng `test2.jsonl`.

### `template.py`

Chứa prompt thuộc riêng evaluation. Không sao chép production generation prompt
đang thuộc backend chính.

### `eval.py`

Được phép chứa cả retrieval evaluation và answer evaluation, dù file có thể dài
hơn, vì người dùng chấp nhận luồng tập trung và dễ theo dõi.

Nội dung chính:

- keyword-based MRR và nDCG;
- retrieval evaluation;
- generation và judge;
- batch execution;
- summary;
- ghi CSV.

### `evaluator.py`

Gộp nhiệm vụ giao diện hữu ích của evaluator cũ và `evaluator2.py` thành một
file. Không tạo thêm `evaluator2.py` trong project mới.

Giao diện có:

- file câu hỏi;
- một slider `Số câu chạy cùng lúc`, mặc định 3;
- nút `Đánh giá retrieval`;
- nút `Đánh giá câu trả lời`;
- progress;
- bảng kết quả;
- summary;
- đường dẫn CSV.

## Dữ liệu và profile Phase 7

Ban đầu dùng:

```text
knowledge-base-hue/foods/evaluation/test2.jsonl
```

File này có 20 câu thật, được copy nguyên vẹn từ bộ 104 câu và phân bổ tương đối
đều trên 8 category.

Sau khi chạy ổn định, chỉ đổi đường dẫn sang:

```text
knowledge-base-hue/foods/evaluation/tests.jsonl
```

Không xây workflow mới chỉ vì tăng từ 20 lên 104 câu.

Phase 7 hiện chỉ dùng `dense_only`. Sau này mới chạy cùng phép đánh giá để so
sánh:

- `dense_only`
- `hybrid_no_rerank`
- `hybrid_rerank`

Không xây trước màn hình hoặc orchestration cho phần so sánh chưa cần dùng.

## Retrieval evaluation đã duyệt

MRR và nDCG chỉ dựa vào keyword xuất hiện trong retrieved chunk text, không phân
biệt hoa thường.

Không bắt buộc gold file, source hoặc section để tính hai metric này.

Kết quả gồm:

- MRR;
- nDCG;
- số keyword tìm thấy;
- tổng số keyword;
- keyword coverage;
- error nếu câu đó lỗi.

Output cố định, ghi đè sau mỗi lần chạy:

```text
backend/evaluation/retrieval_results.csv
```

## Answer evaluation đã duyệt

Luồng thật:

```text
question -> dense retrieval -> context -> gpt-5.4-nano answer
-> gpt-5.4-mini judge
```

Judge chỉ dùng ba điểm giống code cũ:

- accuracy;
- completeness;
- relevance.

Ngoài ra có feedback ngắn, cụ thể và dễ hiểu.

Không có groundedness score.

Output cố định, ghi đè sau mỗi lần chạy:

```text
backend/evaluation/answer_results.csv
```

Nếu một câu lỗi, ghi lỗi vào row và tiếp tục. Không retry, resume hoặc tạo hệ
thống phục hồi phức tạp.

## Những cơ chế không cần thiết đã bị từ chối

Không xây hoặc yêu cầu những phần sau khi chúng không phục vụ trực tiếp chức
năng người dùng:

- cost accounting;
- hàm tính hoặc ước tính chi phí;
- consent hoặc paid confirmation gate cho API đã được người dùng cho phép;
- calibration;
- resume workflow;
- run ID;
- generation run ID;
- timestamp dùng để quản lý evaluation package;
- checksum;
- matching package;
- tamper detection;
- partial artifact;
- artifact audit;
- nhiều validator chồng lên nhau;
- nhiều test files chỉ để bảo vệ các cơ chế trên.

Không đổi tên hoặc chuyển nơi để giữ lại kiến trúc đã bị từ chối.

## Test phải tối giản và cần thiết

Phase 7 chỉ giữ:

```text
backend/tests/test_evaluation.py
```

Khoảng 6–8 test dễ hiểu là đủ:

- đọc đúng 20 câu;
- fields cần thiết tồn tại;
- MRR đúng;
- nDCG đúng;
- retrieval trả đúng cấu trúc;
- answer trả đúng ba điểm và feedback;
- UI handler trả đúng số output;
- `load_tests(path)` dùng đúng path.

Không đặt mục tiêu 103 test hoặc một con số lớn khác. Không tạo test chỉ để bao
phủ cơ chế không cần thiết hoặc trường hợp kỹ thuật cực hiếm.

Mỗi test phải trả lời được câu hỏi:

> Test này bảo vệ hành vi thật nào mà người dùng cần?

## Không fake, phải chạy thật

Quy tắc này áp dụng cho toàn bộ hệ thống, không riêng Phase 7.

Không được dùng:

- fake ID;
- fake dataset;
- fake provider;
- fake artifact;
- mock provider response;
- replay output;
- kết quả bịa đặt;
- output từ run cũ để tuyên bố run mới đã đạt.

Implementer và Reviewer được phép:

- truy cập online;
- dùng Qdrant thật;
- dùng model và backend thật;
- dùng API key có sẵn qua env-file loader an toàn;
- thực hiện paid API calls thật đã được người dùng cho phép;
- chạy `gpt-5.4-nano` thật;
- chạy `gpt-5.4-mini` thật;
- chạy 20 câu thật và 104 câu thật.

Không cần tạo code tính chi phí hoặc confirmation gate. Người dùng tự theo dõi
chi phí.

Test pass không thay thế live integration run. Lỗi network, Qdrant, provider,
quota hoặc model phải được báo đúng là lỗi thật, không thay bằng fallback giả.

Active Hue Qdrant collection chỉ được đọc để bảo vệ dữ liệu thật.

## Cách thiết kế notebook

Notebook phải giúp con người hiểu hệ thống, không phải chứng minh một audit
contract kỹ thuật.

Phong cách tham khảo:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0
/home/minhhieu/llm_rag/tai_lieu/notebook_simple
```

Quy tắc:

- mỗi cell chỉ làm một việc;
- Markdown giải thích ngắn ngay trước code;
- code cell ngắn;
- giới thiệu bản đơn giản trước;
- thêm từng bước theo trình tự tự nhiên;
- import backend functions thay vì duplicate runtime logic;
- hiển thị dữ liệu và kết quả mà người dùng quan tâm;
- không nhồi validator, audit, package matching hoặc test suite vào notebook;
- repository notebook để outputs rỗng và `execution_count: null`;
- Run All thật trên bản tạm để xác minh.

Notebook 07 nên đi theo thứ tự:

1. Phase 7 đánh giá gì.
2. Đọc 20 câu thật.
3. Xem một câu hỏi.
4. Chạy retrieval thật.
5. Giải thích MRR/nDCG.
6. Sinh và chấm một câu trả lời thật.
7. Xem accuracy, completeness, relevance và feedback.
8. Chạy batch 20 câu.
9. Xem summary.
10. Mở giao diện.

## Review Phase 6 về Phase 0 trước Phase 8

Không chuyển ngay sang Phase 8 sau khi Phase 7 hoàn thành.

Phải review lần lượt Phase 6 về Phase 0:

1. Người dùng cung cấp tài liệu phù hợp cho phase đó.
2. So sánh code, folders, tests và notebook hiện tại với tài liệu.
3. Tìm phần quá phức tạp, kỹ thuật hoặc không cần thiết.
4. Đề xuất thiết kế đơn giản để người dùng duyệt.
5. Xây dựng lại phần cần thiết.
6. Viết lại notebook của phase theo phong cách đơn giản.
7. Chạy hệ thống thật để xác nhận.

Kiểm tra đặc biệt xem các phase cũ có những cơ chế tương tự cost, consent,
calibration, resume, identity, timestamp package, checksum, matching package,
tamper detection, validator chồng lớp hoặc test suite quá lớn hay không.

Không tự động xóa một cơ chế chỉ vì tên của nó kỹ thuật. Trước hết phải xác định
nó có bảo vệ một nhu cầu runtime hoặc dữ liệu thật hay không. Nếu không cần thì
đề xuất bỏ; nếu cần thì giữ và giải thích bằng ngôn ngữ đơn giản.

## Bốn tài liệu cần brainstorming ở session sau

### `IMPLEMENTER_WORKFLOW.md`

Cần thảo luận cách:

- yêu cầu implementer viết code đơn giản;
- cho phép research có điều kiện;
- cấm fake và yêu cầu live evidence;
- giảm yêu cầu test quá mức;
- bỏ các gate và báo cáo kỹ thuật không cần thiết;
- vẫn giữ bảo vệ secret, dữ liệu và worktree.

### `REVIEWER_WORKFLOW.md`

Cần thảo luận cách:

- biến over-engineering thành một finding rõ ràng;
- reviewer phải đọc source và chạy thật;
- không yêu cầu thêm lớp kỹ thuật khi không có nhu cầu;
- đánh giá lợi ích so với độ phức tạp;
- vẫn giữ review độc lập và data safety.

### `Session_Prompt.md`

Cần thảo luận cách:

- ghi nguyên tắc đơn giản hóa toàn hệ thống;
- ghi quyền chạy online/API thật;
- ghi chính sách không fake;
- phân biệt reference trực tiếp của Phase 7 với reference riêng của phase khác;
- giữ shared context cần thiết nhưng bỏ audit bureaucracy.

### `Project_Status.md`

Cần thảo luận cách:

- giữ đây là snapshot ngắn, không phải audit log dài;
- ghi đúng Phase 7 simple reset;
- ghi gate review Phase 6 về Phase 0 trước Phase 8;
- không ghi lại chi tiết cost, checksum, artifact hoặc số test không còn ý nghĩa;
- giữ đủ thông tin để session sau tiếp tục mà không gây nhầm lẫn.

## Quy trình session brainstorming tiếp theo

1. Đọc đầy đủ file nhắc việc này.
2. Đọc đặc tả và implementation plan Phase 7 mới.
3. Đọc đầy đủ bốn file governance hiện tại.
4. Không sửa file ngay.
5. Liệt kê phần cần giữ, phần cần đơn giản hóa và phần cần loại bỏ trong từng
   file.
6. Hỏi người dùng từng quyết định còn ảnh hưởng lớn.
7. Trình bày thiết kế thay đổi cho bốn file.
8. Chỉ chỉnh sửa sau khi người dùng xác nhận.
9. Kiểm tra chéo để bốn tài liệu không mâu thuẫn nhau.
10. Commit/push chỉ khi người dùng cho phép trong session đó.

## Kết quả mong muốn

Sau session tiếp theo, bốn file governance phải hỗ trợ một cách làm việc:

- code dễ hiểu;
- hệ thống đơn giản;
- notebooks giống tài liệu học cho con người;
- tests vừa đủ;
- chạy thật, kết quả thật;
- không fake;
- cho phép kỹ thuật nâng cao có căn cứ;
- loại bỏ over-engineering;
- vẫn bảo vệ secrets, dữ liệu thật và phạm vi công việc.
