"""Quán ăn gợi ý trong lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-quan-trong-lich-plan.md`, cờ `quan_lich`).

Mọi thứ do code: mỗi ngày, bữa trưa gần điểm cuối buổi sáng (không có sáng ⇒ điểm đầu buổi chiều), bữa tối gần điểm buổi tối (không có ⇒
điểm cuối buổi chiều);
≤ 2 quán CÙNG CỤM với điểm đó và ≤ 2 km tới điểm, quán ăn trước cà phê, trong cùng loại quán kho trước rồi tới nguồn chưa kiểm, gần điểm nhất,
không lặp quán trong cả chuyến.
Model không chọn, không thấy tên quán (khối này không vào tin nhắn gửi model; an toàn này dựa cả vào `nho_cau_tra_loi: false` — bật nhớ câu trả
lời thì chữ lịch, kể cả tên quán OSM, sẽ vào lịch sử gửi model ⇒ xem lại trước khi bật, review B m-2). Không giờ / giá / điện thoại (nguồn mở không có ngày kiểm).
Bảng: `data/phase_9/lich_trinh/bang_quan_lich_v1.json` (quán kho + dữ liệu mở thành phố + OpenStreetMap; dựng bằng script, private).
Cụm thiếu quán ⇒ không có dòng (không đoán, không lấy cụm khác).
"""
import json
import math
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

MAP_BASE = "https://www.google.com/maps/search/?api=1&query="  # link do code dựng từ toạ độ, chỉ mở khi người dùng bấm
LOAI = {"quan_an": "quán ăn", "ca_phe": "cà phê"}
NHAN = {"du_lieu_mo": "dữ liệu mở của thành phố, chưa kiểm", "osm": "từ bản đồ mở, chưa kiểm"}  # kho ⇒ không nhãn (có bài để đọc)
NGUON = ("kho", "du_lieu_mo", "osm")
SO_QUAN = 2
# "gần" = ≤ 2 km đường chim bay tới điểm: mô phỏng đầu (không giới hạn) có p95 9,3 km (cùng cụm nhưng cụm rộng — phá, biển, lăng xa) ⇒ dòng "ăn gần X"
# sai nghĩa. Điểm không có toạ độ ⇒ không kiểm được ⇒ không dòng.
KM_TOI_DA = 2.0
TEN_TOI_DA = 80
# tên từ nguồn mở là dữ liệu người khác viết: chặn ký tự điều khiển / ký tự định dạng vô hình (Cf: đảo chiều U+202E, U+200B…) / link / thẻ / cú pháp
# link Markdown (review B m-1)
# Ảnh quán ngoài kho (C 14/11 tối): tên file tự host dưới `frontend/public/anh/quan/` (quán kho dùng ảnh Khám phá theo mã bài ở giao diện).
_ANH = re.compile(r"quan/[a-z0-9_]{1,40}")
_BAN = re.compile(r"[\x00-\x1f\x7f]|https?:|www\.|//|\]\(|[<>]")


def _ten_sach(ten: str) -> bool:
    return not _BAN.search(ten) and not any(unicodedata.category(ch) == "Cf" for ch in ten)


def nap_bang_quan(path: str | Path, cum_diem) -> dict:
    """Lúc khởi động (cờ `quan_lich`): mỗi quán đủ tên (≤ 80 ký tự, không ký tự điều khiển / link), loại đã biết, cụm có trong bảng điểm,
    toạ độ hai số, nguồn đã biết (kho ⇒ mã bài; osm ⇒ link openstreetmap). Sai một dòng ⇒ không khởi động. Trả `{cum: [quán…]}`."""
    rows = json.loads(Path(path).read_text(encoding="utf-8"))["quan"]
    theo_cum: dict[str, list[dict]] = {}
    for q in rows:
        ten = q.get("ten")
        ok = (isinstance(ten, str) and 0 < len(ten.strip()) <= TEN_TOI_DA and _ten_sach(ten) and q.get("loai") in LOAI
              and q.get("cum") in cum_diem and q.get("nguon") in NGUON and isinstance(q.get("toa"), list) and len(q["toa"]) == 2
              and all(isinstance(x, (int, float)) for x in q["toa"])
              and (q["nguon"] != "kho" or isinstance(q.get("bai_id"), str))
              and (q["nguon"] != "osm" or str(q.get("link", "")).startswith("https://www.openstreetmap.org/"))
              and (q.get("anh") is None or (q["nguon"] != "kho" and isinstance(q["anh"], str) and _ANH.fullmatch(q["anh"]))))
        if not ok:
            raise ValueError(f"bảng quán lịch: dòng không hợp lệ ({str(ten)[:40]!r})")
        theo_cum.setdefault(q["cum"], []).append(q)
    return theo_cum


def _km(a, b) -> float:
    """Khoảng cách theo đường chim bay (km) — chỉ để xếp quán gần trước, không in ra."""
    dlat, dlon = math.radians(b[0] - a[0]), math.radians(b[1] - a[1])
    h = math.sin(dlat / 2) ** 2 + math.cos(math.radians(a[0])) * math.cos(math.radians(b[0])) * math.sin(dlon / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def _chon(ds: list[dict], toa_diem, da_dung: set) -> list[dict]:
    # chỉ quán ≤ KM_TOI_DA; bữa chính ⇒ chỉ quán ăn, cà phê chỉ khi không có quán ăn nào (A 14/11: bữa tối từng gợi ý một quán cà phê có bài kho
    # trước quán ăn OSM); trong cùng loại: quán kho trước, rồi gần điểm nhất
    gan = [(q, _km(toa_diem, q["toa"])) for q in ds if (q["ten"], tuple(q["toa"])) not in da_dung]
    gan = [(q, km) for q, km in gan if km <= KM_TOI_DA]
    xep = [q for q, km in sorted(gan, key=lambda x: (x[0]["loai"] != "quan_an", NGUON.index(x[0]["nguon"]), x[1]))]
    an = [q for q in xep if q["loai"] == "quan_an"]
    return (an or xep)[:SO_QUAN]  # có quán ăn ⇒ chỉ quán ăn (1–2); không có quán ăn nào trong 2 km ⇒ mới gợi ý cà phê


def _hien(q: dict) -> dict:
    return {"ten": q["ten"], "loai": LOAI[q["loai"]], "nhan": NHAN.get(q["nguon"]), "bai_id": q.get("bai_id"),
            "anh": q.get("anh"), "map_url": MAP_BASE + quote(f"{q['toa'][0]},{q['toa'][1]}")}


def an_uong(theo_cum: dict, bang, khung: dict, toa_do: dict | None) -> list[dict]:
    """`[{ngay, bua: "trua" | "toi", gan: tên điểm, quan: [...]}]` theo khung của bộ xếp; bữa không có quán cùng cụm ⇒ không có mục."""
    da_dung: set = set()
    ra = []
    for ng in khung["ngay"]:
        sang, chieu = ng["buoi"].get("sang", []), ng["buoi"].get("chieu", [])
        toi = [j for j in ng["buoi"].get("toi", []) if j in bang.theo_id]  # có điểm buổi tối ⇒ ăn tối gần đó (người đi đã ở đó)
        for bua, diem in (("trua", sang[-1] if sang else (chieu[0] if chieu else None)), ("toi", toi[0] if toi else (chieu[-1] if chieu else None))):
            if diem is None:
                continue
            d = bang.theo_id[diem]
            toa = (toa_do or {}).get(diem)
            chon = _chon(theo_cum.get(d["cum"], []), toa, da_dung) if toa else []
            if chon:
                da_dung |= {(q["ten"], tuple(q["toa"])) for q in chon}
                ra.append({"ngay": ng["ngay"], "bua": bua, "gan": d["ten"], "quan": [_hien(q) for q in chon]})
    return ra


def dong_chu(an: list[dict]) -> list[str]:
    """Khối chữ thuần cho `ghep_chu` (nút chép / tải, lịch sử chat)."""
    if not an:
        return []
    dong = ["", "**Ăn uống gợi ý (gần điểm tham quan)**"]
    for a in an:
        ds = " · ".join(q["ten"] + (f" ({q['nhan']})" if q["nhan"] else "") for q in a["quan"])
        dong.append(f"- Ngày {a['ngay']}, ăn {'trưa' if a['bua'] == 'trua' else 'tối'} gần {a['gan']}: {ds}")
    dong.append("Gợi ý theo vị trí — chưa kiểm giờ mở cửa, giá; quán có thể đã đổi.")
    return dong
