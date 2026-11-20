# VIỆC ĐÃ XONG — mỗi việc một dòng, để tìm lại hồ sơ (nối thêm ở cuối)

Bắt đầu ghi: 11:08 19/11/2026 (giờ `date`). [đang thử từ 19/11] Việc rời `VIEC_DANG_MO.md` thì ghi một dòng ở đây: tên việc · ngày xong · sha gộp vào main · thư mục ngày có report · thư mục riêng tư.

| Việc | Xong | Sha gộp | Report | Riêng tư |
|---|---|---|---|---|
| Bỏ trần token đầu ra (User yêu cầu) | 19/11/2026 | `193e972` | `report_agent/2026-11-19/TONG_HOP.md` | `data/phase_9/bo_max_token/` |
| Bỏ ngân sách ngữ cảnh + trần lịch sử theo token (User yêu cầu) | 19/11/2026 | `6938ab7` | `report_agent/2026-11-19/TONG_HOP.md` | `data/phase_9/bo_ngan_sach/` |
| Sửa lịch bằng lời: câu "dời hai điểm" (cờ `sua_lich_doi_cho_code` bật) | 19/11/2026 | `dc69768`, bật cờ `c03156f` | `report_agent/2026-11-19/b_sua_lich_doi_cho_implementation.md` | `data/phase_9/sua_lich_doi_cho/` |
| Câu thiếu cảnh báo "tạm ngừng": bản code (cờ `noi_dong_tam_ngung` bật); bản lời dặn không đạt | 19/11/2026 | `55d01a8` | `report_agent/2026-11-19/c_s09_noi_dong_tam_ngung_implementation.md` | `data/phase_9/s09_code/`, `data/phase_9/s09_luu_y/` |
| Vòng máy tự dò cấu hình bước tìm (0 / 15 vượt nhiễu) | 19/11/2026 | `0f06e00` | `report_agent/2026-11-19/b_tu_toi_uu_buoc_tim_implementation.md` | `data/cach_lam_2026-11-18/tu_toi_uu/` |
| Lượt đo cuối Phase 9 phần đã thấy + mốc "xong phần nhóm kèm mục chưa đạt" | đo 18/11, mốc 19/11/2026 | mốc code `55d01a8` | `report_agent/2026-11-19/b_do_cuoi_b7_implementation.md` | `data/phase_9/b7_cuoi/` |
- Thí nghiệm mức suy luận low · medium · high — xong 19/11/2026 — giữ mức mặc định (không đổi code); báo cáo vào main `b712475` — hồ sơ `report_agent/2026-11-19/b_muc_suy_luan_implementation.md`, `bai_hoc/VIEC_MOI_XONG.md` mục 12, riêng tư `data/phase_9/muc_suy_luan/`.
- Đưa ngữ cảnh lớn hơn vào model (15 đoạn / cả mục / cả bài) · xong 19:17 19/11/2026 · không đề nghị nhánh nào, giữ 10 đoạn · báo cáo gộp `8ed8023` + `ed6f250` · hồ sơ `report_agent/2026-11-19/`, riêng tư `data/ngu_canh_lon_2026-11-19/` (còn nợ: mục `bai_hoc/`).
- "Kho có một phần thì bỏ cả câu / tìm thêm rồi từ chối" · đóng 21:50 19/11/2026 bằng GHI GIỚI HẠN (User chọn sau khi đếm: hai cổng hẹp do code kiểm được chỉ với tới khoảng 3–6 lượt, rủi ro sát sàn ngoài kho; áp chung từng thử 14/11 phạm sàn) · không code · hồ sơ riêng tư `data/tra_loi_mot_phan_2026-11-19/PLAN.md` (bản `3981b1cac149`, không duyệt), `data/bo_ca_cau_2026-11-19/bo_C/` (bộ nháp), tra cứu `data/tra_cuu_cli/2026-11-19_tra-loi-mot-phan-rag/`.
- Lịch đã lưu vào lượt hỏi thường · bật 19/11/2026 · gộp `1a9a0f8`, bật `62a2762` · `report_agent/2026-11-19/c_lich_da_luu_implementation.md` · riêng tư `data/lich_da_luu_2026-11-19/`.
- Nói thật giới hạn ở việc "làm thay" · bật 19/11/2026 · gộp `26ccef9`, bật chung `b71e1e9` · riêng tư `data/tu_choi_khuon_2026-11-19/`.
- Xuất lịch PDF + PowerPoint · bật 19/11/2026 · gộp `4dbbaca`, bật chung `b71e1e9` · `report_agent/2026-11-19/e_xuat_lich_implementation.md` · riêng tư `data/xuat_lich_dep_2026-11-19/` (trước deploy: giới hạn số lượt tải).
- Hỏi tiếp về nơi vừa nêu (cờ `nho_ten_goi_y`) · bật 19/11/2026 · gộp squash `7a27705`, bật chung `b71e1e9` · `report_agent/2026-11-19/b_nho_ten_goi_y_implementation.md` · riêng tư `data/hoi_tiep_goi_y_2026-11-19/` (còn việc sửa nhỏ: `VIEC_DANG_MO.md` việc 2).
- Đo lại bộ 80 kịch bản ở điểm dừng · 19/11/2026 · main `b71e1e9` · xong việc 51 ⇒ 58, 0 điều sai mới · riêng tư `data/kich_ban_pho_thong_2026-11-19/luot_2/`.
- Gõ "lên lịch giúp mình" trong ô chat ⇒ câu cố định · đóng 19/11/2026 KHÔNG gộp (lỗi đích không còn tái hiện 0 / 6 + 0 / 6 lượt) · nhánh hồ sơ `origin/p9-e-chi-sang-len-ke-hoach` `d0249b1` · riêng tư `data/len_lich_chat_2026-11-19/`.
- "Câu xin danh sách trả thiếu mục" · đóng 19/11/2026 bằng GHI GIỚI HẠN (runbook 10.1) · riêng tư `data/kich_ban_pho_thong_2026-11-19/dem_danh_sach_thieu_muc_C.md`.
- Sửa nhỏ cờ `nho_ten_goi_y`: câu hỏi tiếp chỉ xin liệt kê lại các nơi vừa nêu thì lượt đó không nhận dòng ghi chú · 20/11/2026 · main `2d43d76` (code `a1f4df5`) · bắt nhầm 0 / 32 + 0 / 3 trên hai bộ dò, nhận đúng 9 / 20 + 5 / 5; lỗi có sẵn danh sách thiếu mục còn nguyên (runbook 10.1) · `report_agent/2026-11-20/b_nho_ten_liet_ke_lai_implementation.md` · riêng tư `data/kich_ban_pho_thong_2026-11-19/viec_2_sua_nho/`.
