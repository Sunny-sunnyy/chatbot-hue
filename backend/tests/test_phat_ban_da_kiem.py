"""Ba chỗ hở của đoạn cuối một lượt (soát khác hãng 22/11/2026, ca A1 / A2 / A6) — 0 USD: tìm kho thật, model theo kịch bản.
A1: công tắc `giu_chu_toi_kiem` giữ chữ tới sau phép kiểm nhưng lại phát chữ GỐC của model ⇒ câu có số sai (đã bị phép kiểm số gỡ) vẫn đi ra rồi mới bị
thay. A2: bản viết lại của lưới `het_luot_viet_lai` còn lỗi kiểm (mã nguồn lạ) vẫn được phát rồi mới báo lỗi. A6: đường trả lời thường đã thấy model gọi
công cụ thời tiết loại bão / lũ, rồi bị huỷ vì tin là lệnh sửa lịch ⇒ dấu đó mất ⇒ lưới cuối không gắn câu bản tin chính thức + 112.
Số lượt thật lúc sửa: điều kiện của A1 1 / 470 lượt, A2 0 / 537, A6 chưa thấy — sửa vì mỗi chỗ một hai dòng và A6 là an toàn."""
import asyncio
import dataclasses
import json
import re

from llm import thoi_tiet as tt
from llm.assistant import AnswerTrace, AssistantFlags, _giu_dau_bao_lu, answer_turn_stream, luoi_cuoi_bao
from test_b2_tool_loop import answer, deps, generator  # noqa: F401  (`deps` = fixture tìm kho thật)
from test_het_luot_viet_lai import MOT_Y, kich_ban
from test_khoang_cach import BAT, kc_call

VIET_LAI = AssistantFlags(lan_tim_dau="v2", cau_nhieu_y=True, het_luot_viet_lai=True)
MA_LA = "Huế có nhiều món đáng thử [999]."


def chay(deps, cau, script, flags):
    gen, trace = generator(script), AnswerTrace()
    gen.chu_ve_mot_lan = True  # như lớp dịch Bedrock: chữ của lượt có công cụ về một lần ở cuối
    return trace, asyncio.run(_gom(answer_turn_stream(cau, *deps, gen, trace, flags)))


async def _gom(luong):
    return [e async for e in luong]


def chu_da_gui(events):
    return " ".join(d for k, d in events if k in ("delta", "thay_chu"))


def _so_sai(n, kw):
    if n == 1:
        return [kc_call("a", "b")]
    so = re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: Khoảng cách", json.dumps(kw, ensure_ascii=False, default=str).replace("\\n", "\n"))
    return [answer(f"Từ Điểm A đến Điểm B khoảng 4,0 km, đi xe khoảng 10 phút [{so[-1]}]. Đi đường vòng thì khoảng 999 km [{so[-1]}].")]


def test_held_text_goes_out_only_after_the_number_check_removed_the_wrong_sentence(deps):
    giu = dataclasses.replace(BAT, giu_chu_toi_kiem=True)
    trace, events = chay(deps, "Từ A sang B bao xa?", _so_sai, giu)
    assert trace.citation_error is None and trace.kiem_so_go["nac"] == 1 and "999" not in trace.answer and "4,0 km" in trace.answer
    assert "999" not in chu_da_gui(events)  # trước bản sửa: mảnh chữ đầu mang cả câu "999 km", route phải gửi `thay_chu` sau đó
    assert "".join(d for k, d in events if k == "delta").strip() == trace.answer.strip()
    # đối chứng: công tắc tắt ⇒ chữ ra ngay khi model viết (đường cũ, route thay sau) — bản sửa không chạm đường này
    assert "999" in chu_da_gui(chay(deps, "Từ A sang B bao xa?", _so_sai, BAT)[1])


def test_rewrite_that_fails_the_citation_check_is_not_sent(deps):
    giu = dataclasses.replace(VIET_LAI, giu_chu_toi_kiem=True)
    for flags in (giu, VIET_LAI):  # giữ chữ: không chữ nào ra; không giữ: chữ giữ chỗ đã ra, bản viết lại hỏng không được gửi thay vào
        trace, events = chay(deps, MOT_Y, kich_ban(lan_viet_lai=MA_LA), flags)
        assert trace.citation_error is not None and "[999]" not in chu_da_gui(events)
    assert chu_da_gui(chay(deps, MOT_Y, kich_ban(lan_viet_lai=MA_LA), giu)[1]) == ""
    # đối chứng: bản viết lại hợp lệ vẫn ra đúng một lần
    trace, events = chay(deps, MOT_Y, kich_ban(), giu)
    assert trace.citation_error is None and chu_da_gui(events) == trace.answer


def test_storm_mark_of_the_cancelled_normal_path_survives_into_the_edit_turn():
    cau = "Trời gió giật mạnh quá, bỏ Đầm Chuồn khỏi ngày 1 giúp mình"  # không có chữ nào của lưới bão / lũ
    flags = AssistantFlags()
    co_dau = AnswerTrace(thoi_tiet_ctx={"bao_lu": True, "bao_lu_model": True})  # đường thường: model đã gọi công cụ thời tiết loại bão / lũ
    sua = AnswerTrace(answer="Đã bỏ Đầm Chuồn.")
    _giu_dau_bao_lu(sua, co_dau)
    assert luoi_cuoi_bao(cau, sua, flags) is True and tt.CAU_BAO_LU in sua.notice and "112" in sua.notice
    khong = AnswerTrace(answer="Đã bỏ Đầm Chuồn.")
    _giu_dau_bao_lu(khong, AnswerTrace(thoi_tiet_ctx={"bao_lu": False, "bao_lu_model": False}))
    _giu_dau_bao_lu(khong, AnswerTrace())
    assert khong.thoi_tiet_ctx is None and luoi_cuoi_bao(cau, khong, flags) is False and khong.notice is None  # đối chứng: không có dấu ⇒ không gắn
