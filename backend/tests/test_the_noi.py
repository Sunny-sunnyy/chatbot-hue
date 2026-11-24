"""Công tắc `the_noi` (việc X10, 22/11/2026). Vì sao: ở tin nhiều ý model ghi "Tư liệu chưa có thông tin về giờ mở cửa / địa chỉ / giá vé…" cho nơi mà kho
CÓ — tên nơi tới ngữ cảnh từ một nguồn chỉ liệt kê, thuộc tính nằm ở bài riêng không ai tra (tin gia đình 4 ý: 8 / 9 câu trả lời có dòng sai; tin nhiều ý
khác: 11 / 46 lượt). Hàm thuần chạy trên ngữ cảnh đã ghi của 54 lượt: 34 / 34 cặp sai loại giờ / địa chỉ / vé có đúng dòng trong thẻ; Đàn Xã Tắc (bài
không ghi giờ, vé) không ra thẻ ⇒ dòng "chưa có" đúng còn nguyên. 0 USD: tìm kho thật, model theo kịch bản; tên nơi trong phần hàm thuần là tên bịa."""
import asyncio
import dataclasses
import json
import re
import time

import pytest

from core import so_vet
from core.settings_loader import load_settings
from ingestion.source_state import discover_full_corpus_files
from llm import liet_ke as lk
from llm import the_noi as thn
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream_parallel
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_b2_tool_loop import _tool_outputs, answer, deps, generator, run_turn, tool_call  # noqa: F401  (`deps` = fixture tìm kho thật)

# ---------- hàm thuần, kho bịa ----------
KHO_BIA = tuple(lk.bai_tu_markdown(rel, md) for rel, md in (
    ("heritages/heritage/dinh gio bac.md", "# Dinh Gió Bấc\n\n- **Địa chỉ:** 1 đường Thử\n- Giờ mở cửa: 08h00 – 16h00\n- Mở cửa đón khách từ năm 2020.\n"),
    ("foods/restaurants/quan may.md", "# Quán Mây\n\nĐịa chỉ: 2 đường Thử\nGiờ hoạt động: 6h - 9h\n"),
    ("heritages/heritage/dan khong gio.md", "# Đàn Không Giờ\n\nMột nền đất cổ, bài không ghi giờ hay vé.\n"),
    ("heritages/heritage/lang thu.md", "# Lăng Thử\n\nBài chỉ kể chuyện xây lăng.\n"),
    ("travel/places/thac thu.md", "# Thác Thử\n\nĐịa chỉ: 3 đường Thử\n\nKhu thác tạm ngừng đón khách khi có lũ.\n"),
    ("foods/restaurants/thac thu quan.md", "# Thác Thử Quán\n\nĐịa chỉ: 4 đường Thử\n"),
    ("foods/local_specialties/che thu.md", "# Chè Thử\n\nĐịa chỉ: món ăn, không phải một nơi\n"),
    (thn.BAI_VE_LE, "# Vé thử\n\n| STT | Tên điểm | Nơi | Giá người lớn | Giá trẻ em |\n| :---: | :--- | :--- | :---: | :---: |\n"
                    "| 1 | Dinh Gió Bấc *(tên chữ)* | Huế | 10.000 | Miễn phí |\n| 2 | Lăng vua Thử | Huế | 20.000 | 5.000 |\n"),
))
BANG_BIA = thn.dung_bang(KHO_BIA)
HANG_DINH, HANG_LANG = "| 1 | Dinh Gió Bấc *(tên chữ)* | Huế | 10.000 | Miễn phí |", "| 2 | Lăng vua Thử | Huế | 20.000 | 5.000 |"


def test_table_copies_only_label_lines_of_place_articles_and_matches_ticket_rows_by_name():
    theo_ten = {n.ten: n for n in BANG_BIA.noi}
    assert set(theo_ten) == {"Dinh Gió Bấc", "Quán Mây", "Lăng Thử", "Thác Thử", "Thác Thử Quán"}                      # bài không có dòng nào để chép và bài không phải một nơi: không vào bảng
    assert theo_ten["Dinh Gió Bấc"].dong == ("Địa chỉ: 1 đường Thử", "Giờ mở cửa: 08h00 – 16h00")  # dòng "Mở cửa đón khách…" (nhãn không đứng đầu) không được chép
    assert theo_ten["Dinh Gió Bấc"].ve == HANG_DINH and theo_ten["Quán Mây"].ve is None
    assert theo_ten["Lăng Thử"].dong == () and theo_ten["Lăng Thử"].ve == HANG_LANG       # ô tên "Lăng vua X" khớp bài "Lăng X"
    assert BANG_BIA.ve_rel == thn.BAI_VE_LE and BANG_BIA.ve_dau.startswith("| STT | Tên điểm")
    assert thn.dung_bang(KHO_BIA[:2]).ve_dau == "" and len(thn.dung_bang(KHO_BIA[:2]).noi) == 2  # kho không có bài vé ⇒ vẫn có thẻ địa chỉ / giờ


@pytest.mark.parametrize("ngu_canh, mong", [
    ("Gợi ý: Dinh Gió Bấc, Quán Mây.", ["Dinh Gió Bấc", "Quán Mây"]),
    ("gợi ý: dinh gió bấc và QUÁN MÂY", []),                    # khác hoa thường ⇒ không khớp
    ("Quán Mâyy và Dinh Gió Bấcc", []),                         # khúc của một chữ dài hơn ⇒ không khớp
    ("Đàn Không Giờ nằm gần Chè Thử", []),                      # nơi bài không ghi gì / bài không phải một nơi ⇒ không có thẻ
    ("Trưa ghé Thác Thử Quán.", ["Thác Thử Quán"]),             # tên một nơi nằm trong tên bài KHÁC dài hơn ⇒ nhắc quán không phải nhắc thác
    ("Thác Thử Quán nằm cách Thác Thử 2 km.", ["Thác Thử", "Thác Thử Quán"]),
])
def test_a_place_gets_a_card_only_when_its_exact_name_is_in_the_context(ngu_canh, mong):
    noi, _ = thn.the_moi(BANG_BIA, ngu_canh, frozenset(), thn.TRAN_THE)
    assert [n.ten for n in noi] == mong


def test_no_card_for_an_article_already_in_the_sources_and_the_cap_and_ticket_rows():
    ca = "Dinh Gió Bấc, Quán Mây, Lăng Thử"
    noi, ve = thn.the_moi(BANG_BIA, ca, frozenset(), thn.TRAN_THE)
    assert [n.ten for n in noi] == ["Dinh Gió Bấc", "Quán Mây", "Lăng Thử"] and ve == (HANG_DINH, HANG_LANG)  # theo thứ tự của bảng
    noi, ve = thn.the_moi(BANG_BIA, ca, frozenset({"heritages/heritage/dinh gio bac.md"}), thn.TRAN_THE)  # bài riêng đã có nguồn (đoạn thật hoặc thẻ lần trước)
    assert [n.ten for n in noi] == ["Quán Mây", "Lăng Thử"] and ve == (HANG_LANG,)
    assert [n.ten for n in thn.the_moi(BANG_BIA, ca, frozenset(), 1)[0]] == ["Dinh Gió Bấc"] and thn.the_moi(BANG_BIA, ca, frozenset(), 0) == ((), ())
    noi, ve = thn.the_moi(BANG_BIA, f"{ca}\n{HANG_LANG}", frozenset(), thn.TRAN_THE)  # hàng vé đã ở ngữ cảnh ⇒ không chép lại; nơi chỉ có hàng vé ⇒ hết thứ để gắn
    assert [n.ten for n in noi] == ["Dinh Gió Bấc", "Quán Mây"] and ve == (HANG_DINH,)


def test_answer_citing_a_card_still_gets_the_safety_line_of_the_whole_article():
    """Thẻ chỉ chép dòng địa chỉ / giờ; câu "tạm ngừng khi có lũ" nằm ở dòng khác của bài ⇒ phần nối ghi chú phải soi cả bài của thẻ."""
    from llm.assistant import set_notice
    from retrieval.full_corpus_context import PackedSource
    thac = next(n for n in BANG_BIA.noi if n.ten == "Thác Thử")
    the = PackedSource(id=1, title=thac.ten, heading_path=(thn.MUC_THE,), excerpts=thac.dong, source=thac.rel)
    flags = AssistantFlags(noi_dong_tam_ngung=True, may_have_changed_notice=True)
    co = AnswerTrace(answer="Thác Thử ở số 3 đường Thử [1].", cited=(the,), muc_luc_bai={1: (thac.bai,)})
    set_notice(co, flags)
    assert "tạm ngừng đón khách khi có lũ" in co.notice
    khong_neu_ten = AnswerTrace(answer="Nơi đó ở số 3 đường Thử [1].", cited=(the,), muc_luc_bai={1: (thac.bai,)})  # cùng luật với công cụ liệt kê: bài chỉ được soi khi câu trả lời nêu tên nơi
    set_notice(khong_neu_ten, flags)
    assert "tạm ngừng" not in (khong_neu_ten.notice or "")


# ---------- qua lõi trợ lý: tìm kho thật, model theo kịch bản ----------
NHIEU_Y_HEP = "Huế có món gì ngon, ăn ở đâu?"                                   # hai vế hỏi + chữ hỏi hẹp ("ở đâu") ⇒ thuộc cổng
NHIEU_Y_VE = "Điểm nào ít phải leo bậc, giá vé bao nhiêu, giờ mở cửa thế nào?"  # kéo về đoạn chỉ liệt kê tên các điểm ít bậc
KHONG_THUOC_CONG = ("Huế có món gì ngon?", "Giờ mở cửa Đại Nội?", "Lăng nào đẹp nhất, đi mất bao lâu?")  # một ý · một ý có chữ hỏi hẹp · nhiều ý không có chữ hỏi hẹp
CAU_TIM = "quán bún bò ngon ở Huế"
TAT = AssistantFlags(tim_them=True, cau_nhieu_y=True)
_NHAN_DAU_DONG = re.compile(r"^(địa chỉ|khu vực|giờ (mở cửa|hoạt động))", re.I)


@pytest.fixture(scope="module")
def mo():
    settings = load_settings(validate_private_paths=False)
    return dataclasses.replace(TAT, the_noi=True, the_noi_bang=thn.dung_bang(lk.nap_muc_luc(*discover_full_corpus_files(settings))))


def _the(trace):
    return [s for s in trace.so_nguon if s.heading_path == (thn.MUC_THE,)]


def _ma_the(kwargs) -> int | None:
    """Mã nguồn của thẻ nơi CUỐI trong chuỗi gửi model (kịch bản dùng để trích đúng một thẻ)."""
    ma = re.findall(rf"\[Nguồn (\d+)\]\\nTiêu đề: [^\\]+\\nMục: {re.escape(thn.MUC_THE)}", json.dumps(kwargs["input"], ensure_ascii=False))
    return int(ma[-1]) if ma else None


def _gui(gen) -> list:
    """Thứ model nhận trong một lượt: chuỗi của lời gọi đầu + kết quả công cụ của các lời gọi sau (mã lời gọi công cụ do kịch bản sinh mỗi lần một khác ⇒
    không so nguyên `input`)."""
    goi = gen.client.responses.calls
    return [goi[0]["input"]] + [_tool_outputs(c) for c in goi[1:]]


def _tim_roi_trich_the(n, kw):
    """Lời gọi 1: model tìm kho một lần; lời gọi 2: trả lời, trích thẻ nơi cuối nó nhận được (không có thẻ ⇒ trích nguồn 1)."""
    return [tool_call(CAU_TIM)] if n == 1 else [answer(f"Quán mở buổi sáng [{_ma_the(kw) or 1}].")]


def test_multi_part_turn_with_a_narrow_question_gets_cards_after_the_first_search_and_after_the_model_search(deps, mo):
    gen = generator(_tim_roi_trich_the)
    trace = run_turn(deps, NHIEU_Y_HEP, gen, mo)
    goi = gen.client.responses.calls
    the, bang = _the(trace), {n.ten: n for n in mo.the_noi_bang.noi}
    assert trace.nhieu_y and the and trace.the_noi == [s.title for s in the]
    assert [s.id for s in trace.so_nguon] == list(range(1, len(trace.so_nguon) + 1))
    for s in the:
        assert s.source == bang[s.title].rel and s.excerpts == bang[s.title].dong and all(_NHAN_DAU_DONG.match(d) for d in s.excerpts)  # mã nguồn của CHÍNH bài, dòng chép nguyên
        assert [x.source for x in trace.so_nguon].count(s.source) == 1                           # bài riêng không có đoạn nào khác trong sổ nguồn; không thẻ thứ hai
        truoc = "\n\n".join(p for p in trace.context_parts if f"[Nguồn {s.id}]\n" not in p and int(re.search(r"\[Nguồn (\d+)\]", p).group(1)) < s.id)
        assert s.title in truoc                                                                  # tên nơi đã ở ngữ cảnh TRƯỚC khi thẻ được gắn
    dau, sau = json.dumps(goi[0]["input"], ensure_ascii=False), _tool_outputs(goi[1])[-1]
    assert f"Mục: {thn.MUC_THE}" in dau and f"Mục: {thn.MUC_THE}" in sau and sau.index("Mục: " + thn.MUC_THE) > sau.index("[Nguồn ")  # lần của code lẫn của model; thẻ nối SAU kết quả tìm
    assert trace.citation_error is None and trace.cited[0].heading_path == (thn.MUC_THE,) and trace.cited[0].source == bang[trace.cited[0].title].rel  # phép kiểm trích nguồn nhận thẻ
    assert so_vet.ban_ghi("chat", {}, trace)["the_noi"] == trace.the_noi
    assert all(trace.muc_luc_bai[s.id][0].rel == s.source for s in the)  # bài của thẻ đi theo mã nguồn thẻ (phần nối câu an toàn)

    tat = run_turn(deps, NHIEU_Y_HEP, generator(_tim_roi_trich_the), TAT)
    assert not _the(tat) and tat.the_noi == []
    assert [v["vao_ngu_canh"] for v in trace.vet["tim"]] == [v["vao_ngu_canh"] for v in tat.vet["tim"]]  # thẻ không đẩy đoạn kho nào ra khỏi ngữ cảnh


def test_ticket_rows_go_into_one_source_of_the_ticket_article(deps, mo):
    trace = run_turn(deps, NHIEU_Y_VE, generator(lambda n, kw: [answer(INSUFFICIENT_ANSWER)]), mo)
    ve = [s for s in trace.so_nguon if s.heading_path == (thn.MUC_VE,)]
    assert len(ve) == 1 and ve[0].source == thn.BAI_VE_LE and ve[0].excerpts[0] == mo.the_noi_bang.ve_dau
    co_ve = {n.ten for n in mo.the_noi_bang.noi if n.ve in ve[0].excerpts[1:]}
    assert "Cung An Định" in co_ve and co_ve <= set(trace.the_noi) and len(ve[0].excerpts) == 1 + len(co_ve)  # hàng của đúng các nơi được gắn thẻ


@pytest.mark.parametrize("cau", KHONG_THUOC_CONG)
def test_turns_outside_the_gate_send_the_model_the_same_bytes(deps, mo, cau):
    a, b = generator(_tim_roi_trich_the), generator(_tim_roi_trich_the)
    tat, bat = run_turn(deps, cau, a, TAT), run_turn(deps, cau, b, mo)
    assert _gui(a) == _gui(b) and len(_gui(a)) == 2
    assert bat.the_noi == [] and bat.so_nguon == tat.so_nguon and bat.answer == tat.answer


def test_switch_off_or_no_table_does_nothing(deps, mo):
    assert AssistantFlags().the_noi is False  # mặc định của code là tắt; giá trị trong settings.yaml thật không khoá ở test (công tắc mở 22/11/2026)
    goc = generator(_tim_roi_trich_the)
    run_turn(deps, NHIEU_Y_HEP, goc, TAT)
    for flags in (dataclasses.replace(mo, the_noi=False), dataclasses.replace(TAT, the_noi=True)):  # tắt dù có bảng · mở mà không có bảng (im lặng, không lỗi)
        gen = generator(_tim_roi_trich_the)
        trace = run_turn(deps, NHIEU_Y_HEP, gen, flags)
        assert _gui(gen) == _gui(goc) and trace.the_noi == []


def test_settings_switch_loads_the_table_without_turning_the_listing_tool_on():
    settings = load_settings(validate_private_paths=False)
    settings["assistant"] = {**settings["assistant"], "the_noi": True, "liet_ke_bai": False, "ho_so_chu_de": False}  # hồ sơ theo chủ đề cần mục lục của `liet_ke_bai` ⇒ tắt theo
    flags = AssistantFlags.from_settings(settings)
    assert flags.the_noi and len(flags.the_noi_bang.noi) > 100 and flags.muc_luc is None


def test_the_rewrite_after_the_search_budget_carries_the_cards(deps, mo):
    """Lưới `het_luot_viet_lai`: lần viết lại không công cụ nhận cả ngữ cảnh đã gom — thẻ nằm trong đó, số nguồn giữ nguyên."""
    flags = dataclasses.replace(mo, het_luot_viet_lai=True)
    gen = generator(lambda n, kw: [tool_call(f"{CAU_TIM} {n}")] if n <= 2 else [answer("placeholder" if n == 3 else f"Quán mở buổi sáng [{_ma_the(kw)}].")])
    trace = run_turn(deps, NHIEU_Y_HEP, gen, flags)
    viet_lai = gen.client.responses.calls[3]
    chu = json.dumps(viet_lai["input"], ensure_ascii=False)
    assert not viet_lai.get("tools") and all(f"[Nguồn {s.id}]\\nTiêu đề: {s.title}\\nMục: {thn.MUC_THE}" in chu for s in _the(trace))
    assert trace.citation_error is None and trace.cited[0].heading_path == (thn.MUC_THE,)


@pytest.mark.parametrize("parallel", [False, True])
def test_through_the_route_events_with_the_router_running_in_parallel(deps, mo, parallel):
    """Đúng đường người dùng đi: định tuyến (song song khi `parallel`) ⇒ lõi stream ⇒ sự kiện gửi trình duyệt; nguồn người dùng bấm là bài của nơi đó."""
    from api.routes.chat import STREAM_METRIC_FIELDS, _answer_events
    from test_chat_stream import parse_sse

    dem = []

    def script(n, kw):
        if "ngoai_pham_vi" in (kw.get("instructions") or ""):  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        dem.append(n)
        return _tim_roi_trich_the(len(dem), kw)

    flags = dataclasses.replace(mo, router=True, song_song_tra_loi=parallel)
    trace, metrics = AnswerTrace(), dict.fromkeys(STREAM_METRIC_FIELDS)
    bai_ids = frozenset(n.rel for n in mo.the_noi_bang.noi)

    async def go():
        turn = answer_turn_stream_parallel(NHIEU_Y_HEP, *deps, generator(script), trace, flags, None, None)
        return parse_sse([e async for e in _answer_events(turn, trace, metrics, time.perf_counter(), bai_ids=bai_ids)])
    events = asyncio.run(go())
    ten = [k for k, _ in events]
    assert "error" not in ten and ten[-1] == "done" and metrics["outcome"] == "success" and trace.the_noi
    nguon = next(d for k, d in events if k == "sources")
    assert len(nguon) == 1 and nguon[0]["title"] in trace.the_noi and nguon[0]["bai_id"] == trace.cited[0].source
