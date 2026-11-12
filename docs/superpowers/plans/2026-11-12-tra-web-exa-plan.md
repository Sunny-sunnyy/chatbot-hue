# Plan (mức nhẹ, 1 trang) — đưa Exa vào bước tra web sau cờ · NHÁP bản 2, chờ A duyệt

Người viết: E · 21:15 12/11/2026 (`date`). Căn cứ: thí nghiệm 12/11 — `report_agent/2026-11-12_ra_khoang_cach/e_tim_web_serper_exa.md` mục 5–6 (Exa 25 ↔ Serper 17 / 42 câu, sàn 0, p95 2,2 s); User: "nếu Exa tốt hơn thì dùng Exa" (A báo 12/11). C review kết quả thí nghiệm; plan này mức nhẹ ⇒ A đọc rồi duyệt.

**Bản 2 (21:25 12/11/2026, `date`):** sửa theo review gộp của C (`report_agent/2026-11-12_ra_khoang_cach/e_exa_review.md`: 2 major, 5 minor) + chốt tạm của A — bảng "Chỗ đổi" cuối file.

## 1. Thay đổi (chỉ nguồn của sổ web; lời dặn, cổng mở, luật kiểm giữ nguyên)
| Chỗ | Sửa gì |
|---|---|
| `backend/llm/tra_web.py` | thêm `tim_web_exa(cau, *, api_key, timeout, loai_ten_mien=(), transport=None) -> KetQuaWeb` và `tim_web_exa_truoc(…, timeout, exa_timeout, …)` cạnh `tim_web` (Serper): `POST https://api.exa.ai/search`, `type "auto"`, `numResults 5`, `userLocation "VN"`, `contents.highlights.maxCharacters 400`; sổ web **cùng khuôn** (đoạn trích = các highlights nối lại, cắt 400); tiền lấy từ `costDollars.total` của phản hồi; lỗi / hết giờ / 0 kết quả xử như Serper. Module này vẫn là nơi **duy nhất** gọi ra web |
| `backend/api/app.py` `_tim_web_server` | chọn nguồn theo cấu hình: `exa` ⇒ gọi Exa; Exa có **hạn riêng 3 s** (đo 12/11: p95 2,2 s); **Exa lỗi / hết giờ / 0 kết quả / thiếu khoá ⇒ gọi Serper một lần** với phần còn lại của hạn chung 5 s (còn < 0,5 s ⇒ thôi) — ca Exa hết giờ vẫn còn ~2 s cho Serper (p50 của Serper 2,0 s ⇒ dự phòng ở ca này **không chắc kịp**, nói thẳng). Khoá đọc trong hàm như hiện nay |
| `backend/config/settings.yaml` + `core/settings_loader.py` | `assistant.tra_web_nguon: serper` (mặc định — **cờ tắt = như hôm nay**) / `exa`; `assistant.tra_web_exa_moi_ngay: 40` (trần lượt Exa / ngày — **tham số**, mặc định trong mức miễn phí ~47 lượt / ngày; đếm trong RAM; vượt ⇒ dùng Serper) · `tra_web_exa_timeout_seconds: 3` · `tra_web_exa_loai_ten_mien: []` (**tham số**, mặc định rỗng = cấu hình đã đo; đổi ⇒ đo lại 42 câu trước khi bật); biến môi trường `HUE_TRA_WEB_NGUON` cho bản Docker |
| log `chat_metrics` | mục `tra_web` trong `tools` thêm `nguon` (`exa` / `serper` / `exa>serper`), không chữ — **một dòng ở `assistant.py` `cong_web`, làm sau khi nhánh "hết lượt tìm" merge** (file đó B đang giữ); `KetQuaWeb.nguon` đã có sẵn |
| test | phản hồi Exa ghi sẵn (qua `transport`): khuôn sổ, cắt 400, link không hợp lệ bị bỏ, lỗi 401 / 402 / 429 / hết giờ ⇒ "loi", dự phòng sang Serper đúng một lần, trần / ngày; test ranh giới: chỉ `tra_web.py` có địa chỉ Exa |

## 2. Thay hay đứng trước Serper — khuyến nghị: **Exa trước, Serper dự phòng**
- *Vì sao:* Exa hơn rõ khi chạy được (25 ↔ 17); gói miễn phí có hạn (10 USD / tháng ≈ 1.400 lượt) và có thể hết tín dụng (mã 402) ⇒ cần đường lùi tự động về thứ đang chạy ổn.
- *Khi nào sai:* dự phòng làm lượt web chậm thêm khi Exa hết giờ (đã chặn bằng ngân sách thời gian chung 5 s).
- *Chọn khác mất gì:* "chỉ Exa" đơn giản hơn nhưng hết tín dụng là mất mục web; "gọi cả hai rồi gộp" chỉ thêm 2 / 42 câu mà tốn gấp đôi.
- **Không dùng** `excludeDomains` (cấu hình có lọc kém hơn ở thí nghiệm).

## 3. Tiền + hạn mức
- Mỗi lượt web: tra 0,001 ⇒ **0,007 USD** (model viết mục ≈ 0,0002 không đổi) ⇒ lượt có web ≈ 0,0018 ⇒ ≈ 0,008 USD. Chỉ lượt kho từ chối mới tra.
- **Đối chiếu sàn tiền ≤ 0,0005 USD / câu (trung bình):** câu Huế hiện ≈ 0,00042. Một lượt web bằng Exa ≈ 0,008 ⇒ chỉ cần **≈ 1–2 % số câu đi web bằng Exa trả phí** là trung bình vượt sàn (0,00042 + 0,01 × 0,0075 ≈ 0,0005). Trong tín dụng miễn phí thì tiền thật của lượt Exa = 0. ⇒ **Một câu cho User (A hỏi):** giữ sàn 0,0005 và chỉ dùng Exa trong phần miễn phí (mặc định, trần 40 lượt / ngày) — hay nhận tiền / câu cao hơn ở lượt có web để mục web tốt hơn.
- Trần 40 lượt Exa / ngày (mặc định) nằm trong tín dụng miễn phí (10 USD / tháng ≈ 47 lượt / ngày); hết trần / hết tín dụng (mã 402) ⇒ tự về Serper.
- **Nguồn tổng hợp của chính Exa (`exa.ai`)** — 7 / 109 nguồn được trích ở thí nghiệm; mặc định **giữ** (mục web vẫn ghi tên miền nguồn như mọi nguồn); User chọn loại ⇒ đặt `tra_web_exa_loai_ten_mien: [exa.ai]` **và đo lại 42 câu** (kết quả 25 ↔ 17 nhạy với 5 mục dùng nguồn này — report mục 6b).
- Tiền đo của plan này: ≈ **0,05 USD** thật + ≈ 0,5 USD tín dụng Exa.

## 4. Tiêu chí ghi trước (đo 1 lượt, cờ `exa`)
| # | Tiêu chí | Bộ | Mức |
|---|---|---|---|
| X1 | Cờ mặc định ⇒ không đổi gì | test + Q1 | chuỗi gửi model giống byte; lượt web vẫn gọi Serper |
| X2 | Sàn mục web như B6 | 28 câu web đã thấy + 12 câu lưu trú / ăn gần, qua **server thật** | 0 link ngoài sổ · 0 số / tiền ngoài đoạn trích lọt ra · câu thiên tai cố định · câu lưu trú 0 giá · câu ngoài Huế 0 mục web · 0 truy vấn chứa tên (3 chuỗi nêu tên) |
| X3 | Không làm hỏng an toàn | an toàn 32 ×1 (chỉ các câu kho từ chối mới đi web) | 4 số như mọi bậc; ca mới ⇒ thủ tục sinh lại, hai người chấm cùng gắn |
| X4 | Tốc độ | cùng lượt X2 | từ gửi tới sự kiện `web`: p50 không chậm hơn mốc Serper cùng buổi quá 1 s; tra p95 ≤ 5 s |
| X5 | Dự phòng | test (lỗi 402 / 429 / 0 kết quả / thiếu khoá / **Exa hết giờ ở hạn riêng**) + 1 lượt thật với khoá Exa cố ý sai (qua biến môi trường của tiến trình thử, không sửa `.env`) | lượt đó có mục web từ Serper, `nguon: exa>serper` |
| X6 | Lặp lại được lợi ích | **đủ 42 câu** của thí nghiệm, qua server thật, chấm mù 2 người (cả hai cùng gắn) | **Exa ≥ Serper + 3** cùng buổi (lần lặp, nới từ +5 vì là xác nhận; dưới ngưỡng ⇒ dừng, báo A, không bật) |

## 5. Rà khung AI FDE (ngắn) — đường ra mới
| Mục | Thiết kế | Ghi chú cho User |
|---|---|---|
| Dữ liệu gửi ra | câu hỏi lượt này đã bỏ email / số điện thoại, cắt 120 ký tự, thêm " Huế" — **như đang gửi Serper** | **Exa ghi trong chính sách riêng tư (29/06/2026) rằng truy vấn được dùng để cải thiện sản phẩm, kể cả huấn luyện**; chế độ không lưu chỉ có ở gói doanh nghiệp. User đã duyệt Exa cho thí nghiệm (câu tự viết); **bật cho người dùng thật = câu hỏi thật của họ tới Exa** ⇒ A hỏi User một câu riêng trước khi bật ở bản công khai; trang Giới thiệu thêm tên nhà cung cấp tra web |
| Chữ web là dữ liệu | đoạn trích Exa dài hơn (≤ 400 ký tự × 5) ⇒ nhiều chữ lạ hơn vào model viết mục | model viết mục **không có công cụ**; mọi link do code dựng; luật kiểm số / tiền / link giữ nguyên ⇒ rủi ro không đổi loại, X2 đo |
| Khoá | `EXA_API_KEY` đọc trong hàm, không log, không vào `repr` | — |
| Hạn mức / lạm dụng | trần lượt / ngày bằng code + giới hạn lượt / IP sẵn có | — |
| Phục hồi | lỗi ⇒ Serper ⇒ câu cố định | — |

## 6. Giờ · ai
Code + test ~1,5 giờ · đo + chấm ~1 giờ. Làm sau khi nhánh "hết lượt tìm" merge (cùng vùng tra web / vòng công cụ). Người code: E; review cả nhánh: C hoặc B.

## Chỗ đổi bản 2 (theo review của C + chốt tạm của A)
| Finding | Sửa ở |
|---|---|
| M-1 hạn 5 s của Exa không để lại thời gian cho Serper | mục 1 (hạn riêng 3 s, nói thẳng ca hết giờ không chắc kịp), X5 (test ca hết giờ) |
| M-2 sàn tiền 0,0005 / câu; trần / ngày so mức miễn phí | mục 3 (đối chiếu + một câu cho User; trần mặc định 40) |
| F-1 nguồn tổng hợp của chính Exa | mục 3 (tham số loại tên miền, mặc định rỗng; đổi ⇒ đo lại); report mục 6b |
| X6 đủ 42 câu, ngưỡng rõ · test thiếu khoá ⇒ Serper · quyền riêng tư | X6, X5, mục 5 |

## Trạng thái code (21:25 12/11/2026)
Nhánh `p9-tra-web-exa` (worktree `/tmp/e_exa`, từ `main` `547a405`), **phần 0 USD đã xong, chưa đo có phí, chưa merge**: `backend/llm/tra_web.py` (Exa + Exa-trước-Serper-dự-phòng), `backend/api/app.py` (`_tim_web_server` chọn nguồn + trần / ngày), `core/settings_loader.py` (`HUE_TRA_WEB_NGUON`), `config/settings.yaml` (+4 dòng — **sẽ chồng với nhánh "hết lượt tìm" nếu nhánh đó cũng sửa khối `assistant:`; rebase sau khi nhánh đó merge**), test `tests/test_tra_web_exa.py` (mới) + `tests/test_settings_env.py`. Chưa làm: trường `nguon` trong log (chờ `assistant.py`), X2–X6.

## Sửa sau duyệt — GHI TRƯỚC lượt có phí X2–X6 (21:45 12/11/2026, `date`; A duyệt trần)
- **Tiền: ước của bản 2 thiếu** (0,05 ⇒ **≈ 0,18 USD**; A duyệt **trần 0,20** + tín dụng Exa): plan đòi đo qua server thật = cả lượt (định tuyến + trả lời + mục web ≈ 0,0013 USD / câu), không chỉ bước tra. Tiêu chí X1–X6 **không đổi**.
- **Cách chạy (ghi trước):** nhánh `p9-tra-web-exa` `76e976e`; server của worktree, cổng 8891, **mỗi lúc một server**: lượt 1 biến môi trường `HUE_TRA_WEB_NGUON=exa` (42 câu của thí nghiệm ⇒ số cho X2, X4, nhánh Exa của X6), tắt; lượt 2 không đặt biến (Serper, cùng 42 câu ⇒ nhánh Serper của X6 + mốc X4). Mỗi câu một kết nối mới, không cookie. Ghép `chat_metrics` theo `turn_id` (log của worktree).
- **X6 chấm:** các lượt có mục web (`co_muc`) của hai nhánh vào một lô xáo, 2 người chấm mù, cùng đề chấm của thí nghiệm; đạt khi cả hai cùng gắn; **Exa ≥ Serper + 3**.
- **X2 đếm bằng code trên lượt 1:** mọi mục web lọt ra có `web_kiem` rỗng; câu lưu trú 0 số tiền; 0 link trong chữ. Các vế "câu ngoài Huế 0 mục web" và "0 truy vấn chứa tên" **không phụ thuộc nhà cung cấp** (cổng mở và cách dựng truy vấn không đổi — test hiện có khoá) ⇒ dùng lại, không chạy thêm.
- **X3 làm rõ cách đo:** chuỗi gửi model của phần trả lời kho không đổi ⇒ phần kho dùng lại số an toàn hiện có; chạy an toàn 32 ×1 với cờ `exa` và **chấm phần MỤC WEB** của các câu có mục: 2 người chấm, 0 mục web nói ngược hoặc bỏ điều kiện / cảnh báo **có trong đoạn trích**; đếm bằng code: 0 mục lọt có lỗi kiểm.
- **X5:** một lượt thật với `EXA_API_KEY` sai đặt riêng cho tiến trình thử ⇒ có mục web từ Serper, log `nguon: exa>serper`.
- **Nợ ghi nhận (không thuộc việc này):** ca "model vẫn xin `tim_kho` đã ẩn" (nhánh hết-lượt-tìm) nên có dấu riêng trong log để đếm.
