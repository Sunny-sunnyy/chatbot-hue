# STATUS E — kết phiên 16:48 05/11/2026 (`date`) · terminal phiên 05/11 `hue-rag-7a` · Claude Opus 5.5 · vai thực thi (Phase 10 + review)

## PHIÊN TỐI 05/11 — terminal `hue-rag-bc` · E10 + Playwright + E9 + E11 XONG (20:26 05/11/2026)
- **`p10-anh` đã commit + push: `0632e10`** (từ `268466d`, áp patch `9138ca6b1fc3`: 9 file +542 / −2, cờ `anh.bat: false`; hook quét 0 trùng). Test `test_p10_anh.py` + `test_assistant_boundary.py`: **40 passed** [Chạy].
  Mục "Nhánh p10-anh CHƯA COMMIT" bên dưới đã hết đúng.
- **E11 khung điện thoại XONG (20:26 05/11/2026):** bản `main` che câu trả lời (360×740 thẻ ảnh mở: còn 191 px đọc) ⇒ CSS màn ≤ 700 px (ảnh 72 px bên trái chữ) ⇒ 322 px; 390×844 gợi ý 227 ⇒ 398. **Nhánh `p10-anh-mobile` `13c6a7a` — A review + merge `main` `76319e2`** (nhánh chờ User xoá) (chỉ `frontend/src/index.css` +8; `test_static_ui` 3 passed; build OK). Ảnh trước / sau + script `data/phase_10/anh/e11/`. Tiền 0,00252. Báo cáo User `BAO_CAO_HOI_BANG_ANH.md` bản 2 (A đã commit). 
- **E1 giọng nói XONG (20:34 05/11/2026, 0 USD):** `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md` — đọc + kiểm 2 kết quả Codex (đếm lại: STT 12 mở / 12 tự khai, TTS 36 / 7); xếp STT Gipformer 68M · Zipformer-30M hynt · Moonshine vi; TTS VieNeu v3 Turbo int8 (máy có `avx512_vnni`) · ZeroTTS; mốc Web Speech API (STT mặc định gửi âm thanh ra ngoài — MDN); bộ đo + ngưỡng đề xuất §5 (chưa chạy). Chờ A / User duyệt tải model + thư viện.
- Worktree `/tmp/e_anh` **đã gỡ** (symlink unlink trước).
- **Playwright P1 ĐẠT (19:51 05/11/2026)** — report e8 mục cuối; script `data/phase_10/anh/a1_playwright/ui_p1.py`, kết quả `…/ket_qua/`. Cờ tắt 0 nút; cờ bật: lỗi kiểu / > 10 MB chặn ở trình duyệt; ảnh trong ds ⇒ gợi ý ⇒ bấm ⇒ trả lời 7 nguồn; ảnh mèo ⇒ "chưa nhận ra" ⇒ Gõ tên; 0 CSP / 0 request ngoài. Server đã tắt, cờ trả `false`. Tiền lượt này 0,001634 (gồm 1 lần gọi ảnh thừa do script hỏng lần đầu).
- **E9 XONG — ÂM cả 3 phương án (20:19 05/11/2026)**: report `report_agent/2026-11-05_phase_10_anh/e9_siglip_implementation.md`. P2a 5/25 · P2b 20/25, ép 5/5 (điểm ngoài chồng điểm trong) · P2c 21·19, ép 1·3, Q-e 12/33. Không chạy vòng chỉnh (lý do §4). Collection **`hue_anh_siglip2` 172 điểm** còn trong Qdrant — chờ User quyết xoá.
- **Merge `main` `2ca9937`** (A, cờ tắt) gồm `973823f` (C198 m-1). Report e8 sửa m-2 + dòng boundary.
- **Báo cáo User mới `bao_cao_he_thong/BAO_CAO_HOI_BANG_ANH.md` bản 1** — chờ A review (A thêm dòng vào `bao_cao_he_thong/README.md`).
- **Tiền Phase 10: 0,098380 USD** / trần 0,15 (dừng 0,13) — E11 0,00252; P2c 0,015681 (+ 2 lần quá hạn log 0 USD, ≤ ~0,0008).
- Ảnh mẫu E9 (đếm lại sau vòng tải tối — số 179 / 34 lúc mở phiên là **đếm nhầm** cả file phiếu): **172 ảnh / 40 tên**; 5 tên tải dở thiếu `phieu_nguon.jsonl` (bien_thuan_an, dan_xa_tac, doi_vong_canh, me_xung, pho_tay — nguồn tra theo thứ tự dòng `mau/<id>.txt`); pho_tay chỉ 2 ảnh (Commons giữ > 15 phút ⇒ bỏ). **Kiểm lớp 2: 0 trùng** với 36 ảnh đo (sha256 + tên file Commons) ⇒ `e9/kiem_trung_ket_qua.json`.

- **E12 XONG:** spec Phase 10 **bản 3 `bc246a4ba3d6`** (§8 giọng nói NGHE viết đủ: G1–G9, bậc G0–G4, bộ 40 câu, V-a…V-f, bảo mật, bảng FDE; §9 M-1 / M-3 đề xuất đóng; §12 (7)–(10); phần ảnh không đổi) — chờ review ≤ 2 vòng ⇒ User duyệt sha.
- **E13 + E15 XONG:** review `p9-b6` vòng 1 `9140152` changes_requested 0 / 2 / 2 ⇒ B169 sửa `77d51b6` ⇒ **vòng 2 ready_for_user_confirmation** (`report_agent/2026-11-02_phase_9_code/b165_review.md`: dò `renderWebHtml` thật trong Chromium 0 link ngoài; server bắt `<a` / `href=` / `//host`; lụt / áp thấp; khoá không trong `repr`; "đang" ⇒ giới hạn, lý do đủ). Worktree `/tmp/e13/wt` đã gỡ; còn `/tmp/e13/probe_fe*.py` (tạm).
- **E14 XONG:** spec Phase 10 **bản 4 `784d6f7abd9f`** (B167 vòng 3: M-1 (a) V-b WER ⇒ theo dõi, quyết V-a + V-c + V-d; m-1 chuẩn hoá số; m-2 khoá mở khi luồng xong; m-3 p95 câu ≤ 10 s; m-4 tham số tập kiểu; m-5, m-6 §13) — chờ B vòng 2 (cuối).

- **E16 G0 giọng nói XONG (21:16 05/11/2026, 0 USD):** nhánh `p10-giong-noi` **`93bbc63`** (đã push; `sherpa-onnx` 2.0.1 + core — lock không đổi gói khác; gói mới ~10 ngày). Model `data/phase_10/giong_noi/models/` 108 MB (Gipformer int8 ghim `318322b`, Zipformer-30M int8). Cả hai chạy được; chữ HOA, không dấu câu; Gipformer số bằng chữ, Zipformer có chữ số ("TV"); 2 luồng ≈ 0,1 s / câu 3,7 s, RSS 180–230 MB; hotwords chạy với `modified_beam_search` nhưng điểm khác nhau giữa model, điểm 20 Gipformer chèn lặp ⇒ chọn ở G2. Report `report_agent/2026-11-05_phase_10_anh/e16_g0_giong_noi.md`. Worktree `/tmp/e_giong` (nhánh `p10-giong-noi`) giữ cho G3. **Chờ G1 (User thu 40 câu do C soạn).**

- **E17 XONG (review sớm B5b `b669981`):** major — miễn `[n]` ở lượt thời tiết áp cho cả chữ model ⇒ giờ / giá kho không trích lọt (dò 3 / 3 qua). Đề xuất: miễn chỉ khi mọi số ⊂ khối (hẹp) hoặc khối dự báo là nguồn thật (sạch); thiếu test. `report_agent/2026-11-02_phase_9_code/b168_review_som.md`; đã nhắn A + B. Worktree `/tmp/e17` đã gỡ. **A chọn cách (4)** (khối dự báo thành nguồn thật, 0 miễn `[n]`) ⇒ chờ B sửa rồi E kiểm một vòng (dò lại 3 ca (a)(b)(c) + ca trích `[k]` nguồn dự báo).

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
- **E1 giọng nói:** xong phiên tối 05/11 — xem mục trên.
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
