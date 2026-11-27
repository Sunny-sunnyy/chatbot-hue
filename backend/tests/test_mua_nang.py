"""Unit test cho công cụ `goi_y_phuong_an_mua_nang` (Đợt 2, cờ `goi_y_mua_nang`) và trần vòng `max_turns_for`."""
import asyncio
import datetime as dt

import pytest

from llm import khoang_cach as kc
from llm import lich_trinh_v2 as lt2
from llm import liet_ke as lk
from llm import mua_nang as mn
from llm import thoi_tiet as tt
from llm.assistant import (
    AnswerTrace,
    AssistantFlags,
    MAY_HAVE_CHANGED_NOTICE,
    _lich_extra,
    mua_nang_for_turn,
    set_notice,
)
from llm.generator_openai_full_corpus import ASSISTANT_MAX_TURNS, MAX_VONG_CONG_CU_TOI_DA, max_turns_for


def _bang_mau() -> lt2.BangV2:
    diem = (
        {
            "id": "dai_noi",
            "ten": "Đại Nội Huế",
            "cum": "kinh_thanh",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "nua_buoi",
            "trong_nha": "ngoai_troi",
            "bac_thang": "it",
            "uu_tien": {"chung": 1},
            "nguon": "heritages/heritage/Đại Nội Huế.md",
            "toi_nhe": False,
        },
        {
            "id": "bao_tang_co_vat",
            "ten": "Bảo tàng Cổ vật Cung đình Huế",
            "cum": "kinh_thanh",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "ngan",
            "trong_nha": "trong_nha",
            "bac_thang": "it",
            "uu_tien": {"chung": 3},
            "nguon": "heritages/heritage/Bảo tàng Cổ vật Cung đình Huế.md",
            "toi_nhe": False,
        },
        {
            "id": "bao_tang_le_ba_dang",
            "ten": "Trung tâm Nghệ thuật Lê Bá Đảng",
            "cum": "bo_nam",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "ngan",
            "trong_nha": "trong_nha",
            "bac_thang": "it",
            "uu_tien": {"chung": 4},
            "nguon": "travel/places/Lê Bá Đảng.md",
            "toi_nhe": False,
        },
        {
            "id": "aeon_mall",
            "ten": "AEON Mall Huế",
            "cum": "an_cuu",
            "buoi": ["toi"],
            "thoi_luong": "ngan",
            "trong_nha": "trong_nha",
            "bac_thang": "it",
            "uu_tien": {"chung": 8},
            "nguon": "travel/places/AEON Mall Huế.md",
            "toi_nhe": True,
        },
        {
            "id": "thac_nhi_ho",
            "ten": "Thác Nhị Hồ",
            "cum": "phu_loc",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "nua_buoi",
            "trong_nha": "ca_hai",
            "bac_thang": "nhieu",
            "mua_luu_y": {"thang": [9, 10, 11, 12, 1, 2], "bo_khoi_lich": True},
            "uu_tien": {"chung": 5},
            "nguon": "travel/places/Thác Nhị Hồ.md",
            "toi_nhe": False,
        },
    )
    return lt2.BangV2(
        diem=diem,
        theo_id={d["id"]: d for d in diem},
        cum={"kinh_thanh": "Kinh Thành", "bo_nam": "Bờ Nam", "an_cuu": "An Cựu", "phu_loc": "Phú Lộc"},
        uu_tien=("chung",),
        loai_hien=(),
        nhac_mua_chung="",
        toi_nhe=("aeon_mall",),
        thu_tu_toi=(),
    )


BANG_KC = kc.BangKhoangCach(
    ten={
        "dai_noi": "Đại Nội Huế",
        "bao_tang_co_vat": "Bảo tàng Cổ vật Cung đình Huế",
        "bao_tang_le_ba_dang": "Trung tâm Nghệ thuật Lê Bá Đảng",
        "aeon_mall": "AEON Mall Huế",
        "thac_nhi_ho": "Thác Nhị Hồ",
    },
    ten_khac={"dai_noi": (), "bao_tang_co_vat": (), "bao_tang_le_ba_dang": (), "aeon_mall": (), "thac_nhi_ho": ()},
    cap={
        "dai_noi|bao_tang_co_vat": {"km": 0.6, "phut": 3},
        "dai_noi|bao_tang_le_ba_dang": {"km": 2.4, "phut": 7},
        "dai_noi|aeon_mall": {"km": 4.5, "phut": 12},
        "dai_noi|thac_nhi_ho": {"km": 45.0, "phut": 55},
    },
)


def _du_bao_mau(mua_mm: float = 12.0) -> tt.DuBao:
    hom = dt.date(2026, 11, 27)
    return tt.DuBao(
        trang_thai="ok",
        ngay=[
            {
                "ngay": hom,
                "tmin": 22,
                "tmax": 26,
                "mua": mua_mm,
                "xs": 80,
            },
            {
                "ngay": hom + dt.timedelta(days=1),
                "tmin": 23,
                "tmax": 35,
                "mua": 0.0,
                "xs": 10,
            },
        ],
        cap_nhat="10:00 27/11",
        ms=1.0,
        tu_cache=True,
        loi=None,
    )


def test_default_flags_off_and_validation():
    f = AssistantFlags()
    assert f.goi_y_mua_nang is False
    assert f.so_sanh_diem_den is False
    with pytest.raises(ValueError, match="goi_y_mua_nang"):
        AssistantFlags(goi_y_mua_nang=True, tim_them=True)


def test_max_turns_cap_stops_linear_tool_growth():
    obj = object()
    assert MAX_VONG_CONG_CU_TOI_DA == 6
    assert max_turns_for(None) == ASSISTANT_MAX_TURNS
    assert max_turns_for(obj, obj) == 6
    assert max_turns_for(obj, None, 6) == 7
    assert max_turns_for(obj, obj, 4, obj, obj, obj, obj) == 6
    assert max_turns_for(obj, obj, 5, obj, obj, obj, obj) == 6


def test_co_tu_khoa_luot_blocks_storm_and_non_weather_queries():
    assert mn.co_tu_khoa_luot("Chiều nay trời mưa nên đi đâu gần Đại Nội?", ()) is True
    assert mn.co_tu_khoa_luot("Nắng nóng quá, có chỗ nào trong nhà buổi sáng không?", ()) is True
    assert mn.co_tu_khoa_luot("Gần Đại Nội có gì chơi?", [("Trời đang mưa quá", "...")]) is True
    assert mn.co_tu_khoa_luot("Bão số 5 đang vào Huế nên đi đâu tránh bão?", ()) is False
    assert mn.co_tu_khoa_luot("Khu trung tâm đang ngập lụt nặng có đi chơi đâu được không?", ()) is False
    assert mn.co_tu_khoa_luot("Đại Nội Huế xây dựng năm nào?", ()) is False


def test_loc_diem_and_ket_qua_filter_indoor_cluster_buoi_and_season():
    bang = _bang_mau()
    # Tháng 11: Thác Nhị Hồ bị loại vì `mua_luu_y`; Đại Nội bị loại vì `ngoai_troi` + là `diem_goc`; AEON chỉ có buổi tối
    dong, chon, nguy_hiem = mn.ket_qua(
        bang, BANG_KC, "mua", "dai_noi", "chieu", 0, kq_du_bao=_du_bao_mau(15.0), hom_nay=dt.date(2026, 11, 27)
    )
    assert nguy_hiem is False
    ids = [d["id"] for d in chon]
    assert ids == ["bao_tang_co_vat", "bao_tang_le_ba_dang"]
    assert "cách điểm gốc" in dong[2]
    assert dong[-1] == kc.CAU_GHI_CHU

    # Buổi tối -> AEON Mall xuất hiện
    _, chon_toi, _ = mn.ket_qua(bang, BANG_KC, "mua", "khong_ro", "toi", None, hom_nay=dt.date(2026, 11, 27))
    assert [d["id"] for d in chon_toi] == ["aeon_mall"]

    # Tháng 5 (ngoài mùa mưa lũ): Thác Nhị Hồ (`ca_hai`) được giữ
    _, chon_he, _ = mn.ket_qua(bang, BANG_KC, "nang_nong", "khong_ro", "sang", None, hom_nay=dt.date(2026, 5, 10))
    assert "thac_nhi_ho" in [d["id"] for d in chon_he]


def test_ket_qua_blocks_extreme_rain_over_100mm():
    bang = _bang_mau()
    dong, chon, nguy_hiem = mn.ket_qua(
        bang, BANG_KC, "mua", "dai_noi", "chieu", 0, kq_du_bao=_du_bao_mau(125.0), hom_nay=dt.date(2026, 11, 27)
    )
    assert nguy_hiem is True
    assert chon == [] and dong == ()


def test_mua_nang_for_turn_dedup_notice_and_storm_block():
    bang = _bang_mau()
    bai_co_vat = lk.bai_tu_markdown(
        "heritages/heritage/Bảo tàng Cổ vật Cung đình Huế.md",
        "# Bảo tàng Cổ vật Cung đình Huế\n\nTrạng thái: mở cửa đón khách; tạm dừng đón khách khi có bão lũ lớn để bảo đảm an toàn.\n",
    )
    bai_lbd = lk.bai_tu_markdown(
        "travel/places/Lê Bá Đảng.md",
        "# Trung tâm Nghệ thuật Lê Bá Đảng\n\nGiờ mở cửa: 08:00 - 17:00.\n",
    )

    async def fake_du_bao_ok():
        return _du_bao_mau(10.0)

    async def fake_du_bao_ngap():
        return _du_bao_mau(140.0)

    # Cờ tắt -> _lich_extra không gắn mua_nang_fn
    flags_off = AssistantFlags(tim_them=True, thoi_tiet=True, du_bao=fake_du_bao_ok, bang_lich_v2=bang, khoang_cach=True, khoang_cach_bang=BANG_KC)
    assert "mua_nang_fn" not in _lich_extra("Trời mưa đi đâu?", None, None, AnswerTrace(), None, None, flags_off)

    # Cờ bật + câu bão/lũ -> _lich_extra không đưa công cụ
    flags_on = AssistantFlags(
        tim_them=True,
        thoi_tiet=True,
        du_bao=fake_du_bao_ok,
        bang_lich_v2=bang,
        khoang_cach=True,
        khoang_cach_bang=BANG_KC,
        goi_y_mua_nang=True,
        chong_lap_cong_cu=True,
        noi_dong_tam_ngung=True,
        may_have_changed_notice=True,
    )
    assert "mua_nang_fn" not in _lich_extra("Bão lũ nên đi đâu?", None, None, AnswerTrace(), None, None, flags_on)

    # Câu mưa thường -> trả nguồn [1], chống lặp + giữ cảnh báo tạm ngừng khi set_notice
    trace = AnswerTrace()
    fn = mua_nang_for_turn(trace, "Trời mưa chiều nay gần Đại Nội đi đâu?", bang, BANG_KC, fake_du_bao_ok,
                           {bai_co_vat.rel: bai_co_vat, bai_lbd.rel: bai_lbd}, chong_lap=True)
    out1 = asyncio.run(fn("mua", "dai_noi", "chieu", 0))
    assert "[Nguồn 1]" in out1
    assert len(trace.so_nguon) == 1
    assert trace.so_nguon[0].source == mn.NGUON_SOURCE
    assert trace.tools[-1]["n_ket_qua"] == 2

    out_dup = asyncio.run(fn("mua", "dai_noi", "chieu", 0))
    assert "nguồn [1]" in out_dup
    assert trace.tools[-1].get("lap") is True
    assert len(trace.so_nguon) == 1

    trace.answer = "Chiều mưa bạn có thể ghé Bảo tàng Cổ vật Cung đình Huế hoặc Trung tâm Nghệ thuật Lê Bá Đảng [1]."
    trace.cited = (trace.so_nguon[0],)
    set_notice(trace, flags_on)
    assert trace.luu_y_nguon is not None and "tạm dừng" in trace.luu_y_nguon.casefold()
    assert MAY_HAVE_CHANGED_NOTICE in (trace.notice or "")

    # Mưa >= 100mm -> chặn ngay trong tool + bật dấu bao_lu trên trace
    trace_ngap = AnswerTrace()
    fn_ngap = mua_nang_for_turn(trace_ngap, "Trời mưa đi đâu?", bang, BANG_KC, fake_du_bao_ngap, chong_lap=True)
    blocked = asyncio.run(fn_ngap("mua", "dai_noi", "chieu", 0))
    assert "112" in blocked and "tuyệt đối không gợi ý" in blocked
    assert trace_ngap.so_nguon == []
    assert (trace_ngap.thoi_tiet_ctx or {}).get("bao_lu") is True
    assert trace_ngap.tools[-1].get("bao_lu") is True


def test_generator_registers_mua_nang_tool_schema_and_settings_load():
    from core.settings_loader import load_settings
    from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator

    async def fake_tim_kho(cau: str) -> str:
        return cau

    settings = load_settings(validate_private_paths=False)
    on = {**settings, "assistant": {**settings["assistant"], "goi_y_mua_nang": True}}
    flags = AssistantFlags.from_settings(on)
    assert flags.goi_y_mua_nang is True and flags.bang_lich_v2 is not None

    extra = _lich_extra("Trời mưa chiều nay nên đi đâu gần Đại Nội?", None, None, AnswerTrace(), None, None, flags)
    assert "mua_nang_fn" in extra
    gen = OpenAIFullCorpusGenerator(client=object(), model="x")
    agent, _, _ = gen._assistant_for(fake_tim_kho, **extra)
    names = [t.name for t in agent.tools]
    assert "goi_y_phuong_an_mua_nang" in names
    tool = next(t for t in agent.tools if t.name == "goi_y_phuong_an_mua_nang")
    assert set(tool.params_json_schema["properties"]) == {"tinh_huong", "diem_goc", "buoi", "ngay"}

    # Khi tắt trong bản sao settings: không đăng ký tool mới
    off = {**settings, "assistant": {**settings["assistant"], "goi_y_mua_nang": False, "so_sanh_diem_den": False}}
    flags_off = AssistantFlags.from_settings(off)
    extra_off = _lich_extra("Trời mưa chiều nay nên đi đâu gần Đại Nội?", None, None, AnswerTrace(), None, None, flags_off)
    agent_off, _, _ = gen._assistant_for(fake_tim_kho, **extra_off)
    assert "goi_y_phuong_an_mua_nang" not in [t.name for t in agent_off.tools]
