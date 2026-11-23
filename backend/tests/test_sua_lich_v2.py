"""Sửa lịch bằng lời trên lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-sua-lich-v2-plan.md`) — phần code (0 USD): bộ xếp giữ chỗ / loại điểm,
áp hành động, khối "Đã đổi / Không đổi được", từ dò câu sửa, trạng thái lưu. Phép thử mọi tổ hợp ở `data/len_ke_hoach_v2_2026-11-13/tools/do_sua_lich_v2.py`."""
import dataclasses
import datetime as dt

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_cong_dot_1 import flags_from

V2 = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True)
B = V2.bang_lich_v2


def _lich(n=3, kieu="can_bang", so_thich=("di_tich",), ngay=None, bang=B):
    k = v2.xep_v2(bang, v2.ThamSoV2(n, kieu_di=kieu, so_thich=so_thich), ngay_bat_dau=ngay)
    return k, s.luu_tu_lich(k, None if ngay is None else ngay.isoformat(), None)


def _bang_toi_hai_buoi():
    """Bảng điểm từ bản 13: nơi vừa có ban ngày vừa có buổi tối đứng gần cuối thứ tự chọn buổi tối (`thu_tu_toi`) nên lịch thật hiếm khi dùng nó làm
    hoạt động tối. Các ca "nơi đang là hoạt động tối bị kéo sang ban ngày" cần lịch CÓ tình huống đó ⇒ đưa các nơi ấy lên đầu thứ tự chọn."""
    hai = tuple(d["id"] for d in B.diem if "toi" in d["buoi"] and set(d["buoi"]) - {"toi"})
    return dataclasses.replace(B, thu_tu_toi=hai + tuple(i for i in B.thu_tu_toi if i not in hai))


def test_default_scheduler_unchanged_and_keep_exclude_work():
    k, _ = _lich()
    assert v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), giu=None, loai=frozenset()) == k
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    k2 = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), giu={j: v for j, v in vt.items() if j != x}, loai=frozenset({x}))
    tat = {j for ng in k2["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    assert x not in tat and all(s._vi_tri(k2)[j] == v for j, v in vt.items() if j != x) and v2.kiem_khung_v2(B, k2) == []


def test_remove_replace_move_and_card():
    k, luu = _lich()
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[x]["ten"])])
    assert [(a["loai"], a["diem"]) for a in kq["da_ap"]] == [("bo_diem", x)] and x in kq["luu"]["loai"] and v2.kiem_khung_v2(B, kq["khung"]) == []
    # (C 17/11) bộ xếp lấp chỗ trống ⇒ điểm lấp nằm trong mục đã áp và trong câu báo
    moi_vao = {j for ng in kq["khung"]["ngay"] for b in v2.BUOI for j in ng["buoi"][b]} - {j for ng in k["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    assert {x2["diem"] for x2 in kq["da_ap"][0].get("lap", ())} == moi_vao
    cau = s.thay_doi(B, kq)[0]["cau"]
    assert cau.startswith(f"Đã bỏ {B.theo_id[x]['ten']}") and all(B.theo_id[j]["ten"] in cau for j in moi_vao)
    assert cau.endswith("vào chỗ trống.") if moi_vao else cau == f"Đã bỏ {B.theo_id[x]['ten']}."
    the = s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten=x)])  # không nói thay bằng gì ⇒ thẻ, khung không đổi
    assert the["the"]["cu"] == x and the["khung"] == k and the["the"]["lua_chon"][-1]["gia_tri"] == "bo"
    moi = the["the"]["lua_chon"][0]["gia_tri"]
    bam = s.ap(B, luu, [], sua_chon={"cu": x, "moi": moi})  # bấm nút ⇒ đúng điểm đã chọn vào đúng chỗ cũ
    assert s._vi_tri(bam["khung"])[moi] == vt[x] and x in bam["luu"]["loai"]
    dich = "chieu" if vt[x][1] == "sang" else "sang"
    dd = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=x, buoi=dich)])
    assert (dd["da_ap"] and s._vi_tri(dd["khung"])[x][1] == dich) or dd["khong_doi"]


def test_unknown_names_and_limits_are_reported_not_guessed():
    k, luu = _lich()
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten="Tháp Eiffel"), s.HanhDong(loai="them_diem", ten="x"), s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert kq["khong_doi"][0]["ma_luat"] == "ngoai_bang" and kq["chua_lam"] == ["doi_so_ngay"] and kq["khung"] == k
    dong = s.thay_doi(B, kq)
    assert all(not d["duoc"] for d in dong) and dong[-1]["cau"].startswith("Chưa làm")


def test_change_days_keeps_points_that_still_fit():
    k, luu = _lich(n=3)
    kq = s.ap(B, luu, [s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert len(kq["khung"]["ngay"]) == 2 and kq["doi_truong"] == [("so_ngay", 3, 2)]
    giu = {j: v for j, v in s._vi_tri(k).items() if v[0] <= 2}
    assert all(s._vi_tri(kq["khung"]).get(j) == v for j, v in giu.items()) or v2.kiem_khung_v2(B, kq["khung"]) == []


def test_intent_message_and_name_matching():
    k, luu = _lich(n=1)
    tin = s.tin_nhan_hieu(B, luu, "  bỏ điểm đầu  ")
    assert tin.endswith("Câu người dùng: bỏ điểm đầu") and "Ngày 1" in tin
    assert s.khop_ten(B, "Đại Nội Huế") == "dai_noi" and s.khop_ten(B, "đại nội") == "dai_noi" and s.khop_ten(B, "Đại") is None
    assert s.khop_ten(B, "Quốc Học") == "quoc_hoc" and s.khop_ten(B, "Lăng") is None  # tên ngắn chỉ nhận khi nằm trong đúng một điểm
    assert "Điểm khác có thể thêm" in tin


def test_flag_needs_v2():
    import pytest
    with pytest.raises(ValueError):
        AssistantFlags(sua_lich_v2=True)


def test_card_turn_applies_nothing_else_and_lists_the_rest_as_not_done():
    """Review E M-1: lượt có "thay" không nói điểm ⇒ chỉ thẻ chọn; hành động khác (trước hay sau) vào "Chưa làm", khung không đổi, không báo "Đã"."""
    k, luu = _lich()
    a, b = sorted(s._vi_tri(k))[:2]
    for thu_tu in ([s.HanhDong(loai="bo_diem", ten=a), s.HanhDong(loai="thay_diem", ten=b)],
                   [s.HanhDong(loai="thay_diem", ten=b), s.HanhDong(loai="bo_diem", ten=a)]):
        kq = s.ap(B, luu, thu_tu)
        assert kq["the"]["cu"] == b and kq["da_ap"] == [] and kq["chua_lam"] == ["bo_diem"] and kq["khung"] == k
        assert not any(d["duoc"] for d in s.thay_doi(B, kq)) and any(d["cau"].startswith("Chưa làm") for d in s.thay_doi(B, kq))


def test_parallel_normal_path_waits_for_intent_before_web_and_emergency_wins(monkeypatch):
    """Review E m-1 / B-1 trên đường song song (`assistant._sua_song_song`): đường thường chạy ngay nhưng tra web CHỜ kết quả hiểu ý — lượt sửa
    ⇒ không gọi tra web (chữ người dùng không ra Serper); lượt thường ⇒ có; định tuyến của đường thường thấy khẩn cấp ⇒ không thành lượt sửa."""
    import asyncio
    import dataclasses
    from llm import assistant as a, len_ke_hoach as lkh
    from llm.full_corpus_prompt import MAY_HAVE_CHANGED_NOTICE
    from retrieval.full_corpus_context import PackedSource
    goi_web, luot = [], []

    def lam(hieu_ra, khan_cap=False, the_chon=False):
        async def core(query, rs, cb, gen, tr, flags, recorder, tim_web):
            tr.routing_ms, tr.emergency_by = 1.0, ("router" if khan_cap else None)
            tr.vet["tim"] = [1]  # đường thường (trace phụ) ghi phần sổ vết của nó
            yield "status", {"stage": "routing"}
            if tim_web is not None:
                await tim_web(query)
            yield "delta", "trả lời thường"

        async def hieu(query, gen, tr, flags):
            await asyncio.sleep(0.05)
            tr.vet["sua"] = {"model_ra": []}  # lần hiểu ý ghi sổ vết trên trace CHÍNH
            return hieu_ra

        async def sua(query, rs, cb, gen, tr, flags, kq):
            tr.cited = (PackedSource(1, "t", (), ("e",), "travel/places/x.md"),)  # lịch sau sửa vẫn trích bài điểm đến
            yield "lich_khung", {"sua": True}

        async def web(cau):
            goi_web.append(cau)

        monkeypatch.setattr(a, "_answer_core", core)
        monkeypatch.setattr(lkh, "hieu_va_ap", hieu)
        monkeypatch.setattr(lkh, "stream_sua", sua)
        tr = a.AnswerTrace(); tr.lich_luu = {"x": 1}
        tr.sua_chon = {"cu": "a", "moi": "b"} if the_chon else None
        luot.append(tr)
        fl = dataclasses.replace(V2, router=True, may_have_changed_notice=True)

        async def chay():
            return [e async for e in a._sua_song_song("q", None, None, object(), tr, fl, None, web)]
        return asyncio.run(chay())

    ev = lam({"the": None})  # lượt sửa
    assert ev[-1][0] == "lich_khung" and goi_web == []
    assert luot[-1].notice == MAY_HAVE_CHANGED_NOTICE  # review tích hợp 18/11 #5: lượt sửa giữ dòng "có thể đã thay đổi" như lượt biểu mẫu
    lam({"the": None}, the_chon=True)  # lượt bấm nút thẻ chọn: cùng dòng đó
    assert luot[-1].notice == MAY_HAVE_CHANGED_NOTICE
    ev = lam(None)  # câu thường
    assert ("delta", "trả lời thường") in ev and goi_web == ["q"]
    assert set(luot[-1].vet) == {"sua", "tim"}  # review tích hợp 18/11 #8: sổ vết của câu thường trong cuộc có lịch không mất phần hiểu ý
    goi_web.clear()
    ev = lam({"the": None}, khan_cap=True)  # câu trộn khẩn cấp
    assert ("delta", "trả lời thường") in ev and not any(e[0] == "lich_khung" for e in ev)


def test_param_change_that_changes_nothing_is_reported_not_silent():
    # trước: `doi_tham_so` rỗng / trùng giá trị đang dùng ⇒ lượt sửa không có dòng nào
    _, luu = _lich(kieu="nhe_nhang")
    rong = s.ap(B, luu, [s.HanhDong(loai="doi_tham_so")])
    assert rong["khong_doi"] == [{"diem": "đổi kiểu lịch", "ma_luat": "tham_so_chua_ro"}] and rong["khung"] == luu["khung"]
    assert s.thay_doi(B, rong) == [{"cau": "Mình chưa rõ bạn muốn đổi kiểu lịch thành gì — bạn nói cụ thể hơn nhé.", "duoc": False}]
    trung = s.ap(B, luu, [s.HanhDong(loai="doi_tham_so", kieu_di="nhe_nhang", tre_em=0), s.HanhDong(loai="doi_so_ngay", so_ngay=3)])
    assert [d["cau"] for d in s.thay_doi(B, trung)] == ["Lịch đang đúng như vậy rồi (kiểu đi: nhẹ nhàng; số trẻ em: 0 trẻ em).",
                                                        "Lịch đang đúng như vậy rồi (số ngày: 3 ngày)."]
    assert trung["da_ap"] == [] and trung["khung"] == luu["khung"]


def test_param_change_says_whether_the_plan_was_rearranged():
    # "Đã đổi số trẻ em" một mình không cho biết lịch có xếp lại không; câu báo lấy từ hiệu hai khung (tính lại độc lập ở đây)
    def dat(k):
        return {(j, ng["ngay"], b) for ng in k["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    k, luu = _lich(kieu="can_bang", so_thich=("thien_nhien",))
    kq = s.ap(B, luu, [s.HanhDong(loai="doi_tham_so", tre_em=1)])
    cu, moi = {j for j, *_ in dat(k)}, {j for j, *_ in dat(kq["khung"])}
    assert cu - moi and dat(k) != dat(kq["khung"])  # ca này lịch THẬT sự đổi (nhóm có trẻ em không xếp buổi tối)
    cau = [d["cau"] for d in s.thay_doi(B, kq)]
    assert cau[0] == "Đã đổi số trẻ em: 0 trẻ em → 1 trẻ em." and cau[1].startswith("Lịch xếp lại theo lựa chọn mới: ") and len(cau) == 2
    assert all(B.theo_id[j]["ten"] in cau[1] for j in (cu - moi) | (moi - cu))
    assert sorted(kq["xep_lai"]["ra"]) == sorted(cu - moi) and sorted(kq["xep_lai"]["vao"]) == sorted(moi - cu)
    # review B M-1: điểm dời giữa ban ngày ↔ buổi tối là "đổi ngày hoặc buổi", không được vừa "bớt" vừa "thêm" — quét mọi lượt đổi một tham số
    n_doi_toi = 0
    for n, kieu, st in [(n, kieu, st) for n in (2, 3, 5) for kieu in ("nhe_nhang", "can_bang", "kham_pha") for st in ((), ("am_thuc",), ("di_tich",))]:
        k0, luu0 = _lich(n, kieu, st)
        for hd in ({"tre_em": 1}, {"kieu_di": "nhe_nhang"}, {"kieu_di": "kham_pha"}, {"so_thich": ["thien_nhien"]}, {"so_thich": ["am_thuc"]}):
            x = s.ap(B, luu0, [s.HanhDong(loai="doi_tham_so", **hd)])["xep_lai"]
            if x is None:
                continue
            assert not set(x["ra"]) & set(x["vao"]) and not set(x["doi_cho"]) & (set(x["ra"]) | set(x["vao"]))
            toi0 = {j for ng in k0["ngay"] for j in ng["buoi"]["toi"]}
            n_doi_toi += bool(set(x["doi_cho"]) & toi0)
    assert n_doi_toi  # đối chứng: bộ quét có chạm ca điểm buổi tối đổi chỗ
    # nhiều hơn 6 tên ⇒ chỉ nêu số điểm
    dai = {"da_ap": [], "doi_truong": [], "khong_doi": [], "chua_lam": [], "xep_lai": {"doi_cho": [], "ra": sorted(cu)[:5], "vao": sorted(moi)[:2]}}
    assert [d["cau"] for d in s.thay_doi(B, dai)] == ["Lịch xếp lại theo lựa chọn mới: bớt 5 điểm; thêm 2 điểm."]
    # đổi mà không điểm nào dời (sở thích đang lọc đúng các điểm đã có) ⇒ nói "giữ nguyên chỗ"
    giu = {"da_ap": [{"loai": "doi_tham_so"}], "doi_truong": [("tre_em", 1, 2)], "khong_doi": [], "chua_lam": [],
           "xep_lai": {"doi_cho": [], "ra": [], "vao": []}}
    assert [d["cau"] for d in s.thay_doi(B, giu)] == ["Đã đổi số trẻ em: 1 trẻ em → 2 trẻ em.", "Các điểm trong lịch giữ nguyên chỗ."]
    # đổi số ngày: không thêm dòng xếp lại (dòng "số ngày" đã tự nói)
    ngay = s.ap(B, luu, [s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert ngay["xep_lai"] is None and [d["cau"] for d in s.thay_doi(B, ngay)] == ["Đã đổi số ngày: 3 ngày → 2 ngày."]



def test_every_new_stop_after_removal_is_named_in_the_note():  # (C 17/11) tự thử 16/11: "Đã bỏ X." mà lịch có thêm điểm khác (910 / 960 khung)
    for n, kieu, st in ((2, "can_bang", ("am_thuc",)), (3, "kham_pha", ("di_tich",)), (1, "nhe_nhang", ())):
        k, luu = _lich(n, kieu, st)
        truoc = {j for ng in k["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
        for x in sorted(truoc):
            kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[x]["ten"])])
            if not kq["da_ap"]:
                continue
            moi = {j for ng in kq["khung"]["ngay"] for b in v2.BUOI for j in ng["buoi"][b]} - truoc
            bao = " ".join(d["cau"] for d in s.thay_doi(B, kq))
            assert all(B.theo_id[j]["ten"] in bao for j in moi), (x, moi, bao)


def test_move_that_leaves_the_point_where_it_was_is_not_reported_as_moved():
    # soát khác hãng 20/11: model hiểu một câu thành hai lần dời về cùng một (ngày, buổi) ⇒ hai lần đổi chỗ ngược nhau, lịch y nguyên mà báo "Đã dời…"
    k, luu = _lich()
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    kq = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=x, ngay=vt[x][0], buoi=vt[x][1])])  # dời về đúng chỗ đang đứng
    assert kq["da_ap"] == [] and kq["khung"] == k and [d["ma_luat"] for d in kq["khong_doi"]] == ["van_cho_cu"]
    assert [d["duoc"] for d in s.thay_doi(B, kq)] == [False]
    for y in vt:  # mọi điểm: tự dời về chỗ đang đứng ⇒ khung trả về đúng bản đã lưu (cả thứ tự trong buổi)
        tu = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=y, ngay=vt[y][0], buoi=vt[y][1])])
        assert tu["da_ap"] == [] and tu["khung"] == k and tu["luu"]["khung"] == k
    dich = "chieu" if vt[x][1] == "sang" else "sang"
    roi = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=x, buoi=dich), s.HanhDong(loai="bo_diem", ten=x)])  # dời rồi bỏ chính điểm đó: không văng
    assert x not in s._vi_tri(roi["khung"]) and not any(d["ma_luat"] == "van_cho_cu" for d in roi["khong_doi"])
    cap = [(a, b) for a in sorted(vt) for b in sorted(vt) if a != b and vt[a] != vt[b] and sum(v == vt[b] for v in vt.values()) == 1
           and vt[b][1] in B.theo_id[a]["buoi"] and vt[a][1] in B.theo_id[b]["buoi"]]
    thay = 0
    for a, b in cap:
        dich = {"ngay": vt[b][0], "buoi": vt[b][1]}
        mot = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=a, **dich)])
        if not mot["da_ap"] or s._vi_tri(mot["khung"]).get(b) != vt[a]:
            continue  # lần dời đầu không ra đổi chỗ hai điểm ⇒ không phải ca này
        thay += 1
        assert s._vi_tri(mot["khung"])[a] == vt[b] and "Đã dời" in s.thay_doi(B, mot)[0]["cau"]  # ca ngược: dời thật vẫn báo "Đã dời"
        hai = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=a, **dich), s.HanhDong(loai="doi_buoi", ten=b, **dich)])
        if hai["khung"] == k:
            assert hai["da_ap"] == [] and not any(d["duoc"] for d in s.thay_doi(B, hai))
    assert thay  # bảng điểm thật phải có ít nhất một cặp đổi chỗ được, không thì test này không kiểm gì


def test_refused_move_says_one_reason_and_lists_slots_that_work():
    # đếm 20/11: dời MỘT điểm bị từ chối 36 / 40 lần trên lịch này, mọi ca cùng một câu chung, không gợi ý ⇒ nay: một lý do + các chỗ dời ĐƯỢC
    k, luu = _lich()
    vt = s._vi_tri(k)
    cho = sorted({(ng["ngay"], b) for ng in k["ngay"] for b in v2.BUOI_NGAY})
    ly_do, co_goi_y, khong_goi_y = set(), 0, 0
    for a in sorted(vt):
        duoc = {c for c in cho if c != vt[a] and s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=a, ngay=c[0], buoi=c[1])])["da_ap"]}
        for c in cho:
            if c == vt[a] or c in duoc:
                continue
            kq = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=a, ngay=c[0], buoi=c[1])])
            (kd,), cau = kq["khong_doi"], s.thay_doi(B, kq)[0]["cau"]
            assert kq["khung"] == k and kd["ma_luat"] == "khong_hop_luat" and kd["dich"] == list(c)  # lịch giữ nguyên, mã cho bộ đo giữ nguyên
            assert {(g["ngay"], g["buoi"]) for g in kd["goi_y"]} == duoc  # gợi ý = ĐÚNG các chỗ lần dời thật nhận, không thừa không thiếu
            assert kd["ly_do"] in s.CAU_LY_DO and s.CAU_LY_DO[kd["ly_do"]] in cau and f"buổi {s.NHAN_BUOI[c[1]]} ngày {c[0]}" in cau
            for g in kd["goi_y"]:
                assert f"buổi {s.NHAN_BUOI[g['buoi']]} ngày {g['ngay']}" in cau.split("Dời được sang:")[1]
                if g["doi_voi"]:  # chỗ đích có đúng một điểm ⇒ câu nói rõ điểm sẽ đổi chỗ, và áp thật thì điểm đó về chỗ cũ của điểm được dời
                    lai = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=a, ngay=g["ngay"], buoi=g["buoi"])])
                    assert s._vi_tri(lai["khung"])[g["doi_voi"]] == vt[a] and f"(đổi chỗ với {B.theo_id[g['doi_voi']]['ten']})" in cau
            if not duoc:
                assert cau.endswith("chỉ đứng được ở chỗ hiện tại.") and "Dời được sang" not in cau
            ly_do.add(kd["ly_do"])
            co_goi_y, khong_goi_y = co_goi_y + bool(duoc), khong_goi_y + (not duoc)
    assert {"khu", "kin"} <= ly_do and co_goi_y and khong_goi_y  # bảng điểm thật phải có đủ hai lý do chính và cả hai kiểu câu, không thì test không kiểm gì
    # điểm chưa có trong lịch (dời = thêm) và "thêm điểm" giữ câu chung cũ
    ngoai = next(d["id"] for d in B.diem if d["id"] not in vt and d["id"] not in {j for ng in k["ngay"] for j in ng["buoi"]["toi"]})
    for loai in ("doi_buoi", "them_diem"):
        kq = s.ap(B, luu, [s.HanhDong(loai=loai, ten=ngoai, ngay=1, buoi="sang")])
        assert all("goi_y" not in d for d in kq["khong_doi"])


# ---------- 22/11: bỏ một hoạt động TỐI làm buổi tối của ngày khác đổi theo ⇒ dòng báo phải nói đủ (lượt trình duyệt 22/11: chỉ nói ngày cuối) ----------
def _toi(khung):
    return {ng["ngay"]: list(ng["buoi"]["toi"]) for ng in khung["ngay"]}


def test_removing_an_evening_activity_reports_every_evening_that_changed():
    k, luu = _lich(3, "can_bang", ())
    truoc = _toi(k)
    assert all(len(v) == 1 for v in truoc.values())  # lịch mẫu: mỗi tối một hoạt động
    x = truoc[1][0]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[x]["ten"])])
    sau = _toi(kq["khung"])
    assert sau[1] == truoc[2] and sau[2] == truoc[3] and sau[3][0] not in sum(truoc.values(), [])  # bộ xếp dồn các tối lên, ngày cuối nhận cái mới
    ten = lambda j: B.theo_id[j]["ten"]
    assert s.thay_doi(B, kq)[0]["cau"] == (f"Đã bỏ {ten(x)}. Buổi tối xếp lại: ngày 1 {ten(sau[1][0])}, ngày 2 {ten(sau[2][0])}, "
                                           f"ngày 3 {ten(sau[3][0])} (mới thêm).")
    # bỏ hoạt động tối của NGÀY CUỐI: không tối nào khác đổi ⇒ dòng báo cũ, y nguyên
    y = truoc[3][0]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=ten(y))])
    sau = _toi(kq["khung"])
    assert sau[1] == truoc[1] and sau[2] == truoc[2] and "toi_xep_lai" not in kq["da_ap"][0]
    assert s.thay_doi(B, kq)[0]["cau"] == f"Đã bỏ {ten(y)}, thêm {ten(sau[3][0])} (ngày 3, buổi tối) vào chỗ trống."


def test_every_removal_names_each_evening_that_moved_and_stays_as_before_otherwise():
    """Mọi lịch mẫu × bỏ từng điểm (ban ngày lẫn tối): tối của ngày nào khác trước mà không phải vì điểm mới lấp vào ⇒ câu báo phải có tên hoạt động tối
    mới của ngày đó; không tối nào bị chuyển ngày ⇒ câu báo đúng khuôn cũ."""
    co = khong = 0
    for n in (2, 3, 4):
        for kieu in ("nhe_nhang", "can_bang", "kham_pha"):
            for st in ((), ("di_tich",), ("am_thuc",)):
                k, luu = _lich(n, kieu, st)
                truoc = _toi(k)
                for j in [x for v in truoc.values() for x in v] + sorted(s._vi_tri(k)):
                    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[j]["ten"])])
                    if not kq["da_ap"]:
                        continue
                    sau, cau = _toi(kq["khung"]), s.thay_doi(B, kq)[0]["cau"]
                    moi = {x["diem"] for x in kq["da_ap"][0].get("lap", ())}
                    doi = [d for d in sau if sau[d] != truoc[d] and not (set(sau[d]) <= moi | set(truoc[d]))]
                    if doi:
                        co += 1
                        assert "Buổi tối xếp lại: " in cau and all(f"ngày {d} " in cau and B.theo_id[x]["ten"] in cau for d in doi for x in sau[d]), cau
                    else:
                        khong += 1
                        assert "Buổi tối xếp lại" not in cau and (cau.endswith("vào chỗ trống.") or cau == f"Đã bỏ {B.theo_id[j]['ten']}."), cau
    assert co > 0 and khong > 0


# ---------- soát khác hãng 22/11: K7 (báo giả ở lịch 5 ngày), G5 (thêm / dời làm buổi tối đổi mà không báo), K8a (thêm hoạt động tối không nói "tối") ----------
def test_five_day_schedule_with_a_repeated_evening_does_not_report_evenings_that_did_not_change():
    """Lịch 5 ngày lặp một hoạt động tối ở hai ngày; bảng tra ngược `mã ⇒ một ngày` từng bị ghi đè ⇒ mọi lệnh bỏ / thay báo "Buổi tối xếp lại" dù không tối
    nào đổi (kể cả so một lịch với chính nó)."""
    lap = thay = 0
    # Bảng điểm từ bản 13 có đủ hoạt động tối cho 5 ngày (thêm các dòng quán cà phê tối, cột `la_quan`, và hai mục tối `chi_muc_toi`) nên lịch thật không còn lặp; ca này cần lịch
    # CÓ lặp ⇒ xếp trên bảng đã bỏ các dòng đó.
    it = tuple(d for d in B.diem if not (d.get("la_quan") or d.get("chi_muc_toi")))  # bản 15 thêm hai mục tối nữa (`chi_muc_toi`) — cũng bỏ
    bang = dataclasses.replace(B, diem=it, theo_id={d["id"]: d for d in it}, thu_tu_toi=())
    for kieu in ("nhe_nhang", "can_bang", "kham_pha"):
        for st in ((), ("di_tich",), ("am_thuc",), ("thien_nhien",)):
            k = v2.xep_v2(bang, v2.ThamSoV2(5, kieu_di=kieu, so_thich=st))
            luu = s.luu_tu_lich(k, None, None)
            truoc = _toi(k)
            if len({j for v in truoc.values() for j in v}) == sum(len(v) for v in truoc.values()):
                continue  # lịch này không lặp hoạt động tối nào
            lap += 1
            assert s._toi_xep_lai(k, k) is None  # lịch so với chính nó ⇒ không tối nào đổi
            for j in sorted(s._vi_tri(k)):
                kq = s.ap(bang, luu, [s.HanhDong(loai="bo_diem", ten=bang.theo_id[j]["ten"])])
                if kq["da_ap"] and _toi(kq["khung"]) == truoc:
                    thay += 1
                    assert "Buổi tối xếp lại" not in s.thay_doi(bang, kq)[0]["cau"]
    assert lap > 0 and thay > 0  # bảng điểm thật phải có lịch lặp hoạt động tối, không thì test không kiểm gì


def test_adding_or_moving_an_evening_place_into_the_day_reports_the_evenings_that_moved():
    """Thêm / dời một nơi lịch đang dùng làm hoạt động TỐI sang ban ngày ⇒ bộ xếp chọn lại buổi tối; dòng báo từng chỉ nói "Đã thêm…" / "Đã dời…"."""
    bang = _bang_toi_hai_buoi()
    ten = lambda j: bang.theo_id[j]["ten"]
    co = 0
    for n in (3, 4, 5):
        k, luu = _lich(n, "can_bang", ("di_tich",), bang=bang)
        truoc = _toi(k)
        for x in sorted({j for v in truoc.values() for j in v if set(bang.theo_id[j]["buoi"]) - {"toi"}}):
            for loai in ("them_diem", "doi_buoi"):
                for ngay in range(1, n + 1):
                    for buoi in ("sang", "chieu"):
                        kq = s.ap(bang, luu, [s.HanhDong(loai=loai, ten=ten(x), ngay=ngay, buoi=buoi)], them_khong_the=True)
                        if not kq["da_ap"]:
                            continue
                        sau, cau = _toi(kq["khung"]), s.thay_doi(bang, kq)[0]["cau"]
                        cu = s._ngay_toi(k)
                        if any(j in cu and d not in cu[j] for d, v in sau.items() for j in v):  # một hoạt động tối đứng ở ngày nó chưa từng đứng
                            co += 1
                            assert " Buổi tối xếp lại: " in cau and all(f"ngày {d} " in cau and ten(j) in cau for d, v in sau.items() for j in v), cau
                        else:
                            assert "Buổi tối xếp lại" not in cau, cau
    assert co > 0


def test_adding_an_evening_only_activity_without_saying_evening_gets_the_evening_answer():
    """"Thêm Ca Huế trên sông Hương vào lịch" (không gõ chữ "tối") từng ra "đặt vào buổi nào cũng phạm luật xếp… không còn chỗ nào" — sai, kể cả khi hoạt động
    đó đang nằm ở buổi tối của lịch. Nơi CHỈ có buổi tối ⇒ đi nhánh buổi tối sẵn có: đang ở trong lịch ⇒ nói đang ở tối ngày nào; chưa ⇒ câu nói thật."""
    k, luu = _lich(2, "can_bang", ("di_tich",))
    chi_toi = [d["id"] for d in B.diem if set(d["buoi"]) == {"toi"}]
    dang_o = [j for v in _toi(k).values() for j in v if j in chi_toi]
    chua_co = [j for j in chi_toi if j not in dang_o]
    assert dang_o and chua_co  # bảng điểm thật phải có cả hai ca, không thì test không kiểm gì
    for j, ma in ((dang_o[0], "toi_dang_o"), (chua_co[0], "toi_chua_xep")):
        kq = s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=B.theo_id[j]["ten"])], them_khong_the=True)
        assert not kq["da_ap"] and [d["ma_luat"] for d in kq["khong_doi"]] == [ma], kq["khong_doi"]
        assert "phạm luật xếp" not in " ".join(d["cau"] for d in s.thay_doi(B, kq))


def test_replacing_a_daytime_stop_with_an_evening_place_reports_the_evenings_that_moved():
    """Thay một điểm ban ngày bằng nơi lịch đang dùng làm hoạt động TỐI (chợ, phố đi bộ…) ⇒ các buổi tối bị chọn lại; dòng báo phải nói."""
    bang = _bang_toi_hai_buoi()
    co = khong = 0
    ten = lambda j: bang.theo_id[j]["ten"]
    for n in (2, 3):
        for st in ((), ("di_tich",)):
            k, luu = _lich(n, "can_bang", st, bang=bang)
            truoc, vt = _toi(k), s._vi_tri(k)
            for y, (_, b) in vt.items():
                for x in [j for v in truoc.values() for j in v] + [j for j in bang.theo_id if j not in vt and b in bang.theo_id[j]["buoi"]][:6]:
                    kq = s.ap(bang, luu, [s.HanhDong(loai="thay_diem", ten=ten(y), ten_moi=ten(x))])
                    if not kq["da_ap"]:
                        continue
                    sau, cau = _toi(kq["khung"]), s.thay_doi(bang, kq)[0]["cau"]
                    dau = f"Đã thay {ten(y)} bằng {ten(x)}."
                    cu = {j: d for d, v in truoc.items() for j in v}
                    if any(cu.get(j, d) != d for d, v in sau.items() for j in v):
                        co += 1
                        assert cau.startswith(dau + " Buổi tối xếp lại: ") and all(f"ngày {d} " in cau and ten(j) in cau for d, v in sau.items() for j in v), cau
                    else:
                        khong += 1
                        assert cau == dau, cau
    assert co > 0 and khong > 0
