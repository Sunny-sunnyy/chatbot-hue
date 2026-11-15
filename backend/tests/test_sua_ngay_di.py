"""Sửa lịch bằng lời — đổi ngày đi (plan `docs/superpowers/plans/2026-11-15-sua-lich-ngay-di-plan.md`), phần code 0 USD:
Luôn-a: ngày do code đọc từ chữ người dùng (bảng ca tự đặt); Luôn-b: áp ngày mới trên 3.840 khung thật × 3 ngày — khung sau đúng luật,
điểm đã bỏ không quay lại, giữ được thì y nguyên, câu báo khớp số đếm lại độc lập."""
import datetime as dt
import itertools

import pytest

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as sl
from llm.do_so import NGAY_CHUA_RO, NGAY_KHONG_CO, ngay_tu_cau
from test_cong_dot_1 import flags_from

B = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True).bang_lich_v2
HOM = dt.date(2026, 11, 15)  # Chủ nhật
D = dt.date

CA_NGAY = [
    ("đổi ngày đi sang 20/12", D(2026, 12, 20)), ("mình đi từ 20/12/2026 nhé", D(2026, 12, 20)), ("Đi ngày 5/1 được không", D(2027, 1, 5)),
    ("khởi hành ngày 20 tháng 12", D(2026, 12, 20)), ("đi từ 3 tháng 1 năm 2027", D(2027, 1, 3)), ("hôm nay đi luôn", HOM),
    ("mai mình đi", D(2026, 11, 16)), ("dời sang ngày mai", D(2026, 11, 16)), ("ngày kia mới đi", D(2026, 11, 17)), ("đi ngày mốt", D(2026, 11, 17)),
    ("đổi sang thứ bảy", D(2026, 11, 21)), ("thứ 4 mình mới tới Huế", D(2026, 11, 18)), ("chủ nhật đi", HOM), ("đi CN tuần sau", D(2026, 11, 22)),
    ("thứ hai tuần sau", D(2026, 11, 16)), ("thứ sáu tuần tới mới đi", D(2026, 11, 20)), ("đi cuối tuần này", D(2026, 11, 21)),
    ("cuối tuần sau đi", D(2026, 11, 21)), ("thứ bảy 21/11 nha", D(2026, 11, 21)),  # hai cách nói, cùng một ngày
    ("15/11", HOM), ("14/11", D(2027, 11, 14)),  # không năm ⇒ lần tới gần nhất (nơi gọi chặn quá 180 ngày)
    ("14/11/2026", D(2026, 11, 14)),  # nêu năm ⇒ giữ nguyên, nơi gọi báo đã qua
    # không đọc được MỘT ngày ⇒ không đoán
    ("thay vì 20/12 thì đi 27/12", NGAY_CHUA_RO), ("dời lại 2 hôm", NGAY_CHUA_RO), ("lùi một tuần", NGAY_CHUA_RO), ("đi sớm hơn 1 ngày", NGAY_CHUA_RO),
    ("đổi ngày đi giúp mình", NGAY_CHUA_RO), ("đi dịp Tết", NGAY_CHUA_RO), ("rằm tháng giêng mình đi", NGAY_CHUA_RO), ("đi ngày 20/12 âm", NGAY_CHUA_RO),
    ("tuần sau mới đi", NGAY_CHUA_RO), ("ngày 2 chỉ đi buổi sáng", NGAY_CHUA_RO), ("ngày thứ ba bỏ lăng Tự Đức", NGAY_CHUA_RO),
    ("lịch 3 ngày thôi", NGAY_CHUA_RO), ("mai hay ngày kia đều được", NGAY_CHUA_RO),
    ("đi ngày 30/2", NGAY_KHONG_CO), ("31 tháng 11", NGAY_KHONG_CO),
    # review E M-1: chữ GIỐNG ngày không phải ngày ⇒ không đọc ra ngày (8 ca dò của E + ca cùng họ)
    ("dời ngày đi giúp, mình đi với chị Mai", NGAY_CHUA_RO), ("đổi ngày khởi hành, mình ở đường Mai Thúc Loan", NGAY_CHUA_RO),
    ("đổi ngày đi, bỏ điểm thứ hai trong lịch", NGAY_CHUA_RO), ("dời ngày, điểm thứ 3 bỏ đi", NGAY_CHUA_RO),
    ("lùi chuyến lại, mỗi nơi chỉ ở 1/2 ngày thôi", NGAY_CHUA_RO), ("dời chuyến, quán mở 24/7 mà", NGAY_CHUA_RO),
    ("đổi ngày đi, tỉ lệ 3/4 nhóm bận", NGAY_CHUA_RO), ("đổi ngày đi, nhóm có 2 tháng 3 ngày nghỉ", NGAY_CHUA_RO),
    ("dời ngày đi, bạn Mai Anh chưa xin nghỉ được", NGAY_CHUA_RO), ("đổi ngày đi, mình thích ngắm hoa mai", NGAY_CHUA_RO),
    ("đổi ngày đi, bỏ quán thứ hai với lần thứ ba ghé chợ", NGAY_CHUA_RO), ("dời chuyến, đi khoảng 2/3 quãng đường thì nghỉ", NGAY_CHUA_RO),
    # … nhưng một ngày thật trong cùng câu vẫn đọc đúng (không từ chối nhầm)
    ("đổi sang 20/12 và bỏ điểm thứ hai", D(2026, 12, 20)), ("mai đi luôn, chị Mai cũng đi", D(2026, 11, 16)),
    ("Mai đi luôn nhé", D(2026, 11, 16)), ("Ok. Mai mình đi", D(2026, 11, 16)), ("tối mai tới Huế, đổi ngày đi", D(2026, 11, 16)),
    ("sáng thứ hai mình tới, bỏ điểm thứ hai", D(2026, 11, 16)), ("đi 24/7 nhé", NGAY_CHUA_RO), ("đi từ 24/12, quán mở 24/7", D(2026, 12, 24)),
    # E kiểm phần sửa (19 câu mới, 7 lệch): 4 câu còn ra SAI ngày ⇒ nay "chưa rõ"; 2 câu từ chối nhầm ⇒ nay đúng ngày
    ("dời ngày, tuần thứ hai của tháng bận", NGAY_CHUA_RO), ("đổi ngày đi, tỷ lệ 1/2", NGAY_CHUA_RO), ("dời chuyến, vé 1/2 giá", NGAY_CHUA_RO),
    ("đi vào hôm 20 tháng 12 ngày chủ nhật", NGAY_CHUA_RO),  # "20 tháng 12 ngày" mơ hồ ⇒ không lấy "chủ nhật" còn lại
    ("đổi ngày đi sang 20/12 ngày đẹp", D(2026, 12, 20)), ("MAI ĐI LUÔN", D(2026, 11, 16)),
    ("đi ngày 3/12 giờ nào cũng được", NGAY_CHUA_RO),  # giới hạn đã nhận: tử < mẫu + "giờ" ⇒ coi như phân số, hỏi lại (an toàn)
]


@pytest.mark.parametrize("cau,mong", CA_NGAY)
def test_date_is_read_from_user_words_or_not_guessed(cau, mong):
    assert ngay_tu_cau(cau, HOM) == mong


def test_date_limits_same_as_form():
    assert sl.ngay_di_moi("đi 20/12", HOM) == {"ngay": D(2026, 12, 20)}
    assert sl.ngay_di_moi("đi 14/11/2026", HOM) == {"ma": "ngay_ngoai_han", "diem": "14/11"}  # đã qua
    assert sl.ngay_di_moi("đi 14/11", HOM) == {"ma": "ngay_ngoai_han", "diem": "14/11/2027"}  # lần tới > 180 ngày
    assert sl.ngay_di_moi("đi 14/5", HOM)["ngay"] == D(2027, 5, 14) and sl.ngay_di_moi("đi 15/5", HOM)["ma"] == "ngay_ngoai_han"  # đúng mốc +180
    assert sl.ngay_di_moi("dời 2 hôm", HOM) == {"ma": "ngay_chua_ro", "diem": None}


def _vt_toi(k):
    return sl._vi_tri(k), {j for ng in k["ngay"] for j in ng["buoi"]["toi"]}


@pytest.fixture(scope="module")
def khung_3840():
    st = [()] + [(s,) for s in v2.LOAI_DIEM_THU_TU] + list(itertools.combinations(v2.LOAI_DIEM_THU_TU, 2))
    ngay = (None, D(2027, 4, 7), D(2026, 11, 21), D(2026, 11, 13))  # như mô phỏng 3.840 của bản 2
    kq = {key: v2.xep_v2(B, v2.ThamSoV2(*key[:4], so_thich=key[4]), ngay_bat_dau=key[5])
          for key in itertools.product(range(1, 6), (0, 1), (False, True), ("nhe_nhang", "can_bang", "kham_pha"), st, ngay)}
    assert len(kq) == 3840
    return kq


def test_change_start_date_keeps_rules_and_reports_what_moved(khung_3840):
    """Luôn-b. Ngày mới: một thứ Hai (thứ nhiều điểm đóng cửa), một thứ Bảy có mưa lớn ngày 2 (dữ liệu mưa nhỏ tự đặt), một ngày mùa khác."""
    moi_ds = [({"ngay": D(2026, 11, 23), "co_du_bao": False}), ({"ngay": D(2026, 11, 28), "mua": {"2026-11-29": 90}, "co_du_bao": True}),
              ({"ngay": D(2027, 2, 10), "co_du_bao": False})]
    dem = {"giu": 0, "xep_lai": 0, "dang_dung": 0}
    for key, khung in khung_3840.items():
        cu = None if key[5] is None else key[5].isoformat()
        vt0, toi0 = _vt_toi(khung)
        bo = sorted(vt0)[0] if key[0] >= 2 and len(vt0) > 2 else None  # một điểm người dùng đã bỏ trước đó
        luu = sl.luu_tu_lich(khung, cu, None)
        if bo:
            luu = sl.ap(B, luu, [sl.HanhDong(loai="bo_diem", ten=B.theo_id[bo]["ten"])])["luu"]
            vt0, toi0 = _vt_toi(luu["khung"])
        for nm in moi_ds:
            kq = sl.ap(B, luu, [sl.HanhDong(loai="doi_ngay_di")], ngay_moi=dict(nm))
            assert not v2.kiem_khung_v2(B, kq["khung"]), (key, nm["ngay"])
            nd, dong = kq["ngay_di"], [d["cau"] for d in sl.thay_doi(B, kq)]
            assert nd is not None and not kq["khong_doi"] and kq["luu"]["ngay_di"] == nm["ngay"].isoformat() == nd["moi"] and nd["cu"] == cu
            assert kq["khung"]["ngay_thang"][0] == nm["ngay"].isoformat() and kq["luu"]["mua"] == nm.get("mua", {})
            vt1, toi1 = _vt_toi(kq["khung"])
            if bo:
                assert bo not in vt1 and bo not in toi1, (key, nm["ngay"])  # điểm đã bỏ không quay lại
            # số trong câu báo = đếm lại độc lập từ hai khung
            doi_cho = sorted(j for j in vt0 if j in vt1 and vt1[j] != vt0[j])
            ra, vao = sorted((set(vt0) - set(vt1)) | (toi0 - toi1)), sorted((set(vt1) - set(vt0)) | (toi1 - toi0))
            assert (nd["doi_cho"], nd["ra"], nd["vao"]) == (doi_cho, ra, vao)
            assert dong[0].startswith("Đã đổi ngày đi: ") and f"→ {nm['ngay'].day}/{nm['ngay'].month} (" in dong[0]
            if doi_cho or ra or vao:
                dem["xep_lai"] += 1
                assert dong[1].startswith("Lịch xếp lại theo ngày mới") and (not doi_cho or f"{len(doi_cho)} điểm đổi ngày hoặc buổi" in dong[1])
                assert all(B.theo_id[j]["ten"] in dong[1] for j in ra + vao)
            else:
                dem["giu"] += 1
                assert dong[1] == "Các điểm trong lịch giữ nguyên chỗ."
            assert (dong[-1] == "Ngày này chưa có dự báo thời tiết nên lịch chưa xét mưa.") == (not nm["co_du_bao"])
    assert dem["giu"] > 0 and dem["xep_lai"] > 0, dem


def test_start_date_reasons_and_schema():
    k = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), ngay_bat_dau=D(2026, 11, 21))
    luu = sl.luu_tu_lich(k, "2026-11-21", None)

    def ma(nm):
        kq = sl.ap(B, luu, [sl.HanhDong(loai="doi_ngay_di")], ngay_moi=nm)
        assert kq["khung"] == luu["khung"] and kq["luu"]["ngay_di"] == "2026-11-21" and kq["ngay_di"] is None
        return [(x["ma_luat"], d["cau"]) for x, d in zip(kq["khong_doi"], sl.thay_doi(B, kq))]

    assert ma(None)[0][0] == "ngay_chua_ro"  # nơi gọi không đưa gói ngày ⇒ không đổi, không đoán
    assert ma(sl.ngay_di_moi("dời 2 hôm", HOM)) == [("ngay_chua_ro", sl.CAU_KHONG_DOI["ngay_chua_ro"])]
    assert ma(sl.ngay_di_moi("đi 14/11/2026", HOM))[0][1] == "Mình chỉ xếp được ngày đi từ hôm nay tới 180 ngày nữa nên chưa đổi sang 14/11."
    assert ma(sl.ngay_di_moi("đi 30/2", HOM))[0][0] == "ngay_khong_co"
    assert ma(sl.ngay_di_moi("đi thứ bảy", HOM)) == [("ngay_dang_dung", "Lịch đang đi từ ngày 21/11 rồi.")]
    with pytest.raises(ValueError):
        sl.HanhDong(loai="doi_ngay_di", ngay_di="2026-12-20")  # model không có trường nào để viết ngày
    # lịch chưa có ngày đi ⇒ đặt ngày: "chưa chọn → …"
    k0 = v2.xep_v2(B, v2.ThamSoV2(2))
    kq = sl.ap(B, sl.luu_tu_lich(k0, None, None), [sl.HanhDong(loai="doi_ngay_di")], ngay_moi={"ngay": D(2026, 12, 20), "co_du_bao": False})
    assert sl.thay_doi(B, kq)[0]["cau"] == "Đã đổi ngày đi: chưa chọn → 20/12 (Chủ nhật)."
