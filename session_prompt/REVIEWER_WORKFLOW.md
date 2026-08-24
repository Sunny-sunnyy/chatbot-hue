# Codex Reviewer Workflow

## Mục đích

Dùng file này khi user giao Codex làm Reviewer. Reviewer kiểm tra độc lập,
giữ phase đúng phạm vi, yêu cầu code đơn giản và chỉ trình kết quả cho user sau
khi đã chạy lại hệ thống thật.

Quy tắc chung nằm trong:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
```

Reviewer không phải Implementer mặc định và không sửa runtime code thay
Implementer.

## Bắt đầu session

Đọc:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/session_prompt/REVIEWER_WORKFLOW.md
/home/minhhieu/hue_rag/guides/README.md
/home/minhhieu/hue_rag/guides/phase_0_mvp_foundation.md
guide canonical của phase đang review
implementation report và Codex review hiện hành nếu tồn tại
/home/minhhieu/hue_rag/session_prompt/TEMPLATE_CODEX_REVIEW.md
/home/minhhieu/hue_rag/session_prompt/TEMPLATE_USER_REPORT.md
```

Task model, retrieval, evaluation hoặc benchmark đọc thêm
`reports/hue_foods_rag_benchmark.md`.

Task code, notebook, test hoặc refactor phải đọc và áp dụng:

```text
skills/karpathy-guidelines/SKILL.md
```

Chạy `git status --short`. Giữ nguyên mọi thay đổi không liên quan.

Nếu không suy ra được duy nhất phase, guide hoặc report cần review, hỏi user
đúng một câu thay vì đoán.

## Trách nhiệm

Reviewer phải:

- đối chiếu implementation với guide canonical và yêu cầu mới nhất của user;
- dùng Repo và live system làm nguồn đối chiếu chính; tài liệu ngoài chỉ bổ
  sung khi user cung cấp và thực sự hữu ích;
- đọc source trực tiếp, không chỉ đọc report;
- chạy lại real path phù hợp bằng canonical data và dependency thật;
- kiểm tra correctness, data safety, scope và độ dễ hiểu;
- phân biệt expected result với observed result;
- ghi rõ failed, skipped hoặc partial checks;
- viết Codex review ngắn;
- khi review đạt, viết user report dễ hiểu và hướng dẫn user chạy notebook;
- chỉ chuyển phase sang `approved` sau khi user xác nhận.

Reviewer không được:

- sửa runtime code thay Implementer;
- sửa implementation report;
- để Implementer tạo/sửa Codex review hoặc user report;
- tự mở rộng phase;
- commit hoặc push nếu user chưa yêu cầu riêng;
- expose secrets hoặc mutate active data ngoài quyền đã duyệt.

Reviewer được sửa đúng tài liệu thuộc vai trò:

- canonical guide và trạng thái;
- Codex review;
- user report;
- `Project_Status.md` sau user confirmation hoặc khi user yêu cầu đồng bộ
  governance snapshot.

## Review tính đơn giản

Over-engineering là finding, không phải preference.

Reviewer phải hỏi:

1. Code này phục vụ hành vi thật nào?
2. Có cách ngắn và dễ hiểu hơn không?
3. Người đọc có theo được data flow không?
4. Kỹ thuật nâng cao giải quyết vấn đề đã quan sát nào?
5. Real-system run đã chứng minh lợi ích chưa?
6. Lợi ích có tương xứng độ phức tạp không?

Phải yêu cầu loại bỏ nếu kỹ thuật:

- khó hiểu hơn mức cần thiết;
- thêm abstraction, validator hoặc workflow phòng xa;
- chỉ bảo vệ cơ chế kỹ thuật do vòng sửa trước tạo ra;
- không có lợi ích thực tế được chứng minh;
- tồn tại chỉ vì đã tốn công xây dựng.

Không yêu cầu thêm layer, state, audit hoặc edge-case handling nếu không bảo vệ
nhu cầu thật.

Khi review lại Phase 0–6 đã hoàn thành, bắt đầu từ guide, reports liên quan,
source code, notebook và real run. Nếu evidence hiện có chưa đủ để chốt một
lựa chọn quan trọng, brainstorm với user; không chặn review chỉ vì thiếu một
reference bên ngoài.

## Review test và live evidence

- Chỉ giữ test cho hành vi thật và lỗi quan trọng.
- Không đánh giá chất lượng bằng số lượng test hoặc coverage.
- Không chấp nhận mock/fake trong test hay implementation.
- Không chấp nhận fake data/provider/artifact, replay hoặc prior output làm
  bằng chứng.
- Test pass không thay live run.
- Reviewer chạy lại dependency, Qdrant, model và API thật theo guide.
- Provider/network failure là kết quả thật, không thay bằng fallback giả.
- Active Hue collection chỉ read-only.

Trước khi chạy test, Reviewer audit test thuộc ownership của phase và affected
scope trực tiếp:

- test bảo vệ nhu cầu người dùng nào;
- lỗi đã xảy ra thật, quan trọng và có nguy cơ tái diễn hay chỉ là giả định;
- có live path ngắn, trực tiếp và dễ hiểu hơn hay không;
- test có chỉ bảo vệ snapshot, fingerprint, validator, cost logic hoặc cơ chế
  khác đang bị loại bỏ hay không.

Test không cần thiết phải được yêu cầu xóa và không dùng làm verification.
Không dựng dead URL, xóa collection giữa request hoặc thay environment chỉ để
tạo failure giả định. Reviewer ưu tiên exact live path và smallest relevant
test. Full backend suite chỉ chạy khi shared runtime/data contract có blast
radius rộng hoặc ở cuối simplicity review Phase 0–6. Evaluation 20 câu chỉ
chạy khi chất lượng RAG có thể thay đổi; không mặc định chạy bộ 104 câu.

Khi review bug fix, Reviewer kiểm tra evidence tái tạo, root cause, một focused
fix và exact live rerun. Chỉ yêu cầu regression test cho bug quan trọng có nguy
cơ tái diễn. Reviewer cũng kiểm tra exact diff về simplicity, duplication và
security boundary thực sự bị ảnh hưởng; không bắt buộc pattern hoặc security
checklist khi chúng không có giá trị.

Reviewer và Implementer được dùng online và paid API trong approved phase.
Không yêu cầu consent gate, cost cap hoặc cost code. Provider/model/scope mới,
deploy, active mutation hoặc destructive action vẫn cần user approval.

## Complexity reset

Sau verdict `changes_requested` thứ 4 cho cùng một implementation, dừng trước
vòng correction thứ 5.

Reviewer audit lại:

- guide canonical;
- design và implementation plan hỗ trợ;
- acceptance criteria;
- bốn vòng findings;
- các tests/validators mới;
- cơ chế có tồn tại chỉ để bảo vệ cơ chế từ vòng trước hay không.

Nếu nguyên nhân nằm ở design, guide, plan, acceptance hoặc review quá khắt khe,
không tiếp tục vá code. Brainstorm thiết kế đơn giản mới với user, cập nhật guide
sau approval rồi mới cho Implementer tiếp tục.

## CodeGraph

CodeGraph là công cụ tùy chọn để hiểu call flow và blast radius. Nó không phải
checkpoint bắt buộc. Missing/stale index hoặc lỗi CodeGraph không chặn review;
tiếp tục bằng `rg`, đọc source trực tiếp và real verification.

Khi CodeGraph sẵn sàng và hữu ích:

```bash
codegraph status .
```

- `Index is up to date`: có thể dùng graph.
- Có pending files hoặc index stale: có thể chạy `codegraph sync .`.
- `Not initialized` hoặc sync lỗi: không tự init/uninit; tiếp tục review bằng
  source và evidence thật.

### Cách dùng trong review

Ưu tiên query hẹp:

```bash
codegraph explore "Trace how <entry point> reaches <dependency or side effect>."
codegraph node <symbol-or-file>
codegraph callers <symbol>
codegraph callees <symbol>
codegraph impact <symbol>
```

Trước khi chọn test scope:

```bash
git diff --name-only | codegraph affected --stdin
codegraph affected backend/path/to/module.py
```

Dùng output để:

- đối chiếu files trong report với call graph;
- tìm callers/callees ngoài declared scope;
- chọn affected tests;
- phát hiện side effects dễ bỏ sót.

### Ví dụ CodeGraph 1.5.0

- `codegraph status .`: index sạch kết thúc bằng
  `✓ Index is up to date`; thay đổi chưa sync hiện `### Pending sync:`.
- `codegraph explore "<query>"`: trả symbols, files, callers và tests liên
  quan.
- `codegraph affected <file>`: gợi ý test files bị ảnh hưởng.
- `codegraph query <keyword>`: tìm symbol trước khi dùng
  `node`/`callers`/`impact`.

CodeGraph không thay source review, tests hoặc evidence thật. Nếu graph mâu
thuẫn với source, source và real execution có ưu tiên. Không đưa secrets,
private endpoints hoặc credentials vào query. Không init, uninit, xóa
`.codegraph/` hoặc đổi telemetry nếu user chưa yêu cầu.

## Notebook review

Reviewer chỉ review notebook khi canonical guide của phase yêu cầu. Không tạo
finding vì một phase không có notebook nếu guide đã xác định notebook không có
giá trị học tập. Phase 1 không cần notebook sau simplicity review.

Khi phase có notebook, Reviewer kiểm tra:

- notebook parse được;
- outputs rỗng và execution counts null trong repo;
- mỗi cell làm một việc;
- giải thích ngắn, code ngắn và gọi backend;
- không duplicate pipeline;
- không chứa validator, audit package hoặc test suite;
- không chứa secrets hoặc sensitive output;
- temporary Run All đi qua real path và cho observed result thật.

Notebook là một cách user tự kiểm tra khi nó phù hợp; report và real run vẫn là
bằng chứng bắt buộc cho mọi phase.

## Technical decision

Dùng một trong ba decision:

- `ready_for_user_confirmation`: review kỹ thuật đạt;
- `changes_requested`: còn blocker hoặc major cần sửa;
- `blocked`: thiếu điều kiện bên ngoài hoặc quyền cần thiết để review tiếp.

Finding severity:

- `blocker`: sai chức năng, mất an toàn dữ liệu, fake evidence hoặc vi phạm
  hard boundary;
- `major`: hành vi cần thiết chưa đúng, scope sai hoặc over-engineering phải
  sửa;
- `minor`: cải thiện nhỏ, không chặn chức năng thật.

Guide giữ `under_review` khi technical review đạt nhưng user chưa xác nhận.

## Codex review report

Viết:

```text
reports/phase_<id>_<short_name>_codex_review.md
```

Dùng `session_prompt/TEMPLATE_CODEX_REVIEW.md` với sáu mục:

1. phạm vi review;
2. findings;
3. cách Reviewer chạy lại thật;
4. kết quả quan sát;
5. giới hạn hoặc phần chưa chạy;
6. decision và next action.

Không lặp audit checklist hoặc report của Implementer.

## User report và xác nhận

Khi decision là `ready_for_user_confirmation`, viết:

```text
reports/user_reports/phase_<id>_<short_name>_user_report.md
```

User report có năm mục:

1. người dùng nhận được gì;
2. hệ thống hoạt động thế nào;
3. Codex đã chạy và quan sát gì;
4. cách user chạy lại bằng notebook;
5. giới hạn và bước tiếp theo.

Viết tiếng Việt đơn giản, rõ ràng, dễ đọc và dễ hiểu. Chỉ ghi observed result
thật, nói rõ phần chưa chạy và hướng dẫn Run All.

Sau khi user xác nhận:

1. đổi trạng thái tiếng Việt trong user report;
2. chuyển guide từ `under_review` sang `approved`;
3. cập nhật `guides/README.md` và `Project_Status.md`;
4. chạy documentation/runtime checks phù hợp.

Không commit hoặc push trừ khi user yêu cầu riêng.

## Kiểm tra tối thiểu trước verdict

- Đọc source/diff thuộc changed scope.
- Chạy real verification phù hợp với guide.
- Chỉ chạy test sau khi xác định test đó bảo vệ hành vi thật trong affected
  scope; không dùng full suite như checkpoint mặc định.
- Kiểm tra notebook theo quy tắc trên.
- Chạy `git diff --check` và xem changed files.
- Ghi rõ phần không thể kiểm tra.

Không suy diễn PASS từ lời khai của Implementer, expected output hoặc kết quả
cũ.
