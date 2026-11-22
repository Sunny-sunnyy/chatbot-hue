"""Cờ `nho_cau_tra_loi` nghĩa mới (20/11/2026, plan `report_agent/2026-11-20/b_nho_cau_tra_loi_plan.md`): lịch sử mang câu trả lời của lượt LIỀN TRƯỚC — 0 USD.

Kho cuộc trò chuyện + luật "lượt nào được giữ đáp" là logic thuần. Phần route: app thật + tìm kho thật (Qdrant chỉ đọc), model là SDK thật với client trả
phản hồi dựng sẵn ⇒ đọc được đúng chuỗi lịch sử gửi model. Không phải bằng chứng model thật hiểu "quán thứ hai" — phần đó là lượt đo có phí.
"""
import json

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.conversations import CAT_LOI_TRUOC, NHAN_LOI_TRUOC, ConversationStore, dap_duoc_nho, loi_luot_truoc
from core.settings_loader import load_settings
from llm.assistant import AnswerTrace
from llm.ten_goi_y import TIEN_TO_GHI_CHU, lich_su_cho_luot
from test_b2_tool_loop import answer, generator

GHI_CHU = TIEN_TO_GHI_CHU + "Quán A; Quán B. Danh sách có thể thiếu nơi đã được nêu và không theo thứ tự trong câu trả lời.]"


def kho(**kw) -> ConversationStore:
    return ConversationStore(lambda text: len(text.split()), keep_answers=False, **kw)


def test_chi_luot_lien_truoc_giu_cau_tra_loi_luot_cu_ve_dong_ghi_chu():
    s = kho(chi_dap_lien_truoc=True)
    cid = s.ensure(None)
    s.append(cid, "Ăn cơm hến ở đâu?", "Có Quán A [1] và Quán B [2].", GHI_CHU)
    (hoi, dap), = s.history(cid)
    assert dap == f"{NHAN_LOI_TRUOC}\nCó Quán A và Quán B."  # bỏ mã trích dẫn; KHÔNG kèm dòng ghi chú (tên nơi đã ở trong câu trả lời)
    s.append(cid, "Quán thứ hai ở đường nào?", "Quán B ở đường X [3].", "")
    assert s.history(cid) == (("Ăn cơm hến ở đâu?", GHI_CHU), ("Quán thứ hai ở đường nào?", f"{NHAN_LOI_TRUOC}\nQuán B ở đường X."))
    s.append(cid, "Mở cửa mấy giờ?", "", "")  # lượt không được giữ đáp (nơi gọi đưa chữ rỗng) ⇒ ô rỗng; lượt trước về dòng ghi chú của nó (rỗng)
    assert s.history(cid)[1:] == (("Quán thứ hai ở đường nào?", ""), ("Mở cửa mấy giờ?", ""))
    s.append(cid, "Còn giá vé?", "Vé 100.000 đồng [1].", "")  # sau một lượt không giữ đáp: không có gì để hạ, lượt mới vẫn giữ đáp
    assert s.history(cid)[-2:] == (("Mở cửa mấy giờ?", ""), ("Còn giá vé?", f"{NHAN_LOI_TRUOC}\nVé 100.000 đồng."))


def test_cat_cau_tra_loi_dai_va_co_tat_thi_nhu_cu():
    dai = "chữ " * (CAT_LOI_TRUOC // 2)  # dài gấp đôi trần
    o = loi_luot_truoc(dai)
    assert o.startswith(NHAN_LOI_TRUOC + "\n") and o.endswith(" …") and len(o) <= len(NHAN_LOI_TRUOC) + 1 + CAT_LOI_TRUOC + 2
    assert loi_luot_truoc("") == "" and loi_luot_truoc("[1]") == ""
    s = kho()  # cờ tắt: chỉ câu hỏi + dòng ghi chú, y như trước
    cid = s.ensure(None)
    s.append(cid, "câu", "đáp [1]", GHI_CHU)
    s.append(cid, "câu 2", "đáp 2", "")
    assert s.history(cid) == (("câu", GHI_CHU), ("câu 2", ""))


@pytest.mark.parametrize("doi, outcome, mong", [
    (lambda t: None, "success", True),
    (lambda t: None, "refusal_no_sources", False),  # câu cố định: từ chối, ngoài phạm vi, nói thật giới hạn, hỏi lại
    (lambda t: None, "lam_thay", False),
    (lambda t: setattr(t, "bieu_mau", True), "success", False),  # lượt lịch: chữ lịch có tên quán từ bản đồ mở — model không được thấy
    (lambda t: setattr(t, "lich", {"nguon": []}), "success", False),
    (lambda t: setattr(t, "lich_v2", {"lich": {}}), "success", False),
    (lambda t: setattr(t, "sua", {"n_ap": 1}), "success", False),
    # 21/11: lượt dùng công cụ / nguồn đổi theo giờ không được giữ đáp (số dự báo, ngày, khoảng cách phải đến từ công cụ của lượt này); tìm kho, tra web,
    # liệt kê bài thì giữ
    (lambda t: t.tools.extend([{"name": "tim_kho"}, {"name": "thoi_tiet"}]), "success", False),
    (lambda t: t.tools.extend([{"name": "tim_kho"}, {"name": "lich_san"}]), "success", False),
    (lambda t: t.tools.append({"name": "ngay_lich"}), "success", False),
    (lambda t: t.tools.append({"name": "khoang_cach_san"}), "success", False),
    (lambda t: t.tools.append({"name": "lich_dang_co"}), "success", False),
    (lambda t: t.tools.extend([{"name": "tim_kho"}, {"name": "tim_kho"}, {"name": "tra_web"}]), "success", True),
    (lambda t: t.tools.extend([{"name": "tim_kho"}, {"name": "liet_ke_bai"}]), "success", True),
])
def test_luot_nao_duoc_giu_cau_tra_loi(doi, outcome, mong):
    trace = AnswerTrace(answer="đáp [1]")
    doi(trace)
    assert dap_duoc_nho(trace, outcome) is mong


def test_cau_xin_ke_lai_va_cau_go_lai_khong_lam_mat_cau_tra_loi_lien_truoc():
    lien_truoc = f"{NHAN_LOI_TRUOC}\nCó Quán A và Quán B."
    ls = (("Ăn bún ở đâu?", GHI_CHU), ("Ăn cơm hến ở đâu?", lien_truoc))
    # xin kể lại: gỡ dòng ghi chú (danh sách không đủ) nhưng GIỮ câu trả lời liền trước — danh sách thật nằm ở đó
    assert lich_su_cho_luot(ls, "Kể lại các quán vừa nêu") == (("Ăn bún ở đâu?", ""), ("Ăn cơm hến ở đâu?", lien_truoc))
    # gõ lại nguyên văn câu cũ từng có ghi chú: gỡ ghi chú của lượt cũ, câu trả lời liền trước giữ
    assert lich_su_cho_luot(ls, "Ăn bún ở đâu?") == (("Ăn bún ở đâu?", ""), ("Ăn cơm hến ở đâu?", lien_truoc))
    assert lich_su_cho_luot(ls, "Quán thứ hai ở đường nào?") == ls  # câu thường: nguyên


# ---------- Route thật, model dựng sẵn ----------

def kich_ban(script_calls: list):
    def script(n, kw):
        script_calls.append(kw)
        instructions = kw.get("instructions") or ""
        if "tro_ly_hue" in instructions and "ngoai_pham_vi" in instructions:  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        return [answer(f"Câu trả lời số {sum('ngoai_pham_vi' not in (c.get('instructions') or '') for c in script_calls)} [1].")]
    return script


def tin_tro_ly(kw) -> list[str]:
    """Các tin vai trợ lý trong lịch sử của một lần gọi model (chỉ tin dạng chữ do route đưa vào)."""
    return [i["content"] for i in kw["input"] if isinstance(i, dict) and i.get("role") == "assistant" and isinstance(i.get("content"), str)]


@pytest.mark.parametrize("bat", [True, False])
def test_route_gui_cau_tra_loi_lien_truoc_chi_khi_co_bat(bat):
    app = create_app(load_settings())
    with TestClient(app) as client:
        goc = app.state.generator, app.state.generator_ready, app.state.tim_web, app.state.conversations
        calls: list = []
        app.state.generator, app.state.generator_ready, app.state.tim_web = generator(kich_ban(calls)), True, None
        app.state.cache_tra_loi = None  # không để bộ nhớ giữa các cuộc trò chuyện chen vào phép đếm
        app.state.conversations = ConversationStore(lambda t: len(t.split()), keep_answers=False, chi_dap_lien_truoc=bat)
        for cau in ("Đại Nội Huế mở cửa lúc mấy giờ?", "Còn giá vé ở đó thì sao?", "Đi từ ga Huế tới đó bằng gì?"):
            assert client.post("/api/chat", json={"query": cau}).status_code == 200
        app.state.generator, app.state.generator_ready, app.state.tim_web, app.state.conversations = goc
    viet = [kw for kw in calls if "ngoai_pham_vi" not in (kw.get("instructions") or "")]  # các lần gọi trợ lý (không tính định tuyến)
    luot_1, luot_2, luot_3 = viet[0], viet[1], viet[-1]
    assert isinstance(luot_1["input"], list) and tin_tro_ly(luot_1) == []  # lượt đầu: không lịch sử
    if not bat:
        assert all(NHAN_LOI_TRUOC not in t for kw in viet for t in tin_tro_ly(kw))  # cờ tắt: không lượt nào thấy câu trả lời cũ
        return
    assert tin_tro_ly(luot_2) == [f"{NHAN_LOI_TRUOC}\nCâu trả lời số 1."]  # lượt hai thấy đáp lượt một, đã bỏ mã [1]
    lien_truoc = [t for t in tin_tro_ly(luot_3) if t.startswith(NHAN_LOI_TRUOC)]
    assert len(lien_truoc) == 1 and "Câu trả lời số 2." in lien_truoc[0] and "Câu trả lời số 1." not in "".join(tin_tro_ly(luot_3))  # lượt ba: chỉ đáp lượt hai


def test_bedrock_messages_carry_the_remembered_answer_only_for_the_last_turn():
    """Đường Sonnet (lớp dịch): lịch sử chỉ nhớ câu hỏi ⇒ giữa hai câu hỏi liền nhau lớp dịch chèn dòng giữ chỗ. Khi lượt liền trước có đáp được nhớ, chỗ đó
    là CHỮ THẬT (nhãn + câu trả lời đã bỏ mã trích dẫn) — không còn dòng giữ chỗ cho cặp cuối; các cặp cũ hơn vẫn là dòng giữ chỗ. Không sửa lớp dịch."""
    from llm.bedrock_model import HISTORY_GAP, to_messages
    from llm.generator_openai_full_corpus import with_history

    nho = loi_luot_truoc("Có Quán A [1] và Quán B [2].")
    tin = [(m["role"], m["content"][0]["text"]) for m in to_messages(with_history("Quán thứ hai ở đâu?", (("Ăn bún ở đâu?", ""), ("Ăn cơm hến ở đâu?", nho))))]
    assert tin == [("user", "Ăn bún ở đâu?"), ("assistant", HISTORY_GAP), ("user", "Ăn cơm hến ở đâu?"), ("assistant", nho), ("user", "Quán thứ hai ở đâu?")]
    assert nho.startswith(NHAN_LOI_TRUOC) and "[1]" not in nho and "Quán B" in nho
