# Implementation Report: Full-corpus Metadata v2 (Comprehensive Tasks 1–7)

Implementer: Gemini Implementer
Date: 2026-09-30 +07
Status: complete — all tasks (Tasks 1–7) implemented and verified; system ready for Reviewer final review
Canonical guide: `guides/full_corpus_rag.md`
Spec: `docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md`
Plan: `docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md`
User Approvals:
- Gate 1 (Tasks 1–4): Approved 2026-09-29 +07
- Gate 2 (Task 5): Approved 2026-09-29 +07
- Gate 3 (Task 6): Approved 2026-09-29 +07
- Task 7: Approved 2026-09-30 +07
Git authorization: none
Risk level: high

---

## Authority, gates and repository state

- **Authority:**
  Triển khai theo đúng Written Spec và Implementation Plan được phê duyệt ngày 2026-09-29 +07. Mọi gate chuyển tiếp (Gate 1 preflight, Gate 2 collection migration, Gate 3 runtime retrieval cutover, và Task 7 final regression & handoff) đều được User phê duyệt rõ ràng trước khi tiến hành.
- **Repository state:**
  - Base commit: `92f2e2cce0e85c9b4f733aaab038bc99cad314c0`.
  - Không thực hiện bất kỳ lệnh `git commit`, `git add`, `git push`, `git checkout` hay `git reset` (`git_authorization: none`).
  - Toàn bộ staged changes (staged deletions trong `knowledge-base-hue/`, `.gitignore`) và untracked files từ các phiên trước được bảo toàn nguyên vẹn.
  - `git diff --check` sạch hoàn toàn, không có trailing whitespace.

---

## Changed paths and responsibilities

| Đường dẫn | Thao tác | Trách nhiệm |
|---|---|---|
| `backend/core/schema.py` | Update | Bổ sung hằng số `FULL_CORPUS_DOMAINS`, hàm `domain_for_source()` suy dẫn domain từ component đầu của POSIX path, và hàm `point_id_for_chunk_id()` tạo deterministic UUID5 từ `chunk_id`. |
| `backend/ingestion/chunker.py` | Update | Thêm trường `domain` vào `FullCorpusChunk`, cập nhật `to_qdrant_payload()` trả về đúng 7 trường canonical v2 (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`). |
| `backend/ingestion/full_corpus_pipeline.py` | Update | Mở rộng `FullCorpusCandidate` với trường `metadata_v2_collection_name`, cố định bảng mapping `_METADATA_V2_COLLECTION_BY_CANDIDATE` cho 4 candidate. |
| `backend/ingestion/source_state.py` | Update | Định nghĩa `FULL_CORPUS_BUILD_SCHEMA_V2` (`phase_4_full_corpus_build:v2`), `FULL_CORPUS_PAYLOAD_SCHEMA_V2` (`full_corpus_qdrant_payload:v2`), hàm `make_full_corpus_metadata_v2_build_record()`, và `verify_full_corpus_record_freshness()`. |
| `backend/ingestion/full_corpus_metadata_v2.py` | Create | Module migration chuyên biệt cho metadata-v2: thực thi `preflight`, `migrate`, và `verify` với bounded pagination (batch 64), copy vectors nguyên vẹn, zero re-embedding, kiểm tra tính tương đương vector và payload nghiêm ngặt. |
| `backend/retrieval/full_corpus.py` | Update | Chuyển đổi runtime retrieval sang metadata-v2 collections: chiếu 7 trường canonical; kiểm tra v2 build record, target collection, exact legacy lineage SHA-256 bytes, Qdrant build invariants, và corpus freshness khi khởi tạo; khử rò rỉ private source/chunk path trong payload validation errors; bảo đảm allowlist technical trace và trả về `RetrievedDocument` với `id=chunk_id` cùng metadata `domain`. |
| `backend/tests/test_full_corpus_chunker.py` | Update | Kiểm thử pure payload v2, domain derivation, deterministic UUID5 relation, và 7 canonical fields. |
| `backend/tests/test_full_corpus_qdrant_ingestion.py` | Update | Kiểm thử candidate mapping registry v2, v2 build record constructor, và tính tương thích ngược của v1. |
| `backend/tests/test_full_corpus_metadata_v2.py` | Create | Kiểm thử migration primitives: point transform, vector equivalence, payload validation, confirmation guard, preflight/migrate/verify CLI orchestration với zero mutation khi lỗi. |
| `backend/tests/test_full_corpus_retrieval.py` | Update | Bổ sung các unit test v2 runtime: payload validation, sanitized error messages (không rò rỉ private marker), build record target/lineage/Qdrant invariants checks, startup freshness fail-closed, RRF tie-break preservation trên point UUID, và technical trace allowlist. |
| `reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json` | Create | Preflight artifact xác nhận trạng thái `READY` trước khi ghi dữ liệu tại Gate 1. |
| `data/full_corpus_builds/hue_full_corpus_a_*_metadata_v2.json` | Create | 4 build records v2 chính thức cho 4 candidate targets tại Gate 2. |
| `session_prompt/CURRENT_HANDOFF.md` | Update | Cập nhật tài liệu bàn giao chuẩn hóa cho Reviewer. |

---

## RED/GREEN focused checks

Mọi bước triển khai đều tuân thủ nghiêm ngặt quy trình TDD (RED -> GREEN):
- **Task 1 (Chunker & Schema v2):** RED xác nhận thiếu domain & 7 trường v2 -> GREEN: 34 passed.
- **Task 2 (Candidate registry & build record v2):** RED xác nhận thiếu target mapping & v2 build schema -> GREEN: 24 passed.
- **Task 3 & 4 (Migration primitives & Preflight CLI):** RED xác nhận module chưa tồn tại -> GREEN: 76 passed.
- **Task 6 (Runtime cutover):** RED ban đầu: 11 failed, 13 passed -> GREEN: 24 passed -> Correction 1: 25 passed.
- **Task 7 (Final regression check):**
  ```bash
  HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest \
    backend/tests/test_full_corpus_chunker.py \
    backend/tests/test_full_corpus_sparse.py \
    backend/tests/test_full_corpus_qdrant_ingestion.py \
    backend/tests/test_full_corpus_metadata_v2.py \
    backend/tests/test_full_corpus_retrieval.py -q --tb=short
  ```
  - **Kết quả:** **158 passed in 111.76s**, 0 failed, 0 warnings.

---

## Canonical payload/domain/identity evidence

1. **Exact 7 canonical fields:**
   - `search_text`: chuỗi văn bản không rỗng được chuẩn hóa LF dùng để reranking và hiển thị.
   - `source`: đường dẫn tương đối POSIX của file Markdown nguồn.
   - `title`: tiêu đề tài liệu.
   - `heading_path`: danh sách các heading phân cấp (list[str]).
   - `evidence_parts`: danh sách các đoạn evidence với schema nghiêm ngặt (`role`, `start`, `end`, `text`).
   - `chunk_id`: định dạng `<source>#<chunk_index>`.
   - `domain`: phân loại sản phẩm suy dẫn từ component đầu của POSIX path.
2. **Canonical product domains:**
   - Tập hợp 5 domain hợp lệ: `{"foods", "heritages", "festivals", "performing_arts", "travel"}`.
   - Được suy dẫn tất định bằng `domain_for_source(source)`.
3. **Deterministic UUID5 identity:**
   - Quan hệ 1-1 tất định: `point_id == str(uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}"))`.
   - Bảo toàn khóa chính duy nhất cho Qdrant point.

---

## Gate 1 four-pair preflight

- **Thực thi:**
  ```bash
  UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight \
    --output reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
  ```
- **Kết quả:**
  - Trạng thái tổng thể: `READY` trên cả 4 candidate pairs.
  - Zero mutations: không tạo collection, không ghi điểm, không sinh build record v2.
  - Xác nhận 4 legacy sources có đầy đủ 8.460 points hợp lệ, 205 files nguồn tươi mới, và 4 target metadata-v2 hoàn toàn chưa tồn tại.
  - Preflight artifact SHA-256: `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`.

---

## Gate 2 collection writes and complete verification

- **Thực thi:**
  Di chuyển tuần tự từng cặp candidate sau khi User phê duyệt Gate 2:
  1. `e5-small-384` -> `hue_full_corpus_a_e5_small_384_metadata_v2` (384D)
  2. `e5-base-768` -> `hue_full_corpus_a_e5_base_768_metadata_v2` (768D)
  3. `huydang-dek21-768` -> `hue_full_corpus_a_huydang_dek21_768_metadata_v2` (768D)
  4. `qwen3-embedding-0.6b-1024` -> `hue_full_corpus_a_qwen3_06b_1024_metadata_v2` (1024D)
- **Quy trình copy vectors:**
  - Vectors (dense và sparse) được sao chép trực tiếp từ source points sang target points qua các trang scroll 64 points.
  - Hoàn toàn không tải mô hình embedding dense, không re-encode, không gọi API bên ngoài.
- **Xác thực toàn diện:**
  - Đối chiếu 100% 33.840 points (8.460 points/collection × 4 targets): từng giá trị float của dense vector, từng index/value của sparse vector, và toàn bộ 7 trường payload đều khớp tuyệt đối giữa source và target.
  - Lệnh kiểm chứng độc lập cuối:
    ```bash
    UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
    ```
    Kết quả: **`Verification status: VERIFIED`** trên toàn bộ 4 targets.

---

## Build-record v2 and vector lineage

- **4 build records v2 đã ghi tại `data/full_corpus_builds/`:**
  - `hue_full_corpus_a_e5_small_384_metadata_v2.json`
  - `hue_full_corpus_a_e5_base_768_metadata_v2.json`
  - `hue_full_corpus_a_huydang_dek21_768_metadata_v2.json`
  - `hue_full_corpus_a_qwen3_06b_1024_metadata_v2.json`
- **Vector lineage và invariants:**
  - Mỗi record chứa khối `migration`:
    ```json
    "migration": {
      "mode": "copy_verified_vectors",
      "source_collection": "<legacy_collection>",
      "source_build_record_sha256": "<sha256_of_legacy_build_record_file>"
    }
    ```
  - Schema literals: `schema_version == "phase_4_full_corpus_build:v2"` và `qdrant.payload_schema_version == "full_corpus_qdrant_payload:v2"`.
  - Qdrant invariants: `dense_vector_name == "dense"`, `sparse_vector_name == "sparse"`, `distance == "cosine"`, `point_count == 8460`.
  - Runtime retrieval service bắt buộc đối chiếu SHA-256 thực tế của file legacy build record với trường `source_build_record_sha256` khi khởi tạo.

---

## Legacy collection immutability

- Cả 4 legacy collection (`hue_full_corpus_a_e5_small_384`, `hue_full_corpus_a_e5_base_768`, `hue_full_corpus_a_huydang_dek21_768`, `hue_full_corpus_a_qwen3_06b_1024`) cùng các collections Foods đều giữ nguyên trạng thái chỉ đọc.
- Không có bất kỳ thao tác xóa, cập nhật point hay thêm payload index nào trên các legacy collections.
- Các file legacy build record v1 trong `data/full_corpus_builds/` giữ nguyên vẹn nội dung và SHA-256.

---

## Gate 3 runtime freshness and retrieval identity

- **Khởi tạo dịch vụ (`build_full_corpus_retrieval_service`):**
  - Trỏ target collection sang `candidate.metadata_v2_collection_name`.
  - Kiểm tra v2 build record: schema version, target collection name, lineage SHA-256 khớp file legacy thực tế, và toàn bộ 4 invariant Qdrant.
  - Kiểm tra độ tươi của corpus filesystem: quét 205 files nguồn, tính SHA-256 từng file, fail-closed nếu phát hiện bất kỳ file nào bị thêm, xóa, hoặc sửa đổi so với build record.
  - Kiểm tra live Qdrant target: point count == 8.460 và `payload_schema == {}` (bảo đảm zero payload indexes theo invariant thiết kế).
- **Xử lý truy vấn (`FullCorpusRetrievalService.search`):**
  - Chiếu chính xác 7 trường canonical trong `with_payload`.
  - `validate_point_payload` kiểm tra cấu trúc 7 trường, tính tương thích giữa `source` và `chunk_id`, point UUID relation, và domain derivation.
  - Bảo toàn xếp hạng và tie-break RRF trên point UUID nội bộ.
  - Xây dựng `RetrievedDocument` trả về có `id == chunk_id` và metadata chứa `domain`.
  - Technical trace (`stages`) chỉ chứa allowlist an toàn: `point_id`, `chunk_id`, `domain`, `rank`, `score`.

---

## Selected real retrieval smoke

Chạy thực tế ở chế độ read-only với 2 kịch bản smoke matrix:

1. **8 cells no-rerank (4 candidates × 2 treatments × query P5-Q01):**
   - Lệnh:
     ```bash
     HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run \
       --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 \
       --treatment dense_bm25_rrf native_hybrid_rrf \
       --reranker none \
       --select P5-Q01 \
       --output data/full_corpus_metadata_v2_smoke.json
     ```
   - **Kết quả:** **PASS on all 8 cells** (exit code 0), `determinism_pass = True`, anomalies `[]`. Toàn bộ document IDs trả về theo định dạng canonical `chunk_id`.
   - Latency p95: từ 34.58 ms đến 230.48 ms.
   - Artifact: `data/full_corpus_metadata_v2_smoke.json` (gitignored).

2. **2 cells MiniLM reranker (candidate `e5-small-384` × 2 treatments × query P5-Q01):**
   - Lệnh:
     ```bash
     HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run \
       --candidate e5-small-384 \
       --treatment dense_bm25_rrf native_hybrid_rrf \
       --reranker minilm \
       --select P5-Q01 \
       --output data/full_corpus_metadata_v2_minilm_smoke.json
     ```
   - **Kết quả:** **PASS on both cells** (exit code 0, 21 warm observations/cell), `determinism_pass = True`.
   - Latency p95: **1475.2 ms** và **1197.8 ms** (đáp ứng xuất sắc latency gate < 3000 ms).
   - Artifact: `data/full_corpus_metadata_v2_minilm_smoke.json` (gitignored).

---

## Privacy and unchanged public/evaluation boundaries

- **Zero leakage:**
  - Thông báo lỗi khi validate payload chỉ chứa safe `point_id` và generic reason code; tuyệt đối không chứa `source`, `chunk_id`, `search_text`, `evidence_parts` hay absolute paths.
  - Technical trace không chứa nội dung câu truy vấn, text văn bản, payload thô hay credentials.
  - Các tệp smoke output trace đều nằm trong đường dẫn gitignored (`data/*.json`).
- **Unchanged boundaries:**
  - Không thay đổi public API, schema giao diện ứng dụng.
  - Không thay đổi bộ Golden evaluation queries/answers, không chạy đánh giá LLM hay gọi paid API.
  - Không dùng trường `domain` để filter, boost hay can thiệp vào điểm ranking số học.

---

## Acceptance mapping

| Tiêu chí Written Spec / Plan | Trạng thái | Bằng chứng thực tế |
|---|---|---|
| 7 trường canonical v2 | ĐẠT | `to_qdrant_payload()` trong `chunker.py`, `validate_point_payload()` trong `full_corpus.py`. |
| Suy dẫn 5 domain từ source path | ĐẠT | `domain_for_source()` trong `schema.py`, kiểm thử trong `test_full_corpus_chunker.py`. |
| Quan hệ chunk_id và point UUID | ĐẠT | `point_id_for_chunk_id()` trong `schema.py`, kiểm thử trong `test_full_corpus_retrieval.py`. |
| Cố định 4 metadata-v2 target collections | ĐẠT | `_METADATA_V2_COLLECTION_BY_CANDIDATE` trong `full_corpus_pipeline.py`. |
| Sao chép vector nguyên vẹn không re-embedding | ĐẠT | `run_migration()` trong `full_corpus_metadata_v2.py`, zero model load, 100% vector equality. |
| Build record v2 và lineage SHA-256 | ĐẠT | 4 files v2 build records tại `data/full_corpus_builds/`, đối chiếu SHA legacy build record. |
| Zero payload schema index | ĐẠT | `validate_full_corpus_collection_info()` xác nhận `payload_schema == {}` trên cả 4 targets. |
| Strict startup freshness fail-closed | ĐẠT | `verify_full_corpus_record_freshness()` fail-closed khi phát hiện sai khác filesystem corpus. |
| RetrievedDocument có chunk_id & domain | ĐẠT | `build_retrieved_document()` trong `full_corpus.py`, kiểm chứng trong 2 smoke runs. |
| Trace allowlist & privacy | ĐẠT | `format_stage_entry()` chỉ chứa 5 trường allowlist, privacy probe tests đạt 100%. |

---

## Deviations and anomalies

- Trong quá trình review Gate 3, Reviewer đã phát hiện 2 major findings (F1: startup target/lineage/Qdrant invariants checks, F2: sanitized payload validation errors) và 1 minor (F3: evidence hygiene).
- Implementer đã xử lý triệt để trong Correction 1:
  - F1: Thêm kiểm tra target collection name, lineage SHA tính từ bytes của exact legacy build record file, và đầy đủ 4 Qdrant invariants (`dense`, `sparse`, `cosine`, 8460).
  - F2: Khử toàn bộ rò rỉ source/chunk path trong exceptions, dập exception chaining bằng `from None`, bổ sung marker-based privacy tests.
  - F3: Sửa Risk level thành `high`, chuẩn hóa tên 7 trường payload, sửa build schema literal thành `phase_4_full_corpus_build:v2`, làm sạch trailing whitespace.
- Hiện tại: **Không còn bất kỳ deviation hay anomaly nào chưa được giải quyết**.

---

## Failed, skipped and not verified

- **Full backend test suite:** Không chạy (nằm ngoài phạm vi Task 7 để kiểm soát blast radius, tuân thủ nguyên tắc chỉ chạy focused regression suite 158 tests).
- **Data mutation:** Không thực hiện bất kỳ thao tác xóa, sửa, hay ghi đè nào trên các collections hay build records hiện có.

---

## Limitations and Reviewer handoff

- Hệ thống đã hoàn tất toàn bộ chu trình di chuyển metadata-v2 và runtime cutover một cách an toàn, tất định và có bằng chứng xác thực đầy đủ.
- Nhiệm vụ tiếp theo: Bàn giao cho Reviewer thực hiện independent final review toàn diện cho workstream Metadata v2.
