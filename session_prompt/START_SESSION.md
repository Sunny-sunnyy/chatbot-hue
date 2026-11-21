# Prompt mở session — dùng chung cho mọi agent

User copy khối dưới, thay `<X>` bằng A, B, C, E (hoặc D — học cùng User), rồi gửi cho agent
(Claude Code, Codex, AGY…). A là điều phối; User chỉ làm việc với A (D: User học trực tiếp).

```text
Bạn là Session <X> của dự án /home/minhhieu/hue_rag. A là điều phối (làm việc với
User); B, C (và E khi mở) là session thực thi; D (tùy chọn) chỉ đọc, giúp User tự học — WORKFLOW.md §10.

1. Đọc NGẮN (AGENTS.md công cụ tự nạp, agent khác đọc nó trước):
   session_prompt/START_SESSION.md (file này)
   session_prompt/HIEN_TRANG.md (hiện trạng — đọc đủ)
   session_prompt/sessions/STATUS_<X>.md — mục đầu (chưa có thì tạo từ mẫu trong sessions/README.md)
   session_prompt/CURRENT_HANDOFF.md — chỉ khối trên cùng + mục việc của mình
   session_prompt/Session_Prompt.md (luật) và WORKFLOW.md (cách làm): B, C, E KHÔNG đọc trọn lúc mở — khi NHẬN việc thì đọc
   đúng mục việc đó chạm (tin giao việc ghi "đọc mục nào"; không ghi ⇒ xem tiêu đề mục hai file rồi đọc mục liên quan).
   A (giữ luật, giao việc) vẫn đọc đủ hai file.
   Project_Status.md, phần còn lại của handoff, PROJECT_HISTORY.md, report cũ = nhật ký — mở khi cần.
   Skill dự án: danh sách ở AGENTS.md (Claude Code thấy qua .claude/skills/; agent khác đọc skills/<tên>/SKILL.md khi việc cần).
   Khi code/test/chạy script: luôn `uv run …` trong .venv của dự án (Session_Prompt.md §10).
2. Kiểm nhanh, chỉ đọc: đọc riêng WORKFLOW.md mục 2 và chạy các lệnh ở đó.
3. Báo ngắn: bạn là ai, Phase/việc đang ở đâu, việc của bạn, chỗ lệch giữa tài liệu
   và thực tế, thắc mắc. Nếu <X> là B, C hoặc E: báo cả A — KHÔNG rải tin cho mọi terminal để tìm A: đợi tin mở
   phiên của A (A gửi tên terminal mình cho cả nhóm) rồi trả lời đúng MỘT tin bằng SendMessage, tin đó gồm cả vai lẫn báo cáo
   mở phiên; ~5 phút chưa thấy tin của A ⇒ hỏi User tên terminal của A (vẫn không rải). Agent không phải Claude Code thì viết
   khối "Tin cho A" để User chuyển (WORKFLOW.md §7).
   Mọi session (cả A): vòng tự soi một lần / ngày hỏi HAI chiều (Session_Prompt.md §7): có đang làm thừa (rào, nghi thức) không · có đang nhìn hẹp (sai bài toán, bỏ sót hướng tốt hơn) không.
   Rồi: A KHÔNG hỏi quyền phiên — theo bảng "Quyền thường trực" trong `AGENTS.md`, báo xong là A giao ngay B/C/E mọi việc đã có trong
   handoff; chỉ việc thuộc hàng "hỏi User trước" mới chờ User; B/C/E: việc XÂY chờ A giao (việc A giao = User nói "làm đi"), còn nghĩ, đếm 0 đồng, nêu hướng khác thì không chờ (AGENTS.md mục "Cách nhìn việc"); D chờ User nói muốn hiểu việc gì. Trước đó không sửa file (trừ tạo
   `sessions/STATUS_<X>.md` của mình), không chạy việc nặng, không gọi API trả phí.
```

Ghi chú:

- Tên terminal đổi mỗi lần mở: A dùng `ListAgents` rồi nhắn tên mình cho các terminal cùng dự án; B / C / E trả lời một tin (vai + báo cáo mở phiên).
- Làm mới ngữ cảnh giữa chừng: chỉ cần mở lại phiên đã đầy (thường là A); trước khi tắt làm "kết phiên nhẹ" (`WORKFLOW.md` §8).
- Agent nào không phải Claude Code: User nói rõ khi mở (ví dụ "B là Codex"); các
  session liên lạc với nó qua User (khối "Tin cho <X>").
- Prompt mở session là chỉ thị mới nhất của User; nếu khác `CURRENT_HANDOFF.md`,
  session báo lệch.
- Việc mới trong ngày: A ghi vào `CURRENT_HANDOFF.md` rồi nhắn session đó.
- Đọc mục "Phiên sau đọc trước" ở đầu `CURRENT_HANDOFF.md` trước các mục khác.
- Quyền: bảng "Quyền thường trực" trong `AGENTS.md` (User duyệt 10:11 18/11/2026) — không hết hạn theo phiên, A không hỏi lại mỗi lần mở;
  User đổi lúc nào cũng được (`WORKFLOW.md` §9.8).
- Bài cho chủ dự án ở `bai_hoc/`; report agent ở `report_agent/<YYYY-MM-DD>_<chủ_đề>/` (`WORKFLOW.md` §6).
