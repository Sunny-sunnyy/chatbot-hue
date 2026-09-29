# Full-corpus Metadata v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking. Do not dispatch sub-agents unless the
> User grants that authority separately.

**Goal:** Implement the approved seven-field Full-corpus metadata contract,
build four isolated metadata-v2 collections by copying verified vectors, and
cut retrieval over only after separate write and cutover approvals.

**Architecture:** Canonical chunks derive one validated five-value domain and
serialize an exact seven-field payload. A dedicated migration CLI pairs each
legacy collection with one fixed metadata-v2 target, regenerates payload from
fresh chunks, copies dense+sparse vectors without loading an embedding model,
and writes a v2 build record only after complete verification. Retrieval later
switches to the v2 collections, validates source freshness at startup and maps
Qdrant point UUIDs to logical chunk IDs at the result boundary.

**Tech Stack:** Python 3.13, qdrant-client 1.19.0, Qdrant v1.18.3, NumPy,
pytest, deterministic JSON and SHA-256; no new dependency.

```text
Status: approved by User 2026-09-29 +07
Written Spec: approved by User 2026-09-29 +07
Risk: high
Implementation authorization: Gate 1 / Tasks 1–4 approved by User 2026-09-29 +07
Legacy Full-corpus collections: read-only
Foods MVP collections/runtime: read-only and out of scope
Live-write authorization: separate Gate 2 approval required
Runtime cutover authorization: separate Gate 3 approval required
Collection deletion/replacement/cleanup: none
Dense embedding or paid model/API execution: none
Git authorization: none
```

## Global Constraints

- Canonical Written Spec:
  `docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md`.
- Baseline commit is
  `92f2e2cce0e85c9b4f733aaab038bc99cad314c0`; preserve all unrelated staged,
  unstaged and untracked User changes.
- Canonical inventory remains `205` files and `8.460` Representation A chunks;
  source text is UTF-8 strict with CRLF/CR normalized to LF before SHA-256.
- Product domains are exactly `foods`, `heritages`, `festivals`,
  `performing_arts`, `travel`; first `source` path component is their only
  source of truth.
- Payload v2 has exactly `search_text`, `source`, `title`, `heading_path`,
  `evidence_parts`, `chunk_id`, `domain`; missing or extra fields fail closed.
- Qdrant point ID remains
  `uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")`.
- Build schema is `phase_4_full_corpus_build:v2`; Qdrant payload schema is
  `full_corpus_qdrant_payload:v2`.
- Legacy build records remain v1 and immutable. A migration-only validator may
  read their exact five-field payload; runtime v2 must not accept it.
- Reuse exact dense+sparse vectors from the matching legacy point. Do not load
  `FullCorpusDenseRunner`, encode dense text, refit sparse state or call any
  external model/API.
- Keep Phase 3 sparse state schema/hash/vocabulary unchanged. Do not recompute
  or replace the state artifact.
- Create no payload index, alias, collection registry service, dual-read,
  dual-write, retry/resume/rollback framework or automatic cleanup.
- Baseline retrieval remains unfiltered. `domain` never filters, boosts, fuses
  or reranks in this workstream.
- Full-corpus Golden remains four fields. Public Phase 6 request/response and
  source-card contracts remain unchanged.
- Detailed point/vector/source evidence stays ignored under `data/`; tracked
  artifacts contain only allowlisted configuration, counts, hashes, statuses
  and sanitized errors.
- No code task may write Qdrant before Gate 2. No runtime candidate mapping may
  switch to metadata-v2 collections before Gate 3.
- Do not edit `knowledge-base-hue/`, `.gitignore`, `qdrant_storage/`, existing
  v1 build records, legacy collection contents, Foods code/config or Golden.
- Do not add dependencies or change `pyproject.toml`/`uv.lock`.
- Git authorization is `none`: do not add, commit, push, reset, clean or
  checkout. The commit steps normally required by `writing-plans` are omitted
  because the User has not granted Git writes.

---

## Exact collection mapping

| Candidate | Immutable source | Fresh target |
|---|---|---|
| `e5-small-384` | `hue_full_corpus_a_e5_small_384` | `hue_full_corpus_a_e5_small_384_metadata_v2` |
| `e5-base-768` | `hue_full_corpus_a_e5_base_768` | `hue_full_corpus_a_e5_base_768_metadata_v2` |
| `huydang-dek21-768` | `hue_full_corpus_a_huydang_dek21_768` | `hue_full_corpus_a_huydang_dek21_768_metadata_v2` |
| `qwen3-embedding-0.6b-1024` | `hue_full_corpus_a_qwen3_06b_1024` | `hue_full_corpus_a_qwen3_06b_1024_metadata_v2` |

These are the only legal migration pairs. CLI callers select candidate ID and
must confirm its exact fixed target; they cannot pass a source or arbitrary
target name.

## File map

| Path | Action | Responsibility |
|---|---|---|
| `backend/core/schema.py` | Modify | Domain derivation, chunk-ID relation and seven-field chunk payload. |
| `backend/ingestion/full_corpus_pipeline.py` | Modify narrowly | Add four fixed metadata-v2 names beside the immutable Phase 4 names. |
| `backend/ingestion/source_state.py` | Modify | Build-record v2 constructor while preserving v1 constructor/serialization. |
| `backend/ingestion/full_corpus_metadata_v2.py` | Create | Legacy reader, preflight, vector copy, full verification and guarded CLI. |
| `backend/vectorstore/points.py` | Modify | Validate/build exact seven-field points for canonical fresh chunk paths. |
| `backend/retrieval/full_corpus.py` | Modify after Gate 3 | V2 readiness/freshness, strict payload, logical IDs/domain and new targets. |
| `backend/retrieval/full_corpus_smoke.py` | Modify only if assertions require | Preserve smoke CLI while accepting v2 trace/result contract. |
| `backend/tests/test_full_corpus_chunker.py` | Modify | Domain distribution, deterministic identity and exact payload checks. |
| `backend/tests/test_full_corpus_sparse.py` | Modify narrowly | Correct synthetic source locator to canonical relative form. |
| `backend/tests/test_full_corpus_qdrant_ingestion.py` | Modify | Seven-field points, v2 records and exact target mapping tests. |
| `backend/tests/test_full_corpus_metadata_v2.py` | Create | Pure migration validation/copy/verification/CLI guard tests. |
| `backend/tests/test_full_corpus_retrieval.py` | Modify after Gate 3 | V2 payload, freshness, logical result and private trace tests. |
| `reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json` | Generate at Gate 1 | Sanitized read-only readiness evidence for four source/target pairs. |
| `data/full_corpus_metadata_v2_execution.json` | Generate, ignored | Detailed per-candidate write/verification evidence without corpus text. |
| `reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md` | Create at Gate 1 | Sanitized code/test/read-only preflight evidence for the first Reviewer checkpoint. |
| `reports/full_corpus_metadata_v2_implementation_2026_09_29.md` | Create | Sanitized Implementer evidence and acceptance mapping. |
| `session_prompt/CURRENT_HANDOFF.md` | Replace only at final handoff | Compact `final_review` packet. |

Implementer must not edit the Written Spec, this Plan, canonical guide,
`Project_Status.md` or Reviewer reports. Reviewer owns their status/routing
updates after approval and review.

## Locked interfaces

### Chunk and payload

`backend/core/schema.py` exposes:

```text
FULL_CORPUS_DOMAINS: frozenset[str]
domain_for_source(source: str) -> str
validate_chunk_id(source: str, chunk_id: str) -> int
```

`FullCorpusChunk.domain` is `init=False`, derived once in `__post_init__` from
`source`. `to_qdrant_payload()` returns exactly the seven fields in the Written
Spec.

### Candidate mapping

`FullCorpusCandidate.collection_name` remains the immutable Phase 4/legacy
name. Add `metadata_v2_collection_name: str`; old Phase 4 ingestion continues
to reference only `collection_name` and is not executed in this workstream.

### Build record v2

`backend/ingestion/source_state.py` adds:

```text
FULL_CORPUS_BUILD_SCHEMA_V2 = "phase_4_full_corpus_build:v2"
FULL_CORPUS_PAYLOAD_SCHEMA_V2 = "full_corpus_qdrant_payload:v2"

make_full_corpus_metadata_v2_build_record(
    *,
    collection_name: str,
    source_collection: str,
    source_build_record_sha256: str,
    candidate_id: str,
    model_id: str,
    revision: str,
    dimension: int,
    corpus_identity: str,
    sources: Mapping[str, str],
    sparse_state: SparseState,
    sparse_state_sha256: str,
) -> dict[str, Any]
```

The existing `make_full_corpus_build_record()` remains a v1 historical
constructor so its existing deterministic tests and legacy artifacts do not
change.

### Migration CLI

`python -m backend.ingestion.full_corpus_metadata_v2` has exactly:

```text
preflight [--candidate <one or more fixed candidate IDs>] --output <tracked JSON path>
migrate --candidate <one fixed candidate ID> --confirm-target <exact fixed target>
verify [--candidate <one or more fixed candidate IDs>]
```

`preflight` and `verify` never call a Qdrant mutating method. `migrate` is the
only write path and rejects missing/wrong confirmation before target creation.

### Runtime v2

`build_full_corpus_retrieval_service()` keeps its public signature. Internally
it selects `candidate.metadata_v2_collection_name`, requires both v2 schema
versions, verifies current source hashes and returns:

```text
RetrievedDocument.id = payload.chunk_id
RetrievedDocument.metadata = source/title/heading_path/evidence_parts/domain
```

RRF/reranker inputs remain keyed by point UUID until final result construction,
so Phase 5 score/tie-break semantics do not change.

## Review Contract

### Risk and staged authority

Risk is `high` because the work creates four real Qdrant collections, writes
8.460 points per target and changes canonical retrieval identity/readiness.
Legacy collections are immutable and vectors are reused, but a wrong mapping
could copy the wrong vector space or make runtime consume an incomplete
artifact.

Approval is staged:

1. **Plan approval / Gate 1:** authorizes Tasks 1–4, focused tests and read-only
   queries/preflight against the four legacy collections. It does not authorize
   Qdrant create/upsert or runtime cutover.
2. **Gate 2 live-write approval:** after Reviewer presents a `READY` preflight,
   User must approve the four exact target names. This authorizes Task 5 only.
3. **Gate 3 cutover approval:** after four targets/build records pass independent
   review, User must authorize Task 6 runtime mapping/readiness changes.

Any partial/failed target stops the sequence. Deleting or repairing it needs a
new exact-target approval and is not pre-authorized by any gate above.

### Required Implementer evidence

1. base/head and complete worktree inventory before and after; unrelated staged
   corpus untracking, `.gitignore` and untracked User files preserved;
2. RED/GREEN commands for domain/path validation, chunk-ID/point-ID relation,
   exact seven fields, build-record versions and migration guards;
3. deterministic four-pair registry and rejection of arbitrary source/target;
4. read-only preflight proving all four legacy records/collections match their
   candidate, current source hashes, point IDs, five-field payload and named
   vectors, while all four targets/build-record paths are absent;
5. explicit evidence that preflight imported no vector matrix artifact, loaded
   no dense model and invoked no Qdrant mutation;
6. after Gate 2, per-candidate completed upsert count and full target
   verification of `8.460` IDs/payloads plus source-equal dense+sparse vectors;
7. v2 build-record bytes/hash with exact lineage for each target;
8. post-write proof that four legacy collections still have expected schema,
   count and unchanged v1 build-record hashes;
9. after Gate 3, startup freshness PASS on current corpus plus pure mismatch
   tests for added/deleted/changed source;
10. selected real retrieval smoke covering all four candidates, both retrieval
    treatments and at least one MiniLM path, with logical chunk IDs/domain and
    unchanged point-ID rank/tie-break semantics;
11. public/Golden boundary confirmation and no payload indexes;
12. sanitized tracked artifacts; failed/skipped/partial/not-run outcomes stated
    exactly.

### Reviewer minimum checks

Before Gate 2 recommendation:

```bash
git status --short
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output /tmp/full_corpus_metadata_v2_reviewer_preflight.json
```

Reviewer reads every changed/untracked path and the complete preflight artifact;
new files are inspected directly or with `git diff --no-index /dev/null <path>`.
Reviewer confirms the CLI contains no write call reachable from `preflight` or
`verify` and no embedding runner invocation.

After Gate 2 writes:

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
```

Reviewer independently verifies all four targets and lineage records, then
checks legacy source schema/count/v1 record hashes. Reviewer does not rerun
`migrate`.

After Gate 3 runtime work:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py -q --tb=short
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 --treatment dense_bm25_rrf native_hybrid_rrf --reranker none --select P5-Q01 --output data/full_corpus_metadata_v2_reviewer_smoke.json
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 --treatment dense_bm25_rrf native_hybrid_rrf --reranker minilm --select P5-Q01 --output data/full_corpus_metadata_v2_reviewer_minilm_smoke.json
git diff --check
```

Reviewer additionally inspects Qdrant collection info to prove
`payload_schema == {}` for all four targets, and confirms tracked artifacts do
not contain query text, evidence text, per-source maps, vectors, absolute paths
or secrets.

Findings use `blocker`, `major`, `minor`. Verdict is one of
`ready_for_user_confirmation`, `changes_requested`, `blocked`. Technical PASS
does not authorize cleanup or close the metadata workstream without User
confirmation.

---

### Task 1: Canonical domain, chunk identity and seven-field payload

**Files:**

- Modify: `backend/core/schema.py`
- Modify: `backend/vectorstore/points.py`
- Modify: `backend/tests/test_full_corpus_chunker.py`
- Modify: `backend/tests/test_full_corpus_sparse.py`
- Modify: `backend/tests/test_full_corpus_qdrant_ingestion.py`

**Interfaces:**

- Consumes: existing `FullCorpusChunk`, `EvidencePart` and UUID5 helper.
- Produces: `domain_for_source()`, `validate_chunk_id()`, materialized
  `FullCorpusChunk.domain` and exact seven-field `to_qdrant_payload()`.

- [ ] **Step 1: Record worktree baseline without modifying it**

Run:

```bash
git status --short
git diff --cached --stat
git diff --name-only
```

Expected: note all pre-existing staged/unstaged/untracked paths. Do not stage,
restore or edit unrelated files.

- [ ] **Step 2: Add failing domain and identity tests**

Add focused cases equivalent to:

```python
@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("foods/a.md", "foods"),
        ("heritages/a.md", "heritages"),
        ("festivals/a.md", "festivals"),
        ("performing_arts/a.md", "performing_arts"),
        ("travel/places/a.md", "travel"),
        ("travel/services/a.md", "travel"),
        ("travel/tickets/a.md", "travel"),
    ],
)
def test_domain_for_source_is_exact(source, expected):
    assert domain_for_source(source) == expected

@pytest.mark.parametrize(
    "source",
    ["tourism/a.md", "/foods/a.md", "foods\\a.md", "foods/../a.md", ""],
)
def test_domain_for_source_rejects_noncanonical_source(source):
    with pytest.raises(ValueError):
        domain_for_source(source)

def test_chunk_payload_v2_and_identity_relation():
    chunk = sample_chunk("foods/test.md#0")
    assert chunk.domain == "foods"
    assert set(chunk.to_qdrant_payload()) == {
        "search_text", "source", "title", "heading_path", "evidence_parts",
        "chunk_id", "domain",
    }
    assert chunk.to_qdrant_payload()["chunk_id"] == chunk.chunk_id
    assert chunk.to_qdrant_payload()["domain"] == "foods"
    assert validate_chunk_id(chunk.source, chunk.chunk_id) == 0
```

Also assert wrong source prefix, missing `#`, negative/non-decimal ordinal and
wrong point UUID are rejected by point input validation. Correct the synthetic
`knowledge-base-hue/foods/test.md` source in
`backend/tests/test_full_corpus_sparse.py` to `foods/test.md`; production source
contract is already relative to the knowledge-base root.

- [ ] **Step 3: Run RED**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: new domain/payload tests fail because the interfaces and two payload
fields do not exist; unrelated existing assertions remain diagnosable.

- [ ] **Step 4: Implement the minimal canonical helpers**

Use this direct shape in `backend/core/schema.py`:

```python
from dataclasses import dataclass, field

FULL_CORPUS_DOMAINS = frozenset(
    {"foods", "heritages", "festivals", "performing_arts", "travel"}
)

def domain_for_source(source: str) -> str:
    if not isinstance(source, str) or not source or source.startswith("/"):
        raise ValueError("source must be a non-empty relative POSIX path")
    if "\\" in source:
        raise ValueError("source must use POSIX separators")
    parts = source.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("source contains a non-canonical path component")
    domain = parts[0]
    if domain not in FULL_CORPUS_DOMAINS:
        raise ValueError(f"unsupported full-corpus domain: {domain}")
    return domain

def validate_chunk_id(source: str, chunk_id: str) -> int:
    prefix = f"{source}#"
    if not isinstance(chunk_id, str) or not chunk_id.startswith(prefix):
        raise ValueError("chunk_id must serialize source#ordinal")
    ordinal_text = chunk_id[len(prefix):]
    if not ordinal_text.isdecimal():
        raise ValueError("chunk ordinal must be a non-negative decimal integer")
    ordinal = int(ordinal_text)
    if str(ordinal) != ordinal_text:
        raise ValueError("chunk ordinal must use canonical decimal form")
    return ordinal
```

Add `domain: str = field(init=False)` and set it in
`FullCorpusChunk.__post_init__` with `domain_for_source(self.source)`. Add
`chunk_id` and `domain` to `to_qdrant_payload()` without changing the other
five values.

In `backend/vectorstore/points.py`, change both exact payload field sets to the
seven-field set and call `validate_chunk_id(chunk.source, chunk.chunk_id)` plus
`point_id_for_chunk_id(chunk.chunk_id)` equality before constructing a point.

- [ ] **Step 5: Run GREEN and deterministic full chunk check**

Run the Step 3 command again. Expected: PASS. Then run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_chunker.py::test_full_corpus_determinism_and_preview_byte_equality -q --tb=short
```

Expected: PASS with `205` files/`8.460` deterministic chunks; every chunk domain
matches its source root and two runs produce identical IDs/payloads.

### Task 2: Fixed target registry and build-record v2

**Files:**

- Modify: `backend/ingestion/full_corpus_pipeline.py`
- Modify: `backend/ingestion/source_state.py`
- Modify: `backend/tests/test_full_corpus_qdrant_ingestion.py`

**Interfaces:**

- Consumes: Task 1 payload contract and existing four candidates.
- Produces: fixed source→target names and deterministic v2 build-record
  constructor for Task 3.

- [ ] **Step 1: Add failing registry and record tests**

Assert the ordered registry equals exactly:

```python
[
    ("e5-small-384", "hue_full_corpus_a_e5_small_384", "hue_full_corpus_a_e5_small_384_metadata_v2", 384),
    ("e5-base-768", "hue_full_corpus_a_e5_base_768", "hue_full_corpus_a_e5_base_768_metadata_v2", 768),
    ("huydang-dek21-768", "hue_full_corpus_a_huydang_dek21_768", "hue_full_corpus_a_huydang_dek21_768_metadata_v2", 768),
    ("qwen3-embedding-0.6b-1024", "hue_full_corpus_a_qwen3_06b_1024", "hue_full_corpus_a_qwen3_06b_1024_metadata_v2", 1024),
]
```

Create a v2 record and assert:

```python
assert set(record) == {
    "schema_version", "status", "collection_name", "representation",
    "corpus", "dense", "sparse", "qdrant", "migration",
}
assert record["schema_version"] == "phase_4_full_corpus_build:v2"
assert record["qdrant"]["payload_schema_version"] == "full_corpus_qdrant_payload:v2"
assert record["migration"] == {
    "mode": "copy_verified_vectors",
    "source_collection": "hue_full_corpus_a_e5_small_384",
    "source_build_record_sha256": "a" * 64,
}
```

Also prove the existing v1 constructor still returns v1 with no `migration` or
`payload_schema_version`, and v2 rejects a non-hex/non-64 source record hash or
source==target.

- [ ] **Step 2: Run RED**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Expected: new registry/record tests fail; legacy v1 tests still pass.

- [ ] **Step 3: Add the exact target names without changing legacy meaning**

Extend the existing dataclass in this field order:

```python
@dataclass(frozen=True)
class FullCorpusCandidate:
    candidate_id: str
    collection_name: str
    dense_spec: DenseModelSpec
    metadata_v2_collection_name: str
```

Construct all four entries from the existing dense specs, old mapping and one
fixed `_METADATA_V2_COLLECTION_BY_CANDIDATE` mapping containing exactly the
table above. Validate both mapping key sets against `DENSE_MODEL_SPECS` and
validate all eight names are unique. Do not redirect any Phase 4 call site.

- [ ] **Step 4: Implement the v2 constructor by preserving v1 validation**

`make_full_corpus_metadata_v2_build_record()` first calls the existing v1
constructor, then returns a fresh dictionary with:

```python
record["schema_version"] = FULL_CORPUS_BUILD_SCHEMA_V2
record["collection_name"] = collection_name
record["qdrant"] = {
    **record["qdrant"],
    "payload_schema_version": FULL_CORPUS_PAYLOAD_SCHEMA_V2,
}
record["migration"] = {
    "mode": "copy_verified_vectors",
    "source_collection": source_collection,
    "source_build_record_sha256": source_build_record_sha256,
}
```

Validate the digest with `len == 64` and `int(value, 16)`, require distinct
source/target names, and keep deterministic serializer/final-only writer
unchanged.

- [ ] **Step 5: Run GREEN**

Run the Step 2 command. Expected: PASS, including unchanged v1 deterministic
bytes and new deterministic v2 bytes.

### Task 3: Migration primitives and full vector equivalence

**Files:**

- Create: `backend/ingestion/full_corpus_metadata_v2.py`
- Create: `backend/tests/test_full_corpus_metadata_v2.py`

**Interfaces:**

- Consumes: Task 1 payloads and Task 2 pair/build contracts.
- Produces: strict legacy record validation, point-copy construction, source/
  target vector equality and read-only/full-write orchestration primitives.

- [ ] **Step 1: Write failing pure tests for legacy and migrated records**

Use qdrant-client `models.Record`/`models.PointStruct` values. Required cases:

```python
def test_build_migrated_point_preserves_vectors_and_replaces_payload():
    source = legacy_record(point_id, legacy_payload, dense, sparse)
    point = build_migrated_point(source, chunk, expected_dimension=2)
    assert str(point.id) == point_id
    assert point.vector["dense"] == dense
    assert point.vector["sparse"] == sparse
    assert point.payload == chunk.to_qdrant_payload()

test_legacy_reader_rejects_seven_fields_or_wrong_vectors
  expected: ValueError before any target point is constructed
test_migrated_comparison_rejects_one_dense_value_change
  expected: ValueError identifying dense mismatch without vector contents
test_migrated_comparison_rejects_sparse_index_or_value_change
  expected: ValueError identifying sparse mismatch without vector contents
test_migrated_comparison_rejects_payload_or_id_change
  expected: ValueError identifying payload or point-ID mismatch
test_candidate_confirmation_rejects_arbitrary_target
  expected: ValueError before any Qdrant mutation
```

Also test duplicate source point, missing fresh chunk ID, foreign source point,
target extra/missing point and build-record/source-hash mismatch.

- [ ] **Step 2: Run RED**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py -q --tb=short
```

Expected: collection fails because the module/interfaces do not exist.

- [ ] **Step 3: Implement strict migration-only validators**

Keep these constants/functions local to the migration module:

```text
LEGACY_PAYLOAD_FIELDS = frozenset(
    {"search_text", "source", "title", "heading_path", "evidence_parts"}
)
MIGRATION_BATCH_SIZE = 64

validate_legacy_payload(point_id: str, payload: Any) -> dict[str, Any]
validate_named_vectors(
    point_id: str, vector: Any, expected_dimension: int
) -> tuple[list[float], models.SparseVector]
build_migrated_point(
    source_record: models.Record,
    chunk: FullCorpusChunk,
    expected_dimension: int,
) -> models.PointStruct
assert_migrated_record_equal(
    source_record: models.Record,
    target_record: models.Record,
    expected_payload: Mapping[str, Any],
    expected_dimension: int,
) -> None
```

The legacy validator duplicates only the frozen five-field boundary needed to
read old artifacts; it must not be imported by runtime retrieval. Dense values
must be finite and exact dimension. Sparse indices/values must be aligned,
finite and strictly increasing. Equality compares dense list values, sparse
indices/value lists and exact v2 payload; no tolerance or re-normalization.

- [ ] **Step 4: Implement bounded source iteration and target verification**

Use Qdrant scroll pages of `64` with `with_payload=True` and
`with_vectors=["dense", "sparse"]`. For each page:

1. reject duplicate/foreign point UUID;
2. resolve the fresh chunk by UUID;
3. create target `PointStruct` with copied vectors and fresh payload;
4. on verification, retrieve the same IDs from target with vectors/payload;
5. compare by ID with `assert_migrated_record_equal()`.

After all pages, require exact expected ID set and exact source/target counts.
Never materialize all dense matrices or vector payloads into a tracked file.

- [ ] **Step 5: Run GREEN**

Run the Step 2 command. Expected: PASS using only in-memory qdrant model objects;
no server, model or filesystem corpus is required for these pure cases.

### Task 4: Guarded CLI and read-only four-pair preflight — Gate 1

**Files:**

- Modify: `backend/ingestion/full_corpus_metadata_v2.py`
- Modify: `backend/tests/test_full_corpus_metadata_v2.py`
- Generate after tests: `reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json`

**Interfaces:**

- Consumes: Tasks 1–3.
- Produces: `preflight`, `migrate`, `verify` commands and sanitized `READY`
  evidence. Only `migrate` reaches create/upsert.

- [ ] **Step 1: Add failing CLI routing and no-write tests**

Patch a recording client and assert:

```python
assert run_preflight(recording_client, selected_candidates) == ready_evidence
assert recording_client.mutations == []

assert run_verify(recording_client, selected_candidates) == verified_evidence
assert recording_client.mutations == []

with pytest.raises(ValueError, match="exact target confirmation"):
    run_migration(recording_client, pair, confirm_target="wrong")
assert recording_client.mutations == []
```

Test unknown/duplicate candidate selectors, unsafe tracked output content,
existing target, existing target record, stale source hashes, legacy v1 schema
mismatch, point-set mismatch and vector/payload mismatch. A preflight failure
must yield overall `BLOCKED`, non-zero CLI exit and zero writes.

- [ ] **Step 2: Run RED**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py -q --tb=short
```

Expected: new orchestration/CLI tests fail.

- [ ] **Step 3: Implement direct orchestration**

`preflight` must, for every selected pair:

- call existing fresh corpus preparation without loading a dense runner;
- read exact v1 build record bytes and compute SHA-256;
- compare current source hashes and corpus/sparse identities;
- validate source Qdrant schema/count, all IDs, exact legacy payloads and both
  vectors;
- require target collection absent and target record absent;
- emit only candidate/source/target names, dimensions, counts, schema versions,
  source-record SHA, corpus/sparse identities, readiness and safe errors.

Do not emit the 205-path mapping, point IDs, payloads or vectors. Serialize the
tracked preflight artifact deterministically and atomically.

`migrate` must rerun the selected pair preflight immediately, validate exact
confirmation, create one target with existing default dense/sparse schema,
copy/upsert bounded pages, run complete verification, then atomically write one
v2 build record. On error it records completed/observed safe counts, writes no
final record and performs no delete/rollback.

`verify` requires an existing complete target/v2 record and reruns full
payload/vector equality read-only.

- [ ] **Step 4: Run GREEN and focused regression**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short
```

Expected: PASS.

- [ ] **Step 5: Run the real read-only preflight**

This step is authorized only after User approval of this Plan/Review Contract:

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
```

Expected: overall `READY`; all four legacy sources have `8.460` valid points,
current sources are fresh, all four fixed targets and target build-record paths
are absent, and mutation count is zero.

- [ ] **Step 6: Stop at Gate 2**

Write the interim Implementer evidence note at
`reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md` and replace
`CURRENT_HANDOFF.md` with `Target role: reviewer`, exact code/artifact paths,
command results and one next action: review Gate 1 and request User approval for
the four exact targets. Do not run `migrate`.

### Task 5: Build and verify four metadata-v2 collections — Gate 2

**Files/State:**

- Create in Qdrant: four exact metadata-v2 targets from the mapping table.
- Create locally: four corresponding v2 build records under
  `data/full_corpus_builds/`.
- Generate/update ignored: `data/full_corpus_metadata_v2_execution.json`.

**Interfaces:**

- Consumes: Reviewer-accepted `READY` preflight and explicit User Gate 2
  approval naming all four targets.
- Produces: four fully verified immutable targets and v2 build records.

- [ ] **Step 1: Reconfirm authority and absence immediately before writes**

Record the User approval text and run the exact Step 4 preflight command again.
Expected: `READY`; if any target/record now exists or source state changed, stop
without writing.

- [ ] **Step 2: Migrate E5-small and verify**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate e5-small-384 --confirm-target hue_full_corpus_a_e5_small_384_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate e5-small-384
```

Expected: `8.460` points and complete exact payload/vector verification; v2
record exists only after verification.

- [ ] **Step 3: Migrate E5-base and verify**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate e5-base-768 --confirm-target hue_full_corpus_a_e5_base_768_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate e5-base-768
```

Expected: same contract for the 768-dimensional candidate.

- [ ] **Step 4: Migrate HuyDang and verify**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate huydang-dek21-768 --confirm-target hue_full_corpus_a_huydang_dek21_768_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate huydang-dek21-768
```

Expected: same contract; no PyVi/model execution is needed because vectors are
copied.

- [ ] **Step 5: Migrate Qwen and verify**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate qwen3-embedding-0.6b-1024 --confirm-target hue_full_corpus_a_qwen3_06b_1024_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate qwen3-embedding-0.6b-1024
```

Expected: same contract; no CUDA/Qwen model load occurs.

If any migrate/verify command fails, stop immediately. Do not continue to later
candidates and do not delete or repair the failed target.

- [ ] **Step 6: Verify all targets and immutable sources together**

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
```

Expected: all four targets PASS. Re-run source-only observations and prove
legacy schema/count plus the four v1 build-record SHA-256 values match Gate 1.

- [ ] **Step 7: Stop for independent review and Gate 3**

Update the interim evidence/handoff with per-target counts, v2 record hashes,
legacy immutability and failed/skipped status. Stop before changing retrieval
collection selection. Reviewer independently runs the post-Gate-2 Review
Contract and asks User for exact runtime cutover approval.

### Task 6: Cut canonical retrieval to metadata v2 — Gate 3

**Files:**

- Modify: `backend/retrieval/full_corpus.py`
- Modify only if required: `backend/retrieval/full_corpus_smoke.py`
- Modify: `backend/tests/test_full_corpus_retrieval.py`

**Interfaces:**

- Consumes: four Reviewer-verified targets/v2 records and explicit User Gate 3
  approval.
- Produces: strict v2 readiness, source freshness, logical chunk IDs/domain and
  unchanged retrieval ranking behavior.

- [ ] **Step 1: Add failing v2 payload/readiness/result tests**

Required cases:

```text
test_v2_payload_accepts_exact_identity_and_domain
  expected: exact payload object returned unchanged
test_v2_payload_rejects_legacy_five_fields
  expected: RetrievalDependencyError listing chunk_id/domain as missing
test_v2_payload_rejects_extra_field
  expected: RetrievalDependencyError listing the extra key
test_v2_payload_rejects_point_uuid_chunk_id_mismatch
  expected: RetrievalDependencyError before result construction
test_v2_payload_rejects_domain_source_mismatch
  expected: RetrievalDependencyError before result construction
test_v2_build_record_rejects_wrong_build_or_payload_schema
  expected: ComponentNotReadyError
test_v2_freshness_rejects_added_deleted_and_changed_source
  expected: ComponentNotReadyError for all three mismatch classes
test_result_uses_chunk_id_and_domain_but_rrf_ties_still_use_point_id
  expected: logical result ID plus unchanged internal point-ID order
test_trace_contains_only_point_id_chunk_id_domain_rank_score_allowlist
  expected: no query/search/evidence/source-path field
```

Trace tests must reject query/search/evidence/source path. Test both no-rerank
and MiniLM-success construction so both boundaries return logical chunk IDs.

- [ ] **Step 2: Run RED**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py -q --tb=short
```

Expected: new v2 assertions fail against the five-field/v1 runtime.

- [ ] **Step 3: Implement strict payload and startup freshness**

Change the Qdrant payload projection to all seven fields. Reuse
`domain_for_source()`, `validate_chunk_id()` and `point_id_for_chunk_id()`; wrap
their validation failures as `RetrievalDependencyError` naming only safe point
ID/reason.

At composition:

```python
collection_name = candidate.metadata_v2_collection_name
record_path = BUILD_RECORDS_DIR / f"{collection_name}.json"
root, rel_paths = discover_full_corpus_files(settings)
current_sources = compute_corpus_state(root, rel_paths)
fresh, discrepancies = verify_full_corpus_record_freshness(
    current_sources, record_data
)
if not fresh:
    raise ComponentNotReadyError("Full-corpus source state is stale")
```

Require v2 build/payload versions, matching lineage source collection, all
existing model/sparse/count invariants and target collection schema with empty
Qdrant payload-index schema. Do not log path-level discrepancies in public
errors.

- [ ] **Step 4: Preserve point-ID ranking and map only at result/trace boundary**

Keep `candidate_docs`, dense/sparse branches, BM25, RRF and reranker tie-breaks
keyed by point UUID. When a returned payload has been validated, allowlisted
stage rows become:

```python
{
    "point_id": point_id,
    "chunk_id": payload["chunk_id"],
    "domain": payload["domain"],
    "rank": rank,
    "score": score,
}
```

Final documents become:

```python
RetrievedDocument(
    id=payload["chunk_id"],
    score=float(final_score),
    text=payload["search_text"],
    metadata={
        "source": payload["source"],
        "title": payload["title"],
        "heading_path": list(payload["heading_path"]),
        "evidence_parts": list(payload["evidence_parts"]),
        "domain": payload["domain"],
    },
)
```

Do not place rank/score/point ID in document metadata and do not use domain in
any scoring branch.

- [ ] **Step 5: Run GREEN and focused regression**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_sparse.py -q --tb=short
```

Expected: PASS.

- [ ] **Step 6: Run selected real retrieval smoke**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 --treatment dense_bm25_rrf native_hybrid_rrf --reranker none --select P5-Q01 --output data/full_corpus_metadata_v2_smoke.json
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 --treatment dense_bm25_rrf native_hybrid_rrf --reranker minilm --select P5-Q01 --output data/full_corpus_metadata_v2_minilm_smoke.json
```

Expected: all selected cells technically PASS; trace/result identities satisfy
v2. Ranking differences versus a freshly built ANN index are observations, not
automatic failures, unless IDs/payload/vectors/score semantics violate the
contract.

### Task 7: Final regression, report and Reviewer handoff

**Files:**

- Inspect: every changed/untracked implementation path.
- Create: `reports/full_corpus_metadata_v2_implementation_2026_09_29.md`
- Replace: `session_prompt/CURRENT_HANDOFF.md`

**Interfaces:**

- Consumes: Tasks 1–6 plus Gate evidence.
- Produces: one sanitized implementation report and exact `final_review`
  handoff; no project closure or Phase 6 restart.

- [ ] **Step 1: Run final focused checks**

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_retrieval.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
git diff --check
```

Expected: PASS and no whitespace errors. Do not run the full backend suite
unless changed dependency evidence or a focused failure expands the blast
radius.

- [ ] **Step 2: Self-review simplicity, authority and privacy**

Confirm:

- one fixed candidate mapping, one migration module and no framework/registry
  service;
- old and new payload validators are isolated to migration/runtime roles;
- no embedding runner/model call exists in migration flow;
- only exact approved target names received writes;
- legacy/Foods collections and v1 records are unchanged;
- no domain filter/index/boost, Golden/API change or speculative metadata;
- no tracked artifact contains corpus/query/evidence/vector/path-level data;
- unrelated User worktree changes remain untouched.

- [ ] **Step 3: Write the Implementer report**

Use exactly these sections:

```text
## Authority, gates and repository state
## Changed paths and responsibilities
## RED/GREEN focused checks
## Canonical payload/domain/identity evidence
## Gate 1 four-pair preflight
## Gate 2 collection writes and complete verification
## Build-record v2 and vector lineage
## Legacy collection immutability
## Gate 3 runtime freshness and retrieval identity
## Selected real retrieval smoke
## Privacy and unchanged public/evaluation boundaries
## Acceptance mapping
## Deviations and anomalies
## Failed, skipped and not verified
## Limitations and Reviewer handoff
```

The report is an evidence index, not approval. It contains no source-path list,
point rows, vectors, query/evidence text, absolute paths or secrets.

- [ ] **Step 4: Create the final-review handoff and stop**

Replace `session_prompt/CURRENT_HANDOFF.md` with:

- `Target role: reviewer`;
- `Handoff kind: final_review`;
- base/head and exact changed/untracked implementation paths;
- three User gate decisions and exact authorized Qdrant targets/actions;
- command/result summary and report/artifact paths;
- deviations/anomalies/partial target state;
- exact Reviewer minimum commands;
- one next action: independently review metadata v2 implementation.

Do not edit the Written Spec, Plan, guide or `Project_Status.md`; do not create a
User Report; do not commit/push. Give the User the standard four-file Reviewer
bootstrap prompt.

## Spec coverage and simplicity check

| Written Spec area | Plan coverage |
|---|---|
| Layered ownership and seven-field payload | Tasks 1–2 |
| Five-value domain derived from source | Task 1 |
| Logical chunk ID and UUID relation | Tasks 1 and 6 |
| Separate build/payload versions and lineage | Task 2 |
| Four fresh collections, copied vectors | Tasks 3–5 |
| Complete source/target verification | Tasks 3–5, Review Contract |
| Runtime exact schema and freshness fail-closed | Task 6 |
| RetrievedDocument/trace identity and privacy | Task 6 |
| No index/filter/evaluation/public expansion | Global constraints, Tasks 6–7 |
| Legacy closure/history preserved | Tasks 2, 5 and 7 |
| Separate write/cutover authority | Review Contract, Tasks 4–6 |

The plan adds one migration module because vector-copy lifecycle is not a
responsibility of the original embedding pipeline or runtime retriever. It
reuses existing candidate/model, chunking, sparse-state, Qdrant schema and
atomic record primitives; it does not introduce a metadata framework.

## Approval effect

User approval of this Plan and Review Contract on 2026-09-29 authorizes only
Gate 1: Tasks 1–4, focused local tests, local corpus reads and read-only
inspection/scroll of the four immutable legacy Full-corpus collections. It does
not authorize
Qdrant create/upsert, build-record v2 writes, runtime cutover, deletion,
replacement, cleanup, dense embedding, external API/model calls, Git writes or
Phase 6 continuation.

Gate 2 and Gate 3 require later explicit User approvals exactly as defined in
the Review Contract.
