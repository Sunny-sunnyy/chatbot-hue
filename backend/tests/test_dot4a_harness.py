"""Unit test 0 USD cho 3 cơ chế tối ưu Đợt 4A (`kiem_du_bang_chung`, `canh_bao_vong_con_lai`, `toi_uu_dot2_va_viet_lai`)."""
import asyncio
import copy
import datetime as dt
import json

import pytest

from core.settings_loader import load_settings
from llm import khoang_cach as kc
from llm import lich_trinh_v2 as lt2
from llm import liet_ke as lk
from llm import thoi_tiet as tt
from llm.assistant import TEN_VIET_LAI, AnswerTrace, AssistantFlags, _lich_extra, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import (
    ANSWER_SYSTEM_INSTRUCTIONS,
    ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y,
    ASSISTANT_HISTORY_NOTE,
    INSUFFICIENT_ANSWER,
    KIEM_DU_BANG_CHUNG_NOTE,
    TOOL_LIMIT_TEXT,
    VIET_LAI_NHIEU_Y_TEXT,
)
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401
from test_cong_dot_1 import SETTINGS, form_trace, run, viet_theo_khung
from test_het_luot_tim import sent_requests, tools_sent
from test_het_luot_viet_lai import GIU_CHO, CO_NGUON, kich_ban
from test_liet_ke_bai import MUC_LUC, goi_liet_ke
from test_vong_cuoi_chi_viet import tool_outputs

NEW_FLAGS = ("kiem_du_bang_chung", "canh_bao_vong_con_lai", "toi_uu_dot2_va_viet_lai")


def _bang_v2_va_kc(tmp_path):
    diem = (
        {
            "id": "dai_noi",
            "ten": "Đại Nội Huế",
            "cum": "kinh_thanh",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "nua_buoi",
            "trong_nha": "ngoai_troi",
            "bac_thang": "it",
            "uu_tien": {"chung": 1},
            "nguon": "heritages/heritage/Đại Nội Huế.md",
            "toi_nhe": False,
        },
        {
            "id": "bao_tang_co_vat",
            "ten": "Bảo tàng Cổ vật Cung đình Huế",
            "cum": "kinh_thanh",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "ngan",
            "trong_nha": "trong_nha",
            "bac_thang": "it",
            "uu_tien": {"chung": 2},
            "nguon": "heritages/heritage/Bảo tàng Cổ vật Cung đình Huế.md",
            "toi_nhe": False,
        },
    )
    bang_v2 = lt2.BangV2(
        diem=diem,
        theo_id={d["id"]: d for d in diem},
        cum={"kinh_thanh": "Kinh Thành"},
        uu_tien=("chung",),
        loai_hien=(),
        nhac_mua_chung="",
        toi_nhe=(),
        thu_tu_toi=(),
    )
    (tmp_path / "kc.json").write_text(json.dumps({"cap": {"dai_noi|bao_tang_co_vat": {"km": 0.6, "phut": 3}}}), encoding="utf-8")
    (tmp_path / "diem.json").write_text(
        json.dumps({"diem": [{"id": "dai_noi", "ten": "Đại Nội Huế"}, {"id": "bao_tang_co_vat", "ten": "Bảo tàng Cổ vật Cung đình Huế"}]}),
        encoding="utf-8",
    )
    bang_kc = kc.nap_bang(tmp_path / "kc.json", tmp_path / "diem.json")

    async def du_bao():
        hom = dt.date(2026, 11, 27)
        return tt.DuBao(
            trang_thai="ok",
            ngay=[{"ngay": hom, "tmin": 22, "tmax": 28, "mua": 5.0, "xs": 60}],
            cap_nhat="10:00 27/11",
            ms=1.0,
            tu_cache=True,
        )

    return bang_v2, bang_kc, du_bao


def test_dot4a_flags_default_off_in_code_and_settings():
    defaults = AssistantFlags()
    for key in NEW_FLAGS:
        assert getattr(defaults, key) is False
    settings = load_settings(validate_private_paths=False)
    for key in NEW_FLAGS:
        assert settings["assistant"][key] is False
    loaded = AssistantFlags.from_settings(settings)
    for key in NEW_FLAGS:
        assert getattr(loaded, key) is False


def test_all_new_flags_off_keep_byte_identical_requests_and_tool_list(deps, tmp_path):
    """(i) Cả 3 công tắc tắt: chuỗi gửi model & danh sách tool giống byte qua mọi loại lượt."""
    bang_v2, bang_kc, du_bao = _bang_v2_va_kc(tmp_path)
    base_kwargs = dict(
        tim_them=True,
        het_luot_bo_cong_cu=True,
        het_luot_viet_lai=True,
        cau_nhieu_y=True,
        thoi_tiet=True,
        du_bao=du_bao,
        khoang_cach=True,
        khoang_cach_bang=bang_kc,
        bang_lich_v2=bang_v2,
        goi_y_mua_nang=True,
        so_sanh_diem_den=True,
        cong_cong_cu="linh_hoat",
    )
    flags_default = AssistantFlags(**base_kwargs)
    flags_explicit_off = AssistantFlags(
        **base_kwargs,
        kiem_du_bang_chung=False,
        canh_bao_vong_con_lai=False,
        toi_uu_dot2_va_viet_lai=False,
    )

    scenarios = [
        ("Đại Nội Huế ở đâu?", (), lambda n, kw: [tool_call("Đại Nội")] if n == 1 else [answer("Ở Huế [1].")]),
        ("Còn giá vé thì sao?", (("Đại Nội ở đâu?", "Ở Huế."),), lambda n, kw: [answer("Giá vé [1].")]),
        ("Đại Nội ở đâu và mở cửa mấy giờ?", (), kich_ban()),
    ]
    for query, history, script in scenarios:
        gen_a, gen_b = generator(script), generator(script)
        asyncio.run(answer_turn(query, *deps, gen_a, AnswerTrace(history=history), flags_default))
        asyncio.run(answer_turn(query, *deps, gen_b, AnswerTrace(history=history), flags_explicit_off))
        assert sent_requests(gen_a) == sent_requests(gen_b)


@pytest.mark.parametrize("stream", [False, True])
def test_kiem_du_bang_chung_by_turn_type_first_history_multipart_and_form(deps, monkeypatch, stream):
    """(ii) kiem_du_bang_chung cho lượt đầu, lượt lịch sử, lượt nhiều ý (tool + không tool) và không vào lượt biểu mẫu."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    base = load_settings(validate_private_paths=False)
    s_off = copy.deepcopy(base)
    s_off["full_corpus_generation"]["provider"] = "openai"
    s_on = copy.deepcopy(s_off)
    s_on["assistant"]["kiem_du_bang_chung"] = True

    gen_off = OpenAIFullCorpusGenerator.from_environment(s_off)
    gen_on = OpenAIFullCorpusGenerator.from_environment(s_on)
    assert KIEM_DU_BANG_CHUNG_NOTE not in gen_off.answer_agent.instructions
    assert KIEM_DU_BANG_CHUNG_NOTE in gen_on.answer_agent.instructions
    assert KIEM_DU_BANG_CHUNG_NOTE in gen_on.assistant_agent.instructions
    assert KIEM_DU_BANG_CHUNG_NOTE in gen_on.assistant_history_agent.instructions
    assert KIEM_DU_BANG_CHUNG_NOTE in gen_on.assistant_agent_nhieu_y.instructions
    assert KIEM_DU_BANG_CHUNG_NOTE in gen_on.assistant_history_agent_nhieu_y.instructions
    assert KIEM_DU_BANG_CHUNG_NOTE not in gen_on.bieu_mau_agent.instructions

    # Kiểm qua luồng chạy thật (dù generator gốc khởi tạo mặc định tắt -> flags runtime vẫn bật đúng)
    for use_tools in (False, True):
        for query, history, is_multi in [
            ("Đại Nội Huế có chỗ gửi xe ô tô qua đêm không?", (), False),
            ("Còn giờ mở cửa ngày Tết thì sao?", (("Đại Nội ở đâu?", "Ở Huế."),), False),
            ("Đại Nội ở đâu và giá vé cho thú cưng thế nào?", (), True),
        ]:
            flags_off = AssistantFlags(tim_them=use_tools, cau_nhieu_y=True, kiem_du_bang_chung=False)
            flags_on = AssistantFlags(tim_them=use_tools, cau_nhieu_y=True, kiem_du_bang_chung=True)

            def run_one(flags):
                gen = generator(lambda n, kw: [answer("Thông tin [1].")])
                trace = AnswerTrace(history=history)
                if stream:
                    async def go():
                        return [e async for e in answer_turn_stream(query, *deps, gen, trace, flags)]
                    asyncio.run(go())
                else:
                    asyncio.run(answer_turn(query, *deps, gen, trace, flags))
                return gen.client.responses.calls[0]["instructions"]

            instr_off = run_one(flags_off)
            instr_on = run_one(flags_on)
            assert KIEM_DU_BANG_CHUNG_NOTE not in instr_off
            assert KIEM_DU_BANG_CHUNG_NOTE in instr_on
            if history and use_tools:
                assert ASSISTANT_HISTORY_NOTE in instr_on
            if is_multi and use_tools:
                assert "Tư liệu chưa có thông tin về:" in instr_on

    # Lượt biểu mẫu giữ nguyên byte kể cả khi bật kiem_du_bang_chung
    s_form_off = copy.deepcopy(SETTINGS)
    s_form_off["assistant"].update(lich_trinh_bieu_mau=True, kiem_du_bang_chung=False)
    s_form_on = copy.deepcopy(SETTINGS)
    s_form_on["assistant"].update(lich_trinh_bieu_mau=True, kiem_du_bang_chung=True)
    gen_f_off = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
    gen_f_on = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
    q_f, tr_f_off = form_trace({"so_ngay": "2", "di_cung": "cap_doi"})
    _, tr_f_on = form_trace({"so_ngay": "2", "di_cung": "cap_doi"})
    run(deps, q_f, gen_f_off, AssistantFlags.from_settings(s_form_off), tr_f_off)
    run(deps, q_f, gen_f_on, AssistantFlags.from_settings(s_form_on), tr_f_on)
    assert sent_requests(gen_f_off) == sent_requests(gen_f_on)


@pytest.mark.parametrize("stream", [False, True])
def test_canh_bao_vong_con_lai_keeps_tool_prefix_fixed_and_appends_reminder_tail(deps, stream):
    """(ii) canh_bao_vong_con_lai: giữ nguyên mảng tools cố định (không rút tim_kho/liet_ke_bai) và nối <nhac_vong> cuối output khi còn <= 2 bước."""
    flags_on = AssistantFlags(
        tim_them=True,
        het_luot_bo_cong_cu=True,
        liet_ke_bai=True,
        muc_luc=MUC_LUC,
        canh_bao_vong_con_lai=True,
    )
    # so_vong = 5 (4 + 1 cho liet_ke_bai):
    # - Call 1 -> tim_kho #1 (calls=1, con_lai=4 > 2) -> KHÔNG <nhac_vong>
    # - Call 2 -> liet_ke_bai #1 (calls=2, con_lai=3 > 2) -> KHÔNG <nhac_vong>
    # - Call 3 -> tim_kho #2 (calls=3, con_lai=2 <= 2) -> CÓ <nhac_vong>
    # - Call 4 -> tim_kho #3 (calls=4, con_lai=1 <= 2, vượt so_lan_tim_kho=2) -> trả TOOL_LIMIT_TEXT + <nhac_vong>, vẫn KHÔNG rơi lỗi
    # - Call 5 -> trả lời có nguồn [1]
    def script(n, kw):
        if n == 1:
            return [tool_call("Huế vòng 1")]
        if n == 2:
            return [goi_liet_ke("quan_an", ("bún",))]
        if n in (3, 4):
            return [tool_call(f"Huế vòng {n}")]
        return [answer("Có thông tin [1].")]

    gen = generator(script)
    trace = AnswerTrace()
    if stream:
        async def go():
            return [e async for e in answer_turn_stream("Huế có quán gì ngon?", *deps, gen, trace, flags_on)]
        asyncio.run(go())
    else:
        asyncio.run(answer_turn("Huế có quán gì ngon?", *deps, gen, trace, flags_on))

    assert trace.fixed_outcome is None and trace.citation_error is None and trace.answer == "Có thông tin [1]."
    # Mảng tools schema ở cả 5 lần gọi giữ cố định 100% (không rút tim_kho hay liet_ke_bai bằng is_enabled)
    sent_tools = tools_sent(gen)
    assert len(sent_tools) == 5 and all(names == ["tim_kho", "liet_ke_bai"] for names in sent_tools)
    schemas = [kw.get("tools") for kw in gen.client.responses.calls]
    assert all(s == schemas[0] for s in schemas)

    outs = tool_outputs(gen, 5)
    assert len(outs) == 4
    assert "<nhac_vong>" not in outs[0]
    assert "<nhac_vong>" not in outs[1]
    assert outs[2].endswith("</nhac_vong>") and "Còn 2 lượt" in outs[2]
    assert TOOL_LIMIT_TEXT in outs[3] and outs[3].endswith("</nhac_vong>") and "Còn 1 lượt cuối" in outs[3]


def test_toi_uu_dot2_va_viet_lai_actionable_feedback_by_turn_type(deps):
    """(ii) Actionable Feedback khi viết lại lỗi citation (một ý & nhiều ý; không chạm _cuu_max_turns)."""
    flags_off = AssistantFlags(lan_tim_dau="v2", cau_nhieu_y=True, het_luot_viet_lai=True, toi_uu_dot2_va_viet_lai=False)
    flags_on = AssistantFlags(lan_tim_dau="v2", cau_nhieu_y=True, het_luot_viet_lai=True, toi_uu_dot2_va_viet_lai=True)

    # 1) Tin một ý: bật -> chẩn đoán lỗi citation vào prompt viết lại; tắt -> không có
    gen_off = generator(kich_ban())
    asyncio.run(answer_turn("Huế có món gì ngon?", *deps, gen_off, AnswerTrace(), flags_off))
    assert "bản nháp trước trượt kiểm" not in str(gen_off.client.responses.calls[3]["input"])

    gen_on = generator(kich_ban())
    trace_on = AnswerTrace()
    asyncio.run(answer_turn("Huế có món gì ngon?", *deps, gen_on, trace_on, flags_on))
    rewrite_input = str(gen_on.client.responses.calls[3]["input"])
    assert "bản nháp trước trượt kiểm: chưa gắn mã nguồn [n]" in rewrite_input
    assert f"[1]..[{len(trace_on.so_nguon)}]" in rewrite_input
    assert VIET_LAI_NHIEU_Y_TEXT not in rewrite_input
    assert trace_on.tools[-1]["name"] == TEN_VIET_LAI and trace_on.answer == CO_NGUON

    # 2) Tin nhiều ý: có cả VIET_LAI_NHIEU_Y_TEXT lẫn chẩn đoán lỗi citation
    gen_ny = generator(kich_ban())
    asyncio.run(answer_turn("Vé vào Đại Nội giá bao nhiêu, mở cửa mấy giờ?", *deps, gen_ny, AnswerTrace(), flags_on))
    rewrite_ny = str(gen_ny.client.responses.calls[3]["input"])
    assert VIET_LAI_NHIEU_Y_TEXT in rewrite_ny and "bản nháp trước trượt kiểm: chưa gắn mã nguồn [n]" in rewrite_ny

    # 3) _cuu_max_turns (chạm trần vòng, không có citation_error) -> không chèn chẩn đoán citation_error
    flags_cuu = AssistantFlags(tim_them=True, cuu_max_turns=True, toi_uu_dot2_va_viet_lai=True)
    gen_cuu = generator(lambda n, kw: [tool_call(f"Huế {n}")] if kw.get("tools") else [answer("Có thông tin [1].")])
    trace_cuu = AnswerTrace()
    asyncio.run(answer_turn("Huế có gì?", *deps, gen_cuu, trace_cuu, flags_cuu))
    assert trace_cuu.cuu_max_turns == {"thanh_cong": True}
    assert "bản nháp trước trượt kiểm" not in str(gen_cuu.client.responses.calls[-1]["input"])


def test_toi_uu_dot2_dedup_mua_nang_in_linh_hoat_mode(tmp_path):
    """(ii) Chế độ linh_hoat + toi_uu_dot2_va_viet_lai: khử lặp bảng 47 điểm ở mua_nang và giữ Tool Use Examples."""
    bang_v2, bang_kc, du_bao = _bang_v2_va_kc(tmp_path)
    gen = OpenAIFullCorpusGenerator(client=object(), model="x")

    async def fake_tim_kho(cau: str) -> str:
        return cau

    base = dict(
        tim_them=True,
        thoi_tiet=True,
        du_bao=du_bao,
        khoang_cach=True,
        khoang_cach_bang=bang_kc,
        bang_lich_v2=bang_v2,
        goi_y_mua_nang=True,
        so_sanh_diem_den=True,
        cong_cong_cu="linh_hoat",
    )
    extra_off = _lich_extra("Trời mưa nên đi đâu?", None, None, AnswerTrace(), None, None, AssistantFlags(**base, toi_uu_dot2_va_viet_lai=False))
    ag_off, _, _ = gen._assistant_for(fake_tim_kho, **extra_off)
    by_off = {t.name: t for t in ag_off.tools}
    assert "Mã điểm:" in (by_off["goi_y_phuong_an_mua_nang"].description or "")
    assert "Ví dụ gọi mẫu:" not in (by_off["goi_y_phuong_an_mua_nang"].description or "")
    assert "Ví dụ gọi mẫu:" not in (by_off["so_sanh_diem_den"].description or "")

    extra_on = _lich_extra("Trời mưa nên đi đâu?", None, None, AnswerTrace(), None, None, AssistantFlags(**base, toi_uu_dot2_va_viet_lai=True))
    ag_on, _, _ = gen._assistant_for(fake_tim_kho, **extra_on)
    by_on = {t.name: t for t in ag_on.tools}
    mn_desc = by_on["goi_y_phuong_an_mua_nang"].description or ""
    ss_desc = by_on["so_sanh_diem_den"].description or ""
    assert "Mã điểm:" not in mn_desc and "khoang_cach" in mn_desc and "Ví dụ gọi mẫu:" in mn_desc
    assert "Mã điểm:" not in ss_desc and "khoang_cach" in ss_desc and "Ví dụ gọi mẫu:" in ss_desc
    assert (ag_on.model_settings.extra_args or {}).get("prompt_cache_key") == "hue_assistant_lh_v1_d2"
