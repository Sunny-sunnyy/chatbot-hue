# Review B41 — rebase B1 (context 10 + NFC) lên `main` mới (A, 2026-10-26 20:50 +0700)

Người kiểm: A. Đối tượng: nhánh `p82-b1` `811d25d` (gốc `43cdcd6`), report §7 `phase_8_2_b1_implementation.md` trên nhánh. 0 USD.

## Cổng tối thiểu
- `git log main..origin/p82-b1`: 2 commit (`e1e16b3` code B1, `811d25d` report). `git diff main...origin/p82-b1`: 8 file — code chỉ còn
  `max_context_documents` 5 → 10 (settings + validator + test pin), `normalize_query` (NFC + kiểm rỗng cũ) gọi đầu `search`, 1 test NFC, `experiments/phase_8_2/b1.py`
  (harness đo, không vào đường chạy API). Không còn `minilm` / `REPO_ROOT` / Rep B; import trần đúng gói 1b. Không thấy thay đổi ngoài phạm vi.

## Bằng chứng
- T1 (158 câu giống byte `cefb2d1ad609`), T5, test 4 file (= `main` + 1 test NFC; failed / error cũ cần key): B chạy mới, A dùng như chỉ mục.
- **T2 đổi cách đo:** không gọi model; bắt đầu vào SDK (thay `_execute_agent`) và so với cây cũ `f23d396` 176 / 176 + đối chứng dương `main` ctx 5 khác
  0 / 176. Đây không phải mock làm PASS cho hành vi model — chỉ chứng minh **đầu vào** model không đổi; `input_tokens` là suy bắc cầu (B ghi rõ).
  A quyết: **không chạy lượt sinh có phí lúc này** (User duyệt bước này 0 USD). Bằng chứng model thật cho context 10 sẽ có ở cổng ổn định khi merge
  (sau B0): `/chat` thật, 1 câu trong kho + 1 câu ngoài kho.

## Finding
- **m1 (minor, ngoài phạm vi B41):** comment sai "import này cũng đưa gốc repo + backend/ vào sys.path" còn ở 3 file `experiments/phase_8_1/` trên
  `main` — A ghi việc nhỏ, sửa ở lần sửa code sau (không chặn).

## Kết luận
`ready_for_user_confirmation` cho phần rebase. **Merge vào `main` chỉ sau B0** (User đọc cặp mù) + áp luật dừng B0 (spec 8.2) + cổng ổn định.
