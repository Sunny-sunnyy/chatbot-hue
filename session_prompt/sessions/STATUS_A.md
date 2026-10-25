# STATUS A — cập nhật 11:05 25/10/2026 (kết phiên sáng)

Terminal: `hue-rag-2c` · Agent: Claude Opus 5.5 · Vai: điều phối. Phiên này không mở B/C (tên terminal đổi mỗi lần mở).

## Commit cuối
- Trước phiên: `4d641db`. Phiên 25/10: `2ecdef2`, `2d1255a`, `455e453`, `187314e`, `abded38` + commit STATUS này (`git log -1`).

## Đang làm
- Không. Phiên sau quay lại Phase 8.1: `CURRENT_HANDOFF.md` mục "PHIÊN SAU" + "Việc của A" (6 câu khi duyệt B16).

## Đang khai báo sửa
- không

## Vừa xong (phiên 25/10 sáng — chỉ cách làm)
- Đợt `report_agent/2026-10-25_cai_tien_cach_lam/` ĐÓNG (`TONG_HOP.md`): `improve-workflow` + sổ, `run-experiment` nâng,
  Session D, `AGENTS.md`/`CLAUDE.md`, hook `.githooks/pre-commit`, deny `.env` cho Claude Code, 19 đề xuất cho dự án.
- Kiểm độc lập 2 vòng (ready) + thử mở phiên bằng sub-agent đóng vai B (nắm đúng).
- Bản mô tả cách làm của dự án khác (bản 2) để private ở `data/external_project_notes/`; file tracked giữ bản 1.

## Đã học / bẫy gặp
- Brief sub-agent: đọc lại trước khi gửi (lỡ gửi còn `{{…}}`). Kết quả sub-agent: tự kiểm 2–3 khẳng định chính.
- Phép thử có thể sai: key giả sinh quá ngắn làm tưởng hook lỗi — kiểm chính phép thử trước khi kết luận.
- Review chéo bắt được lỗi hook mà 12 ca tự thử không bắt (S10) — không bỏ bước review cho thay đổi "nhỏ".
- Sửa tài liệu bằng script: dùng `uv run python`, không `python3` hệ thống (S11).
- Luật deny `.env*` chặn cả lệnh shell nhắc tới tên file đó (`ls`, `rm`) — nhờ User chạy `!` khi cần.
- `git worktree list` có 4 worktree cũ của AGY dưới `~/.gemini/` — không phải của A, để nguyên.
- (giữ) Repo PUBLIC; người điều phối không đọc câu kín; `CURRENT_HANDOFF.md` đọc lại trước khi sửa.

## Việc dở / câu hỏi cho User (phiên sau)
- Quyền phiên (điều phối rộng, trần tiền) — hỏi lại khi mở phiên.
- Câu hỏi dự án cũ vẫn mở: `CURRENT_HANDOFF.md` "Câu hỏi cho User".

## Tiền paid phiên này
- 0 USD. Sub-agent (5 đọc khóa học, 1 review 2 vòng, 1 thử mở phiên, 1 review nhỏ) dùng quota Claude Code.
