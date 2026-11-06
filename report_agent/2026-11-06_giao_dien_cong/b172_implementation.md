# Implementation Report: B172 — nghiên cứu giao diện cổng du lịch

Người làm: B (Claude Code, Opus 5.5)
Date: 22:26 06/11/2026 (`date`)
Canonical guide: việc B172 trong `session_prompt/CURRENT_HANDOFF.md` mục "Việc giao — giao diện cổng du lịch" (A, 22:01 06/11/2026).

## 1. Phạm vi

User chọn tối 06/11: làm giao diện kiểu cổng du lịch (theo khuôn Huế TRIPO, mức đầy đủ, hai đợt). B172 là phần nghiên cứu cho A viết spec đợt 1.
- 0 USD, không sửa code.
- Xem mọi trang công khai của Huế TRIPO; tìm 5–8 trang cùng đề tài; viết tổng hợp các mẫu nên học / không nên chép.
- Luật như các vòng TRIPO trước: một trình duyệt, không đăng nhập, không nhập thông tin cá nhân, không bấm đặt / gọi / chia sẻ / gửi, không cấp vị trí.

## 2. Thay đổi chính

Không đổi code / kho / cấu hình. File mới (đều ở `data/`, private, trừ report này):
- `data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md` — **file chính**: TRIPO từng trang, bảng so sánh 6 trang, **15 mẫu nên học** (thấy ở đâu · vì sao hợp · dữ liệu có / chưa có), **10 điều không nên chép**, giới hạn.
- `…/tools/`: 6 file. `do_menu.py`, `chup_tripo.py`, `tro_ly_noi.py`, `chup_khac.py` (Playwright), `thu_nho.py` (thu nhỏ ảnh để xem), yêu cầu Codex. Kèm số đo `do_tripo.json`, `do_khac.json`, `tro_ly_noi.json`, `menu.json`.
- `…/anh/`: `tripo/` (34 lượt chụp + 8 ảnh header / trợ lý nổi), `khac/` (15 lượt), bản thu nhỏ `*_nho/`. 219 MB.
- `data/tra_cuu_cli/2026-11-06_b172-cong-du-lich-ai/` — kết quả Codex.

## 3. Cách đã chạy thật

Từ gốc repo, `.venv` của dự án (Playwright 1.58, chromium headless):
- `timeout 180 uv run python data/nghien_cuu_giao_dien_2026-11-06/tools/do_menu.py`
  - Lấy menu trang chủ, rê chuột "Khám phá". 10 đường dẫn: trang chủ, Trợ lý AI, 7 mục, Bản đồ.
- `timeout 1200 uv run python …/tools/chup_tripo.py`
  - 17 trang × 1440 / 390 = 34 lượt, 0 lỗi.
  - Mỗi lượt: ảnh màn đầu + cả trang, số đo (font, màu, cỡ tiêu đề, phần tử cố định, thẻ lặp, nút, ô nhập).
- `timeout 300 uv run python …/tools/tro_ly_noi.py`
  - Cuộn xem header, bấm mở nút trợ lý nổi ở 2 trang × 2 cỡ màn hình. Không gõ.
- `timeout 900 scripts/tra_web_codex.sh …/tools/yeu_cau_codex_cong_du_lich.md b172-cong-du-lich-ai`
  - 281 s. 14 lượt tìm, 24 trang mở thật, 1 URL tự khai (`visitwales.com`, B đã mở lại), 0 lệnh shell.
- WebFetch kiểm 3 ý chính: Visit Wales — trợ lý Gwydion; GO TOKYO — trang "Tokyo Navigation AI"; GoVietnam — bố cục + lối vào trợ lý. Cả 3 khớp báo cáo Codex.
- `timeout 900 uv run python …/tools/chup_khac.py`
  - 5 trang (Visit Wales, GO TOKYO + trang AI, GoVietnam + `/chat/`, Visit Vietnam, Layla).
  - Trang chủ 1440 + 390, trang khám phá 1440: 15 lượt, 0 lỗi.
- Đếm dữ liệu kho bằng `scripts/grep_kb.sh -l` (chỉ số file, không chép nội dung) + đọc khoá trường của `data/phase_9/lich_trinh/diem_v3.json`.

## 4. Kết quả quan sát

**TRIPO [Chạy]:**
- Khung chung:
  - Header cố định 81 px (trang chủ trong suốt, cuộn thì trắng).
  - Màu nhấn tím `#7008E7`, chữ Roboto 16 px, tiêu đề hero chữ có chân.
  - Thẻ bo 16–24 px; chip và nút bo tròn hẳn.
- Trợ lý vào trang theo **2 đường**:
  - Nút nổi 80 px ở mọi trang ⇒ khung chat 380 × 560 ngay trang đó (điện thoại: phủ cả màn).
  - Trang "Trợ lý AI" riêng: biểu mẫu chip 4 tab + ô chat.
- Điện thoại: thanh dưới 5 mục, Trợ lý AI là nút giữa.
- 7 trang danh sách cùng một khuôn: chip loại con + "Bộ lọc (số)" + lưới 4 cột 12 thẻ.
- Trang chi tiết: tóm tắt, hộp thông tin bên phải, bản đồ nhỏ, "Báo cáo thông tin".
- Bản đồ: Leaflet, 9 lớp, 3.006 điểm.

**Điểm yếu TRIPO thấy được:**
- Số đánh giá cùng một điểm lệch giữa bản laptop (4,7 / 17 lượt) và điện thoại (4,9 / 500).
- Chuỗi `">` lọt ra chữ ở thẻ lữ hành.
- Sự kiện đã qua vẫn ở "nổi bật".
- Nhiều "Đang cập nhật" / "Liên hệ".

**5 trang khác [Chạy, 3 ý chính kiểm bằng WebFetch]:** trợ lý đặt ở nút nổi (Visit Wales "Ask Gwydion", GoVietnam), cụm nút nổi (GO TOKYO), nút giữa thanh dưới (Visit Vietnam), hoặc chính hero (Layla). Visit Wales và GO TOKYO đều **nói rõ giới hạn của AI** (BETA, "có thể sai", "không nhập thông tin cá nhân", trả lời từ nội dung của chính cổng).

**15 mẫu nên học** (chi tiết + dữ liệu cần ở `tong_hop.md` §3):
1. Nút trợ lý nổi mọi trang.
2. Thanh dưới trên điện thoại.
3. Hero là ô hỏi trợ lý.
4. Chip gợi ý câu hỏi.
5. Ô khám phá theo 5 mảng kho.
6. Trang danh sách một khuôn.
7. Thẻ chỉ hiện trường có nguồn.
8. Trang chi tiết từ file kho.
9. "Hỏi trợ lý về điểm này" [Đề xuất, TRIPO không có].
10. Báo thông tin sai.
11. Bản đồ có lớp lọc.
12. Lịch sự kiện theo tháng.
13. Trang giới thiệu trợ lý + giới hạn.
14. Lên lịch bằng chip ⇒ lịch theo buổi.
15. Thời tiết nhỏ trên header.

Dữ liệu: 1–5, 8, 9, 13, 14, 15 dùng được với cái hệ thống đã có. 6, 7, 10, 11, 12 có một phần. **Ảnh được phép dùng: chưa có.**

**Không nên chép:** nhận diện cổng nhà nước (logo, tên, mascot, màu + bố cục y hệt), đăng nhập, đặt chỗ / gọi / chia sẻ, sao đánh giá, "gần bạn", danh mục nghìn cơ sở, ảnh / video của cổng khác, tile Google Maps.

Tiền: 0 USD.

## 5. Lỗi và giới hạn

1. Mỗi trang một lần chụp tối 06/11 — khối động (băng chuyền, sự kiện) có thể khác lúc khác.
2. Phương tiện / tour / sự kiện: chỉ lấy được trang danh sách con, chưa có trang chi tiết thật (link đầu tiên script tìm thấy là danh sách con).
3. Số đo tự động có chỗ sai: "header" ở GO TOKYO / Layla ra chiều cao cả trang (không có thẻ `<header>` rõ); màu đếm theo số phần tử, không theo diện tích.
4. Không thử hội thoại trợ lý của trang nào; chưa đánh giá chất lượng trả lời.
5. Visit Wales lúc chụp hiện lớp chặn bot trên hero + bảng cookie lớn (B không bấm chấp nhận) ⇒ ảnh màn đầu bị che.
6. Mindtrip / Traveley / Adtona chỉ theo báo cáo Codex, B chưa chụp / kiểm.
7. Số đếm kho (địa chỉ 86, giờ 14, giá 12 file…) là số file có chữ khớp mẫu, không phải số trường đủ dữ liệu — C209 đếm kỹ.
8. Ảnh 219 MB ở `data/` (private) — xoá bớt khi xong spec nếu cần chỗ.

## 6. Bàn giao cho người kiểm

- A đọc `data/nghien_cuu_giao_dien_2026-11-06/tong_hop.md` (§3 bảng 15 mẫu, §4 không nên chép) để viết spec đợt 1.
- Ảnh xem nhanh: `anh/tripo_nho/`, `anh/khac_nho/ghep_*.jpg`.
- Chạy lại: các lệnh mục 3 (0 USD, mỗi lần một trình duyệt).

**Giải thích ngắn:** B xem kỹ cổng Huế TRIPO và 5 cổng / ứng dụng du lịch có AI khác. Từ đó rút ra 15 cách trình bày nên học cho chatbot Huế, ví dụ:
- nút trợ lý nổi ở mọi trang;
- thanh điều hướng dưới trên điện thoại;
- trang danh sách và trang chi tiết dựng thẳng từ kho;
- nói rõ giới hạn của AI.

Cũng có 10 thứ không nên làm theo vì hue_rag không có dữ liệu, hoặc vì dễ bị nhầm là trang của nhà nước.
