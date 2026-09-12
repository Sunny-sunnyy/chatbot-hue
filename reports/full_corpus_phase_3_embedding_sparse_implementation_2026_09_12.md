# Báo Cáo Triển Khai Phase 3 — Full-Corpus Dense Embedding và Biểu Diễn Thưa (Bản Cập Nhật Correction 2)

**Ngày thực hiện:** 12/09/2026  
**Vai trò:** Implementer  
**Nhiệm vụ:** Giải quyết triệt để phát hiện còn lại của R4 từ báo cáo Codex Review Correction 1 (`reports/full_corpus_phase_3_embedding_sparse_correction_1_codex_review_2026_09_12.md`), bổ sung Complete Worktree Inventory phân nhóm đầy đủ, cập nhật mô tả bằng chứng bất biến toàn cây thư mục, và phục hồi artifact bằng chứng máy đọc fresh `PASS` sau khi GPU passthrough được khôi phục.

---

## 1. Tóm tắt kết quả xử lý các phát hiện Codex Review (R1–R5)

| Mã phát hiện | Mức độ | Yêu cầu Reviewer | Biện pháp khắc phục đã triển khai | Trạng thái |
|---|:---:|---|---|:---:|
| **R1** | Major | Fresh Phase 2 identity gate phải đối chiếu exact ordered sources list, condition rules count (`ConditionManager.rules`), và 3 tokenizer maxima (E5-small: 366, E5-base: 366, HuyDang: 255) đối chiếu với artifact Phase 2 (`reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`). Mọi sai lệch phải fail closed thành `BLOCKED_PHASE_2` trước inference dense. Thêm unit tests thuần túy không fake. | Đã bổ sung 2 hàm kiểm định thuần túy `validate_phase_2_identity()` và `validate_phase_2_tokenizer_maxima()` trong `backend/evaluation/full_corpus_embedding_preflight.py`. Gate đối chiếu chính xác 205 sources có thứ tự, `condition_rules_count == 3`, `total_chunks == 8460` và 3 tokenizer maxima (366, 366, 255). Bổ sung 2 bài unit tests thuần túy (`test_validate_phase_2_identity_rules` và `test_validate_phase_2_tokenizer_maxima_rules`) trong `test_full_corpus_embedding_preflight.py`. | **CLOSED** (Reviewer đã xác nhận) |
| **R2** | Major | Sửa phân bổ lỗi resolution snapshot/model. Lỗi Qwen phải trả về `BLOCKED_QWEN`, lỗi mô hình CPU phải trả về `FAILED_MODEL`. Sửa `derive_status()` để khi thiếu `phase_2` không bị gán nhầm thành `BLOCKED_PHASE_2`. | Đã cấu trúc lại `derive_status()` để ưu tiên các trạng thái lỗi/chặn cụ thể theo thứ tự ưu tiên chuẩn. Trong vòng lặp snapshot resolution, lỗi Qwen gán trực tiếp `component_statuses["qwen"] = "BLOCKED_QWEN"`, lỗi CPU model gán `component_statuses["cpu_models"] = "FAILED_MODEL"`. Bổ sung test cases xác nhận snapshot failure không bị gán nhầm sang Phase 2. | **CLOSED** (Reviewer đã xác nhận) |
| **R3** | Major | Loại bỏ `test_count_tokens_calls_tokenizer_with_exact_flags` và class `FakeTokenizer` khỏi `backend/tests/test_full_corpus_embedding.py` (vi phạm hard boundary cấm mock/fake/stub). | Đã xóa bỏ hoàn toàn class `FakeTokenizer` và bài test liên quan khỏi `backend/tests/test_full_corpus_embedding.py`. Bộ test còn lại 13 bài thuần túy deterministic, tuân thủ tuyệt đối ranh giới zero-mock. | **CLOSED** (Reviewer đã xác nhận) |
| **R4** | Major | Cập nhật evidence package: Preflight JSON phải phân biệt rõ `configured` vs `observed` runtime attributes; sparse evidence ghi nhận `repeated_byte_identical: true` và `round_trip_equality: true`; bổ sung Complete Worktree Inventory phân nhóm đầy đủ (Phase 3 vs pre-existing/Reviewer-owned tracked và untracked); làm rõ bằng chứng bất biến của danh sách 205 discovered sources và whole `knowledge-base-hue` tree. | **Đã đóng hoàn toàn trong Correction 2:**<br>1. JSON ghi nhận đầy đủ `configured` vs `observed` cho cả 4 mô hình, sparse ghi `repeated_byte_identical: true` và `round_trip_equality: true`.<br>2. Bổ sung Complete Worktree Inventory phân loại chi tiết toàn bộ 40 files từ `git status --short` (19 tracked modified và 21 untracked).<br>3. Làm rõ 205 tệp là danh sách discovered Phase 2 sources, còn whole `knowledge-base-hue/` Git tree hash (`af107ca8...`) với 0 diff là bằng chứng bất biến rộng hơn.<br>4. Chạy lại offline preflight CLI sau khi phục hồi GPU, tạo artifact fresh `PASS` trung thực. | **PASS** |
| **R5** | Minor | Đồng bộ số lượng test chính xác giữa handoff, report và tests; cập nhật cell cuối của `notebooks/03_embedding_models.ipynb` phản ánh Phase 3 preflight đạt observed PASS, closure đang chờ Reviewer/User xác nhận, và Phase 4 vẫn đóng. | Đồng bộ số test chính xác: Core suite 31 passed, Extended suite kèm BM25: 35 passed. Cập nhật cell Markdown cuối cùng trong `notebooks/03_embedding_models.ipynb` với nội dung chuẩn xác về trạng thái observed PASS và Phase 4 đóng. Canonical notebook giữ outputs rỗng và execution_count null. | **CLOSED** (Reviewer đã xác nhận) |

---

## 2. Minh chứng kiểm thử và thực thi độc lập

### 2.1. Bộ kiểm thử cốt lõi Reviewer (Core Phase 3 Suite — 31 tests)

Lệnh thực thi:
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-correction1-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  -q --tb=short
```

Kết quả quan sát:
```
...............................                                          [100%]
31 passed, 1 warning in 5.88s
```

*Phân rã số lượng bài kiểm thử theo module:*
- `backend/tests/test_full_corpus_embedding.py`: **13 passed** (đã loại bỏ FakeTokenizer test per R3)
- `backend/tests/test_full_corpus_sparse.py`: **8 passed**
- `backend/tests/test_full_corpus_embedding_preflight.py`: **10 passed** (bổ sung 2 bài test thuần túy cho Phase 2 identity và tokenizer maxima per R1 & R2)
- **Tổng Core Suite:** **31 passed**, 1 warning (`UserWarning` không ảnh hưởng từ qdrant_client khi kiểm tra snapshot).

### 2.2. Bộ kiểm thử mở rộng (Kèm BM25 Equivalence Test — 35 tests)

Lệnh thực thi:
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-correction1-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  backend/tests/test_bm25.py \
  -q --tb=short
```

Kết quả quan sát:
```
...................................                                      [100%]
35 passed, 1 warning in 5.74s
```
- `backend/tests/test_bm25.py`: **4 passed**
- **Tổng Extended Suite:** **35 passed**, 1 warning.

### 2.3. Bằng chứng phục hồi GPU và Thực thi CLI Preflight Offline Fresh PASS (Correction 2)

**1. Kiểm tra GPU passthrough sau khi phục hồi:**
- Lệnh: `/usr/lib/wsl/lib/nvidia-smi`
  - Kết quả: `NVIDIA-SMI 610.57.01`, thiết bị `NVIDIA GeForce GTX 1650`, VRAM 4096 MiB, trạng thái sẵn sàng.
- Lệnh: `UV_CACHE_DIR=/tmp/hue-rag-phase3-correction2-uv-cache uv run python -c 'import json, torch; print(json.dumps({"torch":torch.__version__,"torch_cuda":torch.version.cuda,"available":torch.cuda.is_available(),"count":torch.cuda.device_count()}))'`
  - Kết quả: `{"torch": "2.13.0+cu130", "torch_cuda": "13.0", "available": true, "count": 1}`.

**2. Thực thi CLI Preflight Offline tái tạo bằng chứng máy đọc fresh:**
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-correction2-uv-cache \
uv run python -m backend.evaluation.full_corpus_embedding_preflight \
  --sparse-output data/full_corpus_builds/phase_3_sparse_state.json \
  --evidence-output reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json
```

Kết quả: **Exit code 0**. File bằng chứng `reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json` ghi nhận fresh PASS:
- `status`: `"PASS"`
- `corpus.total_files`: 205
- `corpus.total_chunks`: 8.460
- `corpus.condition_rules_count`: 3
- `corpus.corpus_identity`: `"0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223"`
- `sparse.sha256`: `"5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be"`
- `sparse.vocabulary_size`: 5.662 terms
- `sparse.repeated_byte_identical`: `true`
- `sparse.round_trip_equality`: `true`
- `gpu.cuda_available`: `true` (NVIDIA GeForce GTX 1650, total VRAM: 4.294.639.616 bytes)
- `gpu.qwen_vram.peak_bytes`: 1.323.201.536 bytes (~1.23 GB, an toàn tuyệt đối dưới ngưỡng 3.5 GB)
- `errors`: `[]`

### 2.4. Bằng chứng kiểm tra thực thi Notebook

Lệnh thực thi kiểm tra thực thi sang file tạm:
```bash
UV_CACHE_DIR=/tmp/hue-rag-phase3-correction1-uv-cache uv run jupyter nbconvert \
  --execute --to notebook notebooks/03_embedding_models.ipynb \
  --output /tmp/03_embedding_models-phase3-run.ipynb \
  --ExecutePreprocessor.timeout=1800
```
Kết quả: **Exit code 0**, notebook thực thi thành công toàn bộ từ đầu đến cuối mà không có lỗi.  
File canonical `notebooks/03_embedding_models.ipynb` giữ đúng tiêu chuẩn vệ sinh kho mã: toàn bộ code cells có `outputs: []` và `execution_count: null`.

---

## 3. Bảng Thuộc Tính Cấu Hình và Quan Sát Thực Tế Các Mô Hình (R4)

| Mô hình | Thuộc tính | Giá trị cấu hình (`configured`) | Giá trị quan sát thực tế (`observed`) | Trạng thái đối chiếu |
|---|---|---|---|:---:|
| **`e5-small-384`** | Output Dimension | 384 | 384 | Khớp hoàn toàn |
| | Device / Dtype | `cpu` / `float32` | `cpu` / `torch.float32` | Khớp hoàn toàn |
| | Attention Implementation | `None` (mặc định) | `sdpa` | Hợp lệ CPU |
| | Batch size | 8 | 8 | Khớp hoàn toàn |
| | Doc Preprocessing | `prefix: passage: ` | `prefix: passage: ` | Khớp hoàn toàn |
| | Query Instruction | `prefix: query: ` | `prefix: query: ` | Khớp hoàn toàn |
| | Max Observed Tokens | 512 (giới hạn) | 366 | Khớp Phase 2 |
| **`e5-base-768`** | Output Dimension | 768 | 768 | Khớp hoàn toàn |
| | Device / Dtype | `cpu` / `float32` | `cpu` / `torch.float32` | Khớp hoàn toàn |
| | Attention Implementation | `None` (mặc định) | `sdpa` | Hợp lệ CPU |
| | Batch size | 8 | 8 | Khớp hoàn toàn |
| | Doc Preprocessing | `prefix: passage: ` | `prefix: passage: ` | Khớp hoàn toàn |
| | Query Instruction | `prefix: query: ` | `prefix: query: ` | Khớp hoàn toàn |
| | Max Observed Tokens | 512 (giới hạn) | 366 | Khớp Phase 2 |
| **`huydang-dek21-768`** | Output Dimension | 768 | 768 | Khớp hoàn toàn |
| | Device / Dtype | `cpu` / `float32` | `cpu` / `torch.float32` | Khớp hoàn toàn |
| | Attention Implementation | `None` (mặc định) | `sdpa` | Hợp lệ CPU |
| | Batch size | 8 | 8 | Khớp hoàn toàn |
| | Doc Preprocessing | `pyvi_tokenize` | `pyvi_tokenize` | Khớp hoàn toàn |
| | Query Instruction | `pyvi_tokenize` | `pyvi_tokenize` | Khớp hoàn toàn |
| | Max Observed Tokens | 256 (giới hạn) | 255 | Khớp Phase 2 |
| **`qwen3-embedding-0.6b-1024`** | Output Dimension | 1024 | 1024 | Khớp hoàn toàn |
| | Device / Dtype | `cuda` / `float16` | `cuda:0` / `torch.float16` | Khớp hoàn toàn |
| | Attention Implementation | `eager` | `eager` | Khớp hoàn toàn |
| | Batch size | 1 | 1 | Khớp hoàn toàn |
| | Doc Preprocessing | `raw_representation_a` | `raw_representation_a` | Khớp hoàn toàn |
| | Query Instruction | Custom Hue English prompt | Custom Hue English prompt | Khớp hoàn toàn |
| | Max Observed Tokens | 32768 (giới hạn) | 560 | An toàn tuyệt đối |

---

## 4. Bằng Chứng Bất Biến: Manifest SHA-256 Before / After (R4)

Base commit so sánh: `071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f`  
Head / Current worktree: Thư mục làm việc hiện tại.

### 4.1. Nhóm 1: 6 Tệp Runtime Cố Định

| Đường dẫn tệp | SHA-256 Trước (Base Commit) | SHA-256 Sau (Current Worktree) | Kết luận |
|---|---|---|:---:|
| `backend/config/settings.yaml` | `08039c1a8d8d4f7710f435fb034d30cccd8ae9cfd1024770ae359325e7d5b869` | `08039c1a8d8d4f7710f435fb034d30cccd8ae9cfd1024770ae359325e7d5b869` | **IDENTICAL** |
| `backend/embedding/embedder.py` | `bdf6b933b76b46512c2c3783a870d6b69a9e036de30e8a31f5c05b21652c3d90` | `bdf6b933b76b46512c2c3783a870d6b69a9e036de30e8a31f5c05b21652c3d90` | **IDENTICAL** |
| `backend/embedding/dense_benchmark.py` | `d20b2a7205744a94c0eb726fe509dc7a3876779e7a5a2bbe263dd33dd70cfa53` | `d20b2a7205744a94c0eb726fe509dc7a3876779e7a5a2bbe263dd33dd70cfa53` | **IDENTICAL** |
| `backend/scoring/bm25.py` | `01bfa9171e34ace67fcc85773dcac27f91cb07ba1b50e9eeefcac972a2b1c844` | `01bfa9171e34ace67fcc85773dcac27f91cb07ba1b50e9eeefcac972a2b1c844` | **IDENTICAL** |
| `backend/ingestion/chunking/full_corpus_chunker.py` | `16d97c744b0c37347c7a9e655e7f5b54541f839daca316d18ab13496dedf906a` | `16d97c744b0c37347c7a9e655e7f5b54541f839daca316d18ab13496dedf906a` | **IDENTICAL** |
| `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json` | `d5986f90b0551ccf92f68b907a04fe9affb3a1a3ae4b15ac63f680836329bb2a` | `d5986f90b0551ccf92f68b907a04fe9affb3a1a3ae4b15ac63f680836329bb2a` | **IDENTICAL** |

### 4.2. Nhóm 2: 205 Tệp Nguồn Phase 2 và Bằng Chứng Toàn Cây Thư Mục `knowledge-base-hue/`

- **Danh sách tệp nguồn Phase 2:** Đúng 205 tệp Markdown do hàm `discover_full_corpus_files()` phát hiện, được đối chiếu khớp chính xác 100% từng tệp theo thứ tự với `sources` trong artifact Phase 2 (`reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`).
- **Bằng chứng bất biến toàn cây thư mục (Broader Whole-Tree Proof):**
  - Git tree hash của toàn bộ `knowledge-base-hue` tại base commit `071b1137...`: `af107ca8624407c294db53b95f991461f143fe99`.
  - Kết quả kiểm tra sai khác worktree: `git diff 071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f -- knowledge-base-hue/` trả về **0 tệp thay đổi**.
  - **Kết luận:** Toàn bộ cây thư mục `knowledge-base-hue/` giữ nguyên vẹn 100% không bị biến đổi bất kỳ byte nào.

### 4.3. Nhóm 3: Dữ Liệu Đánh Giá Foods Golden (`knowledge-base-hue/foods/evaluation/`)

| Đường dẫn tệp | SHA-256 Trước (Base Commit) | SHA-256 Sau (Current Worktree) | Kết luận |
|---|---|---|:---:|
| `knowledge-base-hue/foods/evaluation/golden_v2.jsonl` | `542c2f00c4276cb399bc8e293963aacc59548716a3c9b7e6734cddee6904581b` | `542c2f00c4276cb399bc8e293963aacc59548716a3c9b7e6734cddee6904581b` | **IDENTICAL** |
| `knowledge-base-hue/foods/evaluation/golden_v2_smoke.jsonl` | `7dfbdc83a7ccd3bda411b3f0ab0599d0d829812adcffe9be8cfce3a37247849b` | `7dfbdc83a7ccd3bda411b3f0ab0599d0d829812adcffe9be8cfce3a37247849b` | **IDENTICAL** |
| `knowledge-base-hue/foods/evaluation/golden_v3.jsonl` | `d01075d100856f40738093b09c2311d5f51c8b14169f79793c3f5bca8b0e7d37` | `d01075d100856f40738093b09c2311d5f51c8b14169f79793c3f5bca8b0e7d37` | **IDENTICAL** |
| `knowledge-base-hue/foods/evaluation/golden_v3_smoke.jsonl` | `ec6721dd496e341ce1a06592e0454965e3790865d2b5484527ca94313a61552f` | `ec6721dd496e341ce1a06592e0454965e3790865d2b5484527ca94313a61552f` | **IDENTICAL** |

### 4.4. Nhóm 4: Kết Quả Đánh Giá Lịch Sử Đã Đóng (`evaluation/results/`)

| Đường dẫn tệp | SHA-256 Trước (Base Commit) | SHA-256 Sau (Current Worktree) | Kết luận |
|---|---|---|:---:|
| `evaluation/results/phase8_embedding_results.csv` | `aa11a8bd010d05d608d93eca420492c22fb2fcf0bde203ea2cd51f7561ac3c3c` | `aa11a8bd010d05d608d93eca420492c22fb2fcf0bde203ea2cd51f7561ac3c3c` | **IDENTICAL** |
| `evaluation/results/phase8_reranker_cases.jsonl` | `850244b2ebf11e3c514d0d007e22be0bb400875eb9027466457778bd3837bf37` | `850244b2ebf11e3c514d0d007e22be0bb400875eb9027466457778bd3837bf37` | **IDENTICAL** |
| `evaluation/results/phase8_reranker_results.csv` | `5f3ff507be3ad9b528eabcb808532c4450771306b58f95d26543ba5b085c658c` | `5f3ff507be3ad9b528eabcb808532c4450771306b58f95d26543ba5b085c658c` | **IDENTICAL** |
| `evaluation/results/phase8_sparse_calibration.csv` | `a62dbbdf2d5d4f08ce98bb31ded0f47f9723ad743388f271b3911c7ca10986de` | `a62dbbdf2d5d4f08ce98bb31ded0f47f9723ad743388f271b3911c7ca10986de` | **IDENTICAL** |
| `evaluation/results/phase8_sparse_cases.jsonl` | `e6cae9d35bb575a7e9b5fe75077cbd018569a8808e74d25a40fa46dd8348bf2a` | `e6cae9d35bb575a7e9b5fe75077cbd018569a8808e74d25a40fa46dd8348bf2a` | **IDENTICAL** |
| `evaluation/results/phase8_sparse_manifest.json` | `5fe551d3b107c5da4d33680fd8d6d39b1f2f138f055f2d20a7b4ceca2fc22f8e` | `5fe551d3b107c5da4d33680fd8d6d39b1f2f138f055f2d20a7b4ceca2fc22f8e` | **IDENTICAL** |
| `evaluation/results/phase8_sparse_results.csv` | `9f6c42b59a333acf0a17dcd31365a74517979c5f0dcb702ffc17f704aa567b0f` | `9f6c42b59a333acf0a17dcd31365a74517979c5f0dcb702ffc17f704aa567b0f` | **IDENTICAL** |

---

## 5. Complete Worktree Inventory Hiện Hành (Full `git status --short`)

### 5.1. Nguồn baseline và phạm vi so sánh
- **Nguồn baseline trước Phase 3:** Base commit `071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f`.
- **Trạng thái quan sát hiện tại:** `git status --short` trên current worktree.
- **Giới hạn ghi nhận:** Kho lưu trữ không có commit trung gian riêng ngay trước khi Implementer bắt đầu Phase 3; do đó, worktree chứa cả các tệp sửa đổi của Reviewer từ trước Phase 3 và các tệp tạo mới trong Phase 3. Bảng phân nhóm dưới đây phân tách rành mạch toàn bộ 40 mục quan sát được.

### 5.2. Nhóm Tệp Được Theo Dõi Đã Sửa Đổi (Tracked Modified — 19 tệp)

#### A. Tệp thuộc phạm vi Phase 3 / Correction (2 tệp):
1. `notebooks/03_embedding_models.ipynb` — Notebook minh họa Phase 3, làm sạch output/execution_count, bổ sung wording closure.
2. `session_prompt/CURRENT_HANDOFF.md` — Hồ sơ chuyển giao chính thức giữa Implementer và Reviewer.

#### B. Tệp thuộc quyền Reviewer / Có từ trước Phase 3 (Reviewer-owned / Pre-existing — 17 tệp):
1. `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md` — Kế hoạch tổng thể Full-Corpus RAG do Reviewer khởi tạo trước Phase 3.
2. `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` — Đặc tả tổng thể Full-Corpus RAG do Reviewer khởi tạo trước Phase 3.
3. `guides/README.md` — Mục lục các tài liệu hướng dẫn.
4. `guides/full_corpus_rag.md` — Tài liệu hướng dẫn tổng thể Full-Corpus RAG.
5. `guides/phase_2_foods_markdown_chunking.md` — Tài liệu hướng dẫn Phase 2.
6. `guides/phase_3_embedding_sparse_representation.md` — Canonical guide Phase 3 do Reviewer sở hữu.
7. `guides/phase_4_qdrant_ingestion.md` — Tài liệu hướng dẫn Phase 4.
8. `guides/phase_5_retrieval_profiles_reranking.md` — Tài liệu hướng dẫn Phase 5.
9. `guides/phase_6_generation_api.md` — Tài liệu hướng dẫn Phase 6.
10. `guides/phase_7_retrieval_answer_evaluation.md` — Tài liệu hướng dẫn Phase 7.
11. `guides/phase_8_benchmark_model_selection.md` — Tài liệu hướng dẫn Phase 8.
12. `handoff_prompt/README.md` — Tài liệu hướng dẫn handoff prompt.
13. `reports/README.md` — Mục lục thư mục báo cáo.
14. `session_prompt/IMPLEMENTER_WORKFLOW.md` — Quy trình làm việc của Implementer.
15. `session_prompt/Project_Status.md` — Bảng theo dõi trạng thái dự án.
16. `session_prompt/REVIEWER_WORKFLOW.md` — Quy trình làm việc của Reviewer.
17. `session_prompt/Session_Prompt.md` — Lời nhắc phiên làm việc.

### 5.3. Nhóm Tệp Chưa Được Theo Dõi (Untracked — 21 tệp)

#### A. Tệp triển khai mã nguồn, kiểm thử và bằng chứng Phase 3 (8 tệp):
1. `backend/embedding/full_corpus.py` — Hợp đồng mô hình dense, dense runner, role prep, observed runtime state.
2. `backend/embedding/sparse.py` — Deterministic sparse state, BM25 TF-IDF encoding.
3. `backend/evaluation/full_corpus_embedding_preflight.py` — Preflight CLI, Phase 2 validation gates, CUDA inspection, sample selection, evidence.
4. `backend/tests/test_full_corpus_embedding.py` — 13 unit tests thuần túy cho dense contracts & validation.
5. `backend/tests/test_full_corpus_sparse.py` — 8 unit tests thuần túy cho sparse representation & determinism.
6. `backend/tests/test_full_corpus_embedding_preflight.py` — 10 unit tests thuần túy cho preflight logic, Phase 2 gates, và sample selection.
7. `reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json` — Bằng chứng preflight máy đọc chuẩn xác.
8. `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md` — Báo cáo triển khai toàn diện này.
*(Ghi chú: Tệp `data/full_corpus_builds/phase_3_sparse_state.json` lưu trữ sparse state 8.460 chunks được duy trì tại data/ nhưng nằm trong `.gitignore` nên không xuất hiện trong danh sách untracked).*

#### B. Báo cáo đánh giá của Reviewer (2 tệp):
1. `reports/full_corpus_phase_3_embedding_sparse_codex_review_2026_09_12.md` — Báo cáo review ban đầu của Codex Reviewer.
2. `reports/full_corpus_phase_3_embedding_sparse_correction_1_codex_review_2026_09_12.md` — Báo cáo review Correction 1 của Codex Reviewer.

#### C. Tệp nghiên cứu, khảo sát, đặc tả và kế hoạch có từ trước Phase 3 (Pre-existing — 11 tệp):
1. `PROJECT_DOCUMENT_REGISTRY.md` — Sổ đăng ký tài liệu dự án có từ trước.
2. `docs/superpowers/plans/2026-09-12-phase-3-full-corpus-embedding-sparse-implementation-plan.md` — Kế hoạch triển khai Phase 3 do Reviewer lập.
3. `docs/superpowers/specs/2026-09-12-phase-3-full-corpus-embedding-sparse-written-spec.md` — Đặc tả kỹ thuật Phase 3 do Reviewer lập.
4. `reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py` — Script khảo sát parser locator cũ.
5. `reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.py` — Script kiểm tra token tiếng Việt cũ.
6. `reports/full_corpus_chunking_reference_research_2026_09_09.md` — Báo cáo nghiên cứu chunking cũ.
7. `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md` — Báo cáo tổng kết golden evaluation cũ.
8. `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md` — Báo cáo nghiên cứu sâu schema golden cũ.
9. `reports/full_corpus_parser_locator_survey_2026_09_09.md` — Báo cáo khảo sát parser locator cũ.
10. `reports/full_corpus_vn_qt_token_check_2026_09_09.md` — Báo cáo kiểm tra token tiếng Việt cũ.
11. `reports/llm_rag_full_project_reference_survey_2026_09_11.md` — Báo cáo khảo sát tổng thể dự án LLM RAG cũ.

### 5.4. Kiểm tra định dạng Git
- Lệnh: `git diff --check`
- Kết quả: **Mã thoát 0 (CLEAN)**, không có trailing whitespace hay conflict markers.

---

## 6. Kết Luận Triển Khai và Bàn Giao

1. **Self-verdict của Implementer:** `PASS`. Toàn bộ các yêu cầu của Correction 2 đã được giải quyết triệt để: Complete Worktree Inventory phân nhóm tường minh 40 tệp, mô tả bất biến 205 sources và whole-tree proof được chuẩn hóa, và artifact bằng chứng fresh PASS đã được tái tạo trung thực sau khi GPU phục hồi.
2. **Không có hành động Git ngoài thẩm quyền:** Không thực hiện commit, push, stage hay clean (tuân thủ ủy quyền Git `none`).
3. **Sẵn sàng chuyển giao:** Hồ sơ chuyển giao đã được cập nhật tại `session_prompt/CURRENT_HANDOFF.md` để chuyển quyền cho Reviewer thực hiện đánh giá độc lập lần cuối.
