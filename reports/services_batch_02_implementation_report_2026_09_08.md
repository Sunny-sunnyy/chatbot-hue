# Implementation Report: Services Batch 2 — Lịch trình du lịch Huế (Ngắn ngày & 3 ngày 2 đêm)

- **Implementer:** Implementer
- **Date:** 2026-09-08
- **Canonical guide:** `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
- **Hồ sơ kiểm chứng:** `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XLI và Mục XLII)
- **Tài liệu bàn giao:**
  1. `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md`
  2. `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`

---

## 1. Tổng quan triển khai

Implementer đã hoàn tất việc nghiên cứu, đối chiếu xác thực và biên soạn 02 tài liệu answer-facing hướng dẫn lịch trình thuộc Services Batch 2 theo quy chuẩn của Inventory và phân công của Người dùng:
- **Tài liệu 1 (Ngắn ngày):** Phục vụ quỹ thời gian từ nửa ngày (buổi sáng, buổi chiều, buổi tối), trọn 1 ngày cho người lần đầu và 2 ngày 1 đêm; tích hợp các biến thể theo phương tiện đến (tàu hỏa ga Huế, máy bay sân bay Phú Bài, từ Đà Nẵng) và điều kiện thời tiết (mưa dầm, nắng nóng gay gắt).
- **Tài liệu 2 (3 ngày 2 đêm):** Khung lịch trình tiêu chuẩn vàng cho du lịch Huế tự túc; phân bổ cân bằng năng lượng theo 3 ngày; tích hợp 4 phương án chuyên biệt (chiều sâu di sản, đời sống bản địa/food tour, sinh thái đầm phá/Bạch Mã, gia đình có trẻ nhỏ/người cao tuổi), phương án thích ứng ngày mưa bất chợt và phương án mở rộng 4 ngày 3 đêm.

Toàn bộ các bài học kinh nghiệm và nguyên tắc chấn chỉnh từ Batch 1 đã được áp dụng triệt để:
- Không dùng mỹ từ, giữ văn phong bách khoa, trung tính, hướng dẫn thiết thực.
- Không khóa cứng giờ giấc chi tiết từng phút, không cố định số hiệu tàu xe hay giá vé dễ biến động; chỉ khóa logic gom cụm tuyến và thời lượng tương đối.
- Tách biệt rõ ràng Ca Huế trên sông Hương và Nhã nhạc cung đình Huế tại Duyệt Thị Đường.
- Khóa chặt các điều kiện an toàn đối với hoạt động chèo SUP, thuyền sông Hương và đường đèo núi.

---

## 2. Nguồn dữ liệu & Hồ sơ kiểm chứng

Implementer đã tổng hợp và xử lý toàn bộ 15 URL do Người dùng cung cấp cho Batch 2:
1. `https://vnquehuongtoi.com/blog/du-lich-hue-3-ngay-2-dem-tu-tuc-lich-trinh-chi-tiet-2026`
2. `https://vnquehuongtoi.com/blog/lich-trinh-du-lich-hue-3-ngay-2-dem-tu-tuc-2026`
3. `https://mia.vn/cam-nang-du-lich/du-lich-hue-3-ngay-2-dem-20032`
4. `https://mia.vn/cam-nang-du-lich/kinh-nghiem-du-lich-hue-3-ngay-2-dem-an-gi-choi-gi-2582`
5. `https://mytour.vn/vi/blog/bai-viet/goi-y-lich-trinh-hanh-trinh-tham-hiem-hue-trong-vong-3-ngay-2-dem.html`
6. `https://mytour.vn/vi/blog/bai-viet/trai-nghiem-day-du-co-do-voi-ke-hoach-du-lich-hue-3-ngay-2-dem-ti-mi.html`
7. `https://mytour.vn/vi/blog/bai-viet/duoc-phep-nghi-vai-ngay-that-la-mot-niem-vui-lon-hay-xem-ngay-lich-trinh-hue-tu-tuc-3n2d-cua-mytourvn-de-tan-huong-ky-nghi-cua-ban.html`
8. `https://vuivivudanang.vn/blogs/tin-tuc-hue/du-lich-hue-tu-tuc-3-ngay-2-dem-lich-trinh-chi-tiet-an-gi-di-dau-chi-phi-moi-nhat`
9. `https://vuivivudanang.vn/blogs/tin-tuc-hue/lich-trinh-hue-3-ngay-2-dem-chi-tiet-nhat-cho-nguoi-di-lan-dau`
10. `https://www.thegioididong.com/hoi-dap/du-lich-hue-cam-nang-tu-tuc-tu-a-z-1591265`
11. `https://dulichdanda.com/du-lich/hue/` (Ghi nhận lỗi SSL 526, đã đối chiếu chéo độc lập)
12. `https://vietsensetravel.com/kinh-nghiem-du-lich-hue-chi-tiet-tu-az-n.html`
13. `https://queenbus.com.vn/du-lich-hue-3-ngay-2-dem`
14. `https://huelogistics.net/lich-trinh-du-lich-hue-3-ngay-2-dem-chi-tiet-an-gi-di-dau-o-dau/`
15. `https://www.traveloka.com/vi-vn/explore/culinary/an-gi-o-hue/143468`

Hồ sơ kiểm chứng chi tiết cấp claim, bảng ma trận đối chiếu địa giới hành chính và danh mục dữ liệu động đã được tích hợp đầy đủ tại:
- **Mục XLI:** Hồ sơ kiểm chứng cho `Lịch trình du lịch Huế ngắn ngày.md`.
- **Mục XLII:** Hồ sơ kiểm chứng cho `Lịch trình du lịch Huế 3 ngày 2 đêm.md`.

---

## 3. Chuẩn hóa địa giới hành chính hiện hành mốc 09/2026

Toàn bộ các địa danh xuất hiện trong cả 2 lịch trình đều tuân thủ 100% mô hình 40 đơn vị hành chính cấp xã theo Nghị quyết 1675/NQ-UBTVQH15:
- **Lõi bờ bắc:** Phường Phú Xuân (Đại Nội, Kỳ Đài, Chợ Đông Ba, phố cổ).
- **Lõi bờ nam:** Phường Thuận Hóa (Ga Huế, Cung An Định, Trường Quốc Học, phố Tây).
- **Tuyến tây nam:** Phường Kim Long (Chùa Thiên Mụ, Lăng Minh Mạng) và phường Thủy Xuân (Lăng Tự Đức, Lăng Khải Định, Làng hương Thủy Xuân, Đồi Vọng Cảnh).
- **Phía đông:** Phường Hóa Châu (Bao Vinh, Rú Chá), phường Dương Nỗ (Thanh Tiên, Sình), phường Mỹ Thượng (Đầm Chuồn), phường Thuận An (biển Thuận An), phường Thanh Thủy (Cầu ngói Thanh Toàn).
- **Phía nam:** Xã Phú Lộc (Vườn quốc gia Bạch Mã), xã Chân Mây – Lăng Cô (Vịnh Lăng Cô, Đầm Lập An, Hải Vân Quan).
- **Phía bắc:** Phường Phong Thái (Suối khoáng Alba Thanh Tân), phường Phong Dinh (Làng cổ Phước Tích).

Tuyệt đối không dùng tên quận/huyện cũ hoặc phường cũ trước sáp nhập.

---

## 4. Kết quả kiểm tra kỹ thuật (Verification)

| Tiêu chí kiểm tra | `Lịch trình du lịch Huế ngắn ngày.md` | `Lịch trình du lịch Huế 3 ngày 2 đêm.md` | Đánh giá |
|:---|:---:|:---:|:---:|
| **Số dòng (Lines)** | 249 | 338 | Chuẩn mực |
| **Cấu trúc Headings** | 1 H1, 10 H2, 21 H3 | 1 H1, 11 H2, 26 H3 | Khớp 100% Inventory |
| **Trailing Whitespace** | 0 lỗi | 0 lỗi | Đạt |
| **YAML Frontmatter** | Không có | Không có | Đạt (Clean RAG) |
| **Section `## Nguồn dữ liệu`** | Không có | Không có | Đạt |
| **Link ngoài (`https://`)** | Không có | Không có | Đạt |
| **Wiki-link (`[[]]`)** | Không có | Không có | Đạt |
| **Rò rỉ tên file `.md`** | Không có | Không có | Đạt |
| **Mỹ từ quảng bá** | 0 lỗi | 0 lỗi | Trung tính |
| **Chunk Independence** | 100% đạt | 100% đạt | Đạt |

---

## 5. Kết luận

Services Batch 2 đã hoàn thành toàn diện, đạt độ sạch Markdown tuyệt đối và sẵn sàng để Reviewer tiến hành thẩm định.
