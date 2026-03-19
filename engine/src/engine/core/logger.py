import logging
import logging.config
import json
import os
from typing import Optional


class Logger:
    def __init__(self, log_dir: str = "logs", config_path: Optional[str] = None):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self._setup_fallback() if not config_path else self._load_config(config_path)

    def _load_config(self, path: str):
        with open(path, "r") as f:
            logging.config.dictConfig(json.load(f))

    def _setup_fallback(self):
        log_path = os.path.join(self.log_dir, "engine.log")
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        if root.hasHandlers():
            root.handlers.clear()

        handler = logging.FileHandler(log_path)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        )
        root.addHandler(handler)

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)


SYSTEM_LOGGER = logging.getLogger("ENGINE")
API_LOGGER = logging.getLogger("API")
