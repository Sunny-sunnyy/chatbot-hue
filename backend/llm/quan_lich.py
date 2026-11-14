"""Quán ăn gợi ý trong lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-quan-trong-lich-plan.md`, cờ `quan_lich`).

Mọi thứ do code: mỗi ngày, bữa trưa gần điểm cuối buổi sáng (không có sáng ⇒ điểm đầu buổi chiều), bữa tối gần điểm buổi tối (không có ⇒
điểm cuối buổi chiều);
≤ 2 quán CÙNG CỤM với điểm đó và ≤ 2 km tới điểm, quán kho trước rồi tới nguồn chưa kiểm, gần điểm nhất, không lặp quán trong cả chuyến.
Model không chọn, không thấy tên quán (khối này không vào tin nhắn gửi model). Không giờ / giá / điện thoại (nguồn mở không có ngày kiểm).
Bảng: `data/phase_9/lich_trinh/bang_quan_lich_v1.json` (quán kho + dữ liệu mở thành phố + OpenStreetMap; dựng bằng script, private).
Cụm thiếu quán ⇒ không có dòng (không đoán, không lấy cụm khác).
"""
import json
import math
import re
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
_BAN = re.compile(r"[\x00-\x1f\x7f]|https?:|www\.|[<>]")  # tên từ nguồn mở là dữ liệu người khác viết: chặn ký tự điều khiển / link / thẻ


def nap_bang_quan(path: str | Path, cum_diem) -> dict:
    """Lúc khởi động (cờ `quan_lich`): mỗi quán đủ tên (≤ 80 ký tự, không ký tự điều khiển / link), loại đã biết, cụm có trong bảng điểm,
    toạ độ hai số, nguồn đã biết (kho ⇒ mã bài; osm ⇒ link openstreetmap). Sai một dòng ⇒ không khởi động. Trả `{cum: [quán…]}`."""
    rows = json.loads(Path(path).read_text(encoding="utf-8"))["quan"]
    theo_cum: dict[str, list[dict]] = {}
    for q in rows:
        ten = q.get("ten")
        ok = (isinstance(ten, str) and 0 < len(ten.strip()) <= TEN_TOI_DA and not _BAN.search(ten) and q.get("loai") in LOAI
              and q.get("cum") in cum_diem and q.get("nguon") in NGUON and isinstance(q.get("toa"), list) and len(q["toa"]) == 2
              and all(isinstance(x, (int, float)) for x in q["toa"])
              and (q["nguon"] != "kho" or isinstance(q.get("bai_id"), str))
              and (q["nguon"] != "osm" or str(q.get("link", "")).startswith("https://www.openstreetmap.org/")))
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
    # chỉ quán ≤ KM_TOI_DA; quán kho trước; bữa ăn ⇒ quán ăn trước cà phê; rồi gần điểm nhất
    gan = [(q, _km(toa_diem, q["toa"])) for q in ds if (q["ten"], tuple(q["toa"])) not in da_dung]
    gan = [(q, km) for q, km in gan if km <= KM_TOI_DA]
    return [q for q, km in sorted(gan, key=lambda x: (NGUON.index(x[0]["nguon"]), x[0]["loai"] != "quan_an", x[1]))][:SO_QUAN]


def _hien(q: dict) -> dict:
    return {"ten": q["ten"], "loai": LOAI[q["loai"]], "nhan": NHAN.get(q["nguon"]), "bai_id": q.get("bai_id"),
            "map_url": MAP_BASE + quote(f"{q['toa'][0]},{q['toa'][1]}")}


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
