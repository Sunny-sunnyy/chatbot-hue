# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 14:57 27/11/2026 (giờ `date`) — **ĐÃ KẾT PHIÊN SẠCH.**

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã kết thúc gọn **Chiến dịch Tối ưu Harness · Agentic RAG · Tools · Agent · 0-GPU Image QA trên `gpt-6-luna`** (Đợt 1, Đợt 2, Nấc 2B, Đợt 3A), **2 báo cáo nghiên cứu chuyên sâu Paper/Repo**, và **đồng bộ giáo trình `bai_hoc/giao_trinh/` (`d341fd96`)**; toàn bộ `8` worker `/swarm` đã được `kill` sạch sau khi đẩy lên `origin/main` (`29ad79e8`).

## 2. Đã xong trong 27/11 (`0 USD` AWS, ~`0,321–0,328 USD` OpenAI cả chiến dịch)
- **Đợt 1 (`d67375f2`, `~0,052–0,059 USD`):** **GIỮ & BẬT** `chong_lap_cong_cu` + `cuu_max_turns` (`max_turns` `1/14 → 0/14`, `p95 14,5 → 12,0 s`), giữ tắt `siet_tro_chuyen`, thông `1C` 3 cụm.
- **Đợt 2 (`aa333ca`, `0,169822 USD`, `66 MỞ / 7 TẮT`):** **GIỮ & BẬT** `goi_y_mua_nang` (`1/8 → 5/8`, USD `-40,5%`) + `so_sanh_diem_den` (`1/8 → 6/8`, USD `-37,3%`), khoá `MAX_VONG_CONG_CU_TOI_DA = 6`, log USD `so_tay`/`ho_so`.
- **Nấc 2B & Đợt 3A (`75f545c6` + `79cb4dea`, `0,099352 USD`):** **GIỮ & BẬT `cong_cong_cu: linh_hoat`** (`9/10` lách từ khoá, `0/5` gọi thừa, USD **`-15,23%`**, `cached_tokens` `46,5% → 76,9%`); **GIỮ `anh.che_do_tu_choi: mac_dinh`** (do `confidence_gate` làm tụt recall dương `-17` top-1 dù giảm FP `-50%`).
- **Nghiên cứu chuyên sâu (`0 USD`, đã xoá `/tmp/hr_*_repos/`):** `c2` ([KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md](../../data/nghien_cuu_2026-11-27/KHAO_SAT_CHUYEN_SAU_PAPER_REPO_2026.md)) & `b2` ([DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md](../../data/nghien_cuu_2026-11-27/DOC_CODE_REPO_RAG_EVAL_VA_DE_XUAT.md)).
- **Giáo trình (`d341fd96`, `0 USD`):** `d2` đồng bộ `21` file `bai_hoc/giao_trinh/`, `e2` duyệt `READY` (`0` blocker, `0` leak).

## 3. Chờ phiên sau
- Phiên mới mở theo `START_SESSION.md` đọc ngay các ứng viên Đợt 4 trong 2 báo cáo nghiên cứu nếu Hiếu chọn chạy tiếp, hoặc hỗ trợ deploy AWS thật khi Hiếu rảnh.

## 4. Tài nguyên & Chi phí lúc kết phiên
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8039`, `8880`:** đều đang TRỐNG.
- **Swarm:** đã `kill` hết toàn bộ `8` worker (`b`, `c`, `e`, `b2`, `c2`, `d2`, `e2`, `monitor`), không còn worktree dở.
- **Chi phí OpenAI lũy kế phần test của nhóm:** ~**1,08 USD** / trần **2–2,5 USD**.
