# Plan (mức nhẹ, 1 trang) — Lưu trú: "khu nên ở + link tìm chỗ ở do code dựng" · NHÁP bản 2

Người viết: E, 20:47 12/11/2026 (`date`). A giao sau khi User chốt phương án (c) ngày 12/11/2026. **Code chưa làm** — chờ nhánh `p9-het-luot-tim` (cùng file `backend/llm/assistant.py`) merge; C review plan này.
Mức nhẹ: ≤ 0,2 USD, không đổi kiến trúc, **không bộ kín**, đo 1 lượt, 1 review cả nhánh.

**Bản 2 (20:56 12/11/2026, `date`):** sửa theo review của C (`2026-11-12-luu-tru-khu-va-link-plan_review.md`: 1 major, 6 minor) — bảng "Chỗ đổi" cuối file. Mức nhẹ ⇒ A đọc rồi duyệt, không review lại.

## Căn cứ để review
- Quyết định cũ: `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` dòng "Lưu trú (Phase 11, backlog)"; ghi chú nghiên cứu 05/11 (private) `data/phase_11_nghien_cuu/luu_tru/e5_khu_o_va_link.md`.
- Lỗi đã đếm: `report_agent/2026-11-08_phase_9_ban_13/c_dot_2_dem_implementation.md` mục kết quả "Lưu trú".
- Mẫu có sẵn để dùng lại: `backend/llm/lich_trinh.py` (`MAP_BASE`, hàm `ban_do`); `frontend/src/chat.jsx` (`MAP_PREFIX` — giao diện chỉ nhận link đúng gốc này); `backend/api/routes/chat.py` (`_web_payload` — cách đưa một khối dữ liệu riêng ra giao diện).

## 1. Vấn đề (đã đếm) và mục tiêu
Câu "nên ở khu nào": kho trả lời đủ dùng 2 / 2. Câu hỏi **cơ sở lưu trú cụ thể**: 3 / 4 bị kho từ chối, phần web lúc có lúc không (lượt đếm 12/11). Mục tiêu: ở **mọi lượt về lưu trú**, người dùng luôn có một lối đi tiếp — thẻ "Tìm chỗ ở trên bản đồ" với 3 khu nên ở và link Google Maps cho từng khu — dù kho trả lời hay từ chối.

## 2. Quyết định giữ từ 05/11 (không đổi)
- **Không nói giá phòng** (luật `gia_luu_tru` của mục web giữ nguyên; thẻ mới không có số tiền).
- **Link do code dựng**, chỉ gốc `https://www.google.com/maps/search/?api=1&query=` (định dạng có tài liệu chính thức, không cần khoá); chuỗi tìm lấy từ **bảng khu cố định**, **0 chữ của người dùng / model trong URL**. Booking / Agoda / Google Travel: không ở bản này.
- Model **không** viết link, không chọn khu; model chỉ diễn đạt phần kho có (như hôm nay).

## 3. Thay đổi (code quyết; chuỗi gửi model **không đổi** ở cả hai trạng thái cờ)
| Chỗ | Sửa gì |
|---|---|
| `data/phase_11/luu_tru/khu_v1.json` (private, **User duyệt**) | 3 khu lấy đúng từ mục "nên chọn khu vực lưu trú" của kho: tên hiển thị · 1 dòng "hợp với ai" (chép ý kho) · chuỗi tìm Maps cố định · danh sách **mục kho về lưu trú** (file + tiêu đề mục) dùng để nhận lượt — lập **rộng**: mục "nên ở khu nào" **và** mọi mục nêu cơ sở lưu trú trong các bài điểm tham quan (kho có ≥ 6 bài như vậy) |
| `backend/llm/luu_tru.py` (mới, ~60 dòng) | `nap_bang`, `la_luot_luu_tru(documents, cited, bang)`, `the_luu_tru(bang)` ⇒ `[{khu, hop_voi, map_url}]` + `bai_id` của bài kho chứa mục "nên ở khu nào" (thẻ có dòng nguồn mở được bài) (dựng bằng `urllib.parse.quote`) + câu cố định "Kho chưa có danh sách từng cơ sở; bạn xem khu nên ở và tìm trên bản đồ" |
| `backend/llm/assistant.py` | `AssistantFlags.luu_tru: bool = False` (+ nạp bảng ở `from_settings`); `AnswerTrace.luu_tru`; một lời gọi sau khi có câu trả lời kho (cạnh `set_notice`) ở cả ba đường (không stream, stream, stream song song). Không chạm `_before_model`, lời dặn, công cụ |
| `backend/api/routes/chat.py` | trường `luu_tru` trong `ChatResponse` + sự kiện SSE `luu_tru` sau `sources` / `web`; log `chat_metrics` thêm `co_the_luu_tru` (0 / 1, không chữ) |
| `backend/config/settings.yaml`, `api/routes/cong.py` | cờ `luu_tru: false` + đường dẫn bảng; `/api/tinh_nang` báo cờ |
| `frontend/src/chat.jsx` | thẻ dưới câu trả lời: 3 dòng khu + link (lọc `MAP_PREFIX` như thẻ lịch; `target=_blank rel="noopener noreferrer"`); nhãn "mở Google Maps — không phải gợi ý cơ sở cụ thể" |

## 4. Khi nào hiện thẻ — bước 0 chọn giữa: theo nguồn · từ khoá · HỢP hai cách (bản 2)
- **Cách 1 (khuyến nghị) — theo NGUỒN KHO, code tất định:** lượt là "về lưu trú" khi trong **nguồn được trích** có mục thuộc danh sách mục lưu trú của bảng; lượt bị kho từ chối thì xét **k đoạn đầu của lần tìm đầu** (k ghi ở bước 0). Không đọc chữ người dùng, không thêm lần gọi model, chuỗi gửi model giống byte. *Khi nào sai:* câu về phố Tây / Lăng Cô không hỏi chỗ ở mà vẫn kéo mục lưu trú lên đầu ⇒ thẻ hiện thừa (vô hại nhưng nhiễu) — bước 0 đếm trước. *Chọn khác mất gì:* không bắt được câu lưu trú mà tầng tìm không kéo được mục lưu trú nào.
- **Cách 2 — NHÃN DO MODEL:** thêm trường `chu_de` vào đầu ra có cấu trúc của lần định tuyến. Bắt theo nghĩa, không phụ thuộc tầng tìm. *Mất gì:* đổi lời dặn định tuyến ⇒ không còn giống byte ⇒ phải chạy lại hồi quy định tuyến (Golden 176 chỉ định tuyến ×2 + bộ tuyến) ≈ 0,05 USD + nửa buổi; vượt mức nhẹ.
- **Cách 3 — TỪ KHOÁ có sẵn `tra_web.la_cau_luu_tru`** (đang chạy cho luật giá của mục web). C đọc 6 câu lưu trú của lượt 12/11: từ khoá khớp 3 / 3 câu cơ sở cụ thể bị kho từ chối; cách 1 (theo nguồn trích) chỉ chắc ở 2 câu "khu nào" vốn đã ổn, 3 câu bị từ chối có 0 nguồn trích nên phụ thuộc k đoạn đầu (chưa đo).
- **Được phép chọn "HỢP" (cách 1 HOẶC cách 3)** nếu bước 0 cho thấy tốt hơn: thẻ chỉ là **hiển thị** — chữ người dùng không vào URL, không vào chuỗi gửi model, không đổi câu trả lời ⇒ từ khoá ở đây không mang rủi ro của "định tuyến bằng từ khoá" (thứ dự án đã bỏ). *Khi nào sai:* câu có chữ "khách sạn" nhưng hỏi việc khác (vd lịch sử một toà nhà) ⇒ thẻ thừa — L2 đếm.

## 5. Bước 0 — đếm 0 USD trước khi code (quyết k, hoặc dừng)
**6 câu mới viết xong và khoá TRƯỚC bước 0** (người viết ≠ E). Chạy **chỉ tầng tìm** (không gọi model) trên: 12 câu lưu trú (mục 6) · Golden 176 · an toàn 32 · ngoài phạm vi 44. Ghi bảng: với k = 3 / 5 / 10, bao nhiêu câu lưu trú có mục lưu trú trong k đoạn đầu; bao nhiêu câu thường dính. **Báo riêng 4 câu cơ sở cụ thể đã đếm 12/11** với ba cột đặt cạnh nhau: theo nguồn (k = 3 / 5 / 10) · từ khoá · hợp. **Chọn phương án đơn giản nhất** (ưu tiên: theo nguồn với k nhỏ nhất ⇒ hợp ⇒ từ khoá) đạt L1, L1b, L2; không phương án nào đạt ⇒ dừng, báo A (xét cách 2).

## 6. Tiêu chí ghi trước
| # | Tiêu chí | Bộ | Mức |
|---|---|---|---|
| L1 | Lượt lưu trú có thẻ | 12 câu tiếng Việt = 4 câu cơ sở cụ thể + 2 câu "khu nào" của lượt đếm 12/11 + **6 câu mới** (người viết ≠ người code; loại: theo khu, theo người đi cùng, gần một điểm, loại hình) | ≥ 10 / 12 |
| **L1b** | **Đúng loại lỗi đã đếm** | 4 câu cơ sở cụ thể của lượt 12/11 | **≥ 3 / 4** có thẻ |
| L1c (báo riêng, không vào luật) | câu tiếng Anh | 1–2 câu | ghi có / không |
| L2 | Câu thường **không** dính thẻ | Golden 158 câu trong kho + an toàn 32 (đếm bằng code trên tầng tìm + nguồn trích của lượt B7 giữa kỳ, 0 USD) | ≤ 3 / 190, và 0 câu an toàn |
| L3 | Ngoài phạm vi không có thẻ | 44 câu đã thấy | 0 (câu cố định ngoài phạm vi ⇒ code không xét) |
| L4 | Link | mọi thẻ sinh ra + test ca chữ lạ (`../`, `?`, `&`, có dấu) | 100 % đúng gốc Maps; 0 ký tự từ câu hỏi trong URL; 0 số tiền trong thẻ |
| L5 | Chuỗi gửi model | Q1 hiện có | giống byte cả khi cờ **bật** lẫn tắt ⇒ **không** chạy lại Golden / an toàn có phí (luật spec §4: chuỗi không đổi ⇒ dùng lại số) |
| L6 | Lượt thật qua server, cờ bật | 12 câu, **một trạng thái** (chuỗi gửi model giống byte ⇒ so bật ↔ tắt chỉ đo nhiễu model) | sự kiện `luu_tru` đến sau `sources` / `web`; thẻ đúng L4; 0 lỗi; `chat_metrics.co_the_luu_tru` = số thẻ |
| L7 | Test theo **loại lượt** (0 USD) | 5 ca: kho trả lời có trích mục lưu trú · kho từ chối + web có mục · kho từ chối + web không mục · câu ngoài phạm vi · lượt biểu mẫu lịch trình **1 ngày** · lượt biểu mẫu lịch trình **≥ 2 ngày** | thẻ: có · có · có · không · không · **có** |

## 7. Rà khung AI FDE (ngắn)
| Mục | Hiện trạng / thiết kế | Khớp? |
|---|---|---|
| Có cần model không | không — bảng + luật theo nguồn; model không thêm việc | khớp |
| Việc phải đúng ⇒ code | chọn khu, dựng URL, câu cố định, cấm giá | khớp |
| Chữ người dùng là dữ liệu | không vào URL, không vào bảng | khớp |
| Đường ra mới | chỉ link người dùng tự bấm tới Google Maps (đã có ở thẻ lịch); server không gọi ra ngoài; CSP không đổi | khớp |
| Dữ liệu cá nhân | bảng 3 khu, không cơ sở, không người | khớp |
| Đo hai chiều | L1 (có khi cần) ↔ L2 / L3 (không khi không cần) | khớp |
| Phục hồi | bảng thiếu / hỏng ⇒ cờ coi như tắt, log một dòng; không chặn câu trả lời | khớp |

## 8. Tiền · giờ · ai
- Tiền: bước 0 = 0; L6 = 12 câu × 1 trạng thái × ≈ 0,0013 ≈ **0,015 USD**; dự phòng 0,02 ⇒ **≤ 0,04** (Phase 11 / quỹ chung — A ghi).
- Giờ (ước thô): bảng + bước 0 ~30 phút · code + test ~1,5 giờ · giao diện + Playwright một khổ màn ~45 phút · đo + report ~30 phút.
- Người viết 6 câu mới: C hoặc B (không phải người code). Review cả nhánh: C.
- **User cần duyệt:** bảng `khu_v1.json` (3 khu + câu "hợp với ai" + chuỗi tìm Maps) trước khi bật cờ.

## 8b. Bổ sung 20:51 12/11/2026 — số người + ngày nhận / trả phòng trên link (User hỏi; hướng mặc định của A)

- **Nguyên tắc:** số người và ngày là **tham số của link do code dựng**; trợ lý **không nói giá phòng, không cộng tiền phòng vào bất kỳ đâu** (kể cả dòng dự toán của lịch trình). Giá do trang đích hiện.
- **Vướng phải quyết trước khi code:** link Google Maps (đích duy nhất của bản 1) **không mang được** ngày / số người. Muốn mang thì cần đích thứ hai. Hai lựa chọn cho User (A hỏi, một câu):
  - **(a) — khuyến nghị cho bản 1: chỉ Maps, link theo khu.** Ổn định (tài liệu chính thức), không rủi ro tham số. *Mất gì:* người dùng tự nhập ngày / số người ở trang họ chọn.
  - **(b) Thêm một link Booking.com** bên cạnh link Maps **chỉ khi lượt đã có đủ ngày nhận + ngày trả** (thiếu ⇒ chỉ link Maps theo khu). Tham số `ss` (tên khu lấy từ bảng) · `checkin` · `checkout` · `group_adults` · `no_rooms=1` · `lang=vi`. *Khi nào sai:* tham số là dạng quan sát được, không có tài liệu chính thức ⇒ có thể đổi âm thầm; cần một test Playwright "chỉ kiểm `href`" + kiểm tay định kỳ. *Tốn thêm:* ~1 giờ code + gốc cho phép thứ hai ở giao diện.
- **Nếu chọn (b) — ai điền tham số (đều là code):**
  - **ngày + số người từ biểu mẫu "Lên kế hoạch"** (giá trị nút / ô đã chọn) — nguồn tin cậy nhất; biểu mẫu hiện có `so_ngay`, `di_cung` nhưng **chưa có ô ngày đi và số người** ⇒ thêm ô là đổi giao diện biểu mẫu (ngoài mức nhẹ, tách việc);
  - **code dò trong câu gõ:** số ngày đã có bộ dò (`backend/llm/do_so.py`); ngày cụ thể dùng lịch code tính sẵn (`ngay_lich`); số người cần bộ dò mới (số + "người / người lớn / khách") — dò không chắc ⇒ **bỏ tham số đó**, không đoán;
  - kiểm bằng code: ngày nhận < ngày trả, không ở quá khứ, ≤ 30 đêm, 1–10 người; sai ⇒ rơi về link theo khu.
- **Nếu User chọn (b): tách thành việc riêng** (plan riêng sau bản 1 — khớp mục 9 "không làm ở bản này"). Tiêu chí dự kiến: B1 — 100 % link Booking đúng gốc `https://www.booking.com/searchresults.html?`, mọi giá trị qua `urlencode`, 0 chữ tự do của người dùng (chỉ số / ngày đã chuẩn hoá + tên khu từ bảng); B2 — lượt thiếu ngày ⇒ 0 link Booking; B3 — 0 số tiền trong thẻ và trong chữ trả lời do thẻ thêm.

## 9. Không làm ở bản này
Danh sách cơ sở lưu trú trong kho (chờ quyết định nguồn dữ liệu — `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` mục lưu trú); link đặt phòng điền sẵn ngày / người; gợi ý khu theo người đi cùng (cần bảng lớn hơn).

## Chỗ đổi bản 2 (theo review của C)

| Finding | Sửa ở |
|---|---|
| M-1 cách kích hoạt chưa chắc bắt đúng loại lỗi đã đếm | mục 4 (thêm cách 3 + cho phép "hợp"), mục 5 (bước 0 báo riêng 4 câu cơ sở cụ thể, ba cột), mục 6 (L1b ≥ 3 / 4), mục 3 (danh sách mục lưu trú lập rộng) |
| L6 so bật ↔ tắt chỉ đo nhiễu | L6 một trạng thái; tiền ≤ 0,04 |
| 6 câu mới viết trước bước 0 · câu tiếng Anh để riêng | mục 5, L1, L1c |
| 5 ca test theo loại lượt | L7 |
| 8b (b) mâu thuẫn mục 9 | 8b: chọn (b) ⇒ tách việc |
| thẻ kèm dòng nguồn | mục 3 (`bai_id`) |

**Sửa sau duyệt (21:20 12/11/2026, A quyết):** thêm **đường kích hoạt thứ hai** — lượt biểu mẫu lịch trình từ **2 ngày** trở lên ⇒ code gắn thẻ (quyết theo số ngày của biểu mẫu, không qua nguồn kho / từ khoá); lịch 1 ngày không thẻ. Đổi L7 (5 ca ⇒ 6 ca). Không đổi tiền, không đổi tiêu chí khác ⇒ không duyệt lại.

**Sửa sau duyệt (21:37 12/11/2026):** bảng `khu_v1.json` thêm trường `cum` cho mỗi khu = danh sách cụm của bảng điểm thuộc khu đó (ánh xạ 8 cụm ⇒ 3 khu, dùng chung cho thẻ dưới lịch — spec biểu mẫu của C — và bài lưu trú theo khu — spec kho 3). User duyệt cùng bảng. Không đổi tiêu chí, tiền.
