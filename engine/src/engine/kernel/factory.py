from typing import Any, Dict, Optional, Union
from ..config.loader import ConfigLoader
from .engine import Engine
from .context import CTX


def create_engine(config_source: Optional[Union[str, Dict[str, Any]]] = None) -> Engine:
    """
    Entry point to initialize the Blackbox Kernel.

    Args:
        config_source: Can be a file path (str), a raw dictionary, or None to trigger automatic discovery.
    """
    if config_source is None or isinstance(config_source, str):
        # Trigger discovery (TOML -> JSON) or load specific path
        config = ConfigLoader.discover_and_load(config_source)
    elif isinstance(config_source, dict):
        # Direct dictionary injection
        config = ConfigLoader.load_from_dict(config_source)
    else:
        raise TypeError("config_source must be a path (str), a dict, or None.")

    # Boot the global context logger
    CTX.log_manager.get_logger(config.log_level)

    return Engine(config)
