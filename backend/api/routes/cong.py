"""API chỉ đọc của cổng du lịch đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` D6): danh sách bài kho cho trang
Khám phá, một bài, ô thời tiết trang chủ, cờ tính năng, lịch mẫu của trang Lên kế hoạch. Không gọi model, không ghi gì.

Bài kho = đúng các file runtime của chỉ mục: lúc khởi động `build_full_corpus_retrieval_service` đã kiểm danh sách + hash file khớp build record
(`corpus.sources`), rồi `api/app.py` mới nạp danh sách này. `id` bài từ trình duyệt chỉ được **so nguyên chuỗi** với danh sách đó — không ghép
đường dẫn từ chữ người dùng (không đọc được file ngoài danh sách)."""
from pathlib import Path

from fastapi import APIRouter, Query, Request

from api.routes.chat import _flags, error_response
from ingestion.source_state import read_source_lf
from llm import lich_trinh_v2 as lt2
from llm import thoi_tiet as tt
from llm.hoi_lai import SO_NGAY_TOI_DA, SO_THICH_TOI_DA

router = APIRouter()

TOM_TAT_MAX = 200  # ký tự của dòng tóm tắt trên thẻ (spec D10: 1–2 dòng)
_KHONG_PHAI_BAI = ("evaluation/", "meta/", "_source-dumps/")  # thư mục không bao giờ là bài (discover đã loại; giữ thêm một lớp rẻ — spec §7)


def _bi_chan(bai_id: str) -> bool:
    return ".." in bai_id or bai_id.startswith(("/", *_KHONG_PHAI_BAI)) or "sealed" in bai_id


def _tieu_de(markdown: str, bai_id: str) -> str:
    dong = next((d for d in markdown.splitlines() if d.startswith("# ")), None)
    return dong[2:].strip() if dong else Path(bai_id).stem


def _doan_dau(markdown: str, bo_danh_sach: bool) -> list[str]:
    """Các dòng của khối văn đầu tiên (bỏ tiêu đề mục, bảng, kẻ ngang; `bo_danh_sach` ⇒ bỏ cả dòng gạch đầu)."""
    doan: list[str] = []
    for dong in markdown.splitlines():
        dong = dong.strip()
        bo = dong.startswith(("#", "|", "---")) or (bo_danh_sach and dong.startswith(("- ", "* ")))
        if not dong or bo:
            if doan:
                break
            continue
        doan.append(dong.lstrip(">-* ").strip())
    return doan


def _tom_tat(markdown: str) -> str:
    """Đoạn **văn xuôi** đầu tiên, bỏ dấu đậm / nghiêng, cắt ở ranh giới chữ ≤ `TOM_TAT_MAX`.

    Bỏ dòng gạch đầu: ~100 / 204 bài mở bằng mục "Thông tin chung" dạng "- **Tên chính thức:** …" ⇒ thẻ hiện nhãn trường thay vì lời giới thiệu
    (S2 m: CONG/s2_implementation.md). Bài chỉ có danh sách (không có đoạn văn) ⇒ lấy khối danh sách đầu như trước."""
    doan = _doan_dau(markdown, bo_danh_sach=True) or _doan_dau(markdown, bo_danh_sach=False)
    chu = " ".join(doan).replace("*", "").replace("__", "")
    if len(chu) <= TOM_TAT_MAX:
        return chu
    return chu[:TOM_TAT_MAX].rsplit(" ", 1)[0] + "…"


def nap_kham_pha(root: Path, rel_paths: list[str]) -> dict[str, dict]:
    """Bài kho theo `id` = đường dẫn tương đối của file runtime. Giữ cả Markdown trong RAM: kho chỉ đổi khi build lại chỉ mục (khởi động lại)."""
    bai = {}
    for rel in rel_paths:
        if _bi_chan(rel):
            continue
        markdown = read_source_lf(root / rel)
        phan = rel.split("/")
        bai[rel] = {"id": rel, "linh_vuc": phan[0], "loai_con": phan[1] if len(phan) > 2 else None,
                    "tieu_de": _tieu_de(markdown, rel), "tom_tat": _tom_tat(markdown), "markdown": markdown}
    return bai


def _chua_san_sang():
    return error_response(503, "kham_pha_unavailable", "Danh sách bài tạm thời chưa có.")


def _khong_thay():
    return error_response(404, "not_found", "Không tìm thấy.")


@router.get("/api/kham_pha")
async def danh_sach(request: Request):
    """Mọi bài (không Markdown) — trang danh sách lọc theo `linh_vuc` / `loai_con` ở giao diện (204 bài, nhỏ)."""
    bai = getattr(request.app.state, "kham_pha", None)
    if bai is None:
        return _chua_san_sang()
    return {"bai": [{k: b[k] for k in ("id", "linh_vuc", "loai_con", "tieu_de", "tom_tat")} for b in bai.values()]}


@router.get("/api/kham_pha/bai")
async def mot_bai(request: Request, id: str = Query(min_length=1, max_length=300)):
    bai = getattr(request.app.state, "kham_pha", None)
    if bai is None:
        return _chua_san_sang()
    b = None if _bi_chan(id) else bai.get(id)  # so nguyên chuỗi với danh sách
    if b is None:
        return _khong_thay()
    return {k: b[k] for k in ("id", "linh_vuc", "loai_con", "tieu_de", "markdown")}


@router.get("/api/thoi_tiet")
async def thoi_tiet(request: Request):
    """Ô thời tiết hôm nay: cùng hàm + cache 30 phút của công cụ thời tiết (B5b); số do code đọc từ Open-Meteo, không model. Cờ tắt ⇒ 404;
    lỗi ⇒ chỉ trạng thái (giao diện ẩn ô — không số cũ / số đoán)."""
    flags = _flags(request.app.state)
    if not flags.thoi_tiet:
        return _khong_thay()
    kq = await flags.du_bao()
    if kq.trang_thai != "ok":
        return {"trang_thai": "loi"}
    d = kq.ngay[0]
    return {"trang_thai": "ok", "hom_nay": {"tmax": d["tmax"], "tmin": d["tmin"], "xs_mua": d["xs"]}, "cap_nhat": kq.cap_nhat,
            "ghi_cong": tt.GHI_CONG}


@router.get("/api/tinh_nang")
async def tinh_nang(request: Request):
    """Cờ tính năng giao diện cần để ẩn / hiện mục (một lần gọi lúc tải trang). Chỉ boolean — trừ khoá `len_ke_hoach_v2`: **chỉ có khi cờ bật**
    (cờ tắt ⇒ khoá vắng hẳn, phản hồi giống hôm nay — plan đợt 1 ý 1), mang các ô biểu mẫu hiện + giới hạn của bộ xếp đang dùng (ý 7)."""
    state = request.app.state
    flags = _flags(state)
    co = {"lich_trinh_bieu_mau": flags.lich_trinh_bieu_mau, "thoi_tiet": flags.thoi_tiet, "anh": getattr(state, "anh", None) is not None,
          "tra_web": flags.tra_web, "ban_do_lich": flags.ban_do_lich}
    if flags.len_ke_hoach_v2:
        co["len_ke_hoach_v2"] = {"o_hien": list(flags.len_ke_hoach_o_hien), "so_ngay_toi_da": SO_NGAY_TOI_DA, "so_thich_toi_da": SO_THICH_TOI_DA,
                                 "so_thich_hien": list(flags.so_thich_hien)}  # loại < 4 điểm hoặc dưới sàn mô phỏng ⇒ không hiện
    return co


# Lịch mẫu "Ví dụ" (User 14/11: trang Lên kế hoạch lúc chưa xếp quá trống). Tổ hợp cố định A chốt: 2 ngày · 2 người lớn · cân bằng · thích di
# tích; không ngày đi (không dự báo, không đoán thứ). Do CHÍNH bộ xếp đang chạy dựng (`xep_v2` + `dung_lich`) ⇒ ví dụ không hứa điều bộ xếp không
# làm. Không câu tả (thẻ đã có nhãn loại điểm), không gọi model, không nguồn — câu tả từ kho chỉ có ở lịch thật. Bảng nạp một lần lúc khởi động ⇒ dựng một
# lần rồi giữ (khoá theo id bảng).
TRUONG_MAU = {"so_ngay": "2", "nguoi_lon": 2, "kieu_di": "can_bang", "so_thich": ["di_tich"]}
_mau: dict[int, dict] = {}


def dung_lich_mau(flags) -> dict:
    """Cùng các bước của lịch thật trừ phần cần model / kho: xếp ⇒ dựng ⇒ gắn nơi ở + quán theo cờ (`len_ke_hoach.gan_o_an`)."""
    from llm.len_ke_hoach import gan_o_an  # import muộn như các route khác dùng lõi trợ lý
    bang = flags.bang_lich_v2
    khung = lt2.xep_v2(bang, lt2.tu_truong(TRUONG_MAU))
    lich = lt2.dung_lich(bang, khung, {}, None, (), None, flags.anh_lich_bang if flags.anh_lich else None)
    gan_o_an(lich, bang, khung, flags)
    cau = {m["id_muc"]: "" for m in lt2.moi_muc(lich)}  # nhãn loại điểm đã hiện trên thẻ ⇒ không câu lặp; "" = đã xong (không vẽ "đang viết…")
    return {"lich": lich, "cau": cau, "truong": TRUONG_MAU}  # `truong`: nút "Xếp lịch như ví dụ" gửi đúng tổ hợp này


@router.get("/api/lich_mau")
async def lich_mau(request: Request):
    """Lịch mẫu cho trang Lên kế hoạch lúc chưa xếp. Cờ `len_ke_hoach_v2` tắt ⇒ 404."""
    flags = _flags(request.app.state)
    if not flags.len_ke_hoach_v2:
        return _khong_thay()
    if id(flags) not in _mau:  # cờ + bảng nạp một lần lúc khởi động ⇒ dựng một lần cho bộ cờ đó
        _mau[id(flags)] = dung_lich_mau(flags)
    return _mau[id(flags)]
