# Review: governance vòng 9 — W30 (hook cảnh báo giờ ước), W31 (WORKFLOW §9.2), I6 (2 bẫy ra Project_Status §8)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-32`) · Date: 13:24 28/10/2026 (`date`)
Canonical guide: `session_prompt/SO_CAI_TIEN_CACH_LAM.md` mục W30, W31, I6 (User duyệt cả ba 13:20 28/10/2026, theo sổ)
Đối tượng: commit `25f23ae` — `.githooks/pre-commit` (+8), `session_prompt/WORKFLOW.md` §6 + §9.2, `session_prompt/Project_Status.md` §8, sổ cải tiến. 0 USD.

## 1. Phạm vi đã review

- `git show 25f23ae` cho 4 file governance (đọc hết diff); đọc thêm toàn bộ hook để biết `$added` lấy gì.
- Thử hook bằng **commit thật** trong worktree tạm (`git worktree add --detach /tmp/c_gov9_wt HEAD`, `core.hooksPath=.githooks`). Một file thử 12 dòng: giờ ước đúng dạng, giờ thật,
  sha hex, chữ `HH:Mx` trong luật, và các biến thể. Xong thì `git worktree remove --force`. Không tạo nhánh. Commit thử nằm ở HEAD tách rời, không thuộc nhánh nào.
- Không đụng file của A. Không sửa hook.

## 2. Findings

Không có blocker hay major.

**m-1 — Mẫu hook chỉ bắt đúng một dạng giờ ước; vài biến thể rẻ để thêm vẫn lọt.**
- Vị trí: `.githooks/pre-commit:61`, mẫu `(^|[^0-9])[0-2][0-9]:[0-5]x($|[^0-9A-Za-z])`.
- Bằng chứng (lần thử §4): bắt được `12:3x`, `09:5x`, `12:1x–12:3x`, `(23:5x)`. Lọt: `12:3X` (x hoa), `9:3x` (giờ một chữ số), `12:xx`.
  Giờ ước trông như giờ thật (ví dụ ghi 11:36 trong khi `date` là 11:25 — bẫy C gặp 28/10) thì **không** máy nào bắt được.
- Tác động: nhỏ, vì hook chỉ cảnh báo, và dạng hay gặp nhất đã bắt được. Nhưng sổ ghi W30 là rào "bằng máy" cho họ lỗi này. Thực ra chỉ dạng có chữ x được rào; dạng giờ trông như thật vẫn chỉ
  dựa vào luật chữ ở WORKFLOW §6.
- Tiêu chí đóng, chọn một:
  - nới mẫu thành `(^|[^0-9])[0-2]?[0-9]:([0-5][xX]|xx)($|[^0-9A-Za-z])` rồi chạy lại 12 dòng thử ở §4: thêm 3 dòng lọt thành bắt, 5 dòng âm vẫn im;
  - hoặc giữ mẫu, nhưng sổ (cột W30) ghi một câu: "chỉ bắt dạng HH:Mx; giờ ước dạng giờ thật vẫn dựa vào luật chữ".

**m-2 — Cảnh báo in nội dung dòng nhưng không in tên file; số "dòng diff #" khó dò.**
- Vị trí: `.githooks/pre-commit:64` (`cut -c1-160 | sed 's/^/  dòng diff #/'`).
- Bằng chứng: `#N` là số thứ tự trong `$added` của **mọi** file gộp lại, không phải số dòng trong file; dòng in ra cũng không kèm tên file. Ở lần thử chỉ có 1 file nên dò được.
  Commit governance thường gồm 4–6 file. Khối secret và khối quét trùng cố ý **không** in nội dung. Khối này in ≤ 160 ký tự, nên một dòng vừa có giờ ước vừa trùng Golden / kho sẽ bị
  in chữ ra terminal (máy cục bộ, không lên git ⇒ mức nhỏ).
- Tiêu chí đóng: in `<file>:<số dòng trong file>` thay cho nội dung, ví dụ lấy từ `git diff --cached -U0` theo từng file, hoặc `git grep --cached -nE <mẫu> -- <file staged>` rồi lọc dòng
  thêm mới. Hoặc ghi lý do giữ như hiện tại, ví dụ "nội dung giúp sửa nhanh; chấp nhận in cục bộ".

Ghi nhận (không phải finding):
- **Không báo nhầm** ở giờ thật (`12:30 28/10/2026`), sha hex, `0x1F`, chữ `HH:Mx` trong chính luật WORKFLOW, `112:3x`, `12:3xy`. Báo nhầm duy nhất là tỉ lệ `10:3x` — chấp nhận
  được, vì chỉ cảnh báo.
- Hook **không chặn**: commit thử đi qua, exit 0. Cảnh báo vẫn hiện cả khi `git commit -q`. Thứ tự đúng: cảnh báo nằm sau quét trùng, trước dòng kết luận `fail`.
- **WORKFLOW §6** (dòng giờ): thêm "28/10 ~7 lần ⇒ hook cảnh báo (W30)" và luật "giờ quyết định của User không có dấu giờ ⇒ ghi giờ A ghi nhận bằng `date`" — rõ, khớp sổ.
- **WORKFLOW §9.2** (W31): dòng nằm đúng mục "Giao việc", ngay sau đoạn "Session rảnh". Nội dung khớp đề xuất trong sổ: lượt đo latency đang chạy ⇒ không chạy lượt trả phí, việc nặng CPU,
  quét / build Qdrant; A ghi vào mục giao. Sự cố gốc là của C (28/10, C tự khai ở review C80) — mô tả đúng.
- **Project_Status §8** (I6): 2 bẫy nằm đúng mục "Bẫy kỹ thuật đã biết", cạnh bẫy worktree / `uv` cùng họ. Bẫy log dùng chung còn kèm chuyện "gỡ worktree xóa luôn log" — đúng, có ích.
- **"Dời" chưa trọn:** `STATUS_A.md:18` vẫn còn bẫy `--env-file`, và chính dòng đó có giờ ước `09:3x` (dòng cũ, hook chỉ xét dòng thêm mới nên không nhắc). Để A quyết khi viết lại STATUS kết
  phiên. C không sửa file của A.
- Sổ: W29 ⇒ `đang dùng`; W30 / W31 / I6 ⇒ `đang thử`, ghi "User duyệt cả ba 13:20 28/10/2026" — khớp commit.

## 3. Cách người kiểm chạy lại thật

```bash
W=/tmp/c_gov9_wt; git worktree add --detach $W HEAD && cd $W && mkdir -p tmp_c
# 12 dòng: A1 "12:3x" · A2 "09:5x" · A3 "12:1x–12:3x" · A4 "(23:5x)" · A5 "12:30 28/10/2026" · A6 sha hex + "0x1F" · A7 "`HH:Mx`"
#          A8 "12:3X" · A9 "9:3x" · A10 "12:xx" · A11 "112:3x" và "12:3xy" · A12 tỉ lệ "10:3x"
git add tmp_c/t.md && git commit -q -m "test W30 (throwaway)"; cd - && git worktree remove --force $W
```

## 4. Kết quả quan sát

| Dòng thử | Mong đợi | Hook | Khớp |
|---|---|---|---|
| A1–A4 (giờ ước dạng HH:Mx) | cảnh báo | cảnh báo 4 / 4 | ✓ |
| A5 giờ thật, A6 sha / hex, A7 chữ `HH:Mx`, A11 dính số / dính chữ | im | im 4 / 4 | ✓ |
| A12 tỉ lệ `10:3x` | im | cảnh báo | báo nhầm nhẹ (chấp nhận) |
| A8 `12:3X`, A9 `9:3x`, A10 `12:xx` | (nên) cảnh báo | im | m-1 |
| commit có đi qua không | đi qua (không chặn) | exit 0, commit tạo | ✓ |
| quét trùng vẫn chạy | có | `tmp_c/t.md 0 trùng` | ✓ |
| dọn | không còn worktree / nhánh | `git worktree list` không còn `/tmp/c_gov9_wt`; danh sách nhánh không đổi | ✓ |

## 5. Giới hạn hoặc phần chưa chạy

- Không thử commit nhiều file (m-2 suy từ đọc code). Không thử trên Codex / AGY (hook ở tầng git nên giống nhau).
- Không kiểm lại sự kiện gốc của I6 (`--env-file` chạy nền): chỉ đọc, đối chiếu với STATUS_A.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** W30 / W31 / I6 áp đúng như sổ ghi. m-1, m-2 là cải tiến nhỏ của hook: A làm khi tiện, hoặc ghi giới hạn vào sổ.
