"""Cờ `tim_theo_ve` (22/11/2026, S2) — 0 USD. Vì sao: lần tìm kho đầu dùng nguyên một tin nhiều vế ⇒ đoạn kho của vế phụ hay không vào ngữ cảnh ⇒
model ghi nhầm "Tư liệu chưa có thông tin về…". Cờ bật: tin NHIỀU Ý giữ đủ các đoạn của lần tìm bằng cả tin + nối thêm 2 đoạn đầu của lần tìm riêng
từng vế. File này kiểm phần code (tìm kho THẬT qua Qdrant, model giả): tin một ý và cờ tắt không đổi gì; phần ngữ cảnh cũ giữ nguyên; số nguồn nối tiếp
trích dẫn được; đường stream song song (đường người dùng đi) chạy được với cờ bật. Chất lượng câu trả lời là lượt đo có phí ghi ở report của nhánh."""
import asyncio
import dataclasses
import json

import pytest

from core.settings_loader import load_settings
from llm.assistant import TRAN_SO_VE_TIM, AnswerTrace, AssistantFlags, answer_turn, cac_ve_tim, so_y
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_cau_nhieu_y import CAU_HAI_Y, Client, deps  # noqa: F401  (`deps` = fixture tìm kho thật)

TAT = AssistantFlags(router=True, tim_them=True, cau_nhieu_y=True)
BAT = dataclasses.replace(TAT, tim_theo_ve=True)
CAU_MOT_Y = "Vé lẻ vào Đại Nội giá bao nhiêu?"


def test_flag_defaults_off_in_code_and_is_on_in_settings():
    """Mặc định của code là tắt (cấu hình thiếu dòng ⇒ chạy như cũ); settings đang chạy: MỞ từ 22/11/2026."""
    assert AssistantFlags().tim_theo_ve is False
    assert load_settings(validate_private_paths=False)["assistant"]["tim_theo_ve"] is True


def test_search_clauses_are_wider_than_the_multi_part_counter_and_capped():
    """Vế để TÌM nhận cả kiểu gõ tắt và cắt ở dấu chấm — `so_y` (luật quyết tin nhiều ý) không đổi."""
    tin = "Ok sáng có phở rồi. Trưa thì gần chợ có quán nào ngon k? Giá bn, mở tới mấy giờ. Cảm ơn nha"
    assert cac_ve_tim(tin) == ["Trưa thì gần chợ có quán nào ngon k?", "mở tới mấy giờ"]  # "Giá bn" ngắn dưới 8 ký tự; câu chào không có từ hỏi
    assert cac_ve_tim("vé bao nhiêu, vé bao nhiêu, mở cửa mấy giờ?") == ["vé bao nhiêu", "mở cửa mấy giờ?"]  # vế trùng chỉ tìm một lần
    nhieu = ", ".join(f"điểm số {i} mở cửa mấy giờ" for i in range(10))
    assert len(cac_ve_tim(nhieu)) == TRAN_SO_VE_TIM and so_y(nhieu) == 10


def test_search_clauses_do_not_cut_inside_a_number():
    """Soát khác hãng 22/11 (Gemini Carbon 11): cắt ở MỌI dấu chấm / phẩy làm câu tìm cụt ngay giữa con số ("200.000" ⇒ "000 có gồm …")."""
    tin = "Vé Đại Nội 200.000 có gồm Bảo tàng Cổ vật không, lăng Tự Đức 150.000 mở cửa mấy giờ?"
    assert cac_ve_tim(tin) == ["Vé Đại Nội 200.000 có gồm Bảo tàng Cổ vật không", "lăng Tự Đức 150.000 mở cửa mấy giờ?"]
    assert cac_ve_tim("Đi 1,5 km thì mất bao lâu? Vé 200,000 có đắt không?") == ["Đi 1,5 km thì mất bao lâu?", "Vé 200,000 có đắt không?"]


def _chay(deps, flags, cau, text="Vé lẻ người lớn 200.000 đồng [1]."):
    """Một lượt qua lõi thật. Trả trace + lời gọi TRẢ LỜI (lời gọi model có ngữ cảnh kho trong đầu vào — không phải lời gọi định tuyến)."""
    client, trace = Client(text), AnswerTrace()
    asyncio.run(answer_turn(cau, *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags))
    tra_loi = [g for g in client.calls if "[Nguồn 1]" in json.dumps(g["input"], ensure_ascii=False)]
    assert len(tra_loi) == 1
    return trace, tra_loi[0]


def _trong_dau_vao(chu: str, goi: dict) -> bool:
    return json.dumps(chu, ensure_ascii=False)[1:-1] in json.dumps(goi["input"], ensure_ascii=False)


def test_single_part_message_is_untouched_by_the_flag(deps):
    """Tin một ý: cờ bật hay tắt, thứ gửi model giống hệt, cùng số nguồn, không có lần tìm thêm."""
    (t_tat, goi_tat), (t_bat, goi_bat) = _chay(deps, TAT, CAU_MOT_Y), _chay(deps, BAT, CAU_MOT_Y)
    assert goi_bat["input"] == goi_tat["input"] and goi_bat["instructions"] == goi_tat["instructions"]
    assert t_bat.packed == t_tat.packed and "n_ve" not in t_bat.tools[0]


def test_multi_part_message_keeps_every_old_chunk_and_appends_clause_chunks(deps):
    """Tin nhiều ý, cờ bật: phần ngữ cảnh của lần tìm bằng cả tin giữ nguyên từng ký tự và đứng trước; đoạn của từng vế nối sau, đánh số tiếp, không
    trùng; cả phần nối thêm nằm trong thứ gửi model; log ghi số vế + số đoạn thêm (chỉ số đếm)."""
    (t_tat, goi_tat), (t_bat, goi_bat) = _chay(deps, TAT, CAU_HAI_Y), _chay(deps, BAT, CAU_HAI_Y)
    cu, moi = t_tat.packed, t_bat.packed
    assert moi.text.startswith(cu.text) and moi.sources[:len(cu.sources)] == cu.sources
    them = moi.sources[len(cu.sources):]
    assert 1 <= len(them) <= 2 * len(cac_ve_tim(CAU_HAI_Y))
    assert [s.id for s in moi.sources] == list(range(1, len(moi.sources) + 1)) and len(set(moi.document_ids)) == len(moi.document_ids)
    assert _trong_dau_vao(moi.text, goi_bat) and _trong_dau_vao(cu.text, goi_tat) and not _trong_dau_vao(moi.text, goi_tat)
    assert goi_bat["instructions"] == goi_tat["instructions"]  # cờ không đổi lời dặn
    assert t_bat.tools[0]["n_ve"] == len(cac_ve_tim(CAU_HAI_Y)) and t_bat.tools[0]["n_them_ve"] == len(them)
    assert "n_ve" not in t_tat.tools[0]


def test_answer_may_cite_an_appended_chunk(deps):
    """Câu trả lời trích số nguồn của một đoạn NỐI THÊM ⇒ phép kiểm trích dẫn nhận (đoạn đó có trong sổ nguồn của lượt)."""
    t_tat, _ = _chay(deps, TAT, CAU_HAI_Y)
    so = len(t_tat.packed.sources) + 1
    t_bat, _ = _chay(deps, BAT, CAU_HAI_Y, text=f"Vé lẻ người lớn 200.000 đồng [1]. Dịp Tết có chương trình riêng [{so}].")
    assert t_bat.citation_error is None and any(s.id == so for s in t_bat.cited)
    t_khong, _ = _chay(deps, TAT, CAU_HAI_Y, text=f"Vé lẻ người lớn 200.000 đồng [1]. Dịp Tết có chương trình riêng [{so}].")
    assert t_khong.citation_error is not None  # cờ tắt: số nguồn đó không tồn tại ⇒ đúng là đoạn nối thêm làm nó hợp lệ


@pytest.mark.parametrize("parallel", [False, True])
def test_live_stream_path_runs_with_the_flag_on(deps, parallel):
    """Đường stream đang chạy thật (song song định tuyến, bản cờ phụ do lõi tự tạo): cờ bật ⇒ không lỗi, lượt nhiều ý có đoạn nối thêm, lượt một ý không."""
    from llm.assistant import answer_turn_stream, answer_turn_stream_parallel
    from test_b2_tool_loop import answer, generator
    from test_b6_tra_web import _events

    def script(n, kw):
        ins = kw.get("instructions") or ""
        if "tro_ly_hue" in ins and "ngoai_pham_vi" in ins:  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        return [answer("Vé lẻ người lớn 200.000 đồng [1].")]
    ham = answer_turn_stream_parallel if parallel else answer_turn_stream
    so_nguon = {}
    for ten, flags, cau in (("tat", TAT, CAU_HAI_Y), ("bat", BAT, CAU_HAI_Y), ("bat_mot_y", BAT, CAU_MOT_Y)):
        trace = AnswerTrace()
        events = _events(ham, cau, *deps, generator(script), trace, dataclasses.replace(flags, song_song_tra_loi=parallel), None, None)
        assert [d for k, d in events if k == "error"] == [], ten
        assert trace.answer and trace.packed is not None, ten
        so_nguon[ten] = len(trace.packed.sources)
    assert so_nguon["bat"] > so_nguon["tat"] and so_nguon["bat_mot_y"] <= so_nguon["tat"]  # chỉ lượt nhiều ý có đoạn nối thêm


# ---------- cờ con `tim_ve_bo_cut` (22/11/2026): vế tìm CỤT — không chủ thể, chỉ có từ hỏi + từ thuộc tính chung — không được tìm riêng ----------
K22 = ("Nhà mình có 4 người thôi nha, ko phải 5. Vậy đi Đại Nội + Tự Đức thì tổng vé cả nhà bao nhiêu, bà có được giảm ko? Bảo tàng Cổ vật vs An Định "
       "chưa rõ bậc với giá vé thì thôi, có điểm nào khác ít bậc, biết giá, giờ mở cửa ko? Bé ngồi lâu là quấy lắm")  # tin của người dùng mô phỏng (lượt mốc 12 vai)


def test_subject_less_clause_switch_defaults_off_in_code_and_is_on_in_settings():
    assert AssistantFlags().tim_ve_bo_cut is False
    assert load_settings(validate_private_paths=False)["assistant"]["tim_ve_bo_cut"] is True  # settings đang chạy: MỞ từ 22/11/2026


@pytest.mark.parametrize("ve, cut", [
    ("mất bao lâu?", True), ("ko phải 5", True), ("giờ mở cửa ko?", True), ("Trên đó chơi gì", True), ("Bao nhiêu km", True), ("mấy h mở", True),
    ("Lăng đó đóng cửa mấy giờ?", True), ("trong lăng thì sao?", True), ("vé bao nhiêu?", True),
    # không cụt: có tên riêng (kể cả đứng đầu vế), tên gõ thường, hoặc còn hai từ mang nội dung
    ("Mémoire ở đâu", False), ("quán nào mở khuya nữa ko", False), ("bà có được giảm ko?", False), ("có điểm nào khác ít bậc", False),
    ("đại nội mở cửa mấy giờ", False), ("Vậy đi Đại Nội + Tự Đức thì tổng vé cả nhà bao nhiêu", False), ("xe điện có tính tiền riêng ko?", False),
    # lượt đọc của phiên khác 22/11: chủ thể đi lại / dịch vụ chỉ một hai từ — vế tự tìm được, không lọc
    ("vé xe buýt bao nhiêu", False), ("vé tàu bao nhiêu", False), ("taxi bao nhiêu tiền", False), ("chợ đêm mở mấy giờ", False), ("thuê xe ở đâu", False),
    ("xe ôm giá sao", False), ("homestay giá sao", False), ("đổi tiền ở đâu", False), ("atm ở đâu", False), ("wifi có không", False),
    ("có chỗ gửi xe ko", False), ("mưa thì đi đâu trong nhà được?", False),
    ("cách bao xa?", True), ("mua ở đâu?", True), ("giá khoảng bao nhiêu?", True), ("có sđt ko?", True),   # vẫn cụt: không chủ thể
])
def test_subject_less_clause_is_recognised_by_words_only(ve, cut):
    from llm.assistant import _ve_cut
    assert _ve_cut(ve) is cut


def test_subject_less_clauses_are_dropped_from_the_search_clauses_only_when_asked():
    cu = cac_ve_tim(K22)
    assert cu == ["ko phải 5", "Vậy đi Đại Nội + Tự Đức thì tổng vé cả nhà bao nhiêu", "bà có được giảm ko?", "Bảo tàng Cổ vật vs An Định chưa rõ bậc",
                  "có điểm nào khác ít bậc", "giờ mở cửa ko?"]                                    # tắt: y như trước, kể cả hai mẩu cụt
    assert cac_ve_tim(K22, True) == [v for v in cu if v not in ("ko phải 5", "giờ mở cửa ko?")]   # bật: bỏ đúng hai mẩu đó, các vế khác giữ nguyên thứ tự
    tin = "Momiji với Mémoire ở đâu, mấy giờ mở cửa? Còn quán nào mở khuya nữa ko"
    assert cac_ve_tim(tin, True) == ["Mémoire ở đâu", "quán nào mở khuya nữa ko"]                 # hai vế máy từng gắn nhầm khi đếm: không bị lọc
    assert cac_ve_tim("mấy h mở cửa, mấy h đóng", True) == []                                      # mọi vế đều cụt ⇒ không tìm riêng vế nào (như trước khi có tính năng)


def test_subject_less_clause_switch_only_removes_passages_of_those_clauses(deps):
    """Qua lõi thật: cờ con bật ⇒ số vế tìm riêng giảm đúng bằng số vế cụt; phần tìm bằng cả tin y nguyên; không có đoạn nào MỚI; tin nhiều ý không có
    vế cụt và tin một ý ⇒ thứ gửi model giống hệt."""
    LOC = dataclasses.replace(BAT, tim_ve_bo_cut=True)
    (t_cu, _), (t_moi, _) = _chay(deps, BAT, K22), _chay(deps, LOC, K22)
    cu, moi, n_chinh = list(t_cu.packed.document_ids), list(t_moi.packed.document_ids), len(t_cu.documents)
    assert t_moi.tools[0]["n_ve"] == t_cu.tools[0]["n_ve"] - 2
    assert moi[:n_chinh] == cu[:n_chinh] and set(moi) <= set(cu) and len(moi) < len(cu)
    for cau in (CAU_HAI_Y, CAU_MOT_Y):
        (t_a, goi_a), (t_b, goi_b) = _chay(deps, BAT, cau), _chay(deps, LOC, cau)
        assert goi_a["input"] == goi_b["input"] and t_a.packed == t_b.packed
