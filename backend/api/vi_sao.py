"""Nút "Vì sao trả lời vậy?" (công tắc `assistant.vi_sao`, mặc định TẮT; chủ dự án chọn hướng "Giải thích" 06:16 24/11/2026).

Người xem demo bấm nút dưới một câu trả lời ⇒ thấy lượt đó trợ lý đã làm gì: các lần gọi model, đã tìm gì trong kho / gọi công cụ gì, câu trả lời
dựa vào nguồn nào, mất bao lâu. KHÔNG có model nào được gọi ở đây: bản tóm tắt chỉ sắp lại thứ lượt đó ĐÃ ghi trên `AnswerTrace`.

Cách chạy: lúc một lượt kết thúc và đã có mã lượt (`turn_id`, cấp sẵn ở sự kiện `done` — `api/feedback.py`), route dựng MỘT bản tóm tắt nhỏ từ đúng
bản ghi mà sổ vết dùng (`core/so_vet.ban_ghi`) rồi cất vào RAM theo mã lượt (trần `MAX_LUOT`; hết hạn sau `TTL_SECONDS` = 30 phút, cùng hạn với trí nhớ
cuộc trò chuyện — bản tóm tắt có câu người dùng gõ, câu tìm, câu tra web, mà trang Giới thiệu nói chữ người dùng ở trong bộ nhớ tối đa 30 phút; khởi động lại
server ⇒ mất). `GET /api/vi_sao/{turn_id}`
trả bản đó. Không đọc / ghi file nào, không ghi log nào có chữ người dùng ⇒ không phụ thuộc cờ `so_vet`. Mã lượt ngẫu nhiên 16 ký tự, không nằm trong
cookie ⇒ người khác không đoán được lượt của ai.

`tom_tat` nhận ĐÚNG khuôn một dòng sổ vết ⇒ thử được trên các dòng thật ở `data/debug_trace/` mà không gọi model (`tests/test_vi_sao.py` dùng bản ghi tự dựng).
Thứ KHÔNG có ở đây: phép đối chiếu từng CÂU của câu trả lời với ĐOẠN nó dựa vào — hệ thống chưa làm phép đó; khuôn không chừa chỗ sẵn.
"""
import logging
import time
from collections import OrderedDict
from pathlib import PurePosixPath

from fastapi import APIRouter, Request

from api.conversations import TTL_SECONDS
from core import so_vet

logger = logging.getLogger("chat")
router = APIRouter()

MAX_LUOT = 200  # trần RAM: bỏ lượt cũ nhất (mỗi bản vài KB)
# ký tự: chuỗi gửi model chỉ KHÁC câu gõ khi lượt mang các ô đã chọn (thẻ hỏi lại, biểu mẫu Lên kế hoạch — `chat._model_query` ghép giá trị các ô vào câu),
# khi đó nó dài gấp nhiều lần câu gõ. Lượt nối tiếp thường KHÔNG đổi câu: lịch sử đi riêng, không ghép vào chuỗi này.
TRAN_CAU_GUI = 300

# Nhãn do code viết — giao diện in nguyên, không tự dịch mã.
NHAN_GOI = {"phan_loai": "Phân loại câu hỏi", "tim_them": "Quyết định tìm thêm / gọi công cụ", "viet": "Viết câu trả lời",
            "hieu_lenh": "Hiểu câu lệnh sửa lịch", "viet_cau_ta": "Viết câu tả các điểm trong lịch", "web": "Viết mục «Từ web»", "khac": "Gọi model"}
NHAN_CONG_CU = {
    "thoi_tiet": "Xem dự báo thời tiết", "ngay_lich": "Tra ngày và âm lịch", "lich_san": "Tra ngày và âm lịch (code tính sẵn)",
    "khoang_cach": "Tính khoảng cách giữa hai điểm", "khoang_cach_san": "Tính khoảng cách giữa hai điểm (code tính sẵn)",
    "gan_diem": "Tìm quán / điểm gần một nơi", "liet_ke_bai": "Liệt kê các bài của kho khớp câu hỏi",
    "su_kien": "Tra lễ hội / sự kiện theo ngày", "su_kien_san": "Tra lễ hội / sự kiện theo ngày (code tính sẵn)",
    "lich_dang_co": "Đọc lịch đang có của cuộc trò chuyện", "lich_trinh": "Xếp lịch", "tra_web": "Tra web một lần (kho không có câu trả lời)",
    "viet_lai_het_luot": "Viết lại câu trả lời từ bằng chứng đã gom", "chay_lai_khong_dap": "Chạy lại lượt, không dùng câu trả lời liền trước",
}
# Công cụ do CODE tự chạy (không phải model gọi giữa chừng); mục có khoá `by` thì theo `by`.
CODE_CHAY = {"lich_san", "khoang_cach_san", "su_kien_san", "lich_dang_co", "tra_web", "viet_lai_het_luot", "chay_lai_khong_dap"}
BO_QUA = {"lam_thay"}  # dấu nội bộ, không phải một bước người xem cần thấy
NHAN_HANH_DONG = {"them_diem": "Thêm", "bo_diem": "Bỏ", "thay_diem": "Thay", "doi_buoi": "Dời", "doi_hang_o": "Đổi hạng chỗ ở",
                  "doi_so_ngay": "Đổi số ngày", "doi_cho_ngay": "Đổi chỗ hai ngày", "chua_ho_tro": "Việc chưa hỗ trợ"}
NHAN_BUOI = {"sang": "buổi sáng", "chieu": "buổi chiều", "toi": "buổi tối"}


class KhoViSao:
    """Mã lượt ⇒ bản tóm tắt, trong RAM, có trần số lượt và có hạn giờ (`ttl` giây kể từ lúc cất). Bản quá hạn bị XOÁ khỏi RAM ở lần cất / lần đọc kế, và
    đọc ra None như bản đã bị đẩy khỏi trần."""

    def __init__(self, max_luot: int = MAX_LUOT, ttl: float = TTL_SECONDS, clock=time.monotonic) -> None:
        self._items: OrderedDict[str, tuple[float, dict]] = OrderedDict()  # thứ tự chèn = thứ tự thời gian
        self._max, self._ttl, self._clock = max_luot, ttl, clock

    def _don_het_han(self) -> None:
        moc = self._clock() - self._ttl
        while self._items and next(iter(self._items.values()))[0] < moc:
            self._items.popitem(last=False)

    def dat(self, turn_id: str, ban: dict) -> None:
        self._don_het_han()
        self._items[turn_id] = (self._clock(), ban)
        while len(self._items) > self._max:
            self._items.popitem(last=False)

    def lay(self, turn_id: str) -> dict | None:
        self._don_het_han()
        muc = self._items.get(turn_id)
        return None if muc is None else muc[1]


def _giay(ms) -> float | None:
    return None if ms is None else round(float(ms) / 1000, 2)


def _la_luot_sua(sua: dict | None) -> bool:
    """Cuộc đã có lịch thì lượt nào cũng mang khối `sua_lich`; lượt SỬA là lượt có hành động, có dòng kết quả, hoặc đi đường nút thẻ chọn."""
    if not sua:
        return False
    return bool((sua.get("so_dem") or {}).get("n_hanh_dong") or sua.get("thay_doi") or sua.get("chon_the"))


def _loai(ghi: dict) -> str:
    so_do, tra_loi = ghi.get("so_do") or {}, ghi.get("tra_loi") or {}
    if so_do.get("cache") == "trung":
        return "bo_nho_dem"
    if _la_luot_sua(ghi.get("sua_lich")):
        return "sua_lich"
    if (ghi.get("lich") or {}).get("bieu_mau"):
        return "lap_lich"
    ket = so_do.get("outcome") or tra_loi.get("ket_qua_co_dinh")
    if ket == "out_of_scope":
        return "ngoai_pham_vi"
    if ket == "lam_thay":
        return "lam_thay"
    if so_do.get("refusal") or ket == "refusal_no_sources":
        return "tu_choi"
    return "hoi_dap"


def _goi_model(ghi: dict, loai: str) -> list[dict]:
    ra = []
    for g in ghi.get("goi_model") or []:
        tuyen, kind = g.get("route"), g.get("kind") or []
        if tuyen == "router":
            viec = "phan_loai"
        elif tuyen == "sua_lich":
            viec = "hieu_lenh"
        elif tuyen == "tra_web":
            viec = "web"
        elif "function_call" in kind:
            viec = "tim_them"
        elif loai == "lap_lich":
            viec = "viet_cau_ta"
        elif tuyen in ("tro_ly_hue", "tro_chuyen"):
            viec = "viet"
        else:
            viec = "khac"
        ra.append({"viec": viec, "nhan": NHAN_GOI[viec], "giay": _giay(g.get("ms"))})
    return ra


def _tieu_de_kham_pha(bai_ids, nguon: str) -> str | None:
    """`bai_ids` của route là sổ bài Khám phá (đường dẫn ⇒ {tieu_de, …}); nơi gọi khác có thể truyền một tập đường dẫn ⇒ không có tiêu đề."""
    bai = bai_ids.get(nguon) if isinstance(bai_ids, dict) else None
    return bai.get("tieu_de") if isinstance(bai, dict) else None


def _buoc_tim(tim: dict, ms, ghi: dict, trich: dict, bai_ids) -> dict:
    cau = [c for c in (tim.get("cau") or []) if isinstance(c, str)]
    cua_model = tim.get("by") == "model"
    dinh_tuyen = set((ghi.get("tuyen") or {}).get("cau_tim_dinh_tuyen") or ())
    if cua_model:
        nhan = "Model tự viết thêm câu tìm"
    elif len(cau) > 1:
        nhan = f"Hệ thống tìm bằng {len(cau)} câu tìm (câu của bạn và từng vế hỏi)"
    elif cau and cau[0] in dinh_tuyen:
        nhan = "Hệ thống tìm bằng câu tìm do bước phân loại viết"
    elif cau and cau[0] in (ghi.get("cau_go"), ghi.get("cau_gui_model")):
        nhan = "Hệ thống tìm bằng chính câu của bạn"
    else:
        nhan = "Hệ thống tìm trong kho"
    bai: dict[str, dict] = {}
    for hang, kq in enumerate(tim.get("ket_qua") or [], start=1):  # thứ tự kết quả = thứ hạng của lần tìm
        nguon = kq.get("source") or ""
        # tiêu đề bài: của chính đoạn tìm được (như danh sách nguồn) ⇒ của nguồn được trích ⇒ của trang Khám phá; tên file chỉ là chỗ lùi cuối
        # cho dòng sổ vết cũ chưa ghi tiêu đề (đọc nhánh 24/11: tên file không dấu từng lọt vào bảng của 1.318 / 6.475 dòng bài)
        o = bai.setdefault(nguon, {"title": kq.get("title") or trich.get(nguon) or _tieu_de_kham_pha(bai_ids, nguon) or PurePosixPath(nguon).stem,
                                   "bai_id": nguon if nguon in bai_ids else None,  # `duoc_trich` dưới đây là dấu mức BÀI (bài có đoạn được trích), không phải của từng đoạn
                                   "so_doan": 0, "hang": hang, "duoc_trich": nguon in trich})
        o["so_doan"] += 1
    vao = tim.get("vao_ngu_canh")
    return {"loai": "tim", "ai": "model" if cua_model else "he_thong", "nhan": nhan, "giay": _giay(ms), "cau": cau,
            "so_doan_tim": len(tim.get("ket_qua") or []), "so_doan_moi": None if vao is None else len(vao), "bai": list(bai.values())}


def _buoc(ghi: dict, trich: dict, bai_ids) -> list[dict]:
    """Mọi lần tìm + mọi công cụ khác, ĐÚNG thứ tự lượt đã ghi (`trace.tools`); mỗi lần tìm thật ghép với bản ghi chi tiết cùng thứ tự của nó."""
    tim = list(ghi.get("tim_kho") or [])
    ra, i = [], 0
    for c in ghi.get("cong_cu") or []:
        ten = c.get("name")
        if ten in BO_QUA:
            continue
        if ten == "tim_kho":
            if c.get("sau_lich") or c.get("het_luot"):  # model xin tìm nhưng code không cho chạy (đã có lịch / hết lượt tìm): không có bản ghi chi tiết
                continue
            if i < len(tim):
                ra.append(_buoc_tim(tim[i], c.get("ms"), ghi, trich, bai_ids))
                i += 1
            continue
        ai = "model" if c.get("by") == "model" else "he_thong" if c.get("by") == "code" or ten in CODE_CHAY else "model"
        ra.append({"loai": "cong_cu", "ai": ai, "nhan": NHAN_CONG_CU.get(ten) or f"Công cụ: {ten}", "giay": _giay(c.get("ms"))})
    ra.extend(_buoc_tim(t, None, ghi, trich, bai_ids) for t in tim[i:])  # lệch số (không nên có): vẫn hiện đủ lần tìm, không kèm giây
    return ra


def _hanh_dong(h: dict) -> str:
    phan = [NHAN_HANH_DONG.get(h.get("loai"), str(h.get("loai")))]
    if h.get("ten"):
        phan.append(str(h["ten"]))
    if h.get("ten_moi"):
        phan.append(f"bằng {h['ten_moi']}")
    if h.get("ngay") is not None:
        phan.append(f"ngày {h['ngay']}")
    if h.get("buoi"):
        phan.append(NHAN_BUOI.get(h["buoi"], str(h["buoi"])))
    return " · ".join(phan)


def _sua_lich(sua: dict) -> dict:
    return {"model_doc": [{"nhan": _hanh_dong(h)} for h in sua.get("model_ra") or [] if isinstance(h, dict)],
            "ket_qua": [{"cau": d.get("cau"), "duoc": bool(d.get("duoc"))} for d in sua.get("thay_doi") or [] if isinstance(d, dict) and d.get("cau")]}


def _web(ghi: dict) -> dict | None:
    web = ghi.get("web")
    if not web or not web.get("cau_gui_tra_web"):
        return None
    return {"cau": web["cau_gui_tra_web"], "so_nguon": len(web.get("so_web") or [])}


def tom_tat(ghi: dict, bai_ids=()) -> dict:
    """Bản tóm tắt của một lượt từ bản ghi khuôn sổ vết (`so_vet.ban_ghi`). Chỉ sắp lại thứ đã ghi; mọi câu chữ ở đây do code viết."""
    so_do, tra_loi = ghi.get("so_do") or {}, ghi.get("tra_loi") or {}
    loai = _loai(ghi)
    nguon_trich = tra_loi.get("nguon_trich") or []
    trich = {s.get("source"): s.get("title") for s in nguon_trich}
    goi = _goi_model(ghi, loai)
    buoc = _buoc(ghi, trich, bai_ids)
    lan_tim = [b for b in buoc if b["loai"] == "tim"]
    so_doan = len(ghi.get("ngu_canh") or [])  # mỗi phần tử là chữ ngữ cảnh của MỘT lần tìm ⇒ đếm đoạn theo `so_doan_moi`
    so_doan = sum(b["so_doan_moi"] or 0 for b in lan_tim) if lan_tim else so_doan
    web = _web(ghi)
    sua = _sua_lich(ghi["sua_lich"]) if loai == "sua_lich" else None
    cau_go, cau_gui = ghi.get("cau_go"), ghi.get("cau_gui_model")
    khac = isinstance(cau_gui, str) and isinstance(cau_go, str) and cau_gui.strip() != cau_go.strip()
    so_truoc = len(ghi.get("lich_su") or [])

    ghi_chu = []
    if loai == "bo_nho_dem":
        tom = "Câu trả lời lấy lại từ một lượt giống hệt trước đó — không gọi model, không tìm lại."
        ghi_chu.append("Hệ thống nhớ tạm câu trả lời của những câu hỏi lặp lại y nguyên; khởi động lại máy chủ thì bộ nhớ này mất.")
    elif loai == "sua_lich":
        tom = (f"Model đọc câu lệnh ra {len(sua['model_doc'])} việc; đặt vào lịch và kiểm luật là việc của code."
               if sua["model_doc"] else "Lượt sửa lịch này không có việc nào do model đọc ra.")
        ghi_chu.append("Model chỉ đọc câu lệnh (làm gì, điểm nào, ngày / buổi nào). Việc đặt điểm vào lịch và kiểm luật — giờ mở cửa, khu, nhịp đi — do code làm."
                       if goi else "Bạn bấm nút — code áp thẳng lựa chọn đó, không gọi model.")
    elif loai == "lap_lich":
        tom = f"Code xếp khung lịch; model được gọi {len(goi)} lần để viết câu tả các điểm từ kho."
        du_phong = (ghi.get("lich") or {}).get("v2_so_cau_du_phong")
        ghi_chu.append("Khung lịch (điểm nào, ngày nào, giờ nào) do code xếp theo luật — không gọi model. Model chỉ viết câu tả cho từng điểm từ bài trong kho"
                       + (f"; {du_phong} câu bị bộ kiểm loại và được thay bằng câu dự phòng." if du_phong else "."))
    elif loai == "ngoai_pham_vi":
        tom = "Bước phân loại xếp câu này ngoài phạm vi văn hoá – du lịch Huế ⇒ không tìm trong kho, trả một câu cố định."
        ghi_chu.append("Câu trả lời của lượt này là câu cố định do code trả, không phải model tự viết.")
    elif loai == "lam_thay":
        tom = "Bạn nhờ trợ lý tự làm một việc hệ thống không có (đặt chỗ, gửi tin, xem tình trạng phòng…) ⇒ trả một câu nói thật cố định."
        ghi_chu.append("Câu trả lời của lượt này là câu cố định do code chọn theo loại việc được nhờ.")
    elif loai == "tu_choi":
        # chữ chỉ nói điều hệ thống BIẾT (soát khác hãng 24/11/2026): đoạn được ĐƯA cho model, không phải "model đã đọc"; lượt từ chối = model trả câu
        # cố định, hệ thống không tự kiểm lại là kho thiếu thật hay không
        tom = f"Trợ lý gọi model {len(goi)} lần, tìm trong kho {len(lan_tim)} lần, đưa {so_doan} đoạn kho cho model; lượt này không có căn cứ đủ để trả lời."
        ghi_chu.append("Không có đoạn nào để đưa cho model ⇒ code trả câu từ chối cố định, không gọi model viết." if tra_loi.get("ket_qua_co_dinh") == "refusal_no_sources"
                       else "Câu từ chối là câu cố định của hệ thống: model nhận các đoạn tìm được và trả đúng câu đó thay vì tự viết từ hiểu biết riêng. "
                            "Hệ thống không tự kiểm lại là kho có thật sự thiếu hay không.")
    else:
        tom = f"Trợ lý gọi model {len(goi)} lần, tìm trong kho {len(lan_tim)} lần, đưa {so_doan} đoạn kho cho model, trích {len(nguon_trich)} nguồn."
    if so_truoc and loai != "bo_nho_dem":
        ghi_chu.append(f"Model được đưa kèm {so_truoc} lượt trước của cuộc trò chuyện.")
    if web is not None:
        ghi_chu.append("Phần «Từ web» lấy ngoài kho, chưa được kiểm với kho.")
    if any(c.get("name") == "viet_lai_het_luot" for c in ghi.get("cong_cu") or []):
        ghi_chu.append("Bản viết đầu không qua được phép kiểm nguồn nên hệ thống cho viết lại một lần từ bằng chứng đã gom.")

    return {
        "loai": loai, "tom_tat": tom,
        "cau": {"go": cau_go, "gui": (cau_gui[:TRAN_CAU_GUI] + ("…" if len(cau_gui) > TRAN_CAU_GUI else "")) if khac else None, "so_luot_truoc": so_truoc},
        "goi_model": goi, "buoc": buoc,
        "nguon": [{"ma": s.get("id"), "title": s.get("title"), "bai_id": s.get("source") if s.get("source") in bai_ids else None,
                   "muc": " › ".join(s.get("heading_path") or [])} for s in nguon_trich],
        "web": web, "sua_lich": sua,
        "thoi_gian": {"tong": _giay(so_do.get("total_ms")), "tim": _giay(so_do.get("search_ms")), "dung_ngu_canh": _giay(so_do.get("context_ms")),
                      "model": _giay(so_do.get("generation_ms"))},
        "ghi_chu": ghi_chu,
    }


def cat(state, bat: bool, duong: str, metrics: dict, trace, cau_go, cau_model, bai_ids=()) -> None:
    """Route gọi ở cuối lượt (cùng chỗ ghi sổ vết, lúc số đo đã đủ). Nơi gọi (`chat._ghi_vet`) bọc lỗi: bản tóm tắt là phần thêm, không được làm
    hỏng lượt trả lời."""
    kho, turn_id = getattr(state, "vi_sao", None), metrics.get("turn_id")
    if not bat or kho is None or not turn_id or trace is None:
        return
    kho.dat(turn_id, tom_tat(so_vet.ban_ghi(duong, metrics, trace, cau_go, cau_model), bai_ids))


@router.get("/api/vi_sao/{turn_id}")
async def vi_sao(turn_id: str, request: Request):
    """Bản tóm tắt "lượt này trợ lý đã làm gì". 404: công tắc tắt · mã lượt không có (server đã khởi động lại, quá trần, quá hạn 30 phút, lượt không có câu trả lời)."""
    flags = getattr(request.app.state, "assistant_flags", None)
    kho = getattr(request.app.state, "vi_sao", None)
    ban = kho.lay(turn_id) if kho is not None and getattr(flags, "vi_sao", False) is True else None
    if ban is None:
        from api.routes.chat import error_response  # một chỗ dựng thân lỗi JSON (như `api/feedback.py`)
        return error_response(404, "khong_co", "Chi tiết của lượt này không còn được giữ.")
    return ban
