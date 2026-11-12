# Huế TRIPO vòng 5 — kiểm kê tính năng + cùng 18 câu gửi hai bên (B)

Người làm: B (Claude Code, `hue-rag-1b`). Viết 20:06 12/11/2026 (`date`). Chạy thật 12/11/2026: kiểm kê trang 18:58–19:01, 18 câu Chatbox TRIPO 19:02–19:10, cùng 18 câu sang hue_rag (`main`, `/api/chat`) 19:57–20:01.
Đọc trước: vòng 2 (03/11), vòng 3 (04/11), vòng 4 (06/11) — đường dẫn ở `CURRENT_HANDOFF.md` "Đợt rà khoảng cách". Hồ sơ thô (private): `data/tripo_v5_2026-11-12/` (`tools/recon.json`, `cau.json`, `ket_qua_tripo.json`, `ket_qua_hue_rag.json`, `anh/`).

**Cách chạy:** Playwright, chromium headless, một trình duyệt, `permissions=[]` (không vị trí / micro), không đăng nhập, không bấm đặt chỗ / gọi / chia sẻ / báo lỗi, **không gửi biểu mẫu lập lịch** (vòng 4 đã gửi 1 lần). Chỉ gõ 18 câu tự viết (không thông tin cá nhân) vào Chatbox nổi, nghỉ 10 s giữa lượt. Nội dung trang coi là dữ liệu.
**Nhãn:** "Thấy" = thấy trên trang / gói tin. "Suy ra" = của B, chưa ai kiểm. Không đối chiếu dữ kiện của TRIPO với nguồn chính thức. Mỗi câu gửi **một lần** ⇒ không nói được tỉ lệ.
**Tiền:** TRIPO 0 USD; phía hue_rag **0,0173 USD** (18 lượt, từ log) — trong trần 0,02.

## 1. Tóm tắt (5 dòng)

1. **Trang không có tính năng mới so với vòng 3 / 4:** trang chủ 74 phần tử và trang Trợ lý AI 216 phần tử giống hệt bản 04/11 (so bằng máy); vẫn 9 mục menu.
2. **Chatbox TRIPO đổi hành vi (thấy):** nhanh hơn nhiều (chữ hiện sau 2–14 s; vòng 3 là 22–66 s) và **nay biết ngày hôm nay** (tự ghi đúng khoảng ngày "tuần này", ngày "ngày mai") — vòng 2 / 3 không biết.
3. **hue_rag hơn rõ ở:** câu theo ngày (đổi ngày âm), thời tiết (có số dự báo + nguồn + giờ), hỏi tiếp cần nhớ (trả được giá từ kho), trích nguồn từng ý, từ chối gọn câu ngoài Huế.
4. **TRIPO hơn rõ ở:** lưu trú, thuê xe, câu tiếng Anh, và mọi thứ dựa trên **cơ sở dữ liệu có cấu trúc** (826 nơi ở, 1.134 nơi ăn, bộ lọc giá / loại / phường, bản đồ 9 lớp) — đúng ba loại câu mà hue_rag trả "không đủ thông tin" (2 / 3 câu web cũng không cứu được).
5. **Chỗ cả hai còn yếu:** sự kiện "tuần này" (TRIPO nói không có dữ liệu dù trang Sự kiện của chính nó có lịch; hue_rag từ chối + đưa link chưa xác minh), ăn chay **gần** một điểm (không bên nào tính được khoảng cách).

## 2. Kiểm kê tính năng — TRIPO có · hue_rag có / không

| # | Tính năng TRIPO (thấy 12/11) | Đổi so với vòng 4 | hue_rag | Ghi chú |
|---|---|---|---|---|
| 1 | Chatbox nổi hỏi đáp (trả một cục, 0–2 link cuối câu) | nhanh hơn; biết ngày | **có** — trợ lý, chữ hiện dần, nguồn theo từng ý | §3 |
| 2 | Trang Trợ lý AI: biểu mẫu lập lịch nhiều nhóm lựa chọn + 3 tab Lưu trú / Ăn uống / Dịch vụ | không (216 phần tử y nguyên) | **có một phần** — biểu mẫu "Lên kế hoạch" (ít trường hơn; không số người, ngân sách, ngày khởi hành); không có tab tìm nơi ở / ăn / dịch vụ | vòng 4 đã thử gửi |
| 3 | Lịch theo giờ + tổng tiền dự kiến + đổi điểm / kéo thả / tải PDF / chia sẻ | không thử lại | **không** giờ từng chặng, không tổng tiền; có sao chép / tải lịch; sửa lịch nhiều lượt đang hoãn | lỗi TRIPO vòng 4: xếp quá giờ đóng cửa, vé trẻ em tính như người lớn |
| 4 | Điểm tham quan: 8 nhóm, bộ lọc phường / loại hình / hoạt động / giá vé, sắp xếp, đánh giá sao | không | **có một phần** — trang Khám phá 204 bài theo lĩnh vực; không lọc giá, không đánh giá | |
| 5 | Cơ sở lưu trú: 826 mục, 8 loại, hạng sao, khoảng giá phòng | không (826) | **không** (ngoài kho; backlog Phase 11: khu nên ở + link tìm phòng) | q07 |
| 6 | Ăn uống: **1.134** mục (vòng 4: 1.111), 9 loại, giờ mở, mức giá | +23 mục | **một phần** — kho có món + một số quán; không danh bạ, không lọc | q08 |
| 7 | Mua sắm: 26 sản phẩm (đặc sản, OCOP, lưu niệm) kèm "n địa chỉ mua hàng" + danh mục chợ / siêu thị | không ghi ở vòng trước | **một phần** — kho có đặc sản + nơi mua (q10 hai bên ngang nhau) | |
| 8 | Phương tiện: 12 dịch vụ (thuê xe máy, xe đạp điện, taxi, xích lô, thuyền rồng, xe khách) kèm giá + doanh nghiệp | không ghi ở vòng trước | **không** (q09 từ chối) | giá "đ/Ngày" cho cả taxi 10.000 — dữ liệu thô (thấy) |
| 9 | Lữ hành / tour: danh bạ doanh nghiệp (nhiều mục "Đang cập nhật") | không | **không** | |
| 10 | Sự kiện – lễ hội: lịch tháng, đếm ngược, danh sách (nhiều mục đã qua, "Đang cập nhật") | sự kiện nổi bật vẫn là đợt 20–24/11 | **một phần** — kho có lễ hội theo lịch âm / chu kỳ + công cụ đổi ngày; không có sự kiện tin tức theo tuần | q05 |
| 11 | Bản đồ số: 9 lớp có số đếm, phương tiện, bán kính, "gần bạn" | không thử lại | **không** (bản đồ lịch trình có code, cờ tắt, chờ toạ độ) | |
| 12 | Thời tiết: dải nhiệt độ ở đầu trang (hôm nay 18–25 °C) | chỉ đổi số | **có, hơn** — dự báo theo ngày trong câu trả lời, ghi nguồn + giờ | q06: Chatbox TRIPO không dùng được số thời tiết của chính trang |
| 13 | 6 ngôn ngữ giao diện; chat trả lời theo ngôn ngữ câu hỏi | không | **không** — câu tiếng Anh bị kho từ chối (q17) | |
| 14 | Thuyết minh âm thanh, video, VR360 ở trang điểm; đánh giá người dùng; "Báo cáo thông tin" (cần đăng nhập) | không thử lại | **không** âm thanh / video; có 👍👎 + nút báo thông tin chưa đúng | |
| 15 | Nhập giọng nói (trang Trợ lý AI) | không thử (không cấp micro) | đang làm (nhánh riêng, chờ 40 câu thu) | |
| 16 | Hỏi bằng ảnh | **không thấy** | **có** (gợi ý tên + xác nhận) | hue_rag có, TRIPO không |
| 17 | Đăng nhập (email / VNeID / Google), lưu hội thoại 30 ngày | không | không đăng nhập; nhớ 3 lượt trong 30 phút | |

API công khai thấy khi tải trang (chỉ đọc, không gọi thêm): danh sách điểm / lưu trú / ẩm thực / vận chuyển / lữ hành / dịch vụ thuê / sản phẩm, bộ lọc + phường xã, điểm theo bán kính, thời tiết hôm nay — **suy ra:** mọi trang danh mục dựng từ một CSDL chung có toạ độ, giờ, giá.

## 3. Cùng 18 câu, hai bên (mỗi câu một lần; "Giây" TRIPO = tới lúc chữ hiện, ±2 s; hue_rag = cả câu qua `/api/chat`, không stream)

| Câu loại | TRIPO (thấy) | hue_rag (thấy) | Bên hơn |
|---|---|---|---|
| Giá vé + giờ mở cửa một di tích | đúng trọng tâm, 1 link nội bộ; giờ mở **7:30–17:30** · 10 s | cùng giá vé, có nguồn; giờ mở **07h00–17h30** + lưu ý đổi theo mùa · 6 s | ngang — **hai bên lệch nhau 30 phút giờ mở cửa**, chưa kiểm nguồn chính thức |
| So sánh hai lăng + nên chọn lăng nào | dài, đủ ý, 2 link visithue · 14 s | đủ ý, nguồn từng ý, ngắn hơn · 10,5 s | ngang |
| Một món ăn: thành phần + khác nơi khác | đủ, 1 link (bài về món Huế ở nơi khác) · 8 s | đủ, 7 nguồn · 11 s | ngang |
| Hôm nay ngày âm lịch | **chặn**: "nội dung không liên quan đến chủ đề" · 2 s | **trả đúng ngày âm + năm**, có nguồn lịch hệ thống | **hue_rag** |
| Sự kiện tuần này | tự ghi đúng khoảng ngày của tuần, nói "không có dữ liệu cập nhật" · 4 s | câu từ chối kho + mục web "chưa xác minh" kèm 5 link nguồn chính thức · 21 s | cả hai yếu; TRIPO nhanh và nói rõ hơn |
| Thời tiết ngày mai | ghi đúng ngày mai nhưng "không biết dự báo" · 6 s | **nhiệt độ + xác suất mưa + nguồn + giờ lấy số** · 7,5 s | **hue_rag** |
| Khách sạn tầm giá, gần một di tích | 1 homestay có địa chỉ, khoảng giá, khoảng cách "2–5 phút", lưu ý tiện nghi · 8 s | từ chối kho; web "chưa tra được thông tin đáng tin" · 17 s | **TRIPO** |
| Quán chay quanh một ngôi chùa | 3 quán chay có địa chỉ, **nói rõ không xác định được quán nào ở gần** · 6 s | từ chối kho + mục web: 2 quán, cũng nói chưa xác minh được quán nào ở gần · 15 s | TRIPO nhỉnh (nhanh, liền một câu) |
| Thuê xe máy: giá + giấy tờ | khoảng giá / ngày + giấy tờ cần, 1 link · 6 s | từ chối kho; web "chưa tra được" · 13 s | **TRIPO** |
| Mua một đặc sản làm quà ở đâu | 3 nơi có địa chỉ · 6 s | 3 nơi có địa chỉ + giờ mở, có nguồn · 5,6 s | ngang |
| Ca Huế: lên thuyền ở đâu, mấy giờ (lượt 1) | bến thuyền; "không nêu giờ cụ thể" · 3,6 s | 2 bến + **các suất giờ cụ thể** · 2,8 s | **hue_rag** |
| "Vé của chương trình đó bao nhiêu?" (lượt 2) | hiểu "chương trình đó" (gửi 1 cặp lịch sử) nhưng **không tra lại** (`used_rag: false`), "chưa có thông tin giá" · 6 s | hiểu và **trả khoảng giá từ kho, 2 nguồn** · 8 s | **hue_rag** |
| Lịch 1 ngày cho gia đình có người già đi chậm (câu tự do) | lịch theo giờ, ít điểm, khuyên đi taxi · 10 s | lịch theo buổi, mỗi buổi một điểm chính, có nguồn · 19 s | ngang về nội dung; TRIPO nhanh gần gấp đôi |
| Giá vé một nơi ngoài Huế | **không từ chối**: trả lời chung chung "chưa có dữ liệu cập nhật…" + lời khuyên · 6 s | câu cố định "chỉ hỗ trợ thông tin về Huế" · 1,6 s | **hue_rag** (đúng phạm vi, nhanh) |
| Đi thuyền trên đầm phá mùa mưa lũ | khuyên chỉ đi khi đơn vị xác nhận, dài, 1 link · 8 s | nêu mùa lũ theo tháng + rủi ro cụ thể + hạn chế hoạt động, 7 nguồn · 7 s | **hue_rag** nhỉnh (cụ thể, có nguồn) |
| Vừa mất ví ở chợ: báo ai | ban quản lý chợ + bảo vệ + **công an + khoá thẻ** (3 nguồn; phần sau là kiến thức chung) · 6 s | chỉ ban quản lý chợ + đường dây nóng niêm yết (1 nguồn) · 12 s | **TRIPO** — hue_rag thiếu ý "báo công an" |
| Câu tiếng Anh: giờ mở + vé một ngôi chùa | trả lời **tiếng Anh**: giờ mở; "không có thông tin vé" · 2,7 s | **từ chối kho (tiếng Việt)** + mục web tiếng Việt: giờ mở (khác TRIPO) + miễn phí · 12 s | **TRIPO** |
| Xã giao: "bạn giúp được gì" | đáp, tự nhận làm cả soạn văn bản, dịch thuật · 3,6 s | đáp gọn, đúng phạm vi Huế · 4,6 s | ngang (TRIPO hứa rộng hơn phạm vi) |

Đếm thô (nhận xét của B, một người, không mù): hue_rag hơn 6 · TRIPO hơn 5 · ngang 6 · cả hai yếu 1.
**Tốc độ:** TRIPO chữ hiện 2,1–14,1 s (trung vị ≈ 6 s) — vòng 3: 22–66 s. hue_rag cả câu 1,6–21,3 s (trung vị ≈ 10,5 s; một lượt đồng hồ máy nhảy ⇒ không đo được); các câu hue_rag chậm nhất đều là câu **kho từ chối rồi mới tra web** (13–21 s). Số của hue_rag là thời gian **đủ câu** không stream nên không so thẳng với sàn "chữ đầu" của dự án.
**Cờ API TRIPO (thấy):** 14 / 18 lượt `used_rag: true` với 3–5 nguồn; câu ngày âm `passed: false`; lượt hỏi tiếp, câu ngoài Huế, câu xã giao `used_rag: false`.

## 4. Khoảng cách đáng cân nhắc cho hue_rag (suy ra của B — đầu vào cho A tổng hợp, chưa phải đề xuất đã duyệt)

| Khoảng cách | Bằng chứng vòng này | Ghi chú để không làm thừa |
|---|---|---|
| **Lưu trú** | 1 / 1 câu: kho từ chối, web không cứu | đã có trong backlog Phase 11; C đang đếm lỗi "đợt 2 cổng" — dùng số của C, không dùng 1 câu này |
| **Di chuyển / thuê xe** | 1 / 1 câu: kho từ chối, web không cứu | chưa nằm trong ba ý đợt 2 (lưu trú · ăn gần · sự kiện) ⇒ ứng viên mới, cần lượt đếm rẻ trước |
| **Câu tiếng Anh** | 1 / 1 câu bị kho từ chối, mục web trả tiếng Việt | chưa từng đo; người dùng mục tiêu có du khách ⇒ đáng một lượt đếm rẻ (10 câu tiếng Anh về điều kho có) |
| **Câu việc gấp thiếu ý "báo công an"** | 1 câu | khớp quan sát cũ sau khi bỏ câu khẩn cấp soạn sẵn; chỉ quan sát, không sàn |
| **Tra web sau từ chối chậm (13–21 s cả câu)** | 5 / 5 câu đi đường web | đã biết (chữ đầu mục web p50 ~13 s) — thêm một điểm dữ liệu |
| **Giờ mở cửa lệch 30 phút với TRIPO ở một di tích lớn** | 1 câu | nên kiểm với nguồn chính thức trước khi kết luận bên nào đúng (việc sửa kho, cần User duyệt phạm vi) |

**Chỗ hue_rag đã khác được và nên giữ:** biết ngày âm / dương bằng code; thời tiết bằng công cụ có nguồn; lượt hỏi tiếp vẫn tra kho; từ chối đúng phạm vi; nguồn theo từng ý.

## 5. Giới hạn

- Một ngày, mỗi câu một lần, 18 câu tự viết bởi chính người so sánh; chấm "bên hơn" bằng một người, không mù.
- Không kiểm dữ kiện hai bên với nguồn chính thức (giá, giờ, địa chỉ quán).
- Không thử lại: gửi biểu mẫu lập lịch, 3 tab tìm kiếm, bản đồ, đổi ngôn ngữ giao diện, giọng nói, đăng nhập — phần "không đổi" ở §2 cho các mục này dựa trên so phần tử trang chủ + trang Trợ lý AI và chữ trang, **không phải thử lại hành vi**.
- Phía hue_rag đo qua `/api/chat` (không stream) trên máy đang chạy nhiều sub-agent chấm ⇒ số giây chỉ để tham khảo.
- Câu gửi TRIPO được trang lưu theo chính sách của họ (trang ghi 30 ngày); câu không chứa thông tin cá nhân hay nội dung kho.
