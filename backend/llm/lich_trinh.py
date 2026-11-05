"""Lịch trình gợi ý — phần code thuần (Phase 9 B5, plan `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 `b572443dc9cd`).

Chia việc (spec Phase 9 §3, khung AI FDE §2): **code** chọn + xếp điểm từ bảng điểm User duyệt (D2–D5), dựng khung, khối ghi chú (D4b), dòng
"Mình hiểu" (D12), link bản đồ (D11) và kiểm cuối (D8); **model** chỉ trích trường + viết lời theo khung (D7). Module không gọi mạng, không
import SDK — lõi (`llm/assistant.py`) bọc thành công cụ và lấy đoạn kho cho mỗi điểm (D6).

Khung là dữ liệu có cấu trúc (dict JSON được) để bậc "sửa lịch nhiều lượt" sau B5 dùng lại.
"""
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from urllib.parse import quote

from llm.do_so import do_so_ngay
from llm.hoi_lai import GIA_TRI
from llm.so_tien import tim_so_tien

BUOI = ("sang", "chieu", "toi")
NHAN_BUOI = {"sang": "Sáng", "chieu": "Chiều", "toi": "Tối"}
LOAI_DIEM = {"di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"}
THOI_LUONG = {"ngan", "nua_buoi", None}
# §2b — cụm kề (ghi trước theo vị trí kho ghi; "cùng hướng", không phải đường đi). `nam_xa` không kề cụm nào (cả ngày một cụm).
CUM_KE_GOC = {"kinh_thanh": ("bo_nam", "kim_long", "dong_bien"), "bo_nam": ("an_cuu",), "an_cuu": ("thuy_xuan",),
              "thuy_xuan": ("kim_long", "lang_xa"), "kim_long": ("lang_xa",)}
CUM_KE: dict[str, set[str]] = {}
for _a, _bs in CUM_KE_GOC.items():
    for _b in _bs:
        CUM_KE.setdefault(_a, set()).add(_b)
        CUM_KE.setdefault(_b, set()).add(_a)
CUM_XA = "nam_xa"  # D3 (Quyết 2 của User): chỉ xếp khi so_ngay ≥ 3 hoặc người dùng nêu điểm đó
HAN_CHE = {"nguoi_lon_tuoi", "gia_dinh_tre_em"}  # D4: luôn 1 suất / buổi, ≤ 2 suất / ngày, không buổi tối
GIO_QUAN_THE = "07h00–17h30"  # D5 (a): khung giờ chung của file vé Quần thể (trích đoạn file vé)
MAX_THEM_DIEM = 3
# D5 (a): đoạn file vé Quần thể chứa khung giờ chung — một đoạn cho cả lịch (D6 (i))
VE_NGUON = "travel/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md"
VE_CAU_TIM = "khung giờ mở cửa tham quan Quần thể Di tích Cố đô Huế"
# D1: tham số công cụ = đúng 4 trường lịch trình của B4 D2 (enum) — cùng tập giá trị với `TruongInput`
SoNgay = Literal["1", "2", "3", "4+"]
DiCung = Literal["mot_minh", "cap_doi", "gia_dinh_tre_em", "nguoi_lon_tuoi", "nhom_ban"]
KieuDi = Literal["thong_tha", "day_lich"]
SoThich = Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"]

# D2b — mã luật ⇒ câu cố định (code nối vào khối D4b; model không viết lý do)
CAU_KHONG_XEP = {
    "ngoai_bang": "«{diem}» chưa có trong bảng điểm của mình nên chưa xếp vào lịch.",
    "khong_buoi_hop_le": "{diem} chỉ hợp buổi không phù hợp với người đi cùng nên mình chưa xếp.",
    "het_suat": "{diem} chưa xếp được vì lịch đã kín chỗ — thêm ngày thì mình xếp được.",
    "khong_co_doan_nguon": "{diem} chưa xếp vì mình chưa lấy được tài liệu của điểm này trong kho.",
    "vuot_ngan_sach": "Ngày {diem} chưa xếp — bạn hỏi thêm để mình xếp tiếp nhé.",
}
# D4b (1) — giả định công khai khi trường không bắt buộc bị thiếu; D15 (bản 7) "Trả lời luôn" ⇒ 1 ngày tạm
CAU_GIA_DINH = {
    "so_ngay_tam": "Mình tạm xếp cho 1 ngày — bấm Sửa để đổi.",
    "so_ngay_4": "Bạn chọn từ 4 ngày — mình xếp 4 ngày đầu.",
    "so_thich": "Chưa biết sở thích nên mình gợi ý di tích tiêu biểu, thêm một điểm thiên nhiên mỗi ngày.",
    "kieu_di": "Chưa biết kiểu đi nên mình xếp thong thả, mỗi buổi một điểm.",
    "di_cung": "Chưa biết bạn đi cùng ai nên mình xếp cho người lớn đi được nhiều.",
}
# pilot B160: model bỏ dấu ◦ khi viết lời ⇒ câu cố định nêu thẳng tên điểm lấp (code biết), không dựa vào dấu model phải chép
CAU_THIEU_SO_THICH = "Kho chỉ có {k} điểm hợp sở thích của bạn nên mình thêm điểm di tích tiêu biểu: {ten}."
CAU_CO_THE_DOI = "Giờ mở cửa có thể đã thay đổi — bạn kiểm tra lại trước khi đi."
TIEU_DE_GHI_CHU = "**Ghi chú của lịch**"
MAP_BASE = "https://www.google.com/maps/search/?api=1&query="  # D11: URL tìm kiếm Google Maps (định dạng công khai)


def chuan_ten(text: str) -> str:
    """D2 luật khớp: NFC + casefold + gộp khoảng trắng; bỏ hậu tố " huế" khi phần còn lại ≥ 2 chữ."""
    t = " ".join(unicodedata.normalize("NFC", text).casefold().split())
    if t.endswith(" huế") and len(t[: -len(" huế")].split()) >= 2:
        t = t[: -len(" huế")]
    return t


@dataclass(frozen=True)
class Bang:
    """Bảng điểm User duyệt (`diem_v3.json`): điểm theo thứ tự bảng + khoá khớp tên (mỗi khoá đúng một điểm)."""
    diem: tuple[dict, ...]
    theo_id: dict
    khoa: dict  # tên đã chuẩn hoá ⇒ id
    cum: dict


def nap_bang(path: str | Path) -> Bang:
    """Đọc + kiểm bảng lúc khởi động (D2): trường bắt buộc, giá trị hợp lệ, **mỗi khoá tên trỏ đúng một điểm** — sai ⇒ `ValueError` (không khởi động)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cum, diem = data["cum"], data["diem"]
    theo_id, khoa = {}, {}
    for d in diem:
        missing = {"id", "ten", "cum", "loai", "thoi_luong", "gio_mo_cua", "nguon", "buoi", "quan_the", "luu_y", "ten_khac"} - set(d)
        if missing:
            raise ValueError(f"bảng điểm: {d.get('id')} thiếu {sorted(missing)}")
        if d["id"] in theo_id or d["cum"] not in cum or not set(d["loai"]) <= LOAI_DIEM or d["thoi_luong"] not in THOI_LUONG \
                or not d["buoi"] or not set(d["buoi"]) <= set(BUOI):
            raise ValueError(f"bảng điểm: {d['id']} sai giá trị")
        theo_id[d["id"]] = d
        for ten in (d["id"], d["ten"], *d["ten_khac"]):
            k = chuan_ten(ten)
            if khoa.get(k, d["id"]) != d["id"]:
                raise ValueError(f"bảng điểm: khoá tên trùng «{ten}»")
            khoa[k] = d["id"]
    return Bang(tuple(diem), theo_id, khoa, cum)


def khop_diem(bang: Bang, ten: str) -> str | None:
    """Tên người dùng nêu ⇒ id điểm (khớp **nguyên tên** sau chuẩn hoá, không khớp chuỗi con); không khớp ⇒ None."""
    return bang.khoa.get(chuan_ten(ten))


@dataclass(frozen=True)
class ThamSo:
    """Tham số đã chốt của một lần xếp (giá trị trường B4 D2; `so_ngay` do code chốt theo D15)."""
    so_ngay: str  # "1" | "2" | "3" | "4+"
    di_cung: str | None = None
    kieu_di: str | None = None
    so_thich: str | None = None
    them_diem: tuple[str, ...] = ()
    so_ngay_tam: bool = False  # D15 bản 7: "Trả lời luôn" ⇒ 1 ngày tạm


def chot_so_ngay(truong: dict | None, tu_model: str | None, cau: str) -> tuple[str | None, bool]:
    """D15 (+ D12 (b)): số ngày code dùng ⇒ (giá trị, tạm?); (None, False) = **cần hỏi lại**. Thứ tự: (1) lượt ghép (`truong` từ nút) — không bao
    giờ hỏi lần hai: có `so_ngay` ⇒ dùng, rỗng / thiếu ("Trả lời luôn") ⇒ 1 ngày **tạm**; (2) tham số model, đối chiếu số dò trong câu người
    dùng — lệch ⇒ hỏi; (3) model không gửi ⇒ số dò được (đúng một giá trị); (4) vẫn thiếu ⇒ hỏi."""
    if truong is not None:
        return (truong["so_ngay"], False) if truong.get("so_ngay") else ("1", True)
    do = do_so_ngay(cau)
    if tu_model is not None:
        return (None, False) if do is not None and do != tu_model else (tu_model, False)
    return do, False


def _so_ngay(ts: ThamSo) -> int:
    return 4 if ts.so_ngay == "4+" else int(ts.so_ngay)


def _cum_hop(cum: str, cums: list[str]) -> bool:
    """D4: ≤ 2 cụm / ngày; buổi sau cùng cụm hoặc cụm kề; `nam_xa` cả ngày một cụm."""
    if not cums:
        return True
    if CUM_XA in cums or cum == CUM_XA:
        return cum == CUM_XA and CUM_XA in cums
    if cum in cums:
        return True
    return len(cums) < 2 and any(cum in CUM_KE.get(c, ()) for c in cums)


def xep(bang: Bang, ts: ThamSo) -> dict:
    """D2–D5: chọn + xếp điểm theo buổi ⇒ khung. Thứ tự ưu tiên = điểm người dùng nêu, rồi điểm hợp sở thích theo thứ tự bảng; thiếu ⇒ lấp
    bằng di tích theo thứ tự bảng **có nhãn** (D2 #2). Điểm nêu mà không xếp được ⇒ `khong_xep` + mã luật (D2b)."""
    n = _so_ngay(ts)
    han_che = ts.di_cung in HAN_CHE
    buoi_duoc = ("sang", "chieu") if han_che else BUOI
    khong_xep: list[dict] = []
    them_ids: list[str] = []
    for ten in ts.them_diem[:MAX_THEM_DIEM]:
        id_ = khop_diem(bang, ten)
        if id_ is None:
            khong_xep.append({"diem": ten, "ma_luat": "ngoai_bang"})
        elif not set(bang.theo_id[id_]["buoi"]) & set(buoi_duoc):
            khong_xep.append({"diem": bang.theo_id[id_]["ten"], "ma_luat": "khong_buoi_hop_le"})
        elif id_ not in them_ids:
            them_ids.append(id_)
    khong_xep += [{"diem": ten, "ma_luat": "het_suat"} for ten in ts.them_diem[MAX_THEM_DIEM:]]

    def dung_duoc(d: dict) -> bool:
        return (d["cum"] != CUM_XA or n >= 3 or d["id"] in them_ids) and bool(set(d["buoi"]) & set(buoi_duoc))

    so_thich = ts.so_thich or "di_tich"
    hop = [d["id"] for d in bang.diem if d["id"] not in them_ids and so_thich in d["loai"] and dung_duoc(d)]
    pool = them_ids + hop
    thien_nhien = [d["id"] for d in bang.diem if ts.so_thich is None and "thien_nhien" in d["loai"] and dung_duoc(d)]
    lap = [d["id"] for d in bang.diem if "di_tich" in d["loai"] and dung_duoc(d)]
    used: set[str] = set()
    ngoai_so_thich: list[str] = []

    def chon(cands: list[str], buoi: str, cums: list[str], chi_ngan: bool = False) -> str | None:
        for id_ in cands:
            d = bang.theo_id[id_]
            if id_ not in used and buoi in d["buoi"] and _cum_hop(d["cum"], cums) and (not chi_ngan or d["thoi_luong"] == "ngan"):
                return id_
        return None

    ngay = []
    for i in range(1, n + 1):
        cums: list[str] = []
        slots = {b: [] for b in BUOI}
        tn_hom_nay = False
        for buoi in buoi_duoc:
            id_ = None
            if buoi == "chieu" and not tn_hom_nay:
                id_ = chon(thien_nhien, buoi, cums)  # mặc định công khai: một điểm thiên nhiên / ngày (D2)
                tn_hom_nay = id_ is not None
            id_ = id_ or chon(pool, buoi, cums)
            if id_ is None and buoi != "toi":  # buổi tối chỉ xếp điểm hợp sở thích / người dùng nêu, không lấp
                id_ = chon(lap, buoi, cums)
                if id_ is not None and ts.so_thich is not None and ts.so_thich not in bang.theo_id[id_]["loai"]:
                    ngoai_so_thich.append(id_)
            if id_ is None:
                continue
            used.add(id_)
            slots[buoi].append(id_)
            if bang.theo_id[id_]["cum"] not in cums:
                cums.append(bang.theo_id[id_]["cum"])
            # D4: `day_lich` ⇒ thêm suất thứ hai cùng buổi chỉ khi cả hai điểm cùng cụm và đều ngắn (null tính như nửa buổi)
            if ts.kieu_di == "day_lich" and not han_che and bang.theo_id[id_]["thoi_luong"] == "ngan":
                hai = chon(pool, buoi, [bang.theo_id[id_]["cum"]], chi_ngan=True)
                if hai is not None and bang.theo_id[hai]["cum"] == bang.theo_id[id_]["cum"]:
                    used.add(hai)
                    slots[buoi].append(hai)
        ngay.append({"ngay": i, "buoi": slots})

    khong_xep += [{"diem": bang.theo_id[id_]["ten"], "ma_luat": "het_suat"} for id_ in them_ids if id_ not in used]
    gia_dinh = (["so_ngay_tam"] if ts.so_ngay_tam else []) + (["so_ngay_4"] if ts.so_ngay == "4+" else []) + \
        [k for k in ("so_thich", "kieu_di", "di_cung") if getattr(ts, k) is None]
    return {"tham_so": {"so_ngay": ts.so_ngay, "di_cung": ts.di_cung, "kieu_di": ts.kieu_di, "so_thich": ts.so_thich,
                        "them_diem": list(ts.them_diem), "so_ngay_tam": ts.so_ngay_tam},
            "ngay": ngay, "ngoai_so_thich": ngoai_so_thich,
            "thieu_so_thich": len(hop) + len(them_ids) if ngoai_so_thich else None,
            "khong_xep": khong_xep, "gia_dinh": gia_dinh}


def diem_trong_khung(khung: dict) -> list[str]:
    """Id điểm đã xếp, theo thứ tự ngày → buổi."""
    return [id_ for ng in khung["ngay"] for b in BUOI for id_ in ng["buoi"][b]]


def bo_diem(khung: dict, id_: str, ten: str, ma_luat: str) -> None:
    """D6 (iv): điểm không có đoạn đúng file ⇒ bỏ khỏi khung + `khong_xep` (mã luật)."""
    for ng in khung["ngay"]:
        for b in BUOI:
            if id_ in ng["buoi"][b]:
                ng["buoi"][b].remove(id_)
    khung["khong_xep"].append({"diem": ten, "ma_luat": ma_luat})


def cat_ngay_cuoi(khung: dict) -> list[str]:
    """D6 (iii): vượt ngân sách ngữ cảnh ⇒ bớt ngày cuối (khung ghi "ngày … chưa xếp"); trả id các điểm đã bớt."""
    ng = khung["ngay"].pop()
    khung["khong_xep"].append({"diem": str(ng["ngay"]), "ma_luat": "vuot_ngan_sach"})
    return [id_ for b in BUOI for id_ in ng["buoi"][b]]


def gio_diem(bang: Bang, id_: str) -> str | None:
    """D5: giờ có nguồn của điểm — Quần thể ⇒ khung giờ file vé; có `gio_mo_cua` ⇒ chép đúng; còn lại ⇒ None (kho không ghi giờ)."""
    d = bang.theo_id[id_]
    return GIO_QUAN_THE if d["quan_the"] else d["gio_mo_cua"]


def kiem_khung(bang: Bang, khung: dict) -> list[str]:
    """Luật xếp (Q2), độc lập với `xep` — mỗi lỗi một mã. Khung đúng ⇒ []. Dùng cho test cố tình vi phạm (#5) và cho dòng tiến độ D14."""
    ts = khung["tham_so"]
    han_che = ts["di_cung"] in HAN_CHE
    them_ids = {khop_diem(bang, t) for t in ts["them_diem"]} - {None}
    loi: list[str] = []
    so_ngay_hoi = 4 if ts["so_ngay"] == "4+" else int(ts["so_ngay"])
    cat = sum(k["ma_luat"] == "vuot_ngan_sach" for k in khung["khong_xep"])
    if len(khung["ngay"]) + cat != so_ngay_hoi:
        loi.append("so_ngay")
    for ng in khung["ngay"]:
        cums: list[str] = []
        so_suat = 0
        for b in BUOI:
            ids = ng["buoi"][b]
            so_suat += len(ids)
            for id_ in ids:
                d = bang.theo_id[id_]
                if b not in d["buoi"]:
                    loi.append("buoi_ngoai_buoi")
                if d["cum"] == CUM_XA and so_ngay_hoi < 3 and id_ not in them_ids:
                    loi.append("nam_xa")
                if d["cum"] not in cums:
                    cums.append(d["cum"])
            if len(ids) > 1 and (han_che or ts["kieu_di"] != "day_lich"):
                loi.append("qua_day_buoi")
            if len(ids) > 1 and ts["kieu_di"] == "day_lich" and not han_che and (
                    len({bang.theo_id[i]["cum"] for i in ids}) > 1 or any(bang.theo_id[i]["thoi_luong"] != "ngan" for i in ids) or len(ids) > 2):
                loi.append("day_lich_sai")
        if len(cums) > 2 or (CUM_XA in cums and len(cums) > 1):
            loi.append("qua_2_cum")
        if len(cums) == 2 and not (cums[1] in CUM_KE.get(cums[0], ())):
            loi.append("cum_khong_ke")
        if han_che and (so_suat > 2 or ng["buoi"]["toi"]):
            loi.append("han_che_qua_day")
    da_xep = diem_trong_khung(khung)
    if len(da_xep) != len(set(da_xep)):
        loi.append("trung_diem")
    ghi = {k["diem"] for k in khung["khong_xep"]}
    for id_ in them_ids:  # D2b: mỗi điểm người dùng nêu ở đúng một nơi
        if (id_ in da_xep) == (bang.theo_id[id_]["ten"] in ghi):
            loi.append("them_diem_lac")
    if ts["so_thich"] is not None:
        for id_ in da_xep:
            if ts["so_thich"] not in bang.theo_id[id_]["loai"] and id_ not in them_ids and id_ not in khung["ngoai_so_thich"]:
                loi.append("lap_khong_nhan")
        if khung["ngoai_so_thich"] and khung["thieu_so_thich"] is None:
            loi.append("lap_khong_cau")
    return loi


def dong_minh_hieu(khung: dict) -> str:
    """D12 (a): dòng đầu câu trả lời có lịch, dựng từ **tham số thật** (không phải chữ model); nút "Sửa" do giao diện vẽ."""
    ts = khung["tham_so"]
    phan = [GIA_TRI["so_ngay"][ts["so_ngay"]] + (" (tạm)" if ts["so_ngay_tam"] else "")]
    phan += [GIA_TRI[k][ts[k]] for k in ("di_cung", "kieu_di", "so_thich") if ts[k]]
    return "Mình hiểu: " + " · ".join(phan) + " — sai thì bấm **Sửa**."


def khung_chu(bang: Bang, khung: dict, nguon: dict[str, int], luat: str, nguon_ve: int | None = None) -> str:
    """Chữ khung đưa model (D7): luật trình bày đứng đầu, rồi từng ngày / buổi / điểm kèm số nguồn [n] và giờ có nguồn (D5 — giờ Quần thể
    trích đoạn file vé `nguon_ve`)."""
    dong = [luat, "", "Khung lịch:"]
    for ng in khung["ngay"]:
        dong.append(f"Ngày {ng['ngay']}")
        for b in BUOI:
            for id_ in ng["buoi"][b]:
                d = bang.theo_id[id_]
                gio = gio_diem(bang, id_)
                if gio and d["quan_the"] and nguon_ve is not None:
                    gio = f"{gio} [{nguon_ve}]"
                nhan = " ◦" if id_ in khung["ngoai_so_thich"] else ""
                dong.append(f"- {NHAN_BUOI[b]}: {d['ten']}{nhan} [{nguon[id_]}]" + (f" · giờ: {gio}" if gio else ""))
    return "\n".join(dong)


def _cau_thieu(bang: Bang, khung: dict) -> str:
    return CAU_THIEU_SO_THICH.format(k=khung["thieu_so_thich"], ten=", ".join(bang.theo_id[i]["ten"] for i in khung["ngoai_so_thich"]))


def khoi_ghi_chu(bang: Bang, khung: dict, nguon: dict[str, int]) -> str:
    """D4b: khối "Ghi chú của lịch" do code nối sau chữ model — giả định, câu thiếu sở thích, điểm không xếp, lưu ý có [n], dòng giờ có thể đổi."""
    dong = [CAU_GIA_DINH[k] for k in khung["gia_dinh"]]
    if khung["thieu_so_thich"] is not None:
        dong.append(_cau_thieu(bang, khung))
    dong += [CAU_KHONG_XEP[k["ma_luat"]].format(diem=k["diem"]) for k in khung["khong_xep"]]
    ids = diem_trong_khung(khung)
    dong += [f"{bang.theo_id[i]['ten']}: {bang.theo_id[i]['luu_y']} [{nguon[i]}]" for i in ids if bang.theo_id[i]["luu_y"]]
    if any(gio_diem(bang, i) for i in ids):
        dong.append(CAU_CO_THE_DOI)
    return "\n".join([TIEU_DE_GHI_CHU, *(f"- {d}" for d in dong)]) if dong else ""


def kiem_ghi_chu(bang: Bang, khung: dict, khoi: str) -> list[str]:
    """Q2: khối D4b có đủ mọi câu bắt buộc — giả định cho trường thiếu, câu thiếu sở thích, mỗi điểm không xếp, mỗi lưu ý của điểm trong
    khung (vd Thác Nhị Hồ mùa mưa lũ — D3). Thiếu ⇒ mã lỗi (test cố tình vi phạm đưa khối thiếu một câu)."""
    can = [CAU_GIA_DINH[k] for k in khung["gia_dinh"]] + [CAU_KHONG_XEP[k["ma_luat"]].format(diem=k["diem"]) for k in khung["khong_xep"]]
    if khung["thieu_so_thich"] is not None:
        can.append(_cau_thieu(bang, khung))
    can += [bang.theo_id[i]["luu_y"] for i in diem_trong_khung(khung) if bang.theo_id[i]["luu_y"]]
    return ["ghi_chu_thieu"] if any(c not in khoi for c in can) else []


def map_url(ten: str) -> str:
    """D11: link "mở bản đồ" dựng bằng code từ tên điểm + ", Huế" (không toạ độ, không chữ model)."""
    return MAP_BASE + quote(f"{ten}, Huế")


def ban_do(bang: Bang, khung: dict) -> list[dict]:
    return [{"ten": bang.theo_id[i]["ten"], "map_url": map_url(bang.theo_id[i]["ten"])} for i in diem_trong_khung(khung)]


# ---------- D8: kiểm cuối chữ model ----------

# `7h` · `07h00` · `5h30` · `7 giờ` · `5 giờ 30` · `7:00` (dạng có ":" phải có phút — "Ngày 1:" không phải giờ)
_GIO = re.compile(r"(?<![\w/])(\d{1,2})(?:\s*(?:h|giờ)\s*(\d{2})?|:(\d{2}))(?![\w/])", re.IGNORECASE)
_THOI_LUONG = re.compile(r"(?<![\w])\d+(?:[.,]\d+)?\s*(?:tiếng|phút)(?![\w])", re.IGNORECASE)
_URL = re.compile(r"https?://", re.IGNORECASE)
_CITE = re.compile(r"\[\s*(?:nguồn\s*)?(\d+)\s*\]", re.IGNORECASE)
_TIEU_DE_NGAY = re.compile(r"(?im)^\W*(?:ngày\s*(?:thứ\s*)?\d+|ngày\s+(?:một|hai|ba|bốn))\b")
_DONG_BUOI = re.compile(r"(?im)^\W*(?:sáng|chiều|tối)\b")


def gio_trong_chu(text: str) -> set[tuple[int, int]]:
    """Mọi giờ dạng `7h` / `07h00` / `7:00` / `7 giờ` / `5 giờ 30` / `5h30` ⇒ (giờ, phút) đã chuẩn hoá."""
    return {(int(h), int(m1 or m2 or 0)) for h, m1, m2 in _GIO.findall(unicodedata.normalize("NFC", text)) if int(h) <= 24}


def tap_gio(bang: Bang, khung: dict) -> set[tuple[int, int]]:
    """D5: tập giờ khung = mọi (giờ, phút) code chuẩn hoá từ chuỗi giờ đã đưa vào khung."""
    return set().union(*(gio_trong_chu(g) for i in diem_trong_khung(khung) if (g := gio_diem(bang, i))))


def _ten_xuat_hien(bang: Bang, text: str) -> dict[str, list[int]]:
    """Id điểm bảng có tên (khoá chuẩn hoá) xuất hiện trong chữ ⇒ các dòng chứa tên đó."""
    dong = [" ".join(unicodedata.normalize("NFC", d).casefold().split()) for d in text.splitlines()]
    hit: dict[str, list[int]] = {}
    for khoa, id_ in bang.khoa.items():
        if khoa == id_:  # khoá id (vd `dai_noi`) không phải chữ người viết
            continue
        mau = re.compile(r"(?<![\w])" + re.escape(khoa) + r"(?![\w])")
        for i, d in enumerate(dong):
            if mau.search(d):
                hit.setdefault(id_, []).append(i)
    return hit


def co_dang_lich(text: str) -> bool:
    """D8 (7): chữ có dạng lịch (≥ 2 tiêu đề ngày, hoặc ≥ 2 dòng mở bằng Sáng / Chiều / Tối)."""
    return len(_TIEU_DE_NGAY.findall(text)) >= 2 or len(_DONG_BUOI.findall(text)) >= 2


def kiem_cuoi(bang: Bang, text: str, khung: dict | None, nguon: dict[str, int] | None = None) -> list[str]:
    """D8 trên **chữ model** (không gồm khối code nối). Khung None = câu không gọi `lich_trinh` mà chữ có dạng lịch (D8 (7)) ⇒ kiểm với khung
    rỗng. Trả mã vi phạm (rỗng = đạt); hỏng ⇒ lõi xử như citation hỏng (rút lại)."""
    ids = set() if khung is None else set(diem_trong_khung(khung))
    hit = _ten_xuat_hien(bang, text)
    loi = []
    if set(hit) - ids:
        loi.append("diem_ngoai_khung")  # (1) (+ (8): tên điểm `khong_xep` như điểm đã xếp)
    if gio_trong_chu(text) - (set() if khung is None else tap_gio(bang, khung)):
        loi.append("gio_ngoai_khung")  # (2)
    if _THOI_LUONG.search(text):
        loi.append("thoi_luong")  # (2) chữ thời lượng — lời không nêu thời lượng (D4)
    if tim_so_tien(text):
        loi.append("gia")  # (3)
    if _URL.search(text):
        loi.append("url")  # (6)
    if khung is not None and nguon is not None:  # (4) mỗi điểm trong khung có [n] của chính nó trên dòng nhắc tên
        dong = text.splitlines()
        for id_ in ids:
            if not any(nguon[id_] in {int(n) for n in _CITE.findall(dong[i])} for i in hit.get(id_, [])):
                loi.append("thieu_trich_dan")
                break
    return loi


def dem_nhac_lai(bang: Bang, text: str, khung: dict) -> int:
    """D8 (8) — chỉ đếm (Q5): số câu giả định / lưu ý của khối D4b mà model chép lại."""
    t = unicodedata.normalize("NFC", text).casefold()
    cau = [CAU_GIA_DINH[k] for k in khung["gia_dinh"]] + [bang.theo_id[i]["luu_y"] for i in diem_trong_khung(khung) if bang.theo_id[i]["luu_y"]]
    return sum(c.casefold()[:30] in t for c in cau)

