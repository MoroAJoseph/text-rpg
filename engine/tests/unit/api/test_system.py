import pytest
from engine import (
    create_engine,
    EngineOptions,
    SystemEventEnum,
)
from engine.api import SystemAPI


@pytest.fixture
def engine():
    return create_engine(EngineOptions())


def test_system_api_emits_start(engine):
    api = SystemAPI(engine)
    api.start()

    # Peek into the bus queue
    events = list(engine.ctx.bus._next_queue)

    # Verify ENGINE_START exists in the queue
    start_event = next(
        (e for e in events if e.name == SystemEventEnum.ENGINE_START), None
    )
    assert start_event is not None
