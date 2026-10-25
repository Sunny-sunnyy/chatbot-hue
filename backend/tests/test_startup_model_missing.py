"""Gói 1b (C-01 b): model tìm kiếm không nạp được lúc khởi động ⇒ 503 retrieval_unavailable, không phải 409 "cần lập chỉ mục lại".

Đầu vào thật, không mock: tiến trình con với HF_HUB_OFFLINE=1 và HF_HOME trỏ thư mục rỗng ⇒ không tìm thấy snapshot e5. Kiểm cả nguyên nhân
(lớp lỗi + thông điệp), vì 503 một mình cũng ra khi Qdrant tắt. Chạy riêng file này (User chạy bằng `!` — auto mode của session chặn lệnh
đặt HF_HOME rỗng); không gọi mạng / OpenAI, không ghi Qdrant.
"""
import json
import subprocess
import sys
from pathlib import Path

from core.settings_loader import load_settings
from ingestion.full_corpus_pipeline import candidate_by_id
from vectorstore.qdrant import client_from_settings

PROBE = """
import json
from fastapi.testclient import TestClient
import core.schema
from api.app import create_app
from core.settings_loader import load_settings
from retrieval.full_corpus import build_full_corpus_retrieval_service

settings = load_settings()
runtime = settings["full_corpus_runtime"]
out = {}
try:
    build_full_corpus_retrieval_service(candidate_id=runtime["candidate_id"], retrieval_treatment=runtime["retrieval_treatment"],
                                        reranker=runtime["reranker"], settings=settings).close()
    out["raised"] = None
except Exception as exc:
    out["raised"] = f"{type(exc).__module__}.{type(exc).__name__}"
    out["is_retrieval_dependency_error"] = type(exc) is core.schema.RetrievalDependencyError
    out["message"] = str(exc)
    out["has_cause"] = exc.__cause__ is not None
with TestClient(create_app(settings)) as client:
    response = client.post("/api/chat", json={"query": "Giá vé Đại Nội?"})
out["status"] = response.status_code
out["code"] = response.json().get("error", {}).get("code")
print(json.dumps(out, ensure_ascii=False))
"""


def test_missing_dense_model_at_startup_returns_503_for_the_right_reason(tmp_path):
    settings = load_settings()
    collection = candidate_by_id(settings["full_corpus_runtime"]["candidate_id"]).collection_name
    client = client_from_settings(settings)
    try:
        assert client.collection_exists(collection), "Qdrant :6335 phải chạy và có collection runtime (điều kiện trước của test)"
    finally:
        client.close()

    res = subprocess.run(
        [sys.executable, "-c", PROBE],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": "", "HF_HUB_OFFLINE": "1", "HF_HOME": str(tmp_path)},
    )
    assert res.returncode == 0, res.stderr[-2000:]
    out = json.loads(res.stdout.strip().splitlines()[-1])
    assert out["is_retrieval_dependency_error"], out
    assert "Dense model readiness failed" in out["message"], out
    assert out["has_cause"], out
    assert (out["status"], out["code"]) == (503, "retrieval_unavailable"), out
