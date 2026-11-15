# Lịch lọc cơ sở ven biển theo `phia_bien` — B · 10:56 15/11/2026

Việc (E đề xuất, A giao 15/11): ô "Nơi ở" của lịch tách hai phía ven biển bằng trường `phia_bien` của bảng v3 (cùng trường trang "Chỗ ở" dùng) thay cho dò
chữ "Phú Vang / Thuận An / Phú Lộc / Lăng Cô" trong địa chỉ. Nhánh `p9-phia-bien` từ main `60f556b`; hàm thuần ⇒ chỉ test file chạm (W76).

- **Đổi:** `backend/llm/luu_tru_lich.py` — `PHIA_BIEN` (chữ địa chỉ) ⇒ `PHIA_CUM = {"dong_bien": "bac", "nam_xa": "nam"}`, lọc `c["phia_bien"] == PHIA_CUM[cum_dau]`;
  `nap_bang_luu_tru` đã kiểm mọi cơ sở ven biển có `phia_bien` (C). Test mô phỏng 3.840 khung kiểm phía bằng bảng (map viết lại độc lập).
- **Mô phỏng** (`data/ngan_sach_o_2026-11-15/tools/so_phia_bien.py`, backend main ↔ nhánh, 3.840 khung × 4 lựa chọn ngân sách = 15.360 ô Nơi ở):
  **72 đổi** = 36 lịch ven biển phía bắc × (không chọn, "4–5 sao"): **thêm** SBH Gloria (4 sao, bảng ghi `phia_bien: bac`, có ảnh), không bỏ cơ sở nào
  (trước bị loại vì địa chỉ không ghi tên huyện). Mức "1 sao / đạt chuẩn" và "2–3 sao": 0 đổi. Đúng như E dự đoán (chỉ Gloria).
- **Test:** `tests/test_luu_tru_lich.py` 15 đạt (11 s). Không server / Playwright (hàm thuần, không chạm chat / route). 0 USD.
- **Giới hạn:** phía của Gloria theo bảng v3 (C gán, E review); không kiểm lại toạ độ ở nhánh này.
- Kèm: sửa số "12 ⇒ 36" trong `b_ngan_sach_o_implementation.md` thành số đếm thật 13 ⇒ 32 (C, `dem_sau.json`).
