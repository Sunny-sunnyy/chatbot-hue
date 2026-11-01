# Review: governance CA1 + CA3 của A (commit `547ac4a`)

Decision: **changes_requested** (0 blocker / 1 major / 2 minor — minor không mở vòng) · Người kiểm: B (Claude Opus 5.5) · Date: 12:44 01/11/2026 (`date`) · 0 USD
Bản kiểm: commit **`547ac4a`** — `scripts/tra_web_codex.sh` (rào CA3), `.githooks/pre-push` (mới, CA1); căn cứ C109 `data/tra_cuu_cli/2026-11-01_codex-rao-doc-file/ket_qua.md`, lượt thật của A
`data/tra_cuu_cli/2026-11-01_kiem-rao-codex/`. Một lần review gọn (A dặn: không mở vòng cho minor).

## 1. Phạm vi đã review

`git show 547ac4a` (5 file; 2 file code / hook, còn lại trạng thái). Không chạy Codex (không cần — dùng lượt thật của A + `codex --help` / `codex features list`, chỉ đọc). Không gọi `agy`.
Ca dò pre-push trong **repo tạm** có remote giả (`/tmp/b_prepush_probe2`, đã xoá) — không đụng repo thật / remote thật.

**Đạt:**
- **CA3 `tra_web_codex.sh`:** bỏ `-s` (đúng ghi chú C109: có `--sandbox` thì profile bị bỏ qua); `--disable shell_tool` / `view_image` — tên tính năng **có thật** ở `codex-cli 0.166.0` (`codex features list`:
  `shell_tool stable true`, `view_image stable true`; `codex exec --help`: `--disable <FEATURE>` = `-c features.<name>=false`); profile `webonly` chặn `:root`, chỉ đọc thư mục làm việc + đường tối thiểu;
  `command_execution > 0` ⇒ `exit 3` (trước: chỉ cảnh báo). Lượt thật của A: 3 lượt tìm web, **0** lệnh shell, mã thoát 0; sự kiện `error` duy nhất là "vượt ngân sách mô tả skill" (không liên quan rào).
- **CA1 `pre-push`:** đúng ý "lớp thứ hai cho mọi agent / người": quét **mọi** commit sắp đẩy (`remote..local`; nhánh mới: `--not --remotes`; xoá nhánh: bỏ qua). Ca dò (repo tạm, nhánh mới chưa có trên remote):
  `data/x.md` ⇒ **chặn**; dòng `sk-…` trong `backend/a.py` ⇒ **chặn**; `docs/a.md` có chữ có dấu ⇒ **qua**; **đẩy hai ref một lần** (một sạch + một có `knowledge-base-hue/k.md`) ⇒ chặn cả lượt, remote **không**
  nhận ref nào (đúng: hook thoát 1 thì git bỏ mọi ref). `.env.example` ⇒ chặn — cùng luật `(^|/)\.env($|\.)` với pre-commit, repo không có `.env.example` nào được theo dõi (`git ls-files` = 0) ⇒ nhất quán, không phải
  chặn nhầm so với luật hiện hành.

## 2. Findings

**M-1 (major) — pre-push KHÔNG chặn đường dẫn private có ký tự không phải ASCII (tên tiếng Việt).**
- Vị trí: `.githooks/pre-push:18` `files=$(git diff-tree --no-commit-id --name-only -r --diff-filter=ACMR "$c")` rồi `:21` regex `^(data/|knowledge-base-hue/|gửi chatgpt/|…`.
- Bằng chứng (B chạy thật, repo tạm, `core.quotePath` mặc định — repo thật cũng **unset**): `git diff-tree` in tên file có dấu **trong ngoặc kép kèm mã bát phân** ⇒ regex không khớp ⇒ đẩy qua:
  | Commit chứa | `diff-tree` in ra | push |
  |---|---|---|
  | `data/x.md` | `data/x.md` | **chặn** ✓ |
  | `gửi chatgpt/ghi chú.md` | `"g\341\273\255i chatgpt/ghi ch\303\272.md"` | **qua (rc 0)** ✗ |
  | `data/ghi chú.md` | `"data/ghi ch\303\272.md"` | **qua (rc 0)** ✗ |
- Tác động: đúng vùng private của repo này hay có tên tiếng Việt — thư mục `gửi chatgpt/` (luôn có dấu) và nhiều file kho (`knowledge-base-hue/…/Đồi Vọng Cảnh.md` …) ⇒ lớp thứ hai lọt đúng ca nó sinh ra để bắt
  (commit tạo bằng `--no-verify` / máy chưa bật pre-commit). Kiểm tên dự án khác trên **tên file** (`:27`) cũng đọc `$files` nên cùng lỗ. Pre-commit **không** dính: `.githooks/pre-commit:14` dùng `-z`.
- Tiêu chí đóng: lấy tên file bằng `-z` như pre-commit (`git diff-tree --no-commit-id --name-only -r -z --diff-filter=ACMR "$c" | tr '\0' '\n'`, hoặc `git -c core.quotePath=false …`); chạy lại 3 ca trên ⇒
  cả 3 **chặn**, ca `docs/a.md` vẫn qua.

**m-1 (minor, không mở vòng) — còn tính năng Codex có thể chạm file / chạy lệnh chưa tắt.** `codex features list` (0.166.0) còn bật: `unified_exec` (+ `unified_exec_tty`, công cụ chạy lệnh khác `shell_tool`),
`browser_use` / `browser_use_full_cdp_access`, `computer_use`, `code_mode_host`, `multi_agent`, `apps` / `plugins`. C109 không bàn các tính năng này. Lớp 2 (profile chỉ đọc thư mục làm việc) + lớp 3 (bắt
`command_execution`) vẫn che phần lớn, và lượt thật 0 lệnh. Gợi ý (một dòng, tùy A): thêm `--disable unified_exec --disable browser_use --disable computer_use --disable code_mode_host --disable multi_agent`.

**m-2 (minor, không mở vòng) — đầu script bỏ mất giới hạn "Codex vẫn nạp `~/.codex/skills`" dù vẫn đúng.** `--ignore-user-config` không chặn quét skill: `codex.err` lượt của A ghi
`skills scan reached its traversal limit (root: …/.codex/skills)` và sự kiện "1189 skills were not included". Ghi chú cũ (đã xoá ở `547ac4a`) nên giữ để người đọc không nghĩ skill của User đã bị tách.

## 3. Cách người kiểm chạy lại thật

- `git show 547ac4a`; `codex --version`; `codex exec --help | grep`; `codex features list` (chỉ đọc); `jq` trên `codex.jsonl` + đọc `codex.err` lượt của A.
- Repo tạm: `git init --bare -b main remote.git` + `work` (chép `pre-push`, `core.hooksPath .githooks`), mỗi ca một nhánh mới từ `main` rồi `git push origin <nhánh>`; một lượt `git push origin m_clean m_bad`.
  Đã `rm -rf` repo tạm (`/tmp/b_prepush_probe*` không còn).

## 4. Kết quả quan sát

Như §1 và bảng M-1. Câu bất biến kiểm: "commit sạch (kể cả chữ có dấu trong nội dung) vẫn đẩy được" — giữ (`docs/a.md` qua).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lượt Codex mới (tránh dùng gói tài khoản cho việc A đã có bằng chứng); không thử ép Codex dùng `unified_exec` / `browser_use` để đọc file (m-1 là [Code / tài liệu], chưa chạy).
- Không thử commit merge có nội dung giải xung đột riêng (pre-push đọc `git show` của merge — chưa kiểm).

## 6. Decision và bước tiếp theo

`changes_requested` chỉ vì **M-1** (sửa một dòng `-z`, chạy lại 3 ca). m-1 / m-2 tùy A, không mở vòng. Sửa xong ⇒ B kiểm đúng 3 ca M-1.

## Vòng 2 (12:50 01/11/2026 `date`, B) — kiểm `89c988e`: **ready**. M-1 đóng: repo tạm với hook mới (`-z`) ⇒ `data/x.md`, `gửi chatgpt/ghi chú.md`, `data/ghi chú.md`, `knowledge-base-hue/…/Đồi.md` đều **chặn**; `docs/ghi chú sạch.md` qua (repo tạm đã xoá). m-1: tắt thêm browser_use / browser_use_external / computer_use / apps / plugins / multi_agent, giữ `code_mode_host` có lý do; `unified_exec` ghi giới hạn (lớp 2 + 3); lượt 3 của A: tìm web 3, shell 0, không cảnh báo cờ. m-2: dòng skills trả lại (`tra_web_codex.sh:13-14`). Không mở vòng.
