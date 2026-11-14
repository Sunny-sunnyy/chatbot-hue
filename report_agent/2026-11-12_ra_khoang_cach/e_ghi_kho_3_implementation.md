# Ghi kho lần 3 14/11 — 4 bài nơi chưa có bài + giờ Đại Nội theo mùa · E · 16:15 14/11/2026

A giao (User duyệt khi vắng). Tiêu chí ghi trước: `data/sua_kho_2026-11-14_ghi_kho_3/TIEU_CHI.md`. Review bài + diff: C (`c_review_kho_3.md`, private; 1 major + 3 minor đã sửa, A chỉnh câu giờ đêm). Dữ liệu, script, log: `data/sua_kho_2026-11-14_ghi_kho_3/`, `data/bai_kho_moi_2026-11-14/`.

## Vì sao 4 bài này (đếm trước khi xây, 0,0065 USD)
- Danh sách 50 địa danh khách hay hỏi ⇒ 26 chưa có bài riêng; nhiều nơi là một phần bài lớn (vd các công trình trong Kinh thành) nên không cần bài riêng.
- Hỏi thử 6 câu trên chỉ mục cũ: 2 câu bị từ chối (cầu, nhà ga), 3 câu chỉ được 1–2 câu mỏng, 1 câu trả lời được ⇒ chọn 4 bài: cầu Trường Tiền, Ga Huế, chùa Từ Hiếu, nhà vườn An Hiên.

## Đổi gì
- 4 bài mới (2 agent con tra công khai bằng Codex + tự mở trang đối chiếu; mỗi ý có nguồn + ngày; chỗ nguồn mâu thuẫn viết "nguồn ghi A hoặc B" / khoảng):
  `travel/places/Cầu Trường Tiền.md` (25 đoạn), `travel/places/Ga Huế.md` (15), `heritages/heritage/Chùa Từ Hiếu.md` (19), `travel/places/Nhà vườn An Hiên.md` (22).
- Bài Đại Nội: dòng giờ mở cửa ⇒ theo mùa (hè 06h30 – 18h00, đông 07h00 – 17h30, giờ ngừng bán vé; tham quan đêm theo chương trình) + dòng nguồn. 11 bài lăng / điện ghi "khung chung 07h00 – 17h30" GIỮ — nguồn chỉ nói Đại Nội (A đồng ý).
- Chỉ mục: 212 ⇒ 216 file, 8.522 ⇒ **8.603 đoạn**; record `82abd97169cd`, sparse `3404406926f2`, T1 `652da5944fe7`. Sao lưu: `knowledge-base-hue/meta/backup_ghi_kho_2026-11-14_lan_3/`. Dựng 16:05 – 16:10, cả nhóm dừng việc trong lúc dựng.

## Đo (theo luật đo câu chạm) — ĐẠT
| Bộ | Kết quả |
|---|---|
| T1 (0 USD) | 9 / 158 câu đổi top 10; 2 câu có đoạn bài mới / bài Đại Nội ⇒ "câu chạm" |
| Golden: 2 câu chạm + 18 câu ngoài kho ×1 | 0 lỗi kỹ thuật, 0 lỗi trích dẫn; **ngoài kho bị trả lời 0 / 18**; từ chối không đổi (20 / 20 cùng lớp với mốc lần 2). 2 câu chạm: câu trả lời cùng ý, chỉ đổi cách viết (E đọc tay cả hai cặp — không cần người chấm mù) |
| An toàn 32 ×1 | 0 đổi lớp, 0 câu ngoài kho mới bị trả lời, 0 lỗi; 0 câu có đoạn bài mới trong ngữ cảnh; 1 câu có dòng giờ Đại Nội mới, lớp không đổi ⇒ 4 số S-AT không cần chấm lại |
| 7 câu hỏi thử (E viết, không phải Golden) | cầu Trường Tiền, Ga Huế: hết từ chối, trích bài mới, nói đúng khoảng năm / "nguồn không thống nhất"; chùa Từ Hiếu: đủ ý (hiếu thảo, thái giám, Thích Nhất Hạnh, kiến trúc); nhà vườn An Hiên: trả lời "có mở cửa" từ bài mới; Đại Nội: trả lời theo mùa; 0 số trái với bài |

Ghi nhận ngoài lề: A thấy "[11]" trong câu trả lời /api/chat — không phải lỗi: số gốc của sổ nguồn (tìm thêm ⇒ sổ > 10), nguồn 11 có trong `sources`; giao diện đánh lại số khi hiện.

## Tiền
≈ 0,030 USD (đếm trước 0,0065 · Golden 20 câu 0,0065 · an toàn 0,0205 · 7 câu thử 0,0028 · kiểm "[11]" ≈ 0,0005). Codex: gói ChatGPT; agent con: quota Claude.

## Còn lại
- Ảnh cho 4 bài: C đang tìm (bảng ảnh Khám phá).
- Sổ ghi việc `bao_cao_he_thong/` + `bai_hoc/`: theo A giao.
