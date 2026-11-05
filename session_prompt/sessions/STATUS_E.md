# STATUS E — kết phiên 16:48 05/11/2026 (`date`) · terminal phiên 05/11 `hue-rag-7a` · Claude Opus 5.5 · vai thực thi (Phase 10 + review)

## PHIÊN TỐI 05/11 — terminal `hue-rag-bc` · E10 XONG (19:23 05/11/2026)
- **`p10-anh` đã commit + push: `0632e10`** (từ `268466d`, áp patch `9138ca6b1fc3`: 9 file +542 / −2, cờ `anh.bat: false`; hook quét 0 trùng). Test `test_p10_anh.py` + `test_assistant_boundary.py`: **40 passed** [Chạy].
  Mục "Nhánh p10-anh CHƯA COMMIT" bên dưới đã hết đúng.
- Worktree `/tmp/e_anh` (nhánh `p10-anh`) dựng lại; symlink `data`, `knowledge-base-hue` untracked — gỡ khi xong.
- **Playwright P1 ĐẠT (19:51 05/11/2026)** — report e8 mục cuối; script `data/phase_10/anh/a1_playwright/ui_p1.py`, kết quả `…/ket_qua/`. Cờ tắt 0 nút; cờ bật: lỗi kiểu / > 10 MB chặn ở trình duyệt; ảnh trong ds ⇒ gợi ý ⇒ bấm ⇒ trả lời 7 nguồn; ảnh mèo ⇒ "chưa nhận ra" ⇒ Gõ tên; 0 CSP / 0 request ngoài. Server đã tắt, cờ trả `false`.
- **Tiền Phase 10: 0,080179 USD** / trần 0,15 (dừng 0,13) — lượt này 0,001634 (gồm 1 lần gọi ảnh thừa do script hỏng lần đầu).
- **E9 chuẩn bị (A giao):** vòng tải 6 tên trống đang chạy nền; script kiểm trùng lớp 2 `data/phase_10/anh/e9/kiem_trung.py` (sha256 + tên file Commons ⇒ `kiem_trung_ket_qua.json`). Embed SigLIP **chờ A báo** (B Q1 xong / RAM ≥ 5 GB).
- Ảnh mẫu E9 đếm lại: 179 ảnh / 34 tên (trống 6: che_heo_quay, lang_gia_long, lang_khai_dinh, nui_ngu_binh, pho_nguyen_dinh_chieu, pho_tay).

## PHIÊN SAU ĐỌC TRƯỚC
- **Nhánh `p10-anh` — CHƯA COMMIT** (auto mode chặn: luật User "commit / push hỏi trước"; tin A không thay User). Worktree `/tmp/e_anh` ở `main` `268466d` + 9 file chưa commit
  (+542 / −2: `backend/llm/nhan_anh.py`, `backend/api/routes/anh.py`, `backend/tests/test_p10_anh.py`, `app.py`, `settings.yaml` khối `anh:` (`bat: false`), `test_assistant_boundary.py` (`ALLOWED`),
  `frontend/src/HoiBangAnh.jsx`, `App.jsx`, `index.css`). **`/tmp` mất khi máy khởi động lại ⇒ bản lưu: `data/phase_10/anh/p10_anh_chua_commit.patch` `9138ca6b1fc3`**
  (áp: tạo lại worktree nhánh `p10-anh` từ `268466d` ⇒ `git apply <patch>`). Việc đầu phiên: **xin User cho commit + push nhánh** (User gõ đồng ý ở terminal E).
- **A1 + A2 (ảnh, P1 luna) xong:** report `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` (A1 đạt T1–T9; A2 **âm** theo tiêu chí gốc: v0 / v1 / v2 × 2 lượt). **User chọn giữ v1** dạng gợi ý có
  xác nhận (đổi thước vì có bước bấm) — code đang ở lời dặn **v1**, `max_tokens` 1024, timeout 20. Report đã ghi "User đổi thước".
- **Giao diện P1 v1:** `HoiBangAnh.jsx` (nút chỉ hiện khi `GET /api/anh/ung_vien` 200; xem trước `blob:`; "Gợi ý từ ảnh, có thể sai — chọn đúng tên"; "Không phải các tên này — tôi gõ tên"; bấm tên ⇒
  câu ghép A3 ⇒ `ask`); CSP `img-src 'self' blob:`; build riêng trong worktree OK. **Chưa chạy Playwright / chưa thử trên trình duyệt** ⇒ bước kế: Playwright (cờ bật tạm) + review cả nhánh (C hoặc B) ⇒ User quyết cờ.
- **E9 SigLIP 2 (P2):** tiêu chí ghi trước `data/phase_10/anh/e9/tieu_chi_ghi_truoc.md` `a8524989f221` (đạt ⇔ Q-a ≥ 22/25 VÀ Q-c ≤ 1/5). Model `google/siglip2-base-patch16-224` **đã tải** (HF cache, 1,5 GB).
  Ảnh mẫu: `e9/mau/<id>.txt` (186 ứng viên / 40 tên, loại tên file trùng bộ đo) ⇒ tải `e9/mau_anh/<id>/` **149 ảnh, 30 / 40 tên xong**; chưa xong: bien_thuan_an, che_heo_quay, dan_xa_tac, doi_vong_canh, lang_gia_long,
  lang_khai_dinh, me_xung, nui_ngu_binh, pho_nguyen_dinh_chieu, pho_tay (chạy lại vòng tải — tự bỏ tên đã có phiếu); không có ứng viên: banh_ep_hue, khu di tích Chủ tịch HCM. **Chưa embed, CHƯA tạo collection
  Qdrant** (`hue_anh_siglip2` mới chỉ có trong script). Script: `e9/e9.py` (`nap` / `do` / `ket_hop`), chấm bằng `tools/do_a2.py cham`. Chưa kiểm lớp 2 (sha256 ảnh mẫu ↔ ảnh đo). Ảnh mẫu chưa ai xem tận mắt (giới hạn).
- **E1 giọng nói:** dở (tạm dừng theo User) — `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md`.
- **Review đã đóng phiên này:** plan B5 bản 7 ready · sửa lịch bản 3 `5b68f3cb666a` ready · B5b bản 2 `cc09fda9f634` ready · spec Phase 10 bản 2 (B review) · plan A1 bản 2 (C review).
- **Tiền Phase 10:** 0,078545 USD / trần 0,15 (dừng 0,13) — bước 0 0,000384 + A2 0,078161. P2c (luna kết hợp) ước ≈ 0,027.
- **Dọn:** worktree `/tmp/e_anh` (symlink `data`, `knowledge-base-hue` untracked — gỡ khi xong); `/tmp/e8_*`, `/tmp/e7_*` (file tạm, xoá được).

## Đã học / bẫy
- `max_tokens` gồm suy luận: 512 cắt 4 / 66 ảnh khó ⇒ đầu ra hỏng bị chấm "không nhận ra" (số đo lạc quan) ⇒ luôn đếm `output_tokens == trần`.
- `codex.jsonl`: lô mở trang là `action.type: other` (results `ref_id` *view*) — đã sửa script (E7, commit `ea114ae`).
- Hàm B5 `bo_diem` / `cat_ngay_cuoi` sửa khung tại chỗ + trace phụ #6 chép tham chiếu ⇒ trạng thái đổi theo lượt bị huỷ (review sửa lịch M-1).
- Symlink `frontend/dist` trong worktree trỏ bản build chung ⇒ build trong worktree sẽ ghi đè — gỡ symlink trước khi build.
- Commons trả 429 khi gọi dày; chỉ nhận cỡ thumbnail chuẩn (400 với cỡ tự chọn) — `tai_anh.py` / `tim_mau.py` chờ theo `Retry-After`.
- Lỡ gõ tay giờ (hook bắt) và lỡ dùng `python3` hệ thống ⇒ luôn `date` + `uv run`.
