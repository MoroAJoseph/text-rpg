from enum import Enum, auto

from engine.core.bus import EventBus
from engine.core.models import EventData
from engine.core.enums import EventTypeEnum
from engine.domains.input.enums import KeyInputEnum


class MockEventName(Enum):
    TEST_A = auto()
    TEST_B = auto()


def test_bus_double_buffering():
    bus = EventBus()
    processed = []

    def on_a(event):
        processed.append("A")
        # Emit B during processing of A
        bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=MockEventName.TEST_B))

    bus.subscribe_to_name(MockEventName.TEST_A, on_a)
    bus.subscribe_to_name(MockEventName.TEST_B, lambda e: processed.append("B"))

    bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=MockEventName.TEST_A))

    # First process: only A should be handled
    bus.process()
    assert "A" in processed
    assert "B" not in processed

    # Second process: B (emitted during A) is handled
    bus.process()
    assert "B" in processed


def test_subscribe_by_type():
    bus = EventBus()
    type_hits = 0

    def on_input_type(event):
        nonlocal type_hits
        type_hits += 1

    bus.subscribe_to_type(EventTypeEnum.INPUT, on_input_type)

    bus.emit(EventData(type=EventTypeEnum.INPUT, name=MockEventName.TEST_A))
    bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=MockEventName.TEST_B))

    bus.process()
    assert type_hits == 1  # Should ignore the SYSTEM event


def test_event_bus_separation():
    bus = EventBus()
    results = []

    def on_up(event: EventData):
        results.append("UP_PROCESSED")
        # Emit during process to test double buffering
        bus.emit(EventData(type=EventTypeEnum.INPUT, name=KeyInputEnum.DOWN))

    bus.subscribe_to_name(KeyInputEnum.UP, on_up)
    bus.subscribe_to_name(KeyInputEnum.DOWN, lambda e: results.append("DOWN_PROCESSED"))

    bus.emit(EventData(type=EventTypeEnum.INPUT, name=KeyInputEnum.UP))

    bus.process()
    assert "UP_PROCESSED" in results
    assert "DOWN_PROCESSED" not in results  # Still in next queue

    bus.process()
    assert "DOWN_PROCESSED" in results
