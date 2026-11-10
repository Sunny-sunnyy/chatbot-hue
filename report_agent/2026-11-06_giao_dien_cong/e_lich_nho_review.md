# Review: việc nhỏ lịch trình — (1) sao chép / tải · (4) câu buổi tối · (6) link Maps theo toạ độ (+ sửa m-1 / m-2 review bản đồ)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 3 minor). Riêng (6) **chạy ngay khi merge** (biểu mẫu đang bật) ⇒ nên xem m-1 / m-2 trước.
Người kiểm: E (Claude Code, `hue-rag-22`)
Date: 10:36 08/11/2026
Implementation report: `report_agent/2026-11-06_giao_dien_cong/b_lich_nho_implementation.md`

## 1. Phạm vi đã review

- **Git:** `origin/p11-lich-nho` = `a43cd14`. Merge-base với `main` (`27ba49e`) là `d0adf31` (nhánh bản đồ, đã vào `main` qua `a4fde29`) ⇒ diff thật = 2 commit:
  - `098a710`: (1) / (4) / (6);
  - `a43cd14`: sửa m-1 / m-2 của review bản đồ, B đẩy sau khi A giao.
- 9 file +102 / −28. `git diff --check`: sạch. Report của B viết trước `a43cd14` ⇒ phần m-1 / m-2 E kiểm riêng.
- **Đọc exact diff:** `lich_trinh.py` (`CAU_KHONG_XEP`, `MA_TOI`, `DONG_KHUNG_TOI`, `xep`, `map_url`, `ban_do`), `assistant.py` (`from_settings`, `lich_cho_giao_dien`), `settings.yaml` (chú thích), `chat.jsx` (`vanBanLich`, `LuuLich`, `answerRef`), `BanDoLich.jsx`, `toaDo.js` (mới), `index.css`, 2 file test.
- **Đối chiếu tiêu chí A giao:** (1) không gọi server, chữ khớp lịch đang hiện, không HTML thô · (4) mã mới chỉ khi chưa nêu sở thích, kiểm cuối vẫn áp · (6) toạ độ đúng điểm, thiếu ⇒ link tên, URL do code dựng · chuỗi gửi model giống byte · m-1 / m-2.
- **Ngoài phạm vi / lệch:** không thấy. B không đụng định tuyến (đúng lời A dặn).

## 2. Findings

Không có blocker / major.

### m-1 (minor, sản phẩm — cần A / User chọn) — link theo toạ độ mất thẻ địa điểm của Google Maps

- Vị trí: `lich_trinh.map_url` — có toạ độ ⇒ `query=<vĩ độ>,<kinh độ>`.
- Bằng chứng (file tải ở lượt E chạy, `e_review/ui/ban_do_tat_lich.txt`): 5 / 6 link là dạng toạ độ.
  - Mở link toạ độ trên Google Maps chỉ ra **một ghim trần tại toạ độ**, không có thẻ địa điểm (tên, giờ mở cửa, ảnh, đánh giá) như khi tìm theo tên [Suy — theo tài liệu Maps URLs: tham số `query` là toạ độ ⇒ đặt ghim tại đó; E không mở trình duyệt Google].
  - Đổi lại: không lệch sang nơi trùng tên (lý do C197).
- Tác động: người dùng bấm "mở bản đồ" thấy đúng chỗ (nếu toạ độ đúng) nhưng mất thông tin nơi đó. Áp cho **mọi** lịch từ biểu mẫu ngay khi merge, không qua cờ.
- Tiêu chí đóng: A / User chọn (a) giữ toạ độ, (b) giữ link theo tên, hoặc (c) toạ độ chỉ cho các điểm C197 thấy lệch theo tên. Ghi lựa chọn vào handoff. Không chặn merge nếu chọn (a).

### m-2 (minor, dữ liệu) — một toạ độ có thể không đúng điểm mang tên

- "Kinh thành Huế (Ngọ Môn – Kỳ Đài)" = 16,4694; 107,5822, còn "Đại Nội Huế" trong **cùng bảng** = 16,4685; 107,5764 ⇒ lệch khoảng 0,6 km về phía đông. Ngọ Môn là cổng chính của Đại Nội nên toạ độ này khó là Ngọ Môn [Suy, chưa mở bản đồ]. B cũng ghi điểm này.
- Tiêu chí đóng: User mở `data/phase_11/lich_nho/kiem_17_link.md` (B đã soạn), tick cột "Đúng chỗ?"; điểm sai ⇒ bỏ toạ độ điểm đó. Nên làm **trước** merge vì (6) không có cờ.

### m-3 (minor, vận hành) — file toạ độ thành bắt buộc khi biểu mẫu bật

- `assistant.py` `from_settings`: toạ độ nạp khi có bảng lịch (không còn phụ thuộc `ban_do_lich`) ⇒ thiếu `diem_toa_do_v5.json` thì app **không khởi động** (đúng thiết kế fail-closed, cùng kiểu bảng điểm).
- B đã ghi allow-list deploy ⇒ chỉ cần A chắc mục này nằm trong checklist deploy (E-dep).

### Ghi nhận (không phải finding)

- (4) đổi chữ khung gửi model **chỉ** ở lượt câu gõ tự do có xin buổi tối + chưa nêu sở thích (`DONG_KHUNG_TOI` mới). Cờ `lich_trinh` đang tắt ⇒ production không đổi. Bộ Q1 không có lượt này (B đã ghi).
- (1) `vanBanLich` lấy `innerText` của khối trả lời (đã qua DOMPurify) ⇒ chữ thường. Link chỉ lấy `map_url` đã lọc `MAP_PREFIX`. Câu hỏi + tóm tắt lấy từ lượt (biểu mẫu: chữ cố định). File chỉ ở máy người dùng.
- Sửa m-1 / m-2 bản đồ: ghim chỉ nhận `Number.isInteger(thu_tu) && thu_tu > 0`; một hàm `toaDoHopLe` chung ở `toaDo.js` (bundle chính, nhỏ) ⇒ đóng m-1, m-2 của `e_ban_do_review.md`.

## 3. Cách người kiểm chạy lại thật

Worktree `/tmp/e_ln` (detached tại `a43cd14`), symlink `data/` + kho.

1. **Ca dò 0 USD, khác cách B** (B: test đơn vị vài ca): `data/phase_11/lich_nho/e_review/do_lich_nho.py`, chạy trên `main` (thư mục chính, `backend/` sạch) và trên nhánh.
   - **Mọi 864 tổ hợp** (số ngày × đi cùng × kiểu đi × sở thích × xin buổi tối), mỗi tổ hợp ghi: mã `khong_xep`, `kiem_khung`, `khung_chu`, `kiem_cuoi`.
   - Ba câu cho `kiem_cuoi`: (a) "nói ngược" hứa buổi tối, (b) model chép nguyên dòng khung buổi tối, (c) model chép câu lý do.
   - Link Maps 28 điểm ↔ bảng toạ độ.
2. **Q1 mới:** `capture_all.py` (0 USD) trên `main` `27ba49e` và trên nhánh, `cmp`. Không dùng mốc `2a2a40e` của B.
3. **Trình duyệt** `data/phase_11/lich_nho/e_review/ui_luu_lich.py`: 1 lượt biểu mẫu thật (3 ngày · Di tích) mỗi lần, server cờ `ban_do_lich` **tắt** (như production) rồi **bật** (sửa tạm `settings.yaml` của worktree, đã trả lại). Kiểm:
   - ghi mọi request lúc bấm 2 nút;
   - clipboard ↔ file;
   - `innerText` của đúng khối trả lời ⊂ file;
   - dò `<thẻ`, `**`, `](` trong file;
   - mọi `map_url` của sự kiện SSE `lich_trinh` có trong file;
   - cờ bật: đếm `.ghim` từng ngày ↔ số điểm có toạ độ trong SSE.
4. Test: `test_ban_do_lich`, `test_b5_lich_trinh`, `test_static_ui`, `test_cong_dot_1`, `test_b5b_thoi_tiet`, `test_b6_tra_web`.

## 4. Kết quả quan sát (lần chạy mới của E)

| Kiểm | Kết quả |
|---|---|
| (4) 864 tổ hợp `main` ↔ nhánh | **48 / 864 khác, cả 48 đúng dạng mong đợi**: xin buổi tối + chưa nêu sở thích + không đi cùng trẻ nhỏ / người lớn tuổi ⇒ `toi_khong_diem` thành `toi_chua_so_thich`, mã khác giữ nguyên. 816 tổ hợp còn lại giống hệt (kể cả `khung_chu`) |
| (4) kiểm cuối | câu "nói ngược" bị bắt (`toi_ngoai_khung`) ở **mọi** tổ hợp có mã buổi tối (cả mã mới); model chép nguyên dòng khung / câu lý do mới ⇒ **không** bị bắt nhầm; `kiem_khung` rỗng ở mọi tổ hợp |
| (6) link | **28 / 28 đúng**: 17 điểm có toạ độ ⇒ `query` = đúng "vĩ độ,kinh độ" của bảng, gốc `https://www.google.com/maps/search/`; 11 điểm thiếu ⇒ "tên, Huế" như cũ. URL chỉ ghép từ bảng (không chữ người dùng / model) |
| Q1 chuỗi gửi model | **giống byte** `main` `27ba49e` (228 / 228) |
| (1) cờ bản đồ tắt | lúc bấm 2 nút: **0 request**; clipboard = file; chữ đang hiện ⊂ file; **0** dấu HTML / Markdown thô; 6 / 6 link trong file; dòng cuối "có thể sai…"; 0 lỗi CSP / console |
| (1) + m-1 / m-2, cờ bật | clipboard = file, chữ ⊂ file, 0 HTML thô, mọi link có; **ghim mỗi ngày 2 / 1 / 2 = số điểm có toạ độ trong SSE**; 0 lỗi CSP / console |
| Test | **440 passed** |
| Log | 2 dòng `chat_metrics` = 2 lượt; chữ câu biểu mẫu trong log = 0 |

**Tiền E: 0,001028 USD** (2 lượt biểu mẫu). Dò + Q1 + test: 0.

## 5. Giới hạn hoặc phần chưa chạy

- Lượt cờ bật: bộ đếm request chạy tiếp lúc E bấm đổi ngày để đếm ghim (sau 2 nút lưu) ⇒ có 12 request tile, **không tách** được lúc bấm 2 nút. Bằng chứng "không gọi server" lấy từ lượt cờ tắt (0 request). Code `LuuLich` không phụ thuộc cờ.
- E không mở link toạ độ trên Google Maps bằng trình duyệt (m-1 là suy theo định dạng URL; m-2 là so hai toạ độ trong bảng).
- (4) chỉ kiểm bằng hàm thật (`xep`, `kiem_cuoi`), không lượt model — đường câu tự do đang tắt.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Code đúng tiêu chí A giao; chuỗi gửi model giống byte.
- **Trước khi merge** nên có lựa chọn của A / User cho m-1 (giữ link toạ độ hay tên), và User mở 17 link (m-2), vì (6) tới người dùng ngay, không có cờ.
- Không cần vòng review mới nếu chỉ bỏ toạ độ vài điểm trong file dữ liệu.
