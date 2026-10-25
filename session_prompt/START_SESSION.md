# Prompt mở session — dùng chung cho mọi agent

User copy khối dưới, thay `<X>` bằng A, B, C (hoặc D — học cùng User), rồi gửi cho agent
(Claude Code, Codex, AGY…). A là điều phối; User chỉ làm việc với A (D: User học trực tiếp).

```text
Bạn là Session <X> của dự án /home/minhhieu/hue_rag. A là điều phối (làm việc với
User); B, C là session thực thi; D (tùy chọn) chỉ đọc, giúp User tự học — WORKFLOW.md §10.

1. Đọc toàn bộ, theo thứ tự:
   session_prompt/START_SESSION.md
   session_prompt/Session_Prompt.md
   session_prompt/WORKFLOW.md
   session_prompt/Project_Status.md
   session_prompt/CURRENT_HANDOFF.md
   session_prompt/sessions/STATUS_<X>.md (chưa có thì tạo từ mẫu trong sessions/README.md)
   Sau đó chỉ đọc những gì mục việc của <X> trong CURRENT_HANDOFF chỉ định.
   PROJECT_HISTORY.md và report cũ chỉ mở khi cần trả lời một câu cụ thể.
   Skill dự án nằm ở .claude/skills/ (Claude Code tự thấy; agent khác đọc
   skills/<tên>/SKILL.md): practical-project-coding khi sửa code/test,
   risk-gated-agent-review khi review chéo, propose-options khi đưa lựa chọn cho User,
   run-experiment khi thử/so sánh phương án, improve-workflow (A) khi kết phiên / rút kinh nghiệm.
   Khi code/test/chạy script: luôn `uv run …` trong .venv của dự án (Session_Prompt.md §10).
2. Kiểm nhanh, chỉ đọc, theo WORKFLOW.md mục 2.
3. Báo ngắn: bạn là ai, Phase/việc đang ở đâu, việc của bạn, chỗ lệch giữa tài liệu
   và thực tế, thắc mắc. Nếu <X> là B hoặc C: báo cả A — bằng SendMessage nếu cả
   hai là Claude Code, nếu không thì viết khối "Tin cho A" để User chuyển
   (WORKFLOW.md §7).
   Rồi chờ: A chờ User nói "làm đi"; B/C chờ A giao việc; D chờ User nói muốn hiểu việc gì. Trước đó không sửa file (trừ tạo
   `sessions/STATUS_<X>.md` của mình), không chạy việc nặng, không gọi API trả phí.
```

Ghi chú:

- Tên terminal đổi mỗi lần mở: dùng `ListAgents`, hỏi "là B hay C" nếu chưa rõ.
- Agent nào không phải Claude Code: User nói rõ khi mở (ví dụ "B là Codex"); các
  session liên lạc với nó qua User (khối "Tin cho <X>").
- Prompt mở session là chỉ thị mới nhất của User; nếu khác `CURRENT_HANDOFF.md`,
  session báo lệch.
- Việc mới trong ngày: A ghi vào `CURRENT_HANDOFF.md` rồi nhắn session đó.
- Đọc mục "Phiên sau đọc trước" ở đầu `CURRENT_HANDOFF.md` trước các mục khác.
- Quyền đặc biệt của phiên trước (tự điều phối rộng, trần tiền) hết hạn khi kết phiên; A hỏi lại
  User trong báo cáo mở phiên (`WORKFLOW.md` §9.8).
- Báo cáo cho User nằm ở `bao_cao_he_thong/` (mục lục `README.md`); report agent ở
  `report_agent/<YYYY-MM-DD>_<chủ_đề>/` (`WORKFLOW.md` §6).
