"""API chỉ đọc của cổng du lịch đợt 1 (spec `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` D6): danh sách bài kho cho trang
Khám phá, một bài, ô thời tiết trang chủ, cờ tính năng. Không gọi model, không ghi gì.

Bài kho = đúng các file runtime của chỉ mục: lúc khởi động `build_full_corpus_retrieval_service` đã kiểm danh sách + hash file khớp build record
(`corpus.sources`), rồi `api/app.py` mới nạp danh sách này. `id` bài từ trình duyệt chỉ được **so nguyên chuỗi** với danh sách đó — không ghép
đường dẫn từ chữ người dùng (không đọc được file ngoài danh sách)."""
from pathlib import Path

from fastapi import APIRouter, Query, Request

from api.routes.chat import _flags, error_response
from ingestion.source_state import read_source_lf
from llm import thoi_tiet as tt

router = APIRouter()

TOM_TAT_MAX = 200  # ký tự của dòng tóm tắt trên thẻ (spec D10: 1–2 dòng)
_KHONG_PHAI_BAI = ("evaluation/", "meta/", "_source-dumps/")  # thư mục không bao giờ là bài (discover đã loại; giữ thêm một lớp rẻ — spec §7)


def _bi_chan(bai_id: str) -> bool:
    return ".." in bai_id or bai_id.startswith(("/", *_KHONG_PHAI_BAI)) or "sealed" in bai_id


def _tieu_de(markdown: str, bai_id: str) -> str:
    dong = next((d for d in markdown.splitlines() if d.startswith("# ")), None)
    return dong[2:].strip() if dong else Path(bai_id).stem


def _tom_tat(markdown: str) -> str:
    """Đoạn văn đầu sau tiêu đề (bỏ dòng tiêu đề mục, bảng, kẻ ngang), bỏ dấu đậm / nghiêng, cắt ở ranh giới chữ ≤ `TOM_TAT_MAX`."""
    doan: list[str] = []
    for dong in markdown.splitlines():
        dong = dong.strip()
        if not dong:
            if doan:
                break
            continue
        if dong.startswith(("#", "|", "---")):
            if doan:
                break
            continue
        doan.append(dong.lstrip(">-* ").strip())
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
    """Cờ tính năng giao diện cần để ẩn / hiện mục (một lần gọi lúc tải trang). Chỉ boolean."""
    state = request.app.state
    flags = _flags(state)
    return {"lich_trinh_bieu_mau": flags.lich_trinh_bieu_mau, "thoi_tiet": flags.thoi_tiet, "anh": getattr(state, "anh", None) is not None,
            "tra_web": flags.tra_web, "ban_do_lich": flags.ban_do_lich}
