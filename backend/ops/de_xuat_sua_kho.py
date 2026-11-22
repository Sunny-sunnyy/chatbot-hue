"""Lệnh 1 / 2 — ĐỀ XUẤT sửa kho khi một mức giá đổi. KHÔNG ghi vào kho: chỉ đọc kho, gọi model một lần, ghi ra một thư mục đề xuất.

Chạy từ `backend/` (cần biến môi trường của model đang chạy, như lúc bật server — `guides/DOI_MODEL_VIET.md`):

    uv run python -m ops.de_xuat_sua_kho --gia "vé vào cổng Đại Nội, người lớn" --cu 200.000 --moi 250.000 --nguon "https://…"

Chưa biết kho đang ghi giá cũ là bao nhiêu ⇒ hỏi kho trước (không gọi model, 0 đồng):

    uv run python -m ops.de_xuat_sua_kho --noi "Đại Nội"

Ra: `data/de_xuat_kho/<ngày_giờ>/DE_XUAT.md` (bản để đọc) · `de_xuat.patch` (file vá) · `vet.json` (vết máy đọc, lệnh duyệt dùng).
Duyệt: `uv run python -m ops.duyet_sua_kho <thư mục đó>`. Lõi: `ops/sua_kho.py`.
"""
from __future__ import annotations

import argparse
import asyncio
import copy
import dataclasses
import datetime as dt
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from core.settings_loader import BACKEND_DIR, load_settings
from ingestion.source_state import discover_full_corpus_files
from ops import sua_kho

GOC_REPO = BACKEND_DIR.parent
HAN_GIO_MODEL = 180  # giây — một lời gọi phán vài chục chỗ ở mức suy luận cao; hạn 45 giây của lượt chat không đủ


def cac_bai_kho(settings: dict, goc_kho: Path) -> tuple[list[str], set[str]]:
    """(mọi bài của kho tính cả ba file kiểm kê, tập file kiểm kê — nằm trong kho nhưng không vào chỉ mục). Cùng bộ dò file với lúc dựng chỉ mục."""
    s = copy.deepcopy(settings)
    kb = s["full_corpus"]["knowledge_base"]
    kb["root_dir"] = str(goc_kho)
    _, trong_chi_muc = discover_full_corpus_files(s)
    kb["exclude_files"] = []
    _, tat_ca = discover_full_corpus_files(s)
    return tat_ca, set(tat_ca) - set(trong_chi_muc)


def in_cac_gia_canh_ten(goc_kho: Path, cac_bai: list[str], noi: str) -> None:
    """Chế độ hỏi kho: các con số tiền (từ 1.000) đứng trên những dòng có nhắc `noi`, gom theo giá trị."""
    dem, vi_du = Counter(), {}
    for bai in cac_bai:
        for so_dong, dong in enumerate((goc_kho / bai).read_text(encoding="utf-8").splitlines(), 1):
            if noi.casefold() not in dong.casefold():
                continue
            for m in sua_kho._SO.finditer(dong):
                v = sua_kho.gia_tri(m["so"], m["dv"])
                if v and v >= 1000 and (m["dv"] or not m["so"].isdigit()):  # số trơn bốn chữ số không nhóm nghìn thường là năm ("2026")
                    dem[v] += 1
                    vi_du.setdefault(v, f"{Path(bai).stem}, dòng {so_dong}: {dong.strip()[:140]}")
    if not dem:
        print(f"Không dòng nào trong kho vừa nhắc «{noi}» vừa có số tiền.")
        return
    print(f"Các số tiền đứng cùng dòng với «{noi}» trong kho (số lần · ví dụ một dòng):")
    for v, so_lan in sorted(dem.items(), key=lambda x: -x[1]):
        print(f"  {sua_kho.nhom_nghin(v):>12} · {so_lan:>2} lần · {vi_du[v]}")
    print("\nChọn đúng mức giá đã đổi rồi chạy lại với --gia \"<mô tả mức giá>\" --cu <giá cũ> --moi <giá mới> --nguon <link hoặc nơi lấy giá>.")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Đề xuất sửa kho khi một mức giá đổi (không ghi kho).")
    p.add_argument("--gia", help='mô tả mức giá đã đổi, lời thường — ví dụ "vé vào cổng Đại Nội, người lớn"')
    p.add_argument("--cu", help="giá cũ kho đang ghi, ví dụ 200.000")
    p.add_argument("--moi", help="giá mới, ví dụ 250.000")
    p.add_argument("--nguon", help="link hoặc nơi bạn lấy giá mới (ghi vào mục Nguồn dữ liệu của bài)")
    p.add_argument("--noi", help="chỉ hỏi kho: in các số tiền đang đứng cạnh tên nơi này rồi dừng (không gọi model)")
    p.add_argument("--goc", default=str(GOC_REPO), help="gốc repo có kho cần đọc (mặc định: repo này; dùng khi thử trên một bản chép)")
    p.add_argument("--ra", help="thư mục ghi đề xuất (mặc định: data/de_xuat_kho/<ngày_giờ>/)")
    a = p.parse_args(argv)

    settings = load_settings(validate_private_paths=False)
    goc = Path(a.goc).resolve()
    ten_kho = (BACKEND_DIR / settings["full_corpus"]["knowledge_base"]["root_dir"]).resolve().relative_to(GOC_REPO).as_posix()
    goc_kho = goc / ten_kho
    cac_bai, ngoai_chi_muc = cac_bai_kho(settings, goc_kho)

    if not a.cu:
        if not a.noi:
            p.error("thiếu --cu (giá cũ). Chưa biết kho đang ghi bao nhiêu thì chạy: --noi \"<tên nơi>\"")
        in_cac_gia_canh_ten(goc_kho, cac_bai, a.noi)
        return 0
    if not (a.gia and a.moi and a.nguon):
        p.error("cần đủ --gia (mô tả mức giá), --cu, --moi và --nguon")
    gia_cu, gia_moi = sua_kho.doc_gia(a.cu), sua_kho.doc_gia(a.moi)
    if gia_cu == gia_moi:
        p.error("giá mới bằng giá cũ — không có gì để sửa")

    cac_lan = sua_kho.quet_kho(goc_kho, cac_bai, ngoai_chi_muc, gia_cu)
    if not cac_lan:
        print(f"Kho không có chỗ nào ghi con số {sua_kho.nhom_nghin(gia_cu)}. Không có gì để đề xuất.")
        return 1
    print(f"Con số {sua_kho.nhom_nghin(gia_cu)} xuất hiện {len(cac_lan)} lần ở {len({x.bai for x in cac_lan})} bài. Đang hỏi model từng chỗ có phải «{a.gia}» không…")

    # import ở đây: chế độ hỏi kho (--noi) không cần nạp lớp gọi model
    from llm.generator_openai_full_corpus import CallLog, OpenAIFullCorpusGenerator
    settings["full_corpus_generation"]["timeout_seconds"] = HAN_GIO_MODEL
    generator = OpenAIFullCorpusGenerator.from_environment(settings)
    call_log = CallLog()
    dieu_la = asyncio.run(sua_kho.phan_doan(generator, a.gia, gia_cu, cac_lan, call_log, HAN_GIO_MODEL))
    tien = sum(c.get("usd") or 0 for c in call_log.calls)

    luc = dt.datetime.now()
    de_xuat = sua_kho.dung_de_xuat(goc_kho, ten_kho, cac_lan, gia_cu, gia_moi, a.gia, a.nguon, luc.strftime("%d/%m/%Y"))
    ra = Path(a.ra).resolve() if a.ra else GOC_REPO / "data" / "de_xuat_kho" / luc.strftime("%Y-%m-%d_%H%M%S")
    ra.mkdir(parents=True, exist_ok=False)  # mỗi lần chạy một thư mục mới, không ghi đè đề xuất cũ

    def git(*lenh: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-c", "core.quotepath=false", "-C", str(goc), *lenh], capture_output=True, text=True)

    ban_kho = git("rev-parse", "--short", "HEAD").stdout.strip() or "không rõ"
    lenh_duyet = f'uv run python -m ops.duyet_sua_kho "{ra}"' + ("" if goc == GOC_REPO else f' --goc "{goc}"')
    # Các bảng JSON ngoài kho mà trợ lý dùng (bảng điểm / quán của trang Lên kế hoạch, bảng sự kiện theo ngày…): chỉ BÁO — có ghi con số cũ
    # không, có câu chép nguyên văn từ một bài mà câu đó vừa đổi không. Lệnh này không sửa bảng; chữ của bảng không gửi model.
    ngoai_kho, bang_lech = [], []
    bai_cu = {bai: (goc_kho / bai).read_text(encoding="utf-8") for bai in de_xuat.bai_moi}
    for gia_tri_cau_hinh in settings.get("assistant", {}).values():
        if isinstance(gia_tri_cau_hinh, str) and gia_tri_cau_hinh.endswith(".json") and (BACKEND_DIR / gia_tri_cau_hinh).exists():
            bang = BACKEND_DIR / gia_tri_cau_hinh
            so = sua_kho.dem_trong_file_khac(bang, gia_cu)
            if so:
                ngoai_kho.append((bang.name, so))
            bang_lech += [(bang.name, bai, cau) for bai, cau in sua_kho.cau_chep_bi_doi(bang, bai_cu, de_xuat.bai_moi)]
    cham = sua_kho.cham_file_dieu_kien(goc_kho / "meta" / "full_corpus_conditions.json", de_xuat.cac_lan)

    (ra / "de_xuat.patch").write_text(de_xuat.va, encoding="utf-8")
    (ra / "DE_XUAT.md").write_text(sua_kho.viet_ban_de_xuat(
        de_xuat, mo_ta=a.gia, gia_cu=gia_cu, gia_moi=gia_moi, nguon=a.nguon, luc=luc.strftime("%H:%M %d/%m/%Y"), ban_kho=ban_kho, tien_usd=tien,
        model=generator.model, lenh_duyet=lenh_duyet, ngoai_kho=ngoai_kho, bang_lech=bang_lech, cham_dieu_kien=cham, dieu_la=dieu_la),
        encoding="utf-8")
    (ra / "vet.json").write_text(json.dumps({
        "luc": luc.isoformat(timespec="seconds"), "mo_ta": a.gia, "gia_cu": gia_cu, "gia_moi": gia_moi, "nguon": a.nguon,
        "ten_kho": ten_kho, "ban_kho": ban_kho, "model": generator.model, "usd": tien, "cac_lan_goi_model": call_log.calls,
        # băm từng bài sẽ sửa, lúc đề xuất: lệnh duyệt từ chối nếu bài đã đổi từ đó
        "bam_bai": {bai: hashlib.sha256((goc_kho / bai).read_bytes()).hexdigest() for bai in de_xuat.bai_moi},
        "bai_ngoai_chi_muc": sorted(b for b in de_xuat.bai_moi if b in ngoai_chi_muc),
        "dieu_la": dieu_la, "xem_lai": de_xuat.xem_lai, "bang_lech": bang_lech, "bang_co_gia_cu": ngoai_kho, "cac_lan": [dataclasses.asdict(x) for x in cac_lan],
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    dem = Counter(x.phan_doan for x in cac_lan)
    print(f"Sẽ sửa {dem['dung']} chỗ ở {len(de_xuat.bai_moi)} bài · không rõ {dem['khong_ro']} · không phải giá này {dem['khong']} · model {tien:.4f} USD")
    if de_xuat.va:
        kiem = git("apply", "--check", str(ra / "de_xuat.patch"))
        if kiem.returncode != 0:
            print(f"LỖI: file vá không áp được vào kho hiện tại — KHÔNG duyệt đề xuất này.\n{kiem.stderr.strip()}", file=sys.stderr)
            return 2
    print(f"Kho CHƯA đổi. Đọc: {ra / 'DE_XUAT.md'}")
    if de_xuat.va:
        print(f"Duyệt (từ backend/): {lenh_duyet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
