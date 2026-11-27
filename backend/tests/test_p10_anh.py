"""Phase 10 A1 — hỏi bằng ảnh: T1–T7 của plan `2026-11-05-phase-10-a1-plan.md` bản 2 (logic thuần, ảnh nhỏ tự tạo; không gọi model, không mạng).
T8 (server thật, 11 MB, file tạm) và T9 (capture_all, uvicorn) chạy ngoài pytest — xem report."""
import io
import json
import logging
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from pydantic import ValidationError
from starlette.datastructures import Headers

from api.app import create_app
from api.routes.anh import ANH_FIELDS, kiem_dau_vao
from core.settings_loader import BACKEND_DIR
from llm.nhan_anh import AnhKhongHopLe, chuan_bi_anh, kiem_lai, kieu_dau_ra, nap_danh_sach

GOC = "http://127.0.0.1:8000"
MB10 = 10 * 1024 * 1024
DS = [{"id": "diem_a", "ten": "Điểm A", "ten_khac": ["chỗ A"]}, {"id": "diem_b", "ten": "Điểm B", "ten_khac": []},
      {"id": "mon_c", "ten": "Món C", "ten_khac": []}, {"id": "mon_d", "ten": "Món D", "ten_khac": []}]


def anh(fmt: str = "JPEG", size=(64, 48), exif=None) -> bytes:
    out = io.BytesIO()
    im = Image.new("RGB", size, (200, 30, 30))
    im.save(out, format=fmt, **({"exif": exif} if exif is not None else {}))
    return out.getvalue()


def h(**kw) -> Headers:
    base = {"content-type": "image/jpeg", "content-length": "1000"}
    base.update({k.replace("_", "-"): v for k, v in kw.items() if v is not None})
    for k in [k.replace("_", "-") for k, v in kw.items() if v is None]:
        base.pop(k, None)
    return Headers(base)


# T1 — rào A10 trước khi đọc thân
@pytest.mark.parametrize("headers, expected", [
    (h(sec_fetch_site="cross-site"), (403, "cross_site")),
    (h(sec_fetch_site="same-site"), (403, "cross_site")),
    (h(sec_fetch_site="none"), (403, "cross_site")),
    (h(sec_fetch_site="same-origin"), None),
    (h(origin="https://trang-la.example"), (403, "cross_origin")),
    (h(origin="http://127.0.0.1:9999"), (403, "cross_origin")),
    (h(origin=GOC), None),
    (h(), None),  # không Sec-Fetch-Site / Origin (curl, trình duyệt cũ) ⇒ còn rào kiểu nội dung
    (h(content_type="multipart/form-data; boundary=x"), (415, "unsupported_media_type")),
    (h(content_type="text/plain"), (415, "unsupported_media_type")),
    (h(content_type="application/x-www-form-urlencoded"), (415, "unsupported_media_type")),
    (h(content_type="image/heic"), (415, "unsupported_media_type")),
    (h(content_type=None), (415, "unsupported_media_type")),
    (h(content_type="IMAGE/JPEG; charset=x"), None),
    (h(content_type="image/png"), None),
    (h(content_length=None), (413, "payload_too_large")),
    (h(content_length="abc"), (413, "payload_too_large")),
    (h(content_length="-1"), (413, "payload_too_large")),
    (h(content_length=str(MB10 + 1)), (413, "payload_too_large")),
    (h(content_length=str(MB10)), None),
])
def test_t1_kiem_dau_vao(headers, expected):
    assert kiem_dau_vao(headers, GOC, MB10) == expected


def test_t1_cross_site_thang_truoc_kieu_noi_dung():
    # trang lạ gửi multipart: chặn vì khác nguồn, trước cả kiểm kiểu
    assert kiem_dau_vao(h(sec_fetch_site="cross-site", content_type="multipart/form-data"), GOC, MB10) == (403, "cross_site")


# T2 — EXIF (GPS + hướng) bị xoá, ảnh xoay đúng
def test_t2_xoa_exif_va_xoay():
    exif = Image.Exif()
    exif[0x0112] = 6  # Orientation: xoay 90° ⇒ rộng ↔ cao
    exif[0x8825] = {2: (16.0, 28.0, 0.0), 4: (107.0, 35.0, 0.0)}  # GPSInfo
    src = anh(size=(80, 40), exif=exif.tobytes())
    assert Image.open(io.BytesIO(src)).getexif()  # ảnh vào có EXIF thật
    out, w, h_ = chuan_bi_anh(src, max_pixels=10_000, canh_dai=1024)
    im = Image.open(io.BytesIO(out))
    assert (w, h_) == (80, 40) and im.size == (40, 80)
    assert not im.getexif() and "exif" not in im.info


# T3 — bom giải nén: chặn theo số điểm ảnh trước khi giải mã
def test_t3_qua_nhieu_diem_anh():
    with pytest.raises(AnhKhongHopLe) as e:
        chuan_bi_anh(anh(size=(1200, 1000)), max_pixels=1_000_000, canh_dai=1024)
    assert (e.value.status, e.value.code) == (413, "image_too_large")
    chuan_bi_anh(anh(size=(900, 900)), max_pixels=1_000_000, canh_dai=1024)


# T4 — định dạng: chỉ JPEG / PNG / WEBP (đọc theo nội dung, không theo nhãn)
@pytest.mark.parametrize("fmt", ["JPEG", "PNG", "WEBP"])
def test_t4_dinh_dang_cho_phep(fmt):
    out, _, _ = chuan_bi_anh(anh(fmt), max_pixels=10_000, canh_dai=1024)
    assert Image.open(io.BytesIO(out)).format == "JPEG"


@pytest.mark.parametrize("data", [anh("GIF"), anh("BMP"), b"day khong phai anh", b""])
def test_t4_dinh_dang_bi_tu_choi(data):
    with pytest.raises(AnhKhongHopLe) as e:
        chuan_bi_anh(data, max_pixels=10_000, canh_dai=1024)
    assert (e.value.status, e.value.code) == (415, "unsupported_image")


# T5 — thu nhỏ ảnh điện thoại về cạnh dài 1024
def test_t5_thu_nho():
    out, w, h_ = chuan_bi_anh(anh(size=(4032, 3024)), max_pixels=40_000_000, canh_dai=1024)
    assert (w, h_) == (4032, 3024) and Image.open(io.BytesIO(out)).size == (1024, 768)


# T6 — kiểu đầu ra strict + backend kiểm lại
def test_t6_kieu_dau_ra():
    Out = kieu_dau_ra(DS)
    assert Out.model_validate({"ung_vien": ["diem_a"], "khong_nhan_ra": False})
    for bad in ({"ung_vien": ["la_lam"], "khong_nhan_ra": False}, {"ung_vien": [], "khong_nhan_ra": False, "giai_thich": "x"}):
        with pytest.raises(ValidationError):
            Out.model_validate(bad)
    schema = json.dumps(Out.model_json_schema())
    assert '"enum"' in schema and "la_lam" not in schema


def test_t6_kiem_lai():
    Out = kieu_dau_ra(DS)
    assert kiem_lai(Out(ung_vien=["mon_c", "diem_a", "mon_c"], khong_nhan_ra=False), DS) == [
        {"id": "mon_c", "ten": "Món C"}, {"id": "diem_a", "ten": "Điểm A"}]
    assert kiem_lai(Out(ung_vien=["diem_a"], khong_nhan_ra=True), DS) == []
    assert kiem_lai(Out(ung_vien=[], khong_nhan_ra=False), DS) == []
    assert kiem_lai(None, DS) == []


def test_t6_qua_ba_ten_thi_cat_khong_bao_loi():
    """Đường Bedrock gỡ `maxItems` khỏi khuôn gửi đi (`bedrock_model.UNSUPPORTED_SCHEMA_KEYS`) ⇒ model có thể trả 4 tên. Trước 23/11/2026 kiểu đầu ra
    tự chặn ở 3 nên cả lượt thành lỗi "chưa nhận ra" dù model đã nhận ra; nay kiểu nhận, `kiem_lai` giữ ba tên đầu."""
    Out = kieu_dau_ra(DS)
    bon = Out.model_validate({"ung_vien": ["mon_d", "diem_a", "diem_b", "mon_c"], "khong_nhan_ra": False})
    assert kiem_lai(bon, DS) == [{"id": "mon_d", "ten": "Món D"}, {"id": "diem_a", "ten": "Điểm A"}, {"id": "diem_b", "ten": "Điểm B"}]


# T7 — nạp danh sách: id / tên trùng ⇒ lỗi khởi động
def test_t7_nap_danh_sach(tmp_path):
    p = tmp_path / "ds.json"
    p.write_text(json.dumps(DS, ensure_ascii=False), encoding="utf-8")
    assert [m["id"] for m in nap_danh_sach(p)] == ["diem_a", "diem_b", "mon_c", "mon_d"]
    for bad in (DS + [{"id": "diem_a", "ten": "Khác", "ten_khac": []}], DS + [{"id": "diem_e", "ten": "điểm  a", "ten_khac": []}],
                DS + [{"id": "diem_f", "ten": "Chỗ A Huế", "ten_khac": []}]):
        p.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        with pytest.raises(ValueError):
            nap_danh_sach(p)


def test_t6_xac_nhan_truoc_di_theo_ung_vien():
    """Mục danh sách mang `xac_nhan_truoc` (nơi dễ bị nhầm với nơi khác không có trong danh sách — 23/11/2026: cầu Dã Viên ra "Cầu Trường Tiền")
    ⇒ ứng viên trả về mang cờ đó để giao diện hiện thẻ xác nhận thay vì tự hỏi; mục không có cờ ⇒ ứng viên y như cũ (không thêm khoá)."""
    ds = [{**DS[0], "xac_nhan_truoc": True}, *DS[1:]]
    Out = kieu_dau_ra(ds)
    assert kiem_lai(Out(ung_vien=["diem_a", "mon_c"], khong_nhan_ra=False), ds) == [
        {"id": "diem_a", "ten": "Điểm A", "xac_nhan_truoc": True}, {"id": "mon_c", "ten": "Món C"}]


def test_t7_danh_sach_that():
    """Danh sách ĐANG CHẠY (đường dẫn ở `settings.yaml`) nạp được — id / khoá tên không trùng — và 42 tên chủ dự án duyệt 05/11 còn nguyên ở đầu."""
    import yaml
    duong = yaml.safe_load((BACKEND_DIR / "config" / "settings.yaml").read_text(encoding="utf-8"))["anh"]["danh_sach"]
    p, goc = (BACKEND_DIR / duong).resolve(), (BACKEND_DIR / "../data/phase_10/anh/danh_sach_ten.json").resolve()
    if not (p.exists() and goc.exists()):  # bản clone / worktree không có data/ (private)
        pytest.skip("không có data/phase_10/anh/")
    ds = nap_danh_sach(p)
    assert len(ds) >= 40 and kieu_dau_ra(ds)
    assert ds[:42] == nap_danh_sach(goc)


# Mức route (không lifespan ⇒ không generator, không model): rào chạy trước khi đọc thân / gọi model
def test_route_tat_co_404_va_rao_truoc_generator():
    app = create_app()
    client = TestClient(app)  # không `with` ⇒ lifespan không chạy ⇒ app.state.anh = None, generator = None
    assert client.post("/api/anh/ung_vien", content=anh(), headers={"content-type": "image/jpeg"}).status_code == 404
    assert client.get("/api/anh/ung_vien").status_code == 404  # giao diện không hiện nút ảnh khi cờ tắt
    app.state.anh = {"danh_sach": DS, "agent": None, "max_bytes": 5000, "max_pixels": 10_000, "canh_dai": 1024, "timeout": 15}
    post = lambda body, **hd: client.post("/api/anh/ung_vien", content=body, headers={"content-type": "image/jpeg", **hd})
    assert post(anh(), **{"sec-fetch-site": "cross-site"}).status_code == 403
    assert post(anh(), origin="https://trang-la.example").status_code == 403
    assert client.post("/api/anh/ung_vien", files={"f": ("a.jpg", anh(), "image/jpeg")}).status_code == 415  # multipart
    assert post(b"x" * 6000).status_code == 413
    assert client.get("/api/anh/ung_vien").json() == {"bat": True}
    r = post(anh())  # qua mọi rào ⇒ tới bước cần generator ⇒ 503, chưa gọi model
    assert r.status_code == 503 and r.json() == {"code": "generator_unavailable"}


def test_anh_metrics_logs_cached_tokens_and_keeps_response_unchanged(caplog):
    import asyncio
    from llm.nhan_anh import kieu_dau_ra

    assert "cached_tokens" in ANH_FIELDS
    Out = kieu_dau_ra(DS)

    class FakeGen:
        async def _run(self, agent, items, call_log, timeout):
            call_log.calls.append({
                "input_tokens": 1200,
                "cached_tokens": 1024,
                "output_tokens": 25,
                "reasoning_tokens": 0,
                "usd": 0.00012,
            })
            return SimpleNamespace(final_output=Out(ung_vien=["diem_a"], khong_nhan_ra=False))

    app = create_app()
    app.state.generator = FakeGen()
    app.state.anh = {
        "danh_sach": DS,
        "agent": SimpleNamespace(),
        "max_bytes": 100_000,
        "max_pixels": 1_000_000,
        "canh_dai": 1024,
        "timeout": 10,
    }
    client = TestClient(app)
    with caplog.at_level(logging.INFO, logger="chat"):
        resp = client.post("/api/anh/ung_vien", content=anh(), headers={"content-type": "image/jpeg"})
    assert resp.status_code == 200
    assert resp.json() == {"ung_vien": [{"id": "diem_a", "ten": "Điểm A"}], "khong_nhan_ra": False}

    metric_line = next(rec.message for rec in caplog.records if rec.message.startswith("anh_metrics "))
    metric_obj = json.loads(metric_line.split("anh_metrics ", 1)[1])
    assert tuple(metric_obj.keys()) == ANH_FIELDS
    assert metric_obj["cached_tokens"] == 1024 and metric_obj["input_tokens"] == 1200
