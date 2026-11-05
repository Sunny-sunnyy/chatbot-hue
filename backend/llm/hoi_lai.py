"""Hỏi lại khi câu lịch trình thiếu thông tin (Phase 9 B4, plan `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 2 `42fa62d2425f`;
**B4b — bản 8 `69afbb2732cf` D2′:** chỉ còn loại lịch trình — câu chi phí giữ hành vi `main` vì B4 âm ở câu chi phí, report B4 §2e / §2f).

**B5 (plan B5 bản 7 D15, User 10:07 05/11/2026 "code tự hỏi"; review C183 m-2):** công cụ `hoi_lai` cho model đã gỡ (luật lọc D3 cũng gỡ —
lịch sử ở tag `hoso/p9-b4`); **code** của công cụ `lich_trinh` tự trả thẻ khi thiếu số ngày. Ở đây còn: danh sách trường (D2 — khớp bộ đo C143
`data/phase_9/bo_do_b4/luat_ghi_truoc.md` và plan B5 D1), dữ liệu dựng nút (D8) và câu ghép đủ ý (D4). Không gọi mạng, không SDK — lõi và route đều dùng. Chữ người dùng thấy ở thẻ hỏi lại và câu ghép
là chữ cố định ở đây, không phải chữ model hay chữ tự do từ trình duyệt.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Trường theo loại (thứ tự = thứ tự hỏi / cắt; bắt buộc đứng trước) và trường bắt buộc (D2 — mặc định bộ đo C143).
TRUONG_THEO_LOAI: dict[str, tuple[str, ...]] = {
    "lich_trinh": ("so_ngay", "di_cung", "kieu_di", "so_thich"),
    "chi_phi": ("so_nguoi", "so_ngay", "muc_chi"),  # B5c D7: thẻ do code của `tinh_tien` dựng (chỉ trường còn thiếu); thẻ "Sửa" có đủ 3
}
BAT_BUOC: dict[str, tuple[str, ...]] = {"lich_trinh": ("so_ngay",), "chi_phi": ("so_nguoi", "so_ngay")}

# Nhãn nút: tên trường + từng giá trị cho phép (giá trị = khoá bộ đo C143). Nhãn dùng cả cho câu ghép.
NHAN_TRUONG = {"so_ngay": "Số ngày", "di_cung": "Đi cùng ai", "kieu_di": "Kiểu đi", "so_thich": "Sở thích", "so_nguoi": "Số người",
               "muc_chi": "Mức chi"}
GIA_TRI: dict[str, dict[str, str]] = {
    "so_ngay": {"1": "1 ngày", "2": "2 ngày", "3": "3 ngày", "4+": "từ 4 ngày"},
    "di_cung": {"mot_minh": "đi một mình", "cap_doi": "đi hai người (cặp đôi)", "gia_dinh_tre_em": "gia đình có trẻ em",
                "nguoi_lon_tuoi": "có người lớn tuổi", "nhom_ban": "nhóm bạn"},
    "kieu_di": {"thong_tha": "đi thong thả", "day_lich": "đi dày lịch"},
    "so_thich": {"di_tich": "thích di tích", "am_thuc": "thích ẩm thực", "thien_nhien": "thích thiên nhiên",
                 "le_hoi_nghe_thuat": "thích lễ hội, nghệ thuật", "chup_anh": "thích chụp ảnh"},
    # B5c D7: nút 1–5 + "6+" (giao diện mở ô số 6–20; giá trị gửi lên là số nguyên — `TruongInput.so_nguoi`)
    "so_nguoi": {"1": "1 người", "2": "2 người", "3": "3 người", "4": "4 người", "5": "5 người", "6+": "6 người trở lên"},
    "muc_chi": {"tiet_kiem": "mức tiết kiệm", "tieu_chuan": "mức tiêu chuẩn", "thoai_mai": "mức thoải mái"},
}
MAX_SO_NGUOI = 20


class TruongInput(BaseModel):
    """Giá trị người dùng chọn ở nút (D4): dữ liệu không tin cậy từ trình duyệt ⇒ chỉ đúng tập giá trị trên, trường lạ ⇒ 422.
    Rỗng (`{}`) = "Trả lời luôn" (không hỏi lại nữa)."""
    model_config = ConfigDict(extra="forbid")
    so_ngay: Literal["1", "2", "3", "4+"] | None = None
    di_cung: Literal["mot_minh", "cap_doi", "gia_dinh_tre_em", "nguoi_lon_tuoi", "nhom_ban"] | None = None
    kieu_di: Literal["thong_tha", "day_lich"] | None = None
    so_thich: Literal["di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh"] | None = None
    so_nguoi: int | None = Field(default=None, ge=1, le=MAX_SO_NGUOI)  # B5c D7: số nguyên 1–20 (khoảng không nhân được — lệch B4 D2 cũ)
    muc_chi: Literal["tiet_kiem", "tieu_chuan", "thoai_mai"] | None = None


def the_hoi_lai(loai: str, truong: list[str], cau_goc: str) -> dict:
    """Dữ liệu thẻ hỏi lại cho giao diện (sự kiện `clarify` / trường `clarify` của `/api/chat`) — code dựng nút từ bảng (spec §3)."""
    return {"loai": loai, "cau_goc": cau_goc, "bat_buoc": [t for t in truong if t in BAT_BUOC[loai]],
            "truong": [{"ten": t, "nhan": NHAN_TRUONG[t], "lua_chon": [{"gia_tri": k, "nhan": v} for k, v in GIA_TRI[t].items()]} for t in truong]}


def ghep_cau(cau_goc: str, truong: TruongInput) -> str:
    """D4: câu gốc + giá trị đã chọn ⇒ một câu đủ ý, chữ từ bảng nhãn (tất định). Không chọn gì ("Trả lời luôn") ⇒ đúng câu gốc."""
    chon = [f"{gia_tri} người" if ten == "so_nguoi" else GIA_TRI[ten][gia_tri] for ten, gia_tri in truong.model_dump(exclude_none=True).items()]
    cau = cau_goc.strip()
    return cau if not chon else f"{cau} (Thông tin thêm: {'; '.join(chon)}.)"
