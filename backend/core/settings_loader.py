"""Load application settings from config/settings.yaml."""
from pathlib import Path

import yaml


BACKEND_DIR = Path(__file__).resolve().parents[1]
SETTINGS_PATH = BACKEND_DIR / "config" / "settings.yaml"


def load_settings():
    """Load settings and reject an unknown active retrieval profile."""
    with SETTINGS_PATH.open() as file:
        settings = yaml.safe_load(file)
    active_profile = settings.get("active_profile")
    profiles = settings.get("profiles", {})
    if active_profile not in profiles:
        raise ValueError(
            f"Unknown active_profile: {active_profile!r}. "
            f"Valid profiles: {sorted(profiles)}"
        )
    return settings
