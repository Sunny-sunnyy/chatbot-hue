# Báo cáo cho bạn: Nghiên cứu rộng trước Phase 9 (trợ lý du lịch - văn hoá)

**Cập nhật lần cuối: 16:13 01/11/2026 — bản 2: thêm kết quả ChatGPT (đã kiểm 9 ý), thử Huế TRIPO trên 10 câu, hướng Phase 9 bạn chọn, lịch đến bảo vệ.**
Trước: 15:28 01/11/2026 — bản 1 sơ bộ (Codex + kiểm tay; review B118 đạt). Người viết: A · Tra + kiểm: B (thực tế, người dùng, thử TRIPO), C (paper, repo, kiểm
ChatGPT) · Review bản 2: B (B120). Tiền: 0 USD API cho nghiên cứu; thử hue_rag 11 câu ≈ 0,004 USD (~100 đồng).

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
