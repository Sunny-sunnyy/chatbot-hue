"""Bản đồ lịch trình (plan `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` bản 1 `e738f6f9f3ae`) — 0 USD.

Bảng điểm + bảng toạ độ thật (`data/phase_9/lich_trinh/`, private). T1 dữ liệu giao diện; T2 kiểm toạ độ lúc nạp; T3 CSP theo cờ.
T4 (chuỗi gửi model giống byte) chạy bằng `capture_all.py`, không ở đây.
"""
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from api.app import FRONTEND_CSP, FRONTEND_CSP_BAN_DO, FRONTEND_DIR, TILE_HOST, create_app, frontend_csp
from core.settings_loader import load_settings
from llm import lich_trinh as lt
from llm.assistant import BACKEND_DIR, AnswerTrace, AssistantFlags, lich_cho_giao_dien, nap_bang_lich

SETTINGS = load_settings(validate_private_paths=False)
BANG = nap_bang_lich(SETTINGS)
TOA_DO_PATH = BACKEND_DIR / SETTINGS["assistant"]["lich_trinh_toa_do"]
TOA_DO = lt.nap_toa_do(TOA_DO_PATH, BANG)
KHUNG = lt.xep(BANG, lt.ThamSo(so_ngay="3", so_thich="di_tich"))


def test_coordinates_loaded_only_for_itinerary_points_that_have_them():
    raw = json.loads(TOA_DO_PATH.read_text(encoding="utf-8"))["diem"]
    expected = {d["id"]: (d["vi_do"], d["kinh_do"]) for d in raw if d["id"] in BANG.theo_id and d["vi_do"] is not None}
    assert TOA_DO == expected
    assert 0 < len(TOA_DO) <= len(BANG.diem)  # bảng v7 (13/11) phủ đủ 28 điểm v3; ca "thiếu toạ độ" giữ ở test bản 2 (bảng v8 có điểm null)


def test_map_items_follow_the_plan_order_with_per_day_numbers():
    items = lt.ban_do(BANG, KHUNG, TOA_DO)
    assert [i["ten"] for i in items] == [BANG.theo_id[i]["ten"] for i in lt.diem_trong_khung(KHUNG)]
    for ng in KHUNG["ngay"]:
        ids = [id_ for b in lt.BUOI for id_ in ng["buoi"][b]]
        cua_ngay = [i for i in items if i["ngay"] == ng["ngay"]]
        assert [i["thu_tu"] for i in cua_ngay] == list(range(1, len(ids) + 1))
        for item, id_ in zip(cua_ngay, ids):
            assert item["buoi"] in ng["buoi"] and id_ in ng["buoi"][item["buoi"]]
            assert item["toa_do"] == (list(TOA_DO[id_]) if id_ in TOA_DO else None)
            assert item["map_url"] == lt.map_url(BANG.theo_id[id_]["ten"])


def test_flag_off_keeps_the_old_payload_shape():
    def trace():
        t = AnswerTrace()
        t.lich = {"khung": KHUNG}
        return t

    off = AssistantFlags(lich_trinh_bieu_mau=True, bang_lich=BANG)
    on = AssistantFlags(lich_trinh_bieu_mau=True, bang_lich=BANG, ban_do_lich=True, toa_do_lich=TOA_DO)
    old = lich_cho_giao_dien(trace(), off, "câu")["ban_do"]
    assert all(set(i) == {"ten", "map_url"} for i in old) and old == lt.ban_do(BANG, KHUNG)
    new = lich_cho_giao_dien(trace(), on, "câu")["ban_do"]
    assert all(set(i) == {"ten", "map_url", "ngay", "buoi", "thu_tu", "toa_do"} for i in new)
    assert [{"ten": i["ten"], "map_url": i["map_url"]} for i in new] == old


def test_maps_link_by_name_and_coordinates_only_loaded_for_map_flag():
    # A 08/11 (review E p11-lich-nho): link Google Maps theo TÊN (bỏ link theo toạ độ); toạ độ chỉ nạp khi cờ `ban_do_lich` bật ⇒ bật biểu mẫu
    # không cần file toạ độ
    for i in lt.ban_do(BANG, KHUNG, TOA_DO):
        assert i["map_url"] == lt.MAP_BASE + lt.quote(f"{i['ten']}, Huế")
    assert not SETTINGS["assistant"].get("ban_do_lich") and AssistantFlags.from_settings(SETTINGS).toa_do_lich is None


def test_flag_needs_coordinates():
    with pytest.raises(ValueError, match="ban_do_lich"):
        AssistantFlags(lich_trinh_bieu_mau=True, bang_lich=BANG, ban_do_lich=True)


@pytest.mark.parametrize("vi_do, kinh_do", [(10.77, 106.70), (16.46, 0), ("16.46", 107.59), (True, 107.59), (16.46, None)])
def test_bad_coordinates_stop_startup(tmp_path, vi_do, kinh_do):
    id_ = BANG.diem[0]["id"]
    path = tmp_path / "toa_do.json"
    path.write_text(json.dumps({"diem": [{"id": id_, "vi_do": vi_do, "kinh_do": kinh_do}]}), encoding="utf-8")
    with pytest.raises((ValueError, TypeError)):
        lt.nap_toa_do(path, BANG)


def test_csp_adds_tile_host_and_data_images_only_when_flag_on():
    assert frontend_csp(SimpleNamespace()) == FRONTEND_CSP  # trước lifespan
    assert frontend_csp(SimpleNamespace(assistant_flags=AssistantFlags())) == FRONTEND_CSP
    on = AssistantFlags(lich_trinh_bieu_mau=True, bang_lich=BANG, ban_do_lich=True, toa_do_lich=TOA_DO)
    assert frontend_csp(SimpleNamespace(assistant_flags=on)) == FRONTEND_CSP_BAN_DO
    # chỉ `img-src` đổi: thêm `data:` (GIF rỗng Leaflet dùng để huỷ tile) + đúng một host ngoài; phần còn lại giống byte
    assert FRONTEND_CSP_BAN_DO.replace(f" data: {TILE_HOST}", "", 1) == FRONTEND_CSP
    assert FRONTEND_CSP_BAN_DO.count("https://") == 1 and f"img-src 'self' blob: data: {TILE_HOST};" in FRONTEND_CSP_BAN_DO

    assert (FRONTEND_DIR / "index.html").is_file(), "chưa có bản build giao diện — chạy `cd frontend && npm ci && npm run build`"
    app = create_app(SETTINGS)  # không chạy lifespan ⇒ gắn cờ tay
    app.state.assistant_flags = on
    client = TestClient(app)
    for path in ("/", "/static/index.html"):
        assert client.get(path).headers["content-security-policy"] == FRONTEND_CSP_BAN_DO
