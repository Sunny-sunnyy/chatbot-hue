# User Report Writing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:executing-plans` to implement this plan task by task. Do not use
> subagents unless the user explicitly requests delegation.

**Goal:** Viết lại mẫu, quy trình và hai báo cáo hiện có để người học có thể đọc
trong khoảng năm phút, hiểu kết quả và biết cách xác nhận.

**Architecture:** Báo cáo người dùng dùng một cấu trúc tám mục và chỉ trình bày
thông tin cần cho việc học, tự kiểm tra và xác nhận. Mã trạng thái cùng chi tiết
kỹ thuật tiếp tục nằm trong guide và Codex review; báo cáo người dùng chỉ diễn
giải chúng bằng tiếng Việt.

**Tech Stack:** Markdown, Jupyter Notebook làm bằng chứng người dùng, `rg` và
Git để kiểm tra tài liệu.

## Global Constraints

- Chỉ sửa năm file đã được duyệt trong thiết kế.
- Không sửa Python, notebook, guide, báo cáo kỹ thuật hoặc
  `Project_Status.md`.
- Không gọi mạng, mô hình hoặc dịch vụ ngoài.
- Không đọc hoặc đưa bí mật vào tài liệu.
- Báo cáo người dùng không hiển thị mã trạng thái nội bộ.
- Mỗi báo cáo dùng đúng tám mục đã chốt.
- Notebook là cách tự kiểm tra chính.
- Không commit hoặc push nếu người dùng chưa yêu cầu rõ.
- Không đưa thay đổi có sẵn ngoài phạm vi vào lần sửa này.

---

### Task 1: Thay mẫu báo cáo người dùng

**Files:**

- Modify: `session_prompt/TEMPLATE_USER_REPORT.md`

**Interfaces:**

- Consumes: `docs/superpowers/specs/2026-08-09-user-report-writing-design.md`.
- Produces: cấu trúc bắt buộc cho mọi báo cáo trong `reports/user_reports/`.

- [ ] **Step 1: Kiểm tra file trước khi sửa**

```bash
git status --short
sed -n '1,260p' session_prompt/TEMPLATE_USER_REPORT.md
```

Expected: nhận diện thay đổi có sẵn và không ghi đè phần ngoài yêu cầu.

- [ ] **Step 2: Thay cấu trúc cũ bằng tám mục đã duyệt**

Mẫu phải dùng đúng các tiêu đề:

```markdown
# Báo cáo dành cho người dùng: Giai đoạn <số> - <tên dễ hiểu>

## Trạng thái hiện tại
## Bạn nhận được gì từ giai đoạn này
## Hệ thống hoạt động như thế nào
## Kết quả Codex đã kiểm tra
## Cách bạn tự kiểm tra
## Giới hạn hiện tại
## Bước tiếp theo và cách xác nhận
## Nếu bạn muốn xem chi tiết kỹ thuật
```

Phần trạng thái dùng:

```text
Trạng thái: Đang chờ bạn xác nhận
Cập nhật lúc: DD-MM-YYYY HH:MM
Notebook cần kiểm tra: notebooks/0<giai_đoạn>_<tên>.ipynb
```

Không đưa `Phase status`, `Technical review decision`, `User confirmation`,
`Report path` hoặc mã trạng thái nội bộ vào phần hiển thị.

- [ ] **Step 3: Ghi hướng dẫn ngắn cho từng mục**

Mẫu phải nói rõ thông tin cần ghi, thông tin không chép từ báo cáo kỹ thuật,
cách giải thích số liệu, kết quả notebook cần quan sát và hai câu phản hồi xác
nhận đã duyệt.

- [ ] **Step 4: Thêm quy tắc ngôn ngữ và chín câu tự kiểm tra**

Giữ bảng thay thế từ khó hiểu. Bổ sung quy tắc giải thích thuật ngữ một lần rồi
dùng cách gọi tiếng Việt.

- [ ] **Step 5: Kiểm tra mẫu mới**

```bash
rg -n '^## ' session_prompt/TEMPLATE_USER_REPORT.md
rg -n 'Phase status|Technical review decision|User confirmation|Report path' session_prompt/TEMPLATE_USER_REPORT.md
git diff --check -- session_prompt/TEMPLATE_USER_REPORT.md
```

Expected: đủ tám mục; nếu mã trạng thái xuất hiện thì chỉ nằm trong câu hướng
dẫn “không hiển thị”, không nằm trong mẫu báo cáo; không có lỗi khoảng trắng.

### Task 2: Đồng bộ quy trình Reviewer và hướng dẫn thư mục

**Files:**

- Modify: `session_prompt/REVIEWER_WORKFLOW.md`
- Modify: `reports/user_reports/README.md`

**Interfaces:**

- Consumes: mẫu mới từ Task 1.
- Produces: quy tắc Reviewer và hướng dẫn thư mục thống nhất với mẫu.

- [ ] **Step 1: Đối chiếu nội dung hiện có**

```bash
sed -n '250,340p' session_prompt/REVIEWER_WORKFLOW.md
sed -n '1,240p' reports/user_reports/README.md
```

Expected: xác định mọi đoạn còn yêu cầu mã trạng thái tiếng Anh, cấu trúc dài
hoặc danh sách nhiều ô xác nhận.

- [ ] **Step 2: Cập nhật quy trình Reviewer**

Quy trình phải yêu cầu tám mục, trạng thái tiếng Việt, notebook là cách kiểm
tra chính, không đưa lệnh kỹ thuật dài khi không cần và cập nhật báo cáo thành
bản hiện trạng. Mã trạng thái chính xác vẫn nằm trong guide và Codex review.

Không thay quyền phê duyệt, cập nhật `Project_Status.md`, commit hoặc push.

- [ ] **Step 3: Viết gọn README**

README chỉ giải thích báo cáo dành cho ai, khác báo cáo kỹ thuật thế nào, tám
mục bắt buộc, quy tắc tiếng Việt, vòng đời xác nhận và quyền sở hữu của Codex.

- [ ] **Step 4: Kiểm tra hai tài liệu**

```bash
rg -n 'remediation|canonical|payload|runtime|gate' reports/user_reports/README.md
rg -n 'TEMPLATE_USER_REPORT.md|tám mục|notebook' session_prompt/REVIEWER_WORKFLOW.md reports/user_reports/README.md
git diff --check -- session_prompt/REVIEWER_WORKFLOW.md reports/user_reports/README.md
```

Expected: README không có từ khó hiểu; cả hai file cùng dẫn tới mẫu và không có
lỗi khoảng trắng.

### Task 3: Viết lại báo cáo Giai đoạn 1

**Files:**

- Modify: `reports/user_reports/phase_1_backend_skeleton_user_report.md`

**Interfaces:**

- Consumes: `reports/phase_1_backend_skeleton_codex_review.md`,
  `notebooks/01_backend_foundation.ipynb` và mẫu mới.
- Produces: báo cáo Giai đoạn 1 ngắn, tự đứng độc lập và chờ xác nhận.

- [ ] **Step 1: Đối chiếu bằng chứng**

```bash
sed -n '1,280p' reports/phase_1_backend_skeleton_codex_review.md
sed -n '1,260p' reports/user_reports/phase_1_backend_skeleton_user_report.md
```

Expected: giữ kết quả về 10 gói Python, ba cấu hình tìm kiếm, `ValueError`, nhật
ký và `RetrievedDocument`.

- [ ] **Step 2: Viết lại theo tám mục**

Giải thích `backend` là phần mã xử lý phía sau ở lần đầu. Nói rõ cấu hình sai bị
từ chối là hành vi đúng và người dùng đã chạy notebook. Không đưa câu lệnh kỹ
thuật. Ghi ngắn những việc chưa có: dữ liệu Foods, tìm kiếm, Qdrant và tạo câu
trả lời.

- [ ] **Step 3: Kiểm tra báo cáo**

```bash
rg -n '^## ' reports/user_reports/phase_1_backend_skeleton_user_report.md
rg -n 'Phase status|Technical review decision|User confirmation|pending|confirmed|remediation|canonical|gate|runtime|payload' reports/user_reports/phase_1_backend_skeleton_user_report.md
rg -n '10 gói|dense_only|ValueError|RetrievedDocument' reports/user_reports/phase_1_backend_skeleton_user_report.md
git diff --check -- reports/user_reports/phase_1_backend_skeleton_user_report.md
```

Expected: đúng tám mục; không có mã trạng thái hoặc từ khó; đủ bốn bằng chứng
chính; không có lỗi khoảng trắng.

### Task 4: Viết lại báo cáo Giai đoạn 2

**Files:**

- Modify: `reports/user_reports/phase_2_foods_markdown_chunking_user_report.md`

**Interfaces:**

- Consumes: `reports/phase_2_foods_markdown_chunking_codex_review.md`,
  `notebooks/02_foods_data_and_chunking.ipynb` và mẫu mới.
- Produces: báo cáo Giai đoạn 2 phản ánh kết quả người dùng vừa chạy.

- [ ] **Step 1: Đối chiếu bằng chứng**

```bash
sed -n '1,280p' reports/phase_2_foods_markdown_chunking_codex_review.md
sed -n '1,300p' reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
```

Expected: dùng số mới nhất 91 tệp, 572 đoạn, 0 đoạn thường vượt 400, 8 bảng
vượt 400 và 31 kiểm thử đạt.

- [ ] **Step 2: Viết lại theo tám mục**

Giải thích `chunk` một lần là đoạn dữ liệu nhỏ rồi chỉ dùng “đoạn dữ liệu”.
Giải thích mức 400 ký tự, ngoại lệ bảng và nhãn `Tên quán — địa chỉ`. Ghi rõ
người dùng đã chạy notebook và thấy 572, 0, 8. Không đưa lệnh kỹ thuật hoặc tên
nhóm tiếng Anh không cần thiết. Nêu rõ chưa đánh giá chất lượng tìm kiếm.

- [ ] **Step 3: Kiểm tra báo cáo**

```bash
rg -n '^## ' reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
rg -n 'Phase status|Technical review decision|User confirmation|pending|confirmed|remediation|canonical|gate|runtime|payload' reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
rg -n '91 tệp|572 đoạn|0 đoạn thường|8 bảng|31 kiểm thử' reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
git diff --check -- reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
```

Expected: đúng tám mục; không có mã trạng thái hoặc từ khó; đủ năm bằng chứng;
không có lỗi khoảng trắng.

### Task 5: Kiểm tra chéo toàn bộ phạm vi

**Files:**

- Verify: `session_prompt/TEMPLATE_USER_REPORT.md`
- Verify: `session_prompt/REVIEWER_WORKFLOW.md`
- Verify: `reports/user_reports/README.md`
- Verify: `reports/user_reports/phase_1_backend_skeleton_user_report.md`
- Verify: `reports/user_reports/phase_2_foods_markdown_chunking_user_report.md`

**Interfaces:**

- Consumes: kết quả Task 1 đến Task 4.
- Produces: nhóm tài liệu nhất quán, sẵn sàng để người dùng đọc.

- [ ] **Step 1: Kiểm tra đường dẫn**

```bash
test -f notebooks/01_backend_foundation.ipynb
test -f notebooks/02_foods_data_and_chunking.ipynb
test -f guides/phase_1_backend_skeleton.md
test -f guides/phase_2_foods_markdown_chunking.md
test -f reports/phase_1_backend_skeleton_codex_review.md
test -f reports/phase_2_foods_markdown_chunking_codex_review.md
```

Expected: tất cả lệnh trả mã 0.

- [ ] **Step 2: Tìm mã trạng thái và từ khó hiểu**

```bash
rg -n 'awaiting_user_confirmation|ready_for_user_confirmation|pending|confirmed|changes_requested|remediation|canonical|payload|runtime|gate' reports/user_reports/*.md
```

Expected: không có kết quả.

- [ ] **Step 3: Kiểm tra tám mục và định dạng**

```bash
rg -n '^## ' reports/user_reports/phase_1_backend_skeleton_user_report.md reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
git diff --check
git status --short
```

Expected: mỗi báo cáo có đúng tám mục theo cùng thứ tự; không có lỗi khoảng
trắng; thay đổi của nhiệm vụ này chỉ nằm trong năm file được duyệt.

- [ ] **Step 4: Đọc lại như một người mới học**

Trả lời chín câu hỏi trong tài liệu thiết kế. Nếu một câu trả lời là “không”,
sửa đúng đoạn gây khó hiểu rồi chạy lại Task 5.

Không commit hoặc push. Sau khi hoàn tất, gửi người dùng đường dẫn hai báo cáo,
tóm tắt thay đổi và mời xác nhận nội dung.
