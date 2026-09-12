# Phase 3 Full-corpus Embedding và Sparse Representation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans`
> to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for
> tracking. User grants the lead Implementer discretion to use sub-agents under
> `session_prompt/IMPLEMENTER_WORKFLOW.md`; plan order and scope remain binding.

**Goal:** Kiểm chứng bốn dense embedding contracts trên một mẫu full-corpus nhỏ,
bắt buộc Qwen3-Embedding-0.6B chạy CUDA FP16 trên GTX 1650, và tạo sparse state
deterministic dùng chung cho Phase 4/5 mà chưa encode dense toàn corpus hay ghi Qdrant.

**Architecture:** Giữ đường Phase 3 tách khỏi Foods runtime: một module khai báo
và chạy dense candidates, một module sở hữu sparse state/BM25 vector contract,
và một CLI orchestration tạo artifact/evidence. CLI lấy fresh Representation A
từ Phase 2, tokenize toàn corpus nhưng chỉ dense-encode mẫu deterministic 10–15
chunks; các model được load và release tuần tự.

**Tech Stack:** Python 3.13, Sentence Transformers 5.6.1, Transformers 5.14.1,
PyTorch 2.13.0, PyVi 0.1.1, NumPy, pytest, Jupyter/nbconvert, JSON/SHA-256.

```text
Status: approved by User 2026-09-12
Written Spec: approved by User 2026-09-12
Implementation authorization: Phase 3 only through active handoff
Git authorization: none
Sub-agent authorization: user-standing; lead Implementer decides under workflow
Post-approval consistency correction: deterministic tests use no mock/fake/stub; scope, behavior, risk and authority unchanged
```

## Global Constraints

- Written Spec canonical:
  `docs/superpowers/specs/2026-09-12-phase-3-full-corpus-embedding-sparse-written-spec.md`.
- Tài liệu active/tương lai chỉ dùng `Phase`; chuỗi cũ chỉ được giữ khi nó là
  exact filename của artifact Phase 2 lịch sử đã đóng.
- Dependency là fresh Phase 2 output: observed baseline 205 files, 8.460 chunks,
  ba condition rules, zero errors/oversized groups; counts không được hard-code
  thành product invariant.
- Representation A phải là exact `FullCorpusChunk.search_text` do
  `build_representation_a_search_text()` tạo; không thêm renderer hoặc labels.
- Không sửa `backend/embedding/embedder.py`, Foods runtime/config/profile,
  Qdrant, Golden data, retrieval, reranker, generation, API hoặc frontend.
- Không dense-encode toàn corpus; chỉ tokenize toàn corpus với
  `truncation=False` và dense-encode một mẫu ordered 10–15 chunks.
- Bốn revisions/dimensions là exact; không đổi revision, device, dtype, batch,
  attention implementation, dimension hoặc input contract tự động.
- E5-small, E5-base và HuyDang chạy CPU/FP32; Qwen chạy CUDA/FP16, batch size 1,
  standard PyTorch eager attention, native 1024D.
- Qwen không có CPU fallback, quantization, FlashAttention, `device_map=auto`,
  `truncate_dim`, PCA, slicing hoặc batch auto-shrink.
- Qwen CUDA success là điều kiện Phase PASS. GPU/driver/CUDA/OOM failure phải
  được ghi evidence và trả `blocked`, không được biến thành model PASS.
- Sparse tokenizer tái sử dụng trực tiếp `backend.scoring.bm25.tokenize`, với
  `k1=1.5`, `b=0.75`, lexicographic vocabulary, query value `1.0`.
- Sparse state phải byte-identical cho cùng ordered chunks/config; không lưu
  8.460 sparse document vectors.
- Dense/GPU evidence không chứa vector values, corpus text, secrets hoặc absolute
  Hugging Face cache path.
- Model timings chỉ là diagnostic; cosine không có PASS threshold và không chọn winner.
- Notebook canonical phải có outputs rỗng và `execution_count: null`; Run All
  chỉ thực hiện trên copy trong `/tmp`.
- Git authorization là `none`: không commit, push, reset, clean hoặc stage file.
- Implementer tự quyết dùng sub-agent theo standing User authorization; lead
  giữ dependency order, giao disjoint ownership, kiểm kết quả và bàn giao Reviewer.

---

## File map

- Create `backend/embedding/full_corpus.py`: model specs, role preprocessing,
  exact snapshot resolution, tokenizer scan, sequential Sentence Transformers runner.
- Create `backend/embedding/sparse.py`: corpus identity, immutable sparse state,
  deterministic serialization, document/query vector construction.
- Create `backend/evaluation/full_corpus_embedding_preflight.py`: fresh Phase 2
  input, deterministic sample selection, GPU readiness, orchestration và JSON evidence CLI.
- Create `backend/tests/test_full_corpus_embedding.py`: deterministic spec,
  preprocessing and vector-validation tests using real pure inputs/dependencies;
  model construction/inference is verified by the real bounded run.
- Create `backend/tests/test_full_corpus_sparse.py`: formula, serialization,
  determinism, BM25 dot-product equivalence tests.
- Create `backend/tests/test_full_corpus_embedding_preflight.py`: sample,
  blocked/PASS aggregation, evidence redaction và CLI behavior tests.
- Modify `notebooks/03_embedding_models.ipynb`: Vietnamese bounded Phase 3
  walkthrough calling backend APIs only.
- Create during approved implementation:
  `data/full_corpus_builds/phase_3_sparse_state.json` (ignored generated state).
- Create during approved implementation:
  `reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json`.
- Create after verification:
  `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md`.
- Modify only at implementation handoff:
  `session_prompt/CURRENT_HANDOFF.md`.
- Modify `pyproject.toml` and `uv.lock` only under the conditional CUDA dependency
  gate in Task 5; no dependency edit is expected before that gate fires.

Immutable paths for before/after SHA-256 evidence:

- `backend/config/settings.yaml`;
- `backend/embedding/embedder.py`;
- `backend/embedding/dense_benchmark.py`;
- `backend/scoring/bm25.py`;
- `backend/ingestion/chunking/full_corpus_chunker.py`;
- `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`
  (preserved historical Phase 2 filename);
- all 205 discovered curated Markdown inputs;
- Foods Golden files and all existing `evaluation/results/` artifacts.

## Public interfaces locked by this plan

`backend.embedding.full_corpus` produces:

```python
@dataclass(frozen=True)
class DenseModelSpec:
    key: str
    model_id: str
    revision: str
    dimension: int
    max_tokens: int
    input_contract: Literal["e5", "pyvi", "qwen3"]
    device: Literal["cpu", "cuda"]
    dtype: Literal["float32", "float16"]
    batch_size: int

DENSE_MODEL_SPECS: tuple[DenseModelSpec, ...]
QWEN_QUERY_TASK: str

def prepare_document(spec: DenseModelSpec, text: str) -> str: ...
def prepare_query(spec: DenseModelSpec, query: str) -> str: ...
def resolve_snapshot(spec: DenseModelSpec, allow_download: bool) -> Path: ...
def count_tokens(tokenizer: Any, prepared_text: str) -> int: ...

class FullCorpusDenseRunner:
    def __init__(self, spec: DenseModelSpec, snapshot_path: Path): ...
    def load(self) -> None: ...
    def tokenizer(self) -> Any: ...
    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...
    def embed_queries(self, queries: Sequence[str]) -> list[list[float]]: ...
    def runtime_identity(self) -> dict[str, object]: ...
    def close(self) -> None: ...
```

`backend.embedding.sparse` produces:

```python
@dataclass(frozen=True)
class SparseVector:
    indices: tuple[int, ...]
    values: tuple[float, ...]

@dataclass(frozen=True)
class SparseState:
    schema_version: str
    corpus_identity: str
    document_count: int
    average_document_length: float
    k1: float
    b: float
    tokenizer: str
    vocabulary: tuple[str, ...]
    idf: tuple[float, ...]

def compute_corpus_identity(chunks: Sequence[FullCorpusChunk]) -> str: ...
def fit_sparse_state(chunks: Sequence[FullCorpusChunk]) -> SparseState: ...
def encode_sparse_document(text: str, state: SparseState) -> SparseVector: ...
def encode_sparse_query(query: str, state: SparseState) -> SparseVector: ...
def serialize_sparse_state(state: SparseState) -> bytes: ...
def write_sparse_state(state: SparseState, path: Path) -> str: ...
def load_sparse_state(path: Path) -> SparseState: ...
```

`backend.evaluation.full_corpus_embedding_preflight` produces:

```python
P7_ORDER: tuple[str, ...]
SMOKE_QUERIES: tuple[str, ...]

def classify_chunk(chunk: FullCorpusChunk) -> frozenset[str]: ...
def select_dense_sample(
    chunks: Sequence[FullCorpusChunk],
    longest_by_model: Mapping[str, str],
    minimum: int = 10,
    maximum: int = 15,
) -> list[FullCorpusChunk]: ...
def inspect_cuda() -> dict[str, object]: ...
def derive_status(component_statuses: Mapping[str, str]) -> str: ...
def run_preflight(
    sparse_output: Path,
    evidence_output: Path,
    allow_downloads: bool = False,
) -> tuple[dict[str, object], int]: ...
```

## Review Contract

**Risk level:** `high`. Triggers: real model resolution/download and inference,
CUDA/VRAM observation, embedding/scoring contract, durable sparse/evidence
artifacts, conditional dependency lock change và notebook execution.

**Required Implementer evidence:**

1. exact base/head/worktree state before and after, including every untracked path;
2. focused RED/GREEN commands for Tasks 1–4 and complete backend regression result;
3. exact snapshot IDs and resolved revisions for all four models, without absolute cache paths;
4. Windows `nvidia-smi`, WSL `/usr/lib/wsl/lib/nvidia-smi`, project Torch/CUDA
   identity, GTX 1650 identity and VRAM readings;
5. per-model prepared-role assertions, full-corpus max/over-limit counts,
   bounded sample IDs, shapes, dimensions, finite/norm ranges and diagnostic timings;
6. Qwen proof: CUDA parameter device, FP16 parameter dtype, batch 1, eager
   attention, native 1024D, document raw Representation A and exact query instruction;
7. sparse state schema/count/vocabulary/hash, two-generation byte comparison,
   round-trip equality and selected BM25 dot-product equality;
8. canonical JSON structural/redaction checks proving no vector values, corpus
   text, secrets or absolute cache paths;
9. temporary Notebook 03 Run All command/result plus canonical notebook
   `outputs=[]` and null execution counts;
10. before/after hashes for every immutable path group, exact deviations,
    failures/skips/limitations and acceptance mapping in the implementation report.

**Minimum independent Reviewer checks:** resolve base/head and complete worktree;
read every changed/untracked path and exact diff; map it to spec/plan; inspect
Qwen device/dtype/attention checks and all no-fallback branches; inspect sparse
formula and deterministic serialization; validate evidence schema/sample size,
artifact hashes, notebook cleanliness and immutable-path hashes; run
`git diff --check`.

**Exact independent Reviewer reruns from repository root:**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  -q --tb=short
```

Expected: focused deterministic tests PASS without network, model load, CUDA,
Qdrant or notebook execution.

```bash
git diff --check
```

Expected: no output. Per User direction, Reviewer does not repeat heavy model
downloads/inference, GPU smoke, full tokenizer scan or Notebook Run All; those
remain Implementer evidence and are audited against machine-readable artifacts.

**Correction evidence eligible for reuse:** unchanged deterministic test logs;
unchanged exact snapshot resolution; immutable hashes; sparse bytes/hash when
corpus identity and sparse code are unchanged; GPU identity only while Windows
driver, WSL kernel, Torch lock and device remain unchanged. Dense inference,
VRAM, notebook or tokenizer evidence must be rerun if its model code, revision,
preprocessing, dependency, corpus identity or environment changes.

**New User authority required:** Windows/Administrator action; Git write;
Qdrant read/write; dense full-corpus encoding; new collection/index; alternate
model/revision/dimension/device/dtype; CPU fallback/quantization/FlashAttention;
dependency change other than the narrow Task 5 gate; raw corpus, Foods runtime,
Golden/evaluation change; cleanup/cutover; paid API; scope expansion.

**Closure fields:** Reviewer records technical verdict (`PASS`, `PASS WITH
LIMITATIONS`, `BLOCKED`, `FAIL`), remaining risks, deviations, observed artifact
identities and exact next gate. Only User can approve Phase 3 closure and permit
Phase 4 design.

---

### Task 1: Dense model contracts và role preprocessing

**Files:**

- Create: `backend/embedding/full_corpus.py`
- Create: `backend/tests/test_full_corpus_embedding.py`

**Interfaces:**

- Consumes: `SentenceTransformer`, `huggingface_hub.snapshot_download`,
  `pyvi.ViTokenizer`, NumPy and Torch.
- Produces: all `backend.embedding.full_corpus` interfaces listed above for Task 3.

- [ ] **Step 1: Write contract/preprocessing tests that fail before the module exists**

Create tests with these exact assertions:

```python
def test_dense_specs_are_exact_and_ordered():
    assert [(s.key, s.model_id, s.revision, s.dimension, s.max_tokens,
             s.device, s.dtype, s.batch_size) for s in DENSE_MODEL_SPECS] == [
        ("e5-small-384", "intfloat/multilingual-e5-small",
         "614241f622f53c4eeff9890bdc4f31cfecc418b3", 384, 512,
         "cpu", "float32", 8),
        ("e5-base-768", "intfloat/multilingual-e5-base",
         "d128750597153bb5987e10b1c3493a34e5a4502a", 768, 512,
         "cpu", "float32", 8),
        ("huydang-dek21-768", "CODE4LIFEOFFICIAL/huydang-dek21-embedding",
         "517f1af7dd04a57194f1de2990f0c6ede0a3109b", 768, 256,
         "cpu", "float32", 8),
        ("qwen3-embedding-0.6b-1024", "Qwen/Qwen3-Embedding-0.6B",
         "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3", 1024, 32768,
         "cuda", "float16", 1),
    ]

def test_role_preprocessing_is_exact():
    e5, _, huydang, qwen = DENSE_MODEL_SPECS
    assert prepare_document(e5, "Văn bản") == "passage: Văn bản"
    assert prepare_query(e5, "Câu hỏi") == "query: Câu hỏi"
    assert prepare_document(huydang, "Văn bản") == ViTokenizer.tokenize("Văn bản")
    assert prepare_query(huydang, "Câu hỏi") == ViTokenizer.tokenize("Câu hỏi")
    assert prepare_document(qwen, "Văn bản") == "Văn bản"
    assert prepare_query(qwen, "Câu hỏi") == (
        "Instruct: Given a Vietnamese question about Hue culture, heritage, "
        "festivals, performing arts, food, and travel, retrieve relevant "
        "Vietnamese passages that answer the question.\nQuery: Câu hỏi"
    )
```

Also assert empty/whitespace input raises `ValueError`, unknown input contract
raises `ValueError`, and `count_tokens()` calls tokenizer with
`add_special_tokens=True, truncation=False`.

- [ ] **Step 2: Run the focused test and observe RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest backend/tests/test_full_corpus_embedding.py -q --tb=short
```

Expected RED: import failure for `backend.embedding.full_corpus`.

- [ ] **Step 3: Implement immutable model specs and preprocessing**

Use one frozen dataclass and the four exact values above. Implement the role
branches directly. Define the Qwen task text as one string and render exactly
`Instruct: {QWEN_QUERY_TASK}\nQuery: {query}`. Do not place any of these candidates
in active `settings.yaml` or `E5Embedder`.

- [ ] **Step 4: Add exact snapshot path validation and implementation**

Implement `resolve_snapshot()` with this exact call:

```python
{
    "repo_id": spec.model_id,
    "revision": spec.revision,
    "local_files_only": not allow_download,
}
```

Resolve the returned path and verify the snapshot directory name equals the
40-character revision. A missing/mismatched snapshot raises a clear exception;
never pick the newest cached snapshot. Deterministic tests exercise the returned
path/revision validator with temporary directory names only; Task 5 verifies the
real `snapshot_download` call and four actual cache snapshots. Do not replace
Hugging Face with a fake client.

- [ ] **Step 5: Test pure validation and implement the sequential runner**

Test vector validation directly with small NumPy arrays for wrong count,
dimension, non-finite values and non-unit norm. Implement the runner so source
inspection and Task 5 real evidence verify:

- CPU candidates construct with `device="cpu"`; Qwen with `device="cuda"`;
- Qwen passes `model_kwargs={"torch_dtype": torch.float16,
  "attn_implementation": "eager"}` and no `device_map`;
- output order/count/dimension, finite values and norm `pytest.approx(1, abs=1e-4)`;
- Qwen parameter device is CUDA and dtype is FP16; CPU parameters are CPU/FP32;
- document/query encoding uses `normalize_embeddings=True`,
  `convert_to_numpy=True`, `show_progress_bar=False` and exact batch size;
- `close()` drops the model, calls `gc.collect()`, and only then empties CUDA cache.

Validation failure must raise; it must not retry with altered parameters.
Do not use a mocked/fake/stub Sentence Transformer in tests. The real bounded
four-model run in Task 5 is the integration proof for construction, device,
dtype, arguments and lifecycle.

- [ ] **Step 6: Run GREEN and static diff check**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest backend/tests/test_full_corpus_embedding.py -q --tb=short
git diff --check
```

Expected: all Task 1 tests PASS; diff check has no output.

---

### Task 2: Deterministic sparse state và BM25-equivalent vectors

**Files:**

- Create: `backend/embedding/sparse.py`
- Create: `backend/tests/test_full_corpus_sparse.py`

**Interfaces:**

- Consumes: `FullCorpusChunk`, `backend.scoring.bm25.tokenize`, `K1`, `B`.
- Produces: `SparseState`, serialization and document/query encoding APIs for Task 3 and Phase 4/5.

- [ ] **Step 1: Write failing formula and vocabulary tests**

Build three minimal `FullCorpusChunk` objects whose `search_text` values are
`"bún bò huế"`, `"bún hến"`, and `""`. Assert:

```python
state = fit_sparse_state(chunks)
assert state.document_count == 2
assert state.average_document_length == pytest.approx(2.5)
assert state.k1 == 1.5
assert state.b == 0.75
assert state.tokenizer == "backend.scoring.bm25.tokenize:v1"
assert state.vocabulary == tuple(sorted({"bún", "bò", "huế", "hến"}))
assert len(state.idf) == len(state.vocabulary)
```

Also assert no non-empty document raises `ValueError`, duplicate chunk IDs raise,
and corpus order changes `corpus_identity`.

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest backend/tests/test_full_corpus_sparse.py -q --tb=short
```

Expected RED: import failure for `backend.embedding.sparse`.

- [ ] **Step 3: Implement state fitting and corpus identity**

Compute identity from UTF-8 canonical JSON of the ordered list
`[{"chunk_id": ..., "search_text": ...}, ...]` using
`ensure_ascii=False`, `sort_keys=True`, separators `(",", ":")`, then SHA-256.
Fit only non-empty tokenized documents. Build document frequency from unique
terms per document, sort terms lexicographically, and compute:

```python
math.log((n - df + 0.5) / (df + 0.5) + 1.0)
```

Do not read private fields from `BM25`; both implementations share only the
public tokenizer and the locked constants/formula.

- [ ] **Step 4: Test and implement document/query vectors**

Document indices are vocabulary indices in ascending order. Each value is:

```python
idf * tf * (state.k1 + 1.0) / (
    tf + state.k1 * (
        1.0 - state.b + state.b * document_length / state.average_document_length
    )
)
```

Query terms are deduplicated, unknown terms omitted, indices sorted, and every
value equals `1.0`. Assert exact empty-vector behavior for empty/OOV input.
For multiple corpus/query/document cases assert:

```python
dot = sum(dict(zip(doc.indices, doc.values)).get(i, 0.0) * value
          for i, value in zip(query.indices, query.values))
assert dot == pytest.approx(BM25().fit(corpus).score(query_text, document_text))
```

- [ ] **Step 5: Test and implement deterministic serialization**

Serialize `SparseState` only, with aligned vocabulary/IDF arrays, using
`json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"`.
Write through a sibling temporary file and `Path.replace()`. Return SHA-256 of
written bytes. Loader rejects unknown schema version, non-lexicographic vocab,
length mismatch, non-finite IDF, wrong constants and malformed identity.

Assert two writes produce identical bytes/SHA-256 and load→serialize preserves
the exact bytes. Assert serialized bytes do not contain any document vector.

- [ ] **Step 6: Run GREEN and regression for existing BM25**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_sparse.py backend/tests/test_bm25.py \
  -q --tb=short
git diff --check
```

Expected: Task 2 and existing BM25 tests PASS; diff check has no output.

---

### Task 3: Deterministic sample, CUDA gate và evidence orchestration

**Files:**

- Create: `backend/evaluation/full_corpus_embedding_preflight.py`
- Create: `backend/tests/test_full_corpus_embedding_preflight.py`

**Interfaces:**

- Consumes: Task 1 dense APIs, Task 2 sparse APIs,
  `chunk_full_corpus()` and `FullCorpusChunk`.
- Produces: `run_preflight()` and CLI used by Task 5 and Notebook 03.

- [ ] **Step 1: Write failing deterministic sample tests**

Create synthetic chunks across the seven exact partitions:

```python
P7_ORDER == (
    "foods", "heritages", "festivals", "performing_arts",
    "travel_places", "travel_services", "travel_tickets",
)
```

`classify_chunk()` returns any matching tags from `paragraph`, `list`, `table`,
`condition`: table when an evidence part has role `header`; condition when role
is `condition`; list when an evidence text has a Markdown list-item line;
paragraph for a body chunk without table/list markers.

`select_dense_sample()` must choose, in stable order:

1. first chunk by `chunk_id` for each P7;
2. first chunk for each missing content tag;
3. every per-model longest chunk supplied by tokenizer scan;
4. lexicographic fill until 10 chunks;
5. fail closed if coverage requires more than 15 or any P7/tag/longest ID is absent.

Assert same shuffled input produces identical ordered IDs, sample length is
10–15, all P7/tags/longest IDs are covered, and duplicate selections collapse.

- [ ] **Step 2: Write pure status aggregation and evidence-redaction tests**

Pass literal component-status dictionaries to `derive_status()` and literal
JSON-safe evidence dictionaries to the redaction validator. Assert all of the
following without replacing a model, tokenizer, CUDA, chunker or Hugging Face
dependency:

- fresh Phase 2 errors make final status `BLOCKED_PHASE_2` and no model runs;
- CUDA unavailable maps to final status `BLOCKED_GPU` and exit code 1;
- one over-limit item records count/ID and returns `BLOCKED_TOKEN_LIMIT`;
- Qwen OOM or wrong dtype/device status maps to `BLOCKED_QWEN`;
- CPU model failure status maps to `FAILED_MODEL`;
- all contracts satisfied returns `PASS`, exit code 0;
- JSON has no `vectors`, `search_text`, source text, environment values,
  authorization headers, tokens or absolute cache paths.

Actual no-retry/no-fallback behavior is verified by reading the direct control
flow and by the real Task 5 result; tests do not manufacture dependency failures.

- [ ] **Step 3: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding_preflight.py -q --tb=short
```

Expected RED: module/functions are missing.

- [ ] **Step 4: Implement GPU inspection**

`inspect_cuda()` returns JSON-safe fields only:

```python
{
    "torch_version": torch.__version__,
    "torch_cuda_version": torch.version.cuda,
    "cuda_available": torch.cuda.is_available(),
    "device_count": torch.cuda.device_count(),
    "device_index": 0,
    "device_name": torch.cuda.get_device_name(0),
    "total_vram_bytes": torch.cuda.get_device_properties(0).total_memory,
}
```

If unavailable, omit device-only fields and record a sanitized error. Reject a
device name that does not contain `GTX 1650`. Do not mutate drivers or call a
fallback device.

- [ ] **Step 5: Implement fresh corpus, sparse state and tokenizer scan**

Resolve all four exact snapshots first and load tokenizers from those snapshot
paths. Construct the Phase 2 fit checker from the first three exact specs only;
Qwen's 32K limit must not change closed Phase 2 chunk boundaries. Call
`chunk_full_corpus(is_fits_tokenizer_fn=phase_2_checker)` and require no errors,
unique IDs and a non-empty ordered result.

Load the preserved historical Phase 2 preview artifact named in the File map.
Require its status `PASS`, exact source list, file/chunk/condition counts and the
first three tokenizer maxima to equal the fresh results. Derive expected values
from that artifact rather than hard-coding 205/8.460 in runtime code. A mismatch
returns `BLOCKED_PHASE_2` before dense inference.

Fit sparse state, serialize twice (one temporary, one target), and require byte
equality before recording its SHA-256. For each of the four tokenizers, prepare
every document with `prepare_document()`, count with special tokens and
`truncation=False`, and retain only aggregate max, max chunk ID and over-limit
count/IDs. Scan all three fixed queries through each model's query preprocessing
as well. Qwen queries use the exact instruction; Qwen documents have no
instruction. Any over-limit input blocks before dense inference.

- [ ] **Step 6: Implement bounded sequential dense inference**

Use these fixed smoke queries:

```python
SMOKE_QUERIES = (
    "Đại Nội Huế có những điểm tham quan nào?",
    "Lễ hội truyền thống ở Huế thường diễn ra khi nào?",
    "Tôi nên ăn món gì và di chuyển thế nào khi du lịch Huế?",
)
```

Select 10–15 documents after tokenizer maxima are known. For each model in
`DENSE_MODEL_SPECS`, construct one runner, load, encode selected documents and
three queries, record shapes/norm min/max and elapsed diagnostics, then close in
`finally` before continuing. Vectors exist only in memory and are discarded.

Before Qwen inference call `torch.cuda.reset_peak_memory_stats(0)`; record
allocated/reserved after load and peak after inference. Require the runner's
parameter device/dtype to be CUDA/FP16 and output dimension 1024. Never catch an
error to rerun with another setting.

- [ ] **Step 7: Implement deterministic/sanitized evidence writing and CLI**

CLI arguments are exact:

```text
--sparse-output data/full_corpus_builds/phase_3_sparse_state.json
--evidence-output reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json
--allow-downloads
```

Evidence schema contains `schema_version`, `status`, `corpus`, `sample`,
`queries`, `models`, `gpu`, `sparse`, `errors`; each model includes exact ID,
revision, input contract, dimension, max tokens, device/dtype/batch, tokenizer
aggregates and smoke aggregates. Each sample row contains only ordered index,
chunk ID, source, heading path, coverage tags and per-model token counts; it does
not contain `search_text` or evidence text. Write evidence even on blocked/failure
and exit non-zero. Sanitize exception text to model/component/error class; do
not dump traceback, environment, cache path or input content into JSON.

- [ ] **Step 8: Run GREEN and combined focused suite**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  backend/tests/test_bm25.py \
  -q --tb=short
git diff --check
```

Expected: all focused deterministic tests PASS without model/network/CUDA;
diff check has no output.

---

### Task 4: Notebook 03 bounded learning path

**Files:**

- Modify: `notebooks/03_embedding_models.ipynb`

**Interfaces:**

- Consumes: Task 1 specs/preprocessing, Task 2 sparse state summary and Task 3
  `run_preflight()`/canonical evidence.
- Produces: a clean Vietnamese notebook that exercises the same backend path.

- [ ] **Step 1: Replace Foods/full-encoding narrative and duplicated operations**

The notebook must have these sections:

1. Phase 3 scope and explicit exclusions;
2. four-model contract table from `DENSE_MODEL_SPECS`;
3. Representation A and document/query preprocessing examples;
4. bounded preflight invocation using `/tmp` outputs and
   `allow_downloads=False`;
5. tokenizer/sample/dense/GPU summary without vectors;
6. sparse state/BM25 dot-product demonstration through backend functions;
7. handoff statement: dense full-corpus encoding and Qdrant belong to Phase 4.

Delete the old 572-Foods full encoding cells and remote-model statement. Do not
copy model/sparse algorithms into notebook cells.

- [ ] **Step 2: Add a structural notebook test**

In `backend/tests/test_full_corpus_embedding_preflight.py`, parse the canonical
notebook JSON and assert all code cells have `execution_count is None`, outputs
equal `[]`, backend Phase 3 imports exist, and forbidden calls/text are absent:
`chunk_foods_markdown`, `E5Embedder`, Qdrant clients, full-corpus dense loops,
OpenRouter and vector dumps.

- [ ] **Step 3: Run structural tests without executing the notebook**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding_preflight.py -q --tb=short
git diff --check
```

Expected: structural tests PASS; canonical notebook remains clean.

---

### Task 5: Host/WSL CUDA gate, exact models and real bounded run

**Files:**

- Create when successful: `data/full_corpus_builds/phase_3_sparse_state.json`
- Create/update on every attempt:
  `reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json`
- Conditional only: modify `pyproject.toml`, `uv.lock`

**Interfaces:**

- Consumes: Tasks 1–4 and User-controlled Windows host.
- Produces: real Phase 3 machine-readable evidence or an honest blocked artifact.

- [ ] **Step 1: Capture Linux-side precondition without changing the host**

```bash
/usr/lib/wsl/lib/nvidia-smi
UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache uv run python -c \
'import json, torch; print(json.dumps({"torch": torch.__version__, "torch_cuda": torch.version.cuda, "available": torch.cuda.is_available(), "count": torch.cuda.device_count()}))'
```

Expected before User repair may be `GPU access blocked by the operating system`.
Record it as `BLOCKED_GPU`; do not install an NVIDIA Linux display driver.

- [ ] **Step 2: Give the User the exact Administrator PowerShell sequence**

The Implementer asks the User to run:

```powershell
nvidia-smi
wsl --update
wsl --shutdown
```

If Windows `nvidia-smi` fails or does not recognize the GTX 1650, the
Implementer points the User to NVIDIA's official driver download/support page
and asks the User to install the current supported Windows Game Ready or Studio
driver, then reboot. The Implementer must not guess a version from a third-party
site and must not perform the installation itself. Primary references:

- `https://docs.nvidia.com/cuda/wsl-user-guide/`;
- `https://www.nvidia.com/Download/index.aspx`;
- `https://learn.microsoft.com/en-us/windows/wsl/basic-commands`.

After Windows `nvidia-smi` identifies the GTX 1650 and WSL restarts, ask the
User to run in ordinary PowerShell:

```powershell
wsl -d Ubuntu-24.04 -- /usr/lib/wsl/lib/nvidia-smi
```

The Implementer waits for the User's result; it does not perform host mutation.

- [ ] **Step 3: Recheck WSL and project Torch after host repair**

Repeat Step 1 and additionally run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache uv run python -c \
'import torch; assert torch.cuda.is_available(); p=torch.cuda.get_device_properties(0); print(torch.cuda.get_device_name(0), p.total_memory)'
```

Expected: `torch.cuda.is_available()` true, device name contains `GTX 1650`, and
reported VRAM corresponds to the physical 4 GB class device. Otherwise stop
with `BLOCKED_GPU`.

- [ ] **Step 4: Apply the narrow dependency gate only if passthrough works but Torch does not**

First preserve hashes:

```bash
sha256sum pyproject.toml uv.lock
```

Because the exact compatible replacement cannot be known before the observed
driver/runtime mismatch, do not guess or run an unconstrained upgrade. Report
`torch.__version__`, `torch.version.cuda`, driver output and
`uv tree --package torch`; request User approval for one exact proposed `uv`
command/version. Until
that approval, Phase remains `BLOCKED_GPU`. Never use `pip` or another environment.

- [ ] **Step 5: Resolve/download the four exact snapshots**

Only after CUDA readiness, run the approved CLI with downloads enabled; its
resolver must pass each exact revision to Hugging Face. Public downloads are
authorized by approval of this plan, but no token value may be printed:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache uv run python -m \
backend.evaluation.full_corpus_embedding_preflight \
  --sparse-output data/full_corpus_builds/phase_3_sparse_state.json \
  --evidence-output reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json \
  --allow-downloads
```

Expected PASS conditions: exit 0; four exact revisions; Qwen CUDA/FP16/batch 1/
1024D; all tokenizer over-limit counts zero; sample 10–15; sparse artifact
written with repeated-byte equality. Any other result remains blocked/failed.

- [ ] **Step 6: Repeat offline to prove cached exact resolution**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m backend.evaluation.full_corpus_embedding_preflight \
  --sparse-output data/full_corpus_builds/phase_3_sparse_state.json \
  --evidence-output reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json
```

Expected: exit 0 and the same corpus identity, sample IDs, model revisions,
token maxima and sparse SHA-256. Timings/VRAM are diagnostic and may differ.

- [ ] **Step 7: Run Notebook 03 only as a temporary copy**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache uv run jupyter nbconvert \
  --execute --to notebook notebooks/03_embedding_models.ipynb \
  --output /tmp/03_embedding_models-phase3-run.ipynb \
  --ExecutePreprocessor.timeout=1800
```

Expected: exit 0 using cached snapshots and the bounded backend path; only the
`/tmp` copy contains outputs.

- [ ] **Step 8: Verify artifact and canonical notebook hygiene**

```bash
jq '{status, corpus, sample_count:(.sample|length), models, gpu, sparse, errors}' \
  reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json
jq '[.cells[] | select(.cell_type=="code") | {execution_count, outputs}]' \
  notebooks/03_embedding_models.ipynb
rg -n 'vectors|search_text|Bearer|api[_-]?key|/home/' \
  reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json
```

Expected: status `PASS`; sample count 10–15; four model summaries; Qwen GPU
proof; no errors; canonical code cells null/empty; final `rg` has no output.

---

### Task 6: Regression, immutable evidence và Reviewer handoff

**Files:**

- Create: `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md`
- Modify: `session_prompt/CURRENT_HANDOFF.md`

**Interfaces:**

- Consumes: all task logs/artifacts and the Review Contract.
- Produces: auditable implementation report and one exact Reviewer/final_review handoff.

- [ ] **Step 1: Run focused and complete backend verification**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  backend/tests/test_bm25.py -q --tb=short

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-implementer-uv-cache \
uv run python -m pytest backend/tests -q --tb=short

git diff --check
```

Expected: focused suite and full backend suite PASS; diff check has no output.
If a pre-existing unrelated test fails, record exact command/failure and prove
the focused Phase 3 suite still passes; do not relabel the full suite PASS.

- [ ] **Step 2: Prove immutable paths and no Qdrant/data expansion**

Compare before/after SHA-256 manifests for the immutable paths in the File map.
Also run:

```bash
git status --short
git diff --name-only
git ls-files --others --exclude-standard
```

Expected: only approved Phase 3 paths plus the eight known pre-existing
untracked research files appear. No Qdrant collection command is run and no
dense vector artifact exists.

- [ ] **Step 3: Write the implementation report**

The report must contain:

- base/head/worktree and separation of pre-existing changes;
- changed-file responsibility map;
- every acceptance criterion mapped to observed evidence;
- exact commands and exit states, including both real preflight runs;
- model revisions, preprocessing, shapes/norms/token maxima and GPU/VRAM summary;
- sparse identity/hash/determinism/BM25-equivalence summary;
- notebook temporary execution and canonical cleanliness;
- immutable hashes, deviations, failed/skipped/not-verified items;
- technical self-verdict without claiming User closure or Phase 4 authorization.

- [ ] **Step 4: Update the active handoff for Reviewer final review**

Set `Target role: reviewer`, `Handoff kind: final_review`, exact base/head, risk
`high`, Review Contract path/section, changed files, artifact/report pointers,
test results, known eight pre-existing untracked files, deviations and stop
condition. Keep Git authorization `none` and preserve the User's standing
sub-agent authorization in the handoff.

- [ ] **Step 5: Stop**

Do not update canonical guide/status, start Phase 4 design, encode full-corpus
dense vectors, create Qdrant collections, commit or push. Reviewer performs the
independent gate and asks User for Phase 3 closure.

---

## Plan approval effect

Approval of this Plan and Review Contract authorizes one Implementer-led effort
for the exact Phase 3 files, tests, public model downloads and bounded local
execution above. The lead may use sub-agents under the standing User
authorization while preserving plan order and scope. It does not authorize
Windows host mutation by the Implementer, conditional dependency edits without
the resolved exact-version approval in Task 5, Git write, Qdrant, dense
full-corpus encoding, Phase 4 work, paid APIs, cleanup or production cutover.
