"""Bộ xếp lịch "Lên kế hoạch" bản 2 — bước (b) của plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md` (spec bản 3.3 §5b, §5c.1,
§5c.3, §5c.4). Code thuần, không mạng, không model. Bộ xếp cũ (`lich_trinh.xep`) giữ nguyên cho đường câu tự do và khi cờ `len_ke_hoach_v2` tắt.

Luật (thứ tự ưu tiên khi kéo ngược nhau, spec 5b — luật thấp chỉ chọn trong phần luật cao còn cho phép):
1. nhóm hạn chế (có trẻ em / người lớn tuổi): 1 điểm mỗi buổi, tránh điểm nhiều bậc thang khi cùng cụm có điểm thay;
2. (bước d / e: thứ, mùa, giờ mở cửa);
3. cụm: ≤ 2 cụm kề một ngày tính trên mọi điểm sáng + chiều; cụm xa cả ngày, chỉ khi lịch ≥ 3 ngày và **không ở ngày 1**;
4. điểm ưu tiên của sở thích (cột `uu_tien_theo_so_thich` của bảng, thứ tự 1–4) đứng đầu thứ tự xét;
6. sở thích (≤ 2, xen kẽ A1, B1, A2, B2…); không chọn ⇒ nhóm "chung" + một điểm thiên nhiên mỗi ngày (luật cũ);
7. kiểu đi: số điểm mỗi buổi tính bằng phút (nhẹ nhàng 1 điểm; cân bằng quỹ 210; khám phá nhiều quỹ 240; tối đa 2 điểm / buổi).
Số người lớn không vào bộ xếp (spec 3.1: ngoại lệ có chủ ý của N1). Buổi tối xếp ở bước (e), sau khi khung tham quan chốt.
"""
import datetime as dt
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from llm import luu_tru_lich as ltl

from llm.citations import CITATION_PATTERN
from llm.lich_trinh import BUOI, CAU_CO_THE_DOI, CAU_KHONG_XEP, CUM_KE, CUM_XA, LOAI_DIEM, MAP_BASE, TIEU_DE_GHI_CHU, _cum_hop, chuan_ten
from llm.so_tien import tim_so_tien

BUOI_NGAY = ("sang", "chieu")
PHUT = {"ngan": 75, "nua_buoi": 150}  # 5c.3: phút tham quan
DI_CUNG_CUM, DI_CUM_KE = 15, 30  # 5c.3: phút đi giữa hai điểm trong một buổi
QUY = {"nhe_nhang": None, "can_bang": 210, "kham_pha": 240}  # None = đúng 1 điểm / buổi
KIEU_DI_MAC_DINH = "can_bang"
TOI_DA_BUOI = 2
SO_NGAY_TOI_DA = 5
NGUONG_LOAI = 4  # spec §8 câu 4: loại có < 4 điểm trong bảng ⇒ ô sở thích đó không hiện
TRONG_NHA = {"trong_nha", "ngoai_troi", "ca_hai"}
COT_V8 = {"thoi_luong", "trong_nha", "bac_thang", "uu_tien"}  # 5c.1: thiếu ⇒ không khởi động khi cờ bật


@dataclass(frozen=True)
class BangV2:
    diem: tuple[dict, ...]
    theo_id: dict
    cum: dict
    uu_tien: dict  # sở thích | "chung" ⇒ danh sách id theo thứ tự 1–4
    loai_hien: tuple[str, ...]  # sở thích đủ điểm để hiện trên biểu mẫu (thứ tự như `LOAI_DIEM_THU_TU`)
    nhac_mua_chung: dict | None


LOAI_DIEM_THU_TU = ("di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh")


def nap_bang_v2(path: str | Path) -> BangV2:
    """Đọc + kiểm bảng v8 lúc khởi động: cột bắt buộc của bảng cũ + cột v8 (5c.1); `thoi_luong` không còn rỗng; danh sách ưu tiên chỉ trỏ tới
    điểm có trong bảng và hợp sở thích. Sai ⇒ `ValueError` (server không khởi động khi cờ bật — bài học 10/11: thiếu file ⇒ tính năng tắt im lặng)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cum, diem = data["cum"], data["diem"]
    theo_id = {}
    for d in diem:
        missing = ({"id", "ten", "cum", "loai", "gio_mo_cua", "nguon", "buoi", "quan_the", "luu_y", "ten_khac"} | COT_V8) - set(d)
        if missing:
            raise ValueError(f"bảng điểm v2: {d.get('id')} thiếu {sorted(missing)}")
        if d["id"] in theo_id or d["cum"] not in cum or not d["loai"] or not set(d["loai"]) <= LOAI_DIEM or d["thoi_luong"] not in PHUT \
                or d["trong_nha"] not in TRONG_NHA or d["bac_thang"] not in ("nhieu", None) or not d["buoi"] or not set(d["buoi"]) <= set(BUOI):
            raise ValueError(f"bảng điểm v2: {d['id']} sai giá trị")
        if d.get("doan_mo_ta") is not None and not (isinstance(d["doan_mo_ta"], str) and d["doan_mo_ta"].startswith(d["nguon"] + "#")):
            raise ValueError(f"bảng điểm v2: {d['id']} doan_mo_ta phải là chunk_id của chính file nguồn ({d['nguon']}#<số>)")
        theo_id[d["id"]] = d
    uu_tien = data["uu_tien_theo_so_thich"]
    for khoa, ids in uu_tien.items():
        if khoa != "chung" and khoa not in LOAI_DIEM:
            raise ValueError(f"bảng điểm v2: ưu tiên của sở thích lạ {khoa}")
        for id_ in ids:
            if id_ not in theo_id or (khoa != "chung" and khoa not in theo_id[id_]["loai"]):
                raise ValueError(f"bảng điểm v2: ưu tiên {khoa} trỏ tới {id_} không có / không hợp sở thích")
    if "chung" not in uu_tien:
        raise ValueError("bảng điểm v2: thiếu danh sách ưu tiên 'chung'")
    loai_hien = tuple(l for l in LOAI_DIEM_THU_TU if sum(l in d["loai"] for d in diem) >= NGUONG_LOAI)
    return BangV2(tuple(diem), theo_id, cum, uu_tien, loai_hien, data.get("nhac_mua_chung"))


@dataclass(frozen=True)
class ThamSoV2:
    so_ngay: int
    tre_em: int = 0
    lon_tuoi: bool = False
    kieu_di: str | None = None  # None ⇒ `KIEU_DI_MAC_DINH`, có dòng giả định
    so_thich: tuple[str, ...] = ()
    nguoi_lon: int | None = None  # chỉ vào lời văn / dòng "Mình hiểu"; không vào bộ xếp

    @property
    def han_che(self) -> bool:
        return self.tre_em >= 1 or self.lon_tuoi


def tu_truong(moi: dict) -> ThamSoV2:
    """Giá trị biểu mẫu khuôn mới (`hoi_lai.doi_sang_moi` đã áp cho giá trị cũ) ⇒ tham số bộ xếp."""
    so_thich = moi.get("so_thich") or ()
    return ThamSoV2(so_ngay=int(moi["so_ngay"]), tre_em=moi.get("tre_em") or 0, lon_tuoi=bool(moi.get("lon_tuoi")), kieu_di=moi.get("kieu_di"),
                    so_thich=tuple([so_thich] if isinstance(so_thich, str) else so_thich), nguoi_lon=moi.get("nguoi_lon"))


def _xen_ke(ds: list[list[str]]) -> list[str]:
    """A1, B1, A2, B2… bỏ id đã có (một điểm hợp cả hai sở thích chỉ xét một lần, ở vị trí sớm nhất)."""
    out: list[str] = []
    for k in range(max((len(x) for x in ds), default=0)):
        for x in ds:
            if k < len(x) and x[k] not in out:
                out.append(x[k])
    return out


def thu_tu_xet(bang: BangV2, so_thich: tuple[str, ...], bo: set[str] = frozenset()) -> tuple[list[str], list[str], set[str]]:
    """5c.4: (thứ tự điểm sở thích = ưu tiên ⇒ hợp sở thích theo thứ tự bảng, xen kẽ hai sở thích; danh sách di tích lấp; tập điểm ưu tiên).
    Không chọn sở thích ⇒ ưu tiên "chung" rồi di tích theo thứ tự bảng (luật cũ: mặc định di tích tiêu biểu). `bo` = điểm cả lịch không dùng được
    (cụm xa khi < 3 ngày) — bỏ **trước khi** xen kẽ, để lượt của một sở thích không rơi vào điểm của sở thích kia."""
    khoa = list(so_thich) or ["chung"]
    uu = _xen_ke([[i for i in bang.uu_tien.get(k, []) if i not in bo] for k in khoa])
    loai = list(so_thich) or ["di_tich"]
    hop = _xen_ke([[d["id"] for d in bang.diem if l in d["loai"] and d["id"] not in bo] for l in loai])
    lap = [d["id"] for d in bang.diem if "di_tich" in d["loai"]]
    return uu + [i for i in hop if i not in uu], lap, set(uu)


def _phut_di(a: dict, b: dict) -> int | None:
    if a["cum"] == b["cum"]:
        return DI_CUNG_CUM
    return DI_CUM_KE if b["cum"] in CUM_KE.get(a["cum"], ()) else None


# 5c.3 giờ gợi ý (phút từ 0:00): sáng 8:00 · chiều 13:30; khám phá nhiều 7:30 · 13:00; nhóm hạn chế giờ như nhẹ nhàng
GIO_BAT_DAU = {"kham_pha": {"sang": 450, "chieu": 780}, "khac": {"sang": 480, "chieu": 810}}
CUM_TOI = ("bo_nam", "kinh_thanh")  # 5c.4: hoạt động tối chỉ ở hai cụm trung tâm (khách đã về khu trung tâm)
CAU_TOI = {"xa": "Tối nghỉ sau chuyến đi xa.", "tre_em": "Để trống — đi cùng trẻ nhỏ nên lịch chỉ xếp buổi sáng và chiều.",
           "lon_tuoi": "Để trống — đi cùng người lớn tuổi nên lịch chỉ xếp buổi sáng và chiều.",
           "khong_co": "Tối tự do — kho chưa có hoạt động buổi tối hợp ngày này."}


def ra_phut(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def in_gio(a: int, b: int) -> str:
    return f"{a // 60}:{a % 60:02d} – {b // 60}:{b % 60:02d}"


def dat_gio(d: dict, t: int) -> tuple[int, int] | None:
    """Lần ghé bắt đầu sớm nhất lúc `t` ⇒ (bắt đầu, kết thúc) nằm gọn trong một khung `gio_mo` (mở muộn ⇒ dời tới giờ mở); vượt giờ đóng mọi
    khung ⇒ None. Điểm không có `gio_mo` (kho không ghi giờ) ⇒ không ràng buộc."""
    dai = PHUT[d["thoi_luong"]]
    if not d.get("gio_mo"):
        return t, t + dai
    for mo, dong in d["gio_mo"]:
        s = max(t, ra_phut(mo))
        if s + dai <= ra_phut(dong):
            return s, s + dai
    return None


NGUONG_MUA = 60  # = `thoi_tiet.NGUONG_MUA` (không thêm ngưỡng mới — spec 5c.2); giữ ở đây để module thuần không import phần gọi mạng
THU_TU_MUA = {"trong_nha": 0, "ca_hai": 1, "ngoai_troi": 2}  # ngày mưa: điểm không ưu tiên xét trong nhà ⇒ cả hai ⇒ ngoài trời


def tam_dung(d: dict, ngay: dt.date | None) -> bool:
    """5c.2 (i): điểm tạm dừng đón khách theo mùa, ngày đó rơi vào tháng dừng."""
    m = d.get("mua_luu_y") or {}
    return ngay is not None and bool(m.get("bo_khoi_lich")) and ngay.month in m.get("thang", ())


def dung_thu(d: dict, ngay: dt.date | None) -> bool:
    """Thứ hoạt động (`ngay_hoat_dong`, thứ Hai = 0): rỗng = mọi ngày; chưa có ngày đi ⇒ không biết thứ ⇒ chỉ điểm mọi ngày (không đoán).
    Thứ đóng cửa của điểm ban ngày (`dong_cua_thu`): biết ngày ⇒ không xếp vào thứ đó; chưa có ngày ⇒ vẫn xếp (đa số ngày mở cửa)."""
    if ngay is not None and ngay.weekday() in (d.get("dong_cua_thu") or ()):
        return False
    thu = d.get("ngay_hoat_dong") or []
    return not thu or (ngay is not None and ngay.weekday() in thu)


def xep_v2(bang: BangV2, ts: ThamSoV2, ngay_1_khong_xa: bool = True, ngay_bat_dau: dt.date | None = None,
           mua: dict | None = None, giu: dict[str, tuple[int, str]] | None = None, loai: frozenset[str] = frozenset()) -> dict:
    """Khung tham quan sáng / chiều theo luật ở đầu module. `ngay_1_khong_xa=False` chỉ để mô phỏng so "có / không luật cụm xa ngày 1".
    Bước (d): `ngay_bat_dau` (ngày đi) ⇒ mỗi ngày lịch có ngày thật ⇒ luật mùa + thứ xét theo NGÀY (lịch vắt hai tháng xét từng ngày);
    `mua` = {ngày: khả năng mưa %} (chỉ các ngày có dự báo) ⇒ ngày ≥ `NGUONG_MUA` đổi thứ tự xét của điểm không ưu tiên.
    Sửa lịch (plan 2026-11-14-sua-lich-v2): `giu` = điểm giữ nguyên chỗ {id: (ngày, buổi sáng / chiều)}, đặt trước rồi buổi đó không lấp thêm;
    `loai` = điểm người dùng đã bỏ — không bao giờ được chọn lại (cả buổi tối). Mặc định (None, rỗng) ⇒ đúng như trước (test 3.840 khung giống byte)."""
    n = ts.so_ngay
    giu = {i: v for i, v in (giu or {}).items() if v[0] <= n and v[1] in BUOI_NGAY and i not in loai}
    ngay_cua = (lambda i: None) if ngay_bat_dau is None else (lambda i: ngay_bat_dau + dt.timedelta(days=i - 1))
    kieu = ts.kieu_di or KIEU_DI_MAC_DINH
    quy = None if ts.han_che else QUY[kieu]  # nhóm hạn chế: trần là "nhẹ nhàng" (spec 3.1)
    bo = ({d["id"] for d in bang.diem if d["cum"] == CUM_XA} if n < 3 else set()) | set(loai)
    pool, lap, uu = thu_tu_xet(bang, ts.so_thich, bo)
    lap = [j for j in lap if j not in loai]  # sửa lịch: danh sách lấp không giữ `bo` (cụm xa tự lọc ở `dung_duoc`) ⇒ loại điểm đã bỏ riêng ở đây
    hop_so_thich = set(pool) - uu if ts.so_thich else set()
    thien_nhien = [d["id"] for d in bang.diem if not ts.so_thich and "thien_nhien" in d["loai"] and d["id"] not in loai]
    T = bang.theo_id
    used: set[str] = set(giu)
    bi_thay: dict[str, str] = {}  # điểm ưu tiên bị thay vì bậc thang ⇒ điểm thay (ghi chú do code nếu cuối cùng vẫn không xếp)

    bat_dau = GIO_BAT_DAU["kham_pha" if kieu == "kham_pha" and not ts.han_che else "khac"]
    gio: dict[str, tuple[int, int]] = {}

    def dung_duoc(id_: str, ngay_i: int, buoi: str, cums: list[str], t: int | None = None) -> bool:
        d = T[id_]
        if id_ in used or buoi not in d["buoi"] or not _cum_hop(d["cum"], cums):
            return False
        if dat_gio(d, bat_dau[buoi] if t is None else t) is None:  # bậc 2 (5b): vượt giờ đóng ⇒ không xếp
            return False
        if tam_dung(d, ngay_cua(ngay_i)) or not dung_thu(d, ngay_cua(ngay_i)):  # bậc 2 (5b): thắng cả ưu tiên
            return False
        return d["cum"] != CUM_XA or (n >= 3 and (ngay_i > 1 or not ngay_1_khong_xa))

    def tranh_bac_thang(id_: str, ngay_i: int, buoi: str, cums: list[str]) -> str:
        """Nhóm hạn chế + điểm nhiều bậc thang ⇒ điểm khác cùng cụm, không bậc thang, theo cùng thứ tự xét (nếu có)."""
        if not ts.han_che or T[id_]["bac_thang"] != "nhieu":
            return id_
        thay = next((j for j in pool + lap if j != id_ and T[j]["cum"] == T[id_]["cum"] and T[j]["bac_thang"] is None
                     and dung_duoc(j, ngay_i, buoi, cums)), None)
        if thay is None:
            return id_
        if id_ in uu:
            bi_thay.setdefault(id_, thay)
        return thay

    def diem_dau(ngay_i: int, buoi: str, cums: list[str], tn_hom_nay: bool) -> str | None:
        if buoi == "chieu" and not ts.so_thich and not tn_hom_nay:
            id_ = next((j for j in thien_nhien if dung_duoc(j, ngay_i, buoi, cums)), None)
            if id_ is not None:
                return tranh_bac_thang(id_, ngay_i, buoi, cums)
        if buoi == "sang":  # B171 (L-a) giữ: sáng ưu tiên điểm còn "bạn chiều" cùng cụm / cụm kề để chiều không phải lấp ngoài sở thích
            id_ = next((j for j in pool if dung_duoc(j, ngay_i, buoi, cums) and any(
                p != j and p not in used and "chieu" in T[p]["buoi"] and _cum_hop(T[p]["cum"], [T[j]["cum"]]) for p in pool)), None)
            if id_ is not None:
                return tranh_bac_thang(id_, ngay_i, buoi, cums)
        id_ = next((j for j in pool + lap if dung_duoc(j, ngay_i, buoi, cums)), None)
        return None if id_ is None else tranh_bac_thang(id_, ngay_i, buoi, cums)

    def them(ids: list[str], cums: list[str]) -> None:
        for id_ in ids:
            used.add(id_)
            if T[id_]["cum"] not in cums:
                cums.append(T[id_]["cum"])

    pool_goc, lap_goc = pool, lap
    ngay = []
    for i in range(1, n + 1):
        if mua and (mua.get(ngay_cua(i)) or 0) >= NGUONG_MUA:  # ngày mưa: điểm ưu tiên giữ chỗ, phần còn lại xét trong nhà trước (sort ổn định)
            pool = [j for j in pool_goc if j in uu] + sorted([j for j in pool_goc if j not in uu], key=lambda j: THU_TU_MUA[T[j]["trong_nha"]])
            lap = sorted(lap_goc, key=lambda j: THU_TU_MUA[T[j]["trong_nha"]])
        else:
            pool, lap = pool_goc, lap_goc
        cums: list[str] = []
        slots: dict[str, list[str]] = {b: [] for b in BUOI}
        tn_hom_nay = False
        giu_buoi: set[str] = set()
        for id_, (ng_g, b_g) in giu.items():  # sửa lịch: điểm giữ chỗ đặt trước, tính vào cụm của ngày; giờ nối tiếp như điểm thêm
            if ng_g != i:
                continue
            truoc = slots[b_g][-1] if slots[b_g] else None
            t = bat_dau[b_g] if truoc is None else gio[truoc][1] + (_phut_di(T[truoc], T[id_]) or DI_CUM_KE)
            them([id_], cums)
            slots[b_g].append(id_)
            gio[id_] = dat_gio(T[id_], t) or (t, t + PHUT[T[id_]["thoi_luong"]])  # vượt giờ đóng ⇒ kiểm khung bắt (ngoai_gio_mo)
            tn_hom_nay = tn_hom_nay or "thien_nhien" in T[id_]["loai"]
            giu_buoi.add(b_g)
        for buoi in BUOI_NGAY:  # điểm đầu của sáng rồi chiều trước (bậc 4–6), điểm thêm theo kiểu đi sau (bậc 7) — điểm thêm không được chiếm suất cụm
            if buoi in giu_buoi:
                continue
            dau = diem_dau(i, buoi, cums, tn_hom_nay)  # của điểm ưu tiên buổi chiều (mô phỏng lần đầu: 2 / 960 khung thiếu ưu tiên số 1 vì vậy)
            if dau is None:
                continue
            tn_hom_nay = tn_hom_nay or "thien_nhien" in T[dau]["loai"]
            them([dau], cums)
            slots[buoi].append(dau)
            gio[dau] = dat_gio(T[dau], bat_dau[buoi])
        for buoi in BUOI_NGAY:
            if not slots[buoi] or buoi in giu_buoi:
                continue
            tong = PHUT[T[slots[buoi][0]]["thoi_luong"]]
            # review 14/11 M-1: quỹ phút không tính thời gian chờ giờ suất / mở cửa ⇒ điểm thêm buổi sáng phải xong trước giờ đầu buổi chiều
            het_sang = gio[slots["chieu"][0]][0] if slots["chieu"] else bat_dau["chieu"]
            while quy is not None and len(slots[buoi]) < TOI_DA_BUOI:  # 5c.3: điểm thêm cùng cụm / cụm kề với điểm ngay trước, vừa quỹ phút
                truoc = T[slots[buoi][-1]]
                t_den = gio[slots[buoi][-1]][1]  # điểm thêm bắt đầu sau điểm trước + phút đi (5c.3); phải vừa giờ mở cửa của nó
                tiep = next((j for j in pool + lap if _phut_di(truoc, T[j]) is not None and dung_duoc(j, i, buoi, cums, t_den + _phut_di(truoc, T[j]))
                             and tong + _phut_di(truoc, T[j]) + PHUT[T[j]["thoi_luong"]] <= quy
                             and (buoi != "sang" or dat_gio(T[j], t_den + _phut_di(truoc, T[j]))[1] <= het_sang)), None)
                if tiep is None:
                    break
                tong += _phut_di(truoc, T[tiep]) + PHUT[T[tiep]["thoi_luong"]]
                gio[tiep] = dat_gio(T[tiep], t_den + _phut_di(truoc, T[tiep]))
                them([tiep], cums)
                slots[buoi].append(tiep)
        ngay.append({"ngay": i, "buoi": slots})

    toi_nghi = _xep_toi(bang, ts, ngay, [ngay_cua(i) for i in range(1, n + 1)], set(used) | set(loai))
    da_xep = [j for ng in ngay for b in BUOI for j in ng["buoi"][b]]
    ngoai = [j for j in da_xep if ts.so_thich and not set(ts.so_thich) & set(T[j]["loai"]) and j not in
             [x for ng in ngay for x in ng["buoi"]["toi"]]]  # hoạt động tối không phải "điểm lấp ngoài sở thích"
    thieu = [s for s in ts.so_thich if not any(j in da_xep for j in bang.uu_tien.get(s, []))]  # 5c.7 (4): ghi chú do code
    gia_dinh = (["kieu_di"] if ts.kieu_di is None else []) + (["han_che"] if ts.han_che else []) + \
        (["so_thich"] if not ts.so_thich else [])
    ngays = [ngay_cua(i) for i in range(1, n + 1)]
    # 5c.2 (i): điểm ưu tiên không xếp vì đang tạm dừng theo mùa ⇒ ghi chú (mã `tam_dung_mua`)
    tam_dung_uu = [j for j in uu if j not in da_xep and any(tam_dung(T[j], x) for x in ngays)]
    return {"phien_ban": 2,
            "tham_so": {"so_ngay": n, "nguoi_lon": ts.nguoi_lon, "tre_em": ts.tre_em, "lon_tuoi": ts.lon_tuoi, "kieu_di": kieu,
                        "so_thich": list(ts.so_thich)},
            "ngay": ngay, "ngoai_so_thich": ngoai, "hop_so_thich": sorted(hop_so_thich & set(da_xep)), "thieu_uu_tien": thieu,
            "thay_bac_thang": [{"diem": k, "thay": v} for k, v in bi_thay.items() if k not in da_xep], "gia_dinh": gia_dinh,
            "ngay_thang": [None if x is None else x.isoformat() for x in ngays], "tam_dung_mua": tam_dung_uu,
            "gio": {j: in_gio(*gio[j]) for j in gio}, "toi_nghi": toi_nghi,
            "mua_mua": bool(bang.nhac_mua_chung) and any(x is not None and x.month in bang.nhac_mua_chung["thang"] for x in ngays),
            "khong_xep": []}  # `lich_trinh.bo_diem` / `cat_ngay_cuoi` ghi vào đây khi lấy đoạn kho (dùng lại phần lấy nguồn của đường cũ)


def _xep_toi(bang: BangV2, ts: ThamSoV2, ngay: list[dict], ngays: list, da_dung: set[str]) -> dict[int, str]:
    """Bước (e), chọn SAU khi khung tham quan đã chốt (không làm đổi khung — spec 5b bậc 8): nhóm không hạn chế ⇒ mỗi tối một hoạt động đúng thứ,
    chỉ ở hai cụm trung tâm, không trùng điểm ban ngày, không lặp tới khi hết (hết ⇒ lặp hoạt động diễn mọi tối, nhãn "có thể đi lại");
    ngày có điểm cụm xa ⇒ tối nghỉ; nhóm hạn chế ⇒ tối để trống (lý do). Trả {ngày: mã tối nghỉ} (ngày có hoạt động không có mặt)."""
    T, nghi = bang.theo_id, {}
    so_thich = set(ts.so_thich)
    ung_vien = sorted((d for d in bang.diem if "toi" in d["buoi"] and d["cum"] in CUM_TOI and d["id"] not in da_dung),
                      key=lambda d: not (so_thich & set(d["loai"])))  # hợp sở thích trước, rồi thứ tự bảng (sort ổn định)
    da_toi: list[str] = []
    for ng, ngay_that in zip(ngay, ngays):
        if ts.han_che:
            nghi[ng["ngay"]] = "tre_em" if ts.tre_em else "lon_tuoi"
            continue
        if any(T[j]["cum"] == CUM_XA for b in BUOI_NGAY for j in ng["buoi"][b]):
            nghi[ng["ngay"]] = "xa"
            continue
        hop = [d["id"] for d in ung_vien if dung_thu(d, ngay_that) and not tam_dung(d, ngay_that)]
        moi = [j for j in hop if j not in da_toi]
        lai = [j for j in hop if not T[j].get("ngay_hoat_dong")]  # diễn mọi tối ⇒ đi lại được
        chon = moi[0] if moi else (lai[0] if lai else None)
        if chon is None:
            nghi[ng["ngay"]] = "khong_co"
            continue
        ng["buoi"]["toi"].append(chon)
        da_toi.append(chon)
    return nghi


ANH_SRC = "/anh/lich/"  # ảnh lịch tự host (frontend/public/anh/lich/) — CSP img-src 'self' không đổi
ANH_TRANG = "https://commons.wikimedia.org/"
FRONTEND_PUBLIC = Path(__file__).resolve().parents[2] / "frontend" / "public"


def nap_bang_anh(path: str | Path, bang: BangV2) -> dict[str, dict]:
    """Bảng ảnh lịch (đợt 2 B0 của C, `bang_anh_v1.json`) ⇒ {id_diem: {src, tac_gia, giay_phep, trang[, chu_thich]}}. Lúc khởi động (cờ `anh_lich`):
    id phải có trong bảng điểm, `src` dưới `/anh/lich/` và file có thật, `trang` là trang Wikimedia Commons, đủ tác giả + giấy phép; sai ⇒ `ValueError`."""
    out = {}
    for a in json.loads(Path(path).read_text(encoding="utf-8"))["anh"]:
        id_, src = a.get("id_diem"), a.get("src") or ""
        if id_ not in bang.theo_id or id_ in out:
            raise ValueError(f"bảng ảnh: {id_} không có trong bảng điểm hoặc lặp")
        if not (src.startswith(ANH_SRC) and "/" not in src[len(ANH_SRC):] and src.endswith(".jpg") and (FRONTEND_PUBLIC / src.lstrip("/")).is_file()):
            raise ValueError(f"bảng ảnh: {id_} src phải là file có thật dưới {ANH_SRC}")
        if not (a.get("tac_gia") and a.get("giay_phep") and str(a.get("trang", "")).startswith(ANH_TRANG)):
            raise ValueError(f"bảng ảnh: {id_} thiếu tác giả / giấy phép / trang ảnh Commons")
        out[id_] = {k: a[k] for k in ("src", "tac_gia", "giay_phep", "trang", "chu_thich", "doi") if a.get(k)}  # `doi`: chỉnh khác thu nhỏ (vd cắt)
    return out


def kiem_doan_mo_ta(bang: BangV2, lay_doan) -> None:
    """Lúc khởi động (cờ bản 2 bật): mọi `doan_mo_ta` của bảng phải có trong chỉ mục đang chạy — chunk_id đổi khi dựng lại chỉ mục / sửa kho.
    Thiếu ⇒ `ValueError` nêu rõ mã thiếu (server không khởi động; không lặng lẽ quay về đoạn kém). `lay_doan` = `retrieval_service.lay_doan`."""
    can = {d["id"]: d["doan_mo_ta"] for d in bang.diem if d.get("doan_mo_ta")}
    co = lay_doan(list(can.values()))
    thieu = sorted(f"{i}: {c}" for i, c in can.items() if c not in co)
    if thieu:
        raise ValueError(f"bảng điểm v2: {len(thieu)} doan_mo_ta không có trong chỉ mục (dựng lại chỉ mục ⇒ cập nhật bảng): {'; '.join(thieu)}")


def diem_v2(khung: dict) -> list[str]:
    return [j for ng in khung["ngay"] for b in BUOI for j in ng["buoi"][b]]


def diem_ban_ngay(khung: dict) -> list[str]:
    """Điểm tham quan sáng / chiều (không gồm hoạt động tối) — đơn vị của các sàn "suất sáng / chiều"."""
    return [j for ng in khung["ngay"] for b in BUOI_NGAY for j in ng["buoi"][b]]


def kiem_khung_v2(bang: BangV2, khung: dict) -> list[str]:
    """Luật xếp kiểm **độc lập** với `xep_v2` (mỗi lỗi một mã; khung đúng ⇒ []): dùng cho mô phỏng toàn tổ hợp + test cố tình vi phạm."""
    T, ts = bang.theo_id, khung["tham_so"]
    n, han_che = ts["so_ngay"], ts["tre_em"] >= 1 or ts["lon_tuoi"]
    loi: list[str] = []
    if len(khung["ngay"]) != n or [ng["ngay"] for ng in khung["ngay"]] != list(range(1, n + 1)):
        loi.append("so_ngay")
    for ng in khung["ngay"]:
        cums: list[str] = []
        so = 0
        toi = ng["buoi"].get("toi") or []
        if len(toi) > 1 or (toi and han_che):
            loi.append("toi_qua_day")
        for j in toi:
            if "toi" not in T[j]["buoi"] or T[j]["cum"] not in CUM_TOI:
                loi.append("toi_sai_diem")
            if any(T[x]["cum"] == CUM_XA for b in BUOI_NGAY for x in ng["buoi"][b]):
                loi.append("toi_ngay_xa")
        gio_k = khung.get("gio", {})
        for b in BUOI_NGAY:  # 5c.3: giờ do code in — đúng thời lượng, trong giờ mở cửa, tăng dần, cách nhau ≥ phút đi; buổi chiều không trước 13:00
            truoc = None
            for j in ng["buoi"][b]:
                if j not in gio_k:
                    loi.append("thieu_gio")
                    continue
                s, e = (ra_phut(x.strip()) for x in gio_k[j].split("–"))
                if e - s != PHUT[T[j]["thoi_luong"]] or (T[j].get("gio_mo") and not any(ra_phut(o) <= s and e <= ra_phut(c) for o, c in T[j]["gio_mo"])):
                    loi.append("ngoai_gio_mo")
                if b == "chieu" and s < GIO_BAT_DAU["kham_pha"]["chieu"]:
                    loi.append("gio_buoi_sai")
                if truoc is not None and s < truoc[1] + (_phut_di(T[truoc[0]], T[j]) or 0):
                    loi.append("gio_chong")
                truoc = (j, e)
        sang, chieu = ng["buoi"]["sang"], ng["buoi"]["chieu"]
        if sang and chieu and sang[-1] in gio_k and chieu[0] in gio_k and \
                ra_phut(gio_k[sang[-1]].split("–")[1].strip()) > ra_phut(gio_k[chieu[0]].split("–")[0].strip()):
            loi.append("sang_chong_chieu")  # review 14/11 M-1: hai buổi liền nhau không được chồng giờ
        for b in BUOI_NGAY:
            ids = ng["buoi"][b]
            so += len(ids)
            for id_ in ids:
                d = T[id_]
                if b not in d["buoi"]:
                    loi.append("buoi_ngoai_buoi")
                if d["cum"] == CUM_XA and (n < 3 or ng["ngay"] == 1):
                    loi.append("cum_xa")
                if d["cum"] not in cums:
                    cums.append(d["cum"])
            if len(ids) > TOI_DA_BUOI or (len(ids) > 1 and (han_che or ts["kieu_di"] == "nhe_nhang")):
                loi.append("qua_day_buoi")
            if len(ids) > 1:
                phut = PHUT[T[ids[0]]["thoi_luong"]]
                for a, c in zip(ids, ids[1:]):
                    di = _phut_di(T[a], T[c])
                    if di is None:
                        loi.append("ghep_khong_ke")
                        break
                    phut += di + PHUT[T[c]["thoi_luong"]]
                if QUY.get(ts["kieu_di"]) is not None and phut > QUY[ts["kieu_di"]]:
                    loi.append("vuot_quy")
        if so == 0:
            loi.append("ngay_rong")
        if len(cums) > 2 or (CUM_XA in cums and len(cums) > 1):
            loi.append("qua_2_cum")
        if len(cums) == 2 and cums[1] not in CUM_KE.get(cums[0], ()):
            loi.append("cum_khong_ke")
        if han_che and so > 2:
            loi.append("han_che_qua_day")
        ngay_that = khung.get("ngay_thang", [None] * n)[ng["ngay"] - 1] if khung.get("ngay_thang") else None
        ngay_that = None if ngay_that is None else dt.date.fromisoformat(ngay_that)
        for id_ in (j for b in BUOI for j in ng["buoi"][b]):
            if tam_dung(T[id_], ngay_that):
                loi.append("tam_dung_mua")
            if not dung_thu(T[id_], ngay_that):
                loi.append("sai_thu")
    ban_ngay = [j for ng in khung["ngay"] for b in BUOI_NGAY for j in ng["buoi"][b]]
    toi_all = [j for ng in khung["ngay"] for j in ng["buoi"].get("toi") or []]
    if len(ban_ngay) != len(set(ban_ngay)) or set(ban_ngay) & set(toi_all):
        loi.append("trung_diem")
    if any(toi_all.count(j) > 1 and T[j].get("ngay_hoat_dong") for j in set(toi_all)):  # chỉ hoạt động diễn mọi tối mới được lặp
        loi.append("toi_lap_sai")
    if ts["so_thich"]:  # điểm lấp ngoài sở thích chỉ tính sáng / chiều (hoạt động tối chọn theo thứ, không phải "lấp")
        ngoai = {j for ng in khung["ngay"] for b in BUOI_NGAY for j in ng["buoi"][b] if not set(ts["so_thich"]) & set(T[j]["loai"])}
        if ngoai != set(khung["ngoai_so_thich"]):
            loi.append("lap_khong_nhan")
    return loi


# =====================================================================================================================================
# Bước (c): khuôn `lich` phiên bản 2 (spec 5c.5) + model chỉ viết một câu cho mỗi mục (5c.6) + kiểm từng câu — code thuần
# =====================================================================================================================================

NHAN_LOAI = {"di_tich": "di tích", "am_thuc": "ẩm thực", "thien_nhien": "thiên nhiên", "le_hoi_nghe_thuat": "lễ hội, nghệ thuật",
             "chup_anh": "chụp ảnh"}
NHAN_BUOI = {"sang": "Sáng", "trua": "Trưa", "chieu": "Chiều", "toi": "Tối"}
NHAN_KIEU_DI = {"nhe_nhang": "nhẹ nhàng", "can_bang": "cân bằng", "kham_pha": "khám phá nhiều"}
NHAN_MUC = {"co_the_di_lai": "có thể đi lại", "kiem_lich_dien": "kiểm lịch diễn trước khi đi"}  # nhãn mục hiện cho người dùng (code viết)
CAU_MUC_TOI_DA = 30  # từ / câu (5c.6) — chỉ đếm để báo, không thay câu (lời dặn đã giới hạn; cắt chữ model là sửa chữ người khác viết)
# Ghi chú do code viết (model không viết lý do) — mã ⇒ câu
CAU_GHI_CHU = {
    "kieu_di": "Chưa chọn kiểu đi nên mình xếp mức cân bằng.",
    "han_che": "Đi cùng trẻ em hoặc người lớn tuổi nên mình xếp nhẹ nhàng: mỗi buổi một điểm, không xếp buổi tối.",
    "so_thich": "Chưa chọn sở thích nên mình gợi ý điểm tiêu biểu, thêm một điểm thiên nhiên mỗi ngày.",
    "thay_bac_thang": "{diem} có nhiều bậc thang (theo kho) nên mình xếp {thay} cùng khu thay vào.",
    "thieu_uu_tien": "Lịch này chưa xếp được điểm tiêu biểu nhất cho sở thích {so_thich} — thêm ngày thì mình xếp được nhiều điểm hơn.",
    "tam_dung_mua": "{diem} đang tạm dừng đón khách vào thời gian này trong năm (theo kho) nên mình chưa xếp.",
    "bac_thang": "{diem} có nhiều bậc thang (theo kho) — cân nhắc khi đi cùng trẻ nhỏ hoặc người lớn tuổi.",
}
# 5c.6: câu model không được chứa giờ / thời lượng / tiền / đường dẫn (code in những thứ đó)
_GIO = re.compile(r"(?<!\w)\d{1,2}\s*(?:[:hg]\s*\d{2}|h(?!\w)|giờ|tiếng|phút)", re.IGNORECASE)
_THOI_LUONG = re.compile(r"(?<!\w)(?:\d+|một|hai|ba|nửa)\s*(?:giờ|tiếng|phút|ngày)(?!\w)", re.IGNORECASE)
_LINK = re.compile(r"https?://|www\.|\.(?:vn|com|net|org)(?!\w)", re.IGNORECASE)


# review 14/11 M-2: câu nói về tài liệu / nguồn thay vì tả điểm ("tài liệu không cung cấp thông tin về …") ⇒ câu dự phòng. Thử trên 1.068 câu
# model đã lưu của nghiệm thu: trúng đúng 1 câu lỗi, 0 câu tốt bị chặn.
# Không bắt "tài liệu" / "văn bản" đứng một mình: điểm bảo tàng có thể "trưng bày tài liệu, văn bản cổ" (review E m-3).
_NOI_VE_TAI_LIEU = re.compile(r"(?:theo|trong) tài liệu|tài liệu (?:không|chưa|chỉ|được cung cấp)|đoạn trích|nguồn (?:này |trên )?(?:không|chưa)|không (?:cung cấp|đề cập|nhắc(?: đến| tới)?|có thông tin|nêu)"
                              r"|nội dung (?:chỉ|không)|chỉ (?:mô tả|nói về)|thông tin (?:về .{0,40} )?(?:không|chưa) có", re.IGNORECASE)


def co_suat_dien(diem: dict) -> bool:
    """Điểm tối là buổi diễn (loại lễ hội – nghệ thuật) ⇒ cần nhãn "kiểm lịch diễn" khi chưa có ngày đi. Chợ / phố đêm không có suất diễn ⇒ không
    nhãn (lượt thật 14/11: chợ bị gắn nhãn này). Điểm chỉ mở vài tối trong tuần không được xếp khi chưa có ngày (`dung_thu`) nên không cần nhãn khác."""
    return "le_hoi_nghe_thuat" in diem["loai"]


def ten_cua(diem: dict) -> list[str]:
    return [diem["ten"], *diem["ten_khac"]]


# Tên chặng ngắn cho tiêu đề ngày (giao diện) — theo mã cụm cố định của bảng; cụm lạ ⇒ tên cụm của bảng bỏ phần trong ngoặc
TEN_CHANG = {"kinh_thanh": "Kinh thành", "bo_nam": "Bờ nam sông Hương", "an_cuu": "An Cựu", "thuy_xuan": "Thủy Xuân — lăng và đồi thông",
             "kim_long": "Kim Long", "lang_xa": "Lăng xa thượng nguồn", "dong_bien": "Đầm phá và biển", "nam_xa": "Phía nam xa"}


def dung_lich(bang: BangV2, khung: dict, nguon: dict[str, int], ngay_di: str | None = None, them_ghi_chu: list[dict] = (),
              toa_do: dict | None = None, anh: dict | None = None) -> dict:
    """Khung đã có nguồn ⇒ `lich` phiên bản 2 (spec 5c.5). `toa_do` (cờ `ban_do_lich`, đợt 2): {id: (vĩ, kinh)} của bảng toạ độ ⇒ mỗi mục mang đúng
    dòng bảng theo `id_diem`; điểm thiếu ⇒ null (không ghim đoán); None ⇒ mọi mục null như đợt 1. Toạ độ không vào tin nhắn gửi model. `id_muc` = `n<ngày>-<buổi>-<thứ tự>` (khoá ổn định cho câu của model). Giờ gợi ý,
    ảnh, toạ độ, ngày tháng / thứ: các bước sau (d), (e), đợt 2 — ở đây để null."""
    ngay = []
    for ng in khung["ngay"]:
        ngay_that = (khung.get("ngay_thang") or [None] * len(khung["ngay"]))[ng["ngay"] - 1]
        muc = []
        for b in BUOI:
            for k, id_ in enumerate(ng["buoi"][b], start=1):
                d = bang.theo_id[id_]
                toi = b == "toi"
                lap_lai = toi and id_ in [x for ng0 in khung["ngay"] if ng0["ngay"] < ng["ngay"] for x in ng0["buoi"]["toi"]]
                muc.append({"id_muc": f"n{ng['ngay']}-{b}-{k}", "buoi": b, "loai": "hoat_dong_toi" if toi else "tham_quan", "id_diem": id_,
                            "ten": d["ten"], "gio": d.get("gio_toi") if toi else khung.get("gio", {}).get(id_),
                            "nguon": nguon.get(id_), "anh": dict(anh[id_]) if anh and id_ in anh else None,  # đợt 2 (B): cờ `anh_lich`
                            "toa_do": list(toa_do[id_]) if toa_do and id_ in toa_do else None,
                            "nhan": (["ngoai_so_thich"] if id_ in khung["ngoai_so_thich"] else []) + (["co_the_di_lai"] if lap_lai else [])
                                    + (["kiem_lich_dien"] if toi and ngay_that is None and co_suat_dien(d) else []),  # chưa có ngày ⇒ không khẳng định diễn hôm đó
                            "map_url": MAP_BASE + quote(f"{d['ten']}, Huế"),
                            "loai_diem": list(d["loai"])})  # giao diện: màu + nhãn theo loại điểm (không vào tin nhắn gửi model)
        if ng["ngay"] in khung.get("toi_nghi", {}):  # tối nghỉ: dòng do code (không qua model, không nguồn)
            muc.append({"id_muc": f"n{ng['ngay']}-toi-1", "buoi": "toi", "loai": "nghi", "id_diem": None,
                        "ten": CAU_TOI[khung["toi_nghi"][ng["ngay"]]], "gio": None, "nguon": None, "anh": None, "toa_do": None, "nhan": []})
        # giao diện mới 14/11: phút đi tới mục ngay trước TRONG CÙNG BUỔI = đúng số bộ xếp đã dùng để giãn giờ (ước theo cụm, 5c.3);
        # mục đầu buổi / hoạt động tối / tối nghỉ ⇒ không có trường (không đoán)
        for a, c in zip(muc, muc[1:]):
            if a["buoi"] == c["buoi"] != "toi" and a["id_diem"] and c["id_diem"]:
                phut = _phut_di(bang.theo_id[a["id_diem"]], bang.theo_id[c["id_diem"]])
                if phut is not None:
                    c["phut_di"] = phut
        # giao diện: "tên chặng" của ngày = các cụm của điểm ban ngày theo thứ tự đi (tên cụm của bảng, bỏ phần trong ngoặc); không vào model
        chang = list(dict.fromkeys(TEN_CHANG.get(c, bang.cum[c].split(" (")[0])
                                   for c in (bang.theo_id[m["id_diem"]]["cum"] for m in muc if m["id_diem"] and m["buoi"] != "toi")))
        ngay.append({"ngay": ng["ngay"], "ngay_thang": ngay_that, "chang": chang,
                     "thu": None if ngay_that is None else dt.date.fromisoformat(ngay_that).weekday(), "muc": muc})
    ts = khung["tham_so"]
    ghi_chu = [{"ma": "mua_mua", "cau": bang.nhac_mua_chung["cau"]}] if khung.get("mua_mua") else []  # 5c.2 (iii): đầu khối, đúng một dòng
    ghi_chu += [{"ma": m, "cau": CAU_GHI_CHU[m]} for m in khung["gia_dinh"]]
    if ts["tre_em"] or ts["lon_tuoi"]:  # bộ đo ý 2: nhóm hạn chế + điểm nhiều bậc thang còn trong lịch (không có điểm thay cùng khu) ⇒ ghi chú
        ghi_chu += [{"ma": "bac_thang", "cau": CAU_GHI_CHU["bac_thang"].format(diem=bang.theo_id[j]["ten"])}
                    for j in dict.fromkeys(diem_ban_ngay(khung)) if bang.theo_id[j]["bac_thang"] == "nhieu"]
    ghi_chu += [{"ma": "tam_dung_mua", "cau": CAU_GHI_CHU["tam_dung_mua"].format(diem=bang.theo_id[j]["ten"])} for j in khung.get("tam_dung_mua", [])]
    ghi_chu += [{"ma": "du_bao", **c} for c in them_ghi_chu]  # `{"cau", "ngay"?}` từ `len_ke_hoach.dong_du_bao`
    ghi_chu += [{"ma": "thay_bac_thang", "cau": CAU_GHI_CHU["thay_bac_thang"].format(diem=bang.theo_id[x["diem"]]["ten"],
                                                                                        thay=bang.theo_id[x["thay"]]["ten"])}
                for x in khung["thay_bac_thang"]]
    ghi_chu += [{"ma": "thieu_uu_tien", "cau": CAU_GHI_CHU["thieu_uu_tien"].format(so_thich=NHAN_LOAI[s])} for s in khung["thieu_uu_tien"]]
    ghi_chu += [{"ma": k["ma_luat"], "cau": CAU_KHONG_XEP[k["ma_luat"]].format(diem=k["diem"])} for k in khung["khong_xep"]]
    if khung.get("gio"):
        ghi_chu.append({"ma": "gio_goi_y", "cau": "Giờ trong lịch là giờ gợi ý theo thời lượng tham quan thường gặp. " + CAU_CO_THE_DOI})
    return {"phien_ban": 2, "tham_so": {**ts, "ngay_di": ngay_di}, "minh_hieu": dong_minh_hieu_v2(ts, ngay_di), "ngay": ngay,
            "o_dau": None, "ghi_chu": ghi_chu}


def moi_muc(lich: dict) -> list[dict]:
    """Mục model viết câu (tham quan, hoạt động tối); mục "nghỉ" là dòng do code, không vào model."""
    return [m for ng in lich["ngay"] for m in ng["muc"] if m["loai"] != "nghi"]


def dong_minh_hieu_v2(ts: dict, ngay_di: str | None) -> str:
    """Dòng đầu lịch, dựng từ **tham số thật** (không chữ model): số ngày · người · kiểu đi · sở thích · ngày đi."""
    phan = [f"{ts['so_ngay']} ngày"]
    if ts.get("nguoi_lon"):
        phan.append(f"{ts['nguoi_lon']} người lớn")
    if ts.get("tre_em"):
        phan.append(f"{ts['tre_em']} trẻ em")
    if ts.get("lon_tuoi"):
        phan.append("có người lớn tuổi")
    phan.append(f"đi {NHAN_KIEU_DI[ts['kieu_di']]}")
    if ts.get("so_thich"):
        phan.append("thích " + ", ".join(NHAN_LOAI[s] for s in ts["so_thich"]))
    if ngay_di:
        phan.append("đi từ " + "/".join(reversed(ngay_di.split("-"))))
    return "Mình hiểu: " + " · ".join(phan) + " — sai thì bấm **Sửa**."


def tin_nhan_model(lich: dict, tai_lieu: str) -> str:
    """Tin nhắn user của lần gọi viết câu (5c.6): danh sách mục (id_muc, tên điểm, mã tài liệu của điểm) + tài liệu từng điểm. Không chữ người
    dùng nào vào đây (chỉ giá trị biểu mẫu đã thành khung)."""
    dong = ["Danh sách mục:"]
    dong += [f"- {m['id_muc']}: {m['ten']} (tài liệu [{m['nguon']}])" for m in moi_muc(lich)]
    return "\n".join(dong) + "\n\nTài liệu:\n" + tai_lieu.strip()


def kiem_cau(bang: BangV2, muc: dict, cau: str) -> str | None:
    """Kiểm cuối MỘT câu (5c.6) ⇒ mã lỗi hoặc None. Lỗi ⇒ câu dự phòng cho riêng mục đó (không rút cả lịch)."""
    cau = cau.strip()
    if not cau:
        return "rong"
    if _NOI_VE_TAI_LIEU.search(unicodedata.normalize("NFC", cau)):
        return "noi_ve_tai_lieu"
    ma = [int(x) for x in CITATION_PATTERN.findall(cau)]
    if not ma:
        return "khong_ma"
    if any(x != muc["nguon"] for x in ma):
        return "ma_ngoai_nguon"
    if _GIO.search(cau) or _THOI_LUONG.search(cau):
        return "gio"
    if tim_so_tien(cau):
        return "tien"
    if _LINK.search(cau):
        return "link"
    chu = chuan_ten(cau)
    cua_minh = [chuan_ten(t) for t in ten_cua(bang.theo_id[muc["id_diem"]])]
    for d in bang.diem:
        if d["id"] == muc["id_diem"]:
            continue
        for t in ten_cua(d):
            k = chuan_ten(t)
            # tên điểm khác nằm trong câu — trừ khi chính tên đó là một phần tên của điểm này (tên con nằm trong điểm lớn: plan (c) đếm ca này)
            if re.search(rf"(?<!\w){re.escape(k)}(?!\w)", chu) and not any(k in m for m in cua_minh):
                return "ten_khac"
    return None


def cau_du_phong(bang: BangV2, muc: dict) -> str:
    """Câu do code khi câu model thiếu / lỗi: tên + loại điểm, không mô tả, kèm mã nguồn của điểm (5c.6)."""
    loai = ", ".join(NHAN_LOAI[x] for x in bang.theo_id[muc["id_diem"]]["loai"])
    return f"{muc['ten']} — điểm {loai} [{muc['nguon']}]."


def chon_cau(bang: BangV2, lich: dict, tu_model: list[dict]) -> tuple[dict[str, str], dict[str, str]]:
    """Mảng `{id_muc, cau}` của model ⇒ (câu cuối theo id_muc, mã lỗi theo id_muc). Lặp id ⇒ lấy phần tử đầu; id lạ ⇒ bỏ; thiếu ⇒ dự phòng."""
    muc = {m["id_muc"]: m for m in moi_muc(lich)}
    dau: dict[str, str] = {}
    for x in tu_model:
        if x.get("id_muc") in muc and x["id_muc"] not in dau:
            dau[x["id_muc"]] = x.get("cau") or ""
    cau, loi = {}, {}
    for id_muc, m in muc.items():
        ma = "thieu" if id_muc not in dau else kiem_cau(bang, m, dau[id_muc])
        cau[id_muc] = cau_du_phong(bang, m) if ma else dau[id_muc].strip()
        if ma:
            loi[id_muc] = ma
    return cau, loi


def ghep_chu(lich: dict, cau: dict[str, str]) -> str:
    """Trường `answer` chữ thuần (lịch sử chat, nút chép, giao diện cũ) — code ghép từ khung + câu; mỗi mục mang mã nguồn của điểm."""
    dong = [lich["minh_hieu"]]
    for ng in lich["ngay"]:
        dong += ["", f"**Ngày {ng['ngay']}**"]
        for m in ng["muc"]:
            gio = f" ({m['gio']})" if m["gio"] else ""
            them = "".join(f" ({NHAN_MUC[x]})" for x in m.get("nhan", ()) if x in NHAN_MUC)
            dong.append(f"- {NHAN_BUOI[m['buoi']]}: {m['ten']}" if m["loai"] == "nghi" else
                        f"- {NHAN_BUOI[m['buoi']]}{gio}: {m['ten']}{them} — {cau[m['id_muc']]}")
    if lich["ghi_chu"]:
        dong += ["", TIEU_DE_GHI_CHU, *(f"- {g['cau']}" for g in lich["ghi_chu"])]
    if lich.get("o_dau"):  # cờ `luu_tru_lich` (cờ tắt ⇒ None ⇒ chữ giống bản trước)
        dong += ltl.dong_chu(lich["o_dau"])
    return "\n".join(dong)


class CauStream:
    """Bóc các phần tử `{id_muc, cau}` ĐÃ ĐÓNG từ luồng JSON `{"cau": [...]}` đang stream (5c.6: một sự kiện mỗi khi một phần tử đóng ngoặc).
    Chữ cuối vẫn do lần đọc đầu ra có cấu trúc quyết; đây chỉ để hiện câu sớm."""

    def __init__(self) -> None:
        self.raw = ""
        self.pos = None  # vị trí sau dấu `[` của mảng
        self.ra = 0

    def feed(self, delta: str) -> list[dict]:
        self.raw += delta
        if self.pos is None:
            m = re.match(r'\s*\{\s*"cau"\s*:\s*\[', self.raw)
            if m is None:
                return []
            self.pos = m.end()
        out = []
        dec = json.JSONDecoder()
        while True:
            m = re.match(r"\s*,?\s*", self.raw[self.pos:])
            start = self.pos + m.end()
            if start >= len(self.raw) or self.raw[start] != "{":
                return out
            try:
                obj, end = dec.raw_decode(self.raw, start)
            except json.JSONDecodeError:
                return out
            self.pos = end
            if isinstance(obj, dict):
                out.append(obj)
