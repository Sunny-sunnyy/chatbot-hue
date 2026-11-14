"""Cổng du lịch đợt 1 — S1 backend (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` D3 / D4 / D6 / D7, §6 Q-F phần tất định,
Q-K) — 0 USD.

Đường biểu mẫu: SDK thật + client giả có kịch bản (không mạng) + Qdrant thật (đọc) + bảng điểm thật (`diem_v3.json`, private) — như
`test_b5_lich_trinh.py`. Chuỗi gửi model kiểm theo **mỗi loại lượt** (`WORKFLOW.md` §4 (4c)): lượt biểu mẫu đầu, lượt biểu mẫu có lịch sử, lượt hỏi
tiếp sau biểu mẫu; "cờ tắt giống byte" đo bằng Q1 (`capture_all.py`, report S1). Đây **không** là bằng chứng chữ model thật khớp khung — phần đó
ở S3 (lượt có phí, Q-F F-a).
"""
import asyncio
import copy
import dataclasses
import itertools
import json
import re
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.routes.chat import CAU_BIEU_MAU, _source_responses
from core.settings_loader import load_settings
from llm import lich_trinh as lt
from llm.do_so import do_ngay_di
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream_parallel
from llm.full_corpus_prompt import ANSWER_SYSTEM_INSTRUCTIONS, INSUFFICIENT_ANSWER, LICH_TRINH_LUAT
from llm.hoi_lai import GIA_TRI, TruongInput, ghep_cau
from retrieval.full_corpus_context import PackedSource
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)
from test_b5b_thoi_tiet import nguon
from test_chat_stream import parse_sse

SETTINGS = load_settings(validate_private_paths=False)
BUILD_RECORD = Path(__file__).resolve().parents[2] / "data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json"


def flags_from(**assistant) -> AssistantFlags:
    s = copy.deepcopy(SETTINGS)
    s["assistant"].update(assistant)
    return AssistantFlags.from_settings(s)


# settings.yaml bật biểu mẫu + thời tiết từ 07/11 ⇒ mốc "cờ biểu mẫu tắt" đặt rõ; mọi cờ khác như đang chạy (định tuyến, #6, tra web…) ⇒ so đúng một cờ
OFF = flags_from(lich_trinh_bieu_mau=False)
FORM = flags_from(lich_trinh_bieu_mau=True)
TRUONG = ("so_ngay", "di_cung", "kieu_di", "so_thich")
FORM_INSTRUCTIONS = f"{ANSWER_SYSTEM_INSTRUCTIONS}\n\n{LICH_TRINH_LUAT}"  # V5 (X1c của C): luật lịch trong lời dặn hệ thống của lượt biểu mẫu


def effort(kwargs):
    """Mức suy luận trong thân yêu cầu gửi OpenAI: SDK gửi `Reasoning(effort=…)`, không đặt ⇒ `Omit` (không có `effort`) ⇒ None."""
    return getattr(kwargs.get("reasoning"), "effort", None)


def chu_gui(kwargs) -> str:
    """Mọi chữ trong `input` một lần gọi (tin nhắn user / lịch sử)."""
    out = []

    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(kwargs["input"])
    return "\n".join(out)


def tools_of(kwargs) -> list:
    tools = kwargs.get("tools")
    return tools if isinstance(tools, list) else []


def viet_theo_khung(kwargs) -> str:
    """Model giả "đúng luật" cho lượt biểu mẫu: khung nằm trong tin nhắn user (không phải kết quả công cụ)."""
    dong = re.findall(r"^- (Sáng|Chiều|Tối): (.+?)(?: ◦)? \[(\d+)\]", chu_gui(kwargs), re.M)
    return "\n".join(f"{buoi}: ghé {ten} — điểm đáng xem [{n}]." for buoi, ten, n in dong)


def form_trace(truong: dict, history=()) -> tuple[str, AnswerTrace]:
    trace = AnswerTrace(truong=truong, search_query=CAU_BIEU_MAU, bieu_mau=True, history=history)
    return ghep_cau(CAU_BIEU_MAU, TruongInput(**truong)), trace


def run(deps, query, gen, flags, trace, stream=False):
    async def go():
        if stream:  # đường route stream: qua `answer_turn_stream_parallel` (#6 bật trong OFF / FORM)
            return [e async for e in answer_turn_stream_parallel(query, *deps, gen, trace, flags)]
        await answer_turn(query, *deps, gen, trace, flags)
    return asyncio.run(go())


# ---------- Q-F phần tất định: mọi tổ hợp nút ⇒ khung nhận đúng giá trị nút, 0 hỏi lại, 0 công cụ, 1 lần gọi ----------

def test_qf_every_button_combo_reaches_the_frame_unchanged(deps):
    # Q-U3 chưa chốt ⇒ mặc định spec: ẩn "đi dày" ⇒ biểu mẫu không gửi `kieu_di` (khung dùng mặc định của code — không phải giá trị model)
    combos = list(itertools.product(GIA_TRI["so_ngay"], GIA_TRI["di_cung"], [None], [None, *GIA_TRI["so_thich"]]))
    assert len(combos) == 4 * 5 * 6
    gen = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
    lech, khong_qua = [], []
    for combo in combos:
        truong = {k: v for k, v in zip(TRUONG, combo) if v is not None}
        query, trace = form_trace(truong)
        run(deps, query, gen, FORM, trace)
        ts = trace.lich["khung"]["tham_so"]
        if {k: ts[k] for k in TRUONG} != {k: truong.get(k) for k in TRUONG} or ts["so_ngay_tam"] or ts["hoi_toi"] or trace.clarify is not None:
            lech.append(combo)
        if trace.citation_error is not None or trace.lich_kiem:
            khong_qua.append(combo)
    calls = gen.client.responses.calls
    assert lech == [] and khong_qua == []
    assert len(calls) == len(combos)  # đúng 1 lần gọi model / lượt: không định tuyến, không vòng công cụ
    assert all(tools_of(c) == [] and c["instructions"] == FORM_INSTRUCTIONS and effort(c) == "low" for c in calls)


@pytest.mark.parametrize("kieu_di", list(GIA_TRI["kieu_di"]))
def test_qf_walking_style_button_also_reaches_the_frame(deps, kieu_di):
    # nếu User chọn hiện "kiểu đi" ở Q-U3: giá trị nút vẫn tới khung nguyên vẹn
    query, trace = form_trace({"so_ngay": "2", "di_cung": "cap_doi", "kieu_di": kieu_di})
    run(deps, query, generator(lambda n, kw: [answer(viet_theo_khung(kw))]), FORM, trace)
    assert trace.lich["khung"]["tham_so"]["kieu_di"] == kieu_di


def test_fixed_question_never_triggers_evening_or_date_detectors():
    # câu cố định dựng từ nút không được tự bật "xin buổi tối" (B171) hay dò ngày đi (B5b) — mọi tổ hợp kể cả "kiểu đi"
    for combo in itertools.product(*([None, *GIA_TRI[t]] for t in TRUONG)):
        truong = {k: v for k, v in zip(TRUONG, combo) if v is not None}
        cau = ghep_cau(CAU_BIEU_MAU, TruongInput(**truong))
        assert not lt.hoi_buoi_toi(cau) and do_ngay_di(cau, date(2026, 11, 7)) is None, cau


# ---------- chuỗi gửi model theo mỗi loại lượt (4c) ----------

@pytest.mark.parametrize("history", [(), (("Huế có món gì ngon?", ""),)])
@pytest.mark.parametrize("stream", [False, True])
def test_form_turn_request_has_frame_rules_and_no_tools(deps, history, stream):
    gen = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
    query, trace = form_trace({"so_ngay": "2", "di_cung": "gia_dinh_tre_em", "so_thich": "di_tich"}, history)
    events = run(deps, query, gen, FORM, trace, stream)
    (sent,) = gen.client.responses.calls  # 1 lần gọi: #6 song song không chạy, không định tuyến
    text = chu_gui(sent)
    assert tools_of(sent) == [] and sent["instructions"] == FORM_INSTRUCTIONS and effort(sent) == "low"
    assert LICH_TRINH_LUAT in text and f"Câu hỏi:\n{query}" in text  # khung + luật viết lời do code đưa vào ngữ cảnh
    assert ("Huế có món gì ngon?" in text) == bool(history)
    assert trace.route == "tro_ly_hue" and trace.citation_error is None and trace.lich_kiem == []
    assert trace.answer.startswith("Mình hiểu: 2 ngày") and lt.TIEU_DE_GHI_CHU in trace.answer
    assert [t["name"] for t in trace.tools] == ["lich_trinh"] and trace.web is None
    if stream:
        statuses = [d for kind, d in events if kind == "status"]
        assert statuses[0] == {"stage": "lich_trinh", "buoc": "dang_xep"} and statuses[-1] == {"stage": "generating"}
        assert not [s for s in statuses if s["stage"] in ("routing", "searching", "searched")]
        assert "".join(d for kind, d in events if kind == "delta") == trace.answer


@pytest.mark.parametrize("stream", [False, True])
def test_form_turn_model_refusal_becomes_code_built_itinerary(deps, stream):
    # B171 T3 (b) giữ ở lượt biểu mẫu: có khung mà model trả câu từ chối ⇒ code dựng lời lịch tối thiểu; stream không lộ câu từ chối
    query, trace = form_trace({"so_ngay": "1", "di_cung": "nguoi_lon_tuoi"})
    events = run(deps, query, generator(lambda n, kw: [answer(INSUFFICIENT_ANSWER)]), FORM, trace, stream)
    assert trace.lich["chu_thay"] and INSUFFICIENT_ANSWER not in trace.answer and trace.citation_error is None
    if stream:
        assert "".join(d for kind, d in events if kind == "delta") == trace.answer


@pytest.mark.parametrize("stream", [False, True])
def test_follow_up_turn_after_form_goes_like_main(deps, stream):
    # lượt hỏi tiếp sau biểu mẫu: đường thường; bật cờ biểu mẫu không đổi chuỗi gửi model (định tuyến tắt để client giả chỉ cần một kịch bản)
    history = ((ghep_cau(CAU_BIEU_MAU, TruongInput(so_ngay="2")), ""),)
    sent = {}
    for name, flags in (("form", FORM), ("off", OFF)):
        gen = generator(lambda n, kw: [answer("Đại Nội mở cửa từ 7 giờ [1].")])
        run(deps, "Đại Nội mở cửa mấy giờ?", gen, dataclasses.replace(flags, router=False, tra_web=False), AnswerTrace(history=history), stream)
        sent[name] = gen.client.responses.calls
    assert sent["form"] == sent["off"] and len(sent["form"]) == 1
    assert effort(sent["form"][0]) is None and LICH_TRINH_LUAT not in sent["form"][0]["instructions"]  # lượt thường: không suy luận "low", không luật lịch


def test_form_flag_needs_table_only():
    with pytest.raises(ValueError):
        AssistantFlags(lich_trinh_bieu_mau=True)
    assert FORM.bang_lich is not None and not FORM.lich_trinh and OFF.bang_lich is None


# ---------- route: biểu mẫu, bai_id, Khám phá, thời tiết, cờ ----------

@pytest.fixture(scope="module")
def app_client():
    app = create_app()
    with TestClient(app) as client:
        yield app, client


def _with(app, flags, gen=None):
    original = app.state.assistant_flags, app.state.generator, app.state.generator_ready
    app.state.assistant_flags = flags
    if gen is not None:
        app.state.generator, app.state.generator_ready = gen, True
    return original


def _restore(app, original):
    app.state.assistant_flags, app.state.generator, app.state.generator_ready = original


def test_route_form_off_404_and_needs_day_count(app_client):
    app, client = app_client
    original = _with(app, OFF)
    try:
        off = client.post("/api/chat", json={"query": "x", "bieu_mau": True, "truong": {"so_ngay": "2"}})
        off_stream = client.post("/api/chat/stream", json={"query": "x", "bieu_mau": True, "truong": {"so_ngay": "2"}})
        _with(app, FORM)
        no_days = client.post("/api/chat", json={"query": "x", "bieu_mau": True, "truong": {"di_cung": "cap_doi"}})
        no_truong = client.post("/api/chat", json={"query": "x", "bieu_mau": True})
    finally:
        _restore(app, original)
    assert off.status_code == 404 and off_stream.status_code == 404 and off.json()["error"]["code"] == "not_found"
    assert no_days.status_code == 422 and no_truong.status_code == 422


@pytest.mark.parametrize("path", ["/api/chat", "/api/chat/stream"])
def test_route_form_turn_ignores_typed_text_and_sends_bai_id(app_client, caplog, path):
    app, client = app_client
    gen = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
    original = _with(app, FORM, gen)
    typed = "chữ tự do lạ không được tới model"
    try:
        with chat_log_records(caplog) as records:
            r = client.post(path, json={"query": typed, "bieu_mau": True, "truong": {"so_ngay": "1", "so_thich": "di_tich"}})
    finally:
        _restore(app, original)
    (sent,) = gen.client.responses.calls
    assert typed not in chu_gui(sent) and CAU_BIEU_MAU in chu_gui(sent)
    if path == "/api/chat":
        body = r.json()
        answer_text, sources, lich = body["answer"], body["sources"], body["lich_trinh"]
    else:
        events = parse_sse([f"{block}\n\n".encode() for block in r.text.strip("\n").split("\n\n")])
        answer_text = "".join(d["text"] for kind, d in events if kind == "delta")
        sources = next(d for kind, d in events if kind == "sources")
        lich = next(d for kind, d in events if kind == "lich_trinh")
        assert "routing" not in [d["stage"] for kind, d in events if kind == "status"]
    assert r.status_code == 200 and answer_text.startswith("Mình hiểu: 1 ngày") and lich["ban_do"]
    assert sources and all(s["bai_id"] in app.state.kham_pha for s in sources)
    (line,) = metric_lines(records)
    assert line["outcome"] == "success" and line["lich_trinh_ok"] is True and line["route"] == "tro_ly_hue"
    assert typed not in json.dumps(line, ensure_ascii=False)


def test_source_bai_id_only_for_corpus_articles():
    kho = PackedSource(id=1, title="t", heading_path=(), excerpts=(), source="foods/x.md")
    web = PackedSource(id=2, title="t", heading_path=(), excerpts=(), source="open-meteo")
    assert [s.bai_id for s in _source_responses((kho, web), {"foods/x.md": {}})] == ["foods/x.md", None]
    assert [s.bai_id for s in _source_responses((kho,))] == [None]  # mặc định cũ (không tập bài) ⇒ null


def test_explore_lists_exactly_the_build_record_sources(app_client):
    _, client = app_client
    record = set(json.loads(BUILD_RECORD.read_text(encoding="utf-8"))["corpus"]["sources"])
    bai = client.get("/api/kham_pha").json()["bai"]
    # Q-K: đủ mọi bài của build record, 0 bài ngoài danh sách (không ghi cứng số bài — kho đổi theo mỗi lần ghi kho)
    assert len(bai) == len(record) and {b["id"] for b in bai} == record
    assert {b["linh_vuc"] for b in bai} == {"foods", "heritages", "festivals", "performing_arts", "travel"}
    assert all(b["tieu_de"] and len(b["tom_tat"]) <= 201 and "markdown" not in b for b in bai)
    assert all(b["loai_con"] == (b["id"].split("/")[1] if b["id"].count("/") == 2 else None) for b in bai)


def test_explore_article_only_by_exact_id(app_client):
    app, client = app_client
    some = next(iter(app.state.kham_pha))
    ok = client.get("/api/kham_pha/bai", params={"id": some})
    assert ok.status_code == 200 and ok.json()["markdown"].startswith("# ") and ok.json()["id"] == some
    for bad in ["../.env", f"{some}/..", f"./{some}", f"/{some}", "evaluation/golden_full_corpus.jsonl", "foods/x_sealed.md",
                "foods/khong_co_bai_nay.md", some.upper(), ""]:
        r = client.get("/api/kham_pha/bai", params={"id": bad})
        assert r.status_code in (404, 422) and "markdown" not in r.text, bad
    assert client.get("/api/kham_pha/bai").status_code == 422


def test_weather_and_feature_routes(app_client):
    app, client = app_client
    original = _with(app, dataclasses.replace(OFF, thoi_tiet=False))  # cờ tắt đặt rõ: settings.yaml bật thoi_tiet + biểu mẫu từ 07/11
    # `anh` của /api/tinh_nang đọc `app.state.anh`, chỉ có khi có khoá OpenAI + `anh.bat` (bật 08/11) ⇒ đặt rõ "tắt", không phụ thuộc settings / --env-file
    anh_goc, app.state.anh = app.state.anh, None
    try:
        off = client.get("/api/thoi_tiet")
        features_off = client.get("/api/tinh_nang").json()
        _with(app, dataclasses.replace(OFF, thoi_tiet=True, du_bao=nguon()))
        ok = client.get("/api/thoi_tiet").json()
        features_on = client.get("/api/tinh_nang").json()
        _with(app, dataclasses.replace(OFF, thoi_tiet=True, du_bao=nguon(status=500)))
        loi = client.get("/api/thoi_tiet").json()
        _with(app, FORM)
        features_form = client.get("/api/tinh_nang").json()
    finally:
        _restore(app, original)
        app.state.anh = anh_goc
    assert off.status_code == 404
    assert ok == {"trang_thai": "ok", "hom_nay": {"tmax": 30, "tmin": 23, "xs_mua": 20}, "cap_nhat": "09:15 06/11",
                  "ghi_cong": "Dữ liệu thời tiết: Open-Meteo.com (CC BY 4.0)"}
    assert loi == {"trang_thai": "loi"}  # lỗi ⇒ không số
    assert features_off == {"lich_trinh_bieu_mau": False, "thoi_tiet": False, "anh": False, "tra_web": True, "ban_do_lich": False}
    assert features_on["thoi_tiet"] is True and features_form["lich_trinh_bieu_mau"] is True


def test_report_wrong_info_logs_only_known_article_id(app_client, caplog):
    """Việc nhỏ 8: nút "Báo thông tin chưa đúng" — chỉ nhận `bai_id` có trong danh sách Khám phá; log một dòng chỉ có `bai_id`."""
    app, client = app_client
    some = next(iter(app.state.kham_pha))
    with chat_log_records(caplog) as records:
        ok = client.post("/api/bao_sai", json={"bai_id": some})
        bad = [client.post("/api/bao_sai", json=body) for body in (
            {"bai_id": "../.env"}, {"bai_id": "foods/khong_co.md"}, {"bai_id": some.upper()}, {"bai_id": ""}, {},
            {"bai_id": some, "ghi_chu": "chữ tự do"}, {"bai_id": "x" * 301})]
    assert ok.status_code == 200 and ok.json() == {"ok": True}
    assert [r.status_code for r in bad] == [404, 404, 404, 422, 422, 422, 422]
    lines = [json.loads(r.getMessage().removeprefix("chat_bao_sai ")) for r in records if r.getMessage().startswith("chat_bao_sai ")]
    assert lines == [{"bai_id": some}]


def test_card_summary_skips_label_bullets():
    """Việc nhỏ 3: thẻ Khám phá lấy đoạn văn xuôi đầu, không lấy mục "Thông tin chung" dạng "- **Tên chính thức:** …"."""
    from api.routes.cong import _tom_tat
    md = "# Chùa X\n\n## Thông tin chung\n\n- **Tên chính thức:** Chùa X\n- **Loại:** chùa\n\n## Tổng quan\n\n> Chùa X là một **ngôi chùa** cổ.\n"
    assert _tom_tat(md) == "Chùa X là một ngôi chùa cổ."
    assert _tom_tat("# X\n\n- **Tên:** X\n- Mục hai\n") == "Tên: X Mục hai"  # bài chỉ có danh sách ⇒ như trước
