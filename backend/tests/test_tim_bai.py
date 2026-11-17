"""Ô tìm trang Khám phá (`frontend/src/timBai.js`, hàm thuần) — chạy bằng node thật. Lỗi 16/11: tìm "lăng" ra các bài "làng…" trước, "chè" ra
"Điện Hòn Chén" ⇒ bài khớp đúng dấu đứng trước, bài chỉ khớp khi bỏ dấu đứng sau; không bỏ bài nào."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "frontend/src"
NODE = shutil.which("node")
BAI = ["Hội vật làng Sình", "Lăng Tự Đức", "Làng hương Thủy Xuân", "Điện Hòn Chén", "Chè Hẻm Huế", "Lăng Minh Mạng", "Chùa Thiên Mụ", "Đồi Vọng Cảnh"]


def tim(q: str) -> list[str]:
    js = (f"import {{ timBai }} from '{(SRC / 'timBai.js').as_uri()}';\n"
          f"const bai = {json.dumps([{'tieu_de': t} for t in BAI], ensure_ascii=False)};\n"
          f"console.log(JSON.stringify(timBai(bai, {json.dumps(q, ensure_ascii=False)}).map(b => b.tieu_de)));")
    return json.loads(subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout)


@pytest.mark.skipif(NODE is None, reason="cần node (giao diện build bằng node)")
def test_search_puts_exact_diacritics_first_and_keeps_loose_matches():
    assert tim("lăng") == ["Lăng Tự Đức", "Lăng Minh Mạng", "Hội vật làng Sình", "Làng hương Thủy Xuân"]   # đúng dấu trước, giữ "làng"
    assert tim("làng") == ["Hội vật làng Sình", "Làng hương Thủy Xuân", "Lăng Tự Đức", "Lăng Minh Mạng"]   # chiều ngược
    assert tim("chè") == ["Chè Hẻm Huế", "Điện Hòn Chén"]
    assert tim("lang") == ["Hội vật làng Sình", "Lăng Tự Đức", "Làng hương Thủy Xuân", "Lăng Minh Mạng"]   # gõ không dấu ⇒ thứ tự gốc
    assert tim("doi vong") == ["Đồi Vọng Cảnh"]                                                            # đ ⇒ d
    assert tim("  THIÊN MỤ ") == ["Chùa Thiên Mụ"]                                                         # hoa / thường, khoảng trắng
    assert tim("lăng") == tim("lăng")                                                                 # chữ tổ hợp (NFD) ⇒ như NFC
    assert tim("xyzq") == []
    assert tim("") == BAI and tim("   ") == BAI
