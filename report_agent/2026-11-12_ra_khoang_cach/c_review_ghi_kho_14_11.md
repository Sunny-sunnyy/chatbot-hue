# Review — gói ghi kho 14/11 của E (trước khi ghi)

Người kiểm: C (`hue-rag-b4`) · 09:54 14/11/2026 (`date`) · skill `risk-gated-agent-review` · 0 USD (1 WebFetch trang công khai của Sở Du lịch Huế).
Đầu vào: `data/sua_kho_2026-11-14_ghi_kho/kho.diff` (211 dòng) + `tools/ghi_kho.py` (private). Không đọc `evaluation/`, `*sealed*`; grep kho bằng `scripts/grep_kb.sh`.

**Kết luận: changes_requested — 1 major (sửa nhỏ), 0 blocker.** Sửa xong M-1 thì C coi là ready, không cần review vòng 2. C chỉ đọc lại một dòng diff.

## Đã kiểm
- **3 bài mới = bản nháp đã review:** `ghi_kho.py` chép thẳng từ file nháp (`shutil.copyfile`), không dựng lại. Bài đi lại md5 `1ccfc5f639d6`. Hai bài điểm mỏng có sửa m-1 của C (13/11). Ba thư mục đích đã có sẵn trong kho.
- **Khuôn kho:** cả 3 bài bắt đầu bằng `#`, không YAML, không mục rỗng, không có "Liên kết nội bộ", có `## Nguồn dữ liệu`.
- **3 sửa ở 2 bài vé:** nội dung khớp gói User duyệt. Mỗi sửa thêm đúng 1 dòng nguồn có ngày đối chiếu. ③ Địa chỉ và giờ mở cửa bảo tàng (số nhà trên đường Lê Trực, 7:00 – 17:30) khớp trang Sở Du lịch C mở lại hôm nay. Phường trên trang là tên phường cũ; kho dùng tên phường sau sáp nhập 7/2025, đúng như các bài khác.
- **Script:** `write` đòi file khớp bản sao trước khi ghi. Mỗi chuỗi cũ phải có đúng 1 lần. Script kiểm hết rồi mới ghi file nào. File mới đã có thì dừng. `lui` trả kho về như cũ. Đủ cho một lần ghi, không thừa.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| M-1 | major | bài `travel/places/Phố đi bộ Nguyễn Đình Chiểu.md` dòng 56 (ngoài diff) | Sửa ② đổi số nhà khu trưng bày Lê Bá Đảng trong bài vé thành số 17 (theo trang Sở Du lịch), nhưng bài phố đi bộ vẫn ghi **số 15A**. Sau khi ghi, kho **tự mâu thuẫn** về số nhà, và trợ lý có thể trích bất kỳ bên nào. Trang Sở Du lịch ghi Bảo tàng Mỹ thuật ở số 17, có khu trưng bày Lê Bá Đảng bên trong, và **không nhắc số 15 hay 15A**. Bài mới của Không gian lưu niệm chỉ ghi "đường Lê Lợi", không có số. | Thêm một sửa vào `EDITS` cho dòng 56, cùng mục ② User đã duyệt: ghi theo nguồn (khu trưng bày trong Bảo tàng Mỹ thuật Huế, số 17), **hoặc** bỏ số nhà ở dòng này. Chạy lại `diff`. Nếu A thấy việc này ngoài gói ⇒ A quyết, không tự chọn. |

## Ghi chú (không chặn)
- Lần review kho 3 ngày 13/11, C không bắt được dòng 56. Bài học: sửa một sự kiện trong kho thì grep mọi chỗ khác nhắc cùng sự kiện, không chỉ chỗ được báo.
- `performing_arts_guides.md` dòng 118 chỉ ghi "đường Lê Lợi", không có số ⇒ không mâu thuẫn.

## Vòng sửa (09:55 14/11/2026, `date`)
M-1 **đóng**: E thêm sửa thứ tư (A chốt cùng mục ②). Dòng 56 bài phố đi bộ đổi số nhà 15A ⇒ 17, đúng như nguồn. `kho.diff` dựng lại 222 dòng. File thứ ba nằm trong `EDITS` nên sao lưu / ghi / lùi đều có file này. **Kết luận: ready** — E ghi được.
