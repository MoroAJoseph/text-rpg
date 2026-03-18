import pytest
from engine import (
    create_engine,
    EngineOptions,
    EventData,
    EventTypeEnum,
    SystemEventEnum,
)
from engine.api.system import SystemAPI
from engine.api.events import EventsAPI


@pytest.fixture
def engine():
    """Provides a fresh, isolated engine instance for each test."""
    return create_engine(EngineOptions())


def test_system_api_emits_start(engine):
    # Inject the engine instance
    api = SystemAPI(engine)
    api.start()

    # Check the bus belonging to THIS engine instance
    event = engine.ctx.bus._next_queue[0]
    assert event.type == EventTypeEnum.SYSTEM
    assert event.name == SystemEventEnum.ENGINE_START


def test_events_api_subscription(engine):
    # Inject the engine instance
    api = EventsAPI(engine)
    called = False

    def callback(event: EventData):
        nonlocal called
        called = True

    api.on(SystemEventEnum.ENGINE_TICK, callback)

    # Trigger the bus on this specific instance
    test_event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK)
    engine.ctx.bus.emit(test_event)
    engine.ctx.bus.process()

    assert called is True
