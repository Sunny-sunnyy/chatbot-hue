# Dữ liệu + ảnh khách sạn, sửa cách chọn ≤ 5 cơ sở · B · 18:35 14/11/2026

A giao theo ưu tiên mới của User (17:50 14/11/2026: dữ liệu, ảnh khách sạn phải đầy đủ; vẫn không nói giá phòng). Plan `docs/superpowers/plans/2026-11-14-khach-san-du-lieu-anh-plan.md` — A duyệt bản sha `067fc664c753` (mức nhẹ, không review plan). Nhánh `p9-khach-san`. Dữ liệu, script, ảnh ứng viên: `data/khach_san_2026-11-14/` (private).

## Đếm trước khi xây (0 USD)
- Bảng 140 cơ sở của E: mô tả / ảnh / link riêng 0 / 140; toạ độ ước (~1 km) 117, không có 23.
- Cách chọn cũ, mô phỏng 3.840 khung: **lỗi thật** — trong một mức hạng xếp theo tên abc ⇒ **5 sao 0 / 6.108 lượt** ở mức cao cấp (luôn hai khách sạn 4 sao đầu bảng chữ cái), **3 sao 0 lần**; 16 / 140 cơ sở từng hiện; 72 % lịch cùng một bộ 5.

## Đổi gì
| File | Đổi |
|---|---|
| `backend/llm/luu_tru_lich.py` | `chon_co_so`: trong mỗi mức lấy lần lượt từng hạng, hạng cao trước (1 × 5 sao + 1 × 4 sao; 1 × 3 sao + 1 × 2 sao; 1 sao trước đạt chuẩn); cùng hạng: cùng cụm ⇒ có ảnh ⇒ tên. Mỗi cơ sở thêm `map_url` (tìm theo tên + địa chỉ, cùng gốc link bản đồ của lịch) và `anh` (chỉ ảnh chắc). Nạp bảng: ảnh phải dưới `/anh/khach_san/…jpg`, không thì server không khởi động. |
| `backend/config/settings.yaml` | `lich_trinh_bang_luu_tru` ⇒ `data/khach_san_2026-11-14/bang_luu_tru_lich_v2.json` (md5 `a47c9a751a3e`) = bảng E + toạ độ Places + ảnh đã duyệt. |
| `frontend/src/LichV2.jsx`, `lkh.css` | Thẻ "Nơi ở gợi ý": ảnh nhỏ bên trái (chỉ nhận đường `/anh/khach_san/`), link "Bản đồ" + "Tìm phòng" (kiểm gốc cả phía trình duyệt); 0 chữ ghi công. |
| `frontend/public/anh/khach_san/` | 66 ảnh (480 px, 2,6 MB). |
| `backend/tests/test_luu_tru_lich.py` | Test thứ tự hạng đổi theo luật mới + ca lỗi 14/11 (hai 4 sao tên "A…" không được đẩy 5 sao ra) + có ảnh trước. |

**Không làm so với plan (B tự quyết, lý do):** "mô tả ngắn do code viết" — chỉ lặp lại hạng + địa chỉ + khu mà thẻ đã hiện ⇒ bỏ. Website riêng, đánh giá Google, giá: không làm (như plan).

## Dữ liệu
- **Toạ độ Serper Places:** nhận **82 / 140** (sàn ghi trước ≥ 100 — **TRƯỢT**, A nhận). Luật nhận siết sau khi soát tay các ca tên không trùng hẳn bắt nhận nhầm (một nhà hàng cùng tên; chi nhánh "2" ↔ bản gốc): tên khớp (bỏ dấu, bỏ dấu cách) + loại hình lưu trú + đúng số chi nhánh + đúng tên đường trong địa chỉ + ≤ 3 km toạ độ ước. 81 vào bảng; 1 bị giữ toạ độ cũ vì cụm gần mới thuộc khu khác khu đã duyệt (0 cơ sở đổi khu). 58 còn lại giữ toạ độ ước. Toạ độ chỉ dùng để chọn cụm gần; link Bản đồ tìm theo tên + địa chỉ nên có cho cả 140.
- **Ảnh (cách v3, A chốt vòng tự soi: 1 agent con chọn + B nhìn lại mọi ảnh nhận):** Serper Images 140 lượt; 131 cơ sở có ứng viên. 4 agent con (13 cơ sở từng hiện trước, rồi 3 nhóm ~40). Lượt chọn: 106 có ảnh (68 "cao", 38 "vừa"). B nhìn lại 68 ảnh "cao": 66 nhận, 2 hạ `kc` (một ảnh vẽ phối cảnh, một biển có số điện thoại). "Vừa" ⇒ `kc`, không vào bảng (ảnh không chắc cạnh tên khách sạn dễ khiến khách tưởng đúng nơi).
  - **Kết quả: 66 / 140 cơ sở có ảnh hiện được** (5 sao 8 / 10 · 4 sao 12 / 14 · 3 sao 5 / 7 · 2 sao 14 / 30 · 1 sao 11 / 49 · đạt chuẩn 16 / 30); 40 `kc`; 34 không ảnh đáng tin (9 không ứng viên).
  - Trên 3.840 khung: **14.924 / 15.288 ô cơ sở hiện ra có ảnh (97,6 %)**; ô thiếu ảnh chủ yếu là một cơ sở 1 sao hay hiện.
- Bảng có dòng trùng (cùng tên + địa chỉ, hai dòng — vd La Perle, Như Phú; Villa Louise hai địa chỉ thôn / xã): giữ như bảng E, ghi để lần sau gộp.

## Đo — ĐẠT (trừ sàn Places)
| Bộ | Kết quả |
|---|---|
| Luôn (3.840 khung, 0 USD) | test lưu trú 8 / 8 đạt (gồm mọi luật "Luôn": đúng khu, ≤ 5, nhãn, 0 link ngoài mẫu). **5 sao: 3.036 / 3.036 lịch khu trung tâm** (mẫu số = mọi lịch khu trung tâm; khu này luôn có mức cao cấp trong ≤ 5); **3 sao: 3.036 / 3.036** (trước: 0 / 0). Cơ sở khác nhau từng hiện: 12 (chỉ báo, không sàn) |
| Q1 | khối nơi ở không vào tin nhắn gửi model — test sẵn có đạt; không đổi chuỗi gửi model |
| UI (Playwright 1440 + 390, server nhánh, xếp lịch thật) | **ĐẠT**: thẻ 5 cơ sở, 4 ảnh tải được (480 px), 10 / 10 link đúng gốc + `_blank` + `noopener`, 0 chữ ghi công, 0 lỗi console, 0 yêu cầu ra ngoài lúc tải. Ảnh `data/khach_san_2026-11-14/anh_pw/`, script `tools/pw_khach_san.py` |
| Test rộng `backend/tests` (3 phút 48) | 1.039 đạt; 5 hỏng / lỗi chỉ vì chạy không `--env-file` (cần khoá OpenAI) ⇒ chạy lại 5 test đó có `--env-file`: 5 / 5 đạt |

## Tiền (từ log)
≈ **0,283 USD**: Places 140 lượt 0,140 · Images 140 lượt 0,140 · Playwright 4 lần xếp lịch 0,0025. Agent con: quota Claude. Trần đợt 0,40.

## Giới hạn / việc sau
- Deploy: allow-list ảnh docker phải thêm `data/khach_san_2026-11-14/bang_luu_tru_lich_v2.json` (thay bảng E) — A thêm vào checklist trước deploy.
- 74 / 140 cơ sở chưa có ảnh chắc; phần lớn 1–2 sao ít khi hiện. Thêm ảnh: chỉ khi luật chọn đổi làm chúng hiện (đếm lại lúc đó).
- Toạ độ ước còn 58 cơ sở; trong khu trung tâm không dùng khoảng cách để xếp (sai số ~1 km).
