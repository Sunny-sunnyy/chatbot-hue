"""4 chốt trước deploy (checklist E-dep: giới hạn lượt, cookie `Secure`, tắt /docs, xoay log) — 0 USD, không lifespan (không nạp model / Qdrant).

Hợp đồng giữ: **không đặt biến môi trường ⇒ hành vi như trước**; đặt ⇒ chốt chạy đúng. Lượt bị cho qua đi tiếp tới route (ở đây trả 503 vì không lifespan)."""
import datetime as dt

from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from api.app import create_app
from api.gioi_han import LOI_BAO, LOI_BAO_TAI_FILE, LOI_BAO_TONG, TRAN_TAI_FILE, TRONG_SO_DUONG, GioiHanLuot
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


# ---------- 27/11: trọng số lượt gọi model (chống cost-amplification cho /api/so_tay, /api/ho_so) ----------
def test_weighted_rate_limit_unit_ip_and_total_caps():
    assert TRONG_SO_DUONG == {
        "/api/chat": 1,
        "/api/chat/stream": 1,
        "/api/anh/ung_vien": 1,
        "/api/so_tay": 10,
        "/api/ho_so": 8,
    }
    hom_nay = dt.date(2026, 11, 27)
    # Trần IP = 12: 1 lần so_tay (10) -> còn 2 điểm -> ho_so (8) bị chặn ngay và KHÔNG cộng điểm, chat (1) vẫn qua 2 lần rồi mới chặn
    g = GioiHanLuot(tran=12)
    assert g.chan("ip1", hom_nay, trong_so=10) is None
    assert g.chan("ip1", hom_nay, trong_so=8) == LOI_BAO
    assert g.cho_qua("ip1", hom_nay) is True
    assert g.cho_qua("ip1", hom_nay) is True
    assert g.cho_qua("ip1", hom_nay) is False
    # Trần tổng = 15: ip1 dùng ho_so (8), ip2 dùng ho_so (8) bị chặn bởi trần tổng (8+8=16>15), không cộng vào ip2 lẫn tổng
    g_tong = GioiHanLuot(tran=50, tran_tong=15)
    assert g_tong.chan("ip1", hom_nay, trong_so=8) is None
    assert g_tong.chan("ip2", hom_nay, trong_so=8) == LOI_BAO_TONG
    assert g_tong.chan("ip2", hom_nay, trong_so=7) is None  # vẫn còn đúng 7 điểm (8 + 7 == 15)
    assert g_tong.chan("ip3", hom_nay, trong_so=1) == LOI_BAO_TONG


def test_weighted_rate_limit_middleware_rejects_heavy_routes_with_429(monkeypatch):
    monkeypatch.setenv("HUE_LUOT_MOI_NGAY", "11")
    monkeypatch.setenv("HUE_LUOT_TONG_MOI_NGAY", "12")
    c = TestClient(create_app())
    # 1 lần /api/ho_so (8 điểm) -> còn 3 điểm ở IP và 4 điểm ở tổng
    assert c.post("/api/ho_so", json={"ma": "di_tich"}).status_code != 429
    # Gọi tiếp /api/so_tay (10 điểm) khi chỉ còn 3 < 10 -> 429 ngay, không cộng điểm
    r = c.post("/api/so_tay")
    assert r.status_code == 429 and r.json() == {"error": {"code": "rate_limited", "message": LOI_BAO}}
    # Vẫn còn đúng 3 lượt /api/chat (8 + 3 = 11), lượt thứ 4 bị chặn 429
    assert [c.post("/api/chat", json=CAU).status_code == 429 for _ in range(4)] == [False, False, False, True]
