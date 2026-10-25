# Phase 8.1 G5 — bản nháp bảng kết luận quyết định (B19)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 13:46 +0700 (`date`) · Việc: B19 (A giao 13:44) ·
Trạng thái: **bảng chính thức của G5** (tên file giữ chữ "draft" để không gãy link); A review 13:5x · cập nhật G3 sau khi C chốt · 0 USD · Spec 8.1 §5 G5, §6 tiêu chí 3 ("mỗi dòng top 10 của C11 có kết
luận hoặc lý do NOT RUN"). Không chép câu Golden, câu kín, corpus.

**Cách đọc:**
- Kết luận theo luật ghi trước của từng gate (skill `run-experiment` §4): **giữ** (đã đo, phương án khác không tốt hơn) ·
  **thay bằng X** (tốt hơn trên dev **và** xác nhận trên test) · **chưa rõ** (có tín hiệu, chưa qua luật) · **NOT RUN** (lý do).
- "Thay bằng X" ở đây là **đề xuất cho 8.2**; chatbot chưa đổi gì ở 8.1, đưa vào runtime cần User duyệt.
- Cột "Bằng chứng" chỉ ghi số đo (quan sát). Dòng "suy ra" ghi riêng, có chữ *suy ra*.
- Số chính = dev bỏ câu `unnatural` (88 câu trong kho; 32 câu có đoạn đúng); nhãn sha `0b65d1c138d2`; Golden md5
  `0f7dbf41b422` (G2 trở đi). Viết tắt report: G0.1-2 = `phase_8_1_g0_1_2_measure_implementation.md`; G1 =
  `phase_8_1_g1_implementation.md`; G2 = `phase_8_1_g2_implementation.md`; G3 = `phase_8_1_g3_implementation.md`; G4 =
  `phase_8_1_g4_implementation.md`; G4K = `phase_8_1_g4_keyword_implementation.md`.
- **G3 đã chốt** (report `abc9cb72d1a0`, B review ready — `phase_8_1_g3_review.md`): không biến thể chia đoạn nào tốt hơn.

## 1. Mười chỗ đáng lo nhất của C11 (§4)

| Hạng | Mục C11 | Kết luận | Bằng chứng (quan sát) | Dẫn |
|---:|---|---|---|---|
| 1 | Cỡ chunk 2.1 (+0.6, 2.3) | **giữ** | H1 (chỉ e5-small) không khác; H2 gộp cùng heading T 128 không khác, T 256 / 384 / 512 **kém hơn** (mất 4 / 6 / 6 câu ở ngân sách 750 token; T 512 tụt có CI sau Holm); small-to-big **kém hơn** (0/24/8); B10 (ngân sách 1.500 token ≈ context 10): H2 384 / 512 vs H1 mất 6 câu ⇒ **kém hơn**. *Suy ra*: đoạn to tìm thấy nhiều hơn (top-10 5/26/1 ở T 512) nhưng chiếm chỗ, ít đoạn lọt context | G3 §3.1, §3.3, §3.4, §3.7 |
| 2a | Context 5 (6.1) | **thay bằng 10 đoạn** | dev: Completeness +0,261 [+0,080; +0,477], 9/77/2, p Holm 0,007; từ chối nhầm 13 → 7; 0 câu out_of_scope bị trả lời; lỗi citation 4 → 4; nhóm đủ đoạn đúng 0/13/0. **test** (41 câu): +0,268 [+0,024; +0,585], 6/34/1; citation 4 → 4. USD/câu ×1,5 (≈ 0,0002) | G2 §4.1, §4.4 |
| 2b | Từ chối tất-cả-hoặc-không (6.4) | **giữ** (P1 kém hơn) — tín hiệu H8 | P1 "trả lời phần có căn cứ": từ chối nhầm 13 → 1, 17 câu trả lời một phần, Completeness +0,114 [−0,023; +0,250] (chưa vượt 0) nhưng **2 câu out_of_scope bị trả lời** (sàn). G1.6: **22/22** câu từ chối nhầm 7B thiếu ≥ 1 đoạn đúng trong 5 đoạn đưa model; 0 câu đủ bằng chứng mà vẫn từ chối | G2 §4.2; G1 §4 G1.6 |
| 3a | Model sinh (6.7) | **NOT RUN** | User 24/10: giữ `gpt-6-luna`, không so model sinh ở Phase 8 (thay amendment 10-01 §5 / 10-23 R6) | `Project_Status.md` §5 |
| 3b | Prompt (6.5) | **giữ** (P2 không khác) | P2 (2 luật spec Phase 6 §10): Completeness +0,000 [−0,068; +0,068]; lỗi citation 4 → 1 (phụ) | G2 §4.2 |
| 3c | Reasoning effort (6.8) | **giữ mặc định (không gửi)** | `none`: Completeness +0,136 [+0,034; +0,261] p Holm 0,031 nhưng lỗi citation 4 → **8** (> +2) ⇒ kém hơn; `low`: citation 4 → 9 ⇒ kém hơn; `high`: không khác, USD ×1,11 | G2 §4.5 |
| 4 | Dense model (3.1, 3.2) | **NOT RUN** ở 8.1 | Spec 8.1 / User 24/10: dense chỉ e5-small + Qwen3-Embedding-8B, index 8B để 8.2 | `Project_Status.md` §5 |
| 5 | Thước đo (7B.5, 7.5, 7B.6, 7.3, 7B.1, 7B.2) | **thay một phần** — xem §2 | so theo cặp + Holm + đối chứng âm/dương (G0.2); chia 120 dev / 56 test (G0.1); đoạn đúng 55 câu (G0.3); chỉ số theo đoạn đúng trong 5 đoạn đưa model (G1–G4K); **chưa**: mốc người (7B.6), bám nguồn bằng code (7B.2) | G0.1-2 §4; G1 |
| 6 | Pool 30 + RRF k 60 (5.2, 5.3) | **giữ** (chưa rõ) — tín hiệu pool rộng | Recall: hợp hai nhánh @100 đủ đoạn đúng 97,5% (40 câu), top-10 55–60%. 10 biến thể trộn (G1.3) không qua Holm; native p100 không rerank vs runtime (dev 30): +0,100 [−0,033; +0,233], 4/25/1 (mất 1); G4K P: k 10 / 30 không khác | G1 §4 G1.1, G1.3; G4 §4.4; G4K §4.4 |
| 7 | Bảng mỗi dòng 1 chunk (2.2) | **giữ** | H3 gộp dòng bảng (so H1): 0/32/0, keyword −0,284 [−0,852; 0] — không khác (trần 7 câu) | G3 §3.2 |
| 8 | Reranker (5.5) | **giữ `none`** — tín hiệu luna | MiniLM vượt 512: 0/158 (G1.5). M1 / M2 × trơn / kèm mục (top-10): **kém hơn** (mất 1–3 câu). G4-B M1 pool 100: kém hơn so runtime (mất 1), không khác so native p100 không rerank. Luna listwise: 3/27/0, MRR@10 +0,172 [+0,092; +0,261], chưa rõ (trần 3 câu); +3,5 s/câu | G1 §4 G1.5; G4 §4.2–4.5 |
| 9 | Ràng buộc tokenizer HuyDang (2.3, 2.4) | **không khác** (bỏ được — đề xuất dọn) | H1 (bỏ e5-base + HuyDang 256): 8.398 đoạn (−61), 0/32/0 ở chỉ số chính; keyword context-B 1 câu tụt / 1 câu tăng (cận dưới −3,41) | G3 §3.1 |
| 10 | Bẫy hạ tầng (X.1, 4.3) | **đã xử lý cho thí nghiệm** (không đổi runtime) | Harness gọi production qua tham số mặc định = hành vi cũ (G0.5, B11, B13; G3 `chunks=None`; G4 `max_length=None`); mỗi biến thể chunker một collection `hue_81_g3_*` + build record + sparse state riêng, kiểm sha danh sách đoạn (G3). Mốc byte runtime `cefb2d1a…` giữ nguyên qua mọi gate. Loader vẫn ép tổ hợp runtime (đúng ý: runtime không đổi) | `phase_8_1_g0_5_params_implementation.md`; G3 §1–2; G4 §2 |

**Ngay dưới top 10:**

| Mục C11 | Kết luận | Bằng chứng | Dẫn |
|---|---|---|---|
| BM25 tách âm tiết (3.7) | **giữ** | cặp âm tiết / pyvi kém hơn (mất 1–4 câu; native còn tụt keyword −2,65 / −2,27 điểm %); nguyên cụm mã không khác (0 câu đổi) | G4K §4.2 |
| BM25 k1 / b (3.8) | **giữ** | b 0,5 / 1,0 trên runtime và native: không tốt hơn; 3/4 lượt mất 1–2 câu hoặc tụt keyword | G4K §4.4 |
| NFC câu hỏi (0.5) | **đề xuất thêm NFC** (chưa xác nhận test) | câu NFD: MRR −0,204 [−0,265; −0,144]; NFD → NFC giống hệt gốc (tất định) | G1 §4 G1.4 |
| Câu không dấu (mới, từ G1.4) | **chưa rõ** — lỗ hổng lớn | runtime: đủ đoạn đúng trong 5 đoạn 13/32 → **1/32**, MRR 0,716 → 0,162. Khử dấu cả kho + câu: kém hơn (mất 2 / 4 câu có dấu); trên câu không dấu ở native: 3/29/0 (chưa vượt 0), sparse@100 0,250 → 0,812, MRR 0,209 → 0,414 | G1 §4 G1.4; G4K §4.3 |
| Validator citation (6.6) | **giữ** | chính sách "một nguồn thì gán" (A chọn): 0 câu đổi trên 7B Run 1/2 + 5 lượt G2 — mọi lỗi là "không có `[n]`" khi context có 5 (10) nguồn | G2 §4.3 |
| Representation A (2.7) | **giữ** | tiền tố chỉ heading gần nhất: 4/21/7; không tiền tố: 3/21/8 ⇒ **kém hơn** (mất 7 / 8 câu); keyword / MRR lệch theo cách đo nên không dùng | G3 §3.5 |

## 2. Các dòng C11 khác có số đo ở 8.1

| Mục | Kết luận | Bằng chứng | Dẫn |
|---|---|---|---|
| 4.2 HNSW mặc định | **giữ** | top-10 và tập dense-30 giống exact 108/108; latency như nhau. Ghi chú G4K: 30 đầu của `limit=100` khác `limit=30` ở 1/108 câu (HNSW phụ thuộc `limit`) | G1 §4 G1.2; G4K §4.0 |
| 5.1 `dense_bm25_rrf` vs native | **giữ** | native p30 / p100 không qua Holm, mất 1–2 câu | G1 §4 G1.3 |
| 6.3 Thứ tự context | **giữ** | xếp 5 đoạn gom theo tài liệu: Completeness −0,023 [−0,068; +0,023]; lỗi citation 4 → 6 (6 mới / 4 hết) | G2 §4.1 |
| 6.2 Ngân sách token | **giữ** (không chạm) | context 10: input TB ≈ 1.660 token/câu, xa 16.384 | G2 §5 |
| 7.4 reference LLM viết | **đã sửa 10 câu** (User 25/10) | C27 review ready; md5 `0f7dbf41b422`; không so điểm 10 câu đó với 7B | `phase_8_1_golden_fix_review.md` |
| 7B.3 Judge Claude không pin | **giữ, có số nhiễu** | mọi gate 8.1 dùng cùng model (Claude Opus 5.5 kế thừa). Nhiễu judge-only (cùng chữ, hai lượt chấm): Completeness đổi 2/88 câu, chênh TB 0,000. Nhiễu cả đường (sinh lại + chấm lại, G2.0 vs 7B Run 1): 10/83 câu | G2 §4 (đối chứng), §4.5 |
| 7B.4 Tổng hợp / đếm | **thay** (đo thêm) | macro theo loại câu, bảng từ chối 2×2 (G0.2); nhãn `answer_type` full / partial / refusal do sub-agent riêng (G2); `is_refusal` chỉ khớp hệt — đã kiểm | G0.1-2 §2; G2 §3–4 |
| 0.2 Inventory performing_arts | **không khác** — an toàn, đề xuất dọn | S1 bỏ 33 đoạn: 0/32/0, keyword 0/88/0 (inventory lọt top-10 ở 2/120 câu dev) | G3 §3.6 |
| 0.7 Code fence bị bỏ | **không khác** — an toàn, đề xuất dọn | S2 thêm 2 đoạn: 0/32/0 | G3 §3.6 |
| 2.6 3 cặp lặp body | **không khác** — an toàn, đề xuất dọn | S3 bỏ 3 đoạn: 0/32/0 | G3 §3.6 |
| Còn lại (0.1, 0.3, 0.4, 2.5, 2.8, 2.9, 3.3–3.6, 4.1, 5.4, 6.9–6.11, 7.1, 7.2, X.2) | **NOT RUN** | C11 xếp tác động thấp / không cần đo, hoặc ngoài phạm vi spec 8.1 (3.3 index 8B, 6.10 Representation B có phí → 8.2) | C11 §3 |

## 3. Đề xuất cho 8.2 (có bằng chứng)

| # | Đề xuất | Lợi đo được | Rủi ro / chưa biết | Chi phí | Cần User duyệt |
|---:|---|---|---|---|---|
| 1 | **Context 10 đoạn** (`max_context_documents` 5 → 10) | Completeness +0,26 dev / +0,27 test; từ chối nhầm −6 câu / 88 dev; 0 câu OOS bị trả lời; G3 B10: đoạn to không thay được 10 đoạn nhỏ | prompt dài ×1,8; chưa có mốc người | +≈ 0,00007 USD/câu (×1,5) | đổi hành vi runtime (settings) |
| 2 | **NFC câu hỏi** ở API / BM25 | phục hồi hoàn toàn câu NFD (MRR −0,204 → 0) | chưa biết tỉ lệ người dùng gửi NFD (C11 §7 câu 4) | ~0 (1 dòng) | đổi code runtime (nhỏ) |
| 3 | **Khử dấu khi câu hỏi không dấu** (chỉ mục BM25 khử dấu, chọn theo câu hỏi) | ở native, câu không dấu: sparse@100 0,25 → 0,81, MRR 0,21 → 0,41 (phụ); *suy ra*: tránh được thiệt cho câu có dấu vì chỉ bật khi không dấu — **chưa đo** | nhánh dense e5 vẫn kém với câu không dấu; câu không dấu là biến đổi máy, chưa phải câu thật | build sparse state + index mới (free) | đổi index + runtime; cần thí nghiệm riêng trước |
| 4 | **Pool rộng (native 100)** | dev 30: +4 / −1 câu đủ đoạn đúng (chưa rõ); G4-B cho thấy phần lợi chủ yếu do pool | mất 1 câu; chưa đo cùng context 10 | latency ~+10 ms | đổi retrieval runtime |
| 5 | **Rerank listwise `gpt-6-luna`** | MRR@10 +0,17 có CI, 0 câu mất, 3/3 câu cứu được | chưa rõ ở chỉ số chính (trần 3 câu); +3,5 s/câu; phụ thuộc API | ≈ 0,0003 USD/câu (~270 token ra do model tự suy luận) | dùng model cho bước mới |
| 6 | **H8 trả lời một phần** (P1, có chặn OOS) | từ chối nhầm 13 → 1 | 2 câu OOS bị trả lời (phạm sàn); đổi hợp đồng spec Phase 6 §10; cần biến thể giữ từ chối OOS | ≈ 0,00015 USD/câu | đổi hành vi + spec |
| 7 | **Giảm lỗi citation ở bước sinh** | P2: 4 → 1 (phụ); `none` cho Completeness +0,14 nhưng citation 4 → 8 | G2.3 cho thấy validator hiện tại không chạm tới lỗi "thiếu `[n]`" ⇒ cần cách khác (ví dụ sinh lại một lần) — chưa đo | thấp | đổi prompt / validator |
| 8 | **Dọn chunker khi build lại index** (H1 bỏ ràng buộc HuyDang; S1 bỏ inventory; S2 giữ fence; S3 bỏ 3 đoạn lặp) | cả bốn không khác ở đoạn đúng (0/32/0) ⇒ *suy ra*: bớt ràng buộc / sửa dữ liệu mà không thiệt | H1: 1 câu tụt keyword; không có bằng chứng chất lượng tăng | build lại index (free) | đổi chunker (rủi ro cao theo WORKFLOW) |
| 9 | **Index Qwen3-Embedding-8B** | chưa đo (spec để 8.2) | 504 / 429; cần cách gọi chịu lỗi (C11 3.6, đề xuất cải tiến mục 10) | có phí (~0,008 USD build, chưa kiểm) | provider đã duyệt; thiết kế cách gọi |
| 10 | **Mốc người** 20 câu (D6) trước khi quyết theo điểm câu trả lời | — | mọi kết luận câu trả lời 8.1 dựa vào judge Claude | 1–2 giờ công User | **User** |

## 4. Khâu còn dính (skill `practical-project-coding` "Ranh giới theo khâu pipeline")

| Khâu | Chỗ dính | Gặp ở | Gợi ý tách (8.2) |
|---|---|---|---|
| Ingestion | `prepare_full_corpus_input` / `build_candidate` tự đọc settings (`_phase4_settings`) và tự tạo Qdrant client; chunker chỉ đổi tokenizer qua settings (gộp đoạn / tiền tố phải làm ngoài) | G3 | nhận settings / client làm tham số; G3 đã thêm `chunks=None` |
| BM25 / sparse | `tokenize` là hằng trong `scoring/bm25.py`, `embedding/sparse.py` import trực tiếp ⇒ không truyền được tách từ khác vào `fit_sparse_state` / encode; G4K phải chép công thức sang harness | G4K | tham số `tokenizer` (mặc định = hiện tại) + ghi tokenizer vào sparse state / build record |
| Retrieval | top-10 `fused[:10]` và nhiều `limit` là hằng; dense `limit` đổi kết quả HNSW (1/108) | G1, G4K | tham số `top_k`; ghi `limit` vào trace |
| Rerank | `CrossEncoderReranker` không lộ tokenizer / độ dài cắt (G4 thêm `max_length`, `loaded_device`; harness vẫn đọc `_model.tokenizer`) | G4 | property `tokenizer_max_length` công khai |
| Context | `PackedSource` không mang `chunk_id`; harness phải dò lại bằng `FullCorpusContextBuilder._source` (`packed_chunk_ids`); không có tham số ngân sách token theo số token (G3 phải tự dựng context-B) | G2, G3, G4, G4K | thêm `chunk_id` vào `PackedSource`; tham số ngân sách |
| Evaluator | `run_retrieval_eval` / `context_keyword_coverage` gọi `load_settings` bên trong; `CONCURRENCY`, giá USD là hằng | G1, G2 | đọc ở rìa, truyền vào |
| Generator | `answer_case` nhận service / builder / generator làm tham số — **đã tách được** (G2 dùng thật); `from_environment` đọc env ở rìa | G2 | — |
| Harness | ghi đè theo `--name` (C21 m3) — đã chặn ở G2 / G3 / G4 / G4K; harness G1 vẫn ghi đè | G1 | sửa G1 nếu còn dùng |

## 5. Giới hạn chung của 8.1 (cho TONG_HOP / báo cáo User)

- Bộ thử nhỏ: 32 câu dev có đoạn đúng, 88 câu dev trong kho; test 41 câu trong kho / 10 câu đoạn đúng số chính. Nhiều kết
  luận "chưa rõ" là do trần số câu có thể đổi (ghi trước ở từng plan).
- Judge là Claude (không có mốc người). 15 câu test có đoạn đúng đã nhìn ở G1.6. Câu kín chưa dùng (G0.4 chờ User khóa).
- Câu không dấu / NFD là biến đổi máy từ câu dev.
- Tiền 8.1 tới bản nháp này (B17 + B18): 0,1653 USD (B) — A cộng phần các session khác.

## 6. Lời thường cho User (nháp)

Sau khi rà lại các quyết định cũ bằng thí nghiệm có luật ghi trước, chỉ **một** thay đổi đủ chắc để đề xuất: đưa cho model
**10 đoạn thay vì 5**, câu trả lời đầy đủ hơn rõ ở cả bộ thử lẫn bộ kiểm, tốn thêm khoảng 50% tiền mỗi câu (vẫn rất rẻ). Các
thử khác — model xếp hạng lại, đổi cách tách từ, chia đoạn to hơn, đổi prompt, mức suy luận — hoặc không khác, hoặc làm rơi
đoạn đúng của vài câu. Phát hiện lớn nhất cần sửa tiếp: người dùng gõ **không dấu** thì tìm kiếm gần như hỏng. Đổi cách
chia đoạn (12 cách) cũng không tốt hơn — đoạn to tìm thấy nhiều hơn nhưng chiếm chỗ nên làm rơi đoạn đúng của câu khác.
