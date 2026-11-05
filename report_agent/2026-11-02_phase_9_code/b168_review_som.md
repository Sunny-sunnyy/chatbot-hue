# Review sớm (một chỗ): B5b — miễn lỗi "không có [n]" ở lượt thời tiết · `p9-b5b` `b669981`

Người kiểm: E (Claude Opus 5.5, `hue-rag-bc`) · việc **E17** (A giao) · 21:24 05/11/2026 · 0 USD. Phạm vi: chỉ `backend/llm/assistant.py` `_thoi_tiet_cuoi` (đoạn miễn `NO_CITATION`) + test `test_no_citation_allowed_only_for_weather_tool_turns`; report `b168_b5b_implementation.md` §2 lệch 1.

**Kết luận: major — miễn đang rộng hơn cần; sửa trước lượt có phí.**
1. **Khối dự báo do code nối** (`tool["khoi"]` nối sau chữ model, sau kiểm; stream phát riêng `delta` sau phần model) — đúng. Nhưng thứ được miễn `[n]` là **chữ của model**, không phải khối.
2. **Lọt thật [Chạy, `_thoi_tiet_cuoi` + helper test của nhánh]:** lượt có công cụ, lỗi `NO_CITATION`, chữ model: (a) "Mai trời 23–27 °C." ⇒ qua (đúng ý) · (b) "Mai trời 23–27 °C. Đại Nội mở cửa 7h–17h, vé người lớn 200.000 đồng." ⇒ **qua, không `[n]`** · (c) "Mai có mưa nhẹ. Lăng Tự Đức đóng cửa vào thứ hai." ⇒ **qua**. Lượt thời tiết vẫn có ngữ cảnh kho (lần tìm đầu bằng câu gốc) ⇒ câu hỏi hai ý ("mai mưa không, Đại Nội mở mấy giờ?") cho model nêu giờ / giá kho không trích. `kiem_so` chỉ bắt số có đơn vị thời tiết (°C, mm, %) ⇒ không chặn (b).
3. **Cách hẹp hơn, đề xuất (nhỏ nhất):** chỉ miễn khi **mọi** con số trong chữ model (`_MOI_SO`, không chỉ số thời tiết) ⊂ `tap_so(khối)` — có số khác (giờ, giá, ngày) ⇒ giữ `NO_CITATION` ⇒ rút lại như hôm nay; mô tả công cụ thêm một câu "điều lấy từ tài liệu vẫn ghi mã [n]" (hướng dẫn, không phải rào). Còn hở (c) (sự thật kho không có số) ⇒ ghi giới hạn.
4. **Cách sạch hơn (nếu A muốn 0 miễn):** khối dự báo thành **một nguồn thật trong sổ nguồn** (id riêng, nhãn "Dự báo Open-Meteo, cập nhật …"), model trích `[k]` như nguồn kho ⇒ không nới bộ kiểm citation, đóng cả (c); tốn hơn (đường sổ nguồn + giao diện), phải đo lại hành vi trích của model.
5. **Test bất biến chưa đủ:** test hiện có phủ "có công cụ ⇒ miễn / mã lạ ⇒ rút / không công cụ ⇒ rút", **thiếu** ca "có công cụ + nội dung kho không `[n]`". Đóng: thêm (b) ⇒ rút lại (bắt buộc với cách 3), (a) ⇒ qua, (c) ⇒ ghi rõ là giới hạn (hoặc rút lại nếu chọn cách 4); chạy lại `test_b5b_thoi_tiet.py` + Q1 / Q1m (cờ tắt không đổi).

Dò: worktree `/tmp/e17` (`b669981`, symlink `data/` + `knowledge-base-hue/`) — gỡ được.

---

## Vòng 2 — kiểm phần sửa `a0906a6` (cha `b669981`; A chọn cách 4) · 21:38 05/11/2026 · E (việc **E18**)

**Kết luận: đạt** (0 major; 1 minor). Diff 4 file (`assistant.py`, `thoi_tiet.py`, `full_corpus_prompt.py`, `test_b5b_thoi_tiet.py`), +52 / −37.
- **Khối dự báo là nguồn thật:** `_nguon_thoi_tiet` thêm `PackedSource` id tiếp theo vào sổ nguồn (khuôn `_block` như đoạn kho, `source="open-meteo"` — không trùng tiền tố H4c), đếm vào ngữ cảnh; API lỗi ⇒ nguồn "chưa lấy được" với câu `CAU_LOI` (không chữ số). **Chỗ miễn `NO_CITATION` đã gỡ** ⇒ bộ kiểm citation giống `main`. Mô tả công cụ thêm "ý kho vẫn ghi đúng mã [n]".
- **Dò lại [Chạy, 0 USD] qua đường thật của test** (`run` ⇒ generator kịch bản ⇒ kiểm citation ⇒ `_thoi_tiet_cuoi`; file dò tạm, không commit, đã xoá): (a) chỉ dự báo không mã ⇒ **rút** · (b) kho có số không mã ⇒ **rút** · (c) kho không số không mã ⇒ **rút** · (d) dự báo có `[k]` ⇒ **qua** · (f) API lỗi, model trích `[k]` rồi tự viết "30 °C" ⇒ **rút** (`weather numbers without source`) · (e) "dự báo `[k]`. Đại Nội mở cửa 7h–17h." (câu kho không mã cạnh câu có mã) ⇒ qua — **giới hạn chung có sẵn ở `main`** (`select_cited_sources` đòi ≥ 1 mã hợp lệ, không đòi từng câu), không còn là chỗ nới riêng của B5b.
- Test: cả file `test_b5b_thoi_tiet.py` (65) + 6 ca dò ⇒ **71 passed**. Q1 / Q1m: dùng lại của B (report b168 §7) — sửa chỉ chạm đường cờ bật.
- **m-1 (minor):** `git diff --check b669981 a0906a6` ⇒ `backend/tests/test_b5b_thoi_tiet.py:315: new blank line at EOF` — xoá dòng trống cuối file.
