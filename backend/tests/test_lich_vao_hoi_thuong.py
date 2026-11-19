"""Cờ `lich_vao_hoi_thuong` (plan private `data/lich_da_luu_2026-11-19/PLAN.md` mục 4): cuộc đã có lịch lưu + lượt hỏi thường tuyến `tro_ly_hue` ⇒ code nối
MỘT nguồn "Lịch bạn đang có" (lịch + số giờ do code tính) vào ngữ cảnh. Phần hàm thuần: đáp số tính tay ghi trong test. Phần loại lượt (WORKFLOW §4 4c):
chạy qua `answer_turn_stream_parallel` với ĐÚNG các cờ đường đi đang chạy thật (định tuyến + chạy song song + tìm thêm + sửa lịch bản 2) — đường tìm thật
(Qdrant chỉ đọc), model thay bằng client trả lời theo kịch bản ⇒ **không** phải bằng chứng hành vi model, chỉ kiểm code đưa gì vào yêu cầu gửi model."""
import asyncio
import copy
import json

import pytest

from llm import assistant as a
from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream_parallel
from llm.full_corpus_prompt import OUT_OF_SCOPE_ANSWER, ROUTER_INSTRUCTIONS, SUA_LICH_LOI_DAN, SUA_LICH_LOI_DAN_CHT
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_cong_dot_1 import chu_gui, flags_from
from test_toc_do_song_song import Client, TimedResponses, _request_bytes, deps  # noqa: F401 (`deps`: fixture đường tìm thật)

# Cờ đường đi đặt RÕ trong test (không dựa vào `settings.yaml`): đúng bộ đang chạy thật khiến lượt hỏi thường đi qua HAI tầng trace phụ
DUONG_DI = dict(router=True, tim_them=True, song_song_tra_loi=True, lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True,
                sua_lich_chua_ho_tro=True, sua_lich_doi_cho_code=True, tra_web=False, thoi_tiet=False, bao_lu_cong_cu=False)
ON = flags_from(**DUONG_DI, lich_vao_hoi_thuong=True)
OFF = flags_from(**DUONG_DI, lich_vao_hoi_thuong=False)
B = ON.bang_lich_v2
QUERY = "Ngày 1 của lịch này đi hết mấy tiếng?"


def lich_2_ngay() -> dict:
    """Lịch mặc định của biểu mẫu (2 ngày, 2 người lớn, đi cân bằng) — đúng lịch của các kịch bản đã thấy lỗi."""
    khung = v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang", so_thich=(), nguoi_lon=2))
    return s.luu_tu_lich(khung, None, None)


# ---------- Hàm thuần ----------

def test_gio_doc_nguoc_dung_khuon_va_khong_doan():
    assert v2.doc_gio(v2.in_gio(480, 630)) == (480, 630)
    assert v2.doc_gio("8:00 - 10:30") is None and v2.doc_gio("10:30 – 8:00") is None and v2.doc_gio(None) is None and v2.doc_gio("sáng") is None
    assert [v2.in_thoi_luong(p) for p in (495, 300, 45)] == ["8 giờ 15 phút", "5 giờ", "45 phút"]


def test_dong_lich_mac_dinh_khop_dap_so_tinh_tay():
    """Đáp số tính tay trên lịch mặc định: ngày 1 = Đại Nội 8:00 – 10:30 + Đầm Chuồn 13:30 – 16:00 ⇒ đầu – cuối 8 giờ, tham quan 2,5 + 2,5 = 5 giờ;
    ngày 2 = bốn điểm 75 phút, 8:00 ⇒ 16:15 ⇒ đầu – cuối 8 giờ 15 phút, tham quan 5 giờ; cả lịch 6 điểm, 10 giờ; ngày dài nhất = ngày 2."""
    dong = v2.dong_lich_dang_co(B, lich_2_ngay())
    assert dong[0] == "Tham số của lịch: 2 ngày · 2 người lớn · đi cân bằng."
    assert dong[1] == "Ngày 1: Sáng (8:00 – 10:30) Đại Nội Huế; Chiều (13:30 – 16:00) Đầm Chuồn; Tối (18:00 – 23:00) Chợ Đông Ba."
    assert dong[2] == ("Ngày 1 — số do hệ thống tính: 2 điểm tham quan ban ngày; bắt đầu 8:00; kết thúc mục ban ngày cuối 16:00; "
                       "từ đầu tới cuối phần ban ngày 8 giờ; tổng thời lượng tham quan ban ngày 5 giờ (chưa gồm đi lại, ăn nghỉ); "
                       "buổi tối: Chợ Đông Ba 18:00 – 23:00.")
    assert "4 điểm tham quan ban ngày; bắt đầu 8:00; kết thúc mục ban ngày cuối 16:15; từ đầu tới cuối phần ban ngày 8 giờ 15 phút; " \
           "tổng thời lượng tham quan ban ngày 5 giờ" in dong[4]
    assert dong[5] == ("Cả lịch — số do hệ thống tính: 6 điểm tham quan ban ngày; 2 hoạt động buổi tối; tổng thời lượng tham quan ban ngày 10 giờ "
                       "(chưa gồm đi lại, ăn nghỉ); ngày dài nhất (từ đầu tới cuối phần ban ngày): Ngày 2 (8 giờ 15 phút).")
    assert dong[-1] == v2.DONG_TIEN_VE_CHUA_CO and len(dong) == 7


def test_gio_khong_doc_duoc_thi_khong_in_so_cua_ngay_do_va_khong_in_tong():
    luu = lich_2_ngay()
    luu["khung"]["gio"]["dai_noi"] = "buổi sáng"  # chuỗi lạ ⇒ không đoán
    dong = v2.dong_lich_dang_co(B, luu)
    assert dong[2] == "Ngày 1 — số do hệ thống tính: 2 điểm tham quan ban ngày; buổi tối: Chợ Đông Ba 18:00 – 23:00."
    assert "bắt đầu 8:00" in dong[4]  # ngày đọc được vẫn có số
    assert dong[5] == "Cả lịch — số do hệ thống tính: 6 điểm tham quan ban ngày; 2 hoạt động buổi tối."


def test_nguon_khong_mang_cau_ta_cua_model_va_theo_lich_da_sua():
    luu = lich_2_ngay()
    luu["cau"] = {"dai_noi": "CÂU TẢ DO MODEL VIẾT"}  # `luu_sau_luot` lưu câu tả đã kiểm — không được vào nguồn
    assert "CÂU TẢ" not in " ".join(v2.dong_lich_dang_co(B, luu))
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten="Đầm Chuồn")])  # lượt sửa: bỏ một điểm ⇒ lượt hỏi kế phải thấy lịch ĐÃ sửa
    sau = " ".join(v2.dong_lich_dang_co(B, kq["luu"]))
    assert "Đầm Chuồn" not in sau.split("Ngày 2:")[0] and "Đại Nội Huế" in sau


def test_co_can_sua_lich_v2_va_tim_them():
    with pytest.raises(ValueError, match="lich_vao_hoi_thuong"):
        AssistantFlags(lich_vao_hoi_thuong=True)
    assert ON.lan_tim_dau == "v0" and ON.router and ON.song_song_tra_loi  # điều kiện để `_answer_core` dựng trace phụ tầng hai


# ---------- Loại lượt: nguồn lịch CÓ / KHÔNG trong yêu cầu gửi model ----------

class KichBan(TimedResponses):
    """Như `TimedResponses` + lần gọi "hiểu ý sửa lịch" (nhận ra bằng lời dặn) trả danh sách hành động cho trước."""

    def __init__(self, route, sua=(), **kw):
        super().__init__(route, kw.pop("router_delay", 0), kw.pop("answer_delay", 0))
        self.sua = list(sua)

    async def create(self, **kwargs):
        if str(kwargs.get("instructions", "")).startswith((SUA_LICH_LOI_DAN[:60], SUA_LICH_LOI_DAN_CHT[:60])):
            return await self._tra({"hanh_dong": self.sua}, kwargs)
        return await super().create(**kwargs)

    async def _tra(self, payload, kwargs):
        from openai.types.responses import Response
        from test_toc_do_song_song import USAGE, message
        self.calls.append(kwargs)
        return Response.model_validate({"id": "resp_sua", "created_at": 0, "model": "probe", "object": "response", "output": [message(payload)],
                                        "parallel_tool_calls": False, "tool_choice": "auto", "tools": [], "usage": USAGE, "status": "completed"})


def loai(kwargs) -> str:
    dan = str(kwargs.get("instructions", ""))
    return "router" if dan.startswith(ROUTER_INSTRUCTIONS[:80]) else \
        "sua" if dan.startswith((SUA_LICH_LOI_DAN[:60], SUA_LICH_LOI_DAN_CHT[:60])) else "khac"


def chay(deps, flags, luu, route="tro_ly_hue", sua=(), query=QUERY, **kw):
    responses = KichBan(route, sua, **kw)
    gen = OpenAIFullCorpusGenerator(client=Client(responses), model="probe")

    async def go():
        trace = AnswerTrace()
        trace.lich_luu = copy.deepcopy(luu)
        events = [e async for e in answer_turn_stream_parallel(query, *deps, gen, trace, flags)]
        return trace, events

    trace, events = asyncio.run(go())
    return trace, events, responses.calls


def co_nguon(calls) -> list[str]:
    """Loại của mọi yêu cầu gửi model có mang nguồn lịch (nhận ra bằng tiêu đề nguồn + dòng tiền vé do code in)."""
    return [loai(c) for c in calls if v2.TIEU_DE_NGUON_LICH in chu_gui(c) and v2.DONG_TIEN_VE_CHUA_CO in chu_gui(c)]


def test_hoi_thuong_trong_cuoc_co_lich_nhan_dung_mot_nguon_qua_ca_hai_tang(deps):
    trace, _, calls = chay(deps, ON, lich_2_ngay())
    assert co_nguon(calls) == ["khac"]  # đúng MỘT yêu cầu — lần gọi trợ lý; định tuyến và lần hiểu ý sửa không mang nguồn này
    assert [t["name"] for t in trace.tools].count("lich_dang_co") == 1
    nguon = [x for x in trace.so_nguon if x.source == v2.NGUON_LICH_SOURCE]
    assert len(nguon) == 1 and nguon[0].id == len(trace.so_nguon) and nguon[0].excerpts == tuple(v2.dong_lich_dang_co(B, lich_2_ngay()))
    assert trace.sua == {"n_hanh_dong": 0, "khan_cap": False} and [c["route"] for c in trace.llm_calls] == ["sua_lich", "router", "tro_ly_hue"]
    tat, _, calls_tat = chay(deps, OFF, lich_2_ngay())
    assert co_nguon(calls_tat) == [] and "lich_dang_co" not in [t["name"] for t in tat.tools]
    # cờ bật chỉ đổi yêu cầu của lần gọi trợ lý: định tuyến + hiểu ý sửa giống byte cờ tắt
    assert _request_bytes([c for c in calls if loai(c) != "khac"]) == _request_bytes([c for c in calls_tat if loai(c) != "khac"])


def test_cuoc_khong_co_lich_co_bat_giong_byte_co_tat(deps):
    bat, _, calls_bat = chay(deps, ON, None)
    tat, _, calls_tat = chay(deps, OFF, None)
    assert _request_bytes(calls_bat) == _request_bytes(calls_tat) and co_nguon(calls_bat) == []
    assert [t["name"] for t in bat.tools] == [t["name"] for t in tat.tools]


def test_luot_sua_khong_nhan_nguon_va_duong_sua_giong_byte(deps):
    """Model hiểu là câu sửa ("thay điểm" thiếu điểm mới ⇒ thẻ chọn, không cần lần gọi viết câu) ⇒ lượt sửa: đường thường bị huỷ, kết quả không có nguồn lịch;
    yêu cầu của đường sửa giống byte cờ tắt. `answer_delay` giữ lần gọi trợ lý của đường thường chưa xong lúc bị huỷ."""
    sua = [{"loai": "thay_diem", "ten": "Đầm Chuồn"}]
    bat, su_kien, calls_bat = chay(deps, ON, lich_2_ngay(), sua=sua, query="Thay Đầm Chuồn bằng chỗ khác", answer_delay=3)
    tat, _, calls_tat = chay(deps, OFF, lich_2_ngay(), sua=sua, query="Thay Đầm Chuồn bằng chỗ khác", answer_delay=3)
    assert "sua_the" in [k for k, _ in su_kien] and bat.fixed_outcome == "sua_the"
    assert "lich_dang_co" not in [t["name"] for t in bat.tools] and not [x for x in bat.so_nguon if x.source == v2.NGUON_LICH_SOURCE]
    assert _request_bytes([c for c in calls_bat if loai(c) == "sua"]) == _request_bytes([c for c in calls_tat if loai(c) == "sua"])
    assert len([c for c in calls_bat if loai(c) == "sua"]) == 1


def test_luot_bam_the_chon_khong_chay_duong_thuong(deps, monkeypatch):
    """Lượt bấm nút thẻ chọn (`sua_chon`): không có đường trả lời thường ⇒ không thể có nguồn lịch. Đồ giả chỉ để dựng điều kiện: lõi đường thường
    bị gọi thì test hỏng; bước viết lại lịch (cần model) thay bằng một sự kiện."""
    from llm import len_ke_hoach

    async def khong_duoc_goi(*args, **kw):
        raise AssertionError("đường thường không được chạy ở lượt bấm thẻ chọn")
        yield  # pragma: no cover

    async def sua_gia(query, rs, cb, gen, tr, flags, kq):
        yield "sua", {"n_ap": len(kq["da_ap"])}

    monkeypatch.setattr(a, "_answer_core", khong_duoc_goi)
    monkeypatch.setattr(len_ke_hoach, "stream_sua", sua_gia)

    async def go():
        trace = AnswerTrace()
        trace.lich_luu, trace.sua_chon = lich_2_ngay(), {"cu": "Đầm Chuồn", "moi": "bo"}
        gen = OpenAIFullCorpusGenerator(client=Client(KichBan("tro_ly_hue")), model="probe")
        return trace, [e async for e in answer_turn_stream_parallel("", *deps, gen, trace, ON)]

    trace, su_kien = asyncio.run(go())
    assert ("sua", {"n_ap": 1}) in su_kien and "lich_dang_co" not in [t["name"] for t in trace.tools]


def test_tro_chuyen_va_ngoai_pham_vi_trong_cuoc_co_lich_khong_nhan_nguon(deps):
    """Định tuyến chậm hơn lần gọi trợ lý chạy trước ⇒ lần gọi chạy trước (bị bỏ) có thể đã mang nguồn; thứ người dùng nhận và trace cuối thì không."""
    chat, _, calls = chay(deps, ON, lich_2_ngay(), route="tro_chuyen", query="Cảm ơn bạn nhé")
    assert chat.route == "tro_chuyen" and "lich_dang_co" not in [t["name"] for t in chat.tools] and chat.so_nguon == []
    tro_chuyen = [c for c in calls if loai(c) == "khac" and v2.TIEU_DE_NGUON_LICH not in chu_gui(c)]
    assert tro_chuyen  # lần gọi của tuyến trò chuyện (lần cho ra câu trả lời) không mang lịch
    ngoai, su_kien, _ = chay(deps, ON, lich_2_ngay(), route="ngoai_pham_vi", query="Giá vàng hôm nay bao nhiêu?")
    assert [d for k, d in su_kien if k == "delta"] == [OUT_OF_SCOPE_ANSWER]
    assert ngoai.so_nguon == [] and ngoai.tools == [] and ngoai.fixed_outcome == "out_of_scope"


def test_dinh_tuyen_chon_khan_cap_di_duong_tro_ly_hue_nen_co_nguon(deps):
    trace, _, calls = chay(deps, ON, lich_2_ngay(), route="khan_cap", query="Tôi bị lạc ở Đại Nội")
    assert trace.emergency_by == "router" and co_nguon(calls) == ["khac"] and [t["name"] for t in trace.tools].count("lich_dang_co") == 1


# ---------- Phép kiểm số không nhận số của nguồn lịch ----------

def test_so_cua_nguon_lich_khong_mo_rong_kiem_so_thoi_tiet():
    """Nguồn lịch đầy giờ / phút ("8:00", "30", "15"). Câu trả lời trích nguồn lịch rồi nêu "30 °C" không có ở nguồn nào khác ⇒ phép kiểm số thời tiết
    vẫn phải bắt (trước khi sửa: số của mọi nguồn được trích đều được phép)."""
    from llm import thoi_tiet as tt
    from retrieval.full_corpus_context import PackedSource
    lich = PackedSource(id=1, title=v2.TIEU_DE_NGUON_LICH, heading_path=(v2.MUC_NGUON_LICH,), excerpts=tuple(v2.dong_lich_dang_co(B, lich_2_ngay())),
                        source=v2.NGUON_LICH_SOURCE)
    kho = PackedSource(id=2, title="Bài kho", heading_path=("Mục",), excerpts=("Nhiệt độ trung bình 25 °C.",), source="travel/x.md")
    trace = AnswerTrace()
    trace.cited, trace.answer = (lich, kho), "x"
    a._thoi_tiet_cuoi(trace, "Hôm đó khoảng 30 °C, có lúc 25 °C. [1][2]")
    assert trace.thoi_tiet_kiem == ["30"]  # 25 có ở bài kho ⇒ được; 30 chỉ có trong giờ của lịch ⇒ bị bắt
    assert tt.tap_so(" ".join(lich.excerpts)) >= {"30", "15"}  # đúng là nguồn lịch có các số đó


def _luot_co_lich_va_khoang_cach(chu_model: str) -> AnswerTrace:
    """Lượt hỏi thường có nguồn lịch [1] + nguồn khoảng cách do code dựng [2] (model gọi công cụ khoảng cách để ước đường về)."""
    from types import SimpleNamespace
    from llm import khoang_cach as kc
    from retrieval.full_corpus_context import PackedSource
    dong_kc = ("Từ Đại Nội Huế đến Đầm Chuồn: khoảng 12 km theo đường đi, đi xe ước khoảng 25 phút (chưa tính kẹt xe).",)
    trace = AnswerTrace()
    trace.so_nguon = [PackedSource(id=1, title=v2.TIEU_DE_NGUON_LICH, heading_path=(v2.MUC_NGUON_LICH,),
                                   excerpts=tuple(v2.dong_lich_dang_co(B, lich_2_ngay())), source=v2.NGUON_LICH_SOURCE),
                      PackedSource(id=2, title=kc.TIEU_DE_NGUON, heading_path=(kc.MUC_NGUON,), excerpts=dong_kc, source=kc.NGUON_SOURCE)]
    trace.khoang_cach = [{"diem_a": "dai_noi", "diem_b": "dam_chuon", "dong": dong_kc}]
    trace.generated = SimpleNamespace(text=chu_model)
    a._finish_generated(trace, AssistantFlags())
    return trace


def test_so_gio_do_code_in_o_nguon_lich_khong_bi_kiem_so_khoang_cach_rut():
    """Review B M1: phép kiểm số khoảng cách xét MỌI số kèm đơn vị thời gian trong chữ model. Câu trả lời nêu đúng "8 giờ", "5 giờ" code in ở nguồn
    lịch, cạnh số km / phút của nguồn khoảng cách ⇒ không được rút."""
    trace = _luot_co_lich_va_khoang_cach("Ngày 1 phần ban ngày kéo dài 8 giờ, tổng thời lượng tham quan 5 giờ [1]. "
                                         "Từ Đại Nội đến Đầm Chuồn khoảng 12 km, đi xe khoảng 25 phút, có thể kẹt xe [2].")
    assert trace.khoang_cach_kiem == [] and trace.citation_error is None


def test_thoi_gian_di_lai_bia_van_bi_bat_khi_co_nguon_lich():
    """Chỉ số CÓ ĐƠN VỊ thời gian của nguồn lịch được phép: "30 phút" (30 chỉ có trong giờ đồng hồ "10:30") và "40 km" vẫn bị bắt."""
    trace = _luot_co_lich_va_khoang_cach("Ngày 1 kéo dài 8 giờ [1]. Từ Đại Nội đến Đầm Chuồn khoảng 40 km, đi xe khoảng 30 phút, có thể kẹt xe [2].")
    assert trace.khoang_cach_kiem == ["40", "30"] and trace.citation_error is not None


# ---------- Giai đoạn 2: tổng tiền vé lẻ do code cộng từ cột giá của bảng điểm ----------

BANG_GIA = v2.nap_bang_v2(a.BACKEND_DIR / "../data/phase_9/lich_trinh/diem_v11.json")  # bảng có cột `gia_ve` (26 / 41 điểm, giá chép từ kho, đã soát)


def _luu(bang, **ts) -> dict:
    return s.luu_tu_lich(v2.xep_v2(bang, v2.ThamSoV2(**ts)), None, None)


def test_bang_chua_co_cot_gia_thi_chi_mot_dong_chua_tinh_duoc():
    assert not any("gia_ve" in d for d in B.diem)  # bảng đang chạy của settings chưa có cột giá ⇒ hành vi giai đoạn 1
    assert v2.dong_tien_ve(B, lich_2_ngay()) == [v2.DONG_TIEN_VE_CHUA_CO]


def test_tong_ve_le_lich_mac_dinh_khop_dap_so_tinh_tay():
    """Đáp số tính tay (người chép bảng giá ghi trước, độc lập với code): lịch mặc định 2 ngày, 2 người lớn — Đại Nội 200.000 + Lăng Đồng Khánh
    100.000 + Lăng Thiệu Trị 50.000, × 2 = 700.000 đồng; miễn phí: Chùa Thiên Mụ, Đồi Vọng Cảnh; 3 điểm chưa có giá không tính là 0."""
    dong = v2.dong_tien_ve(BANG_GIA, _luu(BANG_GIA, so_ngay=2, kieu_di="can_bang", so_thich=(), nguoi_lon=2))
    assert dong == [
        "Tiền vé lẻ của lịch — số do hệ thống tính từ bảng giá (2 người lớn):",
        "- Đại Nội Huế: 200.000 đồng/người lớn × 2 = 400.000 đồng.",
        "- Lăng Đồng Khánh: 100.000 đồng/người lớn × 2 = 200.000 đồng.",
        "- Lăng Thiệu Trị: 50.000 đồng/người lớn × 2 = 100.000 đồng.",
        "Miễn phí: Chùa Thiên Mụ, Đồi Vọng Cảnh.",
        "Chưa có giá trong bảng (KHÔNG tính là 0 đồng): Đầm Chuồn, Chợ Đông Ba, Phố đi bộ Nguyễn Đình Chiểu.",
        "Tổng vé lẻ của các điểm có giá: 700.000 đồng (chưa gồm 3 điểm chưa có giá; chưa tính vé gộp, miễn giảm — các điểm thuộc Quần thể di tích có "
        "vé gộp rẻ hơn, xem bài vé).",
    ]
    assert v2.dong_lich_dang_co(BANG_GIA, _luu(BANG_GIA, so_ngay=2, kieu_di="can_bang", so_thich=(), nguoi_lon=2))[-7:] == dong  # nằm cuối nguồn lịch


def test_khoang_gia_tre_em_va_diem_thieu_muc_tre_em():
    """Tính tay: 2 người lớn + 1 trẻ em — Đèo Hải Vân 70.000 × 2 = 140.000 (trẻ em miễn phí) · Bạch Mã 60.000 – 65.000 × 2 = 120.000 – 130.000 + trẻ
    em 20.000 – 25.000 · Thác Nhị Hồ 10.000 – 15.000 × 2 = 20.000 – 30.000 (bảng không có mức trẻ em) ⇒ tổng 300.000 – 325.000, là KHOẢNG."""
    dong = v2.dong_tien_ve(BANG_GIA, _luu(BANG_GIA, so_ngay=3, kieu_di="kham_pha", so_thich=("thien_nhien",), nguoi_lon=2, tre_em=1))
    assert dong[0].endswith("(2 người lớn, 1 trẻ em tính mức 7–12 tuổi):")
    assert "- Vườn quốc gia Bạch Mã: 60.000 – 65.000 đồng/người lớn × 2 = 120.000 – 130.000 đồng; 20.000 – 25.000 đồng/trẻ em × 1 = 20.000 – 25.000 đồng." in dong
    assert "- Đèo Hải Vân: 70.000 đồng/người lớn × 2 = 140.000 đồng; trẻ em 7–12 tuổi miễn phí." in dong
    assert "Chưa có mức vé trẻ em 7–12 tuổi trong bảng (phần trẻ em chưa vào tổng): Thác Nhị Hồ." in dong
    assert dong[-1] == ("Tổng vé lẻ của các điểm có giá: 300.000 – 325.000 đồng (chưa gồm 3 điểm chưa có giá; chưa gồm vé trẻ em ở 1 điểm; "
                        "chưa tính vé gộp, miễn giảm).")  # không điểm nào thuộc Quần thể di tích ⇒ không nhắc vé gộp


def test_khong_biet_so_nguoi_lon_thi_khong_nhan_ra_tong():
    luu = _luu(BANG_GIA, so_ngay=2, kieu_di="can_bang", so_thich=(), nguoi_lon=2)
    luu["tham_so"]["nguoi_lon"] = None
    dong = v2.dong_tien_ve(BANG_GIA, luu)
    assert "- Đại Nội Huế: 200.000 đồng/người lớn." in dong and dong[-1].startswith("Chưa biết số người lớn nên chưa nhân ra tổng")
    assert not any("Tổng vé lẻ" in x for x in dong)
