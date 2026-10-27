# C58 — Thời gian chờ của /api/chat nằm ở khâu nào? (chatbot đang chạy, context 5)

Người làm: C (Claude Opus 5.5, `hue-rag-5b`) · 12:00 27/10/2026 +0700 (`date`) · Việc: C58 (A giao). Điều tra theo skill systematic-debugging; **không đổi code `main`** — đo tạm trong
worktree `/tmp/c_lat` (đã gỡ). **Tiền thật: 0,0074884 USD** (45 lần gọi `gpt-6-luna`, token do generator trả về, đo tạm ghi ra file; trần 0,01). File này không chép câu hỏi — chỉ số đếm.

## Cho bạn (3 dòng)

- Gần như **toàn bộ** thời gian chờ là lúc model viết câu trả lời (≈ 98 %). Tìm đoạn chỉ ~40 ms, dựng ngữ cảnh ~2 ms, kiểm trích dẫn ~0 ms, đường HTTP ~2 ms.
- Khoảng "dư 1,5 s" giữa đo qua API (B65) và đo trong code thử nghiệm **không phải do API chậm**, mà do **bộ câu khác nhau**: 22 câu B tự viết khiến model viết dài gần gấp đôi
  (TB 176 so với 98 token), và độ dài đó giải thích được ~1,1 s chậm hơn. Cùng 22 câu dev, qua API mất p50 2,15 s — gần bằng trong code thử nghiệm hôm 25/10 (1,97 s).
- Không có chỗ "thừa" nào để cắt ở đường API. Muốn nhanh hơn phải làm model viết ít hơn hoặc hiện chữ dần — cả hai đụng tới chất lượng / thiết kế, cần thí nghiệm riêng.

## 1. Cách đo

- **Đo tạm theo khâu** trong `backend/api/routes/chat.py` (worktree `main` `a94ebc5`; diff lưu private `data/phase_8_2/latency_2710/c58/instrumentation.diff`): mốc
  thời gian trước / sau `retrieval_service.search` (kèm `trace.timings_ms` sẵn có: dense = nhúng câu hỏi e5 CPU + truy vấn Qdrant; BM25; RRF), dựng ngữ cảnh, gọi model
  (kèm `latency_ms` và token của chính generator), kiểm citation + dựng phản hồi; ghi một dòng JSON mỗi câu (không ghi nội dung câu, chỉ sha).
- **Server thật** `uvicorn api.app:app` cổng 8014 (8011 bị tiến trình khác chiếm), `/health` 5 / 5 ready, context 5 như chatbot đang chạy.
- **Câu hỏi:** 22 câu B65 tự viết + 22 câu dev chọn bằng seed 20261024 (20 câu chính + 2 câu ngoài kho), **xen kẽ** từng câu trong **một** lượt tuần tự (11:55–11:57) — hai bộ
  cùng server, cùng phút, nên không lẫn dao động theo giờ. Client: bản chép `run_latency.py` của B65 (thêm `--questions`), 1 câu khởi động không tính.
- Script phân tích private `c58_analyze.py` ⇒ `c58_analysis.json`; log server 0 dòng lỗi; 44 / 44 câu HTTP 200.

## 2. Thời gian theo khâu (ms; p50 / p95 / TB)

| Khâu | 22 câu tự viết | 22 câu dev |
|---|---|---|
| **Client đo (đầu–cuối)** | 3.357 / 5.429 / 3.249 | 2.191 / 3.315 / 2.323 |
| Server tổng | 3.354 / 5.427 / 3.247 | 2.189 / 3.313 / 2.321 |
| HTTP + client (= client − server) | 2 / 3 / 2 | 2 / 3 / 2 |
| Tìm đoạn (trong `to_thread`) | 38 / 85 / 52 | 41 / 69 / 44 |
| — nhúng câu hỏi + Qdrant dense | 33 / 81 / 47 | 37 / 64 / 40 |
| — BM25 / RRF | 3 / 0,1 | 4 / 0,1 |
| Dựng ngữ cảnh | 2 / 3 / 2 | 2 / 2 / 2 |
| **Gọi model sinh** (gồm mạng) | **3.269 / 5.386 / 3.193** | **2.152 / 3.275 / 2.275** |
| Kiểm citation + dựng phản hồi | 0 / 0,1 / 0 | 0 / 0,1 / 0 |
| Token model viết ra (gồm suy luận) | 178 / 364 / 176 | 86 / 207 / 98 |
| Token vào | 941 / 1.391 / 983 | 952 / 1.202 / 966 |

Gọi model chiếm ≈ 97–98 % thời gian. Trên 44 câu, thời gian gọi model ≈ **1,16 s + 11,5 ms × token ra** (tương quan **0,97**).

## 3. Nguyên nhân (đã chứng minh / giải thích được / giả thuyết)

- **Đã chứng minh (cùng lượt, xen kẽ, cùng server):** khoảng dư ~1,5 s **không** nằm ở HTTP, tìm đoạn, dựng ngữ cảnh hay kiểm citation (cộng lại < 50 ms). Nó nằm ở **bước sinh**.
- **Giải thích được bằng token ra, chưa can thiệp:** thời gian sinh tương quan 0,97 với số token model viết ra; câu tự viết ra ~1,8× token so với câu dev, p50 chậm hơn 1,12 s.
  B67 kiểm lại trong từng bộ câu: thêm biến "bộ câu" vào hồi quy theo token ra thì biến đó chỉ +24 ms ⇒ chênh giữa hai bộ gần như hết sau khi tính token ra. Token vào gần
  bằng nhau (941 / 952) nên không phải do ngữ cảnh dài. Chưa thử đổi độ dài câu trả lời để xác nhận nhân quả.
- **Giả thuyết:** chênh ~0,2 s giữa cùng câu dev qua API (p50 2,15 s) và trong code thử nghiệm 8.1 (1,97 s, token ra TB 98 / 98) là dao động theo lúc gọi — hai lượt khác ngày
  (27/10 so với 25/10) và khác cách gọi (tuần tự so với đồng thời 4), nên chưa tách được.
- **Giả thuyết (chưa đo):** câu tự viết hỏi mở hơn (gợi ý, so sánh, "nên…") nên câu trả lời dài hơn; hoặc model suy luận nhiều hơn. Usage hiện chỉ lưu tổng token ra, chưa tách
  token suy luận ⇒ chưa phân biệt được.

## 4. Cách sửa nhỏ nhất (chưa sửa)

- **Không có chỗ thừa** ở đường API để cắt; tìm đoạn (~40 ms) đã nhỏ so với 2–5 s.
- Muốn giảm thời gian chờ phải giảm **token ra** hoặc đổi trải nghiệm — đều là thí nghiệm có tiêu chí chất lượng ghi trước:
  - giảm mức suy luận: đã thử 27/10 (R1) — token ra ~0,72× nhưng phạm sàn câu từ chối;
  - nhắc model trả lời gọn / đặt trần token ra: nhanh hơn ~11,5 ms mỗi token bớt được, nhưng có thể làm thiếu ý (lỗi "trả lời quá gọn" đã thấy ở 9 / 88 câu);
  - hiện chữ dần (streaming): không đổi tổng thời gian, chỉ đổi thời gian thấy chữ đầu; phải thiết kế lại cách kiểm citation (nghiên cứu 26/10 khuyên giữ đệm toàn bộ).
- **Một việc nhỏ đáng làm trước (đo, không phải tối ưu):** cho `/api/chat` ghi log token vào / ra (và token suy luận nếu SDK trả) + thời gian từng khâu mỗi câu, không ghi nội
  dung — hiện route không ghi usage, nên mọi số tiền / tốc độ qua API đều phải ước hoặc đo tạm như lần này. Việc này đổi code `main` ⇒ A / User quyết.

## 5. Giới hạn

- Một lượt, 22 + 22 câu, tuần tự, máy User; p95 dựa trên 1–2 câu chậm nhất. Không đo lúc gọi đồng thời.
- Đo ở context 5 (chatbot đang chạy); context 10 (B65) không khác về thời gian chờ.
