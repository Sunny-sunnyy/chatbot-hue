"""Session-scoped live fixtures for the live-only backend suite.

Every collection this suite creates or mutates carries the
TEST_COLLECTION_PREFIX marker; the active collection is never written to.
The session fixture ingests the curated foods corpus through the real
ingestion pipeline (real chunker, real E5, real sparse embedder, real
Qdrant) into one isolated test collection and deletes it at session end,
printing the cleanup outcome. A final sweep removes any leftover marked
test collections and reports each outcome.
"""

import copy

import pytest

from core.settings_loader import load_settings
from vectorstore.qdrant import get_client

TEST_COLLECTION_PREFIX = "hue_rag_live_test_"
TEST_COLLECTION = "hue_rag_live_test_e5_small_384"
ACTIVE_COLLECTION = "hue_foods_e5_small_384"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: test exercising real external dependencies "
        "(Qdrant, local E5/MiniLM, OpenAI API)",
    )


def assert_test_collection(name):
    """Fail fast when a collection name is not a marked isolated test target."""
    assert name.startswith(TEST_COLLECTION_PREFIX), (
        f"refusing to touch collection {name!r}: missing test marker "
        f"{TEST_COLLECTION_PREFIX!r}"
    )
    assert name != ACTIVE_COLLECTION, "refusing to touch the active collection"


def make_test_settings(collection_name=TEST_COLLECTION, **overrides):
    """Return a deep copy of the real settings targeting a test collection."""
    assert_test_collection(collection_name)
    settings = copy.deepcopy(load_settings())
    settings["vector_database"]["collection_name"] = collection_name
    for key, value in overrides.items():
        if "." in key:
            section, field = key.split(".", 1)
            settings[section][field] = value
        else:
            settings[key] = value
    return settings


def cleanup_collection(client, name):
    """Delete one marked test collection and report the verified outcome."""
    assert_test_collection(name)
    try:
        client.delete_collection(name)
    except Exception as exc:  # a failed delete must be reported, not hidden
        print(f"LIVE CLEANUP {name}: FAILED {type(exc).__name__}")
        return False
    remaining = client.collection_exists(name)
    outcome = "FAILED - still exists" if remaining else "ok"
    print(f"LIVE CLEANUP {name}: {outcome}")
    return not remaining


def sweep_test_collections(client):
    """Delete every leftover marked test collection; report each outcome."""
    try:
        names = [c.name for c in client.get_collections().collections]
    except Exception as exc:  # Qdrant down: report, do not hide
        print(f"LIVE CLEANUP sweep: FAILED {type(exc).__name__}")
        return []
    leftovers = [n for n in names if n.startswith(TEST_COLLECTION_PREFIX)]
    for name in leftovers:
        cleanup_collection(client, name)
    return leftovers


@pytest.fixture(scope="session")
def live_settings():
    """Real settings loaded from disk (deep copy, safe to override)."""
    return copy.deepcopy(load_settings())


@pytest.fixture(scope="session")
def real_client():
    """The real cached Qdrant client for the configured server."""
    db = load_settings()["vector_database"]
    return get_client(db["url"], db["timeout"])


@pytest.fixture(scope="session")
def real_chunks():
    """All 572 curated foods chunks through the real markdown chunker."""
    from ingestion.chunking.markdown_chunker import chunk_foods_markdown

    chunks = chunk_foods_markdown()
    assert len(chunks) == 572
    return chunks


@pytest.fixture(scope="session")
def real_embedder():
    """The real local E5 embedder loaded once per session."""
    from embedding.embedder import E5Embedder

    embedding = load_settings()["embedding"]
    return E5Embedder(
        model_id=embedding["model"],
        dimension=embedding["vector_size"],
        device=embedding["device"],
        batch_size=embedding["batch_size"],
    )


@pytest.fixture(scope="session")
def ingested_collection(real_client, real_embedder):
    """Ingest the real curated corpus through the real pipeline.

    chunk_foods_markdown, the E5 embedder, the sparse embedder and Qdrant
    are all real; the summary is yielded to tests and the marked test
    collection is deleted at session end with a reported outcome.
    """
    from ingestion.chunking.markdown_chunker import chunk_foods_markdown
    from ingestion.pipeline import run_ingestion

    summary = run_ingestion(
        make_test_settings(TEST_COLLECTION),
        chunker=chunk_foods_markdown,
        embedder=real_embedder,
        client=real_client,
    )
    yield summary
    cleanup_collection(real_client, TEST_COLLECTION)


@pytest.fixture(scope="session")
def ingested_point_structs(ingested_collection, real_client):
    """Real PointStructs (with real dense/sparse vectors) scrolled back."""
    records, _ = real_client.scroll(
        TEST_COLLECTION, limit=1000, with_payload=True, with_vectors=True
    )
    assert len(records) == 572
    return records


@pytest.fixture(scope="session")
def real_retrieved_docs(ingested_collection, real_client, real_embedder):
    """Top real dense retrieval results for one query from the test collection."""
    from retrieval.dense_retriever import DenseRetriever

    retriever = DenseRetriever(
        client=real_client,
        embedder=real_embedder,
        collection_name=TEST_COLLECTION,
        top_k=10,
    )
    documents = retriever.search("bún bò Huế")
    assert documents, "real retrieval returned no documents"
    return documents


@pytest.fixture(scope="session", autouse=True)
def _live_cleanup_sweep(real_client):
    """Guarantee no marked test collection survives a test session."""
    yield
    sweep_test_collections(real_client)


@pytest.fixture()
def require_openai_key():
    """Fail loudly when OPENAI_API_KEY is missing from the environment."""
    import os

    if not os.environ.get("OPENAI_API_KEY", "").strip():
        pytest.fail(
            "OPENAI_API_KEY is not set in the environment; "
            "live generation tests are real failures when the key is missing"
        )
