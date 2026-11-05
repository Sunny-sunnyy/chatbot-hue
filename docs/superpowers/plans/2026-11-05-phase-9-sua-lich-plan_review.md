# Review: plan Phase 9 "sửa lịch nhiều lượt" (`sua_lich`, ý #8 + #9)

## Vòng 1 — bản 2 (sha tính từ file `1aa47fa2fd41`, E, 13:27 05/11/2026)

Decision: **changes_requested** (0 blocker · 2 major · 4 minor) — luật mới: tối đa 2 vòng; vòng 2 chỉ còn minor ⇒ ready.
Người kiểm: E (Claude Opus 5.5, `hue-rag-7a`) · A giao (+ kiểm thêm: bảng rà FDE, `ROUTE_INPUTS` của #6, không lặp lỗi "hỏi lại lần hai", giá trị đã nói không bị ghi đè).
Cách: chỉ bảng "Căn cứ để review" của plan + đọc code `main` (`ba0c187`, có #6 `5a8aa5e` + B5 `d66f6a3`) theo file + hàm ghi trong căn cứ. 0 USD. Không đọc STATUS / tin của C.

### Đã khớp (không finding)
- Ý #8 đủ: khung giữ ở server (D1), hành động có tên (D3), xếp lại cùng luật B5 + giữ chỗ không bị chạm (D5), "Đã đổi / Giữ nguyên / Chưa làm" do code (D7), thay điểm ⇒ 2–3 điểm cùng cụm để bấm (D6),
  ≤ 2 hành động / lượt + nêu ý không làm (D4), tránh 2 lỗi gộp Travel-AI (D5: `loai` không quay lại; gộp `ThamSo`). Ý #9: chuỗi sửa kiểu người thật, chạy lặp (pass^2 — A quyết).
- **`ROUTE_INPUTS` (#6):** hôm nay `("history", "truong", "search_query")` (`assistant.py`); trace phụ chỉ mang các trường này ⇒ D2 thêm `lich_cu` là **đúng và bắt buộc** (thiếu ⇒ trace phụ không thấy khung ⇒ không đưa `sua_lich`); §8 có điều kiện dừng. `_merge_spec` giữ `ROUTE_INPUTS` của trace chính, chép phần còn lại từ trace phụ chỉ khi tuyến = `tro_ly_hue`.
- Q1 / Q1m: lượt không có khung ⇒ danh sách công cụ như B5 ⇒ so byte thay hồi quy Golden / an toàn — hợp lý (đường B5 đã qua Q4). Q4 phủ câu khẩn cấp / ngoài phạm vi **sau** lịch (lúc `sua_lich` được đưa).
- Bộ kín quyết ngay ở plan (luật 05/11 (2)) — có lý do (chỉnh mô tả công cụ nhiều vòng).

### Findings

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-1** | major | D1, D2, D6 (đường dữ liệu khung) | Các hàm B5 **sửa khung tại chỗ**: `lich_trinh.bo_diem(khung, …)` (`ng["buoi"][b].remove(id_)`, `khung["khong_xep"].append`), `cat_ngay_cuoi` (`khung["ngay"].pop()`). Plan D2 đặt `trace.lich_cu` từ cuộc rồi thêm vào `ROUTE_INPUTS` — trace phụ #6 chép **tham chiếu** (`AnswerTrace(**{name: getattr(trace, name)})`). Nếu `sua_lich` / `ap_hanh_dong` áp hành động trên `lich_cu` (cùng đối tượng với `Conversation.lich` trong RAM) thì khung đã lưu **đổi ngay**, kể cả khi: tuyến cuối ≠ `tro_ly_hue` (#6 huỷ trace phụ), lượt bị kiểm cuối rút lại, lượt dừng ở thẻ chọn D6 | Trái D1 "chỉ lưu sau lượt qua kiểm cuối"; lượt sau sửa trên khung người dùng chưa từng thấy (điểm bị bỏ âm thầm) — đúng loại lỗi bậc này muốn chặn; harness 1 chuỗi có thể không bắt (lỗi chỉ hiện ở lượt kế sau lượt hỏng) | D1 / D2 ghi: route đặt `trace.lich_cu = copy.deepcopy(<khung đã lưu>)` (hoặc khung bất biến); `sua_lich` chỉ ghi **`trace.lich_moi`** (bản riêng); **chỉ route** lưu `lich_moi` vào cuộc, sau kiểm cuối, từ trace chính (đã merge ⇒ chỉ khi tuyến `tro_ly_hue`). Test: (i) #6 tuyến khác ⇒ khung lưu không đổi; (ii) kiểm cuối hỏng ⇒ không đổi; (iii) thẻ chọn ⇒ không đổi tới lượt `sua_chon`; (iv) hai lượt liên tiếp `bo_diem` ⇒ lượt 2 thấy đúng khung của lượt 1 |
| **M-2** | major | §7 tiền ↔ §6 bước 4–5 ↔ §8 | Chính bảng §7: 1 vòng (không chỉnh) = 0,01 + 0,07 + 0,035 + 0,02 + 0,01 = **0,145 ≈ mốc dừng 0,15**; vòng chỉnh 2 (+0,02) ⇒ 0,165 > **trần 0,16**. §6 cho chỉnh ≤ 3 vòng | Có **bất kỳ** vòng chỉnh nào ⇒ chạm dừng trước kín / Q4 / Q8 ⇒ bậc không đi hết như chữ plan; quyết lúc chạy sẽ thành "cắt gì" tuỳ hứng | Ghi trước **một** cách: (a) A xin User trần đủ cho 2 vòng chỉnh (≈ 0,19–0,20) **trước** lượt có phí; hoặc (b) thứ tự cắt ghi trước: pilot = 2 chuỗi đầu của đã thấy (không chạy lại), vòng chỉnh chạy chuỗi hỏng ×2 + 2 đối chứng ×1, Q8 1 chuỗi, chỉnh tối đa 2 vòng — kèm bảng cộng lại ≤ 0,15 |
| m-1 | minor | §5 "Cỡ mẫu" | còn "≥ 8 / 10 **pass^3**" sau khi đổi sang pass^2 (bản 2) | đọc lệch | sửa thành pass^2 |
| m-2 | minor | D5, Q2 (c) "giá trị đã nói không bị ghi đè" | Code không biết trường nào **người dùng đã nói** ↔ **mặc định công khai** (D4b B5), và `doi_tham_so` có thể được model điền đủ trường (kể cả trường người dùng không nhắc) ⇒ ghi đè đúng lỗi Travel-AI mà sàn chỉ bắt được nếu nhãn biết | Q2 (c) khó chấm tất định; người dùng không thấy giá trị cũ bị đổi | `lich` lưu thêm `da_noi` (trường lấy từ tham số / nút ở lượt lịch, không phải mặc định); `doi_tham_so` chỉ nhận trường **khác** giá trị lưu; đổi một trường `da_noi` ⇒ D7 có dòng "Đã đổi <trường>: <cũ> → <mới>"; Q2 (c) so `da_noi` trước / sau với nhãn |
| m-3 | minor | D6 thẻ chọn ↔ Q2 (g) | Thẻ chọn chỉ có các điểm code đưa; không có lối ra "không thay"; không ghi luật cho lượt mang `sua_chon` (B5 D15 có luật "lượt mang `truong` không hỏi lần hai"; B5 bản 6 từng có vòng hỏi không dứt) | người dùng không muốn điểm nào ⇒ phải gõ, model có thể gọi lại `thay_diem` không `ten_moi` ⇒ thẻ lần hai | thêm nút "Bỏ điểm này, không thay" (code áp `bo_diem`) + luật "lượt mang `sua_chon` ⇒ không đưa thẻ chọn" + test; Q2 (g) đếm cả thẻ chọn |
| m-4 | minor | §9 bảng rà FDE | Thiếu cột **hiện trạng** (file + hàm) và **đề xuất** (`Session_Prompt.md` §7 — bảng rà khung) | khó đối chiếu | thêm hai cột, vd `conversations.py` `Conversation` (hôm nay chỉ `turns`), `assistant.py` `ROUTE_INPUTS` (3 trường), `lich_trinh.py` `bo_diem` (sửa tại chỗ — M-1) |

### Giới hạn
- Không chạy code (plan chưa code); M-1 suy từ đọc `lich_trinh.py` + `assistant.py` [Code, chưa chạy]. Không mở bộ đo (chưa có).

### Decision và bước tiếp
**changes_requested** — C sửa M-1, M-2 (+ minor) thành bản 3, báo sha; E kiểm vòng 2 (vòng cuối theo luật 2 vòng). Không gấp (code chỉ bắt đầu khi B5 bật).

## Vòng 2 — bản 3 (sha tính từ file `5b68f3cb666a`, E, 13:31 05/11/2026) — vòng cuối (luật 2 vòng)

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 0 minor mới) — A duyệt sha. 0 USD.
Cách kiểm: sha tính từ file; đọc "Chỗ đổi bản 3" + D1, D2, D5, D6, §3, §5, §6, §7, §9; grep "3 vòng / vòng 3 / pass^3" ⇒ 0 chỗ sót.

| Finding | Kiểm | Kết luận |
|---|---|---|
| **M-1** khung sửa tại chỗ | D1: đọc / ghi bằng `copy.deepcopy`, **chỉ route ghi**, sau kiểm cuối, từ trace chính (#6: chỉ khi tuyến `tro_ly_hue`); rút lại / lỗi / huỷ / thẻ chọn không ghi. D2: `trace.lich_cu = copy.deepcopy(…)` + vào `ROUTE_INPUTS`; `sua_lich` chỉ ghi `trace.lich_moi`. §3 test (i)–(iv) đúng tiêu chí đóng; Q2 (g) đọc khung của cuộc sau mỗi lượt | **đóng** |
| **M-2** tiền | A quyết trần 0,20 / dừng 0,19; chỉnh ≤ 1 vòng; pilot = 2 chuỗi đầu đã thấy (không chạy lại). Bảng §7 cộng lại: 0,07 + 0,03 + 0,035 + 0,03 + 0,01 = **0,175** < 0,19 ⇒ đi hết được với 1 vòng chỉnh. C tự sửa ước Q4 (0,02 ⇒ 0,03) | **đóng** |
| m-1 | §5 "pass^2" | **đóng** |
| m-2 | D1 `da_noi` (không gồm mặc định D4b); D5 chỉ nhận trường khác giá trị lưu + dòng "Đã đổi <trường>: cũ → mới"; Q2 (c) so `da_noi` | **đóng** |
| m-3 | D6 nút "Bỏ điểm này, không thay" (code áp `bo_diem`); lượt mang `sua_chon` không đưa thẻ lần hai; danh sách nút lưu kèm khung để server kiểm `moi` | **đóng** |
| m-4 | §9 có cột hiện trạng (file + hàm) + đề xuất | **đóng** |

**Bước tiếp:** A duyệt sha `5b68f3cb666a`. Code chỉ bắt đầu khi B5 bật (User chấm Q3).
