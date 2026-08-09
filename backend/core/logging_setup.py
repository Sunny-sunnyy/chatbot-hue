"""Configure logging from config/logging.yaml."""
import logging.config
import yaml
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
LOGGING_CONFIG_PATH = BACKEND_DIR / "config" / "logging.yaml"
LOGS_DIR = BACKEND_DIR / "logs"
LOG_FILE_NAME = "application.log"


def setup_logging():
    """Apply logging config; log files are written to BACKEND_DIR/logs."""
    LOGS_DIR.mkdir(exist_ok=True)
    with LOGGING_CONFIG_PATH.open() as file:
        config = yaml.safe_load(file)
    config["handlers"]["file"]["filename"] = str(LOGS_DIR / LOG_FILE_NAME)
    logging.config.dictConfig(config)
