"""Công cụ khoảng cách 16/11 (`llm/khoang_cach.py`, plan `2026-11-16-khoang-cach-plan.md`). Phần thuần 0 USD; phần nối trợ lý dùng fixture `deps`
(Qdrant thật, chỉ đọc) + model là client soạn kịch bản (như `test_ngay_lich.py`)."""
import asyncio
import dataclasses
import json
import re

import pytest

from llm import khoang_cach as kc
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_b2_tool_loop import _ids, answer, deps, generator, tool_call  # noqa: F401
from test_b5_lich_trinh import tool_names

BANG = kc.BangKhoangCach(ten={"a": "Điểm A", "b": "Điểm B", "c": "Điểm C"}, ten_khac={"a": ("Tên khác A",), "b": (), "c": ()},
                         cap={"a|b": {"km": 4.0, "phut": 4}, "b|a": {"km": 4.2, "phut": 5}, "a|c": {"km": 79.3, "phut": 75}, "c|a": {"km": 0.3, "phut": 1}})


def test_result_uses_table_numbers_and_travel_time_rule():
    # phút = 1,25 × phút OSRM + 5: 4 ⇒ 10; 75 ⇒ 99 = 1 giờ 39 phút; 1 ⇒ 6 (1,25 làm tròn nửa lên); < 0,5 km ⇒ "dưới 0,5 km"
    assert kc.ket_qua(BANG, "a", "b")[0] == "Từ Điểm A đến Điểm B: khoảng 4,0 km đường đi, khoảng 10 phút đi xe (ước theo đường)."
    assert "khoảng 79 km đường đi, khoảng 1 giờ 39 phút đi xe" in kc.ket_qua(BANG, "a", "c")[0]
    assert "dưới 0,5 km đường đi, khoảng 6 phút đi xe" in kc.ket_qua(BANG, "c", "a")[0]


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
    # review 16/11 m1: "cách làm / nấu / đây", thời lượng nấu / xem không có từ di chuyển ⇒ không bật
    ("Cách làm bún cần bao nhiêu nguyên liệu?", False), ("Cách nấu chè cần mấy loại đậu?", False), ("Bánh luộc mấy tiếng thì chín?", False),
    ("Nấu nồi bún mất bao lâu?", False), ("Buổi diễn kéo dài mấy tiếng?", False), ("Vé này cách đây mấy năm?", False),
    ("Từ chợ đi xe máy mấy phút?", True), ("Ra biển mất bao lâu?", True),
])
def test_keyword_detector(cau, co):
    assert kc.co_tu_khoa(cau) is co


def test_number_check_catches_numbers_not_in_sources():
    cho_phep = kc.tap_so_theo_loai(" ".join(kc.ket_qua(BANG, "a", "b")))  # "khoảng 4,0 km …, khoảng 10 phút"
    assert kc.kiem_so("Khoảng 4,0 km, đi xe khoảng 10 phút [3].", cho_phep) == []
    assert kc.kiem_so("Khoảng 4.0 km, đi xe khoảng 10 phút.", cho_phep) == []  # chấm thập phân ⇒ chuẩn về phẩy
    assert kc.kiem_so("Khoảng 4 km, đi xe khoảng 10 phút.", cho_phep) == []    # model làm tròn 4,0 ⇒ 4 (lượt đo 16/11: rút lại oan)
    assert kc.kiem_so("Khoảng 5 km, đi xe 12 phút.", cho_phep) == ["5", "12"]     # ca đối chứng: số tự ước ⇒ bắt được
    assert kc.kiem_so("Khoảng 10 km, đi xe 4 phút.", cho_phep) == ["10", "4"]     # đảo đơn vị (review m2) ⇒ bắt được
    assert kc.kiem_so("Đi xe 15p, hoặc 1h nếu kẹt.", cho_phep) == ["15", "1"]    # viết tắt cũng xét
    assert kc.kiem_so("Lăng xây năm 1840, có 3 cổng.", cho_phep) == []            # số không kèm đơn vị khoảng cách / thời gian ⇒ không xét
    assert kc.kiem_so("Khoảng 8 km.", kc.tap_so_theo_loai("khoảng 8,3 km")) == []
    assert kc.kiem_so("Khoảng 9 km.", kc.tap_so_theo_loai("khoảng 8,3 km")) == ["9"]


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


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("cau, history", [("Đại Nội có những công trình gì?", ()),
                                          ("Còn chùa Thiên Mụ thì sao?", (("Đại Nội có những công trình gì?", ""),))])
def test_flag_on_without_keyword_sends_same_model_input_as_flag_off(deps, cau, history, stream):
    # review m3: câu không có từ khoá ⇒ chuỗi gửi model (mọi kwargs của mọi lần gọi) giống hệt cờ tắt
    def ghi(dich):
        return generator(lambda n, kw: (dich.append(json.dumps(kw, ensure_ascii=False, sort_keys=True, default=lambda o: type(o).__name__)),
                                        [answer("Mình chưa rõ.")])[1])
    tat, bat = [], []
    chay(deps, cau, ghi(tat), TAT, history, stream)
    chay(deps, cau, ghi(bat), BAT, history, stream)
    assert tat and tat == bat


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
        return [answer(f"Từ Điểm A đến Điểm B khoảng 4,0 km, đi xe khoảng 10 phút [{so[-1]}].")]

    trace, events = chay(deps, "Từ A sang B bao xa?", generator(kich_ban), BAT, stream=stream)
    assert trace.citation_error is None and trace.khoang_cach_kiem == [] and trace.cited[-1].title == kc.TIEU_DE_NGUON
    if stream:  # công cụ tra bảng không phát trạng thái "đang tìm kho"
        assert sum(1 for e in events if e[0] == "status" and e[1].get("stage") == "searching") == 0


def test_model_number_not_in_source_is_withdrawn(deps):
    def kich_ban(n, kw):
        if n == 1:
            return [kc_call("a", "b")]
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Khoảng cách", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        return [answer(f"Khoảng 5 km, đi xe 12 phút [{so[-1]}].")]

    trace, _ = chay(deps, "Từ A sang B bao xa?", generator(kich_ban), BAT)
    # 21/11/2026: số lạ không còn làm cả lượt báo lỗi — câu chứa nó bị gỡ; ở đây không còn gì ⇒ câu từ chối cố định. Lần trượt vẫn được ghi.
    assert trace.khoang_cach_kiem == ["5", "12"] and trace.citation_error is None and trace.kiem_so_go["nac"] == 2
    assert trace.answer == INSUFFICIENT_ANSWER


@pytest.mark.parametrize("cau, flags, so_vong", [("Từ A sang B bao xa?", BAT, 5), ("Đại Nội có những công trình gì?", BAT, 4),
                                                ("Từ A sang B bao xa?", TAT, 4)])
def test_max_turns_plus_one_only_when_distance_tool_offered(deps, cau, flags, so_vong):
    vong = []
    gen = generator(lambda n, kw: (vong.append(n), [tool_call(f"nơi {n}")])[1])
    trace, _ = chay(deps, cau, gen, flags)
    assert len(vong) == so_vong and trace.fixed_outcome == "max_turns"


# ---------- Khoảng cách tính sẵn (plan `2026-11-17-khoang-cach-tinh-san-plan.md`) ----------
BANG_TEN = kc.BangKhoangCach(
    ten={"dn": "Đại Nội Huế", "kt": "Kinh thành Huế (Ngọ Môn – Kỳ Đài)", "tm": "Chùa Thiên Mụ", "kg": "Không gian Lê Văn", "tt": "Trung tâm Lê Văn"},
    ten_khac={"dn": ("Hoàng thành Huế",), "kt": ("Kinh thành Huế", "Thành Huế"), "tm": ("Chùa Linh Mụ",), "kg": ("Lê Văn",), "tt": ("Lê Văn",)},
    cap={f"{a}|{b}": {"km": 3.0, "phut": 8} for a in ("dn", "kt", "tm") for b in ("dn", "kt", "tm") if a != b})


@pytest.mark.parametrize("cau, cap", [
    ("Từ Đại Nội Huế đến Chùa Thiên Mụ bao xa?", ("dn", "tm")),
    ("chùa linh mụ cách  đại nội mấy km", ("tm", "dn")),                      # tên khác, chữ thường, thừa khoảng trắng, bỏ " Huế", theo thứ tự câu
    ("Từ Hoàng thành Huế ra Thành Huế bao xa?", ("dn", "kt")),                  # cụm dài trước: "Hoàng thành Huế" không bị "Thành Huế" ăn mất
    ("Kinh thành cách chùa Thiên Mụ bao xa?", ("kt", "tm")),
    ("Đại Nội-chùa Thiên Mụ đi xe máy mất mấy phút?", ("dn", "tm")),
    ("Đại Nội có gần chùa Thiên Mụ không?", ("dn", "tm")),
    ("Đại Nội với chùa Thiên Mụ cách nhau bao xa?", ("dn", "tm")),
    ("Từ Đại Nội đi chùa Thiên Mụ rồi về lại Đại Nội bao xa?", None),          # ba lần nhắc tên ⇒ không phải dạng "A … B"
    # review E 16/11 M-1 — hai tên bảng có mặt nhưng khoảng cách được hỏi là tới / từ nơi thứ ba, hoặc tên nằm trong tên riêng khác
    ("Đại Nội và chùa Thiên Mụ cách trung tâm bao xa?", None),
    ("Từ ga Huế đến Đại Nội và chùa Thiên Mụ bao xa?", None),
    ("Từ Đại Nội đến chùa Thiên Mụ rồi qua lăng kia bao xa?", None),
    ("Từ khách sạn Đại Nội đến chùa Thiên Mụ bao xa?", None),
    ("Từ Đại Nội Plaza đến chùa Thiên Mụ bao xa?", None),
    ("Đại Nội có xa trung tâm hơn chùa Thiên Mụ không?", None),
    ("Đến chùa Thiên Mụ từ Đại Nội thì bao xa?", None),                         # m-1: không đoán chiều đi ⇒ đường cũ
    ("Đại Nội cách trung tâm bao xa?", None),                                   # một điểm
    ("Từ Đại Nội qua Kinh thành rồi tới chùa Thiên Mụ bao xa?", None),         # ba điểm
    ("Từ Lê Văn đến Đại Nội bao xa?", None),                                    # "Lê Văn" trỏ hai mã ⇒ không đọc ⇒ còn một điểm
    ("Khách sạn Đại Nộib cách chùaThiên Mụ bao xa?", None),                     # không khớp giữa chữ (ranh giới chữ)
    ("Đi Đại Nội hay chùa Thiên Mụ thì bao xa?", None),                         # hai lựa chọn
    ("Đại Nội với chùa Thiên Mụ, nơi nào gần hơn?", None),                      # câu so sánh
    ("Đại Nội mở cửa mấy giờ, còn chùa Thiên Mụ thì sao?", None),               # hai điểm nhưng không hỏi khoảng cách
    ("Từ Đại Nội đến Không gian Lê Văn bao xa?", None),                         # đủ hai điểm nhưng bảng không có số cho cặp ⇒ đường cũ
])
def test_precomputed_pair_reads_exactly_two_table_places(cau, cap):
    assert kc.cap_tinh_san(cau, BANG_TEN) == cap


def test_short_names_for_reading_user_text_stay_out_of_tool_description():
    # review E m-2: tên gõ tắt chỉ để CODE đọc câu; mô tả công cụ (chuỗi gửi model) vẫn chỉ có tên + tên khác của bảng
    bang = kc.BangKhoangCach(ten={"cho_dong_ba": "Chợ Đông Ba", "dn": "Đại Nội Huế"}, ten_khac={"cho_dong_ba": (), "dn": ()},
                             cap={"cho_dong_ba|dn": {"km": 2.0, "phut": 5}})
    assert kc.cap_tinh_san("Đông Ba cách Đại Nội bao xa?", bang) == ("cho_dong_ba", "dn")
    assert kc.mo_ta_cong_cu(bang).endswith("Danh sách:\ncho_dong_ba: Chợ Đông Ba\ndn: Đại Nội Huế")


SAN = dataclasses.replace(BAT, khoang_cach_tinh_san=True)
CAU_SAN = "Từ Điểm A đến Điểm B bao xa?"


def _ghi(dich):
    return generator(lambda n, kw: (dich.append(json.dumps(kw, ensure_ascii=False, sort_keys=True, default=lambda o: type(o).__name__)),
                                    [answer("Mình chưa rõ.")])[1])


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("history", [(), (("Điểm C có gì hay?", ""),)])
def test_precomputed_distance_is_in_first_model_input_without_distance_tool(deps, history, stream):
    seen = []
    gen = generator(lambda n, kw: (seen.append(kw), [answer("Mình chưa rõ.")])[1])
    trace, _ = chay(deps, CAU_SAN, gen, SAN, history, stream)
    chu = json.dumps(seen[0], ensure_ascii=False, default=str)
    assert len(seen) == 1 and "khoang_cach" not in tool_names(seen[0]) and "tim_kho" in tool_names(seen[0])
    assert kc.TIEU_DE_NGUON in chu and "khoảng 4,0 km đường đi, khoảng 10 phút đi xe" in chu
    assert trace.khoang_cach == [{"diem_a": "a", "diem_b": "b", "dong": kc.ket_qua(BANG, "a", "b")}]
    assert [t for t in trace.tools if t["name"] == "khoang_cach_san"] == [{"name": "khoang_cach_san", "ms": 0.0, "diem_a": "a", "diem_b": "b"}]
    # ca đối chứng: cùng câu, cờ tính sẵn tắt ⇒ có công cụ, ngữ cảnh chưa có nguồn khoảng cách
    seen.clear()
    chay(deps, CAU_SAN, gen, BAT, history, stream)
    assert "khoang_cach" in tool_names(seen[0]) and kc.TIEU_DE_NGUON not in json.dumps(seen[0]["input"], ensure_ascii=False, default=str)


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("cau, history", [
    ("Từ A sang B bao xa?", ()),                                       # có từ khoá, không đọc được hai tên ⇒ đường cũ
    ("Điểm A cách trung tâm bao xa?", ()),                             # một điểm
    ("Điểm A và Điểm B mở cửa mấy giờ?", ()),                          # hai điểm, không từ khoá
    ("Còn Điểm A với Điểm B thì sao?", ((CAU_SAN, ""),)),              # từ khoá chỉ ở câu liền trước ⇒ đường cũ (model gọi công cụ)
])
def test_precompute_flag_on_but_no_pair_sends_same_model_input_as_flag_off(deps, cau, history, stream):
    cu, moi = [], []
    chay(deps, cau, _ghi(cu), BAT, history, stream)
    chay(deps, cau, _ghi(moi), SAN, history, stream)
    assert cu and cu == moi


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("chu_model, loi", [("Từ Điểm A đến Điểm B khoảng 4,0 km, đi xe khoảng 10 phút [{n}].", []),
                                            ("Khoảng 5 km, đi xe 12 phút [{n}].", ["5", "12"])])
def test_number_check_still_runs_on_precomputed_distance(deps, chu_model, loi, stream):
    def kich_ban(n, kw):
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Khoảng cách", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        return [answer(chu_model.format(n=so[-1]))]

    trace, _ = chay(deps, CAU_SAN, generator(kich_ban), SAN, stream=stream)
    assert trace.khoang_cach_kiem == loi and trace.citation_error is None and (trace.kiem_so_go is None) is (not loi)
    assert ("5 km" in trace.answer) is False
    if not loi:
        assert trace.cited[-1].title == kc.TIEU_DE_NGUON


def test_precomputed_turn_keeps_default_max_turns(deps):
    vong = []
    gen = generator(lambda n, kw: (vong.append(n), [tool_call(f"nơi {n}")])[1])
    trace, _ = chay(deps, CAU_SAN, gen, SAN)
    assert len(vong) == 4 and trace.fixed_outcome == "max_turns"


def test_precompute_flag_needs_distance_flag():
    with pytest.raises(ValueError, match="khoang_cach_tinh_san"):
        AssistantFlags(tim_them=True, khoang_cach_tinh_san=True)


# ---------- Ghi chú "chưa tính kẹt xe" do code nối (16/11 tối) ----------
@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("flags", [BAT, SAN])  # đường công cụ và đường tính sẵn
@pytest.mark.parametrize("chu_model, notice", [
    ("Từ Điểm A đến Điểm B khoảng 4,0 km, đi xe khoảng 10 phút [{n}].", kc.CAU_GHI_CHU),                       # model bỏ ghi chú ⇒ code nối
    ("Từ Điểm A đến Điểm B khoảng 4,0 km, khoảng 10 phút đi xe, chưa tính kẹt xe hay dừng nghỉ [{n}].", None),  # model đã ghi ⇒ không lặp
    ("Nơi này có nhiều công trình [1].", None),                                                                 # chỉ trích đoạn kho, không trích nguồn khoảng cách ⇒ không nối
])
def test_code_adds_traffic_note_when_answer_cites_distance_source_without_it(deps, flags, chu_model, notice, stream):
    def kich_ban(n, kw):
        so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Khoảng cách", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
        if not so:
            return [kc_call("a", "b")]
        return [answer(chu_model.format(n=so[-1]))]

    trace, events = chay(deps, CAU_SAN, generator(kich_ban), flags, stream=stream)
    assert trace.notice == notice and trace.citation_error is None


def test_traffic_note_comes_before_may_have_changed_notice():
    from llm.assistant import MAY_HAVE_CHANGED_NOTICE, PackedSource, set_notice
    trace = AnswerTrace()
    trace.answer = "Khoảng 4,0 km [1]. Vé vào cửa xem ở quầy [2]."
    trace.cited = [PackedSource(id=1, title=kc.TIEU_DE_NGUON, heading_path=(kc.MUC_NGUON,), excerpts=("x",), source=kc.NGUON_SOURCE),
                   PackedSource(id=2, title="Vé", heading_path=("Vé",), excerpts=("y",), source="travel/tickets/ve.md")]
    set_notice(trace, dataclasses.replace(TAT, may_have_changed_notice=True))
    assert trace.notice == f"{kc.CAU_GHI_CHU} {MAY_HAVE_CHANGED_NOTICE}"
