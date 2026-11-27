"""Regression tests (0 USD, offline) proving async retrieval does not block event loop and dense runner serializes encode() safely."""

from __future__ import annotations

import asyncio
from pathlib import Path
import threading
import time
from types import SimpleNamespace

import numpy as np

from core.schema import RetrievedDocument
from embedding.full_corpus import DENSE_MODEL_SPECS, FullCorpusDenseRunner
from llm.assistant import AnswerTrace, search_into_trace
from retrieval.full_corpus import RetrievalResult, RetrievalTrace


def test_full_corpus_dense_runner_serializes_concurrent_encode(tmp_path: Path):
    spec = DENSE_MODEL_SPECS[0]  # e5-small-384
    snap = tmp_path / spec.revision
    snap.mkdir()

    active = 0
    max_active = 0
    counter_lock = threading.Lock()

    class _FakeModel:
        def encode(self, prepared, **_kw):
            nonlocal active, max_active
            with counter_lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.02)
            with counter_lock:
                active -= 1
            vec = np.zeros((len(prepared), spec.dimension), dtype=np.float32)
            vec[:, 0] = 1.0
            return vec

    runner = FullCorpusDenseRunner(spec, snap)
    runner._model = _FakeModel()

    async def _run():
        return await asyncio.gather(
            *[asyncio.to_thread(runner.embed_queries, [f"câu hỏi {i}"]) for i in range(6)]
        )

    out = asyncio.run(_run())
    assert len(out) == 6
    assert all(len(batch) == 1 and len(batch[0]) == spec.dimension for batch in out)
    assert max_active == 1


def test_search_into_trace_offloads_blocking_search_and_context_builder():
    doc = RetrievedDocument(
        id="a#0",
        score=0.9,
        text="Đại Nội Huế mở cửa hằng ngày.",
        metadata={
            "source": "heritages/dai-noi.md",
            "title": "Đại Nội Huế",
            "heading_path": ["Giờ mở cửa"],
            "evidence_parts": [{"role": "body", "start": 0, "end": 28, "text": "Đại Nội Huế mở cửa hằng ngày."}],
            "domain": "heritages",
        },
    )
    fake_trace = RetrievalTrace(
        candidate_id="e5-small-384",
        collection_name="test",
        retrieval_treatment="dense_bm25_rrf",
        reranker="none",
        counts={"dense": 1, "final": 1},
        timings_ms={"dense_ms": 50.0, "total_ms": 55.0},
        stages={},
        rerank_status="not_applicable",
        anomalies=(),
        classification="PASS",
    )

    class _SlowService:
        def search(self, _q: str) -> RetrievalResult:
            time.sleep(0.15)
            return RetrievalResult(documents=[doc], trace=fake_trace)

    class _SlowBuilder:
        def build(self, *_args, **_kw):
            time.sleep(0.10)
            return SimpleNamespace(text="[Nguồn 1]\nTiêu đề: Đại Nội Huế", sources=(object(),), input_tokens=10, document_ids=("a#0",))

    async def _measure():
        ticks = 0

        async def _heartbeat():
            nonlocal ticks
            while True:
                await asyncio.sleep(0.02)
                ticks += 1

        hb = asyncio.create_task(_heartbeat())
        try:
            trace = AnswerTrace()
            await search_into_trace(
                ["Đại Nội"],
                cau_hoi="Đại Nội",
                retrieval_service=_SlowService(),
                context_builder=_SlowBuilder(),
                trace=trace,
            )
        finally:
            hb.cancel()
            await asyncio.gather(hb, return_exceptions=True)
        return ticks

    ticks = asyncio.run(_measure())
    # Tổng blocking = 0.25 s; nếu chạy trên event loop thì ticks sẽ <= 1, còn chạy qua to_thread thì ticks >= 6.
    assert ticks >= 6
