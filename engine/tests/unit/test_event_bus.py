from engine import EventData, EventTypeEnum, KeyInputEnum
from engine.core.event_bus import EngineEventBus


def test_event_bus_separation():
    bus = EngineEventBus()
    results = []

    def on_up(event: EventData):
        results.append("UP_PROCESSED")
        bus.emit(EventData(type=EventTypeEnum.INPUT, name=KeyInputEnum.DOWN))

    def on_down(event: EventData):
        results.append("DOWN_PROCESSED")

    bus.subscribe(KeyInputEnum.UP, on_up)
    bus.subscribe(KeyInputEnum.DOWN, on_down)

    bus.emit(EventData(type=EventTypeEnum.INPUT, name=KeyInputEnum.UP))

    bus.process()
    assert "UP_PROCESSED" in results
    assert "DOWN_PROCESSED" not in results

    bus.process()
    assert "DOWN_PROCESSED" in results
