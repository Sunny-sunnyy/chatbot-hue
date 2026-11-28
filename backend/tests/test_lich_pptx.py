"""Xuất lịch ra PowerPoint (`api/lich_pptx.py`) — code điền đối tượng lịch vào các trang, không model.
Khoá các sàn ghi trước của plan: mọi điểm có mặt đúng ngày / buổi / giờ / thứ tự · ghi chú an toàn theo vào file, dự báo cũ thì không · dùng đủ ảnh tự host,
KHÔNG in ghi công ảnh (chủ dự án 14/11) · câu an toàn của LƯỢT theo vào file · ngày dài chia trang ĐỀU, không mất điểm · chữ trong file ⊂ chữ của lịch + hằng số của khuôn.
Lịch trong test tự dựng (không phải dữ liệu bộ đo). Phần đọc lại file cần `python-pptx` (chưa có trong môi trường ⇒ bỏ qua, ghi rõ)."""
import io
from pathlib import Path

import pytest

from api.lich_pptx import CAU_TOI_DA, DONG_DU_BAO, DONG_NGUON, DONG_THAY_DOI, MAP_PREFIX, dung_pptx, trang_lich

COMMONS = {"src": "/anh/lich/dai_noi.jpg", "tac_gia": "Người Chụp", "giay_phep": "CC BY-SA 4.0", "trang": "https://commons.wikimedia.org/x"}
ANH_WEB = {"src": "/anh/lich/pho_tay.jpg", "nguon": "web", "ten_mien": "vi-du.vn", "trang": "https://vi-du.vn/x"}   # không có giấy phép


def muc(ngay, buoi, k, ten, gio, anh=None, ghi_chu=None, loai="tham_quan"):
    return {"id_muc": f"n{ngay}-{buoi}-{k}", "buoi": buoi, "loai": loai, "id_diem": ten.lower(), "ten": ten, "gio": gio, "ghi_chu": ghi_chu, "anh": anh,
            "map_url": MAP_PREFIX + "?api=1&query=" + ten.replace(" ", "+")}


def lich_mau(so_muc_ngay_2=2):
    ngay_2 = [muc(2, "sang", i + 1, f"Điểm {i + 1}", f"{8 + i}:00 – {8 + i}:45") for i in range(so_muc_ngay_2)]
    return {"phien_ban": 2, "tham_so": {"so_ngay": 2, "ngay_di": "2026-12-05"}, "minh_hieu": "Mình hiểu: 2 ngày · 2 người lớn — sai thì bấm **Sửa**.",
            "ngay": [{"ngay": 1, "ngay_thang": "2026-12-05", "chang": ["Kinh thành"],
                      "muc": [muc(1, "sang", 1, "Đại Nội Huế", "8:00 – 10:30", COMMONS), muc(1, "chieu", 1, "Khu phố Tây", "13:30 – 14:45", ANH_WEB),
                              muc(1, "toi", 1, "Chợ Đông Ba", "18:00 – 23:00", None, "phố ẩm thực đêm trước cổng chợ", "hoat_dong_toi")]},
                     {"ngay": 2, "ngay_thang": "2026-12-06", "chang": [], "muc": ngay_2}],
            "ghi_chu": [{"ma": "tam_dung_mua", "cau": "Thác tạm dừng đón khách mùa mưa lũ."}, {"ma": "du_bao", "cau": "Ngày 1: mưa 90 %."},
                        {"ma": "gio_goi_y", "cau": "Giờ trong lịch là giờ gợi ý."}],
            "an": [{"ngay": 1, "bua": "trua", "gan": "Đại Nội Huế", "quan": [{"ten": "Quán A"}, {"ten": "Quán B"}]}]}


CAU = {"n1-sang-1": "Khám phá Hoàng thành [1].", "n1-toi-1": "Dạo chợ đêm [Nguồn 3]."}


def test_every_item_is_present_in_order_with_time_and_session():
    trang = trang_lich(lich_mau(), CAU, ngay_tao="19/11/2026")
    assert [t["kieu"] for t in trang] == ["bia", "ngay", "ngay", "luu_y"]
    n1 = trang[1]
    assert (n1["so"], n1["tiep"], n1["ngay_chu"]) == (1, False, "Thứ Bảy 5/12/2026")
    assert [(m["buoi"], m["gio"], m["ten"]) for m in n1["muc"]] == [("Sáng", "8:00 – 10:30", "Đại Nội Huế"), ("Chiều", "13:30 – 14:45", "Khu phố Tây"),
                                                                    ("Tối", "18:00 – 23:00", "Chợ Đông Ba")]
    assert n1["muc"][0]["cau"] == "Khám phá Hoàng thành." and n1["muc"][2]["cau"] == "Dạo chợ đêm."   # mã nguồn [n] không vào file
    assert n1["muc"][2]["ghi_chu"] == "phố ẩm thực đêm trước cổng chợ" and n1["an"] == [{"bua": "Trưa", "gan": "Đại Nội Huế", "quan": ["Quán A", "Quán B"]}]
    assert trang[0]["so_diem"] == 5 and trang[0]["tom_tat"] == "2 ngày · 2 người lớn"
    assert trang[0]["diem_chinh"] == ["Đại Nội Huế", "Khu phố Tây", "Điểm 1", "Điểm 2"]          # điểm ban ngày đầu tiên, theo thứ tự đi
    assert [d["ten"] for d in trang[3]["ban_do"]] == ["Đại Nội Huế", "Khu phố Tây", "Chợ Đông Ba", "Điểm 1", "Điểm 2"]


def test_long_description_is_cut_at_a_word_boundary_but_names_and_times_never_are():
    dai = "Rất dài " * 40
    lich = lich_mau()
    lich["ngay"][0]["muc"][0]["ten"] = "Tên điểm rất dài " * 6
    m = trang_lich(lich, {"n1-sang-1": dai + "[2]."})[1]["muc"][0]
    assert len(m["cau"]) <= CAU_TOI_DA + 1 and m["cau"].endswith("dài…") and m["ten"] == "Tên điểm rất dài " * 6 and m["gio"] == "8:00 – 10:30"


def test_safety_notes_follow_into_the_file_but_stale_forecast_does_not():
    dong = [d for t in trang_lich(lich_mau(), CAU) if t["kieu"] == "luu_y" for d in t["dong"]]
    assert "Thác tạm dừng đón khách mùa mưa lũ." in dong and DONG_THAY_DOI in dong and DONG_DU_BAO in dong and DONG_NGUON in dong
    assert not any("mưa 90 %" in d for d in dong)   # dự báo lấy lúc trả lời, server không lưu ⇒ không in số cũ vào file tải về


def test_all_self_hosted_photos_are_used_and_nothing_is_credited():
    """Chủ dự án 14/11/2026 (nhắc lại 19/11): gỡ mọi chữ ghi công khỏi hệ thống ⇒ file dùng đủ ảnh của bảng ảnh (cả ảnh lấy từ trang web khác),
    không có trang nguồn ảnh, không in tác giả / giấy phép. Ảnh ngoài `/anh/lich/` hoặc có thư mục con / ".." ⇒ không dùng."""
    lich = lich_mau()
    lich["ngay"][0]["muc"][2]["anh"] = {"src": "/anh/lich/../../bi_mat.jpg"}
    trang = trang_lich(lich, CAU)
    anh = [m["anh"] for t in trang if t["kieu"] == "ngay" for m in t["muc"]]
    assert anh[:3] == [{"src": "/anh/lich/dai_noi.jpg"}, {"src": "/anh/lich/pho_tay.jpg"}, None]
    assert trang[0]["anh"] == [{"src": "/anh/lich/dai_noi.jpg"}, {"src": "/anh/lich/pho_tay.jpg"}]
    assert [t["kieu"] for t in trang][-1] == "luu_y" and "nguon_anh" not in {t["kieu"] for t in trang}
    assert not any(x in str(trang) for x in ("Người Chụp", "CC BY", "Commons", "vi-du.vn", "tac_gia", "giay_phep"))


@pytest.mark.parametrize("so, chia", [(5, [5]), (6, [3, 3]), (7, [4, 3]), (11, [4, 4, 3])])
def test_long_day_is_split_evenly_and_loses_nothing(so, chia):
    ngay_2 = [t for t in trang_lich(lich_mau(so), CAU, 5) if t["kieu"] == "ngay" and t["so"] == 2]
    assert [len(t["muc"]) for t in ngay_2] == chia and [t["tiep"] for t in ngay_2] == [False] + [True] * (len(chia) - 1)
    assert [m["ten"] for t in ngay_2 for m in t["muc"]] == [f"Điểm {i + 1}" for i in range(so)]


def test_plan_without_any_photo_still_builds():
    lich = lich_mau()
    for m in lich["ngay"][0]["muc"]:
        m["anh"] = None
    trang = trang_lich(lich, CAU)
    assert trang[0]["anh"] == [] and trang[-1]["kieu"] == "luu_y"


def test_file_text_is_a_subset_of_plan_text_plus_template_constants(tmp_path):
    """Đọc LẠI file đã dựng: mỗi đoạn chữ trong file phải là chữ của lịch (tên, giờ, câu tả đã bỏ mã nguồn, ghi chú) hoặc chữ cố định của khuôn."""
    pptx = pytest.importorskip("pptx")
    lich = lich_mau(7)
    trang = trang_lich(lich, CAU, ngay_tao="19/11/2026")
    prs = pptx.Presentation(io.BytesIO(dung_pptx(trang, Path(tmp_path))))   # thư mục ảnh rỗng ⇒ ô hoạ tiết mang tên điểm thay ảnh, không lỗi
    assert len(prs.slides) == len(trang)
    chu = [p.text for s in prs.slides for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs if p.text.strip()]
    cho_phep = " ".join(str(v) for t in trang for v in ([t.get(k) for k in ("tieu_de", "tom_tat", "ngay_chu", "chang")] + (t.get("dong") or []) + (t.get("diem_chinh") or [])
                                                        + [x for a in t.get("an") or [] for x in (a["bua"], a["gan"], *a["quan"])] + [d["ten"] for d in t.get("ban_do") or []]
                                                        + [x for m in t.get("muc") or [] for x in (m["buoi"], m["gio"], m["ten"], m["cau"], m["ghi_chu"])]) if v)
    co_dinh = ("Lịch trình Huế · trang", "điểm tham quan", "Tạo ngày 19/11/2026", "Ngày ", "Lưu ý trước khi đi", "Ăn gần đó", "Mở bản đồ từng điểm",
               " gần ", "•  ", "Bấm tên điểm để mở bản đồ.", "File này sửa được: đổi chữ, thêm ảnh của bạn trước khi gửi cho người đi cùng.")
    for doan in chu:
        con = doan
        for c in co_dinh:
            con = con.replace(c, " ")
        assert all(tu.strip(",:") in cho_phep or tu in ("(tiếp)", "·", "—") or tu.isdigit() for tu in con.split()), doan
    link = {sh.text_frame.text: sh.click_action.hyperlink.address for s in prs.slides for sh in s.shapes
            if sh.has_text_frame and sh.click_action.hyperlink.address}
    assert len(link) == 10 and all(u.startswith(MAP_PREFIX) for u in link.values())          # chỉ link bản đồ do code dựng; chữ hiện ra là TÊN điểm
    trang_ngay_2 = [i for i, t in enumerate(trang) if t["kieu"] == "ngay" and t["so"] == 2]
    ten = [p.text for i in trang_ngay_2 for sh in prs.slides[i].shapes if sh.has_text_frame for p in sh.text_frame.paragraphs if p.text.startswith("Điểm ")]
    assert [x for k, x in enumerate(ten) if x not in ten[:k]] == [f"Điểm {i + 1}" for i in range(7)]   # thứ tự điểm ngày 2 giữ nguyên qua các trang


# ---------- đường tải `GET /api/lich/pptx` (bảng điểm thật — private; không model, không bộ tìm) ----------
@pytest.fixture(scope="module")
def may_chu():
    """App tối thiểu chỉ có route tải + kho hội thoại thật + cờ nạp từ settings (bật `xuat_pptx`). Đồng hồ giả để thử hết hạn."""
    pytest.importorskip("pptx")
    import copy
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from api.conversations import ConversationStore
    from api.routes.xuat import router
    from core.settings_loader import load_settings
    from llm import lich_trinh_v2 as lt2
    from llm import sua_lich_v2 as sl
    from llm.assistant import AssistantFlags
    s = copy.deepcopy(load_settings(validate_private_paths=False))
    s["assistant"]["xuat_pptx"] = True
    s["assistant"]["slide_designer"] = False
    flags = AssistantFlags.from_settings(s)
    gio = [1000.0]
    app = FastAPI()
    app.include_router(router)
    app.state.assistant_flags, app.state.conversations = flags, ConversationStore(len, clock=lambda: gio[0])
    khung = lt2.xep_v2(flags.bang_lich_v2, lt2.tu_truong({"so_ngay": 2, "nguoi_lon": 2}))
    luu = sl.luu_tu_lich(khung, None, None)
    diem = lt2.diem_v2(khung)
    luu["cau"] = {diem[0]: "Câu tả đã kiểm của điểm đầu [1]."}
    return TestClient(app), app, gio, luu, [flags.bang_lich_v2.theo_id[j]["ten"] for j in diem]


def test_download_is_404_when_flag_off_or_no_saved_plan(may_chu):
    client, app, gio, luu, _ = may_chu
    assert client.get("/api/lich/pptx").json()["error"]["code"] == "khong_co_lich"            # không cookie ⇒ không có lịch, không file rỗng
    cid = app.state.conversations.ensure(None)
    assert client.get("/api/lich/pptx", cookies={"conversation_id": cid}).status_code == 404   # cuộc có thật nhưng chưa có lịch
    bat = app.state.assistant_flags
    app.state.assistant_flags = __import__("dataclasses").replace(bat, xuat_pptx=False)
    try:
        r = client.get("/api/lich/pptx", cookies={"conversation_id": cid})
        assert (r.status_code, r.json()["error"]["code"]) == (404, "not_found")
    finally:
        app.state.assistant_flags = bat


def test_download_rebuilds_the_saved_plan_and_expires_with_it(may_chu):
    import pptx
    client, app, gio, luu, ten_diem = may_chu
    store = app.state.conversations
    cid = store.ensure(None)
    store.luu_lich(cid, luu)
    r = client.get("/api/lich/pptx?ten=../../x", cookies={"conversation_id": cid})   # tham số lạ bị bỏ qua: route không đọc tham số nào
    assert r.status_code == 200 and r.headers["content-type"].startswith("application/vnd.openxmlformats")
    assert "lich-trinh-hue.pptx" in r.headers["content-disposition"] and r.headers["cache-control"] == "no-store"
    trang = [[p.text for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs] for s in pptx.Presentation(io.BytesIO(r.content)).slides]
    chu = [c for t in trang for c in t]
    ngay = [c for t in trang if any(x.startswith("Ngày ") for x in t) for c in t if c in ten_diem]   # chỉ các trang "Ngày N"
    assert [c for k, c in enumerate(ngay) if c not in ngay[:k]] == ten_diem           # mọi điểm của lịch lưu, đúng thứ tự đi
    assert "Câu tả đã kiểm của điểm đầu." in chu and DONG_THAY_DOI in " ".join(chu)    # câu tả đã bỏ mã nguồn; dòng "có thể đã thay đổi" theo vào file
    assert not any("api=1" in c or "http" in c for c in chu)                           # không link / đường dẫn nào trong chữ
    gio[0] += 31 * 60                                                                  # quá hạn 30 phút, cuộc chưa bị dọn
    het = client.get("/api/lich/pptx", cookies={"conversation_id": cid})
    assert (het.status_code, het.json()["error"]["code"]) == (404, "khong_co_lich")


# ---------- câu AN TOÀN của LƯỢT (bão / lũ: bản tin chính thức + 112) phải theo vào file (review nhánh, M1) ----------
def test_turn_safety_sentence_is_first_note_and_on_cover():
    """Màn hình vẽ câu này đậm ở đầu thẻ lịch; file dựng từ trạng thái lưu nên trạng thái lưu phải mang nó. Không có ⇒ file y như trước."""
    from llm import thoi_tiet as tt
    co = trang_lich(lich_mau(), CAU, an_toan=tt.CAU_BAO_LU)
    luu_y = next(t for t in co if t["kieu"] == "luu_y")
    assert luu_y["dong"][0] == tt.CAU_BAO_LU and luu_y["an_toan"] is True and co[0]["an_toan"] == tt.CAU_BAO_LU
    khong = trang_lich(lich_mau(), CAU)
    assert khong[0]["an_toan"] is None and not next(t for t in khong if t["kieu"] == "luu_y")["an_toan"]
    assert all(tt.CAU_BAO_LU not in d for t in khong for d in t.get("dong") or [])


def test_saved_plan_keeps_the_storm_sentence_of_its_turn():
    """Route: lượt lịch mà dòng ghi chú có câu bão / lũ ⇒ trạng thái lưu mang đúng HẰNG SỐ đó (không chữ tự do); lượt thường ⇒ không có khoá."""
    from api.routes.chat import an_toan_cua_luot
    from llm import thoi_tiet as tt
    from llm.assistant import AnswerTrace
    assert an_toan_cua_luot(AnswerTrace(notice=f"{tt.CAU_BAO_LU} Giờ mở cửa có thể đã thay đổi.")) == tt.CAU_BAO_LU
    assert an_toan_cua_luot(AnswerTrace(notice="Giờ mở cửa có thể đã thay đổi.")) is None and an_toan_cua_luot(AnswerTrace()) is None


def test_download_carries_the_saved_storm_sentence(may_chu):
    import pptx
    from llm import thoi_tiet as tt
    client, app, gio, luu, _ = may_chu
    gio[0] += 3600                                   # cuộc mới sau ca hết hạn của test trước
    store = app.state.conversations
    cid = store.ensure(None)
    store.luu_lich(cid, {**luu, "an_toan": tt.CAU_BAO_LU})
    r = client.get("/api/lich/pptx", cookies={"conversation_id": cid})
    assert r.status_code == 200
    trang = [[p.text for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs] for s in pptx.Presentation(io.BytesIO(r.content)).slides]
    assert tt.CAU_BAO_LU in trang[0]                                                    # bìa
    luu_y = next(t for t in trang if "Lưu ý trước khi đi" in t)
    assert [d for d in luu_y if d.startswith("•")][0] == "•  " + tt.CAU_BAO_LU           # dòng ĐẦU của trang lưu ý
