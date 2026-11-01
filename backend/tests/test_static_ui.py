from pathlib import Path

from fastapi.testclient import TestClient

from api.app import create_app
from core.settings_loader import load_settings

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_static_files_use_local_marked_and_dompurify():
    html = (REPO_ROOT / "frontend/index.html").read_text(encoding="utf-8")
    js = (REPO_ROOT / "frontend/app.js").read_text(encoding="utf-8")
    assert "/static/vendor/marked.umd.js" in html
    assert "/static/vendor/purify.min.js" in html
    assert "cdn.jsdelivr.net" not in html
    assert "DOMPurify.sanitize(marked.parse(" in js
    assert '"img"' in js and '"style"' in js  # DOMPurify bỏ ảnh + CSS nội dòng (không tự tải từ máy khác)
    assert "innerHTML = answer" not in js


def test_root_and_assets_are_served_without_starting_lifespan():
    client = TestClient(create_app(load_settings()))
    root = client.get("/")
    assert root.status_code == 200
    # chữ Markdown do model viết không được làm trang tải gì từ máy khác (S3 streaming, rà bảo mật C106 R2)
    assert "default-src 'self'" in root.headers["content-security-policy"]
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/vendor/marked.umd.js").status_code == 200
    assert client.get("/static/vendor/purify.min.js").status_code == 200
