---
name: risk-gated-agent-review
description: Dùng khi một session kiểm (review chéo) việc của session khác hoặc khi bàn giao việc để được kiểm — đối chiếu diff với tiêu chí nghiệm thu, kiểm tra độc lập theo rủi ro, viết finding, xử lý correction và đóng việc. Áp dụng cho mô hình A điều phối + B/C thực thi của hue_rag.
---

# Review chéo theo rủi ro

## Mục đích

Người kiểm tập trung công sức vào chỗ rủi ro thật; người làm chịu trách nhiệm làm
đủ phạm vi, tự kiểm và đưa bằng chứng. Ai làm thì người khác kiểm. Luật chung
(bằng chứng, quyền, đơn giản) ở `session_prompt/Session_Prompt.md`; cách phối hợp
ở `session_prompt/WORKFLOW.md`.

## Khi bàn giao để được kiểm (người làm)

Report (`session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md`) cần đủ để người kiểm
không phải đoán:

- đối chiếu từng tiêu chí nghiệm thu với bằng chứng;
- đường dẫn đã đổi (kể cả xóa, untracked) và lý do lệch kế hoạch;
- lệnh đã chạy và kết quả quan sát thật;
- failed / skipped / not verified, giới hạn;
- phần người kiểm nên chạy lại;
- số call trả phí đã dùng nếu có.

Không trình bày giá trị mong đợi hay kết quả cũ như kết quả mới.

## Khi kiểm (người kiểm)

### Cổng tối thiểu

1. Xác nhận trạng thái Git (commit gốc, worktree) khớp report.
2. Liệt kê mọi đường dẫn đổi, kể cả untracked.
3. Đọc exact diff.
4. Đối chiếu diff với tiêu chí nghiệm thu.
5. Tìm thay đổi ngoài phạm vi và sai lệch chưa khai báo.
6. `git diff --check`.
7. Tìm bằng chứng thiếu hoặc mâu thuẫn.

Report là chỉ mục bằng chứng, không tự chứng minh PASS. Sau cổng tối thiểu chỉ
chạy lại phần tiêu chí, rủi ro hoặc mâu thuẫn yêu cầu; không lặp mọi lệnh của
người làm.

### Kiểm thêm theo tác động

| Tác động | Người kiểm làm thêm |
|---|---|
| Chỉ tài liệu | Nhất quán, link, trạng thái vòng đời |
| Logic chức năng | Đọc đường bị sửa, chạy kiểm tra nhỏ nhất có ích |
| Dependency/provider | Cách phân giải, nơi dùng, hợp đồng chính thức khi cần |
| Database/tích hợp | Chạy đúng đường thật bị ảnh hưởng trên đích an toàn (chỉ đọc nếu được) |
| Model/retrieval/chấm điểm | Chỉ chạy lại phần bị thay đổi |
| Dữ liệu đang chạy/xóa | Quyền, đích chính xác, trạng thái trước/sau |
| Bảo mật/API công khai | Ranh giới bị ảnh hưởng, hành vi quan sát được |

### Câu hỏi về độ đơn giản

Code này phục vụ hành vi thật nào? Có cách trực tiếp hơn mà vẫn đủ không? Người
đọc theo được data flow không? Kỹ thuật nâng cao giải quyết vấn đề quan sát được
nào, có bằng chứng không, có tương xứng không? Không trả lời được thì là finding.

### Finding và kết luận

- Mức: `blocker` (sai chức năng cốt lõi, mất an toàn dữ liệu, bằng chứng giả, vi
  phạm quyền) · `major` (behavior/phạm vi chưa đúng, độ phức tạp phải sửa) ·
  `minor` (cải thiện nhỏ, không chặn, không mở vòng sửa riêng).
- Mỗi finding: vị trí, yêu cầu bị ảnh hưởng, bằng chứng, tác động, tiêu chí đóng
  quan sát được. Gom mọi finding vào một lượt.
- Kết luận: `ready_for_user_confirmation` · `changes_requested` · `blocked`
  (thiếu điều kiện/quyền bên ngoài).
- Không hạ vấn đề an toàn hay behavior bắt buộc thành minor. Vấn đề ngoài phạm vi
  ghi ngắn, không tự đưa vào correction.
- Review viết theo `session_prompt/TEMPLATE_REVIEW.md`.

## Correction

- Người kiểm ghi phần cần sửa vào mục việc của người làm trong
  `CURRENT_HANDOFF.md`: finding, đường dẫn, tiêu chí đóng, kiểm tra phải chạy
  lại, bằng chứng được dùng lại, ranh giới giữ nguyên.
- Người làm xử lý trong một lượt: sửa, hoặc phản biện bằng bằng chứng / cách đơn
  giản hơn. Không tự đóng finding.
- Người kiểm kiểm lại phần sửa và đường bị ảnh hưởng, dùng lại bằng chứng đủ điều
  kiện. Finding mới phải chỉ ra bằng chứng mới hoặc điểm trước bỏ sót.
- Bất đồng kéo dài: A tổng hợp lựa chọn + khuyến nghị cho User.
- Sau bốn vòng `changes_requested`: dừng, A xem lại thiết kế với User.

## Đóng việc

- Việc rủi ro cao: kiểm đạt → A trình User (kết quả, bằng chứng, giới hạn) → User
  đóng. Việc trung bình/thấp: A đóng và báo User.
- Sau khi đóng: A cập nhật `CURRENT_HANDOFF.md` (bỏ việc đã xong), `Project_Status.md`
  nếu hiện trạng đổi, thêm mục `PROJECT_HISTORY.md`, commit/push.

## Dùng lại bằng chứng

Chỉ khi bằng chứng đã đạt trong cùng chuỗi việc và phần sửa không đổi đầu vào,
dependency, môi trường hay luồng dữ liệu. Ghi lý do; không gọi là lần chạy mới.
