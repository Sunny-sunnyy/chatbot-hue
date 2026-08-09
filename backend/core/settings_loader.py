"""Load application settings from config/settings.yaml."""
import yaml
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
SETTINGS_PATH = BACKEND_DIR / "config" / "settings.yaml"


def load_settings():
    """Load settings from YAML and return them as a dict."""
    with SETTINGS_PATH.open() as file:
        settings = yaml.safe_load(file)
    _validate_active_profile(settings)
    return settings


def _validate_active_profile(settings):
    """Raise ValueError when active_profile does not resolve to a profile."""
    active = settings.get("active_profile")
    profiles = settings.get("profiles", {})
    if active not in profiles:
        raise ValueError(
            f"Unknown active_profile: {active!r}. Valid profiles: {sorted(profiles)}"
        )
