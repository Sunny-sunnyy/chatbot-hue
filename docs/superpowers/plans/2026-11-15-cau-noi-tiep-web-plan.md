# Plan — câu hỏi nối tiếp: mục web mang đúng chủ thể · B · bản 1 · 15:49 15/11/2026

Mức nhẹ (≤ 0,2 USD, không đổi kiến trúc). Căn cứ đếm + nguyên nhân gốc: `report_agent/2026-11-12_ra_khoang_cach/b_cau_noi_tiep_dem.md` (tái tạo 2 / 2).
**Căn cứ để review:** `backend/llm/assistant.py` (`cong_web`, `tool_for_turn`, `web_gate_open`) · `backend/llm/tra_web.py` (`cau_tim_web`, `dau_vao_model`) · `data/phase_9/bo_do_b3/README.md` mục sàn "0 truy vấn web chứa tên".

## 1. Lỗi và cỡ của nó

Lượt hỏi tiếp không nêu lại tên nơi / món + kho không có điều được hỏi ⇒ kho từ chối đúng ⇒ code tra web bằng **nguyên câu lượt này** (không tên) ⇒ mục web nói về nơi khác. Tái tạo 2 / 2 (có và không đại từ).
Phần kho không lỗi: model viết câu tìm kho nêu đúng tên ở 9 / 9 lần. Tần suất ở người dùng thật chưa biết (chưa có log người thật); User gặp ngay trong buổi tự thử đầu ⇒ đáng sửa.

## 2. Đổi MỘT thứ (nhánh `p9-web-noi-tiep`, cờ `web_cau_noi_tiep`, mặc định tắt)

Khi lượt **có lịch sử** và model đã tự tìm kho ít nhất một lần: câu dùng cho phần web (cả câu gửi tra web lẫn câu đưa model viết mục web) = **câu tìm kho cuối cùng model đã viết ở lượt này** thay cho câu người dùng gõ.
Câu đó vẫn đi qua `cau_tim_web` (bỏ email / số điện thoại, ≤ 120 ký tự, thêm "Huế"). Không thêm lần gọi model, không đổi lời dặn, không đổi cổng web.
- Lượt không lịch sử, hoặc model không tìm lần nào ⇒ **y như hôm nay** (giống byte).
- Phương án đã cân và bỏ: (a) code ghép câu 1 + câu 2 — đếm 0 USD: phá 2 / 3 cặp đổi chủ đề; (b) thêm một lần gọi model viết lại câu đứng một mình cho mọi lượt có lịch sử — sửa được cả lần tìm đầu nhưng +1 lần gọi (~1,5 s, thêm tiền) ở mọi lượt hỏi tiếp, để dành nếu (chính) không đạt; (c) đưa lịch sử vào lần viết mục web — không sửa được câu gửi tra web.

## 3. Tiêu chí (ghi trước)

- **Bộ đo:** 2 cặp đã thấy của B + **10 cặp mới do một session khác viết** (B không viết bộ quyết của chính mình): 6 cặp "hỏi tiếp + kho thiếu" (3 không chủ ngữ, 3 có đại từ), 2 cặp "đổi chủ đề thật + kho thiếu", 2 cặp "nêu tên mình ở lượt 1 rồi hỏi tiếp + kho thiếu". Mỗi cặp 1 lượt, đường stream thật, tra web thật. Không bộ kín.
- **Sàn (code đếm):** (S1) 0 câu gửi tra web chứa tên người dùng — 3 chuỗi cũ `web_neu_ten` + 2 cặp mới; (S2) cờ tắt ⇒ câu gửi tra web + chuỗi gửi model giống byte; cờ bật + lượt không lịch sử ⇒ giống byte (test, 0 USD ⇒ 10 câu "web trả lời được" của bộ B6 không cần chạy lại);
  (S3) cặp đổi chủ đề: câu gửi tra web **không** chứa chủ thể lượt 1 — 0 / 2 sai; (S4) mọi kiểm cuối mục web bằng code giữ nguyên (test).
- **Chỉ số quyết:** trên 8 cặp hỏi tiếp + kho thiếu (2 đã thấy + 6 mới): câu gửi tra web nêu đúng chủ thể **≥ 7 / 8** (so chữ bằng code; mốc 0 / 2) **và** mục web nói về đúng chủ thể hoặc là câu cố định an toàn, **0 mục nói về nơi khác** (B đọc tay + người review đọc lại; mốc 2 / 2 nói về nơi khác).
- **Theo dõi:** kết quả mục web theo loại; USD / lượt (không đổi số lần gọi ⇒ kỳ vọng như cũ).
- **Giữ khi:** đủ sàn + chỉ số quyết ⇒ A trình User bật. S1 phạm ⇒ dừng, không chỉnh vòng (đổi sang phương án (b) phải có plan mới).

## 4. Tiền, test, review

≈ 12 cặp × 2 lượt × ~0,003 + tra web 12 × 0,001 + 3 chuỗi cũ ≈ **0,10 USD**, trần 0,15. Test: file chạm (`test_b6_tra_web.py` + test mới cho 4 loại lượt: đầu / có lịch sử có tìm / có lịch sử không tìm / lượt nút) có và không khoá; test rộng một lần trước bàn giao. Một review cả nhánh.

## 5. Khi nào sai

- Câu tìm kho cuối của model hẹp hơn câu hỏi (model tách ý) ⇒ mục web chỉ trả lời một phần — bộ đo có cặp 2 lần tìm để thấy.
- Model chép tên người dùng vào câu tìm kho ⇒ tên ra ngoài: S1 bắt; đây là rủi ro chính của hướng này.
- Lượt hỏi tiếp mà kho từ chối ngay, model không tìm lần nào ⇒ vẫn lỗi như cũ (0 / 2 đã thấy; đếm trong bộ đo).

## 6. Rà khung AI FDE (ngắn)

| Mục | Hiện trạng | Khớp / lệch | Đề xuất |
|---|---|---|---|
| Đường ra: gửi gì | `tra_web.cau_tim_web`: chỉ câu người dùng gõ ở lượt này | **đổi có chủ đích** — cần A / User nhận: câu **model viết** (có tên nơi lấy từ lượt trước) ra ngoài thay câu gõ | vẫn qua bộ lọc email / số điện thoại + cắt 120 ký tự; S1 đo tên người dùng |
| Chữ model là dữ liệu | câu tìm kho của model hiện chỉ dùng trong hệ thống | lệch mới: dùng làm truy vấn ngoài | không dùng làm gì khác; không log chữ (chỉ cờ `web_cau_tu_model: true` trong mục `tools`) |
| Quyết bằng code | cổng web do code quyết | khớp — không đổi | — |
| Kiểm đầu ra | `tra_web.kiem_muc_web` | khớp — không đổi | — |
