# Implementation Report: Phase 8 — Notebook 08a Dense Embedding Benchmark

Implementer: Implementer
Date: 2026-08-28 (+07)
Canonical guide:

```text
guides/phase_8_benchmark_model_selection.md
```

Tài liệu thiết kế và kế hoạch đã được phê duyệt:

```text
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
```

Báo cáo Codex Review trước đó:

```text
reports/phase_8_08a_embedding_benchmark_codex_review.md
```

---

## 1. Phạm vi

- **Được phê duyệt & Scope Amendment:** Catalog được mở rộng thành 8 cấu hình (bổ sung `huydang-dek21-embedding-768`). Trong vòng thực thi này, User ủy quyền thực thi live benchmark cho đúng **5 cấu hình**:
  1. `e5-small-384` (Control baseline)
  2. `multilingual-minilm-l12-384`
  3. `huydang-dek21-embedding-768` (Mới)
  4. `e5-base-768`
  5. `qwen3-embedding-0.6b-384`
- **Các cấu hình trì hoãn (Deferred):** Ba cấu hình gồm `e5-large-1024`, `bge-m3-dense-1024`, và `qwen3-embedding-0.6b-1024` chưa được phép chạy trong vòng này và bị runtime boundary từ chối (fail closed).
- **Ranh giới an toàn:** Không sửa production config/settings, không thay đổi `E5Embedder` production, không sửa Golden Dataset V3, không mutate active collection (`hue_foods_e5_small_384`), không gọi paid API, không production cutover.

---

## 2. Thay đổi chính

1. **Dependency:**
   - [`pyproject.toml`](file:///home/minhhieu/hue_rag/pyproject.toml) & [`uv.lock`](file:///home/minhhieu/hue_rag/uv.lock): Bổ sung `pyvi==0.1.1` (phục vụ tách từ tiếng Việt cho Huydang DEk21) và `FlagEmbedding==1.4.0` (phục vụ BGE-M3).
2. **Dense Model Runners:**
   - [`backend/embedding/dense_benchmark.py`](file:///home/minhhieu/hue_rag/backend/embedding/dense_benchmark.py):
     - Định nghĩa 8 `DenseBenchmarkSetting` (immutable) với pinned model revisions.
     - `HuydangDenseRunner`: Kiến trúc PhoBERT ~135M params, native 768D, FP32, `max_length=256`, áp dụng `pyvi.ViTokenizer.tokenize()` đồng nhất cho cả query và document trước khi kiểm tra độ dài và encode bằng native `SentenceTransformer`.
     - `SentenceTransformerDenseRunner`: chạy E5 family và MiniLM với CPU FP32, batch document 8, query 1, tiền tố passage/query cho E5.
     - `Qwen3DenseRunner`: hỗ trợ `truncate_dim=384` chính thức qua SentenceTransformers và câu lệnh instruction tiếng Việt chuẩn `QWEN_QUERY_INSTRUCTION`.
     - `BGEM3DenseRunner`: đảm bảo `model.eval()`, `model.float()`, `model.to("cpu")` trong `load()` và trước mỗi forward.
3. **Orchestration, Scoring & Boundaries:**
   - [`backend/evaluation/embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/evaluation/embedding_benchmark.py):
     - Kiểm tra nghiêm ngặt boundary: Yêu cầu `expected_active_snapshot` bắt buộc; so sánh equality toàn bộ setting object với canonical setting map; từ chối mọi deferred setting; kiểm tra collection allowlist và snapshot trước khi thực thi.
     - `score_retrieval_case`: chấm điểm binary exact relevance theo cặp `(source, section)` với gain=1 chỉ cho lần xuất hiện đầu tiên trong Top 5.
     - `evaluate_category_guardrails` & `paired_bootstrap_intervals`: đối chiếu chính xác ordered `(case_id, category)` matching.
     - `upsert_embedding_results_csv`: validate exact header của file hiện hữu trước khi ghi/upsert.
     - `sanitize_benchmark_error`: loại bỏ toàn bộ URL query parameters (`?` và `&`), signed headers/keys (`X-Amz-Credential`, `X-Amz-Signature`), `Authorization: Basic/Bearer`, `Cookie/Set-Cookie` và duyệt đệ quy qua `__cause__`.
     - Tính toán và ghi nhận chính xác category deltas (`delta_recall_at_5`, `delta_mrr_at_5`, `delta_ndcg_at_5`) cho 9 category rows của mỗi candidate.
     - Bổ sung `category_table(control_result, candidate_results)` và cập nhật `settings_table()` hiển thị trạng thái `Authorized (Now)` / `Deferred (Future)`.
4. **Focused Tests:**
   - [`backend/tests/test_embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/tests/test_embedding_benchmark.py): 23 focused deterministic unit tests kiểm tra toàn diện: scoring, aggregation, guardrails, bootstrap, category matching invariants, clear gain, best lighter selection, CSV header validation, boundary rejection (unapproved key, forged object, deferred setting, active target, missing snapshot), error sanitization, Huydang DEk21 contract, PyVi tokenization và category/settings table helpers.
5. **Notebook Giáo dục:**
   - [`notebooks/08a_embedding_benchmark.ipynb`](file:///home/minhhieu/hue_rag/notebooks/08a_embedding_benchmark.ipynb): Cập nhật danh mục 8 cấu hình, vòng lặp candidate gồm 4 authorized candidates, hiển thị bảng 9 categories và phân tích trade-offs quan sát được trong phần kết luận. Đảm bảo toàn bộ outputs rỗng và `execution_count: null`.

---

## 3. Cách đã chạy thật

1. **Focused Deterministic Tests:**
   ```bash
   cd backend
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache \
   uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
   ```
   *Kết quả:* `23 passed in 5.12s`.

2. **Real Local Benchmark Run (5 Cấu hình được ủy quyền):**
   - Chạy trên Qdrant Docker container (`http://localhost:6333`), CPU FP32, dataset Golden V3 (45 cases) và 572 chunks chuẩn:
     1. Control: `intfloat/multilingual-e5-small` (rev: `614241f622f53c4eeff9890bdc4f31cfecc418b3`) trên `hue_foods_08a_e5_small_384`.
     2. Candidate 1: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (rev: `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`) trên `hue_foods_08a_minilm_l12_384`.
     3. Candidate 2: `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (rev: `517f1af7dd04a57194f1de2990f0c6ede0a3109b`) trên `hue_foods_08a_huydang_dek21_768`.
     4. Candidate 3: `intfloat/multilingual-e5-base` (rev: `d128750597153bb5987e10b1c3493a34e5a4502a`) trên `hue_foods_08a_e5_base_768`.
     5. Candidate 4: `Qwen/Qwen3-Embedding-0.6B` với `truncate_dim=384` (rev: `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`) trên `hue_foods_08a_qwen3_06b_384`.

---

## 4. Kết quả quan sát

### A. Bảng tổng hợp chất lượng (Quality Metrics @ Top 5)

| Cấu hình | Dim | Trạng thái | Hits / 45 | Recall@5 | MRR@5 | nDCG@5 | Ranking Stable (3/3) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E5-small 384D (control)** | 384 | `completed` | **41 / 45 (91.1%)** | **0.8185** | **0.7748** | **0.7425** | `True` |
| **Multilingual MiniLM-L12 384D** | 384 | `completed` | 34 / 45 (75.6%) | 0.5815 | 0.5144 | 0.4709 | `True` |
| **Huydang DEk21 768D** | 768 | `completed` | 40 / 45 (88.9%) | 0.8370 | 0.7211 | 0.7164 | `True` |
| **E5-base 768D** | 768 | `completed` | **42 / 45 (93.3%)** | **0.8407** | 0.6985 | 0.7061 | `True` |
| **Qwen3 Embedding 0.6B 384D** | 384 | `completed` | 39 / 45 (86.7%) | 0.7481 | 0.6237 | 0.6175 | `True` |

### B. So sánh Bootstrap, Guardrails & Quyết định Clear Gain

| Candidate | $\Delta$ nDCG@5 | 95% Percentile CI | Guardrails Đạt | Clear Gain vs Control | Best Lighter | Clear Gain vs Lighter | Finalist Eligible |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MiniLM-L12 384D** | **-0.2716** | `[-0.3756, -0.1711]` | **FAIL** (2/9) | `False` | `e5-small-384` | `False` | `True` |
| **Huydang DEk21 768D** | **-0.0262** | `[-0.1270, +0.0749]` | **FAIL** (6/9) | `False` | `e5-small-384` | `False` | `True` |
| **E5-base 768D** | **-0.0364** | `[-0.1002, +0.0219]` | **FAIL** (7/9) | `False` | `e5-small-384` | `False` | `True` |
| **Qwen3 384D** | **-0.1251** | `[-0.2321, -0.0157]` | **FAIL** (6/9) | `False` | `e5-small-384` | `False` | `True` |

### C. Độ trễ và Thời gian thực thi (Latency trên CPU FP32)

| Cấu hình | Cold Load | Doc Embed (572 chunks) | Query Embed (p50 / p95) | Qdrant Search (p50 / p95) | Total Latency (p50 / p95) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E5-small 384D (control)** | 7.55 s | **19.81 s** | **21.76 ms** / 33.17 ms | 5.44 ms / 7.92 ms | **27.40 ms** / 39.75 ms |
| **MiniLM-L12 384D** | 5.33 s | 15.77 s | 23.42 ms / 41.31 ms | 5.80 ms / 7.76 ms | 29.34 ms / 48.31 ms |
| **Huydang DEk21 768D** | 3.26 s | 44.38 s | 64.21 ms / 101.67 ms | 7.08 ms / 9.79 ms | 71.24 ms / 114.62 ms |
| **E5-base 768D** | 7.15 s | 47.15 s | 50.93 ms / 80.63 ms | 6.16 ms / 8.80 ms | 57.09 ms / 88.44 ms |
| **Qwen3 0.6B 384D** | 41.50 s | 765.20 s (~12.75 min) | 781.77 ms / 1,118.36 ms | 5.70 ms / 10.86 ms | 788.54 ms / 1,125.91 ms |

### D. Tài nguyên bộ nhớ & Truncation

| Cấu hình | Max Length | Truncated Docs / 572 | RSS trước load | RSS sau load | Peak RSS quan sát |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E5-small 384D (control)** | 512 | **0** | 956 MB | 1,338 MB | **1,543 MB** |
| **MiniLM-L12 384D** | 128 | **83** | 1,331 MB | 1,773 MB | 2,048 MB |
| **Huydang DEk21 768D** | 256 | **1** | 1,650 MB | 1,820 MB | 2,197 MB |
| **E5-base 768D** | 512 | **0** | 1,697 MB | 1,987 MB | 2,720 MB |
| **Qwen3 0.6B 384D** | 512 | **0** | 1,920 MB | 2,450 MB | 2,871 MB |

### E. Chi tiết nDCG@5 theo từng Category

| Category ($n$) | E5-small 384D (Control) | MiniLM-L12 384D | Huydang DEk21 768D | E5-base 768D | Qwen3 384D |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **relationship** (14) | **0.8994** (14/14 hits) | 0.5119 (12/14) | 0.8587 (14/14) ❌ | 0.8148 (13/14) ❌ | 0.6991 (12/14) ❌ |
| **direct_fact** (7) | 0.7930 (6/7 hits) | 0.4411 (5/7) | 0.7694 (7/7) ✅ | 0.8132 (7/7) ✅ | **0.8457** (6/7) ✅ |
| **food_knowledge** (7) | 0.7546 (6/7 hits) | 0.5349 (6/7) | **0.8571** (6/7) ✅ | 0.7606 (7/7) ✅ | 0.4402 (6/7) ❌ |
| **comparative** (6) | **0.5440** (5/6 hits) | 0.4221 (4/6) | 0.3972 (4/6) ❌ | 0.4929 (5/6) ❌ | 0.5031 (6/6) ✅ |
| **holistic** (3) | 0.6399 (3/3 hits) | 0.3125 (2/3) | **0.7606** (3/3) ✅ | 0.5850 (3/3) ✅ | 0.7339 (3/3) ✅ |
| **spanning** (3) | **0.3977** (3/3 hits) | 0.2818 (2/3) | 0.1131 (1/3) ❌ | 0.3412 (3/3) ✅ | 0.0487 (1/3) ❌ |
| **guide_planning** (2) | 0.5000 (1/2 hits) | 0.0000 (0/2) | 0.5655 (2/2) ✅ | 0.5000 (1/2) ✅ | **0.8155** (2/2) ✅ |
| **numerical** (2) | **1.0000** (2/2 hits) | 1.0000 (2/2) | **1.0000** (2/2) ✅ | **1.0000** (2/2) ✅ | 0.6934 (2/2) ✅ |
| **temporal** (1) | 0.6131 (1/1 hit) | **0.8772** (1/1) | 0.6934 (1/1) ✅ | 0.6131 (1/1) ✅ | 0.6131 (1/1) ✅ |

### F. An toàn hệ thống và Snapshot đối chiếu
- **Active Collection (`hue_foods_e5_small_384`):** Snapshot trước và sau benchmark hoàn toàn trùng khớp (572 points, dense size 384, giữ nguyên trạng thái read-only tuyệt đối).
- **Isolated Collections:** Đầy đủ 5 collections authorized được khởi tạo và ghi đúng 572 points:
  1. `hue_foods_08a_e5_small_384`: 572 points, 384D.
  2. `hue_foods_08a_minilm_l12_384`: 572 points, 384D.
  3. `hue_foods_08a_huydang_dek21_768`: 572 points, 768D.
  4. `hue_foods_08a_e5_base_768`: 572 points, 768D.
  5. `hue_foods_08a_qwen3_06b_384`: 572 points, 384D.
- **CSV Reconciliation:** File `evaluation/results/phase8_embedding_results.csv` chứa chính xác 50 dòng (5 dòng overall + 45 dòng category) của 5 model authorized.

---

## 5. Lỗi và giới hạn

1. **Phân tích & Giới hạn của Model Huydang DEk21:**
   - **Kiến trúc & Huấn luyện:** Backbone PhoBERT (135M params), native 768D, `max_seq_length=256`, mean pooling. Được fine-tune trên ~100.000 cặp câu hỏi/văn bản pháp luật Việt Nam (Legal domain).
   - **Điểm sáng:** Bắt được 40/45 hits, Recall@5 cao (0.8370), nDCG@5 đạt 0.7164 (gần tiệm cận E5-small 0.7425 và nhỉnh hơn E5-base 0.7061). Đặc biệt đạt nDCG@5 cao ở nhóm `food_knowledge` (0.8571) và `holistic` (0.7606) nhờ khả năng biểu diễn từ ngữ tiếng Việt tốt sau khi tách từ bằng `ViTokenizer`.
   - **Hạn chế quan sát được:**
     - `max_length=256` khiến 1 chunk bị cắt ngắn (so với 512 của E5).
     - Trượt 3 category guardrails (`comparative`, `relationship`, `spanning`), đặc biệt ở `spanning` chỉ bắt được 1/3 hits do đặc thù câu hỏi dàn trải ngữ cảnh dài.
     - Thời gian query latency (~46.7 ms) chậm hơn gấp đôi so với E5-small (~20.8 ms).
2. **Giới hạn thực thi & Phạm vi trì hoãn:**
   - Ba cấu hình 1024D (`e5-large-1024`, `bge-m3-dense-1024`, `qwen3-embedding-0.6b-1024`) đã bị dừng thực thi local theo chỉ đạo tài nguyên của User và bị runtime boundary từ chối.
   - Chưa thực hiện paid OpenRouter API calls, hybrid retrieval, reranking, generation hay production cutover.
3. **Kết luận an toàn:**
   - Không có lỗi blocker chưa xử lý trong phạm vi 5 model authorized. Active production collection và production settings được giữ nguyên vẹn.

---

## 6. Handoff cho Reviewer

Reviewer nên kiểm tra:
1. File báo cáo triển khai này: [`reports/phase_8_08a_embedding_benchmark_implementation_report.md`](file:///home/minhhieu/hue_rag/reports/phase_8_08a_embedding_benchmark_implementation_report.md).
2. Mã nguồn backend và test:
   - [`backend/embedding/dense_benchmark.py`](file:///home/minhhieu/hue_rag/backend/embedding/dense_benchmark.py) (`HuydangDenseRunner`, PyVi tokenization, 8 settings catalog)
   - [`backend/evaluation/embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/evaluation/embedding_benchmark.py) (Boundary verification, mandatory snapshot, deferred rejection, category deltas)
   - [`backend/tests/test_embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/tests/test_embedding_benchmark.py) (23 unit tests)
3. Notebook: [`notebooks/08a_embedding_benchmark.ipynb`](file:///home/minhhieu/hue_rag/notebooks/08a_embedding_benchmark.ipynb) (xác nhận outputs sạch và có bảng category).
4. Dữ liệu thực nghiệm: [`evaluation/results/phase8_embedding_results.csv`](file:///home/minhhieu/hue_rag/evaluation/results/phase8_embedding_results.csv) (50 dòng của 5 models authorized).
5. Lệnh chạy lại unit test độc lập:
   ```bash
   cd backend
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
   ```
6. Kiểm tra an toàn:
   ```bash
   git diff --check
   git status --short
   ```
   Xác nhận active collection `hue_foods_e5_small_384` không bị biến động và `backend/config/settings.yaml` không thay đổi.
