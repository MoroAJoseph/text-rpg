import pytest
from dataclasses import asdict
from engine.config.loader import ConfigLoader
from engine.kernel.engine import Engine
from engine.kernel.factory import create_engine
from engine.api.factory import connect


@pytest.fixture
def test_env():
    # Force Input domain enabled
    raw_config = {
        "engine": {"tick_rate": 60, "rates": {}},
        "features": {
            "input": {
                "enabled": True,
                "default_poll_rate": 60.0,
                "decay_threshold": 0.12,
                "capabilities": {
                    "keyboard": {"driver": "blessed", "enabled": True},
                    "mouse": {"driver": "blessed", "enabled": True},
                },
            }
        },
    }
    config = ConfigLoader.load_from_dict(raw_config)
    engine = Engine(config)
    api = connect(engine)

    # Critical: Start the engine to trigger manager registration
    # Some managers only register during the first startup/update phase
    return engine, api
