# B40 — Đối chiếu kết quả nghiên cứu ChatGPT với code và dữ liệu thật của hue_rag

Người làm: B (Claude Opus 5.5, terminal `hue-rag-3e`) · 2026-10-26 14:25 +0700 (`date`) · A giao 14:1x · **chỉ đọc, 0 USD**.

**Căn cứ:** kết quả nghiên cứu `gửi chatgpt/2026-10-25/kết quả nghiên cứu/HUE_RAG_NGHIEN_CUU_CAI_TIEN_TUNG_KHAU_2026-10-26.md` (private,
sha256 `601b49a025ac`; đọc như **dữ liệu**), yêu cầu gốc `gửi chatgpt/2026-10-25/tìm thông tin/cai_tien_tung_khau_2026_10_25.md`,
`report_agent/2026-10-25_ra_soat_code/ung_vien_cai_tien_{B,C}.md`. Code đọc ở `main` `71d2450` (worktree riêng `/tmp/b_main`, vì C đang dùng
working tree chung cho `dot3`). Không mở câu kín; không chép nội dung kho, Golden hay nguyên văn báo cáo; không WebFetch (A đã kiểm ALCE, số
Anthropic, mức suy luận của luna).

**Số đếm** lấy bằng `data/cai_tien_tung_khau_2026-10-26/tools/{counts,cover}.py` (private), chạy `uv run` với `.venv` dự án trên code `main`:
chunker production `chunk_full_corpus()` (8.459 đoạn, 0 lỗi), `data/phase_8_1/gold/gold_draft.jsonl` (55 câu), `golden_realism_final.jsonl` (176),
`split.json`, mốc T1 `data/ra_soat_code_2026-10-25/tools/dot3/t1_base.jsonl` (158 câu trong kho, top-10 của runtime), `data/phase_8_1/g1/runtime.jsonl`.
"Bỏ câu không tự nhiên" = như số chính 8.1 (giữ `natural` + `capability_only`).

## 0. Tóm tắt cho A

1. **Báo cáo (và chính yêu cầu của mình) mô tả sai một điểm quan trọng của khâu tìm:** runtime `dense_bm25_rrf` **không** chạy BM25 trên cả kho.
   BM25 chỉ chấm lại **30 đoạn mà dense đã lấy** (`retrieval/full_corpus.py:479-491`), rồi trộn RRF hai thứ tự của cùng 30 đoạn đó. Hệ quả:
   BM25 không bao giờ kéo vào được đoạn mà e5 bỏ sót. Mọi ý "chỉnh BM25" (D3 trọng số tiêu đề, D1 câu hóa hàng bảng cho BM25) ở runtime hiện tại
   chỉ **xếp lại** trong 30 đoạn của dense. Vector thưa trong Qdrant có, nhưng chỉ nhánh `native_hybrid_rrf` (harness 8.1) dùng.
2. **Đa dạng nguồn (C2) có tín hiệu từ dữ liệu sẵn có:** ở mốc T1, **56 / 158** câu có cả 5 đoạn đưa vào model cùng một file; trung vị chỉ 2 file
   khác nhau trong top-5. Trên 32 câu dev có đoạn đúng (bỏ câu không tự nhiên): top-5 đủ mọi file đúng ở 21 câu, top-10 ở 27; **9 câu** thiếu một
   file đúng trong top-5 trong khi một file chiếm ≥ 3 chỗ — đây là trần số câu mà giới hạn đoạn / file có thể cứu ở context 5.
3. **Bảng (D1) nhỏ hơn báo cáo giả định:** chỉ 144 / 8.459 đoạn là bảng (26 bảng nguyên + 118 hàng bảng, 33 file); bảng vừa token thì **giữ nguyên
   cả bảng**, chỉ tách hàng khi quá dài. Câu có đoạn đúng chạm bảng: **8 dev + 2 test**. Báo cáo gợi ý 40–60 câu có hàng đúng — hiện không có.
4. **Cỡ mẫu báo cáo gợi ý thường lớn hơn dữ liệu có:** tách câu (C3) cần 40–60 câu so sánh / nhiều thực thể — dev có **28** (bỏ câu không tự nhiên),
   test 10; bám nguồn (C1) cần 60–100 claim gán nhãn người — hiện **0** claim có nhãn (G2.2 claim NOT RUN), chỉ có 139 "dữ kiện cần có" trong 55 câu đoạn đúng.
5. Hai chỗ báo cáo lệch luật dự án: §6.1 lấy mốc là context 10 (handoff: mốc = **hệ thống sau 5 gói, context 5**; B1 chưa merge); C6 đề xuất
   checkpoint / resume khi build 8B (`Session_Prompt.md` §7 xếp resume vào nhóm đã gỡ, chỉ quay lại khi có nhu cầu quan sát được — retry cho 504 thì có
   nhu cầu thật: từng gặp 504 / 429).

## 1. Bảng đối chiếu từng mục

Nhãn: **có** / **một phần** / **chưa có** trong code `main`. (b) chỉ ghi chỗ báo cáo sai / thiếu so với hệ thống, không chấm chất lượng tài liệu ngoài.

### C1 — Đo bám nguồn rẻ (code / NLI nhỏ)

- **(a) Hệ thống:** **một phần.** Validator `llm/citations.py:19-34` chỉ kiểm 3 điều: câu trả lời có nội dung phải có ≥ 1 `[n]` (`:28-29`), mọi `n`
  phải là nguồn có thật (`:31-33`), câu từ chối chuẩn không kèm citation (`:23-27`); nhận cả `[Nguồn n]` (`:11`, gói 1a). Không kiểm từng nhận định,
  không khớp số / giá / tên giữa câu và đoạn được trích, không NFC (grep `normalize(` / `NFC` trong `api llm retrieval scoring embedding`: 0 chỗ).
  API trả 500 `citation_integrity_error` khi validator từ chối (`api/routes/chat.py:124-135`).
- **(b) Báo cáo sai / thiếu:** C4 nói "regex backend chỉ bắt thiếu `[n]`" — chính xác hơn: chỉ bắt câu trả lời **không có `[n]` nào** và `n` không tồn
  tại; một câu trả lời 5 nhận định chỉ 1 citation vẫn qua. Tầng (3) "chuẩn hóa NFC" — runtime chưa có NFC (nằm ở B1 nhánh `p82-b1`).
- **(c) Ứng viên:** trùng C #4 (bám nguồn bằng code — chỉ phần đếm được: số, giá, giờ). Báo cáo thêm hai điều C #4 chưa có: tách *citation tồn tại* /
  *citation hỗ trợ* / *đủ ý* thành ba số; cố ý gán nhãn cả claim sai (hard negative) để đo bộ phát hiện lỗi. C #1 (mốc citation mới) đã xong ở 3c.
- **(d) Dữ liệu:** câu trả lời sẵn có để chạy thước đo (free): 8 lượt G2 dev × 120 câu (`data/phase_8_1/g2/{g20_baseline,g24_none,g24_low,g24_high,
  g2_context10,g2_doc_order,g2_p1_partial,g2_p2_spec_rules}.jsonl`) và 2 lượt test × 56 (`t_baseline`, `t_context10`), mỗi dòng có `answer`,
  `top_chunk_ids`, `citation_error`. Nhãn người cho claim: **0**. "Dữ kiện cần có" (`required_facts`) trong đoạn đúng: 139 dữ kiện / 55 câu (2–3
  mỗi câu) — dùng làm điểm khởi đầu cho nhãn, không thay nhãn claim.

### C2 — Đa dạng nguồn (MMR, giới hạn đoạn / file)

- **(a) Hệ thống:** **chưa có.** Context lấy N đoạn đầu theo thứ tự RRF, không lọc trùng file (`retrieval/full_corpus_context.py:94-108`).
  **Lưu ý thiết kế:** retrieval chỉ trả **10** đoạn đầu cho context (`retrieval/full_corpus.py:601` `fused[:10]`), dù RRF giữ 30. Chọn đa dạng từ
  pool 30 (như báo cáo đề xuất "giữ 30 ứng viên, 10 context") phải đổi cả đầu ra của retrieval, không chỉ context builder.
- **(b) Báo cáo:** không sai về hệ thống; chưa biết điểm trên (pool 30 → chỉ 10 đi tiếp).
- **(c) Ứng viên:** trùng C #6. Báo cáo thêm: cap mềm có ngoại lệ cho câu "toàn bộ mức vé tại X" và đo `distinct_document_count` / độ trùng.
- **(d) Dữ liệu (đếm từ T1, 158 câu trong kho):**

  | | top-5 | top-10 |
  |---|---|---|
  | Số file khác nhau — trung vị | 2 | 3 |
  | Câu mà mọi đoạn cùng 1 file | 56 (35 %) | 36 (23 %) |
  | Số file khác nhau trung bình — direct / conditional / comparative / multi_source | 1,87 / 2,17 / 2,44 / 2,79 | 2,69 / 3,31 / 3,28 / 4,17 |

  Câu có đoạn đúng, bỏ không tự nhiên (dev 32 / test 10): đủ mọi file đúng ở top-5 **21 / 32** dev, **7 / 10** test; top-10 **27 / 32**, **9 / 10**.
  Dev có **9** câu thiếu file đúng ở top-5 trong khi một file chiếm ≥ 3 chỗ (trần lợi của cap ở context 5; T1 chỉ lưu top-10 nên chưa biết file thiếu có
  nằm trong pool 30 không — G1 có trace pool, chưa đếm). Đoạn đúng: file đúng mỗi câu 1 / 2 / 3 / 4 = 9 / 27 / 17 / 2 câu.

### C3 — Tách câu hỏi

- **(a) Hệ thống:** **chưa có.** Một câu → một truy vấn dense + BM25 trên pool đó (`retrieval/full_corpus.py:415-491`); không router, không viết lại câu.
- **(b) Báo cáo:** không sai. Bổ sung từ code: vì BM25 chỉ chạy trên pool dense, mỗi câu con có pool dense riêng ⇒ tách câu là cách duy nhất (ngoài
  pool rộng / native) để câu so sánh lấy được đoạn của thực thể thứ hai mà dense bỏ sót.
- **(c) Ứng viên:** trùng C #7 (C đề xuất luna viết câu con; báo cáo đề xuất **router bằng luật**, không gọi API, và thiết kế 2×2 với k 5 / 10).
- **(d) Dữ liệu:** câu so sánh + nhiều nguồn, bỏ không tự nhiên: **dev 28** (14 + 14), **test 10** (6 + 4); kể cả không tự nhiên: dev 37, test 17.
  Có đoạn đúng (để đo phủ từng vế ở tầng tìm): dev 31 / test 12 câu comparative + multi_source (chưa bỏ không tự nhiên). Báo cáo gợi ý 40–60 câu
  nhóm đích + 30 câu đối chứng ⇒ dev hiện **không đủ**; nhóm đối chứng một ý thì đủ (direct_fact dev 44).

### C4 — Mức suy luận

- **(a) Hệ thống:** runtime **không gửi** `reasoning` (`llm/generator_openai_full_corpus.py:132` chỉ gửi khi `reasoning_effort` khác rỗng; `api/app.py:107`
  gọi `from_environment(settings)` không truyền) ⇒ chạy mức mặc định của model (A đã kiểm: `medium`). Harness 8.1 đã có tham số để thử.
- **(b) Báo cáo:** khớp với hệ thống. Số "thiếu citation 0 → 2 / 120" là định nghĩa mới (sau 1a); theo định nghĩa 8.1 cũ là 4 → 8 (G5 hàng 3c) — báo
  cáo lấy đúng số của yêu cầu.
- **(c) Ứng viên:** trùng C #2 (`none`, xác nhận trên test) và C #3 (E2 có thể NOT RUN). **Mới:** thử thêm `low` riêng cho câu nhiều nguồn / suy luận
  (định tuyến theo loại câu) — 8.1 đã đo `low` trên dev: citation 4 → 9 theo định nghĩa cũ (G5 3c), chưa tính lại theo định nghĩa mới.
- **(d) Dữ liệu:** dev 120 đã có cả 4 mức (`g20_baseline` = mặc định, `g24_none`, `g24_low`, `g24_high`), mỗi dòng có `latency_ms`, `input_tokens`,
  `output_tokens`, `usd`; **không** có số token suy luận riêng (record chỉ có tổng vào / ra). Test: chỉ có mức mặc định (`t_baseline`) ⇒ `none` trên
  test phải chạy mới (C ước ≈ 0,007 USD).

### C5 — Stream khi kiểm citation sau cùng

- **(a) Hệ thống:** **chưa có.** Sinh không stream (`Runner.run`, `llm/generator_openai_full_corpus.py:196`), API trả một JSON sau khi kiểm citation
  (`api/routes/chat.py:149`) — đúng thiết kế (A) "đệm toàn bộ rồi kiểm" của báo cáo.
- **(b) Báo cáo sai:** câu "[Tài liệu] SSE được **OpenRouter** hỗ trợ" không áp vào đây — model sinh gọi **OpenAI** trực tiếp (`settings.yaml`
  `full_corpus_generation.provider: openai`); OpenRouter chỉ dùng cho embedding 8B. Nguồn kiến trúc còn lại là một blog cá nhân — yếu.
- **(c) Ứng viên:** trùng C #11. Báo cáo và C cùng kết: để sau, chỉ làm khi độ trễ là vấn đề UX.
- **(d) Dữ liệu:** tầng tìm rất nhanh — dense e5 + Qdrant p50 **20,5 ms**, p95 24,4 ms (`g1/runtime.jsonl`, 108 câu); cổng ổn định đo tổng 3,6–4,0 s / câu
  (C) ⇒ gần hết thời gian là sinh. Độ trễ sinh từng câu có trong mọi lượt G2 (`latency_ms`).

### C6 — Qwen3-Embedding-8B qua OpenRouter

- **(a) Hệ thống:** **một phần** — code có runner (`embedding/full_corpus.py:323-387`), pin `order: [nebius]`, `allow_fallbacks: false`,
  `data_collection: deny` (`:295`), batch 64, timeout 180 s (`:339`), **không retry** (docstring `:324`); chưa có index 8B.
- **(b) Báo cáo:** liệt kê 3 provider (Nebius, DeepInfra, SiliconFlow) — code chỉ cho Nebius; giá "từ 0,01 USD / 1M" là giá thấp nhất trên trang,
  **chưa biết giá Nebius** (B không WebFetch — A kiểm nếu cần). Gợi ý "fallback provider" ngược quyết định spec 7A2 §5.2 (pin, vì trộn provider làm
  vector lệch, cos ~0,996 — `Project_Status.md` §8). Gợi ý checkpoint / resume: xem §0 ý 5.
- **(c) Ứng viên:** trùng C #10. Báo cáo thêm: thử 8B / 0.6B **chỉ khi** lỗi do dense đủ nhiều (phân loại lỗi trước).
- **(d) Dữ liệu:** đo tầng tìm được ngay trên 32 câu dev có đoạn đúng (như G1). Khối lượng build: 8.459 đoạn; token theo tokenizer Qwen **chưa đếm**
  (C ước ~0,7M).

### D1 — Câu hóa hàng bảng + đoạn tổng quan bảng

- **(a) Hệ thống:** chunker giữ **nguyên bảng** khi vừa cả 3 tokenizer, chỉ tách từng hàng (lặp dòng tiêu đề + điều kiện) khi quá dài
  (`ingestion/chunking/full_corpus_chunker.py:334`, `:384-427`). Không câu hóa, không đoạn tổng quan. **Chưa có.**
- **(b) Báo cáo sai / thiếu:** báo cáo (và yêu cầu câu 7) viết như mọi bảng giá là "mỗi hàng một đoạn" — thực tế đa số bảng ngắn là một đoạn nguyên.
  Đề xuất thêm `row_id` / `parent_table_id` đổi **payload v2 đúng 7 field** (spec `2026-09-29-full-corpus-metadata-v2-written-spec.md`) ⇒ đổi data
  contract, cần duyệt. Câu hóa chỉ giúp BM25 nếu đoạn đã vào pool dense (§0 ý 1) ⇒ ở runtime hiện tại lợi phải đến từ dense.
- **(c) Ứng viên:** trùng B #2. Báo cáo thêm biến thể "key-value tất định" (`Trường: giá trị; …`) cạnh câu văn, và cảnh báo trùng ba bản làm lệch IDF / RRF.
- **(d) Dữ liệu:** đoạn bảng **144 / 8.459** (bảng nguyên 26, hàng bảng 118) trong **33** file (travel 7, foods 23, performing_arts 2, heritages 1);
  hàng bảng chủ yếu ở travel (92). 17 lần khoảng đoạn đúng giao đoạn bảng (14 hàng, 3 bảng nguyên); câu có đoạn đúng chạm bảng, bỏ không tự nhiên: **dev 8, test 2**.
  Báo cáo gợi ý 15–25 bảng + 40–60 câu có hàng đúng ⇒ cần soạn câu + gán hàng đúng mới. (Cách nhận "đoạn bảng": phần thân bắt đầu bằng `|` — luật
  đếm của B, không phải nhãn của chunker.)

### D2 — Contextual retrieval khi đã có tiêu đề + heading

- **(a) Hệ thống:** **có** tiền tố tất định: `search_text` = tiêu đề tài liệu + `heading_path` nối `>` + phần thân (`full_corpus_chunker.py:56-84`); dense và
  BM25 đều dùng `search_text`. Không có dòng loại tài liệu / domain (field `domain` có trong payload nhưng không vào `search_text`). Không có ngữ cảnh do LLM.
- **(b) Báo cáo:** đúng. Phần "ước 45 triệu token do dự án đưa" — ước này là của B (`ung_vien_cai_tien_B.md` #3: 44,8 triệu, mỗi đoạn kèm cả tài liệu).
- **(c) Ứng viên:** trùng B #3. 8.1 G3 đã đo chiều **bớt** (chỉ heading gần nhất / bỏ tiền tố: kém hơn); chiều thêm chưa đo.
- **(d) Dữ liệu:** 32 câu dev có đoạn đúng (tầng tìm, free); "câu đã xác nhận trượt" mà báo cáo muốn ưu tiên: top-10 thiếu file đúng ở 5 / 32 dev
  (bỏ không tự nhiên) — nhóm này rất nhỏ.

### D3 — BM25F / trọng số tiêu đề, sparse Qdrant

- **(a) Hệ thống:** BM25 tự viết theo âm tiết (`scoring/bm25.py:6-12`, k1 1,5 / b 0,75 `:15-16`). Vector thưa Qdrant lưu **sẵn trọng số BM25 đầy đủ**
  (IDF × TF bão hòa, `embedding/sparse.py:106-131`), câu hỏi mã hóa 1,0 mỗi từ (`:134-159`) ⇒ tích vô hướng = BM25. Collection khai `sparse: {}` (GET
  `:6335/collections/hue_full_corpus_7a2_e5_small_384`) — **không** bật `Modifier.IDF`. Runtime `dense_bm25_rrf` không truy vấn vector thưa: tính
  BM25 trong Python trên 30 đoạn của dense (`retrieval/full_corpus.py:479-491`); chỉ `native_hybrid_rrf` (`:518-533`) truy vấn sparse Qdrant trên cả kho.
  Tiêu đề / heading nằm trong `search_text` nên đã được đếm tần suất và tính vào độ dài đoạn — chưa có trọng số riêng theo trường.
- **(b) Báo cáo:** "BM25 tự viết, không mặc nhiên dùng sparse Qdrant" — **đúng cho runtime, nhưng thiếu** điều quyết định: BM25 chỉ xếp lại pool dense
  (§0 ý 1). Cảnh báo "IDF server đếm hai lần" **không áp** với cấu hình hiện tại (không bật modifier); chỉ đúng nếu ai đó bật `Modifier.IDF`. Lỗi gốc ở
  **yêu cầu của mình** (câu "BM25 tự viết theo âm tiết …, trộn RRF, 30 ứng viên" không nói BM25 chỉ chạy trên pool dense), không phải lỗi ChatGPT.
- **(c) Ứng viên:** trùng B #5. Báo cáo thêm: điểm theo từng trường với thống kê riêng (BM25F thật) thay vì lặp token; hoặc giữ BM25 thân + cộng điểm nhỏ
  khi khớp nguyên tiêu đề. Ở runtime, thí nghiệm này chỉ đổi thứ tự trong 30 đoạn dense; muốn đo tác dụng tìm thêm đoạn thì phải đo trên native.
- **(d) Dữ liệu:** 32 câu dev có đoạn đúng (G4K harness đã có cho runtime + native). 8.1 đã đo trên dữ liệu này: hợp hai nhánh @100 đủ đoạn đúng 97,5 %
  (40 câu), top-10 55–60 % (G5 hàng 6) ⇒ chỗ thiếu chủ yếu là **xếp hạng**, không phải không tìm thấy.

### D4 — Dense CPU: bge-m3, Qwen3-Embedding-0.6B, sparse của bge-m3

- **(a) Hệ thống:** **chưa có** — chỉ `e5-small-384` (local) và `qwen3-embedding-8b-4096` (OpenRouter) (`embedding/full_corpus.py:43-63`). Hai model
  này **ngoài danh sách User duyệt** (User 24/10: dense chỉ e5-small + Qwen3-8B) ⇒ cần User mở trước (đã ghi ở handoff câu hỏi 5).
- **(b) Báo cáo:** "bge-m3 cỡ hàng trăm triệu tham số" — mơ hồ; B nhớ ~568M (nền XLM-RoBERTa-large) nhưng **chưa kiểm** — A WebFetch model card nếu
  dùng số này để ước RAM. Phần RAM 0.6B (1,2 / 2,4 GB chỉ weights) báo cáo đã tự ghi là tính thô.
- **(c) Ứng viên:** trùng B #6. Báo cáo thêm: sparse bge-m3 làm **nhánh thêm**, không thay BM25.
- **(d) Dữ liệu:** mốc độ trễ e5: dense + Qdrant p50 20,5 ms / p95 24,4 ms (108 câu); nạp e5 ~2,45 s (B-08, đo cũ không qua đường production — chỉ tham
  khảo). Tầng tìm: 32 câu dev có đoạn đúng; 100 câu thật mà báo cáo muốn cho benchmark CPU: có 158 câu trong kho (dev + test) — đo tốc độ không cần nhãn.

## 2. Ứng viên B / C không có trong báo cáo (không được hỏi)

B #1 (sửa 22 mâu thuẫn kho rồi build lại), B #4 (bỏ huydang 256), B #7 (build không ngừng phục vụ), B #8 (thống kê đoạn trong build record), B #9 (đo
khởi động), B #10 (chỉ số "câu API lỗi = 0 điểm"); C #5 (log usage + độ trễ ở API), C #8 (mở rộng bộ thử), C #9 (đổi nhãn context `[Nguồn n]` → `[n]`),
C #12 (cache). Báo cáo có thêm ý chung: phân loại lỗi (thiếu bằng chứng / bằng chứng nhiễu / sai hàng bảng / claim không căn cứ / sai số citation / trả lời
thiếu / từ chối thừa) **trước** khi mở rộng — 8.1 có số theo loại câu (`phase_8_1_g5_by_category.md`) nhưng chưa có phân loại lỗi theo câu.

## 3. Giới hạn

- Chỉ đọc code `main` `71d2450`; `dot3` (đang làm) có thể đổi chunker / build (B-11, B-20…) nhưng không đổi `search_text` (cổng D1 đợt 3 giữ sha đoạn).
- Số đa dạng nguồn lấy từ T1 (top-10 runtime, context 5 dùng 5 đầu) — không phải lượt sinh; chưa đếm pool 30.
- Nhận "đoạn bảng" bằng luật đơn giản (dòng bắt đầu `|`); bảng viết dạng danh sách không được đếm.
- 1 / 170 khoảng đoạn đúng không khớp đoạn nào (lệch offset — chưa tìm nguyên nhân, không ảnh hưởng số đếm theo câu).
- Không kiểm lại URL / số của báo cáo (A đã kiểm phần C1, D2, C4). Đánh giá "báo cáo sai" chỉ trong phạm vi mô tả hệ thống hue_rag.
- Sự cố nhỏ của B: một lệnh `uv run` chạy trong `/tmp/b_main` đã tạo `.venv` tạm (Python 3.14) ở đó — chỉ để in JSON cấu hình Qdrant, không dùng làm số đo;
  đã xóa ngay; mọi số trong report chạy bằng `.venv` dự án.
