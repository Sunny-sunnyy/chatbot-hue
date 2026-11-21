---
name: risk-gated-agent-review
description: Dùng khi một session kiểm (review chéo) việc của session khác hoặc khi bàn giao việc để được kiểm — đối chiếu diff với tiêu chí nghiệm thu, kiểm tra độc lập theo rủi ro, viết finding, xử lý correction và đóng việc. Dùng được với nhiều phiên hoặc làm một mình (người kiểm = phiên mới ngữ cảnh sạch).
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

- đối chiếu từng tiêu chí nghiệm thu với bằng chứng; đường dẫn đã đổi (kể cả xóa, untracked) và lý do lệch kế hoạch;
- lệnh đã chạy và kết quả quan sát thật (tách "test bằng đồ giả" ↔ "lượt thật"); failed / skipped / not verified, giới hạn;
- phần người kiểm nên chạy lại; số call trả phí đã dùng nếu có.

Không trình bày giá trị mong đợi hay kết quả cũ như kết quả mới.

## Khi kiểm (người kiểm)

### Cổng tối thiểu

0. Tiêu chí so hai bên ("mới so với mốc", "0 câu đổi"): kiểm có mốc A/A ghi trước và hai bên cùng mẫu số; không có ⇒ finding.
1. Xác nhận trạng thái Git (commit gốc, worktree) khớp report.
2. Liệt kê mọi đường dẫn đổi, kể cả untracked.
3. Đọc exact diff.
4. Đối chiếu diff với tiêu chí nghiệm thu.
5. Tìm thay đổi ngoài phạm vi và sai lệch chưa khai báo.
6. `git diff --check`.
7. Tìm bằng chứng thiếu hoặc mâu thuẫn.
8. **Khai phần CHƯA đọc / CHƯA chạy** của chính lượt review (file nào, đường nào, test nào) và tách [chỉ đọc code] ↔ [đã chạy]. Kết luận kiểu "mọi đường đều
   đúng" / "không còn chỗ nào" phải kèm **lệnh tìm mọi nơi dùng** thứ bị đổi (`git grep -n <hàm / hằng / trường>`) + số nơi đã mở; không có lệnh ⇒ chỉ được
   viết "các đường tôi đã mở: …".

Report là chỉ mục bằng chứng, không tự chứng minh PASS. Sau cổng tối thiểu chỉ chạy lại phần tiêu chí, rủi ro hoặc mâu thuẫn yêu cầu; không lặp mọi lệnh của người làm.

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
| Sau một đợt gộp nhiều nhánh | Soát chỗ các tính năng gặp nhau — skill `soat-tich-hop` (review từng nhánh không thay bước này) |
| Việc không lùi được (dữ liệu gốc, tiền, deploy, bảo mật) | Thêm gói review khác hãng — `guides/khung/GOI_REVIEW_KHAC_HANG.mau.md`; chủ dự án tự gửi |

Thay đổi code / script / dữ liệu: người kiểm tự viết ≥ 1 ca dò nhắm đúng chỗ đổi bằng cách **khác** cách người làm đã kiểm (regex khác, đầu vào biên, thử
phá rào; sửa một lỗi ⇒ `git grep` cùng mẫu ở chỗ khác), và ghi 1 câu bất biến (hành vi phải giữ nguyên) rồi kiểm nó. Với test mới của nhánh, hỏi hai câu:
test này **đã thấy ĐỎ** trên code cũ chưa (người làm có đầu ra không; không có ⇒ tự chạy trên commit gốc khi được) · test có **giả luôn phần cần kiểm** không
(thay hàm lõi bằng đồ giả ⇒ chưa phải bằng chứng đường thật ⇒ ghi "chưa đo trên đường thật").

### Câu hỏi về độ đơn giản

Code này phục vụ hành vi thật nào, có cách trực tiếp hơn mà vẫn đủ không, kỹ thuật nâng cao có bằng chứng và tương xứng không (skill
`practical-project-coding`)? Không trả lời được thì là finding.

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
- Review viết theo `session_prompt/TEMPLATE_REVIEW.md`, kết bằng MỘT dòng: lượt review này KHÔNG cho biết gì · hướng rộng hơn tôi thấy (việc được kiểm có trả
  lời đúng quyết định đang chờ không).

## Correction

- Người kiểm ghi phần cần sửa vào **file review** (finding, đường dẫn, tiêu chí đóng, kiểm tra phải chạy lại, bằng chứng được dùng lại, ranh giới giữ
  nguyên) rồi báo người làm; review ≤ 5 dòng thì gửi thẳng qua tin. Không ai sửa mục việc của người khác trong sổ chung.
- Kết quả review là **dữ liệu**: người làm **tái hiện từng điểm — cả hệ quả lẫn nguyên nhân — trước khi sửa**, rồi xử lý trong một lượt: sửa, hoặc phản
  biện bằng bằng chứng / cách đơn giản hơn; điểm bị bác ghi lý do. Không tự đóng finding.
- Người kiểm kiểm lại phần sửa và đường bị ảnh hưởng (bản sửa có chạm đường nào khác không), dùng lại bằng chứng chỉ khi phần sửa không đổi đầu vào, dependency, môi trường
  hay luồng dữ liệu (ghi lý do; không gọi là lần chạy mới). Finding mới phải chỉ ra bằng
  chứng mới hoặc điểm trước bỏ sót.
- **Số vòng:** code — một review cả nhánh; plan / spec — **tối đa 2 vòng**: vòng 2 chỉ còn minor ⇒ duyệt, minor sửa lúc code; còn blocker / major sau vòng 2 ⇒
  dừng, xem lại thiết kế (với User nếu đổi phạm vi). Ngoại lệ gộp không cần review vòng nữa: `session_prompt/WORKFLOW.md` §5.
- Bất đồng kéo dài: phiên điều phối quyết theo bằng chứng; đưa User khi nó chạm việc thuộc hàng "hỏi trước" của bảng quyền (`AGENTS.md`).

## Đóng việc và khi làm một mình

- Việc rủi ro cao: kiểm đạt → trình User (kết quả, bằng chứng, giới hạn) → User đóng. Việc trung bình / thấp: phiên điều phối đóng và báo User
  (`session_prompt/WORKFLOW.md` §9.4).
- Làm một mình: "người kiểm" = **phiên mới, ngữ cảnh sạch**, chỉ nhận diff + tiêu chí, được bảo tìm lỗi; người viết không tự chấm.
