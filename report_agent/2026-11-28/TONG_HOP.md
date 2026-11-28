# Tổng hợp đợt 28/11/2026 — Đợt 5 Phần A (100% Local, 0 OAuth), Đồng bộ Giáo trình & Phân tích `google-research/harness2`

**Thời gian:** 09:50 – 11:56 28/11/2026 (giờ `date`)  
**Điều phối:** Session A (`agy` CLI + `/swarm` gồm `builder`, `eval`, `verifier`, `docs`, `monitor`)  
**Phạm vi:** Triển khai và đo so cặp trước–sau toàn bộ **Đợt 5 — Phần A (100% local, 0 OAuth)** theo `data/dot5_multi_agent_2026-11-27/THIET_KE_DOT5.md` (trần OpenAI `<= 0,55 USD`, `0 USD` AWS), kết hợp đọc phân tích `google-research/harness2` (`0 USD`) và đồng bộ `bai_hoc/giao_trinh/`.

---

## 1. Kết quả gộp lên `main`
- **Gộp Đợt 5 — Phần A (`origin/p22-b-dot5a-local` @ `c493cdc1`):**
  - **Chuẩn hoá `CanonicalItinerary` (`backend/api/hanh_trinh_chuan.py`):** trích xuất cấu trúc lịch bất biến từ `lich_tu_luu`, khoá manifest ảnh tự host (`/anh/lich/`, `/anh/khach_san/`), loại bỏ toàn bộ chữ ghi công ảnh (`0%`), tách quyền sạch giữa RAG Agent, Slide Designer Agent và lớp xuất xác định.
  - **Lịch `.ics` v2 (`backend/api/lich_ics.py`, `GET /api/lich/ics`, `frontend/src/lich_ics.js` `dungIcsV2`):** thêm `VTIMEZONE Asia/Ho_Chi_Minh`, xử lý mục 1 mốc giờ (`90'`/`60'`) & không giờ (`VALUE=DATE`), thêm sự kiện nhắc nhận/trả phòng `o_dau` kèm disclaimer `"chưa kiểm giá, phòng trống"`, đưa `an_toan` lên đầu `DESCRIPTION`, thêm `URL;VALUE=URI:`, ổn định `UID` theo `{ngay_dau}-{id_muc}@tro-ly-hue`, và chặn `ngay_di = null` (`HTTP 400`).
  - **Deep Link OTA 3 sàn & Mẫu hỏi phòng (`backend/llm/luu_tru_lich.py`, `frontend/src/LichV2.jsx`, `ChoO.jsx`, `chat.jsx`, `co.css`, `tl.css`):** sinh link Booking/Agoda/Traveloka có `checkin`/`checkout`/`adults`/`children`/`rooms` qua `urlencode`/`quote_plus`, kiểm allowlist 3 host và chặn `..`/`%2e%2e` đồng bộ cả backend lẫn frontend (`linkPhongHopLe`), thêm nút **"Chép mẫu hỏi phòng"** 6 trường (`0 USD`), và vá CSS `flex-wrap: wrap` ở `.co-link` (`co.css:20`) và `.the-ks-link` (`tl.css:94`).
  - **`.pptx` v2 & `Slide Designer Agent` (`backend/api/pptx_catalog.py`, `pptx_fit.py`, `lich_pptx.py`, `backend/llm/slide_designer.py`, `routes/xuat.py`, `routes/cong.py`, `gioi_han.py`, `assistant.py`):** 3 bảng màu + 9 layout + đo tràn chữ 3 tầng + cắt ảnh trung tâm `Pillow` + trang `o_dau` + `notes_map` 2 cột + tách `Slide Designer Agent` (`slide_designer_cfg:` trước `assistant:` trong `settings.yaml`, cache theo `(itinerary_hash, theme_id)`). Đóng lỗ hổng rate-limit trên `GET /api/lich/pptx` (`use_llm=False`, `0 USD`; chỉ `POST /api/lich/pptx` chịu trọng số `3` trong `gioi_han.py`).
  - **Cấu hình & Runbook (`settings.yaml`, `deploy/docker/dong_goi.sh`, `guides/RUNBOOK_BAN_GIAO.md`):** **70 MỞ / 8 TẮT** (`xuat_nang_cao: true`, `slide_designer: true`); theo lựa chọn của chủ dự án lúc `11:25 28/11`, đặt `slide_designer_cfg.use_llm: true` để thử nghiệm xem slide AI trên máy demo, còn `dong_goi.sh` ép `use_llm: false` để bản deploy chạy chế độ code `0 USD / 0,36s`.
- **Gộp cập nhật giáo trình (`origin/p22-d-giao-trinh-dot5a` @ `6b01170b`):** `docs` cập nhật `25` file trong `bai_hoc/giao_trinh/`, `verifier` review chéo `READY` (`0` blocker/major, `A 195 · B 146 · C 266 · E 240 · F 204 · G 355 · H 214 · I 226`; không đưa Phần B chưa xây).

---

## 2. Số đo Trước–Sau & Kiểm chứng (`data/thu_dot5a_2026-11-28/KET_LUAN_DOT5A.md`)
- **Kiểm tra code & test (`c493cdc1`, sau khi build `frontend/dist`):**
  - 6 file chạm (`test_dot5a_slide_designer.py`, `test_dot5a_ics_deeplink.py`, `test_lich_pptx.py`, `test_chot_deploy.py`, `test_settings_env.py`, `test_static_ui.py`): **`45 passed`**.
  - `test_assistant_boundary.py`: **`4 passed`**.
  - `test_len_ke_hoach_v2.py` (chạy riêng với Qdrant `:6335`): **`95 passed, 1 failed`** (`test_v2_flag_needs_table_and_fails_loudly` có sẵn từ khi mở `goi_y_mua_nang: true` ở Đợt 2).
  - `git diff --check`: exit `0`; đếm cờ `settings.yaml`: **`70` `true` / `8` `false`**.
- **Cụm 1 — `.ics` v2 (`n = 20`):** bao phủ mục lịch `95,81% → 100,0%` (`191/191`, bỏ sót `8 → 0`), `VTIMEZONE` `0/18 → 18/18`, `URL;VALUE=URI:` `0/18 → 18/18`, check-in/out `o_dau` `0/18 → 17/17`, chặn `ngay_di=null` `2/2`, giữ ổn định `UID` `5/5` cặp (`13/13, 12/12, 10/10, 10/10, 19/19`).
- **Cụm 3 — Deep Link OTA & Mẫu hỏi phòng (`n = 15 + 12`):** `1/3 → 3/3` sàn (`15/15` lịch đủ ngày/khách/mẫu 6 trường), rào hai chiều `9/12 → 12/12`; Playwright cổng `8039` (`1536×695` & `390×844`) sạch `0` lỗi console, `0` thẻ xén chữ sau vá CSS, `0 px` tràn ngang mobile.
- **Cụm 2 — `.pptx` v2 & `Slide Designer Agent` (`n = 24`, A/A `n = 10`):**
  - **Baseline cũ (`28f8ea16`):** `0,0%` sạch bố cục (`277` ô tràn, `102` câu cắt `170`), `3,0` layout TB, `0,0%` trang `o_dau`, `p50/p95 = 0,108s / 0,203s`.
  - **Bản `.pptx` v2 code (`0 USD`):** **`100,0%`** sạch bố cục, **`5,95`** layout TB, **`100,0%`** `o_dau` (`22/22`), `0%` méo ảnh `>5%`, `0%` ghi công ảnh, **`p50/p95 = 0,211s / 0,358s`**.
  - **Bản `Slide Designer` `gpt-6-luna` (`POST /api/lich/pptx`):** **`100,0%`** sạch bố cục, **`6,23`** layout TB, **`100,0%`** `o_dau` (`22/22`), `23/24` LLM + `1` fallback `TimeoutError` sạch ở `20,5s`, **`p50/p95 = 17,239s / 28,676s`**, chi phí vòng 2 **`0,039778 USD`** (`0,001657 USD/deck`; tổng 2 vòng + A/A: **`0,120794 USD`** / trần `0,55 USD`). Đã soi trực tiếp 12 PDF/84 PNG và chép 3 cặp mẫu CODE vs AI tại `data/thu_dot5a_2026-11-28/mau_cho_hieu/`.
- **Nghiên cứu `google-research/harness2` (`0 USD`):** `@eval` hoàn tất `data/nghien_cuu_2026-11-28/HARNESS2_PHAN_TICH.md` từ mã nguồn thật (đã xoá `/tmp/hr_eval_harness2`).

---

## 3. Giới hạn & Việc gác lại
- Phần AI thiết kế slide (`use_llm: true`) có độ trễ `17,2s` trung vị / `28,7s` `p95` ở lần tải đầu mỗi lịch (đang mở thử nghiệm ở máy demo; lùi bằng 1 dòng `use_llm: false`, gói deploy đã ép sẵn `false`).
- Kiểm chuẩn RFC 5545 `.ics` dùng validator tự viết chặt trong test/script vì môi trường offline chưa cài được gói `icalendar` từ PyPI.
- Script `data/thu_dot5a_2026-11-28/chay_do_dot5a.py --che-do live` (nếu chạy lại sau này) cần chuyển sang `POST /api/lich/pptx` sau khi đóng `GET /api/lich/pptx` ở `use_llm=False`.
- Phần B (Google Workspace OAuth Testing mode) và Deploy AWS thật tiếp tục gác sang phiên sau.
