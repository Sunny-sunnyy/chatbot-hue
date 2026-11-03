"""Hỏi lại khi câu lịch trình / chi phí thiếu thông tin (Phase 9 B4, plan `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 2 `42fa62d2425f`).

Một chỗ cho danh sách trường (D2 — khớp bộ đo C143 `data/phase_9/bo_do_b4/luat_ghi_truoc.md` và plan B5 D1), luật lọc lời gọi của model (D3),
dữ liệu dựng nút (D8) và câu ghép đủ ý (D4). Không gọi mạng, không SDK — lõi và route đều dùng. Chữ người dùng thấy ở thẻ hỏi lại và câu ghép
là chữ cố định ở đây, không phải chữ model hay chữ tự do từ trình duyệt.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict

Loai = Literal["lich_trinh", "chi_phi"]
TruongTen = Literal["so_ngay", "di_cung", "kieu_di", "so_thich", "so_nguoi", "muc_chi"]

# Trường theo loại (thứ tự = thứ tự hỏi / cắt; bắt buộc đứng trước) và trường bắt buộc (D2 — mặc định bộ đo C143).
TRUONG_THEO_LOAI: dict[str, tuple[str, ...]] = {
    "lich_trinh": ("so_ngay", "di_cung", "kieu_di", "so_thich"),
    "chi_phi": ("so_nguoi", "so_ngay", "muc_chi"),
}
BAT_BUOC: dict[str, tuple[str, ...]] = {"lich_trinh": ("so_ngay",), "chi_phi": ("so_nguoi", "so_ngay")}
MAX_TRUONG = 3

# Nhãn nút: tên trường + từng giá trị cho phép (giá trị = khoá bộ đo C143). Nhãn dùng cả cho câu ghép.
NHAN_TRUONG = {"so_ngay": "Số ngày", "di_cung": "Đi cùng ai", "kieu_di": "Kiểu đi", "so_thich": "Sở thích", "so_nguoi": "Số người", "muc_chi": "Mức chi"}
GIA_TRI: dict[str, dict[str, str]] = {
    "so_ngay": {"1": "1 ngày", "2": "2 ngày", "3": "3 ngày", "4+": "từ 4 ngày"},
    "di_cung": {"mot_minh": "đi một mình", "cap_doi": "đi hai người (cặp đôi)", "gia_dinh_tre_em": "gia đình có trẻ em",
                "nguoi_lon_tuoi": "có người lớn tuổi", "nhom_ban": "nhóm bạn"},
    "kieu_di": {"thong_tha": "đi thong thả", "day_lich": "đi dày lịch"},
    "so_thich": {"di_tich": "thích di tích", "am_thuc": "thích ẩm thực", "thien_nhien": "thích thiên nhiên",
                 "le_hoi_nghe_thuat": "thích lễ hội, nghệ thuật", "chup_anh": "thích chụp ảnh"},
    "so_nguoi": {"1": "1 người", "2": "2 người", "3-4": "3–4 người", "5+": "từ 5 người"},
    "muc_chi": {"tiet_kiem": "mức chi tiết kiệm", "tieu_chuan": "mức chi tiêu chuẩn", "thoai_mai": "mức chi thoải mái"},
}


class TruongInput(BaseModel):
    """Giá trị người dùng chọn ở nút (D4): dữ liệu không tin cậy từ trình duyệt ⇒ chỉ đúng tập giá trị trên, trường lạ ⇒ 422.
    Rỗng (`{}`) = "Trả lời luôn" (không hỏi lại nữa)."""
    model_config = ConfigDict(extra="forbid")
    so_ngay: Literal["1", "2", "3", "4+"] | None = None
    di_cung: Literal["mot_minh", "cap_doi", "gia_dinh_tre_em", "nguoi_lon_tuoi", "nhom_ban"] | None = None
    kieu_di: Literal["thong_tha", "day_lich"] | None = None
    so_thich: Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"] | None = None
    so_nguoi: Literal["1", "2", "3-4", "5+"] | None = None
    muc_chi: Literal["tiet_kiem", "tieu_chuan", "thoai_mai"] | None = None


def loc_truong(loai: str, truong_thieu: list[str]) -> tuple[list[str], str | None]:
    """D3 — ranh giới, không phải phép đo: bỏ trường không thuộc `loai` (giữ thứ tự bảng, bỏ trùng); rỗng ⇒ trường bắt buộc của `loai`;
    > 3 ⇒ giữ 3 theo thứ tự bảng. Trả (danh sách, "dien" | "cat" | None) — harness đếm số lần code phải điền / cắt (plan M-1)."""
    thuoc = [t for t in TRUONG_THEO_LOAI[loai] if t in set(truong_thieu)]
    if not thuoc:
        return list(BAT_BUOC[loai]), "dien"
    if len(thuoc) > MAX_TRUONG:
        return thuoc[:MAX_TRUONG], "cat"
    return thuoc, None


def the_hoi_lai(loai: str, truong: list[str], cau_goc: str) -> dict:
    """Dữ liệu thẻ hỏi lại cho giao diện (sự kiện `clarify` / trường `clarify` của `/api/chat`) — code dựng nút từ bảng (spec §3)."""
    return {"loai": loai, "cau_goc": cau_goc, "bat_buoc": [t for t in truong if t in BAT_BUOC[loai]],
            "truong": [{"ten": t, "nhan": NHAN_TRUONG[t], "lua_chon": [{"gia_tri": k, "nhan": v} for k, v in GIA_TRI[t].items()]} for t in truong]}


def ghep_cau(cau_goc: str, truong: TruongInput) -> str:
    """D4: câu gốc + giá trị đã chọn ⇒ một câu đủ ý, chữ từ bảng nhãn (tất định). Không chọn gì ("Trả lời luôn") ⇒ đúng câu gốc."""
    chon = [GIA_TRI[ten][gia_tri] for ten, gia_tri in truong.model_dump(exclude_none=True).items()]
    cau = cau_goc.strip()
    return cau if not chon else f"{cau} (Thông tin thêm: {'; '.join(chon)}.)"
