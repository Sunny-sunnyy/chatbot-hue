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
import json
from dataclasses import dataclass
from pathlib import Path

from llm.lich_trinh import BUOI, CUM_KE, CUM_XA, LOAI_DIEM, _cum_hop

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


def xep_v2(bang: BangV2, ts: ThamSoV2, ngay_1_khong_xa: bool = True) -> dict:
    """Khung tham quan sáng / chiều theo luật ở đầu module. `ngay_1_khong_xa=False` chỉ để mô phỏng so "có / không luật cụm xa ngày 1"."""
    n = ts.so_ngay
    kieu = ts.kieu_di or KIEU_DI_MAC_DINH
    quy = None if ts.han_che else QUY[kieu]  # nhóm hạn chế: trần là "nhẹ nhàng" (spec 3.1)
    bo = {d["id"] for d in bang.diem if d["cum"] == CUM_XA} if n < 3 else set()
    pool, lap, uu = thu_tu_xet(bang, ts.so_thich, bo)
    hop_so_thich = set(pool) - uu if ts.so_thich else set()
    thien_nhien = [d["id"] for d in bang.diem if not ts.so_thich and "thien_nhien" in d["loai"]]
    T = bang.theo_id
    used: set[str] = set()
    bi_thay: dict[str, str] = {}  # điểm ưu tiên bị thay vì bậc thang ⇒ điểm thay (ghi chú do code nếu cuối cùng vẫn không xếp)

    def dung_duoc(id_: str, ngay_i: int, buoi: str, cums: list[str]) -> bool:
        d = T[id_]
        if id_ in used or buoi not in d["buoi"] or not _cum_hop(d["cum"], cums):
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

    ngay = []
    for i in range(1, n + 1):
        cums: list[str] = []
        slots: dict[str, list[str]] = {b: [] for b in BUOI}
        tn_hom_nay = False
        for buoi in BUOI_NGAY:  # điểm đầu của sáng rồi chiều trước (bậc 4–6), điểm thêm theo kiểu đi sau (bậc 7) — điểm thêm không được chiếm suất cụm
            dau = diem_dau(i, buoi, cums, tn_hom_nay)  # của điểm ưu tiên buổi chiều (mô phỏng lần đầu: 2 / 960 khung thiếu ưu tiên số 1 vì vậy)
            if dau is None:
                continue
            tn_hom_nay = tn_hom_nay or "thien_nhien" in T[dau]["loai"]
            them([dau], cums)
            slots[buoi].append(dau)
        for buoi in BUOI_NGAY:
            if not slots[buoi]:
                continue
            tong = PHUT[T[slots[buoi][0]]["thoi_luong"]]
            while quy is not None and len(slots[buoi]) < TOI_DA_BUOI:  # 5c.3: điểm thêm cùng cụm / cụm kề với điểm ngay trước, vừa quỹ phút
                truoc = T[slots[buoi][-1]]
                tiep = next((j for j in pool + lap if dung_duoc(j, i, buoi, cums) and _phut_di(truoc, T[j]) is not None
                             and tong + _phut_di(truoc, T[j]) + PHUT[T[j]["thoi_luong"]] <= quy), None)
                if tiep is None:
                    break
                tong += _phut_di(truoc, T[tiep]) + PHUT[T[tiep]["thoi_luong"]]
                them([tiep], cums)
                slots[buoi].append(tiep)
        ngay.append({"ngay": i, "buoi": slots})

    da_xep = [j for ng in ngay for b in BUOI for j in ng["buoi"][b]]
    ngoai = [j for j in da_xep if ts.so_thich and not set(ts.so_thich) & set(T[j]["loai"])]
    thieu = [s for s in ts.so_thich if not any(j in da_xep for j in bang.uu_tien.get(s, []))]  # 5c.7 (4): ghi chú do code
    gia_dinh = (["kieu_di"] if ts.kieu_di is None else []) + (["han_che"] if ts.han_che and kieu != "nhe_nhang" else []) + \
        (["so_thich"] if not ts.so_thich else [])
    return {"phien_ban": 2,
            "tham_so": {"so_ngay": n, "nguoi_lon": ts.nguoi_lon, "tre_em": ts.tre_em, "lon_tuoi": ts.lon_tuoi, "kieu_di": kieu,
                        "so_thich": list(ts.so_thich)},
            "ngay": ngay, "ngoai_so_thich": ngoai, "hop_so_thich": sorted(hop_so_thich & set(da_xep)), "thieu_uu_tien": thieu,
            "thay_bac_thang": [{"diem": k, "thay": v} for k, v in bi_thay.items() if k not in da_xep], "gia_dinh": gia_dinh}


def diem_v2(khung: dict) -> list[str]:
    return [j for ng in khung["ngay"] for b in BUOI for j in ng["buoi"][b]]


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
        if ng["buoi"].get("toi"):
            loi.append("toi_o_buoc_b")  # buổi tối chỉ xếp ở bước (e)
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
    da_xep = diem_v2(khung)
    if len(da_xep) != len(set(da_xep)):
        loi.append("trung_diem")
    if ts["so_thich"]:
        ngoai = {j for j in da_xep if not set(ts["so_thich"]) & set(T[j]["loai"])}
        if ngoai != set(khung["ngoai_so_thich"]):
            loi.append("lap_khong_nhan")
    return loi
