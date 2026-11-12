# Tìm web: Serper đang ra sao, có nên thêm Exa — phần của E

Người viết: E · 20:50 12/11/2026 (`date`) · A giao (User hỏi tối 12/11/2026) · **0 USD API** (1 lượt Codex tra web + 4 lần mở trang kiểm; **không gọi Exa**).
Nhãn: **[log]** / **[dữ liệu đo cũ]** = E đếm từ file có sẵn · **[code]** = đọc code · **[đã mở]** = E tự mở trang gốc hôm nay · **[Codex]** = Codex báo đã mở, E chưa mở lại · **[chưa kiểm]**.
Phần nguồn dữ liệu lưu trú: file riêng `e_nguon_luu_tru.md` cùng thư mục.

## 1. Serper hôm nay: tìm thì ổn, phần "không ra thông tin" là do đoạn trích quá ngắn + luật kiểm

**Cách đang chạy [code — `backend/llm/tra_web.py`]:** kho từ chối ⇒ code gửi Serper **một** câu tìm (câu hỏi + " Huế", `gl=vn`, `hl=vi`, 5 kết quả, hạn 5 s, không thử lại) ⇒ model chỉ thấy **tiêu đề + đoạn trích** của 5 kết quả (không mở trang) ⇒ model viết mục "Từ web (chưa kiểm)" ⇒ code kiểm: mọi số tiền và mọi chuỗi số trong mục phải có trong đoạn trích; câu lưu trú không được có số tiền; câu thời gian thực không được có chữ số; câu thiên tai ⇒ câu cố định. Một lỗi ⇒ **bỏ cả mục**.

**Đếm trên log server, 73 lượt có tra web (mọi lượt từ 05/11, gồm lượt đo) [log]:**

| Kết cục | Số lượt | Vì sao |
|---|---:|---|
| Có mục web | 44 (60 %) | — |
| "Chưa xác minh" (câu cố định + link) | 13 (18 %) | câu thời gian thực mà mục model viết có chữ số ⇒ luật an toàn chặn (đúng thiết kế) |
| "Không tin cậy" (bỏ mục) | 14 (19 %) | số ngoài đoạn trích 9 · số tiền ngoài đoạn trích 4 · nêu giá phòng 2 (một lượt dính 2 mã) |
| Câu thiên tai (cố định) · model lỗi | 1 · 1 | — |
| **Serper lỗi / hết giờ / 0 kết quả** | **0** | 73 / 73 lần trả 3–5 kết quả; thời gian tra p50 ≈ 2,0 s |

Lượt web của B7 giữa kỳ (10 câu "web trả lời được"): 6 có mục · 3 "không tin cậy" · 1 cổng không mở — cùng hình dạng.

**Hai quan sát giải thích con số [dữ liệu đo cũ — 56 lượt tra / 280 kết quả của bộ đo web]:**
- **Đoạn trích rất ngắn:** trung vị 147 ký tự / kết quả (dài nhất 169) ⇒ model có ≈ 730 ký tự cho cả mục. Câu hỏi giá / giờ / số điện thoại thường cần con số nằm **trong trang**, không nằm trong 147 ký tự đó.
- **Nguồn kém:** 90 / 280 kết quả (32 %) là facebook.com; trang .gov.vn chỉ 7 / 280; 56 tên miền khác nhau.

**Kết luận phần 1:** (quan sát) Serper **không hỏng** — chưa lần nào lỗi hay rỗng. (quan sát) ~37 % lượt không ra mục là do luật kiểm chặn, trong đó 18 % là luật an toàn cố ý. (giả thuyết, chưa có phép thử tách) 19 % "không tin cậy" phần lớn do model lấy số từ trí nhớ / suy ra khi đoạn trích không chứa số — nguồn tìm trả **đoạn dài hơn theo câu hỏi** có thể giảm phần này; nó **không** giảm phần 18 % (luật an toàn giữ nguyên).

## 2. Exa cho gì khác Serper (tra công khai 12/11/2026)

| | **Serper** (đang dùng) | **Exa** |
|---|---|---|
| Trả gì | kết quả Google: tiêu đề + đoạn trích ngắn + link; không có nội dung trang **[đã mở serper.dev]** | `/search` trả kết quả **kèm** `highlights` (đoạn **trích nguyên văn** từ trang, chọn theo câu hỏi; có `maxCharacters`) hoặc `text` (toàn văn) trong cùng một lần gọi **[đã mở tài liệu highlights]** |
| Tốc độ hãng nêu | 1–2 s **[đã mở]** | `lite` ~0,45 s · `auto` ~1 s · `deep` 4–15 s; lấy trang mới (không từ chỉ mục) có thể chờ tới 10 s **[Codex]** |
| Giá / lượt | **0,001 USD** (gói nhỏ nhất; 2.500 lượt thử) **[Codex; E thấy "2.500 free queries" trên trang]** | `lite` **0,004** · `auto` **0,007** USD / lượt tới 10 kết quả **[đã mở trang giá]**. Trang giá **không ghi rõ** highlights có nằm trong giá gốc không (Codex nói có; nếu tính riêng: +0,001 / 1.000 trang) ⇒ ước trần **0,012 USD / lượt** (auto + highlights 5 trang) |
| Dùng thử | 2.500 lượt | 10 USD tín dụng / tháng + 10 USD lần đầu, không cần thẻ **[đã mở]** ⇒ đủ cho thí nghiệm |
| Tiếng Việt / trang .vn | Google ⇒ phủ tốt, có `gl` / `hl` | **không tìm thấy bằng chứng công khai nào** về chất lượng Exa với truy vấn tiếng Việt hay độ phủ .vn **[Codex: không tìm thấy]** ⇒ đây là rủi ro chính, chỉ đo mới biết |
| Lọc nguồn | không | `includeDomains` / `excludeDomains`, lọc ngày **[Codex]** — bỏ được facebook, ưu tiên trang chính thức |
| Điều khoản | **không tìm thấy trang điều khoản mở được** [chưa kiểm] (User đã chấp nhận rủi ro này ở spec Phase 9) | chính sách riêng tư (29/06/2026): truy vấn được dùng cải thiện sản phẩm "kể cả huấn luyện"; không lưu-không-giữ chỉ ở gói doanh nghiệp 12.000 USD / năm; điều khoản **không nói rõ** quyền hiển thị lại đoạn trang cho người dùng cuối **[Codex]** |
| So đo độc lập | — | 2 bảng xếp hạng 2026 cho Exa cao hơn Serper / Tavily, nhưng **đều do bên bán API khác vận hành**, tiếng Anh, không phải du lịch Việt Nam **[Codex]** ⇒ không dùng làm bằng chứng |

**Lựa chọn khác đáng so [Codex; E mở kiểm Brave]:** **Brave Search API** — 5 USD / 1.000 lượt, 5 USD miễn phí / tháng, có "extra snippets" (thêm tới 5 đoạn / kết quả) và "LLM Context" (đoạn trích xếp hạng sẵn) **[đã mở]** — cùng ý với Exa, rẻ hơn `auto`; Tavily (~0,008 / lượt), Linkup (0,005–0,006), Firecrawl / Jina (mở trang, chậm hơn 5 s). Google Custom Search đóng đăng ký mới; Bing Search API đã ngừng; Perplexity Sonar đã ngừng.
**Cách không cần nhà cung cấp mới (đề xuất, chưa đo):** giữ Serper, code tự tải **1–2 trang đầu** (không phải mạng xã hội) rồi trích đoạn quanh từ khoá — 0 USD thêm nhưng mở đường ra mới từ server (tải trang lạ ⇒ phải rà bảo mật: giới hạn tên miền, cỡ, thời gian, không theo chuyển hướng lạ) và dễ vượt hạn 5 s.

**Nhận định:** Exa **đáng thử** vì đúng chỗ đang thiếu (đoạn trích dài, nguyên văn, lọc được nguồn), nhưng **chưa đủ căn cứ để bật**: đắt gấp 4–12 lần mỗi lượt, tiếng Việt chưa ai đo, truy vấn người dùng bị dùng để huấn luyện ở gói thường. Mục web hiện đã ≈ 0,0018 USD / câu (vượt sàn 0,0005 của câu thường) ⇒ thêm 0,004–0,012 là đổi đáng kể về tiền.

## 3. NHÁP — chờ User chọn: plan 1 trang thí nghiệm Serper ↔ Exa (↔ Brave tuỳ chọn)

- **Câu hỏi:** cùng bộ câu, nguồn tìm trả đoạn dài có làm **nhiều lượt ra mục web đúng hơn** mà không phạm sàn không?
- **Đổi một thứ:** chỉ nguồn của sổ web (tiêu đề + đoạn + link). Lời dặn viết mục web, luật kiểm, cổng mở — giữ nguyên. Đoạn Exa cắt ≤ 400 ký tự (bằng trần `MAX_SNIPPET_CHARS` hiện có) để lời dặn không phải đổi. Chạy trong harness riêng ở `data/` (không đụng `backend/`); mốc Serper chạy **cùng buổi**.
- **Bộ đo (đã thấy, có sẵn):** 28 câu web B6 + 10 câu hỏi kèm + 6 câu lưu trú / ăn gần / sự kiện bị từ chối ở lượt đếm 12/11 ≈ **44 câu**, 1 lượt mỗi bên. Không bộ kín (mức nhẹ; thí nghiệm chọn nguồn, không chỉnh lời dặn).
- **Tiêu chí ghi trước:**
  1. *Chỉ số quyết:* số câu có mục web **đúng và trả lời được câu hỏi** (2 người chấm mù, cả hai cùng gắn) — Exa ≥ Serper + 5 / 44 mới gọi là hơn.
  2. *Sàn (đếm bằng code, như B6):* 0 link ngoài sổ · 0 số / tiền ngoài đoạn trích lọt ra người dùng · câu thiên tai cố định · câu lưu trú 0 giá · 0 câu ngoài Huế có mục web.
  3. *Theo dõi:* tỉ lệ "không tin cậy"; tỉ lệ kết quả từ mạng xã hội; thời gian tra p50 / p95 (**p95 ≤ 5 s**, vượt ⇒ không đạt); USD / lượt thật.
  4. *Luật giữ / gỡ:* đạt (1) + (2) + p95 ⇒ trình User bật theo cờ; không đạt ⇒ giữ Serper, hồ sơ ở `data/`.
- **Tiền:** Exa 44 lượt × ≤ 0,012 ≈ 0,5 USD **nằm trong 10 USD tín dụng miễn phí** ⇒ 0 USD thật; Serper 44 × 0,001 = 0,04; model viết mục 88 lượt × ≈ 0,0008 ≈ 0,07 ⇒ **≈ 0,11 USD** thật. Chấm: agent con, 0 USD API.
- **Cần User:** (a) duyệt **nhà cung cấp mới Exa** + đường ra mới (câu hỏi người dùng đã chuẩn hoá gửi tới Exa; ở thí nghiệm chỉ gửi câu **tự viết** của bộ đo, không có câu người dùng thật); (b) tạo tài khoản Exa, đặt khoá `EXA_API_KEY` vào `.env` (agent không đọc file này); (c) có thêm Brave vào cùng lượt không (thêm 1 khoá, ≈ 0,02 USD).
- **Khi nào kết luận sai:** bộ 44 câu là câu agent tự viết, không phải câu người dùng thật; một lượt mỗi bên (kết quả tìm đổi theo ngày).
- **Phương án không làm gì:** giữ Serper; nhận ~4 / 10 lượt web không ra mục; phần lưu trú đã có hướng riêng (thẻ khu + link).

## 4. Giới hạn
- Số [log] trộn lượt đo của nhiều bộ ⇒ là hình dạng lỗi, không phải tỉ lệ người dùng thật.
- E mở kiểm 4 trang (giá Exa, tài liệu highlights, Serper, Brave); giá Serper theo bậc, điều khoản Exa, hai bảng xếp hạng là **[Codex]**.
- Chưa gọi Exa lần nào ⇒ mọi nhận định về chất lượng Exa là từ tài liệu của hãng.
