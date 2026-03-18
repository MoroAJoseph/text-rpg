from unittest.mock import MagicMock
from engine.managers.input import InputManager
from engine.core.event_bus import EngineEventBus
from engine import KeyInputEnum, InputStateEnum, EventTypeEnum, InputEvent


def test_input_manager_emits_single_event_to_bus():
    # 1. Setup local bus and manager
    bus = EngineEventBus()
    manager = InputManager(bus=bus)

    mock_provider = MagicMock()
    mock_provider.poll.return_value = [
        InputEvent(key=KeyInputEnum.SPACE, state=InputStateEnum.PRESSED, timestamp=1.0),
        InputEvent(key=KeyInputEnum.SPACE, state=InputStateEnum.PRESSED, timestamp=1.1),
    ]
    manager.register_provider(mock_provider)

    # 2. Update
    manager.update()

    # 3. Verify exactly 1 event reached the injected bus
    assert len(bus._next_queue) == 1
    event = bus._next_queue[0]
    assert event.type == EventTypeEnum.INPUT
    assert event.name == KeyInputEnum.SPACE
