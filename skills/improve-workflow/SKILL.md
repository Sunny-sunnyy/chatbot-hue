---
name: improve-workflow
description: Session A (điều phối) của hue_rag — dùng lúc kết phiên / đóng đợt, khi User phải nhắc agent cùng một điều lần thứ hai, khi một sự cố quy trình làm mất giờ / tiền / dữ liệu (lỡ chạy paid, commit lẫn file, sửa đè file của session khác, báo cáo không cập nhật, brief sub-agent sai…), hoặc khi User xin "rút kinh nghiệm", "cải tiến cách làm", "tự cải thiện". Biến sự cố có bằng chứng thành ≤ 3 đề xuất sửa luật / skill / rào bằng máy cho User duyệt, gỡ luật cũ, sửa memory sai, ghi sổ cải tiến. Không dùng để đổi mục tiêu, tiêu chí đo, quyền, trần tiền hay code chatbot.
---

# Tự cải tiến cách làm — Session A

Nguồn ý: khóa AI FDE (agent sai thì sửa vào harness, không chỉ sửa một lần; bên đề xuất không tự quyết —
người duyệt cho **thử**, bằng chứng quyết **giữ / gỡ**, mỗi vòng ít thay đổi) và cách làm của một dự án khác
của User (ghi chú private `data/external_project_notes/`). **Harness** của hue_rag = `AGENTS.md`, `session_prompt/`,
`skills/`, memory của agent, `.githooks/`, `.claude/settings.json`, `.claude/hooks/`. Luật gốc (`session_prompt/Session_Prompt.md`,
`WORKFLOW.md`) thắng skill này; governance chỉ A sửa, User duyệt qua skill này. Sổ:
`session_prompt/SO_CAI_TIEN_CACH_LAM.md`.

## 1. Đầu vào — chỉ sự cố có bằng chứng

Đọc: mục "Đã học / bẫy gặp" của `sessions/STATUS_*.md`; review có `changes_requested` / finding lặp; lời User
sửa agent trong phiên; memory loại `feedback`; `git log` (commit sửa commit trước); sổ (mục `đang thử`).
Mỗi sự cố ghi: ngày, session, chuyện gì, **mất gì** (giờ / USD / dữ liệu / User phải nhắc), bằng chứng
(file:dòng, commit), **lần thứ mấy**, **phát hiện bằng gì** (tự kiểm / review chéo / User / công cụ chặn) — loại lỗi
hay bị bắt muộn thì đề xuất bước kiểm sớm hơn. Ý hay chưa có sự cố (khóa học, bài viết) ⇒ "ý chờ", chưa thành luật.

## 2. Đề xuất — tối đa 3 mỗi vòng, nấc rẻ trước

1. **Gỡ / gộp / dời**: luật trùng, hết hiệu lực, bài học nằm sai chỗ (trong STATUS / handoff / memory của
   một agent ⇒ về skill của khâu, `WORKFLOW.md` hoặc `Project_Status.md` §8 để mọi agent đọc được).
2. **Sửa câu** của luật có sẵn mà vẫn bị làm sai.
3. **Thêm luật** 1–3 dòng vào đúng một chỗ, kèm "vì sao" (sự cố, ngày); viết thành việc làm được ngay (lệnh, đường
   dẫn, mẫu cụ thể), không viết lời khuyên chung chung.
4. **Rào bằng máy** khi luật bằng chữ bị vi phạm ≥ 2 lần, **hoặc ngay lần đầu nếu hậu quả không đảo ngược
   được** (lộ dữ liệu lên repo public, xóa dữ liệu, mở câu kín). Ưu tiên rào mọi agent đều chịu (hook git
   `.githooks/`, kiểm trong script); quyền + hook Claude Code (`.claude/settings.json`, `.claude/hooks/` — W37) là lớp thêm. Luôn giữ dòng chữ
   tương ứng cho agent không chịu rào đó.

Mỗi đề xuất viết theo `propose-options` (lời thường): sự cố + lần; sửa ở đâu (file, mục, nguyên văn dòng
thêm / gỡ); cái giá (thêm bao nhiêu chữ phải đọc, chặn nhầm gì); **cách biết có ích** (sự cố có lặp không,
agent có làm đúng không); khi nào gỡ.
**Không đề xuất qua skill này:** mục tiêu / phạm vi, tiêu chí đo hay bộ thử của thí nghiệm đang chạy, quyền,
trần tiền, code chatbot — các việc đó đi đường thường (`WORKFLOW.md` §3, §9).

## 3. Duyệt → thử → giữ / gỡ

- User duyệt từng đề xuất; duyệt = **cho thử**, chưa phải "đúng". Áp xong ghi sổ `đang thử`, ngày, file đổi,
  theo dõi gì. Thay đổi governance do A làm vẫn cần người khác kiểm (B/C hoặc sub-agent ngữ cảnh mới).
- **Mỗi vòng, trước khi thêm đề xuất mới,** xét lại **mọi** mục `đang thử` (không chỉ mục mới): không lặp và luật được
  dùng ⇒ `đang dùng`; lặp ⇒ lên một nấc; qua 2 phiên làm việc thật không ai cần, gây vướng, hoặc **đang chặn việc đáng làm**
  ⇒ đề xuất `gỡ`; chưa có dịp dùng ⇒ giữ, ghi lý do. Ghi kết quả xét **thêm vào trước** ghi chú cũ ở cột "Xem lại", không
  ghi đè (W38, theo khung_fde v1 — 31/10: 39 mục `đang thử`, W1–W13 chưa vòng nào xét; khoá AI FDE W2D5·83: luật tự viết có
  thể tự trói tay).
- Bằng chứng ở đây chỉ là quan sát (sự cố lặp hay không). Nói thẳng với User; không viết "đã chứng minh".

## 4. Giữ harness gọn và đúng (mỗi vòng)

- `wc -l` các file `START_SESSION.md` bắt đọc; ghi số vào sổ. Dài thêm đáng kể ⇒ đề xuất dời lịch sử ra, để
  link — **không cắt nội dung còn hiệu lực** (User 2026-10-25: sợ agent mất ngữ cảnh).
- **Memory dùng chung cho mọi session Claude** (A/B/C/D cùng thư mục): mục sai / cũ (đối chiếu
  `Project_Status.md`, `CURRENT_HANDOFF.md`) ⇒ sửa hoặc xóa; luật mọi agent cần ⇒ đưa vào tài liệu chung.
- Một luật ở hai chỗ ⇒ giữ một, chỗ kia trỏ tới.

## 5. Kết vòng

Vòng nào sửa file mà `START_SESSION.md` bắt đọc: giao một sub-agent ngữ cảnh mới đóng vai B, chỉ đọc theo
`START_SESSION.md`, báo lại vai / việc / luật cứng nó nắm được và chỗ khó hiểu — sửa chỗ thiếu trước khi kết vòng
(2026-10-25: cách này tìm ra 6 chỗ chưa rõ).

3–5 dòng lời thường cho User: sự cố nào, đã đổi gì, đã gỡ gì, phiên sau theo dõi gì. Một dòng vào
`CURRENT_HANDOFF.md` và `TONG_HOP.md` của đợt. Commit khi được phép (`WORKFLOW.md` §9.6).
