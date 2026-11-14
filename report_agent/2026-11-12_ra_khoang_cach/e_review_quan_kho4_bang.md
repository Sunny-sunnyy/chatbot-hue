# Review nhánh `p9-quan-kho4-bang` `26505d6` (C — bảng quán lịch sau ghi kho 4) · E · 17:55 14/11/2026

Mức nhẹ, 0 USD.

## Kết luận: `ready_for_user_confirmation` — A merge được; 1 minor

## Đã kiểm
- **Diff:** 1 dòng comment ở `settings.yaml:89` (469 quán: kho 42, dữ liệu mở 4, OSM 423; md5). md5 file thật `580881638793` khớp comment.
- **Khử trùng, kiểm độc lập** (script riêng `/tmp/e_rv_trung.py`, chạy trên bảng đã dựng + bảng OSM gốc):
  - 5 / 5 dòng OSM bị bỏ đúng là cùng quán với dòng kho, khoảng cách 0–85 m. 3 dòng là quán mới; 2 dòng là trùng có từ trước. Có 1 dòng OSM ghi sai dấu, vẫn khớp đúng nhờ bỏ dấu.
  - Quét ngược: các dòng OSM cách quán kho ≤ 200 m, có chung từ có nghĩa mà KHÔNG bị bỏ ⇒ 11 cặp. Cả 11 cặp E đọc ra là quán khác nhau (tên khác hẳn, hoặc cùng đường nhưng khác số nhà) ⇒ không sót trùng.
- **Đếm và mô phỏng:** E không chạy lại. Đây là số C chạy, ghi trong biên bản (`data/quan_lich_2026-11-14/bien_ban_quan_kho_them.md`, mục "Ghi kho 4"). Nhánh chỉ đổi comment, còn bảng là file private đã dựng ⇒ chạy lại không thêm thông tin.

## Finding
- **m-1 (không chặn):** luật "tên bỏ dấu chứa nhau" xét cả chiều *tên OSM nằm trong tên kho*.
  - Bảng OSM có 42 dòng trong cụm mà tên chỉ 1 từ (vd một chữ chung như "cafe"). Một dòng như vậy cách quán kho ≤ 200 m mà tên kho có chứa từ đó thì sẽ bị bỏ nhầm.
  - Hôm nay chưa xảy ra: 0 dòng bị bỏ nhầm.
  - Đóng khi (nếu thêm quán kho lần sau): chỉ nhận chiều *OSM ⊂ kho* khi tên OSM có ≥ 2 từ; hoặc in danh sách bỏ để người xem như lần này.
