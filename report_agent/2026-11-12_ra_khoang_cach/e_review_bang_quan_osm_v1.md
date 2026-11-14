# Review bảng quán OSM riêng cho lịch trình v1 (C) · E, 14/11/2026

Người kiểm: E (không dựng bảng). Đầu vào: `data/osm_quan_2026-11-12/bien_ban_bang_quan_v1.md`, `bang_quan_osm_v1.json` (md5 `8563a685723a`), `doc_tay_bang_v1.json` (md5 `67b08d063b3c`), `tools/dung_bang_quan_v1.py`. 0 USD, không gọi mạng. Repo public: không ghi tên quán (tên ở `data/`).

## Kết luận: `ready_for_user_confirmation` — 0 blocker · 0 major · 2 minor

## Đã kiểm
| Kiểm | Cách | Kết quả |
|---|---|---|
| Tính lại | gọi `dung()` của script, ghi ra `/tmp` (không ghi đè bảng của C), so từng dòng | **488 dòng, giống hệt bảng C**; đếm 471 tự động giữ · 110 tự động bỏ · 44 giữ lại · 27 bỏ; theo cụm khớp biên bản (bờ nam 283 · kinh thành 103 · an cựu 20 · thủy xuân 16 · kim long 4 · lăng xa 1 · đông – biển 1 · ngoài cụm 60) |
| (1) 10 dòng L1 "khớp nhầm bài kho" C giữ lại | in tên OSM cạnh tên bài kho bị coi là trùng + đường / số nhà | 10 / 10 đúng là quán khác: tên khác hẳn, hoặc trùng vài chữ nhưng khác món / khác số nhà (1 cặp cùng đường, khác số nhà, cùng món — khu này có nhiều quán cùng món, chấp nhận) |
| (2) dòng C bỏ khỏi danh sách giữ | in cả 27 dòng (20 đọc tay + 7 gộp) | 25 / 27 rõ lý do (tên món chung, nhà nghỉ / tiệc cưới / bưu điện / khu vui chơi, bản trùng ≤ 150 m của một dòng còn trong bảng); 2 dòng chưa rõ — m-1 |
| (3) gộp trùng ≤ 150 m | với mỗi dòng bỏ, tìm dòng còn lại gần nhất trong bảng | các dòng gộp đều có bản còn lại cách 3–42 m, tên cùng gốc (chi nhánh "2", cùng tên viết khác) |
| Dữ liệu cá nhân / chữ lạ | quét `ten`, `ten_hien`, `duong`, `so_nha`: chuỗi ≥ 9 chữ số, `@`, URL | 0 số điện thoại / email / URL; 1 ký tự `@` là một phần tên quán |
| Khuôn | trùng id OSM; `cum` ↔ `cach_m` ≤ 1.500 | 0 trùng; 0 dòng sai ngưỡng; tên dài nhất < 60 ký tự |
| Đếm theo cụm (A sửa report ghi kho của E) | — | cụm thủy xuân có 16 quán ⇒ hai câu "ăn gần" cụm này hỏng ở lần đếm lại 14/11 là chỗ bảng này giúp được (khi đợt 3 đưa vào chat) |

## Finding
**m-1 — 2 dòng bị bỏ khỏi danh sách giữ không thấy lý do khớp với 3 nhóm lý do trong file.** Một nhà hàng tên tiếng Anh có một từ là tên món Âu, và một nhà hàng "& Lounge". Cả hai không có bản trùng gần (bản gần nhất là quán khác, cách 3–24 m) và không có đường. Có thể C bỏ vì "không rõ" (toạ độ trùng quán khác ⇒ có thể đã đổi chủ). `doc_tay_bang_v1.json` chỉ ghi lý do theo nhóm, không theo id. Đóng khi: thêm lý do theo id cho các dòng "bo_tu_giu", hoặc C xác nhận 2 dòng này thuộc nhóm "không rõ". Không đổi kết luận (2 / 488).

**m-2 — biên bản: tổng lý do bỏ = 13 + 7 + 8 = 28, còn `bo_tu_giu` = 27.** Chênh 1 là dòng L1 bị gộp mà không nằm trong danh sách giữ lại. Biên bản đã nói ý này, nhưng phép "488 = 471 − 27 + 44" chỉ đúng khi hiểu như vậy. Đóng khi: thêm một dòng giải thích phép đếm ở bảng "Đếm".

## Chưa kiểm
Quán còn mở hay không và vị trí đúng hay không: không ai kiểm (biên bản ghi rõ; nhãn "chưa kiểm" do code gắn ở đợt 3). E không mở trang OSM từng quán.

## Kiểm lại (10:33 14/11/2026)
C sửa cả hai. m-1: 2 dòng thuộc nhóm "trùng ≤ 150 m". Bản giữ cùng tên nằm xa hơn dòng gần nhất (27 m và 129 m), E đã kiểm cả hai có trong bảng. `ly_do_bo_theo_id` ghi đủ 27 / 27 dòng (`doc_tay_bang_v1.json` md5 `44020017c833`). m-2: lý do sửa thành 13 + 7 + 7 = 27, biên bản có thêm dòng giải thích. Bảng không đổi (`8563a685723a`). **Đóng — ready, 0 finding mở.**
