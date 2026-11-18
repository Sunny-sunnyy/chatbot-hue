# Khi chỉ có một agent làm hue_rag (từ 12/2026)

Bản nháp (E, 08:37 18/11/2026). Người đọc: MỘT agent làm một mình — Codex, Antigravity CLI (User tự lái) hoặc một phiên Claude — không còn nhóm A / B / C / E.
Đọc theo thứ tự: `AGENTS.md` (7 luật cứng) ⇒ file này ⇒ `guides/RUNBOOK_BAN_GIAO.md` (lệnh từng việc). `session_prompt/Session_Prompt.md` và `WORKFLOW.md` tả cách
làm của bốn phiên: phần luật dữ liệu, bằng chứng, quyền, tiền vẫn áp; phần điều phối (giao việc, tin nhắn giữa phiên, `STATUS_<X>.md`, vòng tự soi) **không áp**.
Nhãn: **[đã chạy]** = E chạy lệnh đó sáng 18/11/2026 và thấy đầu ra · **[chưa chạy]** = chưa ai chạy ở dạng viết tại đây · **(chờ User)** = User chưa quyết.

## 1. Ngày đầu nhận repo — lấy mốc trước khi sửa gì

1. `git config --get core.hooksPath` ⇒ phải in `.githooks` [đã chạy]; khác ⇒ `git config core.hooksPath .githooks` [chưa chạy].
2. `git status --short | grep -v '^??'` ⇒ rỗng [đã chạy]. Thư mục chưa theo dõi (`data/`, `knowledge-base-hue/`, `lauran_tan/`…) là dữ liệu riêng: không `git add`.
3. Runbook mục 1 → 3: bật Qdrant, chạy server, **test rộng một lượt** và ghi lại số đạt / hỏng làm mốc [chưa chạy 18/11 — máy đang dùng chung; các lệnh đó
   runbook ghi đã chạy 17/11]. Test hỏng sẵn từ mốc không phải lỗi của bạn; test hỏng thêm sau khi bạn sửa là của bạn.

## 2. Ai kiểm việc của bạn (không còn review chéo giữa các phiên)

- Việc thấp / trung bình (sửa chữ, sửa một hàm trong tính năng đã có): tự kiểm bằng lệnh, rồi mở **một phiên mới, ngữ cảnh sạch**, chỉ đưa diff + tiêu chí, nhờ nó
  tìm lỗi. Phiên đang làm không tự duyệt việc của mình (`AGENTS.md` luật 5).
- Việc mức cao (sửa kho, xoá dữ liệu, đổi model / nhà cung cấp, deploy, tiền ngoài mức đã cho, đổi luật xếp lịch): dừng trước khi làm; User xem diff / kế hoạch.
  **(chờ User: ai kiểm việc mức cao trong tháng 12 — User tự xem diff, hay một agent khác hãng review trước.)**
- Commit / push: hỏi User trước mỗi lần. Quyền cho sẵn `git commit` / `git push` chỉ nằm trong cấu hình riêng của Claude Code trên máy này.

## 3. Trước khi báo "xong" — bảng bắt buộc (User duyệt 17/11/2026)

Mọi báo cáo "xong" kết bằng bảng bốn cột: **đã làm · chưa làm · tự hoãn + lý do · lệnh kiểm + đầu ra thật**. Không có cột lệnh kiểm thì chưa xong. Ghi `PASS / PARTIAL / FAIL / NOT RUN` đúng như đã thấy. User sẽ chọn một dòng bất kỳ và bảo bạn chạy lại trước mặt.

## 4. Khi gặp lỗi — bốn bước, không nhảy bước

Tái hiện (đúng cấu hình đang chạy, thử MỘT lượt trước) ⇒ chứng minh nguyên nhân gốc (dòng log, sổ vết — runbook mục 7) ⇒ một sửa tập trung ⇒ chứng minh đã sửa
bằng chính lệnh tái hiện. Không thêm fallback / guard để che lỗi. Hai giả thuyết ⇒ thử từng cái.

## 5. Luật ngắn cho người làm một mình

- Đổi hành vi hệ thống (cờ, bảng dữ liệu, lời dặn, số điểm chỉ mục) ⇒ sửa `session_prompt/Project_Status.md` §4 và mục runbook liên quan **trong cùng nhánh**.
- Lỗi cách làm gặp lần đầu: ghi một dòng vào runbook mục 10. **Lặp lần hai mới thành luật**; máy kiểm được thì viết phép kiểm, không thêm chữ.
- **Tên trông sai có thể đúng** — kiểm trước khi "sửa": model `gpt-6-luna` (`grep -n "model:" backend/config/settings.yaml` [đã chạy]), cổng Qdrant 6335 / 6336
  (không phải 6333), thư mục `gửi chatgpt/` có dấu, collection `hue_full_corpus_7a2_e5_small_384`.
- Kết quả ngược một quyết định User đã ghi (`Project_Status.md` §5; runbook mục 9 khi có) ⇒ dừng, hỏi; không tự chọn lại.
- Code cũ còn nằm cạnh code mới (bộ xếp lịch cũ, cờ đang tắt) không phải mẫu để chép — xem runbook mục 10 "đường cũ" khi có.
- Lệnh **không chạy** [đều chưa chạy — cố ý]: `git clean -fd` · `git reset --hard` · `git checkout -- .` · `git add -A` / `git add .` · `git push --force` ·
  `--no-verify` · `docker compose down -v` · `docker system prune` · `pip install` · `agy` · mọi lệnh đọc / in `.env` · xoá trong `data/`, `knowledge-base-hue/`,
  `qdrant_storage/`. Cần một trong các thứ này ⇒ hỏi User.

## 6. Thứ chỉ Claude Code có — sẽ mất, và cái thay

| Thứ sẽ mất | Nằm ở đâu | Từ tháng 12 |
|---|---|---|
| Máy chặn đọc `.env` và chặn gọi `agy` | `.claude/settings.json` | không còn rào máy ⇒ tự giữ luật 1 và 7 của `AGENTS.md` |
| Cảnh báo "giờ gõ tay" ngay lúc ghi file | `.claude/hooks/` | còn cảnh báo lúc commit (`.githooks/pre-commit`); giờ lấy bằng `date` |
| Skill tự nạp | `.claude/skills/` (liên kết tới `skills/`) | tự mở `skills/<tên>/SKILL.md` khi việc cần; thư mục `.agents/skills` chưa có [chưa chạy] |
| Skill ngoài repo (`writing-plans`, `brainstorming`…) | plugin của Claude Code | viết plan theo mẫu mới nhất trong `docs/superpowers/plans/` |
| Trí nhớ giữa các phiên (~20 ghi chú) | thư mục riêng của Claude, ngoài repo | runbook mục 9 (CHƯA VIẾT) |
| Nhắn tin giữa phiên, agent con, review chéo | công cụ của Claude Code | mục 2 của file này |
| Chặn mở file `*sealed*` | chế độ quyền của Claude Code | không còn rào máy ⇒ tự giữ luật 3 |

**Vẫn còn cho mọi agent** (tầng git / script): `.githooks/pre-commit` + `pre-push` (vùng riêng, dạng khoá bí mật, trùng Golden) · `scripts/commit_push.sh` ·
`scripts/grep_kb.sh` · server từ chối khởi động khi chỉ mục lệch kho hoặc bảng lịch sai.

**Còn chờ User quyết (chưa thành luật):** (a) ai kiểm việc mức cao tháng 12 · (b) có một bản luật chung cho Antigravity / Codex thay `Session_Prompt.md` hay giữ nguyên · (c) phần nào của bàn giao **không**
ghi vào repo public (để ở `data/`).
