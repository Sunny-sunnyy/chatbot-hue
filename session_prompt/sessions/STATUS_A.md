# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 13:43 27/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đang điều hành **Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent · 0-GPU Image QA trên `gpt-6-luna`** qua `/swarm` (`b2`, `c2`, `e2`, `monitor`). Đã đóng **Đợt 1** và **Đợt 2**; đang mở song song **Nấc 2B** & **Đợt 3A**.

## 2. Đã xong trong 27/11 (Đợt 1 + Đợt 2: `0 USD` AWS, `~0,222–0,229 USD` OpenAI)
- **Đợt 1A — GIỮ & BẬT (`e432e32c` + mở `chong_lap_cong_cu` & `cuu_max_turns` ở `d67375f2`):** `n=14` giảm `max_turns` `1/14 → 0/14`, cứu `1a_multi_03`, `p95` `14,5 → 12,0 s` (`0,029046 USD`).
- **Đợt 1B — GỠ / GIỮ TẮT (`siet_tro_chuyen: false`):** `CHƯA RÕ` trên `n=18`, tăng `+8,5%` chi phí (`0,010259 USD`).
- **Đợt 1C — ĐẠT:** `so_tay` (`9,92s` / `16,47s`), `ho_so_chu_de` (`9,85s` / `13,31s`), `sua_lich_hoi_truoc` (`5/5`).
- **Đợt 2 — GIỮ & BẬT `goi_y_mua_nang` + `so_sanh_diem_den` (`aaafe678` + mở cờ thành `66 MỞ / 7 TẮT`, `109 passed`, `0,169822 USD`):** `mua_nang` (`1/8 → 5/8`, `0/4` bão/lũ, USD `-40,5%`), `so_sanh` (`1/8 → 6/8`, `0/3` hụt văn hoá, USD `-37,3%`), khoá `MAX_VONG_CONG_CU_TOI_DA = 6`, log usage/USD cho `so_tay` & `ho_so_chu_de`; riêng `cong_cong_cu: luon` **GỠ** (giữ `tu_khoa`) vì đội `+44,50%` USD dù lách từ khoá `10/10`.

## 3. Đang mở tiếp (Nấc 2B & Đợt 3A)
- **Nấc 2B:** `cong_cong_cu: linh_hoat` (khử lặp bảng 40 địa điểm giữa `khoang_cach` / `gan_diem` / `so_sanh` + `prompt_cache_key` cố định cho `assistant_agent` + giữ rào cứng bão/lũ, ngoài 7 ngày).
- **Đợt 3A:** `anh.che_do_tu_choi: confidence_gate` trong `nhan_anh.py` + `app.py` + `routes/anh.py` giảm nhận nhầm `15/73` trên `gpt-6-luna`.
- **Cuối chiến dịch:** gọi `d2` cập nhật đồng bộ `bai_hoc/giao_trinh/` (nhờ `e2` kiểm chéo) và dọn nhánh tạm / thu gọn `/swarm`.

## 4. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8039`, `8880`:** đều đang TRỐNG.
- **Chi phí OpenAI lũy kế phần test của nhóm:** ~**0,98 USD** / trần **2–2,5 USD**.
