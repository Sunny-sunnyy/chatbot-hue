"""Cập nhật riêng phần chỉ mục của bài đã sửa — kéo collection về khớp kho mà KHÔNG tính lại vector nghĩa của cả kho (mục [7], 22/11/2026).

Dựng lại toàn bộ (`full_corpus_pipeline.build_candidate`) mất khoảng 225 giây vì tính vector nghĩa cho 9.436 đoạn; sửa một bài chỉ đổi vài đoạn.
Lệnh này: chia đoạn cả kho như lúc dựng ⇒ so payload từng điểm với collection đang có ⇒ xoá điểm thừa, tính vector nghĩa CHỈ cho đoạn khác chữ,
ghi lại vector từ khoá của mọi điểm (nó phụ thuộc thống kê của cả kho — `embedding/sparse.py`; chỉ CPU) ⇒ kiểm cả collection bằng hàm kiểm của
lúc dựng ⇒ ghi file thống kê từ khoá rồi bản ghi dựng SAU CÙNG. Kết quả phải giống dựng lại toàn bộ (vector nghĩa lệch cỡ 1e-7 do thành phần lô).

Lệnh chết giữa chừng: bản ghi dựng đã bị dời sang tên `….dang_cap_nhat` trước lần ghi Qdrant đầu tiên ⇒ server từ chối khởi động (phép kiểm sẵn
có "Build record does not exist") thay vì trả lời lệch; chạy lại lệnh là kéo về đúng, vì bước so là so với CHÍNH collection chứ không tin sổ.
Lùi một lần sửa kho: `git revert` bài rồi chạy lại chính lệnh này.

Chạy (từ `backend/`, TẮT server trước, bật lại sau khi xong — server đọc thống kê và xoá câu trả lời đã nhớ lúc khởi động):
    uv run python -m ingestion.cap_nhat_rieng --chi-xem     # chỉ in bài nào khác chỉ mục, không ghi gì
    uv run python -m ingestion.cap_nhat_rieng               # chạy thật
Thử trên bản chép (ba tham số đi cùng nhau): --kho <thư mục kho chép> --collection <tên thử> --thu-muc-ban-ghi <thư mục>.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import socket
import time
from typing import Any

from qdrant_client import QdrantClient, models

from core.schema import FullCorpusChunk, domain_for_source
from embedding.full_corpus import OpenRouterDenseRunner, create_dense_runner
from embedding.sparse import SparseState, build_vocabulary_index, compute_corpus_identity, encode_sparse_document, fit_sparse_state, write_sparse_state
from ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from ingestion.full_corpus_pipeline import BUILD_RECORD_ROOT, QDRANT_TIMEOUT, SPARSE_STATE_PATH, _phase4_settings, candidate_by_id
from ingestion.source_state import (
    compute_corpus_state,
    discover_full_corpus_files,
    make_full_corpus_build_record,
    write_final_full_corpus_build_record,
)
from vectorstore.points import FULL_CORPUS_BATCH_SIZE, build_full_corpus_point_batch, validate_full_corpus_point_inputs
from vectorstore.qdrant import SPARSE_VECTOR_NAME, client_from_settings, validate_full_corpus_collection_info
from vectorstore.upsert import FULL_CORPUS_SCROLL_LIMIT, upsert_full_corpus_batch, verify_full_corpus_collection

DUOI_DANG_CAP_NHAT = ".dang_cap_nhat"
CONG_SERVER = 8010


def settings_voi_kho(settings: dict[str, Any], kho: Path) -> dict[str, Any]:
    """Bản settings trỏ sang một kho CHÉP (gốc bài + file điều kiện `meta/full_corpus_conditions.json` của bản chép) — chỉ cho chạy thử."""
    goc = Path(kho).resolve()
    fc = settings["full_corpus"]
    return {**settings, "full_corpus": {**fc, "knowledge_base": {**fc["knowledge_base"], "root_dir": str(goc)},
                                        "conditions_file": str(goc / "meta/full_corpus_conditions.json")}}


def _payload_dang_co(client: QdrantClient, collection: str) -> dict[str, dict[str, Any]]:
    """Payload của mọi điểm đang nằm trong collection, theo mã điểm."""
    co: dict[str, dict[str, Any]] = {}
    offset = None
    while True:
        trang, offset = client.scroll(collection, limit=FULL_CORPUS_SCROLL_LIMIT, offset=offset, with_payload=True, with_vectors=False,
                                      timeout=QDRANT_TIMEOUT)
        co.update({str(r.id): r.payload for r in trang})
        if offset is None:
            return co


def _chup_collection(client: QdrantClient, collection: str) -> str:
    """Bản chụp Qdrant trước khi ghi (0,2 giây, khoảng 63 MB, nằm trong container ở /qdrant/snapshots/<collection>/). Trả tên bản chụp."""
    return client.create_snapshot(collection, wait=True).name


def _bai_khac_bam(ban_ghi_cu: dict[str, Any] | None, nguon: dict[str, str]) -> list[str]:
    """Bài thêm / bớt / đổi mã băm so với bản ghi dựng cũ (không có bản ghi cũ ⇒ rỗng)."""
    cu = ((ban_ghi_cu or {}).get("corpus") or {}).get("sources")
    if not isinstance(cu, dict):
        return []
    return sorted(bai for bai in set(cu) | set(nguon) if cu.get(bai) != nguon.get(bai))


def _ghi_lai_vector_tu_khoa(client: QdrantClient, collection: str, chunks: list[FullCorpusChunk], thong_ke: SparseState,
                            bang_tu: dict[str, int]) -> None:
    """Vector từ khoá của điểm = hàm của chữ đoạn VÀ thống kê cả kho ⇒ thống kê đổi thì ghi lại cho mọi điểm; vector nghĩa + payload giữ nguyên."""
    for dau in range(0, len(chunks), FULL_CORPUS_BATCH_SIZE):
        diem = []
        for chunk in chunks[dau:dau + FULL_CORPUS_BATCH_SIZE]:
            tu_khoa = encode_sparse_document(chunk.search_text, thong_ke, bang_tu)
            diem.append(models.PointVectors(id=chunk.point_id, vector={
                SPARSE_VECTOR_NAME: models.SparseVector(indices=list(tu_khoa.indices), values=list(tu_khoa.values))}))
        client.update_vectors(collection, points=diem, wait=True, timeout=QDRANT_TIMEOUT)


def dong_bo(*, chi_xem: bool = False, kho: Path | None = None, collection: str | None = None, thu_muc_ban_ghi: Path | None = None,
            client: QdrantClient | None = None) -> dict[str, Any]:
    """Kéo collection về khớp kho. Trả: `da_khop`, `bai_doi` (bài có đoạn đổi HOẶC đổi mã băm, đã xếp), `so_doan_tinh_lai`, `so_diem_xoa`,
    `so_diem`, `giay`, … `chi_xem=True` ⇒ không ghi gì. Ba tham số `kho` / `collection` / `thu_muc_ban_ghi` chỉ để chạy thử trên bản chép."""
    bat_dau = time.perf_counter()
    settings = _phase4_settings()
    candidate = candidate_by_id(settings["full_corpus_runtime"]["candidate_id"])
    thu = (kho, collection, thu_muc_ban_ghi)
    if any(x is not None for x in thu):
        # Rào (hậu quả khó lùi): kho thử lẫn với collection đang chạy là ghi đè chỉ mục thật bằng chữ của bản chép.
        if any(x is None for x in thu):
            raise ValueError("Chạy thử cần ĐỦ ba tham số: kho, collection, thu_muc_ban_ghi")
        if collection == candidate.collection_name:
            raise ValueError("Collection thử không được trùng tên collection đang chạy")
        settings = settings_voi_kho(settings, kho)
        ten, goc_ghi = collection, Path(thu_muc_ban_ghi)
    else:
        ten, goc_ghi = candidate.collection_name, BUILD_RECORD_ROOT
    duong_ban_ghi = goc_ghi / f"{ten}.json"
    duong_tam = duong_ban_ghi.with_name(duong_ban_ghi.name + DUOI_DANG_CAP_NHAT)
    duong_thong_ke = goc_ghi / SPARSE_STATE_PATH.name
    chieu = candidate.dense_spec.dimension

    # 1. Kho hiện tại ⇒ đoạn mong đợi + thống kê từ khoá mới (cùng các hàm của lúc dựng lại toàn bộ)
    goc, duong_bai = discover_full_corpus_files(settings)
    nguon = compute_corpus_state(goc, duong_bai)
    chunks, loi = chunk_full_corpus(settings)
    if loi:
        raise ValueError(f"Chia đoạn kho lỗi, chưa ghi gì: {loi}")
    dinh_danh = compute_corpus_identity(chunks)
    thong_ke = fit_sparse_state(chunks)
    bang_tu = build_vocabulary_index(thong_ke)
    mong_doi = {chunk.point_id: chunk for chunk in chunks}

    dong_client = client is None
    client = client or client_from_settings(settings)
    runner = None
    try:
        # 2–3. So với CHÍNH collection: điểm thừa ⇒ xoá; điểm thiếu / khác payload ⇒ làm lại
        validate_full_corpus_collection_info(client.get_collection(ten), chieu)
        dang_co = _payload_dang_co(client, ten)
        thua = sorted(set(dang_co) - set(mong_doi))
        lam_lai = [chunk for chunk in chunks if dang_co.get(chunk.point_id) != chunk.to_qdrant_payload()]
        duong_cu = duong_ban_ghi if duong_ban_ghi.is_file() else duong_tam if duong_tam.is_file() else None
        ban_ghi_cu = json.loads(duong_cu.read_text(encoding="utf-8")) if duong_cu else None
        bai_theo_doan = sorted({dang_co[i]["source"] for i in thua} | {chunk.source for chunk in lam_lai})
        bai_theo_bam = _bai_khac_bam(ban_ghi_cu, nguon)
        # "Đã khớp" = không điểm nào khác VÀ bản ghi dựng + file thống kê đang nói đúng kho này (lần chạy trước chết sau bước ghi Qdrant ⇒ chưa khớp)
        da_khop = (not thua and not lam_lai and duong_ban_ghi.is_file() and ban_ghi_cu["corpus"].get("sources") == nguon
                   and ban_ghi_cu["corpus"].get("identity") == dinh_danh and duong_thong_ke.is_file()
                   and hashlib.sha256(duong_thong_ke.read_bytes()).hexdigest() == ban_ghi_cu["sparse"].get("state_sha256"))
        kq: dict[str, Any] = {
            "collection": ten, "chi_xem": chi_xem, "da_khop": da_khop, "bai_doi": sorted(set(bai_theo_doan) | set(bai_theo_bam)),
            "bai_doi_theo_doan": bai_theo_doan, "bai_doi_theo_bam": bai_theo_bam, "so_doan_tinh_lai": len(lam_lai), "so_diem_xoa": len(thua),
            "so_diem": len(chunks), "so_bai": len(nguon),
        }
        if chi_xem or da_khop:
            return {**kq, "giay": round(time.perf_counter() - bat_dau, 1)}

        # 4. Sao lưu: bản chụp Qdrant + hai file cũ
        kq["ban_chup"] = _chup_collection(client, ten)
        sao_luu = goc_ghi / "sao_luu" / datetime.now().strftime("%Y%m%d_%H%M%S")
        sao_luu.mkdir(parents=True, exist_ok=True)
        for file in (duong_cu, duong_thong_ke):
            if file is not None and file.is_file():
                shutil.copy2(file, sao_luu / file.name)
        kq["sao_luu"] = str(sao_luu)

        # 5. Từ đây tới lúc xong: không có bản ghi dựng ⇒ server từ chối khởi động
        if duong_ban_ghi.is_file():
            duong_ban_ghi.replace(duong_tam)

        # 6. Xoá điểm thừa; tính vector nghĩa chỉ cho đoạn phải làm lại rồi ghi (vector nghĩa + vector từ khoá mới + payload)
        if thua:
            client.delete(ten, points_selector=models.PointIdsList(points=thua), wait=True, timeout=QDRANT_TIMEOUT)
        nha_cung_cap = set(((ban_ghi_cu or {}).get("dense") or {}).get("providers") or [])
        if lam_lai:
            runner = create_dense_runner(candidate.dense_spec)
            runner.load()
            vector_nghia = runner.embed_documents_matrix([chunk.search_text for chunk in lam_lai])
            validate_full_corpus_point_inputs(lam_lai, vector_nghia, chieu, thong_ke, bang_tu)
            for dau in range(0, len(lam_lai), FULL_CORPUS_BATCH_SIZE):
                cuoi = dau + FULL_CORPUS_BATCH_SIZE
                upsert_full_corpus_batch(client, ten, build_full_corpus_point_batch(lam_lai[dau:cuoi], vector_nghia[dau:cuoi], thong_ke, bang_tu),
                                         QDRANT_TIMEOUT)
            if isinstance(runner, OpenRouterDenseRunner):
                nha_cung_cap |= set(runner.providers_seen)

        # 7. Vector từ khoá của mọi điểm KHÔNG làm lại, theo thống kê mới
        da_lam = {chunk.point_id for chunk in lam_lai}
        _ghi_lai_vector_tu_khoa(client, ten, [chunk for chunk in chunks if chunk.point_id not in da_lam], thong_ke, bang_tu)

        # 8. Kiểm cả collection bằng hàm kiểm của lúc dựng: số điểm, payload của MỌI điểm, mẫu vector (đoạn đầu mỗi lĩnh vực)
        mau: dict[str, str] = {}
        for chunk in chunks:
            mau.setdefault(domain_for_source(chunk.source), chunk.chunk_id)
        kq["kiem"] = verify_full_corpus_collection(client, ten, chieu, chunks, tuple(mau.values()), QDRANT_TIMEOUT)
        if compute_corpus_state(*discover_full_corpus_files(settings)) != nguon:
            raise ValueError("Kho đổi trong lúc lệnh đang chạy — chạy lại lệnh")

        # 9. File thống kê từ khoá, rồi SAU CÙNG bản ghi dựng (có bản ghi dựng ⇔ collection khớp kho)
        bam_thong_ke = write_sparse_state(thong_ke, duong_thong_ke)
        spec = candidate.dense_spec
        ban_ghi = make_full_corpus_build_record(
            collection_name=ten, candidate_id=candidate.candidate_id,
            dense={"model_id": spec.model_id, "revision": spec.revision, "dimension": spec.dimension},
            sources=nguon, chunk_count=len(chunks), corpus_identity=dinh_danh, sparse_state=thong_ke, sparse_state_sha256=bam_thong_ke,
            providers=sorted(nha_cung_cap),
        )
        kq["bam_ban_ghi_dung"] = write_final_full_corpus_build_record(ban_ghi, duong_ban_ghi)
        duong_tam.unlink(missing_ok=True)
        return {**kq, "bam_thong_ke": bam_thong_ke, "giay": round(time.perf_counter() - bat_dau, 1)}
    finally:
        if runner is not None:
            runner.close()
        if dong_client:
            client.close()


def _server_dang_chay() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", CONG_SERVER), timeout=0.3):
            return True
    except OSError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Cập nhật riêng phần chỉ mục của bài đã sửa (kéo collection về khớp kho)")
    parser.add_argument("--chi-xem", action="store_true", help="chỉ in bài nào khác chỉ mục, không ghi gì")
    parser.add_argument("--kho", type=Path, help="[chạy thử] thư mục kho chép")
    parser.add_argument("--collection", help="[chạy thử] tên collection thử")
    parser.add_argument("--thu-muc-ban-ghi", type=Path, help="[chạy thử] nơi để file thống kê + bản ghi dựng thử")
    parser.add_argument("--ghi-ket-qua", type=Path, help="ghi kết quả (JSON) ra file này")
    args = parser.parse_args()
    if not args.chi_xem:
        print("TẮT server trước khi chạy lệnh này, BẬT lại sau khi xong (server đọc thống kê từ khoá và xoá câu trả lời đã nhớ lúc khởi động).")
        if args.collection is None and _server_dang_chay():
            print(f"CẢNH BÁO: cổng {CONG_SERVER} đang mở — server đang chạy sẽ còn dùng thống kê cũ và câu trả lời đã nhớ cho tới khi khởi động lại.")
    kq = dong_bo(chi_xem=args.chi_xem, kho=args.kho, collection=args.collection, thu_muc_ban_ghi=args.thu_muc_ban_ghi)
    if args.ghi_ket_qua:
        args.ghi_ket_qua.write_text(json.dumps(kq, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(kq, ensure_ascii=False, indent=1))
    if kq["da_khop"]:
        print("Chỉ mục ĐÃ KHỚP kho — không ghi gì.")
    elif args.chi_xem:
        print(f"CHƯA khớp: {len(kq['bai_doi'])} bài đổi, {kq['so_doan_tinh_lai']} đoạn phải tính lại, {kq['so_diem_xoa']} điểm thừa. Chưa ghi gì.")
    else:
        print(f"XONG trong {kq['giay']} giây: {len(kq['bai_doi'])} bài đổi, tính lại {kq['so_doan_tinh_lai']} đoạn, xoá {kq['so_diem_xoa']} điểm; "
              f"collection có {kq['so_diem']} điểm. Bản chụp trước khi ghi: {kq['ban_chup']}. Khởi động lại server để dùng chỉ mục mới.")


if __name__ == "__main__":
    main()
