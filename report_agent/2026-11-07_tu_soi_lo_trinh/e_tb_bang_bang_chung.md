# Bảng bằng chứng cho đồ án — theo khâu (E-tb, 12:58 07/11/2026)

Việc A giao: nguồn cho quyển báo cáo + slide. 0 USD, chỉ đọc. Chỉ có số và loại câu — không chép kho, Golden hay câu kín.
**Nguồn chính:**
- `bao_cao_he_thong/91_BAO_CAO_SO_SANH_PHUONG_AN.md` §2.1 — 67 quyết định Phase 0 → 8.2, đã review 2 vòng; số `#n` dưới đây là số dòng của bảng đó.
- `10_BAO_CAO_DANH_GIA.md` §1, `07_BAO_CAO_SINH_CAU_TRA_LOI_API.md` §1 + mục theo ngày, `08_BAO_CAO_HOI_BANG_ANH.md` §1.
- `Project_Status.md` §2–§4; report đợt cổng `report_agent/2026-11-06_giao_dien_cong/`.

E **không** đối chiếu lại từng số với file gốc. Bảng so sánh phương án đã đối chiếu 115 khẳng định; các số Phase 9–10 lấy từ báo cáo khâu. Trước khi đưa lên slide, nên đối chiếu số nào in lớn.

## Nhãn "ai đo"

- **[Claude]**: judge Claude chấm điểm 1–5 (Đúng / Đủ / Trúng ý), mù, so theo cặp, bootstrap + Holm.
- **[Người]**: User đọc (B0 cặp mù 01/11; duyệt độ tự nhiên câu kín). Mốc người chỉ tham khảo.
- **[Máy]**: code đếm, tất định, không cần người chấm (đoạn đúng, giống byte, latency, USD, kiểm cuối).
- **[2 agent]**: hai sub-agent Claude chấm độc lập theo phiếu.
- **[Chưa đo]**: đã làm / định làm, chưa có số.
- **[1 lần]**: một lượt đo, chưa lặp.

## 1. Số của chatbot đang chạy (mốc để trình bày)

| Thước | Số | Ai đo · nguồn |
|---|---|---|
| Golden 176 (158 trong kho + 18 ngoài kho): từ chối nhầm | **12 / 158** (sau tìm thêm B2: 4–6 / 158) | [Máy] · DANH_GIA §1, SINH §1 |
| Câu ngoài kho bị trả lời | **0** (Golden, bộ kín 40, bộ an toàn) | [Máy] |
| Điểm Đúng / Đủ / Trúng ý (129 câu tự nhiên) | **4,71 / 4,58 / 4,72** — lượt cuối Phase 1–8, 01/11 | [Claude] · E13 |
| Bộ kín 40 câu chưa ai thấy | Đủ **4,18** (Golden 4,58) ⇒ số Golden **lạc quan** | [Claude] · E13 |
| Bộ an toàn 32 câu | đảo cảnh báo **0**; sai điều kiện mới 2 (đúng ngưỡng ≤ 2) | [Claude tách ý] + [Máy] |
| Lỗi trích dẫn tới người dùng | **0 / 489** lần sinh | [Máy] |
| Tới chữ đầu (trình duyệt) | trước định tuyến 1,23 / 2,61 s (p50 / p95, 38 câu) · sau B1 câu về Huế 3,57 / 6,57 s · #6 song song −1,37 s [0,34; 2,14] | [Máy] [1 lần] · SINH §1, mục 05/11 |
| Tiền / câu | ≈ **0,00025** USD (RAG 1–8) · ≈ 0,00031 (tìm thêm) · đường web ≈ 0,0018 | [Máy] giá đủ |
| Yêu cầu User (28/10) | p50 ≤ 3 s, p95 ≤ 5 s, ≤ 0,0005 USD | — |

## 2. Bảng theo khâu — quyết định · phương án đã thử · kết quả

| Khâu | Quyết định đang chạy | Đã thử và **bỏ** (vì sao) | Kết quả có số | Ai đo · nguồn |
|---|---|---|---|---|
| Kho | Kho đóng (closed-world), 204 file / 5 lĩnh vực; 2 đợt sửa kho + giờ mở cửa | Đưa file danh mục vào chỉ mục (không khác, loại) | Sửa kho "không làm hỏng", **không thấy tốt hơn** (thước không nhạy) | [Claude] [1 lần] · #3–#8 |
| Golden | 176 câu do AI viết, người duyệt; 120 thử / 56 kiểm; bỏ 29 câu không tự nhiên | — | Kappa độ tự nhiên 0,765; kết luận không đổi khi bỏ | [Người] + [Claude] · #10, #56 |
| Chia đoạn | Mỗi khối Markdown một đoạn, không gộp; bảng dài tách từng dòng; tiền tố tiêu đề đầy đủ | Gộp 256 / 384 / 512 token (kém), mở rộng cả mục (mất 8 câu), rút gọn tiền tố (mất 7 / 8 câu), gộp dòng bảng (không khác) | 12 biến thể, **không biến thể nào thắng** | [Máy] đoạn đúng · #13–#18 |
| Nhúng (vector) | e5-small 384 chiều, chạy CPU máy | **Qwen3-Embedding-8B** (API): mất đoạn đúng 3 dev + 3 test, chậm +2,2 s | Một phép so có chấm duy nhất cho model vector | [Máy] [xác nhận nhóm kiểm] · #21 |
| Từ khoá | BM25 tách âm tiết, k1 1,5 / b 0,75, RRF k 60 | Cặp âm tiết, pyvi tách từ (kém); các k1 / b / k khác (không tốt hơn) | — | [Máy] · #23–#24 |
| Lưu | Qdrant 1 collection, HNSW | Tìm chính xác: giống hệt 108 / 108 câu ⇒ giữ HNSW | — | [Máy] · #26 |
| Tìm | Vector + BM25 trộn RRF, pool 30; chuẩn hoá NFC | Pool 100 (mất 1 câu); reranker GPU (mất 1–3 câu); **luna chọn đoạn**: tầng tìm +9 câu nhưng tầng trả lời kém + 3,8× tiền | Chỗ nghẽn = **xếp hạng**; mọi sửa xếp hạng trượt sàn "0 câu mất" | [Máy] + [Claude] · #28–#35 |
| Ngữ cảnh | **10 đoạn** (trước 5) — **thí nghiệm duy nhất thắng** ở rà soát 8.1 | Đảo thứ tự đoạn (không khác) | Đủ dev +0,26 [+0,08; +0,48], test +0,27 [+0,02; +0,59]; câu kín Đủ **+0,82**, Đúng +0,70, 0 câu tụt; B0: 3 cặp bản 5 đoạn từ chối nhầm | [Claude] + [Người] · #37, #57, #59 |
| Sinh / lời dặn | gpt-6-luna; thiếu một vế ⇒ từ chối cả câu; kiểm `[n]` bằng code | Trả lời một phần (câu ngoài kho bị trả lời — phạm sàn); suy luận `none` / `low` (kém); luật kiểm sau sinh (7 / 10 cờ là câu có ích) | **Model sinh chưa từng so có chấm** — chỗ hở | [Claude] · #36, #39, #42, #44 |
| Trợ lý: định tuyến (B1) | Model phân loại 4 tuyến; khẩn cấp ⇒ câu soạn sẵn 113 / 114 / 115 / 112 | **Luật từ khoá khẩn cấp:** kín bắt 0 / 8, chặn nhầm 2 / 8 (bỏ); **tắt suy luận định tuyến** #1: nhanh 0,2–0,35 s nhưng 2 câu an toàn bị xếp ngoài phạm vi (bỏ) | Định tuyến bắt khẩn cấp 10 / 10 kín; chữ đầu chậm ~2 s | [Máy] · SINH mục 03–04/11 |
| Trợ lý: tìm thêm (B2) | Model gọi `tim_kho` thêm ≤ 2 lần | — | 18 câu nhiều nguồn Đủ **+1,17** [+0,44; +2,00]; 1 câu an toàn sai mới (sửa ở B3) | [Claude] · SINH §1 |
| Trợ lý: nhớ hội thoại (B3 / B3b) | Nhớ **câu hỏi** 3 lượt, không nhớ câu trả lời | Nhớ cả câu trả lời: lượt kín mượn nguồn đối tượng khác (bỏ) | Kín: nhớ tên 10 / 10; hỏi tiếp +0,60; mượn nguồn 6 / 6 từ chối đúng | [Claude] + [Máy] · SINH mục 03/11 |
| Trợ lý: hỏi lại (B4) | Code quyết hỏi (thẻ nút); công cụ "hỏi lại" của model **gỡ** | Model tự hỏi lại: **âm 2 vòng** (tự ghi dòng "Tổng"; thiếu cảnh báo ở 2 câu) | — | [Máy] + [Claude] · SINH mục 05/11 |
| Trợ lý: tính tiền (B5c) | **Không bật** | Code tính tiền: phép tính đúng 8 / 8 nhưng mất điều kiện miễn vé ⇒ **âm 2 vòng**, lưu nhánh | Bài học: "phép tính ⇒ code" vẫn hỏng nếu model chọn sai dòng giá | [Máy] · SINH mục 05/11 |
| Trợ lý: lịch trình (B5, B171) | Câu gõ tự do **tắt**; đi qua **biểu mẫu, code quyết** (cổng đợt 1) | Bộ kín v1: câu không tự nhiên ⇒ không dùng; **kín v2 (User duyệt câu): 3 / 5 < 4 / 5** | Lỗi tìm ra: từ chối khi hỏi kèm (chứng minh bằng code, E20); "đi dày" không làm được bằng dữ liệu kho (E21) | [2 agent] khớp 15 / 15 ô + [Người] · SINH mục 06/11 |
| Trợ lý: thời tiết (B5b) | Open-Meteo, số do code dựng; cờ tắt → bật khi merge cổng (User 07/11) | — | Đạt luật ghi trước; cổng sau merge 196 test | [Máy] · SINH mục 06/11 |
| Trợ lý: tra web (B6) | **Bật**: kho từ chối ⇒ Serper 1 lần ⇒ mục "Từ web (chưa kiểm)", code kiểm link / tiền / thiên tai | Thêm "đang" vào luật thời gian thực (chặn nhầm 1 câu đúng — không thêm) | Đạt luật ghi trước + kín ×2; mục web tới sau ~13 s; 0,0018 USD | [Máy] + [Claude] · SINH mục 05/11 |
| Tốc độ | Streaming; **#6** chạy trả lời song song định tuyến | Tắt ghi đệm OpenAI (đắt hơn — bỏ) | #6: chữ đầu −1,37 s; 228 / 228 chuỗi giống byte; an toàn 90 lượt 0 vi phạm | [Máy] |
| Ảnh (Phase 10) | Gợi ≤ 3 tên trong 42 tên, **người dùng xác nhận**; cờ tắt | **SigLIP 2** chạy máy (3 cách, âm: ảnh mèo cũng ra tên Huế); thước gốc âm (2 / 5 ảnh không phải Huế bị gán tên) | Đúng trong 3 gợi ý 22 / 25; ≈ 0,0004 USD / ảnh; p95 6,3–9,1 s (chưa đạt 5 s) | [Máy] · HOI_BANG_ANH §1 |
| Giọng nói (Phase 10) | Plan G2 duyệt (sherpa-onnx) | Web Speech (bỏ ở spec) | **[Chưa đo]** — chờ thu 40 câu | — |
| Giao diện | React + Vite; cổng đợt 1 (dòng "Nguồn", Khám phá 204 bài, biểu mẫu) | Số `[n]` trong chữ (User bỏ) | S4 review đạt; bundle 106 KB gzip; Q-F / Q-G / Q-N **đang đo (C)** | [Máy] · `s4_review_*.md` |
| Đánh giá | Judge Claude chính, luna phụ; chấm mốc + biến thể cùng lượt mù | — | Claude ↔ luna khớp 0,892–0,960; nhiễu chỉ-chấm 2 / 88 ≪ nhiễu cả đường 10 / 83 | [Claude] · #51–#53 |
| Deploy | — | — | **[Chưa đo]**: RAM 1,9 GB app + Qdrant (đo 07/11); chưa chạy trên AWS | [Máy] · `e_dep_chuan_bi_deploy.md` |

## 3. Câu chuyện mạnh nhất khi bảo vệ (đề xuất E)

1. **"Thử nhiều, giữ ít — có luật ghi trước."**
   - Rà soát 8.1 thử lại 56 quyết định cũ; **chỉ 10 đoạn thắng**.
   - Các thử nghiệm Phase 9 cũng bị bỏ có lý do bằng số: luật khẩn cấp, tắt suy luận, hỏi lại do model, tính tiền, lịch trình câu tự do, SigLIP 2, Qwen3-8B.
   - Đây là bằng chứng phương pháp, mạnh hơn kể thêm tính năng.
2. **"An toàn trước, kho đóng."** 0 câu ngoài kho bị trả lời; đảo cảnh báo 0; câu khẩn cấp ra câu soạn sẵn; web tách riêng "chưa kiểm".
3. **"Phép tính / thứ tự / trường bắt buộc ⇒ code."** Lịch trình đi biểu mẫu, code xếp. B5c cho thấy cả việc "code tính" cũng hỏng khi model chọn sai dữ liệu đầu vào ⇒ nói được giới hạn.
4. **Trung thực về thước:**
   - bộ kín cho điểm thấp hơn Golden 0,4;
   - mốc người chỉ tham khảo;
   - model sinh chưa từng so;
   - tốc độ sau định tuyến vượt sàn ở p95.

## 4. Lỗ hổng bằng chứng nên lấp trước bảo vệ (theo thứ tự lợi / tiền)

1. **Lượt đo chốt trên bản deploy** (Golden + an toàn 32 + kín còn lại nếu có + latency trên máy AWS). Hiện mọi số đo trên máy User.
2. **Một số tuyệt đối Phase 9:** từ lượt cuối 01/11, Golden chỉ báo chênh theo cặp ⇒ cần một bảng Đúng / Đủ / Trúng ý của bản cuối (B7).
3. **Mốc người nhỏ cho bản cuối** (vd User đọc 20 câu bản cuối, không chấm điểm, chỉ đạt / không) — hiện [Người] chỉ có B0 (5 ↔ 10 đoạn).
4. Latency p95 câu về Huế sau định tuyến (6,57 s một lần đo, trước #6) ⇒ đo lại một lần trên bản cuối.
5. Giọng nói: không có số ⇒ nếu giữ trong đồ án phải đo G2; nếu cắt thì ghi "hướng phát triển" (E đề xuất cắt — `tu_soi_E.md` §4).
