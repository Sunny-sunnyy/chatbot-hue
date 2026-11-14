# Review nhánh `p9-quan-lich` `b03ed28` (C): quán ăn gợi ý trong lịch bản 2

- **Người kiểm:** B, 16:41 14/11/2026.
- **Mức:** nhẹ, một review cả nhánh, 0 USD (A giao).
- **Kết luận: `ready_for_user_confirmation`.** 0 blocker, 0 major, 2 minor.

## Cổng tối thiểu
- **Diff:** 9 file, +241 / −5. Khuôn giống khối "nơi ở": module thuần `quan_lich.py`, cờ + nạp bảng lúc khởi động, `lich["an"]` sau `dung_lich`, `ghep_chu`, thẻ giao diện. Không có gì ngoài phạm vi. `flags_from` ghim thêm `quan_lich: False`.
- **A dặn kiểm ba chỗ:**
  - **Tên quán OSM là chữ người ngoài viết.**
    - Lúc nạp, `_BAN` chặn ký tự điều khiển (\x00–\x1f, \x7f), `http(s):`, `www.`, `< >`; tên dài hơn 80 ký tự cũng bị chặn. Sai một dòng thì server không khởi động.
    - Link OSM phải đúng gốc `https://www.openstreetmap.org/`.
    - Giao diện vẽ tên bằng chữ React (không HTML), link chỉ nhận `#/kham-pha/bai/…` (quán kho) hoặc gốc bản đồ của lịch, mở tab mới khi bấm.
    - Đủ cho bảng hiện tại; xem m-1.
  - **Không vào chuỗi gửi model:**
    - `tin_nhan_model` chỉ đọc `id_muc`, `ten`, `nguon`;
    - lần hiểu ý sửa (`sua_lich_v2.tin_nhan_hieu`) dựng từ `khung` + bảng điểm, không từ `lich`;
    - lịch sử hội thoại chỉ nhớ câu hỏi (`nho_cau_tra_loi: false`), nên chữ `ghep_chu` có tên quán không quay lại model.
    - ⇒ đúng; xem m-2.
  - **Trần 2 km:** `_chon` lọc `km <= KM_TOI_DA` trước khi xếp. Test mô phỏng 3.840 khung khẳng định mọi quán ≤ 2 km và cùng cụm; test riêng "điểm xa / không toạ độ ⇒ không dòng".

## Kiểm [Chạy] (0 USD)
- `tests/test_quan_lich.py` không khoá, worktree tách ở `b03ed28`: **10 đạt** (11 s).
- **Bảng `bang_quan_lich_v1.json` (460 quán):**
  - 28 / 28 mã bài của quán kho có trong build record hiện tại (kho 216 file sau lần ghi kho 3) ⇒ link "Đọc bài" không gãy;
  - 0 tên có ký tự định dạng ẩn (Unicode Cf); 0 tên giống tên miền;
  - 6 tên có ký tự Markdown (ngoặc, gạch dưới — vd "Tai Phu Restaurant (Nem Lui)"), vô hại.
- **Dò bộ lọc tên:** "Quán\u202eabc" (đảo chiều chữ), "Quán\u200bx" (ký tự vô hình), "[x](javascript:…)", "quanngon.vn" đều **lọt** `_BAN` (xem m-1).
- `markdown.js` (DOMPurify) bỏ link `javascript:`. Chữ `ghep_chu` chỉ dùng cho nút chép / tải, thẻ lịch không dựng Markdown từ nó.

## Finding
- **m-1 (minor, gia cố) — `_BAN` chưa chặn ký tự định dạng Unicode và cú pháp link Markdown.**
  - Hiện 0 tên trong bảng dính, và đường hiện tên không dựng link ⇒ không có lỗ thật. Nhưng bảng sẽ dựng lại từ OSM: một tên có U+202E có thể làm chữ hiển thị đảo ngược; một tên "[…](//host)" sẽ thành link nếu sau này chữ `ghep_chu` được dựng Markdown ở đâu đó.
  - Đề xuất: thêm vào `_BAN` các ký tự loại Cf (\u200b–\u200f, \u202a–\u202e, \u2066–\u2069), `](` và `//`; thêm 2 ca vào `test_table_load_rejects_bad_rows`.
- **m-2 (minor, ghi chú) — phụ thuộc vào `nho_cau_tra_loi: false`.**
  - Nếu sau này bật nhớ câu trả lời, chữ `ghep_chu` (có tên quán OSM do người ngoài viết) sẽ vào lịch sử gửi model. Đó là chữ ngoài đi vào lời nhắc.
  - Đề xuất: ghi một dòng ở comment cờ `quan_lich` hoặc trong report. Không cần sửa code bây giờ.

## Ghi nhận
- Ba quyết định trong phạm vi (trần 2 km, bữa tối gần điểm tối, tên có "cà phê" ⇒ cà phê) đều xuất phát từ lỗi do lượt đo bắt ⇒ hợp lý.
- Report ghi rõ giới hạn "ngoài trung tâm gần như chỉ quán OSM chưa kiểm". Đúng là điểm yếu User nên biết khi bật.
