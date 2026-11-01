# Review: runbook lượt đo cuối Phase 1–8 (C108)

Decision: **changes_requested** (0 blocker / 3 major / 5 minor) · Người kiểm: B (Claude Opus 5.5) · Date: 12:35 01/11/2026 (`date`)
Bản kiểm (B tự tính sha): `data/do_cuoi_2026-11-01/runbook.md` **`48e084451940`**; `tools/do_cuoi.py` `2ba9593d7a32`, `an_toan_cuoi.py` `3fa3dd9c5d27`, `ngay_cuoi.py` `e2c5768da93d`,
`latency_cuoi.py` `a5894f7f8e92`, `tien_cuoi.py` `6cefac38fd00` (private). Đối chiếu: plan đã duyệt `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` **`ae8d42d520d4`** §2, §3, §5, §6, §8.
0 USD. **Không** chạy `preflight` / `import-truoc` / `check`: các lệnh đó ghi file bằng `write_new` (từ chối ghi đè) vào thư mục của lượt thật ⇒ chạy thử sẽ chặn lượt chạy thật; B tính lại các số trong
bộ nhớ thay vào (§3). Không mở bộ kín (`so_trung_sha.py` không đọc).

## 1. Phạm vi đã review

Trọng tâm A giao: `analyze` (F1–F4, T1–T3, luật A/A), `compare` (A1, A2), cách ghép bộ "trước" (sha), trần tiền cộng dồn; thêm: thứ tự runbook ↔ plan §5, ước tiền ↔ plan §6, điều kiện dừng ↔ plan §8.

**Đạt (đối chiếu được):**
- **Bộ "trước"** (`do_cuoi.py` `import_truoc`): kiểm sha `45487ea1d88a` trước khi chép, chép giống byte + meta. B tính lại trên file nguồn: sha `45487ea1d88a`, meta commit `751b352`, 176 dòng; theo đúng
  logic `check()`: F3 0, F1 0, F4 0, **T3 12** (= mốc 12 / 158; khớp `dot2/analyze.json` T3 `sau` 12), có `wall_ms`, **không** có trường đệm (⇒ `check --arm truoc` tính giá phẳng — đã ghi); lượt cũ cũng
  `concurrency 1` như lượt mới (`wall_ms` so được).
- **T1 / T2** (`analyze`): số câu tụt trên 129 câu số chính ≤ `MAX_DROP = N_AA + 3 = 5` **và** `mean_diff` theo cặp ≥ −0,1 — đúng plan §3.1; câu 500 trích dẫn ⇒ Đủ = Đúng = 1 (như đợt 1 / 2).
  **T3:** từ chối nhầm `sau` ≤ `truoc` + 1 trên 158 câu — đúng.
- **Luật A/A** (plan §11 Q2 PA1): N_AA giữ 2; `AA_near_threshold` = 4 ≤ số tụt ≤ 6 (= "4–5 hoặc vượt 1") ⇒ chỉ khi đó đọc `AA_drops_also_changed_sau_vs_aa`; `khong_lam_hong` **không** dùng A/A để
  đổi kết luận — đúng "chỉ để tách trôi, A trình User".
- **F1 / F2 / F4:** F1 = câu ngoài kho bị trả lời ở `sau` (trừ câu lỗi / 500); F2 = "nói chắc sai" mới (người dùng thấy, Đúng ≤ 3) ở `sau` mà không ở `truoc`, chấm lại mù hai bên trước khi `analyze`
  một lần; F4 = 500 trích dẫn mới — đúng F1–F4 plan §3.1.
- **Chấm mù ba bên** (`export_judge`): gộp câu trả lời trùng chữ, xáo seed, số mục mờ, judge không thấy `map.json`; kiểm md5 Golden = preflight.
- **Trần tiền Golden cộng dồn** (`run`): `spent_usd()` cộng `usd` của mọi `*.meta.json` Golden (trừ `truoc`) lúc bắt đầu + tiền lượt đang chạy; kiểm **trước mỗi câu**; meta ghi ở `finally` (cả khi lỗi).
  Cap 0,11 = ước 0,088 + 25 % (< 50 % luật plan §6).
- **Bộ an toàn** (`an_toan_cuoi.py`): A1 = câu ngoài kho không bị từ chối ở `sau`; A2 vế 1 = P0_sai mới (trong câu `p0_relevant`) ≤ 2; vế 2 = danh sách phải phân loại (i)/(ii)/(iii) bởi người không viết câu
  trả lời; "một trong hai judge"; cổng đối chứng 9 / 10 · ≤ 1 / 5 · tách lô 0; sinh lại 3 lần **hai bên**, mốc trên **`751b352`** worktree riêng + kiểm T1 giống byte (đúng M-1 vòng plan) — `bao_A` khi
  bên "sau" sai nhiều lần hơn mốc.
- **15 câu theo ngày** (`ngay_cuoi.py analyze`): sàn 0 L1 / L2 ("một trong hai judge") trên 12 câu quyết (15 − 3 đối chứng) — đúng plan §3.3; chặn chấm thật nếu judge chưa qua 6 / 6 phiếu kiểm.
- **Thứ tự** runbook ↔ plan §5: ghi trước ⇒ cổng ổn định ⇒ S4 + 22 câu B65 một mình (W31) ⇒ Golden "sau" ⇒ A/A cùng ngày ⇒ an toàn ⇒ ngày ⇒ bộ kín **sau** cùng ⇒ tiền — khớp (bộ kín chạy sau
  để không ai thấy số bộ kín trước khi Golden / an toàn chốt — hợp lý). Không có "thử thêm" (Q3a ⇒ Phase 9).
- `latency_cuoi.py`: kiểm sha bộ 22 câu `bac5c91db005`, đọc log từ offset (chỉ dòng mới), tiền giá đủ từ log, kiểm 23 dòng. `tien_cuoi.py`: trừ dòng trùng của file gộp `<arm>.jsonl` (B kiểm cả ca có
  `--retry`: tổng = pilot + rest + retry, đúng).

## 2. Findings

**M-1 (major) — các lệnh `$G …`, `$A …`, `$S …` ở bước 5–7 không chạy được như viết.**
- Vị trí: `runbook.md` §5 (`G="PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run … python …"` rồi `$G run …`), §6 (`A=…`, `S=…`), §7 (`$A --questions …`).
- Bằng chứng (B chạy thật, bash): `G="FOO_TEST=1 printenv FOO_TEST"; $G` ⇒ `/bin/bash: line 1: FOO_TEST=1: command not found`. Bash chỉ nhận `VAR=giá trị` là gán biến khi nó **viết thẳng** đầu lệnh, không
  khi nó đến từ mở rộng biến ⇒ mọi lệnh Golden / an toàn / ngày dừng ngay ở lần gọi đầu. `G2="env FOO_TEST=1 printenv FOO_TEST"; $G2` ⇒ `1` (chạy).
- Tác động: runbook không thực thi được từ bước 5; người chạy phải tự sửa lúc chạy (dễ sửa khác nhau giữa các lần).
- Tiêu chí đóng: thêm `env` đầu mỗi chuỗi (`G="env PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run …"`) hoặc dùng hàm bash; chạy một lệnh 0 USD qua biến (vd `$G --help`, `$S --help`) cho thấy chạy được.

**M-2 (major) — `ngay_cuoi.py export` ghi xong file rồi văng `NameError`, chặn bước 7.**
- Vị trí: `tools/ngay_cuoi.py:55` `"real": len(qs)` — trong `export()` không có biến `qs` (chỉ có trong `analyze()`).
- Bằng chứng: kiểm tĩnh AST (tên được đọc mà không gán / nhập / định nghĩa trong hàm) ⇒ `export [('qs', 55)]`; các script khác 0 (một báo nhầm ở `latency_cuoi.py:39` là biến `except … as exc`).
  B **không** chạy `export` (nó ghi vào thư mục lượt thật).
- Tác động: `round0.jsonl`, `round1.jsonl`, `round1_map.json` đã ghi xong thì lệnh lỗi; chạy lại bị chặn (`OUT exists`) ⇒ phải xoá tay thư mục giữa lượt đo.
- Tiêu chí đóng: sửa thành số mục thật (vd `sum(src.startswith("real:") for src, _ in items)`); chạy `export` một lần trên **bản sao** đầu vào ở thư mục tạm (`OUT` nhận tham số hoặc biến môi trường) ⇒ exit 0,
  `round1` 26 mục; rồi xoá bản thử.

**M-3 (major) — runbook cho chạy lại câu lỗi kỹ thuật, trái điều kiện dừng của plan; và F3 tính sau khi thay.**
- Vị trí: `runbook.md` §5 ("Câu lỗi kỹ thuật (F3): chạy lại **một** lần đúng câu đó … rồi `merge --retry`"); `do_cuoi.py` `merge(..., retry)` thay dòng lỗi; `analyze` `floors_pass["F3"]` đọc `check_<arm>.json`
  tính trên file **đã gộp** (dòng lỗi đã bị thay).
- Bằng chứng: plan §8 (bản duyệt `ae8d42d520d4`): "**lỗi kỹ thuật / provider (ghi nguyên, không retry ngoài plan)**" nằm trong danh sách "Dừng + báo A"; plan §3.1 sàn F3 "0 lỗi kỹ thuật". Plan không có
  bước chạy lại.
- Tác động: một lỗi provider được "sửa" bằng lần gọi thứ hai và sàn F3 báo qua — đổi thước sau khi thấy lỗi (đúng thứ luật "không retry ngoài plan" chặn).
- Tiêu chí đóng: một trong hai — (a) bỏ bước retry: gặp lỗi ⇒ dừng, ghi nguyên, báo A (đúng plan); hoặc (b) A trình User sửa plan §8 thành luật retry có tên (một lần, đúng câu) **và** `analyze` báo F3
  trên file **trước khi thay** (giữ danh sách câu lỗi gốc) + `replaced_by_retry` vào kết quả. Chọn (b) ⇒ bản plan mới cần duyệt lại sha.

**m-1 — bước 7 chạy bằng Python hệ thống.** `runbook.md` §7 + docstring `ngay_cuoi.py:9`: `python3 -I …` — `Session_Prompt.md` §10: code / script luôn `uv run` trong `.venv` dự án, không system
Python. Tiêu chí đóng: đổi sang `uv run --project /home/minhhieu/hue_rag python -I …` (hoặc `/home/minhhieu/hue_rag/.venv/bin/python -I`).

**m-2 — trần bộ an toàn / câu ngày so bằng tiền giá phẳng, dư quá luật "vượt ước > 50 %".** `an_toan_run.py` ghi `usd` theo `cost_usd` giá phẳng; runbook đặt `--cap 0.015` (ước phẳng 0,0081 ⇒ trần
= +85 %) và ngày `--cap 0.008` (ước phẳng 0,0037 ⇒ +116 %). Plan §6: "Lượt nào vượt ước > 50 % ⇒ dừng". Tiêu chí đóng: cap = ước phẳng × 1,5 (≈ 0,012 và ≈ 0,0056), hoặc ghi rõ đây là trần
cứng còn luật 50 % kiểm tay sau lượt bằng `tien_cuoi.py`.

**m-3 — `analyze` văng lỗi thay vì báo nếu còn dòng lỗi.** Dòng lỗi kỹ thuật không vào lô chấm (`export_judge` bỏ `error`) ⇒ `completeness` / `accuracy` = `None` ⇒ `s[i][m] < t[i][m]` (`do_cuoi.py:302`)
ném `TypeError` khi câu lỗi thuộc 129 câu số chính. Với M-3 (a) lượt đã dừng trước đó nên ít gặp; nhưng nếu muốn có `analyze.json` cho báo cáo ca hỏng thì cần bỏ qua / đánh dấu dòng `None`.
Tiêu chí đóng: tùy C (ghi giới hạn hoặc bỏ qua dòng lỗi có đếm).

**m-4 — ước tiền §10 chưa cập nhật S4 đã đo thật.** Dòng "S4 ≈ 0,014 (ước spec)" — S4 đã chạy 01/11 trên `streaming-final` `6a0c842`: **0,015802 USD** (giá đủ, 64 lần gọi —
`report_agent/2026-10-31_streaming_spec/s4_do_d2_implementation.md`). Nếu dùng lại S4 (bước 3) thì phần này là tiền **đã tiêu**, không còn là ước; ghi commit S4 = `6a0c842` cho điều kiện `git diff`.

**m-5 — bộ kín (bước 8) không có trần tiền riêng.** Các phần khác đều có `--cap`; bước 8 chỉ ghi "≈ 0,01 USD — cộng tay". Tiêu chí đóng: ghi trần (vd 0,015) cho lệnh sinh 40 câu.

**Ghi chú (không phải finding):**
- n-1: §6 dọn worktree mốc dùng `rm /tmp/do_cuoi_moc/data …` — auto mode hay chặn `rm`; đường an toàn đã quen: `unlink` từng symlink rồi `git worktree remove` (`STATUS_B.md` bẫy 31/10).
- n-2: `preflight` / `import-truoc` không chạy thử được (ghi `write_new`) — nếu muốn kiểm trước lượt thật, thêm cờ `--dry` (in, không ghi). Không bắt buộc.

## 3. Cách người kiểm chạy lại thật

- `sha256sum` runbook + 6 script; đọc toàn bộ `runbook.md`, `do_cuoi.py`, `an_toan_cuoi.py`, `ngay_cuoi.py`, `latency_cuoi.py`, `tien_cuoi.py`; `grep add_argument` của `an_toan_run.py` (có `--qids`,
  `--repeat`, `--cap`, `--questions`, `--out` như runbook dùng).
- Bộ "trước" tính lại trong bộ nhớ (Python `.venv`, chỉ đọc): sha / meta / F1 / F3 / F4 / T3 / trường đệm / `wall_ms` / concurrency (§1).
- Ca dò bash cho M-1 (2 dòng, không đụng repo). Kiểm tĩnh AST tên chưa định nghĩa trên 5 script (M-2).
- Đối chiếu nguyên văn plan §8 (M-3), §6 (m-2), §3.1–§3.3 (mục "Đạt").

## 4. Kết quả quan sát

Như mục "Đạt" và bằng chứng từng finding. Logic quyết định (F1–F4, T1–T3, A/A, A1–A2, sàn ngày) **khớp** plan đã duyệt; vấn đề nằm ở **chạy được** (M-1, M-2) và **một điều kiện dừng lệch plan** (M-3).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lệnh nào của runbook (đều ghi vào thư mục lượt thật hoặc có phí); `check()` / F-counts kiểm bằng tính lại trong bộ nhớ.
- Không đọc `an_toan_run.py` / `loi_nang.py` ngoài phần cờ + cách tính `usd` (dùng lại từ đợt 2, đã review khi đó).
- Không review bước bộ kín ngoài chỗ cắm (C không viết, theo plan §3.7).

## 6. Decision và bước tiếp theo

`changes_requested` — C sửa M-1, M-2, M-3 (M-3 (b) cần A / User) + m-1…m-5 tuỳ C, báo sha mới; B kiểm **phần sửa** (dùng lại mục "Đạt" nếu các dòng đó không đổi).

---

# Vòng 2 — kiểm phần sửa (runbook `bdd883bb367c`, `do_cuoi.py` `8045d4fa1572`, `an_toan_cuoi.py` `3c26897afae1`, `ngay_cuoi.py` `dc56bf0016bb`)

Decision: **ready_for_user_confirmation** — M-1, M-2, M-3, m-1…m-5, n-1 đóng · Người kiểm: B · Date: 12:47 01/11/2026 (`date`) · 0 USD. B tự tính sha 4 file (khớp tin C).

| Finding | Kiểm của B | Đóng? |
|---|---|---|
| M-1 | §0 nay là 4 hàm bash `G` / `A` / `S` / `N` có `env`; B **chạy chính đoạn §0** (từ `backend/`, chỉ `--help`) ⇒ in `hàm OK` | ✓ |
| M-2 | `ngay_cuoi.py:56` đếm `real` / `safe` từ `items`; kiểm tĩnh AST lại ⇒ 0 tên chưa định nghĩa ở `ngay_cuoi.py`, `do_cuoi.py`, `an_toan_cuoi.py`; C chạy `export` trên bản sao (`DO_CUOI_DIR`) ⇒ 26 mục | ✓ |
| M-3 | `do_cuoi.py`: không còn `--retry` (`grep` chỉ còn ở docstring + §12); `run` ghi dòng lỗi rồi `stopped_by_error = True` + `break` (:147-149) ⇒ dừng, báo A — đúng plan §8 | ✓ |
| m-1 | `N()` = `uv run --project $R python -I …` | ✓ |
| m-2 | `--cap` an toàn 0,012 · ngày 0,0056 · sinh lại 0,0025 (= ước phẳng × 1,5) — runbook dòng 90, 101, 113 | ✓ |
| m-3 | `analyze` chỉ so câu có điểm ở cả ba bên, báo `main_unscored` (:313) | ✓ |
| m-4 / m-5 / n-1 | S4 `6a0c842` 0,015802 đã tiêu; bộ kín trần 0,015; `unlink` symlink | ✓ |

Câu bất biến kiểm: **thư mục lượt thật chưa bị lượt thử làm bẩn** — `data/do_cuoi_2026-11-01/golden/` chưa có (C chạy thử `preflight` / `import-truoc` trên bản sao `/tmp/c108t`, đã xoá) ⇒ `write_new` của
lượt thật không bị chặn. Logic quyết định (F / T / A/A / A1–A2 / ngày) không đổi so với vòng 1 ngoài phần đã kê ⇒ dùng lại mục "Đạt" vòng 1.
