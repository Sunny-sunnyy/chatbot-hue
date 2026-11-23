"""Dựng THƯ MỤC NGỮ CẢNH cho `docker build` — đúng những file ảnh app cần, không hơn.

Vì sao có (đếm 23/11/2026): bản nháp 16/11 chép tay danh sách file bảng ở HAI chỗ (Dockerfile + danh sách chừa) và đã mục hai lần — lần này lệch
4 file bảng + 4 bài kho so với `settings.yaml`. Ở đây danh sách được SINH từ chính thứ app đọc lúc khởi động:
  - code (`backend/`, `frontend/`, `pyproject.toml`, `uv.lock`): lấy từ MỘT commit bằng `git archive` ⇒ ảnh ứng với đúng một sha, không dính file
    sửa dở, `node_modules`, `dist`, log, ảnh riêng không vào git (`frontend/public/anh/rieng`);
  - bài kho: đúng các bài có trong bản ghi dựng chỉ mục, lấy từ cùng commit, so băm sha256 từng bài với bản ghi (app cũng so lúc khởi động —
    lệch thì app không trả lời được, nên dừng ở đây cho sớm);
  - file bảng riêng tư: mọi đường dẫn `../data/…` trong `backend/config/settings.yaml` CỦA commit đó + bản ghi dựng + thống kê từ khoá, chép từ
    thư mục `data/` của cây chính (thư mục này không vào git).
Không chép: `.env`, file khoá, bộ câu kín, bộ câu mẫu, `_source-dumps`, phần còn lại của `data/`. Chỉ mục Qdrant KHÔNG nằm trong ảnh (đi bằng bản chụp).

Chạy (thường qua `dung_anh.sh`):  uv run python deploy/docker/dung_ngu_canh.py --ref <commit> --du-lieu <cây chính>/data --ra <thư mục trống>
"""
import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import yaml

MA = ("backend/", "frontend/", "pyproject.toml", "uv.lock")
CAM = re.compile(r"sealed|(^|/)\.env|/rieng/|_source-dumps|/evaluation/", re.IGNORECASE)  # không bao giờ được vào phần dữ liệu của ảnh
BAN_GHI_DUNG = "full_corpus_builds"  # `backend/ingestion/full_corpus_pipeline.BUILD_RECORD_ROOT`
THONG_KE_TU_KHOA = "full_corpus_sparse_state.json"  # `…full_corpus_pipeline.SPARSE_STATE_PATH`


def dung(loi: str):
    sys.exit(f"DỪNG: {loi}")


def duong_dan_du_lieu(cau_hinh) -> set[str]:
    """Mọi chuỗi `../data/…` hoặc `../knowledge-base-hue/…` là GIÁ TRỊ trong settings.yaml (không tính chú thích), bỏ tiền tố `../`."""
    ra = set()

    def di(nut):
        if isinstance(nut, dict):
            for con in nut.values():
                di(con)
        elif isinstance(nut, list):
            for con in nut:
                di(con)
        elif isinstance(nut, str) and nut.startswith(("../data/", "../knowledge-base-hue/")):
            ra.add(nut[3:])

    di(cau_hinh)
    return ra


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ref", required=True, help="commit / nhánh lấy code + kho")
    p.add_argument("--du-lieu", required=True, type=Path, help="thư mục data/ của cây chính")
    p.add_argument("--ra", required=True, type=Path, help="thư mục ngữ cảnh (phải trống hoặc chưa có)")
    a = p.parse_args()
    if a.ra.exists() and any(a.ra.iterdir()):
        dung(f"{a.ra} không trống")
    a.ra.mkdir(parents=True, exist_ok=True)
    goc = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
    sha = subprocess.run(["git", "rev-parse", f"{a.ref}^{{commit}}"], capture_output=True, text=True, cwd=goc).stdout.strip()
    if not sha:
        dung(f"không có commit nào tên {a.ref}")

    # 1. Đúng HAI file của thư mục bản ghi dựng: bản ghi dựng duy nhất (file có khoá `corpus`, tên = tên collection) + thống kê từ khoá (tên cố định).
    #    File .json khác ai đó để tạm ở đó KHÔNG vào ảnh.
    thu_muc_ghi = a.du_lieu / BAN_GHI_DUNG
    co_kho = [(f, b) for f in sorted(thu_muc_ghi.glob("*.json")) if "corpus" in (b := json.loads(f.read_text(encoding="utf-8")))]
    if len(co_kho) != 1:
        dung(f"cần đúng MỘT bản ghi dựng trong {thu_muc_ghi}, thấy {len(co_kho)}")
    file_ghi, ban_ghi = co_kho[0]
    thong_ke = thu_muc_ghi / THONG_KE_TU_KHOA
    if not thong_ke.is_file() or hashlib.sha256(thong_ke.read_bytes()).hexdigest() != ban_ghi["sparse"]["state_sha256"]:
        dung(f"{thong_ke} thiếu hoặc không khớp băm ghi trong bản ghi dựng")
    bai = ban_ghi["corpus"]["sources"]  # {đường dẫn trong kho: sha256}

    # 2. Code + bài kho từ đúng commit đó, một lượt đọc `git archive`
    luong = subprocess.run(["git", "archive", "--format=tar", sha, *[m.rstrip("/") for m in MA], "knowledge-base-hue"], capture_output=True, cwd=goc)
    if luong.returncode:
        dung(f"git archive lỗi: {luong.stderr.decode()[:300]}")
    so_ma, lech = 0, []
    with tarfile.open(fileobj=io.BytesIO(luong.stdout)) as tar:
        cau_hinh = yaml.safe_load(tar.extractfile("backend/config/settings.yaml").read())
        can = duong_dan_du_lieu(cau_hinh)
        kho_khac = {d for d in can if d.startswith("knowledge-base-hue/") and "." in Path(d).name}  # file kho ngoài bài (bảng điều kiện); bỏ dòng trỏ thư mục gốc
        for muc in tar:
            if not muc.isfile():
                continue
            ten = muc.name
            if ten.startswith("knowledge-base-hue/"):
                trong_kho = ten[len("knowledge-base-hue/"):]
                if trong_kho in bai:
                    if hashlib.sha256(tar.extractfile(muc).read()).hexdigest() != bai[trong_kho]:
                        lech.append(trong_kho)
                elif ten not in kho_khac:
                    continue
            elif not ten.startswith(MA):
                continue
            else:
                so_ma += 1
            tar.extract(muc, a.ra, filter="data")
    thieu_bai = [b for b in bai if not (a.ra / "knowledge-base-hue" / b).is_file()]
    if lech or thieu_bai:
        dung(f"kho ở commit {sha[:8]} KHÁC chỉ mục đang có ({len(lech)} bài lệch băm, {len(thieu_bai)} bài thiếu; ví dụ {(lech + thieu_bai)[:3]}) "
             "⇒ chọn commit có kho khớp chỉ mục, hoặc cập nhật chỉ mục trước (runbook 5b)")
    thieu_kho = [d for d in kho_khac if not (a.ra / d).is_file()]

    # 3. File bảng riêng tư theo settings.yaml của commit đó
    rieng = sorted(d for d in can if d.startswith("data/"))
    thieu = [d for d in rieng if not (a.du_lieu.parent / d).is_file()] + thieu_kho
    if thieu:
        dung(f"settings.yaml của commit {sha[:8]} trỏ tới file không có trên máy: {thieu}")
    rieng += [f"data/{BAN_GHI_DUNG}/{f.name}" for f in (thong_ke, file_ghi)]
    for d in rieng:
        dich = a.ra / d
        dich.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(a.du_lieu.parent / d, dich)

    # 4. Không có thứ cấm trong phần dữ liệu (code `backend/`, `frontend/` là code công khai — có file tên chứa "golden", "evaluation")
    du_lieu_trong_anh = [str(f.relative_to(a.ra)) for goc_con in ("knowledge-base-hue", "data") for f in (a.ra / goc_con).rglob("*") if f.is_file()]
    cam = [d for d in du_lieu_trong_anh if CAM.search(d)]
    if cam:
        dung(f"file cấm lọt vào ngữ cảnh: {cam[:5]}")

    # 5. Bảng kê: người cầm gói đọc để biết ảnh mang gì
    ke = [f"commit: {sha}", f"bai_kho: {len(bai)} (khớp băm với bản ghi dựng; {ban_ghi['qdrant']['point_count']} điểm Qdrant)", f"file_code: {so_ma}",
          "file_rieng_tu (từ data/, KHÔNG có trong git — vì chúng mà ảnh không được đẩy lên kho ảnh công khai):"]
    ke += [f"  {d}  sha256={hashlib.sha256((a.ra / d).read_bytes()).hexdigest()[:16]}" for d in rieng]
    (a.ra / "DANH_SACH.txt").write_text("\n".join(ke) + "\n", encoding="utf-8")
    print(f"ngữ cảnh {a.ra}: commit {sha[:8]} · {so_ma} file code · {len(bai)} bài kho khớp băm · {len(rieng)} file riêng tư từ data/ · 0 file cấm")


if __name__ == "__main__":
    main()
