# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 11:56 28/11/2026 (giờ `date`) — **ĐÃ KẾT ĐỢT SẠCH ĐỢT 5 — PHẦN A.**

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất trọn **Đợt 5 — Phần A (100% local, 0 OAuth)** từ [THIET_KE_DOT5.md](../../data/dot5_multi_agent_2026-11-27/THIET_KE_DOT5.md), gộp code + cấu hình **70 MỞ / 8 TẮT** (`c493cdc1`), dựng mới `frontend/dist`, gộp đồng bộ `25` file giáo trình (`6b01170b`), hoàn tất phân tích `google-research/harness2` (`0 USD`) và chuẩn bị 3 cặp mẫu slide tại `data/thu_dot5a_2026-11-28/mau_cho_hieu/`.

## 2. Đã xong trong đợt sáng–trưa 28/11 (09:50 – 11:56, `0 USD` AWS, `0,120794 USD` OpenAI)
- **Đợt 5 — Phần A (`c493cdc1` gộp lên `main`, `45 + 4 + 95 passed` trên các file kiểm chạm):**
  - **Chuẩn hoá `CanonicalItinerary` (`backend/api/hanh_trinh_chuan.py`):** tách quyền 3 Agent sạch (`0` rò OAuth/chat/web, `0` ghi công ảnh).
  - **`.ics` v2 (`backend/api/lich_ics.py`, `GET /api/lich/ics`, `frontend/src/lich_ics.js`):** `191/191 = 100%` mục lịch (`soBo: 8 → 0`), `VTIMEZONE Asia/Ho_Chi_Minh` (`18/18`), `URL;VALUE=URI:` (`18/18`), nhắc check-in/out `o_dau` (`17/17`), chặn `ngay_di=null` (`2/2`), giữ ổn định `UID` `5/5` cặp.
  - **Deep Link OTA 3 sàn + Mẫu hỏi phòng (`luu_tru_lich.py`, `LichV2.jsx`, `ChoO.jsx`, `chat.jsx`, `co.css`, `tl.css`):** `3/3` sàn Booking/Agoda/Traveloka kèm ngày/khách/phòng + nút chép mẫu hỏi phòng 6 trường (`15/15`), rào hai chiều `12/12`, Playwright cổng `8039` (`1536×695` & `390×844`) `0` lỗi console, `0` thẻ xén chữ.
  - **`.pptx` v2 & `Slide Designer Agent` (`pptx_catalog.py`, `pptx_fit.py`, `slide_designer.py`, `lich_pptx.py`, `xuat.py`, `gioi_han.py`, `dong_goi.sh`):** bản code `0 USD` đạt `100%` sạch bố cục (`0% → 100%`), `100%` trang `o_dau`, `5,95` layout TB, `0%` méo ảnh, `p95=0,358s`; bản AI `gpt-6-luna` đạt `100%` sạch, `100%` `o_dau`, `6,23` layout TB, `0,001657 USD/deck`, `p50/p95=17,24s/28,68s`. Theo chốt của Hiếu (`11:25`), đặt `slide_designer_cfg.use_llm: true` thử nghiệm ở máy demo, `dong_goi.sh` ép `use_llm: false`, `GET /api/lich/pptx` giữ `0 USD`.
- **Nghiên cứu `google-research/harness2` (`0 USD`):** `@eval` đọc trực tiếp repo và ghi [HARNESS2_PHAN_TICH.md](../../data/nghien_cuu_2026-11-28/HARNESS2_PHAN_TICH.md), đã xoá `/tmp/hr_eval_harness2`.
- **Giáo trình (`6b01170b` gộp lên `main`, `0 USD`):** `@docs` cập nhật `25` file `bai_hoc/giao_trinh/`, `@verifier` review `READY` (`A 195 · B 146 · C 266 · E 240 · F 204 · G 355 · H 214 · I 226`).

## 3. Việc gác lại
- **Đợt 5 — Phần B (Google OAuth Testing mode):** Calendar (`calendar.events`), Google Slides & Sheets (`drive.file`), Gmail Draft (`gmail.compose`) — gác phiên sau.
- **Deploy AWS thật (`deploy/`):** gác chờ Hiếu rảnh.

## 4. Tài nguyên & Chi phí lúc kết đợt
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8039` / server tạm:** đã tắt sạch, không còn worktree tạm.
- **Swarm:** sẽ `kill` sạch các worker trước khi báo Hiếu kết đợt.
- **Chi phí OpenAI lũy kế phần test của nhóm:** ~**1,47 USD** (`~1,35` tới Đợt 4A + `0,120794` Đợt 5A).
