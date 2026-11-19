"""Cờ `nho_ten_goi_y` (plan private `data/hoi_tiep_goi_y_2026-11-19/PLAN.md`) — logic thuần + chỗ ghi lịch sử, 0 USD, không nạp bộ tìm, không model.

Giữ: (1) tên lấy từ NGUỒN ĐÃ TRÍCH là bài riêng của một nơi, đúng thứ tự trích — không lấy chữ model viết; (2) lượt lịch / biểu mẫu / từ chối không
để lại ghi chú (chữ lịch có tên quán từ bản đồ mở không được vào lịch sử gửi model); (3) cờ tắt ⇒ lịch sử y như trước (chỉ câu hỏi).
Không phải bằng chứng model thật hiểu "quán đó" là quán nào — phần đó ở lượt đo có phí.
"""
from types import SimpleNamespace

import pytest

from api.conversations import ConversationStore
from api.routes.chat import _remember
from llm.assistant import AnswerTrace, AssistantFlags
from llm.generator_openai_full_corpus import with_history
from llm.ten_goi_y import TOI_DA, ghi_chu_goi_y, ten_noi_da_trich
from retrieval.full_corpus_context import PackedSource


def src(i: int, title: str, source: str) -> PackedSource:
    return PackedSource(id=i, title=title, heading_path=(), excerpts=("x",), source=source)


QUAN_A = src(1, "Quán A", "foods/restaurants/quan a.md")
QUAN_B = src(5, "Quán B", "foods/restaurants/quan b.md")
QUAN_A_DOAN_2 = src(18, "Quán A", "foods/restaurants/quan a.md")
CAM_NANG = src(2, "Cẩm nang ẩm thực", "foods/food-guides.md")
CAM_NANG_TRONG_THU_MUC_NOI = src(3, "Cẩm nang du lịch", "travel/places/travel_guides.md")
MON = src(4, "Bánh nậm", "foods/local_specialties/banh nam.md")
DICH_VU = src(6, "Lưu trú ở Huế", "travel/services/luu tru.md")
THOI_TIET = src(7, "Dự báo thời tiết", "thoi_tiet")
DIEM = src(8, "Đồi X", "travel/places/Đồi X.md")
DI_TICH = src(9, "Lăng Y", "heritages/heritage/Lăng Y.md")
CA_PHE = src(10, "Cà phê Z", "foods/cafes/ca phe z.md")


def test_names_follow_first_citation_order_and_skip_non_place_sources():
    cited = (QUAN_A, CAM_NANG, CAM_NANG_TRONG_THU_MUC_NOI, MON, QUAN_B, DICH_VU, THOI_TIET, DIEM, DI_TICH, CA_PHE, QUAN_A_DOAN_2)
    answer = "Thử Quán B.[5] Hoặc Quán A [Nguồn 1][18], xem thêm [2][3][4][6][7]. Gần đó có Đồi X [8], Lăng Y [9] và Cà phê Z.[10] Quán B ngon.[5]"
    assert ten_noi_da_trich(answer, cited) == ("Quán B", "Quán A", "Đồi X", "Lăng Y", "Cà phê Z")  # thứ tự TRÍCH, không phải thứ tự mã; mỗi bài một lần
    assert ten_noi_da_trich("Chỉ có cẩm nang.[2][3] Và món.[4]", cited) == ()
    assert ten_noi_da_trich("", cited) == () and ten_noi_da_trich("Không trích gì.", cited) == ()
    assert ten_noi_da_trich("Mã lạ.[99]", cited) == ()  # mã không có trong sổ nguồn đã trích ⇒ bỏ qua, không ném lỗi


def test_names_are_capped():
    many = tuple(src(i, f"Quán {i}", f"foods/restaurants/q{i}.md") for i in range(1, TOI_DA + 4))
    answer = " ".join(f"Quán {s.id}.[{s.id}]" for s in many)
    assert ten_noi_da_trich(answer, many) == tuple(f"Quán {i}" for i in range(1, TOI_DA + 1))


def trace(**kw) -> AnswerTrace:
    t = AnswerTrace()
    t.answer, t.cited = "Thử Quán A.[1] Hoặc Quán B.[5]", (QUAN_A, QUAN_B)
    for k, v in kw.items():
        setattr(t, k, v)
    return t


GHI_CHU = ("[Ghi chú hệ thống — câu trả lời lượt này có trích bài kho của các nơi: Quán A; Quán B. "
           "Danh sách có thể thiếu nơi đã được nêu và không theo thứ tự trong câu trả lời.]")


def test_note_claims_only_what_code_knows():
    assert "gợi ý" not in GHI_CHU and "1." not in GHI_CHU and "có thể thiếu" in GHI_CHU  # không đánh số, không nói "đã gợi ý", tự khai là có thể thiếu


@pytest.mark.parametrize("kw, mong", [
    ({}, GHI_CHU),                                                       # lượt trả lời từ kho, có trích bài riêng của nơi
    ({"bieu_mau": True}, ""),                                            # lượt biểu mẫu "Lên kế hoạch"
    ({"lich": {"ngay": []}}, ""),                                        # lượt có lịch bản 1
    ({"lich_v2": {"ngay": []}}, ""),                                     # lượt có lịch bản 2 (chữ lịch có tên quán từ bản đồ mở)
    ({"fixed_outcome": "refusal_no_sources", "cited": ()}, ""),          # lượt từ chối
    ({"fixed_outcome": "out_of_scope", "cited": ()}, ""),                # ngoài phạm vi
    ({"fixed_outcome": "lam_thay"}, ""),                                 # câu cố định do code đặt, dù sổ nguồn còn
    ({"cited": ()}, ""),                                                 # trò chuyện: không có nguồn
    ({"answer": "Theo cẩm nang.[2]", "cited": (CAM_NANG,)}, ""),         # chỉ trích bài tổng hợp ⇒ giới hạn đã nhận
])
def test_note_per_turn_kind(kw, mong):
    assert ghi_chu_goi_y(trace(**kw)) == mong


def req(flags: AssistantFlags, keep_answers: bool = False):
    store = ConversationStore(lambda text: len(text.split()), keep_answers=keep_answers)
    state = SimpleNamespace(conversations=store, assistant_flags=flags)
    return SimpleNamespace(app=SimpleNamespace(state=state)), store, store.ensure(None)


def test_route_remembers_note_only_with_flag_and_only_for_success_turns():
    bat, tat = AssistantFlags(nho_ten_goi_y=True), AssistantFlags()
    request, store, cid = req(tat)
    _remember(request, cid, "quán nào ngon", trace(), "success")
    assert store.history(cid) == (("quán nào ngon", ""),)  # cờ TẮT ⇒ lịch sử y như trước: chỉ câu hỏi

    request, store, cid = req(bat)
    _remember(request, cid, "quán nào ngon", trace(), "success")                                            # lượt đầu
    _remember(request, cid, "lên lịch 2 ngày", trace(lich_v2={"ngay": []}), "success")                      # lượt có lịch
    _remember(request, cid, "quán đó có chỗ đậu xe không", trace(fixed_outcome="refusal_no_sources", cited=(),
                                                                 answer="Tôi không tìm thấy đủ thông tin."), "refusal_no_sources")  # lượt từ chối
    assert store.history(cid) == (("quán nào ngon", GHI_CHU), ("lên lịch 2 ngày", ""), ("quán đó có chỗ đậu xe không", ""))
    # lượt hỏi tiếp: model nhận đúng một tin trợ lý là dòng ghi chú, không có chữ câu trả lời / chữ lịch
    items = with_history("cho địa chỉ quán đó", store.history(cid))
    assert [i["role"] for i in items] == ["user", "assistant", "user", "user", "user"] and items[1]["content"] == GHI_CHU
    assert all("Thử Quán A" not in i["content"] for i in items)

    request, store, cid = req(bat)
    _remember(request, cid, "x", trace(), "lam_thay")  # kết thúc khác "success" ⇒ không ghi chú dù trace còn nguồn
    assert store.history(cid) == (("x", ""),)

    request, store, cid = req(bat, keep_answers=True)  # nhớ cả câu trả lời (đường cũ) ⇒ giữ câu trả lời đã cắt mã, không dùng ghi chú
    _remember(request, cid, "quán nào ngon", trace(), "success")
    assert store.history(cid) == (("quán nào ngon", "Thử Quán A. Hoặc Quán B."),)


def test_flag_reads_from_settings_and_defaults_off():
    assert AssistantFlags().nho_ten_goi_y is False
    assert AssistantFlags.from_settings({"assistant": {"nho_ten_goi_y": True}}).nho_ten_goi_y is True


def test_run_chains_keeps_row_keys_and_passes_note_to_next_turn(monkeypatch):
    """Đường chạy chuỗi của bộ đo (`run_chains`, dùng cho lượt đo có phí) — thay bộ tìm, bộ dựng ngữ cảnh, generator và `answer_turn` bằng đồ giả
    (0 USD, không nạp gì): dòng kết quả còn đủ khoá cũ (`cau_tim_model`) + có `ghi_chu_goi_y`; lượt 2 nhận lịch sử = (câu hỏi, dòng ghi chú) khi cờ bật,
    (câu hỏi, "") khi cờ tắt. Không phải bằng chứng model thật — chỉ khoá phần nối dây."""
    import asyncio
    import evaluation.full_corpus_eval as fe

    seen = []

    async def fake_turn(question, service, cb, gen, tr, flags, *rest):
        seen.append(tr.history)
        tr.answer, tr.cited, tr.model_queries = "Thử Quán A.[1] Hoặc Quán B.[5]", (QUAN_A, QUAN_B), ["câu tìm"]

    class Gen:
        async def aclose(self):
            pass

    builder = SimpleNamespace(_tokenizer=SimpleNamespace(encode=lambda text: text.split()), _token_count=lambda *a: 0)
    monkeypatch.setattr(fe, "load_settings", lambda **kw: {"full_corpus_runtime": {"retrieval_treatment": "x"}})
    monkeypatch.setattr(fe, "build_retrieval", lambda *a: SimpleNamespace(close=lambda: None))
    monkeypatch.setattr(fe, "build_context_builder", lambda s: builder)
    monkeypatch.setattr(fe.OpenAIFullCorpusGenerator, "from_environment", classmethod(lambda cls, s: Gen()))
    monkeypatch.setattr(fe, "answer_turn", fake_turn)
    chains = [{"id": "c1", "loai": "x", "luot": [{"cau": "quán nào ngon", "ky_vong": "tra_loi"}, {"cau": "cho địa chỉ quán đó", "ky_vong": "tra_loi"}]}]
    for bat, lich_su_luot_2 in ((True, (("quán nào ngon", GHI_CHU),)), (False, (("quán nào ngon", ""),))):
        seen.clear()
        monkeypatch.setattr(fe.AssistantFlags, "from_settings", classmethod(lambda cls, s, _b=bat: AssistantFlags(nho_ten_goi_y=_b, nho_cau_tra_loi=False)))  # như settings.yaml: chỉ nhớ câu hỏi
        rows = asyncio.run(fe.run_chains(chains, "nho"))
        assert seen == [(), lich_su_luot_2]
        assert [r["cau_tim_model"] for r in rows] == [["câu tìm"], ["câu tìm"]] and [r["n_history_turns"] for r in rows] == [0, 1]
        assert [r["ghi_chu_goi_y"] for r in rows] == ([GHI_CHU, GHI_CHU] if bat else ["", ""])
