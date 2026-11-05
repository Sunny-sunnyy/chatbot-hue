# Review sớm (một chỗ): B5b — miễn lỗi "không có [n]" ở lượt thời tiết · `p9-b5b` `b669981`

Người kiểm: E (Claude Opus 5.5, `hue-rag-bc`) · việc **E17** (A giao) · 21:24 05/11/2026 · 0 USD. Phạm vi: chỉ `backend/llm/assistant.py` `_thoi_tiet_cuoi` (đoạn miễn `NO_CITATION`) + test `test_no_citation_allowed_only_for_weather_tool_turns`; report `b168_b5b_implementation.md` §2 lệch 1.

**Kết luận: major — miễn đang rộng hơn cần; sửa trước lượt có phí.**
1. **Khối dự báo do code nối** (`tool["khoi"]` nối sau chữ model, sau kiểm; stream phát riêng `delta` sau phần model) — đúng. Nhưng thứ được miễn `[n]` là **chữ của model**, không phải khối.
2. **Lọt thật [Chạy, `_thoi_tiet_cuoi` + helper test của nhánh]:** lượt có công cụ, lỗi `NO_CITATION`, chữ model: (a) "Mai trời 23–27 °C." ⇒ qua (đúng ý) · (b) "Mai trời 23–27 °C. Đại Nội mở cửa 7h–17h, vé người lớn 200.000 đồng." ⇒ **qua, không `[n]`** · (c) "Mai có mưa nhẹ. Lăng Tự Đức đóng cửa vào thứ hai." ⇒ **qua**. Lượt thời tiết vẫn có ngữ cảnh kho (lần tìm đầu bằng câu gốc) ⇒ câu hỏi hai ý ("mai mưa không, Đại Nội mở mấy giờ?") cho model nêu giờ / giá kho không trích. `kiem_so` chỉ bắt số có đơn vị thời tiết (°C, mm, %) ⇒ không chặn (b).
3. **Cách hẹp hơn, đề xuất (nhỏ nhất):** chỉ miễn khi **mọi** con số trong chữ model (`_MOI_SO`, không chỉ số thời tiết) ⊂ `tap_so(khối)` — có số khác (giờ, giá, ngày) ⇒ giữ `NO_CITATION` ⇒ rút lại như hôm nay; mô tả công cụ thêm một câu "điều lấy từ tài liệu vẫn ghi mã [n]" (hướng dẫn, không phải rào). Còn hở (c) (sự thật kho không có số) ⇒ ghi giới hạn.
4. **Cách sạch hơn (nếu A muốn 0 miễn):** khối dự báo thành **một nguồn thật trong sổ nguồn** (id riêng, nhãn "Dự báo Open-Meteo, cập nhật …"), model trích `[k]` như nguồn kho ⇒ không nới bộ kiểm citation, đóng cả (c); tốn hơn (đường sổ nguồn + giao diện), phải đo lại hành vi trích của model.
5. **Test bất biến chưa đủ:** test hiện có phủ "có công cụ ⇒ miễn / mã lạ ⇒ rút / không công cụ ⇒ rút", **thiếu** ca "có công cụ + nội dung kho không `[n]`". Đóng: thêm (b) ⇒ rút lại (bắt buộc với cách 3), (a) ⇒ qua, (c) ⇒ ghi rõ là giới hạn (hoặc rút lại nếu chọn cách 4); chạy lại `test_b5b_thoi_tiet.py` + Q1 / Q1m (cờ tắt không đổi).

Dò: worktree `/tmp/e17` (`b669981`, symlink `data/` + `knowledge-base-hue/`) — gỡ được.
