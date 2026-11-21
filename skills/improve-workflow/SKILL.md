---
name: improve-workflow
description: Session A (điều phối) của hue_rag — dùng cuối mỗi ngày làm việc, lúc kết phiên / đóng đợt, khi User phải nhắc agent cùng một điều lần thứ hai hoặc phải tự gợi một hướng nhóm lẽ ra phải nêu, khi một sự cố quy trình làm mất giờ / tiền / dữ liệu, hoặc khi User xin "rút kinh nghiệm", "cải tiến cách làm". Biến sự cố có bằng chứng thành ≤ 3 thay đổi luật / skill / rào bằng máy do NHÓM tự quyết (một phiên khác đọc), gỡ luật cũ, sửa memory sai, ghi sổ cải tiến; chỉ hỏi User khi chạm bảy luật cứng hoặc bảng quyền. Không dùng để đổi mục tiêu, tiêu chí đo, quyền, trần tiền hay code chatbot.
---

# Tự cải tiến cách làm — phiên điều phối

Luật cách làm do nhóm tự giữ và tự gọt (đang thử từ 21/11/2026 — `session_prompt/HIEN_TRANG.md` mục 4; User đổi lại lúc nào cũng được). Làm một mình thì bạn là
người chạy vòng này. Luật gốc (`AGENTS.md`, `session_prompt/`) thắng skill này. **Harness** = mọi thứ định hình cách agent làm: `AGENTS.md`, `session_prompt/`,
`skills/`, `guides/CACH_LAM_VIEC.md`, `.githooks/`, cấu hình + hook của từng công cụ, trí nhớ riêng của agent. Sổ: `session_prompt/SO_CAI_TIEN_CACH_LAM.md`.

## 0. Nhịp — cuối MỖI ngày làm việc, bốn bước (≤ 15 phút); kết phiên / đóng đợt chạy đủ mục 1–5

1. **Đọc các con số** (`session_prompt/HIEN_TRANG.md` mục 4): (a) việc đã báo "xong" bị lật lại · (b) lần User phải nhắc lại một điều đã nói · (c) lần User phải
   tự gợi một hướng nhóm lẽ ra phải nêu · con số sản phẩm đang đuổi. Đếm bằng lệnh trên file sẵn có; số chưa ai soát gắn "chưa soát". Các số này — không phải
   cảm giác — trả lời "cách làm đang tốt lên hay xấu đi".
2. **Hỏi hai chiều:** có làm THỪA không (rào, nghi thức, bước kiểm không bắt lỗi thật) · có NHÌN HẸP không (thước đang đo có đúng thứ người dùng gặp, hướng tốt
   hơn nào chưa ai nêu).
3. **Lỗi nào lặp lần HAI** hôm nay ⇒ xử theo thứ tự nấc ở mục 2 (máy trước, chữ sau). Lỗi gặp lần đầu: sửa việc đó, ghi một dòng bẫy, chưa thành luật.
4. **Tổng chữ luật không tăng:** mỗi luật / bước / rào thêm hôm nay kèm một thứ gỡ ít nhất bằng cỡ đó (luật thừa, bước không bắt lỗi thật, chữ trùng) — trừ luật
   an toàn / dữ liệu.

## 1. Đầu vào — chỉ sự cố có bằng chứng

Đọc: mục bẫy của `sessions/STATUS_*.md`; review có `changes_requested`; lời User sửa agent hoặc gợi hướng (`data/loi_user/`); `git log` (commit sửa commit
trước); sổ (mục `đang thử`). Mỗi sự cố ghi: ngày, ai, chuyện gì, **mất gì** (giờ / USD / dữ liệu / User phải nhắc hay gợi), bằng chứng (`file:dòng`, commit),
**lần thứ mấy**, **phát hiện bằng gì** (tự kiểm / người khác kiểm / User / máy chặn).
Ý về CÁCH LÀM chưa có sự cố (khoá học, bài viết) ⇒ chưa thành luật. Ý về HƯỚNG / sản phẩm ⇒ `session_prompt/Y_CHUA_THU.md` kèm phép đếm rẻ nhất.

## 2. Thay đổi — tối đa 3 mỗi vòng; gỡ trước, rồi máy trước chữ sau

0. **Gỡ / gộp / dời** trước khi thêm: luật trùng, hết hiệu lực, lời dè dặt đã hết lý do, bài học nằm sai chỗ (trong sổ riêng / trí nhớ của một agent ⇒ về skill
   của khâu hoặc tài liệu chung để mọi agent đọc được).
1. **Bỏ hẳn khả năng sai:** đổi thiết kế, để script làm thay bước người / agent hay làm sai (ví dụ script in dòng "đã đẩy lên" thay vì agent gõ tay).
2. **Máy kiểm:** test, hook git, phép kiểm trong script — ưu tiên tầng **mọi agent đều đi qua** (hook git); cấu hình riêng của một công cụ chỉ là lớp thêm. Rào
   mới phải **thử một lần bằng ca cố ý hỏng** trước khi tin; chưa thử ⇒ ghi "chưa thử".
3. **Cuối cùng mới chữ:** sửa câu của luật có sẵn mà vẫn bị làm sai, hoặc thêm 1–3 dòng vào đúng MỘT chỗ — viết thành việc làm được ngay (lệnh, đường dẫn,
   mẫu), nói điều NÊN làm kèm phạm vi và lý do; không kèm chuyện sự cố / mã trong câu luật (chuyện để ở sổ).

Hậu quả **không đảo ngược được** (lộ dữ liệu lên repo công khai, xoá dữ liệu, mở bộ câu cất riêng) ⇒ rào bằng máy ngay lần đầu, không chờ lặp. Rào chỉ một công
cụ chịu ⇒ luôn giữ dòng chữ tương ứng cho agent khác.

Mỗi thay đổi ghi cho phiên đọc: sự cố + lần thứ mấy; sửa ở đâu (file, mục, nguyên văn dòng thêm / gỡ); cái giá (thêm bao nhiêu chữ phải đọc, chặn nhầm gì);
**cách biết có ích = các con số ở mục 0 + sự cố đó có lặp không**; khi nào gỡ.
**Không đi qua skill này:** mục tiêu / phạm vi, tiêu chí đo hay bộ thử của thí nghiệm đang chạy, quyền, trần tiền, code sản phẩm — các việc đó đi đường thường
(`WORKFLOW.md` §3, §9).

## 3. Quyết → thử → giữ / gỡ — người xét KHÁC người đề xuất

- **Nhóm tự quyết:** người đề xuất viết diff trên nhánh riêng, một phiên KHÁC đọc rồi mới gộp (làm một mình: phiên mới ngữ cảnh sạch). **Hỏi User** — một câu,
  theo `propose-options` — chỉ khi thay đổi chạm bảy luật cứng hoặc bảng quyền trong `AGENTS.md`. Gộp = **cho thử**, chưa phải "đúng": ghi sổ `đang thử` (ngày,
  file đổi, theo dõi gì, **ai sẽ xét**). Người đề xuất không tự kết luận luật của mình có hiệu quả; người xét kết luận theo các con số + sự cố có lặp không.
- **Mỗi vòng, trước khi thêm thay đổi mới,** xét lại **mọi** mục `đang thử`: không lặp và luật được dùng ⇒ `đang dùng`; lặp ⇒ lên một nấc ở mục 2; qua 2 phiên
  làm việc thật không ai cần, gây vướng, hoặc **đang chặn việc đáng làm** ⇒ `gỡ`; chưa có dịp dùng ⇒ giữ, ghi lý do. Ghi kết quả xét **thêm vào trước** ghi chú
  cũ ở cột "Xem lại", không ghi đè. Bằng chứng ở đây là quan sát trên mẫu nhỏ: chỉ tin chênh rõ.

## 4. Giữ harness gọn và đúng (mỗi vòng kết phiên)

- `wc -c` các file bắt đọc lúc mở phiên; ghi số vào sổ; sau một vòng tổng số đó không tăng. File agent luôn đọc giữ **dưới 24.000 byte** (có công cụ cắt file
  luật ở cỡ đó mà không báo). Dài thêm ⇒ dời lịch sử ra, để link — **không cắt nội dung còn hiệu lực**.
- Trí nhớ riêng của một công cụ (nạp vào mọi phiên trước cả file luật): mục sai / cũ, lời dè dặt không ghi phạm vi (đối chiếu trang hiện trạng) ⇒ sửa hoặc xoá;
  điều mọi agent cần ⇒ đưa vào tài liệu chung, không để ở đó.
- Một luật ở hai chỗ ⇒ giữ một, chỗ kia trỏ tới.

## 5. Kết vòng

Vòng nào sửa file bắt đọc lúc mở phiên: giao một agent con ngữ cảnh mới chỉ đọc đúng các file đó, báo lại vai / việc / luật cứng nó nắm được và chỗ khó hiểu —
sửa chỗ thiếu trước khi kết vòng (lời giao theo skill `giao-viec-agent-con`).

3–5 dòng lời thường cho User (báo, không xin duyệt): các con số ở mục 0, sự cố nào, đã đổi gì, **đã gỡ gì**, phiên sau theo dõi gì. Một dòng vào
`CURRENT_HANDOFF.md` và `TONG_HOP.md` của ngày. Commit / đẩy theo bảng quyền (`AGENTS.md`).
