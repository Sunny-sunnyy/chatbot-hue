# Ứng viên cải tiến khâu dựng kho (chia đoạn, embedding, BM25, Qdrant, build) — danh sách của B

Người viết: B (Claude Opus 5.5, terminal `hue-rag-c3`) · 2026-10-25 21:55 +0700 (`date`) · A giao 21:4x · **chỉ đọc, 0 USD, chưa chạy thí nghiệm nào**.
Mốc so sánh đề xuất = **hệ thống sau 5 gói sửa** (như C). Đối chiếu để không lặp: `ung_vien_cai_tien_C.md` (C #10 index Qwen3-8B, #6 đa dạng nguồn, #7
tách câu hỏi — **không lặp ở đây**), bảng G5 (`report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_decision_table_draft.md` §1–§2), spec 8.2,
nghiên cứu cũ `gửi chatgpt/2026-10-24/kết quả nghiên cứu/phase_8_rag_retrieval_2026_10_24.md` (gọi tắt **NC24**). Repo public: không có câu Golden / nội dung kho.
Mọi lợi ích dưới đây là **giả thuyết**.

**Số dùng để ước** (đếm 21:5x, chỉ số đếm): kho 205 file, **675.520 token** `o200k_base` (trung vị 2.181 / file, p90 8.079, lớn nhất 12.238); 8.459 đoạn.
Sinh context 5 ≈ 0,000133 USD / câu (C, từ log 8.1) ⇒ dev + test 176 câu ≈ **0,023 USD**. Build lại index e5 trên CPU = **0 USD**, nhưng ghi Qdrant ⇒ cần
duyệt đích thử `hue_*` (như 8.1 G3). Judge Claude = quota.

## 1. Danh sách chính (xếp theo lợi ích / chi phí)

| # | Khâu | Ý (giả thuyết) | Đã đo ở 8.1 / G5 / spec 8.2? | Cách thử (`run-experiment`) | Tiền ước | Rủi ro | Câu hỏi cụ thể cho ChatGPT |
|---:|---|---|---|---|---|---|---|
| 1 | Kho + build | **Sửa 22 mâu thuẫn "chắc" (C32) rồi build lại** — câu trả lời sai vì kho tự mâu thuẫn thì không khâu tìm / sinh nào cứu được | **Chưa** — C32 chỉ liệt kê (139 mục, private), G5 không đo | Không phải đổi thuật toán: User duyệt từng sửa (sao lưu `meta/`, diff); build lại theo mục "Build lại index" (`full_corpus_rag.md`); đo trên câu chạm file đã sửa (tầng tìm free + sinh dev / test) — **đổi kho làm đổi mốc** ⇒ chấm baseline cùng lượt mù, không so với số 8.1 | build 0; sinh ≈ 0,023 | vừa (ghi Qdrant + đổi kho; User mất giờ duyệt); trong 69 mục "có thể" cần tra ngoài | Với 22 mục mâu thuẫn chắc: nguồn chính thức nào (cổng tỉnh, Trung tâm Bảo tồn Di tích Huế) có số liệu hiện hành (giá vé, giờ mở cửa, năm xây)? — A gửi **danh sách private** riêng, không dán vào repo |
| 2 | Chia đoạn (bảng) | **Câu hoá hàng bảng giá** — mỗi hàng thêm một câu "Điểm X — loại vé Y — đối tượng Z — giá …" (giữ hàng gốc làm bằng chứng) + một **đoạn tổng quan bảng** dựng bằng luật (tên bảng, các loại vé, chính sách miễn giảm) làm "đường dẫn" tới bảng. Nhắm F2 (bảng giá ngoài top-30, Phase 6) | **Một phần** — H3 (gộp dòng bảng) không khác, trần 7 câu; câu hoá hàng / đoạn tổng quan **chưa đo**; NC24 §5 đề xuất | Tầng tìm trước (free): build collection thử `hue_*`, đo đoạn đúng trong pool 30 / context 5 trên câu có đoạn đúng là hàng bảng (G0.3); chỉ khi tầng tìm tốt lên mới sinh dev + test. Ghi trước "có thể chưa rõ" (≤ 7 câu) | build 0; sinh ≈ 0,023 | vừa (đổi chunker = rủi ro cao theo WORKFLOW; đoạn câu hoá có thể vượt huydang 256 — xem #4) | Có nghiên cứu / benchmark nào đo **recall truy hồi** (không phải table QA) khi câu hoá từng hàng bảng so với giữ hàng Markdown, với embedding nhỏ đa ngôn ngữ (e5-small) và BM25? Đoạn "tổng quan bảng" có làm loãng top-k không? |
| 3 | Chia đoạn (biểu diễn A) | **Thêm một dòng ngữ cảnh tất định** đầu mỗi đoạn (domain / loại tài liệu từ đường file, ví dụ "Vé tham quan — Đại Nội") — 8.1 cho thấy **bớt** ngữ cảnh làm hỏng (chỉ heading gần nhất: mất 7 câu; không tiền tố: mất 8) ⇒ *giả thuyết*: thêm ngữ cảnh rẻ có thể giúp | **Chưa** (G3 §3.5 chỉ thử bớt). Contextual retrieval bằng LLM: NC24 §6 ([Chưa rõ] cho tiếng Việt) | Biến thể tất định trước (free): build thử, tầng tìm trên 32 câu dev có đoạn đúng (sàn: 0 câu mất đoạn đúng); LLM chỉ pilot 20–30 tài liệu có lỗi thật nếu tất định có tín hiệu | tất định 0; LLM toàn kho ≈ **4,7 USD** (44,8 triệu token vào — mỗi đoạn kèm cả tài liệu — + 0,25 USD ra; **vượt trần**), pilot 20 tài liệu ≈ 0,1–0,4 | vừa (đoạn dài hơn ⇒ có thể vượt huydang 256; đổi chunker) | Contextual retrieval (Anthropic 2024) có bản lặp lại độc lập nào với **đoạn ngắn (~85 token)** và tiêu đề + heading đã có sẵn trong đoạn? Phần lợi đến từ tóm tắt tài liệu hay từ tên thực thể? Có biến thể tất định nào được đo? |
| 4 | Chia đoạn | **Bỏ ràng buộc tokenizer huydang 256** (model không chạy ở runtime) khi build lại — điều kiện cần cho #2, #3 (đoạn dài hơn) và tránh build dừng vì huydang sau B-11 | **Đã đo một phần** — G3 H1: 8.398 đoạn (−61), 0/32/0 đoạn đúng, không khác; **Completeness chưa đo**; G5 §3 #8 đề xuất dọn | Gộp vào lần build lại #1 (không chạy riêng): tầng tìm (đã có H1) + sinh dev / test cùng lượt mù với mốc | ≈ 0,023 (nếu sinh) | thấp (H1 đã đo không hại tầng tìm) | — (không cần) |
| 5 | BM25 | **Tăng trọng số tiêu đề / heading cho BM25** (lặp tên thực thể trong văn bản thưa, hoặc thêm một vector thưa riêng cho tiêu đề + heading và trộn RRF) — câu hỏi người dùng thường gọi tên địa điểm / món; dense đã thấy tiêu đề trong Representation A | **Chưa** — 8.1 đo cách tách từ (âm tiết / cặp / pyvi) và k1 / b, không đo trọng số trường | Chỉ đổi văn bản thưa (dense giữ nguyên): build thử, tầng tìm dev (G1 / G4K harness); quyết: đủ đoạn đúng trong context 5 không giảm + MRR CI > 0 sau Holm | build 0; sinh ≈ 0,023 nếu tầng tìm tốt lên | thấp – vừa (đổi sparse state ⇒ build lại; dễ ưu tiên đoạn "tổng quan" hơn đoạn có đáp án) | BM25F / trọng số trường cho RAG đoạn ngắn: bằng chứng nào cho thấy tăng trọng số tiêu đề giúp truy hồi trong kho nhỏ (vài nghìn đoạn) có tiêu đề lặp ở mọi đoạn? Cách làm với một vector thưa (Qdrant sparse) — lặp token hay hai vector? |
| 6 | Embedding | **Dense local mạnh hơn e5-small** (`bge-m3` 1.024 chiều / `Qwen3-Embedding-0.6B`) — VN-MTEB và benchmark cộng đồng xếp cả hai trên dòng e5 (NC24 §2) | **Chưa** — và **ngoài danh sách đã duyệt**: User 24/10 "dense chỉ e5-small + Qwen3-8B" ⇒ **phải hỏi User trước** | Nếu User mở: build collection thử (CPU), tầng tìm dev trước; đo thời gian embed câu hỏi trên CPU (chatbot chạy máy User) | 0 USD (local); CPU build ~10–40 phút (chưa đo) | vừa – cao (model mới cần duyệt; RAM / độ trễ CPU; reindex) | `bge-m3` dense so với `Qwen3-Embedding-0.6B` trên **CPU**: thời gian embed một câu ~15 từ và 8.500 đoạn ~85 token (đã có đo nào?); `bge-m3` sparse (lexical weights) có thay được BM25 âm tiết cho tiếng Việt không? |
| 7 | Build + Qdrant | **Build lại không ngừng phục vụ**: tên collection / đường sparse state / build record lấy từ `settings.yaml` thay hằng trong code (B-06), build vào đích mới rồi đổi runtime (cutover), giữ đích cũ tới khi User duyệt xóa; Qdrant snapshot trước khi xóa | **Chưa** (vận hành, không phải chất lượng); hôm nay chỉ có cách "tại chỗ" (chatbot ngừng tới khi build xong) | Không phải thí nghiệm chất lượng; tiêu chí: build đích mới khi runtime vẫn trả lời; cutover = sửa settings + khởi động lại; T1 trên đích mới giống byte khi kho không đổi | 0 | vừa (chạm runtime khởi động; cần duyệt ghi / xóa Qdrant) | — (không cần) |
| 8 | Build | **Ghi thống kê đoạn vào build record** (số đoạn mỗi domain, phân bố token theo 3 tokenizer, đoạn lớn nhất) — biết ngay kho đổi có đẩy đoạn sát giới hạn không (huydang 255 / 256 hôm nay), thay cho CLI preview sẽ gỡ (B-04) | Chưa | Không phải thí nghiệm; một khối JSON thêm vào record (schema v3 ⇒ v4 **hoặc** file cạnh record để không đổi freshness) | 0 | thấp (đổi schema record ⇒ runtime đọc — nên để file cạnh) | — |
| 9 | API khởi động | **Đo thời gian khởi động thật** qua `create_app` (nạp e5 ~2,45 s + import ~4,4 s + hash 205 file + kiểm Qdrant) để biết có cần tối ưu không | Chưa (B-08 đã rút: đo cũ không đi đường thật) | Đo 3 lần khởi động uvicorn thật (log thời gian từng bước — gộp với ý C #5 ghi usage / độ trễ); chỉ tối ưu nếu > ngưỡng User đặt | 0 | thấp | — |
| 10 | Đánh giá (theo khâu dựng kho) | **Chỉ số "trải nghiệm người dùng"** bên cạnh điểm judge: câu mà API trả lỗi (500 / 409 / 503) tính 0 điểm — hôm nay judge chấm cả câu người dùng không thấy (C-09 / R-02); dùng cho mọi so sánh sau khi build lại | Chưa (lý do mới C-09) | Không phải biến thể: tính lại trên file có sẵn (free, tất định); báo song song, không thay chỉ số chính đã khóa | 0 | thấp (đổi cách báo số ⇒ ghi rõ định nghĩa) | — |

## 2. Đã đo hoặc đã có kế hoạch — không đề xuất lại

| Ý | Ở đâu | Ghi chú |
|---|---|---|
| Cỡ đoạn / gộp đoạn cùng heading (128–512), small-to-big | G5 §1 hạng 1 (H2, small-to-big **kém hơn**) | NC24 §4 đề xuất — đã đo, giữ |
| Gộp dòng bảng | G5 hạng 7 (H3 không khác) | khác #2 (câu hoá hàng — chưa đo) |
| BM25 cặp âm tiết / pyvi / k1 / b / nguyên cụm mã | G5 dưới top 10 (kém hơn / không khác) | NC24 §3 đề xuất — đã đo, giữ |
| Tiền tố Representation A (bớt) | G5 dưới top 10 (kém hơn) | khác #3 (thêm) |
| HNSW, `dense_bm25_rrf` vs native, pool 30 / RRF k | G5 §2, hạng 6 | giữ; pool rộng là tín hiệu (spec 8.2 E3a) |
| Dọn kho: inventory, code fence, 3 cặp lặp | G5 §2 (S1–S3 không khác) | đợt 3 gói sửa / lần build lại |
| Đoạn vượt token (B-11), C-21, B-12, B-14, B-15 | plan đợt 3 (`sua_dot3_plan.md`) | sửa code, không phải thí nghiệm |
| Index Qwen3-Embedding-8B | C #10 | không lặp |
| Câu không dấu | G5 — User 15:15 25/10 ngoài phạm vi | — |

## 3. Câu hỏi gửi ChatGPT (A gộp với Q1–Q5 của C, viết một prompt deep research đầy đủ theo `Session_Prompt.md` §9)

- **QB1 (#2):** recall truy hồi khi câu hoá hàng bảng vs hàng Markdown, có / không đoạn tổng quan bảng — embedding nhỏ đa ngôn ngữ + BM25; URL + số đo.
- **QB2 (#3):** contextual retrieval với đoạn ngắn đã có tiêu đề / heading — bản lặp lại độc lập, biến thể tất định, phần lợi đến từ đâu.
- **QB3 (#5):** trọng số trường (BM25F) trong kho nhỏ có tiêu đề lặp; cách làm với một vector thưa Qdrant.
- **QB4 (#6):** `bge-m3` vs `Qwen3-Embedding-0.6B` trên CPU (thời gian embed câu / kho cỡ 8.500 đoạn), và `bge-m3` sparse thay BM25 tiếng Việt.
- **QB5 (#1):** nguồn chính thức hiện hành cho các mục mâu thuẫn — **danh sách private**, A gửi riêng (không đưa nội dung kho vào prompt chung nếu không cần).
- Đã có trong NC24 — **không hỏi lại:** điểm VN-MTEB / benchmark cộng đồng của các embedding và reranker; pyvi / underthesea / VnCoreNLP; cỡ chunk (arXiv 2505.21700,
  NVIDIA); table understanding (WSDM 2024); question decomposition (ACL SRW 2025); MMR / cap mỗi tài liệu.

## 4. Gợi ý thứ tự cho A (đề xuất, không kết luận)

1. **#10, #9, #8** (free, không đổi hành vi) — làm cùng các gói sửa / cổng ổn định.
2. **#7** trước mọi lần build lại (để build không ngừng chatbot) — sửa code có plan + review.
3. **Một lần build lại gộp:** #1 (sửa kho, User duyệt) + #4 (bỏ huydang) + dọn kho đợt 3 — một mốc mới, chấm baseline cùng lượt mù.
4. Trên mốc mới: **#2, #5, #3 (tất định)** — mỗi cái một collection thử, tầng tìm free trước, sinh chỉ khi tầng tìm tốt lên (~0,023 USD mỗi lượt sinh).
5. **#6** chỉ khi User mở danh sách model; LLM contextual (#3) chỉ pilot.

Tổng tiền nếu làm #1–#5 kèm sinh dev + test mỗi biến thể có tín hiệu: ≈ 4 × 0,023 ≈ **0,09 USD** (ước, chưa pilot); LLM contextual toàn kho (4,7 USD) **không** đề xuất.

## 5. Giới hạn

- Ước tiền theo log 8.1 (context 5); chưa pilot. Thời gian build CPU cho model mới (#6) chưa đo.
- Bộ thử nhỏ (32 câu dev có đoạn đúng; câu bảng giá ≤ 7) ⇒ nhiều mục có thể ra "chưa rõ" — ghi trước ở từng plan.
- Lợi ích theo loại câu không tính được khi chưa build biến thể; B không đọc câu Golden / câu kín để lập danh sách (chỉ đếm token kho).
- 4 ý trong `STATUS_B.md` nằm ở #4 (huydang), #9 (khởi động), #7 (cutover / B-06), #10 (chỉ số trải nghiệm).
