# Review — bài kho lưu trú NHÁP của E (`data/sua_kho_2026-11-13_luu_tru/`, chưa ghi kho)

Người kiểm: C (`hue-rag-b4`) · 12:15 14/11/2026 (`date`) · skill `risk-gated-agent-review` · 0 USD.
Repo public ⇒ review này tả ở mức loại; tên cơ sở chỉ nêu khi cần chỉ chỗ sai, và đó là tên công khai trong danh mục ngành du lịch.

**Kết luận: changes_requested — 1 major, 3 minor.**

## Đã kiểm
- **Luật curated:** cả 5 bài bắt đầu bằng `#`; không YAML; không mục rỗng; `## Nguồn dữ liệu` tối giản (danh mục Cục Du lịch + ngày lấy, khu theo bài cẩm nang của kho + OSM).
- **Dòng bắt buộc của spec** có ở đầu mỗi bài: nguồn + ngày, hạng có thể đã đổi, không gồm giá, chưa gồm homestay.
- **Không có** giá, số điện thoại, email, link đặt phòng, nhận xét. Bộ lọc trong script đúng, và C đọc lại 2 bài thấy không có.
- **Câu "khu này hợp với ai"** (5 bài) khớp ý bài cẩm nang của kho, mục "Nên chọn khu vực lưu trú nào": trung tâm hợp lần đầu đến, ăn uống, đi bộ tối; phía tây hợp người thích yên, nhà vườn, tuyến phía tây; ven biển chỉ hợp khi vùng đó là mục tiêu chính.
  - Bài trung tâm thêm "gần Kinh thành, Đại Nội, chợ Đông Ba, phố đi bộ". Bài cẩm nang không có ý này, nhưng đó là vị trí thật của khu, không phải lời hứa ⇒ chấp nhận.
- **Đếm hạng** trong bảng 141 cơ sở: 5 sao 10 · 4 sao 13 · 3 sao 8 · 2 sao 31 · 1 sao 49 · đạt chuẩn 30. Khớp số trong bài.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| M-1 | **major** | bảng 141 cơ sở ⇒ bài "3–5 sao" | **Cùng một khách sạn ở cùng địa chỉ (số 02 Lê Lợi) có hai dòng: một dòng 5 sao (tên tiếng Việt), một dòng 3 sao (tên tiếng Anh).** Bài liệt kê cả hai ⇒ kho tự mâu thuẫn về hạng, trợ lý có thể nói chắc một hạng sai. Bước khử trùng dùng khoá tên + địa chỉ nên không bắt được hai tên khác nhau. C dò "cùng số nhà + cùng đường" thấy thêm 6 cặp: cặp tên giống hệt + số "I", và 5 cặp tên khác hẳn — có thể là hai cơ sở thật chung toà nhà. | gộp cặp 02 Lê Lợi về **một** dòng, theo bản ghi mới nhất của danh mục (mở trang danh mục kiểm hạng); 6 cặp còn lại đọc tay, mỗi cặp một quyết định ghi vào biên bản. Sau đó số 4–5 sao có thể đổi ⇒ đối chiếu lại với danh sách của thành phố (10 + 11). |
| m-1 | minor | địa chỉ (12 / 141 dòng) | Địa chỉ chép nguyên danh mục, còn tên huyện / thị xã cũ. Từ 01/07/2025 các đơn vị này đã thôi tồn tại; quy ước của kho (đợt sửa 28/10) là tên phường / xã mới, tên cũ để trong ngoặc. | hoặc đổi theo quy ước, hoặc thêm vào dòng bắt buộc một câu nói rõ địa chỉ lấy theo danh mục nên có thể còn tên đơn vị hành chính cũ. |
| m-2 | minor | bài phía tây | Tên file là "phía tây Kim Long – Thủy Xuân", còn tiêu đề `#` là "… — Phía tây yên tĩnh — Kim Long, Thủy Xuân và vùng lăng" (hai dấu gạch dài, khác tên file và khác 4 bài kia). | thống nhất một kiểu tiêu đề cho cả 5 bài |
| m-3 | minor | đối chiếu 4–5 sao | C không tìm được danh sách 10 + 11 của thành phố trong `data/tra_cuu_cli/`. Việc đối chiếu từng tên chưa làm được. Chênh 2 cơ sở 4 sao có thể một phần do M-1. | sau M-1, một lượt WebFetch trang chính thức của thành phố để đối chiếu tên; không khớp thì ghi rõ trong biên bản. |

## Chưa kiểm
- Chưa chia đoạn lại (dùng số của E: 48 đoạn, 0 lỗi).
- Mới đọc tay 2 / 5 bài; 3 bài còn lại chỉ kiểm bằng code (đếm, lọc, câu mở đầu).

## Kiểm lại (12:24 14/11/2026, `date`) — sửa của E
- **M-1 đóng.** Bảng còn 139 cơ sở. Bài "3–5 sao" ghi 30 khách sạn (10 · 13 · 7), Silk Path chỉ còn 1 dòng 5 sao. Cặp số "I" đã gộp.
  - 5 cặp chung địa chỉ còn lại đều có căn cứ ghi trong biên bản: E so điện thoại / email / số phòng trên trang chi tiết danh mục.
  - Tổng các bài khu khớp bảng: 122 + 5 + 9 + 3 = 139.
- **m-1 đóng:** cả 5 bài có câu "địa chỉ theo danh mục, có thể còn tên đơn vị trước 7/2025".
- **m-2 đóng:** tiêu đề = tên file.
- **m-3 đóng:** E đối chiếu tin thành phố — 5 sao 10 / 10 khớp; 4 sao 10 tên khớp, 1 cơ sở mới công nhận 01/2026 chưa có trong danh mục. Thêm hay không là việc A chọn; bài giữ một nguồn kèm câu "hạng có thể đã đổi".

**Kết luận: ready_for_user_confirmation.**
