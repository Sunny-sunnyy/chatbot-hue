# Phase 8.1 — Rà quyết định Phase 0–7 và thí nghiệm so với baseline

**Status:** `approved` — User duyệt 20:49 24/10/2026 (bản 4, gồm M1 + M2) · Ngày: 24/10/2026 (v1 20:20; v2/v3 sau review C15/C15b) · Người viết: A · Đợt:
`report_agent/2026-10-24_phase_8_1_ra_soat/`

## 1. Mục tiêu

Các quyết định kỹ thuật của Phase 0–7 phần lớn do AGY/Codex chọn; bảng rà C11 cho thấy chỉ 2/56 từng
được so trên toàn kho, 29 chưa từng so, 16 mặc định không lý do. 8.1 trả lời bằng số đo: **lựa chọn
nào đang kéo chất lượng xuống, phương án nào thắng baseline, và thắng bao nhiêu**.

8.1 **không đổi chatbot đang chạy** (config runtime, collection runtime, prompt runtime, corpus,
Golden chính thức giữ nguyên). Kết quả là một báo cáo xếp hạng để User đóng 8.1; rồi A mới thiết kế 8.2
(áp dụng phương án thắng).

## 2. Quyết định đã chốt (User 24/10 tối)

| # | Quyết định | Cái giá |
|---|---|---|
| D1 | Phase 8 tách 8.1 (đo, rà, thử) → 8.2 (cải tiến) | Thêm một vòng duyệt; cải tiến thấy được muộn hơn |
| D2 | Rà toàn bộ Phase 0–7, gồm Golden và bộ chấm | Thêm việc sửa thước đo trước khi thử |
| D3 | Model/thư viện mới: liệt kê trong spec (mục 7), User duyệt từng dòng | Dòng bị gạch thì hướng đó chỉ đề xuất trên giấy |
| D4 | Paid nhỏ trong trần 1 USD/phiên; index Qwen3-8B để 8.2 | — |
| D5 | Bộ chấm: chia 176 câu thành **120 thử / 56 kiểm** (phân tầng 5 loại); thêm **30–40 câu mới** kiểu người dùng thật, giữ kín tới cuối 8.2 | User duyệt mẫu câu mới ~20–30 phút |
| D6 | "Đoạn đúng" cho ~40 câu khó: agent gắn, agent khác kiểm chéo, User duyệt ~10 câu. *A mở rộng (C15 M2): ~40 thử + ~15 kiểm; công User không đổi* | Điểm câu trả lời chưa có mốc người (nhắc lại trước quyết định 8.2 dựa vào điểm câu trả lời) |
| D7 | **Giữ `gpt-6-luna`**, không so model sinh; tối ưu sang model nhỏ để sau khi hệ thống ổn. Cam kết "so Qwen ở Phase 8" (amendment 2026-10-01 §5) hoãn theo D7 | Không biết model khác có tốt hơn không |
| D8 | Thư viện không còn dùng giữ nguyên, chỉ gỡ khi xung đột; code luôn `uv` trong `.venv` dự án | — |
| D9 | Nghiên cứu ngoài qua ChatGPT trước (prompt deep research đầy đủ), kiểm URL bằng WebFetch | — |
| D10 | Dense chỉ **e5-small** (đang chạy) và **Qwen3-Embedding-8B** OpenRouter (spec 7A2 §2); 8B để 8.2. Không thử dense khác ở 8.1 | Không biết model dense khác có hơn không |
| D12 | Thêm **rerank listwise bằng `gpt-6-luna`** (kiểu `rag_old_0/pro_implementation`: đưa danh sách đoạn, model trả thứ tự id) so cùng rerank GPU — phương án không cần GPU cho kịch bản deploy AWS | ~0,05–0,1 USD/lượt 120 câu (ước), +1–3 s/câu (ước) |
| D11 | Rerank chạy **GPU GTX 1650 4 GB, fp32** (torch 2.13+cu130 đã có trong `.venv`, `cuda.is_available()` = True — không thêm dependency). Chatbot hiện chạy trên máy User; sau có thể deploy AWS (chưa chắc) ⇒ đo thêm latency CPU trên 5–10 câu | Rerank chỉ dùng được thật khi máy chạy có GPU hoặc đủ nhanh trên CPU |

## 3. Quyết định kỹ thuật của A (trong phạm vi, kèm lý do)

1. **Chạy thí nghiệm bằng harness riêng**, không qua runtime: script trong `backend/experiments/phase_8_1/`
   gọi các hàm production (`chunk_full_corpus`, retrieval, context builder, generator). Lý do: loader ép
   cứng tổ hợp runtime (`settings_loader.py:39-44`, C11 X.1); đổi loader là đổi contract runtime, không
   thuộc 8.1. Không sửa `settings.yaml`/`settings_loader.py`.
   **Một luật cho code production (C15 M1):** hiện prompt/model settings gắn cứng trong generator
   (`generator_openai_full_corpus.py:117-126`), pool 30 / RRF k=60 là hằng (`retrieval/full_corpus.py:465,561,608`),
   build ánh xạ cứng collection runtime + sparse state chung ghi một lần (`full_corpus_pipeline.py:55,66-69,125-131`).
   8.1 được thêm **tham số keyword, mặc định = giá trị hiện tại**, đúng ở các chỗ đó: generator
   (instructions, reasoning effort); retrieval (pool, RRF k, `exact`/search params cho `query_points`
   `full_corpus.py:461-476`; tên collection + build record + đường sparse state mà
   `build_full_corpus_retrieval_service` đang lấy cố định `full_corpus.py:723-750`); build (tên collection,
   đường sparse state, danh sách tokenizer kiểm giới hạn).
   **Logic chia đoạn mới** (nhóm dòng bảng, gộp khối, heading lá, tiền tố) nằm **trong harness**: harness xử
   lý tiếp danh sách chunk do `chunk_full_corpus` trả về (gộp `evidence_parts`, dựng lại `search_text`);
   chunker production không đổi (C15b r2). Không đổi giá trị mặc định, không thêm cấu hình vào `settings.yaml`. Gate G0.6
   kiểm runtime không đổi.
2. **Mỗi biến thể index một collection riêng** tên `hue_81_<biến_thể>` + build record riêng trong
   `data/phase_8_1/builds/`; harness từ chối chạy nếu record không khớp cấu hình chunker của biến thể.
   Lý do: kiểm tươi runtime không biết khi chunker đổi (C11 4.3) → nguy cơ đo nhầm index cũ.
3. **Đoạn đúng gắn theo vị trí trong file nguồn** (source + khoảng ký tự), không theo `chunk_id`, để dùng
   chung cho mọi biến thể chunker (nghiên cứu §14).
4. **So sánh theo cặp trên cùng câu:** paired bootstrap 10.000 lần (CI 95% của chênh trung bình); báo
   thắng/hòa/thua, theo từng loại câu; khi >1 biến thể "thắng" cùng một câu hỏi nghiên cứu thì hiệu chỉnh
   Holm. Không thêm permutation test (một phép là đủ, C15 m5). "Không khác" = CI chứa 0. **Chọn trên 120 câu thử, xác nhận trên 56 câu kiểm**; 30–40 câu kín chỉ mở cuối 8.2.
5. **Judge chính là Claude** (sub-agent Claude Code, ghi model id dùng); không judge phụ `gpt-6-luna` để
   tiết kiệm, trừ khi một kết luận phụ thuộc judge. Biến thể và baseline phải chấm **cùng model judge**;
   model judge đổi thì chấm lại baseline. Chấm dùng quota Claude Code (không USD), mỗi lượt 120 câu ~12 lô.
6. **Ghi trước tiêu chí** cho từng thí nghiệm (file YAML theo khuôn nghiên cứu §IV) trước khi chạy; kết
   quả âm giữ nguyên.

## 4. Phạm vi

**Trong:** sửa/thêm code evaluator và harness thí nghiệm; thêm tham số mặc định-như-cũ (mục 3.1) vào
`backend/llm/generator_openai_full_corpus.py`, `backend/retrieval/full_corpus.py`,
`backend/ingestion/full_corpus_pipeline.py` (và chunker nếu cần cấu hình tokenizer); tạo file chia bộ câu hỏi, file đoạn đúng, bộ
câu mới (private, trong `knowledge-base-hue/evaluation/phase_8_1/`); tạo/xóa collection `hue_81_*`; paid
`gpt-6-luna` trong trần mục 8; báo cáo.

**Ngoài (NOT RUN trong 8.1, có lý do):** Representation B / contextual retrieval (H10, ~8.459 call ≈ 0,6 USD >
trần); tinh chỉnh BM25 k1/b (tác động thấp, C11 3.8); MMR/giới hạn mỗi tài liệu (H12); tách câu hỏi bằng LLM
(H13) và viết lại câu hỏi bằng LLM (`rag_old_0` pro) — thêm một lượt gọi model mỗi câu, sát Phase 9. **Ngoài phạm vi:** sửa runtime (config, loader, prompt, collection đang chạy, API/UI); sửa corpus curated; sửa
`golden_full_corpus*.jsonl`; model sinh khác; dense model khác e5-small (D10); index Qwen3-8B; gỡ dependency; Agentic RAG (Phase 9).

## 5. Các bước (gate)

Mỗi gate: người làm → report → người kia review chéo → A đóng gate (User đóng 8.1 ở cuối).

### G0 — Sửa thước đo và khóa baseline (free; công User ~45–75 phút)

1. File chia 120/56 phân tầng theo `category`, seed cố định, đóng băng (private).
2. Evaluator: paired bootstrap trong `compare`; tự kiểm hai chiều: **đối chứng âm** Run 1 vs Run 2 của 7B
   phải ra "không khác" (CI chứa 0 ở mọi metric), **đối chứng dương** retrieval baseline vs cùng kết quả
   nhưng xáo thứ tự top-10 (free, seed cố định ghi trong report) phải ra "kém hơn" ở MRR/nDCG; macro theo loại câu; bảng từ chối 2×2 (từ chối đúng/nhầm); metric "bằng chứng trong
   5 đoạn đưa model" (dùng `context-coverage` có sẵn).
3. Đoạn đúng cho câu khó ở **cả hai nhóm** (C15 M2): ~40 trong 120 câu thử + ~15 trong 56 câu kiểm (22 câu
   từ chối nhầm + câu nhiều nguồn/so sánh/giá vé), để metric theo đoạn đúng cũng xác nhận được trên nhóm kiểm: agent đề xuất từ union dense100 + BM25 100 + cả file nguồn → agent khác kiểm chéo → User duyệt
   ~10 câu. Ghi `required_facts`, `is_answerable`, `ambiguity`.
4. 30–40 câu mới giữ kín: một sub-agent **mới** chỉ nhận corpus + hướng dẫn soạn (văn nói, không dấu, gõ
   sai nhẹ, đủ 5 loại), không thấy kết quả thí nghiệm; kiểm máy như 7A; User duyệt mẫu; khóa kín.
5. **Tham số mặc định-như-cũ** (mục 3.1): sau khi thêm, pytest full-corpus đạt + retrieval runtime 176 câu
   giống từng byte mốc 7B + review chéo, rồi mới sang G1.
6. Baseline freeze: commit, hash corpus, build record, retrieval 176 câu, 176 câu trả lời 7B Run 1,
   điểm Claude — chạy lại retrieval phải giống từng byte mốc 7B.

### G1 — Chẩn đoán chỉ đọc trên index hiện tại (free)

1. Candidate recall dense / BM25 / hợp hai nhánh ở pool 30/100/200 (đoạn đúng + keyword).
2. Dense HNSW vs `exact=true`: trùng top-k, latency.
3. Hybrid độc lập (`native_hybrid_rrf`, pool 30/100) vs runtime `dense_bm25_rrf` (từ khóa chỉ xếp lại tập
   dense đã chọn); RRF k ∈ {2,10,30,60}; DBSF với từ khóa 20/30%. Tiêu chí ghi trước gồm **0 câu mất đoạn
   đúng khỏi top-10** (đo trên ~55 câu có đoạn đúng; câu còn lại dùng keyword-hit). Lý do: bài học từ một dự án
   RAG khác của User (ghi chú private, mục 10) là cho từ khóa *chọn* ứng viên dễ kéo lên đoạn lặp từ phổ biến
   và làm mất đáp án, còn "chỉ xếp lại" (như runtime) an toàn — trái khuyến nghị nghiên cứu ChatGPT, nên phải
   đo, không suy.
4. Câu hỏi dạng NFD / không dấu / kiểu dấu cũ: bản biến đổi của 120 câu, có và không có NFC ở query.
5. Tỉ lệ cặp vượt 512 token của MiniLM (luật "bỏ rerank cả request").
6. Nhãn tầng lỗi cho ~55 câu có đoạn đúng: có trong kho → trong pool → top-10 → 5 đoạn → model dùng → trích
   đúng (7 checkpoint, nghiên cứu §1).

### G2 — Sinh câu trả lời, retrieval giữ cố định (paid nhỏ)

1. Context 5 vs 10, thứ tự theo hạng vs theo tài liệu.
2. Prompt: baseline vs "trả lời phần có căn cứ, nói rõ phần thiếu" vs baseline + 2 luật thiếu của spec
   Phase 6 §10. Đo từ chối nhầm, giữ 18/18 từ chối đúng, Completeness, lỗi citation, claim không nguồn
   (~55 câu có đoạn đúng).
3. Phát lại chính sách validator citation trên câu trả lời đã lưu (free).
4. (Tùy chọn) `reasoning.effort` low/high vs mặc định `medium` — chỉ trong harness; chạy thử 10 câu trước
   để đo token/USD thật (high có thể tốn hơn nhiều), rồi mới chạy 120 câu nếu vẫn trong trần.

### G3 — Biến thể chia đoạn (build e5 local, free; câu trả lời paid nhỏ cho biến thể thắng)

Lần lượt, mỗi bước so với baseline và biến thể trước: H1 chỉ kiểm tokenizer e5-small 512 → H3 nhóm dòng
bảng → H2 gộp khối cùng heading tới 128/256/384 token (+ biến thể "1 heading lá = 1 đoạn") → small-to-big
(mở rộng đoạn anh em sau khi tìm, không đổi index) → tiền tố tiêu đề (đầy đủ / chỉ heading gần nhất /
không). Kèm sửa nhỏ: loại inventory performing_arts, giữ code fence, 3 cặp đoạn lặp. So với ngân sách token
context cố định để tránh "đoạn to tự thắng keyword". Mỗi biến thể có sparse state riêng
(`data/phase_8_1/builds/<biến_thể>/`). Vì chunk × context tương tác (C15 m3): biến thể chunk thắng được chạy
lại context 5 vs 10 (2×2 nhỏ) trước khi kết luận.

### G4 — Hướng cần model/thư viện mới (chỉ dòng User duyệt ở mục 7)

**Từ khóa:** BM25 âm tiết + cặp âm tiết + nguyên cụm mã; tách từ `pyvi` (đã có
trong `pyproject.toml`, dùng ở `ingestion/preview.py:21` — không thêm thư viện). Đo với cách trộn thắng ở G1.

**Rerank (GPU fp32, D11):** model ở mục 7 (dòng User duyệt); **chỉ xếp lại thứ tự** top-10 đã chọn, không
được chọn đoạn ngoài tập; hai cách chấm: **đoạn trơn** vs **đoạn kèm mục chứa nó** (cùng `heading_path`, cắt
cùng mức cắt 1024 token cho mọi model để so công bằng) — giả thuyết: đơn vị chấm có ngữ cảnh rộng quan trọng
hơn chọn model (ghi chú private), và đoạn của mình rất ngắn (trung vị 85 token). Tiêu chí ghi trước: 0 câu mất
đoạn đúng khỏi **5 đoạn đưa model**; MRR@10 + đoạn đúng trong 5 đoạn đưa model tăng có CI; latency GPU p95 ≤ 3
s/câu (ước, chưa đo — đo 5–10 câu trước; "đoạn kèm mục" có thể vượt, khi đó ghi số thật để User cân nhắc); ghi latency CPU 5–10 câu cho kịch bản
deploy không GPU. **Rerank bằng `gpt-6-luna` (D12):** cùng 10 đoạn, structured output trả thứ tự id (đủ mọi id,
không thêm/bớt); chạy thử 10 câu để đo token/USD/latency thật trước 120 câu; cùng tiêu chí trên, latency ghi
riêng (gọi API). So ba nhánh trên cùng 120 câu: không rerank / GPU (M1, M2) / luna. Chỉ chạy sau khi G1 cho
thấy đoạn đúng đã nằm trong pool (reranker không cứu đoạn ngoài
pool).

### G5 — Tổng hợp

Báo cáo xếp hạng: mỗi quyết định C11 → giữ / thay bằng X (chênh, CI, câu kiểm xác nhận) / chưa rõ; đề
xuất phạm vi 8.2; **danh sách khâu còn dính** (hằng số ẩn, đường dẫn cứng, đọc settings sâu — skill
`practical-project-coding` mục "Ranh giới theo khâu pipeline", User 24/10) để 8.2 tách gọn. Cập nhật `bao_cao_he_thong/` (4 chỗ) và `TONG_HOP.md`; User đóng 8.1.

**Điều kiện dừng sớm:** nếu G1 cho thấy đoạn đúng nằm ngoài hợp hai nhánh @200 ở phần lớn câu lỗi → dừng
tối ưu fusion/reranker, chuyển thẳng sang G3. Nếu G0.2 tự kiểm Run 1 vs Run 2 báo "khác" → dừng, sửa
thước đo trước.

## 6. Tiêu chí nghiệm thu 8.1

1. G0 xong: tự kiểm thống kê (đối chứng âm + dương) đạt; tham số mặc định-như-cũ không đổi runtime (byte); baseline tái lập byte; file chia, đoạn đúng, câu kín tồn tại và được
   duyệt như D5/D6.
2. Mỗi thí nghiệm có tiêu chí ghi trước, kết quả theo cặp (chênh, CI, thắng/hòa/thua, theo loại câu), và
   kết luận tốt hơn / không đổi / kém hơn / chưa rõ; phương án "tốt hơn" đã xác nhận trên 56 câu kiểm.
3. Mỗi dòng trong top 10 của C11 có kết luận hoặc lý do NOT RUN.
4. Runtime không đổi: retrieval 176 câu của runtime vẫn giống từng byte mốc 7B ở cuối 8.1; Qdrant chỉ còn
   collection runtime (mọi `hue_81_*` đã xóa, liệt kê trước/sau).
5. Tiền thật từ log ≤ trần mục 8; mỗi report ghi token + USD.

## 7. Model / thư viện mới — User duyệt từng dòng

| Dòng | Thứ | Để làm gì | Nặng / giấy phép | Chạy |
|---|---|---|---|---|
| M1 | `BAAI/bge-reranker-v2-m3` | xếp hạng lại đa ngôn ngữ thay MiniLM tiếng Anh (G4) | ~568M tham số, ~2,3 GB VRAM fp32; Apache-2.0; huấn luyện max 1024 token | GPU local (fp32 — fp16 trên dòng card này có thể chậm hơn; đo lại) |
| M2 | `AITeamVN/Vietnamese_Reranker` | reranker huấn luyện cho tiếng Việt (fine-tune từ bge-reranker-v2-m3) | ~0,6B F32 (≈2,4 GB), max length 2304; Apache-2.0 (model card, C kiểm WebFetch) | GPU local |

Hai dòng chạy lần lượt (không cùng lúc trên 4 GB). Không cần duyệt (đã có): `pyvi`; torch CUDA trong `.venv`.
Không thử dense khác (D10).

Không có dòng nào gửi dữ liệu ra ngoài. Dòng bị gạch → hướng đó ghi "đề xuất, NOT RUN".

## 8. Quyền và giới hạn

- Qdrant: tạo/ghi/xóa **chỉ** collection tên bắt đầu `hue_81_`; collection runtime chỉ đọc.
- Paid: chỉ `gpt-6-luna` (giá 0,1 / 0,5 USD mỗi 1M token vào/ra). Trần **0,5 USD cho cả 8.1** (ước dùng
  ~0,2–0,3: mỗi lượt 120 câu ~0,016 USD, 176 câu ~0,024 USD), trong trần 1 USD/phiên; vượt thì dừng hỏi.
- Ghi file private: `knowledge-base-hue/evaluation/phase_8_1/` (file mới; không sửa Golden chính thức),
  `data/phase_8_1/`.
- B/C không commit; A commit theo gate. Sub-agent được dùng, kế thừa phạm vi này.

## 9. Rủi ro và cách giảm

| Rủi ro | Giảm |
|---|---|
| Tối ưu khớp 120 câu thử (overfit) | Xác nhận trên 56 câu kiểm; câu kín mở cuối 8.2 |
| Đo nhầm index cũ | Collection + build record riêng mỗi biến thể; harness kiểm khớp cấu hình |
| Đoạn đúng do agent gắn sai | Agent kiểm chéo + User duyệt mẫu; ghi "nhãn agent, người duyệt mẫu" |
| 56 câu kiểm không kín thật (đã bị phân tích ở B4/B5/C1/C11) | Ghi giới hạn này trong mọi kết luận; câu kín 30–40 mới là phép kiểm cuối |
| Judge Claude sai nhất quán | Ghi giới hạn; nhắc chấm tay 20 câu trước quyết định 8.2 dựa vào điểm câu trả lời |
| Đoạn to làm keyword metric tăng giả | Đo theo đoạn đúng + ngân sách token context cố định |
| 8.1 phình to | Điều kiện dừng sớm (mục 5); mỗi gate review chéo; NOT RUN được phép nếu có lý do |

## 10. Nguồn

- Bảng rà: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` (C11)
- Kiểm URL nghiên cứu: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_research_url_check.md` (C14)
- Bài học từ dự án khác của User (private, không commit): `data/phase_8_1/external_lessons_private.md` —
  đo trên dữ liệu khác hue_rag, chỉ dùng làm giả thuyết.
- Nghiên cứu (private): `gửi chatgpt/2026-10-24/kết quả nghiên cứu/phase_8_1_decision_audit_2026_10_24.md`,
  `phase_8_rag_retrieval_2026_10_24.md`, `phase_7b_rag_evaluation_2026_10_24.md`
- Giả thuyết: `reports/phase_8_candidate_hypotheses_2026_10_24.md`; baseline: spec 7B,
  `bao_cao_he_thong/BAO_CAO_DANH_GIA.md`
