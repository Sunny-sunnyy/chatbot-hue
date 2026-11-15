"""Luật ảnh dưới câu trả lời (`frontend/src/anhTraLoi.js`, hàm thuần) — chạy bằng node thật trên anhBai.js thật: code quyết khi nào có ảnh."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "frontend/src"
NODE = shutil.which("node")


def chay(turns: list[dict]) -> list:
    js = (f"import {{ anhTraLoi }} from '{(SRC / 'anhTraLoi.js').as_uri()}';\n"
          f"console.log(JSON.stringify({json.dumps(turns, ensure_ascii=False)}.map(t => anhTraLoi(t.numbers ? {{...t, numbers: new Map(t.numbers)}} : t))));")
    out = subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout
    return json.loads(out)


def ma_co_anh(kc: bool) -> str:
    """Một mã bài loại 'một nơi' có ảnh (kc như yêu cầu) — dò ngược khoá băm của anhBai.js bằng danh sách bài của build record."""
    rec = json.loads((SRC.parents[1] / "data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json").read_text(encoding="utf-8"))
    ids = [s if isinstance(s, str) else s["path"] for s in (rec.get("corpus", {}).get("sources") or rec["sources"])]
    js = (f"import {{ anhCuaBai }} from '{(SRC / 'anhBai.js').as_uri()}'; import {{ loaiCuaMa, LOAI_MOT_NOI }} from '{(SRC / 'anhTraLoi.js').as_uri()}';\n"
          f"const ids = {json.dumps(ids, ensure_ascii=False)};\n"
          f"console.log(ids.find(i => {{ const a = anhCuaBai(i); return a && !!a.kc === {str(kc).lower()} && LOAI_MOT_NOI.has(loaiCuaMa(i)); }}) ?? '');")
    return subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout.strip()


@pytest.mark.skipif(NODE is None, reason="cần node (giao diện build bằng node)")
def test_one_image_only_for_a_single_place_answer_from_the_corpus():
    co, kc = ma_co_anh(False), ma_co_anh(True)
    assert co and kc
    goc = {"phase": "done", "outcome": "success", "tuChoiKho": False, "web": None, "lich": None, "lichV2": None, "clarify": None,
           "suaThe": None, "sources": [{"bai_id": co, "title": "Bài A"}, {"bai_id": co, "title": "Bài A"}]}
    ca = [goc,
          {**goc, "sources": [{"bai_id": co, "title": "Bài A"}, {"bai_id": "x/y/khac.md", "title": "Bài B"}]},  # ≥ 2 bài
          {**goc, "sources": [{"bai_id": kc, "title": "Bài K"}]},  # ảnh "không chắc"
          {**goc, "tuChoiKho": True}, {**goc, "outcome": "out_of_scope"}, {**goc, "web": {"outcome": "co_muc"}},
          {**goc, "lichV2": {}}, {**goc, "phase": "streaming"}, {**goc, "sources": []},
          {**goc, "sources": [{"bai_id": "foods/tong_quan.md", "title": "Tổng quan"}]},  # bài gốc lĩnh vực
          {**goc, "sources": [{"bai_id": "travel/tickets/ve.md", "title": "Vé"}]}]  # loại không phải một nơi
    kq = chay(ca)
    assert kq[0] == [{"anh": kq[0][0]["anh"], "baiId": co, "ten": "Bài A"}] and kq[0][0]["anh"]  # một bài ⇒ như luật cũ (T1)
    assert kq[1:] == [[]] * (len(ca) - 1)


def ma_co_anh_n(n: int) -> list[str]:
    """n mã bài 'một nơi' có ảnh chắc (dò ngược khoá băm như `ma_co_anh`)."""
    rec = json.loads((SRC.parents[1] / "data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json").read_text(encoding="utf-8"))
    ids = [s if isinstance(s, str) else s["path"] for s in (rec.get("corpus", {}).get("sources") or rec["sources"])]
    js = (f"import {{ anhCuaBai }} from '{(SRC / 'anhBai.js').as_uri()}'; import {{ loaiCuaMa, LOAI_MOT_NOI }} from '{(SRC / 'anhTraLoi.js').as_uri()}';\n"
          f"const ids = {json.dumps(ids, ensure_ascii=False)};\n"
          f"console.log(JSON.stringify(ids.filter(i => {{ const a = anhCuaBai(i); return a && !a.kc && LOAI_MOT_NOI.has(loaiCuaMa(i)); }}).slice(0, {n})));")
    return json.loads(subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout)


@pytest.mark.skipif(NODE is None, reason="cần node (giao diện build bằng node)")
def test_several_images_only_for_cited_places_named_in_the_answer():
    """Plan 2026-11-15 (T2): ≥ 2 bài ⇒ chỉ bài đã trích + "một nơi" + ảnh chắc + tên ≥ 2 chữ có trong chữ; ≤ 3; theo thứ tự trích; có tên."""
    a, b, c, d = ma_co_anh_n(4)
    kc = ma_co_anh(True)
    goc = {"phase": "done", "outcome": "success", "tuChoiKho": False, "web": None, "lich": None, "lichV2": None, "clarify": None, "suaThe": None}
    S = lambda *xs: [{"bai_id": i, "title": t} for i, t in xs]
    ca = [
        {**goc, "text": "Quán Bê Ta mở muộn hơn Chùa Anpha.", "sources": S((a, "Chùa Anpha"), (b, "Quán Bê Ta"), (a, "Chùa Anpha"))},  # 2 ảnh, thứ tự trích
        {**goc, "text": "Chùa Anpha đẹp. [2]", "sources": S((a, "Chùa Anpha"), (b, "Quán Bê Ta"))},  # tên B không có trong chữ
        {**goc, "text": "chè ngon, chùa anpha gần đó", "sources": S((c, "Chè"), (a, "Chùa Anpha (Kim Long)"))},  # tên 1 chữ ⇒ bỏ; ngoặc bỏ khi khớp
        {**goc, "text": "Chùa Anpha và Quán Ka", "sources": S((a, "Chùa Anpha"), (kc, "Quán Ka"))},  # ảnh không chắc ⇒ bỏ
        {**goc, "text": "Một Hai, Ba Bốn, Năm Sáu, Bảy Tám", "sources": S((a, "Một Hai"), (b, "Ba Bốn"), (c, "Năm Sáu"), (d, "Bảy Tám"))},  # ≤ 3
        {**goc, "text": "Chùa Anpha và Vé Tham Quan", "sources": S((a, "Chùa Anpha"), ("travel/tickets/ve.md", "Vé Tham Quan"))},  # loại không phải một nơi
        {**goc, "web": {"outcome": "co_muc"}, "text": "Chùa Anpha, Quán Bê Ta", "sources": S((a, "Chùa Anpha"), (b, "Quán Bê Ta"))},  # có mục web ⇒ không ảnh
        {**goc, "text": "Quán Bê Ta [1] rồi Chùa Anpha [2]", "numbers": [["2", 1], ["1", 2]],  # thứ tự như dòng Nguồn (numbers), không theo id
         "sources": [{"id": 1, "bai_id": a, "title": "Chùa Anpha"}, {"id": 2, "bai_id": b, "title": "Quán Bê Ta"}]},
    ]
    kq = chay(ca)
    assert [[x["baiId"] for x in k] for k in kq] == [[a, b], [a], [a], [a], [a, b, c], [a], [], [b, a]]
    assert kq[0][1]["ten"] == "Quán Bê Ta" and all(x["anh"] for k in kq for x in k)
