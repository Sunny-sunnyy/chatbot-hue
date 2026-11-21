"""Công cụ `liet_ke_bai` (cờ `assistant.liet_ke_bai`, plan `report_agent/2026-11-21/b_cong_cu_liet_ke_plan.md`) — 0 USD.

Vì sao: câu xin danh sách và câu "nơi nào có đặc điểm X" cần chạm nhiều BÀI, bước tìm chỉ trả 10 đoạn (đếm 21/11: lăng 2 / 8 bài, lễ hội 0 / 39).
File này kiểm: hàm lọc thuần (bài dựng tay — không chép chữ của kho) · mục lục nạp từ kho thật có đủ bài · công cụ của một lượt đăng đúng MỘT nguồn trích được
· cờ tắt gửi model giống byte, cờ bật chỉ thêm đúng một công cụ ở mọi kiểu lượt. Model là `OpenAIResponsesModel` thật của SDK với phản hồi dựng sẵn; tìm kho là
Qdrant thật (chỉ đọc). Model thật có gọi công cụ đúng lúc không là lượt đo có phí ghi ở report của nhánh.
"""
import asyncio
import json
import re

import pytest

from core.settings_loader import load_settings
from ingestion.source_state import discover_full_corpus_files
from llm import liet_ke as lk
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream, liet_ke_for_turn
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import ASSISTANT_MAX_TURNS, max_turns_for
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)
from test_het_luot_tim import CAU, sent_requests, tools_sent, turn

BAI = {
    "foods/restaurants/quan-a.md": "# Quán Bún A\n\n## Tóm tắt\nLoại hình: quán bún bò.\n\n## Dịch vụ\n- Nhận **hút chân không** mang về.\n- Mở cửa 06:00 – 08:00.",
    "foods/restaurants/quan-b.md": "# Quán Cơm B\n\n## Tóm tắt\nQuán cơm bình dân gần chợ.\n\n## Lưu ý\nQuán KHÔNG nhận hút chân không.",
    "foods/restaurants/quan-c.md": "# Quán Chè C\n\n## Tóm tắt\nLoại hình: quán chè.\n\n## Món\nChè bột lọc, chè hạt sen.",
    "foods/cafes/ca-phe-d.md": "# Cà phê D\n\nKhông gian yên tĩnh, có chỗ gửi xe.",
    "heritages/heritage/lang-e.md": "# Lăng E\n\n## Tóm tắt\nLăng của một vị vua triều Nguyễn.\n\n## Lịch sử\nTrước đây khu này từng là quán nước cho lính canh; nay không còn hàng quán.",
    "travel/cam-nang.md": "# Cẩm nang đi lại\n\nĐi xe máy là tiện nhất.",
}
MUC_LUC = tuple(sorted((lk.bai_tu_markdown(rel, md) for rel, md in BAI.items()), key=lambda b: lk.chuan(b.tieu_de)))
OFF = AssistantFlags(tim_them=True)
ON = AssistantFlags(tim_them=True, liet_ke_bai=True, muc_luc=MUC_LUC)


def goi_liet_ke(nhom: str, cum_tu: list[str]) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "liet_ke_bai",
            "arguments": json.dumps({"nhom": nhom, "cum_tu": cum_tu}, ensure_ascii=False), "status": "completed"}


def ket_qua_cong_cu(kw) -> list[str]:
    return [i["output"] for i in kw["input"] if isinstance(i, dict) and i.get("type") == "function_call_output"]


# ---------- hàm lọc thuần ----------

def test_group_is_the_folder_and_no_phrase_lists_the_whole_group_with_its_intro_line():
    kq = lk.loc(MUC_LUC, "quan_an", [])
    assert (kq.tong, kq.o_ten, kq.cum_tu) == (3, 0, ()) and [d.split(" — ")[0] for d in kq.dong] == ["Quán Bún A", "Quán Chè C", "Quán Cơm B"]
    assert kq.dong[0] == "Quán Bún A — Loại hình: quán bún bò." and kq.dong[2] == "Quán Cơm B — Quán cơm bình dân gần chợ."  # "Loại hình" trước, không có thì câu đầu "Tóm tắt"
    assert lk.loc(MUC_LUC, "quan_ca_phe", []).dong == ("Cà phê D — Không gian yên tĩnh, có chỗ gửi xe.",)  # bài không có mục nào: dòng chữ đầu tiên
    assert lk.loc(MUC_LUC, lk.TAT_CA, []).tong == len(BAI) and lk.loc(MUC_LUC, "le_hoi", []).tong == 0  # bài cẩm nang ngoài mọi nhóm chỉ có ở `tat_ca`


def test_phrase_matches_title_first_then_body_with_the_evidence_line_from_the_article():
    kq = lk.loc(MUC_LUC, "quan_an", ["bún"])
    assert (kq.tong, kq.o_ten) == (1, 1) and kq.dong == ("Quán Bún A — Loại hình: quán bún bò.",)
    kq = lk.loc(MUC_LUC, lk.TAT_CA, ["quán"])  # tên có "quán" xếp trước (3 quán), bài chỉ nhắc trong thân xếp sau kèm ĐÚNG dòng nhắc
    assert (kq.tong, kq.o_ten) == (4, 3) and kq.dong[3].startswith("Lăng E — Trước đây khu này từng là quán nước")
    assert "3 bài có cụm từ ngay ở tên" in lk.trang_thai(kq) and "1 bài chỉ nhắc tới trong nội dung" in lk.trang_thai(kq)


def test_phrase_found_with_the_opposite_meaning_is_listed_with_the_line_that_says_so():
    """So nguyên cụm không hiểu nghĩa ⇒ bài PHỦ ĐỊNH cụm từ vẫn khớp. Hàm không được giấu điều đó: dòng làm chứng phải là chính dòng phủ định để model đọc
    được (và mô tả công cụ dặn đọc dòng kèm theo). Hai ca: phủ định một dịch vụ · nhắc tới thứ nay không còn."""
    kq = lk.loc(MUC_LUC, "quan_an", ["hút chân không"])
    assert kq.tong == 2 and kq.dong == ("Quán Bún A — Nhận hút chân không mang về.", "Quán Cơm B — Quán KHÔNG nhận hút chân không.")
    kq = lk.loc(MUC_LUC, "di_tich", ["hàng quán"])
    assert kq.dong == ("Lăng E — Trước đây khu này từng là quán nước cho lính canh; nay không còn hàng quán.",)


def test_no_match_says_so_and_odd_phrases_are_plain_text_not_patterns():
    kq = lk.loc(MUC_LUC, "quan_an", ["sân golf"])
    assert kq.tong == 0 and kq.dong == () and lk.trang_thai(kq).startswith("Trạng thái: không có bài nào trong tư liệu khớp")
    for la in (".*", "(", "[a-z]+", "quán|chè", "\\w"):  # không thành biểu thức: không khớp gì, không ném lỗi
        assert lk.loc(MUC_LUC, lk.TAT_CA, [la]).tong == 0, la
    assert lk.loc(MUC_LUC, "quan_an", ["", "   ", "x" * 41]).cum_tu == ()  # cụm rỗng / quá dài bị bỏ ⇒ như không có cụm từ
    assert lk.loc(MUC_LUC, "quan_an", ["a", "b", "c", "bún"]).cum_tu == ("a", "b", "c")  # tối đa 3 cụm


def test_matching_ignores_case_and_dash_style_but_keeps_diacritics():
    assert lk.loc(MUC_LUC, "quan_an", ["06:00-08:00"]).tong == 1 and lk.loc(MUC_LUC, "quan_an", ["06:00 — 08:00"]).tong == 1
    assert lk.loc(MUC_LUC, "quan_an", ["HÚT CHÂN KHÔNG"]).tong == 2
    assert lk.loc(MUC_LUC, "quan_an", ["bun"]).tong == 0 and lk.loc(MUC_LUC, "quan_an", ["che"]).tong == 0  # bỏ dấu là khớp nhầm ("che" ≠ "chè")


def test_long_result_is_cut_and_says_how_many_are_left():
    nhieu = tuple(lk.bai_tu_markdown(f"foods/cafes/q{i:02}.md", f"# Quán {i:02}\n\nCó wifi.") for i in range(lk.TOI_DA_DONG + 5))
    kq = lk.loc(nhieu, "quan_ca_phe", ["wifi"])
    assert kq.tong == lk.TOI_DA_DONG + 5 and len(kq.dong) == lk.TOI_DA_DONG and "còn 5 bài nữa" in lk.trang_thai(kq)
    dai = lk.bai_tu_markdown("foods/cafes/dai.md", "# Quán dài\n\n" + "chữ " * 200 + "wifi")
    assert len(lk.loc((dai,), "quan_ca_phe", ["chữ"]).dong[0]) <= len("Quán dài — ") + lk.DONG_DAI_NHAT + 1


def test_index_from_the_real_knowledge_base_has_every_article_and_known_groups():
    """Kho thật: mục lục có đúng số bài `discover_full_corpus_files` trả; mọi nhóm của công cụ có ít nhất một bài; bài nào cũng có tên."""
    root, rel = discover_full_corpus_files(load_settings(validate_private_paths=False))
    muc_luc = lk.nap_muc_luc(root, rel)
    assert len(muc_luc) == len(rel) > 200 and all(b.tieu_de for b in muc_luc)
    for nhom in lk.NHOM:
        assert lk.loc(muc_luc, nhom, []).tong > 0, nhom
    assert sum(lk.loc(muc_luc, nhom, []).tong for nhom in lk.NHOM) <= len(rel)


# ---------- công cụ của một lượt ----------

def test_flag_default_off_and_needs_the_tool_loop_and_the_index():
    assert AssistantFlags().liet_ke_bai is False and AssistantFlags().muc_luc is None
    with pytest.raises(ValueError, match="liet_ke_bai needs"):
        AssistantFlags(tim_them=True, liet_ke_bai=True)
    assert max_turns_for(None, None, ASSISTANT_MAX_TURNS, object()) == ASSISTANT_MAX_TURNS + 1


def test_tool_registers_one_source_that_can_be_cited_and_stops_after_two_calls():
    trace = AnswerTrace()
    cong_cu = liet_ke_for_turn(trace, MUC_LUC)
    ra = asyncio.run(cong_cu("quan_an", ["hút chân không"]))
    assert ra.startswith("Trạng thái: trong tư liệu có 2 bài khớp") and "[Nguồn 1]" in ra and "Quán Cơm B — Quán KHÔNG nhận hút chân không." in ra
    src, = trace.so_nguon
    assert (src.id, src.title, src.source) == (1, lk.TIEU_DE_NGUON, lk.NGUON_SOURCE) and len(src.excerpts) == 2 and "hút chân không" in src.heading_path[0]
    assert trace.tools == [{"name": "liet_ke_bai", "ms": 0.0, "nhom": "quan_an", "n_cum_tu": 1, "n_bai": 2, "n_o_ten": 0}]  # sổ chỉ có số đếm, không có chữ cụm từ
    assert lk.LAN_CUOI not in ra  # lần đầu: chưa phải lần cuối
    khong = asyncio.run(cong_cu("quan_an", ["sân golf"]))  # không khớp ⇒ chỉ dòng trạng thái, KHÔNG đăng nguồn rỗng; lần thứ hai = lần cuối ⇒ nói rõ
    assert khong.startswith("Trạng thái: không có bài nào") and khong.endswith(lk.LAN_CUOI) and len(trace.so_nguon) == 1
    het = asyncio.run(cong_cu("quan_an", []))  # lần thứ ba trong một câu
    assert "đã dùng hết lượt" in het and len(trace.so_nguon) == 1 and trace.tools[-1]["het_luot"] is True


def test_repeating_the_same_call_does_not_register_a_second_source():
    """Lượt thật 21/11 (luna): gọi lại y nguyên nhóm + cụm từ ⇒ trước đây đăng nguồn thứ hai giống hệt và tốn vòng. Nay: dòng trỏ về nguồn đã có (so trên
    cụm từ ĐÃ CHUẨN — khác hoa thường / kiểu gạch vẫn là trùng); lời gọi KHÁC cụm từ vẫn chạy bình thường."""
    trace = AnswerTrace()
    cong_cu = liet_ke_for_turn(trace, MUC_LUC)
    asyncio.run(cong_cu("quan_an", ["hút chân không"]))
    lap = asyncio.run(cong_cu("quan_an", ["HÚT  chân không"]))
    assert lap.startswith("Trạng thái: lời gọi này trùng một lời gọi trước trong câu — kết quả đã có ở nguồn [1]") and lap.endswith(lk.LAN_CUOI)
    assert len(trace.so_nguon) == 1 and trace.tools[-1]["lap"] is True
    trace = AnswerTrace()
    cong_cu = liet_ke_for_turn(trace, MUC_LUC)
    asyncio.run(cong_cu("quan_an", ["sân golf"]))
    assert "lần trước đã không có bài nào khớp" in asyncio.run(cong_cu("quan_an", ["sân golf"])) and trace.so_nguon == []
    trace = AnswerTrace()
    cong_cu = liet_ke_for_turn(trace, MUC_LUC)
    asyncio.run(cong_cu("quan_an", ["bún"]))
    khac = asyncio.run(cong_cu("quan_an", ["chè"]))
    assert "[Nguồn 2]" in khac and len(trace.so_nguon) == 2 and "lap" not in trace.tools[-1]


def test_flag_off_sends_the_same_bytes_and_flag_on_only_adds_one_tool_on_every_kind_of_turn(deps):
    """Cờ tắt (kể cả khi mục lục đã nạp) ⇒ thân gửi model giống byte bản không có tính năng. Cờ bật ⇒ khác ĐÚNG ở chỗ danh sách công cụ có thêm
    `liet_ke_bai` — ở lượt đầu, lượt có lịch sử và đường stream; lời dặn và mọi thứ khác giữ nguyên."""
    viet = lambda n, kw: [answer("Có thông tin [1].")]  # noqa: E731
    for history in ((), (("Huế có gì chơi?", ""),)):
        _, gen_off = turn(deps, viet, OFF, history)
        _, gen_on = turn(deps, viet, ON, history)
        assert tools_sent(gen_off) == [["tim_kho"]] and tools_sent(gen_on) == [["tim_kho", "liet_ke_bai"]], history
        off, on = json.loads(sent_requests(gen_off)), json.loads(sent_requests(gen_on))
        assert [{k: v for k, v in kw.items() if k != "tools"} for kw in on] == [{k: v for k, v in kw.items() if k != "tools"} for kw in off]
        assert on[0]["tools"][:1] == off[0]["tools"] and on[0]["tools"][1]["name"] == "liet_ke_bai"

    async def stream(flags):
        gen, trace = generator(viet), AnswerTrace()
        _ = [e async for e in answer_turn_stream(CAU, *deps, gen, trace, flags)]
        return gen
    assert tools_sent(asyncio.run(stream(OFF))) == [["tim_kho"]] and tools_sent(asyncio.run(stream(ON))) == [["tim_kho", "liet_ke_bai"]]


def test_a_real_turn_lists_then_cites_the_index_source(deps):
    """Một lượt đủ vòng: model gọi `liet_ke_bai`, nhận dòng trạng thái + khối nguồn, rồi viết câu trả lời trích ĐÚNG mã nguồn đó ⇒ qua bộ kiểm trích nguồn;
    nguồn được trích là "Mục lục kho tư liệu" (không phải một bài kho)."""
    def script(n, kw):
        if n == 1:
            return [goi_liet_ke("quan_an", ["hút chân không"])]
        ra = ket_qua_cong_cu(kw)[-1]
        ma = re.search(r"\[Nguồn (\d+)\]", ra).group(1)
        return [answer(f"Trong tư liệu hiện có Quán Bún A nhận hút chân không [{ma}].")]

    trace, gen = turn(deps, script, ON)
    assert trace.citation_error is None and trace.fixed_outcome is None and len(gen.client.responses.calls) == 2
    assert [(s.title, s.source) for s in trace.cited] == [(lk.TIEU_DE_NGUON, lk.NGUON_SOURCE)]
    assert ket_qua_cong_cu(gen.client.responses.calls[1])[-1].startswith("Trạng thái: trong tư liệu có 2 bài khớp")
    assert [t["name"] for t in trace.tools if t["name"] == "liet_ke_bai"] == ["liet_ke_bai"]


def test_tool_is_hidden_after_its_two_calls_and_asking_again_is_a_fixed_refusal_not_an_error(deps):
    """Dùng đủ hai lần ⇒ lần gọi model kế tiếp KHÔNG gửi `liet_ke_bai` nữa (lượt thật 21/11: lần xin thứ ba ăn mất vòng viết ⇒ chạm trần vòng). Model vẫn
    xin công cụ đã ẩn ⇒ câu từ chối cố định như ca `tim_kho` bị ẩn, không phải lỗi 500."""
    def hai_lan_roi_viet(n, kw):
        if n <= 2:
            return [goi_liet_ke("quan_an", [("bún", "chè")[n - 1]])]
        return [answer("Có thông tin [1].")]

    trace, gen = turn(deps, hai_lan_roi_viet, ON)
    assert [("liet_ke_bai" in names) for names in tools_sent(gen)] == [True, True, False] and all("tim_kho" in names for names in tools_sent(gen))
    assert trace.citation_error is None and trace.fixed_outcome is None

    trace, gen = turn(deps, lambda n, kw: [goi_liet_ke("quan_an", [f"cụm {n}"])], ON)  # model cứ xin mãi
    assert trace.fixed_outcome == "max_turns" and trace.answer == INSUFFICIENT_ANSWER and len(gen.client.responses.calls) == 3
