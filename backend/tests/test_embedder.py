"""Tests for dense embedders: local SentenceTransformer and OpenRouter adapter."""
import math

import numpy as np
import pytest

from embedding.base import BaseEmbedder, EmbeddingError
from embedding.batch_embed import embed_in_batches
from embedding.embedder import DOCUMENT_PREFIX, QUERY_PREFIX, SentenceTransformerEmbedder
from embedding.openrouter_embedder import OpenRouterEmbedder

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def _unit_vector(*dims):
    """Return a DIMENSION-length vector with the given leading values."""
    return list(dims) + [0.0] * (DIMENSION - len(dims))


class _FakeModel:
    """SentenceTransformer stand-in returning fixed raw vectors."""

    def __init__(self, vectors=(_unit_vector(3.0, 4.0),)):
        self.vectors = [list(v) for v in vectors]
        self.calls = []

    def encode(self, texts, **kwargs):
        self.calls.append(list(texts))
        count = len(texts)
        return np.asarray([self.vectors[i % len(self.vectors)] for i in range(count)])


class _FakeResponse:
    def __init__(self, status_code, payload=None, headers=None):
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}

    def json(self):
        return self._payload


class _FakeSession:
    """Records POST calls and serves scripted responses in order."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


def _fake_model_load(created, model):
    """Return a monkeypatchable loader that records creations."""
    def load(model_id, device):
        created.append(model_id)
        return model
    return load


@pytest.fixture(autouse=True)
def _clear_model_cache():
    """Isolate the process-level model cache between tests."""
    SentenceTransformerEmbedder  # noqa: B018 - keep import used by fixtures
    from embedding import embedder as module
    module._get_model.cache_clear()
    yield
    module._get_model.cache_clear()


@pytest.fixture()
def fake_model():
    return _FakeModel()


def test_embed_documents_empty_skips_model(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    assert embedder.embed_documents([]) == []
    assert fake_model.calls == []


def test_embed_documents_applies_document_prefix(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    embedder.embed_documents(["Bún bò Huế", "Cơm hến"])
    assert fake_model.calls == [
        ["passage: Bún bò Huế", "passage: Cơm hến"]
    ]


def test_embed_query_applies_query_prefix(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    embedder.embed_query("Quán bún bò ngon nhất?")
    assert fake_model.calls == [["query: Quán bún bò ngon nhất?"]]
    assert DOCUMENT_PREFIX == "passage: "
    assert QUERY_PREFIX == "query: "


def test_embed_documents_returns_one_vector_per_text_in_order(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    vectors = embedder.embed_documents(["a", "b", "c"])
    assert len(vectors) == 3
    # The mock repeats the same raw vector, so order is visible via call count.
    assert fake_model.calls == [["passage: a", "passage: b", "passage: c"]]
    assert all(len(v) == DIMENSION for v in vectors)


def test_vectors_are_l2_normalized(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    vector = embedder.embed_query("Bún bò Huế")
    assert vector == pytest.approx([0.6, 0.8, *([0.0] * (DIMENSION - 2))])


def test_dimension_mismatch_fails_fast(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, dimension=3)
    with pytest.raises(EmbeddingError, match="dimension"):
        embedder.embed_query("Bún bò Huế")


def test_non_finite_vectors_rejected(monkeypatch):
    model = _FakeModel(vectors=(_unit_vector(float("nan"), 1.0),))
    monkeypatch.setattr("embedding.embedder._load_model", _fake_model_load([], model))
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    with pytest.raises(EmbeddingError, match="finite"):
        embedder.embed_query("Bún bò Huế")


def test_zero_norm_vector_rejected(monkeypatch):
    model = _FakeModel(vectors=(_unit_vector(0.0, 0.0),))
    monkeypatch.setattr("embedding.embedder._load_model", _fake_model_load([], model))
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    with pytest.raises(EmbeddingError, match="zero"):
        embedder.embed_query("Bún bò Huế")


def test_custom_prefixes_used_when_configured(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(
        MODEL_ID, DIMENSION, document_prefix="doc: ", query_prefix="q: "
    )
    embedder.embed_documents(["a"])
    embedder.embed_query("b")
    assert fake_model.calls == [["doc: a"], ["q: b"]]


def test_empty_and_whitespace_query_rejected(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    with pytest.raises(EmbeddingError):
        embedder.embed_query("")
    with pytest.raises(EmbeddingError):
        embedder.embed_query("   ")
    assert fake_model.calls == []


def test_model_cached_once_per_process(monkeypatch):
    created = []
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load(created, _FakeModel())
    )
    first = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    second = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    first.embed_documents(["x"])
    second.embed_documents(["y"])
    assert len(created) == 1


def test_model_id_and_dimension_exposed(fake_model, monkeypatch):
    monkeypatch.setattr(
        "embedding.embedder._load_model", _fake_model_load([], fake_model)
    )
    embedder = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    assert embedder.model_id == MODEL_ID
    assert embedder.dimension == DIMENSION


class _RecordingEmbedder(BaseEmbedder):
    """Minimal embedder recording per-call inputs for batching tests."""

    def __init__(self):
        self.calls = []

    @property
    def model_id(self):
        return "recording"

    @property
    def dimension(self):
        return 2

    def embed_documents(self, texts):
        self.calls.append(list(texts))
        return [[float(len(texts))] * 2] * len(texts)

    def embed_query(self, query):
        return [0.0, 1.0]


def test_embed_in_batches_preserves_order_and_boundaries():
    recorder = _RecordingEmbedder()
    vectors = embed_in_batches(recorder, ["t0", "t1", "t2", "t3", "t4"], batch_size=2)
    assert len(vectors) == 5
    assert recorder.calls == [["t0", "t1"], ["t2", "t3"], ["t4"]]
    assert vectors == [[2.0, 2.0]] * 2 + [[2.0, 2.0]] * 2 + [[1.0, 1.0]]


def test_embed_in_batches_empty_input():
    recorder = _RecordingEmbedder()
    assert embed_in_batches(recorder, [], batch_size=2) == []
    assert recorder.calls == []


def test_embed_in_batches_rejects_invalid_batch_size():
    recorder = _RecordingEmbedder()
    with pytest.raises(ValueError):
        embed_in_batches(recorder, ["t0"], batch_size=0)


def _remote_embedder(session, **kwargs):
    """Build an OpenRouterEmbedder with an injected fake session."""
    return OpenRouterEmbedder(
        "qwen/qwen3-embedding-0.6b",
        DIMENSION,
        session=session,
        api_key="test-key",
        **kwargs,
    )


def _ok_payload(texts):
    return {"data": [{"index": i, "embedding": [3.0, 4.0, *([0.0] * (DIMENSION - 2))]}
                     for i in range(len(texts))]}


def test_remote_empty_batch_skips_network():
    session = _FakeSession([])
    embedder = _remote_embedder(session)
    assert embedder.embed_documents([]) == []
    assert session.calls == []


def test_remote_success_returns_normalized_vectors_in_order():
    payload = {"data": [
        {"index": 1, "embedding": [3.0, 4.0, *([0.0] * (DIMENSION - 2))]},
        {"index": 0, "embedding": [4.0, 3.0, *([0.0] * (DIMENSION - 2))]},
    ]}
    session = _FakeSession([_FakeResponse(200, payload)])
    embedder = _remote_embedder(session)
    vectors = embedder.embed_documents(["a", "b"])
    # Response is reordered by index, matching input order.
    assert vectors[0] == pytest.approx([0.8, 0.6, *([0.0] * (DIMENSION - 2))])
    assert vectors[1] == pytest.approx([0.6, 0.8, *([0.0] * (DIMENSION - 2))])


def test_remote_uses_document_and_query_input_types():
    session = _FakeSession([_FakeResponse(200, _ok_payload(["a"]))])
    embedder = _remote_embedder(session)
    embedder.embed_documents(["a"])
    body = session.calls[0][1]["json"]
    assert body["input_type"] == "search_document"

    session = _FakeSession([_FakeResponse(200, _ok_payload(["q"]))])
    embedder = _remote_embedder(session)
    embedder.embed_query("q")
    body = session.calls[0][1]["json"]
    assert body["input_type"] == "search_query"


def test_remote_retries_429_then_succeeds():
    delays = []
    session = _FakeSession([
        _FakeResponse(429),
        _FakeResponse(200, _ok_payload(["a"])),
    ])
    embedder = _remote_embedder(session, sleep=delays.append)
    vectors = embedder.embed_documents(["a"])
    assert len(vectors) == 1
    assert len(session.calls) == 2
    assert delays == [1.0]


def test_remote_fails_after_max_retries_on_5xx():
    delays = []
    session = _FakeSession([_FakeResponse(503)] * 3)
    embedder = _remote_embedder(session, sleep=delays.append)
    with pytest.raises(EmbeddingError, match="retries"):
        embedder.embed_documents(["a"])
    assert len(session.calls) == 3
    assert delays == [1.0, 2.0]


def test_remote_does_not_retry_client_errors():
    session = _FakeSession([_FakeResponse(400)])
    embedder = _remote_embedder(session)
    with pytest.raises(EmbeddingError, match="HTTP 400"):
        embedder.embed_documents(["a"])
    assert len(session.calls) == 1


def test_remote_never_falls_back_to_local_model():
    # A failed remote call must raise; there is no fallback path to another
    # model, which would mix incompatible vector spaces.
    session = _FakeSession([_FakeResponse(500)] * 3)
    embedder = _remote_embedder(session)
    with pytest.raises(EmbeddingError):
        embedder.embed_documents(["a"])


def test_remote_missing_api_key_fails_before_request(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    session = _FakeSession([])
    embedder = OpenRouterEmbedder(
        "qwen/qwen3-embedding-0.6b", DIMENSION, session=session
    )
    with pytest.raises(EmbeddingError, match="OPENROUTER_API_KEY"):
        embedder.embed_documents(["a"])
    assert session.calls == []


def test_remote_mismatched_embedding_count_rejected():
    session = _FakeSession([_FakeResponse(200, _ok_payload(["a"]))])
    embedder = _remote_embedder(session)
    with pytest.raises(EmbeddingError, match="mismatched"):
        embedder.embed_documents(["a", "b"])


def test_remote_batches_large_inputs():
    session = _FakeSession([
        _FakeResponse(200, _ok_payload(["a", "b"])),
        _FakeResponse(200, _ok_payload(["c"])),
    ])
    embedder = _remote_embedder(session, batch_size=2)
    vectors = embedder.embed_documents(["a", "b", "c"])
    assert len(vectors) == 3
    assert len(session.calls) == 2
    bodies = [call[1]["json"] for call in session.calls]
    assert bodies[0]["input"] == ["a", "b"]
    assert bodies[1]["input"] == ["c"]
    assert all(math.isfinite(x) for v in vectors for x in v)


def test_remote_rejects_invalid_batch_size():
    with pytest.raises(EmbeddingError, match="batch_size"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, batch_size=0)
    with pytest.raises(EmbeddingError, match="batch_size"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, batch_size=-3)


def test_remote_rejects_invalid_timeout_and_retries():
    with pytest.raises(EmbeddingError, match="timeout"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, timeout=0)
    with pytest.raises(EmbeddingError, match="max_retries"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, max_retries=-1)


def test_remote_rejects_duplicate_indexes():
    payload = {"data": [
        {"index": 0, "embedding": [3.0, 4.0, *([0.0] * (DIMENSION - 2))]},
        {"index": 0, "embedding": [4.0, 3.0, *([0.0] * (DIMENSION - 2))]},
    ]}
    session = _FakeSession([_FakeResponse(200, payload)])
    embedder = _remote_embedder(session)
    with pytest.raises(EmbeddingError, match="mismatched"):
        embedder.embed_documents(["a", "b"])


def test_remote_rejects_missing_or_out_of_range_indexes():
    # Missing index 0 for two inputs.
    session = _FakeSession([
        _FakeResponse(200, {"data": [
            {"index": 1, "embedding": [3.0, 4.0, *([0.0] * (DIMENSION - 2))]},
        ]})
    ])
    with pytest.raises(EmbeddingError, match="mismatched"):
        _remote_embedder(session).embed_documents(["a", "b"])
    # Out-of-range index 2 for two inputs.
    session = _FakeSession([
        _FakeResponse(200, {"data": [
            {"index": 0, "embedding": [3.0, 4.0, *([0.0] * (DIMENSION - 2))]},
            {"index": 2, "embedding": [4.0, 3.0, *([0.0] * (DIMENSION - 2))]},
        ]})
    ])
    with pytest.raises(EmbeddingError, match="mismatched"):
        _remote_embedder(session).embed_documents(["a", "b"])


def test_remote_uses_retry_after_delay():
    delays = []
    session = _FakeSession([
        _FakeResponse(429, headers={"Retry-After": "3"}),
        _FakeResponse(200, _ok_payload(["a"])),
    ])
    embedder = _remote_embedder(session, sleep=delays.append)
    embedder.embed_documents(["a"])
    assert delays == [3.0]


def test_remote_backoff_is_capped_exponential():
    delays = []
    session = _FakeSession([_FakeResponse(429)] * 3)
    embedder = _remote_embedder(session, sleep=delays.append)
    with pytest.raises(EmbeddingError):
        embedder.embed_documents(["a"])
    # 2**0 and 2**1; the final attempt does not sleep before failing.
    assert delays == [1.0, 2.0]
