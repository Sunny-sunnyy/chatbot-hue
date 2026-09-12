"""Trạng thái và vector biểu diễn thưa (sparse representation) cho Phase 3.

Đảm bảo tính xác định, tương đương chính xác với BM25 cho dot-product retrieval,
và tuần tự hóa không chứa document vectors hay metadata dư thừa.
"""

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import uuid

from backend.core.schema import FullCorpusChunk
from backend.scoring.bm25 import B, K1, tokenize

SCHEMA_VERSION: str = "phase_3_sparse_state:v1"
TOKENIZER_ID: str = "backend.scoring.bm25.tokenize:v1"


@dataclass(frozen=True)
class SparseVector:
    """Vector thưa gồm các chỉ số từ vựng (indices) và giá trị trọng số (values) đã căn chỉnh."""

    indices: tuple[int, ...]
    values: tuple[float, ...]


@dataclass(frozen=True)
class SparseState:
    """Trạng thái từ vựng và IDF bất biến của toàn bộ kho ngữ liệu cho biểu diễn thưa."""

    schema_version: str
    corpus_identity: str
    document_count: int
    average_document_length: float
    k1: float
    b: float
    tokenizer: str
    vocabulary: tuple[str, ...]
    idf: tuple[float, ...]


def compute_corpus_identity(chunks: Sequence[FullCorpusChunk]) -> str:
    """Tính mã băm SHA-256 định danh toàn vẹn của tập chunks theo thứ tự chuẩn."""
    seen_ids: set[str] = set()
    items: list[dict[str, str]] = []
    for chunk in chunks:
        if chunk.chunk_id in seen_ids:
            raise ValueError(f"Duplicate chunk_id found in corpus: {chunk.chunk_id}")
        seen_ids.add(chunk.chunk_id)
        items.append({"chunk_id": chunk.chunk_id, "search_text": chunk.search_text})

    canonical_json = json.dumps(items, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def fit_sparse_state(chunks: Sequence[FullCorpusChunk]) -> SparseState:
    """Khởi tạo trạng thái thưa từ tập các Representation A chunks của toàn corpus."""
    corpus_id = compute_corpus_identity(chunks)

    lengths: list[int] = []
    doc_freq: dict[str, int] = {}

    for chunk in chunks:
        tokens = tokenize(chunk.search_text)
        if not tokens:
            continue
        lengths.append(len(tokens))
        for term in set(tokens):
            doc_freq[term] = doc_freq.get(term, 0) + 1

    if not lengths:
        raise ValueError("Cannot fit sparse state with no non-empty documents")

    num_docs = len(lengths)
    avgdl = sum(lengths) / num_docs

    # Sắp xếp từ vựng theo thứ tự từ điển (lexicographic order)
    sorted_vocab = tuple(sorted(doc_freq.keys()))
    idf_list: list[float] = []
    for term in sorted_vocab:
        df = doc_freq[term]
        idf_val = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)
        idf_list.append(idf_val)

    return SparseState(
        schema_version=SCHEMA_VERSION,
        corpus_identity=corpus_id,
        document_count=num_docs,
        average_document_length=avgdl,
        k1=K1,
        b=B,
        tokenizer=TOKENIZER_ID,
        vocabulary=sorted_vocab,
        idf=tuple(idf_list),
    )


def encode_sparse_document(text: str, state: SparseState) -> SparseVector:
    """Mã hóa văn bản thành vector thưa với trọng số BM25 TF-IDF."""
    tokens = tokenize(text)
    if not tokens:
        return SparseVector(indices=(), values=())

    tf_counts = Counter(tokens)
    doc_length = len(tokens)

    vocab_map = {term: idx for idx, term in enumerate(state.vocabulary)}
    matched: list[tuple[int, float]] = []

    for term, tf in tf_counts.items():
        idx = vocab_map.get(term)
        if idx is None:
            continue
        idf = state.idf[idx]
        denominator = tf + state.k1 * (
            1.0 - state.b + state.b * doc_length / state.average_document_length
        )
        val = idf * (tf * (state.k1 + 1.0)) / denominator
        matched.append((idx, float(val)))

    if not matched:
        return SparseVector(indices=(), values=())

    # Căn chỉnh các chỉ số theo thứ tự tăng dần
    matched.sort(key=lambda x: x[0])
    indices = tuple(item[0] for item in matched)
    values = tuple(item[1] for item in matched)
    return SparseVector(indices=indices, values=values)


def encode_sparse_query(query: str, state: SparseState) -> SparseVector:
    """Mã hóa truy vấn thành vector thưa với trọng số cố định 1.0 cho mỗi từ khóa xuất hiện."""
    tokens = tokenize(query)
    if not tokens:
        return SparseVector(indices=(), values=())

    vocab_map = {term: idx for idx, term in enumerate(state.vocabulary)}
    matched_indices: list[int] = []
    seen_terms: set[str] = set()

    for term in tokens:
        if term in seen_terms:
            continue
        seen_terms.add(term)
        idx = vocab_map.get(term)
        if idx is not None:
            matched_indices.append(idx)

    if not matched_indices:
        return SparseVector(indices=(), values=())

    matched_indices.sort()
    return SparseVector(
        indices=tuple(matched_indices),
        values=tuple(1.0 for _ in matched_indices),
    )


def serialize_sparse_state(state: SparseState) -> bytes:
    """Tuần tự hóa SparseState thành chuỗi byte UTF-8 định dạng JSON chuẩn tắc."""
    data = {
        "average_document_length": state.average_document_length,
        "b": state.b,
        "corpus_identity": state.corpus_identity,
        "document_count": state.document_count,
        "idf": list(state.idf),
        "k1": state.k1,
        "schema_version": state.schema_version,
        "tokenizer": state.tokenizer,
        "vocabulary": list(state.vocabulary),
    }
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_sparse_state(state: SparseState, path: Path) -> str:
    """Ghi SparseState an toàn qua tệp tạm kề cận và trả về mã băm SHA-256."""
    data = serialize_sparse_state(state)
    sha256 = hashlib.sha256(data).hexdigest()

    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f"{path.name}.tmp.{uuid.uuid4().hex}")
    temp_path.write_bytes(data)
    temp_path.replace(path)

    return sha256


def load_sparse_state(path: Path) -> SparseState:
    """Đọc và kiểm tra tính hợp lệ nghiêm ngặt của SparseState từ tệp JSON."""
    if not path.is_file():
        raise FileNotFoundError(f"Sparse state file not found: {path}")

    raw_bytes = path.read_bytes()
    try:
        data = json.loads(raw_bytes.decode("utf-8"))
    except Exception as e:
        raise ValueError(f"Failed to parse sparse state JSON from {path}: {e}") from e

    schema_version = data.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        raise ValueError(f"Unknown schema version: {schema_version!r}, expected {SCHEMA_VERSION!r}")

    k1 = data.get("k1")
    b = data.get("b")
    if k1 != K1 or b != B:
        raise ValueError(f"Invalid BM25 constants: k1={k1}, b={b}; expected {K1}, {B}")

    tokenizer = data.get("tokenizer")
    if tokenizer != TOKENIZER_ID:
        raise ValueError(f"Invalid tokenizer: {tokenizer!r}, expected {TOKENIZER_ID!r}")

    corpus_identity = data.get("corpus_identity", "")
    if not isinstance(corpus_identity, str) or len(corpus_identity) != 64:
        raise ValueError(f"Malformed corpus_identity: {corpus_identity!r}")

    doc_count = data.get("document_count")
    if not isinstance(doc_count, int) or doc_count <= 0:
        raise ValueError(f"Invalid document_count: {doc_count}")

    avgdl = data.get("average_document_length")
    if not isinstance(avgdl, (int, float)) or avgdl <= 0:
        raise ValueError(f"Invalid average_document_length: {avgdl}")

    raw_vocab = data.get("vocabulary")
    raw_idf = data.get("idf")
    if not isinstance(raw_vocab, list) or not isinstance(raw_idf, list):
        raise ValueError("Vocabulary and IDF must be lists")

    if len(raw_vocab) != len(raw_idf):
        raise ValueError(f"Length mismatch: {len(raw_vocab)} terms != {len(raw_idf)} IDF values")

    # Kiểm tra từ vựng có được sắp xếp từ điển chặt chẽ không
    sorted_vocab = sorted(set(raw_vocab))
    if sorted_vocab != raw_vocab:
        raise ValueError("Vocabulary is not strictly sorted in lexicographical order or has duplicates")

    idf_tuple: list[float] = []
    for val in raw_idf:
        if not isinstance(val, (int, float)) or not math.isfinite(val):
            raise ValueError(f"Non-finite IDF value encountered: {val}")
        idf_tuple.append(float(val))

    return SparseState(
        schema_version=schema_version,
        corpus_identity=corpus_identity,
        document_count=doc_count,
        average_document_length=float(avgdl),
        k1=float(k1),
        b=float(b),
        tokenizer=tokenizer,
        vocabulary=tuple(raw_vocab),
        idf=tuple(idf_tuple),
    )
