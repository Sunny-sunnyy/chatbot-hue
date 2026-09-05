# Codex Review: Phase <id> <name>

Decision: ready_for_user_confirmation / changes_requested / blocked
Reviewer: Codex
Date:
Canonical guide:
Implementation report:

## 1. Phạm vi đã review

Nêu phần implementation, source, notebook và evidence thực sự đã đọc/chạy.

## 2. Findings

Dùng severity:

- `blocker`: sai chức năng, mất an toàn dữ liệu, fake evidence hoặc vi phạm
  hard boundary;
- `major`: hành vi cần thiết chưa đúng, scope sai hoặc over-engineering phải
  sửa;
- `minor`: cải thiện nhỏ không chặn chức năng thật.

Nếu không có blocker hoặc major, ghi rõ. Reviewer phải yêu cầu bỏ kỹ thuật khó
hiểu hoặc phức tạp hơn nhu cầu thật.

Mỗi finding: vị trí, requirement, evidence, tác động, tiêu chí đóng. Gom findings
đã phát hiện; correction review nêu delta/ảnh hưởng và lý do finding mới. Ghi
phản biện và quyết định của Reviewer. Áp dụng minor/out-of-scope và xử lý bất
đồng theo `skills/risk-gated-agent-review/SKILL.md`.

## 3. Cách Reviewer chạy lại thật

Ghi exact commands/notebook và real data, database, model, provider, profile đã
dùng. Không chép expected command chưa chạy và không expose secrets.

## 4. Kết quả quan sát

Ghi fresh observed results, ý nghĩa của chúng và mọi failed/skipped/partial
outcome. Không suy diễn PASS từ report của Implementer, mock/fake hoặc output cũ.

Evidence reuse hợp lệ ghi riêng nguồn và lý do phần đó không bị delta ảnh
hưởng; không gọi là fresh. Docs-only ghi kiểm tra tài liệu, không bịa live run.

## 5. Giới hạn hoặc phần chưa chạy

Nêu điều Reviewer chưa kiểm tra được và ảnh hưởng đến decision. Nếu không có,
ghi `Không có giới hạn review đã biết trong phạm vi này.`

## 6. Decision và bước tiếp theo

Với `ready_for_user_confirmation`:

- nêu kết quả, evidence, giới hạn và user report; notebook chỉ khi thuộc scope;
- user không phải chạy lại kỹ thuật trừ phần acceptance yêu cầu rõ;
- ghi Approval Closure Contract ngay tại đây hoặc trong current handoff;
- guide giữ `under_review` đến khi user xác nhận;
- phase tiếp theo vẫn đóng.

Với `changes_requested` hoặc `blocked`:

- nêu exact correction hoặc điều kiện cần thay đổi;
- nếu đây là lần thứ 4, kích hoạt complexity reset trước vòng sửa thứ 5.

Reviewer không sửa runtime và không commit/push nếu user chưa yêu cầu riêng.
