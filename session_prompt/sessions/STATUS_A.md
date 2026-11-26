# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 20:56 26/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất đợt dọn gọn tối 26/11/2026 (`0 USD` API, không bật `/swarm`, review chéo qua sub-agent ngữ cảnh sạch): gộp nhánh giáo trình `d`, ghép ảnh minh hoạ *Lễ Kỳ yên đình làng Huế* (`269/269`), bổ sung giờ mở cửa trung thực cho 4 bài kho + cập nhật chỉ mục Qdrant (`9.540 điểm`), đồng bộ runbook/giáo trình/sổ trạng thái, ghi kỷ luật commit/push lên `main`, và dọn sạch worktree + nhánh Git cũ.

## 2. Đã xong trong đợt 26/11 (`0 USD` API)
- **Review chéo & gộp nhánh giáo trình `origin/p15-d-don-giao-trinh-2511` (`b803b6fc`):** sub-agent bắt 4 finding (2 major ở `00_GIAO_TRINH.md` & `37_BAO_MAT_VA_DU_LIEU_NGUOI_DUNG.md`, 2 minor ở `05` & `PL_I`); đã sửa sạch cả 4 và khớp bộ đếm phụ lục (`A 184 · B 133 · C 250 · E 240 · F 191 · G 348 · H 210 · I 222`).
- **Ghép ảnh *Lễ Kỳ yên đình làng Huế* (`c51475f1`):** chuyển PNG sang `frontend/public/anh/kp/k1fycqz6.jpg`, cập nhật `frontend/src/anhBai.js`, dời PNG gốc sang `data/test_cuoi/ảnh test của hiếu/`, dựng lại `frontend/dist`, Khám phá đạt **269/269 (100 %)**.
- **Bổ sung giờ mở cửa trung thực 4 bài kho (`c51475f1`):** *Chùa Thiên Mụ*, *Hổ Quyền*, *Đàn Xã Tắc*, *Suối Voi* + `overlap_scan.py` + `ingestion.cap_nhat_rieng` (29,8 s, bản ghi & Qdrant đều **269 bài / 9.540 điểm**), chạy lại 4 file test liên quan đạt **86 passed**.
- **Đồng bộ tài liệu & kỷ luật repo:** cập nhật `RUNBOOK_BAN_GIAO.md` (`9.540`, `gpt-6-luna`, `bang_anh_v10.json` + `bang_luu_tru_lich_v7.json`, kiểm nạp `anh 47`), `TEST_2411_TRUA.md`, `WORKFLOW.md` §9.6, `HIEN_TRANG.md`, `VIEC_DANG_MO.md`, `VIEC_DA_XONG.md`, `CURRENT_HANDOFF.md`, `MEMORY.md`.
- **Dọn Git:** gỡ 2 worktree thừa tối 25/11 (`swarm-d-53d0f9ba`, `swarm-e-99ce8184`); xoá sạch toàn bộ nhánh đã gộp và nhánh nháp cũ không còn dùng (local còn đúng `main` + 9 nhánh giữ).

## 3. Đang làm / còn mở
- Không còn việc xây hay dọn tồn ở local. Các phần lớn vẫn gác chờ Hiếu tự mở lại: thuê GPU huấn luyện model nhận ảnh và triển khai lên AWS (`deploy/`).

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Đang giữ đúng kỷ luật chỉ push `main` gọn một lần sau review chéo cuối và kiểm `--chi-kiem` bộ đóng gói Docker.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `80xx`, `888x`:** đều đang TRỐNG.
- **Chi phí OpenAI đợt 26/11:** **0 USD** (lũy kế phần test của nhóm vẫn ~**0,74 USD** / trần **2–2,5 USD**).

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- Trong sandbox mặc định, `.git/` và loopback `127.0.0.1:6335` không mở ghi/nối nên các thao tác git ghi (`merge/commit/push/branch`) và lệnh đụng Qdrant chạy bằng `BypassSandbox: true`.
- `data/hoc_cung_D/tools/dem_hang_phu_luc.py` ghi cứng `/tmp/hr_d_giaotrinh` nên khi chạy trên cây chính cần đọc trực tiếp từ `bai_hoc/giao_trinh/`.

## 7. Ghi nhận thêm từ các phiên
- Giữ nguyên danh sách từ đợt trước cho vòng cải tiến tiếp nếu mở lại (`~/.gemini/config/mcp_config.json`, `chay_t1.py` `U1_KHONG_BAT`).
