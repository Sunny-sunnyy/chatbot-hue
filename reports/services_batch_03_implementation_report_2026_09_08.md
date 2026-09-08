# Implementation Report: Services Batch 3 — Chi phí du lịch Huế

- **Implementer:** Implementer
- **Date:** 2026-09-08
- **Canonical guide:** `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
- **Hồ sơ kiểm chứng:** `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XLIII)
- **Tài liệu bàn giao:**
  1. `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md`

---

## 1. Tổng quan triển khai

Implementer đã hoàn tất việc nghiên cứu, lập ma trận dự toán tài chính và biên soạn tài liệu answer-facing hướng dẫn lập kế hoạch ngân sách cho chuyến đi Huế thuộc Services Batch 3:
- **Định vị & Ranh giới nghiêm ngặt:** Tài liệu cung cấp **khung phương pháp lập dự toán ngân sách và quản lý chi tiêu**, không phải bảng báo giá thương mại hay bảng giá vé chính thức.
- **Ranh giới với nhánh tickets:** Căn cứ theo Nghị quyết số 55/2025/NQ-HĐND ngày 10/12/2025 của HĐND thành phố Huế (vé tuyến 4 điểm 530.000 VNĐ, vé toàn bộ điểm 600.000 VNĐ), Nghị quyết 05/2026/NQ-HĐND (vé Hải Vân Quan 70.000 VNĐ) và khảo sát thực tế vé ca Huế thuyền rồng; không sao chép toàn bộ biểu phí chi tiết mà điều phối người đọc sang các cẩm nang chuyên ngành của nhánh `tourism/tickets/`.
- **Phân định rõ ràng chi phí cố định và chi phí biến đổi:** Tách bạch khoản chi chia sẻ theo nhóm/phòng (khách sạn, taxi, thuê ô tô) và khoản chi tính theo đầu người (ăn uống, vé tham quan, trải nghiệm thuyền rồng).
- **Ba khung ngân sách tiêu biểu:** Khung Tiết kiệm/Bình dân (400k – 650k/người/ngày); Khung Tiêu chuẩn/Trung bình (700k – 1.200k/người/ngày); Khung Thoải mái/Cao cấp (>1.500k/người/ngày).
- **Dự toán chi tiết theo thời lượng chuyến đi:** 1 ngày; 2 ngày 1 đêm; 3 ngày 2 đêm (với các kịch bản solo, cặp đôi, nhóm bạn và gia đình).

---

## 2. Nguồn dữ liệu & Hồ sơ kiểm chứng

Implementer đã tổng hợp và đối chiếu toàn bộ 10 URL do Người dùng cung cấp cho Batch 3:
1. `https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/chi-phi-di-hue.html`
2. `https://vuivivudanang.vn/blogs/tin-tuc-hue/chi-phi-du-lich-hue-2026-di-hue-het-bao-nhieu-tien-chi-tiet-tu-a-z`
3. `https://www.thegioididong.com/hoi-dap/du-lich-hue-cam-nang-tu-tuc-tu-a-z-1591265`
4. `https://junglebosstours.com/vi/kham-pha/blog-du-lich/du-lich-hue`
5. `https://www.bachhoaxanh.com/kinh-nghiem-hay/du-lich-hue-2026-co-gi-hot-goi-y-lich-trinh-va-diem-check-in-1591918`
6. `https://dulichdanda.com/du-lich/hue/`
7. `https://www.vietnamairlines.com/us/vi/plan-book/travel/travel-guide/kinh-nghiem-du-lich-hue`
8. `https://sinhtour.vn/chi-phi-di-hue-3-ngay-2-dem/`
9. `https://vinwonders.com/vi/wonderpedia/news/chi-phi-du-lich-hue/`
10. `https://baonghean.vn/kinh-nghiem-du-lich-hue-3-ngay-2-dem-tron-ven-chi-tiet-10303765.html`

Toàn bộ ma trận định mức chi tiêu, xử lý mâu thuẫn nguồn giá vé cũ và quy tắc tính toán dự phòng rủi ro phát sinh (10% – 15%) đã được ghi nhận chi tiết tại **Mục XLIII** của file `knowledge-base-hue/meta/tourism-research-evidence.md`.

---

## 3. Chuẩn hóa địa giới hành chính hiện hành mốc 09/2026

Tất cả các khu vực lưu trú, ẩm thực và tham quan được đề cập trong dự toán ngân sách đều gắn liền với đơn vị hành chính cấp xã hiện hành theo Nghị quyết 1675/NQ-UBTVQH15:
- Phường Phú Xuân, phường Thuận Hóa, phường Kim Long, phường Thủy Xuân, phường Vỹ Dạ, phường Thanh Thủy, phường Hóa Châu, xã Phú Lộc, xã Chân Mây – Lăng Cô.
- Không dùng tên địa danh hành chính cũ.

---

## 4. Kết quả kiểm tra kỹ thuật (Verification)

- **Số dòng (Lines):** 325 dòng.
- **Cấu trúc Headings:** 1 H1, 11 H2, 31 H3 (Khớp 100% Inventory).
- **Trailing Whitespace:** 0 lỗi.
- **Độ sạch Markdown:** 100% không YAML frontmatter, không mục `## Nguồn dữ liệu`, không liên kết ngoài `https://`, không wiki-link `[[]]`, không rò rỉ tên file `.md` hay đường dẫn nội bộ repository.
- **Chunk Independence:** 100% các tiêu đề H2, H3 và câu đầu tiên của từng đoạn đều định danh rõ ràng chủ thể, đảm bảo tính độc lập ngữ cảnh tuyệt đối khi trích xuất chunk cho hệ thống RAG.

---

## 5. Kết luận

Services Batch 3 (`Chi phí du lịch Huế.md`) đã hoàn thành toàn diện, đạt độ sạch kỹ thuật tuyệt đối và sẵn sàng để Reviewer tiến hành thẩm định.
