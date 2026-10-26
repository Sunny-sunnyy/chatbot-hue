# Review: sửa luật theo sổ cải tiến (W14 + W18, W16, W17, W19, W20) — trọng tâm hook W16

Decision: **changes_requested** (0 blocker / 1 major / 4 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-b5`)
Date: 2026-10-26 20:59 +0700 (`date`)
Canonical guide: `session_prompt/SO_CAI_TIEN_CACH_LAM.md` (W14–W20); `AGENTS.md` luật 2; `Session_Prompt.md` §5
Implementation report: không có. Căn cứ là tin nhắn A (20:5x) + diff A đã stage trên `main` `2d56193`.

## 1. Phạm vi đã review

- `git diff --cached` (5 file): `.githooks/overlap_scan.py` (mới, blob `fdfcdb0`), `.githooks/pre-commit` (+13),
  `session_prompt/Session_Prompt.md` §9 (W19), `session_prompt/WORKFLOW.md` §6 (W20) + §9.2 (W17), `skills/propose-options/SKILL.md` §1
  (W14 + W18). Có thêm `git diff session_prompt/SO_CAI_TIEN_CACH_LAM.md` (cột trạng thái).
- `git diff --cached --check`: sạch.
- Ngoài phạm vi, không có thay đổi lạ. Lúc 20:59, chỗ stage của working tree chung **không còn**: cả 5 file về dạng " M" / "??".
  Nội dung không đổi (blob `overlap_scan.py` vẫn `fdfcdb0`, `pre-commit` vẫn +13). C không chạy lệnh ghi index nào ở working tree
  chung. Mọi `git add` / `reset` của C chạy trong worktree `/tmp/c_w16`. A kiểm lại trước khi stage và commit.
- Mức rủi ro: hook là rào bằng máy cho mọi agent. Hai rủi ro chính: chặn nhầm (làm kẹt commit) và không chặn (lộ dữ liệu private trên repo
  public). Phần tài liệu W14 / W17 / W18 / W19 / W20 chỉ kiểm tính nhất quán.

## 2. Findings

### M-1 (major) — Commit từ worktree `/tmp/…` không có symlink kho thì hook **im lặng bỏ qua** quét trùng

- **Vị trí:** `.githooks/pre-commit`, phần thêm mới, dòng `if [ -f knowledge-base-hue/evaluation/golden_full_corpus.jsonl ]`.
  `.githooks/overlap_scan.py:18-19` (`ROOT` / `GOLDEN` theo vị trí của script).
- **Yêu cầu:** W16: "rào bằng máy cho mọi agent", chỉ bỏ qua ở clone public. `AGENTS.md` luật 2.
- **Bằng chứng (chạy thật, §3 ca 2):** worktree `/tmp/c_w16` có diff của A, **không** symlink `knowledge-base-hue/`, stage một file có 1 dòng
  kho ⇒ `.githooks/pre-commit` **exit 0**, 0,018 s, không in gì. Cùng worktree khi **có** symlink ⇒ exit 1, báo đúng dòng 4.
- **Tác động:** worktree riêng là cách làm chuẩn của B / C khi code song song (`WORKFLOW.md` §3.2, §9.7). Mục B41 tối nay cũng commit từ
  `/tmp/b_p82b1`. Bẫy ở `Project_Status.md` §8 dặn **gỡ** symlink khi xong. Như vậy commit report từ worktree đúng là chỗ rào im lặng tắt,
  và người commit không biết.
- **Cách sửa C đã thử (worktree tạm, không sửa file governance):** đọc kho / Golden từ working tree chính, giống cách hook đã lấy `.venv`.
  - `pre-commit`: đưa `main_root=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")` lên trước `if`, rồi kiểm
    `[ -f "$main_root/knowledge-base-hue/evaluation/golden_full_corpus.jsonl" ]`.
  - `overlap_scan.py`: thêm `MAIN_ROOT` từ `git rev-parse --path-format=absolute --git-common-dir` (cha của nó),
    `KB = MAIN_ROOT / "knowledge-base-hue"`, `GOLDEN = KB / "evaluation/golden_full_corpus.jsonl"`, vòng quét kho dùng `KB.rglob`.
    `ROOT` giữ nguyên cho `backend` import và `git diff` (phải chạy ở worktree).
  - Kết quả thử: worktree **không** symlink ⇒ exit 1, dòng 4. Stage rỗng ⇒ exit 0. Working tree chính quét file ⇒ 0 trùng, exit 0.
- **Tiêu chí đóng:** chạy lại ca 2 ở §3 (worktree không symlink, 1 dòng kho đã stage) ⇒ exit 1 và báo đúng số dòng. Ca âm (5 file của A) vẫn
  exit 0.

### m-1 (minor) — Lỗi chạy máy quét bị báo thành "dòng trùng"

- **Vị trí:** `.githooks/pre-commit`, `if ! uv run … overlap_scan.py --staged; then echo "CHẶN — dòng thêm mới trùng…"`.
- **Bằng chứng:** `PATH=/usr/bin:/bin` (không có `uv`) ⇒ `uv: command not found`, exit 1 kèm câu "dòng thêm mới trùng >= 40 ký tự".
  Python lỗi (import, JSON) cũng ra exit 1, giống hệt khi có trùng.
- **Tác động:** hook chặn đúng hướng an toàn, nhưng câu báo sai làm người commit đi tìm dòng trùng không có.
- **Tiêu chí đóng:** câu báo nói "trùng **hoặc** quét lỗi — xem dòng trên". Hoặc script trả mã riêng khi có trùng (ví dụ 3), còn hook báo
  "quét lỗi" với mã khác.

### m-2 (minor) — Sổ cải tiến: trạng thái ngoài vòng đời, cột đo cũ

- **Vị trí:** `session_prompt/SO_CAI_TIEN_CACH_LAM.md`, các dòng W14 / W16 / W17 / W18 / W19 / W20.
- **Bằng chứng:** đầu sổ định nghĩa vòng đời `đề xuất` → `đang thử` → `đang dùng` / `gỡ` / `bác`. Các dòng mới ghi **`áp dụng`**, không nằm
  trong vòng đời đó. Cột đo của W14 / W16 / W19 / W20 vẫn ghi "User duyệt phiên sau". W16 vẫn ghi "hiện quét ~10–30 s"; đo thật là 0,41 s.
- **Tiêu chí đóng:** đổi trạng thái thành `đang thử` (User duyệt 20:4x 26/10). Cột đo ghi điều sẽ xem ở vòng sau, ví dụ W16: "có lần chặn
  nhầm / bỏ sót nào; thời gian hook".

### m-3 (minor) — Chỗ còn trỏ máy quét cũ, chỗ chưa nhắc hook mới

- **Vị trí:** `session_prompt/CURRENT_HANDOFF.md:176` (cổng ổn định bước 5: "quét `data/tools/overlap_scan.py` trước commit").
  `session_prompt/Project_Status.md` §8, dòng hook: chỉ nhắc tên dự án khác, chưa nhắc quét trùng; chưa có bẫy "worktree" nếu M-1 chưa sửa.
  Bản `data/tools/overlap_scan.py` (private) nay trùng chức năng với bản tracked.
- **Tiêu chí đóng:** cổng ổn định trỏ `.githooks/overlap_scan.py` (hook tự chạy; quét cả file bằng `uv run python .githooks/overlap_scan.py
  <file>`). `Project_Status` §8 thêm nửa dòng về quét trùng. Bản `data/tools/` ghi "thay bằng bản tracked" hoặc bỏ.

### m-4 (minor, chữ) — Nhãn file có khoảng trắng dính dấu tab

- **Vị trí:** `.githooks/overlap_scan.py`, `staged_added_lines`, `current = line[6:]`.
- **Bằng chứng:** với đường dẫn có khoảng trắng, git thêm `\t` ở cuối dòng `+++ b/…`. Hook in ra `bảng lỗi.md\t {…}`. Phát hiện và số dòng
  vẫn đúng (§3 ca 3).
- **Tiêu chí đóng:** `line[6:].rstrip("\t")`. Hoặc để nguyên vì không ảnh hưởng việc chặn.

### Ngoài phạm vi (ghi cho A / User, không phải correction)

- **Câu kín không được quét:** máy quét bỏ `evaluation/` (gồm `*sealed*`) và `_source-dumps/`. W16 duyệt phạm vi "Golden / kho" nên khớp
  duyệt. Nhưng `AGENTS.md` luật 2 liệt kê cả câu kín. Cho hook đọc file câu kín (chỉ in số dòng) là quyết định của User, vì luật giữ mù §5.
- **Giới hạn của cách quét:** quét từng dòng. Đoạn chép trải hai dòng, mỗi dòng ngắn dưới ~44 ký tự, có thể lọt (chỉ khớp khi rơi đúng
  bước 5 ký tự). Chép kho nhưng bỏ `**` định dạng vẫn bị bắt nếu còn ≥ 44 ký tự liền (§3 ca 6).
- **Nhánh tạo trước commit này** (ví dụ `p82-b1`) chạy hook cũ của chính nhánh đó, vì `core.hooksPath` tương đối với worktree. W16 chỉ có
  hiệu lực sau khi rebase.
- **Chặn nhầm trên cây hiện tại:** quét cả file 219 file tracked (backend, guides, session_prompt, skills, `bao_cao_he_thong`,
  `report_agent`, `*.py`) chỉ có **1 dòng** bị cờ, ở `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_golden_fix_review.md:93`. Đó là
  dòng A đã biết (trùng tên file kho). Hook chỉ chặn nếu ai đó sửa đúng dòng này.

### Phần tài liệu (W14, W17, W18, W19, W20)

Khớp nội dung User duyệt ghi trong sổ, đặt đúng chỗ sổ ghi ("Nơi sửa"), không mâu thuẫn luật khác. W20 có mẫu lệnh chạy được. Không có
finding.

## 3. Cách người kiểm chạy lại thật

Worktree riêng `git worktree add --detach /tmp/c_w16 HEAD` (`2d56193`), áp `git diff --cached` của A bằng `git apply --index`. Hook gọi trực
tiếp `.githooks/pre-commit`; không commit. Dòng kho dùng để thử dương là **một dòng của một file kho** (không phải Golden), giữ ở `/tmp`, đã
xóa. File thử nằm trong worktree tạm, đã gỡ bằng `git worktree remove --force` (`git worktree list` không còn `c_w16`).

| Ca | Thiết lập | Kết quả |
|---|---|---|
| 1 âm | 5 file của A đã stage (cùng các ca dương) | cả 5 "0 trùng" |
| 2 dương, worktree **không** symlink kho | thêm file mới 5 dòng, dòng 4 là dòng kho | **exit 0**, không in gì (M-1) |
| 2b dương, worktree **có** symlink | như ca 2 | exit 1, `{'corpus': [4]}`, **0,408 s**; không tạo `.venv` trong worktree |
| 3 tên có dấu + khoảng trắng | file mới `report_agent/zz c tést/bảng lỗi.md`, dòng 2 là dòng kho | exit 1, dòng 2 (nhãn dính `\t` — m-4) |
| 4 nhiều hunk | file tracked 63 dòng: chèn 1 dòng sạch sau dòng 3, dòng kho sau dòng 10 và ở cuối | báo dòng 12 và 66 — đúng số dòng file mới |
| 5 đổi tên + sửa | `git mv` một template, thêm dòng kho ở cuối (R073) | báo dòng 29 = dòng cuối — đúng |
| 6 dòng bắt đầu `++`; chép bỏ định dạng | dòng nội dung `++ <dòng kho>`; dòng kho bỏ `*`/`_`; đoạn 43 ký tự tách 2 dòng | `++` bắt đúng; bỏ định dạng bắt đúng; 2 mảnh 43 ký tự: bắt 1, sót 1 |
| 7 index tạm (`commit -a` / `commit <path>`) | `GIT_INDEX_FILE=/tmp/…` + `read-tree HEAD` + `add` file dương | exit 1, dòng 4 — hook đọc đúng index tạm |
| 8 thiếu `uv` | `PATH=/usr/bin:/bin` | exit 1 với câu "dòng trùng" (m-1) |
| 9 clone không có kho | như ca 2 (không có `knowledge-base-hue/`) | bỏ qua, exit 0 — đúng thiết kế clone public |
| 10 thử cách sửa M-1 | sửa 2 file trong worktree tạm, không symlink | exit 1, dòng 4; stage rỗng exit 0; working tree chính quét file exit 0 |
| 11 chặn nhầm | `uv run python …/overlap_scan.py` cả file trên 219 file tracked | 1 dòng (đã biết) |

Lệnh Python của C đều chạy bằng `uv run` (hook), trừ ba script nhỏ dựng file thử và sửa file tạm. Ba script này chạy bằng `python3`, không
đụng code dự án.

## 4. Kết quả quan sát

- Đọc hunk `-U0` đúng số dòng ở mọi ca thử: nhiều hunk, đổi tên, dòng `++`, đường dẫn có dấu / khoảng trắng (`core.quotePath=false`).
  Index tạm cũng đúng. Thời gian 0,41 s, không đáng kể.
- Lỗ hổng duy nhất ảnh hưởng an toàn là M-1, ở worktree không có symlink kho. Cách sửa hai chỗ đã thử đạt trong worktree tạm.
- Phần tài liệu: không có finding.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy `git commit` thật (A dặn không commit). Hook được gọi trực tiếp với index tương ứng; ca 7 mô phỏng index tạm của `commit -a`.
- Không thử agent khác (Codex / AGY) commit. Hook là shell + `uv`, như nhau với mọi agent có `uv` trên `PATH` (ca 8: thiếu `uv` thì chặn).
- Không thử repo có submodule hoặc `git commit --amend`. `--amend` vẫn chạy pre-commit trên index; chưa đo.

## 6. Decision và bước tiếp theo

**changes_requested:** sửa M-1, rồi chạy lại ca 2 và ca âm. m-1 → m-4 sửa cùng lượt hoặc để A quyết (minor, không chặn). Sửa xong, C kiểm
lại phần sửa: ca 2, 2b, 1 và một ca dương ở working tree chính, dùng lại bằng chứng ca 3–7 vì phần đọc hunk không đổi. Việc mức trung bình
(rào governance, User đã duyệt nội dung) ⇒ A đóng và báo User.

## 7. Kiểm lại phần sửa — 2026-10-26 21:06 +0700 (`date`)

Decision (vòng 2): **ready_for_user_confirmation** (0 blocker / 0 major / 0 minor còn mở; 1 ghi chú chữ). Việc mức trung bình ⇒ A đóng, báo User.

Phần sửa đọc lại: `git diff --cached` 5 file trên `main` `a7b61bb`. `overlap_scan.py` blob `105376c`: `MAIN_ROOT` / `KB` / `GOLDEN`,
`HIT_EXIT = 3`, `rstrip("\t")`. `pre-commit`: `main_root` trước `if`, tách mã 3 với mã khác. `git diff --cached --check` sạch. Phần chưa stage:
sổ cải tiến, `CURRENT_HANDOFF.md`, `Project_Status.md` §8.

| Finding | Kiểm lại (chạy thật) | Kết quả |
|---|---|---|
| M-1 | worktree mới `/tmp/c_w16b` (áp diff của A), **không** symlink kho, stage file mới có dòng kho ở dòng 4 | exit 1, `{'corpus': [4]}`, 0,70 s; không tạo `.venv` trong worktree — **đóng** |
| M-1 (âm) | cùng worktree, chỉ 5 file của A | exit 0 |
| M-1 (working tree chính) | `GIT_INDEX_FILE` tạm + `update-index --cacheinfo` blob file dương (không đụng index chung — sau thử vẫn đúng 5 file A đã stage) | exit 1, dòng 4 |
| m-1 | `PATH=/usr/bin:/bin` ⇒ "quét … LỖI (mã 127)"; worktree tạm bỏ `llm/full_corpus_prompt.py` ⇒ `ModuleNotFoundError` + "LỖI (mã 1)" | **đóng** |
| m-2 | sổ: W14 / W16–W20 `đang thử`, cột đo ghi điều xem vòng sau; W16 "đo 26/10: 0,4 s", mô tả exit 3 | **đóng** |
| m-3 | `CURRENT_HANDOFF.md` cổng ổn định (5) và bảng file trỏ `.githooks/overlap_scan.py`; `Project_Status.md` §8 thêm 2 dòng (worktree, "quét LỖI", câu kín / `_source-dumps/` không quét) | **đóng** |
| m-4 | nhãn `bảng lỗi.md` không còn tab | **đóng** |

Dùng lại bằng chứng §3 ca 3–7 (đọc hunk, đổi tên, `++`, index tạm), vì `staged_added_lines` chỉ đổi `rstrip("\t")` ở nhãn.

Ghi chú chữ (không chặn): dòng W15 (`bác`) cột đo vẫn ghi "User duyệt phiên sau; hay để hook làm?". Dòng "Cập nhật lần cuối" của sổ vẫn là 20:54.

Lúc thử có 4 file `backend/` sửa chưa stage trong working tree chung. Đó là việc B44, A đã commit `c813aa6` ngay sau đó; không liên quan W16.
Dọn: worktree `/tmp/c_w16b` đã gỡ, file tạm `/tmp/c_w16b*` đã xóa; object blob thử nằm rời trong `.git/objects` (không gắn ref, gc sẽ dọn).
