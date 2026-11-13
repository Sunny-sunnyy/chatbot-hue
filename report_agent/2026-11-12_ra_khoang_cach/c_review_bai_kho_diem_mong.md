# Review: 2 bài kho NHÁP cho 2 điểm "cần bổ sung kho" của lịch trình (việc của E)

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 3 minor — sửa chữ lúc ghi kho, không cần vòng review riêng)
Người kiểm: C (`hue-rag-eb`, Claude Code)
Date: 21:49 13/11/2026 (`date`)
Canonical guide: luật kho `session_prompt/Session_Prompt.md` §5 · A giao (13/11)
Implementation report: `data/sua_kho_2026-11-13_diem_mong/BIEN_BAN.md` (private)

## 1. Phạm vi đã review
Hai bài nháp (private, CHƯA vào kho) trong `data/sua_kho_2026-11-13_diem_mong/`: bài về **bảo tàng cổ vật cung đình** (đích đề xuất `heritages/heritage/`) và bài về **không gian lưu niệm của một hoạ sĩ ở phía tây nam thành phố** (đích `travel/places/`) + biên bản nguồn của E. Không có git (`data/`), review trên file hiện có. Không chạm kho; tìm trong kho chỉ qua `scripts/grep_kb.sh`. 0 USD.

## 2. Findings
Không có blocker / major.
- **m-1** — bài không gian lưu niệm, mục "Có gì để xem": ghi một **"phòng trưng bày"** mang tên một loạt tác phẩm. Trang chính thức (WebFetch, mục 3) chỉ có tên đó như **một nhóm tác phẩm trong menu**, không nói là một phòng riêng. Đóng: viết "loạt tác phẩm …" thay cho "phòng trưng bày …".
- **m-2** — cùng bài, dòng "Ngoài trời" (vườn tượng, đường hầm ánh sáng, vườn hoa) + dòng tiện ích: chỉ một nguồn là bài kho hiện có; trang chủ chính thức không nhắc (E đã tự ghi ở biên bản). Chấp nhận được vì nguồn là kho; nếu muốn chắc thì mở thêm một nguồn (biên bản đã nêu một bài báo 2020). Không chặn.
- **m-3** — bài bảo tàng: ý "năm 1909 dựng lại làm thư viện" chỉ một nguồn (Wikipedia, chưa mở bài báo gốc nó dẫn) — E đã ghi. Không chặn; giữ hoặc thêm chữ "theo …".

## 3. Kiểm luật kho §5 (cả hai bài)
Bắt đầu bằng `#` ✓ · không YAML ✓ · không mục / trường rỗng ✓ · không "Liên kết nội bộ" ✓ · `## Nguồn dữ liệu` có ngày xem ✓ · **không giá vé** (trang chính thức có giá — bài không chép ✓), không số điện thoại (trang chính thức có — không chép ✓), không link đặt chỗ ✓ · nội dung tự nhiên, độc lập, hướng người hỏi ✓. Địa chỉ: bài ghi địa giới sau 7/2025 theo kho + nêu tên cũ — trang chính thức còn ghi tên cũ ⇒ cách viết đúng.

## 4. Cách người kiểm chạy lại thật
- **Bộ chia đoạn thật** (`chunk_document` + `parse_markdown_blocks`, tokenizer mặc định, `HF_HUB_OFFLINE=1`, đường dẫn nguồn = đích đề xuất): **12 đoạn / 0 lỗi / dài nhất 582 ký tự** và **15 / 0 / 562** — khớp số E. Tiêu đề mục dài nhất 38 / 45 ký tự (không có lỗi tiêu đề dài như bài nháp ăn gần trước đây).
- **WebFetch 3 trang (13/11):** (1) trang báo nhà nước 2023 — các mốc tên gọi theo năm, số hiện vật, số bảo vật quốc gia, kiến trúc nhà, đơn vị quản lý: khớp bài ✓. (2) trang chính thức của không gian lưu niệm — diện tích, giờ mở + ngày nghỉ: khớp ✓; tên loạt tác phẩm chỉ ở menu (m-1); không nhắc khu ngoài trời (m-2). (3) trang niên biểu chính thức — các mốc đời họa sĩ + ngày khai trương: khớp ✓. (Mô tả ở mức loại để không chép nội dung kho vào file tracked.)
- Không mở lại các ý lấy từ kho (đã có trong kho, E tìm bằng `grep_kb.sh`).

## 5. Ba chỗ kho lệch nguồn ngoài (E nêu, không sửa kho) — người kiểm đồng ý cách xử lý
Bài nháp theo nguồn chính thức / mới hơn và **không** sửa kho: (1) tên người lập không gian lưu niệm (kho ↔ trang chính thức khác tên) · (2) số nhà của khu trưng bày cùng tên hoạ sĩ trên một trục đường ven sông (kho ↔ trang Sở Du lịch khác số; bài bỏ số nhà) · (3) một bài vé trong kho xếp bảo tàng vào cụm bờ nam, trong khi bảo tàng ở trong Kinh thành (bờ bắc). Theo §5 ⇒ A trình User, không tự chọn một phía khi sửa kho.

## 6. Giới hạn
Chưa đo tầng tìm (đoạn mới có chen câu cũ không) — việc của lượt đo sau khi ghi kho (tiêu chí K3 của spec kho 3). Bài không gian lưu niệm có mục "phân biệt" nhắc tên khu trưng bày cùng tên hoạ sĩ ⇒ câu hỏi về khu đó có thể kéo đoạn này lên — đúng ý (giúp phân biệt), nhưng nên có trong bộ đo.

## 7. Kết luận
`ready_for_user_confirmation`: sửa m-1 (một chữ) khi ghi kho; m-2, m-3 tuỳ E. Ba chỗ lệch kho ⇒ A hỏi User.
