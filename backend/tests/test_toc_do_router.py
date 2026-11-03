"""Thí nghiệm tốc độ #1 (plan `docs/superpowers/plans/2026-11-03-phase-9-toc-do-dinh-tuyen-plan.md`; bản A duyệt ghi ở CURRENT_HANDOFF):
cờ `assistant.router_reasoning_effort` chỉ đổi trường `reasoning` của lần định tuyến; `null` ⇒ cấu hình gửi model như B1. Không gọi API."""
import copy
import dataclasses

from openai import AsyncOpenAI

from core.settings_loader import load_settings
from llm.generator_openai_full_corpus import ROUTER_MAX_OUTPUT_TOKENS, OpenAIFullCorpusGenerator


def build(effort):
    return OpenAIFullCorpusGenerator(client=AsyncOpenAI(api_key="test-not-used"), model="gpt-6-luna", router_reasoning_effort=effort)


def test_null_flag_keeps_router_settings_of_b1():
    gen = build(None)
    for agent in (gen.router_agent, gen.router_history_agent, *gen.router_search_agents.values()):
        s = agent.model_settings
        assert s.reasoning is None and (s.max_tokens, s.include_usage, s.store) == (ROUTER_MAX_OUTPUT_TOKENS, True, False)
    assert gen.answer_agent.model_settings.reasoning is None  # lần trả lời không đổi


def test_effort_only_changes_reasoning_on_router_agents():
    base, low = build(None), build("none")
    for a, b in ((base.router_agent, low.router_agent), (base.router_history_agent, low.router_history_agent)):
        assert b.model_settings.reasoning.effort == "none"
        assert dataclasses.replace(b.model_settings, reasoning=None) == a.model_settings and a.instructions == b.instructions
    assert low.answer_agent.model_settings == base.answer_agent.model_settings
    assert low.chat_agent.model_settings == base.chat_agent.model_settings


def test_flag_read_from_settings_edge():
    settings = copy.deepcopy(load_settings(validate_private_paths=False))
    assert settings["assistant"]["router_reasoning_effort"] is None  # mặc định chạy thật: không gửi
