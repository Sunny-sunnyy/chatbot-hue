"""Thẻ khách sạn dưới câu trả lời (`frontend/src/theKhachSan.js`, hàm thuần; plan 2026-11-15-the-khach-san-chat T1–T2) — chạy bằng node thật."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "frontend/src"
NODE = shutil.which("node")
LT = "travel/services/Lưu trú ở Huế — x.md"  # chỉ cần đúng tiền tố bài lưu trú


def chay(turns: list[dict], co_so: list[dict]) -> list:
    js = (f"import {{ theKhachSan }} from '{(SRC / 'theKhachSan.js').as_uri()}';\n"
          f"const cs = {json.dumps(co_so, ensure_ascii=False)};\n"
          f"console.log(JSON.stringify({json.dumps(turns, ensure_ascii=False)}.map(t => theKhachSan(t, cs).map(c => c.ten))));")
    return json.loads(subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout)


@pytest.mark.skipif(NODE is None, reason="cần node (giao diện build bằng node)")
def test_hotel_cards_only_for_lodging_answers_by_core_name_longest_match():
    cs = [{"ten": t, "xep_hang": "4 sao"} for t in ("Khách sạn nghỉ dưỡng Villa Louise", "Khu nghỉ dưỡng Villa Louise Beach", "Khách sạn Silk Path Grand Huế",
                                                    "Khách sạn nghỉ dưỡng Laguna Lăng Cô", "Khách sạn nghỉ dưỡng Hương Giang", "Khách sạn Một", "Khách sạn A B", "Khách sạn C D")]
    goc = {"phase": "done", "outcome": "success", "tuChoiKho": False, "web": None, "lich": None, "lichV2": None, "clarify": None, "suaThe": None,
           "sources": [{"bai_id": LT, "title": "Lưu trú"}]}
    ca = [
        {**goc, "text": "Ở gần biển có **Villa Louise Beach**."},                                   # tên dài nhất ⇒ không kèm "Villa Louise"
        {**goc, "text": "Laguna Lăng Cô và Silk Path Grand đều 5 sao."},                            # tên lõi; bỏ "Huế" cuối
        {**goc, "text": "Khách sạn nghỉ dưỡng Hương Giang ở số 51 Lê Lợi, gần sông Hương Giang."},   # một thẻ, không lặp
        {**goc, "text": "C D, A B, Laguna Lăng Cô, Silk Path Grand Huế"},                           # ≤ 3, theo thứ tự xuất hiện
        {**goc, "text": "Một ở trung tâm, gần Khách sạn Một."},                                     # tên lõi 1 chữ ⇒ chỉ khớp khi có chữ loại hình trước
        {**goc, "text": "Laguna Lăng Cô", "sources": [{"bai_id": "travel/places/Vịnh Lăng Cô.md", "title": "Vịnh"}]},  # không trích bài lưu trú ⇒ 0 (T1)
        {**goc, "text": "Laguna Lăng Cô", "web": {"outcome": "co_muc"}},                             # có mục web ⇒ 0
        {**goc, "text": "Ba Villa Louisea"},                                                          # không theo ranh giới từ ⇒ 0
    ]
    trung = [{"ten": "Khách sạn Thành Nội", "xep_hang": "2 sao"}, {"ten": "Khách sạn Eldora", "xep_hang": "4 sao"}]  # review E m-1
    ca2 = [{**goc, "text": "Khách sạn này nằm trong Thành Nội."}, {**goc, "text": "Có khách sạn Thành Nội ở gần."},
           {**goc, "text": "Bạn thử khách sạn Eldora."}, {**goc, "text": "Eldora ở Bến Nghé."}]
    assert chay(ca2, trung) == [[], ["Khách sạn Thành Nội"], ["Khách sạn Eldora"], []]
    assert chay(ca, cs) == [["Khu nghỉ dưỡng Villa Louise Beach"], ["Khách sạn nghỉ dưỡng Laguna Lăng Cô", "Khách sạn Silk Path Grand Huế"],
                            ["Khách sạn nghỉ dưỡng Hương Giang"], ["Khách sạn C D", "Khách sạn A B", "Khách sạn nghỉ dưỡng Laguna Lăng Cô"], ["Khách sạn Một"], [], [], []]
