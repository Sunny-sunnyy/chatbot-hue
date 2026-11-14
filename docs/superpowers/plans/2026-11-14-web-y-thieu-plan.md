# Plan (mức nhẹ): mục web của câu nhiều ý chỉ tra phần ý thiếu — C

Cập nhật: 15:33 14/11/2026 (C). A giao (lỗi "nói chắc sai" trên giao diện). Không đổi kiến trúc, ≤ 0,05 USD ⇒ A đọc rồi duyệt, một review cả nhánh.

## Lỗi đã thấy
Câu "ý kho có + ý ngoài kho" (luật theo ý chạy) ⇒ cổng web tra bằng **cả câu hỏi**. Hệ quả: mục "Từ web (chưa kiểm)" viết lại cả ý kho đã trả lời, với số khác kho (giờ mở cửa 6:30 ↔ 7:00).
Thấy ở cả 4 / 4 lượt có mục web (6 lượt tra) trong lượt đo `p9-so-y-va` (`data/so_y_va_2026-11-14/do_r.jsonl`; A và T4, mỗi câu 2 lượt).

## Đổi gì (code quyết, không thêm lần gọi model)
- `llm/assistant.py` `cong_web`: khi `trace.nhieu_y` và câu trả lời có dòng "Tư liệu chưa có thông tin về: …":
  - tách câu người dùng thành các vế hỏi (cùng cách tách với `so_y`);
  - chọn vế có nhiều từ chung nhất với các dòng ý thiếu;
  - dùng **vế đó** cho cả truy vấn Serper (`cau_tim_web`) và câu hỏi đưa model viết mục web (`dau_vao_model`).
- Không có dòng ý thiếu / không chọn được vế ⇒ dùng cả câu như hôm nay.
- **Chỉ chữ của người dùng đi ra ngoài** (giữ D2): dòng ý thiếu do model viết chỉ dùng để *chọn* vế, không gửi Serper.
- Câu một ý / cờ `cau_nhieu_y` tắt ⇒ đường không đổi (test: truy vấn giống hệt cũ).

## Đo (theo luật "đo phần đổi")
- **Câu chạm = câu đi luật theo ý VÀ có dòng ý thiếu.**
  - Golden 176: 0 câu `so_y ≥ 2` ⇒ không chạy.
  - An toàn 32: 4 câu `so_y ≥ 2` (S02, S05, S19, S27) ⇒ chạy 4 câu × 2 lượt.
  - Hỏi kèm 10 (cả bộ là câu hai ý) ⇒ chạy 1 lượt.
  - 3 câu "kho + ngoài kho" của lượt so_y ⇒ chạy × 2 lượt.
- **Sàn** (chỉ tính trên câu chạm):
  - mục web không nêu lại ý kho đã trả lời (đọc tay: 0 / n câu có số / giờ của ý kho trong mục web);
  - an toàn: không tệ hơn lượt trước trên cùng 4 câu;
  - 0 câu ngoài kho bị trả lời bằng kho.
- **Test:** chọn vế (3–4 câu nhỏ); câu một ý ⇒ truy vấn giống cũ; `test_cau_nhieu_y.py` + `test_tra_web*.py`.
- **Tiền:** ≈ 0,02–0,03 USD (Serper + gọi model viết mục web).

## Bảng AI FDE (rút gọn)
| Mục | Hiện trạng | Khớp / lệch | Đề xuất |
|---|---|---|---|
| Code ↔ model | vế tra do code chọn; model chỉ viết mục web như cũ | khớp | — |
| Đường ra ngoài | Serper nhận một phần câu người dùng (ít chữ hơn cả câu) | khớp D2, hẹp hơn | — |
| Dữ liệu model viết đi ra ngoài | không (dòng ý thiếu chỉ để chọn) | khớp | — |
| Phục hồi | không chọn được ⇒ cả câu như cũ | khớp | — |
