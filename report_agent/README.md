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
| `2026-10-24_phase_8_1_ra_soat/` | Phase 8.1: Claude rà lại quyết định Phase 0–7 (do AGY/Codex làm), đề xuất + thí nghiệm so với baseline cũ; không đổi hành vi chatbot. User mở 19:00 24/10 | **đang làm** — brainstorm/spec + bảng rà quyết định (C11) |

Phase 7B (2026-10-24): report nằm ở `reports/phase_7b_*` và `reports/phase_8_*` (viết trước khi đổi
cấu trúc, giữ nguyên để không gãy link).
