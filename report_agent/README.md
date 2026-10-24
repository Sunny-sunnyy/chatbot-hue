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
| [2026-10-24_to_chuc_bao_cao/](2026-10-24_to_chuc_bao_cao/) | Tổ chức lại report + viết lại user report các Phase; học cách làm của MekongAI | đang làm |

Phase 7B (2026-10-24): report nằm ở `reports/phase_7b_*` và `reports/phase_8_*` (viết trước khi đổi
cấu trúc, giữ nguyên để không gãy link).
