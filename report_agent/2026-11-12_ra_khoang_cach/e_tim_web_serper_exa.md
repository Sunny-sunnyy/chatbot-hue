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

---

## 5. Thí nghiệm Serper ↔ Exa — GHI TRƯỚC khi chạy (20:59 12/11/2026, `date`)

User duyệt Exa + tự đặt khoá (A báo); A duyệt plan mục 3 như viết, trần **0,12 USD tiền thật** + tín dụng miễn phí của Exa; không thêm Brave. Ghi trước lượt chính:

- **Tài liệu Exa E đã mở hôm nay:** `https://exa.ai/docs/reference/search` (điểm gọi `POST https://api.exa.ai/search`, header `x-api-key`; `type` hiện hành: `auto` (mặc định) · `lite` · `deep-lite` · `deep`; `contents.highlights` có `maxCharacters`; `includeDomains` / `excludeDomains`; `userLocation`; trả `costDollars`) · `https://exa.ai/docs/search/highlights` (đoạn trích **nguyên văn** từ trang) · `https://exa.ai/docs/reference/rate-limits` (gói miễn phí 10 lượt / giây; vượt ⇒ 429) · `https://exa.ai/pricing` (`auto` 7 USD / 1.000 lượt).
- **Cấu hình Exa (một cấu hình, không chỉnh sau khi xem kết quả):** `type: "auto"`, `numResults: 5`, `userLocation: "VN"`, `contents.highlights.maxCharacters: 400` (bằng trần đoạn trích hiện có của hệ thống), **không lọc tên miền** (đổi một thứ: chỉ nhà cung cấp), hạn 5 s, một lần gọi, không thử lại. Câu tìm = đúng chuỗi hệ thống đang gửi Serper (`tra_web.cau_tim_web`).
- **Lượt thử 1 lần gọi (không gọi model) [đã chạy]:** khoá dùng được; 5 kết quả; mỗi kết quả 1 đoạn trích 216–492 ký tự (trước khi cắt 400); **0,007 USD / lượt đã gồm đoạn trích** (không tính thêm); 1,97 s (hãng báo thời gian tìm 1,30 s).
- **Công cụ đo:** `data/exa_2026-11-12/tools/do_exa.py` (private) — gọi đúng hàm `cong_web` của backend (cùng lời dặn viết mục web, cùng `kiem_muc_web`), chỉ thay hàm tra; `backend/` không đổi. Serper chạy trước, Exa ngay sau, cùng buổi.
- **Bộ đo — lệch nhỏ so với nháp (44 ⇒ 42 câu), ghi trước:** 20 câu B6 thuộc loại cần web (bỏ 8 câu "ngoài Huế" / "kho có" vì cổng web không mở với chúng — không phải việc của nhà cung cấp) + 10 câu hỏi kèm + **12** câu lưu trú / ăn gần của lượt đếm 12/11 (lấy cả 12 thay vì 6). Đều là câu tự viết, đã thấy; không câu người dùng thật.
- **Tiêu chí (giữ như mục 3, chỉnh theo n = 42):**
  1. *Chỉ số quyết:* số câu có mục web **đúng và trả lời được câu hỏi** — 2 người chấm mù (agent con, không biết bên), tính khi **cả hai** cùng gắn "đạt". **Exa ≥ Serper + 5** ⇒ "Exa hơn".
  2. *Sàn (code):* 0 mục lọt có số / tiền ngoài đoạn trích, 0 link / mã ngoài sổ, câu lưu trú 0 giá, câu thiên tai cố định — đều do `kiem_muc_web` giữ; sàn = mục nào lọt ra thì `kiem` rỗng (đếm lại bằng code trên file kết quả).
  3. *Tốc độ:* thời gian tra Exa **p95 ≤ 5 s** và 0 lượt hết giờ ngoài mức của Serper + 1.
  4. *Theo dõi (không vào luật):* tỉ lệ "không tin cậy"; tỉ lệ nguồn được trích là mạng xã hội; USD / lượt.
  5. *Luật:* đạt (1) + (2) + (3) ⇒ soạn plan đưa Exa vào sau cờ; không đạt ⇒ giữ Serper, hồ sơ ở `data/exa_2026-11-12/`.
- **Tiền ước:** Exa 42 × 0,007 = 0,29 USD (tín dụng miễn phí) · Serper 0,042 · model viết mục 84 lượt ≈ 0,07 ⇒ tiền thật ≈ **0,11**.

### 5b. Bổ sung GHI TRƯỚC (21:03 12/11/2026, `date`) — theo yêu cầu User "tham số nào chỉnh về Việt Nam được thì chỉnh; câu tìm tiếng Việt"

- **Mốc Serper** giữ đúng như đang chạy: `gl="vn"`, `hl="vi"`, `num=5`, câu tìm = câu hỏi tiếng Việt (bỏ số điện thoại / email, thêm " Huế").
- **Tài liệu Exa nói gì về Việt Nam** (`https://exa.ai/docs/reference/search`, mở 12/11/2026): **có** `userLocation` (mã quốc gia 2 chữ, hoặc toạ độ) — đã đặt `"VN"` ở cả hai cấu hình; **có** `includeDomains` / `excludeDomains` (tên miền, tên miền + đường dẫn, `*.tên-miền`) — **không có trong tài liệu:** lọc theo đuôi `.vn`; **không có trong tài liệu:** tham số ngôn ngữ; **không có trong tài liệu:** loại tìm nào hợp tiếng Việt. Câu tìm gửi Exa = **đúng chuỗi tiếng Việt** gửi Serper, không dịch.
- **Hai cấu hình Exa, mỗi cấu hình một bên riêng (User cho phép tối đa 2):** `exa` = như mục 5 (không lọc tên miền) · `exa2` = như `exa` + `excludeDomains` = facebook.com, tiktok.com, youtube.com, instagram.com, threads.net, x.com, twitter.com, zalo.me. Tiêu chí mục 5 áp cho **từng** bên so với Serper; nếu cả hai đạt, chọn bên có chỉ số quyết cao hơn (hoà ⇒ `exa2` vì ít nguồn mạng xã hội).
- **Tiền (số thật sau bên Serper):** bên Serper 0,090 USD (tra 0,041 + model 0,049 — model đắt hơn ước). Mỗi bên Exa ≈ 0,049 tiền thật ⇒ tổng 0,14 (1 bên) / 0,19 (2 bên) > trần 0,12 ⇒ **E dừng, xin A trần mới trước khi chạy bên Exa.**

## 6. Kết quả thí nghiệm (21:15 12/11/2026, `date`) — **Exa (không lọc tên miền) ĐẠT luật ghi trước; Exa có lọc mạng xã hội KHÔNG đạt**

Chạy 21:01–21:09 12/11/2026, cùng buổi, 42 câu mỗi bên, một lượt. Dữ liệu private: `data/exa_2026-11-12/` (`ket_qua/*.jsonl`, `cham/`).

| | **Serper** (mốc) | **Exa** | **Exa + loại mạng xã hội** |
|---|---:|---:|---:|
| Có mục web (code) | 28 | 27 | 25 |
| "Không tin cậy" (bỏ mục) | 9 | 10 | 13 |
| "Chưa xác minh" (luật thời gian thực) · thiên tai | 3 · 1 | 4 · 1 | 2 · 1 |
| Tra hết giờ 5 s | 1 | 0 | 1 |
| **Chỉ số quyết — mục đúng và trả lời được, cả 2 người chấm cùng gắn** | **17** | **25** | **20** |
| — theo bộ: B6 (20 câu) · hỏi kèm (10) · lưu trú + ăn gần (12) | 5 · 4 · 8 | 10 · 4 · 11 | 7 · 4 · 9 |
| Sàn: mục lọt ra mà kiểm cuối có lỗi | 0 | 0 | 0 |
| Thời gian tra p50 / p95 | 2,0 / 3,1 s | **1,6 / 2,2 s** | 1,8 / 4,0 s |
| Nguồn được trích là mạng xã hội | 24 / 91 | **0 / 109** | 0 / 90 |
| Tiền tra | 0,041 USD | 0,294 (tín dụng miễn phí) | 0,287 (tín dụng miễn phí) |
| Tiền model viết mục | 0,0078 | 0,0104 | 0,0102 |

- **Luật ghi trước:** (1) Exa 25 ≥ Serper 17 + 5 ⇒ **đạt**; Exa lọc mạng xã hội 20 < 22 ⇒ không đạt. (2) sàn 0 / 0 / 0 ⇒ đạt. (3) p95 2,2 s ≤ 5 s, 0 lượt hết giờ ⇒ đạt. ⇒ **Exa cấu hình 1 "hơn Serper" theo luật ghi trước** ⇒ soạn plan đưa vào sau cờ (`docs/superpowers/plans/2026-11-12-tra-web-exa-plan.md`).
- **Đọc số:** số mục **lọt ra** gần bằng nhau (28 ↔ 27); khác ở chỗ mục của Serper thường **không trả lời được câu hỏi** (11 / 28 mục bị cả hai người chấm coi là chung chung / "chưa xác minh được"), còn mục của Exa có nội dung (2 / 27). Khớp giả thuyết mục 1: đoạn trích 147 ký tự không đủ chữ để trả lời. Exa hơn rõ ở bộ B6 (5 ⇒ 10) và lưu trú / ăn gần (8 ⇒ 11); **hỏi kèm không đổi** (4 ⇒ 4).
- **Vì sao lọc mạng xã hội lại kém hơn (quan sát, chưa tách nguyên nhân):** cấu hình 1 đã có 0 nguồn mạng xã hội được trích — bộ lọc không thêm lợi mà làm đổi tập kết quả, tăng "tiền ngoài đoạn trích" (6 ⇒ 8) và chậm hơn (p95 4,0 s, 1 lượt hết giờ). Một lượt mỗi bên ⇒ chênh 25 ↔ 20 giữa hai cấu hình Exa có thể một phần là nhiễu.
- **Hai người chấm:** khớp 77 / 80 mục. Cả hai tự chốt cùng một quy ước cho câu hai phần (đáp được phần hỏi trước = tính là trả lời được) — quy ước này áp như nhau cho ba bên.
- **Câu chỉ một bên làm được:** chỉ Exa 10 câu · chỉ Serper 2 câu · cả hai 15 câu ⇒ gộp hai nguồn được 27 / 42 (thêm 2 câu so với riêng Exa) — không đáng thêm một lượt tra cho mỗi câu.

**Tiền thật cả thí nghiệm: 0,069 USD** (Serper 0,041 + model 0,028); Exa 83 lượt = 0,581 USD **tín dụng miễn phí** (0,007 / lượt, đã gồm đoạn trích).

**Lệch plan / lỗi của E (ghi để rút kinh nghiệm):**
- Bộ đo 42 câu thay vì 44 (ghi trước ở mục 5).
- Thêm cấu hình Exa thứ hai theo yêu cầu User (ghi trước ở 5b).
- **E báo sai tiền một lần:** đọc trường tiền cả lượt (gồm tiền tra) thành tiền model ⇒ báo "0,049 / bên", xin nâng trần 0,12 ⇒ 0,20 không cần thiết; số đúng 0,008–0,010 / bên, tổng 0,069 < trần cũ. Đã đính chính với A.
- Tài liệu Exa không có tham số ngôn ngữ, không lọc theo đuôi `.vn` (ghi ở 5b).

**Giới hạn:** một lượt mỗi bên, một buổi (kết quả tìm đổi theo ngày); 42 câu **tự viết**, không phải câu người dùng thật; người chấm là agent con, không tra web nên "có căn cứ" = khớp đoạn trích, **không phải đúng ngoài đời**; đoạn trích dài / ngắn làm người chấm đoán được bên (mù không hoàn toàn); chưa đo qua server thật (chữ đầu mục web tới người dùng).
