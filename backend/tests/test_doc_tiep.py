"""Bản thử công cụ `doc_tiep` (nhánh thu-b-mo-doc-tiep, 24/11/2026): chọn đoạn kề + hàm của một lượt. Không model, không Qdrant."""
import asyncio

import pytest

from core.schema import RetrievedDocument
from llm import assistant as a
from llm.full_corpus_prompt import TOOL_LIMIT_TEXT
from retrieval.full_corpus_context import FullCorpusContextBuilder, PackedSource


class _Tok:
    def encode(self, s):
        return s.split()


def _doan(so: int, muc: tuple[str, ...]) -> RetrievedDocument:
    return RetrievedDocument(id=f"x/bai.md#{so}", score=0.0, text="giá vé người lớn 150.000 đồng" if so == 9 else f"chữ {so}",
                             metadata={"source": "x/bai.md", "title": "Bài", "heading_path": list(muc), "domain": "x",
                                       "evidence_parts": [{"role": "body", "text": "vé người lớn 150.000 đồng" if so == 9 else f"chữ của đoạn {so}", "start": 0, "end": 1}]})


BAI = [_doan(i, ("Bài", "Lịch sử") if i < 4 else ("Bài", "Tham quan") if i < 8 else ("Khác",)) for i in range(10)]


class _Kho:
    def __init__(self):
        self.goi = []

    def doan_cua_bai(self, source):
        self.goi.append(source)
        return list(BAI) if source == "x/bai.md" else []


def test_chon_doan_khop_tu_truoc_roi_ke_cung_muc():
    doan = [(int(d.id.rsplit("#", 1)[1]), tuple(d.metadata["heading_path"]), d.id, d.text) for d in BAI]
    # không từ nào khớp ⇒ thuần "kề": ba đoạn cùng mục (4, 6, 7) + đoạn gần nhất của mục cùng cấp đầu (3); đọc xuôi
    assert a.chon_doan_trong_bai(doan, 5, ("Bài", "Tham quan"), frozenset({"x/bai.md#5"}), "không có từ nào", k=4) == ["x/bai.md#3", "x/bai.md#4", "x/bai.md#6", "x/bai.md#7"]
    # có từ khớp ⇒ đoạn xa (mục khác, cuối bài) vẫn được chọn trước các đoạn kề
    assert a.chon_doan_trong_bai(doan, 5, ("Bài", "Tham quan"), frozenset({"x/bai.md#5"}), "Giá vé", k=2) == ["x/bai.md#4", "x/bai.md#9"]
    assert a.chon_doan_trong_bai(doan, 5, ("Bài", "Tham quan"), frozenset(d[2] for d in doan), "giá vé") == []
    assert len(a.chon_doan_trong_bai(doan, 0, ("Bài", "Lịch sử"), frozenset(), "")) == a.SO_DOAN_DOC_TIEP


def _luot(limit=3):
    trace = a.AnswerTrace()
    trace.so_nguon.append(PackedSource(1, "Bài", ("Bài", "Tham quan"), ("chữ của đoạn 5",), "x/bai.md"))
    trace.so_nguon.append(PackedSource(2, "Mục lục", ("nhóm",), ("dòng",), "muc-luc"))  # nguồn do code dựng: không có mã đoạn
    trace.seen_ids.append("x/bai.md#5")
    trace.context_parts.append("[Nguồn 1]…")
    trace.ma_doan[1] = "x/bai.md#5"
    kho = _Kho()
    return trace, kho, a.doc_tiep_for_turn("câu hỏi", kho, FullCorpusContextBuilder(_Tok(), max_documents=10), trace, None, "lời dặn", limit)


def test_doc_tiep_noi_so_nguon_va_danh_so_tiep():
    trace, kho, fn = _luot()
    chu = asyncio.run(fn(1, "giá vé"))
    assert "150.000" in chu and kho.goi == ["x/bai.md"] and "[Nguồn 3]" in chu and "[Nguồn 1]" not in chu and "[Nguồn 2]" not in chu
    assert [s.id for s in trace.so_nguon] == list(range(1, 3 + a.SO_DOAN_DOC_TIEP))
    assert "x/bai.md#5" not in trace.seen_ids[1:] and len(trace.seen_ids) == 1 + a.SO_DOAN_DOC_TIEP
    assert trace.ma_doan[3].startswith("x/bai.md#") and trace.model_searches == 1
    assert trace.tools[-1]["name"] == "doc_tiep" and trace.tools[-1]["n_new"] == a.SO_DOAN_DOC_TIEP and trace.tools[-1]["cung_muc"] == 3
    assert trace.vet["tim"][-1]["cau"] == ["doc_tiep:x/bai.md#5"] and len(trace.vet["tim"][-1]["vao_ngu_canh"]) == a.SO_DOAN_DOC_TIEP
    asyncio.run(fn(1, "giá vé"))  # lần hai: ba đoạn còn lại của bài
    assert len(trace.seen_ids) == 10 and asyncio.run(fn(1, "giá vé")) == a.DOC_TIEP_HET


def test_doc_tiep_nguon_khong_phai_doan_va_het_luot():
    trace, kho, fn = _luot(limit=1)
    assert asyncio.run(fn(2, "giá vé")) == a.DOC_TIEP_KHONG_CO and kho.goi == [] and len(trace.so_nguon) == 2 and trace.model_searches == 0  # số nguồn sai không mất lượt
    trace.model_searches = 1  # `tim_kho` đã dùng hết lượt (trần 1) ⇒ chung bộ đếm
    assert asyncio.run(fn(1, "giá vé")) == TOOL_LIMIT_TEXT and trace.tools[-1].get("het_luot") is True and len(trace.so_nguon) == 2


def test_cong_tac_mac_dinh_tat_va_can_tim_them():
    assert a.AssistantFlags().doc_tiep is False
    with pytest.raises(ValueError):
        a.AssistantFlags(doc_tiep=True)
