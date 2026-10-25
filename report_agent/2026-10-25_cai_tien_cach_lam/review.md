# Review: đợt cải tiến cách làm 2026-10-25 (W1–W9)

Decision: **changes_requested**
Người kiểm: sub-agent ngữ cảnh mới (Claude Opus 5.5), do A giao; không nhận kết luận của A
Date: 10:25 25/10/2026 (lấy bằng `date`)
Canonical guide: `report_agent/2026-10-25_cai_tien_cach_lam/KE_HOACH.md` (tiêu chí 1–6, hợp đồng kiểm)
Implementation report: không có file riêng; dùng `KE_HOACH.md` + `session_prompt/SO_CAI_TIEN_CACH_LAM.md`

## 1. Phạm vi đã review

- Git: `main` ở `4d641db`, chưa có gì staged (`git diff --cached --name-only` = 0 dòng).
- Đọc hết: `AGENTS.md`, `CLAUDE.md`, `.githooks/pre-commit`, `.claude/settings.json`, symlink
  `.claude/skills/improve-workflow -> ../../skills/improve-workflow`, `skills/improve-workflow/SKILL.md`,
  `session_prompt/SO_CAI_TIEN_CACH_LAM.md`, `KE_HOACH.md`, `de_xuat_cho_du_an.md`,
  `skills/risk-gated-agent-review/SKILL.md`, `session_prompt/TEMPLATE_REVIEW.md`, `START_SESSION.md` (bản mới).
- Đọc exact diff: `.gitignore`, `skills/run-experiment/SKILL.md`, `session_prompt/{Session_Prompt,WORKFLOW,START_SESSION,CURRENT_HANDOFF,Project_Status}.md`,
  `session_prompt/sessions/STATUS_A.md`, `report_agent/README.md`; đọc thêm `Session_Prompt.md` §4–§6, §10 để đối chiếu.
- File của B (ngoài phạm vi): `g1_retrieval.py`, `phase_8_1_g1_implementation.md`, `phase_8_1_g2_g4_plan.md` sửa
  lần cuối 22:40–22:45 24/10; `báo cáo nghiên cứu github.txt` 01/10 — đều trước phiên A 25/10 (mở 09:34). A không
  khai báo chúng trong `STATUS_A.md` "Đang khai báo sửa". ⇒ A không đụng.
- Kiểm chéo khẳng định: `backend/evaluation/full_corpus_judge_prompt.md:16` đúng là "không chấm citation hay độ
  bám nguồn" (dùng trong `run-experiment` và `de_xuat_cho_du_an.md` mục 6).
- Không mở file `*sealed*`, `knowledge-base-hue/evaluation/`, `.env*`; không gọi API trả phí; không chạy pytest.

## 2. Tiêu chí nghiệm thu

| # | Tiêu chí (KE_HOACH) | Kết luận | Bằng chứng |
|---|---|---|---|
| 1 | Mỗi thay đổi có căn cứ; không thêm cơ chế ngoài danh sách | **PARTIAL** | W1–W9 đều có căn cứ (bảng User `KE_HOACH.md:10-14`, sự cố S1–S8 `SO_CAI_TIEN_CACH_LAM.md:28-37`). Nhưng sổ có I1, I2 (`SO_CAI_TIEN_CACH_LAM.md:22-23` → `Session_Prompt.md:141-143`, `WORKFLOW.md:48-49`) không có trong bảng W1–W9 của `KE_HOACH.md:18-28` ⇒ F3. Không thấy cơ chế mới phức tạp ngoài danh sách (I1/I2 là dời luật có sự cố) |
| 2 | Không mâu thuẫn luật gốc; luật không nằm hai chỗ; skill ≤ ~100 dòng | **PARTIAL** | Không thấy mâu thuẫn (D chỉ ghi `STATUS_D.md` khớp `WORKFLOW.md` §3.2; "A tự sửa thì người khác kiểm" khớp `Session_Prompt.md` §4; `improve-workflow` nhường luật gốc `SKILL.md:11-12`). `AGENTS.md:14-22` chép lại 6 luật kèm trỏ, nhưng trỏ sai mục ⇒ F4. `run-experiment` 113 dòng (> ~100) ⇒ F5; `improve-workflow` 58 dòng |
| 3 | Agent không phải Claude Code làm theo được | **PASS** (có minor F6) | Mọi luật ở Markdown thường (`AGENTS.md`, `session_prompt/`, `skills/*/SKILL.md`); `CLAUDE.md` chỉ là `@AGENTS.md`; `.claude/settings.json` có dòng chữ tương ứng (`AGENTS.md:15`, `Session_Prompt.md` §5); hook ở tầng git, `#!/usr/bin/env bash`, mode 755. AGY có đọc `AGENTS.md` không: chưa kiểm (sổ tự ghi `SO_CAI_TIEN_CACH_LAM.md:19`) |
| 4 | Hook thử bằng lệnh thật ≥ 4 chặn + ≥ 4 qua; settings JSON hợp lệ | **PARTIAL** | Ngưỡng số đạt (mục 4: 9 ca chặn đúng, 10 ca qua đúng), `jq -e . .claude/settings.json` OK, repo thật `git config --get core.hooksPath` = `.githooks`. Nhưng 1 lỗ hổng ngược với hành vi W5 đã ghi ⇒ F1 (major); 1 lỗ hổng ngoài phạm vi ghi ⇒ F2 |
| 5 | Repo public: diff không lộ dữ liệu; `data/` không bị stage | **PASS** | Quét 407 dòng (file mới + dòng `+` của file sửa): 0 lần tên dự án khác, 0 dạng secret (chỉ có chính mẫu regex trong hook), 0 đường dẫn `/home/...` mới; đường dẫn `data/...` chỉ là tên thư mục private của hue_rag; không có câu Golden / câu kín / nội dung corpus; không gì staged; `git check-ignore` xác nhận `data/`, `knowledge-base-hue/`, `gửi chatgpt/`, `.aws/`, `.env*` bị ignore |
| 6 | `git diff --check` sạch; file tracked mới có trong `Project_Status.md` §7 | **PASS** | `git diff --check` rc=0, không output; file mới chưa track: 0 dòng có khoảng trắng cuối, đều kết thúc bằng `\n`. `Project_Status.md` §7 (dòng 150, 158-160) có `AGENTS.md`/`CLAUDE.md`, sổ, `improve-workflow`, `.githooks/pre-commit`, `.claude/settings.json`; đợt nằm trong `report_agent/README.md` |

## 3. Findings

### F1 — major — hook bỏ qua mọi dòng thêm mới có nội dung bắt đầu bằng `++ `

- Vị trí: `.githooks/pre-commit:23` (`grep -vE '^\+\+\+ '`).
- Yêu cầu: W5 (`KE_HOACH.md:24`) "chặn … secret, tên dự án khác ở dòng thêm mới"; tiêu chí 4.
- Bằng chứng: ca E1 (dòng `++ <tên dự án khác> note`) và E3 (dòng `++ AKIA…` 16 ký tự) đều **commit được** trên repo
  tạm. Dòng nội dung `++ x` thành `+++ x` trong diff nên bị bộ lọc dòng tiêu đề file loại ra, trước cả kiểm secret.
- Tác động: lỗ hổng của chính lớp rào cho việc không đảo ngược được (lộ lên repo public). Hiếm gặp, nhưng dễ xảy
  ra khi dán một đoạn diff / patch vào report.
- Tiêu chí đóng: chỉ loại đúng dòng tiêu đề file (ví dụ `grep -vE '^\+\+\+ (b/|"b/|/dev/null)'`, hoặc
  `git diff --cached --dst-prefix=…` với tiền tố riêng rồi lọc theo tiền tố đó); chạy lại E1, E3 phải bị chặn,
  P1–P10 vẫn qua.

### F2 — minor — tên dự án khác chỉ nằm ở tên file thì không bị chặn

- Vị trí: `.githooks/pre-commit:13-15, 32`.
- Yêu cầu: tinh thần luật cứng 2 (`AGENTS.md:16`); W5 chỉ ghi "dòng thêm mới" nên không phải sai hành vi đã hứa.
- Bằng chứng: ca E2 (file rỗng `notes/<tên>.md`) commit được.
- Tác động: tên đường dẫn lên lịch sử public.
- Tiêu chí đóng: áp mẫu tên dự án khác cho cả `$staged` (một dòng), hoặc ghi rõ giới hạn này ở `Project_Status.md` §8.

### F3 — minor — I1, I2 có trong sổ nhưng không có trong kế hoạch; W2, W9 không có dòng trong sổ

- Vị trí: `SO_CAI_TIEN_CACH_LAM.md:15-24` ↔ `KE_HOACH.md:18-28`.
- Yêu cầu: tiêu chí 1 "không thêm cơ chế ngoài danh sách".
- Bằng chứng: I1 (`Session_Prompt.md:141-143`, luật nghiên cứu ChatGPT dời từ memory) và I2 (`WORKFLOW.md:48-49`)
  không có ID W nào; ngoài ra `WORKFLOW.md:46` mở rộng danh sách governance chỉ A sửa (`AGENTS.md`, `.githooks/`,
  `.claude/settings.json`) cũng không ghi ở đâu. Sổ không có dòng W2 (gộp vào W1) và W9 (chỉ một phần thành I3).
- Tác động: kế hoạch được duyệt và sổ không khớp nhau ⇒ người duyệt không thấy đủ thay đổi. Bản thân các thay
  đổi hợp lý (dời luật có sự cố S3, S7 — đúng nấc 1 của `improve-workflow`), không phải over-engineering.
- Tiêu chí đóng: thêm I1, I2 và dòng `WORKFLOW.md:46` vào bảng `KE_HOACH.md` (hoặc gộp vào W9), và sổ ghi W2/W9
  hoặc nói rõ là gộp.

### F4 — minor — `AGENTS.md` trỏ "chi tiết `Session_Prompt.md` §4–§6" nhưng nhiều luật không ở đó

- Vị trí: `AGENTS.md:14`.
- Yêu cầu: tiêu chí 2 (chỗ phụ chỉ trỏ — phải trỏ đúng).
- Bằng chứng: luật 3 (câu kín) không có trong `Session_Prompt.md` (grep "sealed / câu kín" chỉ ra
  `Project_Status.md`, `CURRENT_HANDOFF.md`); luật 4 (`uv run`) ở §10; luật 6 ở §2 (`Session_Prompt.md:38-40`);
  "không commit chi tiết dự án khác" trong luật 2 không có ở §5.
- Tác động: Codex/AGY đọc `AGENTS.md` trước tiên sẽ tìm sai chỗ; luật câu kín và dự án khác thực chất chỉ có bản
  đầy đủ ở handoff / status.
- Tiêu chí đóng: trỏ từng luật đúng mục (§2, §5, §10, `Project_Status.md` §8…), hoặc đưa luật câu kín / dự án khác
  vào `Session_Prompt.md` §5 để `AGENTS.md` chỉ cần trỏ một chỗ.

### F5 — minor — `run-experiment` 113 dòng, vượt mức ~100 của tiêu chí 2

- Vị trí: `skills/run-experiment/SKILL.md` (`wc -l` = 113, +34 dòng trong đợt).
- Tiêu chí đóng: rút về ~100 (ví dụ gộp các gạch đầu dòng "kiểm người chấm" / "câu có số" ở §2), hoặc User chấp nhận
  ghi rõ lý do vượt.

### F6 — minor — vài chỗ chỉ Claude hiểu hoặc thiếu bước tiếp theo

- `.githooks/pre-commit:7` "xem memory dự án" — memory Claude, Codex/AGY không có ⇒ đổi thành `AGENTS.md` luật 2 /
  `Project_Status.md` §8.
- `WORKFLOW.md:29` "phải in .githooks" nhưng không nói làm gì nếu không in ⇒ thêm "không thì chạy
  `git config core.hooksPath .githooks` và báo trong báo cáo mở phiên".
- Tiêu chí đóng: hai dòng trên được sửa.

### F7 — minor — trỏ hỏng và file thử còn sót

- `CURRENT_HANDOFF.md:17` "commit cuối ghi trong `sessions/STATUS_A.md`", nhưng `STATUS_A.md` bản mới đã bỏ mục
  "Commit cuối phiên" ⇒ thêm lại khi commit đợt này.
- Ở gốc repo còn file `.env.denytest` (bị ignore; tên cho thấy là file thử luật deny của W5 — người kiểm không mở).
  `WORKFLOW.md` §8: dọn file tạm ⇒ A xác nhận rồi xóa.
- Sổ ghi "Thử trên repo tạm 12/12 đúng" (`SO_CAI_TIEN_CACH_LAM.md:18`) nhưng không có bảng ca / lệnh ⇒ không tái lập
  được; có thể trỏ sang bảng mục 4 của review này thay vì con số trơn.
- Tiêu chí đóng: ba điểm trên được xử lý.

### Ngoài phạm vi (ghi ngắn, không vào correction)

- File tracked có sẵn từ trước (không thuộc diff) vẫn nhắc tên dự án khác, ví dụ `Session_Prompt.md` §10 và một dòng
  trong `report_agent/README.md`. Đã biết, đang chờ User quyết (mục "15 file" của phiên trước). Hook không chặn dòng
  có sẵn, nhưng sẽ chặn nếu ai sửa đúng dòng đó (đã ghi ở `Project_Status.md:188-190`).
- `.gitignore` mẫu `data/` không neo gốc nên mọi thư mục con tên `data/` (ví dụ `docs/data/`) cũng bị ignore — có từ
  trước, không do đợt này.

Không có blocker. Một major (F1).

## 4. Cách người kiểm chạy lại thật — phép thử hook

Repo tạm `/tmp/rv_hook_16038` (`git init`), chép `.githooks/pre-commit` và `.gitignore` của repo thật,
`git config core.hooksPath .githooks`. Commit gốc (dùng `--no-verify` chỉ để dựng trạng thái): `docs/a.md`,
`docs/old_mention.md` (có tên dự án khác), `docs/b.md`, `docs/to_move.md`, `data/leak.md`, `data/out.md` (add -f).
Mỗi ca: stage → `git commit` → ghi kết quả → `git reset --hard` về gốc. Tên dự án khác được dựng trong shell từ hai
mảnh, không ghi nguyên văn ở đây. Dọn `/tmp` xong (kiểm `ls -d /tmp/rv_*` = 0).

| Ca | Thao tác | Kỳ vọng | Thực tế |
|---|---|---|---|
| B1 | file mới `gửi chatgpt/2026-10-25/tìm thông tin/yêu cầu 1.md` (dấu cách + tiếng Việt), `add -f` | chặn | chặn ✓ (in đúng đường dẫn) |
| B2 | `git mv docs/to_move.md data/moved.md` (đổi tên vào `data/`) | chặn | chặn ✓ |
| B3 | file `docs/ghi chú mới.md`, dòng mới có tên dự án khác viết HOA và viết hỗn hợp | chặn | chặn ✓ |
| B4 | dòng mới dạng AWS access key `AKIA` + 16 ký tự | chặn | chặn ✓ (không in nội dung key) |
| B5 | `backend/.env.production` (thư mục con), `add -f` | chặn | chặn ✓ |
| B6 | dòng mở đầu khóa riêng OpenSSH (dạng `BEGIN … PRIVATE KEY`, viết liền) | chặn | chặn ✓ |
| B7 | `git commit -a` sau khi nối tên dự án khác vào file tracked | chặn | chặn ✓ |
| B8 | `knowledge-base-hue/evaluation/x.json`, `add -f` | chặn | chặn ✓ |
| B9 | dòng mới dạng `sk-proj_` + 22 ký tự | chặn | chặn ✓ (không in nội dung key) |
| E1 | dòng nội dung bắt đầu `++ ` + tên dự án khác | chặn | **qua ✗** (F1) |
| E3 | dòng nội dung bắt đầu `++ ` + dạng AWS key | chặn | **qua ✗** (F1) |
| E2 | file rỗng tên `notes/<tên dự án khác>.md` | chặn (theo tinh thần luật) | **qua ✗** (F2, ngoài phạm vi W5 đã ghi) |
| P1 | `git rm` file tracked có chứa tên dự án khác | qua | qua ✓ |
| P2 | `git rm data/leak.md` (dọn file private lỡ track) | qua | qua ✓ |
| P3 | sửa file: chỉ xóa dòng chứa tên dự án khác | qua | qua ✓ |
| P4 | `git mv data/out.md docs/out.md` (đưa ra khỏi `data/`) | qua | qua ✓ |
| P5 | `data_notes.md` ở gốc; `docs/data/x.md` (`add -f`, chạy lại riêng vì `.gitignore` bỏ qua) | qua | qua ✓ |
| P6 | `docs/.environment.md`, `.envrc_note.md` | qua | qua ✓ |
| P7 | file `báo cáo mới.md` chứa `sk-learn` (ngắn) và `akia…` chữ thường | qua | qua ✓ |
| P8 | file nhị phân `img.png` có chuỗi tên dự án khác bên trong (`--numstat` = `- -`, git coi là nhị phân) | qua (hook thiết kế bỏ nhị phân) | qua ✓ |
| P9 | nội dung thường của hue_rag | qua | qua ✓ |
| P10 | chép nguyên nội dung hook vào `docs/hook_copy.sh` (mẫu không tự khớp) | qua | qua ✓ |

Tổng: ca phải chặn **9/12 chặn đúng** (9/11 nếu không tính E2 ngoài phạm vi), ca phải qua **10/10 qua đúng**.

Kiểm khác: `jq -e . .claude/settings.json` hợp lệ; `git config --get core.hooksPath` (repo thật, chỉ đọc) = `.githooks`;
`git diff --check` sạch.

## 5. Giới hạn hoặc phần chưa chạy

- Không kiểm hành vi thật của luật deny `Read(./.env*)` trong Claude Code (không được mở `.env*`); không biết đường
  dẫn `./` hiểu theo thư mục nào khi Claude Code mở ở thư mục con.
- Không kiểm Codex / AGY có tự đọc `AGENTS.md` không (cần mở agent đó).
- Không kiểm memory Claude (I3) vì memory nằm ngoài repo.
- Không đối chiếu từng con số trong `de_xuat_cho_du_an.md` với report gốc (chỉ kiểm mục 6); đây là đề xuất, chưa
  phải quyết định, sẽ được quyết ở gate tương ứng.

## 6. Decision và bước tiếp theo

**changes_requested** — vì F1 (lỗ hổng một dòng trong rào an toàn). A sửa F1 và các minor F2–F7 trong một lượt (hoặc
phản biện bằng bằng chứng). Kiểm lại: chạy lại E1, E3 (phải chặn), E2 nếu sửa F2, và P1–P10 (phải qua); với F3–F7
chỉ cần đọc lại dòng đã sửa. Bằng chứng dùng lại được: tiêu chí 3, 5, 6 (nếu phần sửa không thêm dòng nhắc dữ
liệu private). Phần sửa là governance do A làm ⇒ vẫn cần người khác kiểm lại phần đổi.

## Vòng 2 (10:32 25/10/2026)

Phạm vi: chỉ các chỗ A sửa theo F1–F7, cùng ranh giới vòng 1 (đọc repo thật; ghi chỉ ở `/tmp`; không sealed / `.env`
/ paid). Trạng thái lúc kiểm: chưa có gì staged; `git diff --check` sạch; `core.hooksPath` = `.githooks`; `jq` OK.

| F | Kết luận | Bằng chứng |
|---|---|---|
| F1 | **đóng** | `.githooks/pre-commit:25-26` dùng `awk` chỉ lấy dòng `+` trong thân hunk (sau `@@`, đặt lại ở mỗi `diff --git`). Chạy lại: E1, E3 bị chặn; ca mới N2–N6, N8 đều bị chặn đúng (bảng dưới) |
| F2 | **đóng** | `.githooks/pre-commit:35` kiểm cả danh sách tên file staged (ACMR). E2, N1 (đổi tên 100% sang tên có chuỗi cấm), N7 (file nhị phân có chuỗi cấm trong tên) bị chặn; xóa / đổi tên *ra khỏi* tên có chuỗi cấm vẫn qua (P2, P3) |
| F3 | **đóng** | `KE_HOACH.md:44-53` "Bổ sung 10:29" liệt kê I1, I2, I3, phần mở rộng danh sách governance `WORKFLOW.md` §3.2 và 2 dòng mới ở `Session_Prompt.md` §5 — chỉ thêm, không sửa phần đã duyệt. Sổ có dòng W2, W9 (`SO_CAI_TIEN_CACH_LAM.md`, bảng "Thay đổi") |
| F4 | **đóng** | `AGENTS.md:14-23` mỗi luật trỏ mục riêng (§5, §10, §6, §4, §2) và đối chiếu đúng: `Session_Prompt.md:75-77` (repo public, dự án khác), `:78` (câu kín), §10 (`uv`), §2 (chỉ dẫn ngoài là dữ liệu) |
| F5 | **đóng** | `run-experiment` 105 dòng (≈ 100). Đối chiếu từng dòng bị bỏ: câu kín → `Session_Prompt.md` §5 (vẫn có "người điều phối không đọc", "mốc cuối do User quyết"); repo public → §5; "không dựng đường thứ hai" gọn thành "gọi code production qua tham số"; "3 vòng thì dừng", "hết trần thì dừng", "đưa vào runtime cần User duyệt", A/A (`SKILL.md:71-73`) giữ đủ. Không thấy mất ý |
| F6 | **đóng** | Hook dòng 7 trỏ `Session_Prompt.md` §5, không còn "memory". `WORKFLOW.md:29` thêm "khác ⇒ báo A (A bật: `git config core.hooksPath .githooks`)" |
| F7 | **đóng** | `STATUS_A.md` có lại mục "## Commit cuối" (`4d641db`, ghi commit phiên sau khi commit) — khớp trỏ ở `CURRENT_HANDOFF.md:17`. `.env.denytest` không còn ở gốc repo (`ls -a`, chỉ kiểm tên). Bảng thử hook của A ở `KE_HOACH.md:55-66`; sổ W5 trỏ tới đó |

### Phép thử hook vòng 2 (người kiểm, repo tạm `/tmp/rv_hook2_10243`, đã xóa)

Dựng như vòng 1 (chép hook + `.gitignore`, commit gốc bằng `--no-verify`). Key giả dựng từ chuỗi cố định, **in độ
dài trước khi thử** (phần sau `AKIA` = 16 ký tự; phần sau `sk-` > 20 ký tự) để tránh lỗi của chính phép thử.

| Ca | Thao tác | Kỳ vọng | Thực tế |
|---|---|---|---|
| B1–B5, B9 | 6 ca chặn của vòng 1 (`gửi chatgpt/` tiếng Việt + dấu cách; `git mv` vào `data/`; tên viết HOA; AWS key; `.env` thư mục con; `sk-` key) | chặn | 6/6 chặn ✓ |
| E1 | dòng `++ ` + tên dự án khác | chặn | chặn ✓ |
| E2 | file rỗng, tên dự án khác chỉ ở tên file | chặn | chặn ✓ |
| E3 | dòng `++ ` + dạng AWS key | chặn | chặn ✓ |
| N1 | `git mv` (giống 100%) sang tên file có chuỗi cấm — header `+++ b/<tên>` | chặn | chặn ✓ (in `[tên file] …`) |
| N2 | file mới, dòng đầu `++<tên>` | chặn | chặn ✓ |
| N3 | dán diff: dòng nội dung `+++ b/<tên>.md` | chặn | chặn ✓ |
| N4 | nội dung giả `diff --git a/x b/x` và `@@ … @@` rồi một dòng có tên | chặn | chặn ✓ |
| N5 | dòng cuối không có newline chứa tên | chặn | chặn ✓ |
| N6 | dòng CRLF chứa tên | chặn | chặn ✓ |
| N7 | file nhị phân có chuỗi cấm trong tên file | chặn | chặn ✓ |
| N8 | chèn AWS key vào giữa một file đã có | chặn | chặn ✓ |
| P1 | xóa file có tên trong nội dung | qua | qua ✓ |
| P2 | xóa file có chuỗi cấm trong tên file | qua | qua ✓ |
| P3 | đổi tên file có chuỗi cấm sang tên sạch | qua | qua ✓ |
| P4 | chỉ xóa dòng có tên | qua | qua ✓ |
| P5 | chỉ đổi mode (`chmod +x`) file có tên trong nội dung | qua | qua ✓ |
| P6 | dòng `++` và `++ i; counter` sạch | qua | qua ✓ |
| P7 | `docs/data/x.md`, `data_notes.md`, `docs/.environment.md` (`add -f`) | qua | qua ✓ |
| P8 | `sk-learn`, `akia…` chữ thường, tên file tiếng Việt | qua | qua ✓ |
| P9 | `git mv data/out.md docs/out.md` | qua | qua ✓ |
| P10 | chép nguyên nội dung hook | qua | qua ✓ |

Tổng: ca phải chặn **17/17 chặn đúng**, ca phải qua **10/10 qua đúng**. Thông báo các ca secret không in nội dung key
(đếm 0 lần chuỗi key trong output B4, B9, E3, N8).

Finding mới: không có. Ghi chú ngoài phạm vi (không vào correction): `Session_Prompt.md` §10 có từ trước vẫn nêu tên
một dự án khác, giờ trái với dòng mới ở §5 cùng file ("file tracked chỉ nói 'một dự án khác của User'") — thuộc nhóm
"15 file" đang chờ User quyết.

Giới hạn vòng 2: như vòng 1 (deny `Read(./.env*)`, Codex/AGY đọc `AGENTS.md`, memory I3 — chưa kiểm).

**Kết luận vòng 2: `ready_for_user_confirmation`.** F1–F7 đều đóng, không có finding mới. Việc đổi governance do A làm
⇒ A trình User kết quả, bằng chứng, giới hạn trên; User xác nhận rồi A commit/push.
