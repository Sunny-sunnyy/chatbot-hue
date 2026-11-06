# STATUS C — kết phiên 06/11 (12:14 06/11/2026 `date`; ≤ 35 dòng; lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`)

## ĐANG LÀM — phiên tối 06/11 (terminal `hue-rag-42`; A `hue-rag-cc` giao, 21:01 06/11/2026)
- (a) **Harness XONG phần 0 USD — review E vòng 1 changes_requested ⇒ đã sửa 21:27 06/11/2026, chờ E kiểm:** `chay_sua_lich.py` md5 `559ebaf5f81e` (E vòng 2 ready; + n-1 mkdir) (`kiem` Q3 10/10 · Q2 0/42 · ca phá 9/9; chạy thử khoá giả 22 lượt đạt), bộ Q4 `chuoi_q4.jsonl` `d35f8d9c5027`; report C207 §7. A quyết: pilot = S01 + S06; E review (`c207_harness_review.md`, E nhắn C); 3 chỗ tự quyết giữ. Lượt có phí chỉ sau khi `lich_trinh` bật. File đã sửa: `data/phase_9/sua_lich/tools/chay_sua_lich.py` (mới), `data/phase_9/bo_do_sua_lich/chuoi_q4.jsonl` (mới, Q4: TD1–TD5 của B5 + 2 chuỗi an toàn sau lịch), `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §5, file này. Worktree `/tmp/c_sualich` (`p9-sua-lich` `09ddaf9`). 0 USD.
- (b) **B171 XONG phía C (21:29 06/11/2026): ready_for_user_confirmation trên `b0e52f8`** (vòng 2: M-2 + dòng khung tối; 351 test, Q1 228/228, ca dò 0/12 bắt nhầm; ghi nhận tách vế làm lọt thêm 2 dạng — A đã quyết không sửa phần lọt) — `b171_review.md` §8. Worktree `/tmp/c_b171` gỡ được.

- (c) **C208 XONG (21:51 06/11/2026):** `p9-sua-lich` `09ddaf9` ⇒ **`79b3d9c`** trên `main` `d930867` (pushed) — gỡ xung đột B5b, sửa `hoi_toi` (xếp lại + sửa trực tiếp) + 4 test; 411 test, Q1 / Q1m 228/228; sửa nhãn đã thấy S03 / S08 (`c00de07114b5`); harness `559ebaf5f81e` (n-1). E kiểm rebase: **ready**, 0 finding (`c207_harness_review.md` "Vòng 3"). **Chờ User `!`** mô phỏng kín (lệnh ở report C207 §8). Report C207 §8.

- (d) **C209 (22:02 06/11/2026, A giao):** nghiên cứu nguồn dữ liệu đợt 2 giao diện cổng (0 USD, không sửa code / kho) — file: `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md`, `data/nghien_cuu_giao_dien_2026-11-06/c209/` (công cụ / kết quả thô), `report_agent/2026-11-06_giao_dien_cong/c209_implementation.md`.

## PHIÊN SAU ĐỌC TRƯỚC (phiên sáng 06/11)
- **Đã xong 06/11** (terminal `hue-rag-a4`, 0 USD):
  - **C207:** `p9-sua-lich` `6543f82` → **`09ddaf9`** trên `main` `0a9e0f3`, đã push. Q1 228/228 (`dba1f578eef1`) · Q1m 228/228 (`ac53ea9046f3`) · 239 + 3 test · `mo_phong.py` 10/10 · `kiem_bo.py --pha` OK 6/6. Report `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md`; kết quả `data/phase_9/sua_lich/q1_c207/`.
  - **Review `p9-b5b`:** vòng 1 `18d1cec` changes_requested ⇒ vòng 2 `0380345` **ready** (`report_agent/2026-11-02_phase_9_code/b168_b5b_review.md` §7). Còn: B rebase + Q1 ⇒ A merge cờ tắt ⇒ User bật.
  - **Review B171** (`p9-b5-sua` `d5028d4`): **changes_requested** — M-1 `_noi_nguoc_toi` bắt nhầm 5/10 câu hợp khung (16 ca dò ghi trong review §2); m-1 bộ dò tối bỏ sót; m-2 đếm k gồm điểm người dùng nêu; T3 (b) sau M-1 (A đã giao B). `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md`.
- **Việc C kế (A giao):**
  1. B báo B171 sửa xong ⇒ kiểm phần sửa **trước**: test + 16 ca dò (viết lại từ review §2) + Q1 + đếm lượt chạy lại 4 câu xin buổi tối.
  2. **Harness lượt có phí sửa lịch** (A đồng ý): CHƯA code — thiết kế + bước kế `data/phase_9/sua_lich/tools/HARNESS_GHI_CHU.md`. Theo plan `5b68f3cb666a`, không đổi tiêu chí; chạy thử 0 USD (khoá giả + OpenAI cổng đóng). Xong ⇒ bổ sung report C207 §5 ⇒ báo A.
  3. Lượt đo có phí sửa lịch (đã thấy ×2 + kín ×2 qua User `!`, trần 0,20) chỉ khi `lich_trinh` bật (B5: E làm bộ kín mới, User duyệt). Trước đó rebase lại nếu `main` đổi code (gộp B171 ⇒ `tham_so.hoi_toi` + `chon_sang` chạm `xep`) + Q1.
  4. Sau đó: B5b phần lịch / "nếu mưa" trên bảng v5 User duyệt; giọng nói khi User thu xong (E).
- **Bộ đo (private, md5 12):** sửa lịch `data/phase_9/bo_do_sua_lich/` đã thấy `d0ad12b6ed12` · kín `daf762bcbbe5`; B6 `bo_do_b6/` `6ed74db21616` · kín `4de04132600b`; B5b `bo_do_b5b/` `7e1bc3da2e44`; bảng `lich_trinh/diem_v5.json` `c7d294fcacd5`.
- **Lệnh kín chờ:** không. **Không đọc** `data/phase_9/b5_v2/`, `data/phase_9/b5/kin/`.
- **Tiền C 06/11: 0 USD.**
- **Backlog (cho A, giữ từ 05/11):** kho mâu thuẫn vị trí Bảo tàng Cổ vật · không có mục "Bảo tàng Mỹ thuật Huế" · câu thiên tai vẫn gọi Serper · chữ đầu mục web p50 ~13 s · case 67 Golden từ chối ngẫu nhiên.
- **Câu hỏi cho A:** không có câu mới.

## Worktree / tạm (mất khi khởi động lại)
- `/tmp/c_sualich` giữ nhánh **`p9-sua-lich`** (gỡ trước khi session khác cần nhánh này). Dựng lại: `git worktree prune; git worktree add /tmp/c_sualich p9-sua-lich` + symlink `data/`, `knowledge-base-hue/`; `cd frontend && npm ci && npm run build` nếu cần `test_static_ui`.
- `/tmp/c_b5b_probe/src` (detach), `/tmp/c_b171` (detach `d5028d4`) — gỡ được (`git worktree remove`). Script tạm `/tmp/c207_tools/` (capture_flags, probe_*) — mất khi khởi động lại.

## Bẫy (giữ)
- Q1m cần cờ bật trên bản sao settings: đặt `core.settings_loader.SETTINGS_PATH` sang file tạm rồi `runpy` `capture_all.py`.
- `python -I` bỏ đường dẫn cwd ⇒ script import `llm.*` chạy không `-I`, với `PYTHONPATH=$PWD`.
- Rebase "hai bên cùng thêm": giữ cả hai, kiểm bằng `git range-diff`.
- Ca dò của người kiểm gồm cả câu **hợp lệ** model hay viết, không chỉ ca vi phạm (B171 M-1 lộ nhờ vậy).
- `run | grep` trong script nuốt lỗi ⇒ ghi log ra file, in mã thoát. Giờ trong file: luôn `date` trước (06/11 lỡ gõ tay 1 lần, hook bắt).
- Kín: dựng lệnh `!` sớm, gộp nhiều bước một lần gõ, chỉ in số / mã; đổi hành vi code ⇒ sửa nhãn kín **trước** lượt có phí.
