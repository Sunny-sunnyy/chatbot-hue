"""Nút "Vì sao trả lời vậy?" (`api/vi_sao.py`, công tắc `vi_sao`): bản tóm tắt dựng từ bản ghi khuôn sổ vết; cất trong RAM theo mã lượt; công tắc tắt ⇒
`done` như cũ và route trả 404. Generator thay thế (không mạng); tìm kho thật như các test API khác."""
import dataclasses
import time

from fastapi.testclient import TestClient

from api.app import create_app
from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents
from api.vi_sao import MAX_LUOT, TRAN_CAU_GUI, KhoViSao, tom_tat
from llm.assistant import AssistantFlags
from core.settings_loader import load_settings
from test_b3_memory import MemoryGenerator
from test_chat_stream import parse_sse, stream_with_text

A, B = "travel/places/Noi A.md", "foods/Quan B.md"


def _ghi(**them) -> dict:
    """Một dòng khuôn sổ vết của lượt hỏi đáp: code tìm (2 bài, 3 đoạn) ⇒ model gọi thời tiết ⇒ model tìm thêm (1 bài) ⇒ viết, trích bài A."""
    ghi = {
        "duong": "chat_stream", "cau_go": "Nơi A mở cửa mấy giờ?", "cau_gui_model": "Nơi A mở cửa mấy giờ?", "lich_su": [],
        "so_do": {"outcome": "success", "refusal": False, "total_ms": 8100.0, "search_ms": 170.0, "context_ms": 10.0, "generation_ms": 7940.0, "cache": "truot"},
        "tuyen": {"route": "tro_ly_hue", "cau_tim_dinh_tuyen": None},
        "tim_kho": [
            {"cau": ["Nơi A mở cửa mấy giờ?"], "by": "code", "vao_ngu_canh": ["a#1", "a#2", "b#1"],
             "ket_qua": [{"chunk_id": "a#1", "source": A, "diem": 0.03}, {"chunk_id": "b#1", "source": B, "diem": 0.03}, {"chunk_id": "a#2", "source": A, "diem": 0.02}]},
            {"cau": ["giờ mở cửa Nơi A"], "by": "model", "vao_ngu_canh": ["a#3"], "ket_qua": [{"chunk_id": "a#3", "source": A, "diem": 0.03}]}],
        "cong_cu": [{"name": "tim_kho", "ms": 170.0, "by": "code"}, {"name": "thoi_tiet", "ms": 400.0}, {"name": "tim_kho", "ms": 90.0, "by": "model"},
                    {"name": "tim_kho", "ms": 0.0, "by": "model", "het_luot": True}],
        "goi_model": [{"route": "router", "kind": ["message"], "ms": 800.0}, {"route": "tro_ly_hue", "kind": ["function_call"], "ms": 1800.0},
                      {"route": "tro_ly_hue", "kind": ["message"], "ms": 6000.0}],
        "ngu_canh": ["…", "…"],
        "tra_loi": {"chu": "Mở cửa từ 7 giờ [3].", "ket_qua_co_dinh": None,
                    "nguon_trich": [{"id": 3, "title": "Nơi A", "source": A, "heading_path": ["Thông tin", "Giờ mở cửa"]}]},
        "web": None, "sua_lich": None, "lich": None,
    }
    ghi.update(them)
    return ghi


def test_hoi_dap_du_bon_nhom_dung_thu_tu():
    ban = tom_tat(_ghi(), bai_ids={A})
    assert ban["loai"] == "hoi_dap" and ban["tom_tat"] == "Trợ lý gọi model 3 lần, tìm trong kho 2 lần, đọc 4 đoạn, trích 1 nguồn."
    assert [g["viec"] for g in ban["goi_model"]] == ["phan_loai", "tim_them", "viet"] and ban["goi_model"][0] == {"viec": "phan_loai", "nhan": "Phân loại câu hỏi", "giay": 0.8}
    # một dãy bước: tìm (code) ⇒ công cụ ⇒ tìm (model); mục "hết lượt tìm" không phải một lần tìm thật ⇒ không thành bước
    assert [(b["loai"], b["ai"], b["nhan"]) for b in ban["buoc"]] == [
        ("tim", "he_thong", "Hệ thống tìm bằng chính câu của bạn"), ("cong_cu", "model", "Xem dự báo thời tiết"), ("tim", "model", "Model tự viết thêm câu tìm")]
    dau = ban["buoc"][0]
    assert dau["so_doan_tim"] == 3 and dau["so_doan_moi"] == 3 and dau["giay"] == 0.17 and dau["cau"] == ["Nơi A mở cửa mấy giờ?"]
    assert dau["bai"] == [{"title": "Nơi A", "bai_id": A, "so_doan": 2, "hang": 1, "duoc_trich": True},
                          {"title": "Quan B", "bai_id": None, "so_doan": 1, "hang": 2, "duoc_trich": False}]  # bài không được trích: tên lấy từ tên file
    assert ban["nguon"] == [{"ma": 3, "title": "Nơi A", "bai_id": A, "muc": "Thông tin › Giờ mở cửa"}]  # `ma` = mã gốc của sự kiện `sources`
    assert ban["thoi_gian"] == {"tong": 8.1, "tim": 0.17, "dung_ngu_canh": 0.01, "model": 7.94}
    assert ban["cau"] == {"go": "Nơi A mở cửa mấy giờ?", "gui": None, "so_luot_truoc": 0} and ban["web"] is None and ban["sua_lich"] is None and ban["ghi_chu"] == []
    assert "diem" not in str(ban)  # điểm trộn không ra giao diện; không có trường nào chừa cho phép đối chiếu câu ↔ đoạn


def test_cau_gui_khac_cau_go_bi_cat_va_dem_luot_truoc():
    ban = tom_tat(_ghi(cau_gui_model="x" * 1000, lich_su=[["a", "b"], ["c", "d"]]))
    assert ban["cau"]["gui"] == "x" * TRAN_CAU_GUI + "…" and ban["cau"]["so_luot_truoc"] == 2
    assert "Trợ lý được đọc 2 lượt trước của cuộc trò chuyện." in ban["ghi_chu"]


def test_tu_choi_ngoai_pham_vi_va_bo_nho_dem():
    tu_choi = tom_tat(_ghi(so_do={"outcome": "success", "refusal": True, "total_ms": 5000.0}, tra_loi={"chu": "…", "nguon_trich": None},
                           web={"cau_gui_tra_web": "câu ra web", "so_web": [{}, {}]}))
    assert tu_choi["loai"] == "tu_choi" and tu_choi["nguon"] == [] and tu_choi["web"] == {"cau": "câu ra web", "so_nguon": 2}
    assert "không đoạn nào trả lời được" in tu_choi["tom_tat"] and any("chưa được kiểm với kho" in c for c in tu_choi["ghi_chu"])
    ngoai = tom_tat(_ghi(so_do={"outcome": "out_of_scope"}, tim_kho=[], cong_cu=[], goi_model=[{"route": "router", "kind": ["message"], "ms": 700.0}],
                         tra_loi={"chu": "…", "nguon_trich": None}))
    assert ngoai["loai"] == "ngoai_pham_vi" and ngoai["buoc"] == [] and [g["viec"] for g in ngoai["goi_model"]] == ["phan_loai"]
    dem = tom_tat(_ghi(so_do={"outcome": "success", "cache": "trung", "total_ms": 3.0}, goi_model=[], cong_cu=[], tim_kho=[]))
    assert dem["loai"] == "bo_nho_dem" and dem["goi_model"] == [] and dem["buoc"] == []


def test_sua_lich_model_doc_va_ket_qua_cua_code():
    sua = {"so_dem": {"n_hanh_dong": 1}, "model_ra": [{"loai": "them_diem", "ten": "Nơi A", "ngay": 1, "buoi": "sang"}], "chon_the": None,
           "thay_doi": [{"cau": "Đã thêm Nơi A vào buổi sáng ngày 1.", "duoc": True}, {"cau": "Chưa làm: …", "duoc": False}]}
    ban = tom_tat(_ghi(sua_lich=sua, tim_kho=[], cong_cu=[], goi_model=[{"route": "sua_lich", "kind": ["message"], "ms": 1500.0}]))
    assert ban["loai"] == "sua_lich" and ban["goi_model"] == [{"viec": "hieu_lenh", "nhan": "Hiểu câu lệnh sửa lịch", "giay": 1.5}]
    assert ban["sua_lich"] == {"model_doc": [{"nhan": "Thêm · Nơi A · ngày 1 · buổi sáng"}],
                               "ket_qua": [{"cau": "Đã thêm Nơi A vào buổi sáng ngày 1.", "duoc": True}, {"cau": "Chưa làm: …", "duoc": False}]}
    assert any("do code làm" in c for c in ban["ghi_chu"])
    # cuộc ĐÃ có lịch nhưng lượt này chỉ hỏi (không hành động, không dòng kết quả) ⇒ vẫn là lượt hỏi đáp
    assert tom_tat(_ghi(sua_lich={"so_dem": {"n_hanh_dong": 0}, "model_ra": [], "thay_doi": [], "chon_the": None}))["loai"] == "hoi_dap"
    # đường nút thẻ chọn: không gọi model
    nut = tom_tat(_ghi(sua_lich={"so_dem": {}, "model_ra": [], "chon_the": {"cu": "a", "moi": "b"}, "thay_doi": [{"cau": "Đã thay …", "duoc": True}]},
                       tim_kho=[], cong_cu=[], goi_model=[]))
    assert nut["loai"] == "sua_lich" and any("Bạn bấm nút" in c for c in nut["ghi_chu"])


def test_kho_co_tran_va_cong_tac_mac_dinh_tat():
    kho = KhoViSao(max_luot=2)
    for i in range(3):
        kho.dat(f"m{i}", {"i": i})
    assert kho.lay("m0") is None and kho.lay("m2") == {"i": 2} and MAX_LUOT == 200
    assert AssistantFlags().vi_sao is False and load_settings(validate_private_paths=False)["assistant"]["vi_sao"] is False


def test_done_chi_bao_vi_sao_khi_cong_tac_bat():
    for bat, mong in ((False, {"outcome": "success", "turn_id": "B" * 16}), (True, {"outcome": "success", "turn_id": "B" * 16, "vi_sao": True})):
        stream, chunks, trace = stream_with_text("Mở cửa từ 7 giờ [1].")
        stream.new_turn_id, stream.co_vi_sao = (lambda: "B" * 16), bat
        assert parse_sse(stream.finish(trace))[-1] == ("done", mong)
    assert StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter()).co_vi_sao is False  # không truyền ⇒ như cũ


def test_route_cat_ban_tom_tat_theo_ma_luot_va_404_khi_tat():
    app = create_app()
    with TestClient(app) as client:
        goc = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator, app.state.generator_ready = MemoryGenerator(), True
        tat = client.post("/api/chat", json={"query": "Đại Nội mở cửa mấy giờ?"}).json()["turn_id"]
        khi_tat = client.get(f"/api/vi_sao/{tat}")
        app.state.assistant_flags = dataclasses.replace(app.state.assistant_flags, vi_sao=True)
        bat = client.post("/api/chat", json={"query": "Đại Nội mở cửa mấy giờ?"}).json()["turn_id"]
        khi_bat, la = client.get(f"/api/vi_sao/{bat}"), client.get(f"/api/vi_sao/{'A' * 16}")
        cu = client.get(f"/api/vi_sao/{tat}")  # lượt chạy lúc công tắc tắt không có bản tóm tắt
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = goc
    assert khi_tat.status_code == 404 and khi_tat.json()["error"]["code"] == "khong_co" and la.status_code == 404 and cu.status_code == 404
    ban = khi_bat.json()
    assert khi_bat.status_code == 200 and ban["cau"]["go"] == "Đại Nội mở cửa mấy giờ?" and ban["thoi_gian"]["tong"] is not None
    assert any(b["loai"] == "tim" and b["ai"] == "he_thong" and b["bai"] for b in ban["buoc"])  # lần tìm thật của code có bài
    assert set(ban) == {"loai", "tom_tat", "cau", "goi_model", "buoc", "nguon", "web", "sua_lich", "thoi_gian", "ghi_chu"}  # khuôn đã chốt với giao diện
