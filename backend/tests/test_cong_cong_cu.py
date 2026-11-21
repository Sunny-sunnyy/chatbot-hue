"""Bậc 5 (21/11/2026) — cổng ĐƯA công cụ thời tiết / ngày / khoảng cách cho trợ lý: từ nguy hiểm thời tiết mới (dông, sấm sét, nước sông lên) + khoá chế độ `cong_cong_cu`.
0 USD, không mạng: hàm cổng thật, `_lich_extra` thật, agent dựng thật (`_assistant_for`) — chỉ bảng khoảng cách và hàm dự báo là đồ dựng để có điều kiện.
Không phải bằng chứng model gọi công cụ đúng lúc — phần đó ở lượt đo có phí."""
import dataclasses
import json

import pytest

from llm import khoang_cach as kc
from llm import thoi_tiet as tt
from llm.assistant import AnswerTrace, AssistantFlags, _lich_extra, _luot_bao_lu
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator

BA_CONG_CU = {"thoi_tiet_fn", "ngay_lich_fn", "khoang_cach_fn"}


@pytest.fixture
def flags(tmp_path) -> AssistantFlags:
    (tmp_path / "kc.json").write_text(json.dumps({"cap": {"a|b": {"km": 1, "phut": 1}}}), encoding="utf-8")
    (tmp_path / "diem.json").write_text(json.dumps({"diem": [{"id": "a", "ten": "A"}, {"id": "b", "ten": "B"}]}), encoding="utf-8")

    async def du_bao():  # không được gọi ở đây: test chỉ xét công cụ nào được ĐƯA
        raise AssertionError("forecast must not be fetched")

    return AssistantFlags(tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, du_bao=du_bao, ngay_lich=True,
                          khoang_cach=True, khoang_cach_bang=kc.nap_bang(tmp_path / "kc.json", tmp_path / "diem.json"))


def dua(query: str, flags: AssistantFlags, history=(), khoang_cach_san=None) -> dict:
    trace = AnswerTrace()
    trace.history, trace.khoang_cach = history, khoang_cach_san
    return _lich_extra(query, None, None, trace, None, None, flags)


@pytest.mark.parametrize("cau, truoc", [
    ("Chiều nay ở Thuận An có dông không?", None),
    ("Nước sông Hương mấy hôm nay có lên cao không?", None),
    ("Đang sấm sét ầm ầm, có nên lên đồi Vọng Cảnh không?", None),
    ("Sông Bồ đang dâng nhanh, đường về Quảng Điền có đi được không?", None),
    ("Nghe tiếng sấm rền, có nên rời đồi Thiên An không?", None),
    ("Nước đang lên ở khu phố cổ Bao Vinh phải không?", None),
    # review phiên đo 21/11: sau khi dòng "nước lên / dâng / về" đổi sang điều kiện dương, các cách nói thật vẫn phải được nhận
    ("Mấy hôm nay nước lên chưa bà con?", None), ("Sông Hương nước lên rồi, đi thuyền rồng được không?", None), ("Nước về tới Hương Sơ chưa?", None),
    ("Bà con ơi nước lên!", None), ("Huế có dông ba ngày nay rồi, mai ra Lăng Cô được không?", None),  # "dông ba ngày" ≠ lỗi gõ "Dông Ba"
    ("Vậy có nên ra biển không?", "Chiều nay ở Thuận An có dông không?"),  # câu hỏi tiếp: xét cả câu hỏi liền trước
])
def test_new_weather_hazard_phrases_open_the_tool_gate_and_both_safety_nets(cau, truoc, flags):
    history = ((truoc, ""),) if truoc else ()
    assert tt.co_tu_khoa_luot_rong(cau, history) and "thoi_tiet_fn" in dua(cau, flags, history)  # công cụ được đưa
    assert tt.la_luot_bao_lu(cau, history) and _luot_bao_lu(cau, history)  # lượt bão / lũ: câu bản tin chính thức + 112 đi kèm
    assert not tt.co_tu_khoa_luot(cau, history)  # cổng của bản cờ `bao_lu_cong_cu` TẮT không đổi


@pytest.mark.parametrize("cau", ["Chợ Đông Ba bán nước mía ở đâu?", "Mùa đông ở Huế nên ăn gì?", "Sông Hương dài bao nhiêu?", "Lăng Tự Đức có gì đặc biệt?",
                                 "Anh hướng dẫn viên nói dông dài quá, lăng này xây năm nào?", "Chợ Dông Ba mở cửa mấy giờ?", "Nước sông Hương có sạch không?",
                                 "Vé thuyền rồng trên sông Hương có lên giá không?", "Ấm đất sét nung ở làng gốm Phước Tích giá bao nhiêu?",
                                 "Ở Phong Điền có quán nào bán con dông xào lăn không?", "Đun nước lên pha trà rồi ăn chè gì ngon?",
                                 "Đi thuyền ra điện Hòn Chén trên sông Hương dâng hương cần chuẩn bị gì?",
                                 # review phiên đo 21/11 — chữ "nước" trong từ ghép / nghĩa khác, và ba câu gài còn lại
                                 "Vua Gia Long thống nhất đất nước lên ngôi năm nào?", "Ngắm sông Hương non nước về đêm ở đâu đẹp nhất?",
                                 "Mua nước về khách sạn ở đâu gần Đại Nội?", "Nhạc nước lên đèn lúc mấy giờ ở công viên Tứ Tượng?",
                                 "Múc nước lên từ giếng cổ làng Phước Tích có uống được không?", "Việt kiều về nước lên Huế chơi mấy ngày thì đủ?",
                                 "Đun  nước lên pha trà kiểu Huế thế nào?",  # hai dấu cách liền nhau không làm hỏng phép loại trừ
                                 "Sét cơm vua ở nhà hàng cung đình giá bao nhiêu?", "Lời sấm về kinh đô Phú Xuân trong sử nhà Nguyễn có thật không?",
                                 "Bác tài bảo xe dông thẳng ra bến, không ghé quán nào hả?", "Thuyền rồng sông Hương dâng trà chiều giá vé bao nhiêu?"])
def test_look_alike_questions_keep_the_gate_and_the_nets_closed(cau, flags):
    assert not tt.co_tu_khoa_luot_rong(cau, ()) and not _luot_bao_lu(cau, ())
    assert not BA_CONG_CU & set(dua(cau, flags))


@pytest.mark.parametrize("history", [(), (("Lăng Tự Đức ở đâu?", ""),)])  # WORKFLOW §4c: lượt đầu + lượt có lịch sử
def test_gate_mode_decides_which_tools_reach_the_model(history, flags):
    cau = "Lăng Tự Đức có gì đặc biệt?"  # không từ khoá thời tiết / ngày / khoảng cách
    assert not BA_CONG_CU & set(dua(cau, flags, history))  # mặc định "tu_khoa": như trước
    luon = dataclasses.replace(flags, cong_cong_cu="luon")
    extra = dua(cau, luon, history)
    assert BA_CONG_CU <= set(extra)

    async def tim_kho(cau_tim: str) -> str:
        return ""

    agent, _, _ = OpenAIFullCorpusGenerator(client=object(), model="x")._assistant_for(tim_kho, history=history, **extra)
    assert [tool.name for tool in agent.tools] == ["tim_kho", "thoi_tiet", "ngay_lich", "khoang_cach"]  # danh sách gửi model ở mọi vòng của lượt


def test_always_mode_keeps_the_two_existing_exceptions(flags):
    luon = dataclasses.replace(flags, cong_cong_cu="luon")
    assert "thoi_tiet_fn" not in dua("Tháng sau Huế có lễ hội gì?", luon)  # ngoài 7 ngày: không có số dự báo nào để đưa
    assert "khoang_cach_fn" not in dua("Lăng Tự Đức có gì đặc biệt?", luon, khoang_cach_san=[{"diem_a": "a", "diem_b": "b", "dong": ("x",)}])  # số đã tính sẵn


def test_gate_mode_follows_the_provider_and_rejects_unknown_values():
    def nap(provider, assistant_mode=None, bedrock_mode=None):
        assistant = {"tim_them": True, **({"cong_cong_cu": assistant_mode} if assistant_mode else {})}
        bedrock = {"cong_cong_cu": bedrock_mode} if bedrock_mode else {}
        return AssistantFlags.from_settings({"assistant": assistant, "full_corpus_generation": {"provider": provider, "bedrock": bedrock}}).cong_cong_cu

    assert nap("openai") == "tu_khoa" and nap("bedrock") == "tu_khoa"  # không khai ⇒ hành vi cũ
    assert nap("openai", assistant_mode="luon", bedrock_mode="tu_khoa") == "luon"
    assert nap("bedrock", assistant_mode="luon", bedrock_mode="tu_khoa") == "tu_khoa"
    assert nap("bedrock", bedrock_mode="luon") == "luon" and nap("openai", bedrock_mode="luon") == "tu_khoa"
    with pytest.raises(ValueError, match="cong_cong_cu"):
        nap("openai", assistant_mode="moi_luot")
