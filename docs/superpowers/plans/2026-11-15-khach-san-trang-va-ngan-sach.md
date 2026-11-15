# Plan — trang khách sạn theo khu + hỏi ngân sách ở (bản 2, C, 10:22 15/11/2026; bản 1 10:17 — sửa theo phản biện B + E)

Việc A giao 15/11 (User chọn). Mức nhẹ: ≤ 0,2 USD, không đổi kiến trúc ⇒ plan 1 trang, A duyệt, code, đo 1 lượt, review cả nhánh. **CHƯA code.**
Số đếm 0 USD [đã chạy]: `data/khach_san_2026-11-15/tools/dem.py` ⇒ `dem.json` (3.840 khung như các lần đếm lịch) + đếm bảng `bang_luu_tru_lich_v2.json` (md5 `039c3adebb9b`).

## 0. Đếm trước khi xây

| Đo gì | Số | Ý nghĩa |
|---|---|---|
| Lịch có ô "Nơi ở" | 3.072 / 3.840 khung | lịch 1 ngày không có đêm ⇒ không có ô |
| Khu được chọn | trung tâm 3.036 (98,8 %) · ven biển 36 · phía tây 0 | gần như mọi lịch ở trung tâm |
| Cơ sở từng hiện trong lịch | **12 / 140** | 3 khách sạn hiện ở **mọi** lịch trung tâm (3.036 / 3.036) |
| Bảng theo khu (cao 4–5 sao · vừa 2–3 sao · bình dân 1 sao / đạt chuẩn) | trung tâm 122 (17 · 35 · 70) · tây 5 (1 · 1 · 3) · biển Thuận An 4 (1 · 1 · 2) · biển Lăng Cô 5 (3 · 0 · 2) · biển không rõ phía 1 · ngoài 3 khu 3 (A Lưới, Phong Điền…) | trung tâm đủ mọi mức; ngoài trung tâm mỏng |
| Có ảnh | 71 / 140 (trung tâm: cao 15 / 17 · vừa 18 / 35 · bình dân 26 / 70) | ½ cơ sở không ảnh |
| Toạ độ | Places 81 · ước mức con đường 117 (~1 km) · địa chỉ 140 / 140 | link Bản đồ dựng từ tên + địa chỉ ⇒ 140 / 140 có link |
| Đủ ảnh + toạ độ Places + địa chỉ | 48 / 140 | |
| Nếu lọc theo một mức (5 cơ sở / mức) | trung tâm: cả 3 mức đủ 5 ở 3.036 / 3.036 khung · ven biển (36 khung): cao 1 · vừa 1 · bình dân 2 · **0 khung mức trống** | ngân sách làm được ngay với bảng hiện có |
| Cơ sở có thể hiện nếu có ngân sách | 12 ⇒ **36** | vẫn tất định: mỗi mức trung tâm luôn ra cùng 5 cơ sở |

Kết luận đếm: (2) ngân sách tăng lựa chọn nhưng chỉ ×3. Muốn khách thấy hết 140 cơ sở thì cần (1) trang riêng. **Thứ tự (B, C, E đồng ý): ngân sách trước; trang làm bản tối thiểu** — lợi của trang chưa đếm được (chưa ai mở).

## 1. Trang "Chỗ ở" theo khu

- **Đổi gì:**
  - Server: `GET /api/cho_o` (`backend/api/routes/cong.py`, như `/api/lich_mau`). Đọc bảng đã nạp lúc khởi động (cờ `luu_tru_lich`), trả cơ sở của 3 khu (≈ 137, xem "Dữ liệu" dưới), mỗi cơ sở các trường `ten, xep_hang, muc, dia_chi, khu, anh, map_url, link`. Không trả `nguon_url`, `ma_nguon`, toạ độ; không giá, không điện thoại.
  - Giao diện: trang `#/cho-o` (`frontend/src/ChoO.jsx`), có link từ ô "Nơi ở" của lịch ("Xem thêm chỗ ở khu này"). Không thêm mục trên thanh trên cùng (đề xuất; A / User quyết).
- **Người dùng thấy:**
  - Nhóm theo khu (trung tâm · phía tây · ven biển Thuận An · **phía nam Phú Lộc – Lăng Cô** — Vedana ở Cầu Hai cách Lăng Cô ~20 km, E), trong khu chia 3 mức; trong mức: có ảnh trước, rồi hạng cao, rồi tên.
  - Mỗi cơ sở: ảnh nếu có (không có ⇒ ô màu), tên, hạng sao, địa chỉ, nút **Bản đồ** / **Tìm phòng**.
  - Dòng nguồn: "danh mục Cục Du lịch Quốc gia, lấy 12/11/2026 — chưa kiểm giá, phòng trống".
  - Lọc theo mức bằng nút; không ô tìm chữ; không khoảng cách (toạ độ Places chỉ 81 / 140).
- **Dữ liệu (E, đếm 0 USD [đã chạy]):**
  - Trùng địa chỉ: 6 cặp. **1 cặp cùng tên** (La Perle / La Perle Huế, cùng số nhà viết khác) ⇒ gộp 1 dòng. 5 cặp khác tên (danh mục có thể ghi cả tên cũ / mới) ⇒ giữ cả hai.
  - Bỏ Đô Thành (A Lưới) và Alba Thanh Tân (Phong Điền): lịch không có điểm nào ở đó.
  - La Vela (5 sao, khu đô thị Đông Nam Thủy An) và SBH Gloria (4 sao, "xã Phú Vinh"): 1 lượt Places mỗi cơ sở (≈ 0,002 USD) lấy toạ độ ⇒ gần trung tâm / đúng phía biển thì xếp khu, không ra thì bỏ. Đổi bảng = bản v3 mới (không sửa tại chỗ file main đang trỏ).

## 2. Biểu mẫu hỏi ngân sách ở

- **Đổi gì:**
  - `chung.jsx` `BIEU_MAU`: nhóm "Chỗ ở theo hạng sao (không bắt buộc)" với nút **1 sao · 2–3 sao · 4–5 sao** (nhãn kèm sao để không đọc như giá — B); không chọn = như hiện nay.
  - `hoi_lai.TruongInput`: `ngan_sach: Literal["binh_dan","vua","cao"] | None`.
  - Giữ mức qua lượt **sửa lịch bằng lời** — đủ 5 chỗ chạm (B): `ThamSoV2.ngan_sach` + `tu_truong` (`lich_trinh_v2.py:96–100`) · dict `tham_so` do `xep_v2` dựng (`:308`, sửa lịch xếp lại qua `sl._xep` ⇒ thiếu ở đây là mất mức) · `sua_lich_v2._ts` (`:80–82`) · `gan_o_an` đọc `ts_k["ngan_sach"]` ⇒ `o_dau` ⇒ `chon_co_so` (`len_ke_hoach.py:115–125`) · `O_BIEU_MAU_V2` (`assistant.py:62`). Không vào bộ xếp điểm.
  - Dòng "Mình hiểu" **không** thêm mức (ô Nơi ở đã cho thấy; ít chỗ chạm). Ghi chú: dòng này nằm trong chữ trả lời `ghep_chu`, không trong tin nhắn gửi model.
  - `luu_tru_lich.chon_co_so(…, muc=None)`: có mức ⇒ ≤ 5 cơ sở của mức đó, cùng luật xếp (hạng cao trước ⇒ gần cụm ⇒ có ảnh ⇒ tên); không mức ⇒ `SO_THEO_MUC` (2, 2, 1) như cũ.
  - Mức trống ở khu đó (hiện 0 khung) ⇒ im lặng dùng (2, 2, 1), không thêm câu (B: nhánh không bảo vệ gì).
- **Không đổi:** không giá phòng; model không thấy mức (khối nơi ở không vào tin nhắn gửi model).

## 3. Tiêu chí + cách đo (ghi trước)

| # | Tiêu chí | Đo |
|---|---|---|
| T1 | Không chọn ngân sách ⇒ ô "Nơi ở" **giống byte** bản hiện nay ở 3.840 / 3.840 khung | mô phỏng, test |
| T2 | Chọn mức ⇒ 100 % cơ sở hiện đúng mức, ≤ 5, cùng khu như cũ | mô phỏng 3.840 × 3 |
| T3 | Q1: tin nhắn gửi model giống byte có / không ngân sách | test (code chạm biểu mẫu → `tham_so`) |
| T4 | Sửa lịch bằng lời giữ mức ngân sách | 1 test đi qua `sl.ap` thật (khung ⇒ `_xep` ⇒ `gan_o_an`) |
| T5 | API trang: đúng tập cơ sở đã chốt, đúng tập trường; 0 dòng trùng tên + địa chỉ; 0 trường giá / điện thoại / toạ độ; ảnh chỉ `/anh/khach_san/…jpg`; link chỉ 2 gốc (Google Maps tìm, Booking tìm) | test |
| T6 | Trang: 0 lỗi console, 0 yêu cầu ra ngoài origin, link `_blank` + `noopener`; khổ 1440 (+ 390 chỉ khi trang có bố cục riêng cho điện thoại) | Playwright 1 lượt, không gọi model |
| T7 | `TruongInput` từ chối giá trị lạ ⇒ 422 | 1 ca test (Literal + `extra="forbid"` của thư viện đã lo phần còn lại) |

Test rộng `backend/tests` 1 lần trước bàn giao. Không bộ kín.

## 4. Tiền và công

- 0 USD cho code + mô phỏng + trang (không gọi model). Playwright ngân sách: 1 lượt xếp lịch ≈ 0,0007 USD. Places 2 cơ sở ≈ 0,002 USD. **Tổng ≤ 0,01 USD.**
- Công ước: trang ~2–3 giờ · ngân sách ~1,5–2 giờ. Hai nhánh riêng, ngân sách trước (nhỏ, chạm ít file); một người review mỗi nhánh.

## 5. Khi nào sai / giới hạn

- **Danh mục cũ dần:** lấy 12/11/2026; cơ sở có thể đóng / đổi hạng ⇒ trang ghi ngày lấy, không nói "còn phòng".
- **Hạng sao ≠ giá:** "bình dân / vừa / cao cấp" là suy từ hạng; 1 sao vẫn có thể đắt hơn 2 sao. Câu chữ nói "theo hạng", không nói "theo giá".
- **Ảnh:** 69 / 140 không ảnh ⇒ trang nửa có ảnh, nửa ô màu. Nhóm bình dân trung tâm chỉ 26 / 70 có ảnh. Thêm ảnh là việc riêng, theo luật chọn ảnh (người giao nhìn lại 100 %).
- **Vẫn tất định:** chọn cùng mức ⇒ cùng 5 cơ sở ở mọi lịch trung tâm. Không xáo ngẫu nhiên (lịch phải lặp lại được); trang là chỗ cho khách tự xem thêm.
- **Ven biển mỏng:** Thuận An mỗi mức 1–2 cơ sở; Lăng Cô không có mức vừa.

## 6. Rà khung AI FDE (ngắn)

| Mục | Hiện trạng | Khớp / lệch | Đề xuất |
|---|---|---|---|
| Có cần model không | Chọn cơ sở + dựng trang hoàn toàn bằng code (`luu_tru_lich.py:68`) | khớp | giữ: lọc theo mức là luật, code làm |
| Chia việc code ↔ model | Model chỉ viết câu tả điểm; nơi ở không vào `tin_nhan_model` (`lich_trinh_v2.py:605`) | khớp | T3 khoá |
| Công cụ / vòng lặp mới | không | — | — |
| Nguồn dữ liệu mới | không; bảng đã có (danh mục nhà nước + ảnh đã duyệt) | khớp | |
| Bộ ba chết người | (a) không dữ liệu riêng tư · (b) tên cơ sở từ danh mục công khai, không vào model · (c) đường ra = link người dùng tự bấm | không đủ ba | |
| Chữ người dùng | ngân sách là enum, `extra="forbid"` (`hoi_lai.py:52`) | khớp | T7 |
| Đường hiện dữ liệu mới (trang) | tên từ bảng ⇒ React tự thoát ký tự; link do code dựng từ 2 gốc cố định; ảnh chỉ gốc tự host (kiểm lúc nạp `luu_tru_lich.py:45`) | khớp | T5, T6 |
| Dữ liệu cá nhân | mức ngân sách không lưu, không log | khớp | nếu sau này bật "nhớ sở thích" ⇒ xét lại |
| Rào đo hai chiều | T1 (không chọn ⇒ giống byte) + T2 (chọn ⇒ đúng mức) | khớp | |

## 7. Câu cần A / User quyết

1. Trang có lên thanh trên cùng không, hay chỉ mở từ ô "Nơi ở" của lịch? **Nhóm đề xuất: chỉ từ lịch** (B, C, E) — ít đổi giao diện; lợi chưa đếm được.
2. Làm cả hai hay chỉ ngân sách trước? **Nhóm đề xuất: cả hai, ngân sách trước**, trang bản tối thiểu.
