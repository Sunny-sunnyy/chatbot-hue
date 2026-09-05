# Bàn giao hiện hành

Target role: reviewer
Authored by: reviewer
Handoff kind: closure
State: active
Base commit: 45eb7e04b561e7793b025b2fc6dc61040d215a61
Head commit: HEAD
Risk level: medium
Git authorization: commit_and_push
Sub-agent authorization: none
Technical verdict: ready_for_user_confirmation

## Objective và authority

Hoàn tất chỉnh workflow/governance và hai skill theo các quyết định user đã
chốt trong session 2026-09-05. User cho phép Reviewer sửa trực tiếp docs sau khi
thống nhất phương án, không tạo spec/plan riêng cho exact task này. Ngoại lệ
không bỏ điểm duyệt spec/plan cho nhiệm vụ sau.

Scope: bảy file bootstrap/workflow/skill dưới đây, `session_prompt/brainstorming.md`,
ba template report hiện có trong `session_prompt/` và bản lưu điều phối dưới đây.
Không sửa runtime/corpus, benchmark, Qdrant, deploy, thiết kế AWS/hotel recommender;
không đọc secrets hoặc dùng sub-agent. User đã cấp quyền commit và push toàn bộ
thay đổi liên quan governance trong session này, gồm bản dịch tiếng Việt của
coordination skill và bản lưu điều phối. Quyền chỉ áp dụng một lần cho đúng
phạm vi trên; không gồm corpus/Heritage, delta Áo dài hoặc handoff hotel.

## Acceptance và canonical pointers

| Acceptance đã chốt | Nơi kiểm tra |
|---|---|
| Duyệt spec rồi plan riêng; correction trong scope không cần duyệt riêng; xác nhận cuối không mặc định tự chạy lại kỹ thuật | `session_prompt/Session_Prompt.md`, `session_prompt/REVIEWER_WORKFLOW.md` |
| Tự quyết code nội bộ trong scope, ghi chú cần thiết bằng tiếng Việt, giữ nguyên nguyên tắc cốt lõi | `session_prompt/IMPLEMENTER_WORKFLOW.md`, `skills/practical-project-coding/SKILL.md` |
| Finding có requirement/evidence/impact/tiêu chí đóng; phản biện và escalation; minor/out-of-scope không tự mở acceptance; review delta và evidence reuse | `skills/risk-gated-agent-review/SKILL.md`, hai workflow |
| Status giữ tổng quan/workstreams; handoff giữ một task/next action; bảo toàn tiến độ cũ | `session_prompt/Project_Status.md`, file này và bản lưu |
| Brainstorming tự đọc hướng dẫn; prompt ngắn; template nhất quán | `session_prompt/brainstorming.md`, `session_prompt/TEMPLATE_CODEX_REVIEW.md`, `session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`, `session_prompt/TEMPLATE_USER_REPORT.md` |

Giữ nguyên cấm mock/fake/stub, active-data/secret/Git boundaries và ngưỡng dừng
trước correction thứ năm. Không áp line count, số test/coverage hoặc cấm class/
helper máy móc. Contract đã rõ không cần đợi sự cố mới được bảo vệ.

## Evidence và giới hạn

Docs-only Review Contract: đọc exact delta so với trạng thái trước mutation,
kiểm consistency, links, ownership/lifecycle, bảo toàn worktree có sẵn và
`git diff --check`. Kiểm tra ngày 2026-09-05:

- Đã đọc exact delta và đối chiếu các quyết định đã chốt; không phát hiện
  blocker/major trong scope governance. Routing, ownership, approval/correction,
  evidence reuse, minor/out-of-scope và ngưỡng correction thứ năm nhất quán.
- `git diff --check`: đạt. Kiểm tra đường dẫn cục bộ: 52 pointers tồn tại;
  Markdown fences cân bằng, status không còn next action độc lập.
- Đối chiếu bản lưu bằng nội dung: khớp nguyên văn hai file trước mutation mới
  nhất. 28 file thay đổi có sẵn ngoài scope không đổi theo đối chiếu hash; HEAD
  vẫn là base ở trên. Đây là kiểm tra docs/worktree, không phải runtime evidence.
- Không chạy backend/model/API tests hoặc xác minh corpus. Reviewer tự kiểm tra
  sửa đổi governance được user giao trực tiếp; không gọi là independent review
  của implementation do một vai trò khác thực hiện. User chưa xác nhận kết quả cuối.
- Theo yêu cầu tiếp theo của user, toàn bộ hướng dẫn trong coordination skill
  đã được dịch sang tiếng Việt, giữ nguyên tên trường/giá trị kỹ thuật. Commit
  và push là quyền xuất bản thay đổi, không tự chuyển kết quả thành user approved.
- Kiểm tra trước commit bản dịch: tên trường/giá trị kỹ thuật và số mục được
  bảo toàn; đường dẫn và `git diff --cached --check` đạt. File Heritage evidence
  có cập nhật đồng thời sau lần đối chiếu 28 file ở trên; đã cô lập ngoài stage,
  không sửa hoặc đưa thay đổi dữ liệu đó vào commit governance.

Diff từ base còn chứa delta Áo dài và status/handoff có sẵn; không quy chúng
thành thay đổi của task governance. Heritage có corpus/report chưa tracked,
được bảo toàn. Bản lưu
`reports/governance_pre_edit_coordination_snapshot_2026_09_05.md` giữ nguyên
handoff và toàn bộ status trước chỉnh sửa; metadata/chỉ dẫn bên trong
không active. Project Status giữ inventory/evidence/report pointers, không
nâng claim Implementer thành verified.

## Approval Closure Contract và next action

Next role: reviewer. Next action: chờ user xác nhận hoàn tất thay đổi governance
từ tóm tắt kết quả và giới hạn; không bắt user chạy lại kỹ thuật. Không tự tiếp
tục Heritage hoặc thực hiện roadmap dữ liệu bằng handoff này.

Sau khi user xác nhận đúng task này, Reviewer được cập nhật riêng đoạn
Governance trong `Project_Status.md` thành user confirmed, và `State`/next action
trong file này thành completed/chờ nhiệm vụ mới. Kiểm lại exact diff,
`git diff --check`, links và consistency của hai file. Không đổi trạng thái các
phase/workstream khác. Chỉ thay handoff bằng task mới khi user đã giao rõ; không
cần chuyển Implementer chỉ để cập nhật trạng thái. Quyền commit/push lần này
không cấp quyền cho commit closure hoặc nhiệm vụ tương lai.
Dừng phần phụ thuộc nếu acceptance/quyền cần đổi hoặc có concurrent edits
trong các file đang sửa chưa cô lập được; giữ nguyên mọi dữ liệu khác.
