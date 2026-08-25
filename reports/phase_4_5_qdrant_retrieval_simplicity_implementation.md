# Phase 4–5 Qdrant & Retrieval Simplicity Implementation Report (Revision 2)

## 1. Executive Summary

This report documents the completed implementation and correction revision 2 for the coordinated Phase 4–5 simplicity refactor of Hue Foods RAG, executed strictly according to the approved design spec (`docs/superpowers/specs/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-design.md`) and implementation plan (`docs/superpowers/plans/2026-08-25-phase-4-5-qdrant-retrieval-simplicity-implementation.md`).

All findings from the Codex Reviewer (`reports/phase_4_5_qdrant_retrieval_simplicity_codex_review.md`) have been resolved:
1. **Active & Candidate Runtime Compatibility**: Read-only retrieval startup before cutover accepts legacy collections with the exact dense 384/Cosine vector (ignoring historical sparse fields), while candidate ingestion and schema validation strictly enforce pure dense-only schema.
2. **Notebooks 03–05 Rebuilt**: Notebook 03 is a focused dense E5 lesson; Notebook 04 conducts read-only inspection on candidate `hue_foods_e5_small_384_dense`; Notebook 05 tests all three retrieval profiles via public `build_service` on the candidate collection without offline flags or invalid compositions. All three notebooks executed cleanly end-to-end with clean outputs.
3. **Test Simplicity & Consolidation**: Consolidated `test_bm25.py` from 20 micro-tests to 4 behavior tests; consolidated `test_context_builder.py` from 10 tests to 4 behavior tests; removed all dead-URL and duplicate mechanism tests.
4. **Comprehensive Test Audit**: Every retained test across the affected test files is audited individually below with a 1-sentence rationale.
5. **No Compatibility Wrappers**: Removed `RetrievalService.snapshot` alias (exposing only `status`).

---

## 2. Baseline vs. Candidate Retrieval Evidence (104 × 3 Questions)

Evaluated over the full 104 canonical questions from `knowledge-base-hue/foods/evaluation/tests.jsonl`.
- Baseline artifact: `reports/phase_4_5_active_retrieval_baseline.json`
- Candidate comparison artifact: `reports/phase_4_5_candidate_retrieval_comparison.json`

### Summary Comparison Table

| Profile | Collection | Questions | Failed | Mean Latency (ms) | Mean MRR | Mean nDCG | Keyword Coverage (%) | Rank Order Identity |
|---|---|---|---|---|---|---|---|---|
| `dense_only` | Active (`hue_foods_e5_small_384`) | 104 | 0 | 22.52 | 0.8250 | 0.8263 | 95.83% | Baseline |
| `dense_only` | Candidate (`..._dense`) | 104 | 0 | 27.09 | 0.8250 | 0.8263 | 95.83% | **104/104 (100%)** |
| `hybrid_no_rerank` | Active (`hue_foods_e5_small_384`) | 104 | 0 | 25.22 | 0.8246 | 0.8327 | 97.12% | Baseline |
| `hybrid_no_rerank` | Candidate (`..._dense`) | 104 | 0 | 22.71 | 0.8246 | 0.8327 | 97.12% | **104/104 (100%)** |
| `hybrid_rerank` | Active (`hue_foods_e5_small_384`) | 104 | 0 | 307.24 | 0.7524 | 0.7772 | 91.19% | Baseline |
| `hybrid_rerank` | Candidate (`..._dense`) | 104 | 0 | 442.35 | 0.7524 | 0.7772 | 91.19% | **104/104 (100%)** |

**Conclusion**: Eliminating stored Qdrant sparse vectors and relying on pure dense Qdrant retrieval + Python BM25 scoring produces zero regression in retrieval accuracy, zero rank shifts across all 312 runs, and clean deterministic execution.

---

## 3. Detailed Architectural & Simplicity Changes

### 3.1. Dual Schema Validation Boundary (`backend/vectorstore/qdrant.py`)
- `validate_collection_info(info, settings, *, strict_dense_only=True)`:
  - `strict_dense_only=True` (default for candidate ingestion and test collections): verifies named `dense` vector (size 384, Cosine) and strictly rejects any sparse vectors or extraneous vector names.
  - `strict_dense_only=False` (used in `core.startup._verify_collection` for read-only retrieval before cutover): verifies named `dense` vector (size 384, Cosine) and point count 572, ignoring historical sparse configurations.
- `client_from_settings()`: uncached client creation from `vector_database` settings.
- `expected_schema()`: returns pure dense named-vector dictionary.

### 3.2. Lexical Tokenization & BM25 (`backend/scoring/bm25.py`)
- Unicode regex word tokenization `tokenize(text: str)` implemented directly in `bm25.py`.
- Removed `SparseEmbedder` import from lexical scoring.

### 3.3. Pure Dense Point Structs (`backend/vectorstore/points.py`)
- `point_id_for(chunk_id)`: deterministic UUID5 point ID generation.
- `build_points()`: builds pure dense `models.PointStruct` with `vector={"dense": ...}` and payload containing `embedding_model`, omitting redundant `embedding_dimension`.

### 3.4. Fail-Explicit Upsert & Guarded Reset (`backend/vectorstore/`)
- `upsert.py`: Bounded batch upsert without retry loop, transient wrappers, or schema alterations.
- `reset.py`: CLI requiring `--collection <name>` and `--confirm "DELETE <name>"`. Displays point count prior to deletion and verifies collection is absent afterwards.

### 3.5. Concrete Cross-Encoder Reranker (`backend/reranking/cross_encoder.py`)
- Concrete `CrossEncoderReranker` class owning local `sentence_transformers.CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")`.
- Eliminated 3 inheritance layers (`BaseReranker` -> `ScorerReranker` -> `CrossEncoderReranker`).

### 3.6. Direct Service Composition (`backend/core/startup.py` & `backend/retrieval/service.py`)
- `build_retrieval_service()` returns `RetrievalService` directly.
- Lightweight immutable dataclass `RetrievalStatus` (`collection_name`, `point_count`, `embedding_model`, `embedding_dimension`, `active_profile`, `bm25_ready`, `reranker_ready`).
- Removed `RetrievalStack`, `RetrievalSnapshot`, config/corpus fingerprints, and `verify_snapshot()` runtime checks.
- Removed `RetrievalService.snapshot` alias (only `service.status` is exposed).

---

## 4. Retained Test Suite Audit

Every retained test in the affected test suites protects a specific user-facing or contract requirement:

### `backend/tests/test_bm25.py` (4 tests)
1. `test_tokenize_keeps_vietnamese_words_and_removes_punctuation`: Protects Unicode regex tokenization to preserve Vietnamese diacritics and strip punctuation for accurate lexical matching.
2. `test_bm25_known_hue_corpus_ranking_and_fit`: Protects BM25 model fitting, finite score guarantees, lexical ranking over Hue food terms, and error handling for unfitted state.
3. `test_min_max_normalize_properties`: Protects min-max score normalization into the [0.0, 1.0] interval, constant-signal zero-mapping, and non-finite rejection.
4. `test_validate_weights_contract`: Protects hybrid fusion weight validation ensuring non-negative, finite weights that strictly sum to 1.0.

### `backend/tests/test_context_builder.py` (4 tests)
1. `test_context_budget_and_document_limits`: Protects whole-chunk context inclusion without mid-chunk truncation within character budgets and caps at maximum allowed documents.
2. `test_structural_safety_and_source_mapping`: Protects JSON evidence serialization so forged internal strings stay escaped and maps ordered source citations with titles, sections, and ranks.
3. `test_empty_input_and_empty_text_handling`: Protects empty document input handling and skips empty or whitespace-only documents while maintaining relative ranking.
4. `test_build_does_not_mutate_documents`: Protects input `RetrievedDocument` instances and their metadata from in-place mutations during context construction.

### `backend/tests/test_ingestion_pipeline.py` (11 tests)
1. `test_dense_point_contract_uses_uuid5_and_model_identity`: Protects deterministic UUID5 point ID creation and payload metadata compliance with the dense-only schema.
2. `test_live_dense_schema_has_no_sparse_vectors`: Protects collection creation to ensure newly created collections have named dense vectors without sparse vector configurations.
3. `test_live_ingestion_summary_and_collection_state`: Protects real ingestion over the curated 572-chunk corpus to produce exact point counts and correct Qdrant vector configurations.
4. `test_ingestion_idempotent_rerun_on_real_dense_collection`: Protects idempotency so re-running ingestion over existing collections succeeds without duplicating points or corrupting state.
5. `test_ingestion_rejects_non_canonical_chunk_count`: Protects the pre-mutation guard that fails closed if corpus chunk count deviates from the canonical 572 chunks.
6. `test_ingestion_rejects_foreign_existing_points_before_upsert`: Protects the pre-mutation subset check that aborts ingestion if the target collection contains unmanaged foreign points.
7. `test_ingestion_rejects_existing_model_mismatch_before_mutation`: Protects against indexing corruption by aborting ingestion if existing points were embedded with a different model ID.
8. `test_upsert_points_and_count_gate_on_real_batch`: Protects batch upsert execution over real batches and verifies the exact point count verification gate.
9. `test_reset_deletes_only_exact_guarded_target_and_reports_count`: Protects the destructive reset command to ensure it only deletes the exact target collection and reports deleted points.
10. `test_reset_rejects_confirmation_mismatch_without_deleting`: Protects the reset command from accidental deletion by requiring an exact `DELETE <name>` confirmation string.
11. `test_reset_refuses_missing_collection`: Protects the reset command to fail explicitly with clear errors when the specified collection does not exist.

### `backend/tests/test_retrieval_service.py` (8 tests)
1. `test_cross_encoder_rerank_contract_and_non_mutation`: Protects the MiniLM cross-encoder reranking contract ensuring finite descending scores, reranker model metadata, and non-mutation of inputs.
2. `test_dense_only_builds_only_required_runtime`: Protects profile-scoped initialization so `dense_only` operates without loading BM25 corpus or MiniLM models.
3. `test_dense_only_search_returns_dense_scores_only`: Protects dense retrieval results to ensure sorted descending scores and prevents fabricated multi-stage metadata.
4. `test_hybrid_no_rerank_runs_dense_then_python_bm25`: Protects `hybrid_no_rerank` execution combining dense candidate retrieval with Python BM25 min-max fusion.
5. `test_hybrid_rerank_runs_dense_bm25_then_real_minilm`: Protects `hybrid_rerank` execution applying real MiniLM cross-encoder reranking to hybrid candidate documents.
6. `test_empty_query_raises_invalid_query_error`: Protects search query validation ensuring empty or whitespace-only queries fail fast with typed `InvalidQueryError`.
7. `test_unknown_profile_raises_configuration_error`: Protects configuration validation ensuring requesting an unconfigured profile fails fast at service startup.
8. `test_repeated_real_search_is_deterministic`: Protects search determinism ensuring identical queries against the same corpus produce identical ranked results.

### `backend/tests/test_evaluation.py` (8 tests)
1. `test_small_dataset_contains_twenty_real_questions`: Protects the evaluation fixture ensuring the 20-question test set contains real Hue food questions covering all categories.
2. `test_questions_have_the_fields_used_by_evaluation`: Protects test question schema ensuring required fields (question, category, reference_answer, keywords) are non-empty.
3. `test_load_tests_uses_the_supplied_path`: Protects test file loader ensuring correct question counts are parsed from specified dataset paths (20 and 104).
4. `test_mrr_uses_keyword_position_in_real_hue_text`: Protects the Mean Reciprocal Rank (MRR) metric calculation based on keyword position in retrieved texts.
5. `test_ndcg_uses_binary_keyword_relevance`: Protects the Normalized Discounted Cumulative Gain (nDCG) metric calculation for ranked retrieval relevance.
6. `test_retrieval_evaluation_uses_the_real_dense_collection`: Protects end-to-end single-question retrieval evaluation against the real dense test collection.
7. `test_answer_evaluation_calls_real_generation_and_judge_models` (paid live): Protects end-to-end answer evaluation with generation and LLM judge scoring (deselected in non-paid runs).
8. `test_retrieval_handler_returns_named_columns_and_rows`: Protects the Gradio evaluation UI handler ensuring structured markdown summaries and table formatting.
9. `test_retrieval_comparison_reports_latency_failures_and_rank_changes`: Protects the retrieval comparison tool ensuring accurate calculation of profile summaries and rank differences.

### `backend/tests/test_api_chat.py` (20 tests: 16 non-paid, 4 paid)
1. `test_import_has_no_external_side_effect`: Protects app module import to ensure no external services or network calls are triggered during import.
2. `test_health_degraded_before_lifespan`: Protects `/health` endpoint reporting `degraded` before the application lifespan initializes.
3. `test_health_ok_after_real_lifespan`: Protects `/health` endpoint reporting `ok` and `ready` components after full lifespan initialization.
4. `test_health_degraded_when_qdrant_is_down`: Protects real failure degradation when Qdrant is unreachable, returning degraded health and HTTP 503 on chat.
5. `test_health_never_exposes_secrets`: Protects API health endpoints ensuring sensitive credentials or API keys are never exposed in response text.
6. `test_empty_query_422`: Protects chat endpoint request validation rejecting empty queries with HTTP 422 `invalid_query`.
7. `test_oversized_query_422`: Protects chat endpoint request validation rejecting queries exceeding 500 characters with HTTP 422 `invalid_query`.
8. `test_whitespace_session_id_422`: Protects chat endpoint request validation rejecting whitespace-only session IDs with HTTP 422 `invalid_session_id`.
9. `test_oversized_session_id_422`: Protects chat endpoint request validation rejecting session IDs exceeding 128 characters with HTTP 422 `invalid_session_id`.
10. `test_missing_body_422_invalid_request`: Protects request body validation rejecting empty POST bodies with HTTP 422 `invalid_request`.
11. `test_malformed_body_422_invalid_request`: Protects request body validation rejecting malformed data types with HTTP 422 `invalid_request`.
12. `test_chat_success_with_explicit_session_id` (paid live): Protects real end-to-end chat flow with client-supplied session ID.
13. `test_chat_generates_session_id_when_missing` (paid live): Protects automatic UUID session ID generation when omitted by client.
14. `test_hybrid_rerank_exposes_real_minilm_in_debug` (paid live): Protects `retrieval_debug` output exposing the real MiniLM reranker model name.
15. `test_retrieval_unavailable_when_collection_vanishes_mid_run`: Protects runtime failure handling returning HTTP 503 `retrieval_unavailable` if a collection is deleted during runtime.
16. `test_generator_not_configured_503`: Protects unconfigured generator error mapping returning HTTP 503 `generator_not_configured` when API key is absent.
17. `test_generator_unavailable_502`: Protects provider network failure error mapping returning HTTP 502 `generator_unavailable` when LLM provider is unreachable.
18. `test_no_sensitive_payload_in_responses` (paid live): Protects response body sanitization ensuring system prompts and secrets are never leaked.
19. `test_lifespan_warms_e5_and_minilm_before_ready`: Protects lifespan component warm-up ensuring both E5 and MiniLM models are pre-warmed for `hybrid_rerank`.
20. `test_dense_only_lifespan_loads_e5_but_never_minilm`: Protects profile-scoped lifespan warm-up ensuring `dense_only` profile pre-warms E5 but never initializes MiniLM.

### Removed Mechanism & Duplicate Tests
- `test_bm25_score_matches_reference_formula` (redundant reference-formula oracle).
- `test_bm25_fit_statistics`, `test_bm25_average_length_counts_non_empty_documents_only`, `test_bm25_query_terms_are_deduplicated`, `test_bm25_out_of_vocabulary_term_contributes_zero`, `test_bm25_empty_document_scores_zero`, `test_bm25_score_before_fit_raises`, `test_bm25_fit_all_empty_corpus_raises`, `test_bm25_refit_resets_state`, `test_bm25_score_is_finite` (consolidated into `test_bm25_known_hue_corpus_ranking_and_fit`).
- `test_min_max_normalize_normal_case`, `test_min_max_normalize_constant_signal_maps_to_zero`, `test_min_max_normalize_empty_input`, `test_min_max_normalize_rejects_non_finite` (consolidated into `test_min_max_normalize_properties`).
- `test_validate_weights_accepts_baseline`, `test_validate_weights_rejects_negative`, `test_validate_weights_rejects_wrong_sum`, `test_validate_weights_rejects_non_finite` (consolidated into `test_validate_weights_contract`).
- `test_budget_counts_serialized_block_and_brackets`, `test_second_whole_chunk_fits_when_budget_allows`, `test_stops_before_chunk_that_does_not_fit_without_truncation`, `test_max_documents_caps_output` (consolidated into `test_context_budget_and_document_limits`).
- `test_each_evidence_block_embeds_its_own_chunk_id`, `test_embedded_forged_label_does_not_create_a_block`, `test_source_mapping_fields_and_order` (consolidated into `test_structural_safety_and_source_mapping`).
- `test_empty_input_returns_empty_context_and_sources`, `test_empty_text_documents_are_skipped_keeping_rank` (consolidated into `test_empty_input_and_empty_text_handling`).
- `test_qdrant_network_failure_propagates_as_dependency_error` (redundant mechanism test; user-visible 503 is protected in `test_api_chat.py`).
- `test_upsert_network_failure_is_real_failure` (dead URL test).
- `test_upsert_bad_request_is_real_failure` (redundant HTTP 400 test).
- `test_validate_existing_points_accepts_real_subset`, `test_validate_existing_points_rejects_foreign_point`, `test_validate_existing_points_rejects_payload_mismatch` (redundant with pipeline-level fail-before-mutation tests).

---

## 5. Deleted Obsolete Files (10 Items)

The following 10 obsolete files and directories were completely removed:
1. `backend/embedding/sparse_embedder.py`
2. `backend/tests/test_sparse_embedder.py`
3. `backend/vectorstore/hybrid_index.py`
4. `backend/tests/test_hybrid_index.py`
5. `backend/tests/test_qdrant_schema.py`
6. `backend/reranking/base.py`
7. `backend/reranking/reranker.py`
8. `backend/reranking/models/` (including `cross_encoder.py` and `__init__.py`)
9. `backend/tests/test_reranker.py`
10. `backend/tests/test_startup.py`

---

## 6. Notebooks Run All Verification

All three Phase 4–5 notebooks were executed end-to-end using `jupyter nbconvert --execute`:
- `notebooks/03_embedding_models.ipynb`: Executed cleanly; verified E5 document/query embedding and Cosine similarity.
- `notebooks/04_qdrant_ingestion.ipynb`: Executed cleanly; verified read-only candidate collection inspection (572 points, pure dense schema).
- `notebooks/05_retrieval_profiles.ipynb`: Executed cleanly; verified all 3 profiles on candidate collection via public `build_service`.
- In-repo notebook files have outputs cleared (`outputs: []`, `execution_count: null`).

---

## 7. Constraint & Governance Compliance Verification

- [x] **Active collection read-only**: `hue_foods_e5_small_384` was never mutated, reset, or deleted (572 points, schema preserved).
- [x] **Candidate collection created**: `hue_foods_e5_small_384_dense` exists with 572 points, pure dense 384/Cosine, UUID5 point IDs.
- [x] **No premature cutover**: `settings.yaml` still targets active collection `hue_foods_e5_small_384` with `active_profile: dense_only`.
- [x] **No test doubles / mocks**: 100% of tests run against real Qdrant, E5, BM25, MiniLM.
- [x] **No git commits / pushes**: No git commit or push performed.
- [x] **Preserved dirty worktree**: Worktree preserved with intentional uncommitted changes outside scope.
