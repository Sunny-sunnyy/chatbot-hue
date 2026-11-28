"""Kiểm thử Đợt 5 Phần A — CanonicalItinerary, `.ics` v2 (validator RFC 5545 chặt), Deep Link OTA 3 sàn + Mẫu hỏi phòng (0 USD)."""
import copy
import datetime as dt
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.conversations import ConversationStore
from api.hanh_trinh_chuan import chuan_hoa_lich, tu_luu_chuan
from api.lich_ics import ThieuNgayDiError, doc_gio_v2, dung_ics, thoat_ics
from api.routes.cong import router as cong_router
from api.routes.xuat import router as xuat_router
from core.settings_loader import load_settings
from llm import lich_trinh_v2 as lt2
from llm import luu_tru_lich as ltl
from llm import sua_lich_v2 as sl
from llm import thoi_tiet as tt
from llm.assistant import AssistantFlags

MAP_PREFIX = "https://www.google.com/maps/search/"


def _unfold_ics(ics_text: str) -> list[str]:
    """Kiểm tra xuống dòng CRLF, giới hạn 75 byte UTF-8 mỗi dòng vật lý, và mở gấp dòng chuẩn RFC 5545 §3.1."""
    assert ics_text.endswith("\r\n"), "Tệp .ics phải kết thúc bằng CRLF"
    raw_lines = ics_text.split("\r\n")[:-1]
    assert raw_lines, "Tệp .ics rỗng"
    for i, line in enumerate(raw_lines):
        assert "\n" not in line and "\r" not in line, f"Dòng {i + 1} chứa LF/CR trần"
        nbytes = len(line.encode("utf-8"))
        assert nbytes <= 75, f"Dòng {i + 1} vượt 75 byte UTF-8 ({nbytes} bytes): {line!r}"
    unfolded: list[str] = []
    for line in raw_lines:
        if line.startswith((" ", "\t")):
            assert unfolded, "Dòng nối nằm đầu tệp"
            unfolded[-1] += line[1:]
        else:
            unfolded.append(line)
    return unfolded


def _validate_rfc5545(ics_text: str) -> list[dict[str, str]]:
    """Validator RFC 5545 chặt (dùng thay `icalendar` khi môi trường không tải được gói ngoài). Trả danh sách VEVENT dict."""
    lines = _unfold_ics(ics_text)
    assert lines[0] == "BEGIN:VCALENDAR" and lines[-1] == "END:VCALENDAR"
    assert "VERSION:2.0" in lines and "CALSCALE:GREGORIAN" in lines
    assert any(l == "BEGIN:VTIMEZONE" for l in lines) and any(l == "TZID:Asia/Ho_Chi_Minh" for l in lines)
    assert any(l == "END:VTIMEZONE" for l in lines)

    events: list[dict[str, str]] = []
    cur: dict[str, str] | None = None
    in_tz = False
    for line in lines:
        if line == "BEGIN:VTIMEZONE":
            in_tz = True
            continue
        if line == "END:VTIMEZONE":
            in_tz = False
            continue
        if in_tz:
            continue
        if line == "BEGIN:VEVENT":
            assert cur is None, "VEVENT lồng nhau"
            cur = {}
            continue
        if line == "END:VEVENT":
            assert cur is not None
            for req in ("UID", "DTSTAMP", "DTSTART", "SUMMARY"):
                assert any(k == req or k.startswith(req + ";") for k in cur), f"VEVENT thiếu {req}: {cur}"
            events.append(cur)
            cur = None
            continue
        if cur is not None:
            assert ":" in line, f"Thuộc tính VEVENT không hợp lệ: {line!r}"
            key, val = line.split(":", 1)
            assert key not in cur, f"Trùng thuộc tính {key} trong VEVENT"
            cur[key] = val

    assert cur is None, "Thiếu END:VEVENT"
    uids = [e["UID"] for e in events]
    assert len(uids) == len(set(uids)), "Trùng UID giữa các sự kiện"
    return events


def _lich_mau_v2(ngay_di: str | None = "2026-12-10") -> dict:
    return {
        "phien_ban": 2,
        "tham_so": {"so_ngay": 2, "nguoi_lon": 2, "tre_em": 1, "lon_tuoi": True, "kieu_di": "nhe_nhang", "ngay_di": ngay_di},
        "minh_hieu": "Mình hiểu: 2 ngày · 2 người lớn · 1 trẻ em · có người lớn tuổi — sai thì bấm **Sửa**.",
        "ngay": [
            {
                "ngay": 1,
                "ngay_thang": ngay_di,
                "thu": 3 if ngay_di else None,
                "chang": ["Kinh thành"],
                "muc": [
                    {
                        "id_muc": "n1-sang-1", "buoi": "sang", "loai": "tham_quan", "id_diem": "dai_noi",
                        "ten": "Đại Nội Huế", "gio": "8:00 – 10:30", "ghi_chu": None,
                        "map_url": MAP_PREFIX + "?api=1&query=Dai+Noi+Hue",
                        "anh": {"src": "/anh/lich/dai_noi.jpg", "tac_gia": "Bị bỏ", "giay_phep": "CC BY"},
                    },
                    {
                        "id_muc": "n1-chieu-1", "buoi": "chieu", "loai": "tham_quan", "id_diem": "thien_mu",
                        "ten": "Chùa Thiên Mụ", "gio": "14:00", "ghi_chu": None,
                        "map_url": MAP_PREFIX + "?api=1&query=Chua+Thien+Mu",
                        "anh": {"src": "/anh/lich/../../secret.jpg"},
                    },
                    {
                        "id_muc": "n1-toi-1", "buoi": "toi", "loai": "hoat_dong_toi", "id_diem": "pho_di_bo",
                        "ten": "Phố đi bộ Nguyễn Đình Chiểu", "gio": None, "ghi_chu": "Mở buổi tối ven sông",
                        "map_url": MAP_PREFIX + "?api=1&query=Pho+di+bo+Hue",
                        "anh": None,
                    },
                ],
            },
            {
                "ngay": 2,
                "ngay_thang": "2026-12-11" if ngay_di else None,
                "thu": 4 if ngay_di else None,
                "chang": ["Thủy Xuân"],
                "muc": [
                    {
                        "id_muc": "n2-toi-1", "buoi": "toi", "loai": "nghi", "id_diem": None,
                        "ten": "Tối nghỉ tại khách sạn", "gio": None, "map_url": None, "anh": None,
                    }
                ],
            },
        ],
        "an": [{"ngay": 1, "bua": "trua", "gan": "Đại Nội Huế", "quan": [{"ten": "Cơm Hến Bà Cam", "loai": "Quán", "map_url": MAP_PREFIX + "?api=1&query=Com+Hen"}]}],
        "o_dau": {
            "khu": "loi_do_thi_hai_bo_song_huong",
            "ten_khu": "trung tâm, hai bờ sông Hương",
            "ly_do": "Gần dịch vụ.",
            "co_so": [
                {
                    "ten": "Huế Heritage Hotel & Spa", "xep_hang": "4 sao", "dia_chi": "12 Lê Lợi, Huế",
                    "map_url": MAP_PREFIX + "?api=1&query=Hue+Heritage",
                    "link": ltl.LINK_TIM + "Hue",
                    "anh": "/anh/khach_san/ks1.jpg",
                }
            ],
            "nhan": ltl.NHAN,
            "nguon": "Cục DL",
        },
        "ghi_chu": [{"ma": "han_che", "cau": "Đi nhẹ nhàng."}, {"ma": "du_bao", "cau": "Mưa 80%."}],
    }


def test_canonical_itinerary_normalizes_hash_and_filters_unsafe_paths():
    cau = {"n1-sang-1": "Hoàng thành triều Nguyễn [1].", "n1-chieu-1": "Ngôi chùa cổ bên sông Hương [Nguồn 2]."}
    c1 = chuan_hoa_lich(_lich_mau_v2(), cau, an_toan=tt.CAU_BAO_LU)
    c2 = chuan_hoa_lich(_lich_mau_v2(), cau, an_toan=tt.CAU_BAO_LU)
    assert c1["schema_version"] == "1.0"
    assert c1["itinerary_hash"] == c2["itinerary_hash"] and len(c1["itinerary_hash"]) == 16
    assert c1["an_toan"] == tt.CAU_BAO_LU
    # Chặn ảnh có `..` và bỏ thông tin ghi công tác giả/giấy phép
    m_sang, m_chieu = c1["ngay"][0]["muc"][0], c1["ngay"][0]["muc"][1]
    assert m_sang["anh"] == {"src": "/anh/lich/dai_noi.jpg"} and m_sang["cau"] == "Hoàng thành triều Nguyễn."
    assert m_chieu["anh"] is None and m_chieu["cau"] == "Ngôi chùa cổ bên sông Hương."
    assert "tac_gia" not in str(c1) and "giay_phep" not in str(c1)
    assert c1["anh_manifest"] == {"diem": {"dai_noi": "/anh/lich/dai_noi.jpg"}, "khach_san": {"Huế Heritage Hotel & Spa": "/anh/khach_san/ks1.jpg"}}
    assert all(g["ma"] != "du_bao" for g in c1["ghi_chu"])


def test_ics_v2_rfc5545_single_time_all_day_lodging_and_safety():
    cau = {"n1-sang-1": "Hoàng thành triều Nguyễn [1]."}
    kq = dung_ics(_lich_mau_v2(), cau, dau_thoi_gian=dt.datetime(2026, 11, 28, 3, 0, tzinfo=dt.timezone.utc), an_toan=tt.CAU_BAO_LU)
    # 3 mục ngày 1 (2 mốc giờ, 1 mốc giờ +90p, 0 giờ all-day) + check-in + check-out = 5 sự kiện (mục nghi bỏ qua)
    assert kq["so_su_kien"] == 5 and kq["so_ca_ngay"] == 1 and kq["so_o_dau"] == 2
    events = _validate_rfc5545(kq["ics"])
    assert len(events) == 5

    # 1. Mục 2 mốc giờ dùng TZID=Asia/Ho_Chi_Minh
    e0 = events[0]
    assert e0["DTSTART;TZID=Asia/Ho_Chi_Minh"] == "20261210T080000"
    assert e0["DTEND;TZID=Asia/Ho_Chi_Minh"] == "20261210T103000"
    assert e0["SEQUENCE"] == "0"
    assert e0["URL;VALUE=URI"].startswith(MAP_PREFIX)
    assert e0["DESCRIPTION"].startswith(thoat_ics(tt.CAU_BAO_LU))

    # 2. Mục 1 mốc giờ (14:00) mặc định +90 phút cho tham_quan
    e1 = events[1]
    assert e1["DTSTART;TZID=Asia/Ho_Chi_Minh"] == "20261210T140000"
    assert e1["DTEND;TZID=Asia/Ho_Chi_Minh"] == "20261210T153000"

    # 3. Mục không giờ xuất VALUE=DATE (all-day, DTEND là ngày hôm sau)
    e2 = events[2]
    assert e2["DTSTART;VALUE=DATE"] == "20261210"
    assert e2["DTEND;VALUE=DATE"] == "20261211"

    # 4 & 5. Check-in ngày 1 (14:00-15:00) & check-out ngày cuối (11:00-12:00) kèm disclaimer
    ci, co = events[3], events[4]
    assert ci["DTSTART;TZID=Asia/Ho_Chi_Minh"] == "20261210T140000" and ci["DTEND;TZID=Asia/Ho_Chi_Minh"] == "20261210T150000"
    assert co["DTSTART;TZID=Asia/Ho_Chi_Minh"] == "20261211T110000" and co["DTEND;TZID=Asia/Ho_Chi_Minh"] == "20261211T120000"
    assert "chưa kiểm giá\\, phòng trống" in ci["DESCRIPTION"] and "chưa kiểm giá\\, phòng trống" in co["DESCRIPTION"]
    assert ci["DESCRIPTION"].startswith(thoat_ics(tt.CAU_BAO_LU))

    # 6. Mục buổi tối 1 mốc giờ mặc định 60 phút
    assert doc_gio_v2("19:30", "hoat_dong_toi") == (19 * 60 + 30, 20 * 60 + 30, False)


def test_ics_v2_blocks_missing_ngay_di_without_guessing():
    with pytest.raises(ThieuNgayDiError):
        dung_ics(_lich_mau_v2(ngay_di=None), {})


def test_ics_route_respects_flag_and_blocks_missing_date():
    s = copy.deepcopy(load_settings(validate_private_paths=False))
    flags_off = AssistantFlags.from_settings(s)
    assert flags_off.xuat_nang_cao is False

    app = FastAPI()
    app.include_router(xuat_router)
    app.include_router(cong_router)
    store = ConversationStore(len)
    app.state.conversations = store
    app.state.assistant_flags = flags_off
    client = TestClient(app)

    cid = store.ensure(None)
    khung_khong_ngay = lt2.xep_v2(flags_off.bang_lich_v2, lt2.tu_truong({"so_ngay": "2", "nguoi_lon": 2, "ngan_sach": "vua"}))
    store.luu_lich(cid, sl.luu_tu_lich(khung_khong_ngay, None, None))
    # Cờ tắt ⇒ 404 và /api/tinh_nang không có khoá mới
    assert client.get("/api/lich/ics", cookies={"conversation_id": cid}).status_code == 404
    tn_off = client.get("/api/tinh_nang").json()
    assert "xuat_nang_cao" not in tn_off and "slide_designer" not in tn_off

    # Bật cờ xuat_nang_cao
    s["assistant"]["xuat_nang_cao"] = True
    app.state.assistant_flags = AssistantFlags.from_settings(s)
    assert client.get("/api/tinh_nang").json()["xuat_nang_cao"] is True
    # Không có ngày đi ⇒ 400 rõ ràng, không đoán ngày
    r_err = client.get("/api/lich/ics", cookies={"conversation_id": cid})
    assert r_err.status_code == 400 and r_err.json()["error"]["code"] == "thieu_ngay_di"

    # Có ngày đi ⇒ 200 hợp lệ RFC 5545
    khung_co_ngay = lt2.xep_v2(flags_off.bang_lich_v2, lt2.tu_truong({"so_ngay": "2", "nguoi_lon": 2, "ngan_sach": "vua"}),
                               ngay_bat_dau=dt.date(2026, 12, 10))
    store.luu_lich(cid, sl.luu_tu_lich(khung_co_ngay, "2026-12-10", None))
    r_ok = client.get("/api/lich/ics", cookies={"conversation_id": cid})
    assert r_ok.status_code == 200 and r_ok.headers["content-type"].startswith("text/calendar")
    events = _validate_rfc5545(r_ok.text)
    assert any("Nhận phòng gợi ý" in e["SUMMARY"] for e in events)


def test_ota_deep_links_and_inquiry_template_two_sided_guardrail():
    # Phía 1: Chặn ca xấu (URL injection, .., javascript:, host lạ, ký tự điều khiển \r\n\0)
    assert ltl.kiem_tra_ota_url("javascript:alert(1)") is None
    assert ltl.kiem_tra_ota_url("http://www.booking.com/hotel.html") is None
    assert ltl.kiem_tra_ota_url("https://evil.example.com/search?q=hue") is None
    assert ltl.kiem_tra_ota_url("https://www.agoda.com/../../etc/passwd") is None
    assert ltl.kiem_tra_ota_url("https://www.agoda.com/search?q=a%2F..%2Fb") is None
    assert ltl.kiem_tra_ota_url("https://www.booking.com/x\r\nSet-Cookie:a=b") is None

    evil_name = "Hotel X &admin=1 /path?x=2 ../evil %2F\r\nX-Inject: 1"
    links = ltl.tao_deep_links_co_so(
        evil_name, ngay_di="2026-12-10", so_ngay=3, nguoi_lon=3, tre_em=1,
        anh_trang="https://www.agoda.com/../../evil",
    )
    assert set(links) == {"booking", "agoda", "traveloka"}
    for host_key, url in links.items():
        assert ltl.kiem_tra_ota_url(url) == url
        p = urlparse(url)
        assert p.scheme == "https" and p.netloc in ltl.ALLOWED_OTA_HOSTS
        qs = parse_qs(p.query)
        assert "admin" not in qs and "x" not in qs, f"Tham số giả lọt vào {host_key}: {qs}"
        assert "\r" not in url and "\n" not in url and "\0" not in url
        assert ".." not in url
        assert ltl.link_phong_hop_le(url) == url

    # Wrapper hợp đồng tao_deep_links(ten, tham_so) & o_dau(..., tham_so=...)
    dl_wrap = ltl.tao_deep_links("Huế Heritage Hotel & Spa", {"ngay_di": "2026-12-10", "so_ngay": 3, "nguoi_lon": 2, "tre_em": 1})
    assert set(dl_wrap) == {"booking", "agoda", "traveloka"} and all(ltl.link_phong_hop_le(u) == u for u in dl_wrap.values())
    s_cfg = load_settings(validate_private_paths=False)
    bang_lt = ltl.nap_bang_luu_tru(
        Path(__file__).resolve().parents[1] / s_cfg["assistant"]["lich_trinh_bang_luu_tru"],
        AssistantFlags.from_settings(s_cfg).bang_lich_v2.cum,
    )
    cums = [k for k in bang_lt["cum_ve_khu"] if k not in ltl.CUM_DI_TRONG_NGAY][:2]
    od = ltl.o_dau(bang_lt, cums, 3, False, tham_so={"ngay_di": "2026-12-10", "so_ngay": 3, "nguoi_lon": 2})
    assert od and all("deep_links" in c and "mau_hoi_phong" in c for c in od["co_so"])

    # Phía 2: Không chặn oan tên hợp lệ có &, /, dấu tiếng Việt
    for ten_hop_le in ("Huế Heritage Hotel & Spa", "Nhà nghỉ Sông Hương / 12 Lê Lợi", "Bún Bò Huế - O Phượng"):
        dl = ltl.tao_deep_links_co_so(ten_hop_le, ngay_di="2026-12-10", so_ngay=3, nguoi_lon=2, tre_em=1)
        assert all(ltl.kiem_tra_ota_url(u) == u for u in dl.values())
        qs_b = parse_qs(urlparse(dl["booking"]).query)
        qs_t = parse_qs(urlparse(dl["traveloka"]).query)
        assert qs_b["ss"][0] == f"{ten_hop_le}, Huế"
        assert qs_b["checkin"][0] == "2026-12-10" and qs_b["checkout"][0] == "2026-12-12"
        assert qs_b["group_adults"][0] == "2" and qs_b["group_children"][0] == "1" and qs_b["no_rooms"][0] == "1"
        assert qs_t["q"][0] == f"{ten_hop_le} Huế" and qs_t["checkin"][0] == "2026-12-10" and qs_t["adults"][0] == "2"

    # Mẫu tin nhắn hỏi phòng đủ 6 trường, giữ yêu cầu người lớn tuổi/trẻ em, không bịa giá/email
    mau = ltl.tao_mau_hoi_phong(
        "Huế Heritage Hotel & Spa", dia_chi="12 Lê Lợi, Huế", ngay_di="2026-12-10", so_ngay=3,
        nguoi_lon=2, tre_em=1, lon_tuoi=True,
    )
    for truong in ("Huế Heritage Hotel & Spa", "10/12/2026", "12/12/2026", "2 đêm", "2 người lớn, 1 trẻ em, có người lớn tuổi",
                   "người lớn tuổi", "trẻ em", "phòng trống", "tổng giá"):
        assert truong in mau
    assert "@" not in mau and not re.search(r"\d[\d.,]*\s*(?:đồng|vnd|vnđ)", mau, re.IGNORECASE)
