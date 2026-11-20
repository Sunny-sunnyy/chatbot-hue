# Plan một trang — mục [4] trang "Bản đồ" riêng trong menu (E viết 15:41 20/11/2026, giờ `date`; chờ phiên điều phối duyệt; chưa viết code)

**Từ dùng:** *bảng điểm* = 41 điểm tham quan mà trang Lên kế hoạch dùng để xếp lịch · *bảng toạ độ* = vị trí của các điểm đó (file riêng tư, khoá `lich_trinh_toa_do` trong `backend/config/settings.yaml`; server đã nạp sẵn khi cờ `ban_do_lich` bật) · *ghim* = dấu tròn trên bản đồ.

**1. Điều chủ dự án đã chốt — và chỗ CHƯA đủ rõ**
- Nguồn duy nhất: `session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-06.md` dòng 15 — cổng mức 2, menu "Trang chủ · Trợ lý AI · Khám phá · **Bản đồ**", trong ngoặc có chữ "bản đồ". Không có spec đợt 2 nào (`ls docs/superpowers/specs`).
- KHÔNG có chữ nào nói: trang hiện NHỮNG nơi nào (chỉ điểm tham quan, hay cả quán / chỗ ở) · bấm vào một nơi thì làm được gì · có lọc không. Mặc định E đề nghị ở mục 2 — phiên điều phối quyết, không hỏi chủ dự án.

**2. Người dùng thấy gì (mặc định đề nghị — bản nhỏ nhất đúng chữ "trang Bản đồ")**
- Menu có thêm "Bản đồ" (sau "Khám phá"), địa chỉ `#/ban-do`; cờ `ban_do_lich` tắt ⇒ không có mục menu, gõ thẳng địa chỉ ⇒ về trang chủ như mọi địa chỉ lạ.
- Một bản đồ Huế có ghim của MỌI điểm trong bảng điểm có toạ độ (hiện 41 điểm; đếm lại khi code), hàng nút lọc theo loại có sẵn trong bảng (Di tích 19 · Thiên nhiên 10 · Chụp ảnh 9 · Ẩm thực 7 · Lễ hội, nghệ thuật 6 — một điểm có thể thuộc hai loại).
- Bấm ghim ⇒ ô nhỏ: tên điểm, loại, link "Mở Google Maps" (cùng link trang lịch đang dùng). Dưới bản đồ: danh sách tên theo loại đang lọc (đọc được khi ô bản đồ không tải, và cho người dùng bàn phím).
- KHÔNG làm ở bản này: quán ăn / chỗ ở trên bản đồ · nút "thêm vào lịch" · vị trí người dùng · đường đi · tìm kiếm · link sang bài Khám phá (bảng điểm không có mã bài chắc chắn cho từng điểm — chưa kiểm).

**3. Dùng lại gì, thêm gì** (KHÔNG thêm nguồn dữ liệu, không thư viện mới, model không tham gia)
- Dùng lại: Leaflet + nguồn ô bản đồ + dòng ghi công bản đồ của `frontend/src/BanDoLich.jsx` (tách phần dựng khung bản đồ thành hàm chung để hai nơi cùng dùng — nếu tách làm đổi hành vi bản đồ lịch thì KHÔNG tách, chép ~15 dòng) · `toaDo.js` · `nguonBanDo.js` · lớp CSS `.bd-khung`, `.ghim` · `lich_trinh.map_url` · điều hướng `route.js` · menu `App.jsx`.
- Thêm: một đường `GET /api/ban_do` trong `backend/api/routes/cong.py` (dựng một lần, trả `[{ten, loai, toa_do, map_url}]` từ bảng điểm + bảng toạ độ đã nạp; cờ tắt ⇒ 404 như `/api/cho_o`) · `frontend/src/TrangBanDo.jsx` (tải riêng như bản đồ lịch ⇒ trang khác không tải Leaflet) · một dòng `route.js`, một dòng menu.
- Ước: backend ~20 dòng + test ~15 · frontend ~90 dòng + ~10 dòng CSS. Dựng lại `frontend/dist` ở cây chính sau khi gộp.

**4. Xong khi (ghi trước)**
- a. `GET /api/ban_do`: số mục = số điểm bảng điểm có toạ độ; mọi toạ độ trong khung Huế; cờ tắt ⇒ 404 (test trong `backend/tests/test_cong_dot_1.py` hoặc file test cổng đang có, đỏ trước xanh sau).
- b. Trình duyệt thật, rộng 1440 và 390: vào `#/ban-do` từ menu ⇒ số ghim = số mục API; bấm lọc "Ẩm thực" ⇒ số ghim = số điểm loại đó; bấm một ghim ⇒ thấy tên + link; trang không tràn ngang ở 390; 0 lỗi trang. Ảnh chụp hai bề rộng, E MỞ ảnh ra nhìn.
- c. Bản đồ trong thẻ lịch không đổi: test hiện có của bản đồ lịch đạt + một lượt nhìn thẻ lịch trên trình duyệt (cùng lượt b).
- d. Trang Trợ lý / Trang chủ không tải thêm file Leaflet (so danh sách file mạng trước ↔ sau ở trang chủ).

**5. Giới hạn biết trước**
- Bản đồ cần mạng tới máy chủ ô bản đồ (như bản đồ lịch); mất mạng ⇒ chỉ còn danh sách. Chỉ 41 điểm tham quan — người tìm quán ăn / khách sạn trên bản đồ sẽ không thấy. Lượt trình duyệt cần bật server (0 USD model, chờ lượt chung).

**6. Kết quả phần code (E ghi 15:49 20/11/2026, giờ `date`; CHƯA có lượt trình duyệt nào — tiêu chí b, c, d chờ lượt bật server; chưa ai review)**
- Phiên điều phối duyệt plan với ba mặc định: chỉ điểm tham quan của bảng điểm · mục menu sau "Khám phá" · được dùng chung phần bản đồ nếu bản đồ lịch không đổi.
- Đã viết: `GET /api/ban_do` + hàm thuần `dung_ban_do` (`backend/api/routes/cong.py` +24) · `frontend/src/TrangBanDo.jsx` (mới, 78 dòng) · `route.js` (`#/ban-do`) · `App.jsx` (mục menu "Bản đồ" chỉ khi cờ `ban_do_lich` bật; trang tải riêng) · `index.css` +4 · `BanDoLich.jsx`: CHỈ thêm chữ `export` cho hàm dòng ghi công bản đồ (không tách gì khác ⇒ bản đồ trong thẻ lịch không đổi một dòng lệnh nào).
- a. [máy kiểm] test mới `test_map_page_lists_every_itinerary_point_that_has_coordinates`: ĐỎ trên code cũ (`AttributeError`), xanh sau; cả file `test_ban_do_lich.py` 14 đạt (Python 3.13). Dữ liệu thật của bộ cờ đang chạy: xem dòng số điểm ở tin báo phiên điều phối.
- [máy kiểm] `npm run build` trong worktree đạt; trang Bản đồ thành file riêng `TrangBanDo-*.js` 2,9 kB, dùng chung file Leaflet `BanDoLich-*.js` với bản đồ lịch.
- CHƯA làm: b (số ghim, lọc, bấm ghim, tràn ngang ở 390 px, ảnh) · c (nhìn lại bản đồ trong thẻ lịch) · d (trang chủ không tải Leaflet) · dựng lại `frontend/dist` ở cây chính sau khi gộp · `bai_hoc/`.

**7. Kết quả lượt trình duyệt + review (E ghi 16:06 20/11/2026, giờ `date`; server riêng của E cổng 8018 chạy từ đúng nhánh này, trình duyệt không màn hình, E đã MỞ ảnh ra nhìn)**
- Review: phiên B đọc cả nhánh `7e1c300` + gọi `dung_ban_do` trên dữ liệu thật: READY (40 mục, mỗi mục đúng bốn trường, không lọt trường nào của bảng riêng tư, 0 toạ độ ngoài khung Huế) [người thứ hai kiểm].
- b. [máy kiểm + E nhìn ảnh] Rộng 1440 và 390: vào từ menu ("Bản đồ" đứng sau "Khám phá") ⇒ `#/ban-do`, **40 ghim = 40 mục API = 40 dòng danh sách**; lọc "Ẩm thực" ⇒ **7 ghim, 7 dòng**; bấm một ghim ⇒ ô "Chợ Đông Ba · Ẩm thực · Mở Google Maps" (link Google Maps theo tên); tràn ngang 0 px ở cả hai bề rộng; 0 lỗi trang; ô bản đồ tải được.
- c. [máy kiểm + E nhìn ảnh] Một lịch thật lập trên nhánh này: bản đồ trong thẻ lịch vẫn có nút "Ngày 1 / Ngày 2", 3 ghim đánh số 1–2–3 và danh sách — như trước.
- d. [máy kiểm] Trang chủ không tải file bản đồ nào (danh sách file mạng lọc theo tên file bản đồ / Leaflet / máy chủ ô: rỗng, cả hai bề rộng).
- Lỗi E thấy khi nhìn ảnh và đã sửa trong nhánh (một dòng CSS): danh sách tên ở màn rộng xếp MỘT cột dài vì luật chia cột bị luật cũ đứng sau đè ⇒ đổi bộ chọn; dựng lại, chạy lại cả hai bề rộng vẫn đạt.
- Giới hạn / điều cần người quyết: (1) "Không gian lưu niệm Lê Bá Đảng" có trong bảng điểm nhưng không có toạ độ ⇒ không lên trang (lịch vẫn có thể xếp điểm này); (2) điện thoại: thanh dưới nay có SÁU mục, chữ bốn mục xuống hai dòng (đọc được, không bị cắt) và nút tròn "Trợ lý Huế" KHÔNG còn nằm giữa (hai mục bên trái, ba mục bên phải) — ảnh `ban_do_390_0_trang_chu.png`; (3) trang dùng lại dòng ghi nguồn bản đồ "© OpenStreetMap…" như bản đồ lịch đang có; (4) ghim không tự tách khi chồng nhau ở mức phóng xa (cụm trung tâm) — phóng to thì tách; (5) kết quả + ảnh (riêng tư): `data/test_cuoi/chay_2026-11-20_chieu/ban_do*.json`, `ban_do_*.png`; ảnh lần chạy đầu bị lần chạy lại ghi đè cùng tên (file JSON thì không).
- CHƯA làm: dựng lại `frontend/dist` ở cây chính sau khi gộp · `bai_hoc/` · điện thoại thật.
