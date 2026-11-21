---
name: improve-project
description: Vòng lặp cải tiến chính SẢN PHẨM của một dự án có một người chủ + coding agent — anh em của improve-workflow (skill kia cải tiến CÁCH LÀM của nhóm, skill này cải tiến dự án). Mỗi vòng: đích · một con số · nguyên nhân lỗi · chỗ đứng khác · ≤ hai hướng · đo lại · giữ / gỡ. Dùng khi mở dự án / giai đoạn mới · tới một mốc · ba lần thử liền không vượt nhiễu · người chủ nói "chưa tới đâu" hoặc phải tự gợi hướng · phần lớn commit gần đây không chạm sản phẩm · trước một việc xây lớn. Vòng đủ ra MỘT trang cho người chủ.
---

# Cải tiến dự án theo vòng

Lỗi "không nhìn ra hướng" không để lại sự cố nào để đếm, nên vòng cải tiến cách làm không thấy nó — vòng này dành cho nó.

**Ai chạy, khi nào.** Nhóm tự chạy ở mốc hoặc khi có dấu hiệu ở phần mô tả; không sinh việc đều đặn cho người chủ. Một phiên làm, một phiên
khác đọc (làm một mình: mở phiên mới ngữ cảnh sạch để đọc). Bản nhanh (15–30 phút, 0 đồng): bước 0–3 trên dữ liệu đã có, KHÔNG ra trang
cho người chủ trừ khi lộ ra việc thuộc quyền người chủ. Skill không tự xây: việc xây đi
đường làm việc thường của dự án (quyền, review).

## Một vòng

**0. Mở bằng trang của vòng TRƯỚC** (vòng đầu thì bỏ qua): con số khi đó ↔ bây giờ · hướng nào đã thử · số có nhúc nhích không · dự đoán nào của vòng trước
sai — đó là dữ liệu về chính cách chọn hướng.

**1. Đích — bằng LỜI người chủ.** Chép nguyên văn: sản phẩm sẽ được dùng / được chấm thế nào · ai dùng · "xong" là gì · người chủ phải tự làm, tự giải thích
những gì. Thiếu thì hỏi — mỗi lần một câu, chỉ thứ CHỈ người chủ biết; không soạn lại thành khung của agent. Chưa có đích khi không ai nói được trong một câu
"ngày sản phẩm được dùng / được chấm, chuyện gì diễn ra".

**2. Một con số sát đích — và thước có đo đúng không.** Chọn MỘT con số sản phẩm gần đích nhất (kiểu "bao nhiêu phiên người dùng làm xong việc họ đến để
làm"); ghi giá trị hôm nay và chạy lại y nguyên thì lệch bao nhiêu — một lần chạy chỉ là một mẫu. Thước (= cách đang đo: bộ câu, bộ test, con số theo dõi) đo
thứ người dùng GẶP (nhiều lượt, câu tự nhiên, việc phổ thông) hay thứ DỄ ĐO (một lượt, câu do nhóm đặt)? Tín hiệu thước lệch: người chủ tự thử thấy lỗi mà
thước không thấy · số tăng mà người chủ vẫn thấy chưa tới đâu · câu đo do chính người viết code đặt.

**3. Bảng lỗi theo NGUYÊN NHÂN, từ dữ liệu đã có — trước khi nghĩ ý mới.** Gom mọi lượt hỏng đã ghi (log, lượt thử, góp ý của người chủ) vào nhiều nhất sáu
nhóm nguyên nhân, không phải triệu chứng; mỗi nhóm: số lượt · một ví dụ · sửa ở lớp nào.

**4. Đổi chỗ đứng nhìn — ít nhất một chỗ khác với thước đang dùng.** Người chủ tự dùng 20 phút (khi người chủ muốn — không đòi) · người dùng do model đóng
vai (có vai, có mục tiêu, hỏi nhiều lượt) · model khác hãng đọc · lịch sử dự án (lần người chủ phải gợi hướng, chuỗi thử không vượt nhiễu, tỉ lệ commit chạm
sản phẩm) · nguồn ngoài (người khác giải bài này thế nào; lựa chọn NỀN — model, thư viện, kiến trúc — đã được so trước khi xây các lớp bù cho nó chưa). Chỗ
đứng mới để KIỂM thước, không thay con số của bước 2: con số giữ nguyên qua các vòng để so được.

**5. Lọc ý — hai trục, đếm trước.** BÀI TOÁN (ai dùng, đo gì, hướng khác, nền khác) ↔ KIỂM SOÁT (rào, nghi thức, luật, sổ, vòng review). Câu thử: ý này đổi
thứ người dùng THẤY, thứ ta BIẾT về người dùng, hay thứ người chủ HIỂU để tự giải thích? Không cái nào ⇒ là kiểm soát ⇒ chỉ làm khi đã có sự cố thật. Mỗi ý
kèm phép đếm / thử RẺ NHẤT cho biết nó đúng hay sai; đếm được trên dữ liệu có sẵn thì làm ngay; chưa có số ⇒ ghi vào danh sách ý chưa thử nếu dự án đã có
(chưa có thì để cuối trang), chưa lên trang trình — sự chú ý của người chủ cũng là chi phí. Điều đã chốt chỉ nêu lại MỘT lần, khi có số mới, nói rõ là đề
nghị mở lại.

**6. Trang của vòng — một trang, lời thường, THAY trang vòng trước** (giữ lại mỗi vòng cũ một dòng: ngày · con số · hướng đã thử · kết quả): đích (nguyên
văn) · đang ở đâu (con số + ba nhóm lỗi lớn nhất) · nhiều nhất bốn hướng kể cả hướng người chủ chưa nêu, ghi rõ ý của ai, mỗi hướng: người dùng thấy gì khác,
số đã đếm, tốn gì, khi nào sai, DỰ ĐOÁN con số sẽ đổi bao nhiêu · việc cần người chủ quyết — chỉ thứ thuộc quyền người chủ (mục tiêu, tiền, dữ liệu, hướng
sản phẩm, đưa ra dùng), mỗi lần một câu; phần còn lại nhóm tự quyết, báo sau.

**7. Làm — đo lại — giữ hoặc gỡ.** Nhiều nhất HAI nhóm lỗi / hướng đứng đầu (nhóm chọn, ghi lý do một dòng; thứ thuộc quyền người chủ thì theo bước 6) đi
vào đường làm việc thường, LẦN LƯỢT; đo lại sau TỪNG hướng bằng CÙNG thước, cùng điều kiện, đủ lượt lặp để biết nhiễu (thước nhỏ: luật ba lượt ở `run-experiment` mục 4); không hơn rõ ngoài nhiễu ⇒ gỡ. Ý đã thử thì rút khỏi danh sách ý; kết quả ghi vào trang, kể cả kết quả âm. Giữ riêng một phần của thước (vài vai / câu) không dùng
để tìm lỗi, chỉ để đo lại; các SÀN của dự án (điều không được xảy ra) kiểm cùng lượt đo — phạm sàn thì không giữ dù con số tăng; bản sửa một lỗi an toàn / sai
sự thật đã tái hiện được thì giữ dù con số không nhúc nhích.

**8. Dừng hoặc quay đầu.** Đạt mức người chủ nêu ⇒ dừng, báo. Hai vòng liền con số không nhúc nhích ngoài nhiễu ⇒ KHÔNG tinh chỉnh tiếp: quay về bước 1–2
(đích và thước có đúng không) và bước 4 (nền có đúng không).

**9. Kết vòng — ĐỀ XUẤT sửa chính skill này (diff do một phiên khác đọc, theo đường của `improve-workflow`), và chia ranh.** Một dòng: bước nào của skill vòng này không dùng tới · thiếu bước nào. Bước hai vòng liền không ai dùng ⇒
đề nghị gỡ; skill phải nhỏ dần. Vòng này cho thấy nút thắt nằm ở CÁCH LÀM ⇒
chuyển sang `improve-workflow`; skill kia thấy ý về hướng sản phẩm thì ghi vào danh sách ý chưa thử cho vòng này đọc.

## Giới hạn

- Skill không sinh luật, sổ hay bước kiểm mới, không lật điều đã chốt: nó ra hướng, phép đếm và một trang.
- Nhiều phiên cùng một model đồng ý với nhau là bằng chứng yếu (chung điểm mù); thông tin KHÁC nhau đáng tin hơn số phiếu [kinh nghiệm dự án gốc; nghiên cứu
  nêu cùng chiều chưa ai trong nhóm tự mở].
- Người dùng do model đóng vai có thể dễ tính hơn người thật: dùng để LỘ lớp lỗi, không thay người thật thử [arXiv 2603.11245 và 2601.17087 nêu cùng chiều —
  phiên điều phối mở phần tóm tắt hai bài; đo trên trợ lý dịch vụ khách hàng tiếng Anh ⇒ là hướng, chưa là bằng chứng cho loại sản phẩm khác].
- "Ba lần thử", "hai vòng liền", "nhiều nhất hai hướng" là mốc kinh nghiệm, chưa nguồn nào cho con số. Bảng phân loại do một người làm thì ghi nhãn "một
  người phân loại" khi dùng để quyết.
- Rút từ MỘT buổi ở MỘT dự án (21/11/2026); chưa chạy trọn một vòng nào, chưa chạy ở dự án thứ hai.

## Ở dự án này (đổi khối này khi chép sang dự án khác)

Đích và điều đã chốt: `session_prompt/HIEN_TRANG.md` mục 4 · lời chủ dự án nguyên văn: `data/loi_user/` (riêng tư) · ý chưa thử: `session_prompt/Y_CHUA_THU.md`
· quyền của chủ dự án: bảng trong `AGENTS.md` · trang của vòng: một mục trong `session_prompt/HIEN_TRANG.md` (không lập file mới).
