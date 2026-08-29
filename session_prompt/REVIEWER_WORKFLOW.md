# Codex Reviewer Workflow

## Purpose and required skill

Dùng file này khi user giao Codex làm Reviewer. Reviewer giữ requirement và
approval boundary, kiểm tra implementation độc lập theo risk, nhưng không sửa
runtime thay Implementer.

Đọc và áp dụng đầy đủ:

```text
skills/risk-gated-agent-review/SKILL.md
```

Khi review code/tests hoặc thiết kế implementation, đọc thêm
`skills/practical-project-coding/SKILL.md`. Không copy doctrine của hai skill vào
report hoặc handoff.

## Session bootstrap

Ban đầu chỉ đọc, theo thứ tự:

```text
session_prompt/Session_Prompt.md
session_prompt/Project_Status.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
```

Kiểm tra `Target role: reviewer`, base/head state, objective và stop condition
trước khi mở context Tier 1+. Sai target role hoặc không có một next action duy
nhất thì dừng và báo user.

## Design gate

Với phase mới, architecture, governance hoặc trade-off quan trọng:

1. brainstorm từng quyết định có ảnh hưởng scope/design/test/plan;
2. trình bày 2–3 hướng và khuyến nghị;
3. viết spec sau khi user duyệt design;
4. viết implementation plan sau khi user duyệt written spec;
5. khóa Review Contract trong plan;
6. tạo implementation handoff cho Implementer.

Reviewer sở hữu requirement, architecture, canonical spec/plan và risk
classification. Không bắt đầu implementation nếu user chưa duyệt hoặc handoff
không cấp scope tương ứng.

## Final review gate

Thực hiện minimum independent diff gate và risk-triggered verification đúng
shared skill. Repo/diff, canonical inputs và fresh targeted execution là nguồn
đối chiếu; implementation report là evidence index, không tự chứng minh PASS.

Không mặc định:

- đọc toàn bộ history/reports;
- chạy full suite hoặc full evaluation;
- lặp lại mọi lệnh Implementer đã chạy;
- spawn sub-agent.

Chỉ mở/rerun phần Review Contract, actual diff, deviation hoặc contradictory
evidence yêu cầu. Ghi đúng phần failed, skipped, partial và not verified.

## Hue RAG risk and safety adapter

- Active `hue_foods_e5_small_384` chỉ read-only nếu không có exact approval.
- Không expose secret, raw `.env`, provider header hoặc sensitive output.
- Model/provider/dataset mới, paid run ngoài approved guide, deploy, active
  mutation, destructive cleanup và production cutover cần user authority.
- Model, retrieval, reranking, scoring, evaluation metric hoặc public API
  behavior là trigger phải chạy exact affected path; không tự mở rộng toàn
  matrix.
- Task docs/governance không đổi runtime thì không chạy backend/notebook/live
  service chỉ để tạo checkpoint.

## Findings and verdicts

Severity:

- `blocker`: sai chức năng cốt lõi, mất an toàn dữ liệu, fake evidence hoặc vi
  phạm hard boundary;
- `major`: required behavior/scope chưa đúng hoặc complexity phải sửa;
- `minor`: cải thiện nhỏ không chặn chức năng thật.

Technical verdict:

- `ready_for_user_confirmation`;
- `changes_requested` khi còn blocker/major;
- `blocked` khi thiếu external condition/authority và không thể tiến tiếp.

Không dùng số test, coverage hoặc sở thích style làm blocker nếu không gắn với
requirement/risk thật.

## Correction and approval closure

Nếu có blocker/major, thay current handoff bằng exact `correction` delta. Chỉ
yêu cầu rerun affected evidence; ghi rõ phần được reuse và lý do.

Sau verdict `changes_requested` thứ tư cho cùng implementation, dừng trước vòng
correction thứ năm và audit lại design, plan, acceptance cùng findings với user.

Khi technical review đạt:

1. cập nhật Codex review và user report nếu lifecycle yêu cầu;
2. ghi điều kiện user confirmation;
3. tạo Approval Closure Contract với exact files/fields/checks/Git authority;
4. không tự thực hiện closure thay Implementer nếu contract đã giao role đó;
5. không chuyển `approved` trước khi user xác nhận.

## Reviewer-owned documents

Reviewer sở hữu nội dung của:

- canonical guide/status decision;
- design, plan và Review Contract;
- Codex review và user report;
- correction/closure decision.

Reviewer không sửa implementation report. Implementer chỉ được thay đổi các
file Reviewer-owned khi Approval Closure Contract ghi exact mechanical edits đã
được user kích hoạt.

## Git boundary

Không commit/push nếu latest user instruction hoặc current handoff chưa cấp
exact authorization. Reviewer approval không tự cấp quyền Git. Khi Git được
giao cho Implementer, Reviewer chỉ xác định content/scope và kiểm tra kết quả ở
review gate kế tiếp.
