import pytest
from unittest.mock import MagicMock, patch
from engine.kernel.engine import Engine
from engine.config.models import EngineConfig


@pytest.fixture
def engine():
    # Use a minimal config to avoid bootstrap complexity
    config = EngineConfig(tick_rate=60)
    with patch("engine.kernel.engine.Engine._bootstrap_domains"):
        return Engine(config)


def test_engine_update_cycle_flow(engine):
    # Mock the bus and a manager
    engine.ctx.bus = MagicMock()
    mock_mgr = MagicMock()
    engine.managers.add("test", mock_mgr)

    engine.update()

    # Verify the 3-Flush Cycle: bus.process() should be called 3 times
    assert engine.ctx.bus.process.call_count == 3
    # Manager should be updated once
    mock_mgr.update.assert_called_once()


def test_engine_handles_stop_event(engine):
    engine.ctx.running = True
    # Simulate the callback that would be triggered by the bus
    engine._handle_exit(None)
    assert engine.ctx.running is False
