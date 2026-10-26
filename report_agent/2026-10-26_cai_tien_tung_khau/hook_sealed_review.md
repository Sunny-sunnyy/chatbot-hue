# Review: hook pre-commit quét câu kín (B45)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-23`)
Date: 2026-10-26 21:21 +0700 (`date`)
Canonical guide: `CURRENT_HANDOFF.md` mục "Việc giao phiên tối 26/10", dòng B45; User duyệt quét câu kín 21:1x; `Session_Prompt.md` §5 (giữ mù)
Thay đổi được kiểm: working tree chưa commit — `git diff .githooks/ session_prompt/Project_Status.md` (3 file, +14 / −4)

## 1. Phạm vi đã review

- Đã đọc exact diff và cả hai file `.githooks/overlap_scan.py`, `.githooks/pre-commit`.
  - `overlap_scan.py` thêm vòng đọc `question` + `reference_answer` của mọi `*sealed*.jsonl` dưới `knowledge-base-hue/evaluation/`, nhãn
    `sealed`.
  - Hai chỗ chữ trong `pre-commit` thêm "câu kín".
  - `Project_Status.md` §8 ghi phạm vi quét mới.
  - Diff chỉ có đúng những thay đổi trên, không có gì ngoài phạm vi.
- Kiểm theo rủi ro: (1) chặn nhầm trên file tracked; (2) ca dương mù; (3) commit từ worktree không symlink; (4) hook có in nội dung không;
  (5) lý do bỏ `sources` / `*sealed*.md`; (6) chỗ còn hở.
- **Giữ mù:** script tạm `/tmp/b45_probe.py` tự đọc câu kín và chỉ in số đếm / nhãn / số dòng. Script ghi file thử vào worktree thử, rồi
  đã xóa (worktree `/tmp/b45_wt` gỡ bằng `git worktree remove --force`; `/tmp/b45_probe.py`, `/tmp/b45_hook.out` đã xóa). B không đọc nội
  dung câu kín; report này không ghi tên file tracked nào.

## 2. Findings

**m-1 (minor) — câu kín ngắn hơn cửa sổ 40 ký tự không bao giờ bị bắt.**
- Vị trí: `.githooks/overlap_scan.py`, hàm `add` (cửa sổ `WINDOW = 40`). Câu < 40 ký tự sinh 0 gram.
- Bằng chứng: trong 55 câu hỏi kín khác nhau (7 file × 36 dòng, gồm các bản cũ), **15 câu dài 21–38 ký tự** (trung vị 36). Đáp án kín:
  0 câu ngắn.
- Tác động: chép nguyên một câu hỏi kín ngắn vào report tracked thì hook không chặn, mà đó đúng là loại lộ đã xảy ra 25/10.
- Đo thêm:
  - hiện **0** file tracked chứa nguyên một trong 15 câu này;
  - nếu thêm phép khớp nguyên câu (chuỗi con sau `norm`) cho câu kín < 40 ký tự thì báo nhầm trên file tracked hiện tại = 0.
- Tiêu chí đóng: A chọn một trong hai.
  - (a) Thêm khớp nguyên câu cho câu kín < `WINDOW`: vài dòng; ca dương / âm như §3.
  - (b) Giữ như cũ và ghi giới hạn vào comment + `Project_Status.md` §8 ("câu kín < 40 ký tự không quét").

**m-2 (minor) — số "báo nhầm" trong comment khác số B đo; kết luận không đổi.**
- Vị trí: comment trong `overlap_scan.py` ("báo nhầm 85–263 dòng tracked mỗi file").
- Bằng chứng (B đo, cùng cửa sổ, trên mọi file text tracked):
  - trường `sources`: 416 dòng;
  - 7 file `*sealed*.md`: 635 / 446 / 122 / 0 / 110 / 92 / 94 dòng.
- Tác động: chỉ là chữ; quyết định bỏ hai nguồn này vẫn đúng.
- Tiêu chí đóng: sửa số trong comment, hoặc ghi "hàng trăm dòng", hoặc ghi rõ cách A đếm.

Quan sát, không phải finding:
- 72 / 252 dòng `*sealed*.jsonl` là dòng ghi thay đổi (`changed`, `line` số nguyên, `realism`, `reason`), không có `question`.
  `row.get(...) or ""` bỏ qua chúng đúng cách. Trường `reason` (66 dòng ≥ 40 ký tự) không được quét. B không đọc nên không biết `reason`
  có trích câu hỏi không. Nếu quét thì báo nhầm hiện tại = 0 dòng (đo). A cân nhắc có thêm hay không; B không đề xuất bắt buộc.
- Gram câu kín trùng gram Golden / kho thì giữ nhãn cũ (`setdefault`). Dòng vẫn bị chặn, chỉ khác nhãn in ra. Chấp nhận được.

## 3. Cách người kiểm chạy lại thật

- **Cấu trúc + câu ngắn:** `uv run --project /home/minhhieu/hue_rag python -I /tmp/b45_probe.py stats` và `short`. Nạp module hook thật
  bằng `importlib` từ `.githooks/overlap_scan.py` của working tree.
- **Chặn nhầm:** `tracked`, gọi `scan.hits` thật trên mọi file text tracked: 572 file, 5 file nhị phân bỏ qua. Mất 9,1 s; hook thật chỉ
  quét dòng stage nên nhanh hơn.
- **Ca dương mù trong worktree không symlink:**
  1. `git worktree add --detach /tmp/b45_wt HEAD`, rồi chép 2 file hook của working tree vào (HEAD chưa có thay đổi). Worktree có 0 symlink.
  2. Script ghi `b45_probe_note.md` gồm 5 dòng: (1) chữ thường; (2) nguyên một câu hỏi kín; (3) một đáp án kín có chữ thêm trước / sau;
     (4) câu hỏi kín ở dạng NFD + nhân đôi khoảng trắng; (5) trường `sources` (thiết kế: không quét).
  3. `git add`, rồi chạy `overlap_scan.py --staged` và `bash .githooks/pre-commit` trong worktree. Không commit.

## 4. Kết quả quan sát (lần chạy mới, 21:1x)

| Kiểm | Kết quả | Đạt |
|---|---|---|
| Chặn nhầm `sealed` trên file tracked | **0 file / 0 dòng** (khớp A). Cùng lượt: `corpus` 80 file / 960 dòng, `golden_a` 1 dòng = 80 report lịch sử User chọn để nguyên (câu 4) — hook chỉ quét dòng thêm mới nên không chặn | ✓ |
| Ca dương `--staged` | `{'sealed': [2, 3, 4]}`, exit **3** — bắt cả 3 dạng (nguyên câu, có chữ thêm, NFD + khoảng trắng); dòng 5 `sources` không bị cờ | ✓ |
| Hook đầy đủ trong worktree không symlink | exit **1**, dòng "CHẶN — … Golden / kho / câu kín (số dòng + nhãn …)"; kho đọc từ working tree chính (`MAIN_ROOT`) | ✓ |
| Hook in nội dung? | đầu ra 3 dòng, chỉ tên file thử + nhãn + số dòng; kiểm máy: 30 ký tự đầu của 3 dòng thử **không** có trong đầu ra | ✓ |
| Tốc độ dựng gram (kể cả câu kín) | ~0,4 s (`stats`); gram `sealed` 1.140 | ✓ |
| Lý do bỏ `sources` / `*sealed*.md` | sẽ báo nhầm 416 dòng / 0–635 dòng mỗi file ⇒ bỏ hợp lý (m-2: số khác comment) | ✓ |

## 5. Giới hạn hoặc phần chưa chạy

- Không thử commit thật (chỉ chạy hook trực tiếp sau `git add`). Đường gọi hook bởi git (`core.hooksPath`) không đổi so với bản đã review
  26/10 nên không chạy lại.
- Ca dương chỉ dùng 1 câu hỏi + 1 đáp án (máy chọn câu đầu đủ dài). Chưa thử mọi câu, nhưng cùng một hàm `add` cho mọi dòng.
- Không đọc nội dung câu kín nên không đánh giá được chữ trong `reason` (quan sát §2).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation**, 0 blocker / 0 major. Phần User duyệt (quét `question` + `reference_answer` câu kín) chạy đúng: chặn ca dương,
0 chặn nhầm, không in nội dung, chạy được từ worktree không symlink. A quyết m-1 (thêm khớp nguyên câu cho câu kín ngắn, hoặc ghi giới hạn)
và m-2 (sửa số trong comment) trước khi commit. Nếu A sửa m-1, B kiểm lại phần sửa: chạy lại ca dương với một câu ngắn + `tracked`.

## Vòng 2 — kiểm phần A sửa (2026-10-26 21:25 +0700, `date`)

Decision vòng 2: **ready_for_user_confirmation** — m-1, m-2 **đóng**; 0 finding mới.

Phần sửa (`git diff .githooks/overlap_scan.py`, working tree):
- **m-1:** thêm `short_questions()`. Câu hỏi Golden + câu kín dài 15 ≤ len < 44 ký tự (sau `norm`) được dò **nguyên câu** trong dòng.
  `hits()` nhận thêm `shorts`: thử gram 40 ký tự trước, rồi mới thử câu ngắn. Mỗi dòng vẫn chỉ ghi một nhãn như cũ. `main()` dựng cả hai.
- **m-2:** comment ghi lại số B đo. `reason` không quét (A: không phải câu hỏi / đáp án) — B đồng ý, giữ đơn giản.
- `grep` toàn repo (trừ `.venv`): không file nào khác import `hits` của hook ⇒ đổi chữ ký hàm không làm hỏng chỗ gọi khác. Bản sao riêng
  `data/tools/overlap_scan.py` độc lập, không đổi.

Kiểm lại (script tạm `/tmp/b45v2/probe.py`, chỉ in số / nhãn, **đã xóa**; nạp module hook thật của working tree):

| Kiểm | Kết quả | Đạt |
|---|---|---|
| Tập câu ngắn | `golden_q` 18, `sealed` 17. Câu < 15 ký tự: Golden 0, câu kín 0 ⇒ ngưỡng dưới 15 không bỏ sót câu nào hiện có. Câu kín < 40 ký tự: 15 (khớp vòng 1); 0 câu kín ngắn trùng Golden | ✓ |
| Chặn nhầm trên mọi file text tracked | `corpus` 80 file / 960 dòng, `golden_a` 1 — **giống hệt vòng 1**; `sealed` 0, `golden_q` 0 ⇒ câu ngắn không thêm dòng báo nhầm nào | ✓ |
| Ca dương mù (chế độ quét file, cùng hàm `hits` như `--staged`) | file thử 5 dòng ⇒ `{'sealed': [2, 3], 'golden_q': [4]}`, exit **3**. Dòng 2 là câu kín ngắn nhất (21 ký tự) chèn giữa câu; dòng 3 là câu đó ở dạng NFD + nhân đôi khoảng trắng; dòng 4 là câu Golden ngắn (29 ký tự) có chữ đứng trước. Dòng 5 (nửa câu kín ngắn) **không** bị cờ, đúng thiết kế "nguyên câu" | ✓ |
| Tốc độ | dựng gram + câu ngắn 0,29 s | ✓ |

Ghi chú, không phải finding:
- Câu dài 40–44 ký tự vốn đã bị bắt qua gram ở vị trí 0. Ngưỡng `< WINDOW + 4` làm hai cách bắt chồng lên nhau ở đoạn này, vô hại.
- Câu ngắn chỉ bị bắt khi chép **nguyên câu**: chép một phần, hoặc sửa vài chữ, thì không bị bắt. Đây là giới hạn chấp nhận được với một
  rào bằng máy; luật giữ mù ở `Session_Prompt.md` §5 vẫn là rào chính.
- `--staged` trong worktree không symlink không chạy lại: đường đó đã đạt ở vòng 1, và vòng 2 chỉ đổi `hits` / `main`, là phần dùng
  chung cho cả hai chế độ quét.
