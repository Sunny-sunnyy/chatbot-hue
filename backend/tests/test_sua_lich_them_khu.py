"""Cờ `sua_lich_them_khu` (BẢN THỬ 23/11/2026, chờ chủ dự án quyết — đổi luật khu) — 0 USD, không gọi model. Vì sao: sau khi cho lệnh thêm vượt nhịp
đi (`sua_lich_them_day`), thứ còn chặn phần lớn lệnh "thêm X" là luật KHU (một ngày quá hai khu, hai khu không liền nhau): đoàn thường 319 ⇒ 836 /
1.116 lệnh làm được khi cho đi sang khu không kề với phút đi lấy từ bảng khoảng cách (liệt kê 108 lịch mẫu). File kiểm phần code trên bảng thật: bảng
phút chưa nạp / cờ tắt ⇒ y như bản chỉ nới nhịp; cờ bật ⇒ chặng sang khu không kề có số phút thật, ≤ 60 phút, giờ nối đủ số phút đó, dòng báo nêu chặng."""
import pytest

from llm import khoang_cach as kc
from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_cong_dot_1 import flags_from
from test_sua_lich_them_day import NGAY_DIEM, _lenh, _them
from test_sua_lich_v2 import B, _lich

T = B.theo_id
KC = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, khoang_cach=True).khoang_cach_bang
KHU = {"qua_2_cum", "cum_khong_ke", "ghep_khong_ke"}


@pytest.fixture
def bang_phut():
    """Nạp bảng phút cho đúng một ca test rồi trả về None (biến mức module của `lich_trinh_v2`)."""
    phut = v2.bu_phut_khu(B, kc.bang_phut(KC))  # như nơi dựng cờ: bảng khoảng cách + cặp thiếu bù bằng chặng dài nhất đã biết giữa hai khu
    v2.dat_phut_khu(phut)
    yield phut
    v2.dat_phut_khu(None)


def test_flag_defaults_off_needs_its_parents_and_loads_no_table_when_off():
    assert AssistantFlags().sua_lich_them_khu is False
    with pytest.raises(ValueError, match="sua_lich_them_khu needs"):
        AssistantFlags(sua_lich_them_khu=True)
    v2.dat_phut_khu({"a|b": 1})
    flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True)  # cờ tắt ⇒ nơi dựng cờ trả biến bảng phút về None
    assert v2.PHUT_KHU is None


def test_minutes_table_uses_the_distance_tool_formula_rounded_up_to_five():
    phut = kc.bang_phut(KC)
    khoa, v = next(iter(KC.cap.items()))
    goc = int(v["phut"] * kc.HE_SO_OSRM + 0.5) + kc.PHUT_CONG
    assert phut[khoa] % 5 == 0 and 0 <= phut[khoa] - goc < 5
    a, b = khoa.split("|")
    assert f"{b}|{a}" in phut  # cặp một chiều dùng cho cả hai chiều


def test_without_the_table_or_the_switch_it_is_the_pace_only_behaviour(bang_phut):
    k, luu = _lich(2, "can_bang")
    for i, ng, b in _lenh(k):
        a = _them(luu, i, ng, b, them_day=True)  # bảng đã nạp, công tắc khu tắt
        v2.dat_phut_khu(None)
        assert a == _them(luu, i, ng, b, them_day=True) == _them(luu, i, ng, b, them_day=True, them_khu=True)  # chưa nạp bảng ⇒ công tắc khu không làm gì
        v2.dat_phut_khu(bang_phut)


@pytest.mark.parametrize("n,kieu", [(2, "can_bang"), (3, "nhe_nhang")])
def test_add_across_non_adjacent_areas_is_applied_timed_with_real_minutes_and_reported(n, kieu, bang_phut):
    """Quét mọi lệnh thêm trên một lịch vừa xếp: ca bản chỉ-nới-nhịp đã làm được ⇒ kết quả không đổi; ca chỉ làm được nhờ khu ⇒ ngày có cả hai dấu, khung
    đúng luật, bỏ dấu khu đi thì chỉ còn mã luật khu, mỗi chặng sang khu không kề có số trong bảng ≤ trần và giờ nối đủ số phút đó, dòng báo nêu chặng."""
    k, luu = _lich(n, kieu)
    n_khu = 0
    for i, ng, b in _lenh(k):
        a = _them(luu, i, ng, b, them_day=True)
        kq = _them(luu, i, ng, b, them_day=True, them_khu=True)
        if a["da_ap"]:
            assert kq == a
            continue
        if not kq["da_ap"]:
            assert kq["khung"] == k
            continue
        n_khu += 1
        ap, moi = kq["da_ap"][0], kq["khung"]
        ngay = ap["ngay"]
        assert moi["khu_them"] == kq["luu"]["khu_them"] == [ngay] and ngay in moi["day_them"] and v2.kiem_khung_v2(B, moi) == []
        khong_dau = {x: v for x, v in moi.items() if x != "khu_them"}
        assert set(v2.kiem_khung_v2(B, khong_dau)) and set(v2.kiem_khung_v2(B, khong_dau)) <= KHU
        d = next(x for x in moi["ngay"] if x["ngay"] == ngay)
        day = [j for bb in v2.BUOI_NGAY for j in d["buoi"][bb]]
        sang_cuoi = d["buoi"]["sang"][-1] if d["buoi"]["sang"] else None
        for x, y in zip(day, day[1:]):
            if v2._phut_di(T[x], T[y]) is not None:
                continue
            m = bang_phut[f"{x}|{y}"]
            assert m <= v2.TRAN_PHUT_KHU
            ket = v2.ra_phut(moi["gio"][x].split("–")[1].strip())
            bat = v2.ra_phut(moi["gio"][y].split("–")[0].strip())
            assert bat >= ket + (v2.NGHI_TRUA + m if x == sang_cuoi else m)  # qua bữa trưa: 60 phút ăn + TRỌN số phút của chặng không kề
        cau = s.thay_doi(B, kq)[0]["cau"]
        assert f"Ngày {ngay} nay đi qua {ap['khu']['so_khu']} khu" in cau and "nay có buổi dày hơn nhịp" in cau
        co_chang = any(v2._phut_di(T[x], T[y]) is None for x, y in zip(day, day[1:]))
        assert bool(ap["khu"]["chang"]) == co_chang and ("là hai khu không liền nhau, đi mất khoảng" in cau) == co_chang
        assert co_chang or ap["khu"]["so_khu"] >= 3  # không có chặng không kề ⇒ ngày đi ba khu nối nhau từng đôi
        bo = s.ap(B, kq["luu"], [s.HanhDong(loai="bo_diem", ten=T[i]["ten"])], them_khong_the=True, them_day=True, them_khu=True)
        assert bo["da_ap"] and v2.kiem_khung_v2(B, bo["khung"]) == []  # bỏ chính điểm vừa thêm thì lịch về lại hợp luật
    assert n_khu > 0


def test_a_leg_longer_than_the_ceiling_is_still_refused():
    """Mọi chặng giữa hai khu không kề dài hơn trần ⇒ không lệnh nào được thêm nhờ khu (y như bản chỉ nới nhịp)."""
    v2.dat_phut_khu({khoa: v2.TRAN_PHUT_KHU + 5 for khoa in kc.bang_phut(KC)})
    try:
        k, luu = _lich(2, "can_bang")
        for i, ng, b in _lenh(k):
            kq = _them(luu, i, ng, b, them_day=True, them_khu=True)
            assert not (kq["da_ap"] and kq["da_ap"][0].get("khu", {}).get("chang"))
            assert v2.kiem_khung_v2(B, kq["khung"]) == []
    finally:
        v2.dat_phut_khu(None)


def test_groups_with_children_or_elderly_are_not_changed(bang_phut):
    k = v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang", so_thich=("di_tich",), lon_tuoi=True))
    luu = s.luu_tu_lich(k, None, None)
    for i in [j for j in NGAY_DIEM if j not in s._vi_tri(k)][:12]:
        assert _them(luu, i, them_day=True, them_khu=True) == _them(luu, i)


def test_every_day_pair_in_non_adjacent_areas_has_minutes(bang_phut):
    """Điểm không có trong bảng khoảng cách (Không gian lưu niệm Lê Bá Đảng — không toạ độ) được bù bằng chặng DÀI NHẤT đã biết giữa hai khu đó: không
    bù thì lịch đã có điểm ấy kẹt ở lệnh "bỏ" kế tiếp (1 / 2.752 lệnh trên lưới 108 lịch)."""
    goc = kc.bang_phut(KC)
    thieu = [i for i in NGAY_DIEM if not any(k.startswith(f"{i}|") for k in goc)]
    assert thieu == ["kg_le_ba_dang"]
    for a in NGAY_DIEM:
        for b in NGAY_DIEM:
            if a != b and v2._phut_di(T[a], T[b]) is None and v2.CUM_XA not in (T[a]["cum"], T[b]["cum"]):
                assert f"{a}|{b}" in bang_phut, (a, b)
    x = thieu[0]
    y = next(j for j in NGAY_DIEM if v2._phut_di(T[x], T[j]) is None and f"{x}|{j}" in bang_phut)
    cung_khu = [goc[f"{a}|{y}"] for a in NGAY_DIEM if T[a]["cum"] == T[x]["cum"] and f"{a}|{y}" in goc]
    assert bang_phut[f"{x}|{y}"] >= max(cung_khu)  # ước dư, không ước thiếu


def test_default_schedule_picks_the_slot_with_fewest_cross_area_legs_and_says_the_true_reason(bang_phut):
    """Lịch mặc định của trang Lên kế hoạch (soi 23/11/2026). Chọn chỗ: "thêm Trường Quốc Học Huế" từng rơi vào giữa hai lăng của ngày 2 (hai chặng không
    kề, đi ra trung tâm rồi quay lại) ⇒ nay cuối buổi chiều, một chặng. Thẻ lịch in số phút của chặng không kề (kể cả chặng qua bữa trưa). Lệnh vẫn bị
    từ chối thì câu nói thứ CÒN chặn sau khi đã nới khu: hết giờ / khu xa — không còn "hai khu không liền nhau"."""
    k, luu = _lich(2, "can_bang", so_thich=())
    ten = {d["ten"]: i for i, d in T.items()}
    n_duoc = 0
    for i, ng, b in _lenh(k):
        if ng is not None:
            continue
        kq = _them(luu, i, them_day=True, them_khu=True)
        if not kq["da_ap"]:
            cau = s.thay_doi(B, kq)[0]["cau"]
            assert "hai khu không liền nhau" not in cau and "đang kín" not in cau and "phạm luật xếp" not in cau
            continue
        n_duoc += 1
        if not kq["da_ap"][0].get("khu"):
            continue
        # chỗ được chọn có ít chặng không kề nhất trong mọi chỗ làm được
        ts, vt = s._ts(k["tham_so"]), s._vi_tri(k)
        # (từ 23/11/2026 lệnh thêm có bước cuối "chèn trước một điểm đang có": lệnh chỉ làm được nhờ bước đó thì so trong các chỗ của bước đó)
        def so_chang(chen):
            return [len(v2.chang_khu(B, next(x for x in k2["ngay"] if x["ngay"] == cho[0]))[1]) for cho in s._cho_thu(B, k, i, None, None)
                    if (k2 := s._thu_cho(B, luu, ts, vt, [], i, cho, False, day_moi=cho[0], khu_moi=cho[0], chen=chen)[0]) is not None]

        assert len(kq["da_ap"][0]["khu"]["chang"]) == min(so_chang(False) or so_chang(True))
        # thẻ: mỗi chặng không kề của ngày đó mang đúng số phút của bảng ở mục ĐẾN
        ngay = kq["da_ap"][0]["ngay"]
        muc = {m["id_diem"]: m for m in next(x for x in v2.dung_lich(B, kq["khung"], {})["ngay"] if x["ngay"] == ngay)["muc"]}
        d = next(x for x in kq["khung"]["ngay"] if x["ngay"] == ngay)
        day = [j for bb in v2.BUOI_NGAY for j in d["buoi"][bb]]
        for x, y in zip(day, day[1:]):
            if v2._phut_di(T[x], T[y]) is None:
                assert muc[y]["phut_di"] == bang_phut[f"{x}|{y}"]
    # lịch mặc định (bảng điểm bản 13): 25 / 31 điểm chưa có thêm được (11 chỉ nhờ nới nhịp, 14 nhờ sang khu); 26 từ 23/11/2026 — Duyệt Thị Đường
    # (suất diễn giờ cố định) vào được nhờ bước cuối "chèn trước một điểm đang có"
    assert n_duoc == 26
    qh = _them(luu, ten["Trường Quốc Học Huế"], them_day=True, them_khu=True)["da_ap"][0]
    assert (qh["ngay"], qh["buoi"]) == (2, "chieu") and len(qh["khu"]["chang"]) == 1
    cau = lambda t: s.thay_doi(B, _them(luu, ten[t], them_day=True, them_khu=True))[0]["cau"]  # noqa: E731
    assert f"cũng vướng: {s.CAU_LY_DO['kin']}." in cau("Lăng Gia Long")
    assert f"cũng vướng: {s.CAU_LY_DO['khu_xa']}." in cau("Vườn quốc gia Bạch Mã")


def test_replace_or_move_on_a_day_that_already_crosses_areas_is_accepted_and_says_so(bang_phut):
    """Ngày người dùng đã nhận đi sang khu không kề: lệnh THAY / DỜI trên ngày đó được nhận theo luật khu đã nới (không thì ngày ấy thành kẹt) và dòng
    trả lời nói thật ngày đó VẪN đi qua mấy khu, chặng nào, bao nhiêu phút (phiên đọc code 23/11/2026: dòng "Đã thay…" từng không nói gì)."""
    k, luu = _lich(2, "can_bang", so_thich=())
    ten = {d["ten"]: i for i, d in T.items()}
    kw = dict(them_khong_the=True, them_day=True, them_khu=True)
    dau = _them(luu, ten["Trường Quốc Học Huế"], them_day=True, them_khu=True)
    ngay = dau["da_ap"][0]["ngay"]
    co_thay = co_doi = 0
    for cu in [j for j, v in s._vi_tri(dau["khung"]).items() if v[0] == ngay and j != ten["Trường Quốc Học Huế"]]:
        for moi in [j for j in NGAY_DIEM if j not in s._vi_tri(dau["khung"])][:14]:
            kq = s.ap(B, dau["luu"], [s.HanhDong(loai="thay_diem", ten=T[cu]["ten"], ten_moi=T[moi]["ten"])], **kw)
            if not kq["da_ap"]:
                continue
            assert v2.kiem_khung_v2(B, kq["khung"]) == []
            cau = s.thay_doi(B, kq)[0]["cau"]
            con_dau = ngay in (kq["khung"].get("khu_them") or ())
            assert (f" Ngày {ngay} vẫn đi qua " in cau) == con_dau, cau
            co_thay += con_dau
    for b in v2.BUOI_NGAY:  # dời chính điểm vừa thêm sang buổi kia của cùng ngày
        kq = s.ap(B, dau["luu"], [s.HanhDong(loai="doi_buoi", ten="Trường Quốc Học Huế", ngay=ngay, buoi=b)], **kw)
        if kq["da_ap"] and ngay in (kq["khung"].get("khu_them") or ()):
            co_doi += 1
            assert f" Ngày {ngay} vẫn đi qua " in s.thay_doi(B, kq)[0]["cau"]
    assert co_thay > 0 and co_doi > 0
