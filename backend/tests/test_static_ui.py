import re
from pathlib import Path

from fastapi.testclient import TestClient

from api.app import FRONTEND_DIR, create_app
from core.settings_loader import load_settings

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD_HINT = "chưa có bản build giao diện — chạy `cd frontend && npm ci && npm run build`"


def built_index():
    index = FRONTEND_DIR / "index.html"
    assert index.is_file(), BUILD_HINT
    return index.read_text(encoding="utf-8")


def test_built_page_runs_under_csp_without_external_assets():
    # CSP `script-src 'self'` (không 'unsafe-inline' / 'unsafe-eval'): bản build chỉ được nạp script từ file của chính server,
    # không script nội dòng, không `eval`; không CDN (yêu cầu 14–15 của giao diện mới).
    html = built_index()
    assert "http://" not in html and "https://" not in html
    scripts = re.findall(r"<script\b([^>]*)>(.*?)</script>", html, re.S)
    assert scripts
    for attrs, body in scripts:
        assert body.strip() == ""
        assert re.search(r'src="/static/assets/[^"]+\.js"', attrs)
    assert "<style" not in html
    for bundle in (FRONTEND_DIR / "assets").glob("*.js"):
        code = bundle.read_text(encoding="utf-8")
        assert "eval(" not in code and "new Function" not in code, bundle.name


def test_answer_sanitizer_is_an_allowlist_without_fetching_tags():
    # DOMPurify theo danh sách cho phép: không thẻ / thuộc tính nào tự tải từ máy khác (review C107 M-1)
    js = (REPO_ROOT / "frontend/src/markdown.js").read_text(encoding="utf-8")
    assert "DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS)" in js
    options = js[js.index("export const SANITIZE_OPTIONS"):]
    options = options[: options.index("};")]
    assert "ALLOWED_TAGS" in options and "ALLOWED_ATTR" in options
    for fetching in ('"img"', '"input"', '"form"', '"style"', '"background"', '"src"', '"svg"', '"srcset"'):
        assert fetching not in options


def test_root_and_assets_are_served_without_starting_lifespan():
    html = built_index()
    client = TestClient(create_app(load_settings()))
    root = client.get("/")
    assert root.status_code == 200
    # chữ Markdown do model viết không được làm trang tải gì từ máy khác (S3 streaming, rà bảo mật C106 R2)
    assert "default-src 'self'" in root.headers["content-security-policy"]
    # cùng trang HTML qua đường /static cũng có CSP (review C107 M-1); tài nguyên khác không cần
    static_page = client.get("/static/index.html")
    assert static_page.status_code == 200
    assert static_page.headers["content-security-policy"] == root.headers["content-security-policy"]
    for asset in re.findall(r'(?:src|href)="(/static/assets/[^"]+)"', html):
        response = client.get(asset)
        assert response.status_code == 200, asset
        assert "content-security-policy" not in response.headers


def test_portal_images_are_in_repo_and_private_image_is_gitignored():
    # Bản clone (không có ảnh riêng) phải build ra đủ ảnh: mọi ảnh `anh.js` trỏ tới ngoài `rieng/` có trong `public/anh/`;
    # ảnh lễ hội không giấy phép mở (`rieng/`) không được vào repo công khai (User 07/11).
    import subprocess

    js = (REPO_ROOT / "frontend/src/anh.js").read_text(encoding="utf-8")
    files = re.findall(r'anh\("([^"]+\.jpg)"', js)
    assert len(files) == 8  # 2 đầu trang + 5 lĩnh vực + ảnh lễ hội riêng
    for name in files:
        if not name.startswith("rieng/"):
            assert (REPO_ROOT / "frontend/public/anh" / name).is_file(), name
    ignored = subprocess.run(["git", "check-ignore", "-q", "frontend/public/anh/rieng/lv_festivals.jpg"], cwd=REPO_ROOT)
    assert ignored.returncode == 0
