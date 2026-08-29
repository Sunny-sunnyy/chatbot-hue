# Implementation Report: Phase 8 — Notebook 08a Dense Embedding Benchmark

Implementer: Implementer
Date: 2026-08-29 (+07)
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

- **Quyết định phạm vi hiệu chỉnh (User Directive 2026-08-29):** Đồng bộ mã nguồn, cấu hình, test, notebook và hạ tầng Qdrant về đúng **3 cấu hình dense embedding canonical**:
  1. `e5-small-384` (Control baseline, 384D)
  2. `huydang-dek21-embedding-768` (Candidate 1, 768D, PhoBERT + PyVi segmentation)
  3. `e5-base-768` (Candidate 2, 768D)
- **Loại bỏ triệt để MiniLM-L12 và các cấu hình không hiệu quả:**
  - Xóa bỏ `multilingual-minilm-l12-384` khỏi catalog runtime và candidate loop.
  - Xóa collection `hue_foods_08a_minilm_l12_384` khỏi Qdrant và xóa cache HuggingFace của model.
  - Đã loại bỏ code của Qwen3, BGE-M3, E5-Large và dependency `FlagEmbedding`.
- **Dữ liệu lịch sử & An toàn hệ thống:**
  - File CSV [`phase8_embedding_results.csv`](file:///home/minhhieu/hue_rag/evaluation/results/phase8_embedding_results.csv) lưu giữ đầy đủ bằng chứng thực nghiệm của các lần chạy (bao gồm cả MiniLM và Qwen làm negative baselines).
  - Active collection `hue_foods_e5_small_384` được giữ read-only tuyệt đối (572 points).
  - 3 isolated collections tương ứng trên Qdrant đều có đúng 572 points.

---

## 2. Thay đổi chính

1. **Dependency:**
   - [`pyproject.toml`](file:///home/minhhieu/hue_rag/pyproject.toml) & [`uv.lock`](file:///home/minhhieu/hue_rag/uv.lock): Giữ `pyvi==0.1.1` phục vụ tách từ tiếng Việt cho Huydang DEk21; không dùng `flagembedding`.
2. **Dense Model Runners:**
   - [`backend/embedding/dense_benchmark.py`](file:///home/minhhieu/hue_rag/backend/embedding/dense_benchmark.py):
     - Định nghĩa chính xác 3 `DenseBenchmarkSetting` (`E5_SMALL_SETTING`, `HUYDANG_DEK21_SETTING`, `E5_BASE_SETTING`).
     - `ALL_DENSE_SETTINGS` (3 settings) và `DENSE_CANDIDATE_SETTINGS` (2 candidates).
     - `RunnerKind = Literal["sentence_transformer", "huydang"]`, `InputContract = Literal["e5", "pyvi_segmented"]`.
     - `build_dense_runner` hỗ trợ `SentenceTransformerDenseRunner` và `HuydangDenseRunner`.
3. **Orchestration, Scoring & Boundaries:**
   - [`backend/evaluation/embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/evaluation/embedding_benchmark.py):
     - `CANONICAL_SETTINGS_MAP` và `APPROVED_COLLECTIONS` khóa chặt 3 cấu hình canonical.
     - Kiểm tra boundary nghiêm ngặt: yêu cầu bắt buộc `expected_active_snapshot`, so sánh object equality toàn phần (`setting == canonical`), kiểm tra collection nằm trong `APPROVED_COLLECTIONS` và khác active collection.
     - `settings_table()` hiển thị danh mục 3 cấu hình authorized.
4. **Focused Tests:**
   - [`backend/tests/test_embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/tests/test_embedding_benchmark.py): 23 focused deterministic unit tests kiểm tra toàn diện: scoring, aggregation, guardrails, bootstrap, clear gain, best lighter selection, CSV header validation & upsert, boundary rejection, error sanitizer, Huydang DEk21 contract & PyVi tokenization, settings table (3 cấu hình).
5. **Notebook Giáo dục:**
   - [`notebooks/08a_embedding_benchmark.ipynb`](file:///home/minhhieu/hue_rag/notebooks/08a_embedding_benchmark.ipynb): Cập nhật danh mục 3 cấu hình, cell candidate chạy 2 authorized candidates (`DENSE_CANDIDATE_SETTINGS`: Huydang và E5-base). Toàn bộ outputs rỗng và `execution_count: null`.

---

## 3. Cách đã chạy thật

1. **Focused Deterministic Tests:**
   ```bash
   cd backend
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-test-uv-cache \
   uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
   ```
   *Kết quả:* `23 passed in 4.87s`.

2. **Kiểm tra trạng thái Qdrant Live:**
   - Kiểm tra active collection và 3 isolated collections:
     - `hue_foods_e5_small_384`: 572 points (read-only, active baseline).
     - `hue_foods_08a_e5_small_384`: 572 points (Control 384D).
     - `hue_foods_08a_huydang_dek21_768`: 572 points (Candidate 768D).
     - `hue_foods_08a_e5_base_768`: 572 points (Candidate 768D).
   - Đã xác nhận xóa thành công `hue_foods_08a_minilm_l12_384` khỏi Qdrant.

---

## 4. Kết quả quan sát (3 Mô hình Hiện hành)

### A. Bảng tổng hợp chất lượng (Quality Metrics @ Top 5)

| Cấu hình | Dim | Trạng thái | Hits / 45 | Recall@5 | MRR@5 | nDCG@5 | Ranking Stable (3/3) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E5-small 384D (control)** | 384 | `completed` | **41 / 45 (91.1%)** | **0.8185** | **0.7748** | **0.7425** | `True` |
| **Huydang DEk21 768D** | 768 | `completed` | 40 / 45 (88.9%) | 0.8370 | 0.7211 | 0.7164 | `True` |
| **E5-base 768D** | 768 | `completed` | **42 / 45 (93.3%)** | **0.8407** | 0.6985 | 0.7061 | `True` |

### B. So sánh Bootstrap, Guardrails & Quyết định Clear Gain

| Candidate | $\Delta$ nDCG@5 | 95% Percentile CI | Guardrails Đạt | Clear Gain vs Control | Best Lighter | Clear Gain vs Lighter | Finalist Eligible |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Huydang DEk21 768D** | **-0.0262** | `[-0.1270, +0.0749]` | **FAIL** (6/9) | `False` | `e5-small-384` | `False` | `True` |
| **E5-base 768D** | **-0.0364** | `[-0.1002, +0.0219]` | **FAIL** (7/9) | `False` | `e5-small-384` | `False` | `True` |

### C. Độ trễ và Thời gian thực thi (Latency trên CPU FP32)

| Cấu hình | Cold Load | Doc Embed (572 chunks) | Query Embed (p50 / p95) | Qdrant Search (p50 / p95) | Total Latency (p50 / p95) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E5-small 384D (control)** | 7.55 s | **19.81 s** | **21.76 ms** / 33.17 ms | 5.44 ms / 7.92 ms | **27.40 ms** / 39.75 ms |
| **Huydang DEk21 768D** | 3.26 s | 44.38 s | 64.21 ms / 101.67 ms | 7.08 ms / 9.79 ms | 71.24 ms / 114.62 ms |
| **E5-base 768D** | 7.15 s | 47.15 s | 50.93 ms / 80.63 ms | 6.16 ms / 8.80 ms | 57.09 ms / 88.44 ms |

### D. Tài nguyên bộ nhớ & Truncation

| Cấu hình | Max Length | Truncated Docs / 572 | RSS trước load | RSS sau load | Peak RSS quan sát |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E5-small 384D (control)** | 512 | **0** | 956 MB | 1,340 MB | **1,574 MB** |
| **Huydang DEk21 768D** | 256 | **1** | 1,648 MB | 1,663 MB | 2,094 MB |
| **E5-base 768D** | 512 | **0** | 1,659 MB | 1,733 MB | 2,185 MB |

### E. Chi tiết nDCG@5 theo từng Category

| Category ($n$) | E5-small 384D (Control) | Huydang DEk21 768D | E5-base 768D |
| :--- | :---: | :---: | :---: |
| **relationship** (14) | **0.8994** (14/14 hits) | 0.8587 (14/14) ❌ | 0.8148 (13/14) ❌ |
| **direct_fact** (7) | 0.7930 (6/7 hits) | 0.7694 (7/7) ✅ | **0.8132** (7/7) ✅ |
| **food_knowledge** (7) | 0.7546 (6/7 hits) | **0.8571** (6/7) ✅ | 0.7606 (7/7) ✅ |
| **comparative** (6) | **0.5440** (5/6 hits) | 0.3972 (4/6) ❌ | 0.4929 (5/6) ❌ |
| **holistic** (3) | 0.6399 (3/3 hits) | **0.7606** (3/3) ✅ | 0.5850 (3/3) ✅ |
| **spanning** (3) | **0.3977** (3/3 hits) | 0.1131 (1/3) ❌ | 0.3412 (3/3) ✅ |
| **guide_planning** (2) | 0.5000 (1/2 hits) | **0.5655** (2/2) ✅ | 0.5000 (1/2) ✅ |
| **numerical** (2) | **1.0000** (2/2 hits) | **1.0000** (2/2) ✅ | **1.0000** (2/2) ✅ |
| **temporal** (1) | 0.6131 (1/1 hit) | **0.6934** (1/1) ✅ | 0.6131 (1/1) ✅ |

### F. An toàn hệ thống và Snapshot đối chiếu
- **Active Collection (`hue_foods_e5_small_384`):** Đã kết nối Qdrant live và đối chiếu snapshot: đúng 572 points, dense size 384, giữ nguyên trạng thái read-only tuyệt đối.
- **Isolated Collections:** Đúng 3 collections authorized tồn tại với 572 points:
  1. `hue_foods_08a_e5_small_384`: 572 points, 384D.
  2. `hue_foods_08a_huydang_dek21_768`: 572 points, 768D.
  3. `hue_foods_08a_e5_base_768`: 572 points, 768D.

---

## 5. Lỗi và giới hạn

1. **Phân tích Model Huydang DEk21:**
   - **Điểm sáng:** Đạt nDCG@5 cao ở nhóm `food_knowledge` (0.8571), `holistic` (0.7606) và `guide_planning` (0.5655) nhờ khả năng phân đoạn từ vựng tiếng Việt tự nhiên của `ViTokenizer`.
   - **Hạn chế:** `max_length=256` ngắn hơn 512 của E5 khiến 1 chunk dài bị cắt ngắn; trượt 3 category guardrails (`comparative`, `relationship`, `spanning`); query latency (~71 ms total) chậm hơn gấp đôi E5-small (~27 ms).
2. **Loại bỏ MiniLM-L12 & Qwen3:**
   - `MiniLM-L12` bị loại bỏ hoàn toàn do max length 128 gây cắt ngắn 83 chunks (14.5%), nDCG@5 tụt sâu (0.4709) và trượt 7/9 guardrails.
   - `Qwen3 0.6B 384D` bị loại do suy giảm nDCG@5 (0.6175), trượt guardrails và độ trễ CPU quá lớn (~765 s cho 572 chunks).
3. **Kết luận an toàn:**
   - Không có lỗi blocker trong phạm vi 3 model authorized. Active production collection và production settings hoàn toàn nguyên vẹn.

---

## 6. Handoff cho Reviewer

Reviewer nên kiểm tra:
1. File báo cáo triển khai này: [`reports/phase_8_08a_embedding_benchmark_implementation_report.md`](file:///home/minhhieu/hue_rag/reports/phase_8_08a_embedding_benchmark_implementation_report.md).
2. Mã nguồn backend và test:
   - [`backend/embedding/dense_benchmark.py`](file:///home/minhhieu/hue_rag/backend/embedding/dense_benchmark.py) (chỉ còn 3 settings: E5-small, Huydang, E5-base)
   - [`backend/evaluation/embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/evaluation/embedding_benchmark.py) (Boundary verification, mandatory snapshot, canonical map, settings table 3 cấu hình)
   - [`backend/tests/test_embedding_benchmark.py`](file:///home/minhhieu/hue_rag/backend/tests/test_embedding_benchmark.py) (23 unit tests pass)
3. Notebook: [`notebooks/08a_embedding_benchmark.ipynb`](file:///home/minhhieu/hue_rag/notebooks/08a_embedding_benchmark.ipynb) (xác nhận outputs sạch và loop đúng 2 candidate).
4. Hạ tầng Qdrant: 3 isolated collections (`hue_foods_08a_e5_small_384`, `hue_foods_08a_huydang_dek21_768`, `hue_foods_08a_e5_base_768`) đều đạt đúng 572 points. Collection MiniLM đã được xóa sạch.
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
   Xác nhận active collection `hue_foods_e5_small_384` (572 points) và `backend/config/settings.yaml` không thay đổi.
