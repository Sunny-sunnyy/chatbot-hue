# Review nhánh `p9-quan-bo-da-dong` `f9119d1` (C — bỏ 1 quán đã đóng khỏi bảng quán lịch) · E · 18:04 14/11/2026

Mức nhẹ, 0 USD. **Kết luận: `ready_for_user_confirmation`** — A merge được; 0 finding.

- Diff: 1 dòng comment `settings.yaml:89` (468 quán, md5). md5 file thật `e17f682903be` khớp.
- Bảng thật: 468 dòng; không còn dòng nào có tên quán đó hay link node OSM của nó.
- Lý do bỏ có nguồn: `data/quan_kho_them_2026-11-14/nguon.md:17` (B loại quán này khỏi kho vì một trang đánh giá ghi đã đóng). Bảng bỏ quán theo link OSM (`DA_DONG`, `dung_bang.py:68`), nên không bỏ nhầm quán khác cùng tên.
- m-1 của review trước đã sửa: chiều "tên OSM nằm trong tên kho" giờ đòi tên OSM có ≥ 2 từ (`dung_bang.py:65`).
- Mô phỏng và đếm: không chạy lại; số C báo ghi trong tin nhắn, file `dem_theo_cum_kho4_bo_hue_an.json`.
