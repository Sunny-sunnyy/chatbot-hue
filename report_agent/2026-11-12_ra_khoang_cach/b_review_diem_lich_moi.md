# Review bảng nháp 7 điểm lịch mới (E) — B · 13:30 15/11/2026 · 0 USD

Nháp `data/diem_lich_moi_2026-11-15/diem_moi_nhap.json` (chưa vào bảng main). **Kết luận: ready_for_user_confirmation, 3 minor.**

- **Trích kho:** 13 / 13 câu / số trích ở các trường giờ, buổi, trong nhà, lưu ý **có thật đúng file:dòng** (`scripts/grep_kb.sh`; Từ Hiếu :42, Trường Tiền :38 :39 :51, Bến Ngự :43 :80–82,
  Tây Hồ :37, An Hiên :6 :11, Lập An :11 :164, Hải Vân :15). Kho **không** ghi giờ mở Hải Vân Quan (chỉ giờ đẹp 07h–09h / 15h30–17h, `Vé tham quan Hải Vân Quan.md:179–180`) ⇒ dùng web là đúng.
- **Trích web (WebFetch B):** Hải Vân Quan khớp nguyên văn ("Daily, 7:00–17:30", "Plan 30–45 minutes…", "checked October 2026").
- **m-1 Chợ Bến Ngự:** `thoi_luong_can_cu` ghi "E mở trang kiểm 15/11" nhưng trang trả **403** (E báo; B thử lại cũng 403) ⇒ sửa chữ thành "Codex mở, E / B chưa tự đọc được"; thời lượng 2 giờ (`nua_buoi`) chỉ dựa 1 nguồn chưa tự kiểm ⇒ thêm 1 nguồn thứ hai hoặc để `ngan` + ghi giới hạn.
- **m-2 Làng nón Tây Hồ:** cụm `an_cuu` (bảng tả "~3,5–4 km") mà điểm gần nhất ~6 km, toạ độ là chùa làng đại diện ⇒ có thể bị xếp chung buổi với An Cựu như "gần" — ghi rõ trong `vi_tri_can_cu` + để User biết khi duyệt.
- **m-3 Hải Vân Quan giờ mở:** chỉ 1 nguồn web (đã kiểm) ⇒ ghi "1 nguồn" ở can_cu. Thời lượng "ngắn" không tính đường ~70 km: bộ xếp không cho ngày có cụm `nam_xa` trộn cụm khác
  (`backend/llm/lich_trinh_v2.py:460`) và không đặt cụm xa ngày 1 (`:217`) ⇒ không thành lịch phi lý.
- Đã đúng như E báo: Từ Hiếu `ngoai_troi` cùng cách nhãn với Chùa Thiên Mụ trong v8; mô phỏng 3.840 khung 0 lỗi `kiem_khung` (`mo_phong.json`).
- **Kiểm lại 13:33 15/11/2026:** E sửa chữ căn cứ (giá trị bảng không đổi) — m-1 cờ "1 nguồn, chưa tự đọc (403)" ⇒ User quyết; m-2 ghi khoảng cách cụm; m-3 ghi "1 nguồn" ⇒ **đóng cả 3**.
