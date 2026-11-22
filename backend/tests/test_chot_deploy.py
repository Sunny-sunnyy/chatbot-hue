"""4 chốt trước deploy (checklist E-dep: giới hạn lượt, cookie `Secure`, tắt /docs, xoay log) — 0 USD, không lifespan (không nạp model / Qdrant).

Hợp đồng giữ: **không đặt biến môi trường ⇒ hành vi như trước**; đặt ⇒ chốt chạy đúng. Lượt bị cho qua đi tiếp tới route (ở đây trả 503 vì không lifespan)."""
import datetime as dt

from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from api.app import create_app
from api.gioi_han import LOI_BAO, LOI_BAO_TAI_FILE, LOI_BAO_TONG, TRAN_TAI_FILE, GioiHanLuot
from api.routes.chat import CONVERSATION_COOKIE, _set_cookie

CAU = {"query": "Xin chào"}


def test_counter_blocks_after_cap_and_resets_next_day():
    g, hom_nay = GioiHanLuot(2), dt.date(2026, 11, 9)
    assert [g.cho_qua("a", hom_nay) for _ in range(3)] == [True, True, False]
    assert g.cho_qua("b", hom_nay)  # IP khác đếm riêng
    assert g.cho_qua("a", hom_nay + dt.timedelta(days=1))


def test_defaults_keep_docs_and_no_limit(monkeypatch):
    for k in ("HUE_TAT_DOCS", "HUE_LUOT_MOI_NGAY", "HUE_LUOT_TONG_MOI_NGAY"):
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


# ---------- 22/11 (rà bảo mật trước deploy): trần tổng mỗi ngày + đếm lượt tải file ----------
def test_total_cap_blocks_every_address_and_downloads_are_counted_apart():
    g, hom_nay = GioiHanLuot(0, tran_tong=3), dt.date(2026, 11, 22)  # không giới hạn theo IP, chỉ trần tổng
    assert [g.chan(ip, hom_nay) for ip in ("a", "b", "c", "d")] == [None, None, None, LOI_BAO_TONG]
    assert g.chan("a", hom_nay, tai_file=True) is None                     # lượt tải file không tính vào trần tổng lượt hỏi
    assert g.chan("d", hom_nay + dt.timedelta(days=1)) is None             # sang ngày ⇒ đếm lại
    g = GioiHanLuot(2)
    assert [g.chan("a", hom_nay, tai_file=True) for _ in range(TRAN_TAI_FILE + 1)][-2:] == [None, LOI_BAO_TAI_FILE]
    assert g.chan("a", hom_nay) is None and g.chan("b", hom_nay, tai_file=True) is None  # hết lượt tải không ăn vào lượt hỏi; IP khác đếm riêng


def test_env_total_cap_alone_turns_the_limiter_on_and_download_route_is_counted(monkeypatch):
    monkeypatch.delenv("HUE_LUOT_MOI_NGAY", raising=False)
    monkeypatch.setenv("HUE_LUOT_TONG_MOI_NGAY", "2")
    c = TestClient(create_app())
    assert 429 not in [c.post("/api/chat", json=CAU).status_code, c.post("/api/chat/stream", json=CAU).status_code]
    r = c.post("/api/chat", json=CAU)
    assert r.status_code == 429 and r.json()["error"]["message"] == LOI_BAO_TONG
    assert [c.get("/api/lich/pptx").status_code == 429 for _ in range(TRAN_TAI_FILE + 1)] == [False] * TRAN_TAI_FILE + [True]
    assert c.get("/api/lich/pptx").json()["error"]["message"] == LOI_BAO_TAI_FILE
    assert c.post("/api/conversation/new").status_code != 429 and c.get("/health").status_code != 429  # đường khác không tính
