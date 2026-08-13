"""Health endpoint: application aliveness vs component readiness."""
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request):
    """Return cached readiness from app.state; never pings external services."""
    state = request.app.state
    components = {
        "app": "alive",
        "qdrant": "ready" if state.retrieval_ready else "not_ready",
        "retrieval": "ready" if state.retrieval_ready else "not_ready",
        "generator": (
            "configured" if state.generator_configured else "not_configured"
        ),
    }
    status = (
        "ok"
        if state.retrieval_ready and state.generator_configured
        else "degraded"
    )
    return {"status": status, "components": components}
