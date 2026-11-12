# Huế TRIPO vòng 6 — chạy thật luồng "Lên kế hoạch chuyến đi" + mọi tính năng công khai · **DỞ (kết phiên 12/11)**

Người làm: B (Claude Code, `hue-rag-1b`) · viết 22:23 12/11/2026 (`date`) · A giao theo yêu cầu của User ("chạy đầy đủ tính năng, lưu lại như tôi").
Cách làm: Playwright (Chromium không màn hình, không cấp quyền vị trí / micro), trang công khai `huetripo.hue.gov.vn`; **không** đăng nhập, đặt chỗ, thanh toán, gửi thông tin cá nhân.
Kết quả lưu (private, không commit): `data/tripo_v6_2026-11-12/<cấu hình>/` — mỗi bước một ảnh chụp toàn trang + HTML + file chữ; `ket_qua.json` ghi giờ từng bước. Tiền: TRIPO 0 USD; phía hue_rag ≈ 0,003 USD (ước, 6 lượt biểu mẫu).

## 0. Chưa làm được / chưa làm — đọc trước

| Phần | Trạng thái | Vì sao |
|---|---|---|
| Luồng lập kế hoạch, cấu hình 1 (1 ngày, cân bằng, văn hoá, cặp đôi, trung bình) | **XONG đủ luồng — 13 bước** | — |
| Cấu hình 2 (2 ngày, nhẹ nhàng, sinh thái, gia đình có trẻ em, tiết kiệm) | **XONG — 10 bước** (không thử "Bổ sung yêu cầu" / "Thay đổi địa điểm") | — |
| Cấu hình 3, 4, 5, 6 (các cấu hình có điền "Tùy chọn thêm") | **HỎNG DO SCRIPT CỦA B — phải chạy lại** | Khi đã điền "Tùy chọn thêm", trang **không hỏi thêm** (không có nút "Bỏ qua & Xem gợi ý") mà tạo phương án luôn (~70–85 giây). Script chỉ chờ ~10 giây, không thấy nút xác nhận, rồi bấm nhầm mục "Bản đồ" trên thanh menu. **Đây không phải lỗi của TRIPO.** Chỉ dùng được bước 01 (biểu mẫu đã điền) và 02 (bảng tóm tắt yêu cầu) |
| Trang chủ, tab Lưu trú / Ăn uống / Dịch vụ, chat tự do, Khám phá, Bản đồ, đổi ngôn ngữ, mục chân trang | **CHƯA CHẠY ở vòng 6** | hết phiên (vòng 5 có chạy một phần: `b_tripo_v5.md`) |
| "Thay đổi địa điểm" ở chặng 1 | mới bấm mở + chụp (cấu hình 1); **chưa đọc** nội dung hộp chọn, chưa chọn điểm thay | hết phiên |
| Nhập bằng giọng nói | không thử được | trình duyệt tự động không có micro — chỉ ghi nhận có nút |
| Bảng so từng tính năng với hue_rag + đề xuất học / bỏ qua | **CHƯA VIẾT** | cần đủ 6 cấu hình + các tính năng khác |

## 1. Luồng lập kế hoạch — từng bước (đã chạy thật ở cấu hình 1; giờ lấy từ `ket_qua.json`)

| # | Bước | Trang làm gì | Thời gian chờ đo được |
|---|---|---|---|
| 1 | Biểu mẫu | 4 nhóm bắt buộc (kiểu đi · loại hình · đi cùng ai · ngân sách) + số người lớn / trẻ em / số ngày bằng nút + / − + ngày giờ khởi hành + "Tùy chọn thêm" (ẩm thực, hoạt động, tôn giáo, yêu cầu khác). Các nhóm nút **tải chậm** ("Đang tải dữ liệu…", 3–11 giây) | 3,4–11 giây mới bấm được |
| 2 | Gửi | Trang tự ghép lựa chọn thành **một câu chữ** rồi gửi như tin nhắn chat; trả bảng tóm tắt yêu cầu + hỏi thêm (nút "Bỏ qua & Xem gợi ý") nếu chưa điền tuỳ chọn | ~14–16 giây |
| 3 | 3 phương án | Mỗi phương án: 1 nơi ở · 2–3 quán · 4 điểm tham quan · 1 mục "đi chơi tối"; có dòng báo "khi tạo lịch, một số điểm có thể bị thay / bỏ" | **~70–86 giây** |
| 4 | "Bổ sung yêu cầu" | Mở lại bảng tuỳ chọn; chọn thêm rồi "Lưu bổ sung" ⇒ tạo lại 3 phương án | ~78 giây |
| 5 | "Xem theo từng buổi" | Mở danh sách quán theo sáng / trưa / tối trong từng phương án | tức thì |
| 6 | "Xác nhận phương án n" | Lịch chi tiết: từng chặng có giờ bắt đầu – kết thúc, tên, điểm đánh giá + số lượt, địa chỉ, giờ hoạt động, khoảng giá, chi phí dự kiến, phút + km tới chặng sau; tổng tiền cả chuyến; nhiệt độ | 1,3–4,1 giây |
| 7 | "Xem bản đồ Ngày n" · "Bản đồ" / "Chỉ đường" / "Xem chi tiết" (mở thẻ mới) / "Thuyết minh" / "Đặt bàn ngay" / "Thay đổi địa điểm" ở từng chặng | đã bấm bản đồ ngày, bản đồ chặng 1, chi tiết chặng 1, thay đổi địa điểm chặng 1 | vài giây |

## 2. Lỗi đếm bằng code trên lịch chi tiết (2 / 6 cấu hình — `tools/rut_lich.py`, kết quả ở `<cấu hình>/lich_rut.json`)

| Loại lỗi | Cấu hình 1 (8 chặng, 2.950.000 đ) | Cấu hình 2 (14 chặng, 2.800.000 đ) |
|---|---|---|
| Kết thúc sau giờ đóng cửa | **1** — một lăng xếp 16:26–17:41, giờ hoạt động ghi tới 17:30 | 0 (các điểm sinh thái không ghi giờ hoạt động ⇒ code không kiểm được) |
| Giờ vô lý | 2 chặng đầu chồng nhau (ở khách sạn 08:00–08:20, ăn sáng bắt đầu 08:05) | **2** — mục "tham quan và dùng bữa" kéo từ ~17:00 tới **sau nửa đêm** (17:01–00:38; 16:37–00:14), rồi "về khách sạn 23:59" — lịch cho gia đình có trẻ em |
| Thiếu giờ đi | 0 | 1 — cần 45 phút, lịch chừa 22 |
| Phút đi quá lạc quan (> 45 km/giờ) | 0 | 2 chặng về khách sạn (28 km / 34 phút; 38 km / 45 phút) |
| Bữa ăn không có quán | 0 (3 quán có tên, có nút đặt bàn) | 4 bữa chỉ ghi "ăn sáng tại địa phương" / "ăn trưa quanh điểm tham quan" |
| Lựa chọn không đổi lịch | Bổ sung "Trải nghiệm buổi tối": phương án 1 và 2 **giống hệt** trước khi bổ sung (phương án 3 đổi 1 điểm); lịch cuối **không có** hoạt động buổi tối nào (mục "đi chơi tối" của phương án bị bỏ) | chưa thử |
| Đi xa với trẻ em | — | ngày 2 đi 21 + 16 + 23 + 38 km giữa các chặng; kiểu đi đã chọn là "nhẹ nhàng" |

Điều TRIPO làm được mà hue_rag hôm nay chưa có (quan sát ở 2 cấu hình): giờ từng chặng · phút + km giữa các chặng · chi phí từng chặng + tổng · nơi ở · quán ăn có tên + giờ hoạt động · điểm đánh giá · 3 phương án để chọn · đổi điểm ở từng chặng · bản đồ theo ngày.

## 3. Phía hue_rag — cùng 6 cấu hình qua biểu mẫu đang chạy (server của User, `/api/chat`, cờ như `main`)

Đã chạy đủ **6 / 6** (22:23 12/11/2026): cả 6 trả lịch (HTTP 200), thời gian 6,5 · 7,0 · 15,4 · 10,5 · 7,4 · 13,9 giây (TRIPO: ~90–100 giây từ lúc gửi tới lịch chi tiết). Phản hồi nguyên văn: `data/tripo_v6_2026-11-12/hue_rag/k1…k6.json` — **chưa đọc / chưa so nội dung** (việc phiên sau).
Ô TRIPO có mà biểu mẫu hue_rag hôm nay **không điền được** (ghi trong từng file, khoá `khong_dien_duoc`): ngân sách · số người · ngày đi · kiểu đi "cân bằng" · vừa trẻ em vừa người lớn tuổi · mọi "tùy chọn thêm" (ẩm thực, tôn giáo, yên tĩnh, ít đi bộ, buổi tối). Bốn ô đầu nằm trong spec "Lên kế hoạch" bản 3.3 đợt 1 (trừ ngân sách).

## 4. Việc phiên sau (theo thứ tự)

1. Sửa `tools/lap_ke_hoach.py`: sau khi gửi, **chờ tới khi có nút "Xác nhận phương án"** (tới 150 giây) dù có hay không nút "Bỏ qua"; không bấm nút "Bản đồ" khi chưa ở trang lịch. Chuyển 4 thư mục k3–k6 hiện có thành `_hong_*` rồi chạy lại.
2. Chạy các tính năng còn lại (bảng mục 0), mỗi tính năng lưu ảnh + HTML từng bước.
3. Đọc + so nội dung lịch hue_rag ↔ TRIPO; viết bảng kiểm kê đủ tính năng + đề xuất học / bỏ qua; báo A + C.

**Giải thích ngắn:** mới chạy trọn luồng lập kế hoạch của trang kia được 2 trên 6 kiểu chuyến đi; cả hai lịch đều có lỗi giờ giấc đếm được bằng code (xếp quá giờ đóng cửa, bữa tối kéo qua nửa đêm), và lựa chọn "buổi tối" bổ sung không làm lịch đổi. Bốn kiểu còn lại hỏng vì script của B chờ chưa đủ lâu — chưa kết luận gì về chúng.
