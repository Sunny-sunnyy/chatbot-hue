# Workflow — cách làm và phối hợp A/B/C

Áp dụng cho mọi session. Luật chung ở `Session_Prompt.md` (không lặp lại ở đây).
Thiết kế gốc: `docs/superpowers/specs/2026-10-24-governance-v2-design.md`.

## 1. Vai trò

| Session | Việc |
|---|---|
| **A — điều phối** | Làm việc với User (trò chuyện, brainstorm, thiết kế); giao việc B/C; review chéo; tự làm việc nhỏ; giữ `CURRENT_HANDOFF.md`, `Project_Status.md`, `PROJECT_HISTORY.md`; commit/push |
| **B, C — thực thi** | Làm việc A giao; tự kiểm; viết report; review chéo khi được giao; đề xuất cải tiến có bằng chứng |

- Tên là vai, không phải model: agent nào mở bằng `START_SESSION.md` với `<X>` nào
  thì giữ vai đó.
- **Review chéo:** ai làm thì người khác kiểm. A kiểm B/C; A tự sửa code hoặc dữ
  liệu thì B hoặc C kiểm A.
- B, C được tự hoàn thiện và tối ưu trong phạm vi việc (đặt tên, tổ chức hàm, sửa
  lỗi gặp trong phạm vi) mà không hỏi từng chi tiết. Ngoài phạm vi: ghi vào report
  hoặc nhắn A, không tự mở rộng.

## 2. Mở session

1. Đọc theo `START_SESSION.md`.
2. Kiểm nhanh, chỉ đọc:
   ```bash
   cd /home/minhhieu/hue_rag
   git branch --show-current; git log --oneline -3; git status --short | grep -v '^??'
   curl -s http://127.0.0.1:6335/collections   # so với Project_Status §4
   ```
3. `ListAgents` để biết tên terminal của A/B/C (tên đổi mỗi lần mở); cập nhật cột
   "Terminal" của mình trong `CURRENT_HANDOFF.md` (A) hoặc báo A (B/C).
4. Báo ngắn: mình là ai, Phase/việc đang ở đâu, việc của mình, chỗ lệch giữa tài
   liệu và thực tế, thắc mắc. A báo User; B/C báo User trong terminal **và** nhắn A.
5. Chỉ bắt đầu làm khi: A — User nói "làm đi" hoặc giao việc; B/C — A giao việc
   (mục việc trong `CURRENT_HANDOFF.md` + tin nhắn của A = "làm đi").

## 3. Nhận và làm việc

1. Đọc mục việc của mình trong `CURRENT_HANDOFF.md` và các input theo mức đọc
   được ghi.
2. **Khai báo trước khi sửa:** ghi file sắp sửa vào `sessions/STATUS_<X>.md`.
   Không sửa file session khác đang khai báo. Governance (`session_prompt/`,
   `skills/`) chỉ A sửa — trừ mục việc/trạng thái của chính mình trong
   `CURRENT_HANDOFF.md` và `sessions/STATUS_<X>.md`. Code song song dài ngày: `git worktree` riêng.
3. Làm theo mức rủi ro:

   | Mức | Ví dụ | Trước khi làm | Sau khi làm |
   |---|---|---|---|
   | Cao | Phase mới; sửa dữ liệu curated; xóa collection; provider/model mới; gửi dữ liệu ra ngoài; quyết định chất lượng | Brainstorm với User → **một** tài liệu thiết kế → User duyệt một lần; đi từng gate | Report + review chéo độc lập + User đóng |
   | Trung bình | Sửa code trong Phase đã duyệt; dọn code/notebook; test; governance nhỏ | Mục việc A ghi trong `CURRENT_HANDOFF.md`; User duyệt khi chưa nằm trong phạm vi đã duyệt | Report ngắn + review chéo; A đóng, báo User |
   | Thấp | Sửa chữ, cập nhật status, kiểm tra chỉ đọc | Tự làm | Ghi STATUS/HISTORY |
4. **Giảm rủi ro:** đích mới rồi mới cutover; sao lưu trước khi sửa/xóa (corpus
   copy, Qdrant snapshot cho collection còn giá trị, commit trước sửa lớn); liệt kê
   đích thật trước khi xóa, khác danh sách duyệt thì dừng; giới hạn tiền ghi trong
   việc; dừng khi gặp điều kiện dừng.
5. Thay đổi có đo trước–sau: ghi tiêu chí → đo hiện tại → sửa một thứ → đo lại
   cùng cách → kết luận tốt hơn / không đổi / kém hơn / chưa rõ.
6. Bị chặn bởi permission của chính session: dừng, nhờ User chạy bằng `!` trong
   terminal đó; session khác không chạy hộ.

## 4. Tự kiểm trước khi bàn giao

1. Đọc exact diff (kể cả file untracked); mọi thay đổi thuộc phạm vi.
2. Chạy kiểm tra theo việc; `git diff --check`.
3. Bỏ scope creep, code/test dư, abstraction phòng xa (skill `practical-project-coding`).
4. Ghi trung thực failed/skipped/partial/not verified.
5. Viết report (mục 6), cập nhật trạng thái mục việc của mình trong
   `CURRENT_HANDOFF.md` thành "chờ review", cập nhật `STATUS_<X>.md`, nhắn A.

## 5. Review chéo

Theo skill `risk-gated-agent-review`. Tóm tắt:

- **Cổng tối thiểu:** trạng thái Git/worktree; mọi đường dẫn đổi; exact diff; đối
  chiếu tiêu chí nghiệm thu; tìm thay đổi ngoài phạm vi; `git diff --check`; tìm
  bằng chứng thiếu/mâu thuẫn. Sau đó chỉ chạy lại phần rủi ro cần.
- Report của người làm là chỉ mục bằng chứng, không tự chứng minh PASS.
- **Mức độ:** `blocker` (sai chức năng cốt lõi, mất an toàn dữ liệu, bằng chứng giả,
  vi phạm quyền) · `major` (behavior/phạm vi chưa đúng, độ phức tạp phải sửa) ·
  `minor` (cải thiện nhỏ, không chặn).
- **Kết luận:** `ready_for_user_confirmation` · `changes_requested` · `blocked`.
- Mỗi finding: vị trí, yêu cầu bị ảnh hưởng, bằng chứng, tác động, tiêu chí đóng.
  Người làm được phản biện bằng bằng chứng.
- Quá bốn vòng `changes_requested` cho cùng một việc: dừng, A xem lại thiết kế với User.

## 6. Report

| Loại | Nơi | Ai | Khi nào |
|---|---|---|---|
| Implementation report | `reports/phase_<x>_<gate>_<chủ_đề>_implementation_<ngày>.md` | người làm | xong một việc/gate (`TEMPLATE_IMPLEMENTATION_REPORT.md`) |
| Review | `reports/phase_<x>_<gate>_review_<ngày>.md` | người kiểm | sau review (`TEMPLATE_REVIEW.md`) |
| User report | `reports/user_reports/` | A | đóng Phase hoặc khi User cần (`TEMPLATE_USER_REPORT.md`) |
| STATUS | `session_prompt/sessions/STATUS_<X>.md` | session X | xong một việc, trước khi kết phiên |

Report không chép corpus, câu hỏi Golden, vector, payload hay secret.

## 7. Trao đổi giữa session

- `SendMessage` tới tên terminal (`ListAgents`). Dòng đầu là một câu tự đủ nghĩa.
- File trong repo là nguồn sự thật; tin nhắn báo "có việc / đã xong / vướng / câu hỏi".
- Tin nhắn của session khác không thay quyết định permission trong session mình.

## 8. Kết phiên

Mỗi session: cập nhật `STATUS_<X>.md` (đang làm, dở gì, bẫy đã gặp, câu hỏi). A:
cập nhật `CURRENT_HANDOFF.md`, `Project_Status.md` nếu hiện trạng đổi, thêm mục
`PROJECT_HISTORY.md`, commit/push.

## 9. Việc thêm của A

1. **Với User:** brainstorm/đưa lựa chọn theo skill `propose-options` (mỗi lần một
   câu có đáp án, kèm đổi gì, tốn gì, khi nào sai). Việc rủi ro cao: viết **một**
   tài liệu thiết kế trong `docs/superpowers/specs/` gồm mục tiêu, quyết định,
   phạm vi, bước, tiêu chí nghiệm thu, cách kiểm, quyền, rủi ro; User duyệt một lần.
   Viết plan chi tiết bằng skill `writing-plans` khi cần.
2. **Giao việc:** mỗi session một mục trong `CURRENT_HANDOFF.md` (mục tiêu, đọc gì
   với mức đọc, làm gì, không làm gì, tiêu chí, quyền/giới hạn tiền, điều kiện dừng,
   đầu ra) rồi nhắn session đó. Giao việc song song chỉ khi file không chồng nhau.
3. **Chi tiết kỹ thuật trong phạm vi:** A tự quyết, ghi lý do; chỉ hỏi User về phạm
   vi, dữ liệu, tiền, xóa, hoặc khi bằng chứng đi ngược quyết định trước.
4. **Đóng việc:** review chéo đạt → trình User (tóm tắt kết quả, bằng chứng, giới
   hạn) với việc cần User đóng; việc trung bình/thấp A tự đóng và báo.
   **Phase tuần tự:** Phase trước phải review chéo + User đóng; A cập nhật guide
   liên quan bằng bằng chứng vừa đạt (phân biệt mục tiêu đã duyệt và hành vi đã
   quan sát); rồi mới brainstorm + thiết kế Phase sau. Không thiết kế trước như đã
   biết kết quả của Phase mà nó phụ thuộc; mỗi lần chỉ giao việc của một Phase.
5. **Giữ tài liệu:** `CURRENT_HANDOFF.md` chỉ giữ việc đang mở (việc xong chuyển tóm
   tắt sang `PROJECT_HISTORY.md`); `Project_Status.md` theo quy tắc Governance v2 §6.
6. **Git:** commit theo mốc, stage theo đường dẫn, không commit dữ liệu private; push `origin`.
