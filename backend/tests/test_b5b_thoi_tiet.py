"""Phase 9 B5b — thời tiết Huế (plan `docs/superpowers/plans/2026-11-05-phase-9-b5b-plan.md` bản 2 `cc09fda9f634`, §3 danh sách test). 0 USD,
**không gọi mạng**: Open-Meteo là phản hồi ghi sẵn qua `httpx.MockTransport` (khuôn theo tài liệu — schema thật kiểm ở probe bước 3); model là
`OpenAIResponsesModel` thật của SDK với client kịch bản của test B2. Phần nối đọc Qdrant thật (chỉ đọc). Câu tự viết, số trong phản hồi tự đặt.
"""
import asyncio
import dataclasses
import functools
import json
from datetime import date, timedelta
from pathlib import Path

import httpx
import pytest

from core.settings_loader import load_settings
from llm import lich_trinh as lt
from llm import thoi_tiet as tt
from llm.assistant import AnswerTrace, AssistantFlags, _dong_thoi_tiet_lich, _thoi_tiet_cuoi, answer_turn, answer_turn_stream
from llm.do_so import do_ngay_di
from retrieval.full_corpus_context import PackedSource
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps`: Qdrant thật, chỉ đọc)
from test_b5_lich_trinh import BANG, ON, lich_call, tool_names, viet_theo_khung

NGAY0 = date(2026, 11, 6)  # thứ Sáu


def phan_hoi(xs=(20, 80, 10, 0, 65, 30, 5), **sua) -> dict:
    """Khuôn phản hồi Open-Meteo (forecast, `daily` + `current`) — số tự đặt; `sua` ghi đè một cột."""
    daily = {"time": [(NGAY0 + timedelta(days=i)).isoformat() for i in range(7)],
             "temperature_2m_max": [29.6, 27.4, 30.0, 31.2, 26.5, 28.0, 29.0],
             "temperature_2m_min": [23.2, 22.6, 24.0, 24.4, 21.9, 22.0, 23.0],
             "precipitation_probability_max": list(xs), "precipitation_sum": [0.4, 12.25, 0.0, 0.0, 8.0, 1.0, 0.0]}
    daily.update(sua)
    return {"latitude": 16.46, "longitude": 107.59, "timezone": "Asia/Ho_Chi_Minh", "current": {"time": "2026-11-06T09:15", "temperature_2m": 26.1},
            "daily": daily}


def nguon(status=200, body=None, exc=None, calls=None):
    def handler(request):
        if calls is not None:
            calls.append(request)
        if exc is not None:
            raise exc
        return httpx.Response(status, json=phan_hoi() if body is None else body) if not isinstance(body, bytes) else httpx.Response(status, content=body)
    return functools.partial(tt.lay_du_bao, transport=httpx.MockTransport(handler))


def du_bao_ok():
    return asyncio.run(nguon()())


WEATHER = dataclasses.replace(ON, lich_trinh=False, bang_lich=None, thoi_tiet=True, du_bao=nguon())
OFF = AssistantFlags(tim_them=True)


# ---------- D4 từ khoá / D6 bão lũ / D3 ngoài 7 ngày / D5 buổi ----------

@pytest.mark.parametrize("cau, co", [
    ("Mai Huế có mưa không?", True), ("Thời tiết Huế cuối tuần thế nào?", True), ("Huế hôm nay nóng không", True),
    ("Lăng Tự Đức mở cửa mấy giờ?", False), ("Mai đi Huế có cần mang ô không?", False),  # câu lạ không từ khoá ⇒ không công cụ (D8 vẫn chạy)
    ("Trời ơi, vé Đại Nội bao nhiêu?", True),  # giới hạn: "trời ơi" khớp từ khoá (plan §3 ghi là giới hạn)
])
def test_keyword(cau, co):
    assert tt.co_tu_khoa(cau) is co


def test_previous_question_with_keyword_offers_tool():  # m-2: "còn chủ nhật?" sau câu thời tiết
    assert tt.co_tu_khoa_luot("Còn chủ nhật?", (("Thời tiết Huế thứ bảy?", ""),)) and not tt.co_tu_khoa_luot("Còn chủ nhật?", ())


@pytest.mark.parametrize("cau, bao_lu", [
    ("Tuần này Huế có bão không?", True), ("Mùa lũ có nên đi Huế?", True), ("Đường nào hay ngập?", True), ("Có cảnh báo mưa lớn không?", True),
    ("Lăng có cảnh báo bậc thang không?", False), ("Có cảnh báo đường trơn không?", False),  # m-3
])
def test_storm_flood(cau, bao_lu):
    assert tt.la_cau_bao_lu(cau) is bao_lu


def test_beyond_seven_days_and_part_of_day():
    assert tt.ngoai_7_ngay("Tuần sau Huế mưa không?", NGAY0) and tt.ngoai_7_ngay("Ngày 20/11 trời thế nào?", NGAY0)
    assert not tt.ngoai_7_ngay("Ngày 8/11 trời thế nào?", NGAY0) and not tt.ngoai_7_ngay("Mai thế nào?", NGAY0)
    assert tt.co_buoi("Chiều nay có mưa không?") and tt.co_buoi("buổi tối mai") and not tt.co_buoi("Mai có mưa không?")


@pytest.mark.parametrize("cau, n", [("lịch mai", 1), ("ngày kia", 2), ("thứ Bảy này", 1), ("cuối tuần này", 1), ("8/11", 2), ("ngày thứ ba đi đâu", None),
                                    ("mai và chủ nhật", None), ("lịch 2 ngày", None), ("20/11", None)])
def test_travel_day(cau, n):
    assert do_ngay_di(cau, NGAY0) == n


# ---------- D7 lấy dự báo: schema, miền, lỗi, cache ----------

def test_parse_rounds_and_reads_update_time():
    kq = du_bao_ok()
    assert kq.trang_thai == "ok" and kq.cap_nhat == "09:15 06/11" and len(kq.ngay) == 7
    d = kq.ngay[1]
    assert (d["tmin"], d["tmax"], d["xs"], d["mua"]) == (23, 27, 80, 12.2)


@pytest.mark.parametrize("kw, loi", [
    ({"status": 500}, "http_500"), ({"status": 429}, "http_429"), ({"exc": httpx.ReadTimeout("t")}, "het_gio"), ({"exc": httpx.ConnectError("c")}, "mang"),
    ({"body": b"<html>"}, "schema"), ({"body": {"daily": {}}}, "schema"),
    ({"body": phan_hoi(temperature_2m_max=[99] * 7)}, "schema"),  # số ngoài miền ⇒ lỗi, không đưa số
    ({"body": phan_hoi(precipitation_probability_max=[120] * 7)}, "schema"), ({"body": phan_hoi(time=["2026-11-06"])}, "schema"),
])
def test_failures_give_no_numbers(kw, loi):
    kq = asyncio.run(nguon(**kw)())
    assert (kq.trang_thai, kq.loi, kq.ngay) == ("loi", loi, [])


def test_request_has_only_fixed_coordinates_and_vietnam_timezone():
    calls = []
    asyncio.run(nguon(calls=calls)())
    q = dict(calls[0].url.params)
    assert str(calls[0].url).startswith(tt.OPEN_METEO_URL) and q["timezone"] == "Asia/Ho_Chi_Minh" and q["forecast_days"] == "7"
    assert (float(q["latitude"]), float(q["longitude"])) == (tt.HUE_LAT, tt.HUE_LON) and set(q) == {"latitude", "longitude", "timezone", "forecast_days", "current", "daily"}


def test_cache_returns_without_network(monkeypatch):
    monkeypatch.setattr(tt, "_CACHE", {"kq": du_bao_ok(), "t": tt.time.monotonic()})
    kq = asyncio.run(tt.lay_du_bao())  # không transport ⇒ nếu không có cache sẽ ra mạng thật; cache còn hạn ⇒ trả ngay
    assert kq.trang_thai == "ok" and kq.tu_cache


# ---------- D5 khối số liệu ----------

def test_block_has_fixed_lines_source_and_time():
    khoi = tt.khoi_du_bao(du_bao_ok(), 1, 2, buoi=True)
    assert khoi.splitlines() == [
        tt.TIEU_DE, "- Thứ Bảy 07/11: 23–27 °C, khả năng mưa 80 %, lượng mưa 12,2 mm", "- Chủ nhật 08/11: 24–30 °C, khả năng mưa 10 %, lượng mưa 0,0 mm",
        f"- {tt.CAU_THEO_CA_NGAY}", f"{tt.GHI_CONG} — số liệu lúc 09:15 06/11. {tt.CAU_CO_THE_DOI}"]


# ---------- D8 mỗi dạng số ----------

@pytest.mark.parametrize("text, so", [
    ("Mai khoảng 27 °C.", ["27"]), ("cao nhất 27°", ["27"]), ("tầm 27 độ", ["27"]), ("27 độ C", ["27"]), ("khả năng mưa 80 %", ["80"]),
    ("khả năng mưa tám mươi phần trăm, tức 80 phần trăm", ["80"]), ("lượng mưa 12,2 mm", ["12,2"]), ("mưa 12.2 mi-li-mét", ["12,2"]),
    ("mưa khoảng 12 li", ["12"]), ("nhiệt độ 23–27 °C", ["23", "27"]), ("từ 23 đến 27 độ", ["23", "27"]),
    ("Vé giảm 50 % cho trẻ em.", []), ("Gọi 2 li cà phê.", []), ("Đi 3 ngày, 2 người.", []),
])
def test_weather_number_forms(text, so):
    assert tt.so_thoi_tiet(text) == so


def _trace(text_cited="", tool_khoi=None, **ctx):
    trace = AnswerTrace(answer="chữ model", cited=(PackedSource(1, "t", (), (text_cited,)),) if text_cited else ())
    trace.thoi_tiet_ctx = {"bao_lu": False, "ngoai_7": False, "buoi": False, "co_cong_cu": tool_khoi is not None, **ctx}
    if tool_khoi is not None:
        trace.thoi_tiet = {"trang_thai": "ok" if tool_khoi else "loi", "khoi": tool_khoi or None}
    return trace


def test_model_numbers_must_come_from_code_or_cited_kho():
    khoi = tt.khoi_du_bao(du_bao_ok(), 1, 1)
    ok = _trace(tool_khoi=khoi)
    _thoi_tiet_cuoi(ok, "Mai Huế 23–27 °C, khả năng mưa 80 % — mang ô nhé.")
    assert ok.citation_error is None and ok.answer.endswith(khoi)
    bia = _trace(tool_khoi=khoi)
    _thoi_tiet_cuoi(bia, "Mai Huế khoảng 35 độ.")  # cố tình: số model tự thêm
    assert bia.thoi_tiet_kiem == ["35"] and bia.citation_error is not None


def test_number_without_tool_is_caught_but_cited_climate_number_is_not():
    tu_viet = _trace()
    _thoi_tiet_cuoi(tu_viet, "Mai chắc khoảng 30 °C.")  # lượt không công cụ (không từ khoá) ⇒ D8 vẫn chặn
    assert tu_viet.citation_error is not None
    kho = _trace(text_cited="Mùa hè Huế nóng, nhiệt độ có ngày lên 38 °C.")
    _thoi_tiet_cuoi(kho, "Mùa hè có ngày tới 38 °C [1].")  # câu khí hậu trích kho có số ⇒ không bị rút nhầm
    assert kho.citation_error is None and kho.thoi_tiet_noi is None and kho.answer == "chữ model"


def test_api_error_appends_fixed_sentence_storm_line_and_beyond_line():
    t = _trace(tool_khoi="", bao_lu=True, ngoai_7=True)
    _thoi_tiet_cuoi(t, "Mình chưa có số liệu.")
    assert t.citation_error is None and t.thoi_tiet_noi == "\n\n".join([tt.CAU_LOI, tt.CAU_BAO_LU, tt.CAU_NGOAI_7_NGAY])
    assert "112" in tt.CAU_BAO_LU and tt.NCHMF_URL in tt.CAU_BAO_LU and not tt.so_thoi_tiet(t.thoi_tiet_noi)


def test_staircase_warning_question_gets_no_nchmf_line():
    t = _trace(bao_lu=tt.la_cau_bao_lu("Lăng có cảnh báo bậc thang không?"))
    _thoi_tiet_cuoi(t, "Có nhiều bậc [1].")
    assert t.thoi_tiet_noi is None


# ---------- D9 / D10 lịch (bảng v4: cột trong nhà / bậc thang — User chưa duyệt; code chỉ đọc cột) ----------

V4 = lt.nap_bang(Path(__file__).resolve().parents[2] / "data/phase_9/lich_trinh/diem_v4.json")


def _co_cot(bang) -> bool:
    return any(d.get("trong_nha") == "ngoai_troi" for d in bang.diem) and any(d.get("trong_nha") in ("trong_nha", "ca_hai") for d in bang.diem)


@pytest.mark.skipif(not _co_cot(V4), reason="bảng v4 chưa có cột trong nhà / ngoài trời")
def test_itinerary_day_forecast_and_rain_alternative(monkeypatch):
    monkeypatch.setattr("llm.assistant.hom_nay_vn", lambda: NGAY0)
    khung = lt.xep(V4, lt.ThamSo(so_ngay="2", so_thich="di_tich"))
    trace = AnswerTrace(lich={"khung": khung})
    dong = asyncio.run(_dong_thoi_tiet_lich(V4, khung, "Lên lịch 2 ngày từ mai giúp mình", nguon(body=phan_hoi(xs=(0, 90, 90, 0, 0, 0, 0))), trace))
    assert dong[0].startswith("Ngày 1 — Thứ Bảy 07/11:") and any(x.startswith("Ngày 2 — Chủ nhật 08/11:") for x in dong)
    assert dong[-1].startswith(tt.GHI_CONG) and trace.lich["thoi_tiet"]["trang_thai"] == "ok"
    ngoai = [i for b in lt.BUOI for i in khung["ngay"][0]["buoi"][b] if V4.theo_id[i].get("trong_nha") == "ngoai_troi"]
    assert any(x.startswith("Nếu mưa ngày 1") for x in dong) == bool(ngoai and any(
        d.get("trong_nha") in ("trong_nha", "ca_hai") and d["cum"] == V4.theo_id[ngoai[0]]["cum"] and d["id"] not in lt.diem_trong_khung(khung)
        for d in V4.diem))


def test_itinerary_without_day_or_with_api_error(monkeypatch):
    monkeypatch.setattr("llm.assistant.hom_nay_vn", lambda: NGAY0)
    khung = lt.xep(BANG, lt.ThamSo(so_ngay="1"))
    calls = []
    assert asyncio.run(_dong_thoi_tiet_lich(BANG, khung, "Lên lịch 1 ngày", nguon(calls=calls), AnswerTrace(lich={}))) == [] and calls == []
    loi = asyncio.run(_dong_thoi_tiet_lich(BANG, khung, "Lên lịch mai", nguon(status=500), AnswerTrace(lich={})))
    assert loi == [tt.CAU_LOI]  # lịch như B5 + câu cố định, 0 số
    note = lt.khoi_ghi_chu(BANG, khung, {i: 1 for i in lt.diem_trong_khung(khung)}, loi)
    assert note.endswith(f"- {tt.CAU_LOI}") and lt.kiem_ghi_chu(BANG, khung, note) == []


def test_staircase_note_only_for_elderly():
    co = next((d for d in V4.diem if d.get("bac_thang") == "nhieu"), None)
    if co is None:
        pytest.skip("bảng v4 chưa ghi bậc thang")
    khung = lt.xep(V4, lt.ThamSo(so_ngay="1", di_cung="nguoi_lon_tuoi", them_diem=(co["ten"],)))
    if co["id"] not in lt.diem_trong_khung(khung):
        pytest.skip("điểm nhiều bậc không xếp được cho người lớn tuổi")
    dong = asyncio.run(_dong_thoi_tiet_lich(V4, khung, "Lên lịch 1 ngày", nguon(), AnswerTrace(lich={})))
    assert f"{co['ten']} có nhiều bậc thang (theo kho)." in dong


# ---------- nối vào lõi: SDK thật + client kịch bản + Qdrant thật ----------

def tt_call(tu=1, den=1) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "thoi_tiet",
            "arguments": json.dumps({"tu_ngay": tu, "den_ngay": den}), "status": "completed"}


def run(deps, query, gen, flags, history=(), stream=False):
    trace = AnswerTrace(history=history)

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(query, *deps, gen, trace, flags)]
        await answer_turn(query, *deps, gen, trace, flags)

    return trace, asyncio.run(go())


def test_tool_only_with_keyword_and_flag_off_request_unchanged(deps):
    seen = []
    gen = generator(lambda n, kw: (seen.append(tool_names(kw)), [answer("Lăng nằm ở ngoại ô [1].")])[1])
    run(deps, "Lăng Tự Đức ở đâu?", gen, WEATHER)
    run(deps, "Lăng Tự Đức ở đâu?", gen, OFF)
    run(deps, "Mai Huế có mưa không?", gen, WEATHER)
    run(deps, "Còn chủ nhật?", gen, WEATHER, history=(("Thời tiết Huế thứ bảy?", ""),))
    assert seen[0] == seen[1] == ["tim_kho"] and seen[2] == seen[3] == ["tim_kho", "thoi_tiet"]


def test_forecast_turn_appends_code_block_and_catches_invented_number(deps):
    def script(text):
        return lambda n, kw: [tt_call(1, 1)] if n == 1 else [answer(text)]
    flags = dataclasses.replace(WEATHER, du_bao=nguon())
    ok, _ = run(deps, "Mai Huế có mưa không?", generator(script("Mai Huế 23–27 °C, khả năng mưa 80 %, nên mang ô.")), flags)
    assert ok.citation_error is None and ok.answer.endswith(ok.thoi_tiet["khoi"]) and ok.thoi_tiet["n_ngay"] == 1
    bia, _ = run(deps, "Mai Huế có mưa không?", generator(script("Mai Huế khoảng 33 độ.")), flags)
    assert bia.citation_error is not None and bia.thoi_tiet_kiem == ["33"]


def test_api_error_turn_has_fixed_sentence_and_no_numbers(deps):
    flags = dataclasses.replace(WEATHER, du_bao=nguon(status=503))
    trace, _ = run(deps, "Mai Huế có mưa không?", generator(lambda n, kw: [tt_call()] if n == 1 else [answer("Mình chưa lấy được dự báo.")]), flags)
    assert trace.citation_error is None and trace.answer.endswith(tt.CAU_LOI) and not tt.so_thoi_tiet(trace.answer)


def test_stream_deltas_equal_final_answer(deps):
    flags = dataclasses.replace(WEATHER, du_bao=nguon())
    trace, events = run(deps, "Mai Huế có bão không?", generator(lambda n, kw: [tt_call()] if n == 1 else [answer("Mai trời 23–27 °C.")]), flags,
                        stream=True)
    shown = "".join(d for k, d in events if k == "delta")
    assert shown == trace.answer and tt.CAU_BAO_LU in shown and ("status", {"stage": "thoi_tiet"}) in events


def test_itinerary_turn_with_day_puts_forecast_in_notes(deps, monkeypatch):
    monkeypatch.setattr("llm.assistant.hom_nay_vn", lambda: NGAY0)
    flags = dataclasses.replace(ON, thoi_tiet=True, du_bao=nguon())
    cau = "Lên lịch 1 ngày ở Huế từ mai giúp mình, mình thích di tích"
    gen = generator(lambda n, kw: [lich_call(so_ngay="1", so_thich="di_tich")] if n == 1 else [answer(viet_theo_khung(kw))])
    trace, _ = run(deps, cau, gen, flags)
    goc, _ = run(deps, cau, generator(lambda n, kw: [lich_call(so_ngay="1", so_thich="di_tich")] if n == 1 else [answer(viet_theo_khung(kw))]), ON)
    assert trace.citation_error is None and trace.lich["khung"] == goc.lich["khung"]  # khung lịch giống B5
    assert "Ngày 1 — Thứ Bảy 07/11:" in trace.lich["ghi_chu"] and tt.GHI_CONG in trace.lich["ghi_chu"]


def test_no_citation_allowed_only_for_weather_tool_turns():
    """Bất biến: chỉ lỗi "không có [n]" ở lượt có gọi công cụ thời tiết được bỏ qua; mã lạ / lượt không công cụ vẫn rút lại."""
    from core.schema import CitationIntegrityError
    from llm.assistant import NO_CITATION
    khoi = tt.khoi_du_bao(du_bao_ok(), 1, 1)
    co_tool = _trace(tool_khoi=khoi)
    co_tool.citation_error = CitationIntegrityError(NO_CITATION)
    _thoi_tiet_cuoi(co_tool, "Mai trời 23–27 °C.")
    assert co_tool.citation_error is None and co_tool.cited == ()
    ma_la = _trace(tool_khoi=khoi)
    ma_la.citation_error = CitationIntegrityError("Unknown citation IDs: [9]")
    _thoi_tiet_cuoi(ma_la, "Mai trời 23–27 °C [9].")
    assert ma_la.citation_error is not None
    khong_tool = _trace()
    khong_tool.citation_error = CitationIntegrityError(NO_CITATION)
    _thoi_tiet_cuoi(khong_tool, "Huế đẹp lắm.")
    assert khong_tool.citation_error is not None
