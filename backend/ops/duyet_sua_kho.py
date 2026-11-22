"""Lệnh 2 / 2 — DUYỆT một đề xuất sửa kho: áp file vá vào kho, lưu một bản ghi git, rồi cập nhật chỉ mục cho riêng các bài đã sửa.

Chạy từ `backend/` sau khi đã ĐỌC `DE_XUAT.md` trong thư mục đề xuất:

    uv run python -m ops.duyet_sua_kho data/de_xuat_kho/<ngày_giờ>

Đây là lệnh DUY NHẤT của tính năng này ghi vào kho, và chỉ người giữ kho chạy (sửa kho thuộc hàng "Hỏi User trước" của bảng quyền — coding agent
không chạy lệnh này trên kho thật). Thử trên một bản chép: thêm `--goc <gốc repo bản chép> --thu` (chỉ áp, không commit, không đụng chỉ mục).
Lùi: `git revert <mã bản ghi>` rồi cập nhật chỉ mục lại.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from core.settings_loader import BACKEND_DIR

GOC_REPO = BACKEND_DIR.parent


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Duyệt một đề xuất sửa kho (áp file vá, lưu bản ghi git, cập nhật chỉ mục).")
    p.add_argument("thu_muc", help="thư mục đề xuất do ops.de_xuat_sua_kho tạo")
    p.add_argument("--goc", default=str(GOC_REPO), help="gốc repo có kho cần sửa (mặc định: repo này)")
    p.add_argument("--thu", action="store_true", help="chỉ áp vào kho của --goc; không commit, không cập nhật chỉ mục (để thử trên bản chép)")
    a = p.parse_args(argv)
    thu_muc, goc = Path(a.thu_muc).resolve(), Path(a.goc).resolve()
    vet = json.loads((thu_muc / "vet.json").read_text(encoding="utf-8"))
    va = thu_muc / "de_xuat.patch"
    cac_bai = [f"{vet['ten_kho']}/{bai}" for bai in vet["bam_bai"]]
    if not cac_bai:
        print("Đề xuất này không có chỗ nào để sửa.")
        return 1

    def git(*lenh: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-c", "core.quotepath=false", "-C", str(goc), *lenh], capture_output=True, text=True)

    # 1. Kho phải còn đúng như lúc đề xuất: bài đã đổi từ đó ⇒ số dòng trong bản đề xuất bạn đọc không còn đúng ⇒ dừng, đề xuất lại.
    da_doi = [bai for bai, bam in vet["bam_bai"].items() if hashlib.sha256((goc / vet["ten_kho"] / bai).read_bytes()).hexdigest() != bam]
    if da_doi:
        print("DỪNG: các bài sau đã đổi từ lúc lập đề xuất — chạy lại lệnh đề xuất rồi đọc bản mới:\n  " + "\n  ".join(da_doi), file=sys.stderr)
        return 2
    kiem = git("apply", "--check", str(va))
    if kiem.returncode != 0:
        print(f"DỪNG: file vá không áp được.\n{kiem.stderr.strip()}", file=sys.stderr)
        return 2

    # 2. Áp. Từ đây kho đã đổi trên đĩa; chưa có bản ghi git.
    ap = git("apply", str(va))
    if ap.returncode != 0:
        print(f"LỖI khi áp file vá.\n{ap.stderr.strip()}", file=sys.stderr)
        return 2
    print(f"Đã áp vào {len(cac_bai)} bài:\n" + git("diff", "--stat", "--", *cac_bai).stdout.rstrip())
    if a.thu:
        print("Chế độ thử: không commit, không cập nhật chỉ mục.")
        return 0

    # 3. Bản ghi git = dấu "đã duyệt" (ai, lúc nào, sửa gì). Chỉ đúng các bài của đề xuất; hook kiểm trước khi ghi vẫn chạy.
    def so(v: int) -> str:
        return f"{v:,}".replace(",", ".")
    loi = (f"kb: price update — {vet['mo_ta']}: {so(vet['gia_cu'])} -> {so(vet['gia_moi'])} "
           f"({sum(1 for x in vet['cac_lan'] if x['phan_doan'] == 'dung')} places in {len(cac_bai)} articles; source: {vet['nguon']})")
    for lenh in (("add", "--", *cac_bai), ("commit", "-m", loi, "--", *cac_bai)):
        buoc = git(*lenh)
        if buoc.returncode != 0:
            print(f"LỖI ở `git {lenh[0]}` — kho đã đổi trên đĩa nhưng CHƯA có bản ghi git; xem `git status`.\n{buoc.stdout}{buoc.stderr}", file=sys.stderr)
            return 2
    print("Đã lưu bản ghi git " + git("rev-parse", "--short", "HEAD").stdout.strip() + " (chưa đẩy lên GitHub).")
    # Lệnh cập nhật chỉ mục không lo các bảng CHÉP TỪ KHO (bảng sự kiện theo ngày, bảng quán của lịch). Bản đề xuất đã báo câu chép nào bị đổi
    # (mục 4); hai test dưới là phép kiểm đủ của hai bảng đó — in ra để người giữ kho / agent chạy, lệnh này không tự chạy bộ test.
    print("Kiểm các bảng chép từ kho (từ backend/, không nạp env):\n"
          "  uv run pytest tests/test_su_kien_theo_ngay.py -q -k quotes_its_source\n"
          "  uv run pytest tests/test_quan_lich.py -q -k marked_closed")

    # 4. Cập nhật chỉ mục cho riêng các bài đã sửa (để chatbot trả lời theo giá mới). File kiểm kê không nằm trong chỉ mục ⇒ bỏ qua.
    #    Lệnh cập nhật (`ingestion.cap_nhat_rieng`) TỰ DÒ bài nào khác chỉ mục; ở đây đối chiếu danh sách nó dò ra với đúng các bài vừa vá —
    #    lệch nghĩa là kho còn thay đổi khác chưa vào chỉ mục, hoặc bản vá không tới ⇒ không tin, dừng, in cả hai danh sách.
    can_cap_nhat = sorted(bai for bai in vet["bam_bai"] if bai not in set(vet.get("bai_ngoai_chi_muc", [])))
    if not can_cap_nhat:
        print("Các bài vừa sửa không nằm trong chỉ mục (file kiểm kê) — không cần cập nhật chỉ mục.")
        return 0
    if goc != GOC_REPO or importlib.util.find_spec("ingestion.cap_nhat_rieng") is None:
        print("CHƯA cập nhật chỉ mục (lệnh cập nhật riêng bài chưa có ở bản code này, hoặc kho vừa sửa không phải kho của server này).\n"
              "Tới khi cập nhật, chatbot vẫn trả lời theo giá cũ và server sẽ từ chối khởi động lại. Các bài cần cập nhật:\n  " + "\n  ".join(can_cap_nhat))
        return 3
    from ingestion import cap_nhat_rieng
    truoc = cap_nhat_rieng.dong_bo(chi_xem=True)
    if sorted(truoc["bai_doi"]) != can_cap_nhat:
        print("DỪNG trước khi đụng chỉ mục: các bài khác chỉ mục không trùng với các bài vừa sửa.\n  vừa sửa: " + ", ".join(can_cap_nhat)
              + "\n  khác chỉ mục: " + ", ".join(sorted(truoc["bai_doi"])) + "\nKho đã có bản ghi git; chỉ mục CHƯA đổi.", file=sys.stderr)
        return 3
    ket_qua = cap_nhat_rieng.dong_bo()
    print(f"Đã cập nhật chỉ mục cho {len(ket_qua['bai_doi'])} bài ({ket_qua['so_doan_tinh_lai']} đoạn tính lại, {ket_qua['giay']} giây). "
          "Khởi động lại server để chatbot trả lời theo giá mới.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
