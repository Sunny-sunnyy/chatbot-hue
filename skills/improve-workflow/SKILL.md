---
name: improve-workflow
description: Tự cải tiến CÁCH LÀM của agent (một agent hay nhiều phiên) — dùng cuối mỗi ngày làm việc, lúc kết phiên / đóng đợt, khi User phải nhắc một điều lần thứ hai hoặc phải tự gợi một hướng agent lẽ ra phải nêu, khi một sự cố quy trình làm mất giờ / tiền / dữ liệu, hoặc khi User xin "rút kinh nghiệm", "cải tiến cách làm". Biến sự cố có bằng chứng thành ≤ 3 thay đổi luật / skill / rào bằng máy do agent tự quyết (một phiên khác đọc), gỡ luật cũ, sửa trí nhớ sai; Không TỰ đổi mục tiêu, tiêu chí đo, luật cứng, quyền, trần tiền hay code sản phẩm — thấy cần đổi thì nêu cho User quyết.
---

# Tự cải tiến cách làm

Chép sang dự án khác chỉ viết lại khối **"Ở dự án này"** cuối file — tên file của mọi thứ nhắc trong thân tra ở đó. Mặc định: luật về
CÁCH LÀM do agent tự giữ và tự gọt; User giữ mục tiêu, luật cứng, bảng quyền. Người chạy: phiên điều phối; làm một mình thì chính bạn, "phiên khác" = phiên
mới ngữ cảnh sạch. File luật của dự án thắng skill này. **Harness** = file luật, skill, hook git, cấu hình từng công cụ, trí nhớ riêng
của agent.

## 0. Nhịp — cuối MỖI ngày làm việc, bốn bước; kết phiên / đóng đợt chạy đủ mục 1–5

1. **Đọc các con số:** (a) việc đã báo "xong" bị lật lại · (b) lần User phải nhắc lại · (c) lần User phải tự gợi một hướng agent lẽ ra phải nêu ·
   con số sản phẩm đang đuổi. Đếm bằng lệnh trên file sẵn có; số chưa ai soát gắn "chưa soát". Các số này, không phải cảm giác, cho biết cách làm tốt lên hay xấu đi.
2. **Hỏi hai chiều:** có làm THỪA không (rào, nghi thức, bước kiểm không bắt lỗi thật) · có NHÌN HẸP không (thước đang đo có đúng thứ người dùng gặp, hướng tốt
   hơn nào chưa ai nêu).
3. **Lỗi lặp lần HAI** hôm nay ⇒ xử theo nấc ở mục 2 (máy trước, chữ sau). Lỗi gặp lần đầu: sửa việc đó, ghi một dòng bẫy, chưa thành luật.
4. **Tổng chữ luật không tăng:** mỗi luật / bước / rào thêm hôm nay kèm một thứ gỡ ít nhất bằng cỡ đó — trừ luật an toàn / dữ liệu.

## 1. Đầu vào — chỉ sự cố có bằng chứng

Đọc: mục bẫy trong sổ riêng của các phiên; review có yêu cầu sửa; lời User sửa agent hoặc gợi hướng; `git log` (commit sửa commit trước); sổ cải tiến
(mục `đang thử`). Mỗi sự cố ghi: ngày, ai, chuyện gì, **mất gì** (giờ / tiền / dữ liệu / User phải nhắc hay gợi), bằng chứng (`file:dòng`, commit),
**lần thứ mấy**, **phát hiện bằng gì** (tự kiểm / người khác kiểm / User / máy chặn).
Ý về CÁCH LÀM chưa có sự cố ⇒ chưa thành luật. Ý về HƯỚNG / sản phẩm ⇒ danh sách ý chưa thử, kèm phép đếm rẻ nhất.

## 2. Thay đổi — tối đa 3 mỗi vòng; gỡ trước, rồi máy trước chữ sau

0. **Gỡ / gộp / dời** trước khi thêm: luật trùng, hết hiệu lực, lời dè dặt đã hết lý do, bài học nằm sai chỗ (sổ riêng / trí nhớ của một agent ⇒ về tài liệu
   chung để mọi agent đọc được).
1. **Bỏ hẳn khả năng sai:** đổi thiết kế, để script làm thay bước người / agent hay làm sai.
2. **Máy kiểm:** test, hook git, phép kiểm trong script — ưu tiên tầng **mọi agent đều đi qua** (hook git); cấu hình riêng của một công cụ chỉ là lớp thêm. Rào
   mới phải **thử một lần bằng ca cố ý hỏng** trước khi tin; chưa thử ⇒ ghi "chưa thử".
3. **Cuối cùng mới chữ:** sửa câu của luật có sẵn mà vẫn bị làm sai, hoặc thêm 1–3 dòng vào đúng MỘT chỗ — viết thành việc làm được ngay, nói điều NÊN làm kèm phạm vi và lý do; không kèm chuyện sự cố / mã trong câu luật (chuyện để ở sổ cải tiến).

Hậu quả **không đảo ngược được** (lộ dữ liệu lên repo công khai, xoá dữ liệu, mở dữ liệu cất riêng) ⇒ rào bằng máy ngay lần đầu, không chờ lặp. Rào chỉ một công
cụ chịu ⇒ luôn giữ dòng chữ tương ứng cho agent khác.

Mỗi thay đổi ghi cho phiên đọc: sự cố + lần thứ mấy; sửa ở đâu (nguyên văn dòng thêm / gỡ); cái giá (thêm bao nhiêu chữ, chặn nhầm gì); **cách biết có ích =
các con số ở mục 0 + sự cố đó có lặp không**; khi nào gỡ. **Skill này không tự đổi:** mục tiêu / phạm vi, tiêu chí đo hay bộ thử của thí nghiệm đang chạy, luật
cứng, quyền, trần tiền, code sản phẩm — thấy cần đổi thì nêu cho User quyết.

## 3. Quyết → thử → giữ / gỡ — người xét KHÁC người đề xuất

- **Agent tự quyết luật cách làm:** phiên nào cũng đề xuất được; người đề xuất viết diff trên nhánh riêng, một phiên KHÁC người viết đọc; ai gộp theo luật
  của dự án. Thay đổi chạm luật cứng hoặc bảng quyền, hoặc gỡ / đảo một câu ghi là lựa chọn của chính User ⇒ **hỏi User** một câu, có đáp án kèm hệ quả. Gộp = **cho thử**: ghi sổ `đang thử` (ngày, file đổi,
  theo dõi gì, **ai sẽ xét**). Người đề xuất không tự kết luận luật của mình có hiệu quả; người xét kết luận theo các con số + sự cố có lặp không.
- **Mỗi vòng, trước khi thêm thay đổi mới,** xét lại **mọi** mục `đang thử`: không lặp và luật được dùng ⇒ `đang dùng`; lặp ⇒ lên một nấc ở mục 2; qua 2 phiên
  làm việc thật không ai cần, gây vướng, hoặc **đang chặn việc đáng làm** ⇒ `gỡ`; chưa có dịp dùng ⇒ giữ, ghi lý do. Ghi kết quả xét **thêm vào trước** ghi chú
  cũ, không ghi đè. Bằng chứng ở đây là quan sát trên mẫu nhỏ: chỉ tin chênh rõ.

## 4. Giữ harness gọn và đúng (mỗi vòng kết phiên)

- `wc -c` các file bắt đọc lúc mở phiên; ghi số vào sổ; sau một vòng tổng đó không tăng (trừ luật an toàn / dữ liệu). File agent luôn đọc giữ **dưới 24.000 byte** (có công cụ cắt file luật
  ở cỡ đó mà không báo). Dài thêm ⇒ dời lịch sử ra, để link — **không cắt nội dung còn hiệu lực**.
- Trí nhớ riêng của một công cụ (nạp trước cả file luật): mục sai / cũ, lời dè dặt không ghi phạm vi ⇒ sửa hoặc xoá; điều mọi agent cần ⇒ đưa vào tài liệu chung.
- Một luật ở hai chỗ ⇒ giữ một, chỗ kia trỏ tới.

## 5. Kết vòng

Vòng nào sửa file bắt đọc lúc mở phiên: giao một agent con ngữ cảnh mới chỉ đọc đúng các file đó, báo lại vai / việc / luật cứng nó nắm được và chỗ khó hiểu —
sửa chỗ thiếu rồi mới kết vòng.

3–5 dòng lời thường cho User (báo, không xin duyệt): các con số ở mục 0, sự cố nào, đã đổi gì, **đã gỡ gì**, phiên sau theo dõi gì. Một dòng vào sổ việc
và tổng hợp ngày.

## Ở dự án này (hue_rag)

File luật, bảy luật cứng, bảng quyền: `AGENTS.md`, `session_prompt/Session_Prompt.md`, `session_prompt/WORKFLOW.md` · trang hiện trạng + các con số:
`session_prompt/HIEN_TRANG.md` mục 4 · sổ cải tiến: `session_prompt/SO_CAI_TIEN_CACH_LAM.md` · ý chưa thử: `session_prompt/Y_CHUA_THU.md` · sổ riêng của phiên:
`session_prompt/sessions/STATUS_<X>.md` · lời User: `data/loi_user/` · sổ việc, tổng hợp ngày: `session_prompt/CURRENT_HANDOFF.md`,
`report_agent/<ngày>/TONG_HOP.md` · skill đi kèm: `propose-options`, `giao-viec-agent-con`.
"Agent tự giữ luật cách làm" đang THỬ ba ngày làm việc từ 21/11/2026 — lúc xét lại và số để xét: `session_prompt/HIEN_TRANG.md` mục 4;
User đổi lại lúc nào cũng được.
