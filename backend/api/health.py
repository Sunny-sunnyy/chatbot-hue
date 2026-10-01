"""Health endpoint: application aliveness vs component readiness."""
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request):
    """Return cached readiness from app.state; never pings external services."""
    state = request.app.state
    retrieval_ready = bool(getattr(state, "retrieval_ready", False))
    tokenizer_ready = bool(getattr(state, "tokenizer_ready", False))
    generator_ready = bool(getattr(state, "generator_ready", False))

    components = {
        "app": "alive",
        "qdrant": "ready" if retrieval_ready else "not_ready",
        "retrieval": "ready" if retrieval_ready else "not_ready",
        "tokenizer": "ready" if tokenizer_ready else "not_ready",
        "generator": "ready" if generator_ready else "not_ready",
    }
    all_ready = retrieval_ready and tokenizer_ready and generator_ready
    status = "ok" if all_ready else "degraded"
    return {"status": status, "components": components}
