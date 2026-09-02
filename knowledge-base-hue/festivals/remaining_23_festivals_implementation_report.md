# Báo cáo thực hiện điều chỉnh 23 file lễ hội theo Codex Review (Vòng Correction 3)

- **Người thực hiện:** Implementer
- **Tài liệu căn cứ:** `knowledge-base-hue/festivals/remaining_23_festivals_codex_review.md` (Mục 7 - Nghiệm thu correction vòng 2 ngày 02/09/2026) & `session_prompt/CURRENT_HANDOFF.md`
- **Base commit:** `66e58a7`
- **Thời gian hoàn thành:** 02/09/2026
- **Trạng thái:** Hoàn tất toàn bộ 11/11 file có major tại Mục 7.2; `git diff --check` pass; sẵn sàng nghiệm thu.

---

## 1. Tổng quan kết quả thực hiện vòng 3

1. **Phạm vi xử lý:**
   - Hoàn thành xử lý chính xác và triệt để toàn bộ **11/11 file có major** tại Mục 7.2 của báo cáo Codex Review.
   - Tuyệt đối không chạm vào 12 file còn lại trong batch 23 file lễ hội.
   - Đối với `Lễ hội Áo dài Huế.md`: Thực hiện nghiêm túc chỉ đạo tại Mục 7.4, không can thiệp chỉnh sửa file này, giữ nguyên delta ngoài scope hiện tại để Reviewer xử lý tách biệt khi đóng Git.
2. **Kỷ luật dữ liệu và chuẩn hóa hành chính:**
   - Tuyệt đối **không thêm mục `## Nguồn dữ liệu`**, không thêm YAML frontmatter, không thêm liên kết nội bộ hay placeholder vào bất kỳ file entity nào.
   - Cập nhật chuẩn xác địa giới hành chính hiện hành theo Nghị quyết số 1675/NQ-UBTVQH15 và các văn bản chỉ đạo của UBND TP Huế năm 2026:
     - 352 Chi Lăng và Đàn Xã Tắc: thuộc **phường Phú Xuân** (trước đây thuộc phường Gia Hội và phường Thuận Hòa).
     - Điện Huệ Nam và Đình làng Hải Cát: thuộc **phường Kim Long** (trước đây thuộc xã Hương Thọ).
     - Tổ đình Từ Đàm, Đàn Nam Giao, Lăng mộ Tổ nghề Kim hoàn (kiệt 175 Phan Bội Châu): thuộc **phường Thuận Hóa** (trước đây thuộc phường Trường An).
     - Núi Tứ Tượng / thôn Bằng Lãng: thuộc **phường Thủy Xuân** (trước đây thuộc xã Thủy Bằng).
   - Xóa bỏ triệt để các nội dung ẩm thực/rượu chưa có bằng chứng xác thực tại `Lễ Thu tế làng An Truyền.md`.
   - Bỏ hoàn toàn các nhận định khái quát "mở cửa tự do" cho toàn bộ nhóm sự kiện tại `Lễ hội Ẩm thực Huế.md`, `Ngày hội Sen Huế.md` và `Chợ quê ngày hội – Cầu ngói Thanh Toàn.md`.
   - Đồng bộ hóa mốc phục dựng `Lễ Ban Sóc triều Nguyễn.md` và điều kiện hóa hoạt động hoa đăng tại `Lễ hội Quán Thế Âm tại Huế.md`.
3. **Kỷ luật Git:**
   - Kiểm tra cú pháp: `git diff --check` sạch hoàn toàn (exit code 0).
   - Tuyệt đối không tự ý commit hoặc push; bảo toàn worktree để Reviewer thực hiện đóng gate theo đúng thẩm quyền.

---

## 2. Bảng mapping chi tiết từng finding tại Mục 7.2 sang exact changed lines và nguồn xác minh

| STT | Tên file | Mức độ & Nội dung finding (Mục 7.2) | Dòng đã sửa (Exact lines) | Tóm tắt nội dung chỉnh sửa | Nguồn xác minh |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Lễ hội Điện Huệ Nam.md` | `major`, cập nhật địa giới sau sắp xếp: 352 Chi Lăng thuộc phường Phú Xuân, Điện Huệ Nam/Hải Cát thuộc phường Kim Long; chỉ giữ tên cũ trong bối cảnh lịch sử | Dòng 12, 74, 77, 116 | Sửa 352 Chi Lăng thành phường Phú Xuân (địa bàn phường Gia Hội cũ); cụm di tích Điện Huệ Nam và làng Hải Cát thành phường Kim Long (địa bàn xã Hương Thọ cũ). | Nghị quyết 1675/NQ-UBTVQH15; Quyết định phân định địa giới UBND TP Huế năm 2026 (*hue.gov.vn*) |
| 2 | `Đại lễ Phật đản tại Huế.md` | `major`, cập nhật địa giới hiện hành: Tổ đình Từ Đàm thuộc phường Thuận Hóa, Quốc tự Diệu Đế thuộc phường Phú Xuân | Dòng 15–16, 19, 56–57, 72 | Sửa Tổ đình Từ Đàm thành phường Thuận Hóa (phường Trường An cũ); Quốc tự Diệu Đế thành phường Phú Xuân (phường Gia Hội cũ); núi Tứ Tượng thành phường Thủy Xuân (xã Thủy Bằng cũ). | Nghị quyết 1675/NQ-UBTVQH15 (*xaydungchinhsach.chinhphu.vn*) |
| 3 | `Lễ tế Nam Giao.md` | `major`, cập nhật Đàn Nam Giao thành phường Thuận Hóa; Trường An chỉ ghi như địa bàn cũ | Dòng 11, 13, 34, 108 | Cập nhật di tích Đàn Nam Giao và làng Dương Xuân thuộc phường Thuận Hóa (địa bàn phường Trường An trước đây); đồng thời cập nhật Đàn Xã Tắc thuộc phường Phú Xuân ở phần phân biệt lễ hội. | Nghị quyết 1675/NQ-UBTVQH15 (*xaydungchinhsach.chinhphu.vn*) |
| 4 | `Lễ tế Xã Tắc.md` | `major`, cập nhật Đàn Xã Tắc thành phường Phú Xuân; Thuận Hòa chỉ ghi như địa bàn cũ | Dòng 11, 13, 52, 93 | Cập nhật khuôn viên di tích Đàn Xã Tắc thuộc phường Phú Xuân (địa bàn phường Thuận Hòa trước đây); đồng thời cập nhật Đàn Nam Giao thuộc phường Thuận Hóa ở phần phân biệt lễ hội. | Nghị quyết 1675/NQ-UBTVQH15 (*xaydungchinhsach.chinhphu.vn*) |
| 5 | `Lễ giỗ Tổ nghề Kim hoàn.md` | `major`, khu lăng mộ kiệt 175 Phan Bội Châu cập nhật thành phường Thuận Hóa; tên cũ chỉ dùng trong bối cảnh lịch sử | Dòng 13, 25, 33, 53, 62 | Cập nhật toàn bộ các vị trí nhắc đến khu lăng mộ tổ nghề (kiệt 175 Phan Bội Châu) thành phường Thuận Hóa (địa bàn phường Trường An trước đây). | Nghị quyết 1675/NQ-UBTVQH15 (*xaydungchinhsach.chinhphu.vn*) |
| 6 | `Lễ hội Quán Thế Âm tại Huế.md` | `major`, núi Tứ Tượng/thôn Bằng Lãng cập nhật thành phường Thủy Xuân (Thủy Bằng là địa bàn cũ); `major`, đồng bộ hóa hoa đăng là hoạt động tùy chương trình từng kỳ | Dòng 11, 13, 26, 33, 53, 71 | Cập nhật núi Tứ Tượng và thôn Bằng Lãng thuộc phường Thủy Xuân (trước đây thuộc xã Thủy Bằng); sửa dòng 26 ở phần tổng quan đồng bộ với dòng 83: lễ thắp hoa đăng diễn ra trong các kỳ có bố trí theo chương trình. | Cổng TTĐT TP Huế xác nhận phường Thủy Xuân thành lập trên cơ sở Thủy Biều, Thủy Bằng, Thủy Xuân (*hue.gov.vn*) |
| 7 | `Lễ Ban Sóc triều Nguyễn.md` | `major`, dòng 127 đổi thành "các kỳ phục dựng gần đây thường tổ chức ngày 1/1; kiểm tra thông báo từng năm", không đóng đinh định kỳ hằng năm | Dòng 127 | Sửa dòng 127 thành: "các kỳ phục dựng gần đây thường tổ chức vào ngày 1/1 Dương lịch tại Quảng trường Ngọ Môn (du khách cần kiểm tra thông báo chính thức từng năm)", đồng bộ tuyệt đối với dòng 10, 69 và 198. | Thông cáo Trung tâm Bảo tồn Di tích Cố đô Huế |
| 8 | `Chợ quê ngày hội – Cầu ngói Thanh Toàn.md` | `major`, bỏ nhánh chợ đêm cuối tuần, mô tả đúng phiên 16 Âm lịch hằng tháng; `major`, dòng 120 bỏ khẳng định mở cửa tự do, hướng dẫn kiểm tra quy định | Dòng 66, 120 | Bỏ cụm "chợ đêm cuối tuần", xác định rõ phiên chợ đêm định kỳ ngày 16 Âm lịch hằng tháng là sinh hoạt thường kỳ độc lập với lễ hội 2 năm/lần; sửa dòng 120 hướng dẫn du khách kiểm tra nội quy, biểu giá và hướng dẫn tại điểm đến. | Kế hoạch Festival Huế 2026; Đề án phát triển du lịch cộng đồng Cầu ngói Thanh Toàn |
| 9 | `Lễ Thu tế làng An Truyền.md` | `major`, xóa nội dung nghề nấu rượu ở dòng 32, xóa toàn bộ mục ẩm thực/rượu làng ở dòng 74–79, và sửa lời khuyên tham quan ở dòng 87 | Dòng 32, 72–80, 87 | Xóa cụm từ "nghề nấu rượu gia truyền" ở dòng 32; xóa bỏ hoàn toàn mục "## Nét đẹp ẩm thực đầm Chuồn" (bánh khoái cá kình, rượu làng Chuồn, thủy sản đầm phá); sửa dòng 87 thành thời gian thích hợp để tham quan kiến trúc gỗ cổ truyền đình làng. | Đối chiếu tư liệu di tích đình làng An Truyền |
| 10 | `Ngày hội Sen Huế.md` | `major`, dòng 103 không khẳng định gian hàng mở cửa tự do, mô tả chính sách vào cửa/đăng ký tùy chương trình và kiểm tra thông báo ban tổ chức | Dòng 103 | Sửa dòng 103 thành: chính sách vào cửa các không gian trưng bày, tham gia workshop thủ công hoặc chương trình ẩm thực chuyên đề tùy thuộc vào quy định của từng kỳ tổ chức; du khách cần kiểm tra thông báo và hướng dẫn của ban tổ chức. | Kế hoạch Ngày hội Sen Huế 2026 (*phongdinh.hue.gov.vn*) |
| 11 | `Lễ hội Ẩm thực Huế.md` | `major`, dòng 107 bỏ khái quát chính sách vào cửa cho cả nhóm sự kiện; hướng dẫn kiểm tra vé/voucher/giá của từng chương trình | Dòng 107 | Sửa dòng 107 thành: chính sách vào cửa, việc phát hành vé hoặc phiếu ẩm thực (voucher/coupon) và biểu giá món ăn được quy định riêng theo từng chương trình, sự kiện cụ thể; du khách cần kiểm tra thông báo và hướng dẫn chính thức trước khi tham dự. | Kế hoạch các chương trình ẩm thực trong khuôn khổ Festival Huế |

---

## 3. Khai báo trạng thái Worktree và Git

- **Base commit xác định:** `66e58a7`
- **Head commit:** `worktree`
- **Danh sách 23 entity lễ hội thuộc batch:**
  - 11 entity đã hoàn thành điều chỉnh chuẩn xác theo Mục 7.2 nêu trên.
  - 12 entity còn lại trong batch giữ nguyên vẹn kết quả đạt từ vòng trước: `Hội vật làng Sình.md`, `Hội vật làng Thủ Lễ.md`, `Hội xuân Gia Lạc.md`, `Lễ hội Cầu ngư.md`, `Lễ hội Đua ghe truyền thống Huế.md`, `Lễ hội Đền Huyền Trân Công chúa.md`, `Lễ hội Hương xưa làng cổ – Phước Tích.md`, `Lễ hội Sóng nước Tam Giang.md`, `Lễ hội Thanh Trà Huế.md`, `Lễ hội làng Dương Nỗ.md`, `Lễ tế Bà Bún Vân Cù.md`, `Ngày hội Hoàng Mai Huế.md`.
- **Entity ngoài scope batch:** `Lễ hội Áo dài Huế.md` (giữ nguyên hiện trạng ngoài scope để Reviewer xử lý theo quy trình đóng Git).
- **Kiểm tra kỹ thuật:**
  - `git diff --check`: Pass 100% (exit code 0).
  - Không có conflict marker, trailing whitespace hay lỗi thụt lề.
  - Sẵn sàng bàn giao Reviewer nghiệm thu vòng 3.
