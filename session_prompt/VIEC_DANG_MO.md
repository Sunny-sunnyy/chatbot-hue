# Việc đang mở (sổ việc — cập nhật 11:56 28/11/2026, đã kết đợt sạch Đợt 5A)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent trên `gpt-6-luna` (đã xong Đợt 1 + Đợt 2 + Nấc 2B + Đợt 3A + Nghiên cứu chuyên sâu + Đợt 4A + Giáo trình `b1b69754`)
- **Đã hoàn tất & đồng bộ lên `main` (`d67375f2`, `aa333ca`, `79cb4dea`, `d341fd96`, `442055ba`, `b1b69754`):**
  - **Đợt 4A (`cd217536`, `f245963c`, `442055ba`, `b1b69754`; tổng chi phí OpenAI thật `0,265824 USD`):**
    - Đánh giá 3 tầng trên nền Golden 176 câu: `backend/evaluation/faithfulness_eval.py` đạt **`15/15 = 100%`** kiểm định nhãn tay (`3/3` bắt gán sai `[n]`), mốc nền Golden 20 đạt **`88,33%`** (`17/20` strict, `0` misattributed); `ToolCallAccuracy` (`0 USD`) trong `trajectory_eval.py` xác nhận khớp Đợt 2 (`19/20 = 95%`); thêm `cached_tokens` vào log `anh.py`.
    - **GIỮ & BẬT `canh_bao_vong_con_lai: true`:** đo cặp `n=18` giảm `cuu_max_turns` `2 → 0`, cắt `50%` gọi thừa (`6 → 3`), `ToolCallAccuracy` F1 `0,831 → 0,849`, cache bước `>=2` `91,00% → 94,58%`, USD **`-6,84%`**.
    - **GIỮ & BẬT `toi_uu_dot2_va_viet_lai: true`:** đo cặp `n=38` nâng `H2_mua_nang` **`4/8 → 8/8`** (USD `-4,3%`), `H2_so_sanh` **`5/8 → 7/8`** (`ToolCallAccuracy` `0,500 → 0,875`, USD `-16,4%`), giảm tổng USD **`-10,02%`** (giới hạn: `_chan_doan_viet_lai` mới kiểm unit test `0/8` live; `vl_01` gọi nhầm `thoi_tiet(bao_lu)` ở vòng 7).
    - **GIỮ TẮT `kiem_du_bang_chung: false`:** `n=36` nền đã tránh bịa `18/18`, bật thêm `+0/18`, tốn `+10,7%` USD và 1 ca bỏ sót `khoang_cach` (`suf_mix_17`).
    - **Giáo trình (`b1b69754`, `0 USD`):** `docs` cập nhật `22` file `bai_hoc/giao_trinh/`, `verifier` review chéo `READY` (`0` blocker/major, `A 192 · B 144 · C 262 · E 240 · F 200 · G 353 · H 212 · I 225`).
    - Hồ sơ đo: [KET_LUAN_DOT4A.md](data/thu_dot4_2026-11-27/KET_LUAN_DOT4A.md).
  - **Đợt 1:** `1A` **GIỮ & BẬT** (`chong_lap_cong_cu: true`, `cuu_max_turns: true`, `trajectory_eval.py`: `max_turns` `1/14 → 0/14`, `p95 14,5 → 12,0 s`); `1B` **GỠ / GIỮ TẮT** (`siet_tro_chuyen: false`); `1C` **ĐẠT** trên `gpt-6-luna`.
  - **Đợt 2:** `goi_y_mua_nang: true` (`1/8 → 5/8`, `0/4` bão/lũ, USD `-40,5%`) + `so_sanh_diem_den: true` (`1/8 → 6/8`, `0/3` hụt văn hoá, USD `-37,3%`) + khoá `MAX_VONG_CONG_CU_TOI_DA = 6` + log USD `so_tay`/`ho_so`.
  - **Nấc 2B — GIỮ & BẬT (`cong_cong_cu: linh_hoat`):** `n=20` lách từ khoá `0/10 → 9/10`, gọi thừa `0/5`, ngoài phạm vi `5/5`, USD **`-15,23%`**, `cached_tokens` `46,5% → 76,9%` (`83,5%` ở kho thuần), `p95 16,1s → 11,5s`, `0` lỗi (`KET_LUAN_DOT2B_3A.md`).
  - **Đợt 3A — GIỮ `mac_dinh` (`anh.che_do_tu_choi: mac_dinh`):** `n=76` ảnh (`0,070648 USD`) `confidence_gate` giảm FP `-50%` (`10/18 → 5/18`) nhưng tụt recall dương `-17` top-1 / `-20` top-3 (`49/55 → 32/55` / `52/55 → 32/55`) ⇒ giữ `mac_dinh`.
  - **Nghiên cứu chuyên sâu (`0 USD`, đã xoá `/tmp/hr_*_repos/`):** `c2` ([KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md](data/nghien_cuu_2026-11-27/KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md)) & `b2` ([DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md](data/nghien_cuu_2026-11-27/DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md)).
- **Còn chờ xét nếu làm tiếp tối ưu RAG/Ảnh (0 GPU):** `anh_hoi_lai_goi_y` vùng xám kiểu ReCoVERR (giữ nguyên tắc trả lời trước) · chạy `faithfulness_eval` cho trọn 176 câu Golden hoặc sau khi bật kết hợp `V2+V3` · tool `goi_y_luu_tru` / `tim_kho` thuần nghĩa (`che_do="y_nghia"`).
- **Nguyên tắc:** mọi thay đổi code mới nằm sau công tắc tắt, đo so cặp với bản cũ theo `run-experiment` — tốt hơn vượt nhiễu mới giữ, kém hơn thì giữ bản cũ, xong cập nhật báo cáo + giáo trình.
- **Đã đóng hẳn (`10:55 27/11/2026`, không nhắc lại):**
  - Thuê GPU + fine-tune model nhận ảnh (giữ nguyên tính năng Hỏi bằng ảnh 55 tên đang chạy bằng `gpt-6-luna`; `goi_may_thue.tar` giữ nguyên không xoá).
  - `MCP Server`; mảng DevSecOps / Supply Chain CVE / Red-Teaming / FinOps.
- **Vẫn gác (chờ chủ dự án tự mở lại khi rảnh):**
  - Bước triển khai thực tế lên AWS (`deploy/`): chờ chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày (khi đóng gói thật nhớ chạy lại `dung_anh.sh origin/main`).

### A.1b. Đợt 5 — Multi-Agent & Tính tự chủ (Phần A **ĐÃ XONG & GỘP `main` 28/11/2026** · Phần B gác chờ triển khai)
- **Phần A (100% local, 0 OAuth — ĐÃ HOÀN TẤT & GỘP `main` từ `origin/p22-b-dot5a-local` @ `c493cdc1` + giáo trình `6b01170b`, `0,120794 USD` OpenAI):**
  - Đã hoàn thành `CanonicalItinerary` (`hanh_trinh_chuan.py`), `.ics` v2 (`lich_ics.py`, `GET /api/lich/ics`, `dungIcsV2`), Deep Link 3 sàn Booking/Agoda/Traveloka + nút chép mẫu hỏi phòng 6 trường (`luu_tru_lich.py` + đồng bộ allowlist 3 file giao diện + vá CSS `co.css:20`/`tl.css:94`), `.pptx` v2 + `Slide Designer Agent` (`pptx_catalog.py`, `pptx_fit.py`, `slide_designer.py`, `lich_pptx.py`, `xuat.py`, `gioi_han.py`, 0 ghi công ảnh).
  - Cấu hình hiện hành: `xuat_nang_cao: true`, `slide_designer: true`, `slide_designer_cfg.use_llm: true` (thử nghiệm ở máy demo theo xác nhận `11:25 28/11` để Hiếu xem slide AI, đổi 1 dòng `use_llm: false` về chế độ code `0đ / 0,36s`; `deploy/docker/dong_goi.sh` ép `use_llm: false`).
  - Hồ sơ & 3 cặp mẫu CODE vs AI cho Hiếu xem: [KET_LUAN_DOT5A.md](data/thu_dot5a_2026-11-28/KET_LUAN_DOT5A.md) & [mau_cho_hieu](data/thu_dot5a_2026-11-28/mau_cho_hieu/).
- **Phần B (Google OAuth Testing mode — gác chờ phiên sau / khi Hiếu sẵn sàng tạo OAuth Client):**
  - Calendar (`calendar.events` `events.import` upsert), Google Slides & Sheets 5 tab (`drive.file`), Gmail Draft (`gmail.compose` chỉ tạo nháp, không `send`).
  - *(Lưu ý trước khi làm Phần B: sửa checklist cổng mẫu `localhost:8000 → localhost:8010` trong [THIET_KE_DOT5.md](data/dot5_multi_agent_2026-11-27/THIET_KE_DOT5.md#L234-L240) cho khớp `scripts/bat_he_thong.sh`.)*
- **Tài liệu thiết kế:** [THIET_KE_DOT5.md](data/dot5_multi_agent_2026-11-27/THIET_KE_DOT5.md) (`242` dòng) & [B_PHAN_TICH_KY_THUAT.md](data/dot5_multi_agent_2026-11-27/B_PHAN_TICH_KY_THUAT.md) (`455` dòng).

### A.2. Nợ kỹ thuật nhỏ (gom làm khi sửa file liên quan, không mở đợt riêng)
- **Độ dài tên trong gói deploy `gpt-6-luna`:** kiểm lại chỗ cắt tên hoặc chữ dài nếu phát hiện trong thực tế (E ghi chú sau rà).
- **Chuẩn hoá 1–2 dòng docstring/comment nhỏ** còn dư từ đợt rà B (`ho_so_chu_de` / `sua_lich_hoan_tac`) nếu có dịp chạm file.
- **Theo dõi ca `vl_01` Đợt 4A:** kiểm tra `0 USD` vì sao câu hỏi ghép 4 vế có chữ `"qua đêm"` gọi nhầm `thoi_tiet(bao_lu)` ở vòng 7 khi có dịp chạm từ khoá thời tiết.

### A.4. Nhánh Git đang giữ (sau đợt dọn sạch tối 26/11 + Đợt 5A 28/11)
- **Đã gộp lên `main` (26–28/11, chờ dọn nếu Hiếu duyệt):** các nhánh Đợt 1–4A (`p15-d-don-giao-trinh-2511`, `p16..p20`, `p21-c-eval-dot4a`, `p21-b-harness-dot4a`, `p21-d-giao-trinh-dot4a`) và Đợt 5A (`p22-b-dot5a-local`, `p22-d-giao-trinh-dot5a`).
- **Nhánh hồ sơ / bản thử còn giữ đối chiếu (9 nhánh):** `thu-b-mo-doc-tiep` · `thu-c-khung-truoc` · `thu-b-ba-duong-tim` · `thu-b-dem-loi-dan` · `p9-b-dem-y-go-tat-2` · `p9-c-ve-loi-nho` · `p9-c-sua-2-het-vong` · `p9-b-vong-cuoi-chu-2` · `p9-e-chi-sang-len-ke-hoach`.

## B. Chỉ số nền & Trần OpenAI của nhóm
- **Model viết mặc định (từ 15:41 25/11):** `gpt-6-luna` (`full_corpus_generation.provider: openai`).
- **Tính năng (`backend/config/settings.yaml`):** **70 MỞ · 8 TẮT** (`anh.bat` + 69 cờ mở / 8 cờ tắt trong `assistant:`), kèm **`cong_cong_cu: linh_hoat`** (Nấc 2B), **`anh.che_do_tu_choi: mac_dinh`** (Đợt 3A), và **`slide_designer_cfg.use_llm: true`** (thử nghiệm local; `dong_goi.sh` ép `false`).
- **Kho & Chỉ mục Qdrant (`hue_full_corpus_7a2_e5_small_384`):** **269 bài · 9.540 đoạn** (cập nhật 26/11; Khám phá **269/269** có ảnh).
- **Cả bộ test (`c2d0ee68` + kiểm chạm Đợt 4A `442055ba` + Đợt 5A `c493cdc1`):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`KET_QUA_c2d0ee68.tsv`); kiểm chạm sau Đợt 5A trên `c493cdc1`: 6 file chạm **`45 passed`** + `test_assistant_boundary.py` **`4 passed`** + `test_len_ke_hoach_v2.py` **`95 passed, 1 failed`** (`test_v2_flag_needs_table_and_fails_loudly` có sẵn từ Đợt 2); kiểm sau Đợt 4A: `108 passed` + `88 passed`.
- **Chi phí OpenAI phần test của nhóm:** **~1,47 USD** (`~1,35` tới Đợt 4A + `0,120794` Đợt 5A) / trần cũ **2–2,5 USD** (chủ dự án 27/11 đã xác nhận sẵn sàng duyệt thêm nếu vượt).
