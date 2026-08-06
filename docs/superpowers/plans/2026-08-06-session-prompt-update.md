# Session Prompt Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Cập nhật `Session_Prompt.md` thành context/workflow hiện tại, loại bỏ trạng thái foods và lịch sử đã lỗi thời, đồng thời ghi nhận task bằng một entry ngắn trong `Project_Status.md`.

**Architecture:** Giữ `Session_Prompt.md` cho identity, quy tắc, workflow và đường dẫn context. Giữ `Project_Status.md` làm nguồn duy nhất cho số liệu và trạng thái hiện tại. Chỉ chỉnh hai file Markdown trong scope, không thay đổi raw data hoặc curated foods.

**Tech Stack:** Markdown, shell validation và `uv run python`.

## Global Constraints

- Giao tiếp bằng tiếng Việt; nội dung code và tên biến nếu có phải dùng English chuẩn.
- Không sửa raw data.
- Không gọi web hoặc enrich dữ liệu.
- Không revert hoặc xóa thay đổi có sẵn của người dùng.
- Không commit hoặc push.
- Thông tin không được cung cấp không được ghi thành dữ liệu hoặc backlog bắt buộc.
- Trước mọi thay đổi file phải kiểm tra `git status`; sau thay đổi phải chạy validation nhỏ nhất phù hợp.

---

### Task 1: Cập nhật Session Prompt

**Files:**
- Modify: `Session_Prompt.md`
- Reference: `Project_Status.md`
- Reference: `knowledge-base-hue/meta/foods-template.md`
- Reference: `docs/superpowers/specs/2026-08-06-session-prompt-update-design.md`

**Interfaces:**
- Consumes: quy tắc hiện tại trong `Session_Prompt.md`, trạng thái current-state trong `Project_Status.md`, schema foods trong `foods-template.md`.
- Produces: một `Session_Prompt.md` không chứa trạng thái foods stale, danh sách file cũ hoặc lịch sử commit/push cũ.

- [ ] **Step 1: Kiểm tra section trước khi sửa**

Chạy:

```bash
git status --short -- Session_Prompt.md Project_Status.md
rg -n '^#{1,3} |20 file|Commit|commit|Next action|Task hiện tại' Session_Prompt.md
```

Xác định các section cần giữ: identity, mandatory files, quy tắc dữ liệu, raw/source dump paths, pipeline và curated foods standard.

- [ ] **Step 2: Thay workflow bằng workflow đã duyệt**

Giữ workflow read-only đơn giản ở mức xử lý trực tiếp. Với task thay đổi file, behavior hoặc design, ghi thứ tự:

```text
using-superpowers
  -> brainstorming
  -> clarifying questions từng câu một
  -> 2-3 approaches
  -> design approval
  -> implementation
  -> validation
  -> cập nhật Project_Status.md
```

Ghi rõ `rich-elicitation` chỉ dùng khi còn ít nhất hai chiều mơ hồ quan trọng và mỗi chiều có ít nhất ba hướng hợp lý; không sửa file trước khi design được duyệt.

- [ ] **Step 3: Thêm curation, source và worktree policies**

Thêm các quy tắc ngắn sau:

- Kiểm tra duplicate và chọn slug ASCII kebab-case trước khi tạo file.
- Entity cùng tên phải được phân biệt theo địa chỉ hoặc thông tin định danh khác.
- Conflict về giá, giờ hoặc địa chỉ phải giữ qualifier theo nguồn; không tự chọn giá trị.
- Nếu không có source cụ thể, dùng `Nội dung người dùng cung cấp`.
- Không nâng claim marketing thành factual claim mạnh hơn dữ liệu gốc.
- Không ghi field/section không được cung cấp.
- Không revert hoặc xóa thay đổi có sẵn; chỉ sửa đúng scope sau khi kiểm tra `git status`.

- [ ] **Step 4: Rút gọn task hiện tại và xóa stale context**

Thay phần task hiện tại bằng nội dung ngắn trỏ sang `Project_Status.md`, ví dụ:

```markdown
## Task hiện tại gần nhất

Trọng tâm hiện tại là tiếp tục curate `knowledge-base-hue/foods`. Số liệu, tiến độ và next action mới nhất nằm trong `Project_Status.md`.
```

Xóa danh sách 20 file, commit/push history cũ, số liệu foods cũ, next actions cũ và nội dung duplicate với `Project_Status.md`.

- [ ] **Step 5: Kiểm tra diff của Session Prompt**

Chạy:

```bash
git diff --check -- Session_Prompt.md
git diff -- Session_Prompt.md
```

Xác nhận diff chỉ chứa các thay đổi trong spec, không chứa raw data, curated foods hoặc thay đổi ngoài workflow/context.

### Task 2: Ghi nhận task trong Project Status

**Files:**
- Modify: `Project_Status.md`

**Interfaces:**
- Consumes: kết quả Task 1 và thời gian Việt Nam hiện tại.
- Produces: đúng một entry mới ở `## Cập nhật gần nhất`.

- [ ] **Step 1: Thêm entry current update**

Entry phải có:

- Timestamp UTC+7 hiện tại.
- Nội dung `Session_Prompt.md` đã được cập nhật theo spec.
- Các stale list/history đã được xóa.
- Validation đã chạy.
- Next action: tiếp tục đọc `Session_Prompt.md`, `Project_Status.md` và template trước task tiếp theo.

Không sửa các section current-state khác trong `Project_Status.md`.

- [ ] **Step 2: Kiểm tra status entry**

Chạy:

```bash
git diff --check -- Project_Status.md
sed -n '1,80p' Project_Status.md
```

Xác nhận entry mới có timestamp, thay đổi, validation và next action.

### Task 3: Validation cuối

**Files:**
- Test: `Session_Prompt.md`
- Test: `Project_Status.md`

**Interfaces:**
- Consumes: hai file sau Task 1 và Task 2.
- Produces: validation pass và diff giới hạn trong hai file được duyệt.

- [ ] **Step 1: Kiểm tra cấu trúc và stale content**

Chạy:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from pathlib import Path; session=Path('Session_Prompt.md').read_text(); status=Path('Project_Status.md').read_text(); required=['using-superpowers','brainstorming','Project_Status.md','foods-template.md','rich-elicitation']; assert all(item in session for item in required); assert '20 file curated' not in session; assert '3ca366b' not in session; assert '## Update log' not in session; assert '## Cập nhật gần nhất' in status; assert 'Validation đã chạy:' in status; assert 'Next action đề xuất:' in status; print('session prompt validation: pass')"
git diff --check -- Session_Prompt.md Project_Status.md
git status --short -- Session_Prompt.md Project_Status.md
```

Expected result: validation pass, whitespace check không có output lỗi, và chỉ hai file trong scope xuất hiện trong status của task này ngoài các thay đổi có sẵn không liên quan.

- [ ] **Step 2: Review final diff**

Chạy:

```bash
git diff --stat -- Session_Prompt.md Project_Status.md
git diff -- Session_Prompt.md Project_Status.md
```

Đọc diff lần cuối để bảo đảm không có source dump, raw data, curated foods, secrets hoặc nội dung ngoài design đã duyệt.

## Completion Criteria

- `Session_Prompt.md` là context/workflow hiện tại, không còn stale foods list hoặc commit history.
- Workflow approval gate và curation/source/worktree policies được ghi rõ.
- `Project_Status.md` có một entry ngắn cho task và current-state không bị thay đổi ngoài scope.
- Tất cả validation cuối pass.
- Không commit hoặc push.
