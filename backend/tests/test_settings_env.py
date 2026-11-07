"""Phase 12 bản deploy: biến môi trường ghi đè đúng 2 giá trị của `settings.yaml`; không đặt ⇒ giống hệt file (máy User không đổi)."""
import copy

import pytest
import yaml

from core.settings_loader import SETTINGS_PATH, apply_env_overrides, load_settings


def from_file() -> dict:
    return yaml.safe_load(SETTINGS_PATH.read_text())


def test_no_env_keeps_file_values(monkeypatch):
    monkeypatch.delenv("HUE_QDRANT_URL", raising=False)
    monkeypatch.delenv("HUE_TRA_WEB", raising=False)
    assert load_settings(validate_private_paths=False) == from_file()


def test_env_overrides_only_the_two_values():
    base = from_file()
    got = copy.deepcopy(base)
    apply_env_overrides(got, {"HUE_QDRANT_URL": "http://qdrant:6335", "HUE_TRA_WEB": "false"})
    assert got["vector_database"]["url"] == "http://qdrant:6335" and got["assistant"]["tra_web"] is False
    got["vector_database"]["url"], got["assistant"]["tra_web"] = base["vector_database"]["url"], base["assistant"]["tra_web"]
    assert got == base


@pytest.mark.parametrize("value", ["0", "False", "no", ""])
def test_bad_web_flag_fails_closed(value):
    with pytest.raises(ValueError):
        apply_env_overrides(from_file(), {"HUE_TRA_WEB": value})
