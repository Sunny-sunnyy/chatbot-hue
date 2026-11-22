"""Phép kiểm "cập nhật riêng bài đã sửa GIỐNG dựng lại toàn bộ" (mục "trợ lý đề xuất sửa kho", 22/11/2026). CHỈ ĐỌC: không ghi Qdrant, không ghi file.

Ba collection:
- `truoc`    — chỉ mục trước khi sửa kho (collection đang chạy hoặc bản chép nguyên trạng của nó);
- `sau`      — collection thử sau khi lệnh cập nhật riêng (`ingestion/cap_nhat_rieng.py`) chạy xong;
- `dung_lai` — collection thử dựng lại TOÀN BỘ từ kho đã sửa (`build_candidate(collection_name=…)`).

Tiêu chí ghi trước (phiên điều phối nhận 08:2x 22/11/2026):
1. `sau` ↔ `dung_lai`: cùng tập mã điểm; payload và vector từ khoá giống hệt; vector nghĩa lệch không quá ngưỡng (mặc định 1e-5).
   Vì sao không đòi vector nghĩa giống từng byte: model tính theo lô 8 đoạn, lô khác thành phần thì lệch cỡ 1e-7 (đo 22/11: cùng thứ tự lô ⇒ giống từng byte).
2. `sau` ↔ `truoc`: điểm cùng mã + cùng payload phải giữ vector nghĩa từng byte (đoạn không đổi chữ thì không được tính lại); điểm mới / đổi payload / bị xoá
   chỉ được thuộc các bài khai là đã sửa. Vector từ khoá của điểm không sửa ĐƯỢC PHÉP đổi: nó phụ thuộc idf, độ dài trung bình và số thứ tự từ vựng của CẢ kho.
3. File thống kê từ khoá giống từng byte; bản ghi dựng giống nhau trừ tên collection.
4. Mỗi câu của bộ câu hỏi: các đoạn đầu ra cùng mã, cùng thứ tự ở `sau` và `dung_lai`, qua đúng dịch vụ tìm đang chạy.

Chạy từ `backend/`:
    uv run python -m ingestion.kiem_cap_nhat_rieng --truoc <collection> --sau <collection> --dung-lai <collection> --bai <bài đã sửa…> \
        --thong-ke-sau <file> --thong-ke-dung-lai <file> --ban-ghi-sau <file> --ban-ghi-dung-lai <file>
Mã thoát 0 = mọi phép đạt; 1 = có phép không đạt (in từng chỗ lệch).
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import json
from pathlib import Path
import sys

import numpy as np
from qdrant_client import QdrantClient

from core.settings_loader import load_settings
from embedding.full_corpus import create_dense_runner
from embedding.sparse import build_vocabulary_index, load_sparse_state
from retrieval.full_corpus import FullCorpusRetrievalService, candidate_by_id
from vectorstore.qdrant import DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME, client_from_settings
from vectorstore.upsert import FULL_CORPUS_SCROLL_LIMIT

NGUONG_VECTOR_NGHIA = 1e-5
BO_CAU_HOI = Path(__file__).resolve().parents[2] / "knowledge-base-hue" / "evaluation" / "golden_full_corpus.jsonl"
QDRANT_TIMEOUT = 30


@dataclass(frozen=True)
class Diem:
    """Một điểm đọc từ Qdrant: payload, vector nghĩa (float32) và vector từ khoá (số thứ tự từ, giá trị)."""

    payload: dict
    nghia: np.ndarray
    tu_khoa: tuple[tuple[int, ...], tuple[float, ...]]


def doc_collection(client: QdrantClient, ten: str) -> dict[str, Diem]:
    """Đọc mọi điểm của một collection (mã điểm ⇒ `Diem`). Điểm không có vector từ khoá (đoạn không có từ nào) ⇒ vector rỗng."""
    diem: dict[str, Diem] = {}
    offset = None
    while True:
        ban_ghi, offset = client.scroll(ten, limit=FULL_CORPUS_SCROLL_LIMIT, offset=offset, with_payload=True, with_vectors=True, timeout=QDRANT_TIMEOUT)
        for r in ban_ghi:
            tu_khoa = r.vector.get(SPARSE_VECTOR_NAME)
            diem[str(r.id)] = Diem(
                payload=r.payload,
                nghia=np.asarray(r.vector[DENSE_VECTOR_NAME], dtype=np.float32),
                tu_khoa=(tuple(tu_khoa.indices), tuple(tu_khoa.values)) if tu_khoa is not None else ((), ()),
            )
        if offset is None:
            return diem


def _vi_du(ma: set[str] | list[str]) -> str:
    return ", ".join(sorted(ma)[:3])


def so_voi_dung_lai(sau: dict[str, Diem], dung_lai: dict[str, Diem], nguong: float = NGUONG_VECTOR_NGHIA) -> tuple[list[str], dict]:
    """Tiêu chí 1. Trả (các chỗ lệch, số đếm)."""
    loi: list[str] = []
    thieu, thua = dung_lai.keys() - sau.keys(), sau.keys() - dung_lai.keys()
    if thieu:
        loi.append(f"{len(thieu)} điểm có ở bản dựng lại mà thiếu ở bản cập nhật riêng (ví dụ {_vi_du(thieu)})")
    if thua:
        loi.append(f"{len(thua)} điểm thừa ở bản cập nhật riêng, bản dựng lại không có (ví dụ {_vi_du(thua)})")
    chung = sau.keys() & dung_lai.keys()
    khac_payload = [i for i in chung if sau[i].payload != dung_lai[i].payload]
    khac_tu_khoa = [i for i in chung if sau[i].tu_khoa != dung_lai[i].tu_khoa]
    lech = {i: float(np.abs(sau[i].nghia - dung_lai[i].nghia).max()) for i in chung}
    qua_nguong = [i for i, d in lech.items() if not d <= nguong]  # viết "not <=" để NaN cũng tính là lệch
    if khac_payload:
        loi.append(f"{len(khac_payload)} điểm khác payload với bản dựng lại (ví dụ {_vi_du(khac_payload)})")
    if khac_tu_khoa:
        loi.append(f"{len(khac_tu_khoa)} điểm khác vector từ khoá với bản dựng lại (ví dụ {_vi_du(khac_tu_khoa)})")
    if qua_nguong:
        loi.append(f"{len(qua_nguong)} điểm có vector nghĩa lệch quá {nguong:g} so với bản dựng lại (ví dụ {_vi_du(qua_nguong)})")
    return loi, {"so_diem_chung": len(chung), "lech_vector_nghia_lon_nhat": max(lech.values(), default=0.0),
                 "vector_nghia_giong_tung_byte": sum(sau[i].nghia.tobytes() == dung_lai[i].nghia.tobytes() for i in chung)}


def so_voi_truoc(truoc: dict[str, Diem], sau: dict[str, Diem], bai_da_sua: set[str]) -> tuple[list[str], dict]:
    """Tiêu chí 2. `bai_da_sua` = giá trị `source` của các bài khai là đã sửa / thêm / xoá."""
    loi: list[str] = []
    chung = truoc.keys() & sau.keys()
    giu_chu = {i for i in chung if truoc[i].payload == sau[i].payload}
    tinh_lai_thua = [i for i in giu_chu if truoc[i].nghia.tobytes() != sau[i].nghia.tobytes()]
    if tinh_lai_thua:
        loi.append(f"{len(tinh_lai_thua)} điểm không đổi chữ mà vector nghĩa đã đổi so với trước (ví dụ {_vi_du(tinh_lai_thua)})")
    # mọi thay đổi (điểm mới, điểm bị xoá, điểm đổi payload) chỉ được nằm trong bài khai là đã sửa
    bai_cham = ({sau[i].payload["source"] for i in sau.keys() - truoc.keys()} | {truoc[i].payload["source"] for i in truoc.keys() - sau.keys()}
                | {sau[i].payload["source"] for i in chung - giu_chu})
    ngoai_khai = bai_cham - bai_da_sua
    if ngoai_khai:
        loi.append(f"{len(ngoai_khai)} bài có điểm thay đổi mà không khai là đã sửa (ví dụ {_vi_du(ngoai_khai)})")
    khong_cham = bai_da_sua - bai_cham
    if khong_cham:
        loi.append(f"{len(khong_cham)} bài khai là đã sửa nhưng không điểm nào của nó đổi (ví dụ {_vi_du(khong_cham)})")
    return loi, {"diem_giu_chu": len(giu_chu), "diem_moi": len(sau.keys() - truoc.keys()), "diem_bi_xoa": len(truoc.keys() - sau.keys()),
                 "diem_doi_chu": len(chung - giu_chu), "bai_co_thay_doi": len(bai_cham),
                 # không phải lỗi — cho thấy bước "ghi lại vector từ khoá cả kho" có thật sự được thử ở ca này
                 "diem_giu_chu_ma_vector_tu_khoa_doi": sum(truoc[i].tu_khoa != sau[i].tu_khoa for i in giu_chu)}


def so_file(thong_ke_sau: Path, thong_ke_dung_lai: Path, ban_ghi_sau: Path, ban_ghi_dung_lai: Path) -> list[str]:
    """Tiêu chí 3."""
    loi: list[str] = []
    if thong_ke_sau.read_bytes() != thong_ke_dung_lai.read_bytes():
        loi.append("file thống kê từ khoá của bản cập nhật riêng khác bản dựng lại")
    hai_ban = [json.loads(p.read_text(encoding="utf-8")) for p in (ban_ghi_sau, ban_ghi_dung_lai)]
    for ban in hai_ban:
        ban.pop("collection_name", None)  # hai collection thử khác tên là đúng
    if hai_ban[0] != hai_ban[1]:
        khoa = sorted(k for k in hai_ban[0].keys() | hai_ban[1].keys() if hai_ban[0].get(k) != hai_ban[1].get(k))
        loi.append(f"bản ghi dựng của bản cập nhật riêng khác bản dựng lại ở mục: {', '.join(khoa)}")
    return loi


def so_ket_qua_tim(dich_vu_sau: FullCorpusRetrievalService, dich_vu_dung_lai: FullCorpusRetrievalService, cau_hoi: list[str]) -> tuple[list[str], dict]:
    """Tiêu chí 4: mỗi câu, danh sách mã đoạn trả ra (đúng thứ tự) phải giống nhau ở hai collection. Không in chữ câu hỏi (bộ câu mẫu)."""
    lech = [so for so, cau in enumerate(cau_hoi)
            if [d.id for d in dich_vu_sau.search(cau).documents] != [d.id for d in dich_vu_dung_lai.search(cau).documents]]
    loi = [f"{len(lech)} / {len(cau_hoi)} câu hỏi ra danh sách đoạn khác nhau giữa bản cập nhật riêng và bản dựng lại (số thứ tự câu: {lech[:10]})"] if lech else []
    return loi, {"so_cau": len(cau_hoi), "so_cau_lech": len(lech)}


def main() -> int:
    parser = argparse.ArgumentParser(description="So bản cập nhật riêng với chỉ mục trước khi sửa và với bản dựng lại toàn bộ (chỉ đọc)")
    parser.add_argument("--truoc", required=True, help="collection trước khi sửa kho")
    parser.add_argument("--sau", required=True, help="collection thử sau khi cập nhật riêng")
    parser.add_argument("--dung-lai", required=True, help="collection thử dựng lại toàn bộ từ kho đã sửa")
    parser.add_argument("--bai", nargs="*", default=[], help="giá trị `source` của các bài đã sửa / thêm / xoá")
    # Bắt buộc, không mặc định về file đang chạy: quên truyền mà so file thật với chính nó thì phép kiểm đạt giả
    parser.add_argument("--thong-ke-sau", required=True, type=Path)
    parser.add_argument("--thong-ke-dung-lai", required=True, type=Path)
    parser.add_argument("--ban-ghi-sau", required=True, type=Path)
    parser.add_argument("--ban-ghi-dung-lai", required=True, type=Path)
    parser.add_argument("--nguong", type=float, default=NGUONG_VECTOR_NGHIA)
    parser.add_argument("--cau-hoi", type=Path, default=BO_CAU_HOI, help="file jsonl, mỗi dòng có khoá `question`")
    args = parser.parse_args()

    settings = load_settings()
    runtime = settings["full_corpus_runtime"]
    client = client_from_settings(settings)
    runner = create_dense_runner(candidate_by_id(runtime["candidate_id"]).dense_spec)
    try:
        truoc, sau, dung_lai = (doc_collection(client, ten) for ten in (args.truoc, args.sau, args.dung_lai))
        ket_qua = [("1. bản cập nhật riêng ↔ bản dựng lại toàn bộ", *so_voi_dung_lai(sau, dung_lai, args.nguong)),
                   ("2. bản cập nhật riêng ↔ chỉ mục trước khi sửa", *so_voi_truoc(truoc, sau, set(args.bai))),
                   ("3. file thống kê từ khoá + bản ghi dựng", so_file(args.thong_ke_sau, args.thong_ke_dung_lai, args.ban_ghi_sau, args.ban_ghi_dung_lai), {})]

        def dich_vu(ten: str, thong_ke: Path) -> FullCorpusRetrievalService:
            state = load_sparse_state(thong_ke)
            return FullCorpusRetrievalService(replace(candidate_by_id(runtime["candidate_id"]), collection_name=ten), runtime["retrieval_treatment"],
                                              runtime["reranker"], runner, state, build_vocabulary_index(state), client)

        cau_hoi = [json.loads(dong)["question"] for dong in args.cau_hoi.read_text(encoding="utf-8").splitlines() if dong.strip()]
        runner.load()
        ket_qua.append(("4. kết quả tìm của bộ câu hỏi", *so_ket_qua_tim(dich_vu(args.sau, args.thong_ke_sau), dich_vu(args.dung_lai, args.thong_ke_dung_lai), cau_hoi)))
    finally:
        runner.close()
        client.close()

    print(f"số điểm: trước {len(truoc)} · sau {len(sau)} · dựng lại {len(dung_lai)}")
    for ten, loi, so in ket_qua:
        print(f"{'ĐẠT      ' if not loi else 'KHÔNG ĐẠT'} {ten}" + (f" — {json.dumps(so, ensure_ascii=False)}" if so else ""))
        for dong in loi:
            print(f"    - {dong}")
    return 1 if any(loi for _, loi, _ in ket_qua) else 0


if __name__ == "__main__":
    sys.exit(main())
