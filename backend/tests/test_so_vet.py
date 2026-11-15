"""Sổ vết debug có nội dung (`core/so_vet.py`): cờ tắt ⇒ không file; cờ bật ⇒ một dòng JSON đủ phần; ghi hỏng không ném lỗi; biến môi trường."""
import json
from types import SimpleNamespace

import pytest

from core import so_vet
from core.settings_loader import apply_env_overrides
from llm.assistant import AnswerTrace, AssistantFlags
from retrieval.full_corpus_context import PackedSource


def _trace() -> AnswerTrace:
    trace = AnswerTrace(route="tro_ly_hue", answer="Trả lời [1].", history=(("câu trước", "đáp trước"),))
    trace.cited = (PackedSource(id=1, title="Bài A", heading_path=("Mục",), excerpts=("đoạn",), source="travel/places/A.md"),)
    trace.model_queries.append("câu tìm model viết")
    trace.context_parts.append("[1] Bài A\nđoạn")
    trace.llm_calls.append({"route": "tro_ly_hue", "ms": 10.0, "usd": 0.0001, "input_tokens": 5, "output_tokens": 2})
    doc = SimpleNamespace(id="travel/places/A.md#3", score=0.51234, metadata={"source": "travel/places/A.md"})
    trace.vet["tim"] = [so_vet.vet_tim(["câu gốc"], "code", [doc] * 12, SimpleNamespace(document_ids=("travel/places/A.md#3",)))]
    trace.vet["web"] = {"cau_gui_tra_web": "câu ra web", "so_web": [{"id": 1, "title": "t", "link": "https://a.vn", "snippet": "s"}]}
    trace.web = {"outcome": "co_muc", "text": "mục web", "kiem": []}
    return trace


def test_flag_off_writes_nothing(tmp_path):
    so_vet.ghi(False, "chat", {"outcome": "success"}, _trace(), "câu gõ", "câu gửi model", thu_muc=tmp_path / "vet")
    assert not (tmp_path / "vet").exists() and AssistantFlags().so_vet is False


def test_flag_on_writes_one_json_line_with_content(tmp_path):
    metrics = {"outcome": "success", "turn_id": "abc", "git_sha": "1234567", "usd": 0.0003}
    so_vet.ghi(True, "chat_stream", metrics, _trace(), "câu gõ", "câu gửi model", thu_muc=tmp_path)
    so_vet.ghi(True, "anh", {"outcome": "ok"}, them={"anh": {"ten_goi_y": ["Đại Nội Huế"]}}, thu_muc=tmp_path)
    (tep,) = tmp_path.iterdir()
    dau, anh = [json.loads(line) for line in tep.read_text(encoding="utf-8").splitlines()]
    assert dau["so_do"] == metrics and dau["duong"] == "chat_stream"  # nguyên dòng số đo ⇒ nối với `chat_metrics` bằng turn_id / git_sha / giờ
    assert (dau["cau_go"], dau["cau_gui_model"], dau["lich_su"]) == ("câu gõ", "câu gửi model", [["câu trước", "đáp trước"]])
    tim = dau["tim_kho"][0]
    assert tim["cau"] == ["câu gốc"] and len(tim["ket_qua"]) == so_vet.TOP_TIM and tim["vao_ngu_canh"] == ["travel/places/A.md#3"]
    assert tim["ket_qua"][0] == {"chunk_id": "travel/places/A.md#3", "source": "travel/places/A.md", "diem": 0.5123}
    assert dau["cau_tim_model"] == ["câu tìm model viết"] and dau["ngu_canh"] and dau["goi_model"][0]["usd"] == 0.0001
    assert dau["tra_loi"]["chu"] == "Trả lời [1]." and dau["tra_loi"]["nguon_trich"][0]["source"] == "travel/places/A.md"
    assert dau["web"]["cau_gui_tra_web"] == "câu ra web" and dau["web"]["text"] == "mục web" and dau["web"]["so_web"][0]["link"] == "https://a.vn"
    assert anh["anh"]["ten_goi_y"] == ["Đại Nội Huế"] and "tra_loi" not in anh
    assert not any(k in json.dumps(dau).lower() for k in ("cookie", "api_key", "authorization"))


def test_write_failure_never_raises(tmp_path, caplog):
    chan = tmp_path / "la_file"
    chan.write_text("x")
    with caplog.at_level("WARNING", logger="chat"):
        so_vet.ghi(True, "chat", {"outcome": "success"}, _trace(), "a", "b", thu_muc=chan)  # thư mục đích là một FILE ⇒ mkdir hỏng
    assert "so_vet failed" in caplog.text and "câu" not in caplog.text  # cảnh báo chỉ có tên lớp lỗi, không nội dung


def test_collecting_never_raises_on_odd_documents():
    """`vet_tim` chạy trong `finally` của lần tìm (cả khi cờ tắt): tài liệu khác khuôn không được ném lỗi đè lỗi gốc của lần tìm (review B M-1)."""
    le = [SimpleNamespace(id="a#1", score=None, metadata=None)]
    assert so_vet.vet_tim(["câu"], "code", le, None) == {"cau": ["câu"], "by": "code", "loi": "AttributeError"}
    assert so_vet.vet_tim(["câu"], "model", None, None)["ket_qua"] == []


def test_merge_keeps_both_search_lists():
    from llm.assistant import _merge_spec
    chinh, phu = AnswerTrace(), AnswerTrace()
    chinh.vet["tim"], phu.vet["tim"], phu.vet["web"] = [{"cau": ["a"]}], [{"cau": ["b"]}], {"cau_gui_tra_web": "w"}
    _merge_spec(chinh, phu, None)
    assert [t["cau"] for t in chinh.vet["tim"]] == [["a"], ["b"]] and chinh.vet["web"] == {"cau_gui_tra_web": "w"}


def test_env_override():
    settings = {"assistant": {"tra_web": False}, "vector_database": {"url": "x"}}
    apply_env_overrides(settings, {})
    assert "so_vet" not in settings["assistant"]
    apply_env_overrides(settings, {"HUE_SO_VET": "true"})
    assert settings["assistant"]["so_vet"] is True and AssistantFlags.from_settings({"assistant": {"so_vet": True}}).so_vet is True
    with pytest.raises(ValueError):
        apply_env_overrides(settings, {"HUE_SO_VET": "1"})
