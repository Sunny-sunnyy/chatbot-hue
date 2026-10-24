# Kế hoạch G1 — chẩn đoán chỉ đọc trên index hiện tại (tiêu chí ghi trước)

Người viết: B (Claude Opus 5.5, terminal `hue-rag-b0`) · Ngày: 2026-10-24 21:32 +0700 (lấy bằng `date`) ·
Trạng thái: **nháp, chờ A duyệt trước khi đo** · Việc: B15 (tin nhắn A 21:31) · Spec 8.1 §5 G1, skill `run-experiment`.

Tiêu chí dưới đây ghi **trước khi thấy số**; không đổi sau khi đo. Kết quả âm giữ nguyên.

## 0. Chung cho mọi thí nghiệm G1

- **Baseline:** runtime đang chạy, commit `0131afb` — `e5-small-384`, `dense_bm25_rrf`, pool 30, RRF k=60, top-10,
  context 5, reranker `none`, collection `hue_full_corpus_7a2_e5_small_384`. Trước khi đo: chạy lại retrieval runtime
  176 câu, phải giống byte mốc `cefb2d1a…`; native phải giống byte mốc `1fbb5c17…` (B13). Khác thì dừng (skill §3.1).
- **Chỉ đọc:** không ghi Qdrant, không tạo collection, không gọi API trả phí (G1 = 0 USD). Code production gọi qua tham
  số B11/B13; logic biến thể (DBSF, biến đổi câu hỏi) nằm trong harness `backend/experiments/phase_8_1/`.
- **Dữ liệu:**
  - chọn trên **dev** (`knowledge-base-hue/evaluation/phase_8_1/split.json`): 120 câu, 108 câu trong kho cho metric
    keyword; **40 câu dev có đoạn đúng** (`data/phase_8_1/gold/gold_*.jsonl`, sau khi A áp m1–m8 của B14);
  - xác nhận trên **test** (50 câu trong kho, 15 câu có đoạn đúng) chỉ cho phương án "tốt hơn";
  - câu kín không đụng.
- **Đoạn đúng:** một chunk *trúng* một trích dẫn gold khi cùng `source` và một `evidence_parts` của chunk giao khoảng
  `[start, end)` của trích dẫn. Một **fact** được phủ khi ≥1 trích dẫn của fact có chunk trúng. Metric theo câu:
  `gold_all` (mọi fact được phủ, 0/1) và `gold_frac` (tỉ lệ fact được phủ). Đo ở 4 tầng: **pool** (tập ứng viên trước
  RRF) / **top-10** / **context-5** (đúng các đoạn `FullCorpusContextBuilder` đóng gói) / (G1.6) câu trả lời.
- **Metric phụ:** MRR@10, nDCG@10, keyword coverage@10 (`score_retrieval` của evaluator, như 7B).
- **So sánh theo cặp:** paired bootstrap 10.000 lần, CI 95%, thắng/hòa/thua (hàm `bootstrap_mean_diff`/`verdict` của
  evaluator C16). >1 biến thể cùng câu hỏi nghiên cứu ⇒ Holm. "Không khác" = CI chứa 0.
- **Hòa điểm ở biên (m1 của C19):** với mọi pool N của nhánh sparse, báo số câu có điểm hạng N = điểm hạng N+1.
- **Pilot:** 5 câu dev có đoạn đúng, `random.Random(20261024).sample`, chỉ để chắc harness chạy (không kết luận).
- **Hợp đồng kiểm:** C review chéo; B nộp JSONL từng câu + bảng tổng; C tự chạy lại ít nhất G1.1 và một biến thể G1.3.
- **Trần:** 0 USD; GPU không dùng; ≤ 1 giờ máy cho cả G1.

## 1. Thí nghiệm

```yaml
- experiment_id: G1.1_candidate_recall
  question: "Đoạn đúng có nằm trong tập ứng viên không, ở pool nào, nhánh nào?"
  baseline: runtime pool 30
  changed_variable: candidate_pool ∈ {30, 100, 200} (đo riêng nhánh dense, nhánh sparse của native, và hợp hai nhánh)
  data: {group: dev, gold_cases: 40, keyword_cases: 108}
  primary_metric: gold_all ở tầng pool (hợp dense ∪ sparse) theo pool
  secondary: gold_frac; keyword (mọi keyword đáp án có trong văn bản ứng viên); số câu hòa điểm biên sparse
  guardrails: []   # chẩn đoán, không chọn phương án
  decision_rule: >
    Nếu ở pool 200 hợp hai nhánh vẫn thiếu đoạn đúng ở > 50% câu lỗi (câu có gold_all = 0 ở top-10 runtime)
    thì dừng tối ưu fusion/rerank, chuyển thẳng G3 (điều kiện dừng sớm spec §5).
  result: null
- experiment_id: G1.2_hnsw_vs_exact
  baseline: dense HNSW mặc định, pool 30
  changed_variable: search_params = SearchParams(exact=True)
  data: {group: dev, keyword_cases: 108}
  primary_metric: trùng top-10 và top-30 dense (Jaccard, theo câu)
  secondary: latency dense p50/p95 (ms); gold_all@pool dense
  decision_rule: "trùng top-10 ≥ 99% câu và gold_all không đổi ⇒ giữ HNSW; ngược lại ghi và đề xuất cho 8.2"
  result: null
- experiment_id: G1.3_fusion
  baseline: runtime dense_bm25_rrf pool 30, k 60
  variants:   # mỗi dòng đổi đúng một thứ so với baseline
    - native_hybrid_rrf pool 30
    - native_hybrid_rrf pool 100
    - dense_bm25_rrf k ∈ {2, 10, 30}
    - native_hybrid_rrf pool 30, k ∈ {2, 10, 30}
    - DBSF (harness, trên điểm hai nhánh native pool 30), trọng số từ khóa 0,2 và 0,3
  data: {group: dev, gold_cases: 40, keyword_cases: 108}
  primary_metric: gold_all ở top-10 (40 câu); MRR@10 (108 câu)
  secondary: gold_all ở context-5; nDCG@10; keyword coverage@10; theo loại câu
  guardrails:
    - "0 câu (trong 40) mất đoạn đúng khỏi top-10 so với baseline"   # bài học private: từ khóa chọn ứng viên dễ làm mất đáp án
    - "nDCG@10 không tụt (CI không nằm hẳn dưới 0)"
  decision_rule: >
    "tốt hơn" = primary CI > 0 (sau Holm trong nhóm biến thể) VÀ đủ guardrail; xác nhận lại trên test (15 + 50 câu) trước khi
    đề xuất cho 8.2. Ngược lại: không đổi / kém hơn / chưa rõ.
  result: null
- experiment_id: G1.4_query_form
  baseline: câu hỏi gốc (dev), runtime
  changed_variable: biến đổi câu hỏi ∈ {NFD, bỏ dấu, kiểu dấu cũ (òa→oà, úy→uý…)}; mỗi biến đổi có và không có NFC trước khi tìm
  data: {group: dev, keyword_cases: 108, gold_cases: 40}
  primary_metric: MRR@10 của câu biến đổi so với câu gốc (theo cặp)
  secondary: gold_all@top-10
  decision_rule: >
    Biến đổi làm MRR tụt (CI < 0) mà NFC phục hồi (CI chứa 0 so với gốc) ⇒ đề xuất NFC query ở 8.2.
    Bỏ dấu tụt mạnh ⇒ ghi giới hạn (cần tách từ/khử dấu, ngoài G1).
  result: null
- experiment_id: G1.5_minilm_overlength
  baseline: runtime top-30 sau RRF
  measure: tỉ lệ câu (dev 108) có ≥1 cặp (câu hỏi, search_text) > max_length MiniLM (512) — luật hiện tại bỏ rerank cả request
  decision_rule: "chỉ ghi số; dùng ở G4 để biết reranker MiniLM sẽ bị bỏ bao nhiêu"
  result: null
- experiment_id: G1.6_failure_layers
  data: {gold_cases: 55 (40 dev + 15 test, báo tách nhóm; test đã bị nhìn ở bước này — ghi rõ)}
  layers: [có trong kho (gold), vào pool 30 runtime, vào top-10, vào context-5, câu trả lời 7B Run 1 từ chối/không, fact được dùng + trích đúng]
  measure: tầng đầu tiên mà gold_all = 0, theo câu và theo loại câu
  note: >
    4 tầng đầu tính tự động. Hai tầng cuối cần judge Claude (sub-agent) trên câu trả lời 7B đã lưu — được phép vì đo
    khâu sau bước sinh (skill §3.5); làm sau khi A duyệt, 0 USD.
  result: null
```

## 2. Không làm ở G1 (lý do)

- Reranker (G4), chia đoạn (G3), sinh câu trả lời (G2): khác gate.
- Tinh chỉnh BM25 k1/b: spec §4 NOT RUN.
- Chạy trên test để chọn: cấm — test chỉ xác nhận.

## 3. Harness và thử khô (B15, 21:33–21:45)

**Code:** `backend/experiments/phase_8_1/g1_retrieval.py` (mới, 293 dòng; `__init__.py` rỗng ở `experiments/` và `experiments/phase_8_1/`). Lệnh `run` (một cấu
hình → JSONL từng câu ở `data/phase_8_1/g1/<tên>.jsonl`, private, git bỏ qua) và `compare` (theo cặp, dùng
`bootstrap_mean_diff`/`verdict`/`holm_adjust` của evaluator). Gọi production: `build_full_corpus_retrieval_service`
(tham số `candidate_pool`, `rrf_k`, `search_params`), `FullCorpusContextBuilder` (qua `build_context_builder`),
`build_retrieved_document`, `score_retrieval`, `encode_sparse_query`, `CrossEncoderReranker.input_token_count`.
Logic chỉ có trong harness: DBSF (chuẩn hóa mean ± 3σ mỗi nhánh, cộng có trọng số, phá hòa theo point_id), biến đổi
câu hỏi (`nfd`, `noaccent`, `tone_swap` oa/oe/uy hai chiều, bỏ qua sau `q`), chấm đoạn đúng theo offset trên
payload Qdrant (scroll chỉ đọc). Ghi chú cách đọc: với runtime `dense_bm25_rrf`, "pool_sparse" là các đoạn BM25 > 0
*trong* tập dense (BM25 chỉ xếp lại), nên `pool_union` = `pool_dense`; nhánh sparse độc lập chỉ có ở native.
`candidate_pool` vừa là pool mỗi nhánh vừa là số giữ sau RRF (B11).

**Thử khô** (5 câu dev có đoạn đúng, `random.Random(20261024).sample` → câu 169, 48, 27, 89, 17; 0 USD; không kết
luận): 5 cấu hình chạy hết không lỗi — runtime; native + đếm MiniLM; DBSF w=0,3; bỏ dấu + NFC; exact + pool 100.
`compare` chạy (2 biến thể → có Holm). **Kiểm đúng đường:** top-10 và MRR/nDCG/Coverage của cấu hình runtime và
native **trùng từng câu** với mốc `retrieval_dense_bm25_rrf_1.jsonl` và `retrieval_native_hybrid_rrf_b13.jsonl`.

**Trước khi đo thật (chờ A):** (1) A duyệt mục 0–1; (2) A áp m1–m8 (B14) vào file đoạn đúng — harness đọc
`data/phase_8_1/gold/gold_draft.jsonl` (đổi `GOLD_PATH` nếu A khóa sang tên khác); (3) chạy lại 2 mốc byte (mục 0).
G1.6 hai tầng cuối (model dùng fact, trích đúng) cần judge Claude trên câu trả lời 7B — làm sau, harness hiện tính 4
tầng đầu.

## 4. A duyệt + bổ sung (ghi TRƯỚC khi đo)

A duyệt mục 0–1 (tin nhắn A), kèm 3 bổ sung, ghi lúc 21:42 +0700 (chưa chạy lượt đo thật nào):

1. **Độ tự nhiên của câu (User 21:40):** nhãn `natural` / `capability_only` / `unnatural` cho 176 câu, do sub-agent
   gắn độc lập, không thấy kết quả G1 (`data/phase_8_1/golden_realism.jsonl`). Mọi bảng G1 báo thêm theo nhãn
   này; khi đã có nhãn, **phần `natural` là số chính cho kết luận**, số trên toàn bộ dev là số phụ. Harness đọc
   nhãn lúc phân tích (`compare`/`table --realism`), không cần chạy lại retrieval khi nhãn đến sau.
2. **Đoạn đúng:** `data/phase_8_1/gold/gold_draft.jsonl` đã áp m1–m8 (validator 55/0) = bản khóa cho G1
   (SHA-256 lúc đo ghi trong report kết quả).
3. **Holm G1.3 trên toàn nhóm 10 biến thể**: native p30, native p100, `dense_bm25_rrf` k ∈ {2, 10, 30} (3),
   native p30 k ∈ {2, 10, 30} (3), DBSF w ∈ {0,2; 0,3} (2) — với từng metric chính (`top10_gold_all`, `mrr`).
