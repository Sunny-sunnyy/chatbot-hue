# Phase 7A2 — Sửa corpus + tạo lại index: Implementation Plan

> **For agentic workers:** thực hiện từng gate theo đúng `CURRENT_HANDOFF.md`.
> Mỗi gate là một handoff riêng; không làm gate sau khi gate trước chưa được
> User đóng. Steps dùng checkbox (`- [ ]`).

**Status:** Approved by User 2026-10-23
**Spec:** `docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md`
(User-approved 2026-10-23; spec là nguồn requirement, plan này không thay spec)

**Goal:** sửa 25 mục tri thức trong corpus, build lại hai index full-corpus
(`e5-small-384` local, `qwen3-embedding-8b` OpenRouter) trên corpus đã sửa,
cutover runtime sang e5-small mới, rồi xóa 13 collection cũ.

**Architecture:** một đường build duy nhất ghi thẳng schema metadata v2 vào
collection mới; build record của từng collection là nguồn sự thật duy nhất cho
"index khớp corpus"; runtime giữ kiểm tra freshness theo hash file trong record.
8B dùng một dense runner gọi OpenRouter có cùng interface với runner local.

**Tech stack:** Python qua `uv`, Qdrant `127.0.0.1:6335`, sentence-transformers
(e5-small), OpenRouter `/api/v1/embeddings`, `httpx`, `gpt-6-luna` (live smoke).

## Global Constraints

- Không mock, fake, stub, replay hay expected value làm PASS evidence.
- Chạy bằng `uv run --env-file .env ...`; không đọc, in hay log giá trị secret.
- `knowledge-base-hue/`, `data/`, Golden và nội dung chunk là private; report
  tracked không chép nội dung corpus, Golden, vector hay raw payload.
- Không đổi chunker. Giữ nguyên `full_corpus.embedding_models` trong
  `backend/config/settings.yaml` (ba tokenizer e5-small/e5-base/huydang quyết
  định ranh giới chunk), dù chỉ còn embed bằng e5-small và 8B.
- Payload đúng 7 field: `search_text`, `source`, `title`, `heading_path`,
  `evidence_parts`, `chunk_id`, `domain`.
- Collection mới: `hue_full_corpus_7a2_e5_small_384`,
  `hue_full_corpus_7a2_qwen3_8b_4096`.
- OpenRouter: model `qwen/qwen3-embedding-8b`, 4096 chiều, batch cố định 64,
  không gửi `dimensions`, `encoding_format: "float"`, không pin provider, mọi
  request gửi `provider: {"data_collection": "deny"}`, không retry/fallback/
  resume. Key lấy từ env `OPENROUTER_API_KEY`.
- Retrieval profile, reranker, context và generation giữ nguyên Phase 6.
- Git authorization: `none` trừ khi handoff ghi khác. Không commit.
- Gợi ý tên hàm/class trong plan là minh họa; ràng buộc là hành vi, path,
  tên collection và acceptance.

---

## Gate 1 — Sửa corpus

Không đổi code, không đụng Qdrant, không paid call.

### Task 1: Backup và baseline

**Files:**
- Create: `knowledge-base-hue/meta/backup_7a2_2026_10_23/<cùng đường dẫn tương đối>`

- [ ] **Step 1:** Từ `gửi chatgpt/kết quả nghiên cứu/TONG_HOP_REVIEWER_2026_10_23.md`
  (mục A) và R1/R2 cùng thư mục (vị trí mục B: K30, K33, K34, K48), lập danh
  sách file sẽ sửa. Với K1, liệt kê thêm các file lăng trong
  `knowledge-base-hue/heritages/heritage/` có ghi mã UNESCO 001–014.
- [ ] **Step 2:** Copy nguyên bản từng file vào backup, giữ đường dẫn:

```bash
cd /home/minhhieu/hue_rag/knowledge-base-hue
mkdir -p meta/backup_7a2_2026_10_23
cp --parents "heritages/heritage-guides.md" meta/backup_7a2_2026_10_23/
# lặp cho từng file trong danh sách Step 1
```

- [ ] **Step 3:** Baseline Golden và chunker (không tốn phí):

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl
```

  Ghi kết quả thật (dự kiến exit 0, 176 và 10 case). Cú pháp theo
  `backend/evaluation/golden_full_corpus.py:139-170` và report Phase 7A.
- [ ] **Step 4:** Ghi số file và số chunk hiện tại bằng chunker thật
  (`discover_full_corpus_files`, `chunk_full_corpus`) và xác nhận không có file
  nào dưới `meta/` được discover.

### Task 2: Sửa 25 mục

**Files:** chỉ các file trong danh sách Task 1.

- [ ] **Step 1:** Sửa 21 mục nhóm A theo đúng cột "Giá trị chuẩn" và "File cần
  sửa". Câu văn tự nhiên, answer-facing; không thêm ghi chú biên tập vào body.
- [ ] **Step 2:** Chỉnh câu chữ 4 mục nhóm B để nói rõ ngữ cảnh, không đổi sự
  kiện (K33 cung khác điện; K34 lễ lịch sử khác bản tái hiện; K30 kỳ 2026 khác
  kỳ đầu 2023; K48 xe máy không tự chạy qua hầm).
- [ ] **Step 3:** Thêm căn cứ vào `## Nguồn dữ liệu` của file bị sửa (URL và
  ngày truy cập lấy từ file tổng hợp/R1/R2). K27 ghi rõ văn bản gốc chưa được
  Reviewer tự mở để kiểm.
- [ ] **Step 4:** Với mỗi file, diff với backup và xác nhận diff chỉ chứa mục
  đã giao và dòng nguồn:

```bash
cd /home/minhhieu/hue_rag/knowledge-base-hue
diff -u "meta/backup_7a2_2026_10_23/heritages/heritage-guides.md" "heritages/heritage-guides.md"
```

- [ ] **Step 5:** Chạy lại chunker thật: không có chunking error; ghi số file và
  số chunk mới.

### Task 3: Golden sau khi sửa

**Files:** chỉ sửa `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` và
`golden_full_corpus_smoke.jsonl` nếu có case bị ảnh hưởng.

- [ ] **Step 1:** Tìm giá trị cũ của 25 mục (ví dụ tên phường cũ, năm cũ, số đo
  cũ) trong `question`, `keywords`, `reference_answer` của cả hai file. Ghi
  danh sách số dòng bị trúng (có thể rỗng).
- [ ] **Step 2:** Case bị trúng: sửa tối thiểu `keywords`/`reference_answer`
  theo giá trị mới. Case trong smoke phải giữ deep-equal với dòng tương ứng
  trong file canonical.
- [ ] **Step 3:** Chạy lại `check` cho cả hai file (lệnh Task 1 Step 3). Yêu
  cầu PASS.
- [ ] **Step 4:** Viết report
  `reports/phase_7a2_gate_1_corpus_correction_implementation_2026_10_23.md`:
  bảng 25 mục (mã, path, dòng trước/sau), danh sách file trong backup, số
  file/chunk trước/sau, kết quả `check` trước/sau, danh sách dòng Golden đã sửa
  kèm mã mục. Không chép nội dung corpus/Golden.
- [ ] **Step 5:** Chuyển handoff về `reviewer` (kind `final_review`) và nhắn
  Reviewer.

---

## Gate 2 — Build 2 index và cutover runtime

### Task 4: Build record là nguồn sự thật duy nhất

**Files:**
- Modify: `backend/ingestion/source_state.py` (`make_full_corpus_build_record`,
  bỏ `make_full_corpus_metadata_v2_build_record`)
- Modify: `backend/ingestion/full_corpus_pipeline.py:53-61,134-201`
- Modify: `backend/retrieval/full_corpus.py:353-456,760-800`
- Test: `backend/tests/test_full_corpus_retrieval.py`,
  `backend/tests/test_full_corpus_qdrant_ingestion.py`

**Interfaces:**
- Produces: `make_full_corpus_build_record(*, collection_name, candidate_id,
  dense: Mapping, sources: Mapping[str, str], chunk_count: int,
  corpus_identity: str, sparse_state: SparseState, sparse_state_sha256: str,
  providers: Sequence[str] = ()) -> dict` — không hard-code 205/8460/5662;
  `file_count = len(sources)`.
- Produces: `validate_full_corpus_build_record(record, candidate,
  current_sources)` — kiểm `status`, `representation`, `schema_version`,
  `collection_name`, `qdrant` (tên vector, distance, `payload_schema_version`),
  `dense` khớp candidate, freshness theo `current_sources`. Không còn nhánh
  `migration`.
- Produces: sparse state dùng chung cho hai collection tại
  `data/full_corpus_builds/full_corpus_sparse_state.json`; runtime kiểm SHA-256
  file bằng `record["sparse"]["state_sha256"]` và
  `sparse_state.corpus_identity == record["corpus"]["identity"]`.

- [ ] **Step 1:** Xóa hằng số `EXPECTED_FILE_COUNT`, `EXPECTED_CHUNK_COUNT`,
  `EXPECTED_CORPUS_IDENTITY`, `EXPECTED_SPARSE_SHA256`, kiểm tra
  `vocabulary_size == 5662`, `PREFLIGHT_OUTPUT_PATH`, phụ thuộc
  `PHASE3_EVIDENCE_PATH` trong `prepare_full_corpus_input`, và mọi nơi import
  chúng (`grep -rn "EXPECTED_CORPUS_IDENTITY\|EXPECTED_CHUNK_COUNT\|EXPECTED_SPARSE_SHA256\|5662\|PREFLIGHT_OUTPUT_PATH" backend`).
- [ ] **Step 2:** `prepare_full_corpus_input()` chỉ còn: discover → hash
  sources → chunk (lỗi chunking thì raise) → `compute_corpus_identity` →
  `fit_sparse_state` → trả về chunks, sources, corpus identity, sparse state.
- [ ] **Step 3:** Runtime (`build_full_corpus_retrieval_service`) đọc build
  record của collection candidate, gọi `validate_full_corpus_build_record`, đọc
  sparse state và kiểm như Interfaces, rồi kiểm `points_count ==
  record["corpus"]["chunk_count"]`.
- [ ] **Step 4:** Cập nhật test bị ảnh hưởng. Giữ một test thuần (dữ liệu nhỏ
  hợp lệ) cho freshness: đổi hash một source → validate raise
  `ComponentNotReadyError`. Xóa test chỉ bảo vệ hằng số/preflight/migration.
- [ ] **Step 5:** Chạy:

```bash
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_retrieval.py tests/test_full_corpus_qdrant_ingestion.py -q
```

  Expected: PASS (test cần Qdrant/model thật chạy thật, không skip bằng mock).

### Task 5: Hai candidate và dense runner OpenRouter

**Files:**
- Modify: `backend/embedding/full_corpus.py` (spec, runner)
- Modify: `backend/ingestion/full_corpus_pipeline.py:66-118` (candidate list)
- Delete: `backend/ingestion/full_corpus_metadata_v2.py`,
  `backend/tests/test_full_corpus_metadata_v2.py`
- Modify: `backend/retrieval/full_corpus_smoke.py`, `backend/llm/phase6_live_smoke.py:110-138`,
  `backend/evaluation/full_corpus_embedding_preflight.py` (chỉ phần tham chiếu
  spec/candidate đã xóa)
- Modify: `pyproject.toml`, `uv.lock` (khai báo `httpx` trực tiếp bằng `uv add httpx`)
- Test: `backend/tests/test_full_corpus_embedding.py`

**Interfaces:**
- Produces: hai candidate duy nhất
  - `e5-small-384` → `hue_full_corpus_7a2_e5_small_384` (spec local hiện hành);
  - `qwen3-embedding-8b-4096` → `hue_full_corpus_7a2_qwen3_8b_4096`, dense spec
    có model `qwen/qwen3-embedding-8b`, dimension 4096, input contract `qwen3`,
    batch 64, đánh dấu provider OpenRouter.
- Produces: `FullCorpusCandidate` chỉ còn một tên collection
  (`collection_name`); bỏ `metadata_v2_collection_name` và mapping cũ.
- Produces: `OpenRouterDenseRunner` cùng các method runtime/build đang dùng:
  `load()`, `embed_documents_matrix(texts) -> np.ndarray`,
  `embed_queries(queries) -> list[list[float]]`, `close()`, và
  `providers_seen: set[str]`.
- Produces: một hàm chọn runner theo spec (local → `FullCorpusDenseRunner`,
  OpenRouter → `OpenRouterDenseRunner`), dùng ở build và runtime.

- [ ] **Step 1:** Viết test thuần cho phần không gọi mạng của runner: kiểm
  response hợp lệ được sắp theo `index`; thiếu vector, sai chiều hoặc `index`
  không đủ thì raise. Input là dict response nhỏ hợp lệ viết tay — đây là pure
  logic, không phải integration evidence.

```python
def test_parse_embeddings_response_orders_by_index_and_checks_dimension():
    body = {"provider": "Nebius", "data": [
        {"index": 1, "embedding": [0.0, 1.0]},
        {"index": 0, "embedding": [1.0, 0.0]},
    ]}
    vectors, provider = parse_embeddings_response(body, expected_count=2, dimension=2)
    assert vectors.tolist() == [[1.0, 0.0], [0.0, 1.0]]
    assert provider == "Nebius"

def test_parse_embeddings_response_rejects_wrong_dimension():
    body = {"provider": "Nebius", "data": [{"index": 0, "embedding": [1.0]}]}
    with pytest.raises(ValueError):
        parse_embeddings_response(body, expected_count=1, dimension=2)
```

- [ ] **Step 2:** Chạy test, xác nhận FAIL vì chưa có hàm.
- [ ] **Step 3:** Cài runner (minh họa; Implementer được tổ chức lại nếu giữ
  hành vi):

```python
OPENROUTER_EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"


def parse_embeddings_response(body: dict, expected_count: int, dimension: int) -> tuple[np.ndarray, str]:
    """Sắp vector theo index và kiểm số lượng/số chiều; sai thì raise."""
    rows = sorted(body["data"], key=lambda item: item["index"])
    if [item["index"] for item in rows] != list(range(expected_count)):
        raise ValueError("OpenRouter response index mismatch")
    matrix = np.asarray([item["embedding"] for item in rows], dtype=np.float32)
    if matrix.shape != (expected_count, dimension):
        raise ValueError(f"OpenRouter response shape {matrix.shape} != {(expected_count, dimension)}")
    return matrix, body["provider"]


class OpenRouterDenseRunner:
    """Gọi OpenRouter embeddings theo batch cố định; lỗi thì raise, không retry."""

    def __init__(self, spec: DenseModelSpec) -> None:
        self.spec = spec
        self.providers_seen: set[str] = set()
        self._client: httpx.Client | None = None

    def load(self) -> None:
        self._client = httpx.Client(
            timeout=180,
            headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        )

    def _embed(self, texts: Sequence[str]) -> np.ndarray:
        response = self._client.post(OPENROUTER_EMBEDDINGS_URL, json={
            "model": self.spec.model_id,
            "input": list(texts),
            "encoding_format": "float",
            "provider": {"data_collection": "deny"},
        })
        response.raise_for_status()
        matrix, provider = parse_embeddings_response(response.json(), len(texts), self.spec.dimension)
        self.providers_seen.add(provider)
        return matrix

    def embed_documents_matrix(self, texts: Sequence[str]) -> np.ndarray:
        prepared = [prepare_document(self.spec, text) for text in texts]
        batches = [prepared[i:i + self.spec.batch_size] for i in range(0, len(prepared), self.spec.batch_size)]
        return np.vstack([self._embed(batch) for batch in batches])

    def embed_queries(self, queries: Sequence[str]) -> list[list[float]]:
        return self._embed([prepare_query(self.spec, q) for q in queries]).tolist()

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
```

- [ ] **Step 4:** Chạy test runner: PASS.
- [ ] **Step 5:** Thu danh sách candidate còn hai; xóa spec e5-base, huydang,
  qwen-0.6B khỏi `DENSE_MODEL_SPECS`, xóa module/test metadata v2, sửa mọi
  import còn lại. `phase6_live_smoke` token checker chỉ dùng tokenizer local
  (`full_corpus.embedding_models` trong settings, như chunker), và
  `get_metadata_v2_point_count` đọc collection của candidate runtime thay cho
  tên cứng.
- [ ] **Step 6:** Kiểm không còn tham chiếu:

```bash
grep -rn "metadata_v2_collection_name\|full_corpus_metadata_v2\|hue_full_corpus_a_\|e5-base-768\|huydang-dek21-768\|qwen3-embedding-0.6b" backend
```

  Expected: không còn kết quả trong code (comment lịch sử trong test đã xóa
  cũng không còn).
- [ ] **Step 7:** Chạy:

```bash
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_embedding.py tests/test_phase6_live_smoke.py tests/test_phase6_settings.py -q
```

  Expected: PASS.

### Task 6: Một đường build thẳng

**Files:**
- Modify: `backend/ingestion/full_corpus_pipeline.py:203-451` (thay
  `run_read_only_preflight`/`build_candidate`/`main`)
- Test: `backend/tests/test_full_corpus_qdrant_ingestion.py`

**Interfaces:**
- Consumes: `prepare_full_corpus_input()` (Task 4), chọn runner (Task 5),
  `build_full_corpus_point_batch`, `create_full_corpus_collection`,
  `upsert_full_corpus_batch`, `verify_full_corpus_collection` hiện có.
- Produces: CLI `uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate <id>`.

- [ ] **Step 1:** `build_candidate(candidate_id)`:
  1. `prepare_full_corpus_input()`;
  2. ghi sparse state vào `data/full_corpus_builds/full_corpus_sparse_state.json`
     nếu chưa có; nếu đã có thì nội dung phải byte-identical, không thì raise;
  3. target collection phải chưa tồn tại (không ghi đè collection có sẵn);
  4. embed toàn bộ `search_text` bằng runner của candidate;
  5. kiểm source hash không đổi trong lúc embed;
  6. tạo collection, upsert theo batch 64, verify bằng
     `verify_full_corpus_collection`;
  7. ghi build record (Task 4) kèm `providers` = `sorted(runner.providers_seen)`
     với 8B;
  8. in tóm tắt JSON ra stdout (collection, số point, shape, norm min/max,
     providers, record path/SHA).
  Lỗi ở bất kỳ bước nào thì raise; không retry, không resume.
- [ ] **Step 2:** Xóa preflight Phase 4 và artifact path; chỉ giữ subcommand
  `build`.
- [ ] **Step 3:** Cập nhật test thuần bị ảnh hưởng; chạy:

```bash
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_full_corpus_qdrant_ingestion.py -q
```

### Task 7: Build thật hai index

**Paid:** OpenRouter tối đa 2 lần build đầy đủ cho 8B.

- [ ] **Step 1:** Build e5-small:

```bash
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate e5-small-384
```

- [ ] **Step 2:** Build 8B:

```bash
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline build --candidate qwen3-embedding-8b-4096
```

  Nếu lỗi: ghi lỗi thật; xóa đúng collection
  `hue_full_corpus_7a2_qwen3_8b_4096` vừa build dở (và record nếu đã ghi), rồi
  chạy lại một lần. Lỗi lần hai thì dừng và báo.
- [ ] **Step 3:** Verify thật cho mỗi collection (script tạm ngoài repo hoặc
  REPL `uv run`): point count = chunk count trong record; mọi payload đúng 7
  field; dense 384/4096 chiều; có sparse vector; mẫu 20 chunk rải 5 domain được
  embed lại thật và cosine với vector đã lưu ≥ 0,999 (min, mean ghi vào report).
  8B dùng tối đa 1 call cho mẫu này.

### Task 8: Cutover runtime và nghiệm thu end-to-end

**Paid:** `gpt-6-luna` đúng 5 call; OpenRouter query tối đa 50 call (tính cả
Task 7 Step 3).

- [ ] **Step 1:** `backend/config/settings.yaml` giữ `full_corpus_runtime.candidate_id:
  e5-small-384` (candidate này giờ trỏ `hue_full_corpus_7a2_e5_small_384`).
- [ ] **Step 2:** Health khởi động runtime thật, như evidence G6 của Phase 6:

```bash
cd /home/minhhieu/hue_rag/backend
uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8016
# terminal khác
curl -s http://127.0.0.1:8016/health
```

  Yêu cầu HTTP 200, mọi component ready (gồm retrieval đã qua freshness). Dừng
  server sau khi ghi kết quả.
- [ ] **Step 3:** Live smoke Phase 6, ghi ra file mới (không ghi đè artifact
  Phase 6):

```bash
cd /home/minhhieu/hue_rag
uv run --env-file .env python -m backend.llm.phase6_live_smoke \
  --cases data/full_corpus_phase_6_live_cases.json \
  --output data/full_corpus_phase_7a2_live_smoke.json --confirm-paid
```

  Nếu script đòi chạy từ `backend/` hoặc có kiểm hash/fingerprint gắn với
  Phase 6, chỉnh đúng phần đó để trỏ collection mới và ghi lại trong report;
  không đổi 5 case hay logic chấm. Đúng 5 call. So từng case với kết quả Phase 6
  (`reports/full_corpus_phase_6_gpt_6_luna_review_2026_10_23.md`): không tệ hơn
  4 PASS / 1 FAIL. Case regression ghi kèm root cause; không chạy lại.
- [ ] **Step 4:** Retrieval smoke 10 (script tạm ngoài repo, không commit): với
  mỗi index, build service bằng `build_full_corpus_retrieval_service` với
  profile runtime (`dense_bm25_rrf`, reranker `none`), chạy 10 câu trong
  `knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl`, K=10; ghi
  top-10 `source` và keyword nào xuất hiện trong top-10 text. Không ngưỡng.
- [ ] **Step 5:** Chạy focused suite bị ảnh hưởng:

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest tests/test_full_corpus_retrieval.py tests/test_full_corpus_qdrant_ingestion.py tests/test_full_corpus_embedding.py tests/test_phase6_live_smoke.py tests/test_phase6_settings.py tests/test_golden_full_corpus.py -q
cd .. && git diff --check
```

  Không chạy test có paid call ngoài giới hạn (ví dụ
  `test_llm_generator_openai.py`). Nếu cách chạy pytest từ repo root khác với
  từ `backend/`, dùng đúng cách Phase 6 implementation report đã dùng.

- [ ] **Step 6:** Report
  `reports/phase_7a2_gate_2_reindex_implementation_2026_10_23.md`: diff tóm
  tắt, lệnh, kết quả thật (số point, chiều, cos min/mean, providers 8B, số call
  OpenRouter/`gpt-6-luna` đã dùng, health, 5 case live smoke so với Phase 6,
  bảng retrieval smoke theo số dòng smoke — không chép câu hỏi/nội dung), lỗi
  và giới hạn. Chuyển handoff về `reviewer` (`final_review`) và nhắn Reviewer.

---

## Gate 3 — Dọn dẹp

Chỉ chạy sau khi User đóng Gate 2. Không đổi code.

### Task 9: Xóa 13 collection và file cũ

- [ ] **Step 1:** Ghi trạng thái trước: danh sách collection và point count của
  bốn collection được giữ.
- [ ] **Step 2:** Xóa đúng 13 collection trong spec §6.1, từng tên một:

```bash
for name in \
  hue_full_corpus_a_e5_small_384 hue_full_corpus_a_e5_small_384_metadata_v2 \
  hue_full_corpus_a_e5_base_768 hue_full_corpus_a_e5_base_768_metadata_v2 \
  hue_full_corpus_a_huydang_dek21_768 hue_full_corpus_a_huydang_dek21_768_metadata_v2 \
  hue_full_corpus_a_qwen3_06b_1024 hue_full_corpus_a_qwen3_06b_1024_metadata_v2 \
  hue_foods_08a_e5_small_384 hue_foods_08a_e5_base_768 hue_foods_08a_huydang_dek21_768 \
  hue_rag_phase8_08b_tfidf_v1_unicode_word_49c5d03359f9 \
  hue_rag_phase8_08b_tfidf_v1_unicode_word_5297c8604335; do
  curl -s -X DELETE "http://127.0.0.1:6335/collections/$name"; echo " $name"
done
```

- [ ] **Step 3:** Xóa 8 build record cũ `data/full_corpus_builds/hue_full_corpus_a_*.json`
  và `data/full_corpus_builds/phase_3_sparse_state.json`.
- [ ] **Step 4:** Kiểm sau: Qdrant còn đúng `hue_foods_e5_small_384`,
  `hue_foods_e5_small_384_dense`, `hue_full_corpus_7a2_e5_small_384`,
  `hue_full_corpus_7a2_qwen3_8b_4096`, point count không đổi;
  `data/full_corpus_builds/` chỉ còn hai record 7a2 và
  `full_corpus_sparse_state.json`; health runtime PASS.
- [ ] **Step 5:** Report
  `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_23.md`, chuyển
  handoff về `reviewer` (`final_review`) và nhắn Reviewer.

Backup Gate 1 được xóa trong closure khi User đóng Phase.

---

## Review Contract

**Risk level:** high — sửa dữ liệu đang chạy, provider mới, gửi corpus private ra
ngoài, xóa không hoàn tác.

| Gate | Implementer phải cung cấp | Reviewer kiểm độc lập tối thiểu | Reviewer chạy lại |
|---|---|---|---|
| 1 | Report Gate 1; backup; kết quả `check` trước/sau; danh sách dòng Golden đã sửa | Diff từng file sửa với backup (đúng 25 mục + dòng nguồn, không gì khác); đọc từng dòng Golden đã sửa cùng User; minimum diff gate | `check` hai file Golden; chunker đếm file/chunk |
| 2 | Report Gate 2; diff code; output build; verify; health; live smoke; retrieval smoke | Exact diff (không còn hằng số cứng/migration/tên cũ; đường build duy nhất; runner không retry/fallback; `data_collection: deny`); test thuần không mock dependency | Read-only: count + payload + chiều hai collection; đọc hai build record; health runtime. Không chạy lại paid call |
| 3 | Report Gate 3; trạng thái trước/sau | Danh sách collection còn lại đúng 4; record còn lại đúng 3 file | `GET /collections`; health runtime |

**Evidence reuse trong correction:** kết quả build/live smoke Gate 2 được reuse
nếu correction không đổi corpus, chunker, runner, build path hoặc retrieval;
phải ghi lý do. Correction đổi một trong các phần đó thì phải build/smoke lại
trong giới hạn paid còn lại, vượt giới hạn cần User cấp thêm.

**Cần quyền mới:** vượt giới hạn paid (§5.6 spec); xóa collection ngoài danh
sách; đổi chunker, payload, retrieval profile hoặc generation; cutover sang 8B;
commit/push.

**Closure:** sau mỗi gate, Reviewer ra verdict theo `REVIEWER_WORKFLOW.md`; User
xác nhận đóng gate. Sau Gate 3, Reviewer cập nhật `Project_Status.md`, guide
full-corpus và ghi chú Phase 8 (spec §7), xóa backup Gate 1 theo User xác nhận,
và đặt `CURRENT_HANDOFF.md` về `completed`.
