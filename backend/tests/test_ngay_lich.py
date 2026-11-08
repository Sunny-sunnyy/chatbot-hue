"""Phase 9 T1 — ngày + âm lịch Việt Nam (`llm/ngay_lich.py`). Logic thuần, 0 USD, không mạng.

Đáp án công khai (E kiểm 08/11/2026): Tết các năm — bảng "Ngày đầu năm theo Con giáp" của vi.wikipedia "Tết Nguyên đán" (tính theo giờ Hà Nội UTC+7; bảng
không ghi nguồn) · Tết 2007 VN 17/02 ↔ TQ 18/02 — Tuổi Trẻ 16/07/2006 "Vì sao lịch VN và Trung Quốc lệch nhau" · Tết 1985 VN 21/01 ↔ TQ 20/02 — spec Phase 9
§12.5 (en.wikipedia "Vietnamese calendar", C kiểm). `lunar-vn` khớp bảng tính sẵn của Hồ Ngọc Đức mọi năm 1966–2099 (`data/phase_9/t1/tools/so_tet.py`).
"""
import datetime as dt

import pytest
from lunar_vn import LunarDate, lunar_to_solar

from llm import ngay_lich as nl

TET = {1985: "21/01/1985", 2007: "17/02/2007", 2020: "25/01/2020", 2021: "12/02/2021", 2022: "01/02/2022", 2023: "22/01/2023",
       2024: "10/02/2024", 2025: "29/01/2025", 2026: "17/02/2026", 2027: "06/02/2027", 2030: "02/02/2030"}


@pytest.mark.parametrize("nam, ngay", TET.items())
def test_tet_matches_public_dates(nam, ngay):
    chu = nl.doi(1, 1, nam, "am")
    assert f"{ngay} dương lịch — ngày 1 tháng Giêng âm lịch" in chu


@pytest.mark.parametrize("nam, viet_nam, trung_quoc", [(1985, dt.date(1985, 1, 21), dt.date(1985, 2, 20)),
                                                       (2007, dt.date(2007, 2, 17), dt.date(2007, 2, 18))])
def test_vietnam_utc7_differs_from_china_utc8(nam, viet_nam, trung_quoc):
    # lý do chọn lịch UTC+7: cùng thuật toán ở UTC+8 ra đúng ngày Tết của Trung Quốc ⇒ thư viện lịch Trung Quốc sẽ sai ở các năm này
    assert lunar_to_solar(LunarDate(1, 1, nam)) == viet_nam
    assert lunar_to_solar(LunarDate(1, 1, nam), time_zone=8.0) == trung_quoc
    assert nl.doi(1, 1, nam, "am").split(" dương")[0].endswith(viet_nam.strftime("%d/%m/%Y"))


def test_round_trip_every_day_in_range():
    d, het = dt.date(nl.NAM_MIN, 1, 1), dt.date(nl.NAM_MAX, 12, 31)
    while d <= het:
        am = nl.solar_to_lunar(d)
        if nl.NAM_MIN <= am.year <= nl.NAM_MAX:
            assert nl.doi(am.day, am.month, am.year, "am", am.leap) == nl.mo_ta(d)
        d += dt.timedelta(days=1)


def test_weekday_and_can_chi_text():
    assert nl.mo_ta(dt.date(2026, 2, 17)) == "Thứ Ba, 17/02/2026 dương lịch — ngày 1 tháng Giêng âm lịch, năm Bính Ngọ"
    assert nl.mo_ta(dt.date(2026, 2, 16)).endswith("ngày 29 tháng Chạp âm lịch, năm Ất Tỵ")  # can chi theo NĂM ÂM, không theo năm dương


@pytest.mark.parametrize("args", [(30, 12, 2025, "am"),            # tháng Chạp Ất Tỵ chỉ 29 ngày (thư viện lặng lẽ ra ngày đầu tháng sau — code bắt)
                                  (1, 6, 2026, "am", True),         # 2026 không có tháng nhuận
                                  (31, 4, 2026, "duong"), (29, 2, 2027, "duong"), (0, 1, 2026, "am"), (1, 13, 2026, "am"),
                                  (1, 1, 2026, "duong", True),
                                  (10 ** 20, 1, 2026, "duong"), (1, 10 ** 20, 2026, "am")])  # review nhánh m-1: số vô lý ⇒ câu cố định, không OverflowError
def test_impossible_dates_get_fixed_sentence(args):
    assert nl.doi(*args) == nl.CAU_NGAY_SAI


def test_leap_month_is_named():
    assert nl.doi(1, 6, 2025, "am", True) == "Thứ Sáu, 25/07/2025 dương lịch — ngày 1 tháng 6 (nhuận) âm lịch, năm Ất Tỵ"


@pytest.mark.parametrize("nam", [1968, 1975, 2101, 1])
def test_years_outside_range_get_fixed_sentence(nam):
    # trước 1976 hai miền khác lịch (Tết Mậu Thân 1968: Bắc 29/01, Nam — có Huế — 30/01) ⇒ không đoán
    assert nl.doi(1, 1, nam, "am") == nl.CAU_NGOAI_KHOANG
    assert nl.doi(1, 1, nam, "duong") == nl.CAU_NGOAI_KHOANG


def test_today_uses_vietnam_time_not_server_time():
    # 17:30 UTC 07/11 = 00:30 08/11 giờ Việt Nam
    assert nl.hom_nay(dt.datetime(2026, 11, 7, 17, 30, tzinfo=dt.timezone.utc)) == dt.date(2026, 11, 8)
    assert nl.hom_nay(dt.datetime(2026, 11, 7, 16, 59, tzinfo=dt.timezone.utc)) == dt.date(2026, 11, 7)


# ---------- Nối vào trợ lý (review plan M-2, m-1 / WORKFLOW §4c): fixture `deps` = Qdrant thật, chỉ đọc; model = client soạn kịch bản ----------
import asyncio  # noqa: E402
import dataclasses  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402

from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream  # noqa: E402
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: E402,F401
from test_b5_lich_trinh import tool_names  # noqa: E402

TAT = AssistantFlags(tim_them=True)
BAT = dataclasses.replace(TAT, ngay_lich=True)


def ngay_call(loai="am", ngay=1, thang=1, nam=0, thang_nhuan=False) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "ngay_lich",
            "arguments": json.dumps({"loai": loai, "ngay": ngay, "thang": thang, "nam": nam, "thang_nhuan": thang_nhuan}), "status": "completed"}


def chay(deps, cau, gen, flags, history=(), stream=False):
    trace = AnswerTrace(history=list(history))

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(cau, *deps, gen, trace, flags)]
        await answer_turn(cau, *deps, gen, trace, flags)

    return trace, asyncio.run(go())


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("cau, history, flags, co_cong_cu", [
    ("Rằm tháng Giêng năm nay là ngày nào dương lịch?", (), BAT, True),                                 # lượt đầu có từ chỉ ngày
    ("Đại Nội rộng bao nhiêu?", (), BAT, False),                                                    # không từ chỉ ngày ⇒ như cũ
    ("Còn chùa Thiên Mụ thì sao?", (("Tối nay Đại Nội có mở cửa không?", "…"),), BAT, True),       # lượt có lịch sử: câu hỏi liền trước có từ chỉ ngày
    ("Rằm tháng Giêng năm nay là ngày nào dương lịch?", (), TAT, False),                             # cờ tắt ⇒ như cũ
])
def test_date_tool_offered_only_with_date_words(deps, cau, history, flags, co_cong_cu, stream):
    seen = []
    gen = generator(lambda n, kw: (seen.append(tool_names(kw)), [answer("Mình chưa rõ.")])[1])
    chay(deps, cau, gen, flags, history, stream)
    assert seen and all(("ngay_lich" in names) is co_cong_cu and "tim_kho" in names for names in seen)


def test_answer_citing_only_the_date_source_passes_citation_check(deps):
    # M-2: câu chỉ có ngày (không đoạn kho) vẫn qua kiểm citation vì kết quả công cụ là một nguồn trong sổ nguồn
    def kich_ban(n, kw):
        if n == 1:
            return [ngay_call("am", 1, 1, 2027)]
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Lịch hệ thống", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        return [answer(f"Mùng 1 Tết năm 2027 là thứ Bảy, 06/02/2027 dương lịch [{so[-1]}].")]

    trace, _ = chay(deps, "Mùng 1 Tết năm sau là thứ mấy?", generator(kich_ban), BAT)
    assert trace.citation_error is None and trace.cited and trace.cited[-1].title == nl.TIEU_DE_NGUON
    assert "06/02/2027" in trace.so_nguon[-1].excerpts[1]


def test_date_tool_counts_at_most_two_calls(deps):
    gen = generator(lambda n, kw: [ngay_call("am", 15, n, 2026)] if n <= 3 else [answer("Mình chưa rõ.")])
    trace, _ = chay(deps, "Rằm các tháng năm nay là ngày nào?", gen, BAT)
    goi = [t for t in trace.tools if t["name"] == "ngay_lich"]
    assert len(goi) == 3 and goi[2].get("het_luot") and sum(s.title == nl.TIEU_DE_NGUON for s in trace.so_nguon) == 2


@pytest.mark.parametrize("cau, flags, so_vong", [
    ("Rằm tháng Giêng năm nay có lễ hội gì?", BAT, 5),   # có đưa `ngay_lich` ⇒ 4 + 1 (A chọn 08/11: công cụ ngày ăn một vòng — R8 chạm trần ở lượt đo)
    ("Đại Nội có những công trình gì?", BAT, 4),          # không từ chỉ ngày ⇒ giữ B2 D5
    ("Rằm tháng Giêng năm nay có lễ hội gì?", TAT, 4),    # cờ tắt ⇒ như cũ
])
@pytest.mark.parametrize("stream", [False, True])
def test_max_turns_plus_one_only_when_date_tool_offered(deps, cau, flags, so_vong, stream):
    from test_b2_tool_loop import tool_call
    vong = []
    gen = generator(lambda n, kw: (vong.append(n), [tool_call(f"lễ hội {n}")])[1])  # model cứ đòi tìm thêm ⇒ chạm trần
    trace, _ = chay(deps, cau, gen, flags, stream=stream)
    assert len(vong) == so_vong and trace.fixed_outcome == "max_turns"


@pytest.mark.parametrize("ngay, thang, nam, sau", [(18, 6, 2026, "đã qua 100 ngày"), (30, 9, 2026, "là hôm nay"), (1, 1, 2027, "còn 90 ngày nữa")])
def test_result_states_before_after_today_by_code(ngay, thang, nam, sau):
    # A2 lượt đo 08/11: model tự so trước / sau rồi kết luận ngược ⇒ code ghi luôn khoảng cách với hôm nay (08/11/2026 = 30/9 âm Bính Ngọ)
    now = dt.datetime(2026, 11, 8, 9, 0, tzinfo=dt.timezone.utc)
    assert nl.ket_qua("am", ngay, thang, nam, False, now).splitlines()[1].endswith(f"— {sau} (so với hôm nay)")


def test_week_and_month_ranges_written_by_code_only_when_asked():
    # R7 lượt 2 (08/11): model tự suy "tuần này là giữa tháng 9 âm" ⇒ code ghi khoảng ngày (A chọn (i))
    now = dt.datetime(2026, 11, 8, 9, 0, tzinfo=dt.timezone.utc)  # Chủ nhật 08/11/2026 = 30/9 âm
    chu = nl.ket_qua("hom_nay", 0, 0, 0, False, now, cau="Tuần này có lễ gì? Tuần tới thì sao, tháng này nữa?").splitlines()
    assert chu[1] == "Tuần này: từ Thứ Hai, 02/11/2026 (ngày 24 tháng 9 âm) đến Chủ nhật, 08/11/2026 (ngày 30 tháng 9 âm)."
    assert chu[2].startswith("Tuần sau: từ Thứ Hai, 09/11/2026 (ngày 1 tháng 10 âm)")
    assert chu[4] == "Tháng âm hiện tại (tháng 9): từ Thứ Bảy, 10/10/2026 (ngày 1 tháng 9 âm) đến Chủ nhật, 08/11/2026 (ngày 30 tháng 9 âm)."
    assert nl.ket_qua("hom_nay", 0, 0, 0, False, now, cau="Rằm tháng Giêng năm nay?").count("\n") == 0  # không cụm khoảng ⇒ chỉ dòng hôm nay



def _vn(y, m, d, h=10):
    return dt.datetime(y, m, d, h - 7, 0, tzinfo=dt.timezone.utc)


@pytest.mark.parametrize("now, ngay, thang, qua, toi", [
    (_vn(2027, 1, 20), 1, 1, ("17/02/2026", "đã qua 337 ngày"), ("06/02/2027", "còn 17 ngày nữa")),     # giữa 1/1 và Tết: "Tết năm nay" không thành Tết đã qua
    (_vn(2027, 2, 7), 1, 1, ("06/02/2027", "đã qua 1 ngày"), ("26/01/2028", "còn 353 ngày nữa")),      # một ngày sau Tết
    (_vn(2027, 1, 20), 15, 12, ("02/02/2026", "đã qua 352 ngày"), ("22/01/2027", "còn 2 ngày nữa")),   # "rằm tháng Chạp năm nay" trong tháng 1
])
def test_no_year_gives_last_and_next_occurrence(now, ngay, thang, qua, toi):
    # review nhánh M-1 (A chọn 08/11): không nêu năm ⇒ code trả cả lần gần nhất đã qua và lần sắp tới, không đoán "năm nay"
    dong = nl.ket_qua("am", ngay, thang, 0, False, now).splitlines()
    assert "lần gần nhất" in dong[1] and qua[0] in dong[1] and dong[1].endswith(f"{qua[1]} (so với hôm nay)")
    assert "lần sắp tới" in dong[2] and toi[0] in dong[2] and dong[2].endswith(f"{toi[1]} (so với hôm nay)")


@pytest.mark.parametrize("cau, co", [
    ("Hôm nay là thứ hai à?", True), ("Thứ 7 này đi Đại Nội được không?", True), ("Chiều 15/1 có gì?", True),
    ("Ngày 2/9/2026 có miễn vé không?", True), ("Đi vào thứ Bảy được không?", True),
    ("Vua thứ ba triều Nguyễn là ai?", False), ("Lần thứ hai tổ chức là năm nào?", False), ("Mùa thứ hai của lễ hội?", False),
    ("Quán mở 24/7 không?", False), ("Uống 1/2 ly thôi", False), ("Đại Nội rộng bao nhiêu?", False),
])
def test_detector_skips_ordinals_and_fractions(cau, co):
    # review nhánh m-2: "thứ X" sau danh từ thứ tự và phân số "1/2", "24/7" không phải ngày (Golden 176 vẫn bật 9 câu — cả 9 là cụm ngày thật)
    assert nl.co_tu_ngay(cau) is co


def test_stream_turn_calling_date_tool_has_no_search_status_and_passes_citation(deps):
    # review nhánh m-6: đường stream có gọi `ngay_lich` thật — không báo "đang tìm kho" cho công cụ này, câu chỉ trích nguồn ngày qua kiểm citation
    def kich_ban(n, kw):
        if n == 1:
            return [ngay_call("am", 1, 1, 2027)]
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Lịch hệ thống", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        return [answer(f"Mùng 1 Tết năm 2027 là thứ Bảy, 06/02/2027 [{so[-1]}].")]

    trace, events = chay(deps, "Mùng 1 Tết năm sau là thứ mấy?", generator(kich_ban), BAT, stream=True)
    stages = [d["stage"] for k, d in events if k == "status"]
    assert "searching" not in stages and stages.count("searched") == 1  # "searched" duy nhất là lần tìm đầu V0, không phải từ `ngay_lich`
    assert any(t["name"] == "ngay_lich" for t in trace.tools) and trace.citation_error is None


@pytest.mark.parametrize("cau, co_cong_cu", [("Tết năm nay là ngày nào?", True), ("Đại Nội rộng bao nhiêu?", False)])
def test_parallel_path_offers_date_tool_only_with_date_words(deps, cau, co_cong_cu):
    # review nhánh m-6: đường song song #6 (định tuyến chạy cùng phần trả lời) — phần trả lời nhận `ngay_lich` đúng như đường thường
    from llm.assistant import answer_turn_stream_parallel
    from llm.full_corpus_prompt import ROUTER_INSTRUCTIONS
    from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
    from test_toc_do_song_song import Client, TimedResponses

    responses = TimedResponses(route="tro_ly_hue", router_delay=0, answer_delay=0)
    gen = OpenAIFullCorpusGenerator(client=Client(responses), model="probe")
    flags = dataclasses.replace(BAT, router=True, song_song_tra_loi=True)

    async def go():
        return [e async for e in answer_turn_stream_parallel(cau, *deps, gen, AnswerTrace(), flags)]

    asyncio.run(go())
    tra_loi = [c for c in responses.calls if not str(c.get("instructions", "")).startswith(ROUTER_INSTRUCTIONS[:80])]
    assert tra_loi and all(("ngay_lich" in tool_names(c)) is co_cong_cu for c in tra_loi)
