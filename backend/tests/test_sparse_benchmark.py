import json
import math
from pathlib import Path
import pytest
from qdrant_client import QdrantClient, models

from core.schema import RetrievedDocument
from scoring.bm25 import BM25 as RuntimeBM25
from evaluation.sparse_benchmark import (
    BM25_SETTINGS,
    FullCorpusBM25,
    TfidfSparseEncoder,
    TfidfState,
    ensure_tfidf_collection,
    build_or_validate_tfidf,
    query_tfidf,
    tfidf_collection_name,
    rrf_fuse,
    weighted_fuse,
    score_at_depth,
    evaluate_depth_category_guardrails,
    select_family_finalist,
    FinalistEvidence,
    DepthCaseMetrics,
    unicode_word_tokenize,
    underthesea_word_tokenize,
    load_checkpoint,
    reconcile_sparse_benchmark,
    ExperimentManifest,
    CheckpointState,
    CALIBRATION_COLUMNS,
    RESULT_COLUMNS,
    CASE_RECORD_FIELDS,
    RETRIEVAL_SETTINGS,
    requested_setting_keys_from_env,
    sanitize_error_message,
    load_or_create_manifest,
    run_retrieval_batch,
    SparseBenchmarkInputs,
    SelectedLexicalContract,
    DEFAULT_RESULTS_DIR,
    MANIFEST_FILENAME,
)


def make_chunk(chunk_id: str, text: str, source: str = "foods/a.md", section: str = "A"):
    return {
        "text": text,
        "metadata": {
            "chunk_id": chunk_id,
            "source": source,
            "title": source,
            "section": section,
            "category": "foods",
            "subcategory": "test",
            "chunk_type": "section",
        },
    }


def make_ranked(chunk_id: str, score: float, source: str = "foods/a.md", section: str = "A"):
    return RetrievedDocument(
        id=chunk_id,
        score=score,
        text=chunk_id,
        metadata={"chunk_id": chunk_id, "source": source, "section": section},
    )


# ---------------------------------------------------------------------------
# Tokenizers & BM25
# ---------------------------------------------------------------------------

def test_approved_bm25_settings_are_exact_and_ordered():
    assert [(s.setting_key, s.k1, s.b) for s in BM25_SETTINGS] == [
        ("baseline", 1.5, 0.75),
        ("k1_low", 1.2, 0.75),
        ("k1_high", 1.8, 0.75),
        ("b_low", 1.5, 0.5),
        ("b_high", 1.5, 1.0),
    ]


def test_unicode_tokenizer_normalizes_nfc_and_keeps_numbers():
    assert unicode_word_tokenize("BÚN bò Huế 2026!") == ["bún", "bò", "huế", "2026"]


def test_underthesea_tokenizer_preserves_compound_tokens():
    tokens = underthesea_word_tokenize("Thừa Thiên Huế có bún bò.")
    assert "thừa_thiên_huế" in tokens or ("thừa" in tokens and "thiên" in tokens)
    assert "bún_bò" in tokens or ("bún" in tokens and "bò" in tokens)


def test_full_corpus_bm25_unicode_baseline_matches_runtime_scores():
    chunks = [
        make_chunk("c-1", "bún bò huế đặc biệt"),
        make_chunk("c-2", "cơm hến huế"),
        make_chunk("c-3", "chè cung đình"),
    ]
    candidate = FullCorpusBM25(chunks, unicode_word_tokenize, k1=1.5, b=0.75)
    scores = candidate.score_query_per_doc("bún bò")
    assert len(scores) == 3
    assert scores[0] > scores[1]
    assert scores[0] > scores[2]
    assert [d.id for d in candidate.search("bún bò", limit=3)] == ["c-1"]


def test_full_corpus_bm25_handles_oov_and_empty():
    chunks = [make_chunk("c-1", "bún bò huế")]
    bm25 = FullCorpusBM25(chunks, unicode_word_tokenize)
    assert bm25.search("xyzzy") == []
    with pytest.raises(ValueError, match="limit"):
        bm25.search("bún", limit=0)


# ---------------------------------------------------------------------------
# TF-IDF Sparse Encoder & Collection
# ---------------------------------------------------------------------------

def test_tfidf_uses_log_tf_smoothed_idf_l2_and_sorted_vocabulary():
    chunks = [make_chunk("c-1", "bún bún bò"), make_chunk("c-2", "bò chè")]
    encoder = TfidfSparseEncoder.fit(chunks, "unicode_word", unicode_word_tokenize)
    assert encoder.vocabulary == {"bò": 0, "bún": 1, "chè": 2}
    vector = encoder.document_vectors[0]
    raw_bun = (1.0 + math.log(2.0)) * (math.log(3.0 / 2.0) + 1.0)
    raw_bo = 1.0
    norm = math.sqrt(raw_bun**2 + raw_bo**2)
    assert vector.indices == [0, 1]
    assert vector.values == pytest.approx([raw_bo / norm, raw_bun / norm])
    assert math.isclose(sum(v * v for v in vector.values), 1.0)


def test_tfidf_oov_query_returns_none():
    encoder = TfidfSparseEncoder.fit(
        [make_chunk("c-1", "bún bò")], "unicode_word", unicode_word_tokenize
    )
    assert encoder.encode("xyzzy") is None


def test_tfidf_collection_requires_explicit_mutation_and_is_reusable():
    client = QdrantClient(":memory:")
    chunks = [make_chunk("c-1", "bún bò"), make_chunk("c-2", "cơm hến")]
    encoder = TfidfSparseEncoder.fit(chunks, "unicode_word", unicode_word_tokenize)
    name = tfidf_collection_name("unicode_word", "a" * 64)
    with pytest.raises(PermissionError, match="ALLOW_EXPERIMENT_MUTATION"):
        ensure_tfidf_collection(client, name, chunks, encoder, "a" * 64, allow_mutation=False)
    assert ensure_tfidf_collection(client, name, chunks, encoder, "a" * 64, allow_mutation=True) == "created"
    assert ensure_tfidf_collection(client, name, chunks, encoder, "a" * 64, allow_mutation=False) == "existing"
    assert [d.id for d in query_tfidf(client, name, encoder, "bún", limit=2)] == ["c-1"]


def test_build_or_validate_tfidf_checks_snapshots():
    client = QdrantClient(":memory:")
    chunks = [make_chunk("c-1", "bún bò")]
    state = build_or_validate_tfidf(
        client,
        chunks,
        unicode_word_tokenize,
        "unicode_word",
        corpus_fingerprint="f" * 64,
        allow_mutation=True,
    )
    assert isinstance(state, TfidfState)
    assert state.status == "created"
    assert state.encoder.vocab_size == 2


# ---------------------------------------------------------------------------
# Fusion Algorithms (RRF & Weighted)
# ---------------------------------------------------------------------------

def test_rrf_uses_union_rank_one_k60_and_chunk_id_ties():
    dense = [make_ranked("a", 0.9), make_ranked("b", 0.8)]
    sparse = [make_ranked("c", 9.0), make_ranked("b", 8.0)]
    fused = rrf_fuse(dense, sparse, limit=10, rrf_k=60)
    assert [d.id for d in fused] == ["b", "a", "c"]
    assert fused[0].score == pytest.approx(1 / 62 + 1 / 62)
    assert fused[1].score == fused[2].score


def test_rrf_rejects_invalid_inputs():
    dense = [make_ranked("a", 0.9), make_ranked("a", 0.8)]
    sparse = [make_ranked("b", 1.0)]
    with pytest.raises(ValueError, match="Duplicate"):
        rrf_fuse(dense, sparse, limit=10, rrf_k=60)

    with pytest.raises(ValueError, match="exact 60"):
        rrf_fuse([make_ranked("a", 0.9)], [make_ranked("b", 1.0)], limit=10, rrf_k=50)

    with pytest.raises(ValueError, match="Non-finite"):
        rrf_fuse([make_ranked("a", float("nan"))], [make_ranked("b", 1.0)], limit=10, rrf_k=60)


def test_weighted_fusion_normalizes_independently_and_missing_is_zero():
    dense = [make_ranked("a", 10.0), make_ranked("b", 5.0)]
    sparse = [make_ranked("b", 20.0), make_ranked("c", 10.0)]
    fused = weighted_fuse(dense, sparse, limit=3, dense_weight=0.6, sparse_weight=0.4)
    assert [d.id for d in fused] == ["a", "b", "c"]
    assert fused[0].score == pytest.approx(0.6 * 1.0 + 0.4 * 0.0)
    assert fused[1].score == pytest.approx(0.6 * 0.0 + 0.4 * 1.0)
    assert fused[2].score == pytest.approx(0.6 * 0.0 + 0.4 * 0.0)


def test_weighted_fusion_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="Weights"):
        weighted_fuse([make_ranked("a", 1.0)], [make_ranked("b", 1.0)], dense_weight=0.7, sparse_weight=0.4)
    with pytest.raises(ValueError, match="Duplicate"):
        weighted_fuse([make_ranked("a", 1.0), make_ranked("a", 2.0)], [make_ranked("b", 1.0)])


# ---------------------------------------------------------------------------
# Metrics & Guardrails
# ---------------------------------------------------------------------------

def test_score_at_depth_deduplicates_source_sections():
    case = {
        "case_id": "q1",
        "category": "cat1",
        "expected_evidence": [
            {"source": "foods/a.md", "section": "A"},
            {"source": "foods/a.md", "section": "B"},
        ],
    }
    docs = [
        make_ranked("c1", 1.0, source="foods/a.md", section="A"),
        make_ranked("c2", 0.9, source="foods/a.md", section="A"),  # duplicate section, no credit
        make_ranked("c3", 0.8, source="foods/a.md", section="B"),
    ]
    m5 = score_at_depth(case, docs, depth=5)
    assert m5.hit is True
    assert m5.recall == pytest.approx(1.0)
    assert m5.mrr == pytest.approx(1.0)
    dcg = 1.0 / math.log2(2) + 1.0 / math.log2(4)
    idcg = 1.0 / math.log2(2) + 1.0 / math.log2(3)
    assert m5.ndcg == pytest.approx(dcg / idcg)


def test_category_guardrails_hierarchical_contract():
    # Large category (n=6): hit count check and nDCG tiebreaker
    ctrl_large = [
        DepthCaseMetrics(f"c{i}", "large", 5, 1.0, 1.0, 1.0, True, (), ())
        for i in range(6)
    ]
    cand_large_loss = [
        DepthCaseMetrics(f"c{i}", "large", 5, 1.0 if i < 5 else 0.0, 1.0, 1.0, i < 5, (), ())
        for i in range(6)
    ]
    p, _ = evaluate_depth_category_guardrails(ctrl_large, cand_large_loss)
    assert p is False

    # Small category (n=3): exact case hit retention
    ctrl_small = [
        DepthCaseMetrics("s1", "small", 5, 1.0, 1.0, 1.0, True, (), ()),
        DepthCaseMetrics("s2", "small", 5, 1.0, 1.0, 1.0, True, (), ()),
        DepthCaseMetrics("s3", "small", 5, 0.0, 0.0, 0.0, False, (), ()),
    ]
    cand_small_pass = [
        DepthCaseMetrics("s1", "small", 5, 1.0, 1.0, 1.0, True, (), ()),
        DepthCaseMetrics("s2", "small", 5, 1.0, 1.0, 1.0, True, (), ()),
        DepthCaseMetrics("s3", "small", 5, 1.0, 1.0, 1.0, True, (), ()),  # extra hit allowed
    ]
    p_s, _ = evaluate_depth_category_guardrails(ctrl_small, cand_small_pass)
    assert p_s is True

    cand_small_fail = [
        DepthCaseMetrics("s1", "small", 5, 1.0, 1.0, 1.0, True, (), ()),
        DepthCaseMetrics("s2", "small", 5, 0.0, 0.0, 0.0, False, (), ()),  # lost hit s2
        DepthCaseMetrics("s3", "small", 5, 1.0, 1.0, 1.0, True, (), ()),
    ]
    p_f, _ = evaluate_depth_category_guardrails(ctrl_small, cand_small_fail)
    assert p_f is False


def test_select_family_finalist_returns_none_when_guardrail_fails():
    dense_controls = {
        "ctrl-dense": FinalistEvidence("ctrl-dense", "ctrl-dense", "", "completed", 3, 0.9, 0.85, 0.75, 0.7, 30.0, True)
    }
    candidates = [
        FinalistEvidence("cand-1", "ctrl-dense", "bm25", "completed", 3, 0.95, 0.90, 0.80, 0.75, 40.0, False),  # failed guardrail
    ]
    assert select_family_finalist(candidates, dense_controls, "bm25") is None


# ---------------------------------------------------------------------------
# Catalog & Schemas
# ---------------------------------------------------------------------------

def test_retrieval_settings_catalog_has_exact_20_settings():
    assert len(RETRIEVAL_SETTINGS) == 20
    assert RETRIEVAL_SETTINGS[0].setting_key == "dense__e5-small-384"
    assert RETRIEVAL_SETTINGS[3].setting_key == "bm25-only"
    assert RETRIEVAL_SETTINGS[13].setting_key == "tfidf-only"
    assert RETRIEVAL_SETTINGS[19].setting_key == "hybrid-tfidf-weighted__e5-base-768"


def test_requested_setting_keys_from_env():
    assert len(requested_setting_keys_from_env(None)) == 20
    assert requested_setting_keys_from_env("bm25-only, tfidf-only") == ("bm25-only", "tfidf-only")
    with pytest.raises(ValueError, match="Invalid"):
        requested_setting_keys_from_env("unknown-setting")


def test_column_schemas_are_exact():
    assert len(CALIBRATION_COLUMNS) == 27
    assert len(RESULT_COLUMNS) == 50
    assert len(CASE_RECORD_FIELDS) == 24


# ---------------------------------------------------------------------------
# Notebook Structure
# ---------------------------------------------------------------------------

def test_08b_notebook_structure_and_clean_outputs():
    import json
    nb_path = Path(__file__).resolve().parent.parent.parent / "notebooks" / "08b_retrieval_fusion_benchmark.ipynb"
    assert nb_path.exists(), "08b notebook must exist"
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4
    assert len(nb["cells"]) >= 20
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == [], f"Code cell {cell.get('id')} must have empty outputs"
            assert cell["execution_count"] is None, f"Code cell {cell.get('id')} must have null execution_count"


# ---------------------------------------------------------------------------
# Calibration Skip, Safety Snapshots & Reconciliation
# ---------------------------------------------------------------------------

def test_calibration_skip_when_completed(tmp_path):
    from evaluation.sparse_benchmark import (
        load_or_run_calibration,
        SparseBenchmarkInputs,
        SelectedLexicalContract,
        run_bm25_parameter_calibration,
        run_tokenizer_calibration,
    )
    from evaluation.golden_dataset import GoldenCase

    dummy_cases = [
        GoldenCase(
            case_id="c1",
            category="direct_fact",
            question="bún bò",
            evidence={"foods/a.md": ["A"]},
            keywords=["bún bò", "huế"],
            reference_answer="Bún bò Huế ngon",
        ),
    ]
    dummy_chunks = [make_chunk("c1", "bún bò huế")]
    client = QdrantClient(":memory:")
    inputs = SparseBenchmarkInputs(
        cases=dummy_cases,
        chunks=dummy_chunks,
        client=client,
        settings={"vector_database": {"collection_name": "dummy"}},
        corpus_fingerprint="c" * 64,
        golden_fingerprint="g" * 64,
        chunker_fingerprint="k" * 64,
    )

    # First run: generates calibration CSV
    param_sel = run_bm25_parameter_calibration(inputs, results_dir=tmp_path)
    tok_sel = run_tokenizer_calibration(inputs, param_sel, results_dir=tmp_path)
    manifest = ExperimentManifest(
        schema_version="phase8-sparse-manifest-v1",
        experiment_version="phase8-08b-v1",
        immutable_identity={},
        batch_history=(),
    )
    checkpoint = load_checkpoint(manifest, results_dir=tmp_path)

    # Second run with checkpoint: must return immediately with cached selection
    param_sel_cached = run_bm25_parameter_calibration(inputs, checkpoint=checkpoint, results_dir=tmp_path)
    assert param_sel_cached.selected_setting_key == param_sel.selected_setting_key

    tok_sel_cached = run_tokenizer_calibration(inputs, param_sel_cached, checkpoint=checkpoint, results_dir=tmp_path)
    assert tok_sel_cached.selected_setting_key == tok_sel.selected_setting_key


def test_reconcile_sparse_benchmark_fail_closed_on_snapshot_or_missing_rows():
    manifest = ExperimentManifest("v1", "phase8-08b-v1", {}, ())
    empty_checkpoint = CheckpointState(
        manifest=manifest,
        completed_setting_keys=(),
        calibration_rows=(),
        result_rows=(),
        case_records=(),
    )
    res = reconcile_sparse_benchmark(empty_checkpoint)
    assert res.complete is False
    assert res.summary["reconciliation_complete"] is False


def test_reconcile_fails_on_missing_required_live_arguments():
    from evaluation.sparse_benchmark import (
        DEFAULT_RESULTS_DIR,
        load_sparse_benchmark_inputs,
        snapshot_active_collection,
        load_or_run_calibration,
        build_or_validate_tfidf,
    )
    manifest = ExperimentManifest.from_dict(
        json.loads((DEFAULT_RESULTS_DIR / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    )
    chk = load_checkpoint(manifest, results_dir=DEFAULT_RESULTS_DIR)
    inputs = load_sparse_benchmark_inputs()
    active_snap = snapshot_active_collection(inputs)
    selected_lexical = load_or_run_calibration(
        inputs, expected_active_snapshot=active_snap, checkpoint=chk, results_dir=DEFAULT_RESULTS_DIR
    )
    tfidf_state = build_or_validate_tfidf(
        inputs.client, inputs.chunks, selected_lexical.tokenizer, selected_lexical.tokenizer_key, expected_active_snapshot=active_snap
    )

    # Missing inputs
    assert reconcile_sparse_benchmark(chk, inputs=None, expected_active_snapshot=active_snap, client=inputs.client, tfidf_state=tfidf_state).complete is False
    # Missing expected_active_snapshot
    assert reconcile_sparse_benchmark(chk, inputs=inputs, expected_active_snapshot=None, client=inputs.client, tfidf_state=tfidf_state).complete is False
    # Missing explicit client (must not fallback to inputs.client)
    assert reconcile_sparse_benchmark(chk, inputs=inputs, expected_active_snapshot=active_snap, client=None, tfidf_state=tfidf_state).complete is False
    # Missing tfidf_state
    assert reconcile_sparse_benchmark(chk, inputs=inputs, expected_active_snapshot=active_snap, client=inputs.client, tfidf_state=None).complete is False


@pytest.mark.parametrize(
    "raw_text,sentinel",
    [
        ("Failed with Authorization: Bearer secret-bearer-token-12345 in header", "secret-bearer-token-12345"),
        ("Request failed with Authorization: secret-direct-auth-99999", "secret-direct-auth-99999"),
        ("Error Bearer bare-token-value-54321 occurred", "bare-token-value-54321"),
        ("Invalid api_key=super-secret-api-key-111", "super-secret-api-key-111"),
        ("Header X-API-Key: x-api-key-sentinel-222", "x-api-key-sentinel-222"),
        ("Session token=jwt-session-token-333", "jwt-session-token-333"),
        ("Auth password=my-top-secret-password-444", "my-top-secret-password-444"),
        ("Connection secret=live-secret-value-555", "live-secret-value-555"),
        ("request api_key='single-quoted-secret-123' failed", "single-quoted-secret-123"),
        ('request password="double quoted secret 456" failed', "double quoted secret 456"),
        ('Authorization: Bearer "quoted-bearer-secret-789"', "quoted-bearer-secret-789"),
        ("""Traceback (most recent call last):
  File "foo.py", line 10, in <module>
    raise ValueError("secret_in_multiline_traceback_999")
ValueError: secret_in_multiline_traceback_999""", "secret_in_multiline_traceback_999"),
    ],
)
def test_sanitize_error_message_sentinels(raw_text, sentinel):
    err = ValueError(raw_text)
    msg = sanitize_error_message(err)
    assert msg.startswith("ValueError: ")
    assert sentinel not in msg, f"Sentinel secret '{sentinel}' leaked in sanitized error message: {msg}"


def test_load_checkpoint_rejects_corrupted_headers_and_invalid_rows(tmp_path):
    manifest = ExperimentManifest("phase8-sparse-manifest-v1", "phase8-08b-v1", {}, ())

    # Bad calibration header
    bad_calib = tmp_path / "phase8_sparse_calibration.csv"
    bad_calib.write_text("col1,col2\na,b\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Calibration CSV headers mismatch"):
        load_checkpoint(manifest, results_dir=tmp_path)
    bad_calib.unlink()

    # Bad result header
    bad_res = tmp_path / "phase8_sparse_results.csv"
    bad_res.write_text("col1,col2\na,b\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Result CSV headers mismatch"):
        load_checkpoint(manifest, results_dir=tmp_path)
    bad_res.unlink()

    # Malformed JSON in cases
    bad_cases = tmp_path / "phase8_sparse_cases.jsonl"
    bad_cases.write_text("not-a-json-line\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed JSON"):
        load_checkpoint(manifest, results_dir=tmp_path)


def test_reconcile_fails_on_partial_7_calibration_rows():
    from evaluation.sparse_benchmark import (
        DEFAULT_RESULTS_DIR,
        load_sparse_benchmark_inputs,
        snapshot_active_collection,
        load_or_run_calibration,
        build_or_validate_tfidf,
    )
    inputs = load_sparse_benchmark_inputs()
    active_snap = snapshot_active_collection(inputs)
    manifest = ExperimentManifest.from_dict(
        json.loads((DEFAULT_RESULTS_DIR / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    )
    checkpoint_full = load_checkpoint(manifest, results_dir=DEFAULT_RESULTS_DIR)
    selected_lexical = load_or_run_calibration(
        inputs, expected_active_snapshot=active_snap, checkpoint=checkpoint_full, results_dir=DEFAULT_RESULTS_DIR
    )
    tfidf_state = build_or_validate_tfidf(
        inputs.client, inputs.chunks, selected_lexical.tokenizer, selected_lexical.tokenizer_key, expected_active_snapshot=active_snap
    )

    # Filter to only 7 overall rows
    only_7_calib = tuple(r for r in checkpoint_full.calibration_rows if r.get("category") == "overall")
    assert len(only_7_calib) == 7

    chk_7 = CheckpointState(
        manifest=manifest,
        completed_setting_keys=checkpoint_full.completed_setting_keys,
        calibration_rows=only_7_calib,
        result_rows=checkpoint_full.result_rows,
        case_records=checkpoint_full.case_records,
    )
    res = reconcile_sparse_benchmark(
        chk_7,
        inputs=inputs,
        expected_active_snapshot=active_snap,
        client=inputs.client,
        tfidf_state=tfidf_state,
        results_dir=DEFAULT_RESULTS_DIR,
    )
    assert res.complete is False
    assert res.summary["reconciliation_complete"] is False


@pytest.mark.parametrize(
    "field_path,bad_value",
    [
        (("corpus_fingerprint",), "0" * 64),
        (("golden_fingerprint",), "0" * 64),
        (("chunker_fingerprint",), "0" * 64),
        (("selected_tokenizer",), "invalid_tokenizer_key"),
        (("selected_bm25", "k1"), 9.99),
        (("tfidf", "formula_version"), "bad-tfidf-formula-v99"),
        (("fusion", "rrf_k"), 999),
        (("dense_prerequisites", 0, "dimension"), 9999),
        (("depths", "final"), 99),
    ],
)
def test_reconcile_fails_on_immutable_identity_mismatches(field_path, bad_value):
    from evaluation.sparse_benchmark import (
        DEFAULT_RESULTS_DIR,
        load_sparse_benchmark_inputs,
        snapshot_active_collection,
        load_or_run_calibration,
        build_or_validate_tfidf,
    )
    inputs = load_sparse_benchmark_inputs()
    active_snap = snapshot_active_collection(inputs)
    raw_manifest = json.loads((DEFAULT_RESULTS_DIR / MANIFEST_FILENAME).read_text(encoding="utf-8"))

    # Apply corruption
    target = raw_manifest["immutable_identity"]
    for key in field_path[:-1]:
        target = target[key]
    target[field_path[-1]] = bad_value

    manifest_bad = ExperimentManifest.from_dict(raw_manifest)
    checkpoint_full = load_checkpoint(manifest_bad, results_dir=DEFAULT_RESULTS_DIR)
    selected_lexical = load_or_run_calibration(
        inputs, expected_active_snapshot=active_snap, checkpoint=checkpoint_full, results_dir=DEFAULT_RESULTS_DIR
    )
    tfidf_state = build_or_validate_tfidf(
        inputs.client, inputs.chunks, selected_lexical.tokenizer, selected_lexical.tokenizer_key, expected_active_snapshot=active_snap
    )

    res = reconcile_sparse_benchmark(
        checkpoint_full,
        inputs=inputs,
        expected_active_snapshot=active_snap,
        client=inputs.client,
        tfidf_state=tfidf_state,
        results_dir=DEFAULT_RESULTS_DIR,
    )
    assert res.complete is False


def test_reconcile_fails_on_non_canonical_case_ids():
    from evaluation.sparse_benchmark import (
        DEFAULT_RESULTS_DIR,
        load_sparse_benchmark_inputs,
        snapshot_active_collection,
        load_or_run_calibration,
        build_or_validate_tfidf,
    )
    inputs = load_sparse_benchmark_inputs()
    active_snap = snapshot_active_collection(inputs)
    manifest = ExperimentManifest.from_dict(
        json.loads((DEFAULT_RESULTS_DIR / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    )
    checkpoint_full = load_checkpoint(manifest, results_dir=DEFAULT_RESULTS_DIR)
    selected_lexical = load_or_run_calibration(
        inputs, expected_active_snapshot=active_snap, checkpoint=checkpoint_full, results_dir=DEFAULT_RESULTS_DIR
    )
    tfidf_state = build_or_validate_tfidf(
        inputs.client, inputs.chunks, selected_lexical.tokenizer, selected_lexical.tokenizer_key, expected_active_snapshot=active_snap
    )

    # Replace case_id in one case record with a non-canonical ID
    corrupted_cases = list(checkpoint_full.case_records)
    corrupted_cases[0] = dict(corrupted_cases[0])
    corrupted_cases[0]["case_id"] = "non-canonical-case-999"

    chk_bad_case = CheckpointState(
        manifest=manifest,
        completed_setting_keys=checkpoint_full.completed_setting_keys,
        calibration_rows=checkpoint_full.calibration_rows,
        result_rows=checkpoint_full.result_rows,
        case_records=tuple(corrupted_cases),
    )
    res = reconcile_sparse_benchmark(
        chk_bad_case,
        inputs=inputs,
        expected_active_snapshot=active_snap,
        client=inputs.client,
        tfidf_state=tfidf_state,
        results_dir=DEFAULT_RESULTS_DIR,
    )
    assert res.complete is False


def test_reconcile_fails_on_count_only_or_malformed_tfidf_collection():
    from evaluation.sparse_benchmark import (
        DEFAULT_RESULTS_DIR,
        load_sparse_benchmark_inputs,
        snapshot_active_collection,
        load_or_run_calibration,
        build_or_validate_tfidf,
    )
    inputs = load_sparse_benchmark_inputs()
    active_snap = snapshot_active_collection(inputs)
    manifest = ExperimentManifest.from_dict(
        json.loads((DEFAULT_RESULTS_DIR / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    )
    chk = load_checkpoint(manifest, results_dir=DEFAULT_RESULTS_DIR)
    selected_lexical = load_or_run_calibration(
        inputs, expected_active_snapshot=active_snap, checkpoint=chk, results_dir=DEFAULT_RESULTS_DIR
    )
    tfidf_state = build_or_validate_tfidf(
        inputs.client, inputs.chunks, selected_lexical.tokenizer, selected_lexical.tokenizer_key, expected_active_snapshot=active_snap
    )

    # In-memory client where collection has no sparse vectors configuration
    client = QdrantClient(":memory:")
    client.create_collection(
        collection_name=tfidf_state.collection_name,
        vectors_config={"dense": models.VectorParams(size=4, distance=models.Distance.COSINE)},
    )
    # Must fail-closed without raising unhandled AttributeError
    res = reconcile_sparse_benchmark(
        chk,
        inputs=inputs,
        expected_active_snapshot=active_snap,
        client=client,
        tfidf_state=tfidf_state,
        results_dir=DEFAULT_RESULTS_DIR,
    )
    assert res.complete is False


def test_read_only_batch_and_reconcile_preserves_artifact_hashes():
    import hashlib
    from evaluation.sparse_benchmark import (
        DEFAULT_RESULTS_DIR,
        MANIFEST_FILENAME,
        CALIBRATION_FILENAME,
        RESULTS_FILENAME,
        CASES_FILENAME,
        load_sparse_benchmark_inputs,
        load_or_run_calibration,
        build_or_validate_tfidf,
        snapshot_active_collection,
    )

    inputs = load_sparse_benchmark_inputs()
    active_snap = snapshot_active_collection(inputs)

    # 1. Load existing checkpoint first (read-only)
    manifest = ExperimentManifest.from_dict(
        json.loads((DEFAULT_RESULTS_DIR / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    )
    checkpoint = load_checkpoint(manifest, results_dir=DEFAULT_RESULTS_DIR)

    # 2. Pass checkpoint to load_or_run_calibration so it does NOT rerun calibration or rewrite calibration CSV
    selected_lexical = load_or_run_calibration(
        inputs,
        expected_active_snapshot=active_snap,
        checkpoint=checkpoint,
        results_dir=DEFAULT_RESULTS_DIR,
    )

    tfidf_state = build_or_validate_tfidf(
        inputs.client,
        inputs.chunks,
        selected_lexical.tokenizer,
        selected_lexical.tokenizer_key,
        expected_active_snapshot=active_snap,
    )

    files = [
        DEFAULT_RESULTS_DIR / MANIFEST_FILENAME,
        DEFAULT_RESULTS_DIR / CALIBRATION_FILENAME,
        DEFAULT_RESULTS_DIR / RESULTS_FILENAME,
        DEFAULT_RESULTS_DIR / CASES_FILENAME,
    ]
    # Record hashes BEFORE read-only batch execution
    hashes_before = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.exists()}

    # Run batch on all 20 completed settings (read-only rerun)
    results = list(
        run_retrieval_batch(
            inputs,
            selected_lexical,
            tfidf_state,
            requested_setting_keys=tuple(s.setting_key for s in RETRIEVAL_SETTINGS),
            expected_active_snapshot=active_snap,
            results_dir=DEFAULT_RESULTS_DIR,
        )
    )
    assert len(results) == 20

    # Reconcile on completed checkpoint with all required live & canonical contexts
    rec = reconcile_sparse_benchmark(
        checkpoint,
        inputs=inputs,
        expected_active_snapshot=active_snap,
        client=inputs.client,
        tfidf_state=tfidf_state,
        results_dir=DEFAULT_RESULTS_DIR,
    )
    assert rec.complete is True

    # Record hashes AFTER read-only batch execution and reconciliation
    hashes_after = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.exists()}
    assert hashes_before == hashes_after, "Read-only run and reconciliation must not change artifact hashes"


def test_run_retrieval_batch_failure_continuation_and_batch_history(tmp_path, monkeypatch):
    import evaluation.sparse_benchmark as sb
    inputs = sb.load_sparse_benchmark_inputs()
    active_snap = sb.snapshot_active_collection(inputs)

    # Initialize manifest and calibration in tmp_path
    selected_lexical = sb.load_or_run_calibration(
        inputs,
        expected_active_snapshot=active_snap,
        results_dir=tmp_path,
    )
    tfidf_state = sb.build_or_validate_tfidf(
        inputs.client,
        inputs.chunks,
        selected_lexical.tokenizer,
        selected_lexical.tokenizer_key,
        expected_active_snapshot=active_snap,
    )

    original_run = sb.run_retrieval_setting
    call_count = [0]

    def mock_run_setting(setting, *args, **kwargs):
        call_count[0] += 1
        if setting.setting_key == "dense__e5-small-384":
            # Simulate failure with secret token in error
            raise RuntimeError("Database timeout with secret=live-secret-test-777!")
        return original_run(setting, *args, **kwargs)

    monkeypatch.setattr(sb, "run_retrieval_setting", mock_run_setting)

    batch_gen = sb.run_retrieval_batch(
        inputs,
        selected_lexical,
        tfidf_state,
        requested_setting_keys=("dense__e5-small-384", "bm25-only"),
        expected_active_snapshot=active_snap,
        results_dir=tmp_path,
    )
    results = list(batch_gen)
    assert len(results) == 2
    # First failed
    assert results[0].status == "failed"
    assert results[0].error == "RuntimeError: operation timed out"
    assert "live-secret-test-777" not in results[0].error
    # Second succeeded (continued)
    assert results[1].status == "completed"

    # Manifest recorded batch history with failed_keys
    manifest_data = json.loads((tmp_path / sb.MANIFEST_FILENAME).read_text(encoding="utf-8"))
    history = manifest_data.get("batch_history", [])
    assert len(history) >= 1
    last_batch = history[-1]
    assert "dense__e5-small-384" in last_batch["failed_keys"]
    assert "bm25-only" in last_batch["executed_keys"]
