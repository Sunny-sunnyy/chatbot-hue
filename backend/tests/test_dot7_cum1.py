"""Kiểm thử Đợt 7 Cụm 1 (P0–P18 trừ P5, 0 USD): tái hiện đỏ trên gốc và xanh sau sửa."""
from __future__ import annotations

import asyncio
import copy
import datetime as dt
import json
import shutil
import subprocess
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from agents.exceptions import ModelBehaviorError
from agents.tool_context import ToolContext
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.conversations import ConversationStore, dap_duoc_nho, dau_lich
from api.gioi_han import ChanLuot, GioiHanLuot
from api.hanh_trinh_chuan import chuan_hoa_lich
from api.lich_ics import dung_ics
from api.routes import chat as r_chat
from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents
from api.routes.ho_so import _mot_muc, _su_kien as ho_so_su_kien
from api.routes.hoan_tac import router as hoan_tac_router
from api.routes.xuat import THU_MUC_ANH, lich_tu_luu, router as xuat_router
from core.settings_loader import BACKEND_DIR, load_settings
from llm import goi_y_luu_tru as gylt
from llm import ho_so_chu_de as hs
from llm import len_ke_hoach as lkh
from llm import lich_trinh_v2 as lt2
from llm import luu_tru_lich as ltl
from llm import mua_nang as mn
from llm import sua_lich_v2 as sl
from llm import thoi_tiet as tt
from llm.assistant import (
    AnswerTrace,
    AssistantFlags,
    _finish_generated,
    _lich_extra,
    _thoi_tiet_cuoi,
    answer_turn_stream,
    goi_y_luu_tru_for_turn,
    luoi_cuoi_bao,
    set_notice,
)
from llm.generator_openai_full_corpus import GeneratedText, OpenAIFullCorpusGenerator
from llm.slide_designer import DayItemSlot, OverviewDayItem, SlideDayPlan, SlideDeckPlan, hau_kiem_slide_deck
from retrieval.full_corpus_context import PackedSource
from test_chat_stream import parse_sse

REPO_ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")


def _bang_v2_va_lt():
    s = load_settings(validate_private_paths=False)
    bang_v2 = lt2.nap_bang_v2(BACKEND_DIR / s["assistant"]["lich_trinh_bang_v2"])
    bang_lt = ltl.nap_bang_luu_tru(BACKEND_DIR / s["assistant"]["lich_trinh_bang_luu_tru"], bang_v2.cum)
    return s, bang_v2, bang_lt


async def _du_bao_mua_to():
    ngay = tt.hom_nay_vn()
    return tt.DuBao("ok", [{"ngay": ngay, "mua": 110.0, "tmax": 28.0, "tmin": 21.0, "xs": 95}], "18:00")


# ---------- P0: nhận diện "sạt" địa hình/đường đi, giữ đối chứng âm vl_01 & "an toàn gửi xe" ----------

def test_p0_sat_dia_hinh_duoc_nhan_nhung_an_toan_gui_xe_van_chan():
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Đường lên Bạch Mã có bị sạt không?", ()) is True
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Đèo Hải Vân có sạt không?", ()) is True
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Phí gửi xe ô tô qua đêm ở Đại Nội là bao nhiêu?", ()) is False
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Gửi xe ở Bảo tàng Cổ vật có an toàn không?", ()) is False
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("An toàn gửi xe qua đêm ở Huế thế nào?", ()) is False

    async def fake_du_bao():
        return tt.DuBao("ok", [{"ngay": tt.hom_nay_vn(), "mua": 2.0, "tmax": 28.0, "tmin": 21.0, "xs": 20}], "18:00")

    flags = AssistantFlags(tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, cong_cong_cu="linh_hoat", du_bao=fake_du_bao)
    tr = AnswerTrace(answer="Đường lên Bạch Mã có thể bị ảnh hưởng.")
    q = "Đường lên Bạch Mã có bị sạt không?"
    extra = _lich_extra(q, None, None, tr, None, None, flags)
    asyncio.run(extra["thoi_tiet_fn"]("bao_lu", 0, 0))
    assert not tr.tools[-1].get("chan_khong_thoi_tiet")
    _thoi_tiet_cuoi(tr)
    luoi_cuoi_bao(q, tr, flags)
    assert tt.CAU_BAO_LU in (tr.answer or "") + (tr.notice or "")


# ---------- P1: phép xét bão/lũ thống nhất khi chạy lại & đảo thứ tự tool ----------

def test_p1_bao_lu_lan_dau_va_dao_thu_tu_tool_chan_luu_tru_va_giu_112():
    _, bang_v2, bang_lt = _bang_v2_va_lt()
    flags = AssistantFlags(
        tim_them=True,
        thoi_tiet=True,
        bao_lu_cong_cu=True,
        cong_cong_cu="linh_hoat",
        du_bao=_du_bao_mua_to,
        goi_y_mua_nang=True,
        goi_y_luu_tru=True,
        luu_tru_bang=bang_lt,
        bang_lich_v2=bang_v2,
    )
    q = "Biển động mạnh, tối nay có chỗ nghỉ nào gần Lăng Cô?"
    tr = AnswerTrace(bao_lu_lan_dau=True, answer="Văn bản lượt hai")
    extra = _lich_extra(q, None, None, tr, None, None, flags)
    assert "goi_y_luu_tru_fn" not in extra
    assert "mua_nang_fn" not in extra
    _thoi_tiet_cuoi(tr)
    luoi_cuoi_bao(q, tr, flags)
    assert tt.CAU_BAO_LU in (tr.answer or "")

    # Đảo thứ tự: câu hỏi có từ "thời tiết" (nên được cấp `thoi_tiet`), nhưng chưa mang từ khoá bão nên được cấp cả `goi_y_luu_tru`;
    # model gọi `goi_y_luu_tru` TRƯỚC khi tự chọn `thoi_tiet("bao_lu")` trong cùng 1 lượt
    tr_dao = AnswerTrace()
    q_dao = "Tối nay ở Lăng Cô thời tiết thế nào, nên chọn chỗ nghỉ nào?"
    extra_dao = _lich_extra(q_dao, None, None, tr_dao, None, None, flags)
    assert "goi_y_luu_tru_fn" in extra_dao
    asyncio.run(extra_dao["goi_y_luu_tru_fn"](khu="ven_bien_nam"))
    asyncio.run(extra_dao["thoi_tiet_fn"]("bao_lu", 0, 0))
    tr_dao.generated = GeneratedText("Gợi ý cơ sở A [1].", None, "gpt-6-luna", None, None, None, 0)
    _finish_generated(tr_dao, flags, q_dao)
    assert not tr_dao.goi_y_luu_tru
    assert all(s.source != gylt.NGUON_SOURCE for s in tr_dao.so_nguon)
    assert all(s.source != gylt.NGUON_SOURCE for s in (tr_dao.cited or ()))
    assert tt.CAU_BAO_LU in (tr_dao.answer or "") or tr_dao.answer == tt.CAU_DAN_BAO_LU
    assert "Gợi ý cơ sở A" not in (tr_dao.answer or "")

    # Ca A (finding verifier): model trích nguồn KB [99] (không trích NGUON_SOURCE) sau khi gọi goi_y_luu_tru -> thoi_tiet("bao_lu")
    kb_src = PackedSource(99, "Lăng Cô", ("Tổng quan",), ("Khu nghỉ dưỡng tại Lăng Cô",), "travel/lang_co.md")
    tr_a = AnswerTrace(so_nguon=[kb_src])
    extra_a = _lich_extra(q_dao, None, None, tr_a, None, None, flags)
    asyncio.run(extra_a["goi_y_luu_tru_fn"](khu="ven_bien_nam"))
    asyncio.run(extra_a["thoi_tiet_fn"]("bao_lu", 0, 0))
    tr_a.generated = GeneratedText("Bạn có thể ở Laguna Lăng Cô [99].", None, "gpt-6-luna", None, None, None, 0)
    _finish_generated(tr_a, flags, q_dao)
    assert tr_a.citation_error is None
    assert "Laguna" not in (tr_a.answer or "")
    assert (tr_a.answer or "").startswith(tt.CAU_DAN_BAO_LU)
    assert tt.CAU_BAO_LU in (tr_a.answer or "")
    assert all(s.source != gylt.NGUON_SOURCE for s in tr_a.so_nguon)

    # Ca B (finding verifier): có số thời tiết lạ không nguồn ("Nhiệt độ 35°C.") kèm NGUON_SOURCE [1] -> không bị _go_so_la khôi phục lại
    tr_b = AnswerTrace()
    extra_b = _lich_extra(q_dao, None, None, tr_b, None, None, flags)
    asyncio.run(extra_b["goi_y_luu_tru_fn"](khu="ven_bien_nam"))
    asyncio.run(extra_b["thoi_tiet_fn"]("bao_lu", 0, 0))
    tr_b.generated = GeneratedText("Gợi ý cơ sở A [1]. Nhiệt độ 35°C.", None, "gpt-6-luna", None, None, None, 0)
    _finish_generated(tr_b, flags, q_dao)
    assert tr_b.citation_error is None
    assert "Gợi ý cơ sở A" not in (tr_b.answer or "")
    assert "35" not in (tr_b.answer or "")
    assert (tr_b.answer or "").startswith(tt.CAU_DAN_BAO_LU)
    assert tt.CAU_BAO_LU in (tr_b.answer or "")

    # Ca C (finding verifier): stream `giu_chu_toi_kiem` (`cho_kiem`) không phát chữ lưu trú cũ khi P1 đã thay `trace.answer`
    flags_stream = AssistantFlags(
        lan_tim_dau="v2",
        tim_them=True,
        thoi_tiet=True,
        bao_lu_cong_cu=True,
        cong_cong_cu="linh_hoat",
        du_bao=_du_bao_mua_to,
        goi_y_luu_tru=True,
        luu_tru_bang=bang_lt,
        bang_lich_v2=bang_v2,
        giu_chu_toi_kiem=True,
    )

    class _FakeStreamGen:
        chu_ve_mot_lan = True
        timeout = 5
        model = "gpt-6-luna"
        max_turns = 6
        assistant_instructions = "ok"

        def start_tools_stream(self, tool_prompt, tool_fn, **extra):
            async def _events():
                await extra["goi_y_luu_tru_fn"](khu="ven_bien_nam")
                await extra["thoi_tiet_fn"]("bao_lu", 0, 0)
                yield SimpleNamespace(
                    type="raw_response_event",
                    data=SimpleNamespace(type="response.output_text.delta", delta='{"answer":"Gợi ý khách sạn A [1]."}'),
                )

            res = SimpleNamespace(stream_events=_events, cancel=lambda: None)
            return res, SimpleNamespace(calls=[]), {}

        def finish_answer_stream(self, result, call_log, started, state):
            return GeneratedText("Gợi ý khách sạn A [1].", None, "gpt-6-luna", None, None, None, 0)

    async def _run_stream():
        tr_s = AnswerTrace()
        evs = [ev async for ev in answer_turn_stream(q_dao, None, None, _FakeStreamGen(), tr_s, flags_stream)]
        return tr_s, evs

    tr_s, evs = asyncio.run(_run_stream())
    streamed_text = "".join(d for k, d in evs if k == "delta")
    assert tr_s.citation_error is None
    assert "Gợi ý khách sạn A" not in streamed_text
    assert tt.CAU_DAN_BAO_LU in streamed_text and tt.CAU_BAO_LU in streamed_text


# ---------- P2: mua_nang kiểm ngưỡng >= 100mm khi ngay=None ----------

def test_p2_mua_nang_kiem_nguong_100mm_khi_ngay_none():
    d = dt.date(2026, 11, 28)
    kq = tt.DuBao("ok", [{"ngay": d, "mua": 110.0, "tmax": 29.0, "tmin": 22.0, "xs": 100}], "18:00")
    p = {"id": "p", "ten": "Bảo tàng mẫu", "trong_nha": "trong_nha", "cum": "kinh_thanh", "buoi": ("sang",), "thoi_luong": "ngan", "loai": "di_tich"}
    b = lt2.BangV2((p,), {"p": p}, {}, {}, (), None)
    dong, chon, nguy_hiem = mn.ket_qua(b, None, "mua", mn.KHONG_RO, "sang", None, kq_du_bao=kq, hom_nay=d)
    assert (dong, chon, nguy_hiem) == ((), [], True)

    # Đối chứng mưa nhẹ: ngay=None giữ dong_du_bao=None (không in dòng dự báo)
    kq_nhe = tt.DuBao("ok", [{"ngay": d, "mua": 10.0, "tmax": 29.0, "tmin": 22.0, "xs": 50}], "18:00")
    dong_nhe, chon_nhe, nguy_hiem_nhe = mn.ket_qua(b, None, "mua", mn.KHONG_RO, "sang", None, kq_du_bao=kq_nhe, hom_nay=d)
    assert nguy_hiem_nhe is False and len(chon_nhe) == 1
    assert not any(line.startswith("Dự báo ngày") for line in dong_nhe)


# ---------- P8: hoàn tác bảo toàn an_toan còn hiệu lực & trả an_toan ra JSON/UI/PPTX ----------

def test_p8_hoan_tac_bao_toan_an_toan_hien_tai_va_tra_ra_json_pptx():
    _, bang_v2, _ = _bang_v2_va_lt()
    s_cfg = load_settings(validate_private_paths=False)
    flags = AssistantFlags.from_settings(s_cfg)
    khung_a = lt2.xep_v2(bang_v2, lt2.tu_truong({"so_ngay": "2", "nguoi_lon": 2, "ngan_sach": "vua"}), ngay_bat_dau=dt.date(2026, 12, 10))
    ten_bo = bang_v2.theo_id[lt2.diem_v2(khung_a)[0]]["ten"]
    kq = sl.ap(bang_v2, sl.luu_tu_lich(khung_a, "2026-12-10", None), [sl.HanhDong(loai="bo_diem", ten=ten_bo)])
    a = sl.luu_tu_lich(khung_a, "2026-12-10", None)
    b = kq["luu"]

    store = ConversationStore(len)
    cid = store.ensure(None)
    store.luu_lich(cid, a)
    store.luu_lich(cid, b, truoc=a, dong=("Đã bỏ một điểm.",))
    # Lượt sau làm phát sinh cảnh báo bão/lũ trên khung hiện tại B (an_toan gắn vào B, snapshot A chưa có)
    store.luu_lich(cid, {**b, "an_toan": tt.CAU_BAO_LU})

    app = FastAPI()
    app.include_router(hoan_tac_router)
    app.include_router(xuat_router)
    app.state.conversations = store
    app.state.assistant_flags = flags
    client = TestClient(app)

    r_undo = client.post("/api/lich/hoan_tac", json={"ma": dau_lich(b)}, cookies={"conversation_id": cid})
    assert r_undo.status_code == 200
    body = r_undo.json()
    assert body.get("an_toan") == tt.CAU_BAO_LU
    assert store.lay_lich(cid).get("an_toan") == tt.CAU_BAO_LU

    r_pptx = client.get("/api/lich/pptx", cookies={"conversation_id": cid})
    assert r_pptx.status_code == 200
    import pptx
    import io
    prs = pptx.Presentation(io.BytesIO(r_pptx.content))
    all_text = "\n".join(p.text for slide in prs.slides for sh in slide.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs)
    assert tt.CAU_BAO_LU in all_text

    # UI chat.jsx nhận du.an_toan từ phản hồi /api/lich/hoan_tac
    chat_jsx = (REPO_ROOT / "frontend/src/chat.jsx").read_text(encoding="utf-8")
    assert "du.an_toan" in chat_jsx


# ---------- P18: Hồ sơ chủ đề — trích đa nguồn không xoá dòng cảnh báo của bài B ----------

def test_p18_ho_so_trich_da_nguon_khong_mat_canh_bao_bai_khac():
    def _d(rel, so, muc, chu):
        return SimpleNamespace(
            id=f"{rel}#{so}",
            text=chu,
            metadata={"source": rel, "title": rel.rsplit("/", 1)[-1][:-3], "heading_path": [muc], "domain": "x",
                      "evidence_parts": [{"role": "body", "text": chu, "start": 0, "end": 1}]},
        )

    bai = [SimpleNamespace(rel=f"travel/places/Bãi biển {t}.md", tieu_de=f"Bãi biển {t}", tom_tat="") for t in ("A", "B", "C", "D", "E")]

    class _KhoDaNguon:
        def doan_cua_bai(self, rel):
            return [
                _d(rel, 0, "Tổng quan", f"giới thiệu tổng quan {rel}"),
                _d(rel, 1, "Đặc điểm", f"bãi cát dài tại {rel}"),
                _d(rel, 2, "Mùa mưa bão và biển động", "Từ tháng 9 đến tháng 12 biển động, sóng lớn, chính quyền cấm tắm."),
            ]

    class MayDaNguon:
        async def viet_so_tay(self, loai, prompt, log):
            # Nguồn 1,2,3 = A (3 là cảnh báo của A); 4,5,6 = B (4 là tổng quan của B, 6 là cảnh báo của B)
            return {
                "y": [
                    {"chu": "Bãi biển A cấm tắm khi biển động", "nguon": [3, 4]},
                    {"chu": "Bãi biển B có bãi cát dài", "nguon": [5]},
                ]
            }

    muc = asyncio.run(
        _mot_muc(
            {"id": "m1", "ten": "Các bãi biển", "bai_goc": bai[:2]},
            "Biển và đầm phá",
            SimpleNamespace(retrieval_service=_KhoDaNguon()),
            SimpleNamespace(the_noi_bang=None),
            MayDaNguon(),
            {"goi_model": 0, "bo_khong_nguon": 0, "bo_qua_dai": 0, "bo_gio_gia": 0, "bo_qua_tran": 0, "tro_an_toan": 0},
        )
    )
    tro_b = [d for d in muc["doan"] if d["kieu"] == "an_toan" and d["nhan"] is None and "Bãi biển B" in (d["chu"] or "")]
    assert len(tro_b) == 1 and tro_b[0]["so"] == [6]


# ---------- P4 + P3 + P11: lưu trú nới hạng, chặn nhớ đáp/bịa giá, dữ liệu có kiểu qua SSE & JSON ----------

def test_p4_noi_hang_co_co_va_chu_ro_rang():
    bang_1sao = {"co_so": [{"ten": "Nhà nghỉ Mẫu", "khu": ltl.KHU_TAY, "xep_hang": "1 sao", "dia_chi": "1 Kim Long", "nguon": "Cục DL"}]}
    txt, data = gylt.ket_qua_co_kieu(bang_1sao, None, khu="phia_tay", hang_sao="cao")
    assert data["da_noi_hang"] is True
    assert "Hạng: cao" not in txt
    assert "Đã nới hạng" in txt

    # Đối chứng khớp hạng: da_noi_hang=False
    txt_ok, data_ok = gylt.ket_qua_co_kieu(bang_1sao, None, khu="phia_tay", hang_sao="binh_dan")
    assert data_ok["da_noi_hang"] is False and "Hạng: binh_dan" in txt_ok


def test_p3_chan_nho_dap_va_bia_gia_phong_co_ma_trich_dan():
    src = PackedSource(1, gylt.TIEU_DE_NGUON, (gylt.MUC_NGUON,), ("Cơ sở mẫu (2 sao)", gylt.NHAN), gylt.NGUON_SOURCE)
    tr_gia = AnswerTrace(
        so_nguon=[src],
        goi_y_luu_tru=[{"n": 1}],
        tools=[{"name": "goi_y_luu_tru"}],
        generated=GeneratedText("Cơ sở mẫu còn phòng tối nay, giá 850.000 đồng [1].", None, "gpt-6-luna", None, None, None, 0),
    )
    _finish_generated(tr_gia, AssistantFlags(), "Gợi ý chỗ ở tối nay")
    assert tr_gia.citation_error is not None
    assert dap_duoc_nho(tr_gia, "retracted", mo_cho_cuoc_co_lich=True) is False

    # Chữ viết tắt giá dạng "1,2tr/đêm" cũng bị chặn nếu không nằm trong KB
    tr_tr = AnswerTrace(
        so_nguon=[src],
        goi_y_luu_tru=[{"n": 1}],
        tools=[{"name": "goi_y_luu_tru"}],
        generated=GeneratedText("Cơ sở mẫu giá khoảng 1,2tr/đêm [1].", None, "gpt-6-luna", None, None, None, 0),
    )
    _finish_generated(tr_tr, AssistantFlags(), "Gợi ý chỗ ở tối nay")
    assert tr_tr.citation_error is not None

    # Câu hợp lệ (chỉ nêu sao, không bịa giá/còn phòng): qua kiểm nhưng vẫn KHÔNG được nhớ đáp
    tr_ok = AnswerTrace(
        so_nguon=[src],
        goi_y_luu_tru=[{"n": 1}],
        tools=[{"name": "goi_y_luu_tru"}],
        generated=GeneratedText("Cơ sở mẫu được xếp 2 sao [1].", None, "gpt-6-luna", None, None, None, 0),
    )
    _finish_generated(tr_ok, AssistantFlags(), "Gợi ý chỗ ở tối nay")
    assert tr_ok.citation_error is None
    assert dap_duoc_nho(tr_ok, "success", mo_cho_cuoc_co_lich=True) is False


def test_p11_du_lieu_luu_tru_co_kieu_qua_sse_va_json():
    _, bang_v2, bang_lt = _bang_v2_va_lt()
    tr = AnswerTrace()
    fn = goi_y_luu_tru_for_turn(tr, bang_lt, bang_v2)
    asyncio.run(fn(khu="ven_bien_nam", hang_sao="tat_ca", so_khach=2))
    tr.answer = "Bạn có thể tham khảo các cơ sở ở Lăng Cô [1]."
    tr.cited = (tr.so_nguon[0],)

    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    events = parse_sse(stream.finish(tr))
    ev_lt = [d for k, d in events if k == "luu_tru"]
    assert len(ev_lt) == 1
    payload = ev_lt[0]
    assert payload["nhan"] == ltl.NHAN and isinstance(payload["da_noi_hang"], bool)
    assert payload["co_so"] and {"ten", "xep_hang", "dia_chi", "vi_tri", "links"} <= set(payload["co_so"][0])
    assert set(payload["co_so"][0]["links"]) == {"booking", "agoda", "traveloka"}

    # ChatResponse (non-stream JSON) cũng có field luu_tru
    assert "luu_tru" in r_chat.ChatResponse.model_fields

    if NODE is not None:
        js_code = (
            "import { theKhachSan } from './frontend/src/theKhachSan.js';"
            "const turn = { phase: 'done', outcome: 'success', sources: [{ id: 1, bai_id: null }],"
            "  text: 'Bạn có thể tham khảo các cơ sở ở Lăng Cô.',"
            f"  luuTru: {json.dumps(payload, ensure_ascii=False)} }};"
            "const cards = theKhachSan(turn, []);"
            "console.log(JSON.stringify({ n: cards.length, links: Object.keys(cards[0]?.links || {}) }));"
        )
        res = subprocess.run([NODE, "--input-type=module", "-e", js_code], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        parsed = json.loads(res.stdout.strip())
        assert parsed["n"] >= 1 and set(parsed["links"]) == {"booking", "agoda", "traveloka"}


# ---------- P9: Slide Designer hau_kiem kiểm overview_summaries & day_number khớp id_muc ----------

def test_p9_hau_kiem_overview_va_day_number():
    canonical = {
        "schema_version": "1.0",
        "tham_so": {"ngay_di": "2026-12-10"},
        "ngay": [
            {"ngay": 1, "ngay_thang": "2026-12-10", "chang": ["Kinh thành"], "muc": [{"id_muc": "n1-sang-1", "ten": "Đại Nội Huế", "loai": "tham_quan", "gio": "08:00 – 09:00", "cau": "Hoàng thành."}]},
            {"ngay": 2, "ngay_thang": "2026-12-11", "chang": [], "muc": []},
        ],
        "anh_manifest": {"diem": {}, "khach_san": {}},
        "o_dau": None,
    }
    plan_bad_ov = SlideDeckPlan(
        theme_id="di_san_tram",
        cover_layout="cover_split",
        deck_title="Lịch Huế",
        deck_subtitle="2 ngày",
        highlights=["Đại Nội Huế"],
        hero_image_id=None,
        secondary_image_ids=[],
        include_overview=True,
        overview_summaries=[OverviewDayItem(ngay=1, summary="Giá phòng 2.000.000 đồng · Tác giả ảnh: ABC")],
        days=[SlideDayPlan(day_number=1, layout_id="day_timeline", day_header="Ngày 1", route_summary="Kinh thành", items=[DayItemSlot(id_muc="n1-sang-1")])],
        include_lodging=False,
        lodging_indices=[],
    )
    errs_ov = hau_kiem_slide_deck(plan_bad_ov, canonical)
    assert any("chua_gia_tien" in e or "chua_ghi_cong_anh" in e for e in errs_ov)

    plan_bad_day = SlideDeckPlan(
        theme_id="di_san_tram",
        cover_layout="cover_split",
        deck_title="Lịch Huế",
        deck_subtitle="2 ngày",
        highlights=["Đại Nội Huế"],
        hero_image_id=None,
        secondary_image_ids=[],
        include_overview=False,
        overview_summaries=[],
        days=[SlideDayPlan(day_number=2, layout_id="day_timeline", day_header="Ngày 2", route_summary="Kinh thành", items=[DayItemSlot(id_muc="n1-sang-1")])],
        include_lodging=False,
        lodging_indices=[],
    )
    errs_day = hau_kiem_slide_deck(plan_bad_day, canonical)
    assert any("lech_ngay_muc" in e for e in errs_day)


# ---------- P10: lich_id độc lập trong UID .ics (Python + JS), giữ qua sửa/hoàn tác, giữ itinerary_hash ----------

def test_p10_lich_id_doc_lap_trong_uid_ics_va_giu_hash_cache():
    def _raw(ten, lich_id):
        return {
            "lich_id": lich_id,
            "tham_so": {"ngay_di": "2026-12-10"},
            "ngay": [{"ngay": 1, "ngay_thang": "2026-12-10", "muc": [{"id_muc": "n1-sang-1", "ten": ten, "buoi": "sang", "loai": "tham_quan", "gio": "08:00 – 09:00"}]}],
        }

    c1 = chuan_hoa_lich(_raw("Đại Nội Huế", "lich_aaa111"))
    c2 = chuan_hoa_lich(_raw("Lăng Minh Mạng", "lich_bbb222"))
    ics1 = dung_ics(c1)["ics"]
    ics2 = dung_ics(c2)["ics"]
    uid1 = next(l for l in ics1.splitlines() if l.startswith("UID:"))
    uid2 = next(l for l in ics2.splitlines() if l.startswith("UID:"))
    assert uid1 != uid2 and "lich_aaa111" in uid1 and "lich_bbb222" in uid2

    # Cùng nội dung nhưng khác lich_id -> itinerary_hash cho cache PPTX giữ nguyên theo nội dung
    c_same = chuan_hoa_lich(_raw("Đại Nội Huế", "lich_zzz999"))
    assert c_same["itinerary_hash"] == c1["itinerary_hash"]

    # Giữ lich_id qua luu_sau_luot & lich_tu_luu
    s_cfg, bang_v2, _ = _bang_v2_va_lt()
    flags = AssistantFlags.from_settings(s_cfg)
    khung = lt2.xep_v2(bang_v2, lt2.tu_truong({"so_ngay": "2", "nguoi_lon": 2}), ngay_bat_dau=dt.date(2026, 12, 10))
    tr_v2 = AnswerTrace(lich_v2={"lich": {**lt2.dung_lich(bang_v2, khung, {}), "lich_id": "lich_giu_01"}, "cau": {}, "loi_khung": [], "khung": khung, "ngay_di": "2026-12-10", "mua": {}, "lich_id": "lich_giu_01"})
    luu = lkh.luu_sau_luot(tr_v2, flags)
    assert luu["lich_id"] == "lich_giu_01"
    lich_ra, _ = lich_tu_luu(luu, flags)
    assert lich_ra["lich_id"] == "lich_giu_01"

    if NODE is not None:
        js_code = (
            "import { dungIcsV2 } from './frontend/src/lich_ics.js';"
            f"const a = dungIcsV2({json.dumps(_raw('Đại Nội Huế', 'js_111'))}, {{}})?.ics || '';"
            f"const b = dungIcsV2({json.dumps(_raw('Lăng Minh Mạng', 'js_222'))}, {{}})?.ics || '';"
            "const ua = a.split('\\r\\n').find(l => l.startsWith('UID:'));"
            "const ub = b.split('\\r\\n').find(l => l.startsWith('UID:'));"
            "console.log(JSON.stringify({ ua, ub }));"
        )
        res = subprocess.run([NODE, "--input-type=module", "-e", js_code], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        out = json.loads(res.stdout.strip())
        assert out["ua"] != out["ub"] and "js_111" in out["ua"] and "js_222" in out["ub"]


# ---------- P12: xin_cong_cu_da_an không phân nhầm Invalid JSON input của tool đang mở ----------

def test_p12_xin_cong_cu_da_an_khong_phan_nham_loi_json():
    gen = OpenAIFullCorpusGenerator(model="gpt-6-luna", client=SimpleNamespace())

    def search(cau_tim: str) -> str:
        return "ok"

    remaining = False
    agent, _, state = gen._assistant_for(
        search,
        con_luot_fn=lambda: remaining,
        canh_bao_vong=(SimpleNamespace(calls=[]), 6),
        canh_bao_vong_con_lai=True,
    )
    tool = next(t for t in agent.tools if t.name == "tim_kho")
    with pytest.raises(ModelBehaviorError) as exc_info:
        asyncio.run(tool.on_invoke_tool(ToolContext(context=None, tool_name=tool.name, tool_call_id="local", tool_arguments="{"), "{"))
    assert "Invalid JSON" in str(exc_info.value)
    assert gen.xin_cong_cu_da_an(exc_info.value, state) is False
    # Đúng lỗi tool bị tắt/ẩn mới trả True
    assert gen.xin_cong_cu_da_an(ModelBehaviorError("Tool tim_kho not found"), {"con_luot_fn": lambda: False, "an_cong_cu": True}) is True


# ---------- P13 + P14: cache AI & contract POST/GET PPTX + X-Slide-Source ----------

def test_p13_p14_cache_ai_tach_get_post_va_use_llm_false():
    s = copy.deepcopy(load_settings(validate_private_paths=False))
    s["assistant"]["slide_designer"] = True
    s["slide_designer_cfg"]["use_llm"] = False
    flags_no_llm = AssistantFlags.from_settings(s)

    app = FastAPI()
    app.include_router(xuat_router)
    app.add_middleware(ChanLuot, gioi_han=GioiHanLuot(tran=4))
    store = ConversationStore(len)
    app.state.conversations = store
    app.state.assistant_flags = flags_no_llm
    cid = store.ensure(None)
    khung = lt2.xep_v2(flags_no_llm.bang_lich_v2, lt2.tu_truong({"so_ngay": "2", "nguoi_lon": 2, "ngan_sach": "vua"}), ngay_bat_dau=dt.date(2026, 12, 10))
    luu = {**sl.luu_tu_lich(khung, "2026-12-10", None), "an_toan": tt.CAU_BAO_LU}
    store.luu_lich(cid, luu)
    client = TestClient(app)

    # P13: POST khi use_llm=False trả lỗi hợp đồng 409, KHÔNG trừ quota AI trọng số 3, và GET vẫn dùng code bình thường
    r_post1 = client.post("/api/lich/pptx", cookies={"conversation_id": cid})
    r_post2 = client.post("/api/lich/pptx", cookies={"conversation_id": cid})
    assert r_post1.status_code == 409 and r_post2.status_code == 409
    r_get = client.get("/api/lich/pptx", cookies={"conversation_id": cid})
    assert r_get.status_code == 200 and r_get.headers.get("X-Slide-Source") == "code"

    # P14: có cache AI trong store -> GET /api/lich/pptx KHÔNG đọc cache AI, POST đọc cache AI và trả X-Slide-Source: cache_ai
    s_ai = copy.deepcopy(s)
    s_ai["slide_designer_cfg"]["use_llm"] = True
    app.state.assistant_flags = AssistantFlags.from_settings(s_ai)
    from api.lich_pptx import trang_lich_v2
    lich_c, cau_c = lich_tu_luu(luu, flags_no_llm)
    canonical = chuan_hoa_lich(lich_c, cau_c, an_toan=luu["an_toan"], thu_muc_anh=THU_MUC_ANH)
    fake_ai_deck = trang_lich_v2(canonical, theme_id="di_san_tram", ngay_tao="28/11/2026")
    fake_ai_deck["slides"][0]["tieu_de"] = "BÌA CACHE AI ĐẶC BIỆT"
    store.luu_slide_cache(cid, canonical["itinerary_hash"], "di_san_tram", fake_ai_deck)

    r_fast = client.get("/api/lich/pptx?theme=di_san_tram", cookies={"conversation_id": cid})
    assert r_fast.status_code == 200 and r_fast.headers.get("X-Slide-Source") == "code"
    import pptx, io
    prs_fast = pptx.Presentation(io.BytesIO(r_fast.content))
    txt_fast = "\n".join(p.text for sh in prs_fast.slides[0].shapes if sh.has_text_frame for p in sh.text_frame.paragraphs)
    assert "BÌA CACHE AI ĐẶC BIỆT" not in txt_fast

    r_ai_cached = client.post("/api/lich/pptx", json={"theme_id": "di_san_tram"}, cookies={"conversation_id": cid})
    assert r_ai_cached.status_code == 200 and r_ai_cached.headers.get("X-Slide-Source") == "cache_ai"
    prs_ai = pptx.Presentation(io.BytesIO(r_ai_cached.content))
    txt_ai = "\n".join(p.text for sh in prs_ai.slides[0].shapes if sh.has_text_frame for p in sh.text_frame.paragraphs)
    assert "BÌA CACHE AI ĐẶC BIỆT" in txt_ai


# ---------- P17: kiem_dan_y trả cờ dung_du_phong đồng nhất log / SSE / cache ----------

def test_p17_ho_so_fallback_dan_y_rong_dong_nhat_co_va_khong_cache():
    chia, dung_du_phong = hs.kiem_dan_y_co_co([], 10)
    assert chia == hs.chia_muc_du_phong(10) and dung_du_phong is True
    chia_ok, dung_du_phong_ok = hs.kiem_dan_y_co_co([{"tieu_de": "M1", "bai": [1, 2]}], 2)
    assert dung_du_phong_ok is False and len(chia_ok) == 1

    from test_ho_so_chu_de import LANG, ML, _Kho
    dem = {}
    class MayDanYRong:
        async def viet_so_tay(self, loai, prompt, log):
            return {"muc": []} if loai == "ho_so_dan_y" else {"y": []}

    async def gom():
        return [
            e async for e in ho_so_su_kien(
                hs.CHU_DE[0], LANG, SimpleNamespace(retrieval_service=_Kho()), SimpleNamespace(the_noi_bang=None, muc_luc=ML), MayDanYRong(), dem
            )
        ]

    sk = [(k.split("event: ", 1)[1].split("\n", 1)[0], json.loads(k.split("data: ", 1)[1])) for k in (e.decode() for e in asyncio.run(gom()))]
    xong = next(d for t, d in sk if t == "xong")
    assert xong["dan_y_do_code"] is True
    assert dem == {}


# ---------- P6, P7, P15 ----------

def test_p6_p15_frontend_xu_ly_429_va_reset_da_tim():
    hoi_anh = (REPO_ROOT / "frontend/src/HoiBangAnh.jsx").read_text(encoding="utf-8")
    assert "r.status === 429" in hoi_anh and "du?.loi" in hoi_anh

    chat_jsx = (REPO_ROOT / "frontend/src/chat.jsx").read_text(encoding="utf-8")
    assert "daTim: []" in chat_jsx and "buoc.length = 0" in chat_jsx


def test_p7_sse_ghep_duoi_bao_toan_newline_bang_markdown():
    prefix = "| Địa điểm | Giờ |\n"
    final = prefix + "|---|---|\n| Đại Nội | Theo mùa [1] |"
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    events = parse_sse([stream.delta(prefix), *stream.finish(AnswerTrace(answer=final, cited=()))])
    shown = "".join(d["text"] for k, d in events if k == "delta")
    assert shown == final
    assert "\n\n|---|---|\n" not in shown
    assert metrics["delta_matches_final"] is True
