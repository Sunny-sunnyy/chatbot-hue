# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 16:49 27/11/2026 (giờ `date`) — **ĐÃ KẾT PHIÊN SẠCH.**

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất trọn **Đợt 4A** (Đánh giá 3 tầng trên nền Golden 176 câu + Tối ưu Harness/Tools trên `gpt-6-luna`), gộp code + mở 2 cơ chế đạt ngưỡng (**68 MỞ / 8 TẮT** ở `442055ba`), gộp đồng bộ `22` file giáo trình `bai_hoc/giao_trinh/` (`b1b69754`), và hoàn tất bản thiết kế **Đợt 5 (Multi-Agent & Tính tự chủ)** gác sẵn cho các phiên sau.

## 2. Đã xong trong phiên chiều 27/11 (15:11 – 16:49, `0 USD` AWS, `0,265824 USD` OpenAI)
- **Đợt 4A Eval (`cd217536`, `41e45fed`, `38 passed`):** `backend/evaluation/faithfulness_eval.py` (kiểm định `15/15 = 100%`, bắt `3/3` gán sai `[n]`; mốc nền Golden 20 đạt `88,33%` / `17/20` strict, `0` misattributed), `ToolCallAccuracy` (`0 USD`) trong `trajectory_eval.py`, bộ đo tại `data/thu_dot4_2026-11-27/`.
- **Đợt 4A Harness & Tools (`f245963c` + `442055ba`, `108 + 88 passed` sau sửa cuối):**
  - **GIỮ & BẬT `canh_bao_vong_con_lai: true`:** `cuu_max_turns` `2 → 0`, gọi thừa `6 → 3`, `ToolCallAccuracy` F1 `0,831 → 0,849`, cache bước `>=2` `91,00% → 94,58%`, USD **`-6,84%`**.
  - **GIỮ & BẬT `toi_uu_dot2_va_viet_lai: true`:** `H2_mua_nang` `4/8 → 8/8`, `H2_so_sanh` `5/8 → 7/8` (`ToolCallAccuracy` `0,500 → 0,875`), tổng USD **`-10,02%`**.
  - **GIỮ TẮT `kiem_du_bang_chung: false`:** nền đã tránh bịa `18/18`, bật thêm `+0/18`, tăng `+10,7%` USD và 1 ca bỏ sót `khoang_cach`.
  - Vá log `cached_tokens` ở `backend/api/routes/anh.py` + đồng bộ `guides/RUNBOOK_BAN_GIAO.md`.
- **Giáo trình (`b1b69754`, `0 USD`):** `docs` cập nhật `22` file `bai_hoc/giao_trinh/`, `verifier` review `READY` (`A 192 · B 144 · C 262 · E 240 · F 200 · G 353 · H 212 · I 225`).
- **Thiết kế Đợt 5 (`0 USD`, gác cho phiên sau):** `data/dot5_multi_agent_2026-11-27/THIET_KE_DOT5.md` (`242` dòng) + `B_PHAN_TICH_KY_THUAT.md` (`455` dòng).

## 3. Việc gác lại cho phiên sau
- **Đợt 5 (Multi-Agent & Tính tự chủ — 3 cụm):** triển khai từ `THIET_KE_DOT5.md` (Phần A `0 OAuth` trước: `.ics` v2, Deep Link Booking/Agoda/Traveloka, mẫu tin hỏi phòng, Slide Designer Agent `.pptx`; rồi Phần B: Google OAuth Testing mode cho Calendar, Slides, Sheets, Gmail Draft).
- **Deploy AWS thật (`deploy/`):** vẫn gác chờ Hiếu chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày (khi đóng gói nhớ chạy `dung_anh.sh origin/main`).

## 4. Tài nguyên & Chi phí lúc kết phiên
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8039`, `8880`:** đều đang TRỐNG.
- **Swarm:** sẽ `kill` sạch các worker trước khi báo Hiếu kết phiên, không còn worktree dở.
- **Chi phí OpenAI lũy kế phần test của nhóm:** ~**1,35 USD** (`~1,08` tới Đợt 3A + `0,265824` Đợt 4A; Hiếu đã duyệt sẵn nếu vượt trần cũ `2–2,5 USD`).
