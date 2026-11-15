# Bảng lưu trú v5 (gộp một cơ sở lặp) + `scripts/commit_push.sh` (W81) — C, 15:14 15/11/2026

Hai việc nhỏ A giao đầu phiên chiều 15/11, hai nhánh riêng. Tiền: 0 USD (không gọi model / API có phí).

## 1. Bảng lưu trú v5 — nhánh `p9-luu-tru-v5` @ `ea0e82c`

- **Vấn đề:** bảng v4 có hai dòng cùng tên, cùng toạ độ, cùng trang ảnh (danh mục gốc ghi hai mã, hai số nhà kề nhau) ⇒ trang Chỗ ở và thẻ khách sạn có thể ra hai thẻ cho một nơi. User chốt gộp; A chốt giữ dòng hạng cao hơn (1 sao).
- **Làm:** script `data/luu_tru_v5_2026-11-15/tools/dung_bang_v5.py` đọc v4, bỏ đúng dòng kia, ghi **file mới** v5 (md5 `34836e7c1438`; v4 `c98ca8c19889` không sửa). Diff tracked: 1 dòng `backend/config/settings.yaml` (`lich_trinh_bang_luu_tru`).
- **Kết quả [Chạy]:**

| Kiểm | Kết quả |
|---|---|
| Số cơ sở · có ảnh · tên lặp | 137 ⇒ 136 · 58 ⇒ 57 · 0 |
| v5 so từng dòng với v4 (`tools/so_v4_v5.py`) | bớt đúng 1 dòng, mọi dòng khác giống hệt |
| Ô "Nơi ở" của lịch, 3.840 khung × 4 mức hạng | đổi 0 / 15.360 (hai dòng này chưa từng vào lịch) |
| Trang Chỗ ở (`trang_cho_o` trên bảng cấu hình) | tên cơ sở đó hiện 1 lần |
| Danh sách tên trùng địa danh (`dung_trung.py` trên v5) | file sinh ra không đổi |
| `test_luu_tru_lich.py` + `test_the_khach_san.py` | 16 passed không env (12,7 s) · 16 passed có `--env-file` (10,9 s) |

- **Không chạy:** test rộng, Playwright, lượt có phí — nhánh chỉ đổi dữ liệu bảng, 0 lịch đổi (`Session_Prompt.md` §8).
- **Còn lại:** file ảnh của dòng bị bỏ thành mồ côi trong `frontend/public/anh/khach_san/` (để nguyên); danh sách chừa của Docker nháp (trong `data/`) còn trỏ v4 ⇒ checklist deploy; số 137 / 58 trong `bai_hoc/` và sổ ghi việc sửa sau khi merge.

## 2. `scripts/commit_push.sh` — nhánh `p9-commit-push` @ `609c7ac`

- **Vấn đề:** 15/11 ba lần một session báo "đã push" khi hook pre-commit đã chặn commit.
- **Làm (32 dòng bash):** `scripts/commit_push.sh "<lời commit>" <file>…` ⇒ `git add` đúng các file đó ⇒ in `git diff --cached --stat` ⇒ commit ⇒ push nhánh hiện tại ⇒ đọc sha từ origin bằng `git ls-remote` ⇒ in `ĐÃ PUSH <sha> origin/<nhánh>`. Mọi đường hỏng in `CHƯA PUSH — <lý do>` và thoát 1 (sai cú pháp: thoát 2).
- **Ba quyết định nhỏ của C (trong phạm vi):** (a) vùng stage đang có sẵn thứ khác ⇒ dừng, vì không thì commit dính file ngoài danh sách; (b) commit bị chặn ⇒ script gỡ các file vừa stage (cây làm việc giữ nguyên) để chạy lại được; (c) file đã xoá vẫn truyền được nếu git đang theo dõi.
- **Chạy thử 0 USD [Chạy]** (`data/commit_push_2026-11-15/thu.sh`, kho tạm + remote bare trong `/tmp`): **ĐÚNG 15 / 15** — đường thường (chỉ file truyền vào được commit, sha origin = sha máy) · thiếu tham số · truyền thư mục · file không có · file không đổi · vùng stage có sẵn · hook pre-commit chặn (không commit mới, vùng stage trống, file giữ nguyên) · hook pre-push chặn (origin vẫn ở commit cũ) · file đã xoá · nhánh mới chưa có trên origin · HEAD tách rời.
- **Chạy thật [Chạy]:** chính script commit + push nhánh của nó qua hook thật của repo ⇒ in `ĐÃ PUSH 609c7ac origin/p9-commit-push`.
- **Chưa thử:** push bị từ chối vì origin đi trước (non-fast-forward) — cùng đường "push lỗi" với ca hook pre-push; push từ worktree `/tmp` trong auto mode của session khác.
- **Sau merge (A):** `WORKFLOW.md` §5 đã ghi "báo sha chỉ bằng dòng script in" — dòng đó là `ĐÃ PUSH <sha> origin/<nhánh>`.
