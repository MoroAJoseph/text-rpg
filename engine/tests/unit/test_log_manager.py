import os
import json
import logging
from engine.managers.log import LogManager


def test_log_manager_creates_dir(tmp_path):
    log_dir = tmp_path / "test_logs"
    assert not log_dir.exists()
    _ = LogManager(log_dir=str(log_dir))
    assert log_dir.exists()


def test_log_manager_fallback_on_missing_config(tmp_path):
    log_dir = tmp_path / "logs"
    bad_config = tmp_path / "non_existent.json"

    manager = LogManager(log_dir=str(log_dir), config_path=str(bad_config))
    logger = manager.get_logger("TEST_FALLBACK")
    logger.info("Fallback test message")

    for handler in logging.getLogger().handlers:
        handler.flush()
        handler.close()

    log_file = log_dir / "engine.log"
    assert log_file.exists()


def test_log_manager_loads_valid_config(tmp_path):
    log_dir = tmp_path / "logs"
    config_file = tmp_path / "config.json"

    config_data = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": str(log_dir / "custom.log"),
            }
        },
        "root": {"handlers": ["file"], "level": "INFO"},
    }

    os.makedirs(log_dir)
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    manager = LogManager(log_dir=str(log_dir), config_path=str(config_file))
    logger = manager.get_logger("CUSTOM")
    logger.info("Config test")
    assert (log_dir / "custom.log").exists()
