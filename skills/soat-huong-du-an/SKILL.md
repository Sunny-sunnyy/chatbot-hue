---
name: soat-huong-du-an
description: Soát HƯỚNG của một dự án có một người chủ + coding agent — có đang đi tới đích của người chủ không, thước đang đo có đúng thứ người dùng gặp không, còn hướng nào chưa ai nêu. Dùng khi mở dự án / Phase mới · tới một mốc · ba lần thử liền ra âm · người chủ nói "chưa tới đâu" hoặc phải tự gợi hướng · phần lớn commit gần đây không chạm sản phẩm · trước một việc xây lớn. Đầu ra — MỘT trang cho người chủ (đang ở đâu bằng số, các hướng kèm phép đếm rẻ nhất, việc cần người chủ quyết). Soát CÁCH LÀM của nhóm thì dùng improve-workflow.
---

# Soát hướng dự án

**Vì sao.** Agent giỏi tối ưu thứ thước đang đo và làm đúng việc được giao; hai việc đó không trả lời "đây có phải bài toán đúng không". Người chủ thường chỉ
nêu phần mình biết. Lỗi "không nhìn ra hướng" không để lại sự cố nào để đếm, nên vòng cải tiến theo sự cố không bao giờ thấy nó.

**Cỡ.** Bản nhanh (15–30 phút, 0 đồng): mục 1–3 trên dữ liệu đã có. Bản đủ (ở mốc, hoặc khi người chủ nói "chưa tới đâu"): thêm mục 4–6. Một phiên làm, một
phiên khác đọc. Trong lúc soát không xây gì.

## 1. Đích — bằng LỜI người chủ

Chép nguyên văn: sản phẩm sẽ được dùng / được chấm thế nào · ai dùng · "xong" là gì · người chủ phải tự làm, tự giải thích những gì. Thiếu thì hỏi — mỗi lần
một câu, chỉ thứ CHỈ người chủ biết; không soạn lại thành khung của agent. Dấu hiệu chưa có đích: không ai nói được trong một câu "ngày sản phẩm được dùng /
được chấm, chuyện gì diễn ra".

## 2. Một con số sát đích — và thước có đo đúng không

- Chọn MỘT con số sản phẩm gần đích nhất (ví dụ: bao nhiêu phiên người dùng làm xong việc họ đến để làm), ghi giá trị hôm nay.
- Thước đang dùng đo thứ người dùng GẶP (nhiều lượt, câu tự nhiên, việc phổ thông) hay thứ DỄ ĐO (một lượt, câu do nhóm đặt)? Tín hiệu thước lệch: người chủ
  tự thử thấy lỗi mà thước không thấy · số trên thước tăng mà người chủ vẫn thấy chưa tới đâu · câu đo do chính người viết code đặt.

## 3. Bảng lỗi theo NGUYÊN NHÂN, từ dữ liệu đã có — trước khi nghĩ ý mới

Gom mọi lượt hỏng đã ghi (log, lượt thử, góp ý của người chủ) vào nhiều nhất sáu nhóm nguyên nhân, không phải triệu chứng; mỗi nhóm: số lượt · một ví dụ · sửa
ở lớp nào. Nhóm lớn nhất chưa ai làm là ứng viên số một.

## 4. Đổi chỗ đứng nhìn — ít nhất một chỗ khác với thước đang dùng

Người chủ tự dùng 20 phút · người dùng do model đóng vai (có vai, có mục tiêu, hỏi nhiều lượt) · model khác hãng đọc · lịch sử dự án (đếm: lần người chủ phải
gợi hướng, chuỗi thử ra âm, tỉ lệ commit chạm sản phẩm) · nguồn ngoài (người khác giải bài này thế nào; lựa chọn NỀN — model, thư viện, kiến trúc — đã được so
trước khi xây các lớp bù cho nó chưa). Ghi mỗi chỗ đứng cho thấy điều gì thước cũ không thấy. Ba lần thử liền ra âm quanh cùng một mốc ⇒ ngừng tinh chỉnh,
hỏi "nút thắt có nằm ở chỗ khác không".

## 5. Lọc ý — hai trục, đếm trước

- **Hai trục.** BÀI TOÁN (ai dùng, đo gì, hướng khác, nền khác) ↔ KIỂM SOÁT (rào, nghi thức, luật, sổ, vòng review). Câu thử: ý này đổi thứ người dùng THẤY,
  thứ ta BIẾT về người dùng, hay thứ người chủ HIỂU để tự giải thích? Không cái nào ⇒ là kiểm soát ⇒ chỉ làm khi đã có sự cố thật. Làm quá tay và nhìn hẹp
  thường đi cùng nhau: giờ bỏ vào rào là giờ không nhìn người dùng.
- **Đếm trước khi XÂY và trước khi TRÌNH.** Mỗi ý kèm phép đếm / thử RẺ NHẤT cho biết nó đúng hay sai; đếm được trên dữ liệu có sẵn thì làm ngay. Ý chưa có số
  ⇒ vào danh sách ý chưa thử, chưa lên trang trình — sự chú ý của người chủ cũng là chi phí.
- **Điều đã chốt** chỉ nêu lại MỘT lần, khi có số mới sau ngày chốt, nói rõ là đề nghị mở lại.

## 6. Đầu ra — một trang, lời thường

1. Đích (nguyên văn người chủ).
2. Đang ở đâu: con số ở mục 2 + ba nhóm lỗi lớn nhất.
3. Nhiều nhất bốn hướng, kể cả hướng người chủ chưa nêu, ghi rõ ý của ai; mỗi hướng: người dùng thấy gì khác · số đã đếm · tốn gì · khi nào sai.
4. Việc cần người chủ quyết — chỉ thứ thuộc quyền người chủ (mục tiêu, tiền, dữ liệu, hướng sản phẩm, đưa ra dùng), mỗi lần một câu; phần còn lại nhóm tự
   quyết, báo sau.
5. "Nếu là chủ dự án, tôi làm khác gì" — nhiều nhất ba dòng, mỗi dòng kèm bằng chứng nào sẽ làm tôi đổi ý.

Không sinh việc đều đặn cho người chủ, không sinh luật / sổ / bước kiểm mới, không lật điều đã chốt: đầu ra chỉ là hướng và phép đếm.

## Giới hạn

- Nhiều phiên cùng một model đồng ý với nhau là bằng chứng yếu (chung điểm mù); thông tin KHÁC nhau đáng tin hơn số phiếu.
- Người dùng do model đóng vai có thể dễ tính hơn người thật: dùng để LỘ lớp lỗi, không thay người thật thử [hướng cần dè chừng; arXiv 2603.11245 và
  2601.17087 nêu cùng chiều — mới có một phiên đọc phần tóm tắt, người viết chưa mở].
- Bảng phân loại do một người làm dễ khớp giả thuyết của chính người đó ⇒ bảng dùng để quyết thì nhờ người khác phân loại mù.
- Rút từ MỘT buổi ở MỘT dự án (21/11/2026); chưa chạy ở dự án thứ hai.

## Ở dự án này (đổi khối này khi chép sang dự án khác)

Đích và điều đã chốt: `session_prompt/HIEN_TRANG.md` mục 4 · lời chủ dự án nguyên văn: `data/loi_user/` (riêng tư) · ý chưa thử: `session_prompt/Y_CHUA_THU.md`
· quyền của chủ dự án: bảng trong `AGENTS.md`.
