import logging
import logging.config
import json
import os


def setup_logger(name: str) -> logging.Logger:
    log_dir = "logs"
    config_path = "logger.config.json"

    # Ensure directory exists before logger tries to write to it
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        # Emergency fallback to a simple file log if the config is missing
        logging.basicConfig(
            filename=os.path.join(log_dir, "latest.log"),
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.warning(
            "Logging config file missing. Falling back to basic file logging."
        )

    return logging.getLogger(name)
