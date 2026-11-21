"""Vòng cuối chỉ viết (kèm dòng báo ở kết quả công cụ sát cuối) + trạng thái "không có số" của công cụ khoảng cách (21/11/2026) — 0 USD.

Vì sao: người dùng mô phỏng — câu 3–5 ý có "bao xa" + nơi không có trong bảng khoảng cách ⇒ 3 lần tìm kho + 3 lần khoảng cách ⇒ hết vòng ⇒ câu từ chối trống
(luna 5 / 44 lượt). Hai cờ ĐỘC LẬP, mặc định TẮT: `vong_cuoi_chi_viet` (vòng cuối không kèm công cụ, và kết quả công cụ sát cuối báo điều đó),
`khoang_cach_trang_thai` (dòng trạng thái khi không có số). Chép từ nhánh `p9-b-vong-cuoi-chi-viet` (`e9a14c12`), KHÔNG kèm cờ thứ ba của nhánh đó (dòng báo
"hết lượt tìm kho": đo thấy model đang chạy trả lời câu ngoài tỉnh bằng kho).
Model là `OpenAIResponsesModel` thật của SDK với phản hồi dựng sẵn (như `test_b2_tool_loop.py`); tìm kho là Qdrant thật (chỉ đọc). Đây không phải bằng chứng
model thật viết gì ở vòng cuối — phần đó là lượt đo có phí ghi trong report của nhánh.
"""
import asyncio

from llm import khoang_cach as kc
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream, khoang_cach_for_turn
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, TOOL_VONG_CUOI_TEXT
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (fixture `deps` dùng chung)
from test_het_luot_tim import CAU, searches_then_answer, sent_requests, tools_sent, turn

OFF = AssistantFlags(tim_them=True)
VONG_CUOI = AssistantFlags(tim_them=True, vong_cuoi_chi_viet=True)


def tool_outputs(gen, call: int) -> list[str]:
    """Kết quả công cụ nằm trong đầu vào của lần gọi model thứ `call` (từ 1)."""
    return [i["output"] for i in gen.client.responses.calls[call - 1]["input"] if isinstance(i, dict) and i.get("type") == "function_call_output"]


def tim_mai(n, kw):
    """Model cứ xin tìm kho chừng nào còn được đưa công cụ; hết công cụ thì viết (trích nguồn [1] của lần tìm đầu)."""
    return [tool_call(f"câu tìm {n}")] if kw.get("tools") else [answer("Có thông tin [1].")]


def test_two_flags_default_off():
    assert (AssistantFlags().vong_cuoi_chi_viet, AssistantFlags().khoang_cach_trang_thai) == (False, False)


def test_last_round_has_no_tools_and_the_model_is_told_in_the_last_tool_result(deps):
    """Cờ tắt: 4 lần gọi đều kèm công cụ, hết vòng ⇒ câu từ chối cố định. Cờ bật: lần gọi thứ 4 KHÔNG kèm công cụ ⇒ model viết; kết quả công cụ của lượt sát
    cuối (và chỉ lượt đó) kết thúc bằng dòng báo "bước kế không còn công cụ"."""
    trace_off, gen_off = turn(deps, tim_mai, OFF)
    assert [bool(names) for names in tools_sent(gen_off)] == [True] * 4
    assert trace_off.fixed_outcome == "max_turns" and trace_off.answer == INSUFFICIENT_ANSWER

    trace, gen = turn(deps, tim_mai, VONG_CUOI)
    assert [bool(names) for names in tools_sent(gen)] == [True, True, True, False]
    assert trace.fixed_outcome is None and trace.answer == "Có thông tin [1]." and trace.citation_error is None
    ra = tool_outputs(gen, 4)
    assert len(ra) == 3 and ra[2].endswith(TOOL_VONG_CUOI_TEXT) and not any(TOOL_VONG_CUOI_TEXT in x for x in ra[:2])


def test_stream_path_also_drops_the_tools_in_the_last_round(deps):
    """Đường STREAM (đường giao diện dùng) dựng công cụ ở một chỗ khác đường không stream: cờ phải tới được cả hai. Cờ bật ⇒ lần gọi thứ 4 không kèm công
    cụ, người dùng nhận chữ model viết; cờ tắt ⇒ câu từ chối cố định như hôm nay."""
    async def collect(flags):
        gen, trace = generator(tim_mai), AnswerTrace()
        events = [e async for e in answer_turn_stream(CAU, *deps, gen, trace, flags)]
        return gen, trace, "".join(data for kind, data in events if kind == "delta")

    gen, trace, chu = asyncio.run(collect(VONG_CUOI))
    assert [bool(names) for names in tools_sent(gen)] == [True, True, True, False]
    assert trace.fixed_outcome is None and chu == "Có thông tin [1]."
    gen_off, trace_off, chu_off = asyncio.run(collect(OFF))
    assert [bool(names) for names in tools_sent(gen_off)] == [True] * 4 and trace_off.fixed_outcome == "max_turns" and chu_off == INSUFFICIENT_ANSWER


def test_turns_that_end_early_send_the_same_bytes_as_flag_off(deps):
    """Lượt kết thúc trước vòng sát cuối (không tìm thêm / tìm một lần): cờ bật gửi model đúng từng byte như cờ tắt — dòng báo và việc ẩn công cụ chỉ xuất hiện
    ở cuối lượt dài. Kiểm cả lượt có lịch sử."""
    for history in ((), (("Huế có gì chơi?", "Có Đại Nội [1]."),)):
        for n_searches in (0, 1):
            _, gen_on = turn(deps, searches_then_answer(n_searches), VONG_CUOI, history)
            _, gen_off = turn(deps, searches_then_answer(n_searches), OFF, history)
            assert sent_requests(gen_on) == sent_requests(gen_off), (history, n_searches)


def test_model_still_asking_for_a_tool_in_the_last_round_gets_the_fixed_refusal_not_an_error(deps):
    """Model lờ dòng báo, vẫn xin công cụ ở vòng không còn công cụ ⇒ SDK báo công cụ không dùng được ⇒ kết cục như hết vòng hôm nay (câu từ chối cố định),
    không phải lỗi 500."""
    trace, gen = turn(deps, lambda n, kw: [tool_call(f"câu tìm {n}")], VONG_CUOI)
    assert len(gen.client.responses.calls) == 4 and not tools_sent(gen)[3]
    assert trace.fixed_outcome == "max_turns" and trace.answer == INSUFFICIENT_ANSWER


def test_distance_tool_says_plainly_when_it_has_no_number():
    """Cờ `khoang_cach_trang_thai`: nơi ngoài danh sách ⇒ kết quả mở đầu bằng dòng trạng thái (đứng ngoài khối nguồn), nguồn "chưa có số" vẫn được đăng để trích;
    cặp có số ⇒ không có dòng trạng thái; cờ tắt ⇒ chữ như cũ."""
    bang = kc.BangKhoangCach(ten={"a": "Điểm A", "b": "Điểm B"}, ten_khac={"a": (), "b": ()}, cap={"a|b": {"km": 4.4, "phut": 9}})

    def goi(trang_thai: bool, diem_b: str) -> tuple[str, AnswerTrace]:
        trace = AnswerTrace()
        return asyncio.run(khoang_cach_for_turn(trace, bang, trang_thai)("a", diem_b)), trace

    khong_co, trace = goi(True, kc.KHAC)
    assert khong_co.startswith(kc.TRANG_THAI_KHONG_CO + "\n\n[Nguồn 1]") and kc.CAU_CHUA_CO in khong_co
    assert len(trace.so_nguon) == 1 and kc.TRANG_THAI_KHONG_CO not in " ".join(trace.so_nguon[0].excerpts) and trace.tools[0]["khong_co"] is True
    co_so, _ = goi(True, "b")
    assert co_so.startswith("[Nguồn 1]") and kc.TRANG_THAI_KHONG_CO not in co_so
    cu, _ = goi(False, kc.KHAC)
    assert cu.startswith("[Nguồn 1]") and kc.TRANG_THAI_KHONG_CO not in cu


def test_listing_tool_shares_the_last_round_rule_and_its_extra_round_is_counted(deps):
    """Ghép với cờ `liet_ke_bai` (21/11): lượt có công cụ liệt kê được thêm MỘT vòng (5 thay vì 4) ⇒ vòng cuối chỉ viết phải là vòng thứ 5, không phải thứ 4;
    công cụ liệt kê bị ẩn sau hai lần dùng VÀ ở vòng cuối, qua cùng hàm gom điều kiện với mọi công cụ khác."""
    from llm import liet_ke as lk
    from test_liet_ke_bai import MUC_LUC, goi_liet_ke

    co = AssistantFlags(tim_them=True, vong_cuoi_chi_viet=True, liet_ke_bai=True, muc_luc=MUC_LUC)

    def script(n, kw):
        if not kw.get("tools"):
            return [answer("Có thông tin [1].")]
        return [goi_liet_ke("quan_an", [("bún", "chè")[n - 1]])] if n <= 2 else [tool_call(f"câu tìm {n}")]

    trace, gen = turn(deps, script, co)
    assert tools_sent(gen) == [["tim_kho", "liet_ke_bai"], ["tim_kho", "liet_ke_bai"], ["tim_kho"], ["tim_kho"], []]  # 5 vòng; vòng 5 không công cụ
    assert trace.fixed_outcome is None and trace.answer == "Có thông tin [1]." and trace.citation_error is None
    ra = tool_outputs(gen, 5)
    assert ra[-1].endswith(TOOL_VONG_CUOI_TEXT) and not any(TOOL_VONG_CUOI_TEXT in x for x in ra[:-1])  # chỉ kết quả công cụ của vòng sát cuối (vòng 4) mang dòng báo
    assert lk.LAN_CUOI in ra[1]  # lần liệt kê thứ hai vẫn nói đó là lần cuối của riêng công cụ này
