"""Lớp `Model` của OpenAI Agents SDK gọi Claude trên Amazon Bedrock (`POST /model/<mã>/invoke`, thân kiểu Anthropic Messages).

Vì sao có file này (21/11/2026): cổng kiểu OpenAI của Bedrock không phục vụ model này ⇒ không đổi `base_url` suông được. Lớp này DỊCH hai chiều
giữa dạng Responses mà SDK dùng (đầu vào: tin nhắn, `function_call`, `function_call_output`, ảnh; đầu ra: `Response`) và dạng Messages của Claude,
để chín agent của `OpenAIFullCorpusGenerator` giữ nguyên. Chỉ dùng khi `full_corpus_generation.provider: bedrock`.

Các giới hạn đã đo thật trên bộ khoá đang dùng (46 lời gọi sáng 21/11/2026) quyết định cách dịch:
- Không có quyền stream ⇒ `stream_response` gọi TRỌN rồi phát chữ một lần (stream giả).
- Khuôn đầu ra / công cụ có `maxItems`, `minimum`… bị trả 400 ⇒ gỡ các từ khoá ràng buộc khỏi schema GỬI ĐI; pydantic phía mình vẫn kiểm đủ.
- `tool_choice` chỉ nhận `auto` (kèm `disable_parallel_tool_use`); không gửi temperature / top_p.
- `max_tokens` là trường bắt buộc ⇒ luôn gửi mức tối đa của model lấy từ cấu hình (coi như không trần — User 19/11 và 21/11/2026); không agent nào
  đặt nhỏ hơn được.
- Mức suy luận luôn gửi RÕ: không gửi gì thì Claude tự suy luận cỡ "high". `none` ⇒ `thinking: between_tools` (đo: 0 token suy luận; `effort: none`
  và `thinking: disabled` đều 400); `low | medium | high` ⇒ `thinking: adaptive` + `output_config.effort`.
- Khối suy luận (`thinking`) không cần gửi lại ở vòng công cụ kế ⇒ bỏ khỏi đầu ra, không cất chữ ký.
- Khuôn JSON ép đầu ra (`output_config.format`) gửi CÙNG công cụ làm Claude gọi công cụ mãi không viết (phát lại một thân yêu cầu đã có đủ kết quả
  công cụ: viết 0 / 30 lần ở mọi mức suy luận; bỏ khuôn: viết 14 / 14) ⇒ lượt vừa có công cụ vừa có khuôn KHÔNG gửi khuôn mà thêm một công cụ nội
  bộ `tra_loi` mang đúng khuôn đó; Claude gọi nó để nộp câu trả lời, lớp dịch đổi lời gọi ấy thành tin trả lời JSON cho SDK (`ANSWER_TOOL`).
  Cũng áp cho vòng mà mọi công cụ thật đã bị ẨN (hết lượt tìm) nhưng lịch sử của lượt đã có lời gọi công cụ: ép khuôn ở vòng đó làm Claude — vẫn
  muốn tìm tiếp — viết rác vào khuôn (phát lại 22 lần: `{"answer": "placeholder"}`, `"tim_kho"`, rỗng… 14 lần, đúng câu từ chối 8 lần; chỉ còn
  `tra_loi`: đúng câu từ chối 20 / 22, 0 rác kiểu đó).
"""
import datetime as dt
import hashlib
import hmac
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote

import httpx
from agents.items import ModelResponse
from agents.models.interface import Model
from agents.tool import FunctionTool
from agents.usage import Usage
from openai.types.responses import Response, ResponseCompletedEvent, ResponseTextDeltaEvent
from openai.types.responses.response_usage import InputTokensDetails, OutputTokensDetails

from core.schema import GenerationError

ANTHROPIC_VERSION = "bedrock-2023-05-31"
# Từ khoá ràng buộc Bedrock từ chối trong khuôn (đo 21/11: `maxItems`, `minimum` / `maximum` ⇒ 400; cả nhóm dưới đã gỡ ở lượt đo đạt).
UNSUPPORTED_SCHEMA_KEYS = frozenset({"maxItems", "minItems", "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
                                     "minLength", "maxLength", "pattern", "default"})
# Khoá mà GIÁ TRỊ là bảng tên ⇒ tên trong bảng không phải từ khoá schema (trường tên `default`, `pattern`… vẫn phải giữ).
NAME_MAP_KEYS = frozenset({"properties", "$defs", "definitions"})
AWS_IDENTIFIER = re.compile(r"arn:aws\S*|(?<!\d)\d{12}(?!\d)")  # không để ARN / mã tài khoản lọt vào lời lỗi ⇒ log
# Công cụ nội bộ để nộp câu trả lời có khuôn ở lượt có công cụ (xem đầu file). SDK không biết tới nó: không bao giờ được chạy như công cụ thật.
ANSWER_TOOL = "tra_loi"
ANSWER_TOOL_DESCRIPTION = ("Nộp câu trả lời cuối cùng cho người dùng. Gọi khi đã đủ thông tin để trả lời, hoặc khi không thể tìm thêm — kể cả khi câu trả lời "
                           "là câu từ chối theo lời dặn. Gọi đúng một lần, đặt toàn bộ câu trả lời vào tham số; không viết câu trả lời ra ngoài công cụ này.")
# Lịch sử hội thoại chỉ nhớ CÂU HỎI (câu trả lời cũ bị bỏ) ⇒ SDK gửi nhiều tin user liền nhau. Claude gộp các tin cùng vai liền nhau thành MỘT lượt, nên câu
# hỏi của lượt trước dính vào câu đang hỏi: định tuyến "chỉ xét tin nhắn cuối" nhìn thấy cả câu hỏi về Huế của lượt trước ⇒ câu "bạn còn nhớ tôi tên gì không"
# bị đưa sang trợ lý tra kho ⇒ trả lời đúng nhưng không có nguồn để trích ⇒ lỗi (bộ chuỗi 21/11: 2 / 2 lần trên bản chính; luna 0 vì OpenAI giữ các tin tách
# rời). Chèn một tin assistant giữ chỗ giữa hai câu hỏi của hai lượt để ranh giới lượt còn nguyên.
HISTORY_GAP = "(Câu trả lời của lượt này không được lưu trong lịch sử.)"
CODE_FENCE = re.compile(r"^```(?:json)?\s*(?P<body>.*?)\s*```$", re.DOTALL)
DATA_URL = re.compile(r"^data:(?P<media>[\w/+.-]+);base64,(?P<data>.+)$", re.DOTALL)


class BedrockError(GenerationError):
    """Lời gọi Bedrock hỏng: mã khác 200, lỗi mạng / hết giờ, hoặc không đọc được file khoá. Là `GenerationError` để MỌI nơi đọc (đường thường,
    đường stream của ô chat, lần viết câu của lịch) xếp nó vào nhóm "lỗi model" như `OpenAIError` — review C 21/11: lỗi trần trên đường stream
    làm lịch mất đường câu dự phòng. Lời lỗi KHÔNG chứa thân phản hồi 403 (thân đó có mã tài khoản / tên vai AWS — log không được có)."""


def strip_constraints(schema: Any) -> Any:
    """Bản sao schema đã gỡ các từ khoá ràng buộc Bedrock không nhận; cấu trúc, kiểu, `enum`, `required` giữ nguyên."""
    if isinstance(schema, list):
        return [strip_constraints(item) for item in schema]
    if not isinstance(schema, dict):
        return schema
    out = {}
    for key, value in schema.items():
        if key in NAME_MAP_KEYS and isinstance(value, dict):
            out[key] = {name: strip_constraints(sub) for name, sub in value.items()}
        elif key not in UNSUPPORTED_SCHEMA_KEYS:
            out[key] = strip_constraints(value)
    return out


def _content_blocks(content: Any) -> list[dict]:
    """Nội dung một tin user / assistant dạng Responses (chuỗi, hoặc danh sách phần `input_text` / `output_text` / `input_image`) ⇒ khối Claude.
    Chữ rỗng bị bỏ (Claude từ chối khối chữ rỗng)."""
    if isinstance(content, str):
        return [{"type": "text", "text": content}] if content else []
    blocks = []
    for part in content:
        kind = part.get("type")
        if kind in ("input_text", "output_text"):
            if part["text"]:
                blocks.append({"type": "text", "text": part["text"]})
        elif kind == "input_image":
            match = DATA_URL.match(part.get("image_url") or "")
            if match is None:
                raise ValueError("Bedrock model only accepts images as base64 data URLs")
            blocks.append({"type": "image", "source": {"type": "base64", "media_type": match["media"], "data": match["data"]}})
        else:
            raise ValueError(f"Unsupported content part for Bedrock model: {kind!r}")
    return blocks


def to_messages(input: "str | list[dict]") -> list[dict]:
    """Đầu vào của SDK ⇒ `messages` của Claude. Các mục liền nhau cùng vai gộp vào MỘT tin (Claude cần `tool_use` của một lượt nằm chung một tin
    assistant và `tool_result` nằm ở tin user ngay sau); `call_id` của SDK chính là `id` khối `tool_use` nên khớp lại được."""
    if isinstance(input, str):
        return [{"role": "user", "content": [{"type": "text", "text": input}]}]
    messages: list[dict] = []

    def add(role: str, blocks: list[dict]) -> None:
        if not blocks:
            return
        if messages and messages[-1]["role"] == role:
            messages[-1]["content"].extend(blocks)
        else:
            messages.append({"role": role, "content": list(blocks)})

    for item in input:
        kind = item.get("type")
        if kind == "function_call":
            add("assistant", [{"type": "tool_use", "id": item["call_id"], "name": item["name"], "input": json.loads(item["arguments"] or "{}")}])
        elif kind == "function_call_output":
            output = item["output"]
            add("user", [{"type": "tool_result", "tool_use_id": item["call_id"],
                          "content": output if isinstance(output, str) else json.dumps(output, ensure_ascii=False)}])
        elif kind in (None, "message") and item.get("role") in ("user", "assistant"):
            blocks = _content_blocks(item["content"])
            # hai CÂU HỎI liền nhau (không phải kết quả công cụ) là hai lượt khác nhau ⇒ giữ ranh giới lượt bằng một tin assistant giữ chỗ
            if (item["role"] == "user" and blocks and messages and messages[-1]["role"] == "user"
                    and all(block["type"] != "tool_result" for block in messages[-1]["content"])):
                messages.append({"role": "assistant", "content": [{"type": "text", "text": HISTORY_GAP}]})
            add(item["role"], blocks)
        else:
            raise ValueError(f"Unsupported input item for Bedrock model: {kind or item.get('role')!r}")
    return messages


def _has_tool_rounds(input: "str | list[dict]") -> bool:
    """Đầu vào của lời gọi đã mang lời gọi / kết quả công cụ của chính lượt chạy này (SDK gửi lại ở mỗi vòng)."""
    return not isinstance(input, str) and any(item.get("type") in ("function_call", "function_call_output") for item in input)


def build_body(system_instructions: str | None, input: "str | list[dict]", model_settings, tools: list, output_schema, max_tokens: int,
               reasoning_default: str) -> dict:
    """Thân yêu cầu `/invoke`. Bỏ qua các thứ chỉ có nghĩa với OpenAI (`store`, `include_usage`, `prompt_cache_key`, `max_tokens` của agent…).
    `reasoning_default` (`none | low | medium | high`): mức suy luận cho agent KHÔNG tự đặt; agent tự đặt (nhóm lịch: "low") giữ mức của nó."""
    body: dict = {"anthropic_version": ANTHROPIC_VERSION, "max_tokens": max_tokens, "messages": to_messages(input)}
    if system_instructions:
        body["system"] = system_instructions
    if tools:
        for tool in tools:
            if not isinstance(tool, FunctionTool):
                raise ValueError(f"Unsupported tool for Bedrock model: {type(tool).__name__}")
        body["tools"] = [{"name": tool.name, "description": tool.description, "input_schema": strip_constraints(tool.params_json_schema),
                          "strict": tool.strict_json_schema} for tool in tools]
        if model_settings.parallel_tool_calls is False:
            body["tool_choice"] = {"type": "auto", "disable_parallel_tool_use": True}
    output_config: dict = {}
    if output_schema is not None and not output_schema.is_plain_text():
        schema = strip_constraints(output_schema.json_schema())
        # khuôn + công cụ, hoặc vòng công cụ đã ẩn hết nhưng lượt này đã có lời gọi công cụ ⇒ nộp câu trả lời qua công cụ nội bộ, không ép khuôn
        if tools or _has_tool_rounds(input):
            body.setdefault("tools", []).append({"name": ANSWER_TOOL, "description": ANSWER_TOOL_DESCRIPTION, "input_schema": schema, "strict": True})
            body.setdefault("tool_choice", {"type": "auto", "disable_parallel_tool_use": True})
        else:
            output_config["format"] = {"type": "json_schema", "schema": schema}
    effort = getattr(model_settings.reasoning, "effort", None) or reasoning_default
    if effort == "none":
        body["thinking"] = {"type": "between_tools"}
    else:
        body["thinking"] = {"type": "adaptive"}
        output_config["effort"] = effort
    if output_config:
        body["output_config"] = output_config
    return body


def to_usage_dict(usage: dict) -> dict:
    """Usage của Claude ⇒ dạng Responses. Claude đếm phần đọc / ghi đệm NGOÀI `input_tokens`; OpenAI đếm TRONG ⇒ cộng lại để `call_entry` và
    `llm.pricing.cost_usd` (trừ phần đệm ra khỏi `input_tokens`) không đổi nghĩa. `output_tokens` của Claude đã gồm token suy luận."""
    cached = usage.get("cache_read_input_tokens") or 0
    cache_write = usage.get("cache_creation_input_tokens") or 0
    input_tokens = (usage.get("input_tokens") or 0) + cached + cache_write
    output_tokens = usage.get("output_tokens") or 0
    return {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens,
            "input_tokens_details": {"cached_tokens": cached, "cache_write_tokens": cache_write},
            "output_tokens_details": {"reasoning_tokens": (usage.get("output_tokens_details") or {}).get("thinking_tokens") or 0}}


def _wrap_plain_answer(text: str, schema: dict) -> str:
    """Đường lùi của `to_response`: Claude viết chữ thường thay vì gọi `ANSWER_TOOL`. Chữ đã là JSON đối tượng — kể cả nằm trong rào ```json … ```
    (review C 21/11: không gỡ rào thì người dùng thấy nguyên khối rào) — ⇒ dùng chính JSON đó (SDK kiểm khuôn như thường)."""
    fenced = CODE_FENCE.match(text.strip())
    for candidate in filter(None, (fenced and fenced["body"], text)):
        try:
            if isinstance(json.loads(candidate), dict):
                return candidate
        except ValueError:
            pass
    required, properties = schema.get("required") or [], schema.get("properties") or {}
    if len(properties) == 1 and required == list(properties) and properties[required[0]].get("type") == "string":
        return json.dumps({required[0]: text.strip()}, ensure_ascii=False)
    raise BedrockError("Bedrock: model không nộp câu trả lời theo khuôn (viết chữ thường thay vì gọi công cụ nộp câu trả lời)")


def to_response(message: dict, model: str, answer_schema: dict | None = None) -> Response:
    """Một Message của Claude ⇒ `Response` của SDK: các khối chữ thành MỘT tin assistant, mỗi `tool_use` thành một `function_call` (giữ `id` làm
    `call_id`), khối suy luận bỏ. `answer_schema` = khuôn đã gửi kèm công cụ nội bộ `ANSWER_TOOL` ở lời gọi này (None = không gửi). Khi có:
    - Claude gọi `ANSWER_TOOL` và KHÔNG gọi công cụ thật nào ⇒ tham số của nó (JSON đúng khuôn) là câu trả lời: thành tin assistant duy nhất, chữ dẫn
      đi kèm bị bỏ; gọi hai lần ⇒ lấy lần đầu.
    - Claude gọi `ANSWER_TOOL` CÙNG công cụ thật ⇒ chạy công cụ thật, bỏ `ANSWER_TOOL` của lượt đó (nó còn muốn tìm thêm; lượt sau nộp lại).
    - Claude không gọi công cụ nào mà viết chữ thường (không ép `tool_choice` được) ⇒ đường lùi: khuôn chỉ có một trường chuỗi bắt buộc thì bọc chữ
      vào trường đó; khuôn khác ⇒ `BedrockError` (nhóm lỗi model). SDK không bao giờ thấy `ANSWER_TOOL`."""
    blocks = message["content"]
    real_calls = [block for block in blocks if block["type"] == "tool_use" and block["name"] != ANSWER_TOOL]
    answer = next((block["input"] for block in blocks if block["type"] == "tool_use" and block["name"] == ANSWER_TOOL), None)
    text = "".join(block["text"] for block in blocks if block["type"] == "text")
    if answer is not None and not real_calls:
        text = json.dumps(answer, ensure_ascii=False)
    elif answer_schema is not None and not real_calls and text:
        text = _wrap_plain_answer(text, answer_schema)
    output: list[dict] = []
    if text:
        output.append({"type": "message", "id": message["id"], "role": "assistant", "status": "completed",
                       "content": [{"type": "output_text", "text": text, "annotations": []}]})
    for block in real_calls:
        output.append({"type": "function_call", "id": block["id"], "call_id": block["id"], "name": block["name"],
                       "arguments": json.dumps(block["input"], ensure_ascii=False), "status": "completed"})
    return Response.model_validate({"id": message["id"], "created_at": 0, "model": model, "object": "response", "output": output,
                                    "parallel_tool_calls": False, "tool_choice": "auto", "tools": [], "status": "completed",
                                    "usage": to_usage_dict(message.get("usage") or {})})


def sign_headers(method: str, host: str, path: str, body: bytes, region: str, creds: dict, now: dt.datetime) -> dict:
    """Header đã ký AWS SigV4 (dịch vụ `bedrock`) bằng thư viện chuẩn — không thêm gói. `creds`: `accessKeyId`, `secretAccessKey`, `sessionToken`."""
    amz_date, day = now.strftime("%Y%m%dT%H%M%SZ"), now.strftime("%Y%m%d")
    headers = {"accept": "application/json", "content-type": "application/json", "host": host, "x-amz-date": amz_date,
               "x-amz-security-token": creds["sessionToken"]}
    signed = ";".join(sorted(headers))
    canonical = "\n".join([method, quote(quote(path, safe="/"), safe="/%"), "", "".join(f"{name}:{headers[name].strip()}\n" for name in sorted(headers)),
                           signed, hashlib.sha256(body).hexdigest()])
    scope = f"{day}/{region}/bedrock/aws4_request"
    to_sign = "\n".join(["AWS4-HMAC-SHA256", amz_date, scope, hashlib.sha256(canonical.encode()).hexdigest()])
    key = ("AWS4" + creds["secretAccessKey"]).encode()
    for part in (day, region, "bedrock", "aws4_request"):
        key = hmac.new(key, part.encode(), hashlib.sha256).digest()
    signature = hmac.new(key, to_sign.encode(), hashlib.sha256).hexdigest()
    headers["authorization"] = f"AWS4-HMAC-SHA256 Credential={creds['accessKeyId']}/{scope}, SignedHeaders={signed}, Signature={signature}"
    return headers


class BedrockClaudeModel(Model):
    """Một model Claude trên Bedrock cho Agents SDK. File khoá tạm được đọc lại MỖI lời gọi (khoá được làm mới bên ngoài); không in / log nội dung."""

    provider = "bedrock"  # `CallLog` đọc để chọn bảng giá (`llm.pricing`)

    def __init__(self, *, model: str, region: str, creds_file: str, timeout: float, max_tokens: int, reasoning_default: str) -> None:
        self.model = model
        self.region = region
        self.creds_file = Path(creds_file)
        self.max_tokens = max_tokens
        self.reasoning_default = reasoning_default
        self.host = f"bedrock-runtime.{region}.amazonaws.com"
        self.http = httpx.AsyncClient(timeout=timeout)

    async def _invoke(self, body: dict) -> Response:
        raw = json.dumps(body, ensure_ascii=False).encode()
        path = f"/model/{self.model}/invoke"
        try:
            creds = json.loads(self.creds_file.read_text(encoding="utf-8"))
            headers = sign_headers("POST", self.host, path, raw, self.region, creds, dt.datetime.now(dt.timezone.utc))
        except (OSError, ValueError, KeyError) as exc:  # chỉ tên lớp lỗi — lời lỗi gốc có thể mang đường dẫn file khoá
            raise BedrockError(f"Không đọc được file khoá Bedrock: {type(exc).__name__}") from None
        try:
            reply = await self.http.post(f"https://{self.host}{path}", content=raw, headers=headers)
        except httpx.HTTPError as exc:  # hết giờ, rớt mạng
            raise BedrockError(f"Bedrock request failed: {type(exc).__name__}") from exc
        if reply.status_code == 403:
            raise BedrockError("Bedrock HTTP 403: khoá Bedrock bị từ chối hoặc đã hết hạn")
        if reply.status_code != 200:
            raise BedrockError(f"Bedrock HTTP {reply.status_code}: {AWS_IDENTIFIER.sub('<aws>', reply.text)[:300]}")
        answer_schema = next((tool["input_schema"] for tool in body.get("tools", ()) if tool["name"] == ANSWER_TOOL), None)
        return to_response(reply.json(), self.model, answer_schema)

    async def get_response(self, system_instructions, input, model_settings, tools, output_schema, handoffs, tracing, *,
                           previous_response_id=None, conversation_id=None, prompt=None) -> ModelResponse:
        response = await self._invoke(build_body(system_instructions, input, model_settings, tools, output_schema, self.max_tokens, self.reasoning_default))
        usage = response.usage
        return ModelResponse(
            output=response.output,
            usage=Usage(requests=1, input_tokens=usage.input_tokens, output_tokens=usage.output_tokens, total_tokens=usage.total_tokens,
                        input_tokens_details=InputTokensDetails.model_validate(usage.input_tokens_details.model_dump()),
                        output_tokens_details=OutputTokensDetails.model_validate(usage.output_tokens_details.model_dump())),
            response_id=response.id,
        )

    async def stream_response(self, system_instructions, input, model_settings, tools, output_schema, handoffs, tracing, *,
                              previous_response_id=None, conversation_id=None, prompt=None):
        """Stream GIẢ: gọi trọn, phát chữ một lần rồi `response.completed` (sự kiện duy nhất SDK bắt buộc). Lượt có gọi công cụ KHÔNG phát chữ:
        nơi đọc (`assistant.py`) ghép mọi mảnh chữ của cả lượt chạy thành một chuỗi JSON câu trả lời."""
        response = await self._invoke(build_body(system_instructions, input, model_settings, tools, output_schema, self.max_tokens, self.reasoning_default))
        items = response.output
        if items and all(item.type == "message" for item in items):
            yield ResponseTextDeltaEvent.model_validate({"type": "response.output_text.delta", "item_id": items[0].id, "output_index": 0,
                                                         "content_index": 0, "delta": items[0].content[0].text, "sequence_number": 0, "logprobs": []})
        yield ResponseCompletedEvent.model_validate({"type": "response.completed", "response": response.model_dump(), "sequence_number": 1})

    async def close(self) -> None:
        await self.http.aclose()
