"""Lớp mỏng `llm.openai_goi_lai.OpenAIGoiLaiModel` (23/11/2026) — 0 USD: lỗi do test dựng, KHÔNG gọi OpenAI (client trỏ một cổng đóng trên chính máy;
lớp cha của SDK được thay bằng kịch bản). Vì sao có lớp này: bản deploy chạy đường OpenAI; lỗi gọi model trước đây chỉ để lại tên lớp `GenerationError`
trong log (không đếm được 500 / 429 / rớt mạng), và một lỗi 5xx thoáng qua làm hỏng cả lượt. Đề: 5xx / lỗi kết nối TRƯỚC sự kiện đầu ⇒ gọi lại một
lần; hai lần liền ⇒ lỗi như cũ; hết giờ, 4xx ⇒ không gọi lại; lỗi SAU khi đã có sự kiện đi ra ⇒ không gọi lại."""
import asyncio
import logging

import httpx
import openai
import pytest
from agents import OpenAIResponsesModel
from openai import AsyncOpenAI

from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.openai_goi_lai import OpenAIGoiLaiModel, goi_lai_duoc
from test_openai_full_corpus_generator import openai_settings

YEU_CAU = httpx.Request("POST", "http://127.0.0.1:9/v1/responses")


def _ma(status: int) -> openai.APIStatusError:
    lop = openai.InternalServerError if status >= 500 else openai.RateLimitError if status == 429 else openai.AuthenticationError
    return lop("lỗi dựng sẵn", response=httpx.Response(status, request=YEU_CAU), body=None)


KET_NOI, HET_GIO = openai.APIConnectionError(request=YEU_CAU), openai.APITimeoutError(request=YEU_CAU)


@pytest.fixture
def kich_ban(monkeypatch):
    """Thay hai hàm của LỚP CHA bằng kịch bản: mỗi lần gọi lấy một mục — lỗi thì ném; lời gọi thường trả mục đó; stream phát từng phần tử, gặp lỗi thì ném."""
    ghi = {"thuong": [], "stream": [], "so_lan": 0}

    async def get_response(self, *a, **k):
        ghi["so_lan"] += 1
        muc = ghi["thuong"].pop(0)
        if isinstance(muc, BaseException):
            raise muc
        return muc

    async def stream_response(self, *a, **k):
        ghi["so_lan"] += 1
        for x in ghi["stream"].pop(0):
            if isinstance(x, BaseException):
                raise x
            yield x

    monkeypatch.setattr(OpenAIResponsesModel, "get_response", get_response)
    monkeypatch.setattr(OpenAIResponsesModel, "stream_response", stream_response)
    return ghi


def _model() -> OpenAIGoiLaiModel:
    return OpenAIGoiLaiModel(model="gpt-thu", openai_client=AsyncOpenAI(api_key="khong-dung-key-that", base_url="http://127.0.0.1:9/v1", max_retries=0))


def _doc(model):
    async def chay():
        return [x async for x in model.stream_response()]
    return asyncio.run(chay())


def test_which_errors_are_retried():
    assert goi_lai_duoc(_ma(500)) and goi_lai_duoc(_ma(503)) and goi_lai_duoc(KET_NOI)
    assert not goi_lai_duoc(HET_GIO) and not goi_lai_duoc(_ma(429)) and not goi_lai_duoc(_ma(401)) and not goi_lai_duoc(ValueError("x"))


@pytest.mark.parametrize("loi", [_ma(503), KET_NOI])
def test_a_transient_error_is_retried_once_and_logged(kich_ban, caplog, loi):
    kich_ban["thuong"] = [loi, "phản hồi"]
    with caplog.at_level(logging.WARNING, logger="llm.full_corpus"):
        assert asyncio.run(_model().get_response()) == "phản hồi"
    assert kich_ban["so_lan"] == 2
    dong = [r.getMessage() for r in caplog.records]
    assert dong == [f"openai_goi_lai loai={type(loi).__name__} status={getattr(loi, 'status_code', None)}"]


def test_two_failures_in_a_row_surface_the_error_with_its_status_in_the_log(kich_ban, caplog):
    kich_ban["thuong"] = [_ma(500), _ma(502)]
    with caplog.at_level(logging.WARNING, logger="llm.full_corpus"), pytest.raises(openai.InternalServerError):
        asyncio.run(_model().get_response())
    assert kich_ban["so_lan"] == 2
    assert [r.getMessage() for r in caplog.records] == ["openai_goi_lai loai=InternalServerError status=500", "openai_loi loai=InternalServerError status=502"]


@pytest.mark.parametrize("loi,lop", [(HET_GIO, openai.APITimeoutError), (_ma(429), openai.RateLimitError), (_ma(401), openai.AuthenticationError)])
def test_timeouts_and_4xx_are_not_retried_but_are_logged(kich_ban, caplog, loi, lop):
    kich_ban["thuong"] = [loi, "không được tới đây"]
    with caplog.at_level(logging.WARNING, logger="llm.full_corpus"), pytest.raises(lop):
        asyncio.run(_model().get_response())
    assert kich_ban["so_lan"] == 1
    assert [r.getMessage() for r in caplog.records] == [f"openai_loi loai={lop.__name__} status={getattr(loi, 'status_code', None)}"]


def test_stream_retries_only_before_the_first_event(kich_ban):
    kich_ban["stream"] = [[_ma(503)], ["a", "b"]]  # lỗi lúc mở yêu cầu, chưa sự kiện nào ⇒ gọi lại, người đọc thấy đúng một dãy
    assert _doc(_model()) == ["a", "b"] and kich_ban["so_lan"] == 2
    kich_ban["so_lan"] = 0
    kich_ban["stream"] = [["a", _ma(503)], ["không được tới đây"]]  # đã phát "a" ⇒ không gọi lại (không phát trùng chữ)
    da_nhan = []

    async def chay():
        async for x in _model().stream_response():
            da_nhan.append(x)
    with pytest.raises(openai.InternalServerError):
        asyncio.run(chay())
    assert da_nhan == ["a"] and kich_ban["so_lan"] == 1
    kich_ban["so_lan"] = 0
    kich_ban["stream"] = [[_ma(500)], [_ma(500)]]  # hai lần liền ⇒ lỗi như cũ
    with pytest.raises(openai.InternalServerError):
        _doc(_model())
    assert kich_ban["so_lan"] == 2
    kich_ban["so_lan"] = 0
    kich_ban["stream"] = [[HET_GIO], ["không được tới đây"]]
    with pytest.raises(openai.APITimeoutError):
        _doc(_model())
    assert kich_ban["so_lan"] == 1


def test_the_openai_path_of_the_generator_uses_this_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "khong-dung-key-that")
    generator = OpenAIFullCorpusGenerator.from_environment(openai_settings())
    assert type(generator.responses_model) is OpenAIGoiLaiModel and generator.client.max_retries == 0
