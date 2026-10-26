"""Session-scoped live fixtures for the full-corpus backend suite.

Fixtures dùng runtime thật (build record, Qdrant chỉ đọc, e5 local); không có
fixture nào tạo hay ghi collection.
"""

import copy
from pathlib import Path
import sys

# Code import trần (`core.*`, `retrieval.*`…) tính từ backend/ (quy ước gói 1b); thêm backend/ để pytest gọi từ gốc repo cũng chạy.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest

from core.settings_loader import load_settings


@pytest.fixture(scope="session")
def live_settings():
    """Real settings loaded from disk (deep copy, safe to override)."""
    return copy.deepcopy(load_settings())


@pytest.fixture()
def require_openai_key():
    """Fail loudly when OPENAI_API_KEY is missing from the environment."""
    import os

    if not os.environ.get("OPENAI_API_KEY", "").strip():
        pytest.fail(
            "OPENAI_API_KEY is not set in the environment; "
            "live generation tests are real failures when the key is missing"
        )


PHASE6_CONTEXT_CHECK_QUESTION = "Huế"


@pytest.fixture(scope="session")
def full_corpus_service(live_settings):
    from retrieval.full_corpus import build_full_corpus_retrieval_service

    runtime = live_settings["full_corpus_runtime"]
    service = build_full_corpus_retrieval_service(
        candidate_id=runtime["candidate_id"],
        retrieval_treatment=runtime["retrieval_treatment"],
        reranker=runtime["reranker"],
        settings=live_settings,
    )
    yield service
    service.close()


@pytest.fixture(scope="session")
def full_corpus_documents(full_corpus_service):
    result = full_corpus_service.search(PHASE6_CONTEXT_CHECK_QUESTION)
    assert result.documents
    assert all(doc.id and doc.metadata.get("domain") for doc in result.documents)
    assert all(doc.metadata.get("evidence_parts") for doc in result.documents)
    return result.documents
