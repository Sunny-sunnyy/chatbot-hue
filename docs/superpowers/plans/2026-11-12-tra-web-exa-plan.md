# Plan (mức nhẹ, 1 trang) — đưa Exa vào bước tra web sau cờ · NHÁP bản 1, chờ A duyệt

Người viết: E · 21:15 12/11/2026 (`date`). Căn cứ: thí nghiệm 12/11 — `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` mục 5–6 (Exa 25 ↔ Serper 17 / 42 câu, sàn 0, p95 2,2 s); User: "nếu Exa tốt hơn thì dùng Exa" (A báo 12/11). C review kết quả thí nghiệm; plan này mức nhẹ ⇒ A đọc rồi duyệt.

## 1. Thay đổi (chỉ nguồn của sổ web; lời dặn, cổng mở, luật kiểm giữ nguyên)
| Chỗ | Sửa gì |
|---|---|
| `backend/llm/tra_web.py` | thêm `tim_web_exa(cau, *, api_key, timeout, transport=None) -> KetQuaWeb` cạnh `tim_web` (Serper): `POST https://api.exa.ai/search`, `type "auto"`, `numResults 5`, `userLocation "VN"`, `contents.highlights.maxCharacters 400`; sổ web **cùng khuôn** (đoạn trích = các highlights nối lại, cắt 400); tiền lấy từ `costDollars.total` của phản hồi; lỗi / hết giờ / 0 kết quả xử như Serper. Module này vẫn là nơi **duy nhất** gọi ra web |
| `backend/api/app.py` `_tim_web_server` | chọn nguồn theo cấu hình: `exa` ⇒ gọi Exa; **Exa lỗi / hết giờ / 0 kết quả ⇒ gọi Serper một lần** với phần thời gian còn lại của hạn 5 s (không còn thời gian ⇒ thôi). Khoá đọc trong hàm như hiện nay |
| `backend/config/settings.yaml` + `core/settings_loader.py` | `assistant.tra_web_nguon: serper` (mặc định — **cờ tắt = như hôm nay**) / `exa`; `assistant.tra_web_exa_moi_ngay: 150` (trần lượt Exa / ngày, đếm trong RAM; vượt ⇒ dùng Serper); biến môi trường `HUE_TRA_WEB_NGUON` cho bản Docker |
| log `chat_metrics` | mục `tra_web` trong `tools` thêm `nguon` (`exa` / `serper` / `exa>serper`), không chữ |
| test | phản hồi Exa ghi sẵn (qua `transport`): khuôn sổ, cắt 400, link không hợp lệ bị bỏ, lỗi 401 / 402 / 429 / hết giờ ⇒ "loi", dự phòng sang Serper đúng một lần, trần / ngày; test ranh giới: chỉ `tra_web.py` có địa chỉ Exa |

## 2. Thay hay đứng trước Serper — khuyến nghị: **Exa trước, Serper dự phòng**
- *Vì sao:* Exa hơn rõ khi chạy được (25 ↔ 17); gói miễn phí có hạn (10 USD / tháng ≈ 1.400 lượt) và có thể hết tín dụng (mã 402) ⇒ cần đường lùi tự động về thứ đang chạy ổn.
- *Khi nào sai:* dự phòng làm lượt web chậm thêm khi Exa hết giờ (đã chặn bằng ngân sách thời gian chung 5 s).
- *Chọn khác mất gì:* "chỉ Exa" đơn giản hơn nhưng hết tín dụng là mất mục web; "gọi cả hai rồi gộp" chỉ thêm 2 / 42 câu mà tốn gấp đôi.
- **Không dùng** `excludeDomains` (cấu hình có lọc kém hơn ở thí nghiệm).

## 3. Tiền + hạn mức
- Mỗi lượt web: tra 0,001 ⇒ **0,007 USD** (model viết mục ≈ 0,0002 không đổi) ⇒ lượt có web ≈ 0,0018 ⇒ ≈ 0,008 USD. Chỉ lượt kho từ chối mới tra.
- Trần 150 lượt Exa / ngày ≈ 1,05 USD / ngày tối đa; trong gói miễn phí ≈ 47 lượt / ngày — **User quyết có nạp tiền Exa khi deploy không** (không nạp ⇒ hết tín dụng thì tự về Serper).
- Tiền đo của plan này: ≈ **0,05 USD** thật + ≈ 0,5 USD tín dụng Exa.

## 4. Tiêu chí ghi trước (đo 1 lượt, cờ `exa`)
| # | Tiêu chí | Bộ | Mức |
|---|---|---|---|
| X1 | Cờ mặc định ⇒ không đổi gì | test + Q1 | chuỗi gửi model giống byte; lượt web vẫn gọi Serper |
| X2 | Sàn mục web như B6 | 28 câu web đã thấy + 12 câu lưu trú / ăn gần, qua **server thật** | 0 link ngoài sổ · 0 số / tiền ngoài đoạn trích lọt ra · câu thiên tai cố định · câu lưu trú 0 giá · câu ngoài Huế 0 mục web · 0 truy vấn chứa tên (3 chuỗi nêu tên) |
| X3 | Không làm hỏng an toàn | an toàn 32 ×1 (chỉ các câu kho từ chối mới đi web) | 4 số như mọi bậc; ca mới ⇒ thủ tục sinh lại, hai người chấm cùng gắn |
| X4 | Tốc độ | cùng lượt X2 | từ gửi tới sự kiện `web`: p50 không chậm hơn mốc Serper cùng buổi quá 1 s; tra p95 ≤ 5 s |
| X5 | Dự phòng | test + 1 lượt thật với khoá Exa cố ý sai (qua biến môi trường của tiến trình thử, không sửa `.env`) | lượt đó có mục web từ Serper, log `nguon: exa>serper` |
| X6 | Lặp lại được lợi ích | 20 câu B6 loại cần web, chấm mù 2 người | Exa ≥ Serper cùng buổi (không cần +5 lần hai; thấp hơn ⇒ dừng, báo A) |

## 5. Rà khung AI FDE (ngắn) — đường ra mới
| Mục | Thiết kế | Ghi chú cho User |
|---|---|---|
| Dữ liệu gửi ra | câu hỏi lượt này đã bỏ email / số điện thoại, cắt 120 ký tự, thêm " Huế" — **như đang gửi Serper** | **Exa ghi trong chính sách riêng tư (29/06/2026) rằng truy vấn được dùng để cải thiện sản phẩm, kể cả huấn luyện**; chế độ không lưu chỉ có ở gói doanh nghiệp. User đã duyệt Exa; nêu lại để quyết lúc deploy công khai |
| Chữ web là dữ liệu | đoạn trích Exa dài hơn (≤ 400 ký tự × 5) ⇒ nhiều chữ lạ hơn vào model viết mục | model viết mục **không có công cụ**; mọi link do code dựng; luật kiểm số / tiền / link giữ nguyên ⇒ rủi ro không đổi loại, X2 đo |
| Khoá | `EXA_API_KEY` đọc trong hàm, không log, không vào `repr` | — |
| Hạn mức / lạm dụng | trần lượt / ngày bằng code + giới hạn lượt / IP sẵn có | — |
| Phục hồi | lỗi ⇒ Serper ⇒ câu cố định | — |

## 6. Giờ · ai
Code + test ~1,5 giờ · đo + chấm ~1 giờ. Làm sau khi nhánh "hết lượt tìm" merge (cùng vùng tra web / vòng công cụ). Người code: E; review cả nhánh: C hoặc B.
