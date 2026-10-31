# Review: B103 — tra web bằng Codex vào cách làm (governance của A)

Decision: **changes_requested** (1 major, 4 minor; không có blocker)
Người kiểm: B (Claude Opus 5.5) · Date: 11:27 31/10/2026 (`date`)
Việc được kiểm (chưa commit, working tree `main` `e39d9c7`):

| File | sha256 (12) |
|---|---|
| `scripts/tra_web_codex.sh` (mới, untracked) | `b1216941a659` (khớp handoff) |
| `.claude/settings.json` (diff: thêm `Bash(agy)`, `Bash(agy:*)` vào `deny`) | `a5ac516e320b` |
| `session_prompt/Session_Prompt.md` (diff §9: đoạn "Tra web bằng Codex CLI" + đổi tên đoạn ChatGPT thành "Nghiên cứu lớn qua ChatGPT web") | `263b5f586884` |

Căn cứ: mục "A — tra web bằng Codex vào cách làm" / B103 trong `CURRENT_HANDOFF.md`; tiêu chí thử ở thư mục private của đợt thử 31/10 (tham số Codex đã dùng). File này **không** chép kết quả tra hay nội dung private.

## 1. Phạm vi đã review

- `git status` / `git diff` của 3 file, đọc hết script (61 dòng).
- Đối chiếu tham số với lượt thử đã chấm: `codex --search exec`, `-m gpt-6-luna`, reasoning `high`, `-s read-only`, `--ephemeral` ⇒ **khớp**. Thêm `--skip-git-repo-check`, `-C <thư mục trống>`, `-o`: hợp lý.
- Chạy script **1 lần** với câu công khai nhỏ (đúng quyền B103). Dò bộ cảnh báo lệnh shell bằng 3 cách khác A (W32): đọc định dạng log thật; tìm mẫu trong 5 log Codex có sẵn;
  đọc tài liệu chính thức về đầu ra `codex exec`.
- Thử chặn `agy` chỉ bằng dạng lệnh **không thể** chạy `agy` dù rào có lọt (`false && …`). **Không** chạy `agy` ở bất kỳ dạng nào, kể cả `agy --version`: luật A 10:54 "không gọi
  `agy` dưới bất kỳ hình thức nào" chặt hơn câu "thử bằng lệnh vô hại như `agy --version`" ở mục B103 ⇒ B theo luật chặt hơn và ghi lệch này.

## 2. Findings

### M-1 (major) — bộ cảnh báo lệnh shell chưa từng được thấy bắt đúng một lệnh thật, mà §9 lại dựa vào nó làm rào

- **Vị trí:** `scripts/tra_web_codex.sh:57` — `grep -c -E '^(exec|/bin/bash|bash -lc)' codex.log`. `Session_Prompt.md` §9: "script cảnh báo lệnh shell ⇒ dừng, báo A".
- **Yêu cầu bị ảnh hưởng:** rào cho rủi ro đã ghi trong tiêu chí thử: sandbox `read-only` **không** chặn đọc file ngoài thư mục làm việc (script tự ghi ở dòng 8). Codex đọc file máy
  (kho, `.env`, `~/.codex/auth.json`…) thì nội dung sẽ đi lên OpenAI. `Session_Prompt.md` §6: bằng chứng phải từ lần chạy thật.
- **Bằng chứng:**
  - 5 log Codex hiện có (3 lượt Y1–Y3, lượt thử của A, lượt B103) đều **0** lệnh shell ⇒ chưa có mẫu thật nào cho thấy dòng log của một lệnh shell trông ra sao.
  - B103 cố tình xin Codex chạy một lệnh vô hại (`echo b103`, có ghi là ngoại lệ kiểm thử). Codex **từ chối** vì phần đầu script cấm shell ("theo chỉ dẫn đầu của bạn… không chạy
    shell"). Tốt cho an toàn, nhưng bộ đếm vẫn chưa được kiểm.
  - Đầu ra dạng chữ của `codex exec` **không có tài liệu**. Trang chính thức (`developers.openai.com/codex/noninteractive` ⇒ chuyển sang `learn.chatgpt.com/docs/non-interactive-mode`)
    chỉ nói "Codex streams progress to `stderr`" — không tả định dạng. Regex `^exec` là đoán theo bản hiện tại, có thể đổi giữa các bản (máy đang chạy 0.166.0).
  - Có cách **có tài liệu**: `codex exec --json` ⇒ JSONL. Ví dụ trên trang cho một mục `"type":"command_execution"`, `"command":"bash -lc ls"`; danh sách loại mục gồm "command
    executions, file changes, MCP tool calls, web searches". Lệnh `codex exec --help` của bản đã cài có `--json` ("Print events to stdout as JSONL").
- **Tác động:** nếu regex trượt (đổi định dạng, có tiền tố giờ, hay công cụ đọc file khác shell), script báo "lệnh shell 0". §9 khiến session tin là không có gì bị đọc. Rào hiện chỉ
  còn **lời dặn trong prompt** (lần này Codex làm theo).
- **Tiêu chí đóng (chọn một, A quyết):**
  - (a) đổi sang `--json`, đếm mục `command_execution` (và `file_change`, `mcp_tool_call`) theo trường `type`, rồi kiểm bằng **một** lần Codex chạy lệnh thật trong thư mục trống
    (prompt riêng **không** có dòng cấm shell, ví dụ `echo`). `--json` còn cho số token (`turn.completed.usage`), tức thước 5 của tiêu chí thử;
  - (b) giữ regex nhưng kiểm bằng đúng lần chạy thật như trên;
  - (c) nếu chưa kiểm được: §9 + chú thích script ghi rõ "bộ đếm **chưa kiểm** trên lệnh thật; rào chính là lời cấm trong prompt" — không để câu "script cảnh báo" như một bảo đảm.

### m-1 (minor) — phần đầu script luôn đòi "nghiên cứu chuyên sâu ≥ 20 lượt tìm", trong khi §9 dùng nó cho cả câu tra nhanh

- **Vị trí:** `scripts/tra_web_codex.sh:25-28` ↔ §9 "Dùng cho câu tra nhanh / kỹ thuật cụ thể".
- **Bằng chứng:** câu B103 (một số phiên bản + ngày) chạy **35 s, 12 lượt tìm**; lượt thử của A 28 s, 10 lượt. Không sai, nhưng mọi câu nhỏ đều bị bảo "không phải câu tra nhanh".
- **Tiêu chí đóng:** hoặc ghi một dòng trong §9 "câu nhỏ vẫn chạy kiểu sâu, ~30 s", hoặc tách chế độ (nhanh / sâu). Mặc định đơn giản: chỉ ghi dòng đó.

### m-2 (minor) — Codex nạp thư mục skill cá nhân của User vào ngữ cảnh mỗi lần tra

- **Bằng chứng:** cả 5 log có `skills scan reached its traversal limit (root: …/.codex/skills)` và "Exceeded skills context budget. All skill descriptions were removed and 1183 / 1189
  additional skills were not included in the model-visible skills list" ⇒ một phần **tên** skill vẫn vào ngữ cảnh gửi model. Thư mục đó dùng chung cho mọi dự án của User. `--ephemeral`
  thì hoạt động đúng: không có dòng mới trong lịch sử / phiên của Codex sau các lượt tra (B đếm, 0).
- **Tác động:** dữ liệu ra ngoài thêm (tên skill cá nhân, có thể của dự án khác), tốn ngữ cảnh, và hành vi Codex phụ thuộc cấu hình máy chứ không chỉ phụ thuộc script. Rủi ro thấp
  (cùng tài khoản OpenAI của User), nhưng §9 hứa "yêu cầu chỉ chứa thông tin công khai".
- **Tiêu chí đóng:** A thử tắt skill cho lượt tra (khoá cấu hình của Codex, nếu có — B chưa tra), hoặc ghi giới hạn này trong chú thích script.

### m-3 (minor) — luật "không gọi `agy`" chỉ nằm ở §9, chưa ở danh sách luật cứng của `AGENTS.md`

- **Bằng chứng:** `grep agy AGENTS.md` ⇒ 0. Sub-agent / agent khác chỉ đọc `AGENTS.md` (luật cứng 1–6) sẽ không thấy. Rào máy `.claude/settings.json` chỉ có tác dụng với Claude Code.
- **Tiêu chí đóng:** thêm một dòng luật cứng trỏ §9 (theo luật "cách làm phải dùng được cho mọi agent").

### m-4 (minor) — §9 chưa nói session **không phải** Claude Code làm gì

- **Vị trí:** §9 "mọi session tự chạy `scripts/tra_web_codex.sh`".
- **Tác động:** một session là Codex thì đã có tìm web sẵn (gọi Codex từ trong Codex là thừa). Một session là AGY thì có tìm web của chính nó (User mở, không phải agent gọi `agy`).
  Hiện chưa có dòng nào nói điều này.
- **Tiêu chí đóng:** thêm nửa dòng "session Codex / AGY dùng tìm web sẵn có của mình, vẫn theo luật 'chỉ thông tin công khai' + WebFetch kiểm".

## 3. Đã dò, đúng (không phải finding)

| Khẳng định | Cách B dò | Kết quả |
|---|---|---|
| Script chạy được, ghi đúng chỗ, không ghi đè | chạy 1 lần (`TRA_WEB_TIMEOUT=300`): mã thoát 0, 35 s, 12 lượt tìm, "lệnh shell 0"; tạo `data/tra_cuu_cli/2026-10-31_b103-probe/{yeu_cau_gui.md, ket_qua.md, codex.log, tom_tat.txt}`; thư mục `/tmp/tra_web_codex.*` tự xoá | ✓ |
| Thêm ngày hôm nay + đòi thông tin mới nhất | `yeu_cau_gui.md` có "Hôm nay: **31/10/2026**" | ✓ |
| Kết quả đúng | đáp án phiên bản / ngày phát hành của một gói Python khớp **PyPI JSON API** (`pypi.org/pypi/<gói>/json`), cách kiểm khác trang Codex đã mở | ✓ |
| Codex làm theo lời cấm shell | Codex từ chối `echo b103` và nêu đúng lý do | ✓ (xem M-1: đây là rào **duy nhất** đã thấy chạy) |
| `--ephemeral` không lưu phiên | đếm dòng của script trong lịch sử / chỉ mục phiên Codex = 0; 0 file phiên mới kể từ trước lượt thử | ✓ |
| Log không có mã màu (regex `^` không bị tiền tố màu làm trượt) | `grep -c $'\x1b'` = 0 trên log | ✓ |
| Chặn `agy` qua lệnh ghép | 4 dạng `false && …` (gọi thẳng; qua `env`; đường dẫn tuyệt đối; tiền tố biến môi trường): **đều bị từ chối**. Dạng `bash -c '…'` bị tầng an toàn của auto mode chặn (không phải rõ do luật `deny`) ⇒ B dừng thử, không lách. B không phân biệt được lần từ chối nào do luật `deny`, lần nào do auto mode | ✓ trong giới hạn |
| Tên ngắn kiểm ký tự, đường dẫn `realpath -e`, `set -euo pipefail`, `grep -c … || true` | đọc | ✓ |

**Câu bất biến:** script không đổi hệ thống đang chạy (không chạm `backend/`, Qdrant, kho). Chỉ ghi vào `data/tra_cuu_cli/` và `/tmp` (tự dọn) ✓.

## 4. Giới hạn

- Bộ đếm lệnh shell: **chưa kiểm** trên lệnh thật (M-1). B không chạy thêm Codex ngoài 1 lần được phép.
- Không biết lần từ chối nào trong phép thử `agy` đến từ luật `deny`, lần nào từ auto mode. Session chạy chế độ quyền khác có thể cho kết quả khác.
- Lệch tài liệu: mục B103 cho thử "`agy --version`", luật A 10:54 cấm mọi dạng ⇒ A sửa một trong hai cho khớp.

## 5. Decision

`changes_requested` — A xử lý M-1 (chọn (a) / (b) / (c)) + m-1…m-4 nếu đồng ý. Đây là việc governance (A tự sửa), B kiểm lại phần đổi. Khi đóng M-1 bằng (a) hoặc (b), lần chạy
"Codex chạy lệnh thật" để kiểm bộ đếm cần quyền riêng (1 lần, 0 USD, thư mục trống, lệnh `echo`).

---

# Vòng 2 — kiểm phần A sửa (script `e0dc2d76a86f`, `AGENTS.md` luật 7, §9)

Decision: **ready_for_user_confirmation** (M-1, m-3, m-4 đóng; m-1 giữ có lý do — chấp nhận; 3 ghi chú minor mới, không mở vòng) · Người kiểm: B · Date: 11:34 31/10/2026 (`date`)

## R2.1 Đóng finding vòng 1

| Finding | A sửa | B kiểm (khác cách A) | Đóng? |
|---|---|---|---|
| M-1 | chọn (a): `--json`, đếm mục `command_execution` / `web_search` bằng `jq`; thêm `url_da_mo.txt` (trang Codex thật sự mở); A kiểm bằng 1 lần Codex chạy `echo` thật | (1) chạy script 1 lần (câu công khai nhỏ): mã 0, 14 s, 2 lượt tìm, 1 trang mở, 0 lệnh shell; đáp án khớp **PyPI JSON API** (cả bản tiền phát hành lẫn bản ổn định); `url_da_mo.txt` có đúng URL báo cáo dẫn. (2) đếm loại sự kiện trong log JSON thật lúc 11:30 của A: `item.started` / `item.completed` `web_search`, `agent_message`, `error`, `turn.*` — bộ lọc `select(.type=="item.completed" and .item.type==$t)` khớp dạng thật. (3) chạy **nguyên văn** hàm đếm của script trên input nhỏ tự dựng (xem R2.2) | ✓ về hướng — xem n-1, n-2 cho hai ca biên |
| m-1 | giữ (câu nhỏ ~30 s chấp nhận được; chế độ "nhanh" chưa có nhu cầu) | lượt B vòng 2: 14 s cho câu nhỏ | ✓ chấp nhận lý do |
| m-2 | ghi giới hạn — **chỉ ở `CURRENT_HANDOFF.md`** | `grep skill` trong script và §9: 0 | xem n-3 |
| m-3 | `AGENTS.md` luật cứng 7 | đọc diff | ✓ |
| m-4 | §9 thêm câu cho session Codex / AGY + cách đọc `url_da_mo.txt` | đọc diff | ✓ rõ cho agent không phải Claude |

## R2.2 Ca biên của bộ đếm (logic thuần, input nhỏ, không gọi Codex)

Chép nguyên văn hàm `items()` + dòng đếm `shell_cmds` của script vào `/tmp` (đã xoá), chạy trên 3 file JSONL nhỏ:

| Input | Kết quả | Ý nghĩa |
|---|---|---|
| `item.started` + `item.completed` của một `command_execution` | `shell_cmds=1`, thoát 0 | ✓ ca thường |
| chỉ `item.started` `command_execution` (lệnh đang chạy thì Codex bị cắt do hết giờ / chết) | `shell_cmds=0` | **trượt** — n-1 |
| ca thường + một dòng không phải JSON (dòng cuối bị cắt khi `timeout` giết Codex giữa lúc ghi) | script **thoát mã 5, không in tóm tắt, không in cảnh báo**; lỗi `jq` bị `2>/dev/null` giấu | **lỗi bị giấu** — n-2 |

## R2.3 Ghi chú minor mới (A sửa nhanh; không cần vòng 3 nếu sửa đúng như dưới)

- **n-1:** đếm theo `item.id` trên **cả** `item.started` lẫn `item.completed`, ví dụ
  `jq -r --arg t "$1" 'select((.type=="item.started" or .type=="item.completed") and .item.type==$t) | .item.id' … | sort -u | wc -l`. Lý do thêm: ví dụ trong tài liệu chính thức chính là
  một `item.started` `command_execution`.
- **n-2:** bỏ `2>/dev/null` ở `items()`, hoặc đọc từng dòng bằng `jq -R 'fromjson? // empty'`, để dòng hỏng không làm script thoát lặng lẽ. Khi đã có dòng hỏng thì in cảnh báo
  "log JSON không đọc trọn — xem `codex.jsonl`".
- **n-3:** giới hạn m-2 (Codex nạp thư mục skill cá nhân dùng chung) đang chỉ nằm ở `CURRENT_HANDOFF.md`, mà file này sẽ bị dọn ⇒ thêm một dòng vào chú thích đầu script (hoặc §9).
  Bằng chứng còn: log JSON thật lúc 11:30 có một mục `error` "Exceeded skills context budget…".
- Ghi thêm: log của lần A cho Codex chạy `echo b103` **không còn trên đĩa** (không thấy trong `data/`) ⇒ chú thích script "đã thử 31/10 với `echo` thật" là lời kể, không còn bằng chứng.
  Nếu A còn file thì chép vào `data/tra_cuu_cli/`; không thì giữ như ghi chú (sửa n-1 xong thì bộ đếm khớp đúng dạng trong tài liệu, nên không cần chạy lại).

## R2.4 Decision

`ready_for_user_confirmation` — luồng chính chạy đúng (--json có tài liệu, kiểm thật 2 lần trong review), luật `agy` có ở `AGENTS.md` + §9 + rào Claude Code. n-1, n-2 là hai dòng
code nên sửa trước khi commit (cùng là ca "hết giờ", đúng lúc rào cần nhất); n-3 một dòng chú thích. Lượt chạy của B: `data/tra_cuu_cli/2026-10-31_b103-r2/` (private).

---

# Vòng 3 — kiểm n-1 / n-2 / n-3 (script `dba4d7bdfc40`)

Decision: **ready_for_user_confirmation** (n-1, n-2, n-3 đóng; không còn finding) · Người kiểm: B · Date: 11:39 31/10/2026 (`date`)

- **Phần đổi:** script dòng 10 (giới hạn skills, n-3), 57–64 (đếm theo `item.id` trên `item.started` + `item.completed`, n-1; `jq -R` + `fromjson?`, đếm dòng hỏng + cảnh báo, bỏ
  `2>/dev/null`, n-2). `AGENTS.md` và §9 không đổi so với vòng 2 (cùng 13 dòng diff). `bash -n` sạch; `git diff --check` sạch.
- **Bằng chứng bộ đếm nay có trên đĩa:** log JSON của lần Codex chạy `echo b103` thật (private, `data/…/log/codex_json_echo_test.jsonl`): `item.started` + `item.completed`
  `command_execution` ⇒ đúng dạng tài liệu.
- **B dò bằng input khác 3 input của A** (chép nguyên văn dòng 60–64 vào `/tmp`, đã xoá; không gọi Codex):

  | Input | bad / tìm / shell | Kết quả |
  |---|---|---|
  | log `echo` thật | 0 / 0 / **1** | ✓ |
  | file rỗng (Codex không chạy được) | 0 / 0 / 0, và ở script thật thì `ket_qua.md` rỗng ⇒ thoát 1 | ✓ |
  | dòng cuối bị cắt **ngay giữa** một sự kiện `command_execution` | **1** / 0 / 0 + cảnh báo "số đếm có thể thiếu" | ✓ — lệnh không đếm được nhưng người chạy được báo |
  | log thật 11:30 của A (không lệnh) | 0 / 6 / 0 — giống `tom_tat.txt` cũ | ✓ bất biến: luồng thường không đổi số |
  | dòng JSON hợp lệ nhưng không phải object (`42`, `null`) | 2 / 0 / 1 + cảnh báo; `jq` in lỗi "Cannot index number" ra stderr nhưng số đếm vẫn đúng | chấp nhận — Codex không xuất dạng này; chỉ là tiếng ồn |

- **Decision:** `ready_for_user_confirmation`. Sẵn để A đưa lệnh commit cho User (stage từng file: `scripts/tra_web_codex.sh`, `.claude/settings.json`,
  `session_prompt/Session_Prompt.md`, `AGENTS.md`, file review này). File review không có kết quả tra hay nội dung private.
