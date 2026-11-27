# Việc đang mở (sổ việc — cập nhật 14:57 27/11/2026, đã kết phiên sạch)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent trên `gpt-6-luna` (đã xong Đợt 1 + Đợt 2 + Nấc 2B + Đợt 3A + Nghiên cứu chuyên sâu + Giáo trình `d341fd96`; chờ Hiếu chọn Đợt 4)
- **Đã hoàn tất & đồng bộ lên `main` (`d67375f2`, `aa333ca`, `79cb4dea`, `d341fd96`; tổng chi phí chiến dịch ~`0,321–0,328 USD` OpenAI):**
  - **Đợt 1:** `1A` **GIỮ & BẬT** (`chong_lap_cong_cu: true`, `cuu_max_turns: true`, `trajectory_eval.py`: `max_turns` `1/14 → 0/14`, `p95 14,5 → 12,0 s`); `1B` **GỠ / GIỮ TẮT** (`siet_tro_chuyen: false`); `1C` **ĐẠT** trên `gpt-6-luna`.
  - **Đợt 2:** `goi_y_mua_nang: true` (`1/8 → 5/8`, `0/4` bão/lũ, USD `-40,5%`) + `so_sanh_diem_den: true` (`1/8 → 6/8`, `0/3` hụt văn hoá, USD `-37,3%`) + khoá `MAX_VONG_CONG_CU_TOI_DA = 6` + log USD `so_tay`/`ho_so`.
  - **Nấc 2B — GIỮ & BẬT (`cong_cong_cu: linh_hoat`):** `n=20` lách từ khoá `0/10 → 9/10`, gọi thừa `0/5`, ngoài phạm vi `5/5`, USD **`-15,23%`**, `cached_tokens` `46,5% → 76,9%` (`83,5%` ở kho thuần), `p95 16,1s → 11,5s`, `0` lỗi (`KET_LUAN_DOT2B_3A.md`).
  - **Đợt 3A — GIỮ `mac_dinh` (`anh.che_do_tu_choi: mac_dinh`):** `n=76` ảnh (`0,070648 USD`) `confidence_gate` giảm FP `-50%` (`10/18 → 5/18`) nhưng tụt recall dương `-17` top-1 / `-20` top-3 (`49/55 → 32/55` / `52/55 → 32/55`) ⇒ giữ `mac_dinh`.
  - **Nghiên cứu chuyên sâu (`0 USD`, đã xoá `/tmp/hr_*_repos/`):** `c2` ([KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md](data/nghien_cuu_2026-11-27/KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md)) & `b2` ([DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md](data/nghien_cuu_2026-11-27/DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md)).
  - **Giáo trình (`d341fd96`, `0 USD`):** `d2` cập nhật `21` file `bai_hoc/giao_trinh/`, `e2` review chéo đạt sạch (`0` blocker, `0` leak).
- **Chờ chủ dự án chọn nếu mở tiếp Đợt 4 (từ 2 báo cáo nghiên cứu, còn dư ~`0,9–1,4 USD` dưới trần):** bộ chấm `faithfulness_eval.py` + `ToolCallAccuracy` (P0/P1) · `canh_bao_vong_con_lai` + giữ ổn định mảng tools (P0/P1) · `kiem_du_bang_chung` kiểu Sufficient Context (P1) · `anh_hoi_lai_goi_y` vùng xám kiểu ReCoVERR (sau Đợt 3A) · vá chi tiết `5/8` & `6/8` Đợt 2.
- **Nguyên tắc:** mọi thay đổi code mới nằm sau công tắc tắt, đo so cặp với bản cũ theo `run-experiment` — tốt hơn vượt nhiễu mới giữ, kém hơn thì giữ bản cũ, xong cập nhật báo cáo + giáo trình.
- **Đã đóng hẳn (`10:55 27/11/2026`, không nhắc lại):**
  - Thuê GPU + fine-tune model nhận ảnh (giữ nguyên tính năng Hỏi bằng ảnh 55 tên đang chạy bằng `gpt-6-luna`; `goi_may_thue.tar` giữ nguyên không xoá).
  - `MCP Server`; mảng DevSecOps / Supply Chain CVE / Red-Teaming / FinOps.
- **Vẫn gác (chờ chủ dự án tự mở lại khi rảnh):**
  - Bước triển khai thực tế lên AWS (`deploy/`): chờ chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày (khi đóng gói thật nhớ chạy lại `dung_anh.sh origin/main`).

### A.2. Nợ kỹ thuật nhỏ (gom làm khi sửa file liên quan, không mở đợt riêng)
- **Độ dài tên trong gói deploy `gpt-6-luna`:** kiểm lại chỗ cắt tên hoặc chữ dài nếu phát hiện trong thực tế (E ghi chú sau rà).
- **Chuẩn hoá 1–2 dòng docstring/comment nhỏ** còn dư từ đợt rà B (`ho_so_chu_de` / `sua_lich_hoan_tac`) nếu có dịp chạm file.

### A.4. Nhánh Git đang giữ (sau đợt dọn sạch tối 26/11 — còn `main` + 9 nhánh giữ)
- **Đã gộp lên `main` (26/11):** `origin/p15-d-don-giao-trinh-2511` (`06670463` → `b803b6fc`), bổ sung 4 bài kho + ảnh *Lễ Kỳ yên*, đồng bộ giáo trình + runbook + sổ trạng thái.
- **Nhánh hồ sơ / bản thử còn giữ đối chiếu (9 nhánh):** `thu-b-mo-doc-tiep` · `thu-c-khung-truoc` · `thu-b-ba-duong-tim` · `thu-b-dem-loi-dan` · `p9-b-dem-y-go-tat-2` · `p9-c-ve-loi-nho` · `p9-c-sua-2-het-vong` · `p9-b-vong-cuoi-chu-2` · `p9-e-chi-sang-len-ke-hoach`. Toàn bộ nhánh đã gộp và nhánh nháp cũ không còn dùng đã được xoá sạch.

## B. Chỉ số nền & Trần OpenAI của nhóm
- **Model viết mặc định (từ 15:41 25/11):** `gpt-6-luna` (`full_corpus_generation.provider: openai`).
- **Tính năng (`backend/config/settings.yaml`):** **66 MỞ · 7 TẮT** (`anh.bat` + 65 cờ mở / 7 cờ tắt trong `assistant:`), kèm **`cong_cong_cu: linh_hoat`** (Nấc 2B) và giữ **`anh.che_do_tu_choi: mac_dinh`** (Đợt 3A).
- **Kho & Chỉ mục Qdrant (`hue_full_corpus_7a2_e5_small_384`):** **269 bài · 9.540 đoạn** (cập nhật 26/11; Khám phá **269/269** có ảnh).
- **Cả bộ test (`c2d0ee68` + kiểm sau Đợt 2B/3A):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`KET_QUA_c2d0ee68.tsv`); kiểm chạm sau Nấc 2B/3A xem `CURRENT_HANDOFF.md`.
- **Chi phí OpenAI phần test của nhóm:** **~1,08 USD** (`~0,98` tới Đợt 2 + `0,028704` đo cặp Nấc 2B + `0,070648` đo cặp Đợt 3A) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
