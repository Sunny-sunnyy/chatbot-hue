"""Xuất lịch `.ics` v2 chuẩn RFC 5545 (Đợt 5 — Phần A, 0 USD, 0 OAuth).

Khác biệt so với bản v1 ở client:
- Dùng `VTIMEZONE` `Asia/Ho_Chi_Minh` (`+0700`, không giờ mùa hè) + `DTSTART;TZID=Asia/Ho_Chi_Minh:...`.
- Hỗ trợ mục chỉ có 1 mốc giờ (mặc định 90 phút cho tham quan, 60 phút cho buổi tối) và mục không có giờ (sự kiện cả ngày `VALUE=DATE`).
- Thêm nhắc nhận phòng (`14:00–15:00` ngày 1) và trả phòng (`11:00–12:00` ngày cuối) từ `o_dau`, luôn giữ disclaimer `"chưa kiểm giá, phòng trống"`.
- Giữ `an_toan` ở đầu `DESCRIPTION`, ổn định `UID` theo `itinerary_hash`, kèm `SEQUENCE` và `URL;VALUE=URI:<map_url>`, gấp dòng ≤ 75 byte UTF-8.
- Chặn cứng `ngay_di == None` (hoặc ngày thiếu `ngay_thang`), tuyệt đối không tự đoán ngày.
"""
import datetime as dt
import re
from typing import Any

from api.hanh_trinh_chuan import MAP_PREFIX, chuan_hoa_lich

TZID = "Asia/Ho_Chi_Minh"
NHAC_GIO = "Giờ gợi ý theo thời lượng tham quan — kiểm lại giờ mở cửa trước khi đi."
NHAC_CA_NGAY = "Chưa có khung giờ cố định — kiểm lại giờ mở cửa trước khi đi."
NHAC_SUAT = "Có nhiều suất — chọn suất khác nếu cần."
DISCLAIMER_O_DAU = "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống."
_GIO_RE = re.compile(r"(?<!\d)(\d{1,2}):(\d{2})(?!\d)")
_LOAI_SU_KIEN = frozenset({"tham_quan", "hoat_dong_toi"})


class ThieuNgayDiError(ValueError):
    """Lỗi rõ ràng khi lịch chưa chọn ngày đi (`ngay_di is None`)."""


def doc_gio_v2(gio: str | None, loai: str) -> tuple[int, int, bool] | None:
    """Đọc chuỗi giờ thành `(bat_dau_phut, ket_thuc_phut, co_nhieu_suat)` hoặc `None` (sự kiện cả ngày).

    - `"8:00 – 10:30"` -> `(480, 630, False)`
    - `"suất 19:00 / 20:00 ..."` -> `(1140, 1200, True)`
    - 1 mốc `"8:00"` -> `+90` phút nếu `tham_quan`, `+60` phút nếu `hoat_dong_toi`
    - Không có mốc giờ hợp lệ -> `None` (xuất `VALUE=DATE`)
    """
    if not isinstance(gio, str) or not gio.strip():
        return None
    moc = []
    for h_s, m_s in _GIO_RE.findall(gio):
        h, m = int(h_s), int(m_s)
        if 0 <= h < 24 and 0 <= m < 60:
            moc.append(h * 60 + m)
    if not moc:
        return None
    if "suất" in gio.casefold():
        return moc[0], moc[0] + 60, True
    if len(moc) >= 2 and moc[1] > moc[0]:
        return moc[0], moc[1], False
    thoi_luong = 60 if loai == "hoat_dong_toi" else 90
    return moc[0], moc[0] + thoi_luong, False


def thoat_ics(chuoi: Any) -> str:
    """RFC 5545 §3.3.11: thoát `\\`, `;`, `,` và xuống dòng."""
    s = str(chuoi or "").replace("\r\n", "\n").replace("\r", "\n")
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def gap_dong_75(dong: str) -> str:
    """RFC 5545 §3.1: mỗi dòng vật lý tối đa 75 byte UTF-8, dòng nối bắt đầu bằng một dấu cách."""
    ra: list[str] = []
    hien: list[str] = []
    dem = 0
    for ky in dong:
        n = len(ky.encode("utf-8"))
        if dem + n > 75:
            ra.append("".join(hien))
            hien = [" ", ky]
            dem = 1 + n
        else:
            hien.append(ky)
            dem += n
    ra.append("".join(hien))
    return "\r\n".join(ra)


def _fmt_local(ngay_iso: str, phut_tu_0h: int) -> str:
    d = dt.date.fromisoformat(ngay_iso)
    ngay_tinh = dt.datetime(d.year, d.month, d.day, 0, 0) + dt.timedelta(minutes=phut_tu_0h)
    return ngay_tinh.strftime("%Y%m%dT%H%M%S")


def _fmt_date(ngay_iso: str, cong_ngay: int = 0) -> str:
    d = dt.date.fromisoformat(ngay_iso) + dt.timedelta(days=cong_ngay)
    return d.strftime("%Y%m%d")


def _mo_ta(cac_dong: list[str | None]) -> str:
    return "\n".join(str(x).replace("**", "").strip() for x in cac_dong if x and str(x).strip())


def dung_ics(
    lich_hoac_chuan: dict,
    cau: dict[str, str] | None = None,
    *,
    dau_thoi_gian: dt.datetime | None = None,
    an_toan: str | None = None,
    sequence: int = 0,
) -> dict[str, Any]:
    """Dựng `.ics` v2 từ `CanonicalItinerary` hoặc `lich` thường. Trả `{ics, so_su_kien, so_ca_ngay, so_o_dau}`."""
    chuan = lich_hoac_chuan if lich_hoac_chuan.get("schema_version") == "1.0" else chuan_hoa_lich(
        lich_hoac_chuan, cau, an_toan=an_toan
    )
    ngay_ds = chuan.get("ngay") or []
    ts = chuan.get("tham_so") or {}
    if not ngay_ds or not ts.get("ngay_di") or not all(ng.get("ngay_thang") for ng in ngay_ds):
        raise ThieuNgayDiError("Lịch chưa có ngày đi — vui lòng chọn ngày đi để xuất tệp .ics.")

    an_toan_chu = an_toan if an_toan is not None else chuan.get("an_toan")
    an_toan_chu = str(an_toan_chu).strip() if an_toan_chu and str(an_toan_chu).strip() else None
    stamp_dt = (dau_thoi_gian or dt.datetime.now(dt.timezone.utc)).astimezone(dt.timezone.utc)
    stamp = stamp_dt.strftime("%Y%m%dT%H%M%SZ")
    ngay_dau = ngay_ds[0]["ngay_thang"]
    ngay_dau_vn = "/".join(reversed(ngay_dau.split("-")))

    dong = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Tro ly Hue//Len ke hoach v2//VI",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{thoat_ics(f'Lịch Huế {len(ngay_ds)} ngày từ {ngay_dau_vn}')}",
        f"X-WR-TIMEZONE:{TZID}",
        "BEGIN:VTIMEZONE",
        f"TZID:{TZID}",
        f"X-LIC-LOCATION:{TZID}",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0700",
        "TZOFFSETTO:+0700",
        "TZNAME:+07",
        "DTSTART:19700101T000000",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]

    so_su_kien = 0
    so_ca_ngay = 0
    so_o_dau = 0

    for ng in ngay_ds:
        ngay_iso = ng["ngay_thang"]
        for m in ng.get("muc") or []:
            if m.get("loai") not in _LOAI_SU_KIEN:
                continue
            gio_parsed = doc_gio_v2(m.get("gio"), str(m.get("loai")))
            cau_muc = m.get("cau") or (cau or {}).get(m.get("id_muc", ""))
            map_url = m.get("map_url")
            co_map = isinstance(map_url, str) and map_url.startswith(MAP_PREFIX)

            if gio_parsed is None:
                mo_ta = _mo_ta([an_toan_chu, m.get("ghi_chu"), cau_muc, NHAC_CA_NGAY, map_url if co_map else None])
                dong.extend([
                    "BEGIN:VEVENT",
                    f"UID:{ngay_dau}-{m['id_muc']}@tro-ly-hue",
                    f"SEQUENCE:{int(sequence)}",
                    f"DTSTAMP:{stamp}",
                    f"DTSTART;VALUE=DATE:{_fmt_date(ngay_iso)}",
                    f"DTEND;VALUE=DATE:{_fmt_date(ngay_iso, 1)}",
                    f"SUMMARY:{thoat_ics(m['ten'])}",
                    f"LOCATION:{thoat_ics(m['ten'] + ', Huế')}",
                    f"DESCRIPTION:{thoat_ics(mo_ta)}",
                    *([f"URL;VALUE=URI:{map_url}"] if co_map else []),
                    "END:VEVENT",
                ])
                so_ca_ngay += 1
            else:
                bd, kt, suat = gio_parsed
                mo_ta = _mo_ta([
                    an_toan_chu,
                    m.get("ghi_chu"),
                    cau_muc,
                    NHAC_GIO,
                    NHAC_SUAT if suat else None,
                    map_url if co_map else None,
                ])
                dong.extend([
                    "BEGIN:VEVENT",
                    f"UID:{ngay_dau}-{m['id_muc']}@tro-ly-hue",
                    f"SEQUENCE:{int(sequence)}",
                    f"DTSTAMP:{stamp}",
                    f"DTSTART;TZID={TZID}:{_fmt_local(ngay_iso, bd)}",
                    f"DTEND;TZID={TZID}:{_fmt_local(ngay_iso, kt)}",
                    f"SUMMARY:{thoat_ics(m['ten'])}",
                    f"LOCATION:{thoat_ics(m['ten'] + ', Huế')}",
                    f"DESCRIPTION:{thoat_ics(mo_ta)}",
                    *([f"URL;VALUE=URI:{map_url}"] if co_map else []),
                    "END:VEVENT",
                ])
            so_su_kien += 1

        # Bổ sung nhắc check-in ngày 1 & check-out ngày cuối nếu có `o_dau`
    o_dau = chuan.get("o_dau")
    if isinstance(o_dau, dict) and (o_dau.get("co_so") or []) and len(ngay_ds) >= 2:
        co_so = o_dau["co_so"]
        ds_ten = "; ".join(
            c["ten"] + (f" ({c['dia_chi']})" if c.get("dia_chi") else "")
            for c in co_so[:3] if c.get("ten")
        )
        ten_khu = o_dau.get("ten_khu") or "Huế"
        disclaimer = o_dau.get("nhan") or DISCLAIMER_O_DAU
        if "chưa kiểm giá, phòng trống" not in disclaimer:
            disclaimer = f"{disclaimer} ({DISCLAIMER_O_DAU})"
        dau_map = next((c.get("map_url") for c in co_so if isinstance(c.get("map_url"), str) and c["map_url"].startswith(MAP_PREFIX)), None)
        ten_dau = co_so[0].get("ten") or ten_khu

        for ma_su_kien, tieu_de, ngay_iso, bd, kt in (
            ("checkin", f"Nhận phòng gợi ý — {ten_dau}", ngay_ds[0]["ngay_thang"], 14 * 60, 15 * 60),
            ("checkout", f"Trả phòng gợi ý — {ten_dau}", ngay_ds[-1]["ngay_thang"], 11 * 60, 12 * 60),
        ):
            mo_ta = _mo_ta([
                an_toan_chu,
                f"Khu gợi ý: {ten_khu}.",
                f"Cơ sở tham khảo: {ds_ten}." if ds_ten else None,
                disclaimer,
            ])
            dong.extend([
                "BEGIN:VEVENT",
                f"UID:{ngay_dau}-{ma_su_kien}@tro-ly-hue",
                f"SEQUENCE:{int(sequence)}",
                f"DTSTAMP:{stamp}",
                f"DTSTART;TZID={TZID}:{_fmt_local(ngay_iso, bd)}",
                f"DTEND;TZID={TZID}:{_fmt_local(ngay_iso, kt)}",
                f"SUMMARY:{thoat_ics(tieu_de)}",
                f"LOCATION:{thoat_ics(f'{ten_khu}, Huế')}",
                f"DESCRIPTION:{thoat_ics(mo_ta)}",
                *([f"URL;VALUE=URI:{dau_map}"] if dau_map else []),
                "END:VEVENT",
            ])
            so_su_kien += 1
            so_o_dau += 1

    dong.append("END:VCALENDAR")
    ics = "\r\n".join(gap_dong_75(line) for line in dong) + "\r\n"
    return {"ics": ics, "so_su_kien": so_su_kien, "so_ca_ngay": so_ca_ngay, "so_o_dau": so_o_dau}
