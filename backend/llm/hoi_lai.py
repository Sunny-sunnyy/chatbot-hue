"""Hỏi lại khi câu lịch trình thiếu thông tin (Phase 9 B4, plan `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 2 `42fa62d2425f`;
**B4b — bản 8 `69afbb2732cf` D2′:** chỉ còn loại lịch trình — câu chi phí giữ hành vi `main` vì B4 âm ở câu chi phí, report B4 §2e / §2f).

**B5 (plan B5 bản 7 D15, User 10:07 05/11/2026 "code tự hỏi"; review C183 m-2):** công cụ `hoi_lai` cho model đã gỡ (luật lọc D3 cũng gỡ —
lịch sử ở tag `hoso/p9-b4`); **code** của công cụ `lich_trinh` tự trả thẻ khi thiếu số ngày. Ở đây còn: danh sách trường (D2 — khớp bộ đo C143
`data/phase_9/bo_do_b4/luat_ghi_truoc.md` và plan B5 D1), dữ liệu dựng nút (D8) và câu ghép đủ ý (D4). Không gọi mạng, không SDK — lõi và route đều dùng. Chữ người dùng thấy ở thẻ hỏi lại và câu ghép
là chữ cố định ở đây, không phải chữ model hay chữ tự do từ trình duyệt.
"""
import datetime as dt
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


# Trường theo loại (thứ tự = thứ tự hỏi / cắt; bắt buộc đứng trước) và trường bắt buộc (D2 — mặc định bộ đo C143).
TRUONG_THEO_LOAI: dict[str, tuple[str, ...]] = {
    "lich_trinh": ("so_ngay", "di_cung", "kieu_di", "so_thich"),
}
BAT_BUOC: dict[str, tuple[str, ...]] = {"lich_trinh": ("so_ngay",)}

# Nhãn nút: tên trường + từng giá trị cho phép (giá trị = khoá bộ đo C143). Nhãn dùng cả cho câu ghép.
NHAN_TRUONG = {"so_ngay": "Số ngày", "di_cung": "Đi cùng ai", "kieu_di": "Kiểu đi", "so_thich": "Sở thích"}
GIA_TRI: dict[str, dict[str, str]] = {
    "so_ngay": {"1": "1 ngày", "2": "2 ngày", "3": "3 ngày", "4+": "từ 4 ngày"},
    "di_cung": {"mot_minh": "đi một mình", "cap_doi": "đi hai người (cặp đôi)", "gia_dinh_tre_em": "gia đình có trẻ em",
                "nguoi_lon_tuoi": "có người lớn tuổi", "nhom_ban": "nhóm bạn"},
    "kieu_di": {"thong_tha": "đi thong thả", "day_lich": "đi dày lịch"},
    "so_thich": {"di_tich": "thích di tích", "am_thuc": "thích ẩm thực", "thien_nhien": "thích thiên nhiên",
                 "le_hoi_nghe_thuat": "thích lễ hội, nghệ thuật", "chup_anh": "thích chụp ảnh"},
}


def _ngay_iso(v):
    """Ngày đi chỉ nhận chuỗi `YYYY-MM-DD` (ô ngày của trình duyệt) — không nhận số / giờ (khuôn lỏng của pydantic nhận cả dấu thời gian)."""
    if isinstance(v, dt.date):
        return v
    if not (isinstance(v, str) and len(v) == 10):
        raise ValueError("ngay_di must be YYYY-MM-DD")
    return dt.date.fromisoformat(v)


SoThich = Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"]


class TruongInput(BaseModel):
    """Giá trị người dùng chọn ở nút (D4): dữ liệu không tin cậy từ trình duyệt ⇒ chỉ đúng tập giá trị trên, trường lạ ⇒ 422.
    Rỗng (`{}`) = "Trả lời luôn" (không hỏi lại nữa).

    "Lên kế hoạch" đợt 1 bước (a) (spec `2026-11-12-len-ke-hoach-ban-2-design.md` §5): nhận thêm giá trị **mới** của biểu mẫu bốn nhóm. Giá trị mới
    chỉ được dùng ở lượt biểu mẫu khi cờ `len_ke_hoach_v2` bật — route kiểm (`co_gia_tri_moi`), ở đây chỉ kiểm khuôn. Số kiểu chặt (không nhận
    chuỗi "2" hay true thay cho số)."""
    model_config = ConfigDict(extra="forbid")
    so_ngay: Literal["1", "2", "3", "4", "5", "4+"] | None = None
    di_cung: Literal["mot_minh", "cap_doi", "gia_dinh_tre_em", "nguoi_lon_tuoi", "nhom_ban"] | None = None
    kieu_di: Literal["thong_tha", "day_lich", "nhe_nhang", "can_bang", "kham_pha"] | None = None
    so_thich: SoThich | Annotated[list[SoThich], Field(min_length=1, max_length=2)] | None = None
    nguoi_lon: Annotated[int, Field(strict=True, ge=1, le=10)] | None = None
    tre_em: Annotated[int, Field(strict=True, ge=0, le=6)] | None = None
    lon_tuoi: Annotated[bool, Field(strict=True)] | None = None
    ngay_di: Annotated[dt.date, BeforeValidator(_ngay_iso)] | None = None

    @model_validator(mode="after")
    def _khong_mau_thuan(self):
        if isinstance(self.so_thich, list) and len(set(self.so_thich)) != len(self.so_thich):
            raise ValueError("so_thich has duplicates")
        if self.di_cung is not None and (self.nguoi_lon, self.tre_em, self.lon_tuoi) != (None, None, None):
            raise ValueError("di_cung (old) cannot be sent with nguoi_lon / tre_em / lon_tuoi (new)")
        return self


# ---------- "Lên kế hoạch" đợt 1 (plan `2026-11-12-len-ke-hoach-dot-1-plan.md` bước (a)) ----------

KIEU_DI_MOI = {"thong_tha": "nhe_nhang", "day_lich": "kham_pha"}  # spec 5c.3: luật "đi dày" cũ bỏ, tên cũ đổi sang mức mới
KIEU_DI_CU = {"nhe_nhang": "thong_tha", "kham_pha": "day_lich", "can_bang": None}  # bộ xếp cũ không có mức giữa ⇒ không truyền kiểu đi
# `di_cung` cũ ⇒ số người (spec §5: "code đổi sang trường mới"); chiều ngược dùng ở bước (a) để bộ xếp cũ chạy với biểu mẫu mới
DI_CUNG_MOI = {"mot_minh": {"nguoi_lon": 1}, "cap_doi": {"nguoi_lon": 2}, "gia_dinh_tre_em": {"nguoi_lon": 2, "tre_em": 1},
               "nguoi_lon_tuoi": {"nguoi_lon": 2, "lon_tuoi": True}, "nhom_ban": {"nguoi_lon": 4}}
TRUONG_CHI_MOI = ("nguoi_lon", "tre_em", "lon_tuoi", "ngay_di")
NGAY_DI_TOI_DA = 180  # spec §5: ngày đi từ hôm nay tới + 180 ngày
# Giới hạn của **bộ xếp cũ** mà bước (a) còn dùng (A đồng ý 12/11): biểu mẫu chưa cho chọn quá mức này; bước (b) nâng lên 5 ngày / 2 sở thích
SO_NGAY_TOI_DA = 4
SO_THICH_TOI_DA = 1


def co_gia_tri_moi(truong: TruongInput) -> bool:
    """Có giá trị chỉ biểu mẫu mới gửi (route: chỉ nhận ở lượt biểu mẫu khi cờ `len_ke_hoach_v2` bật)."""
    return (truong.so_ngay in ("4", "5") or truong.kieu_di in KIEU_DI_CU or isinstance(truong.so_thich, list)
            or any(getattr(truong, ten) is not None for ten in TRUONG_CHI_MOI))


def loi_v2(truong: TruongInput, hom_nay: dt.date) -> str | None:
    """Kiểm giá trị biểu mẫu mới theo ngày Việt Nam + giới hạn của bộ xếp đang dùng; None = hợp lệ (mã lỗi chỉ để test đọc)."""
    if truong.ngay_di is not None and not hom_nay <= truong.ngay_di <= hom_nay + dt.timedelta(days=NGAY_DI_TOI_DA):
        return "ngay_di"
    if truong.so_ngay is not None and truong.so_ngay != "4+" and int(truong.so_ngay) > SO_NGAY_TOI_DA:
        return "so_ngay"
    if isinstance(truong.so_thich, list) and len(truong.so_thich) > SO_THICH_TOI_DA:
        return "so_thich"
    return None


def doi_sang_moi(cu: dict) -> dict:
    """Giá trị cũ (thẻ hỏi lại / biểu mẫu cũ) ⇒ khuôn mới: "4+" ⇒ "4", kiểu đi cũ ⇒ mức mới, sở thích chuỗi ⇒ danh sách, `di_cung` ⇒ số người."""
    moi = {k: v for k, v in cu.items() if k != "di_cung"}
    if cu.get("so_ngay") == "4+":
        moi["so_ngay"] = "4"
    if cu.get("kieu_di") in KIEU_DI_MOI:
        moi["kieu_di"] = KIEU_DI_MOI[cu["kieu_di"]]
    if isinstance(cu.get("so_thich"), str):
        moi["so_thich"] = [cu["so_thich"]]
    if cu.get("di_cung"):
        moi.update(DI_CUNG_MOI[cu["di_cung"]])
    return moi


def doi_sang_cu(moi: dict) -> dict:
    """Khuôn mới ⇒ đúng bốn trường bộ xếp cũ hiểu (`so_ngay`, `di_cung`, `kieu_di`, `so_thich`). Trẻ em thắng lớn tuổi (cả hai là nhóm hạn chế,
    bộ xếp cũ chỉ nhận một); số người lớn chỉ đổi nhãn đi cùng. `ngay_di` chưa dùng ở bộ xếp cũ ⇒ bỏ. Giá trị cũ giữ nguyên."""
    cu: dict = {}
    if moi.get("so_ngay"):
        cu["so_ngay"] = "4+" if moi["so_ngay"] == "4" else moi["so_ngay"]
    if moi.get("di_cung"):
        cu["di_cung"] = moi["di_cung"]
    elif moi.get("tre_em"):
        cu["di_cung"] = "gia_dinh_tre_em"
    elif moi.get("lon_tuoi"):
        cu["di_cung"] = "nguoi_lon_tuoi"
    elif moi.get("nguoi_lon") is not None:
        cu["di_cung"] = {1: "mot_minh", 2: "cap_doi"}.get(moi["nguoi_lon"], "nhom_ban")
    kieu = KIEU_DI_CU.get(moi.get("kieu_di"), moi.get("kieu_di"))
    if kieu:
        cu["kieu_di"] = kieu
    so_thich = moi.get("so_thich")
    if so_thich:
        cu["so_thich"] = so_thich[0] if isinstance(so_thich, list) else so_thich
    return cu


def the_hoi_lai(loai: str, truong: list[str], cau_goc: str) -> dict:
    """Dữ liệu thẻ hỏi lại cho giao diện (sự kiện `clarify` / trường `clarify` của `/api/chat`) — code dựng nút từ bảng (spec §3)."""
    return {"loai": loai, "cau_goc": cau_goc, "bat_buoc": [t for t in truong if t in BAT_BUOC[loai]],
            "truong": [{"ten": t, "nhan": NHAN_TRUONG[t], "lua_chon": [{"gia_tri": k, "nhan": v} for k, v in GIA_TRI[t].items()]} for t in truong]}


def ghep_cau(cau_goc: str, truong: TruongInput) -> str:
    """D4: câu gốc + giá trị đã chọn ⇒ một câu đủ ý, chữ từ bảng nhãn (tất định). Không chọn gì ("Trả lời luôn") ⇒ đúng câu gốc."""
    chon = [GIA_TRI[ten][gia_tri] for ten, gia_tri in truong.model_dump(exclude_none=True).items()]
    cau = cau_goc.strip()
    return cau if not chon else f"{cau} (Thông tin thêm: {'; '.join(chon)}.)"
