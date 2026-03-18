import pytest
from unittest.mock import MagicMock
from engine import EventsAPI
from engine.core import EventData, EventTypeEnum, SystemEventEnum


@pytest.fixture
def mock_engine():
    """Provides a mocked engine with a real bus for subscription testing."""
    engine = MagicMock()
    # We use a real bus here because the API's job is to interact with it
    from engine.core import EngineEventBus

    engine.ctx.bus = EngineEventBus()
    return engine


def test_events_api_subscription(mock_engine):
    """Verify that 'on' correctly registers a callback on the bus."""
    api = EventsAPI(mock_engine)
    received = False

    def callback(event: EventData):
        nonlocal received
        received = True

    # Subscribe to a system tick
    api.on(SystemEventEnum.ENGINE_TICK, callback)

    # Manually emit the event on the engine's bus
    event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK)
    mock_engine.ctx.bus.emit(event)
    mock_engine.ctx.bus.process()

    assert received is True


def test_events_api_multiple_listeners(mock_engine):
    """Ensure multiple callbacks can subscribe to the same event."""
    api = EventsAPI(mock_engine)
    results = []

    api.on(SystemEventEnum.ENGINE_START, lambda e: results.append("A"))
    api.on(SystemEventEnum.ENGINE_START, lambda e: results.append("B"))

    event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_START)
    mock_engine.ctx.bus.emit(event)
    mock_engine.ctx.bus.process()

    assert "A" in results
    assert "B" in results
    assert len(results) == 2


def test_events_api_emit_passthrough(mock_engine):
    """Verify the API can emit events back onto the bus."""
    api = EventsAPI(mock_engine)

    test_event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_STOP)

    api.emit(test_event)

    # Check if it landed in the bus's queue
    assert len(mock_engine.ctx.bus._next_queue) == 1
    assert mock_engine.ctx.bus._next_queue[0].name == SystemEventEnum.ENGINE_STOP
