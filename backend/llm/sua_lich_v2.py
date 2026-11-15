"""Sửa lịch bằng lời trên lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-sua-lich-v2-plan.md`; giữ D1–D11 của plan 05/11).

Model chọn **hành động có tên** (`HanhDong`); **code** áp tối đa `MAX_AP` / lượt. Mỗi hành động = một lần **xếp lại** bằng `xep_v2` với
`giu` (mọi điểm ban ngày không bị chạm giữ đúng ngày / buổi) + `loai` (điểm đã bỏ không quay lại) — giờ gợi ý, luật cụm, quỹ phút, mùa, mưa
đều do đúng một bộ xếp tính; khung mới chỉ được nhận khi `kiem_khung_v2` = 0 lỗi, không thì giữ khung cũ + lý do. Hàm thuần — không mạng,
không SDK. Trạng thái lưu của cuộc (`luu`): {tham_so, ngay_di, mua, khung, loai} — chỉ dữ liệu code dựng (không chữ người dùng).
"""
import copy
import re
import unicodedata
import datetime as dt
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from llm import lich_trinh_v2 as v2
from llm.do_so import ngay_tu_cau
from llm.hoi_lai import NGAY_DI_TOI_DA
from llm.lich_trinh import chuan_ten

MAX_AP = 2
MAX_HANH_DONG = 3  # ý thứ 3 trở đi ⇒ "Chưa làm"
MAX_LUA_CHON = 3
SoThich = Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"]


class HanhDong(BaseModel):
    """Một hành động sửa. `ten` = điểm bị chạm (bỏ / thêm / thay / dời); `ten_moi` = điểm thay vào; `ngay` / `buoi` = chỗ muốn đặt.
    `doi_tham_so` chỉ mang trường người dùng nói muốn đổi. `doi_hang_o` (plan 2026-11-15-sua-lich-hang-cho-o): `ngan_sach` = mức hạng chỗ ở
    người dùng NÊU RÕ; xin đổi hạng mà không nêu hạng ⇒ để trống ⇒ code nói "bạn nói rõ hạng" (không đoán mức).
    `doi_ngay_di` (plan 2026-11-15-sua-lich-ngay-di) KHÔNG có trường: ngày do code đọc từ chữ người dùng (`ngay_di_moi`) — model không viết ngày."""
    model_config = ConfigDict(extra="forbid")
    loai: Literal["bo_diem", "them_diem", "thay_diem", "doi_buoi", "doi_so_ngay", "doi_tham_so", "doi_hang_o", "doi_ngay_di"]
    ten: str | None = Field(default=None, max_length=80)
    ten_moi: str | None = Field(default=None, max_length=80)
    ngay: int | None = Field(default=None, ge=1, le=5)
    buoi: Literal["sang", "chieu"] | None = None
    so_ngay: int | None = Field(default=None, ge=1, le=5)
    kieu_di: Literal["nhe_nhang", "can_bang", "kham_pha"] | None = None
    so_thich: list[SoThich] | None = Field(default=None, max_length=2)
    tre_em: int | None = Field(default=None, ge=0, le=6)  # "đi cùng trẻ nhỏ" ⇒ ≥ 1; "không có trẻ em" ⇒ 0
    lon_tuoi: bool | None = None  # "có người lớn tuổi"
    ngan_sach: Literal["binh_dan", "vua", "cao"] | None = None  # khoá của `luu_tru_lich.MUC_NGAN_SACH`


NHAN_HANH_DONG = {"bo_diem": "bỏ điểm", "them_diem": "thêm điểm", "thay_diem": "thay điểm", "doi_buoi": "dời buổi",
                  "doi_so_ngay": "đổi số ngày", "doi_tham_so": "đổi kiểu lịch", "doi_hang_o": "đổi hạng chỗ ở", "doi_ngay_di": "đổi ngày đi"}
NHAN_BUOI = {"sang": "sáng", "chieu": "chiều"}
CAU_KHONG_DOI = {
    "ngoai_bang": "«{diem}» chưa có trong danh sách điểm của lịch.",
    "khong_co_trong_lich": "{diem} không có trong lịch hiện tại.",
    "da_co_trong_lich": "{diem} đã có trong lịch.",
    "khong_buoi_hop_le": "{diem} không đi được vào buổi đó.",
    "khong_hop_luat": "{diem} đặt ở chỗ đó sẽ làm lịch phạm luật xếp (giờ mở cửa / cụm xa / quá dày) nên mình chưa đổi.",
    "thieu_cho": "Chưa rõ ngày / buổi để dời {diem}.",
    "het_diem_thay": "Không còn điểm phù hợp để thay {diem} (đặt được vào đúng chỗ đó) nên mình giữ nguyên.",
    # đổi hạng chỗ ở: {diem} = tên mức ("2–3 sao"…)
    "hang_chua_ro": "hạng chỗ ở — bạn nói rõ 1 sao / đạt chuẩn, 2–3 sao hay 4–5 sao thì mình đổi.",
    "hang_dang_dung": "Lịch đang gợi ý chỗ ở hạng {diem} rồi.",
    "hang_khong_co": "Khu chỗ ở của lịch này chưa có cơ sở hạng {diem} trong danh mục nên mình giữ nguyên.",
    "khong_muc_o": "Lịch này không có mục gợi ý chỗ ở (lịch 1 ngày) nên không có hạng để đổi.",
    # đổi ngày đi: {diem} = ngày dd/mm
    "ngay_chua_ro": "ngày đi — bạn nói một ngày cụ thể (ví dụ 20/12, hoặc thứ Bảy tuần sau) thì mình đổi.",
    "ngay_khong_co": "Ngày bạn nêu không có trong lịch nên mình chưa đổi ngày đi.",
    "ngay_ngoai_han": "Mình chỉ xếp được ngày đi từ hôm nay tới 180 ngày nữa nên chưa đổi sang {diem}.",
    "ngay_dang_dung": "Lịch đang đi từ ngày {diem} rồi.",
    "ngay_pham_luat": "Đi từ {diem} thì lịch không xếp được đúng luật (giờ mở cửa / cụm xa) nên mình giữ ngày cũ.",
}


def ten_cua_diem(bang: v2.BangV2, id_: str) -> str:
    return bang.theo_id[id_]["ten"]


def khop_ten(bang: v2.BangV2, ten: str | None) -> str | None:
    """Tên người dùng / model nêu ⇒ id điểm của bảng: id nguyên văn, hoặc tên / tên khác khớp NGUYÊN tên sau chuẩn hoá (NFC, casefold, bỏ
    hậu tố " Huế"); không khớp ⇒ None (không đoán gần đúng)."""
    if not ten:
        return None
    if ten in bang.theo_id:
        return ten
    t = chuan_ten(ten)
    dung = next((d["id"] for d in bang.diem if t in (chuan_ten(x) for x in v2.ten_cua(d))), None)
    if dung is not None or len(t.split()) < 2:
        return dung
    # tên ngắn ("Quốc Học" ⇒ "Trường Quốc Học Huế"): nhận khi nằm trong ĐÚNG MỘT điểm của bảng (≥ 2 chữ — Q3 pilot 14/11); nhiều điểm ⇒ không đoán
    gan = {d["id"] for d in bang.diem for x in v2.ten_cua(d) if f" {t} " in f" {chuan_ten(x)} "}
    return gan.pop() if len(gan) == 1 else None


# Rào sau lần hiểu ý (C 15/11, lỗi thứ hạng 2 "nói chắc sai"): "đi từ ngày 20/12" từng ra hành động đổi số ngày 3 ⇒ 1 và báo "Đã đổi" (đếm
# `report_agent/2026-11-12_ra_khoang_cach/c_dem_sua_lich_truong.md`). Code chỉ nhận đổi số ngày khi CON SỐ có trong chữ người dùng gõ, đứng TRƯỚC chữ
# "ngày" (số trong một ngày tháng như "ngày 20/12" không tính), hoặc là số tương đối "thêm / bớt k ngày" khớp số ngày hiện tại ± k. Thiếu số ⇒ không nhận.
_SO_CHU = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "tư": 4, "năm": 5, "sáu": 6}
_SO = r"(\d+|một|hai|ba|bốn|tư|năm|sáu)"
_N_NGAY = re.compile(rf"(?<![\w/.-])(?<!thứ\s){_SO}\s*(?:ngày|hôm|n(?=\s*\d+\s*đ))", re.I)  # "3 ngày", "2 hôm", "4N3Đ"; "thứ hai ngày 20/12" không tính
_THEM = re.compile(rf"(thêm|tăng|kéo dài|nối)\s+(?:thêm\s+)?{_SO}\s*ngày", re.I)
_BOT = re.compile(rf"(bớt|giảm|rút|cắt|bỏ)\s+(?:bớt\s+|đi\s+)?{_SO}\s*(?:ngày|hôm)", re.I)
_BO_NGAY = re.compile(r"bỏ\s+(?:bớt\s+|đi\s+)?ngày\s+(cuối|\d+)", re.I)  # "bỏ ngày cuối", "bỏ ngày 3" (= ngày cuối) ⇒ bớt 1


def _so(x: str) -> int:
    return int(x) if x.isdigit() else _SO_CHU[x.lower()]


def so_ngay_co_trong_cau(cau: str, so_ngay: int | None, hien_tai: int) -> bool:
    """Hành động đổi số ngày ⇒ `so_ngay` mới có căn cứ trong chữ người dùng (tuyệt đối "còn 2 ngày" hoặc tương đối "thêm một ngày")?"""
    if so_ngay is None:
        return False
    t = unicodedata.normalize("NFC", cau)
    if any(_so(m.group(2)) + hien_tai == so_ngay for m in _THEM.finditer(t)) or any(hien_tai - _so(m.group(2)) == so_ngay for m in _BOT.finditer(t)):
        return True
    if so_ngay == hien_tai - 1 and any(m.group(1).lower() == "cuối" or int(m.group(1)) == hien_tai for m in _BO_NGAY.finditer(t)):
        return True
    tuong_doi = {m.start(2) for r in (_THEM, _BOT) for m in r.finditer(t)}  # số sau "thêm / bớt" là số tương đối, không phải tổng số ngày
    return any(_so(m.group(1)) == so_ngay for m in _N_NGAY.finditer(t) if m.start(1) not in tuong_doi)


def loc_hanh_dong(hanh_dong: list, cau: str, luu: dict) -> tuple[list, int]:
    """(hành động giữ, số hành động đổi số ngày bị bỏ vì không có căn cứ trong câu). Hành động khác giữ nguyên."""
    hien_tai = luu["khung"]["tham_so"]["so_ngay"]
    giu = [h for h in hanh_dong if h.loai != "doi_so_ngay" or so_ngay_co_trong_cau(cau, h.so_ngay, hien_tai)]
    return giu, len(hanh_dong) - len(giu)


def luu_tu_lich(khung: dict, ngay_di: str | None, mua: dict | None) -> dict:
    """Trạng thái lưu sau một lượt lịch đạt (bản sao sâu). `mua` {ngày ISO: %} của dự báo đã dùng để xếp."""
    return {"tham_so": copy.deepcopy(khung["tham_so"]), "ngay_di": ngay_di,
            "mua": {(k.isoformat() if isinstance(k, dt.date) else k): v for k, v in (mua or {}).items()},
            "khung": copy.deepcopy(khung), "loai": []}


def _ts(tham_so: dict) -> v2.ThamSoV2:
    return v2.ThamSoV2(so_ngay=tham_so["so_ngay"], tre_em=tham_so["tre_em"], lon_tuoi=tham_so["lon_tuoi"], kieu_di=tham_so["kieu_di"],
                       so_thich=tuple(tham_so["so_thich"]), nguoi_lon=tham_so.get("nguoi_lon"),
                       ngan_sach=tham_so.get("ngan_sach"))


def _vi_tri(khung: dict) -> dict[str, tuple[int, str]]:
    return {i: (ng["ngay"], b) for ng in khung["ngay"] for b in v2.BUOI_NGAY for i in ng["buoi"][b]}


def _xep(bang, luu: dict, ts: v2.ThamSoV2, giu: dict | None, loai) -> dict:
    ngay = dt.date.fromisoformat(luu["ngay_di"]) if luu["ngay_di"] else None
    mua = {dt.date.fromisoformat(k): v for k, v in luu["mua"].items()} or None
    return v2.xep_v2(bang, ts, ngay_bat_dau=ngay, mua=mua, giu=giu, loai=frozenset(loai))


def _dung_luat(bang, khung: dict) -> bool:
    return not v2.kiem_khung_v2(bang, khung)


def _cho_thu(bang, khung: dict, id_: str, ngay: int | None, buoi: str | None) -> list[tuple[int, str]]:
    """Chỗ ứng viên theo ngày / buổi người dùng nói, chỉ buổi điểm đi được; buổi trống trước."""
    d = bang.theo_id[id_]
    cho = [(ng["ngay"], b) for ng in khung["ngay"] for b in v2.BUOI_NGAY
           if (ngay is None or ng["ngay"] == ngay) and (buoi is None or b == buoi) and b in d["buoi"]]
    return sorted(cho, key=lambda c: bool(next(ng for ng in khung["ngay"] if ng["ngay"] == c[0])["buoi"][c[1]]))


def _thu_giu(bang, luu: dict, ts, giu: dict, loai, can: str | None = None) -> dict | None:
    """Xếp lại với `giu`; nhận khi đúng luật và (nếu có) điểm `can` thật sự có trong khung."""
    k = _xep(bang, luu, ts, giu, loai)
    if not _dung_luat(bang, k) or (can is not None and can not in _vi_tri(k)):
        return None
    return k


def _lua_chon_thay(bang, luu: dict, ts, khung: dict, loai: list[str], cu: str) -> list[str]:
    """2–3 điểm đặt được vào đúng chỗ điểm cũ (đúng luật): cùng cụm trước, hợp sở thích trước, chưa có trong lịch, không thuộc `loai`."""
    vt = _vi_tri(khung)
    cho = vt[cu]
    giu0 = {i: v for i, v in vt.items() if i != cu}
    st = set(ts.so_thich)
    ung = [d for d in bang.diem if d["id"] not in vt and d["id"] not in loai and d["id"] != cu and cho[1] in d["buoi"]]
    ung.sort(key=lambda d: (d["cum"] != bang.theo_id[cu]["cum"], bool(st) and not (st & set(d["loai"]))))  # sort ổn định: thứ tự bảng
    out = []
    for d in ung:
        if _thu_giu(bang, luu, ts, {**giu0, d["id"]: cho}, loai + [cu], can=d["id"]) is not None:
            out.append(d["id"])
        if len(out) == MAX_LUA_CHON:
            break
    return out


THU = ("thứ Hai", "thứ Ba", "thứ Tư", "thứ Năm", "thứ Sáu", "thứ Bảy", "Chủ nhật")


def _dd_mm(ngay: dt.date, hom_nay: dt.date | None = None) -> str:
    return f"{ngay.day}/{ngay.month}" + (f"/{ngay.year}" if hom_nay is not None and ngay.year != hom_nay.year else "")


def ngay_di_moi(cau: str, hom_nay: dt.date) -> dict:
    """Ngày đi mới đọc từ CHỮ NGƯỜI DÙNG (`do_so.ngay_tu_cau`) + hạn của biểu mẫu (hôm nay … +180 ngày) ⇒ {"ngay": date} hoặc {"ma", "diem"}
    (khoá + chữ điền của `CAU_KHONG_DOI`). Nơi gọi (`len_ke_hoach.hieu_va_ap`) lấy dự báo cho ngày đó rồi đưa cả gói vào `ap(ngay_moi=…)`."""
    ngay = ngay_tu_cau(cau, hom_nay)
    if isinstance(ngay, str):
        return {"ma": ngay, "diem": None}
    if not hom_nay <= ngay <= hom_nay + dt.timedelta(days=NGAY_DI_TOI_DA):
        return {"ma": "ngay_ngoai_han", "diem": _dd_mm(ngay, hom_nay)}
    return {"ngay": ngay}


def ten_muc_o(ngan_sach: str) -> str:
    return v2.ltl.TEN_MUC[v2.ltl.MUC_NGAN_SACH[ngan_sach]]


def ly_do_giu_hang(bang: v2.BangV2, luu_tru: dict | None, khung: dict, moi: str | None) -> str | None:
    """Mã lý do KHÔNG đổi hạng chỗ ở (khoá của `CAU_KHONG_DOI`), None = đổi được. Thử bằng đúng hàm dựng ô "Nơi ở" của lịch: mức mới phải ra
    cơ sở THUỘC mức đó — `chon_co_so` tự lùi về mọi hạng khi mức trống, lùi lặng lẽ ở đây thành "nói đã đổi mà hạng không đổi"."""
    if moi is None:
        return "hang_chua_ro"
    o = v2.o_dau_khung(luu_tru, bang, khung, moi) if luu_tru is not None else None
    if o is None:
        return "khong_muc_o"
    if moi == khung["tham_so"].get("ngan_sach"):
        return "hang_dang_dung"
    if any(v2.ltl.MUC_HANG[c["xep_hang"]] != v2.ltl.MUC_NGAN_SACH[moi] for c in o["co_so"]):
        return "hang_khong_co"
    return None


def ap(bang: v2.BangV2, luu: dict, hanh_dong: list[HanhDong], sua_chon: dict | None = None, luu_tru: dict | None = None,
       ngay_moi: dict | None = None) -> dict:
    """Áp hành động trên **bản sao** khung đã lưu ⇒ {khung, luu, da_ap, khong_doi, chua_lam, doi_truong, the}.
    `the` khác None ⇒ lượt dừng ở thẻ chọn, khung KHÔNG đổi. `sua_chon` {cu, moi} (bấm nút của thẻ) ⇒ bỏ qua hành động model.
    `luu_tru` = bảng lưu trú đang dùng (None khi cờ nơi ở tắt) — chỉ hành động `doi_hang_o` cần.
    `ngay_moi` = gói của `ngay_di_moi` (+ `mua` {ngày ISO: %} dự báo cho ngày mới, `co_du_bao`) — chỉ `doi_ngay_di` cần; thiếu ⇒ "chưa rõ ngày".
    Đổi ngày đi: thử GIỮ mọi điểm ở chỗ cũ với ngày mới; phạm luật ⇒ xếp lại (điểm đã bỏ không quay lại); kết quả `kq["ngay_di"]`."""
    luu = copy.deepcopy(luu)
    khung = copy.deepcopy(luu["khung"])
    loai = list(luu["loai"])
    ts = _ts(khung["tham_so"])
    kq = {"da_ap": [], "khong_doi": [], "chua_lam": [], "doi_truong": [], "the": None, "ngay_di": None}
    if sua_chon is not None:
        hanh_dong = [HanhDong(loai="bo_diem", ten=sua_chon["cu"])] if sua_chon["moi"] == "bo" else \
            [HanhDong(loai="thay_diem", ten=sua_chon["cu"], ten_moi=sua_chon["moi"])]
    hanh_dong = list(hanh_dong)[:MAX_HANH_DONG]
    # review E M-1: "thay" không nói thay bằng gì ⇒ lượt chỉ dừng ở thẻ chọn; mọi hành động khác của lượt vào "Chưa làm" (không áp nửa chừng
    # rồi mất khi thẻ trả khung cũ). Không có điểm thay ⇒ "Không đổi được" và các hành động khác đi tiếp như thường.
    if sua_chon is None:
        for h in hanh_dong:
            i = khop_ten(bang, h.ten)
            if h.loai == "thay_diem" and h.ten_moi is None and i is not None and i in _vi_tri(khung):
                lua_chon = _lua_chon_thay(bang, luu, ts, khung, loai, i)
                if lua_chon:
                    kq["the"] = {"cu": i, "ten_cu": ten_cua_diem(bang, i),
                                 "lua_chon": [{"gia_tri": j, "nhan": ten_cua_diem(bang, j)} for j in lua_chon] + [{"gia_tri": "bo", "nhan": "Bỏ điểm này, không thay"}]}
                    kq["chua_lam"] = [x.loai for x in hanh_dong if x is not h]
                    return {**kq, "khung": copy.deepcopy(luu["khung"]), "luu": luu}
                break
    kq["chua_lam"] = [h.loai for h in hanh_dong[MAX_AP:]]

    def khong(ten: str | None, ma: str) -> None:
        kq["khong_doi"].append({"diem": ten or "?", "ma_luat": ma})

    for h in hanh_dong[:MAX_AP]:
        vt = _vi_tri(khung)
        i = khop_ten(bang, h.ten)
        if h.loai in ("doi_so_ngay", "doi_tham_so"):
            moi = {"so_ngay": h.so_ngay, "kieu_di": h.kieu_di, "so_thich": None if h.so_thich is None else tuple(h.so_thich),
                   "tre_em": h.tre_em, "lon_tuoi": h.lon_tuoi}
            doi = {f: v for f, v in moi.items() if v is not None and v != getattr(ts, f)}  # chỉ trường khác giá trị đang dùng
            if not doi:
                continue
            ts_moi = v2.ThamSoV2(**{**ts.__dict__, **doi})
            st = set(ts_moi.so_thich)
            giu = {j: v for j, v in vt.items() if v[0] <= ts_moi.so_ngay and (not st or st & set(bang.theo_id[j]["loai"]))}
            k = _thu_giu(bang, luu, ts_moi, giu, loai) or _xep(bang, luu, ts_moi, None, loai)  # giữ làm phạm luật ⇒ xếp lại không giữ
            if not _dung_luat(bang, k):
                khong(NHAN_HANH_DONG[h.loai], "khong_hop_luat")
                continue
            kq["doi_truong"] += [(f, getattr(ts, f), v) for f, v in doi.items()]
            khung, ts = k, ts_moi
            kq["da_ap"].append({"loai": h.loai})
        elif h.loai == "doi_ngay_di":
            nm = ngay_moi or {"ma": "ngay_chua_ro", "diem": None}
            if "ma" in nm:
                khong(nm["diem"], nm["ma"])
                continue
            moi, cu = nm["ngay"], luu["ngay_di"]
            if moi.isoformat() == cu:
                khong(_dd_mm(moi), "ngay_dang_dung")
                continue
            luu_moi = {**luu, "ngay_di": moi.isoformat(), "mua": dict(nm.get("mua") or {})}
            k = _thu_giu(bang, luu_moi, ts, vt, loai) or _xep(bang, luu_moi, ts, None, loai)  # giữ chỗ phạm luật (thứ đóng cửa…) ⇒ xếp lại
            if not _dung_luat(bang, k):
                khong(_dd_mm(moi), "ngay_pham_luat")
                continue
            vt_moi = _vi_tri(k)
            toi = lambda kh: {j for ng in kh["ngay"] for j in ng["buoi"]["toi"]}  # noqa: E731
            kq["ngay_di"] = {"cu": cu, "moi": moi.isoformat(), "co_du_bao": bool(nm.get("co_du_bao")),
                             "doi_cho": sorted(j for j in vt if j in vt_moi and vt_moi[j] != vt[j]),
                             "ra": sorted((set(vt) - set(vt_moi)) | (toi(khung) - toi(k))), "vao": sorted((set(vt_moi) - set(vt)) | (toi(k) - toi(khung)))}
            luu, khung = luu_moi, k
            kq["da_ap"].append({"loai": "doi_ngay_di"})
        elif h.loai == "doi_hang_o":  # hạng không vào bộ xếp ⇒ KHÔNG xếp lại: điểm, ngày, buổi giữ nguyên; chỉ ô "Nơi ở" đổi
            ma = ly_do_giu_hang(bang, luu_tru, khung, h.ngan_sach)
            if ma is not None:
                khong(None if h.ngan_sach is None else ten_muc_o(h.ngan_sach), ma)
                continue
            kq["doi_truong"].append(("ngan_sach", ts.ngan_sach, h.ngan_sach))
            ts = v2.ThamSoV2(**{**ts.__dict__, "ngan_sach": h.ngan_sach})
            khung = {**khung, "tham_so": {**khung["tham_so"], "ngan_sach": h.ngan_sach}}
            kq["da_ap"].append({"loai": "doi_hang_o"})
        elif h.loai == "bo_diem":
            toi = {j for ng in khung["ngay"] for j in ng["buoi"]["toi"]}
            if i is None or (i not in vt and i not in toi):
                khong(h.ten if i is None else ten_cua_diem(bang, i), "ngoai_bang" if i is None else "khong_co_trong_lich")
                continue
            k = _thu_giu(bang, luu, ts, {j: v for j, v in vt.items() if j != i}, loai + [i])
            if k is None:
                khong(ten_cua_diem(bang, i), "khong_hop_luat")
                continue
            khung, loai = k, loai + [i]
            kq["da_ap"].append({"loai": "bo_diem", "diem": i})
        elif h.loai in ("them_diem", "doi_buoi"):
            if i is None:
                khong(h.ten, "ngoai_bang")
                continue
            if h.loai == "them_diem" and i in vt:
                khong(ten_cua_diem(bang, i), "da_co_trong_lich")
                continue
            if h.loai == "doi_buoi" and h.buoi is None:
                khong(ten_cua_diem(bang, i), "thieu_cho")
                continue
            ngay = h.ngay if h.ngay is not None else (vt[i][0] if h.loai == "doi_buoi" and i in vt else None)
            if h.buoi is not None and h.buoi not in bang.theo_id[i]["buoi"]:
                khong(ten_cua_diem(bang, i), "khong_buoi_hop_le")
                continue
            giu0 = {j: v for j, v in vt.items() if j != i}
            k = None
            for cho in _cho_thu(bang, khung, i, ngay, h.buoi):
                giu = {**giu0, i: cho}
                o_kia = [j for j, v in giu0.items() if v == cho]
                if h.loai == "doi_buoi" and i in vt and len(o_kia) == 1:  # chỗ đích có đúng một điểm ⇒ đổi chỗ hai điểm
                    giu[o_kia[0]] = vt[i]
                k = _thu_giu(bang, luu, ts, giu, [x for x in loai if x != i], can=i)
                if k is not None:
                    break
            the_cho = None
            if k is None and h.loai == "them_diem":
                # buổi đã kín (lịch bản 2 thường đủ quỹ phút) ⇒ thế chỗ một điểm lấp / ngoài sở thích ở đúng buổi đó; câu báo nói rõ điểm bị thế
                st = set(ts.so_thich)
                for cho in _cho_thu(bang, khung, i, ngay, h.buoi):
                    o = sorted((j for j, v in giu0.items() if v == cho), key=lambda j: bool(st & set(bang.theo_id[j]["loai"])))
                    for z in o:
                        k = _thu_giu(bang, luu, ts, {**{j: v for j, v in giu0.items() if j != z}, i: cho}, [x for x in loai if x != i], can=i)
                        if k is not None:
                            the_cho = z
                            break
                    if k is not None:
                        break
            if k is None:
                khong(ten_cua_diem(bang, i), "khong_hop_luat")
                continue
            khung, loai = k, [x for x in loai if x != i]
            kq["da_ap"].append({"loai": h.loai, "diem": i, "ngay": _vi_tri(k)[i][0], "buoi": _vi_tri(k)[i][1], "the_cho": the_cho})
        elif h.loai == "thay_diem":
            if i is None or i not in vt:
                khong(h.ten if i is None else ten_cua_diem(bang, i), "ngoai_bang" if i is None else "khong_co_trong_lich")
                continue
            if h.ten_moi is None:  # không nói thay bằng gì ⇒ thẻ chọn (khung không đổi lượt này)
                lua_chon = _lua_chon_thay(bang, luu, ts, khung, loai, i)
                if not lua_chon:
                    khong(ten_cua_diem(bang, i), "het_diem_thay")
                    continue
                kq["the"] = {"cu": i, "ten_cu": ten_cua_diem(bang, i),
                             "lua_chon": [{"gia_tri": j, "nhan": ten_cua_diem(bang, j)} for j in lua_chon] + [{"gia_tri": "bo", "nhan": "Bỏ điểm này, không thay"}]}
                return {**kq, "khung": copy.deepcopy(luu["khung"]), "luu": luu}
            j = khop_ten(bang, h.ten_moi)
            if j is None:
                khong(h.ten_moi, "ngoai_bang")
                continue
            if j in vt:
                khong(ten_cua_diem(bang, j), "da_co_trong_lich")
                continue
            k = _thu_giu(bang, luu, ts, {**{x: v for x, v in vt.items() if x != i}, j: vt[i]}, [x for x in loai if x != j] + [i], can=j)
            if k is None:
                khong(ten_cua_diem(bang, j), "khong_buoi_hop_le" if vt[i][1] not in bang.theo_id[j]["buoi"] else "khong_hop_luat")
                continue
            khung, loai = k, [x for x in loai if x != j] + [i]
            kq["da_ap"].append({"loai": "thay_diem", "diem": i, "moi": j})
    luu.update(tham_so=copy.deepcopy(khung["tham_so"]), khung=copy.deepcopy(khung), loai=loai)
    return {**kq, "khung": khung, "luu": luu}


def _gia_tri(f: str, v) -> str:
    if f == "tre_em":
        return f"{v} trẻ em"
    if f == "lon_tuoi":
        return "có" if v else "không"
    if f == "so_ngay":
        return f"{v} ngày"
    if f == "ngan_sach":
        return "chưa chọn" if v is None else ten_muc_o(v)
    if f == "kieu_di":
        return {"nhe_nhang": "nhẹ nhàng", "can_bang": "cân bằng", "kham_pha": "khám phá nhiều"}.get(v, str(v))
    return ", ".join(v2.NHAN_LOAI.get(x, x) for x in v) or "không chọn"


def thay_doi(bang: v2.BangV2, kq: dict) -> list[dict]:
    """Khối đầu thẻ lịch (giao diện H1 `lich.thay_doi`): mỗi ý một dòng do CODE viết — {cau, duoc}."""
    out = []
    for a in kq["da_ap"]:
        t = a["loai"]
        if t == "bo_diem":
            out.append(f"Đã bỏ {ten_cua_diem(bang, a['diem'])}.")
        elif t == "them_diem":
            thay = f", thế chỗ {ten_cua_diem(bang, a['the_cho'])}" if a.get("the_cho") else ""
            out.append(f"Đã thêm {ten_cua_diem(bang, a['diem'])} (ngày {a['ngay']}, buổi {NHAN_BUOI[a['buoi']]}{thay}).")
        elif t == "doi_buoi":
            out.append(f"Đã dời {ten_cua_diem(bang, a['diem'])} sang buổi {NHAN_BUOI[a['buoi']]} ngày {a['ngay']}.")
        elif t == "thay_diem":
            out.append(f"Đã thay {ten_cua_diem(bang, a['diem'])} bằng {ten_cua_diem(bang, a['moi'])}.")
    out += [f"Đã đổi {({'so_ngay': 'số ngày', 'kieu_di': 'kiểu đi', 'so_thich': 'sở thích', 'tre_em': 'số trẻ em', 'lon_tuoi': 'người lớn tuổi', 'ngan_sach': 'hạng chỗ ở'})[f]}: "
            f"{_gia_tri(f, cu)} → {_gia_tri(f, moi)}."
            for f, cu, moi in kq["doi_truong"]]
    nd = kq.get("ngay_di")
    if nd:
        moi = dt.date.fromisoformat(nd["moi"])
        out.append(f"Đã đổi ngày đi: {_dd_mm(dt.date.fromisoformat(nd['cu'])) if nd['cu'] else 'chưa chọn'} → {_dd_mm(moi)} ({THU[moi.weekday()]}).")
        if nd["doi_cho"] or nd["ra"] or nd["vao"]:
            phan = [f"{len(nd['doi_cho'])} điểm đổi ngày hoặc buổi" if nd["doi_cho"] else "",
                    "bớt " + ", ".join(ten_cua_diem(bang, j) for j in nd["ra"]) if nd["ra"] else "",
                    "thêm " + ", ".join(ten_cua_diem(bang, j) for j in nd["vao"]) if nd["vao"] else ""]
            out.append("Lịch xếp lại theo ngày mới (thứ trong tuần, mùa, dự báo): " + "; ".join(p for p in phan if p) + ".")
        else:
            out.append("Các điểm trong lịch giữ nguyên chỗ.")
        if not nd["co_du_bao"]:
            out.append("Ngày này chưa có dự báo thời tiết nên lịch chưa xét mưa.")
    dong = [{"cau": c, "duoc": True} for c in out]
    dong += [{"cau": CAU_KHONG_DOI[k["ma_luat"]].format(diem=k["diem"]), "duoc": False} for k in kq["khong_doi"]]
    dong += [{"cau": f"Chưa làm: {NHAN_HANH_DONG[t]} — bạn nhắn tiếp nhé.", "duoc": False} for t in kq["chua_lam"]]
    return dong


# Cổng từ khoá đã thử và BỎ (đo 14/11, `tools/do_cong_tu_sua.py`): bộ chuỗi đã thấy 17 / 19 câu sửa qua cổng, câu diễn đạt lạ 3 / 10 (sàn A
# đặt 8 / 10) ⇒ khi cuộc có lịch đã lưu, lượt nào cũng qua lần "hiểu ý sửa" (rỗng ⇒ đường trả lời thường).


def tin_nhan_hieu(bang: v2.BangV2, luu: dict, cau: str) -> str:
    """Tin nhắn cho lần "hiểu ý sửa": lịch hiện tại (ngày · buổi · tên — dữ liệu code) + tham số + câu người dùng."""
    k, ts = luu["khung"], luu["khung"]["tham_so"]
    dong = [f"Tham số: {ts['so_ngay']} ngày · kiểu đi {ts['kieu_di']} · sở thích {', '.join(ts['so_thich']) or 'không chọn'}", "Lịch hiện tại:"]
    for ng in k["ngay"]:
        for b in v2.BUOI:
            ten = [ten_cua_diem(bang, j) for j in ng["buoi"][b]]
            if ten:
                dong.append(f"- Ngày {ng['ngay']} · {({'sang': 'sáng', 'chieu': 'chiều', 'toi': 'tối'})[b]}: {'; '.join(ten)}")
    trong = {j for ng in k["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    dong += ["", "Điểm khác có thể thêm / thay vào (chép đúng tên khi điền ten / ten_moi): "
             + "; ".join(d["ten"] for d in bang.diem if d["id"] not in trong)]  # điểm trong lịch đã có tên ở trên ⇒ không lặp (bớt token)
    return "\n".join(dong) + "\n\nCâu người dùng: " + cau.strip()


def sua_ap(kq: dict) -> dict:
    """Dữ liệu code của lượt sửa (id điểm, mã luật — không chữ): cho bộ đo so với nhãn và cho log."""
    return {"da_ap": kq["da_ap"], "doi_truong": [[f, cu, moi] for f, cu, moi in kq["doi_truong"]], "ngay_di": kq.get("ngay_di"),
            "khong_doi": kq["khong_doi"], "chua_lam": kq["chua_lam"], "the": None if kq["the"] is None else kq["the"]["cu"]}
