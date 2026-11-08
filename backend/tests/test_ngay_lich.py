"""Phase 9 T1 — ngày + âm lịch Việt Nam (`llm/ngay_lich.py`). Logic thuần, 0 USD, không mạng.

Đáp án công khai (E kiểm 08/11/2026): Tết các năm — bảng "Ngày đầu năm theo Con giáp" của vi.wikipedia "Tết Nguyên đán" (tính theo giờ Hà Nội UTC+7; bảng
không ghi nguồn) · Tết 2007 VN 17/02 ↔ TQ 18/02 — Tuổi Trẻ 16/07/2006 "Vì sao lịch VN và Trung Quốc lệch nhau" · Tết 1985 VN 21/01 ↔ TQ 20/02 — spec Phase 9
§12.5 (en.wikipedia "Vietnamese calendar", C kiểm). `lunar-vn` khớp bảng tính sẵn của Hồ Ngọc Đức mọi năm 1966–2099 (`data/phase_9/t1/tools/so_tet.py`).
"""
import datetime as dt

import pytest
from lunar_vn import LunarDate, lunar_to_solar

from llm import ngay_lich as nl

TET = {1985: "21/01/1985", 2007: "17/02/2007", 2020: "25/01/2020", 2021: "12/02/2021", 2022: "01/02/2022", 2023: "22/01/2023",
       2024: "10/02/2024", 2025: "29/01/2025", 2026: "17/02/2026", 2027: "06/02/2027", 2030: "02/02/2030"}


@pytest.mark.parametrize("nam, ngay", TET.items())
def test_tet_matches_public_dates(nam, ngay):
    chu = nl.doi(1, 1, nam, "am")
    assert f"{ngay} dương lịch — ngày 1 tháng Giêng âm lịch" in chu


@pytest.mark.parametrize("nam, viet_nam, trung_quoc", [(1985, dt.date(1985, 1, 21), dt.date(1985, 2, 20)),
                                                       (2007, dt.date(2007, 2, 17), dt.date(2007, 2, 18))])
def test_vietnam_utc7_differs_from_china_utc8(nam, viet_nam, trung_quoc):
    # lý do chọn lịch UTC+7: cùng thuật toán ở UTC+8 ra đúng ngày Tết của Trung Quốc ⇒ thư viện lịch Trung Quốc sẽ sai ở các năm này
    assert lunar_to_solar(LunarDate(1, 1, nam)) == viet_nam
    assert lunar_to_solar(LunarDate(1, 1, nam), time_zone=8.0) == trung_quoc
    assert nl.doi(1, 1, nam, "am").split(" dương")[0].endswith(viet_nam.strftime("%d/%m/%Y"))


def test_round_trip_every_day_in_range():
    d, het = dt.date(nl.NAM_MIN, 1, 1), dt.date(nl.NAM_MAX, 12, 31)
    while d <= het:
        am = nl.solar_to_lunar(d)
        if nl.NAM_MIN <= am.year <= nl.NAM_MAX:
            assert nl.doi(am.day, am.month, am.year, "am", am.leap) == nl.mo_ta(d)
        d += dt.timedelta(days=1)


def test_weekday_and_can_chi_text():
    assert nl.mo_ta(dt.date(2026, 2, 17)) == "Thứ Ba, 17/02/2026 dương lịch — ngày 1 tháng Giêng âm lịch, năm Bính Ngọ"
    assert nl.mo_ta(dt.date(2026, 2, 16)).endswith("ngày 29 tháng Chạp âm lịch, năm Ất Tỵ")  # can chi theo NĂM ÂM, không theo năm dương


@pytest.mark.parametrize("args", [(30, 12, 2025, "am"),            # tháng Chạp Ất Tỵ chỉ 29 ngày (thư viện lặng lẽ ra ngày đầu tháng sau — code bắt)
                                  (1, 6, 2026, "am", True),         # 2026 không có tháng nhuận
                                  (31, 4, 2026, "duong"), (29, 2, 2027, "duong"), (0, 1, 2026, "am"), (1, 13, 2026, "am"),
                                  (1, 1, 2026, "duong", True)])
def test_impossible_dates_get_fixed_sentence(args):
    assert nl.doi(*args) == nl.CAU_NGAY_SAI


def test_leap_month_is_named():
    assert nl.doi(1, 6, 2025, "am", True) == "Thứ Sáu, 25/07/2025 dương lịch — ngày 1 tháng 6 (nhuận) âm lịch, năm Ất Tỵ"


@pytest.mark.parametrize("nam", [1968, 1975, 2101, 1])
def test_years_outside_range_get_fixed_sentence(nam):
    # trước 1976 hai miền khác lịch (Tết Mậu Thân 1968: Bắc 29/01, Nam — có Huế — 30/01) ⇒ không đoán
    assert nl.doi(1, 1, nam, "am") == nl.CAU_NGOAI_KHOANG
    assert nl.doi(1, 1, nam, "duong") == nl.CAU_NGOAI_KHOANG


def test_today_uses_vietnam_time_not_server_time():
    # 17:30 UTC 07/11 = 00:30 08/11 giờ Việt Nam
    assert nl.hom_nay(dt.datetime(2026, 11, 7, 17, 30, tzinfo=dt.timezone.utc)) == dt.date(2026, 11, 8)
    assert nl.hom_nay(dt.datetime(2026, 11, 7, 16, 59, tzinfo=dt.timezone.utc)) == dt.date(2026, 11, 7)
