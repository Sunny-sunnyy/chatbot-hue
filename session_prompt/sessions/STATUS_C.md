# STATUS C — kết phiên tối 05/11 (22:14 05/11/2026 `date`; ≤ 30 dòng; lịch sử: `git show c0e2f89:session_prompt/sessions/STATUS_C.md`)

## PHIÊN 06/11 (terminal `hue-rag-a4`; A giao 10:48 06/11/2026 `date`)
- **C207 (đang làm):** rebase `p9-sua-lich` lên `main` mới trong worktree `/tmp/c_sualich` (nhánh tạm `c207-rebase`, chưa đụng ref `p9-sua-lich`, chưa push) + Q1 (capture_all 228) + test 0 USD. File sẽ ghi: chỉ code trong worktree (giải xung đột rebase nếu có), kết quả `data/phase_9/sua_lich/q1_c207/`, report `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md`. Không đọc `data/phase_9/b5_v2/`.
- **Kế:** review nhánh `p9-b5b` khi B báo; review B171 khi B xong.

## PHIÊN SAU ĐỌC TRƯỚC
- **Đã xong tối 05/11** (terminal `hue-rag-3c`): C192 sửa kho giờ (User giữ; 8.435 đoạn, record `9921888f2030`, T1 `64656a87c109`; `report_agent/2026-11-05_sua_kho_gio/c192_implementation.md`) · B6 kín ×2 đạt (`b165_b6_implementation.md` §10) · kiểm A bật `tra_web` ready (`b165_review.md`) · review `p10-anh` ready (`e8_review.md`) · C202 tắt ghi đệm **âm** (`c202_ghi_dem.md`) · C200 nhiễu S-AT (User duyệt phương án 3) · C201 cache ⇒ backlog Phase 12.
- **Bộ đo (private, md5 12):**
  - sửa lịch `data/phase_9/bo_do_sua_lich/` đã thấy `d0ad12b6ed12` · kín `daf762bcbbe5` (K-S2 sửa theo B166, bản cũ `chuoi_sealed.truoc_B166.jsonl`); trên `6543f82`: 10/10 · 5/5 · `kiem_bo` OK;
  - B6 `bo_do_b6/` đã thấy `6ed74db21616` · kín `4de04132600b` (nhãn giữ sau sửa kho);
  - B5b `bo_do_b5b/` `7e1bc3da2e44` (24 câu, không kín; trên `8bdeb65` OK, ca phá 5/5; D9 / D10 chỉ hiện với bảng v4 / v5);
  - giọng nói `data/phase_10/giong_noi/bo_40_cau/cau.jsonl` `a24d445bfe61`;
  - bảng `lich_trinh/diem_v5.json` (sha `c7d294fcacd5`) + `diem_toa_do_v5.json` + `tools/kiem_v5.py` OK.
- **Phiếu chờ User:** (1) chấm Q3 B5 `data/phase_9/b5/kin/phieu_cham_user.md` · (2) `lich_trinh/diem_cho_user_v5.md` (ô A / B) · (3) duyệt + thu 40 câu theo `bo_40_cau/huong_dan_thu_cho_user.md` ⇒ `data/phase_10/giong_noi/thu/`.
- **Lệnh kín còn chờ:** không.
- **Việc C kế (A chốt):**
  - đo sửa lịch có phí (đã thấy ×2 + kín ×2 qua User `!`) **ngay** khi User chấm Q3 đạt + A bật `lich_trinh` — plan `5b68f3cb666a`;
  - sau đó B5b phần lịch / "nếu mưa" trên bảng User duyệt;
  - giọng nói khi User thu xong.
- **Backlog (cho A):** (a) kho mâu thuẫn vị trí Bảo tàng Cổ vật (file vé Quần thể :189 ↔ Kinh thành :149) · (b) không có mục "Bảo tàng Mỹ thuật Huế" (15 ↔ 15A Lê Lợi lệch) · (c) câu thiên tai vẫn gọi Serper ~0,001 USD · (d) chữ đầu mục web p50 ~13 s · (e) case 67 Golden từ chối ngẫu nhiên.
- **Tiền C phiên tối: 0,056564 USD** (C192 "sau" 0,012834 · C203 0,040633 · C202 0,003097).

## Worktree / tạm
- **Giữ:** `/tmp/c_sualich` (`6543f82`), `/tmp/c_b5b` (`8bdeb65`) — mất khi khởi động lại ⇒ dựng lại từ commit.
- Đã gỡ: `/tmp/c198`, `/tmp/c202` (bản vá ở `data/phase_9/c202_ghi_dem/patch.diff`), `/tmp/c_b6`, `/tmp/c198_probe/`.

## Bẫy (giữ)
- `run | grep` trong script nuốt lỗi (C202 lần đầu) ⇒ ghi log ra file, in mã thoát.
- Mô phỏng bằng **code thật** trước khi chốt nhãn (L01 B5b bản đầu không thử được D10).
- Đổi hành vi code ⇒ sửa nhãn kín **trước** lượt có phí, ghi lý do + sao lưu; ca phá so với số lỗi gốc.
- Kín: dựng lệnh `!` sớm, gộp nhiều bước một lần gõ, chỉ in số / mã.
