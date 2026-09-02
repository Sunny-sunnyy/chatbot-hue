# Bàn giao hiện hành

Target role: reviewer
Authored by: reviewer
Handoff kind: next_design
State: active
Base commit: 2e56273
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none

---

## 1. Objective

Research và thiết kế curated answer-facing content cho:

`knowledge-base-hue/festivals/festival-guides.md`

Guide mới cần học cấu trúc và mức độ hữu ích từ
`knowledge-base-hue/foods/food-guides.md`, nhưng phải được thiết kế theo nhu cầu
thực tế của domain lễ hội thay vì sao chép máy móc schema của foods.

## 2. Inputs và decisions đã có

- 23 entity thuộc `remaining_23_festivals_codex_review.md` đã đạt technical
  review và được commit tại `2e56273`.
- `Festival Huế.md` và `Festival Nghề truyền thống Huế.md` không thay đổi trong
  package vừa đóng.
- `Lễ hội Áo dài Huế.md` còn một delta ngoài scope, được bảo toàn trong
  worktree và chưa nằm trong commit `2e56273`.
- User đề xuất có thể xóa:
  - `knowledge-base-hue/festivals/festival_names_hue_research_inventory.md`;
  - `knowledge-base-hue/festivals/festivals.md`.

## 3. Design gate

Reviewer cần:

1. đọc `food-guides.md`, `festival-guides.md`, hai file được đề xuất xóa,
   festival template và core inventory;
2. kiểm tra mọi consumer/reference của ba file festivals cấp thư mục;
3. xác định exact user questions mà guide phải trả lời và ranh giới với entity;
4. trình bày 2–3 phương án cấu trúc, khuyến nghị một phương án;
5. chỉ viết spec/plan và implementation handoff sau khi user duyệt design.

## 4. Boundaries

- Chưa tạo nội dung guide hoặc xóa file trong design gate.
- Không sửa entity, backend, notebook, index, Qdrant hoặc domain khác.
- Không commit/push nếu chưa có Git authorization mới cho work package này.
- Việc xóa inventory/research file chỉ được đưa vào implementation scope khi
  dependency audit xác nhận không có consumer cần giữ và user duyệt design.

## 5. Next action

Reviewer kiểm tra inputs/dependencies, sau đó trao đổi design của
`festival-guides.md` và retention/deletion policy với user.
