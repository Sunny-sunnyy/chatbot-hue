# Implementer Workflow

## Mục đích

Dùng file này khi user giao một phase hoặc correction đã được duyệt cho
Implementer. Implementer viết code rõ ràng, chạy hệ thống thật và bàn giao bằng
một report ngắn. Implementer không tự approve.

Quy tắc chung nằm trong:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
```

File này chỉ bổ sung trách nhiệm riêng của Implementer.

## Bắt đầu session

Đọc:

```text
/home/minhhieu/hue_rag/session_prompt/Session_Prompt.md
/home/minhhieu/hue_rag/session_prompt/Project_Status.md
/home/minhhieu/hue_rag/session_prompt/IMPLEMENTER_WORKFLOW.md
/home/minhhieu/hue_rag/guides/README.md
/home/minhhieu/hue_rag/guides/phase_0_mvp_foundation.md
guide canonical của phase được giao
/home/minhhieu/hue_rag/session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md
```

Nếu đang sửa finding, đọc Codex review hiện hành. Nếu task liên quan model,
retrieval, evaluation hoặc benchmark, đọc
`reports/hue_foods_rag_benchmark.md`.

Task code, notebook, test hoặc refactor phải đọc và áp dụng:

```text
skills/practical-project-coding/SKILL.md
```

Chạy `git status --short`. Giữ nguyên mọi thay đổi không liên quan.

Nếu không xác định được duy nhất phase, guide hoặc correction scope, hỏi user
đúng một câu thay vì đoán.

## Khi nào được implement

Chỉ bắt đầu khi:

- guide canonical có trạng thái `ready`; hoặc
- trạng thái là `changes_requested` và Codex review/user feedback ghi rõ phần
  cần sửa.

Guide là read-only với Implementer. Thay đổi scope, interface, acceptance,
provider, model hoặc data contract phải quay lại Reviewer và user.

## Cách implement

- Giải thích được data flow bằng ngôn ngữ thông thường.
- Bắt đầu bằng giải pháp nhỏ nhất đáp ứng nhu cầu.
- Một file/hàm có nhiệm vụ rõ ràng.
- Reuse backend hiện có khi phù hợp; không copy một pipeline thứ hai.
- Khi sửa Phase 0–6 sau review, đối chiếu guide và finding với source code,
  notebook cùng hành vi live hiện có; tài liệu ngoài chỉ bổ sung khi user cung
  cấp và thực sự hữu ích.
- Không thêm abstraction, wrapper, validator hoặc flexibility phòng xa.
- Không refactor ngoài phạm vi.
- Xóa import, biến hoặc code do chính thay đổi hiện tại làm dư thừa.
- Không giữ cơ chế đã bị guide yêu cầu loại bỏ bằng cách đổi tên hoặc chuyển file.

Kỹ thuật nâng cao chỉ được đề xuất khi có vấn đề thật, giải pháp đơn giản không
đủ, lợi ích có thể giải thích và real-system run chứng minh lợi ích. Nếu độ
phức tạp vượt lợi ích, phải bỏ kỹ thuật đó.

## Test

- Chỉ tạo test cho hành vi thật và lỗi thực tế quan trọng.
- Không đặt mục tiêu số lượng test hoặc coverage.
- Không tạo nhiều test files cho edge case kỹ thuật hiếm.
- Không dùng mock hoặc fake.
- Dùng real project data và dependency thật phù hợp với hành vi đang kiểm tra.
- Mỗi test phải dễ đọc và trả lời được nó bảo vệ nhu cầu nào của user.
- Trước khi giữ test cũ, đặt lại đúng câu hỏi đó.
- Audit test thuộc phase hiện tại và downstream scope bị ảnh hưởng trực tiếp.
- Xóa test cũ nếu không còn bảo vệ nhu cầu thật, chỉ dựng lỗi giả định, trùng
  live verification hoặc chỉ phục vụ cơ chế đang bị loại bỏ.
- Không chạy test đã xác định là không cần thiết; phase có thể không cần
  automated test.
- Test pass không thay live run.

Chạy exact live path và smallest relevant test trước. Chỉ chạy full backend
suite khi shared runtime/data contract ảnh hưởng nhiều phase hoặc ở cuối chiến
dịch simplicity review Phase 0–6. Chỉ chạy evaluation 20 câu khi thay đổi có
thể ảnh hưởng chất lượng RAG; không mặc định chạy bộ 104 câu.

Không dựng dead URL, xóa collection giữa request hoặc thay environment chỉ để
tạo failure giả định. Chỉ giữ failure test cho lỗi thực tế quan trọng có nguy
cơ tái diễn.

## Debugging và tự review

Khi có bug thật:

1. tái tạo lỗi nhất quán;
2. thu bằng chứng và chứng minh nguyên nhân gốc;
3. thử một focused fix tại một thời điểm;
4. sửa nguyên nhân thay vì thêm fallback hoặc guard che lỗi;
5. chạy lại exact live path; chỉ thêm regression test khi thật sự cần.

Trước handoff, tự review exact diff về code/test dư thừa, duplication,
helper một-caller, abstraction phòng xa và data flow khó hiểu. Giải thích lựa
chọn chỉ khi có trade-off thật; không bắt buộc nêu design pattern. Kiểm tra
security theo input/API, secret, provider, data và destructive target thực sự
bị thay đổi; không tạo security audit giả cho scope không liên quan.

## Chạy và xác minh thật

- Dùng curated/canonical data, actual service state và production backend path.
- Dùng Qdrant, local model và provider API thật theo guide.
- Online và paid API calls trong approved phase được phép, không cần consent
  gate hoặc cost code.
- Không dùng fake ID/data/provider/artifact, mock response, replay hoặc prior
  output làm PASS evidence.
- Ghi đúng failed, skipped và partial outcome.
- Active Hue collection chỉ read-only; mutation cần exact approved isolated
  target hoặc user approval riêng.
- Không đổi provider/model, mở rộng dataset/scope, deploy hoặc thực hiện
  destructive action nếu chưa được duyệt.

Dùng `uv` và safe env-file loader theo `Session_Prompt.md`. Không mở hoặc in
secret values.

## Notebook

Chỉ tạo hoặc cập nhật notebook khi canonical guide của phase yêu cầu vì có giá
trị học tập thật. Không tạo notebook chỉ để đủ số phase. Phase 1 không cần
notebook sau simplicity review.

- Mỗi cell làm một việc.
- Markdown ngắn đứng trước code.
- Code ngắn và gọi backend, không duplicate logic.
- Notebook không phải validator, audit package hoặc test suite.
- Repository notebook sạch outputs và execution counts.
- Run All thật trên temporary copy.
- Dùng đúng style references trong `Session_Prompt.md`.

Nếu guide không yêu cầu notebook, implementation report ghi rõ `not
applicable`; không thay thế notebook bằng validator hoặc smoke-test artifact.

## CodeGraph

CodeGraph là công cụ tùy chọn để hiểu code và giới hạn blast radius. Nó không
phải checkpoint bắt buộc. Missing/stale index hoặc lỗi CodeGraph không chặn
task; tiếp tục bằng `rg`, đọc source trực tiếp và real verification.

Khi CodeGraph sẵn sàng và hữu ích:

```bash
codegraph status .
```

- `Index is up to date`: có thể dùng graph.
- Có pending files hoặc index stale: có thể chạy `codegraph sync .`.
- `Not initialized` hoặc sync lỗi: không tự init/uninit; tiếp tục bằng công cụ
  đọc source thông thường và ghi giới hạn nếu nó ảnh hưởng công việc.

### Cách dùng trước và trong implementation

Ưu tiên query hẹp:

```bash
codegraph explore "Trace how <entry point> reaches <dependency or side effect>."
codegraph node <symbol-or-file>
codegraph callers <symbol>
codegraph callees <symbol>
codegraph impact <symbol>
```

Sau khi xác định changed files hoặc trước khi chọn tests:

```bash
git diff --name-only | codegraph affected --stdin
codegraph affected backend/path/to/module.py
```

Dùng output để:

- tìm module và interface hiện có cần reuse;
- tìm callers/callees trước khi đổi signature;
- kiểm tra blast radius;
- chọn smallest relevant tests.

### Ví dụ CodeGraph 1.5.0

- `codegraph status .`: index sạch kết thúc bằng
  `✓ Index is up to date`; thay đổi chưa sync hiện `### Pending sync:`.
- `codegraph explore "<query>"`: trả symbols, files, callers và tests liên
  quan.
- `codegraph affected <file>`: gợi ý test files bị ảnh hưởng.
- `codegraph query <keyword>`: tìm symbol trước khi dùng
  `node`/`callers`/`impact`.

CodeGraph không thay guide, source reads, tests hoặc evidence thật. Khi graph
mâu thuẫn với source, source và real execution có ưu tiên. Không đưa secrets,
private endpoints hoặc credentials vào query. Không init, uninit, xóa
`.codegraph/` hoặc đổi telemetry nếu user chưa yêu cầu.

## Implementation report

Sau khi hoàn tất scope, viết:

```text
reports/phase_<id>_<short_name>_implementation_report.md
```

Dùng `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md` với sáu mục:

1. phạm vi;
2. thay đổi chính;
3. cách đã chạy thật;
4. kết quả quan sát;
5. lỗi và giới hạn;
6. handoff cho Reviewer.

Không lặp governance checklist. Chỉ ghi security/data-safety detail khi task có
rủi ro hoặc hành động liên quan. Không trình bày expected result như observed.

## Phản hồi review

1. Đọc Codex review.
2. Sửa blocker và major trong exact correction scope.
3. Sửa minor khi đơn giản, cần thiết và không mở rộng thiết kế.
4. Chạy lại kiểm tra thật bị ảnh hưởng.
5. Cập nhật implementation report.
6. Không sửa Codex review.

Nếu correction yêu cầu interface hoặc kiến trúc ngoài guide, dừng và trả lại
Reviewer/user.

Sau lần `changes_requested` thứ 4, không bắt đầu vòng sửa thứ 5. Reviewer phải
audit lại guide, design, plan, acceptance và findings trước.

## Không thuộc quyền Implementer

- Tự approve phase.
- Sửa guide canonical hoặc trạng thái phase.
- Sửa Codex review, user report hoặc `Project_Status.md`.
- Commit hoặc push.
- Mở rộng scope, đổi provider/model hoặc deploy.
- Sửa runtime ngoài approved phase.

Kết thúc bằng `git diff --check`, danh sách changed files và handoff rõ ràng.
