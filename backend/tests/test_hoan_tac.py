"""Bản thử công tắc `sua_lich_hoan_tac` — nút "Hoàn tác lần sửa lịch vừa rồi": cuộc giữ MỘT bản lịch trước lần sửa cuối (RAM), bấm ⇒ lịch về đúng bản đó;
chỉ một bước, chỉ khi lịch chưa đổi thêm. Không gọi model."""
import copy
import dataclasses
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.conversations import ConversationStore, dau_lich
from api.routes import chat as r
from api.routes.hoan_tac import CAU_KHONG_DUOC, router
from api.routes.xuat import lich_tu_luu
from llm import lich_trinh_v2 as lt2
from llm import sua_lich_v2 as s
from test_sua_lich_v2 import B, V2, _lich

MO = dataclasses.replace(V2, sua_lich_v2=True, sua_lich_hoan_tac=True)
TAT = dataclasses.replace(V2, sua_lich_v2=True)


def _bo(luu, thu=0):
    """Lệnh "bỏ <điểm thứ `thu` của lịch>" áp bằng code ⇒ (bản lưu mới, dòng "đã làm" do code viết)."""
    ten = B.theo_id[lt2.diem_v2(luu["khung"])[thu]]["ten"]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=ten)])
    assert kq["da_ap"], ten
    return kq["luu"], tuple(d["cau"] for d in s.thay_doi(B, kq) if d["duoc"])


def _kho():
    kho = ConversationStore(len)
    return kho, kho.ensure(None)


def test_kho_giu_mot_ban_truoc_va_chi_hoan_tac_khi_lich_chua_doi_them():
    _, a = _lich()
    b, dong_b = _bo(a)
    c, dong_c = _bo(b)
    kho, cid = _kho()
    kho.luu_lich(cid, a)
    assert kho.hoan_tac(cid, dau_lich(a)) is None                      # lịch do biểu mẫu xếp: không có gì để hoàn tác
    kho.luu_lich(cid, b, truoc=a, dong=dong_b)
    assert kho.hoan_tac(cid, "sai-ma") is None and kho.lay_lich(cid) == b
    kho.luu_lich(cid, b)                                               # ghi lại CÙNG khung (lượt chỉ thêm câu an toàn) ⇒ vẫn hoàn tác được
    assert kho.hoan_tac(cid, dau_lich(b)) == (a, dong_b) and kho.lay_lich(cid) == a
    assert kho.hoan_tac(cid, dau_lich(b)) is None and kho.hoan_tac(cid, dau_lich(a)) is None   # chỉ MỘT bước
    # hai lần sửa nối nhau: nút của lần sửa cũ không còn dùng được; nút của lần mới trả về bản ngay trước nó
    kho.luu_lich(cid, b, truoc=a, dong=dong_b)
    kho.luu_lich(cid, c, truoc=b, dong=dong_c)
    assert kho.hoan_tac(cid, dau_lich(b)) is None and kho.lay_lich(cid) == c
    assert kho.hoan_tac(cid, dau_lich(c)) == (b, dong_c) and kho.lay_lich(cid) == b
    # sửa rồi XẾP LỊCH MỚI bằng biểu mẫu (khung khác, không có bản trước) ⇒ hết hoàn tác
    kho.luu_lich(cid, c, truoc=b, dong=dong_c)
    _, moi = _lich(n=2)
    kho.luu_lich(cid, moi)
    assert kho.hoan_tac(cid, dau_lich(c)) is None and kho.hoan_tac(cid, dau_lich(moi)) is None and kho.lay_lich(cid) == moi


def test_cuoc_het_han_thi_khong_hoan_tac():
    gio = [0.0]
    kho = ConversationStore(len, ttl=10, clock=lambda: gio[0])
    cid = kho.ensure(None)
    _, a = _lich()
    b, dong = _bo(a)
    kho.luu_lich(cid, b, truoc=a, dong=dong)
    gio[0] = 11
    assert kho.hoan_tac(cid, dau_lich(b)) is None


def _trace_sua(a, b, dong, flags):
    """Lượt sửa đã xong như `len_ke_hoach.chuan_bi` để lại: thẻ mang `thay_doi` và (công tắc bật) nút hoàn tác."""
    thay_doi = [{"cau": c, "duoc": True} for c in dong]
    nut = s.nut_hoan_tac(b["khung"], b["ngay_di"], thay_doi) if flags.sua_lich_hoan_tac else None
    lich = {**lt2.dung_lich(B, b["khung"], {}), "thay_doi": thay_doi, **({"hoan_tac": nut} if nut else {})}
    return SimpleNamespace(lich_luu=a, lich=None, notice=None, weather_note=None,
                           lich_v2={"lich": lich, "cau": {}, "loi_khung": [], "khung": b["khung"], "ngay_di": b["ngay_di"], "mua": None, "loai": []})


def test_luot_sua_doi_duoc_lich_thi_the_co_nut_va_kho_giu_ban_truoc():
    _, a = _lich()
    b, dong = _bo(a)
    nut = s.nut_hoan_tac(b["khung"], b["ngay_di"], [{"cau": c, "duoc": True} for c in dong])
    assert nut == {"nhan": s.NHAN_HOAN_TAC, "ma": dau_lich(b)} and len(nut["ma"]) == 12
    assert s.nut_hoan_tac(b["khung"], b["ngay_di"], [{"cau": "Không đổi được: X không có trong lịch.", "duoc": False}]) is None   # lượt không đổi được gì
    kho, cid = _kho()
    kho.luu_lich(cid, a)
    r.luu_lich_cua_luot(kho, cid, _trace_sua(a, b, dong, MO), MO)
    assert kho.lay_lich(cid)["khung"] == b["khung"] and kho.hoan_tac(cid, nut["ma"]) == (a, dong)   # mã của nút khớp đúng bản lưu route vừa ghi
    kho.luu_lich(cid, a)
    r.luu_lich_cua_luot(kho, cid, _trace_sua(a, b, dong, TAT), TAT)                                  # công tắc tắt ⇒ không giữ bản trước
    assert kho.hoan_tac(cid, nut["ma"]) is None


def _app(flags):
    app = FastAPI()
    app.include_router(router)
    app.state.assistant_flags = flags
    app.state.conversations = ConversationStore(len, keep_answers=False, chi_dap_lien_truoc=True)  # như `api/app.py` dựng
    return app


def test_duong_hoan_tac_tra_lich_ve_dung_ban_truoc_roi_tu_choi_lan_bam_lai():
    _, a = _lich()
    b, dong = _bo(a)
    app = _app(MO)
    kho = app.state.conversations
    cid = kho.ensure(None)
    kho.luu_lich(cid, copy.deepcopy(a))
    kho.luu_lich(cid, b, truoc=copy.deepcopy(a), dong=dong)
    with TestClient(app) as client:
        client.cookies.set(r.CONVERSATION_COOKIE, cid)
        sai = client.post("/api/lich/hoan_tac", json={"ma": "0" * 12})
        assert sai.status_code == 409 and sai.json()["error"] == {"code": "khong_hoan_tac_duoc", "message": CAU_KHONG_DUOC} and kho.lay_lich(cid) == b
        ra = client.post("/api/lich/hoan_tac", json={"ma": dau_lich(b)})
        assert ra.status_code == 200
        du = ra.json()
        lich_truoc, cau_truoc = lich_tu_luu(a, MO)
        # thẻ trả về là đúng thẻ của lịch trước lần sửa — cả quán ăn, ghi chú, giờ (cùng hàm dựng với sổ tay / file tải)
        assert du["trang_thai"] == "da_hoan_tac" and du["lich"] == lich_truoc and du["cau_muc"] == cau_truoc
        assert "hoan_tac" not in du["lich"] and "thay_doi" not in du["lich"]                # lịch trở lại không mang nút nào ⇒ chỉ một bước
        assert du["cau"].startswith("Đã hoàn tác") and all(c in du["cau"] for c in dong)    # nói rõ đã trả lại gì, bằng dòng do code viết
        assert kho.lay_lich(cid) == a
        assert kho.history(cid)[-1][0] == "Hoàn tác lần sửa lịch vừa rồi" and "hoàn tác" in kho.history(cid)[-1][1]   # lượt kế biết lịch đã trở lại
        assert client.post("/api/lich/hoan_tac", json={"ma": dau_lich(b)}).status_code == 409                     # bấm lại nút cũ
    with TestClient(_app(TAT)) as client:
        assert client.post("/api/lich/hoan_tac", json={"ma": dau_lich(b)}).status_code == 404                     # công tắc tắt
