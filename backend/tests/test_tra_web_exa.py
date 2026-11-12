"""Exa trong bước tra web (plan `docs/superpowers/plans/2026-11-12-tra-web-exa-plan.md`). 0 USD, **không gọi mạng**: Exa / Serper là phản hồi ghi sẵn qua
`httpx.MockTransport` (khuôn phản hồi Exa lấy từ lượt thử thật 12/11: `results[].title / url / highlights`, `costDollars.total`). Đây không phải bằng chứng
Exa thật trả đúng — phần đó là thí nghiệm có phí. Câu / đoạn trích tự viết."""
import asyncio
import json
import time
from pathlib import Path

import httpx
import pytest

from api.app import _tim_web_server
from llm import tra_web as tw

CAU = "Ở Huế có phòng tập gym nào mở sớm không?"
EXA_OK = {"results": [
    {"title": "Phòng tập A", "url": "https://a.example.vn/gym?utm_source=x&id=2", "highlights": ["Mở cửa từ 5h sáng.", "Có lớp buổi tối."]},
    {"title": "Không có đoạn trích", "url": "https://b.example.vn/x", "highlights": []},
    {"title": "Link lạ", "url": "ftp://c.example.vn/x", "highlights": ["bỏ"]},
    {"title": "Đoạn dài", "url": "https://d.example.vn/y", "highlights": ["x" * 900]}],
    "costDollars": {"total": 0.007}}
SERPER_OK = {"organic": [{"title": "Từ Serper", "link": "https://s.example.vn/1", "snippet": "Đoạn trích ngắn."}]}


def transport(exa=(200, EXA_OK), serper=(200, SERPER_OK), calls=None, exa_exc=None):
    def handler(request):
        if calls is not None:
            calls.append(request)
        if request.url.host == "api.exa.ai":
            if exa_exc is not None:
                raise exa_exc
            return httpx.Response(exa[0], json=exa[1])
        return httpx.Response(serper[0], json=serper[1])
    return httpx.MockTransport(handler)


def run(coro):
    return asyncio.run(coro)


def test_exa_book_has_same_shape_as_serper_and_code_builds_the_request():
    calls = []
    kq = run(tw.tim_web_exa(CAU, api_key="k", timeout=5, transport=transport(calls=calls)))
    assert (kq.trang_thai, kq.nguon, kq.usd) == ("ok", "exa", 0.007)
    assert [s["id"] for s in kq.so_web] == [1, 2]  # mục không đoạn trích + link lạ bị bỏ, đánh số lại
    assert kq.so_web[0] == {"id": 1, "title": "Phòng tập A", "snippet": "Mở cửa từ 5h sáng. Có lớp buổi tối.", "link": "https://a.example.vn/gym?id=2",
                            "domain": "a.example.vn"}
    assert len(kq.so_web[1]["snippet"]) == tw.MAX_SNIPPET_CHARS  # cắt bằng trần đoạn trích của hệ thống
    body = json.loads(calls[0].content)
    assert calls[0].headers["x-api-key"] == "k" and str(calls[0].url) == tw.EXA_URL
    assert body == {"query": CAU, "type": "auto", "numResults": 5, "userLocation": "VN", "contents": {"highlights": {"maxCharacters": 400}}}


def test_exa_missing_key_opens_no_connection():
    calls = []
    kq = run(tw.tim_web_exa(CAU, api_key=None, timeout=5, transport=transport(calls=calls)))
    assert (kq.trang_thai, kq.loi, calls) == ("loi", "thieu_khoa", [])


@pytest.mark.parametrize("kw, trang_thai, loi", [
    ({"exa": (402, {"error": "x"})}, "loi", "http_402"),            # hết tín dụng
    ({"exa": (429, {"error": "x"})}, "loi", "http_429"),            # quá tốc độ
    ({"exa": (200, {"khac": 1})}, "loi", "schema"),
    ({"exa": (200, {"results": []})}, "rong", None),               # 0 kết quả ≠ lỗi
    ({"exa_exc": httpx.ReadTimeout("t")}, "loi", "het_gio"),
    ({"exa_exc": httpx.ConnectError("c")}, "loi", "mang")])
def test_exa_failures_are_not_empty_results(kw, trang_thai, loi):
    kq = run(tw.tim_web_exa(CAU, api_key="k", timeout=5, transport=transport(**kw)))
    assert (kq.trang_thai, kq.loi, kq.so_web) == (trang_thai, loi, [])


def test_exa_ok_never_calls_serper():
    calls = []
    kq = run(tw.tim_web_exa_truoc(CAU, exa_key="k", serper_key="s", timeout=5, exa_timeout=3, transport=transport(calls=calls)))
    assert kq.nguon == "exa" and [c.url.host for c in calls] == ["api.exa.ai"]


@pytest.mark.parametrize("kw", [{"exa": (402, {})}, {"exa": (200, {"results": []})}, {"exa_exc": httpx.ConnectError("c")}])
def test_exa_failure_or_empty_falls_back_to_serper_exactly_once(kw):
    calls = []
    kq = run(tw.tim_web_exa_truoc(CAU, exa_key="k", serper_key="s", timeout=5, exa_timeout=3, transport=transport(calls=calls, **kw)))
    assert (kq.trang_thai, kq.nguon, kq.so_web[0]["title"]) == ("ok", "exa>serper", "Từ Serper")
    assert [c.url.host for c in calls] == ["api.exa.ai", "google.serper.dev"]
    assert kq.usd == tw.SERPER_USD_PER_CALL  # lượt Exa hỏng không tính tiền


def test_exa_timeout_at_its_own_limit_still_leaves_time_for_serper():  # review C M-1: hạn riêng của Exa < hạn chung
    def cham(request):
        if request.url.host == "api.exa.ai":
            time.sleep(0.25)  # Exa "treo" tới hết hạn riêng rồi hết giờ
            raise httpx.ReadTimeout("t")
        return httpx.Response(200, json=SERPER_OK)
    kq = run(tw.tim_web_exa_truoc(CAU, exa_key="k", serper_key="s", timeout=1.0, exa_timeout=0.25, transport=httpx.MockTransport(cham)))
    assert (kq.trang_thai, kq.nguon) == ("ok", "exa>serper") and kq.ms >= 250


def test_exa_configured_but_key_missing_goes_to_serper_without_calling_exa():  # review C minor
    calls = []
    kq = run(tw.tim_web_exa_truoc(CAU, exa_key=None, serper_key="s", timeout=5, exa_timeout=3, transport=transport(calls=calls)))
    assert (kq.trang_thai, kq.nguon) == ("ok", "exa>serper") and [c.url.host for c in calls] == ["google.serper.dev"]


def test_excluded_domains_are_sent_only_when_configured():
    calls = []
    run(tw.tim_web_exa(CAU, api_key="k", timeout=5, loai_ten_mien=("exa.ai",), transport=transport(calls=calls)))
    assert json.loads(calls[0].content)["excludeDomains"] == ["exa.ai"]


def test_both_fail_reports_error_not_fake_results():
    kq = run(tw.tim_web_exa_truoc(CAU, exa_key="k", serper_key="s", timeout=5, exa_timeout=3, transport=transport(exa=(500, {}), serper=(500, {}))))
    assert (kq.trang_thai, kq.loi, kq.nguon, kq.so_web) == ("loi", "http_500", "exa>serper", [])


def test_no_time_left_means_no_fallback_call():
    calls = []
    kq = run(tw.tim_web_exa_truoc(CAU, exa_key="k", serper_key="s", timeout=0.2, exa_timeout=0.2, transport=transport(calls=calls, exa=(500, {}))))
    assert kq.nguon == "exa" and kq.trang_thai == "loi" and len(calls) == 1  # hạn chung còn < 0,5 s ⇒ không gọi Serper


def server_search(monkeypatch, config: dict, seen: list):
    """Hàm tra của server với hai hàm tra thật thay bằng bộ ghi tên — chỉ kiểm việc CHỌN nguồn + trần / ngày (phần gọi mạng đã kiểm ở trên)."""
    async def exa_truoc(cau, **kw):
        seen.append("exa")
        return tw.KetQuaWeb("ok", nguon="exa")

    async def serper(cau, **kw):
        seen.append("serper")
        return tw.KetQuaWeb("ok")
    monkeypatch.setattr("api.app.tim_web_exa_truoc", exa_truoc)
    monkeypatch.setattr("api.app.tim_web", serper)
    return _tim_web_server({"assistant": config})


def test_default_source_is_serper_as_before(monkeypatch):
    seen = []
    run(server_search(monkeypatch, {"tra_web": True}, seen)(CAU))
    assert seen == ["serper"]


def test_exa_source_respects_daily_cap_then_goes_to_serper(monkeypatch):
    seen = []
    tim = server_search(monkeypatch, {"tra_web_nguon": "exa", "tra_web_exa_moi_ngay": 2}, seen)
    for _ in range(4):
        run(tim(CAU))
    assert seen == ["exa", "exa", "serper", "serper"]


def test_unknown_source_fails_at_startup():
    with pytest.raises(ValueError):
        _tim_web_server({"assistant": {"tra_web_nguon": "google"}})


def test_only_the_web_module_knows_the_exa_address():  # ranh giới (review B m-1): mọi lời gọi Exa đi qua `llm/tra_web.py`
    backend = Path(__file__).resolve().parents[1]
    co = sorted(str(p.relative_to(backend)) for p in backend.rglob("*.py")
                if ".venv" not in p.parts and "tests" not in p.parts and "api.exa.ai" in p.read_text(encoding="utf-8"))
    assert co == ["llm/tra_web.py"]


def test_exa_total_time_is_capped_even_if_each_phase_is_fast():  # review B m-4: hạn tổng, không chỉ hạn từng pha của httpx
    async def cham(request):
        await asyncio.sleep(0.4)
        return httpx.Response(200, json=EXA_OK)
    kq = run(tw.tim_web_exa(CAU, api_key="k", timeout=0.15, transport=httpx.MockTransport(cham)))
    assert (kq.trang_thai, kq.loi) == ("loi", "het_gio") and kq.ms < 350
