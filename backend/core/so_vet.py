"""Sổ vết debug CÓ NỘI DUNG — chỉ cho máy local (User 15/11/2026: báo lỗi khi thử mà `chat_metrics` không có nội dung ⇒ nhóm phải đoán + tái tạo).

Cờ `assistant.so_vet` (mặc định TẮT; biến môi trường `HUE_SO_VET=true` bật). Bật ⇒ mỗi lượt ghi MỘT dòng JSON vào
`data/debug_trace/<YYYY-MM-DD>.jsonl` (`data/` không vào git): câu hỏi, lịch sử gửi model, tuyến, từng lần tìm kho, ngữ cảnh, từng lần gọi model,
câu trả lời + nguồn, phần web, sửa lịch, lỗi — kèm NGUYÊN dòng số đo `chat_metrics` của lượt (để nối: cùng `git_sha`, `turn_id`, giờ).
KHÔNG ghi cookie, IP, khoá. `chat_metrics` giữ nguyên (không nội dung). Bản Docker / công khai: KHÔNG bật (chữ người dùng nằm trên đĩa).
Ghi hỏng không được làm hỏng lượt trả lời: mọi lỗi ở đây chỉ thành một dòng cảnh báo."""
import datetime as dt
import json
import logging
from pathlib import Path

logger = logging.getLogger("chat")
THU_MUC = Path(__file__).resolve().parents[2] / "data" / "debug_trace"
TOP_TIM = 10  # số kết quả mỗi lần tìm được ghi (= số đoạn tối đa vào ngữ cảnh)


def vet_tim(queries: list[str], by: str, documents, packed) -> dict:
    """Một lần tìm kho (lõi gọi ở `search_into_trace`; chỉ giữ trong RAM của lượt): câu tìm, top kết quả (mã đoạn, file, điểm), đoạn vào ngữ cảnh."""
    try:  # gọi trong `finally` của lần tìm, cả khi cờ tắt ⇒ không bao giờ được ném (lỗi ở đây sẽ đè lỗi gốc của lần tìm — review B M-1)
        return {"cau": list(queries), "by": by,
                # `title` (24/11/2026): tiêu đề bài của đoạn — cùng nơi danh sách nguồn lấy tiêu đề
                "ket_qua": [{"chunk_id": d.id, "source": d.metadata.get("source"), "title": d.metadata.get("title"), "diem": round(float(d.score), 4)}
                            for d in (documents or [])[:TOP_TIM]],
                "vao_ngu_canh": None if packed is None else list(packed.document_ids)}
    except Exception as exc:
        return {"cau": list(queries), "by": by, "loi": type(exc).__name__}


def ban_ghi(duong: str, metrics: dict, trace=None, cau_go: str | None = None, cau_model: str | None = None, them: dict | None = None) -> dict:
    """Bản ghi của một lượt. `trace` = `AnswerTrace` (đọc bằng `getattr` ⇒ module này không phụ thuộc lõi); `them` = phần riêng của route (ảnh)."""
    ra = {"gio": dt.datetime.now().isoformat(timespec="seconds"), "duong": duong, "cau_go": cau_go, "cau_gui_model": cau_model,
          "so_do": {k: v for k, v in metrics.items()}}
    if trace is not None:
        lay = lambda ten, mac_dinh=None: getattr(trace, ten, mac_dinh)  # noqa: E731
        vet = lay("vet", {}) or {}
        ra.update(
            lich_su=[list(cap) for cap in lay("history", ())],
            tuyen={"route": lay("route"), "loi": lay("route_error"), "khan_cap_boi": lay("emergency_by"), "cau_tim_dinh_tuyen": lay("cau_tim")},
            tim_kho=vet.get("tim", []),
            cau_tim_model=list(lay("model_queries", [])),
            ngu_canh=list(lay("context_parts", [])),
            the_noi=list(lay("the_noi", [])),  # công tắc `the_noi`: tên các nơi được gắn thẻ trong lượt (chữ thẻ nằm trong `ngu_canh`)
            cong_cu=list(lay("tools", [])),
            goi_model=list(lay("llm_calls", [])),
            tra_loi={"chu": lay("answer"), "ket_qua_co_dinh": lay("fixed_outcome"), "ghi_chu": lay("notice"),
                     "nguon_trich": None if lay("cited") is None else [{"id": s.id, "title": s.title, "source": s.source,
                                                                         "heading_path": list(s.heading_path)} for s in lay("cited")],
                     "loi_trich_dan": None if lay("citation_error") is None else str(lay("citation_error"))[:500],
                     "nhieu_y": lay("nhieu_y"), "chi_y_thieu": lay("chi_y_thieu"), "hoi_lai": lay("clarify")},
            web=None if lay("web") is None else {**lay("web"), **(vet.get("web") or {})},
            sua_lich=None if lay("sua") is None and "sua" not in vet else {"so_dem": lay("sua"), **(vet.get("sua") or {})},
            lich={"bieu_mau": lay("bieu_mau"), "truong": lay("truong"), "buoc": lay("buoc_lich"), "kiem": lay("lich_kiem"),
                  "khung": (lay("lich") or {}).get("khung"), "v2_loi_khung": (lay("lich_v2") or {}).get("loi_khung"),
                  "v2_so_cau_du_phong": (lay("lich_v2") or {}).get("so_cau_du_phong"),
                  "v2_cau_bi_loai": (lay("lich_v2") or {}).get("cau_bi_loai"),  # nguyên văn câu model viết bị `kiem_cau` loại + mã lỗi
                  # lịch bản 2 giữ khung ở `trace.lich_v2` (điểm nào ngày / buổi nào — thứ cần khi "lịch xếp lạ"); khoá của `mua` là ngày ⇒ đổi ra chữ
                  "v2_khung": (lay("lich_v2") or {}).get("khung"), "v2_ngay_di": (lay("lich_v2") or {}).get("ngay_di"),
                  "v2_mua": {str(k): v for k, v in ((lay("lich_v2") or {}).get("mua") or {}).items()} or None} if lay("lich") or lay("lich_v2") or lay("bieu_mau") else None,
            thoi_tiet=lay("thoi_tiet"),
            loi=vet.get("loi") or (None if lay("tool_error") is None else repr(lay("tool_error"))[:500]),
        )
    if them:
        ra.update(them)
    return ra


def ghi(bat: bool, duong: str, metrics: dict, trace=None, cau_go: str | None = None, cau_model: str | None = None, them: dict | None = None,
        thu_muc: Path = THU_MUC) -> None:
    try:
        if not bat:
            return
        dong = json.dumps(ban_ghi(duong, metrics, trace, cau_go, cau_model, them), ensure_ascii=False, default=str)
        thu_muc.mkdir(parents=True, exist_ok=True)
        with open(thu_muc / f"{dt.date.today().isoformat()}.jsonl", "a", encoding="utf-8") as f:
            f.write(dong + "\n")
    except Exception as exc:  # sổ vết là công cụ debug — không bao giờ làm hỏng lượt trả lời
        logger.warning("so_vet failed: %s", type(exc).__name__)
