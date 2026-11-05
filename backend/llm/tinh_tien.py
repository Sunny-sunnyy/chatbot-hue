"""Tính tiền bằng code (Phase 9 B5c, plan `docs/superpowers/plans/2026-11-05-phase-9-b5c-plan.md` bản 3 `bab730a57798`).

Model chỉ chọn loại câu (dự toán / vé / cả hai / khoản ngoài bảng), mức chi, tên điểm; **code** đọc 3 bảng dự toán + bảng vé lẻ Quần thể từ kho
(nạp lúc khởi động, kiểm schema + tổng), lấy số người / ngày (D6 — `do_so`), nhân / cộng (D3, D2b), dựng bảng Markdown có `[n]` + khối ghi chú
(D8) và kiểm số tiền trong chữ model (D9). Hàm thuần — không gọi mạng, không SDK.
"""
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from llm.do_so import MAX_NGUOI, SoNguoi
from llm.hoi_lai import GIA_TRI
from llm.lich_trinh import Bang, chuan_ten, khop_diem
from llm.so_tien import tim_gia_tri

Loai = Literal["du_toan", "ve", "ca_hai", "ngoai_bang"]
MucChi = Literal["tiet_kiem", "tieu_chuan", "thoai_mai"]
MUC: tuple[str, ...] = ("tiet_kiem", "tieu_chuan", "thoai_mai")
NHAN_MUC = {"tiet_kiem": "Tiết kiệm", "tieu_chuan": "Tiêu chuẩn", "thoai_mai": "Thoải mái"}
# D2: tiêu đề mục của 3 bảng trong file chi phí ⇒ số ngày; số hạng mục (không kể dòng tổng) kiểm lúc nạp
TIEU_DE_DU_TOAN = {1: "Dự toán một ngày tại Huế", 2: "Dự toán hai ngày một đêm tại Huế", 3: "Dự toán ba ngày hai đêm tại Huế"}
SO_HANG_MUC = {1: 5, 2: 6, 3: 6}
# Mục bảng vé lẻ: nhận bằng từ khoá của tiêu đề (không chép nguyên tiêu đề kho vào repo public — hook pre-commit)
TU_KHOA_VE = ("bảng giá", "vé lẻ")


def la_muc_ve(tieu_de: str) -> bool:
    t = tieu_de.casefold()
    return all(k in t for k in TU_KHOA_VE)
SO_DONG_VE = 12
MAX_DIEM = 5  # D1: `diem` ≤ 5

# Câu cố định (code nối — D8). Không nhắc số; số nằm trong bảng.
CAU = {
    "han_muc": "Số trong bảng là hạn mức lập kế hoạch của kho (đối chiếu {ngay}), không phải giá niêm yết; chưa gồm chi phí đến / rời Huế.",
    "D3_tre_em": "Mức cho trẻ em có thể khác — kho không ghi số riêng; nên hỏi trực tiếp phụ thu trẻ em.",
    "D5_luu_tru": "Bảng tính theo người khi ở chung phòng; đi một mình / số người lẻ thì tiền phòng mỗi người có thể cao hơn — kho không ghi số cụ thể.",
    "D4_khong_cong_ve": "Khoản tham quan trong dự toán đã là khoản dự trù cho vé, không cộng thêm.",
    "ve_hieu_luc": "Giá vé lẻ theo bảng của Quần thể Di tích Cố đô Huế, có hiệu lực từ {ngay}.",
    "ve_doi_tuong": "Trẻ ngoài độ tuổi này và các đối tượng miễn / giảm: xem chính sách trong nguồn của bảng vé.",
    "ve_gop": "Có vé tuyến gộp nhiều điểm thường rẻ hơn mua lẻ — xem bảng vé gộp trong kho.",
    "ve_tre_khong_so": "Chưa biết số trẻ em nên chưa tính tổng tiền vé.",
    "ve_khong_co": "Chưa có giá vé của «{ten}» trong bảng vé lẻ.",
    "ngoai": "Chưa đủ dữ liệu để tính tổng: {ly_do}.",
    "tam": "Mình tạm tính cho {phan} — bấm Sửa để đổi.",
}
LY_DO_NGOAI = {
    "so_ngay_4_tro_len": "kho chỉ có bảng dự toán 1 ngày, 2 ngày 1 đêm và 3 ngày 2 đêm",
    "dem_lech": "số đêm không khớp bảng 1 ngày / 2 ngày 1 đêm / 3 ngày 2 đêm của kho",
    "nua_ngay": "kho không có bảng dự toán nửa ngày",
    "qua_20_nguoi": f"chỉ tính cho tối đa {MAX_NGUOI} người",
    "ngoai_bang": "kho không có bảng giá cho khoản này (giá phòng, bữa ăn, xe… cụ thể)",
    "ve_ngoai_bang_ve_le": "các điểm này không có trong bảng vé lẻ của Quần thể",
    "khong_co_doan_nguon": "không lấy được đoạn kho của bảng dự toán để trích nguồn",
}
TIEU_DE_GHI_CHU = "**Ghi chú về số tiền**"


@dataclass(frozen=True)
class BangNgay:
    so_ngay: int
    tieu_de: str
    hang_muc: tuple[tuple[str, dict[str, tuple[int, int]]], ...]  # (tên, {mức: (thấp, cao)}) — một người
    tong: dict[str, tuple[int, int]]


@dataclass(frozen=True)
class DongVe:
    ten: str          # phần in đậm của ô tên
    bi_danh: str | None
    nguoi_lon: int
    tre_em: int       # 0 = miễn phí
    id_diem: str | None  # id bảng điểm B5 khớp được (None: dòng không có trong bảng điểm)
    khoa: frozenset[str]


@dataclass(frozen=True)
class BangTien:
    du_toan: dict[int, BangNgay]
    ngay_doi_chieu: str
    ve: tuple[DongVe, ...]
    ve_dieu_kien_tre: str  # chữ điều kiện tuổi đọc nguyên từ tiêu đề cột ("trẻ em từ 7–12 tuổi")
    ve_hieu_luc: str
    nguon_du_toan: str  # `source` của đoạn kho (đường dẫn tương đối gốc kho)
    nguon_ve: str
    diem: Bang  # bảng điểm B5 (khớp tên điểm ⇒ dòng vé, D2b)


_KHOANG = re.compile(r"^\**\s*(\d{1,3}(?:\.\d{3})*|0)\s*–\s*(\d{1,3}(?:\.\d{3})*)\s*\**$")


def _so(chuoi: str) -> int:
    return int(chuoi.replace(".", ""))


def _bang_md(dong: list[str]) -> list[list[str]]:
    """Các dòng bảng Markdown (bỏ dòng kẻ) ⇒ ô đã cắt khoảng trắng."""
    out = []
    for d in dong:
        o = [x.strip() for x in d.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", x) for x in o):
            continue
        out.append(o)
    return out


def _muc(text: str, tieu_de) -> list[str]:
    """Dòng bảng `|…|` đầu tiên liền sau tiêu đề mục (chuỗi đúng nguyên văn, hoặc hàm nhận tiêu đề) — tới mục kế."""
    dong = text.splitlines()
    khop = tieu_de if callable(tieu_de) else (lambda t: t == tieu_de)
    try:
        i = next(k for k, d in enumerate(dong) if d.startswith("#") and khop(d.strip().lstrip("#").strip()))
    except StopIteration:
        raise ValueError(f"bảng tiền: không thấy mục «{tieu_de if isinstance(tieu_de, str) else 'vé lẻ'}»") from None
    bang: list[str] = []
    for d in dong[i + 1:]:
        if d.startswith("#"):
            break
        if d.strip().startswith("|"):
            bang.append(d)
        elif bang:
            break
    return bang


def nap_du_toan(text: str) -> tuple[dict[int, BangNgay], str]:
    """D2: 3 bảng (5 / 6 / 6 hạng mục + dòng tổng), mỗi ô một khoảng hợp lệ, **tổng kho = tổng code cộng từ hạng mục** ở cả 9 ô — sai ⇒ ValueError."""
    out = {}
    for so_ngay, tieu_de in TIEU_DE_DU_TOAN.items():
        rows = _bang_md(_muc(text, tieu_de))
        dau, than = rows[0], rows[1:]
        if [x.casefold() for x in dau[1:]] != ["tiết kiệm", "tiêu chuẩn", "thoải mái"]:
            raise ValueError(f"bảng tiền: cột mức của «{tieu_de}» khác")
        *hang, tong_row = than
        if len(hang) != SO_HANG_MUC[so_ngay] or "tổng" not in tong_row[0].casefold():
            raise ValueError(f"bảng tiền: «{tieu_de}» không đủ {SO_HANG_MUC[so_ngay]} hạng mục + dòng tổng")

        def khoang(o: str) -> tuple[int, int]:
            m = _KHOANG.match(o)
            if not m or _so(m.group(1)) > _so(m.group(2)):
                raise ValueError(f"bảng tiền: ô «{o}» của «{tieu_de}» không phải khoảng")
            return _so(m.group(1)), _so(m.group(2))
        hang_muc = tuple((r[0], {m: khoang(r[k + 1]) for k, m in enumerate(MUC)}) for r in hang)
        tong = {m: khoang(tong_row[k + 1]) for k, m in enumerate(MUC)}
        for m in MUC:
            cong = (sum(h[1][m][0] for h in hang_muc), sum(h[1][m][1] for h in hang_muc))
            if cong != tong[m]:
                raise ValueError(f"bảng tiền: tổng kho {tong[m]} ≠ tổng cộng {cong} ở «{tieu_de}» mức {m}")
        out[so_ngay] = BangNgay(so_ngay, tieu_de, hang_muc, tong)
    ngay = re.search(r"đối chiếu\s+(?:\S+\s+){0,4}?ngày\s+(\d{2}/\d{2}/\d{4})", " ".join(text.split()))
    if not ngay:
        raise ValueError("bảng tiền: không thấy ngày đối chiếu")
    return out, ngay.group(1)


def nap_ve(text: str, bang_diem: Bang) -> tuple[tuple[DongVe, ...], str, str]:
    """D2b: bảng vé lẻ (12 dòng) + điều kiện tuổi ở tiêu đề cột + ngày hiệu lực; **mỗi điểm `quan_the` của bảng điểm khớp đúng một dòng** — sai ⇒ ValueError."""
    rows = _bang_md(_muc(text, la_muc_ve))
    dau = [x.casefold() for x in rows[0]]
    i_ten = next(k for k, x in enumerate(dau) if x.startswith("tên điểm"))
    i_lon = next(k for k, x in enumerate(dau) if "người lớn" in x)
    i_tre = next(k for k, x in enumerate(dau) if "trẻ em" in x)
    dk = re.search(r"(trẻ em[^(]*?)\s*\(", rows[0][i_tre])
    if not dk:
        raise ValueError("bảng vé: không đọc được điều kiện tuổi ở tiêu đề cột trẻ em")
    hl = re.search(r"Ngày có hiệu lực[^:]*:\**\s*(\d{2}/\d{2}/\d{4})", text)
    if not hl:
        raise ValueError("bảng vé: không thấy ngày có hiệu lực")

    def gia(o: str) -> int:
        o = o.strip("* ")
        if o.casefold() == "miễn phí":
            return 0
        if not re.fullmatch(r"\d{1,3}(?:\.\d{3})*", o):
            raise ValueError(f"bảng vé: ô giá «{o}» lạ")
        return _so(o)
    dong = []
    for r in rows[1:]:
        ten = re.search(r"\*\*(.+?)\*\*", r[i_ten])
        bd = re.search(r"\(([^)]+)\)", r[i_ten])
        if not ten:
            raise ValueError(f"bảng vé: ô tên «{r[i_ten]}» không có phần in đậm")
        ten_s, bd_s = ten.group(1).strip(), (bd.group(1).strip() if bd else None)
        ids = {i for i in (khop_diem(bang_diem, ten_s), bd_s and khop_diem(bang_diem, bd_s)) if i}
        if len(ids) > 1:
            raise ValueError(f"bảng vé: dòng «{ten_s}» khớp nhiều điểm {sorted(ids)}")
        id_ = ids.pop() if ids else None
        khoa = {chuan_ten(ten_s)} | ({chuan_ten(bd_s)} if bd_s else set())
        if id_:
            d = bang_diem.theo_id[id_]
            khoa |= {chuan_ten(x) for x in (d["ten"], *d["ten_khac"])}
        dong.append(DongVe(ten_s, bd_s, gia(r[i_lon]), gia(r[i_tre]), id_, frozenset(khoa)))
    if len(dong) != SO_DONG_VE:
        raise ValueError(f"bảng vé: {len(dong)} dòng, cần {SO_DONG_VE}")
    for d in bang_diem.diem:
        if d["quan_the"] and sum(v.id_diem == d["id"] for v in dong) != 1:
            raise ValueError(f"bảng vé: điểm Quần thể «{d['ten']}» không khớp đúng một dòng vé")
    return tuple(dong), dk.group(1).strip(), hl.group(1)


def nap_bang_tien(root: Path, du_toan_rel: str, ve_rel: str, bang_diem: Bang) -> BangTien:
    du_toan, ngay = nap_du_toan((root / du_toan_rel).read_text(encoding="utf-8"))
    ve, dieu_kien, hieu_luc = nap_ve((root / ve_rel).read_text(encoding="utf-8"), bang_diem)
    return BangTien(du_toan, ngay, ve, dieu_kien, hieu_luc, du_toan_rel, ve_rel, bang_diem)


def khop_ve(bang: BangTien, ten: str) -> DongVe | None:
    """Tên model gửi ⇒ dòng vé (khoá dòng: tên in đậm, bí danh, tên + tên khác của điểm bảng B5); không khớp ⇒ None (không đoán)."""
    k = chuan_ten(ten)
    id_ = khop_diem(bang.diem, ten)
    return next((v for v in bang.ve if k in v.khoa or (id_ is not None and v.id_diem == id_)), None)


# ---------- tham số (D6, D7) ----------

@dataclass(frozen=True)
class ThamSoTien:
    loai: str
    so_nguoi: int | None
    nguoi_lon: int | None
    tre_em: int | None
    so_ngay: str | None
    muc_chi: str | None
    diem: tuple[str, ...]
    tam: tuple[str, ...] = ()  # trường code đặt tạm (lượt "Trả lời luôn")
    ngoai: str | None = None


def can_truong(loai: str) -> tuple[str, ...]:
    """Trường bắt buộc theo loại (D7): dự toán cần số người + số ngày; vé cần số người."""
    return {"du_toan": ("so_nguoi", "so_ngay"), "ca_hai": ("so_nguoi", "so_ngay"), "ve": ("so_nguoi",)}.get(loai, ())


def chot_tham_so(loai: str, muc_chi: str | None, diem: list[str] | None, truong: dict | None, nguoi: SoNguoi,
                 ngay: tuple[str | None, str | None]) -> tuple[ThamSoTien | None, list[str]]:
    """D6 + D7: (1) `truong` từ nút ⇒ (2) dò số (đã dò từ câu gốc + câu trước, `nguoi`, `ngay`) ⇒ (3) thiếu: lượt thường ⇒ trả danh sách trường
    cần hỏi (ThamSo None); lượt mang `truong` ⇒ **không hỏi lần hai**, trường còn thiếu đặt tạm 1."""
    if loai == "du_toan" and diem:  # vòng chỉnh 1 (pilot T7): model gửi dự toán kèm tên điểm hỏi vé ⇒ code coi là cả hai (D4: hai bảng riêng)
        loai = "ca_hai"
    tu_nut = truong or {}
    so_nguoi = tu_nut.get("so_nguoi") or nguoi.tong
    nguoi_lon, tre_em = (None, None) if tu_nut.get("so_nguoi") else (nguoi.nguoi_lon, nguoi.tre_em)
    so_ngay_do, ngoai = ngay
    so_ngay = tu_nut.get("so_ngay") or so_ngay_do
    if tu_nut.get("so_ngay"):
        ngoai = None
    if loai in ("ve", "ca_hai") and so_nguoi is None and nguoi_lon is not None:
        so_nguoi = nguoi_lon  # vé: chỉ biết người lớn (trẻ có nhắc nhưng không số) — vẫn tính được tiền người lớn
    can = can_truong(loai)
    thieu = [t for t in can if {"so_nguoi": so_nguoi, "so_ngay": so_ngay if ngoai is None else "x"}[t] is None]
    tam: list[str] = []
    if thieu and truong is None:
        return None, thieu
    for t in thieu:
        tam.append(t)
        if t == "so_nguoi":
            so_nguoi = 1
        else:
            so_ngay = "1"
    if so_nguoi is not None and so_nguoi > MAX_NGUOI:
        ngoai = "qua_20_nguoi"
    if loai in ("du_toan", "ca_hai") and ngoai is None and so_ngay == "4+":
        ngoai = "so_ngay_4_tro_len"
    if loai == "ngoai_bang":
        ngoai = "ngoai_bang"
    return ThamSoTien(loai, so_nguoi, nguoi_lon, tre_em, so_ngay, tu_nut.get("muc_chi") or muc_chi, tuple((diem or [])[:MAX_DIEM]),
                      tuple(tam), ngoai if loai != "ve" or ngoai == "qua_20_nguoi" else None), []


# ---------- tính (D3, D2b, D4, D5) ----------

def tinh(bang: BangTien, ts: ThamSoTien) -> dict:
    """Kết quả số của lượt (dict để log / test / dựng bảng): dự toán theo mức (×số người, cộng riêng từng cận), vé theo dòng; mã lưu ý."""
    kq: dict = {"tham_so": ts, "du_toan": None, "ve": None, "luu_y": [], "ngoai": ts.ngoai, "khong_co": []}
    if ts.ngoai in ("ngoai_bang", "qua_20_nguoi"):
        return kq
    if ts.loai in ("du_toan", "ca_hai") and ts.ngoai is None:
        b = bang.du_toan[int(ts.so_ngay)]
        n = ts.so_nguoi
        muc = (ts.muc_chi,) if ts.muc_chi else MUC
        hang = [(ten, {m: (o[m][0] * n, o[m][1] * n) for m in muc}) for ten, o in b.hang_muc]
        tong = {m: (sum(h[1][m][0] for h in hang), sum(h[1][m][1] for h in hang)) for m in muc}
        kq["du_toan"] = {"so_ngay": b.so_ngay, "tieu_de": b.tieu_de, "muc": muc, "hang_muc": hang, "tong": tong}
        if ts.tre_em:
            kq["luu_y"].append("D3_tre_em")
        if b.so_ngay >= 2 and n % 2 == 1:
            kq["luu_y"].append("D5_luu_tru")
    if ts.loai in ("ve", "ca_hai"):
        dong, khong_co = [], []
        for ten in ts.diem:
            v = khop_ve(bang, ten)
            if v is None:
                khong_co.append(ten)
            elif v not in dong:
                dong.append(v)
        kq["khong_co"] = khong_co
        if not dong:
            kq["ngoai"] = kq["ngoai"] or "ve_ngoai_bang_ve_le"
        else:
            lon = ts.nguoi_lon if ts.nguoi_lon is not None else ts.so_nguoi
            tre = ts.tre_em if ts.nguoi_lon is not None else 0
            hang = [{"ten": v.ten, "gia_lon": v.nguoi_lon, "gia_tre": v.tre_em, "tien_lon": v.nguoi_lon * lon,
                     "tien_tre": None if tre is None else v.tre_em * tre} for v in dong]
            co_tong = tre is not None
            kq["ve"] = {"nguoi_lon": lon, "tre_em": tre, "hang": hang,
                        "tong": sum(h["tien_lon"] + h["tien_tre"] for h in hang) if co_tong else None}
            if ts.loai == "ca_hai" and kq["du_toan"] is not None:
                kq["luu_y"].append("D4_khong_cong_ve")
    return kq


def khung_chu(kq: dict, luat: str) -> str:
    """Chữ đưa model (D8): luật trình bày + bảng sẽ hiện gì + lý do không tính (nếu có). **Không số tiền** — số chỉ ở bảng code nối."""
    ts = kq["tham_so"]
    phan = [luat]
    if kq["du_toan"] is not None:
        muc = ", ".join(NHAN_MUC[m].lower() for m in kq["du_toan"]["muc"])
        phan.append(f"Hệ thống sẽ thêm bảng {kq['du_toan']['tieu_de'].lower()} cho {ts.so_nguoi} người (mức {muc}).")
    if kq["ve"] is not None:
        phan.append("Hệ thống sẽ thêm bảng tiền vé lẻ cho: " + ", ".join(h["ten"] for h in kq["ve"]["hang"]) + ".")
    if kq["khong_co"]:
        phan.append("Bảng vé lẻ không có: " + ", ".join(kq["khong_co"]) + ".")
    if kq["ngoai"]:
        phan.append(f"Không tính tổng được ({LY_DO_NGOAI[kq['ngoai']]}): trả lời bằng thông tin trong tài liệu đã có, kèm [n]; "
                    "không tự ước hay cộng số tiền.")
    return "\n".join(phan)


def dong(so: int) -> str:
    """50000 ⇒ "50.000 đ" (một kiểu viết cho mọi số code dựng)."""
    return f"{so:,}".replace(",", ".") + " đ"


def bang_markdown(bang: BangTien, kq: dict, n_du_toan: int | None, n_ve: dict[str, int]) -> str:
    """D8: bảng do code nối (sau chữ model). `n_du_toan` = số nguồn đoạn bảng dự toán; `n_ve` = tên dòng vé ⇒ số nguồn đoạn dòng đó."""
    phan = []
    dt = kq["du_toan"]
    if dt is not None and n_du_toan is not None:
        ts = kq["tham_so"]
        dau = "| Hạng mục | " + " | ".join(NHAN_MUC[m] for m in dt["muc"]) + " |"
        ke = "|---|" + "---:|" * len(dt["muc"])
        than = [f"| {ten} | " + " | ".join(f"{dong(o[m][0])} – {dong(o[m][1])}" for m in dt["muc"]) + " |" for ten, o in dt["hang_muc"]]
        tong = "| **Tổng tại Huế** | " + " | ".join(f"**{dong(dt['tong'][m][0])} – {dong(dt['tong'][m][1])}**" for m in dt["muc"]) + " |"
        phan.append(f"**Dự toán {dt['tieu_de'][len('Dự toán '):]} cho {ts.so_nguoi} người** [{n_du_toan}]\n\n" + "\n".join([dau, ke, *than, tong]))
    ve = kq["ve"]
    if ve is not None:
        co_tre = ve["tre_em"] is None or ve["tre_em"] > 0
        dau = f"| Điểm | Người lớn × {ve['nguoi_lon']} |" + (f" Trẻ em ({bang.ve_dieu_kien_tre.removeprefix('trẻ em ')}) × {ve['tre_em'] if ve['tre_em'] is not None else '?'} |" if co_tre else "")
        ke = "|---|---:|" + ("---:|" if co_tre else "")
        than = []
        for h in ve["hang"]:
            n = n_ve.get(h["ten"])
            ten = f"{h['ten']} [{n}]" if n else h["ten"]
            lon = f"{dong(h['gia_lon'])} × {ve['nguoi_lon']} = {dong(h['tien_lon'])}"
            tre = "" if not co_tre else (" " + (f"{dong(h['gia_tre'])} (miễn phí)" if h["gia_tre"] == 0 else dong(h["gia_tre"]))
                                          + ("" if h["tien_tre"] is None else f" × {ve['tre_em']} = {dong(h['tien_tre'])}") + " |")
            than.append(f"| {ten} | {lon} |{tre}")
        bang_ve = "\n".join([dau, ke, *than])
        if ve["tong"] is not None:
            bang_ve += f"\n\n**Tổng tiền vé lẻ: {dong(ve['tong'])}**"
        phan.append("**Vé tham quan (vé lẻ)**\n\n" + bang_ve)
    return "\n\n".join(phan)


def dong_minh_hieu(ts: ThamSoTien) -> str:
    """D12 (a) dùng chung với B5: dòng đầu dựng từ tham số thật; "(tạm)" khi code đặt tạm."""
    phan = []
    if ts.loai in ("ve", "ca_hai") and ts.nguoi_lon is not None and ts.tre_em:
        phan.append(f"{ts.nguoi_lon} người lớn · {ts.tre_em} trẻ em")
    elif ts.so_nguoi is not None:
        phan.append(f"{ts.so_nguoi} người" + (" (tạm)" if "so_nguoi" in ts.tam else ""))
    if ts.loai in ("du_toan", "ca_hai") and ts.so_ngay is not None:
        phan.append(GIA_TRI["so_ngay"][ts.so_ngay] + (" (tạm)" if "so_ngay" in ts.tam else ""))
    if ts.muc_chi:
        phan.append("mức " + NHAN_MUC[ts.muc_chi].lower())
    return "Mình hiểu: " + " · ".join(phan) + " — sai thì bấm **Sửa**." if phan else ""


def khoi_ghi_chu(bang: BangTien, kq: dict) -> str:
    """D8: khối ghi chú code nối dưới bảng — mỗi câu cố định một dòng."""
    ts = kq["tham_so"]
    dong_ = []
    if ts.tam:
        phan = " · ".join({"so_nguoi": "1 người", "so_ngay": "1 ngày"}[t] for t in ts.tam)
        dong_.append(CAU["tam"].format(phan=phan))
    if kq["ngoai"]:
        dong_.append(CAU["ngoai"].format(ly_do=LY_DO_NGOAI[kq["ngoai"]]))
    if kq["du_toan"] is not None:
        dong_.append(CAU["han_muc"].format(ngay=bang.ngay_doi_chieu))
    dong_ += [CAU[k] for k in kq["luu_y"]]
    dong_ += [CAU["ve_khong_co"].format(ten=t) for t in kq["khong_co"]]
    if kq["ve"] is not None:
        if kq["ve"]["tong"] is None:
            dong_.append(CAU["ve_tre_khong_so"])
        dong_ += [CAU["ve_hieu_luc"].format(ngay=bang.ve_hieu_luc), CAU["ve_doi_tuong"], CAU["ve_gop"]]
    return "" if not dong_ else TIEU_DE_GHI_CHU + "\n" + "\n".join(f"- {d}" for d in dong_)


def so_code(kq: dict) -> set[int]:
    """Mọi số tiền code tính / in ra ở lượt này (D9 (1): số model được phép nhắc)."""
    out: set[int] = set()
    if kq["du_toan"]:
        for _, o in kq["du_toan"]["hang_muc"]:
            out |= {x for v in o.values() for x in v}
        out |= {x for v in kq["du_toan"]["tong"].values() for x in v}
    if kq["ve"]:
        for h in kq["ve"]["hang"]:
            out |= {h["gia_lon"], h["gia_tre"], h["tien_lon"]} | ({h["tien_tre"]} if h["tien_tre"] is not None else set())
        if kq["ve"]["tong"] is not None:
            out.add(kq["ve"]["tong"])
    return out


_SO_NHOM = re.compile(r"(?<![\w.,])\d{1,3}(?:\.\d{3})+(?![\w.,]?\d)")  # "150.000" không đơn vị (ô bảng kho, chữ model)
_TU_TONG = re.compile(r"(?i)(?<![\w])(?:tổng(?:\s+cộng)?|cả\s+chuyến|tất\s+cả)(?![\w])")


def so_tien_trong(text: str) -> set[int]:
    """Số tiền trong chữ: dạng có đơn vị (`tim_gia_tri`) + số nhóm nghìn không đơn vị (≥ 1.000)."""
    t = unicodedata.normalize("NFC", text)
    return set(tim_gia_tri(t)) | {int(m.group(0).replace(".", "")) for m in _SO_NHOM.finditer(t)}


def kiem_tien(text: str, nguon_text: list[str], kq: dict | None) -> list[str]:
    """D9 trên **chữ model** (không gồm bảng / ghi chú code nối): (1) mọi số tiền ∈ số trong đoạn kho đã đưa ∪ số code tính; (2) dòng có chữ
    "tổng / tổng cộng / cả chuyến / tất cả" kèm số tiền ⇒ hỏng (tổng chỉ do code nối). Rỗng = đạt."""
    cho_phep = set().union(*(so_tien_trong(t) for t in nguon_text)) if nguon_text else set()
    if kq is not None:
        cho_phep |= so_code(kq)
    loi = []
    if so_tien_trong(text) - cho_phep:
        loi.append("so_tien_ngoai")
    if any(_TU_TONG.search(d) and so_tien_trong(d) for d in text.splitlines()):
        loi.append("tong_tu_viet")
    return loi
