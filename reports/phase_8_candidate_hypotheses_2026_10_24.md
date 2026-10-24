# Phase 8 — danh sách giả thuyết cải tiến (rà soát lựa chọn Phase 2–6)

Ngày: 2026-10-24 · Người làm: C · Loại: rà soát chỉ đọc (rủi ro thấp) · Việc:
`session_prompt/CURRENT_HANDOFF.md` → "Việc của C".

Không sửa code, dữ liệu hay Qdrant; không gọi API trả phí. Report không chép nội dung corpus
hay câu hỏi Golden; chỉ ghi số liệu tổng hợp và tên file/chunk (như các report Phase 6 đã làm).

## 1. Cách làm và mức tin cậy

- Đọc: `Project_Status.md` §4–5, `guides/full_corpus_rag.md` (cập nhật 7A2 + "Quyết định đã
  chốt"), spec umbrella `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`,
  code `backend/{ingestion,embedding,retrieval,llm}/`, `backend/scoring/bm25.py`,
  `backend/reranking/cross_encoder.py`; tra cứu report Phase 6 (F1/F2), spec Phase 6
  2026-09-14 §10, kết quả benchmark Foods cũ `evaluation/results/phase8_*.csv`.
- Chạy 3 probe chỉ đọc (script ngoài repo, `/tmp/c_probe/`, `uv run` trong `.venv` dự án,
  `HF_HUB_OFFLINE=1`): thống kê chunk từ chunker hiện hành; truy xuất thật
  `build_full_corpus_retrieval_service("e5-small-384", treatment, "none")` cho 4 case live
  Phase 6 và 176 câu Golden (chỉ đếm độ đa dạng nguồn, **không** tính metric chất lượng — đó là
  việc của 7B); đo token của các bảng bị tách. Qdrant chỉ `query_points` (đọc).
- Ký hiệu cột "Căn cứ": **Q** = quan sát đã đo trong report này hoặc report trước;
  **L** = bằng chứng lịch sử Foods (45 câu, chunker/collection khác, chỉ tham khảo);
  **G** = giả thuyết, chưa có số liệu.
- Cột "Cách làm phổ biến" ghi theo hiểu biết của tôi, **chưa đối chiếu nguồn**. Yêu cầu nghiên
  cứu kèm URL đã viết ở `gửi chatgpt/tìm thông tin/phase_8_retrieval_improvements_2026_10_24.md`
  (chờ User gửi); khi có kết quả, cột này cần được cập nhật bằng nguồn.

## 2. Quan sát mới từ probe

| # | Quan sát | Số liệu |
|---|---|---|
| O1 | Chunk nhỏ, vụn | 8.459 chunk; token e5 (đã gồm tiêu đề + heading) p10 35, p25 55, trung vị 85, p75 122, p95 188, max 366. 20,3% chunk ≤ 48 token; 33,3% ≤ 64. Phần thân (`body`) trung vị 193 ký tự; 22,4% thân < 100 ký tự |
| O2 | Mỗi khối Markdown là một chunk, không gộp khối cạnh nhau | 2.457 mục (source + heading_path); trung vị 3 chunk/mục, p90 6, max 19; 18,4% mục chỉ có 1 chunk. Role pattern: 8.276 chunk chỉ `body`; 174 `header+body` (dòng bảng/mục con bị tách) |
| O3 | Ràng buộc HuyDang 256 vẫn quyết định cỡ chunk dù HuyDang và e5-base không còn là candidate | Chunker vẫn kiểm cả 3 tokenizer (`settings.yaml` `embedding_models`); max HuyDang 255/256. 14 bảng bị tách theo dòng thành 118 chunk; **6 bảng bị tách chỉ vì vượt HuyDang 256** (vừa e5 512) |
| O4 | Chunk bảng giá của F2 là **một dòng bảng** (`header+body`), bảng gốc 12 dòng, 576 token e5 (vượt cả e5 512) | Với câu hỏi F2: chunk `Vé tham quan Quần thể Di tích Cố đô Huế.md#9` hạng dense **191**, #77 hạng 99, #78 hạng **41**; cả ba ngoài top-30 sparse (native hybrid); không vào top-10 ở cả `dense_bm25_rrf` lẫn `native_hybrid_rrf` |
| O5 | `dense_bm25_rrf` (runtime) chỉ chấm BM25 **trong** 30 ứng viên dense → về cấu trúc không cứu được chunk dense bỏ sót | `backend/retrieval/full_corpus.py` nhánh `dense_bm25_rrf`; F2 #78 hạng 41 không thể vào |
| O6 | Context dùng rất ít ngân sách | F2: 5 nguồn = 777 token (report Phase 6) trên `context_limit` 16.384 (−2.048 output −512 margin) |
| O7 | Độ đa dạng nguồn top-5 trên Golden 176 (`dense_bm25_rrf`; native hybrid gần như giống) | Số file khác nhau trong top-5, trung bình / tỉ lệ chỉ 1 file: `multi_source` 2,79 / 10%; `comparative` 2,44 / 16%; `conditional` 2,17 / 45%; `direct_fact` 1,87 / 48%; `out_of_scope` 3,94 / 0%. Vậy "top-5 toàn một tài liệu" (F1 Phase 6) **không** phổ biến ở câu `multi_source` |
| O8 | Prompt từ chối kiểu tất cả-hoặc-không | `backend/llm/full_corpus_prompt.py`: "Nếu bằng chứng không đủ, trả đúng duy nhất câu sau". Đúng spec Phase 6 2026-09-14 §10 ("context tồn tại nhưng không đủ → trả đúng chuỗi này"), nhưng spec umbrella §1 và Decision #6a nói "trả phần có căn cứ hoặc nêu thiếu thông tin". Phase 6 F2: một nửa câu có bằng chứng (miễn giảm) vẫn bị từ chối |
| O9 | Reranker trong code là MiniLM tiếng Anh; vượt độ dài thì bỏ rerank cả request | `backend/reranking/cross_encoder.py`; L: Foods 45 câu, MiniLM làm MRR@5 −0,080 (e5), −0,044 (hybrid), ~0 (HuyDang) |
| O10 | BM25 tách theo âm tiết, không bigram; query trọng số 1,0 mỗi term | `backend/scoring/bm25.py` `\w+` lowercase; vocabulary 5.660 |
| O11 | Representation B có code nhưng chưa từng build; B chỉ nhìn **nội dung chunk**, không nhìn cả tài liệu | `backend/llm/full_corpus_prompt.py` `REPRESENTATION_B_*`, `generator_openai_full_corpus.py` |

## 3. Bảng giả thuyết

Mức ưu tiên sơ bộ: **P1** gắn với vấn đề đã quan sát, chi phí thấp; **P2** gắn với vấn đề
quan sát nhưng tốn hơn hoặc đổi contract; **P3** chưa có vấn đề quan sát rõ.

Cách đo (chung): retrieval-only trước — MRR@10, nDCG@10, Keyword Coverage@10 trên 176 câu, tách
theo `category` (đặc biệt `conditional`, `multi_source`), không tốn phí. Chỉ cấu hình qua vòng
retrieval mới chạy end-to-end (Accuracy/Completeness/Relevance, có phí). Thiết kế evaluator
thuộc 7B; ở đây chỉ ghi metric nào.

| ID | Lựa chọn hiện tại (dẫn chứng) | Cách làm phổ biến (chưa đối chiếu nguồn) | Giả thuyết lợi ích | Căn cứ | Cách đo trên Golden 176 | Chi phí / rủi ro | Ưu tiên |
|---|---|---|---|---|---|---|---|
| H1 | Chunker kiểm 3 tokenizer, gồm HuyDang 256 và e5-base đã bỏ (`settings.yaml` `full_corpus.embedding_models`; spec umbrella §5) | Chỉ kiểm giới hạn của model đang dùng | Bỏ ràng buộc thừa → 6 bảng thôi bị tách; mở đường cho H2/H3 | Q (O3) | Retrieval 3 metric, so riêng câu có đáp án trong 6 bảng đó | Sửa config + build lại index e5 (local, miễn phí); Qwen3-8B max 32k không ràng buộc. Đổi số chunk → build record/sparse state mới | P1 |
| H2 | Mỗi khối Markdown một chunk, không gộp (`full_corpus_chunker.py` `chunk_document`; spec §4 "không trộn sibling độc lập để lấp token budget") | Chia theo heading rồi gộp khối liền nhau trong cùng mục tới một ngưỡng token (vài trăm token) | Chunk đủ ngữ cảnh hơn → dense khớp tốt hơn, ít chunk một-dòng vô nghĩa; top-5 chứa nhiều thông tin hơn | Q (O1, O2) | Retrieval 3 metric + answer 3 metric. **Bẫy đo:** chunk to chứa nhiều keyword hơn → Keyword Coverage@10 tăng "miễn phí"; cần so cả answer metric hoặc ghi tổng token context | Đổi nguyên tắc spec umbrella §4 (cần User duyệt); phải giữ luật điều kiện/phương án loại trừ; build lại index; chunk to dễ vượt MiniLM 512 (H5) | P1 |
| H3 | Bảng quá dài → mỗi dòng một chunk + header (`chunk_document` Case 1) | Nhóm nhiều dòng một chunk (lặp header) tới ngưỡng; hoặc thêm câu văn hóa từng dòng vào `search_text` | Dòng giá vé (F2) được tìm thấy | Q (O4) | Hạng chunk F2 (probe như §2) + metric câu `conditional`/có giá | Nhỏ, cục bộ trong chunker; build lại index. Viết câu văn cho dòng là biến đổi representation — cần quyết định riêng | P1 |
| H4 | Context tối đa 5 chunk (`settings.yaml` `max_context_documents: 5`; spec §8) | Đưa nhiều chunk hơn (10–20) hoặc small-to-big: tìm bằng chunk nhỏ, đưa cả mục cha | Câu gộp nhiều ý và `multi_source` có đủ bằng chứng; gần như không đụng retrieval | Q (O6) | Answer 3 metric (Completeness chính); retrieval không đổi | Chỉ đổi config/context builder; tăng token input (vẫn ≪ 16k); nhiều nguồn nhiễu có thể giảm Relevance | P1 |
| H5 | Reranker `none`; code chỉ có MiniLM tiếng Anh (`cross_encoder.py`; spec §7) | Cross-encoder đa ngôn ngữ (vd. bge-reranker-v2-m3, Qwen3-Reranker-0.6B) trên 30–100 ứng viên | Xếp lại đúng chunk bị dense đẩy xuống (F2 #78 hạng 41 nếu pool 50+) | L (O9), Q (O4) | Retrieval 3 metric; so no-rerank vs reranker với cùng pool; ghi latency CPU | Model mới (cần User duyệt), tải model ~0,5–2 GB, latency CPU; pool > 30 đổi contract Phase 5 | P1 |
| H6 | Runtime `dense_bm25_rrf` (BM25 chỉ chấm lại pool dense) (`settings.yaml`; spec §7) | Hybrid thật: dense và sparse truy xuất độc lập rồi fusion | Cứu chunk dense bỏ sót mà BM25 bắt được | Q (O5), L (Foods e5: hybrid RRF không hơn dense+BM25 cục bộ, recall@5 0,844 vs 0,863) | Retrieval 3 metric; chỉ đổi config (`native_hybrid_rrf` đã có code) | Gần như miễn phí. Trên 4 case Phase 6 không khác biệt → có thể không đổi gì | P1 (rẻ, nên đo cùng baseline 7B) |
| H7 | BM25 âm tiết, không bigram (`bm25.py`) | Tách từ tiếng Việt (pyvi/underthesea) hoặc thêm bigram âm tiết | Khớp cụm từ ("Đại Nội", tên món) chính xác hơn, BM25 bớt nhiễu | G (O10; F2 ngoài top-30 sparse) | Retrieval 3 metric, nhánh sparse riêng + sau fusion | Dependency mới (tách từ) hoặc vocabulary to hơn (bigram); sparse state + index build lại | P2 |
| H8 | Prompt từ chối tất cả-hoặc-không (`full_corpus_prompt.py`; spec Phase 6 §10) | Trả lời phần có căn cứ, nói rõ phần thiếu | Câu gộp nhiều ý không bị từ chối cả câu | Q (O8, Phase 6 F2) | Answer 3 metric (Completeness) + tỉ lệ từ chối nhầm ở câu không phải `out_of_scope` và tỉ lệ từ chối đúng ở `out_of_scope` | Đổi contract (spec Phase 6 §10/§11: citation validator cho phép fallback có/không marker) — cần User; rủi ro trả lời bịa phần thiếu | P2 |
| H9 | Dense e5-small 384 (local); Qwen3-8B chưa có index (`full_corpus.py` `DENSE_MODEL_SPECS`) | Model embedding lớn hơn / mạnh hơn cho tiếng Việt | Dense chính xác hơn với câu dài, gộp ý | L (Foods: Qwen3-0.6B kém e5-small; e5-base không hơn e5-small về MRR) · G (8B) | Retrieval 3 metric, cùng chunker | Paid OpenRouter (8.459 chunk, đã gặp 504/429 — quyết định hiện hành), data egress; 8B nên đo **sau** khi chốt chunker để không phải build 2 lần | P2 |
| H10 | Representation B (LLM sinh ngữ cảnh) chỉ từ nội dung chunk, chưa build (`full_corpus_prompt.py`) | Contextual retrieval: LLM sinh ngữ cảnh từ **cả tài liệu** cho từng chunk | Chunk vụn được "đặt vào ngữ cảnh" → dense/BM25 tốt hơn | G (O11) | Retrieval 3 metric, A vs B cùng model/pipeline (spec §12 bước 5) | Paid (~8.459 call), phụ thuộc H2 (gộp chunk có thể giảm nhu cầu B) | P2 |
| H11 | Pool 30, RRF k=60, top-10 (`full_corpus.py` `reciprocal_rank_fusion`) | Pool 50–100 khi có reranker; weighted fusion | Ít bỏ sót hơn trước rerank | L (Foods: weighted vs RRF lẫn lộn — HuyDang 0,911 vs 0,878, e5 0,830 vs 0,844 recall@5) | Candidate recall (keyword có trong pool), retrieval 3 metric | Rẻ; chỉ có ý nghĩa khi đi cùng H5 | P3 |
| H12 | Không giới hạn số chunk/tài liệu trong top-k | MMR / tối đa n chunk mỗi file | Câu `multi_source` có nhiều nguồn hơn | Q yếu (O7: `multi_source` chỉ 10% top-5 một file) | Retrieval 3 metric theo `multi_source`, `comparative` | Có thể đẩy chunk đúng ra khỏi top-5 ở `direct_fact` (48% một file là hợp lý) | P3 |
| H13 | Câu hỏi đi thẳng vào retrieval, một lượt | Tách câu hỏi gộp / multi-query bằng LLM trước retrieval | Câu gộp hai ý (F2) truy xuất đủ cả hai | Q (một case F2) | Retrieval + answer theo `conditional`, `multi_source` | Thêm 1 LLM call/request (paid, latency); sát ranh giới Agentic Phase 9 | P3 (cân nhắc cho Phase 9) |
| H14 | Không lọc/định tuyến theo `domain` (metadata v2: không payload index/filter) | Lọc theo domain/loại tài liệu | — | Không có vấn đề quan sát | — | Thêm phân loại query; không khuyến nghị | Không đề xuất |

Các lựa chọn rà và **không** thấy lý do đổi: tiền tố `query:`/`passage:` của e5 và instruction
Qwen3 đúng model card (`full_corpus.py` `prepare_*`); ghép tiêu đề + heading vào `search_text`
(Representation A) là cách phổ biến; RRF k=60 là mặc định thông dụng; context builder không cắt
chunk; citation do backend ánh xạ (`backend/llm/citations.py`); API/UI contract tối giản.

## 4. Thứ tự đề xuất (sơ bộ, để A/User cân nhắc)

1. **Cùng baseline 7B, gần như miễn phí:** đo thêm `native_hybrid_rrf` (H6) bên cạnh runtime
   `dense_bm25_rrf` — chỉ đổi config, giúp biết trần của nhánh sparse trước khi sửa BM25.
2. **Chunker một lần** (H1 → H3 → H2): bỏ tokenizer thừa, nhóm dòng bảng, gộp khối nhỏ trong
   cùng mục; mỗi bước build lại index e5 local và đo retrieval-only. Đây là thay đổi nền, nên
   làm trước reranker/embedding để không phải đo lại.
3. **Context và reranker** (H4, H5, H11) trên chunker đã chốt.
4. **BM25 tiếng Việt** (H7) và **prompt trả lời một phần** (H8).
5. **Có phí:** Qwen3-8B (H9), Representation B/contextual (H10) — sau khi chunker ổn định.

Điểm cần lưu khi thiết kế đo: các thay đổi chunker (H1–H3) làm đổi đơn vị mà Keyword
Coverage@10 đếm; so sánh giữa hai chunker cần answer metric hoặc kèm tổng token context, không
chỉ dựa vào keyword proxy.

## 5. Chỗ lệch tài liệu và câu hỏi cho A

1. **Spec lệch nhau về câu trả lời một phần (O8):** spec umbrella §1 + Decision #6a cho phép "trả
   phần có căn cứ", spec Phase 6 §10 và prompt bắt từ chối cả câu. Không phải bug code (code theo
   spec Phase 6), nhưng là lựa chọn của User — đề xuất A đưa vào brainstorm Phase 8 (H8).
2. **`Project_Status.md` §1/§4 ghi "mỗi chunk vừa cả 3 tokenizer"** — đúng hiện trạng, nhưng
   e5-base và HuyDang đã không còn là candidate; ràng buộc này giờ chỉ còn tác dụng làm chunk
   nhỏ (O3). User đã nêu "bỏ ràng buộc huydang 256" cho Phase 8 — số liệu O3 ủng hộ.
3. **F1 Phase 6** (top-5 một tài liệu) phần lớn do câu test; trên Golden `multi_source` chỉ 10%
   top-5 là một file (O7). Đề xuất hạ ưu tiên đa dạng nguồn (H12) cho tới khi baseline 7B cho
   thấy `multi_source` kém.
4. Cần User gửi yêu cầu nghiên cứu
   `gửi chatgpt/tìm thông tin/phase_8_retrieval_improvements_2026_10_24.md` để bổ sung URL cho
   cột "Cách làm phổ biến" và chọn model reranker/embedding/tách từ cụ thể.

## 6. Giới hạn

- Probe đa dạng nguồn (O7) chỉ đếm số file trong top-5, không biết file nào đúng — không phải
  metric chất lượng.
- Hạng chunk F2 (O4) là một câu hỏi; không suy ra tỉ lệ chung.
- Số liệu Foods (L) dùng chunker, collection và Golden khác; chỉ là gợi ý hướng.
- Cột "Cách làm phổ biến" chưa có nguồn đối chiếu (chờ nghiên cứu ngoài).
- Không chạy test, không chạy evaluator, không gọi API trả phí.

## 7. Tái lập probe

Script ngoài repo (không commit): `/tmp/c_probe/chunk_stats.py`, `retrieval_probe.py`,
`chunk9.py`, `table_split.py`. Chạy từ repo root:

```bash
HF_HUB_OFFLINE=1 uv run python /tmp/c_probe/<script>.py
```

Đầu vào: corpus và Qdrant collection `hue_full_corpus_7a2_e5_small_384` hiện hành (8.459 point),
build record `full_corpus_build:v3`. Output chỉ in số liệu và tên file/chunk.
