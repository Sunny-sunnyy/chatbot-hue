"""Cờ `dem_y_go_tat` (21/11/2026) — 0 USD. Vì sao: bộ đếm ý hỏi `so_y` chỉ nhận từ hỏi viết đủ; người dùng gõ tắt ("vé bn, bà có giảm ko?") ⇒ tin 4–5 ý bị
đếm 0–1 ý ⇒ không dùng lời dặn theo ý ⇒ model từ chối cả lượt (lượt mốc 12 vai 21/11: model đang chạy 0 / 65 lượt bị từ chối khi bộ đếm ra ≥ 2 ý, 5 / 24 khi
đếm thiếu vì chữ tắt). Cờ bật: bộ đếm nhận thêm từ hỏi gõ tắt — CHỈ đổi phép đếm. Câu ví dụ ở file này do người viết bản sửa tự đặt; bộ tin độc lập của
phiên điều phối và lượt thật ghi ở report của nhánh."""
import asyncio

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, so_y
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_cau_nhieu_y import Client, deps, test_so_y_counts_question_clauses  # noqa: F401  (`deps` = fixture tìm kho thật)

CAU_DU_CHU = test_so_y_counts_question_clauses.pytestmark[0].args[1]  # bảng (câu gõ đủ chữ, số ý) của test có sẵn


def test_flag_defaults_off_and_needs_the_multi_part_flag():
    assert AssistantFlags().dem_y_go_tat is False
    with pytest.raises(ValueError, match="dem_y_go_tat needs"):
        AssistantFlags(dem_y_go_tat=True)


@pytest.mark.parametrize("cau, n", CAU_DU_CHU)
def test_fully_typed_sentences_count_the_same_with_the_flag(cau, n):
    """Bất biến: câu gõ đủ chữ đếm y như cũ, dù cờ bật hay tắt."""
    assert so_y(cau) == so_y(cau, False) == so_y(cau, True) == n


@pytest.mark.parametrize("cau, tat, bat", [
    ("Vé lăng Minh Mạng bn, người già có giảm ko? Mở cửa tới mấy h", 1, 3),     # "bn" cuối vế · "ko" cuối vế · "mấy" (đã nhận từ trước)
    ("quán đó mở cửa chưa, có chỗ gửi xe k", 1, 2),
    ("đi chợ Đông Ba mua j, giá ntn", 0, 2),
    ("thuê xe máy bn 1 ngày, có cần đặt cọc hok", 0, 2),
    ("vé bn tiền vậy? trẻ em miễn phí đc ko.", 1, 2),                           # "vậy" cuối vế đã được nhận từ trước; "ko." = dấu chấm cuối tin
    ("Chùa mở cửa ko và lăng Tự Đức vé bao nhiu", 0, 2),                         # tách theo "và"
])
def test_abbreviated_question_words_are_counted_only_with_the_flag(cau, tat, bat):
    assert (so_y(cau), so_y(cau, True)) == (tat, bat)


@pytest.mark.parametrize("cau", [
    "Vé vào Đại Nội 200k, mình mang 500k",                 # "k" sau con số là nghìn
    "bn ơi, cho mình xem giờ mở cửa Đại Nội",              # "bn" là "bạn"
    "bn có thể gợi ý quán bún bò được chứ",
    "Mình đi 2 ng lớn, 1 trẻ em",
    "Tầm 150 k một người, ăn vài chục k",                  # "k" sau số có dấu cách / sau từ chỉ lượng
    "ok, cho mình lịch 2 ngày",
    "k, mình hỏi lăng Khải Định cơ",                       # "k" đứng một mình đầu câu = "không" trả lời, không phải tiểu từ hỏi
    "Mình ở KH sạn gần cầu, đi bộ ra phố",
])
def test_lookalikes_are_not_counted(cau):
    assert so_y(cau, True) == so_y(cau) == 0


@pytest.mark.parametrize("cau", ["Vé lăng Khải Định bn", "chùa Thiên Mụ mở cửa ko", "ăn j ở Huế", "từ ga ra Đại Nội đi ntn"])
def test_one_abbreviated_question_is_one_part(cau):
    assert so_y(cau, True) == 1  # một ý ⇒ vẫn dưới ngưỡng 2 ⇒ lượt đó dùng lời dặn cũ


def test_core_uses_the_multi_part_instructions_for_an_abbreviated_message_only_with_the_flag(deps):
    """Đường thật của lõi (tìm kho thật, model giả): tin nhiều ý gõ tắt — cờ tắt ⇒ lời dặn thường như trước; cờ bật ⇒ ĐÚNG lời dặn theo ý mà một tin
    nhiều ý gõ đủ chữ vẫn nhận. Chữ của lời dặn không đổi — chỉ đổi việc lượt nào dùng nó; câu người dùng gửi đi nguyên văn."""
    def chay(cau, flags):
        client, trace = Client("Vé lẻ người lớn 200.000 đồng [1]."), AnswerTrace()
        asyncio.run(answer_turn(cau, *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags))
        return trace, client.calls[0]

    tat = AssistantFlags(router=False, tim_them=True, cau_nhieu_y=True)
    bat = AssistantFlags(router=False, tim_them=True, cau_nhieu_y=True, dem_y_go_tat=True)
    go_tat, du_chu = "Vé Đại Nội bn, người già có giảm ko?", "Vé Đại Nội bao nhiêu, người già có giảm không?"
    (t1, g1), (t2, g2), (t3, g3) = chay(go_tat, tat), chay(go_tat, bat), chay(du_chu, tat)
    assert (t1.nhieu_y, t2.nhieu_y, t3.nhieu_y) == (False, True, True)
    assert g1["instructions"] != g2["instructions"] == g3["instructions"]
    assert go_tat in json_chu(g2["input"]) and "bao nhiêu" not in json_chu(g2["input"])  # chữ người dùng tới model nguyên văn, không bị "dịch" chữ tắt


def json_chu(x) -> str:
    import json
    return json.dumps(x, ensure_ascii=False, default=str)
