"""Nhớ câu trả lời giữa các cuộc trò chuyện (cờ `cache_cau_tra_loi`, plan `report_agent/2026-11-20/b_cache_cau_tra_loi_plan.md`) — 0 USD, không mạng.

Phần kho + luật lưu là logic thuần. Phần route: app thật + tìm kho thật (Qdrant chỉ đọc); model là SDK thật với client trả phản hồi dựng sẵn
(`test_b2_tool_loop.generator`) — đếm được số lần gọi model. Không phải bằng chứng trên model thật: phần đó là một lượt thật ghi ở report.
"""
import json

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.cache_tra_loi import BanLuu, CacheTraLoi, chuan_hoa, dau_phien_ban, luot_luu_duoc
from api.routes.chat import METRIC_FIELDS, STREAM_METRIC_FIELDS
from core.settings_loader import load_settings
from llm import thoi_tiet as tt
from llm.assistant import AnswerTrace, AssistantFlags
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import answer, generator
from test_chat_stream import parse_sse

CAU = "Đại Nội Huế mở cửa lúc mấy giờ?"
CHU = "Đại Nội mở cửa từ sáng [1]."


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def ban(chu: str = "đáp [1]") -> BanLuu:
    return BanLuu(answer=chu, cited=("nguồn",), notice=None, route="tro_ly_hue")


# ---------- Logic thuần ----------

def test_chuan_hoa_gop_khoang_trang_va_hoa_thuong_nhung_giu_dau_va_dau_cau():
    assert chuan_hoa("  Đại Nội   MỞ cửa\tmấy giờ? ") == chuan_hoa("đại nội mở cửa mấy giờ?")
    assert chuan_hoa("Đại Nội") == chuan_hoa("Đại Nội")  # dạng tổ hợp ⇒ NFC
    for khac in ("đại nội mở cửa mấy giờ", "đại nội mở của mấy giờ?", "đại nội mở cửa mấy gio?", "đại nội đóng cửa mấy giờ?"):
        assert chuan_hoa(khac) != chuan_hoa("đại nội mở cửa mấy giờ?")  # thiếu "?", khác dấu thanh, khác chữ ⇒ câu khác


def test_kho_trung_dung_chu_het_han_tran_va_phien_ban():
    clock = Clock()
    kho = CacheTraLoi("kho-1", song_giay=10, tran=2, clock=clock)
    kho.luu("Câu A?", ban("a"))
    assert kho.lay("  câu  a? ").answer == "a" and kho.lay("Câu A") is None and kho.lay("Câu B?") is None
    clock.now = 9.9
    assert kho.lay("Câu A?") is not None
    clock.now = 10  # đúng hạn ⇒ coi như không có, mục bị bỏ
    assert kho.lay("Câu A?") is None and len(kho) == 0
    kho.luu("1", ban("1")), kho.luu("2", ban("2")), kho.luu("3", ban("3"))  # mục thứ ba đẩy mục lưu sớm nhất
    assert kho.lay("1") is None and kho.lay("2").answer == "2" and kho.lay("3").answer == "3" and len(kho) == 2
    # kho / lời dặn / model / cờ đổi ⇒ dấu phiên bản khác ⇒ cùng câu không trúng
    khac = CacheTraLoi("kho-2", clock=clock)
    khac._muc = kho._muc
    assert khac.lay("2") is None
    assert dau_phien_ban("ab", "c") != dau_phien_ban("a", "bc") and dau_phien_ban("x", b"y") == dau_phien_ban("x", "y")


def luot_kho() -> AnswerTrace:
    return AnswerTrace(answer=CHU, cited=("nguồn",), tools=[{"name": "tim_kho", "ms": 1.0}, {"name": "tim_kho", "ms": 1.0, "by": "model"}])


@pytest.mark.parametrize("doi", [
    lambda t: setattr(t, "cited", ()),  # không trích nguồn kho nào
    lambda t: setattr(t, "fixed_outcome", "refusal_no_sources"),  # câu cố định (từ chối, ngoài phạm vi, nói thật giới hạn…)
    lambda t: setattr(t, "citation_error", ValueError("x")),
    lambda t: setattr(t, "web", {"outcome": "co_muc"}),
    lambda t: t.tools.append({"name": "thoi_tiet", "ms": 1.0}),
    lambda t: t.tools.append({"name": "ngay_lich", "ms": 1.0}),
    lambda t: t.tools.append({"name": "khoang_cach_san", "ms": 0.0}),
    lambda t: t.tools.append({"name": "lich_dang_co", "ms": 0.0}),
    lambda t: setattr(t, "lich", {"nguon": []}),
    lambda t: setattr(t, "lich_v2", {"lich": {}}),
    lambda t: setattr(t, "clarify", {"loai": "lich_trinh", "truong": []}),
    lambda t: setattr(t, "lam_thay", "dat_phong"),
    lambda t: setattr(t, "today", "Hôm nay là thứ Sáu, 20/11/2026"),
    lambda t: setattr(t, "thoi_tiet_noi", "khối dự báo"),
    lambda t: setattr(t, "thoi_tiet_dau", "câu cố định"),
    lambda t: setattr(t, "notice", f"{tt.CAU_BAO_LU} Thông tin có thể đã thay đổi."),
    lambda t: setattr(t, "luu_y_nguon", "Điểm này đang tạm ngừng đón khách."),
])
def test_chi_luu_luot_tra_loi_tu_kho_thuan(doi):
    assert luot_luu_duoc(luot_kho(), tu_choi=False)
    assert not luot_luu_duoc(luot_kho(), tu_choi=True)
    trace = luot_kho()
    doi(trace)
    assert not luot_luu_duoc(trace, tu_choi=False)


def test_co_mac_dinh_tat_va_khong_co_kho_khi_tat():
    assert AssistantFlags().cache_cau_tra_loi is False
    assert AssistantFlags.from_settings({"assistant": {"cache_cau_tra_loi": True}}).cache_cau_tra_loi is True


# ---------- Route thật, model dựng sẵn ----------

def kich_ban(chu: str):
    """Định tuyến ⇒ `tro_ly_hue`; trợ lý ⇒ trả `chu` ngay (lần tìm đầu do code làm — `lan_tim_dau: v0`)."""
    def script(n, kw):
        instructions = kw.get("instructions") or ""
        if "tro_ly_hue" in instructions and "ngoai_pham_vi" in instructions:  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        return [answer(chu)]
    return script


@pytest.fixture(scope="module")
def may():
    """Một app cho cả file (dựng app nạp e5 + Qdrant — không dựng nhiều lần). Mỗi test tự đặt generator + kho nhớ mới."""
    app = create_app(load_settings())
    with TestClient(app) as client:
        goc = app.state.generator, app.state.generator_ready, app.state.tim_web
        app.state.generator_ready, app.state.tim_web = True, None  # không tra web trong test (không mạng)
        yield app, client
        app.state.generator, app.state.generator_ready, app.state.tim_web = goc
        app.state.cache_tra_loi = None


def dat(may, chu: str = CHU, bat: bool = True):
    app, client = may
    app.state.generator = generator(kich_ban(chu))
    app.state.cache_tra_loi = CacheTraLoi("thu") if bat else None
    client.cookies.clear()
    return app, client, app.state.generator.client.responses.calls


def hoi(client, cau: str, cuoc_moi: bool = True) -> dict:
    if cuoc_moi:
        client.cookies.clear()
    r = client.post("/api/chat", json={"query": cau})
    assert r.status_code == 200, r.text
    return r.json()


def hoi_stream(client, cau: str, cuoc_moi: bool = True) -> list[tuple[str, object]]:
    if cuoc_moi:
        client.cookies.clear()
    r = client.post("/api/chat/stream", json={"query": cau})
    assert r.status_code == 200, r.text
    return parse_sse([block.encode() + b"\n\n" for block in r.text.split("\n\n") if block.strip()])


def chu_stream(events) -> str:
    return "".join(data["text"] for name, data in events if name == "delta")


def test_nguoi_khac_hoi_dung_cau_do_nhan_lai_ban_luu_khong_goi_model(may, caplog):
    app, client, calls = dat(may)
    with chat_log_records(caplog) as records:
        lan_1 = hoi(client, CAU)
        n_1 = len(calls)
        lan_2 = hoi(client, "  đại nội huế   MỞ CỬA lúc mấy giờ? ")  # cuộc khác; khác hoa thường + khoảng trắng
        qua_stream = hoi_stream(client, CAU)  # cuộc thứ ba, đường stream
        metrics = metric_lines(records)
    assert n_1 >= 2 and len(calls) == n_1  # lần một: định tuyến + trả lời; hai lần sau: 0 lần gọi model
    assert lan_1["sources"] and lan_1["answer"] == "Đại Nội mở cửa từ sáng [1]."
    assert {k: lan_2[k] for k in ("answer", "sources", "notice")} == {k: lan_1[k] for k in ("answer", "sources", "notice")}
    assert lan_2["turn_id"] != lan_1["turn_id"]  # mã lượt (đánh giá) vẫn riêng từng lượt
    ten = [name for name, _ in qua_stream]
    assert ten == [n for n in ("delta", "sources", "notice", "done") if n in ten] and ten.count("delta") == 1  # không sự kiện tiến độ: bước không chạy
    assert chu_stream(qua_stream) == lan_1["answer"] and dict(qua_stream)["sources"] == lan_1["sources"]
    assert dict(qua_stream)["done"]["outcome"] == "success" and ("notice" in ten) == (lan_1["notice"] is not None)
    assert [m["cache"] for m in metrics] == ["truot", "trung", "trung"]
    for m in metrics[1:]:
        assert m["outcome"] == "success" and m["n_llm_calls"] == 0 and m["usd"] == 0 and m["search_ms"] is None and m["refusal"] is False
        assert m["n_cited_sources"] == metrics[0]["n_cited_sources"] and m["route"] == "tro_ly_hue"
    assert set(metrics[1]) == set(METRIC_FIELDS) | {"cache"} and set(metrics[2]) == set(STREAM_METRIC_FIELDS) | {"cache"}
    assert all(CAU not in r.getMessage() and "Đại Nội mở cửa" not in r.getMessage() for r in records)  # log không chữ


def test_luot_stream_cung_luu_va_luot_trung_van_vao_lich_su_cua_cuoc(may, caplog):
    app, client, calls = dat(may)
    lan_1 = hoi_stream(client, CAU)
    n_1 = len(calls)
    with chat_log_records(caplog) as records:
        lan_2 = hoi(client, CAU)  # cuộc mới, trúng bản do lượt stream lưu
        hoi(client, "Còn giá vé thì sao?", cuoc_moi=False)  # lượt hai của CÙNG cuộc: có lịch sử ⇒ không tra, không lưu
        metrics = metric_lines(records)
    assert "status" in [name for name, _ in lan_1] and chu_stream(lan_1) == lan_2["answer"] and dict(lan_1)["sources"] == lan_2["sources"]
    # dòng log của lượt stream ghi ở `finally` của luồng — bộ thử đóng luồng muộn nên nó có thể rơi vào đây ⇒ đọc hai dòng CUỐI
    assert len(calls) > n_1 and metrics[-2]["cache"] == "trung" and metrics[-2]["n_llm_calls"] == 0
    assert metrics[-1]["n_history_turns"] == 1 and "cache" not in metrics[-1]  # lượt trúng đã được nhớ như lượt thường


def test_ca_nguoc_khong_trung(may, caplog):
    app, client, calls = dat(may)
    with chat_log_records(caplog) as records:
        hoi(client, CAU)
        for cau in ("Đại Nội Huế mở cửa lúc mấy giờ", "Đại Nội Huế mở cửa lúc mấy gio?", "Đại Nội Huế đóng cửa lúc mấy giờ?"):
            truoc = len(calls)
            hoi(client, cau)  # thiếu "?", khác một dấu thanh, khác một chữ ⇒ câu khác ⇒ model được gọi
            assert len(calls) > truoc, cau
        truoc = len(calls)
        hoi(client, CAU, cuoc_moi=False)  # cùng câu nhưng là lượt hai của một cuộc ⇒ không tra
        assert len(calls) > truoc
        truoc = len(calls)
        r = client.post("/api/chat", json={"query": CAU, "truong": {}})  # lượt từ nút ("Trả lời luôn") ⇒ không tra
        assert r.status_code == 200 and len(calls) > truoc
        metrics = metric_lines(records)
    assert [m.get("cache") for m in metrics] == ["truot", "truot", "truot", "truot", None, None]


def test_cau_tu_choi_khong_luu(may):
    app, client, calls = dat(may, chu=INSUFFICIENT_ANSWER)
    hoi(client, CAU)
    n_1 = len(calls)
    hoi(client, CAU)
    hoi_stream(client, CAU)
    assert len(calls) >= 3 * n_1 > 0 and len(app.state.cache_tra_loi) == 0  # hỏi ba lần ⇒ model được gọi cả ba lần


def test_co_tat_khong_tra_khong_luu_va_dong_log_nhu_cu(may, caplog):
    app, client, calls = dat(may, bat=False)
    with chat_log_records(caplog) as records:
        hoi(client, CAU)
        n_1 = len(calls)
        hoi(client, CAU)
        hoi_stream(client, CAU)
        metrics = metric_lines(records)
    assert len(calls) >= 3 * n_1 > 0
    assert set(metrics[0]) == set(metrics[1]) == set(METRIC_FIELDS) and set(metrics[2]) == set(STREAM_METRIC_FIELDS)
