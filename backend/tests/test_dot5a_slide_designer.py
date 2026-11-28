"""Kiểm thử Đợt 5 Phần A — Slide Designer Agent + `.pptx` v2 (3 theme, 9 layout, `pptx_fit`, Pillow center-crop, cache, rate-limit, cờ tắt)."""
import asyncio
import copy
import io
import zipfile
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from PIL import Image

from api.conversations import ConversationStore
from api.gioi_han import LOI_BAO, ChanLuot, GioiHanLuot
from api.hanh_trinh_chuan import chuan_hoa_lich, tu_luu_chuan
from api.lich_pptx import dung_pptx_v2, plan_sang_cac_trang, trang_lich_v2
from api.pptx_catalog import ALL_LAYOUTS, THEMES
from api.pptx_fit import cat_sach_ranh_gioi, co_chu_vua_khung, kiem_tra_tran_chu
from api.routes.xuat import THU_MUC_ANH, router as xuat_router
from core.settings_loader import load_settings
from llm import lich_trinh_v2 as lt2
from llm import sua_lich_v2 as sl
from llm import thoi_tiet as tt
from llm.assistant import AssistantFlags
from llm.slide_designer import DayItemSlot, OverviewDayItem, SlideDayPlan, SlideDeckPlan, hau_kiem_slide_deck, thiet_ke_slide


def _lich_day_du(so_ngay: int = 3) -> dict:
    s = load_settings(validate_private_paths=False)
    flags = AssistantFlags.from_settings(s)
    khung = lt2.xep_v2(
        flags.bang_lich_v2,
        lt2.tu_truong({"so_ngay": str(so_ngay), "nguoi_lon": 2, "tre_em": 1, "kieu_di": "can_bang", "ngan_sach": "vua"}),
        ngay_bat_dau=lt2.dt.date(2026, 12, 10),
    )
    lich = lt2.dung_lich(
        flags.bang_lich_v2, khung, {}, "2026-12-10", (),
        flags.toa_do_lich if flags.ban_do_lich else None,
        flags.anh_lich_bang if flags.anh_lich else None,
    )
    from llm.len_ke_hoach import gan_o_an
    gan_o_an(lich, flags.bang_lich_v2, khung, flags)
    cau = {m["id_muc"]: f"Điểm {m['ten']} mang nét văn hoá Huế đặc sắc [1]." for m in lt2.moi_muc(lich)}
    return chuan_hoa_lich(lich, cau, an_toan=tt.CAU_BAO_LU, thu_muc_anh=THU_MUC_ANH)


def _kiem_tra_meo_anh_pptx(pptx_bytes: bytes) -> None:
    """Đọc XML `<p:pic>` và ảnh nhúng trong tệp `.pptx`, xác nhận 0% ảnh méo tỷ lệ > 5%."""
    pptx = pytest.importorskip("pptx")
    prs = pptx.Presentation(io.BytesIO(pptx_bytes))
    assert len(prs.slides) >= 3
    with zipfile.ZipFile(io.BytesIO(pptx_bytes)) as zf:
        for idx, slide in enumerate(prs.slides, start=1):
            for sh in slide.shapes:
                if sh.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                    w_h_box = sh.width / sh.height
                    with Image.open(io.BytesIO(sh.image.blob)) as im:
                        w_h_img = im.size[0] / im.size[1]
                    diff = abs(w_h_box - w_h_img) / w_h_img
                    assert diff <= 0.05, f"Slide {idx} ảnh méo {diff:.2%}: box={w_h_box:.3f}, img={w_h_img:.3f}"


def test_settings_switches_default_false_and_isolated_cfg():
    s = load_settings(validate_private_paths=False)
    assert s["assistant"]["xuat_nang_cao"] is True
    assert s["assistant"]["slide_designer"] is True
    assert s["slide_designer_cfg"] == {
        "model": "gpt-6-luna",
        "use_llm": True,
        "max_retries": 1,
        "timeout_seconds": 20,
        "fallback_code_only": True,
        "reasoning_effort": "none",
    }
    assert "slide_designer_cfg" not in s["full_corpus_generation"]


def test_pptx_v2_renders_all_3_themes_and_9_layouts_without_distortion_or_attribution():
    pptx = pytest.importorskip("pptx")
    canonical = _lich_day_du(3)
    # Bảo đảm mọi layout đều được dựng và render sạch, 0 méo ảnh, 0 ghi công ảnh, giữ an_toan + disclaimer
    for theme_id in THEMES:
        deck = trang_lich_v2(canonical, theme_id=theme_id, ngay_tao="28/11/2026")
        raw = dung_pptx_v2(deck, THU_MUC_ANH)
        _kiem_tra_meo_anh_pptx(raw)
        prs = pptx.Presentation(io.BytesIO(raw))
        all_text = "\n".join(
            p.text for sl in prs.slides for sh in sl.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs
        )
        assert tt.CAU_BAO_LU in all_text
        assert "chưa kiểm giá, phòng trống" in all_text
        for bad in ("CC BY", "Wikimedia", "tac_gia", "giay_phep", "Tác giả"):
            assert bad not in all_text

    # Thử ép đủ 9 layout trong một deck tổng hợp
    diem_ids = [m["id_muc"] for ng in canonical["ngay"] for m in ng["muc"] if m["loai"] != "nghi"]
    all_layouts_plan = {
        "theme_id": "song_huong_xanh",
        "cover_layout": "cover_split",
        "deck_title": "Lịch trình Huế 3 ngày",
        "deck_subtitle": "Kiểm thử đủ 9 layout",
        "highlights": ["Đại Nội Huế", "Chùa Thiên Mụ"],
        "hero_image_id": next(iter(canonical["anh_manifest"]["diem"]), None),
        "secondary_image_ids": list(canonical["anh_manifest"]["diem"])[:2],
        "include_overview": True,
        "overview_summaries": [{"ngay": ng["ngay"], "summary": "Tóm tắt chặng"} for ng in canonical["ngay"]],
        "days": [
            {
                "day_number": canonical["ngay"][0]["ngay"],
                "layout_id": "day_photo_feature",
                "day_header": "Ngày 1",
                "route_summary": "Kinh thành",
                "items": [{"id_muc": m["id_muc"], "short_copy": m.get("cau")} for m in canonical["ngay"][0]["muc"] if m["loai"] != "nghi"],
                "dining_note": None,
            },
            {
                "day_number": canonical["ngay"][1]["ngay"],
                "layout_id": "day_cards_2col",
                "day_header": "Ngày 2",
                "route_summary": "Kim Long",
                "items": [{"id_muc": m["id_muc"], "short_copy": m.get("cau")} for m in canonical["ngay"][1]["muc"] if m["loai"] != "nghi"],
                "dining_note": None,
            },
            {
                "day_number": canonical["ngay"][2]["ngay"],
                "layout_id": "day_compact_grid",
                "day_header": "Ngày 3",
                "route_summary": "Thủy Xuân",
                "items": [{"id_muc": m["id_muc"], "short_copy": m.get("cau")} for m in canonical["ngay"][2]["muc"] if m["loai"] != "nghi"],
                "dining_note": None,
            },
        ],
        "include_lodging": True,
        "lodging_header": None,
        "lodging_indices": [0, 1, 2],
        "notes_header": None,
    }
    assert set(ALL_LAYOUTS) == {
        "cover_hero", "cover_split", "overview_route", "day_timeline",
        "day_cards_2col", "day_photo_feature", "day_compact_grid", "lodging_dining", "notes_map",
    }
    deck_9 = plan_sang_cac_trang(all_layouts_plan, canonical, ngay_tao="28/11/2026")
    raw_9 = dung_pptx_v2(deck_9, THU_MUC_ANH)
    _kiem_tra_meo_anh_pptx(raw_9)
    assert len(diem_ids) > 0


def test_pptx_fit_three_tiers_vietnamese_diacritics():
    # Tầng 1: co font 0.5pt từ base_pt xuống min_pt
    pt_fit, fits, _, _ = co_chu_vua_khung("Đại Nội Huế — Hoàng thành triều Nguyễn", 4.0, 0.45, 16.0, 10.0)
    assert fits is True and 10.0 <= pt_fit <= 16.0

    # Tầng 2: quá dài ở min_pt -> báo overflow_errors
    van_ban_dai = "Cố đô Huế lưu giữ nhiều di sản văn hoá cung đình độc đáo bên dòng sông Hương hiền hoà. " * 6
    pt_over, fits_over, _, _ = co_chu_vua_khung(van_ban_dai, 4.0, 0.7, 12.0, 9.5)
    assert fits_over is False and pt_over == 9.5

    # Tầng 3: cắt sạch ở ranh giới từ + "…"
    cat = cat_sach_ranh_gioi(van_ban_dai, 4.0, 0.7, 9.5)
    assert cat.endswith("…") and len(cat) < len(van_ban_dai)
    _, fits_after, _, _ = co_chu_vua_khung(cat, 4.0, 0.7, 9.5, 9.5)
    assert fits_after is True


def _plan_tu_canonical(canonical: dict, *, short_copy_override: str | None = None, url_la: bool = False) -> SlideDeckPlan:
    days = []
    layouts = ("day_timeline", "day_cards_2col", "day_photo_feature", "day_compact_grid")
    for idx, ng in enumerate(canonical["ngay"]):
        mucs = [m for m in ng["muc"] if m["loai"] != "nghi"]
        days.append(SlideDayPlan(
            day_number=ng["ngay"],
            layout_id=layouts[idx % len(layouts)],
            day_header=f"Ngày {ng['ngay']}",
            route_summary=" → ".join(ng.get("chang") or []) or "Huế",
            items=[
                DayItemSlot(
                    id_muc=m["id_muc"],
                    short_copy=("Xem https://evil.example.com" if url_la and j == 0 else (short_copy_override or m.get("cau"))),
                    show_image=True,
                )
                for j, m in enumerate(mucs)
            ],
            dining_note=None,
        ))
    first_img = next(iter(canonical["anh_manifest"]["diem"]), None)
    return SlideDeckPlan(
        theme_id="di_san_tram",
        cover_layout="cover_hero",
        deck_title="Hành trình Huế",
        deck_subtitle="3 ngày khám phá",
        highlights=["Đại Nội Huế"],
        hero_image_id=first_img,
        secondary_image_ids=list(canonical["anh_manifest"]["diem"])[:2],
        include_overview=True,
        overview_summaries=[OverviewDayItem(ngay=ng["ngay"], summary="Tổng quan ngày") for ng in canonical["ngay"]],
        days=days,
        include_lodging=True,
        lodging_header="Lưu trú gợi ý",
        lodging_indices=[0, 1],
        notes_header="Lưu ý trước khi đi",
    )


def test_slide_designer_retry_postcheck_and_fallback():
    canonical = _lich_day_du(2)

    # 1. Hậu kiểm chặn URL lạ / bịa id_muc / ghi công ảnh / giờ lạ, nhưng cho phép giờ có trong `cau` gốc
    bad_plan = _plan_tu_canonical(canonical, url_la=True)
    assert any("chua_url_la" in e for e in hau_kiem_slide_deck(bad_plan, canonical))
    bad_time_plan = _plan_tu_canonical(canonical, short_copy_override="Giờ tự bịa 23:45 ngoài nguồn.")
    assert any("chua_gio_la" in e for e in hau_kiem_slide_deck(bad_time_plan, canonical))
    canonical_co_gio_cau = copy.deepcopy(canonical)
    canonical_co_gio_cau["ngay"][0]["muc"][0]["cau"] = "Mở cửa 07:30 mỗi ngày."
    ok_time_plan = _plan_tu_canonical(canonical_co_gio_cau, short_copy_override="Tham quan từ 07:30 theo nguồn.")
    assert hau_kiem_slide_deck(ok_time_plan, canonical_co_gio_cau) == []

    # 2. Vòng tự kiểm tràn chữ retry -> gọi lần 2 ngắn hơn -> đạt + ghi đủ token & USD
    long_copy = "Đoạn mô tả cực kỳ dài để kích hoạt cơ chế tự kiểm tra tràn chữ ở vòng đầu tiên. " * 6
    plan_tran = _plan_tu_canonical(canonical, short_copy_override=long_copy)
    plan_gon = _plan_tu_canonical(canonical, short_copy_override="Mô tả ngắn gọn chuẩn mực.")

    class FakeResponses:
        def __init__(self, outs):
            self.outs = list(outs)
            self.calls = 0

        async def parse(self, **kwargs):
            out = self.outs[min(self.calls, len(self.outs) - 1)]
            self.calls += 1
            if isinstance(out, Exception):
                raise out
            return SimpleNamespace(
                output_parsed=out,
                usage=SimpleNamespace(
                    input_tokens=1000,
                    output_tokens=200,
                    input_tokens_details=SimpleNamespace(cached_tokens=400, cache_write_tokens=0),
                ),
            )

    fake_client = SimpleNamespace(responses=FakeResponses([plan_tran, plan_gon]))
    res = asyncio.run(thiet_ke_slide(canonical, cfg={"model": "gpt-6-luna", "max_retries": 2, "timeout_seconds": 15, "fallback_code_only": True}, client=fake_client, use_llm=True))
    assert res.used_llm is True and res.retries == 1 and fake_client.responses.calls == 2
    assert res.input_tokens == 2000 and res.cached_tokens == 800 and res.output_tokens == 400 and res.usd > 0

    # 3. LLM liên tiếp vi phạm hậu kiểm -> rơi êm về bộ dựng thuần code (vẫn giữ an_toan + disclaimer)
    bad_client = SimpleNamespace(responses=FakeResponses([bad_plan, bad_plan, bad_plan]))
    res_fb = asyncio.run(thiet_ke_slide(canonical, cfg={"max_retries": 2, "fallback_code_only": True}, client=bad_client, use_llm=True))
    assert res_fb.used_llm is False and "post_validation_failed" in (res_fb.fallback_reason or "")
    assert res_fb.deck_plan["slides"][0]["an_toan"] == tt.CAU_BAO_LU


def test_slide_designer_route_cache_and_weighted_rate_limit():
    s = copy.deepcopy(load_settings(validate_private_paths=False))
    s["assistant"]["slide_designer"] = False
    flags_off = AssistantFlags.from_settings(s)

    app = FastAPI()
    app.include_router(xuat_router)
    app.add_middleware(ChanLuot, gioi_han=GioiHanLuot(tran=4))
    store = ConversationStore(len)
    app.state.conversations = store
    app.state.assistant_flags = flags_off
    cid = store.ensure(None)
    khung = lt2.xep_v2(flags_off.bang_lich_v2, lt2.tu_truong({"so_ngay": "2", "nguoi_lon": 2, "ngan_sach": "vua"}),
                       ngay_bat_dau=lt2.dt.date(2026, 12, 10))
    luu = {**sl.luu_tu_lich(khung, "2026-12-10", None), "an_toan": tt.CAU_BAO_LU}
    store.luu_lich(cid, luu)
    client = TestClient(app)

    # Cờ slide_designer tắt ⇒ POST /api/lich/pptx trả 404 (chú ý POST vẫn đi qua middleware trước hoặc sau tuỳ tran; đặt tran=4 cho 1 lần qua)
    assert client.post("/api/lich/pptx", cookies={"conversation_id": cid}).status_code == 404

    # Lần POST thứ 2 (3 + 3 = 6 > 4) ⇒ bị rate-limit trọng số 3 trả 429
    r_429 = client.post("/api/lich/pptx", cookies={"conversation_id": cid})
    assert r_429.status_code == 429 and r_429.json()["error"]["message"] == LOI_BAO

    # Kiểm cache theo (itinerary_hash, theme_id) trên app không giới hạn
    app2 = FastAPI()
    app2.include_router(xuat_router)
    store2 = ConversationStore(len)
    app2.state.conversations = store2
    s["assistant"]["slide_designer"] = True
    flags_on = AssistantFlags.from_settings(s)
    app2.state.assistant_flags = flags_on
    cid2 = store2.ensure(None)
    store2.luu_lich(cid2, luu)

    from api.routes.xuat import lich_tu_luu
    lich_c, cau_c = lich_tu_luu(luu, flags_on)
    canonical = chuan_hoa_lich(lich_c, cau_c, an_toan=luu["an_toan"], thu_muc_anh=THU_MUC_ANH)
    sample_plan = _plan_tu_canonical(canonical)
    call_counter = {"n": 0}

    class CountResponses:
        async def parse(self, **kwargs):
            call_counter["n"] += 1
            return SimpleNamespace(
                output_parsed=sample_plan,
                usage=SimpleNamespace(input_tokens=500, output_tokens=100, input_tokens_details=None),
            )

    app2.state.generator = SimpleNamespace(client=SimpleNamespace(responses=CountResponses()))
    c2 = TestClient(app2)
    # Kiểm GET /api/lich/pptx không gọi LLM (`0 USD`, đóng lỗ hổng rate-limit), chỉ POST mới gọi LLM
    r_get = c2.get("/api/lich/pptx", cookies={"conversation_id": cid2})
    assert r_get.status_code == 200 and r_get.headers.get("X-Slide-Layouts")
    assert call_counter["n"] == 0, "GET /api/lich/pptx không được gọi LLM"

    # Kiểm plan_sang_cac_trang ép giữ lodging_dining khi có o_dau dù LLM trả include_lodging=False
    plan_no_lodging = sample_plan.model_copy(update={"include_lodging": False})
    deck_forced = plan_sang_cac_trang(plan_no_lodging.model_dump(), canonical)
    assert any(sl["layout_id"] == "lodging_dining" for sl in deck_forced["slides"])

    r1 = c2.post("/api/lich/pptx", json={"theme_id": "di_san_tram"}, cookies={"conversation_id": cid2})
    r2 = c2.post("/api/lich/pptx", json={"theme_id": "di_san_tram"}, cookies={"conversation_id": cid2})
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.headers.get("X-Slide-Layouts") and r2.headers.get("X-Slide-Layouts")
    assert call_counter["n"] == 1, "Cùng (itinerary_hash, theme_id) phải dùng cache trong phiên, không gọi lại model"
    _kiem_tra_meo_anh_pptx(r1.content)

    # Kiểm lịch 5 ngày nhiều điểm: notes_map chia 2 cột sạch không tràn & câu > 170 ký tự không bị cắt cụt giữa chừng bởi _gon
    c5 = _lich_day_du(5)
    d5 = trang_lich_v2(c5, ngay_tao="28/11/2026")
    assert len(kiem_tra_tran_chu([sl for sl in d5["slides"] if sl.get("layout_id") == "notes_map"])) == 0
    _kiem_tra_meo_anh_pptx(dung_pptx_v2(d5, THU_MUC_ANH))

    # Kiểm POST /api/lich/pptx tôn trọng slide_designer_cfg.use_llm=False (0 lần gọi OpenAI, vẫn ra .pptx v2 9 layout)
    s_code = copy.deepcopy(s)
    s_code["assistant"]["slide_designer"] = True
    s_code["slide_designer_cfg"]["use_llm"] = False
    app3 = FastAPI()
    app3.include_router(xuat_router)
    store3 = ConversationStore(len)
    app3.state.conversations = store3
    app3.state.assistant_flags = AssistantFlags.from_settings(s_code)
    cid3 = store3.ensure(None)
    store3.luu_lich(cid3, luu)
    call_counter_code = {"n": 0}

    class FailIfCalled:
        async def parse(self, **kwargs):
            call_counter_code["n"] += 1
            raise AssertionError("Không được gọi LLM khi slide_designer_cfg.use_llm=False")

    app3.state.generator = SimpleNamespace(client=SimpleNamespace(responses=FailIfCalled()))
    r_code = TestClient(app3).post("/api/lich/pptx", json={"theme_id": "song_huong_xanh"}, cookies={"conversation_id": cid3})
    assert r_code.status_code == 200 and r_code.headers.get("X-Slide-Layouts")
    assert call_counter_code["n"] == 0
    _kiem_tra_meo_anh_pptx(r_code.content)
