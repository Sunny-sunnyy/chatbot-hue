"""4 chốt trước deploy (checklist E-dep: giới hạn lượt, cookie `Secure`, tắt /docs, xoay log) — 0 USD, không lifespan (không nạp model / Qdrant).

Hợp đồng giữ: **không đặt biến môi trường ⇒ hành vi như trước**; đặt ⇒ chốt chạy đúng. Lượt bị cho qua đi tiếp tới route (ở đây trả 503 vì không lifespan)."""
import datetime as dt

from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from api.app import create_app
from api.gioi_han import LOI_BAO, GioiHanLuot
from api.routes.chat import CONVERSATION_COOKIE, _set_cookie

CAU = {"query": "Xin chào"}


def test_counter_blocks_after_cap_and_resets_next_day():
    g, hom_nay = GioiHanLuot(2), dt.date(2026, 11, 9)
    assert [g.cho_qua("a", hom_nay) for _ in range(3)] == [True, True, False]
    assert g.cho_qua("b", hom_nay)  # IP khác đếm riêng
    assert g.cho_qua("a", hom_nay + dt.timedelta(days=1))


def test_defaults_keep_docs_and_no_limit(monkeypatch):
    for k in ("HUE_TAT_DOCS", "HUE_LUOT_MOI_NGAY"):
        monkeypatch.delenv(k, raising=False)
    c = TestClient(create_app())
    assert c.get("/docs").status_code == 200 and c.get("/openapi.json").status_code == 200
    assert all(c.post("/api/chat", json=CAU).status_code != 429 for _ in range(5))


def test_env_turns_off_docs(monkeypatch):
    monkeypatch.setenv("HUE_TAT_DOCS", "1")
    c = TestClient(create_app())
    assert [c.get(p).status_code for p in ("/docs", "/redoc", "/openapi.json")] == [404, 404, 404]


def test_env_limit_returns_429_with_message_on_model_routes_only(monkeypatch):
    monkeypatch.setenv("HUE_LUOT_MOI_NGAY", "2")
    c = TestClient(create_app())
    codes = [c.post("/api/chat", json=CAU).status_code, c.post("/api/chat/stream", json=CAU).status_code]
    assert 429 not in codes
    r = c.post("/api/chat", json=CAU)
    assert r.status_code == 429 and r.json() == {"error": {"code": "rate_limited", "message": LOI_BAO}}
    assert c.post("/api/anh/ung_vien", content=b"x").status_code == 429  # ảnh cũng gọi model ⇒ chung sổ
    assert c.get("/health").status_code != 429 and c.post("/api/feedback", json={}).status_code != 429  # đường khác không tính


def test_cookie_secure_only_when_env_set(monkeypatch):
    monkeypatch.delenv("HUE_COOKIE_SECURE", raising=False)
    r = JSONResponse({})
    _set_cookie(r, "abc")
    assert CONVERSATION_COOKIE in r.headers["set-cookie"] and "secure" not in r.headers["set-cookie"].lower()
    monkeypatch.setenv("HUE_COOKIE_SECURE", "1")
    r = JSONResponse({})
    _set_cookie(r, "abc")
    assert "secure" in r.headers["set-cookie"].lower()

