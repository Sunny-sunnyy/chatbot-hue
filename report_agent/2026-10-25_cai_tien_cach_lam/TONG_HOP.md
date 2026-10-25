# Tổng hợp đợt cải tiến cách làm — 25/10/2026 (ĐÓNG 11:05)

## Mục tiêu
User: phiên này không tiếp dự án, chỉ bàn cách làm việc và cải tiến; tham khảo bản mô tả cách làm của một dự án khác
của User (bản 2, private `data/external_project_notes/`) và khóa AI FDE (User chưa học xong). Yêu cầu thêm: cách làm
phải dùng được gần như nhau cho Codex / AGY, không chỉ Claude Code.

## Quyết định theo giờ
| Giờ | Quyết định |
|---|---|
| 09:5x | Chọn: vòng tự cải tiến, nâng `run-experiment`, Session D; **không** cắt tài liệu mở phiên; đọc lại toàn khóa học, nhìn rộng |
| 10:0x | Thêm: rào bằng máy, `AGENTS.md`/`CLAUDE.md`, hai luật 1 dòng, đọc tài liệu dài bằng sub-agent; A tự quyết chi tiết |
| 10:3x | AGY đọc `START_SESSION.md`; repo chỉ chạy trên máy User |
| 10:4x | Sửa dòng §10 `Session_Prompt.md` sang chữ trung tính |
| 10:5x | Từ một file SELF_IMPROVE.md (GitHub): lấy 3 ý, không lấy phần tự sửa đệ quy; sau đó dừng thêm luật |

## Kết quả
- Mới / đổi: `skills/improve-workflow/` + `session_prompt/SO_CAI_TIEN_CACH_LAM.md`; `skills/run-experiment` (sàn / mức
  tụt / chỉ số quyết, cỡ mẫu, nhiễu A/A, kiểm người chấm); `WORKFLOW.md` §1, §2, §3.2, §8, §9.1, §9.9, §10; `Session_Prompt.md`
  §2, §5, §9; `AGENTS.md`, `CLAUDE.md`; `.githooks/pre-commit`; `.claude/settings.json`; `de_xuat_cho_du_an.md` (19 đề xuất
  cho 8.1 / 8.2 / Phase 9 / deploy — chưa làm).
- Đọc khóa học: 5 sub-agent × 3 tóm tắt → `data/course_notes/v2/` (private); A tự kiểm 4 khẳng định quan trọng (đều
  đúng); sổ khái niệm cho Session D `data/hoc_cung_D/SO_KHAI_NIEM.md` (28 mục, private).
- Kiểm độc lập: vòng 1 `changes_requested` (F1 major: hook lọt dòng bắt đầu `++`, 6 minor) → sửa → vòng 2 `ready`
  (17/17 chặn, 10/10 qua); diff SELF_IMPROVE `ready` (3 nit đã sửa). Thử mở phiên (sub-agent đóng vai B): nắm đúng vai,
  việc, luật cứng, vị trí mọi thứ mới; 6 câu hỏi dự án ghi vào `CURRENT_HANDOFF.md` "Việc của A".
- Commit: `2ecdef2`, `2d1255a`, `455e453`, `187314e` + commit kết phiên. Tiền API: 0 USD.

## Giới hạn
- Mọi thay đổi đang `đang thử`; bằng chứng có ích chỉ là quan sát qua các phiên tới (sổ cải tiến).
- Chưa chạy Codex / AGY thật để thử mở phiên; luật deny `.env` chỉ áp cho Claude Code.
- Lượng chữ mở phiên tăng ~25 dòng (khoảng 770 dòng). Theo dõi ở vòng cải tiến; không cắt nội dung còn hiệu lực.

## Bước tiếp
Phiên sau quay lại Phase 8.1: `CURRENT_HANDOFF.md` mục "PHIÊN SAU"; đọc `de_xuat_cho_du_an.md` mục 1–8 và trả lời 6 câu
ở "Việc của A" khi duyệt plan B16 (G4 / G2).
