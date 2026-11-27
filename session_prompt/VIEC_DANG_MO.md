# Việc đang mở (sổ việc — cập nhật 13:43 27/11/2026)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent trên `gpt-6-luna` (đã xong Đợt 1 & Đợt 2; đang mở Nấc 2B + Đợt 3A)
- **Đã xong Đợt 1 (`e432e32c` + mở cờ `d67375f2`, `~0,052–0,059 USD` OpenAI):**
  - `1A` **GIỮ & BẬT** (`chong_lap_cong_cu: true`, `cuu_max_turns: true`, `trajectory_eval.py`): đo cặp `gpt-6-luna` `n=14` giảm `max_turns` `1/14 → 0/14` (`1a_multi_03` cứu đạt `8` nguồn, `p95` giảm `14,5 → 12,0 s`, `0,029046 USD`).
  - `1B` **GỠ / GIỮ TẮT** (`siet_tro_chuyen: false`): `n=18` bên tắt đã `0/6` lọt `tro_chuyen`, bật lên `CHƯA RÕ` mà tăng `+8,5%` chi phí (`0,010259 USD`).
  - `1C` **ĐẠT** trên `gpt-6-luna` (`so_tay` `9,92s`/`16,47s`, `ho_so_chu_de` `9,85s`/`13,31s`, `sua_lich_hoi_truoc` `5/5`).
- **Đã xong Đợt 2 (`aaafe678` + mở 2 cờ thành `66 MỞ / 7 TẮT`, `0,169822 USD` OpenAI):**
  - `goi_y_mua_nang` **GIỮ & BẬT** (`n=16` đo cặp `1/8 → 5/8`, `0/4` bão/lũ, `0/4` OOS, `p95 24,4s → 12,4s`, USD `-40,5%`, `0` lỗi citation).
  - `so_sanh_diem_den` **GIỮ & BẬT** (`n=14` đo cặp `1/8 → 6/8`, `0/3` hụt văn hoá, `0/3` OOS, `p95 22,2s → 13,2s`, USD `-37,3%`, `0` lỗi citation).
  - `MAX_VONG_CONG_CU_TOI_DA = 6` + ghi log tokens/`usd` cho `so_tay` & `ho_so_chu_de`.
  - `cong_cong_cu: luon` **GỠ / giữ `tu_khoa`**: lách từ khoá đạt `10/10` (`0/10` gọi thừa) nhưng đội `+44,50%` USD (`+89,0%` ở câu thuần kho do lặp danh sách 40 điểm ở schema & `cached=0`) ⇒ chuyển sang **Nấc 2B**.
- **Đang chạy Nấc 2B + Đợt 3A trên `/swarm` (`b2`, `c2`, `e2`):**
  - `b2` (nhánh `p20-b-nang-cap-2b-3a` tách từ `main` sau Đợt 2):
    - **Nấc 2B (`cong_cong_cu: "linh_hoat"`, giữ mặc định `"tu_khoa"`):** khử lặp bảng 40 địa điểm giữa `khoang_cach`, `gan_diem`, `so_sanh_diem_den` (chỉ in 1 lần) + gắn `prompt_cache_key` cố định cho `assistant_agent` để kích hoạt OpenAI Prompt Cache + giữ rào cứng bão/lũ và ngoài 7 ngày.
    - **Đợt 3A (`anh.che_do_tu_choi: "mac_dinh" | "confidence_gate"`, mặc định `"mac_dinh"`):** mở rộng `nhan_anh.py` + `app.py` + `routes/anh.py` kiểm soát 3 trường (`do_chac_chan`, `dau_hieu_dac_trung`, `ly_do_ngan` chỉ dùng nội bộ) và cổng backend xác định, không phá Q-f/Q-g/rào prompt injection.
  - `c2` (`0 USD`): chuẩn bị manifest đo Đợt 3A (`data/thu_harness_2026-11-27/bo_anh_dot3.json`) và script đo cặp OFF (`mac_dinh`) vs ON (`confidence_gate`) trên `gpt-6-luna`.
  - `e2`: review chéo `p20-b-nang-cap-2b-3a`, đo cặp **Nấc 2B** (`n=20`, tiêu chí lách từ khoá `>= 8/10`, gọi thừa `<= 1/10`, USD `<= +20%`) và **Đợt 3A** (`bo_anh_dot3.json`, tiêu chí giảm nhận nhầm `>= 40%` tương đối, recall dương không tụt quá `2` ảnh / `3,5%`, `0` tụt rào chữ dán trên ảnh), ghi `KET_LUAN_DOT2B_3A.md`.
- **Kế tiếp sau khi đóng Nấc 2B & Đợt 3A:** gọi `d2` cập nhật đồng bộ `bai_hoc/giao_trinh/` (nhờ `e2` review chéo), dọn nhánh tạm & thu gọn `/swarm`.
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
- **Tính năng (`backend/config/settings.yaml`):** **66 MỞ · 7 TẮT** (`anh.bat` + 65 cờ mở / 7 cờ tắt trong `assistant:`, sau khi mở `goi_y_mua_nang` & `so_sanh_diem_den`, giữ tắt `siet_tro_chuyen` và `cong_cong_cu: tu_khoa`).
- **Kho & Chỉ mục Qdrant (`hue_full_corpus_7a2_e5_small_384`):** **269 bài · 9.540 đoạn** (cập nhật 26/11; Khám phá **269/269** có ảnh).
- **Cả bộ test (`c2d0ee68` + chạy kiểm lại sau đợt sửa 17:13 25/11 + 26/11):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`data/test_rong_2026-11-22/KET_QUA_c2d0ee68.tsv`); sau Đợt 2 kiểm 6 file chạm **109 passed** (`13:43 27/11`).
- **Chi phí OpenAI phần test của nhóm:** **~0,98 USD** (`~0,81` tới trưa 27/11 + `0,042205` baseline Đợt 2 `c2` + `0,127617` đo cặp Đợt 2 `e2`) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
