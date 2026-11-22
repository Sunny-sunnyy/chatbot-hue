"""Công cụ `gan_diem` — "gần một điểm có gì" (cờ `gan_diem`, 21/11/2026). Phần thuần 0 USD trên bảng dựng tay; phần nối trợ lý dùng fixture `deps` (Qdrant
thật, chỉ đọc) + model là client soạn kịch bản (như `test_khoang_cach.py`). Model thật có GỌI công cụ đúng lúc và viết gì từ kết quả là lượt đo có phí ghi
ở report của nhánh."""
import asyncio
import dataclasses
import json
import re

import pytest

from llm import gan_diem as gd
from llm import khoang_cach as kc
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_b2_tool_loop import _ids, answer, deps, generator, tool_call  # noqa: F401
from test_b5_lich_trinh import tool_names

# Ba điểm: A có quán quanh, B không có quán nào trong 2 km, C có trong bảng tên nhưng không có toạ độ / không có cặp khoảng cách nào
BANG = kc.BangKhoangCach(ten={"a": "Điểm A", "b": "Điểm B", "c": "Điểm C"}, ten_khac={"a": ("Tên khác A",), "b": (), "c": ()},
                         cap={"a|b": {"km": 4.0, "phut": 4}, "b|a": {"km": 4.2, "phut": 5}})
TOA = {"a": (16.4700, 107.5800), "b": (16.3000, 107.9000)}


def _q(ten, loai, lech_m, nguon="kho", muc="chac"):
    """Một quán cách Điểm A `lech_m` mét về phía bắc (1 độ vĩ ≈ 111,2 km)."""
    return {"ten": ten, "loai": loai, "cum": "x", "toa": [TOA["a"][0] + lech_m / 111_195, TOA["a"][1]], "nguon": nguon, "muc_toa_do": muc,
            **({"bai_id": f"foods/{ten}.md"} if nguon == "kho" else {})}


QUAN = {"x": [_q("Quán Gần", "quan_an", 300), _q("Quán Vừa", "quan_an", 1200), _q("Quán Ước", "quan_an", 700, muc="uoc"), _q("Quán Xa", "quan_an", 2600),
              _q("Quán Nguồn Mở", "quan_an", 100, nguon="osm")],
        "y": [_q("Cà Phê Cụm Khác", "ca_phe", 1500)]}


def test_restaurants_only_kb_places_within_two_km_nearest_first():
    dong, n = gd.ket_qua(BANG, QUAN, TOA, "a", "quan_an")
    assert n == 3 and dong[0] == "Quán ăn có bài trong kho quanh Điểm A (gần trước):" and dong[-1] == gd.CAU_GHI_CHU_QUAN
    assert dong[1:4] == ("- Quán Gần: cách Điểm A dưới 0,5 km theo đường chim bay.",
                         "- Quán Ước: cách Điểm A chưa tới 1 km theo đường chim bay.",  # toạ độ mức "ước" ⇒ nấc, không số lẻ
                         "- Quán Vừa: cách Điểm A khoảng 1,2 km theo đường chim bay.")
    chu = " ".join(dong)
    assert "Quán Xa" not in chu and "Quán Nguồn Mở" not in chu  # ngoài 2 km · không có bài kho


def test_cafes_are_found_across_clusters_and_other_kinds_are_not_mixed_in():
    dong, n = gd.ket_qua(BANG, QUAN, TOA, "a", "ca_phe")
    assert n == 1 and dong[1] == "- Cà Phê Cụm Khác: cách Điểm A khoảng 1,5 km theo đường chim bay." and "Quán Gần" not in " ".join(dong)


def test_attractions_come_from_the_distance_table_with_its_numbers():
    dong, n = gd.ket_qua(BANG, QUAN, TOA, "a", "diem_tham_quan")
    assert n == 1 and dong == ("Các điểm tham quan gần Điểm A nhất (theo đường đi):", "- Điểm B: khoảng 4,0 km đường đi, khoảng 10 phút đi xe.", gd.CAU_GHI_CHU_DIEM)
    assert dong[1].split(": ", 1)[1].rstrip(".") in kc.ket_qua(BANG, "a", "b")[0]  # cùng chữ km + phút với công cụ khoảng cách


@pytest.mark.parametrize("diem, loai, cau", [
    ("b", "quan_an", "Trong kho chưa có bài về quán ăn nào trong khoảng 2 km quanh Điểm B."),   # điểm trong bảng, không có quán gần
    ("b", "ca_phe", "Trong kho chưa có bài về quán cà phê nào trong khoảng 2 km quanh Điểm B."),
    ("khac", "quan_an", gd.CAU_NGOAI_BANG),                                                       # nơi ngoài danh sách
    ("c", "ca_phe", gd.CAU_NGOAI_BANG),                                                           # có tên nhưng không có toạ độ
    ("c", "diem_tham_quan", gd.CAU_NGOAI_BANG),                                                   # … và không có cặp khoảng cách nào
])
def test_nothing_nearby_or_unknown_place_gets_one_fixed_honest_line(diem, loai, cau):
    assert gd.ket_qua(BANG, QUAN, TOA, diem, loai) == ((cau,), 0)


@pytest.mark.parametrize("cau, co", [("gần Đại Nội có quán nào ăn trưa ngon không", True), ("quanh chợ Đông Ba có gì ăn", True), ("cạnh cầu có quán cà phê nào", True),
                                     ("Đại Nội mở cửa mấy giờ", False), ("vé lăng Tự Đức bao nhiêu", False), ("đi gần hết ngày", True)])
def test_keyword_detector(cau, co):  # ca cuối: bật thừa vô hại (model không gọi)
    assert gd.co_tu_khoa_luot(cau, ()) is co
    assert gd.co_tu_khoa_luot("thế còn cà phê thì sao?", ((cau, ""),)) is co  # câu hỏi tiếp: xét câu hỏi liền trước


# ---------- nối vào trợ lý ----------
TAT = AssistantFlags(tim_them=True)
BAT = dataclasses.replace(TAT, khoang_cach=True, khoang_cach_bang=BANG, quan_bang=QUAN, quan_toa_do=TOA, gan_diem=True)
KHONG_GAN = dataclasses.replace(BAT, gan_diem=False)
CAU = "Gần Điểm A có quán nào ăn trưa ngon không?"


def gd_call(diem="a", loai="quan_an") -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "gan_diem", "arguments": json.dumps({"diem": diem, "loai": loai}), "status": "completed"}


def chay(deps, cau, gen, flags, history=(), stream=False):
    trace = AnswerTrace(history=list(history))

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(cau, *deps, gen, trace, flags)]
        await answer_turn(cau, *deps, gen, trace, flags)

    return trace, asyncio.run(go())


def test_flag_defaults_off_and_needs_both_tables():
    assert AssistantFlags().gan_diem is False
    for thieu in ({}, {"khoang_cach": True, "khoang_cach_bang": BANG}, {"khoang_cach": True, "khoang_cach_bang": BANG, "quan_bang": QUAN}):
        with pytest.raises(ValueError, match="gan_diem needs"):
            AssistantFlags(tim_them=True, gan_diem=True, **thieu)


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("cau, history, flags, co_cong_cu", [
    (CAU, (), BAT, True),                                                        # lượt đầu có từ "gần"
    ("Điểm A có những công trình gì?", (), BAT, False),                           # không từ khoá ⇒ như cũ
    ("Thế còn cà phê thì sao?", ((CAU, ""),), BAT, True),                         # hỏi tiếp: câu liền trước có từ khoá
    (CAU, (), KHONG_GAN, False),                                                  # cờ tắt ⇒ như cũ
])
def test_tool_offered_only_with_keywords_and_flag(deps, cau, history, flags, co_cong_cu, stream):
    seen = []
    gen = generator(lambda n, kw: (seen.append(tool_names(kw)), [answer("Mình chưa rõ.")])[1])
    chay(deps, cau, gen, flags, history, stream)
    assert seen and all(("gan_diem" in names) is co_cong_cu and "tim_kho" in names for names in seen)


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("cau, history", [(CAU, ()), ("Điểm A có những công trình gì?", ()), ("Còn Điểm B thì sao?", ((CAU, ""),))])
def test_flag_off_sends_same_model_input_as_before(deps, cau, history, stream):
    """Cờ tắt (kể cả câu có từ "gần"): mọi kwargs của mọi lần gọi model giống hệt cấu hình không có cờ. Cờ bật mà câu không có từ khoá: cũng giống hệt."""
    def ghi(dich):
        return generator(lambda n, kw: (dich.append(json.dumps(kw, ensure_ascii=False, sort_keys=True, default=lambda o: type(o).__name__)), [answer("Mình chưa rõ.")])[1])
    goc, tat, bat = [], [], []
    chay(deps, cau, ghi(goc), dataclasses.replace(KHONG_GAN), history, stream)
    chay(deps, cau, ghi(tat), KHONG_GAN, history, stream)
    assert goc and goc == tat
    if not gd.co_tu_khoa_luot(cau, history):
        chay(deps, cau, ghi(bat), BAT, history, stream)
        assert bat == tat


def test_tool_schema_is_closed_lists(deps):
    seen = []
    chay(deps, CAU, generator(lambda n, kw: (seen.append(kw), [answer("Mình chưa rõ.")])[1]), BAT)
    tool = next(t for t in seen[0]["tools"] if t.get("name") == "gan_diem")
    assert tool["parameters"]["properties"]["diem"]["enum"] == ["a", "b", "c", "khac"]
    assert tool["parameters"]["properties"]["loai"]["enum"] == ["quan_an", "ca_phe", "diem_tham_quan"]
    assert "a: Điểm A (Tên khác A)" in tool["description"]


def _so_nguon(kw) -> str:
    return re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Gần Điểm A", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))[-1]


@pytest.mark.parametrize("stream", [False, True])
def test_answer_citing_the_nearby_source_passes_checks_and_is_logged_without_user_text(deps, stream):
    def kich_ban(n, kw):
        return [gd_call("a", "quan_an")] if n == 1 else [answer(f"Gần Điểm A có Quán Gần, cách dưới 0,5 km, và Quán Vừa, cách khoảng 1,2 km theo đường chim bay [{_so_nguon(kw)}].")]

    trace, events = chay(deps, CAU, generator(kich_ban), BAT, stream=stream)
    assert trace.citation_error is None and trace.khoang_cach_kiem == [] and trace.cited[-1].source == gd.NGUON_SOURCE
    assert trace.cited[-1].title == "Gần Điểm A: quán ăn" and "Quán Gần" in trace.answer
    assert [t for t in trace.tools if t["name"] == "gan_diem"] == [{"name": "gan_diem", "ms": 0.0, "diem": "a", "loai": "quan_an", "n": 3}]
    if stream:  # code tra tức thì ⇒ không phát trạng thái "đang tìm kho"
        assert sum(1 for e in events if e[0] == "status" and e[1].get("stage") == "searching") == 0


def test_distance_number_the_code_did_not_give_is_withdrawn(deps):
    def kich_ban(n, kw):
        return [gd_call("a", "quan_an")] if n == 1 else [answer(f"Quán Gần cách Điểm A khoảng 3 km [{_so_nguon(kw)}].")]

    trace, _ = chay(deps, CAU, generator(kich_ban), BAT)
    assert trace.khoang_cach_kiem == ["3"] and trace.citation_error is None and trace.answer == INSUFFICIENT_ANSWER


def test_fourth_call_in_a_turn_gets_a_reminder_and_no_new_source(deps):
    def kich_ban(n, kw):
        return [gd_call("a", ("quan_an", "ca_phe", "diem_tham_quan", "quan_an")[n - 1])] if n <= 4 else [answer("Mình chưa rõ.")]

    trace, _ = chay(deps, CAU, generator(kich_ban), BAT)
    goi = [t for t in trace.tools if t["name"] == "gan_diem"]
    assert len(goi) == 4 and goi[3].get("het_luot") is True and len(trace.gan_diem) == 3


@pytest.mark.parametrize("cau, flags, so_vong", [(CAU, BAT, 5), ("Điểm A có những công trình gì?", BAT, 4), (CAU, KHONG_GAN, 4)])
def test_max_turns_plus_one_only_when_the_tool_is_offered(deps, cau, flags, so_vong):
    vong = []
    trace, _ = chay(deps, cau, generator(lambda n, kw: (vong.append(n), [tool_call(f"nơi {n}")])[1]), flags)
    assert len(vong) == so_vong and trace.fixed_outcome == "max_turns"
