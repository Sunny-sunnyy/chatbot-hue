---
name: improve-workflow
description: Session A (điều phối) của hue_rag — dùng cuối mỗi ngày làm việc, lúc kết phiên / đóng đợt, khi User phải nhắc agent cùng một điều lần thứ hai, khi một sự cố quy trình làm mất giờ / tiền / dữ liệu (lỡ chạy paid, commit lẫn file, sửa đè file của session khác, báo cáo không cập nhật, brief sub-agent sai…), hoặc khi User xin "rút kinh nghiệm", "cải tiến cách làm", "tự cải thiện". Biến sự cố có bằng chứng thành ≤ 3 đề xuất sửa luật / skill / rào bằng máy cho User duyệt, gỡ luật cũ, sửa memory sai, ghi sổ cải tiến. Không dùng để đổi mục tiêu, tiêu chí đo, quyền, trần tiền hay code chatbot.
---

# Tự cải tiến cách làm — Session A

Làm một mình thì bạn là người chạy vòng này; "User duyệt" giữ nguyên. Luật gốc (`AGENTS.md`, `session_prompt/Session_Prompt.md`, `WORKFLOW.md`) thắng skill này;
file luật chỉ phiên điều phối sửa. **Harness** = mọi thứ định hình cách agent làm: `AGENTS.md`, `session_prompt/`, `skills/`, `guides/CACH_LAM_VIEC.md`, `.githooks/`,
cấu hình + hook của từng công cụ, trí nhớ riêng của agent. Sổ: `session_prompt/SO_CAI_TIEN_CACH_LAM.md`. Nguồn ý: khoá AI FDE (agent sai thì sửa vào harness, không
chỉ sửa một lần; bên đề xuất không tự chấm; mỗi vòng ít thay đổi).

## 0. Nhịp — cuối MỖI ngày làm việc, ba bước (≤ 15 phút); kết phiên / đóng đợt chạy đủ mục 1–5

1. **Đọc hai con số** của tuần (ghi ở trang hiện trạng): (a) số việc đã báo "xong" bị lật lại · (b) số lần User phải nhắc lại một điều đã nói. Người đếm ghi tên;
   số chưa ai soát gắn "chưa soát". Hai số này — không phải cảm giác — trả lời "cách làm đang tốt lên hay xấu đi".
2. **Lỗi nào lặp lần HAI** hôm nay ⇒ xử theo thứ tự nấc ở mục 2 (máy trước, chữ sau). Lỗi gặp lần đầu: sửa việc đó, ghi một dòng bẫy, **không** thêm luật.
3. **Thêm bao nhiêu gỡ bấy nhiêu:** mỗi luật / bước / rào thêm hôm nay kèm một thứ gỡ (luật thừa, bước không bắt lỗi thật, chữ trùng) — trừ luật an toàn / dữ liệu.

## 1. Đầu vào — chỉ sự cố có bằng chứng

Đọc: mục "Đã học / bẫy gặp" của `sessions/STATUS_*.md`; review có `changes_requested` / điểm lặp; lời User sửa agent trong phiên; `git log` (commit sửa commit
trước); sổ (mục `đang thử`). Mỗi sự cố ghi: ngày, ai, chuyện gì, **mất gì** (giờ / USD / dữ liệu / User phải nhắc), bằng chứng (`file:dòng`, commit),
**lần thứ mấy**, **phát hiện bằng gì** (tự kiểm / người khác kiểm / User / máy chặn) — loại lỗi hay bị bắt muộn thì đề xuất bước kiểm sớm hơn.
Ý hay chưa có sự cố (khoá học, bài viết) ⇒ "ý chờ", chưa thành luật.

## 2. Đề xuất — tối đa 3 mỗi vòng; gỡ trước, rồi máy trước chữ sau

0. **Gỡ / gộp / dời** trước khi thêm: luật trùng, hết hiệu lực, bài học nằm sai chỗ (trong sổ riêng / trí nhớ của một agent ⇒ về skill của khâu hoặc tài liệu
   chung để mọi agent đọc được).
1. **Bỏ hẳn khả năng sai:** đổi thiết kế, để script làm thay bước người / agent hay làm sai (ví dụ script in dòng "đã đẩy lên" thay vì agent gõ tay).
2. **Máy kiểm:** test, hook git, phép kiểm trong script — ưu tiên tầng **mọi agent đều đi qua** (hook git); cấu hình riêng của một công cụ chỉ là lớp thêm.
   Rào mới phải **thử một lần bằng ca cố ý hỏng** (thấy nó chặn) trước khi tin; chưa thử ⇒ ghi "chưa thử".
3. **Cuối cùng mới chữ:** sửa câu của luật có sẵn mà vẫn bị làm sai, hoặc thêm 1–3 dòng vào đúng MỘT chỗ — viết thành việc làm được ngay (lệnh, đường dẫn, mẫu),
   không kèm chuyện sự cố / mã trong câu luật (chuyện để ở sổ).

Hậu quả **không đảo ngược được** (lộ dữ liệu lên repo công khai, xoá dữ liệu, mở bộ câu cất riêng) ⇒ rào bằng máy ngay lần đầu, không chờ lặp. Rào chỉ một công cụ
chịu ⇒ luôn giữ dòng chữ tương ứng cho agent khác.

Mỗi đề xuất viết theo `propose-options` (lời thường): sự cố + lần thứ mấy; sửa ở đâu (file, mục, nguyên văn dòng thêm / gỡ); cái giá (thêm bao nhiêu chữ phải
đọc, chặn nhầm gì); **cách biết có ích = hai con số ở mục 0 + sự cố đó có lặp không**; khi nào gỡ.
**Không đề xuất qua skill này:** mục tiêu / phạm vi, tiêu chí đo hay bộ thử của thí nghiệm đang chạy, quyền, trần tiền, code sản phẩm — các việc đó đi đường
thường (`WORKFLOW.md` §3, §9).

## 3. Duyệt → thử → giữ / gỡ — người xét KHÁC người đề xuất

- User duyệt từng đề xuất; duyệt = **cho thử**, chưa phải "đúng". Áp xong ghi sổ `đang thử`: ngày, file đổi, theo dõi gì, **ai sẽ xét**. Người đề xuất không tự
  kết luận luật của mình có hiệu quả: người xét là một phiên / người khác (làm một mình: phiên mới ngữ cảnh sạch), kết luận theo hai con số + sự cố có lặp không.
- **Mỗi vòng, trước khi thêm đề xuất mới,** xét lại **mọi** mục `đang thử`: không lặp và luật được dùng ⇒ `đang dùng`; lặp ⇒ lên một nấc ở mục 2; qua 2 phiên
  làm việc thật không ai cần, gây vướng, hoặc **đang chặn việc đáng làm** ⇒ đề xuất `gỡ`; chưa có dịp dùng ⇒ giữ, ghi lý do. Ghi kết quả xét **thêm vào trước**
  ghi chú cũ ở cột "Xem lại", không ghi đè.
- Bằng chứng ở đây chỉ là quan sát trên mẫu nhỏ (chỉ tin chênh rõ). Nói thẳng với User; không viết "đã chứng minh".

## 4. Giữ harness gọn và đúng (mỗi vòng kết phiên)

- `wc -lc` các file bắt đọc lúc mở phiên; ghi số vào sổ. File agent luôn đọc giữ **dưới 24.000 byte**. Dài thêm đáng kể ⇒ dời lịch sử ra, để link —
  **không cắt nội dung còn hiệu lực**.
- Trí nhớ riêng của một công cụ: mục sai / cũ (đối chiếu trang hiện trạng) ⇒ sửa hoặc xoá; điều mọi agent cần ⇒ đưa vào tài liệu chung, không để ở đó.
- Một luật ở hai chỗ ⇒ giữ một, chỗ kia trỏ tới.

## 5. Kết vòng

Vòng nào sửa file bắt đọc lúc mở phiên: giao một agent con ngữ cảnh mới chỉ đọc đúng các file đó, báo lại vai / việc / luật cứng nó nắm được và chỗ khó hiểu —
sửa chỗ thiếu trước khi kết vòng (lời giao theo skill `giao-viec-agent-con`).

3–5 dòng lời thường cho User: hai con số, sự cố nào, đã đổi gì, **đã gỡ gì**, phiên sau theo dõi gì. Một dòng vào `CURRENT_HANDOFF.md` và `TONG_HOP.md` của đợt.
Commit / đẩy theo bảng quyền (`AGENTS.md`).
