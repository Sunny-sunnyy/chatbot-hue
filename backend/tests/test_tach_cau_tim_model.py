"""Công tắc `tach_cau_tim_model` (22/11/2026). Vì sao: câu tìm do MODEL viết gộp hai nơi không kéo được đoạn kho của từng nơi — tin 4 ý "tổng vé Đại Nội +
Tự Đức, bà có được giảm không…": model tìm "giá vé Đại Nội và Lăng Tự Đức…" 2–3 lần mà đoạn có giá vé lẻ Đại Nội không vào 10 đoạn (câu tìm một nơi thì
đoạn đó đứng đầu), hết lượt tìm ⇒ nộp chữ giữ chỗ ⇒ màn hình lỗi (4 / 6 lượt). Đếm 0 đồng trên 396 câu tìm của model đã ghi: 231 câu (58 %) là câu gộp; 32
câu gộp về vé Đại Nội — đoạn có giá vào kết quả 16 / 32 khi để nguyên, 27 / 32 khi nối thêm 2 đoạn đầu của từng phần, không câu nào mất. Lần tìm cả câu
giữ nguyên; phần chỉ NỐI THÊM (cơ chế của `tim_theo_ve`). 0 USD: tìm kho thật, model theo kịch bản."""
import dataclasses
import re

import pytest

from llm.assistant import TRAN_PHAN_CAU_TIM, AssistantFlags, cac_phan_cau_tim
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_b2_tool_loop import _tool_outputs, answer, deps, generator, run_turn, tool_call  # noqa: F401  (`deps` = fixture tìm kho thật)

TAT = AssistantFlags(lan_tim_dau="v2")
MO = dataclasses.replace(TAT, tach_cau_tim_model=True)
GOP, MOT_PHAN = "giá vé lẻ Đại Nội Huế và Lăng Tự Đức người lớn trẻ em", "giá vé lẻ Đại Nội Huế người lớn"


@pytest.mark.parametrize("cau, mong", [
    (GOP, ("giá vé lẻ Đại Nội Huế", "Lăng Tự Đức người lớn trẻ em")),
    ("Đại Nội Huế giá vé lẻ người lớn; người cao tuổi từ 60 tuổi giảm 50%; trẻ em dưới 7 tuổi miễn phí",
     ("Đại Nội Huế giá vé lẻ người lớn", "người cao tuổi từ 60 tuổi giảm 50%", "trẻ em dưới 7 tuổi miễn phí")),
    ("vé Đại Nội + Lăng Tự Đức", ("vé Đại Nội", "Lăng Tự Đức")),
    (MOT_PHAN, ()),                                   # câu tìm một phần: không tìm thêm gì
    ("bún bò và chè", ()),                            # phần quá ngắn bị bỏ ⇒ còn dưới hai phần ⇒ không tách
    ("vô và ra Đại Nội bằng cửa nào", ()),            # "vô" dưới 6 ký tự ⇒ còn một phần ⇒ không tách
    ("giá vé Đại Nội; giá vé Đại Nội", ()),           # hai phần trùng ⇒ một
])
def test_parts_of_a_combined_query(cau, mong):
    assert cac_phan_cau_tim(cau) == mong


def test_parts_are_capped():
    assert len(cac_phan_cau_tim("; ".join(f"điểm tham quan số {i}" for i in range(7)))) == TRAN_PHAN_CAU_TIM


def _luot(deps, cau_tim, flags):
    """Model gọi tìm kho MỘT lần với `cau_tim` rồi nộp câu từ chối; trả (trace, chữ kết quả công cụ model nhận)."""
    gen = generator(lambda n, kw: [tool_call(cau_tim)] if n == 1 else [answer(INSUFFICIENT_ANSWER)])
    trace = run_turn(deps, "Đi hai điểm thì tổng vé cả nhà hết bao nhiêu?", gen, flags)  # câu người dùng không nêu tên nơi: lần tìm đầu không kéo sẵn bảng vé
    return trace, _tool_outputs(gen.client.responses.calls[-1])[-1]


def test_combined_query_keeps_the_whole_query_results_and_appends_each_part(deps):
    tat, chu_tat = _luot(deps, GOP, TAT)
    mo, chu_mo = _luot(deps, GOP, MO)
    assert chu_mo.startswith(chu_tat) and len(chu_mo) > len(chu_tat)   # kết quả của cả câu giữ nguyên chữ, thứ tự, số nguồn; phần chỉ nối SAU
    muc_tat, muc_mo = (next(t for t in tr.tools if t.get("by") == "model") for tr in (tat, mo))
    assert "n_ve" not in muc_tat and muc_mo["n_ve"] == 2 and 1 <= muc_mo["n_them_ve"] <= 4   # dấu đếm được: số phần, số đoạn nối thêm
    assert len(mo.so_nguon) == len(tat.so_nguon) + muc_mo["n_them_ve"] and [s.id for s in mo.so_nguon] == list(range(1, len(mo.so_nguon) + 1))
    gia = re.compile(r"Đại Nội[^\n]{0,80}200\.000")                     # dòng giá vé lẻ Đại Nội (chuỗi "200.000" trần còn có ở giá một tuyến vé gộp)
    assert not gia.search("\n".join(tat.context_parts)) and gia.search(chu_mo)  # đúng ca đã thấy: giá đó chỉ về khi phần "Đại Nội" được tìm riêng


def test_single_part_query_and_switch_off_are_unchanged(deps):
    _, a = _luot(deps, MOT_PHAN, TAT)
    _, b = _luot(deps, MOT_PHAN, MO)
    assert a == b


def test_first_search_of_the_code_is_not_touched(deps):
    """Công tắc chỉ chạm lần tìm của MODEL: lần tìm đầu của code (câu người dùng) cho cùng kết quả dù mở hay tắt."""
    tat, _ = _luot(deps, MOT_PHAN, TAT)
    mo, _ = _luot(deps, MOT_PHAN, MO)
    assert tat.context_parts[0] == mo.context_parts[0]
