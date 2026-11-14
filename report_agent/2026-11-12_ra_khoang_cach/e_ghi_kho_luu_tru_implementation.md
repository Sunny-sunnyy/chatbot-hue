# Ghi kho lần 2 — bài lưu trú · E, 12:58 14/11/2026

A giao (14/11). Repo public ⇒ report tả ở mức loại, không tên cơ sở, không chữ câu Golden. Tệp làm việc (private): `data/sua_kho_2026-11-14_ghi_kho_2/`.

## Kết luận: đạt mọi tiêu chí ghi trước, trừ một phần nhỏ ở câu homestay (minor). Tiền 0,225 USD.

## Đã ghi
- **5 bài mới ở `travel/services/`:** "Lưu trú ở Huế — …"; một bài tổng hợp khách sạn 3–5 sao và 4 bài theo khu (trung tâm hai bờ sông Hương · phía tây · ven biển – đầm phá – Lăng Cô · ngoài ba khu).
  - Bài sinh bằng script `data/sua_kho_2026-11-13_luu_tru/tools/dung_bai_luu_tru.py`, không gõ tay.
  - Gồm 139 cơ sở có hạng / đạt chuẩn từ danh mục Cục Du lịch Quốc gia (lấy 12/11), sau khi gộp 2 cặp trùng.
  - Cộng 1 khách sạn 4 sao công nhận 23/01/2026, nguồn ghi riêng là tin chính thức của ngành du lịch thành phố (A chốt (b)).
  - C review: ready.
- **Bài Bảo tàng Cổ vật:** dòng giờ mở cửa thêm một câu nhắc rằng giờ có thể đổi (theo mùa, khi có sự kiện), giống 11 bài khác dùng chung khung giờ.
- **Code:** `NOTICE_SOURCE_PREFIXES` thêm `travel/services/Lưu trú ở Huế` ⇒ câu trả lời trích bài lưu trú có dòng "thông tin có thể đã thay đổi". Bài "Đi lại ở Huế" cùng thư mục thì không. Có thêm 1 test, `test_assistant.py` 9/9 đạt.
- **Giữ lại, chưa ghi — giờ Đại Nội theo mùa:**
  - Không tìm được trang chính thức nào ghi khung theo mùa (Codex tra 2 lượt).
  - Theo trích của Codex, trang hướng dẫn tham quan mà User dùng ghi số User chép là **giờ bán vé**; giờ mở cửa là 06h30–18h00 (hè) và 07h00–17h30 (đông).
  - E không mở được trang đó: Cloudflare trả 403.
  - A ghi câu hỏi để User xác nhận.

## Dựng lại
- Chạy `tools/chay.sh`: kiểm khoá ⇒ sao lưu ⇒ ghi ⇒ chia đoạn thử ⇒ dựng lại tại chỗ ⇒ T1. Từ 12:45:57 đến 12:50:17, 0 lỗi.
- Kho: 207 ⇒ 212 file, 8.474 ⇒ **8.522 đoạn**. Thêm đúng 48 đoạn mới (9 · 24 · 5 · 5 · 5), khớp số chia thử.
- Build record `38b3ca3eb323`, sparse `47f4b88b1309`.

## Đo (tiêu chí ghi trước: `data/…/ghi_kho_2/TIEU_CHI.md`, 12:52, trước khi xem kết quả "sau")
Hai bên chạy trên cùng code backend: "trước" ở `55f48fe`, "sau" ở `42c0e04`; commit này chỉ sửa 1 test cờ. Chấm theo mức thay đổi: câu nào ngữ cảnh không có đoạn mới thì khác biệt chỉ là nhiễu sinh câu.

| Đo | Tiêu chí | Kết quả | Đạt |
|---|---|---|---|
| T1 (158 câu, 0 USD) | theo dõi | MRR 0,7203 ⇒ 0,7188 · nDCG 0,7545 ⇒ 0,7534 · độ phủ từ khoá 92,04 không đổi. 13 câu đổi top 10. 2 câu có đoạn lưu trú, cả hai thuộc loại hỏi chi phí lưu trú. Một câu, bài chi phí tụt từ hạng 2 xuống hạng 4, vẫn trong top 10 | — |
| K1 Golden 176, máy đếm | 0 lỗi kỹ thuật · từ chối ≤ trước + 1 · 0 lỗi trích dẫn mới | lỗi 0 · từ chối **23 ⇒ 23**: 4 câu mới từ chối, 4 câu hết từ chối; cả 8 câu có ngữ cảnh lần tìm đầu giống hệt, các lần tìm thêm không có đoạn lưu trú ⇒ nhiễu · lỗi trích dẫn 0 | đạt |
| K1, câu có đoạn lưu trú (2) | 1 agent con chấm mù cặp; không câu nào tụt | cả 2 câu: Đủ 5 / Đúng 5 ở cả hai bên. Một câu hoà; một câu người chấm thích cách nói của bản "trước" hơn, điểm vẫn bằng nhau | đạt |
| K2 an toàn 32 | 0 câu có đoạn lưu trú trong ngữ cảnh · lớp không đổi | 0 câu chạm đoạn mới · 0 câu đổi lớp (trả lời / từ chối / ngoài phạm vi) | đạt |
| K4 lưu trú 12 (câu E viết, không Golden) | được trả lời 4/12 ⇒ ≥ 9/12 · 0 câu nêu giá · câu homestay nói rõ không gồm homestay · 0 tên / hạng bịa | được trả lời **4 ⇒ 11 / 12** (câu hỏi giá phòng vẫn từ chối, đúng). 0 câu nêu giá. Chấm mù so với ngữ cảnh: **0 điều không có trong ngữ cảnh**; đúng câu hỏi 9 · một phần 2 · không 1 | đạt, trừ câu homestay |

**Những điểm chưa tốt (minor, theo dõi, chưa sửa):**
- *Câu homestay:* trợ lý nói đúng điều bài cũ ghi (khu phố Tây có homestay), nhưng không nói danh sách lưu trú của kho chưa gồm homestay, dù ý đó có trong ngữ cảnh.
- *Câu khách sạn rẻ ở một khu:* nêu đúng 3 cơ sở, bỏ sót 2 cơ sở cùng loại có trong ngữ cảnh.
- *Câu hỏi giá phòng:* từ chối là trung thực. Tốt hơn thì nói "danh sách không gồm giá" và gợi ý các khách sạn cùng hạng.
- *Câu ven biển:* nêu 2 resort từ một bài điểm đến cũ (không có hạng), bỏ sót 1 khách sạn 5 sao cùng vùng.
- Cả bốn điểm này là cách model chọn ý từ ngữ cảnh, không phải dữ liệu sai. Sửa thì thuộc lời dặn hoặc bậc thử riêng, theo luật "đổi một thứ".

## Tiền
- "Trước": Golden 0,0749 + an toàn 0,0215 + K4 0,0208 = 0,1172 USD.
- "Sau": 0,0774 + 0,0212 + 0,0091 = 0,1077 USD.
- Hai lượt tra Codex: gói ChatGPT, không tính API.
- Người chấm là agent con, dùng quota Claude.
- **Tổng 0,2249 USD.**

## Tệp
- `data/sua_kho_2026-11-14_ghi_kho_2/`:
  - `tools/`: `ghi_kho.py`, `chay.sh`, `do_ben.sh`.
  - `kho.diff`, `TIEU_CHI.md`, `k4_luu_tru.jsonl`.
  - `truoc/`, `sau/`.
  - `cham/`: lô, khoá, kết quả.
  - `chay.log`, `chia_thu.log`, `build_moi.log`, `t1_sau.jsonl`.
- Bản sao trước khi ghi: `knowledge-base-hue/meta/backup_ghi_kho_2026-11-14_lan_2/`.
- Lùi: `python3 -I tools/ghi_kho.py lui`, rồi dựng lại.
