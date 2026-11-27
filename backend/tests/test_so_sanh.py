"""Unit test cho công cụ `so_sanh_diem_den` (Đợt 2, cờ `so_sanh_diem_den`)."""
import asyncio
import re

import pytest

from llm import khoang_cach as kc
from llm import lich_trinh_v2 as lt2
from llm import liet_ke as lk
from llm import so_sanh as ss
from llm import the_noi as thn
from llm.assistant import AnswerTrace, AssistantFlags, _lich_extra, set_notice, so_sanh_for_turn


def _bang_mau() -> lt2.BangV2:
    diem = (
        {
            "id": "lang_tu_duc",
            "ten": "Lăng Tự Đức",
            "cum": "thuy_xuan",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "nua_buoi",
            "trong_nha": "ngoai_troi",
            "bac_thang": "it",
            "gio_mo_cua": "INTERNAL_NOTE_DO_NOT_LEAK_TU_DUC",
            "uu_tien": {"chung": 2},
            "nguon": "heritages/heritage/Lăng Tự Đức.md",
            "toi_nhe": False,
        },
        {
            "id": "lang_minh_mang",
            "ten": "Lăng Minh Mạng",
            "cum": "thuy_xuan",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "nua_buoi",
            "trong_nha": "ngoai_troi",
            "bac_thang": "nhieu",
            "gio_mo_cua": "INTERNAL_NOTE_DO_NOT_LEAK_MINH_MANG",
            "uu_tien": {"chung": 3},
            "nguon": "heritages/heritage/Lăng Minh Mạng.md",
            "toi_nhe": False,
        },
        {
            "id": "chua_thien_mu",
            "ten": "Chùa Thiên Mụ",
            "cum": "kim_long",
            "buoi": ["sang", "chieu"],
            "thoi_luong": "ngan",
            "trong_nha": "ngoai_troi",
            "bac_thang": "it",
            "uu_tien": {"chung": 1},
            "nguon": "heritages/heritage/Chùa Thiên Mụ.md",
            "toi_nhe": False,
        },
    )
    return lt2.BangV2(
        diem=diem,
        theo_id={d["id"]: d for d in diem},
        cum={"thuy_xuan": "Thủy Xuân", "kim_long": "Kim Long"},
        uu_tien=("chung",),
        loai_hien=(),
        nhac_mua_chung="",
        toi_nhe=(),
        thu_tu_toi=(),
    )


BANG_KC = kc.BangKhoangCach(
    ten={"lang_tu_duc": "Lăng Tự Đức", "lang_minh_mang": "Lăng Minh Mạng", "chua_thien_mu": "Chùa Thiên Mụ"},
    ten_khac={"lang_tu_duc": (), "lang_minh_mang": (), "chua_thien_mu": ()},
    cap={
        "lang_tu_duc|lang_minh_mang": {"km": 8.2, "phut": 14},
        "lang_tu_duc|chua_thien_mu": {"km": 6.5, "phut": 13},
    },
)

THE_NOI = thn.Bang(
    noi=(
        thn.Noi(
            "Lăng Tự Đức",
            "heritages/heritage/Lăng Tự Đức.md",
            re.compile("Lăng Tự Đức"),
            ("Giờ mở cửa: 07h00 – 17h30.",),
            "| 3 | Lăng Tự Đức | Thủy Xuân | 150.000 | Miễn phí |",
            None,
        ),
        thn.Noi(
            "Lăng Minh Mạng",
            "heritages/heritage/Lăng Minh Mạng.md",
            re.compile("Lăng Minh Mạng"),
            ("Giờ mở cửa: 07h30 – 17h00.",),
            "| 4 | Lăng Minh Mạng | Hương Thọ | 150.000 | Miễn phí |",
            None,
        ),
    ),
    ve_rel="travel/tickets/ve.md",
    ve_tieu_de="Bảng giá vé tham quan Huế",
    ve_dau="| STT | Điểm | Địa giới | Người lớn | Trẻ em |",
)


def test_validation_requires_tim_them_and_bang():
    with pytest.raises(ValueError, match="so_sanh_diem_den"):
        AssistantFlags(so_sanh_diem_den=True, tim_them=True)


def test_co_tu_khoa_luot_detects_comparisons():
    assert ss.co_tu_khoa_luot("So sánh Lăng Tự Đức và Lăng Minh Mạng giúp mình", ()) is True
    assert ss.co_tu_khoa_luot("Đi cùng người lớn tuổi nên chọn lăng nào ít bậc thang hơn?", ()) is True
    assert ss.co_tu_khoa_luot("Nên đi Đại Nội hay Chùa Thiên Mụ trước?", ()) is True
    assert ss.co_tu_khoa_luot("Giữa Đầm Chuồn với Đầm Lập An chỗ nào hợp hơn?", ()) is True
    assert ss.co_tu_khoa_luot("Lăng Tự Đức xây năm nào?", ()) is False


def test_ket_qua_reads_the_noi_never_gio_mo_cua_and_rejects_under_two_points():
    bang = _bang_mau()
    assert ss.ket_qua(bang, BANG_KC, THE_NOI, ("lang_tu_duc", "lang_tu_duc", ss.KHONG_CO)) == ((), ())
    assert ss.ket_qua(bang, BANG_KC, THE_NOI, ("khong_ton_tai", ss.KHONG_CO, None)) == ((), ())

    dong, chon = ss.ket_qua(bang, BANG_KC, THE_NOI, ("lang_tu_duc", "lang_minh_mang", "chua_thien_mu"))
    assert [d["id"] for d in chon] == ["lang_tu_duc", "lang_minh_mang", "chua_thien_mu"]
    van_ban = "\n".join(dong)
    assert "INTERNAL_NOTE_DO_NOT_LEAK" not in van_ban
    assert "07h00 – 17h30" in van_ban and "150.000" in van_ban
    assert "nhiều bậc thang" in van_ban
    assert "Đường đi Lăng Tự Đức ↔ Lăng Minh Mạng" in van_ban
    assert kc.CAU_GHI_CHU in dong


def test_so_sanh_for_turn_dedup_order_invariant_and_notice():
    bang = _bang_mau()
    bai_mm = lk.bai_tu_markdown(
        "heritages/heritage/Lăng Minh Mạng.md",
        "# Lăng Minh Mạng\n\nTrạng thái: mở cửa; tạm dừng đón khách khu vực bến thuyền khi nước sông dâng cao.\n",
    )

    flags_off = AssistantFlags(tim_them=True, bang_lich_v2=bang)
    assert "so_sanh_fn" not in _lich_extra("So sánh Lăng Tự Đức và Lăng Minh Mạng", None, None, AnswerTrace(), None, None, flags_off)

    flags_on = AssistantFlags(
        tim_them=True,
        bang_lich_v2=bang,
        khoang_cach=True,
        khoang_cach_bang=BANG_KC,
        so_sanh_diem_den=True,
        chong_lap_cong_cu=True,
        noi_dong_tam_ngung=True,
    )
    assert "so_sanh_fn" in _lich_extra("So sánh Lăng Tự Đức và Lăng Minh Mạng", None, None, AnswerTrace(), None, None, flags_on)

    trace = AnswerTrace()
    fn = so_sanh_for_turn(trace, bang, BANG_KC, THE_NOI, {bai_mm.rel: bai_mm}, chong_lap=True)

    # Thiếu 2 điểm khác nhau -> trả actionable feedback, không đăng nguồn
    thieu = asyncio.run(fn("lang_tu_duc", "lang_tu_duc"))
    assert thieu == ss.CAU_THIEU_DIEM
    assert trace.so_nguon == []

    # So sánh hợp lệ -> nguồn [1]
    out1 = asyncio.run(fn("lang_tu_duc", "lang_minh_mang"))
    assert "[Nguồn 1]" in out1
    assert len(trace.so_nguon) == 1 and trace.so_nguon[0].source == ss.NGUON_SOURCE
    assert trace.tools[-1]["n_ket_qua"] == 2

    # Đảo thứ tự cặp điểm với chong_lap=True -> nhận ra trùng, không đăng nguồn mới
    out_dup = asyncio.run(fn("lang_minh_mang", "lang_tu_duc"))
    assert "nguồn [1]" in out_dup
    assert trace.tools[-1].get("lap") is True
    assert len(trace.so_nguon) == 1

    trace.answer = "Lăng Minh Mạng có nhiều bậc thang hơn Lăng Tự Đức, cách nhau khoảng 8,2 km [1]."
    trace.cited = (trace.so_nguon[0],)
    set_notice(trace, flags_on)
    assert kc.CAU_GHI_CHU in (trace.notice or "")
    assert trace.luu_y_nguon is not None and "tạm dừng" in trace.luu_y_nguon.casefold()


def test_generator_registers_so_sanh_tool_schema_and_settings_load():
    from core.settings_loader import load_settings
    from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator

    async def fake_tim_kho(cau: str) -> str:
        return cau

    settings = load_settings(validate_private_paths=False)
    on = {**settings, "assistant": {**settings["assistant"], "so_sanh_diem_den": True}}
    flags = AssistantFlags.from_settings(on)
    assert flags.so_sanh_diem_den is True and flags.bang_lich_v2 is not None and flags.the_noi_bang is not None

    extra = _lich_extra("So sánh Lăng Tự Đức và Lăng Minh Mạng giúp mình", None, None, AnswerTrace(), None, None, flags)
    assert "so_sanh_fn" in extra
    gen = OpenAIFullCorpusGenerator(client=object(), model="x")
    agent, _, _ = gen._assistant_for(fake_tim_kho, **extra)
    names = [t.name for t in agent.tools]
    assert "so_sanh_diem_den" in names
    tool = next(t for t in agent.tools if t.name == "so_sanh_diem_den")
    assert set(tool.params_json_schema["properties"]) == {"diem_1", "diem_2", "diem_3"}

    # Kiểm tra kết quả thật trên bảng v16 + the_noi thật không rò gio_mo_cua
    dong, chon = ss.ket_qua(flags.bang_lich_v2, flags.khoang_cach_bang, flags.the_noi_bang, ("lang_tu_duc", "lang_minh_mang"))
    assert len(chon) == 2 and dong

    off = {**settings, "assistant": {**settings["assistant"], "goi_y_mua_nang": False, "so_sanh_diem_den": False}}
    flags_off = AssistantFlags.from_settings(off)
    extra_off = _lich_extra("So sánh Lăng Tự Đức và Lăng Minh Mạng giúp mình", None, None, AnswerTrace(), None, None, flags_off)
    agent_off, _, _ = gen._assistant_for(fake_tim_kho, **extra_off)
    assert "so_sanh_diem_den" not in [t.name for t in agent_off.tools]
