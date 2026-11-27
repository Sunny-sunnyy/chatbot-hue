# Việc đang mở (sổ việc — cập nhật 11:56 27/11/2026)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent trên `gpt-6-luna` (xong Đợt 1, chuẩn bị Đợt 2 & Đợt 3)
- **Đã xong Đợt 1 (`e432e32c` + mở cờ `64 MỞ / 7 TẮT`, `~0,052–0,059 USD` OpenAI):**
  - `1A` **GIỮ & BẬT** (`chong_lap_cong_cu: true`, `cuu_max_turns: true`, `trajectory_eval.py`): đo cặp `gpt-6-luna` `n=14` giảm `max_turns` `1/14 → 0/14` (`1a_multi_03` cứu đạt `8` nguồn, `p95` giảm `14,5 → 12,0 s`, `0,029046 USD`).
  - `1B` **GỠ / GIỮ TẮT** (`siet_tro_chuyen: false`): `n=18` bên tắt đã `0/6` lọt `tro_chuyen`, bật lên `CHƯA RÕ` mà tăng `+8,5%` chi phí (`0,010259 USD`).
  - `1C` **ĐẠT** trên `gpt-6-luna` (`so_tay` `9,92s`/`16,47s`, `ho_so_chu_de` `9,85s`/`13,31s`, `sua_lich_hoi_truoc` `5/5`, `0,004828 USD` đo log + `~0,0083–0,0149 USD` ước; phát hiện `so_tay.py`/`ho_so.py` chưa ghi `usd`/tokens vào log).
- **Đang chạy Đợt 2 (giao `/swarm` `b2`, `c2`, `e2` từ `THIET_KE_DOT2_DOT3.md`):**
  - `b2` (nhánh `p19-b-tools-dot2`): cài `goi_y_phuong_an_mua_nang` (`goi_y_mua_nang: false`), `so_sanh_diem_den` (`so_sanh_diem_den: false`), kiểm trần `max_turns_for` không tự cộng mù `+1` vượt `6`, và vá ghi `usd`/tokens vào `application.log` cho `so_tay.py` & `ho_so.py`.
  - `c2`: soạn bộ câu công khai Đợt 2 (`n=16` mưa/nắng, `n=14` so sánh, `n=20` tool-gating) + chạy đo TẮT trước trên 8+8 câu đích (`<= 0,02 USD`) để bảo đảm bộ câu phân biệt được với `tim_kho` + `the_noi` trước khi bật đo.
  - `e2`: review chéo `b2`, sau khi `c2` trả cổng `8039` sẽ đo so cặp `H2_mua_nang`, `H2_so_sanh`, `H2_cong_cong_cu_luon` trên `gpt-6-luna` (`<= 0,06 USD`).
- **Chờ sau Đợt 2:** **Đợt 3** (tối ưu Hỏi bằng ảnh 0 GPU qua `confidence_gate` giảm mốc `15/73` ảnh lạ trên `gpt-6-luna`) + gọi `d2` đồng bộ giáo trình `bai_hoc/giao_trinh/`.
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
- **Tính năng (`backend/config/settings.yaml`):** **64 MỞ · 7 TẮT** (`anh.bat` + 63 cờ mở / 7 cờ tắt trong `assistant:`, sau khi mở `chong_lap_cong_cu` & `cuu_max_turns` và giữ tắt `siet_tro_chuyen`).
- **Kho & Chỉ mục Qdrant (`hue_full_corpus_7a2_e5_small_384`):** **269 bài · 9.540 đoạn** (cập nhật 26/11; Khám phá **269/269** có ảnh).
- **Cả bộ test (`c2d0ee68` + chạy kiểm lại sau đợt sửa 17:13 25/11 + 26/11):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`data/test_rong_2026-11-22/KET_QUA_c2d0ee68.tsv`); sau đợt sửa 17:13 25/11 chạy 8 file (`111 passed`); sau đợt sửa kho & ảnh 26/11 chạy 4 file chạm (`86 passed`).
- **Chi phí OpenAI phần test của nhóm:** **~0,81 USD** (`0,66` đo bù 23/11 + `0,008213` Playwright C + `0,000572` kiểm `main` A + `0,0051` 5 lượt `/api/chat` kiểm khói 25/11 + `0,0665833` lượt bộ câu kín & N trên `ea96e47c` + `0,00705963` kiểm Docker `:8880` & `smoke_eval` + `0,039305` đo cặp 1A/1B + `~0,013–0,020` kiểm 1C trên `gpt-6-luna` 27/11) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
