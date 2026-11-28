"""Unit & contract tests Đợt 6 (Toàn diện Local 100%, 0 USD, không cần `.env`)."""
from __future__ import annotations

import asyncio
import copy
import datetime as dt
import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from PIL import Image

from api.app import REPO_ROOT
from api.routes.anh import router as anh_router
from api.routes.cong import router as cong_router
from core.settings_loader import BACKEND_DIR, load_settings
from evaluation.trajectory_eval import MODEL_TOOL_NAMES, la_goi_cong_cu_model
from llm import goi_y_luu_tru as gylt
from llm import lich_trinh_v2 as lt2
from llm import luu_tru_lich as ltl
from llm import ngay_lich as nl
from llm import nhan_anh as na
from llm import thoi_tiet as tt
from llm import tinh_ve as tv
from llm.assistant import (
    AnswerTrace,
    AssistantFlags,
    MAY_HAVE_CHANGED_NOTICE,
    _lich_extra,
    answer_turn_stream,
    check_citations,
    goi_y_luu_tru_for_turn,
    set_notice,
    tinh_ve_for_turn,
)
from llm.generator_openai_full_corpus import CallLog, max_turns_for


def _jpeg_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (64, 64), (120, 90, 60)).save(buf, format="JPEG")
    return buf.getvalue()


# ---------- 6.3a: `tinh_ve` & `tinh_ve_va_gio_tham_quan` ----------

def test_tinh_ve_12_quan_the_single_vs_optimal_combo_and_530k_warning():
    assert len(tv.QUAN_THE_DIEM) == 12
    assert sum(v["nguoi_lon"] for v in tv.QUAN_THE_DIEM.values()) == 1_200_000
    assert sum(v["tre_7_12"] for v in tv.QUAN_THE_DIEM.values()) == 130_000

    # Tuyến 2 điểm Minh Mạng - Gia Long (300k -> 240k)
    opt2, goi2 = tv.toi_uu_quan_the(["lang_minh_mang", "lang_gia_long"], tre_em=False)
    assert opt2 == 240_000 and len(goi2) == 1

    # Tuyến 4 điểm 530k phải có cảnh báo không phải 12 điểm
    txt4, src4 = tv.ket_qua(["dai_noi", "lang_minh_mang", "lang_tu_duc", "lang_khai_dinh"], so_nguoi_lon=1)
    assert "530.000đ" in txt4 and "KHÔNG phải vé toàn bộ 12 điểm" in txt4 and src4 == (tv.NGUON_QUAN_THE,)

    # 5 điểm trọng điểm (4 điểm + Gia Long): tuyến 12 điểm 600k rẻ hơn 530k + 150k = 680k
    opt5, _ = tv.toi_uu_quan_the(["dai_noi", "lang_minh_mang", "lang_tu_duc", "lang_khai_dinh", "lang_gia_long"], tre_em=False)
    assert opt5 == 600_000

    # Cổ vật + An Định + Đại Nội = 80k + 200k = 280k (rẻ hơn 300k)
    opt3, _ = tv.toi_uu_quan_the(["dai_noi", "bao_tang_co_vat", "cung_an_dinh"], tre_em=False)
    assert opt3 == 280_000


def test_tinh_ve_hai_van_quan_separate_elderly_verbatim_and_holidays():
    # Hải Vân Quan tách riêng, trẻ 7-12t miễn phí (<13t), không gộp vào Quần thể
    txt, src = tv.ket_qua(["dai_noi", "hai_van_quan"], so_nguoi_lon=2, so_tre_7_12=1)
    assert "Tách biệt hoàn toàn" in txt or "tách riêng" in txt
    assert "440.000đ" in txt  # 2 * 200k + 1 * 40k Đại Nội
    assert "140.000đ" in txt  # 2 * 70k Hải Vân Quan (trẻ 7-12t miễn phí)
    assert "580.000đ" in txt
    assert src == (tv.NGUON_QUAN_THE, tv.NGUON_HAI_VAN)

    # Người cao tuổi VN >=60t giảm 50% + điều kiện nguyên văn; khách quốc tế >=60t không giảm
    txt_vn, _ = tv.ket_qua(["dai_noi"], so_nguoi_lon=0, so_nguoi_cao_tuoi_vn=2, la_cong_dan_vn=True)
    assert "200.000đ" in txt_vn and tv.DIEU_KIEN_CAO_TUOI_VN in txt_vn
    txt_foreign, _ = tv.ket_qua(["dai_noi"], so_nguoi_lon=0, so_nguoi_cao_tuoi_vn=2, la_cong_dan_vn=False)
    assert "400.000đ" in txt_foreign and "chỉ áp dụng" in txt_foreign

    # 5 ngày lễ miễn phí công dân VN (kể cả mùng 1 Tết âm qua ngay_lich)
    # 2026-02-17 là mùng 1 Tết Bính Ngọ
    am_tet = nl.solar_to_lunar(dt.date(2026, 2, 17))
    assert (am_tet.day, am_tet.month, am_tet.leap) == (1, 1, False)
    for holiday in ("2026-02-17", "2026-03-26", "2026-08-19", "2026-09-02", "2026-11-23"):
        t_le, _ = tv.ket_qua(["dai_noi", "hai_van_quan"], ngay=holiday, so_nguoi_lon=2, la_cong_dan_vn=True)
        assert "NGÀY LỄ MIỄN PHÍ CHO CÔNG DÂN VIỆT NAM" in t_le and "Tổng vé ước tính các mục xác định được giá: 0đ" in t_le

    # 29/3 chỉ miễn Hải Vân Quan, không miễn Quần thể
    t_293, _ = tv.ket_qua(["dai_noi", "hai_van_quan"], ngay="2026-03-29", so_nguoi_lon=1, la_cong_dan_vn=True)
    assert "200.000đ" in t_293 and "miễn phí ngày lễ" in t_293


def test_tinh_ve_hours_closed_monday_and_tool_dedup():
    settings = load_settings(validate_private_paths=False)
    bang_v2 = lt2.nap_bang_v2(BACKEND_DIR / settings["assistant"]["lich_trinh_bang_v2"])

    # Lê Bá Đảng đóng cửa Thứ Hai (2026-11-30 là Thứ Hai)
    t_mon, _ = tv.ket_qua(["kg_le_ba_dang"], ngay="2026-11-30", bang_v2=bang_v2)
    assert "ĐÓNG CỬA vào Thứ Hai" in t_mon

    # Bắt đầu 16:00 không kịp đi hết Đại Nội (150p) + Khải Định trước 17:00
    t_late, _ = tv.ket_qua(["dai_noi", "lang_khai_dinh"], gio_bat_dau="16:00", bang_v2=bang_v2)
    assert "KHÔNG KỊP THỜI LƯỢNG" in t_late

    # Duyệt Thị Đường nhắc vé Đại Nội
    t_dtd, src_dtd = tv.ket_qua(["duyet_thi_duong"], gio_bat_dau="15:30", bang_v2=bang_v2)
    assert "200.000đ" in t_dtd and "qua 2 suất cố định" in t_dtd and tv.NGUON_NGHE_THUAT in src_dtd

    # Tool turn wrapper + chong_lap + MAY_HAVE_CHANGED_NOTICE
    trace = AnswerTrace()
    fn = tinh_ve_for_turn(trace, bang_v2, chong_lap=True)
    res1 = asyncio.run(fn(["dai_noi"], ngay="2026-09-02", so_nguoi_lon=2))
    res2 = asyncio.run(fn(["dai_noi"], ngay="2026-09-02", so_nguoi_lon=2))
    assert "[Nguồn 1]" in res1 and "không gọi lặp lại nữa" in res2.lower()
    assert trace.tools[-1]["lap"] is True
    trace.answer = "Bạn được miễn phí [1]."
    check_citations(trace)
    set_notice(trace, AssistantFlags(tim_them=True, tinh_ve_tham_quan=True, may_have_changed_notice=True))
    assert MAY_HAVE_CHANGED_NOTICE in (trace.notice or "")


# ---------- 6.3b: `goi_y_luu_tru` ----------

def test_goi_y_luu_tru_filters_ota_allowlist_and_hard_nhan():
    settings = load_settings(validate_private_paths=False)
    bang_v2 = lt2.nap_bang_v2(BACKEND_DIR / settings["assistant"]["lich_trinh_bang_v2"])
    bang_lt = ltl.nap_bang_luu_tru(BACKEND_DIR / settings["assistant"]["lich_trinh_bang_luu_tru"], bang_v2.cum)

    for khu, expected_khu, expected_phia in (
        ("trung_tam", ltl.KHU_LOI, None),
        ("phia_tay", ltl.KHU_TAY, None),
        ("ven_bien_bac", ltl.KHU_BIEN, "bac"),
        ("ven_bien_nam", ltl.KHU_BIEN, "nam"),
    ):
        txt, n = gylt.ket_qua(bang_lt, bang_v2, khu=khu, hang_sao="cao", ngay_nhan="2026-12-10", ngay_tra="2026-12-12", so_khach=2)
        assert 1 <= n <= 5
        assert ltl.NHAN in txt
        # Kiểm host OTA hợp lệ & không bịa giá / email
        import re
        urls = re.findall(r"https://[^\s)]+", txt)
        assert urls and all(urlparse(u).hostname in ltl.ALLOWED_OTA_HOSTS for u in urls)
        assert "@" not in txt and "đ/đêm" not in txt and "VND" not in txt
        chon, _ = gylt._loc_co_so(bang_lt, bang_v2, khu=khu, hang_sao="cao")
        assert all(c["khu"] == expected_khu and (expected_phia is None or c["phia_bien"] == expected_phia) for c in chon)

    # Hard invariant trong set_notice dù câu trả lời model quên chép NHAN
    trace = AnswerTrace()
    fn = goi_y_luu_tru_for_turn(trace, bang_lt, bang_v2, chong_lap=True)
    out1 = asyncio.run(fn(khu="ven_bien_bac", gan_diem="bien_thuan_an", hang_sao="tat_ca", so_khach=2))
    out2 = asyncio.run(fn(khu="ven_bien_bac", gan_diem="bien_thuan_an", hang_sao="tat_ca", so_khach=2))
    assert ltl.NHAN in out1 and trace.tools[-1]["lap"] is True
    trace.answer = "Gợi ý khách sạn gần biển Thuận An [1]."
    check_citations(trace)
    set_notice(trace, AssistantFlags(tim_them=True, goi_y_luu_tru=True, luu_tru_bang=bang_lt, bang_lich_v2=bang_v2))
    assert ltl.NHAN in (trace.notice or "")

    # Vòng 2 (6.3b): (1) Chặn ở sàn cứng bão/lũ trong _lich_extra + trong goi_y_luu_tru_for_turn
    storm_q = "Huế đang có tin bão lụt ngập đường, tìm khách sạn ven biển Thuận An tối nay ở cho an toàn."
    flags_lt = AssistantFlags(tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, cong_cong_cu="linh_hoat",
                              du_bao=lambda: None, goi_y_luu_tru=True, luu_tru_bang=bang_lt, bang_lich_v2=bang_v2)
    extra_storm = _lich_extra(storm_q, None, None, AnswerTrace(), None, None, flags_lt)
    assert "goi_y_luu_tru_fn" not in extra_storm
    trace_storm = AnswerTrace()
    fn_storm = goi_y_luu_tru_for_turn(trace_storm, bang_lt, bang_v2, query=storm_q)
    out_storm = asyncio.run(fn_storm(khu="ven_bien_bac"))
    assert "không dùng gợi ý lưu trú" in out_storm.lower() and trace_storm.goi_y_luu_tru is None

    # (2) Ánh xạ Lăng Cô / Đầm Lập An / Bạch Mã về ven_bien_nam dù model gửi bat_ky hay nhầm ven_bien_bac
    for khu_in in ("bat_ky", "ven_bien_bac"):
        chon_lc, mo_ta_lc = gylt._loc_co_so(bang_lt, bang_v2, khu=khu_in, gan_diem="dam_lap_an")
        assert chon_lc and all(c["khu"] == ltl.KHU_BIEN and c["phia_bien"] == "nam" for c in chon_lc)
        assert "bờ Nam" in mo_ta_lc

    # (3) Đặc tả mo_ta_ngan & mo_ta_cong_cu đủ phân biệt Lăng Cô vs Thuận An, có Tool Use Example & trigger rõ ràng
    for desc in (gylt.mo_ta_ngan(bang_v2), gylt.mo_ta_cong_cu(bang_v2)):
        assert "Lăng Cô" in desc and "ven_bien_nam" in desc and "Thuận An" in desc and "ven_bien_bac" in desc
        assert "Ví dụ:" in desc and "HÃY GỌI công cụ này" in desc


# ---------- 6.4a, 6.4b & cờ mặc định TẮT ----------

def test_default_off_flags_and_tinh_nang_slide_designer_ai():
    s = load_settings(validate_private_paths=False)
    assert s["assistant"]["tinh_ve_tham_quan"] is False
    assert s["assistant"]["goi_y_luu_tru"] is False
    assert s["anh"]["che_do_tu_choi"] == "mac_dinh"
    assert max_turns_for(None) == max_turns_for(None, tinh_ve_fn=None, goi_y_luu_tru_fn=None)

    # Kiểm /api/tinh_nang: slide_designer_ai chỉ True khi cả slide_designer và use_llm đều True
    s_on = copy.deepcopy(s)
    s_on["assistant"]["slide_designer"] = True
    s_on["slide_designer_cfg"]["use_llm"] = True
    app_on = FastAPI()
    app_on.include_router(cong_router)
    app_on.state.assistant_flags = AssistantFlags.from_settings(s_on)
    r_on = TestClient(app_on).get("/api/tinh_nang").json()
    assert r_on["slide_designer"] is True and r_on["slide_designer_ai"] is True

    s_no_llm = copy.deepcopy(s_on)
    s_no_llm["slide_designer_cfg"]["use_llm"] = False
    app_no_llm = FastAPI()
    app_no_llm.include_router(cong_router)
    app_no_llm.state.assistant_flags = AssistantFlags.from_settings(s_no_llm)
    r_no_llm = TestClient(app_no_llm).get("/api/tinh_nang").json()
    assert r_no_llm["slide_designer"] is True and "slide_designer_ai" not in r_no_llm

    # Kiểm UI 6.4a & 6.4b tĩnh (0 chữ ghi công ảnh)
    chat_jsx = (REPO_ROOT / "frontend" / "src" / "chat.jsx").read_text(encoding="utf-8")
    for stage in ("khoang_cach", "gan_diem", "so_sanh_diem_den", "goi_y_mua_nang", "tinh_ve", "goi_y_luu_tru", "ngay_lich", "liet_ke_bai"):
        assert f"{stage}:" in chat_jsx
    lich_jsx = (REPO_ROOT / "frontend" / "src" / "LichV2.jsx").read_text(encoding="utf-8")
    assert "Tải PowerPoint nhanh" in lich_jsx and "Tải PowerPoint AI (~15–20s)" in lich_jsx
    assert "/api/lich/pptx?theme=" in lich_jsx
    for bad in ("CC BY", "Wikimedia", "tac_gia", "giay_phep"):
        assert bad not in lich_jsx


def test_stream_status_stages_for_all_new_and_existing_tools():
    tool_to_stage = [
        ("khoang_cach", "khoang_cach"),
        ("gan_diem", "gan_diem"),
        ("so_sanh_diem_den", "so_sanh_diem_den"),
        ("goi_y_phuong_an_mua_nang", "goi_y_mua_nang"),
        ("tinh_ve_va_gio_tham_quan", "tinh_ve"),
        ("goi_y_luu_tru", "goi_y_luu_tru"),
        ("ngay_lich", "ngay_lich"),
        ("liet_ke_bai", "liet_ke_bai"),
    ]

    class FakeStream:
        def __init__(self, tool_name: str):
            self._tool = tool_name

        def cancel(self):
            pass

        def stream_events(self):
            async def gen():
                yield SimpleNamespace(
                    type="run_item_stream_event",
                    name="tool_called",
                    item=SimpleNamespace(raw_item=SimpleNamespace(name=self._tool)),
                )
                yield SimpleNamespace(type="run_item_stream_event", name="tool_output", item=None)
                yield SimpleNamespace(
                    type="raw_response_event",
                    data=SimpleNamespace(type="response.output_text.delta", delta="Trả lời [1]."),
                )
            return gen()

    class FakeGen:
        timeout = 10.0

        def __init__(self, tool_name: str):
            self._tool = tool_name
            self.assistant_instructions = "inst"

        def start_tools_stream(self, *args, **kwargs):
            return FakeStream(self._tool), CallLog(), {"hit_max_turns": False}

        def finish_answer_stream(self, result, call_log, started, state):
            return SimpleNamespace(text="Trả lời [1].", input_tokens=10, output_tokens=5, cached_tokens=0, reasoning_tokens=0, usd=0.0, calls=[], hit_max_turns=False, clarify=None)

    from core.schema import RetrievedDocument
    from retrieval.full_corpus_context import PackedContext, PackedSource

    class FakeRet:
        def search(self, q):
            return SimpleNamespace(
                documents=[RetrievedDocument(id="c1", text="ok", score=0.9, metadata={"source": "a.md", "title": "Nguon"})],
                trace=SimpleNamespace(timings_ms={"dense_ms": 1.0}),
            )

    class FakeCtx:
        def build(self, cau_hoi, docs, **kwargs):
            src = PackedSource(id=1, title="Nguon", heading_path=(), excerpts=("ok",), source="a.md")
            return PackedContext(text="[Nguồn 1] Nguon: ok", sources=(src,), input_tokens=10, document_ids=("c1",))

    flags = AssistantFlags(tim_them=True)
    for tool_name, expected_stage in tool_to_stage:
        trace = AnswerTrace()
        async def run_one():
            return [ev async for ev in answer_turn_stream("hỏi thử", FakeRet(), FakeCtx(), FakeGen(tool_name), trace, flags, None, "u")]
        events = asyncio.run(run_one())
        statuses = [data for kind, data in events if kind == "status"]
        assert {"stage": expected_stage} in statuses
        assert not any(s.get("stage") == "searching" for s in statuses)


# ---------- 6.1: `doi_chieu_mau` 0 GPU ----------

def test_doi_chieu_mau_55_paths_and_two_step_metrics_and_reject():
    thu_muc_anh = REPO_ROOT / "frontend" / "public" / "anh"
    assert len(na.ANH_MAU_55) == 55
    for mid, (rel, loai) in na.ANH_MAU_55.items():
        assert loai in ("diem", "di_san", "mon")
        assert (thu_muc_anh / rel).is_file(), f"Thiếu ảnh mẫu {mid}: {rel}"

    danh_sach = [
        {"id": "chua_thien_mu", "ten": "Chùa Thiên Mụ"},
        {"id": "dai_noi", "ten": "Đại Nội Huế"},
        {"id": "bun_bo_hue", "ten": "Bún bò Huế"},
    ]

    class FakeGen:
        responses_model = "fake"

        def __init__(self, step1_out, step2_out, timeout_on_2: bool = False):
            self.step1_out = step1_out
            self.step2_out = step2_out
            self.timeout_on_2 = timeout_on_2
            self.seen_inputs = []

        async def _run(self, agent, items, call_log, timeout):
            self.seen_inputs.append(items)
            n = len(self.seen_inputs)
            if n == 2 and self.timeout_on_2:
                raise TimeoutError("timeout")
            call_log.calls.append({"input_tokens": 100 * n, "cached_tokens": 20 * n, "output_tokens": 10 * n, "reasoning_tokens": 0, "usd": 0.001 * n})
            return SimpleNamespace(final_output=self.step1_out if n == 1 else self.step2_out)

    app = FastAPI()
    app.include_router(anh_router)
    app.state.anh_limiter = None

    def post_img(gen_obj):
        app.state.generator = gen_obj
        app.state.anh = {
            "danh_sach": danh_sach,
            "agent": na.tao_agent(gen_obj, danh_sach, che_do_tu_choi="doi_chieu_mau"),
            "doi_chieu_agent": na.tao_agent_doi_chieu(gen_obj, danh_sach),
            "thu_muc_anh": thu_muc_anh,
            "che_do_tu_choi": "doi_chieu_mau",
            "max_bytes": 5_242_880,
            "max_pixels": 25_000_000,
            "canh_dai": 1024,
            "timeout": 20,
        }
        return TestClient(app).post("/api/anh/ung_vien", content=_jpeg_bytes(), headers={"Content-Type": "image/jpeg"})

    # 1. Khớp & đôn ứng viên #2 cùng nhóm "diem"
    g_promote = FakeGen(
        SimpleNamespace(ung_vien=["chua_thien_mu", "dai_noi"], khong_nhan_ra=False),
        SimpleNamespace(khop=True, id_chon="dai_noi", ly_do_ngan="Khớp Ngọ Môn"),
    )
    r_ok = post_img(g_promote)
    assert r_ok.status_code == 200
    assert [u["id"] for u in r_ok.json()["ung_vien"]] == ["dai_noi", "chua_thien_mu"]
    assert r_ok.json()["khong_nhan_ra"] is False
    # Bước 2 gửi ảnh khách + 2 ảnh mẫu cùng nhóm
    imgs2 = [c for c in g_promote.seen_inputs[1][0]["content"] if c["type"] == "input_image"]
    assert len(imgs2) == 3 and imgs2[1]["detail"] == "low" and imgs2[2]["detail"] == "low"

    # 2. Khác nhóm ("mon" vs "diem") ⇒ Bước 2 chỉ gửi 1 ảnh mẫu để tiết kiệm token
    g_diff = FakeGen(
        SimpleNamespace(ung_vien=["bun_bo_hue", "dai_noi"], khong_nhan_ra=False),
        SimpleNamespace(khop=True, id_chon="bun_bo_hue", ly_do_ngan="Đúng tô bún"),
    )
    assert post_img(g_diff).json()["ung_vien"][0]["id"] == "bun_bo_hue"
    imgs_diff = [c for c in g_diff.seen_inputs[1][0]["content"] if c["type"] == "input_image"]
    assert len(imgs_diff) == 2

    # 3. Từ chối (khác kiến trúc hoặc bẫy chữ dán) ⇒ trả rỗng, metrics cộng đủ 2 lần gọi
    logs = []
    from api.routes import anh as route_anh
    orig_info = route_anh.logger.info
    route_anh.logger.info = lambda msg, *args: logs.append(json.loads(args[0])) if args and str(msg).startswith("anh_metrics") else None
    try:
        g_rej = FakeGen(
            SimpleNamespace(ung_vien=["chua_thien_mu"], khong_nhan_ra=False),
            SimpleNamespace(khop=False, id_chon=None, ly_do_ngan="Chữ dán giả, kiến trúc khác hẳn"),
        )
        r_rej = post_img(g_rej)
        assert r_rej.json() == {"ung_vien": [], "khong_nhan_ra": True}
        m = logs[-1]
        assert m["outcome"] == "khong_nhan_ra" and m["n_llm_calls"] == 2
        assert m["input_tokens"] == 300 and m["cached_tokens"] == 60 and m["output_tokens"] == 30 and m["usd"] == 0.003
    finally:
        route_anh.logger.info = orig_info

    # 4. Timeout ở Bước 2 ⇒ trả `khong_doan_duoc` sạch sẽ
    g_to = FakeGen(SimpleNamespace(ung_vien=["chua_thien_mu"], khong_nhan_ra=False), None, timeout_on_2=True)
    r_to = post_img(g_to)
    assert r_to.status_code == 200 and r_to.json() == {"ung_vien": [], "khong_nhan_ra": True, "loi": "khong_doan_duoc"}


# ---------- 6.2b: Vá `vl_01` & Rào hai chiều ----------

def test_vl01_non_weather_guard_and_two_sided_boundaries():
    vl_query = "Kể hết các món bánh đặc sản Huế và cho biết phí gửi xe ô tô qua đêm ở Bảo tàng Cổ vật Cung đình Huế."
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem(vl_query, ()) is False
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Mai đi biển Thuận An thời tiết có nguy hiểm gì không?", ()) is True
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Mai đi Huế có an toàn không, trời có nguy hiểm gì không?", ()) is True

    called = {"du_bao": 0}
    async def fake_du_bao():
        called["du_bao"] += 1
        return tt.DuBao(trang_thai="loi", loi="should_not_run")

    flags = AssistantFlags(tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, cong_cong_cu="linh_hoat", du_bao=fake_du_bao)
    trace = AnswerTrace()
    extra = _lich_extra(vl_query, None, None, trace, None, None, flags)
    out = asyncio.run(extra["thoi_tiet_fn"]("bao_lu", 0, 1))
    assert "không liên quan đến thời tiết" in out.lower()
    assert called["du_bao"] == 0
    assert trace.thoi_tiet is None
    assert trace.thoi_tiet_ctx["bao_lu"] is False and trace.thoi_tiet_ctx["bao_lu_model"] is False

    # Rào hai chiều: module mới không import SDK mạng & trajectory_eval nhận diện 2 tool mới
    for mod in (tv, gylt):
        src = Path(mod.__file__).read_text(encoding="utf-8")
        for forbidden in ("import openai", "from openai", "import agents", "from agents", "import httpx"):
            assert forbidden not in src
    assert {"tinh_ve_va_gio_tham_quan", "goi_y_luu_tru"} <= MODEL_TOOL_NAMES
    assert la_goi_cong_cu_model({"name": "tinh_ve_va_gio_tham_quan"})
    assert la_goi_cong_cu_model({"name": "goi_y_luu_tru"})
