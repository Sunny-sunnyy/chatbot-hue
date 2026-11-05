# STATUS E — kết phiên tối 22:14 05/11/2026 (`date`) · terminal `hue-rag-bc` · Claude Opus 5.5 · vai thực thi (Phase 10 + review)

## PHIÊN SAU ĐỌC TRƯỚC
- **Ảnh (Phase 10) — xong, cờ tắt:** `main` có `2ca9937` (P1 luna v1 dạng gợi ý có xác nhận) + `76319e2` (CSS khung điện thoại). Báo cáo User `bao_cao_he_thong/BAO_CAO_HOI_BANG_ANH.md` bản 2.
  E9 SigLIP 2 **âm** cả 3 cách (`report_agent/2026-11-05_phase_10_anh/e9_siglip_implementation.md`). **Câu chờ User (A hỏi):** bật cờ `anh.bat`? xoá collection thử `hue_anh_siglip2` (172 điểm)?
- **Giọng nói — NGHE:** spec Phase 10 **bản 4 `784d6f7abd9f` User duyệt** (§12 (7) sherpa-onnx, (8) tải model, (10) thu 40 câu; (9) Web Speech **bỏ**). **G0 xong** — nhánh `p10-giong-noi` **`93bbc63`** (đã push; chỉ `pyproject.toml` + `uv.lock`: `sherpa-onnx` + `sherpa-onnx-core` 2.0.1), report `report_agent/2026-11-05_phase_10_anh/e16_g0_giong_noi.md`.
  Model (private, gitignore) `data/phase_10/giong_noi/models/` 108 MB: `gipformer_68m/` (int8, HF commit `318322b`), `zipformer_30m/sherpa-onnx-zipformer-vi-30M-int8-2026-02-09/`; script `data/phase_10/giong_noi/tools/g0.py`.
  **Bước kế:** G1 — 40 câu **C đã soạn** (C205, `data/phase_10/giong_noi/bo_40_cau/`, md5 `a24d445bfe61`) ⇒ **chờ User** + ≥ 1 giọng Huế / Trung thu ⇒ E đổi WAV 16 kHz mono bằng `ffmpeg` có sẵn ⇒ **G2** đo 2 model theo **V-a tên riêng ≥ 90 % · V-c số ≥ 90 % · V-d p95 ≤ 1,5 s (câu ≤ 10 s) + RAM ≤ 1,5 GB** (V-b WER chỉ báo; V-e chèn tên sai ≤ 1/40 khi hotwords) ⇒ G3 route + G4 giao diện. Plan G2 ghi trước: 2 luồng; hàm chuẩn hoá số nhận chữ + chữ số (Zipformer ra "TV" / chữ số); dải điểm hotwords thử (Zipformer cần ≥ 8, Gipformer 20 chèn lặp).
  **Tạo lại worktree** (đã gỡ): `git worktree add /tmp/e_giong p10-giong-noi` ⇒ symlink `data/`, `knowledge-base-hue/` khi cần ⇒ chạy bằng `uv run --project /home/minhhieu/hue_rag …`.
- **TTS (đọc thành tiếng):** để sau (ứng viên ở `data/phase_10_nghien_cuu/giong_noi/nghien_cuu_mo_hinh.md` §6 — VieNeu-TTS v3 Turbo, ZeroTTS).

## Review đã làm phiên tối
- **E13 / E15 B6 tra web** (`report_agent/2026-11-02_phase_9_code/b165_review.md`): vòng 1 `9140152` changes_requested 0/2/2 (link HTML `//` lọt server + giao diện; thiếu "lụt" / "áp thấp") ⇒ B sửa `77d51b6` ⇒ vòng 2 **ready** (A đã merge cờ tắt `7ff8e5a`).
- **E17 / E18 B5b thời tiết** (`report_agent/2026-11-02_phase_9_code/b168_review_som.md`): miễn `[n]` quá rộng (major) ⇒ A chọn khối dự báo thành nguồn `[k]` ⇒ B sửa `a0906a6` ⇒ vòng 2 **đạt**, m-1 dòng trống cuối `test_b5b_thoi_tiet.py`.
- Khác: E10 khôi phục + push `p10-anh`; Playwright P1 (máy tính + điện thoại); E12 / E14 spec giọng nói bản 3 ⇒ 4; E1 nghiên cứu giọng nói xong.

## Tiền
- **E phiên tối: 0,019835 USD** = Playwright P1 0,001634 + E9 P2c 0,015681 (+ 2 lần quá hạn log 0, ≤ ~0,0008) + E11 điện thoại 0,00252. **Phase 10 tổng: 0,098380 / trần 0,15 (dừng 0,13).** Giọng nói 0 USD.

## Bẫy / đã học
- `.venv` chung **có `sherpa-onnx`** nhưng lock `main` chưa có (tới khi `p10-giong-noi` merge): `uv run` (đồng bộ không chặt) giữ gói; **`uv sync` thường ở `main` sẽ gỡ** ⇒ cài lại: từ worktree nhánh `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --inexact --frozen`. `sherpa-onnx` 2.0.1 mới ~10 ngày (luật "≥ 2 tuần" chỉ có ở `frontend/.npmrc`).
- CSP trang (`script-src 'self'`) chặn `page.wait_for_function` của Playwright ⇒ chờ bằng locator. Dò giao diện: nạp **chính** `markdown.js` qua import map (`page.route`) thay vì chép lại bộ lọc.
- Kiểm worktree dò đang ở **đúng sha** trước khi kết luận (E15 suýt kết luận trên code cũ).
- Đếm ảnh: loại file phiếu `.jsonl` (đầu phiên báo 179 / 34 là đếm nhầm; đúng 172 / 40).
- Script đặt theo đường dẫn không thấy gói `backend/` ⇒ `PYTHONPATH=<worktree>/backend`.

## Câu hỏi cho A
- Có thêm luật "gói Python ≥ 2 tuần tuổi" như `frontend/.npmrc` không (sherpa-onnx 2.0.1 ~10 ngày)?
- (A trả lời 05/11 tối) luật "gói Python ≥ 2 tuần" ⇒ A hỏi User phiên sau, chưa áp. G1: chỉ chờ User thu — E có thể chuẩn bị trước script đổi WAV + plan G2.
