---
name: propose-options
description: Dùng mỗi khi cần User quyết định một việc thật sự của User trong hue_rag — mục tiêu / kết quả muốn có, tiền, xoá dữ liệu, sửa kho, hướng sản phẩm, deploy, model / provider / dữ liệu mới — và khi vấn đề còn mở cần bàn nhiều bước trước khi chốt (mở Phase, thiết kế việc lớn). Bộ phương án gồm cả hướng User nêu lẫn hướng agent tự thêm; mỗi phương án bằng lời thường kèm đổi gì, tốn gì, khi nào sai, chọn khác mất gì; hỏi mỗi lần một câu có đáp án. Cách làm và luật quy trình KHÔNG đi qua skill này — agent tự quyết, nói lý do.
---

# Đề xuất để User chọn

## Vì sao

User nêu KẾT QUẢ muốn có và giới hạn; agent là bên có chuyên môn và chịu trách nhiệm về khuyến nghị. User thường chọn đúng phương án được khuyến nghị, kể cả khi
chưa hiểu hết ("tôi toàn chọn chứ không đọc, đọc không hiểu" — User 21/11/2026) ⇒ một hộp chọn dựng trong khung User đã nêu chỉ là hình thức, và có thể dắt cả hai
bên vào ngõ cụt. Việc của agent: tự vẽ đủ bài toán, đưa cả hướng User chưa nhắc, so bằng phép đếm / phép thử rẻ, rồi chỉ đem tới User phần thật sự của User.

## 1. Có cần hỏi không

Hỏi khi câu trả lời đổi mục tiêu, phạm vi sản phẩm, dữ liệu, tiền, thao tác phá hủy, deploy, đổi model / provider, kiến trúc khó lùi hoặc quyền (bảng quyền
`AGENTS.md`, cột "Hỏi User trước"; `Session_Prompt.md` §4). Mọi thứ khác — chi tiết kỹ thuật, cách làm, luật quy trình của nhóm — agent tự quyết, nói ra lý do, báo sau; **luật quy trình không trình User duyệt**
(nhóm tự giữ, một phiên khác đọc — skill `improve-workflow`). Không hỏi lại và không khuyến nghị trái điều đã chốt (`HIEN_TRANG.md` mục 4; tra đủ trước khi nói "tài liệu không có"); thấy nên đổi thì nói rõ là đề nghị MỞ
LẠI, kèm thông tin mới.

- **Câu User nói hiểu được nhiều cách** ("đồng ý" áp cho một hay nhiều câu; dữ liệu / code / tài liệu): nhắc lại một câu "ý bạn là … đúng không?" trước khi làm.
- **User liệt kê vài ý bằng dấu phẩy hoặc kết bằng "..."** = "nhớ gì nêu đó": tự nghĩ thêm các ý cùng loại, nói rõ ý nào của User, ý nào mình thêm.
- **Hướng kỹ thuật User nêu là một gợi ý để xét:** thấy nó chưa phải hướng tốt nhất thì nói TRƯỚC khi làm, kèm căn cứ; User vẫn chọn hướng đó thì làm theo.
- **Khuyên bỏ / đóng một hướng chưa từng đo:** không có số chất lượng ⇒ đề xuất phép đo rẻ trước, hoặc ghi rõ "chưa đo, lý do bỏ chỉ là vận hành".
- **Trước khi đưa một phương án XÂY**, người đề xuất tự trả lời ngay trong đề xuất: "lỗi / cơ hội này đã thấy ở người dùng thật hoặc lượt đo thật chưa — dẫn số /
  file · không làm thì mất gì". Chưa có số ⇒ làm phép đếm rẻ trước (0 đồng thì tự làm, không chờ ai), ý ghi vào `session_prompt/Y_CHUA_THU.md`; có số rồi mới
  thành phương án xây.
- **Rào, bộ đo, lượt review, luật mới** (không áp cho sàn an toàn / ngoài kho đã có): chỉ khi có sự cố đã thấy thật; chưa có ⇒ không làm và không trình User —
  trừ hậu quả không đảo ngược (lộ dữ liệu lên repo công khai, xoá dữ liệu, mở bộ câu cất riêng).

## 2. Bộ phương án và mỗi phương án

Bộ phương án phải có **cả hướng User nêu lẫn hướng agent tự thêm**, ghi rõ cái nào của ai; "bài toán thật là một cái khác" và "không làm / giữ như cũ" được là
một phương án khi đó là lựa chọn thật. Mỗi phương án:

| Phần | Viết gì |
|---|---|
| **Là gì** | một–hai câu lời thường; thuật ngữ thì kèm nghĩa |
| **Đổi gì** | với User (thấy gì khác, phải làm gì) và với hệ thống (chạy khác thế nào) |
| **Tốn gì** | thời gian, tiền API, độ phức tạp code, bảo trì |
| **Khi nào sai** | điều kiện làm phương án hỏng hoặc không đáng |
| **Chọn khác thì mất gì** | so trên cùng tiêu chí |

## 3. Khuyến nghị

- **Khuyến nghị gần như là quyết định** ⇒ phải qua phản biện trước khi tới User. Nhóm nhiều phiên: phiên điều phối gửi câu + các phương án cho các phiên đang mở,
  mỗi phiên ≤ 10 dòng (chọn gì, phản biện, rủi ro chưa ai nêu), chốt sau tối đa 2 vòng rồi trình **một** khuyến nghị, ghi chỗ nhóm không đồng ý. Làm một mình: nêu
  luôn **phương án NGƯỢC mạnh nhất** cạnh khuyến nghị. Núm nhỏ / chênh người dùng không cảm nhận được: tự quyết, ghi report.
- Nói **lý do**, và **thông tin nào nếu có sẽ làm đảo khuyến nghị**. Tách rõ **đã đo / có trong code** ↔ **ước lượng** ↔ **giả thuyết**. Phản biện cả phương án
  mình khuyến nghị: khi nào nó thất bại.
- Sau khi User chọn: nhắc lại ngắn lựa chọn đó nghĩa là gì, cái giá là gì — bằng một ví dụ đúng bài toán. Agent không đòi User làm việc gì đều đặn (trả bài, nói
  lại lý do theo tuần…): phần giúp User hiểu là công của agent, nằm ở bài viết cho User (`bai_hoc/`).

## 4. Việc lớn / vấn đề còn mở — đề bài lấy từ LỜI User

1. **Chép nguyên văn** điều User đã nói về việc này (từ cuộc trò chuyện / `data/loi_user/<ngày>.md`). Đó là đề bài; không soạn lại thành khung của agent rồi
   xin tick.
2. **Bổ sung phần thiếu**, ghi rõ phần nào là lời User, phần nào agent thêm: ai dùng · kết quả "xong khi" người dùng thấy gì · đo bằng gì · không làm gì.
3. **Chỉ hỏi lại thứ CHỈ User biết** (muốn đạt gì, giới hạn cứng, điều đang lo, sẽ dùng / trình bày sản phẩm thế nào) — mỗi lần một câu, có đáp án để chọn
   (2–4 đáp án) và luôn chừa đường cho User nói ý khác. Điều file hoặc phép đếm trả lời được thì không hỏi.
4. **Agent tự vẽ bài toán trước khi làm:** hai ba hướng kể cả hướng chưa ai nhắc · mốc đơn giản nhất cách mới phải hơn · tiêu chí thành công bằng số, ghi lúc mở
   · phép thử nhỏ trên dữ liệu thật (đếm, xem mẫu, một lời gọi trong trần đã duyệt) và điều nó cho thấy · phương án B nếu thử dưới ngưỡng. Cần thông tin ngoài:
   tra trước (`Session_Prompt.md` §9).
5. Việc rủi ro cao / khó lùi: gom vào **một** tài liệu thiết kế trong `docs/superpowers/specs/` (mục tiêu bằng lời User, quyết định kèm lý do / cái giá, phạm
   vi, tiêu chí nghiệm thu, quyền, rủi ro) cho User duyệt một lần (`WORKFLOW.md` §9.1); XÂY bắt đầu khi User nói "làm đi". Việc còn lại: theo bảng quyền `AGENTS.md` — hàng "tự làm" thì làm, báo sau; hàng "hỏi trước" thì hỏi một câu rồi
   mới xây.
6. Cuối đề xuất của một việc lớn, thêm vài dòng để User **tự nói lại được** trước người chấm: vấn đề là gì (và cái chưa chắc) → đã xem những hướng nào, vì sao
   chọn hướng này → kiểm bằng cách nào. User chưa hiểu ⇒ agent giải thích lại bằng ví dụ khác, không lặp lại câu cũ.

## 5. Cách nói

Rõ, đơn giản, trúng trọng tâm. **Đủ quan trọng hơn ngắn.** Không dùng nhãn "(Recommended)" thay cho lý do.
