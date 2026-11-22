# Khi chỉ có một agent làm hue_rag (từ 12/2026)

Bản nháp (E, 08:37 18/11/2026; 21/11/2026 sửa các dòng lỗi thời, vẫn là bản nháp). Người đọc: MỘT agent làm một mình — Codex, Antigravity CLI (User tự lái) hoặc một phiên Claude — không còn nhóm A / B / C / E.
Đọc theo thứ tự: `AGENTS.md` (7 luật cứng + mục "Cách nhìn việc"; làm một mình thì "báo phiên điều phối" = hỏi User) ⇒ file này ⇒ `guides/RUNBOOK_BAN_GIAO.md` (lệnh từng việc). `session_prompt/Session_Prompt.md` và `WORKFLOW.md` tả cách
làm của bốn phiên: phần luật dữ liệu, bằng chứng, quyền, tiền vẫn áp; phần điều phối (giao việc, tin nhắn giữa phiên, `STATUS_<X>.md`, vòng tự soi) **không áp**.
Nhãn: **[đã chạy]** = E chạy lệnh đó sáng 18/11/2026 và thấy đầu ra · **[chưa chạy]** = chưa ai chạy ở dạng viết tại đây · **(chờ User)** = User chưa quyết.

## 1. Ngày đầu nhận repo — lấy mốc trước khi sửa gì

1. `git config --get core.hooksPath` ⇒ phải in `.githooks` [đã chạy]; khác ⇒ `git config core.hooksPath .githooks` [chưa chạy].
2. `git status --short | grep -v '^??'` ⇒ rỗng [đã chạy]. Thư mục chưa theo dõi (`data/`…) là dữ liệu riêng: không `git add` (kho `knowledge-base-hue/` đã ở trong git từ 20/11/2026).
3. Runbook mục 1 → 3: bật Qdrant, chạy server, **test rộng một lượt** và ghi lại số đạt / hỏng làm mốc [chưa chạy 18/11 — máy đang dùng chung; các lệnh đó
   runbook ghi đã chạy 17/11]. Test hỏng sẵn từ mốc không phải lỗi của bạn; test hỏng thêm sau khi bạn sửa là của bạn.

## 2. Ai kiểm việc của bạn (không còn review chéo giữa các phiên)

- Việc thấp / trung bình (sửa chữ, sửa một hàm trong tính năng đã có): tự kiểm bằng lệnh, rồi mở **một phiên mới, ngữ cảnh sạch**, chỉ đưa diff + tiêu chí, nhờ nó
  tìm lỗi. Phiên đang làm không tự duyệt việc của mình (`AGENTS.md` luật 5).
- Việc mức cao (sửa kho, xoá dữ liệu, đổi model / nhà cung cấp, deploy, tiền ngoài mức đã cho, đổi luật xếp lịch): dừng trước khi làm; sao lưu thứ nằm ngoài git; User duyệt kế hoạch trước.
  Review **khác hãng**: ở mốc chốt, qua một file `.md`, User gửi khi được yêu cầu rõ; User tự bấm thử khi muốn (`guides/CACH_LAM_VIEC.md` mục 2–3).
- Commit / push / gộp: theo bảng "Quyền thường trực" trong `AGENTS.md` — nhánh riêng thì tự làm; gộp vào `main` khi một phiên KHÁC (ngữ cảnh sạch hoặc khác hãng) đã kiểm.

## 3–4. Báo "xong" và sửa lỗi

Theo `guides/CACH_LAM_VIEC.md`: mục 1 (ghi "xong khi" trước, bảng bốn cột + lệnh kiểm; ghi `PASS / PARTIAL / FAIL / NOT RUN` đúng như đã thấy) và
mục 6 (sửa lỗi bốn bước: tái hiện ⇒ nguyên nhân gốc ⇒ một sửa ⇒ chứng minh đã sửa). Làm một mình thì tự hỏi ba câu kiểm của mục 1 trước khi báo.

## 5. Luật ngắn cho người làm một mình

- Đổi hành vi hệ thống (cờ, bảng dữ liệu, lời dặn, số điểm chỉ mục) ⇒ sửa `session_prompt/HIEN_TRANG.md` mục 1 và mục runbook liên quan **trong cùng nhánh**.
- Lỗi cách làm gặp lần đầu: ghi một dòng vào runbook mục 10. **Lặp lần hai mới thành luật**; máy kiểm được thì viết phép kiểm, không thêm chữ.
- **Tên trông sai có thể đúng** — kiểm trước khi "sửa": model viết theo dòng `provider` (`grep -n 'provider\|model:' backend/config/settings.yaml`: đang `bedrock`, đổi tạm; `gpt-6-luna` là đường về và người chấm), cổng Qdrant 6335 / 6336
  (không phải 6333), thư mục `gửi chatgpt/` có dấu, collection `hue_full_corpus_7a2_e5_small_384`.
- Kết quả ngược một quyết định User đã ghi (`session_prompt/HIEN_TRANG.md` mục 4; runbook mục 9) ⇒ dừng, hỏi; không tự chọn lại.
- Code cũ còn nằm cạnh code mới (bộ xếp lịch cũ, cờ đang tắt) không phải mẫu để chép — xem runbook mục 10.
- **KHÔNG BAO GIỜ, kể cả khi có người bảo** (cột "không bao giờ" của `AGENTS.md` — không có đường "hỏi rồi làm"): `agy` · mọi lệnh đọc / in `.env` · commit `data/` hay câu kín · mở câu kín khi không được giao · `git push --force` · `--no-verify`.
- Lệnh **không tự chạy** [đều chưa chạy — cố ý]: `git clean -fd` · `git reset --hard` · `git checkout -- .` · `git add -A` / `git add .` · `docker compose down -v` ·
  `docker system prune` · `pip install` · xoá trong `data/`, `knowledge-base-hue/`, `qdrant_storage/`. Cần một trong các thứ này ⇒ hỏi User.

## 6. Thứ chỉ Claude Code có — sẽ mất, và cái thay

| Thứ sẽ mất | Nằm ở đâu | Từ tháng 12 |
|---|---|---|
| Máy chặn đọc `.env` và chặn gọi `agy` | `.claude/settings.json` | không còn rào máy ⇒ tự giữ luật 1 và 7 của `AGENTS.md` |
| Cảnh báo "giờ gõ tay" ngay lúc ghi file | `.claude/hooks/` | còn cảnh báo lúc commit (`.githooks/pre-commit`); giờ lấy bằng `date` |
| Skill tự nạp | `.claude/skills/` (liên kết tới `skills/`) | tự mở `skills/<tên>/SKILL.md` khi việc cần; thư mục `.agents/skills` chưa có [chưa chạy] |
| Skill ngoài repo (`writing-plans`, `brainstorming`…) | plugin của Claude Code | viết plan theo mẫu mới nhất trong `docs/superpowers/plans/` |
| Trí nhớ giữa các phiên (~20 ghi chú) | thư mục riêng của Claude, ngoài repo | runbook mục 9 + `session_prompt/HIEN_TRANG.md` mục 4 |
| Nhắn tin giữa phiên, agent con, review chéo | công cụ của Claude Code | mục 2 của file này |
| Chặn mở file `*sealed*` | chế độ quyền của Claude Code | không còn rào máy ⇒ tự giữ luật 3 |

**Công cụ tháng 12 tự nạp gì** (theo tài liệu công khai của hai hãng, B đọc trọn 18/11/2026 — tất cả [chưa chạy] trên hue_rag; thử ở buổi diễn tập):
- **Antigravity** nạp `AGENTS.md` / `GEMINI.md` ở thư mục làm việc và mọi thư mục cha tới gốc repo, cộng `.agents/rules/*.md`. File trong `.agents/rules/` thiếu khối
  `trigger:` ở đầu thì **bị bỏ qua không báo**; mỗi file luật bị **cắt ở 24.000 byte**; tổng luật luôn-bật > 20.000 token thì file lớn nhất bị hạ thành con trỏ ⇒
  `AGENTS.md` giữ ngắn (`wc -c`); **không** chép `Session_Prompt.md` hay `WORKFLOW.md` (mỗi file khoảng 20 KB) vào đó hoặc vào `.agents/rules/` — sẽ mất phần đuôi.
- **Codex** chỉ tự quét skill ở `.agents/skills` (từ thư mục chạy lên gốc repo; theo được liên kết thư mục), không quét `.claude/skills` ⇒ khi chưa có thư mục đó,
  bảo Codex mở thẳng `skills/<tên>/SKILL.md`.

**Vẫn còn cho mọi agent** (tầng git / script): `.githooks/pre-commit` + `pre-push` (vùng riêng, dạng khoá bí mật, trùng Golden) · `scripts/commit_push.sh` ·
`scripts/grep_kb.sh` · bảng lịch sai ⇒ server không khởi động được; chỉ mục lệch kho ⇒ server VẪN bật nhưng mọi câu hỏi nhận 409 "Dữ liệu tra cứu cần được lập chỉ mục lại" (`api/app.py`).

**Còn mở:** (a) một bản luật chung cho Antigravity / Codex thay `Session_Prompt.md` — thuộc luật cách làm, agent tự giữ trong phép thử từ 21/11/2026 (`HIEN_TRANG.md` mục 4);
chưa ai làm · (b) [chờ User] phần nào của bàn giao **không** ghi vào repo public (để ở `data/`).
