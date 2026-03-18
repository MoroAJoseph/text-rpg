import logging
import logging.config
import json
import os
from typing import Optional


class LogManager:
    """Manages system-wide logging instances and configurations."""

    def __init__(self, log_dir: str = "logs", config_path: Optional[str] = None):
        self.log_dir = log_dir
        self._ensure_log_dir()

        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
        else:
            self._setup_fallback()

    def _ensure_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _load_config(self, path: str):
        with open(path, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)

    def _setup_fallback(self):
        log_path = os.path.join(self.log_dir, "engine.log")
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Clear existing handlers to ensure our fallback takes root
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)


SYSTEM_LOGGER = logging.getLogger("ENGINE")
API_LOGGER = logging.getLogger("API")
