# TỔNG HỢP đợt 2026-10-31 — áp khung làm dự án theo khoá AI FDE (khung_fde) vào cách làm của hue_rag

Viết 16:56 31/10/2026 (A, kết phiên chiều). Trạng thái: **ĐÓNG** (User: phiên chiều chỉ làm AI FDE; mọi thay đổi governance có review ngữ cảnh mới, đã commit + push).
Chatbot **không đổi**. 0 USD API trả phí. Dữ liệu / ghi chú (private): `data/external_project_notes/HUE_RAG_DOI_CHIEU_KHUNG_FDE_2026-10-31.md` (đối chiếu đầy đủ a–f),
`data/external_project_notes/` (bản gửi lại dự án kia, file 31/10), `data/course_notes/README.md` (đọc file nào về khoá).

## Mục tiêu
Một dự án khác của User dựng một **khung chung** (khung cá nhân của User, private, ngoài repo — `khung_fde`) từ khoá "AI FDE" bản tóm tắt mới (ver4): nguyên tắc theo
7 giai đoạn, chỉ mục bài, skill mẫu, hook mẫu. User giao A hue_rag: đọc, đối chiếu với hue_rag (code thắng ghi chép), đề xuất lấy gì / giữ gì, rồi áp phần User duyệt.

## Quyết định theo giờ (giờ A ghi nhận bằng `date`; tin User không có dấu giờ)
- 15:25 — mở phiên A (terminal `hue-rag-d5`); B / C không mở.
- 15:51 — User duyệt d1–d3 (hook giờ ước, xét mọi mục đang thử, skill `teach-and-quiz`).
- 15:59 — User: phiên này **chỉ làm AI FDE**, chưa làm tiếp dự án; A được commit + push.
- giữa 15:59 và 16:02 — User chọn gửi kết quả lại cho dự án kia trước, chưa mở Session D, "cho xong AI FDE cả".
- giữa 16:02 và 16:23 — User đồng ý chạy vòng xét đầu tiên (C); rồi để A quyết ("theo bạn nên làm gì") ⇒ A chọn kiểm độc lập trước khi ghi sổ.
- giữa 16:26 và 16:43 — User: chép 2 skill agent; hỏi `session_prompt/` đủ chưa; ghi chú khoá học có cần chép không.
- giữa 16:47 và 16:48 — User: Phase 9 **mở bằng nghiên cứu rộng** (đề tài, dự án, paper, ứng dụng thật), không khoá vào gợi ý lịch trình; Phase 1–8 = RAG mức 1.

## Kết quả
| Việc | Kết quả | Commit |
|---|---|---|
| Đối chiếu (3 agent con đọc ver4 theo tuần) | ver4 **không lật** đề xuất Đ1–Đ3 của bản 30/10; 4 chỗ phải xem lại: bản 30/10 bỏ sót "review cả nhánh bằng agent con ngữ cảnh mới" (khoá W1D5·43); W33 chưa tách lợi "khác họ model" khỏi "ngữ cảnh sạch"; 1 nhãn đổi (cách tính lượt lỗi kỹ thuật — hue_rag chặt hơn khoá); bảng giới hạn ghi khi đóng từng spec | (private) |
| W37 hook Claude Code cảnh báo giờ ước lúc ghi | `.claude/hooks/` + `settings.json`; `thu_hook.sh` 12 / 12; bắt đúng 2 giờ ước A gõ trong phiên trước khi commit; báo nhầm 1 | `f34cb7f` |
| W38 mỗi vòng xét mọi mục đang thử; W39 `teach-and-quiz` cho Session D | `improve-workflow` §3; skill mới + `WORKFLOW.md` §10 (thay luật "skill D sau 2 buổi") | `f34cb7f` |
| Vòng cải tiến 12 (lần dùng đầu W38) | 40 ⇒ **7** mục đang thử; 4 gộp; 0 gỡ; I3 lên nấc (memory trạng thái cũ ⇒ con trỏ); kiểm độc lập sửa 6 chỗ | `32d4b68` |
| W40 phần nhỏ từ skill mẫu | `propose-options` §4b khám phá 5 dòng, §4c; `practical-project-coding` `git grep` mọi nơi gọi + "Giải thích ngắn" | `0d69376` |
| W41 `agent-design-review`, `agent-security-review` | chép sẵn cho Phase 9; security dùng một lần lúc đóng gói Phase 1–8 | `1e375a4` |
| Đồng bộ luật | danh sách skill / hook ở `AGENTS.md`, `START_SESSION.md`, `WORKFLOW.md` §3.2 §6, `Project_Status.md` §5 §7 | `1e375a4` |
| Phase 9 + "RAG mức 1" | `Project_Status.md` §3, §5; handoff mục 5 | `9e83f18` |
| Gửi lại dự án kia | đề xuất sửa khung (hook, 1 số sai trong nguyên tắc, mâu thuẫn trong mẫu `teach-and-quiz`) + bản chung `risk-gated-agent-review` + ứng viên đã "đang dùng" ⇒ khung lên v1.2 rồi v2 (phía dự án kia) | (private) |

**Review:** 5 lượt người kiểm ngữ cảnh mới (W37–W39: 2 vòng, vòng 1 **2 major**; vòng xét 12: sửa 6 chỗ; W40: ready + 5 minor; W41: 2 vòng, vòng 1 **1 major**). Cả 3 major là lỗi
của A, không lộ ra ngoài vì bắt trước commit: chi tiết sự cố dự án khác trong chú thích hook (M-1) và trong ví dụ skill agent — **S60** (2 lần); skill D lệch `WORKFLOW.md` §10 về ghi câu sai.
Hook git `.githooks/pre-commit` cũng chặn đúng 1 lần (tên dự án khác trong dòng STATUS_A).

## Sau kết phiên (User yêu cầu thêm, tới 17:40 31/10/2026)
- Rà lại cả 11 `BAO_CAO_*` / `LUONG` / `DE_XUAT` bằng 5 agent con + 2 người kiểm (vòng 1 phần 2: 2 major — câu Golden lệch kho chưa vào Tóm tắt / checklist; vòng 2 ready) — `4492239`.
- Luật `WORKFLOW.md` §6 "báo cáo luôn đúng thông tin mới nhất" + `run-experiment` §5; memory `reports-always-current`.
- Kiểm Golden chạy lại: 176 đọc được, 1 lỗi "keyword not verbatim in corpus" (dòng 128) — chờ User.
- Brainstorm báo cáo so sánh (5 câu, AskUserQuestion từ câu 2 — S62 câu 1 A viết chữ, User nhắc): quyết định ở `CURRENT_HANDOFF.md` mục 4; gom dời phiên sau.

## Giới hạn
- Bằng chứng vòng xét 12 phần lớn là "được dùng, không thấy lặp" — quan sát, không phải chứng minh; người chấm đầu là A (người đề xuất luật), có kiểm độc lập.
- W37 chỉ chạy cho Claude Code và chỉ trong 4 thư mục tài liệu; Codex / AGY dựa hook git W30 + dòng chữ; `data/` ngoài phạm vi (A gõ 1 giờ ước vào ghi chú `data/`, tự sửa).
- Hook giờ ước: các giới hạn đã biết ghi trong chú thích hook (đường dẫn tuyệt đối, MultiEdit, `git add` cùng lệnh, dòng mới bắt đầu bằng `+`, nhiều session chung `.seen`).
- Skill agent chưa dùng thật lần nào (hue_rag chưa có agent).

## Bước tiếp
- Phiên sau: quay lại dự án theo thứ tự cũ — spec streaming (Q1 + duyệt sha) ⇒ code S1 (dùng `git grep` W40, review cả nhánh trước merge) ⇒ nhiều lượt ⇒ đóng gói (nhìn lại
  Phase 1–8 theo khung, `agent-security-review` một lần) ⇒ Phase 9 mở bằng nghiên cứu rộng.
- Câu cho User: W35 / I8 / W36 (vòng 11); W42 đề xuất cho S60 (handoff).
- Theo dõi: W37 báo đúng / nhầm; W38 vòng sau; W39 hạn 07/11 (0 buổi D ⇒ đề xuất gỡ); I3 memory.
