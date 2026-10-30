"""Harness Qwen3-8B (B92): lịch thử lại và cache batch — logic thuần, không gọi OpenRouter."""
import numpy as np
import pytest

from experiments.phase_8_2.qwen3_8b import load_cached_batch, retry_wait, save_cached_batch


def test_retry_wait_only_for_429_5xx_and_timeout():
    assert retry_wait(0, 400, None) is None
    assert retry_wait(0, 401, None) is None
    assert retry_wait(0, None, None) == 10.0  # timeout
    assert retry_wait(1, 504, None) == 30.0
    assert retry_wait(2, 500, None) == 90.0


def test_retry_wait_429_takes_max_of_schedule_and_retry_after():
    assert retry_wait(0, 429, "45") == 45.0
    assert retry_wait(2, 429, "45") == 90.0
    assert retry_wait(0, 429, "Wed, 21 Oct 2026 07:28:00 GMT") == 10.0  # dạng ngày giờ ⇒ theo lịch


def test_cached_batch_round_trip_and_stops_on_changed_texts(tmp_path):
    texts = ["đoạn một", "đoạn hai"]
    matrix = np.arange(8, dtype=np.float32).reshape(2, 4)
    assert load_cached_batch(tmp_path, 0, texts) is None
    save_cached_batch(tmp_path, 0, texts, matrix, "Nebius")
    loaded, provider = load_cached_batch(tmp_path, 0, texts)
    assert provider == "Nebius" and np.array_equal(loaded, matrix)
    with pytest.raises(ValueError, match="different texts"):
        load_cached_batch(tmp_path, 0, ["đoạn một", "đoạn hai đã sửa"])
