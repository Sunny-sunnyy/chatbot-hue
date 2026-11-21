"""Cờ `su_kien_theo_ngay` (20/11) — bảng lễ hội / hoạt động theo ngày chép từ kho + hàm thuần tra theo khoảng ngày. Không model, không mạng, không Qdrant.
Đây KHÔNG phải bằng chứng trên câu trả lời thật — phần đó là bộ dò độc lập của cổng + một lượt thật cặp tắt ↔ bật."""
import datetime as dt
from pathlib import Path

import pytest

from core.settings_loader import BACKEND_DIR
from llm import su_kien as sk

DUONG_BANG = BACKEND_DIR.parent / "data" / "su_kien_theo_ngay_2026-11-20" / "su_kien_theo_ngay_v2.json"  # bảng private như các bảng lịch (`settings.yaml` `su_kien_bang`)
if not DUONG_BANG.is_file():
    pytest.skip("bản chép không có data/ (bảng sự kiện là dữ liệu private)", allow_module_level=True)
BANG = sk.nap_bang(DUONG_BANG)
KHO = BACKEND_DIR.parent / "knowledge-base-hue"
HOM = dt.date(2026, 11, 20)  # thứ Sáu; ngày 2 tháng 10 âm lịch
NOW = dt.datetime(2026, 11, 20, 9, 0, tzinfo=dt.timezone(dt.timedelta(hours=7)))


@pytest.mark.skipif(not KHO.is_dir(), reason="bản chép không có kho")
def test_every_row_quotes_its_source_article_verbatim():
    """Bảng là bản CHÉP: chuỗi ngày (và ghi chú) của mỗi dòng phải có nguyên văn trong đúng bài nguồn. Kho đổi chữ ⇒ test này đỏ ⇒ sửa bảng."""
    for dong in BANG:
        chu_bai = (KHO / dong["bai"]).read_text(encoding="utf-8")
        assert dong["chu"] in chu_bai, dong["ten"]
        assert dong.get("ghi_chu", "") in chu_bai, dong["ten"]


def _ten(muc):
    return [d["ten"] for d, *_ in muc]


def test_lunar_dates_are_converted_and_found_in_the_asked_window():
    # tháng Giêng âm năm Đinh Mùi: 06/02/2027 – 07/03/2027; mồng 6 = 11/02/2027, 22 tháng Giêng = 27/02/2027
    tu, den, nhan = sk.khoang_hoi("tháng Giêng âm lịch ở Huế có lễ hội gì", HOM)
    assert (tu, den) == (dt.date(2027, 2, 6), dt.date(2027, 3, 7)) and "giêng" in nhan
    kq = sk.tra(BANG, tu, den)
    lan = {d["ten"]: (a, b) for d, a, b in kq["co_dinh"]}
    assert lan["Hội vật làng Thủ Lễ"] == (dt.date(2027, 2, 11), dt.date(2027, 2, 11))
    assert lan["Lễ tế Bà Bún Vân Cù"] == (dt.date(2027, 2, 27), dt.date(2027, 2, 27))
    assert "Tết Nguyên đán ở Huế" in lan and "Lễ hội Quán Thế Âm tại Huế" not in lan
    assert kq["sap_toi"] is None  # có lễ hội trong khoảng ⇒ không nêu "gần nhất"


def test_range_crossing_the_lunar_new_year_is_one_occurrence():
    # "23 tháng Chạp đến mồng 7 tháng Giêng": Tết Đinh Mùi là 06/02/2027, tháng Chạp trước đó 29 ngày (08/01–05/02) ⇒ 23 Chạp = 30/01/2027, mồng 7 = 12/02/2027
    kq = sk.tra(BANG, dt.date(2027, 2, 5), dt.date(2027, 2, 5))
    tet = [(a, b) for d, a, b in kq["co_dinh"] if d["ten"] == "Tết Nguyên đán ở Huế"]
    assert tet == [(dt.date(2027, 1, 30), dt.date(2027, 2, 12))]


def test_empty_window_names_the_nearest_upcoming_fixed_date_festival_and_weekly_activities():
    # cuối tuần 21–22/11/2026 (3–4 tháng 10 âm): không lễ hội ngày cố định nào; gần nhất = 23 tháng Chạp âm (30/01/2027)
    tu, den, _ = sk.khoang_hoi("cuối tuần này ở Huế có sự kiện gì", HOM)
    assert (tu, den) == (dt.date(2026, 11, 21), dt.date(2026, 11, 22))
    kq = sk.tra(BANG, tu, den)
    assert kq["co_dinh"] == [] and kq["uoc"] == []
    dong, a, _ = kq["sap_toi"]
    assert a == dt.date(2027, 1, 30) and dong["ten"] in ("Tết Nguyên đán ở Huế", "Lễ tế Thai Dương phu nhân")
    assert {"Khu phố Tây Huế", "Phố đi bộ Hai Bà Trưng", "Ca Huế trên sông Hương"} <= {d["ten"] for d in kq["tuan"]}


def test_weekly_activity_only_on_its_weekdays():
    thu_ba = sk.tra(BANG, dt.date(2026, 11, 24), dt.date(2026, 11, 24))  # thứ Ba
    assert "Khu phố Tây Huế" not in [d["ten"] for d in thu_ba["tuan"]] and "Ca Huế trên sông Hương" in [d["ten"] for d in thu_ba["tuan"]]


def test_approximate_rows_are_listed_apart_and_never_as_nearest():
    kq = sk.tra(BANG, dt.date(2027, 6, 1), dt.date(2027, 6, 30))  # tháng 6 dương: Sen, Sóng nước chỉ ghi khoảng
    assert {"Ngày hội Sen Huế", "Lễ hội Sóng nước Tam Giang"} <= set(_ten(kq["uoc"]))
    assert all(not d.get("uoc") for d, *_ in kq["co_dinh"])


@pytest.mark.parametrize("cau", [
    "cuối tuần này ở Huế có sự kiện gì",
    "Tối nay Huế có lễ hội gì không?",
    "tuần sau có lễ hội nào ở Huế",
    "tháng 2 ở Huế có lễ hội gì",
    "ngày 27/2 ở Huế có sự kiện gì đặc biệt",
    "cuối tuần này ở Huế có gì không?",               # "có gì không" đứng cuối câu vẫn là hỏi sự kiện
])
def test_gate_opens_only_with_both_a_date_window_and_an_event_word(cau):
    dong = sk.dong_nguon(cau, BANG, NOW)
    assert dong and dong[0].startswith("Khoảng được hỏi") and dong[-1] == sk.CAU_CUOI


@pytest.mark.parametrize("cau", [
    "Huế có những lễ hội nào?",                       # hỏi sự kiện nhưng không nêu khoảng ngày
    "cuối tuần này đi Huế nên ăn gì",                 # có khoảng ngày, không hỏi sự kiện
    "cuối tuần này thời tiết Huế có gì đáng lo không",  # "có gì" về thời tiết
    "Festival Huế tổ chức khi nào",
    "tối nay Đại Nội mở cửa tới mấy giờ, có sự kiện gì không",  # câu hỏi giờ mở cửa: để đường thường
    "lễ hội Cầu ngư năm 2027 rơi vào ngày nào",       # hỏi ngày của MỘT lễ hội: đường "Lịch hệ thống" đang có
    "năm sau Huế có lễ hội gì",                       # khoảng quá dài / không đọc được
    "tháng 3 năm ngoái Huế có lễ hội gì",             # bộ dò mù của E 20/11: hỏi QUÁ KHỨ — không được đưa lịch sắp tới
    "tuần trước ở Huế có sự kiện gì",
    "Ngày mai có gì không ổn với chuyến bay không?",   # review B 20/11: "có gì không ổn / không nên" không phải hỏi sự kiện
    "cuối tuần vừa rồi Huế có lễ hội gì không",
    "",
])
def test_gate_stays_closed_otherwise(cau):
    assert sk.dong_nguon(cau, BANG, NOW) is None


def test_source_lines_carry_the_computed_date_and_the_article_wording():
    dong = sk.dong_nguon("ngày 27/2 ở Huế có lễ hội gì", BANG, NOW)
    bun = [d for d in dong if d.startswith("- Lễ tế Bà Bún Vân Cù")]
    assert bun and "Thứ Bảy 27/02/2027" in bun[0] and "“ngày 22 tháng Giêng Âm lịch”" in bun[0]
    khong = sk.dong_nguon("cuối tuần này ở Huế có sự kiện gì", BANG, NOW)
    assert any("KHÔNG ghi lễ hội nào có ngày cố định" in d for d in khong) and any(d.startswith("Lễ hội có ngày cố định gần nhất") for d in khong)


# ---------- Nối vào trợ lý: nguồn có trong lần gọi model ĐẦU; câu không qua cổng ⇒ chuỗi gửi model y như cờ tắt ----------
import asyncio  # noqa: E402
import dataclasses  # noqa: E402
import json  # noqa: E402

from llm.assistant import AnswerTrace, AssistantFlags, answer_turn  # noqa: E402
from test_b2_tool_loop import answer, deps, generator  # noqa: E402, F401 — `deps`: fixture dựng tìm kho + ngữ cảnh giả

TAT = AssistantFlags(tim_them=True)
BAT = dataclasses.replace(TAT, su_kien_theo_ngay=True, su_kien_bang=BANG)


def _gui_model(deps, cau, flags):
    seen = []
    gen = generator(lambda n, kw: (seen.append(json.dumps(kw, ensure_ascii=False, sort_keys=True, default=lambda o: type(o).__name__)), [answer("Mình chưa rõ.")])[1])
    trace = AnswerTrace()
    asyncio.run(answer_turn(cau, *deps, gen, trace, flags))
    return trace, seen


def test_event_source_reaches_the_first_model_call_only_for_gated_questions(deps):
    trace, seen = _gui_model(deps, "cuối tuần này ở Huế có sự kiện gì", BAT)
    assert sk.TIEU_DE_NGUON in seen[0] and "Khoảng được hỏi (cuối tuần này)" in seen[0]
    assert [t["name"] for t in trace.tools if t["name"] == "su_kien_san"] == ["su_kien_san"]
    assert any(src.source == sk.NGUON_SOURCE for src in trace.so_nguon)
    # đối chứng 1: cùng câu, cờ tắt ⇒ không có nguồn; đối chứng 2: câu không qua cổng, cờ bật ⇒ giống từng ký tự với cờ tắt
    assert sk.TIEU_DE_NGUON not in _gui_model(deps, "cuối tuần này ở Huế có sự kiện gì", TAT)[1][0]
    cau_thuong = "Lăng Tự Đức có gì đáng xem?"
    assert _gui_model(deps, cau_thuong, BAT)[1] == _gui_model(deps, cau_thuong, TAT)[1]


# ---------- 21/11/2026: bộ đọc khoảng ngày — câu có từ hỏi sự kiện trước, khoảng rộng hơn, hai ngày ⇒ từ–đến ----------
THU_BAY = dt.date(2026, 11, 21)


@pytest.mark.parametrize("cau, tu, den", [
    # tin của người dùng mô phỏng (lượt mốc 21/11): con số ngày ở câu đệm từng thắng ⇒ chỉ tra đúng ngày 23/11
    ("ok thứ 2 23/11 nhé. Thế tuần này với tháng này ở Huế có lễ hội hay sự kiện gì không? Mình muốn sắp xếp đi xem luôn", dt.date(2026, 11, 21), dt.date(2026, 11, 30)),
    ("Mình tới Huế ngày 23/11. Tháng 12 có lễ hội gì không?", dt.date(2026, 12, 1), dt.date(2026, 12, 31)),   # ngày ở câu kể, khoảng ở câu hỏi
    ("tuần này với tháng này ở Huế có lễ hội gì không", dt.date(2026, 11, 21), dt.date(2026, 11, 30)),          # hai khoảng ⇒ khoảng rộng hơn
    ("Mình ở Huế từ 23/11 đến 25/11, có sự kiện gì không?", dt.date(2026, 11, 23), dt.date(2026, 11, 25)),      # hai con số ngày ⇒ từ–đến
    ("từ 28/12 đến 2/1 có lễ hội gì", dt.date(2026, 12, 28), dt.date(2027, 1, 2)),                               # vắt qua năm
    ("hôm nay với ngày mai có sự kiện gì", dt.date(2026, 11, 21), dt.date(2026, 11, 22)),                        # hai ngày đơn ⇒ từ–đến
    ("Mình tới ngày 23/11. Ở đó có lễ hội gì không?", dt.date(2026, 11, 23), dt.date(2026, 11, 23)),             # câu hỏi không nêu khoảng ⇒ đọc cả tin như cũ
    ("cuối tuần này ở Huế có sự kiện gì", dt.date(2026, 11, 21), dt.date(2026, 11, 22)),                         # "cuối tuần này" KHÔNG bị nới thành "tuần này"
    ("cuối tuần sau có lễ hội gì", dt.date(2026, 11, 28), dt.date(2026, 11, 29)),                                # … và không thành "tuần sau"
    # câu hỏi sự kiện KHÔNG nêu khoảng ⇒ đọc cả tin theo thứ tự ưu tiên CŨ (ngày ghi số trước), không lấy "khoảng rộng nhất" của cả tin: một tin thật có
    # "rằm tháng 10" ở câu khác từng bị kéo sang cả tháng 10 năm sau khi luật rộng nhất áp cho cả tin
    ("Ok rằm thứ hai 23/11 rồi. Nhưng lễ hội thì chưa thấy gì cụ thể. Thế rằm tháng 10 ở chùa có nghi lễ nào không?", dt.date(2026, 11, 23), dt.date(2026, 11, 23)),
])
def test_range_is_read_from_the_asking_sentence_and_widened_not_narrowed(cau, tu, den):
    assert sk.hoi_su_kien(cau) and sk.khoang_hoi(cau, THU_BAY)[:2] == (tu, den)


def test_impossible_date_and_out_of_range_month_still_give_no_range():
    assert sk.khoang_hoi("ngày 31/2 có lễ hội gì", THU_BAY) is None
    assert sk.khoang_hoi("tháng 13 âm lịch có lễ hội gì", THU_BAY) is None
