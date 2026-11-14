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
          f"console.log(JSON.stringify({json.dumps(turns, ensure_ascii=False)}.map(t => anhTraLoi(t))));")
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
    assert kq[0] == {"anh": kq[0]["anh"], "baiId": co, "ten": "Bài A"} and kq[0]["anh"]
    assert kq[1:] == [None] * (len(ca) - 1)
