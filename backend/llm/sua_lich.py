"""Sửa lịch nhiều lượt (Phase 9, plan `docs/superpowers/plans/2026-11-05-phase-9-sua-lich-plan.md` bản 3 `5b68f3cb666a`).

Model chọn **hành động có tên** (D3); **code** áp tối đa 2 hành động / lượt (D4) trên khung đã lưu của cuộc, theo **đúng luật B5** (mọi thay đổi
qua `kiem_khung`), giữ chỗ điểm không bị chạm, không cho điểm đã bỏ quay lại, không để giá trị mặc định ghi đè giá trị người dùng đã nói (D5),
đưa thẻ chọn khi "thay" mà không nói thay bằng gì (D6), rồi dựng khối "Đã đổi / Không đổi được / Chưa làm" (D7). Hàm thuần — không mạng, không SDK.
Trạng thái lưu của cuộc (D1, `luu`): {tham_so, da_noi, khung, them, loai, cau_goc, the_chon}. Mọi hàm nhận / trả **bản sao** (không sửa tại chỗ).
"""
import copy
from typing import Literal

from pydantic import BaseModel, ConfigDict

from llm.hoi_lai import GIA_TRI, NHAN_TRUONG
from llm.lich_trinh import (BUOI, CAU_KHONG_XEP, HAN_CHE, NHAN_BUOI, Bang, DiCung, KieuDi, SoNgay, ThamSo, diem_trong_khung, khop_diem,
                            kiem_khung, xep)

MAX_AP = 2  # D4
MAX_HANH_DONG = 3  # D3: model gửi tối đa 3 (ý thứ 3 ⇒ "Chưa làm")
MAX_LUA_CHON = 3  # D6
TRUONG_SUA = ("so_ngay", "di_cung", "kieu_di", "so_thich")


class HanhDong(BaseModel):
    """Một hành động sửa (D3). `ten` = điểm bị chạm (bỏ / thêm / thay / dời); `ten_moi` = điểm thay vào; `ngay` / `buoi` = chỗ muốn đặt."""
    model_config = ConfigDict(extra="forbid")
    loai: Literal["bo_diem", "them_diem", "thay_diem", "doi_buoi", "doi_so_ngay", "doi_tham_so"]
    ten: str | None = None
    ten_moi: str | None = None
    ngay: int | None = None
    buoi: Literal["sang", "chieu", "toi"] | None = None
    so_ngay: SoNgay | None = None
    di_cung: DiCung | None = None
    kieu_di: KieuDi | None = None
    so_thich: Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh", "bo"] | None = None


NHAN_HANH_DONG = {"bo_diem": "bỏ điểm", "them_diem": "thêm điểm", "thay_diem": "thay điểm", "doi_buoi": "dời buổi",
                  "doi_so_ngay": "đổi số ngày", "doi_tham_so": "đổi kiểu lịch"}
# mã luật thêm cho sửa lịch (ngoài mã B5 `CAU_KHONG_XEP`)
CAU_KHONG_DOI = {
    **CAU_KHONG_XEP,
    "khong_co_trong_lich": "«{diem}» không có trong lịch hiện tại.",
    "da_co_trong_lich": "{diem} đã có trong lịch.",
    "khong_hop_luat": "{diem} đặt ở chỗ đó sẽ làm lịch phạm luật xếp (cụm xa / quá dày) nên mình chưa đổi.",
    "thieu_cho": "Chưa rõ ngày / buổi để dời {diem}.",
    "het_diem_thay": "Không còn điểm phù hợp để thay {diem} (cùng cụm, hợp sở thích, đặt được vào chỗ đó) nên mình giữ nguyên.",
}
TIEU_DE_SUA = "**Mình đã sửa lịch**"


def luu_tu_lich(khung: dict, da_noi: list[str], them: list[str], cau_goc: str) -> dict:
    """D1: trạng thái lưu sau một lượt lịch đạt (bản sao sâu)."""
    return {"tham_so": copy.deepcopy(khung["tham_so"]), "da_noi": list(da_noi), "khung": copy.deepcopy(khung), "them": list(them),
            "loai": [], "cau_goc": cau_goc, "the_chon": None}


def _vi_tri(khung: dict) -> dict[str, tuple[int, str]]:
    return {i: (ng["ngay"], b) for ng in khung["ngay"] for b in BUOI for i in ng["buoi"][b]}


def _dat(khung: dict, id_: str, ngay: int, buoi: str) -> None:
    next(ng for ng in khung["ngay"] if ng["ngay"] == ngay)["buoi"][buoi].append(id_)


def _go(khung: dict, id_: str) -> None:
    for ng in khung["ngay"]:
        for b in BUOI:
            if id_ in ng["buoi"][b]:
                ng["buoi"][b].remove(id_)


def _ten(bang: Bang, id_: str) -> str:
    return bang.theo_id[id_]["ten"]


def _hop(bang: Bang, khung: dict) -> bool:
    """Khung thử còn đúng mọi luật B5? (`kiem_khung` 0 lỗi)."""
    return not kiem_khung(bang, khung)


def _dong_bo(bang: Bang, khung: dict, them: list[str]) -> None:
    """Giữ `tham_so.them_diem` và nhãn "ngoài sở thích" khớp khung sau khi sửa trực tiếp (để `kiem_khung` / khối ghi chú B5 đọc đúng)."""
    co = set(diem_trong_khung(khung))
    khung["tham_so"]["them_diem"] = [_ten(bang, i) for i in them if i in co]
    st = khung["tham_so"]["so_thich"]
    khung["ngoai_so_thich"] = [i for i in khung["ngoai_so_thich"] if i in co]
    if st is not None:
        khung["ngoai_so_thich"] += [i for i in co if st not in bang.theo_id[i]["loai"] and i not in them and i not in khung["ngoai_so_thich"]]
    if khung["ngoai_so_thich"] and khung.get("thieu_so_thich") is None:
        khung["thieu_so_thich"] = len([i for i in co if st in bang.theo_id[i]["loai"]])


def _thu_dat(bang: Bang, khung: dict, them: list[str], id_: str, cho: list[tuple[int, str]]) -> tuple[dict | None, tuple[int, str] | None]:
    """Thử đặt `id_` lần lượt vào các chỗ (ngày, buổi); chỗ đầu tiên khung còn đúng luật ⇒ (khung mới, chỗ)."""
    for ngay, buoi in cho:
        if not any(ng["ngay"] == ngay for ng in khung["ngay"]):
            continue
        k = copy.deepcopy(khung)
        _dat(k, id_, ngay, buoi)
        _dong_bo(bang, k, them + ([id_] if id_ not in them else []))
        if _hop(bang, k):
            return k, (ngay, buoi)
    return None, None


def _cac_cho(khung: dict, ngay: int | None, buoi: str | None) -> list[tuple[int, str]]:
    """Chỗ ứng viên: theo ngày / buổi người dùng nói; chỗ trống trước."""
    cho = [(ng["ngay"], b) for ng in khung["ngay"] for b in BUOI if (ngay is None or ng["ngay"] == ngay) and (buoi is None or b == buoi)]
    return sorted(cho, key=lambda c: bool(next(ng for ng in khung["ngay"] if ng["ngay"] == c[0])["buoi"][c[1]]))


def _ma_cho(bang: Bang, khung: dict, id_: str, buoi: str | None) -> str:
    """Vì sao không đặt được: buổi không hợp với điểm / người đi cùng ⇒ `khong_buoi_hop_le`; còn lại ⇒ hết chỗ hoặc phạm luật cụm / mật độ."""
    d = bang.theo_id[id_]
    han_che = khung["tham_so"]["di_cung"] in HAN_CHE
    if buoi is not None and (buoi not in d["buoi"] or (han_che and buoi == "toi")):
        return "khong_buoi_hop_le"
    if not set(d["buoi"]) & ({"sang", "chieu"} if han_che else set(BUOI)):
        return "khong_buoi_hop_le"
    duoc = set(d["buoi"]) & ({"sang", "chieu"} if han_che else set(BUOI))
    con_trong = any(not ng["buoi"][b] for ng in khung["ngay"] for b in duoc if buoi is None or b == buoi)
    return "khong_hop_luat" if con_trong else "het_suat"  # còn chỗ trống hợp buổi mà vẫn không đặt được ⇒ do luật cụm / mật độ


def _xep_lai(bang: Bang, luu: dict, ts_moi: dict, them: list[str], loai: list[str]) -> dict:
    """D5: đổi số ngày / tham số ⇒ xếp lại với **giữ** chỗ các điểm còn hợp tham số mới (điểm người dùng thêm, điểm hợp sở thích mới, buổi hợp
    người đi cùng, ngày còn trong lịch); `loai` không quay lại; điểm người dùng thêm vẫn ưu tiên. Giữ làm khung phạm luật ⇒ xếp lại không giữ."""
    n = 4 if ts_moi["so_ngay"] == "4+" else int(ts_moi["so_ngay"])
    han_che = ts_moi["di_cung"] in HAN_CHE
    giu: dict[str, tuple[int, str]] = {}
    dem_ngay: dict[int, int] = {}
    for id_, (ngay, buoi) in _vi_tri(luu["khung"]).items():
        d = bang.theo_id[id_]
        hop_st = id_ in them or ts_moi["so_thich"] is None or ts_moi["so_thich"] in d["loai"]
        if ngay > n or not hop_st or (han_che and (buoi == "toi" or dem_ngay.get(ngay, 0) >= 2)):
            continue
        if han_che and any(v == (ngay, buoi) for v in giu.values()):
            continue
        giu[id_] = (ngay, buoi)
        dem_ngay[ngay] = dem_ngay.get(ngay, 0) + 1
    ts = ThamSo(so_ngay=ts_moi["so_ngay"], di_cung=ts_moi["di_cung"], kieu_di=ts_moi["kieu_di"], so_thich=ts_moi["so_thich"],
                them_diem=tuple(_ten(bang, i) for i in them))
    khung = xep(bang, ts, giu, frozenset(loai))
    if kiem_khung(bang, khung):
        khung = xep(bang, ts, None, frozenset(loai))
    return khung


def _lua_chon_thay(bang: Bang, khung: dict, them: list[str], loai: list[str], cu: str) -> list[str]:
    """D6: 2–3 điểm cùng cụm với điểm cũ, hợp sở thích, chưa có trong lịch, không thuộc `loai`, đặt được vào đúng chỗ điểm cũ (đúng luật)."""
    ngay, buoi = _vi_tri(khung)[cu]
    st = khung["tham_so"]["so_thich"] or "di_tich"
    co = set(diem_trong_khung(khung))
    k0 = copy.deepcopy(khung)
    _go(k0, cu)
    out = []
    for cum_cung in (True, False):
        for d in bang.diem:
            i = d["id"]
            if i in co or i in loai or i == cu or i in out or st not in d["loai"] or (d["cum"] == bang.theo_id[cu]["cum"]) != cum_cung:
                continue
            k, _ = _thu_dat(bang, k0, [x for x in them if x != cu], i, [(ngay, buoi)])
            if k is not None:
                out.append(i)
            if len(out) == MAX_LUA_CHON:
                return out
        if len(out) >= 2:
            break
    return out


def the_chon(bang: Bang, cu: str, lua_chon: list[str], cau_goc: str) -> dict:
    """Dữ liệu thẻ chọn (D6) — nút chỉ chứa id code đưa (≥ 1 điểm thay: hết điểm thì không có thẻ, B166); thêm nút "Bỏ điểm này, không thay"."""
    return {"loai": "sua_chon", "cau_goc": cau_goc, "cu": cu, "ten_cu": _ten(bang, cu),
            "lua_chon": [{"gia_tri": i, "nhan": _ten(bang, i)} for i in lua_chon] + [{"gia_tri": "bo", "nhan": "Bỏ điểm này, không thay"}]}


def ap_hanh_dong(bang: Bang, luu: dict, hanh_dong: list[HanhDong], sua_chon: dict | None = None) -> dict:
    """D3–D6: áp hành động trên **bản sao** khung đã lưu ⇒ {khung, luu (trạng thái mới), da_ap, khong_doi, chua_lam, doi_truong, the}.
    `the` khác None ⇒ lượt dừng ở thẻ chọn, khung **không** đổi. `sua_chon` (lượt bấm nút) ⇒ bỏ qua hành động model, áp đúng lựa chọn, không thẻ."""
    luu = copy.deepcopy(luu)
    khung = copy.deepcopy(luu["khung"])
    them, loai = list(luu["them"]), list(luu["loai"])
    ts = dict(luu["tham_so"])
    kq = {"da_ap": [], "khong_doi": [], "chua_lam": [], "doi_truong": [], "the": None}
    if sua_chon is not None:
        moi = sua_chon["moi"]
        hanh_dong = [HanhDong(loai="bo_diem", ten=sua_chon["cu"])] if moi == "bo" else \
            [HanhDong(loai="thay_diem", ten=sua_chon["cu"], ten_moi=moi)]
    hanh_dong = list(hanh_dong)[:MAX_HANH_DONG]
    kq["chua_lam"] = [h.loai for h in hanh_dong[MAX_AP:]]
    hanh_dong = hanh_dong[:MAX_AP]

    def id_cua(ten: str | None) -> str | None:
        return None if ten is None else (ten if ten in bang.theo_id else khop_diem(bang, ten))

    def khong(ten: str | None, ma: str) -> None:
        kq["khong_doi"].append({"diem": ten or "?", "ma_luat": ma})

    # (1) đổi số ngày / tham số (xếp lại một lần, gộp "thêm điểm" không nêu chỗ của cùng lượt vào ưu tiên)
    tham = [h for h in hanh_dong if h.loai in ("doi_so_ngay", "doi_tham_so")]
    if tham:
        ts_moi = dict(ts)
        for h in tham:
            for f in TRUONG_SUA:
                v = getattr(h, f, None)
                if v is None:
                    continue
                v = None if (f == "so_thich" and v == "bo") else v
                if v != ts_moi[f]:  # D5: chỉ nhận trường khác giá trị đã lưu
                    kq["doi_truong"].append((f, ts_moi[f], v))
                    ts_moi[f] = v
        ts_moi["so_ngay_tam"] = False
        them_cung = [h for h in hanh_dong if h.loai == "them_diem" and h.ngay is None and h.buoi is None]
        for h in them_cung:
            i = id_cua(h.ten)
            if i is not None and i not in them:
                them.append(i)
                loai = [x for x in loai if x != i]
        if kq["doi_truong"] or them_cung:
            khung = _xep_lai(bang, {**luu, "khung": khung}, ts_moi, them, loai)
            co = set(diem_trong_khung(khung))
            for h in them_cung:
                i = id_cua(h.ten)
                (kq["da_ap"].append({"loai": "them_diem", "diem": i, **dict(zip(("ngay", "buoi"), _vi_tri(khung)[i]))}) if i in co
                 else khong(h.ten, "ngoai_bang" if i is None else "het_suat"))
        if kq["doi_truong"]:  # điền lại đúng giá trị cũ ⇒ không tính là đã đổi (D5)
            kq["da_ap"] += [{"loai": h.loai, **{f: getattr(h, f) for f in TRUONG_SUA if getattr(h, f, None) is not None}} for h in tham]
        ts = ts_moi
        luu["da_noi"] = sorted(set(luu["da_noi"]) | {f for f, _, _ in kq["doi_truong"]})
        hanh_dong = [h for h in hanh_dong if h not in tham and h not in them_cung]
    # (2) sửa trực tiếp trên khung (giữ chỗ mọi điểm khác)
    for h in hanh_dong:
        i = id_cua(h.ten)
        if h.loai == "bo_diem":
            if i is None or i not in _vi_tri(khung):
                khong(h.ten if i is None else _ten(bang, i), "ngoai_bang" if i is None else "khong_co_trong_lich")
                continue
            _go(khung, i)
            loai.append(i)
            them = [x for x in them if x != i]
            kq["da_ap"].append({"loai": "bo_diem", "diem": i})
        elif h.loai == "them_diem":
            if i is None:
                khong(h.ten, "ngoai_bang")
                continue
            if i in _vi_tri(khung):
                khong(_ten(bang, i), "da_co_trong_lich")
                continue
            loai = [x for x in loai if x != i]
            k, cho = _thu_dat(bang, khung, them, i, _cac_cho(khung, h.ngay, h.buoi))
            if k is None:
                khong(_ten(bang, i), _ma_cho(bang, khung, i, h.buoi))
                continue
            khung, them = k, them + [i]
            kq["da_ap"].append({"loai": "them_diem", "diem": i, "ngay": cho[0], "buoi": cho[1]})
        elif h.loai == "doi_buoi":
            vt = _vi_tri(khung)
            if i is None:
                khong(h.ten, "ngoai_bang")
                continue
            ngay = h.ngay if h.ngay is not None else (vt[i][0] if i in vt else None)
            if ngay is None or h.buoi is None:
                khong(_ten(bang, i), "thieu_cho")
                continue
            if i in vt and vt[i] == (ngay, h.buoi):  # đã ở đúng chỗ (vd sau khi đổi chỗ với điểm kia)
                kq["da_ap"].append({"loai": "doi_buoi", "diem": i, "ngay": ngay, "buoi": h.buoi})
                continue
            k = copy.deepcopy(khung)
            cu = vt.get(i)
            if cu is not None:
                _go(k, i)
            o_kia = [x for x in (next((ng for ng in k["ngay"] if ng["ngay"] == ngay), {"buoi": {}})["buoi"].get(h.buoi, []))]
            if cu is not None and len(o_kia) == 1:  # chỗ đích có một điểm ⇒ đổi chỗ hai điểm
                _go(k, o_kia[0])
                _dat(k, o_kia[0], *cu)
            k2, _ = _thu_dat(bang, k, them if cu is not None else them + [i], i, [(ngay, h.buoi)])
            if k2 is None:
                khong(_ten(bang, i), _ma_cho(bang, khung, i, h.buoi))
                continue
            khung = k2
            if cu is None:
                them.append(i)
                loai = [x for x in loai if x != i]
            kq["da_ap"].append({"loai": "doi_buoi", "diem": i, "ngay": ngay, "buoi": h.buoi})
        elif h.loai == "thay_diem":
            vt = _vi_tri(khung)
            if i is None or i not in vt:
                khong(h.ten if i is None else _ten(bang, i), "ngoai_bang" if i is None else "khong_co_trong_lich")
                continue
            if h.ten_moi is None:  # D6: không nói thay bằng gì ⇒ thẻ chọn (khung không đổi lượt này)
                if sua_chon is not None:
                    continue
                lua_chon = _lua_chon_thay(bang, khung, them, loai, i)
                if not lua_chon:  # B166 (bộ kín mô phỏng 0 USD của C, K-S2): thẻ chỉ có nút Bỏ là thẻ rỗng ⇒ không thẻ, ghi "Không đổi được"
                    khong(_ten(bang, i), "het_diem_thay")
                    continue
                kq["the"] = {"cu": i, "lua_chon": lua_chon}
                return {**kq, "khung": copy.deepcopy(luu["khung"]), "luu": {**luu, "the_chon": kq["the"]}}
            j = id_cua(h.ten_moi)
            if j is None:
                khong(h.ten_moi, "ngoai_bang")
                continue
            if j in vt:
                khong(_ten(bang, j), "da_co_trong_lich")
                continue
            k = copy.deepcopy(khung)
            _go(k, i)
            them_k = [x for x in them if x != i]
            k2, _ = _thu_dat(bang, k, them_k, j, [vt[i]])
            if k2 is None:
                khong(_ten(bang, j), _ma_cho(bang, khung, j, vt[i][1]))
                continue
            khung, them = k2, them_k + [j]
            loai = [x for x in loai if x not in (j,)] + [i]
            kq["da_ap"].append({"loai": "thay_diem", "diem": i, "moi": j})
    _dong_bo(bang, khung, them)
    khung["khong_xep"] = [k for k in khung["khong_xep"] if k["ma_luat"] in ("vuot_ngan_sach",)] if not tham else khung["khong_xep"]
    khung["tham_so"]["so_ngay_tam"] = False
    luu.update(tham_so=copy.deepcopy(khung["tham_so"]), khung=copy.deepcopy(khung), them=them, loai=loai, the_chon=None)
    return {**kq, "khung": khung, "luu": luu}


def _nhan_gia_tri(f: str, v) -> str:
    return "không đặt" if v is None else GIA_TRI[f].get(v, str(v))


def khoi_sua(bang: Bang, kq: dict) -> str:
    """D7: khối "Đã đổi / Không đổi được / Chưa làm" do code nối (mỗi ý một dòng, nhãn cố định)."""
    dong = []
    for a in kq["da_ap"]:
        t = a["loai"]
        if t == "bo_diem":
            dong.append(f"Đã bỏ {_ten(bang, a['diem'])}.")
        elif t == "them_diem":
            dong.append(f"Đã thêm {_ten(bang, a['diem'])} (ngày {a['ngay']}, buổi {NHAN_BUOI[a['buoi']].lower()}).")
        elif t == "doi_buoi":
            dong.append(f"Đã dời {_ten(bang, a['diem'])} sang buổi {NHAN_BUOI[a['buoi']].lower()} ngày {a['ngay']}.")
        elif t == "thay_diem":
            dong.append(f"Đã thay {_ten(bang, a['diem'])} bằng {_ten(bang, a['moi'])}.")
    dong += [f"Đã đổi {NHAN_TRUONG[f].lower()}: {_nhan_gia_tri(f, cu)} → {_nhan_gia_tri(f, moi)}." for f, cu, moi in kq["doi_truong"]]
    dong += ["Không đổi được: " + CAU_KHONG_DOI[k["ma_luat"]].format(diem=k["diem"]) for k in kq["khong_doi"]]
    dong += [f"Chưa làm: {NHAN_HANH_DONG[t]} — bạn nhắn tiếp nhé." for t in kq["chua_lam"]]
    if kq["da_ap"] and not kq["doi_truong"]:
        dong.append("Giữ nguyên: các buổi khác.")
    return "" if not dong else TIEU_DE_SUA + "\n" + "\n".join(f"- {d}" for d in dong)
