"""Công tắc `nho_dap_cuoc_co_lich` (22/11/2026). Vì sao: cuộc ĐÃ LƯU lịch thì "nhớ câu trả lời liền trước" tắt ngầm cho MỌI câu hỏi thường về sau — đường
thường của cuộc đó luôn để lại `trace.sua = {n_hanh_dong: 0}` và luôn nối nguồn lịch, nên luật "lượt DÙNG lịch không giữ đáp" thành "cả cuộc không giữ" (soát
khác hãng 22/11; lập lịch xong quay sang hỏi "quán thứ hai bạn vừa kể ở đường nào" là cách dùng thường). Bật: (1) chỉ chặn lượt thật sự sửa lịch hoặc câu
trả lời có TRÍCH nguồn lịch; (2) lượt bị rút khi đang nhớ đáp được chạy lại một lần cả trong cuộc có lịch — lần hai đi thẳng đường trả lời thường, KHÔNG
gọi lại bước hiểu ý sửa lịch. 0 USD: tìm kho thật, model theo kịch bản; phần loại lượt chạy với ĐÚNG các cờ đường đi đang chạy thật."""
import asyncio
import copy
import json
from types import SimpleNamespace

import pytest
from openai.types.responses import Response, ResponseCompletedEvent, ResponseCreatedEvent, ResponseTextDeltaEvent

from api.conversations import NHAN_LOI_TRUOC, ConversationStore, dap_duoc_nho
from core.settings_loader import load_settings
from llm import lich_trinh_v2 as v2
from llm.assistant import TEN_CHAY_LAI, AnswerTrace, AssistantFlags, answer_turn_stream_parallel
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_cong_dot_1 import chu_gui, flags_from
from test_lich_vao_hoi_thuong import DUONG_DI, KichBan, lich_2_ngay, loai
from test_toc_do_song_song import USAGE, Client, _ids, deps, message  # noqa: F401 (`deps`: fixture đường tìm thật)

TAT = flags_from(**DUONG_DI, lich_vao_hoi_thuong=True, nho_dap_cuoc_co_lich=False)
MO = flags_from(**DUONG_DI, lich_vao_hoi_thuong=True, nho_dap_cuoc_co_lich=True)
CAU_TRUOC, CAU = "Vé lẻ vào Đại Nội giá bao nhiêu?", "Thế trẻ em thì bao nhiêu?"
CO_DAP = ((CAU_TRUOC, f"{NHAN_LOI_TRUOC}\nVé lẻ người lớn 200.000 đồng."),)
KHONG_DAP = ((CAU_TRUOC, ""),)
KHONG_TRICH, CO_TRICH = "Trẻ em 40.000 đồng.", "Trẻ em 40.000 đồng [1]."
KHO = SimpleNamespace(source="travel/tickets/x.md")
LICH = SimpleNamespace(source=v2.NGUON_LICH_SOURCE)
THUONG_CO_LICH = {"n_hanh_dong": 0, "khan_cap": False}   # thứ đường thường của cuộc có lịch để lại ở `trace.sua`


def test_switch_defaults_off_in_code_and_is_open_in_settings():
    # Code default stays off; settings.yaml opened it 22/11/2026 after the real-run retry met its pre-written criteria.
    assert AssistantFlags().nho_dap_cuoc_co_lich is False
    assert load_settings(validate_private_paths=False)["assistant"]["nho_dap_cuoc_co_lich"] is True


@pytest.mark.parametrize("ten, trace, tat, mo", [
    ("hỏi thường trong cuộc có lịch, trích bài kho", AnswerTrace(sua=dict(THUONG_CO_LICH), cited=(KHO,), tools=[{"name": "tim_kho"}, {"name": "lich_dang_co"}]), False, True),
    ("hỏi VỀ lịch: câu trả lời trích nguồn lịch", AnswerTrace(sua=dict(THUONG_CO_LICH), cited=(KHO, LICH), tools=[{"name": "tim_kho"}, {"name": "lich_dang_co"}]), False, False),
    ("lượt sửa lịch thật", AnswerTrace(sua={"n_hanh_dong": 1, "n_ap": 1}, cited=(), tools=[]), False, False),
    ("khẩn cấp trong cuộc có lịch", AnswerTrace(sua={"n_hanh_dong": 0, "khan_cap": True}, cited=(KHO,), tools=[{"name": "tim_kho"}]), False, False),
    ("cuộc có lịch nhưng lượt dùng dự báo", AnswerTrace(sua=dict(THUONG_CO_LICH), cited=(KHO,), tools=[{"name": "thoi_tiet"}, {"name": "lich_dang_co"}]), False, False),
    ("cuộc KHÔNG có lịch, hỏi thường", AnswerTrace(cited=(KHO,), tools=[{"name": "tim_kho"}]), True, True),
    ("cuộc KHÔNG có lịch, lượt dùng khoảng cách", AnswerTrace(cited=(KHO,), tools=[{"name": "khoang_cach"}]), False, False),
])
def test_which_turns_keep_their_answer(ten, trace, tat, mo):
    assert dap_duoc_nho(trace, "success") is tat, ten
    assert dap_duoc_nho(trace, "success", mo_cho_cuoc_co_lich=True) is mo, ten
    assert dap_duoc_nho(trace, "refusal", mo_cho_cuoc_co_lich=True) is False


def test_an_edit_turn_in_between_drops_the_remembered_answer():
    """Lượt sửa lịch xen giữa không được giữ đáp ⇒ ô lịch sử của lượt trước về dòng ghi chú; lượt sau lệnh sửa không còn thấy câu trả lời cũ."""
    kho = ConversationStore(len, chi_dap_lien_truoc=True)
    cid = kho.ensure(None)
    kho.append(cid, "Kể các quán chè ở Huế", "Chè Hẻm, chè Mợ Tôn Đích [1].", ghi_chu="[ghi chú tên nơi]")
    assert kho.history(cid)[-1][1].startswith(NHAN_LOI_TRUOC) and kho.history_khong_dap(cid) is not None
    sua = AnswerTrace(sua={"n_hanh_dong": 1, "n_ap": 1}, answer="Đã bỏ Chợ Đông Ba.", cited=())
    kho.append(cid, "Bỏ Chợ Đông Ba khỏi lịch", "Đã bỏ Chợ Đông Ba." if dap_duoc_nho(sua, "success", mo_cho_cuoc_co_lich=True) else "", ghi_chu="")
    assert all(NHAN_LOI_TRUOC not in dap for _, dap in kho.history(cid)) and kho.history_khong_dap(cid) is None
    assert kho.history(cid)[0] == ("Kể các quán chè ở Huế", "[ghi chú tên nơi]")


class NhoDap(KichBan):
    """Lần gọi trợ lý: đầu vào mang câu trả lời nhớ ⇒ chữ KHÔNG trích nguồn (như lượt đo thật 22/11); không mang ⇒ có `[1]`."""

    def __init__(self, sua=()):
        super().__init__("tro_ly_hue", sua)
        self.thay_dap = []

    async def create(self, **kwargs):
        if loai(kwargs) != "khac":
            return await super().create(**kwargs)
        self.calls.append(kwargs)
        co = NHAN_LOI_TRUOC in chu_gui(kwargs)
        self.thay_dap.append(co)
        output = [message({"answer": KHONG_TRICH if co else CO_TRICH})]
        response = Response.model_validate({"id": f"resp_{next(_ids)}", "created_at": 0, "model": "probe", "object": "response", "output": output,
                                            "parallel_tool_calls": False, "tool_choice": "auto", "tools": [], "usage": USAGE, "status": "completed"})
        if not kwargs.get("stream"):
            return response

        async def events():
            yield ResponseCreatedEvent.model_validate({"type": "response.created", "response": response.model_dump(), "sequence_number": 0})
            yield ResponseTextDeltaEvent.model_validate({"type": "response.output_text.delta", "item_id": output[0]["id"], "output_index": 0,
                                                         "content_index": 0, "delta": output[0]["content"][0]["text"], "sequence_number": 1, "logprobs": []})
            yield ResponseCompletedEvent.model_validate({"type": "response.completed", "response": response.model_dump(), "sequence_number": 2})
        return events()


def _chay(deps, flags, sua=(), cau=CAU):
    responses = NhoDap(sua)
    gen = OpenAIFullCorpusGenerator(client=Client(responses), model="probe")
    trace = AnswerTrace(history=CO_DAP, lich_su_khong_dap=KHONG_DAP)
    trace.lich_luu = copy.deepcopy(lich_2_ngay())

    async def go():
        return [e async for e in answer_turn_stream_parallel(cau, *deps, gen, trace, flags)]
    return trace, asyncio.run(go()), responses


def test_retracted_ordinary_turn_in_a_saved_plan_conversation_is_rerun_once_without_understanding_the_edit_again(deps):
    trace, events, r = _chay(deps, MO)
    assert r.thay_dap == [True, False]                                    # lần đầu thấy câu trả lời nhớ; lần chạy lại thì không
    assert [loai(c) for c in r.calls].count("sua") == 1                   # bước hiểu ý sửa lịch chạy ĐÚNG MỘT lần — lần hai đi thẳng đường thường
    assert trace.citation_error is None and trace.answer == CO_TRICH and trace.tools[-1]["name"] == TEN_CHAY_LAI
    assert [d for k, d in events if k == "thay_chu"] == [""]
    assert trace.lich_luu == lich_2_ngay() and trace.sua == THUONG_CO_LICH  # lịch của cuộc và số đếm của bước hiểu ý lần đầu: trace chính giữ
    lan_hai = [c for c in r.calls if loai(c) == "khac"][-1]
    assert v2.TIEU_DE_NGUON_LICH in chu_gui(lan_hai)                      # lần hai vẫn thấy lịch đã lưu như mọi câu hỏi thường của cuộc đó
    assert dap_duoc_nho(trace, "success", mo_cho_cuoc_co_lich=True) is True       # câu trả lời của lần chạy lại (trích bài kho) được giữ cho lượt kế


def test_switch_off_keeps_the_old_error_in_a_saved_plan_conversation(deps):
    trace, events, r = _chay(deps, TAT)
    assert r.thay_dap == [True] and trace.citation_error is not None and not [e for e in events if e[0] == "thay_chu"]
    assert all(t["name"] != TEN_CHAY_LAI for t in trace.tools)


def test_an_edit_turn_is_never_rerun(deps):
    """Lần đầu là lượt SỬA lịch (model hiểu là "thay điểm" thiếu điểm mới ⇒ thẻ chọn) ⇒ không chạy lại, lịch không bị đụng lần hai."""
    trace, events, r = _chay(deps, MO, sua=[{"loai": "thay_diem", "ten": "Đầm Chuồn"}], cau="Thay Đầm Chuồn bằng chỗ khác")
    assert trace.fixed_outcome == "sua_the" and [loai(c) for c in r.calls].count("sua") == 1
    assert all(t["name"] != TEN_CHAY_LAI for t in trace.tools) and not [e for e in events if e[0] == "thay_chu"]


def test_an_edit_turn_leaves_its_code_written_result_lines_for_the_next_turn():
    """Đo 23/11/2026: "bỏ giúp mình điểm đầu tiên của ngày 2" rồi hỏi "Vậy ngày 2 giờ còn những điểm nào?" — lượt kế thấy câu LỆNH (ô đáp rỗng) cạnh lịch ĐÃ sửa
    nên áp lệnh thêm một lần trong đầu và cãi thẻ lịch (2 / 3 lần trên model đang chạy, 1 / 1 trên model cũ). Ô lịch sử của lượt sửa nay mang các dòng do CODE
    viết ở đầu thẻ ("Đã bỏ X."); chữ thẻ lịch — có tên quán lấy từ bản đồ mở — vẫn không vào lịch sử. Lệnh hiểu ý + bộ áp chạy thật, chỉ model là đồ giả."""
    from api.conversations import GHI_CHU_SUA_DAU
    from api.routes.chat import _remember
    from llm import sua_lich_v2 as s
    from llm.ten_goi_y import lich_su_cho_luot
    from test_sua_lich_kem_hoi import _bo, _chay, _co
    from test_sua_lich_v2 import B

    cau = "Mai có bão vào Huế, bỏ giúp mình điểm đầu tiên của ngày 1"
    k, kq, tr, _ = _chay(lambda k: [_bo(k)], _co(), cau)
    ten = B.theo_id[sorted(s._vi_tri(k))[0]]["ten"]
    assert kq is not None and tr.sua_dong == tuple(d["cau"] for d in s.thay_doi(B, kq)) and tr.sua_dong[0].startswith(f"Đã bỏ {ten}")
    tr.answer, tr.lich_v2 = "Ngày 1 — buổi sáng … Ăn trưa gần đó: Quán Bịa Từ Bản Đồ Mở.", {"lich": {}}  # chữ thẻ lịch của lượt sửa
    kho = ConversationStore(len, chi_dap_lien_truoc=True)
    cid = kho.ensure(None)
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(conversations=kho, assistant_flags=MO)))
    _remember(request, cid, cau, tr, "success")
    (hoi, dap), = kho.history(cid)
    assert hoi == cau and dap == f"{GHI_CHU_SUA_DAU}{' '.join(tr.sua_dong)}]"
    assert "Quán Bịa" not in dap and NHAN_LOI_TRUOC not in dap and kho.history_khong_dap(cid) is None  # không chữ thẻ, không phải "đáp được nhớ"
    # lượt kế nhận đúng ô đó — kể cả câu xin liệt kê lại (luật bỏ dòng ghi chú TÊN NƠI không đụng dòng này); có lượt mới thì ô vẫn ở lại
    assert lich_su_cho_luot(kho.history(cid), "Vậy ngày 1 giờ còn những điểm nào?") == ((cau, dap),)
    assert lich_su_cho_luot(kho.history(cid), "Liệt kê các điểm đó") == ((cau, dap),)
    kho.append(cid, "Vậy ngày 1 giờ còn những điểm nào?", "Còn hai điểm [1].", ghi_chu="")
    assert kho.history(cid)[0] == (cau, dap)
    # đối chứng: lượt hỏi thường không có dòng sửa ⇒ ô lịch sử y như trước (đáp được nhớ, không dòng ghi chú sửa)
    thuong = AnswerTrace(sua=dict(THUONG_CO_LICH), cited=(), tools=[{"name": "tim_kho"}], answer="Vé 200.000 đồng [1].")
    _remember(request, cid, "Vé Đại Nội bao nhiêu?", thuong, "success")
    assert kho.history(cid)[-1] == ("Vé Đại Nội bao nhiêu?", f"{NHAN_LOI_TRUOC}\nVé 200.000 đồng.") and thuong.sua_dong == ()
