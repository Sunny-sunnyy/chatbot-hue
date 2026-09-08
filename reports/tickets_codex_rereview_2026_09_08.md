# Codex Re-review: Du lịch Huế - Nhánh vé tham quan và trải nghiệm (Tickets)

Decision: ready_for_user_confirmation  
Reviewer: Codex  
Date: 2026-09-08  
Canonical guide: `knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md`  
Implementation report: `reports/tickets_implementation_correction_report_2026_09_08.md`  

---

## 1. Phạm vi đã review

Thẩm định độc lập đợt sửa đổi tập trung (batch correction) khắc phục toàn bộ 03 Major Findings và 03 Minor Findings được ghi nhận tại `reports/tickets_codex_review_2026_09_08.md`:
- `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md`
- `knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md`
- `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
- `knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md`
- `knowledge-base-hue/tourism/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md`
- `knowledge-base-hue/meta/tourism-research-evidence.md` (mục XLVI, XLVII)
- `reports/tickets_implementation_correction_report_2026_09_08.md`

---

## 2. Findings & Trạng thái đóng

1. **Major Finding 1: Thừa ngày miễn vé 30/4 và 01/5 tại Hải Vân Quan**
   - *Kiểm tra thực tế:* Dòng 75–86 của `Vé tham quan Hải Vân Quan.md` đã xóa bỏ hoàn toàn 2 gạch đầu dòng ngày 30/4 và 01/5. Danh sách ngày miễn phí cho công dân Việt Nam hiện khớp 100% với Nghị quyết số 05/2026/NQ-HĐND (Tết, 26/3, 29/3, 19/8, 02/9, 23/11 & 24/11).
   - *Trạng thái:* **CLOSED (ĐÃ ĐÓNG)**.

2. **Major Finding 2: Địa giới hành chính đỉnh đèo Hải Vân theo Nghị quyết 1675/NQ-UBTVQH15**
   - *Kiểm tra thực tế:* Dòng 19 của `Vé tham quan Hải Vân Quan.md` đã được cập nhật xác định ranh giới giữa `xã Chân Mây – Lăng Cô, thành phố Huế` và `phường Hải Vân, thành phố Đà Nẵng` (kèm chú thích tên cũ trước ngày 01/07/2025), đồng bộ hoàn toàn với file canonical `knowledge-base-hue/tourism/Đèo Hải Vân.md`.
   - *Trạng thái:* **CLOSED (ĐÃ ĐÓNG)**.

3. **Major Finding 3: Địa giới hành chính Không gian lưu niệm Lê Bá Đảng**
   - *Kiểm tra thực tế:* Dòng 155, 156 và dòng 298 của `Vé các điểm tham quan và trải nghiệm khác ở Huế.md` đã được sửa thành `Thôn Kim Sơn, phường Thủy Xuân, thành phố Huế` (chú thích rõ khu vực xã Thủy Bằng cũ trước khi sáp nhập vào phường Thủy Xuân theo Nghị quyết 1675/NQ-UBTVQH15), nhất quán 100% với File 2 dòng 42.
   - *Trạng thái:* **CLOSED (ĐÃ ĐÓNG)**.

4. **Minor Finding 1: Số hiệu quyết định Quy chế Ca Huế cũ**
   - *Kiểm tra thực tế:* Dòng 79 của File 4 và dòng 1973 của evidence đã được sửa thành `21/2024/QĐ-UBND` ngày 03/05/2024.
   - *Trạng thái:* **CLOSED (ĐÃ ĐÓNG)**.

5. **Minor Finding 2: Đồng bộ mốc phân loại thuyền đơn/đôi Ca Huế**
   - *Kiểm tra thực tế:* Dòng 86–87 của File 4 đã điều chỉnh thành `dưới 15 khách` (thuyền đơn) và `từ 15 khách trở lên` (thuyền đôi), đồng bộ với dòng 127 và thực tế bến Tòa Khâm.
   - *Trạng thái:* **CLOSED (ĐÃ ĐÓNG)**.

6. **Minor Finding 3: Diễn đạt tiêu chuẩn độ tuổi trẻ em Quần thể Di tích Cố đô Huế**
   - *Kiểm tra thực tế:* Dòng 119–124 và dòng 135 của File 1 đã làm rõ độ tuổi 7–12 là căn cứ pháp lý chính theo Nghị quyết số 55/2025/NQ-HĐND; mốc chiều cao dưới 1,2m chỉ mang tính phụ trợ thực địa.
   - *Trạng thái:* **CLOSED (ĐÃ ĐÓNG)**.

---

## 3. Cách Reviewer chạy lại thật

```bash
git status --short
git diff --check
git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md"
git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md"
git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md"
git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md"
git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md"
```

Đọc và đối chiếu từng dòng exact diff giữa trạng thái ban đầu và sau khi sửa đổi.

---

## 4. Kết quả quan sát

- `git diff --check`: PASS (mã thoát 0, không có lỗi định dạng hay xung đột).
- `git diff --no-index --check /dev/null`: PASS (output chẩn đoán rỗng, không có trailing whitespace trên toàn bộ 05 file tickets).
- Toàn bộ 05 file answer-facing giữ nguyên vẹn tiêu chuẩn định dạng: duy nhất 01 H1 khớp tên file, không YAML frontmatter, không URL ngoài `http/https`, không wiki-link, không đuôi `.md` trong bài, không metadata RAG.
- Toàn bộ 06/06 findings đã được giải quyết triệt để, không phát sinh finding mới.

---

## 5. Giới hạn hoặc phần chưa chạy

Không có giới hạn kỹ thuật trong phạm vi nhánh vé tham quan. Dữ liệu niêm yết thương mại tại các nhà thuyền Ca Huế, xe buýt 2 tầng, Alba Thanh Tân, Bạch Mã Village và Sốnglab là mức giá ghi nhận tại thời điểm tháng 09/2026; cẩm nang đã khuyến cáo người đọc xác nhận lại sát ngày đi.

---

## 6. Decision và Approval Closure Contract

- **Technical Decision:** `ready_for_user_confirmation`.

### Approval Closure Contract
1. **Xác nhận cần từ người dùng:** Người dùng xác nhận nghiệm thu kỹ thuật đối với 05 file cẩm nang vé du lịch Huế trong thư mục `knowledge-base-hue/tourism/tickets/`.
2. **Cập nhật trạng thái sau xác nhận:**
   - Reviewer tự cập nhật `session_prompt/Project_Status.md`: Ghi nhận hoàn tất nhánh `tourism/tickets` (05 file answer-facing và 01 inventory).
   - Reviewer cập nhật `session_prompt/CURRENT_HANDOFF.md`: Chuyển trạng thái sang `State: completed`, đóng nhiệm vụ tickets và chờ lệnh tiếp theo từ người dùng.
3. **Quyền hạn Git:** Giữ nguyên `git_authorization: none` (không commit/push khi chưa có lệnh riêng từ người dùng).
4. **Bước tiếp theo:** Sau khi người dùng xác nhận nghiệm thu nhánh vé, toàn bộ dữ liệu nội dung du lịch Huế (`places`, `services`, `tickets`) sẽ sẵn sàng cho bước lập spec/plan migration taxonomy sang `travel/` theo đúng lộ trình đã ghi nhận trong `Project_Status.md`.
