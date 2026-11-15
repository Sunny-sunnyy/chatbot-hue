# Trang "Chỗ ở" theo khu + bảng lưu trú v3 — implementation (C, 10:43 15/11/2026)

Plan: `docs/superpowers/plans/2026-11-15-khach-san-trang-va-ngan-sach.md` §1 (sha `b5d8bc184090`, User duyệt 10:28 15/11). Nhánh `p9-cho-o` @ `86acfb1` (worktree `/tmp/c_co`). Chờ E review.

## Bảng v3 (`data/khach_san_2026-11-15/bang_luu_tru_lich_v3.json`, md5 `97eedb0cc2ab`; script `tools/dung_bang_v3.py`; 0 USD)
- Gộp "La Perle Huế" vào "La Perle": cùng số nhà viết khác, cùng 2 sao, cùng địa điểm Places.
- Bỏ Đô Thành (A Lưới) và Alba Thanh Tân (Phong Điền).
- La Vela: toạ độ Places nằm cách cụm An Cựu 2,5 km ⇒ code tính ra khu trung tâm.
- SBH Gloria: toạ độ Places, giữ khu ven biển, `phia_bien` "bac" ("Phú Vinh" = vùng Phú Vang cũ). Đây là suy luận theo địa giới.
- Mọi cơ sở ven biển có `phia_bien`. Loader kiểm: chỉ `bac` / `nam`, và chỉ cơ sở ven biển mới có.
- Places của 2 cơ sở lấy từ cache của B (`data/khach_san_2026-11-14/places/`), không gọi lại.
- 140 ⇒ **137** cơ sở: trung tâm 122 (18 · 34 · 70) · tây 5 · ven biển bắc 5 · nam 5. Có ảnh 69.
- **Lịch đổi [đã chạy]** (`tools/so_v2_v3.py` ⇒ `so_v2_v3.json`): **364 / 3.840** khung có ô Nơi ở khác.
  - Tất cả cùng một kiểu: La Vela (5 sao) vào thay Indochine Palace khi cụm chính trong khu là An Cựu (luật "gần cụm trước" có sẵn).
  - Khác: 0.

## Code
- `luu_tru_lich.trang_cho_o(bang)` (cuối file):
  - 4 nhóm khu (ven biển tách bắc / nam) ⇒ 3 mức theo hạng.
  - Trong mỗi mức: có ảnh trước ⇒ hạng cao ⇒ tên.
  - Mỗi cơ sở chỉ có `ten, xep_hang, dia_chi, anh, map_url, link` (link dựng như `chon_co_so`).
- `GET /api/cho_o` (`api/routes/cong.py`): cờ `luu_tru_lich` tắt ⇒ 404; dựng một lần mỗi bộ cờ.
- Giao diện:
  - `ChoO.jsx` + `co.css`: lọc khu / hạng; ảnh chỉ `/anh/khach_san/…jpg`; link chỉ 2 gốc + `_blank noopener`.
  - Route `#/cho-o[/<khu>]`.
  - Ô "Nơi ở" của lịch có link "Xem thêm chỗ ở khu này" ⇒ trang đã lọc sẵn khu. Không thêm mục trên thanh trên cùng.
- `settings.yaml`: `lich_trinh_bang_luu_tru` ⇒ v3.

## Kiểm [đã chạy]
- `tests/test_luu_tru_lich.py`: 11 passed. Có 2 test mới:
  - trang: mọi cơ sở đúng 1 lần, đúng khu / mức, đúng tập trường, 0 trùng tên + địa chỉ, ảnh / link đúng gốc, có ảnh trước;
  - loader `phia_bien`: 3 ca hỏng.
- Cả `backend/tests` (`--env-file`): **1050 passed, 291 s**.
- Playwright (`tools/pw_cho_o.py`, ảnh `data/khach_san_2026-11-15/anh/`): **DAT**.
  - Khổ 1440 + 390: 137 cơ sở; lọc phía nam ⇒ 5, thêm 4–5 sao ⇒ 3; 0 lỗi console; 0 yêu cầu ra ngoài; 0 link / ảnh sai gốc; 390 không cuộn ngang.
  - Lịch thật 3 ngày ⇒ bấm "Xem thêm chỗ ở khu này" ⇒ `#/cho-o/loi_do_thi_hai_bo_song_huong`, chỉ hiện nhóm trung tâm.
  - Lượt đầu báo KHONG_DAT vì lỗi trong chính script kiểm (ảnh phục vụ dưới `/static/`), không phải lỗi trang; sửa script, chạy lại.
- Server tạm cổng 8038, cwd `/tmp/c_co/backend`, đã tắt.

## Tiền
2 lượt xếp lịch thật trong Playwright ≈ 0,0014 USD. Bộ test đầy đủ có vài lượt gọi thật, chưa tách số. Places 0 (dùng cache).

## Giới hạn
- 68 / 137 cơ sở không ảnh (ô màu).
- Danh mục lấy 12/11/2026.
- Trong lịch, Gloria vẫn không hiện ở khung Thuận An, vì lịch lọc phía theo địa chỉ ("Phú Vinh" không khớp). Trang thì dùng `phia_bien`. Muốn lịch cũng dùng `phia_bien` là việc riêng: chạm `chon_co_so`, nơi B đang sửa cho ngân sách.
