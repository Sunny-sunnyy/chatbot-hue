# Báo cáo cho bạn: Nghiên cứu rộng trước Phase 9 (trợ lý du lịch - văn hoá)

**Cập nhật lần cuối: 21:05 04/11/2026 — bản 5: thêm mục 000 — đọc code 8 repo + 1 paper bạn gửi, thử Huế TRIPO vòng 3, tra web về agent ⇒ tính năng đáng thêm, xếp theo bậc.** Trước: 18:40 03/11/2026 — bản 4: thêm mục 00 — nghiên cứu sản phẩm thật (15 trợ lý du lịch / di sản trên thế giới + thử Huế TRIPO vòng 2) ⇒ tính năng đáng học, xếp theo bậc Phase 9.** Trước: 14:55 02/11/2026 — bản 3: hướng đổi thành trợ lý agent có công cụ (nghiên cứu thêm 02/11, spec duyệt) — xem mục 0 ngay dưới.** Trước: 16:13 01/11/2026 — bản 2: thêm kết quả ChatGPT (đã kiểm 9 ý), thử Huế TRIPO trên 10 câu, hướng Phase 9 bạn chọn, lịch đến bảo vệ.**
Trước: 15:28 01/11/2026 — bản 1 sơ bộ (Codex + kiểm tay; review B118 đạt). Người viết: A · Tra + kiểm: B (thực tế, người dùng, thử TRIPO), C (paper, repo, kiểm
ChatGPT) · Review bản 2: B (B120). Tiền: 0 USD API cho nghiên cứu; thử hue_rag 11 câu ≈ 0,004 USD (~100 đồng).

## 000. Cập nhật 04/11 — đọc code repo bạn gửi + TRIPO vòng 3 + agent (bạn yêu cầu 04/11)

**Đã làm (0 USD API, 6 agent con của A, A kiểm 2–3 ý mỗi phần bằng file / code thật):** đọc **code** (trước chỉ đọc README) 8 repo + paper arXiv 2203.07742 bạn gửi, đọc lại `báo cáo nghiên cứu github.txt` (gồm ghi chú cuối của bạn: router, lọc theo lĩnh vực, viết lại câu, chia câu), thử Huế TRIPO vòng 3 bằng Playwright (15 lượt, tập trung lịch trình nhiều ràng buộc + sửa lịch nhiều lượt), tra web về trợ lý du lịch dạng agent (Codex + A mở kiểm 4 nguồn). Mỗi repo có hồ sơ đủ để **không cần clone lại** (commit, license, cây thư mục, đoạn code then chốt): `data/nghien_cuu_tinh_nang_2026-11-04/` (private).

**Điều thấy được (quan sát, đã kiểm):**
- **Ghi chú của bạn trong github.txt:** router đầu vào — **đã có** (B1); viết lại câu tìm — **đã thử, kém hơn, bỏ** (B2a); chia câu tìm nhiều lần — **đã có** dạng trợ lý tự gọi `tim_kho` thêm ≤ 2 lần (B2b); **lọc theo lĩnh vực (foods / heritages…) — chưa có**.
- **TRIPO vòng 3:** cách trang lập lịch chạy giống hướng B5 (model đổi chữ ⇒ nhãn biểu mẫu, **code** chọn điểm + xếp giờ + tính tiền; lượt sửa gửi kèm cả lịch hiện tại, model trả một hành động có tên). Nhưng lỗi thấy được: mất "2 ngày" và số người (lịch ra 1 ngày, "1 người lớn", cả 2 lần chạy); cùng câu mà ngân sách lần "Tiết kiệm" lần "Trung bình"; xếp bảo tàng quá giờ đóng cửa 77 phút theo chính dữ liệu của nó; lịch kết thúc 23:12 cho nhà có bé 5 tuổi và ông 72 tuổi; câu sửa hai ý chỉ làm một ý, im lặng bỏ ý kia; lượt sửa không kiểm lại ràng buộc cũ; chậm 22–66 s.
- **Repo `KhaiBoiPho/agentic-rag`:** tác giả ghi ngay trong code (`app/core/chat/router.py` dòng 1–15, A đọc): khi đã nhét sẵn nhiều đoạn tìm được, model **không chịu gọi công cụ** mà trả "không có dữ liệu" ⇒ họ chuyển sang định tuyến trước, code gọi công cụ. hue_rag đang đúng tình huống đó (tìm 10 đoạn trước rồi mới đưa model có công cụ) ⇒ B5 đã có sàn "≥ 9 / 10 câu lịch trình gọi `lich_trinh`" (plan bản 3); có phương án dự phòng nếu trượt.
- **Repo trợ lý du lịch (`Travel-AI-Assistant`, `trip-advisor-agent`):** hỏi lại theo danh sách trường bắt buộc (Travel-AI: 3 trường, `domain.py:69-77`, A đọc), nhưng có lỗi gộp lượt (không bỏ được sở thích; số người mặc định ghi đè số đã nói), sửa bằng form không tính lại; trip-advisor để model tự đặt cờ "đủ thông tin", vòng hỏi không có trần, "mưa ⇒ trong nhà" chỉ là lời dặn — và có lỗi bảo mật (công cụ ghi DB không cần duyệt, secret trả về trình duyệt). `booking-bot`: không phải agent, có lỗi chèn câu truy vấn.
- **Repo gợi ý khách sạn (3 repo) + `vietnamese-rag-system`:** không có gì mang nguyên sang được — cần dữ liệu tương tác / rating mà kho không có, và tự có lỗi (repo khách sạn đổi "huế" thành "Thừa Thiên Huế" nên hỏi về Huế ra 0 kết quả — A đọc `ai_engine.py:427`; ViHoRec: gợi ý theo nội dung kém cả "chọn khách sạn phổ biến nhất" — A đọc bảng kết quả; `vietnamese-rag-system`: chia đoạn theo cấu trúc không chạy vì xuống dòng bị xoá trước — A đọc code). Paper 2203.07742 = **ViWOZ** (2022, bộ hội thoại đặt dịch vụ tiếng Việt, không phải RAG).
- **Nguồn web về agent** (A mở kiểm): Anthropic "Building effective agents" (luồng cố định + công cụ trước, agent tự do sau); khảo sát 100 lịch trình ChatGPT-3.5: 52 % xếp điểm vào giờ không mở; Flex-TravelPlanner: làm tốt một lượt không báo trước được việc sửa nhiều lượt.
- **`báo cáo nghiên cứu github.txt` ghi sai nhiều chỗ** về hue_rag (model, reranker, số file) và về chính các repo (vd "Text-to-SQL", "7–8 trường", "bỏ được điểm") ⇒ chỉ dùng làm chỉ mục, không làm bằng chứng.

**Tính năng đáng thêm — A xếp theo bậc (đề xuất):**

| Khi | Tính năng | Học từ | Đổi gì cho người dùng | Công sức · rủi ro |
|---|---|---|---|---|
| **B5 (thêm vào plan, trước khi code — A quyết, B review)** | kiểm giá bắt cả dạng "…000đ" / "triệu"; không đủ điểm hợp sở thích ⇒ câu cố định nói rõ; **nói rõ phần không xếp được** + lý do lấy từ mã luật của code; dòng giả định / lưu ý do **code** nối, không để model chép; mỗi luật xếp có một test cố tình vi phạm | repo khách sạn (lọc giá sai không báo), TRIPO (lặng lẽ bớt điểm), Travel-AI | lịch không lặng lẽ thiếu / sai; người dùng biết vì sao | nhỏ · thấp |
| **B5 — cần bạn duyệt bảng** | cột **tên khác** cho điểm (kho gọi "Hiếu Lăng", "Hoàng thành"…) | đối chiếu kho | gõ tên khác vẫn nhận đúng điểm | nhỏ · thấp |
| **B4 / B5** | "Mình hiểu: 2 ngày · có người lớn tuổi · thong thả — sai thì bấm sửa" + code dò số trong câu để **phát hiện lệch** rồi hỏi lại | TRIPO mất "2 ngày" | không bị lịch sai số ngày mà không biết | nhỏ · thấp |
| **Sau B5 — bậc mới, cần bạn chọn** | **sửa lịch nhiều lượt**: server giữ khung lịch của phiên, công cụ `sua_lich` với hành động có tên (bỏ điểm, dời buổi, đổi số ngày, thay điểm — đưa 2–3 điểm cùng cụm để bấm chọn), code xếp lại bằng cùng luật B5 + dòng "Đã đổi / Giữ nguyên"; bộ đo chuỗi sửa, mỗi chuỗi chạy 3 lần | TRIPO, Travel-AI, Flex-TravelPlanner; 3 agent cùng đề xuất | "bỏ lăng Khải Định", "ngày 2 chỉ đi chiều" ⇒ lịch mới đúng luật | vừa (~2–3 ngày) · trung bình (câu sửa mơ hồ) |
| **B5b (cùng thời tiết)** | cột trong nhà / nhiều bậc ⇒ "phương án ngày mưa", "ít bậc thang" | trip-advisor, TRIPO | lịch hợp trời mưa / người đi chậm | nhỏ (dữ liệu bạn duyệt) · trung bình nếu kho không ghi rõ ⇒ để trống |
| **Sau Phase 9 — đo rẻ trước** | **lọc / ưu tiên theo lĩnh vực** (ý của bạn): đếm 0 USD trên kết quả đo đã có, chỉ thí nghiệm khi ≥ 3 câu thiếu ý vì đoạn lĩnh vực khác chiếm chỗ; đếm đoạn gần trùng trong 10 đoạn; gắn nhãn lỗi tự động | ghi chú của bạn, `vietnamese-rag-system` | có thể bớt từ chối nhầm | đếm 0 USD · thí nghiệm sau |
| **Không làm** | gợi ý theo lọc cộng tác / rating (không có dữ liệu), tối ưu quãng đường (9 file có toạ độ), GraphRAG, định tuyến bằng danh sách từ, bảng SQL giá, rerank / sparse mới (Phase 8 đã thử, bỏ), nhớ cả câu trả lời, web bật sẵn | — | — | — |

**Giới hạn:** đọc code, **không chạy** code repo (lỗi trong repo là suy từ code, chưa thấy chạy); TRIPO thử một lần, 15 lượt; nguồn web phần lớn Codex tự khai (0 trang mở thật), A mở kiểm 4. Hồ sơ: `data/nghien_cuu_tinh_nang_2026-11-04/` — `sa1_github.md`, `sa2_tripo_v3_agentic.md` (+ `tripo_v3/`), `sa3_khaiboipho.md`, `repo_*.md` (7), `paper_2203.07742.md`.

## 00. Cập nhật 03/11 tối — sản phẩm thật: có gì đáng học (bạn yêu cầu 03/11)

**Đã làm (0 USD API):** (1) Codex quét **15 trợ lý AI du lịch / di sản đang chạy** (Tokyo EDO, HelloBC Canada, AI Tour Quý Châu, Pythia Hy Lạp, Chessie Baltimore, Booking, Tripadvisor, Google Canvas, Expedia, bảo tàng Dalí / National Gallery / Acropolis…) + khảo sát người dùng — Codex chỉ tìm 8 lượt, **0 trang mở thật** ⇒ A tự mở kiểm 3 nguồn chính (Tokyo EDO, HelloBC, khảo sát Beach.com): **đúng**; các nguồn khác là tự khai, chưa kiểm. (2) Agent con của A thử **Huế TRIPO vòng 2** bằng Playwright (11 lượt chat + các tính năng vòng 1 chưa thử; không đăng nhập, không gửi biểu mẫu); A kiểm 3 ý bằng file thô: đúng.

**Điều thấy được (quan sát):**
- TRIPO **hỏi tiếp không tìm lại kho** (gói tin `used_rag: false` ở 3 / 11 lượt): "còn lăng kia thì sao" hiểu đúng đối tượng nhưng nói "không có dữ liệu giá vé" — trong khi lượt sau chính nó liệt kê giá lăng đó. Chào "Xin chào" bị chặn là "không liên quan chủ đề".
- TRIPO **có dữ liệu theo ngày trên trang** (lịch sự kiện tháng, thời tiết 23–31°C) nhưng chat trả lời "không có dữ liệu thời gian thực"; thời tiết ghi "trực tiếp" mà thật ra là bản tin ngày hôm trước.
- Câu khẩn cấp (người thân ngã trong Đại Nội): có số 115 nhưng 7 bước sơ cứu tự sinh, không nguồn, ~32 s. Lịch trình / chi phí: **trả lời tạm rồi hỏi lại 2–3 ý bằng chữ** (vòng 1 không hỏi lại). Nguồn 0–4 link / câu, có link hỏng; chữ hiện sau **6–58 s**, không hiện dần.
- Thế giới (nguồn đã kiểm): Tokyo EDO có **nút báo câu sai**, cảnh báo "không bảo đảm đúng / đủ", lịch sử mất khi đóng trang; HelloBC dùng RAG, 8 câu gợi ý mẫu, tự nhắc người dùng kiểm thông tin quan trọng; khảo sát Mỹ 09/2025 (1.003 người): 77 % tin AI khi lập kế hoạch nhưng chỉ **32 %** để AI lập trọn chuyến.

**Tính năng đáng học — A xếp theo bậc Phase 9 (đề xuất, chưa chốt):**

| Nhóm | Tính năng | Học từ | Ở hue_rag | Công sức · rủi ro nói sai |
|---|---|---|---|---|
| Đã có — giữ, dùng khi trình bày | hỏi tiếp vẫn tìm kho bằng câu có tên đối tượng; trích nguồn từng ý; chữ hiện dần; câu gợi ý; nhãn "AI có thể sai" + dòng "có thể đã thay đổi"; câu khẩn cấp soạn sẵn có nguồn | TRIPO hỏng đúng các chỗ này | B2–B3, giao diện | — |
| Đưa vào bậc đang có | **trả lời tạm có nguồn + hỏi lại 1–3 ý, kèm nút chọn nhanh** | TRIPO v2, Tripadvisor, Booking (7 / 15 sản phẩm hỏi tiếp) | **B4** (thiết kế cách hỏi) | vừa · thấp |
| Đưa vào bậc đang có | **link "mở bản đồ"** cho từng điểm trong lịch trình, dựng bằng code từ tên / địa chỉ có trong kho (không để model tạo toạ độ) | TRIPO, Google | **B5** | nhỏ · thấp |
| Đưa vào bậc đang có | **dữ liệu theo ngày do code lọc** (sự kiện tuần này từ lịch trong kho, thời tiết từ API) — luôn ghi ngày của dữ liệu | chỗ TRIPO hỏng | "code giữ ngày" (spec) + thời tiết (plan B5 quyết) | vừa · trung bình (ngày sai) |
| **Đã làm (B142, merge `6817897` 03/11 tối)** | nút 👍 / 👎 ở mỗi câu (log mã lượt + đánh giá, không lưu chữ) | Tokyo EDO | **có** | — |
| **Đã làm (B142)** | câu ngoài phạm vi kèm nút gợi ý câu trong phạm vi | TRIPO vòng 1 câu 10 | **có** | — |
| Không làm (7 tuần, một người) | thuyết minh âm thanh, giọng nói, đa ngôn ngữ, bản đồ toàn tỉnh, nhận diện ảnh, đặt chỗ | bảo tàng, OTA | — | lớn · dữ liệu không có |

**Chỗ hue_rag đang kém:** tốc độ chữ đầu câu về Huế 3,50 / 5,33 s **vượt sàn bạn đặt** (3 / 5 s) — vẫn nhanh hơn TRIPO nhiều lần, nhưng là sàn của chính mình. Log cho thấy phần tìm kho chỉ ~50 ms; thời gian nằm ở lần gọi phân loại câu (~1,5–2,9 s) + chờ model trả chữ đầu ⇒ hướng tối ưu: giảm mức suy luận / cố định khoá đệm cho lần phân loại, hoặc gộp phân loại vào lần trả lời (đổi kiến trúc — bạn quyết). Chưa đo, chưa hứa số.

**Giới hạn:** TRIPO thử một lần, mỗi loại một câu; không kiểm dữ kiện TRIPO với nguồn chính thức. Danh sách thế giới: 15 sản phẩm, phần lớn nguồn là thông cáo của chính đơn vị (nguồn nói), 3 nguồn A đã mở kiểm. Hồ sơ (private): `data/nghien_cuu_tinh_nang_2026-11-03/tripo_v2/bao_cao_tripo_v2.md`, `data/tra_cuu_cli/2026-11-03_tinh-nang-the-gioi/ket_qua.md`.

## 0. Cập nhật 02/11 — hướng đổi thành trợ lý agent có công cụ (đọc mục này trước; mục 1–7 là bản 01/11)

- **Bạn đổi hướng (02/11):** "lên trợ lý mà không có gì khác RAG mức 1 thì gọi thẳng LLM cần gì trợ lý" ⇒ Phase 9 là **trợ lý agent có công cụ**. Ý "không agent tổng quát tự tra web" ở mục 1 **không còn đúng**.
- **Nghiên cứu thêm 02/11** (0 USD API): 3 sub-agent đọc khoá AI FDE (kiến trúc agent, bảo mật + bài capstone, chi phí / trạng thái), ChatGPT deep research (agent có công cụ trong sản phẩm thật,
  OpenAI Agents SDK, tra web an toàn, đo agent, chi phí), B tra web (SDK, điều khoản Serper, đo agent) + dò SDK thật (≈ 0,0002 USD), C thử nâng SDK. A tự mở trang gốc kiểm: SDK mới nhất 0.24.0 (15/10/2026);
  `max_turns` đếm số lần gọi model; điều khoản Serper (29/05/2024) tự nhận dịch vụ "business-to-business", không nói rõ được hiển thị cho người dùng cuối.
- **Mọi nguồn cùng khuyên:** **agent dưới chính sách** — việc luôn phải xảy ra (ngày hôm nay, lần tìm kho đầu, giới hạn) để code làm; model chỉ tự quyết phần cần phán đoán (khoá: "luồng cố định thì một lần gọi
  đúng ngang agent mà rẻ hơn"; ChatGPT: "không thả agent ReAct tự do cho bản đầu"). Ước (chưa đo): câu về Huế ~2 lượt gọi ≈ 0,0004 USD; câu tra web thêm ~0,001 USD tiền Serper.
- **Bạn chọn (02/11, spec bản 9 duyệt `169c2dd5f86a`):** agent định tuyến có đầu ra có cấu trúc ⇒ trò chuyện / trợ lý Huế (công cụ: tìm thêm kho, hỏi lại, lịch trình) / ngoài phạm vi / khẩn cấp; code giữ ngày,
  tra web Serper khi kho từ chối (mục "Từ web" có nhãn chưa kiểm), lần tìm đầu là thí nghiệm; nhớ hỏi + đáp trong cuộc trò chuyện; OpenAI Agents SDK 0.19.4; chất lượng trước, ghi tiền mỗi lần gọi; trần 2,0 USD.
- **Chi tiết:** `docs/superpowers/specs/2026-11-02-phase-9-design.md` (§2 quyết định, §5 tám bậc, §10 bảng bạn đã chọn); tư liệu private `data/nghien_cuu_phase_9_2026-11-01/agent/`.

## 1. Tóm tắt

- **Đề tài (bạn đã chốt với giảng viên):** "Xây dựng ứng dụng hỗ trợ trải nghiệm văn hóa và du lịch Huế dựa trên Retrieval-Augmented Generation". Bảo vệ
  khoảng 04–10/01/2027 ⇒ A tạm đặt **đóng code ~20/12/2026** (~7 tuần).
- **Hướng Phase 9 bạn chọn (01/11):** **trợ lý di sản Huế đáng tin + lịch trình gợi ý nhỏ.** Gồm: câu nhiều nguồn đủ ý · hỏi lại khi thiếu thông tin · nhớ
  hội thoại ngắn · thông tin theo ngày ghi rõ nguồn / ngày + chặn câu an toàn trước mô hình · lịch trình chỉ gợi ý **thứ tự điểm có nguồn** (không giờ / giá
  chính xác, không đặt chỗ). Không làm: agent tổng quát tự tra web, đặt chỗ, giọng nói / ảnh / nhiều ngôn ngữ.
- **Vì sao hướng này (bằng chứng đã kiểm):**
  - Huế đã có **Huế TRIPO** (Sở VHTTDL Huế + HueCIT, ra mắt 31/10/2026, dùng GPT-5 mini theo bài của HueCIT) — mạnh ở lập lịch trình, nhưng thử 10 câu thấy:
    xếp điểm sau giờ đóng cửa, trả lời câu an toàn / chi phí bằng kiến thức chung không nguồn, **nói ngược kho ở câu điều kiện vào khu vực**, 14–36 s / câu.
  - Người dùng tin AI thấp: Booking.com (37.325 người, 33 thị trường có Việt Nam): **6 %** tin AI hoàn toàn, 12 % để AI tự quyết; Expedia / YouGov (> 5.700
    người, Expedia đặt hàng): 66 % không tin AI tự đặt. ⇒ (suy ra) **có nguồn + không bịa + biết hỏi lại** là giá trị thật, và là chỗ hue_rag khác TRIPO.
  - Lập lịch trình đầy đủ bằng LLM rất khó (TravelPlanner: GPT-4 đúng 0,6 %) ⇒ chỉ làm bản nhỏ, dựa trên hỏi lại + nhớ ngắn.
  - Agent tổng quát tốn 2,7–3,6× token, không luôn hơn pipeline có mô-đun ("Is Agentic RAG worth it?", ACL 2026) ⇒ (suy ra) dễ vượt trần 0,0005 USD / câu.
- **hue_rag lộ 2 chỗ cần sửa khi thử 10 câu:** từ chối nhầm câu hỏi 2 ý (giờ + giá vé — kho có giá vé); không nhớ lượt trước.
- **Bạn đã chọn (01/11):** phiên sau chạy **song song** — B code giao diện, C viết một spec Phase 9 để bạn duyệt. **Đầu phiên sau bạn cần:** duyệt gói npm cho giao diện.

## 2. Nghiên cứu đã chạy thế nào

```text
4 mạch Codex (thực tế · người dùng · paper · repo) — nông, B / C tự mở trang gốc kiểm ~3 ý / mạch
  + ChatGPT web (yêu cầu 5 phần, 616 dòng kết quả) — C kiểm 9 ý: 6 đúng hết, 3 sai một phần
  + B thử Huế TRIPO bằng Playwright (không đăng nhập, không đặt / gửi) + cùng 10 câu trên hue_rag
  → A tổng hợp ⇒ brainstorm với bạn (B1: hướng; B2: lịch)
```

**Độ tin:** chỉ ý có nhãn [đã kiểm] / [B kiểm] / [C kiểm] là đã có người mở trang gốc; ý chưa kiểm chỉ xuất hiện khi có nhãn [tự khai]. ChatGPT tốt hơn Codex nhiều
(sâu, có cấu trúc, có cả hướng nên tránh) nhưng **vẫn sai chi tiết 3 / 9 ý** — mục 4. Hồ sơ (private): `data/nghien_cuu_phase_9_2026-11-01/`.

## 3. Thử Huế TRIPO ↔ hue_rag (10 câu tự viết, không lấy từ bộ đánh giá; B đánh giá, không phải chấm chuẩn)

| # | Loại câu | Huế TRIPO | hue_rag | Nhận xét |
|---|---|---|---|---|
| 1 | di tích | dài, có cấu trúc; 1 link danh mục; ~26 s | đủ ý, nguồn theo từng ý; 6,7 s | cả hai được; hue_rag có nguồn từng ý |
| 2 | giờ + giá vé | trả lời cụ thể giờ + giá (khớp trang danh mục của nó) | **từ chối** | **hue_rag từ chối nhầm** — kho có giá vé người lớn (A kiểm) |
| 3 | món ăn | dài, có ý diễn giải đáng ngờ (chưa kiểm) | 2 nguồn, so vùng miền cụ thể | — |
| 4 | lễ hội theo ngày | đưa một khoảng ngày | cùng khoảng ngày, 1 nguồn | khớp nhau (chưa đối chiếu nguồn chính thức) |
| 5 | nghệ thuật | định nghĩa chung chung | cụ thể hơn: nơi diễn, suất diễn, điều kiện, 6 nguồn | hue_rag hơn |
| 6 | lịch trình 2 ngày | chi tiết theo buổi; **không hỏi lại** | khung ngắn có nguồn; **không hỏi lại** | TRIPO giàu hơn; cả hai không hỏi lại |
| 6b | lượt tiếp (bố mẹ lớn tuổi) | **nhớ lượt trước**, viết lại nhịp chậm | **không nhớ** | hue_rag thiếu hẳn nhiều lượt |
| 7 | chi phí, thiếu thông tin | tự ước một khoảng triệu đồng, không hỏi lại, chen chữ tiếng Anh | từ chối | không bên nào hỏi lại |
| 8 | **điều kiện vào khu vực** | "**không có quy định bắt buộc**" | khu thờ tự / cung điện **bắt buộc** kín đáo, 4 nguồn | **trái nhau ở loại lỗi tệ nhất**; nhiều file kho ghi quy định này (A kiểm kho; chưa đối chiếu web) |
| 9 | an toàn | lời khuyên chung tự sinh, không nguồn | thận trọng, có điều kiện bắt buộc, 3 nguồn | hue_rag thận trọng + có nguồn |
| 10 | ngoài phạm vi | lái sang gợi ý quán ở Huế (thân thiện) | từ chối chuẩn | đáng học: từ chối kèm gợi ý trong phạm vi |

**Biểu mẫu lập lịch trình của TRIPO (B chạy thật):** chọn bằng nút → trợ lý hỏi thêm bằng nút (sở thích, đi bộ ít) → 3 phương án → lịch theo giờ có km, chi phí
từng mục, thuyết minh, bản đồ, chỉ đường, chia sẻ, tải PDF. Lỗi thấy: xếp một lăng **sau giờ đóng cửa** chính trang ghi; lịch dày dù chọn có người lớn tuổi.
⇒ (suy ra) **hỏi lại bằng nút** là mẫu giao diện đáng học cho phần hỏi lại của mình.

## 4. ChatGPT nói gì — đã kiểm (C117)

| Ý | Kết quả kiểm |
|---|---|
| TRIPO dùng GPT-5 mini + embedding + "Tourism Knowledge Model" | đúng; nhưng bài gốc **không** ghi "6 ngôn ngữ" (chỉ "đa ngôn ngữ"), và "dưới 3 giây" là của tối ưu lịch trình, **không phải** tốc độ chat |
| Booking.com: 37.325 người, 33 thị trường, 6 % tin hoàn toàn, 12 % để AI tự quyết | đúng nguyên văn |
| Bảo tàng Peranakan (Singapore): QR cạnh hiện vật, chỉ dùng nội dung bảo tàng duyệt | đúng; trang gọi là "thử nghiệm" |
| HeriStepAI ở Bảo tàng Đà Nẵng: đeo thiết bị, > 10 ngôn ngữ | đúng |
| Luật Trí tuệ nhân tạo 134/2025/QH15 (hiệu lực 01/03/2026): phải báo người dùng đang tương tác với AI (Điều 11.1) | đúng (C đọc qua bản dịch tiếng Anh "chỉ để tham khảo" vì bản gốc là ảnh scan); Điều 3.5: dùng cá nhân phi thương mại không tính là "bên triển khai" — **cần người hiểu luật xác nhận** ⇒ (suy ra) giao diện vẫn nên có nhãn "Trợ lý AI" |
| Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (hiệu lực 01/01/2026) | đúng ⇒ (suy ra) nhớ hội thoại: phiên ngắn, không hỏi tên / số điện thoại, không log vị trí |
| Klook Nearby: 71,4 % thử, 56,7 % quay lại | số đúng; giai đoạn ghi sai (trang gọi là ra mắt, không phải beta) |
| Bài về trích dẫn (ALCE) | ChatGPT **gộp tên 2 bài khác nhau** làm một |
| Adaptive-RAG (chọn cách tìm theo độ khó) | khớp tóm tắt (bảng không có số) |

**Đề xuất của ChatGPT (đọc như ý kiến, không phải bằng chứng):** 5 hướng — câu nhiều nguồn (ưu tiên 1), hỏi lại đúng lúc (2), nhớ ngắn (3), thông tin theo ngày + an
toàn (4), thuyết minh di sản theo QR (tuỳ chọn); 3 hướng nên tránh — agent tổng quát, lịch trình đầy đủ có đặt chỗ, làm cùng lúc giọng nói / ảnh / bản đồ / nhiều ngôn ngữ.
Kiến trúc gợi ý: **luật trong code đi trước** (ý định, trường còn thiếu, mức rủi ro) ⇒ tìm 1 lần hoặc 2–3 nhánh song song ⇒ **một** lần gọi model ⇒ kiểm cuối. A đồng ý
phần lớn; khác ở chỗ đưa **chặn câu an toàn lên sớm** (lỗi tệ nhất của mình, rẻ — mẫu bảo tàng Royal Armouries [đã kiểm]).

## 5. Điều đã biết từ bản 1 (giữ gọn)

- Royal Armouries (Anh): câu về cháy / trẻ lạc / cấp cứu bị chặn trước mô hình, trả câu soạn sẵn; phần còn lại RAG 5 đoạn, không rerank. [đã kiểm]
- Moffatt v Air Canada (2024): hãng chịu trách nhiệm cho câu sai của chatbot, dẫn link đúng cũng không miễn. [B kiểm]
- Khách Việt (Agoda 03/2026 — nguồn có lợi ích, không nêu cỡ mẫu): 81 % muốn dùng AI, 28 % chủ động tin. Khách bảo tàng từng dùng AI (Musa Guide — nguồn có lợi
  ích; n = 212): 61 % tin bảo tàng hơn AI, 27 % kiểm lại câu trả lời. [B kiểm]
- Hỏi lại: LLM tự nhận ra câu mơ hồ còn kém (CLAMBER, ACL 2024) ⇒ (suy ra) dùng danh sách trường trong code. [C kiểm]
- Nhiều lượt: hệ tốt nhất vẫn yếu ở lượt sau (MTRAG / MTRAG-UN). [C kiểm]
- Tìm kiếm tiếng Việt: lai BM25 + vector thắng vector đơn ở cả 10 bộ (EACL 2026) — cùng hướng lai với hue_rag, cách trộn khác. [C kiểm]
- Repo: hỏi lại theo danh sách trường (`ytthuan/trip-advisor-agent`), tính tiền bằng code (`KhaiBoiPho/agentic-rag`); 8 repo của khảo sát 01/10 đều nhỏ. [C kiểm]

## 6. Lịch đến bảo vệ (A đề xuất — chưa chốt; ước công agent + thời gian bạn đọc / duyệt)

| Thứ tự | Việc | Ước |
|---|---|---|
| 1 | Giao diện mới (hướng đã chốt; thêm nhãn "Trợ lý AI") | ~1 tuần |
| 2 | Chặn câu an toàn + ghi "theo nguồn ngày…" cho giờ / giá / lễ hội | 2–3 ngày |
| 3 | Hỏi lại khi thiếu thông tin (danh sách trường trong code, hỏi bằng nút như TRIPO) | ~1 tuần |
| 4 | Nhớ hội thoại ngắn (3–5 lượt, phiên ngắn) | ~1 tuần |
| 5 | Lịch trình gợi ý nhỏ (thứ tự điểm theo khu vực, có nguồn) — cần dữ liệu khu vực / thời lượng ~20–30 điểm | 1–1,5 tuần |
| 6 | Câu nhiều nguồn — thử 1 lần; không vượt nhiễu thì ghi kết quả âm, dừng (**chỗ cắt đầu tiên** nếu trễ) | 1–2 tuần |
| 7 | Đóng code ~20/12, đo hồi quy, viết luận văn | ~2 tuần |

Thêm vào danh sách thử: câu hỏi 2 ý bị từ chối cả câu khi kho chỉ có một ý (thử TRIPO câu 2) — cách xử lý phải khác lần thử "trả lời một phần" ở 8.2 (bị bỏ vì làm hỏng sàn câu ngoài kho).

## 7. Chưa biết

- Kho có đúng thực tế ở câu trang phục không (chưa đối chiếu web); TRIPO đúng / sai ở câu món ăn.
- Số của các paper lịch trình sau TravelPlanner; chi phí vận hành thật của các tổ chức; khảo sát người dùng tại Huế (không tìm thấy).
- Một lần thử 10 câu, một người đánh giá — không phải phép đo; muốn đưa vào luận văn cần lặp lại có tiêu chí ghi trước.

## Phụ lục — hồ sơ kỹ thuật

- Việc: B117 (mạch 1–2), C116 / C116b (mạch 3–4), C117 (kiểm ChatGPT), B119 (thử TRIPO), B118 / B120 (review); đợt `report_agent/2026-11-01_nghien_cuu_phase_9/`;
  mục "Nghiên cứu rộng Phase 9", "Brainstorm Phase 9", "B119" trong `session_prompt/CURRENT_HANDOFF.md`.
- Hồ sơ private: `data/nghien_cuu_phase_9_2026-11-01/` (`b_mach1–2.md`, `c_mach3–4.md`, `c117_kiem_chatgpt.md`, `tripo/b119_kham_pha.md` + ảnh + JSON thô).
- Nguồn đã kiểm (chọn): `huetripo.hue.gov.vn/trip-planner` · thông cáo Expedia 14/04/2026 · `news.booking.com` Global AI Sentiment Report · `royalarmouries.org` (bản ghi
  minh bạch thuật toán) · `askmona.ai` (Peranakan) · Moffatt v Air Canada 2024 BCCRT 149 · arXiv 2402.01622, 2601.07711 · `github.com/longstnguyen/ViRE` · Luật 134/2025/QH15, 91/2025/QH15.
- Yêu cầu ChatGPT: `gửi chatgpt/2026-11-01/tìm thông tin/…` (`e45bf409b2db`); kết quả `gửi chatgpt/2026-11-01/kết quả nghiên cứu/hue_rag_phase9_research_2026-11-01.md` (private).
