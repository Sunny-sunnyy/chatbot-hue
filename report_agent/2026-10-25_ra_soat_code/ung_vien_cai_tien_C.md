# Ứng viên cải tiến từng khâu — danh sách của C (chuẩn bị đợt "tìm hướng tốt hơn", User 20:0x)

Người viết: C (Claude Opus 5.5, terminal `hue-rag-7f`) · 2026-10-25 20:41 (`date`) · A giao 20:4x · **chỉ đọc, 0 USD, chưa chạy thí nghiệm nào**.
Mốc so sánh đề xuất = **hệ thống sau 5 gói sửa** (context 5, validator citation mới từ 1a — chưa có B1 context 10 vì `p82-b1` chờ B0).
Đối chiếu để không lặp: bảng G5 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md`), tổng hợp G5
(`phase_8_1_g5_synthesis.md`), inventory (`phase_8_1_decision_inventory.md` §3–§4), spec 8.2 (`docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`).
Repo public: không có câu Golden / nội dung kho. Mọi lợi ích dưới đây là **giả thuyết**.

**Đơn giá dùng để ước** (tính lại từ tổng thật các lượt G2 8.1, `data/phase_8_1/g2/*_{pilot,rest}.meta.json` ÷ số câu): sinh context 5 ≈
**0,000133 USD / câu** (G2.0 dev 0,0160 / 120); context 10 ≈ **0,000204** (G2.1a 0,0245 / 120); reasoning `none` ở context 5 ≈ **0,000122**
(0,0146 / 120). Judge Claude = quota, 0 USD. Dev 120 / test 56 (trong kho: 88 / 41).

## 1. Danh sách chính (xếp theo lợi ích / chi phí)

| # | Khâu | Ý — vì sao có thể tốt hơn (giả thuyết) | Đã đo ở 8.1 / G5 / spec 8.2? | Cách thử (`run-experiment`) | Tiền ước | Rủi ro | Nghiên cứu ngoài? |
|---:|---|---|---|---|---|---|---|
| 1 | Đánh giá | **Mốc citation mới (gói 3c)**: tính lại "lỗi citation" của mọi mốc 7B / 8.1 / B1 theo validator mới, ra file mới — điều kiện trước cho mọi quyết định dùng chỉ số này (3c, E1–E3) | Chưa — **lý do mới C-09** (định nghĩa đổi ở 1a; C35 đã đếm: 69 → 14 trên 1.600 câu) | Không phải thí nghiệm; tất định từ file có sẵn; không ghi đè G0.6 | **0** | thấp (nhầm số cũ / mới — ghi rõ định nghĩa) | không |
| 2 | Sinh | **Reasoning `none`** — Completeness tăng có CI ở dev, rẻ hơn ~9 %, nhanh hơn ~8 % (p50 sinh 1,53 s so với 1,66 s) | **Đã đo** G2.4: Completeness +0,136 [+0,034; +0,261] p Holm 0,031; bị loại vì citation 4 → 8 (> +2). **Lý do mới C-09:** định nghĩa mới 0 → 2 (= +2, không vượt), nhưng A/A 7B Run 1 → 2 cũng 0 → 2 ⇒ nằm trong nhiễu | Tiêu chí ghi **trước**: sàn 0 câu OOS bị trả lời (dev + test); tụt cho phép citation (định nghĩa mới) ≤ +2 câu; quyết Completeness CI 95 % > 0 (Holm nếu > 1 biến thể). Dev **dùng lại** G2.4 (chỉ tính lại citation — khâu sau sinh, tất định) nhưng số dev chỉ là *tín hiệu* (tiêu chí đổi sau khi thấy số); **xác nhận trên test** bằng lượt mới, chấm cùng lượt mù với `t_baseline`. Test trong kho 41 câu ⇒ có thể chỉ ra "chưa rõ" (cỡ mẫu — ghi trước) | test 56 ở context 5: **≈ 0,007 USD**. Nếu mốc là context 10 (sau B1): dev + test 176 × ≈ 0,000186 ≈ **0,033 USD** | thấp (một tham số; luna nhận `none` — G2.4 0 lỗi kỹ thuật); số test nhỏ | không |
| 3 | Sinh / validator | **Thu hẹp E2** (spec 8.2: "lỗi thiếu `[n]`"): sau 1a lỗi còn lại chỉ loại "không có ngoặc số" — 0 / 176 ở mốc G2.0 dev + test, 0 / 176 ở B1, 2 / 176 ở 7B Run 2 ⇒ E2 có thể **NOT RUN** (tiết kiệm 0,03–0,05 USD) hoặc chỉ thử "sinh lại một lần khi không có `[n]`" trên đúng các câu đó | Spec 8.2 E2 viết **trước** C-09 — lý do mới | Luật bỏ sớm ghi trước (như E3): đếm câu lỗi trên mốc mới (free, mục 1); < số câu tối thiểu cho CI 95 % > 0 ⇒ NOT RUN, ghi lý do | **0** (đếm); nếu chạy sinh lại: ~14 câu × 0,0002 ≈ 0,003 | thấp | không |
| 4 | Đánh giá | **Bám nguồn bằng code**: tỉ lệ nhận định không có `[n]`, và citation trỏ nguồn không chứa dữ kiện (số, tên) của câu — cần **trước** E1 (trả lời một phần dễ thêm câu không căn cứ) | **Chưa** — 8.1 G2.2 chỉ số phụ "claim không nguồn" **NOT RUN** (G5 §6, 7B.2) | Thước đo, không phải biến thể: kiểm thước trước (4 phiếu đã biết mức, `run-experiment` §2) rồi tính trên mốc + G2.x có sẵn | **0** (code / sub-agent quota) | vừa (tách câu / khớp số tiếng Việt dễ sai ⇒ chỉ dùng phần đếm được bằng code: số, giá, giờ) | **có** — câu hỏi Q1 (§3) |
| 5 | API | **Ghi usage + độ trễ mỗi câu vào log** (token vào / ra, ms từng bước, số nguồn; không ghi nội dung câu hỏi) — hiện không đo được tiền / trễ trên server thật (cổng ổn định gói 3 phải ước) | Chưa (C34 ghi `logging.yaml` chỉ áp API; không có dòng usage) | Không phải thí nghiệm chất lượng; tiêu chí: cổng ổn định có số token + ms từ log; log 0 nội dung người dùng | **0** | thấp (lộ dữ liệu nếu ghi câu hỏi — cấm) | không |
| 6 | Ngữ cảnh | **Đa dạng nguồn trong context** (giới hạn số đoạn / tài liệu, hoặc MMR) — context 10 lợi chủ yếu ở câu **nhiều nguồn** (dev +0,71) và **so sánh** (+0,64) ⇒ *giả thuyết*: một phần lợi đến từ việc có thêm tài liệu khác, đạt được với ít đoạn hơn (rẻ hơn) hoặc cộng thêm khi giữ 10 | **Chưa** — 8.1 chỉ thử *thứ tự* gom theo tài liệu (6.3, không khác) và G3 small-to-big, không thử đa dạng | Tầng tìm / context trước (free, tất định): đoạn đúng trong N đoạn đưa model trên 32 câu dev có đoạn đúng + theo loại câu; chỉ khi tầng đó tốt lên mới sinh dev + test. Quyết: Completeness nhóm nhiều nguồn / so sánh (n nhỏ ⇒ ghi trước "có thể chưa rõ") | tầng tìm **0**; sinh dev + test **≈ 0,024–0,036** | vừa (cắt mất đoạn đúng thứ 2 cùng tài liệu ở câu trực tiếp — sàn: 0 câu mất đoạn đúng) | có — Q2 |
| 7 | Tìm kiếm | **Tách câu so sánh / nhiều thực thể thành truy vấn con** (luna viết 2–3 câu con, gộp kết quả bằng RRF) — câu so sánh cần đoạn của ≥ 2 thực thể; một truy vấn chung dễ chỉ ra một bên | **Chưa** (8.1 không thử viết lại câu hỏi; luna chỉ dùng để rerank G4) | Tầng tìm trước: đoạn đúng của **mỗi** thực thể trong context, chỉ trên câu `multi_source` / `comparative` dev (gắn nhãn tự động theo category); bật theo loại câu ⇒ cần bộ phân loại câu — biến thể riêng | gọi luna 1 lần / câu (~400 token) ≈ 0,0001 USD × 54 câu nhiều nguồn + so sánh (dev + test) ≈ 0,005; sinh dev + test ≈ 0,03 | vừa – cao (+1–2 s / câu; phân loại sai làm hại câu trực tiếp) | có — Q3 |
| 8 | Đánh giá | **Mở rộng bộ thử tự nhiên** (thêm 40–60 câu trong kho, nhất là nhiều nguồn / so sánh / có số) — test hiện 41 câu trong kho, nhiều kết luận 8.1 "chưa rõ" vì trần cỡ mẫu; Q1 plan E1 cũng vướng điều này | Một phần — 8.1 thêm 36 câu kín (để mốc cuối, không dùng chọn) | Theo quy trình 7A (agent soạn, agent khác kiểm, User đọc mẫu); nhãn đoạn đúng cho câu mới; ghi rõ bộ nào đã thấy / kín | **0** USD (quota + giờ User đọc mẫu) | vừa (câu do LLM soạn thiếu tự nhiên — dùng nhãn độ tự nhiên 8.1) | không |
| 9 | Ngữ cảnh / prompt | **Khớp nhãn citation**: prompt dặn "`[n]`" nhưng context gắn "`[Nguồn n]`" ⇒ đổi nhãn context về "`[n]`" (hoặc prompt nói rõ cả hai) — giảm định dạng lệch, có thể giảm "không ngoặc số" | Chưa (6.3 chỉ thử thứ tự) — lý do mới C-09 | Đổi đầu vào model ⇒ thí nghiệm đầy đủ: quyết = lỗi citation (định nghĩa mới) giảm; sàn Completeness không tụt quá nhiễu A/A, 0 OOS bị trả lời | dev + test ≈ 0,023 (ctx 5) / 0,036 (ctx 10) | thấp — **lợi nhỏ** (sau 1a lỗi đã gần 0) ⇒ xếp thấp | không |
| 10 | Tìm kiếm | **Index Qwen3-Embedding-8B** (đã duyệt provider) — dense lớn hơn có thể tìm đoạn đúng tốt hơn e5-small | **Chưa** — spec 8.1 để 8.2; spec 8.2 không có bước 8B (E1–E3) | Tầng tìm free sau khi build: đoạn đúng trong pool / context trên 32 câu dev; quyết như G1 | build ≈ 8.459 đoạn × ~85 token ≈ 0,7M token — giá OpenRouter **chưa kiểm** (A ước trước) + mỗi câu hỏi 1 lần gọi | cao (504 / 429 Nebius; build lại index = rủi ro cao; thêm phụ thuộc mạng lúc hỏi) | có — Q4 |
| 11 | API / UI | **Trả lời dạng stream** (giảm thời gian chờ thấy chữ đầu; câu trả lời hiện 3,6–4,0 s ở cổng ổn định) | Chưa | Đo thời gian tới chữ đầu / tổng; vướng: validator citation cần cả câu ⇒ phải chọn kiểm sau khi xong (UI ẩn / sửa nguồn cuối) — đổi hợp đồng API Phase 6 | 0 (đo bằng vài câu, ~0,001) | cao (đổi hợp đồng; câu bị validator từ chối đã hiện cho người dùng) | có — Q5 |
| 12 | API | **Cache câu hỏi lặp** (khóa = câu sau NFC + build record) — bớt tiền / trễ khi nhiều người hỏi giống nhau | Chưa | Chỉ đáng khi có lưu lượng thật; hiện chatbot chạy máy User ⇒ **để sau deploy** | 0 | thấp – vừa (cache cũ khi build lại — khóa theo build record) | không |

## 2. Đã có kế hoạch hoặc đã đo — không đề xuất lại

| Ý | Ở đâu | Ghi chú |
|---|---|---|
| Context 10 + NFC | spec 8.2 B1 (`p82-b1`, chờ B0) | đã đo thắng ở 8.1 |
| Trả lời một phần có chặn OOS (H8 / P1) | spec 8.2 E1 | nên chạy **sau** mục 4 (bám nguồn) |
| Pool rộng; rerank luna listwise | spec 8.2 E3a / E3b (có luật bỏ sớm) | tín hiệu 8.1 |
| Mốc người đọc cặp mù | spec 8.2 B0 | User đọc khi tiện |
| Chunker (12 biến thể), bảng 1 dòng / đoạn, tiền tố, BM25 tách từ / k1 / b, HNSW, cách trộn, reranker GPU M1 / M2, prompt P2, thứ tự context | G5 §1–§2 | **giữ** — không có lý do mới |
| Câu không dấu | G5 §1 | User 15:15 25/10 **loại khỏi phạm vi** |
| Model sinh khác | G5 3a | User 24/10: giữ `gpt-6-luna` |
| Dọn chunker (H1, S1–S3) | G5 §3 #8, đợt 3 gói sửa | không khác — chỉ vệ sinh khi build lại |

## 3. Câu hỏi cho nghiên cứu ngoài (ChatGPT — A gộp, viết prompt deep research đầy đủ theo `Session_Prompt.md` §9)

- **Q1 (mục 4):** Cách đo "bám nguồn" (faithfulness / citation precision) cho RAG tiếng Việt **bằng code hoặc LLM rẻ**, không cần nhãn người
  từng câu: phương pháp nào (claim tách câu + NLI, khớp số / thực thể, RAGAS faithfulness, ALCE citation recall / precision…) có bằng chứng tương
  quan với người chấm, và sai ở đâu với tiếng Việt? Cần URL bài / repo, số tương quan.
- **Q2 (mục 6):** Giới hạn đoạn mỗi tài liệu / MMR trong context của RAG hybrid: có nghiên cứu / benchmark nào cho thấy đa dạng tài liệu giúp câu
  nhiều nguồn mà không hại câu một nguồn? Tham số λ / số đoạn mỗi tài liệu thường dùng; cách đo.
- **Q3 (mục 7):** Query decomposition cho câu so sánh / nhiều thực thể (ví dụ "least-to-most", "self-ask", sub-question RRF): khi nào lợi so với một
  truy vấn, chi phí độ trễ, cách bật theo loại câu; bằng chứng cho corpus nhỏ (vài nghìn đoạn).
- **Q4 (mục 10):** So sánh `multilingual-e5-small` với `Qwen3-Embedding-8B` (và dòng nhỏ hơn) trên truy hồi tiếng Việt (MTEB / VN-MTEB, Zalo
  legal…); giá OpenRouter hiện tại cho Qwen3-Embedding-8B; lỗi 504 / 429 thường gặp và cách gọi chịu lỗi.
- **Q5 (mục 11):** Mẫu thiết kế stream câu trả lời RAG khi phải **kiểm citation sau cùng** (buffer theo câu, kiểm từng câu, gửi nguồn cuối) — có
  hệ thống / thư viện nào làm, đánh đổi gì.

## 4. Gợi ý thứ tự cho A (đề xuất, không kết luận)

1. Mục 1 (free) ⇒ quyết mục 3 (free) ⇒ mục 2 (≈ 0,007 USD, xác nhận test) — ba việc này dùng lại dữ liệu có sẵn, gần như không tốn.
2. Mục 5 (free, một dòng log) — đi cùng gói sửa kế tiếp hoặc 1b.
3. Mục 4 (thước đo) trước E1 của spec 8.2; mục 8 song song nếu User có giờ đọc mẫu.
4. Mục 6, 7 (tầng tìm free trước, sinh chỉ khi tầng tìm tốt lên) — sau khi có nghiên cứu Q2 / Q3.
5. Mục 9, 10, 11, 12: để sau (lợi nhỏ, rủi ro cao, hoặc cần deploy).

Tổng tiền nếu làm mục 1–3, 6, 7 ở context 5: ≈ 0,007 + 0,036 + 0,036 ≈ **0,08 USD** (ước, chưa tính E1–E3 của spec 8.2).

## 5. Giới hạn

- Số tiền / độ trễ là ước từ log 8.1 (luna, context 5 / 10); chưa pilot. Mục 10 chưa có giá OpenRouter.
- Lợi ích mọi mục là giả thuyết; bộ thử nhỏ (32 câu dev có đoạn đúng, 41 câu test trong kho) nên nhiều mục có thể ra "chưa rõ" — ghi trước ở từng plan.
- C không đọc câu Golden / câu kín để lập danh sách; nhận xét theo loại câu lấy từ bảng G5 theo loại câu (số đã công bố).
