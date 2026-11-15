# Review nhánh `p9-web-noi-tiep` (B) — E · 16:15 15/11/2026 (`date`) · 0 USD

Bản review: origin `2b0be16` (code `16a6715`). Căn cứ: diff `origin/main...origin/p9-web-noi-tiep` (4 file: `assistant.py` +22 / −8, `settings.yaml` +1, `test_b6_tra_web.py` +53, report), report của B, dữ liệu đo private `data/cau_noi_tiep_2026-11-15/quyet_r1.jsonl`. E không chạy lại lượt có phí.

**Kết luận: `changes_requested` (nhẹ)** — 0 blocker · 1 major (chỉ chặn việc BẬT cờ, không chặn merge cờ tắt) · 2 minor. M-1 + m-1 đóng bằng vài dòng + 2 ca test ⇒ A đọc diff rồi merge, không cần vòng 2.

## Cổng tối thiểu
- Phạm vi đúng 3 file code / test + report; `git diff --check` sạch; cờ `web_cau_noi_tiep` mặc định tắt ở cả dataclass lẫn `settings.yaml`.
- Tiêu chí so hai bên: mốc "0 / 10" của Quyết 1 là số tất định tính bằng code (cùng 10 cặp); Quyết 2 mốc 2 / 2 là ca của User, bên cờ bật n = 8 — **khác mẫu số**, B có ghi rõ; chấp nhận vì chỉ số quyết là "0 mục lạc đề" tuyệt đối, không phải hiệu hai bên.
- Số của report đối chiếu với `quyet_r1.jsonl` (E đọc 17 lượt thứ hai): 8 lượt cổng web mở ở nhóm hỏi tiếp, cả 8 câu tra web có tên chủ thể của lượt 1 — khớp "8 / 8". Mục web lạc đề 0 / 8 là B đọc tay; E không đọc lại từng mục.

## Bốn chỗ B nhờ soi
1. **Luật chặn có lỏng hơn không — KHÔNG.** Thiên tai / lưu trú / thời gian thực xét chuỗi ghép cả hai câu ⇒ chỉ thêm ca bị chặn. Luật "số người dùng tự gõ được phép" vẫn nhận đúng câu gõ. Hệ quả ngược (đã có trong report): model thêm ngày / số vào câu tìm ⇒ mục web dễ bị thay câu cố định hơn — an toàn, không phải lỏng.
2. **Đường song song — CÓ sang trace chính.** `_merge_spec` chép mọi trường trừ nhóm giữ riêng; `model_queries` không thuộc nhóm đó, `history` thuộc nhóm đầu vào định tuyến nên trace chính vốn đã có. Ca dò của E gọi thẳng `_merge_spec`: trace chính nhận đủ 2 câu tìm và còn lịch sử.
3. **Tên người dùng (S1) — không có rào, chỉ có số đo 0 / 4.** Ca dò: câu tìm của model có tên riêng ⇒ ra nguyên câu tra web (bộ lọc chỉ bỏ email / số điện thoại). Trước bản sửa, tên chỉ ra web khi người dùng gõ nó ở chính lượt đó; nay có thêm đường "tên ở lượt trước". Xem m-2.
4. **Mục "Điều người quyết cần biết" — đủ và thẳng** (ca gốc của User hết lạc đề nhưng 2 / 2 vẫn là câu cố định; 5 / 13 mục bị bộ kiểm số thay). Thiếu một điều: M-1 dưới đây.

## Finding
**M-1 (major cho việc bật cờ) — câu hỏi tiếp NHIỀU Ý: câu tìm cuối của model có thể là của ý kho ĐÃ CÓ.**
- Vị trí: `cau_cho_web` lấy `model_queries[-1]`; `cong_web` vẫn ghép "(chỉ viết cho phần: <vế thiếu>)" từ câu GÕ.
- Bằng chứng: (a) ca dò 0 USD — lượt có lịch sử, model tìm hai lần theo thứ tự "ý thiếu" rồi "ý có" ⇒ câu tra web là câu của ý kho đã trả lời, còn lời dặn viết mục web lại đòi vế thiếu ⇒ kết quả web không liên quan vế cần viết; (b) trong 17 lượt thứ hai của bộ đo **không có lượt nào là câu nhiều ý** (0 dòng "tư liệu chưa có thông tin về" ở lượt 2) ⇒ đường này chưa được đo lần nào; (c) lượt 1 của chính bộ đo cho thấy câu nhiều ý + cổng web là ca thật.
- Tác động: với câu hỏi tiếp nhiều ý, cờ bật có thể làm mục web kém hơn cờ tắt (cờ tắt gửi cả câu gõ, có đủ các vế).
- Tiêu chí đóng (chọn một): (i) lượt `trace.nhieu_y` ⇒ `cau_cho_web` trả câu gõ như cũ (1 dòng + 1 ca test) — E khuyến nghị, đúng tinh thần "chỉ đổi ca đã đo"; hoặc (ii) đo ≥ 4 cặp hỏi tiếp nhiều ý trước khi bật và ghi kết quả.

**m-1 — câu tìm rỗng / toàn khoảng trắng của model ⇒ tra web chỉ còn chữ tên thành phố.** Ca dò: `model_queries = [""]` hoặc `["   "]` ⇒ câu gửi tra web là mỗi chữ thêm tự động. Hiếm (tham số công cụ là chuỗi bắt buộc) nhưng rẻ: chỉ dùng câu model khi `.strip()` khác rỗng, không thì câu gõ (+ 1 ca test).

**m-2 (theo dõi, không sửa code) — S1 dựa vào n = 4.** Ghi vào checklist lúc bật: đếm trong log lượt có `cau_tu_model` (đã có cờ, không chữ) và đọc tay câu tra web ở lượt đo kế có người dùng nêu tên. Không thêm bộ lọc tên bằng code (không có danh sách tên ⇒ sẽ là rào đoán).

## Bất biến E đã kiểm (ca dò riêng, gọi thẳng hàm trên code nhánh, 0 USD)
Cờ tắt / không truyền cờ / lượt không lịch sử ⇒ `cau_cho_web` trả đúng câu gõ (3 / 3) — hành vi đang chạy không đổi khi merge cờ tắt.

## Ngoài phạm vi (ghi ngắn)
- Câu model viết bị cắt ở giới hạn độ dài có thể đứt giữa từ (B đã ghi).
- Ca gốc của User muốn ra giờ thật cần việc riêng về bộ kiểm số (B đã ghi) — E đồng ý không gộp vào nhánh này.
