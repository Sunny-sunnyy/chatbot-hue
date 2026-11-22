"""Cập nhật riêng phần chỉ mục của bài đã sửa (`ingestion/cap_nhat_rieng.py`): kết quả phải GIỐNG dựng lại toàn bộ, chỉ đoạn khác chữ được
tính lại vector nghĩa, lệnh chết giữa chừng rồi chạy lại vẫn kéo về đúng. Kho nhỏ trong thư mục tạm; Qdrant bản trong bộ nhớ của chính thư viện;
model embedding thay bằng hàm tất định theo chữ (để so được từng số) — lượt thật trên Qdrant server + e5-small ghi ở report của nhánh."""
import hashlib
import json
from pathlib import Path
import socket

import numpy as np
import pytest
from qdrant_client import QdrantClient

from embedding.sparse import build_vocabulary_index, fit_sparse_state
from ingestion import cap_nhat_rieng as cnr
from ingestion.chunking.full_corpus_chunker import chunk_full_corpus
from ingestion.full_corpus_pipeline import _phase4_settings
from vectorstore.points import build_full_corpus_point_batch
from vectorstore.qdrant import create_full_corpus_collection

THU = "thu_cap_nhat_rieng"
BAI_VE = "travel/tickets/ve-dai-noi.md"
BAI_PHO = "foods/bun-bo.md"
BAI_LANG = "heritages/lang-tu-duc.md"


def _bai(ten: str, muc: list[tuple[str, str]]) -> str:
    return f"# {ten}\n\n" + "\n\n".join(f"## {dau}\n\n{chu}" for dau, chu in muc) + "\n"


KHO = {
    BAI_VE: _bai("Vé tham quan Đại Nội", [
        ("Giá vé", "Vé vào Đại Nội Huế cho người lớn là 200.000 đồng một lượt."),
        ("Giờ mở cửa", "Đại Nội mở cửa từ 7 giờ đến 17 giờ 30 mỗi ngày trong mùa hè."),
        ("Lưu ý", "Trẻ em dưới 7 tuổi được miễn vé khi đi cùng người lớn."),
    ]),
    BAI_PHO: _bai("Bún bò Huế", [
        ("Món ăn", "Bún bò Huế có nước dùng nấu từ xương bò, sả và mắm ruốc."),
        ("Giá tham khảo", "Một tô bún bò ở quán bình dân khoảng 35.000 đồng."),
    ]),
    BAI_LANG: _bai("Lăng Tự Đức", [
        ("Kiến trúc", "Lăng Tự Đức nằm giữa rừng thông, có hồ Lưu Khiêm và nhà thủy tạ."),
        ("Vé", "Vé vào lăng Tự Đức cho người lớn là 150.000 đồng."),
    ]),
}


class RunnerGia:
    """Vector nghĩa tất định theo chữ; đếm chữ đã được tính để biết lệnh tính lại bao nhiêu đoạn."""
    da_tinh: list[str] = []

    def load(self) -> None: ...
    def close(self) -> None: ...

    def embed_documents_matrix(self, texts):
        RunnerGia.da_tinh.extend(texts)
        hang = []
        for chu in texts:
            v = np.random.default_rng(int(hashlib.sha256(chu.encode()).hexdigest()[:16], 16)).standard_normal(384)
            hang.append(v / np.linalg.norm(v))
        return np.asarray(hang, dtype=np.float32)


@pytest.fixture
def moi_truong(tmp_path: Path, monkeypatch):
    kho = tmp_path / "kho"
    for duong, chu in KHO.items():
        (kho / duong).parent.mkdir(parents=True, exist_ok=True)
        (kho / duong).write_text(chu, encoding="utf-8")
    (kho / "meta").mkdir()
    (kho / "meta/full_corpus_conditions.json").write_text("[]", encoding="utf-8")
    RunnerGia.da_tinh = []
    monkeypatch.setattr(cnr, "create_dense_runner", lambda spec: RunnerGia())
    monkeypatch.setattr(cnr, "_chup_collection", lambda client, ten: "ban-chup-thu")  # Qdrant trong bộ nhớ không có bản chụp
    client = QdrantClient(":memory:")
    _dung_lai(client, THU, kho)
    RunnerGia.da_tinh = []
    return {"kho": kho, "ghi": tmp_path / "ghi", "client": client}


def _dung_lai(client: QdrantClient, ten: str, kho: Path) -> None:
    """Dựng lại TOÀN BỘ từ kho, bằng đúng các hàm của đường dựng — bản để so."""
    chunks, loi = chunk_full_corpus(cnr.settings_voi_kho(_phase4_settings(), kho))
    assert not loi
    thong_ke = fit_sparse_state(chunks)
    if client.collection_exists(ten):
        client.delete_collection(ten)
    create_full_corpus_collection(client, ten, 384, 30)
    vector = RunnerGia().embed_documents_matrix([c.search_text for c in chunks])
    client.upsert(ten, points=build_full_corpus_point_batch(chunks, vector, thong_ke, build_vocabulary_index(thong_ke)), wait=True)


def _anh(client: QdrantClient, ten: str) -> dict:
    diem, _ = client.scroll(ten, limit=1000, with_payload=True, with_vectors=True)
    return {str(d.id): (d.payload, d.vector["dense"], list(d.vector["sparse"].indices), list(d.vector["sparse"].values)) for d in diem}


def _chay(mt, **them):
    return cnr.dong_bo(kho=mt["kho"], collection=THU, thu_muc_ban_ghi=mt["ghi"], client=mt["client"], **them)


def _giong_dung_lai(mt) -> None:
    _dung_lai(mt["client"], "dung_lai", mt["kho"])
    assert _anh(mt["client"], THU) == _anh(mt["client"], "dung_lai")


def _sua(mt, duong: str, cu: str, moi: str) -> None:
    file = mt["kho"] / duong
    chu = file.read_text(encoding="utf-8")
    assert cu in chu
    file.write_text(chu.replace(cu, moi), encoding="utf-8")


def test_sua_mot_con_so_chi_tinh_lai_doan_do_va_giong_dung_lai(moi_truong):
    _chay(moi_truong)  # lần đầu: chỉ để có bản ghi dựng + file thống kê của collection thử
    truoc = _anh(moi_truong["client"], THU)
    RunnerGia.da_tinh = []
    _sua(moi_truong, BAI_VE, "200.000 đồng", "250.000 đồng")

    xem = _chay(moi_truong, chi_xem=True)
    assert (xem["bai_doi"], xem["so_doan_tinh_lai"], xem["da_khop"]) == ([BAI_VE], 1, False)
    assert _anh(moi_truong["client"], THU) == truoc and RunnerGia.da_tinh == []  # chỉ xem ⇒ không ghi, không tính

    kq = _chay(moi_truong)
    assert (kq["bai_doi"], kq["so_doan_tinh_lai"], kq["so_diem_xoa"]) == ([BAI_VE], 1, 0)
    assert len(RunnerGia.da_tinh) == 1 and "250.000" in RunnerGia.da_tinh[0]  # chỉ MỘT đoạn được tính lại vector nghĩa
    sau = _anh(moi_truong["client"], THU)
    giu = [i for i in sau if sau[i][0] == truoc[i][0]]
    assert len(giu) == len(sau) - 1 and all(sau[i][1] == truoc[i][1] for i in giu)  # đoạn không đổi chữ: vector nghĩa y nguyên
    _giong_dung_lai(moi_truong)
    ban_ghi = json.loads((moi_truong["ghi"] / f"{THU}.json").read_text(encoding="utf-8"))
    thong_ke = moi_truong["ghi"] / "full_corpus_sparse_state.json"
    assert ban_ghi["sparse"]["state_sha256"] == hashlib.sha256(thong_ke.read_bytes()).hexdigest() == kq["bam_thong_ke"]
    assert not list(moi_truong["ghi"].glob(f"*{cnr.DUOI_DANG_CAP_NHAT}"))

    RunnerGia.da_tinh = []  # (bản dựng lại để so ở trên cũng dùng runner này)
    lan_hai = _chay(moi_truong)  # đã khớp ⇒ không ghi gì
    assert lan_hai["da_khop"] and lan_hai["bai_doi"] == [] and RunnerGia.da_tinh == [] and "ban_chup" not in lan_hai


def test_them_bai_moi_va_rut_giua_bai(moi_truong):
    _chay(moi_truong)
    truoc = _anh(moi_truong["client"], THU)
    moi = "festivals/le-hoi-dien-hon-chen.md"
    (moi_truong["kho"] / "festivals").mkdir()
    (moi_truong["kho"] / moi).write_text(_bai("Lễ hội điện Hòn Chén", [("Thời gian", "Lễ hội điện Hòn Chén diễn ra vào tháng ba và tháng bảy âm lịch.")]),
                                         encoding="utf-8")
    _sua(moi_truong, BAI_VE, "## Giờ mở cửa\n\nĐại Nội mở cửa từ 7 giờ đến 17 giờ 30 mỗi ngày trong mùa hè.\n\n", "")  # rút GIỮA bài ⇒ đoạn sau dịch số

    kq = _chay(moi_truong)
    assert kq["bai_doi"] == [moi, BAI_VE] and kq["so_diem_xoa"] == 1 and kq["so_diem"] == len(truoc)  # thêm một đoạn, bớt một đoạn
    sau = _anh(moi_truong["client"], THU)
    khong_sua = [i for i in sau if i in truoc and sau[i][0] == truoc[i][0]]
    assert khong_sua and all(sau[i][1] == truoc[i][1] for i in khong_sua)
    assert any(sau[i][2:] != truoc[i][2:] for i in khong_sua)  # thống kê cả kho đổi ⇒ vector từ khoá của điểm KHÔNG sửa cũng được ghi lại
    _giong_dung_lai(moi_truong)


@pytest.mark.parametrize("cho_chet", ["_ghi_lai_vector_tu_khoa", "write_sparse_state"])
def test_chet_giua_chung_roi_chay_lai_van_ve_dung(moi_truong, monkeypatch, cho_chet):
    _chay(moi_truong)
    _sua(moi_truong, BAI_LANG, "150.000 đồng", "180.000 đồng")
    with monkeypatch.context() as m:
        m.setattr(cnr, cho_chet, lambda *a, **k: (_ for _ in ()).throw(RuntimeError("chết giữa chừng")))
        with pytest.raises(RuntimeError):
            _chay(moi_truong)
    ghi = moi_truong["ghi"]
    assert not (ghi / f"{THU}.json").exists() and (ghi / f"{THU}.json{cnr.DUOI_DANG_CAP_NHAT}").is_file()  # server sẽ từ chối khởi động

    kq = _chay(moi_truong)  # payload đã khớp từ lần chết, nhưng chưa có bản ghi dựng ⇒ KHÔNG được coi là đã khớp
    assert not kq["da_khop"] and kq["bai_doi"] == [BAI_LANG]
    assert (ghi / f"{THU}.json").is_file() and not list(ghi.glob(f"*{cnr.DUOI_DANG_CAP_NHAT}"))
    _giong_dung_lai(moi_truong)
    assert _chay(moi_truong)["da_khop"]


def test_bai_doi_ma_bam_ma_khong_doi_doan_nao(moi_truong):
    _chay(moi_truong)
    truoc = _anh(moi_truong["client"], THU)
    RunnerGia.da_tinh = []
    file = moi_truong["kho"] / BAI_PHO
    file.write_text(file.read_text(encoding="utf-8") + "\n\n", encoding="utf-8")  # dòng trống cuối bài: mã băm file đổi, không đoạn nào đổi

    kq = _chay(moi_truong)
    assert (kq["bai_doi"], kq["so_doan_tinh_lai"], kq["bai_doi_theo_doan"], kq["da_khop"]) == ([BAI_PHO], 0, [], False)
    assert RunnerGia.da_tinh == [] and _anh(moi_truong["client"], THU) == truoc
    ban_ghi = json.loads((moi_truong["ghi"] / f"{THU}.json").read_text(encoding="utf-8"))
    assert ban_ghi["corpus"]["sources"][BAI_PHO] == hashlib.sha256(file.read_text(encoding="utf-8").encode()).hexdigest()
    assert _chay(moi_truong)["da_khop"]


def test_tham_so_chay_thu_phai_di_cung_nhau_va_khong_trung_collection_dang_chay(moi_truong):
    with pytest.raises(ValueError, match="ĐỦ ba tham số"):
        cnr.dong_bo(kho=moi_truong["kho"], client=moi_truong["client"])
    with pytest.raises(ValueError, match="trùng tên collection đang chạy"):
        cnr.dong_bo(kho=moi_truong["kho"], collection="hue_full_corpus_7a2_e5_small_384", thu_muc_ban_ghi=moi_truong["ghi"],
                    client=moi_truong["client"])
    with pytest.raises(ValueError, match="trùng thư mục bản ghi dựng thật"):  # kể cả `chi_xem`: dừng trước khi đọc / ghi gì
        cnr.dong_bo(chi_xem=True, kho=moi_truong["kho"], collection=THU, thu_muc_ban_ghi=cnr.BUILD_RECORD_ROOT, client=moi_truong["client"])


# ---------- Soát khác hãng 22/11 (điểm 4): server chỉ kiểm chỉ mục một lần lúc khởi động ⇒ còn chạy trong lúc cập nhật là trả lời trên chỉ mục dở ----------
@pytest.fixture
def cong_dang_mo(monkeypatch):
    """Một cổng THẬT đang nghe, đóng vai cổng server (không tựa vào server nào đang chạy trên máy)."""
    with socket.socket() as o:
        o.bind(("127.0.0.1", 0))
        o.listen()
        monkeypatch.setattr(cnr, "CONG_SERVER", o.getsockname()[1])
        yield


def test_real_write_stops_before_reading_anything_while_the_server_port_is_open(monkeypatch, cong_dang_mo):
    monkeypatch.setattr(cnr, "discover_full_corpus_files", lambda settings: pytest.fail("đã đi quá phép dò cổng"))  # lưới an toàn: không chạm chỉ mục thật
    assert cnr.server_dang_chay()
    with pytest.raises(cnr.ServerDangChay, match="Tắt server"):
        cnr.dong_bo()


def test_view_only_and_trial_collection_runs_are_not_blocked_by_the_open_port(moi_truong, cong_dang_mo):
    assert _chay(moi_truong, chi_xem=True)["da_khop"] is False  # bản thử chưa có bản ghi dựng ⇒ chưa khớp, và không bị chặn
    assert _chay(moi_truong)["so_doan_tinh_lai"] == 0 and _chay(moi_truong)["da_khop"]


def test_closed_port_reads_as_no_server(monkeypatch):
    with socket.socket() as o:
        o.bind(("127.0.0.1", 0))
        cong = o.getsockname()[1]
    monkeypatch.setattr(cnr, "CONG_SERVER", cong)  # cổng vừa đóng
    assert not cnr.server_dang_chay()
