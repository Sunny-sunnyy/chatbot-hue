# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 11:56 27/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đang điều hành **Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent trên `gpt-6-luna`** qua `/swarm` (`b2`, `c2`, `e2`, `monitor`). Đã đóng gọn **Đợt 1** và chuẩn bị mở **Đợt 2**.

## 2. Đã xong trong trưa 27/11 (Đợt 1: `0 USD` AWS, `~0,052–0,059 USD` OpenAI)
- **Đợt 1A — GIỮ & BẬT (`e432e32c` + mở `chong_lap_cong_cu` & `cuu_max_turns`, thành `64 MỞ / 7 TẮT`):** đo cặp `gpt-6-luna` `n=14` giảm `max_turns` `1/14 → 0/14`, cứu `1a_multi_03` (`8` nguồn hợp lệ, `0` lỗi citation), `p95` giảm `14,5 → 12,0 s`, `trajectory_eval.py` hoạt động (`0,029046 USD`).
- **Đợt 1B — GỠ / GIỮ TẮT (`siet_tro_chuyen: false`):** trên `n=18` câu đã thấy, bên TẮT đã `0/6` lọt `tro_chuyen`, bật lên `CHƯA RÕ` mà tăng `+8,5%` chi phí (`0,010259 USD`).
- **Đợt 1C — ĐẠT (`c2` chạy, `e2` đối chiếu):** `so_tay` (`9,92s` / `16,47s`), `ho_so_chu_de` (`9,85s` / `13,31s`), `sua_lich_hoi_truoc` (`5/5`) đều chạy mượt trên `gpt-6-luna` (`0,004828 USD` đo log + `~0,0083–0,0149 USD` ước).
- **Thiết kế Đợt 2–3:** `data/thu_harness_2026-11-27/THIET_KE_DOT2_DOT3.md` + 3 góp ý chỉnh của `e2`.

## 3. Đang mở tiếp (Đợt 2 & Đợt 3)
- **Đợt 2:** `goi_y_phuong_an_mua_nang` + `so_sanh_diem_den` + đo `cong_cong_cu: luon` vs `tu_khoa` + vá ghi `usd`/tokens cho `so_tay.py` & `ho_so.py`.
- **Đợt 3:** tối ưu Hỏi bằng ảnh 0 GPU trên `gpt-6-luna` (`confidence_gate`).
- **Cuối chiến dịch:** gọi `d2` cập nhật đồng bộ `bai_hoc/giao_trinh/` và dọn nhánh tạm.

## 4. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8039`, `8880`:** đều đang TRỐNG.
- **Chi phí OpenAI lũy kế phần test của nhóm:** ~**0,81 USD** / trần **2–2,5 USD**.
