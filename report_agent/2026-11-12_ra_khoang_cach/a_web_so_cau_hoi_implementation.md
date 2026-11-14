# Mục web: số có sẵn trong câu hỏi không bị coi là số bịa · A · 17:54 14/11/2026

Nhánh `p9-web-so-cau-hoi`. 0 USD (không gọi model / Serper / Qdrant). Căn cứ: `e_dem_web_thay_cau.md` (E, 16 / 21 mục bị thay là năm người dùng gõ).

## Đổi gì
- `backend/llm/tra_web.py` `kiem_muc_web`: thêm tham số `cau_hoi`; luật `so_ngoai_trich` trừ chuỗi số có trong câu hỏi. Luật tiền (`tien_ngoai_trich`) **không đổi** — tiền người dùng gõ vẫn phải có trong đoạn trích.
- `backend/llm/assistant.py`: truyền `cau_hoi=query` (câu gốc của người dùng, không phải câu đã thêm "chỉ viết cho phần…").
- Chuỗi gửi model không đổi (chỉ phép kiểm sau khi model viết) ⇒ không cần lượt có phí (luật "Đo đúng chỗ đổi").

## Kiểm
- [Chạy] `tests/test_b6_tra_web.py`: 100 passed (thêm 1 test: năm / tháng trong câu hỏi qua; số model tự thêm vẫn chặn; tiền trong câu hỏi vẫn chặn; không truyền câu hỏi ⇒ như cũ).
- [Chạy] Đếm lại trên 76 mục đã lưu (script E, thêm `cau_hoi=r["query"]`; bản sửa ở `/tmp/a_dem/dem_moi.py`): bị thay **21 ⇒ 10** (có mục 62 / 76 = 81,6 %). 10 còn lại: tiền ngoài trích 4 (đúng) · số "39" model thêm 1 (đúng) · đoạn không mã 1 · **4 mục một câu: model tóm "01/5/2026" thành "tháng 5/2026"** ⇒ chuỗi số khác ⇒ chặn (phía an toàn, giới hạn cách so chuỗi số đã biết; không sửa).
- E dự kiến 21 ⇒ 5; thật 21 ⇒ 10 vì 4 mục trên — E đếm theo luật cũ cả số không đến từ câu hỏi.

## Rủi ro
Bản 1 miễn mọi chuỗi số trong câu hỏi ⇒ C review M-1: tiền đề sai (giờ / ngày / số nhà) người dùng gõ có thể thành "nói chắc sai", trong khi cả 11 mục cứu được chỉ nhờ năm. **Bản 2 (sửa theo review): chỉ miễn năm 19xx / 20xx đứng riêng**; giờ / ngày / số nhà / tiền người dùng gõ vẫn phải có trong đoạn trích. Chấp nhận phần còn lại vì một năm lặp lại từ câu hỏi chỉ đi với "chưa xác minh được …" hoặc nói về năm người dùng hỏi.
