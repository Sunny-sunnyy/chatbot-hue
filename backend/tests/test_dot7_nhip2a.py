"""Unit test offline (0 USD) cho Đợt 7 Nhịp 2A: Mũi 2.2 (H2.2a), Mũi 2.3 (H2.3b + reasoning low + timeout 30s), Cụm 3 (A0 + doi_chieu_canh_tranh) và 2 minor."""
from __future__ import annotations

import asyncio
import io
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from core.settings_loader import load_settings
from llm import full_corpus_prompt as fp
from llm import goi_y_luu_tru as gylt
from llm import luu_tru_lich as ltl
from llm import nhan_anh as na
from llm import slide_designer as sd
from llm import thoi_tiet as tt
from llm.assistant import AssistantFlags
from test_dot5a_slide_designer import _lich_day_du, _plan_tu_canonical


def _jpeg_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (64, 48), (180, 90, 60)).save(buf, format="JPEG")
    return buf.getvalue()


def test_mui_2_2_sua_lich_gpt6_va_giu_nguyen_bien_the_cu():
    bo = fp.SUA_LICH_LOI_DAN_TOI_HOI_BO
    assert "cach_toi" in bo and "hoi_them" in bo and "chua_ho_tro" in bo
    assert "sang / chieu / toi" in bo and "không tự chọn" in bo.casefold()
    # Các biến thể cờ cũ giữ nguyên không bị ghi đè
    assert "cach_toi" not in fp.SUA_LICH_LOI_DAN_TOI_HOI
    assert "hoi_them" not in fp.SUA_LICH_LOI_DAN_CHT
    assert fp.SUA_LICH_LOI_DAN.startswith("Bạn đọc câu người dùng")


def test_mui_2_3_slide_designer_low_timeout_30_va_h23b_separate_retry():
    s = load_settings(validate_private_paths=False)
    assert s["slide_designer_cfg"]["reasoning_effort"] == "low"
    assert s["slide_designer_cfg"]["timeout_seconds"] == 30
    flags = AssistantFlags.from_settings(s)
    assert flags.slide_designer_cfg["reasoning_effort"] == "low"
    assert flags.slide_designer_cfg["timeout_seconds"] == 30

    canonical = _lich_day_du(2)
    long_copy = "Đoạn mô tả quá dài để bắt buộc vòng 1 bị lỗi tràn chữ và chạy retry tách message. " * 6
    plan_tran = _plan_tu_canonical(canonical, short_copy_override=long_copy)
    plan_gon = _plan_tu_canonical(canonical, short_copy_override="Ngắn gọn chuẩn.")

    seen_calls = []

    class FakeResponses:
        def __init__(self):
            self.n = 0

        async def parse(self, **kwargs):
            seen_calls.append(kwargs)
            out = plan_tran if self.n == 0 else plan_gon
            self.n += 1
            return SimpleNamespace(
                output_parsed=out,
                usage=SimpleNamespace(
                    input_tokens=1500,
                    output_tokens=250,
                    input_tokens_details=SimpleNamespace(cached_tokens=1200, cache_write_tokens=0),
                ),
            )

    res = asyncio.run(
        sd.thiet_ke_slide(
            canonical,
            cfg={"model": "gpt-6-luna", "max_retries": 1, "fallback_code_only": True},
            client=SimpleNamespace(responses=FakeResponses()),
            use_llm=True,
        )
    )
    assert res.used_llm is True and res.retries == 1 and len(seen_calls) == 2
    assert seen_calls[0]["reasoning"] == {"effort": "low"}
    assert seen_calls[0]["instructions"] == sd.SLIDE_DESIGNER_INSTRUCTIONS
    # H2.3b: giữ nguyên messages[0] tĩnh từ vòng 1 sang vòng 2, chỉ nối user message lỗi ở phần tử thứ 2
    assert len(seen_calls[0]["input"]) == 1 and seen_calls[0]["input"][0]["role"] == "user"
    assert len(seen_calls[1]["input"]) == 2
    assert seen_calls[1]["input"][0] == seen_calls[0]["input"][0]
    assert seen_calls[1]["input"][1]["role"] == "user"
    assert "tràn chữ" in seen_calls[1]["input"][1]["content"]


def test_cum_3_a0_static_first_va_doi_chieu_canh_tranh():
    s = load_settings(validate_private_paths=False)
    assert s["anh"]["che_do_tu_choi"] == "mac_dinh"
    assert set(na.CHE_DO_TU_CHOI) == {"mac_dinh", "confidence_gate", "doi_chieu_mau", "doi_chieu_canh_tranh"}

    ds = [
        {"id": "dai_noi", "ten": "Đại Nội Huế", "ten_khac": ["Hoàng Thành Huế"]},
        {"id": "lang_tu_duc", "ten": "Lăng Tự Đức", "ten_khac": []},
        {"id": "cau_truong_tien", "ten": "Cầu Trường Tiền", "ten_khac": []},
    ]
    jpg = _jpeg_bytes()
    msgs = na.dau_vao(jpg, ds)
    assert msgs[0]["role"] == "developer" and msgs[0]["content"].startswith("Danh sách:\n")
    assert msgs[1]["role"] == "user" and msgs[1]["content"][0]["detail"] == "auto"

    gen = SimpleNamespace(responses_model="gpt-6-luna")
    ag_md = na.tao_agent(gen, ds, che_do_tu_choi="mac_dinh")
    assert ag_md.instructions == na.NHAN_ANH_INSTRUCTIONS
    assert (ag_md.model_settings.extra_args or {}).get("prompt_cache_key") == na.NHAN_ANH_CACHE_KEY_MD

    ag_ct = na.tao_agent_doi_chieu_canh_tranh(gen)
    assert ag_ct.output_type is na.DoiChieuCanhTranhOutput
    assert (ag_ct.model_settings.extra_args or {}).get("prompt_cache_key") == na.NHAN_ANH_CACHE_KEY_CT

    thu_muc_anh = Path(__file__).resolve().parents[2] / "frontend" / "public" / "anh"

    class FakeGen:
        def __init__(self, step1_ids, chon):
            self.step1_ids = step1_ids
            self.chon = chon
            self.calls = []

        async def _run(self, agent, items, call_log, timeout):
            self.calls.append((agent, items))
            if len(self.calls) == 1:
                return SimpleNamespace(final_output=SimpleNamespace(ung_vien=self.step1_ids, khong_nhan_ra=False))
            return SimpleNamespace(final_output=na.DoiChieuCanhTranhOutput(chon=self.chon, ly_do_ngan="So sánh góc nhìn"))

    # chon="A": giữ ứng viên bước 1; chon="B" (khi B nằm trong ung_vien): đôn B lên đầu; chon="khac": loại bỏ []
    g_a = FakeGen(["dai_noi", "lang_tu_duc"], "A")
    res_a = asyncio.run(na.doan_ten(g_a, ag_md, jpg, ds, SimpleNamespace(calls=[]), 15.0, che_do_tu_choi="doi_chieu_canh_tranh", doi_chieu_agent=ag_ct, thu_muc_anh=thu_muc_anh))
    assert [u["id"] for u in res_a] == ["dai_noi", "lang_tu_duc"] and len(g_a.calls) == 2

    g_b = FakeGen(["dai_noi", "lang_tu_duc"], "B")
    res_b = asyncio.run(na.doan_ten(g_b, ag_md, jpg, ds, SimpleNamespace(calls=[]), 15.0, che_do_tu_choi="doi_chieu_canh_tranh", doi_chieu_agent=ag_ct, thu_muc_anh=thu_muc_anh))
    assert [u["id"] for u in res_b] == ["lang_tu_duc", "dai_noi"]

    g_k = FakeGen(["dai_noi"], "khac")
    res_k = asyncio.run(na.doan_ten(g_k, ag_md, jpg, ds, SimpleNamespace(calls=[]), 15.0, che_do_tu_choi="doi_chieu_canh_tranh", doi_chieu_agent=ag_ct, thu_muc_anh=thu_muc_anh))
    assert res_k == [] and len(g_k.calls) == 2


def test_minor_nhan_noi_hang_co_dau_va_an_toan_gui_xe_cau_dai():
    bang_1sao = {"co_so": [{"ten": "Nhà nghỉ Mẫu", "khu": ltl.KHU_TAY, "xep_hang": "1 sao", "dia_chi": "1 Kim Long", "nguon": "Cục DL"}]}
    txt_noi, data_noi = gylt.ket_qua_co_kieu(bang_1sao, None, khu="phia_tay", hang_sao="vua")
    assert data_noi["da_noi_hang"] is True and data_noi["ghi_chu_noi_hang"] == "Đã nới hạng vì khu vực chưa có hạng vừa."
    assert "hạng vừa" in txt_noi and "hang vua" not in txt_noi

    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Gửi xe qua đêm ở phố đi bộ Nguyễn Đình Chiểu có an toàn không?", ()) is False
    assert tt.co_dau_hieu_thoi_tiet_hoac_nguy_hiem("Gửi xe ở Huế, trời có bão an toàn không?", ()) is True
