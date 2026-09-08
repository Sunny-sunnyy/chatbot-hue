# Codex Review: Du lịch Huế - Nhánh vé tham quan và trải nghiệm (Tickets)

Decision: changes_requested  
Reviewer: Codex  
Date: 2026-09-08  
Canonical guide: `knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md`  
Implementation report: `reports/tickets_implementation_report_2026_09_08.md`  

---

## 1. Phạm vi đã review

Thẩm định độc lập toàn bộ các file triển khai thuộc phạm vi bàn giao:
- 05 file cẩm nang vé answer-facing mới tạo trong `knowledge-base-hue/tourism/tickets/`:
  1. `Hướng dẫn mua và sử dụng vé du lịch Huế.md`
  2. `Vé tham quan Quần thể Di tích Cố đô Huế.md`
  3. `Vé tham quan Hải Vân Quan.md`
  4. `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
  5. `Vé các điểm tham quan và trải nghiệm khác ở Huế.md`
- Hồ sơ nghiên cứu và kiểm chứng tại các mục XLIV, XLV, XLVI, XLVII, XLVIII trong `knowledge-base-hue/meta/tourism-research-evidence.md`.
- Báo cáo triển khai `reports/tickets_implementation_report_2026_09_08.md`.
- Sử dụng 05 sub-agent chuyên trách độc lập kết hợp websearch tiếng Việt để kiểm chứng chéo từng căn cứ pháp lý, biểu phí, chính sách ưu đãi, đối tượng miễn giảm và địa giới hành chính hiện hành sau ngày 01/07/2025 theo Nghị quyết số 1675/NQ-UBTVQH15.

---

## 2. Findings

### Major Findings (Bắt buộc phải sửa)

1. **Major Finding 1: Thừa ngày miễn phí 30/4 và 01/5 tại Di tích Hải Vân Quan**
   - **Vị trí:** `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md` (dòng 82–83) và `knowledge-base-hue/meta/tourism-research-evidence.md` (dòng 1953).
   - **Requirement bị ảnh hưởng:** Tiêu chí nghiệm thu của inventory về tính chính xác của dữ liệu pháp lý cấp 1 và chính sách miễn giảm.
   - **Evidence:** Căn cứ toàn văn Nghị quyết số 05/2026/NQ-HĐND ngày 22/05/2026 của Hội đồng nhân dân thành phố Huế quy định mức thu, quản lý và sử dụng phí tham quan Hải Vân Quan, các ngày lễ được mở cửa miễn phí cho công dân Việt Nam chỉ bao gồm:
     + Tết Nguyên Đán (các ngày nghỉ chính thức).
     + Ngày 26/3 (Ngày giải phóng thành phố Huế).
     + Ngày 29/3 (Ngày giải phóng thành phố Đà Nẵng).
     + Ngày 19/8 (Ngày Cách mạng Tháng Tám thành công).
     + Ngày 02/9 (Ngày Quốc khánh).
     + Ngày 23/11 và 24/11 (Ngày Di sản Văn hóa Việt Nam).
     *Nghị quyết hoàn toàn KHÔNG có quy định miễn phí vào ngày 30/4 và ngày 01/5.*
   - **Tác động:** Sai lệch văn bản pháp quy, cung cấp thông tin sai khiến du khách có thể bị động về ngân sách khi đến tham quan vào dịp lễ 30/4 – 01/5.
   - **Tiêu chí đóng:** Xóa bỏ hoàn toàn 2 dòng quy định miễn phí ngày 30/4 và 01/5 tại dòng 82–83 trong `Vé tham quan Hải Vân Quan.md`; đồng bộ lại tóm tắt tại dòng 1953 của `tourism-research-evidence.md`.

2. **Major Finding 2: Địa giới hành chính tại đỉnh đèo Hải Vân chưa cập nhật theo Nghị quyết số 1675/NQ-UBTVQH15**
   - **Vị trí:** `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md` (dòng 19).
   - **Requirement bị ảnh hưởng:** Yêu cầu bắt buộc về địa giới hành chính hiện hành mốc tháng 09/2026 theo Nghị quyết 1675/NQ-UBTVQH15, không dùng địa danh cũ.
   - **Evidence:** Dòng 19 hiện ghi: *"thị trấn Lăng Cô, huyện Phú Lộc, thành phố Huế (trực thuộc Trung ương) và phường Hòa Hiệp Bắc, quận Liên Chiểu, thành phố Đà Nẵng"*. Kể từ ngày 01/07/2025, theo Nghị quyết 1675/NQ-UBTVQH15, thị trấn Lăng Cô đã hợp nhất cùng 3 xã lân cận thành **xã Chân Mây – Lăng Cô, thành phố Huế**; phía Đà Nẵng, phường Hòa Hiệp Bắc đã sáp nhập thành **phường Hải Vân, thành phố Đà Nẵng** (đã chuẩn hóa trong file canonical `knowledge-base-hue/tourism/Đèo Hải Vân.md` dòng 9–10).
   - **Tác động:** Sử dụng địa danh hành chính cũ đã hết hiệu lực, gây mâu thuẫn với kho tri thức của dự án.
   - **Tiêu chí đóng:** Cập nhật dòng 19 xác định đúng ranh giới hành chính hiện hành: giữa **xã Chân Mây – Lăng Cô, thành phố Huế** và **phường Hải Vân, thành phố Đà Nẵng** (có thể mở ngoặc chú thích tên cũ trước ngày 01/07/2025 để người đọc tiện tra cứu đối chiếu).

3. **Major Finding 3: Chưa cập nhật địa giới hành chính của Không gian lưu niệm Lê Bá Đảng theo Nghị quyết 1675/NQ-UBTVQH15**
   - **Vị trí:** `knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md` (dòng 155 và dòng 298).
   - **Requirement bị ảnh hưởng:** Yêu cầu chuẩn hóa địa giới hành chính hiện hành và tính nhất quán nội bộ với `Vé tham quan Quần thể Di tích Cố đô Huế.md` (dòng 42).
   - **Evidence:** File hiện ghi địa chỉ tại thôn Kim Sơn, `xã Thủy Bằng`. Tuy nhiên, theo Nghị quyết số 1675/NQ-UBTVQH15 có hiệu lực từ ngày 01/07/2025, toàn bộ diện tích và dân số của xã Thủy Bằng đã được sáp nhập cùng phường Thủy Biều và phường Thủy Xuân cũ để thành lập một đơn vị hành chính mới là **phường Thủy Xuân, thành phố Huế** (xã Thủy Bằng không còn tồn tại là đơn vị cấp xã độc lập).
   - **Tác động:** Dùng sai cấp đơn vị hành chính hiện hành, mâu thuẫn trực tiếp với dòng 42 của File 2.
   - **Tiêu chí đóng:** Sửa địa chỉ tại dòng 155 và dòng 298 thành `Thôn Kim Sơn, phường Thủy Xuân, thành phố Huế` (có thể ghi chú thêm: khu vực xã Thủy Bằng cũ trước đợt sáp nhập tháng 07/2025).

---

### Minor Findings (Khuyến nghị hoàn thiện)

4. **Minor Finding 1: Số hiệu quyết định cũ bị thay thế về Quy chế Ca Huế**
   - **Vị trí:** `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (dòng 79) và `meta/tourism-research-evidence.md` (dòng 1973).
   - **Evidence:** Quyết định do UBND tỉnh Thừa Thiên Huế ban hành ngày 03/05/2024 về Quy chế quản lý Ca Huế mang số hiệu **21/2024/QĐ-UBND** (còn QĐ 24/2024/QĐ-UBND ngày 09/05/2024 là về Quỹ phòng, chống thiên tai). File ghi nhầm thành 24/2024/QĐ-UBND.
   - **Tiêu chí đóng:** Đổi `24/2024/QĐ-UBND` thành `21/2024/QĐ-UBND`.

5. **Minor Finding 2: Đồng bộ mốc phân loại thuyền đơn và thuyền đôi Ca Huế**
   - **Vị trí:** `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (dòng 86–87 so với dòng 127).
   - **Evidence:** Dòng 86–87 ghi mốc "dưới 20 khách" / "từ 20 khách trở lên", trong khi dòng 127 và quy chuẩn phân loại thuyền Ca Huế thực tế là mốc 15 khách (thuyền đơn dưới 15 khách, thuyền đôi từ 15 khách trở lên).
   - **Tiêu chí đóng:** Điều chỉnh dòng 86–87 thành mốc "dưới 15 khách" và "từ 15 khách trở lên" để đồng bộ nội bộ.

6. **Minor Finding 3: Đồng bộ diễn đạt tiêu chuẩn trẻ em Quần thể Di tích Cố đô Huế**
   - **Vị trí:** `knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md` (dòng 120).
   - **Evidence:** File 2 (dòng 13, 120) căn cứ sát Nghị quyết 55/2025 lấy độ tuổi làm tiêu chuẩn pháp lý (dưới 7 tuổi miễn phí, 7–12 tuổi vé trẻ em; mốc chiều cao dưới 1,2m là hỗ trợ kiểm tra thực địa). File 1 ghi thêm mốc `0,8m đến dưới 1,4m`.
   - **Tiêu chí đóng:** Diễn đạt rõ ràng độ tuổi 7–12 là căn cứ pháp lý chính của Nghị quyết 55/2025 để tránh du khách nhầm lẫn với quy chuẩn đo chiều cao của các khu vui chơi tư nhân.

---

## 3. Cách Reviewer chạy lại thật

1. Kiểm tra định dạng và trạng thái kho mã:
   ```bash
   git status --short
   git diff --check
   git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md"
   git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md"
   git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md"
   git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md"
   git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md"
   ```
2. Khởi chạy 05 sub-agent chuyên trách độc lập tra cứu web bằng tiếng Việt:
   - Trích xuất và đối chiếu Nghị quyết 55/2025/NQ-HĐND của HĐND thành phố Huế.
   - Trích xuất và đối chiếu Nghị quyết 05/2026/NQ-HĐND của HĐND thành phố Huế.
   - Trích xuất và đối chiếu Quyết định 104/2025/QĐ-UBND (Công báo thành phố Huế Số 59/2025).
   - Đối chiếu danh mục sắp xếp 40 đơn vị hành chính cấp xã theo Nghị quyết số 1675/NQ-UBTVQH15 của Ủy ban Thường vụ Quốc hội.
   - Đối chiếu thực tế dữ liệu các khu du lịch: VQG Bạch Mã (sạt lở Km12, hotline 0234.3871330), Bạch Mã Village, Alba Thanh Tân, Không gian lưu niệm Lê Bá Đảng, Sốnglab, City Sightseeing.

---

## 4. Kết quả quan sát

- **Kết quả kỹ thuật:**
  + `git diff --check`: PASS (mã thoát 0).
  + `git diff --no-index --check /dev/null`: PASS (output rỗng, sạch trailing whitespace).
  + Tiêu chuẩn answer-facing: Cả 05 file đều có duy nhất 01 H1 khớp chính xác tên file; không YAML frontmatter; không liên kết ngoài `http/https`; không wiki-link; không đuôi `.md` trong bài; không metadata RAG.
- **Kết quả thẩm định nội dung:**
  + File 1 (`Hướng dẫn mua và sử dụng vé du lịch Huế.md`): Đạt chuẩn xuất sắc 100%.
  + File 2 (`Vé tham quan Quần thể Di tích Cố đô Huế.md`): Đạt chuẩn xuất sắc 100% (căn cứ pháp lý, 12 điểm lẻ, 7 combo, miễn giảm, địa giới 12 di tích đều chuẩn xác).
  + File 3 (`Vé tham quan Hải Vân Quan.md`): Nội dung rất tốt nhưng dính 2 Major Findings (thừa ngày miễn vé 30/4 & 01/5; địa giới hành chính chưa cập nhật xã Chân Mây – Lăng Cô / phường Hải Vân).
  + File 4 (`Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`): Đạt chuẩn tốt, dính 2 Minor Findings về số hiệu quyết định cũ và mốc thuyền 15 khách.
  + File 5 (`Vé các điểm tham quan và trải nghiệm khác ở Huế.md`): Nội dung chi tiết chuẩn xác, dính 1 Major Finding về địa giới hành chính xã Thủy Bằng cần sửa thành phường Thủy Xuân.

---

## 5. Giới hạn hoặc phần chưa chạy

Không có giới hạn review nào ngoài phạm vi đã nêu. Mọi thông tin đã được kiểm chứng độc lập trực tiếp qua văn bản quy phạm pháp luật và hệ thống dữ liệu thực địa mốc tháng 09/2026.

---

## 6. Decision và bước tiếp theo

- **Decision:** `changes_requested`.
- **Handoff kind:** `correction`.
- **Target role:** `implementer`.
- **Phạm vi sửa đổi (Correction Delta):**
  1. File `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md`: Sửa Major Finding 1 (xóa ngày 30/4 và 01/5) và Major Finding 2 (cập nhật xã Chân Mây – Lăng Cô / phường Hải Vân).
  2. File `knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md`: Sửa Major Finding 3 (cập nhật Thôn Kim Sơn, phường Thủy Xuân, thành phố Huế).
  3. File `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`: Sửa Minor Finding 1 (QĐ 21/2024) và Minor Finding 2 (mốc 15 khách).
  4. File `knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md`: Cân chỉnh Minor Finding 3 nếu cần thiết.
  5. File `knowledge-base-hue/meta/tourism-research-evidence.md`: Đồng bộ lại các mục tương ứng tại XLVI và XLVII.
- Reruns bắt buộc sau khi sửa: `git diff --check`, no-index whitespace check và đọc lại exact diff các dòng được sửa.
- Git authorization: `none`.
