# Huế TRIPO vòng 7 — lấy mẫu GIAO DIỆN để so với hue_rag · B, 10:54 14/11/2026

A giao (User 14/11: "Lên kế hoạch của mình đơn giản quá, không nổi bật / sinh động; ít nhất phải được như TRIPO").

**Cách làm:**
- Playwright, trang công khai, `permissions=[]`. Không đăng nhập, không đặt chỗ / thanh toán, không gửi thông tin cá nhân. 0 USD.
- Script: `data/tripo_v7_2026-11-14/tools/chup.py`. Mỗi trang chụp 1440 + 390, cuộn hết trang cho ảnh lười tải hiện ra, rồi lưu ảnh toàn trang + HTML.
- Dò tay trước: trang chủ 1440 + 390, đọc ảnh rồi mới chụp tiếp.

**Dùng lại v6 (12–13/11), không chạy lại:**
- luồng lập kế hoạch đủ bước tới lịch ra (`data/tripo_v6_2026-11-12/k1_…`, `k2_…`, khổ 1366);
- 7 trang danh mục + chi tiết, bản đồ, tab Lưu trú / Ăn uống / Dịch vụ, tiếng Anh (`tinh_nang/`).

Đổi từ 12/11: thứ tự khối trang chủ và biểu mẫu "Lên kế hoạch" **giống v6** (so ảnh); sự kiện trên trang chủ đã đổi theo ngày.

**Chưa làm:**
- luồng lập kế hoạch ở khổ 390 (cần ~2–3 phút / lượt chờ tạo phương án; script v6 cố định khổ 1366) ⇒ phần "lịch ra" ở điện thoại chưa có ảnh;
- ảnh lịch v6 chỉ chụp khung nhìn, không toàn trang.

## 1. Mỗi trang — cái gì làm nó "sinh động"

| Trang | Bố cục / khối nổi bật | Ảnh · bản đồ · thẻ | Tương tác · chuyển động |
|---|---|---|---|
| Trang chủ (`01_trang_chu_1440 / _390`) | ảnh nền to cả bề ngang (sông về đêm) + tiêu đề chữ có chân + ô tìm bo tròn ở giữa ⇒ 2 thẻ đôi "lên kế hoạch chưa?" (có linh vật robot) + "hỏi gợi ý về: ở đâu / ăn gì / mua gì / chơi đâu" (4 biểu tượng màu) ⇒ "Khám phá nhanh": 8 ô màu nhạt, mỗi ô một biểu tượng + hình mờ lớn bên phải ⇒ "Điểm tham quan" lưới 4 thẻ ⇒ "Sự kiện nổi bật" băng chuyền thẻ ảnh lớn ⇒ "Tour" lưới 4 thẻ ⇒ chân trang | thẻ điểm: ảnh 4:3 phủ kín đầu thẻ, sao điểm + số lượt đánh giá, giờ mở cửa + địa chỉ có biểu tượng, giá màu tím đậm, nút "Xem chi tiết" viền | băng chuyền sự kiện có **đồng hồ đếm ngược** (ngày · giờ · phút · giây) và nút ‹ ›; nút lọc "Nổi bật / Gần bạn / Được yêu thích"; linh vật nổi góc phải mọi trang; nền xen kẽ trắng / tím rất nhạt theo khối |
| Trợ lý AI — Lên kế hoạch (`02_tro_ly_1440`) | thanh chuyển 4 tab dạng viên thuốc (Lên kế hoạch · Lưu trú · Ăn uống · Dịch vụ) ⇒ một thẻ trắng lớn chứa cả biểu mẫu: 3 ô "kiểu đi" có biểu tượng + dòng giải thích ⇒ các nhóm chip bo tròn ⇒ hàng số đếm − n + (người lớn, trẻ em, số ngày) + ô ngày ⇒ 3 nút ngân sách ⇒ "Tùy chọn thêm" ⇒ ô chat cố định ở đáy | nền có hình vẽ chìm cầu / thành (ảnh nền nhạt) | chọn chip đổi màu ngay; sau "Gửi": bong bóng tím của người dùng + thẻ tóm tắt lựa chọn (khung xanh nhạt) + thẻ hỏi thêm có chip |
| Kết quả lịch (v6 `08_sau_xac_nhan_lich`) | hai cột: trái là lời chat tóm tắt theo buổi, phải là lịch. Thanh đầu trang: tiêu đề + ngày giờ bắt đầu + số người + **tổng tiền dự kiến**, cùng nút sửa / tải / chia sẻ / về nhà + nhiệt độ. Có tab "Tổng quan · Ngày 1…", tóm tắt chuỗi điểm nối bằng mũi tên | **dòng thời gian dọc**: mỗi chặng một chấm biểu tượng theo loại (ở · ăn · tham quan) + **viên giờ** "08:00 – 08:20" màu xanh; thẻ chặng có ảnh vuông bên trái, tên + sao, địa chỉ, khoảng giá, chi phí dự kiến; giữa hai chặng là dòng "ô tô 5 phút · 0,2 km" | mỗi chặng có Xem chi tiết · Bản đồ · Chỉ đường · Thay đổi địa điểm; nút "Xem bản đồ Ngày 1"; kéo thả sắp lại (biểu tượng ⋮⋮); xoá chặng (×) |
| Danh sách điểm (`03_diem_tham_quan_1440 / _390`) | ảnh băng ngang có tiêu đề + ô tìm ⇒ hàng chip loại (Di tích · Văn hoá · Tâm linh…) ⇒ "Bộ lọc (419)" ⇒ lưới 4 cột | thẻ như trang chủ + **nhãn loại** dán góc trên ảnh ("Di tích", "Thiên nhiên") | "Xem thêm" tải tiếp |
| Chi tiết điểm (`06_chi_tiet_dai_noi_1440 / _390`) | đường dẫn ⇒ tên + địa chỉ + hàng nút tròn (quay lại, báo, link, gọi, chia sẻ) + "Đặt vé" ⇒ **khảm ảnh** 1 lớn + 4 nhỏ ("+24") ⇒ hai cột: trái Tóm tắt · Nội dung chi tiết (có "Đọc thêm") · Giá vé (bảng) · Video · Âm thanh thuyết minh · Đánh giá; phải: thẻ thông tin (loại, giờ, giá, điện thoại), tiện ích, bản đồ nhỏ, "báo thông tin sai" ⇒ "Địa điểm khác" 4 thẻ | khảm ảnh, bảng giá có nút | trình phát âm thanh thuyết minh, lọc đánh giá |
| Bản đồ (`04_ban_do`), Sự kiện (`05_su_kien`) | bản đồ toàn màn + lớp; sự kiện lưới thẻ ảnh lớn | — | — |

**Tóm lại (quan sát):** cảm giác "sinh động" đến từ 5 thứ, không phải từ chuyển động:
1. ảnh thật ở mọi thẻ và mọi chặng;
2. biểu tượng màu cho từng loại;
3. "viên" (pill) cho giờ / nhãn / tab;
4. nền xen kẽ theo khối + hình vẽ chìm;
5. con số nổi bật (sao, giá, tổng tiền, đếm ngược).

Chuyển động thật chỉ có ở băng chuyền + đổi màu khi chọn.

## 2. TRIPO có ↔ hue_rag có / thiếu (5 trang của mình)

| Trang của mình | TRIPO có | Mình hiện có | Thiếu — **GIAO DIỆN** (làm được ở đợt giao diện, không cần backend) | Thiếu — **TÍNH NĂNG** (cần backend / dữ liệu) |
|---|---|---|---|---|
| Trang chủ | ảnh nền to, ô tìm giữa, 8 ô khám phá có biểu tượng, lưới thẻ ảnh, băng chuyền sự kiện | ô hỏi, chip gợi ý, thời tiết, 5 lĩnh vực (chữ), dải sông | ảnh nền to (đã có ảnh Commons sạch giấy phép) · ô lĩnh vực có biểu tượng SVG + màu nhạt · thẻ điểm có ảnh (24 ảnh của C) · thẻ "Lên kế hoạch" nổi bật có hình · nền xen kẽ khối | thẻ sự kiện có ngày thật + đếm ngược (cần bảng sự kiện có ngày) · sao / lượt đánh giá (không có dữ liệu, không nên bịa) · giá vé trên thẻ (kho có một phần, phải kèm "kiểm lại") |
| Lên kế hoạch — biểu mẫu | thẻ trắng lớn, 3 ô kiểu đi có biểu tượng + câu giải thích, chip bo tròn, số đếm − + | form.lc 4 nhóm, nút, số đếm | ô "kiểu đi" thành 3 thẻ có biểu tượng + một dòng giải thích · chip bo tròn đổi màu khi chọn · ảnh nền chìm · thanh tab trên cùng | ngân sách (cần dữ liệu giá; đợt 3) |
| Lên kế hoạch — lịch ra | dòng thời gian dọc, biểu tượng loại, viên giờ, ảnh vuông mỗi chặng, phút + km giữa chặng, tab ngày, thanh đầu có tổng hợp, tóm tắt chuỗi điểm | thẻ .lich-v2: dòng "Mình hiểu", ngày → buổi · giờ → tên → câu, ghi chú, nguồn, Sao chép / Tải / Sửa; bản đồ (cờ tắt) | **dòng thời gian dọc + chấm biểu tượng theo buổi + viên giờ** · ảnh điểm mỗi mục (B1: 24 / 34 điểm đã có ảnh) · tab / neo "Ngày 1 · 2 · 3" · thanh đầu lịch (số ngày · số người · ngày đi · thời tiết) · tóm tắt chuỗi điểm mỗi ngày bằng mũi tên · dòng "đi X phút" giữa hai điểm (code đã có phút đi trong bảng — chỉ cần đưa ra) | Thay đổi địa điểm / xoá / kéo thả từng mục (cần API sửa lịch) · chi phí dự kiến (đợt 3 / dữ liệu giá) · quán ăn + nơi ở trong lịch (đợt 3: OSM + "khu + link") · bản đồ (có sẵn, đang chờ DNS host tile để kiểm) |
| Trợ lý (chat) | bong bóng tím người dùng, thẻ tóm tắt lựa chọn, thẻ hỏi thêm có chip, linh vật | chữ hiện dần, bước tiến độ, thẻ hỏi lại, nguồn [n], mục web riêng | bong bóng người dùng có màu · thẻ tóm tắt lựa chọn dạng khung · biểu tượng cho bước tiến độ | — (phần chat của mình đã có nhiều thứ TRIPO không có: nguồn, từ chối đúng, mục web tách) |
| Khám phá / bài | danh sách có ảnh băng ngang, chip loại, lưới thẻ ảnh + nhãn loại; chi tiết có khảm ảnh, thẻ thông tin bên phải, "địa điểm khác" | danh sách bài theo lĩnh vực (chữ), trang bài đọc Markdown, báo sai | thẻ bài có ảnh + nhãn lĩnh vực (ảnh chỉ có cho điểm trong bảng ảnh) · trang bài hai cột: nội dung trái, thẻ "thông tin nhanh" phải (giờ / giá / địa chỉ lấy từ mục "Thông tin chung" của bài) · "bài liên quan" cuối trang | khảm nhiều ảnh / video / thuyết minh âm thanh (không có dữ liệu) |
| Giới thiệu | (TRIPO không có trang riêng) | 1 cột chữ | như bàn nhóm vòng 1 (dải ảnh, thẻ tính năng, 3 bước, giới hạn) | — |

**Không nên chép:**
- sao / lượt đánh giá, "đặt bàn / đặt vé", giá không nguồn: mình không có dữ liệu thật ⇒ bịa là phạm "nói chắc sai";
- linh vật robot: tốn công, ít giá trị;
- v6 đếm được lỗi giờ trong lịch TRIPO (`b_tripo_v6_lap_ke_hoach.md` §2) ⇒ chỉ học phần **trình bày**, không học luật xếp.

## 3. Ảnh tiêu biểu đưa User (≤ 12) — trong `data/` (private)
1. `data/tripo_v7_2026-11-14/01_trang_chu_1440.png` — trang chủ đủ khối
2. `data/tripo_v7_2026-11-14/01_trang_chu_390.png` — trang chủ điện thoại
3. `data/tripo_v7_2026-11-14/02_tro_ly_1440.png` — biểu mẫu lên kế hoạch
4. `data/tripo_v7_2026-11-14/02_tro_ly_390.png` — biểu mẫu ở điện thoại
5. `data/tripo_v6_2026-11-12/k1_1ngay_canbang_vanhoa_capdoi_tb/03_sau_bo_qua.png` — thẻ tóm tắt + hỏi thêm
6. `data/tripo_v6_2026-11-12/k1_1ngay_canbang_vanhoa_capdoi_tb/08_sau_xac_nhan_lich.png` — **lịch dòng thời gian** (mẫu chính cho trang của mình)
7. `data/tripo_v6_2026-11-12/k1_1ngay_canbang_vanhoa_capdoi_tb/09_ban_do_ngay_1.png` — bản đồ ngày
8. `data/tripo_v7_2026-11-14/03_diem_tham_quan_1440.png` — lưới thẻ có nhãn loại
9. `data/tripo_v7_2026-11-14/06_chi_tiet_dai_noi_1440.png` — chi tiết hai cột + khảm ảnh
10. `data/tripo_v7_2026-11-14/05_su_kien_1440.png` — thẻ sự kiện ảnh lớn
11. `data/len_ke_hoach_v2_2026-11-13/nghiem_thu/pw_1411/nghiem_thu_1440.png` — lịch của mình hôm nay (để đặt cạnh số 6)
12. `data/len_ke_hoach_v2_2026-11-13/nghiem_thu/pw_1411/nghiem_thu_390.png` — lịch của mình ở điện thoại

**Đề xuất ưu tiên cho đợt giao diện:** trang Lên kế hoạch.
- Dòng thời gian dọc + ảnh mỗi mục + viên giờ + dòng phút đi + thanh đầu lịch: tất cả dữ liệu đã có trong `lich` / bảng ⇒ 0 backend, trừ "phút đi" cần thêm một trường nhỏ.
- Trang chủ đứng thứ hai.

## 4. Hiệu ứng / chuyển động TRIPO dùng — đo bằng trình duyệt thật (`data/tripo_v7_2026-11-14/tools/hieu_ung.py`, 0 USD)

| Loại | Có gì (đo được) | Ghi chú |
|---|---|---|
| Di chuột lên thẻ điểm | thẻ **nhấc lên 4 px** + bóng đổ mềm (`0 12px 32px rgba(0,0,0,.08)`), **ảnh trong thẻ phóng 1,03**; chuyển trong **0,2 s**, đường cong `cubic-bezier(0.16, 1, 0.3, 1)` (ra nhanh, dừng êm) | hiệu ứng "sinh động" rõ nhất, rất rẻ (CSS) |
| Tin nhắn chat | mỗi dòng tin **mờ dần + trượt vào** (`chatMsgFadeIn`, 0,3 s); **ba chấm "đang gõ"** nhấp nháy; khung chat nổi `slideInRight` | |
| Lúc chờ tải | **khung xương lấp lánh** (skeleton / `placeholder-glow`, `placeholder-wave` của Bootstrap) thay cho chữ "Đang tải" | |
| Băng chuyền | sự kiện nổi bật trượt ngang có nút ‹ ›, đồng hồ đếm ngược chạy từng giây | |
| Khi cuộn | **không** có hiệu ứng hiện dần khi cuộn (0 lớp đổi khi cuộn hết trang; 0 phần tử `data-aos` / `animate__`) | |
| Chuyển trang | **tải lại cả trang** (không có chuyển cảnh mượt giữa trang) | |
| Video / ảnh động / Lottie | 0 trên trang chủ | |
| Tổng | 133 quy tắc CSS có `transition` (phần lớn của Bootstrap), 32 có `animation`; có tắt theo `prefers-reduced-motion` (của Bootstrap) | |

**Kết luận đo được:** TRIPO "sinh động" chủ yếu nhờ ảnh + màu + biểu tượng (§1). Chuyển động chỉ là ba thứ nhỏ:
1. thẻ nhấc lên khi di chuột;
2. tin chat hiện dần + ba chấm "đang gõ";
3. khung xương lấp lánh lúc chờ.

Không có hiệu ứng khi cuộn, không có chuyển cảnh giữa trang ⇒ thêm hai thứ này là mình **hơn** TRIPO, không phải để bắt kịp.
