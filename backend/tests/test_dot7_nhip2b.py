"""Unit test offline (0 USD) cho Đợt 7 Nhịp 2B (Mũi 2.1: H2.1a P_GPT6 + H2.1b CIT_CAU & đồng bộ stream/non-stream)."""
from __future__ import annotations

import asyncio
from types import SimpleNamespace

from core.schema import RetrievedDocument
from core.settings_loader import load_settings
from llm import full_corpus_prompt as fp
from llm import thoi_tiet as tt
from llm.assistant import (
    AnswerTrace,
    AssistantFlags,
    answer_query,
    answer_turn_stream,
    tool_for_turn,
)
from llm.citations import check_sentence_citations, split_sentences_vi
from llm.generator_openai_full_corpus import GeneratedText
from retrieval.full_corpus_context import PackedSource


def _packed_src(sid: int = 1, text: str = "Đại Nội mở cửa từ 7h00 đến 17h30, giá vé 200.000 đồng.") -> PackedSource:
    return PackedSource(
        id=sid,
        title="Đại Nội Huế",
        heading_path=("Giờ mở cửa",),
        excerpts=(text,),
        source="heritages/dai_noi.md",
    )


def test_h21a_gpt6_prompts_va_docstring_tim_kho():
    assert fp.ANSWER_SYSTEM_INSTRUCTIONS.count(fp._LUAT_TU_CHOI) == 1
    assert fp.ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y == fp.ANSWER_SYSTEM_INSTRUCTIONS.replace(fp._LUAT_TU_CHOI, fp._LUAT_NHIEU_Y)
    assert "xuất đúng duy nhất câu sau" in fp.ANSWER_SYSTEM_INSTRUCTIONS
    assert "không suy vượt cận số hay mốc năm ngoài Bằng chứng" in fp.ANSWER_SYSTEM_INSTRUCTIONS
    assert "Công cụ tim_kho(cau_tim)" in fp.ASSISTANT_TOOL_NOTE

    tr = AnswerTrace()
    fn = tool_for_turn("Giờ mở cửa Đại Nội?", None, None, tr, None, fp.ANSWER_SYSTEM_INSTRUCTIONS)
    assert (fn.__doc__ or "").startswith(fp.TIM_KHO_MO_TA)


def test_cit_cau_bien_tieng_viet_va_bo_qua_khoi_he_thong():
    # 1. Dấu chấm đặt TRƯỚC [2][8]
    r_dot = check_sentence_citations("Chùa có kiến trúc gỗ sơn đỏ. [2][8] Ba tầng tiếp theo được xây bằng gạch [3].")
    assert r_dot["passed"] is True and r_dot["missing_count"] == 0

    # 2. Viết tắt TAN. CAFE không bị tách câu
    r_abbr = check_sentence_citations("Quán TAN. CAFE nằm ở trung tâm Huế [1].")
    assert r_abbr["passed"] is True and r_abbr["total_sentences"] == 1

    # 3. Câu chốt ngắn ('Có.' / 'Không.') trước câu có [n] cùng dòng được miễn
    r_verdict = check_sentence_citations("Có. Đại Nội mở cửa hằng ngày từ 7h00 [1].\nKhông hẳn. Giờ tối chỉ mở một số dịp [2].")
    assert r_verdict["passed"] is True and len(r_verdict["exempted"]) == 2
    assert all(e["reason"] == "short_verdict" for e in r_verdict["exempted"])

    # 4. Tiêu đề, CAU_Y_THIEU và khối thời tiết / CAU_DAU_BAO_LU được bỏ qua
    text_blocks = (
        f"{tt.CAU_DAU_BAO_LU}\n\n"
        "## Giờ tham quan\n"
        "**Thông tin chung:**\n"
        "Đại Nội mở cửa lúc 7h00 [1].\n"
        f"{fp.CAU_Y_THIEU} giá vé gửi xe.\n\n"
        "**Dự báo thời tiết Huế**\n- Thứ Bảy: 25 °C\n\n"
        "Với bão, lũ, ngập: theo dõi bản tin chính thức."
    )
    r_blocks = check_sentence_citations(text_blocks)
    assert r_blocks["passed"] is True and len(split_sentences_vi(text_blocks)) == 1

    # 5. Phát hiện đúng câu nhận định thiếu [n]
    r_miss = check_sentence_citations("Vé lẻ giá 200.000 đồng. Giờ mở cửa từ 7h00 [1].")
    assert r_miss["passed"] is False and r_miss["missing_count"] == 1
    assert "200.000" in r_miss["missing_sentences"][0]["text"]


def _make_nonstream_env(first_text: str, rewrite_text: str | Exception):
    src = _packed_src(1)
    doc = RetrievedDocument(
        id="doc1",
        text="Đại Nội mở cửa từ 7h00 đến 17h30, giá vé 200.000 đồng.",
        score=1.0,
        metadata={"source": src.source, "title": src.title, "heading_path": ["Giờ mở cửa"], "evidence_parts": []},
    )
    rewrite_calls = []

    class FakeGen:
        model = "gpt-6-luna"
        assistant_instructions = fp.ANSWER_SYSTEM_INSTRUCTIONS

        async def generate_with_tools(self, tool_prompt, tool_fn, call_log, **extra):
            return GeneratedText(first_text, None, "gpt-6-luna", 100, 20, 120, 10.0)

        async def generate_answer(self, query, context, **kwargs):
            rewrite_calls.append(context)
            if isinstance(rewrite_text, Exception):
                raise rewrite_text
            return GeneratedText(rewrite_text, None, "gpt-6-luna", 100, 20, 120, 10.0)

    tr = AnswerTrace(
        so_nguon=[src],
        documents=[doc],
        context_parts=["[Nguồn 1] Đại Nội mở cửa từ 7h00 đến 17h30, giá vé 200.000 đồng."],
    )
    return FakeGen(), tr, rewrite_calls


def test_h21b_viet_lai_nonstream_va_giu_ban_goc_khi_loi_hoac_tu_choi():
    s = load_settings(validate_private_paths=False)
    assert s["assistant"]["kiem_trich_dan_cau"] is True
    assert AssistantFlags().kiem_trich_dan_cau is False

    q = "Đại Nội mở cửa mấy giờ và giá vé bao nhiêu?"
    draft = "Đại Nội mở cửa từ 7h00 đến 17h30. Giá vé 200.000 đồng [1]."

    # 1. Cờ tắt -> không kích hoạt cit_cau_viet_lai
    gen_off, tr_off, rw_off = _make_nonstream_env(draft, "x [1].")
    flags_off = AssistantFlags(lan_tim_dau="v2", kiem_trich_dan_cau=False)
    asyncio.run(answer_query(q, None, None, gen_off, tr_off, None, None, flags_off))
    assert tr_off.answer == draft and not rw_off

    # 2. Cờ bật -> gọi viết lại 1 lần với phản hồi định hướng, sửa đủ [1] ở cả 2 câu
    gen_ok, tr_ok, rw_ok = _make_nonstream_env(draft, "Đại Nội mở cửa từ 7h00 đến 17h30 [1]. Giá vé 200.000 đồng [1].")
    flags_on = AssistantFlags(lan_tim_dau="v2", kiem_trich_dan_cau=True)
    asyncio.run(answer_query(q, None, None, gen_ok, tr_ok, None, None, flags_on))
    assert len(rw_ok) == 1 and "chưa gắn mã nguồn [n]" in rw_ok[0]
    assert tr_ok.answer == "Đại Nội mở cửa từ 7h00 đến 17h30 [1]. Giá vé 200.000 đồng [1]."
    entry_ok = next(t for t in tr_ok.tools if t["name"] == "cit_cau_viet_lai")
    assert entry_ok["restored"] is False and entry_ok["after_passed"] is True

    # 3. Bản viết lại biến thành từ chối (INSUFFICIENT_ANSWER) -> khôi phục nguyên bản gốc có trích dẫn
    gen_ref, tr_ref, _ = _make_nonstream_env(draft, fp.INSUFFICIENT_ANSWER)
    asyncio.run(answer_query(q, None, None, gen_ref, tr_ref, None, None, flags_on))
    assert tr_ref.answer == draft and tr_ref.citation_error is None
    entry_ref = next(t for t in tr_ref.tools if t["name"] == "cit_cau_viet_lai")
    assert entry_ref["restored"] is True and entry_ref["tu_choi"] is True

    # 4. Bản viết lại trích mã nguồn lạ -> khôi phục nguyên bản gốc có trích dẫn
    gen_bad, tr_bad, _ = _make_nonstream_env(draft, "Đại Nội mở cửa từ 7h00 [99].")
    asyncio.run(answer_query(q, None, None, gen_bad, tr_bad, None, None, flags_on))
    assert tr_bad.answer == draft and tr_bad.citation_error is None
    assert next(t for t in tr_bad.tools if t["name"] == "cit_cau_viet_lai")["restored"] is True

    # 5. Bão/lũ hoặc làm thay hoặc có lịch -> KHÔNG kích hoạt
    gen_bao, tr_bao, rw_bao = _make_nonstream_env(draft, "x [1].")
    asyncio.run(answer_query("Bão lũ thì Đại Nội mở cửa không?", None, None, gen_bao, tr_bao, None, None, flags_on))
    assert not rw_bao


def test_h21b_stream_cho_kiem_va_stream_thay_chu():
    src = _packed_src(1)
    q = "Đại Nội mở cửa mấy giờ và giá vé bao nhiêu?"
    draft = "Đại Nội mở cửa từ 7h00 đến 17h30. Giá vé 200.000 đồng [1]."
    rewritten = "Đại Nội mở cửa từ 7h00 đến 17h30 [1]. Giá vé 200.000 đồng [1]."

    def _run(giu_chu_toi_kiem: bool, chu_ve_mot_lan: bool, rewrite_out: str):
        class FakeStreamGen:
            model = "gpt-6-luna"
            timeout = 5
            max_turns = 5
            assistant_instructions = fp.ANSWER_SYSTEM_INSTRUCTIONS

            def __init__(self):
                self.chu_ve_mot_lan = chu_ve_mot_lan

            def start_tools_stream(self, tool_prompt, tool_fn, **extra):
                async def _events():
                    yield SimpleNamespace(
                        type="raw_response_event",
                        data=SimpleNamespace(type="response.output_text.delta", delta=f'{{"answer":{draft!r}}}'.replace("'", '"')),
                    )

                return SimpleNamespace(stream_events=_events, cancel=lambda: None), SimpleNamespace(calls=[]), {}

            def finish_answer_stream(self, result, call_log, started, state):
                return GeneratedText(draft, None, "gpt-6-luna", 100, 20, 120, 10.0)

            async def generate_answer(self, query, context, **kwargs):
                return GeneratedText(rewrite_out, None, "gpt-6-luna", 100, 20, 120, 10.0)

        tr = AnswerTrace(so_nguon=[src], context_parts=["[Nguồn 1] Đại Nội mở cửa từ 7h00 đến 17h30, giá vé 200.000 đồng."])
        flags = AssistantFlags(lan_tim_dau="v2", kiem_trich_dan_cau=True, giu_chu_toi_kiem=giu_chu_toi_kiem)

        async def _go():
            return tr, [ev async for ev in answer_turn_stream(q, None, None, FakeStreamGen(), tr, flags)]

        return asyncio.run(_go())

    # 1. cho_kiem (giu_chu_toi_kiem=True + chu_ve_mot_lan=True): chỉ phát bản viết lại, không lộ draft
    tr1, ev1 = _run(True, True, rewritten)
    deltas1 = "".join(d for k, d in ev1 if k == "delta")
    assert tr1.answer == rewritten and deltas1 == rewritten
    assert not [e for e in ev1 if e[0] == "thay_chu"]

    # 2. cho_kiem nhưng bản viết lại từ chối -> phát lại đúng bản gốc hợp lệ
    tr2, ev2 = _run(True, True, fp.INSUFFICIENT_ANSWER)
    deltas2 = "".join(d for k, d in ev2 if k == "delta")
    assert tr2.answer == draft and deltas2 == draft

    # 3. Stream thường (giu_chu_toi_kiem=False): phát `thay_chu` với bản viết lại
    tr3, ev3 = _run(False, False, rewritten)
    assert tr3.answer == rewritten
    assert ("thay_chu", rewritten) in ev3
