"""Công cụ khoảng cách 16/11 (`llm/khoang_cach.py`, plan `2026-11-16-khoang-cach-plan.md`). Phần thuần 0 USD; phần nối trợ lý dùng fixture `deps`
(Qdrant thật, chỉ đọc) + model là client soạn kịch bản (như `test_ngay_lich.py`)."""
import asyncio
import dataclasses
import json
import re

import pytest

from llm import khoang_cach as kc
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from test_b2_tool_loop import _ids, answer, deps, generator, tool_call  # noqa: F401
from test_b5_lich_trinh import tool_names

BANG = kc.BangKhoangCach(ten={"a": "Điểm A", "b": "Điểm B", "c": "Điểm C"}, ten_khac={"a": ("Tên khác A",), "b": (), "c": ()},
                         cap={"a|b": {"km": 4.0, "phut": 4}, "b|a": {"km": 4.2, "phut": 5}, "a|c": {"km": 79.3, "phut": 75}, "c|a": {"km": 0.3, "phut": 1}})


def test_result_uses_table_numbers_and_speed_floor():
    # 4 km OSRM ghi 4 phút (60 km/h) ⇒ sàn 40 km/h ra 6 phút; 79,3 km / 75 phút ⇒ 119 phút = 1 giờ 59 phút; < 0,5 km ⇒ "dưới 0,5 km"
    assert kc.ket_qua(BANG, "a", "b")[0] == "Từ Điểm A đến Điểm B: khoảng 4,0 km đường đi, khoảng 6 phút đi xe (ước theo đường)."
    assert "khoảng 79 km đường đi, khoảng 1 giờ 59 phút đi xe" in kc.ket_qua(BANG, "a", "c")[0]
    assert "dưới 0,5 km đường đi, chưa tới 2 phút đi xe" in kc.ket_qua(BANG, "c", "a")[0]


@pytest.mark.parametrize("a, b", [("a", "khac"), ("khac", "b"), ("a", "a")])
def test_place_outside_list_or_same_place_gets_no_number(a, b):
    assert kc.ket_qua(BANG, a, b) == (kc.CAU_CHUA_CO,)


def test_pair_missing_from_table_gets_no_number():
    dong = kc.ket_qua(BANG, "b", "c")
    assert dong == ("Mình chưa có số khoảng cách từ Điểm B đến Điểm C.",) and not re.search(r"\d", dong[0])


@pytest.mark.parametrize("cau, co", [
    ("Từ điểm này sang điểm kia bao xa?", True), ("đi từ chợ ra biển có xa ko", True), ("Hai nơi cách nhau mấy cây số", True),
    ("Từ ga đi lăng mất bao lâu?", True), ("Khoảng cách giữa hai chùa là bao nhiêu?", True), ("Chợ với cầu có gần nhau không", True),
    ("Lăng cách trung tâm bao nhiêu km", True),
    ("Chùa mở cửa bao lâu mỗi ngày?", False), ("Nên ở Huế bao lâu?", False), ("Vé tham quan cách tính thế nào?", False),
    ("Cột km 0 ở đâu?", False), ("Chùa mở cửa mấy giờ?", False),
])
def test_keyword_detector(cau, co):
    assert kc.co_tu_khoa(cau) is co


def test_number_check_catches_numbers_not_in_sources():
    cho_phep = kc.tap_so(" ".join(kc.ket_qua(BANG, "a", "b")))
    assert kc.kiem_so("Khoảng 4,0 km, đi xe khoảng 6 phút [3].", cho_phep) == []
    assert kc.kiem_so("Khoảng 4.0 km, đi xe khoảng 6 phút.", cho_phep) == []  # chấm thập phân ⇒ chuẩn về phẩy
    assert kc.kiem_so("Khoảng 4 km, đi xe khoảng 6 phút.", cho_phep) == []    # model làm tròn 4,0 ⇒ 4 (lượt đo 16/11: rút lại oan)
    assert kc.kiem_so("Khoảng 8 km.", kc.tap_so("khoảng 8,3 km")) == [] and kc.kiem_so("Khoảng 9 km.", kc.tap_so("khoảng 8,3 km")) == ["9"]
    assert kc.kiem_so("Khoảng 5 km, đi xe 10 phút.", cho_phep) == ["5", "10"]     # ca đối chứng: số tự ước ⇒ bắt được
    assert kc.kiem_so("Lăng xây năm 1840, có 3 cổng.", cho_phep) == []            # số không kèm đơn vị khoảng cách / thời gian ⇒ không xét


def test_load_rejects_table_with_unknown_ids(tmp_path):
    (tmp_path / "kc.json").write_text(json.dumps({"cap": {"a|zz": {"km": 1, "phut": 1}}}), encoding="utf-8")
    (tmp_path / "diem.json").write_text(json.dumps({"diem": [{"id": "a", "ten": "A"}]}), encoding="utf-8")
    with pytest.raises(ValueError, match="zz"):
        kc.nap_bang(tmp_path / "kc.json", tmp_path / "diem.json")


# ---------- Nối vào trợ lý (WORKFLOW §4c: mỗi loại lượt) ----------
TAT = AssistantFlags(tim_them=True)
BAT = dataclasses.replace(TAT, khoang_cach=True, khoang_cach_bang=BANG)


def kc_call(a="a", b="b") -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "khoang_cach",
            "arguments": json.dumps({"diem_a": a, "diem_b": b}), "status": "completed"}


def chay(deps, cau, gen, flags, history=(), stream=False):
    trace = AnswerTrace(history=list(history))

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(cau, *deps, gen, trace, flags)]
        await answer_turn(cau, *deps, gen, trace, flags)

    return trace, asyncio.run(go())


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("cau, history, flags, co_cong_cu", [
    ("Từ Đại Nội sang chùa Thiên Mụ bao xa?", (), BAT, True),                                   # lượt đầu có từ khoá
    ("Đại Nội có những công trình gì?", (), BAT, False),                                         # không từ khoá ⇒ như cũ
    ("Còn sang lăng Tự Đức thì sao?", (("Từ Đại Nội sang chùa Thiên Mụ bao xa?", ""),), BAT, True),  # hỏi tiếp: câu liền trước có từ khoá
    ("Từ Đại Nội sang chùa Thiên Mụ bao xa?", (), TAT, False),                                   # cờ tắt ⇒ như cũ
])
def test_distance_tool_offered_only_with_keywords(deps, cau, history, flags, co_cong_cu, stream):
    seen = []
    gen = generator(lambda n, kw: (seen.append(tool_names(kw)), [answer("Mình chưa rõ.")])[1])
    chay(deps, cau, gen, flags, history, stream)
    assert seen and all(("khoang_cach" in names) is co_cong_cu and "tim_kho" in names for names in seen)


def test_tool_schema_is_enum_of_table_ids_plus_other(deps):
    seen = []
    gen = generator(lambda n, kw: (seen.append(kw), [answer("Mình chưa rõ.")])[1])
    chay(deps, "Từ Đại Nội sang chùa Thiên Mụ bao xa?", gen, BAT)
    tool = next(t for t in seen[0]["tools"] if t.get("name") == "khoang_cach")
    assert tool["parameters"]["properties"]["diem_a"]["enum"] == ["a", "b", "c", "khac"]
    assert "a: Điểm A (Tên khác A)" in tool["description"]


@pytest.mark.parametrize("stream", [False, True])
def test_answer_citing_distance_source_passes_checks(deps, stream):
    def kich_ban(n, kw):
        if n == 1:
            return [kc_call("a", "b")]
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Khoảng cách", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        return [answer(f"Từ Điểm A đến Điểm B khoảng 4,0 km, đi xe khoảng 6 phút [{so[-1]}].")]

    trace, events = chay(deps, "Từ A sang B bao xa?", generator(kich_ban), BAT, stream=stream)
    assert trace.citation_error is None and trace.khoang_cach_kiem == [] and trace.cited[-1].title == kc.TIEU_DE_NGUON
    if stream:  # công cụ tra bảng không phát trạng thái "đang tìm kho"
        assert sum(1 for e in events if e[0] == "status" and e[1].get("stage") == "searching") == 0


def test_model_number_not_in_source_is_withdrawn(deps):
    def kich_ban(n, kw):
        if n == 1:
            return [kc_call("a", "b")]
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Khoảng cách", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        return [answer(f"Khoảng 5 km, đi xe 10 phút [{so[-1]}].")]

    trace, _ = chay(deps, "Từ A sang B bao xa?", generator(kich_ban), BAT)
    assert trace.khoang_cach_kiem == ["5", "10"] and trace.citation_error is not None


@pytest.mark.parametrize("cau, flags, so_vong", [("Từ A sang B bao xa?", BAT, 5), ("Đại Nội có những công trình gì?", BAT, 4),
                                                ("Từ A sang B bao xa?", TAT, 4)])
def test_max_turns_plus_one_only_when_distance_tool_offered(deps, cau, flags, so_vong):
    vong = []
    gen = generator(lambda n, kw: (vong.append(n), [tool_call(f"nơi {n}")])[1])
    trace, _ = chay(deps, cau, gen, flags)
    assert len(vong) == so_vong and trace.fixed_outcome == "max_turns"
