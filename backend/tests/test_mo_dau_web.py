"""Khi kho thiếu mà mục web có nội dung (`frontend/src/moDauWeb.js`, hàm thuần) — chạy bằng node thật. Server giữ câu từ chối chuẩn;
giao diện bỏ câu từ chối chuẩn khi `web.outcome == "co_muc"` để hiện thẳng khung "Từ web (chưa kiểm)"."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

SRC = Path(__file__).resolve().parents[2] / "frontend/src"
NODE = shutil.which("node")


def chay(ca: list) -> list:
    js = (f"import {{ moDauWeb, CAU_TU_CHOI }} from '{(SRC / 'moDauWeb.js').as_uri()}';\n"
          f"console.log(JSON.stringify([CAU_TU_CHOI, ...{json.dumps(ca, ensure_ascii=False)}.map(([t, w]) => moDauWeb(t, w))]));")
    return json.loads(subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True, check=True, timeout=30).stdout)


@pytest.mark.skipif(NODE is None, reason="cần node (giao diện build bằng node)")
def test_refusal_lead_hidden_only_when_web_section_has_content():
    T = INSUFFICIENT_ANSWER
    co = {"outcome": "co_muc"}
    ca = [[T, co], [f"{T}\n\nTư liệu chưa có thông tin về: giờ mở cửa.", co], [T, {"outcome": "web_rong"}], [T, {"outcome": "thien_tai"}],
          [T, {"outcome": "chua_xac_minh"}], [T, None], ["Chùa Thiên Mụ mở cửa cả ngày [1].", co], [f"Có thể. {T}", co], [f"  {T}", co]]
    tu_choi, *ra = chay(ca)
    assert tu_choi == T  # chuỗi của giao diện phải trùng câu chuẩn của server
    assert ra[0] == "" and ra[1] == "Tư liệu chưa có thông tin về: giờ mở cửa."
    assert ra[2:6] == [T, T, T, T]  # web trắng / câu cố định / không có mục web ⇒ giữ câu cũ
    assert ra[6] == ca[6][0] and ra[7] == ca[7][0]  # không phải câu mở đầu ⇒ không đổi
    assert ra[8] == ""
