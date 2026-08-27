---
name: practical-project-coding
description: Use for tasks that design implementation, write, debug, refactor, review, or verify code and tests. Focus on clear data flow, proportional complexity, surgical scope, useful tests, and fresh real-system evidence. Do not use for docs-only work, data curation, status reporting, or general questions.
---

# Practical Project Coding

## Mục đích

Giúp coding agent giải quyết đúng nhu cầu thật bằng code rõ ràng, dễ hiểu và có
verification tương xứng. Skill này là nền tảng dùng chung; nó không thay thế
governance của dự án, workflow theo vai trò, convention framework hoặc skill
chuyên ngành.

Code không cần phải ngắn. Độ phức tạp được chấp nhận khi nó giải quyết một vấn
đề thực tế, cách trực tiếp hơn không đủ, lợi ích giải thích được và chi phí đọc,
chạy, kiểm tra, bảo trì vẫn tương xứng. Không dùng kỹ thuật nâng cao chỉ vì nó
phổ biến, hiện đại hoặc có thể hữu ích trong tương lai.

Không biến skill này thành ceremony. Task nhỏ, rõ ràng chỉ cần thay đổi nhỏ và
exact verification. Task có trade-off quan trọng mới cần làm rõ assumption,
so sánh phương án và chờ duyệt thiết kế trước khi implement.

## Hai loại nguồn sự thật

### Quyền hạn và requirement

Khi các instruction khác nhau, ưu tiên:

1. safety, permission và ràng buộc của platform;
2. yêu cầu mới nhất đã được người dùng xác nhận;
3. project governance áp dụng cho exact path;
4. workflow đúng với vai trò hiện tại;
5. canonical guide hoặc contract của task/phase;
6. design và implementation plan đã được duyệt.

Report, status snapshot và convention quan sát được không tự tạo requirement
mới. Không âm thầm chọn một nguồn thấp hơn để override nguồn cao hơn.

### Evidence về hành vi thực tế

Để xác định hệ thống đang làm gì, đọc source code, canonical data, dependency
state và fresh execution phù hợp. Code hiện tại hoặc một run cũ không override
requirement đã duyệt; chúng là evidence để đối chiếu implementation với
requirement.

Nếu instruction và hành vi thật mâu thuẫn theo cách làm thay đổi behavior,
scope, data contract, kiến trúc hoặc verification, nêu rõ mâu thuẫn và xin
quyết định thay vì tự chọn.

## Ngôn ngữ

- Tên biến, hàm, class, type, API và schema dùng English rõ ràng.
- Comment và docstring cần thiết ưu tiên viết bằng tiếng Việt, trừ khi project
  governance quy định rõ ngôn ngữ khác.
- Chỉ comment về mục đích, lý do, constraint, assumption hoặc trade-off mà code
  không tự thể hiện; không chú thích lại câu lệnh hiển nhiên.
- Không dùng comment để biện hộ cho code khó hiểu. Đơn giản hóa code trước.

## Cổng 1: Trước khi sửa

- Đọc instruction áp dụng cho exact path và giữ nguyên thay đổi không liên quan.
- Xác định behavior hiện tại, behavior mong muốn, affected data flow và scope.
- Nêu assumption hoặc điểm chưa rõ chỉ khi chúng có thể thay đổi kết quả.
- Xác định success criteria có thể quan sát và cách verification phù hợp.
- Tìm production path hoặc module đang dùng trước khi tạo đường đi thứ hai.
- Chọn giải pháp nhỏ nhất đáp ứng đầy đủ requirement, không phải giải pháp có ít
  dòng nhất.

Không tự tạo hoặc đề xuất project governance chỉ vì repo chưa có instruction.
Chỉ làm việc đó khi người dùng yêu cầu riêng.

## Cổng 2: Khi sửa

### Giữ data flow trực tiếp

Người đọc phải theo được:

```text
input -> transformation -> dependency -> side effect -> output hoặc error
```

Ưu tiên lời gọi trực tiếp và cấu trúc quen thuộc của ngôn ngữ/framework. Không
thêm registry, factory, wrapper, event bus, service locator, state machine,
cache, concurrency hoặc generic framework nếu chúng không giải quyết một vấn
đề đã được quan sát hoặc một contract thật.

### Chia trách nhiệm vừa đủ

- Một đơn vị code nên có mục đích gọi tên được bằng ngôn ngữ thông thường.
- Tách code khi responsibility độc lập hoặc data flow đã khó theo dõi.
- Không tách chỉ để đạt line count, tạo helper một-caller không có giá trị hoặc
  phân tán logic vốn cần đọc cùng nhau.
- Ưu tiên function; dùng class khi state, lifecycle hoặc interface thật sự cần.
- File dài không tự động là lỗi. Khó hiểu và trộn responsibility mới là lỗi.

### Chỉ thêm abstraction khi có bằng chứng

Abstraction hợp lý khi có nhiều consumer/implementation thật, provider hoặc
lifecycle boundary rõ ràng, hay code trực tiếp đã gây duplication hoặc vấn đề
được quan sát. Không dùng một con số use case như hard gate.

Trước khi thêm kỹ thuật phức tạp, phải giải thích được:

- vấn đề thật cần giải quyết;
- vì sao cách trực tiếp không đủ;
- lợi ích cụ thể;
- verification nào chứng minh lợi ích;
- vì sao complexity tăng thêm là tương xứng.

Không trả lời được thì giữ giải pháp trực tiếp.

### Giữ thay đổi surgical

- Mỗi thay đổi phải liên hệ được với requirement, root cause hoặc verification.
- Không refactor, format hoặc dọn code lân cận ngoài scope.
- Chỉ xóa import, helper hoặc code khi chính thay đổi hiện tại làm chúng dư.
- Ghi nhận vấn đề ngoài scope để báo lại; không tự mở rộng task.
- Không suy diễn thêm quyền từ task; tuân thủ platform và project governance.

### Xử lý lỗi có mục đích

Chỉ thêm error handling khi requirement, dependency contract hoặc evidence thực
tế cho thấy lỗi có thể xảy ra và caller có phản ứng hữu ích. Không bắt exception
rộng để che lỗi và không thêm retry, fallback, recovery workflow hoặc validator
phòng xa. Provider hoặc dependency failure phải được báo đúng, không thay bằng
kết quả giả rồi coi là thành công.

## Cổng 3: Test và verification

### Test có giá trị

Chỉ tạo hoặc giữ test khi nó bảo vệ behavior cần thiết, một contract quan trọng
hoặc rủi ro thực tế có chi phí tái diễn đáng kể. Không đặt mục tiêu theo số test,
coverage hoặc số file test. Không test implementation detail, abstraction phòng
xa hoặc cơ chế đang bị loại bỏ.

Skill này không bắt buộc TDD. Dùng TDD khi project/task yêu cầu hoặc khi vòng
RED-GREEN-REFACTOR giúp làm rõ pure logic hay tái tạo bug. Methodology cụ thể có
thể do skill chuyên biệt quyết định.

### Phân biệt input unit-level và evidence hệ thống

- Pure deterministic logic được dùng input/model/value tối thiểu, trực tiếp và
  hợp lệ để kiểm tra output, invariant hoặc error contract.
- Input nhỏ như vậy không phải evidence cho database, provider, model, network
  hoặc production integration.
- Không dùng mock, fake, stub dependency, replay, response cũ hoặc artifact cũ
  để tuyên bố integration hoặc completion PASS.
- Khi behavior phụ thuộc integration, phải chạy dependency và production path
  thật trong exact target an toàn được phép.

### Verification theo behavior và blast radius

- Pure logic: focused deterministic checks.
- Database, API, UI, model hoặc service integration: exact real path.
- Shared contract hoặc blast radius rộng: affected checks trước; full suite chỉ
  khi phạm vi thực sự biện minh.
- Test pass không thay live run khi behavior cần integration.
- Chỉ fresh execution của task hiện tại được ghi là observed PASS.

Nếu môi trường hoặc quyền không cho phép chạy, ghi đúng `not verified`,
`partial`, `failed` hoặc `blocked`; không thay bằng evidence giả.

## Cổng 4: Review và handoff

Khi review, ưu tiên requirement và user behavior, correctness, data safety,
scope, compatibility, data flow, complexity và fresh evidence. Dùng hệ severity
và verdict của project nếu có; không chặn vì sở thích cá nhân hoặc best practice
không gắn với tác động thật.

Trước khi bàn giao, đọc exact diff và kiểm tra:

- mọi thay đổi đều thuộc scope;
- data flow không khó hiểu hơn mức cần thiết;
- không có abstraction, fallback, validator hoặc flexibility phòng xa;
- test và verification thực sự bảo vệ behavior đã nêu;
- observed result không bị trộn với expected hoặc prior result.

Bàn giao ngắn: thay đổi gì, đã chạy gì, kết quả quan sát, phần failed/skipped/
partial/not verified và giới hạn còn lại. Không áp report format hoặc checklist
mới nếu project đã có workflow riêng.
