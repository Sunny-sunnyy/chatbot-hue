"""Deterministic tests for full-corpus sparse representation state and BM25 equivalence."""

import math
from pathlib import Path
import pytest

from backend.core.schema import FullCorpusChunk
from backend.embedding.sparse import (
    SparseState,
    SparseVector,
    compute_corpus_identity,
    encode_sparse_document,
    encode_sparse_query,
    fit_sparse_state,
    load_sparse_state,
    serialize_sparse_state,
    write_sparse_state,
)
from backend.scoring.bm25 import BM25


def make_chunk(chunk_id: str, text: str) -> FullCorpusChunk:
    return FullCorpusChunk(
        chunk_id=chunk_id,
        source="knowledge-base-hue/foods/test.md",
        title="Tiêu đề thử nghiệm",
        heading_path=["Mục 1"],
        evidence_parts=[],
        search_text=text,
    )


def test_sparse_state_fitting_and_properties() -> None:
    chunks = [
        make_chunk("c1", "bún bò huế"),
        make_chunk("c2", "bún hến"),
        make_chunk("c3", ""),
    ]
    state = fit_sparse_state(chunks)
    assert state.document_count == 2
    assert state.average_document_length == pytest.approx(2.5)
    assert state.k1 == 1.5
    assert state.b == 0.75
    assert state.tokenizer == "backend.scoring.bm25.tokenize:v1"
    assert state.vocabulary == tuple(sorted({"bún", "bò", "huế", "hến"}))
    assert len(state.idf) == len(state.vocabulary)
    assert all(math.isfinite(val) for val in state.idf)


def test_sparse_state_empty_corpus_raises() -> None:
    chunks = [make_chunk("c1", ""), make_chunk("c2", "   ")]
    with pytest.raises(ValueError, match="no non-empty documents"):
        fit_sparse_state(chunks)


def test_sparse_state_duplicate_chunk_id_raises() -> None:
    chunks = [
        make_chunk("c1", "bún bò"),
        make_chunk("c1", "bún riêu"),
    ]
    with pytest.raises(ValueError, match="Duplicate chunk_id"):
        compute_corpus_identity(chunks)


def test_corpus_identity_changes_with_order_or_content() -> None:
    c1 = make_chunk("c1", "bún bò")
    c2 = make_chunk("c2", "bún hến")

    id1 = compute_corpus_identity([c1, c2])
    id2 = compute_corpus_identity([c2, c1])
    id3 = compute_corpus_identity([c1, make_chunk("c2", "cơm hến")])

    assert id1 != id2
    assert id1 != id3
    assert len(id1) == 64  # SHA-256 hex digest


def test_encode_sparse_empty_and_oov() -> None:
    chunks = [make_chunk("c1", "bún bò huế")]
    state = fit_sparse_state(chunks)

    assert encode_sparse_document("", state) == SparseVector(indices=(), values=())
    assert encode_sparse_document("   ", state) == SparseVector(indices=(), values=())
    assert encode_sparse_document("phở hà nội", state) == SparseVector(indices=(), values=())

    assert encode_sparse_query("", state) == SparseVector(indices=(), values=())
    assert encode_sparse_query("   ", state) == SparseVector(indices=(), values=())
    assert encode_sparse_query("phở gà", state) == SparseVector(indices=(), values=())


def test_encode_sparse_document_and_query_bm25_equivalence() -> None:
    raw_texts = [
        "Đại Nội Huế là quần thể di tích lịch sử nổi tiếng",
        "Bún bò Huế và cơm hến là đặc sản ẩm thực Huế",
        "Lễ hội Festival Huế thu hút đông đảo du khách tham quan di tích",
    ]
    chunks = [make_chunk(f"doc_{i}", text) for i, text in enumerate(raw_texts)]

    bm25 = BM25().fit(raw_texts)
    state = fit_sparse_state(chunks)

    queries = [
        "di tích Đại Nội Huế",
        "ẩm thực món ăn bún bò đặc sản",
        "du lịch Festival Huế tham quan",
        "món lạ không có trong từ điển",
    ]

    for q in queries:
        sparse_query = encode_sparse_query(q, state)
        for doc_text in raw_texts:
            sparse_doc = encode_sparse_document(doc_text, state)

            # Tính tích vô hướng giữa query vector và document vector
            doc_map = dict(zip(sparse_doc.indices, sparse_doc.values))
            dot_product = sum(doc_map.get(idx, 0.0) * val for idx, val in zip(sparse_query.indices, sparse_query.values))

            bm25_score = bm25.score(q, doc_text)
            assert dot_product == pytest.approx(bm25_score, rel=1e-5, abs=1e-7)


def test_sparse_state_serialization_determinism_and_roundtrip(tmp_path: Path) -> None:
    chunks = [
        make_chunk("c1", "bún bò huế đặc sản"),
        make_chunk("c2", "chè heo quay món ngon xứ huế"),
    ]
    state = fit_sparse_state(chunks)

    path1 = tmp_path / "sparse_1.json"
    path2 = tmp_path / "sparse_2.json"

    sha1 = write_sparse_state(state, path1)
    sha2 = write_sparse_state(state, path2)

    bytes1 = path1.read_bytes()
    bytes2 = path2.read_bytes()

    assert bytes1 == bytes2
    assert sha1 == sha2

    # Roundtrip check
    loaded = load_sparse_state(path1)
    assert loaded == state
    assert serialize_sparse_state(loaded) == bytes1

    # Khẳng định không chứa document vectors trong tệp
    text_content = path1.read_text(encoding="utf-8")
    assert "c1" not in text_content
    assert "doc_" not in text_content


def test_load_sparse_state_validation_failures(tmp_path: Path) -> None:
    valid_chunks = [make_chunk("c1", "bún bò")]
    state = fit_sparse_state(valid_chunks)

    valid_path = tmp_path / "valid.json"
    write_sparse_state(state, valid_path)
    base_text = valid_path.read_text(encoding="utf-8")

    import json

    # 1. Sai schema version
    bad_schema = json.loads(base_text)
    bad_schema["schema_version"] = "unknown:v99"
    p = tmp_path / "bad_schema.json"
    p.write_text(json.dumps(bad_schema), encoding="utf-8")
    with pytest.raises(ValueError, match="Unknown schema version"):
        load_sparse_state(p)

    # 2. Sai hằng số k1 hoặc b
    bad_k1 = json.loads(base_text)
    bad_k1["k1"] = 1.2
    p = tmp_path / "bad_k1.json"
    p.write_text(json.dumps(bad_k1), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid BM25 constants"):
        load_sparse_state(p)

    # 3. Sai tokenizer
    bad_tok = json.loads(base_text)
    bad_tok["tokenizer"] = "other_tokenizer"
    p = tmp_path / "bad_tok.json"
    p.write_text(json.dumps(bad_tok), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid tokenizer"):
        load_sparse_state(p)

    # 4. Vocabulary không sắp xếp từ điển
    bad_vocab = json.loads(base_text)
    bad_vocab["vocabulary"] = ["huế", "bún"]
    p = tmp_path / "bad_vocab.json"
    p.write_text(json.dumps(bad_vocab), encoding="utf-8")
    with pytest.raises(ValueError, match="Vocabulary is not strictly sorted"):
        load_sparse_state(p)

    # 5. Lệch chiều dài giữa vocabulary và idf
    bad_len = json.loads(base_text)
    bad_len["idf"].append(1.0)
    p = tmp_path / "bad_len.json"
    p.write_text(json.dumps(bad_len), encoding="utf-8")
    with pytest.raises(ValueError, match="Length mismatch"):
        load_sparse_state(p)

    # 6. IDF chứa giá trị không hữu hạn
    bad_idf = json.loads(base_text)
    bad_idf["idf"][0] = float("inf")
    p = tmp_path / "bad_idf.json"
    p.write_text(json.dumps(bad_idf), encoding="utf-8")
    with pytest.raises(ValueError, match="Non-finite IDF"):
        load_sparse_state(p)
