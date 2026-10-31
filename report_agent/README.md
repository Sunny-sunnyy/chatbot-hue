# report_agent — report theo đợt việc

Từ 2026-10-24 (User): mỗi đợt việc có một folder `report_agent/<YYYY-MM-DD>_<chủ_đề>/` (ngày mở
đợt, chủ đề ngắn không dấu cách). Report implementation/review của đợt nằm trong folder đó.
Quy tắc chung: `session_prompt/WORKFLOW.md` §6. `reports/` là lịch sử tới 2026-10-24, không thêm file.

- Báo cáo cho User nằm ở `bao_cao_he_thong/` (gốc repo): `LUONG_HOAT_DONG_HE_THONG.md`,
  `BAO_CAO_<KHÂU>.md`, `nhat_ky/`. User report cũ: `reports/user_reports/` (lịch sử).
- Nghiên cứu ChatGPT (private, không commit): `gửi chatgpt/<YYYY-MM-DD>/{tìm thông tin,kết quả nghiên cứu}/`.

Report không chép corpus, câu hỏi Golden, vector, payload hay secret.

## Các đợt

| Folder | Nội dung | Trạng thái |
|---|---|---|
| [2026-10-24_to_chuc_bao_cao/](2026-10-24_to_chuc_bao_cao/) | Tổ chức lại báo cáo (`bao_cao_he_thong/`), viết lại báo cáo Phase 0–7B, học cách làm MekongAI (`0a709db`), dọn Foods (B9) — [TONG_HOP.md](2026-10-24_to_chuc_bao_cao/TONG_HOP.md) | **chưa đóng** — B9 chờ C review phiên sau |
| [2026-10-25_cai_tien_cach_lam/](2026-10-25_cai_tien_cach_lam/) | Cải tiến cách làm (không đổi chatbot): vòng tự cải tiến, nâng `run-experiment`, Session D, `AGENTS.md`, hook git; đề xuất cho 8.1/8.2/9 từ khóa AI FDE — [KE_HOACH.md](2026-10-25_cai_tien_cach_lam/KE_HOACH.md) | **ĐÓNG** 11:05 25/10 — [TONG_HOP.md](2026-10-25_cai_tien_cach_lam/TONG_HOP.md); review đạt 2 vòng |
| `2026-10-24_phase_8_1_ra_soat/` | Phase 8.1: Claude rà lại quyết định Phase 0–7 (do AGY/Codex làm), đề xuất + thí nghiệm so với baseline cũ; không đổi hành vi chatbot. User mở 19:00 24/10 | **ĐÓNG** 15:27 25/10 — [TONG_HOP.md](2026-10-24_phase_8_1_ra_soat/TONG_HOP.md); chỉ context 10 thắng; G0.6 khóa |
| `2026-10-25_phase_8_2_ap_dung/` | Phase 8.2: đưa context 10 + NFC vào chatbot, mốc người đọc cặp mù, thử E1 trả lời một phần / E2 lỗi `[n]` / E3 luna trên chatbot mới. User chọn phạm vi 16:0x 25/10 | **đang chạy** (tối 26/10) — B1 rebase ready (`p82-b1`, merge sau B0); Bước 2 = spec §10 (đợt cải tiến từng khâu): K1 / R2 kém hơn, K3 duyệt chờ chạy |
| `2026-10-25_ra_soat_noi_dung_kho/` | Rà nội dung kho (chỉ đọc): chỗ tự mâu thuẫn + thông tin có thể đã cũ, để User xem; sửa ở đợt build lại index. User duyệt 16:1x 25/10 | **đang mở** — C32 |
| `2026-10-26_cai_tien_tung_khau/` | Tìm hướng tốt hơn từng khâu (thử + so với mốc sau 5 gói sửa code) = Bước 2 spec 8.2 §10. User mở 20:0x 25/10 | **đóng 11:17 27/10/2026** (User chọn chốt đợt): K1, K3, K3b-n, R1, R2 kém hơn; K3b-m tầng tìm tốt hơn nhưng khâu trả lời kém hơn theo luật; R3, K2, E2 NOT RUN; chatbot không đổi ([TONG_HOP.md](2026-10-26_cai_tien_tung_khau/TONG_HOP.md)) |
| [2026-10-27_phan_ton_phase_cu/](2026-10-27_phan_ton_phase_cu/) | Phần tồn Phase cũ (User 14:15 27/10: xong phần tồn rồi mới đi tiếp): B1 rebase sẵn, plan B3, gold v3, nợ nhỏ code / guide, soạn + kiểm đợt sửa kho (áp sau đóng 8.2), Qwen3-8B ⇒ thí nghiệm sau | **mở** — chuẩn bị xong 27/10 chiều; áp sau đóng 8.2 |
| [2026-10-31_tra_web_codex/](2026-10-31_tra_web_codex/) | Tra web bằng Codex CLI thay chép tay qua ChatGPT web (User duyệt 31/10): thử 6 lượt + chấm (dữ liệu `data/tra_cuu_cli_2026-10-31/`), `scripts/tra_web_codex.sh`, chặn `agy`, §9 | **ĐÓNG** 31/10 (`1a9dca4`, B103 ready) — [TONG_HOP.md](2026-10-31_tra_web_codex/TONG_HOP.md) |
| [2026-10-31_streaming_spec/](2026-10-31_streaming_spec/) | Spec streaming câu trả lời: kiểm nghiên cứu ChatGPT, đối chiếu code, nháp v3, D1–D3 User chốt, spec + review Claude + Codex (W33) | **mở** — chờ User Q1 + duyệt sha `cf1ae9ef6c2c` — [TONG_HOP.md](2026-10-31_streaming_spec/TONG_HOP.md) |
| `2026-10-25_ra_soat_code/` | Rà code Phase 0–7 (chỉ đọc): code thừa, độ phức tạp, khâu dính, test, guide lệch code, hiệu năng, cơ hội phát triển. User 16:5x 25/10 dừng 8.2 để rà trước | **ĐÓNG** 16:4x 26/10 — rà + kiểm chéo + sửa cả 5 gói (1a, 1b, 3, 4, đợt 3 `421c302`); [TONG_HOP.md](2026-10-25_ra_soat_code/TONG_HOP.md) |

Phase 7B (2026-10-24): report nằm ở `reports/phase_7b_*` và `reports/phase_8_*` (viết trước khi đổi
cấu trúc, giữ nguyên để không gãy link).
