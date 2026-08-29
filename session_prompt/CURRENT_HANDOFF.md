# Bàn giao hiện hành

Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Base commit: b4452dd617757565840622228054b5679eff3713
Head commit: HEAD
Risk level: medium
Git authorization: none

## 1. Mục tiêu và trạng thái kết thúc

Review governance correction khôi phục các hành vi cốt lõi về coding,
implementation, test, debugging, live verification và review của Hue RAG, đồng
thời giữ nguyên kiến trúc điều phối risk-gated. Trạng thái kết thúc là một
correction handoff chính xác hoặc `ready_for_user_confirmation` kèm Approval
Closure Contract. Không bắt đầu Notebook 08b.

## 2. Các quyết định mới nhất của user

- Khôi phục hành vi theo đúng trách nhiệm của từng file, không chép nguyên văn
  các file cũ.
- Giữ `risk-gated-agent-review` cho điều phối và
  `practical-project-coding` cho nền tảng coding dùng chung.
- Đặt chính sách chung của dự án trong `Session_Prompt.md` và cách áp dụng riêng
  của từng role trong hai workflow.
- Đặt trạng thái phase/project hiện hành trong `Project_Status.md`; file này chỉ
  giữ exact task đang active.
- Golden V3 có 45 full cases và smoke subset 10 row deep-equal.
- Executable dense catalog gồm E5-small, Huydang DEk21 và E5-base.
- Codex Reviewer load Superpowers bằng cơ chế native; Gemini Implementer tìm
  skills tại `~/.codex/skills/`.
- Không mặc định dùng sub-agent. Không commit hoặc push.

## 3. Nguồn canonical cần đọc

Đọc đầy đủ:

```text
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
reports/risk_gated_agent_review_implementation_report.md
```

Sau đó kiểm tra exact diff từ base tới worktree và mọi untracked path.

## 4. Phạm vi và ranh giới

Phạm vi implementation:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/Project_Status.md
session_prompt/CURRENT_HANDOFF.md
reports/risk_gated_agent_review_implementation_report.md
```

Spec và plan đã duyệt là lifecycle inputs thuộc Reviewer. Hai project skills là
read-only. Runtime, tests, dependencies, datasets, notebooks, Qdrant, evaluation
artifacts, paid API, active mutation, destructive action, production cutover và
Notebook 08b đều ngoài phạm vi.

## 5. Hợp đồng review

Risk là `medium` vì diff thay đổi hành vi và quyền của agent trong tương lai
nhưng không thay product runtime. Reviewer phải:

1. xác minh base/worktree state và mọi changed/untracked path;
2. đọc toàn bộ governance diff và map vào spec;
3. kiểm tra mỗi rule có một canonical owner và chỉ lặp ngắn khi có chủ đích;
4. chạy `git diff --check`, current-state scans và canonical path checks;
5. replay độc lập mười behavior scenarios trong implementation report;
6. xác nhận runtime/artifact paths và hai project skills không có diff.

Không chạy backend tests, notebooks, models, Qdrant hoặc paid API trừ khi actual
diff cho thấy một undeclared runtime trigger.

## 6. Đối chiếu tiêu chí chấp nhận và bằng chứng

| Yêu cầu | Bằng chứng |
|---|---|
| Shared simplicity/test/debug/live policy | `Session_Prompt.md` |
| Hành vi vận hành của Reviewer | `REVIEWER_WORKFLOW.md` |
| Hành vi vận hành của Implementer | `IMPLEMENTER_WORKFLOW.md` |
| Tương thích với risk-gated | Section 10 của spec và exact workflow diff |
| Current-only project snapshot | `Project_Status.md` |
| Detailed producer evidence | implementation report |
| Không đổi runtime/skills | protected-path diff và status checks |
| Một exact next action | handoff này |

## 7. Các đường dẫn thay đổi và bằng chứng

Các worktree paths dự kiến gồm sáu implementation files ở trên cùng spec và
plan đã được duyệt. `session_prompt_old/` là untracked context không liên quan
và phải được giữ nguyên.

Implementation report ghi fresh word counts, required/obsolete scans,
responsibility mapping, manual scenarios, path checks, protected-path checks và
format results. Reviewer coi các claims đó là evidence index và tự chạy lại các
kiểm tra theo Review Contract.

## 8. Sai lệch và giới hạn

- Codex thực hiện docs correction theo direct user instruction thay vì Gemini.
  Independent review vẫn bắt buộc; handoff này không tuyên bố approval.
- Runtime/live checks được chủ đích bỏ qua vì không có product path thay đổi.
- Checkpoint đã được commit/push theo yêu cầu riêng của user. Git authorization
  hiện là `none`; handoff này không cấp quyền Git tiếp theo cho Reviewer.

## 9. Kế hoạch đóng phê duyệt

Sau technical readiness và user confirmation, closure contract có thể cập nhật
exact lifecycle state và thay file này bằng `next_design` handoff target Reviewer
cho research và brainstorming Notebook 08b. Handoff đó không được authorize 08b
implementation/run, paid API, active Qdrant mutation hoặc production cutover.

## 10. Hành động tiếp theo và điều kiện dừng

Reviewer thực hiện medium-risk documentation review và trả findings theo
severity. Dừng nếu base không hợp lệ, có undeclared changed path, thiếu canonical
input, authority mâu thuẫn hoặc evidence không được hỗ trợ. Không sửa runtime
thay Implementer, bắt đầu Notebook 08b, commit hoặc push.
