from unittest.mock import MagicMock
from engine.api.system import SystemAPI
from engine.core.enums import EventTypeEnum, SystemEventEnum


def test_system_api_stop_emits_event():
    engine = MagicMock()
    api = SystemAPI(engine)

    api.stop()

    # Verify the correct event was emitted to the bus
    args, _ = engine.ctx.bus.emit.call_args
    event = args[0]
    assert event.type == EventTypeEnum.SYSTEM
    assert event.name == SystemEventEnum.STOP
