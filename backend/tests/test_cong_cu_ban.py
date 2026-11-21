"""Khoá `assistant.cong_cu_ban` (bậc 3, 21/11/2026) — bản MÔ TẢ công cụ gửi model: 1 = chữ như trước (giống byte), 2 = bốn mô tả viết lại. 0 USD.

Đi đường thật của một lượt (`answer_turn` và `answer_turn_stream` — hai chỗ gọi `mo_ta_theo_ban`), model là `OpenAIResponsesModel` thật của SDK với phản hồi dựng
sẵn (như `test_b2_tool_loop.py`), tìm kho là Qdrant thật (chỉ đọc); bảng khoảng cách và hàm dự báo là đồ dựng để có điều kiện. Test đọc đúng danh sách công cụ
nằm trong yêu cầu gửi model. Đây KHÔNG phải bằng chứng model chọn công cụ / tham số tốt hơn với bản 2 — phần đó là lượt đo có phí ghi trong report của nhánh.
"""
import asyncio
import dataclasses
import json

import pytest

from llm import khoang_cach as kc
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import (INSUFFICIENT_ANSWER, KHOANG_CACH_MO_TA_2, NGAY_LICH_MO_TA, NGAY_LICH_MO_TA_2, THOI_TIET_BAO_LU_MO_TA,
                                    THOI_TIET_BAO_LU_MO_TA_2, THOI_TIET_MO_TA, tim_kho_mo_ta_2)
from test_b2_tool_loop import answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)
from test_het_luot_tim import sent_requests

CAU = "Huế có món gì ngon?"
LICH_SU = (("Lăng Tự Đức ở đâu?", ""),)
TEN = ["tim_kho", "thoi_tiet", "ngay_lich", "khoang_cach"]


@pytest.fixture
def flags(tmp_path) -> AssistantFlags:
    (tmp_path / "kc.json").write_text(json.dumps({"cap": {"a|b": {"km": 1, "phut": 1}}}), encoding="utf-8")
    (tmp_path / "diem.json").write_text(json.dumps({"diem": [{"id": "a", "ten": "A"}, {"id": "b", "ten": "B"}]}), encoding="utf-8")

    async def du_bao():  # model dựng sẵn không gọi công cụ nào: test chỉ xét MÔ TẢ được gửi
        raise AssertionError("forecast must not be fetched")

    # `cong_cong_cu: luon` ⇒ cả ba công cụ thời tiết / ngày / khoảng cách được đưa ở mọi câu (không phải chọn câu có từ khoá)
    return AssistantFlags(tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, du_bao=du_bao, ngay_lich=True, cong_cong_cu="luon",
                          khoang_cach=True, khoang_cach_bang=kc.nap_bang(tmp_path / "kc.json", tmp_path / "diem.json"))


def luot(deps, flags: AssistantFlags, history=(), stream: bool = False) -> tuple[dict, list[dict]]:
    """Một lượt qua đường thật ⇒ (công cụ theo tên như nằm trong yêu cầu gửi model, mọi yêu cầu của lượt đã bỏ id)."""
    gen, trace = generator(lambda n, kw: [answer(INSUFFICIENT_ANSWER)]), AnswerTrace(history=history)

    async def chay():
        if stream:
            [e async for e in answer_turn_stream(CAU, *deps, gen, trace, flags)]
        else:
            await answer_turn(CAU, *deps, gen, trace, flags)

    asyncio.run(chay())
    cong_cu = gen.client.responses.calls[0]["tools"]
    assert [t["name"] for t in cong_cu] == TEN  # tên và thứ tự không phụ thuộc bản mô tả
    return {t["name"]: t for t in cong_cu}, json.loads(sent_requests(gen))


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("history", [(), LICH_SU])  # WORKFLOW §4c: lượt đầu + lượt có lịch sử
def test_version_1_is_the_default_and_leaves_every_request_unchanged(deps, flags, history, stream):
    luot(deps, dataclasses.replace(flags, cong_cu_ban=2), history, stream)  # một lượt bản 2 chạy TRƯỚC không được để lại gì cho lượt sau
    cong_cu, gui = luot(deps, dataclasses.replace(flags, cong_cu_ban=1), history, stream)
    assert AssistantFlags().cong_cu_ban == 1 and gui == luot(deps, flags, history, stream)[1]  # khoá = 1 ≡ không đặt khoá
    assert cong_cu["tim_kho"]["description"].startswith("Tìm thêm Bằng chứng trong kho tri thức Huế")
    assert cong_cu["thoi_tiet"]["description"] == THOI_TIET_BAO_LU_MO_TA and cong_cu["ngay_lich"]["description"] == NGAY_LICH_MO_TA
    assert cong_cu["khoang_cach"]["description"] == kc.mo_ta_cong_cu(flags.khoang_cach_bang)


@pytest.mark.parametrize("stream", [False, True])  # hai chỗ gọi: đường không stream và đường stream
@pytest.mark.parametrize("history", [(), LICH_SU])
def test_version_2_rewrites_the_four_descriptions_and_nothing_else(deps, flags, history, stream):
    cu, gui_cu = luot(deps, flags, history, stream)
    moi, gui_moi = luot(deps, dataclasses.replace(flags, cong_cu_ban=2, so_lan_tim_kho=3), history, stream)
    mo_ta_tim, _, dong_tham_so = tim_kho_mo_ta_2(3).partition("\n\nArgs:\n")
    assert moi["tim_kho"]["description"] == mo_ta_tim and "tối đa 3 lần" in mo_ta_tim  # số lần tìm lấy từ cấu hình, không viết cứng
    assert moi["thoi_tiet"]["description"] == THOI_TIET_BAO_LU_MO_TA_2 and moi["ngay_lich"]["description"] == NGAY_LICH_MO_TA_2
    assert moi["khoang_cach"]["description"] == kc.mo_ta_cong_cu(flags.khoang_cach_bang, KHOANG_CACH_MO_TA_2)
    assert moi["khoang_cach"]["description"].endswith("\nDanh sách:\na: A\nb: B") and '"khac"' in moi["khoang_cach"]["description"]
    # khuôn tham số: chỉ dòng tả `cau_tim` đổi; ba công cụ kia giữ nguyên khuôn (enum mã điểm, số ngày, loại)
    assert moi["tim_kho"]["parameters"]["properties"]["cau_tim"]["description"] == dong_tham_so.split("cau_tim: ", 1)[1]
    for ten in TEN[1:]:
        assert moi[ten]["parameters"] == cu[ten]["parameters"], ten
    # ngoài danh sách công cụ, yêu cầu gửi model (lời dặn, tin nhắn, ngữ cảnh) không đổi một chữ
    assert [{k: v for k, v in yc.items() if k != "tools"} for yc in gui_moi] == [{k: v for k, v in yc.items() if k != "tools"} for yc in gui_cu]


def test_weather_tool_without_the_storm_parameter_has_no_version_2(deps, flags):
    """Cờ `bao_lu_cong_cu` tắt ⇒ công cụ thời tiết không có `loai`; mô tả bản 2 nói về `loai` nên không được gắn vào bản công cụ này."""
    cong_cu, _ = luot(deps, dataclasses.replace(flags, bao_lu_cong_cu=False, cong_cu_ban=2))
    assert cong_cu["thoi_tiet"]["description"] == THOI_TIET_MO_TA and "loai" not in cong_cu["thoi_tiet"]["parameters"]["properties"]


def test_key_is_read_from_settings_and_rejects_unknown_versions():
    def doc(assistant: dict) -> int:
        return AssistantFlags.from_settings({"assistant": assistant, "full_corpus_generation": {"provider": "openai"}}).cong_cu_ban

    assert doc({}) == 1 and doc({"cong_cu_ban": 1}) == 1 and doc({"cong_cu_ban": 2}) == 2
    for sai in (0, 3, "2"):
        with pytest.raises(ValueError, match="cong_cu_ban"):
            doc({"cong_cu_ban": sai})
