"""Cờ `sua_lich_buoi_toi` (21/11/2026) — 0 USD. Vì sao: lệnh "dời <điểm ban ngày> sang buổi tối" — khuôn hành động chỉ có sáng / chiều nên model không ghi
được điều người dùng nói: Sonnet để trống buổi ⇒ người dùng thấy "Chưa rõ ngày / buổi" (5 / 9 lượt thật), luna đổi thành "chiều" (2 / 9).
Cờ bật: khuôn + lời dặn nhận "toi"; CODE trả lời thật. File này kiểm phần code (bảng điểm thật, bộ xếp thật); model có điền "toi" hay không là lượt đo có
phí ghi ở report của nhánh."""
import pytest

from llm import full_corpus_prompt as p
from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from llm.generator_openai_full_corpus import SuaLichOutputCHT, SuaLichOutputToi
from test_sua_lich_v2 import B, _lich


def _ban_ngay_va_toi(k):
    """(một điểm CHỈ đi ban ngày đang ở trong lịch, một hoạt động đang ở buổi tối của lịch) — lấy từ bảng thật, không ghi cứng tên."""
    vt = s._vi_tri(k)
    ngay = next(j for j in sorted(vt) if "toi" not in B.theo_id[j]["buoi"])
    toi = next(j for ng in k["ngay"] for j in ng["buoi"]["toi"])
    return ngay, toi


def test_flag_defaults_off_and_needs_the_unsupported_action_flag():
    assert AssistantFlags().sua_lich_buoi_toi is False
    with pytest.raises(ValueError, match="sua_lich_buoi_toi needs"):
        AssistantFlags(sua_lich_buoi_toi=True)


def test_only_the_new_schema_and_prompt_know_the_evening_slot():
    """Cờ tắt ⇒ khuôn và lời dặn cũ không đổi (không có "toi"); bản mới chỉ khác đúng dòng `doi_buoi` và giá trị thêm của `buoi`."""
    assert '"toi"' not in SuaLichOutputCHT.model_json_schema().__repr__().replace("'", '"')
    assert '"toi"' in SuaLichOutputToi.model_json_schema().__repr__().replace("'", '"')
    assert "sang / chieu / toi" in p.SUA_LICH_LOI_DAN_TOI and "toi" not in p.SUA_LICH_LOI_DAN_CHT.split("- doi_buoi")[1].split("\n")[0]
    cu, moi = p.SUA_LICH_LOI_DAN_CHT.split("\n"), p.SUA_LICH_LOI_DAN_TOI.split("\n")
    assert len(cu) == len(moi) and [a for a, b in zip(cu, moi) if a != b] == [p._DOI_BUOI_CU.rstrip("\n")]
    with pytest.raises(Exception):
        s.HanhDongCHT(loai="doi_buoi", ten="x", buoi="toi")


def test_moving_a_daytime_place_to_the_evening_is_refused_with_the_real_reason_and_places_it_can_go():
    k, luu = _lich()
    x, _ = _ban_ngay_va_toi(k)
    ten, (ngay_cu, _) = B.theo_id[x]["ten"], s._vi_tri(k)[x]
    kq = s.ap(B, luu, [s.HanhDongToi(loai="doi_buoi", ten=ten, ngay=ngay_cu, buoi="toi")])
    assert kq["khung"] == k and not kq["da_ap"]  # lịch không đổi
    kd, = kq["khong_doi"]
    assert (kd["ma_luat"], kd["ly_do"], kd["dich"]) == ("khong_buoi_hop_le", "ban_ngay", [ngay_cu, "toi"])
    # gợi ý = ĐÚNG các chỗ một lần dời thật nhận (thử từng chỗ bằng hành động dời thường)
    duoc = {(n, b) for ng in k["ngay"] for n in [ng["ngay"]] for b in v2.BUOI_NGAY if (n, b) != s._vi_tri(k)[x]
            and s.ap(B, luu, [s.HanhDongCHT(loai="doi_buoi", ten=ten, ngay=n, buoi=b)])["da_ap"]}
    assert {(g["ngay"], g["buoi"]) for g in kd["goi_y"]} == duoc
    cau, = [d["cau"] for d in s.thay_doi(B, kq)]
    assert cau.startswith(f"{ten} chưa dời sang buổi tối ngày {ngay_cu} được vì đây là điểm tham quan ban ngày")
    assert ("Dời được sang: " in cau) if duoc else cau.endswith("chỉ đứng được ở chỗ hiện tại.")
    assert "Chưa rõ ngày" not in cau
    # không nói ngày ⇒ lấy ngày điểm đang đứng (như lần dời thường)
    kq2 = s.ap(B, luu, [s.HanhDongToi(loai="doi_buoi", ten=ten, buoi="toi")])
    assert kq2["khong_doi"][0]["dich"] == [ngay_cu, "toi"]


def test_evening_capable_place_and_add_to_evening_get_an_honest_sentence_and_the_plan_is_untouched():
    k, luu = _lich()
    x, t = _ban_ngay_va_toi(k)
    ngay_khac = next(ng["ngay"] for ng in k["ngay"] if t not in ng["buoi"]["toi"])
    kq = s.ap(B, luu, [s.HanhDongToi(loai="doi_buoi", ten=B.theo_id[t]["ten"], ngay=ngay_khac, buoi="toi")])  # hoạt động tối sang tối khác: chưa có phép xếp tay
    assert kq["khung"] == k and kq["khong_doi"] == [{"diem": B.theo_id[t]["ten"], "ma_luat": "toi_chua_xep"}]
    cau = s.thay_doi(B, kq)[0]["cau"]
    assert cau.startswith(f"Mình chưa đặt được {B.theo_id[t]['ten']} vào buổi tối theo ý bạn") and "lịch sẽ tự chọn một hoạt động khác" in cau and "xếp tay" not in cau
    # điểm ban ngày CHƯA có trong lịch, thêm hoặc dời vào buổi tối ⇒ câu nói rõ "buổi tối" + lý do (review 21/11: trước là "không đi được vào buổi đó")
    ngoai = next(d["id"] for d in B.diem if d["id"] not in s._vi_tri(k) and "toi" not in d["buoi"] and d["id"] not in {j for ng in k["ngay"] for j in ng["buoi"]["toi"]})
    for loai in ("them_diem", "doi_buoi"):
        kq = s.ap(B, luu, [s.HanhDongToi(loai=loai, ten=B.theo_id[ngoai]["ten"], ngay=1, buoi="toi")])
        assert kq["khung"] == k and kq["khong_doi"] == [{"diem": B.theo_id[ngoai]["ten"], "ma_luat": "ban_ngay_khong_toi"}], loai
        assert s.thay_doi(B, kq)[0]["cau"] == f"{B.theo_id[ngoai]['ten']} không xếp được vào buổi tối vì đây là điểm tham quan ban ngày, còn buổi tối lịch chỉ xếp hoạt động buổi tối."


def test_asking_for_the_evening_slot_a_place_already_has_says_so_without_advice_to_remove_it():
    """Review 21/11: "dời <hoạt động tối> sang tối ngày N" khi nó ĐANG ở tối ngày N ⇒ trước nhận lời khuyên "bỏ hoạt động tối đang có" (chính là nó)."""
    k, luu = _lich()
    _, t = _ban_ngay_va_toi(k)
    ngay = next(ng["ngay"] for ng in k["ngay"] if t in ng["buoi"]["toi"])
    for kw in ({"ngay": ngay}, {}):  # nói đúng ngày, hoặc không nói ngày
        kq = s.ap(B, luu, [s.HanhDongToi(loai="doi_buoi", ten=B.theo_id[t]["ten"], buoi="toi", **kw)])
        assert kq["khung"] == k and [d["cau"] for d in s.thay_doi(B, kq)] == [f"{B.theo_id[t]['ten']} đang ở buổi tối ngày {ngay} rồi."]


def test_replacing_an_evening_activity_no_longer_claims_it_is_not_in_the_plan():
    """Lỗi có sẵn (không cần cờ, khuôn cũ): "thay <hoạt động đang ở buổi tối> bằng …" ⇒ code báo "… không có trong lịch hiện tại" — SAI, nó đang ở buổi tối của
    lịch. Code chưa thay được hoạt động buổi tối ⇒ câu nói thật điều đó; lịch không đổi. Điểm thật sự không có trong lịch vẫn nhận câu cũ."""
    k, luu = _lich()
    _, t = _ban_ngay_va_toi(k)
    khac = next(d["ten"] for d in B.diem if "toi" in d["buoi"] and d["id"] != t and d["id"] not in {j for ng in k["ngay"] for j in ng["buoi"]["toi"]})
    for hd in (s.HanhDong(loai="thay_diem", ten=B.theo_id[t]["ten"], ten_moi=khac), s.HanhDong(loai="thay_diem", ten=B.theo_id[t]["ten"])):
        kq = s.ap(B, luu, [hd])
        cau, = [d["cau"] for d in s.thay_doi(B, kq)]
        assert kq["khung"] == k and not kq.get("the") and "không có trong lịch" not in cau
        assert cau.startswith("Mình chưa thay được hoạt động buổi tối theo ý bạn") and f"Bạn có thể bỏ {B.theo_id[t]['ten']}" in cau
    ngoai = next(d for d in B.diem if d["id"] not in s._vi_tri(k) and d["id"] not in {j for ng in k["ngay"] for j in ng["buoi"]["toi"]})
    kq = s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten=ngoai["ten"], ten_moi=khac)])
    assert s.thay_doi(B, kq)[0]["cau"] == f"{ngoai['ten']} không có trong lịch hiện tại."


def test_daytime_moves_behave_exactly_as_before_with_the_new_schema():
    """Bất biến: hành động sáng / chiều qua khuôn mới cho đúng kết quả như qua khuôn cũ (mọi điểm × mọi chỗ của một lịch 3 ngày)."""
    k, luu = _lich()
    for x in sorted(s._vi_tri(k)):
        for ng in k["ngay"]:
            for b in v2.BUOI_NGAY:
                kw = dict(loai="doi_buoi", ten=B.theo_id[x]["ten"], ngay=ng["ngay"], buoi=b)
                assert s.ap(B, luu, [s.HanhDongToi(**kw)]) == s.ap(B, luu, [s.HanhDongCHT(**kw)]), kw
