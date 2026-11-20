# Phase 7A review notes (private)

Reviewer: `hue-rag-66`. File private, có nội dung case; không commit.

## GATE P — pilot `heritages` (2026-10-23)

Đối chiếu 20/20 case với `sources` bằng tìm text trong file nguồn: **mọi dữ
kiện trong 20 reference answer đều có trong corpus.** Hai case `out_of_scope`
(#7 Hoàng thành Thăng Long, #20 năm UNESCO của Mỹ Sơn) đã kiểm độc lập: corpus
chỉ nhắc tên, không có giá vé hay năm công nhận.

| # | Category | Kết luận | Ghi chú |
|---:|---|---|---|
| 1 | direct_fact | Sửa nhẹ | Answer thêm "dẫn từ chân núi Châu Chữ lên Cung Thiên Định": bỏ (P1) |
| 2 | comparative | Giữ | |
| 3 | direct_fact | Sửa nhẹ | Bỏ chiều cao/rộng và "bia đá lớn nhất" (P1) |
| 4 | conditional | Giữ | Vé: kiểm trùng với `travel_tickets` ở Task 3 |
| 5 | multi_source | Giữ | |
| 6 | direct_fact | Sửa nhẹ | Câu hỏi "ai": bỏ năm 1601 và đồi Hà Khê khỏi answer; bỏ keyword `1601` (P1) |
| 7 | out_of_scope | Giữ | |
| 8 | direct_fact | Sửa nhẹ | Giữ "hơn 54 m"; bỏ chi tiết 17,5 m/37 m hoặc giữ một câu ngắn; keyword `54 m` nên đặc thù hơn (P3) |
| 9 | comparative | Sửa nhẹ | Keyword `10 km`/`6 km` quá chung, dễ khớp đoạn khác: dùng chuỗi nguyên văn dài hơn hoặc thêm tên lăng (P3) |
| 10 | conditional | Giữ | heritage-guides liệt kê Thế Miếu trong khu vực bắt buộc trang phục kín đáo |
| 11 | direct_fact | Giữ | |
| 12 | multi_source | Giữ | |
| 13 | direct_fact | Sửa nhẹ | Bỏ "từ năm 1954 phối thờ Vân Hương Thánh Mẫu" (P1) |
| 14 | comparative | Giữ | Corpus có mâu thuẫn K10 (cả hai nhà hát đều được gọi là "cổ nhất"); câu hỏi theo năm xây nên không bị ảnh hưởng |
| 15 | conditional | Giữ | |
| 16 | direct_fact | Sửa nhẹ | Bỏ "sau đợt trùng tu tháng 8/2024" (P1) |
| 17 | multi_source | Sửa nhẹ | Bỏ "theo thế càn khôn hiệp đức" (P1) |
| 18 | comparative | Sửa | Đang hỏi hai dữ kiện, không phải so sánh. Viết lại thành "Đàn Nam Giao và Đàn Xã Tắc có quay về cùng một hướng không?" (P2) |
| 19 | direct_fact | Sửa nhẹ | Bỏ giá trẻ em, mức tiết kiệm và mốc tháng (P1); kiểm trùng `travel_tickets` |
| 20 | out_of_scope | Giữ | |

## Findings

- **P1 (sửa hướng dẫn viết):** reference answer thêm dữ kiện ngoài câu hỏi. Ở
  Phase 7B, Completeness chấm theo reference: câu trả lời đúng nhưng ngắn sẽ bị
  trừ điểm oan, còn Relevance thì phạt thông tin thừa. Hướng dẫn đang viết "câu
  sau thêm chi tiết đủ để kiểm chứng"; phải đổi thành **"chỉ trả lời đúng điều
  được hỏi, cộng điều kiện bắt buộc nếu có; không thêm dữ kiện phụ"**.
- **P2:** `comparative` phải thực sự so sánh (hơn/kém, trước/sau, giống/khác).
- **P3:** keyword dạng số phải đủ đặc thù (kèm đơn vị và ngữ cảnh nguyên văn,
  hoặc đi cùng tên thực thể) để không khớp nhầm đoạn khác.
- **P4:** report tracked đang nêu tên hai thực thể `out_of_scope`, gần như lộ hai
  câu hỏi: thay bằng mô tả chung.
- **K10 (corpus):** Duyệt Thị Đường ("nhà hát hoàng gia cổ nhất còn lại") và
  Minh Khiêm Đường ("nhà hát cung đình cổ nhất còn tồn tại") mâu thuẫn. Bổ sung
  vào danh sách K1–K9.

## Đánh giá văn phong (cho User)

Câu hỏi ngắn, rõ, giọng người thật, không đánh đố. Không có câu xin lời khuyên.
Pilot nghiêng về lịch sử/kiến trúc, phù hợp `heritages`; các partition du lịch
và món ăn sẽ thực dụng hơn.

## GATE R — 180 case (2026-10-23)

Đối chiếu dữ kiện: 3 sub-agent độc lập của Reviewer (read-only), bảng chi tiết ở
`/tmp/hue_review/verify_foods.md`, `verify_heritage_festival_arts.md`,
`verify_travel.md`. Reviewer tự đọc 160 case mới về văn phong, nhãn và tính
khách quan. Kết quả: 166/180 OK; 14 case cần xử lý.

| Partition | # | Xử lý | Lý do |
|---|---:|---|---|
| foods | 16 | DROP | Chi phí ăn uống/ngày: food-guides.md:95 và Chi phí du lịch Huế.md:80 ghi khác nhau |
| foods | 19 | FIX nhẹ | Câu hỏi số ít "Quán… nào" nhưng đáp án có 2 quán: "Những quán bún bò nào…" |
| heritages | 30 | FIX | Nhãn `conditional` → `direct_fact` |
| festivals | 5 | FIX | Hỏi rõ "tên Điện Huệ Nam" (Thiệu Trị đặt "Huệ Nam Tự" năm 1842; Đồng Khánh ban "Huệ Nam Điện" năm 1886) |
| festivals | 16 | FIX | Keyword "Năm 2024" quá chung: dùng chuỗi nguyên văn đặc thù hơn |
| festivals | 18 | DROP | Mâu thuẫn mới K51: Lễ hội Cầu ngư.md:10,75–76 (3 năm một lần) vs Hệ đầm phá Tam Giang – Cầu Hai.md:194 (hằng năm) |
| festivals | 20 | FIX | Bỏ câu rào đón "cần kiểm tra thông báo" |
| festivals | 22 | FIX | "Không nhất thiết" → câu hỏi và đáp án dứt khoát |
| performing_arts | 15 | FIX | Câu hỏi rối: viết gọn |
| travel_places | 3 | DROP | Câu tin tức hành chính (mức phạt), không phải câu du khách hỏi |
| travel_places | 9 | DROP | Mâu thuẫn mới K52: Đèo Hải Vân.md:12,19,74 (496 m) vs Hải Vân Quan.md:8,16 và Vé tham quan Hải Vân Quan.md:19 (khoảng 490 m) |
| travel_places | 14 | FIX | "Theo quyết định nào" quá hành chính: hỏi năm/ngày thành lập |
| travel_services | 8 | FIX | Đáp án mơ hồ: dùng khoảng cách (Thuận An ~15 km: Bãi biển Thuận An.md:9; Lăng Cô ~60 km: Vịnh Lăng Cô.md:9), thêm sources. Ghi K53: Hải Vân Quan.md:137 ghi ~70 km; kết luận không đổi |
| travel_services | 10 | FIX | Nhãn `conditional` → `direct_fact` |
| travel_services | 11 | FIX | Ghi điều kiện cụ thể (tạm ngừng khi nước sông dâng cao / cấm xuất bến do thời tiết, mùa lũ tháng 10–12: Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md:251), thêm sources |

Bổ sung K45: Hệ đầm phá Tam Giang – Cầu Hai.md:224 ghi Đầm Chuồn "thuộc Đầm Thủy Tú".

Phân bố dự kiến sau xử lý (176 case): direct ~74 / multi 29 / cond ~29 / comp 25 /
oos 18. `multi_source` = 29 được chấp nhận (trong biên; spec cấm ép đủ số).

Mẫu cho User (seed 20261023, chọn ngẫu nhiên trong các case không bị đánh dấu,
bỏ 20 case pilot): foods 1,3,12,13,14,17,18,21,25,38; heritages 24,25,27,34,35;
festivals 1,2,3,10,11,13,14,24,26,28; performing_arts 1,3,5,7,10,11,14,16;
travel_places 2,10,11,13,15,17,22,26,28,30; travel_services 1,2,3,5,6,13;
travel_tickets 4,9,10,11,12,13.
