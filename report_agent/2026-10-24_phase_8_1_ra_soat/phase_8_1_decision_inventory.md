# Phase 8.1 — Bảng rà quyết định kỹ thuật Phase 0–7B và bằng chứng đứng sau

Ngày: 24/10/2026 (viết xong 19:26, giờ lấy bằng `date`) · Người làm: C · Loại: rà soát chỉ đọc, miễn
phí · Việc: `session_prompt/CURRENT_HANDOFF.md` "### C11" · Review: A.

Không sửa code, config, corpus, Golden; không ghi Qdrant; không gọi API trả phí. Report không chép
nội dung corpus hay câu Golden; chỉ ghi số tổng hợp và tên file.

## 1. Cách làm và mức tin cậy

- **Nguồn:** code ở commit `c57ec43` (`git show HEAD:<path>`). Working tree đang có việc dọn B9 chưa
  commit, nên số dòng có thể lệch sau B9; với `settings.yaml` có ghi kèm tên key. Ngoài code còn dùng:
  - `Project_Status.md` §5;
  - specs `docs/superpowers/specs/` (đọc theo mục), `PROJECT_HISTORY.md` (grep);
  - report `reports/*` (benchmark Foods 08a/08b/08c, Phase 3–7B), `bao_cao_he_thong/`;
  - nghiên cứu ChatGPT (private, chỉ tóm ý);
  - các giả thuyết H1–H14, O1–O11 ở `reports/phase_8_candidate_hypotheses_2026_10_24.md` (dùng lại,
    không làm lại).
- **Sub-agent:** 3 sub-agent `general-purpose`, mỗi agent gom dữ kiện một vùng (0–2 · 3–5 · 6–7B),
  chỉ đọc, brief chung `/tmp/c11/brief_common.md`. C tự kiểm lại các điểm then chốt (mục 1.1). Mọi
  kết luận và xếp hạng là của C.
- **Probe chỉ đọc** (`uv run`, `HF_HUB_OFFLINE=1`, script ngoài repo ở `/tmp/c11/`):
  - chạy `chunk_full_corpus()` thật trên 205 file: 8.459 chunk, 0 lỗi;
  - kiểm NFC của corpus, Golden và tokenizer;
  - một GET cấu hình collection Qdrant;
  - đếm token/latency từ file kết quả 7B đã lưu (`data/evaluation/phase_7b/`).
- **Thang trạng thái:**
  - `so sánh trên full-corpus`: có ít nhất một phương án khác được đo trên Golden toàn kho;
  - `chỉ đo trên Foods`: chỉ có số trên bộ Foods 45/104 câu, 572 chunk, chunker khác;
  - `chưa so sánh`: có hoặc không có lý do, nhưng không đo phương án khác;
  - `mặc định không lý do`: con số hay lựa chọn không có lý do ghi lại;
  - `bị ép bởi ràng buộc đã hết`: lý do gốc nay không còn.
- **Tác động:** ước theo cơ chế và số đã có. Đây là **giả thuyết**, chưa phải đo.

### 1.1 Điểm C đã tự kiểm lại

| Điểm | Kết quả kiểm |
|---|---|
| Loader chỉ chấp nhận đúng tổ hợp runtime | **Đúng**: `backend/core/settings_loader.py:39-44` raise nếu khác `e5-small-384` / `dense_bm25_rrf` / `none` |
| Kiểm tươi khi khởi động không biết chunker đổi | **Đúng**: `source_state.py:99-130` chỉ so hash file nguồn. Build record có `corpus{chunk_count,file_count,identity,sources}`, `dense`, `qdrant`, `representation: "A"`, `sparse`; **không** có cấu hình chunker/tokenizer |
| Golden gộp **không xáo** | **Đúng**: `golden_full_corpus.py:110-121`; spec 7A `:32` "Concat theo thứ tự partition cố định, không shuffle" |
| Cam kết so Qwen ở Phase 8 | **Đúng**: amendment `2026-10-01-phase-6-openai-baseline-amendment.md:86-101` ("Qwen là benchmark bắt buộc"); amendment `2026-10-23-…-gpt-6-luna…md:109-110` |
| Prompt thiếu luật của spec Phase 6 §10 | **Đúng**: spec `2026-09-14…:239-243` có luật "không dùng title/heading như bằng chứng" và luật đoạn/list. `full_corpus_prompt.py:7-16` không có hai luật này |
| 4 câu lỗi citation vẫn được chấm cao | **Đúng**: `reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md:111` (5,000 / 4,750 / 5,000) |
| File inventory performing_arts vẫn được index | **Đúng**: `settings.yaml` `full_corpus.knowledge_base.exclude_files` (`:44-46`) chỉ có 2 inventory travel |
| Bản chunker đầu tiên có gộp khối (3.318 chunk) | **Đúng**: `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md:115-126` |
| LLM thấy gì trong context | LLM thấy `Tiêu đề / Mục / Bằng chứng` (đoạn trích `evidence_parts`) của 5 nguồn (`full_corpus_context.py:78-86`). Metric truy xuất chấm trên `search_text` top-10 (`retrieval/full_corpus.py:330`). Sub-agent vùng 0–2 ghi nhầm "context là search_text"; đã sửa ở dòng 2.7 |

## 2. Tóm tắt

- Có **56 quyết định** đang hiệu lực, chia vùng như các bảng ở mục 3. Theo trạng thái:
  - **2** `so sánh trên full-corpus`: cách tìm 5.1 (chưa theo cặp) và người chấm 7B.3 (chỉ so hai LLM với
    nhau);
  - **5** `chỉ đo trên Foods`;
  - **29** `chưa so sánh`;
  - **16** `mặc định không lý do`;
  - **4** `bị ép bởi ràng buộc đã hết`.
- **Toàn bộ lựa chọn chia đoạn chưa từng được đo** bằng metric truy xuất hay câu trả lời, kể cả trên
  Foods. Bản đầu có gộp khối (3.318 chunk); reviewer bỏ gộp bằng lập luận, không đo.
- **Bằng chứng Foods khó chuyển sang toàn kho:** benchmark 08a/b/c chạy trên chunker Foods (gộp ~400 ký
  tự): 91 file foods ra 572 chunk. Chunker toàn kho cắt cùng 91 file ra 1.670 chunk, nhỏ hơn ~2,9 lần.
- **Model sinh, prompt, reasoning, context 5 chunk chưa từng được so sánh** trên Golden. Chọn model chỉ
  dựa trên 5 câu live không chấm điểm. Cam kết "so Qwen ở Phase 8" đã rơi khỏi danh sách việc.
- **Thước đo hiện có chưa đủ để kết luận "tốt hơn"** khi đổi một thứ:
  - không kiểm định theo cặp;
  - không có tập giữ kín;
  - không có mốc người;
  - keyword proxy chưa kiểm với nhãn người;
  - metric truy xuất chấm `search_text` top-10, trong khi LLM chỉ thấy bằng chứng của top-5.

  Đây là điều kiện tiên quyết của 8.1 (mục 5, bước 0).
- **Hạ tầng thí nghiệm có hai bẫy:** loader ép cứng tổ hợp runtime, và kiểm tươi không biết khi chunker
  đổi.

## 3. Bảng quyết định theo vùng

Cột: **#** · **Quyết định** · **Giá trị hiện tại** (`file:dòng` ở `c57ec43`) · **Ai/khi nào chốt** ·
**Phương án từng xét** · **Bằng chứng** (đo trên gì, metric, kết quả) · **Trạng thái** · **Tác động** ·
**Thí nghiệm đề xuất** (đổi một thứ, baseline = giá trị hiện tại). Giá ước: sinh 176 câu ~0,024 USD
(context 10 ~0,04); `gpt-6-luna` chấm phụ ~0,03 USD; Claude chấm chính dùng quota Claude Code (0 USD).

### Vùng 0–1 — Dữ liệu curated, data flow

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 0.1 | Phạm vi discovery | 5 domain, 7 glob: `settings.yaml` `full_corpus.knowledge_base.include_globs` `:32-39`; `backend/ingestion/source_state.py:47-84` | Plan `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md` §3.1, User 11/09 | Không ghi (Foods-only là lịch sử) | Không đo (phạm vi sản phẩm). 6 file guide (424 chunk) có mặt trong top-5 tổng 30 lượt trên 158 câu (đếm theo file, một câu có thể tính nhiều lần) | `chưa so sánh` | thấp | Không cần |
| 0.2 | Loại file inventory | `exclude_files` chỉ 2 inventory travel (`:44-46`); `performing_arts/performing-arts-entities-inventory.md` **vẫn được index** (33 chunk) | `Project_Status.md` §5 (2026-09-08) ghi "inventory bị loại"; `PROJECT_HISTORY.md:774` lại tính 13 file performing_arts là "approved scope" | Không ghi | File inventory: top-1 ở 1/158 câu, top-10 ở 3/158 (7B `retrieval_dense_bm25_rrf_1.jsonl`) | `mặc định không lý do` (có thể sót) | thấp | Thêm vào `exclude_files` trong lần build lại của H1/H2; đo 3 metric truy xuất; free |
| 0.3 | Bỏ mục nguồn | Đúng heading `Nguồn dữ liệu`: `markdown_blocks.py:16,163` | Plan §3.1 "exact heading contract" | Decisions `2026-09-09-full-corpus-context-decisions.md:306-317` nêu cần rà nội dung quản lý lẫn trong bài, chưa chốt | Không đo | `chưa so sánh` | thấp | Rà tay, không cần đo |
| 0.4 | Đọc nguồn | UTF-8 strict, CRLF/CR → LF, không chuẩn hóa Unicode: `source_state.py:24-34` | Umbrella `2026-09-11-full-corpus-rag-written-spec.md` §3 | Không ghi | Probe C: 205/205 file đã ở dạng NFC, 0 ký tự dấu tách rời | `chưa so sánh` | thấp | Không cần |
| 0.5 | **Chuẩn hóa câu hỏi** (A thêm) | Không NFC ở API hay BM25: `scoring/bm25.py:12` chỉ `lower()`; `api/routes/chat.py:25,50` chỉ strip. NFC chỉ ở evaluation: `full_corpus_eval.py:83`, `golden_full_corpus.py:33` | Không có quyết định ghi lại | Không | Probe logic: câu NFD "đại nội" bị BM25 tách thành đa/i/no/i; tokenizer e5 cho `input_ids` NFD ≠ NFC. Corpus 0 và Golden 0/176 câu NFD. **Chưa biết** người dùng thật có gửi NFD không | `mặc định không lý do` | thấp–vừa (tùy tỉ lệ NFD thật) | Free: tạo bản NFD của 176 câu, đo truy xuất so với NFC. Cách sửa ứng viên: NFC ở API (không đổi corpus) |
| 0.6 | Quy tắc viết curated | Template `knowledge-base-hue/meta/*-template.md` giả định "mỗi section đủ ngữ cảnh khi thành một chunk" (heritage-template `:115,288`; tourism-template `:21,246`; performing-arts-template `:203`) | User + các đợt biên soạn 8–9/2026 | Không ghi | Không đo. Dữ liệu viết theo mức section, chunker cắt theo mức block (2.1) | `chưa so sánh` | cao (qua 2.1) | Biến thể "1 heading lá = 1 chunk nếu vừa e5 512", nằm trong H2 |
| 0.7 | Parser Markdown | markdown-it-py, bật table (`markdown_blocks.py:118`); bỏ `fence`/`html_block`/`hr`/dòng chỉ có ảnh (`:333`) | Survey parser được User duyệt 09/09 (`reports/full_corpus_parser_locator_codex_review_2026_09_09.md` §9–10) | mistune có trong môi trường, không so ("đã đủ") | Chỉ độ đúng locator 40/40 part. **2 code fence bị bỏ không báo** (`heritages/heritage/Đàn Nam Giao.md`, `Đàn Xã Tắc.md`, ~360 ký tự) | `chưa so sánh` | thấp | Sửa nhỏ (emit fence như paragraph), gộp vào lần build lại chunker |

### Vùng 2 — Chia đoạn

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 2.1 | **Cỡ chunk: 1 block Markdown = 1 chunk, không gộp** | `full_corpus_chunker.py:344-628` (`chunk_document`). Block: list item 75% (6.244/8.311), paragraph 2.010, table 40, blockquote 17; trung vị 85 token e5 (O1) | Bản đầu của Implementer (11/09) gộp cùng `heading_path` theo trần token → 3.318 chunk. Codex review W1-R2 (`reports/full_corpus_rag_wave_1_codex_review_2026_09_12.md:47-70`) bỏ "blind budget-fill grouping" → 8.460. User đóng Phase 2 12/09; User 24/10 "giữ tới baseline 7B" | (a) gộp cùng heading (3.318 chunk, **chưa từng embed/đo**); (b) Foods gộp ~400 ký tự; (c) nhóm P1/P2 trong survey `full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md` §5 (chỉ đếm token 6 mẫu, tự ghi "không phải quality PASS") | **Không phương án nào được đo** truy xuất/câu trả lời, kể cả Foods. Chỉ có baseline 7B trên chunker hiện tại (MRR@10 0,721; comparative 0,53; multi_source 0,54) | `chưa so sánh` | **cao** | H2: gộp block liền nhau cùng `heading_path` tới 256 token e5, và biến thể section-level (0.6); làm sau H1. Build lại e5 local (free). Đo truy xuất + câu trả lời trên 176 câu theo cặp (~0,024 + 0,03 USD). Bẫy: chunk to tự làm Keyword Coverage tăng → kèm gold evidence (7.3) |
| 2.2 | **Bảng quá dài → mỗi dòng 1 chunk + header** | `full_corpus_chunker.py:385-447` (tách dòng `:415-445`); 40 bảng, 14 bị tách thành 118 chunk | Implementer chọn 1 dòng; spec umbrella §4 `:90` chỉ đòi giữ header/đơn vị/điều kiện | Decisions `:438-440` "nhóm hàng có nghĩa, **không đặt một hàng làm mặc định**"; survey P3b nhóm hàng (chỉ đếm token) | Probe O4: chunk dòng giá của câu F2 hạng dense 41/99/191. 6 bảng tách chỉ vì HuyDang, 8 bảng vượt cả e5 512 | `chưa so sánh` | **cao** (câu giá/vé) | H3: nhóm 3–8 dòng, lặp header; đo hạng chunk F2 + nhóm `conditional`. Free |
| 2.3 | **Ràng buộc 3 tokenizer** | `settings.yaml` `full_corpus.embedding_models` `:48-60` (e5-small 512, e5-base 512, HuyDang 256 + pyvi); `full_corpus_chunker.py:302-341`; `ingestion/preview.py:95-118` | Decisions `:481`, umbrella §5 `:142-145` (User 11/09) vì "ba dense candidates". 7A2 bỏ e5-base/HuyDang khỏi candidate nhưng giữ chunker (spec 7A2 `:30,107`) | Không ghi | Max quan sát 366/512, 366/512, 255/256. **23 block → 90 chunk chỉ vì HuyDang** (6 bảng, 17 list item). e5-base cùng tokenizer với e5-small, kiểm hai lần là thừa | `bị ép bởi ràng buộc đã hết` | vừa (điều kiện cần cho 2.1) | H1: chỉ giữ e5-small 512; build lại (free); so riêng câu có đáp án trong 23 block đó |
| 2.4 | List dài: tách theo mục con kèm nhãn cha, hoặc tách câu | `full_corpus_chunker.py:450-514` (nhãn cha `:481-489`), `:549-626` | Spec §4 `:89`; Codex W1-R1 Option A (lỗi HuyDang 280>256 trong khi e5 vẫn vừa) | Không ghi | Không đo. 17 list item bị tách chỉ vì HuyDang | `bị ép bởi ràng buộc đã hết` | vừa | Tự hết khi làm H1, không cần riêng |
| 2.5 | Paragraph dài: tách câu | Regex `full_corpus_chunker.py:50`; gộp câu `:583-626` | Spec §4 `:88` | Không ghi | Corpus hiện tại: 0 paragraph bị tách | `chưa so sánh` | thấp | Không |
| 2.6 | Không overlap | Không có trong code; 3 cặp chunk lặp body (blockquote trong list item, `markdown_blocks.py:233-251`) | Spec §4 `:92`; decisions `:283` | rag_old_0 overlap 200 ký tự (loại bằng lập luận) | Không đo | `chưa so sánh` | thấp | Sửa 3 cặp lặp khi làm H2 |
| 2.7 | `search_text` = Representation A (tiêu đề + heading_path + các part) | `full_corpus_chunker.py:71-99`. Dense nhúng với `passage: ` (`embedding/full_corpus.py:82`); BM25 chạy trên cùng text (`embedding/sparse.py:72`). LLM **không** đọc `search_text`, chỉ đọc tiêu đề/mục/đoạn trích (`full_corpus_context.py:78-86`) | Decisions `:469-480`, umbrella §5 `:138-140` (User 11/09) | Foods dùng nhãn khác; Representation B (H10) chưa build | **Chưa ablation ở đâu cả.** Chunk vụn (thân trung vị 193 ký tự) khiến nhãn chiếm phần lớn token; từ trong tiêu đề lặp ở mọi chunk cùng file trong BM25 | `chưa so sánh` | vừa | Biến thể A′ (bỏ tiêu đề, hoặc chỉ giữ heading cuối); build lại e5 (free); đo **sau** H2 vì tỉ lệ nhãn/thân phụ thuộc cỡ chunk |
| 2.8 | Gắn điều kiện bằng luật tay | 3 luật trong `backend/config/full_corpus_conditions.json`; `full_corpus_chunker.py:132-296`; 9 chunk có condition | Umbrella §4 `:95-103`; decisions `:467` tự ghi "không hứa bao phủ toàn corpus" | P3a (lặp đủ "Bao gồm"/"Không bao gồm") bị loại vì vượt token | Chưa rà toàn corpus; bảng giá của câu F2 không có luật. 7B `conditional`: MRR 0,816, Completeness 4,41 | `chưa so sánh` | vừa | Rà tay các câu `conditional`/từ chối nhầm xem có thiếu điều kiện không; free; đi cùng H3 |
| 2.9 | Locator, `chunk_id = source#ordinal`, tất định | `markdown_blocks.py:335-353`; `core/schema.py:46-51,88-95` | Umbrella §4, Decision #3 | Decisions `:370` (JSON compact, không theo) | 100% part khớp; đây là hợp đồng toàn vẹn, không phải đánh đổi chất lượng | `chưa so sánh` | thấp | Không |

### Vùng 3 — Embedding và BM25

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 3.1 | **Dense runtime e5-small-384** | `embedding/full_corpus.py:42-53`; `settings.yaml` `full_corpus_runtime.candidate_id` `:111`; ép ở `settings_loader.py:39-40` | Phase 6: "smoke configuration, không phải winner" (spec `2026-09-14…:48,182`). User 7A2 §2 (23/10) chọn làm mặc định; cutover 8B chờ bằng chứng | e5-base, HuyDang, Qwen3-0.6B, MiniLM-L12 (Foods 08a); Qwen3-8B (7A2) | **Foods 45** (08a, `reports/phase_8_08a_embedding_benchmark_implementation_report.md:89-100`): MRR@5 e5-small 0,775 / e5-base 0,699 / HuyDang 0,721; nDCG@5 0,743 / 0,706 / 0,716. CI của chênh nDCG cắt 0. Đo trên chunk Foods. Toàn kho: chỉ có baseline e5 | `chỉ đo trên Foods` | **cao** (đặt pool 30 cho mọi bước sau) | H9: e5-base hoặc Qwen3-Embedding-0.6B local (free; 0.6B cần User duyệt) trên chunker đã chốt; 8B có phí sau đó |
| 3.2 | Bỏ e5-base, HuyDang, Qwen3-0.6B khỏi toàn kho | `embedding/full_corpus.py:41-66` còn 2 spec | User 7A2 §2 `:30` (23/10), **không ghi lý do** | Không ghi | 4 index toàn kho (từ 13/09) bị xóa ở 7A2 Gate 3 **chưa từng chấm Golden**. Qwen3-0.6B chỉ đo trên Foods ở 384 chiều cắt ngắn | `chỉ đo trên Foods` | vừa | Gộp vào 3.1 |
| 3.3 | Ứng viên thứ hai Qwen3-Embedding-8B (4096, OpenRouter), chưa có index | `embedding/full_corpus.py:54-65` (batch 64) | User 7A2 §2, §5; survey `reports/phase_7a2_openrouter_embedding_survey_2026_10_23.md` | MRL 1024 chiều: thăm dò 1 lần, không chọn | Smoke 10 trên index trộn 3 provider: 17/19 vs e5 18/19 keyword (index đã xóa). Query 1,1–1,5 s | `chưa so sánh` | cao (chưa biết) | H9 sau khi chốt chunker; có phí (build ước ~0,008 USD theo survey, chưa kiểm) + cần cách gọi chịu 504/429 |
| 3.4 | Tiền tố e5 `query:`/`passage:`; instruction tiếng Anh cho Qwen | `embedding/full_corpus.py:69-73,81-85,95-98` | Phase 3 spec `2026-09-12…` §5 | Không ghi | Theo model card; không ablation | `chưa so sánh` | thấp | Không cho e5. Instruction Qwen: đo khi có index 8B |
| 3.5 | Chuẩn hóa L2 + Cosine; e5 CPU FP32 batch 8; pin revision | `embedding/full_corpus.py:45-51,257,279`; `vectorstore/qdrant.py:10,83` | Phase 3 §5, Phase 4 §5 | Dot (tương đương với vector đơn vị) | Không cần đo (tương đương toán học; batch không đổi chất lượng) | `chưa so sánh` | thấp | Không |
| 3.6 | OpenRouter: pin Nebius, không fallback, `data_collection: deny`, không retry, timeout 180 s | `embedding/full_corpus.py:295-356` | User 24/10 (spec 7A2 §5.2) | Không pin → bị loại vì cos 0,995 (trộn provider) | Nebius lặp lại cos 1,0; build bị 504; DeepInfra từng trả 429 | `chưa so sánh` (ràng buộc tái lập) | thấp với chất lượng; **chặn 3.3** | Thiết kế cách gọi (batch nhỏ, thử lại) ở 8.1/8.2 |
| 3.7 | **BM25 tách âm tiết** `\w+` lowercase | `scoring/bm25.py:6-12`; `embedding/sparse.py:24` | Phase 3 spec §8 `:188-189` "không tạo tokenizer thứ hai"; Foods 08b chọn vì đơn giản | underthesea (Foods 08b); bigram chưa thử | **Foods 45**, BM25 riêng: unicode_word R@30 0,952 / nDCG@5 0,648 vs underthesea 0,956 / 0,642 | `chỉ đo trên Foods` | vừa (tên ghép "Đại Nội", tên món) | H7: bigram âm tiết (free) hoặc pyvi (dependency mới); sparse state + index mới |
| 3.8 | BM25 k1=1,5, b=0,75; query weight 1; IDF tính ở client, Qdrant modifier none; sparse state ghi một lần | `scoring/bm25.py:15-16`; `embedding/sparse.py:64-163`; `vectorstore/qdrant.py:84` (GET: `sparse: {}`) | Phase 3 §8, Phase 4 §5 `:101-107` (bật `Modifier.IDF` thì sparse dot ≠ BM25) | k1 1,2/1,8; b 0,5/1,0 (Foods) | **Foods 45**: baseline thắng nhẹ nDCG@5 0,648 vs 0,644 (b cao); b thấp không đạt guardrail. avgdl toàn kho khác hẳn | `chỉ đo trên Foods` | thấp | Free, làm sau H7: b ∈ {0,5; 1,0} |

### Vùng 4 — Qdrant

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 4.1 | 1 collection/candidate, dense + sparse cùng point; payload đúng 7 field, không index/filter; point id UUID5 | `vectorstore/qdrant.py:77-85`; `vectorstore/points.py:145-149`; `core/schema.py:46-51`; GET: `payload_schema: {}` | Decision #1/#2 (decisions `:1144-1155`), metadata v2 `2026-09-29…` §4 | Subdomain/tags/filter bị loại vì chưa có ai dùng | Không áp dụng | `chưa so sánh` (kiến trúc) | thấp | Không (H14 không đề xuất) |
| 4.2 | HNSW mặc định, không `exact`/`hnsw_ef`, không quantization | `retrieval/full_corpus.py:461-476`; cấm tùy biến ở `vectorstore/qdrant.py:103-106`; GET: m 16, ef_construct 100, full_scan_threshold 10000, 6 segment | Phase 4 spec §5 `:109-111` ("mở lại khi có nhu cầu") | Không ghi | **Chưa từng so HNSW với exact** | `mặc định không lý do` | thấp (8.459 point, có thể đã gần exact; chưa kiểm) | Free: so top-30 exact vs HNSW trên 158 câu bằng script đọc |
| 4.3 | Kiểm tươi bằng build record v3 | `ingestion/source_state.py:99-130,133`; `retrieval/full_corpus.py:353-417` | Spec 7A2 §5.3 | Không ghi | Chỉ so hash file nguồn; record không ghi cấu hình chunker/tokenizer | `mặc định không lý do` | vừa (**rủi ro thí nghiệm**: đổi chunker mà dùng nhầm collection cũ thì runtime không báo) | Không phải thí nghiệm. Spec 8.1 nên quy định mỗi biến thể chunker một collection + record riêng |

### Vùng 5 — Tìm kiếm

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 5.1 | Cách tìm `dense_bm25_rrf` (BM25 chỉ chấm lại 30 ứng viên dense) | `settings.yaml` `full_corpus_runtime.retrieval_treatment` `:112`; ép `settings_loader.py:41-42`; `retrieval/full_corpus.py:506-602` | Decision #1 (11/09) coi đây là đối chứng; Phase 6 "smoke configuration"; giữ sau 7B vì chênh nhỏ | `native_hybrid_rrf`; Foods: weighted fusion | **Golden 158 (7B)**: 0,721 / 0,755 / 92,35 vs native 0,726 / 0,761 / 93,41 — chưa kiểm theo cặp. **Foods 08b:** "rescore" là **weighted min-max 0,6/0,4**, không phải RRF → tổ hợp runtime chưa từng chạy trên Foods | `so sánh trên full-corpus` (chỉ e5, keyword proxy, không theo cặp) | vừa (về cấu trúc không cứu được chunk dense bỏ sót, O5) | Free: paired bootstrap trên 2 file `data/evaluation/phase_7b/retrieval_*.jsonl` sẵn có |
| 5.2 | **Pool 30 ứng viên** | Hằng `limit=30` ở `retrieval/full_corpus.py:465,561,608` | Phase 5 spec §5 `:121,144,148`; tuning ngoài phạm vi (`:80`) | Không ghi (Foods 08b cũng chỉ K=30) | **Chưa đo candidate recall.** Chunk F2 ở hạng dense 41/99/191 | `mặc định không lý do` | vừa–cao (là trần của mọi bước sau, kể cả reranker) | H11 / §8.4 bước 0: candidate recall @30/100/200 cho dense và BM25 trên 158 câu; free |
| 5.3 | RRF k=60, không trọng số, tie theo id | `retrieval/full_corpus.py:146-176,608` | Phase 5 spec §7 `:166-181` (cấm weighted/min-max) | Weighted 0,6/0,4 (Foods) | Foods 45 lẫn lộn (H11). **k chưa từng đổi**; với hạng ≤30, đóng góp mỗi nhánh chỉ trong 1/61–1/90 → BM25 xếp lại yếu | `mặc định không lý do` | thấp–vừa | Free: k ∈ {10, 30, 60} trên 158 câu (cần tham số trong code/script) |
| 5.4 | Trả top-10, không ngưỡng điểm | `retrieval/full_corpus.py:627,644,669` | Phase 5 spec §3 `:86` | Không ghi | 7B: từ chối đúng 18/18 (do LLM, không cần ngưỡng) | `mặc định không lý do` | thấp | Không (context: 6.1) |
| 5.5 | **Reranker `none`; chỉ có MiniLM tiếng Anh; một cặp vượt 512 thì bỏ rerank cả request** | `settings.yaml` `full_corpus_runtime.reranker` `:113`; ép `settings_loader.py:43-44`; `reranking/cross_encoder.py:13,22-27`; `retrieval/full_corpus.py:632-645` | Phase 6 smoke cell; User "chọn A" (decisions `:190-210`); reranker Qwen hoãn (`:215-223`) | MiniLM; cắt bớt / rerank một phần bị loại | **Foods 45** (08c): MiniLM trên e5 ΔnDCG@5 −0,070 [CI −0,135; −0,008]. Toàn kho **chỉ đo latency** (p95 1,0–1,3 s). Tỉ lệ bỏ rerank chưa từng đo, dù decisions `:201-203` hứa ghi log | `chỉ đo trên Foods` | cao nếu có reranker đa ngôn ngữ; thấp với MiniLM | Trước tiên đếm tỉ lệ cặp vượt 512 trên 158×30 cặp (free). Sau đó H5 bge-reranker-v2-m3 (model mới, cần duyệt; free) |

### Vùng 6 — Context, prompt, citation, model sinh, API/UI

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 6.1 | **Context tối đa 5 chunk** | `settings.yaml` `full_corpus_generation.max_context_documents` `:126`; `settings_loader.py:84`; `retrieval/full_corpus_context.py:32,95` | User 09/09 Decision #6b (decisions `:54,110`); lo "thêm nguồn làm mơ hồ, **đặc biệt với Qwen3.5 9B**" (`:243-245`), model này đã bỏ | "Lấy thêm điều kiện gốc sau top-5": hoãn | Thăm dò B5 (`reports/phase_8_probe_context_top10_2026_10_24.md`): case đủ keyword trong context 0,785 → 0,873 (comparative 0,44 → 0,72), token prompt ×1,77. Sinh lại 22 case lỗi: 10/22 hết từ chối, chưa chấm. B4: 12/22 có bằng chứng ở hạng 6–10 | `bị ép bởi ràng buộc đã hết` | **cao** (22/158 từ chối nhầm là nguồn mất điểm lớn nhất) | H4: 10 chunk trên 176 câu, so theo cặp Completeness + từ chối nhầm theo nhóm; ~0,04 + 0,03 USD |
| 6.2 | Ngân sách token 16.384 / 2.048 / 512 | `settings.yaml` `:123-125`; `full_corpus_context.py:102` | Decision #6d (profile Qwen); amendment 10-01 §2 biện minh lại | Không ghi | Chưa từng chạm trần: input lớn nhất 1.734 token, trung bình 947 | `bị ép bởi ràng buộc đã hết` | thấp lúc này | Không riêng; ghi khi chạy H4/H2 |
| 6.3 | Thứ tự và định dạng context | Giữ thứ tự RRF, nhãn `[Nguồn n]` / `Tiêu đề` / `Mục` / `Bằng chứng`; chunk không vừa ngân sách thì dừng (`full_corpus_context.py:78-109`) | Phase 6 spec §9 | Không ghi | Không đo | `mặc định không lý do` | thấp–vừa (context < 2k token) | Ưu tiên thấp: gom chunk cùng tài liệu đứng cạnh nhau; ~0,024 USD + chấm |
| 6.4 | **Từ chối tất-cả-hoặc-không** (so chuỗi chính xác) | `llm/full_corpus_prompt.py:3-5,14-15` | Phase 6 spec §10 (14/09); **lệch** umbrella Decision #6a (decisions `:57,100-102`: "trả phần có căn cứ") | #6a không vào spec Phase 6 | 22/158 từ chối nhầm, cùng 22 case ở cả hai run. B4: 10/22 có một phần bằng chứng, 4/22 đủ keyword vẫn từ chối. B5: 3/4 vẫn từ chối ở context 10 | `chưa so sánh` | **cao** | H8 (User quyết; đổi contract validator): prompt "trả phần có căn cứ, nói rõ phần thiếu"; đo Completeness, từ chối nhầm, giữ 18/18 từ chối đúng, đếm claim không nguồn; ~0,024 + chấm |
| 6.5 | Nội dung prompt | `llm/full_corpus_prompt.py:7-16`, viết cho Qwen, một commit `151bc53` (01/10) | Phase 6 spec §10; amendment 10-23 §4 "không sửa prompt" khi đổi sang luna | Không ghi | Chưa từng A/B. Lỗi "không có citation" 4/176 (Run 1) và 6/176 (Run 2). **Thiếu 2 luật spec §10** (mục 1.1) | `chưa so sánh` | vừa | Biến thể nhấn "mỗi câu có [n]" + bổ sung 2 luật thiếu; đo lỗi citation + điểm; ~0,024 + chấm |
| 6.6 | Validator citation: lỗi → 500, không sửa, không thử lại | `llm/citations.py:9-27`; `api/routes/chat.py:134-144` | Decision #6a; Phase 6 spec §11–12 | Không ghi | Người dùng thấy 500 ở 2,3–3,4% câu. **4 câu lỗi citation (Run 1) được chấm 5 / 4,75 / 5** → validator đang bỏ câu trả lời tốt | `chưa so sánh` | vừa (trải nghiệm) | Free: áp chính sách khác (ví dụ trả câu kèm cảnh báo, `sources=[]`) lên câu trả lời đã lưu của Run 1/2 rồi đếm |
| 6.7 | **Model sinh `gpt-6-luna`** (alias, không pin snapshot) | `settings.yaml` `full_corpus_generation.model` `:117`; `settings_loader.py:66` | User 23/10 ("rẻ hơn, mạnh hơn"). Qwen 3.5-9B (09/09) bị thay trước khi chạy; `gpt-5.4-nano` (01/10) | **Amendment 10-01 §5: Qwen là benchmark bắt buộc ở Phase 8**; amendment 10-23 R6 nhắc lại | nano 5 câu live 3 đạt/2 không (1 lỗi 502); luna 5 câu 4/5; khác thời điểm, **không chấm điểm** | `chưa so sánh` | **cao** | So `gpt-6-luna` với Qwen 3.5-9B (đúng cam kết) và/hoặc nano trên 176 câu, cùng prompt/context. Cần provider OpenRouter + data egress (User duyệt); giá chưa kiểm |
| 6.8 | Không cấu hình reasoning effort (khóa cấm) | `settings_loader.py:50-62` (`reasoning_effort` `:53`) | Amendment 10-01 §2 ("dùng mặc định") | Không ghi | Mặc định của luna chưa rõ; usage không cho thấy reasoning token | `mặc định không lý do` | vừa (có thể đổi quyết định trả lời/từ chối) | low vs medium/high trên 176 câu; ≤0,1 USD ước; phải bỏ khóa cấm (đổi contract) |
| 6.9 | Tham số sinh khác | Không truyền temperature (luna trả 400); max output 2.048 (quan sát max 369, trung bình ~83); timeout 45 s; không retry; structured output 1 field; đếm token `o200k_base` (chưa kiểm cho luna, `tiktoken` KeyError) | Amendment 10-01 §2–3; 10-23 | Bản Qwen: timeout 90 s | p50 ~1,6 s, max ~5,0 s; 0 lỗi kỹ thuật trên 374 call. Ảnh hưởng của structured output chưa đo | `mặc định không lý do` | thấp | Không ưu tiên |
| 6.10 | Representation B có code, chưa có index | `llm/representation_b.py`; `full_corpus_prompt.py:18-21,37-41`; `settings.yaml` `:121` | Decision #5/#6c; Phase 6 spec §7 | Representation A (đang chạy) | Generator B gọi live **1 lần** ở Phase 6 (đạt); chưa build index, chưa đo truy xuất | `chưa so sánh` | vừa (theo nguồn ngoài [R1]) | H10 (có phí, ~8.459 call); thử 20–30 tài liệu lỗi trước |
| 6.11 | API/UI | `query` 1–500 ký tự, có strip, cấm field thừa (`routes/chat.py:24-26`); mã lỗi 422/409/503/502/500; không có nguồn đóng gói được thì từ chối mà không gọi model (`:105-108`); `/health` dùng trạng thái cache (`api/health.py:7-24`); UI tĩnh | Decision #6a; Phase 6 spec §8, §12 | Không ghi | Câu Golden dài nhất 129 ký tự; nhánh từ chối không gọi model xảy ra 0/352 | `mặc định không lý do` (con số 500) | thấp | Không |

### Vùng 7/7A — Golden

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 7.1 | Cách soạn: LLM viết (pilot + 6 sub-agent), người đọc toàn bộ, User đọc mẫu 55; 180 → 176; gộp theo partition, **không xáo** | `evaluation/golden_full_corpus.py:110-121`; smoke 10 chọn tay | Spec 7A §2, §7 (User 23/10) | Chép Foods V3; 7 nhãn rag_old_0; viết tuần tự từng partition — bị bác | `check` đạt. **Không đo** mức đại diện cho câu người dùng thật | `chưa so sánh` | vừa | Ghi giới hạn; bổ sung câu thật khi có log người dùng |
| 7.2 | 5 loại câu và số lượng | `golden_full_corpus.py:13`; 75 / 29 / 29 / 25 / 18 (mục tiêu ~70/35/30/25/15, lệch ±20%) | Spec 7A §4–5 (User 23/10) | Không ghi | `out_of_scope` chỉ 18 câu → khoảng tin cậy rộng. Điểm tổng bị `direct_fact` (43%) chi phối; 121/176 câu đạt 5/5/5 | `mặc định không lý do` (tỉ lệ) | vừa | Free: báo thêm trung bình macro theo nhóm |
| 7.3 | **Keyword nguyên văn từ corpus làm nhãn truy xuất** | `golden_full_corpus.py:67-88` (≥1 keyword mang đáp án, không có trong câu hỏi) | Spec 7A §3; guide `full_corpus_rag.md:236-247` | Không ghi | **Keyword proxy chưa từng kiểm với nhãn người**; nghiên cứu cảnh báo rò nhãn và false negative | `chưa so sánh` | vừa–cao (mọi metric truy xuất và chẩn đoán từ chối dựa vào nó) | §8.4 bước 0: gắn gold evidence (tài liệu/dòng) cho 30–40 câu khó, so keyword-hit với nhãn người; công người, User duyệt mẫu |
| 7.4 | `reference_answer` do LLM viết | Câu ngắn, chỉ dữ kiện corpus; judge chỉ so với nó | Spec 7A §3 | Không ghi | Chỉ có người duyệt (một phần đọc mẫu); độ đầy đủ chưa đo | `chưa so sánh` | vừa (reference thiếu ý thì Completeness sai) | Kiểm trong lượt audit người (7B.6) |
| 7.5 | Không tách tập phát triển / giữ kín | Spec 7A §2, §8 ("Phase 8 không tune theo từng case") | User 23/10 | Nghiên cứu (private) khuyên tách, hoặc ghi rõ *exploratory* | B5 chọn case theo lỗi (report có ghi exploratory) | `mặc định không lý do` | vừa (độ tin kết luận 8.1) | Free: chia phân tầng theo nhóm (ví dụ 120/56), khóa phần giữ kín. **User quyết** |

### Vùng 7B — Bộ chấm

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| 7B.1 | Metric truy xuất keyword @10, chấm trên `search_text` top-10 (LLM chỉ thấy bằng chứng của top-5); nDCG lý tưởng tính trong chính danh sách đã lấy | `evaluation/full_corpus_eval.py:51,86-115` | Thừa kế Foods Phase 7 (spec `2026-08-23…:94-99`); 7A §8; 7B §4.2 | Không ghi | Chạy lại giống từng byte | `chưa so sánh` | vừa (chunk to → Coverage tăng "miễn phí") | Free: dùng lệnh `context-coverage` có sẵn để thêm metric bằng chứng @5 + gold evidence (7.3) |
| 7B.2 | Metric câu trả lời Đúng/Đủ/Trúng ý 1–5, so với reference, bỏ qua `[n]`, không chấm bám nguồn | `evaluation/full_corpus_judge_prompt.md:16-31` | rag_old_0 → Foods Phase 7 → 7B §4.2–4.3 | Groundedness bị loại ở Foods vì đơn giản (spec 2026-08-23 §5) | Có trần: khi bot đã trả lời thì ~4,9. Không bắt được bịa trong câu có citation hợp lệ | `chưa so sánh` | vừa–cao | Free: thêm `required_fact_recall` / `unsupported_claim_rate` trên 20–40 câu (Claude chấm) |
| 7B.3 | Judge: Claude chính (theo model của session, **không pin**), `gpt-6-luna` phụ | Gate 3 report; `full_corpus_eval.py:372-395` | User D3 (7B, tiết kiệm, khác họ với model sinh) | Judge luna (10-23) | Claude chấm lại 30 câu: lệch ≤1 ở 100%. Claude vs luna 176 câu trùng 89–96%, lệch ≥2 ở 0,6% | `so sánh trên full-corpus` (ổn định + khớp hai LLM; chưa so người) | vừa | Pin model judge cho cả 8.1; đổi judge thì chấm lại baseline |
| 7B.4 | Tổng hợp và đếm | Trung bình theo case (spec ghi "macro"; `full_corpus_eval.py:127-138`); từ chối = so chuỗi chính xác (`:118-120`); lỗi citation không trừ điểm (`:292-296`) | 7A §8 / 7B §4.2 (A chốt phần citation) | Không ghi | 0/352 câu trả lời chứa một phần câu từ chối | `mặc định không lý do` | thấp–vừa | Free: thêm macro theo nhóm + ma trận từ chối 2×2 (tử số/mẫu số) |
| 7B.5 | So sánh hai cấu hình | `compare_scores` (`:482-505`) chỉ đo **độ khớp** hai file điểm; không bootstrap/permutation/CI; không ngưỡng | 7B §3, §4.4 | Nghiên cứu khuyên paired bootstrap 10k + permutation, cân nhắc cluster theo file | Nhiễu một cặp run ≤0,011 | `chưa so sánh` | vừa (độ tin **mọi** quyết định 8.1) | Free: thêm paired bootstrap/permutation; tự kiểm bằng Run 1 vs Run 2 ("không đổi gì" phải ra không khác) |
| 7B.6 | Không có mốc người | User bỏ chấm tay 24/10; `user_scoring.md` (20 câu) và `parse-user-scores` (`:508-533`) đã sẵn | User 24/10 | Nghiên cứu: audit 30–40 câu phân tầng, weighted kappa, MAE | Chưa có | `chưa so sánh` | vừa–cao (mọi kết luận 8.1 dựa trên judge LLM) | Free: User chấm 20 câu sẵn (~1–2 giờ). **User quyết** |

### Vùng thêm — Hạ tầng thí nghiệm

| # | Quyết định | Giá trị hiện tại | Ai/khi nào | Phương án từng xét | Bằng chứng | Trạng thái | Tác động | Thí nghiệm đề xuất |
|---|---|---|---|---|---|---|---|---|
| X.1 | Loader ép cứng tổ hợp runtime | `settings_loader.py:39-44` | Phase 6 (validate fail-closed). Phase 6 spec (`:46,172-182`) lại nói "chọn bằng cấu hình" | Không ghi | Mọi A/B ở 8.1 phải chạy qua script riêng hoặc phải nới loader. File này cũng nằm trong B9 | `mặc định không lý do` | vừa (quy trình) | Spec 8.1 chốt cách chạy thí nghiệm: script gọi `build_full_corpus_retrieval_service` với tham số, **không** đổi runtime |
| X.2 | Tham số tìm kiếm là hằng trong code; key Foods trong `settings.yaml` không được đọc | Pool 30, k=60, top-10, tên MiniLM, batch 8 là hằng. `retrieval.top_k`, `dense_weight`, `reranking.model`… thuộc Foods (B9 đang gỡ) | — | — | Dễ đọc nhầm là "đang cấu hình được" | `mặc định không lý do` | thấp | Sau B9 kiểm lại: chỉ còn key thật sự được dùng |

## 4. Mười chỗ đáng lo nhất (tác động × độ thiếu bằng chứng)

| Hạng | Chỗ | Vì sao lo | Bước đầu tiên |
|---:|---|---|---|
| 1 | **Cỡ chunk** (2.1, kèm 0.6, 2.3) | Tác động cao; chưa từng đo phương án nào, kể cả Foods. 75% chunk là một gạch đầu dòng; dữ liệu viết theo mức section. Phương án gộp bị bỏ bằng lập luận | H1 → H2 (build lại e5 local, free), đo bằng thước đo đã sửa ở hạng 5 |
| 2 | **Từ chối tất-cả-hoặc-không + context 5** (6.4, 6.1) | Nguồn mất điểm lớn nhất (22/158, mỗi câu 1/1/1). Lý do giới hạn 5 gắn với Qwen 9B đã bỏ. Mới chỉ có thăm dò trên case chọn theo lỗi | H4 trên 176 câu theo cặp (~0,07 USD); H8 chờ User quyết |
| 3 | **Model sinh, prompt, reasoning chưa từng so** (6.7, 6.5, 6.8) | Chọn model trên 5 câu không chấm. Prompt viết cho Qwen, thiếu 2 luật của spec. Reasoning để mặc định chưa rõ. Cam kết so Qwen ở Phase 8 đã rơi | Đưa so sánh model vào spec 8.1/8.2 (User duyệt provider); biến thể prompt ~0,024 USD |
| 4 | **Dense model** (3.1, 3.2) | Đặt trần cho mọi bước sau. Bằng chứng chỉ trên Foods, chunk khác ~2,9 lần; 3 ứng viên bị xóa mà không chấm toàn kho | Sau khi chốt chunker: e5-base / Qwen3-0.6B local (free) |
| 5 | **Thước đo chưa đủ để kết luận** (7B.5, 7.5, 7B.6, 7.3, 7B.1, 7B.2) | Không kiểm định theo cặp, không tập giữ kín, không mốc người, keyword proxy chưa kiểm, metric truy xuất không khớp cái LLM thấy. Không sửa thì 8.1 khó phân biệt cải tiến thật với nhiễu | **Làm trước tất cả** (mục 5, bước 0); phần lớn free |
| 6 | **Pool 30 và RRF k=60** (5.2, 5.3) | Pool là trần của mọi bước sau, chưa từng đo candidate recall; chunk F2 ở hạng 41/99/191 | Candidate recall @30/100/200 (free) |
| 7 | **Bảng: mỗi dòng 1 chunk** (2.2) | Ngược đề xuất của chính tài liệu thiết kế; dòng giá khó tìm (F2) | H3 (free) |
| 8 | **Reranker** (5.5) | Chỉ có MiniLM tiếng Anh, bằng chứng chỉ trên Foods; luật "vượt 512 thì bỏ rerank cả request" chưa từng đếm | Đếm tỉ lệ vượt 512 (free), rồi H5 (cần duyệt model) |
| 9 | **Ràng buộc tokenizer HuyDang** (2.3, 2.4) | Lý do đã hết; 23 block bị tách thành 90 chunk | H1 (free, rẻ nhất trong nhóm chunker) |
| 10 | **Bẫy hạ tầng thí nghiệm** (X.1, 4.3) | Loader chặn A/B qua cấu hình; kiểm tươi không biết khi chunker đổi → có thể đo nhầm index cũ mà không ai biết | Spec 8.1 quy định: script riêng, mỗi biến thể một collection + record riêng |

Ngay dưới top 10: BM25 tách âm tiết (3.7, chỉ Foods), chuẩn hóa NFC câu hỏi (0.5), validator
citation bỏ câu trả lời tốt (6.6), Representation A chưa ablation (2.7).

## 5. Thứ tự thí nghiệm đề xuất (đề xuất cho A/User, không đổi hành vi chatbot)

| Bước | Việc | Chi phí | Cần duyệt |
|---|---|---|---|
| 0a | Sửa thước đo trên dữ liệu đã có: paired bootstrap/permutation trong `compare` (tự kiểm Run 1 vs Run 2); macro theo nhóm; ma trận từ chối 2×2; metric bằng chứng @5 (`context-coverage`) | free | không (code evaluator — mức trung bình) |
| 0b | Quyết định của User: tách tập giữ kín (7.5); chấm tay 20 câu (7B.6); gold evidence 30–40 câu (7.3); pin model judge (7B.3) | công người | **User** |
| 1 | Đo chỉ đọc trên index hiện tại: candidate recall @30/100/200 (5.2); RRF k (5.3); exact vs HNSW (4.2); tỉ lệ vượt 512 của MiniLM (5.5); bản NFD của 176 câu (0.5); paired bootstrap `dense_bm25_rrf` vs native (5.1) | free | không |
| 2 | Phát lại trên câu trả lời đã lưu: chính sách validator citation (6.6) | free | không |
| 3 | Chunker, mỗi biến thể một collection riêng: H1 (2.3) → H3 (2.2) → H2 (2.1, gồm biến thể section-level) → A′ (2.7); kèm loại inventory (0.2), fence (0.7), 3 cặp lặp (2.6) | free (e5 local); câu trả lời ~0,05 USD/biến thể | spec 8.1 (đổi chunker = rủi ro cao) |
| 4 | Sinh câu trả lời: H4 context 10 (6.1); biến thể prompt (6.5); reasoning effort (6.8) | ~0,03–0,1 USD mỗi lượt | spec 8.1; 6.8 đổi contract |
| 5 | Có phí / model mới: H8 (6.4, User quyết); reranker bge-v2-m3 (5.5); dense e5-base/Qwen3-0.6B/8B (3.1, 3.3); so model sinh Qwen 3.5-9B (6.7); H10 (6.10) | vừa | **User** (model/provider/egress) |

## 6. Chỗ lệch giữa tài liệu và code (mới so với H-report)

1. **Chunker "có gộp" trên giấy, không gộp trong code:** spec umbrella `:86` ("grouping ưu tiên giữ đơn
   vị cùng chủ đề"), decisions `:429`, docstring `full_corpus_chunker.py:3` ("semantic grouping").
2. **Bảng:** decisions `:440` "không đặt một hàng làm mặc định", trong khi code tách đúng 1 dòng.
3. **Inventory:** `Project_Status.md` §5 ghi "inventory bị loại khỏi discovery", nhưng
   `performing_arts/performing-arts-entities-inventory.md` vẫn được index.
4. **Nội dung bị bỏ:** spec/plan nói không bỏ evidence, nhưng 2 code fence bị bỏ không báo (0.7).
5. **Template ↔ chunker:** template viết theo section; chunker cắt theo block (0.6).
6. **Loader ↔ spec Phase 6:** spec nói runtime "chọn bằng cấu hình"; loader chỉ cho một tổ hợp (X.1).
7. **Kiểm tươi** không ghi cấu hình chunker/tokenizer (4.3).
8. **Log bỏ rerank** được hứa (decisions `:201-203`) nhưng chưa report nào ghi số (5.5).
9. **Prompt thiếu 2 luật** của spec Phase 6 §10 (6.5); chưa thấy quyết định nào bỏ chúng (chưa kiểm
   sâu).
10. **Cam kết so Qwen ở Phase 8** (amendment 10-01 §5, 10-23 R6) không có trong H1–H14, §8.4 hay
    `CURRENT_HANDOFF.md` (6.7).
11. **Spec 7B gọi "macro-average theo case"**, nhưng code tính trung bình có trọng số theo case, không
    phải macro theo nhóm (7B.4).
12. **`Project_Status.md` §5 `:103`** còn ghi "User chấm ~20 case", trong khi 7B đóng không có điểm
    người.
13. **Sửa report cũ của C:**
    - `reports/phase_8_candidate_hypotheses_2026_10_24.md` H6/O9 ghi "Foods: hybrid RRF không hơn
      dense+BM25 cục bộ". Thực ra bản "dense+BM25 cục bộ" ở Foods 08b là **weighted 0,6/0,4**, không
      phải RRF, nên tổ hợp runtime chưa từng chạy trên Foods.
    - `bao_cao_he_thong/BAO_CAO_BO_CAU_HOI_GOLDEN.md` §2 ghi "gộp thành 1 file (xáo cố định)" là
      **sai**: không xáo (mục 1.1).
    - `BAO_CAO_TIM_KIEM.md` §3 ghi MiniLM "Đã thử, chưa áp dụng" mà không nói là chỉ thử trên Foods.
    - `BAO_CAO_SINH_CAU_TRA_LOI_API.md` §5 ghi Representation B "chưa từng dùng": generator B đã gọi
      live 1 lần, chỉ chưa có index.

    C đề xuất tự sửa 3 file `bao_cao_he_thong` khi A giao (C không sửa ngoài khai báo C11).

## 7. Cần nghiên cứu ngoài (câu hỏi cho ChatGPT — A gộp vào yêu cầu chung)

1. **Cỡ chunk cho tài liệu tiếng Việt viết chủ yếu bằng gạch đầu dòng:** có số đo nào so "mỗi item một
   chunk" với "gộp item cùng mục tới N token", section-level, hay small-to-big, trên embedding đa ngôn
   ngữ cỡ nhỏ (multilingual-e5-small)?
2. **Bảng trong dense retrieval** (không phải LLM hiểu bảng): có số đo cho cỡ nhóm dòng, hoặc cho việc
   chuyển dòng bảng thành câu văn so với giữ Markdown, với e5?
3. **Tiền tố tiêu đề/heading vào passage ngắn** ("contextual chunk headers"): giúp hay hại e5 khi nhãn
   chiếm >50% token? Có ablation công bố không?
4. **Chuẩn hóa Unicode (bổ sung câu hỏi NFC của A):**
   - Tỉ lệ thực tế người dùng gửi tiếng Việt dạng NFD (macOS, bàn phím ảo, copy từ PDF) là bao nhiêu?
   - Kiểu đặt dấu cũ/mới ("hoà"/"hòa") có cần chuẩn hóa cho BM25 và e5 không?
   - Tokenizer SentencePiece của multilingual-e5 có tự chuẩn hóa không? (Probe C: `input_ids` NFD ≠
     NFC.)
5. **Qdrant:** khi không đặt `hnsw_ef`, search dùng ef nào? Collection ~8,5k point chia 6 segment, dưới
   `full_scan_threshold`, có thực chất đang quét đủ (exact) không?
6. **RRF k=60 với danh sách ngắn (30/nhánh):** có bằng chứng chọn k nhỏ hơn hoặc fusion có trọng số cho
   hybrid tiếng Việt không?
7. **Reranker:**
   - MiniLM tiếng Anh (WordPiece) sinh bao nhiêu token mỗi âm tiết tiếng Việt có dấu?
   - Giới hạn độ dài thực tế của bge-reranker-v2-m3 và Qwen3-Reranker là bao nhiêu?
8. **Qwen3-Embedding:**
   - Nên viết instruction cho câu hỏi tiếng Việt bằng tiếng Việt hay tiếng Anh?
   - Mất bao nhiêu chất lượng khi dùng MRL 1024 thay vì 4096?
   - Nebius phục vụ ở độ chính xác nào?
9. **BM25 tiếng Việt:** có so sánh đối đầu đo được giữa bigram âm tiết và pyvi/underthesea không? (H7
   ghi là chưa có.)
10. **`gpt-6-luna`:**
    - Có nhận reasoning effort không, mặc định là gì?
    - Tokenizer và context window chính thức là gì?
    - Structured output (JSON một field) có làm giảm tuân thủ citation không?
11. **Trả lời một phần vs từ chối cả câu** với câu hỏi nhiều vế: có nghiên cứu đối chứng không? (H8 ghi
    là chưa có.)
12. **Thứ tự chunk khi context ngắn** (<2k token): hiệu ứng "lost in the middle" có còn đáng kể không?
13. **`qwen/qwen3.5-9b` trên OpenRouter:** giá, nhà cung cấp, structured output có ổn định không (cho
    phép so model ở 6.7)?
14. **Công cụ chấm claim-level** (RAGAS/DeepEval…): có cái nào dùng ổn với tiếng Việt và judge rẻ không?

## 8. Giới hạn

- Tác động là ước lượng theo cơ chế, chưa đo. Số đếm theo trạng thái phụ thuộc cách tách dòng; một
  số dòng gộp nhiều quyết định nhỏ (3.5, 3.8, 6.9, 6.11).
- Số dòng code theo `c57ec43`; sau khi B9 commit, `settings.yaml`/`settings_loader.py` sẽ lệch dòng
  (tên key không đổi).
- Một số dữ kiện lấy từ sub-agent mà C chưa kiểm lại từng dòng (ví dụ số Foods 08a/08b/08c, latency).
  Các điểm then chốt cho xếp hạng đã kiểm ở mục 1.1.
- Không chạy test, không chạy evaluator, không gọi API trả phí; GET Qdrant một lần.

## 9. Tái lập

Script ngoài repo (không commit), chạy từ repo root bằng `HF_HUB_OFFLINE=1 uv run python <script>`:

- `/tmp/c11/nfc_probe.py`, `nfc_probe2.py` (NFC corpus/tokenizer);
- `/tmp/c11/p02/probe*.py` (thống kê block/chunk, block bị tách vì tokenizer, fence bị bỏ, guide/inventory
  trong top-k);
- ghi chú từng vùng: `/tmp/c11/area2_verified.md`, `area3_verified.md`, `nfc_facts.md`.

Đầu vào: corpus 205 file, collection `hue_full_corpus_7a2_e5_small_384` (8.459 point), build record
`full_corpus_build:v3`, kết quả 7B ở `data/evaluation/phase_7b/`.
